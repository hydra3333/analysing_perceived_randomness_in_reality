@echo off
setlocal DisableDelayedExpansion
rem A development batch: back-history for a new method, or a research rerun (MHUP-B; supplement v0.8 section 7.1A).
rem Usage: Run_Development_Batch.bat --game POWERBALL --fill
rem It runs src\Development_Batch_Orchestrator.py (a sequencer: it starts the other launchers one after another, and
rem nothing else) with the project venv's Python; arguments are forwarded with %%*.
rem No byte code is written or read (design v0.1r7 section 4.1).
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%.venv\Scripts\activate.bat"
set "TOOL=%ROOT%src\Development_Batch_Orchestrator.py"
set "RC=0"
if not exist "%PY%" goto :missing_venv
if not exist "%VENV_ACTIVATE%" goto :missing_venv
if "%~1"=="" goto :usage
if not exist "%TOOL%" goto :missing_tool
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
pushd "%ROOT%src"
if errorlevel 1 goto :pushd_failed
rem Interpreter option -u keeps the children's echoed output unbuffered.
"%PY%" -B -u "%TOOL%" %*
set "RC=%ERRORLEVEL%"
popd
goto :finish
:missing_venv
echo [RUN-DEVELOPMENT-BATCH] ERROR: Project .venv missing or invalid. >&2
set "RC=2"
goto :finish
:usage
echo Usage: %~nx0 --game POWERBALL --fill >&2
set "RC=3"
goto :finish
:missing_tool
echo [RUN-DEVELOPMENT-BATCH] ERROR: src\Development_Batch_Orchestrator.py is missing. >&2
set "RC=5"
goto :finish
:wrong_venv
echo [RUN-DEVELOPMENT-BATCH] ERROR: Another virtual environment is active: "%VIRTUAL_ENV%" >&2
set "RC=6"
goto :finish
:activation_failed
echo [RUN-DEVELOPMENT-BATCH] ERROR: Project venv activation failed. >&2
set "RC=7"
goto :finish
:prefix_failed
echo [RUN-DEVELOPMENT-BATCH] ERROR: Project Python does not report the expected sys.prefix. >&2
set "RC=8"
goto :finish
:pycache_present
echo [RUN-DEVELOPMENT-BATCH] ERROR: transitory_data\no_pycache_ever exists; refusing to run. >&2
set "RC=10"
goto :finish
:pushd_failed
echo [RUN-DEVELOPMENT-BATCH] ERROR: Could not enter src. >&2
set "RC=9"
:finish
endlocal & exit /b %RC%
