# Build step 3, slice B: the two residual corrections after EX_325, for the focused recheck - v0.1

**Date:** 25 November 2026. **Author:** the Claude web chat. **Reviewer:** the ChatGPT reviewer chat.
**Status:** for the focused recheck EX_325 asks for. Not reviewed, not ratified, nothing installed. It authorises
nothing. It follows `SLICE_B_PACKAGE_NOTE_v0_1.md` and `SLICE_B_CORRECTIONS_AFTER_EX_323_v0_1.md`, which are left as
you read them; where they differ from this note, this note is the later one.

## 1. What this is

EX_325 (decision log entry 296) closed five of EX_323's seven findings and left two narrow residuals. I read both
against the files and both are true. Only those two are changed here. The exact differences from the files you
read (the overlay at `3ca9a04`, EX_324) are in `SLICE_B_CORRECTIONS_AFTER_EX_325_DIFFERENCE.txt` beside this note
(4 files, 10 hunks):

| File | Lines added | Lines removed | Hunks |
|---|---|---|---|
| `deploy/restore_tool.py` | 25 | 8 | 3 |
| `src/research/research_job.py` | 19 | 14 | 5 |
| `tests/test_trees_restore.py` | 44 | 9 | 1 |
| `tests/test_trees_snapshot.py` | 68 | 2 | 1 |

No file is added or removed; the manifest is unchanged; no forecast-class file is touched.

## 2. B-B02 residual: the rest of the settings' path rule

`deploy/restore_tool.py`, `check_destination`, with one new small function `_is_a_full_real_path` (not empty; a full
path by `Path.is_absolute`, so on Windows with its drive; equal to its own real path, as
`research/settings.py` asks of every path of a settings file; the folder need not exist). Before anything is
touched the backup's own settings must now give: a role that is QA or PROD; the tree root, the environment and the
backup root each present, full and real; the environment inside the tree and the backup root outside it. The
manifest's root and role must agree with them, as before. Nothing is read from the old tree, DEV or a drive list;
no link is searched for; a tree and a backup root that no longer exist do not stop a restore.

*Tests* (`NothingIsTouchedUnless`): a backup root that is relative, missing or empty; an environment that is
relative or missing; an environment outside the tree and a backup root inside it (as before); a role DEV on which
manifest and settings agree; a tree root named through a link; each refused with nothing touched. And a restore
with the tree gone and the backup root gone still succeeds.

## 3. B-C03 residual: the point this job reached, not the note in the tree

`src/research/research_job.py`. `run` keeps `reached = {'writing': False}` in memory and passes it to `run_locked`,
which sets it True immediately after `mark_due` has returned, before anything is tidied or written. The refusal
handler reads that and nothing else (`is_due` is no longer used in this file):

- not reached: "refused before any game was worked; nothing was written.", and **no backup is tried**, whatever
  note lies in the tree. A refusal at a guard never becomes a backup attempt.
- reached, in QA or PROD: the owed backup is tried after the lock is released (with the standing warning if it
  cannot be made), then "No research was written: no forecast, score or report. This job had written the tree's
  note that a backup is owed, so the backup was tried (its result is above)."
- reached, in DEV: "No research was written: no forecast, score or report. (If an interrupted status write was
  tidied away, a line above says so.)"; no note, no backup, and no claim that nothing changed.

A note that cannot be written refuses the job before `reached` is set, so it is reported as nothing written, which
is true. `run_locked` has one more argument, `reached`; nothing else of it changed.

*Tests* (`TheResearchJobsBackups`): your sequence (a note left by an earlier job; the backup failing at the start;
this job's own note; a refusal on a foreign file in the staging folder): two BACKUP NOT MADE lines, the standing
warning twice, the truthful END line, the note still there; a refusal at a guard with a note lying in the tree (the
orphan marker: no backup at all; the launch guard under the lock: only the owed backup at the start, none after);
DEV; a note that cannot be written.

## 4. The evidence (the cloud: Linux, Python 3.15.0b4; mine, not Windows' and not yours)

In `evidence/` beside this note, the two files with `EX_325` in their names.

- **The affected modules on the final files** (`AFFECTED_MODULES_AFTER_EX_325.txt`): `test_trees_snapshot` 36 tests,
  `test_trees_restore` 52, `test_research_job` 48, `test_file_form` 52, `test_research_manifest` 9: all OK.
- **Planted faults for these two corrections** (`PLANTED_FAULTS_EX_325_CORRECTIONS.txt`; the script is
  `mutation_check_ex325_corrections.py`): 11, one at a time (6 for B-B02, 5 for B-C03): 11 of 11 caught.
- **Not run, as you asked:** the whole suite and the earlier planted-fault scripts. The joined rehearsal runs the
  whole suite.
- Nothing ran on Windows.
