# The reporting part and the rankings: final design (proposal v0.2)

Date: 28 November 2026. From the Claude web chat, for the reviewer's reading and the owner's ratification.
**Status: FINAL DESIGN, PROPOSED. Nothing in it is built, installed or authorised.** It replaces proposal v0.1 and
gathers what the three of us agreed in the discussion papers v0.1 to v0.4 and decision log entry 414. Its
companion is the amendment `exchange/Claude_Specification_Amendment_A1_Reporting_CANDIDATE_v0_1_20261128.md`,
which holds the words to be ratified and what becomes of every measure of R3 section 17.

## 0. In short

- A **reporting part**, separate from the engine, makes every print-out. It reads what the engine has stored and
  computes no forecast and no score. A change to it makes reports again and nothing else.
- Each method's **TOP ticket and WORST ticket is a track of its own.** All tracks of a game are ranked together.
- The ranking is by **many criteria**, each a named sort of the same table, each with a rank column. Criteria are
  switched on and off in a small settings file; everything is always computed.
- Where a criterion can be set against luck it has an **exact luck figure, Z**, with both ends of the list shown.
- **Every report states the yardstick** (how far the first of N gets by luck), begins with a plain-English
  introduction and ends with a legend that explains every column it prints, with worked examples.
- Text, CSV and an Excel workbook. Reports for the latest draw by default, any draw or all draws on request.

## 1. Rules that govern all of it

1. **The game's draw number is the only scientific time axis** (MRD-12; R3 17.3.1). Every order, window, gap,
   streak, endpoint, grouping, chart axis and invalidation is by draw number. Clock times record only when a file
   was made. The two games are never pooled or joined.
2. **Everything reported is exploratory and descriptive.** "A descriptive order. It selects nothing." No report
   uses the words evidence, finding or discovery of its own contents.
3. **The science is untouched:** N-1 isolation, the forecasts, the scoring, TOP and WORST from one ranking, both
   OV-1 series (main barrel only, as ratified), the sealed Mode H records, the updater.
4. **No report is ever an input** to a method, a score or a later report.
5. **Nothing of R3 section 17 is dropped silently.** Every measure has a disposition in the amendment.

## 2. The reporting part

- **Where:** `src/reporting/`, beside `src/updater/`. Like the updater it is left out of the engine's fingerprint
  and has a fingerprint of its own, kept with the reports it made.
- **What moves into it:** all printing. The ranking reports replace the league table. The next-draw reports and
  the two OV-1 print-outs move as they are.
- **What it reads:** the stored lists (forecasts, scores, both OV-1 series), the results on file, each method's
  declaration and small files, the tree's settings. It reads through the engine's existing reading and checking
  code and never through a path that changes anything.
- **What it refuses, saying what to do** ("run Run_Research.bat first"): the engine in the tree is not the one the
  stored results were made with; a method's stored lists were not made by the method now installed; a list fails
  its own checks. It then makes nothing for that game.
- **What it never does:** start a research job, a rebuild, the updater or a scoring; write outside
  `results/research/<GAME>/reports/`; change a fingerprint or a scientific record.
- **The lock:** it works under the tree's lock, taken by itself or already held by the job that started it.
- **Commands.** Every research job ends by making the reports (LAST). A new launcher in every tree makes reports
  alone: `Run_Reports.bat [LAST | DRAW <n> | ALL [--workbooks]] [--game POWERBALL|OZLOTTO|BOTH]`.
- **Exit codes of `Run_Reports.bat`:** 0, every report asked for is made and current; 1, made but incomplete (the
  last lines name each output not made or not current, and why); 2, refused, nothing changed.
- **Inside a job:** if the reports come out incomplete the forecasts and scores stand, the job ends with its
  existing "not clean" code, and its last lines say the research is done and which reports are not.

## 3. Units, tracks and what each track is measured over

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
  but too little history; when an expected target has no score; when the track is retired before the requested
  draw; or when the records cannot show it. Otherwise **"grid as declared"**. The figures are shown either way. The
  legend says that the methods and their design were chosen with the history in view, so every table is
  exploratory whatever the tag.
- **Other tags:** LOW_N (fewer than 30 scored draws); RETIRED from draw n, with its reason; "bracket" and "order
  not resolved" (section 5.3). A value that is undefined is shown as "-" and never as nought.

## 4. The measures of phase 1

Definitions are R3 v0.5 section 17's, word for word, except MR17, which is new and defined here.
D is 9 for Powerball and 7 for Oz Lotto.

| Measure | What it is | Barrels | Luck figure |
|---|---|---|---|
| MR0 | Prizes by division, best division first (the vector W_1 .. W_D) | both | a side reference only: the chance of its best division or better at least once |
| MR1 | Prize rarity: total bits of surprise of the prizes won; shown a draw | both | exact, or bracketed (5.3) |
| MR1-T | The owner's (0.90 W_1 + 0.07 W_2 + 0.03 W_3) / n | both | none: a preference score |
| MR4.X.d | Wins of exactly division d, for every d | both | exact binomial |
| MR4.C.d | Wins of division d or better, for every d; MR4.C.D is "any prize", shown as MR4.ANY | both | exact binomial |
| MR4.B.2-3 | Wins of Division 2 or 3 (the owner's original band) | both | exact binomial |
| MR7.MAIN | Total main-barrel hits | main | exact convolution |
| MR7.PB | Times the Powerball was picked (Powerball only) | Powerball | exact binomial |
| MR17.SUM | Main hits plus Powerball hits, each hit once (Powerball only) | both | exact convolution |
| MR17.EQ | Each barrel's total on its own fair-draw scale, the two added (Powerball only) | both | exact (5.4) |

- "Both" for Oz Lotto means the seven numbers and the supplementaries drawn, as the operator counts a division;
  methods never forecast supplementaries (MRD-03).
- **MR17.SUM:** H = M + B over the track's n scored draws. The one-draw law is the main-hit law times
  (0.95 + 0.05 z); its n-th power is the exact law of the total. The legend says the main barrel supplies about 95
  per cent of its fair-draw spread, so it mostly follows MR7.MAIN.
- **MR17.EQ:** E = (M - 1.4 n) / sqrt(n x 392/425) + (B - n/20) / sqrt(n x 0.0475). Each barrel has equal say in
  the fair-draw spread; that is not equal hits, prizes or information. The weights come from the game's rules; none
  is fitted. E itself is not Z: E, both components, both tails and Z are reported apart.
- Identical events are one test (MR4.X.1 is MR4.C.1). MR0's side reference is one of the MR4.C.d figures.

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
(MR4.C.3, MR4.B.2-3, MR4.X.3, MR1-T) are nought for every track until a track wins one of Divisions 1 to 3; their
legends say so.

## 5. The luck figure

### 5.1 Tails and Z

- For a track with n above 0: P_up is the chance, under fair draws, of a total at least the observed; P_lo, of a
  total at most the observed; both include the observed value.
- Z_plus = max(0, the normal deviate whose upper tail is P_up); Z_minus likewise from P_lo; **signed Z = Z_plus -
  Z_minus.** At most one of the two is above nought. Nought means neither tail is below a half.
- Both tails and both sigmas are in the CSV and the workbook. Tails are computed and kept so that very small ones
  survive (summed from the far end; never as one minus something); the CSV carries their logarithms as well.
- Sorting uses the unrounded values. A report never ranks by a rounded figure.
- A bound of nought or an infinite sigma, if one ever arises, is shown as such; it is never averaged.

### 5.2 Exact laws

- MR7.MAIN: the n-th power of the one-draw hypergeometric law (R3 17.4.4). MR7.PB and every MR4 event: binomial.
  MR17.SUM: as section 4. These depend only on the game and n, not on the ticket, so each is computed once for
  each n and shared.
- They hold for one track on a grid fixed without regard to the outcomes scored (R3 17.3.7A). That is what the
  grid tag reports.

### 5.3 MR1: the bracket

- The total of the division weights b_d = -log2(p_d) has an exact law in principle. It is computed on a fine grid
  twice, with every weight rounded down and with every weight rounded up, and the observed total is bounded by the
  same two roundings. With L and U the two computed totals, and [l_obs, u_obs] the observed:
  P(L >= u_obs) <= P_up <= P(U >= l_obs), and P(U <= l_obs) <= P_lo <= P(L <= u_obs).
- **Display:** where both bounds give the same Z to the two decimals shown, that Z is shown. Otherwise "from - to",
  tagged "bracket".
- **Order:** by the midpoint of the two bounds of Z; if either bound is nought or infinite, by the other bound.
  Where the brackets of neighbouring tracks overlap, both are tagged "order not resolved". An overlap is never
  shown as a tie.
- The grid's fineness is fixed by benchmark in the code plan. If no practical grid makes the bounds usually agree,
  R3's simulation (N1) is used for this figure, labelled, with its uncertainty.

### 5.4 MR17.EQ: the exact tail

With k = sqrt(6272/323) (about 4.4066; irrational, and free of n): for each Powerball total b, "E at least the
observed" is "M at least m_obs + (b_obs - b) k". When b differs from b_obs that bound is never a whole number, so
the least M is settled by whole-number arithmetic; when b equals b_obs it is M at least m_obs. So

    P_up = sum over b of P(B = b) x P(M >= m_obs + ceil((b_obs - b) x k)),

from the two exact laws of 5.2, and P_lo likewise.

## 6. Ranks

- Competition ranks: 1, 1, 3. A shared rank only for a true tie on the sort's keys; inside it, lines are listed in
  identity order, TOP before WORST.
- Z sorts: signed Z, greatest first; then the raw excess; then shared. Rate and raw sorts: their value, greatest
  first. MR0: the division vector, best first; then MR1; then shared.
- A track for which a sort is undefined or does not apply is listed last, unranked. Every report says how many
  tracks are ranked and how many are shown.

## 7. The yardstick, in every report

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
- A sort with no chance attached (MR0, MR1.RAW, MR1-T, the rate and raw sorts) prints luck's expectation instead.
- The dependence note: a method's TOP and WORST come from one ranking; methods and criteria overlap. A track high
  on one list alone may be luck, or a pattern only that measure sees.

## 8. The reports

### 8.1 Files, under `results/research/<GAME>/reports/`

    rankings/d<draw, 5 digits>/rank_<GAME>_d<draw>_<sort>_<short title>.txt     one for each sort switched on
    rankings/d<draw>/rank_<GAME>_d<draw>.csv                                    every track, every column
    rankings/d<draw>/rank_<GAME>_d<draw>.xlsx                                   the workbook
    next/ and ov1/                                                              as now
    README.txt, and made_times.csv (which gains a column: current, or NOT CURRENT with the reason)

For example `rank_POWERBALL_d01593_MR7_MAIN_Z_main_hits_against_luck.txt`.

### 8.2 The text report: a reading view

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
| tags | section 3 |

### 8.3 The CSV and the workbook: everything

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
  No formula recomputes a figure. Workbooks are made for LAST and DRAW n; for ALL only with `--workbooks`.

### 8.4 Introduction and legend of every text report

- **At the top:** what the report is in three or four plain lines; game; the draw it runs to; the tree that made
  it; that forecasts use earlier draws only and that this is a look back (how many forecasts were made before
  their result is in the columns); the yardstick; the standing words.
- **Underneath, the legend:** every column printed, one by one; the criterion's identity, short title, what it
  measures, what its Z means; **a worked example from the first line of that report, using its own exact chance**
  ("by luck about 1 track in 28 would do at least this well; that is Z = +1.80"), with the "luck's spread"
  arithmetic offered only as intuition and marked approximate; what TOP and WORST are and what each end of the
  list means for each; the game's divisions and odds and how "7x1 8x4 9x9" is read; every tag; what the report
  does not say.

## 9. Settings

- **`REPORT_SETTINGS.ini` at the tree's root,** the owner's own in each tree like `ENVIRONMENT.ini`: an install or
  a copy never replaces it; a backup holds it. An example with every name and the defaults is distributed as
  `REPORT_SETTINGS.example.ini`. No file: the defaults.
- **One kind of switch:** which sorts have a text file (and so a rank column in the text reports), and which
  formats are written (text, CSV, workbook). Nothing switches a computation: every measure is always computed and
  is in the CSV and workbook, and the yardsticks do not move.
- A name it does not know, or a value that is not on or off, is refused with the list of names it knows. If a
  format is off, the run says where the full data is.
- A change of settings makes the affected reports again and nothing else.

## 10. Which draws; keeping reports current; failures

- **LAST** (the default; what every job does): the reports through the latest scored draw. **DRAW n:** through
  draw n. **ALL:** through every scored draw.
- **No report on disk is stale.** Each game's reports folder notes what its reports were made from: the reporting
  part's fingerprint, the engine's, the settings, the tree, the methods with their fingerprints and retirements,
  and the stored lists as they stood. A new draw adds lines and leaves earlier draws' reports valid. Any other
  change makes them stale: **every existing draw's reports of that game are removed and made again** in the formats
  and sorts switched on. A sort switched off has its files removed and not remade. (A finer rule may replace
  "every existing draw" if the measurement of section 14 shows a need.)
- **Reports copied from PROD** are not the destination's own (another tree, perhaps other settings): the
  destination's job removes them and makes its own. Its settings file is not touched by the copy.
- **Failure.** Stale files are removed first, then made. If a making fails, that output is absent, the run names
  the game, the draw, the format and the cause, and ends "incomplete". **A workbook that Excel holds open** can be
  neither replaced nor removed: it is left as it is, listed NOT CURRENT in `made_times.csv`, named in the run's
  last lines, and put right by the next run once Excel has let go. The other reports of that draw are still made.

## 11. The moved print-outs

- The next-draw reports and both OV-1 print-outs are made at every run of the reporting part, for the same draws
  and with the same contents as now. For the same stored inputs their bytes are the same after the move as before.
  Introductions and legends are added to them afterwards as a declared change.
- **One point for the code plan:** two things those print-outs show live today only in the job's memory (why the
  second OV-1 series stopped early, if it did; a results cutoff). The engine will store them beside the series, as
  part of its one change, so that the reporting part still only reads.

## 12. The engine's one change, installing and proof

- **The change:** `reports.py` leaves `src/research/`; the engine's fingerprint leaves `src/reporting/` out; the
  job stores the two facts of section 11 and ends by starting the reporting part. Nothing that computes a
  forecast, a score or an OV-1 line is edited. Under the present rules each tree then makes everything again, once.
- **Installing:** the reporting part, `Run_Reports.bat` and `REPORT_SETTINGS.example.ini` go with the
  infrastructure under the same flag; install, create, copy, restore and their checks learn the reporting
  part's fingerprint; the install message is widened ("only the updater, the reporting part or the launchers
  differ"). No new deploy tool. An install that changes only the reporting part rebuilds nothing.
- **Proof in DEV, against the backup made just before:** every forecast's scientific content and digest, every
  score, both OV-1 series, each method's identity, targets and establishment draw are equal. The envelope of a
  line (tree, time, results version, whether the result was on file) rightly changes and is the only thing set
  aside; any other normalising is stated. If a difference appears, it is first told apart from the move by one
  rebuild of the old code in the present environment.
- **Route:** A (DEV, QA, PROD) or B (DEV, PROD, then `Copy_From_PROD.bat both QA`), the owner's choice after the
  proof.
- **Known and accepted:** the rebuild marks every earlier forecast as made after its result. Kept for a later
  discussion (entry 412).

## 13. Phases 2 and 3 (reporting only; no rebuild)

- **Phase 2, promptly after phase 1:** MR16 first (all its R3 events, intervals, the detectable-rate line and the
  power examples; counted once with the MR4 and MR7.PB tests it repeats) and MR5; then MR10, MR10.BOTTOM, MR11; the
  workbook's draw-detail sheet (long form, keyed by draw number, with examples of grouping by draw-number ranges),
  the "observations worth inspecting" sheet (fixed stated rules, by category, both directions, never forced to a
  number) and Excel's own charts (draw number on the axis; title, units, window and caption).
- **Phase 3:** MR2, MR3, MR8, MR9, MR12, MR13, MR15; MR6 and MR14 for methods that supply their own probabilities.
- **Not scheduled, kept in R3:** the in-sample mode; the other uses of N1; a common scored set or starting draw;
  an Oz Lotto main-plus-supplementary diagnostic.
- If a later measure needs something not stored, that is tabled by itself; a reporting change cannot create it.

## 14. Open by agreement: the measurement

Once phase 1 is in DEV the reporting part prints the time each part took. The owner runs, after a normal job:
`Run_Reports.bat LAST`; `Run_Reports.bat ALL`; `Run_Reports.bat ALL --workbooks`. Claude brings the timings back
with a recommendation on whether anything broader than section 10's rule is worth having. No time is promised
before that.

## 15. Tests (permanent, on invented draws; no real updater, no live tree)

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

## 16. What is asked, and the order of work

- **The reviewer:** its reading of this design and of the amendment.
- **The owner:** ratification of both (it would be RAT-74).
- **Then:** Claude's code plan (files, the MR1 grid benchmark, the stored facts of section 11, the core columns as
  built), the code and tests in DEV for the reviewer's reading, the proof, the owner's installs on his separate
  go, the measurement, the manual and handovers; phase 2; then the tidy.

END.
