# TASK_T027 - Windows rehearsal of build step 2, third part: the comparison with the old records once more, with the corrected tool of package v1r3, in the scratch tree on D:

**Task ID:** T027. **Date:** 24 November 2026. **Author:** the Claude web chat. Rulebook v0.7 (RAT-44). **Section 2A applies to steps 3 to 7, in the folder `D:\DELETE_ME\a_p_r_i_r\T025\`** (the folder of TASK_T025, kept for this purpose).

**Purpose.** TASK_T026 ran the first fill of both games in the scratch tree `D:\DELETE_ME\a_p_r_i_r\T025\tree` and it passed; its last step, the comparison with the old system's records, stopped with `DIFFERENT: 2802` in each game (report `outbox\REPORT_T026.md`, main `dc0f532`). The Claude web chat found the cause in the comparison tool, not in the engine: the old system kept a record `INSUFFICIENT_HISTORY` for each target before a variant had enough earlier draws, a new list begins at the variant's first target and has no line there, and the tool wrongly asked for one. The tool is corrected in package `STEP2_Research_Engine_v1r3`, which the reviewer passed (EX_294). **That explanation is an inference until the corrected tool has read the real old run folders.** This task runs the corrected tool, and nothing else, on the scratch tree as it stands: the fill of TASK_T026 and the old run folders it copied are still there. **What a scratch run computes is a rehearsal, not a result of the project.**

**What it does not do.** It runs no research job and no launcher, makes no task clone, builds no Python environment, and has no network use. It changes nothing in the main repository (only this task's report is committed there) and nothing in the main `.venv`. The comparison tool reads only: it writes nothing and computes no forecast. It ends no process and changes no date, time or time zone. It names no real QA or PROD tree.

**Before the owner starts this task (the owner, not the runner):** `git pull --ff-only` has been done (it brings the corrected tool, in `exchange\EX_293_Claude\`) and this is a new Claude Code conversation; nothing of the project is running; `D:\DELETE_ME\a_p_r_i_r\T025` is as TASK_T026 left it. The task takes about ten minutes.

## Owner options

- None.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality` |
| PY (the main venv's Python) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe` |
| TOOL (the corrected tool, in the main repository; read only) | `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\exchange\EX_293_Claude\STEP2_Research_Engine_v1r3\tools\compare_fill_with_old_records.py` |
| SCRATCH (the scratch folder) | `D:\DELETE_ME\a_p_r_i_r\T025` |
| TREE (the scratch tree) | `D:\DELETE_ME\a_p_r_i_r\T025\tree` |
| SEV (the scratch evidence folder) | `D:\DELETE_ME\a_p_r_i_r\T025\evidence` |
| SPY (the scratch tree's own Python) | `D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe` |
| STOOL (the copy of the corrected tool that this task makes) | `D:\DELETE_ME\a_p_r_i_r\T025\evidence\compare_fill_with_old_records_v1r3.py` |

Run each command in Git Bash, from MAIN, exactly as written. On anything other than the expected output and exit code: **STOP**, record the output, and go to step 8. Never retry, repair or reorder a step. **After a STOP, leave `D:\DELETE_ME\a_p_r_i_r\T025` exactly as it is** (rulebook section 2A item 9).

**Recording** (so that nothing improvised is needed):
- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T027.md` as you go: after each step, add its command, its exit code and its output, before starting the next step.
- Exit codes: the program's own. Do not pipe a command under test into another program. Where a step below itself pipes a recorded file through `tr`, `grep`, `tail` or `wc`, that is only to show parts of the file.
- **What you may add to a task line, and nothing else:** `cd` to MAIN before it; and, for a line that does not itself write an `EXIT CODE` line, `echo "EXIT CODE $?"` straight after it. Neither is a deviation. For the time of a long step you may run `date +%H:%M:%S` in Git Bash as a command of its own before and after it: with a format it only prints the time. Never run `date` or `time` in CMD.
- **Steps marked (long)** can run longer than the shell's foreground limit, so each such command line carries its own recording: run that exact line as one background command, and wait until it has finished. Its output and, on the last line, its own exit status (`... EXIT CODE <n>`, written by the same shell straight after the program ends) are in the file the line names. If that last line is missing or shows another number than the step expects, that is a STOP: never infer a pass from the other lines, and never take an exit status from another shell or from the launch of the background command.
- **What goes into the report from a recorded file** is said at each step. Files under `D:\DELETE_ME\a_p_r_i_r\T025` stay there; only the text a step names is copied into the report, under a heading that names the file it came from (rulebook section 2A item 4 and section 7).
- **Never copy into the report:** a line that shows numbers drawn in any draw, or a line that shows a path under `C:\Users\`. Put `[line withheld: possible data value]` or `[line withheld: a user folder path]` in its place and say so under Deviations. The commands of this task print counts, draw numbers (which draw, not what was drawn), times and check lines.

## Steps

**1. Python.**
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```
Expected: the venv path, a Python version, and a Windows platform line.

**2. The main repository's state** (read-only; record the output; this step does not stop the task).
```
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

**3. The scratch folder is an ordinary folder on D:, and the scratch tree is as this task needs it** (rulebook section 2A item 2; read-only): its own Python, the new lists of both games and the copied old run folders are there, and this task's two files are not there yet.
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import os, sys; p = r'D:\DELETE_ME'; t = r'D:\DELETE_ME\a_p_r_i_r\T025\tree'; e = r'D:\DELETE_ME\a_p_r_i_r\T025\evidence'; j = getattr(os.path, 'isjunction', lambda x: False); missing = [n for n in (r'.venv\Scripts\python.exe', r'results\research\POWERBALL\variants', r'results\research\OZLOTTO\variants', r'results\real\development\contract_runs\POWERBALL', r'results\real\development\contract_runs\OZLOTTO') if not os.path.exists(os.path.join(t, n))]; early = [n for n in ('compare_fill_with_old_records_v1r3.py', 'early_comparison_v1r3.txt') if os.path.lexists(os.path.join(e, n))]; ok = os.path.isdir(p) and not os.path.islink(p) and not j(p) and os.path.normcase(os.path.realpath(p)) == os.path.normcase(p) and os.path.isdir(e) and not missing and not early; print('real path:', os.path.realpath(p)); print('missing:', missing); print('there already:', early); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```
Expected: `real path: D:\DELETE_ME`, `missing: []`, `there already: []`, then `SCRATCH CHECK PASS`.

**4. Copy the corrected tool from the main repository into the scratch evidence folder, by reading, and check that it is the tool the reviewer passed** (its SHA-256 after CRLF is made LF, so that Git's line endings do not matter).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I -c "import hashlib, shutil, sys; s = r'E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\exchange\EX_293_Claude\STEP2_Research_Engine_v1r3\tools\compare_fill_with_old_records.py'; d = r'D:\DELETE_ME\a_p_r_i_r\T025\evidence\compare_fill_with_old_records_v1r3.py'; shutil.copyfile(s, d); h = hashlib.sha256(open(d, 'rb').read().replace(b'\r\n', b'\n')).hexdigest(); ok = h == 'b4135af7ea925caba020bcbc77185999f51837bff0dcedddeb295ff0d241ada6'; print('TOOL SHA-256 (LF):', h); print('TOOL COPY PASS' if ok else 'TOOL COPY STOP'); sys.exit(0 if ok else 1)"
```
Expected: `TOOL SHA-256 (LF): b4135af7ea925caba020bcbc77185999f51837bff0dcedddeb295ff0d241ada6`, then `TOOL COPY PASS`.

**5. (long) The comparison with the old development records, with the corrected tool** (it reads only; a few minutes).
```
"D:\DELETE_ME\a_p_r_i_r\T025\tree\.venv\Scripts\python.exe" -B "D:\DELETE_ME\a_p_r_i_r\T025\evidence\compare_fill_with_old_records_v1r3.py" --tree "D:\DELETE_ME\a_p_r_i_r\T025\tree" > "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" 2>&1; echo "COMPARE EXIT CODE $?" >> "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt"
```

**6. The comparison's lines that are not per-variant lines, and the count of per-variant lines.**
```
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" | grep -v -e " equal$" -e "^DIFFERENT"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" | grep -c " equal$"
tr -d '\r' < "D:/DELETE_ME/a_p_r_i_r/T025/evidence/early_comparison_v1r3.txt" | grep -c "^DIFFERENT"
```
Copy the output of the three commands into the report. Lines beginning `DIFFERENT` are counted and never copied (they may show numbers drawn). **The exit codes of the second and third commands:** `grep -c` prints its count and exits 0 when the count is above 0, and exits 1 when the count it prints is exactly 0. For these two commands an exit code 1 together with a printed `0` is therefore not an error. An exit code 2, no number printed, or an exit code that does not fit the number printed, is a STOP. Whether the numbers themselves are the right ones is step 7.

**7. What step 6 must show.** Exactly these eight lines from the first command, with these numbers:
- `POWERBALL: part 1: old score records (TOP and WORST): 22884; equal in the new score lists: 22884; DIFFERENT: 0`
- a line beginning `POWERBALL: part 2: old development forecasts read from the run folders: 17280 (for 17280 variant and target pairs); equal in the new lists: 14478; INSUFFICIENT_HISTORY records before the variant's first target, where the new list has no line: 2802; DIFFERENT: 0;` and ending `(never forecast by the old development runs): 640`
- `POWERBALL: part 2: forecasts named by the tracked rank ledgers: 11442; of those not among the old forecasts compared: 0`
- `OZLOTTO: part 1: old score records (TOP and WORST): 11916; equal in the new score lists: 11916; DIFFERENT: 0`
- a line beginning `OZLOTTO: part 2: old development forecasts read from the run folders: 8760 (for 8760 variant and target pairs); equal in the new lists: 5958; INSUFFICIENT_HISTORY records before the variant's first target, where the new list has no line: 2802; DIFFERENT: 0;` and ending `(never forecast by the old development runs): 640`
- `OZLOTTO: part 2: forecasts named by the tracked rank ledgers: 5958; of those not among the old forecasts compared: 0`
- a line beginning **`RESULT: PASS - COMPLETE - both games; all 34800 old score records equal the new score lists; all 20436 old development forecasts in the run folders were found in the new lists`** and holding `the 5604 old INSUFFICIENT_HISTORY records all lie before their variants' first targets`
- `COMPARE EXIT CODE 0`

The second command prints **160**; the third prints **0**. **Anything else is a STOP**, and the report says exactly which line or number differs: any other number in any of these lines, a `DIFFERENT:` count above 0, a third number above 0, `RESULT: STOP`, `RESULT: PARTIAL` or `RESULT: REFUSED`, or another exit code. A different result is evidence to be read, not something to explain away.

## Clean-up

**8. Nothing to remove.** This task makes no task clone. **The scratch folder `D:\DELETE_ME\a_p_r_i_r\T025` is not removed by this task.** It is left as it is, whether the task passed or stopped; the project owner deletes it himself when the Claude web chat says it is no longer needed.

## Report

**9. Finish** `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T027.md` in the format of `outbox\README.md` (the step table and the RESULT line at the top). Also record:
- the wall-clock time of step 5;
- that this task created no folder under `D:\DELETE_ME\`, that it wrote two files into `D:\DELETE_ME\a_p_r_i_r\T025\evidence` (the tool's copy and `early_comparison_v1r3.txt`), and that `D:\DELETE_ME\a_p_r_i_r\T025` was left in place, not removed;
- whether the main repository's `git status --short` at the end is the same as in step 2 (run it again and include it).

## Finish

**10. Commit the report** (one file; not pushed).
```
"E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\.venv\Scripts\python.exe" -I "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\CLAUDE_CODE_WORKING_FOLDER_TREE\tools\cc_clone.py" commit-report --task T027
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**11. Tell the project owner** the RESULT line, the report's path, and: "please push".
