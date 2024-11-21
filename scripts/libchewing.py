from common import CMakeBuilder, patch

project = 'libchewing'

patch(project)

CMakeBuilder(project, [
    '-DWITH_SQLITE3=OFF',
    '-DBUILD_TESTING=OFF',
    '-DWITH_RUST=OFF'
]).exec()
