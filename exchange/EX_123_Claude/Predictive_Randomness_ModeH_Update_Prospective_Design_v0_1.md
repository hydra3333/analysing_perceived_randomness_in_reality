# Mode H, the results update and the prospective mode - design v0.1

**Version:** v0.1, 2 November 2026 (Adelaide, UTC+10:30). CANDIDATE for design-stage review (R-3).
**Author:** Claude (primary designer and coder). **Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner.
**Base:** `main` at `21db0331275e503032700e7b12c5def9db7727d3` (DOC-10 installed at `7bb0bfd`; register v0.23).
**Authorises nothing.** No run, update, holdout opening, Mode H, FINAL or prospective forecast follows from this text. Every one of those stays a separate owner approval after review.
**Holdout statement:** this note contains no outcome of any draw. Draw numbers appear only as identifiers. Calendar dates of future draws were derived from the era profiles' weekly rule (`game_profiles.derived_date`), not from any result.

## Work-item card

| Field | Value |
|---|---|
| Item | MHUP-1: Mode H, the results update and the prospective mode (roadmap item 10c; GOAL-1, ORD-1) |
| Author / reviewer | Claude / ChatGPT reviewer chat (R-3 design review; R-2 later for code) |
| Risk tier | HIGH (reader and digest code; evaluator and scorer; holdout access and unsealing; publication and freezing; `source_data/`) |
| Owner inputs (binding) | MH-1, OFF-1, EFF-1, HX-1, HX-2, FB-1, GOAL-1, ORD-1, TSC-1 (register v0.23) |
| Probe findings carried | A1, A2, A3, A6, A7, A8, A11 (register v0.23; `exchange/EX_116_Claude/cold_read_probe_findings.md`) |
| Reviewer's notes on the takeover (1 November 2026) | (1) flagged holdout draws stay valid and counted; (2) holdout outcomes stay inaccessible until the reviewed, owner-authorised Mode H procedure, which then permits scoring; (3) the first results are described as showing no statistically compelling departure from the fair-draw reference under the reported measures, not as proof of randomness |
| Evidence state | DESIGN ONLY. Code facts below were read from the base commit and are cited by file and line |

## 0. The whole thing in plain English

Today the system can only look at draws before the holdout. To make real next-draw forecasts we need four things, in this order:

1. **Read a results file that has grown.** Every reader today refuses the results file as soon as it has a second version (finding A1). The first job is a reader that accepts the updater's later versions, checks their history, and still serves each forecast only the draws before its target.
2. **Open the holdout, once, on the record.** You freeze a study plan (which methods, which measures, which software), then write the opening record. Only then does the updater add the holdout draws and every later draw.
3. **Mode H.** Every released variant forecasts each of the ten holdout draws, each from the draws before it. All forecasts are frozen before the scorer reads any holdout result. Then the ten draws are scored once, and Powerball 1585 and 1586 carry their exposure flag (still fully counted).
4. **The weekly session (MH-1).** Per game, one command: catch up any draws that have no forecast, score the open forecast, then freeze and record the next draw's forecast before that draw. Everything runs offline; the timing proof is a local, chained record with times, and a GitHub push is only an optional extra witness.

The draws we are aiming at (derived from the weekly calendar rule): **Oz Lotto 1708 on Tuesday 10 November** and **Powerball 1591 on Thursday 12 November**. Before them, the catch-up covers Oz Lotto 1704-1707 and Powerball 1587-1590 (1587 and 1588 flagged, HX-2).

## 1. A wording conflict that needs your decision first (OWNER Q1)

Register v0.23 ("Terms for that design") and H-1 section 10 describe Mode H as: every released variant forecasts each of the ten holdout draws **walk-forward (each from the draws before it)**, **all frozen before the holdout is opened**, then scored once.

Both halves cannot hold literally. A walk-forward forecast for Powerball 1578 must be trained on draw 1577, which is itself a holdout draw; it cannot exist until 1577's result is available to the training data. Only the first target of each game (Powerball 1577, Oz Lotto 1694) can be forecast before any holdout result is available.

Two readings keep the intent:

- **Reading A (RECOMMENDED): "frozen before the scorer reads any holdout result."** The holdout is opened and added to the results file; then one Mode H batch forecasts all ten targets, each method seeing only the draws before its target (the strict N-1 rule, which T-05 already proves); every forecast is frozen, create-only, before the scorer reads any holdout result; then the ten are scored once. This is exactly how the reviewed walk-forward batches and the WF-1B scorer already work, so it needs the least new code.
- **Reading B: "release one outcome at a time."** For each target in turn: freeze every forecast for N, then release N's result, score N, move on. This gives a step-by-step time record (R3 6.2 mentions this "separated store" option). It needs a new step engine and more review.

Why A is enough: under A no method ever sees its own target or any later draw (the reader reads no row at or after the target and T-05 tests it), and the scorer cannot read a holdout result until the whole Mode H batch is frozen (section 4.3). What B adds is a timestamped ordering between each freeze and each release; under A that ordering is replaced by the batch-complete rule plus the N-1 reader. A forecast for target 1577 is byte-identical whether it is made before or after the update (T-05), so freezing it early would add nothing measurable.

## 2. Piece 1 - reading a results file that has grown (finding A1)

### 2.1 What the code does today

- `src/methods/_common/game_draws_reader.py` lines 241-254: the run manifest must pin `ledger_version == 1`, the ledger must have exactly one row, `INIT`, with `last_draw == holdout_first - 1`. Line 237: the target must satisfy `historical_development_target_allowed` (target < `holdout_first`), apart from E_1's forecast-only 1577 exception (lines 234-236).
- `src/methods/_common/walk_forward.py` lines 100-109 and 184-195: the batch pins row 1 of the ledger only, with `ledger_version: 1`, and refuses `last >= holdout_first`.
- `src/evaluation/outcome_reader.py` lines 49-51 and 55-80: targets only in `[first_draw + 1, holdout_first - 1]`, and the ledger must be the single INIT row.
- `src/evaluation/report.py` lines 125-126: `last <= holdout_first - 1`.
- The updater (`src/results_master_v0_1.py`) rewrites the whole master with `to_csv_bytes` (lines 185-189: header, then one CRLF-terminated line per draw) after appending new draws (lines 640-647), appends one ledger row per run (`UPDATE`, or `NO_CHANGE` with the same SHA-256 and a new version number, lines 633-636), and keeps a create-only backup of the previous master (line 639). The INIT master was also written with `to_csv_bytes` (`cmd_init`, around line 446).

### 2.2 The version-2 reading rules (RECOMMENDED)

One shared, orchestration-only module, `src/methods/_common/master_versions.py`, used by the draw reader, the outcome reader, the walk-forward driver and the report. Nothing in it reaches a method.

1. **Ledger chain check.** The header equals the updater's `LEDGER_COLUMNS` exactly. Versions run 1, 2, 3, ... with no gap. Row 1 is the INIT row with today's exact checks (unchanged). Every later row is `UPDATE` or `NO_CHANGE`:
   - `NO_CHANGE`: the same `master_sha256`, `first_draw`, `last_draw` and `draw_count` as the row before; `added_count` 0.
   - `UPDATE`: the same `first_draw`; `added_first` = previous `last_draw` + 1; `added_last` = `last_draw`; `draw_count` = previous `draw_count` + `added_count`; `backup_sha256` = the previous row's `master_sha256`.
   - Any other action, or any broken rule: refuse. The INIT verification record is checked as today.
2. **Prefix-verified pins.** A run still pins `(ledger_version v, master_sha256 s)`. The reader accepts the pin when row v exists with `master_sha256 == s`, and when the SHA-256 of the current master's first `1 + draw_count(v)` lines (header plus v's draws, each with its CRLF) equals s. Because the updater only appends and re-serialises with the same function, version v's bytes are an exact prefix of every later version (section 2.1). Consequences:
   - the committed batches and reports (pinned to version 1) stay verifiable after any update;
   - a `NO_CHANGE` row needs no special handling: a pin to it verifies like a pin to the row it repeats;
   - a later change to any earlier row (a correction) breaks the prefix check and every run refuses: corrections need their own reviewed design (R3 10.3), which this note does not provide.
3. **The target ceiling.** For a pin to version v, the reader allows targets up to `last_draw(v) + 1`. Targets at or above the game's `holdout_first` additionally need a valid opening record for that game (section 3.2); without one the reader refuses exactly as today. The E_1 1577 exception is unchanged.
4. **What does not change.** The prefix parse (`_parse_prefix`, lines 161-209) still reads no data column of the target or any later row. View schemas and digests are unchanged, so every existing forecast, golden and T-05 test is unchanged. The whole-master and prefix SHA-256 remain orchestration-only provenance (the B1 rule) and never reach a method.
5. **The outcome reader** uses the same chain and pin rules, and serves targets up to `last_draw(v)` only. For targets at or above `holdout_first` it also needs the opening record and the freeze rule of section 4.3.

**Tests (planned; R-4 oracles):** a synthetic ledger of 1 INIT, 2 UPDATE and 1 NO_CHANGE rows, with every chain rule broken once (each must refuse); a byte-exact prefix oracle built independently of the updater; T-05 rerun on a version-3 synthetic master (the same view bytes and digests as on version 1 for every development target); a corrected earlier row must refuse; the existing 471 tests unchanged.

## 3. Piece 2 - opening the holdout (findings A2, A3)

### 3.1 The study manifest (R3 6.2)

Before the holdout is opened, a tool writes, create-only, `results/real/holdout/<GAME>/MODE_H_STUDY_MANIFEST_V1.json`, and appends one search-log row. It binds:
- the cohort: every released (game, method, variant) with its declaration digest and registry-entry digest, and every registered method that is not runnable, by name, with its status (R3 10.1(3); mark, never suppress);
- the targets: the ten holdout draws (Powerball 1577-1586, Oz Lotto 1694-1703), with the exposure flags of HX-1 (Powerball 1585 and 1586);
- the measures and the Mode H families (section 4.4), the N1 seed policy, and the scorer's version;
- the code: the SHA-256 of every file under `src/` that the batch and the scorer import (method, contract, reader, evaluation);
- **the environment (R3-T50):** the Python version and the exact name and version of every installed distribution in the venv (`importlib.metadata`), and their digest. This also closes the open item that the owner's full package list was never recorded.

The owner may commit it to GitHub as an optional witness (OFF-1).

### 3.2 The opening record

`HOLDOUT_OPENED_<GAME>.json` (schema `HOLDOUT_OPENED_V1`) is today defined only by the updater's check (`results_master_v0_1.py` lines 135-150: `schema`, `game`, a 64-hex `study_manifest_sha256`, `opened_utc`, `owner_statement`). Design:
- written only by a new owner-run command, `open --game G`, create-only in `source_data/`, after it checks that the study manifest exists, is valid and its SHA-256 is the one named; the owner types a fixed sentence as `owner_statement`;
- it is permanent, and it also unlocks every later update for that game (finding A2): this is intended, because after Mode H the weekly session needs those updates;
- the readers (section 2.2 rule 3) accept it with the same field checks as the updater, plus a check that the named study manifest exists with that SHA-256.

### 3.3 The order of events for each game (each step is the owner's separate approval)

1. The code package installed and verified. Nothing has read a holdout result.
2. **Approval 1:** freeze the study manifest; write the opening record.
3. **Approval 2:** the first results update (`Run_Results_Updater.bat update --games G`; never run bare). It adds the holdout and every later draw in one version (finding A3). Before this first run, the updater's offline `--self-test` is run under Python 3.15 (finding A9).
4. **Approval 3:** the Mode H batch (section 4).
5. **Approval 4:** the Mode H score and report (section 4.3 to 4.5).
6. Then the catch-up and the first weekly session (section 5), after you decide whether to declare the system developed (GOAL-1).

### 3.4 The store (R3 6.2; OWNER Q2)

RECOMMENDED: **the combined master** that the updater already writes, with the version-2 reader of section 2. A separate quarantine store releasing one result at a time would mean changing the owner's updater (finding A3) and building a release engine (Reading B); under Reading A it gives no extra protection, because methods are already confined to their prefix and the scorer to the freeze rule.

## 4. Piece 3 - Mode H

### 4.1 The batch

The existing walk-forward driver gains a Mode H batch kind: `plan --mode H --game G --manifest <study manifest>`. It:
- refuses unless the opening record and the study manifest are valid and agree, and the pinned master version covers the last target;
- takes its cohort, targets and environment from the study manifest (no other choice is possible);
- refuses unless the installed environment and code digests equal the study manifest's (R3-T50: no upgrade within Mode H);
- runs each (variant, target) exactly as today, one contract run each, with `run_mode` `REAL_HOLDOUT`. In the contract vocabulary (`contract_vocab.py` lines 69-100), `REAL_HOLDOUT` is reserved and refused today; this package adds the one producible row `REAL_HOLDOUT / FORECAST -> (HOLDOUT_FORECAST, HOLDOUT_MODE_H)`. The evidence tier `HOLDOUT_MODE_H` already exists; the product kind `HOLDOUT_FORECAST` is new (an E2R-1 vocabulary addition, recorded in the register).
- uses the existing STOP rule unchanged.

Size: Powerball 40 variants x 10 targets = 400 runs; Oz Lotto 400 runs. On the first batches' timings (17,280 runs in about 80 minutes), each game's Mode H batch takes a few minutes.

### 4.2 One batch only

A Mode H batch can be planned once per game. A second plan for the same study manifest is refused. A run that stops is reported as stopped, never retried or replaced (mark, never suppress); the owner decides what follows.

### 4.3 The freeze rule (always-review subject)

The scorer reads a holdout result only when the Mode H batch's plan and segment records show the batch COMPLETE: every (variant, target) of the study manifest has a terminal, consumable record. Every frozen forecast record is create-only (`os.link`, as today), so nothing can be added or changed after scoring starts. The score attempt records the batch's record digests before its first outcome read.

### 4.4 Scoring once, and the report

- The WF-1B scorer and report are reused unchanged in their measures (MR0-MR16), N1 (R = 10,000) and layout, with Part A (descriptive) first. New Mode H families are added to the family registry with `mode: "H"` and windows equal to the ten targets; they are fixed in the study manifest before opening.
- **N1 seed:** RECOMMENDED: reuse the approved root `N1_ROOT_NIST_C2_20261031T1030Z_V1` unchanged. N1's streams are keyed by policy, root, game, replicate and target (`src/evaluation/n1_generator.py` lines 48-50), and no earlier report used any target at or after the holdout, so the Mode H targets get fair draws never generated before; the generator needs no change. Alternative: a fresh pre-announced pulse for Mode H, which would add at least one day.
- **Scored once:** one score attempt per game; a second attempt for the same batch is refused unless the first ended in a STOP before any outcome read.
- **Flags:** Powerball 1585 and 1586 carry `HOLDOUT_EXPOSED_HX1` in every per-target record and in the report; they are scored and counted in every measure like any other draw (no gap, nothing excluded); the flag is information only.
- **Words:** the report's plain-English summary describes any null result as "no statistically compelling departure from the fair-draw reference under the reported measures", never as proof of randomness. Ten targets give little power; the report says so.

## 5. Piece 4 - the weekly session (MH-1, OFF-1, EFF-1)

### 5.1 One command per game

`Run_Weekly_Session.bat --game G` (a new wrapper with the standard venv checks), in this order:
1. **Results update** (the owner's updater, a separate program, run by the wrapper as its first step, or by the owner just before; it is the only step that needs the internet). If it fails, the session stops.
2. **Catch-up**, in draw order: for every draw that has a result but no forecast, a walk-forward run of every released variant (each from the draws before it), frozen; then scored.
3. **Score the open forecast**, if its draw now has a result.
4. **Freeze and record the next draw's forecast** (target = last result + 1), so exactly one forecast per variant is always open.

### 5.2 Labels (OWNER Q3)

RECOMMENDED: every target after the holdout uses `run_mode` `FINAL_NEXT_DRAW` (reserved today, unreserved here), and the evidence tier is decided at freeze time by a fixed rule:
- `PROSPECTIVE`: frozen before the cut-off for its draw (section 5.3);
- `CATCH_UP` (a new tier): frozen after its draw, and the method revision was installed before that draw's date (MH-1);
- `DEVELOPMENT_WF_EXPLORATORY`: frozen after its draw, and the revision was installed later (MH-1: "otherwise ordinary walk-forward evidence").

The three are kept apart in every record and league table. Powerball 1587 and 1588 carry the exposure flag `HOLDOUT_EXPOSED_HX2` when caught up; they stay fully valid and counted (HX-2).

For the current cohort, Powerball 1587-1589 and Oz Lotto 1704-1706 fall before the releases of 31 October 2026, so they will be `DEVELOPMENT_WF_EXPLORATORY`; Powerball 1590 (5 November) and Oz Lotto 1707 (3 November) will be `CATCH_UP` if the install-date rule (OWNER Q5) accepts the 31 October installs.

### 5.3 The cut-off (OWNER Q4)

RECOMMENDED: a forecast is `PROSPECTIVE` only if its freeze time is before **00:00 Adelaide time on the draw's date** (derived from the era profile). This needs no knowledge of the exact draw hour, and it leaves each game a window of several days: Oz Lotto from Wednesday to Monday, Powerball from Friday to Wednesday.

### 5.4 The timing proof (OFF-1; supersedes R3 10.1(6), 10.2's push step and R3-D20 for this project)

- A local, create-only, digest-chained **forecast ledger** per game: `results/real/prospective/<GAME>/FORECAST_LEDGER_V1.jsonl`. Each freeze appends one line holding: the target and its derived date, the freeze time (UTC), the batch's roster with every run record's digest (including every registered but non-runnable method, by status; R3 10.3), the environment digest, and the previous line's digest. A line is appended only after every run record it names is frozen.
- Optional witnesses, never required: a GitHub push of the ledger, or an emailed copy of the newest line's digest. The report states which witness exists for each forecast; without one the label stays `PROSPECTIVE` (OFF-1), and the report says the timing rests on the local record.
- Proof strength (R3-D20's "must be tested"): a test shows that a ledger line edited, removed or reordered breaks the chain; a test shows that the session refuses to freeze a target whose cut-off has passed under the `PROSPECTIVE` label. What a local clock cannot prove (a deliberately wrong clock) is stated in the report.

**This design asks you to ratify that this section supersedes, for this project, R3 10.1(6), the "commit and push" steps of R3 10.2 and the push requirement of R3-D20** (as register v0.23 anticipates under OFF-1). R3's text is not edited; the register records the supersession.

### 5.5 Scores and the league table (EFF-1)

- A local, append-only **score ledger** per game (`SCORE_LEDGER_V1.jsonl`): one line per scored (variant, target), with the measures' per-target values, the outcome's source (master version and SHA-256; this is R3 7.6's "outcome ledger", finding A11), the label and any flag.
- The weekly path reads only the new runs and the new draw. The league table is built from the score ledger. N1 runs over the `PROSPECTIVE` and `CATCH_UP` draws only. Full rebatches use WF-1C's workers when it exists.
- The league table is cumulative and never retunes a method (MH-1).
- **Report cadence (OWNER Q6):** RECOMMENDED: each session prints a short after-draw note (the open forecast's scores and the new forecast) and writes the cumulative table to a file; the full report with N1 on request.

### 5.6 FINAL and "developed" (OWNER Q8)

RECOMMENDED: the weekly session **is** R3's FINAL_NEXT_DRAW protocol (R3 1.3 and 10) as amended by section 5.4, and your GOAL-1 declaration that the system is developed **is** R3's "explicit FINAL opening". The first `PROSPECTIVE` forecast follows that declaration, which follows Mode H. R3 10.1's other preconditions are already met or are met by this package (ratified scoring formulas; frozen released variants; the full roster listed; refreshed and digested sources; L identified; the ledger in place).

## 6. Piece 5 - the results update procedure (findings A6, A7, A8)

The updater's code is not changed by this design.
- **A6 (single source):** the project's production source is Lotterywest's results-search page only, an earlier owner decision. RECOMMENDED: record that R2-C03's "independent evidence" and the proposal's candidate-then-promotion step are satisfied in production by the updater's checks (the overlap with the master must match exactly; consecutive numbers; date rule) plus the owner's acceptance of each new version (A7); the owner's private, by-hand check of The Lott stays outside the repository and is never automated.
- **A7 (accepting a version):** a one-page owner checklist in the package: after each update, read the updater's printed summary (draws checked, draws added, warnings), then run the session; a STOP leaves everything as it is and comes to Claude. A stale lock, or a crash between the master replace and the ledger append, is reported, never repaired by hand without a reviewed procedure. The reader's chain check (section 2.2) refuses a master that disagrees with its ledger, so such a crash cannot be used silently.
- **A8 (the update window):** the default window (this month plus five back) overlaps the master while the session runs weekly; the checklist says to use `--months-back` to reach the master's last draw after any long break.

## 7. Packages and schedule

RECOMMENDED (OWNER Q9): **two code packages**, so Mode H is never held up by the weekly work, and any FB-1 slip touches only the second:
- **MHUP-A** (HIGH): section 2 (the version-2 reading rules), section 3 (study manifest and opening command), section 4 (Mode H batch, freeze rule, Mode H families, scorer ceiling), and the vocabulary row `REAL_HOLDOUT`.
- **MHUP-B** (HIGH): section 5 (`FINAL_NEXT_DRAW`, the labels, the forecast and score ledgers, the cut-off, the session wrapper) and the section 6 checklist.

| When (Adelaide) | What | Who |
|---|---|---|
| Mon 2 Nov | This design to the reviewer (EX_123) | You relay; reviewer reviews |
| Tue 3 Nov | Fixes; your ratification and answers to Q1-Q9 | Claude; you |
| Tue 3 - Wed 4 Nov | MHUP-A code, tests, mutation checks, rehearsals | Claude |
| Wed 4 - Thu 5 Nov | MHUP-A code review; Claude Code rehearsal (T016); install | Reviewer; you |
| Thu 5 - Fri 6 Nov | MHUP-B code; review; rehearsal; install | Claude; reviewer; you |
| Fri 6 - Sun 8 Nov | Approvals 1-4 per game; Mode H; your GOAL-1 decision | You |
| Sun 8 - Mon 9 Nov | First session, Oz Lotto: catch-up 1704-1707; forecast 1708 frozen before 00:00 Tue 10 Nov | You |
| Mon 9 - Wed 11 Nov | First session, Powerball: catch-up 1587-1590; forecast 1591 frozen before 00:00 Thu 12 Nov | You |

This is tight. Each review round that needs a recheck costs about half a day. **If any step slips past Friday 6 November, Oz Lotto 1708 slips to the following week (FB-1); Powerball 1591 has two more days.** I will say so the day it happens, not later.

## 8. Decisions

- **DECIDED** (owner, register v0.23): MH-1, OFF-1, EFF-1, HX-1, HX-2, FB-1, GOAL-1, ORD-1, TSC-1; the holdout ranges; one master per game; the updater's code and the two-site checker unchanged.
- **RECOMMENDED** (for the owner, after review): Q1 Reading A; Q2 the combined master; Q3 the labels and `FINAL_NEXT_DRAW`; Q4 the cut-off at 00:00 Adelaide on the draw date; Q6 the report cadence; Q8 FINAL and "developed"; Q9 two packages; the N1 seed reuse (section 4.4); the R3 supersession (section 5.4).
- **OPEN, for the owner:**
  - **Q5 (install dates for CATCH-UP):** OFF-1 says validity is checked against local install records, not Git. None exist for installs so far, and the registry's `effective_date` is the release package's build date, not its install date. RECOMMENDED: from MHUP-A on, every install's COMMITTED step writes a create-only local install record; for the current cohort, a one-off record carries the install dates the register already records (31 October 2026 for REL-1 and E_1 revision 2), which you confirm when the session first runs.
  - **Q7 (the display rule after opening):** today nobody may display or compute with Powerball 1577 or later or Oz Lotto 1694 or later. After a game's holdout is opened and Mode H scored, those draws become ordinary history for training and scoring. RECOMMENDED: from then on, the rule for that game becomes "no lottery-results searches, no results websites, and no draw outcomes pasted into the chats except inside report text you choose to share"; until you decide, the rule stays exactly as it is.
- **Not in scope:** result corrections (R3 10.3), WF-1C, Method A's diagnostics, any change to the updater or the two-site checker.

## 9. Not tested, and what the code round must show

Nothing here is implemented or tested. The code round must show: the chain and prefix tests (section 2.2); T-05 on a grown synthetic master; the Mode H batch refusing without a valid opening record, with a mismatched study manifest, with a changed environment, and a second time; the scorer refusing before the batch is complete and a second time; the forecast ledger's chain and cut-off tests; mutation checks for each rule; LF and CRLF rehearsals; a Claude Code rehearsal on Windows. All tests on invented data; none reads a holdout result.

*End of design v0.1.*
