# Predictive Randomness - wave 2: E_2, E_17 (Method A), E_19 and E_18 (gaps between appearances), design note v0.1

**Document:** the method-level specification of the first variants of E_2, E_17, E_18 and E_19 (R2 v0.5 sections 7.1 and 7.17; R1 v0.4), with one shared gaps helper, and the design of the package that adds them. E_17 takes the predictor of the owner's Method A (`GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md`, section 3).
**Version:** v0.1r1 DRAFT for the reviewer's focused RECHECK, 30 October 2026. It resolves EX_069's three findings: W2-B01 (E_17's slope variant is replaced by Method A's own log-age rule, decided exactly; owner decision W2-3), W2-C01 (E_18's fitting from completed gaps only, and its limits, are stated) and W2-O01 (the template finding is reworded as a byte-reproducibility rule; owner decision W2-7). Nothing else changes. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule.
- **No code yet:** the code follows only after this design passes.
- **Probes:** feasibility and behaviour probes on invented data are reported in section 8; the reference script that computes every number in sections 8 and 9 travels with this note.
- **Base:** `main` at `0026cb7` (wave 1 installed at `947c370`, with register v0.18).
- **The owner's order of work** (register v0.18): wave 2 is E_2, E_17 as Method A, E_19 and E_18. Then come releases and WF-1, and wave 3 (with Method B as E_45).

## 1. In plain English

Four ways of using **how long it has been since each number was last drawn**:
- **E_2 (recurrence-interval alignment):** each number has its own typical gap between appearances (its average, or its middle value). E_2 favours the numbers for which the next draw would complete a gap of about that length: "its usual return is due now", not "the longest overdue".
- **E_17 (recurrence hazard; your Method A's predictor):** pooled over all numbers of a barrel, how likely is a number to come up, given how long it has been absent? If the answer is flat, there is no effect. If recently drawn numbers come up more often ("hot") or less often, E_17 learns that from the data, including its direction, and ranks accordingly. One variant is exactly your Method A's rule, using its own log of the age.
- **E_19 (periodic hazard):** does that chance repeat with a short cycle? For example, if two draw machines alternated and one favoured a ball, that ball would tend to return after an even number of draws. E_19 looks for cycles of 2, 3 and 4 draws, number by number.
- **E_18 (mixture of recurrence modes):** each number's gaps are described as a mix of four fixed patterns: quick returns, fair returns, long absences, and evenly spaced returns. E_18 learns each number's mix and asks how likely its return is now.

**None of them uses random numbers.** Everything is exact fractions, as in every installed method, so Windows and Linux publish the same bytes. Method A's diagnostic tests (A1 to A5), which need simulated fair histories and so random numbers, are proposed as a separate later package with the NIST seed (section 13, decision W2-3).

## 2. What is modelled

- **The observation:** for target N, barrel B (K of its L labels drawn per draw; fair rate r = K/L; fair mean gap m = L/K) and label j, the eligible draws are those before N, at positions i = 1..W, oldest first.
- **The view:** `UNORDERED_SET`, without dates. As for every method, it holds only the current game format's draws (Method A's section 5.1 requirement is met by the contract's view, not by the method).
- **Barrels:** Powerball MAIN (K = 7, L = 35, m = 5) and POWERBALL (K = 1, L = 20, m = 20); Oz Lotto MAIN (K = 7, L = 47, m = 47/7).
- **Minimum history:** stated per variant (section 6). Earlier targets get the contract's `INSUFFICIENT_HISTORY` record.

## 3. The shared definitions (the gaps helper)

**3.1 Appearances, gaps and ages.**
- **Appearances:** a_1 < a_2 < ... < a_n, the positions at which j was drawn.
- **Completed gaps:** g = a_{t+1} - a_t (each at least 1; 1 means consecutive draws).
- **Age at draw i:** i minus j's last appearance before i.
- **The projected age** at the target: G_j = W + 1 - a_n. It is the gap that j would complete if drawn at the target (R1's "projected next-draw age"); G_j = 1 means j was drawn in the latest draw.
- **A never-seen label** (n = 0) is treated as last seen at position 0, so G_j = W + 1. This is a lower bound on its true age, and is the stated convention.

**3.2 Censoring (Method A's section 3.4 item 7).**
- **The stretch before a label's first appearance** has unknown age. It is excluded everywhere: no gap and no exposure.
- **The open stretch since the last appearance** is not a completed gap. It is every method's input G_j. How it enters each estimate differs:
  - **E_17 and E_19** estimate hazards from exposures (3.3), so the open stretch enters them as at-risk exposures without an event: proper right-censoring.
  - **E_18** fits its mixture weights from completed gaps only (4.4), so the open stretch does not enter the fit; it only says where the fitted hazard is read.
  - **E_2** estimates no hazard: its characteristic interval comes from completed gaps, and G_j is compared with it.

**3.3 Exposures (for E_17 and E_19).** Each (label, eligible draw) pair with a known age k is one exposure. It is at risk at age k, with an event if j is drawn at that draw. R_k and E_k are the pooled at-risk and event counts at age k over the barrel's labels; a window S restricts them to the newest S draws, with ages still measured from the true last appearance. Under fair draws every exposure's event chance is exactly r, whatever its age.

**3.4 Age bins** (E_17, E_18). The upper bin edges are the distinct values of ceil(f m) for f = 1/5, 2/5, 3/5, 1, 8/5, 13/5, giving seven bins on a roughly logarithmic scale:

| Barrel | m | Bins (ages) |
|---|---|---|
| Powerball MAIN | 5 | 1, 2, 3, 4-5, 6-8, 9-13, 14+ (exactly Method A's A2 bins) |
| POWERBALL | 20 | 1-4, 5-8, 9-12, 13-20, 21-32, 33-52, 53+ |
| Oz Lotto MAIN | 47/7 | 1-2, 3, 4-5, 6-7, 8-11, 12-18, 19+ |

All six edges are distinct for the three real barrels. In a small test barrel, repeated edges merge (an empty bin is dropped).

## 4. The rules

**4.1 E_2, recurrence-interval alignment.** For label j with completed gaps (all, or the last 8), the characteristic interval c_j is:
- their mean (for all gaps, exactly (a_n - a_1)/(n - 1)), or their median (the mean of the two middle values when the count is even);
- m, the fair mean gap, if j has no completed gap (R2's "handle never-seen values").

The score is the relative distance, negated so that closer scores higher:

  s_j = -|G_j - c_j| / c_j

A score of 0 means the next draw would complete exactly j's characteristic gap. The relative form puts all labels on one scale, whatever their typical gap.

**4.2 E_17, discrete recurrence hazard.** Two forms.
- **Binned (R1's "flat, increasing, decreasing or peaked shapes"):** for bin b, with R_b and E_b the at-risk and event counts summed over its ages, and prior strength c:

  h_b = (E_b + c r) / (R_b + c),  and  s_j = h_{bin(G_j)}

  This is each bin's Beta posterior mean, shrunk towards the fair rate by c fair exposures.
- **Log-age sign (Method A's A3 predictor, exactly in its ranking; owner decision W2-3):** with n = sum of R_k exposures and e = sum of E_k events, the integers a_k = n E_k - e R_k (they sum to 0) give

  n S_zy = sum_k a_k ln k,  sigma = sign(n S_zy) in {+1, 0, -1},  and  s_j = sigma G_j

  Here S_zy = sum over exposures of (z - zbar)(y - ybar), with the covariate z = ln(age), as Method A has it; y is 1 for an event.

**Why this is Method A's predictor, exactly in its ranking.** Method A fits a logistic regression of appearance on log(gap), with mild shrinkage of the slope towards 0, and ranks by the fitted chance at the projected age. Three facts make sigma G_j rank the same way:
1. **Only the sign of the slope matters for the ranking.** The fitted chance is a strictly increasing (positive slope) or strictly decreasing (negative slope) function of the age. So the ranking is "longest absent first" or "most recently drawn first", and equal ages tie.
2. **Shrinkage towards 0 never changes that sign,** so a ridge penalty of any fixed size has no effect on the ranking. None is used.
3. **The logistic slope has the sign of S_zy, for the same covariate.** With the intercept profiled out, the log-likelihood is concave in the slope, and its derivative at slope 0 is S_zy, the score statistic. So the maximum-likelihood slope has the sign of S_zy (or is infinite with that sign, if the data separate).

**This needs Method A's own covariate.** v0.1 used the harmonic number H_k in place of ln k and claimed the same ranking. EX_069 (W2-B01) proved that false with an exact witness: another increasing transform of the age can reverse the sign. On fair invented draws, the two signs differed at 10 of 312 targets (section 8). The harmonic slope is withdrawn.

**How the sign is decided exactly.** sum_k a_k ln k = sum_p e_p ln p over the primes p dividing the ages, with integers e_p = sum_k a_k v_p(k) (v_p(k) is the power of p in k).
- **Bounds:** rational lower and upper bounds on each ln p come from ln p = a ln 2 + 2 atanh((m - 1)/(m + 1)), with p = 2^a m and 1 <= m < 2, and ln 2 = 2 atanh(1/3). The atanh series is summed for a fixed number of terms, and its tail is bounded by a geometric series.
- **The loop:** the number of terms doubles until the bounds on sum_p e_p ln p exclude 0.
- **It always ends.** The logs of distinct primes are linearly independent over the rationals (by unique factorisation), so sum_p e_p ln p is 0 only when every e_p is 0. The method then returns sigma = 0 without any bound.
- **The cost:** at most 0.007 s per target in the probes; 8 terms sufficed at every probed target.
- **The published scores** are the integers sigma G_j, exactly representable in float64. They are not Method A's fitted chances, which would need an iterative fit, but they rank identically.

When sigma = 0, every label scores the same: one tie group, ordered by the contract's `TIE_SHA256_V1`. That is a fixed pseudo-random order with no lean towards low numbers, which is what Method A asked of its seeded tie-break, with no seed needed.

**4.3 E_19, periodic recurrence hazard.** With cycle length T, residue q = k mod T, E_17's binned hazard b(k) = h_{bin(k)} (prior c) as the trend, and shrinkage d:
- **Per label and residue:** O_{j,q}, the events at ages k = q (mod T), and X_{j,q}, the sum of b(k) over j's exposures at those ages (the events the trend alone predicts).
- **Pooled:** phi_q = (O_q + d) / (X_q + d), with O_q and X_q summed over labels.
- **The label's own periodic factor,** shrunk towards the pooled one, with the label's overall level divided out:

  psi_{j,q} = [(O_{j,q} + d phi_q) / (X_{j,q} + d)] / [(O_j + d) / (X_j + d)]

  O_j and X_j are j's totals over all residues.
- **The score:** s_j = b(G_j) psi_{j, G_j mod T}.

**Why it is built this way:**
- **Dividing by the trend** keeps E_17's age effect (for example, clustering at age 1) from showing up as a false cycle.
- **Dividing by the label's own level** keeps a frequently drawn number from looking periodic. In probes, without that division a planted cycle mostly reappeared as a frequency effect (section 8).
- **The periods are fixed at 2, 3 and 4,** one per variant, and are never scanned or chosen afterwards (R1's warning about accidental peaks).
- **The physical reading:** a rotation of machines or ball sets every 2, 3 or 4 draws, with one of them biased, would make a ball return at ages that are multiples of the cycle. Periodicity in the draw index itself (calendar, machine identity) belongs to E_14 and E_15 and to Method A's diagnostic A5, not here.

**4.4 E_18, mixture of recurrence modes.** A fixed library of four gap laws, all exact:
- **FAST:** geometric, mean m/2 (rapid returns);
- **FAIR:** geometric, mean m (the fair law itself);
- **SLOW:** geometric, mean 2m (long absences);
- **REGULAR:** negative binomial of shape 2 with p = 2r, mean m (the fair average gap, but more evenly spaced): P(g) = (g - 1) p^2 (1 - p)^(g - 2) for g >= 2. Its survival is P(gap >= G) = (1 - p)^(G - 1) + (G - 1) p (1 - p)^(G - 2), and its hazard rises from 0 at age 1 towards 2r.

**Fitting each label:**
- **The data:** j's completed gaps (all, or those with both ends inside the newest S draws) are binned with section 3.4's bins. Only completed gaps are used (W2-C01): this is a descriptive fit of the gaps seen, not a censored-likelihood fit.
- **A prior:** c pseudo-gaps distributed exactly as the fair law, giving the shrunk bin shares q_b.
- **The mixing weights** w (non-negative, summing to 1) minimise sum_b (q_b - sum_c w_c P_c(b))^2 / P_FAIR(b): a minimum chi-square fit with the fair law's expected shares as denominators.
- **Exactly:** the objective is a strictly convex quadratic (the four components' bin vectors are linearly independent), so the optimum is the unique feasible solution with the smallest objective among the equality-constrained solutions on the 15 possible supports. Every support is tried, in fractions.
- **The score** is j's predictive hazard at its projected age:

  s_j = sum_c w_c P_c(gap = G_j) / sum_c w_c P_c(gap >= G_j)

**Properties:**
- **The fair law is nested.** A label with no completed gap gets w = FAIR exactly and the score r.
- **Why minimum chi-square, not EM:** EM would need iterations in floating point (no longer exact or platform-identical) or in fractions (whose size explodes). The fixed library makes the fit a small exact quadratic programme.
- **Why four components:** with FAST, FAIR and REGULAR only, a label with rapid returns and long absences was not representable. SLOW was added, and the rapid-plus-absent probe then works (section 8).
- **The limits of fitting completed gaps only** (W2-C01), stated and accepted for revision 1:
  - **A current long absence does not enter the fit.** A number in the middle of a long absence has no completed gap for it yet, so its fit leans, slightly, towards its shorter past gaps.
  - **Long gaps are under-represented.** A gap of length g fits within a span of S draws at only S - g of its possible positions. The windowed variants show this most: for POWERBALL with S = 104, a 40-draw gap carries about 0.6 of a 1-draw gap's chance of being counted. The effect is the same for every label, and it can move weight towards FAST and away from SLOW.
  - **A censored-likelihood fit,** which would use the open stretch and remove both effects, would be a separate variant with its own design review.

## 5. Outputs, per barrel (E2R-1 sections 5 and 7)

**Every channel:**
- `RANKING_WITH_SCORES`, `FLOAT64`;
- TOP `TOP_MARGINAL`, WORST `INVERSE`, `TOP_MARGINAL_AND_INVERSE_V1`;
- `TIE_SHA256_V1`.

**Every declaration:** score-only (`probability_kind` `NONE`, no `ProbabilityVector`; decision W2-4); no diagnostic record; deterministic (`stochastic_fit` false, no seed); `IS_NOT_APPLICABLE`; Oz Lotto MAIN only.

| Method | `fit_sampling_model_version` |
|---|---|
| E_2 | `RECURRENCE_INTERVAL_ALIGNMENT_V1` |
| E_17 | `DISCRETE_RECURRENCE_HAZARD_V1` |
| E_19 | `PERIODIC_RESIDUE_HAZARD_V1` |
| E_18 | `FIXED_LIBRARY_GAP_MIXTURE_MINCHISQ_V1` |

**Why score-only:**
- E_17's and E_18's scores are conditional chances for each label alone, but they do not sum to K across labels. A published vector would need an extra renormalising step that is a model choice of its own.
- E_2's and E_19's scores are not chances at all.
- The calibration notes say so, and add that each method is not expected to beat chance if the draws are fair.

## 6. The variants (fixed in revision 1)

All variants are in both games. "Min" is `minimum_history_draws`.

| Method | `variant_id` | Settings | Min | Meaning |
|---|---|---|---|---|
| E_2 | `RECUR_MEAN_ALL_V1` | mean of all gaps | 104 | the number's average return |
| E_2 | `RECUR_MEDIAN_ALL_V1` | median of all gaps | 104 | its middle return (robust to long absences) |
| E_2 | `RECUR_MEAN_LAST8_V1` | mean of its last 8 gaps | 104 | its recent rhythm |
| E_17 | `HAZARD_BINS_C100_V1` | binned, c = 100, all exposures | 52 | the hazard's shape, whole history |
| E_17 | `HAZARD_BINS_W208_C100_V1` | binned, c = 100, newest 208 draws | 208 | the same over the last 4 years |
| E_17 | `HAZARD_LOGAGE_SIGN_V1` | sign of the log-age trend, all exposures | 52 | Method A's predictor, exactly in its ranking |
| E_19 | `PERIODIC_T2_V1` | T = 2, c = 100, d = 20 | 104 | a 2-draw cycle |
| E_19 | `PERIODIC_T3_V1` | T = 3, c = 100, d = 20 | 104 | a 3-draw cycle |
| E_19 | `PERIODIC_T4_V1` | T = 4, c = 100, d = 20 | 104 | a 4-draw cycle |
| E_18 | `MIX4_ALL_C10_V1` | all gaps, c = 10 | 104 | each number's whole-history mix |
| E_18 | `MIX4_W208_C10_V1` | gaps inside the newest 208 draws, c = 10 | 208 | its mix over the last 4 years |
| E_18 | `MIX4_W104_C10_V1` | gaps inside the newest 104 draws, c = 10 | 104 | its mix over the last 2 years |

**Notes on the settings:**
- **Method A's burn-in** of 52 draws is kept for its own variants. The per-label methods start at 104, so that Powerball numbers (about one appearance in 20 draws) have a few gaps.
- **E_18 varies its window, not its prior.** In probes, prior strengths c = 2 and 40 shared 6.7 to 6.8 of their TOP 7 with c = 10, while the 208-draw window shared 4.35 with the whole history.
- **The windows are counted in draws, not gaps,** so that they mean the same in every barrel. A window of "the last 30 gaps" would equal "all gaps" for every Powerball number for years.
- **E_2's last-8 variant** counts gaps, since its question is the number's own last few returns.
- **The count:** 4 methods x 3 variants x 2 games = 24 declarations and 24 `FORMULA_OPEN` entries.

## 7. Relation to other methods (honest overlap; template section 8)

- **E_17 `HAZARD_LOGAGE_SIGN_V1` ranks purely by projected age:** longest absent first if sigma = +1, most recently drawn first if sigma = -1, and labels of equal age tie (section 4.2). No installed method ranks exactly this way. E_9's fastest decay (lambda = 5/6) is the nearest, since its score is dominated by the latest appearance, but it also counts earlier ones.
- **E_17's binned variants rank by the age bin only,** so all labels in one bin tie, and the order within a bin is the contract's tie order. That is the model's own statement: labels of similar age are equal.
- **E_19 is E_17's `HAZARD_BINS_C100_V1` times a periodic factor:** s_j / b(G_j) = psi_{j, G_j mod T} exactly. When no number shows a cycle, E_19's ranking tends towards E_17's binned one, refined by small factors. On fair invented draws, they shared 2.85 of their TOP 7 on average (chance: 1.40).
- **E_18 partly ranks by frequency:** a number with more appearances has shorter gaps, more FAST weight and a higher hazard. On fair invented draws, it shared 4.1 of its TOP 7 with E_1. It differs from E_1 where a number's gap pattern, not its count, sets its hazard.
- **E_2 differs from all of these:** it is the only method whose favoured age is set by each label's own typical gap. It shared 0.1 of its TOP 7 with E_17's binned form and 1.7 with E_1.
- **Which pattern each method catches** (planted probes, section 8):
  - an even rhythm at one age is caught by E_2's median variant, not by E_18 (its fixed laws cannot make a sharp peak), and not by E_2's mean (the long absences pull the mean away);
  - rapid returns with long absences are caught by E_18;
  - clustering after a draw is caught by E_17;
  - a single-ball 2-draw cycle is caught by E_19 T = 2.

The tests check each exact relation (E_17's log-age ranking against a pure age ordering; E_19's ratio identity; E_18's nested fair law), comparing `ranked_groups`.

## 8. Feasibility and behaviour (author probes; invented draws only, never real data)

Invented draws are deterministic (SHA-256 orderings, no random-number generator). Planted effects use weighted draws without replacement with a fixed multiplier rule.

- **Speed,** one target at the full invented history, exact fractions: the slowest variants (E_18's) took between 0.1 and 0.5 s per target across runs (Powerball 433 draws, Oz Lotto 218). All others took 0.02 s or less. The evidence file `ev_wave2_probes.txt` holds every probe's output.
- **E_17's log-age sign on fair draws:**
  - over independent fair histories (W = 300), it was +1 in 99 of 200 POWERBALL histories and 69 of 120 MAIN ones (the mean of S_zy at -0.46 and +1.25 standard errors from 0); no bias is evident;
  - within one history, consecutive targets share their sign, because they share their draws.
- **The exact sign rule** (W2-B01):
  - on EX_069's witness history, it gives -1 (60-digit decimal value of n S_zy: -2798.499...), while v0.1's harmonic slope was positive;
  - over 312 targets of three invented histories (all three barrels), it agreed with a 60-digit decimal computation, and with the second route of section 10, every time;
  - the harmonic slope's sign differed from it at 10 of the 312.
- **E_18 on fair draws:** on average 40% to 46% of a MAIN number's weight sits off FAIR, by noise. FAST plus SLOW can imitate FAIR, so the split between components is weakly identified; the hazard is what is used.
- **Planted effects** (MAIN, 433 draws):

  | Planted | Result |
  |---|---|
  | Clustering: a number drawn last draw is 1.6x as likely | E_17's log-age sign -1 (n S_zy about -5.75 million; over 40 fair histories of the same size its standard deviation was about 0.65 million); age-1 bin hazard 0.272 against about 0.19 |
  | One ball 3x as likely on odd draws (a 2-draw cycle) | E_19 T = 2: that ball in the TOP 7 at 79 of 164 favoured targets, and 20 of 165 others. Without dividing out its level: 141 and 101 (mostly a frequency effect, so the level is divided out) |
  | One ball 2.5x as likely at ages 1-2, 0.4x later | E_18 (`MIX4_ALL`): in the TOP 7 at 42 of 42 favoured targets, and 7 of 123 others; weights FAST 0.65, SLOW 0.35 |
  | One ball 4x as likely at age 5, 0.25x otherwise | E_2 median: in the TOP 7 at 21 of 21 targets where its projected age is 5, and 27 of 308 others. E_2 mean: 0 of 21. E_18: 0 of 10 |

## 9. Worked examples (computed by tool, not by hand)

The setting for all of them: 10 labels, K = 2 (r = 1/5, m = 5, so Powerball MAIN's bins), and 12 draws, oldest first: {1,2}, {3,4}, {1,5}, {2,6}, {1,7}, {3,8}, {1,9}, {2,10}, {4,5}, {1,6}, {3,7}, {1,8}. Small priors (c = 10, d = 2 and c = 2) are used so that the data visibly move the results.

- **Gaps:** label 1 has 2, 2, 2, 3, 2; label 2 has 3, 4; label 3 has 4, 5; labels 4 to 8 have one gap each (7, 6, 6, 6, 6); labels 9 and 10 have none.
- **Projected ages,** labels 1 to 10: 1, 5, 2, 4, 4, 3, 2, 1, 6, 5.
- **Exposures by age** 1 to 7: R = 22, 20, 15, 11, 7, 5, 1 and E = 0, 4, 2, 2, 1, 4, 1. The gap route and the per-draw route agree.

1. **E_2, mean:**
   - the scores are -6/11, -3/7, -5/9, -3/7, -1/3, -1/2, -2/3, -5/6, -1/5, 0;
   - label 10 scores 0: no gap, so c = m = 5, and its projected age is 5;
   - label 1, median: -1/2; label 1, mean of its last 2 gaps: -3/5.
2. **E_17, binned, c = 10:**
   - the bin hazards are 1/16, 1/5, 4/25, 5/28, 7/16, 1/5, 1/5 (no exposure reached the last two bins, so they stay at r);
   - label 9 (age 6, bin 6-8) scores highest, at 7/16.
3. **E_17, log-age sign:**
   - a_k for ages 1 to 7: -308, 44, -48, 8, -17, 254, 67 (n = 81 exposures, e = 14 events);
   - the prime exponents are e_2 = 314, e_3 = 206, e_5 = -17 and e_7 = 67, and n S_zy = 546.98 > 0, so sigma = +1: longest absent first;
   - the scores are the projected ages: label 9 first (6), then labels 2 and 10, tied (5).
4. **E_19, T = 2, c = 10, d = 2:**
   - the pooled phi is 448/379 (even ages) and 160/199 (odd ages);
   - label 1, drawn every second draw, has psi = 1.0524 (even) and 0.5233 (odd). Its projected age is 1, so its score is 0.0327, the lowest.
5. **E_18, c = 2,** weights (FAST, FAIR, SLOW, REGULAR):
   - label 1, (0.6589, 0, 0, 0.3411): rapid, even returns, score 0.2636;
   - label 2, (0.2131, 0, 0, 0.7869), score 0.2984;
   - labels 9 and 10 (no gaps), (0, 1, 0, 0) exactly, score 1/5.

The reference script asserts every exact value quoted here, the bin edges of the three real barrels, and the survival formulas against direct summation. The tests check the same values.

## 10. Verification inside each method (verify())

Each `verify()` recomputes by a differently written route and refuses any difference:
- **The helper's exposures:** a per-draw walk of ages, against the route built from completed gaps plus the open stretch.
- **E_2:** the mean by telescoping, (a_n - a_1)/(n - 1), against the sum of gaps; the median by counting, against sorting.
- **E_17:** bin sums from the per-age counts, against direct per-bin counting. The log-age sign by the prime-exponent route, against bounds on each ln k taken directly, without factorising; the two must agree. The ranking is checked to be the pure age ordering in the direction of sigma.
- **E_19:** the per-residue sums, against a per-exposure loop. The identity s_j / b(G_j) = psi is checked exactly.
- **E_18:**
  - the weights by an optimality certificate rather than a re-run: they are non-negative and sum to 1, and the gradient conditions (KKT) hold exactly at them;
  - each survival value by its closed form, against 1 minus the sum of the probabilities below it.

## 11. The package

**New files:**
- **the shared helper** `src/methods/_common/recurrence_gaps.py`, revision 1. It holds, exactly:
  - appearances, completed gaps, gaps inside a window and projected ages (sections 3.1 and 3.2);
  - exposures by age, by both routes;
  - the age bins;
  - the certified sign of an integer combination of logs (4.2), by both routes.

  It is named by all four methods (the shared-helper case; decision W2-1). It does not touch wave 1's `occurrence_counts.py`.
- **`src/methods/E_002/`, `E_017/`, `E_018/` and `E_019/`,** each with `__init__`, `variants.py`, `contract.py` and `IN_DEVELOPMENT.txt`;
- the 24 declarations and 24 entries (replacing nothing: the four methods' `NOT_YET_SPECIFIED` placeholders stay, as in wave 1);
- **tests:** `tests/test_recurrence_gaps.py` and `tests/test_wave2_recurrence.py`. They cover:
  - the worked examples and the bins of the three real barrels;
  - censoring, and the never-seen convention;
  - each variant's own setting, computed in the test;
  - the relations of section 7;
  - no peeking (T-05);
  - a contract run under a simulated release, the installed state refused, and the folder guards;
- this note and its reference script, and the template's draft 3 (section 12).

**Replaced:** `Method_Contract_Runner.py` gets four `ADAPTERS` lines; the template's three files become draft 3.

**Unchanged:** everything else, including E_1, E_3, E_4, E_6, wave 1, their helpers, the contract libraries, the reader and the coordinator.

**Release:** the same pattern as wave 1. The package installs non-runnable; releases come next, with WF-1.

## 12. Findings for the template (the owner's keep-current rule) and draft 3

This design found five things for the template. Draft 3 would add them, in the code package, as "things that bite" and checklist items:
1. **Published values must be byte-identical on Windows and Linux** (owner decision W2-7, after W2-O01). Exact arithmetic is preferred: an exact closed form, an exact finite search (E_18's 15 supports) or an exact certificate (E_3/E_4's alternation, E_18's KKT check, E_17's certified sign). An iterative floating-point fit is allowed only with objective proof of cross-platform byte identity and canonical output and tie rules. Library functions such as `log`, `exp` and `pow` may round differently between platforms.
2. **The sign trap**, a sibling of the same-count trap. When a score is a monotone function of one shared per-label quantity, with a fitted direction, the ranking depends only on that direction's sign. Shrinkage or rescaling that cannot flip the sign cannot change the ranking, so it is not a variant setting.
3. **Probe pooled methods with a planted single-label effect.** Pooling over labels dilutes an effect carried by one label (E_19's first form). Design the per-label route, or say why pooling is intended.
4. **Divide out what another method already measures** before claiming a new effect (E_19 divides out the age trend and the label's level), and check with a planted effect that the claim survives.
5. **Changing a covariate is not ranking-preserving** (W2-B01). Replacing a model's covariate by another increasing transform can reverse the fitted direction, and so the ranking. Claim that two forms are equivalent only with a proof, and search for a witness.

## 13. Owner decisions

- **W2-1 (RECOMMENDED): one shared gaps helper** for the four methods, versioned with them (as W1-1 and D34-1).
- **W2-2 (RECOMMENDED): the 12 variants of section 6,** with every setting fixed now. This is a scientific choice; the owner may prefer other windows, priors or cycles.
- **W2-3 (OWNER-DECIDED 30 October 2026, after EX_069): Method A becomes E_17 with Method A's own log-age rule (section 4.2), and its diagnostics come later.** The owner chose the faithful rule (EX_069's choice A) over keeping v0.1's harmonic slope as a renamed surrogate, or both.
  - **What E_17 keeps of Method A:**
    - the predictor, ranking exactly as Method A's (section 4.2);
    - the 52-draw burn-in;
    - the censoring rule;
    - tie-breaks without a lean towards low numbers;
    - the post-2018 data, through the contract's view;
    - the shape variants R1 asks of E_17.
  - **What is measured elsewhere:**
    - Method A's "run the predictor on simulated fair histories" is R3's N1 fair-draw simulator at WF-1. For E_17's match counts N1 is exact even though E_17 adapts (R3 section 17.5A).
    - Method A's diagnostics A1 to A5 (short-gap ratio, gap-distribution distance, hazard slope test, number variance, periodogram), with their 10,000-history simulated envelopes, become a separate "Method A diagnostics" package after WF-1. It needs the seed policy and the NIST root (reminder R-004), and a diagnostic report design.
  - **Not pursued:** Method A's decisions 3 and 4 (drawn order, machine and ball-set metadata). They would need new data sources, which the project's rules allow only by a separate owner decision, and never by contacting a lottery website.
  - **The options still open on the diagnostics' timing:** (b) build them in wave 2, which means settling R-004 now.
- **W2-4 (RECOMMENDED): all four score-only in revision 1** (section 5). The option: E_17's binned variants publish a renormalised marginal vector. That needs a stated renormalisation and a check that each value stays at most 1.
- **W2-5 (RECOMMENDED): E_18 as a fixed four-law library fitted by exact minimum chi-square** (section 4.4), not EM. The option: a fitted-component mixture as a later variant, which needs an exact or certified fitting route first.
- **W2-6 (RECOMMENDED): E_19 per label, with the trend and the label's level divided out, and cycles fixed at 2, 3 and 4,** never scanned. The option: pooled only (simpler, but probes show it misses a single-ball cycle).
- **W2-7 (OWNER-DECIDED 30 October 2026, after EX_069): the template's draft 3** with the five findings of section 12, in the code package, finding 1 in the byte-reproducibility wording of W2-O01.
- **W2-8 (RECOMMENDED): the NIST seed (R-004) is due at WF-1's design, not in wave 2.** N1 itself draws simulated fair outcomes, so WF-1 is the first part of the project that uses random numbers; the Method A diagnostics would follow.

## 14. Not in scope

Not in scope:
- real-data runs, walk-forward and scoring (WF-1, next);
- Method A's diagnostics (decision W2-3);
- any change to installed methods or the contract libraries;
- probability-publishing variants;
- wave 3 onward.

The gates and the orphan-marker rule apply unchanged.
