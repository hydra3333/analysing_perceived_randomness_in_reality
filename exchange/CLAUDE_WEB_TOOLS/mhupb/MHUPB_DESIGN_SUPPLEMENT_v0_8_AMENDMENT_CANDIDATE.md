# MHUP-B design supplement - v0.8 (AMENDMENT CANDIDATE)

**Status: AMENDMENT CANDIDATE, by the Claude web chat (17 November 2026).** A full edition: the supplement v0.7 as the
project owner ratified it on 17 November 2026 (RAT-33; SHA-256 `04c4f68a638fff7d93f06d25084d1454bdfc443e9aab6b0b12ffdfd8b5323d26`)
with the focused amendments listed in section 1A. They answer the reviewer's review of the code plan (EX_223: B01, B02,
B03, B04, C01, C02, C03) and follow the owner's directions OD-1 to OD-4 (decision log entries 69 and 70). Everything not
listed in section 1A is v0.7's text, unchanged; the builder `make_supplement_v0_8.py` makes it from v0.7's bytes by
counted edits. **Until the owner ratifies v0.8, v0.7 is the ratified edition and governs. Ratifying v0.8 approves a
design: it authorises no code, run, rescore, re-forecast or install, each of which needs its own go.** Drafts v0.1 to
v0.6 are kept in the same folder as history. It supplements the ratified design
(`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`, "the design" below).

**Review record:** EX_207 (v0.1), EX_208 (v0.2), EX_209 (v0.4), EX_211 (v0.5), EX_213 (v0.6: focused design pass); for
v0.8, EX_223 (the review of the code plan, which asked for these amendments). **Gates left
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
- **Amended in v0.8.** A missed week does not end the formal test: a draw for which no forecast set was frozen in time
  counts as neutral, by a rule fixed in advance that cannot see the result. A set that was frozen but whose pre-draw
  entry is missing still stops the test, and a stopped test stays stopped. Any runnable method can be run again over
  past draws for research; such reruns are kept apart and never change the league's totals.

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
| EX_223 B01; owner OD-2, OD-3 (v0.8) | Every target is one opportunity; a missed week is a neutral factor fixed in advance; the cut-off for the pre-draw entry | 6.5, 6.8 |
| EX_223 C02 (v0.8) | A failure is never a skip; blocked and stop; the factor table sealed before the outcome | 6.8 |
| EX_223 B03 (v0.8) | Back-history by the release instant, not the release date | 7.2 rule 2A |
| EX_223 B04; owner OD-1 (v0.8) | Routine fill and exploratory rerun; canonical and exploratory attempts | 7.1A, 4 rule 2A |
| EX_223 C01, C03, B02 (v0.8) | One writer per ledger; one small source file, with admission inside an approved workflow; a table is logged only when its set is complete | 4 rules 4 and 5, 5.1 |
| Owner OD-4 (v0.8) | A stopped stream stays stopped; no second registration in MHUP-B | 6.8 |

## 1A. What v0.8 changes in the ratified v0.7

Everything else is v0.7's text, byte for byte.

| Where | Change |
|---|---|
| Header, section 0, section 1 | Status and review record; one summary bullet; six table rows; this section |
| 4, after rule 2 | New rule 2A: canonical and exploratory attempts; the first admitted score is the canonical one |
| 4 rule 4 | One sentence replaced: who starts a publication, and the one writer of each ledger |
| 4 rule 5 | Replaced: one small tracked source file; routine admission is part of an approved workflow |
| 5.1 | One sentence added: a set is logged only when both archive files exist |
| 6.5 | What the registration fixes; "every target is one opportunity" |
| 6.8 | The two-lines bullet extended; "who writes" reworded; new: the cut-off, the opportunity rule, failures; "after a stop" replaced |
| 7.1A (new) | Two kinds of development run |
| 7.2 rule 2A | Replaced: by the release instant; exploratory reruns above the holdout |
| 7.3 | One sentence added |
| 11, 12, 13, 14 | The ER-6 note; three alternatives; the decisions O-5 to O-7; the code round's added proofs |

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
2A. **What the totals count, and what may be run (v0.8; owner OD-1; EX_223 B04).** Rule 2 governs the league's totals, not
   what may be run. A development attempt is either *canonical* (listed in `LEAGUE_SOURCES_<GAME>.json`; its scores enter
   the all-draws column) or *exploratory* (never listed; shown only in separate, labelled comparisons by named
   attempt). A routine-fill attempt (7.1A), or a report attempt over a plan of the first kind, is admitted as canonical
   by its own workflow only if no key it supplies is already supplied by a canonical source or by the weekly score
   ledger; otherwise it is not admitted and the table is unchanged. So the canonical
   score for a key is the first one admitted. It is never replaced because a later run is newer or more favourable. An
   exploratory rerun is never admitted. Replacing a canonical source is a correction: a reviewed, named change on the
   owner's decision.
3. **Missing source.** If a listed source is absent or fails its identity check, the all-draws block prints "not available:
   <source>" for the affected variants. A partial total is never shown as a total.
4. **Who writes what** (EX_209 C03; EX_211). The reporting source adapters and the table formatter are read-only towards
   every source: they open no sealed Mode H path, no freeze line and no score ledger for writing, and they write only
   the table files under `results/method_rankings/<GAME>/league/` (5.1). A publication is started only by the
   orchestrator or by the one named publish command it runs, which the owner may also run on its own. One writer, and
   only it, creates the table files and appends their `WEEKLY_TABLE` row to the search log (required for every
   publication, whoever started it). The OV-1 lines are appended to their own create-only ledger by the one OV-1
   recorder, started in the same way (6.8). Nothing else writes either (v0.8; EX_223 C01). The forecasting and scoring halves (L2, L3) keep the duties the design gives them: they, and nothing else,
   create freeze lines and score lines. The table rescores nothing.
5. `LEAGUE_SOURCES_<GAME>.json` is one small tracked file. It is changed only by the reviewed admission step of a
   workflow the owner has approved. Admitting a routine-fill attempt that conflicts with nothing (rule 2A) is part of
   that workflow's go and needs no separate one (for example the Powerball 1145-1285 report run of section 8).
   Anything that conflicts refuses; resolving it is a separately reviewed, named change on the owner's decision. Every
   published table names the file's digest and the exact sources it used; Git keeps the file's history (v0.8; EX_223
   C03).

## 5. Files, archive and history (D-2 to D-4; EX_207 R-5 D)

**5.1 Names.** `league_<GAME>_d<draw, 5 digits>_v<version, 5 digits>_<UTC date-time>.txt`, with the same as `.csv`.
Each table set (the `.txt` and `.csv` of one publication) is logged in the search log (`WEEKLY_TABLE`). A set is logged,
and counts as published, only when both of its archive files are durable and verified. An interrupted publication is
finished with exactly the same bytes and identity, or is marked incomplete; it is never logged as complete, never
overwritten and never abandoned silently (v0.8; EX_223 B02).
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
  rule, the opportunity rule and the cut-off of 6.8, the scoring policy whose lines are read, the numerical kernel's
  version, and the error budget. It is created before the first contributing target is drawn, and before that target's
  forecast is frozen. The score starts at that first future target. **No draw already made, and no forecast whose outcome
  was known when this statistic was chosen, can ever enter it.** From the start, every target is one opportunity, taken
  in draw order exactly once: counted, skipped (V = 0) or missed (6.8), the last two with factor 1; none is dropped,
  repeated or recomputed (amended in v0.8).
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
  log-factors and the running score. A factor line without its earlier eligibility line refuses. (v0.8: the eligibility
  line also holds the weight of every number and the digest of the draw's sealed factor table; a missed target has one
  line of its own, written after its cut-off; see below.)
- **Who writes them, and when** (EX_211 F01; EX_223 C01). The orchestrator starts the OV-1 recorder as soon as a freeze
  line closes, before the session ends and so before the outcome exists; it is attempted at once and is never held back
  until the cut-off. The recorder needs only the frozen tickets. It is the one writer of this ledger. It is not part of
  table publication: a failed league table never prevents it, and its own failure never undoes or delays a freeze.
- **The cut-off (v0.8; owner OD-3; EX_223 B01).** For target T the cut-off C(T) is 01:30 UTC on T's derived draw date.
  That is 12:00 noon in Adelaide during daylight saving and 11:00 in Adelaide standard time: never later than noon in
  Adelaide, and with no time-zone data to depend on. It is at least seven hours before a result can exist, on the
  owner's statement, recorded in the registration, that both games close at 7.30pm AEST. An eligibility line counts
  only if it is durable before C(T) and T's result is not then in the master; otherwise the recorder refuses to write
  one. **The cut-off moves no forecast deadline:** a ticket counts only if its own freeze time is before the design's
  midnight deadline (design 6.4), exactly as before, and nothing frozen later is promoted. If the operator's schedule
  changes so that a result could exist before C(T), the owner stops the stream by a recorded stop before the first
  affected draw; and a counted draw whose date in the master is not its derived date stops the stream.
- **Every target is one opportunity, classified by a rule fixed at registration (v0.8; owner OD-2; EX_223 B01).** From
  the first eligible target on, the targets are taken in draw order, each exactly once. A *pre-cut-off freeze line* for
  T is the freeze line of a next-draw set for T whose own freeze time is before C(T).
  - *Counted:* T has a pre-cut-off freeze line and a valid eligibility line. Its factor is that of 6.5, or 1 if the
    line records V = 0.
  - *Missed (`MISSED_NO_FREEZE`):* T has no pre-cut-off freeze line. Its factor is 1. The program decides this, never
    a person. After C(T) it records the fact from the forecast ledger, whose whole chain it has first verified, and
    labels the line as recorded after the cut-off from the records, which is a weaker witness than a pre-outcome line.
  - *Stop:* T has a pre-cut-off freeze line and no valid eligibility line at C(T). **"OV-1 eligibility NOT VERIFIED -
    PRIMARY STREAM STOP"** (F01), in the session record and in every report for that game from that target. It is
    never treated as missed.
  Which of the three applies is fixed by what existed before C(T), and so before T's result existed. Recording it
  later reads that fact and cannot choose it: a freeze line appended later carries its own later time and can never
  become a pre-cut-off line. If the ledger's chain does not verify, or its times do not run forward, absence is not
  established and nothing is recorded: an absence of evidence is never evidence of absence. The genuine forecasts,
  their scores and the failure evidence are always kept, and forecasting and scoring continue as normal.
- **Failures (v0.8; EX_223 C02).** A failure is never a skip.
  - *Blocked:* an input is not yet there or cannot be verified (the result not yet accepted; a score line not yet
    written; a ledger that does not verify). Nothing is written for that target or any later one until it resolves. No
    target is passed over.
  - *Stop:* the F01 case above; a recorded owner stop; or a contradiction about a counted target between what was
    sealed and what came later: the factor table rebuilt at scoring is not the one whose digest the eligibility line
    sealed; X is not a value the frozen weights can produce, or its two derivations disagree; an eligible variant's
    score line does not carry the frozen record's digest and the registered scoring policy; the draw's date is not its
    derived date. After a stop no factor line is appended for that target or any later one.
  - *Sealed before the outcome:* the factor table of a counted draw (every possible X, for each lambda) and its
    certificate are computed when the eligibility line is written, and the table's digest is in that line. The factor
    line only looks up the observed X. If the table cannot be computed and certified then, no eligibility line is
    written, which is the F01 case and is decided before the outcome. The scoring policy whose lines are read is fixed
    in the registration; a corrective score never enters OV-1.
  - *Why a stop can never manufacture a crossing:* a stop ends the stream at its last value, and no later factor is
    ever applied. Every crossing the software can declare is therefore a crossing of the whole registered process at
    that same draw. Stopping can only remove crossings. What would break the guarantee is passing over a draw and
    carrying on; outside the missed rule above, which is fixed before the outcome, the software never does that.
- **After a stop** (EX_213 RC-1; owner OD-4, v0.8). The stream stays stopped. MHUP-B provides no second registration, and
  no reconstruction rule is registered, so there is no recovery after an outcome. A retry of the recorder before C(T)
  is ordinary operation, not a recovery. For any future design, RC-1 stands: a new registration has a distinct test
  identity and must receive an explicit, reviewed error-budget allocation across all confirmatory registrations; there
  is no automatic reset and no reuse of the earlier per-game 2.5% allowance; and building a line after the outcome is
  never assumed to be equivalent to the pre-outcome record.
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

**7.1A Two kinds of development run (v0.8; owner OD-1, decision log entry 69; EX_223 B04).** Both use the one driver, the
same N-1 isolation and the same record contracts, and both give development evidence only.
- *Routine fill:* when a variant is released, or a gap exists, only the missing pairs are run: each released variant's
  eligible targets for which no canonical score exists. Records that exist are reused. Its report attempt is admitted
  to the league's sources if nothing conflicts (section 4 rule 2A), and a new league table is published.
- *Exploratory rerun:* on the owner's request, any currently runnable variants, or the whole released cohort, over any
  eligible targets, whether or not they were scored before: any target up to `holdout_last` (after the seal), and any
  later accepted target whose weekly freeze line exists. It is a new, separate attempt. It is never admitted to the
  league's sources and never changes a canonical figure; it is shown in labelled comparisons by named attempt.
- Neither kind alters or reopens a sealed Mode H record, a weekly record, a frozen forecast or an earlier attempt.
  Neither can make a known draw prospective or holdout evidence. Repeated runs of a draw are never added together or
  treated as independent observations. A retired revision is run only if an installed, released revision makes it
  runnable; archived code is never executed.
- The kind, the cohort and the targets are fixed in the attempt's plan. For plans of this new kind this is a recorded
  exception to the full-cohort choice of 31 October 2026 (ER-6 declined); plans of the first kind are unchanged. Once
  this is ratified, choosing another eligible window needs no new design decision; each run on the owner's PC still
  needs his go.

**7.2 The window contract** (an R3 17.3.6 amendment, not a bound edit). For development batches and reports of a game:
1. Until that game's `MODE_H_SEALED` record exists, the Phase 1 cap stands (1576, 1693).
2. After it exists, the cap is `holdout_last` (1586, 1703) for every variant.
2A. **Beyond the holdout (amended in v0.8; EX_223 B03, B04):** a routine fill may also cover an accepted target whose
   weekly freeze line was written before the variant's release instant (the `released_utc` of its release record),
   provided no weekly ticket or record exists for that pair. A target still open when the variant joined the session
   roster is the weekly session's, never a batch's. An exploratory rerun (7.1A) may cover any accepted target whose
   weekly freeze line exists. Either is read-only towards the weekly records: it opens no freeze line and writes
   nothing to the weekly ledgers. A routine fill has its own source identity in `LEAGUE_SOURCES_<GAME>.json`, and
   section 4's one-score rule stops any overlap with a weekly record.
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
untouched, and the reconstruction file marks where a variant's history is back-filled (5.3). An exploratory rerun (7.1A)
adds no row and changes no figure in this ranking (v0.8).

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
the Architecture's next edition; the runner's rulebook; the design itself, by a short amendment naming this supplement;
and (v0.8) a note beside the record of ER-6 that plans of the new kind may name their variants (7.1A).

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
- **Stopping the formal test at the first missed week** (v0.8): the strictest reading, and simple; but over years one
  missed week is close to certain, so it would almost surely end the test early for no scientific reason. Replaced by
  the opportunity rule of 6.8, which the reviewer accepts only because the missed status is fixed before the outcome.
- **Noon by Adelaide's own clock** (v0.8): needs time-zone data and a rule for the daylight-saving change. The fixed
  instant of 6.8 is never later than Adelaide's noon and has neither.
- **Full-cohort batches only** (the choice of 31 October 2026) (v0.8): no restricted plans to review; but every new
  method would repeat every earlier run, rule 2A could not work at all, and the owner's wish to rerun any method over
  any eligible draws would be unmet. Kept unchanged for plans of the first kind.

## 13. For the reviewer and the owner

**The reviewer's recommendation (EX_213):** ratify, with RC-1 (now in 6.8). **For v0.8:** EX_223 asked for the amendments
of section 1A; the owner gave his directions on 17 November 2026 (decision log entries 69 and 70).

**The owner's decisions** (his position is in decision log entry 59). O-1 to O-4 were approved with v0.7 (RAT-33) and
are unchanged:
- O-1. The table and files of sections 3 and 5.
- O-2. OV-1 as the one confirmatory forward test for each game, by the evidence score of 6.5 with a bar of 40, everything
  else secondary.
- O-3. The window contract and re-forecasting rules of section 7.
- O-4. The objective of scoring Powerball targets 1145-1285; the run itself needs a separate go once its command is reviewed.

**New in v0.8, for the owner's ratification:**
- O-5. The opportunity rule, the cut-off and the failure rules of 6.5 and 6.8 (his directions OD-2, OD-3 and OD-4).
- O-6. The two kinds of development run and the canonical rule (7.1A, 7.2 rule 2A, section 4 rule 2A; his direction OD-1).
- O-7. The writer, source-file and publication wording (section 4 rules 4 and 5; 5.1).

## 14. Not tested; what the code round must show

Nothing here has run against project data. The simulation uses invented draws and one tilt model. The code round must
show: the exact distribution and variance against brute force for both games; the import-isolation test and fault injection
at every interface between the live path and the reporting layers, with the accepted ledger and freeze bytes unchanged;
each refusal of sections 4 and 7; the source adapters tested against the actual schemas of the existing score records;
and a session interrupted at every step with the table layer made to fail.

For v0.8 the code round must also show: every target classified as counted, skipped, missed or a stop from the records
alone, with the cut-off tested at its exact second and across both daylight-saving changes; the missed status refused
when the forecast ledger's chain is broken or its times run backwards; each stop cause planted once, with no factor
line after it; the sealed factor table equal to the one rebuilt at scoring; both kinds of development run through the
one driver, with no key counted twice and no exploratory attempt in a canonical total; and an interrupted publication
finished with the same bytes or marked incomplete, never logged as complete.

End of v0.8.
