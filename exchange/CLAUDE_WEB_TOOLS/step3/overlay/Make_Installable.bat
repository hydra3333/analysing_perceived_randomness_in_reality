@echo off
setlocal DisableDelayedExpansion
rem Marking finished variants, or the infrastructure, ready to be installed (specification v0.6 sections 4 and 12.2).
rem Usage: Make_Installable.bat INFRA
rem        Make_Installable.bat family variant
rem        Make_Installable.bat family/variant [family/variant ...]        add --unmark to remove markers
rem It runs deploy\deploy_command.py with DEV's own Python, in isolated mode and writing no cache; what is typed
rem after the command is passed on unchanged. It works in DEV only: the tree it works in is the folder this file is in.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "TOOL=%ROOT%deploy\deploy_command.py"
if not exist "%ROOT%ENVIRONMENT.ini" goto :missing_settings
if not exist "%PY%" goto :missing_venv
if not exist "%TOOL%" goto :missing_tool
"%PY%" -I -B -u "%TOOL%" make-installable %*
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
