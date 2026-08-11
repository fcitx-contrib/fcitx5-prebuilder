from common import PLATFORM, ROOT, USR, CMakeBuilder, patch, steal

project = "opencc"

if PLATFORM != "macos":
    steal(project)

patch(project)

CMakeBuilder(
    project,
    ["-DUSE_SYSTEM_MARISA=ON"],
    includes=[f"{ROOT}/build/{USR}/include"],
    # libopencc-jieba.so unable to find library -lmarisa
    ios=["-DENABLE_PLUGINS=OFF"],
    harmony=["-DENABLE_PLUGINS=OFF"],
    js=["-DENABLE_PLUGINS=OFF"],
).exec()
