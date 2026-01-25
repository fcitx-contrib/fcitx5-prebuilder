from common import Builder, INSTALL_PREFIX, PLATFORM, ROOT, HARMONY_NATIVE, OHOS_ARCH, ensure, get_platform_cflags, patch

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
        match PLATFORM:
            case 'macos':
                # Enable dlopen for librime-cloud
                cflags += ' -DLUA_USE_MACOSX'
            case 'ios':
                cflags += ' -DLUA_USE_IOS'
            case 'harmony':
                cflags += f' -fPIC --target={'aarch64' if OHOS_ARCH == 'arm64-v8a' else 'x86_64'}-linux-ohos'
            case 'js':
                cflags += ' -fPIC'

        command += [
            'make',
            'a',
            '-j8',
            f'CFLAGS="{cflags}"'
        ]

        match PLATFORM:
            case 'js':
                command += [
                    'CC=emcc',
                    'AR="emar q"',
                    'RANLIB=emranlib'
                ]
            case 'harmony':
                command += [
                    f'CC={HARMONY_NATIVE}/llvm/bin/clang',
                    f'AR="{HARMONY_NATIVE}/llvm/bin/llvm-ar rc"',
                    f'RANLIB={HARMONY_NATIVE}/llvm/bin/llvm-ranlib'
                ]

        ensure(command[0], command[1:])

    def install(self):
        usr = self.dest_dir + INSTALL_PREFIX
        include_lua_dir = usr + '/include/lua'
        lib_dir = usr + '/lib'
        ensure('mkdir', ['-p', include_lua_dir, lib_dir])
        ensure('cp', [
            'lua.h',
            'luaconf.h',
            'lualib.h',
            'lauxlib.h',
            f'{ROOT}/patches/lua.hpp',
            include_lua_dir
        ])
        ensure('cp', ['liblua.a', lib_dir])

LuaBuilder('lua').exec()
