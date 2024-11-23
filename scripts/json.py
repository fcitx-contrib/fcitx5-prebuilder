from common import CMakeBuilder

CMakeBuilder('json', [
    '-DJSON_BuildTests=OFF'
]).exec()
