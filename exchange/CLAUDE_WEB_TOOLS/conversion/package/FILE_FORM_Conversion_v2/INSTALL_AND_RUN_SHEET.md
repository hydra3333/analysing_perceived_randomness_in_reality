# FILE_FORM_Conversion_v2 - DEV brought to the file-form standard (doc/FILE_FORM_STANDARD_v0_2.md, RAT-49): the sheet

**One attempt. Each part only on the owner's own go.** Built against commit `abfcfc962c78fad1c0f2a472681a1ebcb6d3fcb3`.

**The whole safety net is your copy of the whole project folder (part 1).** This conversion is never resumed
(EX_313). **If anything prints `STOP`, `FAIL`, `REFUSED`, an error, or anything other than what this sheet
expects: stop there. Run nothing again, change nothing, send Claude the whole window.** The way back is part 9:
the whole folder put back from your copy, on your own go. A fresh attempt comes only after the cause is understood.
(The one exception: in part 5 the word `FAILED` on a module's line and the lines `FAILS IN BOTH RUNS` are the three
failures that exist today, and are expected as long as the comparison ends as part 5 says.)

**What it does.** Copies in 12 files (4 new, 8 replaced: the engine's writers now write CRLF;
`.gitattributes`; `.gitignore`). Changes the line endings, and nothing else, of the other listed files
(686 on the list) and of `ENVIRONMENT.ini`. **Removes DEV's research results (`results\research\`) and the status
file in each variant folder**, which the fill in part 6 makes again. Stages the result in Git and puts the
documents' working copies back to Git's own bytes. **It does not touch** the results masters and their ledgers (it
proves them unchanged), the `.jsonl` ledgers, the updater's grabs and backups, the old system's records, the six
retired Mode H files, `.venv` or `GAIS\`. No calculation is changed. Nothing here contacts a lottery website,
changes the PC's date or time, or ends a process.

**Before you start:** nothing of the project running (no research job, no results update, no runner task), and no
editor holding a file of the project open. Use **one CMD window** for parts 1 to 8, so that the five names set in
part 1 stay set.

## Part 1. Update, check the package, make your copy and check it (about 10 minutes)

```bat
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
set PY=.venv\Scripts\python.exe
set ZIP=exchange\CLAUDE_WEB_TOOLS\conversion\package\FILE_FORM_Conversion_v2.zip
set PKG=E:\TEMP\FILE_FORM_Conversion_v2
set EVID=E:\TEMP\FILE_FORM_evidence_v2
set COPY=E:\TEMP\FILE_FORM_copy_of_project
git status --short
git pull --ff-only
git status --short
git log -1 --format=%h -- src tests
certutil -hashfile "%ZIP%" SHA256
if exist "%PKG%" echo STOP: %PKG% exists already
if exist "%EVID%" echo STOP: %EVID% exists already
if exist "%COPY%" echo STOP: %COPY% exists already
```

Expected: both `git status --short` print nothing; the pull says `Fast-forward` or `Already up to date`; the
`git log` line prints **`5f16b35`** (no commit has touched `src` or `tests` since build step 2, so the suite run made
after build step 2 is the baseline for part 5); `certutil` prints the SHA-256 **Claude gave you in the chat for
`FILE_FORM_Conversion_v2.zip`**; and the three `if exist` lines print **nothing** (none of the three folders exists
yet). If one prints `STOP`, tell Claude. (`COPY` may be set to any other new folder outside the project
folder, on a drive with room for the whole project folder.)

Then unpack the package and make the copy:

```bat
%PY% -I -m zipfile -e "%ZIP%" E:\TEMP
robocopy . "%COPY%" /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NFL /NDL /NP
%PY% -I -B "%PKG%\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase copy --copy "%COPY%"
```

Expected: robocopy's summary shows **0** in the columns `Mismatch` and `FAILED`; then a line
`compared ... file(s)` and the last line **`COPY PASS (your copy holds every file of the project folder, byte for
byte)`** (it reads every file twice: a few minutes). **Do not go on without `COPY PASS`.**

## Part 2. Check, copy the package's files in, check (a minute)

One line; each step runs only if the one before it passed:

```bat
%PY% -I -B "%PKG%\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase pre && xcopy "%PKG%\repo_overlay\*" . /E /H /Y && %PY% -I -B "%PKG%\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase post
```

Expected: `PRE PASS`; `12 File(s) copied`; `POST PASS`.

## Part 3. Convert (a few minutes)

```bat
%PY% -I -B "%PKG%\tools\convert_to_file_form.py" --tree . --list "%PKG%\CONVERSION_LIST.json" --copy "%COPY%" --record "%EVID%\CONVERSION_RECORD.json"
```

It prints what it found, class by class, **before it changes anything**. Check before you type:
the second line names the list's SHA-256 `40abea55b09e13f341f056a43596c334e10ef462563715c42a850175a919f2f4`;
`IN NO CLASS, OR NOT AS EXPECTED ........ 0`; four results files under `UNTOUCHED, AND PROVED UNTOUCHED`; and a
line saying your copy holds every file to be converted and to be removed. (On 24 November your look showed 650 to
convert and 1,578 to remove; with the package's files copied in, the first number is now a little lower.)
**Type `CONVERT`** and Enter, then **type `REMOVE`** and Enter. Nothing is changed until both are typed.

Expected, at the end: a line beginning `PROVED: all 686 listed files have the list's "after" SHA-256`, and the
last line `FILE-FORM CONVERSION - END - FINISHED. Go on with the next part of the sheet.`

## Part 4. Stage in Git, and put the documents' working copies back (a minute or two)

```bat
%PY% -I -B "%PKG%\tools\stage_and_refresh.py" --tree . --list "%PKG%\CONVERSION_LIST.json"
```

It prints what it will do before it does it. Check before you type:
`TO BE STAGED, exactly as on disk ....... 685 of the 686 listed file(s)`; some two thousand working copies to
be put back, most under `exchange`, **none under `GAIS`, `source_data` or `results`**; and
`NOT AS EXPECTED ........................ 0`. **Type `STAGE`** and Enter.

Expected: a line beginning `PROVED: all 686 listed files are staged`, and the last line
`STAGE AND REFRESH - END - FINISHED. Nothing was committed or pushed: that is the next part of the sheet.` Then:

```bat
git status --short | find /c /v ""
git status --short | findstr /v /b /c:"M  " /c:"A  "
```

Expected: the first prints **685**; the second prints **nothing**.

## Part 5. The suite, and the comparison with the suite after build step 2 (about 30 minutes)

```bat
%PY% -B "%PKG%\tools\run_suite.py" . "%EVID%\suite_after"
%PY% -B "%PKG%\tools\compare_suite_reports.py" "E:\TEMP\STEP2_evidence\suite_after" "%EVID%\suite_after" > "%EVID%\comparison.txt"
findstr /v /b /c:"NEW: " /c:"MODULE NEW: " "%EVID%\comparison.txt"
find /c "NEW: " "%EVID%\comparison.txt"
git status --short | findstr /v /b /c:"M  " /c:"A  "
```

(If `E:\TEMP\STEP2_evidence\suite_after` no longer exists, stop and tell Claude: the baseline is then made from
your copy, and Claude gives the two commands.)

Expected: the suite's last line `DONE: 54 modules, 830 tests ran`. From `findstr`, exactly these:
`before: 52 modules; unittest ran 762 tests; identified here: 762`;
`after: 54 modules; unittest ran 830 tests; identified here: 830`;
**`tests in both runs: 762; with the same result: 762`**;
three entries `FAILS IN BOTH RUNS` (`test_gitignore_lines`, with the words `FAILURE LINES DIFFER` and its two long
lines; and two tests of `test_multigame_reader_contracts`);
and the last line `RESULT: DIFFERENCES FOUND - each needs an explanation`, **which is expected here:** the only
differences are the 2 new test modules and their 68 new tests. `find /c` prints **70**. The last command prints
**nothing**.
**A STOP is any line beginning `CHANGED`, `DISAPPEARED`, `MODULE CHANGED`, `MODULE DISAPPEARED`,
`NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`, a `tests in both runs` line whose two numbers differ, a count other
than 70, or any line from the last command.**

## Part 6. Commit and check (not pushed), then the fill - the fill on your own separate go

```bat
git commit -m "FILE-FORM STANDARD (RAT-49): DEV converted to CRLF; the engine's writers write CRLF; Git converts nothing" && %PY% -I -B "%PKG%\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase committed
```

Expected: **`COMMITTED PASS`**. **Do not push yet.**

Then the fill (about 47 minutes; leave the window alone):

```bat
Run_Research.bat --game BOTH --no-update
```

Expected, at the end: for each game a line beginning `POWERBALL: finished. Results on file through draw` (and the
same for `OZLOTTO`), each ending `prevailing OV-1: not started; waiting for a successful results step`; no line
beginning `WARNING`; and the last line **`The job finished.`** A line with `REFUSED` or `STOPPED`, or a last line
`A STOP is a STOP: ...`, is a STOP.

Then the same command once more, into a file (a few minutes):

```bat
Run_Research.bat --game BOTH --no-update > "%EVID%\second_job.txt" 2>&1
type "%EVID%\second_job.txt"
git status --short
```

Expected: for each game `written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files`;
the last line `The job finished.`; and `git status --short` prints nothing.

## Part 7. The comparison with the old development records, and the push

```bat
%PY% -B "%PKG%\tools\compare_fill_with_old_records.py" --tree . > "%EVID%\comparison_with_old_records.txt" 2>&1
findstr /v /e /c:" equal" "%EVID%\comparison_with_old_records.txt"
findstr /e /c:" equal" "%EVID%\comparison_with_old_records.txt" | find /c /v ""
```

It reads only. Expected from the first `findstr`, exactly seven lines, as after build step 2: for each game the
two `part 1` and `part 2` lines with **`DIFFERENT: 0`** and the line about the tracked rank ledgers ending
`not among the old forecasts compared: 0`; and the last line beginning **`RESULT: PASS - COMPLETE - both games`**. The
second command prints **160**. Anything else is a STOP.

**Push only after that PASS:**

```bat
git push
git rev-parse HEAD
```

## Part 8. What to send Claude

The commit ID of part 7; the window of parts 1 to 4; `%EVID%\comparison.txt`; the last twenty lines of the fill's
window and roughly how long it took; `%EVID%\second_job.txt`; `%EVID%\comparison_with_old_records.txt`; and
`%EVID%\CONVERSION_RECORD.json`. **Keep your copy (`%COPY%`) until Claude says the conversion is proved.**

## Part 9. ONLY after a STOP, and only on your own go: the whole folder put back from your copy

Nothing was pushed, so GitHub is as it was. Close every program that has a file of the project open. The stopped
folder is kept beside the project under another name, for the diagnosis; it is not deleted here.

```bat
cd /d E:\SOFTWARE-Win11\powerball
ren analysing_perceived_randomness_in_reality analysing_perceived_randomness_in_reality_STOPPED
robocopy "%COPY%" "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality" /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NFL /NDL /NP
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
%PY% -I -B "%PKG%\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase copy --copy "%COPY%"
git status --short
```

Expected: `ren` prints nothing (if it says the folder is in use, a program still holds a file: close it and give
the same line again); robocopy shows **0** under `FAILED`; **`COPY PASS`**; and `git status --short` prints nothing.
DEV is then exactly as it was before part 2. Send Claude the window, and keep `%EVID%` and the `_STOPPED` folder.
