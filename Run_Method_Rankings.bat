@echo off
setlocal DisableDelayedExpansion
rem Method-ranking report tool launcher (Architecture v0.8 section 5A.4; WF-1B).
rem Usage: Run_Method_Rankings.bat --game POWERBALL --batch wf-... --first 1286 --last 1576
rem It runs src\evaluation\Method_Rankings_Report.py with the project venv's Python; arguments are forwarded with %%*.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%.venv\Scripts\activate.bat"
set "TOOL=%ROOT%src\evaluation\Method_Rankings_Report.py"
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
"%PY%" -c "import sys,pathlib;sys.exit(0 if pathlib.Path(sys.prefix).resolve()==pathlib.Path(sys.argv[1]).resolve() else 12)" "%EXPECTED_ENV%"
if errorlevel 1 goto :prefix_failed
rem Pin numerical library threads before the tool imports NumPy.
set "OMP_NUM_THREADS=1"
set "OPENBLAS_NUM_THREADS=1"
set "MKL_NUM_THREADS=1"
set "NUMEXPR_NUM_THREADS=1"
pushd "%ROOT%src\evaluation"
if errorlevel 1 goto :pushd_failed
"%PY%" -u "%TOOL%" %*
set "RC=%ERRORLEVEL%"
popd
goto :finish
:missing_venv
echo [RUN-RANKINGS] ERROR: Project .venv missing or invalid. >&2
set "RC=2"
goto :finish
:usage
echo Usage: %~nx0 --game POWERBALL --batch wf-... --first 1286 --last 1576 >&2
set "RC=3"
goto :finish
:missing_tool
echo [RUN-RANKINGS] ERROR: src\evaluation\Method_Rankings_Report.py is missing. >&2
set "RC=5"
goto :finish
:wrong_venv
echo [RUN-RANKINGS] ERROR: Another virtual environment is active: "%VIRTUAL_ENV%" >&2
set "RC=6"
goto :finish
:activation_failed
echo [RUN-RANKINGS] ERROR: Project venv activation failed. >&2
set "RC=7"
goto :finish
:prefix_failed
echo [RUN-RANKINGS] ERROR: Project Python does not report the expected sys.prefix. >&2
set "RC=8"
goto :finish
:pushd_failed
echo [RUN-RANKINGS] ERROR: Could not enter src\evaluation. >&2
set "RC=9"
:finish
endlocal & exit /b %RC%
