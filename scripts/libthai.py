from common import CMakeBuilder, patch

project = 'libthai'

patch(project, 'libthai.cmake', 'CMakeLists.txt')

CMakeBuilder(project).exec()
