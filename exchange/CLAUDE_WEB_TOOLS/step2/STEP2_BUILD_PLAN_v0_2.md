# Build step 2 (the research engine, in DEV) - build plan v0.2

**Date:** 23 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status:** a working plan, not a design
and not a rule. The authority is the specification v0.6, the deployment design v0.12 and the coding practices
(RAT-40). The owner's go: decision log entry 176. Nothing here authorises any operation on the owner's PC.
**Why it exists:** so that the build can be followed, redirected early, and resumed by another chat. Each choice below
that the specification leaves open is marked RECOMMENDED, with the alternative; the reviewer and the owner judge them
with the code (H-1 v9 section 8.2).
**v0.2 (23 November 2026) brings section 2's table into line with the code as built:** one more module
(`game_state.py`) and the program behind the launchers (`src/research_command.py`); `code_identity.py`, `settings.py`,
`job_lock.py` and `results_step.py` are classed `derived`, because the job imports them and the class test now takes
the job as an entry point of the code that makes derived results; `research/__init__.py` fixes the numerical libraries
to one thread. v0.1 is kept beside this file. Nothing else is changed.

## 1. The work item

- **Item:** build step 2 of specification 17.4: the lists, the research job with its fill and catch-up, scoring, the
  reports, both OV-1 scores, the status file and withdrawal (specification sections 3 to 11), with the header
  identities and the checks of 5.6A and 5.8 from the first day, RAT-40's start-and-end warnings, and the coding
  practices.
- **Risk tier:** HIGH (the reader and the permitted view, the list writer, scoring, the readout, OV-1, the status file).
- **Author:** Claude. **Reviewer:** the ChatGPT reviewer chat (entry 175).
- **Not in step 2** (step 3 or 4): `Init_Tree`, `Install`, `Reinstall_Infra`, the readiness marker and the static import
  check, backups, restore, the PROD updater's launch from the job, the process-table rule, `INSTALLED_FILES.json`; the
  rerun, `Check_Forecasts`, the two copies from PROD, the correction command.

## 2. Where the new code goes, and what it reuses

**New code is one new package, `src/research/`,** beside the old system, which is not edited (specification 17.3: "new
code is added in DEV beside the old; nothing is removed"). The old suite's 571 tests therefore keep their results.

| New module (`src/research/`) | What it does | Specification | Class (12.4) |
|---|---|---|---|
| `__init__.py` | the package; sets the numerical libraries to one thread before NumPy loads | 5.4 | forecast |
| `settings.py` | reads `ENVIRONMENT.ini`; role, roots; the checks of deployment design section 1 that apply to one tree | 2; DD 1 | derived |
| `variant_folders.py` | finds families and variants; validates `VARIANT.json`; the fingerprint; undeclared files refused | 3.2, 3.4 | forecast |
| `code_identity.py` | reads `deploy/INFRA_MANIFEST.ini`; the forecasting-code identity; the scoring and OV-1 code digests | 12.4 | derived |
| `reader.py` | the accepted results on file; the permitted view (the draws before the target, nothing else) | 6; 5.4 | forecast |
| `method_api.py` | the one exception type a method raises for a failure of its own mathematics | 5.3 | forecast |
| `readout.py` | scores to ranking, ties, TOP and WORST | 1.2 (E2R-1 section 7) | forecast |
| `forecast_engine.py` | one target of one variant: view, task, `compute`, readout, `verify`, the line's content | 5.3, 5.4, 6 | forecast |
| `variant_lists.py` | the two list files: header, chain, append, torn last line, the invariants | 5.1 to 5.6 | derived |
| `status_file.py` | `VARIANT_STATUS.ini`: read, check, write by rename | 3.5 | derived |
| `game_state.py` | one game's records as the job holds them: variants, lists, statuses; what is foreign or held | 5.6 (5), 5.6A, 5.7 | derived |
| `scoring.py` | the one scoring function and the score line | 8, 5.5 | derived |
| `ov1_numeric.py` | the passed kernel, copied byte for byte from the MHUP-B slice 2 | 10.1 | derived |
| `ov1_ledger.py` | the prevailing ledger and the exploratory score | 10.2 to 10.7 | derived |
| `derived_check.py` | the full check of scores and ledger; `NOT_CURRENT_FROM.json`; stale reports moved | 5.8 | derived |
| `reports.py` | league, next-draw and OV-1 print-outs; `README.txt` | 9, 10.5, 10.6 | derived |
| `results_step.py` | QA and DEV: the checked copy from the place the settings name | 7.1 | derived |
| `research_job.py` | `Run_Research`: start, fill, results, catch-up, end; foreign and held lists; warnings at start and end | 7, 5.6A, 5.7 | derived |
| `withdraw.py` | `Withdraw_Variant` | 11 | derived |
| `job_lock.py` | the job lock and the updater's own lock (each an exclusive create); the orphan-marker check | 15; 11; DD 2, 9 | derived |

Also: `src/research_command.py` (the one program behind the launchers; `other`); `Run_Research.bat`,
`Withdraw_Variant.bat` (root launchers; `other`); `deploy/INFRA_MANIFEST.ini`; `ENVIRONMENT.example.ini`;
`.gitignore` lines; tests under `tests/`.

**Reused unchanged from the old system** (each is imported by the existing method files, so it is forecasting code by
the import rule and goes on the manifest as `forecast`): `_common/contract_forecast.py` (the types a method returns),
`contract_task.py` (the frozen task), `contract_records.py` (score groups, tie order, digests), `contract_vocab.py`,
`canonical_encoding.py`, `game_profiles.py`; and E_1's `multigame_e1.py` and `e1_historical_appearance_frequency.py`.
From `src/evaluation/`: the prize divisions (`divisions.py`), read when slice A's scoring is written.

## 3. Choices the specification leaves to the code (each RECOMMENDED, with the alternative)

1. **The reader.** The old `game_draws_reader.py` cannot be imported by the new engine as it stands: its loader pulls in
   the version, owner-record, dispatch, registry and runner modules of the old system, with the Mode H opening-record
   gate (H-1 v9 section 10, the watchpoint). RECOMMENDED: `research/reader.py` carries the same `DrawView` class and
   the same prefix parser, **copied without change**, with no Mode H gate; a test requires the copied definitions to be
   identical to the old module's (compared as parsed code), and requires the same view digest as the old loader for
   every target on invented masters and, in DEV, on the real ones. *Alternative:* split the old reader file in two
   and edit the old loader to import the shared half; that changes a file every old forecast passes through and
   needs the equivalence check again.
2. **The readout.** RECOMMENDED: a small native readout that calls the same functions the old assembly calls
   (`score_groups`, `tie_identity_for`, `order_groups` in `contract_records.py`), so ranking, ties, TOP and WORST are the
   old system's by construction, without the old declaration, revision, run-mode, product or receipt fields
   (specification 1.2). A test requires scores, ranking, TOP and WORST equal to the old `assemble_forecast` for every
   existing variant. *Alternative:* call the old assembly with old-style declarations; that keeps the retired fields
   alive and gives a new method no way in.
3. **What a method is given and returns (the method contract of the new system).** Unchanged for the 40 existing
   variants: `compute(task, view)` returns a `MethodOutput`; `verify(task, view, forecast, diagnostic)` raises
   `ValueError` on a mismatch. The frozen task keeps its eleven fields; the retired ones get one fixed value each for
   every variant and never enter a record. `verify` is given a record with the keys the methods read (`record_status`;
   for each barrel `label_low`, `label_high`, `scores`, `ranking`, `top`, `worst`, `probability`).
4. **`METHOD_FAILED`** (5.3): `compute` raising `research.method_api.MethodFailed`; the readout refusing the output;
   `verify` raising `ValueError`. **Any other exception writes no line and stops the game.** No existing method raises
   `MethodFailed` today; a `ValueError` out of `compute` is therefore a stop, not a recorded failure.
5. **A probability vector** returned by a method is validated by the readout (a list of floats, one for each number)
   and handed to `verify`; it is not stored, because the line's content is the scores, the ranking, TOP and WORST
   (5.3), and for the variants that publish one it equals their scores.
6. **Results that changed other than by growing** (7.1) are found from the lists themselves: each forecast line holds
   the digest of its permitted view, so the newest line of a list must equal the digest computed from the file now on
   file; a difference is located by halving and the draw is named. The file's version and SHA-256 for the envelope
   come from its ledger's last row, which must name the file on disk.
7. **DEV's research results are not tracked by Git** (`results/research/`, `results/research_set_aside/`, `records/`,
   `scratch/`, `ENVIRONMENT.ini`, `VARIANT_STATUS.ini` in `.gitignore`). They are the state of one tree, rebuilt by a job.
   *Alternative:* track them; about 40 MB a game and a commit at every job. **The owner may choose otherwise.**
8. **In DEV, until PROD exists** (step 3), the settings name no place to copy results from: the results step is "left
   out", so no eligibility draw is written and DEV has no prevailing OV-1 yet (7.2, "the first job with the updater
   failing"). The copy and the eligibility rule are built and tested now, on invented trees.
9. **The process-table rule** (deployment design 9) arrives with the launchers' guard in step 3, where it is listed
   for QA and PROD. Step 2's job takes the job lock and makes the orphan-marker check.

## 4. Slices (for review as they are ready; installed once, at the end, on the owner's own go)

- **A. Identity and records:** `settings`, `variant_folders`, `code_identity` (with the manifest and the class test),
  `reader`, `method_api`, `readout`, `forecast_engine`, `variant_lists`, `status_file`, `scoring`.
- **B. The job and OV-1:** `job_lock`, `results_step`, `ov1_numeric`, `ov1_ledger`, `derived_check`, `research_job`,
  `withdraw`.
- **C. Reports and launchers:** `reports`, the two `.bat` files, `ENVIRONMENT.example.ini`, the `.gitignore` lines; the
  owner's sheet, which ends with DEV's first full fill and the first measured timings (specification 20).

## 5. Tests (specification 18; invented games and toy variants unless marked)

Records (F01) and the planted crashes of 5.7; N-1 (F06); the job's examples of 7.2 line for line; the status file;
withdrawal (F02, R5-F01); OV-1 (F03) including "QA and PROD agree"; the derived check (R6-F02, R7-F01 as far as it
needs no rerun); roles as far as one tree's settings go; the class test (N01). **Oracles against the old code, in
DEV:** the copied reader against the old loader; the native readout against the old assembly; **(real)** every
forecast of DEV's first full fill against the old development records (score of every number, ranking, TOP, WORST) -
the transition check's comparison, made early because it is cheap here. One planted fault for each rule. The whole
suite before and after.

## 6. Settled in this package, as H-1 v9 section 10 asks

- The exact clause list for E2R-1 section 7: in the package note, from the readout as built.
- Specification 17.3's pointer to the simplification design v0.1 section 10: this plan's section 2 and the package
  note's table of what the engine imports are the list.
- Line endings: the fingerprint and the code identity hash bytes on disk. In DEV on Windows, Git's `core.autocrlf`
  gives CRLF working files; identities are then DEV's own, which is harmless while DEV's lists are DEV's. The
  `.gitattributes` pin for `src/` is put to the owner with step 3, when files first travel to another tree.
- The Mode H opening-record gate: not present in the new reader; the old one is untouched.

## 7. Open questions for the owner (none blocks the build)

1. Item 7 of section 3: DEV's research results untracked by Git (RECOMMENDED), or tracked?
2. Review in slices as they are ready, one install at the end (RECOMMENDED), or one review of the whole?
