from common import CMakeBuilder, patch

project = 'leveldb'

# Disable tools.
# ios: disable Werror.
# js: disable threads. 
patch(project)

CMakeBuilder(project, [
    '-DLEVELDB_BUILD_BENCHMARKS=OFF',
    '-DLEVELDB_BUILD_TESTS=OFF'
]).exec()
