from common import CMakeBuilder, INSTALL_PREFIX, PLATFORM, ROOT, TARGET, USR, cache, ensure, patch

project = 'opencc'

if PLATFORM != 'macos':
    # Steal data from native build.
    prebuilt = 'opencc-arm64.tar.bz2'
    url = f'https://github.com/fcitx-contrib/fcitx5-prebuilder/releases/download/macos/{prebuilt}'

    cache(url)
    directory = f'build/{TARGET}/opencc{INSTALL_PREFIX}'
    ensure('mkdir', ['-p', directory])
    ensure('tar', [
        'xjvf',
        f'cache/{prebuilt}',
        '-C',
        directory,
        'share'
    ])

patch(project)

CMakeBuilder(project, [
    f'-DCMAKE_CXX_FLAGS=-I{ROOT}/build/{USR}/include',
    '-DUSE_SYSTEM_MARISA=ON',
    '-DENABLE_DARTS=OFF'
]).exec()
