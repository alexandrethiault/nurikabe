# These are unneccesary files automatically included when installing the application (sorry, couldn't find a way to avoid including them) which you can remove safely. Running this script should reduce the size of the application significantly.
# DON'T RUN THIS IF THE APPLICATION WAS BUILT USING A VERSION OF PYGAME THAT IS NOT AT LEAST 2.0.

rm python3.dll
rm api-ms-win-crt-*.dll

rm lib/python3*.dll
rm lib/libcrypto-1_1-x64.dll
rm lib/unicodedata.pyd
rm lib/vcruntime140.dll
rm lib/api-ms-win-crt-*.dll
rm lib/pywintypes3*.dll
rm lib/_bz2.pyd
rm lib/_ctypes_test.pyd
rm lib/_hashlib.pyd
rm lib/_lzma.pyd
rm lib/_queue.pyd
rm lib/_socket.pyd
rm lib/_testbuffer.pyd
rm lib/_testcapi.pyd
rm lib/_win32sysloader.pyd
rm lib/select.pyd
rm lib/win32api.pyd
rm lib/win32file.pyd
rm lib/win32pipe.pyd

rm -r lib/ctypes/test
rm -r lib/ctypes/macholib
rm lib/ctypes/_aix.pyc
rm lib/ctypes/util.pyc
rm lib/ctypes/wintypes.pyc

# Remove every codec or file supplied in lib/encodings except the 5 that are actually used
mkdir lib/tmp
mv lib/encodings/__init__.pyc lib/tmp
mv lib/encodings/aliases.pyc lib/tmp
mv lib/encodings/latin_1.pyc lib/tmp
mv lib/encodings/mbcs.pyc lib/tmp
mv lib/encodings/utf_8.pyc lib/tmp
rm -r lib/encodings
mv lib/tmp lib/encodings

rm lib/importlib/metadata.pyc
rm lib/importlib/_bootstrap.pyc
rm lib/importlib/_bootstrap_external.pyc

rm -r lib/pygame/__pyinstaller
rm -r lib/pygame/_sdl2
rm -r lib/pygame/docs
rm -r lib/pygame/examples
rm -r lib/pygame/tests
rm -r lib/pygame/threads
rm lib/pygame/python3*.dll
rm lib/pygame/api-ms-win-crt-*.dll
rm lib/pygame/libwebp-7.dll
rm lib/pygame/libFLAC-8.dll
rm lib/pygame/libtiff-5.dll
rm lib/pygame/libmpg123-0.dll
rm lib/pygame/libmodplug-1.dll
rm lib/pygame/libvorbis-0.dll
rm lib/pygame/libopus-0.dll
rm lib/pygame/sdl2_mixer.dll
rm lib/pygame/libvorbisfile-3.dll
rm lib/pygame/libogg-0.dll
rm lib/pygame/libopusfile-0.dll
rm lib/pygame/portmidi.dll
rm lib/pygame/pygame.ico
rm lib/pygame/pygame_icon.icns
rm lib/pygame/pygame_icon.svg
rm lib/pygame/pygame_icon.bmp
rm lib/pygame/pygame_icon.tiff
rm lib/pygame/freesansbold.ttf
rm lib/pygame/sprite.pyc
rm lib/pygame/_camera*.pyc
rm lib/pygame/_dummy*.pyc
rm lib/pygame/_numpy*.pyc
rm lib/pygame/_sprite.*.pyd
rm lib/pygame/_freetype.*.pyd
rm lib/pygame/*.pyi

rm cleanup.bat
rm cleanup.sh
