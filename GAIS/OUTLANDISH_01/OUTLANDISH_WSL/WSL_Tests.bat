@echo off
setlocal DisableDelayedExpansion
rem OUTLANDISH_WSL: run packed-format tests under existing project Windows venv.
set "ROOT=%~dp0..\..\..\"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [PACKED] ERROR: Existing project Python venv missing: "%PY%" 1>&2
  endlocal & exit /b 2
)
call "%ROOT%activate_venv.bat"
if errorlevel 1 (endlocal & exit /b 3)
"%PY%" -c "import numpy; print('NumPy',numpy.__version__)"
if errorlevel 1 (endlocal & exit /b 4)
"%PY%" -m unittest discover -s "%~dp0." -p "test_wsl_packed.py" -v
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
