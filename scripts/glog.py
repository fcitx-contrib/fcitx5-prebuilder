from common import CMakeBuilder

CMakeBuilder('glog', [
    '-DWITH_GFLAGS=OFF',
    '-DWITH_UNWIND=OFF',
    '-DBUILD_EXAMPLES=OFF',
]).exec()
