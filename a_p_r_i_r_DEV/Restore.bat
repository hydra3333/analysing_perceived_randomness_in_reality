@echo off
setlocal DisableDelayedExpansion
rem DEV only (the simple scheme v0.2, section 7): puts the QA or the PROD tree back from one of its backups.
rem The tree as it was is renamed aside, never deleted. The tree's .venv is then built again by hand.
rem Usage: Restore.bat QA^|PROD backup_file.zip      for example: Restore.bat QA QA_20261201_201012_after_job.zip
rem It runs deploy\dev_command.py with this tree's own Python, in isolated mode and writing no cache;
rem what is typed after the command is passed on unchanged. The tree it works in is the folder this file is in.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "TOOL=%ROOT%deploy\dev_command.py"
if not exist "%ROOT%ENVIRONMENT.ini" goto :missing_settings
if not exist "%PY%" goto :missing_venv
if not exist "%TOOL%" goto :missing_tool
"%PY%" -I -B -u "%TOOL%" restore %*
exit /b %ERRORLEVEL%
:missing_settings
echo REFUSED: %ROOT%ENVIRONMENT.ini is missing, so this folder is not a tree. In DEV, copy ENVIRONMENT.example.ini to ENVIRONMENT.ini and check its paths. 1>&2
exit /b 2
:missing_venv
echo REFUSED: this tree's Python was not found at %PY%. Build the tree's .venv first. 1>&2
exit /b 2
:missing_tool
echo REFUSED: %TOOL% is missing. The research system is not installed in this tree. 1>&2
exit /b 2
