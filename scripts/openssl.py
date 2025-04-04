import os
from common import HARMONY_NATIVE, INSTALL_PREFIX, OHOS_ARCH, OHOS_TARGET, PLATFORM, Builder, ensure, patch

project = 'openssl'

patch(project)

os.environ['SOURCE_DATE_EPOCH'] = '0' # Reproducible: crypto/buildinf.h

class OpenSSLBuilder(Builder):
    def configure(self):
        arch = 'ohos-aarch64' if OHOS_ARCH == 'arm64-v8a' else 'ohos-x86_64'
        ensure('./Configure', [
            arch,
            f'--prefix={INSTALL_PREFIX}',
            '--libdir=lib',
            '-static',
            'no-apps',
            'no-docs',
            'no-tests',
            *self.options
        ])

    def build(self):
        ensure('make', ['clean'])
        command = []

        cflags = ['-O3', '-fPIC']
        if PLATFORM == 'harmony':
            cflags += [f'--target={OHOS_TARGET}']

        command += [
            'make',
            '-j8',
            f'CFLAGS="{' '.join(cflags)}"'
        ]

        if PLATFORM == 'harmony':
            command += [
                f'CC={HARMONY_NATIVE}/llvm/bin/clang',
                f'AR="{HARMONY_NATIVE}/llvm/bin/llvm-ar"',
                f'RANLIB={HARMONY_NATIVE}/llvm/bin/llvm-ranlib'
            ]

        ensure(command[0], command[1:])

    def install(self):
        ensure('make', ['install', f'DESTDIR={self.dest_dir}'])

    def pre_package(self):
        ensure('rm', ['-rf',
            f'{self.dest_dir}{INSTALL_PREFIX}/bin',
            f'{self.dest_dir}{INSTALL_PREFIX}/ssl'
        ])

OpenSSLBuilder(project).exec()
