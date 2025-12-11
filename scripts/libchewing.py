from common import CMakeBuilder, CARGO_TARGET, INSTALL_PREFIX, PLATFORM, ensure, patch, steal

project = 'libchewing'

patch(project)

if PLATFORM != 'macos':
    steal(project)


class ChewingBuilder(CMakeBuilder):
    def install(self):
        super().install()
        # libchewing.a only has an empty .c, which is only useful for building .so.
        ensure('cp', [
            f'{self.build_}/libchewing_capi.a',
            f'{self.dest_dir}{INSTALL_PREFIX}/lib/libchewing.a'
        ])


ChewingBuilder(project, [
    '-DWITH_SQLITE3=OFF',
    f'-DRust_CARGO_TARGET={CARGO_TARGET}'
]).exec()
