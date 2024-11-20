from common import CMakeBuilder

CMakeBuilder('ecm', [
    '-DBUILD_TESTING=OFF'
]).exec()
