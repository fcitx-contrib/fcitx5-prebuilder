import os
from common import MesonBuilder, ensure

NEEDED_JSON = 'iso_639-3.json'
# The only translation we need: language code/name when system doesn't recognize.
# iso_639_3.mo is a symlink to it, which causes extraction error on Windows (f5h).
NEEDED_MO = 'iso_639-3.mo'

class IsoCodesBuilder(MesonBuilder):
    def pre_package(self):
        # Keep only the needed .json file.
        json_path = f'{self.dest_dir}/usr/share/iso-codes/json'
        for filename in os.listdir(json_path):
            if filename != NEEDED_JSON:
                os.remove(f'{json_path}/{filename}')

        # Keep only the needed .mo file.
        locale_path = f'{self.dest_dir}/usr/share/locale'
        for code in os.listdir(locale_path):
            code_path = f'{locale_path}/{code}'
            lc_messages_path = f'{code_path}/LC_MESSAGES'
            filenames = os.listdir(lc_messages_path)
            if '@' not in code and NEEDED_MO in filenames:
                for mo in filenames:
                    if mo != NEEDED_MO:
                        os.remove(f'{lc_messages_path}/{mo}')
            else:
                ensure('rm', ['-rf', code_path])            

IsoCodesBuilder('iso-codes').exec()
