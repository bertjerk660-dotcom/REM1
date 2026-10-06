@echo off
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvarsall.bat" x86
if errorlevel 1 exit /b 1
cd /d "C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\third_party\NVSE-6.4.9\fnv_gmod_thug2_input92_candidate"
cl /nologo /EHsc /W4 /WX /std:c++14 test_activation92.cpp /Fo:bin\test_activation92.obj /Fe:bin\test_activation92.exe
if errorlevel 1 exit /b 1
bin\test_activation92.exe
exit /b %ERRORLEVEL%
