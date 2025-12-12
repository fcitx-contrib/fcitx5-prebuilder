import os
from common import Builder, CARGO_TARGET, INSTALL_PREFIX, ROOT, ensure, patch

project = 'cskk'
patch(project)


class CskkBuilder(Builder):
    def build(self):
        os.environ['RUSTFLAGS'] = f'--remap-path-prefix={ROOT}/{project}=.' # Reproducible: absolute path
        ensure('cargo', ['build', '--release', '--features=capi', f'--target={CARGO_TARGET}'])
        ensure('cbindgen', ['--output', 'libcskk.h', 'cskk'])

    def install(self):
        usr = f'{self.dest_dir}{INSTALL_PREFIX}'
        include_dir = f'{usr}/include'
        lib_dir = f'{usr}/lib'
        pkgconfig_dir = f'{lib_dir}/pkgconfig'
        share_dir = f'{usr}/share/libcskk'

        ensure('mkdir', ['-p', include_dir, pkgconfig_dir, share_dir])
        ensure('cp', ['libcskk.h', include_dir])
        ensure('cp', [f'target/{CARGO_TARGET}/release/libcskk.a', lib_dir])
        ensure('cp', [f'{ROOT}/patches/cskk.pc', pkgconfig_dir])

        for directory in ('rule', 'rules'):
            ensure('cp', ['-r', f'assets/{directory}', share_dir])

CskkBuilder(project).exec()
