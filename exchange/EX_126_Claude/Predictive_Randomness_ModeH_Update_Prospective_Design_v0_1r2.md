# Mode H, the results update and the prospective mode - design v0.1r2

**Version:** v0.1r2, 3 November 2026 (Adelaide, UTC+10:30). CANDIDATE for the reviewer's focused RECHECK after EX_125 (R-3, HIGH). Replaces v0.1r1 (EX_124). Appendix B is the resolution table for every EX_125 finding; Appendices E to L are the eight acceptance items EX_125 section 5 asks for.
**Author:** Claude (the primary designer and coder). **Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner.
**Base:** `main` at `3a9f6ac` (documents); `src/` and `tests/` unchanged since PERF-1 at `3fce327` (register v0.23). Every code citation gives file and line at that base; Appendix D anchors each one to its Git blob id and quotes the line's text, so the citation can be checked in any view (EX_125 C07).
**Authorises nothing.** No run, update, holdout opening, Mode H, FINAL or prospective forecast follows from this text. Each of those stays a separate owner approval after review.
**Holdout statement:** this note contains no outcome of any draw. Draw numbers appear only as identifiers. Dates of future draws were derived from the era profiles' weekly rule (`game_profiles.derived_date`), not from any result.

## Terms used in this note

- **MHUP-1:** this work item (Mode H, the results Update and the Prospective mode). **MHUP-A, MHUP-B:** its two code packages (section 8).
- **Mode H:** the one-time test on the ten sealed holdout draws per game (Powerball 1577-1586, Oz Lotto 1694-1703).
- **The master:** a game's results file, `source_data/<GAME>_results_master.csv`; **the master ledger:** its append-only version list, one row per updater run. **The forecast ledger**, **the witness ledger** and **the score ledger** are new weekly records (sections 6.5, 6.6). R3's **outcome record** is the master row that supplied an outcome, identified by master version and SHA-256; R3's **evaluation record** is the score ledger (6.6).
- **"Version 1 only":** today every reader accepts only the first (INIT) master version. **The version-2 rules** (section 3) accept version 2 and every later version.
- **Freeze** has three senses, kept apart: the **plan freeze** (the study manifest and code fixed before the holdout is opened, 4.1); a **frozen forecast** (a method's run record, published create-only, as today); a **freeze line** (one line of the forecast ledger saying every active variant's run for a target is DONE, 6.5).
- **DONE, COMPLETE:** the driver's terms for a planned run that ended in a continue class, and for a batch all of whose runs are DONE (5.2).
- **Binding:** the block in a run request that names the Mode H batch or the weekly session the run belongs to; the gates resolve it at fixed paths (3.4). The requests that need one are `REAL_HOLDOUT`, `CATCH_UP`, `FINAL_NEXT_DRAW`, and `REAL_DEVELOPMENT` with a target above the development prefix; `REAL_DEVELOPMENT` within the prefix (today's batches) and the synthetic modes carry none, as today. An **unbound** request of the first kind refuses to publish.
- **Seal:** a value-free marker beside a game's Mode H batch record, written by the scorer when the Mode H score is COMPLETE; the dispatch gate reads it to refuse further holdout runs (5.2).
- **Session:** one invocation of the weekly command for one game, with its create-only session record and its session lock (6.1). Every run of a session pins the master version the session record pins; if the master has grown meanwhile, the run refuses and the session is over (fail closed).
- **Evidence tier:** the label a scored record carries: `HOLDOUT_MODE_H`, `PROSPECTIVE`, `CATCH_UP` (new) or `DEVELOPMENT_WF_EXPLORATORY` (R3 17.3.9; MH-1). **Effective class:** what a report counts a record as, derived by the total rule of Appendix I from the tier, the deadline, the outcome timing and the install evidence; one record's effective class can be `LATE_PRE_DRAW` (new; an operational category, never counted as evidence of any tier). "Development" has two senses: the development **prefix** (draws before the holdout, R3 6) and the development **tier**; 3.2 rule 3 and 6.4 keep them apart.
- **Publication status:** `PUBLISHED_BEFORE_DRAW` or `TIMELINESS_UNVERIFIED` (R3 10.5), derived at report time from the witness ledger (6.5); never stored in a frozen record or a score line.
- **Q1 to Q11:** the owner's questions, listed with their answers in section 9.
- **R-4 oracles:** the reviewer's right to independent reference checks (exact-arithmetic or independently built fixtures) for high-consequence code (agreed position; H-1 1.4).

## Work-item card

| Field | Value |
|---|---|
| Item | MHUP-1 (roadmap item 10c; GOAL-1, ORD-1) |
| Author / reviewer | Claude / ChatGPT reviewer chat (R-3 design review, EX_124 to EX_127; R-2 later for the code) |
| Risk tier | HIGH (reader, digest and record-validator code; the dispatch gate; evaluator and scorer; holdout access and unsealing; freezing and publication; contract vocabulary; a new E_1 revision; launchers and an orchestrator; `source_data/`) |
| Owner inputs (binding) | MH-1, OFF-1, EFF-1, HX-1, HX-2, FB-1, GOAL-1, ORD-1, TSC-1 (register v0.23); the ratification of 2 November 2026 (stock-take record v0.7, last section); the decisions of 3 November 2026 (roadmap 10c): **Q10** ER-2r1 extended to E_1 revision 3; **Q1** option A, the corrected design still to pass this recheck before the owner ratifies it as a whole; **B02** MH-1's per-target order implemented exactly; **C03** Lotterywest's published results are trusted as official, no second-source check in production |
| Plain-English direction | `exchange/Direction_for_operational_procedures_v0_2r1.md` (content-checked by the reviewer, PASS; a copy with a status line goes into `doc/` with the next document package, R-013) |
| Probe findings carried | A1, A2, A3, A6, A7, A8, A9, A11 (register v0.23) |
| Reviewer input carried | the three takeover notes of 1 November; Response 2 of the stock-take; the direction content check; **EX_125** (5 BLOCKER, 9 CORRECTION, 3 OPTIONAL; Appendix B) |
| Evidence state | DESIGN ONLY. Nothing implemented, nothing tested |

## 0. The whole thing in plain English

Today the system can only look at draws before the holdout. To make real next-draw forecasts we need five things, in this order:

1. **Read a master that has grown.** Every reader today refuses the master as soon as it has a second version (finding A1): even an update that finds nothing new writes a NO_CHANGE line and stops everything. The first job is a reader that accepts later versions, checks their history, and still serves each forecast only the draws before its target.
2. **Let E_1 take part.** E_1's installed revision 2 refuses, in its own code, every run mode except development and every target beyond the development cap (section 2). It gets a revision 3 with the same arithmetic and wider admission, in the first package, under the one-package exception the owner has extended to it (Q10).
3. **Open the holdout, once, on the record.** You freeze a study plan (which methods, which measures, every file of code and every launcher, every installed package), then write the opening record. Only then does the updater add the holdout draws and every later draw, once; nothing else may change until Mode H is scored.
4. **Mode H.** Every released variant forecasts each of the ten holdout draws, each from the draws before it (the reader hands a method nothing from its target draw or later: that is what "N-1 isolation" means below), inside one owner-approved batch that every run must name. No forecast is scored until every planned run is finished; then the ten draws are scored once. Powerball 1585 and 1586 carry their exposure flag and count fully. This is **option A, the owner's decision of 3 November 2026**: a precommitted holdout evaluation, not pre-draw forecasting, and every record and report says so.
5. **The weekly session (MH-1).** Per game, one command you type. It works through every draw that has a result but no score, one draw at a time and exactly in MH-1's order: forecast N from the draws before it, reveal N, score N, then N+1; then it freezes the next draw's forecast before that draw's deadline. Inside the command, a small sequencer runs two separate programs in turn, one that forecasts and one that scores, so methods and the scorer stay apart. Everything runs offline; the timing proof is a local, chained record; a GitHub push is an optional witness whose status is worked out at report time.

The draws in view (from the weekly calendar rule): the planning target is **Oz Lotto 1709 on Tuesday 17 November** and **Powerball 1592 on Thursday 19 November** as the first forecasts frozen before their draws (in practice by 23:00 the evening before, because the command stops starting a forecast within the last hour before midnight); the week of 9 November is a stretch only. Whatever the first session's date, the catch-up covers every draw since the holdout. For the 39 variants released on 31 October 2026, Oz Lotto 1704-1706 and Powerball 1587-1589 are development evidence (they predate the release) and Oz Lotto 1707 onward and Powerball 1590 onward are CATCH-UP; for E_1 revision 3 the boundary is its own release date (section 2).

## 1. Mode H: the reading of "frozen before the holdout is opened" (Q1, decided)

Register v0.23 ("Terms for that design") and H-1 section 10 describe Mode H as: every released variant forecasts each of the ten holdout draws **walk-forward (each from the draws before it)**, **all frozen before the holdout is opened**, then scored once. Both halves cannot hold literally: the forecast for Powerball 1578 must be trained on draw 1577, which is itself a holdout draw. The stock-take round weighed three readings; the owner decided **A** on 3 November 2026, after the reviewer's EX_125, which provisionally favours A (O01) provided B01, B04 and C05 are met (they are, in sections 3.4, 4.1 and 5.3).

- **A (decided):** the study plan and code are frozen before the holdout is opened; the holdout is opened and added to the master, once; then one Mode H batch forecasts all ten targets, each method seeing only the draws before its target (the N-1 rule, which test T-05 already proves); every planned run is DONE, and every published forecast frozen create-only, before any approved scoring process reads any holdout result; then the ten are scored once. Its honest description, used throughout: **a precommitted holdout evaluation with N-1 isolation, not pre-draw forecasting**; the outcomes are already in the system when the forecasts are made, held away from the methods by the reader (R3 17.3.5, line 1130: "historical evaluation, not advance-frozen prospective forecasting"). Neither A nor B makes already-public outcomes prospective (EX_125 O01).
- **B (not chosen; kept described truthfully):** for each target in turn, freeze every forecast for N, then release N's result, score N, move on. It buys a local timestamp ordering between each freeze and each release, at the cost of a staged release of the master, a predating check, and recovery rules in the most protected code.
- **C (withdrawn):** forecast all ten holdout draws from the development draws only, freeze, then open and score. The target is not a scientific input of any released method (the driver runs unordered, date-free views: `walk_forward.py` lines 45 and 143-144), but it does enter every method's tie-break key (`contract_records.py` lines 405-409), every non-legacy view digest (`game_draws_reader.py` line 125) and E_1's own tie key (`E_001/multigame_e1.py` lines 23 and 50). Under C the ten forecasts from one prefix would have identical scores and could differ only in the order of tied numbers: a fixed-origin test of one scoring, not of the retraining process. In plain words: C would test the same forecast ten times. The corrected reason is on the roadmap and in the stock-take record (v0.8).

**The primary statement Mode H supports (for the register amendment):** "a locked holdout study: the study plan, the code and the environment were frozen before the holdout was opened; every forecast used only draws before its target; all planned attempts, and every successfully published forecast, were frozen before any scoring process read a holdout outcome." Register v0.23's sentence "all frozen before the holdout is opened" is to be read, and in register v0.24 amended, to this wording (EX_125 C04: "all planned attempts", not "every pair produced a forecast"). Q1 is **OWNER-DECIDED** (3 November 2026) as an input; the design as a whole is ratified after this recheck.

## 2. E_1 revision 3 (a precondition found by the cold read; Q10 decided)

E_1 revision 2's multi-game function (`src/methods/E_001/multigame_e1.py`) refuses any `data_kind` other than `SYNTHETIC_CONTRACT_TEST` or `REAL_DEVELOPMENT` (lines 30-32; the adapter passes the run mode as the data kind, `contract_adapters/e_001.py` line 27) and any target outside `historical_development_target_allowed` (lines 33-34). Both checks are inside the released method's own code, so E_1 would end every Mode H, catch-up or prospective run with `RUNTIME_FAILURE METHOD_FAILED`. Any change to a released method's code is a new revision (E2R-R14A; R3 6.3).

**E_1 revision 3 inside MHUP-A**, by the CODE-3 pattern used for revision 2: the same counting, ranking and tie order as revision 2; the two admission checks replaced: the function takes the **view data kind** (3.3), accepting `SYNTHETIC_CONTRACT_TEST` and `REAL_HISTORICAL_DEVELOPMENT`, and the adapter passes `view_data_kind(task.run_mode)` instead of the run mode, so the method never sees a run mode (EX_125 C06); the target check becomes the shared target gate and mode gates of section 3 (the method keeps only `len(records) == target - first_draw`); revision 2's files archived unchanged under `archive/methods/E_001/r2/` (E2R-R54); a new declaration and registry entries. **Identity proof:** a frozen reference fixture `tests/fixtures/e1_r2_reference_v1.json`, computed at the base outside the repository as E1R2-T01 did with `e1_r1_reference_v1.json`, against which revision 3 must match label for label, in both games, for every ranking and tie output, on invented prefixes under the synthetic kind and the real view kind, and identically under each new real mode on the same prefix (EX_125 C01); the archive is never executed (E2R-R56; `test_code3_retirement.ArchiveIsNeverExecuted`).

**Release (Q10, OWNER-DECIDED 3 November 2026):** ER-2r1 (register v0.23 line 1200: one package, installed in named steps behind E_1's own `IN_DEVELOPMENT.txt`, copied first and deleted last, never committed) is extended to revision 3. EX_125 C01 asks for the whole-package safety argument, because MHUP-A also changes the shared readers, validators, the dispatch gate and the evaluator for the other 39 variants: Appendix J gives the ordered install and what refuses at every interim step, including a **package-wide barrier** (`src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt`, copied first and deleted last, never committed) that the new dispatch gate honours like the orphan marker: while it exists, every run refuses.

Consequences the owner should see: the Mode H cohort stays 40 variants; E_1 revision 3's release date is MHUP-A's install date, so under MH-1's rule (4.3) every draw dated on or before that install is development evidence for revision 3, not CATCH-UP, whatever its number; the baseline install record (4.3) lists the 39 variants released on 31 October 2026 and E_1 revision 2 marked superseded; MHUP-A's own install record lists revision 3. The legacy forecast-only E_1 record for target 1577 (H-1 7.3) stays as it is and is never scored (R3 6: "never Mode H"); the Mode H forecast for 1577 is a separate revision-3 contract record and is scored. Under one data kind (3.3) the two coincide label for label (the same prefix, the same tie rule), a free R-4 oracle: R3 6 protects the legacy record's status, not the numbers. **Existing tests that change** (Appendix L lists every one): `tests/test_code3_retirement.py` line 91 (the archive holds `r1` and `r2`); `tests/test_e1r2_revision2.py` lines 223-239 (revision 2's refusals become revision 3's admissions, and the revision-2-equals-revision-1 test becomes a fixture comparison once revision 3 holds the active `SUPPORTED` entry).

## 3. Piece 1: reading a master that has grown (finding A1)

### 3.1 What pins version 1 or the development ceiling today

The complete inventory at the base (Appendix D anchors every line):

| File and lines | What it does today | New rule |
|---|---|---|
| `_common/game_draws_reader.py` 237, 234-236 | target below `holdout_first` (E_1 1577 forecast-only exception) | the target gate of 3.2 rule 3 |
| `_common/game_draws_reader.py` 241-254 | manifest `ledger_version == 1`; ledger exactly one INIT row | the chain and pin rules of 3.2 |
| `_common/contract_records.py` 335-336 | `validate_run_request`: target below the cap (E2R-R52) | the target gate and the structural part of the mode gates (3.4) |
| `_common/contract_records.py` 354 | `ledger_version` in 1..1 | any version the chain accepts |
| `_common/contract_forecast.py` 275-277 | forecast and diagnostic header: target below the cap | the target gate (a Mode H record is otherwise never consumable) |
| `_common/contract_receipts.py` 68 | receipt `ledger_version` in 1..1 | any version the chain accepts |
| `_common/contract_task.py` 45-46 | view data kind by run mode | one data kind for every real mode (3.3) |
| `Method_Contract_Runner.py` 50 | the command line hard-codes `ledger_version: 1` | the current last row; a `--binding` argument for real modes (3.4) |
| `_common/walk_forward.py` 98-109, 184-185 | the batch pins ledger row 1; refuses `last >= holdout_first` | pins the current last row; the ordinary `WF` kind keeps `last <= holdout_first - 1`; the Mode H kind of section 5 |
| `evaluation/outcome_reader.py` 49-51, 64-69, 120-121 | targets in `[first_draw + 1, holdout_first - 1]`; single INIT row; a second guard | up to `last_draw(v)`, under the freeze-before-outcome rule (5.3) |
| `evaluation/report.py` 125-126 | `last <= holdout_first - 1` | relaxed for a Mode H batch with a valid opening record |
| `E_001/multigame_e1.py` 30-34 | E_1's own admission checks | revision 3 (section 2) |
| `_common/multigame_standalone_contract.py` 43, 120; `_common/multigame_worker_launch_handshake.py` 27; `coordinator_private/multigame_launch_spec.py` 63 | the legacy Package 2 standalone path's and the coordinated path's own ceilings | **unchanged**: the coordinated path stays refused (D2-1) and this design does not touch it |

The updater (`src/results_master_v0_1.py`) rewrites the whole master with `to_csv_bytes` (lines 185-189: the header, then one CRLF-terminated line per draw) after appending the new draws (lines 640-647); increments the version (line 629); appends one ledger row per run, `UPDATE` (643-647) or `NO_CHANGE` with the same SHA-256 (633-637); keeps a create-only backup of the previous master (639) and a create-only copy of what it fetched (613). The INIT master was written by the same `to_csv_bytes` (line 446). `Run_Results_Updater.bat` with no arguments runs `update` with the default window (its lines 4 and 33). **Binding until MHUP-A is installed: the updater is not run in any form.** A `NO_CHANGE` row alone makes every batch, run, report and install's suite step refuse; the updater itself still works, and committed records stay readable as files.

### 3.2 The version-2 rules

One shared, orchestration-only module, `src/methods/_common/master_versions.py`, used by every file in the table above. Nothing in it reaches a method; its outputs never enter a `DrawView` (the B1 rule holds). It carries its own copy of the updater's `LEDGER_COLUMNS`, with a test asserting equality with `src/results_master_v0_1.py` (the owner's tool is not imported by project code). `tests/test_wf1b_static.py` lines 12-14 (`ALLOWED_COMMON`) gains `_common.master_versions`.

1. **Ledger chain check (the closed grammar; EX_125 C02).** The header equals `LEDGER_COLUMNS` exactly, in order. Every row has every column; versions are the integers 1, 2, 3, ... in order with no gap, no duplicate and no extra or truncated line; `utc` parses as an ISO-8601 UTC instant and never decreases; `first_draw` equals the profile's first draw in every row; `master_sha256`, `grab_sha256`, `backup_sha256` and `tool_sha256` are 64 lower-case hex digits where present; `tool_version` is non-empty; `note` is free text, ASCII only. Row 1 is the INIT row with today's checks of its own fields (action, counts, first and last draw, the INIT verification record); the one change is that the run's pin is now bound to its own row v (rule 2), not necessarily to row 1. Every later row is:
   - `NO_CHANGE`: the same `master_sha256`, `last_draw` and `draw_count` as the row before; `added_count` 0; `added_first`, `added_last`, `backup_file`, `backup_sha256` empty; `grab_file` and `grab_sha256` present (the grab itself is not required to exist: it is a local, untracked file);
   - `UPDATE`: `added_count` >= 1; `added_first` = previous `last_draw` + 1; `added_last` = `last_draw` = `added_first` + `added_count` - 1; `draw_count` = previous `draw_count` + `added_count`; `backup_sha256` = the previous row's `master_sha256`; `backup_file` and `grab_file` present;
   - any other `action`, or any broken rule: refuse. The INIT verification record is checked as today.
   This is **cross-row consistency**, not a cryptographic chain of the ledger itself: the rows are plain CSV. The cryptographic link is rule 2, which binds every row to the bytes of the current master.
2. **Prefix-verified pins.** Because the updater only appends and re-serialises with the same function, version v's bytes are an exact prefix of every later version. The reader checks **every row** against the current master: the SHA-256 of the first `1 + draw_count(row)` lines (the header and that row's draws, each with its CRLF) must equal the row's `master_sha256`; the first field of the last of those lines must equal `last_draw(row)`; and the whole file's SHA-256 must equal the last row's. A run pins `(ledger_version v, master_sha256 s)`: every run of a session or batch pins the current last row; the pin is accepted when row v exists with that SHA-256 and passed the prefix check. **Two pins per scored forecast** (EX_125 C02): the forecast record pins its training master version; the score line pins the master version that supplied the outcome; the two need not be the same and both are kept. Consequences:
   - the committed batches and reports (pinned to version 1) stay verifiable after any update;
   - a `NO_CHANGE` row needs no special handling;
   - a later change to any earlier row (a correction) breaks the prefix check and every run refuses: corrections need their own reviewed design (R3 10.3); this note does not provide one;
   - an update interrupted between the master replace and the ledger append (finding A7) leaves a master whose SHA-256 matches no row: every reader refuses, as does the updater's own next run (`load_verified_master`, lines 298-300). Recovery is in section 7.
3. **The target gate** (replacing `historical_development_target_allowed` as the run-time gate in every file of the table): for a pin to version v, targets up to `last_draw(v) + 1`; a target at or above the game's `holdout_first` additionally needs a valid opening record for that game (4.2) **and** the mode gates of 3.4. `historical_development_target_allowed` stays as the **definition of the development prefix** and is what the mode gates use; E2R-R52's "hard-coded target ceilings (now the profile's `historical_development_target_allowed`)" and R3 6's "development caps remain 1576/1693" are amended to this reading in the register. The E_1 1577 legacy exception is unchanged.
4. **What does not change.** The prefix parse (`_parse_prefix`, lines 161-209) still reads no data column of the target or any later row. View schemas and digests are unchanged for every existing run.
5. **The outcome reader** uses the same chain and pin rules and serves targets up to `last_draw(v)` only, and only under the freeze-before-outcome rule (5.3).

### 3.3 One data kind for every real mode

`contract_task.view_data_kind` (lines 45-46) maps `REAL_DEVELOPMENT` to `REAL_HISTORICAL_DEVELOPMENT` (`contract_task.py` line 17) and any other run mode to its own name; the data kind is part of the permitted-view digest, which feeds every tie-break. Every real run mode (`REAL_DEVELOPMENT`, `REAL_HOLDOUT`, `CATCH_UP`, `FINAL_NEXT_DRAW`) maps to the one existing string `REAL_HISTORICAL_DEVELOPMENT`, documented as "the real master's prefix view", so that a forecast depends on the prefix, the configuration and the software only (R3 1.4), never on the mode; every existing digest and golden is unchanged. **The compatibility boundary (EX_125 C06):** "same digest and ranking" means the method's inputs (the permitted view and its digest) and its numerical and ranked outputs, including tie-group order and the first and last admissible targets; the run request, the receipts and the forecast record's metadata rightly differ by mode and binding. The run mode and the evidence tier stay separate, immutable metadata.

### 3.4 The gates: structure, publication and scoring kept apart (EX_125 B01)

Three different things are decided by three different parts, with no caller-chosen authority (E2RC2-B01, B02):

- **(a) Structural validation** (`validate_run_request`, the forecast header, the receipts): a request that needs a binding (Terms) must carry one: `{kind: MODE_H_BATCH, batch_id, plan_digest}` or `{kind: WEEKLY_SESSION, session_id, session_digest}`; its shape and the mode-to-target-range rules are checked here: `REAL_HOLDOUT` only for targets in `[holdout_first, holdout_last]`; `CATCH_UP` and `FINAL_NEXT_DRAW` only above `holdout_last`; `REAL_DEVELOPMENT` above the prefix only above `holdout_last` (never a holdout target); synthetic modes and `REAL_DEVELOPMENT` within the prefix carry no binding and are unchanged. The mode-to-pin rule is checked where the pin is read (the runner, through the reader): `FINAL_NEXT_DRAW` only for target = `last_draw(v) + 1` of the pinned version v (so a `FINAL_NEXT_DRAW` record can never exist for a draw whose result the pinned master already holds); `CATCH_UP` and `REAL_DEVELOPMENT` above the prefix only for targets at or below `last_draw(v)`.
- **(b) Publication admission** (the dispatch gate, `contract_dispatch.py`, which already reads the installed registry and no draw data, E2R-R23A): resolves the binding at fixed roots derived from the project root, reading only value-free records: a Mode H binding must name the game's one plan (5.1), with that digest, listing this exact (game, method, revision, variant, target), and the game's **seal** (5.2) must not exist; a weekly binding must name an existing session record (6.1) for this game, with that digest, listing this variant as active with its release date, and the game's developed record must exist; the request's master pin must equal the session record's pin (a master that grew mid-session fails the session closed); the mode must agree with the install evidence in the session record: `CATCH_UP` only if the variant's release date is before the target's draw date, `REAL_DEVELOPMENT` above the prefix only if it is not; a `REAL_HOLDOUT` request additionally needs the opening record. **A request that needs a binding and has none, or whose binding does not resolve, refuses before anything is read and publishes nothing.** The barriers also live here: the orphan marker and, during an install, `INSTALL_IN_PROGRESS.txt` (Appendix J).
- **(c) Scoring rights** (the evaluator): the freeze-before-outcome rule (5.3) and the binding check repeated: a record is scored only if its binding resolves and it is **the record the plan's roster or the freeze line names for its pair**: the first bound DONE attempt, by `frozen_at_utc` then `run_id` (E2R-R40C's predeclared designation of the one official record per pair; any later bound record for the same pair is listed and never scored).

A hand-typed `Method_Contract_Runner.py run` in one of these modes therefore refuses unless it names an existing plan or session that lists it; the command line gains `--binding` for that purpose and nothing else. **Q11, for the owner (EX_125 B01 asks for a deliberate decision):** RECOMMENDED: admit such a hand-made bound request (it is harmless: if the pair already has a bound DONE record, the hand-made record is a later attempt and is never named by the roster or freeze line, so it is never scored; if it is the first, it is the official record, exactly as if the session had made it); alternative: refuse every real-mode request not made by the driver or the forecasting half, which the gate cannot tell apart from a hand-made one without a per-run secret, so it would need a new mechanism. What neither defends against: someone with write access to the owner's PC creating a plan or session record under the fixed roots by hand; the controls are against mistakes and against the AI chats and the runner, not against the owner's own machine. Appendix E is the gate matrix.

**Tests (planned; R-4 oracles):** a synthetic ledger of one INIT, two UPDATE and one NO_CHANGE rows, with every grammar rule broken once (each must refuse); a byte-exact prefix oracle built independently of the updater; T-05 rerun on a version-3 synthetic master (the same view bytes and digests as on version 1 for every development target); a corrected earlier row must refuse; an interrupted-update fixture (master replaced, ledger not appended) must refuse; a forecast made in each real mode on the same invented prefix has the same digest, ranking and tie order; each structural, publication and scoring gate refused once per rule, including an unbound request, a forged binding digest, a binding to a sealed batch, a `REAL_HOLDOUT` request before any plan, and a `REAL_DEVELOPMENT` request for a holdout target; every existing test unchanged except those in Appendix L.

## 4. Piece 2: opening the holdout (findings A2, A3) and the install records (Q5)

### 4.1 The study manifest (R3 6.2; EX_125 B04)

Before the holdout is opened, an owner-run command (`Run_Evaluation.bat Method_Mode_H.py manifest --game G`; 6.1 for the launcher) writes, create-only, `results/real/holdout/<GAME>/MODE_H_STUDY_MANIFEST_V1.json`, and appends one search-log row of type `MODE_H_STUDY_MANIFEST` (R3 7.4). It binds:
- the cohort: every released (game, method, revision, variant) with its declaration digest and registry-entry digest, and every registered method that is not runnable, by name and status (R3 10.1(3); mark, never suppress);
- the targets: the ten holdout draws, with the exposure flags of HX-1 (Powerball 1585 and 1586);
- the measures and the Mode H families (5.4), the N1 seed policy, and the scorer's version;
- **the executable and scientific closure** (Appendix H): the SHA-256 of **every file under `src/`, whatever its extension** (all Python, the registries, the seed records, the contract data), except the interpreter's byte-code caches (`__pycache__/` and `*.pyc`, `*.pyo`), which are excluded by name and are not code; every `.bat` at the repository root (`Run_Experiment.bat`, `Run_Evaluation.bat`, `Run_Weekly_Session.bat`, `Run_Method_Rankings.bat`, `Run_Coordinator.bat`, `Run_Results_Updater.bat`, the venv wrappers), `requirements.txt` and `install_upgrade_dependencies_into_venv.bat`; the updater's source is under `src/` and is therefore covered. Excluded, with the reason stated in the manifest: `tests/`, `doc/`, `review/`, `exchange/`, `CLAUDE_CODE_WORKING_FOLDER_TREE/`, `.claude/` (not executed in Mode H), and the data folders (`source_data/`, `results/`, `transitory_data/`: data and records, pinned by version and digest separately). The listing is a full enumeration with digests, so an added or deleted file is a mismatch;
- **the environment (R3-T50):** the Python version, the platform, and the exact name and version of every installed distribution in the venv (`importlib.metadata`), and their digest. This also closes the open item that the owner's full package list was never recorded;
- **the master version at freeze** (`v_f`, today's version 1) and the rule that **exactly one** `UPDATE` row may follow it before the batch (the admitted version `v_a = v_f + 1`, section 4.4 step 3).

Every later Mode H step (the plan, every `run` invocation, the score) re-enumerates and re-digests the closure and the environment and refuses on any difference, and refuses if the ledger holds any row beyond `v_a` until the Mode H score is sealed. The updater is the owner's separate program and is not changed; the scientific tools are what refuse, and the checklist says no update runs between Approval 2 and the end of Approval 4. The owner may commit the manifest to GitHub as an optional witness (OFF-1).

### 4.2 The opening record (finding A2)

`HOLDOUT_OPENED_<GAME>.json` (schema `HOLDOUT_OPENED_V1`) is today defined only by the updater's check (`results_master_v0_1.py` lines 135-150: `schema`, `game`, a 64-hex `study_manifest_sha256`, `opened_utc`, `owner_statement`). Design:
- written only by an owner-run command (`Method_Mode_H.py open --game G`), create-only in `source_data/`, after it checks that the study manifest exists, is valid and has the SHA-256 it names; the owner types a fixed sentence as `owner_statement`; one search-log row of type `HOLDOUT_OPENED`;
- it is permanent, and it also unlocks every later update for that game: intended, because after Mode H the weekly session needs those updates;
- the gates (3.4) accept it with the updater's field checks, plus a check that the named study manifest exists with that SHA-256. **The opening record starts the reviewed sequence; it authorises no run by itself** (B01): every real run must also be bound to the plan or a session.

**Exposure after the first update (to be shown to the owner before Approval 2; EX_125 O03):** the six master files are tracked by Git. After the first update, the masters hold the holdout and every later outcome, and when the owner pushes, every clone (this chat's, the reviewer's, Claude Code's) contains them. The rules do not change: no chat and no runner opens `source_data`, `results` or `transitory_data`, and `.claude/settings.json` denies those reads to Claude Code; only the owner decides whether `source_data/` keeps being pushed (OFF-1 makes GitHub optional). `.gitignore` lines (MHUP-A members): `source_data/backups/`, `source_data/grabs/`, `source_data/.results_master.lock` (local working files, covered by the owner's backups); the opening and developed records are small owner records and stay tracked. Q7 (section 9) lists the documents whose wording changes once a game's holdout is open.

### 4.3 Install records (Q5; owner-ratified mechanism, 2 November 2026)

MH-1 makes a catch-up forecast valid only if the method revision was installed before that draw's date; OFF-1 says this is checked against local install records, not Git history (E2R-R54: Git history is never relied on). Design:
- **From MHUP-A onward**, every code install writes one create-only record, `src/methods/_common/contract_data/install_records/INSTALL_<PACKAGE>_V1.json`, by a small tool in the package run right after POST PASS and before staging, so the record is committed with the package; it holds the package name, its manifest SHA-256, the UTC time and the local calendar date of the POST PASS, and the list of (game, method, revision, variant) registry entries the package added or released; the install instructions require steps 1 to 10 of Appendix J on one calendar day, so that date is also the day the variants became runnable (otherwise STOP, and Claude decides). No commit ID is stored. The verifier's COMMITTED phase checks the record is present and consistent; the verifier itself stays read-only.
- **The baseline record**, `INSTALL_BASELINE_20261031_V1.json`, travels in MHUP-A as an ordinary reviewed member: 40 entries, the 39 variants released on 31 October 2026 (REL-1 at `6a1bed9` and WF-1A at `0d98706`; register v0.23 lines 1183 and 1189) and E_1 revision 2 (E1R2 at `86d12ea`, line 1215) marked `superseded_by: revision 3`; the dates are the days the variants became released, not the earlier dates their non-runnable code was installed. The owner's installation of MHUP-A is his confirmation of the record.
- **The rule:** a catch-up forecast for draw N by a variant is CATCH-UP if the variant's release date (local calendar date) is before N's derived draw date; otherwise it is development evidence. **Validation:** each record carries its own digest; every entry it names must have a registry chain entry, active or superseded, for exactly that (game, method, revision, variant); two records naming the same entry refuse at validation; a variant with no record is ineligible for CATCH-UP (its forecasts are development evidence), never an error.

### 4.4 The order of events for each game (each step is the owner's separate approval)

1. MHUP-A installed and verified (Appendix J). MHUP-B is installed **before Approval 1** (section 8's plan) or after the Mode H score is sealed, never between, because an install changes the closure the study manifest freezes (4.1) and every later Mode H step would refuse. Nothing has read a holdout result.
2. **Approval 1:** freeze the study manifest; write the opening record. Before it, the owner is shown the exposure consequence of 4.2 (EX_125 O03).
3. **Approval 2:** the first results update (`Run_Results_Updater.bat update --games G`; never bare). It adds the holdout and every later draw in one version, `v_a` (finding A3). Before this first run, the updater's offline `--self-test` is run under Python 3.15 (finding A9); the owner reads its output and any `FAIL` or traceback is a STOP that comes to Claude. **No further update until the Mode H score is sealed.**
4. **Approval 3:** the Mode H batch (section 5).
5. **Approval 4:** the Mode H score and report (5.3 to 5.5). The score record's COMPLETE line seals the batch.
6. Then the owner decides whether to declare the system developed (GOAL-1, 6.7), and the first weekly session follows.

### 4.5 The store (R3 6.2; Q2)

R3 6.2 asks the design to compare a combined master holding the holdout outcomes with a separate store releasing one outcome at a time. **Combined master (option A, decided with Q1):** the outcomes sit in the file the reader opens; what keeps them from the methods is the prefix parse (no data column of the target or any later row is decoded, 3.2 rule 4), T-05 (a forecast is byte-identical when later rows change), the B1 rule (whole-file provenance never reaches a method), the frozen study plan, code and environment (4.1), create-only records, the binding gates (3.4), and the freeze-before-outcome rule (5.3) on the scorer's side; these are the guarantees the weekly catch-up relies on anyway. **Separate store (option B):** the outcomes are released one at a time, so the reader can never see a later outcome even in principle; the cost is the staged-release engine in the most protected area and its recovery rules. The reviewer's EX_125 O01 provisionally favours A on these terms.

## 5. Piece 3: Mode H

### 5.1 The batch

The walk-forward driver gains a Mode H batch kind: `Run_Experiment.bat Method_Walk_Forward.py plan --mode H --game G` (Option F for method runs). It:
- refuses unless the opening record and the study manifest are valid and agree, the ledger's last row is exactly `v_a` (4.1), and the closure and environment digests equal the manifest's (R3-T50);
- takes its cohort, targets and environment from the study manifest (no other choice is possible);
- records its batch id, create-only, as `MODE_H_BATCH_ID.json` beside the study manifest, which is what makes a second plan for the game refuse;
- runs each (variant, target) exactly as today, one contract run each, with run mode `REAL_HOLDOUT` and the batch binding (3.4), under roots derived from the project root by batch kind (`roots()` becomes kind-aware, `walk_forward.py` lines 66-70): `results/real/holdout/wf_batches/<GAME>/<batch id>/` and `results/real/holdout/contract_runs/`; the same `wf-<32 hex>` batch-id scheme, so `load_plan` (lines 208-214) changes only its root and accepts the plan's search-log row type `MODE_H_BATCH` (today it requires `WF_BATCH`, lines 220-230); `.gitignore` lines for the new run and attempts folders are package members, as WF-1B's were;
- re-checks the closure, the environment and the ledger at the start of every `run` invocation;
- uses the existing STOP rule unchanged (lines 56-59).

**Vocabulary.** E2R-R41's reserved table (E2R-1 lines 500-503) already fixes `REAL_HOLDOUT / FORECAST -> (WF_FORECAST, HOLDOUT_MODE_H)`. This design unreserves that row as written, and E2R-R44 ("Mode H and FINAL stay shut") is amended by it: the row opens only for a request bound to the game's one plan, with the opening record present. No new product kind. The runner's data-source rule (`contract_runner.py` lines 118-122) treats every real mode as it treats `REAL_DEVELOPMENT`: the project itself, nothing else. **No new code switch:** the new real modes are gated by the owner's create-only records (the opening record here, the developed record in 6.7) and the binding gates of 3.4, rather than by a constant the owner would have to edit; `ENABLE_CONTRACT_REAL_DEVELOPMENT` (lines 114-116) keeps gating development runs only; H-1 5.4's switch list is amended to say so.

Size: 40 variants x 10 targets = 400 runs per game; on the first batches' rate (17,280 runs in about 80 minutes, owner-reported, H-1 7.5) about two minutes per game, estimated; the holdout prefixes are the longest, so the average rate understates slightly.

### 5.2 One batch only, and what "complete" means

One Mode H plan per game (the batch-id record above); a second plan is refused. The driver's resume works as today (lines 264-271, 387-391): a pair not proven DONE is attempted again on the next `run`; completed runs are kept. **A pair is DONE when its attempt's run folder proves the planned run happened and ended in a CONTINUE class** (lines 331-352): a `RUNTIME_FAILURE METHOD_FAILED` is DONE, is scored as missing (R3 3.6, missingness is reported; R3 10.5 status `PREDICTION_FAILED` in the records), and blocks nothing; it is never mistaken for a forecast (EX_125 C04: a DONE-without-forecast record has no forecast digest and is listed as such in the roster). **The batch is COMPLETE when every planned pair is DONE.** The Mode H forecast of a pair is its first DONE attempt bound to the batch (by `frozen_at_utc` then `run_id`). When the Mode H score is COMPLETE the scorer writes the **seal**, `MODE_H_SEALED.json`, create-only beside `MODE_H_BATCH_ID.json`: the score run id and the score record's digest, no values; the dispatch gate reads the seal, never a score record, to refuse further `REAL_HOLDOUT` publication (5.1).

### 5.3 The freeze-before-outcome rule (an always-review subject; EX_125 C05)

One orchestration-only function in the evaluator, `outcome_release_allowed(game, N)`, with fixed evidence paths and no caller-chosen inputs (E2RC2-B01, B02), decides whether the outcome reader may serve target N **to an approved scoring process**; it says nothing about the outcome's existence (under A the updater has already ingested it) and it is not a claim about other programs: the method-facing guarantee is the reader's own (every permitted view excludes its target and all later outcomes, 3.2 rule 4). The rule:
- for a holdout target: only when the game's Mode H batch is COMPLETE (5.2), and the scorer has verified the **exact** roster of the plan (every planned pair, by identity) and chosen each pair's first DONE attempt bound to that plan; a COMPLETE marker of any other batch, or a roster that differs from the plan, refuses;
- for a later target: only when the game's forecast ledger holds the freeze line for N (6.5), naming each record the scorer will read.
Every frozen forecast record is create-only (`os.link`, as today), so nothing can be added or changed after scoring starts. The score attempt records the digests of every record it scores before its first outcome read. N-1 isolation does not make option A prospective evidence; it makes it a precommitted holdout evaluation (section 1).

### 5.4 Scoring once, and the report

- The WF-1B scorer and report are reused in their measures (MR0-MR16), N1 (R = 10,000) and layout, with Part A (descriptive) first; the report's ceiling (`report.py` lines 125-126) is relaxed for a Mode H batch with a valid opening record; the report's fixed texts become tier-aware (today `report_writer.py` lines 422-423 print that no holdout draw is read or scored; the Mode H report states instead that the ten holdout draws were scored once under the primary statement of section 1). The search-log row type is `MODE_H_REPORT`.
- **Families (EX_125 C09):** new Mode H families in the family registry with **mode `WF`** (E2R-R39 and R3 17.3.5 allow `WF` or `IS` only; a Mode H forecast is a walk-forward record) and a new field `evidence_tier: HOLDOUT_MODE_H`, windows equal to the ten targets; fixed in the study manifest before opening. **Mode H is its own family and window and is never pooled with prospective or catch-up evidence**; every report prints the WF meaning (R3 17.3.5A), the tier, the family's M, and the number of draws beside every figure; TOP and WORST side by side; the surprisingly poor shown with the surprisingly good.
- **N1 seed:** reuse the approved root `N1_ROOT_NIST_C2_20261031T1030Z_V1` unchanged. N1's streams are keyed by policy, root, game, replicate and target (`n1_generator.py` lines 48-50), and no earlier report used a target at or after the holdout, so the Mode H targets draw fair draws never generated before; the family plan is frozen before opening (4.1). No new pulse is needed (EX_125 O02).
- **Scored once:** one routine score attempt per game, create-only; a second routine attempt is refused unless the first ended in a STOP before any outcome read. The ratified exception applies here as in the weekly session: a separately identified scoring run beside the first, to correct a scorer fault or add a measure, under its own identity (the three-way split, 2 November 2026); the first score is never edited.
- **The exposure flag:** one flag, naming the record (`HOLDOUT_EXPOSURE_RECORD_v0_3`, item 1), with the decision it rests on (HX-1 for Powerball 1585 and 1586 in Mode H; HX-2 for 1587 and 1588 when the weekly session scores them). It lives in the score records, the ledgers and the reports, not in the frozen forecast (`METHOD_FORECAST_V1` is a closed schema, E2R-R13). Flagged draws are scored and counted in every measure like any other draw; the flag is information only.
- **Words:** the report describes any null result as "no statistically compelling departure from the fair-draw reference under the reported measures", never as proof of randomness; states that ten draws per game give limited statistical power; and labels the study a precommitted holdout evaluation (section 1).
- **No double counting:** the weekly session never re-forecasts or re-scores a Mode H target for a variant whose Mode H pair is DONE (6.3); the league table shows Mode H in its own column.

## 6. Piece 4: the weekly session (MH-1, OFF-1, EFF-1; B02 decided)

### 6.1 Three programs, two launchers, one command

Two rules meet here. **Option F** (H-1 5.4): method code runs only through `Run_Experiment.bat`, which launches files under `src\methods\` (its lines 20 and 38), and there is "no second production launcher". **The import firewall** (Architecture 12.5, MRT-05; `tests/test_wf1b_static.py` lines 34-38 and 60-63): no file under `src/methods/` may import the evaluator or name the outcome reader, and the evaluator imports no method code. A single program that both forecasts and scores would breach the firewall. WF-1B already bent the launcher rule once, with review: the evaluator has its own launcher, `Run_Method_Rankings.bat` (it runs one fixed tool, its line 9). **MH-1's order** (predict N, reveal N, score N, then N+1) and the owner's B02 decision require the two halves to alternate per target.

Design (the bent rule named: H-1 5.4's launcher sentence is amended to name the evaluator launchers and the session wrapper):
- `Run_Evaluation.bat <file> <args>`: a general evaluator launcher mirroring `Run_Experiment.bat` for files under `src\evaluation\` (venv checks, `SETLOCAL`, `SAFE_ARG`, `%*`); `Run_Method_Rankings.bat` stays. It launches `Method_Mode_H.py` (4.1, 4.2, 6.7) and `Method_Weekly_Score.py`.
- `Method_Weekly_Forecast.py` under `src/methods/`, run through `Run_Experiment.bat`: the forecasting half. It never imports the evaluator. Its commands: `status`, `open-session`, `next` (one unit of work, 6.3).
- `Method_Weekly_Score.py` under `src/evaluation/`: the scoring half (`score --target N`) and the witness commands `witness` and `verify` (6.5). It imports the outcome reader, so `test_wf1b_static.py` line 63 (only `report.py` may) gains it. `Method_Mode_H.py`, also under `src/evaluation/`, writes the two owner records into `source_data/` (4.2, 6.7), so `test_wf1b_static.py` line 60 (no evaluator file but the outcome reader names `source_data`) gains it too (Appendix L).
- `src/Weekly_Session_Orchestrator.py`: a small sequencer beside the coordinator at the `src/` root that imports neither `methods` nor `evaluation` (a static test says so). **What it is under Architecture 5C:** not a coordinator. It refuses to start unless `VIRTUAL_ENV` and `sys.prefix` are the project `.venv` (5C.1, as the coordinator does); it launches each half through its launcher with `subprocess.Popen(..., cwd=ROOT, shell=False, stdin=DEVNULL)` and blocks on `wait()` with no timeout; it never terminates, polls, inspects or looks up any process, uses no PID, no psutil and no timer, and writes no orphan evidence; on a child's non-zero exit it stops and prints the child's output; a hung child is visible to the owner, who closes the console; nothing is killed and nothing is reported as `UNVERIFIED` (that is coordinator vocabulary). It learns the session id and the target from each child's exit code and one machine-readable last line, used for sequencing only; the evidence is the records. The precedent for `Run_Experiment.bat` as the child of a Python parent is the coordinator itself (`Powerball_Experiment_Coordinator.py` lines 35, 793 and 943-945) and the synthetic lifecycle module; both so far launched only POC and synthetic runs, so this is the first production contract run launched from a Python parent, which the Windows rehearsal (T017) must show. Arguments to `.bat` children pass through `SAFE_ARG` rules (H-1 section 6; a `--session <32 hex>` and `--target <integer>` are SAFE_ARG-clean). Architecture 5C.1's list of launch interfaces is amended by ratification to name it (Appendix K).
- `Run_Weekly_Session.bat --game G`: the one command the owner types (MH-1), a wrapper with the standard venv checks that runs the orchestrator.
- The Claude Code rulebook's rule 7 and the owner's `.claude/settings.json` deny patterns gain all of these (the runner never runs them).

**The session record and the session lock (EX_125 B01; cold read P3):** `open-session` writes, create-only, `results/real/weekly/<GAME>/sessions/SESSION_<32 hex>.json`: the game, the start time, the master version and SHA-256 pinned (the ledger's last row), the environment digest, the developed record's digest, and the active roster (every released, unretired variant with its revision and release date). Every weekly run binds to it and must pin the same master version (3.4). A session is never edited; records of earlier sessions stay bound to theirs. `open-session` also takes the game's **session lock**, `ACTIVE_SESSION.lock`, create-only, holding the session id; it refuses while a lock exists. The orchestrator removes the lock at a clean end. After an interruption (Ctrl+C, a closed console, a crash) the lock stays, because Windows does not end a child when its parent dies (H-1 section 6) and the forecasting half may still be running; the checklist's procedure is: confirm with `Get-Process python` that no project process is running, then delete the lock by hand; no AI chat or runner ever clears it. With the first-attempt rule (3.4(c)) a stray second record from such a case is listed and never scored.

**In order, each week:**
1. **The results update**, the owner's updater, run by the owner first (`Run_Results_Updater.bat update --games POWERBALL,OZLOTTO`); the only step that needs the internet. The updater and the forecasting and scoring code stay separate programs (MH-1).
2. `Run_Weekly_Session.bat --game OZLOTTO`, then `--game POWERBALL`; each refuses unless the game's developed record exists (6.7).
3. The owner copies `source_data/` and `results/` to the backup drive (section 7's checklist); optionally pushes the ledgers and records the witness (6.5).

### 6.2 The status block

The forecasting half's `status` prints, per game: the last accepted draw (from the master); per variant, summarised, the last draw with a bound DONE record and the last scored draw; the backlog (outstanding draws), each with its R3 10.5 status `OUTCOME_AVAILABLE` or `OUTCOME_PENDING`; the next target, its derived date and its deadline; the number of active variants; the effective class each outstanding target's records will receive (Appendix I); and any unbound real-mode records found under the weekly root. If an expected result is not yet in the master, it says so and does nothing for that target.

### 6.3 One target at a time, in MH-1's order (EX_125 B02)

The scope for a game is every draw from `holdout_last + 1` onward. The holdout draws themselves are Mode H's: the released cohort has its Mode H records for them, and a method released later never forecasts them in the weekly session (they are training history for it; if the owner ever wants a later method's forecasts on the holdout draws, that is a development batch under a separately reviewed extension, not in scope). A target N is **closed** for a variant when it has a score record; N is closed for the game when it is closed for every active variant. **MH-1 as read here:** MH-1 lists the catch-up, then the scoring of the open prospective forecast, then the next freeze; an open forecast whose result has arrived is the lowest unclosed draw with a result, so in strict draw order it is scored first; the order below is that reading, which is also what EX_125 B02 asks for. The orchestrator loops over the forecasting half's `next` and the scoring half's `score`, and the forecasting half **enforces the order itself**, so a faulty orchestrator cannot skip a step. `next --game G --session S` finds the lowest target N that is not closed and whose result is accepted, then does one of three things:

- **N has a freeze line already** (an open forecast whose result has arrived; or a resume after a crash between freezing and scoring): it exits `FROZE N` at once and runs nothing.
- **N has no freeze line and some active variant has no bound DONE record for N:** for each such variant it runs one contract run in the mode of 6.4 (a failed run is DONE with `PREDICTION_FAILED` and is not run again); then, when every active variant has a bound DONE record, it appends N's freeze line (6.5), naming for each variant **one** record, the first bound DONE attempt by `frozen_at_utc` then `run_id` (any other bound record for the pair is listed as a later attempt), and exits `FROZE N`.
- **No such N exists:** see the next-draw cases below.

It never looks at N + 1 while an unclosed N with an accepted result exists.
- The orchestrator then runs `score --game G --session S --target N`: the scoring half verifies the freeze line names every record it reads, scores every record of N that has no score line yet (6.6), and exits. Then the orchestrator calls `next` again.
- When no accepted draw is left unclosed, `next` either freezes the next draw's `FINAL_NEXT_DRAW` set (6.4) and exits `FROZE_NEXT N` (the orchestrator stops: the session is complete, with the forecast open), or exits `WAIT N` (N's result not accepted; status `OUTCOME_PENDING`) or `NONE` (the deadline rule forbids a forecast now); the orchestrator stops and prints the status block. If the master has grown since the session opened, every run refuses (3.4(b)) and `next` exits `STALE`; the orchestrator stops and the owner starts a new session.

Every step is persisted in create-only records before the next begins (the run records, the freeze line, the score lines), so a crash anywhere resumes by rerunning the command: `next` re-derives the state from the records and continues at the same N; nothing accepted is rewritten; nothing is scored twice (a score line is create-only, keyed by the full identity of 6.6). Appendix F is the event-order diagram.

### 6.4 Run modes, the deadline and the labels (Q3, Q4, Q5)

The forecasting half decides each run's mode by a fixed rule before the run, so the contract vocabulary stays a pure table (E2R-R41), and the gates of 3.4 check the result:
- N's result is accepted and the variant's release date (4.3) is before N's draw date: run mode **`CATCH_UP`** (a new run mode), producible row `CATCH_UP / FORECAST -> (WF_FORECAST, CATCH_UP)` (a new evidence tier); an E2R-1 (9.1, E2R-R41) and R3 17.3.9 amendment, recorded in the register. A new mode is needed because E2R-R41 fixes the tier per run mode and MH-1 wants the labels kept apart in records;
- N's result is accepted and the release date is not before N's draw date: run mode `REAL_DEVELOPMENT`, tier `DEVELOPMENT_WF_EXPLORATORY` (MH-1: "ordinary walk-forward development evidence"), bound to the session, target above `holdout_last` (3.4); these runs go to the development run root;
- N = last accepted draw + 1 (the gate of 3.4(a) allows `FINAL_NEXT_DRAW` for no other target) and at least one hour remains before N's deadline **when the set starts**: run mode `FINAL_NEXT_DRAW`, E2R-R41's reserved row `(WF_FORECAST, PROSPECTIVE)` unreserved as written (E2R-R44 amended; the row opens for a request bound to a session, with the developed record); the forecast is left open. The hour rule is judged once, at the start of the set; a set interrupted and resumed with less than an hour left stays partial until N's result is accepted, after which the missing variants get `CATCH_UP` records and the freeze line marks them `MISSING_BATCH`;
- N = last accepted draw + 1 and less than one hour remains, or the deadline has passed: the forecasting half refuses to forecast (`NONE`) and the status block says the draw will be caught up once its result is accepted (the owner's accepted position: a missed deadline costs that week's pre-draw standing, nothing else).
Exposure: Powerball 1587 and 1588 carry the exposure flag (5.4) in their score records and in the ledger whatever their label. Run root for `CATCH_UP` and `FINAL_NEXT_DRAW`: `results/real/weekly/contract_runs/`; its `.gitignore` lines (the run folders and the session attempts ledger) are MHUP-B members; the forecast, witness and score ledgers and the session records are tracked, so a push of them is a witness.

**The deadline (Q4):** 00:00 local time on the draw's date, computed from the PC's clock and time zone (no new dependency), recorded with every record as the UTC instant and the local offset; the local clock is not an independent witness (6.5). Alternative, for the owner: a fixed UTC instant (12:00 UTC on the day before), independent of the PC's time zone setting.

**Effective class (EX_125 B05; the total rule is Appendix I):** a record's tier is immutable (fixed by its run mode). Its **effective class**, used by every report, league table and N1 input, is derived per record: a `FINAL_NEXT_DRAW` record whose own publication receipt time (`frozen_at_utc`) is before N's deadline is `PROSPECTIVE`; one frozen after the deadline (possible only when a run started before 23:00 is still running at midnight) is **`LATE_PRE_DRAW`**, a named operational category shown in the operational portfolio view, scored and kept, never counted as prospective or catch-up evidence and never excluded from the portfolio count; it is never re-forecast (N closes when scored). A straddling set therefore classifies record by record; the freeze line summarises (`deadline_met` true only if every `FINAL_NEXT_DRAW` record of the line is before the deadline). `MISSING_BATCH` (R3 10.5) is recorded on N's freeze line for exactly those variants that were active and released before N's draw date yet have no `FINAL_NEXT_DRAW` record for N (a scheduled prospective freeze was missed); a method's back-history before its release is never `MISSING_BATCH` (EX_125 C08). **In plain words, one invented week:** Oz Lotto 1712 is next; the session starts at 22:30 on the Monday, with the hour rule met; 38 variants freeze by 23:40 and are PROSPECTIVE; one variant's run is slow and freezes at 00:05 on the Tuesday, so its record is `LATE_PRE_DRAW`, kept and shown but not counted as prospective; one variant failed, so its record is `PREDICTION_FAILED` and counts as missing. Had the owner started the session on Tuesday morning instead, no set would start, and after the draw all 40 would be CATCH-UP with `MISSING_BATCH` on the line.

**Invariant (a postcondition of a completed session):** at most one open forecast per active variant per game; exactly one when the session ended `FROZE_NEXT`; a newly released revision has none until the session has caught it up; a retired one has none ever again.

### 6.5 The forecast ledger and the witness ledger: the timing proof (OFF-1; EX_125 B03)

- A local, create-only, digest-chained **forecast ledger** per game, `results/real/weekly/<GAME>/FORECAST_LEDGER_V1.jsonl`. When every active variant has a DONE record for target N, the forecasting half appends one **freeze line**: the target and its derived date, the session id, the freeze time (UTC and local offset), the deadline and `deadline_met`, the roster with every record's full identity (6.6) and digest, each record's run mode and `frozen_at_utc`, each failed variant marked `PREDICTION_FAILED`, each `MISSING_BATCH` variant, every registered but non-runnable method by status (R3 10.3), the environment digest, the master version and SHA-256 pinned, and the previous line's digest. A line is appended only after every record it names is DONE; the freeze-before-outcome rule (5.3) reads this line. **The line carries no witness or publication status.**
- **What the chain proves:** that the records agree with each other; comparing it with an earlier trusted digest, kept separately, reveals later changes; by itself it proves neither when the records were made nor that the whole chain was never replaced.
- **The witness ledger** (append-only, `WITNESS_LEDGER_V1.jsonl`), the **witness evidence and verification history** (B03), with two kinds of line, both written by `Method_Weekly_Score.py`:
  - `WITNESS_RECORDED`: the owner, after pushing the ledgers or emailing a line's digest, records `--target N --kind github|email --ref <commit id or message id>`; the line holds the freeze line's digest, the kind, the reference, and the time recorded. It is the owner's claim, not proof.
  - `WITNESS_VERIFIED`: a person (the owner, the reviewer, or anyone named) who has checked the reference records `--target N --verified-by <name> --received-utc <instant> --how <one line>`: that the reference exists, carries exactly that freeze-line digest, and was received at the stated instant by the outside service (GitHub's own record of when the push arrived, not the commit's author time, which is a local clock; the email's received header); the `--how` line names the source read. The verification is a human act outside the repository; the line records who, how and when.
  - **Publication status is derived at report time, never stored in a score line or a frozen record:** `PUBLISHED_BEFORE_DRAW` when a `WITNESS_VERIFIED` line exists whose received instant is before N's deadline; otherwise `TIMELINESS_UNVERIFIED` (with "witness recorded, not verified" or "no witness" shown). A later verification changes the next report, never an accepted score: no rescoring, no edit (the three-way split holds). A witness line for an unknown freeze digest, or a `WITNESS_VERIFIED` line whose received instant is after the deadline, is kept and shown and never promotes the status. No routine run touches the network.
- **R3 10.5's statuses, where each lives:** `OUTCOME_PENDING` / `OUTCOME_AVAILABLE` in the status block; `MISSING_BATCH` and `PREDICTION_FAILED` in freeze lines (6.4, 6.3); `PUBLISHED_BEFORE_DRAW` / `TIMELINESS_UNVERIFIED` derived at report time from the witness ledger. Appendix G is the witness lifecycle.
- **Tests (R3-D20's "must be tested"):** a ledger line edited, removed or reordered breaks the chain; the forecasting half refuses to freeze a `FINAL_NEXT_DRAW` set after its deadline, and within the hour before it; the scoring half refuses a target with no freeze line; a straddling set is classified record by record; a witness line for an unknown digest is refused; a verification received after the deadline does not promote; a verification added after the score changes the next report and no score byte.
- **R3 clauses superseded for this project, on ratification:** 1.3 ("freeze and push the full batch remotely before the actual target event"); 1.5's "externally verifiable pre-draw proof" (made optional); 10.1(6) ("pushed to the declared remote"); 10.2's "COMMIT AND PUSH TO REMOTE BEFORE DRAW" and "SAVE REMOTE REVISION/PUSH EVIDENCE" steps and its paragraph after the diagram ("archive remote ref/commit IDs"); 11.5 item 4's "remote publication evidence"; 17.3.9's `PROSPECTIVE` definition ("frozen and published before their draws" becomes "frozen before their deadline and recorded in the local forecast ledger; publication status derived separately from the witness ledger"); and R3-D20's "GitHub push evidence required". R3 10.5's statuses and E2R-R40C's "labelled unverified and counted" are applied as written (Appendix K).

### 6.6 Scores and the league table (EFF-1; EX_125 C04, C09)

- A local, append-only **score ledger** per game, `SCORE_LEDGER_V1.jsonl`: one line per scored record, keyed by the **full identity** `(game, method, method revision, variant, target, run_id of the scored attempt, score run id, scorer version)`; the line holds the per-target quantities WF-1B already computes (TOP and WORST matches, Powerball match, prize division, rank positions), the scored record's digest (or the failure record's), the forecast's training pin and the outcome's pin (the master version and SHA-256 that supplied it: R3 11.5's **outcome record**, which answers finding A11), the tier, `frozen_at_utc`, the effective class (Appendix I), any exposure flag. Report grouping keys are (game, method, revision, variant) and the effective class; the record keys above are immutable. This ledger is R3 11.5 item 6, the **evaluation record**. The scoring code reuses WF-1B's measure functions through a thin per-target driver; no measure, label or formula changes. Each method revision is reported separately (R3 6.3).
- The weekly path reads only the new runs and the new draw. The league table is built from the score ledger, cumulative, with PROSPECTIVE, CATCH-UP and development evidence in separate columns, `LATE_PRE_DRAW` in the operational portfolio view only, the number of draws and the exposure period beside every figure, and Mode H and the development reports referenced in their own columns; nothing is retuned because of its ranking (MH-1). N1 and the significance tables run over the PROSPECTIVE and CATCH-UP records only, with their own family definitions, counts and multiple-comparison allowance, in the full report; cohorts of different exposure are compared on matched draws.
- **Cadence (Q6):** each session prints a short after-draw note and writes the dated cumulative table, with a search-log row of type `WEEKLY_TABLE` (C09: every dated table is logged); the full report with N1 on request or monthly, each a new dated report with its own search-log row of type `WEEKLY_REPORT`; earlier reports stay as published.
- **Retired revisions:** their forecasts and scores stay where they are; the league table shows "as published" and "current methods" side by side (D-8); a retired index is a later small item (roadmap 21b), not part of this design.

### 6.7 FINAL and "developed" (Q8; EX_125 O02)

The weekly session **is** R3's FINAL_NEXT_DRAW protocol (R3 1.3 and 10) as amended by 6.5, and the owner's GOAL-1 declaration that the system is developed **is** R3's "explicit FINAL opening". The declaration is a create-only owner record, `source_data/DEVELOPED_<GAME>.json`, written by `Run_Evaluation.bat Method_Mode_H.py declare-developed --game G`, which refuses unless the game's Mode H score record is sealed, prints R3 10.1's precondition list with the evidence for each (ratified scoring formulas; frozen released variants; the full roster listed; refreshed and digested sources; L identified from the master; the ledgers in place; the R3 supersession of 6.5 ratified), and records the owner's typed statement and the Mode H score record's digest; the gates (3.4) check those fields, so an arbitrary file is not a declaration. The weekly session and the `CATCH_UP` and `FINAL_NEXT_DRAW` modes refuse without it.

## 7. Piece 5: the results update procedure (findings A6, A7, A8) and the owner's checklist

The updater's code is not changed by this design. MHUP-B carries a one-page owner checklist:
- **Normal week:** run the updater with its arguments; read its summary (draws checked, added, warnings); run the weekly session for each game; copy `source_data/` and `results/` to the second drive; once a month, restore one backup copy to a scratch folder and compare it (the restore test); optionally push the ledgers and record the witness (6.5). Backups cover the git-ignored run, attempts and score records, which exist nowhere else.
- **A6 (single source; OWNER-DECIDED 3 November 2026, C03):** production uses Lotterywest's results-search page only (TSC-1 retires the two-site checker), and **the owner has decided that Lotterywest's published results are official and trusted as they stand, so no second-source check of a new draw is required in production.** What the updater's checks prove: that the fetched page agrees with every draw already held, that the new draws are consecutive and correctly dated, and (by the chain check) that the master and its ledger agree; what they do not prove: that a newly appended draw matches any second source. This decision supersedes, for production, R2-C03's "independent evidence" and the proposal's candidate-then-promotion step; register v0.24 records it (Appendix K). The owner's private, by-hand check of The Lott stays his own and is never automated.
- **A7 (an interrupted update; EX_125 C02):** the updater's own message is "does not match the last ledger entry" (line 299); every other tool refuses with its chain error. Recovery is an **owner-run, reviewed procedure in MHUP-B's checklist**, never a test on real files, with these checks before anything is copied: (1) the newest file in `source_data/backups/` has the SHA-256 the last ledger row records as `master_sha256` (it is that row's master); (2) the current master's SHA-256 matches no row and its parsed last draw is above the ledger's (the update stopped between the replace and the append, and nowhere else); (3) no scientific tool has run since the update started (the status block and the session records show no later run); (4) the owner states the action in the checklist's line. Then copy the backup over the master and rerun the update, which refetches and re-adds. If any check fails, stop and send the output. **A stale lock** (`source_data/.results_master.lock`, lines 653-672) is the updater's own lock, not the coordinator's orphan marker: delete it only after `Get-Process python` shows no updater process and the lock's timestamp predates it. **A grab from a refused or interrupted run** stays in `source_data/grabs/` as evidence; it is never deleted and never used. Nothing else is ever edited by hand.
- **A8 (the update window):** the default window (this month plus five back) overlaps the master while sessions run weekly; after a long break the checklist says to use `--months-back` to reach the master's last draw (the updater refuses without an overlap, lines 616-617).

## 8. Packages and schedule (Q9)

**Two code packages**, so Mode H is never held up by the weekly work:
- **MHUP-A** (HIGH): sections 2 (E_1 revision 3 under the extended ER-2r1, Appendix J), 3 (the version-2 rules, every file in the table, one data kind, the binding gates and the barrier), 4 (the study manifest with its closure, the opening and declare commands under `Method_Mode_H.py`; the install-record tool and the baseline record; the `.gitignore` lines) and 5 (the Mode H batch kind, binding and roots, the freeze rule, the Mode H families, the report's ceiling and texts); `Run_Evaluation.bat`; the `REAL_HOLDOUT` row unreserved; the rulebook and deny-pattern additions for MHUP-A's tools (`Run_Evaluation.bat`, `Method_Mode_H.py`); MHUP-B adds its own.
- **MHUP-B** (HIGH): section 6 (the `CATCH_UP` mode and tier, `FINAL_NEXT_DRAW` unreserved, `Method_Weekly_Forecast.py`, `Method_Weekly_Score.py`, the orchestrator, `Run_Weekly_Session.bat`, the session records, the three ledgers, the deadline, `LATE_PRE_DRAW`, the league table, its `.gitignore` lines) and section 7's checklist.

**The plan (the owner's planning target of 2 November 2026; not a deadline; FB-1 is the protection):**

| When (Adelaide) | What | Who |
|---|---|---|
| Tue 3 Nov | v0.1r2 to the reviewer as EX_126 | You relay; the reviewer rechecks |
| Wed 4 - Thu 5 Nov | Any further round; your ratification of the design and answers to Q2-Q4, Q6-Q9 | Claude; you |
| Thu 5 - Mon 9 Nov | MHUP-A code (including E_1 revision 3 and the barrier), tests, mutation checks, rehearsals; code review; Claude Code rehearsal (T016); install | Claude; the reviewer; you |
| Tue 10 - Fri 13 Nov | MHUP-B the same (T017); installed before Approval 1 | Claude; the reviewer; you |
| Fri 13 - Sun 15 Nov | Approvals 1-4 per game; Mode H run and scored; your GOAL-1 decision | You |
| Sun 15 - Mon 16 Nov | First session, both games: catch-up of Oz Lotto 1704-1708 and Powerball 1587-1591; Oz Lotto 1709 frozen before 00:00 Tue 17 Nov (the set must start by 23:00 Mon) | You |
| Tue 17 - Wed 18 Nov | Powerball 1592 frozen before 00:00 Thu 19 Nov (the set must start by 23:00 Wed) | You |

Each review round that needs a recheck costs about half a day (estimated); the snapshot took four rounds. E_1 revision 3 and the barrier add about half a day to MHUP-A; the orchestrator adds about a day to MHUP-B (estimated). If the plan slips, the first prospective forecasts move a week and the catch-up covers the draws in between (FB-1). I will say so the day it happens.

## 9. Decisions, and the owner's questions Q1 to Q11

| Q | The question | Status and where |
|---|---|---|
| Q1 | What does "frozen before the holdout is opened" mean: A, B or C? | **OWNER-DECIDED 3 Nov 2026: A**, as an input; the design is ratified after this recheck (section 1) |
| Q2 | Combined master, or a separate release store? | Combined, following Q1 (4.5) |
| Q3 | Which run modes and tiers label the weekly runs? | RECOMMENDED `CATCH_UP` (new), `REAL_DEVELOPMENT`, `FINAL_NEXT_DRAW` by rule, bound to a session (6.4) |
| Q4 | The deadline for a prospective forecast | RECOMMENDED 00:00 local on the draw date, with an hour's margin (6.4); the alternative stated |
| Q5 | How "installed before that draw" is proved | DECIDED mechanism (owner, 2 Nov); format, validation and rule RECOMMENDED (4.3) |
| Q6 | The report cadence | RECOMMENDED weekly table, logged; full report on request or monthly (6.6) |
| Q7 | The display rule for holdout draws after opening | OPEN; see below |
| Q8 | Is the weekly session R3's FINAL, and "developed" its opening? | RECOMMENDED yes, with the checked developed record (6.7) |
| Q9 | One package or two? | RECOMMENDED two (8) |
| Q10 | Extend ER-2r1 to E_1 revision 3? | **OWNER-DECIDED 3 Nov 2026: yes**, with Appendix J's safeguards (2) |
| Q11 | May a hand-made bound request be admitted (harmless under the first-attempt rule), or must every real-mode run come from the driver or the forecasting half? | RECOMMENDED admit (3.4); the alternative needs a new mechanism |

- **DECIDED** (owner): MH-1, OFF-1, EFF-1, HX-1, HX-2, FB-1, GOAL-1, ORD-1, TSC-1 (register v0.23); on 2 November 2026: the three-way split; archive-and-index for a retired revision; the three labels; the status block; at most one open forecast per active variant per game, nothing scored twice, an unaccepted draw left open; Q5's mechanism; the planning target; on 3 November 2026: Q1 = A; Q10 = ER-2r1 extended; B02 = MH-1's per-target order implemented exactly; C03 = Lotterywest trusted, no second-source check in production.
- **RECOMMENDED** (for the owner, after this recheck): the primary statement and the register amendments (below); the version-2 rules, one data kind and the gates (3); the install-record format and rule (4.3); the `.gitignore` lines (4.2, 6.4); the N1 seed reuse (5.4); the programs and launchers (6.1); Q3, Q4 and `LATE_PRE_DRAW` (6.4); the witness ledger (6.5); Q6 (6.6); Q8 (6.7); Q9 (8); Q11 (3.4); the A7 recovery procedure (7).
- **OPEN, for the owner:** **Q7, the display rule after opening:** today nobody may display or compute with Powerball 1577 or later or Oz Lotto 1694 or later. After a game's holdout is opened and Mode H scored, those draws are ordinary history for training and scoring, and the masters in every clone contain them (4.2). RECOMMENDED, and the reviewer leans the same way (O03): keep the restriction on raw draw values in the AI chats after Mode H: "no lottery-results searches, no results websites, no opening of `source_data`, `results` or `transitory_data` by any chat or runner, and no draw outcome pasted into the chats except inside report text the owner chooses to share"; the documents to amend are the Claude Code rulebook (rules 4 and 5), H-1 section 5.1, H-2 section 5 and the holdout exposure record; until the owner decides, the rule stays exactly as it is.
- **Register amendments this design asks for, on ratification (Appendix K has the full retained/superseded list):** register v0.23's "all frozen before the holdout is opened" (section 1); E2R-R52's run-time ceiling and R3 6's "development caps remain" (3.2 rule 3); E2R-R44's "Mode H and FINAL stay shut" (5.1, 6.4); E2R-1 9.1 and E2R-R41 and R3 17.3.9 for `CATCH_UP`, and the operational category `LATE_PRE_DRAW` (6.4); the R3 clauses of 6.5; R2-C03 and the proposal's candidate-then-promotion step, for production (7, C03); H-1 5.4's switch list (5.1) and launcher sentence (6.1); H-1 7.3 for E_1 revision 3 (2); ER-2r1 extended (Q10); the Claude Code rulebook rule 7 and the owner's deny patterns for the new tools (6.1); Architecture 5C.1's list of launch interfaces, to name the orchestrator as a sequencer that is not a coordinator (6.1); the option C reason (section 1).
- **Not in scope:** result corrections (R3 10.3); WF-1C; a cross-batch report reusing frozen records and the retired index (roadmap 21b); Method A's diagnostics; any change to the updater or the two-site checker; the coordinated path; the method-registry presentation.

## 10. Not tested, and what the code round must show

Nothing here is implemented or tested. Appendix L lists the oracles and the existing tests that change. In one paragraph: the chain grammar, prefix, interrupted-update, one-data-kind and gate tests (3); T-05 on a grown synthetic master; E_1 revision 3's label-for-label identity with the revision 2 reference fixture (2); the install-record tool, the baseline record's validation and the duplicate refusal (4.3); the closure and environment digest refusals (4.1); the Mode H batch refusing without a valid opening record, with a mismatched study manifest, with a changed closure, with an extra ledger row, and a second time; the freeze-before-outcome function refusing before the batch is COMPLETE, for a roster that differs from the plan, and before a freeze line exists; the scorer refusing a second routine attempt; the forecasting half's ordering (never past an unclosed N; every variant DONE for N before N's freeze line), its refusal within the hour before and after the deadline, its record-by-record classification of a straddling set, its handling of a failed variant and of an unaccepted result, `MISSING_BATCH` only for eligible variants, and its ignoring of unbound records; the scoring half's double-scoring guard, its roster verification and its refusal without a freeze line; the orchestrator's resume after a crash between freezing and scoring, its static import test and its no-kill property; the ledger chain and witness tests; the launchers' venv checks; mutation checks for each rule; LF and CRLF rehearsals; Claude Code rehearsals on Windows (T016, T017). All tests on invented data; none reads a holdout result; no destructive test without the owner's separate approval.

## Appendix A. The reviewer's cautions, and where each lands

| Caution (takeover notes; Response 2; direction check; EX_125 optional) | Where |
|---|---|
| Flagged holdout draws stay valid and counted | 5.4 |
| Holdout outcomes inaccessible until the reviewed, owner-authorised procedure, which then permits scoring | 4.2, 4.4, 5.3 |
| "No statistically compelling departure", never proof of randomness | 5.4 |
| Steps must not score the same target twice; N known to the scorer, not to the method forecasting N | 6.3, 6.6; 3.2 rule 4 |
| "Find the last forecast" safe for a new revision, a retired one, missing results, a partial session | 6.3 derives state from bound records and ledgers; 6.4 invariant |
| "Exactly one open forecast" is an aspiration, not yet demonstrated | 6.4 states it as a postcondition; Appendix L tests it |
| A catch-up forecast is not pre-draw, however strict its isolation; labels apart; Q5 conditional | 6.4; 4.3; Appendix I |
| Re-scoring means a new dated report, not an edit; scores re-verified under a new identity | 5.4, 6.3, 6.6 |
| Retirement: index, not move; both report views | 6.6; roadmap 21b |
| Mode H under A is a precommitted holdout evaluation, not pre-draw forecasting | 1, 4.5, 5.3 |
| Option C's definedness for target-dependent variants | 1 (corrected reason) |
| Mode H's second pass over the same draws would double count | 5.4, 6.3 |
| The chain's evidential limits; the witness must verifiably receive the digest before the draw | 6.5, Appendix G |
| Operator status block | 6.2 |
| Backups need a restore test; GitHub is not a backup of git-ignored records | 6.1, 7 |
| Method registry versus ratification register | 9, not in scope |
| Q5's install-date rule versus the promised catch-up labels | 4.3, 0, 2 |
| Keep the raw-value restriction in the chats after Mode H (O03) | 9, Q7 |
| Do not let an arbitrary JSON file act as the developed approval (O02) | 6.7 |

## Appendix B. Resolution of EX_125 (the B/C/O table)

| Finding | Resolution | Changed paragraphs | Tests |
|---|---|---|---|
| B01 real-mode requests bypass authorisation | **Applied.** Structure, publication admission and scoring rights separated; every real-mode run carries a binding to the game's one Mode H plan or to a session record, resolved by the dispatch gate at fixed roots from value-free records; unbound requests refuse before anything is read; `REAL_DEVELOPMENT` above the prefix only above `holdout_last`; a sealed batch (the seal marker) refuses further publication; the pin and release-date gates; the first-attempt designation; the session lock; the opening record starts the sequence and authorises no run; the hand-made bound path is put to the owner as Q11 | 3.4, 4.2, 5.1, 5.3, 6.1 session record, Appendix E | Appendix L: every gate once per rule; unbound, forged digest, sealed batch, pre-plan `REAL_HOLDOUT`, `REAL_DEVELOPMENT` on a holdout target, orphan and barrier states |
| B02 catch-up order is not MH-1's | **Applied (owner decision B02).** One target at a time: `next` freezes N, `score` scores N, then N+1; the forecasting half enforces the order itself; an open forecast with a result is handled first; never past an unaccepted draw; resume per persisted step; an orchestrator alternates the two halves inside the one command | 6.1, 6.3, Appendix F | Two and four missed draws; crash between freeze and score; a failed method; independent game backlogs; the event order asserted |
| B03 witness status unstable | **Applied.** Facts (records, freeze lines, score lines) kept apart from the append-only witness ledger with `WITNESS_RECORDED` and `WITNESS_VERIFIED` lines; publication status derived at report time, never stored; an owner-entered reference never promotes by itself; late verification changes the next report, no rescoring; no network in routine runs | 6.5, 6.6, Appendix G | Score first, verify later, new report, zero score bytes changed; unknown digest; wrong digest; received after the deadline |
| B04 study freeze incomplete | **Applied.** Closure = every file under `src/` plus the root launchers, `requirements.txt` and the dependency installer, with stated exclusions; environment list; `v_f` and the one-update rule; re-check at every Mode H step; fail closed on any difference; the updater itself unchanged, the scientific tools refuse | 4.1, 4.4, 5.1, Appendix H | Mutate each category; add an unseen file; change a package version; append a ledger row between approvals |
| B05 straddling FINAL set has no tier | **Applied.** Total per-record rule: tier immutable; effective class derived from `frozen_at_utc` versus the deadline, the outcome timing and the install evidence; `LATE_PRE_DRAW` named, scored, kept, shown in the portfolio only, never re-forecast; one definition for the note, the score ledger, the tables and N1 | 6.4, 6.6, Appendix I | All variants before the deadline; one after; restart midway; result pending; result later; a genuine after-draw catch-up |
| C01 E_1 one-package safety argument | **Applied.** Ordered install with a package-wide barrier honoured by the new dispatch gate, E_1's own flag, what refuses at each interim step, STOP states, negative tests; the fixture oracle, both games, real and synthetic kinds, each new mode on the same prefix; the legacy 1577 record unscored | 2, Appendix J | Appendix J's negatives; Appendix L |
| C02 ledger grammar, pins, recovery | **Applied.** Closed grammar for every column and row kind; cross-row consistency distinguished from the prefix hash link; two pins per scored forecast; recovery as an owner-run reviewed procedure with four checks; the updater's lock distinguished from the orphan marker; no tests on real files | 3.2, 7 | Appendix L: every grammar rule broken once |
| C03 Lotterywest cross-checks are not independent corroboration | **Applied (owner decision C03).** What the checks prove and do not prove stated; the owner's decision to trust Lotterywest as official recorded as a supersession for production, to be recorded in register v0.24 | 7, Appendix K | none (a decision) |
| C04 full identity in records | **Applied.** Score lines keyed by (game, method, revision, variant, target, run_id, score run id, scorer version); failure records distinguished; each revision reported separately; the primary statement reads "all planned attempts and every successfully published forecast" | 1, 5.2, 6.6 | Appendix L |
| C05 meaning of the outcome gate under A | **Applied.** The gate governs approved scoring reads only; the method-facing guarantee is the reader's; the scorer verifies the exact plan roster and first DONE attempts; "N-1 isolation does not make A prospective" | 5.3, 1 | Roster-mismatch refusal |
| C06 one view kind: compatibility boundary | **Applied.** Inputs and ranked outputs equal; request and record metadata differ; E_1 revision 3 takes the view kind, not the run mode | 3.3, 2 | Rankings, tie-group order, digests, first and last targets per mode |
| C07 line numbers | **Rebutted with evidence, and made robust.** Every citation was re-verified against the Git objects at `3a9f6ac` (`git show 3a9f6ac:<path>`); the numbers stand. Appendix D anchors each citation to its blob id and quotes the line's text, so any view can verify | Appendix D | none |
| C08 `MISSING_BATCH` scope | **Applied.** Only for variants active and released before N's draw date with no `FINAL_NEXT_DRAW` record for N; back-history is development evidence; the four statuses' homes stated | 6.4, 6.5 | Appendix L |
| C09 reporting and search log | **Applied.** Every dated table logged (`WEEKLY_TABLE`); Mode H its own family, never pooled; counts, exposure and matched-draw comparison; TOP and WORST side by side; poor results shown | 5.4, 6.6 | Appendix L |
| O01 Q1/Q2 | **Noted.** The owner decided A on 3 November 2026 after this advice; B kept described truthfully | 1, 4.5 | |
| O02 Q3-Q6, Q8-Q10 | **Applied where it adds a rule:** the developed record is checked and preconditioned (6.7); the deadline records UTC and offset and the clock is no witness (6.4); release dates, not code-arrival dates (4.3); no new pulse (5.4) | 4.3, 5.4, 6.4, 6.7 | |
| O03 Q7 | **Noted.** The exposure consequence is shown before Approval 2; the recommendation now matches the reviewer's lean: keep the raw-value restriction in the chats | 4.2, 4.4, 9 | |

## Appendix C. The cold reads

Before EX_124, a fresh helper with no knowledge of this chat cold-read the draft and rechecked the revision (`cold_read_findings_v0_1r1.md`, `cold_read_recheck_v0_1r1.md`, in EX_124). This edition had a third pass from the same kind of helper on the v0.1r2 draft (`cold_read_v0_1r2.md`, in EX_126, with the draft and the diff), whose findings (one dead end for later-released methods, a classification table that was not total, the seal, the session lock, the orchestrator's standing under 5C, byte-code caches in the closure, and several wording points) are applied in this text.

## Appendix D. Citation anchors (EX_125 C07)

Every code citation in this note, with the Git blob id of the file at `3a9f6ac` and the text of the first cited line as stored (CRLF stripped), so that a reader whose tool shows different line numbers can still find the place. Verified with `git rev-parse 3a9f6ac:<path>` and `git show 3a9f6ac:<path>`.

| File (blob id at 3a9f6ac) | Lines | First cited line, as stored |
|---|---|---|
| `src/methods/E_001/multigame_e1.py` (`2ff455e1fd16`) | 23 | `values = (DOMAIN, view_sha256, str(target), METHOD_ID, VARIANT_ID,` |
| `src/methods/E_001/multigame_e1.py` (`2ff455e1fd16`) | 30-32 | `if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):` |
| `src/methods/E_001/multigame_e1.py` (`2ff455e1fd16`) | 33-34 | `if not profile.historical_development_target_allowed(target):` |
| `src/methods/E_001/multigame_e1.py` (`2ff455e1fd16`) | 50 | `ranking = sorted(counts, key=lambda n:(-counts[n], _digest(digest,tar...` |
| `src/methods/contract_adapters/e_001.py` (`58f925bb3c04`) | 27 | `task.target_draw_number, data_kind=task.run_mode)` |
| `src/methods/_common/contract_records.py` (`922977654e59`) | 335-336 | `if not p.historical_development_target_allowed(target):` |
| `src/methods/_common/contract_records.py` (`922977654e59`) | 354 | `_int(r['ledger_version'], f'{where}.ledger_version', low=1, high=1)` |
| `src/methods/_common/contract_records.py` (`922977654e59`) | 405-409 | `def tie_identity_for(record: Mapping, barrel_id: str, tie_version: st...` |
| `src/methods/_common/contract_forecast.py` (`ce28e4308953`) | 275-277 | `target = _int(rec['target_draw_number'], f'{where}.target_draw_number')` |
| `src/methods/_common/contract_receipts.py` (`d9b8544844cd`) | 68 | `_int(r['ledger_version'], f'{where}.ledger_version', low=1, high=1)` |
| `src/methods/_common/contract_task.py` (`13b8ba08b29e`) | 17 | `REAL_VIEW_DATA_KIND = 'REAL_HISTORICAL_DEVELOPMENT'  # the reader's e...` |
| `src/methods/_common/contract_task.py` (`13b8ba08b29e`) | 45-46 | `def view_data_kind(run_mode: str) -> str:` |
| `src/methods/_common/contract_vocab.py` (`f32f92847a1b`) | 69-73 | `RUN_MODES = frozenset(('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEX...` |
| `src/methods/_common/contract_vocab.py` (`f32f92847a1b`) | 113 | `TRACK_MODES = frozenset(('WF', 'IS'))` |
| `src/methods/_common/contract_runner.py` (`fa94da83a179`) | 114-116 | `if r.get('run_mode') == 'REAL_DEVELOPMENT' and ENABLE_CONTRACT_REAL_D...` |
| `src/methods/_common/contract_runner.py` (`fa94da83a179`) | 118-122 | `if r.get('run_mode') == 'REAL_DEVELOPMENT':` |
| `src/methods/Method_Contract_Runner.py` (`4c59d0f6fac6`) | 50 | `'run_id': run_id, 'master_file': f'{args.game}_results_master.csv', '...` |
| `src/methods/Method_Contract_Runner.py` (`4c59d0f6fac6`) | 89-90 | `repo_root = CR.PROJECT_ROOT` |
| `src/methods/_common/game_draws_reader.py` (`dcd425b9e143`) | 125 | `'target': self.target,` |
| `src/methods/_common/game_draws_reader.py` (`dcd425b9e143`) | 161 | `def _parse_prefix(raw: bytes, game_id: str, target: int, *, include_d...` |
| `src/methods/_common/game_draws_reader.py` (`dcd425b9e143`) | 234-237 | `legacy_exception = (game_id == 'POWERBALL' and target == 1577 and` |
| `src/methods/_common/game_draws_reader.py` (`dcd425b9e143`) | 241-244 | `if (run_manifest['master_file'] != name or type(sha) is not str or` |
| `src/methods/_common/game_draws_reader.py` (`dcd425b9e143`) | 249-254 | `if (len(ledger) != 1 or ledger[0].get('version') != '1' or` |
| `src/methods/_common/game_profiles.py` (`f8159d8dedd7`) | 72-76 | `def historical_development_target_allowed(self, draw_number: int) -> ...` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 45 | `VIEW = 'UNORDERED_SET'` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 56-59 | `CONTINUE = frozenset({('SUCCESS', 'PUBLISHED'), ('RUNTIME_FAILURE', '...` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 66-70 | `def roots() -> dict:` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 98-109 | `def ledger_pin(game_id: str) -> str:` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 143-144 | `if VIEW not in d['observation_views'] or d['uses_dates']:` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 184-185 | `if last >= p.holdout_first:` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 208-214 | `def load_plan(game_id: str, batch_id: str) -> dict:` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 220-230 | `if record_digest(plan) not in _logged_plan_digests(batch_id):` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 264-271 | `# ---------------------------------------------------------------- at...` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 331-352 | `"""('DONE', reason) only if this attempt's run folder proves the plan...` |
| `src/methods/_common/walk_forward.py` (`4555d5eee48d`) | 387-391 | `def pending(plan: Mapping) -> list[tuple[dict, int]]:` |
| `src/evaluation/outcome_reader.py` (`e32a176adc5b`) | 49-51 | `if type(t) is not int or not (p.first_draw + 1 <= t <= p.holdout_firs...` |
| `src/evaluation/outcome_reader.py` (`e32a176adc5b`) | 64-69 | `if (len(ledger) != 1 or ledger[0].get('version') != '1' or ledger[0]....` |
| `src/evaluation/outcome_reader.py` (`e32a176adc5b`) | 120-121 | `if number >= p.holdout_first:                # unreachable by constru...` |
| `src/evaluation/report.py` (`0ab2615b6340`) | 125-126 | `if last > p.holdout_first - 1:` |
| `src/evaluation/report_writer.py` (`843612330b2c`) | 422-423 | `w('- Every number above is computed from frozen forecasts and the act...` |
| `src/evaluation/n1_generator.py` (`d8ee66657b9c`) | 48-50 | `def stream_key(root_hex: str, policy_id: str, game_id: str, replicate...` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 135-150 | `def holdout_opened(root: Path, game: str) -> bool:` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 185-189 | `def to_csv_bytes(game: str, draws: list[Draw]) -> bytes:` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 226-233 | `def replace_atomically(path: Path, data: bytes) -> str:` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 298-300 | `if sha(data) != last["master_sha256"]:` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 446 | `data = to_csv_bytes(game, draws)` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 592 | `def update_game(root: Path, game: str, fetcher, months_back: int, tod...` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 613 | `grab_sha = write_new(grab_path, to_csv_bytes(game, grab))` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 616-617 | `if not overlap:` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 629 | `version = int(last["version"]) + 1` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 633-637 | `if not new:` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 639 | `backup_sha = write_new(backup, master_bytes)` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 640-647 | `merged = master + new` |
| `src/results_master_v0_1.py` (`7e3e67ba2061`) | 653-672 | `class Lock:` |
| `Run_Results_Updater.bat` (`1f31084cad2a`) | 4 | `rem No arguments = "update" with defaults (current month plus the pre...` |
| `Run_Results_Updater.bat` (`1f31084cad2a`) | 33 | `"%PY%" -u "%TOOL%" update` |
| `Run_Experiment.bat` (`dda9b4f5c3b4`) | 20 | `if not exist "%ROOT%src\methods\%SCRIPT_NAME%" goto :missing_script` |
| `Run_Experiment.bat` (`dda9b4f5c3b4`) | 38 | `pushd "%ROOT%src\methods"` |
| `Run_Method_Rankings.bat` (`72751378cae1`) | 9 | `set "TOOL=%ROOT%src\evaluation\Method_Rankings_Report.py"` |
| `tests/test_wf1b_static.py` (`9e359c9a260b`) | 12-14 | `ALLOWED_COMMON = {'_common.contract_publication', '_common.contract_r...` |
| `tests/test_wf1b_static.py` (`9e359c9a260b`) | 34-38 | `def test_no_method_file_imports_the_evaluator(self):` |
| `tests/test_wf1b_static.py` (`9e359c9a260b`) | 60-63 | `self.assertNotIn('_trusted_file_bytes', text, p.name)` |
| `tests/test_code3_retirement.py` (`6e80a4774921`) | 91 | `self.assertEqual(sorted(p.name for p in (ROOT / 'archive' / 'methods'...` |
| `tests/test_code3_retirement.py` (`6e80a4774921`) | 94-99 | `class ArchiveIsNeverExecuted(unittest.TestCase):` |
| `tests/test_e1r2_revision2.py` (`063d2d80c7bf`) | 223-239 | `def test_admitted_and_refused(self):` |
| `src/methods/_common/multigame_standalone_contract.py` (`b113717073d3`) | 43 | `if not profile.historical_development_target_allowed(target):` |
| `src/methods/_common/multigame_standalone_contract.py` (`b113717073d3`) | 120 | `not profile.historical_development_target_allowed(target)):` |
| `src/methods/_common/multigame_worker_launch_handshake.py` (`c83ccca76ac3`) | 27 | `if (type(draw_number) is not int or not profile.historical_developmen...` |
| `src/coordinator_private/multigame_launch_spec.py` (`a6ecb047d3be`) | 63 | `if not profile.historical_development_target_allowed(draw_number):` |

## Appendix E. The gate matrix (EX_125 acceptance item 1)

Stages: **S0** before any opening; **S1** opened, no Mode H plan; **S2** plan exists, batch in progress; **S3** batch COMPLETE, not scored; **S4** Mode H scored (sealed); **S5** developed record exists (weekly operation); **X** orphan marker present, or `INSTALL_IN_PROGRESS.txt` present (any stage). A newly released variant joins the session roster at its next session and is forecast from `holdout_last + 1` onward (never the holdout draws, 6.3); a retired one leaves the roster; the gates are the same. "Validate" = passes structural validation; "Publish" = the dispatch gate admits the run and a record may be published; "Score" = the evaluator may score it.

| Request | S0 | S1 | S2 | S3 | S4 | S5 | X |
|---|---|---|---|---|---|---|---|
| Synthetic modes (no binding) | validate, publish (synthetic workspace), never scored as evidence | same | same | same | same | same | refuse |
| `REAL_DEVELOPMENT`, target in the development prefix (no binding; today's batches) | validate, publish, scored by a development report | same | same | same | same | same | refuse |
| `REAL_DEVELOPMENT`, target above `holdout_last`, bound to a session, release date not before the draw date | validate; publish refused (no developed record) | validate; publish refused | validate; publish refused | validate; publish refused | validate; publish refused | validate, publish, score after N's freeze line | refuse |
| `REAL_DEVELOPMENT`, target above `holdout_last`, unbound, or release date before the draw date (should be `CATCH_UP`) | refuse (structural / publication) | refuse | refuse | refuse | refuse | refuse | refuse |
| `REAL_DEVELOPMENT`, holdout target | refuse (structural) | refuse | refuse | refuse | refuse | refuse | refuse |
| `REAL_HOLDOUT`, bound to the game's plan | refuse (no opening record) | refuse (no plan) | validate, publish if the pair is in the plan and not DONE; not scored | publish refused (all DONE); score when the roster verifies | refuse (sealed) | refuse (sealed) | refuse |
| `REAL_HOLDOUT`, unbound or wrong digest or other target | refuse | refuse | refuse | refuse | refuse | refuse | refuse |
| `CATCH_UP` / `FINAL_NEXT_DRAW`, bound to a session, target above `holdout_last`, mode agreeing with the release date and the pin | validate; publish refused (no developed record) | validate; publish refused | validate; publish refused | validate; publish refused | validate; publish refused | validate, publish; score after N's freeze line (and N's result accepted) | refuse |
| `CATCH_UP` with release date not before the draw date; `FINAL_NEXT_DRAW` for a target the pinned master already holds; any run whose pin differs from its session's | refuse (publication / pin gate) | refuse | refuse | refuse | refuse | refuse | refuse |
| `CATCH_UP` / `FINAL_NEXT_DRAW`, unbound, or holdout target | refuse | refuse | refuse | refuse | refuse | refuse | refuse |
| Hand-typed `Method_Contract_Runner.py run` with `--binding` | as the row of its mode and binding: it is admitted only if the plan or session it names exists and lists it; it is scored only as that plan's or session's record | | | | | | refuse |
| `IN_SAMPLE_DIAGNOSTIC`, benchmarks, coordinated path | refused today; unchanged | | | | | | refuse |

## Appendix F. The weekly session: states and event order (acceptance item 2)

One owner command, two processes, one target at a time. Persisted state: run records (create-only), the session record, the freeze lines, the score lines.

```
Run_Weekly_Session.bat --game G
  -> orchestrator (imports neither side)
     1. Run_Experiment.bat Method_Weekly_Forecast.py status --game G        [prints the status block]
     2. Run_Experiment.bat Method_Weekly_Forecast.py open-session --game G  [SESSION_<id>.json, create-only]
     3. loop:
          Run_Experiment.bat Method_Weekly_Forecast.py next --game G --session S
            N := lowest target not closed for every active variant, with an accepted result
            if the master's last row differs from S's pin: -> STALE, stop (owner opens a new session)
            if no such N:
               if next draw M = last accepted + 1 and >= 1 h before M's deadline (judged once, here):
                    run every active variant in FINAL_NEXT_DRAW for M (bound to S), freeze line for M  -> FROZE_NEXT M, stop
               else -> WAIT (result pending) or NONE (deadline rule), stop
            if N has a freeze line: -> FROZE N            (open forecast now with a result; or resume after a crash)
            else: for each active variant without a bound DONE record for N: one run (mode by 6.4)
                  when all DONE: append N's freeze line naming one record per variant (first bound DONE attempt)  -> FROZE N
          Run_Evaluation.bat Method_Weekly_Score.py score --game G --session S --target N
            verify N's freeze line names every record; outcome_release_allowed(G, N)
            for each record of N without a score line: read N's outcome once, score, append (create-only)
          (back to next)
     4. print the status block; exit
```

Properties: (i) `next` never considers N + 1 while an N with an accepted result is not closed, so N is closed before N + 1 whatever the orchestrator does; (ii) a crash after the freeze line and before the score resumes at `next`, which returns `FROZE N` without running anything, then `score` runs; a crash during the runs for N resumes with the remaining variants only (bound DONE records are kept); a crash during `score` resumes with the unscored records only (score lines are create-only); (iii) no accepted record is rewritten at any step; (iv) an open `FINAL_NEXT_DRAW` forecast whose result has now arrived is the lowest unclosed N with an accepted result, so it is scored before anything else; (v) an unaccepted draw stops the loop; the next session continues from it.

## Appendix G. The witness lifecycle (acceptance item 3)

```
freeze line for N appended (digest d)                      [forecast ledger; local; the fact]
   |
   |-- optional: owner pushes the ledgers / emails d        [outside the repository]
   |-- optional: owner records WITNESS_RECORDED(N, kind, ref, time recorded)   [witness ledger; a claim]
   |-- optional, any time later: a named person checks the reference and records
   |      WITNESS_VERIFIED(N, verified-by, received-utc, how)                     [witness ledger; evidence]
   |
score for N appended (facts only: quantities, pins, tier, frozen_at_utc, effective class)   [score ledger]
   |
report (any date): publication status derived now:
     PUBLISHED_BEFORE_DRAW  if a WITNESS_VERIFIED line for d has received-utc < N's deadline
     TIMELINESS_UNVERIFIED  otherwise, shown as "witness recorded, not verified" or "no witness"
```

Worked cases (invented): (1) score first on 15 November, the owner pushes on 16 November and records the witness, the reviewer verifies on 20 November that the commit carries d and GitHub shows it pushed on 16 November 09:12 UTC, before the deadline: the report of 21 November says PUBLISHED_BEFORE_DRAW; the score line of 15 November is byte-identical. (2) A `WITNESS_RECORDED` line names a commit that does not exist: the verifier records nothing; status stays TIMELINESS_UNVERIFIED, the claim is shown. (3) A commit exists but carries a different digest: `WITNESS_VERIFIED` is not written (the verifier found no match); shown as unverified. (4) A commit pushed after the deadline: `WITNESS_VERIFIED` with received-utc after the deadline is recorded and shown; the status does not promote. No step needs the network inside the project's tools; verification is a human act recorded afterwards.

## Appendix H. The Mode H study manifest: digest inventory (acceptance item 4)

| Category | What is enumerated and digested | How a difference is treated |
|---|---|---|
| Method and contract code | every file under `src/methods/` (all extensions: `.py`, `.json`, `.txt`, including `contract_data/` and `install_records/`), excluding `__pycache__/` and `*.py[co]` by name (interpreter caches, not code; the non-claim: a tampered cache is not detected, which is why the launchers run Python with `-B` or the manifest step clears the caches first) | any added, removed or changed file: refuse |
| Evaluator | every file under `src/evaluation/` (code, `registry/*.json`, `seed_policies/*.json`) | refuse |
| Orchestration and tools | every other file under `src/` (the coordinator, `coordinator_private/`, `package_tools/`, the updater `results_master_v0_1.py`, the two-site checker, the orchestrator) | refuse |
| Launchers and sequencing | every `.bat` at the repository root; `requirements.txt`; `install_upgrade_dependencies_into_venv.bat` | refuse |
| Environment | Python version; platform; every installed distribution name and version (`importlib.metadata`), sorted; digest of that list | refuse |
| Registries and declarations | covered by `src/methods/_common/contract_data/` and `src/evaluation/registry/` above; the cohort's declaration and entry digests also listed explicitly | refuse |
| Source data version | `v_f` (the ledger's last row at freeze, with its SHA-256); the rule "exactly one UPDATE row follows before the batch"; the batch records `v_a` | any row beyond `v_a` before the score is sealed: refuse |
| Deliberately excluded (stated in the manifest) | `tests/`, `doc/`, `review/`, `exchange/`, `CLAUDE_CODE_WORKING_FOLDER_TREE/`, `.claude/`, `.git*` (not executed in Mode H); `source_data/`, `results/`, `transitory_data/` (data and records, pinned separately; `transitory_data/` holds reviewed orphan utilities that never run in Mode H) | not claimed |

Checked at: the manifest (written), the plan, every `run` invocation, the score. Tests mutate each category once, add a previously unseen executable file, change one package version string, and append a `NO_CHANGE` row between approvals; each must refuse before any scientific action.

## Appendix I. Effective class: the total rule (acceptance item 5)

Inputs per record: the run mode (hence the immutable tier), the record's `frozen_at_utc`, N's deadline, whether N's result was accepted before the record was made, the variant's release date versus N's draw date, and whether the record is a forecast or a `PREDICTION_FAILED` failure.

| Case | Run mode / tier | Effective class | Counted where |
|---|---|---|---|
| Holdout target, bound to the Mode H plan | `REAL_HOLDOUT` / `HOLDOUT_MODE_H` | `HOLDOUT_MODE_H` | Mode H family only |
| On time: `FINAL_NEXT_DRAW`, `frozen_at_utc` < deadline, result accepted later | `PROSPECTIVE` | `PROSPECTIVE` (publication status derived separately) | PROSPECTIVE tables and N1 |
| Late before the draw: `FINAL_NEXT_DRAW`, `frozen_at_utc` >= deadline, result not yet accepted when made | `PROSPECTIVE` (immutable) | `LATE_PRE_DRAW` | operational portfolio only; scored and kept; never re-forecast |
| After the draw, release date before the draw date | `CATCH_UP` / `CATCH_UP` | `CATCH_UP` | CATCH-UP tables and N1 |
| After the draw, release date on or after the draw date (a method's back-history) | `REAL_DEVELOPMENT` / `DEVELOPMENT_WF_EXPLORATORY` | `DEVELOPMENT_WF_EXPLORATORY` | development tables; never `MISSING_BATCH` |
| Failure in any mode | the mode's tier, `PREDICTION_FAILED` | missing in that class | counted as missing (R3 3.6) |
| Eligible variant with no `FINAL_NEXT_DRAW` record for N (missed freeze) | none for that record; the later catch-up record is `CATCH_UP` | the freeze line marks the variant `MISSING_BATCH` for N | the missed week is reported |
| A straddling set | per record, by the rows above | per record | the freeze line's `deadline_met` summarises |
| Restart midway through a `FINAL_NEXT_DRAW` set, at least an hour before the deadline | remaining variants complete the set; each record by its own `frozen_at_utc` | per record | as above |
| Restart midway with less than an hour left | the set stays partial; after N's result is accepted the missing variants get `CATCH_UP` records and are marked `MISSING_BATCH` on the line | per record | as above |
| The master grows during a session (a result arrives mid-set) | every further run of the session refuses (its pin differs from the session's); `next` exits `STALE`; a new session continues N as a catch-up | per record | as above |
| `FINAL_NEXT_DRAW` requested for a draw the pinned master already holds | refused by the pin gate (3.4(a)); no record | none | none |
| `CATCH_UP` requested with release date on or after the draw date; `REAL_DEVELOPMENT` above `holdout_last` requested with release date before it | refused by the publication gate (3.4(b)); no record | none | none |

Every combination of the inputs falls in exactly one row above (the gates make the remaining combinations impossible, and those rows say so). A record's effective class is written into its score line and is the same in the weekly note, the dated tables, the full report and N1's inputs; no record is relabelled in place.

## Appendix J. MHUP-A installation safety (acceptance item 6; EX_125 C01)

Barriers: **E** = E_1's own `src/methods/E_001/IN_DEVELOPMENT.txt` (today's rule: E_1 refuses while it exists); **P** = the package-wide `src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt`, honoured by the **new** dispatch gate like the orphan marker (every run refuses while it exists), unknown to the old gate. Neither is ever committed. The owner launches nothing during the install (checklist), so the interim notes describe what would refuse if a run were wrongly launched.

| Step | Action | Files changed | What refuses if a run were launched | STOP handling |
|---|---|---|---|---|
| 0 | `git status --short` clean; `git pull --ff-only` | none | as today | stop |
| 1 | PRE (verifier, read-only) | none | as today | stop |
| 2 | Copy barriers **E** and **P** | two new files | old gate: E_1 refuses (E); the other 39 run as today (old code, old data) | stop; remove E and P |
| 3 | Copy the overlay (readers, validators, new dispatch gate, E_1 r3 and its archive of r2, registry entries, evaluator, launchers, records) | the package's files | new gate: everything refuses (P); E_1 also refuses (E); mixed old/new modules possible only during the copy itself | stop; send output; Claude writes the restore steps (`git checkout --` of the listed paths, then remove E and P) |
| 4 | POST (verifier) | none | everything refuses (P) | stop as step 3 |
| 5 | The suite (the barrier paths are module constants the harness patches, so the suite passes with P present) | none | everything refuses (P) | stop as step 3 |
| 6 | The install-record tool writes `INSTALL_MHUP_A_V1.json` | one new file | everything refuses (P) | stop as step 3 |
| 7 | Delete **E**, then **P** | two files removed | nothing refuses beyond the normal gates; E_1 r3 is now released (the ER-2r1 extension) | if P was removed and a later step fails: re-create P by hand (its content is one fixed line) and stop |
| 8 | Stage the listed paths; `git status --short` shows exactly them; commit | index, commit | normal | stop |
| 9 | COMMITTED (verifier, including the install record) | none | normal | stop; do not push |
| 10 | Push | remote | normal | |

Negative tests shipped with the package: a run attempted with P present refuses with `INSTALL_IN_PROGRESS`; with E present E_1 refuses; an overlay with one file missing or one byte wrong STOPs at POST; the suite fails if P is absent at step 5 in the rehearsal (proving the harness patches it, not the absence of the barrier); a synthetic run attempted after step 7 with the suite having failed is prevented by the sequence (step 7 follows a passed step 5). What this does not claim: protection against a run deliberately launched between steps 2 and 3 (old code, old data: it behaves as today) or during the copy of step 3 (mixed modules; the checklist forbids it).

## Appendix K. Rules retained, amended or superseded, and the new names (acceptance item 7)

| Rule | Status after ratification |
|---|---|
| R2 N-1 and view contract; T-05; B1 | retained unchanged |
| R2-C03 "independent evidence" and the proposal's candidate-then-promotion step | superseded for production by the owner's C03 decision of 3 November 2026 (7) |
| R3 1.3 push; 1.5 external proof; 10.1(6); 10.2 push steps and post-diagram paragraph; 11.5 item 4 remote evidence; 17.3.9 `PROSPECTIVE` wording; R3-D20 push requirement | superseded for this project under OFF-1 (6.5); R3's text unchanged until its next edition |
| R3 10.5 statuses; E2R-R40C "labelled unverified and counted" | applied as written (6.4, 6.5) |
| R3 6 "development caps remain 1576/1693"; E2R-R52 run-time ceiling | amended: the caps define the development prefix; run-time targets are gated by master version, opening record and mode gates (3.2, 3.4) |
| R3 6.2 study manifest, opening record, combined-versus-separate store | satisfied by 4.1, 4.2, 4.5 |
| R3 3.6 missingness; R3 6.3 revision separation; R3 7.4 search log; R3 17 rankings as reports | retained; applied in 5.2, 6.6 |
| R3-T50 no upgrade within Mode H | applied by the closure and environment freeze (4.1) |
| E2R-R41 reserved rows for `REAL_HOLDOUT` and `FINAL_NEXT_DRAW` | unreserved as written (5.1, 6.4) |
| E2R-R44 "Mode H and FINAL stay shut" | amended: open only for bound requests under the owner records (3.4) |
| E2R-1 9.1 closed vocabularies; R3 17.3.9 tiers | amended: run mode and tier `CATCH_UP` added; operational category `LATE_PRE_DRAW` added (6.4) |
| E2R-R14A new revision for any code change; E2R-R54 archive; E2R-R56 archive never executed; E2R-R58 release package | retained; ER-2r1 extended to E_1 revision 3 by the owner (Q10) |
| E2RC2-B01/B02 no caller-chosen authority | retained; the binding is resolved by the gate at fixed roots (3.4) |
| H-1 5.4 switches | amended: no new switch; the owner records and the gates govern the new modes (5.1) |
| Architecture 5C.1 launch interfaces (protected section; amended by ratification, not edited) | the orchestrator is named as a sequencer of the two launchers that is not a coordinator: no supervision, no termination, no PID use, no orphan writes (6.1) |
| H-1 5.4 Option F "no second production launcher" | amended: `Run_Method_Rankings.bat` (WF-1B), `Run_Evaluation.bat` and `Run_Weekly_Session.bat` are the evaluator and session launchers; method code still runs only through `Run_Experiment.bat` (6.1) |
| H-1 5.1 holdout rules; rulebook rules 4 and 5; H-2 section 5; the exposure record | unchanged until Q7 is decided (9) |
| Rulebook rule 7 (never run); `.claude/settings.json` deny patterns | extended to `Run_Evaluation.bat`, `Run_Weekly_Session.bat`, `Method_Mode_H.py`, `Method_Weekly_Forecast.py`, `Method_Weekly_Score.py`, `Weekly_Session_Orchestrator.py` (6.1) |
| Register v0.23 "all frozen before the holdout is opened" | amended to the primary statement (1) |
| Lotterywest cross-checks | prove agreement with held draws, consecutive numbering, dates and master-ledger consistency; do not prove a new draw against a second source (7) |

New names: `Run_Evaluation.bat`, `Run_Weekly_Session.bat`, `Method_Mode_H.py` (`manifest`, `open`, `declare-developed`), `Method_Weekly_Forecast.py` (`status`, `open-session`, `next`), `Method_Weekly_Score.py` (`score`, `witness`, `verify`), `Weekly_Session_Orchestrator.py`, `master_versions.py`; records `MODE_H_STUDY_MANIFEST_V1`, `MODE_H_BATCH_ID`, `SESSION_<id>`, `FORECAST_LEDGER_V1`, `WITNESS_LEDGER_V1`, `SCORE_LEDGER_V1`, `INSTALL_<PACKAGE>_V1`, `INSTALL_BASELINE_20261031_V1`, `DEVELOPED_<GAME>`; search-log row types `MODE_H_STUDY_MANIFEST`, `HOLDOUT_OPENED`, `MODE_H_BATCH`, `MODE_H_REPORT`, `WEEKLY_TABLE`, `WEEKLY_REPORT`; vocabulary `CATCH_UP` (run mode and tier), `LATE_PRE_DRAW` (operational category), `WITNESS_RECORDED`, `WITNESS_VERIFIED` (witness ledger line kinds); barrier `INSTALL_IN_PROGRESS.txt`.

## Appendix L. Oracles and tests (acceptance item 8), and the existing tests that change

**Oracles (R-4):** a byte-exact prefix oracle for the master versions, built without the updater; T-05 extended to a version-3 synthetic master with two UPDATE and one NO_CHANGE rows, a changed historical prefix (must refuse), an aborted transaction fixture (must refuse); the E_1 revision 2 reference fixture (label-for-label rankings and tie order, both games, synthetic and real view kinds, each real mode on the same prefix); the exact-arithmetic measures as in WF-1B; an independently built chain checker for the forecast ledger.

**Gates:** every structural, publication and scoring rule refused once (Appendix E), including forged and unbound requests, a sealed batch, a pre-plan holdout request, a holdout target in `REAL_DEVELOPMENT`, the orphan marker and the install barrier.

**Mode H:** manifest written once; plan refused without opening record, with a mismatched manifest, with a changed closure or environment, with an extra ledger row, and a second time; COMPLETE requires every planned pair DONE; a failed pair is DONE and scored as missing; the scorer refuses an incomplete batch, a roster that differs from the plan, and a second routine attempt; the corrective scoring run has its own identity.

**Weekly:** two and four missed draws per game, independently; a variant released after Mode H is forecast from `holdout_last + 1` and never for a holdout draw; a session whose master grew mid-way exits `STALE` and every further run refuses; the session lock refuses a second `open-session`; `next` never considers N + 1 while N is unclosed with an accepted result; a crash after the freeze line and before the score resumes without rerunning; a crash during runs reruns only the remaining variants; a failed variant is DONE and not rerun; `FROZE_NEXT` only with at least an hour to the deadline; refusal after the deadline; a straddling set classified record by record; `MISSING_BATCH` only for eligible variants; unbound records ignored and listed; the orchestrator imports neither side (static), never kills (static: no `terminate`, `kill`, `taskkill`, psutil), stops on a non-zero child exit.

**Ledgers and witness:** chain breaks on edit, removal, reorder; witness line for an unknown digest refused; verification received after the deadline does not promote; verification added after the score changes the next report and no score byte; no network call in any routine command (static).

**Install:** Appendix J's negatives in the LF and CRLF rehearsals; the install-record tool's duplicate refusal; the baseline record's validation.

**Existing tests that change (the only ones):** `tests/test_code3_retirement.py` line 91 (archive folders `r1` and `r2`); `tests/test_e1r2_revision2.py` lines 223-239 (admissions of revision 3; the revision comparison becomes a fixture comparison); `tests/test_wf1b_static.py` lines 12-14 (`ALLOWED_COMMON` gains `_common.master_versions`), line 60 (`Method_Mode_H.py` may name `source_data`, for the two owner records it writes there) and line 63 (`Method_Weekly_Score.py` may import the outcome reader); every other existing test unchanged, with the suite runner's expected counts updated from the tools.

**Mutation checks:** one planted defect per rule above, each caught by a named test; shipped with the package. **Rehearsals:** LF and CRLF clones; Claude Code T016 (MHUP-A) and T017 (MHUP-B) on Windows. No destructive test without the owner's separate approval; no test reads a holdout result.

*End of design v0.1r2.*
