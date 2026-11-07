@echo off
setlocal DisableDelayedExpansion
rem Explicit arguments required; read-only samples only, NO legacy registry.
set "ROOT=%~dp0..\..\..\"
set "PY=%ROOT%.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [PACKED] ERROR: project venv not found: "%PY%" 1>&2
  endlocal & exit /b 2
)
if "%~1"=="" (
  echo Usage: %~nx0 --input FILE --constant phi --digits COUNT [--reference EXISTING_NUMERIC_BIN]
  endlocal & exit /b 2
)
call "%ROOT%activate_venv.bat"
if errorlevel 1 (endlocal & exit /b 3)
"%PY%" "%~dp0wsl_verify_windows.py" %*
set "RC=%ERRORLEVEL%"
endlocal & exit /b %RC%
