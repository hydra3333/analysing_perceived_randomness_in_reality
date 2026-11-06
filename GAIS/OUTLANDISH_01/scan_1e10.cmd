@echo off
rem OUTLANDISH_01 v0.2: first 10,000,000,000 digits of each verified active pi/phi.
setlocal
pushd "%~dp0" || exit /b 1
python outlandish_artifacts.py audit
if errorlevel 1 (popd & exit /b 2)
python outlandish_powerball_stage_a.py scan --constants pi phi --prefix-digits 10000000000
set "SCAN_RC=%ERRORLEVEL%"
python outlandish_artifacts.py audit
if errorlevel 1 if "%SCAN_RC%"=="0" set "SCAN_RC=2"
popd
exit /b %SCAN_RC%
