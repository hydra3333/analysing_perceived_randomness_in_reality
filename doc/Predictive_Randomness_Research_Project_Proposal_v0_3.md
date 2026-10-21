# Australian Powerball: Experimental Investigation of Randomness, Predictability, and Perceived Reality

## Comprehensive project proposal — version 0.3 (document-coordination and policy-reconciliation review candidate)

**Prepared:** 21 October 2026  
**Status:** v0.3 **review/ratification candidate** incorporating subsequent user agreements and coordinating the project charter with R1 v0.4; **not** a predictor implementation specification, a scored evaluation, or blanket approval of candidate-method formulas  
**Primary platform:** Windows 11; Python 3.14.8 (standard build); project-local `.venv`; AMD Ryzen 9 3900X (12 physical / 24 logical processors), 32 GB RAM; VS Code and ordinary Windows CMD  
**Primary observation period:** **19 April 2018, Draw 1144**, onward — exactly the seven-from-35 and one-from-20 format; **no earlier-rule-era records, even for Powerball-only analysis**  
**Proposed program naming:** `Powerball_Predictor_v001.py`, followed by versioned successors  
**Experimental method naming:** permanent `E_1`, `E_2`, … identifiers, each paired with an intelligible name  
**Data acquisition:** date-stamped core ascending-set CSV and separately cross-checked **operator-labelled drawn-order CSV**; operator evidence is not 444 independent broadcast verifications  
**Simulation safeguards:** artificial draw observations, fitted synthetic states and synthetic outcomes never enter real-data training, predictions or real-result scores; separate synthetic research **may inform disclosed model design, calibration interpretation, feasibility, debugging and priorities**, without becoming evidence of real-world predictive success or an exclusion gate

> **Central premise — deliberately unconventional:** This project is an empirical investigation of whether the apparent randomness of real-world Australian Powerball draws hides any exploitable structure. It expressly permits questioning familiar assumptions about probability, temporal independence, causal relationships, connectedness, and even the way we conceptualise perceived reality. We do **not** rule out a method merely because prevailing models say it should not work. Equally, we do **not** pronounce a method predictive merely because it produces an intriguing pattern. All proposals are welcome to be examined; evidence, reproducibility, mathematical consistency, and prospective performance decide what conclusions can honestly be drawn.

---

### Revision record — v0.2 to v0.3 (21 October 2026)

This is a **controlled update of the complete v0.2 proposal**, not a replacement charter. Its purpose is to eliminate drift after the separate R1 research and user decisions. Section 2's challenge to conventional notions of randomness and perceived reality is retained without qualification or restriction.

1. **Document roles and authority clarified:** proposal governs agreed project policy; `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` governs the 62-method *research catalogue* and candidate mathematics; future R2 and R3 documents will govern detailed method contracts and evaluation rules **once approved**. A research recommendation does not silently amend policy. The R1 v0.4 header naming proposal v0.2 is its historical source basis, not a competing current project charter.
2. **Research completed to candidate-catalogue stage:** retain the original six `E_1`–`E_6`, and record 56 additional candidate identities `E_7`–`E_62`, including pilot-wave-*inspired mathematical models* `E_57`–`E_62`; permit **up to 100 additional candidates** if useful (potentially through `E_106`), with **no numerical quota** and no automatic implementation authorization.
3. **Critical synthetic-policy correction:** synthetic null-world, planted-effect and identifiability research is performed and reported separately and may inform **disclosed research design, calibration, sensitivity, computational planning, and interpretation**. Synthetic draws, synthetic-fitted latent states, artificial outcomes and synthetic scores are **not substituted into actual-draw training, fitted forecast states, real-data score tables or forecasts**. No synthetic failure disqualifies a method or prohibits its real-data experiment. Supersedes the blanket no-design-influence prohibitions in v0.2 §§4, 10 and 15.
4. **Draw order resolved:** the official operator The Lott's **Drawn / Numerical** presentation and its Draw 1297 explicitly labelled historical results corroborate the corresponding Lotterywest-derived order CSV. Name this **operator-labelled drawn order** rather than provisional “reported order”; preserve the limited claim that not all 444 draws have separately been verified from broadcasts. R2 is to define **one common ordered/unordered data-use policy** for compatible experiments.
5. **Pilot-wave family and user protection:** `E_57`–`E_62` remain investigable on **real** eligible-era observations. Exact/regularised guidance, set-likelihood, cyclic-order and hidden-state diagnostic qualifications are in R1; neither conventional expectations nor artificial identifiability diagnostics exclude any method. Quantum inspiration is **not** evidence of a quantum causal mechanism in lottery apparatus.
6. **Computational design proposed for R2:** user hardware, one process per method, 1–12 worker pool (optional 24-worker SMT benchmark), single-threaded numerical backends, B1/B10 prediction-target computational benchmarks, 100 versus full development-history training windows, timing/resource/failure-only benchmark reports, and worker-count reproducibility. Computational cost never determines method retention or combination eligibility.
7. **Reproducibility strengthened:** within controlled matching numerical conditions, 1-worker and 12-worker prediction payloads must be **bit-identical** as the default future implementation acceptance check; an exception requires a specific documented cause and user approval. Benchmark runtime measurements are excluded from byte equality.
8. **Project-status and repository references refreshed:** the repository now holds two 444-draw source CSVs for Draws 1144–1587, the v0.3 scraper, R1 v0.4, working Python 3.14 `.venv` and `requirements.txt`. Nothing in this edit asserts that the E-methods have been implemented or scored, or that the final holdout has been opened.

**Coordination rule:** The accepted later user instructions recorded here supersede conflicting v0.2 text. Existing v0.2 revision notes below are preserved as history, not operative rules when contradicted by v0.3. Detailed R1 model proposals remain *candidate designs* pending R2 review. No repository files or datasets are modified by this Markdown deliverable.

### Historical revision record — v0.1 to v0.2 (preserved; superseded where stated above)

- Corrected current-rules inception to **Draw 1144 on 19 April 2018**, adding the two valid April draws and updating the script.
- Confirmed a **hard bar** on all pre-change draw results, including Powerball-only variants (rejection of review D4).
- Incorporated review decisions D1/D2/D3/D5 to the approved or provisionally approved extent without converting them into restrictive method-selection principles.
- Introduced an explicit **simulation firewall**: independent artificial histories and reports have no influence on any real-data prediction, including parameters and method selection.
- Expanded the possible observational domain to include optional, independently checked **Lotterywest reported draw order**, with equipment metadata and external feeds expressly optional.
- Emphasised permanent method retention and combination eligibility **irrespective of high method-method correlation**, or conventional expectations.
- Added potential simulation-power and method-sensitivity diagnostics, always as separate reference instruments rather than gates limiting speculative research.
- Preserved the central principle that the project deliberately questions perceived reality and accepted independence models.

**Source/status note:** The supplied Claude review is a review input, **not** an independent ratified project authority; this version reflects the user's subsequent decisions and the additional source checks. The optional enhanced scraper was tested with local fixtures. A complete live trial of Lotterywest enrichment was not possible from this document-authoring environment.

## 0. Document control, precedence and current project state

### 0.1 Why there are two substantive documents

The documentation is deliberately **layered, not merged**:

| Document | Repository path / status | Governing responsibility |
|---|---|---|
| **Project Proposal v0.3 (this file)** | `doc/Predictive_Randomness_Research_Project_Proposal_v0_3.md` — review/ratification candidate | **Project charter:** research purpose, philosophy, user-agreed policies, boundaries, retain-all-methods rule, and decision/governance controls. |
| **R1 Experimental Methods Research v0.4** | `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` — completed research catalogue, current **review candidate** | Research findings and **E_1–E_62 candidate inventory** (not an approved mathematical/implementation specification). It makes recommendations; it does not independently change the charter. |
| **R2, future** | No ratified R2 file yet | Detailed mathematical definitions, candidate variants, agreed observation policy, input/output contracts and implementation specifications. Requires review. |
| **R3, future** | No ratified R3 file yet | Predictive scoring, historical-evaluation protocol, inference and reporting standards; requires review. |
| **Operational source/data** | `src/`, `source_data/`, `requirements.txt`, `.vscode/` | Implementation and observational evidence. Operational files do not by themselves authorize new research-policy rules. |

**Precedence when documents appear to differ:** (1) a clear subsequent **user-ratified decision** controls; (2) the latest user-approved project proposal governs project-wide policy; (3) an approved R2/R3 specification would control its own expressly delegated technical area, without overriding project policy; (4) R1 supplies candidate research and rationale, not policy overrides. Unratified assistant recommendations are labelled *proposed* or *candidate*. Material conflicts are raised for resolution; do **not** silently average the documents or interpret newer text as authorisation to breach a user decision.

**Transitional cross-reference:** R1 v0.4 records v0.2 as the proposal available when R1 was authored, with “subsequent user instructions controlling”. That is accurate **historical provenance**. This v0.3 succeeds v0.2 for future charter review; retaining R1's historical citation is not a substantive inconsistency. A future metadata-only R1 update may point to a ratified v0.3, but no R1 content needs rewriting now.

### 0.2 Agreed, candidate and deferred are different statuses

- **User-agreed:** items recorded as decisions, including same-rule draw boundary, ten-draw holdout, all-method retention, speculative openness, synthetic separation **with permitted disclosed methodological learning**, and baseline benchmark direction. Their **detailed implementation** may still require ratification.
- **Research candidate:** the 62 `E_x` concepts in R1, mathematical variants, optional inputs, and software/bench proposals. Recording them does **not** claim they are coded or predictive.
- **Deferred:** numerical scoring rules, evidence thresholds, ensemble qualification mechanics, actual method implementation order, frozen formula/parameter specifications, and exact execution contracts.
- **Not performed:** a predictor build, an E-method walk-forward run, synthetic calibration runs, final-holdout evaluation, or genuine next-draw forecast.

### 0.3 Current observed source boundary

As packaged in the inspected repository ZIP on 21 October 2026, `source_data/australian_powerball_history_20261021.csv` and `source_data/australian_powerball_draw_order_20261021.csv` each contain **444 draws, Draw 1144 through 1587**, from 19 April 2018 through 15 October 2026, within the 7-of-35 plus 1-of-20 rules. The two files present **different observational views**, not two independent histories. Their matching seven-number sets, Powerball values and draw keys were checked during R1. The new predictor should never infer extraction order from ascending columns or treat the two CSVs as 888 independent draws.

A **historically labelled** drawn-order series is now supported by official operator evidence described in §11.5. That source qualification does not assert that all 444 draws have been independently video-verified.

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

The inspected **repository snapshot dated 21 October 2026** contains **444 consecutive current-format draws**, Draw 1144 through Draw 1587 (latest dated **15 October 2026**), in both source CSVs. This is verified from the supplied repository files and their matching keys/sets, **not** a claim that a fresh live download was carried out in this drafting environment.

### 3.2 Historical CSV and operator-labelled drawn order

The project repository contains a **growing**, date-stamped validated record of draws in its `source_data/` directory. The primary ten-column `australian_powerball_history_20261021.csv` records draw number, ISO date, the seven main numbers (usually stored in ascending order) and one Powerball value. The separately sourced `australian_powerball_draw_order_20261021.csv` records the **operator-labelled drawn order** for the same 444 historical draws, with successful draw-key, set and Powerball agreement against the primary CSV. These are two *views of the same observations*, not an enlarged independent sample.

The reviewed starting boundary remains **Draw 1144, 19 April 2018**; no observations from a different main- or Powerball-barrel rule configuration may be added even for a barrel-only variant. The valid source dataset will grow as new completed draws are collected and validated. Filename dates represent acquisition dates, not necessarily dates of the most recent draw.

**Operator evidence:** The Lott's Draw 1587 `Drawn / Numerical` display, and the explicitly drawn-order-labelled official Draw 1297 results (25 March 2021), match the corresponding repository sequences. Lotterywest's historical display supplies the ordered CSV. This justifies the label **operator-labelled drawn order**, while leaving room for optional independent broadcast checks and later source corrections. §11.5 records the provenance and R2 policy implications.

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
| **A-08** | Reserve the **latest 10 completed draws** as a final, untouched test set while developing and selecting methods. |
| **A-09** | When deliberately making a **real prediction for the next unobserved draw**, allow the chosen model to use **all currently available history**, including those 10 draws. |
| **A-10** | The recurrence-interval idea concerns reaching or being near a characteristic **optimal interval on the next draw**, **not** simply being the most overdue. |
| **A-11** | Begin with six user-proposed experimental families and allow research into **up to 100 additional candidate methods if useful** (not a quota). R1 currently contains the original six plus **56 additional candidates** (`E_1`–`E_62`). Candidate listing is not implementation approval. |
| **A-12** | Methods have permanent identifiers `E_1`, `E_2`, … and explanatory names, with modular Python implementations and shared utilities. |
| **A-13** | Preserve **every method**, regardless of standalone rank, apparent failure, novelty, or lack of explanatory mechanism. |
| **A-14** | Every method remains eligible for future single-method or multi-method experiments and combinations, subject to transparent criteria. |
| **A-15** | Combination experiments receive new permanent experimental identifiers; qualification and weighting criteria can evolve, with user review and agreement. |
| **A-16** | Score, compare, and report predictions against known draws, but **defer detailed scoring and selection-policy decisions** until the exploratory-method research and design have been discussed. |
| **A-17** | Python **3.14** is the intended implementation platform. Additional packages must be flagged explicitly and installed only into a **project-specific virtual environment**, not globally. |
| **A-18** | Research and method selection come **before writing the predictor**; the project proceeds through discussion and user ratification. Updating the existing independent scraper is permitted ahead of predictor design. |
| **A-19** | **D1 direction accepted:** separately run null-world, planted-effect and other synthetic/calibration studies, including thousands of simulations where useful. These may inform **disclosed** design, calibration, sensitivity, debugging and interpretation but are not evidence of real predictive success or an automatic eligibility gate. |
| **A-20** | **Synthetic/real firewall (clarified):** artificial observations, fitted synthetic states, synthetic forecasts/outcome scores and synthetic-only parameter fits are never mixed with real draws, real fitted forecast states or real predictive scores. **Documented methodological learning** from simulations is permitted, including model-design and feasibility choices. No method is automatically excluded for failing a synthetic diagnostic. |
| **A-21** | **D2 direction accepted:** investigate additional observations, including now-supported **operator-labelled drawn order** and optional machine/ball-set information. Equipment metadata is neither necessary nor a gating dependency. |
| **A-22** | **D3 accepted:** correct the full compatible historical starting point to **Draw 1144, 19 April 2018**, with no first-two-draw omission. |
| **A-23** | **D4 rejected:** no historical observations from **any** earlier differing game-matrix configuration; specifically, no older Powerball-only extension even if its barrel individually resembled the current one. |
| **A-24** | **D5 provisionally accepted:** reserve extensibility for independent external, time-indexed data, subject to provenance and the information-available-before-forecast rule; no external variable is mandatory. |
| **A-25** | Neither poor standalone scores nor strong correlation with another method may be used to discard, deprioritise as a matter of principle, or make an experimental method ineligible for combinations. Correlation is descriptive reporting information. |
| **A-26** | Core ascending-number results and source-qualified **operator-labelled drawn order** are distinct views of the **same draws**. Never infer draw order from sorted columns, and never double-count rows as independent observations. |
| **A-27** | Revised acquisition preserves the ordinary ten-column dated CSV; official independent verification/draw-order output is optional and must fail closed on missing or contradictory data. |
| **A-28** | The conventional independent-uniform model can calibrate *interpretation and instrument sensitivity* but is **never a gatekeeper** for method eligibility. Synthetic data/states are never genuine forecast inputs, although disclosed simulation-derived methodological learning is permitted. |
| **A-29** | A one-round external Claude review was originally invited; subsequent voluntary discussions informed R1, but ongoing dual-assistant review is **not** required project governance. |

| **A-30** | The project-charter document and the R1 research-catalogue document serve **separate, coordinated roles**. A research recommendation does not silently overrule later user-approved project policy; user agreement controls substantive changes. |
| **A-31** | Extend the available research space to 100 additional candidate methods; **keep every** `E_x` concept and variants, regardless of perceived implausibility, speed, poor results or inter-method correlation. |
| **A-32** | Add all six pilot-wave-inspired **mathematical** research candidates `E_57`–`E_62`, including the corrected guided-particle methods E_61/E_62, as eligible for **real-data** experiments. Their origin does not imply quantum physics is a lottery mechanism; identifiability results are diagnostic, **not** an exclusion rule. |
| **A-33** | Treat Lotterywest's cross-checked ordered numbers as **The Lott operator-labelled drawn order** (supported by Draw 1297 and 1587 evidence). Retain source provenance and the narrower limitation of no complete independent broadcast verification. R2 will have **one common** ordered/unordered data-use policy for compatible methods. |
| **A-34** | Develop the initial CPU execution design around configurable **1–12 separate worker processes**, one E-method per worker; optional benchmark to 24 logical workers, controlled native numeric-library threads and **32 GB memory awareness**. Speed does not determine method eligibility. |
| **A-35** | Keep **computational benchmarking** separate from research scoring. Support `X` walk-forward targets (B1=1, B10=10), a configurable preceding-history length `W` (e.g., 100 or full), and exclude the frozen latest-ten holdout. Do not score or show benchmark predictions in timing reports. |
| **A-36** | The default acceptance criterion for the future implementation is **bit-identical prediction payloads** under 1-worker and 12-worker runs in a controlled matching numerical configuration. Any specific exception needs a documented cause and **explicit user approval**. |
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
| **D2 — equipment metadata and drawn order** | **Accept investigative scope** | Order is now supported as **operator-labelled drawn order**; equipment details are exploratory only and not a dependency |
| **D3 — first qualifying draw 1144** | **Accept and implement in scraper** | Include 19 and 26 April 2018; prohibit earlier configurations |
| **D4 — older Powerball-only history** | **Reject expressly** | Never bring different-rule-era records into the dataset, even for just the unchanged second barrel |
| **D5 — date-indexed external observations** | **Provisionally accept** | Keep an extensible interface; require information-time provenance; no obligatory feeds |

The independent review also highlighted sensitivity, the `E_2` recurrence-hazard formulation, common mathematical ancestry among apparently different models, and source-qualified drawn-order evidence. These are included as research design considerations, **not as grounds to narrow speculative method eligibility**.

### 4.3 Immediate software update and its limits

The independent acquisition program is now `scrape_australian_powerball_history_from_2018_04_19_v0_3.py`. Normal execution writes `australian_powerball_history_YYYYMMDD.csv` containing Draw 1144 onward. With `--official-order`, it additionally obtains official Lotterywest draw-order observations and requires complete independent agreement before writing `australian_powerball_draw_order_YYYYMMDD.csv`. It performs **no synthetic experimentation and no forecasting**. The tests already performed against the new script used synthetic **parser fixtures** to check software behaviour; those are not the future prediction-model simulation programme. The later supplied repository ZIP contains the resulting **444-row** official-order CSV and matching core CSV. These were compared during R1. This does not establish that every subsequent live website request will succeed or that every historical draw was independently broadcast-verified.

## 5. The central experimental workflow

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

For example, if the latest completed draw were `1587`, a ten-draw historical evaluation would target draws `1578`–`1587`, with predictions for `1578` trained only on data through `1577`, and predictions for `1587` trained only through `1586`.

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

**This v0.3 formulation supersedes the stricter v0.2 “no influence even on design” language.** The aim is to keep separate sources of **evidence** while allowing research instruments to be improved. The user has specifically authorised thousands of synthetic simulations, and has clarified that these may inform design, methodological feasibility and interpretation. The user has **not** authorised mixing simulated draws with actual Powerball history or presenting synthetic performance as proof of real-world predictive ability.

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

If scraping succeeded but the data are incomplete, the prediction system must not silently proceed as though the history were exhaustive.

### 11.2 Source checking

The existing scraper is not itself an oracle. When practical, independently spot-check historical results and the latest draws against a reputable operator or archive. Record the source name, retrieval date, content coverage and checksum of any dataset used in a substantive experimental run.

The acquisition program already aims to preserve a successful prior CSV when a scrape fails; the research loader should provide a second line of validation.

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

The basic ten-column history contains the seven main values usually **sorted ascending**. Their storage positions do **not** establish the physical drawing sequence. A separate, cross-checked `australian_powerball_draw_order_20261021.csv` holds the **operator-labelled drawn order** for **the same 444 draws**, not additional independent draws.

The Lott (the game operator) provides a **Drawn / Numerical** display. In Draw 1587, the **Drawn** sequence is **14, 24, 15, 3, 27, 32, 30**, Powerball **16**; numerical order is 3, 14, 15, 24, 27, 30, 32. Both correspond to the repository observations. An [official The Lott Draw 1297 results document](https://journalists.medianet.com.au/DisplayAttachment.aspx?j=947279&k=4845489&s=0), dated **25 March 2021**, expressly labels the sequence **“Winning Numbers (drawn order)”** and gives **14, 15, 16, 21, 12, 25, 10**, Powerball **5**, identical to the repository row. The [Lotterywest Draw 1144 result](https://www.oz.lotterywest.com/powerball/results/draw/1144) displays the corresponding historical main-number order **9, 5, 32, 13, 33, 4, 25**, Powerball **7**. These support an operator-labelled drawn-order *dataset*, not a claim that each of the 444 rows has been independently broadcast-verified.

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

### 12.3 Actual repository layout and possible future additions

The user has established a GitHub repository, `hydra3333/analysing_perceived_randomness_in_reality`, with local checkout at `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`. The repository ZIP inspected for v0.3 already contains:

```text
analysing_perceived_randomness_in_reality/
    .vscode/settings.json
    .gitignore
    activate_venv.bat
    deactivate_venv.bat
    requirements.txt
    doc/
        Predictive_Randomness_Research_Project_Proposal_v0_2.md
        Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md
        SAL_Powerball-Game-Rules_March-2026.pdf
    src/
        scrape_australian_powerball_history_from_2018_04_19_v0_3.py
    source_data/
        australian_powerball_history_20261021.csv
        australian_powerball_draw_order_20261021.csv
    results/
    README.md
    LICENSE
    .venv/                         # local environment, untracked; not in ZIP
```

**This v0.3 deliverable should be saved in `doc/` under its new filename.** The existing v0.2 can be retained as an earlier revision. The workspace's Python 3.14 `.venv` has been created and CMD/VS Code activation verified; do not commit `.venv` or automatically install research dependencies globally.

Possible **future** directories such as `src/methods/`, `tests/`, `config/` and isolated real/synthetic subdirectories under `results/` can be agreed in R2 or R3. They are **not** present mandates and are not being created by this proposal. The existing source-data and results locations should be respected unless the user approves a move.

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

Record the Python version, library versions, significant numerical options, floating-point backend and reproducible task-identity-derived pseudo-random seeds. **Future default acceptance test:** on the same controlled host, code revision, data, Python/packages, single-threaded numerical backend and task seeds, **1-worker and 12-worker execution must produce bit-identical canonical predictive payloads**. Timing numbers are excluded. A failure needs investigation, not an automatic tolerance. Only a technically justified, narrowly scoped exception with a disclosed alternative equivalence test and **explicit user approval** may override the default. A performance claim dependent on one lucky random seed is not a robust result.

### 12.6 Performance and caching

The dataset is small, but some methods may involve expensive latent-state inference, optimisation restarts, integrations and simulations. Start with the simple **one-process-per-E-method** plan using a configurable pool of **1–12 workers** on the 12-physical-core / 24-thread Ryzen 9 3900X, **32 GB RAM**. Keep each worker's native numerical-library parallel threads limited to one initially, and schedule fewer workers when peak memory warrants. Cache safely reusable historical-only computations; **never share a cache across forecast cutoffs if it contains future-fitted information**. Optional 24-worker SMT throughput tests are **benchmarks**, not default parallelism.

### 12.7 Failure handling

The program should fail clearly on missing source data, impossible selections, model fit failures, missing Python packages and inconsistent experimental outputs. One failing E-method should be reported and isolated if the runner can safely continue, but missing or failed predictions must never be misrepresented as valid poor scores.

---

### 12.8 Provisional benchmark and parallel execution baseline for R2

**Purpose:** computational engineering measurement only, **not** predictive research or a scientific ranking. The final R2 design will specify executable commands and the definitive test contract; these points are the user-accepted *baseline direction*.

- **Scheduler:** Python `concurrent.futures.ProcessPoolExecutor`, Windows-safe importable workers and `if __name__ == "__main__":`; 1–12 configurable worker processes, usually one method task each. Worker-internal BLAS/OpenMP threading pinned to one **before importing** NumPy/SciPy; inspect loaded thread pools. An optional memory-safe **24-worker** test measures simultaneous multithreading, not a required production count.
- **Single benchmark system, two settings:** `X` = number of consecutive walk-forward **targets** (preset **B1=1**, **B10=10**); `W` = amount of actual history immediately preceding each target (e.g., **100** or **all eligible**). For a target N, training always ends at N−1; `W` does not mean training on only the target draw. Independent full historical research will later use a separately agreed evaluation plan.
- **Targets:** the `X` draws immediately **before** the frozen latest-ten holdout. With the currently reviewed 444-draw archive, the reserved holdout is **1578–1587**; B1 target **1577** has 433 preceding observations; B10 targets **1568–1577** have 424–433 prior observations. Compare `W=100` and `W=all` on the *same targets*. Never inspect reserved-holdout outcomes when selecting these benchmarks.
- **Timings / resources:** separate startup/import, fit, prediction and orchestration overhead; log wall clock, correctly scoped process CPU time, peak **real process memory**, worker count, versions, NumPy BLAS details and Windows power plan. `psutil` could be useful for native process measurements and must be flagged for venv installation; `tracemalloc` alone does not measure native NumPy allocations reliably. Three repeated runs are desirable when feasible, but configurable for very long methods.
- **No benchmark prediction-merit reporting:** forecast results may be generated **internally solely** for reproducibility checking; publish timings, resources, failure status and comparison digests, **not picks, predictive scores, rank tables or match statistics**. A separately labelled one-history synthetic fair fixture is permissible only as a computational fixture, never a scored real prediction or synthetic calibration claim.
- **Determinism:** seeds derived from stable task identity, **not worker assignment or scheduling order**. One-worker and 12-worker predictions **must be bit-identical** by default under controlled equal conditions; any proposed exception needs justification and prior user approval (§12.5).
- **Failures:** configurable method timeout and memory safeguards; a timeout, crash, out-of-memory or incomplete result is a **failure with available partial durations**, never an invented completion time or a zero-quality valid forecast. Computational cost may influence workload planning, **never method permanence or ensemble eligibility**.
- **Later optimisation only if measured:** possibility of independent synthetic-history/restart tasks, target-block work without future leakage, measured compiled numerical kernels or other acceleration. Warm-start dependent targets remain sequential unless the altered protocol is explicitly specified. No need to move to a free-threaded Python build now.

## 13. Python dependencies and local virtual environment

### 13.1 Agreed packaging approach

Any needed third-party packages must be stated explicitly before use. **Do not install packages globally** into the user's Python 3.14 environment. Use a project-local virtual environment (`venv`) and ordinary `pip` package installation inside it.

The user has **already created and verified** a Python 3.14.8 project-local `.venv`, installed `requests` and `beautifulsoup4` inside it, saved `requirements.txt`, and confirmed both VS Code and ordinary CMD activation. **No new research packages are being installed by this document.** Each additional dependency (e.g., NumPy, SciPy, `psutil`, `threadpoolctl`, or any compiled optimiser) must be proposed explicitly and installed inside this same project venv after agreement.

### 13.2 Preliminary package possibilities — not installation instructions yet

| Package / facility | Possible role | Status |
|---|---|---|
| Python standard library (`csv`, `datetime`, `math`, `statistics`, `pathlib`, `json`, `venv`, etc.) | Basic loading, validation, control, reporting | Available with Python; exact API to design |
| **NumPy** | Arrays, binary occurrence matrices, vectorised operations | Likely useful; version/availability to confirm later |
| **SciPy** | Statistical distributions, optimisation, curve fitting, signal processing | Likely useful for advanced methods; confirm later |
| **pandas** | Tabular transforms and CSV processing | Optional, not mandatory for ~440 rows |
| **scikit-learn** | Regularised models and some machine-learning candidates | Only if the selected experiments need it |
| Other packages | Particular Bayesian, time-series, wavelet, chaos or optimisation approaches | Research and justify individually before adding |

Existing `requests` and `beautifulsoup4` belong primarily to the **separate scraper** and need not automatically become predictor dependencies.

### 13.3 Existing environment: ordinary CMD and VS Code

The project-specific `.venv` **already exists** in the local checkout and is excluded by `.gitignore`. It uses Python 3.14.8, and the local package installation was verified. VS Code has a project-specific Windows Command Prompt profile that activates it; independent Windows CMD sessions can activate it with the user's verified `activate_venv.bat`.

In a **new Windows Command Prompt** already positioned in the repository root:

```cmd
activate_venv.bat
python -c "import sys; print(sys.executable)"
```

Or, without the helper, run `call .venv\Scripts\activate.bat`. To leave the environment, use the verified `deactivate_venv.bat`. From inside VS Code, **new** terminals already activate the same project venv using the checked project terminal profile. No second virtual environment, new system-wide Python configuration or global package installation is needed.

Future selected methods may require additional packages. Propose each dependency and compatible version before installing, use `python -m pip` from this existing environment, and deliberately update `requirements.txt` after verification. Do not recreate `.venv` or overwrite the existing package set merely to draft R2.

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
| Scraper or website change | Upstream HTML or publication changes may interrupt acquisition | Keep collection separate; reject empty or invalid datasets; preserve working CSVs; optional official-source verification must fail closed |
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
11. **Implementation:** Final module structure, CLI design, report formats, worker-pool and benchmark details, numerical backends, per-method runtime limits, package versions and tests; default requirements of 1–12 workers, 32 GB awareness, B1/B10 computational probes and worker-count reproducibility are stated in §12.8.
12. **Future forecasts:** Which methods or combinations to use for a real draw, and how to record the pre-draw commitment.
13. **Independent verification:** What external checks of source data or surprising findings would be most useful?
14. **Drawn-order operational policy:** How will the **operator-labelled drawn-order** view be exposed consistently to each compatible method, distinguished from unordered sets, and annotated with provenance? Optional independent video spot checks can improve source assurance but are not a prerequisite.
15. **Optional external datasets:** Which, if any, provide testable real-time or historical-before-cutoff observations, and with what timestamp provenance?
16. **Synthetic instrumentation:** Which generator families and diagnostics provide useful **separate** sensitivity and identifiability research, while allowing **disclosed design learning** but forbidding substitution of synthetic observations/fit states/scores into real prediction?
17. **Data source robustness:** The repository currently contains two validated 444-row source views. How should future downloader executions prove completeness, detect changed HTML and preserve dated provenance?

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

### 20.1 Recommended next action

**Review and, if acceptable, ratify this coordinated Proposal v0.3**, with `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md` retained as the separate current **R1 research review candidate**. If both are accepted, proceed to **R2**, the formal method-and-architecture specification, rather than conducting a second unspecific R1 literature survey or writing predictor code prematurely. R1 may still expand selectively toward up to 100 additional methods if worthwhile; it is not a quota or R2 blocker.

The R2 draft should address: stable E-identity and variants, source-qualified unordered/drawn-order observations, distinct barrel outputs, exact method mathematics and packages, error/timeout contracts, common data cutoffs, the simple 1–12 process/32 GB performance baseline, B1/B10 timing-only benchmarks, and the bit-identical controlled-worker acceptance test. R3 should later settle prediction scoring, combination evaluation and holdout testing without being pre-empted here.

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

**End of Project Proposal v0.3 — coordinated review/ratification candidate.**
