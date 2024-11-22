from common import CMakeBuilder

CMakeBuilder('libuv', [
    '-DLIBUV_BUILD_SHARED=OFF',
    '-DLIBUV_BUILD_TESTS=OFF'
]).exec()
