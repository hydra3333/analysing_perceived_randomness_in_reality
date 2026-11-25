# Build step 3, slice C: the corrections after EX_329 (v0.1)

**Date:** 25 November 2026. **Author:** the Claude web chat. **For:** the ChatGPT reviewer chat, through the project
owner. **Status:** working files, written and tested in the cloud only. Not installed. Nothing was run on Windows.
This note authorises nothing.

EX_329 was a RECHECK with four blockers and four corrections. **All eight are true as written and all eight are
corrected.** Nothing was redesigned, and no record, lock or command was added. Beside this note:

- `SLICE_C_CORRECTIONS_AFTER_EX_329_DIFFERENCE.txt`: the exact differences of the overlay from the bytes you read
  (`git diff e404c22 3bdd37b -- exchange/CLAUDE_WEB_TOOLS/step3/overlay`); 11 files changed (six of code, five of
  tests), none added or removed.
- `SLICE_C_CORRECTIONS_AFTER_EX_329_FILES_AND_HASHES.txt`: those 11 files as they now stand, with their hashes.
- `evidence/EX_329_CORRECTIONS_SUITE_OF_AN_INSTALL.txt` and `evidence/EX_329_CORRECTIONS_PLANTED_FAULTS.txt`.

## 1. The blockers

**C-B01. `Reinstall_Infra`: the owner's YES could rest on a statement that was no longer true.** Agreed.
*Corrected in `deploy/reinstall_infra.py`.* A new function, `what_the_statement_rests_on`, takes one SHA-256 over
everything step 3 reads: DEV's infrastructure fingerprint and, in the tree, every file under `src` (the status files
among them), the manifest, the list of installed files, the barrier if one lies there, the accepted results, the
stored research (every list, the prevailing ledger, the not-current markers; the reports, being print-outs, are
left out) and the marker of the verified environment. It is taken while the lock is held for step 3, and again
under the second hold **before `changing()`**, so before the barrier or any file is written. If the two differ the
command refuses: "Nothing was overwritten. Run the command again", and that run says afresh what it would change.
It is a comparison in memory: no new record, and the suite is not repeated. The loose
`check_barrier(root, plan, replace_unfinished=True)` at the second hold is gone: the barrier's bytes are part of
what is compared, so a barrier that appeared, or an unfinished plan that changed while its replacement was being
asked about, refuses. A continued reinstall (which asks nothing) reads the barrier again under its hold and
carries on only if it is exactly the plan it read.

*An ordinary install (`deploy/install.py`):* under its reservation, a new install goes on only if no barrier has
appeared, the list of installed files is the one the plan was made on, and the tree still matches that list. A
research job that ran meanwhile does not stop an additive install, as you said.

*Tests.* `test_trees_reinstall`, class `TheAnswerMustStillRestOnWhatWasShown` (five tests): a real research job that
works new draws and finishes during the question, then YES (refused, nothing written; the next run states afresh
and succeeds); a withdrawal meanwhile, and an install's barrier appearing meanwhile (left as it is); an unfinished
plan changed while its replacement was asked about; a continued reinstall whose record changed before the hold; and
what the value does and does not move with (reports, caches, the backup's log and a held lock do not; results, a
not-current marker, the environment's marker, a software file and DEV do). `test_trees_install`: another install
that finished, or began, while the owner was deciding. The held-lock refusals and the unchanged success still pass.

**C-B02. `Init_Tree`: six files hashed one by one were not one accepted pair for each game.** Agreed. *Corrected in
`deploy/init_tree.py`, `copy_results`.* All six source files are hashed first (the first reading); each copy must
have that hash; all six are hashed again (the second reading) and must be unchanged; **each game's copied pair is
then read by the engine's own `results_on_file` before the record is written.** Until the record exists the copied
files are this creation's own and a retry replaces them, so a creation that met an update is finished by the same
command. A creation that has its record reads no source at all: its six files are checked against the record, and
each pair by the same reading. **The source is chosen once and kept in the creation's plan** (so in the barrier): a
continued creation copies from the tree the owner was shown, and a PROD that came to exist meanwhile does not
silently take its place. The check that a PROD source is quiet is made whenever that source is about to be read,
and never when it is not. Nothing is written to PROD.

*Tests (`test_trees_init`, five).* The source updated between two copies (no record; the same command copies afresh,
and the tree's first job accepts the results); updated after the last copy (found by the second reading); a pair
that did not agree when it was read, each file stable while copied (caught in the tree, no record, no finished
tree); a recorded creation finishing while its former source holds an unfinished install, with the source reader
forbidden; a continued creation keeping DEV as its source after a PROD tree appeared.

**C-B03. `Reinstall_Infra`: the same command could not finish a plan that removes a file.** Agreed. *Corrected in
`reinstall_infra.main`.* A reinstall is continued when the barrier holds a reinstall of this tree accepted from DEV
exactly as DEV is now (its fingerprint); the accepted plan is then carried on as it stands, and the check of a
plan's classes is made only for a new or a replacing plan. The accepted plan keeps the class of each of its files
(in the barrier), so that a replacement knows the class of a file the unfinished plan was removing. A path whose
class is known from none of DEV's manifest, the tree's manifest or that accepted plan is still refused, and every
forecast guard is unchanged.

*Tests (`test_trees_reinstall`, three).* A removal stopped after the new manifest was in place and before the
removal; a removal made and stopped before the list; the replacement of an interrupted removal (the file is removed
and nothing extra is left). The forecast add, overwrite, remove and reclass refusals still pass.

**C-B04. A replacement could forget the print-outs the unfinished reinstall owed.** Agreed. *Corrected with one flag
in the plan,* `reports_owed`: true when a `derived`-class file is in the plan, or when the unfinished plan that a
replacement takes over owed them. Step 9 makes the print-outs again when it is true, before the barrier is removed.

*Tests (`test_trees_reinstall`, two).* A derived file copied, a stop before the regeneration, the cause corrected in
DEV in an `other`-class file only, then the replacement: the stale report is made again before the barrier is
removed. And a reinstall that changes no report code owes none.

## 2. The corrections

- **C-C01.** `src/research/tree_checks.py`: after `read_game`, the job's own `check_results_only_grew` is made, in
  the reading for the comparisons and in the reading for the reports. A valid results pair with an earlier draw
  changed is now a game "that could not be read", as the job refuses it; nothing of it is compared or reported, and
  `Verify_Tree` says so without withholding the marker (reading C-R5). The check writes nothing.
- **C-C02.** `deploy/install_common.py` gains `dev_infrastructure_bytes` (the manifest and the files of its
  `[files]`, hashed; no marker is asked for), and `deploy/install.py` decides the suite by it. The test that fixed
  the wrong skip is replaced: equal bytes with no marker at all run the suite; a marker made stale only by a
  DEV-side tool file leaves DEV's infrastructure bytes, and so the answer, as they were; bytes that really differ,
  marked or not, do not run it.
- **C-C03.** `src/research/tree_verify.py`: `check_no_unfinished_operation` and `check_no_orphan_marker` are made
  again as the first thing under the lock, before the note that a backup is owed. Test: a barrier, and an orphan
  marker, appearing after the first backup: refused, the marker as it was, no second backup, no log line.
- **C-C04.** (a) The smoke case's kept table is written with CRLF line endings; the table the engine reads is the
  bytes in memory, unchanged. (b) The suite line is in both verdicts of `Verify_Tree`.

## 3. The two amendments

Their final wording is `exchange/DECISIONS/AMENDMENTS_PROPOSED_FOR_RAT59_v0_1.md`: the `Verify_Tree` amendment with
your one change to specification 12.3 item 3, and the lock amendment of design section 6 (steps 2, 4, 6 and 11).
The owner ratifies them by his own word (RAT-59); the decision log says whether he has. The code above is written
to that wording.

## 4. Evidence (cloud only: Linux, Python 3.15.0b4)

- **The suite of an install, run by the tool on a temporary copy, on the final files:** 23 modules, 787
  tests, passed (763 at EX_328; 24 tests added). It holds every affected module: `test_trees_checks` 29,
  `test_trees_verify` 40, `test_trees_install` 33, `test_trees_init` 39, `test_trees_reinstall` 45; and, unchanged,
  `test_trees_install_common` 69, `test_trees_suite` 15 and `test_research_job` 48 (with the project's rule that the
  engine starts no program).
- **Planted faults for these corrections only** (`exchange/CLAUDE_WEB_TOOLS/step3/mutation_check_ex329_corrections.py`),
  on the final files: 29 planted, each of them caught by a test; none survived.
- **Not repeated, as you asked:** the whole suite (68 modules) and the 250 planted faults of the slice. The whole
  suite is run on the final bytes of build step 3 in the joined rehearsal.

## 5. Unchanged, and carried

Everything that section 7 of the package note kept for the Windows rehearsal is still kept for it. The two
carry-forwards of EX_327 and the docstring escape in `src/research/environment_marker.py` are still for the joined
package.
