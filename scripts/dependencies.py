dag = {
    'librime': ['boost', 'glog', 'leveldb', 'marisa', 'opencc', 'yaml-cpp'],
    'opencc': ['marisa'],
}

macos = [
    'anthy-cmake',
    'boost',
    'default-icon-theme',
    'fmt',
    'glib',
    'glog',
    'iso-codes',
    'json-c',
    'json-glib',
    'leveldb',
    'libchewing',
    'libexpat',
    'libgee',
    'libhangul',
    'libintl',
    'librime',
    'libskk',
    'libthai',
    'libuv',
    'libxkbcommon',
    'lua',
    'marisa',
    'opencc',
    'pcre2',
    'xkeyboard-config',
    'yaml-cpp',
    'zstd'
]

ios = [
    'boost',
    'fmt',
    'glog',
    'json-c',
    'leveldb',
    'libintl',
    'librime',
    'libuv',
    'marisa',
    'opencc',
    'yaml-cpp',
    'zstd'
]

js = [
    'boost',
    'extra-cmake-modules',
    'fmt',
    'glog',
    'iso-codes',
    'json-c',
    'leveldb',
    'libexpat',
    'librime',
    'libthai',
    'libxkbcommon',
    'marisa',
    'opencc',
    'xkeyboard-config',
    'yaml-cpp',
    'zstd'
]

platform_projects = {
    'macos': macos,
    'ios': ios,
    'js': js
}
