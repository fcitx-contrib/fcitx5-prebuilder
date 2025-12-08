import os

from common import MakeBuilder, XDG_DATA_DIRS, ensure, patch

project = 'libkkc'

# Disable gobject-introspection.
# Disable tools and data.
# Intl.bindtextdomain is not available on emscripten.
patch(project)
# Use vapi generated on Linux with gobject-introspection.
ensure('cp', ['patches/marisa-glib.vapi', 'libkkc/marisa-glib'])

# valac uses it to locate gee-0.8.vapi
os.environ['XDG_DATA_DIRS'] = XDG_DATA_DIRS

class LibkkcBuilder(MakeBuilder):
    def configure(self):
        if not os.path.exists('configure'):
            ensure('autoreconf', ['-i'])
        super().configure()

LibkkcBuilder(project).exec()
