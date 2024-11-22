from common import MesonBuilder

MesonBuilder('json-glib', [
    '-Ddocumentation=disabled',
    '-Dtests=false',
    '-Dintrospection=disabled'
]).exec()
