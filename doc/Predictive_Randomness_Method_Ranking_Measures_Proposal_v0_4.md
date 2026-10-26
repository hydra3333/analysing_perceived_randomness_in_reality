# Predictive Randomness - Method Ranking Measures (league tables)

**Document:** Method Ranking Measures Proposal, version 0.4.
**Author:** Claude (independent reviewer). Drafted at the project owner's request from the owner's speculative-discussion starter. Revised after ChatGPT's independent review (`MR_v0_2_ChatGPT_Independent_Review_v0_1.md`), Claude's response (`Claude_Response_ChatGPT_MR_v0_2_Review_v1.md`, SHA-256 `45c7b352...ca3b`) and ChatGPT's focused spot-check of v0.3 (`MR_v0_3_ChatGPT_Focused_Spotcheck_v0_1.md`).
**Date:** 26 October 2026 (Adelaide).

**Status:** PROPOSAL, RATIFICATION CANDIDATE.
- It records the project owner's decisions of 26 October 2026 (section 2).
- It is **not yet ratified**, and it grants **no run, coding, data-access or holdout authority**.
- It changes nothing in Package 2 v0.11, and P3 v0.2 is untouched.
- On ratification its content is **integrated into the governing documents** (section 15), not kept as a separate layer.

**Repository baseline:** `hydra3333/analysing_perceived_randomness_in_reality` at HEAD `6726963` (governing set ratified 26 October 2026).

**Holdout discipline:** this document contains no winning, Powerball or supplementary number of any draw. All figures are fair-draw reference calculations.

**ID prefixes:**

| Prefix | Meaning |
|---|---|
| `MR` | measures |
| `MRD` | owner decisions |
| `RK` | ranking-use rules |
| `PO` | pattern-origin categories |
| `MRT` | tests |
| `MRO` | open items |
| `PD1..PD9` | Powerball prize divisions |
| `OD1..OD7` | Oz Lotto prize divisions |
| `N1` | fair-draw null simulator |

None collides with existing IDs: A-, D-, I-, R2-C, R2-D, T-, W-, O-, M-INV-, ERR-.

**Changes from v0.3** (ChatGPT spot-check of v0.3; Claude's disposition: AGREE on all, with one refinement to B1):
- **B1 (N1 calibration claim):** AGREE, verified independently by exhaustive enumeration.
  - Replaying fair outcomes against fixed adaptive forecasts does **not** give a valid null for cross-track maxima, or for measures scored with forecast weights or probabilities.
  - **Refinement (verified):** it **is** exact for single-track statistics computed only from the track's own hit sequence, because a fair draw's chance of each match count is the same whatever numbers were picked, so adaptation cannot change it.
  - N1 therefore has two classes (5A): `N1_CALIBRATED` for that hit-sequence class only, and `N1_FIXED_FORECAST_REFERENCE` for everything else.
  - The cross-track global figure is Bonferroni over exact local p-values, which is valid under adaptation.
  - A full recursive simulator is a possible later design (MRO-10).
- **C1:** Bonferroni is guaranteed only with valid local p-values and a predeclared family; otherwise it is labelled `BONFERRONI_REFERENCE_UNCALIBRATED`.
- **C2:** probability capability is per channel.
- **C3:** analysis units (3.4A); each hypothesis counted once.
- **C4:** MR6 zero probabilities allowed (log score minus infinity), with a typed status. Claude's extension: a zero anywhere in q makes the fair-relative reference undefined for that target, so that target is excluded from MR6's significance figure but kept in the raw score.
- **C5:** MR14 moments parameterised by draw size K, with a residual guard.
- **O1:** Monte Carlo interval contract.
- **O2:** MR3's next opportunity is labelled hypothetical.
- **O3:** no change.
- **New:** MR16 hit-rate estimate with exact interval and detectable-effect line (owner request; MRD-22).
- **New:** WF and IS results shown side by side for every applicable measure, each mode keeping its own rank column (owner request; MRD-23; section 7.5).
- **New:** plain-English definitions and self-explanatory display names for WF and IS, printed in every report (owner request; MRD-24; section 3.5A).

**Changes from v0.2:**
- **ChatGPT's review findings, as agreed (MRD-15):**
  - B1: in-sample significance labelled `IS_NOT_CALIBRATED` and shown, not suppressed. Both reviewers now treat B1 as a CORRECTION.
  - B2: Sidak removed; Bonferroni over predeclared families; the N1 maximum statistic; a search log.
  - B3: MR15 approximations labelled and calibrated by N1.
  - B4: recurrence uses scored-opportunity gaps.
  - C1-C10 applied.
  - The stage-1 contract fields adopted.
- **New measures and components:**
  - MR6-MR10 (ChatGPT's proposals) and the MR10.BOTTOM mirror adopted (MRD-16);
  - N1 fair-draw null simulator adopted (MRD-17);
  - multiplicity rules (MRD-18);
  - defaults ratified (MRD-19).
- **Exposure record:** item 6 drafted as the separate `HOLDOUT_EXPOSURE_RECORD_v0_2.md` (MRD-20).
- **Principles:**
  - "mark, never suppress" (MRD-21);
  - evidence tiers and the four pattern-origin categories (section 3.9);
  - calibration-status labels (section 5).

---

## 0. Scope in one paragraph

After the project has produced forecasts for many historical target draws, the owner wants to **rank the methods by how successful their forecasts would have been**, always separately for Powerball and Oz Lotto.
- It runs **independently of production prediction runs**.
- It uses prize divisions and further statistical measures.
- It prints every number used, with a plain explanation of what each measure means and how far each figure can be trusted.

There are two modes:
- **Walk-forward (WF):** the honest mode. Each forecast used only draws before its target.
- **In-sample (IS):** a diagnostic the owner explicitly requested, knowing it is biased. The method is trained once on all available draws, and that fit is scored against draws that were part of its own training.

The modes are never ranked against each other as competitors, but every applicable measure is shown with both modes side by side.

The project is deliberately speculative. Conventional statistics is used here **as an instrument for telling kinds of pattern apart, never as a gate** on which ideas, methods or measures may be investigated or reported.

---

## 1. Purpose (the owner's intent, restated)

1. Measure, for each method and each of its readouts (TOP and WORST), how its forecasts would have fared against actual results over a window of past draws.
2. Express that success in complementary ways:
   - prize divisions won;
   - total matches;
   - how often and how regularly wins recur;
   - whether a further win looks "due";
   - streaks and trends;
   - rank-based and probability-based quality;
   - how improbable the results are under a fair draw, on the sigma scale;
   - several statistical and quantum-inspired measures.
3. Produce league tables per game and mode, saved to files that hold the rankings, every number behind them, and a plain-English explanation of each measure, with its calibration status and evidence tier.
4. Keep the rankings as **reports**. They never alter forecasts. Any use of rankings to choose methods is itself a registered, honestly tested method (section 9).

The owner expects the most likely final outcome to be that no method predicts as hoped. The aim is to find out whether careful, broad testing can spot anything conventional statistics has missed. A well-measured null result is a valid outcome.

---

## 2. Owner decisions recorded (26 October 2026)

| ID | Decision |
|---|---|
| MRD-01 | The league-table concept is accepted, with Claude's corrections: in-sample bias labelled; modes never mixed in one ranking; Oz window within the current format; supplementaries; meta-method rule; housekeeping. |
| MRD-02 | Measure and report **all prize divisions** (Powerball 9, Oz Lotto 7), not only Divisions 1-3. Very small numbers are acceptable; full-width integers and floats were chosen for this. |
| MRD-03 | **The ratified rule changes so that supplementary numbers are included in scoring** (Oz Lotto Divisions 2, 4 and 7 need them; the Oz master already stores them). **Scope: scoring and measuring only, never predicting.** Apart from Powerball's separate barrel, a prediction is only a set of numbers, and no number is designated in advance as a supplementary (section 8). |
| MRD-04 | **Current-format draws only** (Proposal section 3.1). The Oz Lotto window never starts before draw 1474 (17 May 2022). |
| MRD-05 | Rankings never feed forecasts. Claude decides the rule for any use of rankings to choose methods (section 9). |
| MRD-06 | Significance is shown on the **sigma scale used in public science reporting** (1 to 6 sigma). **Zero wins is 0 excess sigma.** A deficit sigma is reported separately and can be nonzero when wins were expected (section 5). |
| MRD-07 | Housekeeping: measure IDs `MR..`; the weight typo corrected; processing in draw-number order; UTC timestamps in file names; windows never past opened and scored draws. |
| MRD-08 | Claude's measures MR11-MR15 are accepted (formulas as corrected in this version). |
| MRD-09 | **Reporting rule:** every measure, method, variant, status and mode is reported with its **ID, name, one-line summary and a short explanation**, so its meaning is never lost from a report. |
| MRD-10 | The forecast for target draw N is trained on the current-era draws from the era's first draw through **N-1 inclusive**. |
| MRD-11 | One numbering convention everywhere (section 3.2), consistent with conventions R2/R3 already use. |
| MRD-12 | The time axis is the **draw number** (already ratified). "Date order" means ascending draw-number order. |
| MRD-13 | The ranking is run **independently** of production prediction runs, never inside the weekly FINAL batch. |
| MRD-14 | Keep **MR1-T**, the owner's 90/7/3 weighting of Divisions 1-3, alongside the all-division score MR1. |
| MRD-15 | Accept ChatGPT's findings B1-B4, C1-C10, O1-O8 and the stage-1 contract fields, **with Claude's dispositions** (Claude response v1). |
| MRD-16 | Adopt MR6-MR10 (ChatGPT's proposals) and the optional mirror MR10.BOTTOM. |
| MRD-17 | Adopt the **N1 fair-draw null simulator** (section 5A). |
| MRD-18 | **Multiplicity:** Bonferroni over comparison families declared in advance is the guaranteed global figure; the N1 maximum-statistic figure is shown alongside (v0.4: as a labelled reference for adaptive methods, section 5A); a programme-wide search log counts every report; exploratory tables are allowed, labelled and counted (section 5B). |
| MRD-19 | Defaults: the MR13 prior scale is 0.5, also tested at 0.25 and 1.0; results on fewer than 30 draws are flagged `LOW_N`; the extra Oz Lotto measures use main numbers only; N1 runs **R = 10,000** replicates per calibrated table. |
| MRD-20 | Record exposure item 6 (ChatGPT's unsolicited search preview) in `HOLDOUT_EXPOSURE_RECORD_v0_2.md`. |
| MRD-21 | **Mark, never suppress.** The owner knowingly accepts in-sample bias. Every number requested is calculated and shown. Where a figure is not a calibrated probability, it carries a label saying so; it is never withheld for that reason. |
| MRD-23 | Show **walk-forward and in-sample results side by side** for every applicable measure. Each mode keeps its own rank column; the two modes never compete in a single ranking (section 7.5). |
| MRD-24 | The terms **walk-forward** and **in-sample** are generic, so every report prints their exact meaning in this project, and every table and file header uses self-explanatory display names (section 3.5A). |
| MRD-22 | Adopt **MR16**, the hit-rate estimate with an exact interval and a "detectable at this n" line, so the limits of the small samples are visible in every report. |

---

## 3. Conventions and definitions

### 3.1 Identity and time axis

- Every draw is identified by `(game_id, draw_number)`; `game_id` is `POWERBALL` or `OZLOTTO`. Draw numbers are the operator's official numbers.
- **The draw number is the time axis.** All processing is in ascending draw-number order. Dates are never used for ordering or arithmetic.
- Games are never pooled. Every table, statistic, file and ranking belongs to one game.

### 3.2 Numbering conventions (the single "base" for everything)

There is no zero-based or one-based re-indexing of draws. Where R2/R3 already fix a convention, it is used unchanged.

| Quantity | Convention |
|---|---|
| Draws | Always by **official draw number** (for example Powerball 1286), never by position. |
| Ball labels | Printed values: Powerball main 1-35, Powerball 1-20, Oz Lotto 1-47. (Existing convention.) |
| Rank positions | **1-based, 1 = best.** Matches R3's mid-rank convention (1 = highest predicted). |
| Training set for target N | Era first draw through N-1 inclusive (3.3). |
| Draw-number gap, a < b | b - a; consecutive draws have gap 1. |
| Scored-opportunity index | Within a stated comparison set C, sorted by draw number, the 1st scored target has index 1, the 2nd index 2, and so on (3.8). |
| Counts | Plain counts from 0. |
| Internal array indices | May be 0-based internally; **never** appear in records, files, file names or reports. |

### 3.3 Training set (walk-forward)

For game G with first current-era draw E(G) (Powerball 1144, Oz Lotto 1474):

    H(N) = { eligible draws d of game G with E(G) <= d <= N - 1 }

This is the ratified strict N-1 rule (R2), in the owner's words: "0 to Pi-1 inclusive when predicting Pi", where 0 is the era's first draw.

### 3.4 Track and entry

- A **track** is a forecast stream (game, method E_n, variant, readout, mode), with readout `TOP` or `WORST` and mode `WF` or `IS`.
- Per target draw a track supplies one **entry**:
  - Powerball: 7 distinct main numbers from 1-35 plus 1 Powerball from 1-20;
  - Oz Lotto: 7 distinct numbers from 1-47.
- Methods never forecast supplementaries (MRD-03). An unavailable readout (for example `INVERSE_UNAVAILABLE`) leaves that target unscored for that track, and the status is counted.
- TOP and WORST of one method and variant come from **one ranking**. They are dependent and never counted as unrelated evidence.

### 3.4A Analysis units

Each measure is computed on exactly one analysis unit:

| Unit | Meaning | Measures |
|---|---|---|
| `READOUT_TRACK` | One readout (TOP or WORST) of one method/variant/mode | MR0-MR4, MR7, MR8, MR9, MR12, MR13, MR15, MR16 |
| `METHOD_VARIANT_RANKING` | The single full ranking of one method/variant/mode | MR5, MR10, MR10.BOTTOM |
| `METHOD_VARIANT_PROBABILITY` | The probability vector(s) of one method/variant/mode | MR6, MR14 |
| `TOP_WORST_PAIR` | The paired TOP and WORST readouts of one method/variant/mode | MR11 |

- CSV rows, league-table rows and family test counts are keyed by `(analysis_unit, unit_id, sub-measure)`.
- A method-level value is never duplicated into two apparent TOP and WORST tests, and each distinct hypothesis is counted once in M.
- If one readout is unavailable for a target, `TOP_WORST_PAIR` measures skip that target, and the count is reported.

### 3.5 Modes

- **WF:** the entry for target N comes from the method's frozen forecast record for N, fitted on H(N) (R2/R3 historical evaluation).
  - The ranking tool **does not re-run methods** in WF; it reads stored frozen records.
  - A retrospective WF run done after all outcomes are known still needs mechanical no-leakage proof and frozen input identities. It is historical evaluation, not advance-frozen prospective forecasting (3.9).
- **IS:** section 7. One full fit on all eligible draws up to the window end, applied to every target. Labelled `IN_SAMPLE_DIAGNOSTIC`.

### 3.5A Plain meanings of the two modes (MRD-24; printed in every report)

The short codes `WF` and `IS` are used in IDs and file names. Everywhere a person reads a result (report headers, the glossary, table titles and column headings, the CSV header row and the JSON manifest), the mode is shown with its **display name and its plain meaning**, word for word as below.

**WF - Walk-forward ("honest test: trained on earlier draws only")**
> For every past draw that is scored, the method was trained **only on the draws before it**, then its prediction for that draw was compared with the actual result. This is exactly the position in real life, where the next draw is unknown when the prediction is made. It is an honest test of prediction.

**IS - In-sample ("hindsight fit: trained on all draws, including the ones scored")**
> The method was trained **once on every draw in the history**, including the draws it is then scored against, and its predictions were checked against those same draws. It shows how well the method describes results it has already seen. It is **not** a test of prediction, and its success figures are inflated by hindsight: a method with no skill at all typically gains about 3 sigma this way (section 18.3).

**Rules:**
- **Column headings** use the display names, for example "Walk-forward (earlier draws only)" and "In-sample (hindsight: all draws)". A bare "WF" or "IS" never appears alone in a heading.
- **The difference column** is headed "In-sample minus walk-forward (hindsight advantage)".
- **Every IS page** keeps the banner in 7.4, in addition to its display name.
- These texts are held in `MEASURE_REGISTRY_V1` with the measure texts and versioned with them. Test MRT-13 checks that they are present.

### 3.6 Window

- W = [S, L], inclusive draw numbers, for one game. S and L are parameters, recorded in every output.
- **Default S:** the first current-era draw on or after 1 January 2021:
  - Powerball **1286** (2021-01-07, checked in the master);
  - Oz Lotto **1474** (2022-05-17).
- **Rules:**
  - S >= E(G).
  - L is never above the latest draw that is (a) opened under the holdout rules and (b), for FINAL_HOLDOUT_10 and later, already scored from its frozen forecasts.
  - In Phase 1, L <= 1576 (Powerball) and L <= 1693 (Oz Lotto). Any other value is refused.
- **Default Phase 1 window sizes:** Powerball 1286-1576 is 291 draws; Oz Lotto 1474-1693 is 220 draws.
- In WF, a method needing more history than H(N) records `INSUFFICIENT_HISTORY` (existing status) for those targets.

### 3.7 Scored set, cohorts, comparison set and report statuses

- **Scored set:** targets in W with readout status `PREDICTION_AVAILABLE` (R3). Every other status is counted per track, with reasons.
- **Cohort:** the set of tracks in a league table.
  - **Calibrated tables** (those showing a guaranteed Bonferroni global figure) use a **predeclared cohort**, registered before the first report that uses it, with a membership digest (section 5B).
  - **Exploratory tables** may use any cohort, labelled `EXPLORATORY_COHORT`; their Bonferroni figure uses the actual number of tests, and every such table is counted in the search log.
- **Comparison set C:** by default, the intersection of the cohort's scored sets, so every track is measured on the same draws. An `OWN_SET` table (each track on its own scored set) may be produced, labelled, with n per row. The membership of C, its digest and its missing targets are recorded.
- **n** = the number of draws in C used for a measure.
- **Report-only statuses** (distinct from the R2 benchmark, R3 evaluation and registry vocabularies):
  - `MR_NOT_APPLICABLE` (capability missing);
  - `MR_INSUFFICIENT_DATA` (below a measure's stated minimum);
  - `MR_UNDEFINED` (mathematically undefined, for example a period with fewer than 2 wins);
  - `MR_NUMERIC_INVALID` (non-finite or invalid input);
  - `NULL_VARIANCE_ZERO` (the reference variance is 0, so no sigma is defined; shown as neutral).

  Undefined values are never omitted silently and never sorted as zero.
- **`LOW_N`:** set when n < 30 (MRD-19). It is one calibration flag among several and never a substitute for a valid reference.

### 3.8 Scored-opportunity gaps (used by MR2, MR3)

Within C, sorted by draw number, scored target k has opportunity index k = 1..n. For a track's wins at opportunity indices o_1 < ... < o_k:
- the **opportunity gap** is o_(i+1) - o_i;
- the **opportunities since** the last win, counted to the next draw after the window, is (n - o_k) + 1.

The +1 counts the next draw, L+1, as the next opportunity. This convention is stated in every report.

Draw-number gaps are also shown, labelled descriptive.

### 3.9 Evidence tiers and pattern origins

Every report states its **evidence tier**:
- `DEVELOPMENT_WF_EXPLORATORY`: walk-forward on development data that methods, windows and measures may have been designed against;
- `HOLDOUT_MODE_H`: FINAL_HOLDOUT_10 after Mode H scoring;
- `PROSPECTIVE`: forecasts frozen and published before their draws;
- `IS_DESCRIPTIVE`: in-sample.

A development league table is always exploratory, whatever its p-values. No development ranking alone supports a "discovery" claim. Selection provenance is recorded: method versions, windows, measures, and any development-driven changes.

Every report also explains the **four possible origins of an apparent pattern**:

| ID | Origin | How the project distinguishes it |
|---|---|---|
| PO-1 | An unavoidable consequence of how the method works | Partly diagnosable: N1 fixed-forecast replays show some method-built patterns, but not all for adaptive methods (5A). Planted-effect and null synthetic tests (MRT-07). A full recursive simulator (MRO-10) would cover more. |
| PO-2 | An effect of fitting to past outcomes | Present in IS by construction; absent in WF by N-1 isolation. Shown by the IS-versus-WF comparison. |
| PO-3 | Chance, many comparisons or selection | Bonferroni, the N1 maximum statistic, the search log, predeclared cohorts. |
| PO-4 | A pattern that persists on genuinely new outcomes | Only HOLDOUT_MODE_H and PROSPECTIVE tiers can show it. |

All four are worth exploring. The reports keep them distinct.

---

## 4. Per-draw match record and division classification

### 4.1 Match record (one per track per scored target)

Powerball record:

| Field | Type | Meaning |
|---|---|---|
| `game_id` | text | `POWERBALL` |
| `draw_number` | int64 | target draw |
| `track_id` | text | see 3.4 |
| `mode` | text | `WF` or `IS` |
| `main_matches` (m) | int64, 0..7 | entry main numbers equal to a drawn main number |
| `powerball_match` (b) | int64, 0..1 | entry Powerball equals the drawn Powerball |
| `division` | int64, 0..9 | 0 = none |

Oz Lotto record:

| Field | Type | Meaning |
|---|---|---|
| `game_id` | text | `OZLOTTO` |
| `draw_number` | int64 | target draw |
| `track_id` | text | see 3.4 |
| `mode` | text | `WF` or `IS` |
| `main_matches` (m) | int64, 0..7 | entry numbers equal to a drawn winning (main) number |
| `supplementary_matches` (s) | int64, 0..3 | entry numbers equal to a drawn supplementary; s <= 7 - m |
| `division` | int64, 0..7 | 0 = none |

These are evaluator outputs, written only after the target's outcome is opened. They are never fed back to any method.

### 4.2 Powerball divisions

Source: SA Lotteries Powerball game rules (March 2026), rule 9.4, `doc/SAL_Powerball-Game-Rules_March-2026.pdf`. Classification is a function of (m, b), so each entry wins **at most one** division, the highest it qualifies for.

**Exact fractions are primary; "about 1 in" values are rounded to the nearest whole number** (except PD9, shown to one decimal).

| Division | Requirement | Exact probability per entry | About 1 in | Bits (-log2 p) |
|---|---|---|---|---|
| PD1 | m = 7, b = 1 | 1/134490400 | 134,490,400 | 27.003 |
| PD2 | m = 7, b = 0 | 19/134490400 | 7,078,442 | 22.755 |
| PD3 | m = 6, b = 1 | 49/33622600 | 686,176 | 19.388 |
| PD4 | m = 6, b = 0 | 931/33622600 | 36,115 | 15.140 |
| PD5 | m = 5, b = 1 | 3969/67245200 | 16,943 | 14.048 |
| PD6 | m = 4, b = 1 | 5733/6724520 | 1,173 | 10.196 |
| PD7 | m = 5, b = 0 | 75411/67245200 | 892 | 9.800 |
| PD8 | m = 3, b = 1 | 28665/5379616 | 188 | 7.552 |
| PD9 | m = 2, b = 1 | 51597/3362260 | 65.2 | 6.026 |
| none (0) | every other (m, b) | | | 0 |

**Formula:**
- P(m) = C(7,m) x C(28,7-m) / C(35,7), where C(35,7) = 6,724,520;
- P(b = 1) = 1/20, independent of m.
- Over the 134,490,400 equally likely (main set, Powerball) outcomes, the division counts are 1, 19, 196, 3724, 7938, 114660, 150822, 716625 and 2063880 (independently confirmed by ChatGPT).
- Any division: 611573/26898080, about 1 in 43.98.

Division numbers follow the operator's prize order, not probability order: PD7 is more likely than PD6.

### 4.3 Oz Lotto divisions

Source: Lotterywest's Oz Lotto game page. Seven winning (main) numbers and three supplementary numbers are drawn from one 47-ball barrel, ten distinct numbers in all. Classification is a function of (m, s).

| Division | Requirement | Exact probability per entry | About 1 in (rounded to nearest) | Lotterywest published | Bits |
|---|---|---|---|---|---|
| OD1 | m = 7 | 1/62891499 | 62,891,499 | 62,891,499 | 25.906 |
| OD2 | m = 6, s = 1 | 7/20963833 | 2,994,833 | 2,994,834 | 21.514 |
| OD3 | m = 6, s = 0 | 259/62891499 | 242,824 | 242,825 | 17.890 |
| OD4 | m = 5, s >= 1 | 798/20963833 | 26,270 | 26,271 | 14.681 |
| OD5 | m = 5, s = 0 | 4662/20963833 | 4,497 | 4,497 | 12.135 |
| OD6 | m = 4 (any s) | 345800/62891499 | 182 | 182 | 7.507 |
| OD7 | m = 3, s >= 1 | 887075/62891499 | 71 | 71 | 6.148 |
| none (0) | every other (m, s) | | | | 0 |

**Formula:**
- P(m, s) = C(7,m) x C(3,s) x C(37, 7-m-s) / C(47,7), where C(47,7) = 62,891,499 and 7-m-s >= 0.
- Division counts over 62,891,499 outcomes: 1, 21, 259, 2394, 13986, 345800, 887075.
- Any division: 416512/20963833, about 1 in 50.33.

In every case checked (OD2-OD7), Lotterywest's published odds equal the exact value **rounded up** to the next whole number. The exact fractions govern.

### 4.4 Fair-draw moments used by several measures

| Quantity | Powerball | Oz Lotto |
|---|---|---|
| Mean main matches per entry | 7/5 = 1.4 | 49/47 = 1.04255 |
| Variance of main matches | 392/425 = 0.92235 (sd 0.96039) | 39200/50807 = 0.77155 (sd 0.87838) |
| Powerball match probability | 1/20 (variance 0.0475) | (no Powerball) |
| P(main matches >= m), m = 0..7 | 1, 0.823922, 0.431748, 0.124830, 0.0182608, 0.00120975, 2.92958e-5, 1.48709e-7 | 1, 0.703560, 0.276337, 0.0566231, 0.00576327, 0.000264917, 4.46801e-6, 1.59004e-8 |
| One-draw main-match probabilities p_G,m | C(7,m) x C(28,7-m) / C(35,7) | C(7,m) x C(40,7-m) / C(47,7) |

The main-match distribution is hypergeometric.

---

## 5. Significance: sigma convention and calibration labels (MRD-06, MRD-21)

### 5.1 Definitions

- **P_up:** the reference probability of a result at least as favourable as observed. **P_lo:** at least as unfavourable.
  - Example: for k wins in n draws at per-draw probability p, P_up = P(X >= k) and P_lo = P(X <= k), where X ~ Binomial(n, p).
- **Local excess sigma:** Z_plus = max(0, Phi_inv(1 - P_up)), where Phi_inv is the inverse standard normal (one-sided).
  - **k = 0 gives P_up = 1, so 0 excess sigma** (MRD-06).
- **Local deficit sigma:** Z_minus = max(0, Phi_inv(1 - P_lo)).
  - It can be nonzero for zero wins when wins were expected. Example: zero Powerball Division 9 wins in 291 draws has P_lo = 0.0111058, which is 2.28673 deficit sigma.
  - A WORST readout that avoids drawn numbers more than chance allows is a pattern of interest.
- **Sigma level:** floor(Z_plus), shown as 0-5 or ">= 6".
- **One-sided reference confidence:** 100 x (1 - P_up)%. It is the complement of a reference-model tail, **never** a probability that a method works.
  - It is rounded **down** for display, and P_up itself is always printed, so a nonzero tail never shows as "100%".
- **Bayes factors** (MR13) are not p-values. They get no sigma conversion and no multiplicity adjustment.

### 5.2 Calibration-status labels (on every significance figure)

| Label | Meaning |
|---|---|
| `EXACT_LOCAL` | Exact reference tail for this single track and sub-measure (for example binomial division counts, MR7, MR8, MR11). |
| `APPROX_UNCALIBRATED` | Normal or other approximation not yet checked against N1. Shown, labelled. |
| `N1_CALIBRATED` | Probability from N1, **only** for single-track statistics in the hit-sequence class (5A), where the replay is exact even for adaptive methods. The Monte Carlo uncertainty is shown. |
| `N1_FIXED_FORECAST_REFERENCE` | N1 replay figure for any other statistic (cross-track maxima; measures scored with forecast weights or probabilities). Shown as a reference; not a calibrated probability for adaptive WF methods. |
| `BONFERRONI_REFERENCE_UNCALIBRATED` | Bonferroni arithmetic applied where its prerequisites fail (an input not `EXACT_LOCAL`/`N1_CALIBRATED`, or a post-hoc family). Shown; not a guaranteed figure. |
| `IS_NOT_CALIBRATED` | Any significance figure in an IS table. The number is shown, but because the method was fitted on these outcomes it is not a calibrated probability (section 7). |
| `NOT_A_P_VALUE` | Descriptive scores and Bayes factors. |

### 5.3 Global significance (MRD-18)

- **Bonferroni:** P_Bonf = min(1, M x P_up) for a family of M tests; Z_plus_Bonf = max(0, Phi_inv(1 - P_Bonf)).
  - It is **guaranteed**, whatever the correlation between tests, only when every input p-value is valid under its null (`EXACT_LOCAL` or `N1_CALIBRATED`) and the family is predeclared (5B).
  - Otherwise the same arithmetic is shown, labelled `BONFERRONI_REFERENCE_UNCALIBRATED`.
  - Important and verified: the exact local tails of the hit-sequence class (MR1 by N1, MR4, MR7, MR8, MR9 by N1, MR11, MR12 by N1, MR15 by N1, MR16) **stay exact under adaptive walk-forward**, so a Bonferroni over them is a genuinely guaranteed cross-track global figure.
  - For exploratory tables, M is the actual number of tests in the table; the search log records them. Disclosure is necessary, but it is not by itself a programme-wide adjustment.
- **N1 maximum statistic:** the replay probability that the most extreme result in the family is at least as extreme as the observed one. For adaptive WF methods this is **not** a calibrated global p-value, because fixing later forecasts breaks their dependence on earlier outcomes (ChatGPT's counterexample, verified). It is shown as `N1_FIXED_FORECAST_REFERENCE`.
  - Reported as (k+1)/(R+1) (conservative), with a Clopper-Pearson 95% interval on k/R.
  - Resolution is about 1/R. With R = 10,000 it never resolves beyond about 3.7 sigma, and it is never implied to resolve 5-6 sigma.
- **The Sidak formula is not used.**
- **Reference table** (one-sided):

| Sigma | One-sided P_up | Confidence | Common description |
|---|---|---|---|
| 1 | 0.158655 | 84.13447% | |
| 2 | 0.0227501 | 97.72499% | |
| 3 | 0.00134990 | 99.86501% | "evidence" (physics usage) |
| 4 | 3.16712e-5 | 99.99683% | |
| 5 | 2.86652e-7 | 99.99997% | "discovery" (physics usage) |
| 6 | 9.86588e-10 | 99.9999999% | |

- **Printed with the table:** "The physics words apply to a single test declared in advance and confirmed on new data. They are never applied to a development or in-sample league table."

### 5A. N1 - fair-draw null simulator (MRD-17)

- **What N1 does:** it replays R sets of fair outcomes against the actual stored WF forecasts, without refitting.
- **Where it is exact: the hit-sequence class.** For a statistic computed only from one track's own per-target outcome codes (main matches m_t, Powerball hit b_t, supplementary matches s_t, division), the replay is **exact even for adaptive methods**.
  - Under a fair draw, the distribution of (m_t, b_t, s_t) for any ticket of the fixed shape is the same whatever numbers it contains. So these codes are independent and identically distributed across targets however the ticket was chosen from earlier outcomes.
  - Verified: in a 4-draw toy with an adaptive method, the true and replayed distributions of the hit count agree exactly.
  - The class covers MR1, MR4, MR7, MR8, MR9, MR11 (the TOP and WORST sets are disjoint and the same size, so the pair's joint code distribution is also invariant), MR12, MR15 and MR16.
  - For this class N1 may equally simulate the codes directly. Its results are labelled `N1_CALIBRATED`.
- **Where it is only a reference:**
  - (a) **Maxima or other joint statistics across tracks.** The joint law of different tracks' hits depends on how their forecasts overlap, and adaptive overlap depends on earlier outcomes. ChatGPT's exhaustive 4-draw counterexample, checked by Claude, gives a true probability of 1/16 but a replay probability of 15/128.
  - (b) **Single-track measures scored with forecast-dependent weights or probabilities:** MR5, MR6, MR10, MR10.BOTTOM, MR14. Verified with a forecast-weighted toy: true and replayed distributions differ.
  - These are labelled `N1_FIXED_FORECAST_REFERENCE`. Their approximate local Z stays `APPROX_UNCALIBRATED`. Martingale arguments make the standardised sums approximately normal, but that is not exactness.
- **Not valid for IS** (section 7).
- **Full recursive simulator** (MRO-10, a separate design): each replicate feeds its own simulated earlier outcomes into method refits. It would calibrate (a) and (b) properly, at the cost of running method code.
- **Generator:** per replicate, one fair draw per target in C, using exact game mechanics:
  - Powerball: 7 of 35 without replacement, plus 1 of 20;
  - Oz Lotto: 10 distinct of 47, the first 7 main and the last 3 supplementary.
  - The PRNG algorithm, seed, version and R (default 10,000, MRD-19) are recorded. Each replicate scores **every** track in the table on the same simulated draws.
  - **Monte Carlo contract:** for k exceedances in R, report (k+1)/(R+1) and the Clopper-Pearson 95% interval on k/R. Same seed and inputs give identical results.
- **Uses:**
  - exact simulated p-values for the hit-sequence class: MR15's false-alarm probability on the actual draw grid and frequency scan; validation or replacement of the MR1, MR9 and MR12 normal approximations;
  - reference figures (labelled) for cross-track maxima and for weight- or probability-scored measures;
  - partial PO-1 diagnosis.
- **Firewall:** replicates and their scores are calibration artefacts, labelled `NULL_CALIBRATION`. They are stored apart from real records, never enter any real ledger, fit or forecast, and are covered by the synthetic firewall. Results may be regenerated from the seed; storing every replicate is optional.
- **Not an admission gate:** a measure is shown whether or not N1 has calibrated it (MRD-21). N1 upgrades labels from `APPROX_UNCALIBRATED` to `N1_CALIBRATED` for the hit-sequence class, and adds `N1_FIXED_FORECAST_REFERENCE` figures for other statistics.

### 5B. Families and the search log (MRD-18)

- **Family:** a named, versioned set of (cohort, sub-measures, window, mode, game), registered in `FAMILY_REGISTRY` with a digest **before** the first report that uses it.
  - M is the number of distinct (analysis_unit, unit_id, sub-measure) tests in the family (3.4A).
  - Main and Powerball channels are separate families unless a joint family is declared.
- **Search log:** `results/method_rankings/SEARCH_LOG.csv`, programme-wide, append-only and committed. One row per report run:
  - UTC time, game, mode, window, cohort and digest, family IDs or `EXPLORATORY_COHORT`, the number of tests, measures, tool version and SHA.
  - It shows how much searching was done, including exploratory tables, reruns and window changes. A family declared after its results were inspected is recorded as such, and its Bonferroni figure is labelled `POST_HOC_FAMILY`.
- Exploration stays free: any table may be produced, provided it is labelled and logged.

---

## 6. Measure registry

Every measure has:
- its ID, name, **one-line summary** and **short explanation** (MRD-09);
- an exact definition;
- its ranking key(s);
- edge cases;
- outputs;
- its calibration status (5.2).

The texts are versioned in `MEASURE_REGISTRY_V1` and printed in every report's glossary.

**Notation:**
- `MRk.PDd` / `MRk.ODd`: measure k at Powerball / Oz Lotto division d.
- `MR4.X.d`: exactly division d. `MR4.C.d`: division d or better. `MR4.B.a-b`: band a..b.
- `.MAIN` and `.PB`: channels. Oz Lotto has MAIN only for MR6-MR15 (MRD-19).
- n = draws in C. W_d = the count of division-d wins. p_d = division-d probability. b_d = -log2 p_d.

**Two ranking tables where relevant:** a **descriptive** table (by the raw score) and a **significance** table (by local Z_plus, with global figures). They are never conflated.

**Measure IDs:** MR0-MR4 derive from the owner's R0-R10 (section 17); MR5 is R3's existing measure; MR6-MR10 are ChatGPT's (MRD-16); MR10.BOTTOM is Claude's mirror; MR11-MR15 are Claude's; MR16 is the owner-requested hit-rate interval (MRD-22). Each measure's analysis unit is listed in 3.4A.

### MR0 - Division win profile

- **One line:** who has won the best prizes, best division first.
- **Short explanation:** counts how many times the track's entries would have won each prize division. Tracks are ranked by top-division wins first, then the next division, and so on. Top-division wins are extremely rare under a fair draw, so most tracks share the same counts at the top; the lower divisions carry most of the information.
- **Definition:** V = (W_1, ..., W_D), with D = 9 (Powerball) or 7 (Oz Lotto).
- **Ranking:** V descending, lexicographic. On the common set C, equal V means equal MR1, so ties share a rank. In `OWN_SET` tables, n differs, so MR1 descending breaks ties.
- **Outputs:** W_1..W_D, n, the expected counts n x p_d. Calibration: `NOT_A_P_VALUE` (see MR4 for significance).

### MR1 - Surprisal-weighted division score; MR1-T - owner's top-division score

- **One line:** the average "rarity" of prizes won per draw, in bits.
- **Short explanation:** each division win is worth the bits of surprise it represents under a fair draw: about 6.0 bits for Powerball Division 9, up to 27.0 bits for Division 1. MR1 is the average bits won per draw, next to the fair-draw expectation. MR1-T keeps the owner's original weighting of the three top divisions (Division 1 90%, Division 2 7%, Division 3 3%); it is a declared preference score, not a statistical weight.
- **Definition:**
  - MR1 = (1/n) x sum over draws of b(division), with b(0) = 0.
  - E0 per draw: 0.153679 bits for Powerball (sd 1.025914), 0.131326 bits for Oz Lotto (sd 0.931722).
  - Z = (n x MR1 - n x E0) / (sqrt(n) x sd). This is `APPROX_UNCALIBRATED` and heavy-tailed for rare divisions, so it is replaced by an N1 p-value when available.
  - MR1-T = (0.90 x W_1 + 0.07 x W_2 + 0.03 x W_3) / n.
- **Ranking:** MR1 descending (descriptive); Z_plus (significance); MR1-T descending in its own table.
- **Outputs:** MR1, E0, the difference, Z with its label, MR1-T.

### MR2 - Division recurrence period (per division)

- **One line:** how often, on average, this track wins division d.
- **Short explanation:** for a division won at least twice, this is the average number of scored draws between successive wins. Shorter periods rank higher, with regularity shown alongside. Under a fair draw the expected spacing is about 1/p_d scored draws (about 65 for Powerball Division 9), and wins arrive irregularly. This is a pattern description; ranking the shortest period among tracks with 2 or more wins favours tracks that happened to win twice close together.
- **Definition** (per division d, per track, on C):
  - Win opportunity indices o_1 < ... < o_k (3.8), with k = W_d.
  - If k >= 2: mean opportunity period G_d = (o_k - o_1)/(k - 1).
  - CV_d = the sample sd of the opportunity gaps (denominator k - 2) divided by G_d, only when k >= 3.
  - Fair reference: 1/p_d.
  - **Also shown, labelled descriptive:** the draw-number period (N_k - N_1)/(k - 1).
- **Ranking:** defined G_d ascending, then CV_d ascending (defined before undefined), then k descending. Then k = 1, then k = 0, each sharing a rank.
- **Edge cases:** k <= 1 gives `MR_UNDEFINED`. G_d > 0 when defined.
- **Outputs:** k, the first and last win draws, G_d, CV_d, 1/p_d, the opportunity gaps, the draw-number period. Calibration: `NOT_A_P_VALUE`.

### MR3 - Division "due" alignment (per division)

- **One line:** is this track about due for another division-d win?
- **Short explanation:** compares the scored opportunities since the track's last division-d win, including the next draw, with its average period from MR2. Near 0 means the next draw falls close to the track's usual spacing. Under a fair draw wins have no memory, so this is a pattern indicator, never a reason to exclude a method. Using it to choose methods is itself a forecasting method and must be registered (section 9).
- **Definition:** requires k >= 2. since_d = (n - o_k) + 1 (3.8). A_d = |since_d - G_d| / G_d.
- **Label:** "retrospective alignment for a hypothetical next opportunity". The track may not actually forecast draw L+1, so this is never itself a prediction.
- **Ranking:** A_d ascending; undefined last.
- **Outputs:** since_d, G_d, A_d, the signed since_d - G_d, and the draw-number equivalent (labelled descriptive). Calibration: `NOT_A_P_VALUE`.

### MR4 - Division sigma (excess wins)

- **One line:** how many sigma above fair-draw chance this track's division wins are.
- **Short explanation:** counts the track's wins in a set of divisions and asks how likely at least that many would be under a fair draw over the same draws. That probability is shown on the sigma scale used in science reporting. Zero wins is 0 excess sigma. The local figure treats the track alone; the global figures allow for how many tests were made.
- **Definition:** for a division set S: p_S = the sum of p_d over d in S (exact); k_S = wins in S; X ~ Binomial(n, p_S); P_up and P_lo exact. Then section 5.
- **Sub-measures:**
  - `MR4.X.d` (every d);
  - `MR4.C.d` (every d);
  - the owner's original sets `MR4.C.3` (owner R8), `MR4.B.2-3` (owner R9) and `MR4.X.3` (owner R10).
- **Ranking:** Z_plus descending, then k_S descending, then shared rank.
- **Outputs:** k_S, n, n x p_S, P_up, the reference confidence, local Z_plus and level, Bonferroni (guaranteed) and N1 maximum-statistic (reference) global figures, local Z_minus. Calibration: `EXACT_LOCAL`.

### MR5 - Rank position (existing R3 measure)

- **One line:** where the method's ranking placed the numbers that were actually drawn.
- **Short explanation:** R3's ratified evaluator measure: the average mid-rank of the 7 drawn main numbers in the method's full frozen ranking (1 = most favoured), and the drawn Powerball's mid-rank. Fair-draw expectations are 18.0 (Powerball main), 10.5 (Powerball) and 24.0 (Oz Lotto). Lower means the method tended to favour numbers that came up. It belongs to the method and variant, because TOP and WORST share one ranking.
- **Definition:**
  - Per target, `mean_rank_main` and `rank_powerball` (R3). MR5.MAIN and MR5.PB are their means over C.
  - Per-target fair variance of the 7-label mean given the frozen mid-rank vector r: var_r x (N - 7) / (7 x (N - 1)), with N = 35 or 47.
  - Z = (sum of expected - sum of observed) / sqrt(sum of variances); `APPROX_UNCALIBRATED`, with an N1 reference figure (`N1_FIXED_FORECAST_REFERENCE`).
- **Ranking:** MR5 ascending (descriptive); Z_plus (significance).
- **Outputs:** the MR5 mean, its expectation, Z_plus, Z_minus.

### MR6 - Logarithmic probability quality (ChatGPT)

- **One line:** rewards probability forecasts that gave more probability to the numbers actually drawn, and heavily penalises overconfident misses.
- **Short explanation:** a strictly proper logarithmic score for the probability the method gave to a drawn main number (one of the seven chosen at random). It complements MR14 fidelity, but unlike MR14 it sharply penalises giving near-zero probability to a number that came up. It does not score the full seven-number event.
- **Applicability:** a typed main-channel probability output (section 13, field 3).
  - `NORMALIZED_LABEL_PROBABILITY` gives q directly.
  - `MARGINAL_INCLUSION_PROBABILITY` gives q = r/7, a valid distribution over a randomly chosen drawn label.
  - Otherwise `MR_NOT_APPLICABLE`.
- **Definition:**
  - q_j >= 0 with sum 1 over N labels (a zero is a valid, if bold, forecast).
  - g_t = (1/7) x sum over j in D_t of log2(N x q_j), which is minus infinity if any drawn label has q_j = 0.
  - Fair conditional expectation e_t = (1/N) x sum over j of log2(N x q_j), which is <= 0.
  - Variance v_t = ((N - 7)/(7 x (N - 1))) x Var_pop[log2(N x q_j)].
  - G = the mean of g_t. Z = sum(g_t - e_t) / sqrt(sum v_t); `APPROX_UNCALIBRATED`, with an N1 reference figure.
  - PB channel: g = log2(20 x q_PB[drawn]); e = (1/20) x sum of log2(20 x q_PB[j]); the corresponding population variance.
- **Edge cases:**
  - **A drawn label with q_j = 0:** the target's score is minus infinity, status `LOG_SCORE_NEG_INFINITY`. It is kept and never smoothed by the evaluator; any smoothing belongs inside the frozen method.
    - The track's G is then minus infinity, encoded as a tagged non-numeric value in CSV and JSON, and the track is placed last in the descriptive table, ties among such tracks broken by the count of such targets, fewer first.
  - **Any q_j = 0, drawn or not:** the fair reference e_t and v_t are undefined for that target, status `MR_UNDEFINED_REFERENCE`.
    - Such targets are excluded from MR6's significance figure (with the count reported) and kept in the raw score G.
    - N1 replays treat them the same way.
  - Negative, non-finite or wrongly normalised q gives `MR_NUMERIC_INVALID`.
  - Sum of v_t = 0 gives `NULL_VARIANCE_ZERO`.
- **Ranking:** G descending (descriptive); Z_plus (significance).
- **Outputs:** G, the sum of g, the mean e, the excess, Z_plus, Z_minus, n, the probability semantics, the null-variance flag.

### MR7 - Total main-match excess (ChatGPT; core stage)

- **One line:** did the track hit more main numbers in total than fair draws would produce?
- **Short explanation:** counts **every** main-number match, prize or not. It is the most direct test of a steady advantage and applies to every method that produces tickets.
- **Definition:**
  - S = the sum of m_t over C.
  - The exact null distribution of S is given by the coefficients of A_G(z)^n, with A_G(z) = sum over m = 0..7 of p_G,m z^m (4.4).
  - P_up = P(S_null >= S), P_lo = P(S_null <= S).
  - PB channel: B = the sum of b_t, ~ Binomial(n, 1/20).
  - MAIN and PB p-values are never combined without a declared joint rule.
- **Ranking:** S - n x mean0 descending (descriptive); Z_plus (significance).
- **Outputs:** n, S, S/n, mean0, Var0, observed minus expected, P_up, P_lo, Z_plus, Z_minus, the PB analogue. Calibration: `EXACT_LOCAL`.

### MR8 - Longest match streak (ChatGPT)

- **One line:** did the track achieve an unusually long run of consecutive good-matching draws?
- **Short explanation:** measures bursts of success rather than totals. A run of consecutive draws, each with at least 3 main matches, may be interesting even if the average is ordinary. It does not assume any period, or that a run will continue.
- **Definition:**
  - h = 3 (predeclared; a different h is a new sub-test). x_t = 1 when m_t >= 3.
  - R = the longest run of x_t = 1 over consecutive official draw numbers within C. An unscored target breaks a run.
  - p_h = P0(m >= 3): 0.1248297 for Powerball, 0.05662309 for Oz Lotto.
  - P0(R >= r) is computed exactly by a dynamic programme over run-length states 0..r-1, restarting at every gap:
    - v_new[0] = (1 - p_h) x sum(v_old);
    - v_new[j+1] = p_h x v_old[j] for j < r - 1;
    - the mass p_h x v_old[r-1] is absorbed.
    - P_up = the absorbed probability. R = 0 gives P_up = 1.
- **Ranking:** R descending (descriptive); Z_plus (significance).
- **Outputs:** R, its start and end draw numbers, the scored and gap counts, h, p_h, P_up, Z_plus. Calibration: `EXACT_LOCAL`.

### MR9 - Early versus late change (ChatGPT)

- **One line:** did the track's matching get better or worse in the later half of the window?
- **Short explanation:** separates a rising or falling pattern from one good overall score. It measures change over time, not whether a change will persist.
- **Definition:**
  - Split C (sorted by draw number) at n_early = floor(n/2), n_late = n - n_early. The split is fixed, never optimised.
  - Means a (early) and b (late). Delta = b - a.
  - Var0(Delta) = sigma0^2 x (1/n_early + 1/n_late), with sigma0^2 from 4.4.
  - Z = Delta / sqrt(Var0); `APPROX_UNCALIBRATED`, replaced by `N1_CALIBRATED` when N1 runs (hit-sequence class). Z_plus covers improvement, Z_minus deterioration.
  - PB channel: Bernoulli variance 0.0475.
- **Edge cases:** n < 2 gives `MR_UNDEFINED`. A change of split is a new sub-test.
- **Ranking:** Delta descending (descriptive); Z_plus (significance).
- **Outputs:** the early and late counts and means, Delta, the variance, Z_plus, Z_minus, the boundary draw numbers.

### MR10 - Top-rank discounted gain (ChatGPT); MR10.BOTTOM - bottom-rank mirror (Claude)

- **One line (MR10):** rewards placing the eventually drawn numbers very near the top of the ranking.
- **One line (MR10.BOTTOM):** rewards placing the eventually drawn numbers very near the bottom, an "inverse signal".
- **Short explanation:** MR5 weighs all rank distances equally. MR10 uses a fixed logarithmic discount, so rank 1 counts much more than rank 20, while every drawn number still contributes. MR10.BOTTOM applies the same discount from the bottom of the ranking, matching the project's interest in WORST picks and inverse signals. Neither creates a forecast or a tie rule; `TIE_SHA256_V1` is unchanged.
- **Definition:**
  - Frozen mid-ranks r_j (R3). w_j = 1 / log2(1 + r_j).
  - G_t = the sum of w_j over drawn main labels.
  - e_t = (7/N) x sum of w_j; v_t = 7 x (N - 7)/(N - 1) x Var_pop(w).
  - Z = sum(G_t - e_t)/sqrt(sum v_t); `APPROX_UNCALIBRATED`, with an N1 reference figure.
  - MR10.BOTTOM: the same with r'_j = N + 1 - r_j.
  - PB channel: w at the drawn Powerball, with expectation mean(w) and variance Var_pop(w) over 20 labels.
- **Edge cases:** sum of v = 0 gives `NULL_VARIANCE_ZERO`. These are ranking-level measures (method and variant), not per readout.
- **Ranking:** the mean gain descending (descriptive); Z_plus (significance).
- **Outputs:** the observed and expected mean gain, the excess, Z_plus, Z_minus, n.

### MR11 - TOP versus WORST contrast

- **One line:** does the method's TOP pick beat its own WORST pick?
- **Short explanation:** each method's TOP and WORST picks come from one ranking and never share a number. If the ranking carries information, TOP should match more drawn numbers than WORST; if the information is inverted, WORST will. Under a fair draw neither should win more often. This is each method's built-in control experiment.
- **Definition:**
  - Over draws in C where both readouts are scored: D_t = m_TOP,t - m_WORST,t.
  - n_plus counts D_t > 0 and n_minus counts D_t < 0; ties are excluded.
  - Exact sign test: P_up = P(Y >= n_plus), P_lo = P(Y <= n_plus), with Y ~ Binomial(n_plus + n_minus, 1/2).
  - PB channel `MR11.PB`: D_t = b_TOP,t - b_WORST,t.
- **Ranking:** Z_plus descending; a separate list of Z_minus descending headed "inverse-signal candidates".
- **Edge cases:** no non-tied draws gives 0 sigma both ways.
- **Outputs:** n_plus, n_minus, ties, the mean D, P_up, Z_plus (local and global), Z_minus. Calibration: `EXACT_LOCAL` (WF).

### MR12 - Information gain (Shannon surprisal)

- **One line:** how much more surprising, in bits, this track's matches were than chance.
- **Short explanation:** each draw's match count is scored by how surprising "at least this many matches" would be under a fair draw: 7 matches is about 22.7 bits, while 0 or more matches is 0 bits. The total is compared with the fair-draw average. This is Shannon's measure of information, the everyday-world limit of the entropy used in quantum theory. It ranks tracks even when no prize was won.
- **Definition:**
  - MAIN channel: u_t = -log2 P0(M >= m_t); U = the sum of u_t.
  - Fair per-draw mean and sd: Powerball 0.911756 / 1.138676; Oz Lotto 0.879151 / 1.143974.
  - Z = (U - n x mean)/(sqrt(n) x sd); `APPROX_UNCALIBRATED`, replaced by `N1_CALIBRATED` when N1 runs (hit-sequence class).
  - PB channel: u = 4.321928 bits on a hit, otherwise 0; mean 0.216096, sd 0.941942.
- **Ranking:** U - expected descending (descriptive); Z_plus (significance).
- **Outputs:** U, the expected U, the excess bits, Z_plus, Z_minus.

### MR13 - Bayes factor against a fair draw

- **One line:** how strongly the evidence favours "this track has some skill" (or "inverse skill") over pure chance.
- **Short explanation:** compares a fair draw with a fair draw tilted slightly towards (BF_plus) or away from (BF_minus) the track's picks. The Bayes factor says how many times better the tilted explanation fits. It can also show evidence *for* pure chance, and it behaves sensibly with small counts. Bands (Kass and Raftery) for log10 BF: below 0.5 "barely worth mentioning", 0.5-1 "substantial", 1-2 "strong", above 2 "decisive". It is not a p-value.
- **Definition:**
  - **MAIN channel:**
    - P_theta(m) = P0(m) x exp(theta x m) / Z(theta), where Z(theta) = sum over j of P0(j) x exp(theta x j).
    - With S = the sum of m_t, l(theta) = theta x S - n x ln Z(theta).
    - BF_plus = integral over theta > 0 of exp(l(theta)) x pi_plus(theta), where pi_plus is a half-normal of scale 0.5, normalised on theta > 0.
    - BF_minus is the same for theta < 0.
    - Computed by adaptive quadrature in log space.
    - Sensitivity at scales 0.25 and 1.0 (MRD-19).
  - **PB channel:** k hits in n draws; H0: q = 1/20.
    - BF_plus uses Beta(1,19) **truncated to q > 1/20** and renormalised.
    - BF_minus uses Beta(1,19) truncated to q < 1/20 and renormalised.
    - Computed through incomplete-beta and log-gamma functions.
- **Ranking:** log10 BF_plus descending; a separate BF_minus list.
- **Outputs:** log10 BF_plus, log10 BF_minus, the band, the posterior mean of theta, the sensitivity values. Calibration: `NOT_A_P_VALUE`.

### MR14 - Fidelity (classical squared Bhattacharyya affinity)

- **One line:** how closely the method's predicted probabilities matched what was actually drawn.
- **Short explanation:** for methods that state a probability for every number, this measures the overlap between that probability spread and the actual draw. The formula has the same form as the "fidelity" between two quantum states; for ordinary probabilities it is the squared Bhattacharyya affinity. **The quantum link is a mathematical analogy, not a claim of a quantum mechanism.** It suits the pilot-wave family (E_57-E_62), whose outputs are Born-rule probabilities. A uniform guess scores exactly 7/N (0.2 for Powerball main).
- **Applicability:** as MR6 (typed probability output); otherwise `MR_NOT_APPLICABLE`. A method never gains this capability by rescaling scores.
- **Definition:**
  - a_j = sqrt(q_j); F_t = (1/7) x (sum over j in D_t of a_j)^2.
  - E_t and V_t are computed exactly (algorithm below). Z = sum(F_t - E_t) / sqrt(sum V_t); `APPROX_UNCALIBRATED`, with an N1 reference figure.
  - PB channel: F_t = q_PB(drawn); E_t = 1/20; V_t = (1/20) x sum of q_j^2 - 1/400.
- **Exact moments** (stated for a general draw size K; production uses K = 7):
  - Inclusion factors: pi_k = (K)_k/(N)_k, using falling factorials.
  - Power sums: p1 = sum a, p2 = sum a^2, p3 = sum a^3, p4 = sum a^4.
  - Distinct-index sums:
    - S31 = p3 x p1 - p4;
    - S22 = p2^2 - p4;
    - S211 = p2 x p1^2 - p2^2 - 2 x p3 x p1 + 2 x p4;
    - S1111 = p1^4 - 6 x p1^2 x p2 + 3 x p2^2 + 8 x p1 x p3 - 6 x p4.
  - Moments of the drawn-subset sum:
    - E2 = pi_1 x p2 + pi_2 x (p1^2 - p2);
    - E4 = pi_1 x p4 + 4 x pi_2 x S31 + 3 x pi_2 x S22 + 6 x pi_3 x S211 + pi_4 x S1111.
  - E_t = E2/K; V_t = E4/K^2 - E_t^2. (With K = 7, F_t uses the factor 1/7 as above.)
  - Verified by exhaustive subset enumeration (MRT-11), independently by Claude and ChatGPT.
- **Edge cases:**
  - Uniform q gives V_t = 0, hence `NULL_VARIANCE_ZERO` (neutral, never NaN or infinite).
  - A computed V_t below zero by no more than 1e-12 x E4/K^2 is set to 0. A larger negative value is `MR_NUMERIC_INVALID`.
- **Ranking:** the mean F descending (descriptive); Z_plus (significance).
- **Outputs:** the mean F, the mean E, Z_plus, Z_minus, the probability semantics.

### MR15 - Spectral periodicity of match counts (Lomb-Scargle)

- **One line:** do this track's match counts rise and fall in a repeating cycle?
- **Short explanation:** looks for a repeating rhythm in the track's draw-to-draw match counts, using the Lomb-Scargle periodogram, an astronomy method for finding periods in unevenly spaced data. It reports the strongest cycle length in draws and how unusual a peak that strong would be by chance. It works even when no prize was won, and echoes the spectral method family (E_33-E_40).
- **Definition:**
  - z_t = (m_t - mean0)/sd0 at the scored draw numbers t in C (gaps allowed).
  - T = L - S + 1. Frequencies f_k = k/T for k = 1..K, with K = floor((T - 1)/2). The Nyquist frequency is excluded.
  - omega = 2 x pi x f; tau from tan(2 x omega x tau) = sum of sin(2 x omega x t) / sum of cos(2 x omega x t).
  - Power, using the known unit variance: P(f) = (1/2) x { [sum z_t cos(omega (t - tau))]^2 / sum cos^2(omega (t - tau)) + [sum z_t sin(omega (t - tau))]^2 / sum sin^2(omega (t - tau)) }.
  - Statistic: P_max over the grid.
  - **Approximate FAP** = 1 - (1 - exp(-P_max))^K, labelled `APPROX_UNCALIBRATED` and shown. It assumes independent exponential ordinates, which discrete, gappy series do not strictly satisfy.
  - **N1 FAP:** the simulated distribution of P_max on the same grid and draw set, labelled `N1_CALIBRATED`, with the Monte Carlo interval.
  - PB channel: z_t = (b_t - 0.05)/sqrt(0.0475).
- **Edge cases:** n < 30 gives `LOW_N`; fewer than 3 scored targets gives `MR_INSUFFICIENT_DATA`.
- **Ranking:** P_max descending (descriptive); Z_plus from the best available FAP (significance).
- **Outputs:** P_max, the best period 1/f, the top 3 periods with their power, both FAPs, Z_plus, labels.

### MR16 - Hit-rate estimate with exact interval

- **One line:** how often this track achieved a given kind of success, how uncertain that rate is, and how big an advantage this sample could even detect.
- **Short explanation:** a success here is a yes/no event per draw, such as any prize division, a particular division, at least 2, 3 or 4 main matches, or a Powerball hit. MR16 shows the track's observed rate with an exact 95% interval and the fair-draw rate beside it. It also shows the smallest advantage that could reach 3 sigma over this window, and the chance of reaching 3 sigma if the method were truly 1.5x or 2x better. With a few hundred draws the intervals are wide, and seeing that plainly prevents striking-looking counts being over-read. It vetoes nothing.
- **Sub-measures:**
  - `MR16.ANYDIV`;
  - `MR16.PDd` / `MR16.ODd`, every division;
  - `MR16.M2`, `MR16.M3`, `MR16.M4` (at least 2, 3, 4 main matches);
  - `MR16.PB` (Powerball only).
- **Definition** (per sub-measure, per `READOUT_TRACK`, on C):
  - k = the draws with the success event; observed rate k/n; fair rate p (exact, from section 4).
  - **Interval:** the Clopper-Pearson 95% interval for a constant rate. It is exact for a constant rate and conservative-approximate for a rate that varies over the window (labelled).
  - **Local significance:** P_up = P(X >= k), X ~ Binomial(n, p), giving `EXACT_LOCAL`. This is the same tail as MR4 for division events, and it is not counted twice in M.
  - **Detectable-effect line:**
    - k_3 = the smallest k with P(X >= k) <= 0.00134990 (3 sigma);
    - the detectable ratio is k_3 / (n x p);
    - the power at 1.5x and 2x is P(X >= k_3) for X ~ Binomial(n, min(1, c x p)), with c = 1.5 and 2.
- **Reference values** for the default windows (computed exactly):

| Event | n | Expected by chance | k_3 (ratio) | Power at 1.5x / 2x |
|---|---|---|---|---|
| Powerball, any division | 291 | 6.6 | 16 (2.42x) | 0.04 / 0.25 |
| Powerball, 3+ main | 291 | 36.3 | 55 (1.51x) | 0.49 / 0.99 |
| Powerball hit | 291 | 14.6 | 28 (1.92x) | 0.11 / 0.61 |
| Oz Lotto, any division | 220 | 4.4 | 13 (2.97x) | 0.02 / 0.10 |
| Oz Lotto, 3+ main | 220 | 12.5 | 25 (2.01x) | 0.08 / 0.52 |

- **Ranking:** the lower interval bound descending (descriptive: the rate the data most surely supports); Z_plus (significance).
- **Edge cases:** k = 0 gives an interval lower bound of 0 and 0 excess sigma. n = 0 gives `MR_INSUFFICIENT_DATA`.
- **Outputs:** k, n, the rate, the interval, p, n x p, P_up, Z_plus, k_3, the ratio, the two power values.

---

## 7. In-sample diagnostic mode (IS)

**7.1 Purpose.** To see how each method's fully trained state fares over the window. The owner knowingly accepts the bias: the window's draws are part of the training data. IS answers "how well does the method describe the draws it has seen", never "how well does it predict".

**7.2 Procedure** (per game, method, variant; window [S, L]):

1. **Full fit** on F = H(L + 1), the eligible draws E(G)..L. It reads no draw after L.
   - Record the frozen parameter digest, the master version and SHA, and the environment.
   - In Phase 1 the fit never touches quarantined draws.
2. **Apply:** for each target N in [S, L] ascending, produce the entry from the frozen parameters plus, where used, the recent-state inputs from H(N) only.
3. **Score** against draw N (section 4).

**7.3 Capability** (declared in the method-generic contract, section 13):
- `IS_STATIC`: one fixed entry scored against every target (for example E_1's raw counts).
- `IS_STATEFUL`: fixed parameters, with state from before N.
- `IS_NOT_APPLICABLE`: the method appears in WF tables only.

Declaring a capability authorises nothing, and does not require all methods to implement IS.

**7.4 Firewall and labelling:**
- Product label `IN_SAMPLE_DIAGNOSTIC`; evidence tier `IS_DESCRIPTIVE`.
- Every IS page carries: "IN-SAMPLE DIAGNOSTIC - the scored draws were part of the training data; this is NOT evidence of prediction."
- **All IS numbers are calculated and shown (MRD-21)**, including sigma, p-values and Bayes factors. Every significance figure is labelled `IS_NOT_CALIBRATED`, because fitting on these outcomes means fair-draw tails no longer apply.
  - The label may be applied once per IS table rather than repeated on every figure; the owner's choice of presentation.
  - An unusually high IS figure is kept as an observation worth checking on genuinely new data. It is never a calibrated finding.
- N1 is not used to calibrate IS. A whole-pipeline null (refitting on simulated histories) is a possible later design (MRO-10).
- IS records never enter the R3 scientific score ledger or the result allowlist, are never counted as WF, holdout or prospective evidence, and are never used by any method or meta-method.
- **IS and WF tracks never compete in one ranking.** They are shown side by side (7.5).
- After holdout draws are opened and scored, IS windows may include them, and the report states that they are in-sample for IS.

**7.5 Side-by-side display (MRD-23).** For every measure and sub-measure applicable in both modes, the report includes a side-by-side table on the same window and comparison set.

| Columns | Content |
|---|---|
| Unit | method / variant / readout, or the measure's analysis unit (3.4A) |
| Walk-forward (earlier draws only) | the WF value and its WF rank (among WF units only) |
| In-sample (hindsight: all draws) | the IS value and its IS rank (among IS units only), labelled `IS_NOT_CALIBRATED` where it is a significance figure |
| In-sample minus walk-forward (hindsight advantage) | IS minus WF; descriptive |

- Rows are sorted by WF rank by default; sorting by IS rank is a report option.
- A unit without IS capability shows "IS not applicable" in its IS cells and stays in the table by its WF values.
- Ranks are computed separately per mode, so an IS value never displaces a WF rank, or the reverse.
- The difference is an overfitting gauge, never an unbiased estimate of out-of-sample performance.
- It is reported for every applicable measure. Fair-draw simulation shows that even E_1 typically gains about 3 sigma in-sample by chance alone, so the difference column is the meaningful reading.

---

## 8. Supplementary-number rule change (MRD-03)

**Current ratified text:** in R2, Architecture section 0 and the Proposal: "Three supplementary Oz Lotto labels are provenance only and never become scientific inputs"; supplementaries are "excluded from every method view/scorer".

**Replacement rule:**
- The Oz Lotto supplementary numbers of a **target** draw may be read **by the evaluator only**, after (a) the target's outcome is opened and (b) the track's frozen forecast for that target exists.
- They are used solely to compute `supplementary_matches` and the prize division.
- They remain excluded from every method view, fit, seed, view digest, readout and forecast.
- Methods never forecast supplementaries.
- The main and Powerball match channels are unchanged, and Oz Lotto has no Powerball channel (`ABSENT`).
- The master already stores `Supp_1..Supp_3`, so there is no data change.

**Scope confirmed by the owner:** scoring and measuring only, never predicting. Using supplementaries as method inputs would be a separate scientific decision, outside this proposal.

---

## 9. Use of rankings (MRD-05; rules decided by Claude)

- **RK-1:** rankings are **reports**. They never alter any frozen forecast, fit, configuration, variant roster, readout or FINAL batch.
- **RK-2:** rankings are not scientific results, never go on the result-consumer allowlist, and are never read by a method.
- **RK-3:** any rule using rankings to **choose, weight or switch** methods is a **meta-method**. It must:
  - be registered (an E_55/E_56 variant if it fits, otherwise E_63+ by owner decision);
  - obey strict N-1, using only WF scores of targets < N known before N's freeze;
  - use **WF only, never IS**;
  - predeclare its measure, window, tie rule and minimum history;
  - be scored and ranked like any method.
- **RK-4:** any report highlighting a top-ranked track shows the number of tracks and tests compared and the global figures (5.3), plus the search-log count.
- **RK-5:** the owner studying development rankings and then changing a method is permitted design influence on development data. Each change creates a new versioned variant and is recorded in the method change log. Development rankings never extend into quarantined draws.
- **RK-6:** rankings over FINAL_HOLDOUT_10 are produced only after Mode H scoring of those targets.

---

## 10. Reporting (MRD-09)

**10.1 Files** (create-only, `os.rename` on Windows; in `results/method_rankings/<GAME>/`):
- `ranking_<GAME>_<MODE>_<S>-<L>_<UTCSTAMP>.txt`: human-readable and complete;
- `.csv`: one row per (track, sub-measure);
- `.json`: the run manifest and reproducibility receipt.

`<GAME>` is `POWERBALL` or `OZLOTTO`; `<MODE>` is `WF` or `IS`; `<UTCSTAMP>` is `YYYYMMDDTHHMMSSZ`. Example: `ranking_POWERBALL_WF_1286-1576_20261026T040000Z.txt`.

**10.2 Text report layout:**
1. **Header:**
   - game; mode, by display name with its plain meaning from 3.5A (plus the IS banner); evidence tier; window;
   - the cohort and its digest, or `EXPLORATORY_COHORT`, and the family IDs;
   - comparison-set size n, and track counts by status;
   - master version and SHA; tool version and SHA; the N1 seed and R; the environment;
   - the search-log row number.
2. **Glossary:** first, the plain meanings of the two modes, word for word from 3.5A; then every measure, sub-measure, status, label, mode and tier used, each with ID, name, one-liner and short explanation; then the four pattern origins PO-1..PO-4.
3. **Fair-draw reference:** the division tables, expected counts for this n, the sigma table and caution, and the calibration-label legend.
4. **League tables:** descriptive and significance tables per measure and sub-measure, per mode; plus the **side-by-side WF/IS tables** (7.5). Each row gives rank, track ID, **method ID, name and one-liner**, readout, variant, n, all outputs, and calibration labels.
5. **Per-track detail.**
6. **Notes:** M per family; Bonferroni and N1 resolution; `LOW_N`; undefined values; ties; exclusions by status.

**10.3 Methods in reports** carry their E-number, name and one-liner in tables, and their short explanation in the glossary. The method registry therefore holds these texts (section 13).

**10.4 Ties:** standard competition ranking ("1=, 1=, 3"), listed by track ID within a tie. Exact quantities are compared exactly; floats at full float64 equality. `TIE_SHA256_V1` is not used.

**10.5 Number display:**
- counts as integers;
- probabilities to 6 significant digits in scientific notation;
- confidence rounded down, never "100%";
- sigma to 2 decimals;
- bits to 3 decimals;
- log10 Bayes factors to 3 decimals.

---

## 11. Numerics and precision

- `int64` throughout, with Python `int` for combinatorial counts; `float64` for floats. No narrowing.
- Division probabilities are exact `Fraction`s.
- **Tails in production:** log-space summation of exact log-pmf terms (via lgamma), summing whichever side is shorter, with the sigma conversion taken from log-survival or the inverse survival function. Never compute Phi_inv(1 - P) by forming 1 - P.
- **Exact oracle:** `Fraction` tails and integer polynomial coefficients (MR7) serve as the test oracle over the actual domain, including tails below 1e-300 (MRT-04).
- **Sigma accuracy:** within 1e-6 against the oracle where the oracle is computable, with documented asymptotics beyond that, labelled.
- MR13 quadrature is in log space, tested against closed-form cases.
- Timing is not committed until benchmarked on synthetic fixtures (ChatGPT O8).

---

## 12. Execution model (independent of production; MRD-13)

- **WF rankings:** a standalone **report tool** reads stored frozen forecasts, opened outcomes, the registries and the search log. It runs no method code. It includes N1. It is run whenever the owner chooses, never inside the FINAL batch.
- **IS runs** are method runs through the existing single launch interface (`Run_Experiment.bat`, optionally coordinated), with a declared mode `in-sample-diagnostic`, writing to a separate IS namespace.
- **Wrapper:** `Run_Method_Rankings.bat` follows the ratified wrapper rules (venv checks, `SETLOCAL`/`ENDLOCAL`, explicit `.venv` Python, `%*`). Like `Run_Results_Updater.bat`, it is a tool launcher, recorded in the Architecture.
- **Evaluator rules:** outcomes are read only for opened targets that have frozen forecasts; supplementaries only under section 8.
- Dependency rules are unchanged: no upgrade between freeze and score, or within Mode H.

---

## 13. Phasing - when to code it

| Stage | When | What |
|---|---|---|
| 0 | Now | ChatGPT spot-check of this v0.3; owner ratification; integration into the governing documents (section 15). No code. Package 2 v0.11 proceeds unchanged in parallel. |
| 1 | The **method-generic contract** package required before E_2 (Architecture 20A), after v0.11 is accepted. Proposed name: "E_2 readiness". **Not** in v0.11; P3 v0.2 is not edited. | The contract-field schema, ratified by the owner first (fields 1-7 below). |
| 2 | With the R3 **scorer** and E_1's authorised development walk-forward | Match records; divisions (with section 8); MR0, MR1/MR1-T, MR4, MR5, **MR7**, **MR16**; analysis units; the report format and glossary; sigma and labels; Bonferroni; families and the search log; **N1**. Tests MRT-01..10, 12..14, 16..19, 21..23. |
| 3 | After E_2-E_6 walk-forward results are scored | MR2, MR3, MR6, MR8, MR9, MR10/MR10.BOTTOM, MR11-MR15; IS mode; multi-method tables; the side-by-side WF/IS tables (7.5). Remaining tests. |
| 4 | Later | Any registered meta-method (RK-3), separately reviewed. |

**Stage-1 contract fields** (adopted from ChatGPT's section E):
1. `game_id`; method and variant IDs and version; the immutable schema ID; era and profile version; registry status (`SUPPORTED` / `FORMULA_OPEN` / `UNSUPPORTED_FOR_GAME`) with its reason; the method **name, one-liner and short explanation**, with per-version provenance.
2. TOP and WORST readout status recorded **independently**; `INVERSE_UNAVAILABLE` is never manufactured. The frozen ticket; the main ranking and per-label scores; the Powerball ranking and scores where applicable; the `TIE_SHA256_V1` identity and digest.
3. **Per-channel probability capability:**
   - `main_probability_kind`: `NONE`, `NORMALIZED_LABEL_PROBABILITY` (length N, values in [0,1], sum 1) or `MARGINAL_INCLUSION_PROBABILITY` (length N, values in [0,1], sum 7).
   - `powerball_probability_kind`: `NONE` or `PB_CATEGORICAL` (length 20, sum 1); `ABSENT` for Oz Lotto.
   - Normalisation tolerance is stated per kind (for example an absolute error of at most 1e-12 on the sum).
   - Never inferred from arbitrary scores or from a theoretical claim. A method may declare both channels.
   - Recorded per channel: the vector order, float64 representation, smoothing and calibration notes, provenance and a digest.
4. `IS_capability`: `IS_STATIC`, `IS_STATEFUL` or `IS_NOT_APPLICABLE`, with a versioned future fit/apply interface where genuinely supported. Declaring a capability authorises nothing.
5. Separate `product_kind`, `run_mode`, `score_status`, evidence tier and forecast-freeze receipt. WF and IS are not readout variants. IS cannot enter the R3 ledger. The allowlist stays strict and empty until authorised.
6. Per track: the canonical pre-target forecast identity; the target `(game_id, draw_number)`; master and ledger provenance; a view digest excluding post-target content; the environment identity; the window and cohort; the status captured before the outcome is opened. The master SHA is provenance only.
7. A scorer-only post-outcome record: drawn main set, Powerball where applicable, Oz supplementary matches and division. Never fed to a predictor. Quarantine opening is separately gated.

**Acceptance before E_2:**
- shape and numeric contracts;
- profile separation between games;
- prefix-only view and digest independence (T-05);
- R3 tie and WORST consistency;
- no Powerball or supplementaries in Oz predictor views;
- the mode firewall;
- not-applicable behaviour per capability;
- extension points without early implementation of ranking or IS;
- a schema versioning and migration rule.

---

## 14. Tests

| ID | Test |
|---|---|
| MRT-01 | Division tables equal the exact fractions and integer counts in section 4. Published rounded odds agree (Powerball rule 9.4; Lotterywest Oz odds, rounded up). |
| MRT-02 | Classification is exhaustive and exclusive over every (m, b) and valid (m, s). Invalid s > 7 - m is rejected. |
| MRT-03 | The sigma conversion reproduces section 5's table to 1e-6. k = 0 gives 0 excess sigma. The deficit example (P_lo 0.0111058, 2.28673 sigma) is reproduced. Displayed confidence is never "100%". |
| MRT-04 | Production log-space tails agree with the exact `Fraction` oracle, including n up to 5000, p down to 1e-9, and tails below 1e-300. |
| MRT-05 | Isolation: no outcome read beyond L or before opening. Supplementaries are read only by the evaluator for scored targets. No method view contains supplementaries (static and runtime checks). |
| MRT-06 | IS firewall: refused by the scientific ledger and allowlist; the banner and `IS_NOT_CALIBRATED` present; no ranking mixes IS and WF units as competitors; side-by-side tables keep separate per-mode rank columns and do not change either mode's ranks; N1 refuses IS input. |
| MRT-07 | Planted, **measure-specific** synthetic effects are detected: a hit-rate tilt (MR4, MR7, MR11, MR12, MR13), a cycle (MR15), a streak (MR8), drift (MR9), probability vectors (MR6, MR14), top or bottom placement (MR10, MR10.BOTTOM). Null synthetic tracks give near-nominal rejection rates. Synthetic data stays firewalled. |
| MRT-08 | Determinism: identical inputs and seed give byte-identical CSV, and text identical apart from header timestamps. |
| MRT-09 | Tie display (10.4). |
| MRT-10 | MR5 per-target values equal R3's evaluator values. |
| MRT-11 | MR14's K-parameterised E_t and V_t agree with exhaustive enumeration on small domains ((N, K) = (10,3), (12,7), (9,4)) to 1e-12, with an independent analytic check, and with seeded simulation at (35,7) and (47,7). Uniform q gives `NULL_VARIANCE_ZERO`. The residual guard behaves as specified. |
| MRT-12 | All numeric fields are int64 or float64. |
| MRT-13 | Every printed ID has registry text, and the two mode definitions of 3.5A appear word for word in the glossary. No heading shows a bare `WF` or `IS`. The report fails otherwise. |
| MRT-14 | Window guard: S >= E(G); L within the cap; Oz S < 1474 rejected. |
| MRT-15 | (Stage 4) A meta-method uses only WF scores of targets < N. |
| MRT-16 | N1 classes. (a) For the hit-sequence class, N1 matches the exact distributions of MR4, MR7, MR8 and MR11 within Monte Carlo error, **including for adaptive synthetic methods**. (b) ChatGPT's adaptive 4-draw counterexample is reproduced (true 1/16, replay 15/128), and the cross-track maximum is labelled `N1_FIXED_FORECAST_REFERENCE`, never `N1_CALIBRATED`. (c) A forecast-weighted adaptive toy confirms that weight- and probability-scored measures are labelled reference. Seed reproducibility. |
| MRT-17 | Families: registration precedes first use (checked against the search log); M is computed correctly; post-hoc families are labelled `POST_HOC_FAMILY`. |
| MRT-18 | The search log is append-only; every report run adds exactly one row. |
| MRT-19 | MR7's exact integer-coefficient oracle agrees with the production computation and with N1. |
| MRT-20 | MR8's dynamic programme agrees with brute-force enumeration on short gappy sequences. |
| MRT-21 | MR15: the frequency grid excludes Nyquist; the power normalisation matches its definition; the N1 FAP is computed on the actual draw grid. |
| MRT-22 | MR16: the Clopper-Pearson intervals match an independent exact implementation. k_3 and the power values for the section 6 reference table are reproduced. Division-event tails are not double-counted with MR4 in M. |
| MRT-23 | Analysis units: each measure is computed on its declared unit (3.4A). No method-level value appears as two readout tests. M counts distinct hypotheses once. |
| MRT-24 | MR6 zeros: an observed q_j = 0 gives `LOG_SCORE_NEG_INFINITY`, a tagged value and last place; an unobserved zero gives `MR_UNDEFINED_REFERENCE` for that target's significance only; the evaluator never smooths. |

---

## 15. Integration into the governing documents on ratification

New clean editions, no addenda:

| Document | Integration |
|---|---|
| R3 v0.4 -> v0.5 | Largest change. A new section for the method ranking measures: sections 3.4-3.9, 4, 5 (including 5A, 5B), 6, 9 and 10; division scoring for both games, using Oz supplementaries for division classification only; evidence tiers and pattern origins. |
| R2 v0.4 -> v0.5 | The supplementary rule (section 8) replacing the "structural checks only" text; the IS mode and firewall (section 7); the stage-1 contract fields and typed probability semantics; the numbering conventions (3.2). |
| Architecture v0.7 -> v0.8 | Section 0's supplementary sentence; the report tool and wrapper; the IS run mode via `Run_Experiment.bat`; N1 as an evaluator component; 20A contract fields. **Section 5C untouched.** |
| Proposal v0.5 -> v0.6 | The same supplementary sentence (sections 0 and 3.1); a charter note on rankings, IS diagnostics, "mark, never suppress" and statistics as instrument, not gate; the explanation-text rule. |
| Next task spec ("E_2 readiness") | Stage-1 fields; later, the stage 2-3 tasks. **P3 v0.2 is not edited.** |
| Ratification register v0.3 -> v0.4 | New entries and hashes. |
| HOLDOUT_EXPOSURE_RECORD v0.1 -> v0.2 | Item 6 (MRD-20); drafted separately and ratifiable now. |
| Unchanged | R1 v0.4, TIE v0.2, the E_1 legacy schema and goldens, the masters, the owner tools, the coordinator, Package 2 v0.11. |
| Handovers | After ratification, a short update (Claude v9 addendum or v10; a coder handover note) points to the new editions. |

---

## 16. Open items

| ID | Item | Status |
|---|---|---|
| MRO-01 | Scope of the supplementary rule | RESOLVED: scoring and measuring only (MRD-03). |
| MRO-02 | Keep MR1-T | RESOLVED: keep (MRD-14). |
| MRO-03 | Reserved measures MR6-MR10 | RESOLVED: filled by ChatGPT's measures (MRD-16). Further measures take MR16 onward. |
| MRO-04 | MR13 prior scale | RESOLVED: 0.5, with 0.25 and 1.0 sensitivity (MRD-19). |
| MRO-05 | LOW_N threshold | RESOLVED: n < 30 (MRD-19). |
| MRO-06 | Identity for any future meta-method | OPEN; decided when one is proposed. |
| MRO-07 | Oz Lotto supplementary channel for MR6-MR15 | RESOLVED: main only (MRD-19). |
| MRO-08 | Multiplicity families | RESOLVED: predeclared families, Bonferroni, N1 maximum statistic, search log (MRD-18). |
| MRO-09 | Expected-payout measure (ChatGPT O1) | DEFERRED: only with legally sourced, versioned payout data. |
| MRO-10 | Full recursive (whole-pipeline) null simulator: refits methods inside each replicate, which would calibrate cross-track maxima and weight- or probability-scored measures for adaptive WF, and IS significance | DEFERRED: separate reviewed design if ever wanted; it requires running method code. |
| MRO-11 | Larger N1 R for higher-resolution global figures | OPEN: owner may raise R per table; cost to be benchmarked. |

---

## 17. Traceability

### 17.1 To the owner's starter text

| Starter item | Where addressed |
|---|---|
| Draws 1 to P0 / O0; first draw in 2021 is P1 / O1 | 3.6 (S defaults: Powerball 1286; Oz Lotto 1474 under MRD-04; L at the cap) |
| Step 1, full training, bias acknowledged | Section 7 (IS), MRD-21 |
| Step 2 window with default parameters | 3.6; ascending draw-number order (MRD-12) |
| 2.1 fully trained prediction | 7.2-7.3 |
| 2.2 methods where full training does not apply | 7.3 `IS_NOT_APPLICABLE`: WF tables only |
| 2.3 collect matches | 4.1 |
| Step 3, rankings per game | Sections 6 and 10 |
| Division rules, top-down | 4.2-4.3 (all divisions, MRD-02) |
| R0 | MR0 |
| R1 (90/7/3) | MR1-T; MR1 |
| R2-R4 | MR2 per division |
| R5-R7 | MR3 per division |
| R8-R10 | MR4.C.3, MR4.B.2-3, MR4.X.3 |
| Output file with numbers | Section 10 |
| Up to 5 further measures | MR11-MR15 (Claude); MR6-MR10 (ChatGPT) |
| Run independently of production | Section 12 |
| Architecture impact | Sections 12, 13, 15, 18 |

### 17.2 To ChatGPT's review

| Finding | Where applied |
|---|---|
| B1 (agreed as CORRECTION) | 5.2 `IS_NOT_CALIBRATED`; 7.4; MRD-21 |
| B2 | 5.3, 5A, 5B; MRD-18 |
| B3 | MR15; 5A |
| B4 | 3.8; MR2; MR3 |
| C1 | MRD-06; 5.1 |
| C2 | Section 11; MRT-04 |
| C3 | MR13 PB channel |
| C4 | MR6/MR14 applicability; MR14 exact moments; section 13 field 3 |
| C5 | MRT-07; MRT-11 |
| C6 | 3.7 |
| C7 | MR0; MR1; MR2; MR3 |
| C8 | 3.5; 3.9 |
| C9 | Section 2 (MRD-19); section 16 |
| C10 | 4.2-4.3 rounding; 5.1 confidence; 5B channels; 3.7 LOW_N |
| O1 | MRO-09 |
| O2 | MR14 |
| O3 | Section 18.9 |
| O4 | 3.4 |
| O5 | 10.1-10.2 receipt; 5B |
| O6 | Section 6 (descriptive vs significance tables); RK-3 |
| O7 | MR1 |
| O8 | Section 11 |
| Contract fields | Section 13 |

### 17.3 To ChatGPT's spot-check of v0.3

| Finding | Where applied |
|---|---|
| B1 (N1 claim; agreed, with the hit-sequence refinement) | 5.2, 5.3, 5A, 3.9 PO-1, 18.4; MRT-16 |
| C1 | 5.2, 5.3 |
| C2 | Section 13 field 3; MR6 applicability |
| C3 | 3.4A; 5B; MRT-23 |
| C4 | MR6 edge cases; MRT-24 |
| C5 | MR14 exact moments; MRT-11 |
| O1 | 5.3; 5A Monte Carlo contract |
| O2 | MR3 label |
| O3 | No change |

---

## 18. Claude's analysis, implications and design matters

**18.1 Feasibility.**
- WF ranking re-reads stored forecasts and outcomes and computes; no method runs.
- N1 adds R replicates of cheap scoring per calibrated table.
- IS adds one full fit plus applications per method.
- The expensive part, walk-forward forecasting, is already planned.
- No timing is committed until benchmarked.

**18.2 Why all divisions matter.** Expected division wins under a fair draw, per track and across 124 tracks (62 methods x TOP/WORST), for the default Phase 1 windows:

| Division | Powerball, n = 291, per track | Powerball, 124 tracks | Division | Oz Lotto, n = 220, per track | Oz Lotto, 124 tracks |
|---|---|---|---|---|---|
| PD1 | 0.0000022 | 0.00027 | OD1 | 0.0000035 | 0.00043 |
| PD2 | 0.000041 | 0.0051 | OD2 | 0.000073 | 0.0091 |
| PD3 | 0.00042 | 0.053 | OD3 | 0.00091 | 0.11 |
| PD4 | 0.0081 | 1.0 | OD4 | 0.0084 | 1.0 |
| PD5 | 0.017 | 2.1 | OD5 | 0.049 | 6.1 |
| PD6 | 0.25 | 31 | OD6 | 1.2 | 150 |
| PD7 | 0.33 | 40 | OD7 | 3.1 | 385 |
| PD8 | 1.6 | 192 | | | |
| PD9 | 4.5 | 554 | | | |

- Top divisions are essentially never expected. One PD3 win in 291 draws is about 3.34 local sigma, which is why global figures and the search log matter.
- The lower divisions, and the every-draw measures (MR5-MR15, especially MR7), give the tables their resolving power.

**18.3 In-sample results.**
- A static method's IS entry is chosen with the outcomes in view, so its matches are inflated by construction.
- IS measures descriptive fit. Its main use is the side-by-side IS/WF comparison and its "in-sample optimism" column (7.5). A one-off fair-draw simulation by Claude (20,000 runs, not part of the design) found that E_1's in-sample TOP averages about 13% more main matches than chance, typically about 3.3 sigma, with 3 sigma or more in about 67% of runs, from fitting alone. Reading the optimism column:
  - large optimism with no WF advantage suggests fitting noise;
  - agreement suggests stability.
- The owner knowingly accepts this, and every number is shown, labelled.

**18.4 Multiple comparisons.**
- About 124 tracks and about 20 sub-measures make roughly 2,500 tests per family. Under a fair draw, about 3 local results at or above 3 sigma are expected by chance, and a local 5 sigma about 0.0007 times.
- Bonferroni over exact local p-values gives the guaranteed figure. This holds under adaptive walk-forward for the hit-sequence class, which includes the strongest every-draw measures (MR7, MR16, MR11).
- N1 is exact for single-track hit-sequence statistics. For cross-track maxima and probability- or weight-scored measures it is a labelled reference only, because replaying fixed adaptive forecasts breaks their dependence on earlier outcomes.
- The search log keeps honest count of all exploration.
- **Small samples:** MR16's detectable-effect line shows, per event, what advantage this window could even reveal. Frequent events (3+ matches) can show about a 1.5x advantage; division counts need about 2.4-3x.

**18.5 "Due" measures and the ruler.** Under a fair draw, wins have no memory. MR3 is shown as a pattern indicator, never a veto. Its value as a choosing rule can be tested only as a registered meta-method (RK-3).

**18.6 Selecting the best performer.** The top of a league table is partly luck, so its next results usually regress towards the mean. That is why any "follow the leader" rule is scored prospectively as its own method, and why reports show global figures.

**18.7 Design implications (summary).**
1. Package 2 v0.11 and P3 v0.2: no change.
2. Method-generic contract before E_2: the stage-1 fields. This is the one design item that matters now.
3. Rule changes on ratification: the evaluator-only supplementary rule; the R3 ranking section; the IS product and firewall; the explanation-text rule; the numbering conventions; evidence tiers.
4. New components: the report tool and wrapper; the IS run mode; N1 (two classes); the measure and family registries; the search log; method registry texts; analysis-unit keys.
5. No impact on Architecture 5C, the switches, the holdout boundaries, the E_1 goldens or the master data.

**18.8 Holdout and Mode H.** Phase 1 windows and IS fits end at 1576 / 1693. Holdout targets enter rankings only after Mode H scoring (RK-6).

**18.9 Philosophy compliance.**
- No measure excludes, demotes or vetoes a method; every method stays registered and reported.
- Fair-draw figures are rulers beside every result.
- "Mark, never suppress" (MRD-21) means every number the owner wants is calculated and shown, with a plain label of how far it can be trusted.
- Statistics here sorts patterns into the four origins (PO-1..PO-4); it never decides which ideas may be explored. Being open to unconventional hypotheses and careful about numerical correctness are compatible, and this design needs both. If something unexpected does appear, the same rigour is what will let it stand.

*End of document.*
