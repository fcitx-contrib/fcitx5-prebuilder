from common import MesonBuilder, patch

project = 'glib'

# Make sure glib selects proxy-libintl
patch(project)

MesonBuilder(project, [
    '-Dtests=false',
    '-Dintrospection=disabled'
]).exec()
