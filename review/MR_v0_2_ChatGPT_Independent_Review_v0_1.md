# ChatGPT Independent Review — Method Ranking Measures Proposal v0.2

**26 October 2026 · REVIEW ONLY · NOT RATIFIED · No coding or run authority**

**Reviewed source:** `Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_2.md` (770-line Markdown supplied by owner; original described as Claude draft v0.2). Review is independent of Claude's prior drafting. I checked the arithmetic of the stated fair-draw formulas using exact integer combinations and rational probabilities, and compared the game definitions with public rules pages. **No project scripts or experiments were run; no development masters were accessed, and all numerical calculations below use theoretical fair-draw distributions only. DISCLOSURE: One public web search for game rules unexpectedly returned a results-page preview containing quarantined draw values. That preview was visible to this review; I did not request/open that results page and did not use any of those values in calculations, analysis or the document. This incidental exposure should be added, value-free, to the owner’s holdout-exposure record.**

**Verdict: NOT READY FOR RATIFICATION AS WRITTEN.** Four scientific/contract **BLOCKERS**, followed by correctable ambiguities and optional improvements. The framework and owner's choices are worth retaining. **Package 2 v0.11 C1–C6 must remain unchanged.** Recommendations are not owner decisions.

## A. BLOCKERS

### B1 — In-sample sigma and Bayesian evidence are invalid under the proposed null

Sections 3.5, 5, 6, 7 and 10 calculate or promise ordinary fair-draw sigma, p-values, Bayes factors and global significance in both WF and IS league tables. In IS the fit deliberately uses the same outcomes subsequently scored. Consequently the ticket selection, distribution and fit are **not fixed independently of those outcomes**. The binomial, hypergeometric or normal-reference tails supplied for an outcome-independent entry no longer calibrate the entire fit-and-score procedure. An all-page banner saying “diagnostic” is necessary but **does not make a displayed 5-sigma or decisive Bayes factor scientifically interpretable**.

**Required:** IS reports may show raw counts, matching, gaps, ranks, description, MR1, MR1-T and observed IS-minus-WF differences, but mark uncalibrated **p-value/sigma/Bayes-factor significance as `IS_NOT_CALIBRATED`** rather than presenting them as calibrated findings. If the owner wants calibrated IS significance later, an independent whole-pipeline null simulation must **refit** the method on each synthetic history, repeat the scoring and include every investigated variant; its meaning and costs require a separate reviewed design. Any reported IS optimism difference is a descriptive diagnostic, not an unbiased numerical estimate of out-of-sample generalisation.

The WF marginal fair-draw null is valid for genuinely prefix-only forecast tickets fixed without the outcome, even if their selection responds to earlier draws. Historical WF on development data remains exploratory if methods, windows or report measures were designed by looking at those same development outcomes. No “discovery” claim from development ranking alone.

### B2 — The claimed global sigma is not a generally valid correction

Section 5 uses `P_global = 1 - (1-P_up)^M` (Šidák) and section 18 acknowledges correlated tracks and sub-measures. Šidák is exact under independence, not in general; **negative dependence can make it anti-conservative**. Simple counterexample: two mutually exclusive p=0.05 events have family error 0.10, whereas Šidák gives 0.0975. Moreover `M = tracks × sub-measures in the same table` is not necessarily the number of comparisons used when the best method is selected across **many** divisions, tables, variants, windows, reruns and games. Section 16 MRO-08 calls this family definition OPEN while section 5 makes a per-table default operative.

**Required:** For a mathematically defensible conservative adjustment, use `P_Bonf = min(1, M * P_local)` for an explicitly frozen/predeclared complete family with valid marginal p-values. Alternatively a separately validated joint-null max-statistic calibration may use the actual correlations and selection procedure. Šidák can be displayed as an **assumption-dependent supplementary estimate only**, never the primary guaranteed global sigma. Record `M`, the entire family membership/definition, version, prior searches/window selection and what the correction **does not** cover. Searching more alternatives after examining results invalidates a previously declared complete family. A single per-table `M` is insufficient to claim programme-wide error control. The global sigma must be marked **not calibrated** for IS.

Keep the owner's one-sided sigma convention and the zero-**excess**-win rule. Avoid unqualified physics “evidence/discovery” language for exploratory rankings.

### B3 — MR15 spectral false-alarm formula cannot be accepted as calibrated significance

Section 6 MR15 assumes Lomb–Scargle power at all frequencies is independently `Exp(1)` and therefore `FAP = 1-(1-exp(-P_max))^K`. For unevenly sampled matches, grid powers are generally dependent; match counts are **discrete, non-Gaussian**; frequency normalisation is not fully specified; at a Nyquist frequency for an even regular grid the ordinate does not have the generic two-degree-of-freedom exponential distribution. Sparse/missing targets aggravate the problem. Section 18 already treats this as approximate, but mapping the approximation directly to scientific sigma and the MRT-07 nominal false-alarm requirement is not justified.

**Required:** MR15 FAP/sigma should be **`UNCALIBRATED_EXPLORATORY`** until an independent, seeded, versioned fair-draw null calibration is specified and tested for the **actual scored draw-number grid, method capabilities, scanned frequencies and maximum-over-frequency statistic**, preferably replicating the whole tested-selection process. Null-generated matches must be drawn from the exact game-specific hypergeometric model, and the Powerball channel from Bernoulli(1/20). Report period/power descriptively in the meantime. Specify a minimum usable sample size, frequency normalisation and uncertainty of any Monte Carlo p-value. Repeating the same null calibration after choosing an interesting period is not independent confirmation.

### B4 — MR2/MR3 fair-draw recurrence ruler is wrong for non-contiguous scored sets

Section 3.7 permits missing `PREDICTION_AVAILABLE` targets and an own-set table. MR2's gap `N_(i+1)-N_i`, and MR3's time since last win `L+1-N_k`, count draw numbers through **unscored/unavailable opportunities**. But the supplied fair-draw reference `1/p_d` is the mean number of **scored opportunities** between successes. These are not interchangeable when statuses have gaps. The same issue affects MR15 if its missingness mechanism changes with previous outcomes.

**Required:** Retain draw-number intervals as an explicitly labelled calendar/draw-time description, but for a chance-rate comparison define and rank the **scored-opportunity gap** (difference in ordinal positions within the track's actual comparison set) and the “opportunities since” value in that same set. For MR3, the not-yet-scored target `L+1` is an opportunity only if this exposure convention is defined and its inclusion is made explicit. Alternatively require contiguous, eligible, fully scored targets for these MR2/MR3 sub-measures and mark other cases inapplicable. Never compare official-draw gaps against `1/p_d` when data are missing. Record C/own-set membership and missingness/pre-outcome status provenance.

## B. CORRECTIONS REQUIRED

**C1 — Suppress contradictions in sigma wording (sections 2, 5 and MR4).** “0 wins = 0 sigma” must mean **0 excess sigma**. Zero Powerball Division 9 wins in n=291 has a nontrivial **deficit** tail: `P_lo ≈ 0.01110583557`, `Z_minus ≈ 2.28673`; the document's equations correctly permit that. Avoid promising both excess and deficit sigma are zero for k=0. Clamping negative normal deviates at zero is fine.

**C2 — Separate exact p-values from numerical exactness (section 11).** Exact rational division probabilities are excellent. But promising to sum `Fraction` binomial tails for every method/window up to n=5000, then convert to float64, is computationally burdensome and gives no explicit way to obtain `P~1e-300` without underflow. Specify a reference **exact-rational acceptance oracle** (small/moderate cases), a **tested log-tail numerical implementation** for production, and precision cross-checks over the actual domain, including ultra-small probabilities. Use inverse survival of p or log-survival, not `norm.ppf(1-p)`. Clarify that the 1e-6 sigma accuracy is subject to an independently reliable reference and is not asserted merely by using float64. A printed confidence of “100%” must not conceal a nonzero tail probability.

**C3 — MR13 Bayes factors (section 6).** The main-channel half-normal prior on `theta>0` defines a one-sided `BF_plus` and separately `theta<0` defines `BF_minus`; this is mathematically coherent **provided both priors are normalised on their respective half-lines**. The Powerball-channel `q~Beta(1,19)` is **two-sided around the fair q=0.05**: its BF cannot be labelled `BF_plus`. Name it `BF_ANY` or define properly truncated-plus and truncated-minus Beta alternatives with renormalised priors; do not infer a direction from a two-sided BF. Report prior sensitivity. Bayes factors are not p-values or sigma and cannot be assigned the sigma-based global adjustment without a separately justified rule.

**C4 — MR14 probability semantics and edge cases (sections 6, 13).** The formula for classical **squared Bhattacharyya affinity** is correct, as is its stated fair-draw expectation. However the contract must distinguish genuine, forecast-time per-label **inclusion probabilities** (sum 7) from a normalised probability distribution over labels (sum 1) and from arbitrary scores/weights. Dividing inclusion marginals by 7 gives a distribution over a uniformly chosen drawn member; it does **not** generate a full joint probability distribution for a 7-number ticket. A method must not gain `PROBABILITY_OUTPUT` just by renormalising its uncalibrated scores. Report which semantics are frozen and versioned. For uniform q, the per-target MR14 F is constant and `V_t=0`; its sigma division is `0/0`, so report neutral/no-variance (`NULL_VARIANCE_ZERO`), not NaN, infinite sigma or a numerical error. Specify the actual order-4 variance algorithm before declaring MR14 implementable.

**C5 — MR15 descriptive versus calibrated status (sections 6, 14).** Until B3 is resolved, use `P_MAX`, best periods and a **descriptive** spectral score but not a calibrated false alarm or Z. Revise MRT-07 to plant **different effects for different measures**: a constant per-draw hit-rate advantage need not create a cycle; MR14 requires probability vectors; MR11 requires both readouts. MRT-11 requires independent analytical checks as well as fixed-seed simulation.

**C6 — Predeclare measure and cohort identity (sections 3.7, 9, 10, 16).** An “intersection of available tracks” can shrink to empty or change whenever a FORMULA_OPEN method is added. Define which tracks are eligible for a cohort *before* examining scored outcomes, record the cohort membership digest and exact draw comparison set. Undefined measure values must not be silently omitted or sorted as zero. Use separate `NOT_APPLICABLE`, `INSUFFICIENT_DATA`, `UNDEFINED` and `NUMERIC_INVALID` statuses where appropriate; preserve the existing R2 benchmark, R3 evaluation and per-game registry vocabularies rather than reusing them for report-only statuses. Report counts of unscored targets and reasons.

**C7 — Measurement interpretation (MR0–MR4 and MR12).** MR0's MR1 tie-break is mathematically redundant if all division counts match. MR2 and MR3 are primarily pattern descriptions, not calibrated significance, and selecting shortest recurrence conditional on `k>=2` is survivor-biased. MR1 and MR12 normal approximation is not reliable for rare extreme division observations at n≈220–291 (a rare single top-division hit produces heavy tails); mark resulting Z explicitly APPROX and validate empirical type-I errors, not only first two moments. Never call a small local tail a discovery in a development league table.

**C8 — Historical WF vs truly prospective validation (sections 3.5, 9 and 18).** A retrospective walk-forward produced after all outcomes are known still requires mechanical no-leakage proof and frozen input identities. It is useful historical evaluation, **not** equivalent to advance-frozen prospective forecasts. Record method/version/window/measure selection provenance and any development-data-driven changes. Independent holdout/production results remain a separate tier.

**C9 — OPEN item governance (section 16).** `MRO-04`, `MRO-05`, `MRO-07` and `MRO-08` are called OPEN while operative sections embed their “draft defaults” as fixed parameters. The owner should ratify each default as a decision or keep it explicitly provisional and out of binding operational requirements. B2 makes MRO-08 especially consequential. `MRD-08` accepting MR11–MR15 conceptually does not ratify defective formulae that this review identifies.

**C10 — Numeric, display, and reporting consistency.** Match decimal odds to exact fractions, identifying published rounding direction; don't silently claim displayed 1-in values are exact where they are rounded. “Confidence = 100(1-p)%” is a **one-sided reference-tail complement**, not the posterior probability the method is real. For Powerball PB/main channels, document whether ranking comparisons and test families are separate. Make `LOW_N` only one of several calibration flags and never a substitute for a valid null. Output files remain create-only and rankings never change forecasts.

## C. INDEPENDENT MATHEMATICAL AND NUMERICAL CHECKS

I enumerated all attainable `(m,b)` and `(m,s)` combinations with integer combinatorial counts. All probabilities below are exact fractions; decimals are merely displays. The operator division definitions match current official game descriptions on Lotterywest's `/games/powerball` and `/games/oz-lotto` pages, and The Lott's public playing guide. (I did **not** inspect any results pages.)

| Check | Independently computed | Assessment |
|---|---:|---|
| `C(35,7)*20` | 134,490,400 | PASS |
| `C(47,7)` | 62,891,499 | PASS |
| Powerball division counts over 134,490,400 outcomes, PD1..PD9 | `1, 19, 196, 3724, 7938, 114660, 150822, 716625, 2063880` | PASS |
| Oz Lotto division counts over 62,891,499 outcomes, OD1..OD7 | `1, 21, 259, 2394, 13986, 345800, 887075` | PASS |
| Powerball any-prize probability | `611573/26898080`; odds 1 in 43.9818 | PASS |
| Oz Lotto any-prize probability | `416512/20963833`; odds 1 in 50.3319 | PASS |
| Main match mean/variance Powerball | 1.4 / 0.922352941176 | PASS |
| Main match mean/variance Oz Lotto | 49/47 / 0.771547227744 | PASS |
| MR1 fair mean/sd Powerball | 0.1536785353 / 1.0259137077 bits | PASS |
| MR1 fair mean/sd Oz Lotto | 0.1313255220 / 0.9317216314 bits | PASS |
| MR12 fair mean/sd Powerball MAIN | 0.91175620595 / 1.13867640721 bits | PASS |
| MR12 fair mean/sd Oz Lotto MAIN | 0.87915096790 / 1.14397398706 bits | PASS |
| MR12 fair mean/sd Powerball PB | 0.21609640474 / 0.94194239034 bits | PASS |
| MR5 no-tie per-target main-rank SD Powerball / Oz | 3.464101615 / 4.780914437 | PASS |
| n=291, one PD3 win `Binomial(n,p)` upper tail | `0.00042400014`, `Z≈3.33663` | PASS (document says ~3.3 sigma) |
| Sigma table at 1 through 6 | Standard normal one-sided survival | PASS to displayed rounding |
| MR14 F and E for uniform q | both 7/N, null variance zero | Formula PASS; missing edge handling |
| MR11 sign test, conditional on non-ties | `Binomial(n_plus+n_minus,1/2)` under outcome-independent TOP/WORST symmetry | PASS for WF; **not** IS calibration |
| MR13 MAIN exponential tilt normaliser `Z(theta)` and log ratio | Correct exponential-family likelihood ratio | PASS conditional on declared prior and leakage-free data |
| MR15 independent exponential peak assumption | Does **not** generally hold for actual discrete/gappy series | FAIL as calibrated FAP |

Independent fair main-match upper-tail probabilities for m=0..7:

- Powerball: `1, 0.8239220048, 0.4317482884, 0.1248297276, 0.01826078293, 0.001209751774, 0.0000292957713, 0.000000148709499` — matches §4.4.
- Oz Lotto: `1, 0.7035599358, 0.2763374904, 0.05662308987, 0.005763274938, 0.0002649165669, 0.000004468012442, 0.00000001590040015` — matches §4.4.

The §18.2 291-draw and 220-draw per-track and 124-track expected prize counts reproduce to displayed rounding. The §18.4 `2500 × 0.00134990 ≈ 3.375` and `2500 × 2.86652e-7 ≈ 0.0007166` counts also check out **if the per-test p-values are valid**. These expected counts do not imply independence between tests.

The remaining mathematical definitions were reviewed symbolically: the MR2 telescoping gap and CV denominator, MR3 alignment (subject to B4), MR4 disjoint division-set probability sum, MR5 finite-population variance with ties, MR11 signed paired comparison, MR12 surprisal transform, MR13 integral form, and MR14 expectation. MR14 variance is asserted but **not specified**, while MR15's FAP assumptions are unacceptable without calibration. Thus “every formula” cannot truthfully be marked PASS.

## D. PROPOSED MEASURES MR6–MR10 (NOT OWNER DECISIONS)

Each proposed measure is distinct from existing MR0–MR5 and MR11–MR15. For any p-value below, **WF-only nominal calibration** is intended until the complete testing family and selection procedure are ratified. In IS display the descriptive score but mark null significance not calibrated. The fair reference assumes each ticket/ranking was genuinely fixed without seeing its target's outcome.

### MR6 — Logarithmic probability quality (proposed; probability capability required)

- **One line:** reward probability forecasts that assign more probability to the numbers that actually appear, while heavily penalising overconfident misses.
- **Short explanation:** a strictly proper logarithmic scoring rule for the distribution of a **uniformly chosen one of the seven drawn main labels**. It complements MR14 fidelity and, unlike MR14, sharply penalises assigning near-zero probability to an observed number. It makes no claim to score the full joint seven-number event.
- **Exact definition:** before the draw freeze `q_j>0` with `sum(q_j)=1`, explicitly identified as a distribution over the uniformly chosen winning main label, not an arbitrary renormalised rank score. For each draw with winning set D and N possible main labels (`N=35/47`), define `g_t=(1/7) Σ_{j∈D} log2(N q_j)`. Under fair draws, conditional expectation `e_t=(1/N)Σ_{j=1}^N log2(N q_j)≤0`, and variance `v_t=((N-7)/(7(N-1))) Var_pop[log2(N q_j)]`. The strictly proper part is the underlying log score `Σ log q_j/7`; the fair-relative constant only changes its presentation. Across targets, score `G=mean(g_t)`, reference `mean(e_t)` and nominal `Z=(Σ(g_t-e_t))/sqrt(Σv_t)` where `Σv_t>0`. For Powerball's separate barrel use `g_PB=log2(20 q_PB[drawn])`, `e_PB=(1/20)Σ log2(20 q_PB[j])` and the corresponding population variance.
- **Ranking key:** `G` descending as descriptive probability quality; the calibrated excess `Z_plus` in a separate WF significance league table, not silently conflated. MAIN and PB separately.
- **Edge cases:** `q=0` gives an infinite negative log-score if observed; require owner-reviewed smoothing **inside the frozen method**, never silently in evaluator. Reject negative, nonfinite, wrongly normalised q. If `v_t=0` for all targets, report neutral `NULL_VARIANCE_ZERO` (uniform q). Inapplicable without meaningful `PROBABILITY_OUTPUT`.
- **Outputs:** `G, Σg, mean(e), Σ(g-e), Zplus, Zminus, n, probability_semantics, null-variance flag`.
- **Fair-draw reference:** the conditional e and v above; nominal asymptotic normal with finite-population correction, validated by exact/simulated null.

### MR7 — Total main-match excess (proposed; all ticket tracks)

- **One line:** did the track hit more main numbers in total than fair draws would produce?
- **Short explanation:** uses **every** predicted main-number match, even if the ticket wins no prize division. This is more direct than rare-division counts and different from MR12's logarithmic transform.
- **Exact definition:** `S=Σ_t m_t`; for n scored fair-draw tickets the one-draw generating polynomial is `A_G(z)=Σ_{m=0}^7 p_{G,m} z^m`, where `p_G,m=C(7,m)C(N-7,7-m)/C(N,7)`. The fair count distribution is defined by coefficients of `A_G(z)^n`. Upper tail is `Pr(S_null ≥ S_observed)`; lower tail likewise. This is an exact mathematical definition, with production numerics subject to validated stable algorithms. A separate Powerball barrel channel uses `B=Σ b_t ~ Binomial(n,1/20)`.
- **Ranking key:** total excess `S - n μ0` descending (or average excess for a common C); a separate WF significance ranking by valid local and conservative global sigma.
- **Edge cases:** `n=0` is unavailable; non-identical available target sets require the cohort/own-set labels. Counts use Python `int` if necessary. Never combine MAIN and PB p-values without an approved joint rule.
- **Outputs:** `n,S,S/n,μ0,Var0,observed_minus_expected,p_up,p_lo,Zplus,Zminus` and PB analogue.
- **Fair-draw reference:** Powerball `μ0=1.4, Var0=392/425`; Oz `μ0=49/47, Var0=39200/50807`. Conditional predictability preserves this null under truly prefix-only selection.

### MR8 — Unusually long match streak (proposed; all ticket tracks)

- **One line:** does the method achieve a notably long sequence of consecutive better-than-ordinary matching draws?
- **Short explanation:** measures bursts of success rather than total success. A sequence of matches on consecutive official draw numbers may be interesting even if the mean is ordinary. It does not presume periodicity or that a run is predictive.
- **Exact definition:** define predeclared `h=3` main-number matches, and `x_t=1(m_t≥3)`. Let `R` be the longest sequence of `x_t=1` across **consecutive official draw numbers** whose forecasts were available; missing targets break a run. `p_h=P0(m≥3)` from §4.4. For an observed streak threshold `r≥1`, compute `P0(R≥r)=1-P0(no length-r run)` by an exact Bernoulli dynamic programme over states `0..r-1` of consecutive successes, restarting at every gap: `v_new[0]=(1-p_h)Σv_old`, `v_new[j+1]=p_h v_old[j]` for `j<r-1`; discarded probability `p_h v_old[r-1]` is absorption. The complement of surviving probability is the exact upper tail under the specified gap pattern. `R=0` yields upper tail 1.
- **Ranking key:** upper-tail p ascending / valid local sigma descending in a WF table; raw R descending in a descriptive table.
- **Edge cases:** `n=0` unavailable; `R=0` gives excess sigma 0; pre-outcome missingness eligibility must be proven; change of threshold h is a **new sub-test** and contributes to multiplicity.
- **Outputs:** longest streak, beginning/end draw keys, scored/gap counts, h, p_h, exact `P_up`, and calibration status.
- **Fair-draw reference:** `p_h` is hypergeometric-tail `P0(m≥3)` = ~0.1248297 Powerball, ~0.05662309 Oz Lotto; the streak DP accounts for each actual contiguous segment.

### MR9 — Recent-versus-earlier performance change (proposed; all ticket tracks)

- **One line:** did a method's matching performance improve or deteriorate in the later half of the evaluation window?
- **Short explanation:** separates a rising/falling signal from one good cumulative score. This is a measure of temporal change, **not evidence that a change will persist**.
- **Exact definition:** sort the n **scored** targets by official draw number, split at `n_early=floor(n/2)`, `n_late=n-n_early` without optimising the split. With main-match means `a,b`, define `Δ=b-a`. Under fair draws `E(Δ)=0` and `Var0(Δ)=σ²_G(1/n_early+1/n_late)`, where the one-draw hypergeometric variance is in §4.4. Report the signed standardised `Z=Δ/sqrt(Var0)`, the upper-tail/excess Z for improvement, and lower-tail for deterioration; asymptotic calibration is approximate. Powerball's PB channel analogously uses Bernoulli variance 0.0475.
- **Ranking key:** `Δ` descending for descriptive improvement; `Z_plus` descending for nominal WF signal.
- **Edge cases:** `n<2` undefined; n small explicitly LOW_N; extreme missing-target patterns are disclosed; freeze the split rule before inspecting data and count repeated windows in the testing family.
- **Outputs:** early/late counts, means, `Δ`, variance, Zplus/Zminus, boundary draw numbers, LOW_N.
- **Fair-draw reference:** zero drift and the variance above; independent calibration tests must check approximation for bounded discrete counts.

### MR10 — Top-rank discounted gain (proposed; requires full frozen ranking)

- **One line:** reward placing the eventually drawn numbers very near the top, more strongly than the ordinary average-rank measure.
- **Short explanation:** MR5 gives equal rank-distance weight across all positions. MR10 uses a predeclared reciprocal-log discount, rewarding rank 1 considerably more than rank 20 while still measuring every drawn number. It is a classical ranking measure, **not a new forecast or tie rule**.
- **Exact definition:** for each target, frozen full ranking with midranks `r_j` as defined by R3 and `w_j=1/log2(1+r_j)` (all finite). Let `G_t=Σ_{j∈drawn main}w_j`; fair conditional expectation `e_t=(7/N)Σ_j w_j`, variance `v_t=7*(N-7)/(N-1)*Var_pop(w)` (finite-population sampling without replacement). Aggregate `Σ(G_t-e_t)/sqrt(Σv_t)` for nominal approximate WF Z and report mean raw gain. For the separate Powerball barrel the score is `w_{drawn PB}`, fair expectation `mean(w)` and variance `Var_pop(w)`.
- **Ranking key:** mean gain descending for descriptive table; valid local `Zplus` descending for significance table.
- **Edge cases:** tie midranks honoured; `Σv=0` gives neutral/null-variance status; do not derive a different TOP or WORST ordering—`TIE_SHA256_V1` remains the forecast-time rule. MR10 is **one method/variant ranking measurement**, not two independent readout records.
- **Outputs:** observed mean gain, expected gain, gain excess, Zplus/Zminus, tie/rank metadata, n.
- **Fair-draw reference:** exactly e and v conditional on each frozen score/rank vector; Z is explicitly an approximation and needs independent calibration.

## E. STAGE-1 METHOD-GENERIC CONTRACT: REVIEW OF SECTION 13

**Agree with its timing:** reserve interfaces in the owner-approved **method-generic contract before E_2**, **not** Package 2 v0.11 C1–C6. However separate **metadata declarations** from the much later IS execution engine.

Minimum proposed immutable per-method/variant fields:

1. `game_id`, stable method/variant IDs and version, immutable scientific schema ID, era/profile version, registered `SUPPORTED/FORMULA_OPEN/UNSUPPORTED_FOR_GAME` reason, and method description/name/one-liner **with per-version provenance**.
2. `readout` status TOP/WORST **independently**; `INVERSE_UNAVAILABLE` must not be manufactured. Frozen ticket, main ranking, main per-label scores, Powerball ranking and scores when applicable; exact `TIE_SHA256_V1` encoding/domain identity and digest.
3. `probability_capability`: `NONE` or an explicit typed semantic such as `NORMALIZED_LABEL_PROBABILITY` (`Σq=1`, drawn-label distribution), `MARGINAL_INCLUSION_PROBABILITY` (`Σr=7` and `0≤r≤1`), or PB categorical (`ΣqPB=1`). Do **not** silently infer one from arbitrary numeric scores or a Born-interpretation claim. State calibration/smoothing, full vector order and representation (float64, finite, no narrower widths), provenance and digest. MR14 may use `r/7` in its specific affinity score, but must not claim a full joint ticket distribution from marginals.
4. `IS_capability`: `IS_STATIC`, `IS_STATEFUL`, or `IS_NOT_APPLICABLE`, with a versioned **future** fit/apply contract when genuinely supported. Declaring applicability does **not** authorise IS execution or imply all 62 methods must implement a fit/apply split now.
5. Separate `product_kind`, `run_mode`, `score_status`, evidence tier and **forecast-freeze timing/receipt**. `WF`/`IS` are not scientific readout variants; IS cannot enter the R3 scientific ledger. The result allowlist remains independently strict/empty until authorised.
6. For each track: canonical pre-target forecast identity, target `(game_id,draw_number)`, source master/ledger provenance as permitted, view digest **excluding post-target content**, controlled environment identity, chosen window/comparison cohort, and status captured before opening the target outcome. The master whole-file SHA is provenance only and never a seed.
7. Scorer-only post-outcome record: drawn main set, Powerball when applicable, Oz supplementary matches and prize division, **never fed back to a predictor**; quarantine opening is independently gated. A separate report layer computes MR measures from immutable eligible forecast/outcome pairs.

**Acceptance fields/tests before E_2:** exact shape and numeric contracts, cross-game profile separation, view/digest prefix-only independence (existing T-05), R3 tie and WORST consistency, absent PB/supplementaries in Oz predictor views, evaluation-mode firewall, per-capability not-applicable behaviour, future extension points **without** early implementation of ranking or IS, and a well-defined schema migration/versioning rule. The owner should separately ratify the contract-field schema before development beyond v0.11.

## F. ADDITIONAL OPTIONAL / DESIGN COMMENTS

- **O1:** Record predicted-versus-realised **expected payout** only if official historical per-division payouts are legally sourced and versioned; do not conflate “winning division” with real monetary returns. Current MR1 is a rarity score, not an expected dollar prize.
- **O2:** MR14's quantum terminology is a mathematical analogy (classical squared Bhattacharyya affinity), **not evidence of a quantum mechanism**. This is consistent with the owner's philosophy and should be printed in its glossary.
- **O3:** “No method is deprioritised by score” remains in force. The methods can appear in rank order for observation without suppressing low scorers or changing method eligibility.
- **O4:** For measures computed on overlapping TOP/WORST tracks, retain one source ranking identity and the known paired dependence; never count the two as unrelated evidence.
- **O5:** Require versioned fixed table-family definitions and a **report reproducibility receipt**: exact list of tracks, comparison targets, data version, forecast hashes, registry/measure versions, null-calibration version, test counts, and algorithm/environment identity. Create-only outputs and stable sorting are appropriate.
- **O6:** Clarify that report rows are *per measure/sub-measure, game, mode and cohort*, not one universal scientifically meaningful “best method” league table; selection remains a separately registered meta-method tested prospectively.
- **O7:** Using all lower divisions is scientifically helpful because top divisions are too sparse for most development tracks. The owner's MR1-T remains valid as an explicit, separate **predeclared preference score**, not a statistically optimal weight or a p-value.
- **O8:** The projected cost of “seconds per game” is unverified; exact Fraction tails, many Monte Carlo null replicates, Bayesian quadrature, IS refits and multiple combinations can dominate runtime. State no timing commitment until benchmarked on authorised synthetic fixtures.

## G. DECISIONS TO PUT BEFORE THE OWNER AFTER CLAUDE'S REVIEW

- **DECIDED — preserve:** both games separately; all 9/7 divisions; Oz supplementaries in evaluator only; 90/7/3 MR1-T; WF/IS separation and explicit diagnostic disclaimer; no ranking feeding a predictor without a registered meta-method; no Package 2 v0.11 expansion.
- **RECOMMENDED for owner ratification:** B1 IS significance handling; B2 family-wide conservative multiplicity; B3 spectral descriptive status until valid null calibration; B4 recurrence exposure rules; C1–C10 corrections; optional measures MR6–MR10 as proposals rather than automatically adopted decisions; and the contract clarifications.
- **OPEN pending owner review:** exact multiplicity family/when predeclared (MRO-08); calibration methods and computation budget; MR13 PB direction and priors (MRO-04); minimum-n/LOW_N semantics (MRO-05); supplementary channel for additional measures (MRO-07); probability-vector semantics; optional IS capability execution; future meta-method identity (MRO-06); owner choice to adopt any/all of MR6–MR10.

**Holdout-exposure housekeeping:** The owner should record the unsolicited public-search preview exposure described above in the factual holdout-exposure record, without reproducing numbers or claiming that it had no effect. **Proposed process:** Claude reviews this document, then the owner decides which recommendations to ratify. Only after that should the proposal be integrated into new clean editions of Proposal/R2/R3/Architecture (and any needed task spec/register), with independent review and no addenda. Nothing here changes present authority, holdout access, source acquisition, scientific execution or Package 2 v0.11 C1–C6.

## Sources consulted for rules (no outcome access)

- Uploaded `Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_2.md` (primary source; 770 lines).
- Lotterywest game-information pages (division definitions and *rounded* published odds only): https://www.lotterywest.wa.gov.au/games/powerball ; https://www.lotterywest.wa.gov.au/games/oz-lotto .
- The Lott public playing-guide descriptions (rules only): https://help.thelott.com/hc/en-us/articles/4416863320217-How-do-I-play-the-Powerball-game ; https://help.thelott.com/hc/en-us/articles/4416863329689-How-do-I-play-the-Oz-Lotto-game . This review did not automate, click through to, or intentionally fetch any results pages. **An unsolicited search-result snippet contained quarantined draw values; see the value-free disclosure at the start of this review.** No such values are reproduced here.
