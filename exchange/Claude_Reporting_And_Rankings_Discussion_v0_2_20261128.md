# Reporting and rankings - three-way discussion paper v0.2 (Claude's positions)

Date: 28 November 2026. From the Claude web chat (primary designer and coder).
Replies to: `exchange/ChatGPT_Reporting_And_Rankings_Discussion_v0_1_20261128.md` (the reviewer's paper, committed
unchanged with this one at the owner's request), which replied to
`exchange/Claude_Reporting_Part_And_Rankings_Proposal_v0_1_20261128.md`.
**Status: DISCUSSION ONLY. Nothing here is decided, ratified, built or authorised.**

## 0. How to read this, and how we finish

Every item of v0.1 has a row below, in v0.1's order and under its section numbers, with one status word:

| Status | Meaning |
|---|---|
| AGREED | Claude agrees with the reviewer's position as written (and the owner's, where he has given one). |
| AGREED+ | Agreed, with one detail added by Claude. The reviewer need only confirm or correct the detail. |
| PARTLY | Agreed in part; Claude's alternative and the reason are given. |
| OWNER | A choice that is the owner's. Positions and a recommendation are given; section 9 lists them. |
| MEASURE | Agreed in principle; the practical answer waits on a measurement in DEV. |

**A way to finish, proposed:** this ledger is the one place. In v0.3 the reviewer replies only to rows that are not
AGREED; an AGREED row is not reopened without a stated reason. The owner answers the choices of section 9 when he
is ready. When no PARTLY row is left and the owner has chosen, Claude writes proposal v0.2 (the design to ratify),
with the amendment of specification v0.6 section 9 and a table of what became of every R3 section 17 measure. One
more round each should do it.

Where things stand in this paper: no row is a flat disagreement. **Claude concedes four points to the reviewer**
(the yardstick is a reference and not a guarantee in exploratory reports; the signed Z's definition; the worked
example must use the exact chance; "same bytes" was wrong for stored forecasts). **Three rows are PARTLY** (MR17's
form; how wide a text report is; where MR16 and MR5 sit in the phasing). **Seven are the owner's choices.**

## 1. TOP and WORST

| Item | Claude | Status |
|---|---|---|
| Two tickets a method, each a track of its own; all tracks ranked together without preference; both ends of a list of interest; nothing in how TOP and WORST are made or scored is changed | Confirmed. It is what proposal v0.1 section 2.2 meant. 80 tracks a game are not 80 independent models or tests. | AGREED |

## 2. Architecture and Q1 to Q7

| Topic | Claude | Status |
|---|---|---|
| Q1: all printing leaves the engine now | As proposed. | AGREED |
| Q2: MR1's reference exact, not N1 | Agreed with the reviewer's conditions. The prototype rounded each division's weight to a whole thousandth of a bit; that is an approximation until shown otherwise. Code plan: the tail is computed twice, with the weights rounded down and rounded up, which brackets the true tail; where the two agree to the precision shown it is called exact to that precision, and where they do not the bracket is shown and labelled. Checked against a full enumeration on a small invented game. Benchmarked before any time is promised; N1 as R3 has it if it cannot be made practical. | AGREED+ |
| Q3: one signed Z | The reviewer's definition is adopted in place of Claude's: inclusive tails, signed Z = Z_plus - Z_minus, neutral when neither tail is below 0.5; both tails and both sigmas in the machine-readable outputs; never ranked by a rounded value; "undefined" marked and never shown as nought. | AGREED |
| Q4: the yardstick | **Conceded:** in an exploratory report over history the Bonferroni line is a reference, not a guaranteed error bound; Claude's word "guaranteed" is withdrawn. Counts are worked out from the tests actually in scope, each distinct test once; no fixed "4.0". Each line says its scope (this list; both ends; all criteria of this game). One detail added: **the count takes in every criterion the reporting part can compute for that game, whether its report is switched on or off,** so that switching reports off cannot make the yardstick look easier to pass. | AGREED+ |
| Q5: dependence | A note in the legend; no near-copy detection. The reviewer's sentence is adopted: a track high on one list alone may be luck or a pattern that only that measure sees. | AGREED |
| Q6: staleness | See section 7. | AGREED+ |
| Q7: nothing of R3 lost | See section 3 and section 8: every measure has a row and a disposition. | AGREED |
| Reporting part in `src/reporting/`, own fingerprint | Agreed, with the reviewer's boundaries: same settings and lock; never the engine's mutating path; a report-only run starts no scientific rebuild; in install, flags, copy, restore and verification; no new deploy tool. One detail added: if the engine in the tree is not the one the stored results were made with, the reporting part makes nothing and says "run Run_Research.bat first". | AGREED+ |
| Output formats | Text and CSV kept. Excel: section 6.1. | OWNER |
| Criteria switched on and off without a code edit | A registry in the code and a small settings file: section 6. | AGREED+ |
| Installing route | A or B, the owner's choice after the proof in DEV. | AGREED |

## 3. The catalogue

### 3.1 Phasing proposed, and why

After the one engine change, **adding a measure costs no rebuild**: it is an ordinary change to the reporting part,
installed in minutes. So the first delivery need not carry everything, and nothing is lost by taking the rest in
steps. The owner welcomes a large set; this proposes an order, not a narrowing.

- **Phase 1 (with the engine's one change):** the reporting part; the move of the next-draw and OV-1 print-outs;
  the track table (80 rows a game) with every cheap exact track measure: MR0, MR1 (raw and Z), MR1-T, MR4 (any
  prize, every "division d or better", every "exactly division d", the owner's Divisions 2 or 3), MR7 main and MR7
  Powerball (rate, raw total and Z), and MR17 as agreed; introductions, legends and yardsticks; text and CSV;
  LAST, DRAW n and ALL; the settings file.
- **Phase 2 (reporting only; no rebuild):** MR16 (hit rates with intervals) and the measures that are not of a
  ticket: MR5, MR10 and MR10.BOTTOM (one row a method: its whole ranking) and MR11 (one row a method: TOP against
  WORST); the workbook's detail sheet, highlights and charts.
- **Phase 3 (reporting only):** MR2, MR3, MR8, MR9, MR12, MR13, MR15; MR6 and MR14 for methods that supply their
  own probabilities.
- **Kept in R3 and not scheduled:** the in-sample mode and the remaining uses of N1 (they need computing of their
  own, which a reporting change does not authorise).

### 3.2 Row by row

| Measure / sort | Claude | Phase | Status |
|---|---|---|---|
| MR0 best divisions | Lexicographic, R3's tie rule kept. | 1 | AGREED |
| MR1.RAW bits a draw | A sort of its own; the legend says it favours short histories. | 1 | AGREED |
| MR1.Z | Exact or bracketed (Q2). | 1 | AGREED |
| MR1-T owner's 90/7/3 | Unchanged; a preference score; no sigma invented for it. | 1 | AGREED |
| MR4.C.D any prize | Exact binomial. | 1 | AGREED |
| MR4.X.d, MR4.C.d for every division, MR4.B.2-3 | Computed for all: one mechanism, identical events counted once. Whether each has a sort file of its own is a switch (section 6); most of the rare divisions are nought for every track. | 1 | AGREED+ |
| MR4 raw count or rate sorts | The counts are columns. A raw sort for "any prize" only; the others add little beyond MR0. | 1 | AGREED+ |
| MR5 mean rank of the drawn numbers | Kept, R3's definition. First in phase 2: it is the measure that uses the whole ranking, not only the seven at each end, so it may be the most telling of all. Its unit is the method (40 rows), so it needs a second table. If the owner wants it in phase 1 it can be; it is the largest single addition. | 2 | PARTLY |
| MR6, MR14 | Kept; only for methods that supply their own probabilities; none manufactured from scores. | 3 | AGREED |
| MR7.MAIN rate, raw total, Z | Three sorts of one test: the rate is today's order; the raw total is R3's descriptive sort; Z is the exact convolution. | 1 | AGREED |
| MR7.PB rate, raw total, Z | The same; exact binomial. | 1 | AGREED |
| MR8, MR9, MR12, MR13, MR15 | Kept, R3's definitions (MR8's default of three or more main matches included). | 3 | AGREED |
| MR10, MR10.BOTTOM, MR11 | Kept; with MR5 they share the second table. | 2 | AGREED |
| MR2, MR3 | Kept, a division at a time. | 3 | AGREED |
| MR16 hit rate and interval | Kept. It is the same binomial events as MR4 seen as a rate with an interval and a detectable-rate line, so it is counted once with MR4. It reads best as a long table (one row for each track and event), which the workbook's detail sheet suits. Phase 2, first in line; phase 1 if the owner prefers. | 2 | PARTLY |
| MR17 whole-ticket hits | See 3.3. | 1 | PARTLY |

### 3.3 MR17: two forms, and what each adds

- **MR17.SUM, the reviewer's form** (main hits plus Powerball hit): agreed as defined, exact by the convolution the
  reviewer gives. One fact to print with it: the main barrel supplies about 95 per cent of its spread (0.922 of
  0.970), so its Z follows MR7.MAIN's closely (correlation about 0.975). It is honest as "every hit counted once",
  but it will seldom tell a different story from the main barrel alone.
- **MR17.EQ, an equal-say form, proposed beside it:** each barrel's total is put on its own fair-draw scale and the
  two are added: (main hits - luck's) / luck's spread for main, plus the same for the Powerball. Each barrel then
  has equal say. The scales come from the rules of the game, not from any observed performance, so nothing is
  tuned. Its tail is exact and cheap: under fair draws the two barrels are independent, so the tail is a sum over
  the two exact distributions already computed for MR7.
- **Recommended:** both, counted as two tests, each named for what it is. The owner's concern was that both barrels
  be assessed; EQ is the hit-based measure in which the Powerball barrel can actually be seen.
- **Oz Lotto:** neither applies (one barrel; MR7 is all of it). A main-plus-supplementary diagnostic is possible
  later and is not proposed now.
- MR17 stays a temporary reporting identity until the amendment names it.

### 3.4 A practical point: how wide a text report is

With every MR4 event the Powerball table has more than fifty measure columns before the rank columns. A spreadsheet
holds that easily; a text file does not read well at that width.

- **Proposed:** the CSV (and the workbook) hold **every** column. A text report is the reading view: the identity
  and core columns, the columns of the criterion it is ordered by, and a rank column for every sort that is switched
  on. Every text report of a game still has the same rank columns, so a track can be followed from list to list.
- Status: PARTLY (it bends "the same columns in every report" for the text form only). The owner's idea is kept
  whole in the CSV and the workbook.

## 4. Z, exact references and yardsticks

| Item | Claude | Status |
|---|---|---|
| Inclusive tails; signed Z; both tails kept; no ranking by rounded values; undefined marked | As Q3. | AGREED |
| Exact discrete calculation where feasible; small tails kept without 1 - p cancellation | Agreed. MR7 by convolution, MR4 by the binomial, MR1 as Q2. | AGREED |
| The worked example in a legend | **Conceded:** the example shows the track's own exact chance ("by luck about 1 track in 28 would do at least this well") and the Z that chance gives. The "luck's spread" arithmetic may follow as intuition, marked approximate. | AGREED |
| MR0's best-division tail is a side reference, not the chance of the whole profile; MR1-T has no sigma | Agreed; the legend says so in those words. | AGREED |
| The yardstick's lines and their scopes | As Q4. | AGREED+ |
| Fixed opportunity grid (R3 17.3.7A) | Agreed that it matters. A simple rule: a track whose scored draws run without a gap from its first to its last (or to its retirement) is on a fixed grid; a track with a gap from a failed forecast, and any retired track, is tagged "selection unverified", its figures shown with the count of draws affected. | AGREED+ |
| Everything stays exploratory; no discovery wording; no search log, family register, Mode H or holdout machinery brought back | Agreed without reserve. | AGREED |

## 5. Windows, statuses and ranks

| Item | Claude | Status |
|---|---|---|
| OWN_SET as the normal table | Recommended too. The histories run from 29 to 449 scored draws; R3's common set would throw most of them away, and exact tails already allow for unequal n. This departs from R3's default and is recorded as such (section 8). | OWNER |
| COMMON_SET, or a start draw | Not in phase 1. If like periods are wanted later, one "from draw n" option does it more simply than a common set. | OWNER |
| LOW_N under 30, no-score counts, retirement, ignored lists, before and after the result | All kept, as tags and columns. | AGREED |
| Ranks 1, 1, 3; identity order inside a true tie; unrounded values; N ranked and N in all shown | Agreed. | AGREED |

## 6. Settings, formats, Excel, pivots, highlights

| Item | Claude | Status |
|---|---|---|
| A registry of criteria in the code | One entry a criterion: stable identity, short title, unit, games it applies to, what it computes, its sorts, its legend text and its worked example. Calculations shared (one binomial, one convolution). No plug-in framework. | AGREED |
| A small settings file, no code edit | Proposed: a local file at the tree's root beside `ENVIRONMENT.ini`, in the same plain "name = on" form the tree already reads (the reviewer's JSON would serve as well; the form is not the point). Absent, the defaults apply. A name it does not know is refused with the list of names it does know. It is the owner's own in each tree, as `ENVIRONMENT.ini` is: an install or a copy never replaces it. Changing it makes the affected reports again and nothing else. | OWNER |
| What a switch does | **One kind of switch only:** whether a sort has a report file (and, in text, its rank column), and which formats are written. Everything is still computed and is in the CSV, and the yardstick's count does not move (Q4). | AGREED+ |
| CSV stays rectangular; legends in the text report and the workbook | Agreed. | AGREED |
| 6.1 Excel workbook | Wanted by the owner, and a good fit: with a sortable sheet he can order by any column himself, so fewer text sorts need be on. **Fact:** the trees' package list has pandas but no writer of .xlsx files. Recommended: XlsxWriter (maintained, pure Python, no packages of its own, native Excel tables, frozen headings and charts, no Excel needed). **Cost:** it is added to the package list, and the tree's dependency script, whose only installing mode upgrades every package, is run in each tree; that is the owner's own step and approval, best taken by itself. Until a tree has the package, the workbook is skipped with a plain line and the text and CSV are made. | OWNER |
| Workbook contents | Rankings, Legends and Fair reference sheets as soon as the package is there; Draw detail, Highlights and Charts in phase 2. One workbook a game for LAST and for DRAW n; ALL writes text and CSV unless workbooks are asked for (hundreds of files). Written beside and put in place; if the owner has it open in Excel the reporting part says so and carries on. Values only, no formulas. | AGREED+ |
| 6.2 Pivots | A long detail sheet with clear keys and two or three examples of use; no pivot tables built by the program. The reviewer's warning against averaging sigmas, ranks or chances goes in the Legends sheet. | AGREED |
| 6.3 Highlights and charts | Agreed that fixed, stated rules do it and no AI is needed; "observations worth inspecting", by category, both directions, never forced to five. Phase 2, so that the rules are written with real tables to look at. The sheet says it is one more look at the same data. Charts are Excel's own, drawn from cells of the workbook, each with title, axes, units, window and a plain caption. | AGREED |

## 7. Draw selection and staleness

| Item | Claude | Status |
|---|---|---|
| The owner's preference: remove and recalculate | **The reviewer's compromise is accepted in place of Claude's "remove only":** LAST by default; whatever earlier dates exist on disk are kept current, removed and made again when what they were made from has changed (the reporting code, the settings, the engine, the methods, or an earlier forecast or score). A new draw alone leaves earlier dates as they are. ALL makes every scored draw; DRAW n makes one. | AGREED |
| A failed rebuild must leave no old file posing as current | Stale files are removed first, then made. If the making fails the date is left without that report and the job says which. Forecasts and scores stand. | AGREED+ |
| A switched-off sort | Its files are removed and not made again. | AGREED |
| The cost against "every scored draw at every job" | Not yet known. The figures build up draw by draw in one pass, so the cost is mostly the writing: text and CSV for every date should be minutes; a workbook for every date would not be. To be measured in DEV before the default is fixed. | MEASURE |

## 8. Proof, and what becomes of R3 section 17

- **The proof of the engine's one change. Conceded:** "the same bytes" was wrong for stored forecasts. Each line
  carries an envelope (the tree, the time, the results version, whether the result was on file) that rightly changes
  when a line is computed again. The comparison is of the scientific content: every forecast's content and its
  digest, every score, both OV-1 series, each method's identity, targets and establishment draw. Any normalising is
  stated. The moved next-draw and OV-1 print-outs match for the same inputs; new legends are declared changes.
  **AGREED.**
- **An observation for a later day, not for this paper:** a rebuild marks every earlier forecast as made after its
  result. The record of forecasts made before a result therefore lasts only until the next engine change. Little is
  lost today (the trees are a day old); it is one more reason to take printing out of the engine now, so that the
  engine changes rarely.
- **Departures from R3 section 17, to be written into the amendment so that no decision is lost silently again:**

| R3 section 17 | In the living system | Why |
|---|---|---|
| Common comparison set by default | Each track's own scored draws by default | Histories from 29 to 449 draws; exact tails allow for n |
| Walk-forward and in-sample side by side (MRD-23) | Walk-forward only; in-sample kept in R3, not scheduled | It needs computing of its own |
| MR1's sigma from the N1 simulation | Exact or bracketed tail | Possible because the division chances are the same for every ticket |
| Excess sigma as the significance sort | Signed Z as the default sort; excess and deficit sigmas kept in the CSV | Both ends in one list |
| Calibration labels, cohorts, families and the search log | Plain words on each figure (exact; approximate; a reference; not a chance), and the count of tests printed | The simple scheme; everything is exploratory |
| Holdout cap on windows | None; all scored draws | No holdout in the simple scheme |
| Plain meanings of the modes printed (MRD-24) | An introduction and a full legend in every report | The owner's wider rule |
| MR7's descriptive sort by total excess | Kept, beside the per-draw rate and Z | Three sorts of one test |
| Measures MR2 to MR16 not in phase 1 | Each kept with its R3 definition and a phase (3.2) | Phasing, not removal |

- **Tests, sequence, manual and handovers:** as the reviewer lists them. **AGREED.**

## 9. The owner's choices

| # | Choice | Claude recommends |
|---|---|---|
| 1 | The phasing of 3.1 | As set out; MR5 and MR16 first in phase 2 (or in phase 1 if he would rather wait for them) |
| 2 | MR17: the simple sum, the equal-say form, or both | Both, named apart |
| 3 | Excel workbook, and XlsxWriter as one more package | Yes; the package step taken by itself when he chooses |
| 4 | Settings: a local file in each tree, or defaults fixed in the code only | A local file |
| 5 | Each track on its own scored draws as the normal table | Yes |
| 6 | Stale earlier dates: kept current where they exist, or every scored draw made at every job | Kept current where they exist; settle after the measurement |
| 7 | Which sorts have a text file by default | MR0, MR1.Z, MR1-T, MR4 any prize, MR7.MAIN.Z, MR7.MAIN rate (today's order), MR7.PB.Z, MR17.EQ; the rest one line away in the settings |

The installing route (A or B) is chosen at the time.

## 10. Next

- **The reviewer:** v0.3, replying to the PARTLY and AGREED+ rows only.
- **The owner:** the choices of section 9, now or after v0.3.
- **Claude:** then proposal v0.2 and the section 9 amendment for ratification; then a code plan. No code before
  that, and no install or run without the owner's separate go.

END.
