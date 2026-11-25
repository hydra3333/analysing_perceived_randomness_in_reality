@echo off
setlocal DisableDelayedExpansion
rem Verify this tree's Python environment after it was built or rebuilt (specification v0.6 section 13).
rem Usage: Verify_Tree.bat
rem It runs src\tree_checks_command.py with this tree's own Python, in isolated mode and writing no cache;
rem what is typed after the command is passed on unchanged. The tree it works in is the folder this file is in.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "TOOL=%ROOT%src\tree_checks_command.py"
if not exist "%ROOT%ENVIRONMENT.ini" goto :missing_settings
if not exist "%PY%" goto :missing_venv
if not exist "%TOOL%" goto :missing_tool
"%PY%" -I -B -u "%TOOL%" verify %*
exit /b %ERRORLEVEL%
:missing_settings
echo REFUSED: %ROOT%ENVIRONMENT.ini is missing. This folder is not a tree that Init_Tree.bat made. 1>&2
exit /b 2
:missing_venv
echo REFUSED: this tree's Python was not found at %PY%. Build the tree's .venv first. 1>&2
exit /b 2
:missing_tool
echo REFUSED: %TOOL% is missing. The research system is not installed in this tree. 1>&2
exit /b 2
