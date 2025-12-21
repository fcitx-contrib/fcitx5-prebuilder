import os
from common import INSTALL_PREFIX, OHOS_ARCH, MakeBuilder, ensure

os.environ['SOURCE_DATE_EPOCH'] = '0' # Reproducible: crypto/buildinf.h

class OpenSSLBuilder(MakeBuilder):
    def configure(self):
        arch = 'linux-aarch64' if OHOS_ARCH == 'arm64-v8a' else 'linux-x86_64'
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

    def pre_package(self):
        ensure('rm', ['-rf',
            f'{self.dest_dir}{INSTALL_PREFIX}/bin',
            f'{self.dest_dir}{INSTALL_PREFIX}/ssl'
        ])

OpenSSLBuilder('openssl').exec()
