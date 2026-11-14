@echo off
setlocal DisableDelayedExpansion
rem 39 direct requirements; mirror these in the future per-user installer.
rem Source: union of both original lists, minus redundant Python stdlib configparser backport.
rem The standard configparser module comes with Python 3.15; no PyPI backport needed.
rem Host-specific source policy: COMPUTERNAME=3900X allows source distributions.
rem All other hosts require wheels only, including dependencies and the pip upgrade.
rem The /I comparison of COMPUTERNAME is case-insensitive.
rem Clear any inherited PIP_ONLY_BINARY value before applying this policy.
rem Missing installs or LibCST import failures are reported; final exit is nonzero if incomplete.
set "PIP_ONLY_BINARY="
set "INSTALL_POLICY=SOURCE_ALLOWED"
if /I not "%COMPUTERNAME%"=="3900X" set "PIP_ONLY_BINARY=:all:"
if /I not "%COMPUTERNAME%"=="3900X" set "INSTALL_POLICY=WHEELS_ONLY"
rem Modes: INSTALL_UPGRADE (default), INSTALL (alias for upgrade), UPGRADE, VERIFY (read-only).
rem Explicit Python interpreter, not the possibly active python on PATH.
rem This script does not uninstall PyInstaller or run pip-review --auto.
rem These are independent environments; equal names do not guarantee equal installed versions.
set "DIRECT_PACKAGES=pip tzdata tzlocal pytz numpy pandas mypy pymediainfo pydub sockets requests python-utils python-dotenv pyyaml html5lib psutil pywin32 pywin32-ctypes python-dateutil blake3 chardet charset-normalizer libcst wakepy pystray pillow py7zr rich pydantic beautifulsoup4 scipy threadpoolctl selenium pyahocorasick setuptools wheel packaging pipdeptree pip-review"
set "APP_PACKAGES=tzdata tzlocal pytz numpy pandas mypy pymediainfo pydub sockets requests python-utils python-dotenv pyyaml html5lib psutil pywin32 pywin32-ctypes python-dateutil blake3 chardet charset-normalizer libcst wakepy pystray pillow py7zr rich pydantic beautifulsoup4 scipy threadpoolctl selenium pyahocorasick setuptools wheel packaging pipdeptree pip-review"
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%.venv\Scripts\activate.bat"
set "SNAP_DIR=%ROOT%transitory_data\dependency_snapshots"
set "RC=0"
if not exist "%PY%" goto :missing_python
if not exist "%VENV_ACTIVATE%" goto :missing_python
for %%I in ("%ROOT%.venv\.") do set "EXPECTED_ENV=%%~fI"
if defined VIRTUAL_ENV goto :check_active
call "%VENV_ACTIVATE%"
if errorlevel 1 goto :activation_failed
if not defined VIRTUAL_ENV goto :activation_failed
goto :verify_python
:check_active
for %%I in ("%VIRTUAL_ENV%\.") do set "ACTIVE_ENV=%%~fI"
if /I not "%ACTIVE_ENV%"=="%EXPECTED_ENV%" goto :wrong_venv
:verify_python
"%PY%" -c "import sys,pathlib;sys.exit(0 if pathlib.Path(sys.prefix).resolve()==pathlib.Path(sys.argv[1]).resolve() else 12)" "%EXPECTED_ENV%"
if errorlevel 1 goto :prefix_failed
set "MODE=INSTALL_UPGRADE"
if not "%~2"=="" goto :usage
if "%~1"=="" goto :dispatch
if /I "%~1"=="INSTALL" set "MODE=INSTALL_UPGRADE"
if /I "%~1"=="INSTALL_UPGRADE" set "MODE=INSTALL_UPGRADE"
if /I "%~1"=="UPGRADE" set "MODE=INSTALL_UPGRADE"
if /I "%~1"=="VERIFY" set "MODE=VERIFY"
if /I not "%~1"=="INSTALL" if /I not "%~1"=="INSTALL_UPGRADE" if /I not "%~1"=="UPGRADE" if /I not "%~1"=="VERIFY" goto :usage
:dispatch
echo [DEPS] Mode: %MODE%
echo [DEPS] Environment: project .venv
echo [DEPS] Computer: %COMPUTERNAME%
echo [DEPS] Package policy: %INSTALL_POLICY%
echo [DEPS] Python: "%PY%"
echo [DEPS] 39 direct packages: %DIRECT_PACKAGES%
"%PY%" --version
if errorlevel 1 goto :failure
"%PY%" -m pip --version
if errorlevel 1 goto :failure
if not exist "%SNAP_DIR%" mkdir "%SNAP_DIR%"
if errorlevel 1 goto :failure
set "STAMP=%RANDOM%_%RANDOM%"
if /I "%MODE%"=="VERIFY" goto :post_install
set "BEFORE=%SNAP_DIR%\before_%STAMP%.txt"
set "AFTER=%SNAP_DIR%\after_%STAMP%.txt"
"%PY%" -m pip freeze --all > "%BEFORE%"
if errorlevel 1 goto :failure
rem Upgrade pip first for every installation mode, then upgrade all direct requirements.
rem VERIFY remains read-only.
rem Host-specific binary policy applies to pip and its dependencies too.
echo [DEPS] Upgrading pip before other packages.
"%PY%" -m pip install --upgrade pip
if errorlevel 1 goto :failure
"%PY%" -m pip --version
if errorlevel 1 goto :failure
rem Install direct requirements individually so one failure does not block the rest.
rem On non-3900X hosts, source builds are blocked. Any failure is recorded, and
rem overall success is refused even if other packages install successfully.
set "UNAVAILABLE=%SNAP_DIR%\unavailable_%STAMP%.txt"
if exist "%UNAVAILABLE%" del /q "%UNAVAILABLE%"
if errorlevel 1 goto :failure
rem LibCST 0.3.x is not usable on Python 3.15 (import fails).
rem Require LibCST 1.9.0 or newer; never fall back to an older wheel.
rem LibCST 1.9.0 needs PyYAML. Its source build may be attempted on 3900X.
for %%P in (%APP_PACKAGES%) do (
    if /I "%%P"=="libcst" (
        "%PY%" -m pip install --upgrade "libcst>=1.9.0"
    ) else (
        "%PY%" -m pip install --upgrade %%P
    )
    if errorlevel 1 (
        echo [DEPS] INSTALL FAILED - %INSTALL_POLICY%: %%P
        >> "%UNAVAILABLE%" echo %%P
    )
)
"%PY%" -m pip freeze --all > "%AFTER%"
if errorlevel 1 goto :failure
"%PY%" -c "import sys; rd=lambda p: dict(l.strip().split('==',1) for l in open(p,encoding='utf-8',errors='replace') if '==' in l); a=rd(sys.argv[1]); b=rd(sys.argv[2]); ch=[k+': '+a.get(k,'(new)')+' -> '+b[k] for k in sorted(b) if a.get(k)!=b[k]]; [print('[DEPS] CHANGED '+c) for c in ch]; print('[DEPS] No package versions changed.' if not ch else '[DEPS] WARNING: package versions changed. Re-run compatibility checks before research.')" "%BEFORE%" "%AFTER%"
if errorlevel 1 goto :failure
:post_install
set "INCOMPLETE=0"
if exist "%UNAVAILABLE%" set "INCOMPLETE=1"
"%PY%" -m pip check
if errorlevel 1 (
    echo [DEPS] WARNING: pip check found broken requirements.
    set "INCOMPLETE=1"
)
rem Metadata alone is insufficient: old LibCST installs but fails to import on 3.15.
"%PY%" -c "import libcst; assert libcst.parse_module('x = 1').code == 'x = 1'"
if errorlevel 1 (
    echo [DEPS] WARNING: LibCST import/parse test FAILED; this environment is incomplete.
    set "INCOMPLETE=1"
)
echo [DEPS] Installed direct package versions:
"%PY%" -c "import importlib.metadata as md,sys; r=[(n,next((d.version for d in md.distributions(name=n)),None)) for n in sys.argv[1:]]; [print(n+('=='+v if v else ' NOT INSTALLED')) for n,v in r]; sys.exit(0 if all(v for n,v in r) else 7)" %DIRECT_PACKAGES%
if errorlevel 1 set "INCOMPLETE=1"
set "SNAP=%SNAP_DIR%\environment_%STAMP%.txt"
"%PY%" -c "import sys,hashlib,pathlib; print('Python:',sys.version.replace(chr(10),' ')); print('Interpreter:',sys.executable); print('Installer_SHA256:',hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest()); print('Installed packages:')" "%~f0" > "%SNAP%"
if errorlevel 1 goto :failure
"%PY%" -m pip freeze --all >> "%SNAP%"
if errorlevel 1 goto :failure
echo [DEPS] Generated environment snapshot: "%SNAP%"
if "%INCOMPLETE%"=="1" goto :incomplete
echo [DEPS] SUCCESS. All 39 direct requirements installed; research compatibility tests remain required.
goto :finish
:incomplete
echo [DEPS] INCOMPLETE. One or more of the 39 required packages could not be installed or verified.
if exist "%UNAVAILABLE%" (
    echo [DEPS] Packages whose installation failed:
    type "%UNAVAILABLE%"
    echo [DEPS] Failure list saved: "%UNAVAILABLE%"
)
echo [DEPS] Install policy was %INSTALL_POLICY%. Inspect failures and rerun compatibility tests.
set "RC=1"
goto :finish
:missing_python
echo [DEPS] ERROR: Project .venv python.exe and activate.bat must exist next to this batch file. >&2
echo [DEPS] Expected Python: "%PY%" >&2
set "RC=2"
goto :finish
:wrong_venv
echo [DEPS] ERROR: Another venv is active: "%VIRTUAL_ENV%". >&2
set "RC=3"
goto :finish
:activation_failed
echo [DEPS] ERROR: Project .venv activation failed. >&2
set "RC=4"
goto :finish
:prefix_failed
echo [DEPS] ERROR: Python sys.prefix does not match project .venv. >&2
set "RC=5"
goto :finish
:usage
echo Usage: %~nx0 [INSTALL_UPGRADE ^| INSTALL ^| UPGRADE ^| VERIFY] >&2
set "RC=6"
goto :finish
:failure
set "RC=%ERRORLEVEL%"
if "%RC%"=="0" set "RC=1"
echo [DEPS] ERROR: operation or verification failed, exit=%RC%. No success claimed. >&2
:finish
endlocal & exit /b %RC%
