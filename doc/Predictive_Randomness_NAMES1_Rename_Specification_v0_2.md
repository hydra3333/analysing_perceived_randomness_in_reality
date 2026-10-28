# Predictive Randomness - NAMES-1 one-off rename specification, v0.2

**Document:** the design for NAMES-1, the one-off rename of existing versioned file names to stable names (E2R-1 specification v0.3r3, sections 12A.1, 12A.4 and 12A.5; owner decisions D-4 and D-7, 28 October 2026).
**Version:** v0.2 DRAFT for focused RECHECK, 28 October 2026 (Adelaide, UTC+10:30). v0.2 answers the R-3 review of v0.1, `Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md` (`30d24ed02ff4ba3b0c84c760f306c8bfd02ddd2717db61013e60f855e3ace85a`; 0 BLOCKER, 4 CORRECTION, 1 OPTIONAL, 1 RECONSIDER). Section 10 lists the changes.
**Author:** Claude (primary designer and coder). **Independent reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner.
**Status:** DRAFT. A design only. It authorises no rename, no source change and no run. The NAMES-1 code package follows only after this design is reviewed and ratified and the owner authorises execution.
**Base:** repository commit `38fc60e03ea0766f72476cbab7c0e1eb5bd59d07`.
**Risk tier:** HIGH. NAMES-1 changes import lines in the reader and the coordinator (always-review subjects), so the code package always gets an independent RECHECK, whatever its size.
**Holdout statement:** no draw outcome appears here. Design evidence used only the accepted offline suite in a disposable copy.

**Tags.** **DECIDED** cites an owner decision or ratified text; **RECOMMENDED** is a design choice proposed for ratification; **OPEN** is a decision for the owner, with a recommendation. Requirement IDs are `N1-Rnn`; tests are `N1-Tnn`.

---

## 1. Purpose in plain English

Many current files carry a version in their name: `game_draws_reader_v1.py`, `e1_historical_appearance_frequency_v0_3.py`, `test_multigame_exit_receipt_v0_8.py` and so on. The number is a development draft or interface number, not a method revision. Under the owner's new rule that `src/` holds current code only with stable names (D-4), these names mislead. NAMES-1 renames them once, updates every reference on an exact reviewed list, and changes nothing else, with proof.

## 2. Principles

- **N1-R01 (DECIDED; E2R-R60, D-7; bounded by v0.2).** NAMES-1 changes file names and the references to them, and nothing else. Every edited file equals its predecessor with exactly the substitutions on the allowlist (section 5A): 94 sites in 27 files, each with its category. Any other change is refused. No schema, record identity, golden or scientific constant changes.
- **N1-R01A (RECOMMENDED; v0.2).** Not every reference is a plain import. Some are text that the code or a test compares with a file or module name. Those literals **must** change, because leaving the old name would break or silently weaken the check they belong to. Changing them keeps the check's existing purpose; it does not leave the literal text unchanged. The allowlist names each one:
  - **A, imports and module paths** (84 sites): `import` and `from` lines, including relative imports and one test-to-test import, and two `mock.patch` target strings in `test_e1_standalone`;
  - **B, file-name and path literals** (7 sites): the coordinator's exit-receipt issuer location and the two tests that check it (B1); the exit-receipt module's list of contract files it hashes (B2); two tests that read the lifecycle module's source to check it (B3);
  - **C, negative firewall assertions** (2 sites): the static test that forbids any method file other than E_001 from importing the shared reader. Keeping the old literal would let a method import the renamed reader unnoticed, so it must name the current reader. The new literal is a shorter substring, so the check stays at least as strict;
  - **D, documentary text** (1 site): a docstring in `multigame_e1` that names E_1's module.
- **N1-R01B (DECIDED by the code; recorded in v0.2).** One B2 consequence is visible in records. A coordinator exit receipt records `contract_modules_sha256`, keyed by the contract files' names, and recomputes it on consumption. After NAMES-1 the keys are the new names, so a receipt issued before NAMES-1 no longer verifies afterwards, and is refused. That is the same fail-closed result as any edit to those two files. No scientific receipt can exist yet (the three switches are False and the allowlist is empty), synthetic receipts are made afresh for each run, and no committed fixture holds a receipt.
- **N1-R02 (DECIDED; E2R-R60).** The eleven protected coordinator functions stay AST-identical to v0.6. The two coordinator edit sites (three lines) are in `coordinator_main` and at module level, outside the protected functions.
- **N1-R03 (DECIDED; E2R-R14A, E2R-R60).** E_1 keeps revision 1. NAMES-1 records that decision explicitly, on the strength of the substitution-equality proof (section 5), not on unchanged goldens alone. The exception is scoped to NAMES-1.
- **N1-R04 (DECIDED; delivery method, register v0.6).** Delivery is by whole files, with explicit renames. The owner runs a listed `git mv` for each rename, then copies an overlay of the edited contents. The read-only verifier proves that each old path is gone, each new path has the expected bytes, and nothing else changed. There are no hand edits.

## 3. What is renamed (RECOMMENDED scope)

Eighteen runtime modules and nine current test modules: 27 files. Folders do not change.

| Old path | New path |
|---|---|
| `src/methods/_common/e1_common_reader_bridge_v1.py` | `src/methods/_common/e1_common_reader_bridge.py` |
| `src/methods/_common/e1_historical_appearance_frequency_v0_3.py` | `src/methods/_common/e1_historical_appearance_frequency.py` |
| `src/methods/_common/e1_standalone_contract_v0_1.py` | `src/methods/_common/e1_standalone_contract.py` |
| `src/methods/_common/e1_training_view_v0_1.py` | `src/methods/_common/e1_training_view.py` |
| `src/methods/_common/game_draws_reader_v1.py` | `src/methods/_common/game_draws_reader.py` |
| `src/methods/_common/game_profiles_v1.py` | `src/methods/_common/game_profiles.py` |
| `src/methods/_common/multigame_ancestry_release_v1.py` | `src/methods/_common/multigame_ancestry_release.py` |
| `src/methods/_common/multigame_console_protocol_v1.py` | `src/methods/_common/multigame_console_protocol.py` |
| `src/methods/_common/multigame_coordinated_manifest_v1.py` | `src/methods/_common/multigame_coordinated_manifest.py` |
| `src/methods/_common/multigame_e1_v1.py` | `src/methods/_common/multigame_e1.py` |
| `src/methods/_common/multigame_method_registry_v1.py` | `src/methods/_common/multigame_method_registry.py` |
| `src/methods/_common/multigame_result_registry_v1.py` | `src/methods/_common/multigame_result_registry.py` |
| `src/methods/_common/multigame_standalone_contract_v1.py` | `src/methods/_common/multigame_standalone_contract.py` |
| `src/methods/_common/multigame_synthetic_scorer_v1.py` | `src/methods/_common/multigame_synthetic_scorer.py` |
| `src/methods/_common/multigame_worker_launch_handshake_v1.py` | `src/methods/_common/multigame_worker_launch_handshake.py` |
| `src/coordinator_private/multigame_coordinator_exit_receipt_v2.py` | `src/coordinator_private/multigame_coordinator_exit_receipt.py` |
| `src/coordinator_private/multigame_launch_spec_v1.py` | `src/coordinator_private/multigame_launch_spec.py` |
| `src/coordinator_private/multigame_windows_lifecycle_v1.py` | `src/coordinator_private/multigame_windows_lifecycle.py` |
| `tests/test_multigame_console_and_synthetic_scorer_v0_4.py` | `tests/test_multigame_console_and_synthetic_scorer.py` |
| `tests/test_multigame_exit_receipt_v0_8.py` | `tests/test_multigame_exit_receipt.py` |
| `tests/test_multigame_launch_and_manifest_v0_8.py` | `tests/test_multigame_launch_and_manifest.py` |
| `tests/test_multigame_science_allowlist_v0_8.py` | `tests/test_multigame_science_allowlist.py` |
| `tests/test_multigame_v011_reader_contracts.py` | `tests/test_multigame_reader_contracts.py` |
| `tests/test_multigame_v011_static_and_timing.py` | `tests/test_multigame_static_and_timing.py` |
| `tests/test_multigame_windows_lifecycle_review_v0_9.py` | `tests/test_multigame_windows_lifecycle_review.py` |
| `tests/test_p2_r1_t05_hardening_v1.py` | `tests/test_t05_hardening.py` |
| `tests/test_p3_e1_standalone_v0_1.py` | `tests/test_e1_standalone.py` |
**Kept exactly as they are, because their version is a real identity, not a file-naming habit:**
- every schema, variant, profile and tie identifier inside the code (for example `MULTIGAME_E1_FORECAST_V1_REVIEW`, `FULL_HISTORY_RAW_COUNTS_V1`, `POWERBALL_PROFILE_V1`, `TIE_SHA256_V1`). These are record identities, and renaming them would change hashes;
- the frozen fixtures `tests/p3_e1_synthetic_v0_3.json` (the goldens' fixture) and `tests/fixtures/coordinator_v0_6_baseline/Powerball_Experiment_Coordinator_v0_6.py.txt` (the committed v0.6 coordinator; the AST anchor);
- the negative checks that forbid retired module names (`_common.lotterywest_api_client_v1`, `_common.multigame_results_build_v1`, `_common.multigame_offline_source_pipeline_v1`, `_common/multigame_coordinator_exit_receipt_v1.py`). These are not in the map and are untouched;
- two arbitrary module names that tests give to files they load by path (`e001_multigame_synthetic_review`, `synthetic_probe_v08`). They are labels, not file names, and are untouched;
- history: everything under `review/` and `doc/`, and the committed backup `transitory_data/E_001_before_commitB_recovery.py.bak`.

## 4. What NAMES-1 does not do

- **N1-R05 (OPEN-N1; refines ratified D-4, so the owner decides; section 8).** As proposed, NAMES-1 does **not** create per-method folders or move E_1's code, and it does not claim to put D-4's folder rule into practice. The reasons:
  1. The ratified Option F wrapper `Run_Experiment.bat` accepts only a bare file name directly in `src\methods` and runs from that folder. Moving `E_001_Historical_Appearance_Frequency.py` would mean changing the wrapper, which is provisional under ERR-R2-02 and tied to owner Windows gates.
  2. Architecture's own layout is `src/methods/E_###_name.py`.
  3. The shared reader imports `canonical_bytes` from E_1's module, so moving that module into an E_1 folder would make shared code depend on a method folder. Separating the shared encoding out is a code change, not a rename.

  The proposed reading of D-4 (option A in section 8): each method's **entry file** stays at `src/methods/E_<nnn>_<Name>.py`, and its **folder** `src/methods/E_<nnn>/` holds its method-specific modules and its `IN_DEVELOPMENT.txt` flag. Folders are created when a method's code first arrives (E_2 first). E_1's modules stay in `_common` under stable names, until a separate, reviewed E_1 package moves them, if the owner wants that. Under A, the static import-firewall test, which today scans only `src/methods/*.py`, must be widened to the method folders when the first one arrives, in the E_2-readiness code package; NAMES-1 does not change its scope. Whichever option the owner picks, the E_2-readiness admission rule (an active `SUPPORTED` registry entry **and** no `IN_DEVELOPMENT.txt`) is unchanged.
- **Out of scope (OPEN-N2), listed so nothing is forgotten.** NAMES-1 does not run, import, rename or retire any of these:
  - the **owner's data tools**: `src/results_master_v0_1.py` (run by `Run_Results_Updater.bat`), the `src/two_site_results_check_v0_2.py` .. `_v0_7.py` series, and `src/scrape_australian_powerball_history_from_2018_04_19_v0_3.py`. H-1 says Claude does not rewrite or invoke them, and they touch data acquisition. Which of them are still in use is the owner's to decide;
  - the **legacy one-off test scripts**: `tests/p0_static_checks.py`, the `tests/p1p2_*` scripts (including the `_v0_3` .. `_v0_6` interlock scripts), `tests/windows_architecture_poc_suite.py` and `tests/prepare_p3_e1_synthetic_csv_v0_1.py`;
  - the POC probe workers, which have no version in their names;
  - everything under `review/` (history; its old kit scripts will no longer import against the new names, which is acceptable for history).

## 5. Proof plan (E2R-R60; reviewer's ADD-C07; corrected in v0.2)

| Test | What it proves |
|---|---|
| N1-T01 | **No stale reference anywhere live.** (a) A whole-word scan of every `.py` file under `src/` and `tests/` finds no old map name. (b) The same scan of every other live file, of any type, outside `review/`, `doc/` and `transitory_data/`, finds none either. The expected non-Python reference allowlist is **empty**: no `.bat`, `.cmd`, `.txt`, `.json` or other live file names a map file, before or after NAMES-1. (c) The six `.bat` files are byte-identical, and the verifier guards that. (d) No `.py` or `.pyc` with an old map name exists under `src/` or `tests/` outside `__pycache__`. |
| N1-T02 | **Substitution equality against the exact allowlist** (section 5A). Each edited file is rebuilt from its predecessor by replacing only the allowlisted (line, token) sites and must then be byte-identical to the new file. Every other file, including each pure rename at its new path, is byte-identical to its predecessor, and the file count is unchanged. The check prints every authorised change with its category, so each B, C and D site is shown, not just counted. |
| N1-T03 | **AST equality.** For every edited module, the predecessor's AST, with the same allowlisted substitutions applied to its import names and string constants, equals the new AST. |
| N1-T04 | The eleven protected coordinator function ASTs are unchanged: the existing no-skip TH-1 test, against the v0.6 fixture. |
| N1-T05 | **Import origin, in a fresh interpreter.** Each check runs in its own new `python -I -B` process with an explicit `sys.path` (`src`, `src/methods`, `tests`) and no `PYTHONPATH`, so nothing already imported or left on a path can help. For each of the 27 map entries: `find_spec(old)` is `None`, and the new name imports with that `__name__` and its `__file__` resolving to the new path. |
| N1-T05A | **Category B and C checks, with mutations** (v0.2). (1) The coordinator's issuer literal is the new file name only; its comparison and refusal lines are unchanged; and in a fresh interpreter the receipt module's resolved `__file__` equals the coordinator's expected issuer. (2) Mutation: the old issuer literal fails closed (`FileNotFoundError` from `resolve(strict=True)`), so it cannot pass silently. (3) The receipt's contract-file hashes are computed from the two renamed files. (4) Firewall control: the renamed tree passes the static firewall test. (5) Mutations: a probe method file containing `from _common.game_draws_reader import DrawView`, or `import _common.game_draws_reader as r`, makes the firewall test fail. (6) Demonstration: with the old literal kept, the same probe passes, which is why the literal must change. (7) The base tree passes the same firewall test before the rename. Mutations run in disposable copies only. |
| N1-T06 | Wrappers and launch. No `.bat` file changes (N1-T01(c)). The standalone E_1 contract test and the synthetic worker tests pass under the new names. |
| N1-T07 | The E_1 legacy goldens, the prefix-only and view regressions and T-05: the full offline suite under its new module names. |
| N1-T08 | The three switches are still False and the allowlist is still empty (existing tests, plus a verifier guard). |
| N1-T09 | **Windows, all 79 current tests** (v0.2). The owner runs both commands below on Windows, Python 3.14, with a read-only per-module reporter in the package that prints each module's tests run, skips with their reasons, and result, plus the platform and Python version. Expected per module: reader contracts 10, static and timing 6, launch and manifest 11, exit receipt 18, science allowlist 6, console and synthetic scorer 7, T-05 hardening 2 (60 in all); E_1 standalone 13, lifecycle review 6 (19 in all). The two symlink tests (in reader contracts and exit receipt) **may** skip where Windows does not allow symlinks, as before; that is an expected possibility, not a required count. Any other skip, a different count, or any failure stops the install for examination. Both extra modules are offline and synthetic: the lifecycle review module never starts a Windows process, and the E_1 standalone module uses invented CSVs in temporary folders. Adding them authorises no destructive, lifecycle or process-kill test. |
| N1-T10 | **Immediate installation-recovery check** (v0.2). While the recorded NAMES-1 commit still exists, a `git revert` of it in an isolated, disposable clone restores every old path and passes the old suite. This is a check made at install time only. It is not a promise of later rollback or historical replay, which may not be possible after the owner cleans Git history. NAMES-1 adds no per-file historical hashes, archive commit IDs or run-time attestations for rollback. |

**The 60-test standard offline suite (new names):**
`PYTHONPATH=src:src/methods:tests python -m unittest tests.test_multigame_reader_contracts tests.test_multigame_static_and_timing tests.test_multigame_launch_and_manifest tests.test_multigame_exit_receipt tests.test_multigame_science_allowlist tests.test_multigame_console_and_synthetic_scorer tests.test_t05_hardening`

**The other 19 current tests (new names):**
`PYTHONPATH=src:src/methods:tests python -m unittest tests.test_e1_standalone tests.test_multigame_windows_lifecycle_review`

On Windows CMD: `set PYTHONPATH=src;src\methods;tests`, then each `python -m unittest ...` line, then `set PYTHONPATH=`.

## 5A. The allowlist (v0.2)

`allowlist.tsv` lists all 94 authorised sites: new path, old path, line, old token, new token and category. It is built by `build_allowlist.py`, which classifies an import line as A automatically and requires every other site to be one of the twelve fixed entries below, and each of those twelve to be found. Anything else stops it. Line numbers are those of `38fc60e`.

| Category | Site (old path:line) | Old token | Why it must change |
|---|---|---|---|
| A, 82 sites | every `import` / `from` line in the 27 files | the module's old name | the module is renamed |
| A, patch | `tests/test_p3_e1_standalone_v0_1.py:213`, `:261` | `e1_training_view_v0_1` | a `mock.patch` target must name the module that exists |
| B1, origin | `src/Powerball_Experiment_Coordinator.py:1105` | `multigame_coordinator_exit_receipt_v2` | the issuer location check must name the real file; the old name fails closed |
| B1, origin | `tests/test_multigame_exit_receipt_v0_8.py:261`, `:280` | `multigame_coordinator_exit_receipt_v2` | they check the coordinator's issuer literal and that the file exists |
| B2, contract files | `src/coordinator_private/multigame_coordinator_exit_receipt_v2.py:31` (two tokens) | `multigame_result_registry_v1`, `multigame_console_protocol_v1` | the receipt hashes these files by name (N1-R01B) |
| B3, source read | `tests/test_multigame_v011_static_and_timing.py:78`; `tests/test_multigame_windows_lifecycle_review_v0_9.py:112` | `multigame_windows_lifecycle_v1` | they read that module's source to check it |
| C, firewall | `tests/test_multigame_v011_static_and_timing.py:99`, `:102` | `game_draws_reader_v1` | the forbidden import must be the reader that exists (N1-R01A) |
| D, docstring | `src/methods/_common/multigame_e1_v1.py:3` | `e1_historical_appearance_frequency_v0_3` | it names E_1's module |

## 6. Design evidence (author-side trial; not the package)

The map was applied to disposable exports of `38fc60e` by `apply_trial.py`. These are Claude's own Linux trials (Python 3.13.17, NumPy 2.5.3), not the package's acceptance and not a Windows result:
- **The change:** 27 files renamed; 94 substitutions in 27 files, all on the allowlist (`t02_check.py`: PASS; 284 other files byte-identical; 311 files before and after).
- **Per module, before and after** (`per_module_suite.py`): 10, 6, 11, 18, 6, 7 and 2 tests (60), then 13 and 6 (19); all OK, no skips on Linux, identical before and after.
- **Fresh-interpreter and mutation checks** (`negative_checks.py`): 94 checks, all PASS. They cover the 27 path changes, the 27 old-name refusals, the 27 new-name origins, the issuer, contract-file and firewall checks of N1-T05A, and the live-file scan with the six `.bat` files byte-identical.
- **Leftover versioned names:** none in any live file, other than the out-of-scope owner tools and the kept identities of section 3.

## 7. Records that go out of date

- The H-1 v1r2 module map (section 7.1) and suite command.
- R2, R3 and Architecture mentions of the old file names.
- The TH-1 records, which name the old test modules.
- Register v0.7's out-of-date line on Architecture's standalone `.py` wording, once the owner settles OPEN-N1.

The register edition installed with NAMES-1 lists these, and records the OPEN-N1 decision; the next H-1 revision folds them in. Historical records are never edited.

## 8. Decisions for the owner

**OPEN-N1 - Per-method folders: which layout did D-4 mean?** D-4 says "a folder per method". This is a choice about a ratified decision, so it is the owner's, and it is recorded in the next register edition.
- **A (recommended by Claude and by the reviewer):** entry files stay directly in `src/methods/`, as the launch wrapper requires. Each method's folder `src/methods/E_<nnn>/` holds its own modules and its `IN_DEVELOPMENT.txt` flag, created when that method's code first arrives (E_2 first). E_1 is left as it is for now. NAMES-1 stays a pure rename and does not touch the safety-reviewed wrapper.
- **B:** the literal reading, with everything for a method, entry file included, inside its folder. That needs the wrapper and the reader reworked first, as their own separately reviewed package, before NAMES-1 or E_2.

**OPEN-N2 - Owner tools and legacy test scripts: in NAMES-1 or later?**
- **Recommendation: later, and only if you want it.** NAMES-1 leaves them exactly as they are. Any later tidy-up would be its own small package with its own scope, decided by you after checking that no wrapper depends on what is changed, and would not change how data is acquired.

**OPEN-N3 - Test file names.**
- **Recommendation:** use the stable names in section 3. In particular, `test_multigame_v011_reader_contracts` becomes `test_multigame_reader_contracts`, and `test_p2_r1_t05_hardening_v1` becomes `test_t05_hardening`. All 79 tests and their call sites are updated and proven (N1-T02, N1-T09).

## 9. What comes next

On ratification, nothing is renamed yet. The NAMES-1 code package (the overlay, the explicit `git mv` list, the read-only verifier, the per-module reporter and the evidence) is a separate HIGH-tier package: it needs the owner's authorisation to prepare and to install, and an independent RECHECK of the always-review code.

## 10. Changes from v0.1

- **N1-C01:** N1-R01 now bounded by an exact, categorised allowlist (new N1-R01A, N1-R01B and section 5A); N1-T02 compares against it and prints every authorised change; new N1-T05A adds the mutation and negative cases. The v0.1 claim that test logic is unchanged is withdrawn: B and C sites change their literal text to keep their purpose.
- **N1-C02:** N1-T09 covers all 79 tests on Windows, with per-module counts and skip reasons; the 19-test command is added.
- **N1-C03:** N1-T01 extended to every live file and an empty non-Python allowlist; N1-T05 runs in fresh `-I -B` interpreters; old paths proven absent; the issuer check proven to match the new name without relaxing it.
- **N1-C04:** N1-T10 is now an immediate installation-recovery check in a disposable clone, while the commit exists.
- **N1-O01:** the owner's tools are no longer called "superseded"; NAMES-1 does not run, import, rename or retire them.
- **N1-REC01:** OPEN-N1 restated as the owner's choice between A and B; N1-R05 no longer reads as decided.
- Also: section 3 lists the test-loader labels and history files left untouched; N1-R05 notes that under option A the import-firewall test must later be widened to method folders; section 9 says what follows ratification.

*End of NAMES-1 specification draft v0.2.*
