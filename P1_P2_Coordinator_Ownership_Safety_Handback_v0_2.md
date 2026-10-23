# Windows P1/P2 coordinator process-ownership safety patch v0.2

**Date:** 23 October 2026  
**Status:** ENGINEERING REVIEW / NON-DESTRUCTIVE WINDOWS TEST CANDIDATE; **not** production-approved.  
**Authority:** owner-ratified `doc/Predictive_Randomness_Software_Architecture_Discussion_v0_4.md`; Claude safety review v2 and subsequent Option F clarification, augmented by the owner's explicit termination safety switch and BEFORE/AFTER report requirement.

## Package and preservation

Package contains precisely **one replacement** and **two new files**:

- **REPLACE** `src/Powerball_Experiment_Coordinator.py` — the coordinator from P1/P2 source package v0.1 only.
- **NEW** `tests/p1p2_non_destructive_safety_checks.py` — synthetic tests, never start or terminate OS processes.
- **NEW** `P1_P2_Coordinator_Ownership_Safety_Handback_v0_2.md` — this handback.

Original P1/P2 coordinator v0.1 SHA-256 (before replacement):

`ec83cf85c091f6f73ea733bcdcc062a646ff6dc55a6e178b0b042cb245850186`

**If your on-disk coordinator checksum does not match, do not overwrite.** Supply the current file for reconciliation. No other existing files should be replaced; no changes to `.venv`, P0 scripts, the RATIFIED architecture, dataset, or prediction methodology. The existing six-file P1/P2 source ZIP remains an untouched historical baseline. Git has not been committed or pushed by the author.

## Binding safety switch

Near the top of `src/Powerball_Experiment_Coordinator.py`:

```python
ENABLE_PROCESS_TERMINATION = False
```

**False is the shipped default.** There is deliberately **no command-line override**. Only the owner changing it in the source to `True` can permit kill requests. **Do not change it yet.** In addition, `--plan-termination` is always non-destructive, even if the switch is later True.

Every stop request prints BEFORE with root PID/name/creation time, retained descendants' PID/name/creation times and parent/depth; then AFTER with no-action/refusal/attempts/outcomes. Output appears in the console; summary details are in `manifest.json`. A disabled stop cannot report `STOPPED_CONFIRMED` and coordinator exits unsuccessfully (and may leave a process running). This safeguard is not a sandbox: `Ctrl+C` delivered by the *console* to a worker may independently cause that worker to exit; the switch controls only coordinator-issued termination.

## Implementation changes

- Process ownership is established by **live parent/child ancestry while the `Run_Experiment.bat` root CMD wrapper is alive**, with per-edge creation-time consistency. Captured `psutil.Process` objects are retained. The status-file PID is **only a validation observation**, never added to kill candidates.
- Root is killed, *only if enabled and ownership validated*, through its `subprocess.Popen` handle. Owned descendants, *only if enabled and ownership validated*, are killed through their retained `psutil.Process` objects, whose kill implementation detects reused PIDs.
- Expected process-name sanity filter for normal, venv-activated coordinated runs: root `cmd.exe`; verified descendants `cmd.exe`, `findstr.exe`, `python.exe`. This reflects actual `Run_Experiment.bat` (including `findstr.exe`). These names do **not** independently confer ownership. Full executable paths are optional evidence, not termination authority.
- The coordinator now checks both `sys.prefix` **and** active `VIRTUAL_ENV`, normalised to the project's `.venv`. Normal human start remains `Run_Coordinator.bat`, which can activate and then restore the caller's environment. Direct Python coordinator start without activation fails; manually launched individual experiments still use `Run_Experiment.bat`.
- Ctrl+C uses a flag-setting handler instead of asynchronous `KeyboardInterrupt` cleanup. Further Ctrl+C is ignored once cleanup begins; the manifest is still attempted, and interrupted exit code is `130`.
- No `taskkill` fallback, no PID-from-status kill, and no Windows Job Object. The batch runners are **unchanged**.
- `--allow-memory-stress` is refused while `ENABLE_PROCESS_TERMINATION` is False; avoid all memory pressure testing until separate approval.
- `--plan-termination` is a **preview** during normal, naturally completing sleep tests. It enumerates ownership and emits BEFORE/AFTER without killing; it is *not* evidence of successful forced termination.

**Residual limitations:** A process which starts/exits between periodic scans may not be captured. A descendant can be missed after its parent disappears. No wrong-process-kill guarantee is asserted without OS isolation. In uncertainty, leave the process alone, report anomaly and fail the run. No production acceptance until full Windows test gates and independent review.

## Step-by-step safe Windows testing — current batch files unchanged

Use ordinary CMD in repository root. **Do not set the kill switch to True.**

1. Verify original coordinator identity *before* extraction:

   ```cmd
   certutil -hashfile src\Powerball_Experiment_Coordinator.py SHA256
   ```

   Expected original v0.1 hash above. If mismatched, **STOP** and reconcile; no overwrite.

2. Extract the package into repository root, allowing replacement of **only** `src\Powerball_Experiment_Coordinator.py`. The other two files must be new.

3. Verify syntax and non-destructive synthetic tests:

   ```cmd
   call activate_venv.bat
   python tests\p1p2_static_checks.py
   python tests\p1p2_non_destructive_safety_checks.py
   ```

   Expect PASS messages. The safety test does not spawn or kill any process.

4. Real Windows ancestry preview, *one worker* (the sleep finishes naturally):

   ```cmd
   call Run_Coordinator.bat --poc --case=sleep-timeout --count=1 --workers=1 --sleep-seconds=12 --timeout-seconds=45 --plan-termination
   echo %ERRORLEVEL%
   ```

   Expect `ENABLE_PROCESS_TERMINATION=False`, `SAFETY BEFORE` (root/descendants), matching experiment evidence, `SAFETY AFTER ... PREVIEW ONLY; no termination attempted`, normal RESULT/DIGEST/FINISH, coordinator PASS and exit code 0. **Look for root `cmd.exe`, descendant `python.exe` and possibly transient `cmd.exe` or `findstr.exe`**, recording the actual tree shape. *No `chcp.com` normally under a coordinator-launched individual experiment.* No kill actions should appear.

5. On confirmation of step 4, test **six-worker** plan-only preview with the same `--sleep-seconds=12 --timeout-seconds=45 --plan-termination`, but `--count=6 --workers=6`. This is only a subsequent authorised step; do not run it just to establish this patch's initial installation.

6. Perform the remaining N-series negative tests and unrelated-process decoys before proposing **any** switch change to True. Do not run timeout, interruption, memory-guard forced-termination or any D-series destructive tests yet. A disabled switch would leave live workers, not safely complete a termination test.

## Acceptance evidence

**Passed here:** Python AST compilation; prior P1/P2 static syntax/architecture checks; synthetic independent process-ancestry/allow-list checks, forged status decoy, run-id mismatch, `False` switch, safe plan-only mode even when a fake-module switch is True, ownership refusal with True, BEFORE/AFTER report. No OS process was killed or started by the synthetic tests.

**Not yet done:** actual Windows ancestry enumeration and pipe observation with this patch, true six-worker preview, unrelated real process decoys, genuine termination while owner-enabled, Ctrl+C completion, leak/orphan checks, production acceptance.

### Meaning of a dry-run failure

With owner switch `False`, a timeout/interrupt cannot be declared cleanly terminated. If accidentally triggered, check the console output and live processes; do **not** change the switch simply to silence the failure. `ORPHAN_SUSPECTED` / `TERMINATION_DISABLED` describes a required manual investigation, not proof that other Windows processes were affected.
