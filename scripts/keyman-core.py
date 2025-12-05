from common import MesonBuilder, patch

project = 'keyman-core'
patch(project)

MesonBuilder(project, [
    '-Ddebug=false', # Reproducible: absolute path
    '-Dkeyman_core_tests=false'
]).exec()
