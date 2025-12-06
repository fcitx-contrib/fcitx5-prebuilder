from common import MesonBuilder, ensure, patch

project = 'keyman-core'
patch(project)

ensure('mkdir', ['-p', 'keyman-core/resources'])
ensure('cp', ['keyman/resources/build/meson/standard.meson.build', 'keyman-core/resources/meson.build'])

MesonBuilder(project, [
    '-Ddebug=false', # Reproducible: absolute path
    '-Dkeyman_core_tests=false'
]).exec()
