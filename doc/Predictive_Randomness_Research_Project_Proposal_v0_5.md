# Australian Powerball / Oz Lotto: Experimental Investigation of Randomness, Predictability, and Perceived Reality

## Comprehensive project proposal — v0.5 consolidated, OWNER-RATIFIED (26 October 2026)

**Edition status: OWNER-RATIFIED 26 October 2026 (consolidated v0.4 review baseline).** This edition supersedes Proposal v0.4. Ratification of documentation alone grants no run, Mode H, holdout, process-termination, scraper/update or scientific-use authority.

**Platform:** Windows 11; Python 3.14, project-local `.venv`; AMD Ryzen 9 3900X (12 physical / 24 logical), 32 GB RAM; VS Code and Windows CMD.  
**Permanent method register:** E_1..E_62 presently described; room for additional owner-approved E-numbers.  
**Current data:** Versioned accepted development masters, as specified in §3 and R2; historical two-CSV and scraper descriptions are superseded.  

> **Central premise — deliberately unconventional:** This project is an empirical investigation of whether the apparent randomness of real-world Australian Powerball draws hides any exploitable structure. It expressly permits questioning familiar assumptions about probability, temporal independence, causal relationships, connectedness, and even the way we conceptualise perceived reality. We do **not** rule out a method merely because prevailing models say it should not work. Equally, we do **not** pronounce a method predictive merely because it produces an intriguing pattern. All proposals are welcome to be examined; evidence, reproducibility, mathematical consistency, and prospective performance decide what conclusions can honestly be drawn.

---

## 0. Document authority and current research state

The consolidated Proposal governs research philosophy and project charter. R1 v0.4 governs the permanent research-method catalogue; R2 v0.4 governs experimental inputs, mathematical/software contracts and N−1; R3 v0.4 governs evaluation, freeze and reporting; Architecture v0.7 governs runtime/safety; P3 v0.2 governs outstanding implementation. The specified consolidated governing editions were **owner-ratified on 26 October 2026**. The former §0A multi-game amendment, §0B decisions and approved R2 errata have been integrated into their subject sections; the historical record remains in prior ratified files, not as operative contradictory paragraphs here.

**Current development data (25 October 2026, master version 1):** `POWERBALL` draw 1144–1576 (433 rows; master SHA-256 `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8`) and `OZLOTTO` draw 1474–1693 (220 rows; master SHA-256 `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f`). Authoritative versioned files are `source_data/<GAME>_results_master.csv`, `source_data/<GAME>_results_master_ledger.csv` and `source_data/<GAME>_results_master_init_verification.json`; the `INIT` ledger record and initialisation record bind these identities. These are the owner's accepted development masters, confirmed by Claude against Git HEAD `3ddb8a6` on 25 October 2026; verify identities again against the current Git HEAD before coding. Lotterywest's ordinary results-search pages were acquired with the committed owner-run tools. The published number sequence is **`OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`**, not verified physical drawing order. Three supplementary Oz Lotto labels are provenance only and never become scientific inputs. Results from 1 August 2026 onward are quarantined: Powerball 1577+ and Oz Lotto 1694+. `FINAL_HOLDOUT_10` is Powerball 1577–1586 and Oz Lotto 1694–1703; development caps are 1576 and 1693, respectively. The E_1 target-1577 regression is strictly a *forecast-only* exception using 1144–1576, not a permission to read or score its outcome. These constraints are normative in R2 v0.4 (data/views) and R3 v0.4 (evaluation/freeze).

**Current execution boundary:** ChatGPT implements and Claude independently reviews; the owner alone ratifies. No Package 2 v0.11 code or scientific use is approved by this documentation. All existing process-termination switches remain False; no uncertain PID may be killed and the global unresolved-orphan interlock remains binding. Current coordinator supports at most six methods concurrently (configurable one through six), with timing and full Windows acceptance gates in Architecture. Result/score consumer allowlist remains empty.

**Document classification:** DECIDED items are owner-ratified/owner-decided; RECOMMENDED items await specific owner approval; OPEN items remain unresolved. Neither documentation ratification nor independent review grants execution authority. Completed: accepted E_1 Powerball forecast-only regression and development master initialisation, with reported independent checks. Outstanding: Package 2 reader and coordinator v0.11 corrections, independent review, and acceptance before scientific use. R1/R2 methodology and future per-method mathematical details are not presumed implemented.

---

## 1. Executive statement

### 1.1 Purpose

Develop an extensible Python-based **experimental research environment** for exploring whether historical Australian Powerball results can help forecast subsequent results, and, if so, under what conditions, by what techniques, and with what measurable reliability.

The project is **not** premised on an assertion that Powerball can be predicted. Nor is it premised on the assertion that it cannot be predicted. Its purpose is to **investigate**, including through unconventional and speculative approaches that would ordinarily be excluded by starting from a fully independent-and-uniform drawing model as an unquestioned truth.

It is important that this research remain capable of reporting a genuinely surprising observation without dismissing it on principle. A surprising observation also must not be promoted prematurely into evidence of a discovery: repeated independent validation, error analysis, and prospective testing are necessary.

### 1.2 Desired practical capabilities

The eventual system should:

1. Read and validate a locally maintained, progressively growing draw-history CSV.
2. Maintain the main-number barrel and Powerball barrel as **distinct prediction targets**, while presenting their selected predictions as a combined draw prediction.
3. Register and execute numerous individual experimental predictive methods, each with a permanent identifier and understandable name.
4. Predict historical draws **as they would have been predicted before those draws occurred**, using only information then available.
5. Compare predictions with actual outcomes, including proper chance-based reference results and uncertainty where relevant.
6. Preserve **every** method, including low-ranked, apparently ineffective, odd, and speculative methods.
7. Examine individual methods and combinations of methods, including combinations that draw on seemingly poor standalone methods.
8. Support real, next-draw predictions using all available history when the user explicitly chooses to perform such a prediction.
9. Keep a transparent, reproducible record of methods, data, configuration, predictions, results, evaluations, and decisions.
10. Permit the evaluation and method-qualification policies to evolve, with changes explicit, justified, and subject to user agreement.
11. Support source-qualified **operator-labelled drawn order** as well as unordered seven-number sets where applicable, under one shared R2 input policy.
12. Support computational benchmarking **separately from predictive merit evaluation**, with resource-safe parallelism, reproducible results and explicit failure reporting.

### 1.3 What is *not* being claimed

No winning-number forecast has been shown to beat chance. No causal mechanism, universal interconnection, hidden temporal dependence, or break in accepted probability theory has been demonstrated. This document authorises **investigation** of such possibilities, not belief in them.

A good outcome may be a reliable positive result, a clear negative result, a discovery about the biases or fragility of analysis methods, or a better understanding of when apparently astonishing predictions arise by chance.

---

## 2. Foundational research philosophy: challenge perceived reality

### 2.1 A deliberately assumption-challenging investigation

The principal motivation is to investigate the possibility that what we *perceive* as randomness in reality may not exhaust the structure of actual events. The project is willing to question whether something ordinarily called an independent random event may nevertheless carry detectable associations with prior observations, subtle temporal structures, environmental processes, unknown mechanisms, or relationships not represented in conventional lottery models.

This includes, without endorsing any particular explanation:

- Unexpected recurrence, clustering, or periodicity.
- Long- or short-range temporal associations.
- Weak nonstationarities and evolving distributions.
- Nonlinear dependencies, chaotic-looking phenomena, and hidden-state processes.
- Information present in combinations of observations but not in individual marginal frequencies.
- Counterintuitive conditional relationships.
- Cross-scale effects, delayed or indirect associations, and unexplained regularities.
- More speculative ideas about connectivity, synchrony, complex systems, and the adequacy of our models of reality.

**None of these avenues is to be rejected solely because conventional probability models predict that it should fail.** A proposed model is to be evaluated on its definability, operational meaning, integrity of its test, and observed predictive results.

### 2.2 “No assumptions” — the precise project meaning

The phrase **“no assumptions”** is understood as **no unexamined assumption that forecloses a potentially testable hypothesis**, particularly the assumption that historical draws categorically cannot convey predictive information.

It does **not** mean abandoning logical consistency, arithmetic, observable lottery rules, data provenance, or the distinction between evidence and speculation. Some premises are unavoidable to calculate anything: for example, a draw entry has a date, a draw identifier, seven distinct main numbers and one Powerball under the chosen rules. These are **observational and game-definition constraints**, not prejudgments about the predictive question.

Three layers must therefore remain distinguishable:

| Layer | Treatment in this project | Example |
|---|---|---|
| **Observed facts and game definitions** | Apply and verify, subject to correction if the evidence changes | Seven distinct main numbers from 1–35 and a Powerball from 1–20 in the selected era |
| **Reference hypotheses** | Quantify and test; do not elevate to unchallengeable truth | Independent, uniform draws with fixed probabilities |
| **Exploratory hypotheses** | Permit, implement when sufficiently specified, and test fairly | Numbers have time-varying recurrence signatures that forecast a future draw |

A technique may be mathematically coherent but empirically ineffective. Another may be mathematically invalid (for example, data leakage disguised as a prediction). The project should identify that difference honestly rather than label everything unusual as nonsense.

### 2.3 The independent-draw model is a benchmark, not a veto

Under the conventional *ideal* model, each numbered main ball has marginal appearance probability `7/35 = 0.20` on any given draw, and each Powerball value has probability `1/20 = 0.05`. A uniformly chosen seven-number ticket has an expected overlap of `7 × 7/35 = 1.4` main numbers with the actual draw. These are mathematical consequences **conditional on that reference model**.

They provide essential comparison targets. They are **not** used as a reason to ban tests of dependencies, unequal probabilities, hidden patterns, or anomalous outcomes. If a method convincingly exceeds these benchmarks on properly isolated future data, that is precisely the sort of result to investigate.

The fixed sampling structure does impose real constraints: within one main-barrel draw, seven numbers are sampled without replacement. For purposes of the model, per-number probabilities and whole-combination probabilities must not be confused.

### 2.4 Monty Hall as a conceptual reminder — and its limit

The Monty Hall problem is cited as a reminder that probability can be profoundly counterintuitive and that information from earlier events or observations can affect conditional probability assessments. It motivates openness to unexpected informational structures.

It is **not proof** that past lottery results alter the probabilities of subsequent independent draws. The familiar Monty Hall result follows from the host’s specified behaviour, which provides information. In this project the analogous question is whether **some comparable informational structure actually exists in the observed draw data**, including a structure not yet anticipated by conventional models. That question is to be examined, not assumed away.

### 2.5 The policy for strange or poor results

> **A surprising result deserves examination, not automatic acceptance or dismissal.**

This applies equally to surprisingly high, low, negative, contradictory, unstable, or unintuitive performance. Methods that appear unsuccessful remain part of the experiment and can contribute to later investigations, including as contrarian signals, components of combinations, or indicators of what *does not* work.

### 2.6 Operational meaning of a claim about “reality”

The research may challenge received intuitions about reality, but its findings must be stated at the evidentiary level actually reached. For example:

- “A model scored unusually well on this historical segment” is a **descriptive observation**.
- “The advantage persisted on a previously untouched evaluation segment” is **stronger evidence**.
- “The model beat a declared chance baseline on prospective draws repeatedly, with uncertainty accounted for” is **stronger still**.
- “The universe is connected in a way that makes lotteries predictable” is a **much broader causal or metaphysical claim** and would require evidence beyond a favourable backtest.

This distinction keeps the project radical in **what it is willing to test**, yet disciplined in **what it concludes**.

---

## 3. Existing resources and observational domain

### 3.1 Known game rules and era boundary

For the current-format Australian Powerball game, the working game definition is:

- **Main barrel:** seven **distinct** numbers selected from integers `1` to `35`.
- **Powerball barrel:** one integer from `1` to `20`.
- The main-barrel and Powerball outcomes are distinct components of the same reported draw.

The first draw governed by the current seven-from-35 and one-from-20 game matrix was **Draw 1144 on Thursday 19 April 2018**. This is the **inclusive start** of the primary dataset. Lotterywest confirms the seven-from-35 change, with the Powerball remaining one-from-20 ([Lotterywest announcement, 12 April 2018](https://www.lotterywest.wa.gov.au/lotterywest/media-centre/powerball-to-deliver-more-winners-and-bigger-jackpots)); the historical result is accessible at [Lotterywest Draw 1144](https://www.oz.lotterywest.com/powerball/results/draw/1144). Draw 1145 on 26 April 2018 also belongs to this same era and must be included.

**Hard exclusion decision:** All historical draws using **any different numbers of balls in a barrel, any different drawing count, or any other incompatible game configuration** are excluded from the real predictive dataset. This applies **even if one component (such as the Powerball barrel) retained its current rules**. There will be **no extended pre-April-2018 Powerball-only training variant**. D4 from the external review is expressly rejected. If future game rules change, the programme must stop and require new, explicit dataset/era policy rather than silently merge data.

**Current development data (25 October 2026, master version 1):** `POWERBALL` draw 1144–1576 (433 rows; master SHA-256 `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8`) and `OZLOTTO` draw 1474–1693 (220 rows; master SHA-256 `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f`). Authoritative versioned files are `source_data/<GAME>_results_master.csv`, `source_data/<GAME>_results_master_ledger.csv` and `source_data/<GAME>_results_master_init_verification.json`; the `INIT` ledger record and initialisation record bind these identities. These are the owner's accepted development masters, confirmed by Claude against Git HEAD `3ddb8a6` on 25 October 2026; verify identities again against the current Git HEAD before coding. Lotterywest's ordinary results-search pages were acquired with the committed owner-run tools. The published number sequence is **`OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`**, not verified physical drawing order. Three supplementary Oz Lotto labels are provenance only and never become scientific inputs. Results from 1 August 2026 onward are quarantined: Powerball 1577+ and Oz Lotto 1694+. `FINAL_HOLDOUT_10` is Powerball 1577–1586 and Oz Lotto 1694–1703; development caps are 1576 and 1693, respectively. The E_1 target-1577 regression is strictly a *forecast-only* exception using 1144–1576, not a permission to read or score its outcome. These constraints are normative in R2 v0.4 (data/views) and R3 v0.4 (evaluation/freeze).

### 3.2 Historical CSV and operator-labelled drawn order

The accepted results masters are versioned, per-game immutable development-source identities; see the current data paragraph above and R2 §2.

The reviewed starting boundary remains **Draw 1144, 19 April 2018**; no observations from a different main- or Powerball-barrel rule configuration may be added even for a barrel-only variant. The valid source dataset will grow as new completed draws are collected and validated. Filename dates represent acquisition dates, not necessarily dates of the most recent draw.

**Source qualification:** Draw order is source-published and owner-assumed, not independently proven to match actual physical draw order; see R2 §4 and the factual exposure record.

The period and complete historical record are small enough for standard in-memory techniques, although some proposed latent-state optimisation methods will be computationally intensive. Source integrity and information availability **before each forecast cutoff** remain binding requirements.

### 3.3 Acquisition is distinct from prediction

The present project starts from locally available results. The prediction program should **not depend on live web scraping during a backtest**, and it must never use a newly refreshed results source to reveal the outcome of a draw it is pretending to predict.

A separate update/validation step may refresh the CSV. The research system then takes an explicitly identified, validated snapshot of the CSV. This separation makes retrospective experiments reproducible and protects against inadvertent future-information leakage.

### 3.4 Existing simple analyses

Lottery websites already report elementary descriptive statistics, including frequencies, percentages, and average intervals since appearance. These are useful **starting points**, not authority about predictive efficacy. Our proposed research aims to test, extend, question, and combine such approaches rather than assume their claims are correct.

### 3.5 Scale and computational feasibility

A few hundred draws, with eight numeric outcomes per draw, form a very small dataset by modern computing standards. Most methods can run comfortably in memory on an ordinary Windows PC, including thousands of walk-forward evaluations for inexpensive algorithms.

The principal limitation is likely to be **statistical information content**, not RAM or CPU capacity. Sophisticated models can be computationally easy to fit while having far too few truly independent observations to establish predictive generalisation.

---

## 4. Confirmed requirements and decisions from the discussion

The following are recorded as **agreed project intentions**, not merely assistant recommendations. The original A-identifiers are retained to preserve traceability; new decisions extend the series. Approved concepts do **not** automatically ratify every mathematical formula or software interface suggested later.

| ID | Agreement |
|---|---|
| **A-01** | The purpose is open-ended experimentation into apparent randomness and the possibility of historical predictive information, including challenges to conventional assumptions about reality. |
| **A-02** | Conventional independence assumptions do not provide an automatic exclusion rule for speculative but testable methods. |
| **A-03** | Clearly distinguish an implementable or interesting hypothesis from proven predictive value and from outright mathematical defects. |
| **A-04** | Use **Draw 1144 (19 April 2018) onward**, including the two late-April draws, and only draws having the complete identical current **7/35 + 1/20** game configuration. Earlier draws are excluded even for Powerball-only experiments. |
| **A-05** | Treat main-ball and Powerball predictions separately, then produce a combined draw prediction. |
| **A-06** | Use chronological, out-of-sample historical predictions: a model predicting draw `N` sees only eligible information from draws **before** `N`. |
| **A-07** | Support the “last 10” historical-prediction concept; design the retrospective evaluation count to be configurable. |
| **A-08** | Reserve the **fixed, calendar-quarantined `FINAL_HOLDOUT_10`** (Powerball 1577–1586; Oz Lotto 1694–1703), never the moving latest ten, as the independent final historical evaluation set. The date boundary is 1 August 2026. |
| **A-09** | When deliberately making a **real prediction for the next unobserved draw**, allow the chosen model to use **all currently available history**, including those 10 draws. |
| **A-10** | The recurrence-interval idea concerns reaching or being near a characteristic **optimal interval on the next draw**, **not** simply being the most overdue. |
| **A-11** | Begin with six user-proposed experimental families and allow research into **up to 100 additional candidate methods if useful** (not a quota). R1 currently contains the original six plus **56 additional candidates** (`E_1`–`E_62`). Candidate listing is not implementation approval. |
| **A-12** | Methods have permanent identifiers `E_1`, `E_2`, … and explanatory names, with modular Python implementations and shared utilities. |
| **A-13** | Preserve **every method**, regardless of standalone rank, apparent failure, novelty, or lack of explanatory mechanism. |
| **A-14** | Every method remains eligible for future single-method or multi-method experiments and combinations, subject to transparent criteria. |
| **A-15** | Combination experiments receive new permanent experimental identifiers; qualification and weighting criteria can evolve, with user review and agreement. |
| **A-16** | Score, compare, and report predictions against known draws, but **defer detailed scoring and selection-policy decisions** until the exploratory-method research and design have been discussed. |
| **A-17** | Python **3.14** is the intended implementation platform. Additional packages must be flagged explicitly and installed only into a **project-specific virtual environment**, not globally. |
| **A-18** | Development is phased and owner-gated: ratified research and method specifications precede scientific execution; Package 1 data acquisition and E_1 regression foundations have been completed; Package 2 v0.11 and its reviews are outstanding.
| **A-19** | **D1 direction accepted:** separately run null-world, planted-effect and other synthetic/calibration studies, including thousands of simulations where useful. These may inform **disclosed** design, calibration, sensitivity, debugging and interpretation but are not evidence of real predictive success or an automatic eligibility gate. |
| **A-20** | **Synthetic/real firewall (clarified):** artificial observations, fitted synthetic states, synthetic forecasts/outcome scores and synthetic-only parameter fits are never mixed with real draws, real fitted forecast states or real predictive scores. **Documented methodological learning** from simulations is permitted, including model-design and feasibility choices. No method is automatically excluded for failing a synthetic diagnostic. |
| **A-21** | **D2 direction accepted:** investigate additional observations, including now-supported **operator-labelled drawn order** and optional machine/ball-set information. Equipment metadata is neither necessary nor a gating dependency. |
| **A-22** | **D3 accepted:** correct the full compatible historical starting point to **Draw 1144, 19 April 2018**, with no first-two-draw omission. |
| **A-23** | **D4 rejected:** no historical observations from **any** earlier differing game-matrix configuration; specifically, no older Powerball-only extension even if its barrel individually resembled the current one. |
| **A-24** | **D5 provisionally accepted:** reserve extensibility for independent external, time-indexed data, subject to provenance and the information-available-before-forecast rule; no external variable is mandatory. |
| **A-25** | Neither poor standalone scores nor strong correlation with another method may be used to discard, deprioritise as a matter of principle, or make an experimental method ineligible for combinations. Correlation is descriptive reporting information. |
| **A-26** | Core ascending-number results and source-qualified **operator-labelled drawn order** are distinct views of the **same draws**. Never infer draw order from sorted columns, and never double-count rows as independent observations. |
| **A-27** | Acquisition is separate from modelling: use the accepted per-game versioned result masters, owner-run Lotterywest results-search updater, append-only ledger and atomic/versioned backups. Independent Lott verification is owner-hand-saved, not programmatic API scraping.
| **A-28** | The conventional independent-uniform model can calibrate *interpretation and instrument sensitivity* but is **never a gatekeeper** for method eligibility. Synthetic data/states are never genuine forecast inputs, although disclosed simulation-derived methodological learning is permitted. |
| **A-29** | The owner requires independent Claude review of ChatGPT-delivered code and governing documents under the agreed always-review list; owner alone controls ratification, reviewer latitude and DECIDED/RECOMMENDED/OPEN classifications.

| **A-30** | The project-charter document and the R1 research-catalogue document serve **separate, coordinated roles**. A research recommendation does not silently overrule later user-approved project policy; user agreement controls substantive changes. |
| **A-31** | Extend the available research space to 100 additional candidate methods; **keep every** `E_x` concept and variants, regardless of perceived implausibility, speed, poor results or inter-method correlation. |
| **A-32** | Add all six pilot-wave-inspired **mathematical** research candidates `E_57`–`E_62`, including the corrected guided-particle methods E_61/E_62, as eligible for **real-data** experiments. Their origin does not imply quantum physics is a lottery mechanism; identifiability results are diagnostic, **not** an exclusion rule. |
| **A-33** | The accepted masters retain the source-published number sequence. It is **operator drawn order assumed by owner decision** (`OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`), not separately verified physical order; retain source provenance and never infer order from numerically sorted labels.
| **A-34** | Initial scheduler capacity is configurable **1–6** separate method processes (six default and maximum), pinned single-thread numerical workers; higher capacity requires new owner-reviewed approval.
| **A-35** | Keep **computational benchmarking** separate from research scoring. Support `X` walk-forward targets (B1=1, B10=10), a configurable preceding-history length `W` (e.g., 100 or full), and exclude the frozen latest-ten holdout. Do not score or show benchmark predictions in timing reports. |
| **A-36** | Verify bit-identical canonical scientific outputs for one versus six workers and direct-versus-coordinated invocation with matching conditions; no default 12-worker criterion. Test exceptions require explicit owner review.
| **A-37** | Synthetic datasets may support disclosed design choices and null-world interpretation, but must remain separate in storage, fit state, prediction generation and scoring. Synthetic identifiability, null calibration and planted-effect outcomes must not be interpreted as a ban on real experiments. |

### 4.1 Boundary between agreed research policy and later choices

The proposals that follow include architectural suggestions, validation safeguards, reporting schemes, possible formulas, and research categories from the assistant. Unless they directly restate the above agreements, they are **proposed for consideration**. Their inclusion in a comprehensive proposal must not be mistaken for silent approval. The **provisional** nature of some D1/D2/D5 details means that implementation mechanisms and experimental formats remain reviewable even though the broad directions are endorsed.

The user subsequently clarified that simulations **may inform method design, practical feasibility, sensitivity analysis and interpretation**, provided those influences are transparent. What is prohibited is contaminating a genuine forecast with **artificial observations, fitted synthetic state, synthetic-only parameter estimates or scores masquerading as real data**. Synthetic results do **not** automatically qualify or disqualify methods. Parameters of an actual forecast must be estimated according to the real-data information-cutoff protocol. §§10.6–10.7 specify the operative safeguards. This paragraph supersedes stricter v0.2 wording.

---

### 4.2 External single-round review and disposition

A single invited Claude review proposed five decisions and several corrections. After assessment, the current disposition is:

| Review item | Disposition | Boundaries |
|---|---|---|
| **D1 — whole-pipeline reference and planted-effect simulations** | **Accept direction; execution details deferred** | Distinct synthetic data/states and reports, thousands of simulations permitted; **disclosed method-design and interpretive learning permitted**, no substitution of artificial observations/fit states/scores into genuine forecasts |
| **D2 — equipment metadata and drawn order** | **Accept investigative scope** | Published order is **owner-assumed operator order** (`OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`), not independently verified physical order; equipment details remain exploratory, not a dependency |
| **D3 — first qualifying draw 1144** | **DECIDED, accepted current master** | Include 19 and 26 April 2018; prohibit earlier configurations |
| **D4 — older Powerball-only history** | **Reject expressly** | Never bring different-rule-era records into the dataset, even for just the unchanged second barrel |
| **D5 — date-indexed external observations** | **Provisionally accept** | Keep an extensible interface; require information-time provenance; no obligatory feeds |

The independent review also highlighted sensitivity, the `E_2` recurrence-hazard formulation, common mathematical ancestry among apparently different models, and source-qualified drawn-order evidence. These are included as research design considerations, **not as grounds to narrow speculative method eligibility**.

### 4.3 Immediate software update and its limits

The current owner-run acquisition tools are `src/two_site_results_check_v0_7.py`, `src/results_master_v0_1.py`, and `Run_Results_Updater.bat`. Earlier standalone scraper tools are historical, not current authority.

## 5. The central experimental workflow

**Current training and numeric contract:** Each target N is fitted afresh on only eligible preceding draws, with `int64` internal and output integer arrays and `float64` floating arrays, and readonly isolated owned prefix views. The entire master may be SHA-256 hashed bytewise for integrity, but row N and later must not be parsed/converted; the whole-master hash must not determine model features, seeds or forecast content. Dates are optional and digest-bound when consumed; ordinary E_1 view digest stays unchanged. Automatic dependency install-and-upgrade is retained, but requires offline suites and golden/boundary checks to PASS before further work, and is prohibited between freeze and score or within Mode H. Incremental fit caches require reviewed byte-identical equivalence to scratch fit.



### 5.1 Retrospective prediction: draw `N` using draws before `N`

Let the available, validated history be numbered chronologically from the oldest eligible draw `O` through the most recently observed draw `L`.

For any historical target draw `N`:

1. Construct the training information from `O` through `N-1`, with **no data from `N` or later**.
2. Fit or update a method using only that eligible information.
3. Generate its ranked candidate main numbers, candidate Powerball numbers, and selected draw prediction for `N`.
4. Save the prediction and metadata before evaluating it.
5. Reveal the known actual result for `N` to the evaluation component only.
6. Score and report predicted versus actual outcomes.
7. Advance the simulated time by one draw and repeat for later eligible `N` values.

This is **expanding-window walk-forward validation**. The method is refitted, or its internal state is updated, at each step as it would have been when operating in real time.

An approach using a rolling rather than expanding historical window may itself be an experimental design choice, to be investigated without looking ahead.

### 5.2 Meaning of the “last 10” concept

The user’s original example: for each of the last ten already-completed draws, pretend that the target draw has **not yet happened**, use all data preceding it, make the next-draw prediction, and compare it with its actual result.

For an illustrative retrospective evaluation, choose pre-quarantine development targets in the corresponding game and refit independently through each target N−1; do not incorporate the August 2026 quarantined outcomes.

**Important reconciliation with the holdout rule:** The **latest ten** are reserved for the **final evaluation**, so during method-development iterations the analogous walk-forward experiments should target *earlier* historical draws. The reserved last ten are run **only after the method design and selection rules have been frozen for that evaluation**. This honours both the “last 10” idea and the agreement not to contaminate the final evaluation set.

### 5.3 Configurable evaluation lengths

Ten retrospective predictions are useful for inspection and quick regression tests, but produce highly uncertain comparative rankings. The eventual evaluator should support a configurable number of targets (for example, 10, 50, 100, or a longer admissible sequence), restricted to the appropriate development/evaluation region.

The choice of sample size, initial minimum training history, and computational budget is **not yet settled**.

### 5.4 Development period, reserved final ten, and next-draw operation

Three circumstances must remain explicitly separate:

**Mode D — Research and development:** Experiment on historical draws that precede the latest-ten holdout. Develop methods, explore parameters, compare methods, and propose combinations *without reading holdout outcomes for selection*. The complete CSV may be loaded operationally, but the prediction/tuning code must enforce the permitted chronology.

**Mode H — Reserved final evaluation:** Once an evaluation plan has been fixed, run eligible methods on the ten reserved draws in historical order. Each simulated prediction for a holdout draw sees only the preceding draws (possibly including earlier holdout draws that would already have been observed at that simulated date), but **the user must not repeatedly tune to those final results while continuing to call them untouched**.

**Mode P — Actual next-draw prediction:** At the user’s instruction, fit the selected methods to **every completed draw then available**, including the previously reserved latest ten, and publish the forecast *before* the real next draw takes place. Record the exact information cutoff and do not revise that recorded forecast after its outcome is known.

### 5.5 A moving holdout needs governance

The phrase “latest ten draws” moves as new draws are published. Proposed policy:

- Record the exact draw numbers and CSV snapshot that constitute a **specific evaluation holdout**.
- Keep that designated holdout fixed while a research/evaluation cycle is underway.
- Once the holdout has been used for choosing/tuning methods, do not describe it as independently untouched again.
- A newly accumulating future set can serve as a later prospective evaluation set.
- Avoid retroactively redefining which ten draws counted as “final” to favour particular results.

These operational details are **recommendations** for later approval, not a modification of the agreed ten-draw reservation.

### 5.6 Genuine future prediction

A real forecast is the strongest practical form of the experiment because its target is not yet observed. The program should save a timestamped, immutable or append-only record stating:

- Predicted draw number/date and the latest data draw used.
- File digest, dataset coverage, method IDs and versions, parameters, any randomness seeds.
- Individual methods’ rankings and combined selected numbers.
- Any method-combination or weighting policy version.
- A timestamp demonstrating the prediction preceded the reported real draw.

When the real result becomes available, add the outcome and evaluation as a **separate record**, preserving the original prediction.

---

## 6. Two-barrel modelling and the form of predictions

### 6.1 Separate modelling targets

The primary predictive targets are:

1. **Main-barrel inclusion:** rank numbers `1`–`35` for inclusion in the next **seven-number set**.
2. **Powerball result:** rank numbers `1`–`20` for selection as the next Powerball.

The method may use a coherent statistical model that represents number interactions; it must nevertheless return distinct main-barrel and Powerball assessments. Any future proposal to use cross-barrel historical patterns as explanatory *inputs* should be considered openly, but it must not accidentally conflate their output spaces.

### 6.2 Required common output concept

Each experiment should, where applicable, provide:

- An ordered ranking of all 35 main-ball candidates.
- An ordered ranking of all 20 Powerball candidates.
- The selected **top seven distinct** main numbers and **top one** Powerball.
- Scores explaining its ranking; calibrated probabilities only if those probabilities have a defensible meaning.
- The history cutoff and fitted configuration.
- An explanation of what the scores mean, or an explicit indication that they are uncalibrated relative scores.

A method that naturally produces only partial rankings, a distribution over full seven-number sets, or an anomaly signal could still be accepted: the shared interface may need an adapter or a declared alternative output type. **Do not discard a potentially useful method merely to preserve an overly rigid software interface.**

### 6.3 Important order and dependence issues

- `Ball_1` … `Ball_7` in the **ordinary ten-column CSV** are **ascending/storage positions**, not draw-order positions. The **separate operator-labelled drawn-order CSV** supplies that additional observation; a model must not infer that `Ball_1` of the ascending CSV was physically drawn first.
- Seven main numbers are distinct within a draw. Selecting independently highest-scoring numbers is straightforward, but models of **whole combinations** may require joint scoring to respect interactions between included numbers.
- A frequency-based probability for one number and a probability for an entire seven-number combination are not interchangeable.
- Ties must be resolved reproducibly or with a declared and recorded random seed.
- **One common R2 observation policy** should govern whether a method consumes an unordered set, an operator-labelled ordered sequence, or both; these are two views of one draw, not independent extra observations. The policy applies to all mathematically compatible methods, without automatically creating an `E_x` duplicate for each data view.

---

## 7. The initial six user-proposed experimental methods

The identifiers and descriptive titles below are a **proposed initial registry**; the underlying six ideas are agreed, but formal mathematics, exact ranking direction, hyperparameters and tie-breaking still require design review.

### E_1 — Historical Appearance Frequency

**Core question:** Have numbers drawn more often in the observed history tended to be drawn more often subsequently?

For each eligible historical interval, count how many draws contain each main number and how many times each Powerball value appeared. Convert counts to percentages or comparable scores and rank candidates, initially favouring the most frequently observed values.

**Potential variations:** Full-history frequencies; recent-window frequencies; decayed frequencies; smoothed frequencies; Bayesian shrinkage; frequency changes over successive periods.

**Interpretation caution:** Frequency differences will occur even when draws have identical underlying probabilities. Unequal sample counts are observations, not on their own evidence of unequal future probabilities.

**Standalone status:** Simple, directly testable baseline and potentially useful component of future ensembles.

### E_2 — Expected Recurrence-Interval Alignment

**Core question:** Which numbers are approaching their own characteristic or optimal recurrence interval **in the next draw**?

For each number, obtain historical gaps between its successive appearances. Estimate one or more characteristic intervals, then compare the projected age of the number **at the target draw** with that interval.

**Critical agreed interpretation:** This is **not** merely “choose whichever numbers are most overdue.” A number may rank most highly when its next-draw age is **near** its fitted characteristic interval, even if other numbers have been absent for longer.

Illustrative possibility — not an approved formula:

- If a number typically recurs at an interval of about five draws and the last appearance was four draws before the proposed next draw, its interval-alignment score might be high.
- Alternatives might use the mean, median, mode, robust centre, a fitted waiting-time likelihood, a harmonic/seasonal recurrence model, or individual multiple characteristic intervals.
- A sensible experiment could compare a **peak-at-the-expected-interval** formulation against an **overdue** formulation as separate parameterised variants or distinct method IDs if conceptually different.

**Technical question to settle:** Whether to measure the interval in draw-number differences, the count of intervening nonappearances, or projected target-draw age. These are offset by one; the chosen convention must be unambiguous and tested.

**Interpretation caution:** Under an ideal independent model, a past absence does not increase or decrease a number’s next-draw inclusion probability; the present experiment tests whether actual data depart from that model or exhibit useful structure.

### E_3 — Occurrence-Curve Endpoint Forecast

**Core question:** If each number’s appearance history is represented as a binary time series, do fitted curves predict which numbers are most likely to appear next?

Represent each draw as `1` if a candidate number appears and `0` otherwise. Fit a curve or time-series function to that historical sequence, and **evaluate it at the next, unobserved draw**, not merely at the last observed draw. Rank numbers by the resulting next-step forecast score.

**Possible families to research:** Polynomial and spline smoothing; constrained smooth curves; regularised regression; local regression; harmonic fits; parametric curves; state-space models and other nonlinear curve fitting.

**Critical safeguard:** A fitted curve can easily interpolate noise and produce edge artefacts. Any tuning of curve family, order, smoothing strength or fit window must respect the walk-forward training boundary.

**Status:** Legitimate as an experiment. Its mathematical fit quality on the training history is **not** proof of next-draw predictive ability.

### E_4 — Occurrence-Curve Gradient Forecast

**Core question:** Does a positive or increasing *slope* in each candidate’s fitted occurrence curve signal a higher probability of appearance at the next draw?

Fit a curve to each candidate’s prior binary sequence, estimate its derivative/gradient at or approaching the forecast point, and rank by an agreed direction and magnitude of the predicted trend.

The endpoint value in E_3 and the derivative in E_4 carry different information and should remain independently testable, even if they share curve-fitting utilities.

**Possible extensions:** First and second derivatives, rate-of-change normalisation, local versus global slope, robust smoothers, slope confidence/stability, and slope-plus-level combinations (which would become separate combination methods).

**Cautions:** Gradients of fits to short, noisy binary series can be extremely sensitive to model order and boundary choice. A rising fitted curve need not continue rising in the next unseen draw.

### E_5 — Shared Population/Draw Distribution Model

**Core question:** Can one selected statistical distribution or stochastic model for the **population of candidate numbers** support meaningful next-draw probability/ranking estimates?

Identify appropriate *discrete* sampling or probability models for the observed phenomenon. Fit their parameters using eligible historical data and derive next-draw rankings separately for the main and Powerball barrels.

**Candidate mathematical constructs to research:** Categorical/multinomial families (for Powerball), finite-population selection structures (for main-ball sets), hierarchical Bayesian models, models of heterogeneous inclusion probabilities, temporal mixtures, and variants that allow drift or dependence.

The question is **not** “which arbitrary continuous curve fits a histogram best?” A Gaussian is usually inappropriate as a literal model for numbered-ball categorical draws, although continuous functions might legitimately appear in an auxiliary smoothing or latent-variable model.

**Cautions:** Distinguish fitting the historical marginal frequency distribution from fitting a predictive *time-conditioned* model. One distribution across the 35 main numbers does not by itself account for the seven-without-replacement structure.

### E_6 — Per-Number Fitted Distribution Models

**Core question:** Can a different estimated distribution or waiting-time process for **each number** yield next-draw ranking information missed by a shared model?

For each candidate number, estimate its historical inclusion process and fit candidate distributions or stochastic process models. Use each model to estimate a next-draw score, propensity, hazard, or appropriately defined appearance probability.

**Candidate constructs to research:** Bernoulli/Beta-Bernoulli models, geometric waiting times, discrete survival/hazard models, renewal processes, mixtures, time-varying inclusion probabilities, and per-number latent states.

**Cautions:** The observation count per number is small. Flexible distribution fitting can badly overfit; an apparent “best distribution” chosen after inspecting many alternatives is itself a selection process that must be tested outside its fitting observations.

### 7.1 No premature verdicts on the six methods

All six will be preserved as distinct conceptual starting methods. They are **not guaranteed to be equally predictive**, and some may turn out to be mostly descriptive or systematically misleading. That possibility does not justify deleting them or preventing their use in later combinations.

### 7.2 Design questions still open within these methods

- Historical fit horizon: all available prior draws, a sliding window, or multiple horizons?
- Which summary statistics and model families are compared?
- Whether scores are raw, normalised, or calibrated as probabilities?
- How are tied scores handled?
- Does an algorithm train one independent model per number or a coordinated multivariate model?
- How do we distinguish a new experimental method from a parameter variant or version change?
- Which outputs are useful to preserve for later ensemble studies?

Those matters must be resolved in the detailed experimental-method design, not silently decided in the first implementation.

---
### 7.3 Refinement of E_2 and relationships among E-methods

**E_2** retains the user’s original *next-draw alignment with a characteristic recurrence interval* as its primary definition. A general **gap-dependent occurrence hazard** is a further candidate parameterisation, permitting peaked, decreasing, rising, bimodal, or irregular dependence on elapsed time since last appearance. A flat hazard describes the conventional reference; it is a comparator rather than an exclusion principle. Mode, median, mean, quantile, robust fitting and fitted gap distributions may each imply different candidate forecasts, and these differences should be recorded as distinct evaluated variants. None is assumed superior before testing.

Several proposed approaches may be mathematically related—for example, decayed frequencies, smoothed occurrence-curve extrapolations and some conjugate-probability updates can all produce different weighted summaries of recent binary history. **Method-family labels, ranking correlation and error-correlation analyses are desirable as reports, not as deletion, implementation-deprioritisation or ensemble-ineligibility rules.** Subtly distinct related methods may still produce useful conditional or ensemble information. Any suggestion of inversion or combination must be tested under its own independently recorded definition.

## 8. Research programme and completed R1 catalogue — up to 100 additional candidates

### 8.1 Agreement on scope, not pre-selection of winners

A separate **R1 method-discovery and literature-research phase** has now produced the current **62-candidate catalogue**: the six original E_1–E_6 and **56 additional E_7–E_62**, including the pilot-wave-inspired mathematical family E_57–E_62. The user’s subsequently expanded scope permits **up to 100 additional experimental candidates beyond the original six** (potentially E_7–E_106 if worthwhile). “Up to” is **not a quota** and does not require implementation of all candidates.

Research should not be confined to literature specifically about lotteries or gambling. Useful approaches may come from research on noisy measurements, randomness testing, signal processing, state estimation, change detection, dynamical systems, information theory, time series, nonlinear statistics, machine learning, complex systems, and speculative research traditions.

**R1 v0.4 documents research already conducted and references already collected**, not implementation or evidence of predictive merit. Candidate identities and mathematical variants remain subject to detailed R2 review. This charter establishes research openness and governance, not a list of authorised code changes.

### 8.2 Research domains to explore

The following are **research domains** represented by or available to extend the current R1 catalogue; the definitive individual *research candidate* descriptions and `E_x` mappings are in R1 v0.4:

1. **Classical and modern probability:** frequency models, exact distribution tests, nonuniform categorical outcomes, occupancy models, hypergeometric structure, exchangeability and deviations from exchangeability.
2. **Bayesian inference:** hierarchical pooling, Dirichlet-type priors, posterior predictive ranking, dynamic Bayesian models and uncertainty-aware shrinkage.
3. **Recurrence and renewal theory:** waiting times, hazard functions, survival analysis, multiple recurrences and slowly changing return-time structure.
4. **Time-series analysis:** lagged dependence, autoregressive ideas adapted to categorical/binary data, seasonal/harmonic models, exponentially weighted updates and state-space forecasting.
5. **Curve fitting and signal processing:** low-/high-pass effects, splines, polynomial or rational approximations, regularisation, wavelets, Fourier components, spectral peaks and adaptive filtering.
6. **Nonlinear dynamics and chaos:** phase-space embeddings, nonlinear prediction, surrogate-data tests, Lyapunov-related diagnostics, recurrence quantification and sensitivity to initial conditions, *subject to their assumptions and severe short-data limitations*.
7. **Information theory:** entropy, conditional entropy, mutual information, transfer entropy, compressibility, minimum description length and information shared among lagged observations.
8. **Randomness testing and change detection:** runs tests, serial-dependence tests, autocorrelation, cumulative-sum methods, changepoints, distribution drift and other diagnostics repurposed carefully for forecasting.
9. **Combinatorics and inter-number structure:** historical co-occurrence, pairs and higher-order sets, conditional inclusion models, interaction graphs and structured multi-label rankings.
10. **Machine learning:** regularised classifiers, tree-based learners, gradient-boosting variants, kernel methods, ranking methods and other algorithms adapted to the limited dataset.
11. **Sequence and pattern mining:** motifs, symbolic dynamics, subsequence similarity, nearest-neighbour histories, Markov-style transitions and history-pattern lookup.
12. **Latent-state and regime models:** hidden Markov ideas, switching models, mixture-of-experts and models that posit changing hidden conditions.
13. **Ensemble methods:** equal-weight models, tuned mixtures, stacking with strictly historical training, confidence-aware selection, diversification and contrarian components.
14. **Meta-learning and adaptive algorithm selection:** context-dependent choice among predictors, cautious online reweighting and explicit testing of whether performance regimes repeat.
15. **Speculative / uncommon constructs:** unconventional transforms, cross-scale periodicities, numerological-like transforms treated as falsifiable hypotheses rather than established mechanisms, synchrony ideas, non-obvious temporal alignments and other approaches that can be precisely operationalised and prospectively tested.

These categories intentionally overlap. Cross-disciplinary and apparently unlikely approaches are welcome where they can be made into coherent tests.

### 8.3 Research record for each candidate

For each candidate approach, R1’s catalogue records or future additions should provide:

- A permanent *candidate* research reference until an `E_x` implementation ID is granted.
- A short, understandable name and a concise plain-English explanation.
- Its source discipline and, where available, relevant papers, books, documentation or credible analyses.
- The hypothesised informative signal and the assumptions the technique **makes or challenges**.
- Mathematical formulation or enough detail to make one possible.
- Required data and what the existing CSV can/cannot supply.
- Expected computational and software requirements; potential Python package dependencies.
- Whether it predicts main numbers, Powerball values, full combinations, or a meta-score.
- Potential sources of misleading apparent success (e.g., overfitting, circularity, high model flexibility, multiple tests).
- Proposed methods for checking whether any advantage is reproducible or merely coincidental.
- Classification: established method applied speculatively, technically coherent exploratory proposal, insufficiently specified hypothesis needing development, or mathematically unsound *as currently formulated*.
- Recommendation for priority, **without deleting or disqualifying the concept from the project record**.

### 8.4 Meaning of “sensible or gibberish”

The user has asked for plain-spoken advice about whether an idea makes sense. The response should be frank **without using convention as a substitute for analysis**. Suggested labels:

| Label | Meaning | Action |
|---|---|---|
| **Well-defined and mathematically coherent** | A clear calculation and a testable forecast exist; predictive success still unknown | Eligible to implement and test |
| **Speculative but testable** | The causal rationale is uncertain or unconventional, but a non-leaking experimental prediction can be defined | Eligible to implement and test |
| **Under-specified** | An interesting notion has no unique forecast or measurable rule yet | Refine the idea; retain record |
| **Mathematically inconsistent or circular** | The current formulation contradicts its own rules, uses future outcomes, or defines success retrospectively | Flag precisely; seek a corrected formulation; retain record |
| **Empirically ineffective so far** | Properly tested, with no convincing out-of-sample advantage | Rank/report accordingly; **do not discard** |

No one category is a permanent verdict on the possibility of alternative formulations or combination value.

---

### 8.5 R1 candidate catalogue handoff and pilot-wave-inspired family

**Current catalogue:** E_1–E_62, including 56 additional candidates beyond the original six. The exact explanatory text, references and method-specific constraints reside in R1 v0.4; this proposal **does not duplicate all 62 methods** or silently make their current formulas binding. Its job is to preserve their eligibility and control how specifications are approved.

The six currently catalogued pilot-wave/**Bohmian-inspired** methods are:

| Research ID | Candidate idea | Status and crucial qualification |
|---|---|---|
| E_57 | Fixed-Size Determinantal Seven-Set Model | A seven-subset interaction model (symmetric positive-semidefinite kernel); **not** synonymous with sequential Wallenius weighted sampling; main barrel chiefly. |
| E_58 | Unconditioned Coupled Latent-Wave Field | Hidden coupled oscillatory propensities; needs a separately valid seven-without-replacement selection mechanism. |
| E_59 | Draw-Conditioned Coupled Latent-Wave Field | Related latent field updated from actual observations available before each prediction. |
| E_60 | Post-Change Non-Equilibrium Relaxation Analogue | Models changing/relaxing departures after detected or documented regime changes; apparatus details optional. |
| E_61 | Guided-Particle Circulation | Latent trajectories with shared guiding field, possible one-dimensional **order preservation**, separately specified valid capture likelihood and testable recurrence/association patterns. |
| E_62 | Guided-Particle Circulation with Reinjection | Outcomes can change hidden particle states through a defined reinjection rule; its hypothesis differs from E_61. |

These are models intended for **real eligible-era draw data**, not synthetic-only demonstrations. Synthetic identifiability testing is informative, not an implementation/eligibility gate. R1 records the correction that an exact node-free guidance reference requires precise coefficient and node conditions; regularised, noisy, different-dimensional or different-feedback variants are distinguished rather than confused with that reference. The **analogy** to de Broglie–Bohm theory gives no evidence of a quantum process in the draw machine. None of these facts prejudges empirical outcome.

Method correlation, expensive inference and absence of apparatus labels cannot delete, exclude or categorically deprioritise any candidate. R2 should determine the practical scope of each implementation, with separate permanent identity for materially changed hypotheses and version/variant metadata for compatible changes.

## 9. Permanent method retention and evolving qualification

### 9.1 Non-negotiable retention policy

**All experimental methods stay in the project.** A method is never deleted, silently hidden, or stripped of its identity solely because it is low-ranked, unorthodox, negative, unstable or apparently unsuccessful.

Retained material should include, as practicable:

- Its `E_x` ID and descriptive name.
- Its mathematical or procedural definition, parameters and historical rationale.
- Implementation source and version history.
- Available individual predictions and complete rankings/scores.
- Historical evaluations, including negative results.
- Dependency and environment information.
- Notes on known defects, methodological caveats and corrections.
- Its use as a component of any subsequent combinations.

The report interface may sort, filter, abbreviate or fold items for readability, but the persisted registry must preserve all methods and make the entire catalogue available on request.

### 9.2 Low performance does not imply zero combination value

A weak individual signal might still contain useful **complementary** information. For example, it might:

- Make errors on different draws than another method.
- Identify a subset of numbers another method systematically undervalues.
- Provide a regime or anomaly indicator.
- Be informative *inverted* or down-weighted, if that rule is independently tested.
- Become useful only when conditional on some other historical characteristic.
- Reduce variance or diversify a group of strongly correlated predictors.

Conversely, combinations can look better simply because enough alternatives were tried until one happened to fit the sample. Both possibilities must remain visible.

### 9.3 Changing qualification rules

The user's agreed policy permits qualification methods to **change over time** in response to recommendations and subsequent discussion. Possible later criteria could consider standalone score, score stability, uncertainty, diversity of errors, complementarity, rank correlation, calibration, computational cost, reproducibility or particular historical regimes.

Any such eligibility or weighting rule must be **named, versioned, justified, and identifiable in reports**. It may be revised with the user's agreement. The project should preserve earlier rules and results for auditability rather than silently rewriting the past.

### 9.4 Combination experiments get their own identities

An ensemble, weighted sum, voting procedure, learned selector, conditional combination, anti-correlation inversion or other multi-method construct is itself a distinct experiment and should be assigned a **new permanent `E_x` identifier**.

A combination's identity should specify its components, their versions, score normalisation, weights/rules, tie-breaking, training period and evaluation conditions. Changing these in a materially different way may require either a version change or a separate method ID, per a later-agreed registry policy.

### 9.5 Protecting combinations against hindsight bias

The system should not select and weight a combination by looking at the *same* target draw outcomes on which it then claims an unbiased improvement. Candidate weights or membership rules must be chosen using data available *before* the evaluated draw, with a suitably separate evaluation stage when practical.

This safeguard does not prevent unlimited speculative experimentation. It ensures we can recognise whether a striking score is a genuine forecast or merely a retrospective construction.

---

### 9.6 Correlation must not determine eligibility

Related methods can agree almost perfectly overall and still disagree on unusual periods or boundary cases; disagreements may matter. Maintain all methods, preserve their individual outputs, and allow all of them into selection and ensemble experiments. A method-family label is **metadata**, not a filter, a ranking penalty or an implicit vote against an approach. Any mathematical concerns about duplicate evidence are to be reflected when *interpreting results*, while methods remain implemented and available.

## 10. Evaluation, scoring and interpretation — principles agreed; specifics deferred

### 10.1 Why this section is provisional

The user has explicitly agreed to discuss detailed testing, scoring and method-comparison choices **later**, after considering the research and experimental approaches. Consequently, **nothing in this section establishes a ratified scoring formula, leaderboard policy, threshold or proof standard**. It documents issues that a rigorous design will need to address.

### 10.2 Candidate direct-result measures

Possible elementary observations include:

- Number of correctly predicted main numbers, from `0` to `7`.
- Whether the predicted Powerball was correct (`0` or `1`).
- Joint outcome: the distribution of main-number matches alongside Powerball accuracy.
- Performance averaged or accumulated across historically simulated target draws.
- Rank position assigned to each actual drawn number.
- Quality of a complete ranked list rather than just its top chosen numbers.
- Proper scoring of declared probabilities, if a method actually generates meaningful probabilities.
- Stability of method performance across multiple non-overlapping historical periods.

### 10.3 Reference behaviour and uncertainty

A useful reference is a correctly implemented predictor that selects seven distinct main numbers uniformly from `1`–`35`, and a Powerball uniformly from `1`–`20`.

Under the standard fair-independent **reference** model:

- Expected number of main-number matches per predicted seven-number set: **1.4**.
- Probability of a correctly predicted Powerball: **5%**.
- The probability distribution for the number of main matches follows a **hypergeometric** law, not a binomial model treating the seven chosen numbers as independent.
- A Powerball top-one match indicator has the reference Bernoulli probability `0.05` per draw.

These are **reference-model calculations**, not declarations that alternatives are impossible.

A ranking outperforming the reference on only ten draws is inherently uncertain. The precise inference method, including treatment of temporal correlations, multiple comparisons, changing rules and repeated method selection, remains for subsequent design.

### 10.4 Multiple experiments and the look-elsewhere effect

With six initial methods, up to fifty more proposals, many fit variants and potentially hundreds of ensembles, there will be many opportunities for attractive but accidental findings. The project must **preserve and investigate surprising winners**, while recording how many candidate models, windows, weightings and decision rules were attempted. Otherwise the most successful-looking model can be a selection artefact.

Reporting an empirical effect size alone is different from demonstrating that the effect is unlikely under chance. Both deserve attention.

### 10.5 Negative, anomalous and apparently contradictory findings

Do not “tidy away” negative results. Reports should be able to identify:

- Methods that underperform the reference.
- Methods that predict well in one historical block and poorly elsewhere.
- Methods with unusually high scores but unstable rankings.
- Methods that are strongly correlated with one another and therefore add little independent information.
- Methods with opposite signals that could become useful in a contrarian or mixture approach.
- Diagnostics suggesting data integrity or implementation errors rather than a real effect.

These observations contribute to the experimental record even if no winning predictor results.

---

### 10.6 Synthetic research and calibration — separately executed, permitted to inform disclosed design

**Current rule:** synthetic diagnostics may inform disclosed design but their data, fitted states and outcomes never enter real fit, forecasts or scoring. See R2 §1 and R3 §9.

**S-01 — Real-data information boundary.** When making a prediction for real draw N, only authentic, eligible-era observations and other expressly permitted real-world facts **available before N** may enter real-data fitted state, learned weights and direct forecasting computations. Synthetic histories, synthetic-fitted latent states, artificial forecast outcomes and synthetic-only scores must not be substituted for real observations or real fit states.

**S-02 — Physical and logical separation.** Null-world and planted-effect experiments use explicitly marked synthetic inputs, jobs, manifests, outputs and reports. They may share reliable numerical *code* and pure mathematical utilities with real-data methods; **synthetic generated records and learned synthetic states must not enter the real-data training/prediction path**. Keep distinct results and avoid pooled performance tables that confuse artificial and actual observations.

**S-03 — Allowed learning from simulations.** Findings **may inform disclosed choices** about model-family design, mathematically valid likelihoods, optimisation algorithms, parameterisation, research priority, sensitivity, robustness, error interpretation and computational implementation. Such choices must be recorded. A design informed by simulation is **not** a claim that the simulated effect exists in reality; fitting parameters and choosing real-world forecasting configurations must obey the eventual real-data walk-forward, model-selection and holdout protocol. No invisible synthetic-trained state or parameter may be imported into a real forecast.

**S-04 — No automatic gate.** A method that fails a null-world, planted-effect, recovery, identifiability or diagnostic test is **retained** and remains eligible for investigation with real data and combinations. Record the failure beside any apparent real-world success so its interpretation is not overstated. Synthetic tests measure properties of the specified generator/instrument, not all possible structures in reality.

**S-05 — Interpretation uses a reference ruler, not a veto.** Null-world outputs may help quantify how unusual a real score looks under a precisely defined artificial mechanism, including any search across variants or ensembles. Planted effects can measure ability to detect certain constructed signals. Neither assumes all reality is constrained by the generators. A good synthetic forecast is **not** an actual lottery success.

**Illustrative separate calibration programme, not yet a binding set of scores:**

1. Independent-uniform same-format history generator (7 distinct from 35 and 1 from 20).
2. Deliberately biased inclusion and unequal-selection mechanisms.
3. Recurrence-specific synthetic dynamics (including characteristic-interval peaks).
4. Periodic, regime-switching, wave-field, coupled-state, nonlinear and conditional-feedback generators.
5. Whole-pipeline null-world and planted-effect runs which expose the impact of trying many methods, variants and combinations.
6. Identifiability diagnostics comparing hidden-state recovery, ranking/probability prediction and numerical repeatability **separately**.
7. Thousands of replications where informative and computationally feasible, with independently derived task seeds.

Under the ideal independent model, the expected main-set overlap for a seven-number prediction is 1.4, with standard deviation approximately 0.96. These are **reference assumptions** used to understand a test instrument's sensitivity and limitations, never to pre-empt exploration of unexplained real-world structure. Specific prediction scores and evidence thresholds remain deferred to R3.

### 10.7 Reporting, auditing and contamination safeguards

Real-data reports record authentic data snapshot, temporal cutoff, prediction methods and configurations, original forecasts, actual outcomes and evaluation status. Synthetic-only reports record generator, artificial effects, seeds, sample size, algorithm revision and appropriate synthetic results. A combined *interpretive* narrative may compare conclusions **with origins clearly labelled**; never pool observed and artificial results into one predictive leaderboard.

An implementation should reject attempts to mix source types inadvertently and test that **altering synthetic data files does not change a fixed real-data forecast when real inputs, the agreed method definition and configuration are held constant**. That test does **not** prohibit consciously documented later design revisions that were motivated by simulation findings; such revisions have new version/configuration provenance and must themselves pass proper real-data evaluation.

**No predictive-score feedback from benchmark mode:** Computational benchmarking may generate internal predictions solely to check deterministic equality, but its public report carries resource use, failure/status and output equality digests—not matches, winning numbers, per-ball ranks, prediction comparisons or scores used to decide model merit. (§12.8.)

## 11. Data integrity, leakage prevention and provenance

The accepted versioned per-game master replaces the original two-file observational arrangement. R2 §2–4 is the normative home for strict row-first filtering, view kinds, source ownership, sealed prefixes and date digests. See §0 for current hashes and boundaries.


### 11.1 Validation on loading

The research program should reject, quarantine, or explicitly flag data inconsistent with the selected era:

- Missing or duplicate draw identifiers.
- Missing, repeated or nonchronological draw dates where regularity is expected.
- Unexpected gaps in the draw-number sequence, subject to verified exceptions.
- Main values outside `1`–`35`, duplicate main numbers in a draw, or other violations of the seven-number set definition.
- Powerball values outside `1`–`20`.
- Empty fields or inconsistent CSV row widths.
- Conflicting records for the same draw across retrieved files.
- Source-format or game-rule changes that require a separate dataset era.

If a per-game results-master validation or update fails, preserve the previously accepted master/ledger identity and STOP scientific use of the affected candidate version; the owner-run master updater has create-only and ledger-backed recovery policies.

### 11.2 Source checking

Published results and third-party cross-checks are observations, not an oracle; owner-run source checking provides independent evidence.

The accepted results-master tool preserves prior versions, backups, verification and hashes before any promotion; do not replace this with the retired scraper.

### 11.3 Temporal leakage prevention

A run targeting draw `N` must not access:

- The actual winning numbers of draw `N` or any later draw during forecast generation.
- Histograms or other summaries computed over future-inclusive data.
- Curve-fitting coefficients fitted on all available draws when the simulated target was earlier.
- Feature scales, hyperparameters, method weights, or feature selections that were tuned after examining the target's actual result, unless clearly labelled as a non-independent exploratory analysis.
- A “best-of-many” method choice based on the holdout results while still representing the same holdout as untouched.

Simple tests should deliberately inject distinctive future data and verify that earlier predictions are **bit-for-bit or logically unchanged**.

### 11.4 Historical corrections

A historical draw result might be corrected or an acquisition source might change. Maintain data snapshot identity and allow a run to be reproduced against its original snapshot. A correction should generate new evaluation artefacts with a new provenance record rather than silently rewriting old reports.

### 11.5 Operator-labelled drawn order — qualified observation, common R2 policy

The accepted master includes a source-published main-number sequence and one drawing per row. `UNORDERED_SET` derives an ascending copy; `OPERATOR_DRAWN_ORDER` is the owner-assumed source-published sequence. The earlier date-stamped sorted/order CSV pair remains historical provenance only, not two samples and not the active source.

**Historical note:** Prior Proposal v0.3/v0.4 and protected R1 quote a post-quarantine draw as drawn-order evidence; those passages remain historical and are disclosed in `HOLDOUT_EXPOSURE_RECORD_v0_1`. They are not repeated in this current charter.

**The former “reported order is provisional” statement is superseded.** The source is sufficiently labelled for the project's normal **drawn-order** analyses, with provenance and qualification visible in the source/data manifest; optional broadcast checks remain a useful enhancement, **not an eligibility gate**.

The extra sequence may enable early-versus-late extraction-position hypotheses and simpler ordered sequential-selection likelihoods for compatible methods. Other models may inherently predict only **unordered sets**. R2 must specify **one cross-method policy** for source qualification, information-cutoff rules, ordered versus unordered observation/likelihood, and the fact that an order-sensitive model is not necessarily interchangeable with a set-only model. Do not force a mathematically unordered method such as a fixed-size determinantal set model to use order; do not create a different E-number merely because compatible methods evaluate both standard data views.

### 11.6 Optional equipment metadata and other observational channels

Some physically grounded hypotheses may concern distinct machines, ball sets, replacements, maintenance or operating conditions. Sources and reliable per-draw identifiers are **not yet established**. Their absence is not a reason to block the project or disadvantage nonphysical hypotheses. Reserve extensibility but do not fabricate apparatus labels or treat secondary equipment claims as proven facts.

### 11.7 Optional time-indexed external observational data

Exploration of environmental, synchrony, cross-game, indirect or seemingly unrelated temporal hypotheses may eventually require other datasets. Any proposed feed must identify its own provenance, timestamp semantics, latency, access conditions, changes and missing intervals. Most importantly, a predictor pretending to forecast draw N must only receive information actually **known before draw N**. An event timestamp is not necessarily its publication timestamp. Propose data feeds as candidates during research rather than silently introducing them now.

---

## 12. Proposed Python 3.14 design

### 12.1 Software philosophy

Aim for **clarity, reproducibility, modularity, traceability and extensibility** rather than a large monolithic collection of scripts. The historical record is small in memory, but some proposed methods are computationally intensive; begin with simple measurable parallel execution and benchmark before adding specialised acceleration. Scientific rigour, comprehensible implementations and reliable timing matter more than premature optimisation.

The user suggested `Powerball_Predictor_v001.py`, with each `E_x` as a separate function (possibly assisted by subordinate functions), plus shared top-level utilities. That remains the initial preferred interface. Splitting into packages or separate experiment modules is an **optional future architecture** if a single file becomes unwieldy; do not treat it as already approved.

### 12.2 Illustrative conceptual components

1. **Configuration and run controller:** Select dataset, time cutoff, mode (development, reserved final evaluation, live forecast), target range, experiments and parameters.
2. **Data loader / validator:** Read compatible-era CSV, canonicalise dates and unordered seven-number sets, optionally join source-qualified **operator-labelled drawn order** as the same draw’s second observation view, verify integrity, and supply immutable chronological records. Reject earlier-rule-era records even if Powerball fields alone appear compatible.
3. **Experimental registry:** Map `E_x` IDs and names to implementations, versions, dependencies, parameters, documentation and output adapters, retaining all 62 current research candidates for eventual R2 specification without assuming they are all already coded.
4. **Shared mathematical utilities:** Counts, recency, gap histories, indicator matrices, numerical fitting, tie handling and careful probability operations.
5. **Individual predictors:** Separate implementation entries for E_1, E_2, etc., with no side effects on each other's data.
6. **Historical walk-forward engine:** Construct permissible training ranges and simulate one future draw at a time.
7. **Combination engine:** Invoke registered methods and combine their historical-only outputs under separately registered `E_x` rules.
8. **Evaluation engine:** Compare stored predictions with actual outcomes, calculate agreed scores and uncertainty.
9. **Reporter:** Produce digestible summaries and full machine-readable results, including low-ranked and highly correlated methods. Keep real-data reports strictly separate from every synthetic report.
10. **Provenance / audit recorder:** Capture source data identities, method/config versions, Python/package environment, seeds and declared simulation-informed design changes. Keep synthetic records/fit states/scores out of real forecasts.
11. **Computational benchmark and process-pool controller (proposed):** configurable worker pool, B1/B10 and history-window timing modes, controlled native threads, reproducibility comparisons, timeouts, memory measurements, and **timing-only** reports.

### 12.3 Current repository layout and potential additions

The repository is `hydra3333/analysing_perceived_randomness_in_reality`. The existing `src/` code supports the reviewed E_1 and coordinator foundations but the Package 2 scientific reader C1/C2 is **not yet accepted**. Current authoritative owner-run data utilities include `src/two_site_results_check_v0_7.py`, `src/results_master_v0_1.py`, `Run_Results_Updater.bat`, and `install_upgrade_dependencies_into_venv.bat` (automatic install-and-upgrade by default). Data live under `source_data/` in versioned per-game masters, ledgers and verification records. `doc/` contains approved specifications and historical audit records; `tests/` and `results/` preserve bounded evidence by track. The previously date-stamped two-file Powerball histories and deprecated scrapers remain only as Git history where applicable; do not use them as current input.

Future packages, directories and task interfaces require an explicit versioned design, not inference from these examples.

### 12.4 Shared experiment interface — conceptual, not final Python API

Inputs might be an immutable sequence of historical draws **up to but excluding** the prediction target, a prediction-target identifier/date, and method-specific parameters. Outputs might be a structured object with:

```text
experiment_id            E_3
experiment_name          Occurrence-Curve Endpoint Forecast
method_version           0.1
history_first_draw       ...
history_last_draw        ...
predicted_draw           ...
main_scores              mapping 1..35 -> score
powerball_scores         mapping 1..20 -> score
main_ranked              permutation of 1..35
powerball_ranked         permutation of 1..20
selected_main            seven distinct values
selected_powerball       one value
score_semantics          e.g., fitted next-step indicator / relative ranking
parameter_snapshot       ...
random_seed              ... or none
warnings                 ...
```

These are **illustrative metadata fields**, not a JSON schema or final type contract. The implementation should be flexible enough for unusual but properly specified experimental outputs.

### 12.5 Numerical reproducibility

Record the Python version, library versions, significant numerical options, floating-point backend and reproducible task-identity-derived pseudo-random seeds. **Future default acceptance test:** on the same controlled host, code revision, data, Python/packages, single-threaded numerical backend and task seeds, **1-worker and 6-worker execution must produce bit-identical canonical predictive payloads**. Timing numbers are excluded. A failure needs investigation, not an automatic tolerance. Only a technically justified, narrowly scoped exception with a disclosed alternative equivalence test and **explicit user approval** may override the default. A performance claim dependent on one lucky random seed is not a robust result.

### 12.6 Performance and caching

The dataset is small, but some methods may involve expensive latent-state inference, optimisation restarts, integrations and simulations. Start with the simple **one-process-per-E-method** plan using a configurable pool of **1–6 workers** on the 12-physical-core / 24-thread Ryzen 9 3900X, **32 GB RAM**. Keep each worker's native numerical-library parallel threads limited to one initially, and schedule fewer workers when peak memory warrants. Cache safely reusable historical-only computations; **never share a cache across forecast cutoffs if it contains future-fitted information**. Any future more-than-six-worker/SMT throughput trial requires separate owner review and authority; it is not a default benchmark.

### 12.7 Failure handling

The program should fail clearly on missing source data, impossible selections, model fit failures, missing Python packages and inconsistent experimental outputs. One failing E-method should be reported and isolated if the runner can safely continue, but missing or failed predictions must never be misrepresented as valid poor scores.

---

### 12.8 Current timing-only benchmark and parallel baseline (owner-decided)

- One operating-system method process per worker; configurable 1–6 active workers, default six, pin numerical backends to one thread. No default 12/24-worker requirement.
- Timing-only B1 target **Powerball 1576**, training 1144–1575 (432 draws); B1 W=100 trains 1476–1575. B10 targets **1567–1576** with correct earlier per-target prefixes. No benchmark may cross the August 2026 quarantine boundary.
- Equivalent one-/six-worker canonical forecasts, manual/coordinated wrapper identity and Windows safety gates are acceptance requirements, not performance-ranking rules. Runtime caches require reproducibility proof and must not leak target N or later observations.

## 13. Python dependencies and local virtual environment

### 13.1 Agreed packaging approach

Any needed third-party packages must be stated explicitly before use. **Do not install packages globally** into the user's Python 3.14 environment. Use a project-local virtual environment (`venv`) and ordinary `pip` package installation inside it.

The user maintains a project-local `.venv`; current authoritative package maintenance is `install_upgrade_dependencies_into_venv.bat` with its default install-and-upgrade action, plus independent post-upgrade regression gates.

### 13.2 Preliminary package possibilities — not installation instructions yet

| Package / facility | Possible role | Status |
|---|---|---|
| Python standard library (`csv`, `datetime`, `math`, `statistics`, `pathlib`, `json`, `venv`, etc.) | Basic loading, validation, control, reporting | Available with Python; exact API to design |
| **NumPy** | Arrays, binary occurrence matrices, vectorised operations | Likely useful; version/availability to confirm later |
| **SciPy** | Statistical distributions, optimisation, curve fitting, signal processing | Likely useful for advanced methods; confirm later |
| **pandas** | Tabular transforms and CSV processing | Optional, not mandatory for ~440 rows |
| **scikit-learn** | Regularised models and some machine-learning candidates | Only if the selected experiments need it |
| Other packages | Particular Bayesian, time-series, wavelet, chaos or optimisation approaches | Research and justify individually before adding |

Historical requirements and web-scraper packages are not the current dependency authority; see Architecture §5A.2 and the numerical reference.

### 13.3 Existing environment: ordinary CMD and VS Code

The project-specific `.venv` **already exists** in the local checkout and is excluded by `.gitignore`. It uses Python 3.14.8, and the local package installation was verified. VS Code has a project-specific Windows Command Prompt profile that activates it; independent Windows CMD sessions can activate it with the user's verified `activate_venv.bat`.

In a **new Windows Command Prompt** already positioned in the repository root:

```cmd
activate_venv.bat
python -c "import sys; print(sys.executable)"
```

Or, without the helper, run `call .venv\Scripts\activate.bat`. To leave the environment, use the verified `deactivate_venv.bat`. From inside VS Code, **new** terminals already activate the same project venv using the checked project terminal profile. No second virtual environment, new system-wide Python configuration or global package installation is needed.

Future selected methods may require additional packages. Propose each dependency and compatible version before installing, use `python -m pip` from this existing environment, and deliberately update `install_upgrade_dependencies_into_venv.bat` after verification. Do not recreate `.venv` or overwrite the existing package set merely to draft R2.

---

## 14. Proposed research and development phases

These phases remain a **proposed sequencing**, not permission to proceed automatically. **R1 has produced the research catalogue v0.4** and R2 is the recommended next substantive drafting phase once this proposal and the catalogue are accepted. No predictor implementation is authorised by producing this coordination revision.

### Phase R0 — Ratify the project charter and operating principles

**Objective:** Confirm that the written proposal accurately captures the user's intention, especially the deliberately assumption-challenging research philosophy.

**Activities:**

1. Review user-agreed items A-01 through A-37, distinguishing policy commitments from still-proposed technical details.
2. Correct any misinterpretation, particularly around recurrence timing, holdout use, method retention, and the meaning of challenging perceived reality.
3. Establish the proposal's role as project guidance and identify which open decisions belong to later design stages.

**Deliverable:** User-approved revision of this project proposal. **Gate:** No unreviewed assistant recommendation becomes a binding rule merely by appearing in the document.

### Phase R1 — Research the wider experimental landscape

**Objective / current status:** R1 has **catalogued 56 additional candidates** (E_7–E_62) beyond the six original user ideas; exploration of **up to 100 additional candidates** is permitted if future research warrants it. The current R1 v0.4 report is a **completed research deliverable and review candidate**, not a method implementation or proof of predictive value.

**Search domains include:** classical and Bayesian statistics; stochastic processes; nonlinear time-series methods; signal processing; spectral analysis; dynamical systems and chaos; entropy and information theory; change-point detection; state-space estimation; probability calibration; machine learning; model averaging; evolutionary search; unusual or speculative pattern-detection methods; and combinations across these domains.

For each proposed candidate, prepare a research note containing:

- A permanent provisional candidate label until the user approves its `E_x` identity.
- A plain-English description and, where useful, precise mathematics.
- What it actually measures, and how that could generate a forecast for the next draw.
- Input requirements, expected parameter complexity, plausible dataset limitations, and Python dependency needs.
- Whether it can operate separately for the two barrels and respect the main barrel's sampling without replacement.
- Its scientific status: established methodology, exploratory transfer, speculative hypothesis, or mathematically defective reasoning. These are **descriptors for review**, not grounds for deleting a candidate.
- The risk of mistaking retrospective curve fit or hindsight-based selection for prospective prediction.
- A recommendation for priority, feasibility, and sensible early tests.
- References for substantive external claims when that research is performed.

**Deliverable:** `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md`, the **completed current catalogue** of E_1–E_62 for review. **Not delivered:** working implementations, evaluated rankings or verified predictive improvements.

### Phase R2 — Agree on experimental inventory and definitions

**Objective:** Decide which new candidates become individually specified experiments and how related variants will be identified.

Resolve, for example, whether two alternative curve families belong in one tunable E-method or in separately numbered E-methods, and when a changed scientific question requires a new identity. Work against **all 62 current candidate identities**, not merely the first six. Specify operator-labelled ordered/unordered inputs under one common data policy; separate-barrel prediction outputs; model variants (including E_57–E_62); and source/temporal constraints. Candidate formulas in R1 are reviewed rather than silently adopted as implementation authority.

**Deliverable:** A separately reviewed **R2 versioned method/implementation specification**, covering method contracts, stable names/variants, formula choices, inputs, outputs, dependencies, benchmarking and unresolved issues. No unratified R1 recommendation becomes binding solely by appearing in its catalogue.

### Phase R3 — Agree on test design, scoring, and evidence standards

**Objective:** Develop the evaluation framework *after* reviewing candidate methods, as requested.

Issues for explicit discussion include:

- Historical walk-forward ranges and minimum warm-up observations.
- The ten-draw development holdout, its exact frozen membership, and rules for access.
- Counts of main-number matches, Powerball correctness, probability/ranking metrics, and combined-draw scoring.
- Appropriate null/reference methods and simulated benchmarks.
- Quantification of chance variation, multiple-comparison effects, model tuning, and uncertainty.
- How to compare a ranking method with a calibrated-probability method fairly.
- Policy for selecting, reweighting, reversing, or combining weak and strong methods.
- When to escalate a surprising signal for fresh-data confirmation.

**Deliverable:** Explicitly approved test-and-scoring specification. **Gate:** Do not retrospectively invent a metric to validate a favoured historical prediction without clearly treating it as exploratory.

### Phase I1 — Build the minimal, verifiable Python foundation

**Objective:** Implement a correct loader, validation, experiment registry, historical walk-forward runner, and reporting facility before adding complex models.

Start with deterministic test fixtures and transparent baseline experiments. Provide a script suitable for the user's Windows/Python 3.14 workflow. Record all third-party dependencies and teach installation in a local virtual environment. Confirm that every model sees only allowed historical data for the target draw. **Construct separate synthetic-only test infrastructure** capable of thousands of null-world or planted-effect draws and repetitions; implement explicit barriers so those jobs cannot tune or select real-draw forecasts.

**Deliverable:** First working, versioned predictor program and repeatable basic tests. **Gate:** A historical prediction must be reproducible from the frozen dataset and experiment configuration.

### Phase I2 — Implement and validate the initial methods

**Objective:** Implement the six agreed conceptual experiment families with independently inspectable output.

For each method: test on small artificial sequences with known expected results; confirm behavior on missing or pathological data; execute the common walk-forward test; produce scores and ranks; and retain full experiment metadata even where the method performs poorly.

**Deliverable:** Six implemented method families, or a clear explanation of any blocked item with its registry identity preserved.

### Phase I3 — Add researched methods and combinations iteratively

Implement methods in manageable groups, not necessarily all 50 at once. Later add E-numbered combination experiments. A combination's apparent improvement on data that helped create it is provisional until evaluated on data that did not help select it.

Poor performers stay in the registry. They can be revisited as components, contrarian signals, conditional specialists, or inspiration for new hypotheses.

**Deliverable:** Expanding versioned method registry, historical results, and combination studies.

### Phase V1 — Conduct the reserved final historical evaluation

Use the approved evaluation set and declared protocols to examine final candidates. Make clear which methods, parameters, and combination rules were frozen *before* the set was examined. If findings motivate further changes, label those as new exploratory work rather than treating the same holdout as pristine again.

**Deliverable:** Final historical evaluation report with uncertainties, anomalies, negative results, and method-ranking tables.

### Phase P1 — Make and archive genuine next-draw predictions

Create a prediction for the next unobserved draw from **all information available at the forecast cutoff**, explicitly including the formerly reserved ten draws when the user authorises genuine future prediction. Save the forecast independently of subsequent results. When actual numbers become available, evaluate and append outcomes without modifying the original forecast.

Repeat prospectively if the user wishes. Prospective results are the strongest practical guard against hindsight fitting.

**Deliverable:** Timestamped forecast records and later separately recorded observed outcomes.

---

## 15. Proposed testing and quality-assurance controls

These are suggestions for later acceptance, not yet a binding test specification.

### 15.1 Unit tests for basic interpretation

- **Draw parsing:** Exactly seven distinct main values within 1–35 and one Powerball value within 1–20; reject duplicates, invalid dates, noninteger values, and wrong column counts.
- **Rules era:** A pre-19-April-2018 row must not silently enter the selected training period.
- **Chronology:** Sort by draw date/number as required; detect duplicates and gaps, but do not silently fabricate missing observations.
- **Occurrence indicators:** For each historical main draw exactly seven indicator positions equal one; for Powerball exactly one position equals one.
- **Recurrence calculation:** Explicitly verify the off-by-one convention with hand-worked sequences.
- **Forecast selection:** Select seven distinct main values and exactly one Powerball value, respecting declared ranking and tie-breaking rules.

### 15.2 Temporal non-leakage tests

For any target draw `N`, modify the result at `N` and every later draw in a test dataset. A correctly isolated prediction for `N` must not change. This is a particularly strong automated test for unintended future-data leakage.

Similarly, a model's fitted transformations, hyperparameter selection, calibration, standardisation, and ensemble weights must not use data outside that prediction's permitted information window.

### 15.3 Separate synthetic-only research apparatus

**This is a fully separate experimental track, not a subroutine of real prediction training.** Construct artificial histories from known mechanisms, including:

- Ideal uniform independent draws.
- Deliberately biased but otherwise independent draws.
- Periodic or quasi-periodic inclusion processes.
- Abrupt and gradual changes in inclusion propensity.
- Hidden-regime processes and constructed dependencies.
- Adversarial misleading trends that fit the past but reverse later.

These tests check whether an E-method can, where appropriate, detect the kind of structure specified by the synthetic generator. Success on artificial mechanisms is **not evidence that the mechanism exists in Australian Powerball**. Report null/planted outcomes in a **synthetic-only report family**, with thousands of repetitions allowed. **Disclosed design learning** from synthetic work may improve algorithms or motivate variants. What must not be mixed into real predictions is the **artificial observation dataset, its fitted synthetic hidden state, its synthetic-only parameters, or its artificial outcome scores**. Real choices must be documented, historically admissible and evaluated on actual data under agreed protocols. No failure here automatically bars real-data investigation.

### 15.4 Reproducibility and reporting checks

Maintain inputs, chosen method version, parameter snapshot, library versions, random seeds if used, calculation warnings, and full ranked outputs. A failed or unavailable method should be reported as such, never disguised as a zero-scoring valid prediction.

---

## 16. Proposed research risk register

| Risk | Why it matters | Proposed treatment |
|---|---|---|
| False discovery across many methods | With many tests, unusually successful-looking models arise by chance | Track the number of attempts, preserve full rankings, use untouched and prospective tests, and account for search effects in interpretation |
| Historical information leakage | Using future data yields deceptively strong backtests | Explicit forecast cutoffs, immutable historical slices, non-leakage tests |
| Overfitting a short history | Approximately several hundred weekly draws offer limited power for high-dimensional models | Parameter restraint where helpful, uncertainty reporting, stability tests, separate final evaluation |
| Cherry-picked results | Selective reporting can conceal unsuccessful hypotheses | Permanent E-method registry and preservation of all results, including negative outcomes |
| Hidden rule-era mixture | Combining incompatible ball ranges produces invalid conclusions | **Hard Draw 1144 (19 April 2018) boundary**; exclude any differing configuration, including proposed extended Powerball-only history |
| Input-data errors or later corrections | False patterns may reflect incorrect draw histories | Validate sequences and ranges, cross-check unusual cases, preserve dataset snapshots and correction history |
| Treating descriptive fit as prediction | Excellent curve fit may have no next-step utility | Walk-forward evaluation, prospective forecasts, separate in-sample diagnostics |
| Instability of fitted models | Tiny changes in the data can reverse predictions | Sensitivity and parameter-stability checks, error bars, versioned configurations |
| Incomparable method outputs | Rankings, raw scores, and probabilities are different objects | Common reporting protocol; distinguish score semantics and calibrate only where justified |
| Retrospective ensemble tuning | Ensembles may look better because built after seeing outcomes | Give combinations separate identities; log selection/weighting rules; evaluate on new data |
| Mistaking correlation for mechanism | Predictive association does not uniquely establish a physical or metaphysical explanation | Separate empirical findings from causal and philosophical interpretations |
| Premature dismissal of an unusual idea | Could overlook a legitimately informative relationship | Preserve and examine all methods; classify objections precisely; allow speculative research |
| Assuming unusual success proves predictive power | Could elevate noise into false confidence | Repeated, independently checked observations, uncertainty analysis, prospective replication |
| Source publication / browser update change | Upstream page format may interrupt owner-run results-master updater | Require verified create-only versioning, independent source audit, preserve previous master/ledger |
| Dependency or environment drift | Results could change as Python libraries evolve | Local `venv`, explicit package/version inventory and controlled numerical seeds |
| Synthetic-to-real contamination | Artificial draws, fitted synthetic state, or scores might leak into real-data training or be misrepresented as real success | Separate execution/data/reports, explicit provenance, tests on fixed real inputs/configuration; **disclosed simulation-informed design remains permitted** |
| False exclusion through method correlation | Related methods may contain subtle complementary information despite similar overall predictions | Retain all and keep all eligible; report correlation without excluding or deprioritising by default |
| Incomplete drawn-order or apparatus provenance | Operator-labelled ordering has evidence, but not every row has independent broadcast verification; apparatus identifiers may be missing | Retain source manifest and sequence/set checks; make apparatus optional; do not misstate operator records as independent broadcasts |
| Prospective forecast rewriting | A forecast could be modified after the result becomes known | Save timestamped, immutable forecast artefact before drawing; optional Git commit timestamp as independent evidence |

The two philosophies at the heart of the project are **both** represented here: avoid dismissing an unorthodox hypothesis merely because it violates a familiar model, and avoid claiming that a surprising backtest alone proves the universe works differently.

---

## 17. Method registry and research-record governance — proposed

### 17.1 Permanent experiment identity

Once assigned, `E_17` always refers to the same core experimental question. Materially different scientific hypotheses or altered combination logic should receive a new `E_x` number; bug fixes and compatible refinements may use the method's version field. Which changes require new IDs versus versions remains a decision for the method-specification phase.

A method can have statuses such as *proposed*, *specified*, *implemented*, *tested*, *experimental only*, *inactive for a particular report*, or *blocked*. **Inactive does not mean deleted or ineligible forever.**

### 17.2 Per-method research record

A useful record would contain the question, rationale, exact data construction, mathematical definition, prediction transformation, chosen parameters, dependencies, version, test coverage, historical results, anomalies, known faults, and combination history. This enables a later reviewer to reproduce or reinterpret a result rather than rely on a short label.

### 17.3 Qualification for combined methods

Combination eligibility should **not** be decided solely by an individual's standalone rank. Candidate criteria might eventually include:

- Whether a method's errors differ systematically from those of others.
- Stability across disjoint historical periods.
- Complementary predictions or inverse/contrarian information.
- Diversity of analytical mechanisms and their dependencies.
- How sensitive results are to parameter choices and training-window sizes.
- Whether improvement survives tests not used to construct the combination.

Selection, weighting and qualification rules may change as the research matures, but each change should be documented, and the user should approve consequential revisions. No method is erased because it stops qualifying under the current rule.

### 17.4 Evidence preservation

Keep all experimental evaluations and anomalies in a versioned or otherwise reproducible archive. Reports may rank, filter or summarise for readability, but a low-rank method remains discoverable with its historical record intact. Distinguish results from a shared dataset used for exploration from genuinely reserved or prospective results.

---

## 18. Decisions deliberately deferred

This section identifies unanswered questions; **none is being silently decided by the proposal**.

1. **Research-to-specification scope:** Which of the **62 currently catalogued** candidates will receive formal R2 contracts in which order, and how future E_63+ candidates will be proposed within the optional 100-additional-method scope? **Retention and combination eligibility remain unconditional**.
2. **Method granularity:** When does a change define a new E-method, as opposed to a parameter variant or version?
3. **Recurrence alignment:** Exact interval convention, robust estimator, appropriate fitting window, and prediction score.
4. **Curve fitting:** Chosen curve families, constraints, forecast extrapolation versus endpoint estimation, gradient definitions, and regularisation.
5. **Distribution fitting:** Candidate families, goodness-of-fit measures, whether probabilities must be calibrated, and how to model sampling without replacement.
6. **Walk-forward programme:** Which historical ranges and evaluation counts will be used for each stage, beyond the agreed last-ten concept?
7. **Holdout policy:** Exact frozen membership and treatment of subsequent data arrivals and re-evaluations.
8. **Evaluation metrics:** Which performance measures become primary, secondary, and exploratory?
9. **Evidence thresholds:** What justifies describing an observed advantage as promising, replicated, or potentially predictive?
10. **Method combination:** Eligibility, weighting, score normalisation, inversion, conditional gating, and ensemble search.
11. **Implementation:** Final module structure, CLI design, report formats, worker-pool and benchmark details, numerical backends, per-method runtime limits, package versions and tests; default requirements of 1–6 workers, 32 GB awareness, B1/B10 computational probes and worker-count reproducibility are stated in §12.8.
12. **Future forecasts:** Which methods or combinations to use for a real draw, and how to record the pre-draw commitment.
13. **Independent verification:** What external checks of source data or surprising findings would be most useful?
14. **Drawn-order operational policy:** How will the **operator-labelled drawn-order** view be exposed consistently to each compatible method, distinguished from unordered sets, and annotated with provenance? Optional independent video spot checks can improve source assurance but are not a prerequisite.
15. **Optional external datasets:** Which, if any, provide testable real-time or historical-before-cutoff observations, and with what timestamp provenance?
16. **Synthetic instrumentation:** Which generator families and diagnostics provide useful **separate** sensitivity and identifiability research, while allowing **disclosed design learning** but forbidding substitution of synthetic observations/fit states/scores into real prediction?
**Historical-source statement withdrawn:** authoritative source is the per-game versioned master and ledger described in §3 and R2 §2.

The user expressly requested **discussion of testing and scoring later**, after candidate methods have been explored. The document therefore records concepts and safeguards without imposing a premature scoring specification.

---

## 19. Success criteria and interpretation of outcomes

The project can be successful in more than one scientifically meaningful way:

**Software success:** A reliable, understandable, extensible Python 3.14 environment that loads correct current-format draw data, runs arbitrary registered methods consistently, preserves their results, and produces leakage-free retrospective and real-world forecasts.

**Research success:** A thorough record of what was tested, which hypotheses survived particular evaluations, which failed, what anomalies arose, and how robust the conclusions are. A rigorous negative finding is a valid outcome; it does not erase the experiment's value.

**Potential predictive success:** Evidence that a predeclared method or combination gives a repeatable advantage over appropriate reference behaviour on data not used to discover or tune it, ideally including multiple genuine prospective draws. The level of claim should match the amount and quality of evidence.

**Broader conceptual success:** Identifying an unexpected and reproducible regularity that merits new explanations or additional independent research. It may challenge a conventional model without automatically establishing any particular alternative theory of reality.

The project does **not** promise a profitable lottery system, a winning ticket, or proof of a metaphysical claim. Such promises would outrun the evidence. Nothing about that restraint limits the range of hypotheses the investigation is prepared to entertain.

---

## 20. Immediate next action, document status, and revision protocol

### 20.1 Current next step (DECIDED)

Have Claude independently review this consolidated Proposal v0.5 together with the corresponding R2 v0.4, R3 v0.4, Architecture v0.7, P3 v0.2, register and exposure/reference candidates. After any corrections, the **owner** decides ratification. Only then package and mechanically verify the installation, commit/push the accepted documentation, and produce a comprehensive self-contained ChatGPT coding handover for a separate Claude review. Begin bulk Package 2 v0.11 coding only in the fresh ChatGPT implementation conversation, after that transfer is accepted. R1 v0.4 and the TIE_SHA256_V1 encoding note v0.2 remain unchanged and authoritative. The initial worker limit is **1–6**, not the obsolete 1–12 proposal. No approval to execute a scientific experiment, open holdout, run Oz methods or enable process termination follows from ratifying documentation alone.

### 20.2 Status distinctions

- **User-agreed policy:** The substantive A-01–A-37 commitments (§4), subject to the user's acceptance of this written consolidation.
- **Research complete to catalogue stage:** R1 v0.4 includes E_1–E_62 as **research candidates** with remaining design details for R2.
- **Proposed:** Exact mathematical variants, implementation approaches and the complete executable test contracts beyond the agreed design direction.
- **Deferred:** Detailed predictive scoring, actual method implementation choices and thresholds, ensemble selection, final-holdout protocol details, and future forecast selection.
- **Not done:** No E-method predictor implementation, whole-method predictive backtest, synthetic null/planted run, reserved-holdout scoring or actual next-draw forecast has been asserted.

### 20.3 Version and change management

- Retain v0.2 for historical traceability; store **this** file as `doc/Predictive_Randomness_Research_Project_Proposal_v0_3.md`.
- Retain R1 v0.4 separately, including all 62 research-method entries; there is **no need to regenerate or merge R1** because this charter is being updated.
- If the user ratifies a material change to project policy, amend the proposal/decision register; if an R1 discovery merely suggests a change, label it a recommendation pending approval.
- R2 and R3 should include document dependencies with **exact filenames and statuses**, reference ratified policies and never silently change user-approved commitments.
- Preserve original method identities, experimental records, low-ranked methods, synthetic diagnostics, and observed outcomes with explicit provenance. Do not overwrite an unsuccessful past result to match a later improved design.

### 20.4 Closing project principle

> **We are deliberately willing to challenge the nature of perceived reality, including the usual assumption that past lottery draws contain no predictive information. We will entertain established, unconventional and speculative analytical methods without prejudging their outcomes. Every method is retained, every result can be examined, and claims are strengthened or weakened by transparent, reproducible and genuinely forward-looking evidence.**

**Consolidation note:** Original v0.4 chronology and §0A amendment remain accessible in the ratified predecessor; this candidate integrates current decisions into the present numbered sections.

## Appendix S — Superseded provisions (historical only; non-operative)

- Prior Proposal §0.1–0.3 document chronology, ratification status and two-CSV snapshot descriptions: replaced by consolidated §0 and §3.
- Former §0A multi-game amendment and later §0B patch: integrated into §§0, 3, 5, 11, 12 and normative R2/R3/Architecture; no layered precedence remains.
- A-08 moving “latest ten” holdout: replaced by the fixed August 2026 quarantine and per-game FINAL_HOLDOUT_10.
- Earlier Powerball holdout 1578–1587, development cap 1577, Oz Lotto first-accepted-snapshot highest-ten rule and 7 August 2026 cap: withdrawn.
- Former 1–12 worker / 12-worker equality and 24-worker exploratory acceptance defaults: replaced with approved initial 1–6, six maximum.
- Retired two-CSV, standalone scraper, `Run_Scraper.bat` and historical `requirements.txt` as current source/installer authority: replaced by owner-run master updater and authoritative dependency batch file.
- Historical published ball-value quotations concerning quarantined draws remain in unchanged Git-source history and are disclosed only in the factual exposure record; none are repeated in the operative charter.
