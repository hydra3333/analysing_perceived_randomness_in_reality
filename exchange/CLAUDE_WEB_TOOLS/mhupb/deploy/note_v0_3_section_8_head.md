## 8. Restore (D10; decision log entries 100, 110, 112 and 113; EX_244; EX_248 B01, B02; EX_250 R3-C01, R3-C02)

`restore --snapshot <zip>`, run from an unpacked recovery kit (section 4.7) with whatever Python is installed, on the
owner's own go each time. **It asks nothing of the damaged tree and nothing of E:.** It does not run `check`, does not
use production's Python, reads no file of the E: clone, and does not need any file of the old tree to be readable.

**What it requires (all of these, and nothing else):**

1. The owner's go: the command typed by him, naming the snapshot.
2. The kit's own check (section 4.7), and the snapshot verified in full, every member against its list, before
   anything is touched.
3. **No Python program running on the PC, apart from the restore tool itself** (the owner's decision, entry 113).
   The tool reads Windows' own process table with the standard library and lists every process named `python*.exe`,
   `pythonw*.exe` or `py.exe` outside its own chain. Any one listed, or a table that cannot be read completely, is a
   refusal. It needs no path on G: or E: and no extra package, so it cannot be misled by a damaged tree. It is made
   twice: before the rename, and again straight after it, before anything is unpacked. Nothing is terminated, and no
   acknowledgement stands in for it: the owner closes what is listed, and the restore waits. (Windows' own refusal to
   rename a folder with a file open in it remains as a second barrier.)
4. Only if an orphan marker is found: the condition under "A stale orphan marker" below.

**What it does, in order:**

1. **Looks at the old tree, best effort, for the record only:** locks and barriers left behind; an orphan marker;
   whether each game's weekly folder holds an OV-1 registration. Whatever cannot be read is recorded as "could not be
   read". Nothing found here stops the restore, except the orphan marker's condition.
2. **Renames the old folder** to `G:\a_p_r_i_r_SET_ASIDE_<YYYYMMDD>_<HHMMSS>`: one rename, nothing copied, nothing
   deleted. If the old folder is absent, this step is skipped. If Windows refuses (a file inside is open, or the
   disk is failing), nothing has changed and the tool says what it met. Then the production marker inside the
   set-aside tree, if there is one, is renamed, so no launcher runs there. Then the second process check.
3. **Makes a fresh, empty `G:\a_p_r_i_r`,** writes `RESTORE_IN_PROGRESS.json` in it first, and unpacks **every**
   member, the environment included, hashing each file against the list as it is written. Nothing is merged,
   skipped or rebuilt. An orphan marker inside the snapshot is the one member not unpacked to its place (below).
4. **Writes the restore record** `production_records\RESTORE_<date>_<time>.json` (create-only: the snapshot's name,
   SHA-256 and time; the kit used; the set-aside tree's name; what step 1 found; the times) **and the two restore
   notices** of section 9.
5. **Verifies the whole fresh tree again:** every file against the list, nothing missing and nothing extra, and the
   code against the hash list of its release, which the snapshot itself carries.
6. **Writes the production marker last** and removes `RESTORE_IN_PROGRESS.json`.
7. **A short health check:** it starts the restored environment's own Python once, has it import the third-party
   modules the project uses, and compares the installed distributions with `ENVIRONMENT_VERIFIED.json`. Pass:
   **RESTORED AND READY TO RUN.** Fail: **RESTORED; ENVIRONMENT NOT READY** (the files are all back and verified, but
   this PC's Python is not what it was when the snapshot was taken): the launchers will refuse by themselves, and the
   way forward is the owner's rebuild and `update` (section 6). The tool never says "ready" in that case.
8. No snapshot is taken: the restored tree is the snapshot just read.

**If it stops half-way,** the same command again. A fresh tree still holding `RESTORE_IN_PROGRESS.json` is itself
renamed aside (`..._PARTIAL_RESTORE_...`) and the unpacking starts again. The first set-aside tree is never touched
again by any run.

**The last resort, in the owner's words: "a simple unzip by the human into the right place gets it done".** A
snapshot is an ordinary zip, so with no tool at all the owner can rename the old folder and extract the snapshot to
`G:\a_p_r_i_r` in File Explorer. That skips the process check, the verification, the restore record and the restore
notices. So `HOW_TO_RESTORE.txt` says: first close everything that uses Python; afterwards, as soon as a kit can be
run, `Restore_Production.bat --after-hand-unzip --snapshot <zip>`, which verifies the tree against that snapshot's
list and writes the restore record and the notices (with the time of that moment). Until that is done the formal
OV-1 check of section 9 cannot know a restore happened; ordinary work is unaffected either way.

