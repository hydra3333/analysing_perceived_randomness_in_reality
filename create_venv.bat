@echo off
setlocal DisableDelayedExpansion
rem Create the project-local Python virtual environment; never overwrite one.
rem Place this BAT alongside activate_venv.bat in the repository root.
set "ROOT=%~dp0"
set "VENV=%ROOT%.venv"
set "PY=%VENV%\Scripts\python.exe"
set "ACTIVATE=%VENV%\Scripts\activate.bat"
set "RC=0"

if not "%~1"=="" goto :usage
if exist "%VENV%\" goto :existing
if exist "%VENV%" goto :incomplete
if defined VIRTUAL_ENV goto :active_env

echo [VENV] Creating "%VENV%"

:use_python
where python >nul 2>&1
if errorlevel 1 goto :no_python
python --version
if errorlevel 1 goto :create_failed
python -m venv "%VENV%"
if errorlevel 1 goto :create_failed
goto :verify

:existing
echo [VENV] Existing environment found; leaving it unchanged.
if not exist "%PY%" goto :incomplete
if not exist "%ACTIVATE%" goto :incomplete
goto :finish

:verify
if not exist "%PY%" goto :create_failed
if not exist "%ACTIVATE%" goto :create_failed
"%PY%" -c "import sys,pathlib;sys.exit(0 if pathlib.Path(sys.prefix).resolve()==pathlib.Path(sys.argv[1]).resolve() else 12)" "%VENV%"
if errorlevel 1 goto :verify_failed
"%PY%" --version
if errorlevel 1 goto :verify_failed
"%PY%" -m pip --version
if errorlevel 1 goto :pip_missing

echo [VENV] SUCCESS: "%VENV%"
echo [VENV] To activate in CMD: call "%ROOT%activate_venv.bat"
echo [VENV] To install missing project packages: call "%ROOT%install_upgrade_dependencies_into_venv.bat" INSTALL
echo [VENV] This script did not install or upgrade packages.
goto :finish

:incomplete
echo [VENV] ERROR: "%VENV%" already exists but is not a complete usable venv. >&2
echo [VENV] No files were changed. Inspect it manually; this script never overwrites or deletes it. >&2
set "RC=2"
goto :finish

:active_env
echo [VENV] ERROR: A virtual environment is already active: "%VIRTUAL_ENV%" >&2
echo [VENV] Deactivate it before creating a new project venv. >&2
set "RC=3"
goto :finish

:no_python
echo [VENV] ERROR: Could not find the Windows Python launcher or python executable. >&2
set "RC=4"
goto :finish

:create_failed
echo [VENV] ERROR: Creation failed; a partial .venv may now exist. No automatic deletion. >&2
set "RC=5"
goto :finish

:verify_failed
echo [VENV] ERROR: Environment interpreter verification failed. >&2
set "RC=6"
goto :finish

:pip_missing
echo [VENV] ERROR: pip is unavailable in the project venv. No packages were installed. >&2
set "RC=7"
goto :finish

:usage
echo Usage: %~nx0  ^(no arguments^) >&2
set "RC=8"

:finish
if not "%RC%"=="0" (
    endlocal
    exit /b %RC%
)
endlocal
call "%~dp0activate_venv.bat"
exit /b %ERRORLEVEL%
