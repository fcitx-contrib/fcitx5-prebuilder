from common import CMakeBuilder

CMakeBuilder('libintl', [
    '-DCMAKE_POLICY_DEFAULT_CMP0054=NEW'
]).exec()
