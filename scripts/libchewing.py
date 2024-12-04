from common import CMakeBuilder, PLATFORM, patch, steal

project = 'libchewing'

patch(project)

if PLATFORM != 'macos':
    steal(project)

CMakeBuilder(project, [
    '-DWITH_SQLITE3=OFF',
    '-DBUILD_TESTING=OFF',
    '-DWITH_RUST=OFF'
]).exec()
