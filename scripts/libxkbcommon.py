from common import MesonBuilder, patch

project = 'libxkbcommon'

patch(project)

MesonBuilder(project, [
    '-Denable-tools=false',
    '-Denable-x11=false',
    '-Denable-docs=false',
    '-Denable-wayland=false',
    '-Denable-bash-completion=false',
    '-Denable-xkbregistry=false'
]).exec()
