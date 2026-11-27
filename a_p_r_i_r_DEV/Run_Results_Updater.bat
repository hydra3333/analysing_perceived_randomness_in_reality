@echo off
setlocal DisableDelayedExpansion
rem The results updater by itself (the simple scheme v0.2, sections 6 and 8): fetches new official results
rem into THIS tree only. The research job runs it at its start anyway, unless --no-update.
rem Usage: Run_Results_Updater.bat [--games POWERBALL,OZLOTTO] [--months-back 5] [--browser chrome^|firefox] [--pause 2]
rem It runs src\research_command.py with this tree's own Python, in isolated mode and writing no cache;
rem what is typed after the command is passed on unchanged. The tree it works in is the folder this file is in.
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "TOOL=%ROOT%src\research_command.py"
if not exist "%ROOT%ENVIRONMENT.ini" goto :missing_settings
if not exist "%PY%" goto :missing_venv
if not exist "%TOOL%" goto :missing_tool
"%PY%" -I -B -u "%TOOL%" update %*
exit /b %ERRORLEVEL%
:missing_settings
echo REFUSED: %ROOT%ENVIRONMENT.ini is missing. In DEV, copy ENVIRONMENT.example.ini to ENVIRONMENT.ini and put this PC's paths in it. 1>&2
exit /b 2
:missing_venv
echo REFUSED: this tree's Python was not found at %PY%. Build the tree's .venv first. 1>&2
exit /b 2
:missing_tool
echo REFUSED: %TOOL% is missing. The research system is not installed in this tree. 1>&2
exit /b 2
