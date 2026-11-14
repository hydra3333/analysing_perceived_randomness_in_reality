# R-015 (b): the Windows POC suite rerun and the launcher / byte-code checks - owner-run instructions (DRAFT r3)

**DRAFT r3 (Claude web chat, 14 November 2026). The reviewer passed r2 for the default route (EX_167 section 4); r3 adds
only its three notes: check each result before the next block; what to do if the expected refusal does not happen; what
this rerun does not cover. Not authorised: run nothing here until the project owner gives it its own go.** Owner decision of
13 November 2026, 22:08 (R-015 (b)): the rerun is preferred; the optional `--with-timeout` test is excluded.

**Why.** MHUP-A changed `Run_Experiment.bat` (the interpreter option `-B`, the byte-code prefix and its refusal) and added
`Run_Evaluation.bat` (design 4.1, 6.1). The automated tests check these statically and on Linux; this is the one check on
your Windows machine that the real launchers still run the existing engineering probes byte for byte, write no byte-code,
and refuse when the byte-code folder exists.

**When.** Before Approval 1, never during the Mode H freeze. Two reasons: step 3 makes the forbidden folder for a moment
(every launch refuses while it exists), and the coordinator fails closed: if it ever judged a worker's fate uncertain it
would write the unresolved-orphan marker, which blocks every launch (Mode H included) until your approved manual clearance.
The cases below passed in October without that happening; run them on an idle machine all the same.

**What it touches.** Synthetic engineering probes only; no lottery data. It does write files: new Git-ignored run folders
under `transitory_data\poc_runs\`, and nothing else. Nothing is terminated. About two minutes. One CMD window (not
PowerShell); Claude Code closed.

**One block at a time.** Compare every line and every `EXIT` value with "Expect" before you run the next block. Anything
different is a STOP at that point: run nothing further, change nothing, send the whole window.

**Never add `--with-timeout`.** With process termination switched off, as it is, that case cannot stop its sleeping
worker: it would fail and write the orphan marker. It stays excluded unless separately reviewed and authorised.

## 1. Preconditions

```
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git status --short
dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json
if exist transitory_data\no_pycache_ever (echo NO_PYCACHE_EVER PRESENT) else (echo NO_PYCACHE_EVER ABSENT)
dir /s /b /a-d src\*.pyc 2>nul | findstr /v /i /c:"__pycache__" | find /c /v ""
```
Expect: nothing from `git status --short`; `File Not Found` for the orphan marker (if it exists, stop and send the output;
never clear it yourself); `NO_PYCACHE_EVER ABSENT`; `0` (no byte-code file under `src\` outside a `__pycache__` folder; files inside those folders
are never read by the launchers and do not count).

## 2. The POC suite (non-destructive; without `--with-timeout`)

```
"%CD%\.venv\Scripts\python.exe" -B tests\windows_architecture_poc_suite.py
```
Expect, in order: `[SMOKE] P1/P2 Windows engineering tests (no lottery dataset)`; five `PASS:` lines (the direct canonical
fixture; one-worker coordinator bytes match; 1-vs-6 byte-identical; exit 3 passed through; hard exit 7 flagged);
`NOT TESTED: timeout cleanup (use --with-timeout explicitly)`; `NOT TESTED: Ctrl+C, memory stress, ...`; `[SMOKE] PASS`.
`[SMOKE] FAIL` or anything else: STOP; send the whole window. Do not rerun, delete or "clean up" anything.

## 3. Two direct launcher runs: one that succeeds, one that exits non-zero (design 4.1)

`%RANDOM%` makes each run id new (a used id is refused by the probe).
```
call Run_Experiment.bat POC_Architecture_Probe.py --poc --case=canonical-fixture --run-id=poc-R015b-ok-%RANDOM%%RANDOM%
echo EXIT %ERRORLEVEL%
if exist transitory_data\no_pycache_ever (echo NO_PYCACHE_EVER PRESENT) else (echo NO_PYCACHE_EVER ABSENT)
call Run_Experiment.bat POC_Architecture_Probe.py --poc --case=exit-code --exit=3 --run-id=poc-R015b-exit3-%RANDOM%%RANDOM%
echo EXIT %ERRORLEVEL%
if exist transitory_data\no_pycache_ever (echo NO_PYCACHE_EVER PRESENT) else (echo NO_PYCACHE_EVER ABSENT)
```
Expect: `BEGIN POC_Architecture_Probe case=canonical-fixture ...`, a `RESULT` line, a `DIGEST` line,
`FINISH POC_Architecture_Probe SUCCESS`, `EXIT 0`, `NO_PYCACHE_EVER ABSENT`; then `BEGIN ... case=exit-code ...`, `EXIT 3`,
`NO_PYCACHE_EVER ABSENT`.

## 4. The launchers refuse when the byte-code folder exists (the one deliberate step)

This makes the folder that must never exist, checks that both launchers refuse to start, and removes it again.
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
`NO_PYCACHE_EVER ABSENT`. If either `EXIT` is not 10 (a launcher started when it had to refuse), or `rmdir` fails, or the
last line says `PRESENT`: STOP and send the output. An empty folder left behind is safe (every project launch refuses
while it exists); do not try to clear it another way.

## 5. Afterwards

```
call Run_Evaluation.bat Method_Mode_H.py statements
echo EXIT %ERRORLEVEL%
if exist transitory_data\no_pycache_ever (echo NO_PYCACHE_EVER PRESENT) else (echo NO_PYCACHE_EVER ABSENT)
dir /s /b /a-d src\*.pyc 2>nul | findstr /v /i /c:"__pycache__" | find /c /v ""
dir transitory_data\poc_runs\UNRESOLVED_ORPHAN.json
git status --short
```
Expect: the three fixed owner sentences (`open: ...`, `advance: ...`, `declare-developed: ...`; this command only prints
them and writes nothing) and `EXIT 0`; `NO_PYCACHE_EVER ABSENT`; `0` again; `File Not Found`; nothing from `git status --short`. Send Claude the whole window.

## Not covered (stated, not claimed)

The timeout case and process-tree termination (`--with-timeout`; excluded; no project tool ends a process whose state is
uncertain); Ctrl+C, memory stress and the other W-suite cases (the suite says so itself); and whether the official
results page still reads correctly, which is the separate fetch-and-parse check (readiness sheet, prerequisite 3).
