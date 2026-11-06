@echo off
setlocal
set "THREADS=4"
pushd "%~dp0" || exit /b 1
python outlandish_artifacts.py audit
if errorlevel 1 (
 echo STOP: workspace contains misplaced large/generated artifacts.
 popd
 exit /b 2
)
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000 --threads %THREADS% --run
if errorlevel 1 (
 echo STOP: Pi pipeline failed. Inspect its output; no Phi generation attempted.
 popd
 exit /b 1
)
python outlandish_big_constants.py pipeline --constant phi --digits 10000000000 --threads %THREADS% --run
if errorlevel 1 (
 echo STOP: Golden-ratio pipeline failed. Inspect output before retrying.
 popd
 exit /b 1
)
python outlandish_artifacts.py audit
if errorlevel 1 (
 echo STOP: final artifact audit failed.
 popd
 exit /b 2
)
popd
echo Both pipelines completed and verified.
exit /b 0
