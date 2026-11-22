# Build step 1 (the folder layout) - package note, v0.3

**Status:** returned for the reviewer's focused recheck as EX_277 (22 November 2026), after EX_276 (RECHECK: four
narrow corrections, STEP1-C01 to C04; the layout itself accepted). Nothing is installed: no file of `src/` or `tests/`
in the repository is changed. The owner's go for build step 1 is decision log entry 158. **v0.3 corrects the two
tools, the sheet and this note's description of the evidence; the change to `src/` and `tests/` is byte for byte the
one EX_275 carried** (v0.1 and v0.2 stay beside this file as history). The package is now `STEP1_Layout_Install_v2`.

## Work-item card

| | |
|---|---|
| Item | BUILD-STEP-1: the folder layout (specification 17.3 phase 1; 17.4 step 1) |
| Author / reviewer | the Claude web chat / the ChatGPT reviewer chat |
| Base commit | the tested trees were built from `fdb1f91`; the install package v2 from `c0e3104` (v1 from `05e9afd`). `src/`, `tests/`, the root `.bat` files and `requirements.txt` are the same in both, and equal `cc0ab73` |
| Scope | method files moved to the family and variant layout; three shared helpers renamed; the runner's table built from the folder tree; imports and test references follow. No computation, contract or record changes |
| Risk tier | HIGH (it touches the code every forecast passes through), kept small |
| Owner gate | entry 158 (the go, cloud workspace only). On his PC, each on his own go: the suite baseline, his ZIP, the install, the equivalence run sheet |
| Evidence state | IMPLEMENTED and AUTHOR-TESTED in the cloud workspace; the install REHEARSED there in an LF and a CRLF clone. Not REVIEWED, not installed, not run on Windows |

## What changes (made by `make_step1_layout.py`, repeatably, from the base commit)

`evidence/STEP1_CHANGED_FILES.txt` lists every file with its hashes; `evidence/STEP1_LAYOUT_CHANGE.diff` is the whole change.

- **15 files moved.** Five are byte for byte unchanged: the three shared helpers (`_common/recurrence_gaps.py`,
  `occurrence_counts.py`, `polynomial_fits.py` to `_shared/<name>_v1.py`), `E_006/contract.py` to `E_006/core_v1.py`,
  and E_1's wrapper `contract_adapters/e_001.py` to `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py`. The other ten
  (`E_00x/contract.py` to `E_00x/core_v1.py`) each differ in exactly one line: the import of a shared helper.
- **80 files added:** 39 `method.py` (one text, differing only in the family and variant names), 40 `VARIANT.json`,
  and `src/methods/_common/method_table.py`.
- **1 file deleted:** `src/methods/contract_adapters/__init__.py` (the folder is empty after the move).
- **1 source file modified in place:** `src/methods/Method_Contract_Runner.py` (+5, -16): its twelve import lines and
  hand-written table become `ADAPTERS = build_method_table()`.
- **14 test files modified:** 43 import lines follow the move (in `src/` and `tests/` together), and 22 counted
  replacements of other lines in eleven test files (the list is `TEST_TEXT_CHANGES` in the builder). Those 22 are:
  a moved file named by its path or module name; a family folder's file list; and four lines that pinned the
  hand-written table (`assertIs(M.ADAPTERS[name], mod)`), which now say that every variant's `method.py` uses that
  family module. No expected value, golden or reference hash is changed.
- **Not changed:** `closure.py` (it lists every file under `src/` and holds no folder list); every calculation;
  every declaration and registry file; the record formats; the revision field.

## Choices made here, each RECOMMENDED, with the alternative

1. **The table has one entry per family that sends a task to the `method.py` of the task's own variant**
   (`FamilyMethods`). So the per-variant files, which are what will later be installed and never changed, are
   the files every run and every test goes through from now on. *Alternative:* keep the table pointing at the
   family module; no test line would change, but the 40 `method.py` files would exist untested.
2. **A variant's `method.py` holds no calculation in this step:** it passes the task to the family's `core_v1.py`
   and refuses a task for any other variant. E_1's `method.py` is its old wrapper, unchanged.
3. **`variants.py`, `beta_bernoulli.py` and each family's `__init__.py` keep their names** beside `core_v1.py`
   (17.3: "its other modules beside it"). They are listed as helpers in `VARIANT.json`. Their names are not
   versioned; if that matters it is a rename for the tidy-up or step 2, before anything is installed.
4. **`_shared/` and the variant folders have no `__init__.py`,** as the layout of specification 3.2 shows.
   *Alternative:* 41 empty files.
5. **`VARIANT.json` holds the fields of specification 3.4:** `family`, `variant`, `title`, `description`, `games`,
   `minimum_earlier_draws` (per game, from the installed declarations), `observation_view`, `files` (names in the
   folder) and `helpers` (paths from `src/methods`, worked out from the import statements). Titles and descriptions
   are mechanical. Nothing reads these files for science yet; step 2 defines the fingerprint and may refine them
   before anything is installed.
6. **The equivalence check lives in `exchange/`, not in `src/`,** and is run from a run sheet. It uses the runner's
   own functions in the runner's order and leaves out only the publication, so it writes nothing.
7. **Out-of-date words inside moved files** (docstrings that still say `contract` or `_common/recurrence_gaps.py`)
   are left: step 1 changes import lines only. They belong to the light tidy-up (RAT-40 note 3).

## Evidence (cloud workspace: Linux, Python 3.15.0b4, numpy 2.5.5, scipy 1.18.1, psutil 7.2.2, pandas 3.1.1)

- **The existing suite, before and after** (`evidence/suite_before/`, `suite_after/`, one `unittest -v` report per
  module; `SUITE_BEFORE_MODULES.txt`, `SUITE_AFTER_MODULES.txt`; **`SUITE_COMPARISON_v2.txt`**). Both runs: 45 modules,
  571 tests by unittest's own count. The corrected comparison identifies all 571 in each run (v1 identified 563:
  it missed tests that print text before their result) and also compares each module's test count and unittest's
  verdict line; it refuses to report "nothing changed" unless every test was identified. Result: no module and no
  test changed, disappeared or appeared. **Three tests fail in both runs, with eight failed assertions in all:**
  `test_mhupa_launchers` `test_gitignore_lines` (one); and in `test_multigame_reader_contracts`,
  `test_master_source_and_ledger_file_hashes` (two sub-tests, Powerball and Oz Lotto: the master's hash against
  the version-1 value) and `test_only_legacy_e1_allowed_at_boundary` (five: four sub-tests and a final assertion,
  each "ValueError not raised"). They exist on `main` today and are not touched by step 1.
- **The equivalence check on the moved code, for the scored forecasts only**
  (`evidence/EQUIVALENCE_CLOUD_MOVED_TREE.txt`; the original output, unchanged). Every scored development forecast
  in the tracked rank ledgers was computed again and has its old `canonical_content_digest`: Powerball 11,442 of
  11,442 and Oz Lotto 5,958 of 5,958, in 40 variants each; about 35 minutes on one core. **This is not the complete
  check.** The first version of the program called it "RESULT: PASS"; the corrected program calls the same
  coverage PARTIAL, because the tracked batch records list 17,280 and 8,760 published forecasts and the cloud copy
  holds no old record for 5,838 and 2,802 of them (`evidence/EQUIVALENCE_CLOUD_COVERAGE_STATUS.txt`). The complete
  result can only come from the owner's PC.
- **Coverage is now checked** (`evidence/EQUIVALENCE_COVERAGE_PROBE.txt`). The program takes the list of every
  published run from the tracked batch segments and requires an old digest for each. In a reduced probe tree
  (one variant per game, its never-scored forecasts published into run folders by the unmoved code): everything
  present gives `RESULT: PASS - COMPLETE`; one game only gives PARTIAL; one run folder removed gives `MISSING: 1`
  and PARTIAL; a run folder without its receipt is REFUSED. The moved code also reproduced those 244 never-scored
  forecasts of the unmoved code exactly.
- **The check can fail** (`evidence/EQUIVALENCE_PLANTED_FAULTS.txt`; the original output): two faults planted in a disposable copy (a
  changed constant in `E_006/beta_bernoulli.py`; a changed line in `E_002/core_v1.py`) gave DIFFERENT and FAILED
  lines and RESULT STOP, exit code 1.
- **The old run folders are read too:** two real run folders made with the unmoved code in a disposable clone (one
  PREDICTION_AVAILABLE, one INSUFFICIENT_HISTORY) were found and reproduced by the moved code.

## The install package (`STEP1_Layout_Install_v2`, built by `build_step1_pkg.py`)

- **What it holds:** `repo_overlay/` (95 new paths and 15 modified files); `DELETE_PATHS.txt` (16 paths: the 15 old
  places of the moved files and `contract_adapters/__init__.py`); `VERIFY_STEP1_INSTALL.py` (the project's reviewed
  read-only verifier template, `wf1/verifier_template.py`, filled in: phases pre, post, committed; 25 guarded
  files, the results masters among them); `INSTALL_MANIFEST_SHA256.txt`; `tools/` (the suite runner, the comparison
  and the equivalence check, so that their bytes are fixed with the package); `INSTALL_AND_RUN_SHEET.md`.
- **The sheet's order** (each part on the owner's own go): his ZIP of the project folder; `git pull` and the suite
  as it is today; PRE, copy, delete, POST; the same suite again and the comparison; the equivalence check, with
  the moved code in place and nothing yet committed; stage, commit, COMMITTED; push only after `COMMITTED PASS`.
  The equivalence check comes before the commit so that a difference is found before anything is pushed.
- **v2 differs from v1 only in** `tools/check_layout_equivalence.py`, `tools/compare_suite_reports.py`,
  `INSTALL_AND_RUN_SHEET.md`, the package's name and the verifier's base commit. The overlay, the deletions list,
  the manifest's entries and `tools/run_suite.py` are identical (compared with `diff` and `cmp`). The exact
  differences are `evidence/EX277_*.diff`.
- **Rehearsed** (`evidence/INSTALL_REHEARSAL_v2.txt`; `rehearse_install.sh`): PRE, POST and COMMITTED PASS in an LF
  checkout and in a `core.autocrlf=true` checkout; four planted cases each STOP (a stray file; wrong bytes in a
  copied file; the deletions left out; a changed results master). The tree the rehearsal installs equals the
  tested tree in `src/` and `tests/` (compared with `diff -r`).
- **The suite is not run by the usual suite runner with fixed counts,** because two modules fail on `main` today.
  The sheet runs one baseline before the install and the same suite after, and compares them test by test.

## Not tested, and limits

- **Nothing has run on Windows or on the owner's Python 3.15.2.** The cloud workspace has a 3.15 beta and newer
  library versions than his. That the old digests are reproduced there anyway is reassuring, not proof.
- **The forecasts that were never scored** (5,838 for Powerball and 2,802 for Oz Lotto: the published runs in the
  tracked batch segments that have no rank-ledger line) have their digests only in the old run folders on the owner's PC. Only his
  own run of the check covers them.
- The full run over the 17,400 scored forecasts was made with the first version of the checker. It was not run
  again: the corrections change what the program counts and reports, not how a forecast is computed again
  (`evidence/EX277_check_layout_equivalence_v1_to_v2.diff`), and its output is kept unchanged.
- The suite reports in `evidence/` were made with the first version of `run_suite.py`. The packaged version (it takes
  the running Python and writes `MODULES.txt`) was then run once more on the moved tree: 45 modules, 571 tests, the
  same line for every module as the first tool's run, and no test changed against the baseline.
- The sheet's Windows commands (`xcopy`, `git rm --pathspec-from-file`, the `.venv` path) are written from the earlier
  packages' sheets and are not run here: the rehearsal used `cp` and the same Git command on Linux.
- The worker-process test E2R-T12 ran in the cloud workspace with the rest of the suite, in both runs (the owner
  has allowed it there: decision log entry 159).

## Coding practices

Met for every newly written file (`method_table.py`, the `method.py` template, the four tools). The moved files
are untouched beyond their import lines, by design.

## Holdout statement

No draw value appears in this note or in the tools. The check reads the tracked score records and the masters
through the project's reader, as the project's own programs do. Every draw is an ordinary draw (RAT-40).
