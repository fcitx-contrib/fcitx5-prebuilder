import os
from common import CMakeBuilder, POSTFIX, ROOT, TARGET, cache, ensure

version = '1.86.0'

boost_dir = f'boost-{version}'
boost_tar = f'{boost_dir}-cmake.tar.xz'
url = f'https://github.com/boostorg/boost/releases/download/{boost_dir}/{boost_tar}'
cache(url)

if os.path.isdir('boost'):
    pattern = 'VERSION ' + version.replace('.', '\\.')
    if os.system(f"grep '{pattern}' boost/CMakeLists.txt") != 0:
        # Version mismatch
        ensure('rm', ['-rf', 'boost'])

if not os.path.isdir('boost'):
    ensure('tar', [
        'xJf',
        f'cache/{boost_tar}',
        '-C',
        '.'
    ])
    ensure('mv', [
        f'{boost_dir}',
        'boost'
    ])

# For js, but harmless for non-windows platform so no need to revert.
file = 'boost/libs/container/include/boost/container/detail/thread_mutex.hpp'
ensure('sed', [
    '-i.bak',
    '"s/#if defined(BOOST_HAS_PTHREADS)/#if 1/"',
    file
])
ensure('rm ', ['-f', file + '.bak'])

CMakeBuilder('boost', [
    '-DBOOST_INCLUDE_LIBRARIES="algorithm;bimap;container;crc;interprocess;iostreams;multi_index;ptr_container;scope_exit;signals2;uuid"',
    '-DBOOST_IOSTREAMS_ENABLE_BZIP2=Off',
    '-DBOOST_IOSTREAMS_ENABLE_ZLIB=Off',
    '-DBOOST_IOSTREAMS_ENABLE_LZMA=Off',
    '-DBOOST_IOSTREAMS_ENABLE_ZSTD=Off'
]).exec()
