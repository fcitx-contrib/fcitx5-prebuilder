from common import MesonBuilder, ensure

class XKeyboardConfigBuilder(MesonBuilder):
    def pre_package(self):
        # Remove X11 to avoid unpack symlink failure on Windows (f5h).
        ensure('rm', ['-rf', f'{self.dest_dir}/usr/share/X11'])

XKeyboardConfigBuilder('xkeyboard-config').exec()
