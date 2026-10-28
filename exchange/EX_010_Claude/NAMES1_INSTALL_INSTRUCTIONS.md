# NAMES-1 - code installation (only after the reviewer's code RECHECK PASS and the owner's go-ahead)

DOC-2 must already be installed. Windows CMD, repository root. `git status --short` must print nothing first. Delete any earlier extracted `E:\TEMP\NAMES1_*` folders, then save this ZIP to `E:\TEMP` and extract it there (`tar -xf "E:\TEMP\NAMES1_Code_Install_v1.zip" -C E:\TEMP`).

## 1. Check, rename, copy, check

```bat
python "E:\TEMP\NAMES1_Code_Install_v1\VERIFY_NAMES1_INSTALL.py" --repo . --phase pre
call "E:\TEMP\NAMES1_Code_Install_v1\RENAME_FILES.cmd"
xcopy "E:\TEMP\NAMES1_Code_Install_v1\repo_overlay\*" . /E /Y
python "E:\TEMP\NAMES1_Code_Install_v1\VERIFY_NAMES1_INSTALL.py" --repo . --phase post
```

Expected: `PRE PASS`; `RENAMES DONE`; `41 File(s) copied` (27 replace renamed or existing files, as intended; 14 are new); `POST PASS`.

## 2. Tests and import checks (offline; nothing is changed)

```bat
.venv\Scripts\python.exe "E:\TEMP\NAMES1_Code_Install_v1\RUN_NAMES1_SUITE.py" --repo .
.venv\Scripts\python.exe "E:\TEMP\NAMES1_Code_Install_v1\CHECK_NAMES1_IMPORTS.py" --repo .
```

Expected: `SUITE PASS` (79 tests; the only allowed skips are the two symlink tests, if Windows cannot create symlinks), then `RESULT PASS`. Send Claude both outputs whatever they say. If either says `STOP`, do not commit: to undo, run `git reset --hard` and then `git clean -fd -- doc review`, which puts the repository back exactly as it was.

## 3. Stage, commit, check, and only then push

```bat
call "E:\TEMP\NAMES1_Code_Install_v1\STAGE_EXACT_FILES.cmd"
git diff --cached --name-status
git commit -m "NAMES-1: one-off rename to stable file names; NAMES-1 v0.2 (ratified) and register v0.8"
python "E:\TEMP\NAMES1_Code_Install_v1\VERIFY_NAMES1_INSTALL.py" --repo . --phase committed
```

Expected: the staged list shows renames (`R`) and modifications (`M`), and 14 lines starting with `A`; then `COMMITTED PASS`. **Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID. Claude then verifies it from GitHub and runs the immediate recovery check (N1-T10) in a disposable clone. If the committed check prints `STOP`, do **not** push: send Claude the output (the commit is still only on your PC; `git reset --hard HEAD~1` removes it). If anything else prints `STOP`, stop and send Claude the output.
