# MHUP-B design supplement - DRAFT v0.4

**Status: a draft by the Claude web chat (17 November 2026, on Fable). Not ratified. It authorises no code, run, rescore or
install.** It replaces drafts v0.1 to v0.3 (kept in the same folder as history). v0.4 answers the reviewer's review of
v0.2 (EX_208: recheck required on four points; section 1). It applies the owner's decisions of
17 November 2026 (decision log entry 51: a full MHUP-B, and one overall measure beside all the others; entry 53: the
holdout draws opened to re-forecasting, with the sealed forecasts kept as separate history) and the reviewer's review of
v0.1 (EX_207: conditional pass on direction, with corrections) to the ratified design
(`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`, "the design" below).

## 0. In plain English

- **One package, built in layers.** MHUP-B carries the weekly session, the league table and its files, one overall measure,
  a new method's back-history, the report window extended past the holdouts, a consolidated report, and the scoring of the
  early Powerball draws. Each layer has its own tests, and the weekly forecasting and scoring never depend on the reporting
  layers: a fault in a table can never stop a forecast being frozen.
- **All draws and all methods go through the same pipeline** (the owner's decision, v0.3). The holdout draws can be forecast
  again by any method, old or new, as ordinary walk-forward. The sealed Mode H forecasts, scores and reports stay exactly
  as they are, as separate history, and each draw is still counted only once in any total.
- **The league table** lists every released method and variant (those with no score yet are shown as such), with an
  all-draws column, a forward-only column and the split by kind of evidence. It is a description: no "significant" marks.
- **The one overall measure** (section 6) asks one question of every forward draw: *were the numbers the methods favoured
  drawn more, or less, than the numbers they disfavoured?* It is kept as a running **evidence score** that starts at 1 and
  is multiplied up or down by each draw. If the score ever reaches the bar, that is the formal result. The bar is set so
  that, under fair draws, the chance of ever reaching it is at most 5%, **however often anyone looks and however long it
  runs**. That is proven, not estimated (v0.4; it replaces v0.2's five readings, which the reviewer showed were not exact).
  Everything else is still reported and is labelled secondary.
- **One choice for the owner:** a score for each game (bar 40 each; no rule changes), or one score for both games together
  (bar 20; quicker if both games lean the same way, but it needs an exception to the ratified rule that games are never
  pooled). Section 6.3.
- **What it can show, honestly:** in a simulation, with the numbers leaning about as much as a 20% tilt, a per-game score
  reaches its bar in about 190 draws (median; under four years of one game) and the joint score in about 165 draws (under
  two years of both). A 10% tilt takes several times longer. A guide only.

## 1. What changed from v0.1, and where each of the reviewer's points lands

| EX_207 | Point | Here |
|---|---|---|
| R-1 | The all-history column stays descriptive; catch-up is not prospective; `PROSPECTIVE` (local clock) is not the same as witness-verified | 3.2, 3.5, 6.4 |
| R-2 | Sort key is descriptive only; LOW_N under 30; zero-score variants shown; stable tie-break; a matched-target view; never used to pick methods | 3.1, 3.3, 3.4 |
| R-3 | Planning figures restated; no power claim carried from one ticket to the aggregate; the aggregate fully specified; error budget; repeated looks | 6, 9 |
| R-4 | Full scope accepted, in independently tested layers with acceptance gates; the live path isolated; back-history rules; the window needs a contract | 2, 7 |
| R-5 A | Variants with no scores | 3.1 |
| R-5 B | A cross-source read contract | 4 |
| R-5 C | `LATE_PRE_DRAW` and publication status | 3.2, 3.5 |
| R-5 D | The past-draw rankings are a reconstruction, not what was published then | 5.3 |
| R-5 E | Class and release-date rules kept; create-only, logged tables | 3.5, 5, 7 |
| EX_206 Q2 | Coverage counts, denominators, window, revision and release timing, TOP and WORST, game and barrel all labelled | 3.2 |
| EX_208 R-1 | Only complete TOP and WORST pairs count; eligibility frozen before the outcome | 6.1 |
| EX_208 R-2 | Pooling the games conflicts with R3 17.3.1: put to the owner as an explicit choice | 6.3 |
| EX_208 R-3, R-4 | The five readings at 2.576 were nominal, not guaranteed (the reviewer's exact counterexample is reproduced); replaced by an exact test martingale | 6.5, 6.6 |
| EX_208 R-5 | Local-clock class for the formal sample, with the witness counts and the limitation printed | 6.4 |
| EX_208 R-6 | No overall measure on the holdout draws by default | 6.7 |
| EX_208 R-7 (1) | Back-history for weekly targets already closed before a variant's release | 7.1, 7.2 |
| EX_208 R-7 (2) | De-duplication by target and readout, not by scoring policy; one approved policy per figure | 4 |
| Owner, entry 51 | Full scope; one overall measure beside all others | 2, 6 |
| Owner, entry 53 (new in v0.3) | The holdout draws open to re-forecasting by every variant; the sealed forecasts kept as separate history | 3.2, 4, 6.7, 7 |

## 2. The package in layers (EX_207 R-4)

| Layer | Contents | Depends on | Acceptance gate (all on invented data unless the owner gives a separate go) |
|---|---|---|---|
| L1 | The `CATCH_UP` mode and tier, `FINAL_NEXT_DRAW` opened for ticketed session requests (design 6.4; E2R-1 amendment) | MHUP-A | The gate matrix of Appendix E passes; every refused combination refuses |
| L2 | The forecasting half, the freeze line, the forecast and witness ledgers (design 6.3, 6.5) | L1 | Appendix F's states and Appendix G's lifecycle, with interruption at every step |
| L3 | The scoring half and the score ledger (design 6.6) | L2 | Nothing scored twice; a second routine score for the same scientific identity refuses |
| L4 | The league table, its files, the history file (sections 3 to 5) | reads L3's ledger and the other sources | Section 4's contract: duplicate, overlap and missing-source cases each refuse or degrade as written |
| L5 | The overall measure (section 6) | reads L2 and L3 | The exact distribution against brute force for both games; each factor's fair-draw mean equal to 1; the reviewer's counterexample reproduced; incomplete pairs excluded |
| L6 | Back-history and the window contract (section 7) | the WF-1A driver and WF-1B report tool | No write under any sealed Mode H path; no freeze line touched; refused windows refuse |
| L7 | The consolidated report and the retired-revision index (section 8) | L4, L5 | Every figure traceable to a named source identity; no pooled P value exists anywhere in it |
| L8 | The orchestrator, `Run_Weekly_Session.bat`, the rulebook edition, the document amendments (section 11) | all | The install rehearsal on Windows, with a full-suite run after step 18 |

**Isolation rule (binding on the code round).** L1 to L3 are the live path. No module of L1 to L3 imports a module of L4
to L7. The session freezes the next forecast and closes its records **before** any table is written. A failure in L4 to L7
ends the session with a distinct exit status ("frozen; table not written") and never undoes, delays or reorders L1 to L3;
the table can be written afterwards by its own command as a new file. A static test enforces the import rule.

**STOP boundaries.** A STOP in L1 to L3 stops the session as the design says. A refusal in L4 to L7 is reported and leaves
the live path's records complete. No layer writes into a path another layer owns.

**Phasing remains the owner's option** (EX_207 R-4): if a reporting layer blocks, L1 to L3 can be released first. It is not
proposed now.

## 3. The league table (D-1; EX_207 R-1, R-2, R-5 A, C, E)

**3.1 Rows.** Every released method, revision and variant of the game: current ones, and retired ones marked "as published"
(design 6.6). A variant with no eligible score is shown as `NO_SCORES` and is unranked. A variant with fewer than 30 scored
draws is marked `LOW_N` and its rank is labelled provisional. A roll-up by method sits above the table.

**3.2 Columns.** Main table, for the TOP ticket (the seven most favoured numbers), main barrel:

| Block | Columns | Notes |
|---|---|---|
| All scored draws | Draws, Hits, Chance, +/- % | Every accepted routine score for that variant, once each, whatever its kind. The holdout draws enter through their walk-forward re-forecast (section 7), never by adding the sealed Mode H scores a second time. **No P value.** |
| Forward only | Draws, Hits, Chance | Effective class `PROSPECTIVE`. Beside it: how many of those draws are witness-verified (design 6.5). The two are never merged |
| Last 10 | Hits | The ten latest scored draws |

A second table with the same rows gives the split by kind in separate columns: development (which includes the
re-forecast holdout draws), catch-up, `LATE_PRE_DRAW` and forward; and beside them **Mode H as sealed** (history: shown,
never added to a total). It also gives the WORST ticket, the Powerball barrel for Powerball, the prize divisions, and for
each variant its revision, release date, first and last scored target and count of missing or failed targets. Game-specific
denominators are printed in the header (Powerball: 7 from 35, chance 1.4 a draw; Oz Lotto: 7 from 47, chance 49/47 a draw).

**3.3 Order.** By hits above chance per draw over all scored draws. Ties, and any comparison where the forward column has
fewer than two draws, are broken by a fixed identity order (method, revision, variant), never by a rate from one draw.
The header says: "A descriptive order. It does not select a winner and is not used to choose methods."

**3.4 Matched-target view.** The full report carries the comparison on matched targets (R3 17.3.7): variants compared only
over the draws all of them have. The weekly table does not.

**3.5 What is never done.** `LATE_PRE_DRAW` is counted once in the all-draws total, shown in its own column, and never in
the forward column. A record's class is fixed by the design's rules (6.4, Appendix I): a forecast made after its draw's
result existed is development evidence for that draw, for ever. Exposure flags print as the design specifies. The table
selects nothing: a rule that chose methods by this order would be a new method needing its own registration.

## 4. The cross-source read contract (EX_207 R-5 B)

The design builds the weekly table from the weekly score ledger and refers to the other evidence. The all-draws column
goes further: it sums across sources. That is a new reporting contract:

1. **Sources, read-only, each named by identity in the table's header.** Summed into the all-draws column: (a) the weekly
   score ledger; (b) the development score records of the report attempts listed in a small tracked file,
   `LEAGUE_SOURCES_<GAME>.json`, each with its attempt identity and window (the re-forecast holdout draws arrive here).
   **Shown but never summed:** (c) each game's sealed Mode H score ledger, used only for the separate "Mode H as sealed"
   column and the comparison of 7.2 rule 7, and only if its SHA-256 equals the one its `SCORE_COMPLETE` record holds.
2. **One score per draw and readout** (EX_208 R-7 (2)). The key is (game, method, revision, variant, target, barrel, TOP or
   WORST). The scoring policy is **not** part of the key: the design lets a corrected score stand beside the original
   (6.6), and both must never be summed. For each figure the table names one approved scoring policy; where an accepted
   correction exists under that policy (its `amendment_of` chain), the latest accepted one is used and the original is
   kept and listed. If two sources, or two listed attempts, hold the same key, or a correction chain is ambiguous, the
   table **refuses** and names the key. It never picks one.
3. **Missing source.** If a listed source is absent or fails its identity check, the all-draws block prints "not available:
   <source>" for the affected variants. A partial total is never shown as a total.
4. **Nothing is written** outside `results/method_rankings/<GAME>/league/`. No sealed path is opened for writing. The table
   rescores nothing.
5. `LEAGUE_SOURCES_<GAME>.json` is changed only by a reviewed step on the owner's go (for example after the Powerball
   1145-1285 report run of section 8).

## 5. Files, archive and history (D-2 to D-4; EX_207 R-5 D)

**5.1 Names.** `league_<GAME>_d<draw, 5 digits>_v<version, 5 digits>_<UTC date-time>.txt`, with the same as `.csv`.
Create-only, tracked, each logged in the search log (`WEEKLY_TABLE`). The newest is the current ranking; every earlier one
remains as published.

**5.2 The history report** joins the published tables, newest first. It recomputes nothing. This is the genuine record of
what was known at each date.

**5.3 The reconstruction file** (one CSV per game, on request) has a row per draw and variant: that draw's matches, running
totals and "rank after that draw". Its header and every row carry the label **"current-cohort historical reconstruction
as of <date>"**. It is not what was published at those dates: a variant released later appears in it from the first draw
with its back-history. A column gives, for each row, whether the variant was released at that draw's date.

## 6. The one overall measure, OV-1 (owner decision 51; EX_207 R-3; EX_208 R-1 to R-6)

**6.1 Definition.** For one forward draw of one game, take every variant that has, for that target, a **complete valid pair**
of frozen TOP-seven and WORST-seven tickets of class `PROSPECTIVE`. A variant with only one of the two, a failure record, a
late or otherwise ineligible record contributes nothing at all; nothing is imputed. Eligibility is fixed and recorded
before the outcome is read. For each number j of the main barrel let

    w_j = (how many of those variants have j in their TOP seven) - (how many have j in their WORST seven)

    X = the sum of w_j over the seven numbers drawn

Because every counted variant adds seven +1s and seven -1s, the weights sum to zero, and under a fair draw X has mean
exactly 0 and variance exactly V = K (N - K) / (N - 1) * (1/N) * sum of (w_j - mean of w)^2 (K = 7; N = 35 or 47).
The draw's score is Z = X / sqrt(V). A draw with V = 0 is skipped and counted as skipped.

**6.2 Why this form.** Shared numbers are handled exactly. The tickets are frozen before the draw, so the argument holds
when methods learn from earlier draws and when variants join or leave (through each draw's freeze line, design 6.3); no
roster is changed for a target already frozen. X needs only the scores already kept; V needs only the frozen tickets.

**6.3 Scope: the owner's choice** (EX_208 R-2). R3 17.3.1, ratified, says: "Games are never pooled. Every table, statistic,
file and ranking belongs to one game."
- **Option P (per game; recommended by the reviewer, and by Claude):** one evidence score per game, each with half the 5%
  (bar 40). No ratified rule changes. A real effect in one game is not diluted by the other, and the plausible causes of
  any real effect (a machine, a ball set) belong to one game.
- **Option J (joint):** one score for the whole programme, the product of the two games' scores (bar 20). About twice as
  quick if both games lean the same way; slower than P if only one does. It needs an explicit owner-approved exception to
  R3 17.3.1 for this one statistic; every table, ranking and file would still be per game.
In both options the test is **two-sided**, on the main barrel, and the other option's figure is shown as secondary.

**6.4 Which records count** (EX_208 R-5). Class `PROSPECTIVE` only, as the design defines it from the local frozen-at time
(6.4, Appendix I). Beside every formal figure the report prints the number of counted draws, how many are
witness-verified, how many lack a witness, and the sentence "class PROSPECTIVE rests on local timing and tamper-evident
records; it is not external proof of pre-draw publication". A witness-verified-only series is shown as description and is
never a second formal test.

**6.5 The formal rule: an exact evidence score** (EX_208 R-3, R-4). For the frozen weights of a draw, the fair-draw
distribution of X is computed **exactly** (a small dynamic programme over the numbers; integers only). For each fixed
lambda in the set L = {-0.20, -0.10, -0.05, +0.05, +0.10, +0.20} the draw's factor is

    f(lambda) = exp(lambda * Z) / E0[ exp(lambda * Z) ]        (E0: the exact fair-draw mean, from that distribution)

Each factor has fair-draw mean exactly 1 given the past. The evidence score after n counted draws is

    E_n = the average over lambda in L of ( f_1(lambda) * f_2(lambda) * ... * f_n(lambda) ),   E_0 = 1

Under fair draws E_n is a nonnegative martingale, so the chance that it **ever** reaches 1/a is at most a (Ville's
inequality), for every admissible sequence of frozen weights, adaptive or not, and for every way of looking at it.
- **Formal result:** Option P: a game's score reaches **40** (2.5% each, 5% in all). Option J: the joint score reaches **20**.
- There are no scheduled readings, no cut-off from a normal approximation, and no reset: the score runs on from its value.
- L, the bar, the eligibility rule and the option are fixed in one registered record before the first counted draw.
- **OV-1 is the only confirmatory test of the forward phase.** The 80-track families and every other measure are reported
  in full and labelled secondary, exploratory (the reviewer's preferred simple option, EX_207).

**6.6 What the checks show** (`ov1_eprocess_check.py` and its output, in this folder; invented fair draws only).
- The reviewer's counterexample is reproduced exactly: with identical tickets, P(|S_104| >= 2.5758293) = 0.0107176149616,
  above 1%. So v0.2's five readings were nominal only, and they are withdrawn.
- For seven weight patterns in both games, each factor's fair-draw mean equals 1 to 16 decimal places, and the exact
  variance equals the formula.
- Under fair draws, in 20,000 runs of 1,040 draws each, the score ever reached 20 in 2.8% to 3.0% of runs (bound 5%) and
  ever reached 40 in 1.3% to 1.4% (bound 2.5%).
- With the draws leaning so that Z averages about 0.22 a draw (roughly v0.2's "20% tilt"), the score reached 40 after a
  median of 190 draws (80% of runs by 297) and reached 20 after a median of 163 (80% by 254). At about 0.11 a draw ("10%
  tilt"): 710 and 567. These depend on the kind of lean simulated; they are a guide and promise nothing.

**6.7 Elsewhere, as description only.** For catch-up and development draws the table may show the same Z values, labelled
retrospective, with no evidence score and no P value. **For the holdout draws nothing of OV-1 is computed by default**
(EX_208 R-6). If the owner later wants it, that is a separate decision, labelled post hoc and kept outside the sealed
study's records.

**6.8 What it needs in the records.** One line per counted draw in a small create-only ledger: game, draw, the freeze
line's identity, the eligible variants' count and digest, X, V, Z, the six factors and the running score. A new measure
entry and calibration label in the registry and R3 (provisional name OV-1; label "exact test martingale"), and one
registered primary-test record holding 6.1 to 6.5, created before the first forward draw is scored.

## 7. Back-history and the window contract (D-5, D-9; EX_207 R-4, R-5 E)

**7.0 The owner's decision of 17 November 2026 (entry 53):** "Retain current forecasts as separate history but
specifically open up holdouts to reforecasting ... so everything draws and methods all get treated the same." So there is
one rule for every variant, old or new, and no special case for the Mode H cohort.

**7.1 What every variant gets.** (a) Draws after the holdout and before its release: the weekly session supplies these
only while their weekly target is still open (design 6.4). **A weekly target already closed is never reopened for a
variant released later (design 6.3)**, so for those draws the variant gets a development back-history batch (rule 2A
below; EX_208 R-7 (1)). (b) Draws up to the end of the holdout: development walk-forward by the
existing driver, from the game's first target to `holdout_last`. For a new variant that is one batch over the whole range.
For the 40 variants of the Mode H cohort, which already have development forecasts up to the old cap, it is one batch over
the ten holdout targets (400 forecasts a game, the size of the Mode H batches).

**7.2 The window contract** (an R3 17.3.6 amendment, not a bound edit). For development batches and reports of a game:
1. Until that game's `MODE_H_SEALED` record exists, the Phase 1 cap stands (1576, 1693).
2. After it exists, the cap is `holdout_last` (1586, 1703) for every variant.
2A. **Beyond the holdout, for a variant released later:** a development batch may also cover any accepted target dated
   before that variant's release for which the variant has no weekly record of any kind. It is read-only towards the
   weekly records: it opens no freeze line and writes nothing to the weekly ledgers. It has its own source identity in
   `LEAGUE_SOURCES_<GAME>.json`, and section 4's one-score rule stops any overlap with a weekly record.
2B. "Every draw" always means every eligible draw: a variant without enough history for a target records
   `INSUFFICIENT_HISTORY`, and the table shows the counts of such targets and of failures.
3. A batch may include the holdout targets for **any** variant, including the 40 of the Mode H cohort. **The sealed Mode H
   forecasts, scores, markers and reports stay exactly as they are, as separate history.**
4. Every such forecast is development evidence. It can never be catch-up, prospective or Mode H evidence.
5. A back-history batch writes only under the development roots. It opens no freeze line, no weekly ledger and no sealed
   Mode H path for writing, and the Mode H study is never rescored.
6. Method-facing N-1 isolation, forecast identities and append-only records are unchanged.
7. **The comparison with the sealed forecasts.** Where a re-forecast is by the same method revision as the sealed Mode H
   forecast for that variant and target, the two forecasts should be identical. The batch's report lists every pair compared
   and every pair that differs. A difference is reported as a finding for the owner and the reviewer; it changes nothing in
   the sealed study. (For a revision changed since the seal, a difference is expected and is listed as such.)
8. **Counted once.** In every table a variant's result for a holdout draw is counted once, from its walk-forward record. The
   Mode H result is shown beside it as history and is never added again (3.2, section 4).
9. The weekly session still never forecasts a holdout target: its scope starts at `holdout_last + 1`, as the design says.

**7.3 "A new method re-ranks all draws."** After 7.1 every variant, old or new, has walk-forward scores for every
draw, so the next league table ranks them all over all scored draws, as a new numbered file. Earlier tables are
untouched, and the reconstruction file marks where a variant's history is back-filled (5.3).

## 8. The consolidated report, the retired index and the early Powerball draws (roadmap 21b; D-6)

- **The consolidated report** is the design's full report (6.6) with these parts, each from named sources and none pooled
  into a P value: the league table; OV-1 (its evidence score and whether the bar has been reached); the forward and
  catch-up family tables of 6.6, labelled secondary; the matched-target view; and the development and Mode H results quoted
  from their own reports by identity, not recomputed.
- **The retired-revision index:** a small tracked file listing each retired revision, its last scored target and where its
  records are.
- **Powerball targets 1145 to 1285:** scored by the installed report tool over that window (no family applies; development
  evidence), on the owner's separate go and after review of the command. Then its attempt is added to
  `LEAGUE_SOURCES_POWERBALL.json`. Until then the all-draws column starts at 1286 and says so.

## 9. Planning figures, restated (replaces v0.1 section 5; EX_207 R-3)

Under an idealised fixed-horizon calculation (normal approximation, one preselected ticket, one-sided, a simple shift in
its mean), about 780 Powerball draws give an 80% chance of passing for a 10% edge on one track in an 80-track family, and
about 195 for a 20% edge. These are planning figures for that one case. They are not a power analysis for weekly repeated
looks, for a changing roster or for OV-1, and they guarantee no result. OV-1's own figures are in 6.6.

## 10. Smaller items

- **HX-2** (Powerball 1587, 1588): kept as ratified. The exposure record is closed in register v0.31 with the HX-1 and HX-2
  facts preserved (EX_206 Q3).
- **The local runner's rules 4 and 5** stay binding until the rulebook edition installed with MHUP-B (EX_206 Q4). Proposed
  wording then: rule 4 withdrawn; rule 5 "you may read files under `source_data`, `results` and `transitory_data` when a
  task says so; you never create, change, move or delete anything there." Everything else in the rulebook stays, and the
  new programs join rule 7.

## 11. Documents to amend with the package

R3 (17.3.6 the window contract, with re-forecasting of the holdout draws after the seal;
17.5A and the registries for OV-1 and its label; the league table and reconstruction as
descriptive outputs); E2R-1 (9.1 and E2R-R41 for `CATCH_UP`, E2R-R44 for `FINAL_NEXT_DRAW`), as the design already lists;
the Architecture's next edition; the runner's rulebook; the design itself, by a short amendment naming this supplement.

## 12. Alternatives considered

- **Keep the 40 cohort variants barred from the holdout draws** (v0.2's rule): no duplicate records, but two classes of
  variant and a special case in every table. Withdrawn at the owner's decision. The duplication is turned to use: rule 7 of
  7.2 makes it a check that the pipeline reproduces the sealed forecasts.
- **Five fixed readings against a normal cut-off** (v0.2): simple to describe, but the reviewer's exact counterexample
  shows a reading can exceed its 1% allowance, so the 5% was nominal. Replaced by the exact evidence score, which is also
  simpler to operate: one number, one bar, valid at every look.
- **Per game or joint:** now the owner's explicit choice (6.3).
- **Raw sum of X divided by the root of summed V** (instead of equal weight per draw): gives draws with more variants more
  say. Defensible; rejected so that one period with many variants cannot dominate, and for the plainer description.
- **One-sided:** slightly more power in the favoured direction, but blind to systematic anti-prediction, which is as much a
  departure from randomness.
- **A wider or finer set of lambdas:** more components spread the evidence thinner. Six values cover leans from slight to
  strong in both directions; put to the reviewer (R-2).
- **An N1 replay of the aggregate:** only a reference for adaptive methods, by R3's own labels. The exact conditional
  variance does not have that weakness.
- **Total TOP minus WORST matches without the variance per draw:** its luck band would have to be estimated or simulated.

## 13. For the reviewer and the owner

**Questions for the reviewer**
- R-1. Section 6.1's complete-pair rule and 6.5's exact evidence score: is OV-1 now a valid finite-sample primary test for
  every admissible sequence of frozen weights?
- R-2. The lambda set of 6.5 and the equal-weight mixture: acceptable, or would you fix another?
- R-3. Section 6.3: is Option J's product of the two games' scores valid as stated, if the owner chooses it?
- R-4. Section 7 as revised: the holdout draws open to re-forecasting by every variant as development evidence only (owner
  decision, entry 53), the sealed records kept as separate history and never summed, the comparison of rule 7, and rule 2A
  for closed weekly targets. Do you agree, and is any further safeguard needed?
- R-5. Section 4 rule 2: does the de-duplication and correction rule close the gap you found?
- R-6. Anything in sections 2 to 8 still in conflict with the design or R3?

**Decisions for the owner (after the reviewer's view)**
- O-1. The table and files of sections 3 and 5.
- O-2. OV-1 as the one confirmatory forward test, by the evidence score of 6.5, with everything else secondary.
- O-3. **Option P (per game, bar 40) or Option J (both games together, bar 20, with an exception to R3 17.3.1).**
- O-4. The window contract and re-forecasting rules of section 7 (the owner's decision of entry 53 is built in).
- O-5. Later, a go for the Powerball 1145-1285 report run.

## 14. Not tested; what the code round must show

Nothing here has run against project data. The simulation uses invented draws and one tilt model. The code round must
show: the exact distribution and variance against brute force for both games; the import-isolation test and fault injection
at every interface between the live path and the reporting layers, with the accepted ledger and freeze bytes unchanged;
each refusal of sections 4 and 7; the source adapters tested against the actual schemas of the existing score records;
and a session interrupted at every step with the table layer made to fail.

End of draft v0.4.
