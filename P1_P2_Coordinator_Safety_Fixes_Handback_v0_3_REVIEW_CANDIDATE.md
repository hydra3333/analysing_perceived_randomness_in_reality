# Predictive Randomness — P1/P2 coordinator safety fixes v0.3

**Status:** SOURCE REVIEW CANDIDATE — not owner-ratified, not Windows-tested.  
**Date:** 23 October 2026  
**Authority:** ratified Software Architecture v0.4 and owner's termination safety requirements.  
**Source base:** the post-commit repository snapshot `analysing_perceived_randomness_in_reality-main(4).zip`, coordinator v0.2.

## Purpose and scope

This is a **narrow correction of Claude's two identified v0.2 defects**, not a redesign of the launch architecture or an approval to enable process termination.

1. **PID reuse:** `capture_owned_tree()` now distinguishes the old captured process from a new child with the same PID. If the stored process object is *confirmed gone*, it is moved to `departed_members`, removed from active membership, and the new process must independently pass *all* ancestry, parent/child creation-time and executable-name checks. If the previous identity is alive **or unverified**, record `MEMBER_PID_IDENTITY_CONFLICT` and refuse the new candidate. No status-file PID is ever used to create a kill target.
2. **Asynchronous termination:** After each successful `psutil.Process.kill()` request (only if the owner switch was manually enabled, and ownership verified), wait on those same stored objects with `psutil.wait_procs(..., timeout=3.0)` before checking survivors. The original wrapper root is still killed only by its Popen handle, and waited for independently. A wait error or live/unverifiable survivor prevents `STOPPED_CONFIRMED`.

The retired-member list is historical evidence only. It is **never** a termination target list.

## Explicitly unchanged

- `ENABLE_PROCESS_TERMINATION = False` near top of source, with **no CLI override**. Do not change to True before separate owner authorisation, Claude source review and safe Windows acceptance tests.
- Every cleanup request emits `[SAFETY BEFORE]` naming root and targets (PID/name/creation time), `[SAFETY ACTION]` only if an owner-enabled cleanup actually attempts a kill, and `[SAFETY AFTER]` with action/wait/survivor/refusal evidence. A dry run reports no signals.
- The strict current policy remains: if no experiment is positively matched by its status PID and creation time, **no coordinator termination is permitted**, even for otherwise verified descendants. The owner decision whether to relax this to "kill verified descendants and report UNVERIFIED" is **OPEN**; v0.3 does *not* prejudge it.
- `Run_Coordinator.bat` → Python coordinator → `Run_Experiment.bat` → per-method Python, or manual `Run_Experiment.bat`. No direct alternative production launch, no taskkill, no project-managed Job Objects, no child-spawning experimental methods.
- Current normal-path descendant-name sanity list: `cmd.exe`, `findstr.exe`, `python.exe`. Executable names alone confer no ownership.
- Only engineering probes, no scientific E-methods or read of source/holdout data.

## Installation and source preservation

The installation ZIP contains precisely **one replacement** and **two new files**:

- **REPLACE** `src/Powerball_Experiment_Coordinator.py`
- **NEW** `tests/p1p2_safety_regression_v0_3.py`
- **NEW** `P1_P2_Coordinator_Safety_Fixes_Handback_v0_3_REVIEW_CANDIDATE.md`

**Before extraction**, run from the Windows repository root:

```cmd
certutil -hashfile src\Powerball_Experiment_Coordinator.py SHA256
```

Expected v0.2 original: `26c471e183d073db6e258a51c5b363f90d3024bc497ebebeba804a25ab187cf4`.

If the checksum differs, STOP; the attached snapshot may no longer match the working tree, and the patch must be reconciled. No P0 files, existing tests, data, ratified documents or handovers are replaced. No requirements/dependency changes. This package makes no Git commits.

New source SHA-256 after installation: `a2402175eaf22bf9d0293b49a6d1c91b48fe20d26866cf5d096dcfae6a95a58b`.

## Safe Windows test sequence — only after Claude review

The four source/synthetic checks below do not launch or terminate experiment processes:

```cmd
call activate_venv.bat
python tests\p0_static_checks.py
python tests\p1p2_static_checks.py
python tests\p1p2_non_destructive_safety_checks.py
python tests\p1p2_safety_regression_v0_3.py
```

The new regression uses **fake process objects only**. A simulated in-memory True switch tests call ordering with a **mocked** `psutil.wait_procs`; it does not edit the Python source switch, start a process or terminate any OS process.

If reviewed and all checks pass, the next real Windows check can be a naturally completing **six-worker plan-only preview** (owner-switch stays False):

```cmd
call Run_Coordinator.bat --poc --case=sleep-timeout --count=6 --workers=6 --sleep-seconds=12 --timeout-seconds=45 --plan-termination
echo %ERRORLEVEL%
```

Expect six BEFORE/AFTER previews, natural finishes, no `[SAFETY ACTION] KILL`, and review *all* per-worker `ownership_anomalies` and `unmatched_status`, **not only** the overall `PASS`. This is a real Windows process-launch test; do not run it until the review is complete. Never run this command through the separate automated smoke suite for this checkpoint: that suite has an independent 120-second timeout that can kill its own `Run_Coordinator.bat` handle regardless of the owner switch.

## Current evidence and limitations

**Passed in isolated Linux synthetic/static checks:** original P0, existing P1/P2 static, existing v0.2 non-destructive ownership checks, and new v0.3 regressions covering exited-PID reuse, same-PID live conflict, switch False, and *fake* asynchronous termination followed by bounded wait. No live process was started or killed by these checks.

**Not yet validated:** v0.3 on the owner's Windows environment, six-worker preview with this revision, unrelated live decoys, cleanup of genuine timeouts, Ctrl+C, actual Windows termination, memory guard and production Option F acceptance.

**Safety limitation:** process-tree supervision remains best-effort and must not be described as OS-enforced containment or an unconditional no-wrong-kill guarantee. Ownership uncertainty remains fail-safe; the operator may need to inspect a suspected orphan manually.

## Specific Claude review request

Please inspect the v0.2→v0.3 diff against the supplied committed snapshot and your two bug reports. Review whether the confirmed-gone retirement and fresh ancestry verification prevent false `MEMBER_PID_REUSED`, including races when the reused PID was formerly a parent; whether the bounded descendant wait and final survivor check are appropriately fail-safe; and whether any changes accidentally broaden termination authority. Confirm that the owner switch is **False**, status PID remains evidence-only, and current strict no-status/no-kill policy remains. Do not approve destructive Windows tests as a consequence of this synthetic review alone.
