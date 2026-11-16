# MHUP-B design supplement - DRAFT v0.2

**Status: a draft by the Claude web chat (17 November 2026, on Fable). Not ratified. It authorises no code, run, rescore or
install.** It replaces draft v0.1 (kept in the same folder as history). It applies the owner's decision of 17 November 2026
(decision log entry 51: a full MHUP-B, and one overall measure beside all the others) and the reviewer's review of v0.1
(EX_207: conditional pass on direction, with corrections) to the ratified design
(`doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`, "the design" below).

## 0. In plain English

- **One package, built in layers.** MHUP-B carries the weekly session, the league table and its files, one overall measure,
  a new method's back-history, the report window extended past the holdouts, a consolidated report, and the scoring of the
  early Powerball draws. Each layer has its own tests, and the weekly forecasting and scoring never depend on the reporting
  layers: a fault in a table can never stop a forecast being frozen.
- **The league table** lists every released method and variant (those with no score yet are shown as such), with an
  all-draws column, a forward-only column and the split by kind of evidence. It is a description: no "significant" marks.
- **The one overall measure** (section 6) asks one question of every forward draw of both games together: *were the numbers
  the methods favoured drawn more, or less, than the numbers they disfavoured?* It has an exact luck yardstick for every
  draw, it stays valid when methods learn from earlier draws, and it is read formally only five times (after 52, 104, 208,
  416 and 832 forward draws), so that looking every week cannot manufacture a result. Everything else is still reported and
  is labelled secondary.
- **What it can show, honestly:** in a simulation, a tilt of 20% towards the most favoured numbers is detected about one
  time in three after one year of both games and about 95 times in 100 after four years; a 10% tilt is detected about 4
  times in 10 after four years. The claim in v0.1 that one measure would be "more than twice as fast" is withdrawn
  (EX_207 R-3).

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
| Owner, entry 51 | Full scope; one overall measure beside all others | 2, 6 |

## 2. The package in layers (EX_207 R-4)

| Layer | Contents | Depends on | Acceptance gate (all on invented data unless the owner gives a separate go) |
|---|---|---|---|
| L1 | The `CATCH_UP` mode and tier, `FINAL_NEXT_DRAW` opened for ticketed session requests (design 6.4; E2R-1 amendment) | MHUP-A | The gate matrix of Appendix E passes; every refused combination refuses |
| L2 | The forecasting half, the freeze line, the forecast and witness ledgers (design 6.3, 6.5) | L1 | Appendix F's states and Appendix G's lifecycle, with interruption at every step |
| L3 | The scoring half and the score ledger (design 6.6) | L2 | Nothing scored twice; a second routine score for the same scientific identity refuses |
| L4 | The league table, its files, the history file (sections 3 to 5) | reads L3's ledger and the other sources | Section 4's contract: duplicate, overlap and missing-source cases each refuse or degrade as written |
| L5 | The overall measure (section 6) | reads L2 and L3 | The exact variance against brute force; the simulation of 6.6 repeated in the test suite at small size |
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
| All scored draws | Draws, Hits, Chance, +/- % | Every accepted routine score for that variant, once each, whatever its kind. **No P value.** |
| Forward only | Draws, Hits, Chance | Effective class `PROSPECTIVE`. Beside it: how many of those draws are witness-verified (design 6.5). The two are never merged |
| Last 10 | Hits | The ten latest scored draws |

A second table with the same rows gives the split by kind in separate columns: development, Mode H, catch-up,
`LATE_PRE_DRAW`, forward. It also gives the WORST ticket, the Powerball barrel for Powerball, the prize divisions, and for
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

1. **Sources, read-only, each named by identity in the table's header:** (a) the weekly score ledger; (b) each game's sealed
   Mode H score ledger, used only if its SHA-256 equals the one its `SCORE_COMPLETE` record holds; (c) the development score
   records of the report attempts listed in a small tracked file, `LEAGUE_SOURCES_<GAME>.json`, each with its attempt
   identity and window.
2. **One score per key.** The key is (game, method, revision, variant, target, barrel, TOP or WORST, scoring policy). If two
   sources hold the same key, or two listed development attempts overlap for a variant, the table **refuses** and names the
   key. It never picks one.
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

## 6. The one overall measure, OV-1 (owner decision 51; EX_207 R-3, O-3)

**6.1 Definition.** For one draw of one game, take every variant that has a frozen forecast for it of class `PROSPECTIVE`.
For each number j of the main barrel let

    w_j = (how many of those variants have j in their TOP seven) - (how many have j in their WORST seven)

    X = the sum of w_j over the seven numbers drawn

Given the frozen tickets, under a fair draw X has mean exactly 0 and variance exactly

    V = K (N - K) / (N - 1) * (1/N) * sum over j of (w_j - mean of w)^2      (K = 7; N = 35 or 47)

The draw's score is Z = X / sqrt(V). A draw with V = 0 (no variant, or weights all equal) is skipped and counted as
skipped. **OV-1 after n counted draws is S_n = (Z_1 + ... + Z_n) / sqrt(n)**, over the forward draws of both games together
in order of draw date (Oz Lotto before Powerball on the same date).

**6.2 Why this form.**
- *Shared numbers are handled exactly.* If thirty variants favour the same number, its weight is 30 and the variance
  formula accounts for it. Nothing is estimated from the data.
- *It stays valid when methods adapt.* The tickets for a draw are frozen before it, so given the past each Z has mean 0
  and variance 1 whatever the methods learned from earlier draws; the sum is a martingale and S_n is close to a standard
  normal value. This is the property the 80-track maximum lacks (its N1 figure is a reference only, R3 17.5A).
- *The roster may change.* New, revised and retired variants enter or leave through the freeze line of each draw (design
  6.3), which is fixed before the draw. No cohort has to be frozen for years.
- *X needs no outcome beyond the scores already kept*: it is the sum over variants of TOP matches minus WORST matches. V
  needs only the frozen tickets.

**6.3 Scope: one test for the whole programme.** Both games, main barrels, forward records only. One hypothesis: the
methods' favoured numbers are drawn at the same rate as their disfavoured numbers. **Two-sided**: a strong result in
either direction means the draws are predictable from the methods' rankings.

**6.4 Which records count.** Class `PROSPECTIVE` only (design 6.4, Appendix I). Never catch-up, development, Mode H or
`LATE_PRE_DRAW`. The report prints beside S_n the same quantity over the witness-verified records alone (design 6.5); the
formal reading uses the `PROSPECTIVE` class as the design defines it, and says how many of its draws are witness-verified.

**6.5 Readings and the error budget.** OV-1 is shown every week with its luck band, as a description. It is **read
formally five times only**: on the first 52, 104, 208, 416 and 832 counted forward draws (about six months, then one, two,
four and eight years with both games). At each reading the result counts if |S_n| is at least **2.576** (a 1% two-sided
event). Five readings at 1% keep the whole plan at or under 5% however often anyone looks in between. After the fifth
reading the plan ends and a new one is declared before further draws.
- **OV-1 is the only confirmatory test of the forward phase.** The 80-track families, every other measure, the per-game
  and Powerball-barrel versions of OV-1 and the league table are reported in full and labelled **secondary, exploratory**
  (the reviewer's preferred simple option, EX_207). A striking secondary result becomes a hypothesis for a new declared
  test on later draws.
- The alternative, if the owner wants the 80-track family confirmatory too: 2.5% each, declared now. Not proposed.

**6.6 What the check shows** (`overall_measure_check.py` and its output, in this folder; simulated draws only).
- *Under fair draws* the share of runs passing a 5% one-sided line was 4.4% to 5.3%, and passing the 0.5% line 0.2% to 0.5%,
  for fixed overlapping tickets and for methods that re-rank from the simulated past, at 52 and 208 draws. So the yardstick
  is right or slightly cautious.
- *Under a tilt* in which a number's chance rises or falls in proportion to its weight, by up to 10% or 20% for the most
  favoured number: passing the upper line S >= 2.576 happened in about 8% of runs at 104 draws and 34% to 40% at 416 for a
  10% tilt; and 35% to 37% at 104 and 93% to 96% at 416 for a 20% tilt (104 draws is one year of both games; 416 is four).
  These figures depend on that tilt model. They are a guide, not a
  promise, and say nothing about a single good method among many poor ones: that case is what the secondary 80-track view
  is kept for.

**6.7 The same quantity elsewhere, as description only.** For catch-up draws, and for development draws from the frozen
development forecasts, the table may show the same Z values, labelled retrospective. For the sealed Mode H draws it is
computed only if the reviewer and owner agree (question R-6): it would read the sealed forecasts and scores without changing
them, and it would be labelled post hoc.

**6.8 What it needs in the records.** One line per counted draw in a small create-only ledger: game, draw, the freeze
line's identity, the number of variants, X, V, Z, and the digest of the weights. A new measure entry and calibration label
in the registry and R3 (provisional name OV-1; label "exact conditional variance, martingale normal approximation"), and
one registered primary-test record holding 6.1 to 6.5, created before the first forward draw is scored.

## 7. Back-history and the window contract (D-5, D-9; EX_207 R-4, R-5 E)

**7.1 What a newly released variant gets.** (a) Draws after the holdout and before its release: already in the design,
through the weekly session, as development evidence (6.4). (b) Draws up to the end of the holdout: one development
walk-forward batch by the existing driver, from the game's first target to `holdout_last`.

**7.2 The window contract** (an R3 17.3.6 amendment, not a bound edit). For development batches and reports of a game:
1. Until that game's `MODE_H_SEALED` record exists, the Phase 1 cap stands (1576, 1693).
2. After it exists, the cap is `holdout_last` (1586, 1703). Draws after that belong to the weekly session only.
3. A batch may include a holdout target for a variant **only if that variant has no Mode H record for that target**. The 40
   cohort variants therefore can never be forecast again on those draws.
4. Every such forecast is development evidence. It can never be catch-up, prospective or Mode H evidence.
5. A back-history batch writes only under the development roots. It opens no freeze line, no weekly ledger and no sealed
   Mode H path for writing, and the Mode H study is never rescored.
6. Method-facing N-1 isolation, forecast identities and append-only records are unchanged.

**7.3 "A new method re-ranks all draws."** After 7.1 the new variant has scores for every draw, so the next league table
ranks it among the others over all scored draws, as a new numbered file. Earlier tables are untouched, and the
reconstruction file marks where its history is back-filled (5.3).

## 8. The consolidated report, the retired index and the early Powerball draws (roadmap 21b; D-6)

- **The consolidated report** is the design's full report (6.6) with these parts, each from named sources and none pooled
  into a P value: the league table; OV-1 (its formal reading if one is due, otherwise its running value); the forward and
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

R3 (17.3.6 the window contract; 17.5A and the registries for OV-1 and its label; the league table and reconstruction as
descriptive outputs); E2R-1 (9.1 and E2R-R41 for `CATCH_UP`, E2R-R44 for `FINAL_NEXT_DRAW`), as the design already lists;
the Architecture's next edition; the runner's rulebook; the design itself, by a short amendment naming this supplement.

## 12. Alternatives considered

- **OV-1 per game at 2.5% each:** two questions instead of one and half the draws for each. Kept as a secondary view.
- **Raw sum of X divided by the root of summed V** (instead of equal weight per draw): gives draws with more variants more
  say. Defensible; rejected so that one period with many variants cannot dominate, and for the plainer description.
- **One-sided:** slightly more power in the favoured direction, but blind to systematic anti-prediction, which is as much a
  departure from randomness.
- **An always-valid boundary** (a mixture or e-value test readable every week): more efficient than five fixed readings,
  but much harder to explain and to verify. Put to the reviewer (R-4).
- **An N1 replay of the aggregate:** only a reference for adaptive methods, by R3's own labels. The exact conditional
  variance does not have that weakness.
- **Total TOP minus WORST matches without the variance per draw:** its luck band would have to be estimated or simulated.

## 13. For the reviewer and the owner

**Questions for the reviewer**
- R-1. Is OV-1 as defined in 6.1 to 6.4 a valid primary test, and is the martingale argument of 6.2 sound for adaptive
  methods and a changing roster?
- R-2. One programme-wide two-sided test (6.3): agree, or per game?
- R-3. Five fixed readings at 1% each (6.5): acceptable as the repeated-look policy?
- R-4. Would you rather have an always-valid boundary, at the cost of complexity?
- R-5. The formal reading on the `PROSPECTIVE` class with the witness-verified figure beside it (6.4): right, or should the
  reading use witness-verified records only?
- R-6. May OV-1 be shown descriptively on the sealed Mode H draws (6.7), read-only and labelled post hoc?
- R-7. Sections 2, 4 and 7: do the layers, the read contract and the window contract meet the conditions of EX_207?

**Decisions for the owner (after the reviewer's view)**
- O-1. The table and files of sections 3 and 5.
- O-2. OV-1 as the one confirmatory forward test, read five times, with everything else secondary (section 6).
- O-3. The window contract and back-history rules of section 7.
- O-4. Later, a go for the Powerball 1145-1285 report run.

## 14. Not tested; what the code round must show

Nothing here has run against project data. The simulation uses invented draws and one tilt model. The code round must
show: the exact variance against brute force for both games; the import-isolation test; each refusal of sections 4 and 7;
a session interrupted at every step with the table layer made to fail; and identical ledgers whatever the table layer does.

End of draft v0.2.
