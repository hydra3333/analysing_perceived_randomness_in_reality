OUTLANDISH_01 -- Windows Sandbox persistent-Python CANDIDATE v4
7 November 2026

PURPOSE
Run the previously working Windows Sandbox automatic setup without installing
Python. In a SECOND, manually invoked echo-on BAT, install an isolated test
Python 3.15.2 into the writable mapped DATA tree on host T:. After restarting
Sandbox, verify it can run independently of the old guest-only Windows registry.
Only then install the owner's original, unchanged pip dependencies.

IMPORTANT: This is a feasibility experiment. A Python full installer MAY reject
installing onto a Windows Sandbox mapped folder; Windows Installer may still
create registration/cache state in disposable guest C:. The previous guest-C:
installation ended with a ZERO-BYTE python.exe and ERROR_FILE_INVALID.
Do not assume persistent installation or package stability until verified.

HOST (normal Windows, sandbox CLOSED):
  Host source (READ ONLY in guest): T:\OUTLANDISH_01_SANDBOX
  Host data (READ/WRITE in guest): T:\OUTLANDISH_01_SANDBOX_DATA
  v4 files go in: T:\OUTLANDISH_01_SANDBOX\SANDBOX\

  Backup the current SANDBOX BATs first. Extract all ten v4 files into the
  SANDBOX directory, replacing only files with matching names. Keep the user's
  original T:\OUTLANDISH_01_SANDBOX\PYTHON\000-Pip-Install-Dependencies.bat.
  Do not move or edit the existing host OUTLANDISH TOML or the six billion-digit
  registered files on G:. The .wsb is unchanged from v3 and may be retained.
  Ensure T:\OUTLANDISH_01_SANDBOX_DATA exists BEFORE launching the .wsb.

GUEST: INITIAL SANDBOX STARTUP (AUTOMATIC; NO PYTHON)
  Launch T:\OUTLANDISH_01_SANDBOX\SANDBOX\OUTLANDISH_01_sandbox.wsb.
  The unchanged .wsb maps C:\HOST_OUTLANDISH_SOURCE read-only and
  C:\HOST_OUTLANDISH_DATA read-write. Startup runs OUTLANDISH_01_Setup.bat.
  Explorer, compact view, Notepad++, three shortcuts, disposable working tree,
  sandbox TOML are prepared as in v3. Python is NOT executed or installed.
  Only a candidate parent and logs folder are created (if missing):
    T:\OUTLANDISH_01_SANDBOX_DATA\python_candidate\
    T:\OUTLANDISH_01_SANDBOX_DATA\python_candidate\logs\
  The installer target Python315 folder is NOT precreated.
  Auto log: T:\OUTLANDISH_01_SANDBOX_DATA\OUTLANDISH_01_setup_auto.log

GUEST: FIRST-TIME MANUAL INSTALL (CMD INSIDE SANDBOX ONLY)
  "C:\HOST_OUTLANDISH_SOURCE\SANDBOX\OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat" INSTALL

  This script is ECHO ON, pauses before installing, displays installer progress,
  and saves the installer logs under ...\python_candidate\logs. The official
  python-3.15.2-amd64.exe is used with options corresponding to the owner's UI:
    InstallAllUsers=0, Include_doc=0, Include_tcltk=0, Include_test=0,
    CompileAll=0, Include_dev/exe/lib/tools/pip=1,
    TargetDir=C:\HOST_OUTLANDISH_DATA\python_candidate\Python315.
  To minimise nonpersistent guest registrations, it additionally excludes
  Python install manager/launcher, file associations and Python shortcuts,
  and DOES NOT permanently edit the Windows PATH (a helper BAT does that).
  User's original Explorer and Notepad++ customisations remain preserved.

  If the installer fails, DO NOT rerun it blindly. Inspect saved logs and
  partial files in the candidate root. Do not delete them until reviewed.
  If success, the BAT verifies sys.prefix, site-packages and pip installation
  paths are under the persistent target and saves a known-good SHA256 record.

GUEST: RESTART TEST -- MOST IMPORTANT
  Close Sandbox normally after a successful INSTALL. Open the .wsb again.
  In a new Sandbox CMD, run:
  "C:\HOST_OUTLANDISH_SOURCE\SANDBOX\OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat" VERIFY

  VERIFY checks Python execution, pip execution, site-packages placement, and
  equality of interpreter SHA256 to the successful INSTALL baseline.
  If VERIFY fails, STOP. This approach has not demonstrated persistence.
  A ready marker alone is not trusted; actual execution and checksum are tested.

GUEST: FULL ORIGINAL PIP DEPENDENCIES (ONLY AFTER VERIFY)
  "C:\HOST_OUTLANDISH_SOURCE\SANDBOX\OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat" DEPS

  This phase sets PATH for its own process, checks Python and package destination,
  and asks you to type RUN before invoking the original dependency BAT UNCHANGED.
  It explicitly uses the correct persistent interpreter and checks its hash
  before AND after installing packages. A generated pip-freeze snapshot is saved
  under ...\python_candidate\logs\pip_freeze_after_deps.txt.

  VERY IMPORTANT: The original dependency BAT contains broad forced upgrades,
  a pip-review --auto call, and a known incorrect `python -m python -m pipdeptree`
  command. A return code of 0 may conceal earlier package failures. The wrapper
  additionally checks pip dependencies and NumPy/SciPy/pandas imports.
  It does NOT establish that all individual packages were installed.
  `PYTHONNOUSERSITE=1` and `PIP_USER=false` are set to discourage pip from
  placing packages under disposable C:\Users\...\AppData.
  Installed interpreter + prefix packages should live together in the mapped
  Python315\Lib\site-packages; VERIFY checks the actual Python configuration.

  The Windows Sandbox .wsb currently permits networking: pip may download data.
  Persistent mapped directories allow guest software to change host T: files.
  The candidate subtree is intentionally separate from OUTLANDISH digits.

USE PYTHON IN ANY NEW SANDBOX CMD
  call "C:\HOST_OUTLANDISH_SOURCE\SANDBOX\OUTLANDISH_01_Python_Env.bat"
  where python
  python --version
  python -m pip --version
  (The helper changes only current CMD PATH, not registry or host settings.)

PREVIEW / 100k TEST ONLY AFTER ALL VERIFICATION
  cd /d C:\OUTLANDISH_WORK
  call PYTHON_ENV.bat
  python outlandish_artifacts.py audit
  python outlandish_artifacts.py status
  python outlandish_big_constants.py pipeline --constant phi --digits 100000
  If preview passes and you deliberately choose to run:
  RUN_PHI_100k_AND_SAVE_REGISTRY.bat
  Result registry is copied from C:\OUTLANDISH_WORK to mapped DATA on success.

NO OTHER ACTIONS AUTOMATICALLY
  - No Python installer / pip on .wsb startup
  - No calculator process at .wsb startup
  - No edits to mapped SOURCE or production OUTLANDISH TOML
  - No disabling Defender / App Control, no elevation, no privileges changes
  - No automatic removal of partial install on failure
  - Automatic BAT has NO pause; manual install BAT intentionally ECHO ON/PAUSE

FILES
  OUTLANDISH_01_Setup.bat             auto startup; compact view etc
  OUTLANDISH_01_Setup_manual_v4.bat   optional manual setup with pauses
  OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat   INSTALL/VERIFY/DEPS
  OUTLANDISH_01_Python_Env.bat        current CMD PATH setup
  OUTLANDISH_01_Open_CMD.bat         interactive helper
  RUN_PHI_100k_AND_SAVE_REGISTRY.bat explicit computation helper
  OUTLANDISH_01_sandbox.wsb          same mapping/startup as v3
  OUTLANDISH_01_Sandbox_Explorer_Notepadpp.reg original 9 + NPP
  outlandish.sandbox.toml            clean test-only digits registry
  README_PERSISTENT_PYTHON.txt       this file

These scripts were statically inspected on Linux. The Python MSI installation
into Windows Sandbox mapped folder remains an UNTESTED hypothesis.
