import platform
import subprocess
from common import CMakeBuilder, INSTALL_PREFIX, PLATFORM, ROOT, ensure

no_addon = '-DBUILD_MOZC_ADDON=OFF'

if PLATFORM == 'js':
    native = {
        'Linux': 'linux',
        'Darwin': 'macos'
    }[platform.system()] + '-' + platform.machine()
    build_dir = f'libmozc/build/{native}'
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


class MozcBuilder(CMakeBuilder):
    def build(self):
        ensure('cmake', ['--build', self.build_, '--target', 'absl_flags_parse'])
        ensure('cmake', ['--build', self.build_, '--target', 'libprotobuf'])
        ensure('cmake', ['--build', self.build_, '--target', 'mozc-static'])

    def install(self):
        usr_dir = f'{self.dest_dir}{INSTALL_PREFIX}'
        mozc_include_dir = f'{usr_dir}/include/mozc'
        dictionary_include_dir = f'{mozc_include_dir}/dictionary'
        protocol_include_dir = f'{mozc_include_dir}/protocol'
        usage_stats_include_dir = f'{mozc_include_dir}/usage_stats'
        lib_dir = f'{usr_dir}/lib'
        ensure('mkdir', [
            '-p',
            dictionary_include_dir,
            protocol_include_dir,
            usage_stats_include_dir,
            lib_dir
        ])

        if PLATFORM == 'macos':
            bin_dir = f'{usr_dir}/bin'
            ensure('mkdir', ['-p', bin_dir])
            ensure('cp', [f'{self.build_}/protoc', bin_dir]) # iOS needs it.

        ensure('cp', [f'{self.build_}/dictionary/pos_matcher_impl.inc', dictionary_include_dir])
        ensure('cp', [f'{self.build_}/protocol/*.pb.h', protocol_include_dir])
        ensure('cp', [f'{self.build_}/usage_stats/usage_stats.pb.h', usage_stats_include_dir])
        ensure('cp', [
            f'{self.build_}/mozc/src/third_party/protobuf/third_party/utf8_range/libutf8_validity.a',
            f'{self.build_}/mozc/src/third_party/protobuf/libprotobuf.a',
            f'{self.build_}/libmozc-static.a',
            lib_dir
        ])

        libabsl_a = f'{lib_dir}/libabsl.a'
        all_libabsl_a = f'$(find {self.build_}/mozc/src/third_party/abseil-cpp -name "*.o")'
        ensure('ar', ['rc', libabsl_a, all_libabsl_a])


options = [no_addon]
if PLATFORM == 'js':
    options.append(f'-DPROTOC_EXECUTABLE={protoc_exe}')

MozcBuilder('libmozc', options).exec()
