@echo off
setlocal DisableDelayedExpansion
rem Put back exactly one backup of a tree, at the path it came from (specification v0.6 section 14.1).
rem Usage: Restore.bat --snapshot "<full path of the backup ZIP>" [--after-hand-unzip]
rem Run it from the folder this recovery kit was unpacked into. It needs only an installed Python: no tree of the
rem project, not DEV, not QA. Read HOW_TO_RESTORE.txt beside this file first. Close every other Python program.
set "KIT=%~dp0"
if not exist "%KIT%restore_tool.py" goto :missing_tool
where python >nul 2>nul
if errorlevel 1 goto :no_python
python -I -B -u "%KIT%restore_tool.py" %*
exit /b %ERRORLEVEL%
:missing_tool
echo REFUSED: %KIT%restore_tool.py is missing. Unpack the whole recovery kit into an empty folder. 1>&2
exit /b 2
:no_python
echo REFUSED: no Python was found on this PC's PATH. Install Python, or start the tool with the full path of any python.exe:  "C:\path\to\python.exe" -I -B "%KIT%restore_tool.py" --snapshot "..." 1>&2
exit /b 2
