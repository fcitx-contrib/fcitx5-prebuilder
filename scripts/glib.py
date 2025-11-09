import os
from common import INSTALL_PREFIX, PLATFORM, ROOT, MesonBuilder, ensure, patch

version = '2.87.0'
project = 'glib'

# Make sure glib selects proxy-libintl
if PLATFORM == 'js':
    os.chdir('glib')
    branch = f'fcitx-{version}'
    ensure('git', ['fetch', 'https://github.com/fcitx-contrib/glib', f'{branch}:{branch}'])
    ensure('git', ['checkout', branch])
    os.chdir(ROOT)
else:
    patch(project)

class GLibBuilder(MesonBuilder):
    def pre_package(self):
        if PLATFORM == 'js':
            file = f'{self.dest_dir}{INSTALL_PREFIX}/lib/pkgconfig/glib-2.0.pc'
            bak = f'{file}.bak'
            ensure('sed', ['-i.bak', '"s|-pthread||g"', file])
            ensure('rm', [bak])

GLibBuilder(project, [
    '-Dtests=false',
    '-Dintrospection=disabled',
    '-Dxattr=false'
]).exec()
