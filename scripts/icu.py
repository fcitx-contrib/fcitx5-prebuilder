import os
import platform
import subprocess

from common import (
    INSTALL_PREFIX,
    MACOS_ARCH,
    MACOS_VERSION,
    PLATFORM,
    ROOT,
    TARGET,
    MakeBuilder,
    cache,
    ensure,
    get_platform_cflags,
    mkdir,
    rmrf,
)

with open(".icu-version") as f:
    version = f.read().strip()

archive = f"icu4c-{version}-sources.tgz"
cache(
    f"https://github.com/unicode-org/icu/releases/download/release-{version}/{archive}"
)
source_dir = f"{ROOT}/icu/{version}"
if not os.path.isdir(f"{source_dir}/icu/source"):
    mkdir(source_dir)
    ensure("tar", ["xf", f"cache/{archive}", "-C", source_dir])


class ICUBuilder(MakeBuilder):
    def configure(self):
        configure = f"{source_dir}/icu/source/configure"
        options = [
            "--enable-static",
            "--disable-shared",
            "--disable-tests",
            "--disable-samples",
            "--disable-extras",
            "--disable-icuio",
        ]
        prefix_map = f"-ffile-prefix-map={ROOT}=."
        env = {**os.environ, "CC": "clang", "CXX": "clang++"}
        if PLATFORM == "js" or MACOS_ARCH != platform.machine():
            # ICU's data build executes native tools when cross compiling.
            host_dir = f"{ROOT}/icu/{version}/build/host"
            mkdir(host_dir)
            host_flags = f"-O3 {prefix_map}"
            if platform.system() == "Darwin":
                host_flags += f" -mmacosx-version-min={MACOS_VERSION}"
            ensure(
                configure,
                [*options, "--with-data-packaging=static"],
                cwd=host_dir,
                env={
                    **env,
                    "CFLAGS": host_flags,
                    "CXXFLAGS": f"{host_flags} -std=c++17",
                },
            )
            ensure("make", ["-j8"], cwd=host_dir)
            build_triplet = subprocess.check_output(
                ["sh", f"{source_dir}/icu/source/config.guess"], text=True
            ).strip()
            options += [
                f"--build={build_triplet}",
                "--host=wasm32-unknown-emscripten"
                if PLATFORM == "js"
                else f"--host={MACOS_ARCH}-apple-darwin",
                f"--with-cross-build={host_dir}",
            ]
        build_dir = f"{ROOT}/icu/{version}/build/{TARGET}"
        mkdir(build_dir)
        os.chdir(build_dir)
        flags = " ".join([*get_platform_cflags(), prefix_map])
        if PLATFORM == "js":
            options += ["--disable-tools", "--disable-dyload"]
            env.update(
                CC="emcc",
                CXX="em++",
                AR="emar",
                RANLIB="emranlib",
                # ICU has no Emscripten make fragment; its WASI rules use LLVM.
                icu_cv_host_frag="mh-wasi",
            )
        ensure(
            configure,
            [
                *options,
                "--with-data-packaging=archive"
                if PLATFORM == "js"
                else "--with-data-packaging=static",
                f"--prefix={INSTALL_PREFIX}",
            ],
            env={
                **env,
                "CFLAGS": flags,
                "CXXFLAGS": f"{flags} -std=c++17"
                + (" -fwasm-exceptions" if PLATFORM == "js" else ""),
                "LDFLAGS": " ".join(get_platform_cflags()),
            },
        )

    def build(self):
        ensure("make", ["-j8"])

    def pre_package(self):
        # McBopomofo consumes the libraries and headers, not ICU's build tools.
        for directory in ("bin", "sbin", "lib/icu"):
            rmrf(f"{self.dest_dir}{INSTALL_PREFIX}/{directory}")
        data_dir = f"{self.dest_dir}{INSTALL_PREFIX}/share/icu/{version}"
        if PLATFORM == "js":
            # Keep data outside WASM to stay below Chromium's sync compile limit.
            rmrf(f"{data_dir}/config")
            for filename in ("install-sh", "mkinstalldirs"):
                os.remove(f"{data_dir}/{filename}")
        else:
            rmrf(f"{self.dest_dir}{INSTALL_PREFIX}/share/icu")


ICUBuilder("icu").exec()
