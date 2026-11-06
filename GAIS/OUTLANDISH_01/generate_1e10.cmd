@echo off
rem OUTLANDISH_01 v0.2: preview by default. Explicit RUN required for generation.
rem IMPORTANT: >=5e9 defaults to Windows swap mode; known to require elevation.
rem No unreviewed RAM-only override is made by this convenience wrapper.
setlocal
pushd "%~dp0" || exit /b 1
python outlandish_artifacts.py audit
if errorlevel 1 (popd & exit /b 2)
if /I "%~1"=="RUN" (
  set "RUN_FLAG=--run"
) else (
  set "RUN_FLAG="
  echo PREVIEW ONLY. To explicitly launch after resolving the memory issue:
  echo     generate_1e10.cmd RUN
)
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000 %RUN_FLAG%
if errorlevel 1 (echo Pi pipeline failed; no phi attempted. & popd & exit /b 2)
python outlandish_big_constants.py pipeline --constant phi --digits 10000000000 %RUN_FLAG%
if errorlevel 1 (echo Phi pipeline failed. & popd & exit /b 2)
python outlandish_artifacts.py audit
if errorlevel 1 (popd & exit /b 2)
popd
exit /b 0
