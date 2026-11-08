# Predictive Randomness — R3 Evaluation, Comparison, Evidence and Reporting Specifications

**Version:** 0.1 — first substantive review candidate  
**Date:** 22 October 2026  
**Status:** **DRAFT — NOT RATIFIED; NO IMPLEMENTATION AUTHORISED BY THIS DOCUMENT ALONE**  
**Suggested repository path:** `doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_1.md`  
**Owner:** Project owner, `hydra3333/analysing_perceived_randomness_in_reality`  
**Governing project charter:** `Predictive_Randomness_Research_Project_Proposal_v0_3.md` — **RATIFIED**  
**Governing research catalogue:** `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` — **RATIFIED**  
**Governing method and execution contracts:** `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` — **RATIFIED 22 October 2026**  
**Research method inventory:** E_1 through E_62, all permanently retained; room for up to 100 methods *additional to the original six*.  
**Computing environment:** Windows 11, Python 3.14, project `.venv`, Ryzen 9 3900X (12 physical cores / 24 logical processors), 32 GB RAM.  
**Observed project dataset at drafting:** 444 valid current-rule draws, numbers 1144–1587; first 19 April 2018, last 15 October 2026. The dataset grows; the examples in this document describe that frozen boundary, **not** an instruction to cap future runs at Draw 1587.

> **Purpose.** Specify how experimental forecasts, including TOP and WORST, will be evaluated, compared, archived and communicated; how methods can be combined without hiding hindsight; how synthetic calibration remains a separate research stream; and how genuine weekly future-draw evidence is preserved. The owner deliberately invites unexpected and unconventional explanatory models. The statistical reference model is a measuring instrument, **not** an admissibility test for experimental hypotheses.

> **Critical separation.** A **predictor** determines and freezes TOP, WORST, full rankings and any native joint predictions using pre-target admissible observations. A separate **evaluator** later receives the actual outcome and computes metrics. Neither rank-position scoring nor the future actual result may alter the already frozen prediction. A **researcher** may inspect synthetic diagnostics and redesign subsequent versions transparently, but synthetic observations or fitted artificial states must not be passed off as real historical evidence.

---

## 0. Document authority, vocabulary, and handoff

### 0.1 Document hierarchy and responsibilities

| Document | Governs | Status |
|---|---|---|
| Project Proposal v0.3 | Philosophy, objectives, project-wide research rules and governance | Ratified |
| R1 v0.4 | Method hypotheses E_1–E_62, exact method identities and research foundations | Ratified |
| R2 v0.3 | Training cutoffs, typed method outputs, method registry, separate modes, prediction freezing, seeds, parallelism, numerical contracts | Ratified |
| **This R3 v0.1** | Proposed evaluation formulae, comparisons, prospective evidence policy, reporting schemas, outcome publication and implementation/evaluation acceptance | **Review draft** |
| Later I-stage implementation | Executable Python conforming to the ratified specifications | Not yet begun |

Later approved owner decisions supersede earlier conflicting text. This document **proposes** choices for the owner to ratify; it must not silently amend an accepted R2 contract or decide the first implementation of an unresolved E-method.

### 0.2 Requirement tags

- **[AGREED/R2]**: A requirement explicitly agreed or inherited from the ratified sources.
- **[R3-PROPOSED]**: Proposed here for owner assessment and ratification.
- **[OPEN]**: Not yet fully defined; this draft provides options and a recommended default.
- **[OPTIONAL]**: Candidate advanced analysis; should not block initial core reporting.

### 0.3 Research philosophy, expressed operationally [AGREED]

1. Investigate whether apparently random physical outcomes show exploitable predictive relationships, including unanticipated, nonlinear, speculative, or apparently counterintuitive structures.
2. Do not exclude a method because independent-draw theory, consensus or current physical explanations suggest low likelihood of success.
3. Retain all experimental methods, variants, unsuccessful results, highly correlated methods and unusual observations as auditable research records.
4. Distinguish a precisely computed chance-reference probability from a claim that a real result was *caused* by chance. An unusual observation may remain unexplained for a substantial period.
5. Investigate clearly demonstrated source or implementation defects promptly. A verified error is different from prematurely attributing surprising results to an unspecified error.
6. A real pre-draw prediction, frozen before the outcome and evaluated afterward, is stronger evidence of forecast capability than a retrospective fit; neither is automatically conclusive.
7. Do not equate empirical predictive improvement with a proof of pilot-wave, quantum, physical-equipment, cosmological or other particular mechanisms.

### 0.4 Seed identity clarification raised by Claude [R3-PROPOSED HANDOFF TO R2]

R2 §9.2 lists `selection_model_version` in the stochastic fit seed identity. Clarify its semantics rather than rewriting the ratified text in place:

- The **mathematical sampling/observation model used in fitting** (for example unordered fixed-size-set likelihood versus ordered weighted-without-replacement likelihood) is a legitimate **fit identity** and may change fitting randomness. Its version belongs in the fit seed identity.
- A **downstream readout/selection rule** (`TOP_MARGINAL`, `MAP_SET`, `INVERSE`, display formatting) applied to an *already frozen fit* must **not** perturb fit initialization, optimisation, or latent state. Its identity belongs only to the distinct derived selection output, and possibly a separately seeded sampling/readout operation if that operation is genuinely stochastic.
- Adopt explicit names `fit_sampling_model_version` and `readout_selection_rule_version` at implementation time, with different identity scopes. Add a regression test: changing only the WORST/report selection cannot change the TOP method fit or its frozen full rankings.

**Status:** Non-blocking semantic clarification, recommended as a concrete implementation contract/erratum linked to R2 v0.3. It does not alter the already-ratified document's mathematical intent.

---

## 1. Dataset identity, target modes and protection against look-ahead

### 1.1 Current-rule admissibility [AGREED/R2]

Only the current Australian Powerball format is admitted as real lottery training data: 7 distinct main labels from 1–35 and one Powerball from 1–20, starting at **Draw 1144** on **19 April 2018**. Do not silently mix other historical ball counts or barrel configurations. Draw numbers must be consecutive. Actual calendar dates are source metadata for validation, optional temporal hypotheses and human-readable reporting; ordinary core forecasting boundaries use draw numbers, not precise timestamps.

The two independently maintained source views are the unordered seven-set and the operator-labelled physical *drawn order*. The drawn-order claim rests on operator provenance; it does not mean each historical event has independent broadcast footage authentication. Do not count those two representations of the **same** draw as independent draw observations.

### 1.2 HISTORICAL_EVALUATION [AGREED/R2]

To forecast a known historical target **N**:

1. Supply only permitted real observations ending at N−1, starting at 1144 or the declared shorter rolling window.
2. Fit and freeze all available forecast channels, TOP and WORST where defined, before outcome access by the evaluator.
3. Separately reveal the genuine result for N to the evaluator and compute fixed measures.
4. Archive the original predictions, actual result, scores, status and legitimate lineage. Outcomes from N and later cannot influence the prediction for N.

The latest original ten draws **1578–1587** constitute the reserved final independent historical evaluation set. Do not consume their outcomes during ordinary development, debugging, benchmarks, method/ensemble selection or iterative adjustment. Its eventual authorised opening is a one-time auditable event; subsequent use means those data are no longer an untouched final test for later versions.

**Example at the original source boundary:** development ends at 1577. Ten consecutive benchmark *targets* are 1568–1577 (not the holdout). With complete history they have 424–433 preceding training draws. Benchmarks generate prediction payloads only for computational correctness and deterministic comparison; benchmark **reports must not show or score** results against actuals.

### 1.3 FINAL_NEXT_DRAW [AGREED/R2]

With the latest consecutively validated observed draw L, the next real target is **L+1**. Every available current-rule draw 1144…L, **including what had been the ten final historical holdout draws**, is permitted for the actual final forecast. A particular fully specified E-method may internally adopt a declared rolling window without imposing a global ten-draw exclusion.

The **entire pre-draw FINAL batch** includes one snapshot of every registered runnable method/variant's available outputs and an explicit entry for each blocked, not-yet-runnable, unavailable or failed registry item. Freeze and push the full batch remotely before the actual target event; later results and scoring live in **separate append-only records**, not inside a mutable prediction record.

The cycle repeats for each newly available genuine draw: compare the previously frozen L+1 batch against the new real result, append and validate that result, fit models to all now permitted real history, and prospectively freeze the next L+2 batch. The owner has chosen to start this cycle **after preparation and modelling**, not prematurely with an arbitrary partial implementation.

### 1.4 No accidental data contamination [AGREED/R2]

- Predictors cannot access the evaluator's truth object or post-target results.
- Caches, precomputed features, hyperparameter fits, seed identities and warm starts have the same cutoff as the direct input view.
- Artificial/synthetic observations do not enter a real-data training view or fitted state.
- The SHA-256 of the **entire current CSV** is provenance only, never part of the historical prediction seed or forecast-content identity.
- A prediction for N is byte-identical when N or any later draw is mutated/appended while its permitted training prefix, configuration and software remain unchanged. Archive metadata may differ; compare canonical forecast content independently.
- Benchmark mode is explicitly separated from predictive-merit evaluation. Its reports contain elapsed/CPU time, memory, statuses and equality tests, **not** match or rank scores.

### 1.5 A practical clarification on date/time information [R3-PROPOSED]

No wall-clock data is needed to calculate N−1 training boundaries. Nonetheless, prospective evidence needs a *time of publication* or other externally verifiable pre-draw proof. That is **audit metadata**, not a predictor's mathematical input, unless a specific separately declared time-dependent experiment legitimately uses time. Consequently, there is no contradiction between “draw-number-only predictions” and preservation of remote pre-draw publication evidence.

---

## 2. Prediction data required by evaluation

### 2.1 Frozen forecast contract [AGREED/R2]

For each method/variant and applicable barrel, the evaluator receives a typed, immutable forecast containing the target draw, method and revision, observations admitted, training-view digest, fitting model identity, and available prediction channels:

- `TOP` — **the method's original native declared primary prediction**, often the seven highest-ranked main numbers and highest-ranked Powerball. Preserve lawful joint-set MAP or other native TOP rules without silently substituting the top marginal seven.
- `WORST` — from the same frozen model: the lowest seven marginal ranks in the main barrel and lowest one in the Powerball barrel, when truthful complete marginal rankings exist. The internal rule is `INVERSE`; for native joint-set TOP, use explicit `INVERSE_FROM_MARGINALS`. The `TOP` and `WORST` main sets are **not necessarily disjoint** for a native joint-set TOP.
- `MAIN_RANK` — when rank-capable, frozen deterministic complete ranking of 1…35, with raw scores (if available), tie groups and tie-resolution policy.
- `POWERBALL_RANK` — corresponding 1…20 ranking and tie metadata.
- Optional legal marginals / categorical probabilities / joint-set probabilities / drawn-order probability model, without inventing probabilities for an uncalibrated ranking.
- Typed unavailable/diagnostic/error status where a method cannot produce an output. **No fabricated numbers.**

`WORST` is a deliberately contrarian readout, **not** the lowest likelihood joint 7-set or a claim that the original method intended to forecast it. It is independently tracked because a consistently inverted signal may have scientific interest.

### 2.2 Separation of fit, readout and evaluation [AGREED/R2]

The execution order is:

```text
admissible history -> fit/update -> freeze model and ranking
                                  |
                                  +-> native TOP readout -> freeze
                                  +-> marginal WORST readout -> freeze
                                  |
                            immutable forecast payload
                                  |
                         (actual result only later)
                                  |
                            separate EVALUATOR
                                  |
                  TOP matches | WORST matches | rank position
```

No evaluator metric, including rank-position mean or mid-rank values derived from the actual draw, may affect the method's TOP/WORST output or its fit for the same target. This prohibition includes indirect configuration or runtime feedback. A later genuinely new forecast is allowed to use **earlier known actual draws** as training observations, as long as the method/revision policy was honestly declared and the prospectively frozen prior forecasts are preserved.

### 2.3 Selection labels and availability [R3-PROPOSED]

| Field | Meaning | Unavailability |
|---|---|---|
| `top_main_set` | Exactly seven distinct numbers from 1–35 | `TOP_MAIN_UNAVAILABLE` with reason |
| `top_powerball` | Exactly one number from 1–20 | `TOP_PB_UNAVAILABLE` with reason |
| `worst_main_set` | Lowest seven from same frozen main marginal ranking | `INVERSE_MAIN_UNAVAILABLE` |
| `worst_powerball` | Lowest from frozen Powerball ranking | `INVERSE_PB_UNAVAILABLE` |
| `mean_rank_main` | **Evaluator-only**, after real result exists; average mid-rank of the seven actual main balls | `RANK_MAIN_UNAVAILABLE` |
| `rank_powerball` | **Evaluator-only**, after real result exists; mid-rank of actual Powerball label | `RANK_PB_UNAVAILABLE` |

Availability is **per barrel and per channel**. Missing Powerball capability does not erase a legitimate main prediction. A missing inverse must not be substituted with random numbers, a previous prediction or another method's ranking.

### 2.4 Ties [R3-PROPOSED/OPEN R2 DETAIL]

Prediction-time tie-breaking remains an R2 open mathematical/design question. Recommended simple deterministic policy: among equal scores, break ties by ascending label in frozen descending-score order; the inverse is the **exact reversal of that frozen order**, not a second separately sorted ascending-score list. This makes T-31 reproducible. Its selection influence is part of the declared method readout version; it is not fed back into fitting.

For **post-draw rank-position**, tied scores receive **mid-ranks**, meaning the average positions occupied by their tie group. An all-tied main ranking assigns rank 18 to every label, and an all-tied Powerball ranking assigns rank 10.5 to every label. Neither tie-derived midpoint may change TOP or WORST.

Any stochastic prediction-time tie breaker must have a separate independently derived readout seed, not feed into the model-fit seed and not depend on target outcomes.

## 3. Required TOP, WORST and rank-position measures

### 3.1 Definitions [R3-PROPOSED FORMALISATION OF AGREED OUTPUTS]

For a target draw N, let:

- `A_N` = actual **unordered** set of seven main numbers, |A_N| = 7.
- `p_N` = actual Powerball number.
- `T_N` = frozen TOP main seven-set when present; `t_N` = frozen TOP Powerball number.
- `I_N` = frozen WORST main seven-set when present; `i_N` = frozen WORST Powerball number.
- `r_N(j)` = **evaluator mid-rank** of main label j (1 = highest predicted rank; 35 = lowest), derived from the frozen *scores/tie groups*, never the actual outcome.
- `q_N(j)` = Powerball label j's frozen evaluator mid-rank (1 = highest; 20 = lowest).

**Required primitive scores:**

```text
MAIN_TOP_MATCHES(N)     = |T_N intersection A_N|        integer 0..7
PB_TOP_HIT(N)           = 1 if t_N == p_N else 0       integer 0/1
MAIN_WORST_MATCHES(N)   = |I_N intersection A_N|        integer 0..7
PB_WORST_HIT(N)         = 1 if i_N == p_N else 0       integer 0/1
MAIN_ACTUAL_MEAN_RANK(N)= (sum over j in A_N of r_N(j)) / 7
PB_ACTUAL_RANK(N)       = q_N(p_N)
```

Each primitive is recorded **only when its required frozen channel exists and the genuine target outcome is known**. There is no automatic single scalar combining all six. Keep TOP and WORST **side by side in the method's report row**, with rank position in its own clearly marked post-draw column(s).

### 3.2 Main and Powerball remain distinct [AGREED/R2]

Never report “eight matching numbers” as though seven-from-35 and one-from-20 are a single eight-number draw mechanism. Combined human-readable display is encouraged, but retain independent main and Powerball counts. If useful, a combined result class may show `(main_matches, powerball_hit)` separately for TOP and WORST, **without** giving the Powerball an arbitrary coefficient. Prize-division style summaries would require exact game-rule mapping and are optional; none are used for fitting or selection here.

### 3.3 Rank position is strictly post-outcome evaluation [AGREED/R2]

The rank-position metric reports **where the numbers that actually appeared fall in the method's already-frozen rankings**. It is not a “third predicted draw”, not another TOP/WORST selection, and not a knob to make either prediction better after the result.

For main numbers, report the arithmetic mean of seven mid-ranks; optionally add the seven individual actual-number ranks as traceability columns in a detail file. For Powerball, report the one actual label's mid-rank. Lower scores suggest the method's top end ranked actual labels higher; higher scores suggest its bottom end did so. This descriptive direction is **not** an automatic causality claim.

Mid-ranks are invariant to arbitrary tie-breaking in the recorded frozen deterministic prediction order. Changing a tie-break policy may change a selection on a future draw, but **cannot** retrospectively change recorded TOP, WORST or the mid-rank measure for an already frozen forecast.

### 3.4 A small illustrative example (not an actual prediction)

A method's frozen main TOP might be `2,7,11,18,24,30,35`, while WORST might be `1,5,13,19,22,28,33`. If the next actual set were `2,5,11,12,19,26,30`, then `MAIN_TOP_MATCHES=3` (`2,11,30`) and `MAIN_WORST_MATCHES=2` (`5,19`). The rank-position mean must still be computed **separately from the full frozen 35-ranking**. It is not reconstructed from the top seven and bottom seven, and cannot change either prediction.

### 3.5 Aggregation across targets [R3-PROPOSED]

For a fixed track with valid forecasts on `n` eligible targets, report:

- Counts of valid, missing, failed, unavailable and out-of-scope targets, with original denominators retained.
- TOP main: `sum_main_top_matches`, `mean_main_top_matches`, histogram of 0…7 matches, and per-target values.
- WORST main: corresponding sum, mean, histogram and per-target values.
- TOP/WORST Powerball: hits and attempts, empirical hit proportions, and per-target values.
- Main rank-position: mean (and median/range or distribution when informative) over the eligible target records with genuine 35-rank output.
- Powerball rank-position: corresponding mean/summary over valid 20-rank records.
- Evidence by time block and exact track revision; do not pool incompatible algorithm revisions into an apparently homogeneous performance series without a disclosed aggregation policy.

The rank-position average and main-set overlap use different underlying measures. A method can have a promising mean rank without having the most high-overlap TOP draws; **report both without substituting one for the other**.

### 3.6 Missingness is a reported outcome, not a free pass [R3-PROPOSED]

A valid absence of a Powerball model is not a Powerball prediction failure; it is `NOT_APPLICABLE`/`UNAVAILABLE`. A runtime crash, timeout or nonfinite output is a **failure**, not a successful abstention. Both remain in the original assigned-target audit denominator, while probability estimates use clearly identified valid-attempt denominators. The report shows coverage to prevent methods with three fortunate predictions among hundreds of missed origins appearing better than consistently runnable methods merely through denominator selection.

Do not collapse `RUNTIME_FAILURE`, `INSUFFICIENT_HISTORY`, `DIAGNOSTIC_ONLY`, `NOT_IMPLEMENTED`, `INVERSE_UNAVAILABLE` and `PREDICTION_AVAILABLE` into one “no score” category. Excluding an attempt from a particular statistic is **not** removal from the registry or from its public record.

### 3.7 Unordered versus drawn-order scoring [R3-PROPOSED]

The primary TOP/WORST main-number overlap scores compare unordered label sets even for a method fitted using operator-labelled drawn order; the requested seven-number prediction is still a seven-set when evaluated for numbers drawn. For a method that additionally forecasts the *order*, preserve its native ordered forecast/probability as an additional typed record and analyse it with separately defined, mathematically appropriate ordered metrics. Do **not** use its predicted order to silently replace or reinterpret the required TOP/WORST seven-set scores. Report which observation view trained each variant.

## 4. Reference-model values: measuring rulers, never research vetoes

### 4.1 Exact distribution for main matches [R3-PROPOSED]

When a fixed legal seven-number prediction is compared with a uniformly selected independent seven-set from 35, let M be the number of matching main numbers. The exact reference distribution is:

```text
P(M = k) = C(7,k) * C(28,7-k) / C(35,7),       k = 0..7
E[M] = 7 * (7/35) = 1.4
Var[M] = 7*(7/35)*(28/35)*(28/34) = 0.922352941176...
SD[M] = 0.960392076798...
```

where C denotes the exact integer binomial coefficient. No binomial approximation treating the seven draws as independent is needed for these single-prediction probabilities.

| k matches | Reference probability |
|---:|---:|
| 0 | 0.1760780 |
| 1 | 0.3921737 |
| 2 | 0.3069186 |
| 3 | 0.1065689 |
| 4 | 0.0170510 |
| 5 | 0.00118046 |
| 6 | 0.0000291471 |
| 7 | 0.0000001487095 |

`P(M >= 4) = 0.01826078` (about one in 54.8) and `P(M >= 5) = 0.00120975` (about one in 826.6). Exact entire seven-set match is one in **6,724,520** for one fixed seven-set against one independent uniform draw.

The same **marginal single-prediction** distribution applies to a legal TOP or WORST seven-set. TOP and WORST within a method are generally **dependent**, and different E-methods/variants are often correlated. Do not apply the independent-predictions formula to a full weekly batch unless independence has actually been justified.

### 4.2 Powerball reference [R3-PROPOSED]

For any one legal predeclared Powerball value, the reference hit probability is `1/20 = 0.05`. For ten fixed, independent future targets, a particular unchanged-meaning predeclared selection stream getting at least two hits has reference probability approximately `0.08614`; this does not imply the same probability for an adaptively selected best-of-many track. Within a ranking, TOP and WORST Powerball numbers are different (assuming a complete ranking) and cannot both match the same actual one-number Powerball on the same draw.

### 4.3 Rank-position reference [R3-PROPOSED]

For a frozen complete ordering of 35 labels, selecting seven actual labels uniformly without replacement yields mean actual rank **18.0**. With distinct ranks 1…35, the one-draw standard deviation of their mean is `sqrt(12) = 3.4641`. Ties handled by mid-ranks preserve the reference expected mean 18.0, **but change the variance**; do not automatically use `sqrt(12)` with many ties.

For the one Powerball actual label, its complete rank is uniform on positions 1…20 under the reference and absent ties: expected rank **10.5**, standard deviation `sqrt(33.25) = 5.7663`. Ties preserve the mean with mid-ranks but can change the variance.

Lower-than-reference average rank suggests that a predeclared ranking placed later drawn values nearer the top; higher-than-reference suggests a stronger inverse ranking. Neither observation tells the evaluator to reverse a previously frozen TOP forecast.

### 4.4 A hit-rate comparison must say *which* claim it addresses [R3-PROPOSED]

Separate:

- **One fixed track:** a predefined method/revision/readout whose performance can be compared with an appropriate single-track reference.
- **A searched winner:** the best of many tried configurations, rankings, selection variants or combinations. The maximum is expected to be more extreme than a single track even under a fair model.
- **A prospective batch claim:** “some method in this complete batch achieved X.” Its reference depends on the joint dependence structure of the declared roster.
- **Persistent performance:** a named, versioned track's sequence across genuinely prospective weeks.
- **Prediction success:** statistical fit or forecasting performance, which is distinct from a physical causal mechanism.

Chance-reference probabilities should accompany relevant noteworthy hits where the reference applies. They may inform further investigation; they cannot be used as an automatic “this must be coincidence” verdict.

---

## 5. Additional accuracy/probability measures [R3-PROPOSED, OPTIONAL INITIALLY]

### 5.1 Important input distinction

A ranking or arbitrary score is not automatically a calibrated probability. Do **not** transform scores to fabricated probabilities merely to fill report columns. Extra probabilistic metrics are available **only** where the method legitimately supplies normalized probabilities or a valid model-defined likelihood, and must be compared on like-for-like targets/views.

### 5.2 Powerball categorical proper scores

For valid categorical probabilities `q_j >= 0`, `sum_{j=1..20} q_j=1`, with actual Powerball p:

```text
POWERBALL_LOG_LOSS = -ln(q[p])
POWERBALL_BRIER_SUM = SUM_{j=1..20} (q[j] - I(j=p))^2
```

The fair uniform reference is `q_j=0.05`; hence reference log loss is `ln(20)` and reference Brier sum is `0.95`. A model assigning zero probability to the actually drawn outcome has mathematically infinite log loss and must not be silently converted to a finite score. If numerical clipping is proposed, its deterministic clipping policy must be declared and fixed *before* evaluation, with clipped and unclipped semantics clearly distinguished.

### 5.3 Main marginal probability scores

For coherent legal seven-of-35 marginal inclusion probabilities `p_j` in `[0,1]` satisfying `sum p_j=7`, an optional **marginal Brier sum** is:

```text
MAIN_MARGINAL_BRIER_SUM = SUM_{j=1..35} (p[j] - I(j in A_N))^2
```

Under uniform `p_j=0.2`, its fair reference expectation is `35*0.2*0.8 = 5.6`. This is a marginal event score, not the probability of the observed seven-set and not evidence that ball-inclusion indicators are independent. Invalid or unconstrained scores do not qualify for this metric.

### 5.4 Joint-set and ordered likelihood

If a method declares a properly normalized joint probability on legal seven-sets, optionally compute `-ln P(A_N)`; uniform reference `ln C(35,7)`. If it declares a legal ordered-sequence distribution and the actual operator-labelled order is available, optionally compute `-ln P(a_1,...,a_7)`; uniform reference `ln(35*34*33*32*31*30*29)` for a fixed ordered sequence of seven distinct labels.

Do not compare raw ordered and unordered negative log likelihood numerically as if they cover the same outcome space. Do not double-count both representations of the same draw as independent evidence.

### 5.5 Calibration and reliability diagrams

Optional future analyses: reliability bins for marginal inclusion probabilities; calibration error, distributional sharpness, and aggregate forecast-vs-outcome plots. Calibration diagnostics must report the number of independent target draws and the within-draw dependence of 35 labels. A single 35-label draw is not 35 independent lottery draws.

### 5.6 Optional score decision [OPEN]

The owner has already required TOP/WORST and rank-position scores. This draft recommends that proper probability scores **remain additional capability-dependent measures**, not a replacement or a condition of E-method eligibility. Detailed numerical presentation and precision policy can be finalised during implementation design or in a controlled R3 revision before live launch.

## 6. Evaluation windows, holdout, adaptive choices and comparable series

### 6.1 Development walk-forward blocks [R3-PROPOSED]

Historical evaluation must specify both its target range and exactly how the fit at each target uses preceding observations. Suggested standard report views when sufficient valid targets exist:

| View | Purpose | Treatment |
|---|---|---|
| `DEV_ALL_ELIGIBLE` | All development-period walk-forward targets for which the particular method's minimum history is satisfied | Primary retrospective breadth, before holdout |
| `DEV_LAST_100` | Most recent 100 development targets | Recency comparison |
| `DEV_LAST_50` | Most recent 50 development targets | Recency comparison |
| `DEV_LAST_10` | Most recent 10 **development** targets, ending at 1577 in the frozen starting snapshot | Diagnostic only; **not** the reserved holdout |
| `FINAL_HOLDOUT_10` | Draws 1578–1587 | Only once explicitly authorised, immutable report, no subsequent claim that it remains pristine after tuning |
| `PROSPECTIVE_ALL` | All genuinely archived-before-draw FINAL target batches | Strongest temporal provenance; track versions and skipped weeks |
| `PROSPECTIVE_LAST_K` | The most recent K genuine prospectively frozen targets, K identified in every report | Descriptive moving view; cannot be cherry-picked or presented alone |

Do not hard-code today’s observed endpoint into evaluation code. Target ranges must derive from a versioned study plan and the available source. Some methods will have too few valid origins to support a full 100-target block; retain and disclose the shortfall rather than creating artificial data.

### 6.2 Separation of discovery, tuning and final evaluation [R3-PROPOSED]

- Use development targets to explore models, mathematical variants, tie rules, forecasting adapters, hyperparameters and ensembles. These choices may legitimately be informed by *permitted past real outcomes*, with full disclosure of the tried search.
- Record the exact candidate configurations tried, including losing configurations; a selection process that searches extensively has a different evidential interpretation from one frozen before the search.
- Reserve the original 1578–1587 results as a final untouched evaluation until the owner explicitly authorises opening. Do not send holdout outcomes to predictors, optimisers or human-selected method rules during development.
- Before opening it, freeze a study manifest identifying method/variant versions, evaluation rules, exact track hypotheses, and planned report outputs. When the holdout is opened, record this in an append-only audit record.
- Never silently claim that an already opened or indirectly used holdout remains independent. New genuinely future-draw targets can provide new prospective evidence, provided corresponding forecasts are frozen beforehand.

### 6.3 Changing method definitions and longitudinal integrity [R3-PROPOSED]

Every scientifically meaningful change to an E-method fit algorithm, readout, feature processing, hyperparameter policy, permitted data view, ensemble membership or weight policy must receive a new immutable method **revision/configuration identity**. Earlier forecasts retain their own version and track. A user's desire to explore an improved method after observing a success or failure is fully legitimate; the new predictions must not be backdated as if made by the prior frozen version.

Report BOTH:

1. **Version-stratified results**, allowing assessment of a particular unchanged method/configuration across targets.
2. **Operational portfolio results**, describing what the full evolving project actually forecast each week, including revisions, failures, new models and changes in nominated primary outputs.

Do not treat the version-stratified and evolving-portfolio series as equivalent.

### 6.4 Fair method comparison [R3-PROPOSED]

Compare two methods on their **common eligible target dates** when claiming one did better than the other. Record this paired target count and which origin filters are active. Also show each method's full own-history record and coverage. For paired main-match differences, compute per-target `(A_top_matches - B_top_matches)` (or analogous WORST/rank differences) before aggregating, instead of comparing means over different time windows and mistaking data availability for performance.

A method receiving operator-drawn-order information and another using only unordered sets may be compared for forecast output performance, but their input capabilities and observation views must be disclosed. The order series is not a second independent sample of draws.

### 6.5 Overlap among TOP/WORST outputs [R3-PROPOSED]

For a marginal top-seven/bottom-seven ranking, TOP and WORST are disjoint. For a whole-set native TOP and marginal WORST, **overlap is permitted** and is not a validation failure. Report a same-method TOP–WORST overlap measure as a diagnostic only when useful; never assume the two track outcomes are independent in chance analysis.

---

## 7. Statistical interpretation, uncertainty and multiple investigations

### 7.1 Basic principle [AGREED]

The project tests the possibility of structure that accepted probability/physics might not anticipate. Reporting a reference-model probability is **not** equivalent to declaring that all realities must obey that model. Conversely, surprising performance is not by itself a proof of causation or an identified hidden mechanism. A method is never deleted, suppressed or prohibited from combinations because a conventional statistical test is unpersuasive.

### 7.2 Descriptive results first [R3-PROPOSED]

Every evaluation report begins with what was **actually forecast**, what was **actually observed**, the evaluation formula, and its denominator. Uncertainty bands, reference p-values, synthetic calibration and mechanism hypotheses are separate clearly labelled layers. Do not place explanatory labels such as “random luck” into an observed-result field.

### 7.3 Uncertainty for a fixed, predeclared track [R3-PROPOSED]

For a fixed legal predeclared selection on each target, under a stated independent-uniform reference, the main-match average's standard error across `n` independent target draws is `0.960392... / sqrt(n)` if the prediction sets were selected without outcome leakage. The analogous Powerball hit proportion reference standard deviation is `sqrt(0.05*0.95/n)`. Such simple formulas are **conditional reference calculations** and do not automatically apply after selection among many retrospectively tried methods, to cross-track maxima, or when the hypothesised reality induces dependence across draw outcomes.

The report should show sample size and clearly labelled uncertainty intervals whose construction is recorded. For small Powerball hit counts, prefer an exact binomial calculation under the reference or a justified Wilson interval for an estimated observed hit proportion; avoid unqualified normal approximations based on tiny counts. For empirical main match means, uncertainty methods can include time-block bootstrap or explicit sequential modelling if dependence is being investigated; never silently assume its outcome proves independence.

### 7.4 Multiple testing and the search record [R3-PROPOSED]

Maintain an auditable `search_history` / `method_selection_log` with trial configurations, learning windows, candidate combinations, reporting rules inspected and reasons for selecting a candidate. An observed best-of-100 configurations should be described differently from a single fixed forecast track. The project may use synthetic null-world whole-pipeline calibration to compare real extremes with extremes a declared null system produces after **the same search procedure**. Synthetic results affect *interpretation and disclosed design*, never contaminate real fitted model states.

Possible inferential reporting includes per-track reference tail probabilities, simulation-based familywise comparisons and false-discovery summaries; the choice, assumptions and calibration scope must be explicit. This is **not** a prescription to eliminate statistically weak, unusual or correlated methods.

### 7.5 Batch-wide chance context [R3-PROPOSED]

For each weekly FINAL batch, report the exact numbers of attempted TOP and WORST channels, distinct rankings, available barrel components, shared/nested variants and exceptions. When describing “at least one method scored four or more” or a similar across-batch event, do **not** compute `1-(1-p)^m` by default: rankings and methods can be highly dependent, and TOP/WORST are paired outputs from the same model. An explicitly documented batch-aware reference simulation can estimate the selected event with the **actual frozen roster** and dependencies; do not present synthetic observations as real lottery outcomes.

**Worked perspective (not an accusation of coincidence):** Under the single-track independent reference, a legal seven-set prediction has probability about 0.01826 of four or more matches. Across many methods and readouts, witnessing at least one such hit may become common even when no method has an individual advantage. This is a reason to maintain per-method longitudinal histories, not a reason to dismiss a particular unexpected hit.

### 7.6 Real-world sequential evidence [R3-PROPOSED]

After the forecast batch for target N has been frozen before the draw, the actual N result can be appended to an independent outcome ledger. The evaluator then scores the **already frozen** predictions. The next target N+1 can use actual N as one of its genuine historical training observations. Evaluation may accumulate across many genuine weeks, with explicit version changes and no deletion of missed/failed attempts.

Do not impose a magical “three successes”, “ten weeks” or similar minimum before a result is worth investigating. Several favourable weeks justify scrutiny, but the number of independent prospective targets and prior selection history still matter for strength of evidence. An absence of measured advantage is also not proof that no unexpected structure exists under every conceivable method.

### 7.7 Interpretation ladder [R3-PROPOSED]

Use precise language distinguishing:

1. **Observed fact:** the method predicted this set, and these values actually appeared.
2. **Measured performance:** a named predeclared score or sequence reached a stated value.
3. **Comparison:** under a specified reference model or simulation, the value has stated uncertainty or tail probability.
4. **Predictive signal hypothesis:** repeated genuine evidence suggests performance may differ from a comparator; still qualified by the search design.
5. **Causal/mechanistic hypothesis:** an explanation for why performance occurs, requiring independent distinguishing evidence.
6. **Broad philosophical inference:** any claim about perceived reality or time/quantum mechanisms, requiring substantially more than the original performance statistic.

A verified data/parser/implementation error is recorded as a distinct **technical finding**, with affected results visibly marked; such evidence can be established at any time. Without evidence, “coincidental fit”, “artefact” and “error” are only possible explanations, not labels to attach reflexively.

### 7.8 Performance and rank correlation [R3-PROPOSED]

Compute agreement between method frozen rankings, TOP sets, WORST sets, per-target overlap scores, and temporal patterns as optional **descriptive** quantities. Same-family similarities do not independently validate a signal and do not remove eligibility for combination. Rank correlation on frozen rankings can be compared across targets, including its volatility; a method that is consistently inverse to another remains scientifically eligible.

---

## 8. Combination experiments and research-selection policies

### 8.1 Permanent availability [AGREED]

All E_1–E_62 and future admitted E-methods remain in the registry. A poor, highly correlated, expensive, speculative or diagnostic-only method is never discarded because of conventional plausibility or observed standalone rank. Missing capability must be represented truthfully. A combination may include any such method when a mathematically specified interface makes that possible.

### 8.2 What an ensemble may consume [R3-PROPOSED]

At target N, an ensemble consumes only the **target-N pre-outcome frozen outputs**, admissible training-side features, and any selection/weighting parameters learned from genuinely earlier known draws. The graph of constituent dependencies is acyclic, with explicit method revisions and observation views. It cannot consume the actual result of N, an evaluator's post-N score for N or hidden synthetic-fitted states. A method that has only diagnostic signals may contribute through a separately versioned and truthful adapter, not invented probabilities.

### 8.3 Candidate combination families [R3-PROPOSED EXPLORATORY]

Without deciding a preferred method, R3 proposes permitting a wide family of declared combination rules:

- Uniform or weighted rank aggregation, including ranks of TOP or inverse methods.
- Aggregation of legal marginal inclusion probabilities (when supplied coherently).
- Joint-set-aware combination of valid probability models, with a legal seven-of-35 output mechanism.
- Diversity/complementarity-aware aggregation and deliberately correlated ensembles.
- Conditional or regime-specific mixture-of-experts rules learned on permitted training observations.
- Time-varying weights based on **prior** observed forecast performance, with fixed update formulas and no leakage.
- Explicitly contrarian combination rules, including an input method's frozen WORST/inverse rank.
- Search or evolutionary procedures over ensembles, with transparent search-history accounting and holdout safeguards.

These are categories, not secretly ratified E_55/E_56 implementations; each scientific combination receiving its own E-number needs owner approval according to R2/R1 governance.

### 8.4 Selection, weighting and inversion timing [R3-PROPOSED]

- A standalone E-method's TOP and WORST readouts are **not** retrospectively reversed because WORST outperformed TOP last week.
- A newly designed future contrarian E-method or ensemble may deliberately use prior known data to weight or invert an input ranking, but its versioned rule must be frozen **before the target** and receive its own stated identity.
- Track the inverse side as a **separate prospective series** even if an ensemble internally uses inversions.
- Do not promote an evaluator metric such as current-target actual rank position into a prediction rule after seeing the outcome.
- Using earlier rank-position results as a *future* adaptive ensemble training signal is an **open policy question**: although mathematically possible with proper temporal cutoffs, it must never redefine the standalone method's frozen TOP/WORST for any past or present target. Proposed default for the first implementation: **no automatic ensemble update from rank-position scores until a separately ratified adaptation rule is specified**.

### 8.5 Ensemble comparison [R3-PROPOSED]

Report each combination as an independent named, versioned track, alongside its constituent source-method IDs/revisions and exact target coverage. Distinguish whether improvements were seen during exploratory selection, on the once-only final holdout, or in subsequent genuinely frozen prospective draws. A candidate combination may be retained despite no improvement; the project need not require proof of synergy for registration or further investigation.

---

## 9. Synthetic calibration, planted effects and diagnostic separation

### 9.1 Three different evidence streams [AGREED/R2]

**REAL DEVELOPMENT:** Authentic draw results within declared historical cutoffs, used to fit models and investigate predictive capability.  
**REAL PROSPECTIVE:** Forecasts immutably published before unknown future draws, then scored afterward.  
**SYNTHETIC RESEARCH:** Separately generated null-world/planted-effect or identifiability inputs, used to test the research apparatus and sensitivity. They are not real successes.

Additional computational **BENCHMARK** output is timing/resource evidence only and should not be shown as a predictive-merit result. Operational statuses must identify these namespaces and block unintended cross-namespace input.

### 9.2 Synthetic null-world runs [R3-PROPOSED]

Draw synthetic histories with an explicitly declared generator. Feed them to the same *software machinery* while isolating source paths, result namespaces, random seeds, fitted state, reports and log provenance. Permitted uses: measure how the whole method-selection search behaves under the declared generator, assess numerical robustness, obtain reference distributions of batch extremes and understand sensitivity limits. Thousands of independent artificial histories are permitted where useful and computationally feasible.

Reference generator assumptions must be recorded precisely, including number of draws, seven-without-replacement mechanics, Powerball range, date/draw-number policy and any within- or between-target dependencies. A fair synthetic generator is only one **chosen mathematical world**, not a postulate that reality must follow it.

### 9.3 Planted-effect runs [R3-PROPOSED]

Specify artificially introduced effects (e.g. uneven ball propensities, recurrence hazard bumps, hidden regimes, periodic fields, coupled selection, ordering effects and equipment-transition relaxation). Measure recovery of predictive patterns, recovery of hidden parameters where identifiable, and practical sensitivity **separately**. A method that cannot recover its own planted mechanism in 440 artificial draws may still run on real data; such a finding is a disclosed diagnostic, not an exclusion veto.

### 9.4 Allowed influence versus forbidden contamination [AGREED/R2]

**Allowed, disclosed:** Lessons from simulations may inform engineering choices, numerical solvers, model families, research priorities, identifiability diagnostics, fitting feasibility and how evidence is interpreted. Such choices create recorded method/configuration revisions.

**Forbidden:** Passing synthetic observations, fitted synthetic hidden trajectories, fitted artificial model weights, artificial target outcomes or simulated prediction scores into an authentic real-data forecast as though they were historical real observations or its legitimately fitted state. A real predictor's fit/forecast depends on its permitted real training view and declared method configuration only.

Test invariance of a fixed real forecast under alteration or deletion of unrelated synthetic study files. Because an *explicitly revised* model can reflect a design lesson from synthetic research, do not confuse disclosed later design changes with direct dataset contamination.

### 9.5 Synthetic research reports and cross-stream narratives [R3-PROPOSED]

A synthetic report may name real-data findings it helps interpret, with its own generator/seed/configuration provenance. It must never add simulated draws to a real method's match histogram or pool synthetic and real evaluation rows without strongly enforced source-class separation. A cross-stream narrative is an **interpretive report**, not one unified performance leaderboard.

---

## 10. Prospective weekly FINAL batch protocol

### 10.1 Preconditions for the first FINAL forecast [AGREED AND R3-PROPOSED]

Before authorising the first genuine target forecast:

1. The R3 scoring formulas for TOP, WORST and rank position are reviewed and **ratified**.
2. Each runnable method/variant has a frozen implementation/configuration, stated input/output capabilities, and the R2-required engineering and leakage tests passed or explicitly owner-approved exceptions recorded.
3. The full registered roster is enumerated: runnable variants, diagnostic-only methods, unavailable implementations and expected failure semantics; no method is silently removed.
4. Required source files have been refreshed, validated and identified by cryptographic digests.
5. The current largest validated actual draw number L is identified. Target is L+1; the draw must not already have occurred at forecast publication time.
6. Batch manifest and publish/proof mechanism are in place; a complete frozen prediction bundle can be pushed to the declared remote before the draw.
7. All current TOP/WORST and rank-position scores use predeclared definitions. Statistical interpretations and test exceptions are identified, even if some advanced evidence thresholds remain exploratory.

### 10.2 Freeze and publication process [R3-PROPOSED]

```text
SOURCE REFRESH -> VALIDATE -> RECORD L AND SNAPSHOT DIGESTS
  -> BUILD TARGET L+1 AND PERMITTED TRAINING VIEWS
  -> ENUMERATE ALL REGISTERED METHODS/VARIANTS
  -> FIT / FREEZE MODEL; GENERATE TOP + WORST WHERE AVAILABLE
  -> VALIDATE AND SERIALIZE CANONICAL FORECAST CONTENT
  -> BUILD COMPLETE BATCH MANIFEST + STATUSES + CONTENT DIGESTS
  -> FREEZE BUNDLE; COMMIT AND PUSH TO REMOTE BEFORE DRAW
  -> SAVE REMOTE REVISION/PUSH EVIDENCE IN AUDIT RECORD
  [ACTUAL L+1 NOT YET KNOWN]
       ...later...
  -> RECORD ACTUAL RESULT IN SEPARATE OUTCOME LEDGER
  -> EVALUATE THE PRE-EXISTING, FROZEN BATCH; PUBLISH REPORT
  -> APPEND NEW VALIDATED DRAW TO REAL SOURCE; PREPARE NEXT L+2
```

A saved local prediction without reliable pre-draw evidence is still scientifically interesting but must not be mislabelled “verified prospective” unless the required timing evidence exists. An author timestamp in a Git object by itself is insufficient; archive remote ref/commit IDs and independent evidence of timely availability. Choose a practical verification method and test it before the first production run; **automated GitHub push is a workflow target, not a claim that current Python has permission to push**.

### 10.3 Complete manifest and append-only record [R3-PROPOSED]

The immutable original target batch contains the exact roster, including every registered E-method and runnable supported variant, their IDs/revisions, native TOP and available WORST, channel-specific unavailable statuses, and numeric/failure diagnostics. Explicitly distinguish a model not implemented from one actually attempted and failed. A hash-tree/manifest can identify the content bytes; canonical hash semantics follow R2.

After the target is drawn, never append the actual outcome *inside* that original immutable batch. Instead create an outcome record and a separately versioned evaluation record whose parent references the frozen batch hash and target draw. If a real outcome is corrected by an authoritative source, append an outcome **correction revision** and a corresponding amended evaluation, preserving the earlier publication as history rather than overwriting it.

### 10.4 No post-draw additions [AGREED/R2]

A method that was not runnable at freeze time cannot have its retrospectively generated successful prediction inserted into the original batch. Recomputations for debugging, new source corrections, alternative fits and newly invented method versions may still be researched, but they are marked **RETROSPECTIVE** with new run IDs and do not acquire historical proof of pre-draw publication.

### 10.5 Prospective continuity [R3-PROPOSED]

For each weekly target, retain `PUBLISHED_BEFORE_DRAW`, `TIMELINESS_UNVERIFIED`, `MISSING_BATCH`, `PREDICTION_FAILED`, `OUTCOME_PENDING`, `OUTCOME_AVAILABLE`, or relevant separate statuses. Report missing weeks rather than silently skipping them. Once the target is complete, preserve distinct TOP and WORST series per `(E-method, revision, variant, barrel, observation_view, readout_rule)`.

A next-week forecast may use the prior week's newly published actual as **real historical training**. It may also contain transparently updated adaptive weights based on earlier legitimate outcomes if that adaptation rule had been predeclared. It may **not** revise last week's original TOP, WORST or post-draw scoring definition.

## 11. Report and data-product specifications

### 11.1 Design rules [R3-PROPOSED]

- Human-readable reports and machine-readable results must be derived from the **same frozen canonical forecast** and separately archived actual/evaluation objects, rather than independently recalculating selections for display.
- Maintain TOP and WORST **adjacent in the same method row**, never split across unrelated tables that prevent direct side-by-side inspection.
- Separate pre-draw forecast presentation from after-draw scoring. A public prediction page must not include future actual-derived ranks, matching values or hints from later outcome data.
- Reports distinguish draw number, relevant date (if present), method and variant revision, data view, barrel availability, TOP readout rule, WORST/inverse rule, incomplete/failed status, provenance and whether the run was historical, synthetic or genuinely prospective.
- Represent mathematically undefined quantities as `NOT_AVAILABLE` plus a reason, not as zero, a blank that resembles zero, or a fabricated worst set.
- Avoid an automatic combined “best method” scalar until the owner has approved the rule; preserve the original individual main/PB metrics and the method roster.

### 11.2 Pre-draw next-draw report (numbers only) [R3-PROPOSED]

For a real next-draw batch, show a row such as:

| Method / variant | TOP main (7) | TOP PB | WORST main (7) | WORST PB | Status / readout notes |
|---|---|---:|---|---:|---|
| E_1 / v1 | `2 7 11 18 24 30 35` | 9 | `1 5 13 19 22 28 33` | 17 | Illustrative invented numbers; full ranking stored |
| E_57 / v1 | `...native set...` | unavailable | `...lowest marginal...` | unavailable | TOP=MAP_SET; WORST=INVERSE_FROM_MARGINALS |
| E_x / diagnostic | unavailable | unavailable | unavailable | unavailable | DIAGNOSTIC_ONLY; no fabricated picks |

**Illustrative values only.** The pre-draw report MUST omit `TOP_matches`, `WORST_matches`, `actual_rank_mean`, and any post-result performance label for that same target. It can show earlier completed-draw evidence in a **separate retrospective/prospective history section** with unambiguous dates and origin provenance, never mix it with the unknown future outcome.

### 11.3 After-draw evaluation report [R3-PROPOSED]

For a completed target, show a concise paired table:

| Method | TOP prediction + actual main matches / PB hit | WORST prediction + actual main matches / PB hit | Post-draw rank-position: main mean / PB rank | Coverage / status |
|---|---|---|---|---|
| E_1 / v1 | original TOP preserved; 3 / miss | original WORST preserved; 2 / hit | 16.8 / 18 | fully available |

The numbers above are **illustrative, not claims about a draw**. The actual seven winning numbers and Powerball appear above or adjacent to the scoring table, and the method row may expand to show exact overlapping labels. The comparison reference (main 1.4 expected; PB 5% per fixed selection) appears in a caption or nearby context when results are highlighted. Detailed probability, rank and uncertainty records are separate drill-down/data files.

### 11.4 Longitudinal summary report [R3-PROPOSED]

Suggested columns per exact track and covered target window:

```text
method_id, method_revision, variant_id, observation_view,
barrel, selection_rule, track_version,
first_target, last_target, assigned_targets, valid_targets, failed_targets,
mean_main_matches, count_main_match_0,...,count_main_match_7,
powerball_hits, powerball_attempts, powerball_hit_rate,
mean_actual_main_rank, mean_actual_powerball_rank,
reference_context, uncertainty_method, provenance_series, notes
```

The **selection-rule** channel may be TOP or WORST, but rank-position is a separate method-ranking evaluation channel, not a third selectable forecast. A long-format machine-readable table may represent independent component rows; a readable summary should recombine TOP and WORST next to one another for each exact method configuration.

The `reference_context` describes the **stated** null/reference model used for that score, not a claim that all physical reality obeys the reference.

### 11.5 Source and outcome ledgers [R3-PROPOSED]

Minimum separate records:

1. `SourceManifest`: real CSV names, digests, draw-number coverage, game-rule configuration, date validation and operator-labelled draw-order provenance.
2. `TrainingViewManifest`: exact rows/covariates accessible to the target predictor, relevant canonical digest, history-window policy, target ID, and **no forbidden future rows**.
3. `ForecastManifest`: method/variant/fit identity, frozen complete ranks or typed unavailable channels, original TOP and WORST, prediction-content hash, numerical warnings, and serialisation version.
4. `FinalBatchManifest`: all registered roster entries for a genuine target, exact hashes, failures, creation/freeze identifiers and remote publication evidence.
5. `OutcomeRecord`: actual target draw as verified, source provenance, validation state and any correction history.
6. `EvaluationRecord`: references to frozen forecast and a versioned outcome; formula IDs/versions, TOP/WORST and post-outcome rank metrics, availability, context baselines and evaluator version.
7. `SearchAndSelectionLedger`: prospective hypothesis/track selections, all tested variants and ensembles, prior-score-based adaptation policy and changes over time.
8. `SyntheticStudyManifest`: artificial generator/effect, seed, source class, fitted-state isolation, result types and methodological implications.
9. `BenchmarkReport`: computational timings, memory, errors and 1-vs-12-worker equality status; **no displayed merit scores**.

Each record uses schema/version identifiers. A full-source hash may identify the encompassing run/manifest but must not influence a prediction for an earlier target whose permitted training view is unchanged.

### 11.6 Illustrative machine-readable immutable record [R3-PROPOSED]

This *conceptual* JSON is an example of shape, not a frozen implementation schema or an actual forecast:

```json
{
  "record_type": "forecast",
  "schema_version": "r3-draft-0.1",
  "namespace": "REAL_PROSPECTIVE",
  "target_draw_number": 1588,
  "method_id": "E_1",
  "method_revision": "example-v1",
  "variant_id": "example",
  "observation_view": "UNORDERED_SET",
  "permitted_training_view_sha256": "<actual validated digest in implementation>",
  "fit_sampling_model_version": "example-fit-v1",
  "top_selection_rule_id": "TOP_MARGINAL",
  "top_main_set": [2,7,11,18,24,30,35],
  "top_powerball": 9,
  "worst_selection_rule_id": "INVERSE",
  "worst_main_set": [1,5,13,19,22,28,33],
  "worst_powerball": 17,
  "full_rankings": "<typed immutable full ranking payload in actual schema>",
  "forecast_content_sha256": "<computed from canonical payload>",
  "status": "PREDICTION_AVAILABLE"
}
```

The strings in angle brackets are **placeholders**. No implementation should emit them as if they were real hashes or complete rankings. If rankings live in a separately hashed referenced payload, the content identity must cover that payload too. Evaluator-only actuals and rank-position values do **not** belong in this frozen object.

### 11.7 Suggested repository output arrangement [R3-PROPOSED]

Retain the existing repository root; the following directories are *design proposals* only, not commands to migrate source files:

```text
analysing_perceived_randomness_in_reality/
  doc/                           # Ratified project policy, research and specifications
  src/                           # Predictor/evaluator/runner implementations later
  source_data/                   # Authentic validated source observations
  results/
    real/
      development/              # Historical development forecasts + evaluations
      final_holdout/             # Sealed/opened once-only holdout evaluations
      prospective/
        forecasts/               # Frozen future-draw batches, committed pre-draw
        outcomes/                # Later actual results/corrections
        evaluations/             # Later TOP/WORST/rank reports
      methods/                   # Versioned track summaries and diagnostics
    synthetic/
      null_world/                # Artificial data, forecasts and separate reports
      planted_effect/           # Artificial effect-generator studies
    benchmarks/                  # Timing/resource only; no merit scores
    audit/                       # Search register, manifests, publication references
  transitory_data/               # Optional scratch ONLY; Git-ignored
  .venv/                         # Local Python environment; Git-ignored
```

Do not put **real fitted states** into synthetic results or import synthetic states into real forecasts. Do not automatically reuse `transitory_data/` artifacts as inputs. Any persistent checkpoints, warm-start storage, resume protocol or persisted fitted state needs an explicitly versioned, cutoff-valid contract and user approval before implementation. A `results/` file may be the archived output of a run without becoming its permissible next-run input.

### 11.8 Precision and reporting format [R3-PROPOSED]

- All draw numbers/labels/main match counts and PB hit indicators are integers.
- Use canonical exact numeric identities for frozen rankings and method scores according to the R2 numerical policy. UI formatting may round *displayed* diagnostic floats but may not modify the canonical archive or alter TOP/WORST tie decisions.
- Show rank means with adequate decimals (suggest four) while retaining full precision in machine-readable data.
- Show exact numerators/denominators next to rates and avoid misleading percentage-only comparisons.
- Archive timezone-aware publication evidence where applicable; the draw-number predictor itself need not perform time-zone mathematics.
- Use explicit `NO_FORECAST`, `NOT_IMPLEMENTED`, `PREDICTION_FAILED`, `INVERSE_UNAVAILABLE`, `OUTCOME_PENDING`, or related typed states instead of ambiguous empty values.

---

## 12. Implementation architecture and evaluation interfaces

### 12.1 Separation of concerns [R3-PROPOSED]

A small initial Python package can expose **logical modules**, without mandating a large class hierarchy:

```text
real_data_loader / source_validator
admissible_training_view_builder
method_registry / method_runner / model_fit
frozen_prediction_serializer / batch_manifest_writer
real_outcome_loader / separate_evaluator
score_aggregator / comparison_engine / report_writer
synthetic_generator_and_runner [separate namespace]
benchmark_runner [timing only]
provenance_verifier / replay_and_leakage_tests
```

The evaluator must not be importable into a method's actual forecasting path in a way that lets target outcomes leak through shared mutable globals or unrestricted data loaders. Prefer narrow, immutable inputs and explicit return objects. An object called `shared_data` means **reusable code and permitted observations**, not intermediate results recycled from one method into another.

### 12.2 Proposed evaluator API boundary [R3-PROPOSED]

```text
ScoreResult evaluate(
    frozen_forecast,    # canonical already-produced prediction
    validated_outcome,  # actual target, delivered only to evaluator
    scoring_policy_id,  # frozen and approved definitions
    provenance_context  # audit-only; never feeds predictor
)
```

The evaluator checks matching target, game-rule identity, legal sets, exact frozen-selection consistency and genuine outcome validity. It computes all available scores and produces a distinct immutable evaluation object referencing both parents. It does **not** call `fit`, `predict`, `select_top`, `select_inverse`, or a stochastic optimiser. Any recomputation of earlier predictions for reproducibility belongs to a separate replay/test path and must not overwrite frozen prospective archives.

### 12.3 Aggregator boundary [R3-PROPOSED]

```text
AggregateReport aggregate(
    immutable_score_records,
    declared_target_window,
    declared_track_key_and_revision_policy,
    declared_reference_model,
    declared_uncertainty_rule,
    coverage_policy
)
```

The aggregator is separate from the per-target evaluator. It cannot secretly select whichever metric makes a method look best, choose windows after seeing results without labelling exploratory selection, or silently combine mismatched source classes. Methods with no valid forecasts receive coverage/failure reports rather than a fabricated score.

### 12.4 Execution design inherited from R2 [AGREED/R2]

- Initial `ProcessPoolExecutor` (or equivalent spawn-safe) pool, one method per worker; **1–12 configurable**, with 24-worker/SMT comparison optional during explicitly labelled benchmarks.
- Limit each worker's numerical BLAS/OMP threading to one unless an approved, documented exception is benchmarked.
- Warm-started successive historical targets execute sequentially per method unless explicitly partitioned with declared alternative semantics.
- Seeds derive from permitted training-view digests and stable method/variant/restart identity, never from process ID, worker slot, completion order or entire source-file hash.
- Canonical prediction bytes should be bit-identical under 1 and 12 workers in a matched environment by default. Exceptions require user-approved detailed justification and alternate acceptance tests.
- Respect 32 GB system memory. Set worker limits/timeouts and record failures explicitly. `psutil` is a candidate dependency to measure native resident memory, not currently a prerequisite for running Python in `.venv`.
- Benchmark presets B1/B10 with history `W=100` versus `W=ALL_PERMITTED`. Report startup, fit, predict and total timing, process CPU and memory, median-of-three repeats where practical, worker reproducibility, and status only. **Never show benchmark predictive scores.**

### 12.5 Dependency policy [AGREED/R2]

Use Python 3.14 in the project's existing virtual environment. No global installations. Any additional PyPI packages (NumPy, SciPy, `psutil`, optional JIT/optimiser packages, graph/network or ML tools) must be explicitly listed with version compatibility and why they are needed before installation. Maintain and commit `requirements.txt` or an approved equivalent pinned set; keep `.venv/` ignored.

### 12.6 Configurable runs without hidden defaults [R3-PROPOSED]

At minimum, future command-line or configuration controls should explicitly state:

- `mode`: `HISTORICAL_EVALUATION`, `FINAL_NEXT_DRAW`, `SYNTHETIC_NULL`, `SYNTHETIC_PLANTED`, `BENCHMARK`.
- `method_roster` and method/variant revisions; for FINAL, **all registered runnable methods** automatically included and nonrunnable identities also manifested.
- `target_draws` (historical), or automatically `L+1` for FINAL.
- `history_policy`: expanding, rolling-W, method-specific minimum size.
- `observation_view` per method variant and source validation policy.
- `scoring_policy_id` for evaluations; prediction does not look at the same target outcome.
- `worker_limit`, `seed_root`, replay/debug switches, strict/failure behaviour, report destinations.

The complete CLI syntax and executable file layout remain implementation decisions rather than claims of existing functionality.

---

## 13. Acceptance testing and independent verification matrix

The tests below are **proposed R3-specific checks**, additional to and compatible with R2's technical acceptance tests. They are not a requirement to implement all E-methods before testing a basic evaluator. Use independently calculable miniature fixtures, genuine archived outcomes when appropriate, and explicit failures when expected. Test identifiers are deliberately `R3-Txx`, distinct from R2 `T-xx`.

| Test | Fixture / challenge | Required result |
|---|---|---|
| R3-T01 | Frozen TOP 7-set and known actual 7-set | Correct integer 0–7 overlap; no selection recomputation |
| R3-T02 | Frozen WORST 7-set and known actual 7-set | Correct integer 0–7 overlap; no selection recomputation |
| R3-T03 | TOP/WORST Powerball and actual label | Correct separate 0/1 hits and denominators |
| R3-T04 | Ranking 1…35 and known actual seven labels | Correct seven-rank arithmetic mean |
| R3-T05 | Powerball ranking 1…20 and known actual label | Correct rank (including fractional mid-rank ties) |
| R3-T06 | All main scores tied; all PB scores tied | Post-draw ranks 18.0 and 10.5; TOP/WORST canonical bytes unchanged |
| R3-T07 | Same frozen forecast; actual result changed in evaluator | Only score/evaluation content changes; original forecast unchanged |
| R3-T08 | Ranking tie policy changed as new readout version | Fitted scores and tie groups unchanged; newly ordered/readout selection explicitly versioned |
| R3-T09 | WORST from complete marginal ranking | Exact reversal of frozen deterministic order; no second ranking fit |
| R3-T10 | Native MAP-set TOP overlaps marginal WORST | Overlap permitted; native TOP never replaced with top-seven marginals |
| R3-T11 | Diagnostic-only method without full rank | No invented inverse, no invented match score; status preserved |
| R3-T12 | Missing Powerball but valid main prediction | Main scored, PB channel unavailable, no substitute values |
| R3-T13 | Joint-set probability versus ordered-sequence probability | Correct distinct outcome space, likelihood and reference |
| R3-T14 | Exact fair seven-set hypergeometric test | Probabilities sum to one; mean 1.4; SD 0.960392… |
| R3-T15 | Exact uniform Powerball probabilities | PB hit chance 0.05; log-loss and Brier reference if enabled |
| R3-T16 | Main marginal uniform 0.2; 7 actual labels | Marginal Brier sum exactly 5.6 if enabled |
| R3-T17 | Method's forecasts valid on 2 of 10 assigned targets | Coverage 2/10; remaining 8 statuses retained, not silently erased |
| R3-T18 | Paired method comparison with different valid target sets | Pair only on common targets and declare sample size |
| R3-T19 | Same forecast run queried by different post-draw reports | Identical source TOP/WORST; rank-position never used as selection input |
| R3-T20 | Historical target N and later source mutation/append | Forecast content unchanged; evaluator comparison independently references truth |
| R3-T21 | Seed scope changed only by readout-selection rule | Model-fit seed/state unchanged, unless genuinely fitting/sampling model changed |
| R3-T22 | Whole-source hash changes; permitted training digest unchanged | Prediction-content identity unchanged; separate run provenance can change |
| R3-T23 | Serial vs 12-worker matched deterministic test | Canonical full forecast content bit-identical by default |
| R3-T24 | Holdout targets included in development benchmark/evaluation request | Rejected until separately approved holdout opening; benchmark never evaluates merits |
| R3-T25 | FINAL uses L known draws, original holdout inside data | All available permitted data accessible; target automatically L+1 |
| R3-T26 | FINAL report generated before outcome | Displays TOP/WORST side by side, but **no** actual-match/rank values |
| R3-T27 | Later outcome imported for same target | Separate immutable evaluation record; original batch hash unchanged |
| R3-T28 | Post-target attempt to add forecast to complete FINAL batch | Original batch unchanged; recomputation labelled retrospective |
| R3-T29 | Two forecast versions across genuine weeks | Exact-track summaries separate; operational portfolio appropriately versioned |
| R3-T30 | Weekly batch contains failed or nonimplemented methods | Explicit roster entries and failure reasons; no silent omissions |
| R3-T31 | Batch some-method-wins report under correlated forecasts | No automatic independent-method multiple-trial formula |
| R3-T32 | Artificial generator/results supplied to real fit | Explicit provenance/type rejection |
| R3-T33 | Synthetic files changed while fixed real fit/config unchanged | Real prediction content unchanged |
| R3-T34 | Synthetic identifiability/calibration test fails | Report failure; E-method remains registered and eligible for real investigation |
| R3-T35 | Benchmark mode completes predictions internally | Timing/status/equality only; no merit report or outcome-based selection |
| R3-T36 | Same result viewed with different text/CSV formatting | Frozen canonical content hash unchanged |
| R3-T37 | An official result corrected later | New outcome revision and amended score, original history preserved |
| R3-T38 | Missing or late remote publication evidence | Explicit unverified/late status, not falsely labelled verified prospective |
| R3-T39 | Source dataset contains changed-rule or missing-number draw | Reject invalid real input; no ad hoc inferred replacements |
| R3-T40 | First FINAL forecast requested without ratified core score policy | Production mode blocked; no post-outcome score selection |
| R3-T41 | Method underperforms, duplicates or highly correlates with others | Remains in catalogue and combination-eligible; retain result history |
| R3-T42 | Actual target revealed before native TOP/WORST generation | Predictor cannot access evaluator truth; fail leakage boundary |
| R3-T43 | A reported summary mixes actual and simulated results | Strict dataset-class validation fails; independent reports retained |
| R3-T44 | Optional rank-position-derived future adaptation | Only allowed with separately approved pre-target rule; never changes older frozen selections |

**Test philosophy:** A method that fails a statistical performance or synthetic identifiability diagnostic remains in the research catalogue. A genuine *software integrity* failure (e.g. future leakage, fabricated numbers or altered pre-draw forecasts) blocks that particular defective execution from being misrepresented as a valid real prediction until corrected. This is not a scientific veto on the underlying hypothesis.

---

## 14. Explicit decision register for owner review

The following are **proposals and open decisions**, not newly ratified requirements merely because this draft contains them. Acceptance of the mandatory evaluation core does not silently ratify optional measures or unspecified mathematical variants.

| ID | Decision | Recommendation / status |
|---|---|---|
| R3-D01 | TOP main/PB primitive formulas | Ratify exact set overlap and one-number PB hit; required |
| R3-D02 | WORST main/PB primitive formulas | Ratify same scoring of inverse selections; required |
| R3-D03 | Post-draw mean actual main rank and actual PB rank | Ratify mid-rank tie measure; **evaluation only**; required |
| R3-D04 | TOP/WORST side-by-side per method | Ratify display and archival rule; already owner-agreed |
| R3-D05 | No automatic combined scalar | Preserve separate main/PB components; recommended |
| R3-D06 | Missingness/coverage denominators | Ratify assigned-target and valid-attempt denominators together |
| R3-D07 | Main/PB reference values | Ratify exact hypergeometric + categorical reference labels, never method vetoes |
| R3-D08 | Simple retrospective target windows | Propose DEV_ALL, LAST_100, LAST_50, LAST_10; preserve holdout |
| R3-D09 | Once-only original holdout | Ratify explicit opening event and pristine-status retirement |
| R3-D10 | Prospective series / immutable batch | Ratify remote pre-draw evidence, version separation and append-only outcomes |
| R3-D11 | Additional probability/likelihood scores | Optional, capability-dependent; formulas proposed, not a block on rank-only methods |
| R3-D12 | Uncertainty reporting | Ratify transparent denominators/reference assumptions; exact statistical thresholds remain open |
| R3-D13 | Multiple-method and adaptive search reporting | Ratify search log and batch-dependence caveat; no exclusion criteria |
| R3-D14 | Ensemble temporal eligibility | Ratify dependence only on legitimate pre-target outputs/states |
| R3-D15 | Rank-position as future adaptive ensemble feature | **OPEN**; recommend no automatic adaptation in first implementation |
| R3-D16 | Tie-break policy affecting TOP/WORST | **OPEN in R2**; recommend deterministic ascending-label break for frozen descending ranks; inverse exact reversal |
| R3-D17 | Seed nomenclature `selection_model_version` | Clarify fit sampling model vs downstream readout; no silent R2 modification |
| R3-D18 | Synthetic calibration role | Ratify distinct artificial reports, allowed design learning and no fitted-state contamination |
| R3-D19 | Speed, process pool, resource controls | Inherit ratified R2; performance cannot delete methods |
| R3-D20 | Timing-proof mechanism for prospective forecasts | **OPEN implementation choice**; GitHub push evidence required, proof strength must be tested |
| R3-D21 | Algorithmic ranking of a single project “best” method | **OPEN**; do not create automatic champion until metrics and selection procedure are predeclared |
| R3-D22 | Interpretation thresholds for departure from chance | **OPEN**; avoid a priori assumptions as eligibility tests and disclose search multiplicity |
| R3-D23 | Optional ordered-sequence performance scoring | **OPEN**; separate from seven-set TOP/WORST |
| R3-D24 | Persistent checkpoint/restart semantics | **OPEN**; not implicit from `transitory_data/` |

### 14.1 Decisions suitable to ratify as the initial evaluation core

Proposed initial **core**: R3-D01 through D07, D09–D10, D13–D14, D17–D19, with D08's windows optional but recommended. This includes enough exact scoring and provenance to avoid choosing TOP/WORST/rank definitions after genuine outcomes become known. It does not choose an automated single best method, a special significance threshold or a first implementation of 62 sophisticated algorithms.

### 14.2 Questions that can remain open until implementation planning

The tie policy (R3-D16), actual storage schemas, remote publication proof mechanics, optional probabilistic scores and formal hypothesis-level discovery thresholds can be resolved in a controlled, versioned step before running affected real forecasts. In particular, **R2-T39 already requires ratifying the core TOP/WORST/rank-position measures before the first genuine FINAL forecast**. R3 should not be considered permission to sidestep that gate.

---

## 15. Proposed post-R3 implementation roadmap

**I1 — Minimal, testable research apparatus:** CSV validation and draw-number cutoffs; immutable typed forecast/actual/evaluation payloads; method registry; deterministic ranking/selection services; score evaluator; basic process pool; canonical hashing; technical tests for leakage and TOP/WORST separation. Start with synthetic *unit fixtures* and legally generated miniature independent data where useful; do not convert test-fixture results into evidence about real lottery predictions.

**I2 — Initial six experiments:** Define/approve the necessary exact mathematical variants of E_1–E_6, implement truthful ranking outputs, verify TOP+WORST and rank-position evaluator separation, and conduct permitted development-period walk-forward testing. Expand method by method rather than inventing one giant script with unstable variants.

**I3 — Additional E_7–E_62 and beyond:** Implement each gradually with unit fixtures, capability declarations, numerical validation, benchmarks and research diagnostics. Retain unsuccessful, speculative, diagnostic and computationally expensive models. Investigate acceleration only after measurements justify it.

**V1 — Controlled historical final holdout:** Freeze the nominated experiment roster and evaluation plan; obtain owner approval before opening original Draws 1578–1587 as final historical evidence; record use, results and any later tuning.

**P1 — First genuine prospective batch:** After preparation and scoring rules are fixed, refresh source, compute L+1 from the current complete observations, archive the entire registered roster's results/statuses, push a verifiably pre-draw batch and subsequently evaluate against the real outcome. Repeat with newly completed genuine draws while preserving earlier frozen predictions.

**C1 — Further research:** New mathematically distinct candidate ideas, external covariates, pilot-wave refinements, inverse-rank methods and combinations remain welcome within the owner's agreed extension allowance; add new E-identities only through documented approval.

Each stage receives its own implementation documents and acceptance evidence. This R3 draft **does not** create executable code or authorise a live forecast by itself.

---

## 16. Sources, cross-reference map and handback

### 16.1 Governing local documents consulted

1. `doc/Predictive_Randomness_Research_Project_Proposal_v0_3.md` — particularly §§2, 5, 9–12, 14–15 (philosophy, holdout, retention, synthetic separation, evidence and development phases).
2. `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` — §§1, 4, 7–9 (operator-labelled drawn order, method hypotheses E_1–E_62, research streams, deferred evaluation decisions and benchmark separation).
3. `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` — §§2–6, 8–13, T-01–T-39 (method outputs, TOP/WORST and rank-position, source cutoff, prospective batch, stable seed, reproducibility, evaluation handoff and technical tests).
4. Claude's R2 v0.2 review and **Claude's subsequent review of R2 v0.3 as transmitted by the owner**, noting the optional seed-terminology clarification. The latter comments are in the project conversation rather than an independently opened repository review file here.

The R2 v0.3 document still labels itself an unratified review candidate internally; the **owner expressly ratified R2 v0.3 afterward on 22 October 2026**. This R3 document records the actual ratification state without rewriting the historical R2 bytes. Current ratification status is governed by explicit owner decisions, not by stale internal headers in a preserved review document.

### 16.2 Exact arithmetic provenance

The reference probabilities in §4 follow directly from the legal seven-from-35 without-replacement and one-from-20 definitions and were independently recalculated from integer combinations for this draft. No live forecast or experimental R3 result was computed. The illustrative sets and scores in §11 are invented only to demonstrate reporting layouts and must not enter real source or prediction records.

### 16.3 Explicit non-claims

- No E-method has been implemented as a new working predictor under this R3 draft.
- No real-world forecast has been produced here, and no future actual outcome has been inspected for scoring.
- The original holdout's outcomes are present in the available historical source files but were **not used to fit, compare or select an E-method in drafting this document**.
- The R3 statistical reference does not establish that the real lottery is independent, quantum-mechanical, deterministic, biased, unpredictable or predictable.
- The optional method-combination examples are conceptual; no weights, active champions or production scoring thresholds have been chosen.

### 16.4 Requested owner review

Review the proposed **evaluation core** (TOP/WORST matches, mid-rank position, missingness and denominators), the separate synthetic/evidence treatment, and the prospective batch/reporting requirements. The key open choices are prediction-time ties, optional scores, and the exact remote publication proof procedure. After review and any revisions, the owner may ratify R3. Only then should the next implementation specifications and staged Python development proceed.

**Closing principle:** The point of this project is to challenge perceived randomness rather than to protect a received explanation. The point of honest pre-outcome forecasting and an auditable evaluator is to give extraordinary, ordinary and disappointing results alike the strongest possible opportunity to be understood.

