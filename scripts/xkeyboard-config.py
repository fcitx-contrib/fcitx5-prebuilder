from common import MesonBuilder, ensure

class XKeyboardConfigBuilder(MesonBuilder):
    def pre_package(self):
        # Remove X11 to avoid unpack symlink failure on Windows (f5h).
        ensure('rm', ['-rf', f'{self.dest_dir}/usr/share/X11'])
        # Remove xkeyboard-config-2.mo which is just a duplicate and not registered by fcitx5.
        ensure('find', [self.dest_dir, '-name', 'xkeyboard-config-2.mo', '-delete'])

XKeyboardConfigBuilder('xkeyboard-config').exec()
