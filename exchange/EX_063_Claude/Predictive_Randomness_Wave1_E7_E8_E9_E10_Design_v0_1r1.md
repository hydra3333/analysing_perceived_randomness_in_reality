# Predictive Randomness - wave 1: E_7, E_8, E_9 and E_10 (frequency methods) and the template's draft 2, design note v0.1r1

**Document:** the method-level specification of the first variants of E_7, E_8, E_9 and E_10 (R2 v0.5 sections 7.1 and 7.7), with one shared counting helper, the design of the package that adds them, and the changes in the new-method template's draft 2.
**Version:** v0.1r1 DRAFT for the reviewer's focused RECHECK, 30 October 2026. It corrects only the ranking statement of section 1 (W1-C01, EX_062), and the reference script now prints and asserts the cap example (W1-O01). No formula, variant or setting changed. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule.
- **No code yet:** the code follows only after this design passes.
- **Probes:** feasibility probes on invented data are reported in section 8.
- **Base:** `main` at `919b580` (E_3/E_4 installed at `5b9edb4`; handovers and register v0.17 at `8defe9d`).
- **The owner's order of work** (30 October 2026; to be recorded in register v0.18): wave 1 is E_7, E_9, E_10 and E_8 with the template's draft 2. Then come wave 2 (E_2, E_17 as Method A, E_19, E_18), releases and WF-1, and wave 3.

## 1. In plain English

Four more ways of turning "how often has each number come up" into a ranking:
- **E_7 (Bayesian frequency shrinkage):** count each number's appearances over a recent window, but pull the estimate back towards the fair-draw rate, as if a year of perfectly fair draws had been added. A short lucky run then counts for less. It publishes chances.
- **E_9 (exponentially decayed rates):** count every past appearance, but let older ones fade quickly: half their weight after about a month, a quarter or half a year. It publishes scores, not chances.
- **E_10 (multi-horizon contrast):** compare each number's rate in the latest stretch with its rate in the stretch before it. TOP is the numbers rising fastest; WORST, the ones falling fastest. Scores, not chances.
- **E_8 (hierarchical rates across periods):** split the history into equal periods, and ask how much more the numbers' rates vary between periods than chance alone would make them. If they vary no more than chance allows, E_8 trusts each number's long-run rate. If they vary more, it leans towards the latest period, by exactly that much. It publishes chances.

**A design point found while specifying them.** Every number is at risk in every draw, so all numbers share the same number of draws. Any score given by the same strictly increasing function of each number's count over the same draws therefore has exactly the ranked groups of counting over those draws. The plain textbook versions of E_7 (a fixed-strength posterior mean) and E_8 (at weight 0) are such functions, so they would rank exactly like E_1. A plain E_9 at E_6's forgetting rates would rank exactly like E_6's decay variants. Count-only scores need not be monotonic in general, and this observation excludes no deliberately non-monotonic method.

So each method is specified to differ in ranking, or, where it does not, says so and differs in its probabilities (section 7):
- E_7 counts over a window;
- E_9 uses faster forgetting than E_6;
- E_10 compares two windows;
- E_8 learns its weighting from the data.

## 2. What is modelled

- **The observation:** for target N, barrel B (K of its L labels drawn per draw; fair rate r = K/L) and label j, x_i(j) = 1 if j was drawn at eligible draw i, else 0. The eligible draws are those before N, oldest first; the newest has age 0.
- **The view:** `UNORDERED_SET`, without dates.
- **Barrels:** Powerball has MAIN (K = 7, L = 35) and POWERBALL (K = 1, L = 20). Oz Lotto has MAIN only (K = 7, L = 47). The formulas below are the same for every barrel, with r = K/L.
- **Minimum history:** stated per variant (section 6). Earlier targets get the contract's `INSUFFICIENT_HISTORY` record, as for E_3/E_4.

## 3. The rules

W is the number of eligible draws, k_j(S) the count of j in the newest S draws, and k_j the count over all W.

**3.1 E_7, Beta shrinkage over a window.** With window M (or all W draws) and prior strength c:

  s_j = (c r + k_j(M)) / (c + M)

This is the posterior mean of a Beta(c r, c(1 - r)) prior updated by the window's counts, the model E_6 uses with c = 1 and no window.
- **Normalisation, exact:** sum over j of s_j = (c L r + K M)/(c + M) = K. So MAIN's values are a marginal-inclusion vector summing to 7 (or Oz's 7), and the POWERBALL's a categorical vector summing to 1.
- **Each value is strictly between 0 and 1.**

**3.2 E_9, exponentially decayed counts.** With factor lambda in (0, 1):

  s_j = sum over eligible draws i of lambda^age(i) x_i(j)

The newest draw weighs 1, and the sum runs over all W draws. Normalising by the sum of the weights would not change the ranking, so the raw weighted count is the score. No probability vector is published (R2: "scores/ranks, not automatically probabilities"). E_6's decay variants already publish the Bayesian chances at slower forgetting.

**3.3 E_10, two-window contrast.** With a short window S inside a long window Lw (Lw > S; or all W draws):

  s_j = k_j(S)/S - (k_j(Lw) - k_j(S))/(Lw - S)

That is the rate in the newest S draws minus the rate in the Lw - S draws before them. The two stretches are disjoint, so under fair draws they are independent.
- **Why the raw difference:** dividing by the fair-draw standard deviation, sqrt(r(1 - r)(1/S + 1/(Lw - S))), is the same for every label, so it would not change the ranking. The raw difference is exact.
- **Readouts:** TOP is the fastest risers; WORST, by the contract's `INVERSE`, the fastest fallers.
- Scores only: a difference of rates is not a chance.

**3.4 E_8, hierarchical rates across periods (beta-binomial, method of moments).** The newest n*P draws are split into n = floor(W/P) consecutive periods of P draws, counted back from the newest, so the latest period is always complete. Any older remainder is not used.

For label j, the period rates are p_{j,b} = (count of j in period b)/P, for b = 1..n, with b = n the latest. Then:
- **m_j**, the mean of the p_{j,b}, and **V_j**, their unbiased sample variance (dividing by n - 1);
- **the per-label excess variance:** t_j = (V_j - (m_j(1 - m_j) + V_j/n)/P) * P/(P - 1);
- **the pooled excess:** t = mean over j of t_j, clamped to the range [0, r(1 - r)];
- **the weight:** w = P t / ((P - 1) t + r(1 - r)), which lies in [0, 1];
- **the score:** s_j = w p_{j,n} + (1 - w) m_j.

**Why this form.** If each period's true rate theta varies around a number's long-run rate with variance tau^2, then:
- Var(p) = tau^2 + (mu(1 - mu) - tau^2)/P, and E[m(1 - m)] = mu(1 - mu) - Var(p)/n;
- t_j is the corresponding moment estimate of tau^2, pooled over labels, the hierarchy's "shared across labels" level;
- w is the beta-binomial shrinkage weight of the latest period towards the long-run rate, with mu(1 - mu) replaced by the fair-draw r(1 - r), so that w is the same for every label.

**What the result means.**
- **No excess variation** (t = 0): w = 0, and E_8 ranks by each number's long-run rate over the n*P draws.
- **Excess variation:** w > 0, and E_8 leans towards the latest period.
- **Normalisation, exact:** each period holds exactly K*P selections, so sum_j p_{j,b} = K for every b. Hence sum_j m_j = K and sum_j s_j = K. Each s_j is in [0, 1].
- **What is published:** a marginal-inclusion vector (MAIN) or a categorical vector (POWERBALL). It is marginals only, not a joint law over seven-number sets (R1's caution about the without-replacement link); the calibration note says so.
- **The name:** R2 calls E_8 "Dirichlet-multinomial". Per label, a Dirichlet's marginal is a Beta, so the per-label beta-binomial over periods is that hierarchy's marginal form. The estimates are moment estimates, not a full Bayesian fit.

## 4. Outputs, per barrel (E2R-1 sections 5 and 7)

**Every channel:**
- `RANKING_WITH_SCORES`, `FLOAT64`;
- TOP `TOP_MARGINAL`, WORST `INVERSE`, `TOP_MARGINAL_AND_INVERSE_V1`;
- `TIE_SHA256_V1`.

**Every declaration:** no diagnostic record; deterministic (`stochastic_fit` false, no seed); `IS_NOT_APPLICABLE`; Oz Lotto MAIN only.

| Method | Probability kind (MAIN / POWERBALL) | Sum tolerance | `fit_sampling_model_version` |
|---|---|---|---|
| E_7 | `MARGINAL_INCLUSION_PROBABILITY` / `PB_CATEGORICAL` | 1e-12 | `BETA_SHRINKAGE_WINDOW_V1` |
| E_8 | `MARGINAL_INCLUSION_PROBABILITY` / `PB_CATEGORICAL` | 1e-12 | `HIER_BETA_BINOMIAL_PERIODS_MOM_V1` |
| E_9 | `NONE` | - | `EXP_DECAYED_COUNT_V1` |
| E_10 | `NONE` | - | `TWO_WINDOW_RATE_CONTRAST_V1` |

**Calibration notes, in the registry texts:**
- E_7's and E_8's values are model-based estimates, not tested for calibration, and ignore that the seven main numbers are drawn together.
- E_9's and E_10's scores are not chances.
- Each method is not expected to beat chance if the draws are fair.

## 5. Exactness and platform identity

Everything is integers and fractions until each published value is rounded once to float64, as in E_6 and E_3/E_4.
- **E_9's powers** lambda^age are exact fractions, as E_6's are; the probe of section 8 times them.
- **E_8** needs no square root: the weight is rational.
- **Probability vectors** (E_7, E_8): their exact sums are exactly K; the rounded floats sum to K within 1e-12, which the contract checks.

## 6. The variants (fixed in revision 1)

All in both games. "Min" is `minimum_history_draws`.

| Method | `variant_id` | Settings | Min | Meaning |
|---|---|---|---|---|
| E_7 | `BETA_SHRINK_W52_C52_V1` | M = 52, c = 52 | 52 | last year, shrunk halfway to fair |
| E_7 | `BETA_SHRINK_W104_C52_V1` | M = 104, c = 52 | 104 | last two years, shrunk a third of the way |
| E_7 | `BETA_SHRINK_FULL_C52_V1` | all W, c = 52 | 1 | full history, heavy shrinkage early on (see section 7) |
| E_9 | `EXP_DECAY_5_6_V1` | lambda = 5/6 | 1 | half-life about 3.8 draws (a month) |
| E_9 | `EXP_DECAY_18_19_V1` | lambda = 18/19 | 1 | about 12.8 draws (a quarter) |
| E_9 | `EXP_DECAY_37_38_V1` | lambda = 37/38 | 1 | about 26.0 draws (half a year) |
| E_10 | `CONTRAST_S13_L104_V1` | S = 13, Lw = 104 | 104 | the latest quarter against the 91 draws before it |
| E_10 | `CONTRAST_S26_L208_V1` | S = 26, Lw = 208 | 208 | the latest half-year against the 182 before |
| E_10 | `CONTRAST_S52_FULL_V1` | S = 52, Lw = all W | 104 | the latest year against all earlier draws |
| E_8 | `HIER_PERIODS_P13_V1` | P = 13 | 26 | quarters |
| E_8 | `HIER_PERIODS_P26_V1` | P = 26 | 52 | half-years |
| E_8 | `HIER_PERIODS_P52_V1` | P = 52 | 104 | years |

**Notes on the settings:**
- **E_9's factors** lambda = 1 - 1/tau with tau = 6, 19 and 38. They are chosen to stay clear of E_6's 74/75 and 149/150 (half-lives about 51.6 and 103.6 draws).
- **The count:** 4 methods x 3 variants x 2 games = 24 declarations and 24 `FORMULA_OPEN` entries.

## 7. Relation to other methods (honest overlap; template section 8)

- **E_7 `BETA_SHRINK_FULL_C52_V1`:** ranks exactly as E_1, apart from the order within exact ties, since `TIE_SHA256_V1` includes the method and variant. Its difference is in its probabilities: a prior worth a year of fair draws, against E_6's prior worth one draw. R3's probability scores (log loss, Brier) are what tell them apart. It is kept as the pure calibration variant (owner decision W1-3).
- **E_7's window variants** rank by the window's count, which is also the ranking E_10's short-window rate would give on its own. E_10 subtracts the earlier rate, so it ranks differently.
- **E_9** ranks exactly like E_6's discounted update at the same lambda. Its factors are chosen not to coincide with E_6's.
- **E_8** with w = 0 ranks by the count over the newest n*P draws (E_1's ranking when n*P = W). In fair-draw probes, w is 0 at many targets and small at the rest (section 8). E_8's ranking departs from counting only to the degree the data show excess variation between periods.
- **E_10** is the only one of the four whose ranking depends on two windows with opposite signs.

The tests check each claimed relation, comparing `ranked_groups`, not TOP and WORST.

## 8. Feasibility and behaviour (author probes; invented fair draws, never real data)

- **E_9's exact powers** over 433 draws for 35 labels: fast (the E_6 precedent).
- **E_8 on fair invented draws,** every 7th target:

  | P | w > 0 at | mean w | largest w |
  |---|---|---|---|
  | 13 | 17 of 59 targets | 0.005 | 0.077 |
  | 26 | 31 of 55 | 0.037 | 0.256 |
  | 52 | 13 of 47 | 0.019 | 0.147 |

  Each run takes about 0.1 s in exact fractions.
- **E_8 with a genuine drift planted** (P = 26; chosen numbers made to appear in about half of the last 52 draws instead of a fifth):
  - one drifting number: w = 0.149, and that number ranks first;
  - seven drifting numbers: w = 0.372, and they take ranks 1 to 7.

  The weight responds to real excess variation and stays near zero without it.

## 9. Worked examples (computed by tool, not by hand)

The setting for all of them: 5 labels, K = 2 (r = 2/5), four draws oldest first: {1,2}, {1,3}, {2,4}, {1,5}.

1. **E_7, M = 2, c = 2:** the window holds {2,4} and {1,5}, so k = 1 for labels 1, 2, 4 and 5, and 0 for label 3.
   - The scores are 9/20, 9/20, 1/5, 9/20, 9/20; the sum is 2.
   - The same with all four draws: 19/30, 7/15, 3/10, 3/10, 3/10.
2. **E_9, lambda = 1/2:** 11/8, 5/8, 1/4, 1/2, 1.
3. **E_10, S = 2, Lw = 4:** -1/2, 0, -1/2, 1/2, 1/2.
4. **E_8, P = 2:** the per-label excesses are 0, -1/4, 0, 0, 0. Their mean, -1/20, is clamped to t = 0, so w = 0, and the scores are the long-run rates 3/4, 1/2, 1/4, 1/4, 1/4 (sum 2).
5. **E_8 at its cap.** 4 labels, K = 2 (r = 1/2), P = 2, six draws: {2,4}, {2,4}, {2,4}, {1,2}, {1,3}, {1,3}.
   - t = 1/4 = r(1 - r), the upper clamp, so w = 1.
   - The scores are the latest period's rates: 1, 0, 1, 0.

The reference script that computed these travels with this note. The tests check every value exactly.

## 10. Verification inside each method (verify())

Each `verify()` recomputes by a differently written route and refuses any difference:
- **E_7:** the posterior built by sequential updates, one draw at a time, against the closed form.
- **E_9:** the recursion s <- lambda s + x, against the direct sum of powers.
- **E_10:** prefix sums, against direct window counts.
- **E_8:** the variance by the sum-of-squares formula in integer counts, against the two-pass formula in rates. The sum identities also hold exactly: sum_j s_j = K, and each period sums to K*P.

## 11. The package

**New files:**
- **the shared helper** `src/methods/_common/occurrence_counts.py`, revision 1. It holds, exactly:
  - per-label counts over the newest S draws;
  - decayed weighted counts, with their recursion;
  - period counts counted back from the newest draw.

  It is named by all four methods (the template's shared-helper case; owner decision W1-1).
- **`src/methods/E_007/`, `E_008/`, `E_009/` and `E_010/`,** each with `__init__`, `variants.py`, `contract.py` and `IN_DEVELOPMENT.txt`;
- the 24 declarations and 24 entries;
- **tests:** `tests/test_occurrence_counts.py` and `tests/test_wave1_frequency.py`. They cover the worked examples, exact normalisation, each variant's own setting computed in the test, the claimed relations of section 7, no peeking (T-05), a contract run under a simulated release, the installed state refused, and the folder guards;
- this note, and the template's draft 2.

**Replaced:** `Method_Contract_Runner.py` gets four `ADAPTERS` lines.

**Unchanged:** everything else, including E_1, E_3, E_4, E_6 and their helpers. E_6's `beta_bernoulli.py` is not refactored onto the new helper: E_6 is installed revision 1.

**Release:** the same pattern as E_6 and E_3/E_4. The package installs non-runnable; releases come later, in the owner's order (after wave 2, with WF-1).

## 12. The template's draft 2 (owner decision W1-5)

**Draft 2 folds in what E_3/E_4 taught,** which their design note listed, and this design's findings. The README and the specification template change; the code skeletons change in the code package, proved there by the template trial.

**In the README:**
1. **The shared-helper case:** a helper in `_common/` with its own tests, named by every method that uses it. A change to it is a new revision of every user (E2R-R14A).
2. **The score-only case:** `probability_kind` `NONE`, no `ProbabilityVector`, and the reason stated.
3. **The minimum-history case:** return an empty `MethodOutput`, so the contract records `INSUFFICIENT_HISTORY`; verify() accepts it.
4. **Several methods in one package:** one helper, one generator for all the declarations, one test module per family plus the helper's tests.
5. **New "things that bite":**
   - the same-count ranking trap of section 1;
   - check a new method's ranking against E_1 and against same-family methods before claiming it differs;
   - plan one planted defect per variant setting and per verification rule (E_6 and E_3/E_4 each found a gap this way);
   - compute every worked example with a tool;
   - never ask the Claude Code runner to count output.
6. **The owner's rule (30 October 2026):** the template is kept up to date whenever findings, Claude's or the reviewer's, warrant it, and each method's handback says whether it found anything for the template.

**In the specification template:** section 8, "relation to other methods", gains an explicit question: does any variant rank exactly like an existing method? If so, what distinguishes it?

## 13. Owner decisions

- **W1-1 (RECOMMENDED): one shared counting helper** for the four methods, versioned with them (as D34-1).
- **W1-2 (RECOMMENDED): the 12 variants of section 6,** with every setting fixed now. This is a scientific choice; the owner may prefer other windows, strengths or half-lives.
- **W1-3 (RECOMMENDED): keep E_7's full-history variant** although it ranks like E_1, as the pure calibration variant. Its point is its probabilities.
  - The option: drop it, leaving E_7 with two variants.
- **W1-4 (RECOMMENDED): E_9 and E_10 score-only; E_7 and E_8 publish marginal probabilities** (section 4), with their limits stated.
- **W1-5 (RECOMMENDED): the template's draft 2** as in section 12, reviewed in this round.
- **W1-6 (RECOMMENDED): E_8's moment-estimate form** (3.4), rather than a full Bayesian fit. A full fit would need a sampler, and so a seed policy and the NIST root (D-9..D-11). It could be a later variant if wanted.

## 14. Not in scope

Not in scope:
- real-data runs, walk-forward and scoring (WF-1, after wave 2);
- any change to E_1, E_3, E_4, E_6 or the contract libraries;
- full Bayesian or sampled versions of E_7 or E_8;
- wave 2 onward.

The gates and the orphan-marker rule apply unchanged.
