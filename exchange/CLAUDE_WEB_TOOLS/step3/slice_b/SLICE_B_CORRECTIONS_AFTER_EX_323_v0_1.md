# Build step 3, slice B: the corrections after EX_323, for the focused recheck - v0.1

**Date:** 25 November 2026. **Author:** the Claude web chat. **Reviewer:** the ChatGPT reviewer chat.
**Status:** for the focused recheck EX_323 asks for. Not reviewed, not ratified, nothing installed. It authorises
nothing. It is read with the slice's package note (`SLICE_B_PACKAGE_NOTE_v0_1.md`, the note EX_323 reviewed), which
is left as it was reviewed; where the two differ, this note is the later one.

## 1. What this is

EX_323 (`exchange/EX_323_ChatGPT.md`, decision log entry 293) accepted the slice's design and asked for four
blockers (B-B01 to B-B04) and three grouped corrections (B-C01 to B-C03) to be put right, narrowly. I read each
against the submitted files and found each one true; none is disputed. Nothing was redesigned and nothing was
added that EX_323 does not ask for.

The exact differences from the files you read (the overlay at `60cbfd9`, EX_322) are in
`SLICE_B_CORRECTIONS_AFTER_EX_323_DIFFERENCE.txt` beside this note (6 files, 50 hunks):

| File | Lines added | Lines removed | Hunks |
|---|---|---|---|
| `deploy/recovery_kit.py` | 11 | 8 | 2 |
| `deploy/restore_tool.py` | 190 | 58 | 20 |
| `src/research/research_job.py` | 25 | 11 | 5 |
| `src/research/snapshot.py` | 77 | 41 | 10 |
| `tests/test_trees_restore.py` | 257 | 4 | 9 |
| `tests/test_trees_snapshot.py` | 149 | 21 | 4 |

No file is added to the overlay and none removed; the manifest is unchanged. No forecast-class file is touched.

## 2. The findings, one by one

### B-B01. The backup now reads its manifest back

`snapshot.py`: `_write_archive` returns the manifest's exact bytes with the hashes; `_check_archive` compares the
manifest member read back with those bytes, and reads every empty-folder member back as empty. A ZIP that does
not decompress (`zlib.error`, `EOFError`, as well as `BadZipFile`) is BACKUP NOT MADE: the note that a backup is
owed stays and the job goes on. No third reading of the tree was added.
*Tests* (`test_trees_snapshot`, `ABackupIsOnlyOfAQuietTree`): a valid ZIP with every file right and ONLY the
manifest changed (another tree root; another hash) is not a backup; an empty-folder member that is not empty;
three kinds of read-back failure give a result, not an exception.

### B-B02. The one destination, and the kit's own list

(a) `restore_tool.py`, new `check_destination`, called by `read_backup` before anything is touched: the backup
must hold `ENVIRONMENT.ini`; the manifest's root must be the root those settings name, both full paths, for the
same role; the environment inside the tree and the backup root outside it. All from the backup's own bytes: no
DEV, no old tree, no drive letters.
(b) `check_kit` requires the manifest to list exactly the kit's three files, each once, before it checks them.
*Tests* (`NothingIsTouchedUnless`, `TheRecoveryKit`): a valid backup whose manifest names a second invented
folder is refused, and that folder is not renamed; a root that is not a full path (also when the settings inside
say the same), an empty root, another role; settings whose environment lies outside the tree or whose backup root
lies inside it; a backup without its settings file; a kit list that is empty, short, or names a file twice.

### B-B03. The process rule's two gaps

(a) `read_windows_processes` reads Windows' report at the end of the loop at once and passes it to the new
`check_table_was_read_to_its_end`: anything but "no more entries" refuses. `check_no_other_python` refuses a table
that does not hold the tool's own process. The launcher/base-Python exception and the start-time check are as
they were.
(b) `environment_starts` calls `subprocess.run` with no time limit, and says why. No watchdog replaces it.
*Tests:* a table without the tool's own process, and an empty one, refuse with nothing touched; the end-of-table
check passes only on Windows' "no more entries"; the tool's one `subprocess` call is `run` with `capture_output`
alone, and the words `timeout=`, `Popen`, `check_output`, `wait(` are not in it. The real Toolhelp calls are for
the joined rehearsal, as you say.

### B-B04. The orphan marker's evidence

`restore`: an orphan marker in the old tree is read BEFORE the tree is renamed. `unpack` keeps as the named
evidence file the backup's marker if the backup holds one, otherwise the old tree's. The record's `orphan_marker`
entry says where markers were found, whose bytes the evidence is, and where the old tree's marker now lies in the
tree set aside. If the old marker is there but cannot be read, no evidence file is claimed: the record and a
warning in capitals say so, and name the tree set aside as the only place it lies. No live marker is restored in
any case, and no condition was added to restoring over a damaged tree.
The time a ZIP keeps for the backup's marker is taken as possibly two seconds early (`ZIP_TIME_STEP`): a PC
started within that interval is not shown to have been started after the marker.
*Tests* (`AStaleOrphanMarker`): the old-only marker's bytes are in the evidence file and the record says "the old
tree" (the earlier test that asserted no evidence is corrected); both markers; an unreadable old marker; the
boundary at 0, 2 and 3 seconds after the ZIP's time.

### B-C01. Exactness of the restored tree, and the settings file

`_tree_now` raises on a folder it cannot list and returns the set of folders; `unpack` compares the fresh tree's
folders exactly with those the payload needs (new `_folders_of`); the reconciliation requires the manifest at the
root to be the chosen ZIP's own bytes and the folders to be exact. The settings file and the orphan member, read
from the archive a second time, are checked against the manifest's hashes before use; the settings file gets its
ZIP time back. What a ZIP keeps is said plainly in `snapshot.py`'s header: an empty folder by its name, without
its time; a time before 1980 as 1980.
*Tests* (`StoppedPartWay`, `ARestore`, `AfterAnUnzipByHand`): one folder more or one fewer stops the restore; a
folder that cannot be listed stops it; a settings file that reads differently the second time is not written; its
time comes back; a missing empty folder, and another manifest at the root, are refused at reconciliation.

### B-C02. This attempt's own ".partial", and a kit that is one

`snapshot.attempt_snapshot` checks for an existing ZIP or ".partial" before the block that owns and removes its
own ".partial". `_newest_kit` names a kit only if its ".sha256" lies beside it and agrees with its bytes and its
own manifest names the whole fingerprint; otherwise the backup is made all the same and names none.
`recovery_kit.build_kit` writes the ".sha256" before it gives the kit its name, so a named kit always has it, and
on failure removes only what that attempt made.
*Tests:* a ".partial" that lay there first is still there, byte for byte; of seven invented kits (finished, older,
unfinished, damaged, another state with the same twelve letters, not a ZIP, another fingerprint) the newest
finished one of the tree's state is named; with none finished, none is named and the backup is made; a kit whose
rename fails leaves nothing behind; an earlier attempt's ".sha256" is not written over.

### B-C03. The job's truth at a refusal, and three wordings

`research_job.run_locked` now makes its read-only checks first (the manifest, the variant folders, `--only`) and
only then writes: the note that a backup is owed, then the tidying of an interrupted status write. So an ordinary
refusal such as an unknown `--only` comes before any write and "nothing was written" is true of it. If a refusal
does follow the note, `run` says so ("No forecast, score or report was written; the tree's note that a backup is
owed had been written ...") and tries the owed backup after the lock is released. `mark_due` refuses with a plain
sentence if the note cannot be written. `run_locked` is annotated `-> tuple`. The job's END line is said by `run`
with the time read after the backup. `Run_Snapshot` says "Every file is read three times (hashed, written into
the ZIP, hashed again) and the ZIP is read back".
*Tests* (`TheResearchJobsBackups`): the note is the first write, before the tidying; an unknown `--only` after the
guard leaves no note, tidies nothing and says "nothing was written"; a refusal after the note is said as it is and
the backup is made; a note that cannot be written; the END line's time. **No test of build step 2 or of slice A
changed** (`test_research_job`, 48 tests, passes as it was).

## 3. Two things done that you should know of

- **The order inside `run_locked` moved:** `discard_unfinished_writes` now follows the three read-only checks
  instead of preceding them. A tree with both a foreign file in the staging folder and a bad `--only` is now
  refused for the `--only`. Nothing else of build step 2's job is changed.
- **One refusal seen in my own workspace, explained:** a run of `test_trees_restore` made while the planted-fault
  runner was ending its last child failed three tests with "1 other Python process(es) of the tree": slice A's
  process rule lists a Python process that ends while it is being read (it cannot be shown not to belong). Run
  again with nothing else running, the module passes. It is the reviewed rule behaving as written, not a fault of
  this slice; on the owner's PC it would be a refusal to run again.
- **The earlier planted-fault script for the whole slice (`mutation_check_slice_b.py`, 53 faults) was not run
  again:** several of its faults point at lines these corrections rewrote. The corrections have their own script
  and run (section 4). Its evidence file stands for the files as you first read them.

## 4. The evidence (the cloud: Linux, Python 3.15.0b4; mine, not Windows' and not yours)

In `evidence/` beside this note, the files with `EX_323` in their names.

- **The affected modules, on the final files** (`AFFECTED_MODULES_AFTER_EX_323.txt`): `test_trees_snapshot` 32
  tests, `test_trees_restore` 49 tests, `test_research_job` 48, `test_trees_launch_guard` 52, `test_file_form` 52,
  `test_research_manifest` 9: all OK.
- **The whole suite,** run because `research_job.py` changed: 61 modules, **1078 tests.** Against the slice as you
  read it: 1053 tests in both runs, every one with the same result; two tests replaced by stricter ones (the kit a
  backup names; the note before the first write); 25 new, all OK. Against slice A as it passed review: 1000 in
  both, all the same. The three known failing tests (eight failed assertions) and no other. **That run was made
  before the last three tests were added to `test_trees_restore` (46 then, 49 now); no program file changed after
  it, and the module was run again by itself.**
- **Planted faults for the corrections** (`mutation_check_ex323_corrections.py`): 34, one at a time (3 for B-B01, 5 for B-B02, 3 for B-B03, 4 for B-B04, 6 for B-C01, 7 for B-C02, 6 for B-C03). The first run caught 32; two survived (a root that is not a full path, which the comparison of the two roots already refused; the kit named before its ".sha256"). Three tests were added, and the run made again, with nothing else running, caught **34 of 34** (`PLANTED_FAULTS_EX_323_CORRECTIONS.txt`).
- **Not tested:** anything on Windows. The Toolhelp reading, the real rename, the restored Python's start and a
  real backup's time remain for the joined rehearsal.
