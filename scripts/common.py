import os
import platform
import subprocess
import sys
from typing import Literal, cast

from dependencies import dag

MACOS_VERSION = 13 # Also need to update meson-macos.ini
IOS_VERSION = 15

PLATFORM_VERSION = {
    'macos': MACOS_VERSION,
    'ios': IOS_VERSION
}

PLATFORM = cast(Literal['macos', 'ios', 'harmony', 'js'], sys.argv[1])
IOS_PLATFORM = 'SIMULATOR' if 'simulator' in sys.argv[2:] else 'OS'
OHOS_ARCH = sys.argv[2] if PLATFORM == 'harmony' else ''

if PLATFORM == 'macos' or IOS_PLATFORM == 'SIMULATOR':
    POSTFIX = '-' + platform.machine()
elif PLATFORM == 'harmony':
    POSTFIX = '-' + OHOS_ARCH
else: # iOS real device or JS
    POSTFIX = ''

ROOT = os.getcwd()

INSTALL_PREFIX = '/usr'
# macos-x86_64, ios-arm64, js, harmony-arm64-v8a
TARGET = f'{PLATFORM}{POSTFIX}'
# macos-x86_64/usr, ios-arm64/usr, js/usr
USR = f'{TARGET}{INSTALL_PREFIX}'

DEBUG = os.environ.get('DEBUG') == '1'

def ensure(program: str, args: list[str]):
    command = " ".join([program, *args])
    print(command)
    if os.system(command) != 0:
        raise Exception("Command failed")


def patch(project: str, src: str | None = None, dst: str | None = None):
    if src and dst:
        ensure('cp', [
            f'patches/{src}',
            f'{project}/{dst}'
        ])
    else:
        os.chdir(project)
        if os.system('git diff --ignore-submodules --exit-code') == 0:
            ensure('git', [
                'apply',
                f'{ROOT}/patches/{project.split("/")[-1]}.patch'
            ])
        os.chdir(ROOT)


def cache(url: str):
    file = url[url.rindex('/') + 1:]
    path = f'cache/{file}'
    if os.path.isfile(path):
        print(f'Using cached {file}')
        return
    ensure('wget', [
        '-P',
        'cache',
        url
    ])


def steal(package: str, directories: tuple[str, ...] = ('share',)):
    # Steal data from native build.
    # Use same arch for bin, e.g. protoc built on macOS x86_64 to build for iOS simulator.
    prebuilt = f'{package}-{platform.machine()}.tar.bz2'
    url = f'https://github.com/fcitx-contrib/fcitx5-prebuilder/releases/download/macos/{prebuilt}'

    cache(url)
    directory = f'build/{TARGET}/{package}{INSTALL_PREFIX}'
    ensure('mkdir', ['-p', directory])
    ensure('tar', [
        'xjf',
        f'cache/{prebuilt}',
        '-C',
        directory,
        *directories
    ])


def get_platform_cflags() -> str:
    if PLATFORM == 'macos':
        return f'-mmacosx-version-min={MACOS_VERSION}'
    if PLATFORM == 'ios':
        if IOS_PLATFORM == 'SIMULATOR':
            arch = f'-arch {platform.machine()}'
            sdk = f'-isysroot {subprocess.check_output("xcrun --sdk iphonesimulator --show-sdk-path", shell=True, text=True).strip()}'
            version = f'-mios-simulator-version-min={IOS_VERSION}'
        else:
            arch = '-arch arm64'
            sdk = f'-isysroot {subprocess.check_output("xcrun --sdk iphoneos --show-sdk-path", shell=True, text=True).strip()}'
            version = f'-miphoneos-version-min={IOS_VERSION}'
        return ' '.join((arch, sdk, version))
    return ''


class Builder:
    def __init__(self, name: str, options: list[str] | None=None, js: list[str] | None=None,
                 ios: list[str] | None=None, src='.'):
        self.name = name
        # /path/to/build/ios-arm64/librime
        self.dest_dir = f'{ROOT}/build/{TARGET}/{self.name}'
        self.options = options or []
        self.src = src
        self.build_ = f'build/{TARGET}'
        self.needs_extract = any(name in deps for deps in dag.values())
        self.js = js or []
        self.ios = ios or []

    def configure(self):
        pass

    def build(self):
        pass

    def install(self):
        pass

    def pre_package(self):
        pass

    def package(self):
        os.chdir(f'{self.dest_dir}{INSTALL_PREFIX}')
        ensure('tar', ['cjf', f'{self.dest_dir}{POSTFIX}.tar.bz2', '*'])

    def extract(self):
        directory = f'build/{USR}'
        os.chdir(ROOT)
        ensure('mkdir', ['-p', directory])
        ensure('tar', ['xjf', f'{self.dest_dir}{POSTFIX}.tar.bz2', '-C', directory])

    def exec(self):
        os.chdir(f'{ROOT}/{self.name}')
        self.configure()
        self.build()
        self.install()
        self.pre_package()
        self.package()
        if self.needs_extract:
            self.extract()


class CMakeBuilder(Builder):
    def configure(self):
        command = ['emcmake'] if PLATFORM == 'js' else []
        command += [
            'cmake',
            '-B', self.build_,
            '-G', 'Xcode' if PLATFORM == 'ios' else 'Ninja',
            '-S', self.src,
            '-DBUILD_SHARED_LIBS=OFF',
            f'-DCMAKE_INSTALL_PREFIX={INSTALL_PREFIX}',
            f'-DCMAKE_FIND_ROOT_PATH={ROOT}/build/{USR}'
        ]

        if PLATFORM == 'harmony':
            command += [
                '-DCMAKE_TOOLCHAIN_FILE=/tmp/command-line-tools/sdk/default/openharmony/native/build/cmake/ohos.toolchain.cmake',
                f'-DOHOS_ARCH={OHOS_ARCH}'
            ]

        if PLATFORM == 'ios':
            # IOS_PLATFORM is recognized by ios.cmake.
            command += [
                f'-DCMAKE_TOOLCHAIN_FILE={ROOT}/ios.cmake',
                f'-DIOS_PLATFORM={IOS_PLATFORM}'
            ]
            command += self.ios
        else: # Ninja
            command.append(f'-DCMAKE_BUILD_TYPE={"Debug" if DEBUG else "Release"}')

        if PLATFORM == 'js':
            # emscripten defaults to full-static libs but we want plugins based on these dependencies to be dynamic.
            command += [
                '-DCMAKE_C_FLAGS=-fPIC',
                '-DCMAKE_CXX_FLAGS=-fPIC'
            ]
            command += self.js

        if PLATFORM in ('macos', 'ios'):
            command.append(f'-DCMAKE_OSX_DEPLOYMENT_TARGET={PLATFORM_VERSION[PLATFORM]}')

        ensure(command[0], [
            *command[1:],
            *self.options
        ])

    def build(self):
        command = ['--build', self.build_]
        if PLATFORM == 'ios':
            command += ['--config', 'Release']
        ensure('cmake', command)

    def install(self):
        os.environ['DESTDIR'] = self.dest_dir
        ensure('cmake', ['--install', self.build_])


class MesonBuilder(Builder):
    def configure(self):
        ensure('meson', [
            'setup',
            self.build_,
            f'--cross-file={ROOT}/scripts/meson-cross-js.ini' if PLATFORM == 'js' else f'--native-file={ROOT}/scripts/meson-macos.ini',
            '--buildtype=release',
            f'--prefix={INSTALL_PREFIX}',
            '--default-library=static',
            *self.options
        ])

    def build(self):
        ensure('ninja', ['-C', self.build_])

    def install(self):
        os.environ['DESTDIR'] = self.dest_dir
        ensure('ninja', ['-C', self.build_, 'install'])


class MakeBuilder(Builder):
    def configure(self):
        ensure('./configure', [
            '-C',
            f'--prefix={INSTALL_PREFIX}',
            *self.options
        ])

    def build(self):
        ensure('make', ['-j8', f'CFLAGS="{get_platform_cflags()}"'])

    def install(self):
        os.environ['DESTDIR'] = self.dest_dir
        ensure('make', ['install'])
