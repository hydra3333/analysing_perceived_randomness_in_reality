**Words used below.** A snapshot's **payload** is every member of the archive except `SNAPSHOT_MANIFEST.json`. The
manifest is the archive's own list; the tool reads it and never unpacks it into production. Two payload members are
handled by name: the production marker `PRODUCTION_ROOT.json` (written last) and an orphan marker, if the snapshot
holds one (never unpacked to its live place; see below).

**What it does, in order:**

1. **Looks at the old tree, best effort, for the record only:** locks and barriers left behind; an orphan marker.
   Whatever cannot be read is recorded as "could not be read". Nothing found here stops the restore, except the orphan
   marker's condition.
2. **Renames the old folder** to `G:\a_p_r_i_r_SET_ASIDE_<YYYYMMDD>_<HHMMSS>`: one rename, nothing copied, nothing
   deleted. If the old folder is absent, this step is skipped. If Windows refuses (a file inside is open, or the
   disk is failing), nothing has changed and the tool says what it met. Then the production marker inside the
   set-aside tree, if there is one, is renamed, so no launcher runs there. Then the second process check.
3. **Makes a fresh, empty `G:\a_p_r_i_r`,** writes `RESTORE_IN_PROGRESS.json` in it first, and unpacks every payload
   member except the two handled by name, hashing each file against the list as it is written. Nothing is merged,
   skipped or rebuilt.
4. **Verifies the payload, exactly** (EX_252 R3-D01). Every file now in the fresh tree is read again and must equal
   the list, and the set of files and empty folders must be exactly: the payload, less the production marker, less the
   orphan marker if there is one, plus `RESTORE_IN_PROGRESS.json`. One file missing, extra or different refuses. The
   code is also checked against the hash list of its release, which the snapshot itself carries.
5. **Adds what a restore adds, each by name, and nothing else:** the restore record
   `production_records\RESTORE_<date>_<time>.json` (create-only: the snapshot's name, SHA-256 and time; the kit used;
   the set-aside tree's name; what step 1 found; the times); and, only if the snapshot held an orphan marker, its
   bytes at `production_records\RESTORE_<date>_<time>_ORPHAN_MARKER.json`.
6. **Writes the production marker last,** from the snapshot's own bytes, checked against the list, and removes
   `RESTORE_IN_PROGRESS.json`. A last listing confirms the tree is exactly: **the payload, plus the restore record,
   plus the orphan evidence file if any, less the live orphan marker if any.** That sentence is the whole allowed
   difference, and the tests show the check passing on a correct restore.
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
snapshot is an ordinary zip, so with no tool at all the owner can restore in File Explorer. `HOW_TO_RESTORE.txt` says,
in this order: close everything that uses Python; rename the old folder; make a new **empty** folder at the **same
path**, `G:\a_p_r_i_r`; extract the snapshot into it. What that leaves, stated truthfully:
- Nothing was checked: not the processes, not the files.
- `SNAPSHOT_MANIFEST.json` now sits at production's root. While it is there no new snapshot is made (the name is the
  archive's own), and every job says so in its standing snapshot warning.
- **If the snapshot held an orphan marker it is now live, and it blocks every launch as it always does.** Nothing
  bypasses it: the owner's ordinary clearance applies.
- `Restore_Production.bat --after-hand-unzip --snapshot <zip>` puts this right when a kit can be run: the same process
  check; every file against that snapshot's list, exactly the payload plus the manifest; then the restore record, in
  which the time is labelled **"reconciliation recorded at"**, never as the time of the unzip, which the tool cannot
  know; and the manifest is moved beside the record. It changes no other file.
- It has no bearing on OV-1 or on any research result (section 9). Its only purposes are the check of the files and
  the next snapshot.

