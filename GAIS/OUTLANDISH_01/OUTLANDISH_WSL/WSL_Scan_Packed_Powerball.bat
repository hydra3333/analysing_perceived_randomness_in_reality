@echo off
setlocal DisableDelayedExpansion
rem Explicit input/draws/results required. Preview-only unless --run supplied.
set "ROOT=%~dp0..\..\..\"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [PACKED] ERROR: project venv not found: "%PY%" 1>&2
  endlocal & exit /b 2
)
if "%~1"=="" (
  echo Usage: %~nx0 --input FILE --draws PREHOLDOUT_CSV --output-root RESULTS_DIR [--run]
  endlocal & exit /b 2
)
call "%ROOT%activate_venv.bat"
if errorlevel 1 (endlocal & exit /b 3)
"%PY%" "%~dp0wsl_scan_packed_powerball.py" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
