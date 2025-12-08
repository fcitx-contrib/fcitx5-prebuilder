from common import CMakeBuilder, INSTALL_PREFIX, MACOS_ARCH, PLATFORM, ensure, patch, steal

project = 'libchewing'

patch(project)

if PLATFORM != 'macos':
    steal(project)

cargo_target = ''
if PLATFORM == 'macos':
    cargo_target = f'{MACOS_ARCH.replace('arm64', 'aarch64')}-apple-darwin'
elif PLATFORM == 'js':
    cargo_target = 'wasm32-unknown-emscripten'


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
    f'-DRust_CARGO_TARGET={cargo_target}'
]).exec()
