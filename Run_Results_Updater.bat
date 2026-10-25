@echo off
setlocal DisableDelayedExpansion
rem Results master updater launcher; project venv only; no auto upgrades.
rem No arguments = "update" with defaults (current month plus the previous 5).
rem Until source_data\HOLDOUT_OPENED_<GAME>.json exists the updater refuses any
rem window reaching the quarantine (on or after 2026-08-01) before any request.
rem Other uses:  Run_Results_Updater.bat --self-test
rem              Run_Results_Updater.bat update --months-back 11
rem              Run_Results_Updater.bat init --build-run <dir> --lott-check-run <dir>
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%.venv\Scripts\activate.bat"
set "TOOL=%ROOT%src\results_master_v0_1.py"
set "RC=0"
if not exist "%PY%" goto :missing_venv
if not exist "%VENV_ACTIVATE%" goto :missing_venv
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
"%PY%" -c "import sys,pathlib;sys.exit(0 if pathlib.Path(sys.prefix).resolve()==pathlib.Path(sys.argv[1]).resolve() else 12)" "%EXPECTED_ENV%"
if errorlevel 1 goto :prefix_failed
pushd "%ROOT%"
if errorlevel 1 goto :pushd_failed
if not "%~1"=="" goto :with_args
"%PY%" -u "%TOOL%" update
set "RC=%ERRORLEVEL%"
goto :done_run
:with_args
"%PY%" -u "%TOOL%" %*
set "RC=%ERRORLEVEL%"
:done_run
popd
goto :finish
:missing_venv
echo [RUN-RESULTS-UPDATER] ERROR: Project .venv missing or invalid. >&2
set "RC=2"
goto :finish
:missing_tool
echo [RUN-RESULTS-UPDATER] ERROR: src\results_master_v0_1.py not found. >&2
set "RC=2"
goto :finish
:wrong_venv
echo [RUN-RESULTS-UPDATER] ERROR: Another virtual environment is active: "%VIRTUAL_ENV%" >&2
set "RC=6"
goto :finish
:activation_failed
echo [RUN-RESULTS-UPDATER] ERROR: Project venv activation failed. >&2
set "RC=7"
goto :finish
:prefix_failed
echo [RUN-RESULTS-UPDATER] ERROR: Python reports an unexpected sys.prefix. >&2
set "RC=8"
goto :finish
:pushd_failed
echo [RUN-RESULTS-UPDATER] ERROR: Could not enter project root. >&2
set "RC=9"
:finish
endlocal & exit /b %RC%
