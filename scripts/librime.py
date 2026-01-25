import os

from common import CMakeBuilder, INSTALL_PREFIX, ROOT, USR, ensure, patch

project = 'librime'

# vertical-lr
# persistent set_option
# no trash "deprecated" default.yaml
patch(project)
patch('librime-lua')
patch('librime-qjs')

os.chdir('librime/plugins')
for plugin in ('lua', 'octagram', 'predict', 'qjs'):
    if not os.path.islink(plugin):
        ensure('ln', ['-s', f'../../librime-{plugin}', plugin])
os.chdir(ROOT)


class LibrimeBuilder(CMakeBuilder):
    def install(self):
        super().install()
        ensure('cp', [
            f'{ROOT}/librime-qjs/build/libqjs.a',
            f'{self.dest_dir}{INSTALL_PREFIX}/lib'
        ])


LibrimeBuilder(project, [
    '-DBUILD_TOOLS=OFF', # propagate to plugins
    '-DBUILD_TEST=OFF',
    '-DBUILD_MERGED_PLUGINS=ON',
    '-DENABLE_EXTERNAL_PLUGINS=OFF',
    f'-DLUA_INCLUDE_DIR={ROOT}/build/{USR}/include/lua',
    f'-DLUA_TARGET={ROOT}/build/{USR}/lib/liblua.a'
], js=['-DENABLE_THREADING=OFF'],
definitions=['BOOST_DISABLE_CURRENT_LOCATION']
).exec()
