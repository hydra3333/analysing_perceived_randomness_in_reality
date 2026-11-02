# Stock-take answers: where we are heading (v0.2)

Claude (the new Claude chat), 2 November 2026. v0.2 applies ChatGPT's six corrections and the previous Claude chat's additions (see the discussion record STOCKTAKE_2026_11_02); the changes are listed at the end. For understanding only. This approves nothing and specifies nothing new. Where it goes beyond what is built or decided, it says PROPOSED (my suggestion, mostly from design v0.1 in EX_123, which has not yet been reviewed) or OPEN.

Labels: **BUILT** working now; **DECIDED** agreed, not built (with the register ID or document); **PROPOSED** my suggestion; **OPEN** not decided. Times are marked (measured) or (estimated). No outcome of Powerball 1577 or later, or Oz Lotto 1694 or later, appears here. Dates of future draws come from the weekly calendar rule in the game profiles, not from any result.

Terms used throughout:
- **Variant:** one fixed setting of a method. 40 variants are released today (E_1 and eleven other methods, most with three or six settings each).
- **Walk-forward:** forecasting a past draw using only the draws before it.
- **The holdout:** ten draws per game sealed since 1 August 2026: Powerball 1577-1586, Oz Lotto 1694-1703.
- **Mode H:** the one-time test on the holdout.
- **The register:** `doc/RATIFICATION_REGISTER_v0_23.md`, the record of every decision.

---

## One-page summary

**1. Aim.** To test, as carefully as possible, whether Australian Powerball and Oz Lotto results hold any pattern that conventional statistics might have missed, using a catalogue of 62 methods from simple counting to pilot-wave-inspired ideas. The most likely result is that nothing works; a carefully measured "nothing" is a good result, and the real test is forecasts made before the draw.

**2. Working now (BUILT).** 40 variants of 12 methods, released in both games. A walk-forward driver that has run every variant over every development draw (Powerball 17,280 runs, Oz Lotto 8,760). A scorer and ranking report, with a fair-draw simulator (N1) seeded from a NIST random pulse. 471 tests. The first reports: under the reported measures, nothing in either game departs convincingly from what fair draws give.

**3. Left to build, in order.**
1. The version-2 results reader (DECIDED needed: register v0.23 probe A1; design PROPOSED in EX_123 section 2). Without it, one results update stops everything: **even an update that finds nothing new writes a NO_CHANGE line to the ledger, and that alone makes every batch, run, report and install refuse. Do not run the updater in any form until this is installed.**
2. Opening the holdout: a frozen study plan and the opening record (DECIDED in outline: R3 6.2 and register v0.23; detail PROPOSED).
3. Mode H: forecast and score the ten holdout draws per game (DECIDED: register v0.23 GOAL-1, HX-1).
4. The weekly session: catch-up, scoring, and the next forecast, offline (DECIDED inputs: MH-1, OFF-1, EFF-1; detail PROPOSED).
5. Then WF-1C (parallel workers), wave 3 (including your Method B as E_45), and the later waves (DECIDED order: ORD-1, roadmap).

**4. A normal week (PROPOSED shape; MH-1 decided the order).** One sitting, both games, any day from Friday to Monday. You run the results update (internet, about a minute). Then one command per game: it catches up any draw with a result but no forecast, scores last week's forecast, and freezes this week's forecast for the next draw. About 40 forecasts per game per week; a few minutes per game (estimated). No approval needed inside a routine week.

**5. Decisions needed from you, and when.**
- After the reviewer's reply to the design (expected 3 November): nine questions, Q1-Q9 in EX_123 section 8, each with a recommendation. The important ones: Q1 what "frozen before opening" means; Q4 the deadline for a prospective forecast; Q8 that the weekly session is R3's FINAL mode and your "developed" declaration is its opening.
- Before Mode H (PROPOSED plan: about 10-14 November; 6-8 November only as a stretch): four separate approvals per game: freeze the study plan and open the holdout; the first results update; the Mode H batch; the Mode H scoring.
- After Mode H: whether to declare the system developed (GOAL-1).

**6. What looks needlessly complicated (quick view).**
- Three evidence labels for post-holdout draws (prospective, catch-up, development) are needed, but the rule deciding them must be simple and printed in every report, or nobody will trust the tables.
- Four separate approvals before Mode H is a lot of ceremony for one game; they protect real gates, but I would like them to be four lines in one session, not four days.
- The install verifier, suite runner, mutation tool and Windows rehearsal for every code package are heavy. They have caught real faults (T012-T015), so I would keep them, but the two Mode H packages should be the last ones that touch the readers for a long time.
- The number of overlapping documents (R3, the register, H-1, the roadmap, the reminders) is itself a cost. The register is the one that counts; the rest point to it.

---

## (a) Mode H, the one-time holdout test

**What it is (DECIDED: R3 sections 6 and 10; register v0.23 "Terms for that design").** Every released variant forecasts each of the ten holdout draws of a game, each forecast using only the draws before its target. The forecasts are frozen, then the ten draws are scored once with the same scorer and measures as the development reports.

**What is frozen before any holdout result is read (PROPOSED, EX_123 section 1, Reading A; OPEN until you decide Q1).** The register's wording says "all frozen before the holdout is opened" and also "walk-forward". Both cannot hold literally: the forecast for Powerball 1578 must train on draw 1577, which is itself in the holdout. My recommended reading: open the holdout and add the results first; then run the Mode H batch, where each method still sees only the draws before its own target (the N-1 rule, which test T-05 proves); then, and only then, let the scorer read any holdout result. Two alternatives are to be weighed in the design review, not chosen here. **B:** release one result at a time, forecast, score, repeat; literal, but needs a new step engine. **C** (raised by the previous Claude chat): forecast all ten holdout draws from the development draws only (Powerball up to 1576, Oz Lotto up to 1693), freeze, then open and score; literally "frozen before opening" and needing only a cap on the reader's history, at the cost that forecasts for the later holdout draws do not see the earlier ones; the ordinary catch-up over the same ten draws then follows as the first weekly steps, flagged. Q1 stays OPEN until the review and your decision.

**Frozen before opening, in any reading (PROPOSED, EX_123 section 3.1):** the study plan: which variants, which measures, which seed, the exact code and the exact list of installed packages (R3-T50, which forbids any software upgrade inside Mode H).

**Kept to one run (PROPOSED, EX_123 sections 4.2-4.4):** one Mode H batch per study plan per game; a second plan is refused. One scoring attempt; a second is refused unless the first stopped before reading any result. Every record is create-only (the file system refuses to overwrite), as all frozen records are today (BUILT).

**Flagged draws (DECIDED: HX-1 and HX-2, exposure record v0.3).** The record's item 1 says a reviewer chat displayed Powerball 1585-1588 on 25 October 2026. Of those, 1585 and 1586 are inside the holdout: they carry a flag in Mode H's records and report. 1587 and 1588 are after the holdout: they carry the same flag when the weekly catch-up scores them. Item 5 notes that ratified documents quote draw 1587 as drawn-order evidence; it gets no Mode H flag because it is outside the holdout. **Why flagged draws still count:** the flag records that a reviewer saw those results; no method was changed because of them, so the forecasts are not tainted, and leaving draws out would make the result less honest, not more (your rule: mark, never suppress). The flag is information; it changes no score.

**What Mode H can and cannot show.** Ten draws per game is a small test. It can catch a method that was secretly tuned to the development draws (it would collapse on fresh ones) and it gives the first honest fresh-draw numbers. It cannot show a small real effect; with ten draws almost any method looks consistent with chance. The real test is the weeks that follow. **Afterwards (PROPOSED, EX_123 Q7; OPEN):** the ten draws become ordinary history for training and scoring, like any other past draw.

## (b) Re-training, and keeping old results honest

**What is recalculated for each forecast (BUILT; DECIDED: R3 section 10 "Fitting", H-1 5.2 "fresh fit for every target").** Every forecast is computed from scratch from the draws before its target. No model is stored between targets. What each of today's methods looks at:
- E_1 all earlier draws (counts). E_2 all earlier gaps (or the last 8). E_6, E_7, E_9 all earlier draws, with some variants weighting older draws less. E_8 periods of 13, 26 or 52 draws. E_3, E_4 a moving window of 52 or 104 draws. E_10 a short window against a long one. E_17, E_18, E_19 all earlier draws (gaps, ages, cycles).
- Future methods: each is designed before coding, and its window is fixed in its specification (E2R-R14A). Nothing beyond today's 12 methods is designed (OPEN). Any cache or incremental fit would need a reviewed proof that it gives byte-identical forecasts (DECIDED: R3 10).

**Can anything alter an earlier frozen forecast, score or ranking? (BUILT: no.)** Forecast records are create-only and each carries a digest of its content. New results cannot change them: a forecast for draw N depends only on draws before N, and test T-05 checks that changing N or later draws leaves every forecast byte-identical. A software change to a released method is a new revision with its own identity; the old forecasts keep the old identity (DECIDED: E2R-R14A, R3 6.3). A published ranking report is a committed file; a new report is a new file. **Reproducing earlier findings:** every run record pins the results file version and digest, the method revision, the variant and the code; rerunning the same inputs gives the same bytes (BUILT and tested across Windows and Linux for the scorer).

**Re-running history (DECIDED: R3 10.4; H-1 5.2).** Allowed for debugging, for a new method revision, or for a full re-batch (which WF-1C will make faster). Every rerun gets a new run identity and is labelled RETROSPECTIVE or as development evidence; it never acquires the original's pre-draw standing, and the original stays on disk.

## (c) Catch-up and missed weeks

**Confirmed (DECIDED: MH-1).** Catch-up forecasts each missed draw separately, in draw order, each from only the draws before it: predict N, reveal N, score N, then move to N+1. This is exactly today's walk-forward (BUILT), applied to draws after the holdout.

**Labels (DECIDED in substance: MH-1; mechanics PROPOSED, EX_123 section 5.2).** PROSPECTIVE: frozen before its draw. CATCH-UP: made after its draw, in order, and valid only if the method revision was installed before that draw's date. Otherwise the forecast is ordinary development evidence. **Which rankings:** the cumulative league table ranks PROSPECTIVE and CATCH-UP draws, kept apart, side by side; development results are a separate table (DECIDED: MH-1, R3 17). For the current cohort: Powerball 1587-1589 and Oz Lotto 1704-1706 fall before the releases of 31 October 2026, so they will be development evidence; Powerball 1590 (5 November) and Oz Lotto 1707 (3 November) qualify as CATCH-UP if the install-date rule accepts the 31 October installs (OPEN: Q5, because no local install records exist yet; OFF-1 says validity is checked locally, not from Git).

**Missed weeks.** The catch-up covers any number of missed draws, one game or both; each caught-up draw joins the history for the forecasts after it (DECIDED: MH-1). Missing a forecast deadline simply means that draw is caught up instead of forecast prospectively; the record shows the gap (DECIDED: R3 10.5, "report missing weeks rather than silently skipping them"). Nothing is lost except the pre-draw standing of that one week.

## (d) Your weekly routine

**One sitting, Friday to Monday, both games: workable (PROPOSED).** Powerball is drawn Thursday, Oz Lotto Tuesday. From Friday to Monday, Thursday's Powerball result is available and both next draws are ahead. **Latest freeze (PROPOSED, EX_123 Q4):** before 00:00 Adelaide time on the draw's date. So Oz Lotto's forecast by Monday night; Powerball's by Wednesday night. In a Friday-Monday sitting both are comfortably met.

**The steps (PROPOSED shape; MH-1 decided the order).**
1. You run the results update (`Run_Results_Updater.bat update --games POWERBALL,OZLOTTO`). Internet. About a minute (estimated; a headless browser with two-second pauses). It prints what it checked and added. No approval after the first run (DECIDED: the first run needs your separate approval; later runs are routine).
2. You run the weekly command for Oz Lotto. The software: catches up any draw with a result but no forecast (40 runs per draw, about 10-15 seconds per draw, estimated from one batch of 17,280 runs in 80 minutes; fine for planning, not a promise); scores the open forecast; freezes the forecast for the next draw and appends it to the forecast ledger. Offline. No approval.
3. The same for Powerball.
4. Optionally, you commit and push the two ledgers as an outside witness (OFF-1: optional).

**Which methods, how many forecasts.** Every released variant: 40 per game today, so about 80 forecasts a week, more as waves are added. **Today's tools:** the walk-forward driver stays as the engine of catch-up and of any full re-batch (with WF-1C's workers); the ranking report stays for the full report with the fair-draw simulator, on request or monthly (OPEN: Q6 cadence); the weekly command prints a short note and the cumulative table (PROPOSED).

**An invented session (Saturday 14 November 2026, after Mode H and your "developed" declaration).** You run the update: it reports Powerball draw 1591 added (drawn Thursday 12 November), Oz Lotto nothing new. You run the Oz Lotto command: no catch-up needed; the open forecast for 1708 was scored last week; it freezes the forecast for 1709 (Tuesday 17 November) at 10:42 and appends the ledger line. You run the Powerball command: the open forecast for 1591 is scored against the new result and the league table updates; the forecast for 1592 (Thursday 19 November) is frozen. **If one result is not available yet** (say Lotterywest has not yet published Thursday's draw): the update reports no change for Powerball; the Powerball command finds the forecast for 1591 still open and leaves it open; it cannot freeze 1592 because 1591 is not yet history, so it does nothing more and says so. You rerun it later in the week once the result is in; the 1592 forecast is still prospective if frozen before Thursday.

## (e) Changing or adding a method

**The steps (BUILT process; `doc/METHOD_TEMPLATE/README.md` draft 4).** You start it by naming the idea and its catalogue number (E_2 to E_62 are reserved names; a new idea beyond them is OPEN and needs a catalogue amendment). Then: a short specification, reviewed and ratified, fixing every variant setting; one code package (installed non-runnable, with a flag file that makes every run refuse); a release package (deletes the flag and appends a "supported" registry entry); then it joins the next walk-forward batch you authorise, and a report.

**Catch-up and its prospective record (DECIDED: MH-1; R3 6.3, 10.4).** A new method's history is development evidence: a full walk-forward over all past draws, including the post-holdout ones, labelled as such. Its CATCH-UP record can begin only at draws after its install date; its PROSPECTIVE record begins at its first forecast frozen before a draw. An improved version is a new revision with a new identity and starts its own record; the old revision's results stay under the old identity, so an improvement is never credited with earlier results.

**Fair comparison with different history (DECIDED: R3 6.3, 6.4; BUILT in part).** The report shows each method's results over the draws it actually forecast, with the number of draws beside every figure. Side-by-side comparison uses the common draws. Version-stratified results (one unchanged method across its draws) and the evolving-portfolio view (what the project forecast each week) are reported separately and never mixed.

## (f) What you will see

**One forecast (BUILT; invented example).** For Powerball, variant `E_6:BETA_FORGET_1Y_V1` (invented name), target 1592: a full ranking of the 35 main numbers and of the 20 Powerball numbers; TOP = the seven best main numbers plus one Powerball, say `[3, 9, 14, 22, 27, 31, 35]` with PB 8; WORST = the seven lowest plus the lowest Powerball. **Scoring (BUILT):** after the draw, how many of TOP's seven match the drawn seven (0-7), whether the Powerball matched, the same for WORST, the prize division each would have won, and the rank position of each drawn number in the method's ranking. The report compares these with the fair-draw reference (an average of 1.4 matches of seven for Powerball) and with 10,000 simulated fair-draw histories (N1).

**Where things are saved (BUILT for development; PROPOSED for the rest).** Run records under `results/real/development/` (development) and, PROPOSED, `results/real/holdout/` and `results/real/prospective/<GAME>/` with a forecast ledger and a score ledger. Reports under `results/method_rankings/`. The one search log at `results/audit/SEARCH_LOG.csv`. Results files under `source_data/`.

**The league table (DECIDED: R3 17, MH-1).** One row per variant, with its measures and the number of draws; development, Mode H, catch-up and prospective kept in separate tables or columns, never pooled; a hindsight-advantage column where in-sample figures appear. Made by the weekly command (short form) and by the full report on request (PROPOSED).

**Which numbers matter.** For a track followed for many weeks: the family-level figures (Bonferroni P and the N1 maximum P), which allow for the number of variants tried; a single variant's p-value is one of 80 and looks small by chance about once in 80. **Telling signal from fluke, over-tuning and self-made pattern (DECIDED: H-1 2A, the four origins PO-1 to PO-4):** a fluke fades on fresh draws; over-tuning shows as development results that Mode H and prospective draws do not repeat; a method's own structure shows up in the fair-draw simulator too (N1 runs the method's scoring against invented fair histories, so a pattern the method creates appears there as well). Only persistence on genuinely new draws (PO-4) counts.

**Genuinely encouraging (my view, PROPOSED as a standard, not a rule).** A predeclared track whose prospective family-level P stays below about 0.01 after allowing for every variant, and whose effect size is stable across the prospective weeks, not carried by one lucky week. **How long (an illustration, not a power calculation and not an expected timeline):** a real effect large enough to matter (say one extra match of seven every few draws) might show in roughly 50-100 prospective draws, one to two years at one draw a week per game; the true number depends on the effect size, the measure, its variance, the number of variants compared and the chosen thresholds, and a small effect would take far longer. Ten holdout draws or a handful of weeks can only rule out large effects.

## (g) New results coming in

**How (BUILT: `src/results_master_v0_1.py`, run by `Run_Results_Updater.bat`).** Confirmed: it reads only Lotterywest's results-search page on `www.lotterywest.wa.gov.au`, with a real headless browser and two-second pauses; no other site, no API, no automation of The Lott (DECIDED: TSC-1 retires the two-site checker). It checks: every draw in the fetched window that overlaps the master matches it exactly, draw numbers are consecutive, dates follow the weekly rule, and no draw is from the quarantined range unless the opening record exists. It keeps a copy of what it fetched and a backup of the previous file, and appends one ledger line per run. **The launcher does not refuse a bare run:** `Run_Results_Updater.bat` with no arguments runs `update` with its default six-month window. It is the Python tool that then refuses, and only while the holdout is closed and the window reaches 1 August 2026. Once the holdout is opened, a bare run is a real update. Always give the arguments.

**Confirmed: after any update, everything refuses (BUILT behaviour; probe A1).** The reader, the walk-forward driver, the outcome reader and the report all require the ledger to be exactly one line, the original INIT line. After an update the ledger has two lines, so every new batch, every method run and every report refuses before writing anything. Some accepted tests read the real results file through that reader, so the test suite would fail, and every install's suite step would STOP. **What does not refuse:** nothing in the project. The updater itself still works (it only checks its own ledger), and the earlier committed records remain readable as files. **The version-2 fix (PROPOSED, EX_123 section 2.2):** accept a ledger of any length whose lines chain correctly (INIT, then UPDATE or NO_CHANGE rows that agree with each other), and check a run's pinned version by hashing the first lines of the current file, which works because the updater only appends. It must be installed first because the first update makes the whole system unusable until it exists.

**Tied to the exact results version (BUILT, extended).** Every run record and every report pins the results file's version number and its SHA-256 digest; the version-2 reader keeps those pins valid after later updates, and refuses if any earlier line of the results file has changed.

**Offline (DECIDED: OFF-1).** Yes. Only the update needs the internet. Everything else runs from the PC.

## (h) Offline, proof of timing, and backups

**Showing a forecast was frozen before its draw (PROPOSED, EX_123 section 5.4; supersedes R3's push requirement once you ratify it; R3-D20 is OPEN until then).** A per-game forecast ledger: one line per freeze, with the target, its date, the freeze time, the digest of every forecast record in that batch, and the digest of the previous line, so the lines form a chain. Every line and every record is create-only. A test shows that editing, removing or reordering a line breaks the chain. **Protection from accidental change:** create-only files, the chain, and (DECIDED: register v0.23 R-011) a Git rule that stops Windows line-ending conversion under `results/`.

**What local records prove, and what needs a witness.** Locally: that the records agree with each other, and that nothing changed since the chain was last checked or anchored. A chain on its own cannot prove the PC's clock was right, nor that the whole chain was never rewritten before it was first anchored. A GitHub push or an emailed digest of the newest ledger line proves to an outsider that the line existed before the draw. Under OFF-1 the witness is optional; the report says which witness exists.

**If GitHub disappeared (DECIDED: OFF-1, your 31 October principle).** You need your repository folder with its `.venv`, the results files under `source_data/`, and the `results/` folder. Everything runs. You would lose: the public record and the easy way of passing packages between the chats (they could travel as zips); the install verifier's "committed" phase as written (it checks Git commits, which still works locally). Changing methods would still work: Claude builds a package, you install it into your local repository.

**Backups (PROPOSED). A GitHub push is not a backup of the irreplaceable records**, because these are deliberately ignored by Git and exist only on your PC:
- `results/real/development/contract_runs/` (every frozen run record);
- `results/real/development/wf_batches/**/attempts.jsonl`;
- `results/real/development/scores/` (the scoring ledgers behind the reports);
- after the first update: `source_data/backups/` and `source_data/grabs/`;
- later: the holdout run records and the prospective forecast and score ledgers, wherever the design puts them.
Pushed, so GitHub holds a copy: the six files in `source_data/`, the report files, the search log, all code and documents. **Habit:** after every weekly session, copy `source_data/` and `results/` to a second drive; before every install, copy the whole repository folder; make the first copy now. The weekly instructions will carry the exact list.

## (i) Approvals and roles

**Routine once running (PROPOSED):** the weekly update, the weekly command, pushing ledgers, reading reports.

**Your approval every time (DECIDED: H-1 sections 1.5 and 11; register):** opening the holdout and the first update; each Mode H batch and scoring; declaring the system developed; every new method's specification, code install and release; any dependency upgrade (then the full suite before anything scientific); any safety switch or allowlist change; any destructive or Windows lifecycle test; any clearance of the orphan marker; any full re-batch or full report on real data; any amendment of a ratified document.

**Who may do what alone.**
- **Claude:** design, code, tests, packages, documents; commits only in `exchange/` and `CLAUDE_CODE_WORKING_FOLDER_TREE/`. Never: open data folders, run anything on real data, change a gate, clear the marker, change `src/`, `tests/`, `doc/`, `review/` or the data folders directly (those change only through packages you install), name you, search for lottery results.
- **ChatGPT (reviewer):** independent review, reproduction of offline tests, competing designs, routine review decisions labelled REVIEWER-DECIDED. Never: commit, run real data, authorise anything.
- **Claude Code (local runner):** carry out a task file in a throw-away clone that cannot push; commit its report. Never: design, fix, run the launchers, update results, access the data folders, push.
- **You:** ratify, authorise every run, install, commit the main tree, push.

## (j) When things go wrong

**What happens (BUILT; H-1 "a STOP is a STOP").** Every tool checks before writing and refuses with a reason. Completed records are protected (create-only), but not every operation is one atomic step: the updater writes the backup, then replaces the results file, then appends the ledger line, so an interruption between the last two leaves a results file that does not match its ledger. The next run detects that and refuses, pointing at the backups; recovery is manual and follows a procedure (to be written in the Mode H design, probe A7).
- Results site changed or down: the updater prints STOP or an error; the results file is untouched; try again later; if the page layout changed, Claude writes a reviewed fix.
- Invalid results (a fetched draw disagrees with the master, a gap in numbers): the updater refuses, keeps the fetched copy for inspection, changes nothing.
- Line-ending damage (as with the first Powerball report): the tool refuses because bytes differ from the record; you restore the committed bytes (the procedure in H-1 section 6); the new `results/` rule prevents a repeat.
- An interrupted run: the walk-forward driver resumes from its records; a run that stopped is recorded as stopped and never retried silently.
- A failed check in an install: STOP; you send the output; nothing is committed.
- The orphan marker: every launch refuses for both games; only your approved manual procedure clears it (DECIDED: binding).

**Recovering safely.** Stop; copy the output to Claude; do nothing else. **Never:** delete or edit a record, clear the marker or a lock by hand without the reviewed procedure, rerun with different arguments to "get past" a refusal, run the updater bare, or run anything that reaches the holdout before Mode H.

**Resuming an interrupted week (BUILT in part; PROPOSED).** Yes. The driver already resumes a batch from its records without redoing completed runs. The weekly command would do the same: it reads the ledgers, finds what is still open, and continues; accepted records are never rewritten.

## (k) Timeline, and what "done" means

**Before the first genuine forecasts (PROPOSED schedule, EX_123 section 7; FB-1 decided).** In order: the design reviewed and ratified (2-3 November); package A (version-2 reader, opening, Mode H) coded, reviewed, rehearsed on your PC, installed (3-5 November); package B (the weekly session) the same (5-6 November); your four approvals per game, the first update, Mode H run and scored (6-8 November); your "developed" decision; the first session with Oz Lotto 1708 (10 November) frozen before midnight Monday 9 November, and Powerball 1591 (12 November) before midnight Wednesday 11 November. **Realistic? No, not as a plan.** It needs every review round to pass first time, and the snapshot alone took four rounds. **PROPOSED honest plan:** Mode H done and the weekly session installed by about 13-15 November, so the first prospective forecasts are Oz Lotto 1709 (Tuesday 17 November) and Powerball 1592 (Thursday 19 November); 9-12 November stays a stretch only. Nothing is lost: Oz Lotto 1707-1708 and Powerball 1590-1591 are caught up in the first session as CATCH-UP draws, exactly as MH-1 intends. **Under FB-1:** nothing is rushed; the missed draws are caught up in the first session and labelled CATCH-UP, so no draw is lost from the record.

**"Developed and operational" (DECIDED: GOAL-1; detail PROPOSED).** It means: the released methods have been run through Mode H and the weekly session works end to end on your PC; from then on every week's forecasts are frozen before their draws and scored after. It does not mean any method predicts anything: the expected result is still that none does. It does not mean the catalogue is finished: waves 3 to 11 and the ensembles keep being added afterwards, each starting its own record.

## Changes from v0.1

ChatGPT's six points (all accepted): Q1 kept OPEN with options A, B and C to weigh (section a); the bare launcher runs an update (g); interruptions can leave the results file and its ledger inconsistent, detected on the next run (j); the local chain proves consistency, not clock time, and a push is not a backup of the git-ignored records (h); the 50-100 draw figure is an illustration (f); 9 November is an aspiration (k). The previous Claude chat's additions: the NO_CHANGE warning (summary 3); the backup list (h); option C (a); the honest target date (summary 5, k); the two wording slips (per-draw time in d; what Claude never changes in i).

*End of stock-take answers v0.2.*
