# Predictive Randomness — R2 Experimental Method Specifications and Software Contracts

**Version:** 0.2 — revised design/ratification candidate (supersedes R2 v0.1 for review; not ratified)  
**Date:** 21 October 2026  
**Status:** **DRAFT FOR USER REVIEW; NOT YET RATIFIED; NO IMPLEMENTATION AUTHORISED BY THIS DOCUMENT ALONE**  
**Proposed repository path:** `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_2.md`  
**Governing charter:** `doc/Predictive_Randomness_Research_Project_Proposal_v0_3.md` (**user-ratified 21 October 2026**)  
**Governing research catalogue:** `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` (**user-ratified 21 October 2026**)  
**Primary platform:** Windows 11, Python 3.14.8, standard CPython, VS Code + Windows CMD, project-local `.venv`; AMD Ryzen 9 3900X, 12 physical cores/24 logical processors, 32 GB RAM  
**Current source snapshot:** 444 current-rule draws, **1144–1587**, 19 April 2018 through 15 October 2026; ordinary-set and operator-labelled drawn-order CSVs. **Current last validated draw** `L=1587`; **next genuine target** `L+1=1588`.

> **Purpose:** Translate the ratified charter and 62-candidate research catalogue into inspectable method identities, shared data and execution contracts, mathematical-specification worksheets, provenance rules, and implementation acceptance tests. This document explicitly **does not** select winning methods, implement the predictor, establish statistical success thresholds, or open the final holdout. Mathematical decisions still requiring user approval remain visibly open rather than being inserted silently.

> **Project philosophy (binding):** The purpose is to test whether perceived randomness conceals predictive structure—including unlikely, unknown, surprising, or heterodox relationships. Conventional independence and chance models are **reference instruments, never vetoes** on which hypotheses may be researched. Every method remains permanently registered and eligible for future combinations, even if weak, correlated, expensive, unstable, or unorthodox. Sound mathematical bookkeeping and honest prospective testing make unconventional hypotheses more testable; they are not permission to remove them.

---

## Revision record — v0.2 changes relative to v0.1

This revision is a **controlled update**, not a replacement for the ratified Proposal v0.3 or R1 v0.4. The content, permanent names and identities of all **62 experimental candidates (E_1–E_62)** are retained. The following decisions/clarifications were made by the user after receiving v0.1; other proposed engineering choices remain proposals:

1. **Draw number is the controlling chronological index** for all ordinary Powerball forecasting and evaluation; exact clock timestamps are not required as mathematical inputs to those methods. Dates remain available as source metadata.
2. **Historical evaluation:** predict a known draw `N` using only eligible draws earlier than `N`, normally `1144 .. N-1`, then independently compare the saved forecast with actual draw `N`. The ten-draw holdout applies to development, historical evaluation and comparison.
3. **FINAL genuine next-draw forecast:** derive the last validated draw `L` from the refreshed actual source, fit using **every available current-rule draw `1144 .. L`**, including the reserved ten when they have actually occurred, and forecast **`L+1`**. A method's explicitly ratified rolling-window model may focus on a shorter subset, but no current known draw is withheld by a holdout rule in FINAL mode.
4. **§2.3:** external phenomena and associated timing fields are optional additions, not a compulsory dependency of the draw-number engine. Retrospective association studies remain permitted when truthfully labelled as such; they are not mislabelled prospective forecasts.
5. **§12.2:** “shared data” means common **Python code and explicitly permitted in-memory source views**. It does not mean recycling the outputs or transitory working state of another run.
6. **Optional root `transitory_data/`:** only genuinely needed scratch files, isolated per run/method, excluded from Git; never automatically become new source observations or forecast inputs. Persistent restart checkpoints, if ever required, need an explicit approved design.
7. **Interpretation over time:** a seemingly surprising fit is not pre-emptively branded a coincidence, synthetic artefact or implementation error because an established theory expects no signal. Several **genuine frozen before-the-draw `L+1` forecasts**, assessed after their actual outcomes become known, are a particularly valuable form of evidence. Such a sequence can remain inconclusive; neither a few successes nor a few failures determines reality. An **independently demonstrated** implementation defect or source-data error can still be identified promptly without waiting weeks; mere suspicion remains a hypothesis to investigate.
8. **No scoring system has been approved here.** R3 still owns scoring, thresholds, interpretations, prospective-evidence standards and method comparison.

**Review discipline:** These changes are recorded as either subsequent user agreement or proposed implementation wording. The whole R2 v0.2 document remains a review draft until ratified. No source code, existing data, proposal or R1 file has been altered by drafting this revision.

---

## 0. Document controls, precedence, and change discipline

### 0.1 Source precedence

1. Explicit, user-ratified later decisions control over conflicting text in earlier documents.
2. Proposal v0.3 controls project policy and scientific philosophy.
3. R1 v0.4 controls the identities, exact names, original hypotheses, qualifications and source bibliography of E_1–E_62. It is **not** an automatic mandate to implement every optional mathematical variant exactly as an R1 suggestion.
4. **Only after ratification**, R2 controls detailed method input/output, registry and implementation contracts; R3 will govern scoring and evidence interpretation.
5. The source CSVs, scrapers and external pages supply observations and provenance, but do not independently amend policy.

The original proposal's header calls itself a review candidate and R1's historical header refers to proposal v0.2; **the user's subsequent explicit ratification** now governs their status. Do not revise those historical files silently. This R2 draft records the accepted current status.

### 0.2 Requirements vocabulary

- **AGREED:** an existing user-ratified decision; this draft must preserve it.
- **PROPOSED:** a practical design solution put forward for explicit approval here.
- **OPEN:** a method-specific or cross-cutting choice not yet decided.
- **DEFERRED TO R3:** a statistical scoring, significance or selection matter that R2 must leave configurable.
- **NOT DONE:** no forecasting method, simulation batch or final-holdout run is asserted to exist because the idea is written here.

Identifiers `R2-Cxx` designate **proposed contract requirements**, not extra experimental methods. The `E_x` labels remain permanent scientific-method identities.

### 0.3 Change and review requirements [PROPOSED]

- Never edit a ratified file in place: issue v0.2, v0.3, etc. with a meaningful change log.
- A substantive algorithm, data-source policy, fitted objective, conditioning rule or selection-rule change creates a new **version of the method specification** and, when it changes the scientific hypothesis, a **new E-number** by user decision. Do not renumber older E-methods.
- Preserve inactive/blocked/error methods and variants in the registry, not delete them.
- Record both proposed design decisions and what the user has actually ratified. An omission or a default in software is **not** a decision.

### 0.4 R2 v0.2 scope

This revised candidate specifies a common architectural contract and provides **one independent method worksheet/profile per E_1–E_62**. Some highly specialised methods remain mathematical **specification candidates**, not fully frozen numerical algorithms. R2 is allowed to progress iteratively: the stable interface, data safety and method registry can be ratified separately from expensive method-specific formula choices. Incomplete mathematics is reported as `FORMULA_OPEN`, not filled in with unrelated standard models.

---

## 1. Agreed scientific and operational invariants

**I-01 — Eligible game era:** Every actual historical training or holdout observation must use exactly **7 distinct main numbers chosen from 1–35, plus 1 Powerball from 1–20**. Eligible start is **Draw 1144 on 19 April 2018**. Historical data from any differing barrel configuration are **excluded for every experiment, including Powerball-only variants**. A separate externally sourced feature series may be permitted without importing older lottery draw records.

**I-02 — Two distinct prediction targets:** Every applicable method returns an assessment of the **seven-main-number set** and the **single Powerball number** separately. A declared experimental hypothesis may use historical interactions between the barrels as *inputs*; it may not use the actual unknown next-draw result from one barrel to predict the other.

**I-03 — Reality hypothesis remains open:** A method is not barred because independent-draw mathematics predicts it cannot help. A surprising retrospective match alone is not sufficient evidence of a new physical or probabilistic mechanism; nor is it automatically declared mere coincidence. Explanations are investigated, not assumed, and repeatedly frozen prospective forecasts can add relevant real-world evidence.

**I-04 — All methods retained:** Every E-method and documented variant survives poor results, correlation, numerical expense, synthetic failure, or failure to fit. Inclusion in an ensemble is never forbidden merely by poor stand-alone ranking.

**I-05 — Draw-number temporal availability:** For historical prediction of draw `N`, no result from draw `N` or a later draw may enter fitting, model choice or the forecast. For a FINAL future target `L+1`, all actually completed eligible results through `L` are permitted. Optional external covariates must obey their own declared before-forecast availability rule when used for an honest historical or genuine future forecast. Neither a timestamp nor an external dataset is required for ordinary draw-history-only modelling. Computational warm starts may only carry valid states from earlier forecast origins.

**I-06 — Final historical holdout (historical evaluation and comparison only):** At current source snapshot `L = 1587`, the ten reserved historical draws are **1578–1587**. Development comparisons and performance benchmarks must not inspect their outcomes as fitting, ranking, hyperparameter, ensemble-selection or design evidence. Holdout membership is frozen and not silently redefined as new weekly observations arrive. The holdout is **not a restriction** on training a genuine FINAL forecast of a future `L+1`.

**I-07 — FINAL next-draw prediction:** Derive `L = max(validated draw_number)` from the current actual-data snapshot. Use all eligible actual history `1144..L` (including previously reserved historical holdout rows) as available training information and forecast target `L+1`. Never artificially reduce the permitted training prefix to `L-10` for a FINAL run. Respect any independently specified rolling-window formula, but make the full real prefix available. Freeze the forecast **before the real target draw occurs**; after the result becomes available, compare it in a separate prospective evaluator. Any previous holdout use is disclosed; the same data cannot simultaneously be claimed pristine for a method whose design saw its outcomes.

**I-08 — Synthetic separation with useful feedback:** Synthetic null-world, planted-effect, identifiability and other artificial research is executed, stored and reported separately. It **may** inform disclosed model design, debugging, sensitivity, feasibility, computational priority and interpretation. It must never insert synthetic draws, synthetic fitted hidden states or simulation outcomes into real-history fitting, real forecast outputs or real evidence scores. Synthetic failure cannot disqualify a method or forbid real-data testing.

**I-09 — Draw order:** The separate Lotterywest-derived sequence is **operator-labelled drawn order**, supported by The Lott's explicit Drawn/Numerical presentation and the 2021 Draw 1297 operator result document. It is *not* an independent second sample of 444 draws, nor is all 444-row physical-video verification claimed. Ordered and unordered views must be handled under **one cross-method policy** (Section 4).

**I-10 — Scoring deferred:** R2 defines what a forecast contains and how it is frozen. R3 will define statistical performance measures, significance/uncertainty, comparison, combination ranking and qualification. No R2 benchmark evaluates predictive merit.

**I-11 — Compute availability:** Default architecture is **one worker process per method**, configurable **1–12** processes initially, single-thread numerical libraries within a worker. Optional 24-worker SMT performance trials are non-default. Speed and failures do not control scientific eligibility.

**I-12 — Same-input determinism:** On the same host and pinned software/numerics configuration, **1-worker and 12-worker predictions must be bit-identical by default**; exceptions require a specific documented technical reason and explicit user approval, not an automatic tolerance waiver.
**I-13 — Interpretation must remain empirically open:** A surprising retrospective result or real-world forecast is not automatically dismissed as a coincidence, synthetic artefact or implementation error merely because it conflicts with a conventional reference model. Interpretations remain **provisional** until sufficiently investigated, including repeated properly frozen genuine future predictions as appropriate. Conversely, repeated apparent wins are not automatic proof of a novel mechanism, and failures are not automatic proof of impossibility. Distinguish a **verified programming/data defect** (which can be established by direct inspection or independent reproduction) from an **unconfirmed explanation** for unusual prediction results. R3 will specify evidence standards; R2 shall not prelabel outcomes as invalid or confirmed discoveries.


---

## 2. Current data contract and admissibility

### 2.1 Accepted source file roles

| File (snapshot example) | Role | Interpretation |
|---|---|---|
| `source_data/australian_powerball_history_20261021.csv` | Primary historical observation | Draw ID, date, seven main numbers, Powerball; seven columns are an **unordered set**, often stored ascending; column positions are **not** extraction positions |
| `source_data/australian_powerball_draw_order_20261021.csv` | Same draws with further published information | Seven main numbers in **operator-labelled drawn order**; never count as additional independently sampled draws |
| `doc/SAL_Powerball-Game-Rules_March-2026.pdf` | Game-rule documentary evidence | Validate current game configuration and distinguish it from any earlier historical configuration |
| Future external and apparatus sources | Optional added observations, not now mandatory | Require provenance, time of availability, semantic definitions, units and missing-data rules |

**R2-C01 [PROPOSED]:** Load both CSVs into a single canonical `DrawRecord` keyed by `(draw_number, draw_date)`; preserve `unordered_main` and `drawn_order_main` as **two views of one event**. Keep immutable raw snapshots and their SHA-256 digests. Do not silently repair conflicting data.

### 2.2 Canonical draw representation [PROPOSED]

```text
DrawRecord:
    draw_number: int
    draw_date_local: ISO-8601 calendar date (Australian date)
    main_set: immutable sorted tuple of 7 unique integers in [1, 35]
    main_draw_order: immutable ordered tuple of same 7 integers, if source available
    powerball: integer in [1, 20]
    source_ids: one or more provenance references
    source_snapshot_sha256: content digests
    validation_status: validated / quarantined / unavailable
```

**R2-C02:** Reject or quarantine any record with duplicate numbers, invalid ranges, date/number contradiction, duplicate draw keys, mismatched seven-set views, or inconsistent Powerball. A fixture may contain intentionally invalid records for tests, but not in the actual `REAL` dataset stream.

**R2-C03:** For the frozen October 2026 snapshot, assert **exactly 444** continuous draws **1144–1587**, Thursdays with seven-day spacing, with matching main sets and Powerball across both CSVs. For each subsequent actual-data snapshot, derive `L` from the validated **maximum actual draw number** and verify consecutiveness through `L`; derive the next live target as `L+1`. Never hard-code `1587` or manually advance `L` in source-independent code. The eligible start **1144** remains fixed.

**R2-C04:** An optional order sequence must consist of exactly the same seven numbers as `main_set`, once each. A missing or unverifiable order view may block an **ordered** variant, but it must not block compatible unordered methods or remove them from the registry.

### 2.3 Primary draw-number control; optional external data [AGREED/PROPOSED]

**The core forecast engine is indexed by actual draw number, not clock time.** Each historical evaluation target `N` gets only the valid draw rows `1144 .. N-1` (or an approved shorter history window); a FINAL prediction for next draw `L+1` gets all available valid rows `1144 .. L` (subject only to that method's mathematical window definition). The existing `Date` field is retained as metadata for checking weekly continuity, displaying results, and supporting future date-related hypotheses. **No exact timestamps are required for ordinary draw-result prediction, benchmark fitting or historical-score matching.**

**External observations are entirely optional.** If a later E-method proposes weather, apparatus changes, astronomical phases, external signals or other phenomena, R2/R3 must separately define its temporal indexing and admissibility. Some may be unambiguously linked by **draw number or calendar date**, needing no exact clock time. Where publication/release time matters to prove a feature was actually knowable before a historical or genuine future forecast, record the available publication date/time to the **precision necessary for that hypothesis**; do not invent missing times. A same-day value released only after a draw is not allowed to masquerade as a pre-draw predictor merely because its observation date matches. If only retrospective alignment is supported, it may still be studied in a **separately labelled retrospective-association mode**, explicitly not assessed as an advance prediction. This preserves unconventional investigations rather than excluding them.

**R2-C05:** The runner constructs an immutable **draw-number-limited** source view: for historical target `N`, rows `< N` only, and for FINAL genuine future target `L+1`, all validated actual rows `<= L`. Methods cannot access the target's unknown actual result, global post-target observations, scoring tables or other time-leaked derived information. For the **development** namespace, the frozen holdout outcomes additionally remain inaccessible. For an **authorised FINAL** namespace, the holdout rows are accessible because they are completed past draws. The forecast method does not receive future outcomes through hidden metadata or helper functions.

**Separate proof-of-prior-forecast from model features.** A prospective forecast should be archived before the target is drawn, with immutable bytes, a digest and some verifiable creation/commit evidence. Such an audit record may contain a wall-clock timestamp or Git commit metadata; that timestamp **is not a required predictive input** and does not alter the draw-number forecasting logic.

### 2.4 Separate dataset namespaces and provenance [PROPOSED]

Every run has one explicit namespace: `REAL_DEVELOPMENT`, `REAL_HOLDOUT`, `REAL_PROSPECTIVE`, `SYNTHETIC_NULL`, `SYNTHETIC_PLANTED`, `SYNTHETIC_IDENTIFIABILITY`, or `BENCHMARK_REAL` / `BENCHMARK_SYNTHETIC`. Each stores results in a segregated directory and writes a namespace manifest. A benchmark run carrying real history is **not** a training-data augmentation and never scores or exposes benchmark predictions.

---

## 3. Historical cutoffs, training windows and holdout boundaries

### 3.1 N-1 principle [AGREED]

For a historical target draw `N`, a method may fit to eligible draws **1144 through N−1 inclusive**, or a declared most-recent subset ending at `N−1`. It must not inspect any result or derived value from `N` or later. This includes hindsight-fitted trends, smoothed series using future boundary points, fitted transforms, extracted optional covariates, precomputed full-history similarities, model-selection heuristics and state initialisers. **The evaluator** may subsequently compare the frozen prediction for `N` with the known actual record for `N`, without returning that outcome to the predictor.

**R2-C06 [PROPOSED]:** The runner constructs a `ForecastRequest` containing an explicit target ID, last accessible draw, a frozen source digest, a named data-view policy, a training-window policy, reproducible seed identity, and an execution namespace. Method functions receive only this object plus their permitted training records.

### 3.2 Fixed present-day benchmark arithmetic

Current eligible source: 1144–1587, with reserved holdout 1578–1587. Development ends at **1577**.

| Mode | Prediction target(s) | Largest permitted training range | Size |
|---|---|---|---|
| B1 | 1577 | 1144–1576 | **433** preceding draws |
| B10 | 1568–1577 | For target 1568: 1144–1567; for target 1577: 1144–1576 | **424–433** preceding draws |
| B1, W=100 | 1577 | 1477–1576 | **100** draws |
| B10, W=100 | 1568–1577 | Rolling last 100, ending at N−1 | **100 per target** |
| Current final holdout (not for development) | 1578–1587 | Only the prior results permissible at each eventual final evaluation origin | Held unopened for development |

**R2-C07 [PROPOSED]:** Benchmarks use `X` consecutive target origins immediately before the frozen holdout, `X=1` or `X=10` presets, and training-history mode `W=100` or `W=ALL_PERMITTED`; additional values may be added with declared names. Do not confuse ten training observations with ten **prediction targets**.

### 3.3 Windows and warm starts [PROPOSED]

- `EXPANDING`: available history from the first eligible draw through N−1.
- `ROLLING_W`: most recent `W` eligible draws preceding N.
- Minimum viable sample size is a **method-specific, reported requirement**, not a reason to delete a method. If history is insufficient, status `INSUFFICIENT_HISTORY` is recorded without inventing a forecast.
- A warm start used for target N may come only from earlier legitimate target states, with code/config/data lineage recorded. Warm-start chaining prevents indiscriminate parallel execution of consecutive origins; alternate cold-start target blocks are separately declared computation variants.
- If a method refits only every `k` draws, this is an explicit, versioned policy. Never silently treat a stale fit as a new fit to N−1.

### 3.4 Holdout lifecycle [PROPOSED]

Freeze a named `HoldoutManifest` recording the ten draw IDs, input snapshot SHA-256, designation date and permitted uses. Pre-ratification development must not access its target outcomes. On the first authorised final evaluation, an audit trail records that the holdout was opened. Subsequent tuning against those results removes the *independent* designation for later tests. A genuine next-draw prediction may intentionally fit all observed draws; label that exception and preserve the forecast timestamp. Do not silently shift the holdout when another Thursday arrives.

### 3.5 Two operating modes and the continuing genuine-forecast cycle [AGREED; execution design PROPOSED]

**Mode A — Historical evaluation/comparison.** With known target `N`, supply the method only eligible draw numbers earlier than `N`; freeze a prediction; then let a separate evaluator compare it with the already-known result for `N`. The historical ten-draw holdout is not used for development/model selection or computational benchmarking. R3 governs scoring and subsequent release of final holdout results.

**Mode B — FINAL genuine real-world prediction.** At each genuine forecast time, refresh and validate the real input source, let `L` be its largest consecutive valid draw number, supply all eligible draws `1144..L`, and predict **`L+1`**. The final ten historical draws are **not withheld**. This is the default meaning of “all training data” for a FINAL run; particular methods can still apply their versioned rolling-window or other mathematical rules to this permitted data.

```text
Initial snapshot:         1144 ... 1587  (L=1587)
FINAL forecast:           fit using 1144 ... 1587 -> predict 1588
Once actual 1588 exists:  separately compare saved 1588 forecast with actual 1588
Updated snapshot:         1144 ... 1588  (L=1588)
Next FINAL forecast:      fit using 1144 ... 1588 -> predict 1589
... repeat for subsequent genuine weekly draws ...
```

A **prospective forecast** is archived/frozen *before its target is drawn*; its content and pre-draw provenance are immutable. The later result and any evaluation live in **separate records**. If an implementation, parameterisation or ensemble rule changes between weeks, retain the prior version and record the new version; do not rewrite the earlier forecasts to match the newly observed result. The collection of consecutive, genuine forecast/result pairs is crucial experimental evidence for R3. It should be possible to report periods in which no valid prediction could be produced rather than omit failures.

**Interpretive neutrality:** Do not predeclare a surprising match a coincidence or assume its cause is a synthetic artefact or bug without independent supporting evidence. An actual demonstrated code defect *can* be established and corrected without weeks of additional draws, with its affected forecasts flagged (never erased). Apparent genuine forecasting ability or its absence should be examined across multiple pre-draw forecast/result pairs, with uncertainty; **“several weeks” is an opportunity for evidence, not an automatic proof threshold**. Never infer a novel causal mechanism from an isolated score. R3 controls statistical conclusions and rules for how adaptive changes affect comparability.

**R2-C07A [PROPOSED]:** Explicitly implement and label `HISTORICAL_EVALUATION` and `FINAL_NEXT_DRAW` workflows (mapping to the established namespaces) with target IDs computed from draw numbers. A FINAL run's `training_last_draw_number` must equal `L`; a historical target's must be at most `N-1`. No code path may silently exclude the reserved ten from FINAL forecasts.


---

## 4. Single common ordered/unordered observation policy

**R2-C08 [PROPOSED]:** Define `observation_view` per method variant from `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, or `PAIRED_DIAGNOSTIC`. This is a shared policy for all E-methods, not 62 independent ad hoc definitions.

- `UNORDERED_SET`: the observation is exactly the seven-number set; sorting is only a storage convention. The likelihood or model ignores the originally reported extraction order.
- `OPERATOR_DRAWN_ORDER`: the observation is the ordered sequence of the seven numbers as published by the operator. Only methods with a valid ordered model may consume this view (for example sequential weighted selection).
- `PAIRED_DIAGNOSTIC`: a controlled comparison of two fitting/view configurations using the **same actual draws**, clearly labelled as paired views rather than independent draws. **No double-likelihood multiplication** for a set and its own order unless the joint factorisation is mathematically specified and does not count the same event twice.

**R2-C09 [PROPOSED]:** The view selected, source identity, ordered likelihood formula and tie or unavailable-order treatment are included in the model configuration and forecast manifest. Switching `UNORDERED_SET` to `OPERATOR_DRAWN_ORDER` does **not automatically** create another E-number; it creates a separately versioned, retained experimental **variant** unless its underlying scientific question changes and the user approves a new E-identity.

### 4.1 Ordered and unordered seven-number probabilities

For positive sequential selection weights `w_1 ... w_35`, the probability of a complete ordered selection `a_1, ..., a_7` with no repeated labels is:

```text
P(a_1,...,a_7 | w) = PRODUCT over r=1..7 of
                     w[a_r] / SUM_{j not previously selected} w[j]
```

The probability of the corresponding **unordered** seven-number set S is the sum of those ordered probabilities over all `7! = 5040` permutations of S, or a validated equivalent expression for the particular sequential-selection model. An unordered DPP likelihood **is not** the same model as this sequential weighting rule. Powerball uses a one-of-20 categorical distribution. The software should expose both views without assuming they are interchangeable or that an operator-labelled sequence is 444 independent additional observations.

### 4.2 Relative scores versus probability distributions

- Seven main-number **marginal inclusion probabilities** are in `[0,1]` and sum to 7 when derived from a coherent exactly-seven-set probability model.
- A Powerball categorical probability vector is nonnegative and sums to 1.
- A full unordered set distribution sums to 1 over all `C(35,7)` legal sets; an ordered sequence distribution sums to 1 over legal sequences.
- A raw score or relative propensity vector need **not** satisfy these probability identities, but may not be labelled “probability.”
- R3 decides whether/how to compare calibrated probabilities and rankings statistically. R2 requires **type honesty**, not a single compulsory scoring convention.

---

## 5. Forecast result schema and method adapter contract

### 5.1 Supported output types [PROPOSED]

A method may produce one or several typed channels, without inventing unsupported outputs:

1. `MAIN_RANK`: 35 labelled real-valued scores or a complete deterministic ranking.
2. `POWERBALL_RANK`: 20 scores or complete ranking.
3. `MAIN_MARGINAL_PROB`: 35 valid inclusion probabilities derived from or justified by a legal 7-set model.
4. `POWERBALL_CATEGORICAL_PROB`: 20 probabilities summing to one.
5. `MAIN_SET_DISTRIBUTION`: lawful probabilities/scores over seven-number combinations, exact or computable via a declared score/probability API without enumerating all sets.
6. `MAIN_ORDER_DISTRIBUTION`: legal ordered-sequence likelihood/scores.
7. `DIAGNOSTIC_SIGNAL`: anomaly/regime/coupling or other intermediate feature that may require an explicitly defined **adapter** to produce a prediction; a valid output, not grounds to delete a method.
8. `ENSEMBLE_RESULT`: combination of already-frozen, time-legitimate source-method outputs under a versioned combination policy.

**R2-C10:** Do not fabricate a numerical probability merely to satisfy an interface. A diagnostic-only method may return `NOT_PREDICTIVE_YET` until a mapping from diagnostics to forecast is specified and validated; it remains registered.

### 5.2 Provisional `ForecastResult` conceptual fields

```text
ForecastResult:
    method_id, method_name, method_revision, variant_id
    run_namespace, observation_view, game_rule_id
    target_draw_number, target_date_if_known, training_last_draw_number
    history_window, source_snapshot_hashes, source_information_cutoff_if_applicable
    fitting_algorithm_id, hyperparameters, random_seed_identity
    outputs: typed channels (ranks / scores / probabilities / joint sets / diagnostic)
    top_main_set: exactly 7 unique eligible numbers, when supplied
    top_powerball: exactly 1 eligible number, when supplied
    selection_rule_id: top marginal / MAP-set / sampled / other declared mapping
    fit_provenance, warm_start_parent, source_method_dependencies
    status, warnings, numeric_validity, effective_sample_size_if_meaningful
    canonical_content_hash, archived_at_if_recorded  # audit metadata, not modelling input
```

**R2-C11 [PROPOSED]:** Top-seven by marginal ranking, maximum-probability whole-set, and sequentially generated legal sets are **different selection rules**. A set-valued method must not be forced to misrepresent its joint model as independent seven individual top picks. If it also emits per-number marginals, label those as additional channels. Each forecast must supply a plain-English interpretation of its output or explicitly say that it is uncalibrated.

**R2-C12 [PROPOSED]:** All numerical outputs must use a defined finite-number policy; NaN/Inf, integer range errors, malformed ordering, duplicate main numbers and mismatched probability normalisation produce a visible validation failure. Numeric failures never silently coerce to an apparently valid forecast.

### 5.3 Consistency and versioning [PROPOSED]

- `method_id` is a permanent stable `E_x` for a scientific hypothesis; `method_revision` changes when its specification or implementation changes.
- `variant_id` records alternative estimators, fits, kernels, conditioning policies, data views or legal selection models while retaining the E-number where the core scientific hypothesis is the same.
- `run_id` identifies one concrete execution; it includes a stable digest of method revision, input snapshots, cutoff, model configuration and randomness scheme.
- If a later combination experiment becomes a distinct scientific method, allocate **a new E-number** by the user-approved method registry procedure. Never re-use or re-number an old ID.
- Dependencies on earlier forecasts or ensembles are recorded as a **directed acyclic graph**; no current-target evaluation outcome feeds a prediction-time combination.

### 5.4 Ties and rankings [OPEN decision]

A consistent default could resolve equal scores by increasing ball number, with tie metadata recorded. Seeded random tie-breaking could be a declared variant. The project has **not** ratified one tie policy yet. It should be set once centrally for reproducibility before coding, not implicitly decided by unstable sort ordering.

---

## 6. Method interface, registry and independent testability

### 6.1 Proposed method lifecycle

```text
register -> validate input capabilities -> prepare/freeze training view
  -> fit_or_update(training <= N-1) -> forecast(target N)
  -> validate typed output -> canonicalize and archive prediction
  -> (separate evaluator, later R3, may reveal N's result)
```

The experiment itself **never** calls the evaluator for the result of its own target. Its model-fit and prediction path cannot access scoring records. The program may offer a high-level CLI wrapper later; this R2 document specifies interfaces, not a finished `.py` file.

### 6.2 Registry fields [PROPOSED]

Each E-method has `id`, exact `name`, `research_source=R1_v0_4`, `scientific_hypothesis`, `input_capability`, `output_capability`, `minimum_history_requirement`, `default_variant` (if ratified), `supported_variants`, `math_spec_status`, `implementation_status`, `dependency_status`, `regression_fixtures`, `numeric_validation`, `resource_profile`, and `reason_for_any_blocker`.

Suggested implementation status enumeration: `RESEARCH_CANDIDATE`, `FORMULA_OPEN`, `SPECIFIED`, `IMPLEMENTING`, `IMPLEMENTED`, `TESTED`, `RUNTIME_FAILURE`, `INSUFFICIENT_DATA`, `SUSPENDED_BY_USER` (never silently dropped). A method can retain its permanent identity regardless of status. "Suspended" is an explicit operational choice, **not deletion**.

### 6.3 Reusable services [PROPOSED]

- Typed/cutoff-limited CSV loader and external-feature provider.
- Lag/recurrence and occurrence indicator sequence generator (not globally precomputed using future rows).
- Legal unordered-set/ordered-sequence probability utilities.
- Stable seeded random-stream service and deterministic ranking/tie adapters.
- Optimisation and validation wrappers, with predictable timeouts/failure reporting.
- Immutable forecast archiving, logging, provenance hashing and manifest generation.
- Resource and timing instrumentation independent of prediction performance.
- Distinct synthetic-generating research utility with namespace-specific provenance.

### 6.4 Handling outputs other than full predictions [PROPOSED]

An information-theory diagnostic or chaos feature that has no direct seven-number ranking **remains a valid registered experimental method**. An explicit, versioned adapter may translate it to a legal forecast (for example, features to a separate fitted predictive head). The adapter must obey N−1 fitting and use no target outcomes; until specified, the status is `DIAGNOSTIC_ONLY`, not a forced random projection.

---

## 7. Method inventory — all 62 identities retained

**R2-C13 [PROPOSED]:** The registry must contain **every** E_1–E_62 identity from the ratified R1 catalogue at startup even if no forecasting code is present. Default registry status may be `FORMULA_OPEN` or `RESEARCH_CANDIDATE`. A running implementation is never presumed from its presence in this table. New ideas may extend through E_106 under the current research allowance, but no empty placeholders are required and identifiers are not assigned casually.

### 7.1 Exact names and source capabilities

| ID | Exact R1 concept name | R1 indicated inputs | Effort noted in R1 | Spec status in this R2 candidate |
|---|---|---|---|---|
| **E_1** | Historical Appearance Frequency | `U` | L | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_2** | Expected Recurrence-Interval Alignment | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_3** | Occurrence-Curve Endpoint Forecast | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_4** | Occurrence-Curve Gradient Forecast | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_5** | Shared Population/Draw Distribution Model | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_6** | Per-Number Fitted Distribution Models | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_7** | Bayesian Frequency Shrinkage | `U` | L | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_8** | Hierarchical Dirichlet–Multinomial Propensity | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_9** | Exponentially Decayed Occurrence Rates | `U` | L | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_10** | Multi-Horizon Frequency Contrasts | `U` | L | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_11** | Change-Point Segmented Propensities | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_12** | Hidden Markov Propensity Regimes | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_13** | Latent State-Space Drift | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_14** | Calendar-Phase Conditional Patterns | `U` | L | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_15** | Historical Epoch Hierarchies | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_16** | Biased Without-Replacement Urn Model | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_17** | Discrete Recurrence Hazard Curves | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_18** | Mixtures of Recurrence Modes | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_19** | Periodic Recurrence-Hazard Peaks | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_20** | Self-Exciting or Self-Inhibiting Occurrence | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_21** | Cross-Number Recurrence Synchrony | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_22** | Lagged Event-Trigger Matrices | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_23** | Pair Co-Occurrence Propensities | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_24** | Higher-Order Triplet Interactions | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_25** | Graph-Based Number Association | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_26** | Draw-Level Geometry and Summary States | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_27** | Nearest Neighbour of Historical Draw Sets | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_28** | Markov Transitions of Draw Summaries | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_29** | Physical Draw Position Preferences | `O` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_30** | Draw-Order Transition Signatures | `O` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_31** | Plackett–Luce Sequential Selection | `O` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_32** | Permutation/Ordinal Structure of Draw Order | `O` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_33** | Fourier and Harmonic Occurrence Forecasts | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_34** | Wavelet-Localized Cycles | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_35** | Singular Spectrum Analysis | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_36** | Gaussian-Process Next-Step Curves | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_37** | Spline and Local-Polynomial Extrapolation | `U` | L | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_38** | Empirical Mode Decomposition | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_39** | Detrended Fluctuation and Long-Memory Features | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_40** | Nonlinear Phase and Periodicity Maps | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_41** | Context-Tree and Compression Prediction | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_42** | Conditional Mutual Information Features | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_43** | Transfer-Entropy Directional Signals | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_44** | Recurrence-Plot Analogue Prediction | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_45** | Delay-Embedded Nearest-Analogue Forecast | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_46** | Local S-Map Nonlinear State Forecast | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_47** | Lyapunov-Style Instability Conditioning | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_48** | Cross-Mapping of Potentially Connected Processes | `U+X` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_49** | Regularized Logistic Event Forecasts | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_50** | Random-Forest Conditional Patterns | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_51** | Boosted-Tree Interaction Discovery | `U` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_52** | Reservoir Computing for Latent Dynamics | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_53** | Evolutionary Symbolic Regression | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_54** | External-Date Covariate Synchrony | `U+X` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_55** | Complementarity-Aware Multi-Method Combination | `R` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_56** | Adaptive Temporal Method Mixtures | `R` | M | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_57** | Fixed-Size Determinantal Seven-Set Model (C-PW1) | `U (main)` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_58** | Unconditioned Coupled Latent-Wave Field (C-PW2) | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_59** | Draw-Conditioned Coupled Latent-Wave Field (C-PW3) | `U` | H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_60** | Post-Change Non-Equilibrium Relaxation Analogue (C-PW4) | `U, optional X` | M/H | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_61** | Guided-Particle Circulation Model (C-PW5A) | `U, optional drawn-order O` | Very high | Proposed profile; formula/details still subject to R2 method-level approval |
| **E_62** | Guided-Particle Circulation with Reinjection (C-PW5B) | `U, optional drawn-order O` | Very high | Proposed profile; formula/details still subject to R2 method-level approval |
`U` = unordered draws; `O` = operator-labelled drawn order; `X` = optional external observations; `R` = prior method predictions/rankings. `U+X` is conditional on actual external observations and correct release-time provenance. **The input codes reproduce the R1 concept; they are not newly ratified declarations of algorithm availability.** Pilot-wave-inspired analogies are *models for testing*, not evidence of quantum effects in the draw machine.

### 7.2 Per-method specification profiles — interpretation

For each registered method below, the first phrase is its retained scientific purpose from R1. The second phrase lists the **initial operational contract or mathematical decision that must be frozen before coding**. The third lists **output type** and/or special constraint. These are implementation planning notes; they do **not** assert that an arbitrary estimator, package, fitting regime or hyperparameter value has been user-approved. All variants, including currently non-identifiable ones, remain eligible for research.

### 7.1 Original six user-designed methods (E_1–E_6)

**E_1 — Historical Appearance Frequency**  
- **Hypothesis retained:** Raw occurrence counts/rates for each eligible number.  
- **Implementation choice to settle:** Choose full/rolling history, smoothing, how ties resolve and whether rankings use counts or rates.  
- **Contract/output:** MAIN_RANK and POWERBALL_RANK.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_2 — Expected Recurrence-Interval Alignment**  
- **Hypothesis retained:** Projected recurrence interval at target N, not simply how overdue.  
- **Implementation choice to settle:** Define gap as next-draw projected interval; mean/median/mode/hazard/mixture are distinct named variants; handle never-seen values.  
- **Contract/output:** Two independent barrel rankings; retain estimator provenance.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_3 — Occurrence-Curve Endpoint Forecast**  
- **Hypothesis retained:** Fit occurrence indicator histories and extrapolate level to next draw.  
- **Implementation choice to settle:** Specify curve family, fitting window, regularisation/boundary extrapolation and binary-response interpretation.  
- **Contract/output:** Number rankings from next-point fitted value.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_4 — Occurrence-Curve Gradient Forecast**  
- **Hypothesis retained:** Fit occurrence history curves and extrapolate their gradient.  
- **Implementation choice to settle:** Specify derivative point, curve family, temporal units, scale and boundary handling.  
- **Contract/output:** Number rankings from extrapolated signed slope.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_5 — Shared Population/Draw Distribution Model**  
- **Hypothesis retained:** Learn shared population/draw propensity or distribution.  
- **Implementation choice to settle:** Choose a legally normalised seven-without-replacement model distinct from Powerball categorical model.  
- **Contract/output:** Set/marginal/rank output, chosen model declared.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_6 — Per-Number Fitted Distribution Models**  
- **Hypothesis retained:** Fit distribution/recurrence process separately for each label.  
- **Implementation choice to settle:** Specify target random variable, distribution family, sparse-data treatment and normalisation.  
- **Contract/output:** Rankings or probabilities only if justified.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.7 Frequency, Bayesian and regime (E_7–E_16)

**E_7 — Bayesian Frequency Shrinkage**  
- **Hypothesis retained:** Regularised Bayesian item-frequency estimates.  
- **Implementation choice to settle:** Set prior family/concentration and fitting window; avoid unapproved pooling with next draw.  
- **Contract/output:** Marginal scores/probabilities with declared 7-set reconciliation.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_8 — Hierarchical Dirichlet–Multinomial Propensity**  
- **Hypothesis retained:** Shared hierarchical propensity across labels and periods.  
- **Implementation choice to settle:** Define hierarchy, hyperprior, link to without-replacement likelihood, identifiability.  
- **Contract/output:** Main and Powerball outputs separately.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_9 — Exponentially Decayed Occurrence Rates**  
- **Hypothesis retained:** Recent appearance with exponential decay.  
- **Implementation choice to settle:** Freeze decay definition, time units and parameter policy at each origin.  
- **Contract/output:** Scores/ranks, not automatically probabilities.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_10 — Multi-Horizon Frequency Contrasts**  
- **Hypothesis retained:** Contrast multiple past windows/horizons.  
- **Implementation choice to settle:** Define all horizons, scale factors and combination formula before target.  
- **Contract/output:** Ranks/scores, stable feature extraction.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_11 — Change-Point Segmented Propensities**  
- **Hypothesis retained:** Regime-specific propensities after inferred change points.  
- **Implementation choice to settle:** Freeze change-detection algorithm and timeline admissibility; no future-inferred breaks.  
- **Contract/output:** Next-regime ranks/probabilities or explicit signal.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_12 — Hidden Markov Propensity Regimes**  
- **Hypothesis retained:** Latent switching regime model.  
- **Implementation choice to settle:** Define hidden states, transition law, observation likelihood and state estimation.  
- **Contract/output:** Filtered next-step propensities/diagnostics.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_13 — Latent State-Space Drift**  
- **Hypothesis retained:** Drifting latent state over time.  
- **Implementation choice to settle:** Define process/observation model, update schedule and legal set link.  
- **Contract/output:** Next-state forecasts and barrel outputs.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_14 — Calendar-Phase Conditional Patterns**  
- **Hypothesis retained:** Conditional signals based on calendar phase.  
- **Implementation choice to settle:** Choose eligible date-indexed phases, avoid hindsight date transforms.  
- **Contract/output:** Number ranks or conditional diagnostics.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_15 — Historical Epoch Hierarchies**  
- **Hypothesis retained:** Share information across declared historical epochs.  
- **Implementation choice to settle:** Define epoch boundaries as known at forecast time or inferred from preceding data.  
- **Contract/output:** Epoch-adjusted scores/ranks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_16 — Biased Without-Replacement Urn Model**  
- **Hypothesis retained:** Unequal item weights in without-replacement draws.  
- **Implementation choice to settle:** Choose sequential Wallenius-like versus other weighted-set law; do not equate to diagonal DPP.  
- **Contract/output:** Legal unordered set / optional ordered likelihood.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.17 Recurrence and event-process (E_17–E_22)

**E_17 — Discrete Recurrence Hazard Curves**  
- **Hypothesis retained:** Discrete hazard of appearance by absence age.  
- **Implementation choice to settle:** Define hazard regularisation, censoring, first-occurrence conventions.  
- **Contract/output:** Projected-age next-target inclusion scores.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_18 — Mixtures of Recurrence Modes**  
- **Hypothesis retained:** Multiple recurrence modes.  
- **Implementation choice to settle:** Specify mixture family, parameter constraints and sparse-number fitting.  
- **Contract/output:** Projected next-draw hazard ranks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_19 — Periodic Recurrence-Hazard Peaks**  
- **Hypothesis retained:** Periodically varying recurrence-hazard peaks.  
- **Implementation choice to settle:** Specify periods, phase, basis, search range and temporal fitting.  
- **Contract/output:** Projected next-draw inclusion scores.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_20 — Self-Exciting or Self-Inhibiting Occurrence**  
- **Hypothesis retained:** Self-excitation and inhibition after appearances.  
- **Implementation choice to settle:** Specify Hawkes-like or other discrete lag kernel and valid probability mapping.  
- **Contract/output:** Next-step ranks and lag diagnostics.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_21 — Cross-Number Recurrence Synchrony**  
- **Hypothesis retained:** Cross-number synchronised recurrence.  
- **Implementation choice to settle:** Define shared-lag/coherence features and information available at N−1.  
- **Contract/output:** Ranks or diagnostic-to-predictive adapter.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_22 — Lagged Event-Trigger Matrices**  
- **Hypothesis retained:** Lagged number-to-number triggers.  
- **Implementation choice to settle:** Define lag grid, direction, regularisation and prediction aggregation.  
- **Contract/output:** Separate barrel rankings; avoid same-draw target leaks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.23 Within-draw, set structure and drawn order (E_23–E_32)

**E_23 — Pair Co-Occurrence Propensities**  
- **Hypothesis retained:** Within-draw pair attraction/repulsion.  
- **Implementation choice to settle:** Define interactions and legal seven-set joint model or marginal adapter.  
- **Contract/output:** Whole-set scores plus optional marginals.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_24 — Higher-Order Triplet Interactions**  
- **Hypothesis retained:** Higher-order triplet associations.  
- **Implementation choice to settle:** Specify interaction representation, sparsity and computational budget.  
- **Contract/output:** Legal set scores or declared feature adapter.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_25 — Graph-Based Number Association**  
- **Hypothesis retained:** Number co-occurrence graph patterns.  
- **Implementation choice to settle:** Define graph construction using preceding draws, graph features and forecast mapping.  
- **Contract/output:** Diagnostic graph features / ranks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_26 — Draw-Level Geometry and Summary States**  
- **Hypothesis retained:** Geometry/summary of recent draw sets.  
- **Implementation choice to settle:** Specify legal features (sum, gaps, parity, spatial index) and mapping to numbers.  
- **Contract/output:** Diagnostic or forecast adapter; no information about target.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_27 — Nearest Neighbour of Historical Draw Sets**  
- **Hypothesis retained:** Closest historical draw analogues.  
- **Implementation choice to settle:** Define set distance and recency window, neighbour count and tie policy.  
- **Contract/output:** Next-step forecast from successors that are already known.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_28 — Markov Transitions of Draw Summaries**  
- **Hypothesis retained:** Markov patterns between draw-level summaries.  
- **Implementation choice to settle:** Define state discretisation/transition fitting and legal-set decoder.  
- **Contract/output:** State distribution + rank/set adapter.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_29 — Physical Draw Position Preferences**  
- **Hypothesis retained:** Differences by actual physical draw position.  
- **Implementation choice to settle:** Use `OPERATOR_DRAWN_ORDER` only; define position-wise features/model.  
- **Contract/output:** Position-aware predictions and ranks.  
- **Inputs:** `O`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_30 — Draw-Order Transition Signatures**  
- **Hypothesis retained:** Transitions between consecutive ordered draw sequences.  
- **Implementation choice to settle:** Define order features/lags and conditional forecast scheme.  
- **Contract/output:** Ordered or unordered forecast with explicit mapping.  
- **Inputs:** `O`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_31 — Plackett–Luce Sequential Selection**  
- **Hypothesis retained:** Sequential Plackett–Luce choices without replacement.  
- **Implementation choice to settle:** Specify 35 weights, likelihood, updates and separate Powerball model.  
- **Contract/output:** Valid ordered 7-tuple distribution plus set marginals.  
- **Inputs:** `O`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_32 — Permutation/Ordinal Structure of Draw Order**  
- **Hypothesis retained:** Permutation/ordinal pattern transitions.  
- **Implementation choice to settle:** Define pattern coding robust to different number identities and tie-free order.  
- **Contract/output:** Order-oriented diagnostic or forecast.  
- **Inputs:** `O`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.33 Spectral, curve fitting and long memory (E_33–E_40)

**E_33 — Fourier and Harmonic Occurrence Forecasts**  
- **Hypothesis retained:** Harmonic periodic occurrence components.  
- **Implementation choice to settle:** Define spectral estimation, phase extrapolation and selection of frequency bins.  
- **Contract/output:** Next-step level/score ranking.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_34 — Wavelet-Localized Cycles**  
- **Hypothesis retained:** Wavelet-scale localised periodic signals.  
- **Implementation choice to settle:** Choose wavelet family, boundary correction, prediction transform.  
- **Contract/output:** Ranks/diagnostic by scale.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_35 — Singular Spectrum Analysis**  
- **Hypothesis retained:** Singular-spectrum decomposition.  
- **Implementation choice to settle:** Choose embedding dimension, components and forecast recurrence rule.  
- **Contract/output:** Next-step scores/ranks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_36 — Gaussian-Process Next-Step Curves**  
- **Hypothesis retained:** Gaussian-process time-series patterns.  
- **Implementation choice to settle:** Choose kernel, time coordinates, likelihood and computational approximation.  
- **Contract/output:** Probabilities only if derived coherently.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_37 — Spline and Local-Polynomial Extrapolation**  
- **Hypothesis retained:** Splines and local polynomial extrapolation.  
- **Implementation choice to settle:** Choose spline order/window/penalty and endpoint derivative rules.  
- **Contract/output:** Forecast scores/ranks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_38 — Empirical Mode Decomposition**  
- **Hypothesis retained:** Empirical-mode decomposition signals.  
- **Implementation choice to settle:** Specify decomposition algorithm, mode forecast/extrapolation, endpoint treatment.  
- **Contract/output:** Scores/diagnostics with explicit boundary checks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_39 — Detrended Fluctuation and Long-Memory Features**  
- **Hypothesis retained:** Long-range fluctuation and memory conditioning.  
- **Implementation choice to settle:** Select detrending scales and feature-to-prediction adapter.  
- **Contract/output:** Diagnostic signal until adapter frozen.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_40 — Nonlinear Phase and Periodicity Maps**  
- **Hypothesis retained:** Phase-space maps and nonlinear periodicity.  
- **Implementation choice to settle:** Define state representation, phase features, evolution and mapping.  
- **Contract/output:** State/rank outputs; no gratuitous chaos claim.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.41 Information theory and nonlinear dynamics (E_41–E_48)

**E_41 — Context-Tree and Compression Prediction**  
- **Hypothesis retained:** Variable-order symbol/context predictors.  
- **Implementation choice to settle:** Define symbolisation, context tree, smoothing and legal draw decoding.  
- **Contract/output:** Forecast set/categorical distribution or ranked adapter.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_42 — Conditional Mutual Information Features**  
- **Hypothesis retained:** Information-theoretic conditional features.  
- **Implementation choice to settle:** Specify variables, conditioning set, estimator and predictive-head mapping.  
- **Contract/output:** Diagnostic only until forecast adapter defined.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_43 — Transfer-Entropy Directional Signals**  
- **Hypothesis retained:** Directional transfer entropy.  
- **Implementation choice to settle:** Define lag/history embedding, conditional estimator and model mapping.  
- **Contract/output:** Diagnostic-only or declared predictive adapter.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_44 — Recurrence-Plot Analogue Prediction**  
- **Hypothesis retained:** Recurrence-plot similarity in reconstructed state.  
- **Implementation choice to settle:** Define embedding, recurrence radius, feature aggregation, future forecast.  
- **Contract/output:** Next-step scores / recurrence indicators.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_45 — Delay-Embedded Nearest-Analogue Forecast**  
- **Hypothesis retained:** Nearest analogues in delay-embedded trajectories.  
- **Implementation choice to settle:** Specify lag dimension, metric and successor observations permitted.  
- **Contract/output:** Forecast state and legal-number adapter.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_46 — Local S-Map Nonlinear State Forecast**  
- **Hypothesis retained:** Local S-map state dynamics.  
- **Implementation choice to settle:** Choose embedding, localisation parameter, regularisation and decoder.  
- **Contract/output:** Predicted state/ranks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_47 — Lyapunov-Style Instability Conditioning**  
- **Hypothesis retained:** Instability/Lyapunov-style conditioning.  
- **Implementation choice to settle:** Define estimation and how instability drives a forecast.  
- **Contract/output:** Diagnostic or gated predictive head.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_48 — Cross-Mapping of Potentially Connected Processes**  
- **Hypothesis retained:** Cross-mapping with external/connected series.  
- **Implementation choice to settle:** External `X` must be time-available; define lag embedding, test and forecast use.  
- **Contract/output:** Conditional diagnostic/forecast without target-time hindsight.  
- **Inputs:** `U+X`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.49 Machine learning, external signals and ensembles (E_49–E_56)

**E_49 — Regularized Logistic Event Forecasts**  
- **Hypothesis retained:** Regularised Bernoulli/inclusion classifiers.  
- **Implementation choice to settle:** Define labels, lag features, imbalance and 7-set reconciliation.  
- **Contract/output:** Predictive scores/marginals with validity checks.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_50 — Random-Forest Conditional Patterns**  
- **Hypothesis retained:** Random forest conditional patterns.  
- **Implementation choice to settle:** Choose features, split policy, origin-specific fit and without-replacement adapter.  
- **Contract/output:** Number ranks and possible uncertainty.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_51 — Boosted-Tree Interaction Discovery**  
- **Hypothesis retained:** Gradient-boosted interaction models.  
- **Implementation choice to settle:** Define feature matrix, hyperparameters and legal selection adapter.  
- **Contract/output:** Scores/ranks; candidate dependency later.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_52 — Reservoir Computing for Latent Dynamics**  
- **Hypothesis retained:** Reservoir recurrent state model.  
- **Implementation choice to settle:** Specify reservoir weights, echo-state dynamics, training and legal output decoding.  
- **Contract/output:** Latent sequence forecasts and rankings.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_53 — Evolutionary Symbolic Regression**  
- **Hypothesis retained:** Evolutionary symbolic formula discovery.  
- **Implementation choice to settle:** Define grammar, variables, fitness training subperiod, search budget.  
- **Contract/output:** Frozen formula plus predictions; no hindsight target.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_54 — External-Date Covariate Synchrony**  
- **Hypothesis retained:** Date-aligned external environmental or other covariates.  
- **Implementation choice to settle:** Specify `X` series source/availability time, lag use and fitting.  
- **Contract/output:** External-conditional score/rank or diagnostic.  
- **Inputs:** `U+X`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_55 — Complementarity-Aware Multi-Method Combination**  
- **Hypothesis retained:** Combine methods by complementarity.  
- **Implementation choice to settle:** Only prior-time frozen constituent forecasts; define combination and weights in later R3.  
- **Contract/output:** ENSEMBLE_RESULT; new permanent E identity already present.  
- **Inputs:** `R`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_56 — Adaptive Temporal Method Mixtures**  
- **Hypothesis retained:** Time-varying selection/mixture of forecasting methods.  
- **Implementation choice to settle:** Define switching rule learned without target outcome; avoid holdout selection.  
- **Contract/output:** ENSEMBLE_RESULT with policy version, R3 selection.  
- **Inputs:** `R`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.57 Pilot-wave-inspired mathematical family (E_57–E_62)

**E_57 — Fixed-Size Determinantal Seven-Set Model (C-PW1)**  
- **Hypothesis retained:** Seven-set determinantal point process with fixed cardinality.  
- **Implementation choice to settle:** Specify symmetric PSD 35x35 L, seven-set partition Z_7(L); uniform L=I; fit regularised restricted L.  
- **Contract/output:** MAIN_SET_DISTRIBUTION and optional main marginals; Powerball separately modelled.  
- **Inputs:** `U (main)`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_58 — Unconditioned Coupled Latent-Wave Field (C-PW2)**  
- **Hypothesis retained:** Unconditioned complex latent-wave field.  
- **Implementation choice to settle:** Specify norm-preserving U, restricted degrees, historical fit and lawful 7-of-35 selection adapter.  
- **Contract/output:** Rank/set and Powerball outputs; no observation-conditioned state correction.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_59 — Draw-Conditioned Coupled Latent-Wave Field (C-PW3)**  
- **Hypothesis retained:** Conditioned complex latent-wave field.  
- **Implementation choice to settle:** Specify preceding-draw state update, norm preservation, same legal observation model as E_58.  
- **Contract/output:** Forecast after state update using at most N-1.  
- **Inputs:** `U`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_60 — Post-Change Non-Equilibrium Relaxation Analogue (C-PW4)**  
- **Hypothesis retained:** Transient post-change relaxation model.  
- **Implementation choice to settle:** Specify eligible known/inferred change dates, decay law, base propensity and legal seven-set model.  
- **Contract/output:** Next-step transient score/propensities; apparatus optional.  
- **Inputs:** `U, optional X`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_61 — Guided-Particle Circulation Model (C-PW5A)**  
- **Hypothesis retained:** Deterministic hidden ring particles with shared wave guidance.  
- **Implementation choice to settle:** Reference K small, beta=2alpha, epsilon=0, node-free, no independent noise; explicit weighted selection.  
- **Contract/output:** Legal ordered or unordered likelihood; hidden order diagnostic not gate.  
- **Inputs:** `U, optional drawn-order O`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

**E_62 — Guided-Particle Circulation with Reinjection (C-PW5B)**  
- **Hypothesis retained:** Guided ring particles with outcome-dependent reinjection.  
- **Implementation choice to settle:** Specify reinsertion/reinitialisation map and time-order of post-draw state changes; preserve E_61 reference distinctions.  
- **Contract/output:** Legal set/ordered forecasts; feedback affects only future draws.  
- **Inputs:** `U, optional drawn-order O`. **Status:** candidate; all unratified numerical sub-variants remain documented rather than silently accepted or rejected.

### 7.9 Method-family invariants and additional E_57–E_62 details

**R2-C14 [PROPOSED]:** Where a method supports both barrels, it shall operate on two separately labelled target domains, even if the fit can share research code. A method designed only for main seven-sets (especially E_57) must not pretend to provide a full independent Powerball model; it can expose a main-only output and, if required, a separately identified one-ball companion/combination method.

**DPP distinction for E_57:** A fixed-size determinantal point process has `P(S) = det(L[S,S])/Z_7(L)` with **symmetric positive-semidefinite L**, and uniform legal sets when `L=I`. A diagonal L yields a fixed-size product-weight subset law, **not** the same distribution as sequential weighted Wallenius draws. R2 must preserve this distinction in method metadata and tests. Off-diagonal DPP structure is diversity/repulsion, not arbitrary positive association.

**E_58/E_59:** For a norm-conserved 35-component complex state `psi`, the value `|psi_i|^2` is at most a categorical-style propensity; it does not by itself form an exact seven-number draw. Both must specify a **valid without-replacement selection mechanism**. E_58 evolves a previously fitted field without per-draw state correction; E_59 updates latent state after each *already observed* result and then advances. Neither's quantum inspiration is physical evidence.

**E_60:** Time-since-change models may use dated observed apparatus changes **if records exist**, or controlled change-point inference from history available at each origin. No apparatus metadata is mandatory. The beginning of the new rules is an eligible epoch boundary, but there are no preceding same-configuration outcomes before Draw 1144 to estimate a direct pre/post baseline there.

**E_61 reference mathematics (preserved from R1):**

```text
psi(theta,t) = SUM_{k=-K..K} c_k exp(i[k*theta - alpha*k^2*t])
SUM_{k=-K..K} |c_k|^2 = 1
|c_0| > SUM_{k != 0} |c_k|                 # sufficient node-free condition
beta = 2*alpha ; epsilon = 0
velocity(theta,t) = beta * Im(conj(psi)*dpsi/dtheta) / |psi|^2
w_j(t) = exp(kappa*cos(theta_j(t)-theta_capture))
```

Here `theta_capture = 0` can fix rotational gauge. Particle labels 1–35 (and separately 1–20) occupy positions on a ring, evolved by the common smooth field. At the main draw, seven distinct labels are selected sequentially without replacement using the positive weights. `kappa=0` nests the uniform legal outcome model. A nonzero Fourier truncation `K=1` does **not** force rigid rotation because it can include `-1,0,1` simultaneously; a single occupied mode gives constant velocity. A node-free exactly guided one-dimensional reference has order-preserving deterministic trajectories, **not a claim of chaos**. Standing-wave or frozen dynamics is a legitimate fitted outcome, not itself a predictive discovery. Allow non-node-free/epsilon-regularised, free-beta, independent-noise, shared-noise, 2D torus and other variants as separate precisely labelled future specifications. An unconstrained variant's numerical difficulty is no grounds for deletion.

**E_61 inference:** Fit unknown coefficients, positions, capture sharpness and dispersion **before** each target, using a declared method such as windowed multistart optimisation, MCMC or sequential Monte Carlo with rejuvenation. A naïve high-dimensional particle filter is not assumed to work. Synthetic identifiability studies can diagnose ordering recovery and own-model forecasting ability, but **never veto a real-history evaluation**. If synthetic self-recovery fails yet real outcomes appear predictive, report that the proposed particle explanation is unconfirmed even if forecasts perform well.

**E_62 feedback:** State a deterministic/stochastic reinjection rule for labels already drawn **only after their draw has occurred**. The rule can alter latent ordering and must not quietly inherit E_61's strict order-conservation claim. Reinjection may create genuine feedback dynamics unlike E_61's unconditioned reference. Forecasting still stops at N−1.

**R2-C15 [PROPOSED]:** No arbitrary `E_x` is automatically duplicated solely to switch between `UNORDERED_SET` and `OPERATOR_DRAWN_ORDER`. Maintain one project-wide observation policy, retain separately named variants and allocate a new E-number only where the scientific hypothesis itself materially changes and the user approves.

---

## 8. Real and synthetic execution pipelines

### 8.1 Mode and namespace separation [PROPOSED]

The runner will present clearly separated top-level modes; a mode flag must not silently switch after errors:

| Mode | Permitted inputs | Purpose | Can reveal target outcome to model? | Reports |
|---|---|---|---|---|
| `REAL_DEVELOPMENT` | Current-rule real development prefix | Fit and produce historical walk-forward predictions | **No** | Frozen predictions; scoring happens later via R3 evaluator |
| `REAL_HOLDOUT` | Frozen real holdout plan, only when authorised | One final evaluation of predeclared methods | **No before each prediction** | Separate holdout forecasts and eventual R3 evaluation |
| `REAL_PROSPECTIVE` / `FINAL_NEXT_DRAW` | All validated eligible real draws through current `L`, **without holdout exclusion** | Freeze prediction for `L+1` before that draw; repeat after each newly known actual draw | **No** | Immutable forecast plus separately appended comparison once actual `L+1` arrives |
| `SYNTHETIC_NULL` | Synthetic history generated under declared null | Calibrate research instrument | Synthetic outcomes only in synthetic workspace | Synthetic-only reports |
| `SYNTHETIC_PLANTED` | Synthetic model with planted structure | Sensitivity/fault injection | Synthetic only, under test plan | Synthetic-only reports |
| `SYNTHETIC_IDENTIFIABILITY` | Known-parameter synthetic model | Test recovery and own-model forecasting | Synthetic only | Synthetic-only diagnostic reports |
| `BENCHMARK_REAL` | Cutoff-limited real development history | Timing and resource measurement | **No** | Only timing, failures, resource figures, equality digests |
| `BENCHMARK_SYNTHETIC` | Labelled synthetic fixture | Timing-only smoke/throughput measurement | **No scoring** | Only timing and technical diagnostics |

**R2-C16 [PROPOSED]:** Synthetic calibrations may inform subsequent *disclosed* choices of numerical algorithm, model parameterisation, architecture and investigation priorities. They cannot inject synthetic data into the *actual fitted forecast state* or count artificial successes as real-world evidence. Synthetic diagnostics do not function as methodological vetoes or give a method preferential claims about reality.

**R2-C17 [PROPOSED]:** Code paths for real prediction do not import or read `results/synthetic/...`, synthetic fit checkpoints, planted truth values or synthetic evaluation scores. Shared general numerical utilities are permitted; shared trained states are not. A generated synthetic fixture must have a manifest that plainly says `SYNTHETIC` and cannot masquerade as the real source CSV.

### 8.2 Predict then evaluate, not the reverse

For a historical draw N, the runner first freezes and archives a valid prediction; only an independent evaluator authorised under R3 may load the actual draw N and calculate scores. The predictor interface must not accept a target-outcome argument. An evaluator's result is a separately versioned record that does not rewrite original prediction bytes. Early development can test mechanics on invented fixtures with known answers without counting this as actual research success.

### 8.2A Prospective evidence and unbiased interpretation [AGREED intention; R3 interpretation DEFERRED]

The project does **not** assume that statistically unusual outcomes are defective simply because conventional models consider them unlikely. Historical walk-forward scores may identify intriguing patterns, but the strongest practical test of prospective usefulness is the repeated **FINAL** sequence: store each `L+1` forecast before the draw; after publication, separately append its actual outcome and evaluation; refresh the source and forecast the next `L+1`. Preserve every attempted target, including abstentions, timeouts, failed fits, and poor predictions, so selection does not hide failures.

For reports, distinguish at least: **observed result**, **possible explanation under investigation**, **independently confirmed data/code fault**, and **provisional interpretation**. “Coincidental fit,” “synthetic artefact,” and “implementation error” are **hypotheses about a result until evidence establishes them**; they must not be imposed as unexplained labels. Clear-cut software defects or source contradictions remain actionable whenever verified, rather than deferred until a series of future draws has accumulated. Repeated prospective successes or failures update evidential confidence, but they do not, without sufficient analysis, conclusively prove a departure from randomness or disprove unconventional mechanisms. R3 decides the statistical framework, adjustment for repeated model changes, and reporting language.

A real-data method must not import fitted synthetic states; independent synthetic diagnostics may help investigate suspicious effects, but cannot overwrite or invalidate an observed prospective result merely by disagreeing with it.


### 8.3 Combination methods [PROPOSED]

E_55/E_56 and future ensembles consume **frozen origin-matched source-method forecasts**, never retrospective score tables or future outcomes. Their dependencies are versioned, their constituent selection policies are frozen before the relevant target, and the dependency graph is acyclic. A combination can include a method that is poor, correlated, contrarian, diagnostic, slow or speculative; adaptors and weights must be explicit. Exact evaluation and selection rules belong to R3.

---

## 9. Parallel execution and numerical reproducibility

### 9.1 Initial scheduler [PROPOSED]

- Standard CPython 3.14 on Windows 11, not a free-threaded or experimental interpreter.
- Start with `concurrent.futures.ProcessPoolExecutor` or an equivalent **spawn-safe** process worker pool.
- Worker count configurable from **1 to 12**, one independently executable E-method per worker in the initial version. Methods needing previous-target warm starts execute their own targets sequentially inside their worker.
- If a method has only a main-barrel component or remains diagnostic-only, record that outcome explicitly; do not counterfeit a full combined forecast merely to fill the worker's result schema.
- Other E-methods wait in the queue. Long, high-memory methods may require reducing active worker count or resource reservations; 12 is an **upper bound**, not a mandate.
- Default each worker's native numeric-thread pool to **one thread**, using controlled `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` and/or inspected threadpoolctl settings. Thread limits should be set **before importing** numerical libraries where required.
- Use the standard `if __name__ == "__main__":` guard; entrypoints and worker functions must be importable/picklable under Windows spawn. Send source data once per worker where possible, not once per target.
- Optional 24-worker (SMT) benchmark is allowed only as a separately labelled throughput/resource trial; do not infer it is automatically faster.

**R2-C18:** Worker count, operating-system scheduling and completion order must never determine seed streams, choose model weights, change historical cutoffs or alter method identity.

### 9.2 Stable random-stream assignment [PROPOSED]

Derive the seed stream from an **explicit canonical task identity**, e.g.:

```text
(root_seed, namespace, method_id, method_revision, variant_id,
 source_snapshot_id, target_draw_number, start/restart_index)
```

Use a stable binary encoding / cryptographic digest to produce input integers for NumPy `SeedSequence`; do not use Python's salted built-in `hash()` or the worker index. Save the stable derivation rule, seed/root, NumPy version and job ID. **R2-C19:** Parallel/serial job order must not change model randomness or canonical forecast bytes.

### 9.3 What bit-identical means [PROPOSED]

Compare **canonical prediction payloads**, excluding creation timestamps, elapsed time, CPU time, worker IDs and temporary paths. Canonicalise field ordering and representations (including floats if used) under a documented serialization rule. Record SHA-256 of the canonical payload and require equality of both bytes and digest for 1-worker and 12-worker runs on a matched environment. Equal digests are useful but checking actual bytes where feasible is preferred. Do not compare logs that necessarily differ by scheduling timestamps.

A mismatch is `REPRODUCIBILITY_FAIL` until fixed or until the user approves a justified method-specific exception with clear scope and alternative reproducibility criterion. Merely declaring a general numeric tolerance is **not** an automatic waiver. Parallel floating-point summations or nondeterministic native kernels, if encountered, must be diagnosed rather than assumed impossible.

### 9.4 Resource safety and failure semantics [PROPOSED]

- Record wall-clock startup/import, fit, forecast, output validation and total pool times separately; also per-worker process CPU time.
- Capture worker process peak resident/working-set memory and, when available, aggregate peak worker memory. `tracemalloc` alone is insufficient for NumPy/native allocations; `psutil` is a candidate dependency subject to venv installation approval.
- Configure per-method timeouts; an exceeded timeout is `TIMEOUT` with partial elapsed time, never a fabricated completion duration.
- Worker exception, crash, OOM, non-finite output, invalid set, missing input, insufficient history and unsupported view receive distinct statuses.
- Do not interpret CPU seconds greater than elapsed seconds as conclusive evidence of incorrect thread pinning; inspect per-process scopes and actual thread-pool configuration.
- Keep the host responsive. A 32-GB total system cannot safely grant twelve unconstrained workers 32 GB each. Resource thresholds and worker reductions should be measured and configurable.
- Record the Windows power plan and the CPU model when comparing time series of benchmarks.

### 9.5 Later acceleration is optional

Parallelising independent synthetic histories, independent restarts, and origin blocks can be considered later. Warm-started origin sequences are **not** freely independent: block splitting needs explicitly declared cold starts or state handoffs. Numba, JAX, PyTorch or compiled kernels are optional only after representative benchmarks and current Python 3.14 Windows-wheel checking. No promised 10× or 50× acceleration is assumed. Slow E-methods remain scientific candidates.

---

## 10. Computational benchmark specification — independent of predictive evaluation

**Purpose:** Measure how the system executes and scales on the **user's actual machine**. Benchmarks must not judge whether a method correctly predicted the historical result.

### 10.1 Single benchmark facility, two presets

- `B1`: `X=1` historical prediction target, **N=1577** for the currently frozen development range.
- `B10`: `X=10` consecutive targets, **N=1568,...,1577** for the current source range.
- `W=ALL_PERMITTED` or `W=100` preceding observations at each N−1 boundary; other W values may be named later.
- The nominated `X` targets finish immediately before the designated holdout, **not inside it**.
- Predictions must still be genuinely computed internally for reproducibility and timing, but **benchmark reports display no guessed numbers, rankings, accuracy, winnings or score comparisons**.
- Short-history timing `W=100` is a computational probe, **not** an approved sufficient fitting sample size for every method.

### 10.2 Required timing comparison

1. Run a configured set of methods serially (`workers=1`).
2. Run the identical set concurrently (`workers=12`), subject to memory limits.
3. Compare canonical **predictions**, not timing logs, for bit-identical equality.
4. Compare all-permitted development history versus W=100 at **the same forecast origins**, to isolate the relationship between training length and run cost.
5. Median of three fresh repetitions **where feasible**, with a declared single-repeat alternative for multi-hour/day operations; show actual repetition count, no invented median.
6. Optional one synthetic fair fixture per method for throughput diagnostics, explicitly `BENCHMARK_SYNTHETIC`, with outcomes concealed and no predictive scoring.
7. Optional 24-worker trial after the 12-worker memory and stability baseline.

**R2-C20:** A benchmark job writes `SUCCESS`, `TIMEOUT`, `ERROR`, `INSUFFICIENT_HISTORY`, `BLOCKED_DEPENDENCY`, `NUMERIC_INVALID` or other declared status, along with wall/CPU/resource fields *if actually measured*. Partial timings on failure are labelled partial. A crash must never be reported as a successful fast execution.

### 10.3 Example timing-only report schema

```text
BenchmarkRecord:
    benchmark_id / timestamp / current specification and software digests
    E-method and variant; real-or-synthetic benchmark namespace
    X, W, target_range, source_snapshot_hash, startup_mode
    worker_count, numerical_backend_threads, external package versions
    startup_wall_s, fit_wall_s, predict_wall_s, total_wall_s
    process_cpu_s, peak_process_memory_bytes, peak_pool_memory_bytes
    repeat_number, actual_repeat_count, cold_or_warm_start
    task_status, error_class_if_any, timeout_limit_s
    canonical_prediction_digest_only, serial_vs_parallel_identity_status
```

No prediction content or predicted-vs-observed comparison appears in this benchmark report. A separate protected internal artifact may hold forecast bytes for deterministic equality checking without making them an input to model selection. Later performance dashboards are allowed but may not become scientific winner rankings.

### 10.4 Environment fingerprint

Record OS edition/build, processor, physical/logical core counts, RAM, power plan, Python version and executable, NumPy/SciPy versions, BLAS/backend metadata (`numpy.show_config()` output or digests), relevant pip package versions, method implementation hashes, source snapshot digests, and the threading/seeding policy. Time measurements without environmental provenance are informative only as rough anecdotes.

---

## 11. Error handling, quality assurance and acceptance criteria

### 11.1 Mandatory invariant tests before any actual-history forecast [PROPOSED]

| Test ID | Test | Expected outcome |
|---|---|---|
| T-01 | Out-of-range ball, duplicate main number, wrong count | Rejected/quarantined with exact reason |
| T-02 | Pre-1144 or older-format draw injected | Excluded; explicit policy violation if used as actual eligible observation |
| T-03 | Two source views disagree on set/Powerball | Halt/quarantine affected draw; no silent preference |
| T-04 | Sorted CSV ball columns treated as extraction positions | Must fail view-type assertion |
| T-05 | Select a target N with hidden N/N+1 outputs in original file | Predictor sees only rows ≤N−1; leakage test PASS |
| T-06 | Post-draw external datum with earlier event date | Not admitted if publication time is after cutoff |
| T-07 | Fake synthetic source flagged as REAL | Namespace/provenance check rejects it |
| T-08 | Synthetic fit checkpoint offered to real predictor | Rejected; no latent state can cross namespace boundary |
| T-09 | Probability with negative entries/invalid sum | Numeric validation failure, not an invented winner |
| T-10 | Main set contains repeat/incorrect count | Forecast validation failure |
| T-11 | Order view absent for ordered-only method | `UNSUPPORTED_INPUT_VIEW`, not method deletion |
| T-12 | Warm start derived from a future target | Reject dependency lineage |
| T-13 | One vs twelve workers, same job identities | Bit-identical canonical forecast bytes by default |
| T-14 | Worker timeout/crash/out-of-memory | Explicit status with no fabricated duration |
| T-15 | Benchmark report generation | Contains only resource/timing/status/digest fields; no scores or predicted numbers |
| T-16 | Repeated same source with changed bytes | Different source digest, run provenance, no silent overwrite |
| T-17 | Permitted FINAL real next-draw run | With current validated maximum `L`, uses all `1144..L` without a holdout exclusion and forecasts `L+1`; archive immutable pre-draw evidence |
| T-18 | Holdout evaluation attempted from development mode | Denied with auditable status |
| T-19 | Each E-method registration E_1–E_62 | Exact names/IDs present, including unimplemented and blocked candidates |
| T-20 | E_57 diagonal DPP treated as sequential weighted draw | Distinct-law check FAIL until corrected |
| T-21 | E_58/59 raw `|psi|²` treated as valid seven-set probability | Invalid; must specify lawful seven-number selection |
| T-22 | E_61 κ=0 legal sequence/set model | Equal-probability seven-of-35 model, independent of hidden trajectories |
| T-23 | Historical prediction target N | Method receives only 1144..N-1, then independent evaluator compares frozen forecast with actual N |
| T-24 | Updated actual CSV ending at L+1 | New FINAL run automatically forecasts L+2; prior L+1 forecast and evaluation remain unmodified |
| T-25 | Synthetic diagnostics or apparent low chance cited as reason to label a real forecast a bug/coincidence | Label remains provisional unless specific supporting evidence exists; verified code faults distinctly recorded |
| T-26 | Optional external features absent | Core draw-number-only forecasting still runs; no exact timestamp requirement |
| T-27 | `transitory_data/` files left from a prior run | No automatic read/reuse as authoritative inputs; scratch isolation and Git ignore verified |
| T-28 | Method fit state written to scratch and another run starts | No implicit intermediate-state reuse; any authorised checkpoint requires explicit lineage and configuration |
| T-29 | Repeated real FINAL forecasts and later known results | All pre-draw forecasts archived intact, outcomes added separately, unsuccessful/failed targets retained |


### 11.2 Method-specific numerical fixtures [PROPOSED]

For each implemented method, provide at least one small deterministic fixture with an independently checkable mathematical result, a no-look-ahead fixture, a seeded-run fixture if stochastic, a numeric-failure fixture, and a result-type validation fixture. Diagnostic-only methods validate their advertised diagnostic output without inventing a seven-number selection. More elaborate synthetic tests do **not** automatically serve as eligibility gates; they are distinct research diagnostics.

For E_57 test positivity/PSD, finite `Z_7`, valid fixed-size distribution and `L=I` uniformity. For E_31/61 test sequential likelihood normalisation on tractable toy cases, then validate the equivalence of ordered sum and unordered legal-set likelihood at testable small dimensions. For E_61/62 test the difference between zero-noise order preservation and outcome-conditioned reinjection; check the reference field and state dynamics with an independently verifiable small numerical example.

### 11.3 Reproducibility and process robustness [PROPOSED]

- Run repeat-test on one and twelve workers under identical environment/seed/configuration and verify **canonical payload bytes**.
- Verify worker exceptions propagate as status records and that partial results cannot be counted as completed method forecasts.
- Verify per-method timeout, interruption and restart do not import stale hidden states from a different target or dataset revision.
- Verify the source/variant/method revision is frozen in forecast provenance.
- Later R3 supplies statistical evaluation-specific tests and reporting requirements; R2 must not silently add a significance threshold now.

---

## 12. Repository organization and development workflow

### 12.1 Existing repository (do not relocate files silently)

```text
analysing_perceived_randomness_in_reality/
    .vscode/
    .venv/                              # local, ignored by Git
    doc/
        Predictive_Randomness_Research_Project_Proposal_v0_3.md
        Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md
        Predictive_Randomness_Experimental_Method_Specifications_R2_v0_2.md
        SAL_Powerball-Game-Rules_March-2026.pdf
    src/
        scrape_australian_powerball_history_from_2018_04_19_v0_3.py
        ... future predictor packages/modules ...
    source_data/
        australian_powerball_history_20261021.csv
        australian_powerball_draw_order_20261021.csv
    results/
    requirements.txt
    .gitignore
    LICENSE
    README.md
```

`...` denotes **illustrative future files**, not existing files. In the previously inspected repository ZIP, a historical proposal version was present; Proposal v0.3 and R1 v0.4 have since been explicitly ratified by the user. Install/update actual repository files under version control explicitly, rather than assuming the ZIP already contains them. The `doc/` directory is the destination selected by the user.

### 12.2 Future layout proposal, not an instruction to create directories yet

```text
src/predictive_randomness/            # common Python CODE: loader, validation, registry, runner, maths
src/predictive_randomness/methods/    # E-method modules, progressively added
src/predictive_randomness/synthetic/  # generators and isolated diagnostics
src/predictive_randomness/benchmark/  # timing-only runner
src/tests/                            # fixture tests
source_data/                          # authoritative validated actual input snapshots
transitory_data/                      # optional disposable scratch; Git-ignored; per-run isolation
results/real/development/             # versioned historical forecasts
results/real/holdout/                 # controlled final evaluation
results/real/prospective/             # immutable future forecasts and separate later comparisons
results/synthetic/null/               # independent simulated histories
results/synthetic/planted/            # independent planted-effect research
results/synthetic/identifiability/     # recovery diagnostics
results/benchmark/                    # timings only, split real/synthetic
```

The existing scraper may be retained in `src/` as-is. Any change to CSV output paths or input acquisition requires a separate controlled source revision; this R2 deliverable does **not** modify it.

**Clarification of “shared data”:** `src/predictive_randomness/` refers to reusable **Python modules** and, as needed, a common immutable **in-memory view of source observations** permitted for the target draw. It does **not** designate a pool of fitted states or intermediate prediction results that another experiment or a repeated run may transparently consume. Experiments may share common stateless numerical routines; model A's fitted intermediate state is **not** implicitly input data for model B. Deliberate ensemble inputs use only explicitly frozen and versioned source-method forecasts under their defined method-combination contract.

**Proposed `transitory_data/` discipline:** Create this root directory **only if** an algorithm actually requires temporary disk-backed data. Default to in-memory calculations. A temporary artifact is scoped to a particular namespace, run ID and method or worker; concurrent workers use noncolliding paths. The directory must be added to `.gitignore` as `/transitory_data/`; contents are **disposable** and must never automatically become `source_data/`, `results/` or a valid input to any subsequent or parallel run. Cleanup and crash residue handling must be controlled. If a later expensive method needs persistent checkpoints or restart after interruption, that capability must be **separately specified, approved and provenance-validated**: a resumable state is not automatically authorised merely because a temporary file exists. Real and synthetic scratch spaces may never exchange fitted states.


### 12.3 Python environment, dependencies, and installation policy [AGREED/PROPOSED]

- Preserve the user's working standard Python 3.14.8 project `.venv`. Do not install modelling libraries globally and do not change VS Code configuration without a demonstrated reason.
- To run in an independent CMD: `call .venv\Scripts\activate.bat` (or the user's working `activate_venv.bat`). VS Code's working custom CMD terminal profile activates it automatically.
- Existing dependency record contains scraper packages (not a complete predictor numerical stack). Any additional PyPI package must be **announced before installation**, its Python 3.14/Windows support checked at the time, and its version recorded in `requirements.txt` or an explicitly named supplementary lock specification.
- Probable first numerical layer: `numpy`, `scipy`; optional `psutil`, `threadpoolctl`; later model-specific libraries only as needed. A dependency in R1 is a research suggestion, not a current installation requirement.
- Keep `.venv/` excluded from Git. Include source, documentation, appropriately licensed observational data, tests and manifest/requirements files as the user approves.

### 12.4 Future command-line experience — draft, not frozen CLI

Potential commands might have forms such as:

```text
python -m predictive_randomness validate-data --snapshot <...>
python -m predictive_randomness registry --list
python -m predictive_randomness benchmark --preset B1 --window 100 --workers 1
python -m predictive_randomness benchmark --preset B10 --window all --workers 12
python -m predictive_randomness forecast --mode development --methods E_1,E_2
python -m predictive_randomness forecast --mode final-next-draw --methods ...  # infer current L -> target L+1
```

These illustrate *purpose*, not installed scripts or approved flags. Versioned command semantics are for a later implementation ticket.

---

## 13. R2/R3 interface and explicit deferred decisions

### 13.1 What R2 controls if ratified

R2 should fix the source schema, registry and immutable method identities, fit/forecast separation, forecast-result types, data-cutoff enforcement, common ordered/unordered view semantics, namespace firewall, canonical reproducibility, initial benchmark instrumentation and method-specification worksheets. It should record what remains mathematically unspecified, not force every candidate into an arbitrary algorithm.

### 13.2 What R3 must decide later

**R2 explicitly does not ratify**:

- Main-number and Powerball performance score definitions and aggregation.
- Whether to rank by count of correctly predicted numbers, likelihood, calibration, proper scoring rules, or other metric; nor any winner threshold.
- Multiplicity correction, uncertainty intervals and standards for a surprising result.
- Method and ensemble selection/reweighting policy (including apparently poor methods), selection freeze, and holdout disclosure timing beyond established rules.
- Forecast comparison windows, repeated prospective-forecast evidence and minimum statistically relevant training/evaluation lengths, including how many real future draws can meaningfully support a conclusion.
- Any conclusion about perceived reality, independence, quantum causes, equipment physics, or nonlocal association based on research mathematics alone; and rules for avoiding premature “coincidence,” “synthetic artefact” or “implementation error” classifications without excluding demonstrable faults.

### 13.3 Mathematical specification questions to ratify in later R2 iterations

- Exactly which mathematical **variant** of each E-method will be first implemented, with complete equations and parameter bounds.
- Which E-methods are diagnostic-only pending a forecast adapter, and which initially generate direct predictions.
- Global score/rank tie policy; legality and normalization tolerance rules; rounding/serialization of floating-point values.
- How a whole-set model selects its publicly displayed seven-number prediction and how the Powerball companion is chosen where not internally modelled.
- Which data view is the default for eligible sequential models, while retaining both permitted views.
- Inference algorithm, seed/restart count, convergence and resource budgets for E_57–E_62.
- Exact worker timeout, memory management and checkpoint resume rules.
- Source-data correction handling across repository versions and real forecast immutability mechanism.
- Exact user interaction for authorising final holdout and real next-draw prediction.

### 13.4 Approval discipline

A proposal here marked `[PROPOSED]` is **not ratified merely because this document was delivered**. The user may ratify (a) the common R2 framework first and (b) individual mathematical method worksheets in stages. This prevents a large document from silently resolving dozens of open statistical or model-fitting questions. Claude or another reviewer may provide voluntary critique, but no further external review is a standing prerequisite; the user remains the decision authority.

---

## 14. Suggested implementation plan after R2 and R3 decisions

**Stage S0 — Freeze documentation handoff:** Commit ratified Proposal v0.3, R1 v0.4 and eventually approved R2. Confirm repository source/data hashes and data-availability cutoff.

**Stage S1 — Data/registry skeleton:** Implement immutable CSV loading, two-view consistency checks, cutoff guard, permanent 62-entry registry, result types, namespace routing and unit tests. Do not build a whole predictor out of a false random/probability adapter.

**Stage S2 — Minimal methods and single-target runner:** After approving their first precise formulas, implement selected transparent E-methods (original E_1–E_6 are natural initial candidates, but not the only legitimate selection). Test numeric behaviour and store canonical pre-evaluation forecasts.

**Stage S3 — 1/12-worker execution and B1/B10:** Verify Windows spawn, thread pinning, seed identity, bit-equality and timing-only reports. Establish realistic performance before adding expensive methods.

**Stage S4 — Expand all-method catalogue implementation iteratively:** Implement additional E-methods and variants without any exclusion based on speculative status, poor results or correlation. Resource-heavy E_57–E_62 may need separate implementation tickets and benchmarks. Preserve all unimplemented identities and potential future E_63–E_106 research additions.

**Stage S5 — R3-governed scoring/holdout/FINAL forecast:** Only after R3 is ratified, run authorised historical evaluations and (when requested) the reserved independent holdout. Each user-authorised genuine forecast must derive `L` from the validated actual-data CSV, fit from every available eligible actual draw through `L` (subject only to an explicitly defined method window), and forecast `L+1`. Preserve its pre-draw archive proof, append the later actual-result comparison separately, then repeat using updated history for the following week. Draw numbers, not clock timestamps, control the model chronology; archive timestamps are optional evidentiary metadata, not fitted predictors.

**Stop rule:** At each step, a failure should identify the blocked unit and its evidence. Do not mark the whole method scientifically invalid because implementation is not yet available.

---

## 15. R2 review checklist and decision register

The following are proposed decisions requiring user consideration; retaining them as a list ensures no implicit approvals:

| ID | Question / proposed decision | Proposed position | Status |
|---|---|---|---|
| R2-D01 | Treat Proposal v0.3 and R1 v0.4 as controlling ratified documents | Yes | **Already agreed** |
| R2-D02 | Register all 62 E-method identities from R1, including diagnostic-only and pilot-wave methods | Yes | **Agreed on retention; software mechanism proposed** |
| R2-D03 | Use a canonical immutable draw model joining the two CSV views on draw key | Yes | **PROPOSED** |
| R2-D04 | Adopt one `UNORDERED_SET` / `OPERATOR_DRAWN_ORDER` / paired-view policy | Yes, with no double counting | **PROPOSED** |
| R2-D05 | Support typed ranks, marginals, whole sets, ordered distributions and diagnostic-only methods | Yes | **PROPOSED** |
| R2-D06 | Use a runner-enforced cutoff and distinct execution namespaces | Yes | **PROPOSED** |
| R2-D07 | Implement 1–12 process pool, one method per worker, pinned one-thread numerics | Yes | **Direction already agreed; mechanics proposed** |
| R2-D08 | Implement B1/B10 with W=100/all, timing-only and explicit statuses | Yes | **Direction already agreed; mechanics proposed** |
| R2-D09 | Require canonical bit-identity 1 vs 12 workers; explicit approval of exceptions | Yes | **Agreed principle; byte format proposed** |
| R2-D10 | Keep synthetic learning allowed but prohibit synthetic training-state contamination | Yes | **Already agreed** |
| R2-D11 | Retain variants without forcing a new E-number solely for observation view | Yes | **PROPOSED** |
| R2-D12 | Stage approval of numerical method formulas rather than auto-freeze all 62 now | Yes | **PROPOSED** |
| R2-D13 | Freeze exact tie policy, mathematical first variants and time budgets after review | Defer concrete choices | **OPEN** |
| R2-D14 | Defer scores, uncertainties, ensembles' evaluation and promotion to R3 | Yes | **Already agreed** |
| R2-D15 | Historical-evaluation mode uses actual draw IDs and only N-1 history; evaluator compares later | Yes | **User clarified; proposed software contract** |
| R2-D16 | FINAL mode determines L from validated actual data, trains on all 1144..L without ten-draw exclusion, predicts L+1 and repeats as new actuals arrive | Yes | **User explicitly agreed** |
| R2-D17 | External series optional; timestamps not required for core forecast; retrospective-only associations labelled distinctly | Yes | **User clarification; detailed contract PROPOSED** |
| R2-D18 | Shared data means common software and permitted in-memory source views; no implicit intermediate-state reuse | Yes | **User clarification; detailed contract PROPOSED** |
| R2-D19 | Introduce optional Git-ignored `transitory_data/` only for necessary isolated scratch; persistent checkpoint reuse requires a separate approval | Yes | **User requested; detailed contract PROPOSED** |
| R2-D20 | Do not pre-judge surprising fits as coincidence, synthetic artefact or implementation error; maintain prospective forecast/evaluation trail while recording verified faults | Yes | **User explicitly required; R3 standards DEFERRED** |


### What acceptance of this document would mean

If the user approves R2 v0.2 **as a framework**, the common contracts and administrative approach become the implementation design basis, while explicitly open mathematical choices remain open. If the user instead requests **complete frozen mathematics for all 62 before any coding**, an additional R2 method-by-method ratification revision will be necessary. Both paths preserve all experimental ideas and do not weaken the project philosophy.

---

## 16. Source traceability and handback

### 16.1 Authoritative source documents

1. **Proposal v0.3:** `Predictive_Randomness_Research_Project_Proposal_v0_3.md`, especially §§0–2 (authority/philosophy), §§3–6 (observational and historical contracts), §8 (expanded research), §9 (retention), §10 (synthetic safeguards), §§11–12 (data and proposed software), §14 (stages), and §18 (deferred decisions).
2. **R1 v0.4:** `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md`, especially §4 (all numbered methods), §4.7 (pilot-wave family and precise candidate mathematical constraints), §7 (separated research streams), §8 (R3 deferral), §8A (benchmarking), §9 (possible dependencies), §10 (decision proposals), and §11 (technical bibliography).
3. **Observed repository snapshots:** `source_data/australian_powerball_history_20261021.csv` and `source_data/australian_powerball_draw_order_20261021.csv` for Draws 1144–1587, plus the project scraper v0.3 and Australian game-rules PDF.
4. **User's subsequent ratification:** explicit in this conversation after the v0.3 proposal and R1 v0.4 deliverables. Ratification is an external approval event, not retroactively changed wording inside the historical source document.

This R2 document builds on those sources and deliberately **does not reproduce the full R1 research references or all derivations**; those remain authoritative in R1. When a method-specific mathematical claim is in doubt, consult its complete R1 entry and cited technical source before writing code. Any new inference or proposed design rule in R2 is marked accordingly.

### 16.2 Explicit non-claims

No E-method has been coded, statistically scored, accepted as predictive, or used to infer an altered law of reality in this document. No null-world or planted-effect study has been run by this document. No holdout draw has been used for selecting methods. No PyPI modelling package has been installed on the user's PC by this document. No change has been made to original CSVs, source scripts or existing ratified Markdown files.

### 16.3 Recommended next review action

Review this R2 v0.2 candidate for scientific intent and software-contract boundaries. Approve or revise R2-D02–D20 individually as needed, then decide whether to (a) ratify the common framework and specify method mathematics iteratively or (b) demand complete first-variant mathematics for every method before starting implementation. There is no requirement to convene Claude unless a new substantive mathematical disagreement warrants it.

**Closing principle:** We do not claim to know in advance what patterns can or cannot exist in perceived reality. We make even unusual hypotheses precise enough to be tested without giving conventional theory veto power. Unexpected results remain worthy of continued, documented investigation—not prematurely classified as a coincidence, artificial-data artefact or bug on theoretical grounds. Verified data/software faults are reported as such; meaningful evidence for (or against) predictive structure is assessed through faithfully archived, repeated real-world forecasts and their subsequent actual results, with the statistical interpretation reserved for R3.

