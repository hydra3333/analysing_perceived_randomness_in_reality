@echo on
@setlocal ENABLEDELAYEDEXPANSION
@setlocal enableextensions

REM ------------------------------------------------------------
REM OUTLANDISH_01 / Windows Sandbox / persistent Python candidate.
REM v5: first install C++ Build Tools IN THIS SANDBOX if needed.
REM This BAT is called by v4's existing MANUAL.bat DEPS phase.
REM No change to Python location; no scientific computation here.
REM Build Tools installation is DISPOSABLE and may be needed in a
REM future fresh Sandbox only if more packages must be compiled.
REM The underlying pip package commands remain in original order.
REM Every pip failure now stops rather than being hidden.
REM ------------------------------------------------------------
if /I not "%USERNAME%"=="WDAGUtilityAccount" goto VC_FORBIDDEN
if /I "%COMPUTERNAME%"=="3900X" goto VC_FORBIDDEN
if not exist "C:\HOST_OUTLANDISH_SOURCE\SANDBOX\" goto VC_MISSING_MAPPING
if not exist "C:\HOST_OUTLANDISH_DATA\" goto VC_MISSING_MAPPING
set "VC_BOOT=C:\HOST_OUTLANDISH_SOURCE\SANDBOX\vs_BuildTools.exe"
set "VC_INSTALL=C:\VSBuildTools"
set "VCVARS=%VC_INSTALL%\VC\Auxiliary\Build\vcvars64.bat"
set "VC_LOGDIR=C:\HOST_OUTLANDISH_DATA\python_candidate\logs"
if not exist "%VC_LOGDIR%\" mkdir "%VC_LOGDIR%"
if errorlevel 1 goto VC_FAILED
set "PIP_LOG=%VC_LOGDIR%\pip_verbose_v5.log"
call :ENSURE_BUILD_TOOLS
if errorlevel 1 exit /b 1
REM ------------------------------------------------------------
REM Original owner's pip package list begins here.
REM ------------------------------------------------------------
REM python -m pip install pyinstaller --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose
pip uninstall -y pyinstaller --no-cache-dir --retries 5 --timeout 60 -vv
if errorlevel 1 goto PIP_FAILED

python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pip
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  tzdata
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  tzlocal
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pytz
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  numpy
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pandas
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  mypy
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pymediainfo
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pydub
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pathlib
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  sockets
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  requests
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  datetime
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  python-utils
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  python-dotenv
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pyyaml
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  html5lib
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  configparser
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  psutil
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pywin32
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pywin32-ctypes
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  python-dateutil
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  blake3
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  chardet
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  charset-normalizer
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  libcst
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  wakepy
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pystray
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pillow
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  py7zr
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  rich
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pydantic
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  beautifulsoup4 
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  scipy 
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  threadpoolctl 
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  selenium 
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pyahocorasick 
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  setuptools
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  wheel
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  packaging
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pipdeptree
if errorlevel 1 goto PIP_FAILED
REM pause
python -m pip install --disable-pip-version-check --no-cache-dir --upgrade --check-build-dependencies --upgrade-strategy eager --verbose --no-warn-script-location  pip-review 
if errorlevel 1 goto PIP_FAILED

python -m pip list --outdated
if errorlevel 1 goto PIP_FAILED

python -m pipdeptree
if errorlevel 1 goto PIP_FAILED

REM pip-review switches
REM   -h, --help                  show this help message and exit
REM   --verbose, -v               Show more output
REM   --raw, -r                   Print raw lines (suitable for passing to pip install)
REM   --interactive, -i           Ask interactively to install updates
REM   --auto, -a                  Automatically install every update found
REM   --continue-on-fail, -C      Continue with other installs when one fails
REM   --freeze-outdated-packages  Freeze all outdated packages to "requirements.txt" before upgrading them
pip-review --auto --continue-on-fail --freeze-outdated-packages --verbose 
if errorlevel 1 goto PIP_FAILED
REM pause

echo Finished.
exit /b 0

:ENSURE_BUILD_TOOLS
if exist "%VCVARS%" goto VC_READY
if not exist "%VC_BOOT%" (
  echo ERROR: Missing Microsoft C++ Build Tools bootstrapper:
  echo   "%VC_BOOT%"
  echo Download Build Tools for Visual Studio 2026 from:
  echo   https://visualstudio.microsoft.com/downloads/
  echo Rename the downloaded installer to vs_BuildTools.exe in SANDBOX.
  exit /b 1
)
echo.
echo [BUILD TOOLS] First-time installation into this disposable Sandbox.
echo [BUILD TOOLS] Expected directory: %VC_INSTALL%
echo [BUILD TOOLS] Installing Desktop development with C++ workload.
echo [BUILD TOOLS] Includes MSVC x64/x86 compiler and Windows SDK.
echo [BUILD TOOLS] This is a LARGE download and install; NOT persistent.
echo [BUILD TOOLS] Your Python and pip packages remain on mapped T: data.
echo [BUILD TOOLS] Installer stdout log: %VC_LOGDIR%\vc_buildtools_bootstrapper_v5.log
echo [BUILD TOOLS] The VS installer also creates its own diagnostic logs.
echo.
set "VC_CONFIRM="
set /p "VC_CONFIRM=Type BUILD to start C++ Build Tools installation (anything else cancels): "
if /I not "%VC_CONFIRM%"=="BUILD" exit /b 2
REM The bootstrapper's --wait is REQUIRED for a usable exit code.
start "" /wait "%VC_BOOT%" --installPath "%VC_INSTALL%" --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --passive --norestart --wait > "%VC_LOGDIR%\vc_buildtools_bootstrapper_v5.log" 2>&1
set "VC_RC=%ERRORLEVEL%"
echo [BUILD TOOLS] Bootstrapper exit code: %VC_RC%
if "%VC_RC%"=="3010" (
  echo ERROR: Build Tools requests a Windows restart. Do not start pip.
  echo A restart will discard this Sandbox; reconsider the approach.
  exit /b 1
)
if not "%VC_RC%"=="0" (
  echo ERROR: Build Tools installer did not succeed.
  echo Inspect %VC_LOGDIR%\vc_buildtools_bootstrapper_v5.log
  exit /b 1
)
if not exist "%VCVARS%" (
  echo ERROR: Installer returned zero but vcvars64.bat not found at:
  echo "%VCVARS%"
  exit /b 1
)
:VC_READY
call "%VCVARS%" > "%VC_LOGDIR%\vcvars64_v5.log" 2>&1
if errorlevel 1 (
  echo ERROR: Unable to configure MSVC x64 environment.
  exit /b 1
)
where cl
if errorlevel 1 (
  echo ERROR: MSVC cl.exe unavailable after vcvars64.bat.
  exit /b 1
)
echo [BUILD TOOLS] C++ compiler ready. Starting original dependency list.
exit /b 0

:PIP_FAILED
echo ERROR: A package command failed. Further package changes stopped.
echo Inspect the output and %PIP_LOG%.
exit /b 1

:VC_FORBIDDEN
echo SAFETY STOP: Windows Sandbox WDAGUtilityAccount only; never host.
exit /b 1

:VC_MISSING_MAPPING
echo ERROR: Required Sandbox mapped source or data folder missing.
exit /b 1

:VC_FAILED
echo ERROR: Could not create persistent Build Tools diagnostic directory.
exit /b 1
