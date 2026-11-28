# Amendment A1 (candidate v0.1): reporting and rankings

Date: 28 November 2026. From the Claude web chat, for the reviewer's reading and the owner's ratification.
**Status: CANDIDATE. Not ratified. It authorises no code, install or run.**

Amends: `doc/Predictive_Randomness_System_Specification_v0_6.md` (section 9 and the sentences named below) and
`exchange/Claude_The_Simple_Scheme_v0_2_20261126.md` (sections 2, 4, 5 and 6, as named below).
Read with: `exchange/Claude_Reporting_Part_And_Rankings_Proposal_v0_2_20261128.md` ("the design"), which says how
each rule here is carried out. Where the two differ, this amendment governs and the design is corrected.
Neither amended file is edited: on ratification this amendment and the design are installed in `doc/` beside them.

## 1. Specification v0.6, section 9: replaced

Section 9 is replaced by the following.

> **9. Saved reports**
>
> **9.1 The reporting part.** Every saved report is made by the reporting part, `src/reporting/`, which is separate
> from the engine. It reads the stored lists, the results on file, the methods' declarations and small files and
> the tree's settings, through the engine's reading and checking code. It computes evaluation measures and prints
> them. It computes no forecast, score or OV-1 line; it changes no scientific record or fingerprint; it starts no
> research job, rebuild or updater; it writes only under `results/research/<GAME>/reports/`. No report is ever an
> input to a method, a score or another report. It works under the tree's lock.
>
> **9.2 Its own identity.** The reporting part is not part of the engine's fingerprint. It has a fingerprint of
> its own, kept with the reports it made. A change to it, or to the report settings, makes reports again and
> nothing else.
>
> **9.3 Acceptable inputs only.** If the engine in the tree is not the one the stored results were made with, or a
> method's stored lists were not made by the method installed, or a list fails its checks, the reporting part makes
> no report for that game and says what the owner must put right.
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
> in the phases of section 4 of this amendment, and MR17. Each measure has one or more named sorts; a rank is
> computed for every sort. Where a measure can be set against a fair draw its reference is an exact tail (for MR1,
> exact or a stated bracket), with both inclusive tails kept and a signed sigma shown. Every report states its
> yardsticks and their scopes, as reference lines and never as error bounds. Every figure is exploratory and
> descriptive: "A descriptive order. It selects nothing."
>
> **9.7 Formats.** A text report for each sort switched on: a reading view with fixed core columns, the columns of
> its criterion and the rank columns of the sorts switched on. One CSV for each game and draw with every track and
> every value, tail, sigma, rank and tag, rectangular. One Excel workbook for each game and draw with the same
> data and its legends. **Every text report begins with a plain-English introduction and ends with a legend that
> explains every column it prints, with worked examples;** the workbook carries the full legends.
>
> **9.8 Settings.** `REPORT_SETTINGS.ini` at the tree's root is the owner's own in each tree: never replaced by an
> install or a copy, and held in backups. It switches which sorts have a text file and which formats are written,
> and nothing else: every measure is always computed and is in the CSV and the workbook, and the yardsticks count
> every distinct test the reporting part computes for the game, whatever is switched on. Absent, the distributed
> defaults apply. An unknown name is refused.
>
> **9.9 Which draws.** Every research job ends by making the reports through the latest scored draw (LAST).
> `Run_Reports.bat` makes reports alone: LAST, DRAW n, or ALL (every scored draw). The next-draw reports and the
> OV-1 print-outs are made at every run, as before this amendment.
>
> **9.10 No stale report.** Reports are derived and replaceable. Each game's reports folder notes what its reports
> were made from. A new draw alone leaves the reports of earlier draws valid. Any other change to what they were
> made from (the reporting part, the settings, the engine, the tree, the methods, an earlier forecast or score)
> makes them stale: the existing reports of that game are removed and made again in the formats and sorts switched
> on. Earlier editions are not kept in the tree; each backup holds the editions of its day.
>
> **9.11 Failure.** If a report cannot be made, the forecasts and scores stand; the output is absent or marked NOT
> CURRENT, never left posing as current; the run names it and ends as incomplete.
>
> **9.12 Every file says** which tree made it, the game, the draw it runs to, how many tracks it holds and how many
> are ranked, which foreign lists were ignored, and that forecasts for draws before a method's installation were
> computed afterwards. The time of making is in the side file, so the same inputs give the same report bytes.

## 2. Other sentences of specification v0.6

- **Section 0, item 6:** "saves a league report after every draw" is read as "ends by making the reports through
  the latest scored draw".
- **Section 10.5:** "It is rebuilt with the league reports" is read as "its print-out is made at every run of the
  reporting part". OV-1's arithmetic, its two series and its main-barrel scope are not changed.
- **Elsewhere:** "league report" and "the league" are read as "the ranking reports" of section 9 above.

## 3. The simple scheme v0.2

- **Section 2** ("the league measures ... as the specification v0.6 ... sections ... 9 ... describe them"): read
  with section 9 as replaced above.
- **Section 4, the infrastructure's fingerprint:** "one SHA-256 over every file under `src\` outside the method
  families" is read as "... outside the method families, the results updater (`src\updater`; entry 356) and the
  reporting part (`src\reporting`)". The updater and the reporting part each have a fingerprint of their own.
- **Section 5, step 6:** replaced by "Make both OV-1 series again; then start the reporting part, which makes the
  reports through the latest scored draw. If the reports are incomplete the job says so; its forecasts and scores
  stand."
- **Section 6, the commands:** one row is added: "`Run_Reports.bat [LAST | DRAW <n> | ALL]` | every tree | makes
  reports alone, from the stored results; computes nothing else". For `Copy_From_PROD.bat`: the destination's job
  makes the destination's own reports under its own report settings, which the copy does not touch.
- **The root files of a tree** gain `Run_Reports.bat` and `REPORT_SETTINGS.example.ini`.

## 4. R3 v0.5 section 17: what becomes of every measure

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
| MR17.SUM (new) | Main hits plus Powerball hits | track, Powerball | Phase 1; defined in the design, section 4 |
| MR17.EQ (new) | Both barrels on their fair-draw scales, added | track, Powerball | Phase 1; defined in the design, sections 4 and 5.4 |

MR17 names two reporting measures. It is not a forecasting method and changes no prize-based measure.
**Kept in R3 and not scheduled:** the in-sample mode (MRD-23); the uses of N1 other than MR1's; a common scored
set or a starting draw as further comparison views; an Oz Lotto main-plus-supplementary diagnostic.

## 5. Where the living system departs from R3 section 17

| R3 section 17 | Now | Why |
|---|---|---|
| The common scored set by default (17.3.7) | Each track's own scored draws by default, with n, first and last scored draw numbers and missing targets shown | Histories run from 29 to 449 scored draws; exact references allow for n |
| Walk-forward and in-sample side by side (MRD-23) | Walk-forward only | In-sample needs computing of its own; kept, not scheduled |
| MR1's sigma from N1 | An exact tail, or a stated bracket; N1, labelled, only if that proves impractical | The division chances are the same for every ticket |
| Excess sigma as the significance sort (MRD-06) | Signed sigma as the ordinary sort; both inclusive tails and both sigmas kept | Both ends in one list |
| Cohorts, families, the search log and calibration labels (17.3.7, 17.5.2, 17.5B) | Not brought back. Each figure carries plain words (exact; bracket; approximate; a reference; not a chance), the grid tag, and the count of distinct tests in its yardstick | The simple scheme; every table is exploratory |
| Windows capped by the holdout | Cumulative through the requested scored draw | No holdout in the simple scheme |
| Plain meanings of the two modes printed (MRD-24) | Every report's introduction and legend explain N-1 forecasting, that the table is a look back, and the before and after columns | The owner's wider rule on legends |
| MR7 ranked by total excess (descriptive) | Kept, beside the per-draw excess and Z, for MAIN and PB | Three sorts of one test |
| Reports written once | Derived and replaceable, by game, draw and format (section 9.10 above) | As specification v0.6 section 9 already had it |

**Unchanged and restated:** MRD-12, the draw number as the time axis; MRD-02, every division measured; MRD-03, no
forecast of supplementaries; MRD-14, MR1-T beside MR1; MRD-06, the sigma scale with deficits reported; MRD-18, the
count of tests stated with every reference line; R3 17.3.7A, the fixed opportunity grid, reported by the grid tag.

## 6. Ratification

On the owner's ratification (it would be RAT-74) this amendment and the design are installed in `doc/`. The
reporting work then proceeds in the order of the design's section 16. Ratification authorises no install or run:
each needs the owner's separate go.

END.
