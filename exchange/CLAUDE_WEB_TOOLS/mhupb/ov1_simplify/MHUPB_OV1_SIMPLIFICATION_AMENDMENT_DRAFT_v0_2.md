# MHUP-B: the OV-1 simplification amendment - DRAFT v0.2

**Status:** DRAFT v0.2 for the reviewer's recheck. Not ratified. It authorises nothing. It answers EX_255 (R-3 RECHECK of
v0.1: E01 to E03; E04 is in the deployment note v0.5). Until it is reviewed and the project owner ratifies it, MHUP-B
design supplement v0.8 stands exactly as it is. v0.1 is kept beside it; `AMENDMENT_v0_1_TO_v0_2.diff` is exact.
**Written:** 20 November 2026, 19:45 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's
direction relayed in EX_253 and EX_255 and his decisions of 20 November 2026 (decision log entries 116 and 119). Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH. It changes the rule of the project's one confirmatory forward test (an always-review subject).
**Amends:** `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` sections 5.3, 6, 7.2 and 7.3, and the release-date
test of design v0.1r7 sections 4.3 and 6.4 (section 5 below gives each change); the code plan v0.3 and the deployment design note follow it (sections 6 and 7).
**Answers:** EX_253 section 5, A to F, and EX_255 E01 to E03. The deployment findings (EX_252; EX_255 E04) are in the
deployment note DRAFT v0.5, sent with this document.

## 0. In plain English

1. **There is one OV-1 score for each game.** Its arithmetic is unchanged: the same weights from every counted
   method's TOP and WORST tickets, the same exact fair-draw calculation, the same six fixed settings, the same
   certified numbers, the same bar of 40. Powerball and Oz Lotto are never combined.
2. **What counts at a draw is decided by draw numbers, never by dates.** Each release of methods records, for each
   game, one whole number: its **first draw**. A method counts in the score at every draw from that number on, until a
   later release retires or replaces it. The number is the next draw after the last one on file when the release is
   made. It is written once and never worked out again. Dates and times stay on backups and administrative records
   only.
3. **The forecast must have seen only earlier draws.** It makes no difference whether it was made before the draw, or
   afterwards because a week was missed or a backup was restored. Nothing is ever "missed" or "stopped" by the clock.
4. **A new method is tested on all of history, and the rankings are redone with it in.** Its results on draws before
   its first draw go into the league table, the draw-by-draw historical ranking and a separate exploratory OV-1 view.
   **They never go into the one prevailing score.** Several new methods or revisions can be released in one go.
4a. **The score starts at the draw after the implementation:** the first draw number of the release that first installs
   this recorder in production.
4b. **Each line of the score is plainly "supported" or "qualified".** Supported: exactly the methods the release
   records say should count at that draw were run. Qualified: one of them could not be run, or failed in a catch-up.
   A qualified line is still valid research and nothing stops; the report then says the 2.5% claim is not certified
   from that draw.
5. **What goes:** the owner's registration step and its record; the "stop" command; the line written before each draw
   as a witness; the noon cut-off; "missed" and "stopped" states; every special rule about OV-1 after a restore.
6. **What stays:** the mathematics and its certified arithmetic; forecasts that cannot see their own draw; one record
   per method and draw; an append-only record of the score that can be rebuilt from the other records and checked.
7. **The claim, stated honestly:** if a game's draws are fair, the chance its score ever reaches 40 is at most 2.5%,
   while every line is supported and the conditions of section 8 hold. The Python environment is not pinned (the
   owner's decision); that is stated as an ordinary assumption, not hidden.

## 1. Sources, and what I verified first

- EX_253 (the owner's direction, relayed), EX_252, EX_255, and the owner's answers in the Claude chat (decision log
  entries 116 and 119): caught-up draws count (the reviewer concurs in principle, EX_255 section 3); the three decisions
  of 17 November 2026 that this reverses are confirmed; the environment is not pinned for a delayed draw; the score
  starts at the draw after the implementation; a release's first draw is the next available draw.
- **Draw numbers, not dates** (the owner, relayed in EX_255 section 0, and entry 116 item 2): an effective starting
  draw number for each method, revision and game, fixed at release, decides when it joins the score. "Dates and
  timestamps may be kept for backups and appropriate administrative/operational evidence but not used in normal
  scientific calculations", because the actual time of a draw cannot be guaranteed. R3 v0.5 MRD-12 and 17.3.1 already
  make the draw number the time axis. **v0.1's use of the release record's day against a draw's derived date is
  withdrawn** (EX_255 E01, and its answer to my question 6: that test is a scientific gate, not a placement).
- **Read in the passed code (staged slice 3):** `weekly_session.py` decides, for a draw caught up after the
  fact, between two run modes by one test: a roster member whose release date is before the draw's derived date runs
  as `CATCH_UP`; any other runs as `REAL_DEVELOPMENT`. The same date test is in `weekly_records.py` (validation) and
  `contract_dispatch.py` (the gate), and the routine fill's rule 2A compares a freeze time with a release instant
  (`walk_forward.py`, `contract_dispatch.py`). Section 5 lists each; all become draw-number tests. `weekly_records.effective_class` then gives the classes
  `PROSPECTIVE`, `LATE_PRE_DRAW`, `CATCH_UP` and `DEVELOPMENT_WF_EXPLORATORY` (design Appendix I). One record exists
  for each variant and target in the weekly tier; a target's set is run for the whole roster and is never reopened.
- **The installed release records:** two, `RELEASE_BASELINE_20261031_V1.json` (80 entries) and `RELEASE_MHUP_A_V1.json`
  (2 entries), both made before any weekly session exists.
- **Run for this document:** `ov1_prevailing_examples_v2.py` and its output, beside this file (v0.1's are kept). Invented draws and toy
  methods only; the passed kernel `ov1_numeric.py` is imported unchanged. Sections 3 and 4 quote it.
- **Not done:** no project code was changed; nothing ran on the owner's PC; no real draw was read.

## 2. The rule (EX_253 A)

**2.1 Unchanged.** Supplement 6.1's weights, X, V and Z; 6.3 (one score per game, two-sided, bar 40, never pooled; the
two games together at or under 5%); 6.5's exact evidence score with the six lambdas and its numerical contract (proved
lower bounds; a crossing only on a proved bound); 6.6. OV-1 remains the only confirmatory test of the forward phase.

**2.2 Which records count** (replaces 6.4). For target T, a variant counts if (a) it is in **the cohort as of T** (2.3)
and (b) its one weekly-tier record for T is a complete valid pair of TOP and WORST tickets. Nothing else counts: not a
development record of any kind (a variant whose first draw is after T; every back-history batch; every exploratory
rerun), not a Mode H record, not a failure record, not half a pair. Nothing is imputed.

**2.3 Draw numbers: a release's first draw, the cohort as of a draw, and the start** (EX_255 E01, E03).
- **The release record carries the number.** Every release record made from now on has one more field,
  `effective_first_draw`: one whole number for each game. It applies to every variant the record releases for that
  game, and it is also where every variant the record retires or supersedes stops: such a variant counts at draws
  below that number and at none from it on. One release may carry several new methods and revisions.
- **How the number is set** (the owner, entry 119): by the reviewed release step itself, as **the last draw on file
  for that game plus one**, after the release's own walk-forward and catch-up. A release that changes the roster is
  made only when the weekly records are caught up to the last draw on file (it already waits for an unfinished weekly
  set). The owner may give a later number on the command; never an earlier one. The run sheet's first step is to bring
  the results up to date, so that "the next draw" has not been made: that is the best operational knowledge there is,
  and no draw number can prove a time.
- **It is immutable.** It is written once, in the create-only record, and never recomputed from a date or a clock.
  **A release put back after a restore keeps its original record and so its original number** (the deployment note
  already returns the original record, not a second one).
- **The two existing records** have no such field. They are named in the code with their numbers: the first draw of
  weekly scope for each game (Powerball 1587, Oz Lotto 1704). Every later record must carry the field.
- **The cohort as of T** is read from the release records alone: every variant released by a record whose first draw
  is at or below T, less every variant retired or superseded by a record whose first draw is at or below T. It does not
  depend on today's roster, on any date, or on when T is computed.
- **The start of the score** (the owner, entry 119: "the draw after implementation"): the first-draw numbers of the
  release record of the package that first installs this recorder in production. Two whole numbers, in an immutable
  record, fixed at the reviewed release of the complete implementation. No draw below them enters the score; such
  draws appear in the rankings and the exploratory view. There is no registration step.
- **What dates are still used for, none of it a gate on the score:** the label "forecast before the draw" or "caught
  up" (design Appendix I's classes, from the freeze time and the deadline); the weekly session's choice of whether
  there is time to forecast the next draw beforehand; the checks that the results file is well formed; backups,
  release records' human-readable days, and displays.

**2.4 Every draw is one opportunity.** From the start, each draw number is taken once, in order. Its factor is the
one of 6.5, or exactly 1 in two cases, each a fixed rule: no variant has a counted pair for it (`NO_COUNTED_PAIR`), or
the weights give V = 0 (`V_IS_ZERO`). No draw is dropped, repeated or chosen. There is no reset, no restart and no
second stream.

**2.5 The record** (replaces 6.8). One append-only ledger per game, one line per draw, written by the one recorder
after that draw's weekly set is complete and scored, in draw order. A line holds: the draw; the counted variants
(their number, and a digest of their identities and frozen-forecast digests); how many of them were forecast before
the draw and how many were caught up; the weight of every number; V; X (derived twice, from the weights and from the
score lines, and the two must agree); Z; the six stored log-factors; the six running sums; the pinned master version;
the kernel's version; and, for anyone investigating a difference later, the digests of the code and of the Python
environment that the computing session recorded. Rebuilding the whole ledger from the weekly records and the scores
must give the same bytes (`verify`).
- **Blocked, never stopped.** If an input is not yet there or does not verify (a result not yet accepted, a score line
  missing, a digest that disagrees, X's two derivations disagreeing, the kernel unable to prove a bound), the recorder
  writes nothing for that draw or any later one and says why. Forecasting, scoring and the league table go on. When the
  cause is fixed the recorder continues from where it was. No person chooses a line's content.
- A crossing is declared on a proved lower bound, as now, and is reported from that draw on.

**2.5A The standing of a line** (EX_255 E02). Worked out by the report and by `verify` from the line and the release
records as they stand; it is not stored, so putting a release record back later changes the standing truthfully and
never the ledger.
- **SUPPORTED:** the variants that have a weekly-tier record for T are exactly the cohort as of T; and, if T's
  forecasts were made after its result was on file, none of them is a failure record.
- **QUALIFIED,** with its reason, otherwise. The reasons that can arise: a cohort member was not run (its code is no
  longer installed because a later release superseded it; or its release record was not in the tree when the draw was
  computed); a variant was run that the records now say had ended; a failure record made in a catch-up.
- A failure record made **before** the draw, and a variant with too little history for T, are fixed before the result
  exists and do not qualify a line.
- **Nothing stops.** The report prints, beside the score: the counted draws; how many lines are supported and how many
  qualified, with the first qualified draw and its reason; and either "the 2.5% bound is supported" or "the 2.5% bound
  is not certified from draw T". A qualified stream is a valid research calculation of lesser evidential standing.
- **When the cohort cannot be reproduced** the handling is this label and nothing else: the line is computed from the
  members that ran, the missing member is named, and no later, revised version is ever substituted for it.

**2.5B The Python environment is not part of the pinned rule** (the owner, entry 119). A method's code, configuration
and seed rule are fixed by its release and checked by identity digests. The environment is whatever production holds
when a draw is computed: it "should live with what it receives", is changed when the owner chooses through his own
tested route, and "if it breaks we restore and do something different". A delayed draw computed under a changed
environment can therefore differ in its number from what would have been computed earlier (example 5c). It is not
qualified for that: the line records the environment's digest so the difference can be investigated, and section 8
states the assumption this rests on.

**2.6 The exploratory view** (replaces 6.7). The existing derived view (`ov1_retrospective.py`) applies the same kernel
to any scored history: the current cohort with every variant's back-history, or every scored identity, over any window.
Its label becomes **"OV-1 EXPLORATORY RETROSPECTIVE - not the prevailing score"**. It gives no P value; 40 is drawn as a
reference line only. It is never written to the ledger. It is where a new method's historical effect on the ensemble is
seen. (One recorder and one derived view, sharing one kernel: not two engines.)

## 3. A newly developed method (EX_253 B)

1. **Released** by a reviewed install, as now; several new methods and revisions may come in one release. The step
   first catches the weekly records up, then writes the release record with its first draw for each game (2.3).
2. **Its whole history is run:** a routine fill (supplement 7.1A) from the game's first compatible draw to the last
   accepted draw, under N-1 isolation, former holdout draws included; draws for which it lacks the history it needs
   record `INSUFFICIENT_HISTORY`. All of it is development evidence.
3. **The rankings are recomputed with it in, and republished:** the league table (a new numbered set; the earlier ones
   stay in the archive as what was known then), and **the draw-by-draw historical ranking** (supplement 5.3's
   reconstruction file: for every draw and variant, the matches, running totals and rank after that draw, labelled
   "current-cohort historical reconstruction as of <date>", with the column saying whether the variant was released at
   that draw). **Change: this file is no longer "on request"; the development batch writes a new dated one each time a
   fill is admitted.** Earlier files are kept.
4. **Its historical OV-1 effect is shown** in the exploratory view (2.6), labelled.
5. **It joins the prevailing score at its first draw,** forecasting it for real with every other method. The lines
   already in the ledger are not touched.

**Invented example (output section 2).** NEW is released when the last draw on file is 108, so its record says first
draw 109. Its designer had seen draws 101 to 108.
- (a) Recomputed ranking, draws 101-108: NEW has 56 hits in 8 draws (7.00 a draw; chance is 1.4); the five older
  variants have 0.75 to 1.50. NEW is first by a wide margin, and the table says so. Draws 109-116: NEW has 11 hits
  (1.38 a draw), third of six: ordinary.
- (b) The prevailing score's lines for draws 101-108 are identical before and after NEW's release.
- (c) NEW counts from draw 109 (six variants in place of five).
- (d) The exploratory view with NEW back-filled reads 3.16 after draw 108 against the prevailing score's 1.03: an
  inflation that comes only from fitting, shown where it belongs and kept out of the score.

## 4. The declared rules on invented examples (EX_253 D; EX_255 E02, E04)

| Case | What the rule gives | Standing | Output |
|---|---|---|---|
| Ordinary weeks | Each draw forecast beforehand; one line a draw | supported | 1 |
| A method released later | Ranked over all history; counted from its first draw; earlier lines unchanged | supported | 2 |
| A missed week (draw 111) | Caught up and counted: the factors and the score are **the same** as if forecast beforehand | supported | 3 |
| Failure records made before the draws | A3 fails at 113: five variants count. Every variant fails at 114: factor 1, the draw not hidden | supported | 4a |
| A failure made in a catch-up | Draw 115 is caught up and A3 fails then: the line is computed from the other five | **qualified** from 115 | 4b |
| A restore, backup taken after draw 110 | Draws 111-116 replayed: factors and final score **equal** the lost originals | supported | 5a |
| An older backup, from before NEW's release; the release put back first, with its original first draw 109 | The catch-up equals the lost originals | supported | 5b-i |
| The same backup; the catch-up run before the release is put back | Draws 109-116 were computed without NEW; the records, once back, say NEW should have counted. Final score 0.963 against the lost 1.008 | **qualified** from 109 | 5b-ii |
| A replay after a changed Python package | One variant computes differently; final score 0.985 against the lost 1.008 | supported (2.5B) | 5c |
| A revision superseded at draw 113 (A2 by A2R) | A2 counts through 112, A2R from 113 | supported | 6a |
| A restore across that supersession | The superseding release is put back, so A2's old code cannot run for 111 and 112 | **qualified** for 111 and 112; supported from 113 | 6b |

No ordinary work becomes "missed" because of today's clock. No back-history is presented as forward evidence. Where
the cohort that should have counted could not be reproduced, the line says so by an objective rule.

**The order after a restore that keeps lines supported:** put back any later release first, then catch up. The deploy
tool's `check` prints this. It fully restores the original score when the later release only added methods (5b-i).
When it superseded a revision, the draws between the backup and that release's first draw are qualified whichever
order is used (6b), because the old code and the new cannot both be installed. Backups are taken after every job and
after every release, so this arises only when a backup older than a superseding release is chosen.

## 5. What is deleted, what survives, and the exact amendments (EX_253 C)

**Deleted:** the registered test record and the owner's registration statement; the `register` and `stop` commands;
the eligibility line written before the outcome and the factor table sealed in it; the cut-off C(T); the classification
counted / missed / stop; **the release-date test as a gate (2.3);** `MISSED_NO_FREEZE` and its reconciliation of the forecast ledger against other records; every
`STOP` cause and "the stream stays stopped"; the rule of no second registration; and, in the deployment note, the
restore notices, the stop cause `NOT_ESTABLISHED_AFTER_RESTORE`, the refusal of `register` after a lost registration,
the look inside the set-aside tree for a registration, and any OV-1 purpose of `--after-hand-unzip`.

**Survives, unchanged:** method-facing N-1 isolation; method, revision and variant identities; release records (with one
field added); one
weekly record per variant and target, never reopened; frozen forecasts and their digests; the score lines and the
one-score rule; the classes of design Appendix I; the kernel and its tests; the bar; per-game scope; the sealed Mode H
records; the league table, its archive and sources; the two kinds of development run; the witness status, reported
beside the score and changing nothing.

**Supplement v0.8, section by section:**

| Section | Change |
|---|---|
| 5.3 | "on request" becomes: written, dated and kept each time a routine fill is admitted (section 3 above) |
| 6.1 | "of class `PROSPECTIVE`" becomes "counted by 6.4"; "Eligibility is fixed and recorded before the outcome is read" becomes "Eligibility is fixed by rules that never read the outcome" |
| 6.2 | "The tickets are frozen before the draw" becomes "Each ticket is the output of code whose release has its first draw at or below that draw, given only the draws before it" |
| 6.3 | none |
| 6.4 | replaced by 2.2, 2.3 and 2.5A; the report prints, beside the score, the counted draws, how many variant-forecasts were made before their draw and how many were caught up, the supported and qualified lines, and the witness counts as now |
| 6.5 | the paragraph "Registered before its first draw" is replaced by 2.3 and 2.4; "counted, skipped (V = 0) or missed (6.8)" becomes "counted, or factor 1 by 2.4". The formal result, the no-reset rule and the numerical contract are unchanged |
| 6.6 | none (the new examples are added by reference) |
| 6.7 | replaced by 2.6 |
| 6.8 | replaced by 2.5, 2.5A and 2.5B |
| 7.2 rule 2A | "whose weekly freeze line was written before the variant's release instant" becomes "below the variant's first draw"; the rest of the rule is unchanged |
| 7.3 | adds: the reconstruction file is rewritten with the new variant in it |
| 0, 1A, 13, 14 | wording that follows from the above |

**Other governing documents:** the code plan v0.3 (the recorder's layer and its test rows); the change note
`OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES` (its "formal prospective" use is now the prevailing score);
the deployment design note (section 6 below); R3's measure entry keeps its label "exact test martingale". **Design
v0.1r7 sections 4.3 and 6.4 and Appendix I:** the classes and their names are unchanged; the one test "released before
the draw's date" becomes "the target is at or above the variant's first draw". The freeze time and the deadline keep
deciding only the label `PROSPECTIVE` or `LATE_PRE_DRAW`.

**Code affected (for the later code round; nothing is coded now).** The release-record schema: `RELEASE_RECORD_V2` adds
`effective_first_draw` (a number for each game); the two existing `V1` records stay valid as they are and are mapped
by name to 1587 and 1704. No weekly session, forecast ledger or OV-1 record exists anywhere yet, so nothing else
needs migrating.

| File | Change |
|---|---|
| `src/package_tools/install_records.py` (installed) | `release-record` writes `effective_first_draw` (last draw on file plus one, or a later number given on the command); for a roster change it also requires the weekly records caught up to the last draw on file |
| `src/methods/_common/release_records.py` (installed) | reads and validates the field (a whole number above the game's last holdout draw; never lower than an earlier record's); the two named `V1` records; `first_draws()` replaces `release_instants()`; new `cohort_as_of(game, target)`; `released_variants()` unchanged |
| `src/methods/_common/weekly_records.py` (slice 2) | the roster entry gains `effective_first_draw`; `validate_named_record`'s test `release date < derived date` becomes `first draw <= target` |
| `src/methods/_common/weekly_session.py` (slice 2) | the same test in its two places (the run mode of a caught-up target; the named record); the roster entry carries the number |
| `src/methods/_common/owner_records.py` (slice 2) | `release_date_of` gives way to a first-draw accessor |
| `src/methods/_common/contract_dispatch.py` (slice 2) | the gate's two tests: `CATCH_UP` needs `first draw <= target`; a routine fill needs `target < first draw` (in place of the freeze time against the release instant) |
| `src/methods/_common/walk_forward.py` (slice 3) | the routine fill's pairs by the same draw-number test |
| `src/evaluation/ov1.py`, `Method_OV1.py` (slice 2) | much smaller: `record`, `status`, `verify` stay; `register`, `stop`, `cutoff`, `reconcile`, the registration and the line kinds other than the one factor line go; the standing of 2.5A |
| `src/evaluation/ov1_numeric.py` (slice 2) | none |
| `src/Weekly_Session_Orchestrator.py` (slice 2) | calls `record` after scoring only; the "stopped" state and its messages go |
| `src/evaluation/consolidated_report.py`, `ov1_retrospective.py` (slice 3) | labels; the score's part reads the new ledger; the before and caught-up counts; supported and qualified |
| `src/Development_Batch_Orchestrator.py` (slice 3) | writes the reconstruction file after an admitted fill |
| The league table and reports | still show each variant's release day, as information; they also show its first draw |
| Tests | `tests/test_mhupb_ov1.py` and the report tests rewritten for these rules; the weekly, dispatch and release-record tests changed where they assert the date test; one planted defect per rule; the kernel's tests untouched |

The passed slices are not reopened as slices; these changes arrive in the integrated package and are reviewed there.

## 6. What this does to the deployment design note

Its section 9 (formal OV-1 after a restore) is replaced by one paragraph: **a restore has no OV-1 side effect.** The
ledger comes back as it was in the backup; the lost draws are caught up by the ordinary session and counted by 2.2, each line with its standing (2.5A);
nothing reads the set-aside tree. The restore notices and everything listed under "Deleted" above leave the note. The
deployment note DRAFT v0.5, sent with this document, carries this with EX_252's corrections, and states when a replay
equals the lost score and when it does not (EX_255 E04).

## 7. Alternatives considered

1. **A draw not forecast beforehand counts as neutral (factor 1).** It needs a clock rule to say what "beforehand" is,
   a rule for what a restore does to draws that were counted, and something to stop a backup being chosen to shed
   draws: the machinery being removed. Example 3 shows it also changes the number for no scientific reason. Not
   proposed. (The owner: caught-up draws count, if the reviewer concurs.)
2. **Start the score at ratification** (v0.1's proposal). Withdrawn: the reviewer prefers the reviewed freeze of the
   complete implementation (EX_255 E03) and the owner chose "the draw after implementation" (entry 119).
2a. **The owner types each release's first draw.** Only he knows whether this week's draw has been made. He chose the
   automatic "next available draw" after the catch-up; a later number can still be given on the command.
2b. **Qualify a line whenever the environment's digest differs from the last session's.** Objective and cheap, but it
   would make the environment part of the pinned rule, which the owner has decided against (2.5B).
2c. **A ceiling on the weekly session's catch-up,** so that after a restore the old code can replay up to a superseding
   release's first draw before that release is put back. It would turn example 6b's two qualified lines into
   supported ones. Not proposed: a new science-affecting option for a rare case; the label is truthful without it.
3. **Keep the pre-draw witness line as an optional extra.** A second kind of line with no rule resting on it. Not
   proposed; the count of forecasts made before their draw carries the same information.
4. **Recompute the score on demand and keep no ledger.** Possible, since it is a function of the other records. The
   ledger is kept because an append-only record that must equal its rebuild is a cheap, strong check against silent
   change.

## 8. The guarantee and its limits (EX_253 E; EX_255 E02)

**Claim, per game:** if the draws are fair, the chance that the prevailing score ever reaches 40 is at most 2.5%,
however often it is looked at and whatever methods are added, revised or retired along the way.

**It is supported while these four hold, each checked by the software.**
1. **Isolation.** Each counted forecast was computed by code given only the draws before its target. (The driver;
   tested.)
2. **The cohort is fixed by draw number.** The variants counted at T are exactly the cohort as of T by the immutable
   release records, each running the code, configuration and seed rule of its release. (2.3; identity digests.)
3. **Every draw once.** From the start, in draw-number order, each draw exactly once, with factor 1 only by 2.4.
   (The recorder; `verify`.)
4. **Every line is supported** (2.5A). From the first qualified line the report says the bound is not certified.

**Why this is enough.** The mathematics needs each draw's weights to be fixed by things that do not depend on that
draw's result. It does not need them to have been computed before the draw. A release's first draw is fixed before
that draw is made; the cohort as of T follows from the records; the forecasts follow from the released code and the
earlier draws. Conditions 2 and 4 replace v0.1's condition about intentions with a rule (EX_255 section 3 and Q2).
Choosing or changing methods in the light of **earlier** draws is allowed: that is what "given the past" means.

**Ordinary assumptions, stated and not policed.** The software and the records work as specified and are not altered.
A release's first draw has truly not been made when the release is written (the owner brings the results up to date
first). **The Python environment and the non-method code are changed through their ordinary reviewed routes and not
in order to move a score; the environment is not pinned, by the owner's decision (2.5B).** A reader who wants a
stricter claim can restrict it to the draws whose forecasts were made before the draw; the report gives that count.

**What differs between the two kinds of counted forecast.** For one made before its draw, the conditions are also
backed by a physical fact: the result did not exist. For one caught up afterwards they rest on the software's
isolation and on the records. That is a weaker kind of evidence for the same conditions, and the report prints the
split.

**What the claim never covers:** the exploratory view; the league table and every ranking; any back-history; Mode H;
a qualified stream from its first qualified draw; a product or sum over both games. A crossing challenges the
fair-draw assumption for that game. It is not proof of a cause and promises nothing about later draws. A strong
historical effect is worth investigating whether or not this claim applies to it.

## 9. Not tested, and uncertainties

- The examples use toy methods and a 35-number barrel. They show the rules, not the real methods' behaviour.
- Whether every real method gives byte-identical forecasts when replayed in the same environment is asserted by the
  method contract (E2R-1 7.1) and exercised by the project's tests, not proved for every future method. Under this amendment a
  difference changes the number, not the validity (example 5c).
- **The environment** is an ordinary assumption here, not a pinned part of the rule (2.5B). EX_255 section 3 asked for
  the "numerical environment/policy" of a delayed draw to be defined; the definition offered is "whatever production
  holds, recorded by digest on the line". The reviewer may judge that insufficient for the unconditional claim; the
  owner's decision is on record (entry 119), and alternative 2b shows what the stricter rule would be.
- **"The next draw has not been made"** when a release is written rests on the results being up to date. No draw
  number can prove it.
- **A restore across a superseding release leaves qualified lines** (example 6b; alternative 2c).

## 10. For the reviewer

1. E01: is the one field per release record, with the two existing records named in the code, the smallest schema
   that meets it? Is the automatic "last draw on file plus one, after the catch-up" acceptable as the conservative
   future target, with the results brought up to date first?
2. E02: does the standing rule (2.5A) say exactly enough about when the bound is supported? Is "a failure record made
   in a catch-up qualifies the line" right, or too strict?
3. The environment (2.5B): accepted as an ordinary assumption on the owner's decision, or does the unconditional
   claim need alternative 2b?
4. E03: the start as the first-draw numbers of the release that first installs the recorder.
5. Example 6b: is the truthful label enough, or is the ceiling of alternative 2c wanted?

End of the amendment, DRAFT v0.2.
End of the amendment, DRAFT v0.1.
