# P1/P2 — Automated unrelated-process decoy test v0.1

**Date:** 23 October 2026  
**Status:** Engineering-only add-on; Windows validation **pending**.  
**Authority:** Ratified Software Architecture v0.4, coordinator ownership policy, and owner's `ENABLE_PROCESS_TERMINATION = False` requirement.

## Package and source identity

Only one new repository test is installed:

- `tests/p1p2_automated_decoy_ownership.py` — NEW; does **not** overwrite any existing project file.

The ZIP also contains this explanatory handback; it can be retained separately or installed in the repository root. No project code, wrappers, requirements, research documents, or historic data are changed.

Reviewed coordinator v0.3 SHA-256 required by the utility:
`a2402175eaf22bf9d0293b49a6d1c91b48fe20d26866cf5d096dcfae6a95a58b`.

The utility verifies this exact coordinator content and also parses the source to require top-level `ENABLE_PROCESS_TERMINATION = False`. If either check fails, it refuses to launch anything.

## DECIDED

- Bundle the N1 unrelated-process probes into one coordinated, **non-destructive** run.
- Create three independent decoys: globally installed Python, this project's venv Python, and a separate `cmd.exe` (not the CMD that launched the test).
- Identify original decoys by PID **and creation time**, including the actual child Python process on Windows when `.venv` uses a Python redirector. Do not mistakenly treat a departed redirector's reused PID as a decoy.
- Launch **six** normal `sleep-timeout` engineering probes using the existing `Run_Coordinator.bat`, which in turn uses the existing `Run_Experiment.bat` for every worker.
- Use `--plan-termination` with 12-second sleep and 45-second worker timeout; inspect all six safety proofs and target lists. Check that no decoy appears, that no safety action occurs, and that the manifest reports six successes with kill switch False.
- After a passing or failing test, decoy Python programs receive a cooperative **stop-file** request; the independent CMD receives `exit` on **its own stdin pipe**. No `kill()`, `terminate()`, process-name-wide action or `taskkill` is implemented by this utility. Every decoy prints BEFORE and AFTER reports including its PID and executable name where identified.
- Python decoys automatically exit themselves after four minutes if the test harness fails unexpectedly. If the CMD decoy does not respond to `exit`, print the PID for human investigation, **never force-kill** it.
- An independent 100-second wait on the coordinator uses `Popen.wait(timeout=...)`, **not** `subprocess.run(timeout=...)`. If the coordinator exceeds the wait, the utility leaves it running, reports its PID and the log path, and declares the test incomplete/failed. It does not silently kill the wrapper or workers.
- Results and stdout logs go only to ignored `transitory_data/poc_runs/decoy_<uuid>/`; the six-worker coordinator's ordinary manifest is in sibling `decoy_<uuid>_coord/`.

## RECOMMENDED — Windows run instructions

Install the new file from the ZIP under the repository root, ensuring no existing file is replaced.

In an ordinary CMD window at the repository root:

```cmd
call activate_venv.bat
python tests\p1p2_automated_decoy_ownership.py --self-test
python tests\p1p2_automated_decoy_ownership.py
echo TEST_EXIT_CODE=%ERRORLEVEL%
```

The self-test checks parser behaviour only. The second command starts the decoys and the coordinator; there is no need to manually open further CMD windows or copy PIDs. The test prints the report and coordinator-console log paths and normally returns `0` only for a complete verified PASS.

**Do not run it if you have changed `ENABLE_PROCESS_TERMINATION` to `True`, or if the coordinator SHA-256 differs.** Do not press Ctrl+C while the test is running unless necessary; that would interrupt evidence collection and the result should be recorded as incomplete.

## OPEN / limitations

- **Actual Windows acceptance is pending.** Local validation covered Python syntax, source scanning for forbidden force-termination call sites, a synthetic plan parser, and a live cooperative Python decoy on Linux. It did **not** run Windows `cmd.exe` or the real coordinator.
- The third-party/global Python interpreter must exist; its path comes from the project's CPython `sys._base_executable`, and the test requires the global interpreter to report `sys.prefix == sys.base_prefix`.
- An unrelated Python interpreter in a *different third-party venv* is not included; a same-project venv, global interpreter and unrelated CMD are sufficient for this bundled first test. Another venv may be added at a later milestone if useful.
- These checks demonstrate **plan-only exclusion**, not safe forced termination, operating-system containment or full Windows P2 acceptance.
- The strict no-status/no-kill policy remains unresolved and unchanged. The two coordinator v0.3 safety corrections have already passed Claude's independent synthetic review, but no destructive validation is authorized.

## Safety evidence to return

Send ChatGPT the `DECOY BEFORE`, `DECOY VERIFY`, `DECOY STOP BEFORE`, `DECOY STOP AFTER`, `DECOY TEST` lines plus `TEST_EXIT_CODE`; if the test fails, also send the coordinator-console log at the path printed by the utility. No separate Claude review is needed for this add-only non-destructive test; consolidate the evidence at the next safety milestone.
