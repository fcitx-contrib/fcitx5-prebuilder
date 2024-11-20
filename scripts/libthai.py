from common import CMakeBuilder, patch

project = 'libthai'

patch(project, 'libthai.cmake', 'CMakeLists.txt')
patch(project, 'libthai.pc.in', '.')

CMakeBuilder(project).exec()
