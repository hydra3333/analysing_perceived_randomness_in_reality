# Predictive Randomness - releases and WF-1 (the first walk-forward results, the R3 scorer and N1), design note v0.1

**Document:** the design of the work that switches the installed methods on and produces the project's first measured results over past draws: the release package, the walk-forward driver, the R3 stage-2 scorer and report, the N1 fair-draw simulator, and N1's seed policy with its NIST Randomness Beacon root.
**Version:** v0.1 DRAFT for the reviewer's design review (R-3), 30 October 2026. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule. Where it proposes to change or clarify one, the owner decision is listed in section 12.
- **No code yet:** each package follows only after this design passes.
- **Probes:** timing and numerical probes on invented data are reported in section 9. The probe and reference scripts travel with this note. They read no repository data file and no real draw.
- **Base:** `main` at `1d836c6` (wave 2 installed at `b61b1a2`; the handovers and register v0.20 at `03f7da4`).
- **The owner's order of work** (register v0.18): releases and WF-1 come now. Wave 3 (with Method B as E_45) follows.

## 1. In plain English

**What happens, in order:**
1. **The methods are switched on** (package REL-1). The 11 installed methods lose their "in development" flag, and each of their 39 variants gets a "supported" registry entry in each game. They can then run, but still only on invented test data.
2. **Real past draws are allowed for walk-forward runs** (package WF-1A). One code switch is turned on, and a new program, the walk-forward driver, runs every switched-on variant over every past draw in the development period. For each target draw it uses only the draws before it, and it freezes the prediction. That is about 1 to 2 hours for Powerball on your PC, and under an hour for Oz Lotto. It reads no results: nothing is compared yet.
3. **A random seed is chosen in public, in advance** (package SEED-1). The fair-draw simulator needs random numbers. Its seed is one NIST Randomness Beacon value, named now (this note proposes the one published at 10:30 am Adelaide time on Friday 6 November 2026), which you fetch by hand once it exists. I check it against NIST's public archive, and only then may the simulator use it.
4. **The predictions are scored and ranked** (package WF-1B). A separate report program reads the frozen predictions, and only then the actual results of those past draws. It counts matches and prize divisions per method, compares each with what fair draws give, says how surprising each result is (on the sigma scale), allows for how many methods were compared, and writes a plain-English report with a glossary. The fair-draw simulator (N1) adds 10,000 simulated fair histories for the figures that need them.

**What you get at the end:** for each game, a report (text, CSV and JSON) ranking every method's TOP and WORST picks over the past draws, with every number labelled by how far it can be trusted. The most likely result is that no method beats fair draws by more than chance; that is a real and useful finding.

**What it does not do:** it never touches the sealed holdout draws (Powerball 1577 onward, Oz Lotto 1694 onward), runs nothing through the coordinator, kills no process, opens no lottery website, and turns on no other switch. The in-sample ("hindsight") tables and the further R3 measures come later (R3 stage 3).

## 2. What the record already fixes

This note builds on these, and changes none of them:
- **Release (D-6, E2R-R57/R58; D6-3):** a method runs only with an active `SUPPORTED` registry entry for its exact variant and revision **and** no `IN_DEVELOPMENT.txt` flag. Release is a separate small reviewed package. A release alone authorises no real data.
- **Real data (D2-2; D6-4):** contract runs on real data stay off (`ENABLE_CONTRACT_REAL_DEVELOPMENT = False`) until a reviewed, owner-approved step. D6-4 names that step "WF-1": real-data contract runs, a walk-forward driver, and the R3 scorer with a first report.
- **The scorer's scope (R3 17.13, stage 2):** match records; divisions (with R2 2.5's evaluator-only supplementary rule); MR0, MR1/MR1-T, MR4, MR5, MR7 and MR16; analysis units; the report format and glossary; sigma and calibration labels; Bonferroni; families and the search log; N1. Tests MRT-01..10, 12..14, 16..19 and 22..23 (see section 11, finding R3-3).
- **Walk-forward (R3 17.3.3, 17.3.5; MRD-10):** the forecast for target N is fitted on the era's draws up to N - 1, frozen, and only then scored. The ranking tool never re-runs methods. A retrospective run is labelled `DEVELOPMENT_WF_EXPLORATORY`.
- **Windows (R3 17.3.6; MRD-04):** default report windows Powerball 1286-1576 (291 draws) and Oz Lotto 1474-1693 (220 draws); never past 1576 / 1693 in this phase.
- **N1 (R3 17.5A; MRD-17, MRD-19):** R = 10,000 replicates; exact for single-track hit-sequence statistics on a fixed grid, a labelled reference otherwise; replicates are calibration artefacts under the synthetic firewall.
- **Seeds (D-9, D-10, D-11; E2R-R63; W2-8; reminder R-004):** a root is one pre-announced NIST Randomness Beacon pulse, fetched once by hand and independently verified; runs never fetch; a later root is allowed for retrospective development runs; every root tried is logged and counted. W2-8: the seed is settled at WF-1's design, because N1 is the first part of the project that uses random numbers.
- **Option F:** one launch interface. The ranking tool's wrapper `Run_Method_Rankings.bat` is already ratified (Architecture 5A.4, 12.5).
- **The gates** that stay closed: the orphan marker, the other three switches, the empty allowlist, Mode H, FINAL, the holdout, process termination, dependency upgrades.

## 3. The packages and their order

| Package | What | Size | Owner's actions |
|---|---|---|---|
| **REL-1** | Release all 39 variants of the 11 installed methods, in both games | small | ratify, install |
| **WF-1A** | The walk-forward driver; real-development storage; the switch turned on | medium | ratify (including the switch), install, then authorise and run each game's batch |
| **SEED-1** | N1's seed policy: announced in this note; the pulse fetched, verified and approved | records only | fetch the pulse after its time; ratify the approved policy |
| **WF-1B** | The R3 stage-2 scorer and report tool, with N1, the families and the search log | large | ratify, install, then run each game's report |

- Each code package follows the routine: design (this note), code, R-2 review, Claude Code rehearsal on invented data, the owner's install, Claude's check from GitHub.
- **REL-1 and WF-1A** can be coded together and reviewed in one round, then installed one after the other.
- **The real batch runs** after WF-1A's install. It needs nothing from WF-1B, so predictions are frozen before the scoring code even exists.
- **SEED-1's approved policy** rides with WF-1B if the pulse has been verified by then; otherwise it follows as a tiny records-only package. Until it is installed, the report tool runs with N1 switched off, and says so (section 7.6).

## 4. REL-1: the release

**Contents** (generated by a script that travels with the package, as in every method package):
- **Delete** the 11 flags `src/methods/E_<nnn>/IN_DEVELOPMENT.txt` for E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19.
- **Append** 78 registry entries, `entry_0002.json`, one per variant per game:
  - `registry_status` `SUPPORTED`, with a reason naming REL-1 and the owner's decision;
  - the same `method_revision` ("1") and `declaration_digest` as `entry_0001`;
  - `previous_entry_digest` = the digest of `entry_0001`;
  - the texts (`method_name`, `one_liner`, `short_explanation`, `text_provenance`) carried unchanged.
- **Unchanged:** every declaration, all code, E_1, and the `NOT_YET_SPECIFIED` placeholder chains of E_2..E_62.
- **Test edits** (HIGH, listed and checked): the "as installed" tests of E_6, E_3/E_4, wave 1 and wave 2 now expect `SUPPORTED` and no flag, and the roster test expects these methods' variants to be released. These are expectation changes about status only; no numerical golden changes.
- **New test:** every released variant, in both games, runs through the installed registry (no simulated release) on an invented workspace to `SUCCESS`, and `read_run` consumes it.

**After REL-1:** the 39 variants run through `Method_Contract_Runner.py` on invented workspaces only. A real-data request is still refused (`REAL_DEVELOPMENT_DISABLED`).

## 5. WF-1A: the walk-forward driver and the switch

### 5.1 The program and its commands

A new entry file, `src/methods/Method_Walk_Forward.py`, is launched through the existing interface (Option F, manual path): `Run_Experiment.bat Method_Walk_Forward.py <command> ...`. It reuses `Method_Contract_Runner.py`'s `ADAPTERS` and the unchanged `run_contract_method`, in one process: no subprocess, no timer, no coordinator, no termination path.

| Command | What it does |
|---|---|
| `plan --game G --first S --last L` | Checks the request, builds and freezes the batch plan (5.2), appends one search-log row, prints the batch ID. Reads only the installed registry and the master's ledger line. |
| `run --batch ID` | Runs the plan (5.3). Re-running the same command resumes. |
| `status --batch ID` | Prints counts by variant and outcome. Read-only. |

### 5.2 The batch plan (frozen before any run)

`WF_BATCH_PLAN_V1`, written create-only to `results/real/development/wf_batches/<GAME>/<batch_id>/plan.json`:
- the batch ID (`wf-<32 hex>`), the game, the window [S, L], the creation time (UTC) and the driver's version;
- the **cohort**: every (method, variant) with an active `SUPPORTED` entry in the installed registry for the game and a runner adapter, in method-number then variant order. For each: the revision, the declaration digest, the registry entry digest, and `minimum_history_draws`. The cohort digest covers that list;
- the **master pin**: the SHA-256 recorded in the game's version-1 INIT ledger line;
- the observation view (`UNORDERED_SET`, dates off) and the run mode `REAL_DEVELOPMENT`.

**Refused at `plan`, before anything is written:** the orphan marker is present; L >= the holdout's first draw (1577 / 1694); S < E(G) + 1 (the era's first draw has no history: 5.3); an empty cohort; a ledger that is not the version-1 INIT line.

### 5.3 Running, resuming and stopping

- **Order:** cohort order, then ascending target. Each variant's whole window is finished before the next variant starts, so a partial batch still gives complete tracks.
- **Each run** is one ordinary standalone contract run (`run_contract_method`, `REAL_DEVELOPMENT`, `WF_FORECAST`), pinned to the plan's digests and master. All of the runner's own refusals apply unchanged: the orphan marker; the switch; the dispatch gate (released variant, no flag); the reader's development-prefix rule (target below 1577 / 1694; ledger, master and INIT checks).
- **A refusal stops the batch** (A STOP is a STOP). If the runner refuses (`RunRefused` or `DispatchRefused`), the driver stops at once, records the refusal, and runs nothing more.
- **A method failure does not stop it.** A run ending in `RUNTIME_FAILURE`, `NUMERIC_INVALID` or `VALIDATION_FAILURE` is the method's own result for that target. It stays on disk, is counted, and the batch goes on. It is never retried automatically.
- **Resume:** a (variant, target) pair is done when a terminal record exists for it under the plan's pins, with any outcome except `RUNTIME_FAILURE` whose reason is `INTERRUPTED` or `PUBLICATION_FAILED:`. Those two are run again. Every attempt's folder stays as it is; nothing is deleted or moved.
- **Ctrl-C** ends the current run with its `INTERRUPTED` terminal record (existing behaviour). The driver then writes its segment record and exits.
- **Segment records:** each `run` invocation writes `segment_<UTC>.json` (create-only) at its end, listing the run IDs it created and why it stopped. The scorer does not depend on them (section 6.1); they are for the owner's audit.
- **Targets with too little history:** a target with 0 < N - E(G) < `minimum_history_draws` runs normally, and the method writes its own `INSUFFICIENT_HISTORY` record (E2R-1 7.4). The era's first draw (Oz Lotto 1474) cannot be a walk-forward target at all, because it has no earlier draw and the reader refuses it, so the plan starts at S >= E(G) + 1.

### 5.4 Where the records go, and what Git keeps

- **Real-development runs** (batch runs and any single `REAL_DEVELOPMENT` run of `Method_Contract_Runner.py`) are published under `results/real/development/contract_runs/<GAME>/<METHOD>/<VARIANT>/<run_id>/`. This is a one-line change of the runner's real run root, which today is `transitory_data/contract_runs/`. `transitory_data/` is disposable and "never automatically re-input" (Architecture 13.1; R3 11.7), but the scorer must read these records, and R3 11.7 places development forecasts in `results/real/development/`.
- **Git:** a full-range batch creates about 17,280 runs for Powerball (432 targets x 40 variants) and 8,760 for Oz Lotto, each a folder of 3 small files. They are git-ignored (`results/real/development/contract_runs/`), so the clean-tree check at the start of every install still passes. The plan and segment records (`wf_batches/`, small, no outcomes) are committed by the owner after the batch.
- **Synthetic runs** are unchanged: they publish under their own workspace.

### 5.5 The switch

`ENABLE_CONTRACT_REAL_DEVELOPMENT` in `src/methods/_common/contract_runner.py` becomes `True` in WF-1A (decision WF1-3). It stays a code-level constant with no command-line or environment override.

**What turning it on allows:** standalone contract runs of **released** variants on the **development prefix** of the owner's version-1 masters. Nothing else.
- The holdout stays sealed twice over. The reader refuses any target at or after the holdout's first draw, and the version-1 masters physically end at 1576 / 1693.
- The orphan marker, the dispatch gate and the data-source check run before anything is read.
- The other three switches and the allowlist are unchanged.
- No coordinated run exists (D2-1).

### 5.6 What the owner runs (after WF-1A is installed)

For each game, in your order (decision WF1-5):
1. `Run_Experiment.bat Method_Walk_Forward.py plan --game POWERBALL --first 1145 --last 1576`, which prints the batch ID.
2. `Run_Experiment.bat Method_Walk_Forward.py run --batch <ID>` (about 100 minutes for Powerball on the probe's speed; section 9.1).
3. `Run_Experiment.bat Method_Walk_Forward.py status --batch <ID>` to see the counts.
4. Commit `results/audit/SEARCH_LOG.csv` and `results/real/development/wf_batches/` (the exact commands come with the package).

Claude Code never runs a real batch: its rehearsals use invented data only (its rulebook, rule 9).

## 6. WF-1B: the scorer and report (R3 stage 2)

### 6.1 One report run, in this fixed order

`Run_Method_Rankings.bat --game G --batch <ID> --first S --last L` (a new wrapper, already ratified in Architecture 5A.4) launches `src/evaluation/Method_Rankings_Report.py`. The new folder `src/evaluation/` holds the scorer, the outcome reader, N1 and the report writer. A static check forbids any method file from importing it, and forbids it from importing any method's code: the report tool runs no method (Architecture 12.5).
1. **Refusals that read nothing:** the orphan marker; the window (S >= E(G), L <= 1576 / 1693; MRT-14); an unknown batch; families that are not registered.
2. **The fixed grid** (6.2) from the plan alone, with its digest.
3. **Collect the frozen forecasts.** For every grid cell, the driver's run folders for that (variant, target) under the plan's pins are found and passed through `read_run`, which establishes every gate itself. If several consumable runs exist (a resumed batch), their `canonical_content_digest` must be equal. The earliest by freeze-receipt time is used (the receipt selection policy, E2R-R40A). Unequal digests are reported as `REPRODUCIBILITY_FAIL`, never hidden.
4. **The scoring plan** (`SCORING_PLAN_V1`, create-only) records the grid, the selected forecasts' content and receipt digests, and the availability counts. It is written **before** any outcome is read.
5. **The outcomes** of the grid's targets only (6.3).
6. **Records:** the score ledger and the rank-position ledger (6.4).
7. **Measures, N1, and the report files;** then exactly one search-log row (6.7).

### 6.2 The fixed grid and the comparison sets

- **A track's grid** (R3 17.3.7A) is every target N in [S, L] with N - E(G) >= max(1, `minimum_history_draws`). It depends only on draw numbers and the declaration, never on outcomes, so exact and N1-calibrated figures keep their status.
- **Availability check:** within the grid, every target must have an available ticket. Any other status (a failure, or an `INSUFFICIENT_HISTORY` record that the declaration does not predict) sets that table's significance figures to `SELECTION_UNVERIFIED`. They are still computed and shown, with the count of affected targets.
- **Finding, with numbers (section 9.2): the default intersection set fails Oz Lotto.** R3's default comparison set is the intersection of the cohort's scored sets. With this cohort:
  - for Powerball (1286-1576), the three 208-draw variants score from 1352, so the intersection is 225 draws instead of 291;
  - for Oz Lotto (1474-1693), the era began only 220 draws before the holdout, so the three 208-draw variants score only 12 draws (1682-1693), and the intersection would be those 12 draws for every track.
- **Proposed (decision WF1-6):**
  - every league table and family uses each track's own grid (R3's labelled `OWN_SET` option, n per row);
  - each game also gets one descriptive common-set table, on the intersection, labelled (Oz Lotto's carries `LOW_N`).

  Bonferroni over exact per-track p-values stays guaranteed with own-set grids, because each test is valid on its own fixed grid (R3 17.5.3 needs valid inputs and a predeclared family, not equal n). The N1 maximum statistic replays each track on its own grid.

### 6.3 The outcome reader (evaluator only)

- **A new orchestration-only function** in `src/evaluation/`, never importable by a method (static check, MRT-05).
- **Inputs:** the game, the plan's master pin, and the set of grid targets.
- **Checks first:** it applies the reader's checks (trusted single-link file; ledger version-1 INIT; full-master SHA-256 equal to the pin; INIT record), reusing the reader's file helper without editing the reader, then reads rows by the raw first field only.
- **Holdout guard:** it returns outcomes only for targets in the grid, refuses any target outside [E(G) + 1, holdout_first - 1], and never decodes a row at or after the holdout's first draw.
- **Supplementaries:** for Oz Lotto, it returns the three supplementary numbers of a target only to compute `supplementary_matches` and the division (R2 2.5, MRD-03). They are never stored: only their match count is.

### 6.4 Records

- **`POST_OUTCOME_SCORE_RECORD_V1`** (E2R-1 section 10, as installed): one per (track, target), validated by the installed `validate_score_record`. One scoring run writes all its records into one create-only ledger file, `results/real/development/scores/<GAME>/<batch_id>/<scoring_run_id>/score_ledger.jsonl`. E2R-R45A's create-only key is checked for uniqueness inside the ledger. A later scoring run writes a new ledger and never replaces one.
- **`RANK_POSITION_RECORD_V1`** (new, evaluator-only; E2R-R47): one per (method, variant, target), with `mean_rank_main` and `rank_powerball` (R3 3.1 mid-ranks from the frozen `ranked_groups`, never the tie-ordered list), and MR5's per-target fair variance. It goes in the same folder as `rank_ledger.jsonl`.
- Both ledgers contain drawn numbers (the score record's `drawn_main` and `drawn_powerball`), so they are git-ignored and never shared (6.8).

### 6.5 Measures in WF-1B

Exactly R3 stage 2, for the WF mode, per game and channel:
- **MR0** division profile;
- **MR1 and MR1-T** (surprisal score; the owner's 90/7/3 score);
- **MR4** (`X.d`, `C.d` for every division; the owner's `C.3`, `B.2-3` and `X.3`);
- **MR5** rank position;
- **MR7** total main-match excess, with its PB analogue;
- **MR16** hit-rate intervals (`ANYDIV`, every division, `M2`, `M3`, `M4`, and `PB` for Powerball).

Each is computed on its declared analysis unit (17.3.4A), on `READOUT_TRACK`s TOP and WORST. Oz Lotto has MAIN only.

**Not in WF-1B (stage 3):** MR2, MR3, MR6, MR8-MR15, the in-sample mode and the side-by-side WF/IS tables. The report says plainly that they are not produced yet.

### 6.6 Exact arithmetic everywhere (decision WF1-7)

R3 17.11 makes production tails log-space sums via `lgamma`, with an exact `Fraction` oracle in the tests. At this project's sizes (n <= 432) the exact route is fast (section 9.3), so the proposal reverses the roles:
- **Counts, sums and divisions** are integers.
- **Tails** are exact: binomial tails as `Fraction`s; MR7's null as integer polynomial coefficients.
- **Sigma** is solved from the exact tail by a `decimal` bisection on the normal tail, at 80 digits. It never forms 1 - p in floating point.
- **Clopper-Pearson bounds** are found by exact bisection.
- **MR1** uses `decimal` logarithms.
- **Conversion to float64 happens once,** at output, by correctly rounded conversion.
- **The `lgamma` route** becomes the tests' independent cross-check (MRT-04 unchanged in substance).

`decimal` and integer arithmetic are the same on every platform, so a report on Windows and Linux is byte-identical, apart from its header time and environment lines. That is W2-7's rule, applied to the scorer. MRT-08 (determinism) then holds across platforms, not only on one machine.

### 6.7 Families, multiplicity and the search log

- **Two predeclared families per game** (decision WF1-6), registered in `src/evaluation/registry/FAMILY_REGISTRY_V1.json`, installed with WF-1B and so before any report:
  - `WF1_<GAME>_MR7_MAIN_V1`: MR7.MAIN's excess p-value (P_up) for every TOP and WORST track of the REL-1 cohort, on own-set grids, in the game's default window (R3 17.3.6). M = 80 per game. For a WORST track, an excess is the "inverse signal" R3 asks about. Deficits are shown locally and are not in the family.
  - `WF1_POWERBALL_MR7_PB_V1`: MR7.PB the same way (Powerball only, M = 80).
  - **Why MR7:** it is R3's most direct every-draw test, it is exact, and it stays exact under adaptive walk-forward, so Bonferroni over it is a guaranteed global figure (R3 17.5.3, 17.18.4).
- **Everything else is exploratory:** `EXPLORATORY_COHORT`, Bonferroni over the table's actual number of tests, labelled, and counted in the search log. Any table may be produced (R3 17.5B).
- **N1 maximum statistic** per family, labelled `N1_FIXED_FORECAST_REFERENCE` (R3 17.5.3).
- **The search log** `results/audit/SEARCH_LOG.csv` (R3 7.4, 17.5B):
  - created with its header on first use, if absent;
  - each report run appends exactly one `RANKING_REPORT` row;
  - each driver `plan` appends one `WF_BATCH` row (a new row type, as R3 7.4 allows, so that every batch is counted).
  - Rows are never edited. The report header gives the row number and the counts per row type.
- **The seed policies tried** for N1 are counted from their own records (section 8.4), and the report states the count.

### 6.8 Report files, and what may be shared

- **Files:** R3 17.10.1, create-only, in `results/method_rankings/<GAME>/`: `ranking_<GAME>_WF_<S>-<L>_<UTCSTAMP>.txt`, `.csv` and `.json`. The layout follows 17.10.2:
  - the header (with the evidence tier `DEVELOPMENT_WF_EXPLORATORY` and the label "retrospective development walk-forward");
  - the glossary, with the two mode texts of 17.3.5A word for word, every measure, label and status, and PO-1..PO-4;
  - the fair-draw reference;
  - the league tables;
  - the per-track detail;
  - the notes.
- **Texts:** measure texts in `MEASURE_REGISTRY_V1`, taken word for word from R3 17.6; method texts from the registry entries.
- **No drawn numbers in report files** (decision WF1-10): only counts, statistics, draw numbers and labels. A report can therefore be attached to either chat without breaking any rule (all its draws are development draws). The ledgers, which do hold drawn numbers, stay local.
- **Git:** the report files and the search log are small, so the owner commits them; `scores/` is git-ignored.

### 6.9 Not in WF-1B

Not in scope: stage-3 measures; in-sample runs; any meta-method; holdout or Mode H; prospective forecasts; coordinated runs; any change to a method.

## 7. N1, the fair-draw simulator

### 7.1 What it computes in WF-1B

- **`N1_CALIBRATED` p-values for MR1**, a hit-sequence statistic. N1 is exact for it even under adaptive walk-forward (R3 17.5A). Its normal approximation is shown beside it, labelled `APPROX_UNCALIBRATED`.
- **A replay check of MR4, MR7 and MR16's exact tails** (MRT-16a, MRT-19). The exact figures are the ones reported.
- **MR5's reference figure,** labelled `N1_FIXED_FORECAST_REFERENCE`.
- **Each family's maximum statistic,** labelled `N1_FIXED_FORECAST_REFERENCE`.

### 7.2 The generator (decision WF1-8)

Python's standard library only, with no NumPy random API, so the simulated draws are identical on every platform and every library version:
- **Stream key** for replicate r (1..R) and target draw N: the length-prefixed fields (each a uint32 little-endian byte length, then its UTF-8 bytes, as in `TIE_SHA256_V1`):
  1. `PREDICTIVE_RANDOMNESS/N1_FAIR_DRAW_V1`;
  2. the seed policy ID;
  3. the root (the beacon's `outputValue`, 128 hex characters as published);
  4. the game ID;
  5. r, in decimal;
  6. N, in decimal.
- **Words:** the SHAKE-256 output of that key (FIPS 202), read as consecutive 64-bit little-endian unsigned integers. SHAKE-256's output for a longer request extends the shorter one, so the stream is well defined at any length.
- **Uniform integer in [0, k):** take the next word w. Accept w if w < 2^64 - (2^64 mod k), and return w mod k. Otherwise discard it and take the next word. This is exactly uniform; a rejection happens with probability below 3 x 10^-18.
- **Powerball:** a partial Fisher-Yates shuffle of 1..35: for i = 0..6, swap position i with position i + U(35 - i). The first 7 are the main set. Then the Powerball is 1 + U(20).
- **Oz Lotto:** the same over 1..47 for i = 0..9. The first 7 are the main numbers and the last 3 the supplementaries (R3 17.5A).
- **Why key by (r, N):** a target's simulated draw does not depend on the window, the cohort or the table. Every table of one game under one policy then shares the same simulated histories, and choosing a window cannot reshuffle them.
- **Monte Carlo contract (R3 17.5A):** (k + 1)/(R + 1), with the Clopper-Pearson 95% interval on k/R; R = 10,000 (MRD-19).

### 7.3 Cost

About 25 s to generate 10,000 x 291 Powerball draws, in pure Python (section 9.3). Scoring all 80 tracks on them uses NumPy integer arrays (bit masks and population counts), which are exact. That takes seconds.

### 7.4 Exact comparisons

N1 compares simulated statistics with observed ones exactly, so a tie is never decided by rounding:
- **MR7 and MR4** are integer counts.
- **MR5** uses twice the mid-rank, an integer.
- **MR1** is a sum of -log2 p_d over the divisions won. "Replicate >= observed" is decided exactly as the rational inequality: the product of p_d^(replicate count) <= the product of p_d^(observed count) (section 9.3).
- **The family maximum statistic** compares exact tail values.

### 7.5 Firewall

- Replicates and their scores are `NULL_CALIBRATION` artefacts. They are never written into a real ledger, never read by a method, and never stored by default, because they regenerate from the policy.
- N1 refuses in-sample input (MRT-06).
- N1 is not a gate: every measure is shown whether or not N1 has run (MRD-21).

### 7.6 Without an approved root

The report tool needs an installed `APPROVED` seed policy to run N1.
- **Without one,** N1's figures show `N1_NOT_RUN: seed policy not approved`, and every other figure is computed as normal.
- **There is no default, test or fallback root** in production code.
- **Tests** use an invented root through the test harness only.

## 8. N1's seed policy and its NIST root (SEED-1; D-9..D-11 applied to N1)

### 8.1 Announcement (the provisional policy)

This section is the announcement stage of E2R-R63. It is committed in `exchange/` with this note, before the pulse exists.

| Field | Value |
|---|---|
| Policy ID | `N1_ROOT_NIST_C2_20261106T0000Z_V1` |
| Purpose | the N1 fair-draw simulator (R3 17.5A) of WF-1B, both games |
| Service | NIST Randomness Beacon, version 2.0 |
| Chain | `chainIndex` 2 (the current chain) |
| Pulse | the pulse whose `timeStamp` is exactly `2026-11-06T00:00:00.000Z` (Friday 6 November 2026, 10:30 Adelaide); epoch milliseconds 1793923200000 |
| Field | `outputValue` (512 bits, 128 hexadecimal characters), used as published |
| Accepted only if | `version` "2.0", `chainIndex` 2, that exact `timeStamp`, `statusCode` 0, and a 128-hex-character `outputValue` |
| Status | `PROVISIONAL` (not runnable) |

- **No "latest", "next" or fallback pulse.** NIST's time lookup returns a different pulse when none exists at the requested time: a probe for an instant before chain 1 began returned that chain's first pulse, with a different time stamp (section 9.4). So the time stamp is checked, never assumed.
- **A missing or failed pulse:** if it does not exist, or fails a check, the policy is `REFUSED`. A new policy with a new announced pulse is needed, and it is counted (8.4).
- **The owner may choose another time:** any later whole minute (the beacon publishes one pulse a minute), as long as the choice is recorded in `exchange/` before that minute. It is the owner's choice (decision WF1-9).

### 8.2 Retrieval and independent verification

1. **After the pulse time,** you open NIST's page for that pulse in your browser: `https://beacon.nist.gov/beacon/2.0/pulse/time/1793923200000`. Save the JSON to `E:\TEMP`, and attach it to the Claude chat. Nothing in the project fetches it.
2. **Claude checks it field by field** against the acceptance row above.
3. **Claude independently reads the same pulse** from NIST's public archive at its permanent address (`https://beacon.nist.gov/beacon/2.0/chain/2/pulse/<pulseIndex>`) and compares `uri`, `chainIndex`, `pulseIndex`, `timeStamp`, `statusCode` and `outputValue`. The reviewer may also check (E2R-R63: "someone other than the person who fetched it").

### 8.3 Approval

- **The approved policy record** (`SEED_POLICY_V1`, `APPROVED`) binds the verified value, the pulse's `uri` and `pulseIndex`, who fetched it and when, and who verified it and when. It goes into `src/evaluation/seed_policies/`, reviewed and immutable, through WF-1B or a tiny SEED-1 package.
- **The provisional and approved records** both stay as history.
- **The root is seed entropy, not data** (E2R-R63). It carries no information about any draw.
- **Timing (D-11):** using a root published after the historical targets is allowed for retrospective development work, and the report says "randomness chosen for the experiment".

### 8.4 Switching and counting (D-10)

- **Switching:** you may replace the root at any time. A new root is a new policy ID; earlier policies and their reports are kept.
- **Counting:** every policy (provisional, approved or refused) stays as a file, and each report states how many N1 roots exist for its game and which one it used.
- **Scope:** later stochastic methods (Method A's diagnostics, Method B's simulated checks, wave 9) each get their own policy in their own design, under E2R-1 7.6; this one is for N1 only.

## 9. Probes and evidence (invented data only)

The scripts and their full outputs travel with this note: `probe_wf_timing.py` (output `ev_wf1_timing_powerball.txt` and `ev_wf1_timing_ozlotto.txt`) and `reference_wf1.py` (output `ev_wf1_reference.txt`). Commands: `python3 -I reference_wf1.py`, and `python3 -I probe_wf_timing.py <repository folder> POWERBALL 29` (or `OZLOTTO 44`).

### 9.1 Walk-forward timing (synthetic, through the installed contract runner)

- **Setting:** an invented full-length master; a simulated release in a temporary copy of the contract data; all 40 variants; targets every 29 draws (Powerball) or 44 draws (Oz Lotto); this Linux container.
- **Per run:** about 0.2 s for the light methods (the reader, `verify()` and publication); 0.3-0.7 s for E_3/E_4's minimax and least-squares variants; up to 1.1 s for E_18.
- **Powerball:** about 14.5 s per target for all 40 variants, so about 70 minutes for 1286-1576 and about 105 minutes for the full development range 1145-1576.
- **Oz Lotto:** about 10.8 s per target, so about 40 minutes for 1475-1693.
- **Windows will differ.** The figures are for planning only; nothing is committed to them (R3 17.11).

### 9.2 Scorable targets per variant (from the installed declarations)

| Game, window | Variants with every target scorable | Fewer |
|---|---|---|
| Powerball 1286-1576 (history at S: 142 draws) | 37 of 40 | E_10 `CONTRAST_S26_L208_V1`, E_17 `HAZARD_BINS_W208_C100_V1`, E_18 `MIX4_W208_C10_V1`: 225 each |
| Oz Lotto 1474-1693 (history at S: 0) | none: target 1474 has no history | 8 variants 219; E_8 P13 194; 14 variants (52-draw minimum) 168; 14 variants (104) 116; the three 208-draw variants 12 |

### 9.3 Numerics (`reference_wf1.py`)

- **Sigma conversion:** the decimal route reproduces R3 17.5.3's table (1-6 sigma) and MRT-03's deficit example: zero Division 9 wins in 291 draws gives P_lo 0.0111058, which is 2.28673 deficit sigma.
- **MR16:** the exact reference rows of R3 17.6 are reproduced: the expected counts, k_3, the threshold ratios and the power at 1.5x and 2x, for all five rows.
- **MR7's exact null** (integer coefficients): Powerball n = 291 in 0.8 s, n = 432 in 2.3 s; Oz Lotto n = 219 in 0.3 s. Each is built once per (game, n) and serves every track with that n.
- **The N1 generator:**
  - 58,200 Powerball draws in 0.5 s;
  - the main-match counts against a fixed ticket fit the hypergeometric law (chi-square 8.69 on 5 degrees of freedom), and the Powerball hits fit 1/20;
  - it is deterministic, and the key bytes and first word are published for an independent implementation;
  - the Oz Lotto draws have the right shape.
  The root is invented (`AB` x 64), never a beacon value.
- **MR1's exact comparison** agrees with the floating-point route on a test pair.

### 9.4 The beacon's format

Read from NIST's public pages (no lottery site involved):
- **Format:** pulses of chain 2 carry `version` 2.0, `period` 60000 ms, `chainIndex` 2, `pulseIndex`, `timeStamp` in ISO form with milliseconds, `statusCode`, and a 128-hex-character `outputValue`. An example is pulse 1594646, at 2025-12-31T18:01:00.000Z.
- **The time lookup can return a different pulse.** The address for 2018-01-31T20:00:00Z, before chain 1 began, returned chain 1's first pulse, at a different time and with `statusCode` 1.

## 10. Tests (per package; synthetic only)

**REL-1:**
- the status expectations (section 4);
- every released variant runs to SUCCESS and is consumable through the installed registry, both games;
- E_1 and every declaration are byte-unchanged;
- the placeholder chains are unchanged;
- the entry chain and digest checks.

**WF-1A:**
- **Plan refusals:** orphan marker; L at or past the holdout; S at E(G); empty cohort; wrong ledger.
- **A synthetic batch through the driver** in a temporary project tree (the harness patches the project root, as the existing tests do), checking:
  - the order;
  - every run's folder and pins;
  - `read_run` consumability;
  - the counts.
- **Resume after a simulated interruption:**
  - no folder is touched;
  - `INTERRUPTED` and `PUBLICATION_FAILED` pairs run again; others do not.
- **A runner refusal stops the batch at once.** A method failure is counted and the batch goes on.
- **The switch:** True in the installed file; still no override path; every other refusal still precedes any read with the switch True (orphan, flag, unreleased, holdout target, wrong master).
- **The real run root** is under `results/real/development/contract_runs/`, and `.gitignore` covers it.
- **Static checks:** the driver imports no evaluation code and no outcome reader, and opens no data file itself.
- **Mutation checks** (planted defects, each caught):
  - the switch read from an argument;
  - a holdout target admitted;
  - resume re-running a finished pair;
  - a refusal not stopping the batch;
  - the plan written after the first run.

**WF-1B:** R3's MRT-01..10, 12..14, 16..19, 22, 23 as listed in 17.14, plus:
- **the grid:** own-set grids; `SELECTION_UNVERIFIED` on an unpredicted `INSUFFICIENT_HISTORY` or a failure; the Oz Lotto 12-draw intersection reproduced;
- **the outcome reader:**
  - only grid targets are returned;
  - a holdout target is refused;
  - no row at or after the holdout is decoded (a planted row beyond 1576 in an invented master is never parsed);
  - supplementaries are returned only to the division step and never stored;
- **the order:** the scoring plan precedes the first outcome read (an instrumented reader);
- **duplicates:** equal duplicate runs pass; unequal ones give `REPRODUCIBILITY_FAIL`;
- **reports:** no drawn number appears in any report file (a scan against the invented outcomes);
- **cross-platform:** byte-identical CSV on Linux and Windows (the owner's run) apart from the header lines;
- **N1:**
  - the published key and first word (section 9.3);
  - no production fallback root;
  - `N1_NOT_RUN` without an approved policy;
  - a refused or provisional policy is never used;
- **the search log:** one row per run of each type;
- **mutation checks.**

## 11. Findings

**For R3** (recorded in the next register; R3's text is not edited):
- **R3-1:** the default intersection comparison set gives Oz Lotto 12 draws with this cohort (section 6.2). Proposed: own-set grids for tables and families, plus a labelled common-set descriptive table (WF1-6).
- **R3-2:** Oz Lotto's default window starts at the era's first draw, 1474, which has no history, so it can be no method's walk-forward target. It is outside every track's grid, by the declaration rule.
- **R3-3:** 17.13's stage-2 test list says "21..23". MRT-21 tests MR15, a stage-3 measure. Proposed reading: MRT-22 and MRT-23 in stage 2, and MRT-21 in stage 3.
- **R3-4:** 17.11's production route (`lgamma`) and test oracle (`Fraction`) swap roles, for byte identity across platforms (WF1-7).

**For the template** (the owner's keep-current rule; proposed for draft 4 at the next method package):
- **T-1:** a method's design states, for each variant, how many targets it can score in each game's default window (R3 17.3.6). Long minimum histories cost targets, most in Oz Lotto, whose era is short.

## 12. Owner decisions

- **WF1-1 (RECOMMENDED): the four packages and their order** (section 3): REL-1, WF-1A, SEED-1 and WF-1B, with REL-1 and WF-1A reviewed together. The option: one combined package (larger review, one install).
- **WF1-2 (RECOMMENDED): release all 39 variants in both games at once** (REL-1). The option: D6-3's original order, E_6's full-memory variant first and the rest later. All 39 passed review and installation in the same way, so staging adds rounds without adding evidence.
- **WF1-3 (RECOMMENDED): turn `ENABLE_CONTRACT_REAL_DEVELOPMENT` on inside WF-1A.** Ratifying WF-1A is then your decision to turn it on, after its reviewed tests. The option: a separate one-line switch package after WF-1A's install.
- **WF1-4 (RECOMMENDED): real-development records under `results/real/development/`** (section 5.4). Bulk run folders and score ledgers are git-ignored; batch plans, segment records, reports and the search log are committed. The options: commit everything (about 52,000 files for one Powerball batch), or nothing.
- **WF1-5 (RECOMMENDED): the first batches cover every eligible development target** (Powerball 1145-1576, Oz Lotto 1475-1693), so later exploratory windows need no new runs. The reports use R3's default windows for the families. Powerball first; Oz Lotto as a second batch with the same tools, when you say. Each batch is your separate run authorisation, recorded in the register. The options: R3's default windows only; Powerball only for now (Oz Lotto method execution has not yet been authorised, H-1 section 5.3).
- **WF1-6 (RECOMMENDED): own-set grids, and the two MR7 families** (sections 6.2 and 6.7). The options: R3's default intersection (Oz Lotto: 12 draws); other or extra families, for example your own MR4 sets C.3, B.2-3 and X.3 as a calibrated family (they are always computed and shown in any case).
- **WF1-7 (RECOMMENDED): exact arithmetic for every statistic** (section 6.6), reversing R3 17.11's production and test routes. The option: R3 17.11 as written, with byte identity on one machine only.
- **WF1-8 (RECOMMENDED): N1's standard-library generator** (section 7.2). The options: NumPy's PCG64 raw bit stream with the same rejection sampling (stable across NumPy versions, but a dependency); NumPy's `Generator.choice` (not recommended: NumPy does not promise that its sampling methods give the same draws across versions).
- **WF1-9 (YOUR CHOICE): N1's beacon pulse.** Recommended: the pulse at `2026-11-06T00:00:00.000Z` (section 8.1). The option: any later whole minute you prefer, recorded in `exchange/` before it arrives.
- **WF1-10 (RECOMMENDED): report files carry no drawn numbers,** so you may attach a report to either chat. The ledgers stay local.
- **WF1-11 (RECOMMENDED): template finding T-1** goes into draft 4 at the next method package (wave 3).

## 13. What the reviewer is asked to check (R-3)

1. **The switch's reach:** that turning on `ENABLE_CONTRACT_REAL_DEVELOPMENT` admits nothing beyond released variants on the development prefix. Check the holdout's two guards, and that every refusal precedes any read.
2. **The driver:** its STOP rule, resume rule and plan-before-run order, and that it needs no termination or coordinator path.
3. **The fixed grid:** that own-set grids keep `EXACT_LOCAL`, `N1_CALIBRATED` and guaranteed Bonferroni status (section 6.2), and that the availability check labels every outcome-dependent case.
4. **The outcome reader's guards,** and the scoring-plan-before-outcome order.
5. **N1:** the generator's uniformity and determinism (section 7.2); the exactness claims of section 7.4; the labels of 7.1.
6. **The seed procedure** against D-9..D-11 and E2R-R63 (section 8), including the acceptance checks and the no-fallback rule.
7. **The families:** whether MR7.MAIN and MR7.PB over TOP and WORST are a sound headline, and whether any figure is mislabelled.
8. **Mark, never suppress:** that nothing in WF-1 hides or demotes a method or a number.

## 14. Not in scope

Not in scope:
- R3 stage 3 (MR2, MR3, MR6, MR8-MR15; in-sample mode; side-by-side tables);
- meta-methods;
- coordinated runs;
- Mode H, the holdout and FINAL;
- prospective forecasts;
- Method A's diagnostics;
- wave 3;
- any change to an installed method;
- any dependency change.

The gates and the orphan-marker rule apply unchanged.
