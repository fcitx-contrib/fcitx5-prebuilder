if [[ $(uname) == MINGW64* ]]; then
  ext=lib
else
  ext=a
fi

if grep fcitx5-prebuilder $(find build -name "*.${ext}"); then
  exit 1
fi
