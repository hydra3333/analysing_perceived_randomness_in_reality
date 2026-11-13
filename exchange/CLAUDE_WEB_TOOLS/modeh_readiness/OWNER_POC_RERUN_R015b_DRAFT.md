# R-015 (b): the Windows POC suite rerun and the launcher / byte-code checks - owner-run instructions (DRAFT)

**DRAFT for the reviewer's check with the Approval 1 readiness sheet (Claude web chat, 13 November 2026). Not authorised:
run nothing here until the project owner gives it its own go.** Owner decision of 13 November 2026, 22:08 (R-015 (b)): the
rerun is preferred over accepting it unrun; the optional `--with-timeout` process-tree termination test is excluded.

**Why.** MHUP-A changed `Run_Experiment.bat` (interpreter options `-B`, the byte-code prefix and its refusal) and added
`Run_Evaluation.bat` (design 4.1, 6.1). The automated tests check these statically and on Linux; this is the one check on your
Windows machine that the real launchers still run the existing engineering probes byte for byte, and refuse when the
byte-code folder exists. **When:** before Approval 1 (it changes no code and no environment, so it does not touch the freeze).
**What it touches:** synthetic engineering probes only, no lottery data; writes only Git-ignored folders under
`transitory_data\poc_runs\`; nothing is terminated (the coordinator's termination is off, and the timeout case is not run).
About two minutes. One CMD window (not PowerShell), Claude Code closed.

## 1. Preconditions

```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git status --short
dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json
if exist transitory_data\no_pycache_ever (echo NO_PYCACHE_EVER PRESENT) else (echo NO_PYCACHE_EVER ABSENT)
dir /s /b /a-d src\*.pyc 2>nul | find /c /v ""
```
Expect: nothing from `git status --short`; `File Not Found` for the orphan marker (if it exists, stop: send the output; never
clear it yourself); `NO_PYCACHE_EVER ABSENT`; a number (write it down: the count of cached byte-code files under `src\`).

## 2. The POC suite (non-destructive; without `--with-timeout`)

```
"%CD%\.venv\Scripts\python.exe" -B tests\windows_architecture_poc_suite.py
```
Expect, in order: `[SMOKE] P1/P2 Windows engineering tests (no lottery dataset)`; five `PASS:` lines (the direct canonical
fixture; one-worker coordinator bytes match; 1-vs-6 byte-identical; exit 3 passed through; hard exit 7 flagged);
`NOT TESTED: timeout cleanup (use --with-timeout explicitly)`; `NOT TESTED: Ctrl+C, memory stress, ...`; `[SMOKE] PASS`.
`[SMOKE] FAIL` or anything else: STOP; send the whole window. Do not rerun, delete or "clean up" anything.

## 3. The launchers refuse when the byte-code folder exists (the one deliberate step)

This makes the folder that must never exist, checks that both launchers refuse to start, and removes it again. While the
folder exists every project launch refuses, which is the point; step 3's last line removes it.
```
mkdir transitory_data\no_pycache_ever
call Run_Experiment.bat POC_Architecture_Probe.py --poc --case=echo-argv --run-id=poc-R015b-refusal-check
echo EXIT %ERRORLEVEL%
call Run_Evaluation.bat Method_Mode_H.py statements
echo EXIT %ERRORLEVEL%
rmdir transitory_data\no_pycache_ever
if exist transitory_data\no_pycache_ever (echo NO_PYCACHE_EVER PRESENT) else (echo NO_PYCACHE_EVER ABSENT)
```
Expect: `[RUN-EXPERIMENT] ERROR: transitory_data\no_pycache_ever exists; refusing to run.` then `EXIT 10`;
`[RUN-EVALUATION] ERROR: transitory_data\no_pycache_ever exists; refusing to run.` then `EXIT 10`; then
`NO_PYCACHE_EVER ABSENT`. If `rmdir` fails or the last line says `PRESENT`: STOP and send the output (every project launch
keeps refusing until the empty folder is gone, which is safe).

## 4. Afterwards

```
call Run_Evaluation.bat Method_Mode_H.py statements
echo EXIT %ERRORLEVEL%
if exist transitory_data\no_pycache_ever (echo NO_PYCACHE_EVER PRESENT) else (echo NO_PYCACHE_EVER ABSENT)
dir /s /b /a-d src\*.pyc 2>nul | find /c /v ""
dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json
git status --short
```
Expect: the three fixed owner sentences (`open: ...`, `advance: ...`, `declare-developed: ...`; this command only prints them)
and `EXIT 0`; `NO_PYCACHE_EVER ABSENT`; the same count as in step 1 (no byte-code was written under `src\` by the launchers);
`File Not Found`; nothing from `git status --short`. Send Claude the whole window.

## Not covered (stated, not claimed)

The timeout case and process-tree termination (`--with-timeout`; excluded by your decision); Ctrl+C, memory stress and the
other W-suite cases (the suite says so itself).
