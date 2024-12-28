import platform
from common import CMakeBuilder, IOS_PLATFORM, INSTALL_PREFIX, PLATFORM, ROOT, ensure, patch, steal

no_addon = '-DBUILD_MOZC_ADDON=OFF'
protoc_exe = ''
options = [no_addon]


class MozcBuilder(CMakeBuilder):
    def build(self):
        ios_release = ['--config', 'Release'] if PLATFORM == 'ios' else []
        ensure('cmake', ['--build', self.build_, '--target', 'absl_flags_parse', *ios_release])
        ensure('cmake', ['--build', self.build_, '--target', 'libprotobuf', *ios_release])
        ensure('cmake', ['--build', self.build_, '--target', 'mozc-static', *ios_release])

    def install(self):
        if PLATFORM == 'ios':
            layer = 'Release-iphone' + ('simulator' if IOS_PLATFORM == 'SIMULATOR' else 'os') + '/'
        else:
            layer = ''

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
            f'{self.build_}/mozc/src/third_party/protobuf/third_party/utf8_range/{layer}libutf8_validity.a',
            f'{self.build_}/mozc/src/third_party/protobuf/{layer}libprotobuf.a',
            lib_dir
        ])

        if PLATFORM == 'ios': # Xcode doesn't support add_library OBJECT and generates many static libs.
            ensure('ar', ['rc', f'{lib_dir}/libmozc-static.a', f'$(find {self.build_} -name "*.o" | grep build/mozc)'])
        else:
            ensure('cp', [f'{self.build_}/libmozc-static.a', lib_dir])

        libabsl_a = f'{lib_dir}/libabsl.a'
        if PLATFORM == 'ios':
            all_libabsl_a = f'$(find {self.build_} -name "*.o" | grep build/absl)'
        else:
            all_libabsl_a = f'$(find {self.build_}/mozc/src/third_party/abseil-cpp -name "*.o")'
        ensure('ar', ['rc', libabsl_a, all_libabsl_a])

    def pre_package(self):
        if PLATFORM != 'macos':
            ensure('rm', ['-rf', f'{self.dest_dir}/usr/bin'])


builder = MozcBuilder('libmozc', options)

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
    protoc_exe = f'{builder.dest_dir}/usr/bin/protoc'

if PLATFORM in ('ios', 'js'):
    options.append(f'-DPROTOC_EXECUTABLE={protoc_exe}')

builder.exec()
