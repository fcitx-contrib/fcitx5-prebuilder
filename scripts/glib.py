import os
import subprocess
from common import PLATFORM, ROOT, MesonBuilder, ensure, patch

project = 'glib'

# Make sure glib selects proxy-libintl
if PLATFORM == 'js':
    os.chdir('glib')
    version = subprocess.check_output("git describe", shell=True, text=True).strip()
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
