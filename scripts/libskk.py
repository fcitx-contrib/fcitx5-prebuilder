import os

from common import MakeBuilder, XDG_DATA_DIRS, ensure, patch

project = 'libskk'

# Fix build without gobject-introspection, disable tools and tests
patch(project)

# valac uses it to locate gee-0.8.vapi
os.environ['XDG_DATA_DIRS'] = XDG_DATA_DIRS

class LibSkkBuilder(MakeBuilder):
    def configure(self):
        if not os.path.exists('configure'):
            ensure('autoreconf', ['-i'])
        super().configure()

LibSkkBuilder(project, ['--disable-docs']).exec()
