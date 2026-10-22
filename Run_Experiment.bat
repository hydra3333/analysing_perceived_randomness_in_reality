@echo off
setlocal DisableDelayedExpansion
rem Human-facing AND provisional coordinator-facing experiment runner (Option F).
rem The first argument must be an ASCII alphanumeric/underscore Python basename.
rem Other arguments are forwarded with %%*; see P0 handback for supported quoting.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%.venv\Scripts\activate.bat"
set "RC=0"
if not exist "%PY%" goto :missing_venv
if not exist "%VENV_ACTIVATE%" goto :missing_venv
if "%~1"=="" goto :usage
set "SCRIPT_NAME=%~1"
rem Avoid using SHIFT or rebuilding arguments from %%1...%%9.
rem Validate the filename BEFORE it enters a filesystem path or command.
set SCRIPT_NAME | "%SystemRoot%\System32\findstr.exe" /R /C:"^SCRIPT_NAME=[A-Za-z0-9_][A-Za-z0-9_]*\.py$" >nul
if errorlevel 1 goto :invalid_name
if not "%SCRIPT_NAME%"=="%~nx1" goto :invalid_name
if /I not "%~x1"==".py" goto :invalid_name
if not exist "%ROOT%src\methods\%SCRIPT_NAME%" goto :missing_script
for %%I in ("%ROOT%.venv\.") do set "EXPECTED_ENV=%%~fI"
if defined VIRTUAL_ENV goto :check_active
call "%VENV_ACTIVATE%"
if errorlevel 1 goto :activation_failed
if not defined VIRTUAL_ENV goto :activation_failed
goto :verify_python
:check_active
for %%I in ("%VIRTUAL_ENV%\.") do set "ACTIVE_ENV=%%~fI"
if /I not "%ACTIVE_ENV%"=="%EXPECTED_ENV%" goto :wrong_venv
:verify_python
"%PY%" -c "import sys,pathlib;sys.exit(0 if pathlib.Path(sys.prefix).resolve()==pathlib.Path(sys.argv[1]).resolve() else 12)" "%EXPECTED_ENV%"
if errorlevel 1 goto :prefix_failed
rem Pin numerical library threads before the experiment imports NumPy / SciPy.
set "OMP_NUM_THREADS=1"
set "OPENBLAS_NUM_THREADS=1"
set "MKL_NUM_THREADS=1"
set "NUMEXPR_NUM_THREADS=1"
pushd "%ROOT%src\methods"
if errorlevel 1 goto :pushd_failed
rem Interpreter option -u keeps console progress unbuffered when piped.
"%PY%" -u %*
set "RC=%ERRORLEVEL%"
popd
goto :finish
:missing_venv
echo [RUN-EXPERIMENT] ERROR: Project .venv missing or invalid. >&2
set "RC=2"
goto :finish
:usage
echo Usage: %~nx0 POC_Architecture_Probe.py --poc --case=echo-argv [options] >&2
set "RC=3"
goto :finish
:invalid_name
echo [RUN-EXPERIMENT] ERROR: First argument must be a filename like POC_Architecture_Probe.py (letters/digits/underscore only). >&2
set "RC=4"
goto :finish
:missing_script
echo [RUN-EXPERIMENT] ERROR: Experiment Python file does not exist in src\methods: "%SCRIPT_NAME%" >&2
set "RC=5"
goto :finish
:wrong_venv
echo [RUN-EXPERIMENT] ERROR: Another virtual environment is active: "%VIRTUAL_ENV%" >&2
set "RC=6"
goto :finish
:activation_failed
echo [RUN-EXPERIMENT] ERROR: Project venv activation failed. >&2
set "RC=7"
goto :finish
:prefix_failed
echo [RUN-EXPERIMENT] ERROR: Project Python does not report the expected sys.prefix. >&2
set "RC=8"
goto :finish
:pushd_failed
echo [RUN-EXPERIMENT] ERROR: Could not enter src\methods. >&2
set "RC=9"
:finish
endlocal & exit /b %RC%
