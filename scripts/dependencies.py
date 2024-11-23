dag = {
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
    'lua',
    'marisa',
    'opencc',
    'yaml-cpp',
    'zstd'
]

js = [
    'boost',
    'ecm',
    'fmt',
    'glog',
    'iso-codes',
    'json',
    'json-c',
    'leveldb',
    'libexpat',
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
    'ios': ios,
    'js': js
}
