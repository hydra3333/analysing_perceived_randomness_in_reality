# Direction for the operational procedures, v0.3r1 (CANDIDATE)

Plain English. First written by the Claude web chat on 2 November 2026 from the owner's part (d) of the
stock-take record (STOCKTAKE_2026_11_02), as amended by Responses 3, 3b and 2 and accepted by the owner that
day; v0.2 and v0.2r1 applied the ChatGPT reviewer's content check and focused recheck. **v0.3** (4 November
2026, by the replacement Claude chat, for the reviewer's content check) brings it up to date with the
ratified MHUP-1 design (MHUP-R, 3 November 2026), the owner's naming decision LW-1, and the owner's
decisions of 4 November 2026. It keeps the owner's objectives and says plainly where the ratified design
delivers them differently or later. It is a direction statement, not a specification: the design and the
ratification register hold the exact rules, and they prevail wherever this file is looser. **v0.3r1** (4 November
2026) applies the reviewer's focused RECHECK of v0.3 (C01 to C03, O01, O02).

**Status and authority:** CANDIDATE v0.3r1, for the ChatGPT reviewer chat's focused recheck and the owner's
ratification; v0.2r1 (owner-ratified operational direction, DIR-1, 2 November 2026) stays in force until
then. This is not an implementation specification and not permission to run any command, access the holdout
or update results. The independently reviewed and owner-ratified designs, the method and process safety
gates, and the separate execution approvals remain binding. No real-data operation is authorised by this
document.

Codes such as MH-1, OFF-1, HX-1 and MHUP-R identify owner decisions recorded in the ratification register;
R3 and E2R name ratified specifications; "the design" is
`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md`. Each point is marked: (ratified) an
owner decision in the register, with its ID; (owner, 4 Nov 2026) an owner decision of 4 November 2026, to be
recorded in register v0.25; (objective) what the owner wants, with how far the ratified design delivers it;
(deferred) agreed, but planned for later; (open) still to be decided.

## 1. What will be in place

- The software; the two results files (one per game, Powerball and Oz Lotto, never pooled); for every method
  revision, its forecast for every draw it was eligible to forecast, in draw order, frozen when made; the score
  of every forecast once its draw is known; and the ranking reports and league tables. A forecast made later
  for an earlier draw is a new record and never acquires pre-draw standing. (ratified: R3, R3 10.4)
- The clock is the draw number within each game: draw numbers define the scientific sequence and every
  training boundary. Dates serve the checks around it: validating incoming results, the deadline and timing
  evidence of a forecast, release eligibility and audit records. (ratified: R3 1.1)
- Every forecast for draw N is calculated fresh from the draws before N, never from a stored model. Each method
  follows its own fixed rule about how far back it looks: most look at all earlier draws, a few are defined to
  look at a window (for example the last 52 or 104 draws), because how far back to look is part of what that
  method is. (ratified: R3 10; E2R-R14A)
- After every draw, the forecasts for it are scored, and the rankings are refreshed as new dated tables.
  (ratified: R3 17; MHUP-R, design 6.6)

## 2. The three kinds of record, and what may change

- **Forecasts** are frozen and never changed or replaced. A later rerun of the same target is a new record with a
  new identity and no pre-draw standing. (ratified: R3 10.3, 10.4)
- **Scores** are kept as accepted. No forecast receives a second routine accepted score under the same scoring
  contract. If a scorer fault or a new measure needs it, a new scoring run is added beside the old one under its
  own identity and provenance; the old one is never edited. (ratified: ST-1, ST-2 as read in register v0.24)
- **Rankings** (league tables, reports) are views of the frozen records and are meant to change: when a draw is
  scored, a method added or retired, or the comparison window changed, a new dated report is made. Every old
  report stays as published. "Re-ranking" means a new report, never an edit. (ratified: ST-1, D-8, R3 17)

## 3. Labels on every scored draw

- PROSPECTIVE: the forecast was frozen before its draw's deadline: 00:00 local time on the draw's date. A
  forecast set is only started with at least one hour to spare, so in practice by 23:00 the evening before.
  (ratified: MHUP-R, Q4; design 6.4)
- CATCH-UP: made after its draw, in draw order, from the draws before it, by a method revision **released**
  before that draw's date. Installing code is not releasing it: the date that counts is the release record's
  local date, written when the revision becomes runnable. Counts in the rankings, kept apart from PROSPECTIVE.
  (ratified: MH-1; MHUP-R, Q5, design 4.3; owner, 4 Nov 2026)
- Development evidence: everything else (the walk-forward over past draws, a new method's back-history, a
  draw dated on or before its method's release). Ranked in its own table. (ratified: MH-1, R3 17)
- LATE_PRE_DRAW: an operational category for a forecast frozen after the deadline but before the result was
  accepted; scored, kept and shown, never counted as evidence of any label. MISSING_BATCH: a mark on a draw's
  record for an eligible variant that missed its pre-draw freeze; that variant's later catch-up forecast for the
  draw counts as CATCH-UP. (ratified: MHUP-R; design 6.4, Appendix I)
- Mode H results carry their own label and family, never pooled. Powerball 1585 and 1586 carry an exposure flag
  within Mode H. Powerball 1587 and 1588 are post-holdout draws and carry the same flag when the weekly pass
  evaluates them; for the methods released on 31 October 2026 their results are development evidence, not
  CATCH-UP. All flagged draws are fully scored and counted. (ratified: HX-1, HX-2 as read in register v0.24)
- Same arithmetic for all; only the label and the table differ. The label is what lets an outsider see which
  forecasts were genuinely made in advance. A forecast's publication status (published before the draw, or
  timeliness unverified) is worked out when a report is made, from the witness record (section 9).
  (ratified: MHUP-R, design 6.5)

## 4. Mode H, the one-time holdout test

- Every released variant forecasts each of the ten sealed holdout draws per game (Powerball 1577-1586,
  Oz Lotto 1694-1703), each from the draws before its target. Every planned pair reaches DONE, including a run
  that fails and is counted as missing; every successfully published forecast is frozen create-only. Only once
  the whole batch is complete are the ten targets scored once and the study sealed. (ratified: MHUP-Q1 option A,
  MHUP-R; design 5.2)
- The statement Mode H supports: "a locked holdout study: the study plan, the code and the environment were
  frozen before the holdout was opened; every forecast used only draws before its target; all planned attempts,
  and every successfully published forecast, were frozen before any scoring process read a holdout outcome."
  It is a precommitted holdout evaluation, not pre-draw forecasting: the outcomes are already in the system
  when the forecasts are made, held away from the methods by the N-1 reader. (ratified: MHUP-R)
- Each step is the owner's separate approval, per game: (1) freeze the study plan and open the holdout;
  (2) the first results update, which must bring in every holdout draw or write nothing; (3) the Mode H batch;
  (4) the scoring, the report and the seal. Between steps 2 and 4 the updater refuses for that game.
  (ratified: MHUP-R, MHUP-D1, MHUP-B04; design 4.4)
- Ten draws per game give limited statistical power; the report says so, and describes a null result as "no
  statistically compelling departure from the fair-draw reference under the reported measures", never as
  proof of randomness. Afterwards the ten draws are ordinary history. (ratified: MHUP-R, design 5.4)
- Whether the rule against displaying holdout draws in the AI chats is relaxed after Mode H. (open: Q7, to be
  decided before step 2; until then nothing changes)

## 5. The normal week

One sitting per week, both games, any day from Friday to Monday; the Oz Lotto session must start its forecast
for the Tuesday draw by 23:00 on the Monday if that forecast is to count as PROSPECTIVE. (agreed 2 Nov 2026;
design 6.4)

1. Run the results updater with its arguments, both games (the only step that needs the internet). It reads
   only Lotterywest-GOV: the official Western Australian Government Lotterywest website, over HTTPS, at
   exactly `www.lotterywest.wa.gov.au`, with no fallback of any kind; `oz.lotterywest.com` and The Lott are
   never contacted. It fetches the current month and the five before it; it refuses unless the fetched draws
   overlap and match the file it already holds, and new draws are consecutive. Run bare, it still runs an
   update, so it is never run bare. It refuses while a weekly session is running. (ratified: LW-1, MHUP-C03,
   MHUP-B04, TSC-1)
2. If the updater (or anything else) STOPs, nothing is retried automatically. The output comes to Claude, who
   diagnoses it and proposes the recovery; the owner authorises each retry. (owner, 4 Nov 2026)
3. For each game, one command (`Run_Weekly_Session.bat --game G`). It prints a status block first: last accepted
   draw, last forecast, last scored draw, backlog, any open forecast, next target and its deadline, number of
   active variants, the label each target will get. (ratified: MHUP-R, design 6.1, 6.2)
4. The command then works through the outstanding draws strictly in draw order. For each one whose result is
   accepted: if a forecast for it already exists, it scores that forecast; if not, it makes a catch-up forecast
   from the draws before it, freezes it, then scores it, with the right label. Only then does it move to the
   next draw. When no outstanding draw is left, it freezes the forecast for the next draw, if at least an hour
   remains before that draw's deadline, and appends it to the forecast ledger. A draw whose result is not yet in
   is left open, never skipped and never guessed. (ratified: MH-1, MHUP-B02; design 6.3)
5. At most one open forecast per active variant per game at any time. A newly released revision joins at its
   next session; its first weekly forecast is the first target frozen after its release. A retired one gets no
   new forecasts. (ratified: MHUP-R, design 6.3, 6.4)
6. If a session is interrupted, running the same command again resumes it where its records left off, but only
   when the project's checks admit a safe resume (no project process still running, the session's lock, an
   unchanged code closure and a fresh resume token); otherwise it STOPs and the reviewed recovery procedure is
   followed, so an interruption is never permission to retry. Nothing accepted is redone. An interrupted session is always resolved (resumed and finished, or its lock cleared
   by the project's checking tool) before any code-changing install, and a session cannot be resumed once the
   installed code has changed. (ratified: design 6.1, 6.3, Appendix J; owner, 4 Nov 2026)
7. Copy `source_data/` and `results/` to the backup drive; once a month, restore one copy to a scratch folder and
   compare it. Optionally push the ledgers to GitHub, or email a ledger line's digest, as an outside witness.
   (agreed 2 Nov 2026; ratified: OFF-1, design 7)

## 6. Missed weeks

Any number of draws, one game or both, independently. The command walks forward over the missed draws exactly
as in section 5 step 4, and leaves the next forecast ready. A forecast made after its draw is CATCH-UP (or
development evidence), never PROSPECTIVE, however strict its isolation; a variant that missed a pre-draw
freeze it was eligible for is marked MISSING_BATCH for that draw. (ratified: MH-1, R3 10.5, MHUP-R)

## 7. Adding a method

- Specification (reviewed, ratified; every variant setting fixed); code package (installed non-runnable, with an
  install record); release package (with a release record, whose date counts for CATCH-UP); then it joins the
  cohort. An install that changes the roster waits until no weekly forecast set is unfinished. (built process;
  template draft 4; ratified: MHUP-R, design 4.3, Appendix J)
- **Objective (the owner's, 2 Nov 2026):** a new method is caught up over every past draw, and the rankings
  for all current methods are then refreshed. **How the ratified design delivers it, and what is deferred:**
  - the development draws (before the holdout): a new walk-forward batch of every variant (ratified: ER-6);
    WF-1C's parallel workers come before the next wave for that reason (ratified: ORD-1); reusing existing
    frozen records instead of re-running them is an efficiency item after WF-1C (deferred: roadmap 21b);
  - from its release onward: the weekly session, from its first frozen target (ratified: MHUP-R, design 6.3);
  - the draws between the holdout and its release: only by a separately identified development batch
    (deferred: roadmap 21b; not yet designed);
  - the ten holdout draws: never in the weekly session, and not by roadmap 21b either, because Mode H is a
    one-time study of the cohort released before it (design 6.3). Forecasts by a later method for those draws
    would need a later, separately reviewed extension, if the owner keeps that objective (open); they could
    only ever be retrospective development evidence: never added to the sealed Mode H family, never given
    pre-draw standing, and never counted as part of the original holdout cohort.
  So a method released after Mode H has two gaps in its record: the post-holdout draws before its release
  (until 21b exists) and the ten holdout draws (unless a later extension is approved). Every ranking shows each
  method's number of draws, and methods are compared on the draws they share.
- Then a new dated ranking report over all current methods and the draws they share. The new method's history
  before its release is development evidence; its CATCH-UP record starts at its release record's date; its
  PROSPECTIVE record starts at its first forecast frozen before a deadline. An improved version is a new
  revision with a new record; it is never credited with the old revision's results. (ratified: R3 6.3, MH-1,
  MHUP-R)

## 8. Retiring a method revision

- Its code and tests are archived (built: CODE-3) and its registry entry becomes RETIRED (ratified: E2R 12A.2).
  A retirement arrives only through an install and takes effect at the next weekly session; a forecast already
  frozen for an open draw is still scored. It makes no new forecasts. (ratified: MHUP-R, design 4.3, 6.3)
- Its frozen forecasts and scores stay where they are, because the reports point at them by path and digest. A
  "retired" folder holds an index pointing to them, not the records themselves. (agreed 2 Nov 2026; the index
  is deferred: roadmap 21b)
- Reports show "as published at the time" and "current methods" side by side (ratified: D-8). A method is never
  retired solely because it performs badly; retirement for supersession (ratified: E2R 12A.2) or another
  legitimate reason follows the method-registry and archive rules, and its evidence stays preserved and visible
  (mark, never suppress).

## 9. Offline, timing proof and backups

- Everything installed runs without GitHub; only the updater needs the internet. (ratified: OFF-1)
- A forecast's timing rests on a local, create-only, digest-chained forecast ledger. The chain checks that the
  records agree with each other. Comparing it with an earlier trusted digest, kept separately, can reveal later
  changes. By itself it cannot prove when the records were made, nor that the whole chain was never replaced. A
  line is proved to predate a draw only when an outside witness (a GitHub push, an emailed digest) verifiably
  received that line's digest before the draw. The owner records the witness, and the person who checks the
  service's own receipt records the verification, in a separate witness ledger; a commit's own timestamp is
  not evidence. The witness is optional and the report says whether one exists. (ratified: OFF-1; MHUP-R,
  design 6.5)
- Backups: `source_data/` and `results/` after every weekly session and before every install, to a second
  drive, with a monthly restore test; GitHub holds the code, documents, reports, ledgers if pushed, and the
  results-file records, but not the git-ignored run, attempts and score records. (agreed 2 Nov 2026; design 7)

## 10. Before any of this can run

- Two code packages, each reviewed, rehearsed on Windows and installed by the owner: MHUP-A (the reader for a
  grown results file, E_1 revision 3, the gates, the study plan and opening tools, Mode H, the updater's small
  change) and MHUP-B (the weekly session and the owner's one-page checklist). (ratified: MHUP-R)
- Before MHUP-A is installed, the updater is not run in any form. After its installation and before Approval 2,
  the owner runs the required offline `--self-test` under Python 3.15. No real results update is permitted until
  the owner grants Approval 2 for that game; a STOP is reported and no retry occurs without the owner's new
  explicit instruction. (ratified: MHUP-R, design 4.4 step 3 and section 7; owner, 4 Nov 2026)
- Then, per game and each with the owner's separate approval, Mode H's four steps (section 4). Then the owner
  decides whether to declare the system developed, which unlocks the weekly session. (ratified: GOAL-1, Q8)
- Planning target (owner-agreed, 2 November 2026; not a deadline): Mode H done and the weekly session installed
  by about 13-15 November 2026, so the first PROSPECTIVE forecasts are Oz Lotto 1709 (17 November) and
  Powerball 1592 (19 November). Protection (ratified: FB-1): if it slips, it slips a week rather than any review
  or rehearsal being cut, and the catch-up covers the missed draws.

## 11. Still open, and deferred

- Open: Q7 (the display rule after Mode H; before the first update); whether a later method should ever
  forecast the holdout draws (section 7).
- Deferred, each its own package and the owner's decision, after WF-1C (roadmap 21b): a consolidated
  owner-facing report that ranks across batches by reusing frozen records; a back-history batch for a later
  method over the post-holdout draws before its release; the retired index. A consolidated report holds the
  separate evidence families (development, Mode H, CATCH-UP, PROSPECTIVE) as separately labelled views, with
  sample sizes, exposure windows and matched-draw comparisons; it does not pool them into one score, and no
  combined statistic is specified here.
- The owner's simplicity (KISS) review, after full implementation, only when the owner asks (R-014); the
  deferred performance study, last, only when the owner activates it (R-006).

## Changes from v0.2r1 (candidate v0.3, 4 November 2026)

1. Status: candidate for the reviewer's content check; v0.2r1 stays in force until the owner ratifies.
2. Section 3: CATCH-UP by the release record's date, not the install date (owner, 4 Nov 2026; design 4.3);
   the deadline decided (Q4); LATE_PRE_DRAW and MISSING_BATCH; publication status from the witness record.
3. Section 4: Mode H as ratified (option A, the primary statement, the four approvals, the seal, the report's
   wording); Q7 the only open point.
4. Section 5: Lotterywest-GOV named (LW-1); the updater's refusals; the STOP-and-retry rule (owner, 4 Nov
   2026); the command named; a newly released revision joins at its next session (replacing "has none until its
   walk-forward is done"); interrupted sessions resolved before a code-changing install (owner, 4 Nov 2026);
   the monthly restore test.
5. Section 6: MISSING_BATCH.
6. Section 7: the owner's objective kept, with how the design delivers it and what is deferred (the
   post-holdout back-history; the holdout draws for later methods); CATCH-UP from the release record.
7. Section 8: retirement through an install, effective at the next session; the retired index deferred.
8. Section 9: the witness ledger and its verification.
9. Section 10: MHUP-A and MHUP-B; the four approvals; GOAL-1.
10. Section 11: only Q7 open from the design; one new open point (holdout forecasts for later methods); the
    deferred items listed.
No owner objective is removed; where the ratified design delivers one differently or later, the section says
so.

## Changes in v0.3r1 (the reviewer's focused RECHECK of v0.3, 4 November 2026)

1. C01, section 4: every planned pair reaches DONE, a failed run counted as missing; scoring only once the whole
   batch is complete (design 5.2); the primary statement in the next bullet unchanged.
2. C02, section 10: the updater is not run before MHUP-A is installed; the offline self-test under Python 3.15
   after its installation and before Approval 2; no real update without Approval 2; a STOP is reported and no
   retry occurs without the owner's explicit instruction.
3. C03, section 7: roadmap 21b covers only the post-holdout draws before a method's release; the ten holdout
   draws need a later, separately reviewed extension, and could only ever be retrospective development evidence.
4. O01, section 11: a consolidated report keeps the evidence families separate; no pooled score.
5. O02, section 5 step 6: a session resumes only when the checks admit a safe resume; otherwise STOP and the
   reviewed recovery procedure.
No other line changed.

*End of direction v0.3r1 (candidate).*
