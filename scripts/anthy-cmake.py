import os

from common import CMakeBuilder, INSTALL_PREFIX, ensure

class AnthyBuilder(CMakeBuilder):
    def pre_package(self):
        cwd = os.getcwd()
        os.chdir('anthy-unicode')
        ensure('./autogen.sh', [])
        ensure('make', ['-j8'])
        anthy_dict_dir = f'{self.dest_dir}{INSTALL_PREFIX}/share/anthy'
        ensure('mkdir', ['-p', anthy_dict_dir])
        ensure('touch', [f'{anthy_dict_dir}/anthy-unicode.conf']) # for fcitx5-anthy to locate
        ensure('cp', ['mkanthydic/anthy.dic', anthy_dict_dir])
        os.chdir(cwd)

AnthyBuilder('anthy-cmake').exec()
