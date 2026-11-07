@echo off
REM Explicit helper (NOT part of automatic setup). CALL to set PATH for this CMD.
call "C:\HOST_OUTLANDISH_SOURCE\SANDBOX\OUTLANDISH_01_Python_Env.bat"
if errorlevel 1 exit /b 1
cd /d C:\OUTLANDISH_WORK
if errorlevel 1 exit /b 1
echo Persistent Python: %OUTLANDISH_PYHOME%
if not exist "%OUTLANDISH_PYHOME%\python.exe" (
  echo Python not yet installed. Run manual INSTALL phase separately.
  exit /b 0
)
"%OUTLANDISH_PYHOME%\python.exe" --version
if errorlevel 1 exit /b 1
"%OUTLANDISH_PYHOME%\python.exe" -m pip --version
if errorlevel 1 exit /b 1
echo Preview only, no computation started:
echo   python outlandish_artifacts.py audit
echo   python outlandish_artifacts.py status
echo   python outlandish_big_constants.py pipeline --constant phi --digits 100000
