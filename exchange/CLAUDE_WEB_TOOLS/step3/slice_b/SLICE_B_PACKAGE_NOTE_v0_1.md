# Build step 3, slice B (backups, the recovery kit, restore): the package note for review - v0.1

**Date:** 25 November 2026. **Author:** the Claude web chat (on Fable; the owner's go, decision log entry 288).
**Reviewer:** the ChatGPT reviewer chat. **Status:** for independent review. Not reviewed, not ratified, nothing
installed. It authorises nothing.

## 0. The work-item card

| | |
|---|---|
| Item | Build step 3, slice B: backups, the recovery kit, restore (build plan v0.1r1 section 4) |
| Author; reviewer | Claude; ChatGPT |
| Base | slice A as it passed review (EX_321): the overlay at `32086ba`. The slice is the same overlay, `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, at `main` `716bc394a4249227677f72b5e75ebae5a04e81a3`: 34 files, laid out as they go into the tree |
| Scope | a verified ZIP of a whole tree; the note that a backup is owed; the research job's two backups; `Run_Snapshot.bat`; the recovery kit's builder; the restore tool with its launcher and instructions, the reconciliation after an unzip by hand, and the orphan-marker exception |
| Not in scope | the commands that ask for a kit or a backup around an install (slice C); the updater (slice D); anything on Windows |
| Governing text | deployment design v0.12 sections 10, 11, 12, 9 and 2; specification v0.6 section 14.1. **No new design:** every reading taken where that text leaves a detail open is in section 4 |
| Risk tier | HIGH: whole-tree backups and an exact restore; the rename of a tree; the orphan-marker exception; a process rule |
| Owner gate | the owner's go for build step 3's design and cloud coding (entry 217) and for this slice (entry 288). **No install, run, tree, backup, restore or runner task is authorised** |

## 1. The files

**New, 8 files:**

- `Run_Snapshot.bat`
- `deploy/kit/HOW_TO_RESTORE.txt`
- `deploy/kit/Restore.bat`
- `deploy/recovery_kit.py`
- `deploy/restore_tool.py`
- `src/research/snapshot.py`
- `tests/test_trees_restore.py`
- `tests/test_trees_snapshot.py`

**Changed, 4 files that slice A's review passed** (their exact differences, 12 hunks, are in
`SLICE_B_CHANGED_FILES_FROM_SLICE_A_AS_REVIEWED_DIFFERENCE.txt` beside this note):

| File | Lines added | Lines removed | Hunks |
|---|---|---|---|
| `deploy/INFRA_MANIFEST.ini` | 6 | 0 | 2 |
| `src/research/research_job.py` | 18 | 10 | 5 |
| `src/research_command.py` | 8 | 3 | 4 |
| `tests/test_trees_launch_guard.py` | 3 | 2 | 1 |

- `research_job.py`: the note that a backup is owed is written before the job's first write; a backup is tried at
  the start if one is owed and made at the end, after the job's lock is released; `run_locked` now returns its
  closing lines, which `run` says after the backup, so that the job's verdict is still the last line.
- `research_command.py`: the command `snapshot` (`Run_Snapshot.bat`); the backup command alone passes the guard's
  refusal on a backup's own lock, and then says what it found there.
- `INFRA_MANIFEST.ini`: `src/research/snapshot.py = derived` and `Run_Snapshot.bat = other` under `[files]`; the
  kit's builder, the restore tool and the kit's two files under `[install_tool]`.
- `tests/test_trees_launch_guard.py`: one test of the launcher's text follows its new line and names the new
  command. No other test of slice A or of build step 2 is changed.

Forecast-class files: none changed, none added. The forecasting-code identity is unchanged; no rebuild follows.

## 2. Where each ratified clause is carried out, and what proves it

| Clause (deployment design v0.12) | Where | Tests |
|---|---|---|
| 10: everything under the root but the two control files; empty folders; a link fails the backup | `snapshot._inventory` | `AVerifiedBackup` (unpacked, byte for byte); `ABackupIsOnlyOfAQuietTree` (a link) |
| 10: zipfile, Deflate level 9, `.zip.partial`, the manifest the last member, with the time, role, root, software fingerprint and kit's name | `snapshot._write_archive`, `attempt_snapshot` | `AVerifiedBackup` (the manifest; the kit named) |
| 10: verified means both: the archive read back; every source read and hashed again, the set unchanged | `_check_archive`, `_check_sources_again` | `ABackupIsOnlyOfAQuietTree` (changed, added, removed; an archive that does not read back) |
| 10: only then the name, the `.sha256`, the log line, `SNAPSHOT_DUE` removed; a `.partial` is never a backup | `attempt_snapshot` | `AVerifiedBackup`; every failing case leaves no ZIP, no `.partial`, no lock |
| 10, 9: quiet by the lock, the process rule before the first reading and after the second, and the second reading | `attempt_snapshot` | the lock; the rule asked twice; refused at either call |
| 10: names `<ROLE>_<date>_<time>_<JOB>.zip` | `attempt_snapshot`, `JOBS` | `AVerifiedBackup` |
| 10, spec 14.1: `SNAPSHOT_DUE` before a job's first write; a job that finds it tries first; if no backup can be made the job goes on with a warning in capitals at start and end | `mark_due`, `backup_for_a_job`, `research_job.run` | `TheResearchJobsBackups` |
| 10: `Run_Snapshot.bat` at any time, made only if the tree is quiet | `snapshot.main`, `research_command.py` | `TheCommandRunSnapshot` |
| 11: the kit: the tool, `Restore.bat`, `HOW_TO_RESTORE.txt`, `KIT_MANIFEST.json`; built from DEV's install-tool files as the infrastructure marker lists them; its `.sha256` | `recovery_kit.build_kit` | `TheRecoveryKit` |
| 11: the tool checks its own files against the manifest before doing anything; standard library only | `restore_tool.check_kit` | `TheRecoveryKit` (a damaged kit; the imports) |
| 12: the destination is the tree root named inside the backup; the backup verified in full before anything is touched | `read_backup`, `restore` | `NothingIsTouchedUnless` |
| 9, 12: no Python program at all on the PC but the tool, before the rename and after; a table that cannot be read refuses | `other_python_programs`, `check_no_other_python`, `read_windows_processes` | `NothingIsTouchedUnless`; `StoppedPartWay` |
| 12 steps 1 and 2: the old tree looked at for the record; one rename, its settings file renamed too | `look_at_old_tree`, `restore` | `ARestore` |
| 12 steps 3 to 6: the progress file first; the payload but the settings file and an orphan marker; read back; the record and the evidence; the settings file last | `unpack` | `ARestore`; `StoppedPartWay` |
| 12 step 7: READY only if the restored Python starts and imports | `environment_starts`, `restore` | `ARestore` |
| 12: stopped half-way, the same command again; an unfinished fresh tree renamed aside first | `restore` | `StoppedPartWay` |
| 12: by hand, then `--after-hand-unzip`; no new backup while the manifest lies at the root | `reconcile_after_hand_unzip`; `snapshot.attempt_snapshot` | `AfterAnUnzipByHand` |
| 12: the orphan-marker exception, parts (a) to (d), none waived | `check_orphan_condition` | `AStaleOrphanMarker` |
| No program ends a process | every file | `TheRecoveryKit` (no such call in the tool) |

## 3. What the owner is told plainly

- Every research job in QA and PROD ends with a whole backup of its tree: three readings of the tree and a level-9
  ZIP. From TASK_T028's figures for an environment alone that is minutes, and about 180 MB or more each time.
  Nothing prunes the backup root (his decision).
- A restore needs every other Python program on the PC closed, Claude Code among them, and every window out of
  the tree's folder (Windows will not rename a folder in use).

## 4. The readings taken where the ratified text leaves a detail open (RECOMMENDED; yours and the owner's to accept or change)

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
10. **A failed attempt removes its own ".partial"** if it can; one left by a backup that was ended is never taken
    for a backup and nothing removes it (nothing prunes a backup root).
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

One more, which the suite forced: **each file is read three times, not twice** (hashed; written into the ZIP by the
library's streaming `write`; hashed again for the second verification). The project's own rule against opening a
file without naming its line ending reads a ZIP member's `.open(` as a path's; writing through `.write` meets the
rule without changing the checker. The read-back check catches a file that changed between its hashing and its
writing.

## 5. The evidence (the cloud: Linux, Python 3.15.0b4; Claude's, not Windows' and not the reviewer's)

All in `evidence/` beside this note.

- **The whole suite** in a fresh clone of `main` with the overlay: **61 modules, 1055 tests**
  (`SUITE_WITH_SLICES_A_AND_B_MODULES.txt`).
- **Against slice A as it passed review:** 1000 tests in both runs, every one with the same result; 55 new (23 of
  the backup, 32 of the kit and the restore), all OK (`SUITE_COMPARISON_SLICE_A_AS_REVIEWED_TO_SLICES_A_AND_B.txt`).
- **Against `main`:** 829 of 830 with the same result (one removed in slice A), 226 new; the three known failing
  tests (eight failed assertions) and no other (`SUITE_COMPARISON_MAIN_TO_SLICES_A_AND_B.txt`).
- **Planted faults** (`PLANTED_FAULTS_SLICE_B.txt`; the script is `mutation_check_slice_b.py`): 53, one at a time:
  24 in the backup and the job's wiring, 3 in the kit's builder, 26 in the restore tool. The first run caught 50;
  three survived (a kit not read back; a backup holding a member its manifest does not list; an orphan marker
  only in the old tree); three tests were added, and the run made again caught **53 of 53**.
- **One fault of mine that the project's own check found:** the first whole run failed `test_file_form` on two
  lines of `snapshot.py`; corrected as section 4's last paragraph says.

## 6. What is not tested, and where it will be

- **Nothing ran on Windows.** `read_windows_processes` and `windows_started_at` (ctypes on kernel32) cannot run in
  the cloud: every process table in the tests is invented, and on Linux the default reader refuses (a test shows
  it). They meet Windows in the joined rehearsal, where the reader is set beside psutil again (TASK_T028 showed
  the two agree on the owner's PC).
- The rename of a real tree on Windows, the restored environment's real start (`environment_starts` is shown only
  to say "not ready" of an invented environment), the kit's `Restore.bat`, and the time and size of a real
  backup: the joined rehearsal.
- No install, tree creation or kit around an install: slice C calls `build_kit` and `attempt_snapshot`.
