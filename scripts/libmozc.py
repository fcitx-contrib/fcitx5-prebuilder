# macos -> macos: package protoc
# macos -> ios: steal protoc
# macos -> js: steal protoc
# linux -> js: build protoc first

import platform
from common import CMakeBuilder, INSTALL_PREFIX, PLATFORM, ROOT, cache, ensure, patch, steal

no_addon = '-DBUILD_MOZC_ADDON=OFF'
protoc_exe = ''
options = [no_addon]


class MozcBuilder(CMakeBuilder):
    def configure(self):
        super().configure()
        oss_dir = f'{self.build_}/data_manager/oss'
        ensure('mkdir', ['-p', oss_dir])
        ensure('ln', ['-sf', f'{ROOT}/cache/mozc_data.inc', f'{oss_dir}/mozc_data.inc'])

    def install(self):
        super().install()
        # Combine all .o files of absl to libabsl.a
        lib_dir = f'{self.dest_dir}{INSTALL_PREFIX}/lib'
        libabsl_a = f'{lib_dir}/libabsl.a'
        all_libabsl_o = f'$(find {self.build_}/mozc/src/third_party/abseil-cpp -name "*.o")'
        ensure('ar', ['rc', libabsl_a, all_libabsl_o])

    def pre_package(self):
        if PLATFORM != 'macos':
            ensure('rm', ['-rf', f'{self.dest_dir}{INSTALL_PREFIX}/bin'])


if PLATFORM == 'js':
    patch('libmozc/mozc')
    if platform.system() == 'Linux': # Nothing to steal so build it.
        build_dir = f'libmozc/build/linux-{platform.machine()}'
        ensure('cmake', [
            '-S', 'libmozc', '-B', build_dir,
            '-G', 'Ninja', '-DCMAKE_BUILD_TYPE=Release',
            no_addon
        ])
        ensure('cmake', [
            '--build', build_dir,
            '--target', 'protoc'
        ])
        protoc_exe = f'{ROOT}/{build_dir}/protoc'

if platform.system() == 'Darwin' and PLATFORM != 'macos':
    steal('libmozc', ('bin',)) # extracted to install dir so need to remove on prepack.
    protoc_exe = f'{MozcBuilder('libmozc').dest_dir}{INSTALL_PREFIX}/bin/protoc'

if PLATFORM in ('ios', 'js'):
    options.append(f'-DPROTOC_EXECUTABLE={protoc_exe}')

cache('https://github.com/fcitx-contrib/fcitx5-mozc/releases/download/latest/mozc_data.inc')

MozcBuilder('libmozc', options).exec()
