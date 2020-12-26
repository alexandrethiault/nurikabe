REM These are unneccesary files automatically included when installing the application (sorry, couldn't find a way to avoid including them) which you can remove safely. Running this script should reduce the size of the application significantly.
REM DON'T RUN THIS IF THE APPLICATION WAS BUILT USING A VERSION OF PYGAME THAT IS NOT AT LEAST 2.0.

@echo off

del python3.dll 2>NUL
del api-ms-win-crt-*.dll 2>NUL

del lib\python3*.dll 2>NUL
del lib\unicodedata.pyd 2>NUL
del lib\vcruntime140.dll 2>NUL
del lib\api-ms-win-crt-*.dll 2>NUL
del lib\pywintypes3*.dll 2>NUL
del lib\_bz2.pyd 2>NUL
del lib\_ctypes_test.pyd 2>NUL
del lib\_hashlib.pyd 2>NUL
del lib\_lzma.pyd 2>NUL
del lib\_queue.pyd 2>NUL
del lib\_socket.pyd 2>NUL
del lib\_testbuffer.pyd 2>NUL
del lib\_testcapi.pyd 2>NUL
del lib\_win32sysloader.pyd 2>NUL
del lib\select.pyd 2>NUL
del lib\win32api.pyd 2>NUL
del lib\win32file.pyd 2>NUL
del lib\win32pipe.pyd 2>NUL

rd /s /q lib\ctypes\test 2>NUL
rd /s /q lib\ctypes\macholib 2>NUL
del lib\ctypes\_aix.pyc 2>NUL
del lib\ctypes\util.pyc 2>NUL
del lib\ctypes\wintypes.pyc 2>NUL

REM Remove every codec or file supplied in lib/encodings except the 5 that are actually used
mkdir lib\tmp 2>NUL
move lib\encodings\__init__.pyc lib\tmp 2>NUL
move lib\encodings\aliases.pyc lib\tmp 2>NUL
move lib\encodings\latin_1.pyc lib\tmp 2>NUL
move lib\encodings\mbcs.pyc lib\tmp 2>NUL
move lib\encodings\utf_8.pyc lib\tmp 2>NUL
rd /s /q lib\encodings 2>NUL
move lib/tmp lib\encodings 2>NUL

del lib\importlib\metadata.pyc 2>NUL
del lib\importlib\_bootstrap.pyc 2>NUL
del lib\importlib\_bootstrap_external.pyc 2>NUL

rd /s /q lib\pygame\__pyinstaller 2>NUL
rd /s /q lib\pygame\_sdl2 2>NUL
rd /s /q lib\pygame\docs 2>NUL
rd /s /q lib\pygame\examples 2>NUL
rd /s /q lib\pygame\tests 2>NUL
rd /s /q lib\pygame\threads 2>NUL
del lib\pygame\python3*.dll 2>NUL
del lib\pygame\api-ms-win-crt-*.dll 2>NUL
del lib\pygame\libwebp-7.dll 2>NUL
del lib\pygame\libFLAC-8.dll 2>NUL
del lib\pygame\libtiff-5.dll 2>NUL
del lib\pygame\libmpg123-0.dll 2>NUL
del lib\pygame\libmodplug-1.dll 2>NUL
del lib\pygame\libvorbis-0.dll 2>NUL
del lib\pygame\libopus-0.dll 2>NUL
del lib\pygame\sdl2_mixer.dll 2>NUL
del lib\pygame\libvorbisfile-3.dll 2>NUL
del lib\pygame\libogg-0.dll 2>NUL
del lib\pygame\libopusfile-0.dll 2>NUL
del lib\pygame\portmidi.dll 2>NUL
del lib\pygame\pygame.ico 2>NUL
del lib\pygame\pygame_icon.icns 2>NUL
del lib\pygame\pygame_icon.svg 2>NUL
del lib\pygame\pygame_icon.bmp 2>NUL
del lib\pygame\pygame_icon.tiff 2>NUL
del lib\pygame\freesansbold.ttf 2>NUL
del lib\pygame\sprite.pyc 2>NUL
del lib\pygame\_camera*.pyc 2>NUL
del lib\pygame\_dummy*.pyc 2>NUL
del lib\pygame\_numpy*.pyc 2>NUL
del lib\pygame\_sprite.*.pyd 2>NUL
del lib\pygame\_freetype.*.pyd 2>NUL
del lib\pygame\*.pyi 2>NUL

del cleanup.sh 2>NUL
del cleanup.bat 2>NUL
