@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%USERNAME%"=="WDAGUtilityAccount" exit /b 1
call "C:\HOST_OUTLANDISH_SOURCE\SANDBOX\OUTLANDISH_01_Python_Env.bat"
if errorlevel 1 exit /b 1
if not exist "%OUTLANDISH_PYHOME%\python.exe" (
  echo ERROR: No persistent Python installed.
  exit /b 1
)
cd /d C:\OUTLANDISH_WORK
if errorlevel 1 exit /b 1
"%OUTLANDISH_PYHOME%\python.exe" --version
if errorlevel 1 exit /b 1
"%OUTLANDISH_PYHOME%\python.exe" outlandish_big_constants.py pipeline --constant phi --digits 100000 --run
if errorlevel 1 (
  echo Pipeline FAILED. Inspect state/results. No registry copy performed.
  pause
  exit /b 1
)
copy /Y "C:\OUTLANDISH_WORK\outlandish.local.toml" "C:\HOST_OUTLANDISH_DATA\outlandish.local.toml" >nul
if errorlevel 1 (
  echo Pipeline ran, but SAVING sandbox TOML failed. Save manually before closing.
  pause
  exit /b 1
)
echo SUCCESS: sandbox-only registry saved in mapped DATA.
pause
exit /b 0
