@echo off
setlocal DisableDelayedExpansion
rem Evaluator launcher (MHUP-A design 6.1): the mirror of Run_Experiment.bat for src\evaluation\.
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
if not exist "%ROOT%src\evaluation\%SCRIPT_NAME%" goto :missing_script
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
set "PYTHONDONTWRITEBYTECODE=1"
"%PY%" -c "import sys,pathlib;sys.exit(0 if pathlib.Path(sys.prefix).resolve()==pathlib.Path(sys.argv[1]).resolve() else 12)" "%EXPECTED_ENV%"
if errorlevel 1 goto :prefix_failed
set "PYTHONPYCACHEPREFIX=%ROOT%transitory_data\no_pycache_ever"
if exist "%PYTHONPYCACHEPREFIX%" goto :pycache_present
rem Pin numerical library threads before the evaluator imports NumPy / SciPy.
set "OMP_NUM_THREADS=1"
set "OPENBLAS_NUM_THREADS=1"
set "MKL_NUM_THREADS=1"
set "NUMEXPR_NUM_THREADS=1"
pushd "%ROOT%src\evaluation"
if errorlevel 1 goto :pushd_failed
rem Interpreter option -u keeps console progress unbuffered when piped.
"%PY%" -B -u %*
set "RC=%ERRORLEVEL%"
popd
goto :finish
:missing_venv
echo [RUN-EVALUATION] ERROR: Project .venv missing or invalid. >&2
set "RC=2"
goto :finish
:usage
echo Usage: %~nx0 Method_Mode_H.py statements [options] >&2
set "RC=3"
goto :finish
:invalid_name
echo [RUN-EVALUATION] ERROR: First argument must be a filename like Method_Mode_H.py (letters/digits/underscore only). >&2
set "RC=4"
goto :finish
:missing_script
echo [RUN-EVALUATION] ERROR: Evaluation Python file does not exist in src\evaluation: "%SCRIPT_NAME%" >&2
set "RC=5"
goto :finish
:wrong_venv
echo [RUN-EVALUATION] ERROR: Another virtual environment is active: "%VIRTUAL_ENV%" >&2
set "RC=6"
goto :finish
:activation_failed
echo [RUN-EVALUATION] ERROR: Project venv activation failed. >&2
set "RC=7"
goto :finish
:prefix_failed
echo [RUN-EVALUATION] ERROR: Project Python does not report the expected sys.prefix. >&2
set "RC=8"
goto :finish
:pycache_present
echo [RUN-EVALUATION] ERROR: transitory_data\no_pycache_ever exists; refusing to run. >&2
set "RC=10"
goto :finish
:pushd_failed
echo [RUN-EVALUATION] ERROR: Could not enter src\evaluation. >&2
set "RC=9"
:finish
endlocal & exit /b %RC%
