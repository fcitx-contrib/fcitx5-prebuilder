from common import MesonBuilder, patch

project = 'json-glib'

# Disable tools.
patch(project)

MesonBuilder(project, [
    '-Ddocumentation=disabled',
    '-Dtests=false',
    '-Dintrospection=disabled'
]).exec()
