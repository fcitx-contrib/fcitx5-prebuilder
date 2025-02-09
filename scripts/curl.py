
from common import CMakeBuilder

project = 'curl'

CMakeBuilder(project, [
    '-DBUILD_CURL_EXE=OFF',
    '-DBUILD_EXAMPLES=OFF',
    '-DBUILD_LIBCURL_DOCS=OFF',
    '-DBUILD_MISC_DOCS=OFF',
    '-DBUILD_TESTING=OFF',
    '-DCURL_CA_BUNDLE="/etc/ssl/certs/cacert.pem"',
    '-DCURL_CA_PATH="/etc/ssl/certs/"',
    '-DCURL_DISABLE_ALTSVC=ON',
    '-DCURL_DISABLE_AWS=ON',
    '-DCURL_DISABLE_BASIC_AUTH=ON',
    '-DCURL_DISABLE_BEARER_AUTH=ON',
    '-DCURL_DISABLE_BINDLOCAL=ON',
    '-DCURL_DISABLE_COOKIES=ON',
    '-DCURL_DISABLE_DIGEST_AUTH=ON',
    '-DCURL_DISABLE_GETOPTIONS=ON',
    '-DCURL_DISABLE_HEADERS_API=ON',
    '-DCURL_DISABLE_HSTS=ON', # cloudpinyin accesses https only.
    '-DCURL_DISABLE_HTTP_AUTH=ON',
    '-DCURL_DISABLE_KERBEROS_AUTH=ON',
    '-DCURL_DISABLE_LIBCURL_OPTION=ON',
    '-DCURL_DISABLE_MIME=ON',
    '-DCURL_DISABLE_NEGOTIATE_AUTH=ON',
    '-DCURL_DISABLE_NETRC=ON',
    '-DCURL_DISABLE_NTLM=ON',
    '-DCURL_DISABLE_OPENSSL_AUTO_LOAD_CONFIG=ON',
    '-DCURL_DISABLE_PARSEDATE=ON',
    '-DCURL_DISABLE_PROGRESS_METER=ON',
    '-DCURL_DISABLE_SOCKETPAIR=ON',
    '-DCURL_DISABLE_SRP=ON',
    '-DCURL_DISABLE_VERBOSE_STRINGS=ON',
    '-DCURL_DISABLE_WEBSOCKETS=ON',
    '-DCURL_USE_LIBPSL=OFF',
    '-DCURL_USE_LIBSSH2=OFF',
    '-DCURL_ZLIB=OFF',
    '-DCURL_ZSTD=OFF',
    '-DENABLE_CURL_MANUAL=OFF',
    '-DENABLE_THREADED_RESOLVER=OFF',
    '-DENABLE_UNIX_SOCKETS=OFF',
    '-DHTTP_ONLY=ON',
    '-DUSE_LIBIDN2=OFF',
    '-DUSE_NGHTTP2=OFF',
]).exec()
