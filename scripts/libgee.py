from common import MakeBuilder, patch

project = 'libgee'

patch(project)

MakeBuilder(project).exec()
