@echo on
@setlocal EnableExtensions DisableDelayedExpansion
REM MANUAL diagnostic Windows Sandbox setup. Pauses are intentionally retained.
REM No Python install or execution at setup; separate manual installer is provided.
REM Prefer OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat for INSTALL / VERIFY / DEPS.
if /I not "%USERNAME%"=="WDAGUtilityAccount" goto FORBIDDEN
if /I "%COMPUTERNAME%"=="3900X" goto FORBIDDEN
set "SRC=C:\HOST_OUTLANDISH_SOURCE"
set "DATA=C:\HOST_OUTLANDISH_DATA"
set "DST=C:\OUTLANDISH_WORK"
set "DEPBAT=%SRC%\PYTHON\000-Pip-Install-Dependencies.bat"
set "REGFILE=%SRC%\SANDBOX\OUTLANDISH_01_Sandbox_Explorer_Notepadpp.reg"
set "NPP_EXE=C:\HOST_SOFTWARE\NPP\notepad++.exe"
set "PYROOT=%DATA%\python_candidate"
set "PYHOME=%PYROOT%\Python315"
if /I "%~1"=="DEPS" goto DEPS_MANUAL
if not "%~1"=="" goto USAGE
:MAIN

echo [1/5] Checking mapped folders and required source files...
if not exist "%SRC%\outlandish_big_constants.py" goto MISSING_SOURCE
if not exist "%SRC%\SANDBOX\outlandish.sandbox.toml" goto MISSING_SOURCE
if not exist "%SRC%\y-cruncher v0.8.7.9547b\y-cruncher.exe" goto MISSING_SOURCE
if not exist "%SRC%\SANDBOX\OUTLANDISH_01_Open_CMD.bat" goto MISSING_SOURCE
if not exist "%SRC%\SANDBOX\RUN_PHI_100k_AND_SAVE_REGISTRY.bat" goto MISSING_SOURCE
if not exist "%SRC%\SANDBOX\OUTLANDISH_01_Python_Env.bat" goto MISSING_SOURCE
if not exist "%DATA%" goto MISSING_DATA
if not exist "%REGFILE%" goto MISSING_REG
pause

echo [1b/5] Prepare the persistent Python candidate parent, NOT the install directory...
if not exist "%PYROOT%\" mkdir "%PYROOT%"
if errorlevel 1 goto FAIL
if not exist "%PYROOT%\logs\" mkdir "%PYROOT%\logs"
if errorlevel 1 goto FAIL
set "PATH=%PYHOME%;%PYHOME%\Scripts;%PATH%"
set "PYTHONNOUSERSITE=1"
set "PIP_USER=false"
echo Candidate: %PYHOME%
pause

echo [2/5] Applying Explorer and Notepad++ customisations...
reg.exe import "%REGFILE%"
if errorlevel 1 goto FAIL
REM Extra compact-view preference, absent from original nine-item .reg file.
reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v UseCompactMode /t REG_DWORD /d 1 /f
if errorlevel 1 goto FAIL
reg.exe query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v UseCompactMode
if errorlevel 1 goto FAIL
if not exist "%NPP_EXE%" echo WARNING: Notepad++ not found at "%NPP_EXE%".
pause

echo [3/5] Creating three desktop shortcuts (PowerShell, NOT VBScript)...
powershell.exe -NoProfile -NonInteractive -Command "$ErrorActionPreference='Stop'; $sh=New-Object -ComObject WScript.Shell; $desk=[Environment]::GetFolderPath('Desktop'); foreach($p in @(@('HOST_software','C:\HOST_SOFTWARE'),@('HOST_OUTLANDISH_01','C:\HOST_OUTLANDISH_SOURCE'),@('HOST_OUTLANDISH_DATA','C:\HOST_OUTLANDISH_DATA'))) { $sc=$sh.CreateShortcut((Join-Path $desk ($p[0]+'.lnk'))); $sc.TargetPath=$p[1]; $sc.Save() }"
if errorlevel 1 goto FAIL
if not exist "%USERPROFILE%\Desktop\HOST_software.lnk" goto FAIL
if not exist "%USERPROFILE%\Desktop\HOST_OUTLANDISH_01.lnk" goto FAIL
if not exist "%USERPROFILE%\Desktop\HOST_OUTLANDISH_DATA.lnk" goto FAIL
dir "%USERPROFILE%\Desktop\HOST*.lnk"
pause

echo [4/5] Preparing disposable OUTLANDISH workspace...
if not exist "%DST%" mkdir "%DST%"
if errorlevel 1 goto FAIL
for %%F in (outlandish_config.py outlandish_artifacts.py outlandish_big_constants.py outlandish_powerball_stage_a.py test_outlandish_v02.py POWERBALL_preholdout_only.csv) do (
  copy /Y "%SRC%\%%F" "%DST%\%%F" >nul
  if errorlevel 1 goto FAIL
)
robocopy "%SRC%\y-cruncher v0.8.7.9547b" "%DST%\y-cruncher v0.8.7.9547b" /E /R:1 /W:1 /NFL /NDL /NJH /NJS /NP
if errorlevel 8 goto FAIL
pause

echo [5/5] Selecting sandbox-only TOML and copying helper BATs...
REM The production TOML in mapped SOURCE must never be overwritten.
if exist "%DATA%\outlandish.local.toml" (
  echo Using previously saved sandbox registry from DATA.
  copy /Y "%DATA%\outlandish.local.toml" "%DST%\outlandish.local.toml" >nul
) else (
  echo Using the clean sandbox TOML template.
  copy /Y "%SRC%\SANDBOX\outlandish.sandbox.toml" "%DST%\outlandish.local.toml" >nul
)
if errorlevel 1 goto FAIL
copy /Y "%SRC%\SANDBOX\OUTLANDISH_01_Open_CMD.bat" "%DST%\OPEN_CMD.bat" >nul
if errorlevel 1 goto FAIL
copy /Y "%SRC%\SANDBOX\RUN_PHI_100k_AND_SAVE_REGISTRY.bat" "%DST%\RUN_PHI_100k_AND_SAVE_REGISTRY.bat" >nul
if errorlevel 1 goto FAIL
copy /Y "%SRC%\SANDBOX\OUTLANDISH_01_Python_Env.bat" "%DST%\PYTHON_ENV.bat" >nul
if errorlevel 1 goto FAIL
pause

echo.
echo SETUP COMPLETE: Registry, compact view, desktop shortcuts, work tree.
echo Python was NOT installed or executed by this setup.
echo MANUAL install / verify / deps:
echo   "%SRC%\SANDBOX\OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat" INSTALL / VERIFY / DEPS
echo No computation has been launched.

REM This manual setup only opens the prepared directory; no Python calls.
start "" explorer.exe "%DST%"
start "OUTLANDISH Sandbox CMD" cmd.exe /k "cd /d C:\OUTLANDISH_WORK"
echo Press any key to finish manual setup.
pause
exit /b 0
:DEPS_MANUAL
REM Optional pip phase, never run until Python has been installed manually.
echo About to run the original OWNER dependency BAT. Python must already work.
pause

:DEPS
REM Optional legacy DEPS phase. Prefer dedicated persistent installer.
call "%SRC%\SANDBOX\OUTLANDISH_01_Python_Env.bat"
if errorlevel 1 goto FAIL
if not exist "%PYHOME%\python.exe" goto FAIL
if not exist "%DEPBAT%" goto MISSING_DEP
echo.
echo [DEPS] Running owner's dependency BAT unchanged:
echo   "%DEPBAT%"
echo.
REM pip-review may write requirements.txt; use guest TEMP, never mapped SOURCE.
set "DEPWORK=%TEMP%\OUTLANDISH_DEP_SETUP"
if not exist "%DEPWORK%" mkdir "%DEPWORK%"
if errorlevel 1 goto FAIL
pushd "%DEPWORK%"
if errorlevel 1 goto FAIL
cmd.exe /d /c ""%DEPBAT%""
set "PIP_RC=%ERRORLEVEL%"
popd
if not "%PIP_RC%"=="0" (
  echo ERROR: Dependency BAT returned %PIP_RC%.
  goto FAIL
)
REM Original BAT can mask errors; independently check relevant imports.
python -m pip check
if errorlevel 1 goto FAIL
python -c "import numpy, scipy, pandas; print('Scientific imports OK:', numpy.__version__, scipy.__version__, pandas.__version__)"
if errorlevel 1 goto FAIL
REM Original BAT contains a known typo in the pipdeptree command.
python -m pipdeptree > "%DEPWORK%\pipdeptree.txt" 2>&1
if errorlevel 1 echo NOTE: pipdeptree failed; see "%DEPWORK%\pipdeptree.txt".
echo [DEPS] Dependency phase finished; no calculation was launched.
pause
exit /b 0

:FORBIDDEN
echo SAFETY STOP: Windows Sandbox WDAGUtilityAccount only; refusing to run.
pause
exit /b 1
:MISSING_SOURCE
echo ERROR: Missing OUTLANDISH source, clean TOML, y-cruncher, or helper BATs.
goto FAIL
:MISSING_DATA
echo ERROR: Missing writable DATA mapping. Create T:\OUTLANDISH_01_SANDBOX_DATA on host.
goto FAIL
:MISSING_REG
echo ERROR: Missing registry file: "%REGFILE%"
goto FAIL
:MISSING_DEP
echo ERROR: Missing owner's dependency BAT: "%DEPBAT%"
goto FAIL
:USAGE
echo USAGE: %~nx0 [DEPS]
exit /b 2
:FAIL
echo SETUP FAILED; no calculation was launched.
pause
exit /b 1
