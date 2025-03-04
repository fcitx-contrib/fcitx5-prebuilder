import os
import platform
import subprocess
import sys
from typing import Literal, cast

from dependencies import dag

MACOS_VERSION = 13.3 # Also need to update meson-macos-*.ini
IOS_VERSION = 15

PLATFORM_VERSION = {
    'macos': MACOS_VERSION,
    'ios': IOS_VERSION
}

PLATFORM = cast(Literal['macos', 'windows', 'ios', 'harmony', 'js'], sys.argv[1])
MACOS_ARCH = sys.argv[2] if PLATFORM == 'macos' else ''
WINDOWS_ARCH = sys.argv[2] if PLATFORM == 'windows' else ''
IOS_PLATFORM = cast(Literal['OS64', 'SIMULATOR64', 'SIMULATORARM64'], sys.argv[2]) if PLATFORM == 'ios' else ''
IOS_ARCH = 'x86_64' if IOS_PLATFORM == 'SIMULATOR64' else 'arm64'
OHOS_ARCH = sys.argv[2] if PLATFORM == 'harmony' else ''
OHOS_TARGET = f'{'aarch64' if OHOS_ARCH == 'arm64-v8a' else 'x86_64'}-linux-ohos'

if PLATFORM == 'macos':
    POSTFIX = '-' + MACOS_ARCH
elif PLATFORM == 'windows':
    POSTFIX = '-' + WINDOWS_ARCH
elif PLATFORM == 'harmony':
    POSTFIX = '-' + OHOS_ARCH
elif PLATFORM == 'ios' and IOS_PLATFORM != 'OS64':
    POSTFIX = '-' + IOS_ARCH
else: # iOS real device or JS
    POSTFIX = ''

if PLATFORM in ('macos', 'ios'):
    os.environ['ZERO_AR_DATE'] = '1' # Reproducible: timestamp of __.SYMDEF SORTED and .o in .a

ROOT = os.getcwd()

INSTALL_PREFIX = '/usr'
# macos-x86_64, ios-arm64, js, harmony-arm64-v8a
TARGET = f'{PLATFORM}{POSTFIX}'
# macos-x86_64/usr, ios-arm64/usr, js/usr
USR = f'{TARGET}{INSTALL_PREFIX}'

DEBUG = os.environ.get('DEBUG') == '1'

HARMONY_NATIVE = '/tmp/command-line-tools/sdk/default/openharmony/native'

tar = {
    'Linux': 'tar',
    'Windows': 'C:/msys64/usr/bin/tar.exe',
}.get(platform.system(), 'gtar')

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
        '-nv', # boost progress bar produces too many lines.
        '-P',
        'cache',
        url
    ])


def steal(package: str, directories: tuple[str, ...] = ('share',)):
    # Steal data from native build.
    prebuilt = f'{package}-{platform.machine()}.tar.bz2'
    url = f'https://github.com/fcitx-contrib/fcitx5-prebuilder/releases/download/macos/{prebuilt}'

    cache(url)
    directory = f'build/{TARGET}/{package}{INSTALL_PREFIX}'
    ensure('mkdir', ['-p', directory])
    ensure(tar, [
        'xjf',
        f'cache/{prebuilt}',
        '-C',
        directory,
        *directories
    ])


def get_platform_cflags() -> str:
    if PLATFORM == 'macos':
        return f'-arch {MACOS_ARCH} -mmacosx-version-min={MACOS_VERSION}'
    if PLATFORM == 'ios':
        arch = f'-arch {IOS_ARCH}'
        if IOS_PLATFORM == 'OS64':
            sdk = f'-isysroot {subprocess.check_output("xcrun --sdk iphoneos --show-sdk-path", shell=True, text=True).strip()}'
            version = f'-miphoneos-version-min={IOS_VERSION}'
        else:
            sdk = f'-isysroot {subprocess.check_output("xcrun --sdk iphonesimulator --show-sdk-path", shell=True, text=True).strip()}'
            version = f'-mios-simulator-version-min={IOS_VERSION}'
        return ' '.join((arch, sdk, version))
    return ''


class Builder:
    def __init__(self, name: str, options: list[str] | None=None, js: list[str] | None=None,
                 macos: list[str] | None=None,
                 ios: list[str] | None=None, harmony: list[str] | None=None, src='.',
                 definitions: list[str] | None=None, includes: list[str] | None=None):
        self.name = name
        # /path/to/build/ios-arm64/librime
        self.dest_dir = f'{ROOT}/build/{TARGET}/{self.name}'
        self.options = options or []
        self.src = src
        self.build_ = f'build/{TARGET}'
        self.needs_extract = any(name in deps for deps in dag.values())
        self.macos = macos or []
        self.js = js or []
        self.ios = ios or []
        self.harmony = harmony or []
        self.definitions = definitions or []
        self.includes = includes or []

    def configure(self):
        pass

    def build(self):
        pass

    def install(self):
        pass

    def strip(self):
        lib_dir = f'{self.dest_dir}{INSTALL_PREFIX}/lib'
        if not os.path.exists(lib_dir):
            return
        all_a = f'{lib_dir}/*.a'
        if PLATFORM == 'harmony':
            ensure(f'{HARMONY_NATIVE}/llvm/bin/llvm-strip', ['--strip-unneeded', all_a])
        elif PLATFORM == 'js':
            ensure('emstrip', ['--strip-unneeded', all_a])
        elif PLATFORM == 'windows':
            all_lib = f'{lib_dir}/*.lib'
            ensure('llvm-strip', ['--strip-unneeded', all_lib])
        else:
            ensure('strip', ['-x', all_a])

    def pre_package(self):
        pass

    def package(self):
        os.chdir(f'{self.dest_dir}{INSTALL_PREFIX}')
        os.environ['LC_ALL'] = 'C'
        ensure(tar, ['cj',
            '--sort=name', '--mtime=@0',
            '--numeric-owner', '--owner=0', '--group=0', '--mode=go+u,go-w',
            '--force-local', # Don't interpret C: as remote address.
            '-f', f'{self.dest_dir}{POSTFIX}.tar.bz2', '*'
        ])

    def extract(self):
        directory = f'build/{USR}'
        os.chdir(ROOT)
        ensure('mkdir', ['-p', directory])
        ensure(tar, ['xf', f'{self.dest_dir}{POSTFIX}.tar.bz2', '-C', directory])

    def exec(self):
        os.chdir(f'{ROOT}/{self.name}')
        self.configure()
        self.build()
        self.install()
        if not DEBUG:
            self.strip()
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
            '-G', 'Ninja',
            '-S', self.src,
            '-DBUILD_SHARED_LIBS=OFF',
            f'-DCMAKE_BUILD_TYPE={"Debug" if DEBUG else "Release"}',
            f'-DCMAKE_INSTALL_PREFIX={INSTALL_PREFIX}',
            f'-DCMAKE_FIND_ROOT_PATH={ROOT}/build/{USR}'
        ]

        if PLATFORM == 'harmony':
            command += [
                f'-DCMAKE_TOOLCHAIN_FILE={HARMONY_NATIVE}/build/cmake/ohos.toolchain.cmake',
                f'-DOHOS_ARCH={OHOS_ARCH}'
            ]
            command += self.harmony

        if PLATFORM == 'ios':
            # PLATFORM is recognized by ios.toolchain.cmake.
            command += [
                f'-DCMAKE_TOOLCHAIN_FILE={ROOT}/ios-cmake/ios.toolchain.cmake',
                '-DENABLE_STRICT_TRY_COMPILE=ON', # leveldb: https://github.com/leetal/ios-cmake/issues/47, https://gitlab.kitware.com/cmake/cmake/-/issues/18121
                f'-DPLATFORM={IOS_PLATFORM}'
            ]
            command += self.ios

        c_cxx_flags = f'-ffile-prefix-map={os.path.abspath(self.src)}=.' # Reproducible: __FILE__
        if self.definitions:
            c_cxx_flags += ' ' + ' '.join(f'-D{definition}' for definition in self.definitions)
        if self.includes:
            c_cxx_flags += ' ' + ' '.join(f'-I{include}' for include in self.includes)

        if PLATFORM == 'windows':
            c_cxx_flags += ' -mno-incremental-linker-compatible' # Reproducible: TimeDateStamp in llvm: WinCOFFObjectWriter.cpp

        if PLATFORM == 'js':
            # emscripten defaults to full-static libs but we want plugins based on these dependencies to be dynamic.
            c_cxx_flags += ' -fPIC'
            command += self.js

        if PLATFORM == 'macos':
            command += [
                f'-DCMAKE_OSX_DEPLOYMENT_TARGET={PLATFORM_VERSION[PLATFORM]}',
                f'-DCMAKE_OSX_ARCHITECTURES={MACOS_ARCH}'
            ]
            command += self.macos
        elif PLATFORM == 'ios':
            command.append(f'-DDEPLOYMENT_TARGET={PLATFORM_VERSION[PLATFORM]}') # ios.toolchain.cmake overrides CMAKE_OSX_DEPLOYMENT_TARGET anyway.

        command += [
            f'-DCMAKE_C_FLAGS="{c_cxx_flags}"',
            f'-DCMAKE_CXX_FLAGS="{c_cxx_flags}"'
        ]

        ensure(command[0], [
            *command[1:],
            *self.options
        ])

    def build(self):
        ensure('cmake', ['--build', self.build_])

    def install(self):
        os.environ['DESTDIR'] = self.dest_dir
        ensure('cmake', ['--install', self.build_, *(['> /dev/null'] if self.name == 'boost' else [])])


class MesonBuilder(Builder):
    def configure(self):
        os.environ['PKG_CONFIG_SYSROOT_DIR'] = f'{ROOT}/build/{TARGET}'
        os.environ['PKG_CONFIG_LIBDIR'] = f'{ROOT}/build/{USR}/lib/pkgconfig'
        ensure('meson', [
            'setup',
            self.build_,
            f'--cross-file={ROOT}/scripts/meson-cross-js.ini' if PLATFORM == 'js' else f'--cross-file={ROOT}/scripts/meson-macos-{MACOS_ARCH}.ini',
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
