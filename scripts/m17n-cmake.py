from common import CMakeBuilder, patch

# Remove dlopen.
patch('m17n-cmake/m17n-lib')

CMakeBuilder('m17n-cmake',
    definitions=['M17NDIR=\\"\\\\\\"/usr/share/m17n\\\\\\"\\"']
).exec()
