import os
import platform

from common import MakeBuilder, ROOT, USR, TARGET, ensure, patch

project = 'libskk'

# Fix build without gobject-introspection, disable tools and tests
patch(project)

os.environ['PKG_CONFIG_SYSROOT_DIR'] = f'{ROOT}/build/{TARGET}'
os.environ['PKG_CONFIG_PATH'] = f'{ROOT}/build/{USR}/lib/pkgconfig'
os.environ['XDG_DATA_DIRS'] = f'{ROOT}/build/{USR}/share'

class LibSkkBuilder(MakeBuilder):
    def configure(self):
        if not os.path.exists('configure'):
            ensure('autoreconf', ['-i'])
        super().configure()

LibSkkBuilder(project, [
    '--disable-docs',
    f'--host={platform.machine()}'
]).exec()
