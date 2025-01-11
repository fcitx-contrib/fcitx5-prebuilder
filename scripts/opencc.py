from common import CMakeBuilder, PLATFORM, ROOT, USR, patch, steal

project = 'opencc'

if PLATFORM != 'macos':
    steal(project)

patch(project)

CMakeBuilder(project, [
    '-DUSE_SYSTEM_MARISA=ON',
    '-DENABLE_DARTS=OFF'
], includes=[f'{ROOT}/build/{USR}/include']).exec()
