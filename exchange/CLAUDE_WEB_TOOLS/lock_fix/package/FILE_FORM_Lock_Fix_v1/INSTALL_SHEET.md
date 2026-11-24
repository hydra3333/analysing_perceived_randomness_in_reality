# FILE_FORM_Lock_Fix_v1 - the lock file's one line ends CRLF on Windows: install sheet

**Only after the conversion's commit is pushed, and on the owner's own go.** One file of one line's change. It
corrects the one new test that fails on Windows after the conversion
(`test_research_file_form ... test_a_lock_file_is_one_line_ending_crlf`): `src\research\job_lock.py` opened the lock
file without the Windows flag for binary mode, so Windows added a carriage return of its own and the line ended
CR CR LF. The lock is taken and refused exactly as before; only the bytes of its one line change. No result,
forecast, score or report is touched, and no rebuild is needed: the engine records the digest of this code in new
lines and never compares it in old ones.

**A STOP is a STOP:** anything other than what is expected: stop, change nothing, send Claude the window.
Nothing of the project running. Windows CMD, in the repository root.

## Part 1. Update and unpack

```bat
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
set PY=.venv\Scripts\python.exe
git status --short
git pull --ff-only
git status --short
certutil -hashfile exchange\CLAUDE_WEB_TOOLS\lock_fix\package\FILE_FORM_Lock_Fix_v1.zip SHA256
if exist "E:\TEMP\FILE_FORM_Lock_Fix_v1" echo STOP: E:\TEMP\FILE_FORM_Lock_Fix_v1 exists already
%PY% -I -m zipfile -e exchange\CLAUDE_WEB_TOOLS\lock_fix\package\FILE_FORM_Lock_Fix_v1.zip E:\TEMP
```

Expected: both `git status --short` print nothing; `certutil` prints the SHA-256 Claude gave you in the chat for
`FILE_FORM_Lock_Fix_v1.zip`; the `if exist` line prints nothing.

## Part 2. Check, copy the one file, check

```bat
certutil -hashfile src\research\job_lock.py SHA256
copy /Y "E:\TEMP\FILE_FORM_Lock_Fix_v1\repo_overlay\src\research\job_lock.py" src\research\job_lock.py
certutil -hashfile src\research\job_lock.py SHA256
git status --short
```

Expected: the first hash is `fadb1785ff2703249b132bf555e4bf2a7311565a1914492dbfdb7585870ba6a7` (the file as the conversion committed it; **if it is anything else, do
not give the `copy` line**); `1 file(s) copied.`; the second hash is `efe8419e5927d87207fc39de0b97519c86b0b4a01f533b5751b6a6f54bc7853f`; and `git status --short` prints
exactly ` M src/research/job_lock.py`.

## Part 3. The affected tests (a minute or two)

```bat
set PYTHONPATH=src;src\methods;tests
%PY% -B -m unittest test_research_file_form test_research_job test_file_form
set PYTHONPATH=
git status --short
```

Expected: `Ran 116 tests`, and a last line beginning **`OK`** (with some skipped). No `FAILED`. `git status --short`
prints the same one line as before.

## Part 4. Commit and push

```bat
git add src/research/job_lock.py
git commit -m "The lock file's one line ends CRLF on Windows (O_BINARY in job_lock.py); the new lock-file test passes"
git push
git rev-parse HEAD
```

Send Claude the window and the commit ID. The next research job needs nothing special: it writes no forecast and
no score again for this change.
