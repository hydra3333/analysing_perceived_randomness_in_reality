# Reporting and rankings - consolidated final design and specification Amendment A1 (v0.5, ratified)

Date: 28 November 2026
Project: hydra3333/analysing_perceived_randomness_in_reality
Prepared by: ChatGPT independent reviewer, at the owner's request, consolidating Claude's
two candidates and incorporating the focused independent review below (v0.3). **v0.4 by the
Claude web chat, at the owner's request (decision log entry 417):** v0.3 with the owner's
decision of 28 November 2026 on the first migration, LAST, ALL, workbooks and the reports
folder worked in. Only the passages listed under "Changes in v0.4" differ from v0.3.
**v0.5, likewise (entry 419):** the reviewer's and the owner's clarifications of v0.4, listed
under "Changes in v0.5". v0.3 and v0.4 are preserved unchanged in exchange/.
Status: RATIFIED by the owner, RAT-74 (28 November 2026; decision log entry 421), after the
reviewer's PASS. Not implemented or installed. Ratification authorises no code, install or run.

Source candidates, preserved unchanged in exchange/:
- exchange/ChatGPT_Reporting_Design_And_Specification_Amendment_A1_CANDIDATE_v0_3_20261128.md (3372e4b), the consolidation.
- exchange/Claude_Reporting_Part_And_Rankings_Proposal_v0_2_20261128.md (add50b6).
- exchange/Claude_Specification_Amendment_A1_Reporting_CANDIDATE_v0_1_20261128.md (e7a600d).
Review baseline: e7a600d1bb5bf335de645031eb622d65fa27101d.
Discussion v0.1-v0.4 and decision log entries 412-415 establish substantive consensus.
The owner's seven choices, including the draw-number correction, stand.

## How to use this document

Part A retains the full design. Part B is the binding amendment to the existing
specification and simple scheme, with the R3 measure dispositions. Upon ratification,
the two parts are installed together as one document in doc/, not two separate
documents. Part B governs specification wording; Part A supplies the detailed design.
Any conflict must be resolved before implementation rather than by choosing whichever
wording is convenient. The earlier specifications remain unchanged except as explicitly
amended, and provisions already superseded by the simple scheme stay superseded.
No new administrative machinery.

## Independent review and changes in this consolidation

The reviewer accepts the agreed architecture, catalogue, three phases, sixteen
Powerball / eleven Oz Lotto default text sorts, all core columns, signed-tail
convention and mathematical MR17 definitions, conditional yardsticks, local INI,
draw-number-only scientific timeline and the open MEASURE plan. For each track,
MR4 has 2D distinct events (D exact + D cumulative - one duplicate + one band):
18 Powerball and 14 Oz Lotto. Add MR1, MR7.MAIN, and for Powerball MR7.PB and
both MR17 forms: 23 and 16 respectively. These are one-sided tests per applicable
track before counting directions, not numbers of independent tests.

The following are focused review corrections/clarifications, not previously
ratified new choices. Claude is asked to concur or propose the simplest correction:

1. A2/A10, B1: read-only currency checks must cover material accepted results,
   status and series inputs, not just code fingerprints. Refusal/interruption
   must not leave stale files represented as current. Clarify mixed-game and
   no-score outcomes and game-specific DRAW scope. No fresh scientific scoring
   from the reporting-only path.
2. A10/A12, B1/B3: existing research_job.settle_infrastructure removes the
   entire reports folder in both games on an engine rebuild. Preserve prior
   requested endpoints/formats before cleanup and through interruption.
   (The first migration: see "Changes in v0.4".) Existing requested
   workbooks are maintained on invalidation even when ALL does not request
   every additional workbook. No new all-history workbook default.
3. A11/A12: game_state.GameRecords documents cutoff as always None in the simple
   scheme, and research_job.open_game does not populate it. Do not revive the
   superseded cutoff machinery or store a permanently empty field. Persist the
   actual prevailing OV-1 blocked reason, with its series/input identity and
   explicit no-block state. Check same-input print-outs against the living code.
4. A3-A6: retirement at the endpoint, not only before it, flags selection
   unverified. Distinguish variance from spread, exact division-one aliases,
   zero observed wins from neutral signed Z, and true ties from overlapping
   numerical bounds. MR1 finite zero Z is not a zero probability bound; handle
   unbounded intervals and non-adjacent overlaps without false ties. State
   the secondary sort-key changes explicitly.
5. A7-A9/B1: distinguish descriptive rankings from tails; preserve exact,
   bracketed, approximate and later N1 references without overpromising
   exactness. Keep the ranking CSV rectangular while retaining provenance;
   XLSX semantic reproducibility does not mean science has changed when
   container metadata differs. Preserve the full data and core reading view.
6. B2/B3/B5: reconcile surviving per-draw publication wording and commands
   with the new LAST/ALL rule. Do not reintroduce older administrative
   mechanisms. R3 definitions otherwise stand, with every measure's disposition.
7. A12/A15: if scientific equivalence fails, distinguish a dependency effect
   from relocation, with any old-code rebuild subject to separate owner GO.
   Add proportionate tests for these concrete boundaries.

No additional architecture, deployment utility, forecasting method or new
administrative gate is proposed. The reviewer has read both candidates,
R3 section 17 and the relevant existing specification, simple scheme,
research_job.py, game_state.py, reports.py and OV-1 code. No project code was
executed. The MR1 numerical prototype and performance are not independently
tested. The code plan must resolve the small implementation details and the
MEASURE item remains open. The owner's dependency assumption from entry 414 stands.

## Changes in v0.4

Claude concurs with review corrections 1 and 3 to 7 above, and with 2 as changed here (decision log entry 416).
The owner's decision (28 November 2026, 19:51; entry 417), in his words: "Our intended end state remains
comprehensive reporting for every scored draw, subject to the actual performance measurements."

1. **The first migration makes LAST only.** The old league files are removed: they were made for every scored draw
   by the old rule and are not requests (A10, A15, B1 9.10).
2. **LAST reports each newly scored draw:** every draw scored since the game's reports were last brought up to
   date, so a job that catches up several draws reports each of them (A10, B1 9.9, B2, B3).
3. **The intended end state** is text and CSV reports for every scored draw, kept current: the owner measures in
   DEV (A14), then runs ALL once in each tree. ALL stays as an explicit recalculation command (A10, A14, A16).
4. **Workbooks** are kept for the latest scored draw and for endpoints specifically asked for (A8, B1 9.10).
5. **The engine no longer deletes the reports folder;** the reporting part alone manages it and its inventory
   (A10, A12, B1 9.10, B3).
6. Existing valid reports are not recalculated; stale ones are removed and made again (unchanged from v0.3).

## Changes in v0.5

The reviewer substantially concurs with v0.4, and the owner and the reviewer agree its three readings (the earlier
latest workbook removed unless asked for; "newly scored" reckoned from the last reported draw in the inventory; a
deleted reports folder starts again with LAST). Their clarifications (28 November 2026, 20:02; entry 419):

1. **What is stale is defined, apart from what may be regenerated for simplicity** (A10, B1 9.10). A report
   through draw T is stale only when something it shows would now come out differently. Regenerating more than
   that is an implementation choice, permitted if it is simplest and its measured cost is acceptable; it is not a
   scientific requirement.
2. **Everything in a report is read relative to its own draw-number endpoint** (A3, A10). A method newly installed
   with walk-forward scores at earlier draws changes the earlier rankings, and that history is wanted. A
   retirement from draw R changes nothing in a report through a draw before R.
3. **Coverage** (A10): failed outputs are retried; once ALL has established every scored draw, that complete
   coverage is maintained, earlier scored draws that become newly available included.
4. **Workbooks asked for through `ALL --workbooks` are requests** and are kept current (A8). **The measurement in
   DEV must not leave an unwanted permanent collection** (A14).

# Part A - Final reporting design

## A0. In short

- A **reporting part**, separate from the engine, makes every print-out. It reads what the engine has stored and
  computes no forecast and no score. A change to it makes reports again and nothing else.
- Each method's **TOP ticket and WORST ticket is a track of its own.** All tracks of a game are ranked together.
- The ranking is by **many criteria**, each a named sort of the same table, each with a rank column. Individual sort files are
  switched on and off in a small settings file; all implemented applicable measures are computed.
- Where applicable a criterion has a **fair-draw reference and signed tail-equivalent Z**, exact, bracketed or
  explicitly approximate as specified, with both ends of the list shown.
- **Every report states the yardstick** (how far the first of N gets by luck), begins with a plain-English
  introduction and ends with a legend that explains every column it prints, with worked examples.
- Text, CSV and an Excel workbook. Reports for the latest draw by default, any draw or all draws on request.

## A1. Rules that govern all of it

1. **The game's draw number is the only scientific time axis** (MRD-12; R3 17.3.1). Every order, window, gap,
   streak, endpoint, grouping, chart axis and invalidation is by draw number. Clock times record only when a file
   was made. The two games are never pooled or joined.
2. **Everything reported is exploratory and descriptive.** "A descriptive order. It selects nothing." No report
   uses the words evidence, finding or discovery of its own contents.
3. **The science is untouched:** N-1 isolation, the forecasts, the scoring, TOP and WORST from one ranking, both
   OV-1 series (main barrel only, as ratified), the sealed Mode H records, the updater.
4. **No report's scientific figures are ever an input** to a method, a score or a later report. The output
   inventory and input identities are bookkeeping for report maintenance only.
5. **Nothing of R3 section 17 is dropped silently.** Every measure has a disposition in Part B.

## A2. The reporting part

- **Where:** `src/reporting/`, beside `src/updater/`. Like the updater it is left out of the engine's fingerprint
  and has a fingerprint of its own, kept with the reports it made.
- **What moves into it:** all printing. The ranking reports replace the league table. The next-draw reports and
  the two OV-1 print-outs move as they are.
- **What it reads:** the stored lists (forecasts, scores, both OV-1 series), the results on file, each method's
  declaration and small files, the tree's settings. It reads through the engine's existing reading and checking
  code and never through a path that changes anything.
- **What it refuses, saying what to do** ("run Run_Research.bat first"): the engine in the tree is not the one the
  stored results were made with; a method's stored lists were not made by the method now installed; a list fails
  its own checks; the accepted results or method status differs materially from that underlying the stored
  science; or the stored OV-1 series and required metadata are absent or stale. It then makes nothing for that
  game. A legitimate empty series differs from a missing series. Use read-only checks of the material source
  identities and existing record consistency, not a fresh scoring run. Foreign lists of uninstalled methods
  remain ignored, as now; a stale or corrupt installed method's list is not silently ignored.
- **What it never does:** start a research job, a rebuild, the updater or a scoring; write outside
  `results/research/<GAME>/reports/`; change a fingerprint or a scientific record.
- **The lock:** it works under the tree's lock, taken by itself or already held by the job that started it.
- **Commands.** Every research job ends by making the reports (LAST). A new launcher in every tree makes reports
  alone: `Run_Reports.bat [LAST | DRAW <n> | ALL [--workbooks]] [--game POWERBALL|OZLOTTO|BOTH]`.
- **Exit codes of `Run_Reports.bat`:** 0, every report asked for is made and current; 1, made but incomplete (the
  last lines name each output not made or not current, and why); 2, refused before making any reports. A refusal for one game while another succeeds is not an overall success;
  the code plan must specify the mixed-game exit, without claiming no changes if another game was written.
- **Inside a job:** if the reports come out incomplete the forecasts and scores stand, the job ends with its
  existing "not clean" code, and its last lines say the research is done and which reports are not.

## A3. Units, tracks and what each track is measured over

- **A track** is one readout of one method: TOP or WORST. Forty methods give eighty tracks a game. Phase 1's
  measures are all of a track. (Phase 2 adds measures of a whole ranking, one row a method, and of the TOP and
  WORST pair; those get tables of their own and are never doubled into two track rows.)
- **Each track is measured over its own scored draws** up to the requested draw (R3's OWN_SET). The report shows
  n, the first and last scored draw numbers, and the expected targets that have no score. A common scored set or a
  starting draw is deferred, not discarded.
- **Raw figures and figures against luck are kept apart.** Allowing for n makes unequal histories comparable
  against luck; it does not make different stretches of draws the same stretch.
- **The grid tag.** A track's expected targets follow from its declaration and the draw numbers alone: every draw
  from the first with at least its declared minimum of earlier draws, to the requested draw. The track is tagged
  **"selection unverified"**, with the reason and the count affected, when a forecast is NO_FORECAST for any reason
  but too little history; when an expected target has no score; when the track is retired from the requested
  draw or earlier; or when the records cannot show it. Otherwise **"grid as declared"**. The figures are shown either way. The
  legend says that the methods and their design were chosen with the history in view, so every table is
  exploratory whatever the tag.
- **Everything is read relative to the report's own endpoint.** A report through draw T shows each track as it
  stood at T: its targets, scores, counts and tags up to T, and a track only if it has a target at or before T. A
  retirement from draw R appears, and sets the grid tag, only in reports through R or a later draw.
- **Other tags:** LOW_N (fewer than 30 scored draws); RETIRED from draw n, with its reason (in reports through
  draw n or later); "bracket" and "order not resolved" (A5.3). A value that is undefined is shown as "-" and never as nought.

## A4. The measures of phase 1

Definitions follow R3 v0.5 section 17, except the explicit departures in this document (including reference
laws, signed ordering and secondary keys). MR17 is new and defined here.
D is 9 for Powerball and 7 for Oz Lotto.

| Measure | What it is | Barrels | Luck figure |
|---|---|---|---|
| MR0 | Prizes by division, best division first (the vector W_1 .. W_D) | both | a side reference only: the chance of its best division or better at least once |
| MR1 | Prize rarity: total bits of surprise of the prizes won; shown a draw | both | exact, or bracketed (A5.3) |
| MR1-T | The owner's (0.90 W_1 + 0.07 W_2 + 0.03 W_3) / n | both | none: a preference score |
| MR4.X.d | Wins of exactly division d, for every d | both | exact binomial |
| MR4.C.d | Wins of division d or better, for every d; MR4.C.D is "any prize", shown as MR4.ANY | both | exact binomial |
| MR4.B.2-3 | Wins of Division 2 or 3 (the owner's original band) | both | exact binomial |
| MR7.MAIN | Total main-barrel hits | main | exact convolution |
| MR7.PB | Times the Powerball was picked (Powerball only) | Powerball | exact binomial |
| MR17.SUM | Main hits plus Powerball hits, each hit once (Powerball only) | both | exact convolution |
| MR17.EQ | Each barrel's total on its own fair-draw scale, the two added (Powerball only) | both | exact (A5.4) |

- "Both" for Oz Lotto means the seven numbers and the supplementaries drawn, as the operator counts a division;
  methods never forecast supplementaries (MRD-03).
- **MR17.SUM:** H = M + B over the track's n scored draws. The one-draw law is the main-hit law times
  (0.95 + 0.05 z); its n-th power is the exact law of the total. The legend says the main barrel supplies about 95
  per cent of its fair-draw variance, so its hit statistic mostly follows MR7.MAIN.
- **MR17.EQ:** E = (M - 1.4 n) / sqrt(n x 392/425) + (B - n/20) / sqrt(n x 0.0475). Each barrel contributes equally to
  the fair-draw variance; that is not equal hits, prizes or information. The weights come from the game's rules; none
  is fitted. E itself is not Z: E, both components, both tails and Z are reported apart.
- Identical events are one test (MR4.X.1 is MR4.C.1). Document both identities as aliases of the same
  event, figures and sort. MR0's side reference is one of the MR4.C.d figures.

**The sorts.** A sort is one ordering of the table. Several sorts of one statistic are one test.

| Sort | Ordered by | Text file by default |
|---|---|---|
| MR0 | the division vector, best first; then MR1; then shared | on |
| MR1.RAW | bits a draw | on |
| MR1.Z | signed Z of the total bits | on |
| MR1-T | its value | on |
| MR4.ANY.RATE | prizes a draw above luck | off |
| MR4.ANY.Z | signed Z of prizes of any division | on |
| MR4.C.d.Z, d below D | signed Z | MR4.C.3 on; the rest off |
| MR4.X.d.Z, d above 1 | signed Z | MR4.X.3 on; the rest off |
| MR4.B.2-3.Z | signed Z | on |
| MR7.MAIN.RATE | main hits a draw above luck (the league's order until now) | on |
| MR7.MAIN.RAW | total main hits above luck (R3's descriptive sort) | on |
| MR7.MAIN.Z | signed Z | on |
| MR7.PB.RATE, MR7.PB.RAW, MR7.PB.Z | the same for the Powerball | on (Powerball) |
| MR17.SUM.RATE | whole-ticket hits a draw above luck | off |
| MR17.SUM.Z | signed Z | on (Powerball) |
| MR17.EQ.RAW | E | off |
| MR17.EQ.Z | signed Z | on (Powerball) |

That is the sixteen default text sorts of the owner's choice 7 for Powerball, and eleven for Oz Lotto. Four of them
(MR4.C.3, MR4.B.2-3, MR4.X.3, MR1-T) have zero observed wins or preference score today. The legends say so
when true. Zero wins do not imply zero signed Z for all n; secondary sort keys can differ too. Do not force a
shared rank on that basis.

## A5. The luck figure

### A5.1 Tails and Z

- For a track with n above 0: P_up is the chance, under fair draws, of a total at least the observed; P_lo, of a
  total at most the observed; both include the observed value.
- Z_plus = max(0, the normal deviate whose upper tail is P_up); Z_minus likewise from P_lo; **signed Z = Z_plus -
  Z_minus.** At most one of the two is above nought. Nought means neither tail is below a half.
- Both tails and both sigmas are in the CSV and the workbook. Tails are computed and kept so that very small ones
  survive (summed from the far end; never as one minus something); the CSV carries their logarithms as well.
- Sorting uses the unrounded values. A report never ranks by a rounded figure.
- Work in log tails where needed. A zero probability lower bound is not a zero true inclusive tail: an observed
  score in the support has positive inclusive tails. Show zero bounds or infinite sigma bounds as such, not
  finite point estimates. Do not average infinity. A finite signed Z of zero is an ordinary value.

### A5.2 Exact laws

- MR7.MAIN: the n-th power of the one-draw hypergeometric law (R3 17.4.4). MR7.PB and every MR4 event: binomial.
  MR17.SUM: as A4. These depend only on the game and n, not on the ticket, so each is computed once for
  each n and shared.
- They hold for one track on a grid fixed without regard to the outcomes scored (R3 17.3.7A). That is what the
  grid tag reports.

### A5.3 MR1: the bracket

- The total of the division weights b_d = -log2(p_d) has an exact law in principle. It is computed on a fine grid
  twice, with every weight rounded down and with every weight rounded up, and the observed total is bounded by the
  same two roundings. With L and U the two computed totals, and [l_obs, u_obs] the observed:
  P(L >= u_obs) <= P_up <= P(U >= l_obs), and P(U <= l_obs) <= P_lo <= P(L <= u_obs).
- **Display:** where both bounds give the same Z to the two decimals shown, that Z is shown. Otherwise "from - to",
  tagged "bracket".
- Obtain signed-Z bounds monotonically from the two tail intervals: lower = excess sigma at the upper
  P_up bound minus deficit sigma at the lower P_lo bound; upper uses the opposite endpoints. Keep the
  unrounded interval even when its displayed endpoints agree.
- **Order:** midpoint of two finite signed-Z bounds, including zero. For a one-sided unbounded interval use
  its finite endpoint as a labelled provisional key. If neither bound is finite, show the interval, leave
  the numerical order unresolved/unranked. Tag all tracks with unresolved overlapping brackets, including
  non-adjacent ones. An overlap or identical provisional key is not a true tie. A demonstrable true tie
  (e.g. same n and division profile and therefore the same law and observed statistic) is ranked as a tie.
  Otherwise use the provisional key, secondary key and stable identity order, with the uncertainty tag.
- The grid's fineness is fixed by benchmark in the code plan. If no practical grid makes the bounds usually agree,
  R3's simulation (N1) is used for this figure, labelled, with its uncertainty.

### A5.4 MR17.EQ: the exact tail

With k = sqrt(6272/323) (about 4.4066; irrational, and free of n): for each Powerball total b, "E at least the
observed" is "M at least m_obs + (b_obs - b) k". When b differs from b_obs that bound is never a whole number, so
the least M is settled by whole-number arithmetic; when b equals b_obs it is M at least m_obs. So

    P_up = sum over b of P(B = b) x P(M >= m_obs + ceil((b_obs - b) x k)),

from the two exact laws of A5.2, and P_lo likewise.

## A6. Ranks

- Competition ranks: 1, 1, 3. A shared rank only for a true tie on the sort's keys; inside it, lines are listed in
  identity order, TOP before WORST.
- Z sorts: signed Z, greatest first; then raw observed minus fair-expected total (for EQ, E, whose fair
  expectation is zero); then shared only for demonstrably equal keys. MR1 provisional order as A5.3.
  Rate and raw sorts: their value, greatest first. MR0: the division vector, best first; then MR1 bits per
  draw; then shared. These signed-Z and secondary keys explicitly replace R3's former excess-only sorts
  and their different secondary keys for phase 1; preserve later measures' own rules unless amended.
- A track for which a sort is undefined or does not apply is listed last, unranked. Every report says how many
  tracks are ranked and how many are shown.

## A7. The yardstick, in every report

Worked out from what is actually in scope; no figure is fixed in the code. Each line states its scope.

- **Illustrative:** "for N ideal independent one-sided tests the first is typically near +x" (the median of the
  greatest; +2.38 for 80). It is not an estimate for these tracks, which depend on each other.
- **Conditional reference for this list:** 0.05 shared over the N tracks at one end (+3.23 for 80) and over both
  ends (+3.42 for 160).
- **Conditional reference for the game:** 0.05 shared over every distinct test of every measure the reporting part
  computes for the game, **whether its report is switched on or off,** at both ends. (With phase 1's measures that
  is 23 tests a Powerball track and 16 an Oz Lotto track: about +4.2 and +4.1.)
- **The words with them:** these are reference lines for a list fixed in advance and looked at once. This is a
  look back over history, repeated at every draw, so they are not error bounds and nothing here is a finding.
- Every report explains the yardstick's scope. Descriptive sorts are not additional tests. Print the relevant
  fair expectation and, if useful, the underlying or auxiliary reference clearly named. MR0's side reference
  is not the p-value of its lexicographic profile; MR1-T has no p-value. Count actual applicable tests and
  units, not an assumed 80 tracks when the population differs.
- The dependence note: a method's TOP and WORST come from one ranking; methods and criteria overlap. A track high
  on one list alone may be luck, or a pattern only that measure sees.

## A8. The reports

### A8.1 Files, under `results/research/<GAME>/reports/`

    rankings/d<draw, 5 digits>/rank_<GAME>_d<draw>_<sort>_<short title>.txt     one for each sort switched on
    rankings/d<draw>/rank_<GAME>_d<draw>.csv                                    every track, every column
    rankings/d<draw>/rank_<GAME>_d<draw>.xlsx                                   the workbook
    next/ and ov1/                                                              as now
    README.txt, and made_times.csv (which gains a column: current, or NOT CURRENT with the reason)

For example `rank_POWERBALL_d01593_MR7_MAIN_Z_main_hits_against_luck.txt`.

### A8.2 The text report: a reading view

Every text report of a game's track table has the same **core columns**, then the columns of the criterion it is
ordered by (its figures, both tails, Z), then one rank column for every sort switched on.

| Core column | What |
|---|---|
| # | place in this list |
| line, readout | method and variant; TOP or WORST |
| scored, first, last, missing | n; first and last scored draw number; expected targets without a score |
| main hits, luck, a draw, excess a draw | the main barrel |
| PB hits, luck, a draw, excess a draw | the Powerball barrel (Powerball only) |
| prizes, luck; divisions | prizes of any division and luck's expectation; wins by division, as 7x1 8x4 9x9 |
| last ten | main-barrel hits at the latest ten scored draws, oldest first |
| before, after | forecasts made before and after the result was on file |
| OV-1 from | first draw in the prevailing OV-1 |
| tags | A3 |

### A8.3 The CSV and the workbook: everything

- **The CSV** is rectangular: one row a track, full column names, every value of every measure, both tails with
  their logarithms, both sigmas, signed Z, the MR1 bounds, a rank for **every** sort (on or off), every tag. No
  prose rows.
- **The workbook** (XlsxWriter; no Excel needed to make it), one for each game and requested draw, in phase 1:
  - **Rankings:** the same rows and columns as an Excel table, numbers as numbers, headings and identity columns
    frozen, filters on, so the owner sorts by any column himself;
  - **Legends:** every column, measure, sort, tag and rule, with worked examples; the warning never to average
    sigmas, ranks or chances;
  - **Fair reference:** the game's rules and division odds, luck's expectations, what the tails and Z mean, the
    yardsticks with their scopes.
  No formula recomputes a figure. A workbook is kept for the latest scored draw of each game and for every
  endpoint asked for by DRAW n; ALL makes workbooks for the other draws only with `--workbooks`. When a newer draw
  becomes the latest, the earlier latest draw's workbook is removed unless that endpoint was asked for. Workbooks
  made by `ALL --workbooks` are asked for, each of them, until the owner resets the collection (A10). Requested
  workbooks follow A10's currency rule unless the workbook format is switched off. State the effective scope and handle a conflict between an explicit workbook request
  and a disabled format clearly.

### A8.4 Introduction and legend of every text report

- **At the top:** what the report is in three or four plain lines; game; the draw it runs to; the tree that made
  it; that forecasts use earlier draws only and that this is a look back (how many forecasts were made before
  their result is in the columns); the yardstick; the standing words.
- **Underneath, the legend:** every column printed, one by one; the criterion's identity, short title, what it
  measures, what its Z means; **a worked example from the first applicable line, using its actual reference (exact, bracketed or labelled approximation)**
  ("by luck about 1 track in 28 would do at least this well; that is Z = +1.80"), with the "luck's spread"
  arithmetic offered only as intuition and marked approximate; what TOP and WORST are and what each end of the
  list means for each; the game's divisions and odds and how "7x1 8x4 9x9" is read; every tag; what the report
  does not say. For a descriptive/preference criterion explain its actual arithmetic instead of inventing a
  tail. If no track has an applicable value, say so.

## A9. Settings

- **`REPORT_SETTINGS.ini` at the tree's root,** the owner's own in each tree like `ENVIRONMENT.ini`: an install or
  a copy never replaces it; a backup holds it. An example with every name and the defaults is distributed as
  `REPORT_SETTINGS.example.ini`. No file: the defaults.
- **One kind of switch:** which sorts have a text file (and so a rank column in the text reports), and which
  formats are written (text, CSV, workbook). Nothing switches a computation: every measure is always computed and
  is in the CSV and workbook, and the yardsticks do not move.
- A name it does not know, or a value that is not on or off, is refused with the list of names it knows. If a
  format is off, say which other complete format is available, or that neither complete format was requested.
- A change of settings makes the affected reports again and nothing else.

## A10. Which draws; keeping reports current; failures

- **LAST** (the default; what every job does): the reports for **each newly scored draw**, that is, through every
  draw scored since the game's reports were last brought up to date, the latest included; so a job that catches up
  several draws reports each of them. Where no reports have been made yet (the first migration; a reports folder
  the owner has deleted), the latest scored draw alone. **DRAW n:** through draw n. **ALL:** through every scored
  draw, in text and CSV: an explicit recalculation of the whole collection, whether or not what exists is valid.
- **The intended end state** (the owner, 28 November 2026) is text and CSV reports for every scored draw, kept
  current, subject to the measurement of A14. The order: the migration makes LAST; the owner measures in DEV; he
  then runs ALL once in each tree; from then on every job adds each newly scored draw, existing valid reports are
  not recalculated, and stale ones are removed and made again.
- **Coverage is kept.** "Newly scored" is reckoned from the last reported draw number in the inventory. An output
  whose making failed stays pending and is retried at every run. Once ALL has established complete coverage, the
  inventory says so and every run maintains it: any scored draw without current reports is made, an earlier scored
  draw that has newly become available (through a newly installed method, say) included.
- **No report is represented as current when stale.** Each game's reports folder notes what its reports were made from: the reporting
  part's fingerprint, the engine's, the settings, the tree, the methods with their fingerprints and retirements,
  and the stored lists as they stood. A sort switched off has its files removed and not remade.
- **What makes a report stale.** A report through draw T is stale when something it shows would now come out
  differently: the reporting part or the report settings changed; the engine that made the stored results changed;
  a forecast, score or OV-1 line at or before T changed; a method with any target at or before T was added, removed
  or changed (a newly installed method's walk-forward scores at earlier draws are wanted in the earlier rankings);
  a retirement from a draw at or before T was made or changed. **It is not stale because of** a new draw after T, a
  retirement from a draw after T, or a method whose targets all lie after T.
- **What is regenerated.** Every stale report is removed and made again in the formats and sorts switched on;
  none is ever left posing as current. The reporting part **may** regenerate more than is stale, up to the game's
  whole collection, where that is the simplest correct implementation and its measured cost is acceptable (A14).
  That is an implementation choice for the code plan, not a scientific requirement to regenerate unaffected
  reports; it may never regenerate less than is stale.
- **Reports copied from PROD** are not the destination's own (another tree, perhaps other settings): the
  destination's job removes them and makes its own. Its settings file is not touched by the copy.
- **Failure.** Stale files are removed first, then made. If a making fails, that output is absent, the run names
  the game, the draw, the format and the cause, and ends "incomplete". **A workbook that Excel holds open** can be
  neither replaced nor removed: it is left as it is, listed NOT CURRENT in `made_times.csv`, named in the run's
  last lines, and put right by the next run once Excel has let go. The other reports of that draw are still made.

**The reports folder and its inventory.** The reporting part alone manages
`results/research/<GAME>/reports/`. **The engine no longer deletes that folder**
(today `research_job.settle_infrastructure` removes it, in both games, on an engine
rebuild). After a rebuild the reporting part finds its reports stale from the
changed identities, and removes and remakes them. It keeps in the reports area a
simple durable inventory: the draw endpoints it holds, the draw the reports were
last brought up to, and the workbooks asked for. This is bookkeeping, not an input
to any scientific calculation. It survives a rebuild, an interrupted job and a
one-game job. **At the first migration the old league files are removed: they were
made for every scored draw by the old rule and are not requests. The inventory
starts with LAST.** Endpoints no longer supported by the accepted draws are removed.
A valid endpoint whose regeneration failed remains pending for retry; disabling a
sort/format removes its outputs, not the knowledge of which endpoints are held. Do
not mistake missing files after a failed run for a request to stop maintaining those
endpoints. If the owner himself deletes a game's reports folder, the next run starts
again with LAST; nothing else depends on that folder.

On a read-only refusal or an interrupted job, the existing input identities must
not imply currency when the current inputs no longer match. A refusal need not
rewrite an invalid scientific tree: explicitly say existing reports cannot be
certified current and which game is affected. The code plan should specify how
currency is determined after interruption and how pending/NOT CURRENT entries
are maintained; no automatic scientific repair. The existing locked-file exception
remains. A DRAW n request is scoped to the named game(s); specify how ambiguous
BOTH or an invalid endpoint is refused/handled independently, never align the
games by date. A no-score game must not fabricate a ranking endpoint.

## A11. The moved print-outs

- The next-draw reports and both OV-1 print-outs are made at every run of the reporting part, for the same draws
  and with the same contents as now. For the same stored inputs their bytes are the same after the move as before.
  Introductions and legends are added to them afterwards as a declared change.
- **One live fact to preserve:** why the second (prevailing) OV-1 series stopped early, if it did. Persist
  that reason (including an explicit no-block state) beside the series with its input identity, so the
  reporting part can read it without recomputing OV-1. Validate it with the associated series; old/missing
  metadata cannot be silently treated as no block. The other purported live fact, `GameRecords.cutoff`,
  is documented in `research/game_state.py` as always None under the simple scheme. `open_game` does not
  set it. The old cutoff machinery is superseded, so do not persist or revive it. Same-input print-outs
  continue to omit that obsolete cutoff line, as now.

## A12. The engine's one change, installing and proof

- **The change:** `reports.py` leaves `src/research/`; the engine's fingerprint leaves `src/reporting/` out; the
  job stores the live OV-1 blocked reason and its identity (A11), no longer deletes the reports folder
  (A10), and ends by starting the reporting part. Nothing that computes a
  forecast, a score or an OV-1 line is edited. Under the present rules each tree then makes everything again, once.
- **Installing:** the reporting part, `Run_Reports.bat` and `REPORT_SETTINGS.example.ini` go with the
  infrastructure under the same flag; install, create, copy, restore and their checks learn the reporting
  part's fingerprint; the install message is widened ("only the updater, the reporting part or the launchers
  differ"). No new deploy tool. An install that changes only the reporting part rebuilds nothing.
- **Proof in DEV, against the backup made just before:** every forecast's scientific content and digest, every
  score, both OV-1 series, each method's identity, targets and establishment draw are equal. The envelope of a
  line (tree, time, results version, whether the result was on file) rightly changes and is the only thing set
  aside; any other normalising is stated. If a difference appears, STOP the equivalence proof and distinguish it from the move; propose a controlled
  old-code rebuild in the present environment to the owner for separate approval. Do not explain away an
  unexplained scientific difference or run it in a live tree without permission. Entry 414 accepts the
  owner's assumption of unchanged scientific packages absent a difference; record actual environment versions.
- **Route:** A (DEV, QA, PROD) or B (DEV, PROD, then `Copy_From_PROD.bat both QA`), the owner's choice after the
  proof.
- **Known and accepted:** the rebuild marks every earlier forecast as made after its result. Kept for a later
  discussion (entry 412).

## A13. Phases 2 and 3 (reporting only; no rebuild)

- **Phase 2, promptly after phase 1:** MR16 first (all its R3 events, intervals, the detectable-rate line and the
  power examples; counted once with the MR4 and MR7.PB tests it repeats) and MR5; then MR10, MR10.BOTTOM, MR11; the
  workbook's draw-detail sheet (long form, keyed by draw number, with examples of grouping by draw-number ranges),
  the "observations worth inspecting" sheet (fixed stated rules, by category, both directions, never forced to a
  number) and Excel's own charts (draw number on the axis; title, units, window and caption).
- **Phase 3:** MR2, MR3, MR8, MR9, MR12, MR13, MR15; MR6 and MR14 for methods that supply their own probabilities.
- **Not scheduled, kept in R3:** the in-sample mode; the other uses of N1; a common scored set or starting draw;
  an Oz Lotto main-plus-supplementary diagnostic.
- If a later measure needs something not stored, that is tabled by itself; a reporting change cannot create it.
  Later approximate or simulation-based measures keep R3's capability/reference distinctions and uncertainty;
  do not promise exact tails for forecast-weighted measures or silently replace/defer a required N1 reference.
  The simulation work beyond MR1 is unscheduled and any such limitation is labelled when implementing them.

## A14. Open by agreement: the measurement

Once phase 1 is in DEV the reporting part prints the time each part took. The owner runs, after a normal job:
`Run_Reports.bat LAST`; `Run_Reports.bat ALL`; `Run_Reports.bat ALL --workbooks`. Claude brings the timings back
with a recommendation. **The owner's intention:** if the timings allow, he then runs ALL once in each tree to
establish the complete text and CSV collection of A10; if they do not, the three of us settle a finer rule first.
**The measurement must not leave an unwanted permanent collection:** `ALL --workbooks` makes every draw's workbook
a request. So the third timing is taken in DEV only, and afterwards the owner deletes DEV's reports folders (which
returns DEV to LAST) and runs ALL without workbooks, unless he decides to keep them. No time is promised before the
measurement.

## A15. Tests (permanent, on invented draws; no real updater, no live tree)

- Every measure and sort worked by hand on a small invented history, both games, both readouts; ranks, ties and
  the unranked.
- Tails: against brute-force counting on a small invented game; R3's own example (no Division 9 win in 291 draws:
  2.29 deficit sigma); equality at the observed value; very small tails; MR1's bounds in the right direction and
  around support boundaries; MR17.SUM's convolution and MR17.EQ's tail against enumeration.
- Yardstick counts: identical events once; several sorts once; unchanged when sorts are switched off.
- The grid tag for each of its reasons; LOW_N; retirement.
- Reports: introduction, yardstick and a legend entry for every column printed; the CSV rectangular; workbook
  sheets and values read back; no draw ordered or grouped by anything but its number.
- Settings: defaults, a switch, an unknown name refused. LAST, DRAW n, ALL; stale reports removed and remade;
  copied reports replaced; a failed output and a locked workbook reported and marked.
- Isolation: a change to the reporting part or its settings changes no forecast, score, OV-1 line or engine
  fingerprint; `Run_Reports.bat` starts no job; the reporting part refuses on stale inputs.
- The moved print-outs: the same bytes for the same inputs. Install, copy and restore carry the reporting part.

Additional focused acceptance cases arising from independent review:
preserve the endpoint inventory across a full rebuild, a stopped job and retry;
the engine never deletes the reports folder; the first migration removes the old
league files and makes LAST alone; a job that catches up several draws reports each
(one workbook, the latest); the earlier latest workbook removed unless asked for; a
reports folder deleted by hand starts again with LAST; a retirement from draw R
leaves reports through earlier draws valid and unchanged, and marks those through R
or later; a newly installed method with earlier scores makes the earlier reports
stale and is included in them; complete coverage, once established, is maintained,
a newly available earlier scored draw included; a failed output is retried;
regenerating more than is stale gives the same bytes as regenerating only that; ALL without
--workbooks maintains existing requested workbooks; stale input refusal after a
source correction; blocked reason bound to the correct stored series; zero finite
Z, unbounded intervals, non-adjacent overlaps and provable ties; retirement exactly
at the endpoint; duplicate division-one aliases; nonzero deficit despite zero
wins; no prose rows in the new ranking CSV. Check XLSX cell types, numeric precision,
metadata and reproducibility without assuming Excel is installed or adding an
unapproved dependency (standard ZIP/XML readback is sufficient for basic checks).
Use identical inputs for same-byte moved print-out checks; distinguish intentional
legend additions and newly generated XLSX metadata from science.

## A16. What is asked, and the order of work

- **Claude:** confirmed, with the changes of v0.4 (decision log entries 416 and 417).
- **The reviewer:** confirm the changes of v0.4.
- **The owner:** ratification of this single document (it would be RAT-74).
- **Then:** Claude's code plan (files, the MR1 grid benchmark, the stored metadata of A11 and endpoint preservation of A10, the core columns as
  built), the code and tests in DEV for the reviewer's reading, the proof, the owner's installs on his separate
  go, the measurement, the owner's ALL in each tree, the manual and handovers; phase 2; then the tidy.

# Part B - Specification Amendment A1

Amends: `doc/Predictive_Randomness_System_Specification_v0_6.md` (section 9 and the specified surviving provisions) and `exchange/Claude_The_Simple_Scheme_v0_2_20261126.md` (sections 2, 4, 5 and 6 and directly related cleanup wording). R3 v0.5 section 17 is retained with the explicit departures below.

## B1. Specification v0.6, section 9: replaced

Section 9 is replaced by the following.

> **9. Saved reports**
>
> **9.1 The reporting part.** Every saved report is made by the reporting part, `src/reporting/`, which is separate
> from the engine. It reads the stored lists, the results on file, the methods' declarations and small files and
> the tree's settings, through the engine's reading and checking code. It computes evaluation measures and prints
> them. It computes no forecast, score or OV-1 line; it changes no scientific record or fingerprint; it starts no
> research job, rebuild or updater; it writes only under `results/research/<GAME>/reports/`. No report's scientific figures are ever an
> input to a method, a score or another report. Output inventory and input identities are bookkeeping only. It works under the tree's lock.
>
> **9.2 Its own identity.** The reporting part is not part of the engine's fingerprint. It has a fingerprint of
> its own, kept with the reports it made. A change to it, or to the report settings, makes reports again and
> nothing else.
>
> **9.3 Acceptable inputs only.** If the engine in the tree is not the one the stored results were made with, or a
> method's stored lists were not made by the method installed, or a list fails its checks, or other material
> scientific inputs or stored OV-1 series/metadata are inconsistent, the reporting part makes no report for that
> game and says what the owner must put right. Existing reports cannot be represented as current on refusal.
>
> **9.4 The time axis.** The game's draw number is the only scientific time axis in every report, in every format:
> orders, windows, gaps, streaks, endpoints, groupings and chart axes. Clock times record only when a file was
> made. Games are never pooled or joined.
>
> **9.5 The files.**
>
>     results/research/<GAME>/reports/rankings/d<draw, 5 digits>/   the ranking reports through that draw
>     results/research/<GAME>/reports/next/next_draw_<GAME>_d<draw>.txt  and  .csv
>     results/research/<GAME>/reports/ov1/ov1_prevailing_<GAME>.txt  and  .csv
>     results/research/<GAME>/reports/ov1/ov1_exploratory_<GAME>.txt  and  .csv
>     results/research/<GAME>/reports/README.txt  and  made_times.csv
>
> **9.6 The ranking reports** replace the league report. For a requested draw T they are cumulative: each track
> over every draw up to T it has a score for (its own scored draws). **A track is one readout of one method, TOP or
> WORST;** all tracks of a game are ranked together by the same rules. The measures are those of R3 v0.5 section 17
> in the phases of section B4 of this amendment, and MR17. Each measure has one or more named sorts; a rank is
> computed for every sort. Where a measure admits a fair reference, show exact inclusive tails where established (MR1 exact or a stated
> bracket, or labelled N1 fallback), with signed sigma and separate tails; later approximate or simulation
> references are labelled according to the applicable definition and limitations. Preference/descriptive scores
> without p-values do not acquire one. Every report states its
> yardsticks and their scopes, as reference lines and never as error bounds. Every figure is exploratory and
> descriptive: "A descriptive order. It selects nothing."
>
> **9.7 Formats.** A text report for each sort switched on: a reading view with fixed core columns, the columns of
> its criterion and the rank columns of the sorts switched on. One CSV for each game and draw with every track and
> every implemented applicable value, tail, sigma, rank and tag, rectangular. One Excel workbook for each game
> and requested draw with the same data and its legends, subject to format and scope selection in A8-A10. **Every text report begins with a plain-English introduction and ends with a legend that
> explains every column it prints, with worked examples;** the workbook carries the full legends.
>
> **9.8 Settings.** `REPORT_SETTINGS.ini` at the tree's root is the owner's own in each tree: never replaced by an
> install or a copy, and held in backups. It switches which sorts have a text file and which formats are written,
> and nothing else: every implemented applicable measure is computed and is in the enabled complete CSV and workbook, and the
> yardsticks count every distinct applicable test the reporting part computes for the game, whatever is switched on. Absent, the distributed
> defaults apply. An unknown name is refused.
>
> **9.9 Which draws.** Every research job ends by making the reports for each newly scored draw, the latest
> included (LAST). `Run_Reports.bat` makes reports alone: LAST, DRAW n, or ALL (every scored draw, recalculated),
> with the game and workbook options in A2/A8. The intended end state is reports for every scored draw, kept
> current, once the owner has run ALL (A10, A14). The next-draw reports and the
> OV-1 print-outs are made at every run, as before this amendment.
>
> **9.10 No stale report.** Reports are derived and replaceable. Each game's reports folder notes what its reports
> were made from. Everything in a report is read relative to its own draw-number endpoint. A report through draw T
> is stale when something it shows would now come out differently: a change to the reporting part, the settings,
> the engine or the tree; a changed forecast, score or OV-1 line at or before T; a method with a target at or
> before T added, removed or changed; a retirement from a draw at or before T. A later draw, a retirement from a
> later draw, or a method whose targets all lie after T does not make it stale. Every stale report is removed and
> made again in the formats and sorts switched on. More than is stale may be regenerated where that is the simplest
> correct implementation; never less. Failed outputs are retried, and complete coverage, once established by ALL,
> is maintained. The reporting part alone manages the reports folder; the
> engine does not delete it. Its inventory of the endpoints held and the workbooks asked for survives
> interruption and rebuild; missing valid outputs are retried, and invalid or disabled ones removed. At the first
> migration the old league files are removed and are not requests. A workbook is kept for the latest scored draw
> and for each endpoint asked for; ALL without a workbook request creates no other. Earlier editions are not kept in the tree; backups hold them.
>
> **9.11 Failure.** If a report cannot be made, the forecasts and scores stand; the output is absent or marked NOT
> CURRENT, never left posing as current; the run names it and ends as incomplete.
>
> **9.12 Report provenance.** Each report identifies its tree, game, draw endpoint, number of applicable units
> shown/ranked, foreign lists ignored and retrospective/before-result-on-file provenance, as applicable. For the
> new rectangular ranking CSV use data columns and the associated text/workbook/side-file metadata, not prose
> rows. Moved next-draw/OV-1 outputs keep their original layout before declared legend changes. Making times
> belong in the side file; same inputs give the same text/CSV bytes. For XLSX require reproducible data and
> semantics and deterministic file metadata where practical; do not treat ZIP/container metadata differences as
> scientific changes.

## B2. Other sentences of specification v0.6

- **Section 0, item 6:** "saves a league report after every draw" is read as "ends by making the reports for
  each newly scored draw".
- **Section 10.5:** "It is rebuilt with the league reports" is read as "its print-out is made at every run of the
  reporting part". OV-1's arithmetic, its two series and its main-barrel scope are not changed.
- **Elsewhere:** "league report" and "the league" are read as "the ranking reports" of section 9 above.

- The still-applicable wording of sections 5.7, 7 and their examples requiring a league report at each
  individual scored draw is read subject to the replacement section 9: the engine completes its science
  in draw order, then reports each newly scored draw (LAST) and keeps the endpoints it holds current. ALL
  remains available.
- Do not reactivate old administrative provisions already superseded by the simple scheme section 11
  (including old cutoff/not-current barrier machinery, chains, status files and historical rerun commands).
  The new report-currency bookkeeping in section 9 is only for derived presentation outputs. Other
  cross-references to per-draw league publication are read consistently with the same rule.

## B3. The simple scheme v0.2

- **Section 2** ("the league measures ... as the specification v0.6 ... sections ... 9 ... describe them"): read
  with section 9 as replaced above.
- **Section 4, the infrastructure's fingerprint:** "one SHA-256 over every file under `src\` outside the method
  families" is read as "... outside the method families, the results updater (`src\updater`; entry 356) and the
  reporting part (`src\reporting`)". The updater and the reporting part each have a fingerprint of their own.
- **Section 5, step 4:** "everything is rebuilt" no longer includes deleting the reports folder: the reporting
  part finds its reports stale and makes them again.
- **Section 5, step 6:** replaced by "Make both OV-1 series again; then start the reporting part, which makes the
  reports for each newly scored draw. If the reports are incomplete the job says so; its forecasts and scores
  stand."
- **Section 6, the commands:** one row is added: "`Run_Reports.bat [LAST | DRAW <n> | ALL [--workbooks]]
  [--game POWERBALL|OZLOTTO|BOTH]` | every tree | makes reports alone, from stored scientific records;
  computes evaluation measures, no forecasts, real scores or OV-1 lines". For `Copy_From_PROD.bat`: the destination's job
  makes the destination's own reports under its own report settings, which the copy does not touch.
- **The root files of a tree** gain `Run_Reports.bat` and `REPORT_SETTINGS.example.ini`. The local
  `REPORT_SETTINGS.ini` is not a distributed root file. An engine rebuild does not delete the reports
  folder (A10); the reporting fingerprint and launchers participate in the existing infrastructure
  flag and install/copy/restore checks, not the scientific engine fingerprint.

## B4. R3 v0.5 section 17: what becomes of every measure

R3 v0.5 stays in `doc/` unchanged and remains the source of every definition. Phase 1 comes with the engine's one
change; phases 2 and 3 are changes to the reporting part alone.

| Measure | Short meaning | Unit | Disposition |
|---|---|---|---|
| MR0 | Prizes by division, best first | track | Phase 1 |
| MR1 | Prize rarity (bits) | track | Phase 1; raw and Z sorts; exact or bracketed tail in place of N1 |
| MR1-T | The owner's 90/7/3 | track | Phase 1; unchanged; no sigma |
| MR2 | Division recurrence period | track | Phase 3 |
| MR3 | Division "due" alignment | track | Phase 3 |
| MR4 | Division wins against luck | track | Phase 1: every MR4.X.d and MR4.C.d (MR4.C.D shown as "any prize"), and MR4.B.2-3; the owner's MR4.C.3, MR4.B.2-3 and MR4.X.3 on by default |
| MR5 | Mean rank of the drawn numbers | method ranking | Phase 2, first |
| MR6 | Logarithmic probability quality | method probabilities | Phase 3, for methods that supply their own probabilities |
| MR7 | Total main hits; Powerball hits | track | Phase 1: MAIN and PB, each with rate, raw-total and Z sorts |
| MR8 | Longest match streak | track | Phase 3 |
| MR9 | Early against late | track | Phase 3 |
| MR10, MR10.BOTTOM | Discounted gain from the top; from the bottom | method ranking | Phase 2 |
| MR11 | TOP against WORST | TOP and WORST pair | Phase 2 |
| MR12 | Match surprisal | track | Phase 3 |
| MR13 | Bayes factors | track | Phase 3 |
| MR14 | Probability fidelity | method probabilities | Phase 3, as MR6 |
| MR15 | Periodicity of match counts | track | Phase 3 |
| MR16 | Hit rates with exact intervals | track | Phase 2, first; all its R3 events; counted once with the MR4 and MR7.PB tests it repeats |
| MR17.SUM (new) | Main hits plus Powerball hits | track, Powerball | Phase 1; defined in A4 |
| MR17.EQ (new) | Both barrels on their fair-draw scales, added | track, Powerball | Phase 1; defined in A4 and A5.4 |

MR17 names two reporting measures. It is not a forecasting method and changes no prize-based measure.
**Kept in R3 and not scheduled:** the in-sample mode (MRD-23); the uses of N1 other than MR1's; a common scored
set or a starting draw as further comparison views; an Oz Lotto main-plus-supplementary diagnostic.

## B5. Where the living system departs from R3 section 17

| R3 section 17 | Now | Why |
|---|---|---|
| The common scored set by default (17.3.7) | Each track's own scored draws by default, with n, first and last scored draw numbers and missing targets shown | Histories run from 29 to 449 scored draws; exact references allow for n |
| Walk-forward and in-sample side by side (MRD-23) | Walk-forward only | In-sample needs computing of its own; kept, not scheduled |
| MR1's sigma from N1 | An exact tail, or a stated bracket; N1, labelled, only if that proves impractical | The division chances are the same for every ticket |
| Excess sigma as the significance sort (MRD-06) | Signed sigma and raw-excess secondary key for phase 1 (A6); both inclusive tails and both sigmas kept | Both ends in one list; explicit changed sort keys |
| Cohorts, families, the search log and calibration labels (17.3.7, 17.5.2, 17.5B) | Not brought back. Each figure carries plain words (exact; bracket; approximate; a reference; not a chance), the grid tag, and the count of distinct tests in its yardstick | The simple scheme; every table is exploratory |
| Windows capped by the holdout | Cumulative through the requested scored draw | No holdout in the simple scheme |
| Plain meanings of the two modes printed (MRD-24) | Every report's introduction and legend explain N-1 forecasting, that the table is a look back, and the before and after columns | The owner's wider rule on legends |
| MR7 ranked by total excess (descriptive) | Kept, beside the per-draw excess and Z, for MAIN and PB | Three sorts of one test |
| Reports written once | Derived and replaceable, by game, draw and format (section 9.10 above) | As specification v0.6 section 9 already had it |

**Unchanged and restated:** MRD-12, the draw number as the time axis; MRD-02, every division measured; MRD-03, no
forecast of supplementaries; MRD-14, MR1-T beside MR1; MRD-06, the sigma scale with deficits reported; MRD-18, the
count of tests stated with every reference line; R3 17.3.7A, the fixed opportunity grid, reported by the grid tag.

## B6. Ratification

On the owner's ratification (it would be RAT-74), install this single consolidated document in `doc/`.
It is the governing reporting design and amendment; retain the source candidates unchanged in exchange/.
The reporting work then proceeds in A16's order. Ratification is not an install or run GO; each needs the
owner's separate authority.

END.
