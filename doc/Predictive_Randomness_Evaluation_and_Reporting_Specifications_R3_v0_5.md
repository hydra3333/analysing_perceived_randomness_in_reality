# Predictive Randomness — R3 Evaluation, Comparison, Evidence and Reporting Specifications

**Version:** 0.5 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026): R3 v0.4 plus section 17, which carries the owner-ratified Method Ranking Measures Proposal v0.5. Predecessor: R3 v0.4 CONSOLIDATED, OWNER-RATIFIED 26 October 2026.  
**Date:** 27 October 2026 (v0.5 drafted 26 October, ratified 27 October; v0.4 ratified 26 October; v0.3 ratified 24 October)  
**Status:** OWNER-RATIFIED 27 October 2026; R3 v0.4 is historical. Ratification itself grants no Mode H/FINAL authority.
**Repository path:** `doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md`  
**Owner:** Project owner, `hydra3333/analysing_perceived_randomness_in_reality`  
**Governing project charter:** Owner-ratified consolidated Proposal v0.6 (27 October 2026); Proposal v0.5 remains historical.  
**Governing research catalogue:** `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` — **RATIFIED**  
**Governing method and execution contracts:** Owner-ratified consolidated R2 v0.5 (27 October 2026); R2 v0.4 and R2 v0.3 remain historical.  
**Research method inventory:** E_1 through E_62, all permanently retained; room for up to 100 methods *additional to the original six*.  
**Computing environment:** Windows 11, Python 3.14, project `.venv`, Ryzen 9 3900X (12 physical cores / 24 logical processors), 32 GB RAM.  
**Current accepted development data:** POWERBALL 1144–1576 (433) and OZLOTTO 1474–1693 (220), each ledger-pinned INIT/version 1. Historical larger snapshots are preserved in Git but are not live development data.

> **Purpose.** Specify how experimental forecasts, including TOP and WORST, will be evaluated, compared, archived and communicated; how methods can be combined without hiding hindsight; how synthetic calibration remains a separate research stream; and how genuine weekly future-draw evidence is preserved. The owner deliberately invites unexpected and unconventional explanatory models. The statistical reference model is a measuring instrument, **not** an admissibility test for experimental hypotheses.

> **Critical separation.** A **predictor** determines and freezes TOP, WORST, full rankings and any native joint predictions using pre-target admissible observations. A separate **evaluator** later receives the actual outcome and computes metrics. Neither rank-position scoring nor the future actual result may alter the already frozen prediction. A **researcher** may inspect synthetic diagnostics and redesign subsequent versions transparently, but synthetic observations or fitted artificial states must not be passed off as real historical evidence.

---

## Edition history and authority

This owner-ratified consolidated edition was assembled from the previous ratified edition, its owner-approved operational errata and the explicitly owner-decided October 2026 changes. Previous revision histories remain in the unmodified historic source files and are mapped in the accompanying evidence. This paragraph is not an independent new policy.

Edition 0.5 adds section 17, which carries the owner-ratified Method Ranking Measures Proposal v0.5 (26 October 2026), and the pointer edits it needs (0.1, 0.2, 5.6, 7.4, 11.5, 11.7, 12.6, 13 and R3-D21). Sections 0-16 otherwise keep the ratified v0.4 text.

## 0. Document authority, vocabulary, and handoff

### 0.1 Document hierarchy and responsibilities

| Document | Governs | Status |
|---|---|---|
| Proposal v0.6 (consolidated) | Project charter and owner decisions | OWNER-RATIFIED 27 Oct 2026; v0.5 and v0.4 historical |
| R1 v0.4 | Method hypotheses E_1–E_62, exact method identities and research foundations | Ratified |
| R2 v0.5 (consolidated) | Training cutoffs, typed method outputs, method registry, separate modes, prediction freezing, seeds, parallelism, numerical contracts | OWNER-RATIFIED 27 Oct 2026; v0.4 and v0.3 historical |
| **This R3 v0.5** | Current scoring, freeze/evidence contract; method ranking measures (section 17) | OWNER-RATIFIED 27 Oct 2026; v0.4 historical; no Mode H/FINAL authority |
| Method Ranking Measures Proposal v0.5 | Method ranking measures (league tables) | OWNER-RATIFIED 26 Oct 2026; carried in section 17 and in R2 / Architecture / Proposal as pointed to there; the file is kept unchanged as history |
| Package 2 v0.11 | N-1 reader, coordinator evidence and regression corrections C1-C6 | PENDING code/review |

Later approved owner decisions supersede earlier conflicting text. With the owner's ratification of R3 v0.4 (26 October 2026), provisions labelled [R3-PROPOSED] were ratified as written, and they remain ratified in this edition; items labelled OPEN, and decision-register entries still marked OPEN, remain undecided. Section 17 carries the owner-ratified Method Ranking Measures Proposal v0.5 (26 October 2026) as written. This ratification neither silently amends another contract nor decides the first implementation of an unresolved E-method.

### 0.2 Requirement tags

- **[AGREED/R2]**: A requirement explicitly agreed or inherited from the ratified sources.
- **[R3-PROPOSED]**: Proposed here for owner assessment and ratification.
- **[OPEN]**: Not yet fully defined; this draft provides options and a recommended default.
- **[OPTIONAL]**: Candidate advanced analysis; should not block initial core reporting.
- **[MR-RATIFIED]**: Owner-ratified on 26 October 2026 in the Method Ranking Measures Proposal v0.5 and carried in section 17 as written.

### 0.3 Research philosophy, expressed operationally [AGREED]

1. Investigate whether apparently random physical outcomes show exploitable predictive relationships, including unanticipated, nonlinear, speculative, or apparently counterintuitive structures.
2. Do not exclude a method because independent-draw theory, consensus or current physical explanations suggest low likelihood of success.
3. Retain all experimental methods, variants, unsuccessful results, highly correlated methods and unusual observations as auditable research records.
4. Distinguish a precisely computed chance-reference probability from a claim that a real result was *caused* by chance. An unusual observation may remain unexplained for a substantial period.
5. Investigate clearly demonstrated source or implementation defects promptly. A verified error is different from prematurely attributing surprising results to an unspecified error.
6. A real pre-draw prediction, frozen before the outcome and evaluated afterward, is stronger evidence of forecast capability than a retrospective fit; neither is automatically conclusive.
7. Do not equate empirical predictive improvement with a proof of pilot-wave, quantum, physical-equipment, cosmological or other particular mechanisms.

### 0.4 Seed identity clarification — settled by owner-approved ERR-R2-04 [APPROVED/R2 ERRATUM]

R2 §9.2 lists `selection_model_version` in the stochastic fit seed identity. Clarify its semantics rather than rewriting the ratified text in place:

- The **mathematical sampling/observation model used in fitting** (for example unordered fixed-size-set likelihood versus ordered weighted-without-replacement likelihood) is a legitimate **fit identity** and may change fitting randomness. Its version belongs in the fit seed identity.
- A **downstream readout/selection rule** (`TOP_MARGINAL`, `MAP_SET`, `INVERSE`, display formatting) applied to an *already frozen fit* must **not** perturb fit initialization, optimisation, or latent state. Its identity belongs only to the distinct derived selection output, and possibly a separately seeded sampling/readout operation if that operation is genuinely stochastic.
- Adopt explicit names `fit_sampling_model_version` and `readout_selection_rule_version` at implementation time, with different identity scopes. Add a regression test: changing only the WORST/report selection cannot change the TOP method fit or its frozen full rankings.

**Status:** **APPROVED under ERR-R2-04** in `Predictive_Randomness_R2_v0_3_Approved_Erratum_v0_2.md`. This is a binding implementation clarification, not an outstanding proposal. It preserves the ratified R2 v0.3 mathematical intent and does not modify that original file; the distinct readout tie algorithm remains specified in R3.

---

## 1. Dataset identity, target modes and protection against look-ahead

### 1.1 Current-rule admissibility [AGREED/R2]

Accepted real training data use the current game-specific profiles only: POWERBALL (7-of-35 MAIN plus 1-of-20 PB, from draw 1144) and OZLOTTO (7-of-47 MAIN only, from draw 1474). Do not silently mix other historical ball counts or barrel configurations. Within each current era, draw numbers must be consecutive. ISO calendar dates are source metadata for validation, optional temporal hypotheses and human-readable reporting; ordinary core forecasting boundaries use draw numbers, not precise timestamps.

The approved per-game masters provide the unordered seven-set (derived sorted) and published sequence under `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`. Physical order is an owner assumption, not independent video verification. Do not count those two representations of the **same** draw as independent draw observations.

### 1.2 HISTORICAL_EVALUATION [AGREED/R2]

To forecast a known historical target **N**:

1. Supply only permitted same-game observations ending at N−1, starting at the profile era-first draw or a predeclared shorter window.
2. Fit and freeze all available forecast channels, TOP and WORST where defined, before outcome access by the evaluator.
3. Separately reveal the genuine result for N to the evaluator and compute fixed measures.
4. Archive the original predictions, actual result, scores, status and legitimate lineage. Outcomes from N and later cannot influence the prediction for N.

The fixed first-ten holdouts are POWERBALL 1577–1586 and OZLOTTO 1694–1703; neither is available to ordinary development, benchmarking, method choice or reporting. Opening requires a separate Mode H protocol and owner action.

**Benchmark example within the current development boundary:** Powerball B1 targets 1576 with fit rows 1144–1575 (432 rows), W=100 rows 1476–1575; B10 targets 1567–1576, with 423–432 preceding eligible draws. Benchmarks generate prediction payloads only for computational correctness and deterministic comparison; benchmark **reports must not show or score** results against actuals.

### 1.3 FINAL_NEXT_DRAW [AGREED/R2]

With the latest consecutively validated observed draw L, the next real target is **L+1**. Only after an independently authorised holdout protocol and FINAL opening, the latest truly available completed results through L may enter the next genuine forecast as allowed by each method. The development quarantine cannot be bypassed merely by calling a run FINAL. A particular fully specified E-method may internally adopt a declared rolling window without imposing a global ten-draw exclusion.

The **entire pre-draw FINAL batch** includes one snapshot of every registered runnable method/variant's available outputs and an explicit entry for each blocked, not-yet-runnable, unavailable or failed registry item. Freeze and push the full batch remotely before the actual target event; later results and scoring live in **separate append-only records**, not inside a mutable prediction record.

The cycle repeats for each newly available genuine draw: compare the previously frozen L+1 batch against the new real result, append and validate that result, fit models to all now permitted real history, and prospectively freeze the next L+2 batch. The owner permits this cycle only after its separate acceptance and explicit FINAL opening; neither preparation nor this edition alone authorises it.

### 1.4 No accidental data contamination [AGREED/R2]

- Predictors cannot access the evaluator's truth object or post-target results.
- Caches, precomputed features, hyperparameter fits, seed identities and warm starts have the same cutoff as the direct input view.
- Artificial/synthetic observations do not enter a real-data training view or fitted state.
- The SHA-256 of the **entire current CSV** is provenance only, never part of the historical prediction seed or forecast-content identity.
- A prediction for N is byte-identical when N or any later draw is mutated/appended while its permitted training prefix, configuration and software remain unchanged. Archive metadata may differ; compare canonical forecast content independently.
- Benchmark mode is explicitly separated from predictive-merit evaluation. Its reports contain elapsed/CPU time, memory, statuses and equality tests, **not** match or rank scores.

### 1.5 A practical clarification on date/time information [R3-PROPOSED]

No wall-clock data is needed to calculate N−1 training boundaries. Nonetheless, prospective evidence needs a *time of publication* or other externally verifiable pre-draw proof. That is **audit metadata**, not a predictor's mathematical input, unless a specific separately declared time-dependent experiment legitimately uses time. Consequently, there is no contradiction between “draw-number-only predictions” and preservation of remote pre-draw publication evidence.

**Date-dependent evaluation gate (DECIDED; cross-reference R2 §3.1A):** The immutable era profile derives each weekly calendar date from its first draw/date and seven-day cadence. A restricted source-date discrepancy audit produces no quarantined values; a mismatch **halts E_14, E_54 and other date-dependent methods for that game pending owner decision**. Unrelated valid `UNORDERED_SET` methods are not automatically blocked. The evaluator may not treat such a date-dependent run as valid merely because other input checks pass. This is an audit/eligibility rule, not permission to read target N or later in model code.

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

**Proposed mandatory prediction-time policy: deterministic, label-neutral tie resolution.** Sort each barrel's eligible numbers by descending native method score. Where two or more labels have *exactly the same validated score*, assign their relative order using a **separate readout-only**, domain-separated deterministic ordering. An ascending-ball-label preference is *not* an acceptable tie policy: historical E_1 count-rank boundary ties were reported by Claude in approximately 63% of assessed main targets and 14% of Powerball top boundaries (figures reported by reviewer, not independently verified here).

**Specified reference algorithm — proposed version `TIE_SHA256_V1`:** For each tied label, form a canonical, length-delimited UTF-8 byte encoding of the tuple:

```text
("PREDICTIVE_RANDOMNESS/TIE_SHA256_V1", training_view_sha256,
 target_draw_number, method_id, variant_id, barrel_id,
 ranking_tie_readout_version, tied_label)
```

Compute `SHA256(canonical_tuple_bytes)`. Within each equal-score group, order labels by ascending digest bytes; on a cryptographic digest collision only, break the remaining tie by numeric label to provide a total deterministic order. Canonical tuple encoding and versioning must be frozen and verified by exact test vectors before use. These digest-derived keys provide label-symmetric pseudo-random ordering under the conventional hash model, without relying on Python `random.shuffle`, process IDs, dictionary iteration order or changing numerical-library RNG implementations. The seed/key depends **only on information permitted before the target**. It does not use a later actual outcome, whole-file source hash, run time or evaluation score. Include the target draw number for identity even if separate targets legitimately share an identical training window.

**The `ranking_tie_readout_version` is one shared version for construction of the complete tied ranking, not separate versions for TOP versus WORST.** It is distinct from any native joint-set TOP selection rule and from stochastic model fitting.

The resulting **complete marginal ranking is frozen once**. The ranking-capable method's marginal TOP is read from the first seven main positions / first Powerball position; **WORST is read from the last seven main positions / last Powerball position of the frozen ranking (equivalently, the first seven main positions / first Powerball position of its exact reversal)**. If a method's *native* TOP is MAP-set or another joint-set prediction, preserve that native TOP even when it overlaps marginal WORST; the marginal-rank reversal constraint governs the WORST, not replacement of the native TOP. The two outputs are rendered side by side and never adapted after observing the draw.

**Fit/readout independence:** This hash-derived readout key is separate from all stochastic model-fitting random streams. Changing only the tie-break or downstream TOP/WORST readout version **may intentionally change selected numbers at ties**, but must not alter fitted parameters, scores or any legitimately frozen pre-readout model state. Within a single unchanged readout version, repeated runs and worker counts yield identical outputs.

For **post-draw rank-position**, tied *native method scores* receive **mid-ranks**, meaning the average positions occupied by their tie group **before applying the prediction-time digest ordering**. An all-tied main ranking assigns rank 18 to every label, and an all-tied Powerball ranking assigns rank 10.5 to every label. Neither tie-derived midpoint nor the observed actual draw can modify the frozen TOP/WORST predictions.

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

**Reference figures for actual barrels [RATIFIED R3 v0.3 scope].** These are contextual rulers, never method-veto thresholds. For a fair main barrel choosing seven labels from M, expected TOP matches are `49/M`, and mean native-score mid-rank is `(M+1)/2`:

| Game | MAIN TOP expectation | MAIN mean mid-rank | Other real barrel |
|---|---:|---:|---|
| POWERBALL (7 of 35) | 1.4 | 18.0 | PB 1 of 20: hit expectation 1/20, mid-rank 10.5 |
| OZLOTTO (7 of 47) | 49/47 ≈ 1.042553 | 24.0 | None; PB field ABSENT |

Detailed uncertainty uses the appropriate hypergeometric distribution, native-score tie treatment and within-batch dependence. TOP and WORST have separate pre-frozen reference measures; no implicit pooling of games, and no unapproved cross-game standardisation.


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

Separately, the ranking measures MR6 and MR14 (17.6) use only typed probability outputs declared under R2 section 5.6. They are reporting measures and do not settle this optional-score decision, which remains OPEN.

## 6. Evaluation windows, holdout, adaptive choices and comparable series


**DECIDED — fixed holdout:** `POWERBALL` 1577–1586, `OZLOTTO` 1694–1703, quarantined from 2026-08-01; these ranges do not slide. Development caps remain 1576/1693. The narrow E_1 draw-1577 regression is forecast-only, without any outcome read or score, never Mode H. R2 §2 is the **normative data boundary and source-view contract**; this R3 section governs holdout *evaluation* and freeze-to-score discipline. Any outcome used in method design, tuning or selection destroys its claimed pristine independence for that method; disclose holdout exposure and never silently shift or restore status. Opening requires separate owner approval and a reviewed manifest/outcome-release mechanism. The old first-snapshot Oz seal and former Powerball 1578–1587 are withdrawn.

**Current development/holdout boundary [OWNER-DECIDED; REQUIRES THIS EDITION’S RATIFICATION].** A single calendar boundary, **1 August 2026**, applies separately to both games. `POWERBALL` development master: draws **1144–1576** (433); first quarantined draw **1577**, `FINAL_HOLDOUT_10` **1577–1586**. `OZLOTTO` development master: draws **1474–1693** (220); first quarantined draw **1694**, `FINAL_HOLDOUT_10` **1694–1703**. Pre-era observations and quarantined outcomes are ineligible for development. These historical-development caps do not cap a later separately authorised genuine prospective service.

**Very narrow E_1 exception:** the independently accepted Powerball target-1577 forecast may be recomputed from draws 1144–1576 **without parsing, seeing or scoring outcome 1577**. It is a forecast-only regression, neither development scoring nor holdout evidence. No other boundary crossing follows from this exception.

**Mode H is not open.** The first-ten sequential outcome-release protocol, handling of later quarantined draws, and the choice of combined versus separate quarantine storage remain subject to independent review and owner authorisation. Nothing in this documentation enables `HOLDOUT_FETCH`, `results_master update`, FINAL or a scientific run.


### 6.1 Development walk-forward blocks [R3-PROPOSED]

Historical evaluation must specify both its target range and exactly how the fit at each target uses preceding observations. Suggested standard report views when sufficient valid targets exist:

| View | Purpose | Treatment |
|---|---|---|
| `DEV_ALL_ELIGIBLE` | All development-period walk-forward targets for which the particular method's minimum history is satisfied | Primary retrospective breadth, before holdout |
| `DEV_LAST_100` | Most recent 100 development targets | Recency comparison |
| `DEV_LAST_50` | Most recent 50 development targets | Recency comparison |
| `DEV_LAST_10` | Last ten eligible development targets, ending at 1576 (Powerball) or 1693 (Oz Lotto) | Diagnostic only; not the reserved holdout |
| `FINAL_HOLDOUT_10` | POWERBALL 1577–1586; OZLOTTO 1694–1703 | Only once explicitly authorised for one-governed evaluation |
| `PROSPECTIVE_ALL` | All genuinely archived-before-draw FINAL target batches | Strongest temporal provenance; track versions and skipped weeks |
| `PROSPECTIVE_LAST_K` | The most recent K genuine prospectively frozen targets, K identified in every report | Descriptive moving view; cannot be cherry-picked or presented alone |

Do not hard-code today’s observed endpoint into evaluation code. Target ranges must derive from a versioned study plan and the available source. Some methods will have too few valid origins to support a full 100-target block; retain and disclose the shortfall rather than creating artificial data.

### 6.2 Separation of discovery, tuning and final evaluation [R3-PROPOSED]

**Unresolved Mode H store:** the future study must compare a combined master containing quarantined outcomes to a truly separated quarantine store that releases one outcome at a time. No approach is accepted merely by being described; the owner approves an independently reviewed runner and freeze-before-outcome mechanism.


- Use development targets to explore models, mathematical variants, tie rules, forecasting adapters, hyperparameters and ensembles. These choices may legitimately be informed by *permitted past real outcomes*, with full disclosure of the tried search.
- Record the exact candidate configurations tried, including losing configurations; a selection process that searches extensively has a different evidential interpretation from one frozen before the search.
- Reserve each game’s fixed first ten quarantined outcomes from development until a separately authorised Mode H opening; no predictor, optimiser or method-selection process may inspect them.
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

**One search record (single definition).** The search record named above (`search_history` / `method_selection_log`), the `SearchAndSelectionLedger` of 11.5 item 7 and the method-ranking search log of 17.5B are one mechanism, not several: a single programme-wide, append-only, committed file, `results/audit/SEARCH_LOG.csv`, with a typed `row_type` column. Every row carries its UTC time, game and row type, and rows are never edited or deleted. Each method-ranking report run appends exactly one row with `row_type` = `RANKING_REPORT`, holding the fields listed in 17.5B. Trial configurations, candidate combinations, selections and adaptation-policy changes append rows of their own types, defined when the tools that write them are specified. There is no second search log.

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


**DECIDED — freeze-to-score and environment pin:** every game-target study pins dataset identity, eligible N−1 view, method/variant, numerical environment, predicted TOP/WORST, owner-approved scoring/evaluation/holdout-release protocol, and external publication proof before outcome access. **Never upgrade dependencies between freeze and score, or anywhere within a Mode H study (R3-T50).** A whole-master SHA can prove source integrity but cannot be a fit/tie seed. The numerical integrity guidance is non-normative; R2 governs data types and views; Architecture governs installer implementation. No Mode H/FINAL/score operation is authorised by this text.

**Master provenance and no look-ahead:** freeze records bind the accepted ledger version/master SHA, permitted training-view digest, game/draw, method/variant, model config, code/environment and result. The full master hash is provenance only, never fit/readout input. Only after frozen forecast verification may the separately authorised evaluator obtain the correct target outcome. Do not infer Mode H/FINAL authority from this document.

**Numerical and environment contract [OWNER-DECIDED].** Use `int64` throughout common reader internal integer storage and exported numeric views; `float64` for floating arrays, typed calendar dates and Python arbitrary-precision integers when an exact count exceeds `int64`. Validate finite outputs, overflow/underflow, numerical stability, convergence and high-precision reference cases when relevant. The project’s self-contained `install_upgrade_dependencies_into_venv.bat` is the sole human-maintained dependency authority; its default invocation installs **and upgrades** dependencies at the owner's request. Record versions and environment fingerprints. **After every upgrade** STOP further scientific work until all applicable offline, N−1/precision/boundary and frozen E_1 1577 golden tests pass. Never upgrade between freezing a forecast and scoring it or within an R3-T50-pinned Mode H study. These rules prioritise accuracy while maintaining the ability to reproduce an exact frozen evaluation environment.

**Fitting:** each target `N` is fitted afresh from its eligible pre-`N` observations and declared fitting window. Prospective operation ordinarily uses the latest eligible completed-draw history; historical walk-forward uses a different N−1 prefix for each target. An incremental fit or cache requires prior independently reviewed **byte-identical** equivalence to from-scratch fitting (or an owner-ratified alternative). Retain immutable predictions, fit configuration, source/view identities, environment, results and scoring evidence; no blanket requirement to archive all intermediate numeric arrays.


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
7. `SearchAndSelectionLedger`: prospective hypothesis/track selections, all tested variants and ensembles, prior-score-based adaptation policy and changes over time. This is the single search record of 7.4 (`results/audit/SEARCH_LOG.csv`), which also holds the method-ranking report rows of 17.5B.
8. `SyntheticStudyManifest`: artificial generator/effect, seed, source class, fitted-state isolation, result types and methodological implications.
9. `BenchmarkReport`: computational timings, memory, errors and 1-vs-configured-maximum-worker equality status; **no displayed merit scores**.

Each record uses schema/version identifiers. A full-source hash may identify the encompassing run/manifest but must not influence a prediction for an earlier target whose permitted training view is unchanged.

### 11.6 Illustrative machine-readable immutable record [R3-PROPOSED]

This *conceptual* JSON is an example of shape, not a frozen implementation schema or an actual forecast:

```json
{
  "record_type": "forecast",
  "schema_version": "r3-draft-0.1",
  "namespace": "REAL_PROSPECTIVE",
  "target_draw_number": 1576,
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
    method_rankings/             # Per-game ranking reports, create-only (17.10.1)
    audit/                       # Search register (SEARCH_LOG.csv, 7.4), manifests, publication references
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

**Evaluator and report contract.** Every forecast, outcome, score and publication uses the structured pair `(game_id, draw_number)`, versioned actual profile barrels and appropriate training-view identity. A mismatch refuses, even if bare draw numbers coincide. New output schemas require `game_id`; legacy Powerball schema evidence is accepted only under versioned compatibility and is never rewritten. The evaluator independently checks a frozen success result, group/firewall/orphan state, provenance hash and game-target-profile identity **before** releasing exactly that target outcome; a method never receives target or later data. Every held-out target remains accounted for (including failures); any warm-up, burn-in or exclusions must be declared in advance.

**Per-game prospective freeze:** source version/validation, admissible N−1 fitting, freeze all available TOP/WORST and full ranking readouts, publish complete target batch *before* the actual event, and later score separately. Record independently verifiable publication-time evidence; Git author/committer timestamps alone are insufficient. Until authoritative game-specific draw/close timezone evidence exists, do not invent a nominal observed draw timestamp; exact real-time deadline policy remains OPEN.

**Required reporting fields:** game ID, draw number/key, era/profile, method/variant, selected view/schema, training bound, source/ledger identity, status, actual barrels, TOP/WORST availability and rankings, rank-position statistics from frozen native scores, applicable per-barrel R3 metrics and elapsed/resource evidence. The scientific-result consumer allowlist and global group-failure firewall remain non-negotiable. The former Powerball-only candidate 1145–1577 walk-forward proposal is not authorised; current development ranges are fixed in §6.


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

### 12.4 Proposed runtime implementation — R2 direction with later owner instructions [R3-PROPOSED]

- Each E-method is a **standalone executable `.py`**, importing shared project utility modules only as needed. The coordinator controls **independent operating-system subprocesses**, not an in-process method executor or mandatory common module runner. Provisional **Option F**: launch the same protected `Run_Experiment.bat` used by a human operator, through ordinary `subprocess.Popen` with output pipes; subject to Windows proof-of-concept gates. The direct project-venv Python launch remains a documented fallback if wrapper behaviour fails the gates.
- **Configurable concurrency is 1–6 experiment processes, initially default and maximum 6.** The owner-approved R2 worker reconciliation is integrated in consolidated R2 v0.4 and Architecture v0.7. ERR-R2-02 Option F remains provisionally approved, subject to its independent Windows acceptance gates. Any increased worker ceiling needs new owner approval.
- Initially limit each experiment's numerical BLAS/OMP threading to one, set before numeric imports, and verify effective limits. Warm-started successive historical targets execute sequentially per method unless explicitly partitioned with declared alternative semantics.
- Seed and prediction identities derive from permitted training-view digests and stable method/variant/restart identity; **readout tie keys** have their own versioned hash domain and must never change model-fitting seed/state. No process ID, worker slot, completion order, whole-file source hash or future draw outcome may influence either prediction mechanism.
- Canonical **forecast-content** bytes must ordinarily be identical under **1 and 6 configured workers**, for the same task/configuration, on the same pinned environment; exclude legitimate run/clock/resource metadata from the prediction-content comparison. Any exception needs owner-approved rationale and alternative acceptance.
- A method uses a shared status helper to record its own actual PID, `sys.prefix`, wall/CPU time, peak memory, completion status and approved software versions. The coordinator drains child output, monitors available system memory, supervises the wrapper-rooted process tree with `psutil` and verifies termination on timeout; **do not introduce project-managed Windows Job Objects** for the initial design. First-release methods do not create their own child processes unless specifically approved.
- Preserve the 32 GB memory safety constraint and benchmark presets B1/B10 (`W=100` versus `W=ALL_PERMITTED`). Collect actual startup/fit/predict/total times, CPU and memory measurements, statuses and digests; repeat as practical. **Never show benchmark prediction numbers or merit scores.** Run upgrade/compatibility gates before using a changed Python, virtual environment, package stack or wrapper for research.

### 12.5 Dependency policy — latest owner direction [R3-PROPOSED]

Keep Python 3.14 in the existing project `.venv`; install nothing globally. The single **human-maintained authoritative list of all project PyPI dependencies and install/upgrade commands is `install_upgrade_dependencies_into_venv.bat`**, not a separately maintained `requirements.txt`. Its dependency operations run **only on explicit operator invocation**, with venv checks, package/version display, failure propagation and `pip check`. The script may generate version snapshots/lock reports automatically without imposing a second manual manifest. Preserve and commit the exact environment snapshot (including Python/package versions) with each consequential benchmark, each immutable FINAL forecast batch, the single authorised opening of the original ten-draw holdout, and any historical evaluation run used to support substantive research conclusions. Reference that snapshot by digest from the applicable result/evaluation manifest; use a generated record, never a second hand-maintained dependency list. Keep `.venv/` ignored. Compatibility tests follow upgrades; upgrades never occur incidentally during forecasting.

### 12.6 Configurable runs without hidden defaults [R3-PROPOSED]

At minimum, future command-line or configuration controls should explicitly state:

- `mode`: `HISTORICAL_EVALUATION`, `FINAL_NEXT_DRAW`, `SYNTHETIC_NULL`, `SYNTHETIC_PLANTED`, `BENCHMARK`, and `IN_SAMPLE_DIAGNOSTIC` (R2 section 8.4; a labelled diagnostic, never a scientific result).
- `method_roster` and method/variant revisions; for FINAL, **all registered runnable methods** automatically included and nonrunnable identities also manifested.
- `target_draws` (historical), or automatically `L+1` for FINAL.
- `history_policy`: expanding, rolling-W, method-specific minimum size.
- `observation_view` per method variant and source validation policy.
- `scoring_policy_id` for evaluations; prediction does not look at the same target outcome.
- `worker_limit`, `seed_root`, replay/debug switches, strict/failure behaviour, report destinations.

The complete CLI syntax and executable file layout remain implementation decisions rather than claims of existing functionality.

---

## 13. Acceptance testing and independent verification matrix

The tests below are **proposed R3-specific checks**, additional to and compatible with R2's technical acceptance tests. They are not a requirement to implement all E-methods before testing a basic evaluator. Use independently calculable miniature fixtures, genuine archived outcomes when appropriate, and explicit failures when expected. Test identifiers are deliberately `R3-Txx`, distinct from R2 `T-xx`. The method-ranking tests MRT-01..MRT-25 are in 17.14; that prefix is distinct from both.

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
| R3-T23 | Same method/target/config under one versus six configured worker slots | Canonical full forecast content bit-identical by default; resource/clock/provenance run metadata excluded from content comparison |
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

| R3-T45 | Repeated equal-score ranking; reversed TOP/WORST | `TIE_SHA256_V1` hash-key order bit-identical for fixed canonical tuple; WORST exact reversal of frozen ranking, with no systematic ascending-label tie rule |
| R3-T46 | Change downstream tie/readout version while holding fitted model and training fixed | Fitted parameters, raw scores, fit-seed/state and all pre-readout artefacts remain unchanged; selected TOP/WORST may legitimately change only where tie/readout policy changes |
| R3-T47 | Compare tie readout with post-draw rank-position metric | Equal native scores use mid-ranks independent of their digest ordering and actual outcome; rank-position does not feed into predictor |
| R3-T48 | Change only future draws N and later, then recompute tie ranking for N | Identical permitted training-view digest, hash keys, frozen full ranks, TOP and WORST; snapshot audit metadata may change |
| R3-T49 | Coordinator invokes methods via protected batch wrapper, and operator invokes identical fixture | Same permitted argv/configuration, effective `.venv`, numeric thread limits and canonical forecast bytes; expected failures/exit codes and Ctrl+C proven on Windows |
| R3-T50 | Original holdout is opened, or historical evaluation informs a substantive conclusion | Archived evaluation/holdout record references an immutable resolved Python/PyPI environment snapshot, script revision/digest and applicable source/forecast identities; no separately hand-maintained package list |

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
| R3-D16 | Tie-break policy affecting TOP/WORST | **Propose `TIE_SHA256_V1` deterministic hash-key label-neutral order for equal scores; separate from fit RNG; WORST exactly reverses frozen marginal ranking; rank-position retains mid-ranks** |
| R3-D17 | Seed nomenclature `selection_model_version` | Clarify fit sampling model vs downstream readout; no silent R2 modification |
| R3-D18 | Synthetic calibration role | Ratify distinct artificial reports, allowed design learning and no fitted-state contamination |
| R3-D19 | Speed, independent subprocesses, resource controls | **Option F provisionally**, default/max six workers, self-measurement and psutil supervision; R2 v0.3 Approved Erratum v0.2 governs test-language reconciliation; ERR-R2-02 remains provisional until Windows tests/review; performance cannot delete methods |
| R3-D20 | Timing-proof mechanism for prospective forecasts | **OPEN implementation choice**; GitHub push evidence required, proof strength must be tested |
| R3-D21 | Algorithmic ranking of a single project “best” method | **PARTLY DECIDED** (MRD-01, MRD-05, RK-1..RK-6, R3 17): per-measure league tables, as reports only. A single combined best-method score or automatic champion remains **OPEN**. |
| R3-D22 | Interpretation thresholds for departure from chance | **OPEN**; avoid a priori assumptions as eligibility tests and disclose search multiplicity |
| R3-D23 | Optional ordered-sequence performance scoring | **OPEN**; separate from seven-set TOP/WORST |
| R3-D24 | Persistent checkpoint/restart semantics | **OPEN**; not implicit from `transitory_data/` |

### 14.1 Decisions suitable to ratify as the initial evaluation core

Proposed initial **core**: R3-D01 through D07, D09–D10, D13–D14, **D16–D19**, with D08's windows optional but recommended. This includes enough exact scoring and provenance to avoid choosing TOP/WORST/rank definitions after genuine outcomes become known. It does not choose an automated single best method, a special significance threshold or a first implementation of 62 sophisticated algorithms.

### 14.2 Questions that can remain open until implementation planning

Actual storage schemas, remote publication proof mechanics, optional probabilistic scores and formal hypothesis-level discovery thresholds can be resolved in a controlled, versioned step before running affected real forecasts. **Tie resolution (R3-D16) is now proposed concretely and should be ratified before any affected genuine forecast rather than deferred as an unspecified tie policy.** In particular, **R2-T39 already requires ratifying the core TOP/WORST/rank-position measures before a separately authorised genuine FINAL forecast**. R3 should not be considered permission to sidestep that gate.

---

## 15. Proposed post-R3 implementation roadmap

**I1 — Minimal, testable research apparatus:** CSV validation and draw-number cutoffs; immutable typed forecast/actual/evaluation payloads; method registry; deterministic ranking/selection services; score evaluator; basic independent-subprocess coordinator and wrapper proof-of-concept; canonical hashing; technical tests for leakage and TOP/WORST separation. Start with synthetic *unit fixtures* and legally generated miniature independent data where useful; do not convert test-fixture results into evidence about real lottery predictions.

**I2 — Initial six experiments:** Define/approve the necessary exact mathematical variants of E_1–E_6, implement truthful ranking outputs, verify TOP+WORST and rank-position evaluator separation, and conduct permitted development-period walk-forward testing. Expand method by method rather than inventing one giant script with unstable variants.

**I3 — Additional E_7–E_62 and beyond:** Implement each gradually with unit fixtures, capability declarations, numerical validation, benchmarks and research diagnostics. Retain unsuccessful, speculative, diagnostic and computationally expensive models. Investigate acceleration only after measurements justify it.

**V1 — Controlled historical final holdout:** Freeze each game’s experiment roster/study manifest, environment, evaluation plan and owner approval *before* sequentially releasing the fixed ten; the current Mode H storage mechanism remains OPEN and must receive its own review.

**P1 — First genuine prospective batch:** After preparation and scoring rules are fixed, refresh source, compute L+1 from the current complete observations, archive the entire registered roster's results/statuses, push a verifiably pre-draw batch and subsequently evaluate against the real outcome. Repeat with newly completed genuine draws while preserving earlier frozen predictions.

**C1 — Further research:** New mathematically distinct candidate ideas, external covariates, pilot-wave refinements, inverse-rank methods and combinations remain welcome within the owner's agreed extension allowance; add new E-identities only through documented approval.

Each stage receives its own implementation documents and acceptance evidence. This R3 draft **does not** create executable code or authorise a live forecast by itself.

---

## 16. Sources, historical cross-reference and present status

### 16.1 Governing local documents consulted

1. `doc/Predictive_Randomness_Research_Project_Proposal_v0_3.md` — particularly §§2, 5, 9–12, 14–15 (philosophy, holdout, retention, synthetic separation, evidence and development phases).
2. `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` — §§1, 4, 7–9 (operator-labelled drawn order, method hypotheses E_1–E_62, research streams, deferred evaluation decisions and benchmark separation).
3. `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` — §§2–6, 8–13, T-01–T-39 (method outputs, TOP/WORST and rank-position, source cutoff, prospective batch, stable seed, reproducibility, evaluation handoff and technical tests).
4. Claude's R2 v0.2 review and **Claude's subsequent review of R2 v0.3 as transmitted by the owner**, noting the optional seed-terminology clarification. The latter comments are in the project conversation rather than an independently opened repository review file here.

The R2 v0.3 document still labels itself an unratified review candidate internally; the **owner expressly ratified R2 v0.3 afterward on 22 October 2026**. The original ratified R2 remains unchanged pending the owner ratification of consolidated R2 v0.4. Current ratification status is governed by explicit owner decisions, not by stale internal headers in a preserved review document.

### 16.2 Exact arithmetic provenance

The reference probabilities in §4 follow directly from the legal seven-from-35 without-replacement and one-from-20 definitions and were independently recalculated from integer combinations for this draft. No live forecast or experimental R3 result was computed. The illustrative sets and scores in §11 are invented only to demonstrate reporting layouts and must not enter real source or prediction records.

### 16.3 Explicit non-claims

- No E-method has been implemented as a new working predictor under this R3 draft.
- This evaluation specification has not authorised new real-world runs. The separately accepted E_1 forecast-only target-1577 regression is documented; it has not been scored as holdout evidence.
- The original holdout's outcomes are present in the available historical source files but were **not used to fit, compare or select an E-method in drafting this document**.
- The R3 statistical reference does not establish that the real lottery is independent, quantum-mechanical, deterministic, biased, unpredictable or predictable.
- The optional method-combination examples are conceptual; no weights, active champions or production scoring thresholds have been chosen.

### 16.4 Requested owner review

Review the proposed **evaluation core** (TOP/WORST matches, mid-rank position, missingness and denominators), the separate synthetic/evidence treatment, and the prospective batch/reporting requirements. The key open choices are prediction-time ties, optional scores, and the exact remote publication proof procedure. After review and any revisions, the owner may ratify R3. Only then should the next implementation specifications and staged Python development proceed.

**Closing principle:** The point of this project is to challenge perceived randomness rather than to protect a received explanation. The point of honest pre-outcome forecasting and an auditable evaluator is to give extraordinary, ordinary and disappointing results alike the strongest possible opportunity to be understood.


---

## 17. Method ranking measures (league tables) [MR-RATIFIED]

This section carries the owner-ratified **Method Ranking Measures Proposal v0.5** (`doc/Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_5.md`, SHA-256 `c6ca2cb2174ee2963a6fe33347820c80b92e6dd1eda518a1f0c8e3254d67ab19`, ratified 26 October 2026 at commit `ac01678`). It is the governing text on its subject. The proposal file is kept unchanged as history.

- **Numbering:** 17.x here is section x of the proposal (for example 17.5A is proposal 5A, 17.3.7A is proposal 3.7A). Parts with a home elsewhere leave a short pointer:
  - proposal 3.2 (numbering conventions) -> R2 section 3.6;
  - proposal 7.1-7.4 (in-sample mode, procedure, capability, firewall) -> R2 section 8.4; proposal 7.5 stays here as 17.7.5;
  - proposal 8 (supplementary-number rule) -> R2 section 2.5;
  - proposal 12 (execution model) -> Architecture sections 5A.4 and 12.5; the evaluator rules stay here in 17.12;
  - proposal 13 stage-1 contract fields and the acceptance list before E_2 -> R2 section 5.6.
- Proposal section 15 (the integration plan) is carried out by this edition set and is not repeated. Proposal 17.2-17.4 (traceability to the review rounds) stay only in the proposal file.
- **Authority:** this section grants no run, coding, data-access or holdout authority. It changes nothing in Package 2 v0.11, and P3 v0.2 is unchanged.
- **Status:** provisions in this section are owner-ratified as written. Items marked OPEN or DEFERRED in 17.16 remain undecided.
- **Holdout discipline:** this section contains no winning, Powerball or supplementary number of any draw. All figures are fair-draw reference calculations.

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

### 17.0 Scope in one paragraph

After the project has produced forecasts for many historical target draws, the owner wants to **rank the methods by how successful their forecasts would have been**, always separately for Powerball and Oz Lotto.
- It runs **independently of production prediction runs**.
- It uses prize divisions and further statistical measures.
- It prints every number used, with a plain explanation of what each measure means and how far each figure can be trusted.

There are two modes:
- **Walk-forward (WF):** the honest mode. Each forecast used only draws before its target.
- **In-sample (IS):** a diagnostic the owner explicitly requested, knowing it is biased. The method is trained once on all available draws, and that fit is scored against draws that were part of its own training.

The modes are never ranked against each other as competitors, but every applicable measure is shown with both modes side by side.

The project is deliberately speculative. Conventional statistics is used here **as an instrument for telling kinds of pattern apart, never as a gate** on which ideas, methods or measures may be investigated or reported.

### 17.1 Purpose (the owner's intent, restated)

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
4. Keep the rankings as **reports**. They never alter forecasts. Any use of rankings to choose methods is itself a registered, honestly tested method (17.9).

The owner expects the most likely final outcome to be that no method predicts as hoped. The aim is to find out whether careful, broad testing can spot anything conventional statistics has missed. A well-measured null result is a valid outcome.

### 17.2 Owner decisions recorded (26 October 2026)

| ID | Decision |
|---|---|
| MRD-01 | The league-table concept is accepted, with Claude's corrections: in-sample bias labelled; modes never mixed in one ranking; Oz window within the current format; supplementaries; meta-method rule; housekeeping. |
| MRD-02 | Measure and report **all prize divisions** (Powerball 9, Oz Lotto 7), not only Divisions 1-3. Very small numbers are acceptable; full-width integers and floats were chosen for this. |
| MRD-03 | **The ratified rule changes so that supplementary numbers are included in scoring** (Oz Lotto Divisions 2, 4 and 7 need them; the Oz master already stores them). **Scope: scoring and measuring only, never predicting.** Apart from Powerball's separate barrel, a prediction is only a set of numbers, and no number is designated in advance as a supplementary (R2 section 2.5). |
| MRD-04 | **Current-format draws only** (Proposal section 3.1). The Oz Lotto window never starts before draw 1474 (17 May 2022). |
| MRD-05 | Rankings never feed forecasts. Claude decides the rule for any use of rankings to choose methods (17.9). |
| MRD-06 | Significance is shown on the **sigma scale used in public science reporting** (1 to 6 sigma). **Zero wins is 0 excess sigma.** A deficit sigma is reported separately and can be nonzero when wins were expected (17.5). |
| MRD-07 | Housekeeping: measure IDs `MR..`; the weight typo corrected; processing in draw-number order; UTC timestamps in file names; windows never past opened and scored draws. |
| MRD-08 | Claude's measures MR11-MR15 are accepted (formulas as corrected in proposal v0.5, carried in this section). |
| MRD-09 | **Reporting rule:** every measure, method, variant, status and mode is reported with its **ID, name, one-line summary and a short explanation**, so its meaning is never lost from a report. |
| MRD-10 | The forecast for target draw N is trained on the current-era draws from the era's first draw through **N-1 inclusive**. |
| MRD-11 | One numbering convention everywhere (R2 section 3.6), consistent with conventions R2/R3 already use. |
| MRD-12 | The time axis is the **draw number** (already ratified). "Date order" means ascending draw-number order. |
| MRD-13 | The ranking is run **independently** of production prediction runs, never inside the weekly FINAL batch. |
| MRD-14 | Keep **MR1-T**, the owner's 90/7/3 weighting of Divisions 1-3, alongside the all-division score MR1. |
| MRD-15 | Accept ChatGPT's findings B1-B4, C1-C10, O1-O8 and the stage-1 contract fields, **with Claude's dispositions** (Claude response v1). |
| MRD-16 | Adopt MR6-MR10 (ChatGPT's proposals) and the optional mirror MR10.BOTTOM. |
| MRD-17 | Adopt the **N1 fair-draw null simulator** (17.5A). |
| MRD-18 | **Multiplicity:** Bonferroni over comparison families declared in advance is the guaranteed global figure; the N1 maximum-statistic figure is shown alongside (v0.4: as a labelled reference for adaptive methods, 17.5A); a programme-wide search log counts every report; exploratory tables are allowed, labelled and counted (17.5B). |
| MRD-19 | Defaults: the MR13 prior scale is 0.5, also tested at 0.25 and 1.0; results on fewer than 30 draws are flagged `LOW_N`; the extra Oz Lotto measures use main numbers only; N1 runs **R = 10,000** replicates per calibrated table. |
| MRD-20 | Record exposure item 6 (ChatGPT's unsolicited search preview) in `HOLDOUT_EXPOSURE_RECORD_v0_2.md`. |
| MRD-21 | **Mark, never suppress.** The owner knowingly accepts in-sample bias. Every number requested is calculated and shown. Where a figure is not a calibrated probability, it carries a label saying so; it is never withheld for that reason. |
| MRD-23 | Show **walk-forward and in-sample results side by side** for every applicable measure. Each mode keeps its own rank column; the two modes never compete in a single ranking (17.7.5). |
| MRD-24 | The terms **walk-forward** and **in-sample** are generic, so every report prints their exact meaning in this project, and every table and file header uses self-explanatory display names (17.3.5A). |
| MRD-22 | Adopt **MR16**, the hit-rate estimate with an exact interval and a "detectable at this n" line (from v0.5 named "observed hit-rate threshold for local 3 sigma"), so the limits of the small samples are visible in every report. |

### 17.3 Conventions and definitions

#### 17.3.1 Identity and time axis

- Every draw is identified by `(game_id, draw_number)`; `game_id` is `POWERBALL` or `OZLOTTO`. Draw numbers are the operator's official numbers.
- **The draw number is the time axis.** All processing is in ascending draw-number order. Dates are never used for ordering or arithmetic.
- Games are never pooled. Every table, statistic, file and ranking belongs to one game.

#### 17.3.2 Numbering conventions

The numbering conventions (proposal 3.2; MRD-11) are project-wide and live in R2 section 3.6. They apply unchanged to everything in this section.

#### 17.3.3 Training set (walk-forward)

For game G with first current-era draw E(G) (Powerball 1144, Oz Lotto 1474):

    H(N) = { eligible draws d of game G with E(G) <= d <= N - 1 }

This is the ratified strict N-1 rule (R2), in the owner's words: "0 to Pi-1 inclusive when predicting Pi", where 0 is the era's first draw.

#### 17.3.4 Track and entry

- A **track** is a forecast stream (game, method E_n, variant, readout, mode), with readout `TOP` or `WORST` and mode `WF` or `IS`.
- Per target draw a track supplies one **entry**:
  - Powerball: 7 distinct main numbers from 1-35 plus 1 Powerball from 1-20;
  - Oz Lotto: 7 distinct numbers from 1-47.
- Methods never forecast supplementaries (MRD-03). An unavailable readout (for example `INVERSE_UNAVAILABLE`) leaves that target unscored for that track, and the status is counted.
- TOP and WORST of one method and variant come from **one ranking**. They are dependent and never counted as unrelated evidence.

#### 17.3.4A Analysis units

Each measure is computed on exactly one analysis unit:

| Unit | Meaning | Measures |
|---|---|---|
| `READOUT_TRACK` | One readout (TOP or WORST) of one method/variant/mode | MR0-MR4, MR7, MR8, MR9, MR12, MR13, MR15, MR16 |
| `METHOD_VARIANT_RANKING` | The single full ranking of one method/variant/mode | MR5, MR10, MR10.BOTTOM |
| `METHOD_VARIANT_PROBABILITY` | The probability vector(s) of one method/variant/mode | MR6, MR14 |
| `TOP_WORST_PAIR` | The paired TOP and WORST readouts of one method/variant/mode | MR11 |

- CSV rows, league-table rows and family test counts are keyed by `(analysis_unit, unit_id, sub-measure)`. `unit_id` binds `(game_id, method_id, variant_id, mode)` (plus the readout for `READOUT_TRACK`), and the sub-measure names the channel (`.MAIN` / `.PB`) and any division, so separate channels never overwrite each other or merge into one hypothesis (MRT-23).
- A method-level value is never duplicated into two apparent TOP and WORST tests, and each distinct hypothesis is counted once in M.
- If one readout is unavailable for a target, `TOP_WORST_PAIR` measures skip that target, and the count is reported.

#### 17.3.5 Modes

- **WF:** the entry for target N comes from the method's frozen forecast record for N, fitted on H(N) (R2/R3 historical evaluation).
  - The ranking tool **does not re-run methods** in WF; it reads stored frozen records.
  - A retrospective WF run done after all outcomes are known still needs mechanical no-leakage proof and frozen input identities. It is historical evaluation, not advance-frozen prospective forecasting (17.3.9).
- **IS:** R2 section 8.4 (with 17.7.5 for the side-by-side display). One full fit on all eligible draws up to the window end, applied to every target. Labelled `IN_SAMPLE_DIAGNOSTIC`.

#### 17.3.5A Plain meanings of the two modes (MRD-24; printed in every report)

The short codes `WF` and `IS` are used in IDs and file names. Everywhere a person reads a result (report headers, the glossary, table titles and column headings, the CSV header row and the JSON manifest), the mode is shown with its **display name and its plain meaning**, word for word as below.

**WF - Walk-forward ("honest test: trained on earlier draws only")**
> For every past draw that is scored, the method was trained **only on the draws before it**, then its prediction for that draw was compared with the actual result. This is exactly the position in real life, where the next draw is unknown when the prediction is made. It is an honest test of prediction.

**IS - In-sample ("hindsight fit: trained on all draws, including the ones scored")**
> The method was trained **once on every draw in the history**, including the draws it is then scored against, and its predictions were checked against those same draws. It shows how well the method describes results it has already seen. It is **not** a test of prediction, and its success figures can be inflated by hindsight. How much depends on the method. In a separate fair-draw illustration using this project's E_1 method, in-sample fitting alone produced an apparent gain of about 3 sigma; that is not a general value for all methods (R3 section 17.18.3).

**Rules:**
- **Column headings** use the display names, for example "Walk-forward (earlier draws only)" and "In-sample (hindsight: all draws)". A bare "WF" or "IS" never appears alone in a heading.
- **The difference column** is headed "In-sample minus walk-forward (hindsight advantage)".
- **Every IS page** keeps the banner in R2 section 8.4.4, in addition to its display name.
- These texts are held in `MEASURE_REGISTRY_V1` with the measure texts and versioned with them. Test MRT-13 checks that they are present.

#### 17.3.6 Window

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

#### 17.3.7 Scored set, cohorts, comparison set and report statuses

- **Scored set:** targets in W with readout status `PREDICTION_AVAILABLE` (R3). Every other status is counted per track, with reasons.
- **Cohort:** the set of tracks in a league table.
  - **Calibrated tables** (those showing a guaranteed Bonferroni global figure) use a **predeclared cohort**, registered before the first report that uses it, with a membership digest (17.5B).
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

#### 17.3.7A Fixed opportunity grid (condition for exact and N1-calibrated figures)

A per-draw hit-code law that is the same whatever ticket is picked makes single-track statistics exact **only on an opportunity set fixed independently of the outcomes being scored**. If outcomes can decide which targets are scored, or when a track stops, a fixed-n tail is not calibrated. ChatGPT's stopping-rule counterexample, reproduced by Claude, gives about 9.87% false alarms at a nominal 5%.

- **Fixed grid:** for each table, the opportunity grid is every target in the declared window [S, L], for every unit in the cohort. Window, cohort, readouts, units, stopping rule (none: the whole window) and family are fixed and recorded before the report is computed.
- **Availability that cannot depend on outcomes** keeps the calibrated status. Examples:
  - `INSUFFICIENT_HISTORY`, which depends only on the draw number and the method's declared minimum history;
  - a structurally constant `INVERSE_UNAVAILABLE`.
- **Availability that could depend on outcomes** sets the table's significance figures (`EXACT_LOCAL`, `N1_CALIBRATED`, guaranteed Bonferroni) to the label `SELECTION_UNVERIFIED`. The figures themselves are still computed and shown, each with its count of affected targets. Examples:
  - `RUNTIME_FAILURE`, `NUMERIC_INVALID` or `TIMEOUT` on some targets;
  - any readout withheld by a data-dependent rule;
  - any early stop.
- **Restoring calibrated status:** only a separately verified selection-aware or sequential null may restore it.
- **Not enough on its own:** a predeclared cohort does not establish a fixed grid by itself.

#### 17.3.8 Scored-opportunity gaps (used by MR2, MR3)

Within C, sorted by draw number, scored target k has opportunity index k = 1..n. For a track's wins at opportunity indices o_1 < ... < o_k:
- the **opportunity gap** is o_(i+1) - o_i;
- the **opportunities since** the last win, counted to the next draw after the window, is (n - o_k) + 1.

The +1 counts the next draw, L+1, as the next opportunity. This convention is stated in every report.

Draw-number gaps are also shown, labelled descriptive.

#### 17.3.9 Evidence tiers and pattern origins

Every report states its **evidence tier**:
- `DEVELOPMENT_WF_EXPLORATORY`: walk-forward on development data that methods, windows and measures may have been designed against;
- `HOLDOUT_MODE_H`: FINAL_HOLDOUT_10 after Mode H scoring;
- `PROSPECTIVE`: forecasts frozen and published before their draws;
- `IS_DESCRIPTIVE`: in-sample.

A development league table is always exploratory, whatever its p-values. No development ranking alone supports a "discovery" claim. Selection provenance is recorded: method versions, windows, measures, and any development-driven changes.

Every report also explains the **four possible origins of an apparent pattern**:

| ID | Origin | How the project distinguishes it |
|---|---|---|
| PO-1 | An unavoidable consequence of how the method works | Partly diagnosable: N1 fixed-forecast replays show some method-built patterns, but not all for adaptive methods (17.5A). Planted-effect and null synthetic tests (MRT-07). A full recursive simulator (MRO-10) would cover more. |
| PO-2 | An effect of fitting to past outcomes | Present in IS by construction; absent in WF by N-1 isolation. Shown by the IS-versus-WF comparison. |
| PO-3 | Chance, many comparisons or selection | Bonferroni, the N1 maximum statistic, the search log, predeclared cohorts. |
| PO-4 | A pattern that persists on genuinely new outcomes | Only HOLDOUT_MODE_H and PROSPECTIVE tiers can show it. |

All four are worth exploring. The reports keep them distinct.

### 17.4 Per-draw match record and division classification

#### 17.4.1 Match record (one per track per scored target)

Powerball record:

| Field | Type | Meaning |
|---|---|---|
| `game_id` | text | `POWERBALL` |
| `draw_number` | int64 | target draw |
| `track_id` | text | see 17.3.4 |
| `mode` | text | `WF` or `IS` |
| `main_matches` (m) | int64, 0..7 | entry main numbers equal to a drawn main number |
| `powerball_match` (b) | int64, 0..1 | entry Powerball equals the drawn Powerball |
| `division` | int64, 0..9 | 0 = none |

Oz Lotto record:

| Field | Type | Meaning |
|---|---|---|
| `game_id` | text | `OZLOTTO` |
| `draw_number` | int64 | target draw |
| `track_id` | text | see 17.3.4 |
| `mode` | text | `WF` or `IS` |
| `main_matches` (m) | int64, 0..7 | entry numbers equal to a drawn winning (main) number |
| `supplementary_matches` (s) | int64, 0..3 | entry numbers equal to a drawn supplementary; s <= 7 - m |
| `division` | int64, 0..7 | 0 = none |

These are evaluator outputs, written only after the target's outcome is opened. They are never fed back to any method.

#### 17.4.2 Powerball divisions

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

#### 17.4.3 Oz Lotto divisions

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

#### 17.4.4 Fair-draw moments used by several measures

| Quantity | Powerball | Oz Lotto |
|---|---|---|
| Mean main matches per entry | 7/5 = 1.4 | 49/47 = 1.04255 |
| Variance of main matches | 392/425 = 0.92235 (sd 0.96039) | 39200/50807 = 0.77155 (sd 0.87838) |
| Powerball match probability | 1/20 (variance 0.0475) | (no Powerball) |
| P(main matches >= m), m = 0..7 | 1, 0.823922, 0.431748, 0.124830, 0.0182608, 0.00120975, 2.92958e-5, 1.48709e-7 | 1, 0.703560, 0.276337, 0.0566231, 0.00576327, 0.000264917, 4.46801e-6, 1.59004e-8 |
| One-draw main-match probabilities p_G,m | C(7,m) x C(28,7-m) / C(35,7) | C(7,m) x C(40,7-m) / C(47,7) |

The main-match distribution is hypergeometric.

### 17.5 Significance: sigma convention and calibration labels (MRD-06, MRD-21)

#### 17.5.1 Definitions

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

#### 17.5.2 Calibration-status labels (on every significance figure)

| Label | Meaning |
|---|---|
| `EXACT_LOCAL` | Exact reference tail for this single track and sub-measure (for example binomial division counts, MR7, MR8, MR11). |
| `APPROX_UNCALIBRATED` | Normal or other approximation not yet checked against N1. Shown, labelled. |
| `N1_CALIBRATED` | Probability from N1, **only** for single-track statistics in the hit-sequence class (17.5A), where the replay is exact even for adaptive methods. The Monte Carlo uncertainty is shown. |
| `N1_FIXED_FORECAST_REFERENCE` | N1 replay figure for any other statistic (cross-track maxima; measures scored with forecast weights or probabilities). Shown as a reference; not a calibrated probability for adaptive WF methods. |
| `SELECTION_UNVERIFIED` | The table's opportunity set is not a fixed grid (17.3.7A), so exact or N1 tails are not calibrated. The figures are shown. |
| `BONFERRONI_REFERENCE_UNCALIBRATED` | Bonferroni arithmetic applied where its prerequisites fail (an input not `EXACT_LOCAL`/`N1_CALIBRATED`, or a post-hoc family). Shown; not a guaranteed figure. |
| `IS_NOT_CALIBRATED` | Any significance figure in an IS table. The number is shown, but because the method was fitted on these outcomes it is not a calibrated probability (R2 section 8.4). |
| `NOT_A_P_VALUE` | Descriptive scores and Bayes factors. |

#### 17.5.3 Global significance (MRD-18)

- **Bonferroni:** P_Bonf = min(1, M x P_up) for a family of M tests; Z_plus_Bonf = max(0, Phi_inv(1 - P_Bonf)).
  - It is **guaranteed**, whatever the correlation between tests, only when every input p-value is valid under its null (`EXACT_LOCAL` or `N1_CALIBRATED`, which includes the fixed-grid condition of 17.3.7A) and the family is predeclared (17.5B).
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

#### 17.5A N1 - fair-draw null simulator (MRD-17)

- **What N1 does:** it replays R sets of fair outcomes against the actual stored WF forecasts, without refitting.
- **Where it is exact: the hit-sequence class, on a fixed grid (17.3.7A).** For a statistic computed only from one track's own per-target outcome codes (main matches m_t, Powerball hit b_t, supplementary matches s_t, division), on an opportunity grid fixed independently of the outcomes, the replay is **exact even for adaptive methods**.
  - Under a fair draw, the distribution of (m_t, b_t, s_t) for any ticket of the fixed shape is the same whatever numbers it contains. So these codes are independent and identically distributed across targets however the ticket was chosen from earlier outcomes.
  - Verified: in a 4-draw toy with an adaptive method, the true and replayed distributions of the hit count agree exactly.
  - The class covers MR1, MR4, MR7, MR8, MR9, MR11 (the TOP and WORST sets are disjoint and the same size, so the pair's joint code distribution is also invariant), MR12, MR15 and MR16.
  - For this class N1 may equally simulate the codes directly. Its results are labelled `N1_CALIBRATED`.
- **Where it is only a reference:**
  - (a) **Maxima or other joint statistics across tracks.** The joint law of different tracks' hits depends on how their forecasts overlap, and adaptive overlap depends on earlier outcomes. ChatGPT's exhaustive 4-draw counterexample, checked by Claude, gives a true probability of 1/16 but a replay probability of 15/128.
  - (b) **Single-track measures scored with forecast-dependent weights or probabilities:** MR5, MR6, MR10, MR10.BOTTOM, MR14. Verified with a forecast-weighted toy: true and replayed distributions differ.
  - These are labelled `N1_FIXED_FORECAST_REFERENCE`. Their approximate local Z stays `APPROX_UNCALIBRATED`. Martingale arguments make the standardised sums approximately normal, but that is not exactness.
- **Not valid for IS** (R2 section 8.4).
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

#### 17.5B Families and the search log (MRD-18)

- **Family:** a named, versioned set of (cohort, sub-measures, window, mode, game), registered in `FAMILY_REGISTRY` with a digest **before** the first report that uses it.
  - M is the number of distinct (analysis_unit, unit_id, sub-measure) tests in the family (17.3.4A).
  - Main and Powerball channels are separate families unless a joint family is declared.
- **Search log:** the single programme-wide search record defined in R3 section 7.4 (`results/audit/SEARCH_LOG.csv`), append-only and committed. Each report run appends exactly one row with `row_type` = `RANKING_REPORT`:
  - UTC time, game, mode, window, cohort and digest, family IDs or `EXPLORATORY_COHORT`, the number of tests, measures, tool version and SHA.
  - It shows how much searching was done, including exploratory tables, reruns and window changes. A family declared after its results were inspected is recorded as such, and its Bonferroni figure is labelled `POST_HOC_FAMILY`.
- Exploration stays free: any table may be produced, provided it is labelled and logged.

### 17.6 Measure registry

Every measure has:
- its ID, name, **one-line summary** and **short explanation** (MRD-09);
- an exact definition;
- its ranking key(s);
- edge cases;
- outputs;
- its calibration status (17.5.2).

The texts are versioned in `MEASURE_REGISTRY_V1` and printed in every report's glossary.

**Notation:**
- `MRk.PDd` / `MRk.ODd`: measure k at Powerball / Oz Lotto division d.
- `MR4.X.d`: exactly division d. `MR4.C.d`: division d or better. `MR4.B.a-b`: band a..b.
- `.MAIN` and `.PB`: channels. Oz Lotto has MAIN only for MR6-MR15 (MRD-19).
- n = draws in C. W_d = the count of division-d wins. p_d = division-d probability. b_d = -log2 p_d.

**Two ranking tables where relevant:** a **descriptive** table (by the raw score) and a **significance** table (by local Z_plus, with global figures). They are never conflated.

**Measure IDs:** MR0-MR4 derive from the owner's R0-R10 (17.17); MR5 is R3's existing measure; MR6-MR10 are ChatGPT's (MRD-16); MR10.BOTTOM is Claude's mirror; MR11-MR15 are Claude's; MR16 is the owner-requested hit-rate interval (MRD-22). Each measure's analysis unit is listed in 17.3.4A.

#### MR0 - Division win profile

- **One line:** who has won the best prizes, best division first.
- **Short explanation:** counts how many times the track's entries would have won each prize division. Tracks are ranked by top-division wins first, then the next division, and so on. Top-division wins are extremely rare under a fair draw, so most tracks share the same counts at the top; the lower divisions carry most of the information.
- **Definition:** V = (W_1, ..., W_D), with D = 9 (Powerball) or 7 (Oz Lotto).
- **Ranking:** V descending, lexicographic. On the common set C, equal V means equal MR1, so ties share a rank. In `OWN_SET` tables, n differs, so MR1 descending breaks ties.
- **Outputs:** W_1..W_D, n, the expected counts n x p_d. Calibration: `NOT_A_P_VALUE` (see MR4 for significance).

#### MR1 - Surprisal-weighted division score; MR1-T - owner's top-division score

- **One line:** the average "rarity" of prizes won per draw, in bits.
- **Short explanation:** each division win is worth the bits of surprise it represents under a fair draw: about 6.0 bits for Powerball Division 9, up to 27.0 bits for Division 1. MR1 is the average bits won per draw, next to the fair-draw expectation. MR1-T keeps the owner's original weighting of the three top divisions (Division 1 90%, Division 2 7%, Division 3 3%); it is a declared preference score, not a statistical weight.
- **Definition:**
  - MR1 = (1/n) x sum over draws of b(division), with b(0) = 0.
  - E0 per draw: 0.153679 bits for Powerball (sd 1.025914), 0.131326 bits for Oz Lotto (sd 0.931722).
  - Z = (n x MR1 - n x E0) / (sqrt(n) x sd). This is `APPROX_UNCALIBRATED` and heavy-tailed for rare divisions, so it is replaced by an N1 p-value when available.
  - MR1-T = (0.90 x W_1 + 0.07 x W_2 + 0.03 x W_3) / n.
- **Ranking:** MR1 descending (descriptive); Z_plus (significance); MR1-T descending in its own table.
- **Outputs:** MR1, E0, the difference, Z with its label, MR1-T.

#### MR2 - Division recurrence period (per division)

- **One line:** how often, on average, this track wins division d.
- **Short explanation:** for a division won at least twice, this is the average number of scored draws between successive wins. Shorter periods rank higher, with regularity shown alongside. Under a fair draw the expected spacing is about 1/p_d scored draws (about 65 for Powerball Division 9), and wins arrive irregularly. This is a pattern description; ranking the shortest period among tracks with 2 or more wins favours tracks that happened to win twice close together.
- **Definition** (per division d, per track, on C):
  - Win opportunity indices o_1 < ... < o_k (17.3.8), with k = W_d.
  - If k >= 2: mean opportunity period G_d = (o_k - o_1)/(k - 1).
  - CV_d = the sample sd of the opportunity gaps (denominator k - 2) divided by G_d, only when k >= 3.
  - Fair reference: 1/p_d.
  - **Also shown, labelled descriptive:** the draw-number period (N_k - N_1)/(k - 1).
- **Ranking:** defined G_d ascending, then CV_d ascending (defined before undefined), then k descending. Then k = 1, then k = 0, each sharing a rank.
- **Edge cases:** k <= 1 gives `MR_UNDEFINED`. G_d > 0 when defined.
- **Outputs:** k, the first and last win draws, G_d, CV_d, 1/p_d, the opportunity gaps, the draw-number period. Calibration: `NOT_A_P_VALUE`.

#### MR3 - Division "due" alignment (per division)

- **One line:** is this track about due for another division-d win?
- **Short explanation:** compares the scored opportunities since the track's last division-d win, including the next draw, with its average period from MR2. Near 0 means the next draw falls close to the track's usual spacing. Under a fair draw wins have no memory, so this is a pattern indicator, never a reason to exclude a method. Using it to choose methods is itself a forecasting method and must be registered (17.9).
- **Definition:** requires k >= 2. since_d = (n - o_k) + 1 (17.3.8). A_d = |since_d - G_d| / G_d.
- **Label:** "retrospective alignment for a hypothetical next opportunity". The track may not actually forecast draw L+1, so this is never itself a prediction.
- **Ranking:** A_d ascending; undefined last.
- **Outputs:** since_d, G_d, A_d, the signed since_d - G_d, and the draw-number equivalent (labelled descriptive). Calibration: `NOT_A_P_VALUE`.

#### MR4 - Division sigma (excess wins)

- **One line:** how many sigma above fair-draw chance this track's division wins are.
- **Short explanation:** counts the track's wins in a set of divisions and asks how likely at least that many would be under a fair draw over the same draws. That probability is shown on the sigma scale used in science reporting. Zero wins is 0 excess sigma. The local figure treats the track alone; the global figures allow for how many tests were made.
- **Definition:** for a division set S: p_S = the sum of p_d over d in S (exact); k_S = wins in S; X ~ Binomial(n, p_S); P_up and P_lo exact. Then 17.5.
- **Sub-measures:**
  - `MR4.X.d` (every d);
  - `MR4.C.d` (every d);
  - the owner's original sets `MR4.C.3` (owner R8), `MR4.B.2-3` (owner R9) and `MR4.X.3` (owner R10).
- **Ranking:** Z_plus descending, then k_S descending, then shared rank.
- **Outputs:** k_S, n, n x p_S, P_up, the reference confidence, local Z_plus and level, Bonferroni (guaranteed) and N1 maximum-statistic (reference) global figures, local Z_minus. Calibration: `EXACT_LOCAL`.

#### MR5 - Rank position (existing R3 measure)

- **One line:** where the method's ranking placed the numbers that were actually drawn.
- **Short explanation:** R3's ratified evaluator measure: the average mid-rank of the 7 drawn main numbers in the method's full frozen ranking (1 = most favoured), and the drawn Powerball's mid-rank. Fair-draw expectations are 18.0 (Powerball main), 10.5 (Powerball) and 24.0 (Oz Lotto). Lower means the method tended to favour numbers that came up. It belongs to the method and variant, because TOP and WORST share one ranking.
- **Definition:**
  - Per target, `mean_rank_main` and `rank_powerball` (R3). MR5.MAIN and MR5.PB are their means over C.
  - Per-target fair variance of the 7-label mean given the frozen mid-rank vector r: var_r x (N - 7) / (7 x (N - 1)), with N = 35 or 47.
  - Z = (sum of expected - sum of observed) / sqrt(sum of variances); `APPROX_UNCALIBRATED`, with an N1 reference figure (`N1_FIXED_FORECAST_REFERENCE`).
- **Ranking:** MR5 ascending (descriptive); Z_plus (significance).
- **Outputs:** the MR5 mean, its expectation, Z_plus, Z_minus.

#### MR6 - Logarithmic probability quality (ChatGPT)

- **One line:** rewards probability forecasts that gave more probability to the numbers actually drawn, and heavily penalises overconfident misses.
- **Short explanation:** a strictly proper logarithmic score for the probability the method gave to a drawn main number (one of the seven chosen at random). It complements MR14 fidelity, but unlike MR14 it sharply penalises giving near-zero probability to a number that came up. It does not score the full seven-number event.
- **Applicability:** a typed main-channel probability output (R2 section 5.6, field 3).
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
    - Such targets are excluded from MR6's significance figure and kept in the raw score G. Reports show both n (raw-score count) and n_sig (significance-valid count).
    - If n_sig = 0, the significance status is `MR_INSUFFICIENT_DATA`, never numeric zero sigma. The implementation never evaluates minus infinity minus minus infinity.
    - N1 replays treat them the same way.
  - Negative, non-finite or wrongly normalised q gives `MR_NUMERIC_INVALID`.
  - Sum of v_t = 0 gives `NULL_VARIANCE_ZERO`.
- **Ranking:** G descending (descriptive); Z_plus (significance).
- **Outputs:** G, the sum of g, the mean e, the excess, Z_plus, Z_minus, n, the probability semantics, the null-variance flag.

#### MR7 - Total main-match excess (ChatGPT; core stage)

- **One line:** did the track hit more main numbers in total than fair draws would produce?
- **Short explanation:** counts **every** main-number match, prize or not. It is the most direct test of a steady advantage and applies to every method that produces tickets.
- **Definition:**
  - S = the sum of m_t over C.
  - The exact null distribution of S is given by the coefficients of A_G(z)^n, with A_G(z) = sum over m = 0..7 of p_G,m z^m (17.4.4).
  - P_up = P(S_null >= S), P_lo = P(S_null <= S).
  - PB channel: B = the sum of b_t, ~ Binomial(n, 1/20).
  - MAIN and PB p-values are never combined without a declared joint rule.
- **Ranking:** S - n x mean0 descending (descriptive); Z_plus (significance).
- **Outputs:** n, S, S/n, mean0, Var0, observed minus expected, P_up, P_lo, Z_plus, Z_minus, the PB analogue. Calibration: `EXACT_LOCAL`.

#### MR8 - Longest match streak (ChatGPT)

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

#### MR9 - Early versus late change (ChatGPT)

- **One line:** did the track's matching get better or worse in the later half of the window?
- **Short explanation:** separates a rising or falling pattern from one good overall score. It measures change over time, not whether a change will persist.
- **Definition:**
  - Split C (sorted by draw number) at n_early = floor(n/2), n_late = n - n_early. The split is fixed, never optimised.
  - Means a (early) and b (late). Delta = b - a.
  - Var0(Delta) = sigma0^2 x (1/n_early + 1/n_late), with sigma0^2 from 17.4.4.
  - Z = Delta / sqrt(Var0); `APPROX_UNCALIBRATED`, replaced by `N1_CALIBRATED` when N1 runs (hit-sequence class). Z_plus covers improvement, Z_minus deterioration.
  - PB channel: Bernoulli variance 0.0475.
- **Edge cases:** n < 2 gives `MR_UNDEFINED`. A change of split is a new sub-test.
- **Ranking:** Delta descending (descriptive); Z_plus (significance).
- **Outputs:** the early and late counts and means, Delta, the variance, Z_plus, Z_minus, the boundary draw numbers.

#### MR10 - Top-rank discounted gain (ChatGPT); MR10.BOTTOM - bottom-rank mirror (Claude)

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

#### MR11 - TOP versus WORST contrast

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

#### MR12 - Information gain (Shannon surprisal)

- **One line:** how much more surprising, in bits, this track's matches were than chance.
- **Short explanation:** each draw's match count is scored by how surprising "at least this many matches" would be under a fair draw: 7 matches is about 22.7 bits, while 0 or more matches is 0 bits. The total is compared with the fair-draw average. This is Shannon's measure of information, the everyday-world limit of the entropy used in quantum theory. It ranks tracks even when no prize was won.
- **Definition:**
  - MAIN channel: u_t = -log2 P0(M >= m_t); U = the sum of u_t.
  - Fair per-draw mean and sd: Powerball 0.911756 / 1.138676; Oz Lotto 0.879151 / 1.143974.
  - Z = (U - n x mean)/(sqrt(n) x sd); `APPROX_UNCALIBRATED`, replaced by `N1_CALIBRATED` when N1 runs (hit-sequence class).
  - PB channel: u = 4.321928 bits on a hit, otherwise 0; mean 0.216096, sd 0.941942.
- **Ranking:** U - expected descending (descriptive); Z_plus (significance).
- **Outputs:** U, the expected U, the excess bits, Z_plus, Z_minus.

#### MR13 - Bayes factor against a fair draw

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

#### MR14 - Fidelity (classical squared Bhattacharyya affinity)

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

#### MR15 - Spectral periodicity of match counts (Lomb-Scargle)

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

#### MR16 - Hit-rate estimate with exact interval

- **One line:** how often this track achieved a given kind of success, how uncertain that rate is, and what observed rate would be needed to reach 3 sigma.
- **Short explanation:** a success here is a yes/no event per draw, such as any prize division, a particular division, at least 2, 3 or 4 main matches, or a Powerball hit. MR16 shows the track's observed rate with an exact 95% interval and the fair-draw rate beside it. It also shows the observed rate needed to reach 3 sigma locally over this window, and the chance of reaching it if the method were truly 1.5x or 2x better. With a few hundred draws the intervals are wide, and seeing that plainly prevents striking-looking counts being over-read. It vetoes nothing.
- **Sub-measures:**
  - `MR16.ANYDIV`;
  - `MR16.PDd` / `MR16.ODd`, every division;
  - `MR16.M2`, `MR16.M3`, `MR16.M4` (at least 2, 3, 4 main matches);
  - `MR16.PB` (Powerball only).
- **Definition** (per sub-measure, per `READOUT_TRACK`, on C):
  - k = the draws with the success event; observed rate k/n; fair rate p (exact, from 17.4).
  - **Interval:** the Clopper-Pearson 95% interval, a conventional **constant-rate reference interval**. It has guaranteed coverage only for independent trials with one common rate. No coverage is claimed for varying, selected or adaptive success rates. It is always shown, labelled.
  - **Local significance:** P_up = P(X >= k), X ~ Binomial(n, p), giving `EXACT_LOCAL`. This is the same tail as MR4 for division events, and it is not counted twice in M.
  - **Observed hit-rate threshold for local 3 sigma:**
    - k_3 = the smallest k with P(X >= k) <= 0.00134990 (3 sigma);
    - the threshold ratio is k_3 / (n x p). This is the observed rate a result must reach to be 3 sigma locally, **not** the smallest true advantage the sample can detect, which depends on the chosen power.
    - the power at 1.5x and 2x is P(X >= k_3) for X ~ Binomial(n, min(1, c x p)), with c = 1.5 and 2.
- **Reference values** for the default windows (computed exactly):

| Event | n | Expected by chance | k_3 (threshold ratio) | Power at 1.5x / 2x |
|---|---|---|---|---|
| Powerball, any division | 291 | 6.6 | 16 (2.42x) | 0.04 / 0.25 |
| Powerball, 3+ main | 291 | 36.3 | 55 (1.51x) | 0.49 / 0.99 |
| Powerball hit | 291 | 14.6 | 28 (1.92x) | 0.11 / 0.61 |
| Oz Lotto, any division | 220 | 4.4 | 13 (2.97x) | 0.02 / 0.10 |
| Oz Lotto, 3+ main | 220 | 12.5 | 25 (2.01x) | 0.08 / 0.52 |

- **Ranking:** the lower interval bound descending (descriptive: the rate the data most surely supports); Z_plus (significance).
- **Edge cases:** k = 0 gives an interval lower bound of 0 and 0 excess sigma. n = 0 gives `MR_INSUFFICIENT_DATA`.
- **Outputs:** k, n, the rate, the interval, p, n x p, P_up, Z_plus, k_3, the threshold ratio, the two power values.

### 17.7 In-sample diagnostic mode (IS)

The in-sample diagnostic mode (proposal 7.1-7.4: purpose, procedure, capability, firewall and labelling) is an execution contract and lives in R2 section 8.4 (8.4.1-8.4.4). Its side-by-side display (proposal 7.5) is a reporting rule and stays here as 17.7.5.

**17.7.5 Side-by-side display (MRD-23).** For every measure and sub-measure applicable in both modes, the report includes a side-by-side table.
- **Paired target set:** the values in this table are recomputed on the **paired set**, the targets scored in both modes for that unit. The table records n_WF, n_IS, n_paired and the paired-set digest.
- **Ranks:** the rank columns show each mode's rank **from its own league table**, labelled "rank in WF table" and "rank in IS table". They are never recomputed on the paired set, and never subtracted.

| Columns | Content |
|---|---|
| Unit | method / variant / readout, or the measure's analysis unit (17.3.4A) |
| Walk-forward (earlier draws only) | the WF value and its WF rank (among WF units only) |
| In-sample (hindsight: all draws) | the IS value and its IS rank (among IS units only), labelled `IS_NOT_CALIBRATED` where it is a significance figure |
| In-sample minus walk-forward (hindsight advantage) | IS minus WF; descriptive |

- Rows are sorted by WF rank by default; sorting by IS rank is a report option.
- A unit without IS capability shows "IS not applicable" in its IS cells and stays in the table by its WF values.
- Ranks are computed separately per mode, so an IS value never displaces a WF rank, or the reverse.
- The difference is an overfitting gauge, never an unbiased estimate of out-of-sample performance.
- **Comparable quantity per measure:** the difference column uses only the quantity below, in its stated unit. It never subtracts ranks, p-values, sigmas, calibration labels or Bayes factors.

| Measure | Comparable quantity (IS minus WF) | Unit |
|---|---|---|
| MR0 | the count difference per division (a vector) | wins |
| MR1 / MR1-T | MR1; MR1-T | bits per draw; weighted wins per draw |
| MR2 | G_d, where defined in both modes; otherwise `NOT_COMPARABLE` | scored opportunities |
| MR3 | `NOT_COMPARABLE` (values shown) | |
| MR4 | k_S | wins |
| MR5 | the mean mid-rank (negative = IS ranked drawn numbers higher) | rank positions |
| MR6 | G, over targets valid in both modes | bits per draw |
| MR7 | the mean main matches per draw | matches |
| MR8 | R | draws |
| MR9 | Delta | matches per draw |
| MR10 / MR10.BOTTOM | the mean gain | discounted gain |
| MR11 | the mean D | matches |
| MR12 | the excess bits per draw | bits |
| MR13 | `NOT_COMPARABLE` (values shown) | |
| MR14 | the mean F | affinity |
| MR15 | P_max | normalised power |
| MR16 | the observed rate | proportion |
- It is reported for every applicable measure. Hindsight inflation varies by method (the E_1 illustration in 17.18.3 showed about 3 sigma), so the difference column is the meaningful reading.

### 17.8 Supplementary-number rule (MRD-03)

The evaluator-only supplementary-number rule (proposal section 8; MRD-03) lives in R2 section 2.5. Oz Lotto division classification (17.4.1, 17.4.3) reads a target draw's supplementaries only under that rule.

### 17.9 Use of rankings (MRD-05; rules decided by Claude)

- **RK-1:** rankings are **reports**. They never alter any frozen forecast, fit, configuration, variant roster, readout or FINAL batch.
- **RK-2:** rankings are not scientific results, never go on the result-consumer allowlist, and are never read by a method.
- **RK-3:** any rule using rankings to **choose, weight or switch** methods is a **meta-method**. It must:
  - be registered (an E_55/E_56 variant if it fits, otherwise E_63+ by owner decision);
  - obey strict N-1, using only WF scores of targets < N known before N's freeze;
  - use **WF only, never IS**;
  - predeclare its measure, window, tie rule and minimum history;
  - be scored and ranked like any method.
- **RK-4:** any report highlighting a top-ranked track shows the number of tracks and tests compared and the global figures (17.5.3), plus the search-log count.
- **RK-5:** the owner studying development rankings and then changing a method is permitted design influence on development data. Each change creates a new versioned variant and is recorded in the method change log. Development rankings never extend into quarantined draws.
- **RK-6:** rankings over FINAL_HOLDOUT_10 are produced only after Mode H scoring of those targets.

### 17.10 Reporting (MRD-09)

**17.10.1 Files** (create-only, `os.rename` on Windows; in `results/method_rankings/<GAME>/`):
- `ranking_<GAME>_<MODE>_<S>-<L>_<UTCSTAMP>.txt`: human-readable and complete;
- `.csv`: one row per (analysis_unit, unit_id, sub-measure), keyed as in 17.3.4A;
- `.json`: the run manifest and reproducibility receipt.

`<GAME>` is `POWERBALL` or `OZLOTTO`; `<MODE>` is `WF` or `IS`; `<UTCSTAMP>` is `YYYYMMDDTHHMMSSZ`. Example: `ranking_POWERBALL_WF_1286-1576_20261026T040000Z.txt`.

**17.10.2 Text report layout:**
1. **Header:**
   - game; mode, by display name with its plain meaning from 17.3.5A (plus the IS banner); evidence tier; window;
   - the cohort and its digest, or `EXPLORATORY_COHORT`, and the family IDs;
   - comparison-set size n, and track counts by status;
   - master version and SHA; tool version and SHA; the N1 seed and R; the environment;
   - the search-log row number.
2. **Glossary:** first, the plain meanings of the two modes, word for word from 17.3.5A; then every measure, sub-measure, status, label, mode and tier used, each with ID, name, one-liner and short explanation; then the four pattern origins PO-1..PO-4.
3. **Fair-draw reference:** the division tables, expected counts for this n, the sigma table and caution, and the calibration-label legend.
4. **League tables:** descriptive and significance tables per measure and sub-measure, per mode; plus the **side-by-side WF/IS tables** (17.7.5). Each row gives rank, track ID, **method ID, name and one-liner**, readout, variant, n, all outputs, and calibration labels.
5. **Per-track detail.**
6. **Notes:** M per family; Bonferroni and N1 resolution; `LOW_N`; undefined values; ties; exclusions by status.

**17.10.3 Methods in reports** carry their E-number, name and one-liner in tables, and their short explanation in the glossary. The method registry therefore holds these texts (R2 sections 5.6 and 6.2).

**17.10.4 Ties:** standard competition ranking ("1=, 1=, 3"), listed by track ID within a tie. Exact quantities are compared exactly; floats at full float64 equality. `TIE_SHA256_V1` is not used.

**17.10.5 Number display:**
- counts as integers;
- probabilities to 6 significant digits in scientific notation;
- confidence rounded down, never "100%";
- sigma to 2 decimals;
- bits to 3 decimals;
- log10 Bayes factors to 3 decimals.

### 17.11 Numerics and precision

- `int64` throughout, with Python `int` for combinatorial counts; `float64` for floats. No narrowing.
- Division probabilities are exact `Fraction`s.
- **Tails in production:** log-space summation of exact log-pmf terms (via lgamma), summing whichever side is shorter, with the sigma conversion taken from log-survival or the inverse survival function. Never compute Phi_inv(1 - P) by forming 1 - P.
- **Exact oracle:** `Fraction` tails and integer polynomial coefficients (MR7) serve as the test oracle over the actual domain, including tails below 1e-300 (MRT-04).
- **Sigma accuracy:** within 1e-6 against the oracle where the oracle is computable, with documented asymptotics beyond that, labelled.
- MR13 quadrature is in log space, tested against closed-form cases.
- Timing is not committed until benchmarked on synthetic fixtures (ChatGPT O8).

### 17.12 Execution model (independent of production; MRD-13)

The report tool, the in-sample run mode, N1 as an evaluator component (Architecture section 12.5) and the wrapper `Run_Method_Rankings.bat` (Architecture section 5A.4) carry proposal section 12. The evaluator rules stay here:

- **Evaluator rules:** outcomes are read only for opened targets that have frozen forecasts; supplementaries only under R2 section 2.5.
- Dependency rules are unchanged: no upgrade between freeze and score, or within Mode H.

### 17.13 Phasing - when to code it

| Stage | When | What |
|---|---|---|
| 0 | Completed | The proposal was reviewed (v0.4 by ChatGPT; v0.5 applied its findings) and ratified by the owner on 26 October 2026; it is integrated into R3 v0.5, R2 v0.5, Architecture v0.8, Proposal v0.6 and register v0.4, owner-ratified 27 October 2026. No code. Package 2 v0.11 proceeded unchanged in parallel. |
| 1 | The **method-generic contract** package required before E_2 (Architecture 20A), after v0.11 is accepted. Proposed name: "E_2 readiness". **Not** in v0.11; P3 v0.2 is not edited. | The contract-field schema, ratified by the owner first (fields 1-7, R2 section 5.6). |
| 2 | With the R3 **scorer** and E_1's authorised development walk-forward | Match records; divisions (with R2 section 2.5); MR0, MR1/MR1-T, MR4, MR5, **MR7**, **MR16**; analysis units; the report format and glossary; sigma and labels; Bonferroni; families and the search log; **N1**. Tests MRT-01..10, 12..14, 16..19, 21..23. |
| 3 | After E_2-E_6 walk-forward results are scored | MR2, MR3, MR6, MR8, MR9, MR10/MR10.BOTTOM, MR11-MR15; IS mode; multi-method tables; the side-by-side WF/IS tables (17.7.5). Remaining tests. |
| 4 | Later | Any registered meta-method (RK-3), separately reviewed. |

The stage-1 contract fields (proposal section 13, fields 1-7) and the acceptance conditions before E_2 live in R2 section 5.6. Architecture section 20A points to them.

### 17.14 Tests

| ID | Test |
|---|---|
| MRT-01 | Division tables equal the exact fractions and integer counts in 17.4. Published rounded odds agree (Powerball rule 9.4; Lotterywest Oz odds, rounded up). |
| MRT-02 | Classification is exhaustive and exclusive over every (m, b) and valid (m, s). Invalid s > 7 - m is rejected. |
| MRT-03 | The sigma conversion reproduces 17.5's table to 1e-6. k = 0 gives 0 excess sigma. The deficit example (P_lo 0.0111058, 2.28673 sigma) is reproduced. Displayed confidence is never "100%". |
| MRT-04 | Production log-space tails agree with the exact `Fraction` oracle, including n up to 5000, p down to 1e-9, and tails below 1e-300. |
| MRT-05 | Isolation: no outcome read beyond L or before opening. Supplementaries are read only by the evaluator for scored targets. No method view contains supplementaries (static and runtime checks). |
| MRT-06 | IS firewall: refused by the scientific ledger and allowlist; the banner and `IS_NOT_CALIBRATED` present; no ranking mixes IS and WF units as competitors; side-by-side tables keep separate per-mode rank columns and do not change either mode's ranks; N1 refuses IS input. |
| MRT-07 | Planted, **measure-specific** synthetic effects are detected: a hit-rate tilt (MR4, MR7, MR11, MR12, MR13), a cycle (MR15), a streak (MR8), drift (MR9), probability vectors (MR6, MR14), top or bottom placement (MR10, MR10.BOTTOM). Null synthetic tracks give near-nominal rejection rates. Synthetic data stays firewalled. |
| MRT-08 | Determinism: identical inputs and seed give byte-identical CSV, and text identical apart from header timestamps. |
| MRT-09 | Tie display (17.10.4). |
| MRT-10 | MR5 per-target values equal R3's evaluator values. |
| MRT-11 | MR14's K-parameterised E_t and V_t agree with exhaustive enumeration on small domains ((N, K) = (10,3), (12,7), (9,4)) to 1e-12, with an independent analytic check, and with seeded simulation at (35,7) and (47,7). Uniform q gives `NULL_VARIANCE_ZERO`. The residual guard behaves as specified. |
| MRT-12 | All numeric fields are int64 or float64. |
| MRT-13 | Every printed ID has registry text, and the two mode definitions of 17.3.5A appear word for word in the glossary. No heading shows a bare `WF` or `IS`. The report fails otherwise. |
| MRT-14 | Window guard: S >= E(G); L within the cap; Oz S < 1474 rejected. |
| MRT-15 | (Stage 4) A meta-method uses only WF scores of targets < N. |
| MRT-16 | N1 classes. (d) An outcome-dependent stopping or availability synthetic (ChatGPT's 20-step 5% rule, 6467/65536) is labelled `SELECTION_UNVERIFIED`, never `N1_CALIBRATED` or guaranteed. (a) For the hit-sequence class, N1 matches the exact distributions of MR4, MR7, MR8 and MR11 within Monte Carlo error, **including for adaptive synthetic methods**. (b) ChatGPT's adaptive 4-draw counterexample is reproduced (true 1/16, replay 15/128), and the cross-track maximum is labelled `N1_FIXED_FORECAST_REFERENCE`, never `N1_CALIBRATED`. (c) A forecast-weighted adaptive toy confirms that weight- and probability-scored measures are labelled reference. Seed reproducibility. |
| MRT-17 | Families: registration precedes first use (checked against the search log); M is computed correctly; post-hoc families are labelled `POST_HOC_FAMILY`. |
| MRT-18 | The search log is append-only; every report run adds exactly one row. |
| MRT-19 | MR7's exact integer-coefficient oracle agrees with the production computation and with N1. |
| MRT-20 | MR8's dynamic programme agrees with brute-force enumeration on short gappy sequences. |
| MRT-21 | MR15: the frequency grid excludes Nyquist; the power normalisation matches its definition; the N1 FAP is computed on the actual draw grid. |
| MRT-25 | Side-by-side tables: the paired-set recomputation, the n_WF / n_IS / n_paired counts and digest, the comparable-quantity table, `NOT_COMPARABLE` where defined, and no subtraction of ranks, p-values, sigmas, labels or Bayes factors. |
| MRT-22 | MR16: the Clopper-Pearson intervals match an independent exact implementation. k_3 and the power values for the MR16 reference table (17.6) are reproduced. Division-event tails are not double-counted with MR4 in M. |
| MRT-23 | Analysis units: each measure is computed on its declared unit (17.3.4A). No method-level value appears as two readout tests. M counts distinct hypotheses once. |
| MRT-24 | MR6 zeros: an observed q_j = 0 gives `LOG_SCORE_NEG_INFINITY`, a tagged value and last place; an unobserved zero gives `MR_UNDEFINED_REFERENCE` for that target's significance only; the evaluator never smooths. |

### 17.15 Integration into the governing documents

Not carried. Proposal section 15 is carried out by this edition set (see the pointers at the start of section 17); the proposal file keeps it as history.

### 17.16 Open items

| ID | Item | Status |
|---|---|---|
| MRO-01 | Scope of the supplementary rule | RESOLVED: scoring and measuring only (MRD-03). |
| MRO-02 | Keep MR1-T | RESOLVED: keep (MRD-14). |
| MRO-03 | Reserved measures MR6-MR10 | RESOLVED: filled by ChatGPT's measures (MRD-16). Further measures take MR17 onward. |
| MRO-04 | MR13 prior scale | RESOLVED: 0.5, with 0.25 and 1.0 sensitivity (MRD-19). |
| MRO-05 | LOW_N threshold | RESOLVED: n < 30 (MRD-19). |
| MRO-06 | Identity for any future meta-method | OPEN; decided when one is proposed. |
| MRO-07 | Oz Lotto supplementary channel for MR6-MR15 | RESOLVED: main only (MRD-19). |
| MRO-08 | Multiplicity families | RESOLVED: predeclared families, Bonferroni, N1 maximum statistic, search log (MRD-18). |
| MRO-09 | Expected-payout measure (ChatGPT O1) | DEFERRED: only with legally sourced, versioned payout data. |
| MRO-10 | Full recursive (whole-pipeline) null simulator: refits methods inside each replicate, which would calibrate cross-track maxima and weight- or probability-scored measures for adaptive WF, and IS significance | DEFERRED: separate reviewed design if ever wanted; it requires running method code. |
| MRO-11 | Larger N1 R for higher-resolution global figures | OPEN: owner may raise R per table; cost to be benchmarked. |

### 17.17 Traceability to the owner's starter text

| Starter item | Where addressed |
|---|---|
| Draws 1 to P0 / O0; first draw in 2021 is P1 / O1 | 17.3.6 (S defaults: Powerball 1286; Oz Lotto 1474 under MRD-04; L at the cap) |
| Step 1, full training, bias acknowledged | R2 section 8.4 (IS) and 17.7.5, MRD-21 |
| Step 2 window with default parameters | 17.3.6; ascending draw-number order (MRD-12) |
| 2.1 fully trained prediction | R2 sections 8.4.2-8.4.3 |
| 2.2 methods where full training does not apply | R2 section 8.4.3 `IS_NOT_APPLICABLE`: WF tables only |
| 2.3 collect matches | 17.4.1 |
| Step 3, rankings per game | R3 sections 17.6 and 17.10 |
| Division rules, top-down | 17.4.2-17.4.3 (all divisions, MRD-02) |
| R0 | MR0 |
| R1 (90/7/3) | MR1-T; MR1 |
| R2-R4 | MR2 per division |
| R5-R7 | MR3 per division |
| R8-R10 | MR4.C.3, MR4.B.2-3, MR4.X.3 |
| Output file with numbers | 17.10 |
| Up to 5 further measures | MR11-MR15 (Claude); MR6-MR10 (ChatGPT) |
| Run independently of production | 17.12; Architecture section 12.5 |
| Architecture impact | 17.12, 17.13, 17.18; Architecture sections 5A.4 and 12.5; R2 section 5.6 |


### 17.18 Claude's analysis, implications and design matters (informative)

Informative notes carried from the proposal. They explain the measures and give fair-draw context; the rules are in 17.0-17.16.

**17.18.1 Feasibility.**
- WF ranking re-reads stored forecasts and outcomes and computes; no method runs.
- N1 adds R replicates of cheap scoring per calibrated table.
- IS adds one full fit plus applications per method.
- The expensive part, walk-forward forecasting, is already planned.
- No timing is committed until benchmarked.

**17.18.2 Why all divisions matter.** Expected division wins under a fair draw, per track and across 124 tracks (62 methods x TOP/WORST), for the default Phase 1 windows:

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

**17.18.3 In-sample results.**
- A static method's IS entry is chosen with the outcomes in view, so its matches are inflated by construction.
- IS measures descriptive fit. Its main use is the side-by-side IS/WF comparison and its "in-sample optimism" column (17.7.5). **Illustration only, not a test acceptance value:** a one-off fair-draw simulation by Claude (NumPy `default_rng` seed 20261026; 20,000 replicates; each replicate 433 fair Powerball draws; IS TOP = the 7 most frequent numbers over all 433, random tie-break; scored on the last 291; statistic as MR7, standardised Z = (S - 291 x 1.4)/(sqrt(291) x 0.960392)) found that E_1's in-sample TOP averaged about 13% more main matches than chance (1.588 against 1.400 per draw), with a mean Z of about 3.34 and Z >= 3 in about 67% of replicates, from fitting alone. Other methods can gain more or less, including none. Reading the optimism column:
  - large optimism with no WF advantage suggests fitting noise;
  - agreement suggests stability.
- The owner knowingly accepts this, and every number is shown, labelled.

**17.18.4 Multiple comparisons.**
- About 124 tracks and about 20 sub-measures make roughly 2,500 tests per family. Under a fair draw, about 3 local results at or above 3 sigma are expected by chance, and a local 5 sigma about 0.0007 times.
- Bonferroni over exact local p-values gives the guaranteed figure. This holds under adaptive walk-forward for the hit-sequence class, which includes the strongest every-draw measures (MR7, MR16, MR11).
- N1 is exact for single-track hit-sequence statistics. For cross-track maxima and probability- or weight-scored measures it is a labelled reference only, because replaying fixed adaptive forecasts breaks their dependence on earlier outcomes.
- The search log keeps honest count of all exploration.
- **Small samples:** MR16's threshold line shows, per event, the observed rate needed for local 3 sigma, with the power at 1.5x and 2x. Frequent events (3+ matches) need about a 1.5x observed rate; division counts need about 2.4-3x.

**17.18.5 "Due" measures and the ruler.** Under a fair draw, wins have no memory. MR3 is shown as a pattern indicator, never a veto. Its value as a choosing rule can be tested only as a registered meta-method (RK-3).

**17.18.6 Selecting the best performer.** The top of a league table is partly luck, so its next results usually regress towards the mean. That is why any "follow the leader" rule is scored prospectively as its own method, and why reports show global figures.

**17.18.7 Design implications (summary).**
1. Package 2 v0.11 and P3 v0.2: no change.
2. Method-generic contract before E_2: the stage-1 fields. This is the one design item that matters now.
3. Rule changes on ratification: the evaluator-only supplementary rule; the R3 ranking section; the IS product and firewall; the explanation-text rule; the numbering conventions; evidence tiers.
4. New components: the report tool and wrapper; the IS run mode; N1 (two classes); the measure and family registries; the search log; method registry texts; analysis-unit keys.
5. No impact on Architecture 5C, the switches, the holdout boundaries, the E_1 goldens or the master data.

**17.18.8 Holdout and Mode H.** Phase 1 windows and IS fits end at 1576 / 1693. Holdout targets enter rankings only after Mode H scoring (RK-6).

**17.18.9 Philosophy compliance.**
- No measure excludes, demotes or vetoes a method; every method stays registered and reported.
- Fair-draw figures are rulers beside every result.
- "Mark, never suppress" (MRD-21) means every number the owner wants is calculated and shown, with a plain label of how far it can be trusted.
- Statistics here sorts patterns into the four origins (PO-1..PO-4); it never decides which ideas may be explored. Being open to unconventional hypotheses and careful about numerical correctness are compatible, and this design needs both. If something unexpected does appear, the same rigour is what will let it stand.

## Appendix S — Superseded evaluation examples (historical only)

- Original Powerball holdout 1578–1587/development cap 1577 → fixed 1577–1586 and cap 1576 (R3 §6).
- Proposed Oz holdout selected as “ten highest in first accepted snapshot” → fixed 1694–1703 (R3 §6).
- Historical 7 August 2026 data-build cutoff → current 1 August 2026 quarantine boundary.
- Powerball-only score assumptions → game-qualified actual barrels (Oz PB channel ABSENT).

Original revision notes remain accessible in ratified v0.3 and are not separate operative instructions.
