from common import CMakeBuilder, patch

project = 'libpinyin'
patch(project)

CMakeBuilder(project).exec()
