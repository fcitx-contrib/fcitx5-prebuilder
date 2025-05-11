from common import CMakeBuilder

CMakeBuilder('m17n-cmake',
    definitions=['M17NDIR=\\"\\\\\\"/usr/share/m17n\\\\\\"\\"']
).exec()
