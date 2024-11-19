from common import CMakeBuilder

CMakeBuilder('yaml-cpp', [
    '-DYAML_CPP_BUILD_CONTRIB=OFF',
    '-DYAML_CPP_BUILD_TESTS=OFF',
    '-DYAML_CPP_BUILD_TOOLS=OFF'
]).exec()
