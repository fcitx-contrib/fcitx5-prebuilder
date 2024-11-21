import os

from common import MakeBuilder, ensure

class Pcre2Builder(MakeBuilder):
    def configure(self):
        if not os.path.exists('configure'):
            ensure('autoreconf', ['-i'])
        super().configure()

Pcre2Builder('pcre2').exec()
