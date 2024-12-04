from common import CMakeBuilder

CMakeBuilder('pcre2', [
    '-DPCRE2_BUILD_PCRE2GREP=OFF',
    '-DPCRE2_BUILD_TESTS=OFF'
]).exec()
