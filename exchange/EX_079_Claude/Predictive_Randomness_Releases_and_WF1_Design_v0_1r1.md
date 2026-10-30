# Predictive Randomness - releases and WF-1 (the first walk-forward results, the R3 scorer and N1), design note v0.1

**Document:** the design of the work that switches the installed methods on and produces the project's first measured results over past draws: the release package, the walk-forward driver, the R3 stage-2 scorer and report, the N1 fair-draw simulator, and N1's seed policy with its NIST Randomness Beacon root.
**Version:** v0.1r1 DRAFT for the reviewer's focused RECHECK, 30 October 2026. It resolves EX_078 (`exchange/EX_078_ChatGPT.md`, `465a8ce2...84f3`; RECHECK: 1 BLOCKER, 4 CORRECTION, 2 OPTIONAL): WF1-R3-B01 (the driver's STOP rule now classifies the runner's terminal reasons and fails closed; section 5.3), C01 (the seed's trust basis is stated, owner decision WF1-12; section 8), C02 (the search-log row is written before any outcome is read; section 6.1), C03 (the downgrade rules for missing opportunities; section 6.2A), C04 (the numerics wording, accuracy budget and bounds; section 6.6), O01 (the plan checks the flags too; 5.2) and O02 (batch and report windows shown apart; 5.6, 9.1). It also records the owner's decisions WF1-6 and WF1-12 and his reading of D-10 (section 12). Appendix A maps every finding. v0.1 (`12282930...6bdf`) is superseded. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule. Where it proposes to change or clarify one, the owner decision is listed in section 12.
- **No code yet:** each package follows only after this design passes.
- **Probes:** timing and numerical probes on invented data are reported in section 9. The probe and reference scripts travel with this note. They read no repository data file and no real draw.
- **Base:** `main` at `b4b83c1` (EX_077 at `4bdb060`, EX_078 at `b4b83c1`; wave 2 installed at `b61b1a2`; the handovers and register v0.20 at `03f7da4`).
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
- the **cohort**: every (method, variant) with an active `SUPPORTED` entry in the installed registry for the game, no `IN_DEVELOPMENT.txt` flag in its method folder (O01), and a runner adapter, in method-number then variant order. The dispatch gate still rechecks both at every run. For each: the revision, the declaration digest, the registry entry digest, and `minimum_history_draws`. The cohort digest covers that list;
- the **master pin**: the SHA-256 recorded in the game's version-1 INIT ledger line;
- the observation view (`UNORDERED_SET`, dates off) and the run mode `REAL_DEVELOPMENT`.

**Refused at `plan`, before anything is written:** the orphan marker is present; L >= the holdout's first draw (1577 / 1694); S < E(G) + 1 (the era's first draw has no history: 5.3); an empty cohort; a method with a `SUPPORTED` entry whose flag is still present (an inconsistent installed state, reported by name: O01); a ledger that is not the version-1 INIT line.

### 5.3 Running, resuming and stopping

- **Order:** cohort order, then ascending target. Each variant's whole window is finished before the next variant starts, so a partial batch still gives complete tracks.
- **Each run** is one ordinary standalone contract run (`run_contract_method`, `REAL_DEVELOPMENT`, `WF_FORECAST`), pinned to the plan's digests and master. All of the runner's own refusals apply unchanged: the orphan marker; the switch; the dispatch gate (released variant, no flag); the reader's development-prefix rule (target below 1577 / 1694; ledger, master and INIT checks).
- **The STOP rule (A STOP is a STOP; EX_078 WF1-R3-B01).** The driver classifies each run by the terminal record's **reason**, not by its outcome alone, and it fails closed: a reason it does not recognise is a STOP. The installed runner is not changed; the classification lives in the driver.

  | The run ends with | Class | The driver |
  |---|---|---|
  | `RunRefused` or `DispatchRefused` raised (orphan marker, switch, data source, dispatch gate) | STOP | stops at once; nothing was created for that run |
  | reason `DATA_ADMISSION_REFUSED: ...` (outcome `VALIDATION_FAILURE`): the reader refused the pinned ledger, master, INIT record or prefix | STOP | stops at once: the data source is no longer admitted |
  | reason `PUBLICATION_FAILED: ...` or `INTERRUPTED` | STOP | stops at once |
  | any exception escaping `run_contract_method` (including a run folder that cannot be created, a terminal record that cannot be written, and Ctrl-C before the run folder exists) | STOP | stops at once |
  | any other reason prefix | STOP | fails closed and names the reason |
  | reason `METHOD_FAILED: ...` (`RUNTIME_FAILURE` or `NUMERIC_INVALID`) | CONTINUE | the method's own result for that target: counted, never retried |
  | reason `CONTRACT_REFUSED_OUTPUT: ...` (`VALIDATION_FAILURE` or `NUMERIC_INVALID`) | CONTINUE | the method's output failed validation: counted, never retried |
  | reason `NO_TICKET_NO_DIAGNOSTIC: ...` | CONTINUE | a valid empty target (`DIAGNOSTIC_ONLY`), counted |
  | reason `PUBLISHED: ...` (`SUCCESS`) | CONTINUE | the forecast is frozen |

- **Checks at the start of every `run` (also on resume), before any run:** the orphan marker is absent; for every cohort member, the installed registry's active entry digest and declaration digest still equal the plan's, and no flag is present. Any change refuses the whole invocation before anything is created (exit code 2). These are registry reads only; the driver opens no data file.
- **Between targets:** an orphan marker that appears mid-batch makes the next run raise `RunRefused`, which is a STOP; nothing runs after it.
- **Resume:** a (variant, target) pair is **done** when it has a terminal record, under the plan's pins, whose class is CONTINUE. Every other pair is run again on resume: no terminal record at all (including a run folder left without one); `INTERRUPTED`; `PUBLICATION_FAILED`; `DATA_ADMISSION_REFUSED`. Each new attempt gets a new run ID and folder; earlier attempts stay exactly as they are, and nothing is deleted, moved or rewritten.
- **If the cause persists on resume:** a runner refusal stops it again before anything is created. A data-admission failure stops it after one recorded attempt, the first pair it tries. A resume therefore never makes more than one failed attempt.
- **Ctrl-C** during a run ends that run with its `INTERRUPTED` terminal record (existing behaviour). If it lands before the run folder exists, nothing is created. Either way the driver stops, as in the table.
- **Segment records:** each `run` invocation tries to write `segment_<UTC>.json` (create-only) when it stops, listing the run IDs it created, the pairs it classified and why it stopped. If that write fails, the same lines go to the console, and the driver exits with code 1. No evidence depends on it: run folders describe themselves, and the scorer does not read segment records (section 6.1).
- **Exit codes:** 0 every pair done; 1 stopped (by the STOP rule or Ctrl-C); 2 refused before any run.
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

For each game, in your order (decision WF1-5). **The batch range and the report window are different things (O02):**

| Game | Batch: targets predicted | Report window (R3 17.3.6) | Notes |
|---|---|---|---|
| Powerball | 1145-1576 (432 targets) | 1286-1576 (291 draws) | the batch also covers 1145-1285, for later exploratory windows |
| Oz Lotto | 1475-1693 (219 targets) | 1474-1693 (220 draws) | 1474 is in the window but in no track's grid: it has no history, so it is never predicted or scored |

1. `Run_Experiment.bat Method_Walk_Forward.py plan --game POWERBALL --first 1145 --last 1576`, which prints the batch ID.
2. `Run_Experiment.bat Method_Walk_Forward.py run --batch <ID>`. On the Linux probe's speed this is about 105 minutes for Powerball's 432 targets (section 9.1); that is planning evidence, not a Windows result.
3. `Run_Experiment.bat Method_Walk_Forward.py status --batch <ID>` to see the counts.
4. Commit `results/audit/SEARCH_LOG.csv` and `results/real/development/wf_batches/` (the exact commands come with the package).

Claude Code never runs a real batch: its rehearsals use invented data only (its rulebook, rule 9).

## 6. WF-1B: the scorer and report (R3 stage 2)

### 6.1 One report run, in this fixed order

`Run_Method_Rankings.bat --game G --batch <ID> --first S --last L` (a new wrapper, already ratified in Architecture 5A.4) launches `src/evaluation/Method_Rankings_Report.py`. The new folder `src/evaluation/` holds the scorer, the outcome reader, N1 and the report writer. A static check forbids any method file from importing it, and forbids it from importing any method's code: the report tool runs no method (Architecture 12.5).
1. **Refusals that read nothing:** the orphan marker; the window (S >= E(G), L <= 1576 / 1693; MRT-14); an unknown batch; families that are not registered.
2. **The fixed grid** (6.2) from the plan alone, with its digest.
3. **Collect the frozen forecasts.** For every grid cell, the driver's run folders for that (variant, target) under the plan's pins are found and passed through `read_run`, which establishes every gate itself. If several consumable runs exist (a resumed batch), their `canonical_content_digest` must be equal. The earliest by freeze-receipt time is used (the receipt selection policy, E2R-R40A). Unequal digests are reported as `REPRODUCIBILITY_FAIL`, never hidden.
4. **The search-log row (EX_078 WF1-R3-C02).** One `RANKING_REPORT` row is appended to the search log (6.7) **before any outcome is read**. It holds the report attempt ID (`rr-<32 hex>`), the UTC time, the game, mode and window, the cohort and grid digests, the family IDs, the measures, the declared number of tests, the batch ID and the digest of the scoring plan about to be written.
5. **The scoring plan** (`SCORING_PLAN_V1`, create-only) records the attempt ID and the search-log row number, the grid, the selected forecasts' content and receipt digests, and the availability counts. It is written **before** any outcome is read.
6. **The outcomes** of the grid's targets only (6.3).
7. **Records:** the score ledger and the rank-position ledger (6.4).
8. **Measures, N1, and the report files.** The report's JSON names the attempt ID and the row number.

**Attempts that do not finish stay counted.** Every invocation that gets past step 3 has its row, whether or not it reaches a report; a later failure (even after outcomes were read) never removes it, and no row is ever edited. Every report header states the number of `RANKING_REPORT` rows for its game, and how many of them have no completed report (an attempt ID with no report file). A crash between steps 4 and 5 leaves a row without a scoring plan: it is counted as an unfinished attempt, which errs on the side of counting more searching, never less. An invocation refused at step 1, which reads nothing, appends nothing.

### 6.2 The fixed grid and the comparison sets

- **A track's grid** (R3 17.3.7A) is every target N in [S, L] with N - E(G) >= max(1, `minimum_history_draws`). It depends only on draw numbers and the declaration, never on outcomes, so exact and N1-calibrated figures keep their status.
- **Availability check:** within the grid, every target must have an available ticket. Any other status (a failure, or an `INSUFFICIENT_HISTORY` record that the declaration does not predict) sets that table's significance figures to `SELECTION_UNVERIFIED`. They are still computed and shown, with the count of affected targets.
- **Finding, with numbers (section 9.2): the default intersection set fails Oz Lotto.** R3's default comparison set is the intersection of the cohort's scored sets. With this cohort:
  - for Powerball (1286-1576), the three 208-draw variants score from 1352, so the intersection is 225 draws instead of 291;
  - for Oz Lotto (1474-1693), the era began only 220 draws before the holdout, so the three 208-draw variants score only 12 draws (1682-1693), and the intersection would be those 12 draws for every track.
- **Proposed (decision WF1-6):**
  - every league table and family uses each track's own grid (R3's labelled `OWN_SET` option, n per row);
  - each game also gets one descriptive common-set table, on the intersection, labelled (Oz Lotto's carries `LOW_N`).

  Bonferroni over exact per-track p-values stays guaranteed with own-set grids, because each test is valid on its own fixed grid (R3 17.5.3 needs valid inputs and a predeclared family, not equal n). The N1 maximum statistic replays each track on its own grid. The owner agreed to this on 30 October 2026 (WF1-6), subject to the rules of 6.2A.

### 6.2A Missing opportunities: how labels are downgraded (EX_078 WF1-R3-C03)

**Per track.** A grid cell is **valid** when it has exactly one selected consumable forecast with an available ticket for that readout and no reproducibility failure. A track's status is:

| Track status | When | Its local significance labels |
|---|---|---|
| `GRID_COMPLETE` | every cell of its grid is valid | as R3 assigns (`EXACT_LOCAL` for MR4, MR7 and MR16; `N1_CALIBRATED` for MR1 once N1 runs) |
| `GRID_INCOMPLETE` | at least one cell is not valid: a failed or non-consumable run, no run at all, an `INSUFFICIENT_HISTORY` record the declaration does not predict, or a `REPRODUCIBILITY_FAIL` | `SELECTION_UNVERIFIED`; the figures are still computed on the valid cells and shown, with the count of invalid cells by reason |
| `GRID_EMPTY` | no valid cell at all | `MR_INSUFFICIENT_DATA` (n = 0): no p-value, never zero sigma |

With own-set grids, one track's invalid cells change no other track's local figures, because no other track's grid depends on them.

**Per family** (6.7):
- **The roster and M are fixed at registration** (M = 80). A track that is incomplete or empty stays in the roster and in M, and is listed by name with its status. It is never removed or replaced.
- **The guaranteed label** (Bonferroni, guaranteed) is given only if all M tracks are `GRID_COMPLETE`, every input p-value is `EXACT_LOCAL`, and the family was registered before its first use (checked against the search log, MRT-17).
- **Otherwise**, the same arithmetic, min(1, M x p), is shown labelled `BONFERRONI_REFERENCE_UNCALIBRATED`, with the number of tracks that broke the condition. An empty track contributes no p-value, but M is not reduced.
- **The N1 maximum statistic** is `N1_FIXED_FORECAST_REFERENCE` in any case. A family with any incomplete track also carries `SELECTION_UNVERIFIED` on it.

**Per table.**
- An own-set table's local figures follow each row's track status.
- The common-set descriptive table (6.2) is the intersection of the valid cells, so any invalid cell can change it for every row. If any cohort track is `GRID_INCOMPLETE`, every significance figure in that table is `SELECTION_UNVERIFIED` (R3 17.3.7A, applied table-wide as R3 writes it).

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

### 6.6 Exact counts and tails; deterministic high-precision transforms (decision WF1-7; EX_078 WF1-R3-C04)

R3 17.11 makes production tails log-space sums via `lgamma`, with an exact `Fraction` oracle in the tests. At this project's sizes the exact route is fast (sections 9.3 and 9.5), so the proposal reverses the roles. Precisely:
- **Exact integer and rational values:** counts, sums and divisions (integers); binomial tails (`Fraction`s, summed on the shorter side over the common denominator b^n, so exactly and without cancellation); MR7's null distribution (integer polynomial coefficients); N1's comparisons (section 7.4).
- **Deterministic, bounded-accuracy decimal transforms** (not exact values): sigma, MR1's logarithms, and the Clopper-Pearson bounds.
  - **Sigma:** 80-digit `decimal` arithmetic. The normal tail Q(z) uses the erf series for z/sqrt(2) < 5 and the continued fraction (400 terms) from 5 up. Sigma is solved by bisection to an interval far below float64 resolution, and never forms 1 - p in floating point. p >= 1/2 gives 0 sigma exactly.
  - **MR1:** `decimal` logarithms at 80 digits.
  - **Clopper-Pearson:** bisection on the exact binomial tail, to an interval below float64 resolution.
- **Error budget:** each decimal transform is accurate to a relative 1e-30 or better before it is rounded to float64. That is far inside R3 17.11's 1e-6 for sigma. The evidence (section 9.5): the two tail routes agree to 1.7e-47 where both apply; the continued fraction does not change between 400 and 4000 terms; ln Q agrees with an independent asymptotic series to 2e-17 absolute from 12 to 60 sigma.
- **Output:** each value is converted to float64 once, by correctly rounded conversion. Each p-value is also written as `log10` text with 15 significant digits.
  - A p-value below float64's normal range carries the label `P_BELOW_FLOAT64_RANGE`; its float field is the correctly rounded subnormal or 0.0, and its `log10` text is kept.
  - A sigma above 1000 (a p-value below about 10^-217000) is reported as `SIGMA_ABOVE_BOUND`, shown as ">= 1000".
  - No tail is ever silently replaced by an approximation.
- **Bounds on exact work:**
  - binomial tails are exact for every n the project meets (n = 5000 with p = 1e-9 in 0.1 s; section 9.5);
  - MR7's exact null is computed for n <= 1000 (24 s at n = 1000; WF-1's largest n is 432). Above that bound MR7's tail is `MR_EXACT_BOUND_EXCEEDED`, and the normal approximation is shown beside it, labelled `APPROX_UNCALIBRATED`, never unlabelled.
- **The `lgamma` route** becomes the tests' independent cross-check (MRT-04 in substance).
- **Byte identity:** integer, `Fraction` and `decimal` arithmetic and correctly rounded conversion are deterministic and the same on every platform. So a report's CSV and its data fields should be byte-identical on Windows and Linux, excluding the header's time, environment and tool-provenance lines. This is a design property, not yet evidence: WF-1B's tests compare the bytes (on the same synthetic inputs, on Linux in the package's runs and on the owner's Windows run). That is W2-7's rule applied to the scorer, so MRT-08 then holds across platforms, not only on one machine.

### 6.7 Families, multiplicity and the search log

- **Two predeclared families per game** (decision WF1-6), registered in `src/evaluation/registry/FAMILY_REGISTRY_V1.json`, installed with WF-1B and so before any report:
  - `WF1_<GAME>_MR7_MAIN_V1`: MR7.MAIN's excess p-value (P_up) for every TOP and WORST track of the REL-1 cohort, on own-set grids, in the game's default window (R3 17.3.6). M = 80 per game. For a WORST track, an excess is the "inverse signal" R3 asks about. Deficits are shown locally and are not in the family.
  - `WF1_POWERBALL_MR7_PB_V1`: MR7.PB the same way (Powerball only, M = 80).
  - **Why MR7:** it is R3's most direct every-draw test, it is exact, and it stays exact under adaptive walk-forward, so Bonferroni over it is a guaranteed global figure (R3 17.5.3, 17.18.4).
- **Everything else is exploratory:** `EXPLORATORY_COHORT`, Bonferroni over the table's actual number of tests, labelled, and counted in the search log. Any table may be produced (R3 17.5B).
- **N1 maximum statistic** per family, labelled `N1_FIXED_FORECAST_REFERENCE` (R3 17.5.3).
- **The search log** `results/audit/SEARCH_LOG.csv` (R3 7.4, 17.5B):
  - created with its header on first use, if absent;
  - each report invocation that gets past its refusals appends exactly one `RANKING_REPORT` row, before any outcome is read (6.1, step 4);
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
| Accepted only if | `version` "2.0", `chainIndex` 2, that exact `timeStamp`, `statusCode` 0, and a 128-hex-character `outputValue` (upper-case hexadecimal, as NIST publishes it) |
| Trust basis | NIST's official HTTPS service (`beacon.nist.gov`). The pulse's signature and certificate are **not** validated (owner decision WF1-12) |
| Status | `PROVISIONAL` (not runnable) |

- **No "latest", "next" or fallback pulse.** NIST's time lookup returns a different pulse when none exists at the requested time: a probe for an instant before chain 1 began returned that chain's first pulse, with a different time stamp (section 9.4). So the time stamp is checked, never assumed.
- **A missing or failed pulse:** if it does not exist, or fails a check, the policy is `REFUSED`. A new policy with a new announced pulse is needed, and it is counted (8.4).
- **The owner may choose another time:** any later whole minute (the beacon publishes one pulse a minute), as long as the choice is recorded in `exchange/` before that minute. It is the owner's choice (decision WF1-9).

### 8.2 Retrieval and independent verification

1. **After the pulse time,** you open NIST's page for that pulse in your browser: `https://beacon.nist.gov/beacon/2.0/pulse/time/1793923200000`. Save the JSON to `E:\TEMP`, and attach it to the Claude chat. Nothing in the project fetches it.
2. **Claude checks it field by field** against the acceptance row above, and records the SHA-256 of the saved file's bytes.
3. **Claude independently reads the same pulse** from NIST's public archive over HTTPS, at its permanent address (`https://beacon.nist.gov/beacon/2.0/chain/2/pulse/<pulseIndex>`), and compares `chainIndex`, `pulseIndex`, `timeStamp`, `statusCode` and `outputValue` (and `uri`). This is D-9's second-person check (E2R-R63: "someone other than the person who fetched it"). The reviewer may also check.

**What is and is not verified (EX_078 WF1-R3-C01; owner decision WF1-12, 30 October 2026).**
- **Verified:** that two separate HTTPS reads of NIST's official service, by two different people, return the same pulse with the announced chain, time stamp and field, a normal status code and a well-formed value.
- **Not verified:** the pulse's cryptographic signature and certificate. That check is recorded as `NOT_PERFORMED`. D-9 to D-11 never required it, and none of them changes.
- **NIST's notice of 23 October 2026** (on its Beacon 2.0 page, `https://csrc.nist.gov/projects/interoperable-randomness-beacons/beacon-20`) says that pulses issued since 3 September 2026 refer to an incorrect certificate, and that verification for that period will need a different certificate. The 6 November pulse may be affected. Because no signature check is made, the notice does not block approval. It is recorded in the policy, with the pulse's `certificateId` as published.
- **The residual risk, accepted by the owner (WF1-12):** that the value both reads returned was not NIST's genuine output. The seed's purpose is to be externally generated and fixed in advance, so that no one can choose a favourable seed after seeing results. The project does not run a security-critical system. For that purpose, two independent HTTPS reads of NIST's own service are proportionate.
- **Not proposed, but available:** NIST's chain links can be checked without a certificate (the next pulse's `previous` value equals this `outputValue`; SHA-512 of the next pulse's `localRandomValue` equals this `precommitmentValue`). Both links hold on two public chain 1 pulses (section 9.5). The owner may ask for this check later; it is not a condition of approval.

### 8.3 Approval

- **The approved policy record** (`SEED_POLICY_V1`, `APPROVED`) binds:
  - the exact accepted `outputValue`, the pulse's `uri`, `pulseIndex`, `timeStamp`, `statusCode` and `certificateId` as published;
  - the source (the two HTTPS addresses read) and the SHA-256 of the owner's saved file;
  - who fetched it and when, and who verified it and when;
  - `signature_verification: NOT_PERFORMED`, the trust basis (NIST's official HTTPS service; WF1-12), and the reference to NIST's notice of 23 October 2026.

  It goes into `src/evaluation/seed_policies/`, reviewed and immutable, through WF-1B or a tiny SEED-1 package.
- **The provisional and approved records** both stay as history.
- **The root is seed entropy, not data** (E2R-R63). It carries no information about any draw.
- **Timing (D-11):** using a root published after the historical targets is allowed for retrospective development work, and the report says "randomness chosen for the experiment".

### 8.4 Switching and counting (D-10)

- **Switching (D-10 as ratified; confirmed by the owner, 30 October 2026):** the 6 November value is N1's single root unless you later replace it. A replacement is never a quiet substitution: it is a new policy ID with its own pulse, announced in `exchange/` before that pulse exists, approved by the same procedure. Earlier policies and their reports are kept. There is no automatic replacement for a refused pulse either.
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

### 9.5 Added for v0.1r1 (EX_078 WF1-R3-C04 and C01)

`probe_tails.py` (output `ev_wf1_tails.txt`) and `probe_numerics2.py` (output `ev_wf1_numerics2.txt`), fair-draw arithmetic only:
- **The two tail routes,** with the switch at z/sqrt(2) = 5: they agree to a relative 1.7e-47 on [5, 6]. The continued fraction does not change between 400 and 4000 terms at x = 5, 8, 20 and 45. (With v0.1's switch at 3, the overlap on [2.5, 3.5] agreed only to 2.6e-11, which is why the switch moves.)
- **Large sigma:** ln Q(z) agrees with an independent asymptotic series to 1.95e-17 absolute for z = 12 to 60.
- **Extreme and boundary tails:**

  | p | sigma | Q(sigma)/p - 1 | time |
  |---|---|---|---|
  | 1e-300 | 37.0470962993612 | 2.8e-14 | 0.1 s |
  | 1e-700 | 56.68955328257109 | 1.8e-13 | 0.1 s |
  | 1/2 - 1e-20 | 2.5066282746310004e-20 | 4.3e-37 | 6 ms |
  | 1/2 | 0 (exact rule) | 0 | 0 |

  The float64 rounding of sigma accounts for the residuals.
- **MRT-04 sizes,** exact, on the shorter side:
  - n = 5000, p = 1e-9: P(X >= 40) is 10^-260.021 (0.09 s) and P(X >= 3) is 10^-16.682 (0.03 s);
  - n = 5000, p = 51597/3362260: P(X >= 120) is 10^-5.610 (0.13 s).

  Summing the long side, as the first probe did, took about 180 s for the same values.
- **MR7's exact null:** 2.1 s at n = 432 and 23.7 s at n = 1000, hence the bound of 6.6.
- **NIST chain links,** on public chain 1 pulses 1705577 and 1705578: SHA-512 of the next pulse's `localRandomValue` equals the earlier pulse's `precommitmentValue`, and the next pulse's `previous` equals its `outputValue`. Both hold. No certificate is needed (section 8.2: available, not proposed).

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
  - pairs with no terminal record, `INTERRUPTED`, `PUBLICATION_FAILED` or `DATA_ADMISSION_REFUSED` run again; CONTINUE-class pairs do not.
- **The STOP rule (B01), each with zero runs after the stop:**
  - a runner refusal;
  - **an invented master changed after the plan,** so that dispatch admits the request but the reader refuses the pin (`DATA_ADMISSION_REFUSED`). The test counts zero target executions after it, and on resume with the cause still present, exactly one attempt and a stop;
  - an orphan marker created between two targets;
  - an exception escaping the runner (a run folder that cannot be created; a terminal record that cannot be written);
  - Ctrl-C before the run folder exists;
  - an unknown reason prefix (fails closed).
- **CONTINUE:** a method failure, an invalid output and a valid empty target are each counted, and the batch goes on.
- **Start-of-run checks:** a changed active entry, a changed declaration, or a flag added after the plan refuses the invocation before any run.
- **Plan (O01):** a `SUPPORTED` entry with its flag present is refused at `plan`, by name.
- **The switch:** True in the installed file; still no override path; every other refusal still precedes any read with the switch True (orphan, flag, unreleased, holdout target, wrong master).
- **The real run root** is under `results/real/development/contract_runs/`, and `.gitignore` covers it.
- **Static checks:** the driver imports no evaluation code and no outcome reader, and opens no data file itself.
- **Mutation checks** (planted defects, each caught):
  - the switch read from an argument;
  - a holdout target admitted;
  - resume re-running a finished pair;
  - a refusal not stopping the batch;
  - `DATA_ADMISSION_REFUSED` classified as CONTINUE;
  - an unknown reason classified as CONTINUE;
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
- **the search log (C02):** the `RANKING_REPORT` row precedes the first outcome read (an instrumented reader); a failure injected after outcomes are read leaves the row in place, and the next report counts it as an attempt without a report; a crash injected between the row and the scoring plan is counted the same way; a refused invocation appends nothing; one row per driver `plan`;
- **the downgrade rules (C03):** a synthetic family of 79 complete tracks and 1 track with a failed cell gives `BONFERRONI_REFERENCE_UNCALIBRATED` with M = 80 and the failed track listed; a complete 80-track grid gives the guaranteed label; an empty track gives `MR_INSUFFICIENT_DATA` and keeps M = 80; a `REPRODUCIBILITY_FAIL` cell makes its track `GRID_INCOMPLETE`; an incomplete track leaves other tracks' local labels unchanged; the common-set table turns `SELECTION_UNVERIFIED`;
- **the numerics (C04):**
  - MRT-04 at n = 5000 with p down to 1e-9, including tails below 1e-300;
  - sigma at p = 1e-300 and 1e-700, near and at 1/2, against the asymptotic oracle;
  - `P_BELOW_FLOAT64_RANGE`, `SIGMA_ABOVE_BOUND` and `MR_EXACT_BOUND_EXCEEDED` each produced and labelled;
  - the two tail routes agree on their overlap;
- **the seed policy record (WF1-12):** an `APPROVED` record without `signature_verification`, the file SHA-256, the `certificateId` or the two source addresses is refused; a lower-case or wrong-length `outputValue` is refused;
- **N1's word convention:** SHAKE-256 words are unsigned 64-bit little-endian (a test pins the published first word);
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
- **WF1-6 (OWNER-DECIDED 30 October 2026, subject to the review): own-set grids, and the two MR7 families** (sections 6.2, 6.2A and 6.7). The owner agreed to the departure from R3's default intersection set. The options not chosen: R3's default intersection (Oz Lotto: 12 draws). Other or extra families remain possible, registered before first use; for example your own MR4 sets C.3, B.2-3 and X.3 (they are always computed and shown in any case).
- **WF1-7 (RECOMMENDED): exact arithmetic for every statistic** (section 6.6), reversing R3 17.11's production and test routes. The option: R3 17.11 as written, with byte identity on one machine only.
- **WF1-8 (RECOMMENDED): N1's standard-library generator** (section 7.2). The options: NumPy's PCG64 raw bit stream with the same rejection sampling (stable across NumPy versions, but a dependency); NumPy's `Generator.choice` (not recommended: NumPy does not promise that its sampling methods give the same draws across versions).
- **WF1-9 (YOUR CHOICE): N1's beacon pulse.** Recommended: the pulse at `2026-11-06T00:00:00.000Z` (section 8.1); the owner and the reviewer have both said to keep it. The option: any later whole minute you prefer, recorded in `exchange/` before it arrives. Under D-10, as the owner confirmed on 30 October 2026, any later replacement is a new pre-announced policy, with every root kept and counted.
- **WF1-10 (RECOMMENDED): report files carry no drawn numbers,** so you may attach a report to either chat. The ledgers stay local.
- **WF1-11 (RECOMMENDED): template finding T-1** goes into draft 4 at the next method package (wave 3).
- **WF1-12 (OWNER-DECIDED 30 October 2026, after EX_078 C01): the seed's trust basis is NIST's official HTTPS service.** The pulse's signature and certificate are not validated (`NOT_PERFORMED`), and NIST's certificate notice of 23 October 2026 does not block approval. D-9's two-person check stays: the owner fetches the pulse by hand, and Claude independently reads it from NIST's archive and compares the five fields. The owner accepts the residual authenticity risk (section 8.2). D-9 to D-11 are unchanged. The options not chosen: require a signature check (approval would wait for NIST's corrected certificate), or drop the second read as well (an amendment of E2R-R63 stage 2).

## 13. What the reviewer is asked to check (R-3)

**For the focused RECHECK of v0.1r1:** whether each EX_078 finding is resolved (Appendix A): the STOP classification table and its fail-closed default (5.3); the trust-basis wording and policy fields (8.2, 8.3); the search-log order (6.1); the downgrade rules (6.2A); and the numerics wording and bounds (6.6, 9.5). The eight original items follow.

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

## Appendix A. Resolution of EX_078

| Finding | Class | Resolution in v0.1r1 |
|---|---|---|
| WF1-R3-B01 source-admission failures continued | BLOCKER / RECHECK | 5.3: the STOP rule classifies the terminal **reason** and fails closed. `DATA_ADMISSION_REFUSED`, `PUBLICATION_FAILED`, `INTERRUPTED`, escaping exceptions and unknown reasons STOP; only `METHOD_FAILED`, `CONTRACT_REFUSED_OUTPUT`, `NO_TICKET_NO_DIAGNOSTIC` and `PUBLISHED` continue. It adds start-of-run registry checks, the mid-batch marker case, the no-terminal and no-segment cases, and resume while the cause persists (at most one failed attempt). The installed runner is unchanged. Tests in section 10, including the changed-master test with zero subsequent runs |
| WF1-R3-C01 NIST certificate notice; meaning of verification | CORRECTION / RECHECK | 8.1 trust-basis row; 8.2 states what is and is not verified, records NIST's notice and the residual risk, and keeps D-9's second-person check; 8.3 adds the policy fields (`certificateId`, file SHA-256, sources, `signature_verification: NOT_PERFORMED`). Owner decision WF1-12. The announced pulse is unchanged |
| WF1-R3-C02 search-log write too late | CORRECTION / RECHECK | 6.1 step 4: the `RANKING_REPORT` row (attempt ID, scope, grids, families, declared tests, scoring-plan digest) is appended before the scoring plan and before any outcome is read. Unfinished attempts stay counted and are reported. Tests in section 10 |
| WF1-R3-C03 own-set Bonferroni eligibility | CORRECTION / RECHECK | 6.2A: track statuses `GRID_COMPLETE` / `GRID_INCOMPLETE` / `GRID_EMPTY`; the family's roster and M are fixed; the guaranteed label only with all M tracks complete and `EXACT_LOCAL` and registration before first use; otherwise `BONFERRONI_REFERENCE_UNCALIBRATED`; the common-set table goes `SELECTION_UNVERIFIED` table-wide. Tests: 79 + 1, complete 80, empty, reproducibility failure |
| WF1-R3-C04 "exact everywhere" overstated | CORRECTION / RECHECK | 6.6 reworded: exact integer and rational counts and tails; deterministic bounded-accuracy decimal transforms (1e-30 relative budget); once-only float64 output with `log10` text. It adds `P_BELOW_FLOAT64_RANGE`, `SIGMA_ABOVE_BOUND` and the MR7 bound (n <= 1000, else `MR_EXACT_BOUND_EXCEEDED` with a labelled approximation). Byte identity is a design property, to be tested. The route switch moves to 5 (9.5). Extreme-tail and MRT-04-size evidence is in 9.5 |
| WF1-R3-O01 plan-time flag check | OPTIONAL | Adopted (5.2) |
| WF1-R3-O02 batch and report windows | OPTIONAL | Adopted (5.6 table; 9.1 timing labelled planning evidence) |
| Item 5 note: SHAKE word sign and root case | (in item 5) | Unsigned 64-bit little-endian words; upper-case hexadecimal root, as published; both pinned by tests (section 10) |
