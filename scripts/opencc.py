from common import CMakeBuilder, PLATFORM, ROOT, USR, patch, steal

project = 'opencc'

if PLATFORM != 'macos':
    steal(project)

patch(project)

CMakeBuilder(project, [
    f'-DCMAKE_CXX_FLAGS=-I{ROOT}/build/{USR}/include',
    '-DUSE_SYSTEM_MARISA=ON',
    '-DENABLE_DARTS=OFF'
]).exec()
