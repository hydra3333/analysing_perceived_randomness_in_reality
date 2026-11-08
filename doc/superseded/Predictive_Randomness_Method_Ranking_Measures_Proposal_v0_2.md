# Predictive Randomness - Method Ranking Measures (league tables)

**Document:** Method Ranking Measures Proposal, version 0.2.

**Change from v0.1:** the owner settled open items MRO-01 (supplementary scope: scoring only) and MRO-02 (keep MR1-T). Both are now recorded as decisions (MRD-03 updated, MRD-14 added). Nothing else changed.

**Author:** Claude (independent reviewer), drafted at the project owner's request from the owner's speculative-discussion starter of 26 October 2026.

**Date:** 26 October 2026 (Adelaide).

**Status:** PROPOSAL - REVIEW CANDIDATE.
- It records the project owner's decisions of 26 October 2026 (section 2).
- It is **not ratified**, and it grants **no run, coding, data-access or holdout authority**.
- It changes nothing in Package 2 v0.11.
- On ratification, its content is to be **integrated into the governing documents** (section 15), not kept as a separate layer.

**Repository baseline:** `hydra3333/analysing_perceived_randomness_in_reality` at HEAD `6726963` (governing set ratified 26 October 2026).

**Holdout discipline:** this document contains no winning, Powerball or supplementary number of any draw. All figures in it are fair-draw reference calculations.

**ID prefixes used here:**

| Prefix | Meaning |
|---|---|
| `MR` | measures |
| `MRD` | owner decisions recorded here |
| `RK` | rules for using rankings |
| `MRT` | tests |
| `MRO` | open items |
| `PD1..PD9` | Powerball prize divisions |
| `OD1..OD7` | Oz Lotto prize divisions |

None of these collide with existing IDs: A-, D-, I-, R2-C, R2-D, T-, W-, O-, M-INV-, ERR-.

---

## 0. Scope in one paragraph

After the project has produced forecasts for many historical target draws, the owner wants to **rank the methods by how successful their forecasts would have been**, always separately for Powerball and Oz Lotto.
- The ranking runs **independently of production prediction runs**.
- It uses prize divisions and several further statistical measures.
- It prints every number used, with a plain explanation of what each measure means.

Two modes are defined:
- **Walk-forward (WF):** the honest mode. Each forecast used only draws before its target.
- **In-sample (IS):** a diagnostic the owner explicitly requested, knowing it is biased. Each method is trained once on all available draws, and that one fit is used to "predict" draws that were part of its training.

The two modes are never ranked together.

---

## 1. Purpose (the owner's intent, restated)

1. Measure, for each method and each of its readouts (TOP and WORST), how its forecasts would have fared against actual results over a window of past draws.
2. Express that success in several complementary ways:
   - prize divisions won;
   - how often and how regularly wins recur;
   - whether a further win looks "due";
   - how improbable the results are under a fair draw, on the familiar sigma scale;
   - several further statistical and quantum-inspired measures.
3. Produce league tables per game and per mode, saved to files that contain the rankings, the numbers behind them, and a plain-English explanation of every measure.
4. Keep the rankings as **reports**. They never alter forecasts. Any use of rankings to choose methods is itself a registered, honestly tested method (section 9).

---

## 2. Owner decisions recorded (26 October 2026)

These are the project owner's decisions, given in this conversation. They become binding governing text when this proposal is ratified and integrated.

| ID | Decision |
|---|---|
| MRD-01 | The league-table concept is accepted, with the corrections Claude listed ("points to fix"): in-sample bias labelled; modes never mixed in one ranking; Oz window within the current format; supplementaries; meta-method rule; housekeeping. |
| MRD-02 | Measure and report **all prize divisions** (Powerball 9, Oz Lotto 7), not only Divisions 1-3. The owner is unconcerned by very small numbers; full-width integers and floats were chosen for this reason. |
| MRD-03 | **Change the ratified rule so that supplementary numbers are included** in scoring. Oz Lotto Divisions 2, 4 and 7 depend on them, and they are already read and stored in the Oz Lotto master. **Scope confirmed by the owner: scoring and measuring only, never predicting.** Apart from Powerball's separate barrel, a prediction is only a set of numbers; no number is designated in advance as a supplementary (section 8). |
| MRD-04 | Use **current-format draws only** (Proposal section 3.1). The Oz Lotto window never starts before draw 1474 (17 May 2022). |
| MRD-05 | Rankings never feed forecasts. The owner delegated to Claude the exact rule for any use of rankings to choose methods (section 9). |
| MRD-06 | Significance is reported on the **sigma scale used in public reporting of scientific results** (1 sigma to 6 sigma). **Zero wins is 0 sigma.** |
| MRD-07 | Housekeeping accepted: measure IDs `MR..`; weight typo corrected; processing in draw-number order; UTC timestamps in file names; the window never extends past opened and scored draws. |
| MRD-08 | Claude's additional measures (MR11-MR15) are accepted. |
| MRD-09 | **Reporting rule:** every measure, and equally every prediction method, variant, status and mode, is reported with its **ID, name, one-line summary and a short explanation**, so that its meaning is never lost from a report. |
| MRD-10 | The forecast for target draw N is trained on the current-era draws from the era's first draw through **N-1 inclusive**. |
| MRD-11 | One numbering convention applies everywhere, as specified in section 3.2. It is consistent with conventions R2/R3 already use, which take precedence where they exist. |
| MRD-12 | The time axis is the **draw number** (already ratified). "Date order" in the starter text means ascending draw-number order. |
| MRD-13 | The ranking is run **independently** of production prediction runs, never inside the weekly FINAL batch (section 12). |
| MRD-14 | Keep **MR1-T**, the owner's original 90/7/3 weighting of Divisions 1-3, alongside the all-division score MR1. |

---

## 3. Conventions and definitions

### 3.1 Identity and time axis

- Every draw is identified by the pair `(game_id, draw_number)`; `game_id` is `POWERBALL` or `OZLOTTO`. Draw numbers are the operator's official draw numbers.
- **The draw number is the time axis.** Everything in this document is processed in ascending draw-number order. Dates are never used for ordering or arithmetic.
- Games are never pooled. Every table, statistic, file and ranking belongs to exactly one game.

### 3.2 Numbering conventions (the single "base" for everything)

There is no zero-based or one-based re-indexing of draws anywhere in this design. Wherever the existing R2/R3 rules already fix a convention, it is used unchanged; that is noted below.

| Quantity | Convention |
|---|---|
| Draws | Always referred to by their **official draw number** (for example Powerball 1286). Never by a position. |
| Ball labels | Their printed values: Powerball main 1-35, Powerball 1-20, Oz Lotto 1-47. (Existing R2/R3 convention.) |
| Rank positions | **1-based, 1 = best** (most favoured or highest scoring). This matches R3's mid-rank convention (1 = highest predicted). |
| Training set for target N | Era first draw through N-1 inclusive (see 3.3). |
| Gap between two draws a < b | **b - a** draw numbers; consecutive draws have gap 1. |
| "Draws since" a past draw a, counted at draw c | c - a. |
| Counts | Plain counts, starting at 0. |
| Internal array indices | Program internals may index from 0. Such indices **never** appear in records, files, file names or reports. |

### 3.3 Training set (walk-forward)

For game G with first current-era draw E(G) (Powerball 1144, Oz Lotto 1474), the training set for target N is:

    H(N) = { eligible draws d of game G with E(G) <= d <= N - 1 }

This is the ratified strict N-1 rule (R2), restated with the owner's wording: "0 to Pi-1 inclusive when predicting Pi", where "0" means the era's first draw.

### 3.4 Track and entry

- A **track** is one stream of forecasts identified by (game, method E_n, variant, readout, mode):
  - readout is `TOP` or `WORST` (R3);
  - mode is `WF` or `IS` (3.5).
- For each target draw, a track supplies one **entry**, the forecast in the shape of a lottery ticket:
  - Powerball: 7 distinct main numbers from 1-35, plus 1 Powerball from 1-20;
  - Oz Lotto: 7 distinct numbers from 1-47.
- Methods do not forecast supplementaries. The entry's 7 numbers are compared with the drawn supplementaries only to classify divisions (section 4).
- If a method's readout is unavailable for a target (for example `INVERSE_UNAVAILABLE`), that target is not scored for that track, and its status is counted (3.7).

### 3.5 Modes

- **WF (walk-forward):** the entry for target N comes from the method's frozen forecast record for N, fitted on H(N) (R2/R3 historical evaluation).
  - This is the only mode that is evidence of predictive performance.
  - The ranking tool **does not re-run methods** in WF mode. It reads stored frozen forecast records.
- **IS (in-sample diagnostic):** fully defined in section 7.
  - The method is fitted once on all eligible draws up to the window end L.
  - That single fit is applied to every target in the window.
  - Labelled `IN_SAMPLE_DIAGNOSTIC` and never evidence of prediction.

### 3.6 Window

- The window is W = [S, L], inclusive, in draw numbers, for one game. S and L are parameters, recorded in every output.
- **Default S:** the first current-era draw on or after 1 January 2021:
  - Powerball **1286** (2021-01-07; the master's date was checked);
  - Oz Lotto **1474** (2022-05-17, the first current-format draw).
- **Default L:** the latest draw allowed by the rules below.
- **Rules:**
  - S >= E(G).
  - L is never higher than the latest draw that is both (a) opened under the holdout rules and (b), for draws inside FINAL_HOLDOUT_10 or later, already scored from their frozen forecasts.
  - In Phase 1, therefore, L <= 1576 (Powerball) and L <= 1693 (Oz Lotto). The tool refuses any other value.
- **Default window sizes in Phase 1:** Powerball 1286-1576 is 291 draws; Oz Lotto 1474-1693 is 220 draws.
- **WF targets with too little history:** in WF mode, a method that needs more history than H(N) offers records `INSUFFICIENT_HISTORY` for those early targets (existing R2/R3 status). An example is Oz Lotto target 1474, which has no earlier current-era draw.

### 3.7 Scored set, comparison set and statuses

- For each track, the **scored set** is the targets in W whose readout status is `PREDICTION_AVAILABLE` (R3 vocabulary). Every other status is counted and reported per track, never silently dropped.
- A league table compares tracks on a **comparison set** C. By default, C is the intersection of the tracks' scored sets, so every track in the table is measured on exactly the same draws.
  - An alternative "own-set" table (each track on its own scored set) may be produced. It must be labelled `OWN_SET`, with n shown per row.
- n denotes the number of draws in the comparison set used for a measure.
- Measures that rely on approximations (marked "approx" in section 6) carry the flag `LOW_N` when n < 30. They are still computed and shown.

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
| `main_matches` (m) | int64, 0..7 | entry main numbers that equal a drawn main number |
| `powerball_match` (b) | int64, 0..1 | 1 if the entry's Powerball equals the drawn Powerball |
| `division` | int64, 0..9 | 0 = no division |

Oz Lotto record:

| Field | Type | Meaning |
|---|---|---|
| `game_id` | text | `OZLOTTO` |
| `draw_number` | int64 | target draw |
| `track_id` | text | see 3.4 |
| `mode` | text | `WF` or `IS` |
| `main_matches` (m) | int64, 0..7 | entry numbers equal to a drawn winning (main) number |
| `supplementary_matches` (s) | int64, 0..3 | entry numbers equal to a drawn supplementary; s <= 7 - m always |
| `division` | int64, 0..7 | 0 = no division |

The records are evaluator outputs. They are written only after the target's outcome is opened (section 8, RK rules).

### 4.2 Powerball divisions

Source: SA Lotteries Powerball game rules (March 2026), rule 9.4, in `doc/SAL_Powerball-Game-Rules_March-2026.pdf`. There are 9 divisions.

Classification is a function of (m, b), so each entry wins **at most one** division, always the highest one it qualifies for. The owner's "top-down parse" is therefore automatic.

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

Note that PD7 (5 main, no Powerball) is more likely than PD6 (4 main plus the Powerball). Division numbers are the operator's prize order, not probability order.

**Formula:**
- P(m) = C(7,m) x C(28,7-m) / C(35,7), where C(35,7) = 6,724,520;
- P(b = 1) = 1/20;
- m and b are independent.
- Any division: 611573/26898080, about 1 in 44.0 per entry.

### 4.3 Oz Lotto divisions

Source: Lotterywest's Oz Lotto game page; the 7-from-47 format with three supplementaries applies from draw 1474. There are 7 divisions.

Classification is a function of (m, s). Ten distinct numbers are drawn: 7 winning (main) and 3 supplementary.

| Division | Requirement | Exact probability per entry | About 1 in | Bits |
|---|---|---|---|---|
| OD1 | m = 7 | 1/62891499 | 62,891,499 | 25.906 |
| OD2 | m = 6, s = 1 | 7/20963833 | 2,994,833 | 21.514 |
| OD3 | m = 6, s = 0 | 259/62891499 | 242,824 | 17.890 |
| OD4 | m = 5, s >= 1 | 798/20963833 | 26,271 | 14.681 |
| OD5 | m = 5, s = 0 | 4662/20963833 | 4,497 | 12.135 |
| OD6 | m = 4 (any s) | 345800/62891499 | 182 | 7.507 |
| OD7 | m = 3, s >= 1 | 887075/62891499 | 70.9 | 6.148 |
| none (0) | every other (m, s) | | | 0 |

**Formula:**
- P(m, s) = C(7,m) x C(3,s) x C(37, 7-m-s) / C(47,7), where C(47,7) = 62,891,499 and 7-m-s >= 0.
- Any division: 416512/20963833, about 1 in 50.3 per entry.
- These match Lotterywest's published odds to within its rounding (test MRT-01).

### 4.4 Fair-draw moments used by several measures

| Quantity | Powerball | Oz Lotto |
|---|---|---|
| Mean main matches per entry | 7/5 = 1.4 | 49/47 = 1.04255 |
| Variance of main matches | 392/425 = 0.92235 (sd 0.96039) | 39200/50807 = 0.77155 (sd 0.87838) |
| Powerball match probability | 1/20 | (no Powerball) |
| P(main matches >= m), m = 0..7 | 1, 0.823922, 0.431748, 0.124830, 0.0182608, 0.00120975, 2.92958e-5, 1.48709e-7 | 1, 0.703560, 0.276337, 0.0566231, 0.00576327, 0.000264917, 4.46801e-6, 1.59004e-8 |

The main-match distribution is hypergeometric (draw 7 from 35, or from 47, with 7 "successes" in the entry).

---

## 5. The sigma convention (MRD-06)

Several measures produce a probability: how likely a result at least this favourable would be if the draws were fair and the method had no skill. This document reports that probability on the **sigma scale** familiar from public reporting of scientific results.

**Definitions:**
- **Upper-tail probability, P_up:** the fair-draw probability of a result at least as favourable as the one observed.
  - Example: for k wins in n draws with per-draw win probability p, P_up = P(X >= k), where X ~ Binomial(n, p). It is computed exactly (section 11).
- **Local excess sigma:** Z_plus = max(0, Phi_inv(1 - P_up)), where Phi_inv is the inverse of the standard normal cumulative distribution (one-sided).
  - If k = 0, then P_up = 1 and **Z_plus = 0** (MRD-06).
  - Any result at or below what chance typically gives also shows 0 sigma.
- **Confidence percentage:** 100 x (1 - P_up)%.
- **Sigma level:** the whole number of sigma, floor(Z_plus), shown as level 0, 1, 2, 3, 4 or 5, and ">= 6" at 6 or more.
- **Local deficit sigma:** Z_minus = max(0, Phi_inv(1 - P_lo)), where P_lo is the fair-draw probability of a result at least as **un**favourable as observed.
  - This is reported because a method whose WORST readout avoids the drawn numbers more than chance allows is also a pattern of interest.
  - Zero wins with a tiny expectation gives Z_minus = 0 as well.
- **Global sigma** (the look-elsewhere allowance):
  - With M tests in the same report table family, P_global = 1 - (1 - P_up)^M, computed as -expm1(M x log1p(-P_up)).
  - Z_plus_global = max(0, Phi_inv(1 - P_global)).
  - By default, M = the number of (track, sub-measure) pairs in the same table (see MRO-08).
  - This adjustment (Sidak) assumes independent tests. Methods are often correlated, so it is approximate. That is stated in every report.
- **Exact versus approximate:** where an exact tail is available it is used, with no continuity correction. Measures using a normal approximation are labelled "approx".

**Sigma reference** (one-sided, as used in physics reporting):

| Sigma | One-sided P_up | Confidence | Common description |
|---|---|---|---|
| 1 | 0.158655 | 84.13447% | |
| 2 | 0.0227501 | 97.72499% | |
| 3 | 0.00134990 | 99.86501% | "evidence" (physics usage) |
| 4 | 3.16712e-5 | 99.99683% | |
| 5 | 2.86652e-7 | 99.99997% | "discovery" (physics usage) |
| 6 | 9.86588e-10 | 99.9999999% | |

**Caution printed with every sigma table:** the physics thresholds assume one test declared in advance. A league table makes many comparisons at once, so read the **global** sigma when picking out the best of many.

---

## 6. Measure registry

Each measure below gives:
- its ID, name, **one-line summary** and **short explanation** (MRD-09);
- an exact definition;
- the ranking key;
- edge cases;
- its outputs.

The one-line summary and short explanation are stored with the measure definition, versioned (`MEASURE_REGISTRY_V1`), and printed in every report's glossary.

**Sub-measure notation:**
- `MRk.PDd` / `MRk.ODd`: measure k applied to Powerball / Oz Lotto division d.
- `MR4.X.d`: exactly division d.
- `MR4.C.d`: division d or better (divisions 1..d).
- `MR4.B.a-b`: band of divisions a..b.
- `.MAIN` and `.PB` denote the main-number and Powerball channels.

**Common notation:**
- n = draws in the comparison set.
- W_d = the track's count of division-d wins over those draws.
- p_d = fair-draw probability of division d (4.2, 4.3).
- b_d = -log2 p_d.
- L = window end.

**Measure IDs:**
- MR0-MR4 come from the owner's original R0-R10 (traceability in section 17).
- MR5 is R3's existing rank-position measure.
- **MR6-MR10 are reserved** for further measures proposed by ChatGPT or the owner.
- MR11-MR15 are Claude's additions.

### MR0 - Division win profile

- **One line:** who has won the best prizes, best division first.
- **Short explanation:** counts how many times the track's entries would have won each prize division. Tracks are ranked by their wins in the top division first, then the next division, and so on down. Under a fair draw, top-division wins are extremely rare (Powerball Division 1 is about 1 in 134 million per entry), so most tracks will share the same counts at the top; the lower divisions carry most of the information.
- **Definition:** the vector V = (W_1, W_2, ..., W_D), with D = 9 (Powerball) or 7 (Oz Lotto).
- **Ranking key:** V, descending and lexicographic; then MR1 descending; then shared rank (10.4).
- **Edge cases:** none; counts can be 0.
- **Outputs:** W_1..W_D, n, the expected counts n x p_d.

### MR1 - Surprisal-weighted division score (default); MR1-T - owner's top-division score

- **One line:** the average "rarity" of the prizes won per draw, in bits.
- **Short explanation:** each division win is worth the number of bits of surprise it represents under a fair draw. Rarer divisions are worth more: about 6.0 bits for Powerball Division 9, up to 27.0 bits for Division 1. MR1 is the average number of bits won per draw, shown next to what a fair draw would give. MR1-T keeps the owner's original weighting of the three top divisions only (Division 1 90%, Division 2 7%, Division 3 3%).
- **Definitions:**
  - MR1 = (1/n) x sum over draws of b(division), with b(0) = 0 and b(d) = b_d.
  - Fair-draw expectation per draw: E0 = sum_d p_d b_d, which is 0.153679 bits for Powerball (sd per draw 1.025914) and 0.131326 bits for Oz Lotto (sd 0.931722).
  - Report MR1, E0, MR1 - E0, and an approximate sigma: Z = (n x MR1 - n x E0) / (sqrt(n) x sd), converted with section 5's clamps.
  - MR1-T = (0.90 x W_1 + 0.07 x W_2 + 0.03 x W_3) / n. The starter text listed "D1_weight" twice; the third weight belongs to Division 3.
- **Ranking key:** MR1 descending; MR1-T descending in its own table.
- **Edge cases:** n = 0 gives no row.
- **Outputs:** MR1, E0, the difference, Z (approx), MR1-T.

### MR2 - Division recurrence period (per division)

- **One line:** how often, on average, this track wins division d.
- **Short explanation:** for a division the track has won at least twice, this is the average number of draws between successive wins. Shorter periods rank higher, with regularity shown alongside. Under a fair draw, the expected period is about 1/p_d draws (for example about 65 draws for Powerball Division 9), and wins arrive irregularly, so an unusually short or unusually regular period is noteworthy.
- **Definition** (per division d, per track):
  - Let N_1 < N_2 < ... < N_k be the draw numbers of the track's division-d wins, with k = W_d.
  - If k >= 2: gaps g_i = N_(i+1) - N_i (draw-number differences); mean period G_d = (N_k - N_1)/(k - 1).
  - Regularity CV_d = sample standard deviation of the gaps (denominator k - 2) divided by G_d. CV is defined only when k >= 3.
  - Fair-draw reference period: 1/p_d.
- **Ranking key:** tracks with G_d defined first, by G_d ascending, then CV_d ascending (defined before undefined), then k descending. Then tracks with k = 1, then k = 0, each sharing a rank.
- **Edge cases:** k <= 1 gives `PERIOD_UNDEFINED` (no division by zero). Because wins are on distinct draws, G_d > 0 whenever it is defined.
- **Outputs:** k, N_1, N_k, G_d, CV_d, 1/p_d, the gap list.
- **Owner traceability:** R2/R3/R4 = MR2.PD1/PD2/PD3 (and OD1/OD2/OD3). Extended to all divisions.

### MR3 - Division "due" alignment (per division)

- **One line:** is this track about due for another division-d win?
- **Short explanation:** compares the draws since the track's last division-d win, counted to the next draw after the window, with the track's average period from MR2. A value near 0 means the next draw falls close to the track's usual spacing. Under a fair draw, wins have no memory, so this is a pattern indicator only, never a reason to exclude a method. Using it to choose which method to play is itself a forecasting method and must be registered (section 9).
- **Definition** (per division d, per track):
  - Requires k >= 2.
  - since_d = (L + 1) - N_k, the "current draw" being the first draw after the window.
  - A_d = |since_d - G_d| / G_d.
- **Ranking key:** A_d ascending (most "due" first); undefined values last.
- **Edge cases:** k <= 1 gives `ALIGNMENT_UNDEFINED`. G_d > 0 when defined, so there is no division by zero.
- **Outputs:** since_d, G_d, A_d, and the signed difference since_d - G_d (negative = before the usual spacing).
- **Owner traceability:** R5/R6/R7 = MR3.PD1/PD2/PD3 (and Oz). Extended to all divisions.

### MR4 - Division sigma (excess wins)

- **One line:** how many sigma above fair-draw chance this track's division wins are.
- **Short explanation:** counts the track's wins in a chosen set of divisions and asks how likely at least that many wins would be under a fair draw over the same number of draws. That probability is shown as a percentage and on the sigma scale used in science reporting: 3 sigma is about 99.87%, which physicists call "evidence", and 5 sigma is about 99.99997%, "discovery". Zero wins is 0 sigma. The local sigma treats the track on its own; the global sigma allows for how many tracks and measures were compared.
- **Definition:**
  - For a division set S: p_S = sum of p_d over d in S (exact fraction); k_S = draws whose division is in S; X ~ Binomial(n, p_S).
  - P_up = P(X >= k_S) and P_lo = P(X <= k_S), both exact (section 11). Then apply section 5.
- **Sub-measures always produced:**
  - `MR4.X.d`, exactly division d, for every d;
  - `MR4.C.d`, division d or better, for every d;
  - the owner's original sets as named bands: `MR4.C.3` (owner R8: Divisions 1-3), `MR4.B.2-3` (owner R9: Divisions 2-3) and `MR4.X.3` (owner R10: Division 3).
- **Ranking key:** Z_plus descending; ties broken by k_S descending, then shared rank.
- **Edge cases:** k_S = 0 gives P_up = 1, which is 0 sigma (MRD-06).
- **Outputs:** k_S, n, the expected count n x p_S, P_up as a percentage, local Z_plus and its level, global Z_plus, local Z_minus.

### MR5 - Rank position (existing R3 measure)

- **One line:** where the method's ranking placed the numbers that were actually drawn.
- **Short explanation:** this is R3's ratified evaluator measure: the average mid-rank of the 7 drawn main numbers in the method's full frozen ranking (1 = most favoured), and the mid-rank of the drawn Powerball. Fair-draw expectations are 18.0 for Powerball main numbers, 10.5 for the Powerball and 24.0 for Oz Lotto. Lower means the method tended to favour numbers that came up. TOP and WORST come from one ranking, so this measure belongs to the method and variant, not to a single readout.
- **Definitions:**
  - Per target, `mean_rank_main` and `rank_powerball` as defined in R3.
  - MR5.MAIN = mean of `mean_rank_main` over the comparison set. MR5.PB = mean of `rank_powerball` (Powerball only).
  - **Sigma:** per target, given that target's frozen mid-rank vector r (35 or 47 values; ties already averaged), the fair-draw variance of the mean of 7 sampled labels is var_r x (N - 7) / (7 x (N - 1)), where var_r is the population variance of r and N = 35 or 47.
  - Z = (sum of expected - sum of observed) / sqrt(sum of variances). Approx. Positive Z means the drawn numbers were ranked better than chance.
  - Without ties, the per-target sd is 3.4641 (Powerball main) and 4.7809 (Oz Lotto).
- **Ranking key:** Z_plus descending.
- **Outputs:** MR5 mean, expected value, Z_plus, Z_minus.

### MR6 to MR10 - reserved

Reserved for further measures proposed by ChatGPT or the owner during review. Any addition must follow this section's format: one-liner, short explanation, exact definition, ranking key, edge cases, outputs, and a fair-draw reference.

### MR11 - TOP versus WORST contrast

- **One line:** does the method's TOP pick beat its own WORST pick?
- **Short explanation:** every method makes a TOP pick and a WORST pick from the same ranking, and the two never share a number. If the ranking carries real information, TOP should match more drawn numbers than WORST. If it carries inverted information, WORST will. Under a fair draw neither should win more often. This is the method's built-in control experiment.
- **Definition** (per method, variant and mode, over draws where both readouts are scored):
  - D_t = m_TOP,t - m_WORST,t.
  - Count n_plus (D_t > 0) and n_minus (D_t < 0); ties (D_t = 0) are excluded from the test.
  - Exact sign test: P_up = P(Y >= n_plus), P_lo = P(Y <= n_plus), with Y ~ Binomial(n_plus + n_minus, 1/2). Then section 5.
  - Descriptive: mean D.
  - Powerball also gets a separate channel, `MR11.PB`, with D_t = b_TOP,t - b_WORST,t.
- **Ranking key:** Z_plus descending. A separate list of Z_minus descending is headed "inverse-signal candidates".
- **Edge cases:** n_plus + n_minus = 0 gives 0 sigma both ways.
- **Outputs:** n_plus, n_minus, ties, mean D, P_up, Z_plus (local and global), Z_minus.

### MR12 - Information gain (Shannon surprisal)

- **One line:** how much more surprising, in bits, this track's matches were than chance.
- **Short explanation:** each draw's match count is scored by how surprising "at least this many matches" would be under a fair draw. Seven matches is about 22.7 bits; zero or more matches is 0 bits. The total is compared with what a fair draw gives on average. This is Claude Shannon's measure of information. It is also the everyday-world limit of the entropy used in quantum theory (von Neumann entropy reduces to it when quantum effects are absent). It ranks tracks even when no prize division was ever won.
- **Definition:**
  - MAIN channel: u_t = -log2 P0(M >= m_t), using 4.4's tail values; U = sum of u_t.
  - Fair-draw per-draw mean and sd:
    - Powerball main: 0.911756, sd 1.138676;
    - Oz Lotto main: 0.879151, sd 1.143974.
  - Z = (U - n x mean) / (sqrt(n) x sd), approx, then section 5.
  - PB channel (Powerball only): u_t = log2(20) = 4.321928 if b_t = 1, else 0; mean 0.216096, sd 0.941942.
- **Ranking key:** Z_plus descending, per channel.
- **Outputs:** U, the expected U, U - expected (bits), Z_plus, Z_minus.

### MR13 - Bayes factor against a fair draw

- **One line:** how strongly the evidence favours "this track has some skill" over "pure chance".
- **Short explanation:** compares two explanations of the track's match counts: a fair draw, and a fair draw tilted slightly in the track's favour by an unknown amount. The Bayes factor says how many times better the tilted explanation fits. Unlike a sigma, it can also show evidence *for* pure chance, and it behaves sensibly with small counts. Bands (Kass and Raftery): log10 below 0.5 is "barely worth mentioning", 0.5-1 "substantial", 1-2 "strong", above 2 "decisive".
- **Definition:**
  - **MAIN channel:**
    - Fair model P0(m) as in 4.4.
    - Tilted model P_theta(m) = P0(m) x exp(theta x m) / Z(theta), where Z(theta) = sum_j P0(j) x exp(theta x j).
    - With S = sum of m_t over n draws, log likelihood ratio l(theta) = theta x S - n x ln Z(theta).
    - BF_plus = integral over theta > 0 of exp(l(theta)) x pi_plus(theta), where pi_plus is a half-normal prior on theta > 0 with scale 0.5 (MRO-04).
    - BF_minus likewise for theta < 0, reported as inverse-signal evidence.
    - Computed by adaptive quadrature in log space.
    - Reported as log10 BF_plus, log10 BF_minus and the posterior mean of theta.
    - Sensitivity: prior scales 0.25 and 1.0 are also reported.
  - **PB channel** (Powerball): with k Powerball hits in n draws, H0 is q = 1/20 and H1 is q ~ Beta(1, 19), whose mean is 1/20.
    - BF = [B(1 + k, 19 + n - k) / B(1, 19)] / [(1/20)^k x (19/20)^(n - k)], computed with log-gamma.
- **Ranking key:** log10 BF_plus descending.
- **Outputs:** log10 BF_plus, log10 BF_minus, the band, the posterior mean of theta, and the sensitivity values.

### MR14 - Fidelity (quantum state fidelity / Bhattacharyya coefficient)

- **One line:** how closely the method's predicted probabilities matched what was actually drawn.
- **Short explanation:** for methods that state a probability for every number, this measures the overlap between that probability spread and the actual draw. It uses the formula quantum physics uses for the "fidelity" between two states; for ordinary probabilities, it reduces to the Bhattacharyya coefficient. It suits the pilot-wave family (E_57-E_62), whose outputs are Born-rule probabilities. A uniform guess scores exactly 0.2 for Powerball main numbers. Methods that output only a ranking show "not applicable".
- **Definition:**
  - Applicable only to tracks whose method declares the `PROBABILITY_OUTPUT` capability (section 13). Others report `INAPPLICABLE_NO_PROBABILITIES`.
  - **MAIN channel:**
    - For target t, normalise the method's per-label probabilities to q_j summing to 1. If they are inclusion probabilities summing to 7, divide by 7.
    - Let a_j = sqrt(q_j) and D_t = the set of drawn main numbers.
    - F_t = (1/7) x (sum over j in D_t of a_j)^2. A uniform q gives F_t = 7/35 = 0.2 (Powerball) or 7/47 (Oz Lotto).
    - The exact fair-draw expectation given q: E_t = (1/7) x [ pi1 + pi2 x ((sum_j a_j)^2 - 1) ], with pi1 = 7/N and pi2 = (7 x 6)/(N x (N - 1)).
    - The exact variance V_t uses inclusion probabilities of order up to 4 for sampling without replacement. Tests check it against simulation (MRT-11).
    - Z = sum(F_t - E_t) / sqrt(sum V_t), approx.
  - **PB channel:** F_t = q_PB(drawn Powerball); E_t = 1/20; V_t = (1/20) x sum_j q_j^2 - 1/400.
- **Ranking key:** Z_plus descending.
- **Outputs:** mean F, mean E, Z_plus, Z_minus.

### MR15 - Spectral periodicity of match counts (Lomb-Scargle)

- **One line:** do this track's match counts rise and fall in a repeating cycle?
- **Short explanation:** looks for a repeating rhythm in the track's match count from draw to draw, using the Lomb-Scargle periodogram, a standard astronomy method for finding periods in unevenly spaced data. It reports the strongest cycle length in draws and how likely a peak that strong would be by chance. It generalises MR2/MR3 to every draw, not only winning ones, so it works even when no prize was won. It echoes the spectral method family (E_33-E_40).
- **Definition:**
  - Standardise the series z_t = (m_t - mean0)/sd0, with the fair-draw values from 4.4, at the scored draw numbers t (gaps allowed).
  - Frequency grid: f_k = k / T for k = 1..K, where T = L - S + 1 and K = floor(T/2). That covers periods from T draws down to 2 draws.
  - Classical normalised power with known unit variance (Scargle 1982). Under the fair draw, each P(f) is approximately Exp(1).
  - False-alarm probability FAP = 1 - (1 - exp(-P_max))^K (approx), used as P_up in section 5.
  - PB channel: z_t = (b_t - 0.05)/sqrt(0.0475).
- **Ranking key:** Z_plus descending.
- **Outputs:** P_max, the best period 1/f in draws, the top 3 periods with their power, FAP, Z_plus.

---

## 7. In-sample diagnostic mode (IS)

**7.1 Purpose.** The owner wants to see how each method's *fully trained* state would have fared over the window. The owner knows this is biased: the window's draws are part of the training data. IS answers "how well does the method describe the draws it has seen". It never answers "how well does it predict".

**7.2 Procedure** (per game, method, variant; window [S, L]):

1. **Full fit:** fit the method once on F = H(L + 1), the eligible draws E(G)..L. This is the ordinary fit any target-(L+1) forecast would use. It reads no draw after L.
   - Record the frozen parameter digest, the master version and SHA, and the environment.
   - In Phase 1, L <= 1576 / 1693, so the fit never touches quarantined draws.
2. **Apply:** for each target N in [S, L], in ascending order, produce the entry from the frozen full-fit parameters plus, where the method uses recent-state inputs, the state derived from H(N) only.
3. **Score** each entry against draw N (section 4).

**7.3 Method capability** (declared by each method in the method-generic contract; section 13):

| Capability | Meaning |
|---|---|
| `IS_STATIC` | The full fit gives one fixed entry, scored against every target. Example: E_1's raw frequency counts give the same TOP and WORST for every past draw. |
| `IS_STATEFUL` | Fixed parameters, but the entry depends on the state before N (for example a fitted transition model applied to the previous draw). |
| `IS_NOT_APPLICABLE` | The method cannot separate fitting from applying (the owner's "curve fitting" example). The method appears in WF tables only; IS tables list it as "not applicable - see WF". |

**7.4 Firewall and labelling** (binding):
- IS results carry the product label `IN_SAMPLE_DIAGNOSTIC`.
- Every page, table and file of IS output carries the banner: "IN-SAMPLE DIAGNOSTIC - the scored draws were part of the training data; this is NOT evidence of prediction."
- IS records never enter the R3 scientific score ledger or the scientific result-consumer allowlist. They are never counted as walk-forward, holdout or prospective evidence, and never used by any method or meta-method.
- **IS and WF tracks are never ranked in the same table** (MRD-01).
- **Required paired display:** for every method with both modes, the report shows, for MR1, MR11 and MR12:
  - the IS value;
  - the WF value;
  - their difference, labelled "in-sample optimism".

  This turns the known bias into a useful overfitting gauge.
- **After holdout draws are opened:** IS windows extending into FINAL_HOLDOUT_10 or later are allowed only after those targets' frozen forecasts have been scored. From then on those draws are in-sample for IS purposes, and the report says so.

---

## 8. Supplementary-number rule change (MRD-03)

**Current ratified text** (R2, Architecture section 0 and Proposal):
- "Three supplementary Oz Lotto labels are provenance only and never become scientific inputs."
- Supplementaries are "excluded from every method view/scorer".

**Replacement rule, as drafted:**
- The Oz Lotto supplementary numbers of a **target** draw may be read **by the evaluator only**, after:
  - (a) that target's outcome is opened under the holdout rules; and
  - (b) the track's frozen forecast for that target exists.
- They may be used solely to compute `supplementary_matches` and the prize division (section 4).
- They remain excluded from every method view, fit, seed, view digest, readout and forecast.
- Methods do not forecast supplementaries. Oz Lotto has no Powerball channel (`ABSENT`, unchanged).
- The master already stores `Supp_1..Supp_3`, so no data change is needed.

**Scope confirmed by the owner (26 October 2026):** supplementaries are used for scoring and measuring only, never for predicting. Apart from Powerball's separate barrel, a prediction is only a set of numbers, and no number is designated in advance as a supplementary. Using supplementaries as method **inputs** would be a separate scientific decision: it would change view schemas and digests and add a new information channel. It is not part of this proposal.

---

## 9. Use of rankings (MRD-05; rules decided by Claude under the owner's delegation)

- **RK-1:** ranking outputs are **reports**. They never alter any frozen forecast, any fit, configuration, variant roster, readout or FINAL batch. This is consistent with R3's rule that no evaluator metric may affect forecasts.
- **RK-2:** ranking outputs are not scientific results. They are never placed on the result-consumer allowlist, and no method reads them.
- **RK-3:** any rule that uses rankings to **choose, weight or switch** methods for forecasting is a **forecasting method in its own right** (a "meta-method"). It must:
  - be registered under a permanent identity: a variant within the ensemble family E_55/E_56 if it fits their definition, otherwise a new identity E_63 or later by owner decision;
  - obey strict N-1: its ranking for target N uses only WF scores of targets < N, all of whose outcomes were known before N's forecast was frozen;
  - use **WF results only, never IS**;
  - pre-declare its measure, window, tie rule and minimum history;
  - produce its own TOP and WORST tracks, scored and ranked like any other method.
- **RK-4:** any report that highlights a top-ranked track shows the number of tracks and tests compared, and the global sigma (section 5).
- **RK-5:** the owner studying **development** rankings and then changing a method is permitted design influence on development data.
  - Any such change creates a new versioned variant (R2 change control).
  - The influence is recorded in the method change log.
  - Development rankings never extend into quarantined draws (3.6).
- **RK-6:** rankings over FINAL_HOLDOUT_10 are produced only after the Mode H scoring of those targets, never before.

---

## 10. Reporting (MRD-09)

**10.1 Files.** Each run writes, create-only (no overwrite; `os.rename` on Windows), into `results/method_rankings/<GAME>/`:
- `ranking_<GAME>_<MODE>_<S>-<L>_<UTCSTAMP>.txt`: human-readable, complete;
- `ranking_<GAME>_<MODE>_<S>-<L>_<UTCSTAMP>.csv`: one row per (track, sub-measure);
- `ranking_<GAME>_<MODE>_<S>-<L>_<UTCSTAMP>.json`: the run manifest.

Field values:
- `<GAME>` is `POWERBALL` or `OZLOTTO`;
- `<MODE>` is `WF` or `IS`;
- `<UTCSTAMP>` is `YYYYMMDDTHHMMSSZ` in UTC.

Example: `ranking_POWERBALL_WF_1286-1576_20261026T040000Z.txt`. This replaces the starter's example name `ranking_powerball_results_draw_xxxxx_yymmddhhmmss.txt`, carrying the game, mode, window and an unambiguous UTC timestamp.

**10.2 Text report layout:**
1. **Header:** game; mode, with the IS banner where it applies; window S-L; comparison-set size n; track counts by status; master version and SHA; tool version and SHA; environment summary.
2. **Glossary:** every measure, sub-measure, status, mode and product label used in the report, each with ID, name, one-line summary and short explanation, taken from `MEASURE_REGISTRY_V1`.
3. **Fair-draw reference:** the division probability tables (4.2/4.3), expected counts for this n, the sigma table (section 5), and the caution text.
4. **League tables:** one per measure and sub-measure. Each row gives rank, track ID, **method ID, name and one-line summary**, readout, variant, n, and all of the measure's output numbers.
5. **Per-track detail:** division count table, gap lists, sigma values per band, and so on.
6. **Notes:** M for the global sigma; `LOW_N` flags; undefined values; ties; tracks excluded by status.

**10.3 Methods in reports.** Every method appearing in a report is shown with its E-number, name and one-line summary in the tables, and its short explanation in the glossary (MRD-09). The method registry must therefore carry these texts (section 13).

**10.4 Ties.** Ties use standard competition ranking ("1=, 1=, 3"), marked "=". Within a tie, rows are listed by track ID, for display only.
- Exact quantities (counts, exact fractions) are compared exactly.
- Floating quantities are compared at full float64 equality.
- Report ties are not forecasts; `TIE_SHA256_V1` is not used.

**10.5 Number display:**
- counts as integers;
- probabilities in scientific notation to 6 significant digits;
- percentages to as many decimals as needed to show the first digit that differs from 9 (up to 12);
- sigma to 2 decimals;
- bits to 3 decimals;
- Bayes factors as log10 to 3 decimals.

---

## 11. Numerics and precision (MRD-02, existing owner rule)

- Integers are `int64` throughout, with Python `int` (arbitrary precision) for combinatorial counts and exact tails. Floating values are `float64`. No narrower types are used anywhere.
- Division probabilities are held as exact fractions (Python `fractions.Fraction`) built from binomial coefficients.
- Binomial tails P_up and P_lo are computed **exactly** as fractions, summing whichever side has fewer terms, and are converted to float64 only at the end. Values below the float64 range are carried as log10 values.
- The sigma conversion Phi_inv(1 - P) is evaluated from P directly (inverse survival function), never from 1 - P, so small P keeps its accuracy.
  - Required accuracy: 1e-6 absolute in sigma for P >= 1e-300.
  - Below that, a documented asymptotic inversion is used and labelled.
- Bayes-factor integrals use log-space quadrature. Tests use known closed-form cases.

---

## 12. Execution model (independent of production; MRD-13)

- **WF rankings** are produced by a standalone **report tool** that reads only stored frozen forecast records, opened outcomes and the measure registry. It runs no method code.
  - It runs whenever the owner chooses, for example after the weekly scoring.
  - It is never part of the FINAL batch, so it cannot delay or alter the freeze-before-the-draw step.
- **IS runs** are method runs: one full fit plus applications.
  - They go through the existing single launch interface (`Run_Experiment.bat`, optionally under the coordinator), with a declared mode `in-sample-diagnostic`.
  - Their outputs go to the IS namespace, separate from scientific results.
- The **report tool's wrapper** (proposed `Run_Method_Rankings.bat`) follows the ratified wrapper rules: venv checks, `SETLOCAL`/`ENDLOCAL`, the explicit `.venv` Python, `%*` forwarding. Like `Run_Results_Updater.bat`, it is a tool launcher, not a second experiment launcher. The Architecture amendment records it.
- The report tool is an **evaluator**. It may read an outcome only for targets that are opened and that have frozen forecasts. It reads supplementaries under section 8 only.
- The dependency rules are unchanged: no upgrade between freezing a forecast and scoring it, or within Mode H. The report records its own environment.

---

## 13. Phasing - when to code it

| Stage | When | What |
|---|---|---|
| 0 | Now | Review this proposal (ChatGPT, Claude), owner ratification, then integrate into the governing documents (section 15). No code. |
| 1 | In the **method-generic contract** that Architecture 20A requires before E_2 (P3 W5 or its successor task). **Not in Package 2 v0.11**, whose scope stays C1-C6. | Add record fields and capabilities, cheap to add now and costly to retrofit after many methods exist: (a) TOP and WORST entries per target (already required); (b) the full ranking and scores (already required by R3); (c) optional per-label probability vectors plus a `PROBABILITY_OUTPUT` flag; (d) IS capability (`IS_STATIC` / `IS_STATEFUL` / `IS_NOT_APPLICABLE`) and the fit/apply split interface for IS; (e) registry text per method and variant: name, one-liner, short explanation. |
| 2 | With the R3 **scorer**, after E_1's development walk-forward is produced and authorised | Match records, division classification (with the supplementary rule), MR0, MR1/MR1-T, MR4, MR5, the report format and glossary, the sigma machinery, tests MRT-01..MRT-10 and MRT-12..MRT-14. Exercised on E_1 and on synthetic tracks (synthetic firewall applies). |
| 3 | After E_2-E_6 walk-forward results are scored | MR2, MR3, MR11-MR15, IS mode, multi-method league tables, the global sigma, the paired IS/WF display. Remaining tests. |
| 4 | Later | Any registered meta-method (RK-3), with its own review. |

No real-data ranking run happens before the scorer is accepted and the owner has authorised the walk-forward runs it reads.

---

## 14. Tests (to be satisfied by the implementation)

| ID | Test |
|---|---|
| MRT-01 | The division probability tables equal the exact fractions in section 4. Rounded odds agree with the official sources (Powerball rule 9.4 divisions; Lotterywest Oz Lotto odds). |
| MRT-02 | Classification is exhaustive and exclusive: every (m, b) and every valid (m, s) maps to exactly one division or 0. Invalid combinations (s > 7 - m) are rejected. |
| MRT-03 | The sigma conversion reproduces section 5's table to 1e-6. k = 0 gives 0 sigma. Clamping works both ways. |
| MRT-04 | Exact binomial tails agree with an independent exact implementation, including n up to 5000 and p down to 1e-9. No float underflow loses the result. |
| MRT-05 | Isolation: no outcome is read for targets beyond L or not yet opened. Supplementaries are read only by the evaluator for scored targets. No method view contains supplementaries (static and runtime checks). |
| MRT-06 | IS firewall: IS records are refused by the scientific score ledger and the allowlist. The banner appears on every IS output. No table mixes IS and WF tracks. |
| MRT-07 | Planted-effect synthetic tracks (built-in skill) give positive MR4, MR11-MR15 and MR5. Null synthetic tracks give roughly the nominal false-alarm rates. Synthetic data never mixes with real data. |
| MRT-08 | Determinism: the same inputs give byte-identical CSV files, and text files identical apart from header timestamps. |
| MRT-09 | Tie display follows 10.4. |
| MRT-10 | MR5 per-target values equal R3's evaluator values. |
| MRT-11 | MR14's exact expectation and variance agree with a fixed-seed simulation within tolerance (test-only randomness). |
| MRT-12 | All numeric fields are int64/float64. No narrowing anywhere. |
| MRT-13 | Every ID printed in a report has registry text (name, one-liner, explanation). The report fails if any is missing. |
| MRT-14 | Window guard: S >= E(G); L within the cap (Phase 1: 1576 / 1693). An Oz Lotto S < 1474 is rejected. |
| MRT-15 | (Stage 4) A meta-method's ranking for target N uses only WF scores of targets < N. |

---

## 15. Integration into the governing documents on ratification

Following the owner's preference for one clean current text per document, not addenda, the ratified content goes into new editions:

| Document | Integration |
|---|---|
| Proposal (v0.6) | Charter-level statement of the ranking purpose; the IS diagnostic as a permitted, labelled product; the reporting-explanation rule MRD-09 for methods and measures. |
| R2 (v0.5) | The supplementary rule (section 8) replacing the current exclusion text; the IS mode definition and firewall (section 7); the contract fields and capabilities (section 13, stage 1); the numbering conventions (3.2). |
| R3 (v0.5) | A new section for the method ranking measures: sections 3.4-3.7, 4, 5, 6, 9 and 10; division-based scoring for both games; the sigma convention; RK-1..RK-6. |
| Architecture (v0.8) | The report tool and its wrapper; IS runs through `Run_Experiment.bat`; output paths; contract hooks in 20A. Section 5C is untouched. |
| P3 or successor task spec | Stage 1 hooks inside the method-generic contract work; a later task spec for stages 2-3. |
| Ratification register (v0.4) | New entries and hashes. |

---

## 16. Open items

| ID | Item | Draft default |
|---|---|---|
| MRO-01 | Scope of the supplementary rule | **RESOLVED (owner, 26 Oct):** scoring and measuring only (MRD-03, section 8). |
| MRO-02 | Keep MR1-T (the owner's 90/7/3 top-division weighting) alongside MR1? | **RESOLVED (owner, 26 Oct):** keep (MRD-14). |
| MRO-03 | MR6-MR10 reserved for ChatGPT or owner proposals | Open. |
| MRO-04 | MR13 prior scale | 0.5, with 0.25 and 1.0 sensitivity. |
| MRO-05 | Minimum n before approximate measures are shown unflagged | 30. |
| MRO-06 | Identity for any future ranking-based meta-method (E_55/E_56 variant or E_63+) | Decide when proposed. |
| MRO-07 | Whether Oz Lotto MR11-MR15 gain a supplementary channel | Main only. |
| MRO-08 | Family definition for the global sigma (per table, per report or per programme) | Per table. |

---

## 17. Traceability to the owner's starter text

| Starter item | Where addressed |
|---|---|
| "data for draws 1 to P0 / O0; first draw in 2021 is P1 / O1" | 3.6: S defaults to the first current-era draw on or after 2021-01-01 (Powerball 1286; Oz Lotto 1474 under MRD-04); L to the cap. |
| Step 1: full training on all data, bias acknowledged | Section 7 (IS mode), firewalled and labelled. |
| Step 2: Pi from P0 to P1, parameters with defaults | 3.6 window parameters; processed in ascending draw-number order (MRD-12). |
| 2.1: use the fully trained data to predict Pi | 7.2, apply step (`IS_STATIC` / `IS_STATEFUL`). |
| 2.2: methods where full training does not apply: usual method 0..Pi-1 | 7.3 `IS_NOT_APPLICABLE`: shown in WF tables only, never mixed (MRD-01); 3.3 training set. |
| 2.3: collect matches in a list or dict | 4.1 match records (CSV/JSON). |
| Step 3: rankings R0..Rn, separately per game, displayed | Sections 6 and 10. |
| Powerball D1-D3, Oz D1-D3, top-down | Sections 4.2-4.3, all divisions (MRD-02); classification automatically gives the highest division. |
| R0 | MR0 (all divisions, lexicographic, then MR1). |
| R1 (weights 90/7/3; typo) | MR1-T (corrected); MR1 surprisal weighting across all divisions. |
| R2, R3, R4 (periodicity of D1, D2, D3) | MR2.PD1/PD2/PD3 (and Oz), extended to all divisions. |
| R5, R6, R7 ("due" alignment) | MR3, likewise. |
| R8, R9, R10 (sigma for {D1-D3}, {D2-D3}, {D3}) | MR4.C.3, MR4.B.2-3, MR4.X.3; plus all exact and cumulative sets. |
| Output file with rankings and the numbers used | Section 10. |
| Up to 5 further measures with a statistical or quantum link | MR11-MR15. |
| Run independently, or within production only if necessary | Section 12: independently; never inside the FINAL batch. |
| "Does it change the architecture?" | Sections 12, 13 and 18. |

---

## 18. Claude's analysis, implications and design matters

**18.1 Feasibility and cost.** The proposal is fully doable.
- In WF mode the ranking tool only re-reads stored forecasts and outcomes and does arithmetic: seconds per game.
- IS mode adds one full fit plus one application per target per method, small next to the walk-forward runs, which refit for every target.
- The expensive part, walk-forward forecasting, is already planned for its own sake.

**18.2 Measurement resolution: why all divisions matter.** Expected division wins under a fair draw, per track (one TOP or WORST stream) and across 124 tracks (62 methods x TOP/WORST, one variant each), for the default Phase 1 windows:

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

The top three divisions are expected essentially never under a fair draw. Any win there would register as a high local sigma (one PD3 win in 291 draws is about 3.3 sigma locally), which is exactly why the global sigma matters.

The lower divisions occur often enough to separate tracks, and to give MR2/MR3 periodicity something to measure. MR11-MR15 use every draw, so they have resolution whether or not any prize is won. The owner's decision MRD-02 is what makes the league tables informative.

**18.3 What in-sample results can and cannot show.**
- For a static method such as E_1's raw counts, the IS entry is one fixed ticket: by construction, the numbers most frequent in the training draws. Scoring it against those same draws inflates matches, because the ticket was chosen with the outcomes in view.
- IS therefore measures **descriptive fit**. Its legitimate uses are:
  - showing how a method's fully trained state relates to the history it learned from;
  - through the paired IS/WF display, quantifying each method's **in-sample optimism**, a direct overfitting gauge. A method with large optimism and no WF advantage is fitting noise; a method whose IS and WF results agree is at least stable.
- The Proposal already anticipates separate in-sample diagnostics. Section 7's firewall keeps them from being mistaken for evidence.

**18.4 Multiple comparisons.** League tables make many comparisons at once.
- With about 124 tracks and about 20 sub-measures per table family, M is about 2,500 tests.
- Under a fair draw, about 2,500 x 0.00135, roughly 3, local results at or above 3 sigma are expected **by chance alone**; a local 5 sigma by chance is expected about 0.0007 times.
- Hence: global sigma beside local (section 5), RK-4, and R3's existing requirement to disclose multiple comparisons.
- The Sidak adjustment assumes independent tests. Methods built on similar ideas give correlated results, so the adjustment is conservative for some families and not for others. It is presented as approximate.

**18.5 "Due" measures and the fair-draw ruler.** Under a fair draw, wins have no memory: the gap to the next win does not depend on time since the last one. MR3 is therefore reported as a pattern indicator, as context and not as a veto. That fits the project philosophy: no method or idea is excluded because conventional statistics says it cannot work. Its value as a choosing rule can be tested honestly only as a registered meta-method (RK-3), whose own forecasts are then scored like any other.

**18.6 Selecting the best performer.** A track that tops a league table is partly there by luck, so its next results will usually be less extreme ("regression to the mean"). This is not an objection to ranking. It is why any "follow the leader" rule must be scored prospectively as its own method (RK-3), and why reports show global sigma and the number of tracks compared (RK-4).

**18.7 Design implications (summary).**
1. **Package 2 v0.11:** no change.
2. **Method-generic contract** (before E_2): record fields and capabilities (section 13, stage 1). This is the one design item that matters now.
3. **Rule changes needing ratification:** the evaluator-only supplementary rule (section 8); division-based scoring and the ranking measures in R3; the IS product label and firewall in R2; the reporting-explanation rule for methods and measures (MRD-09); the numbering conventions (3.2).
4. **New components:** the ranking report tool and wrapper; the IS run mode on the existing launch interface; `MEASURE_REGISTRY_V1` with explanation texts; registry texts for every method and variant.
5. **No impact** on Architecture 5C process safety, the switches, the holdout boundaries, the E_1 goldens or the master data.

**18.8 Holdout and Mode H.** In Phase 1, every window ends at 1576 / 1693 and every IS fit ends there too, so nothing touches quarantined draws. After FINAL_HOLDOUT_10 is opened and its frozen forecasts are scored under Mode H, windows may extend over it (RK-6). From then on, IS results over those draws are in-sample for them, and the report says so.

**18.9 Philosophy compliance.**
- No measure excludes, demotes or vetoes a method. Every method remains registered and reported whatever its ranking.
- Fair-draw figures appear as measuring rulers beside every result.
- Unusual measures (MR3's "due" alignment, MR14's quantum fidelity, MR15's spectral cycles) sit beside conventional ones, and all are reported with plain explanations.

*End of document.*
