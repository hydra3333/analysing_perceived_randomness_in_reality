# MHUP-B: the OV-1 simplification amendment - DRAFT v0.1

**Status:** DRAFT v0.1 for independent review. Not ratified. It authorises nothing. Until it is reviewed and the project
owner ratifies it, MHUP-B design supplement v0.8 stands exactly as it is.
**Written:** 20 November 2026, 18:37 Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner's
direction relayed in EX_253 and his decisions of 20 November 2026 (decision log entry 116). Fable (High).
**Reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner, after the review.
**Risk tier:** HIGH. It changes the rule of the project's one confirmatory forward test (an always-review subject).
**Amends:** `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_8.md` sections 5.3, 6 and 7.3 (section 5 below gives each
change); the code plan v0.3 and the deployment design note follow it (sections 6 and 7).
**Answers:** EX_253 section 5, A to F. F (EX_252's deployment findings) is in the deployment note DRAFT v0.4, sent with
this document.

## 0. In plain English

1. **There is one OV-1 score for each game.** Its arithmetic is unchanged: the same weights from every counted
   method's TOP and WORST tickets, the same exact fair-draw calculation, the same six fixed settings, the same
   certified numbers, the same bar of 40. Powerball and Oz Lotto are never combined.
2. **What counts at a draw is simple.** A method counts at a draw if it was **released before that draw** and it
   forecast that draw **seeing only the draws before it**. It makes no difference whether the forecast was made before
   the draw, or afterwards because a week was missed or a backup was restored.
3. **So nothing is ever "missed" or "stopped" because of the clock.** A missed week is caught up and counted. A
   restored backup is walked forward and counted. The score is the same either way.
4. **A new method is tested on all of history, and the rankings are redone with it in.** Its results on draws made
   before it was released go into the league table, the draw-by-draw historical ranking and a separate exploratory
   OV-1 view. **They never go into the one prevailing score.** It joins that score at the first draw after its release.
5. **What goes:** the owner's registration step and its record; the "stop" command; the line written before each draw
   as a witness; the noon cut-off; "missed" and "stopped" states; every special rule about OV-1 after a restore.
6. **What stays:** the mathematics and its certified arithmetic; forecasts that cannot see their own draw; one record
   per method and draw; an append-only record of the score that can be rebuilt from the other records and checked.
7. **The claim, stated honestly:** if a game's draws are fair, the chance its score ever reaches 40 is at most 2.5%,
   provided the four conditions of section 8 hold. For a draw forecast afterwards, "it could not have seen the result"
   rests on the software and the records, not on the result not yet existing. The report shows how many counted draws
   are of each kind.

## 1. Sources, and what I verified first

- EX_253 (the owner's direction, relayed), EX_252, and the owner's answers in the Claude chat (decision log entry 116):
  caught-up draws count if the reviewer concurs; **draw numbers are the timeline**; the three decisions of 17 November
  2026 that this reverses are confirmed as reversed on ratification.
- **The timeline is the draw number, already ratified** (the owner asks that the reviewer note this): R3 v0.5, MRD-12,
  "The time axis is the draw number ... Dates are never used for ordering or arithmetic." This amendment states its
  start and its rules in draw numbers.
- **Read in the passed code (staged slice 3):** `weekly_session.py` already decides, for a draw caught up after the
  fact, between two run modes by one test: a roster member whose release date is before the draw's derived date runs
  as `CATCH_UP`; any other runs as `REAL_DEVELOPMENT`. `weekly_records.effective_class` then gives the classes
  `PROSPECTIVE`, `LATE_PRE_DRAW`, `CATCH_UP` and `DEVELOPMENT_WF_EXPLORATORY` (design Appendix I). One record exists
  for each variant and target in the weekly tier; a target's set is run for the whole roster and is never reopened.
- **Run for this document:** `ov1_prevailing_examples.py` and its output, beside this file. Invented draws and toy
  methods only; the passed kernel `ov1_numeric.py` is imported unchanged. Sections 4 and 7 quote it.
- **Not done:** no project code was changed; nothing ran on the owner's PC; no real draw was read.

## 2. The rule (EX_253 A)

**2.1 Unchanged.** Supplement 6.1's weights, X, V and Z; 6.3 (one score per game, two-sided, bar 40, never pooled; the
two games together at or under 5%); 6.5's exact evidence score with the six lambdas and its numerical contract (proved
lower bounds; a crossing only on a proved bound); 6.6. OV-1 remains the only confirmatory test of the forward phase.

**2.2 Which records count** (replaces 6.4). For target T, a variant counts if its **one weekly-tier record for T** is
a complete valid pair of TOP and WORST tickets of class `PROSPECTIVE`, `LATE_PRE_DRAW` or `CATCH_UP`. By the design's
existing rules each of those three classes means: the variant was released before T's draw, and the forecast was made
by the released code under N-1 isolation. Nothing else counts: not a `DEVELOPMENT` record of any kind (a variant
released on or after the draw; every back-history batch; every exploratory rerun), not a Mode H record, not a failure
record, not half a pair. Nothing is imputed.

**2.3 The timeline, the start, and a release's first draw.**
- Everything is ordered by draw number, per game.
- **The start is a draw number for each game, written into this amendment at ratification and into the code as two
  constants:** the first draw of each game not yet made when the owner ratifies. If that is before 24 November 2026:
  **Oz Lotto 1710 and Powerball 1593.** No earlier draw can ever enter the score. There is no registration step and no
  start record to lose.
- **A release's first eligible draw,** per game, is the first draw made after the day of its release record. This is
  the test the weekly code already applies. It is the one place a calendar is used: to put a real-world event, a
  release, onto the draw-number axis. Nothing is ordered or computed by date.
- A variant counts from its first eligible draw: no probation, no preference, no back-fill.

**2.4 Every draw is one opportunity.** From the start, each draw number is taken once, in order. Its factor is the
one of 6.5, or exactly 1 in two cases, each decided without reading the result: no variant has a counted pair for it
(`NO_COUNTED_PAIR`), or the weights give V = 0 (`V_IS_ZERO`). No draw is dropped, repeated or chosen. There is no
reset, no restart and no second stream.

**2.5 The record** (replaces 6.8). One append-only ledger per game, one line per draw, written by the one recorder
after that draw's weekly set is complete and scored, in draw order. A line holds: the draw; the counted variants
(their number, and a digest of their identities and frozen-forecast digests); **how many of them were forecast before
the draw and how many were caught up**; the roster members not counted, by reason; the weight of every number; V; X
(derived twice, from the weights and from the score lines, and the two must agree); Z; the six stored log-factors; the
six running sums; the pinned master version; the kernel's version. Rebuilding the whole ledger from the other records
must give the same bytes (`verify`).
- **Blocked, never stopped.** If an input is not yet there or does not verify (a result not yet accepted, a score line
  missing, a digest that disagrees, X's two derivations disagreeing, the kernel unable to prove a bound), the recorder
  writes nothing for that draw or any later one and says why. Forecasting, scoring and the league table go on. When the
  cause is fixed the recorder continues from where it was. Because every line is a function of the other records,
  nothing needs a permanent stop, and no person chooses a line's content.
- A crossing is declared on a proved lower bound, as now, and is reported from that draw on.

**2.6 The exploratory view** (replaces 6.7). The existing derived view (`ov1_retrospective.py`) applies the same kernel
to any scored history: the current cohort with every variant's back-history, or every scored identity, over any window.
Its label becomes **"OV-1 EXPLORATORY RETROSPECTIVE - not the prevailing score"**. It gives no P value; 40 is drawn as a
reference line only. It is never written to the ledger. It is where a new method's historical effect on the ensemble is
seen. (One recorder and one derived view, sharing one kernel: not two engines.)

## 3. A newly developed method (EX_253 B)

1. **Released** by a reviewed install, as now. Its release record gives its first eligible draw in each game.
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
5. **It joins the prevailing score at its first eligible draw.** The lines already in the ledger are not touched.

**Invented example (output section 2).** NEW is released after draw 108. Its designer had seen draws 101 to 108.
- (a) Recomputed ranking, draws 101-108: NEW has 56 hits in 8 draws (7.00 a draw; chance is 1.4); the five older
  variants have 0.75 to 1.50. NEW is first by a wide margin, and the table says so. Draws 109-116: NEW has 11 hits
  (1.38 a draw), third of six: ordinary.
- (b) The prevailing score's lines for draws 101-108 are identical before and after NEW's release.
- (c) NEW counts from draw 109 (six variants in place of five).
- (d) The exploratory view with NEW back-filled reads 3.16 after draw 108 against the prevailing score's 1.03: an
  inflation that comes only from fitting, shown where it belongs and kept out of the score.

## 4. The declared rules on invented examples (EX_253 D)

| Case | What the rule gives | Output |
|---|---|---|
| Ordinary weeks | Each draw forecast beforehand; one line a draw | 1 |
| A method released later | Ranked over all history; counted from its first eligible draw; earlier lines unchanged | 2 |
| A missed week (draw 111) | Caught up by the next session and counted: the factors and the score are **the same** as if it had been forecast beforehand; the line records "0 before, 6 caught up". Supplement v0.8 would have given it factor 1 | 3 |
| A forecast really missing | A3 has only a failure record for draw 113: five variants count. No variant has a pair for draw 114: factor 1, `NO_COUNTED_PAIR`, the score unchanged, the draw not hidden | 4 |
| A restore, backup taken after draw 110 | Draws 111-116 replayed: factors and final score **equal** the lost originals | 5 |
| An older backup, taken before NEW's release | NEW is installed again after the restore, so its first eligible draw is later; draws 108-116 are replayed without it; the score differs from the one that was lost (0.963 against 1.008). Both are valid; see condition 4 of section 8 | 5b |
| A replay after a changed Python package | One variant computes differently; the score differs from the lost one; every weight still came from history before its draw | 5c |

No ordinary work becomes "missed" because of today's clock, and no back-history is presented as forward evidence.

## 5. What is deleted, what survives, and the exact amendments (EX_253 C)

**Deleted:** the registered test record and the owner's registration statement; the `register` and `stop` commands;
the eligibility line written before the outcome and the factor table sealed in it; the cut-off C(T); the classification
counted / missed / stop; `MISSED_NO_FREEZE` and its reconciliation of the forecast ledger against other records; every
`STOP` cause and "the stream stays stopped"; the rule of no second registration; and, in the deployment note, the
restore notices, the stop cause `NOT_ESTABLISHED_AFTER_RESTORE`, the refusal of `register` after a lost registration,
the look inside the set-aside tree for a registration, and any OV-1 purpose of `--after-hand-unzip`.

**Survives, unchanged:** method-facing N-1 isolation; method, revision and variant identities and release records; one
weekly record per variant and target, never reopened; frozen forecasts and their digests; the score lines and the
one-score rule; the classes of design Appendix I; the kernel and its tests; the bar; per-game scope; the sealed Mode H
records; the league table, its archive and sources; the two kinds of development run; the witness status, reported
beside the score and changing nothing.

**Supplement v0.8, section by section:**

| Section | Change |
|---|---|
| 5.3 | "on request" becomes: written, dated and kept each time a routine fill is admitted (section 3 above) |
| 6.1 | "of class `PROSPECTIVE`" becomes "counted by 6.4"; "Eligibility is fixed and recorded before the outcome is read" becomes "Eligibility is fixed by rules that never read the outcome" |
| 6.2 | "The tickets are frozen before the draw" becomes "Each ticket is the output of code released before the draw and given only the draws before it" |
| 6.3 | none |
| 6.4 | replaced by 2.2; the report prints, beside the score, the counted draws, how many variant-forecasts were made before their draw and how many were caught up, and the witness counts as now |
| 6.5 | the paragraph "Registered before its first draw" is replaced by 2.3 and 2.4; "counted, skipped (V = 0) or missed (6.8)" becomes "counted, or factor 1 by 2.4". The formal result, the no-reset rule and the numerical contract are unchanged |
| 6.6 | none (the new examples are added by reference) |
| 6.7 | replaced by 2.6 |
| 6.8 | replaced by 2.5 |
| 7.3 | adds: the reconstruction file is rewritten with the new variant in it |
| 0, 1A, 13, 14 | wording that follows from the above |

**Other governing documents:** the code plan v0.3 (the recorder's layer and its test rows); the change note
`OWNER_CLARIFICATION_2026_11_18_EQUAL_DRAWS_AND_OV1_USES` (its "formal prospective" use is now the prevailing score);
the deployment design note (section 6 below); R3's measure entry keeps its label "exact test martingale". Design
v0.1r7's classes and Appendix I are not changed.

**Staged code interfaces affected (for the later code round; nothing is coded now):**

| File (slice) | Effect |
|---|---|
| `src/evaluation/ov1.py`, `Method_OV1.py` (2) | Much smaller: `record`, `status`, `verify` stay; `register`, `stop`, `cutoff`, `reconcile`, the registration, and the line kinds other than the one factor line go |
| `src/evaluation/ov1_numeric.py` (2) | none |
| `src/Weekly_Session_Orchestrator.py` (2) | calls `record` after scoring only; the "stopped" state and its messages go |
| `src/evaluation/consolidated_report.py`, `ov1_retrospective.py` (3) | labels; the prevailing score's part reads the new ledger; the before/caught-up counts |
| `src/Development_Batch_Orchestrator.py` (3) | writes the reconstruction file after an admitted fill |
| `tests/test_mhupb_ov1.py` and the report tests | rewritten for the rule above; the kernel's tests untouched |
| `weekly_session.py`, `weekly_records.py`, the league code | none |

The passed slices are not reopened as slices; these changes arrive in the integrated package and are reviewed there.

## 6. What this does to the deployment design note

Its section 9 (formal OV-1 after a restore) is replaced by one paragraph: **a restore has no OV-1 side effect.** The
ledger comes back as it was in the backup; the lost draws are caught up by the ordinary session and counted by 2.2;
nothing reads the set-aside tree. The restore notices and everything listed under "Deleted" above leave the note. The
deployment note DRAFT v0.4, sent with this document, carries this together with EX_252's corrections.

## 7. Alternatives considered

1. **A draw not forecast beforehand counts as neutral (factor 1).** It needs a clock rule to say what "beforehand" is,
   a rule for what a restore does to draws that were counted, and something to stop a backup being chosen to shed
   draws: the machinery being removed. Example 3 shows it also changes the number for no scientific reason. Not
   proposed. (The owner: caught-up draws count, if the reviewer concurs.)
2. **Start at the first draw after production is installed,** not after ratification. Stricter in appearance: nothing
   made before the recorder's code was final could count. It costs each game the draws between ratification and the
   install. I propose the start at ratification, because the rule, the methods and the kernel are all fixed by then,
   and what the later code must compute is fully determined by them. The reviewer may prefer the stricter start.
3. **Keep the pre-draw witness line as an optional extra.** A second kind of line with no rule resting on it. Not
   proposed; the count of forecasts made before their draw carries the same information.
4. **Recompute the score on demand and keep no ledger.** Possible, since it is a function of the other records. The
   ledger is kept because an append-only record that must equal its rebuild is a cheap, strong check against silent
   change.

## 8. The guarantee and its limits (EX_253 E)

**Claim, per game:** if the draws are fair, the chance that the prevailing score ever reaches 40 is at most 2.5%,
however often it is looked at and whatever methods are added, revised or retired along the way.

**It holds under four conditions.**
1. **Isolation.** Each counted forecast was computed by code given only the draws before its target. (Enforced by the
   driver; tested.)
2. **Released first.** Each counted forecast is by a revision released before that draw, running the code,
   configuration and seed rule of that release. (The release records and identity digests; the test of 2.3.)
3. **Every draw once.** From the start, in draw-number order, each draw exactly once, with factor 1 only by 2.4.
   (The recorder; `verify`.)
4. **Honest operation.** The software and the records work as specified and are not altered. And the few decisions
   that can change what is computed for a draw already made but not yet in the ledger (which backup to restore;
   retiring a revision, or changing the Python environment, before a catch-up) are not made in order to move the
   score. Example 5b shows why this must be said. It is a condition on conduct; no machinery is added to police it.

**Why this is enough.** The mathematics needs each draw's weights to be fixed by things that do not depend on that
draw's result. It does not need them to have been computed before the draw. Conditions 1 and 2 give exactly that.
Choosing or changing methods in the light of **earlier** draws is allowed: that is what "given the past" means.

**What differs between the two kinds of counted forecast.** For one made before its draw, conditions 1 and 2 are also
backed by a physical fact: the result did not exist. For one caught up afterwards they rest on the software's
isolation and on the release record. That is a weaker kind of evidence for the same condition, and the report prints
the split so a reader can weigh it. The local clock is no longer part of the claim except through the release record's
day.

**What the claim never covers:** the exploratory view; the league table and every ranking; any back-history; Mode H;
a product or sum over both games. A crossing challenges the fair-draw assumption for that game. It is not proof of a
cause and promises nothing about later draws. A strong historical effect is worth investigating whether or not this
claim applies to it.

## 9. Not tested, and uncertainties

- The examples use toy methods and a 35-number barrel. They show the rules, not the real methods' behaviour.
- Whether every real method gives byte-identical forecasts when replayed in the same environment is asserted by the
  method contract (E2R-1 7.1) and exercised by the project's tests, not proved for every future method. Under this amendment a
  difference changes the number, not the validity (example 5c).
- A variant retired between a draw and its catch-up is not on the roster and so is not listed in that draw's line as
  "not counted". Condition 4 covers the conduct; the line does not show it. I judged a retirement-aware roster too
  much machinery for the case; the reviewer may disagree.
- The draws between ratification and the first production session will all be "caught up". That is the cost of
  alternative 2 not being taken, and it is visible in the report.

## 10. For the reviewer

1. Does the owner's condition hold: do you concur that caught-up draws count (2.2), on the argument of section 8?
2. Is condition 4 stated strongly and plainly enough, without machinery?
3. The start: at ratification (proposed) or at the first production install (alternative 2)?
4. Is anything in "Deleted" still needed for the correctness of the number, as distinct from the old label?
5. The reconstruction file made automatic (section 3, step 3): does it meet the owner's correction on historical
   rankings as you understood it from him?

End of the amendment, DRAFT v0.1.
