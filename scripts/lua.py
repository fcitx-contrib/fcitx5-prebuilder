from common import Builder, INSTALL_PREFIX, PLATFORM, ROOT, ensure, get_platform_cflags, patch

project = 'lua'

# ios: disable dlopen.
patch(project)

class LuaBuilder(Builder):
    def build(self):
        ensure('make', ['clean'])
        command = ['emmake'] if PLATFORM == 'js' else []

        cflags = '-O3'
        if PLATFORM in ('macos', 'ios'):
            cflags += ' ' + get_platform_cflags()
        if PLATFORM == 'macos':
            # Enable dlopen for librime-cloud
            cflags += ' -DLUA_USE_MACOSX'
        elif PLATFORM == 'ios':
            cflags += ' -DLUA_USE_IOS'
        elif PLATFORM == 'js':
            cflags += ' -fPIC'

        command += [
            'make',
            'a',
            '-j8',
            f'CFLAGS="{cflags}"'
        ]

        if PLATFORM == 'js':
            command += [
                'CC=emcc',
                'AR="emar q"',
                'RANLIB=emranlib'
            ]

        ensure(command[0], command[1:])

    def install(self):
        usr = self.dest_dir + INSTALL_PREFIX
        include_lua_dir = usr + '/include/lua'
        lib_dir = usr + '/lib'
        lib_pkgconfig_dir = lib_dir + '/pkgconfig'
        ensure('mkdir', ['-p', include_lua_dir, lib_pkgconfig_dir])
        ensure('cp', [
            'lua.h',
            'luaconf.h',
            'lualib.h',
            'lauxlib.h',
            f'{ROOT}/patches/lua.hpp',
            include_lua_dir
        ])
        ensure('cp', ['liblua.a', lib_dir])
        ensure('cp', [f'{ROOT}/patches/lua.pc', lib_pkgconfig_dir])


LuaBuilder('lua').exec()
