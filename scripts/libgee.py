import os
import platform

from common import MakeBuilder, ensure, patch

project = 'libgee'

patch(project)

class LibgeeBuilder(MakeBuilder):
    def configure(self):
        if not os.path.exists('configure'):
            os.environ['NOCONFIGURE'] = '1'
            ensure('./autogen.sh', [])
        super().configure()

LibgeeBuilder(project, [
    f'--host={platform.machine()}',
]).exec()
