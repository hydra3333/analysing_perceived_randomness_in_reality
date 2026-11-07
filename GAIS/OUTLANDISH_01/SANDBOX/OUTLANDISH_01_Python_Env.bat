@echo off
REM CALL this from any Sandbox CMD. No Python execution / installation here.
if /I not "%USERNAME%"=="WDAGUtilityAccount" (
  echo SAFETY STOP: only inside Windows Sandbox.
  exit /b 1
)
if /I "%COMPUTERNAME%"=="3900X" (
  echo SAFETY STOP: refuses host computer.
  exit /b 1
)
if not exist "C:\HOST_OUTLANDISH_DATA\" (
  echo ERROR: writable host DATA mapping is absent.
  exit /b 1
)
set "OUTLANDISH_PYROOT=C:\HOST_OUTLANDISH_DATA\python_candidate"
set "OUTLANDISH_PYHOME=%OUTLANDISH_PYROOT%\Python315"
set "PATH=%OUTLANDISH_PYHOME%;%OUTLANDISH_PYHOME%\Scripts;%PATH%"
set "PYTHONNOUSERSITE=1"
set "PIP_USER=false"
set "PIP_TARGET="
set "PIP_PREFIX="
set "PIP_ROOT="
set "PIP_CONFIG_FILE=NUL"
REM Keep pip's destination in the interpreter's own Lib\site-packages.
REM Do not set PIP_TARGET, PIP_PREFIX, PIP_ROOT or PYTHONPATH.
exit /b 0
