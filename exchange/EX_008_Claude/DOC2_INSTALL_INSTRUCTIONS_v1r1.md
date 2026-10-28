# DOC-2 - installation, r1 (instructions only changed: the commit is checked before it is pushed)

Windows CMD, repository root. `git status --short` must print nothing first. Delete any earlier extracted `E:\TEMP\DOC2_*` folders, then save this ZIP to `E:\TEMP` and extract it there (`tar -xf "E:\TEMP\DOC2_Install_v1r1.zip" -C E:\TEMP`).

```bat
python "E:\TEMP\DOC2_Install_v1r1\VERIFY_DOC2_INSTALL.py" --repo . --phase pre
xcopy "E:\TEMP\DOC2_Install_v1r1\repo_overlay\*" . /E /Y
python "E:\TEMP\DOC2_Install_v1r1\VERIFY_DOC2_INSTALL.py" --repo . --phase post
call "E:\TEMP\DOC2_Install_v1r1\STAGE_EXACT_FILES.cmd"
git diff --cached --name-status
```

Expected: `PRE PASS`; `8 File(s) copied` (all new; nothing is replaced or deleted); `POST PASS`; 8 lines starting with `A`.

```bat
git commit -m "DOC-2: E2R-1 specification v0.3r3 (ratified) and register v0.7"
python "E:\TEMP\DOC2_Install_v1r1\VERIFY_DOC2_INSTALL.py" --repo . --phase committed
```

Expected: `COMMITTED PASS`. **Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID. If the committed check prints `STOP`, do **not** push: send Claude the output (the commit is still only on your PC; `git reset --hard HEAD~1` removes it). If anything else prints `STOP`, stop and send Claude the output. No test run is needed: no code changes.
