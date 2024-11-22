from common import CMakeBuilder

CMakeBuilder('fmt', [
    '-DFMT_TEST=OFF',
    '-DFMT_DOC=OFF'
]).exec()
