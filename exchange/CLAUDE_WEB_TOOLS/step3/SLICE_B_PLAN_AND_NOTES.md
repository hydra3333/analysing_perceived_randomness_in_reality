# Build step 3, slice B (backups, the recovery kit, restore): plan and working notes

**Date:** 25 November 2026. **Author:** the Claude web chat (on Fable, the owner's go: decision log entry 288).
**Status:** working notes, kept up to date as the slice is written. Not reviewed, not ratified. It authorises nothing.
**If a chat resumes or a new one starts:** read this file, then the files it names under `overlay/`, then go on from
section 4 ("Where it stands").

## 1. What governs the slice (all ratified; nothing here is a new design)

- Deployment design v0.12: section 10 (backups), 11 (the recovery kit), 12 (restore, the reconciliation after an
  unzip by hand, the orphan-marker exception), 9 (the process rules: a backup "before and after", no other Python
  process of this tree; a restore, no Python program at all on the PC, read with the standard library), 2 (where
  the files lie).
- Specification v0.6 section 14.1.
- The owner's decisions: restore is standard library only with its own reader of Windows' processes (entry 222);
  ZIP level 9 (entry 243); no monthly restore test, no replay comparison; a backup that cannot be made does not
  stop the work (a standing warning); a missing kit is a warning and a default-NO question; no program ends a
  process; nothing prunes a backup root.
- TASK_T028 (entry 240): on the owner's PC the standard library and psutil agree on the set of Python processes;
  every program started from an environment is two processes; Windows refuses a rename while a file is open; a
  level-9 ZIP of an environment alone took about 80 seconds and 180 MB.
- The working principle: the smallest thing that carries out those clauses. No repair, no resumption beyond what
  section 12 names ("the same command again"), no new record.

## 2. The parts, in the order they are written

**B1. The backup.** New `src/research/snapshot.py` (infrastructure in every tree; class `derived`, because the job
calls it, as the guard's modules are): the inventory of the tree (everything under the root but `records/SNAPSHOT_DUE`
and `records/SNAPSHOT_IN_PROGRESS.lock`; empty folders kept; a link refuses); the ZIP written as
`<backup_root>/<ROLE>_<YYYYMMDD>_<HHMMSS>_<JOB>.zip.partial`, Deflate level 9, `SNAPSHOT_MANIFEST.json` the last
member; the two verifications (the archive read back against the list; every source file read and hashed again, the
set of files unchanged); then the rename to `.zip`, the `.sha256`, one line in `records/SNAPSHOT_LOG.jsonl`, and
`SNAPSHOT_DUE` removed. Quiet by three things: the lock `records/SNAPSHOT_IN_PROGRESS.lock` (the launch guard already
refuses on it), the process rule before the first reading and after the second, and the second reading. A result is
always a plain statement: MADE AND VERIFIED, or NOT MADE with the reason; never an exception that stops a job.
`Run_Snapshot.bat` (job name `MANUAL`) through `src/research_command.py`. The research job: `SNAPSHOT_DUE` written
before its first write; a backup attempted at its end (`RESEARCH`); a job that finds `SNAPSHOT_DUE` tries the backup
first; the warning in capitals at start and end while no verified backup exists. QA and PROD only: DEV has no backup
root.

**B2. The recovery kit.** New `deploy/recovery_kit.py` (an install tool, DEV): builds
`<backup_root>/KIT_<YYYYMMDD>_<HHMMSS>_<software fingerprint>.zip` and its `.sha256` from DEV's install-tool files
as the infrastructure marker lists them; it holds the restore tool, `Restore.bat`, `HOW_TO_RESTORE.txt` and
`KIT_MANIFEST.json`. Slice C's commands call it; slice B delivers and tests the builder.

**B3. Restore.** New `deploy/restore_tool.py`: ONE file, standard library only, runnable from an unpacked kit with
any installed Python and no tree in reach. Its own reader of Windows' process table (program name, number, parent,
start time; a table that cannot be read refuses). The steps of design section 12, one function each; the same
command again after a stop; `--after-hand-unzip`; the orphan-marker exception with its four conditions.
`Restore.bat` and `HOW_TO_RESTORE.txt` beside it.

## 3. Readings taken (for the reviewer; RECOMMENDED unless marked)

1. **The software fingerprint** (design sections 2, 10, 11) is not defined by a formula in the ratified text. Taken
   as: the SHA-256 of the bytes of the tree's `records/INSTALLED_FILES.json`; its first 12 characters in a kit's file
   name, the whole of it in the manifests.
2. **The backup's modules are classed `derived`,** as the guard's are, because the research job calls them.
3. **The Windows process reader of the restore cannot be run in the cloud.** The restore takes its reader as a
   function; the tests give it invented tables; the real reader meets Windows in the joined rehearsal, where it is
   compared with psutil again. On a system that is not Windows the tool refuses unless a test supplies a reader.
4. **"No Python program at all on the PC but the restore tool":** a process counts when its program name is
   `python.exe`, `pythonw.exe` or `py.exe` (case set aside), the tool's own process and the chain above it
   excepted (an environment's python.exe is the parent of the base Python that runs the tool: TASK_T028).
5. **A backup's time in its name** is local time, as the design's `<YYYYMMDD>_<HHMMSS>` reads; the manifest holds
   the same moment in UTC as well.
6. **A backup is not made while a job or a results update holds its lock,** and the research job makes its own
   backup after it has released its lock. Otherwise `records/JOB.lock` would be inside the ZIP (nothing but the two
   control files is left out), and a restored tree would refuse every job. The backup's own lock and the process
   rule keep the tree quiet meanwhile.
7. **The job's closing lines are said after its backup,** so that its verdict ("The job finished." or "A STOP is a
   STOP ...") is still the last thing the owner reads, and the standing warning stands just above the job's END
   line. For this `run_locked` returns its closing lines instead of saying them (one small change to build step
   2's reviewed job; no step 2 test changed).
8. **`PRE_CORRECTION`** is accepted as a backup's job name with the twelve of design section 10: section 6C of the
   same design uses it.
9. **`Run_Snapshot.bat` passes the launch guard's refusal on a backup's own lock** (it is the command that speaks
   for that lock) and then says what it found: a backup in progress, or a lock left by one that was ended, which
   the owner deletes by hand when he is sure. Nothing clears it for him.
11. **A restore asks for no typed confirmation of its own** beyond the orphan marker's sentence: the ratified
    section 12 names none, the command with `--snapshot` is the owner's explicit act, and the old tree is renamed
    aside, never deleted.
12. **The old tree's settings file is renamed `ENVIRONMENT.ini.SET_ASIDE`** inside the tree that was set aside
    ("its settings file is renamed too, so no launcher runs there").
13. **When the PC was last started** (the orphan exception, part b) is read from Windows' count of milliseconds
    since its start; an orphan marker's time is its file's time in the old tree, and its member's time in the
    backup (to two seconds).
14. **Which third-party modules the restored environment is asked to import:** `numpy` and `psutil`, the two the
    project's installed programs import.
15. **A member's name is checked to lie inside the tree** before anything is unpacked (no `..`, no drive, no
    leading slash). The ratified text does not ask for it; it is three lines against writing outside the tree
    from a damaged or foreign ZIP. Say if it is more than is wanted.
10. **A failed attempt removes its own ".partial"** if it can; one left by a backup that was ended is never taken
    for a backup and nothing removes it (nothing prunes a backup root).

## 4. Where it stands

- 25 November 2026: the ratified clauses read; this plan written.
- **B1 (the backup) is written, with its tests:** `overlay/src/research/snapshot.py`, `overlay/Run_Snapshot.bat`,
  `overlay/tests/test_trees_snapshot.py` (23 tests); wired into `research_job.py` (the note before the first write;
  a backup at the start if one is owed, and at the end), `research_command.py` (the command `snapshot`) and the
  manifest (two lines). One existing test of slice A adjusted for the launcher's new line. In the cloud:
  `test_trees_snapshot`, `test_trees_launch_guard`, `test_research_job` and the other slice modules OK.
- **The whole suite with B1** (a fresh clone, the cloud): 60 modules, 1023 tests. Against slice A as it passed
  review: 1000 tests in both runs, 999 with the same result, 23 new (the backup's), and **one changed to FAIL:**
  `test_file_form` `test_no_program_of_the_project_writes_a_text_file_without_naming_its_line_ending` found two
  lines of `snapshot.py` (a ZIP member opened through `.open(`, which the project's rule reads as a path's text
  open). **Corrected, not waived:** the ZIP is now written with the library's own streaming `write` (each file is
  hashed, then written; the read-back check catches a change between the two) and a member is read back with
  `mode='r'` written out. `test_trees_snapshot` (23) and `test_file_form` (52) rerun: OK. **The whole suite has not
  been run again since that correction; it is run again before the slice goes to review.** The three known
  failing tests are as before.
- **B2 (the recovery kit) and B3 (restore) are written, with their tests:** `overlay/deploy/recovery_kit.py`,
  `overlay/deploy/restore_tool.py` (one file, standard library only; its own reader of Windows' process table),
  `overlay/deploy/kit/Restore.bat`, `overlay/deploy/kit/HOW_TO_RESTORE.txt`, `overlay/tests/test_trees_restore.py`
  (29 tests); four lines added to the manifest's `[install_tool]`. `snapshot.py` also refuses a backup while a
  backup's manifest lies at the tree's root (a tree unzipped by hand and not yet reconciled: design section 12).
  In the cloud `test_trees_restore` (29) and `test_trees_snapshot` (23) are OK.
- **Still to do for the slice:** the whole suite and its comparison; planted faults for B1, B2 and B3; a last read
  of every new file against design sections 10 to 12; then the package note, the exact differences of the files
  slice A's review passed, and the evidence, as for slice A. Then it is put to the owner for the reviewer.

## 5. Costs on the owner's PC, to be told plainly when the slice is put to him

- Every research job in QA and PROD ends with a whole backup of its tree: two full readings of the tree and a
  level-9 ZIP. From TASK_T028's figures for an environment alone this is minutes, not seconds, and about 180 MB or
  more each time; nothing prunes the backup root (his decision), so it grows until he copies and clears it.
- A restore needs every Python program on the PC closed, Claude Code's among them.
