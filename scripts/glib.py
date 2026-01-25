import os
from common import INSTALL_PREFIX, PLATFORM, ROOT, MesonBuilder, ensure, patch, sed

with open('.glib-version') as f:
    version = f.read().strip()
project = 'glib'

# Make sure glib selects proxy-libintl
if PLATFORM == 'js':
    os.chdir('glib')
    branch = f'fcitx-{version}'
    # Originally https://github.com/kleisauke/glib
    ensure('git', ['fetch', 'https://github.com/fcitx-contrib/glib', f'{branch}:{branch}'])
    ensure('git', ['checkout', branch])
    os.chdir(ROOT)
else:
    patch(project)

class GLibBuilder(MesonBuilder):
    def pre_package(self):
        sed(f'{self.dest_dir}{INSTALL_PREFIX}/lib/pkgconfig/gio-2.0.pc', '"s|-lintl||g"') # kkc
        if PLATFORM == 'js':
            sed(f'{self.dest_dir}{INSTALL_PREFIX}/lib/pkgconfig/gmodule-no-export-2.0.pc', '"s|-pthread||g"') # kkc
            sed(f'{self.dest_dir}{INSTALL_PREFIX}/lib/pkgconfig/glib-2.0.pc', '"s|-pthread||g"') # kkc and skk

GLibBuilder(project, [
    '-Dtests=false',
    '-Dlibffi:tests=false',
    '-Dintrospection=disabled',
    '-Dxattr=false'
]).exec()
