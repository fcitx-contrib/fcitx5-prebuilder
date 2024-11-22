from common import CMakeBuilder

CMakeBuilder('zstd', [
    '-DZSTD_LEGACY_SUPPORT=OFF',
    '-DZSTD_BUILD_PROGRAMS=OFF',
    '-DZSTD_BUILD_TESTS=OFF',
    '-DZSTD_BUILD_SHARED=OFF'
], js=['-DZSTD_MULTITHREAD_SUPPORT=OFF'],
src='build/cmake').exec()
