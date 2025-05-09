import os
from common import CMakeBuilder, MACOS_ARCH, PLATFORM, cache, ensure

version = '1.88.0'

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

libs = "algorithm;bimap;container;crc;interprocess;iostreams;multi_index;ptr_container;scope_exit;signals2;uuid"

if PLATFORM == 'macos':
    libs += ';beast'

BOOST_CONTEXT_ABI = {
    'arm64': 'aapcs',
    'x86_64': 'sysv'
}.get(MACOS_ARCH)

CMakeBuilder('boost', [
    f'-DBOOST_INCLUDE_LIBRARIES="{libs}"',
    '-DBOOST_IOSTREAMS_ENABLE_BZIP2=Off',
    '-DBOOST_IOSTREAMS_ENABLE_ZLIB=Off',
    '-DBOOST_IOSTREAMS_ENABLE_LZMA=Off',
    '-DBOOST_IOSTREAMS_ENABLE_ZSTD=Off'
], macos=[
    f'-DBOOST_CONTEXT_ABI={BOOST_CONTEXT_ABI}',
    f'-DBOOST_CONTEXT_ARCHITECTURE={MACOS_ARCH}'
]).exec()
