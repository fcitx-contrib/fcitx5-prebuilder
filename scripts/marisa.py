from common import CMakeBuilder

disable_tools = '-DENABLE_TOOLS=OFF'

CMakeBuilder('marisa',
    js=[disable_tools],
    harmony=[disable_tools],
    ios=[disable_tools]
).exec()
