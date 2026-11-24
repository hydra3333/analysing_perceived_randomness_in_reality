# FILE_FORM_Conversion_v1 - the conversion of DEV to the project's file-form standard (doc/FILE_FORM_STANDARD_v0_2.md, RAT-49): install and run sheet

**Only after the owner's own go for each part.** Windows CMD, in the repository root
(`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`). **Nothing of the project running:** no
research job, no results update, no runner task, no editor holding a file of the project open.
**Save the ZIP to `E:\TEMP`, not into the repository,** delete any earlier `E:\TEMP\FILE_FORM_Conversion_v1` folder, and
extract it **to `E:\TEMP`** (the ZIP holds its own top folder), so that
`E:\TEMP\FILE_FORM_Conversion_v1\VERIFY_FILE_FORM_INSTALL.py` exists. Built against commit `@@BASE@@`.

**What this package does.** It brings every text file of the living project in DEV to the Windows form (each line
ending CRLF), and makes Git store exactly what is on disk.
- It copies in @@OVERLAY_COUNT@@ files of its own, already in that form: @@NEW_COUNT@@ new (the standard's rule
  `deploy\file_form.py`, the engine's helper `src\research\windows_text.py`, two test modules) and @@MODIFIED_COUNT@@
  replaced (four engine modules whose writers now write CRLF; two lines of the old two-site checker's self-test;
  `deploy\INFRA_MANIFEST.ini`; `.gitattributes`; `.gitignore`).
- Its conversion program changes the line endings, and nothing else, of the other listed files
  (@@LIST_COUNT@@ on the list in all), and of this PC's `ENVIRONMENT.ini`.
- **It removes DEV's research results (`results\research\`) and the status file in each variant folder,** on your
  second typed word: they are made again by the fill in part 6, in the new form.
- Its second program stages the converted files in Git and puts the working copies of the documents back to
  Git's own bytes.
- **It does not touch:** the results masters and their ledgers (it proves them unchanged), the updater's grabs and
  backups, the old system's records under `results\`, the six files of the retired Mode H machinery, `.venv`,
  `GAIS\`, or anything under `transitory_data\` except that tracked files there are put back to Git's own bytes.
  No calculation is changed.

**A STOP is a STOP.** If any step prints `STOP`, `FAIL`, `REFUSED`, an error, or anything other than what is
expected: do not go on, do not retry, do not reset or undo anything. Send Claude the whole output.
**The one exception** is the test suite's own report of the failures that exist today: the word `FAILED` on a
module's line in part 5, and the lines `FAILS IN BOTH RUNS`, are expected for as long as the comparison ends as
part 5 says.

**There is no undo. The one way back is your own copy of the project folder (part 1).** If a part stops and Claude
cannot say how to go on, the project folder is put back from that copy, whole.

Nothing here contacts a lottery website, changes the PC's date or time, or ends a process. Parts 1 to 5 and 7
run no research fill; part 6, on its own go, is the fill.

## Part 1. Update, your own copy, and the suite as it is today

```bat
git status --short
git pull --ff-only
git status --short
```

Expected: both `git status --short` print nothing; the pull says `Fast-forward` or `Already up to date`.

**Now make your own copy of the whole project folder,** as before build step 1: a ZIP of it, or a copy of the
folder, somewhere outside the project folder. It must hold `src`, `tests`, `deploy`, `source_data`,
`results\research` and `ENVIRONMENT.ini`. **Wherever this sheet says `COPY`, type its full path** (the ZIP file, or
the copied folder that holds `src`).

**The baseline suite.** If the folder `E:\TEMP\STEP2_evidence\suite_after` still exists (the suite run after build
step 2, made on exactly today's `src` and `tests`), it is the baseline: skip the next command. **Otherwise** make
it now (about 25 minutes):

```bat
.venv\Scripts\python.exe -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\run_suite.py" . "E:\TEMP\FILE_FORM_evidence\suite_before"
git status --short
```

Expected: a last line `DONE: 52 modules, 762 tests ran`; `git status --short` prints nothing.

## Part 2. Check, copy, check (about a minute)

```bat
.venv\Scripts\python.exe -I -B "E:\TEMP\FILE_FORM_Conversion_v1\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase pre
xcopy "E:\TEMP\FILE_FORM_Conversion_v1\repo_overlay\*" . /E /H /Y
.venv\Scripts\python.exe -I -B "E:\TEMP\FILE_FORM_Conversion_v1\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase post
```

Expected: `PRE PASS`; `@@OVERLAY_COUNT@@ File(s) copied`; `POST PASS`.

## Part 3. Look, then convert (a few minutes)

First the look, which changes nothing:

```bat
.venv\Scripts\python.exe -I -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\convert_to_file_form.py" --tree . --list "E:\TEMP\FILE_FORM_Conversion_v1\CONVERSION_LIST.json" --look
```

Expected: the second line names the list's SHA-256 `@@LIST_SHA@@`; the line
`IN NO CLASS, OR NOT AS EXPECTED ........ 0`; no line `THE PACKAGE'S OWN FILES, not yet here`; and the last line
`FILE-FORM CONVERSION - END - LOOKED ONLY; nothing was changed. A real run would find nothing to stop it.`
(The counts of files to convert and to remove are what your tree holds; on 24 November they were 650 and 1,578.)

Then the conversion. **Type the path of your copy in place of `COPY`:**

```bat
.venv\Scripts\python.exe -I -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\convert_to_file_form.py" --tree . --list "E:\TEMP\FILE_FORM_Conversion_v1\CONVERSION_LIST.json" --copy "COPY" --record "E:\TEMP\FILE_FORM_evidence\CONVERSION_RECORD.json"
```

It prints what it found, class by class, as the look did; then a line saying that your copy holds every file to
be converted and to be removed; then it asks. **Type `CONVERT`** and press Enter. It converts, then asks again.
**Type `REMOVE`** and press Enter.

Expected, at the end: a line beginning `PROVED: all @@LIST_COUNT@@ listed files have the list's "after" SHA-256`, and
the last line `FILE-FORM CONVERSION - END - FINISHED. Go on with the next part of the sheet.`
If it stops part-way (Windows refuses a file that another program holds open), close that program and run the
same command again: it goes on from where it stopped, and checks your copy against what it recorded the first
time. If a line names a lock file, do nothing about the lock: tell Claude.

## Part 4. Stage in Git, and put the documents' working copies back (a minute or two)

First the look, which changes nothing:

```bat
.venv\Scripts\python.exe -I -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\stage_and_refresh.py" --tree . --list "E:\TEMP\FILE_FORM_Conversion_v1\CONVERSION_LIST.json" --look
```

Expected: `TO BE STAGED, exactly as on disk ....... @@STAGED_COUNT@@ of the @@LIST_COUNT@@ listed file(s)`; a count of working
copies to be put back (some two thousand, most of them under `exchange`); `NOT AS EXPECTED ........................ 0`;
and the last line `STAGE AND REFRESH - END - LOOKED ONLY; nothing was changed.`

Then the run:

```bat
.venv\Scripts\python.exe -I -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\stage_and_refresh.py" --tree . --list "E:\TEMP\FILE_FORM_Conversion_v1\CONVERSION_LIST.json"
git status --short | find /c /v ""
git status --short | findstr /v /b /c:"M  " /c:"A  "
```

**Type `STAGE`** and press Enter when it asks.

Expected: a line beginning `PROVED: all @@LIST_COUNT@@ listed files are staged`, and the last line
`STAGE AND REFRESH - END - FINISHED. Nothing was committed or pushed: that is the next part of the sheet.`
The first `git status` line prints **@@STAGED_COUNT@@**; the second prints **nothing** (every changed file is staged, and
nothing else is changed).

## Part 5. The suite again, and the comparison (about 30 minutes)

```bat
.venv\Scripts\python.exe -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\run_suite.py" . "E:\TEMP\FILE_FORM_evidence\suite_after"
```

Expected: a last line `DONE: 54 modules, @@TESTS_AFTER@@ tests ran`, and the two new modules `test_file_form` and
`test_research_file_form` each ending `OK`.

Then the comparison. **In the first command, type the baseline folder of part 1 in place of `BASELINE`**
(`E:\TEMP\STEP2_evidence\suite_after`, or `E:\TEMP\FILE_FORM_evidence\suite_before` if you made a new one):

```bat
.venv\Scripts\python.exe -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\compare_suite_reports.py" "BASELINE" "E:\TEMP\FILE_FORM_evidence\suite_after" > "E:\TEMP\FILE_FORM_evidence\comparison.txt"
findstr /v /b /c:"NEW: " /c:"MODULE NEW: " "E:\TEMP\FILE_FORM_evidence\comparison.txt"
find /c "NEW: " "E:\TEMP\FILE_FORM_evidence\comparison.txt"
git status --short | findstr /v /b /c:"M  " /c:"A  "
```

Expected from `findstr` (every line that is not about a new test), exactly these:
`before: 52 modules; unittest ran 762 tests; identified here: 762`;
`after: 54 modules; unittest ran @@TESTS_AFTER@@ tests; identified here: @@TESTS_AFTER@@`;
**`tests in both runs: 762; with the same result: 762`**;
three entries `FAILS IN BOTH RUNS` (the failures that exist today: `test_gitignore_lines`, with the words
`FAILURE LINES DIFFER` and its two long lines, which is expected because that test prints a set in a different
order each run; and two tests of `test_multigame_reader_contracts`);
and the last line `RESULT: DIFFERENCES FOUND - each needs an explanation`. **Here that last line is expected:** the
only differences are the 2 new test modules and their @@NEW_TESTS@@ new tests. `find /c` prints **@@NEW_LINES@@**.
The last command prints **nothing**: the suite has left no file behind and changed none.
**A STOP is any line beginning `CHANGED`, `DISAPPEARED`, `MODULE CHANGED`, `MODULE DISAPPEARED`,
`NOT ALL TESTS IDENTIFIED` or `NO SUMMARY`, a `tests in both runs` line whose two numbers differ, a count other
than @@NEW_LINES@@, or any line from the last command.**

## Part 6. Commit and check (not yet pushed), then DEV's fill - the fill only on your own separate go

```bat
git commit -m "FILE-FORM STANDARD (RAT-49): DEV converted to CRLF; the engine's writers write CRLF; Git converts nothing"
.venv\Scripts\python.exe -I -B "E:\TEMP\FILE_FORM_Conversion_v1\VERIFY_FILE_FORM_INSTALL.py" --repo . --phase committed
```

Expected: **`COMMITTED PASS`**. **If it prints `STOP`: do not push, and do not reset or undo anything.** Send Claude
the whole output. **Do not push yet.**

Then the fill (about 47 minutes; leave the window alone):

```bat
Run_Research.bat --game BOTH --no-update
```

Expected, at the end: for each game a line beginning `POWERBALL: finished. Results on file through draw` (and the
same for `OZLOTTO`), each ending `prevailing OV-1: not started; waiting for a successful results step`; no line
beginning `WARNING`; and the last line **`The job finished.`** A line with `REFUSED` or `STOPPED`, or the last line
`A STOP is a STOP: ...`, is a STOP: change nothing and send Claude the whole output. (If the window is closed or
the PC restarts part-way, the same command continues where it stopped; if it then says
`a process of this tree is running`, read what it says and ask Claude before deleting anything.)

Then the same command once more, into a file (a few minutes):

```bat
Run_Research.bat --game BOTH --no-update > "E:\TEMP\FILE_FORM_evidence\second_job.txt" 2>&1
type "E:\TEMP\FILE_FORM_evidence\second_job.txt"
git status --short
```

Expected: for each game `written: 0 forecasts, 0 scores, 0 prevailing lines, 0 eligibility draws, 0 report files`;
the last line `The job finished.`; and `git status --short` prints nothing.

## Part 7. The comparison with the old development records, and the push

```bat
.venv\Scripts\python.exe -B "E:\TEMP\FILE_FORM_Conversion_v1\tools\compare_fill_with_old_records.py" --tree . > "E:\TEMP\FILE_FORM_evidence\comparison_with_old_records.txt" 2>&1
findstr /v /e /c:" equal" "E:\TEMP\FILE_FORM_evidence\comparison_with_old_records.txt"
findstr /e /c:" equal" "E:\TEMP\FILE_FORM_evidence\comparison_with_old_records.txt" | find /c /v ""
```

It reads only. Expected from the first `findstr`, exactly seven lines, as after build step 2: for each game the
two `part 1` and `part 2` lines with **`DIFFERENT: 0`** and the line about the tracked rank ledgers ending
`not among the old forecasts compared: 0`; and the last line beginning **`RESULT: PASS - COMPLETE - both games`**. The
second command prints **160**. Anything else is a STOP: a line beginning `DIFFERENT`, a `DIFFERENT:` count above
0, `RESULT: STOP`, `RESULT: PARTIAL` or `RESULT: REFUSED`. Change nothing and send Claude the file.

**Push only after that PASS:**

```bat
git push
git rev-parse HEAD
```

## Part 8. What to send Claude

The commit ID of part 7; the whole window of parts 2, 3 and 4 (or the lines from `FILE-FORM CONVERSION - START` and
`STAGE AND REFRESH - START` to their `END` lines); the comparison's text (part 5); the last twenty lines of the
fill's window, the file `second_job.txt` and roughly how long the fill took (part 6); the file
`comparison_with_old_records.txt` (part 7); and the file `E:\TEMP\FILE_FORM_evidence\CONVERSION_RECORD.json`. Claude
then verifies the commit from GitHub: every listed file with exactly the list's "after" bytes, and no other path
changed.

**Keep your copy of part 1** until Claude says the conversion is proved.
