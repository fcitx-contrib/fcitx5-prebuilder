from common import MesonBuilder, ensure, mkdir, patch

project = 'keyman-core'
patch(project)

mkdir('keyman-core/resources')
ensure('cp', ['keyman/resources/build/meson/standard.meson.build', 'keyman-core/resources/meson.build'])

MesonBuilder(project, [
    '-Ddebug=false', # Reproducible: absolute path
    '-Dkeyman_core_tests=false'
]).exec()
