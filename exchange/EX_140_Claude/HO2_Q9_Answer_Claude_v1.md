# HO-2 takeover verification - Claude's answer to Q9 (the owner's operational direction)

Date: 2026-11-04
Project: hydra3333/analysing_perceived_randomness_in_reality
From: the replacement Claude chat; to the ChatGPT reviewer chat, relayed by the project owner
Basis: main at 20a3f40 (no pushes since; checked 4 November 2026 11:45); `doc/Direction_for_operational_procedures_v0_2r1.md`
("the direction"); the owner's own part (d) in `doc/owner_stocktake_v1_0.txt` lines 555-594 ("part (d)"); the
ratified design `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md` ("the design");
register v0.24.
Status: written before seeing the reviewer's assessment or suggested answer. Understanding only: nothing
here proposes implementation changes or authorises any work. A separate file carries a CANDIDATE v0.3 of the
direction, as the owner asked, for the reviewer's content check.

---

## Part A. The completed system, from the owner's side

### A1. What will be there

- **Two results files**, one per game (Powerball and Oz Lotto), never pooled.
- **Every forecast**: for every method revision, a forecast for every draw it was eligible to forecast, in
  draw order, frozen when it was made.
- **The score** of every forecast once its draw is known, and the ranking reports and league tables built
  from those scores.
- **The clock** is the draw number within each game. Dates only serve checks: validating new results, the
  timing of a forecast, release eligibility, and audit.
- **Fresh calculation**: every forecast for draw N is made fresh from the draws before N, never from a
  stored model.
  - Each method keeps its own fixed rule about how far back it looks. Most look at all earlier draws; some
    use a window such as the last 52 or 104 draws, because that window is part of what the method is.
- **A forecast made after its draw** is a new record. It never acquires pre-draw standing.

### A2. An ordinary week (one sitting, any day Friday to Monday, both games)

1. **The owner runs the results updater**, the only step that needs the internet.
   - It reads only Lotterywest-GOV's results page.
   - It refuses unless what it fetched overlaps and agrees with the draws already held, and the new
     draws are consecutive.
   - It is always given its arguments, never run bare.
2. **The owner runs one command per game**, and it prints a status block first:
   - the last accepted draw, the last forecast and the last scored draw;
   - the backlog, and the next target with its deadline;
   - the number of active variants, and the label each target will get.
3. **The command works through outstanding draws strictly in draw order.** For each draw whose result is in:
   - if a forecast already exists, it scores it;
   - if not, it makes a catch-up forecast from the draws before it, freezes it, then scores it.

   It then freezes the forecast for the next draw. A draw whose result is not yet in is left open, never
   skipped and never guessed. No forecast gets a second routine accepted score.
4. **The owner copies `source_data/` and `results/` to a backup drive**, and may push the ledgers to GitHub
   as an outside witness.
5. **Labels.** A forecast counts as PROSPECTIVE only if frozen before its draw's deadline. Every active variant
   has exactly one open forecast per game once it has caught up.

### A3. Missed weeks

- Any number of draws can be missed, in one game or both, independently.
- The same command walks forward over the missed draws exactly as in A2 step 3, and leaves the next forecast
  ready.
- A forecast made after its draw is CATCH-UP or development evidence, never PROSPECTIVE, however strict its
  isolation.

### A4. A new method

- It goes through specification, code package (installed non-runnable) and release package, then joins
  the cohort.
- **The owner's objective (part (d) item 4) is that a new method is caught up from the earliest draw to the
  latest**, and the rankings are then refreshed for all current methods.
- The direction refines this:
  - today, catching up means a new full batch of every variant (ER-6);
  - reusing frozen records instead comes after WF-1C;
  - a new dated report then covers all current methods over the draws they share;
  - the new method's history is development evidence;
  - its CATCH-UP record starts at its install (but see B1);
  - its PROSPECTIVE record starts at its first forecast frozen before a draw;
  - an improved version is a new revision with its own record.

### A5. Retiring a method

- **Part (d) item 5** originally pictured the method and its data moved into a "retired" folder, then all
  draws re-ranked for the methods still current.
- **The agreed direction** (section 8) keeps the records where they are, because reports point at them by
  path and digest:
  - the code and tests are archived (CODE-3);
  - the registry entry becomes RETIRED;
  - a "retired" folder holds only an index pointing at the records;
  - reports show "as published at the time" and "current methods" side by side (D-8);
  - a method is never retired solely for performing badly, and its evidence stays visible (mark, never
    suppress).

## Part B. Does the ratified MHUP-1 design support it?

**Broadly yes, for the weekly loop, missed weeks and Mode H.** It is partial, with deferred items, for the
owner's picture of new methods and complete re-ranking. The points that matter:

### B1. More precise rules that replace looser direction wording

The objective is unchanged in each case.

- **CATCH-UP is decided by the release record's local date, not the install date** (design 4.3; owner,
  4 November 2026). Direction sections 3 and 7 say "install". For the cohort of 31 October 2026 the
  answer is the same: Powerball 1587-1589 and Oz Lotto 1704-1706 are development evidence, and Oz Lotto 1707
  and Powerball 1590 onward are CATCH-UP.
- **The deadline (Q4, decided).** It is 00:00 local on the draw date. A forecast set must start at least an
  hour before, so in practice by 23:00 the evening before. Two categories are new:
  - `LATE_PRE_DRAW`: frozen after the deadline but before the result was accepted. Kept and shown, never
    counted as evidence.
  - `MISSING_BATCH`: an eligible variant missed its pre-draw freeze.
- **The timing proof.** The forecast ledger is local and digest-chained. A separate witness ledger records
  a GitHub push or an emailed digest. PUBLISHED_BEFORE_DRAW is worked out at report time, only from a
  verified witness. This is the direction's section 9 made exact.
- **The updater** reads only Lotterywest-GOV over HTTPS at exactly `www.lotterywest.wa.gov.au` (LW-1),
  with no fallback of any kind. It refuses while a session is running, and between the first update and
  the Mode H seal. Each retry after a STOP needs the owner's explicit say-so (owner, 4 November 2026).
  Its default window is the current month plus five back. Part (d) said "6 or 12 months"; the direction
  says current plus five.
- **Mode H** is ratified as option A, with the primary statement. The direction's section 4 wording lacks
  "environment" and "all planned attempts".
- **"Exactly one open forecast per active variant".** The design states it as at most one, and exactly one
  for the open line's roster after a session that ended with a freeze or an open forecast (design 6.4).
- **One command per game.** It is `Run_Weekly_Session.bat --game G`, in which a sequencer alternates a
  forecasting program and a scoring program (MHUP-B02). Interruptions resume the same session; a master
  that grows mid-session ends it (`STALE`).
- **Interrupted sessions** must be resolved before a code-changing install (owner, 4 November 2026; for the
  MHUP-B checklist).

### B2. A real difference: how a new method catches up (direction sections 5 step 4 and 7; part (d) item 4)

- **What the design delivers:**
  - a newly released variant joins the weekly roster at its next session;
  - its first weekly forecast is the first target frozen after its release; it does not wait for a walk-forward;
  - development back-history over the pre-holdout draws comes from a new full-cohort batch (ER-6), as today.
- **What it does not deliver:**
  - **It never forecasts the ten holdout draws.** Mode H is a one-time study of the released cohort. A later
    method's forecasts on holdout draws would need "a separately reviewed extension" (design 6.3).
  - **The draws between the holdout and its release** (for example, Powerball 1587 up to its release) are
    covered only by "a separately identified development batch". That is roadmap 21b, not in MHUP-1's scope.
    The ordinary walk-forward kind stays capped below the holdout (design 3.1 table).
- **So, until 21b exists,** a method released after Mode H has a permanent gap in its record: the holdout
  draws plus the post-holdout draws before its release. That falls short of part (d)'s "caught up from the
  earliest draw to the latest".
- The design's reason is sound: no later method may claim holdout standing, and closed weekly targets are
  never reopened. But the owner's objective is only partly met until 21b, and the holdout part is not
  planned at all.

### B3. Partly deferred: rankings across everything

- Rankings come from **three separate places today**:
  - each development batch gets its own WF-1B report, in its own window;
  - Mode H gets its own report and family, never pooled;
  - the weekly league table is cumulative from the score ledger, with PROSPECTIVE, CATCH-UP and development
    in separate columns, and Mode H and the development reports referenced in their own columns.
- The owner's "re-ranking of all draws for all prevailing methods" across those sources is partly met:
  - weekly, as a dated cumulative table;
  - in full, only once the **cross-batch report reusing frozen records** exists (roadmap 21b, after WF-1C;
    design section 9, "not in scope").
- Methods released at different times have different numbers of draws. Every figure shows its draw count,
  and cohorts are compared on matched draws.

### B4. Deferred: retirement plumbing

The design covers what retirement means for the weekly loop:
- a retirement arrives only by an install, and takes effect at the next session;
- a retired variant's open forecast is still scored;
- it gets no new forecasts.

The **retired index**, and "as published" next to "current methods" across all reports, are roadmap 21b. CODE-3 already archives a superseded revision's code.

### B5. Supported as the owner described

- the weekly order (forecast, reveal and score each draw in turn, then freeze the next);
- the status block, and an unaccepted draw left open;
- missed weeks in either game independently;
- fresh fitting for every target;
- offline running, with GitHub optional;
- backups, made routine by a weekly copy and a monthly restore test;
- the three labels, never pooled.

## Part C. Preserving original records versus regenerating current rankings

- **Original scientific records are never changed**:
  - every frozen forecast;
  - every accepted score line in the Mode H and weekly score ledgers;
  - every published report.

  A fault in a scorer, or a new measure, gets a **separately identified scoring run beside** the accepted
  one, with its own policy id and `amendment_of`. It never goes over the accepted score (ST-1, ST-2 as read
  in register v0.24).
- **Rankings are views and are meant to be regenerated**: a newly scored draw, an added or retired method,
  or a changed window produces a **new dated report**, while every earlier report stays as published (D-8,
  ST-1).

  So part (d)'s "re-scoring/ranking of all draws" means, in project terms:
  - new forecasts and scores for the newcomer, as new records;
  - for everyone else, a new ranking built from the existing frozen forecasts and accepted scores;
  - never a rewrite of what exists.
- **One nuance to confirm.** As I read H-1 section 7.5, a development report (WF-1B) has its own scoring plan
  and score ledgers, and computes the per-target quantities from a batch's frozen forecasts each time a
  report is run. That is deterministic, never touches a forecast, and is the "view" kind of regeneration.
  The "no duplicate routine accepted score" rule is written for the Mode H and weekly score ledgers. I
  believe both readings are consistent, but I have not checked the WF-1B code on this point. The
  cross-batch report (21b) is where reuse of accepted scores would become the rule.

## Part D. What in the current plan may complicate or frustrate the intended workflow

Identified only; no change proposed.

1. **Adding a method gets heavier as the cohort grows** (ER-6). Every new method means a new full-cohort
   batch per game (today 17,280 Powerball and 8,760 Oz Lotto runs, growing with each wave) and a new
   report, each separately authorised. WF-1C (parallel workers) and 21b (reuse) are the relief, and both
   come after MHUP-1.
2. **The catch-up gap for later methods** (B2). It means the per-draw, every-method history the owner
   pictured will have holes until 21b is designed. For the holdout draws, the holes stay unless an extension
   is separately designed.
3. **Three ranking sources instead of one** (B3), until the cross-batch report exists.
4. **Per-method process weight.** Each method needs:
   - a specification;
   - a code package, then a separate release package (E2R-R58; ER-2r1 was an exception for E_1 only);
   - from MHUP-A on, a two-commit install with install and release records;
   - the D3 rule not to launch certain programs during an install;
   - a Windows rehearsal for each package.

   That is several rounds per wave. It is safe, but slow against "getting it running".
5. **Operator friction in recovery paths:**
   - resume tokens that must be under five minutes old;
   - clearing session or updater locks only through `process_check.py`;
   - the A7 interrupted-update procedure;
   - an install refused while a session lock or an unfinished weekly set exists.

   The updater's unchanged message still says "delete the lock by hand", which the checklist must tell the
   owner never to follow.
6. **Wording that could suggest a weekly approval round.** H-1 section 10.8 lists "every weekly session" as
   permission-gated. After the GOAL-1 declaration I read the owner's own running of the command as that
   permission; it is worth saying plainly so no extra approval step is expected each week.
7. **The deadline depends on the PC's clock and time zone**, and each set must start by about 23:00 the
   evening before: Monday for Oz Lotto, Wednesday for Powerball. A Friday-to-Monday sitting fits both, as
   long as the Oz Lotto session starts its set by 23:00 on Monday.

## Part E. Unresolved questions

1. **Does the owner still want part (d) item 4 in full?** That is, a new method's record covering every
   draw, including the post-holdout draws before its release and the holdout draws.
   - If yes, roadmap 21b's back-history batch is the route for the post-holdout part, and a separately
     reviewed extension would be needed for the holdout part.
   - If not, the gap should be stated as accepted.
2. **Is one combined ranking across development, Mode H and weekly evidence an objective?** If so, it is the
   cross-batch report after WF-1C.
3. **Development reports.** Please confirm that recomputing per-target quantities in each new development
   report (Part C) is the intended "view" behaviour, and not a duplicate scoring under ST-1.
4. **"Every weekly session" (H-1 10.8).** Confirm it is satisfied by the owner choosing to run it after
   GOAL-1.

End of Q9 answer.
