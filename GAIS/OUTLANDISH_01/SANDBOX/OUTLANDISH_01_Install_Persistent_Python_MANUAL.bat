@echo on
@setlocal EnableExtensions DisableDelayedExpansion
REM OUTLANDISH persistent Python candidate experiment. RUN INSIDE WINDOWS SANDBOX ONLY.
REM Default is INSTALL. VERIFY and DEPS are separate phases.
REM No installation runs from .wsb startup, and no scientific computation runs here.

if /I not "%USERNAME%"=="WDAGUtilityAccount" goto FORBIDDEN
if /I "%COMPUTERNAME%"=="3900X" goto FORBIDDEN
set "SRC=C:\HOST_OUTLANDISH_SOURCE"
set "DATA=C:\HOST_OUTLANDISH_DATA"
set "INSTALLER=%SRC%\PYTHON\python-3.15.2-amd64.exe"
set "OWNER_DEPBAT=%SRC%\PYTHON\000-Pip-Install-Dependencies.bat"
call "%SRC%\SANDBOX\OUTLANDISH_01_Python_Env.bat"
if errorlevel 1 goto FAIL
set "PYROOT=%OUTLANDISH_PYROOT%"
set "PYHOME=%OUTLANDISH_PYHOME%"
set "PYEXE=%PYHOME%\python.exe"
set "LOGDIR=%PYROOT%\logs"
if not exist "%PYROOT%\" mkdir "%PYROOT%"
if errorlevel 1 goto FAIL
if not exist "%LOGDIR%\" mkdir "%LOGDIR%"
if errorlevel 1 goto FAIL

if /I "%~1"=="DEPS" goto DEPS
if /I "%~1"=="VERIFY" goto VERIFY
if /I "%~1"=="INSTALL" goto INSTALL
if "%~1"=="" goto INSTALL
goto USAGE

:INSTALL
echo [INSTALL] Target Python directory: %PYHOME%
echo [INSTALL] Python installer: %INSTALLER%
echo [INSTALL] This is a new CANDIDATE only. Do not use it for production.
if not exist "%INSTALLER%" goto MISSING_INSTALLER
if exist "%PYHOME%\" if not exist "%PYEXE%" (
  echo ERROR: Partial Python315 directory found without python.exe.
  echo Refusing to install over an incomplete candidate. Inspect the folder and logs.
  goto FAIL
)
if exist "%PYEXE%" (
  echo Existing python.exe detected: refusing to run installer again.
  echo Use VERIFY; if invalid, inspect before making a NEW candidate directory.
  goto VERIFY
)
if exist "%LOGDIR%\python_known_good.sha256.txt" (
  echo ERROR: Previous install checksum exists but python.exe is missing.
  goto FAIL
)
echo [INSTALL] User options: just-for-me, no documentation, no TclTk/IDLE,
echo [INSTALL] no test suite, no standard-library precompilation.
echo [INSTALL] Deviations: no launcher or shell associations; PATH is handled by BAT.
echo [INSTALL] Visible MSI progress and persistent log under %LOGDIR%.
echo [INSTALL] Persistent mapped path may be rejected by Windows Installer.
echo.
echo Press a key to START the persistent candidate installation, or Ctrl+C to cancel.
pause
start /wait "" "%INSTALLER%" /passive /log "%LOGDIR%\python_installer.log" InstallAllUsers=0 "TargetDir=%PYHOME%" Include_doc=0 Include_tcltk=0 Include_test=0 CompileAll=0 Include_dev=1 Include_exe=1 Include_lib=1 Include_tools=1 Include_pip=1 Include_launcher=0 InstallLauncherAllUsers=0 Shortcuts=0 AssociateFiles=0 PrependPath=0 AppendPath=0
set "INSTALL_RC=%ERRORLEVEL%"
echo Installer exit code: %INSTALL_RC%
if not "%INSTALL_RC%"=="0" (
  echo ERROR: Installer failed. Review %LOGDIR%\python_installer.log
  echo Do NOT delete or retry blindly; partial installation may exist.
  goto FAIL
)
if not exist "%PYEXE%" (
  echo ERROR: Installer returned zero but target python.exe is missing.
  goto FAIL
)
call :VERIFY_RUNTIME
if errorlevel 1 goto FAIL
certutil -hashfile "%PYEXE%" SHA256 > "%LOGDIR%\python_known_good.sha256.txt"
if errorlevel 1 goto FAIL
echo [INSTALL] Baseline SHA-256 saved. DO NOT install dependencies yet.
echo [INSTALL] Close and reopen Sandbox; then run this BAT with VERIFY.
echo [INSTALL] Only after successful fresh-session VERIFY, run this BAT with DEPS.
goto SUCCESS

:VERIFY
echo [VERIFY] Checking Python on persistent mapped T: DATA...
if not exist "%LOGDIR%\python_known_good.sha256.txt" (
  echo ERROR: No successful INSTALL baseline checksum. Incomplete install?
  goto FAIL
)
call :VERIFY_RUNTIME
if errorlevel 1 goto FAIL
certutil -hashfile "%PYEXE%" SHA256 > "%LOGDIR%\python_current.sha256.txt"
if errorlevel 1 goto FAIL
fc /b "%LOGDIR%\python_known_good.sha256.txt" "%LOGDIR%\python_current.sha256.txt" >nul
if errorlevel 1 (
  echo ERROR: python.exe checksum changed from install baseline.
  goto FAIL
)
echo [VERIFY] PASS. Python and pip run and correct persistent paths are selected.
goto SUCCESS

:DEPS
echo [DEPS] Full owner's original dependency installer - NOT a small test list.
echo [DEPS] It performs many upgrades and pip-review --auto.
call :VERIFY_RUNTIME
if errorlevel 1 goto FAIL
if not exist "%LOGDIR%\python_known_good.sha256.txt" (
  echo ERROR: No known-good Python baseline. Run INSTALL and fresh-session VERIFY.
  goto FAIL
)
certutil -hashfile "%PYEXE%" SHA256 > "%LOGDIR%\python_before_deps.sha256.txt"
if errorlevel 1 goto FAIL
fc /b "%LOGDIR%\python_known_good.sha256.txt" "%LOGDIR%\python_before_deps.sha256.txt" >nul
if errorlevel 1 (
  echo ERROR: interpreter checksum differs before dependencies. Refusing.
  goto FAIL
)
if not exist "%OWNER_DEPBAT%" goto MISSING_DEPBAT
set "DEPWORK=%TEMP%\OUTLANDISH_DEP_SETUP"
if not exist "%DEPWORK%\" mkdir "%DEPWORK%"
if errorlevel 1 goto FAIL
echo WARNING: Your BAT may mask intermediate pip failures.
echo WARNING: Installed files on mapped DATA survive closing Sandbox.
set "CONFIRM="
set /p "CONFIRM=Type RUN to execute YOUR ENTIRE dependency BAT (anything else skips): "
if /I not "%CONFIRM%"=="RUN" (
  echo [DEPS] Cancelled by user; no dependencies changed.
  goto SUCCESS
)
pushd "%DEPWORK%"
if errorlevel 1 goto FAIL
call "%OWNER_DEPBAT%"
set "DEPS_RC=%ERRORLEVEL%"
popd
echo [DEPS] Original BAT exit code: %DEPS_RC% (may not reflect all failures).
if not "%DEPS_RC%"=="0" goto FAIL
call :VERIFY_RUNTIME
if errorlevel 1 goto FAIL
certutil -hashfile "%PYEXE%" SHA256 > "%LOGDIR%\python_after_deps.sha256.txt"
if errorlevel 1 goto FAIL
fc /b "%LOGDIR%\python_known_good.sha256.txt" "%LOGDIR%\python_after_deps.sha256.txt" >nul
if errorlevel 1 (
  echo ERROR: interpreter checksum changed during dependency installation.
  goto FAIL
)
"%PYEXE%" -m pip check
if errorlevel 1 goto FAIL
"%PYEXE%" -c "import numpy, scipy, pandas; print('Scientific imports OK:', numpy.__version__, scipy.__version__, pandas.__version__)"
if errorlevel 1 goto FAIL
"%PYEXE%" -m pip freeze > "%LOGDIR%\pip_freeze_after_deps.txt"
if errorlevel 1 goto FAIL
echo [DEPS] PASS for interpreter integrity, pip check, and NumPy/SciPy/pandas.
echo [DEPS] This does not prove every original BAT command succeeded.
goto SUCCESS

:VERIFY_RUNTIME
if not exist "%PYEXE%" (
  echo ERROR: Persistent Python does not exist: %PYEXE%
  exit /b 1
)
for %%F in ("%PYEXE%") do if %%~zF EQU 0 (
  echo ERROR: python.exe is ZERO bytes. Stop; do not run pip or repair.
  exit /b 1
)
"%PYEXE%" --version
if errorlevel 1 exit /b 1
"%PYEXE%" -c "import os,sys,sysconfig; h=os.environ['OUTLANDISH_PYHOME']; p=sys.prefix; s=sysconfig.get_path('purelib'); e=os.path.join(h,'Lib','site-packages'); print('sys.prefix=',p); print('pip site-packages=',s); assert os.path.normcase(os.path.abspath(p))==os.path.normcase(os.path.abspath(h)), 'Wrong interpreter prefix'; assert os.path.normcase(os.path.abspath(s))==os.path.normcase(os.path.abspath(e)), 'Packages would not go to persistent Python tree'"
if errorlevel 1 exit /b 1
"%PYEXE%" -m pip --version
if errorlevel 1 exit /b 1
exit /b 0

:MISSING_INSTALLER
echo ERROR: Cannot find installer at "%INSTALLER%".
goto FAIL
:MISSING_DEPBAT
echo ERROR: Cannot find owner's pip BAT at "%OWNER_DEPBAT%".
goto FAIL
:FORBIDDEN
echo SAFETY STOP: Windows Sandbox WDAGUtilityAccount only, never host.
exit /b 1
:USAGE
echo Usage: %~nx0 [INSTALL ^| VERIFY ^| DEPS]
echo Default: INSTALL. No computation is started.
exit /b 2
:FAIL
echo.
echo MANUAL PHASE FAILED. Do not close the Sandbox before inspecting errors/logs.
pause
exit /b 1
:SUCCESS
echo.
echo MANUAL PHASE COMPLETE. No OUTLANDISH computation was started.
pause
exit /b 0
