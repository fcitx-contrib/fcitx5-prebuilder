from common import CMakeBuilder

CMakeBuilder('libhangul', [
    '-DENABLE_EXTERNAL_KEYBOARDS=OFF',
    '-DENABLE_UNIT_TEST=OFF',
    '-DENABLE_TOOLS=OFF'
]).exec()
