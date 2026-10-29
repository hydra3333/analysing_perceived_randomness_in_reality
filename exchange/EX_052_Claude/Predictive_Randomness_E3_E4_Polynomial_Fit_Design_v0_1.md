# Predictive Randomness - E_3 and E_4 specification (exact polynomial fits, including Chebyshev minimax), design note v0.1

**Document:** the method-level specification of E_3's and E_4's first variants (R2 v0.5 section 7.1), with one shared fitting helper, and the design of the package that adds them.
**Version:** v0.1 DRAFT for the reviewer's design-stage review (R-3), 30 October 2026. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises nothing and changes no ratified rule.
- **No code yet:** unlike E_6, no candidate code is enclosed. The code follows only after this design passes (the owner's "chunks" instruction of 30 October 2026).
- **Feasibility probes:** two probes on invented data are reported in section 7.
- **Base:** `main` with the E_6 package, which is not yet installed; this package is built on top of it.
- **Owner's plan:** E_3 and E_4 together, sharing one Chebyshev fitting helper with least-squares, interpolation and minimax fits (register v0.15 candidate).

## 1. In plain English

For each number, its recent history is a 0/1 series: 1 if it was drawn at that draw, 0 if not. Fit a smooth curve (a polynomial) to that series, then look one step past the last draw:
- **E_3 (occurrence-curve endpoint)** ranks the numbers by the curve's value at the next draw: where is this number's curve heading?
- **E_4 (occurrence-curve gradient)** ranks them by the curve's slope there: is this number trending up or down?

**Three ways to fit the curve, each a set of fixed variants:**
1. **Least squares:** the curve that makes the total squared error smallest, the everyday way.
2. **Interpolation at Chebyshev nodes:** a curve through a few points of a lightly smoothed history, placed at Chebyshev nodes so the curve does not swing wildly.
3. **Chebyshev minimax:** the curve that makes the worst single error as small as possible. This is the owner's Remez idea, in its exact discrete form (Stiefel's exchange method).

**Exactness:** all three are computed exactly with fractions, as E_6 is, so Windows and Linux publish the same bytes. The scores are not probabilities, since a curve can go below 0 or above 1. So E_3 and E_4 publish rankings, TOP and WORST, and no probability vector. This is the template's "score-only" case.

## 2. What is modelled (R2 7.1: "target random variable")

- **The observed series:** for target N, barrel B and label j, the series y_i = x(d_i, j) over the window of the most recent M eligible draws, d_i = N - M + i for i = 0..M-1. The newest draw is i = M - 1.
- **The abscissa:** draw positions are t_i = i - M, so the newest draw is at t = -1 and the target at t = 0. Every t is an integer, so everything stays exact.
- **The view:** `UNORDERED_SET` without dates. Only "was j drawn" is used, not order or dates.
- **Minimum history:** M draws (`minimum_history_draws` = M). Earlier targets get the contract's `INSUFFICIENT_HISTORY` record: published, no ticket, by the existing contract rule.

## 3. The fits (the shared helper, `src/methods/_common/polynomial_fits.py`, revision 1)

Each fit returns a polynomial p of degree at most D in t, with exact rational coefficients. E_3's score is p(0), the value at the target; E_4's score is p'(0), the slope at the target, per draw.

**3.1 Least squares on the raw series (`LS`).** Minimise the sum over i of (y_i - p(t_i))^2.
- **Unique:** the window has M > D distinct points, so the fit is unique.
- **Solved exactly:** by the normal equations in fractions.
- **An honest note:** in exact arithmetic the least-squares polynomial does not depend on the basis or the scaling of t. The Chebyshev basis only helps floating-point conditioning, so this variant is plain polynomial least squares. The method name keeps "Chebyshev" only where it means something: the nodes in 3.2 and the minimax criterion in 3.3.

**3.2 The smoothed series** used by 3.3 and 3.4: S_i = the mean of y over positions i - H .. i + H, clipped to the window. Near the window's edges fewer positions are averaged; S_i uses no draw outside the window, so no future draw.
- H = 4 gives a width of up to 9 draws, about two months of Powerball's weekly draws.
- **Why smoothing is needed:** on raw 0/1 data the minimax fit is degenerate. The probe of section 7 found the constant 1/2, with worst error 1/2, for every label tried, so every number ties. Smoothing makes the worst-error criterion meaningful.

**3.3 Interpolation at Chebyshev nodes (`INTERP`).** The D + 1 Chebyshev nodes of the first kind are mapped onto the window's position range 0..M-1.
- **The node positions:** c_k = the integer nearest to (M - 1)(1 + cos((2k + 1)pi / (2D + 2))) / 2, for k = 0..D, with halves rounded up.
- **Exactness of the nodes:** the cosines are computed once in the specification, not by the method. The method holds the D + 1 integer positions per variant as constants, and the tests check them against the formula. So no floating point is used at run time.
- **The fit:** p is the unique polynomial of degree D through the points (t_{c_k}, S_{c_k}). The positions are distinct for the variants below; the helper refuses otherwise.

**3.4 Chebyshev minimax on the smoothed series (`MINIMAX`).** Minimise the maximum over i of |S_i - p(t_i)|.
- **Unique:** polynomials on distinct points satisfy the Haar condition, so the discrete best approximation is unique.
- **Optimality:** p is optimal exactly when its error reaches its maximum at D + 2 points with alternating signs (the alternation theorem).
- **The algorithm:** Stiefel's single-point exchange, in fractions.
  1. Start from a reference set: D + 2 positions, round(k(M-1)/(D+1)) for k = 0..D+1.
  2. Solve the levelled equations p(t_r) + (-1)^k h = S_r on the reference.
  3. Find the point of largest error, taking the lowest index on ties.
  4. If its error is at most |h|, stop: p is optimal, with worst error |h|.
  5. Otherwise exchange that point into the reference, keeping the signs alternating, by the standard rules, which are spelled out in the helper with no free choices.
- **Termination:** |h| increases strictly at each exchange, and there are finitely many references, so it terminates. The helper still has a cap of 10,000 exchanges and raises if the cap is ever reached, which ends the run as `RUNTIME_FAILURE`. It is never expected.
- **A zero error** (S is exactly a polynomial of degree D, for example a number never drawn in the window, where S is all 0) ends at once with p = S.

**3.5 The gradient.** p'(0) is the coefficient of t in p. So E_4 needs no separate numerical derivative: it is exact.

## 4. Outputs, per barrel (E2R-1 sections 5 and 7)

**Per barrel channel, for both methods and every variant:**
- `ranking_kind` `RANKING_WITH_SCORES`, `score_type` `FLOAT64`;
- TOP `TOP_MARGINAL`, WORST `INVERSE`, `readout_selection_rule_version` `TOP_MARGINAL_AND_INVERSE_V1`;
- `TIE_SHA256_V1`;
- `probability_kind` `NONE`.

The scores are p(0) (E_3) or p'(0) (E_4), each rounded once to float64.

**Other declaration fields:**
- no diagnostic record;
- deterministic;
- `IS_NOT_APPLICABLE`;
- `minimum_history_draws` = M;
- `fit_sampling_model_version` `POLY_LS_RAW_V1`, `POLY_INTERP_CHEB_NODES_SMOOTHED_V1` or `POLY_MINIMAX_SMOOTHED_V1`;
- for Oz Lotto, MAIN only.

**Interpretation, stated in the registry texts:**
- the scores are curve values or slopes, not chances;
- a curve fitted to a short, noisy 0/1 series is least reliable exactly at its end, which is where these methods look;
- that end behaviour is what the experiment measures.

**Why no probabilities** (R2 7.1: "probabilities only if justified"): the values are not constrained to [0, 1] and have no model-based normalisation. Converting them into probabilities would be an invented transformation. "Mark, never suppress" is honoured by publishing the scores themselves.

## 5. The variants (fixed in revision 1; owner decision D34-2)

The same six fit configurations for E_3 and for E_4. The `variant_id` names the fit, the window M and the degree D:

| `variant_id` | Fit | Window M | Degree D | Smoothing H |
|---|---|---|---|---|
| `POLY_LS_W52_D2_V1` | least squares, raw | 52 (a year) | 2 | none |
| `POLY_LS_W52_D3_V1` | least squares, raw | 52 | 3 | none |
| `POLY_LS_W104_D3_V1` | least squares, raw | 104 (two years) | 3 | none |
| `POLY_INTERP_W52_D4_H4_V1` | interpolation at 5 Chebyshev nodes | 52 | 4 | 4 |
| `POLY_MINIMAX_W52_D2_H4_V1` | Chebyshev minimax | 52 | 2 | 4 |
| `POLY_MINIMAX_W52_D3_H4_V1` | Chebyshev minimax | 52 | 3 | 4 |

The interpolation node positions for M = 52, D = 4, which are fixed constants in the code, are 50, 40, 26, 11, 1. That is the formula of 3.3 for k = 0..4, rounded as stated.

**The count:** 2 methods x 6 variants x 2 games = 24 declarations and 24 `FORMULA_OPEN` entries.

## 6. Worked examples (the hand-checkable fixtures)

1. **Least squares, line (D = 1, three points):** y at t = -3, -2, -1 is 1, 0, 1. The mean is 2/3 and the slope is 0, so p(t) = 2/3: E_3's score is 2/3 and E_4's is 0.
2. **Least squares, rising data:** y = 0, 0, 1, 1 at t = -4..-1 gives p(t) = 3/2 + (2/5)t. So E_3's score is 3/2, which is above 1, the reason scores are not probabilities, and E_4's is 2/5.
3. **Minimax, constant (D = 0):** S = 0, 1/3, 1 gives p = 1/2, with worst error 1/2 attained at the two ends with opposite signs.
4. **Minimax, degenerate raw data:** a raw 0/1 series typically gives the constant 1/2 with worst error 1/2, whenever 0s and 1s alternate often enough across the window to supply D + 2 alternating extremes. The probe found this for every label tried. This is the reason for smoothing.
5. **Interpolation:** the points (-3, 0), (-2, 1), (-1, 0) at D = 2 give p(t) = -(t + 2)^2 + 1, so p(0) = -3 and p'(0) = -4.

These values were checked by computation, not by hand: the first draft had two wrong (the node positions and example 2). The tests check each exactly, and the helper's least-squares answer is cross-checked by a second, differently written algorithm (orthogonal-polynomial recurrence against the normal equations).

## 7. Feasibility (author probes, invented data, Python 3.13, not project code)

- **Exact least squares, 35 labels:** 0.13 s at M = 104, D = 3. Even the whole 433-draw history at D = 8 took 4 s. The normal matrix is the same for every label, so the real helper factorises it once per target.
- **Exact minimax on the smoothed series, 35 labels:**
  - 0.10 s at M = 52, D = 2, and 0.34 s at M = 104, D = 3;
  - at most 10 exchanges;
  - 32-35 distinct endpoint scores out of 35;
  - every result passed the alternation-certificate check.
- **Raw 0/1 minimax:** the constant 1/2, error 1/2, which confirms 3.2.

A whole development walk-forward, which is later work (WF-1), would take minutes per variant.

## 8. Verification inside the method (verify())

`verify()` recomputes independently and refuses any difference:
- **Least squares:** coefficients by an orthogonal-polynomial (Forsythe) recurrence, compared exactly with the normal-equation result.
- **Interpolation:** Newton divided differences, against Lagrange.
- **Minimax:** the alternation certificate. The error of the published polynomial reaches its maximum at D + 2 reference points with alternating signs, and is nowhere larger. A certificate check is a genuinely different test from re-running the exchange.

## 9. The package

**New files:**
- `src/methods/_common/polynomial_fits.py`: the shared helper, revision 1;
- `src/methods/E_003/` and `src/methods/E_004/`: each with `__init__`, a small `variants.py` holding the fixed table of section 5, `contract.py` and `IN_DEVELOPMENT.txt`;
- the 24 declarations and 24 entries;
- `tests/test_polynomial_fits.py`, for the helper;
- `tests/test_e3_e4_polynomial.py`, for the methods: worked examples, each variant's own setting computed in the test, no peeking, contract runs under a simulated release, as installed, and folder guards;
- this note.

**Replaced:** `Method_Contract_Runner.py` gets two `ADAPTERS` lines.

**Unchanged:** everything else, including E_6. No existing test needs editing, because E_6's package changed the counting tests to rules.

**Revisions:** E_3 and E_4 each start at revision 1, and both name the helper `polynomial_fits` r1. A later change to the helper means new revisions of both (E2R-R14A), which is the case the retirement tooling, CODE-3, exists for.

**The template:** draft 2 adds the shared-helper case (a helper in `_common/` with its own tests, named by every method that uses it), the score-only case (no probability vector), and the "minimum history = window" case.

**Release:** the same pattern as E_6. Installed non-runnable, released by later small packages, variant by variant if the owner wishes. Real data stays off (WF-1).

## 10. Owner decisions

- **D34-1 (RECOMMENDED): E_3 and E_4 share the helper.** The helper lives in `_common/` and is reviewed as part of both methods; each method names it.
- **D34-2 (RECOMMENDED): the six fit configurations of section 5,** for each method in both games: windows, degrees, smoothing H = 4 and node positions. This is a scientific choice; the owner may prefer other windows or degrees. Every value is fixed now.
- **D34-3 (RECOMMENDED): least squares on the raw series, interpolation and minimax on the smoothed series** (3.2), for the reason shown by the probe.
- **D34-4 (RECOMMENDED): scores only, no probabilities** (section 4).
- **D34-5 (RECOMMENDED): the naming honesty of 3.1.** Least squares is plain polynomial least squares; "Chebyshev" names the nodes and the minimax criterion.

## 11. Not in scope

Not in scope:
- real-data runs, walk-forward and scoring (WF-1);
- splines and local polynomials (E_37), and other curve families;
- a weighted-least-squares or truncated-Chebyshev-series variant (possible later variants, not now);
- any change to E_1, E_6 or the contract libraries.

The gates and the orphan-marker rule apply unchanged.
