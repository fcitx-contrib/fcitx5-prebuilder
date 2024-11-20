import os

from common import CMakeBuilder, ROOT, USR, ensure, patch

project = 'librime'

patch(project)
patch('librime-lua')

os.chdir('librime/plugins')
for plugin in ('lua', 'octagram', 'predict'):
    if not os.path.islink(plugin):
        ensure('ln', ['-s', f'../../librime-{plugin}', plugin])
os.chdir(ROOT)

CMakeBuilder(project, [
    '-DBUILD_TOOLS=OFF', # propagate to plugins
    '-DBUILD_TEST=OFF',
    '-DBUILD_MERGED_PLUGINS=ON',
    '-DENABLE_EXTERNAL_PLUGINS=OFF',
    f'-DLUA_INCLUDE_DIR={ROOT}/build/{USR}/include/lua',
    f'-DLUA_TARGET={ROOT}/build/{USR}/lib/liblua.a'
], js=['-DENABLE_THREADING=OFF']).exec()
