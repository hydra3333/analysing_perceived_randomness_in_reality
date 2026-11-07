# OUTLANDISH_01 — development handover and Windows Sandbox diagnostic appendix

**Date:** 2026-11-07 (Australia/Adelaide)  
**Version:** v1  
**Audience:** A new ChatGPT conversation continuing the owner's standalone OUTLANDISH_01 experiment  
**Status:** Handover of owner-reported operating state and current diagnostic evidence; **not** a newly executed audit, Git checkout, or approval to launch a large computation.

> **Reading instruction:** Sections 1–9 deliberately describe where the project stood **before the Windows Sandbox diversion**. Appendix A onward records the Sandbox experiment, including what was tried, what succeeded, what failed, and the research findings available on 2026-11-07. Do not mistake the blocked Sandbox test for a failure of the established native-Windows, billion-digit production files.

## 1. Project identity, scope and division of work

- GitHub repository: `https://github.com/hydra3333/analysing_perceived_randomness_in_reality`.
- OUTLANDISH source directory **now**: `GAIS/OUTLANDISH_01/` at repository root, not the former `src/GAIS/OUTLANDISH_01/`.
- Primary host: Windows 11; Ryzen 9 3900X (12 physical / 24 logical processors), 32 GiB RAM. Repository and main project virtual environment live on E:; large digit data and OUTLANDISH run artifacts live on G:; T: is a separate WD Black HDD with substantial space, reserved for possible WSL/Sandbox trials.
- OUTLANDISH_01 is an **independent, speculative mathematical-constant digit-stream thought experiment**. It is not the governed E_1..E_62 main predictive-randomness method suite, and it does **not** demonstrate lottery predictability. It nonetheless preserves the independent pre-holdout dataset and does not inspect held-out outcomes in development.
- The owner has authorised direct development/testing of this standalone OUTLANDISH workstream; do **not** infer authority to change the main research project's methods, orchestration, scientific gates, or held-out data.
- The owner strongly prefers pragmatic, reviewable implementations, precise claims, no fabricated runtimes or verification, and command-line procedures appropriate to Windows CMD. Code/diagnostic changes should be isolated and should not unnecessarily proliferate administrative machinery.

## 2. Established pre-Sandbox implementation: what is already in place

### 2.1 Main files and roles

Located under `GAIS/OUTLANDISH_01/` unless stated otherwise:

| File | Role |
|---|---|
| `outlandish_big_constants.py` | Native-Windows y-cruncher launcher, digit conversion, verification and registered `pipeline`; supports previews and explicit `--run`. |
| `outlandish_artifacts.py` | Shared artifact paths, pre/postflight safeguards, active-digit registry, verification, promotion, locking, retirement and recovery. Installed version reported as **v0.2r4**. |
| `outlandish_config.py` | TOML parsing / configuration helpers. |
| `outlandish_powerball_stage_a.py` | Fixed-width, NumPy-vectorised digit scanning and reports for the Powerball historical pre-holdout dataset. |
| `test_outlandish_v02.py` | Standalone regression tests and synthetic safety cases. |
| `outlandish.local.toml` | **Intentionally Git-tracked** local configuration **and machine-maintained active-digit registry**. User section may be edited deliberately; generated state must not be hand-edited. |
| `POWERBALL_preholdout_only.csv` | Pre-holdout-only development data; not a live-results fetcher. |
| `OUTLANDISH_01_v0_2_README.md`, `README.md` | Operational reference; inspect the installed version before relying on old handover excerpts. |
| `generate_1e10.cmd`, `scan_1e9.cmd`, `scan_1e10.cmd` | Convenience launchers; check their current contents and preview semantics before running. |
| `y-cruncher v0.8.7.9547b/` | Local Windows y-cruncher installation, **ignored by Git**. Contains binaries/libraries. |
| `ycruncher_digits/` | Legacy local folder; ignored, not the active large-artifact root. |

The historical standalone handover spec, old v0.1/v0.2 installers and earlier 10^10 README versions are **not** superior to the installed v0.2r4 code, TOML and README. Some older text predates G: relocation, automatic retirement, and the new GAIS root path.

### 2.2 Six constant streams and encoding

| CLI ID | Constant | First digits (decimal point shown for explanation only) |
|---|---|---|
| `pi` | π | `3.1415926535...` |
| `phi` | Golden ratio | `1.6180339887...` |
| `e` | e | `2.7182818284...` |
| `log2` | ln 2 | `0.6931471805...` |
| `gamma` | Euler–Mascheroni γ | `0.5772156649...` |
| `lemniscate` | **Half-perimeter** lemniscate constant | `2.6220575542...` |

Each output file contains **one numeric byte 0–9 per decimal digit** (NOT ASCII `'0'`–`'9'`), beginning with the integer digit and containing **no decimal point**. Thus a `10^9` file has exactly 1,000,000,000 bytes; a `10^10` file will have 10,000,000,000 bytes.

**Lemniscate convention matters:** the y-cruncher built-in source returns approximately `5.244115...` (full perimeter). The OUTLANDISH Python converter applies an exact streaming division by 2 to obtain the chosen `2.622057...` stream before verification and registration. Do not silently change this convention.

### 2.3 Existing large-file state, G:

The owner reported that **all six** constants had successfully completed native-Windows RAM-only pipelines to **10^9 digits each** by the end of 2026-11-06. The six 1,000,000,000-byte binaries were verified and registered active; no pending retirements remained at that checkpoint. This is **owner-reported and previously checked in conversation**, not freshly revalidated by this handover.

Established live artifact parent:

```text
G:\OUTLANDISH_01\large_artifacts\
    digits\       six registered, verified 10^9 numeric-byte binaries
    scratch\      calculation attempts, retained small reports
    staging\      in-progress candidates
    results\      scanner reports
    logs\         receipts and diagnostics
```

Important controls:

- Read the current `outlandish.local.toml` and run `python outlandish_artifacts.py status` / `audit` before new operations. Its `[state.active]` and `[state.pending_retirement]` are **program-generated; do not manually edit**. A `.toml.bak` is only the previous registry snapshot, **not** a backup of the big binaries.
- Live owner policy: `[settings.retention] delete_superseded = true`. In **v0.2r4**, after successful replacement validation and an atomic state publication, precisely the verified predecessor may be auto-retired. This is **not** an authorisation to manually delete files or bypass lock/identity checks. Third-party readers must be idle.
- Registered active files must be strictly extended; a second same-length `pipeline` is not an appropriate test. Full previous-prefix comparison is required for promotion. On handled failures, owned large scratch/intermediates are cleaned but small error evidence remains; crashes may leave recovery material.
- The output location and generated-large-file audits are important. The old project had an accidental history of large generated files under Git-tracked paths; that has been corrected. Large files should not be reintroduced into Git.
- The root `.gitignore` covers OUTLANDISH large artifacts and local y-cruncher, including `/GAIS/**/*.bin`, `/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/`, and `/GAIS/OUTLANDISH_01/ycruncher_digits/`. Confirm the latest ignored-root entry in the current repository if relevant.

### 2.4 Known native-Windows execution characteristics

- Installed y-cruncher version: `v0.8.7.9547b`.
- Owner observed actual **hard instantaneous power-offs** under some higher-concurrency y-cruncher settings. `-TD:4` was used for the established stable runs and is the cautious default for follow-up tests. **`-TD:4` sets y-cruncher's task decomposition, not a strict four-OS-thread/core cap**; observed CPU usage can exceed four cores. Do not raise it automatically or suggest stress tests to find a failure threshold.
- With `[settings.generator] mode = 'auto'`, the installed implementation selects RAM mode for inputs **below** 5 billion digits and disk-swap mode at/above that boundary. `[settings.generator] memory_gib` concerns requested working memory in swap mode, **not** a RAM cap for normal RAM-only calculations.
- The live `[settings.generator]` values must be read from current TOML; historical README examples vary (`threads = 4` and `threads = 12` both appear in different explanatory contexts). Do not infer current live settings from a README example.
- `ycruncher_verify_output = false` was selected in the newer pipeline for speed. Python format, reference-prefix and full SHA-256 checks remain, but **do not independently re-prove newly computed mathematical digits**. Preserve this limitation in scientific claims.
- Owner-supplied order-of-magnitude 10^9 generator observations: `phi` ~15 s y-cruncher; `e` ~44 s; `pi` ~71 s; `log2` ~180 s; `gamma` ~2,447 s (~41 min); lemniscate on the scale of minutes. These are individual observed runs, **not** credible extrapolations to 10^10/10^11 disk-backed computation.

### 2.5 Tests and evidence

Earlier native-Windows owner test run of `test_outlandish_v02.py`: **25 tests total**, 24 PASS and one allowed symlink skip. Separate generator/scanner self-tests existed. The full set of real 10^9 promotions was reported complete and the project committed/pushed; no 10^10 real run has been demonstrated.

`status` reflects registry metadata; `audit` checks path/placement/symlink/large-file safety. Neither substitutes for a **new** full-byte verification of every binary. Full-source digest verification happens in the relevant pipeline/whole-active-file scan paths.

## 3. Established Stage-A Powerball exploration

- Historical Powerball **pre-holdout only**: **433 draws, draw numbers 1144–1576**, cutoff exclusive `1577`. No later draws in development scans.
- Each selected ball is exactly two decimal digits (`03`, `12`, etc.). Search scans **every possible digit-byte offset**, including odd alignment and chunk boundaries.
- Pattern definitions:
  - **P1:** all seven main numbers in operator-drawn order, plus Powerball.
  - **P2:** all seven main numbers in operator-drawn order.
  - **P3:** any six distinct main numbers in any order, plus Powerball.
- A measured **π 10^9** run with `chunk_bytes = 4,000,000` took **27.278917 s** of scan time, yielding **P1=0, P2=0, P3=29**. This result is descriptive only, not evidence of causal structure or predictive power. A one-trillion-byte scan estimate based on it is merely a rough scan-only extrapolation, not a generation forecast.
- Scans use the OUTLANDISH-only historical CSV and do not pool games or consult future/holdout outcomes. The various other-constant scan statuses and report results should be read from the actual reports rather than assumed complete from the existence of six digit binaries.

## 4. Pre-Sandbox open problem: moving from 10^9 to 10^10 (possibly 10^11)

### 4.1 Windows y-cruncher disk-swap privilege obstacle

A 10^10 computation generally exceeds the comfortable 32 GiB RAM-only budget, making y-cruncher's **disk-backed swap mode** necessary. On native Windows, y-cruncher requested **`SeManageVolumePrivilege`** (“Perform volume maintenance tasks”) to use `SetFileValidData()` when preparing large swap files. A conventional non-elevated user did not have the needed privilege. The exact y-cruncher command / performance and safe swap-mode operation remain **untested for a substantive real 10^10 calculation**.

This privilege is security-sensitive and is **not restricted merely to T: or G:**. Do not casually grant it to the everyday user or change system policy. The owner considered a temporary grant/relogin/revoke sequence, but deferred it, preferring a potentially safer Linux route. No authorisation to alter this privilege has been given in this handover.

### 4.2 Research on replacement external-memory numerical engines

The owner sought a **mature, reusable** alternative capable of 10^10–10^11 digits, not a new numerical-HPC software project. Research included FLINT/Arb, python-flint, GMP, apfloat, TachusPI, binary splitting, external-memory FFT, and specialized constant algorithms. An external AI's initial report contained substantial errors and overconfident predictions; a requested correction concluded **NO-GO for a new independent engine**, **GO for further y-cruncher evaluation**. The corrected conclusion is a research judgment, **not** proof that no alternative can work. A function that streams a slice of output still may require enormous RAM to compute the preceding digits.

### 4.3 WSL2 Debian path — planned, not executed

Before diverting to Windows Sandbox, the preferred next *exploratory* route was the **Linux edition of y-cruncher under Debian/WSL2**, potentially avoiding Windows's `SetFileValidData()` requirement.

Known WSL host observations at that time:

```text
WSL version 2.5.7.0; kernel 6.6.87.1-1
Default WSL version: 2
No Linux distributions installed
```

The owner selected **Debian** rather than Ubuntu. Intended *host* area: `T:\OUTLANDISH_WSL\Debian\` holding the guest ext4 VHDX and Linux-side y-cruncher/swap scratch, without repartitioning or formatting T:. The six active result binaries remain on **G:**. Host T: was reported to have approximately **2.62 TB free** at the time; verify current free space before allocating anything.

Important planned controls:

- Complete the owner's **comprehensive backups and recovery-media checks** before Linux installation, privilege edits, disk-layout work, or heavy stress tests. The exact **current** backup completion status should be confirmed with owner; do not infer it from this handover.
- Before WSL installation set/inspect `.wslconfig` memory and WSL **VM swap-file location**, which otherwise may use C:. Beware of WSL virtual-disk max size and dynamic VHDX growth; verify current Microsoft guidance rather than assuming 2.62 TB is automatically addressable.
- Test Linux y-cruncher CLI and external-memory scratch on the ext4 filesystem. `/mnt/t` Windows/WSL cross-filesystem I/O is not equivalent to native ext4 random I/O and may be much slower. Preserve established converter, verification and registry contracts; a **new** Linux-runner integration is not installed.
- Start with a small Linux execution smoke test, then a calculation proven to exercise swap (small 10^5/10^6 calculations may not), then evaluate storage, speed and safety. No guessed runtimes for 10^10 or 10^11.
- `wsl --unregister Debian` would **delete** the Debian guest/data. Do not use casual cleanup commands against a live guest or running computation.

### 4.4 Remaining work (priority order as of pre-Sandbox checkpoint)

1. Protect the existing production source/TOML and six verified G: binaries; confirm backup/recovery readiness.
2. Establish a controlled, genuinely disk-backed y-cruncher execution mode (Debian/WSL2 was preferred; native Windows temporary privilege only with explicit owner decision; Windows Sandbox is an experimental diversion, not yet a working substitute).
3. Verify scratch/data placement, required temporary capacity, runtime characteristics, bounded concurrency, log evidence, and uninterrupted/restorable behaviour before long calculations.
4. Assess feasibility and resource budgeting **per constant**, particularly much slower `gamma`; don't jump directly to six 10^10 calculations or extrapolate RAM-mode timings.
5. Integrate, if necessary, a reviewed Linux / external-swap generation adapter feeding **the same numeric-byte, verified, registered files** on G:, with safe restart/cleanup semantics. Do not bypass the existing content and predecessor-prefix integrity checks.
6. Only then generate larger numbers and use the pre-holdout scanner; interpret matches with chance baselines and guard against exploratory overfitting.

## 5. Safe baseline commands on the original Windows project

These commands are for the original **native project** with its actual project-root `.venv` activated, executed from `GAIS\OUTLANDISH_01`. They are **not** an instruction to run now without reviewing state. Commands without `--run` do not start the real generator.

```bat
python outlandish_artifacts.py validate
python outlandish_artifacts.py paths
python outlandish_artifacts.py status
python outlandish_artifacts.py audit
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test
python test_outlandish_v02.py
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000
```

Do not issue the final command with `--run` until swap privilege/WSL adapter, storage, disk budget, safety and owner approval have been addressed. In particular, never run an unverified same-length `10^9` promotion against an already active 10^9 binary.

## 6. Repository and evidence boundary

The Git repository underwent a **completed** GAIS relocation and targeted history rewrite on 2026-11-06. Its authoritative record is under `exchange/HISTORY_CLEANUP_2026_11_06/` (including `CLOSEOUT.md` and `commit-map.txt`). Old references to `src/GAIS` and old pre-rewrite Git SHAs in earlier records are historical, **not** necessarily current locations or commit identities. Handover material from before v0.2r4 must not be read as the latest code state. The owner reported a committed, pushed clean state for OUTLANDISH after the six 10^9 files were established, but the new chat should inspect actual status rather than assuming today's working tree is unchanged.

---

# Appendix A — Windows Sandbox diversion: objective and file layout

**Scope:** separate experimental attempt to test the **Windows** y-cruncher/Python pipeline at **10^5 = 100,000 digits** inside a disposable Windows Sandbox, with source isolation and test-only storage on T:. This occurred **after** the pre-Sandbox production checkpoint above. It did **not** modify G: active binaries and never reached a successful digit calculation.

Host setup reported via `dir /b /s`:

```text
T:\OUTLANDISH_01_SANDBOX\
    [copied OUTLANDISH .py/.cmd/.csv/.md files]
    outlandish.local.toml             # production-registry COPY: preserve, do NOT use
    PYTHON\
        python-3.15.2-amd64.exe
        000-Pip-Install-Dependencies.bat
    SANDBOX\
        OUTLANDISH_01_sandbox.wsb
        OUTLANDISH_01_Setup.bat
        OUTLANDISH_01_Setup_manual_v3.bat
        OUTLANDISH_01_Sandbox_Explorer_Notepadpp.reg
        outlandish.sandbox.toml
        [helpers]
    y-cruncher v0.8.7.9547b\
        y-cruncher.exe; Binaries\; ...

T:\OUTLANDISH_01_SANDBOX_DATA\       # NEW, dedicated writable test-data tree
```

Sandbox `.wsb` maps (confirmed operational):

```text
C:\HOST_OUTLANDISH_SOURCE\    -> T:\OUTLANDISH_01_SANDBOX\       (read-only)
C:\HOST_OUTLANDISH_DATA\      -> T:\OUTLANDISH_01_SANDBOX_DATA\  (writable)
C:\HOST_SOFTWARE\             -> host C:\software\             (read-only; Notepad++)
```

Current `.wsb` also preserves the owner's selected vGPU/networking/printer/clipboard behaviour. When refining it, **inspect the actual file**; do not silently substitute another person's hardened/default option set.

Guest workspace:

```text
C:\OUTLANDISH_WORK\            # disposable cloned source + y-cruncher
    outlandish.local.toml         # separate clean 10^5 test registry
```

The test TOML uses:

```toml
[settings.storage]
main_root = 'C:\HOST_OUTLANDISH_DATA'
artifact_dir = 'large_artifacts'
digits_dir = 'digits'
scratch_dir = 'scratch'
staging_dir = 'staging'
results_dir = 'results'
logs_dir = 'logs'

[settings.generator]
threads = 4
mode = 'auto'
memory_gib = 1
ycruncher_verify_output = false

[settings.retention]
delete_superseded = false

[state.active]
[state.pending_retirement]
```

The guest's *clean* registry can be copied to `C:\HOST_OUTLANDISH_DATA\outlandish.local.toml` to survive session closure. The host's copied production registry at `C:\HOST_OUTLANDISH_SOURCE\outlandish.local.toml` must **never** be modified or confused with the clean test registry. T: test results and registry may persist via writable mapping; guest C: software, registry, desktop and Python disappear at closure.

# Appendix B — chronological Windows Sandbox findings

## B.1 First setup variants and shortcut failure

- The owner's original `.wsb` XML and initial BAT were generally viable but had to respect the new T: source/data isolation. Early replacements unintentionally removed the owner's original Explorer/Notepad++ configuration, nine registry customisations and desktop links. These were subsequently restored. **Do not regress them.**
- Initial automated Python setup was undesirably slow and produced no persistent startup log. The owner changed a copy to a manual BAT with diagnostic pauses.
- Original shortcut implementation emitted a `.vbs` and called `cscript.exe`; it failed with:

  ```text
  Input Error: There is no script engine for file extension ".vbs".
  ```

  The failure guard correctly stopped setup before Python/workspace creation.
- Replaced VBScript execution with PowerShell + COM `WScript.Shell.CreateShortcut`. Owner ran the command and observed **exit code 0** and three confirmed `.lnk` files on the guest desktop:

  ```text
  HOST_software.lnk
  HOST_OUTLANDISH_01.lnk
  HOST_OUTLANDISH_DATA.lnk
  ```

- Added missing **Explorer compact view** through:

  ```bat
  reg.exe add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v UseCompactMode /t REG_DWORD /d 1 /f
  ```

  The owner confirmed registry value `REG_DWORD 0x1`.
- Original Explorer `.reg` import returned success; that is **not** the same as an individual operational check of every Explorer preference or Notepad++ context-menu behaviour. Notepad++ points at `C:\HOST_SOFTWARE\NPP\notepad++.exe`.

## B.2 Current working no-Python startup: v3

The owner replaced both scripts from `OUTLANDISH_01_Sandbox_NoPythonInstall_v3.zip`:

- `OUTLANDISH_01_Setup.bat`: automatic start via existing `.wsb`; **no Python install, lookup or checks**; **no pauses**; logs to host-mounted `C:\HOST_OUTLANDISH_DATA\OUTLANDISH_01_setup_auto.log`; no calculation.
- `OUTLANDISH_01_Setup_manual_v3.bat`: same phases, with owner-requested pauses for diagnostics.
- Both have a separate explicit `DEPS` option intended for **after** Python is working; this invokes the owner's existing `PYTHON\000-Pip-Install-Dependencies.bat`, not a substituted NumPy-only dependency list. The source dependency BAT includes broad package updates and an invalid `python -m python -m pipdeptree` command; it may also mask intermediate errors. Do not assume the entire package list is installed from the presence of pip.
- Supporting files include `.wsb`, `.reg`, `outlandish.sandbox.toml`, `OUTLANDISH_01_Open_CMD.bat` and `RUN_PHI_100k_AND_SAVE_REGISTRY.bat` (not automatically executed).

**OWNER-CONFIRMED full automatic v3 setup output** on a fresh Sandbox:

```text
[1/5] Checking mapped folders and required source files...       PASS
[2/5] Applying Explorer and Notepad++ customisations...           PASS
    UseCompactMode REG_DWORD 0x1
[3/5] Creating three desktop shortcuts...                        PASS
    three expected .lnk files listed
[4/5] Preparing disposable OUTLANDISH workspace...               PASS
[5/5] Selecting sandbox-only TOML and copying helper BATs...      PASS
    Using the clean sandbox TOML template.
SETUP COMPLETE: Registry, compact view, desktop shortcuts, work tree.
Python is NOT installed, looked up, or checked by this setup.
No computation has been launched.
```

**Do not rewrite this v3 startup merely to fix Python.** It is the first confirmed functioning setup baseline. A future automated script should preserve log/error codes, the owner's full customisations, and no pauses on automatic failure; manual diagnostic script may retain pauses.

## B.3 Native installer attempts inside guest and transient Python success

Sandbox guest reported `Microsoft Windows [Version 10.0.26100.9818]` and account `WDAGUtilityAccount`. Source and test-data mappings appeared under guest C:.

- First script-driven silent installation of `python-3.15.2-amd64.exe` took unexpectedly long. At one stage `Ctrl+C` had no effect. A separate CMD listed two Python installer processes (PIDs 6972 and 7940) and a service-session `msiexec.exe` (PID 3584). The owner terminated **only** the Python installer process tree with:

  ```bat
  taskkill /F /T /IM python-3.15.2-amd64.exe
  ```

  Both Python installer processes terminated. `msiexec.exe` was left alone.
- Installer logs existed under guest `%TEMP%`, with stages visible between 09:51 and 09:59 (core, exe, dev, lib, Tcl/Tk), suggesting progression despite long pauses. They were **not** comprehensively inspected or copied out before restart.
- The owner later manually launched the GUI installer on a clean guest. Selected **Add python.exe to PATH**, Custom installation; unchecked **Documentation**, **Tcl/Tk, turtle and IDLE**, and **Python test suite**; left **Precompile standard library** unticked and remaining advanced options unchanged. The GUI still appeared slow and at one point appeared to install a test-suite component despite the selection; this observation is **not** independently confirmed by MSI logs.
- The installation eventually completed. The existing CMD needed an explicit PATH refresh. The working guest interpreter was:

  ```text
  C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python315\python.exe
  ```

- **OWNER-CONFIRMED transient success:** `python --version` returned `Python 3.15.2`, and `python -m pip --version` returned `pip 26.2.2`. PATH was corrected for the running CMD via:

  ```bat
  set "PATH=%LOCALAPPDATA%\Programs\Python\Python315;%LOCALAPPDATA%\Programs\Python\Python315\Scripts;%PATH%"
  ```

  `where python` and `where pip` both resolved to this same Python installation. The working `python.exe` was previously shown as **105,696 bytes**.

## B.4 pip errors, then zero-byte Python executable

Running the **owner's original** dependency BAT from `C:\OUTLANDISH_WORK` produced:

```text
pip uninstall ... pyinstaller ...
Fatal error in launcher: Unable to create process using
  '"C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python315\python.exe" ...\Scripts\pip.exe ...'

python -m pip install ... pip
Access is denied.
python -m pip install ... tzdata / tzlocal / pytz / numpy ...
Access is denied.
```

A prominent blue Windows **“This app cannot run on your PC”** dialog appeared. The BAT continued through multiple failures; repeated Ctrl+C attempts were needed. Afterwards, even the **full path** `python.exe --version` triggered the blue dialog. This conclusively disproved the earlier hypothesis that PATH was the only remaining problem.

Next owner diagnostics:

```text
C:\OUTLANDISH_WORK>dir "%LOCALAPPDATA%\Programs\Python\Python315\python.exe"
07/11/2026  10:36 AM                 0 python.exe

C:\OUTLANDISH_WORK>certutil -hashfile "%LOCALAPPDATA%\Programs\Python\Python315\python.exe" SHA256
CertUtil: -hashfile command FAILED: 0x800703ee (WIN32: 1006 ERROR_FILE_INVALID)
CertUtil: The volume for a file has been externally altered so that the opened file is no longer valid.
```

**Confirmed:** previously working installed `python.exe` was subsequently **0 bytes and invalid**. **Not established:** which process changed it, whether the actual filesystem content was truncated by an interrupted MSI, a Sandbox overlay/VHD problem, a filter/AV operation, or another mechanism. The pip BAT should not ordinarily zero the interpreter; the temporal association is not a root-cause diagnosis. It is **not** evidence that G: or T: was corrupted; the invalid executable resided on **guest disposable C:**.

## B.5 Security and System event queries: what they do *not* prove

Owner ran:

```bat
wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /q:"*[System[(EventID=1116 or EventID=1117)]]" /c:10 /rd:true /f:text
wevtutil qe System /q:"*[System[(EventID=55 or EventID=98 or EventID=153 or EventID=7)]]" /c:10 /rd:true /f:text
```

- **No matching Windows Defender 1116/1117 detection/remediation events appeared.** This does **not** exclude all security/policy/AV interventions.
- System query returned repeated event **55** records from provider **`Microsoft-Windows-Kernel-Processor-Power`**, describing CPU idle/power capabilities. These were **not** disk/NTFS fault events. Event-ID-only queries across providers can be misleading; filter by provider as well if investigating filesystem events.
- No Code Integrity query result was supplied after the final corruption. Do **not** claim it was checked or cleared.

**Where the diversion stops:** no successful Windows Sandbox 10^5 generator run, no pip dependency setup, and no validated disk-swap test. The baseline v3 startup succeeded, but Python/pip failed during the manual test. Preserve the source code and production six 10^9 G: files unaffected.

---

# Appendix C — researched Windows Sandbox issues and T: persistence option

## C.1 Research findings and confidence

1. **High-confidence explanation for unusually slow MSI installations in Windows Sandbox:** Microsoft-maintained `microsoft/Windows-Sandbox` issue [#85](https://github.com/microsoft/Windows-Sandbox/issues/85) documents the slowdown on Windows 11 24H2/25H2. A Microsoft contributor explained that WinTrust package verification was querying a disabled Defender service while Smart App Control was enabled, leading to retries; reports include repeated ~2-minute delays per MSI. Other users observed Python installs taking >30 minutes [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/3898205/the-setup-process-performance-inside-windows-sandb). The issue discussion records mixed reports even after purported 26H2 fixes. This strongly fits the owner's **slowness**, but it does **not** independently prove the exact installed-policy state of the owner's guest.
2. **Confirmed error meaning, not root cause:** Microsoft [Win32 error definitions](https://learn.microsoft.com/openspecs/windows_protocols/ms-erref/18d8fbe8-a967-4f1c-ae50-99ca8e491d2d) define `ERROR_FILE_INVALID` (1006 / `0x800703EE`) as *“The volume for a file has been externally altered so that the opened file is no longer valid.”* Its occurrence on the guest C: executable does not establish a host physical-disk fault or a specific cause of truncation.
3. **No trustworthy exact-match causal precedent found** establishing that this particular Sandbox slow-MSI issue zeroes an installed Python interpreter. Keep these as **two observations with a possible, unconfirmed connection**. Do not treat unrelated 0-byte WindowsApps Python aliases or past Group Policy file-copy defects as proof for this case.
4. **Windows Sandbox is disposable:** Microsoft [FAQ](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-faq) says guest state disappears on close. [Mapped folders documentation](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file) says a writable mapped directory can persist changes on the host. Hence persistent Python on T: is conceivable, **not yet validated**.
5. Some forum discussions recommend disabling Smart App Control policy **inside the guest** to speed MSI. **Do not apply this by default or change host security policy.** It is a security control change, not a verified remedy for zero-byte `python.exe`; require a separate conscious owner choice after backups and diagnosis.
6. Python 3.15 [Windows full-installer documentation](https://docs.python.org/3/using/windows.html#the-full-installer-deprecated) documents switches including `Include_doc`, `Include_tcltk`, `Include_test`, `CompileAll`, `PrependPath`, `TargetDir`, etc. The classic full installer is deprecated but still available for 3.15. The exact future switches can reproduce the owner's GUI selections if the owner elects scripted installation; do not invent unsupported flags.

## C.2 Could installing once to T: avoid the problem?

**Potentially yes for repeat-installation overhead; not proven as a fix for executable corruption.** The safer design hypothesis is:

```text
HOST ONLY, separate from live OUTLANDISH and other software:
T:\OUTLANDISH_01_SANDBOX_PYTHON_CANDIDATE\
    Python315\...               # prospective persistent interpreter + site-packages
    logs\...                    # install/output/verification receipts

GUEST (new mapped path, exact spelling identical every session):
C:\HOST_OUTLANDISH_PYTHON\     # writable mapping only during construction
```

Do **not** directly install/upgrade into a known-good persistent Python tree and risk destroying it. Build a separately named candidate, verify it, snapshot or copy it **read-only**, and only then consider reuse. A stable guest-mounted path is important because Windows `pip.exe` console entry-point launchers and some packages contain absolute interpreter paths; changing mount location between sessions can break them. Merely copying a registered Python installation does **not** reproduce its original HKCU/HKLM registry state, PATH, launcher or app associations; some features may need reinitialisation. Native extension modules (NumPy/SciPy) must be tested in a fresh sandbox. A mapped host path may have different execution, locking, ACL and performance behaviour from guest C:; **run actual tests before promising portability or speed**.

Additional safety trade-off: mapping persistent Python **writable** exposes host T: files to the sandbox software. After verification, map it **read-only** for ordinary computations when possible, and keep writable result/scratch areas separate. However pip updates cannot modify a read-only environment. Test whether the interpreter works at all from the read-only mapping before adopting that design.

**Recommended incremental investigation, only when owner wants it:**

1. Finish/confirm external backups and ensure the T: candidate directory is not part of the real verified digit registry.
2. Start a clean Windows Sandbox with known-good v3 startup. Do not change G: or the source-mapped production TOML.
3. Test the Python installer **without pip upgrades**, with official owner-selected options (include pip; exclude documentation, Tcl/Tk/IDLE, test suite; no standard-library precompilation). Capture `%TEMP%\Python*log` to the writable mapped T: diagnostic directory **before closing guest**. Compare installer logs with the known repeated MSI trust-policy delays.
4. If the guest C: installation works, record `python.exe` file size/SHA-256 **before and after** each small read-only action (`--version`, `-c`, `-m pip --version`, `-m pip list`), then after a narrowly scoped package install. This isolates the first destructive transition; avoid the original BAT's `pip-review --auto` and wholesale upgrades during diagnosis. Keep the owner's BAT unmodified as evidence.
5. Only after understanding the zero-byte failure, test a fresh persistent T: Python candidate in a newly mapped path, record its file size/hash, test direct `python.exe`, `-m pip`, small package install, and NumPy/SciPy import. Shut down/reopen sandbox, then verify stability and package availability before putting it into the main startup path.
6. Record both **guest C:** and **T: persistent** run results; do not infer that a passing 10^5 RAM-mode run proves Windows disk-swap privilege, large-data performance or safety for 10^10.
7. If errors remain reproducible, collect complete Python/MSI logs and provider-filtered events. The official Windows Sandbox [GitHub bug tracker](https://github.com/microsoft/Windows-Sandbox/issues) and [Microsoft's reporting guidance](https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-faq) are appropriate places to compare/report diagnostics.

## C.3 Next safe actions for the receiving chat

- **First** read this handover and the current `GAIS/OUTLANDISH_01/README.md`, `OUTLANDISH_01_v0_2_README.md`, Python files, live TOML and existing stored diagnostics. Identify exact current files and do not infer that older versioned ZIPs are installed.
- **Ask for no more than is necessary.** If the owner is continuing Sandbox debugging, the next evidence is the preserved installer/guest logs (if captured), the current Python executable size/hash and one controlled reproduction. If the owner elects T: persistence, plan a **separate test directory** and mapping, not a risky live overwrite.
- Do not change the working v3 setup's registry/desktop customisations. Automatic startup **never pauses**; the separate manual BAT may contain pauses. The owner wants the **original full dependency BAT**, not an unrequested substitute package list.
- Preserve `-TD:4` as the cautious owner-tested setting; it is *not* a thread affinity cap.
- If the owner returns to Debian/WSL2, treat that as the **pre-Sandbox preferred** large-run route and independently verify contemporary commands and storage controls before installation.
- Maintain a clean distinction between **(a) confirmed working native 10^9 project**, **(b) blocked Windows Sandbox 10^5 trial**, and **(c) unimplemented Debian/WSL2 10^10 path**.

---

## Sources and interpretation notes

**Owner evidence:** command outputs and observations supplied in the ChatGPT conversation through 2026-11-07, including Sandbox setup stage PASS, successful transient Python 3.15.2/pip 26.2.2, 0-byte `python.exe`, `certutil 0x800703EE`, and Event Viewer queries. Prior owner-reported six-constant 10^9 status and scan timings were retained from project discussion. The current handover does **not** reproduce checks on the owner's host.

**Local supporting package files reviewed in preparation:** prior staged `OUTLANDISH_01_v0_2r4_Auto_Retire/README.md`; `OUTLANDISH_01_Sandbox_NoPythonInstall_v3/OUTLANDISH_01_Setup.bat`, `.wsb`, TOML and README; owner's uploaded dependency BAT; prior GAIS relocation/handover notes. The existence of local archived copies does not prove their byte identity with the owner's latest checked-out repository.

**External sources (researched 2026-11-07):**

- Microsoft Windows Sandbox issue #85 (slow MSI, technical cause and patch discussion): https://github.com/microsoft/Windows-Sandbox/issues/85
- Microsoft Windows Sandbox issue #68 (longstanding slow install reports, mixed update outcomes): https://github.com/microsoft/Windows-Sandbox/issues/68
- Microsoft Q&A, very slow Python installation in Sandbox: https://learn.microsoft.com/en-us/answers/questions/3898205/the-setup-process-performance-inside-windows-sandb
- Microsoft Windows Sandbox configuration and writable mappings: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file
- Microsoft Windows Sandbox FAQ: https://learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-faq
- Microsoft ERROR_FILE_INVALID definition: https://learn.microsoft.com/openspecs/windows_protocols/ms-erref/18d8fbe8-a967-4f1c-ae50-99ca8e491d2d
- Python 3.15 Windows installer documentation: https://docs.python.org/3/using/windows.html

**End of handover.**
