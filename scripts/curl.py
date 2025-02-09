
from common import CMakeBuilder

project = 'curl'

CMakeBuilder(project, [
    '-DCURL_CA_BUNDLE="/etc/ssl/certs/cacert.pem"',
    '-DCURL_CA_PATH="/etc/ssl/certs/"',
    '-DBUILD_CURL_EXE=OFF',
    '-DBUILD_LIBCURL_DOCS=OFF',
    '-DBUILD_MISC_DOCS=OFF',
    '-DENABLE_CURL_MANUAL=OFF',
    '-DENABLE_THREADED_RESOLVER=OFF',
    '-DUSE_NGHTTP2=OFF',
    '-DCURL_USE_LIBPSL=OFF',
    '-DCURL_USE_LIBSSH2=OFF',
    '-DCURL_DISABLE_NTLM=ON',
    '-DCURL_ZLIB=OFF',
    '-DCURL_ZSTD=OFF',
    '-DHTTP_ONLY=ON',
]).exec()
