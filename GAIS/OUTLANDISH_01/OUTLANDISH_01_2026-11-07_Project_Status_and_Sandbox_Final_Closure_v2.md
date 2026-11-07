# OUTLANDISH_01 — Current Project Status, Windows Sandbox Closeout, and Next-Stage Handover

**Date:** 2026-11-07 (Australia/Adelaide)  
**Version:** v2 — consolidated handover, supersedes the 7 November v1 *as a conversation handover*  
**Revision scope:** Full Windows Sandbox closeout, persistent T: Python observations, final `0xC000007B` y-cruncher launch failure, document-name clarification, and Debian/WSL2 next steps.  
**Audience:** A new ChatGPT conversation continuing the owner's standalone OUTLANDISH_01 experiment  
**Status:** Windows Sandbox investigation **closed as an unsuccessful execution route**; native Windows six-constant 10^9 baseline retained; Debian/WSL2 on T: is the next planned route, **not yet installed or tested**. This document is a state handover, **not** a fresh Git checkout, audit, or authorization to launch large calculations.

> **Reading instruction:** Sections 1–6 preserve the **pre-Sandbox established scientific/software baseline**; Section 7 records the **latest decision and outstanding work**. Appendices A–D capture the now-abandoned Windows Sandbox trial and its evidence. Do not mistake the Sandbox launch failure for a failure of the working native-Windows billion-digit project. Installed source code, current TOML and actual receipts remain authoritative for operational behavior.


## Executive status at handover (7 November 2026)

| Area | Confirmed/reported status | Important qualification |
|---|---|---|
| Native-Windows OUTLANDISH | Six separate mathematical-constant **10^9-digit** binaries reported verified and active on G: | Owner report from 6 November; not reread or rehashed during this handover |
| Scanner | Pre-holdout Powerball Stage A implementation and 433-draw development CSV in place; P1/P2/P3 tests and measured pi 10^9 scan | No evidence of predictive value; no holdout use authorized |
| Generator | v0.2r3 pipeline and v0.2r4 artifact management; y-cruncher 0.8.7.9547b, safe handling and preview | Normal RAM-only native calculations worked; large disk-backed mode unproven |
| Windows Sandbox | **Closed / unsuitable for this project after extensive trial** | Tests, registry, dry-run and persistent Python worked, but Windows y-cruncher never launched successfully |
| Small 100,000-digit Sandbox calculation | **NOT completed** | y-cruncher returned `3221225595` unsigned / `-1073741701` signed = `0xC000007B` in ~0.1 s |
| 10^10 digit generation | **NOT started or demonstrated** | Original obstacle: native Windows y-cruncher swap privilege; next plan Debian/WSL2 |
| VM/platform decision | No further Windows Sandbox or VMware/standalone Hyper-V VM efforts | WSL2 *does* rely on Windows virtualization infrastructure; the owner distinguishes it from setting up a general-purpose VM/hypervisor environment |
| Fallback | Temporary `SeManageVolumePrivilege` grant on native Windows, **only if WSL2 fails** | Owner accepts route in principle; do not alter rights or security policy without explicit implementation decision and backup confirmation |

**Immediate instruction for a new chat:** Read this document, then inspect the actually installed `GAIS/OUTLANDISH_01` code/README/TOML before preparing **Debian/WSL2 on T:**. Do not revive Windows Sandbox or start `10^10` work automatically. Begin with storage/backup/configuration checks, then minimal Debian and Linux y-cruncher launch tests.

---

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

### 4.4 Remaining work (historical pre-Sandbox list; updated current plan in §7)

1. Protect the existing production source/TOML and six verified G: binaries; confirm backup/recovery readiness.
2. Establish a controlled, genuinely disk-backed y-cruncher execution mode (Debian/WSL2 was preferred; native Windows temporary privilege only with explicit owner decision; Windows Sandbox has now been abandoned as an unsuccessful test environment).
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


## 7. Current decision and work remaining after Sandbox closeout

**Decisions on 7 November 2026:** The owner is deleting the temporary Windows Sandbox experiment trees from T: and their redundant source-copy folder on E:. This cleanup is **owner-reported/intended; not independently checked complete**. Do not delete any original source, registered G: binaries, production TOML or historical source/evidence documents. Windows Sandbox is not to be debugged further; creating another persistent Python/Build Tools Sandbox is not a prerequisite for the next stage. The owner also declines VMware's Broadcom download/account hurdles and does not want to set up a separate Hyper-V VM simply for this experiment.

**Next preferred approach:** Debian under WSL2, with the Debian installation and Linux y-cruncher scratch **on T:**, **no T: repartitioning**, and verified final output on **G:**. WSL2 was present but had no installed Linux distribution at the earlier checkpoint. Planned guest location was `T:\OUTLANDISH_WSL\Debian\` with underlying guest ext4 VHDX (size/layout to be verified). The guest should be minimal; do not repeat the mistake of installing large unrelated Python development toolchains before a Linux y-cruncher smoke test.

**Practical continuation gates:**

1. **Read/confirm latest source and backups.** Verify that backups and recovery media are complete and available; inspect actual E: repo status, registry and G: artifacts. Do not assume T: cleanup or backup completion was successful from this text.
2. **Check WSL2 and host storage.** Inspect `wsl --version`, `wsl --status`, `wsl --list --verbose`, T:/G: free space, and existing `%USERPROFILE%\.wslconfig` before touching Windows configuration. Control WSL VM RAM, CPU and *VM* `swapFile` placement (which may otherwise use C:). Also understand separate **y-cruncher computation swap scratch** in the Linux ext4 guest.
3. **Confirm supported Debian installation syntax and storage semantics against current primary documentation.** The earlier candidate was `wsl --install --distribution Debian --location T:\OUTLANDISH_WSL\Debian`, but verify it for the installed WSL version rather than assume. Do not partition or format T:. A distro VHDX is dynamically allocated and may have virtual-size limits.
4. **Minimal Linux y-cruncher smoke.** Download/check official Linux y-cruncher for the actual guest CPU/architecture. First demonstrate executable startup and a small, independently verified constant; **do not** install six constants, all Python packages, or a full compiler toolchain just to launch it.
5. **Real out-of-core trial.** Test a calculation that actually uses disk-backed arithmetic on the guest ext4 filesystem with measured space, memory, I/O, logging and exit behavior. A `10^5` or `10^6` digit computation with 1 GiB memory will probably not exercise external swap. Start smaller than `10^10` but meaningfully out of core; choose parameters from observed usage rather than speculation.
6. **Interface/portability.** If Linux y-cruncher succeeds, plan and independently test a minimal adapter/converter to the already-defined byte-digit + full prefix/registry contract. Linux output may be transferred sequentially to a Windows G: staging area for **Windows Python** verification/registration. Do not move production G: data into the WSL guest or silently alter canonical digit semantics.
7. **Then review one real `10^10` attempt**, with an explicit disk/CPU/duration budget and bounded task decomposition. Start with an easier constant, not all six concurrently; `gamma` had a much longer 10^9 runtime than phi. Preserve failure evidence and avoid premature deletion.
8. **Conditional native Windows fallback:** If Debian/WSL2 fails materially, the owner is prepared *in principle* to temporarily grant `SeManageVolumePrivilege` to the ordinary Windows account, make an explicit test, then revoke it and restart/re-login to ensure removal. This is a system-wide, sensitive user right, **not a per-drive permission**, and must receive a specific owner go-ahead at implementation time. Do not run an elevated y-cruncher or casually modify local policy.

**Safety:** Prior actual host hard power-offs occurred with higher y-cruncher concurrency. Stay with previously tolerated `-TD:4` task decomposition unless there is an explicit new decision. This flag is **not** a four-core OS affinity limit. WSL's virtual CPU/memory settings may additionally need control; avoid stressing the host or exposing the six G: files to unverified code.

---


# Appendix A — Completed Windows Sandbox experiment: configuration and scope

**Purpose:** Test the Windows y-cruncher/OUTLANDISH pipeline on `10^5 = 100,000` golden-ratio digits in an isolated disposable Windows Sandbox, with copied source on T: and scratch/results under a separate T: data tree. Goal was to avoid native Windows's disk-swap privilege at larger sizes. **Outcome: the real test never computed digits; Windows y-cruncher failed at process load time.** This appendix is forensic/historical. Its T: files were being deleted at owner's decision and should not be presumed available.

## A.1 Snapshot of host-to-guest setup (historical, not to recreate by default)

```text
HOST (T:)
T:\OUTLANDISH_01_SANDBOX\                 copied stand-alone source, local y-cruncher, PYTHON/, SANDBOX/
  PYTHON\python-3.15.2-amd64.exe         installer
  PYTHON\000-Pip-Install-Dependencies.bat   owner's full dependency BAT (v5 later edited for compiler)
  SANDBOX\OUTLANDISH_01_sandbox.wsb
  SANDBOX\OUTLANDISH_01_Setup.bat
  SANDBOX\OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat
  SANDBOX\OUTLANDISH_01_Python_Env.bat
T:\OUTLANDISH_01_SANDBOX_DATA\            writable test-data tree
  python_candidate\Python315\          installed Python and pip; persisted between guest restarts
  outlandish_run\large_artifacts\     separate scientific data root

GUEST
C:\HOST_OUTLANDISH_SOURCE\          read-only mapping of first T: tree
C:\HOST_OUTLANDISH_DATA\            writable mapping of second T: tree
C:\HOST_SOFTWARE\                  read-only host software/Notepad++ mapping
C:\OUTLANDISH_WORK\                disposable cloned source, y-cruncher, test TOML
```

The .wsb mapped folders correctly. GUI and user preferences were re-applied by startup, while the guest C: filesystem, Windows registry and installed system toolchains were discarded on closing Sandbox. The host-mapped T: data retained any changes made there, including pip updates and installed binaries. **Never confuse this with isolation from the host writable folder.**

The owner originally had nine Explorer registry preferences, a Notepad++ context-menu integration and desktop shortcuts; early assistant setup packages inadvertently removed them, then restored them. Explorer **compact view** (`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\UseCompactMode = 1`) was explicitly added. Three shortcuts were verified:

```text
HOST_software.lnk
HOST_OUTLANDISH_01.lnk
HOST_OUTLANDISH_DATA.lnk
```

The first `.bat` used VBScript through `cscript` and failed because the guest lacked a `.vbs` script engine; PowerShell with `WScript.Shell` COM `CreateShortcut` succeeded. A subsequent automatic setup with **no pauses**, logging and no Python install passed all five startup stages. Manual scripts were separate and allowed diagnostic pauses. **No files or settings in the T: Sandbox test should be installed into E: production.**

## A.2 Python on ephemeral C: — extremely slow and ultimately invalid

A Windows Sandbox guest ran Python installer `python-3.15.2-amd64.exe` (owner-selected **per-user** standard location, PATH on, without documentation, Tcl/Tk/IDLE, Python test suite or standard-library precompilation). The installer took an unusually long time. The initially successful test reported:

```text
C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python315\python.exe
size: 105,696 bytes
Python 3.15.2
pip 26.2.2
```

Existing CMD didn't pick up new PATH until the owner explicitly added Python315 and `Scripts` directories. The original full pip BAT later produced Windows's blue **"This app cannot run on your PC"** popup, pip launcher failure and `Access is denied`. At 10:36 local, `dir` reported **`python.exe` = 0 bytes**. `certutil -hashfile` failed with `0x800703EE` / Win32 1006 `ERROR_FILE_INVALID` (*"volume ... externally altered ... opened file ... no longer valid"*). This proves an invalid executable, **not its cause**. The exact process that truncated or invalidated the file was never identified. Do **not** infer host T:/G: corruption from it.

System event query for IDs 55/98/153/7 returned `Microsoft-Windows-Kernel-Processor-Power` Event 55 (**informational CPU power-management capability**), not NTFS disk corruption. Defender Operational queries for events 1116/1117 returned no output; no Code Integrity enforcement event was established. An empty or broad event query cannot prove the absence of relevant security or volume events.

## A.3 Persistent Python on T: — demonstrated feasible

A later candidate used Windows Python installer's documented `TargetDir` to install once under:

```text
C:\HOST_OUTLANDISH_DATA\python_candidate\Python315
(Host: T:\OUTLANDISH_01_SANDBOX_DATA\python_candidate\Python315)
```

Python installation returned **exit code 0** with the owner's requested exclusions. Direct startup and `-m pip` worked; its `sys.prefix` and `pip` `Lib\site-packages` both resolved within the T: mapped tree. A baseline SHA-256 was saved. A fresh Sandbox restart **independently passed** the provided `VERIFY` phase. Another restart after substantial dependency updates also passed:

```text
Python 3.15.2
pip 26.3
sys.prefix = C:\HOST_OUTLANDISH_DATA\python_candidate\Python315
site-packages = C:\HOST_OUTLANDISH_DATA\python_candidate\Python315\Lib\site-packages
```

`numpy` imported successfully at version **2.5.4**, and owner reports also confirmed Scipy/pandas imports in dependency checks. This is a *real positive result*: a Python installation and packages **can** remain usable across Windows Sandbox restarts when the guest mapping path is stable. The path used for temporary downloads/builds was under `%TEMP%` (disposable C:), which does **not** mean pip's final installation went there. This positive result **did not fix the y-cruncher launch failure** and is not a recommendation to retain Sandbox.

## A.4 Full owner dependency BAT: not required for OUTLANDISH smoke; compiler failure

The owner's original `PYTHON\000-Pip-Install-Dependencies.bat` requested many upgrades, `--upgrade-strategy eager`, `pip-review --auto`, and packages not used by OUTLANDISH. It also contained a bad `python -m python -m pipdeptree` command, which a later draft proposed correcting. The owner expressly wanted the original package list preserved; early assistant NumPy-only substitutions were rejected. One replacement v5 included compiler installation/prerequisites and fail-fast pip error tracking, but this was a Sandbox-only candidate, **not** part of the main project requirements.

A supplied pip log of 1,605 lines showed **six build failures for five distinct packages**:

| Package | Attempts failed | Interpretation |
|---|---:|---|
| PyYAML | 2 | Compiled extension build attempted; missing MSVC toolchain |
| inflate64 | 1 | Compiled archive dependency; missing compiler |
| pybcj | 1 | Compiled archive dependency; missing compiler |
| pyppmd | 1 | Compiled archive dependency; missing compiler |
| pyahocorasick | 1 | Compiled pattern-matching extension; missing compiler |

Representative error:

```text
error: Microsoft Visual C++ 14.0 or greater is required.
Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**This is not a VC++ Redistributable runtime failure.** These packages fell back to compiling from source on Python 3.15 because suitable wheels were unavailable/unsuitable at the time. Many other packages, including NumPy 2.5.4, SciPy and pandas, were usable. OUTLANDISH's scanner uses NumPy; generation is primarily standard-library Python plus external y-cruncher. The five failed packages were **not a demonstrated prerequisite** of the `10^5` OUTLANDISH test.

Attempted Build Tools installer (`vs_BuildTools.exe`) ran the Visual Studio Installer on Sandbox disposable C: and made very slow progress, **stalled at 35% / package 149 of 268**, and was abandoned by closing the entire Sandbox. That is an **abandoned incomplete install**, not proof that Microsoft's toolchain would never install. No completed compiler toolchain survived the guest restart. The owner decided not to spend further effort on full dependency/toolchain installation.

## A.5 OUTLANDISH smoke tests: 25 tests individually accounted for

After the successful persistent Python setup and source copy, the complete Python suite ran:

```text
Ran 25 tests in 51.830s
24 passed ('ok'), 1 ERROR: test_all_launchers_use_manifest_not_hardcoded_drive
FileNotFoundError: C:\OUTLANDISH_WORK\scan_1e9.cmd
```

The failure was **packaging**, not computation: the startup copy routine omitted the three launcher `.cmd` files. The owner copied `scan_1e9.cmd`, `scan_1e10.cmd`, `generate_1e10.cmd` from read-only source to C: worktree and reran the one failing test:

```text
Ran 1 test in 0.013s
OK
```

Therefore **each of the 25 tests passed in aggregate**, but a full 25-test run was **not repeated after copying**. Do not misreport a single clean 25/25 suite execution. The full suite was slow (~52 s) in the mapped persistent Python environment; this does not directly measure numeric calculation performance.

## A.6 Artifact audit and correct test data root

The original clean test TOML had:

```toml
[settings.storage]
main_root = 'C:\HOST_OUTLANDISH_DATA'
```

OUTLANDISH's audit correctly identified **eight unsafe misplaced entries** within `python_candidate`, including large NumPy/SciPy DLLs (`~20 MB`) and `chardet` `.bin` model files. The audit was working as specified; the configuration wrongly placed **all persistent Python files beneath a scientific-artifact-scanned root**. Nothing was deleted and audit rules were not bypassed.

The owner fixed only the test TOML and created a separate root:

```toml
[settings.storage]
main_root = 'C:\HOST_OUTLANDISH_DATA\outlandish_run'
```

```text
T:\OUTLANDISH_01_SANDBOX_DATA\
   python_candidate\Python315\        (outside the audit root)
   outlandish_run\large_artifacts\    (scientific-only subtree)
```

Then:

```text
ARTIFACT AUDIT PASS (standalone audit): no misplaced generated/large files
CONFIG C:\OUTLANDISH_WORK\outlandish.local.toml root=C:\HOST_OUTLANDISH_DATA\outlandish_run
pi/phi/e/log2/gamma/lemniscate: active=NONE pending_retire=NONE
```

The generator's `phi --digits 100000` **dry run passed**, reporting the exact CLI and `-TD:4`:

```text
[phi] TARGET: 100,000 digits INCLUDING integer digit.
[phi] MODE=RAM THREADS_REQUESTED=4 (TD task decomposition, not strict OS thread count)
[phi] COMMAND: "C:\OUTLANDISH_WORK\y-cruncher v0.8.7.9547b\y-cruncher.exe" custom goldenratio -dec:99999 -hex:0 -od:1 -compress:0 -verify:0 -mode:ram -TD:4 -PF:taskqueue
[phi] DRY RUN: nothing launched or modified.
ARTIFACT AUDIT PASS (post-run): no misplaced generated/large files
```

The `-dec:99999` argument yields exactly **100,000 digits including the integer digit**. This was a correct preview and does **not** mean the actual digit output existed.

## A.7 Actual y-cruncher invocation: launch failure, no generated digits

The owner then ran:

```bat
python outlandish_big_constants.py pipeline --constant phi --digits 100000 --run
```

It completed only the safe Python preflight and y-cruncher launch step. y-cruncher immediately failed:

```text
[phi] y-cruncher exit code=3221225595; wall=0.1s
[phi] FAILURE CLEANUP: removed 0 failed-run data file(s); kept small reports
ARTIFACT AUDIT PASS (post-run / error-path): no misplaced generated/large files
ERROR: y-cruncher exit 3221225595
```

**Interpretation:** `3221225595` (unsigned) and `-1073741701` (signed) are both `0xC000007B`, Windows `STATUS_INVALID_IMAGE_FORMAT`. Likely failure to load an executable image or dependency/DLL. That code is not a mathematical failure, Python artifact-registry failure or disk-swap privilege failure. Its **specific cause was not determined**.

Direct execution of `C:\OUTLANDISH_WORK\y-cruncher v0.8.7.9547b\y-cruncher.exe` likewise printed nothing and returned `-1073741701`. Given the very recent y-cruncher Windows launcher and suspected runtime dependency, the owner attempted the official Microsoft VC++ **x64 Redistributable** (`vc_redist.x64.exe`) from the source SANDBOX mapped folder. Its installation appeared very slow; it was launched with `start` (asynchronous), and **successful installation was never conclusively verified**. Running y-cruncher afterwards still produced `0xC000007B`. Do **not** claim the correct Redistributable was definitely installed and failed to fix it; equally do not claim that `STATUS_INVALID_IMAGE_FORMAT` proves a missing runtime is the sole cause.

This is the decisive failure of the Sandbox experiment. The zero-byte ephemeral C: Python issue was separate; the **persistent Python actually worked well enough for all Python tests and checks**. Running the same Windows y-cruncher natively outside Sandbox had previously succeeded at 10^9 digits, so the obstacle is specific to this test guest/toolchain combination, but exact cause remains unproven.

## A.8 Operational disposition

- Owner judged Windows Sandbox not worth further effort and is deleting `T:\OUTLANDISH_01_SANDBOX\` and `T:\OUTLANDISH_01_SANDBOX_DATA\`, plus redundant Sandbox source-copy material on E: (exact deletion completion **not verified**).
- Any `.wsb`, copied production registry, persistent Python candidate, compiler bootstrappers and interim result logs within those trees are **temporary failed-test material**, not needed for ongoing OUTLANDISH operation. Do **not** delete G: active artifacts or E: working source.
- The guest test TOML had **no active registered constants**; the production registry on E: and verified six G: 10^9 files were not involved in a real Sandbox pipeline run.
- Retain narrative evidence in this handover. No future chat should propose spending more time on Sandbox as the default next step.

---

# Appendix B — Explanation of Windows Sandbox errors and limits of findings

| Symptom / output | What is established | What is *not* established |
|---|---|---|
| Silent/slow classic Python MSI installation | The owner observed extreme delays; Python eventually launched once on ephemeral C: | Exact responsible security policy; whether installing to T: resolves guest filesystem cause |
| `python.exe` = 0 bytes and `certutil 0x800703EE` | Guest C: executable was unusable after pip attempts | Root cause; host disk damage or driver fault |
| `cscript` no `.vbs` engine | Original shortcut creation couldn't execute | Whether all scripting methods fail (PowerShell COM succeeded) |
| Missing C++ 14+ while building PyYAML etc | Wheels fell back to source builds requiring MSVC compiler | Need for Visual C++ **runtime** or all packages to run OUTLANDISH |
| Visual Studio installer 35% / 149 of 268 | An expensive guest-C: compiler install stalled and was abandoned | That compiler *could never* complete on a normal machine |
| Eight artifact audit violations under `python_candidate` | Scientific scan root was overly broad | Corruption/misplacement of genuine scientific output |
| `0xC000007B` from y-cruncher | Windows guest couldn't load y-cruncher image/dependency | Which DLL failed, a y-cruncher algorithm bug, a `10^10` swap problem, or proof runtime redist succeeded |
| Power-management provider Event 55 logs | CPU capabilities enumerated at guest startup | NTFS file corruption or host disk errors |

**Relevant background research retained from previous conversation (7 Nov 2026):**

- Microsoft Windows Sandbox slow-MSI issues and trust verification: https://github.com/microsoft/Windows-Sandbox/issues/85 and https://github.com/microsoft/Windows-Sandbox/issues/68. These are relevant to extreme installation time, not proven causes of zero-byte `python.exe` or `0xC000007B`.
- Microsoft Q&A slow Python install in Sandbox: https://learn.microsoft.com/en-us/answers/questions/3898205/the-setup-process-performance-inside-windows-sandb
- Microsoft Sandbox configuration and mapping semantics: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file
- Windows error 1006 `ERROR_FILE_INVALID`: https://learn.microsoft.com/openspecs/windows_protocols/ms-erref/18d8fbe8-a967-4f1c-ae50-99ca8e491d2d
- Windows `STATUS_INVALID_IMAGE_FORMAT` code and y-cruncher Windows launcher notes were discussed in chat; recheck official release notes and dependency diagnostics if ever revisiting, but owner has closed Sandbox path.

---

# Appendix C — Historical handover filenames and their proper authority

The E: folder listing on 7 November contained these three documents (before owner agreed to clearer filenames). The following **renames were recommended; actual renaming was not independently verified**:

| Original | Suggested new name | What it represents |
|---|---|---|
| `OUTLANDISH_01_Standalone_Handover_Spec_v0_1.md` | `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md` | **5 Nov historical** early two-constant status, proposed Oz Lotto work, coding and experiment specification. Not latest implementation. |
| `OUTLANDISH_01_Standalone_Handover_Bundle_v0_1.zip` | `OUTLANDISH_01_2026-11-05_Historical_Source_and_Evidence_Bundle_v0_1.zip` | **5 Nov evidence bundle** accompanying the early handover; historical code/results snapshot, not current release. |
| `OUTLANDISH_01_Handover_2026-11-07_v1.md` | `OUTLANDISH_01_2026-11-07_Project_Status_and_Early_Sandbox_Diagnostics_v1.md` | **7 Nov early checkpoint**, pre-final Sandbox, before persistent T: Python verification and y-cruncher load failure. Superseded as conversation handover by this v2. |

**This document:** `OUTLANDISH_01_2026-11-07_Project_Status_and_Sandbox_Final_Closure_v2.md` is the **most current consolidated AI-to-AI conversation handover**. It is a guide, not a replacement for installed source code, actual live TOML, current repository README or original scientific evidence. Keep the historical files for provenance, but don't follow their obsolete paths and operational assumptions without checking current source.

---

# Appendix D — Suggested first exchange with the new ChatGPT conversation

> I am continuing the standalone `GAIS/OUTLANDISH_01` mathematical-constant search experiment. Please read `OUTLANDISH_01_2026-11-07_Project_Status_and_Sandbox_Final_Closure_v2.md` in full, and the installed source/TOML/README when supplied. The six verified 10^9 digit constants already exist on G: and must be preserved. The Windows Sandbox test has been abandoned: persistent Python and tests worked, but y-cruncher failed to load with `0xC000007B`. Our next route is **Debian/WSL2 on T:** with ext4 scratch, a minimal Linux y-cruncher test, then a genuine disk-backed benchmark. If WSL2 is impractical, discuss the owner's conditional native-Windows `SeManageVolumePrivilege` fallback without changing security settings until explicitly authorized. Do not set up VMware, a separate Hyper-V VM, or another Windows Sandbox experiment, and don't launch a 10^10 computation before we assess disk capacity, CPU/memory budget, checkpointing, verification and preservation of the native OUTLANDISH artifact registry.

## Provenance and verification limitations

- **Sources:** Owner's direct command transcripts and decisions in the current conversation through 7 Nov 2026; the earlier 39,423-byte v1 handover; the older November 5 standalone source/spec bundle; original pip failure log (1,605 lines), and installation artifacts and snippets examined in this chat. The assistant did not access the user's live E:/G:/T: disks or run the production experiment.
- **Labels:** *owner-reported* = asserted from user's command output/observation, not independently reproduced; *preview PASS* = source/software preflight only, not an actual digit-generation result; *abandoned* = user stopped pursuing route, not proof it cannot work for anyone.
- **Potential subsequent change:** Documents may become outdated after owner commits or local modifications. Inspect the current source and live TOML before taking any operational action. No user permission is inferred to delete files, change privileges, use holdout outcomes, or perform huge calculations.

**End of OUTLANDISH_01 consolidated v2 handover — 7 November 2026.**
