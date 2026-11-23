# Build step 2 (the research engine, in DEV) - package note, v0.2

**Status:** corrected after the reviewer's EX_283 (RECHECK: two crash-recovery blockers, both accepted and fixed;
section 0) and offered for the reviewer's recheck as package `STEP2_Research_Engine_v1r1`. Not installed. **Nothing
here authorises any operation on the owner's PC:** his install, and separately DEV's first fill, are each on his own
go. v0.1 of this note and package v1 are kept as they were reviewed (`exchange/EX_282_Claude/`).
**Author:** the Claude web chat (on Fable (High) for this step). **The owner's go for the build:** decision log entry
176; his two answers (DEV's research results are not tracked by Git; review in slices is Claude's choice): entry 177.
**Authority:** `doc/Predictive_Randomness_System_Specification_v0_6.md` ("the specification"),
`doc/Predictive_Randomness_Deployment_Design_v0_12.md` ("the deployment design"), `doc/CODING_PRACTICES_v0_1.md`
(RAT-40). The plan this was built to: `STEP2_BUILD_PLAN_v0_2.md`, beside this file.

## 0. What changed after EX_283 (package v1 to v1r1)

EX_283 found two faults in crash windows by tracing file states that my tests had not planted. Both are real; both
are fixed narrowly; neither touches a forecast or a score.

| Finding | The fault | The correction | The proof |
|---|---|---|---|
| **F283-B01** (BLOCKER) | The status file was written under a temporary name inside the variant folder. A write interrupted before its rename left `VARIANT_STATUS.ini.writing` there; the variant scanner rightly refuses any undeclared file, so the variant was left out (DEV) or the job refused (QA, PROD) | `status_file.write_status` stages the file in `<tree>/records/status_staging/`, never in the variant folder, then renames it into place (same volume, one step). `discard_unfinished_writes` removes what an interrupted write left there, under the job lock, at the start of every job and every withdrawal, and says so. The scanner is as strict as before: no `.writing` file is tolerated in a variant folder | `InterruptedStatusWrite` (3 tests): an eligibility write killed at the rename, a rename that fails, a half-written staged copy; DEV's first creation of a status file killed at the rename; a withdrawal killed or failing at the rename. After each, the real scanner accepts both variants, each variant folder holds exactly its own files, the real job runs, and (for the eligibility cases) every file equals the uninterrupted run's |
| **F283-B02** (BLOCKER) | The copy staged the ledger first, and recovery took "a staged ledger alone" as proof that the results file had been replaced. A crash after staging the ledger and before staging the results file left exactly that, with the old results still in place: recovery then put the new (or partial) ledger beside the old results, and the reader refused | One order: stage the results file, stage the ledger, replace the results file, replace the ledger. A staged results file therefore always means "nothing accepted was touched". And recovery no longer trusts names: a staged ledger is put in place only if its last row names the SHA-256 of the results file on disk; otherwise it is discarded and the accepted pair stands | `InterruptedResultsCopy` (2 tests): seven file states a crash can leave, among them the one EX_283 found (whole and half), each finished or discarded to a pair that agrees with itself; and a kill or a failure before, half-way through and after each of the four steps (20 cases). In every case the accepted pair is old or new, never mixed, and the next job leaves every file equal to the uninterrupted run's, byte for byte |

**A third fault, found by the oracle the reviewer asked for.** Comparing an interrupted-and-continued job with an
uninterrupted one showed that the uninterrupted job itself left league reports one step behind: it wrote them
draw by draw and then, at its end, wrote the eligibility draws, which every league report shows. The next job
rewrote them all. Now every league report is made once more at the end of each job (`write_league_reports`), so
the folder is a function of the lists, the results and the status files when the job ends, as specification 9
requires. One new test and one planted fault.

**Also changed:** the withdrawal makes every refusal before it asks its question (the reason is checked for plain
text first); a file fault during a withdrawal ends with a plain line and exit code 1, each status file whole; the
sheet says that parts 1 to 5 "run no research fill on the real results" (EX_283 Q10: the suite's oracle tests do
read the results files).
**Not changed:** every `forecast`-class file, scoring, the lists' code, OV-1, the derived check. The forecasting-code
identity is the same as v1's, so the suggestive real-data evidence of v1 stands (and the corrected engine was run
once more over those lists: nothing to compute, no report rewritten on the second pass).

**The reviewer's answers to Q1 to Q10 are taken as given;** three of them bind what follows: the line-ending pin is
fixed before the first production installation (Q7); deleting DEV's research results by hand is a DEV-only interim
choice and never advice for QA or PROD (Q8); the real prevailing OV-1 is not called established from synthetic
tests (Q9).

## 1. Work-item card

- **Item:** build step 2 of specification 17.4: the lists, the research job with its fill and catch-up, scoring, the
  reports, both OV-1 scores, the status file and the withdrawal (specification sections 3 to 11), with both header
  identities and the checks of 5.6A and 5.8 from the first day, and RAT-40's warnings at the start and the end.
- **Risk tier:** HIGH (the reader and the permitted view, the list writer, scoring, the readout, OV-1, the status file).
- **What it is not:** `Init_Tree`, `Install`, `Reinstall_Infra`, the readiness marker and the static import check,
  the installed-files check, the process-table rule, backups and restore, the updater's launch from the job in PROD
  (all build step 3); the rerun, `Check_Forecasts`, the two copies from PROD, the correction command (build step 4).
- **The old system is not changed.** No file of its code and no method file is touched. Two existing files are
  edited: `.gitignore` (six patterns added) and one old static test (section 2).

## 2. What the package adds

**33 new files and 2 edited files; nothing deleted.**

| Files | What they are |
|---|---|
| `src/research/` (20 `.py` files) | the engine: section 3's table |
| `src/research_command.py` | the one program behind the two launchers |
| `Run_Research.bat`, `Withdraw_Variant.bat` | the launchers, in the tree's folder (CRLF) |
| `deploy/INFRA_MANIFEST.ini` | the infrastructure manifest: 32 files, each with its class (specification 12.4) |
| `ENVIRONMENT.example.ini` | the tracked example of a tree's settings file (deployment design section 1) |
| `tests/research_fixtures.py` and 7 test modules | 185 tests on invented draws and toy variants, and four oracles against the old code |
| `.gitignore` (edited) | Git ignores `/ENVIRONMENT.ini`, `/results/research/`, `/results/research_set_aside/`, `/records/`, `/scratch/` and every `VARIANT_STATUS.ini` (the state of one tree; owner, entry 177) |
| `tests/test_mhupa_master_versions.py` (edited) | its list of the files under `src/` allowed to name a results file gains `src/research/reader.py`. One line of data in one old test; an honest edit, preferred to hiding the name from the test |

## 3. The engine, file by file

| File (`src/research/`) | What it does | Specification | Class |
|---|---|---|---|
| `__init__.py` | the package; sets the numerical libraries to one thread before NumPy loads | 5.4 | forecast |
| `method_api.py` | `MethodFailed`, the one exception a method raises for a failure of its own mathematics | 5.3 | forecast |
| `variant_folders.py` | finds families and variants; checks `VARIANT.json`; the fingerprint; an undeclared file refuses | 3.2, 3.4 | forecast |
| `reader.py` | the results on file, checked against their ledger; the permitted view (the draws before the target) | 6, 5.4 | forecast |
| `readout.py` | scores to ranking, ties, TOP and WORST | 1.2; section 6 below | forecast |
| `forecast_engine.py` | one target of one variant: view, task, `compute`, readout, `verify`, the line's content | 5.3, 5.4, 6 | forecast |
| `code_identity.py` | reads the manifest; the forecasting-code identity; the derived-code digest; the environment digest | 12.4 | derived |
| `variant_lists.py` | the list files: header, chain, append, the torn last line, invariants 1 to 4 | 5.1 to 5.7 | derived |
| `status_file.py` | `VARIANT_STATUS.ini`: read, check, write (staged outside the variant folder, then one rename); withdrawal and eligibility set once | 3.5 | derived |
| `scoring.py` | the one scoring function | 8, 5.5 | derived |
| `game_state.py` | one game's records in memory; invariant 5; which lists are foreign and which variants held | 5.6, 5.6A | derived |
| `ov1_numeric.py` | the passed kernel, byte for byte from MHUP-B slice 2 (SHA-256 `2858075e...8d8234`) | 10.1 | derived |
| `ov1_ledger.py` | one draw's OV-1 line; the prevailing cohort and start; the exploratory series | 10.2 to 10.5 | derived |
| `derived_check.py` | the full check of every score and the whole ledger; `NOT_CURRENT_FROM.json` | 5.8 | derived |
| `reports.py` | the league, next-draw and OV-1 print-outs; stale reports set aside | 9, 10.5, 10.6, 5.8 | derived |
| `job_lock.py` | the job lock and the updater's own lock; the orphan-marker check | 7.1, 11, 15 | derived |
| `results_step.py` | QA and DEV: the checked copy of the results from the tree the settings name | 7.1 | derived |
| `settings.py` | reads and checks `ENVIRONMENT.ini` | 2; deployment design 1 | derived |
| `research_job.py` | `Run_Research`: Start, Fill, Results, Catch-up, End | 7.1, 7.2, 5.7, 10.2 | derived |
| `withdraw.py` | `Withdraw_Variant` | 11 | derived |

**What the engine uses of the old system, and what it leaves** (this settles specification 17.3's pointer to
"section 10 of the simplification design v0.1", a draft that was never ratified: the list is this one, computed by
following the imports of the two commands, as the class test does).
- **Imported unchanged (7 files):** `src/methods/_common/` `__init__.py`, `canonical_encoding.py`,
  `contract_forecast.py` (the types a method returns), `contract_task.py` (the frozen task and the view digest),
  `contract_records.py` (score groups, the tie order, record digests), `contract_vocab.py`, `game_profiles.py`; and
  `src/evaluation/divisions.py` with its package file. The existing method files import the same `_common` files,
  so they are forecasting code by the import rule and are on the manifest as `forecast`.
- **Copied, character for character:** the `DrawView` class and the prefix parser of
  `_common/game_draws_reader.py`, into `reader.py` (a test compares the copied definitions with the old file's by
  their syntax trees and fails on any difference). The new reader does not import `master_versions`, the owner
  records or the Mode H opening-record gate; the old reader is untouched.
- **Left out:** every other old module: 59 `.py` files under `src/` outside the method folders (the coordinator,
  the runner, registry, dispatch, walk-forward, Mode H, the evaluation tools, the package tools, the updater).
  Nothing of them is imported, started or named by the engine.

## 4. How the job works, in plain English

`Run_Research.bat --game POWERBALL|OZLOTTO|BOTH [--no-update] [--only <family>/<variant> ...]`, for each game:

1. **Start.** The settings; no orphan marker; the job lock; the manifest and the two code identities; the variants
   and their status files (DEV creates a missing one as `ACTIVE`; QA and PROD refuse). The results on file, checked
   against their ledger. Every list read and checked; a list whose header names other variant files or other
   forecasting code than is installed, or which disagrees with its status file, is **foreign**: it is named, never
   appended to, and its variant is **held**. Results that changed other than by growing refuse the game and name the
   draw (found from the view digest each stored forecast holds). Then the full derived check.
2. **Fill and catch-up are one function,** `complete_draw`, called for every draw from the lowest first target to
   the last on file, in order. For one draw, in the write order of 5.7: forecast lines (made durable); score lines
   (made durable); the prevailing OV-1 line if it is the next due; the league report. Each is skipped if already
   there, so a job that was interrupted is continued by the same command.
3. **Results.** QA and DEV: the results are copied from the tree the settings name, only if the results here are
   the beginning of those there. Left out with `--no-update`, with no tree named, or in PROD (step 3 brings the
   updater's launch). A step that fails or is left out changes nothing and is said.
4. **End.** If the results step succeeded: every variant with no eligibility draw, not withdrawn, with its history
   complete, gets the last draw on file plus one, once. The next draw is forecast. The next-draw reports and both
   OV-1 print-outs are made. Every warning is said again.

A report file is written only when its bytes would differ from the file on disk. So every job leaves the reports
folder exactly as the installed code makes it from the current lists, results and status files, and an unchanged
report is not touched.

## 5. Choices made here, each RECOMMENDED, with the alternative

The nine choices of the build plan stand as built (the copied reader without the Mode H gate; a native readout
calling the old `score_groups`, `tie_identity_for` and `order_groups`; the method contract unchanged, with fixed
values for the retired task fields; what becomes `METHOD_FAILED`; the probability vector checked and given to
`verify`, not stored; results that changed found from the lists; DEV's research results untracked (owner); no results
step, eligibility or prevailing score in DEV until a tree exists to copy from; the process-table rule in step 3).
Made while building:

1. **Reports by comparison, not by bookkeeping.** Every job makes every report again in memory and writes only the
   files whose bytes differ. It gives 9's rules (rebuilt from the earliest affected draw; made again when the report
   code changes; EX_269 R7-F02) without the job having to know what was affected. Measured on the real Powerball
   records: a job with nothing new takes 71 seconds in the cloud, most of it the exploratory score. *Alternative:*
   track the earliest affected draw; faster, and one more thing to get wrong.
2. **A next-draw report exists for every draw that some forecast was made for before its result was on file.** It
   is a function of the lists alone, so it is made again like any report. A new tree has one (the next draw); each
   week adds one. *Alternative:* only the newest; then an older file made by older report code would stay in view.
3. **The job lock is a file made by an exclusive create and removed at the end,** as the deployment design words it
   (5 step 6) and as the updater's own lock works. A job that was killed leaves it; the refusal says to delete that
   one file by hand once no job of the tree is running. Nothing ever removes another's lock. *Alternative:* a lock
   the operating system frees with the process; friendlier after a kill, but the install tools of step 3 could not
   tell "held" by looking, and PROD is checked by reading only.
4. **One program behind the launchers, `src/research_command.py`:** it puts this tree's two code folders first on
   the import path, checks that the Python running is the environment the settings file names, and hands over.
   The launchers run it with `-I -B` (isolated; no cache written). The thread settings are fixed in
   `research/__init__.py`, which is forecasting code, so they hold however the engine is started.
5. **Classes.** The job and the withdrawal are entry points of the class test for derived results; what they import
   is therefore `forecast` or `derived`, and `settings.py`, `job_lock.py`, `results_step.py` and `code_identity.py`
   are classed `derived`. `other` is the command program and the two launchers. The job is not classed `forecast`:
   a forecast's content is computed wholly inside `forecast_engine.compute_target` from the results bytes, the
   variant and the target; the job decides only which targets are computed. *Alternative:* class the job
   `forecast`; then any change to its messages would make every list foreign.
6. **"Its history complete" (10.2)** is: not held; a line for every draw from its first target to the last on
   file; every `FORECAST` among them scored. A variant whose first target is beyond the next draw gets no
   eligibility draw yet (it would otherwise block every prevailing line until it had a line).
7. **In DEV an unfinished variant folder (one that fails its checks) is named in a warning and left out; in QA and
   PROD it refuses the job.** DEV is where work in progress lies (specification 4).
8. **A results step "fails" when the source cannot be read whole (said; the job goes on) and "refuses" when the
   results here are not the beginning of the source's (the game stops).**
9. **The withdrawal:** the variant as two words, several pairs allowed; every refusal is made before anything is
   shown; the owner types `WITHDRAW`; one line is added to `records\INSTALL_LOG.jsonl` (the log the deployment design
   names for withdrawals).
10. **A held variant makes the derived results not current from the first target its foreign list names** (5.6A:
    "from that variant's first draw").
11. **"QA and PROD agree ... byte-identical" (18):** two trees with the same software, status files and results
    compute the same content, line for line (tested); each line's envelope still says which tree computed it
    (5.4), so lines each tree computed itself differ in those bytes. Byte-identity holds for data that was copied.
12. **The time of making** of each report is in `reports\made_times.csv`, noted as each file is written.

**Three consequences the reviewer and the owner should know.**
- **Until build step 4 no command clears a held variant or a `MISMATCH`.** The job says so and names the rerun
  command that will. In DEV the interim way out is to delete DEV's untracked `results\research\` folder by hand and
  run the job again (about an hour); DEV's research results are disposable (owner, entry 177).
- **A status file put back alone, after lines were written under a withdrawal, is found:** the ledger no longer
  equals its rebuild, and the results are marked not current from that draw. A whole restore (lists, ledger and
  status files of one day) continues cleanly (tested).
- **Line endings.** The fingerprint and the forecasting-code identity hash the bytes on disk (3.4, 12.4). The
  owner's clone uses `core.autocrlf=true`; if Git ever rewrites the line endings of a file under `src\` there, DEV's
  lists become foreign and are filled again as above. That fails safe and touches only DEV. Entry 157 leaves the
  `.gitattributes` pin to "step 2 or 3, without rewriting every source file as housekeeping": it is **left to step
  3**, where the first byte-bound marker that travels (`I_AM_INSTALLABLE.json`) is built and the pin can be put to
  the owner with its cost. This package does not change `.gitattributes`.

## 6. The exact clause list for E2R-1 section 7 (owed by the code round; specification 20)

`doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` section 7, as the engine carries it:

| Clause | In the engine |
|---|---|
| 7.0 typed output | **Kept in part.** A method returns `MethodOutput` with a `ScoredRanking` for every barrel; no barrel at all means "not enough history". Order-only rankings, native joint sets (`MAP_SET`), `NoOutput` and diagnostic payloads are not used: a joint selection is refused |
| 7.1 the record header; E2R-R25A | **Replaced** by the list line of specification 5.3 and 5.4. Kept in the content: game, family, variant, target, `permitted_view_digest`, status. Retired: `profile_version` and `era_id` (still given to the method in its task), `method_revision`, `declaration_digest` (the variant fingerprint takes its place), `draw_key`, `training_last_draw_number`, `fit_sampling_model_version`, `run_mode`, `product_kind`, `warnings`, `canonical_content_digest`. The run-mode rules of R25A are retired with the modes |
| E2R-R26 (the digest covers pre-target content only) | **Kept** as specification 5.4: the content digest, with everything else in the envelope. Tested: draws at and after the target changed and appended leave the digest unchanged |
| 7.2 per-barrel output | **Kept:** `label_low`, `label_high`, `selected_count`, `scores` (lowest number first), `ranking`, `top`, `worst` (plain lists of numbers). **Not stored, because recomputable or constant:** `ranking_kind`, `ranking_status`, `score_direction` (higher is better), `ranked_groups`, `tie_identity`, `ranking_digest`, the rule names. `probability`: checked and given to `verify`, not stored |
| E2R-R26A | Does not arise: a `FORECAST` has every ranking; anything less is `NO_FORECAST` |
| E2R-R27 (each number once; groups recomputed from the scores) | **Kept:** the old `score_groups` is called |
| E2R-R28 (`TIE_SHA256_V1`) | **Kept unchanged:** the old `tie_identity_for` and `order_groups` are called, with the ratified seven fields (domain, view digest, target, method ID, variant ID, barrel, version). The method ID is the family's old form (`E_2` for `E_002`), so every tie falls as it did |
| E2R-R29 (TOP the first k of the ranking; WORST the first k of its reversal) | **Kept** |
| E2R-R30 (`MAP_SET`) | Not used; refused |
| E2R-R31 (TOP and WORST statuses recorded independently) | **Replaced** by specification 5.3: a `FORECAST` holds complete TOP and WORST for every barrel, or the line is `NO_FORECAST` with one typed reason |
| E2R-R32 (k distinct numbers in range) | **Kept** by construction from the full ranking |
| E2R-R33 (finite scores; no NaN, infinity or negative zero) | **Kept.** The scores of a barrel must be all whole numbers or all floats; the declared score type is no longer a declaration field |
| E2R-R34 (probability vectors) | **Kept in part:** one finite float for each number. The range and sum rules are not applied, because the vector is not stored or scored; it is only handed to the method's own `verify` |
| E2R-R35 (a validation failure is counted, never hidden) | **Replaced** by specification 5.3: the line `NO_FORECAST: METHOD_FAILED`, with the detail in its envelope; counted in every league report |
| 7.4 record status | `PREDICTION_AVAILABLE` is `FORECAST`; `INSUFFICIENT_HISTORY` is `NO_FORECAST: INSUFFICIENT_HISTORY`, declared by the method. The first target is fixed by the declared minimum of earlier draws, so the engine never asks below it. `DIAGNOSTIC_ONLY` is retired |
| 7.5 the tickets | **Kept:** Powerball seven numbers and the Powerball; Oz Lotto seven; scored by specification 8 |
| 7.6 seeds (E2R-R61, R63) | **Standing, unused:** no variant is stochastic; the content holds `"seed": null`. A stochastic method needs its reviewed seed policy first |
| 7.7 the diagnostic record (E2R-R62) | **Retired:** none is produced |

## 7. Evidence (cloud workspace: Linux, Python 3.15.0b4, 2 processors)

Package v1r1 was built from a fresh clone at the base commit (`465758d`) by `build_step2_pkg.py`; its evidence is in
`evidence_v1r1/`, and the whole suite's "after" run was made on a fresh clone holding exactly its files. The rows
marked "real, suggestive" and the scan are in `evidence/` and were made with package v1; section 0 says why they
stand.

| What | Result |
|---|---|
| The engine's own tests (`evidence_v1r1/suite_after/`) | 7 modules, **185 tests, all OK**: identity 25, forecasts 26, records 28, manifest classes 9, the kernel's own 21, the job 42, OV-1 and the checks 34 |
| The whole suite before and after (`evidence_v1r1/SUITE_COMPARISON.txt`) | before 45 modules, 571 tests; after 52 modules, 756 tests. **All 571 old tests give the same result;** the three tests that fail today fail the same way; 7 modules and 185 tests are new |
| The suite again on the tree after the first fill (`evidence/SUITE_AFTER_THE_FIRST_FILL.txt`; made with package v1) | with the settings file, 40 status files, both games' research results and `records/` in place: **all 750 tests of v1 gave the same result** as on the fresh tree. What the first fill leaves behind disturbs no old test. Not repeated for v1r1: it adds only the staging folder under `records/` |
| Planted faults (`evidence_v1r1/PLANTED_FAULTS.txt`, by `mutation_check.py`) | **31 of 31 caught** (26 as before, 5 new for section 0): one fault at a time planted in the engine, the named test required to fail, every file put back |
| The install rehearsal (`evidence_v1r1/INSTALL_REHEARSAL.txt`) | an LF clone and a `core.autocrlf=true` clone: PRE, POST and COMMITTED PASS; seven cases that must STOP, each stops |
| Oracle: the copied reader | the copied definitions equal the old reader's (syntax trees); the new view equals the old loader's view and digest on the real results, targets across both games |
| Oracle: the readout | for all 40 variants in both games, the new engine's scores, ranking, TOP and WORST equal the old `assemble_forecast` (160 forecasts on invented draws) |
| **(real, suggestive)** the first fill of both games in the cloud (`REAL_FILL_CLOUD.txt`) | 40 variants a game, results through the last draw on file. Powerball: 15,118 forecast lines and 15,078 scores in **22 minutes**; a second job with nothing new **71 seconds**; lists 45 MB, reports 11 MB. Oz Lotto: 6,598 lines and 6,558 scores in **7 minutes**; a second job **32 seconds**; lists 19 MB, reports 5 MB |
| **(real, suggestive)** the old score records against the new score lists (`REAL_COMPARISON_CLOUD.txt`, part 1) | **all 34,800 old development score records that Git tracks equal the new lists** (22,884 Powerball, 11,916 Oz Lotto; all 40 variants, TOP and WORST): the numbers drawn, the main matches, the Powerball match or the supplementary matches, and the prize division |
| **(real, suggestive)** old forecasts against new, a sample (`REAL_COMPARISON_SAMPLE.txt`, part 2) | the old run folders exist only on the owner's PC. For two Powerball variants I made the old records again with the old code path (each matched the old digest that Git tracks) and compared: **582 of 582 equal** in view digest, scores, ranking, TOP and WORST; one altered record is found. The complete part 2 is the owner's sheet, part 7 |
| The scan of the coding practices (`evidence_v1r1/CODING_PRACTICES_SCAN.txt`, by `scan_practices.py`) | 29 Python files, 0 findings; three files excused by name (section 10) |

"Suggestive" is the owner's rule for anything Claude works out from real draws: these figures count for nothing
until his own run. They are here because they are the cheapest strong evidence that the new engine reproduces the
old one. No draw's numbers are shown in this note or in the evidence files.

**What the planted crashes cover.** A kill is planted after every single write of a job that catches up three
draws for three variants (forecast lines, score lines, prevailing lines, league reports); inside the status
writer, at its rename (section 0); and before, half-way through and after each step of the results copy (section
0). Each time the job is run again and every file of the tree must equal the uninterrupted run's, byte for byte.
A torn last line in each of the five stored files is cut and written again to the same bytes. **What they do not
cover:** a failure of the disk itself between a flush and the rename, and the behaviour of these calls on Windows,
which only the owner's run can show.

## 8. The install package (`STEP2_Research_Engine_v1r1`, built by `build_step2_pkg.py`)

`repo_overlay/` (the 33 new files and the 2 edited files, whole), `VERIFY_STEP2_INSTALL.py` (the project's reviewed
verifier template: PRE, POST, COMMITTED; 28 guarded files, among them the results files, the old shared code the
engine imports and `.gitattributes`), `tools/` (`run_suite.py` and `compare_suite_reports.py`, byte for byte those
of build step 1; `compare_fill_with_old_records.py`, new), `INSTALL_MANIFEST_SHA256.txt` and
`INSTALL_AND_RUN_SHEET.md`.

The sheet has two halves. **Parts 1 to 5 install and prove the install** (the suite before and after, the
verifier, the commit, the settings file) and run nothing on real results. **Part 6, on the owner's separate go, is
DEV's first fill,** then the same job once more for its timing; **part 7 is the early comparison** with the old
development records, complete on his PC because the old run folders are there.

## 9. Not tested, and limits

- **Nothing has run on Windows.** The two `.bat` launchers have never been executed; the file operations the engine
  relies on there (an exclusive create, a rename over an existing file, a flush to disk, cutting a file's end) are
  standard but unproved here. The first execution is the owner's sheet. The suite's 185 new tests exercise all of
  them on his PC in part 3, before anything real runs.
- **A withdrawal of several variants that is interrupted between two of them** leaves the first withdrawn and the
  rest active, each status file whole. Run again, the command refuses the one already withdrawn and says to name
  the others only. A withdrawal is one-way, so nothing is undone for the owner.
- **An eligibility write that is interrupted, with new draws arriving before the job is run again,** gives the
  variants not yet written the later draw. That is the rule of 10.2 (the first draw not on file after a successful
  results step), applied at the time it is applied; it is said here so that it is not a surprise.
- **Speed on the owner's PC is unknown.** In the cloud a first fill of Powerball takes 22 minutes, nearly all of it
  inside the methods (the exact-fraction fits of E_3, E_4 and E_18). Each draw flushes up to 80 list files to disk;
  on Windows that may add minutes. The sheet asks for the times.
- **The derived check and the exploratory score are recomputed at every job** (5.8: exhaustive). 71 seconds for
  Powerball in the cloud; it grows with the history. If it becomes a nuisance, 5.8's own fallback applies.
- **No command clears a hold or a mismatch until step 4** (section 5).
- **Step 3's checks are absent:** the installed-files check, the process-table rule, the environment marker, the
  "backup due" flag and the end-of-job backup. In step 2 the engine runs in DEV only; nothing creates a QA or PROD
  tree. The job's code for QA and PROD roles is tested on invented trees.
- **PROD's results step is left out** until step 3; the job says so.
- **R3's fuller measures** (specification 9, last line: "on request") are not built.
- **The prevailing OV-1 does not start in DEV** until a tree exists to copy results from: no eligibility draw is
  written without a successful results step (10.2). DEV's reports show the exploratory score only. That is the
  build plan's choice 8 and the specification's rule; it means the prevailing ledger's code is proved on invented
  trees and by the kernel's own tests, not yet on real draws.
- **The envelope's environment digest** names the Python and the installed distributions; it says "computed under
  the same packages", not that two environments are numerically identical (specification 13).

## 10. Coding practices (`doc/CODING_PRACTICES_v0_1.md`)

Applied to every new file: the plain-English header with its four parts; constants at the top, each with its
reason; no path, drive letter or role in code (the tree is the folder the program lies in; the rest comes from the
settings file, whose missing or malformed settings refuse by file, section and key); a comment on every function
with a returned example; messages that say what was found and what to do, in the project's words; held variants and
results not current said at the start and again at the end with the exact command; results independent of the
clock, the locale and accidental ordering; one shared piece of code for each shared task; each rule a test, each
test named for its rule, with planted faults. A scan of every new file for a header, a comment on every function
and class, and unused imports is clean.

**Three exceptions, each deliberate.**
- `ov1_numeric.py` and its test are the passed MHUP-B kernel and its tests, **byte for byte** (only the test's
  import line differs). They keep their own, sparser comments so that the bytes the reviewer passed are the bytes
  that run.
- The definitions copied into `reader.py` keep the old reader's comments, for the same reason; the new functions
  around them follow the practices.
- The `.bat` launchers hold the path `.venv\Scripts\python.exe` relative to the tree, because a batch file cannot
  read the settings file; the program they start checks it against the settings and refuses a mismatch.

## 11. Statement on draws

The engine's tests use invented draws from a seeded generator and toy variants; two oracle tests read the real
results files through the project's readers and compare views and digests, printing no draw. The cloud runs
marked "real, suggestive" read the real results and the old tracked records, which the owner's rules allow Claude
to read; their outputs hold counts and timings only. No lottery website was contacted and no lottery result was
searched for. The comparison tool reads only the old system's development folders
(`results/real/development/`); no tool here opens a Mode H record, and nothing sealed is altered.
