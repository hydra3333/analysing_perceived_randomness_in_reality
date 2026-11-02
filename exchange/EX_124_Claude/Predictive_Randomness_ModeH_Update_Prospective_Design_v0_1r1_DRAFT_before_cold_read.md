# Mode H, the results update and the prospective mode - design v0.1r1

**Version:** v0.1r1, 3 November 2026 (Adelaide, UTC+10:30). CANDIDATE for design-stage review (R-3). Replaces v0.1 (recorded in `exchange/EX_123_Claude/` at `c01717d`, never sent to the reviewer, overtaken by the stock-take round of 2 November 2026 and the owner's ratification of its positions). Appendix B lists what changed.
**Author:** Claude (the primary designer and coder). **Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner.
**Base:** `main` at `3a9f6ac` (documents); `src/` and `tests/` unchanged since PERF-1 at `3fce327` (register v0.23). Code facts are cited by file and line at that base.
**Authorises nothing.** No run, update, holdout opening, Mode H, FINAL or prospective forecast follows from this text. Each of those stays a separate owner approval after review.
**Holdout statement:** this note contains no outcome of any draw. Draw numbers appear only as identifiers. Dates of future draws were derived from the era profiles' weekly rule (`game_profiles.derived_date`), not from any result.

## Work-item card

| Field | Value |
|---|---|
| Item | MHUP-1: Mode H, the results update and the prospective (weekly) mode (roadmap item 10c; GOAL-1, ORD-1) |
| Author / reviewer | Claude / ChatGPT reviewer chat (R-3 design review now; R-2 later for the code) |
| Risk tier | HIGH (reader and digest code; evaluator and scorer; holdout access and unsealing; freezing and publication; a new contract vocabulary row; `source_data/`) |
| Owner inputs (binding) | MH-1, OFF-1, EFF-1, HX-1, HX-2, FB-1, GOAL-1, ORD-1, TSC-1 (register v0.23); the owner's ratification of 2 November 2026 (`exchange/STOCKTAKE_2026_11_02_v0_7.md`, last section) |
| Plain-English direction | `doc/Direction_for_operational_procedures_v0_2.md` (v0.2r1 in `exchange/`; content-checked by the reviewer, PASS) |
| Probe findings carried | A1, A2, A3, A6, A7, A8, A11 (register v0.23) |
| Reviewer input carried | the three takeover notes (1 November); Response 2 of the stock-take (the three-way split, the primary statement for Q1, no double scoring, an unaccepted draw left open, the status block, the registry-versus-register distinction); the direction content check |
| Evidence state | DESIGN ONLY. Nothing implemented, nothing tested |

## 0. The whole thing in plain English

Today the system can only look at draws before the holdout. To make real next-draw forecasts we need four things, in this order:

1. **Read a results file that has grown.** Every reader today refuses the results file as soon as it has a second version (finding A1): even an update that finds nothing new writes a NO_CHANGE line and stops everything. The first job is a reader that accepts the updater's later versions, checks their history, and still serves each forecast only the draws before its target.
2. **Open the holdout, once, on the record.** You freeze a study plan (which methods, which measures, which software, which installed packages), then write the opening record. Only then does the updater add the holdout draws and every later draw.
3. **Mode H.** Every released variant forecasts each of the ten holdout draws, each from the draws before it. No forecast is scored until all are frozen; then the ten draws are scored once. Powerball 1585 and 1586 carry their exposure flag and count fully. Under the owner's preferred reading (option A) this is a precommitted holdout evaluation, not pre-draw forecasting, and the design says so.
4. **The weekly session (MH-1).** Per game, one command: it works through every draw that has a result but no score, strictly in draw order, scoring an existing forecast or making, freezing and scoring a catch-up forecast; then it freezes the next draw's forecast before that draw. Everything runs offline; the timing proof is a local, chained record; a GitHub push is only an optional witness.

The draws in view (from the weekly calendar rule): the planning target is **Oz Lotto 1709 on Tuesday 17 November** and **Powerball 1592 on Thursday 19 November** as the first forecasts frozen before their draws; the week of 9 November (Oz Lotto 1708, Powerball 1591) is a stretch only. Whatever the first session's date, the catch-up covers every draw since the holdout: Oz Lotto 1704-1706 and Powerball 1587-1589 as development evidence (they predate the 31 October installs), Oz Lotto 1707 onward and Powerball 1590 onward as CATCH-UP.

## 1. Mode H: the reading of "frozen before the holdout is opened" (Q1)

Register v0.23 ("Terms for that design") and H-1 section 10 describe Mode H as: every released variant forecasts each of the ten holdout draws **walk-forward (each from the draws before it)**, **all frozen before the holdout is opened**, then scored once. Both halves cannot hold literally: the forecast for Powerball 1578 must be trained on draw 1577, which is itself a holdout draw. The stock-take round weighed three readings:

- **A (the owner's preference, 2 November 2026): the study plan and code are frozen before the holdout is opened; the holdout is opened and added to the results file; then one Mode H batch forecasts all ten targets, each method seeing only the draws before its target (the N-1 rule, which test T-05 already proves); every forecast is frozen, create-only, before the scorer reads any holdout result; then the ten are scored once.** This is exactly how the reviewed walk-forward batches and the WF-1B scorer already work, so it needs the least new code, and it is exactly what the weekly catch-up will do, so Mode H doubles as the rehearsal of the weekly mechanics. Its honest description, which this design uses throughout: **a precommitted holdout evaluation with N-1 isolation, not pre-draw forecasting**: the outcomes are already in the system when the forecasts are made, held away from the methods by the reader.
- **B (kept as the alternative for the reviewer's R-3 review):** for each target in turn, freeze every forecast for N, then release N's result, score N, move on. The forecasting half exists (the driver runs one target at a time); what B adds is a staged release of the results file (ten updater steps or a capped copy of the master, each with its own ledger line), a check that each forecast predates the line that admitted its outcome, and recovery rules for a stop halfway: new code in the most protected area (master, ledger, readers). It buys a local timestamp ordering between each freeze and each release; since the outcomes are already public, it is not prospective evidence either.
- **C (withdrawn):** forecast all ten holdout draws from the development draws only, freeze, then open and score. Checked at the base: no released method uses its target's draw number in its calculation (the driver runs unordered, date-free views; `walk_forward.py` line 45; E_1 alone carries the target in its forecast record as a label, `contract_adapters/e_001.py` line 27). With the same training prefix every variant would therefore produce the same ranking ten times, scored against ten different draws: a fixed-origin test of one forecast, not a test of the retraining process.

**The primary statement Mode H supports (RECOMMENDED wording, for the register amendment):** "a locked holdout study: the study plan and code were frozen before the holdout was opened; every forecast used only draws before its target; no forecast was scored until all were frozen." The register's sentence "all frozen before the holdout is opened" is to be read, and in register v0.24 amended, to this wording; register v0.23's text is not edited. **Q1 stays OPEN until this review and the owner's ratification of the design.** Everything below is written for A and says where B would differ.

## 2. Piece 1: reading a results file that has grown (finding A1)

### 2.1 What the code does today

- `src/methods/_common/game_draws_reader.py` lines 241-254: the run manifest must pin `ledger_version == 1`; the ledger must have exactly one row, `INIT`, with `last_draw == holdout_first - 1`; line 237: the target must be below `holdout_first` (`game_profiles.historical_development_target_allowed`, lines 72-76), apart from E_1's forecast-only 1577 exception (lines 234-236).
- `src/methods/_common/walk_forward.py` lines 100-109 and 184-195: a batch pins row 1 of the ledger only, with `ledger_version: 1`, and refuses `last >= holdout_first`.
- `src/evaluation/outcome_reader.py` lines 49-51 and 55-80: targets only in `[first_draw + 1, holdout_first - 1]`, and the ledger must be the single INIT row.
- `src/evaluation/report.py` lines 125-126: `last <= holdout_first - 1`.
- The updater (`src/results_master_v0_1.py`): rewrites the whole master with `to_csv_bytes` (lines 185-189: the header, then one CRLF-terminated line per draw) after appending the new draws (lines 640-647); appends one ledger row per run, `UPDATE`, or `NO_CHANGE` with the same SHA-256 and a new version number (lines 633-636); keeps a create-only backup of the previous master (line 639) and a create-only copy of what it fetched (line 613). The INIT master was written by the same `to_csv_bytes` (`cmd_init`). `Run_Results_Updater.bat` with no arguments runs `update` with the default window (its line 4 and line 33). **Consequence, binding until piece 1 is installed: the updater is not run in any form.** A `NO_CHANGE` row alone makes every batch, run, report and install's suite step refuse; the updater itself still works, and committed records stay readable as files.

### 2.2 The version-2 reading rules (RECOMMENDED)

One shared, orchestration-only module, `src/methods/_common/master_versions.py`, used by the draw reader, the outcome reader, the walk-forward driver, the report and the weekly command. Nothing in it reaches a method; its outputs never enter a `DrawView` (the B1 rule holds).

1. **Ledger chain check.** The header equals the updater's `LEDGER_COLUMNS` exactly. Versions run 1, 2, 3, ... with no gap. Row 1 is the INIT row with today's exact checks (unchanged). Every later row is `UPDATE` or `NO_CHANGE`:
   - `NO_CHANGE`: the same `master_sha256`, `first_draw`, `last_draw` and `draw_count` as the row before; `added_count` 0.
   - `UPDATE`: the same `first_draw`; `added_first` = previous `last_draw` + 1; `added_last` = `last_draw`; `draw_count` = previous `draw_count` + `added_count`; `backup_sha256` = the previous row's `master_sha256`.
   - Any other action, or any broken rule: refuse. The INIT verification record is checked as today.
2. **Prefix-verified pins.** Because the updater only appends and re-serialises with the same function, version v's bytes are an exact prefix of every later version. The reader therefore checks **every row** of the ledger against the current master: the SHA-256 of the first `1 + draw_count(row)` lines (the header and that row's draws, each with its CRLF) must equal the row's `master_sha256`, and the whole file's SHA-256 must equal the last row's. A run still pins `(ledger_version v, master_sha256 s)`; the pin is accepted when row v exists with that SHA-256 and passed the prefix check. Consequences:
   - the committed batches and reports (pinned to version 1) stay verifiable after any update;
   - a `NO_CHANGE` row needs no special handling;
   - a later change to any earlier row (a correction) breaks the prefix check and every run refuses: result corrections need their own reviewed design (R3 10.3); this note does not provide one;
   - an update interrupted between the master replace and the ledger append (finding A7) leaves a master whose full SHA-256 matches no row: every reader refuses, and so does the updater's own next run (`load_verified_master`, lines 298-300). Recovery is in section 6.
3. **The target ceiling.** For a pin to version v, the reader allows targets up to `last_draw(v) + 1`. A target at or above the game's `holdout_first` additionally needs a valid opening record for that game (section 3.2); without one the reader refuses exactly as today. The E_1 1577 exception is unchanged.
4. **What does not change.** The prefix parse (`_parse_prefix`, lines 161-209) still reads no data column of the target or any later row. View schemas and digests are unchanged, so every existing forecast, golden and T-05 test is unchanged. Whole-master and prefix SHA-256 values remain orchestration-only provenance.
5. **The outcome reader** uses the same chain and pin rules and serves targets up to `last_draw(v)` only. It releases a target's outcome to a scoring step only under the **freeze-before-outcome rule** of section 4.3.

**Tests (planned; R-4 oracles):** a synthetic ledger of one INIT, two UPDATE and one NO_CHANGE rows, with every chain rule broken once (each must refuse); a byte-exact prefix oracle built independently of the updater; T-05 rerun on a version-3 synthetic master (the same view bytes and digests as on version 1 for every development target); a corrected earlier row must refuse; an "interrupted update" fixture (master replaced, ledger not appended) must refuse; the existing 471 tests unchanged.

## 3. Piece 2: opening the holdout (findings A2, A3) and the install records (Q5)

### 3.1 The study manifest (R3 6.2)

Before the holdout is opened, an owner-run command writes, create-only, `results/real/holdout/<GAME>/MODE_H_STUDY_MANIFEST_V1.json`, and appends one search-log row (R3 7.4). It binds:
- the cohort: every released (game, method, variant) with its declaration digest and registry-entry digest, and every registered method that is not runnable, by name and status (R3 10.1(3); mark, never suppress);
- the targets: the ten holdout draws (Powerball 1577-1586, Oz Lotto 1694-1703), with the exposure flags of HX-1 (Powerball 1585 and 1586);
- the measures and the Mode H families (section 4.4), the N1 seed policy, and the scorer's version;
- the code: the SHA-256 of every file under `src/` that the batch and the scorer import;
- **the environment (R3-T50):** the Python version and the exact name and version of every installed distribution in the venv (`importlib.metadata`), and their digest. This also closes the open item that the owner's full package list was never recorded.

The owner may commit it to GitHub as an optional witness (OFF-1).

### 3.2 The opening record (finding A2)

`HOLDOUT_OPENED_<GAME>.json` (schema `HOLDOUT_OPENED_V1`) is today defined only by the updater's check (`results_master_v0_1.py` lines 135-150: `schema`, `game`, a 64-hex `study_manifest_sha256`, `opened_utc`, `owner_statement`). Design:
- written only by a new owner-run command, `open --game G`, create-only in `source_data/`, after it checks that the study manifest exists, is valid and has the SHA-256 it names; the owner types a fixed sentence as `owner_statement`;
- it is permanent, and it also unlocks every later update for that game: intended, because after Mode H the weekly session needs those updates;
- the readers (section 2.2 rule 3) accept it with the updater's field checks, plus a check that the named study manifest exists with that SHA-256.

### 3.3 Install records (Q5; owner-ratified mechanism, 2 November 2026)

MH-1 makes a catch-up forecast valid only if the method revision was installed before that draw's date; OFF-1 says this is checked against local install records, not Git history (E2R-R54 also says Git history is never relied on). Design:
- **From package A onward**, every code install writes one create-only record, `src/methods/_common/contract_data/install_records/INSTALL_<PACKAGE>_V1.json`, by a small tool in the package run right after POST PASS and before staging, so the record is committed with the package; it holds the package name, its manifest SHA-256, the UTC time and the local calendar date of the POST PASS, and the list of (game, method, revision, variant) registry entries the package added or released. The verifier's COMMITTED phase checks it is present and consistent. The verifier itself stays read-only.
- **For the current cohort**, one record, `INSTALL_BASELINE_20261031_V1.json`, travels in package A as an ordinary reviewed member: all 40 released variants, install date 31 October 2026 (REL-1 at `6a1bed9`, WF-1A at `0d98706`, E1R2 at `86d12ea`; register v0.23 lines 1183, 1189, 1215). The owner's installation of package A is his confirmation of it.
- **The rule (RECOMMENDED):** a catch-up forecast for draw N by a variant is CATCH-UP if the variant's install date (local calendar date) is before N's derived draw date; otherwise it is development evidence. Format, verification (the record's own digest; the registry entries it names must exist) and recovery (a missing record makes the variant ineligible for CATCH-UP, never an error) are what Q5 leaves to this design.

### 3.4 The order of events for each game (each step is the owner's separate approval)

1. Packages A and B installed and verified. Nothing has read a holdout result.
2. **Approval 1:** freeze the study manifest; write the opening record.
3. **Approval 2:** the first results update (`Run_Results_Updater.bat update --games G`; never bare). It adds the holdout and every later draw in one version (finding A3). Before this first run, the updater's offline `--self-test` is run under Python 3.15 (finding A9).
4. **Approval 3:** the Mode H batch (section 4).
5. **Approval 4:** the Mode H score and report (sections 4.3 to 4.5).
6. Then the owner decides whether to declare the system developed (GOAL-1, section 5.7), and the first weekly session follows.

### 3.5 The store (R3 6.2; Q2)

RECOMMENDED: **the combined master** that the updater already writes, with the version-2 reader of section 2. A separate quarantine store releasing one result at a time belongs to option B.

## 4. Piece 3: Mode H

### 4.1 The batch

The existing walk-forward driver gains a Mode H batch kind: `plan --mode H --game G`. It:
- refuses unless the opening record and the study manifest are valid and agree, and the current master version covers the last target;
- takes its cohort, targets and environment from the study manifest (no other choice is possible);
- refuses unless the installed environment and code digests equal the study manifest's (R3-T50: no upgrade within Mode H);
- runs each (variant, target) exactly as today, one contract run each, with `run_mode` `REAL_HOLDOUT`, under the run root `results/real/holdout/contract_runs/` derived from the project root (never caller-chosen; `Method_Contract_Runner.py` lines 89-90 show the pattern). In the contract vocabulary (`contract_vocab.py` lines 69-100) `REAL_HOLDOUT` is reserved and refused today; this package adds the producible row `REAL_HOLDOUT / FORECAST -> (HOLDOUT_FORECAST, HOLDOUT_MODE_H)`; the tier exists, the product kind is new (an E2R-1 vocabulary addition, recorded in the register). The runner's data-source rule (`contract_runner.py` lines 118-121) treats every real mode as REAL_DEVELOPMENT is treated: the project itself, nothing else;
- uses the existing STOP rule unchanged.

Size: 40 variants x 10 targets = 400 runs per game; on the first batches' measured rate (17,280 runs in about 80 minutes) about two minutes per game (estimated).

### 4.2 One batch only

One Mode H plan per game, create-only at `results/real/holdout/<GAME>/MODE_H_BATCH/plan.json`, bound to the study manifest's digest; a second plan is refused. The driver's resume works as today: a run that stops is recorded as stopped and never retried silently; the owner decides what follows; completed runs are kept.

### 4.3 The freeze-before-outcome rule (an always-review subject)

One orchestration-only function, `outcome_release_allowed(game, N)`, with fixed evidence paths and no caller-chosen inputs (E2RC2-B01, B02), decides whether the outcome reader may serve target N to a scoring step:
- for a holdout target: only when the Mode H batch plan and segment records show every (variant, target) of the study manifest with a terminal, consumable record (the batch COMPLETE);
- for a later target: only when the forecast ledger (section 5.5) holds the freeze line for N.
Every frozen forecast record is create-only (`os.link`, as today), so nothing can be added or changed after scoring starts. The score attempt records the digests of the records it scores before its first outcome read. Under option B the same function would instead check the staged-release ledger line for N.

### 4.4 Scoring once, and the report

- The WF-1B scorer and report are reused unchanged in their measures (MR0-MR16), N1 (R = 10,000) and layout, with Part A (descriptive) first. The report's ceiling (`report.py` lines 125-126) is relaxed for a Mode H batch with a valid opening record. New Mode H families are added to the family registry with `mode: "H"` and windows equal to the ten targets; they are fixed in the study manifest before opening.
- **N1 seed (RECOMMENDED):** reuse the approved root `N1_ROOT_NIST_C2_20261031T1030Z_V1` unchanged. N1's streams are keyed by policy, root, game, replicate and target (`src/evaluation/n1_generator.py` lines 48-50), and no earlier report used a target at or after the holdout, so the Mode H targets draw fair draws never generated before. Alternative: a fresh pre-announced pulse, which adds at least a day.
- **Scored once:** one score attempt per game, create-only; a second is refused unless the first ended in a STOP before any outcome read.
- **Flags:** Powerball 1585 and 1586 carry `HOLDOUT_EXPOSED_HX1` in every per-target record and in the report; they are scored and counted in every measure like any other draw (no gap, nothing excluded); the flag is information only.
- **Words:** the report describes any null result as "no statistically compelling departure from the fair-draw reference under the reported measures", never as proof of randomness; it states that ten draws per game give limited statistical power; and it labels the study as a precommitted holdout evaluation (section 1).
- **No double counting:** the weekly session never re-forecasts or re-scores the Mode H draws for a variant that has Mode H records (section 5.3); the league table shows Mode H in its own column.

## 5. Piece 4: the weekly session (MH-1, OFF-1, EFF-1)

### 5.1 Two programs, in order

1. **The results update**, the owner's updater, run by the owner first (`Run_Results_Updater.bat update --games POWERBALL,OZLOTTO`); the only step that needs the internet. The updater and the forecasting and scoring code stay separate programs (MH-1).
2. **The weekly command**, `Run_Weekly_Session.bat --game G` (a new wrapper with the standard venv checks), offline, refusing unless the game's developed record exists (section 5.7).

### 5.2 The status block

The command first prints, per game: the last accepted draw (from the master); the last draw with a forecast and the last scored draw per variant, summarised; the backlog (outstanding draws); the next target, its derived date and its deadline; the number of active variants; and the label each outstanding target will receive. If an expected result is not yet in the master, it says so and does nothing for that target.

### 5.3 Outstanding draws, strictly in order

For each active variant of the game, the command's scope is every draw from the game's `holdout_first` onward (the holdout draws included, so that a method released later gets development-evidence forecasts for them), except the draws that variant already has Mode H records for. Working through the accepted draws in ascending order, for each target N:
- a frozen forecast exists and is scored: nothing;
- a frozen forecast exists, unscored, and N's result is accepted: score it (section 5.6);
- no forecast exists and N's result is accepted: run one contract run (run mode by the rule in 5.4), freeze it, then score it;
- N's result is not accepted: stop here for this variant and report it in the status block.
Only when every accepted draw is scored does the command move to the next target (5.4). Nothing is scored twice: a score record is create-only, keyed by (variant, target), and the command checks the score ledger before scoring. A separately identified scoring run to correct a scorer fault or add a measure is the exception, under its own identity (the three-way split, 2 November 2026).

### 5.4 Run modes and labels (Q3, Q4, Q5)

The command decides each run's mode by a fixed rule before the run, so the contract vocabulary stays a pure table (E2R-R41):
- N's result is accepted and the variant's install date is before N's draw date: run mode `CATCH_UP` (new), producible row `CATCH_UP / FORECAST -> (CATCH_UP_FORECAST, CATCH_UP)` (a new tier);
- N's result is accepted and the install date is not before N's draw date: run mode `REAL_DEVELOPMENT`, tier `DEVELOPMENT_WF_EXPLORATORY`, as today (its runs go to the development run root);
- N = last accepted draw + 1 and the time is before N's deadline: run mode `FINAL_NEXT_DRAW` (unreserved here), row `FINAL_NEXT_DRAW / FORECAST -> (PROSPECTIVE_FORECAST, PROSPECTIVE)` (the tier exists); the forecast is left open;
- N = last accepted draw + 1 and the deadline has passed: refuse to forecast; the status block says the draw will be caught up once its result is accepted (the owner's accepted position: a missed deadline costs that week's pre-draw standing, nothing else).
Exposure flags: Powerball 1587 and 1588 carry `HOLDOUT_EXPOSED_HX2` in their records and scores whatever their label (for the current cohort, development evidence; HX-2). One run root for `CATCH_UP` and `FINAL_NEXT_DRAW`: `results/real/weekly/contract_runs/`.

**The deadline (Q4, RECOMMENDED):** 00:00 local time on the draw's date, computed from the PC's clock and time zone (no new dependency), recorded in the ledger as the UTC instant and the local offset. It needs no knowledge of the draw hour and leaves each game several days: Oz Lotto from Wednesday to Monday night, Powerball from Friday to Wednesday night. Alternative: a fixed UTC instant (12:00 UTC on the day before), independent of the PC's time zone setting.

**Invariant:** at most one open forecast per active variant per game, and exactly one whenever the next target is still before its deadline; a newly released revision has none until the command has caught it up; a retired one has none ever again.

### 5.5 The forecast ledger: the timing proof (OFF-1; supersedes R3's push clauses for this project)

- A local, create-only, digest-chained **forecast ledger** per game, `results/real/weekly/<GAME>/FORECAST_LEDGER_V1.jsonl`. When every active variant's run for target N is frozen (or recorded as failed or not runnable), the command appends one line: the target and its derived date, the run mode and tier, the freeze time (UTC and local offset), the deadline, the roster with every run record's digest and every registered but non-runnable method by status (R3 10.3), the environment digest, the master version and SHA-256 pinned, and the previous line's digest. A line is appended only after every record it names is frozen; the freeze-before-outcome rule (4.3) reads this line.
- **What the chain proves (the reviewer's wording, accepted):** that the records agree with each other; comparing it with an earlier trusted digest, kept separately, reveals later changes; by itself it proves neither when the records were made nor that the whole chain was never replaced. Optional witnesses: a GitHub push of the ledger, or an emailed copy of the newest line's digest. A line is proved to predate a draw only when a witness verifiably received its digest before the draw; the report says, per forecast, which witness exists; without one the label stays PROSPECTIVE (OFF-1) and the report says the timing rests on the local record.
- **Tests (R3-D20's "must be tested"):** a ledger line edited, removed or reordered breaks the chain; the command refuses to freeze a `FINAL_NEXT_DRAW` forecast after its deadline; the command refuses to score a target with no freeze line.
- **R3 clauses superseded for this project, on ratification:** 1.3 ("freeze and push the full batch remotely"), 10.1(6), the "COMMIT AND PUSH TO REMOTE" and "SAVE REMOTE REVISION/PUSH EVIDENCE" steps of 10.2, "remote publication evidence" in 11.5 item 4, and R3-D20's push requirement. The register records the supersession; R3's text is not edited (a later R3 edition folds it in).

### 5.6 Scores and the league table (EFF-1)

- A local, append-only **score ledger** per game, `SCORE_LEDGER_V1.jsonl`: one line per scored (variant, target): the per-target quantities WF-1B already computes (TOP and WORST matches, Powerball match, prize division, rank positions), the outcome's source (master version and SHA-256), the label, any flag, and the scorer's version. This is R3 7.6's and 11.5's "outcome ledger" (finding A11). The scoring code reuses WF-1B's measure functions through a thin per-target driver; no measure, label or formula changes.
- The weekly path reads only the new runs and the new draw. The league table is built from the score ledger, cumulative, with PROSPECTIVE, CATCH-UP and development evidence in separate columns, the number of draws beside every figure, and Mode H and the development reports referenced in their own columns; nothing is retuned because of its ranking (MH-1). N1 and the significance tables run over the PROSPECTIVE and CATCH-UP draws only, in the full report.
- **Cadence (Q6, RECOMMENDED):** each session prints a short after-draw note (the scored forecasts and the new forecast) and writes the cumulative table to a dated file; the full report with N1 on request or monthly, each a new dated report with its own search-log row; earlier reports stay as published.
- **Retired revisions:** their forecasts and scores stay where they are; the league table shows "as published" and "current methods" side by side (D-8); a retired index is a later small item (roadmap 21b), not part of this design.

### 5.7 FINAL and "developed" (Q8, RECOMMENDED)

The weekly session **is** R3's FINAL_NEXT_DRAW protocol (R3 1.3 and 10) as amended by 5.5, and the owner's GOAL-1 declaration that the system is developed **is** R3's "explicit FINAL opening". The declaration is a create-only owner record, `source_data/DEVELOPED_<GAME>.json` (written by an owner-run command after Mode H's report, like the opening record), and the weekly command refuses without it. R3 10.1's other preconditions are met or are met by this package (ratified scoring formulas; frozen released variants; the full roster listed; refreshed and digested sources; L identified from the master; the ledger in place). Under OFF-1 the first PROSPECTIVE forecast also needs the supersession of 5.5 ratified first.

## 6. Piece 5: the results update procedure (findings A6, A7, A8)

The updater's code is not changed by this design.
- **A6 (single source):** production uses Lotterywest's results-search page only (an earlier owner decision; TSC-1 retires the two-site checker). RECOMMENDED: record that R2-C03's "independent evidence" and the proposal's candidate-then-promotion step are met in production by the updater's checks (the overlap with the master must match exactly; consecutive numbers; the date rule), the reader's chain check, and the owner's reading of each update's summary (A7); the owner's private, by-hand check of The Lott stays outside the repository and is never automated.
- **A7 (accepting a version, and recovery):** a one-page owner checklist in package B. Normal: read the updater's summary (draws checked, added, warnings), then run the weekly command. **An interrupted update** (master replaced, ledger not appended): every tool refuses with "does not match the last ledger entry"; the recovery is: check that the SHA-256 of the newest file in `source_data/backups/` equals the last ledger row's `master_sha256`; if so, copy that backup over the master and rerun the update, which refetches and re-adds; if not, stop and send the output. **A stale lock** (`source_data/.results_master.lock`, lines 653-672): confirm no updater process is running, then delete the lock. Nothing else is ever edited by hand.
- **A8 (the update window):** the default window (this month plus five back) overlaps the master while sessions run weekly; after a long break the checklist says to use `--months-back` to reach the master's last draw (the updater refuses without an overlap, line 617).

## 7. Packages and schedule (Q9)

RECOMMENDED: **two code packages**, so Mode H is never held up by the weekly work:
- **MHUP-A** (HIGH): sections 2, 3 (the study manifest, the opening command, the install-record tool and the baseline record) and 4 (the Mode H batch, the freeze rule, the Mode H families, the report ceiling); the vocabulary row `REAL_HOLDOUT`.
- **MHUP-B** (HIGH): section 5 (the vocabulary rows `CATCH_UP` and `FINAL_NEXT_DRAW`, the weekly command and wrapper, the ledgers, the deadline, the developed record, the league table) and the section 6 checklist.

**The plan (the owner's planning target of 2 November 2026; not a deadline; FB-1 is the protection):**

| When (Adelaide) | What | Who |
|---|---|---|
| Tue 3 Nov | This design to the reviewer (EX_124) | You relay; the reviewer reviews |
| Wed 4 - Thu 5 Nov | Review rounds; your ratification and answers to Q2-Q4, Q6-Q9 | Claude; you |
| Thu 5 - Sat 7 Nov | MHUP-A code, tests, mutation checks, rehearsals; code review; Claude Code rehearsal (T016); install | Claude; the reviewer; you |
| Sun 8 - Wed 11 Nov | MHUP-B the same (T017) | Claude; the reviewer; you |
| Wed 11 - Fri 13 Nov | Approvals 1-4 per game; Mode H run and scored; your GOAL-1 decision | You |
| Fri 13 - Mon 16 Nov | First session, both games: catch-up of Oz Lotto 1704-1708 and Powerball 1587-1591; Oz Lotto 1709 frozen before 00:00 Tue 17 Nov | You |
| Tue 17 - Wed 18 Nov | Powerball 1592 frozen before 00:00 Thu 19 Nov | You |

Each review round that needs a recheck costs about half a day; the snapshot took four rounds. If the plan slips, the first prospective forecasts move a week and the catch-up covers the draws in between (FB-1). I will say so the day it happens.

## 8. Decisions

- **DECIDED** (owner): MH-1, OFF-1, EFF-1, HX-1, HX-2, FB-1, GOAL-1, ORD-1, TSC-1 (register v0.23); and, on 2 November 2026 (stock-take record v0.7): the three-way split (forecasts frozen; scores kept, new scoring runs beside them; rankings as new dated reports); archive-and-index for a retired revision; the three labels; the status block; at most one open forecast per active variant per game, nothing scored twice, an unaccepted draw left open; Q1 preference A with B kept for review and C withdrawn; Q5's mechanism (local install records; a one-off record for the current cohort); the planning target.
- **RECOMMENDED** (for the owner, after review): the primary statement and register amendment for Mode H (section 1); the version-2 rules (2.2); the install-record rule and format (3.3); Q2 the combined master (3.5); the N1 seed reuse (4.4); Q3 the run modes and tiers (5.4); Q4 the deadline (5.4); Q6 the cadence (5.6); Q8 FINAL and the developed record (5.7); Q9 two packages (7); the R3 supersession list (5.5); the A6 reading and the A7 recovery steps (6).
- **OPEN, for the owner:** Q1 (A or B; the owner's preference is A); **Q7, the display rule after opening:** today nobody may display or compute with Powerball 1577 or later or Oz Lotto 1694 or later; after a game's holdout is opened and Mode H scored, those draws are ordinary history for training and scoring; RECOMMENDED: from then on the rule for that game becomes "no lottery-results searches, no results websites, and no draw outcome pasted into the chats except inside report text the owner chooses to share"; until the owner decides, the rule stays exactly as it is.
- **Not in scope:** result corrections (R3 10.3), WF-1C, a cross-batch report reusing frozen records and the retired index (roadmap 21b), Method A's diagnostics, any change to the updater or the two-site checker, the method-registry presentation (the method registry is the operational list of methods and their status; the ratification register is the record of decisions; the two are different things and stay so).

## 9. Not tested, and what the code round must show

Nothing here is implemented or tested. The code round must show: the chain, prefix and interrupted-update tests (2.2); T-05 on a grown synthetic master; the install-record tool and the baseline record's validation; the Mode H batch refusing without a valid opening record, with a mismatched study manifest, with a changed environment, and a second time; the freeze-before-outcome function refusing before the batch is complete and before a freeze line exists; the scorer refusing a second attempt; the weekly command's ordering (an earlier outstanding draw is always scored before a later one is forecast), its refusal after the deadline, its double-scoring guard and its handling of an unaccepted result; the ledger chain tests; mutation checks for each rule; LF and CRLF rehearsals; Claude Code rehearsals on Windows (T016, T017). All tests on invented data; none reads a holdout result.

## Appendix A. The reviewer's stock-take cautions, and where each lands

| Caution (Response 2 / direction check) | Where |
|---|---|
| Steps must not score the same target twice; a result for N must be known to the scorer but not to the method forecasting N | 5.3; 2.2 rule 4 (the reader reads no row at or after the target) |
| "Find the last forecast" safe for a new revision, a retired one, missing results, a partial session | 5.3 derives state from the frozen records and the ledgers, per variant; 5.4 invariant |
| "Exactly one open forecast" is an aspiration, not yet demonstrated | 5.4 states the invariant precisely; 9 tests it |
| A catch-up forecast is not pre-draw, however strict its isolation; labels kept apart; Q5 dates conditional | 5.4; 3.3 |
| Re-scoring means a new dated report, not an edit; scores can be re-verified under a new identity | 5.3, 5.6 |
| Retirement: index, not move; both report views | 5.6; roadmap 21b |
| Mode H under A is a precommitted holdout evaluation, not pre-draw forecasting | 1, 4.4 |
| Mode H's second pass over the same draws would double count | 4.4 last bullet, 5.3 |
| The chain's evidential limits; the witness must verifiably receive the digest before the draw | 5.5 |
| Operator status block | 5.2 |
| Backups need a restore test; GitHub is not a backup of git-ignored records | 6 checklist (package B) |
| Method registry versus ratification register | 8, not in scope |

## Appendix B. Changes from v0.1

1. Section 1 rewritten: options A, B and C; C withdrawn with the checked reason; the owner's preference A; the honest wording and the register amendment; Mode H described as a precommitted holdout evaluation throughout.
2. Section 2: the NO_CHANGE warning made binding; the prefix check applied to every row; the interrupted-update case named; its test added.
3. Section 3.3 new: install records (Q5), the baseline record, the rule.
4. Section 4: the run root; the runner's data-source rule for real modes; "scored once" and "no double counting" stated; the report's words.
5. Section 5 rewritten: two programs in order; the status block; outstanding draws strictly in order with the four cases; run modes decided by rule, with the new `CATCH_UP` mode and tier and `FINAL_NEXT_DRAW` unreserved; the deadline refusal; the invariant as "at most one"; the ledger's exact contents and the reviewer's wording on what the chain proves; the complete R3 supersession list; the score ledger as R3's outcome ledger; the developed record as the FINAL opening.
6. Section 6: the recovery steps for an interrupted update and a stale lock.
7. Section 7: the honest plan (13-15 November; the week of 9 November a stretch), two rehearsal task numbers.
8. Section 8: the 2 November decisions moved to DECIDED; the method-registry note.
9. Appendix A new: where each reviewer caution lands.

*End of design v0.1r1.*
