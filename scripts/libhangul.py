from common import CMakeBuilder, patch

project = 'libhangul'

patch(project)

CMakeBuilder(project, [
    '-DENABLE_EXTERNAL_KEYBOARDS=OFF',
    '-DENABLE_UNIT_TEST=OFF'
]).exec()
