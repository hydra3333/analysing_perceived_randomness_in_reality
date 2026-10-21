# Australian Powerball: Experimental Investigation of Randomness, Predictability, and Perceived Reality

## Comprehensive project proposal — version 0.1 (discussion draft)

**Prepared:** 21 October 2026  
**Status:** Proposal assembled from the project discussion; **not yet a ratified implementation specification**  
**Primary platform:** Windows 10/11; Python 3.14; local, project-specific virtual environment  
**Initial observation period:** 3 May 2018 onward, under the seven-main-number Powerball format  
**Proposed program naming:** `Powerball_Predictor_v001.py`, followed by versioned successors  
**Experimental method naming:** permanent `E_1`, `E_2`, … identifiers, each paired with an intelligible name

> **Central premise — deliberately unconventional:** This project is an empirical investigation of whether the apparent randomness of real-world Australian Powerball draws hides any exploitable structure. It expressly permits questioning familiar assumptions about probability, temporal independence, causal relationships, connectedness, and even the way we conceptualise perceived reality. We do **not** rule out a method merely because prevailing models say it should not work. Equally, we do **not** pronounce a method predictive merely because it produces an intriguing pattern. All proposals are welcome to be examined; evidence, reproducibility, mathematical consistency, and prospective performance decide what conclusions can honestly be drawn.

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

The game format changed in April 2018 from the previous six-main-number configuration. The requested study deliberately starts **3 May 2018 (draw 1146)**, safely after that change, to avoid silently blending fundamentally different drawing rules. The first qualifying draw and the exact era definition should be cross-checked against the actual data on ingestion, and recorded in the project’s data manifest.

The previous 2018-era rules are relevant to provenance but **not part of the initial modelling dataset**. Any later extension across rule eras will require an explicit methodological decision.

### 3.2 Historical CSV

There is an existing Python downloader/scraper and a growing local CSV containing approximately 440 draws as of October 2026. The agreed starting point is May 2018, and future published draws are to be appended through renewed acquisition.

Expected logical columns are:

`Draw_Number, Date, Ball_1, Ball_2, Ball_3, Ball_4, Ball_5, Ball_6, Ball_7, Powerball`

In the current acquisition source, the seven main balls are displayed typically in **ascending numerical order**. They should **not** be interpreted as the physical order in which balls came out of the machine. The database represents a seven-element **unordered set**, whatever display order happens to be used in the CSV. The single Powerball value is a separate target.

A date-stamped filename such as `australian_powerball_history_20261021.csv` records **file generation/download date**, not the last draw date. The loader should inspect the contents to determine the actual latest covered draw. Files with different retrieval dates can contain the same last published draw.

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

The following are recorded as **agreed project intentions**, not merely assistant recommendations:

| ID | Agreement |
|---|---|
| **A-01** | The purpose is open-ended experimentation into apparent randomness and the possibility of historical predictive information, including challenges to conventional assumptions about reality. |
| **A-02** | Conventional independence assumptions do not provide an automatic exclusion rule for speculative but testable methods. |
| **A-03** | Clearly distinguish an implementable or interesting hypothesis from proven predictive value and from outright mathematical defects. |
| **A-04** | Use current-format Australian Powerball data beginning **May 2018**, rather than combining incompatible rule eras. |
| **A-05** | Treat main-ball and Powerball predictions separately, then produce a combined draw prediction. |
| **A-06** | Use chronological, out-of-sample historical predictions: a model predicting draw `N` sees only eligible information from draws **before** `N`. |
| **A-07** | Support the “last 10” historical-prediction concept; design the retrospective evaluation count to be configurable. |
| **A-08** | Reserve the **latest 10 completed draws** as a final, untouched test set while developing and selecting methods. |
| **A-09** | When deliberately making a **real prediction for the next unobserved draw**, allow the chosen model to use **all currently available history**, including those 10 draws. |
| **A-10** | The recurrence-interval idea concerns reaching or being near a characteristic **optimal interval on the next draw**, **not** simply being the most overdue. |
| **A-11** | Begin with six user-proposed experimental families; later research up to **50 additional candidate methods**, including sophisticated and speculative approaches. |
| **A-12** | Methods have permanent identifiers `E_1`, `E_2`, … and explanatory names, with modular Python implementations and shared utilities. |
| **A-13** | Preserve **every method**, regardless of standalone rank, apparent failure, novelty, or lack of explanatory mechanism. |
| **A-14** | Every method remains eligible for future single-method or multi-method experiments and combinations, subject to transparent criteria. |
| **A-15** | Combination experiments receive new permanent experimental identifiers; qualification and weighting criteria can evolve, with user review and agreement. |
| **A-16** | Score, compare, and report predictions against known draws, but **defer detailed scoring and selection-policy decisions** until the exploratory-method research and design have been discussed. |
| **A-17** | Python **3.14** is the intended implementation platform. Additional packages must be flagged explicitly and installed only into a **project-specific virtual environment**, not globally. |
| **A-18** | Research and method selection come **before writing the predictor**; the project proceeds through discussion and user ratification. |

### 4.1 Important boundary: not everything below is ratified

The proposals that follow include architectural suggestions, validation safeguards, reporting schemes, possible formulas, and research categories from the assistant. Unless they directly restate the above agreements, they are **proposed for consideration**. Their inclusion in a comprehensive proposal must not be mistaken for silent approval.

---

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

- `Ball_1` … `Ball_7` are **display/storage positions**, not necessarily draw-order positions. A model must not infer that `Ball_1` is physically drawn first merely because it is the first CSV column.
- Seven main numbers are distinct within a draw. Selecting independently highest-scoring numbers is straightforward, but models of **whole combinations** may require joint scoring to respect interactions between included numbers.
- A frequency-based probability for one number and a probability for an entire seven-number combination are not interchangeable.
- Ties must be resolved reproducibly or with a declared and recorded random seed.

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
## 8. Research programme for up to 50 additional candidate approaches

### 8.1 Agreement on scope, not pre-selection of winners

After this proposal is understood and accepted as a starting document, undertake a separate **method-discovery and literature-research phase**. The desired scope is **up to 50 additional experimental methods** beyond the six initial user ideas. “Up to” means select for conceptual diversity and worthwhile experimentation rather than padding a list to an arbitrary quota.

Research should not be confined to literature specifically about lotteries or gambling. Useful approaches may come from research on noisy measurements, randomness testing, signal processing, state estimation, change detection, dynamical systems, information theory, time series, nonlinear statistics, machine learning, complex systems, and speculative research traditions.

**This version does not claim that such a literature survey has already been completed** and does not pre-ratify 50 unresearched methods. It defines the scope and standards for that next phase.

### 8.2 Research domains to explore

The following are **search domains and illustrative possibilities**, not yet adopted experimental IDs:

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

For each candidate approach, the research phase should provide:

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

### 11.5 Actual order of drawn balls is not known from ascending CSV storage

If later research proposes hypotheses about first-drawn versus seventh-drawn main balls, the present CSV is **insufficient** to test them. Such an experiment needs authentic, reliably sourced physical draw-order data; alphabetical or ascending storage positions cannot substitute for physical order.

---

## 12. Proposed Python 3.14 design

### 12.1 Software philosophy

Aim for **clarity, reproducibility, modularity, traceability and extensibility** rather than a large monolithic collection of scripts. The project’s small data size means scientific rigour and comprehensible implementations matter more than premature high-performance optimisation.

The user suggested `Powerball_Predictor_v001.py`, with each `E_x` as a separate function (possibly assisted by subordinate functions), plus shared top-level utilities. That remains the initial preferred interface. Splitting into packages or separate experiment modules is an **optional future architecture** if a single file becomes unwieldy; do not treat it as already approved.

### 12.2 Illustrative conceptual components

1. **Configuration and run controller:** Select dataset, time cutoff, mode (development, reserved final evaluation, live forecast), target range, experiments and parameters.
2. **Data loader / validator:** Read CSV, canonicalise dates and unordered seven-number sets, verify integrity, and supply immutable chronological draw records.
3. **Experimental registry:** Map `E_x` IDs and names to implementations, versions, dependencies, parameters, documentation and output adapters.
4. **Shared mathematical utilities:** Counts, recency, gap histories, indicator matrices, numerical fitting, tie handling and careful probability operations.
5. **Individual predictors:** Separate implementation entries for E_1, E_2, etc., with no side effects on each other's data.
6. **Historical walk-forward engine:** Construct permissible training ranges and simulate one future draw at a time.
7. **Combination engine:** Invoke registered methods and combine their historical-only outputs under separately registered `E_x` rules.
8. **Evaluation engine:** Compare stored predictions with actual outcomes, calculate agreed scores and uncertainty.
9. **Reporter:** Produce digestible summaries and full machine-readable results, including low-ranked methods.
10. **Provenance / audit recorder:** Capture source data identities, method/config versions, Python/package environment and random seeds.

### 12.3 Illustrative directory layout (not binding)

```text
powerball/
    Powerball_Predictor_v001.py
    scrape_australian_powerball_history.py
    data/
        australian_powerball_history_YYYYMMDD.csv
    docs/
        Australian_Powerball_Predictive_Randomness_Research_Project_Proposal_v0_1.md
        method_registry.md
        decisions.md
    config/
        research_defaults.json
    results/
        runs/<run_id>/
            manifest.json
            predictions.csv
            per_method_scores.csv
            comparison_report.md
    tests/
        test_data_validation.py
        test_temporal_isolation.py
        test_methods.py
    .venv/                 # local only; not committed
```

The above is a potential end-state structure, **not a request to create it immediately**. If a local Git repository is established, the `.venv`, caches and large/generated run results should be governed by an explicit version-control policy rather than accidentally committed or lost.

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

Record the Python version, library versions, significant numerical options and pseudo-random seeds. Prefer deterministic methods for direct comparisons, or replicate stochastic experiments under controlled independent seeds. Consider tolerances for floating-point comparisons. A performance claim dependent on one lucky random seed is not yet a robust result.

### 12.6 Performance and caching

The dataset is small, but some methods may involve nested parameter searches, many candidate transformations, stochastic optimisation or ensemble combinations. Cache safely reusable historical-only computations and parallelise when worthwhile; **never share a cache across forecast cutoffs if it contains future-fitted information**.

### 12.7 Failure handling

The program should fail clearly on missing source data, impossible selections, model fit failures, missing Python packages and inconsistent experimental outputs. One failing E-method should be reported and isolated if the runner can safely continue, but missing or failed predictions must never be misrepresented as valid poor scores.

---

## 13. Python dependencies and local virtual environment

### 13.1 Agreed packaging approach

Any needed third-party packages must be stated explicitly before use. **Do not install packages globally** into the user's Python 3.14 environment. Use a project-local virtual environment (`venv`) and ordinary `pip` package installation inside it.

No project environment needs to be created and no packages need to be installed **yet**. The user wants guidance when the implementation stage arrives.

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

### 13.3 Illustrative future environment procedure

When approved, a conventional Windows CMD setup could be:

```cmd
cd /d E:\SOFTWARE-Win11\powerball
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
```

The subsequent `pip install ...` packages must be determined from **the ratified research implementation plan**. Versions should be captured in a requirements/lock-style record as appropriate. The user will be guided through this step; no global installations are envisaged.

---

## 14. Proposed research and development phases

These phases are **proposed sequencing**, not permission to proceed automatically. The immediate next phase, once the user accepts this proposal as a working discussion basis, is **research and method-selection discussion**, not implementation.

### Phase R0 — Ratify the project charter and operating principles

**Objective:** Confirm that the written proposal accurately captures the user's intention, especially the deliberately assumption-challenging research philosophy.

**Activities:**

1. Review agreed items A-01 through A-18, distinguishing actual decisions from recommendations.
2. Correct any misinterpretation, particularly around recurrence timing, holdout use, method retention, and the meaning of challenging perceived reality.
3. Establish the proposal's role as project guidance and identify which open decisions belong to later design stages.

**Deliverable:** User-approved revision of this project proposal. **Gate:** No unreviewed assistant recommendation becomes a binding rule merely by appearing in the document.

### Phase R1 — Research the wider experimental landscape

**Objective:** Explore up to **50 additional** potentially relevant analytical and predictive techniques, drawing beyond lottery-specific literature.

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

**Deliverable:** An annotated catalogue of up to 50 additional *candidate approaches*. **Not yet delivered by this proposal:** a completed 50-method literature survey or demonstrated predictive findings.

### Phase R2 — Agree on experimental inventory and definitions

**Objective:** Decide which new candidates become individually specified experiments and how related variants will be identified.

Resolve, for example, whether two alternative curve families belong in one tunable E-method or in separately numbered E-methods, and when a changed scientific question requires a new identity. Retain the first six proposed E-methods as the starting catalogue, with final mathematical definitions subject to review.

**Deliverable:** Versioned method registry with stable names, definitions, inputs, outputs, dependencies, and unresolved questions.

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

Start with deterministic test fixtures and transparent baseline experiments. Provide a script suitable for the user's Windows/Python 3.14 workflow. Record all third-party dependencies and teach installation in a local virtual environment. Confirm that every model sees only allowed historical data for the target draw.

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
- **Rules era:** A pre-May-2018 row must not silently enter the selected training period.
- **Chronology:** Sort by draw date/number as required; detect duplicates and gaps, but do not silently fabricate missing observations.
- **Occurrence indicators:** For each historical main draw exactly seven indicator positions equal one; for Powerball exactly one position equals one.
- **Recurrence calculation:** Explicitly verify the off-by-one convention with hand-worked sequences.
- **Forecast selection:** Select seven distinct main values and exactly one Powerball value, respecting declared ranking and tie-breaking rules.

### 15.2 Temporal non-leakage tests

For any target draw `N`, modify the result at `N` and every later draw in a test dataset. A correctly isolated prediction for `N` must not change. This is a particularly strong automated test for unintended future-data leakage.

Similarly, a model's fitted transformations, hyperparameter selection, calibration, standardisation, and ensemble weights must not use data outside that prediction's permitted information window.

### 15.3 Synthetic-data challenges

Construct artificial histories from known mechanisms, including:

- Ideal uniform independent draws.
- Deliberately biased but otherwise independent draws.
- Periodic or quasi-periodic inclusion processes.
- Abrupt and gradual changes in inclusion propensity.
- Hidden-regime processes and constructed dependencies.
- Adversarial misleading trends that fit the past but reverse later.

These tests check that an E-method can, where appropriate, detect the sort of structure it claims to detect. Success on artificial mechanisms is **not evidence that the mechanism exists in Australian Powerball**.

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
| Hidden rule-era mixture | Combining incompatible ball ranges produces invalid conclusions | May-2018 current-format boundary and source validation |
| Input-data errors or later corrections | False patterns may reflect incorrect draw histories | Validate sequences and ranges, cross-check unusual cases, preserve dataset snapshots and correction history |
| Treating descriptive fit as prediction | Excellent curve fit may have no next-step utility | Walk-forward evaluation, prospective forecasts, separate in-sample diagnostics |
| Instability of fitted models | Tiny changes in the data can reverse predictions | Sensitivity and parameter-stability checks, error bars, versioned configurations |
| Incomparable method outputs | Rankings, raw scores, and probabilities are different objects | Common reporting protocol; distinguish score semantics and calibrate only where justified |
| Retrospective ensemble tuning | Ensembles may look better because built after seeing outcomes | Give combinations separate identities; log selection/weighting rules; evaluate on new data |
| Mistaking correlation for mechanism | Predictive association does not uniquely establish a physical or metaphysical explanation | Separate empirical findings from causal and philosophical interpretations |
| Premature dismissal of an unusual idea | Could overlook a legitimately informative relationship | Preserve and examine all methods; classify objections precisely; allow speculative research |
| Assuming unusual success proves predictive power | Could elevate noise into false confidence | Repeated, independently checked observations, uncertainty analysis, prospective replication |
| Scraper or website change | Upstream HTML or publication changes may interrupt acquisition | Keep collection separate; reject empty or invalid datasets; preserve working CSVs |
| Dependency or environment drift | Results could change as Python libraries evolve | Local `venv`, explicit package/version inventory and controlled numerical seeds |

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

1. **Research catalogue:** Which additional candidate techniques are worth turning into formal methods, and in what order?
2. **Method granularity:** When does a change define a new E-method, as opposed to a parameter variant or version?
3. **Recurrence alignment:** Exact interval convention, robust estimator, appropriate fitting window, and prediction score.
4. **Curve fitting:** Chosen curve families, constraints, forecast extrapolation versus endpoint estimation, gradient definitions, and regularisation.
5. **Distribution fitting:** Candidate families, goodness-of-fit measures, whether probabilities must be calibrated, and how to model sampling without replacement.
6. **Walk-forward programme:** Which historical ranges and evaluation counts will be used for each stage, beyond the agreed last-ten concept?
7. **Holdout policy:** Exact frozen membership and treatment of subsequent data arrivals and re-evaluations.
8. **Evaluation metrics:** Which performance measures become primary, secondary, and exploratory?
9. **Evidence thresholds:** What justifies describing an observed advantage as promising, replicated, or potentially predictive?
10. **Method combination:** Eligibility, weighting, score normalisation, inversion, conditional gating, and ensemble search.
11. **Implementation:** Final module structure, CLI design, report formats, runtime priorities, package versions and tests.
12. **Future forecasts:** Which methods or combinations to use for a real draw, and how to record the pre-draw commitment.
13. **Independent verification:** What external checks of source data or surprising findings would be most useful?

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

Review this proposal for fidelity to the user’s intent. Once the project principles are accepted, commence a **distinct research deliverable** investigating up to 50 additional analytical and speculative methods, with citations and explicit assessments of feasibility and assumptions. Present the candidate inventory for discussion **before writing the predictor program**.

### 20.2 Status distinctions

- **Agreed:** The substantive commitments listed in section 4, as expressed during the conversation.
- **Proposed:** The development sequencing, test controls, architecture, reports, method qualification examples, and governance details beyond the agreed commitments.
- **Deferred:** Specific scoring, technical methods, parameter-selection policies, ensemble rules and implementation interfaces.
- **Not performed by this document:** The promised broad outside research, any actual implementation, any full walk-forward experiment, any claim of improved prediction, and any independently confirmed prospective forecast.

### 20.3 Change management

Future versions should preserve an explicit change summary, distinguish corrected factual statements from revised recommendations, and mark new user-approved decisions. Retired ideas and poorly ranked methods should be recorded rather than silently lost. Proposal revisions should not erase the history of what was tried or rewrite past results after outcomes become known.

### 20.4 Closing project principle

> **We are deliberately willing to challenge the nature of perceived reality, including the usual assumption that past lottery draws contain no predictive information. We will entertain established, unconventional and speculative analytical methods without prejudging their outcomes. Every method is retained, every result can be examined, and claims are strengthened or weakened by transparent, reproducible and genuinely forward-looking evidence.**

**End of project proposal v0.1 — discussion draft.**
