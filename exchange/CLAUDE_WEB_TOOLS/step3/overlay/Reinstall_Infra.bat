@echo off
setlocal DisableDelayedExpansion
rem Bring the infrastructure of the QA or PROD tree to DEV's (specification v0.6 section 12.4; deployment design v0.12 section 6).
rem Usage: Reinstall_Infra.bat QA
rem        Reinstall_Infra.bat PROD
rem        Reinstall_Infra.bat PROD --replace-unfinished
rem It runs deploy\deploy_command.py with DEV's own Python, in isolated mode and writing no cache; what is typed
rem after the command is passed on unchanged. It is run from DEV. It overwrites installed files: it says what it would change and asks before it does.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "TOOL=%ROOT%deploy\deploy_command.py"
if not exist "%ROOT%ENVIRONMENT.ini" goto :missing_settings
if not exist "%PY%" goto :missing_venv
if not exist "%TOOL%" goto :missing_tool
"%PY%" -I -B -u "%TOOL%" reinstall-infra %*
exit /b %ERRORLEVEL%
:missing_settings
echo REFUSED: %ROOT%ENVIRONMENT.ini is missing. In DEV, copy ENVIRONMENT.example.ini to ENVIRONMENT.ini and put this PC's paths in it. 1>&2
exit /b 2
:missing_venv
echo REFUSED: this tree's Python was not found at %PY%. Build the tree's .venv first. 1>&2
exit /b 2
:missing_tool
echo REFUSED: %TOOL% is missing. The install tools are in DEV only; this command is run from the DEV tree. 1>&2
exit /b 2
