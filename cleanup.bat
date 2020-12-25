REM These are unneccesary files automatically included when installing the application (sorry, couldn't find a way to avoid including them) which you can remove safely. Running this script should reduce the size of the application significantly.

@echo off

del python3.dll 2>NUL
del api-ms-win-crt-conio-l1-1-0.dll 2>NUL
del api-ms-win-crt-convert-l1-1-0.dll 2>NUL
del api-ms-win-crt-environment-l1-1-0.dll 2>NUL
del api-ms-win-crt-filesystem-l1-1-0.dll 2>NUL
del api-ms-win-crt-heap-l1-1-0.dll 2>NUL
del api-ms-win-crt-locale-l1-1-0.dll 2>NUL
del api-ms-win-crt-math-l1-1-0.dll 2>NUL
del api-ms-win-crt-process-l1-1-0.dll 2>NUL
del api-ms-win-crt-runtime-l1-1-0.dll 2>NUL
del api-ms-win-crt-stdio-l1-1-0.dll 2>NUL
del api-ms-win-crt-string-l1-1-0.dll 2>NUL
del api-ms-win-crt-time-l1-1-0.dll 2>NUL

del lib\python37.dll 2>NUL
del lib\python38.dll 2>NUL
del lib\unicodedata.pyd 2>NUL
del lib\vcruntime140.dll 2>NUL
del lib\api-ms-win-crt-conio-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-convert-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-environment-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-filesystem-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-heap-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-locale-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-math-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-process-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-runtime-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-stdio-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-string-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-time-l1-1-0.dll 2>NUL
del lib\api-ms-win-crt-utility-l1-1-0.dll 2>NUL
del lib\pywintypes37.dll 2>NUL
del lib\pywintypes38.dll 2>NUL

rd /s /q lib\xml 2>NUL

rd /s /q lib\ctypes\test 2>NUL
rd /s /q lib\ctypes\macholib 2>NUL

rd /s /q lib\pygame\__pyinstaller 2>NUL
rd /s /q lib\pygame\_sdl2 2>NUL
rd /s /q lib\pygame\docs 2>NUL
rd /s /q lib\pygame\examples 2>NUL
rd /s /q lib\pygame\tests 2>NUL
rd /s /q lib\pygame\threads 2>NUL
del lib\pygame\python37.dll 2>NUL
del lib\pygame\python38.dll 2>NUL
del lib\pygame\_sprite.cp37-win_amd64.pyd 2>NUL
del lib\pygame\_sprite.cp38-win_amd64.pyd 2>NUL
del lib\pygame\api-ms-win-crt-conio-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-convert-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-environment-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-filesystem-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-heap-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-locale-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-math-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-process-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-runtime-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-stdio-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-string-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-time-l1-1-0.dll 2>NUL
del lib\pygame\api-ms-win-crt-utility-l1-1-0.dll 2>NUL
del lib\pygame\libwebp-7.dll 2>NUL
del lib\pygame\libFLAC-8.dll 2>NUL
del lib\pygame\libtiff-5.dll 2>NUL
del lib\pygame\libmpg123-0.dll 2>NUL
del lib\pygame\libmodplug-1.dll 2>NUL
del lib\pygame\libvorbis-0.dll 2>NUL
del lib\pygame\pygame.ico 2>NUL
del lib\pygame\libopus-0.dll 2>NUL
del lib\pygame\sdl2_mixer.dll 2>NUL
del lib\pygame\freesansbold.ttf 2>NUL
del lib\pygame\libvorbisfile-3.dll 2>NUL
del lib\pygame\libogg-0.dll 2>NUL
del lib\pygame\libopusfile-0.dll 2>NUL
del lib\pygame\portmidi.dll 2>NUL
del lib\pygame\pygame_icon.icns 2>NUL
del lib\pygame\pygame_icon.tiff 2>NUL

del cleanup.sh 2>NUL
del cleanup.bat 2>NUL