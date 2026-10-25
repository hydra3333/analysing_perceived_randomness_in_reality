@echo off
setlocal DisableDelayedExpansion
rem PROJECT POC: authoritative direct PyPI dependency names are edited HERE.
rem Modes: INSTALL_UPGRADE (default: install anything missing AND upgrade), INSTALL (missing only),
rem UPGRADE (same as INSTALL_UPGRADE), VERIFY (checks only; changes nothing).
rem Any version change is listed; re-run compatibility/reproducibility checks before research use.
rem selenium: owner-run private two-site results check (browser automation, no stealth).
set "DIRECT_PACKAGES=requests beautifulsoup4 psutil numpy scipy threadpoolctl selenium"
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "VENV_ACTIVATE=%ROOT%.venv\Scripts\activate.bat"
set "RC=0"
if not exist "%PY%" goto :missing_venv
if not exist "%VENV_ACTIVATE%" goto :missing_venv
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
if /I "%~1"=="INSTALL" set "MODE=INSTALL"
if /I "%~1"=="INSTALL_UPGRADE" set "MODE=INSTALL_UPGRADE"
if /I "%~1"=="UPGRADE" set "MODE=INSTALL_UPGRADE"
if /I "%~1"=="VERIFY" set "MODE=VERIFY"
if /I not "%~1"=="INSTALL" if /I not "%~1"=="INSTALL_UPGRADE" if /I not "%~1"=="UPGRADE" if /I not "%~1"=="VERIFY" goto :usage
:dispatch
echo [DEPS] Mode: %MODE%
echo [DEPS] Project environment: %EXPECTED_ENV%
echo [DEPS] Direct package requirements: %DIRECT_PACKAGES%
"%PY%" --version
if errorlevel 1 goto :failure
"%PY%" -m pip --version
if errorlevel 1 goto :failure
if not exist "%ROOT%transitory_data" mkdir "%ROOT%transitory_data"
if errorlevel 1 goto :failure
if not exist "%ROOT%transitory_data\dependency_snapshots" mkdir "%ROOT%transitory_data\dependency_snapshots"
if errorlevel 1 goto :failure
set "STAMP=%RANDOM%_%RANDOM%"
if /I "%MODE%"=="VERIFY" goto :post_install
set "BEFORE=%ROOT%transitory_data\dependency_snapshots\before_%STAMP%.txt"
set "AFTER=%ROOT%transitory_data\dependency_snapshots\after_%STAMP%.txt"
"%PY%" -m pip freeze --all > "%BEFORE%"
if errorlevel 1 goto :failure
if /I "%MODE%"=="INSTALL" (
    "%PY%" -m pip install %DIRECT_PACKAGES%
) else (
    "%PY%" -m pip install --upgrade %DIRECT_PACKAGES%
)
if errorlevel 1 goto :failure
"%PY%" -m pip freeze --all > "%AFTER%"
if errorlevel 1 goto :failure
"%PY%" -c "import sys; rd=lambda p: dict(l.strip().split('==',1) for l in open(p,encoding='utf-8',errors='replace') if '==' in l); a=rd(sys.argv[1]); b=rd(sys.argv[2]); ch=[k+': '+a.get(k,'(new)')+' -> '+b[k] for k in sorted(b) if a.get(k)!=b[k]]; [print('[DEPS] CHANGED '+c) for c in ch]; print('[DEPS] No package versions changed.' if not ch else '[DEPS] WARNING: package versions changed. Re-run compatibility and reproducibility checks before using this environment for research.')" "%BEFORE%" "%AFTER%"
if errorlevel 1 goto :failure
:post_install
"%PY%" -m pip check
if errorlevel 1 goto :failure
echo [DEPS] Installed direct package versions:
"%PY%" -c "import importlib.metadata as md,sys; r=[(n,next((d.version for d in md.distributions(name=n)),None)) for n in sys.argv[1:]]; [print(n+('=='+v if v else ' NOT INSTALLED - run this script with INSTALL')) for n,v in r]; sys.exit(0 if all(v for n,v in r) else 7)" %DIRECT_PACKAGES%
if errorlevel 1 goto :failure
rem Snapshot is generated evidence, NOT a second manually maintained dependency list.
set "SNAP=%ROOT%transitory_data\dependency_snapshots\environment_%STAMP%.txt"
"%PY%" -c "import sys,hashlib,pathlib; print('Python:',sys.version.replace(chr(10),' ')); print('Interpreter:',sys.executable); print('Installer_SHA256:',hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest()); print('Installed packages:')" "%~f0" > "%SNAP%"
if errorlevel 1 goto :failure
"%PY%" -m pip freeze --all >> "%SNAP%"
if errorlevel 1 goto :failure
echo [DEPS] Generated environment snapshot: "%SNAP%"
echo [DEPS] SUCCESS. Research runs after upgrades still require compatibility tests.
goto :finish
:missing_venv
echo [DEPS] ERROR: Existing project venv and activate.bat required. >&2
echo [DEPS] Expected interpreter: "%PY%" >&2
set "RC=2"
goto :finish
:wrong_venv
echo [DEPS] ERROR: Another virtual environment is active: "%VIRTUAL_ENV%" >&2
set "RC=3"
goto :finish
:activation_failed
echo [DEPS] ERROR: Project venv activation failed. >&2
set "RC=4"
goto :finish
:prefix_failed
echo [DEPS] ERROR: Python sys.prefix does not match project venv. >&2
set "RC=5"
goto :finish
:usage
echo Usage: %~nx0 [INSTALL_UPGRADE (default) ^| INSTALL ^| UPGRADE ^| VERIFY] >&2
set "RC=6"
goto :finish
:failure
set "RC=%ERRORLEVEL%"
if "%RC%"=="0" set "RC=1"
echo [DEPS] ERROR: dependency operation or verification failed; exit=%RC%. >&2
:finish
endlocal & exit /b %RC%
