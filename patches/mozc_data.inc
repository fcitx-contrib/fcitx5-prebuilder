}}}

#include <fstream>

namespace mozc {
namespace oss {
namespace {

inline const EmbeddedFile& GetOssMozcDataSet() {
  static const EmbeddedFile file = []() -> EmbeddedFile {
    std::ifstream in("/usr/share/mozc/mozc.data", std::ios::binary | std::ios::ate);
    std::streamsize size = in.tellg();
    in.seekg(0, std::ios::beg);
    static std::vector<char> buffer(size);
    in.read(buffer.data(), size);
    return EmbeddedFile{
      reinterpret_cast<const uint64_t*>(buffer.data()),
      static_cast<size_t>(size)
    };
  }();
  return file;
}

const EmbeddedFile& kOssMozcDataSet = GetOssMozcDataSet();
