# Direction for the operational procedures, v0.2r1

Plain English. Written by the new Claude chat on 2 November 2026 from the owner's part (d) of the stock-take
record (STOCKTAKE_2026_11_02), as amended by the previous Claude chat's Responses 3 and 3b and by the ChatGPT
reviewer's Response 2, and as the owner accepted them on 2 November 2026. v0.2 applies the reviewer's content
check of 3 November 2026 (findings 1-7), and v0.2r1 the two wording improvements of its focused recheck
(PASS; the change lists are at the end). It says where we are heading and how the
finished system will behave. It is a direction statement, not a specification: the design documents and the
ratification register hold the exact rules, and they prevail wherever this file is looser.

**Status and authority:** owner-ratified operational direction, 2 November 2026; content checked by the ChatGPT
reviewer chat (author: the Claude web chat). This is not an implementation specification and not permission to
run any command, access the holdout or update results. The independently reviewed and owner-ratified designs,
the method and process safety gates, and the separate execution approvals remain binding. No real-data operation
is authorised by this document.

Codes such as MH-1, OFF-1 and HX-1 identify owner decisions already recorded in the ratification register; R3
and E2R name ratified specifications; Q1 and similar labels identify questions still being resolved in the
forthcoming Mode H design.

Each point is marked: (ratified) an owner decision already in the register, with its ID; (agreed 2 Nov 2026) a
position the owner accepted in the stock-take, to be carried into the Mode H design and ratified there;
(open) still to be decided.

## 1. What will be in place

- The software; the two results files (one per game, Powerball and Oz Lotto, never pooled); for every method
  revision, its forecast for every draw it was eligible to forecast, in draw order, frozen when made; the score
  of every forecast once its draw is known; and the ranking reports. A forecast made later for an earlier draw
  is a new record and never acquires pre-draw standing. (ratified: R3, R3 10.4; built for the development
  draws)
- The clock is the draw number within each game: draw numbers define the scientific sequence and every
  training boundary. Dates serve the checks around it: validating incoming results, the timing evidence of a
  forecast, install eligibility and audit records. (ratified: R3 1.1)
- Every forecast for draw N is calculated fresh from the draws before N, never from a stored model. Each method
  follows its own fixed rule about how far back it looks: most look at all earlier draws, a few are defined to
  look at a window (for example the last 52 or 104 draws), because how far back to look is part of what that
  method is. (ratified: R3 10; E2R-R14A)
- After every draw, the forecasts for it are scored, and the rankings are refreshed. (ratified: R3 17)

## 2. The three kinds of record, and what may change

- **Forecasts** are frozen and never changed or replaced. A later rerun of the same target is a new record with a
  new identity and no pre-draw standing. (ratified: R3 10.3, 10.4)
- **Scores** are kept as accepted. If a scorer fault or a new measure needs it, a new scoring run is added
  beside the old one under its own identity; the old one is never edited. (agreed 2 Nov 2026)
- **Rankings** (league tables, reports) are views of the frozen records and are meant to change: when a draw is
  scored, a method added or retired, or the comparison window changed, a new dated report is made. Every old
  report stays as published. "Re-ranking" means a new report, never an edit. (agreed 2 Nov 2026; ratified in
  substance: D-8, R3 17)

## 3. Labels on every scored draw

- PROSPECTIVE: the forecast was frozen before the ratified deadline for its draw (open: Q4; the deadline may be
  earlier than the draw itself).
- CATCH-UP: made after its draw, in draw order, from the draws before it, by a method revision installed before
  that draw. Counts in the rankings, kept apart from PROSPECTIVE. (ratified: MH-1)
- Development evidence: everything else (the walk-forward over past draws, a new method's back-history, a draw
  before the method existed). Ranked in its own table. (ratified: MH-1, R3 17)
- Mode H results carry their own label. Powerball 1585 and 1586 carry an exposure flag within Mode H. Powerball
  1587 and 1588 are post-holdout draws and carry the same flag when the catch-up pass evaluates them; their
  evidence label follows the method's install date, so for the current cohort (installed 31 October 2026) their
  results are development evidence, not CATCH-UP. All flagged draws remain valid and counted. (ratified: HX-1,
  HX-2, MH-1)
- Same arithmetic for all; only the label and the table differ. The label is what lets an outsider see which
  forecasts were genuinely made in advance. (agreed 2 Nov 2026)
- "Installed before that draw" is established from create-only local install records, not Git history,
  including a one-off owner-confirmed record for the methods installed so far (owner decision, 2 November 2026;
  OFF-1). The record's exact format, verification and recovery rules remain for the design (open: Q5 detail).

## 4. Mode H, the one-time holdout test

- Every released variant forecasts each of the ten sealed holdout draws per game, each from the draws before
  its target; all forecasts are frozen; then the ten are scored once. (ratified: register v0.23 "Terms")
- The statement Mode H is meant to support, as the owner now reads it (agreed 2 Nov 2026, subject to the design
  review): "a locked holdout study: the study plan and code were frozen before the holdout was opened; every
  forecast used only draws before its target; no forecast was scored until all were frozen." This is option A.
  Option B (reveal one result at a time) stays in the design as the alternative for the reviewer to weigh.
  Option C (all ten forecasts from the development draws only) is withdrawn: every released method would give
  the same forecast ten times, so it would not test the retraining process. The register's phrase "all frozen
  before the holdout is opened" is to be amended to the wording above in the Mode H design. (open until the
  design is ratified: Q1)
- Mode H rehearses the forecasting, scoring and data-isolation mechanics that the weekly process will use.
  Under option A it is a precommitted holdout evaluation, not pre-draw forecasting: the outcomes are already in
  the system when the forecasts are made, held away from the methods by the N-1 reader. Its exact guarantees
  are settled in the design review and the owner's approval.
- Ten draws per game give limited statistical power; the report will say so. Afterwards the ten draws become
  ordinary history. (agreed 2 Nov 2026; Q7 open on the display rule)

## 5. The normal week

One sitting per week, both games, any day from Friday to Monday. (agreed 2 Nov 2026)

1. Run the results updater (the only step that needs the internet). It fetches from Lotterywest's results page
   only, the current month and the five before it; it refuses unless the fetched draws overlap and match the
   file it already holds, and new draws are consecutive. Always give it its arguments; run bare, it still runs
   an update. (built; TSC-1)
2. For each game, one command. It prints a status block first: last accepted draw, last forecast, last scored
   draw, backlog, next target and its deadline, number of active variants, the label each target will get.
   (agreed 2 Nov 2026)
3. The command then works through the outstanding draws in draw order. For each one whose result is
   accepted: if a forecast for it already exists, it scores that forecast; if not, it makes a catch-up forecast
   from the draws before it, freezes it, then scores it, with the right label. Only then does it move to the
   next draw. When no outstanding draw is left, it freezes the forecast for the next draw and appends it to
   the forecast ledger. No routine accepted score is
   ever produced twice for the same forecast (a separately identified scoring run to correct a fault or add a
   measure is the exception in section 2); a draw whose result is not yet in is left open, never skipped and
   never guessed. (ratified: MH-1; mechanics open in the design)
4. Exactly one open forecast per active variant per game at any time, once that variant has caught up; a
   newly released revision has none until its walk-forward is done; a retired one has none ever again.
   (agreed 2 Nov 2026)
5. Copy source_data/ and results/ to the backup drive. Optionally push the ledgers to GitHub as an outside
   witness. (agreed 2 Nov 2026; OFF-1: the push is optional)
6. A forecast counts as PROSPECTIVE only if frozen before the deadline for its draw (proposed: midnight Adelaide
   time before the draw date; open: Q4).

## 6. Missed weeks

Any number of draws, one game or both, independently. The command walks forward over the missed draws exactly as
in step 3, and leaves the next forecast ready. A forecast made after its draw is CATCH-UP (or development
evidence), never PROSPECTIVE, however strict its isolation. (ratified: MH-1, R3 10.5)

## 7. Adding a method

- Specification (reviewed, ratified; every variant setting fixed); code package (installed non-runnable);
  release package; then it joins the cohort. (built process; template draft 4)
- It is caught up by a full walk-forward over all past draws. Today that is a new full batch of every variant
  (ratified: ER-6); WF-1C's parallel workers come before the next wave for that reason (ratified: ORD-1).
  Reusing existing frozen records instead of re-running them is an efficiency item for after WF-1C. (agreed
  2 Nov 2026)
- Then a new dated ranking report over all current methods and the draws they share. The new method's history
  is development evidence; its CATCH-UP record starts at its install; its PROSPECTIVE record starts at its first
  forecast frozen before a draw. An improved version is a new revision with a new record; it is never credited
  with the old revision's results. (ratified: R3 6.3)

## 8. Retiring a method revision

- Its code and tests are archived (built: CODE-3) and its registry entry becomes RETIRED (ratified: E2R 12A.2).
  It makes no new forecasts.
- Its frozen forecasts and scores stay where they are, because the reports point at them by path and digest. A
  "retired" folder holds an index pointing to them, not the records themselves. (agreed 2 Nov 2026)
- Reports show "as published at the time" and "current methods" side by side (ratified: D-8). A method is
  never retired solely because it performs badly; retirement for supersession (ratified: E2R 12A.2) or another
  legitimate reason follows the method-registry and archive rules, and its evidence stays preserved and
  visible (mark, never suppress).

## 9. Offline, timing proof and backups

- Everything installed runs without GitHub; only the updater needs the internet. (ratified: OFF-1)
- A forecast's timing rests on a local, create-only, digest-chained forecast ledger. The chain checks that the
  records agree with each other. Comparing it with an earlier trusted digest, kept separately, can reveal later
  changes. By itself it cannot prove when the records were made, nor that the whole chain was never replaced. A line
  is proved to predate a draw only when an outside witness (a GitHub push, an emailed digest) verifiably
  received that line's digest before the draw; the witness is optional and the report says whether one exists.
  (ratified: OFF-1; wording agreed 2 Nov 2026)
- Backups: source_data/ and results/ after every weekly session and before every install, to a second drive,
  with one restore test; GitHub holds the code, documents, reports and the six results-file records, but not
  the git-ignored run, attempts and score records. (agreed 2 Nov 2026)

## 10. Before any of this can run

- The version-2 results reader must be installed before the updater is run in any form: even an update that
  finds nothing new writes a line that today's readers refuse. (register v0.23 probe A1; agreed 2 Nov 2026)
- Then, per game and each with the owner's separate approval: freeze the study plan and open the holdout; the
  first update; the Mode H batch; the Mode H scoring. Then the owner decides whether to declare the system
  developed (ratified: GOAL-1).
- Planning target (owner-agreed, 2 November 2026; not a deadline): Mode H done and the weekly session installed
  by about 13-15 November 2026, so the first PROSPECTIVE forecasts are Oz Lotto 1709 (17 November) and
  Powerball 1592 (19 November); 9-12 November is a stretch only. Protection (ratified: FB-1): if it slips, it
  slips a week rather than any review or rehearsal being cut, and the catch-up covers the missed draws.

## 11. Still open (decided in the Mode H design, not here)

Q1 A or B and the final wording; Q4 the prospective deadline; Q5 the install record's format, verification and
recovery rules (its mechanism is decided); Q6 the full report's
cadence; Q7 the display rule after opening; Q8 that the weekly session is R3's FINAL mode and "developed" is
its opening; Q9 two packages; a cross-batch report that reuses frozen records (after WF-1C); the owner's later
simplicity (KISS) review.

## Changes from v0.1 (the reviewer's content check, findings 1-7)

1. Powerball 1587 and 1588: the catch-up pass flags them; their evidence label follows the install date, so for
   the current cohort they are development evidence, not CATCH-UP (section 3).
2. Q5: the local install record is the decided mechanism; only its format, verification and recovery remain
   open (sections 3 and 11).
3. Mode H: rehearses the mechanics; under A a precommitted holdout evaluation, not pre-draw forecasting;
   "limited statistical power" (section 4).
4. Qualifications: what dates are for (section 1); forecasts exist only for eligible revisions and later ones
   gain no pre-draw standing (section 1); PROSPECTIVE means before the ratified deadline (section 3); one open
   forecast per active variant per game (section 5); "nothing scored twice" means no duplicate routine
   accepted scoring (section 5).
5. Retirement: never solely for performing badly; supersession or another legitimate reason under the registry
   and archive rules (section 8).
6. A status-and-authority paragraph at the top; the witness proves timing only when it verifiably received the
   digest before the draw (section 9); the planning target and FB-1 labelled separately (section 10).
7. A sentence explaining the codes (top).
No position ratified on 2 November 2026 is changed.

## Changes from v0.2 (the reviewer's focused recheck: PASS, with two wording improvements that may be made
without another round)

1. Section 9: the hash chain checks that the records agree with each other; only a comparison with an earlier
   trusted digest reveals later changes; by itself it cannot prove when records were made, nor that the whole
   chain was never replaced.
2. Section 5, step 3: outstanding draws are processed strictly in draw order, scoring an existing forecast or
   making, freezing and scoring a catch-up forecast for each, before the next draw; then the next forecast is
   frozen.
No position is changed.

*End of direction v0.2r1.*
