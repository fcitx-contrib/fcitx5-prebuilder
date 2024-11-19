import os
import platform
import sys
from typing import Callable, Literal, cast

from dependencies import dag

MACOS_VERSION = 13
IOS_VERSION = 15

PLATFORM_VERSION = {
    'macos': MACOS_VERSION,
    'ios': IOS_VERSION
}

PLATFORM = cast(Literal['macos', 'ios', 'js'], sys.argv[1])
POSTFIX = '-' + platform.machine() if PLATFORM == 'macos' or 'simulator' in sys.argv[2:] else ''
IOS_PLATFORM = 'SIMULATOR' if 'simulator' in sys.argv[2:] else 'OS'
ROOT = os.getcwd()

INSTALL_PREFIX = '/usr'
# macos-x86_64, ios-arm64, js
TARGET = f'{PLATFORM}{POSTFIX}'
# macos-x86_64/usr, ios-arm64/usr, js/usr
USR = f'{TARGET}{INSTALL_PREFIX}'


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
        ensure('git', [
            'apply',
            f'--directory={project}',
            f'patches/{project}.patch'
        ])


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


class Builder:
    def __init__(self, name: str, options: list[str] | None=None, src='.', build='build', pre_package: Callable[[], None] | None=None):
        self.name = name
        # /path/to/build/ios-arm64/librime
        self.dest_dir = f'{ROOT}/build/{TARGET}/{self.name}'
        self.options = options or []
        self.src = src
        self.build_ = f'build/{TARGET}'
        self.needs_extract = any(name in deps for deps in dag.values())
        self.pre_package = pre_package

    def configure(self):
        pass

    def build(self):
        pass

    def install(self):
        pass

    def package(self):
        pass

    def extract(self):
        pass

    def exec(self):
        self.configure()
        self.build()
        self.install()
        if self.pre_package:
            self.pre_package()
        self.package()
        if self.needs_extract:
            self.extract()


class CMakeBuilder(Builder):
    def configure(self):
        os.environ['PKG_CONFIG_PATH'] = f'{ROOT}/build/{USR}/lib/pkgconfig'
        os.chdir(f'{ROOT}/{self.name}')
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

        if PLATFORM == 'ios':
            command += [
                f'-DCMAKE_TOOLCHAIN_FILE={ROOT}/ios.cmake',
                f'-DIOS_PLATFORM={IOS_PLATFORM}'
            ]

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

    def package(self):
        os.chdir(f'{self.dest_dir}{INSTALL_PREFIX}')
        ensure('tar', ['cjf', f'{self.dest_dir}{POSTFIX}.tar.bz2', '*'])

    def extract(self):
        directory = f'build/{USR}'
        os.chdir(ROOT)
        ensure('mkdir', ['-p', directory])
        ensure('tar', ['xjf', f'{self.dest_dir}{POSTFIX}.tar.bz2', '-C', directory])
