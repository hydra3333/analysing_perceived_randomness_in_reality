@echo off
setlocal DisableDelayedExpansion
rem Human-facing coordinator launcher; project venv only; no auto upgrades.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%.venv\Scripts\activate.bat"
set "RC=0"
if not exist "%PY%" goto :missing_venv
if not exist "%VENV_ACTIVATE%" goto :missing_venv
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
rem The experiment wrapper reasserts these for each child.
set "OMP_NUM_THREADS=1"
set "OPENBLAS_NUM_THREADS=1"
set "MKL_NUM_THREADS=1"
set "NUMEXPR_NUM_THREADS=1"
pushd "%ROOT%"
if errorlevel 1 goto :pushd_failed
"%PY%" -u "%ROOT%src\Powerball_Experiment_Coordinator.py" %*
set "RC=%ERRORLEVEL%"
popd
goto :finish
:missing_venv
echo [RUN-COORDINATOR] ERROR: Project .venv missing or invalid. >&2
set "RC=2"
goto :finish
:wrong_venv
echo [RUN-COORDINATOR] ERROR: Another virtual environment is active: "%VIRTUAL_ENV%" >&2
set "RC=6"
goto :finish
:activation_failed
echo [RUN-COORDINATOR] ERROR: Project venv activation failed. >&2
set "RC=7"
goto :finish
:prefix_failed
echo [RUN-COORDINATOR] ERROR: Python reports an unexpected sys.prefix. >&2
set "RC=8"
goto :finish
:pushd_failed
echo [RUN-COORDINATOR] ERROR: Could not enter project root. >&2
set "RC=9"
:finish
endlocal & exit /b %RC%
