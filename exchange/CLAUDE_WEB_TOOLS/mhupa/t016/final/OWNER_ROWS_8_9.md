# T016 owner sheet - F2 rows 8 and 9, run by the project owner at the real project root

**Reviewed (R-2 PASS, 11 November 2026). Run only after your own separate go for rows 8 and 9; no go has been given.** These two checks need the
real project root and, for row 9, a launcher, so Claude Code may not run them (rulebook rules 2.5, 2.7 and 2.9; section
2A keeps that). They are your own checks, run only after your separate approval for them, in CMD windows (not
PowerShell). No drawn outcome value is requested or printed; row 8 can read weekly ticket and forecast ledger metadata
if those files exist (before MHUP-B they do not; details below). Neither terminates anything; row 9 starts the existing
engineering-only sleep probe, which ends by itself.

**When.** After T016 has PASSed and before the live install's step 0, with the frozen package extracted to
`E:\TEMP\MHUPA_Install_v1` (the same zip, its SHA-256 checked as the install instructions say). Rows 8 and 9 can be run
in the same sitting.

## Row 8 - the install check prints CLEAN on your ordinary desktop

Keep open what is normally open (Claude Code, a console at the root, VS Code if you use it); close nothing on purpose.

```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
"%CD%\.venv\Scripts\python.exe" -I -B -X "pycache_prefix=%CD%\transitory_data\no_pycache_ever" "E:\TEMP\MHUPA_Install_v1\repo_overlay\src\package_tools\process_check.py" check-no-runs --root "%CD%" --install "E:\TEMP\MHUPA_Install_v1\PACKAGE_MANIFEST_MHUP_A.json"
```

- **Expect:** `CLEAN`.
- **What it reads:** the process table (name, parent and command line of every process; executable, folder, command
  line and start time of Python processes); `.venv\pyvenv.cfg`; whether `src`, `source_data`, `results` and `.git`
  exist; whether each game's `results\real\weekly\<GAME>\ACTIVE_SESSION.lock` exists; the one line of
  `source_data\.results_master.lock` if it exists (it should not); and, because MHUP-A changes the roster, the weekly
  ledgers `results\real\weekly\<GAME>\sessions\SESSION_*_attempts.jsonl` and `FORECAST_LEDGER_V1.jsonl` (they do not
  exist before MHUP-B, so in practice nothing is read). **Writes:** nothing. **Prints:** `CLEAN`, or one line per listed
  process (PID, start time, parent chain, executable, folder, command line) and `REFUSED`; no draw value.
- **Before you forward any output:** a listed process shows its full command line. Look through it for anything private
  (a password, a token, a private path) and blank only that part; keep the PID, start time, executable, folder and the
  `REFUSED`/`CLEAN` line.
- **If REFUSED:** send the whole output to Claude (after that look-through). A refusal naming a real process is
  evidence to investigate, never a reason to end that process. A known false positive is a VS Code Python helper started at the
  root; you may close it through VS Code and run the line again. Nothing is ever terminated by the tool.

## Row 9 - a live launcher child is listed, and CLEAN returns after it ends by itself

**Precondition** (run first, in window B):
```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json
```
Expect "File Not Found". If the file exists, do not run this row; send the output to Claude.

**Window A** - start the probe. Replace `YYYYMMDDHHMM` with the current date and time (for example `202611121530`), so the
run id is new:
```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
Run_Experiment.bat POC_Coordinator_Probe.py --poc --case=sleep-timeout --sleep-seconds 120 --run-id poc-T016-row9-YYYYMMDDHHMM
```
Expect `BEGIN POC_Coordinator_Probe case=sleep-timeout run=poc-T016-row9-...`. It then sleeps for 120 seconds.

**Window B, within those 120 seconds** - the row 8 command (paste its second line again). Expect `REFUSED`, with the
probe's process(es) listed, each with its PID and start time: the venv's `python.exe` (its executable), with its folder
`src\methods` under the root and the root on its command line or an ancestor's.

**Window A** - wait until it prints `FINISH POC_Coordinator_Probe SUCCESS` and returns to the prompt. Do not close it
early. If it never ends by itself, wait; if you must, close window A yourself, and say so.

**Window B, after the FINISH line** - the row 8 command once more. Expect `CLEAN`.

- **What the probe does:** it is the existing synthetic engineering probe (`src\methods\POC_Coordinator_Probe.py`): no
  lottery data and no coordinator. It writes only `transitory_data\poc_runs\poc-T016-row9-...\status.json` and
  `canonical_result.json`. That folder is ignored by Git (it never shows in `git status` and does not affect the
  install's clean-tree check); the files are harmless and can stay.
- **Nothing is terminated** by any tool here.
- **Send Claude** the three outputs of window B and the two lines of window A.
- **If you do not approve row 9:** the oracle is reported unmet. A bare sleeping Python is not a substitute.
