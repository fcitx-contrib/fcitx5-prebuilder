from common import PLATFORM, ROOT, USR, CMakeBuilder, patch, rmrf, steal

project = "opencc"

if PLATFORM != "macos":
    steal(project)

patch(project)


class OpenCCBuilder(CMakeBuilder):
    def pre_package(self):
        # Remove jieba_dict to decrease installer size by 5MB.
        rmrf(f"{self.dest_dir}/usr/share/opencc/jieba_dict")


OpenCCBuilder(
    project,
    # libopencc-jieba.so unable to find library -lmarisa
    ["-DUSE_SYSTEM_MARISA=ON", "-DENABLE_PLUGINS=OFF"],
    includes=[f"{ROOT}/build/{USR}/include"],
).exec()
