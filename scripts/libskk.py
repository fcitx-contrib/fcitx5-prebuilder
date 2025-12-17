import os

from common import MakeBuilder, XDG_DATA_DIRS, patch

project = 'libskk'

# Fix build without gobject-introspection, disable tools and tests
patch(project)

# valac uses it to locate gee-0.8.vapi
os.environ['XDG_DATA_DIRS'] = XDG_DATA_DIRS

MakeBuilder(project, ['--disable-docs']).exec()
