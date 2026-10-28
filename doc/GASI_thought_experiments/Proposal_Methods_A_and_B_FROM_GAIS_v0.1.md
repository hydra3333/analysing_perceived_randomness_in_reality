# Proposal: Methods A and B - candidate experiments derived from an external thought-experiment discussion

- Document: Proposal_Methods_A_and_B_v0.1.md
- Version: v0.1 (PROPOSAL - not ratified)
- Date: 2026-10-28
- Prepared by: Claude, in an independent advisory chat (not the main project chat)
- Prepared for: the GitHub project owner (hydra3333), for later consideration by the main project chat
- Intended timing: after the current implementation package is complete; not intended to interrupt it
- Authority: where anything here conflicts with ratified project documents, the ratified documents prevail. This document does not know the project's experiment interface in detail; mapping onto that interface is left to the main project chat.

---

## 0. Purpose and scope

The project owner asked an external AI assistant (referred to below as GAIS; source file `GASI_thought_experiments_possibly_unexplored_areas.md`) for unconventional ways to probe whether Australian Powerball draws are random in the conventional sense. GAIS offered four frameworks plus a four-phase blueprint. The owner found two of them interesting:

- Framework 1: Riemann zeta zeros, random-matrix theory and "level repulsion".
- Framework 3: non-linear dynamics, Takens' delay embedding and attractor reconstruction.

This document turns those two into concrete, low-cost candidate methods:

- They fit a project whose methods produce next-draw predictions, are measured walk-forward, and are judged against fair-draw baselines.
- They avoid excessive coding: each method is roughly 200-450 lines of Python, numpy/scipy only.
- They avoid long runtimes: minutes on a Ryzen 9 3900X, well inside the stated budget of half an hour to an hour.

It records:

- where each idea comes from;
- what GAIS got wrong and has been corrected here;
- exactly how each method would be measured;
- what to expect and what to watch for.

In keeping with the project premise, unlikely methods are not dismissed in advance. They are given a fair, cheap, well-controlled test.

---

## 1. Summary of the two methods

### Method A - "Recurrence-gap spectrum: do ball numbers repel or cluster across weeks?"

**How it works**

- Each ball number (1-35 main, 1-20 Powerball) has its own history of the weeks in which it was drawn.
- Treat each history like the "energy levels" or "zeta zeros" studied in random-matrix theory.
- Ask whether a number that has just appeared is less likely to reappear soon ("repulsion", the Riemann/random-matrix signature) or more likely ("clustering"), compared with fair draws.
- Also ask whether appearances are more regular or more bunched over longer windows than fair draws allow.

**Prediction:** a fitted "chance of appearing next week, given weeks since last appearance" curve ranks the numbers. The top 7, plus the top Powerball, are the prediction.

**Under fair draws:** the curve is flat and the method has no edge.

### Method B - "Delay-embedding analogues and forbidden patterns: is there week-to-week dynamical memory?"

**How it works**

- Build a "recent situation" from the last few weeks of draws.
- Find the past weeks whose recent situation most resembled it, and use what followed them as the prediction. This is the method of analogues, the practical predictive form of Takens' theorem.
- Separately, check whether certain up/down orderings of consecutive weekly values never occur ("forbidden ordinal patterns"). Such patterns are a fingerprint of deterministic dynamics that random sequences do not leave.

**Prediction:** the weighted votes of the analogue weeks' successors rank the numbers. The top 7, plus the top Powerball, are the prediction.

**Under fair draws:** past situations carry no information about the future and the method has no edge.

---

## 2. Shared provenance and what was changed from the source

### 2.1 Origin

Both methods come from the GAIS response in `GASI_thought_experiments_possibly_unexplored_areas.md`, specifically:

- Framework 1 (Riemann Hypothesis, random-matrix theory and quantum chaos) and its Phase 1 (spacing test, Brody distribution).
- Framework 3 (Takens' embedding and attractor reconstruction) and its Phase 3 (Bandt-Pompe permutation entropy, forbidden patterns).
- Phase 4 (surrogate-data testing), which is adopted for both.

### 2.2 Corrections to the source (recorded so they are not carried into any spec)

1. **Within-draw spacing test (GAIS Phase 1) is rejected as constructed.**
   - Balls are drawn without replacement from whole numbers, so two balls in the same draw can never be closer than 1 apart.
   - Normalised spacings therefore can never be near zero. Any fitted curve will show "repulsion" whatever the physics.
   - With only 6 integer gaps per draw, the "unfolding" step GAIS describes has no meaning.
   - Method A replaces this with an across-time construction (section 3.4) that has an exact, artefact-free null.
2. **Brody parameter mislabelled.**
   - GAIS says a Brody parameter near 1 indicates "Riemann zeros / GUE".
   - Brody parameter 1 reproduces the Wigner surmise for the orthogonal ensemble (GOE, linear repulsion). It does not reproduce the unitary ensemble (GUE, quadratic repulsion), which is the one matching the zeta zeros.
   - The GUE formula GAIS quotes, P(s) = (32/pi^2) s^2 exp(-4 s^2 / pi), is itself correct, but it is not the Brody-1 case.
3. **No mechanism links the Riemann Hypothesis to lottery predictability.**
   - The Montgomery-Odlyzko result is a statistical resemblance between zeta zeros and random-matrix eigenvalues.
   - Nothing about it can be "applied" to predict draws.
   - What can be borrowed is the toolkit: spacing statistics, number variance, rigidity and form factor. Method A uses only that toolkit.
4. **Correlation-dimension estimation (GAIS Framework 3) is excluded.**
   - With N data points, the largest correlation dimension that can be credibly estimated is roughly 2 x log10(N) (Eckmann and Ruelle, 1992). That is about 5 for the ~446 draws in the current format.
   - A "finite fractal dimension" found at this sample size would be untrustworthy.
   - Method B uses analogue forecasting and ordinal patterns instead. Both are designed for short series.
5. **Smaller slips.**
   - "Solovay-Strassen" (GAIS Framework 4) is a primality test, not a normality test.
   - GAIS's draw count of ~1,040 over 20 years ignores the format change. Only the post-April-2018 draws are comparable (section 5.1).

### 2.3 What was deliberately left out

- **Framework 2 (de Broglie-Bohm pilot waves, quantum non-equilibrium):** no observable in weekly lottery results could distinguish it from classical chaos.
- **Framework 4 (algorithmic information, normality in all bases):** needs far more data than exists. With ~446 draws it reduces to ordinary frequency tests.
- **Phase 2 (topological data analysis, persistent homology):**
  - Heavier dependencies (ripser or giotto-tda) and more compute.
  - Persistence diagrams of ~446 points in 7 dimensions are dominated by sampling noise.
  - It could be revisited later if the owner wants it, but it is not proposed here.

---

## 3. Method A - Recurrence-gap spectrum

### 3.1 One-line title

Recurrence-gap spectrum: do ball numbers repel or cluster across weeks?

### 3.2 Provenance

- **H. Montgomery (1973):** derived the pair-correlation function of the Riemann zeta zeros. F. Dyson recognised it as the pair correlation of eigenvalues of random unitary (GUE) matrices.
- **A. Odlyzko (1987 onward):** confirmed this numerically to extraordinary precision for very high zeros.
- **E. Wigner and F. Dyson (1950s-60s):** random-matrix theory as a model for energy levels of heavy nuclei. Eigenvalues "repel": small spacings are suppressed.
- **O. Bohigas, M.-J. Giannoni and C. Schmit (1984):** the conjecture that quantum systems with chaotic classical counterparts show random-matrix level statistics, while integrable systems show Poisson (independent) statistics.
- **T. Brody (1973):** a one-parameter spacing distribution interpolating between Poisson and the Wigner (GOE) surmise.
- **Standard spectral statistics:** nearest-neighbour spacing distribution, number variance Sigma^2(L), Dyson-Mehta spectral rigidity Delta_3(L), and the spectral form factor (Fourier-domain correlation).

The idea borrowed is diagnostic. Random-matrix statistics give a well-developed vocabulary for whether events along a line are:

- independent (Poisson-like),
- mutually avoiding (repulsion, rigidity), or
- bunched (clustering).

Applied to "when does ball number n come up", that vocabulary becomes a sharp randomness test with an exact null.

### 3.3 Why the within-draw version is not used

See section 2.2 item 1. Constraints of the game rules, not physics, would produce the effect GAIS proposed to look for.

### 3.4 Construction (adopted)

1. **Data:** post-format draws only (Draw 1144, 19 April 2018, onward; section 5.1).
2. **Indicator histories.** For each main number n in 1..35, build a 0/1 series I_n(t) over draws t = 1..N, where I_n(t) = 1 if n was drawn in draw t. Do the same for each Powerball number m in 1..20 using the Powerball barrel only.
3. **Event "spectrum":** the draw indices where I_n(t) = 1. The gaps are the differences between consecutive indices (gap >= 1; gap = 1 means consecutive weeks).
4. **Exact null for a single number.**
   - Under fair draws, I_n(t) is independent Bernoulli(p) across draws, with p = 7/35 = 0.2 for main numbers and p = 1/20 = 0.05 for Powerball numbers.
   - Gaps are therefore exactly geometric: P(gap = k) = p (1 - p)^(k - 1).
   - "Unfolding" is trivial: the mean gap is 1/p (5 draws main, 20 draws Powerball) and the rate is constant.
5. **Pooled statistics.** Across numbers, the series are not independent, because each draw contains exactly 7 main numbers. Pooled statistics therefore take their null from Monte Carlo simulation of the real game (section 5.2), not from a formula.
6. **Expected volume (to ~Oct 2026, ~446 draws):**
   - Main: about 89 appearances per number, about 88 internal gaps each, about 3,080 pooled gaps.
   - Powerball: about 22 appearances per number, about 420 pooled gaps.
7. **Censoring.** The stretch before a number's first appearance and the stretch since its last appearance are incomplete gaps.
   - Pre-declare: exclude them from gap-distribution statistics.
   - Include the current open gap only as the predictor input (section 3.6).

### 3.5 Diagnostic statistics (pre-declared)

All are computed separately for the main barrel (pooled over 35 numbers) and the Powerball barrel (pooled over 20 numbers). Each is compared with the same statistic on at least 10,000 simulated fair histories of identical length.

- **A1. Short-gap ratio (primary).**
  - The observed fraction of gaps equal to 1, compared with the null (p: 0.2 main, 0.05 Powerball).
  - A deficit means repulsion (the random-matrix-like direction). An excess means clustering.
  - Also report gaps of 2 and 3 as secondary.
- **A2. Gap-distribution distance.**
  - A single goodness-of-fit distance between the pooled gap histogram and the geometric law, for example chi-square over bins 1, 2, 3, 4-5, 6-8, 9-13, 14+ for main.
  - Its p-value comes from the simulated envelope, not chi-square tables.
- **A3. Hazard profile.**
  - h(k) = P(number appears at gap k | it has not appeared for k - 1 draws). This is flat at p under the null.
  - Fit one slope, a logistic regression of appearance on log(gap) pooled across numbers.
  - Slope < 0: the longer since last seen, the less likely (clustering/"hot").
  - Slope > 0: the longer since last seen, the more likely (repulsion/"due").
- **A4. Number variance Sigma^2(L) (primary).**
  - For window lengths L = 5, 10, 20, 50 draws (pre-declared, overlapping windows), compute the variance of a number's appearance count across windows, averaged over numbers.
  - The null per number is exactly binomial: L x p x (1 - p).
  - Below null means more regular than chance (rigidity, the random-matrix signature, which grows only logarithmically with L). Above null means bunching.
  - Report the ratio observed/null for each L against the simulated envelope.
- **A5. Form factor / periodicity (secondary, optional).**
  - Compute the periodogram of each centred indicator series, normalise and average across numbers, then test the largest peak against the simulated envelope.
  - This is the closest cheap analogue of the spectral form factor.
  - Physical hook: if ball sets or draw machines rotate on a fixed cycle and one set or machine is slightly biased, a peak at that period is the expected signature (section 3.9).

### 3.6 Predictor

For each target draw t + 1, using only draws 1..t (strict walk-forward):

1. **Fit the hazard model** of A3 on draws 1..t, pooled across numbers, separately for each barrel.
   - Two parameters (intercept and slope on log gap), with mild shrinkage toward the null (slope 0) so early fits on little data do not swing wildly.
   - Pre-declare the shrinkage, for example a ridge penalty fixed in advance.
2. **Compute each number's current open gap** g_n (draws since last appearance).
3. **Score each number** by predicted probability h(g_n + 1).
4. **Pick** the top 7 main numbers and the top Powerball number.
   - Ties are broken by a seeded random draw, with the seed recorded.
   - Do not break ties by lowest number: that silently biases toward low numbers.
5. **Burn-in.** No predictions before a pre-declared minimum history, for example 52 draws (one year). Before that the hazard fit is mostly noise.

The sign of any effect is learned from the data, not chosen by hand. If the fitted slope is about 0, the picks are effectively random, which is the correct null behaviour.

This predictor is the formal, testable version of the folk "hot numbers" and "due numbers" beliefs. A clean null result is itself informative: it tests the gambler's-fallacy claims directly.

### 3.7 Measurement within the project

- **Predictions:**
  - One prediction record per target draw, produced walk-forward.
  - Scored by the project's existing scoring (matches, prize-division equivalents) exactly as other methods are.
- **Baselines:**
  - Under fair draws, 7 picks from 35 match on average 7 x 7/35 = 1.4 main numbers (hypergeometric). The Powerball matches with probability 0.05.
  - Compare the method's score with these expectations and with the score distribution obtained by running the identical predictor on simulated fair histories. This null includes any selection or fitting artefacts.
- **Diagnostics:** A1-A5 are reported as randomness-test outputs, separate from prediction scores, each with its simulated-envelope p-value or z-score.
- **Real-world forward predictions:** once the method is frozen, its next-draw predictions join the project's forward predictions. They are the test that counts.

### 3.8 Effort and runtime

- **Code:**
  - About 200-300 lines: indicator building, gap extraction, A1-A5, hazard fit, predictor.
  - It reuses the shared fair-draw simulator (section 5.2).
- **Dependencies:** numpy, scipy.
- **Runtime:**
  - The diagnostics on 10,000 simulated histories take seconds; the indicator arithmetic is about 10^8 operations, vectorised.
  - The walk-forward predictor null (about 1,000 simulated histories x about 400 refits each) takes a few minutes if the hazard fit is kept cheap (closed-form or a few Newton steps on a two-parameter model).
  - Well under the half-hour budget.

### 3.9 Expectations and things to watch

- **Expected outcome:** null. Mechanically mixed balls drawn weekly have no known way to "remember" last week's numbers.
- **What the data could detect (rough):**
  - With ~3,080 main gaps, the standard error of the short-gap ratio is about sqrt(0.2 x 0.8 / 3080), about 0.007.
  - A shift of about 0.02 (a 10% relative change) would reach about 3 sigma.
  - Such an effect would raise expected main matches only from 1.40 to about 1.5 per draw, which is detectable over ~400 walk-forward draws at best marginally.
  - Any real effect is expected to be small.
- **Things to watch:**
  - *Era mixing:* never pool the pre-2018 formats into these statistics (section 5.1).
  - *Censoring handling* (section 3.4 item 7). Getting it wrong biases A1 and A2.
  - *Powerball sparsity:* ~420 gaps give much weaker tests than the main barrel. Expect wide envelopes.
  - *Cross-number dependence:* never use per-number binomial formulas for pooled p-values. Use the simulator.
  - *Cherry-picking:* do not report "number 17 is clustered" findings from 35 per-number tests without correction. The pre-declared statistics are pooled.
  - *Physical covariates:*
    - The current format was introduced with two Smartplay Halogen II draw machines (per public sources).
    - If per-draw machine or ball-set identity is available from any official source, record it as a covariate.
    - A real bias tied to one machine or one ball set would appear as periodicity (A5) or as a split between machine-specific subsets.
    - This is the single most plausible route to a genuine non-random finding, and it is a mechanical one, not an exotic one.

---

## 4. Method B - Delay-embedding analogues and forbidden ordinal patterns

### 4.1 One-line title

Delay-embedding analogues and forbidden patterns: is there week-to-week dynamical memory?

### 4.2 Provenance

- **N. Packard, J. Crutchfield, J. D. Farmer and R. Shaw (1980); F. Takens (1981):** the state of a deterministic dynamical system can be reconstructed, up to a smooth change of coordinates, from delayed copies of a single observed quantity (delay embedding).
- **P. Grassberger and I. Procaccia (1983):** the correlation dimension. **J.-P. Eckmann and D. Ruelle (1992):** its data-size limits (section 2.2 item 4).
- **E. Lorenz (1969):** the method of analogues. Forecast by finding past states similar to the present one and seeing what followed.
- **G. Sugihara and R. May (1990):** simplex projection. Analogue forecasting in a delay embedding, used specifically to distinguish deterministic chaos from noise in short series. Later, S-maps test for state-dependent non-linearity.
- **C. Bandt and B. Pompe (2002):** permutation entropy, from the ordinal patterns of consecutive values.
- **J. Amigo, S. Zambrano and M. Sanjuan (2007):** "true and false forbidden patterns".
  - Deterministic systems have ordinal patterns that can never occur.
  - In random series a missing pattern is only a finite-sample accident.
- **L. Zunino and colleagues (2017):** tied values (equal consecutive values) can create spurious forbidden patterns and false conclusions.
- **J. Theiler and colleagues (1992):** surrogate-data testing for non-linearity.

The idea borrowed is this. If the weekly draw carried any deterministic memory, Takens says it is in principle recoverable from the observed series. The tools that work at small N are analogue forecasting and ordinal patterns, not dimension estimates.

### 4.3 Why correlation dimension is not used

See section 2.2 item 4.

### 4.4 Series (pre-declared; keep to this list)

- **S1 - Powerball value**, 1..20. Scalar. Many ties (section 4.6).
- **S2 - Sum of the 7 main numbers**, 28..224; null mean 126, null standard deviation about 24.2. Scalar, few ties. Diagnostic only; it does not map to picks.
- **S3 - Whole main draw as a 35-bit set.** Used for analogue forecasting of main picks.
- **S4 - Drawn-order series** (conditional on data availability; section 5.6), for example the first-drawn main ball. Physically the most meaningful series for dynamics. Include only if drawn order can be scraped reliably for the whole post-2018 era.

No other series without a recorded decision. Each added series is another chance for a false positive (section 5.3).

### 4.5 B1 - Analogue forecasting (simplex projection) - predictor

**For S3 (main picks)**

1. **State at draw t:** the last E draws as E 35-bit sets.
   - Pack each draw into one 64-bit integer.
   - Hamming distance is then popcount(xor), summed over the E draws.
2. **Library for target t + 1:** all past (state at s, draw at s + 1) pairs with s + 1 <= t. This is strict walk-forward with no look-ahead.
3. **Neighbours:** the k = E + 1 nearest library states. Ties at the boundary distance are included with equal fractional weight, or by seeded random selection; pre-declare which.
4. **Votes:** each neighbour's successor draw votes for its 7 numbers, weighted exp(-d / d_min), the Sugihara-May weighting (guard against d_min = 0).
5. **Pick** the top 7 by weighted vote. Ties are broken by seeded random draw.

**For S1 (Powerball pick):** the same method on the scalar S1 delay vector (S1(t), S1(t-1), ..., S1(t-E+1)), with Euclidean distance. Neighbours' successor Powerball values vote; pick the top value.

**Settings**

- Primary setting pre-declared as E = 2, tau = 1 (consecutive weeks).
- Also report E = 1, 3 and 4 in full as secondary, never selecting the best after the fact.
- Burn-in: no predictions before 52 draws.

**Skill measures**

- For prediction: the project's standard scoring, as for Method A.
- For the dynamics diagnosis on S1 and S2 (the Sugihara-May test):
  - the correlation rho between predicted and actual values;
  - mean absolute error relative to the naive "training mean" forecast.
- Report skill against E (and against forecast horizon 1-3 draws). A genuinely deterministic system shows skill that declines with horizon; noise shows none at any horizon.

**Optional (secondary): S-map on S2**

- Test whether skill improves as the locality parameter theta rises above 0.
- Improvement indicates state-dependent (non-linear) dynamics.
- Include only if cheap to add once B1 exists.

**An expected weakness, recorded in advance**

- Two fair 7-from-35 draws share on average 1.4 numbers, so Hamming distances cluster tightly around 11.
- "Nearest" past states are therefore barely nearer than random ones. This is the curse of dimensionality, and it is why E is kept small.
- If B1 shows no skill, this weakness is part of the honest interpretation. If it does show skill, leakage is the first suspect (section 4.9).

### 4.6 B2 - Forbidden ordinal patterns - diagnostic

1. **Series:** S1 and S2 (and S4 if adopted).
2. **Orders:** d = 3, 4, 5, with tau = 1.
   - d = 6 is excluded: 720 patterns over ~440 vectors gives under one expected count per pattern, so about half would be "missing" by chance.
   - At d = 5 (120 patterns, about 3.7 expected each) about 3 patterns are expected to be missing by chance alone.
   - At d = 4 (24 patterns, about 18 expected each) a missing pattern would be remarkable.
3. **Tie rule (pre-declared).**
   - Equal values are ranked by order of occurrence; this is the common convention.
   - Under the null, ties are frequent for S1: about 27% of 4-value windows and about 42% of 5-value windows contain at least one tie.
   - Run a sensitivity version that drops tied windows, and report both.
4. **Statistics:**
   - (i) the number of missing patterns;
   - (ii) normalised permutation entropy H in [0, 1];
   - (iii) the chi-square of pattern counts.
   - All are compared with at least 10,000 simulated fair histories run through the identical pipeline, including the identical tie rule. This makes tie-induced bias appear equally in the null and cancel.
5. **Nesting check (key discriminator).**
   - A genuinely forbidden pattern at order d forces every order-(d + 1) pattern containing it to be forbidden too, so true forbidden patterns propagate and grow in number with d.
   - Chance misses do not nest consistently.
   - Report whether any pattern missing at d = 4 has all its d = 5 extensions missing.
6. **Optional predictive use (secondary):** given the last d - 1 values, rank next-value regions by how under-represented each continuation pattern is. This is only worth building if B2 shows a significant missing-pattern result.

### 4.7 Measurement within the project

- **Predictions:** B1 produces one prediction record per target draw (7 main + 1 Powerball), walk-forward, scored by the project's standard scoring.
- **Baselines:** the same as Method A (1.4 expected main matches, 0.05 Powerball), plus the score distribution from running B1 unchanged on at least 1,000 simulated fair histories.
- **Diagnostics:** B1 skill curves (S1, S2) and B2 statistics, each with simulated-envelope p-values or z-scores, reported separately from prediction scores.
- **Forward predictions:** as for Method A.

### 4.8 Effort and runtime

- **Code:**
  - B1: about 150-250 lines.
  - B2: about 100-200 lines; no ordpy needed, as the ordinal encoding is a few lines of numpy.
  - Reuses the shared fair-draw simulator.
- **Runtime:**
  - B1 per history: about 400 targets x up to about 446 library states x E popcounts, about 10^6 operations; trivial.
  - B1 over 1,000 null histories x 4 values of E: a few minutes in vectorised numpy.
  - Spread across the 3900X's 12 cores via multiprocessing if wanted; each history is independent.
  - B2 over 10,000 null histories: seconds to a minute.
  - Total well under the half-hour budget.

### 4.9 Expectations and things to watch

- **Expected outcome:** null.
  - Each draw is a separately run physical event.
  - Two machines and possibly several ball sets are in use.
  - Nothing physical obviously carries a "state" from one Thursday to the next.
- **What the data could detect (rough):**
  - The standard error of a forecast-skill correlation over ~400 walk-forward targets is about 1 / sqrt(400) = 0.05.
  - Skill around rho = 0.15 would be about 3 sigma.
  - That is a fairly strong effect; weak memory would go undetected.
- **Things to watch:**
  - *Look-ahead leakage (most important):*
    - Any library pair whose successor is the target draw or later invalidates the result.
    - A positive B1 result should be presumed to be a leakage bug until proven otherwise.
    - Recommended test: run B1 on simulated fair histories and confirm the skill is at chance.
  - *Post-hoc choice of E or k:* report the full pre-declared grid. Never promote the best-looking setting to "primary" afterwards.
  - *Ties:* see section 4.6. Never interpret missing patterns in S1 without the matched simulated null.
  - *Sorted versus drawn order:*
    - Published sorted results destroy the within-draw time order.
    - S3 is unaffected, because it uses sets.
    - S4 depends on drawn order being available.
  - *Machine switching:* if per-draw machine identity is ever available, it is a natural split. Dynamics, if any, would live within one machine's sequence.

---

## 5. Matters common to both methods

### 5.1 Data scope

- **Current format:**
  - 7 main numbers from 35, plus 1 Powerball from 20.
  - First draw: Draw 1144 on Thursday 19 April 2018, confirmed by Lotterywest media releases of 12-13 April 2018.
  - That gives roughly 440-450 draws to late October 2026.
- **Earlier formats (6 from 40, and before that other matrices):**
  - Never pooled with the current format.
  - If wanted later, they can serve as independent replication sets, each analysed in its own format with its own simulator. A real physical effect should replicate; a fluke should not.
- **Oz Lotto:** if the project extends to Oz Lotto, both methods apply unchanged in a separate run with that game's simulator. Supplementary numbers are not used for prediction, consistent with the project's existing decision.

### 5.2 Fair-draw simulator (shared component)

- A single function that generates a synthetic history of N draws with the real game's rules:
  - 7 distinct main numbers uniformly from 1..35;
  - 1 Powerball uniformly from 1..20;
  - integer-valued.
- Uses a seeded generator, with the seed recorded in every output.
- Every statistic in this document takes its p-value from this simulator, run through the identical code path as the real data. That is the main protection against artefacts from the game's discreteness, without-replacement draws and ties.
- If the project already has such a simulator, reuse it. Do not write a second one.

### 5.3 Multiple comparisons and pre-declaration

**Primary outcomes** (pre-declare before running on real data):

- A1 short-gap ratio (main).
- A4 number-variance ratio at L = 10 (main).
- B1 prediction score at E = 2 (main and Powerball).
- B2 missing-pattern count at d = 4 (S2).

**Everything else is secondary**, reported in full but interpreted with the family of tests in mind.

- Count the total number of statistics computed.
- Apply a simple family-wise correction (Holm) to the primary set.
- Treat any secondary "hit" as a hypothesis for the forward-prediction phase, not as a finding.

### 5.4 Confirmation

- A result that survives the simulated null and the correction is still provisional.
- The confirmation is the project's real-world forward predictions against future draws, consistent with the owner's stated view that real predictions against actuals are what counts.
- Freeze the method and its settings before that phase.

### 5.5 Overlap with existing project methods

- The main project chat should check whether any existing method already covers this ground, for example frequency or "hot/cold" methods (overlapping Method A) or nearest-neighbour or pattern methods (overlapping Method B).
- Where overlap exists, adopt only the non-overlapping parts:
  - for Method A, most likely the number-variance and periodicity diagnostics;
  - for Method B, the forbidden-pattern nesting check.

### 5.6 Drawn-order data

- News reports of results often list main numbers in a non-sorted order, which suggests drawn order is recorded somewhere. For example, Draw 1556 is reported as 5, 6, 18, 9, 14, 4 and 13.
- Whether an official, complete, machine-readable drawn-order record exists for the whole post-2018 era has not been verified.
- If it can be scraped reliably, it enables S4 and strengthens Method B.
- If it cannot, both methods still run on sorted results.

### 5.7 Implementation notes

- **Dependencies:** numpy and scipy only.
- **Reproducibility:** deterministic seeds everywhere, recorded in outputs.
- **Hard abort:** stop on any data inconsistency, such as wrong ball counts, out-of-range values, duplicate numbers within a draw, or gaps in draw numbering. Never skip silently.
- **Packing:** main draws as 64-bit integers for fast set operations (Method B).
- **Parallelism:** the simulated-null loops are embarrassingly parallel; use multiprocessing if runtimes ever approach the budget.
- **Architecture:** the main project chat is to map each method onto the ratified experiment interface, wrappers and scoring. This document deliberately does not specify those.

---

## 6. Effort and runtime summary

| Item | Approx. code | Dependencies | Approx. runtime (3900X) |
|---|---|---|---|
| Shared fair-draw simulator | 30-60 lines (or reuse) | numpy | negligible |
| Method A diagnostics (A1-A5) + 10,000-history null | 120-180 lines | numpy, scipy | seconds |
| Method A predictor + 1,000-history predictor null | 80-120 lines | numpy, scipy | a few minutes |
| Method B1 analogues + 1,000-history null | 150-250 lines | numpy | a few minutes |
| Method B2 ordinal patterns + 10,000-history null | 100-200 lines | numpy | under a minute |
| **Total** | **about 500-800 lines** | | **well under 30 minutes** |

---

## 7. Decisions for the project owner

1. **Should Methods A and B be adopted as candidate experiments?**
   - *Why it matters:* they add two cheap, well-controlled tests rooted in the frameworks the owner found interesting.
   - *Recommendation:* adopt both.
   - *Options:* (a) both; (b) A only, which is cheapest and has an exact null; (c) B only; (d) neither.
2. **When should they be implemented?**
   - *Why it matters:* the main chat is mid-implementation and should not be diverted.
   - *Recommendation:* as a later package after the current one completes.
   - *Options:* (a) next package; (b) after the first forward-prediction cycle; (c) defer indefinitely.
3. **Should drawn-order data be pursued in the scrapers?**
   - *Why it matters:* it enables S4, the most physically meaningful series for Method B.
   - *Recommendation:* a one-off feasibility check only; adopt if cheap.
   - *Options:* (a) check now; (b) check when Method B is implemented; (c) do not pursue.
4. **Should per-draw machine and ball-set metadata be sought?**
   - *Why it matters:* a mechanical bias tied to one machine or ball set is the most plausible route to any genuine non-random finding.
   - *Recommendation:* the same feasibility check as decision 3.
   - *Options:* as for decision 3.

---

## 8. References (for provenance; not required reading)

- Amigo, J. M., Zambrano, S., Sanjuan, M. A. F. (2007). True and false forbidden patterns in deterministic and random dynamics. Europhysics Letters 79, 50001.
- Bandt, C., Pompe, B. (2002). Permutation entropy: a natural complexity measure for time series. Physical Review Letters 88, 174102.
- Bohigas, O., Giannoni, M.-J., Schmit, C. (1984). Characterization of chaotic quantum spectra and universality of level fluctuation laws. Physical Review Letters 52, 1.
- Brody, T. A. (1973). A statistical measure for the repulsion of energy levels. Lettere al Nuovo Cimento 7, 482.
- Eckmann, J.-P., Ruelle, D. (1992). Fundamental limitations for estimating dimensions and Lyapunov exponents in dynamical systems. Physica D 56, 185.
- Grassberger, P., Procaccia, I. (1983). Characterization of strange attractors. Physical Review Letters 50, 346.
- Lorenz, E. N. (1969). Atmospheric predictability as revealed by naturally occurring analogues. Journal of the Atmospheric Sciences 26, 636.
- Montgomery, H. L. (1973). The pair correlation of zeros of the zeta function. Proceedings of Symposia in Pure Mathematics 24, 181.
- Odlyzko, A. M. (1987). On the distribution of spacings between zeros of the zeta function. Mathematics of Computation 48, 273.
- Packard, N. H., Crutchfield, J. P., Farmer, J. D., Shaw, R. S. (1980). Geometry from a time series. Physical Review Letters 45, 712.
- Sugihara, G., May, R. M. (1990). Nonlinear forecasting as a way of distinguishing chaos from measurement error in time series. Nature 344, 734.
- Takens, F. (1981). Detecting strange attractors in turbulence. Lecture Notes in Mathematics 898, 366.
- Theiler, J., Eubank, S., Longtin, A., Galdrikian, B., Farmer, J. D. (1992). Testing for nonlinearity in time series: the method of surrogate data. Physica D 58, 77.
- Zunino, L., Olivares, F., Scholkmann, F., Rosso, O. A. (2017). Permutation entropy based time series analysis: equalities in the input signal can lead to false conclusions. Physics Letters A 381, 1883.
- Lotterywest media releases, 12-13 April 2018: Powerball format change to 7 from 35 plus 1 from 20, first draw Draw 1144 on Thursday 19 April 2018.

(End of document.)
