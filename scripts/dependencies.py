dag = {
    'curl': ['openssl'],
    'glib': ['pcre2'],
    'json-glib': ['glib'],
    'libgee': ['glib'],
    'librime': ['boost', 'glog', 'leveldb', 'lua', 'marisa', 'opencc', 'yaml-cpp'],
    'libskk': ['json-glib', 'libgee', 'libxkbcommon'],
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
    'json',
    'json-c',
    'json-glib',
    'leveldb',
    'libchewing',
    'libexpat',
    'libgee',
    'libhangul',
    'libintl',
    'libmozc',
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

windows = [
    'json',
    'libuv'
]

ios = [
    'boost',
    'curl',
    'ecm',
    'fmt',
    'glog',
    'json',
    'json-c',
    'leveldb',
    'libintl',
    'libmozc',
    'librime',
    'libuv',
    'lua',
    'marisa',
    'opencc',
    'yaml-cpp',
    'zstd'
]

harmony = [
    'boost',
    'curl',
    'ecm',
    'fmt',
    'json',
    'libintl',
    'lua',
    'marisa',
    'opencc',
    'openssl',
    'zstd'
]

js = [
    'anthy-cmake',
    'boost',
    'ecm',
    'fmt',
    'glog',
    'iso-codes',
    'json',
    'json-c',
    'leveldb',
    'libchewing',
    'libexpat',
    'libhangul',
    'libmozc',
    'librime',
    'libthai',
    'libxkbcommon',
    'lua',
    'marisa',
    'opencc',
    'xkeyboard-config',
    'yaml-cpp',
    'zstd'
]

platform_projects = {
    'macos': macos,
    'windows': windows,
    'ios': ios,
    'harmony': harmony,
    'js': js
}
