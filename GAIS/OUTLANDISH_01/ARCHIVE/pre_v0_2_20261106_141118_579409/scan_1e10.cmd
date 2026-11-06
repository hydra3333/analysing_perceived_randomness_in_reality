@echo off
setlocal
pushd "%~dp0" || exit /b 1
python outlandish_artifacts.py audit
if errorlevel 1 (
 echo STOP: workspace contains misplaced large/generated artifacts.
 popd
 exit /b 2
)
python outlandish_powerball_stage_a.py scan --draws POWERBALL_preholdout_only.csv --digits digits_pi_10_to_10.bin digits_golden_ratio_10_to_10.bin --chunk-bytes 4000000 --progress-seconds 5
set "SCAN_RC=%ERRORLEVEL%"
python outlandish_artifacts.py audit
if errorlevel 1 if "%SCAN_RC%"=="0" set "SCAN_RC=2"
popd
exit /b %SCAN_RC%
