# Build step 1 (the folder layout) - package note, DRAFT v0.1

**Status:** a working draft by the Claude web chat, 22 November 2026. Not reviewed. Nothing is installed: no file
of `src/` or `tests/` in the repository is changed. The owner's go for build step 1 is decision log entry 158.
**Still to come before this is a package:** the install overlay with its verifier and instructions, and the owner's
run sheet. This note and the files beside it are what the reviewer needs to review the change itself.

## Work-item card

| | |
|---|---|
| Item | BUILD-STEP-1: the folder layout (specification 17.3 phase 1; 17.4 step 1) |
| Author / reviewer | the Claude web chat / the ChatGPT reviewer chat |
| Base commit | `fdb1f91` (`src/`, `tests/`, the root `.bat` files and `requirements.txt` equal `cc0ab73`) |
| Scope | method files moved to the family and variant layout; three shared helpers renamed; the runner's table built from the folder tree; imports and test references follow. No computation, contract or record changes |
| Risk tier | HIGH (it touches the code every forecast passes through), kept small |
| Owner gate | entry 158 (the go, cloud workspace only). On his PC, each on his own go: the suite baseline, his ZIP, the install, the equivalence run sheet |
| Evidence state | IMPLEMENTED and AUTHOR-TESTED in the cloud workspace. Not REVIEWED, not installed, not run on Windows |

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
  module; `SUITE_BEFORE_MODULES.txt`, `SUITE_AFTER_MODULES.txt`; `SUITE_COMPARISON.txt`). Both runs: 45 modules,
  571 tests by unittest's own count, the same count and exit code module by module. Two modules fail in both, with
  the same tests: `test_mhupa_launchers` (`test_gitignore_lines`) and `test_multigame_reader_contracts` (two tests
  pinned to the version-1 masters). No test changed its result, disappeared or appeared.
- **The equivalence check on the moved code** (`evidence/EQUIVALENCE_CLOUD_MOVED_TREE.log`): RESULT PASS. Every
  scored development forecast in the tracked rank ledgers was computed again and has its old
  `canonical_content_digest`: Powerball 11,442 of 11,442 and Oz Lotto 5,958 of 5,958, in 40 variants each. About
  35 minutes on one core.
- **The check can fail** (`evidence/EQUIVALENCE_PLANTED_FAULTS.log`): two faults planted in a disposable copy (a
  changed constant in `E_006/beta_bernoulli.py`; a changed line in `E_002/core_v1.py`) gave DIFFERENT and FAILED
  lines and RESULT STOP, exit code 1.
- **The old run folders are read too:** two real run folders made with the unmoved code in a disposable clone (one
  PREDICTION_AVAILABLE, one INSUFFICIENT_HISTORY) were found and reproduced by the moved code.

## Not tested, and limits

- **Nothing has run on Windows or on the owner's Python 3.15.2.** The cloud workspace has a 3.15 beta and newer
  library versions than his. That the old digests are reproduced there anyway is reassuring, not proof.
- **The forecasts that were never scored** (the "not enough history" records: 5,838 for Powerball and 2,802 for Oz
  Lotto, by the batch records' counts) have their digests only in the old run folders on the owner's PC. Only his
  own run of the check covers them.
- The first run of the full check used the program before a correction to its run-folder reader (two field
  names). That part of the program was not exercised in that run; nothing else in it changed.
- The suite reports were made with the first version of `run_suite.py`, which also ran every module.
- The install overlay, its verifier and the instructions are not built yet.
- The worker-process test E2R-T12 ran in the cloud workspace with the rest of the suite, in both runs.

## Coding practices

Met for every newly written file (`method_table.py`, the `method.py` template, the four tools). The moved files
are untouched beyond their import lines, by design.

## Holdout statement

No draw value appears in this note or in the tools. The check reads the tracked score records and the masters
through the project's reader, as the project's own programs do. Every draw is an ordinary draw (RAT-40).
