# MHUP-B design supplement - v0.7 (RATIFICATION CANDIDATE)

**Status: RATIFICATION CANDIDATE, by the Claude web chat (17 November 2026). The reviewer passed draft v0.6 as a design
and recommended ratification with one condition, RC-1 (EX_213). v0.7 is v0.6 with RC-1 written into section 6.8 and
nothing else changed. It is in force only when the project owner ratifies it. Ratifying it approves a design: it
authorises no code, run, rescore, re-forecast or install, each of which needs its own go.** Drafts v0.1 to v0.6 are kept
in the same folder as history. It supplements the ratified design
(`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`, "the design" below).

**Review record:** EX_207 (v0.1), EX_208 (v0.2), EX_209 (v0.4), EX_211 (v0.5), EX_213 (v0.6: focused design pass). **Gates left
for the code round** (EX_213): the numerical implementation and its error bounds; the adapters against the actual score
schemas; de-duplication and correction-chain tests; eligibility crash and restart tests; isolation of the live path from
the reporting layers; the full suite and the install rehearsal on Windows.

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
- **Decided by the owner (entry 55): one score for each game**, Powerball and Oz Lotto, each with a bar of 40. Games are
  never pooled and no joint figure is made.
- **It starts with the future.** The test is registered before the first draw it will count, and it counts every eligible
  forward draw from then on, once each. Nothing already drawn can enter it.
- **What it can show, honestly:** in a simulation, with the numbers leaning about as much as a 20% tilt, a game's score
  reaches its bar in about 190 draws (median; under four years of that game). A 10% tilt takes several times longer. A
  guide only.

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
| EX_209 B01 | The primary test is registered before its first contributing draw, starts at the first future target and counts every eligible draw once | 6.5, 6.8 |
| EX_209 B02 | The numerical contract: the software's score may never exceed the mathematical score | 6.5, row L5 |
| EX_209 C01 | The comparison with the sealed forecasts is of named forecast content, under stated preconditions | 7.2 rule 7 |
| EX_209 C02 | "Every draw" means a score or a typed status for every eligible target | 7.3 |
| EX_209 C03 | Each writer and its path named; the search log is not optional | 4 rule 4 |
| EX_209 C04 | The OV-1 ledger is create-only and bound to the freeze line and the outcome pin; resumption rules | 6.8 |
| EX_209 C05, R-3 | Option P decided; Option J unselected, not generated and not displayed | 6.3 |
| EX_209 R-5 | The selected score version is bound by identity, never by time or by value | 4 rule 2 |
| EX_211 F01 | A missing pre-outcome eligibility line stops the primary stream openly; it is never skipped or back-filled silently | 6.8 |
| EX_211 F02 | Every running component, the mixture and the comparison with 40 use a proved lower bound, or no crossing is claimed | 6.5 |
| EX_211 C03 | "Opens nothing for writing" applies to the reporting adapters and formatters, not to the forecasting and scoring halves | 4 rule 4 |
| Owner D-11, EX_211 | A `current` folder of copies and a permanent create-only archive, with a whole-set integrity rule | 5.1 |
| EX_213 RC-1 | No automatic new allowance after a stopped stream; recovery only by a rule fixed in advance and blind to the result | 6.8 |
| Owner, entry 51 | Full scope; one overall measure beside all others | 2, 6 |
| Owner, entry 53 (new in v0.3) | The holdout draws open to re-forecasting by every variant; the sealed forecasts kept as separate history | 3.2, 4, 6.7, 7 |

## 2. The package in layers (EX_207 R-4)

| Layer | Contents | Depends on | Acceptance gate (all on invented data unless the owner gives a separate go) |
|---|---|---|---|
| L1 | The `CATCH_UP` mode and tier, `FINAL_NEXT_DRAW` opened for ticketed session requests (design 6.4; E2R-1 amendment) | MHUP-A | The gate matrix of Appendix E passes; every refused combination refuses |
| L2 | The forecasting half, the freeze line, the forecast and witness ledgers (design 6.3, 6.5) | L1 | Appendix F's states and Appendix G's lifecycle, with interruption at every step |
| L3 | The scoring half and the score ledger (design 6.6) | L2 | Nothing scored twice; a second routine score for the same scientific identity refuses |
| L4 | The league table, its files, the history file (sections 3 to 5) | reads L3's ledger and the other sources | Section 4's contract: duplicate, overlap and missing-source cases each refuse or degrade as written |
| L5 | The overall measure (section 6) | reads L2 and L3 | The exact distribution against brute force for both games; each factor's fair-draw mean equal to 1; the reviewer's counterexample reproduced; incomplete pairs excluded; the numerical contract of 6.5 on adversarial weights and long runs; changing rosters and history-dependent weights; interruption and restart giving the same ledger bytes |
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
   correction exists, the one used is the one **named by its record identity** in `LEAGUE_SOURCES_<GAME>.json` (entered
   by a reviewed step on the owner's go); it is never chosen by creation time or by which figure is more favourable. The
   original stays in its source and is listed. If two sources or two listed attempts hold the same key without such a
   named selection, or a correction chain branches, cycles or has conflicting heads, the table **refuses** and names the
   key. Nothing here can change a sealed Mode H result.
3. **Missing source.** If a listed source is absent or fails its identity check, the all-draws block prints "not available:
   <source>" for the affected variants. A partial total is never shown as a total.
4. **Who writes what** (EX_209 C03; EX_211). The reporting source adapters and the table formatter are read-only towards
   every source: they open no sealed Mode H path, no freeze line and no score ledger for writing, and they write only
   the table files under `results/method_rankings/<GAME>/league/` (5.1). The orchestrator, and only it, appends the
   `WEEKLY_TABLE` row to the search log (required, never optional) and the OV-1 lines to their own create-only ledger
   (6.8). The forecasting and scoring halves (L2, L3) keep the duties the design gives them: they, and nothing else,
   create freeze lines and score lines. The table rescores nothing.
5. `LEAGUE_SOURCES_<GAME>.json` is changed only by a reviewed step on the owner's go (for example after the Powerball
   1145-1285 report run of section 8).

## 5. Files, archive and history (D-2 to D-4; EX_207 R-5 D)

**5.1 Names.** `league_<GAME>_d<draw, 5 digits>_v<version, 5 digits>_<UTC date-time>.txt`, with the same as `.csv`.
Each table set (the `.txt` and `.csv` of one publication) is logged in the search log (`WEEKLY_TABLE`).
- **The archive**, `results/method_rankings/<GAME>/league/archive/`: every published set, written once, tracked, and never
  moved, changed, deleted or rewritten. Its paths are the ones the search log records. **The archive is the record.**
- **The current folder**, `results/method_rankings/<GAME>/league/current/` (owner input D-11): copies of the newest complete
  set only, so the current ranking is the only thing in it. It is a convenience, not a source: nothing is ever computed
  or reconstructed from it. Replacing these copies is allowed; replacing an archive file never is.
- **Whole sets only** (EX_211). The members of the current set share one archived publication identity. The new set is
  prepared and checked in full before it becomes visible. If an interruption leaves an incomplete or mixed copy, the
  folder holds a `CURRENT_COPY_INCOMPLETE` notice and is not called current until the copy is repeated from the archive.
  A failed copy never affects the archived publication.
- Retired revisions stay labelled as such and their results are never merged with a current revision's.

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

**6.3 Scope: per game (DECIDED by the owner, 17 November 2026, decision log entry 55).** One evidence score for Powerball
and one for Oz Lotto, each on its own game's main barrel, each two-sided, each with half of the 5% (bar 40). R3 17.3.1
stands unchanged: "Games are never pooled. Every table, statistic, file and ranking belongs to one game." The two results
together keep the programme at or under 5% by the union bound, which needs no independence between the games.
*Not selected:* a joint score for both games (v0.4's Option J). **It is not computed, stored or displayed.** (The reviewer
also notes that a product of two separately valid scores is not automatically valid: it would need one joint sequence of
events and a joint fair-draw assumption, with care over draws on the same date.)

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
- **Formal result:** a game's score reaches **40**. A crossing challenges the fair-draw assumption for that game; it is not
  proof of a cause, nor a promise about future draws.
- There are no scheduled readings, no cut-off from a normal approximation, and no reset: the score runs on from its value,
  whatever methods are added, revised or retired.
- **Registered before its first draw** (EX_209 B01). One record per game fixes the game, the first eligible target, the
  formula of 6.1, the six lambdas and their equal weights, the bar, the pair and V = 0 rules, the freeze-time eligibility
  rule and the error budget. It is created before the first contributing target is drawn, and before that target's
  forecast is frozen. The score starts at that first future target. **No draw already made, and no forecast whose outcome
  was known when this statistic was chosen, can ever enter it.** From the start, every eligible forward draw is included
  exactly once, including skipped (V = 0) draws with factor 1; none is dropped, repeated or recomputed.
- **The numerical contract** (EX_209 B02). The theorem is about exact arithmetic; software uses rounded arithmetic. So:
  the distribution of X is held in exact integers; each log-factor is computed in high-precision decimal arithmetic with a
  stated error bound and is then **lowered by a fixed safety margin larger than that bound**, so the stored factor is never
  above the true one. **The same holds for everything built from the factors** (EX_211 F02): each of the six running
  components, their mixture, and the comparison with 40 are carried as proved lower bounds on their exact values, with
  the rounding of every sum, exponential and logarithm accounted for. A crossing is declared only when the proved lower
  bound of a game's score is at least 40. If such a bound cannot be established for some step, the program refuses to
  claim a crossing; ordinary decimal precision is never taken as proof. The loss of sensitivity from the margin is
  expected to be negligible; its size is to be shown in the code round under the bounds actually implemented, including
  how the guarantee continues beyond any stated number of draws. The score is accumulated in logarithms; a non-finite
  value refuses; a second update for the same draw refuses; and rebuilding the score from the ledger gives the same bytes.
- **OV-1 is the only confirmatory test of the forward phase.** The 80-track families and every other measure are reported
  in full and labelled secondary, exploratory (the reviewer's preferred simple option, EX_207).

**6.6 What the checks show** (`ov1_eprocess_check.py` and its output, in this folder; invented fair draws only).
- The reviewer's counterexample is reproduced exactly: with identical tickets, P(|S_104| >= 2.5758293) = 0.0107176149616,
  above 1%. So v0.2's five readings were nominal only, and they are withdrawn.
- For seven weight patterns in both games, each factor's fair-draw mean equals 1 to 16 decimal places, and the exact
  variance equals the formula.
- Under fair draws, in 20,000 runs of 1,040 draws each, a score ever reached 40 in 1.3% to 1.4% of runs (bound 2.5%).
- With the draws leaning so that Z averages about 0.22 a draw (roughly v0.2's "20% tilt"), a score reached 40 after a
  median of 190 draws (80% of runs by 297). At about 0.11 a draw ("10% tilt"): a median of 710. At about 0.35: a median of
  100. These depend on the kind of lean simulated; they are a guide and promise nothing.
- The check uses fixed weights. It does not exercise changing rosters, history-dependent weights or restarts: the theorem
  covers them, and the code round's tests must (row L5).

**6.7 Elsewhere, as description only.** For catch-up and development draws the table may show the same Z values, labelled
retrospective, with no evidence score and no P value. **For the holdout draws nothing of OV-1 is computed by default**
(EX_208 R-6). If the owner later wants it, that is a separate decision, labelled post hoc and kept outside the sealed
study's records.

**6.8 What it needs in the records** (EX_209 B01, C04).
- **The registered test record**, one per game, as 6.5 says: created before the first contributing target is drawn.
- **Two create-only lines per counted draw** in a small ledger of its own. The *eligibility line* is written when the
  freeze line closes, before the outcome exists: game, target, the registered test's identity, the freeze line's identity,
  the eligible variants' count and digest, the weights' digest, V and whether the draw will be skipped. The *factor line*
  is written at scoring: the eligibility line's identity, the outcome pin (master version and SHA-256), X, Z, the six
  log-factors and the running score. A factor line without its earlier eligibility line refuses.
- **Who writes them, and when** (EX_211 F01). The orchestrator calls the OV-1 recorder as soon as a freeze line closes,
  before the session ends and so before the outcome exists; the recorder needs only the frozen tickets. It is not part
  of table publication: a failed league table never prevents it, and its own failure never undoes or delays a freeze.
- **A missing eligibility line stops the primary stream, openly** (F01). The stream is a strict sequence. If, for a frozen
  prospective target, the eligibility line cannot be written and made durable before the outcome is known, the session
  record and every report say **"OV-1 eligibility NOT VERIFIED - PRIMARY STREAM STOP"** for that game from that target. No
  factor line is appended for that target or any later one; the target is not skipped, a later draw is not treated as the
  next, and nothing is back-filled with hindsight. The genuine forecast, its scores and the failure evidence are kept, and
  forecasting and scoring continue as normal.
- **After a stop** (EX_213 RC-1). Every new registration has a distinct test identity and must receive an explicit,
  reviewed error-budget allocation across all confirmatory registrations; there is no automatic reset and no reuse of
  the earlier per-game 2.5% allowance. A recovery after the outcome may continue the original stream only under a
  reconstruction rule fixed in advance and independent of the outcome, which accounts for every eligible draw; the
  owner's decision to recover may not depend on whether the resulting factor would be favourable. Building a line after
  the outcome is never assumed to be equivalent to the pre-outcome record.
- A skipped draw (V = 0, factor 1) is a recorded eligibility decision and is distinct from a missing or failed line.
- **Interruption.** A resumed session never writes a second line for a draw, never omits an eligible draw, and never
  recomputes a line with a different roster: it reads what is there and continues. The tests interrupt exactly between
  the freeze and the eligibility line.
- **Later information changes nothing already written.** Witness status may be reported beside the score at any time; it
  never alters a past line or a past eligibility decision.
- A new measure entry and calibration label in the registry and R3 (provisional name OV-1; label "exact test
  martingale").

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
7. **The comparison with the sealed forecasts** (EX_209 C01). The two records cannot be byte-identical: the re-forecast's
   run mode is development and the sealed one's is holdout, and the method contract's identity guarantee (E2R-1 7.1) needs
   the same run mode. So the batch's report compares **named forecast content only**: the ranking of the numbers with its
   scores and ties, and the TOP and WORST sets; mode-specific fields are left out. It states for each pair whether these
   preconditions hold: the same method declaration, code and revision; the same view and N-1 history; the same
   configuration, seed policy and identity, tie-break version and relevant environment; and a method whose forecast does
   not depend on the run mode. It lists every pair compared, every difference, the inputs' identities and the likely
   cause. A difference is information for the owner and the reviewer, not automatically a fault, and it changes nothing
   in the sealed study.
8. **Counted once.** In every table a variant's result for a holdout draw is counted once, from its walk-forward record. The
   Mode H result is shown beside it as history and is never added again (3.2, section 4).
9. The weekly session still never forecasts a holdout target: its scope starts at `holdout_last + 1`, as the design says.

**7.3 "A new method re-ranks all draws."** After 7.1 every variant, old or new, has for every eligible draw either a
walk-forward score or a typed status (`INSUFFICIENT_HISTORY`, a failure record); a status is never shown as a score. The
next league table then ranks them all over their scored draws, as a new numbered file. Earlier tables are
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
- **A joint score for both games:** not selected by the owner (entry 55); not computed or displayed (6.3).
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

**The reviewer's recommendation (EX_213):** ratify, with RC-1 (now in 6.8).

**The owner's decisions** (his position is in decision log entry 59):
- O-1. The table and files of sections 3 and 5.
- O-2. OV-1 as the one confirmatory forward test for each game, by the evidence score of 6.5 with a bar of 40, everything
  else secondary.
- O-3. The window contract and re-forecasting rules of section 7.
- O-4. The objective of scoring Powerball targets 1145-1285; the run itself needs a separate go once its command is reviewed.

## 14. Not tested; what the code round must show

Nothing here has run against project data. The simulation uses invented draws and one tilt model. The code round must
show: the exact distribution and variance against brute force for both games; the import-isolation test and fault injection
at every interface between the live path and the reporting layers, with the accepted ledger and freeze bytes unchanged;
each refusal of sections 4 and 7; the source adapters tested against the actual schemas of the existing score records;
and a session interrupted at every step with the table layer made to fail.

End of v0.7.
