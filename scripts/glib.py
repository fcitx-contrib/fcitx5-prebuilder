import os
from common import PLATFORM, ROOT, MesonBuilder, ensure, patch

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

MesonBuilder(project, [
    '-Dtests=false',
    '-Dintrospection=disabled',
    '-Dxattr=false'
]).exec()
