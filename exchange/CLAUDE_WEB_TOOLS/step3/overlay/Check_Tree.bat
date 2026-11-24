@echo off
setlocal DisableDelayedExpansion
rem A read-only look at one tree: DEV, QA or PROD (specification v0.6 section 16; deployment design v0.12 sections 1 and 10).
rem Usage: Check_Tree.bat DEV
rem        Check_Tree.bat QA
rem        Check_Tree.bat PROD
rem It runs deploy\deploy_command.py with DEV's own Python, in isolated mode and writing no cache; what is typed
rem after the command is passed on unchanged. It is run from DEV, and it changes nothing in any tree.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "TOOL=%ROOT%deploy\deploy_command.py"
if not exist "%ROOT%ENVIRONMENT.ini" goto :missing_settings
if not exist "%PY%" goto :missing_venv
if not exist "%TOOL%" goto :missing_tool
"%PY%" -I -B -u "%TOOL%" check-tree %*
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
