from common import CMakeBuilder, INSTALL_PREFIX, ensure

class MozcBuilder(CMakeBuilder):
    def build(self):
        ensure('cmake', ['--build', self.build_, '--target', 'absl_flags_parse'])
        ensure('cmake', ['--build', self.build_, '--target', 'mozc-static'])

    def install(self):
        usr_dir = f'{self.dest_dir}{INSTALL_PREFIX}'
        bin_dir = f'{usr_dir}/bin'
        mozc_include_dir = f'{usr_dir}/include/mozc'
        dictionary_include_dir = f'{mozc_include_dir}/dictionary'
        protocol_include_dir = f'{mozc_include_dir}/protocol'
        usage_stats_include_dir = f'{mozc_include_dir}/usage_stats'
        lib_dir = f'{usr_dir}/lib'
        ensure('mkdir', [
            '-p',
            bin_dir,
            dictionary_include_dir,
            protocol_include_dir,
            usage_stats_include_dir,
            lib_dir
        ])
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
        ensure('libtool', [
            '-o', f'{lib_dir}/libabsl.a',
            f'$(find {self.build_}/mozc/src/third_party/abseil-cpp -name "*.a")'
        ])

MozcBuilder('libmozc', [
    '-DBUILD_MOZC_ADDON=OFF'
]).exec()
