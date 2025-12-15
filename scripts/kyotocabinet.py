from common import INSTALL_PREFIX, MakeBuilder, ensure, patch


project = 'kyotocabinet'
patch(project) # hard-coded include directory

class KyotoCabinetBuilder(MakeBuilder):
    target = 'libkyotocabinet.a'

    def install(self):
        usr = f'{self.dest_dir}{INSTALL_PREFIX}'
        include_dir = f'{usr}/include'
        lib_dir = f'{usr}/lib'
        pkgconfig_dir = f'{lib_dir}/pkgconfig'
        ensure('mkdir', ['-p', include_dir, pkgconfig_dir])
        ensure('cp', ['k*.h', include_dir])
        ensure('cp', [self.target, lib_dir])
        ensure('cp', ['kyotocabinet.pc', pkgconfig_dir])

KyotoCabinetBuilder(project, js=['--disable-zlib']).exec()
