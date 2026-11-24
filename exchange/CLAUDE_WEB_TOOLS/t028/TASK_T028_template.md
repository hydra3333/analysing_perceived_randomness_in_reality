# TASK_T028 - a probe before build step 3 is coded: three facts about this Windows PC (renames when something is open; the size and time of a backup ZIP; what Python can read of other processes), in the scratch folder on D:

**Task ID:** T028. **Date:** 24 November 2026. **Author:** the Claude web chat. Rulebook v0.7 (RAT-44). **Section 2A applies to steps 3 to 8, in the folder `{{SCRATCH}}`** (new; this task creates it). Step 6 also reads, and only reads, under `{{OLDTREE}}` (the scratch tree of TASK_T025, if it is still there).

**Purpose.** Build step 3 (trees, installs, backups and restore) has the owner's go to be designed and coded in the cloud (decision log entry 217), and the owner agreed to this probe first (entry 219). Three things about it cannot be learned in the cloud, and its install, backup and restore logic is designed around them: (1) how Windows answers a rename, a replacement or a removal when a file is open or another program sits in the folder; (2) how large a backup ZIP of a tree with its `.venv` is and how long it takes to write, to read back and to read the tree twice; (3) what a Python program can read of the other processes on this PC, with psutil and with the standard library alone. **This task measures; it checks nothing and decides nothing.** The answers go to the Claude web chat in the report.

**What it does not do.** It runs no program of the project's software: no launcher, no research job, no command of the new system, no test suite. It makes no task clone, builds no Python environment and has no network use. It changes nothing in the main repository (only this task's report is committed there) and nothing in the main `.venv`. It ends no process: the probe starts one small helper program of its own, twice, and each time the helper ends by itself. It changes no date, time or time zone. It names no real QA or PROD tree. It reads no file under the main repository's `source_data`, `results` or `transitory_data`.

**The one program it runs** is the probe `inbox\TASK_T028_probe.py`, written for this task (standard library; it uses psutil, which the main venv has, for a comparison). The task copies it into the scratch folder and runs the copy with the main venv's Python. The probe writes only under `{{SCRATCH}}`. It prints counts, sizes, times, program names (such as `python.exe`) and Windows' answers; it prints no file's contents and no path under a user's folder.

**Before the owner starts this task (the owner, not the runner):** `git pull --ff-only` has been done and this is a new Claude Code conversation; nothing of the project is running; the folder `D:\DELETE_ME` exists. If `{{OLDTREE}}` is still there, leave it: step 6 measures on it. If it has been deleted, the task still runs, and step 6 measures the main `.venv` folder alone. The task takes about ten to fifteen minutes and writes two ZIP files of perhaps 100 to 400 MB each into the scratch folder.

## Owner options

- None.

## Paths

| Name | Full path |
|---|---|
| MAIN (the main repository) | `{{MAIN}}` |
| PY (the main venv's Python) | `{{PY}}` |
| PROBE (the probe, in the main repository; read only) | `{{PROBE}}` |
| SCRATCH (this task's scratch folder; created in step 4) | `{{SCRATCH}}` |
| SPROBE (the copy of the probe that this task makes) | `{{SPROBE}}` |
| OLDTREE (the scratch tree of TASK_T025, if still there; read only) | `{{OLDTREE}}` |
| ZIPOUT (the recorded output of step 6) | `{{ZIPOUT}}` |

Run each command in Git Bash, from MAIN, exactly as written. On anything other than the expected last line and exit code of a step: **STOP**, record the output, and go to step 9. Never retry, repair or reorder a step. **After a STOP, leave `{{SCRATCH}}` exactly as it is** (rulebook section 2A item 9).

**How the three probe steps (5, 6 and 8) are judged.** Each prints a first line `PROBE PART <name>: STARTED ...`, then its numbered measurement lines (`R..`, `Z..` or `P..`), then one last line. **The step passes only if that last line is exactly `PROBE PART <name>: FINISHED` and the exit code is 0.** A last line that says `REFUSED` or `FINISHED WITH ... NOT MADE`, a Python traceback, a missing last line or another exit code is a STOP. The measurement lines between are what this task is run to learn: no answer in them is expected or unexpected, and none of them passes or stops the step. In particular the words `WINDOWS SAID NO (...)` in a line of step 5 are Windows' answer to a question the probe asks on purpose.

**Recording** (so that nothing improvised is needed):
- Write `CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T028.md` as you go: after each step, add its command, its exit code and its output, before starting the next step.
- Exit codes: the program's own. Do not pipe a command under test into another program. Where step 7 pipes a recorded file through `tr`, that is only to show the file.
- **What you may add to a task line, and nothing else:** `cd` to MAIN before it; and, for a line that does not itself write an `EXIT CODE` line, `echo "EXIT CODE $?"` straight after it. Neither is a deviation. For the time of a step you may run `date +%H:%M:%S` in Git Bash as a command of its own before and after it: with a format it only prints the time. Never run `date` or `time` in CMD.
- **Step 6 is marked (long):** it can run longer than the shell's foreground limit, so its command line carries its own recording: run that exact line as one background command, and wait until it has finished. Its output and, on the last line, its own exit status (`ZIP EXIT CODE <n>`, written by the same shell straight after the program ends) are in the file the line names. If that last line is missing or shows another number than 0, that is a STOP: never infer a pass from the other lines, and never take an exit status from another shell or from the launch of the background command.
- **What goes into the report:** the whole output of every step, exactly as printed (steps 5, 7 and 8 print some tens of lines in all). Files under `{{SCRATCH}}` stay there; only the text that step 7 shows from ZIPOUT is copied into the report, under a heading that names that file (rulebook section 2A item 4 and section 7).
- **Never copy into the report** a line that shows a path under `C:\Users\`. Put `[line withheld: a user folder path]` in its place and say so under Deviations. The probe is written to print none.

## Steps

**1. Python.**
```
"{{PY}}" -I -c "import sys, platform; print(sys.executable); print(sys.version); print(platform.platform())"
```
Expected: the venv path, a Python version, and a Windows platform line.

**2. The main repository's state** (read-only; record the output; this step does not stop the task).
```
git status --short
git rev-parse HEAD
git log -1 --format=%s
```

**3. The scratch folder is an ordinary folder on D:, and this task's folder is not there yet** (rulebook section 2A item 2; read-only).
```
"{{PY}}" -I -c "import os, sys; p = r'D:\DELETE_ME'; t = r'{{SCRATCH}}'; j = getattr(os.path, 'isjunction', lambda x: False); ok = os.path.isdir(p) and not os.path.islink(p) and not j(p) and os.path.normcase(os.path.realpath(p)) == os.path.normcase(p) and not os.path.lexists(t); print('real path:', os.path.realpath(p)); print('task folder there already:', os.path.lexists(t)); print('SCRATCH CHECK PASS' if ok else 'SCRATCH CHECK STOP'); sys.exit(0 if ok else 1)"
```
Expected: `real path: D:\DELETE_ME`, `task folder there already: False`, then `SCRATCH CHECK PASS`.

**4. Make this task's scratch folder, copy the probe into it from the main repository by reading, and check that it is the probe this task was written for** (its SHA-256 after CRLF is made LF, so that Git's line endings do not matter).
```
"{{PY}}" -I -c "import hashlib, os, shutil, sys; s = r'{{PROBE}}'; t = r'{{SCRATCH}}'; d = r'{{SPROBE}}'; os.makedirs(t); shutil.copyfile(s, d); h = hashlib.sha256(open(d, 'rb').read().replace(b'\r\n', b'\n')).hexdigest(); ok = h == '{{PROBESHA}}'; print('PROBE SHA-256 (LF):', h); print('PROBE COPY PASS' if ok else 'PROBE COPY STOP'); sys.exit(0 if ok else 1)"
```
Expected: `PROBE SHA-256 (LF): {{PROBESHA}}`, then `PROBE COPY PASS`.

**5. The probe's part "rename"** (a few seconds; it works in its own new folder `{{SCRATCH}}\rename_part`).
```
"{{PY}}" -I -B "{{SPROBE}}" rename --work "{{SCRATCH}}"
```
Passes only as said above: last line `PROBE PART rename: FINISHED`, exit code 0. Copy the whole output into the report.

**6. (long) The probe's part "zip"** (several minutes; it reads the tree OLDTREE, or the main `.venv` folder if OLDTREE is not there, and writes two ZIP files into its own new folder `{{SCRATCH}}\zip_part`; it changes nothing it reads).
```
"{{PY}}" -I -B "{{SPROBE}}" zip --work "{{SCRATCH}}" --tree-root "{{OLDTREE}}" --tree-part ".venv" --tree-part "src" --tree-part "source_data" --tree-part "results\research" --otherwise-environment-of "{{MAIN}}" > "{{ZIPOUTF}}" 2>&1; echo "ZIP EXIT CODE $?" >> "{{ZIPOUTF}}"
```

**7. What step 6 recorded.**
```
tr -d '\r' < "{{ZIPOUTF}}"
```
Passes only as said above: the last two lines are `PROBE PART zip: FINISHED` and `ZIP EXIT CODE 0`. Copy the whole output into the report, under the heading `From the file {{ZIPOUT}}`.

**8. The probe's part "processes"** (a few seconds; it reads Windows' process table, twice, and starts and waits for its own helper program; it ends no process).
```
"{{PY}}" -I -B "{{SPROBE}}" processes --work "{{SCRATCH}}" --scratch-root "D:\DELETE_ME"
```
Passes only as said above: last line `PROBE PART processes: FINISHED`, exit code 0. Copy the whole output into the report.

## Clean-up

**9. Nothing to remove.** This task makes no task clone. **The scratch folder `{{SCRATCH}}` is not removed by this task,** whether the task passed or stopped; the project owner deletes it himself when the Claude web chat says it is no longer needed. Nothing under `{{OLDTREE}}` was changed.

## Report

**10. Finish** `{{MAIN}}\CLAUDE_CODE_WORKING_FOLDER_TREE\outbox\REPORT_T028.md` in the format of `outbox\README.md` (the step table and the RESULT line at the top). Also record:
- the wall-clock time of step 6;
- that this task created the folder `{{SCRATCH}}` under `D:\DELETE_ME\` (with the probe's copy, the recorded output of step 6 and the probe's three part folders in it) and that it was left in place, not removed;
- whether the main repository's `git status --short` at the end is the same as in step 2 (run it again and include it).

## Finish

**11. Commit the report** (one file; not pushed).
```
"{{PY}}" -I "{{CC}}" commit-report --task T028
```
Expected: `COMMIT-REPORT PASS`. If it STOPs, leave the report uncommitted and tell the project owner.

**12. Tell the project owner** the RESULT line, the report's path, and: "please push".
