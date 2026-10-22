# Windows Architecture POC — Coordinator Source Handback v0.1

**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Date:** 22 October 2026  
**Status:** Implementation candidate; **not** Windows-tested or accepted; Option F still conditional.  
**Authority:** ratified Windows POC Task Specification v0.1, Architecture v0.3, R2 Approved Erratum v0.2, R3 v0.2; Claude's six implementation notes.

## 1. Why this source package exists

This is the next bounded engineering deliverable after the Windows P0 standalone tests. It adds a coordinator for launching **only synthetic engineering POC programs** through the already-tested `Run_Experiment.bat`. No E_1–E_62 predictions, source-data access, holdout scoring, research fitting or final forecasting are performed.

## 2. Existing-file preservation

**New files only**; do not overwrite *any* existing repository file:

| File | Purpose |
|---|---|
| `Run_Coordinator.bat` | Human-facing launcher; explicit project `.venv` check, conditional activation and `SETLOCAL` restoration; CLI arguments forwarded using `%*`. CRLF. |
| `src/Powerball_Experiment_Coordinator.py` | Option F subprocess scheduler, six-worker ceiling, bounded pipe readers, monitoring, timeout/process-tree cleanup, result verification, immutable manifest and environment snapshot. |
| `src/methods/POC_Coordinator_Probe.py` | Additional **synthetic-only** sleeping, CPU and controlled-memory probe. No E-number, no lottery data. |
| `tests/windows_architecture_poc_suite.py` | Safe Windows smoke suite (direct-versus-coordinated one/six, failed/abrupt exits); optional timeout only when requested. |
| `tests/p1p2_static_checks.py` | Pure static compilation/text checks (not a substitute for Windows execution). |
| `P1_P2_Coordinator_Source_Handback_v0_1.md` | This handback. |

**Do not replace:** `.gitignore`, `.gitattributes`, `Run_Experiment.bat`, dependency installer v0.2, either existing activation script, existing P0 probe/common modules, research specifications, source CSVs or scraper.

## 3. Implementation rules

- **Coordinator starts child through `Run_Experiment.bat`** with `subprocess.Popen`, not through a separate Python interpreter, `ProcessPoolExecutor`, Job Objects or general-purpose plugin registration. Only the whitelisted POC programs are exposed; the `E_???_*.py` production discovery rule is not implemented here.
- **Workers:** 1–6, default 6. The input `--count` is independent of the concurrency limit.
- **Child output:** asynchronous daemon pipe reader per child with bounded queue; log every line, prefix relayed console messages, and never wait indefinitely for EOF. Missing EOF after cleanup is `ORPHAN_SUSPECTED`.
- **Result validation:** check child `sys.prefix`, true PID, status, canonical bytes, SHA-256 and console RESULT/DIGEST/FINISH consistency. One unique worker run folder for every invocation. No overwrite of an existing group manifest or worker result.
- **Failure/timeout:** on expiry enumerate live psutil descendants before killing the root; verify actual child PID plus creation time to guard PID reuse. `ORPHAN_SUSPECTED` prevents further launches and overall success. No experiment-spawned child processes in the current contract.
- **Memory:** coordinator monitors available physical RAM; POC memory allocations above 128 MB require `--allow-memory-stress`; **do not run 2-GB tests until basic P2 tests and operator review**.
- **Evidence:** ignored `transitory_data/poc_runs/<group-id>/manifest.json`, `pip_freeze.txt`, `runtime_environment.json`, per-worker logs; raw output remains disposable, not automatically committed as scientific evidence.
- **CMD AutoRun:** the coordinator inspects HKCU and HKLM Command Processor AutoRun entries and fails clearly if configured; it does not change the registry or rely on an untested hand-built `/D /C` command string.
- **Python upgrades:** do not assume `Popen.pid` names the computing interpreter. Repeat compatibility tests after upgrades. No Windows process management has been verified in the development container.

## 4. Installation safeguards

From the repository root:

1. Save or inspect local changes using `git status --short`.
2. Inspect the six entries in this ZIP before extracting; they should be absent from your checkout. If one already exists, **stop and compare before overwriting**.
3. Extract at repository root with paths preserved; the ZIP contains no `.git`, absolute paths, P0 replacements, dependencies or actual data.
4. Run `git status --short` and confirm only the six expected additions (existing P0 files may still be uncommitted). Do not commit until reviewing the source and local Windows evidence.

## 5. First safe Windows commands — IN ORDER

**Step A — Static check** (from project root; activate the project `.venv` if necessary):

```cmd
call activate_venv.bat
python tests\p1p2_static_checks.py
```

**Step B — One worker through the common wrapper, with full console output**:

```cmd
call Run_Coordinator.bat --poc --case=canonical-fixture --count=1 --workers=1
 echo %ERRORLEVEL%
```

Expected: one worker launched, P0 probe BEGIN/RESULT/DIGEST/FINISH, coordinator reports `PASS successes=1/1`, exit code 0. No prediction output; only synthetic fixture.

**Step C — Safe automated suite**: **only after Step B passes**.

```cmd
python tests\windows_architecture_poc_suite.py
 echo %ERRORLEVEL%
```

Expected: standalone and coordinated canonical bytes equal, one-versus-six equal, known exit-3 and hard-exit-7 correctly recorded, all within a small synthetic workload. The suite deliberately expects overall coordinator failure for the negative cases and verifies it. No memory stress or Ctrl+C test occurs.

**Step D — Optional, only after reviewing Step C**: a single sleeping worker timing out; this terminates the synthetic child process tree (no lottery work).

```cmd
python tests\windows_architecture_poc_suite.py --with-timeout
```

This repeats the safe checks before testing the timeout. **Do not run Step D until the smoke results are reviewed**, especially if the process-tree behaviour is surprising.

## 6. Evidence and classification

Report actual commands, console/return codes, test suite output and the specific ignored `manifest.json` paths. In particular record `wrapper_pid`, experiment PID, creation time, status, `console_integrity`, exit code, and any orphan diagnostics. The W suite is **NOT fully executed** by the smoke script.

- Already tested manually during P0: .venv automatic activation/restoration, external-venv rejection, invalid filenames, canonical fixture, ordinary failure, hard exit and deliberate non-overwrite collision.
- Collision/no-clobber belongs under **A-17/A-18 and POC-Q08**. **W-23 is the simulated upgrade-gating test and remains NOT TESTED**; do not reuse the earlier collision directory name as a test identity.
- Pending after initial smoke: large pipe-volume W-02, W-08 timeout (optional test), interactive Ctrl+C W-10/W-18, careful memory W-06/W-13, CMD quoting/path-with-spaces W-24, full upgrade gate W-23 and other W-suite obligations.
- `ERR-R2-02` (Option F) stays **provisionally approved**. Actual Windows P2 evidence, independent review and project-owner decision are required before final acceptance.

## 7. Implementation verification in the packaging environment

- New Python source files were syntax compiled and static-checked; the new batch file has CRLF-only lines.
- A **Linux surrogate process**, not Windows CMD, exercised six parallel synthetic jobs, expected nonzero and hard exits, and a bounded timeout/cleanup cycle. These checks do **not** prove Windows batch quoting, venv redirector behaviour, Ctrl+C or memory handling.
- Existing project source was used as the P0 contract baseline; **none of its files were changed by this ZIP**.

## 8. Next review gate

Collect real Windows results first. Diagnose any deviations before widening the P2 test matrix. Do not implement genuine E-methods or treat the W suite/Option F as closed merely because the safe smoke passed.
