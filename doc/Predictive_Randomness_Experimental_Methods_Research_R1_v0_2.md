# Predictive Randomness — R1 Research Catalogue and Experimental Options

**Version:** R1 v0.2 — expanded research discussion draft  
**Prepared:** 21 October 2026  
**Intended repository location:** `doc/Predictive_Randomness_Experimental_Methods_Research_R1_v0_2.md`  
**Authoritative project basis:** `doc/Predictive_Randomness_Research_Project_Proposal_v0_2.md` (the supplied repository's v0.2 discussion draft, with subsequent user instructions controlling in any conflict)  
**Scope:** original E_1–E_6, **54 additional current research candidates E_7–E_60**, including four pilot-wave-inspired mathematical constructions; a flexible research ceiling of **up to 100 additional candidates** (E_7–E_106 if all are needed), with no quota or requirement to fill the ceiling. Supporting literature, implementation considerations, boundaries and recommendations require user review.  
**This document does not prescribe code, settle scoring, perform historical predictive experiments, or claim a lottery forecasting advantage.**

### R1 v0.2 revision record (21 October 2026)

- **Preserved:** every E_1–E_56 entry and its existing research identity; the source datasets, project philosophy, holdout, and synthetic/real firewall are unchanged.
- **Added:** four pilot-wave-inspired candidate methods, **E_57–E_60**, mapped from the user's accepted C-PW1–C-PW4 proposals. Their shared intellectual origin does **not** mean that quantum effects have been measured in lottery machinery.
- **Expanded:** previous research scope of 50 additional candidates to **up to 100 additional candidates if worthwhile**. This does not authorise 100 implementations, invent 46 more candidates, or impose a target number.
- **Clarified:** valid fixed-size sampling, independent physics-versus-analogy claims, low-dimensional model constraints, optional apparatus metadata, and complete separation of synthetic research from real predictions.
- **Status:** all new mathematical specifications remain provisional pending R2 review; no model was run, optimised or scored in preparing this revision.

## 0. Executive assessment

R1 has found a defensible way to explore all the requested areas: ordinary and heterodox probability models; event recurrence; cross-number and physical draw-order structure; spectral, curve-fitting and nonlinear time-series analysis; information theory; automated learning; symbolic-discovery techniques; and external relationships that could challenge familiar ideas of independence. These are **54 current additional candidate applications to Powerball**, not scientific papers asserting successful lottery prediction; the project may examine up to **100 additional** candidates when warranted. Each has a reproducible mathematical or algorithmic interpretation, an observable target and at least a plausible computational pathway. They have **not yet demonstrated forecasting ability** on these data.

**Governing premise:** the project expressly permits challenging conventional understandings of probability, causality, temporal independence, and the nature of perceived reality. No method is denied implementation because accepted statistical theory predicts no advantage. Inferences, however, are constrained by what tests actually demonstrate. The conventional independent/fair-draw model is an optional *reference instrument* for comparison, never a veto. Neither model redundancy nor low standalone results is a reason to discard a method or bar it from combination experiments.

**Critical user restriction:** Null-world, planted-effect and related artificial-history investigations are **entirely separate projects of evaluation**, and may not select, tune, weight, approve, eliminate or otherwise affect methods or numbers used to predict real draws. Synthetic findings may be described alongside real results only as a clearly labelled independent report; they are not production inputs. Thousands or more synthetic trials are acceptable; their amount is a performance question, not a policy concern.

**Another hard restriction:** no result from any game era with a different count or range of numbers drawn from *either* barrel may enter the core predictive data. The extended pre-April-2018 Powerball suggestion has been rejected. The base era begins with **Draw 1144, 19 April 2018** (seven drawn from 35; one drawn from 20). Machine and ball-set metadata, if discoverable, may be added, but failure to find them must not block R1 or implementation.

---

## 1. Repository evidence and scope of source inspection

The supplied GitHub repository ZIP was inspected, not merely inferred from earlier chat. Its current archive contains the project proposal, the March 2026 South Australian Powerball rules PDF, scraper v0.3, two CSV datasets, VS Code configuration, `requirements.txt`, and the source/data/results directories. A **structural integrity check** compared all rows of both CSVs. That check is not an experimental performance test and did not use or evaluate any candidate predictions.

| Dataset | Repository path | Rows | First and last draw | Assessment |
|---|---|---:|---|---|
| Unordered winning set | `source_data/australian_powerball_history_20261021.csv` | 444 | 1144 (2018-04-19) – 1587 (2026-10-15) | Complete consecutive draw-number range in supplied CSV |
| Reported physical draw order | `source_data/australian_powerball_draw_order_20261021.csv` | 444 | Same | Matches every corresponding unordered set and Powerball value |

**Data check:** 444/444 joined rows agree on draw number, date and Powerball; sorting each seven-number draw-order list reproduces exactly the unordered seven-number list; all draw numbers increment by one from 1144 to 1587. This establishes **internal consistency of the supplied files**, not independent confirmation that every historical result was transcribed correctly. The draw-order CSV includes a Lotterywest result URL for every draw; the earlier scraper also supports an official-source verification run. Before treating provenance as externally validated in a formal report, retain the scraper's run log and, where appropriate, repeat official-source checks.

**Repository file hashes (SHA-256) at research time:**

- `doc/Predictive_Randomness_Research_Project_Proposal_v0_2.md`: `6efc75e5c96bd9af2f16ef8ce3cb210462806512882eb18fa0d18771b3730488`
- `source_data/australian_powerball_history_20261021.csv`: `6dc91efe2f5d3993c9c7247d979a16ad2a5082a4eaa364fad3d6ef9f31ebb1d7`
- `source_data/australian_powerball_draw_order_20261021.csv`: `67a08e278d5fec1226c08db2f90476d19a9ec1d49e8bcca6f4cfc0ddc4037408`

### 1.1 What is and is not established

- **Established from supplied files:** there are two *locally available*, internally matching datasets, including reported draw order. No need to defer all order-related research pending acquisition.
- **Established from the South Australian rules:** the current game specifies seven numbers from 1–35 and one Powerball from 1–20; physical apparatus is a possible but not obligatory observational channel.
- **Established from literature:** the candidate mathematical techniques exist and have uses in other data-generating processes. This **does not** establish they can forecast this lottery.
- **Not performed in R1:** no method-specific walk-forward trial, numerical parameter optimisation, combined predictor selection, holdout scoring, or real future-draw prediction. The most recent ten historical draws have not been used to choose candidate methods.

### 1.2 The only baseline numbers needed to interpret future evaluation

For seven unique picks drawn uniformly from 35, an independently chosen seven-number set has expected overlap **1.4**; a single Powerball guess under uniform 1-in-20 has probability **0.05**. The theoretical standard deviation of main-set overlap is approximately **0.96**. These are descriptive benchmarks **conditional on the reference model**, not a declaration that reality must follow it. A complete joint combination has **C(35,7) × 20 = 134,490,400** possible outcomes under this combinatorial setup; the astronomical combination space is one reason full-combination learning is sparse, not a prohibition on trying it.

### 1.3 Five rules for making the unusual testable

1. **Explicit observations:** define what the unusual hypothesis predicts in recorded variables, even when its physical mechanism is unknown.
2. **Temporal integrity:** at historical forecast cutoff N−1, use only observations **available by N−1**, not merely observations subsequently assigned an earlier calendar date.
3. **Permanent identity:** retain E-number, algorithm and parameter/version identity even if poor, similar to other methods, or theoretically surprising.
4. **Permissive interfaces:** some candidates produce numbers, probabilities, order distributions, conditional signals or diagnostics rather than a neat 35+20 vector. An adapter is preferred to excluding a method.
5. **Distinct reporting:** distinguish *tested predictive results*, *model adequacy*, *internal patterns*, *speculative interpretations* and *synthetic-only sensitivity findings*.

---

## 2. Original six experiments — unchanged research identities

These six are **retained**, not replaced or automatically promoted/demoted by R1 findings. Precise equations and settings remain R2 decisions.

| Method | Existing name | Core research hypothesis | Important design question |
|---|---|---|---|
| **E_1** | Historical Appearance Frequency | Historically frequent numbers may retain elevated relative propensity | Full-history vs recent vs recency-weighted frequency |
| **E_2** | Expected Recurrence-Interval Alignment | A number may be favoured when its **next-draw projected age** approaches an estimated characteristic interval | Gap convention, mean/median/mode/mixture, phase of projected next occurrence |
| **E_3** | Occurrence-Curve Endpoint Forecast | Next-step value of a fitted 0/1 occurrence curve may rank candidates | Curve family, extrapolation endpoint, smoothing and constraints |
| **E_4** | Occurrence-Curve Gradient Forecast | Next-step curve derivative may convey information distinct from level | Slope location, order, scale, curvature and direction |
| **E_5** | Shared Population/Draw Distribution Model | A shared finite-population/discrete model may forecast relative draw propensities | How the seven-without-replacement constraint is modelled |
| **E_6** | Per-Number Fitted Distribution Models | Distinct per-number models may forecast recurrence or inclusion | What is estimated, how sparse data are regularised, shape/parameter choice |

**Refinement of E_2:** define the *target* as the age **at the proposed next draw**, not how long a number has been overdue. Let `d` be the number of intervening draws since the last appearance; a next-draw recurrence could be represented as interval `d+1`. Under the independent reference, expected recurrence intervals are 5 (main-number marginal inclusion p=0.2) and 20 (Powerball p=0.05), but many other fitted timing and shape assumptions are allowed. **Do not conflate the mode, median and mean**: for geometric recurrence, they differ greatly. An estimator choice itself is an experiment.

An early candidate architecture is to preserve the original E-methods and add clearly named variants for alternative kernels, interval estimators and fitted distributions. Never quietly change what an existing E-number signifies.

---

## 3. Research foundations and literature-based methodology

### 3.1 Temporal forecasting is different from explanation

Rolling-origin or expanding-window validation constructs a fresh forecast using only earlier draws, which is the correct historical analogue of a real advance prediction; see [S01]. R1 does **not** choose a particular scoring system. Proper scoring rules are a later option when genuinely probabilistic outputs exist [S02]. Reusing the same history to search many rules can manufacture apparent discoveries; White's data-snooping work provides a relevant interpretation instrument [S03]. In this project, these ideas help describe evidence and potential hindsight effects, not gate-keep heterodox methods.

### 3.2 Nonrandomness, predictability and knowledge of mechanism are distinct

A sequence may exhibit a statistic different from a specified reference, yet still have little next-step predictive utility; conversely an empirically useful forecast can precede an understood causal mechanism. Tests of randomness should not be confused with proof of (un)predictability. NIST explicitly notes that statistical randomness suites cannot certify a generator for all purposes [S04, S05]. A constrained mechanical drawing is **not** literally a cryptographic bitstream, so NIST tests require adaptation to seven-of-35 selection and a separate one-of-20 process.

### 3.3 Numerical methods should preserve the combinatorial sample space

At a minimum, seven main numbers per draw cannot repeat within the draw, and the Powerball is an independent *target variable* in our modelling interfaces (not a proven independence statement). Predictive scores need not be probabilities; if probabilities are claimed, marginal main-barrel inclusion probabilities should sum to **7**, and Powerball probabilities to **1**, assuming the method models valid outcomes. Models of the **complete unordered set** need not reduce to seven independently chosen top marginals. Physical drawing order provides a different output space: ordered seven-number sequences with no repetition.

### 3.4 Broad research categories are intentionally overlapping

Statistics, chaos, symbolic dynamics and machine learning often re-express related functions. Similar forecasts should be measurable as a phenomenon of interest, **not interpreted as permission to drop correlated methods**. Higher method correlation also does not mean methods must have zero ensemble value: near-identical forecasts can differ under particular regimes or counterexamples.

---

## 4. The 54 currently catalogued additional candidate experiments (E_7–E_60)

**Reading key:** A candidate labelled **Established technique / speculative application** uses published mathematics but has **no established Powerball advantage**. **Project-specific experimental construction** means the particular feature-to-prediction mapping is an R1 proposal rather than a directly documented lottery method. **Input codes:** `U` = unordered main-number sets plus Powerball (modelled separately); `O` = reported draw order; `X` = optional externally sourced covariates; `R` = method forecasts/rankings. Some candidates are meaningful only if their prerequisite data or input methods exist. **Cost** is rough relative implementation/development effort (L/M/H), *not* judgement of likelihood of success. Library mentions are prospective only; nothing should be installed until R2/R3 approve.

## 4.0 Quick catalogue by research family

- **Frequency, Bayesian & regime:** 10 additional E-methods.
- **Recurrence & event processes:** 6 additional E-methods.
- **Within-draw structure & draw order:** 10 additional E-methods.
- **Spectral & curve fitting:** 8 additional E-methods.
- **Information, chaos & nonlinear structure:** 8 additional E-methods.
- **Machine learning, external & combinations:** 8 additional E-methods.
- **Pilot-wave-inspired mathematical analogues:** 4 additional E-methods; these use established or deliberately constructed models rather than treating lottery drawings as quantum experiments.

### Numbered candidate index

| E-ID | Candidate name | Required inputs | Effort |
|---|---|---|---|
| E_7 | Bayesian Frequency Shrinkage | `U` | L |
| E_8 | Hierarchical Dirichlet–Multinomial Propensity | `U` | M |
| E_9 | Exponentially Decayed Occurrence Rates | `U` | L |
| E_10 | Multi-Horizon Frequency Contrasts | `U` | L |
| E_11 | Change-Point Segmented Propensities | `U` | M |
| E_12 | Hidden Markov Propensity Regimes | `U` | H |
| E_13 | Latent State-Space Drift | `U` | M |
| E_14 | Calendar-Phase Conditional Patterns | `U` | L |
| E_15 | Historical Epoch Hierarchies | `U` | M |
| E_16 | Biased Without-Replacement Urn Model | `U` | H |
| E_17 | Discrete Recurrence Hazard Curves | `U` | M |
| E_18 | Mixtures of Recurrence Modes | `U` | M |
| E_19 | Periodic Recurrence-Hazard Peaks | `U` | M |
| E_20 | Self-Exciting or Self-Inhibiting Occurrence | `U` | M |
| E_21 | Cross-Number Recurrence Synchrony | `U` | M |
| E_22 | Lagged Event-Trigger Matrices | `U` | M |
| E_23 | Pair Co-Occurrence Propensities | `U` | M |
| E_24 | Higher-Order Triplet Interactions | `U` | H |
| E_25 | Graph-Based Number Association | `U` | M |
| E_26 | Draw-Level Geometry and Summary States | `U` | M |
| E_27 | Nearest Neighbour of Historical Draw Sets | `U` | M |
| E_28 | Markov Transitions of Draw Summaries | `U` | M |
| E_29 | Physical Draw Position Preferences | `O` | M |
| E_30 | Draw-Order Transition Signatures | `O` | M |
| E_31 | Plackett–Luce Sequential Selection | `O` | H |
| E_32 | Permutation/Ordinal Structure of Draw Order | `O` | M |
| E_33 | Fourier and Harmonic Occurrence Forecasts | `U` | M |
| E_34 | Wavelet-Localized Cycles | `U` | M |
| E_35 | Singular Spectrum Analysis | `U` | M |
| E_36 | Gaussian-Process Next-Step Curves | `U` | M |
| E_37 | Spline and Local-Polynomial Extrapolation | `U` | L |
| E_38 | Empirical Mode Decomposition | `U` | H |
| E_39 | Detrended Fluctuation and Long-Memory Features | `U` | M |
| E_40 | Nonlinear Phase and Periodicity Maps | `U` | H |
| E_41 | Context-Tree and Compression Prediction | `U` | M |
| E_42 | Conditional Mutual Information Features | `U` | M |
| E_43 | Transfer-Entropy Directional Signals | `U` | H |
| E_44 | Recurrence-Plot Analogue Prediction | `U` | H |
| E_45 | Delay-Embedded Nearest-Analogue Forecast | `U` | M |
| E_46 | Local S-Map Nonlinear State Forecast | `U` | H |
| E_47 | Lyapunov-Style Instability Conditioning | `U` | H |
| E_48 | Cross-Mapping of Potentially Connected Processes | `U+X` | H |
| E_49 | Regularized Logistic Event Forecasts | `U` | M |
| E_50 | Random-Forest Conditional Patterns | `U` | M |
| E_51 | Boosted-Tree Interaction Discovery | `U` | M |
| E_52 | Reservoir Computing for Latent Dynamics | `U` | H |
| E_53 | Evolutionary Symbolic Regression | `U` | H |
| E_54 | External-Date Covariate Synchrony | `U+X` | H |
| E_55 | Complementarity-Aware Multi-Method Combination | `R` | M |
| E_56 | Adaptive Temporal Method Mixtures | `R` | M |
| E_57 | Fixed-Size Determinantal Seven-Set Model (C-PW1) | `U` (main) | H |
| E_58 | Unconditioned Coupled Latent-Wave Field (C-PW2) | `U` | H |
| E_59 | Draw-Conditioned Coupled Latent-Wave Field (C-PW3) | `U` | H |
| E_60 | Post-Change Non-Equilibrium Relaxation Analogue (C-PW4) | `U`, optional `X` | M/H |

---

### E_7 — Bayesian Frequency Shrinkage

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** L.
- **Experimental question and rationale:** Estimate every number’s latent propensity with a prior and historical appearance counts; shrink noisy extremes rather than treating raw counts as exact probabilities.
- **Proposed next-draw signal:** Rank posterior means, sampled propensity ranks or an agreed credible-bound variant.
- **Technical challenge or potential failure mode:** A prior can dominate sparse evidence; seven main observations per draw are dependent within a draw.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S06.

### E_8 — Hierarchical Dirichlet–Multinomial Propensity

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** M.
- **Experimental question and rationale:** Place a population-level hierarchy on relative number propensities, with separate treatment of Powerball categorical outcomes and main-set selection.
- **Proposed next-draw signal:** Use posterior predictive weights; map main scores through a valid seven-without-replacement construction.
- **Technical challenge or potential failure mode:** A plain multinomial over seven picks is not itself a faithful main-barrel generative model.
- **Possible packages:** SciPy; PyMC optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S06.

### E_9 — Exponentially Decayed Occurrence Rates

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** L.
- **Experimental question and rationale:** Compute appearances with decreasing weight as history recedes; scan multiple decay half-lives without collapsing them into one untracked default.
- **Proposed next-draw signal:** Rank weighted counts or changes in weighted propensity.
- **Technical challenge or potential failure mode:** Highly related to E_1 and E_3 but permanently distinct; recency effect has not been demonstrated.
- **Possible packages:** NumPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S01.

### E_10 — Multi-Horizon Frequency Contrasts

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** L.
- **Experimental question and rationale:** Compare short, medium and full-history estimates to detect numbers whose observed propensity appears to be rising, falling or reversing.
- **Proposed next-draw signal:** Predict using contrasts or a rank over horizon-specific rates.
- **Technical challenge or potential failure mode:** Many window choices invite hindsight selection; require time-available data at each origin.
- **Possible packages:** NumPy, pandas optional. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S01.

### E_11 — Change-Point Segmented Propensities

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** M.
- **Experimental question and rationale:** Detect possible historical breakpoints in occurrence rates, such as changes in equipment, handling or unexplained regimes.
- **Proposed next-draw signal:** Fit probabilities within the most recent inferred segment; preserve breakpoint uncertainty.
- **Technical challenge or potential failure mode:** A detected boundary may be caused by ordinary finite-sample variation; equipment change need not be known.
- **Possible packages:** ruptures optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S07.

### E_12 — Hidden Markov Propensity Regimes

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** H.
- **Experimental question and rationale:** Infer unobserved persistent regimes governing numbers or global patterns, even without direct equipment labels.
- **Proposed next-draw signal:** Estimate regime-conditioned probabilities for the next draw.
- **Technical challenge or potential failure mode:** Regime count and emission parameters can be unidentifiable with approximately 444 observations.
- **Possible packages:** hmmlearn or statsmodels optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S07.

### E_13 — Latent State-Space Drift

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** M.
- **Experimental question and rationale:** Allow smooth or abrupt stochastic evolution of each number’s latent log-odds over draws.
- **Proposed next-draw signal:** One-step forecast of latent state then valid per-barrel rank or probability.
- **Technical challenge or potential failure mode:** Independent per-number latent probabilities must be reconciled with fixed seven-of-35 sampling.
- **Possible packages:** statsmodels, SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S01.

### E_14 — Calendar-Phase Conditional Patterns

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** L.
- **Experimental question and rationale:** Test whether date-derived phase variables (month, week-of-year, astronomical calendar computed in advance) condition rankings.
- **Proposed next-draw signal:** Model next known draw date’s seasonal state and derive number scores.
- **Technical challenge or potential failure mode:** Day-of-week is constant (Thursday), so by itself contains no discriminatory information.
- **Possible packages:** datetime, NumPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S01.

### E_15 — Historical Epoch Hierarchies

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** M.
- **Experimental question and rationale:** Stratify history into explicitly defined epochs and partially pool estimates, allowing regime shifts without requiring known causes.
- **Proposed next-draw signal:** Blend recent-epoch and overall propensities according to modelled uncertainty.
- **Technical challenge or potential failure mode:** Many arbitrary split schemes can yield apparent structure; do not use the held-out draws to choose splits.
- **Possible packages:** NumPy, PyMC optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S06.

### E_16 — Biased Without-Replacement Urn Model

- **Family / inputs:** Frequency, Bayesian & regime; `U`. **Development effort:** H.
- **Experimental question and rationale:** Assign unequal positive physical-selection weights to main balls and use a sequential weighted-without-replacement model, including multivariate Wallenius variants.
- **Proposed next-draw signal:** Generate valid seven-element set propensities and optional ordered sampling probabilities.
- **Technical challenge or potential failure mode:** A two-colour SciPy implementation alone does not solve full 35-individual-weight fitting; may need custom likelihood/sampling.
- **Possible packages:** SciPy; custom Monte Carlo. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S08.

### E_17 — Discrete Recurrence Hazard Curves

- **Family / inputs:** Recurrence & event processes; `U`. **Development effort:** M.
- **Experimental question and rationale:** Fit an appearance hazard as a function of age since last appearance, allowing flat, increasing, decreasing or peaked shapes.
- **Proposed next-draw signal:** Score each ball at its **projected next-draw age**; retain E_2 characteristic-interval model distinctly.
- **Technical challenge or potential failure mode:** Right-censored gaps and interval convention matter; a hazard is not the same as a gap density.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S09.

### E_18 — Mixtures of Recurrence Modes

- **Family / inputs:** Recurrence & event processes; `U`. **Development effort:** M.
- **Experimental question and rationale:** Fit multiple interval components per ball instead of one average return time (e.g., rapid returns plus longer cycles).
- **Proposed next-draw signal:** Use predictive mass/hazard at the next interval under the fitted mixture.
- **Technical challenge or potential failure mode:** Few recurrences per value may make mixtures unstable; no arbitrary minimum likelihood is a theory veto.
- **Possible packages:** SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S09.

### E_19 — Periodic Recurrence-Hazard Peaks

- **Family / inputs:** Recurrence & event processes; `U`. **Development effort:** M.
- **Experimental question and rationale:** Test oscillatory hazard structures, including repeated preferred return ages or beats between intervals.
- **Proposed next-draw signal:** Predict when the next-draw age approaches any fitted harmonic peak.
- **Technical challenge or potential failure mode:** Multiple frequency scans create accidental peaks; phase and draw-index conventions matter.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S10.

### E_20 — Self-Exciting or Self-Inhibiting Occurrence

- **Family / inputs:** Recurrence & event processes; `U`. **Development effort:** M.
- **Experimental question and rationale:** Treat each appearance as a discrete event which might transiently raise or lower later appearance propensity.
- **Proposed next-draw signal:** Use lag kernels with positive or negative signed effects to rank the next draw.
- **Technical challenge or potential failure mode:** Continuous-time Hawkes processes require careful adaptation to a fixed weekly seven-number drawing system.
- **Possible packages:** NumPy; statsmodels optional. No installation is authorised by this research entry.
- **Research character:** Established family / project adaptation. **Reference anchor(s):** S09.

### E_21 — Cross-Number Recurrence Synchrony

- **Family / inputs:** Recurrence & event processes; `U`. **Development effort:** M.
- **Experimental question and rationale:** Examine whether gap phases of one number carry information about forthcoming appearances of another.
- **Proposed next-draw signal:** Construct lagged conditional scores based on pairs of recurrence clocks.
- **Technical challenge or potential failure mode:** Cross-number apparent synchrony can arise from seven picks per draw; conditional controls required.
- **Possible packages:** NumPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S09.

### E_22 — Lagged Event-Trigger Matrices

- **Family / inputs:** Recurrence & event processes; `U`. **Development effort:** M.
- **Experimental question and rationale:** Estimate which numbers tend to appear at selected lags after other numbers or after Powerball events.
- **Proposed next-draw signal:** Aggregate lag-conditioned target candidate scores from the latest observed events.
- **Technical challenge or potential failure mode:** There are many possible lag–number combinations and few examples per cell.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S11.

### E_23 — Pair Co-Occurrence Propensities

- **Family / inputs:** Within-draw structure & draw order; `U`. **Development effort:** M.
- **Experimental question and rationale:** Fit pairwise attraction or repulsion within seven-number subsets, beyond marginal frequencies.
- **Proposed next-draw signal:** Score coherent seven-number candidate sets or condition one number on an emerging set.
- **Technical challenge or potential failure mode:** Pairs within the same draw are structurally dependent even under the uniform reference; avoid equating co-occurrence with next-draw influence.
- **Possible packages:** NumPy, networkx optional. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S12.

### E_24 — Higher-Order Triplet Interactions

- **Family / inputs:** Within-draw structure & draw order; `U`. **Development effort:** H.
- **Experimental question and rationale:** Search for groups of three or more main numbers that appear together unusually or forecast a future group.
- **Proposed next-draw signal:** Score whole-set candidates using sparse triplet signals.
- **Technical challenge or potential failure mode:** Triplets proliferate combinatorially; smoothing and targeted feature sets needed.
- **Possible packages:** NumPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S12.

### E_25 — Graph-Based Number Association

- **Family / inputs:** Within-draw structure & draw order; `U`. **Development effort:** M.
- **Experimental question and rationale:** Build a dynamically updated graph of numerical links: within-draw pairs, lagged transitions or common recurrence phases.
- **Proposed next-draw signal:** Derive graph centrality, communities or predictive edge scores for candidates.
- **Technical challenge or potential failure mode:** Graph structure depends on how edges are defined; centrality alone is not a forecast.
- **Possible packages:** networkx optional. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S12.

### E_26 — Draw-Level Geometry and Summary States

- **Family / inputs:** Within-draw structure & draw order; `U`. **Development effort:** M.
- **Experimental question and rationale:** Encode sum, range, parity mix, adjacent-number gaps, sorted spacing, modular residues and other whole-set characteristics.
- **Proposed next-draw signal:** First forecast next-draw summary state; select a legal set consistent with the preferred state.
- **Technical challenge or potential failure mode:** A sum or parity profile cannot identify a unique set; numeric labels may have no intrinsic physical geometry.
- **Possible packages:** NumPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S12.

### E_27 — Nearest Neighbour of Historical Draw Sets

- **Family / inputs:** Within-draw structure & draw order; `U`. **Development effort:** M.
- **Experimental question and rationale:** Search for previous multi-draw patterns resembling the recent sequence using Jaccard, Hamming, overlap or other set distances.
- **Proposed next-draw signal:** Retrieve the outcomes following similar historical states and rank those outcomes.
- **Technical challenge or potential failure mode:** Small state recurrences are rare; distance choice and inclusion of future outcomes require strict origin cuts.
- **Possible packages:** scikit-learn optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S13.

### E_28 — Markov Transitions of Draw Summaries

- **Family / inputs:** Within-draw structure & draw order; `U`. **Development effort:** M.
- **Experimental question and rationale:** Reduce each draw to a categorical state (e.g., sum band, overlaps, spacing or latent cluster) and model state transitions.
- **Proposed next-draw signal:** Predict next state then estimate conditional number rankings.
- **Technical challenge or potential failure mode:** Full-draw Markov chains are too sparse without controlled state aggregation.
- **Possible packages:** NumPy, scikit-learn optional. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S13.

### E_29 — Physical Draw Position Preferences

- **Family / inputs:** Within-draw structure & draw order; `O`. **Development effort:** M.
- **Experimental question and rationale:** Ask whether a particular ball shows elevated probability of occupying early or late extraction positions.
- **Proposed next-draw signal:** Model each physical position conditional on earlier extracted balls; derive final valid set.
- **Technical challenge or potential failure mode:** Observed positions are dependent due to no replacement; do not treat display-sorted Ball_1 as physical position.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S08.

### E_30 — Draw-Order Transition Signatures

- **Family / inputs:** Within-draw structure & draw order; `O`. **Development effort:** M.
- **Experimental question and rationale:** Model ordered neighbour pairs, distances, reversals or transition fingerprints within actual extraction sequences.
- **Proposed next-draw signal:** Forecast sequential extraction probabilities and aggregate into a seven-ball draw prediction.
- **Technical challenge or potential failure mode:** Adjacency in extraction order does not imply an underlying numeric adjacency mechanism.
- **Possible packages:** NumPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S14.

### E_31 — Plackett–Luce Sequential Selection

- **Family / inputs:** Within-draw structure & draw order; `O`. **Development effort:** H.
- **Experimental question and rationale:** Fit item worth parameters for an ordered without-replacement sequence and test variations allowing draw-specific regimes.
- **Proposed next-draw signal:** Sample or rank full ordered draws; recover unordered seven-number set.
- **Technical challenge or potential failure mode:** A constant-worth model is restrictive; possible physical ball weights and position effects may differ.
- **Possible packages:** custom likelihood; choix optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S14.

### E_32 — Permutation/Ordinal Structure of Draw Order

- **Family / inputs:** Within-draw structure & draw order; `O`. **Development effort:** M.
- **Experimental question and rationale:** Represent an extraction sequence as the permutation of its sorted seven values and calculate ordinal-pattern frequencies/entropy.
- **Proposed next-draw signal:** Predict recurring permutation motifs or condition number selection on historical motif state.
- **Technical challenge or potential failure mode:** Permutations of a random subset have constrained structure; 7! patterns are sparse.
- **Possible packages:** antropy optional; NumPy. No installation is authorised by this research entry.
- **Research character:** Established tool / project adaptation. **Reference anchor(s):** S15.

### E_33 — Fourier and Harmonic Occurrence Forecasts

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** M.
- **Experimental question and rationale:** Fit sinusoidal components to each 0/1 occurrence sequence or a multivariate derived feature.
- **Proposed next-draw signal:** Extrapolate phase and amplitude to next draw, producing relative scores.
- **Technical challenge or potential failure mode:** Edge effects, irregular meaning of period, and frequency-selection overfit are significant.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S16.

### E_34 — Wavelet-Localized Cycles

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** M.
- **Experimental question and rationale:** Analyze components operating at different timescales and changing phase, rather than a stationary single-frequency Fourier fit.
- **Proposed next-draw signal:** Extrapolate most recent selected scales and phases by one draw.
- **Technical challenge or potential failure mode:** Boundary artefacts and few cycles at coarse scales can dominate.
- **Possible packages:** PyWavelets optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S16.

### E_35 — Singular Spectrum Analysis

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** M.
- **Experimental question and rationale:** Use lag-trajectory matrix decomposition to isolate potentially recurrent trend, oscillatory or joint modes in occurrence series.
- **Proposed next-draw signal:** Reconstruct relevant components and extend one step, separately for both barrels.
- **Technical challenge or potential failure mode:** Short binary sequences can yield convincing-looking decompositions of noise; component choice remains a model hypothesis.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S17.

### E_36 — Gaussian-Process Next-Step Curves

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** M.
- **Experimental question and rationale:** Fit flexible kernel-based trends with chosen smoothness and periodic structures, potentially varying across numbers.
- **Proposed next-draw signal:** Predict next-draw latent score or probability after an appropriate link function.
- **Technical challenge or potential failure mode:** Gaussian-process regression on binary 0/1 indicators needs an explicit likelihood interpretation; exact GP classification may be heavier.
- **Possible packages:** scikit-learn optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S18.

### E_37 — Spline and Local-Polynomial Extrapolation

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** L.
- **Experimental question and rationale:** Use smoothing splines, LOESS/local-polynomial fits and controlled boundary extrapolations as alternatives to E_3/E_4 parametric curves.
- **Proposed next-draw signal:** Use one-step curve level or derivative under distinct named variants.
- **Technical challenge or potential failure mode:** Endpoint derivative estimates can change sharply with bandwidth and kernel.
- **Possible packages:** SciPy, statsmodels optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S18.

### E_38 — Empirical Mode Decomposition

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** H.
- **Experimental question and rationale:** Decompose nonlinear/nonstationary series into intrinsic mode functions and study their time-varying phase.
- **Proposed next-draw signal:** Project recent modes one step, then recombine or rank by selected components.
- **Technical challenge or potential failure mode:** EMD endpoint extension and mode-mixing are material issues; not automatically a probabilistic model.
- **Possible packages:** PyEMD package identity to verify before installation. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S19.

### E_39 — Detrended Fluctuation and Long-Memory Features

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** M.
- **Experimental question and rationale:** Estimate multiscale persistence or antipersistence in indicator or summary signals and use the feature to alter forecasts.
- **Proposed next-draw signal:** Condition relative ranks on estimated scale-dependent memory.
- **Technical challenge or potential failure mode:** A Hurst-like exponent is primarily descriptive; convert to an explicit predictive mapping or retain as diagnostic.
- **Possible packages:** NumPy, antropy optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S15.

### E_40 — Nonlinear Phase and Periodicity Maps

- **Family / inputs:** Spectral & curve fitting; `U`. **Development effort:** H.
- **Experimental question and rationale:** Fit piecewise periodic, phase-reset, chirp-like or nonlinear oscillatory mappings rather than fixed sine waves.
- **Proposed next-draw signal:** Extrapolate preferred phase for each number at next draw.
- **Technical challenge or potential failure mode:** Very flexible phase maps can fit almost anything; parameter identity and boundary treatment essential.
- **Possible packages:** SciPy. No installation is authorised by this research entry.
- **Research character:** Project-specific experimental construction. **Reference anchor(s):** S16.

### E_41 — Context-Tree and Compression Prediction

- **Family / inputs:** Information, chaos & nonlinear structure; `U`. **Development effort:** M.
- **Experimental question and rationale:** Learn variable-length conditional patterns in per-number binary histories or finite-alphabet encoded draw states.
- **Proposed next-draw signal:** Obtain next-symbol probabilities from context-tree weighting or related predictors.
- **Technical challenge or potential failure mode:** Compressibility does not automatically mean next-step predictability, especially across encodings.
- **Possible packages:** custom Python / NumPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S20.

### E_42 — Conditional Mutual Information Features

- **Family / inputs:** Information, chaos & nonlinear structure; `U`. **Development effort:** M.
- **Experimental question and rationale:** Estimate whether historical candidate features retain predictive association with next-draw inclusion after conditioning on a simpler history.
- **Proposed next-draw signal:** Transform conditional information into a prespecified ranking/model feature.
- **Technical challenge or potential failure mode:** MI estimates are biased in sparse high-dimensional tables; MI alone is not a predictor.
- **Possible packages:** scikit-learn, SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S11.

### E_43 — Transfer-Entropy Directional Signals

- **Family / inputs:** Information, chaos & nonlinear structure; `U`. **Development effort:** H.
- **Experimental question and rationale:** Examine whether one number’s past contains information about another number’s future beyond the latter’s own past.
- **Proposed next-draw signal:** Produce directed lagged relation weights for the next draw.
- **Technical challenge or potential failure mode:** Transfer entropy is observational and does not by itself establish physical causation; finite-sample estimates are fragile.
- **Possible packages:** IDTxl or custom small discrete estimator. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S11.

### E_44 — Recurrence-Plot Analogue Prediction

- **Family / inputs:** Information, chaos & nonlinear structure; `U`. **Development effort:** H.
- **Experimental question and rationale:** Use phase-space recurrence and recurrence-quantification structure on encoded multi-draw state vectors.
- **Proposed next-draw signal:** Condition forecasts on historical states near the present state in recurrence space.
- **Technical challenge or potential failure mode:** With ~444 draws, embedded high-dimensional spaces may contain few genuine neighbours.
- **Possible packages:** pyunicorn optional or NumPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S21.

### E_45 — Delay-Embedded Nearest-Analogue Forecast

- **Family / inputs:** Information, chaos & nonlinear structure; `U`. **Development effort:** M.
- **Experimental question and rationale:** Construct lag vectors as proxy dynamical states and locate past trajectories similar to the latest observed trajectory.
- **Proposed next-draw signal:** Use successor states of nearest past analogues as candidate forecasts.
- **Technical challenge or potential failure mode:** Takens-style results do not guarantee that a short discrete lottery history admits useful attractor reconstruction.
- **Possible packages:** NumPy, scikit-learn. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S22.

### E_46 — Local S-Map Nonlinear State Forecast

- **Family / inputs:** Information, chaos & nonlinear structure; `U`. **Development effort:** H.
- **Experimental question and rationale:** Use locally weighted linear maps on delay-embedded state vectors, adapting local coefficients to the current state.
- **Proposed next-draw signal:** One-step projection of inclusion-score vector or draw-state features.
- **Technical challenge or potential failure mode:** Neighbourhood scale and embedding dimension consume substantial freedom; no underlying deterministic attractor established.
- **Possible packages:** NumPy, scikit-learn. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S22.

### E_47 — Lyapunov-Style Instability Conditioning

- **Family / inputs:** Information, chaos & nonlinear structure; `U`. **Development effort:** H.
- **Experimental question and rationale:** Estimate local divergence or finite-time instability in an embedding and investigate whether perceived predictable windows exist.
- **Proposed next-draw signal:** Predict with different model dynamics or confidence when local instability signal changes.
- **Technical challenge or potential failure mode:** Lyapunov exponent estimates from short noisy binary series may not be meaningful; this requires explicit operational criteria.
- **Possible packages:** NumPy; nolds optional. No installation is authorised by this research entry.
- **Research character:** Established concept / speculative application. **Reference anchor(s):** S22.

### E_48 — Cross-Mapping of Potentially Connected Processes

- **Family / inputs:** Information, chaos & nonlinear structure; `U+X`. **Development effort:** H.
- **Experimental question and rationale:** Apply nonlinear cross-mapping to test whether a second measured real-world process reconstructs aspects of draw-history evolution.
- **Proposed next-draw signal:** If an external series is timestamp-safe, derive a joint next-step signal.
- **Technical challenge or potential failure mode:** Cross-mapping was developed for coupled dynamical systems; causation cannot be asserted from chance alignments or common seasonal effects.
- **Possible packages:** pyEDM optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S23.

### E_49 — Regularized Logistic Event Forecasts

- **Family / inputs:** Machine learning, external & combinations; `U`. **Development effort:** M.
- **Experimental question and rationale:** Build lagged features (age, previous appearances, pair history, summary state) and fit per-number penalized event classifiers.
- **Proposed next-draw signal:** Predict next-draw inclusion scores separately for main and Powerball; enforce valid output format.
- **Technical challenge or potential failure mode:** Strong regularisation helps numerical fitting but does not prove predictive structure; sparse data and shared training events matter.
- **Possible packages:** scikit-learn. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S13.

### E_50 — Random-Forest Conditional Patterns

- **Family / inputs:** Machine learning, external & combinations; `U`. **Development effort:** M.
- **Experimental question and rationale:** Let shallow trees search for nonlinear combinations of lag, recurrence and draw-summary variables.
- **Proposed next-draw signal:** Aggregate forest predictions into per-barrel ranks.
- **Technical challenge or potential failure mode:** Model flexibility can make in-sample patterns misleading; train only on past-origin features.
- **Possible packages:** scikit-learn. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S13.

### E_51 — Boosted-Tree Interaction Discovery

- **Family / inputs:** Machine learning, external & combinations; `U`. **Development effort:** M.
- **Experimental question and rationale:** Use gradient-boosted trees to discover interactions and state-dependent changes among a bounded lagged-feature set.
- **Proposed next-draw signal:** Next-step predicted inclusion scores, with a legal combinatorial selector.
- **Technical challenge or potential failure mode:** Small samples and many hyperparameters demand transparent frozen variants; keep correlated tree methods.
- **Possible packages:** scikit-learn; XGBoost optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S13.

### E_52 — Reservoir Computing for Latent Dynamics

- **Family / inputs:** Machine learning, external & combinations; `U`. **Development effort:** H.
- **Experimental question and rationale:** Feed multi-draw encoded histories to a fixed recurrent reservoir and fit a regularized readout for the next outcome.
- **Proposed next-draw signal:** Use predicted vector or state embedding to rank candidate numbers.
- **Technical challenge or potential failure mode:** Reservoir computing has forecast chaotic physical systems, not demonstrated a Powerball advantage; few training sequences constrain capacity.
- **Possible packages:** NumPy / SciPy. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S24.

### E_53 — Evolutionary Symbolic Regression

- **Family / inputs:** Machine learning, external & combinations; `U`. **Development effort:** H.
- **Experimental question and rationale:** Search interpretable mathematical expressions of lag, gap, date, draw-order and transformed features without confining the model to standard probability formulas.
- **Proposed next-draw signal:** Evaluate discovered expressions at next known draw with complete history cut-off.
- **Technical challenge or potential failure mode:** Equation search is a very large multiple-try procedure. PySR pulls Julia dependencies and is optional; a pure-Python prototype may be easier.
- **Possible packages:** gplearn or PySR optional. No installation is authorised by this research entry.
- **Research character:** Established technique / speculative application. **Reference anchor(s):** S25.

### E_54 — External-Date Covariate Synchrony

- **Family / inputs:** Machine learning, external & combinations; `U+X`. **Development effort:** H.
- **Experimental question and rationale:** Explore weather, pressure, geomagnetic, lunar/solar, astronomical, geophysical or other independently sourced signals known before a draw.
- **Proposed next-draw signal:** Join timestamp-valid covariates, test lag/phase effects and forecast from the next available or forecast covariate value.
- **Technical challenge or potential failure mode:** External variables require independent historical provenance, location/timezone, missingness and publication-time checks. A speculative connection is not excluded a priori.
- **Possible packages:** requests; pandas; source-specific APIs TBD. No installation is authorised by this research entry.
- **Research character:** Project-specific exploratory construction. **Reference anchor(s):** S23.

### E_55 — Complementarity-Aware Multi-Method Combination

- **Family / inputs:** Machine learning, external & combinations; `R`. **Development effort:** M.
- **Experimental question and rationale:** Combine individual E-method scores/ranks and investigate when even weak or highly correlated methods bring complementary information.
- **Proposed next-draw signal:** Create distinct registered combination method output with optional transformations and weights.
- **Technical challenge or potential failure mode:** No method excluded by standalone performance or correlation; selection and weights must use only the permitted real-training portion, not synthetic findings or holdout.
- **Possible packages:** NumPy, SciPy. No installation is authorised by this research entry.
- **Research character:** Project-specific ensemble construction. **Reference anchor(s):** S03.

### E_56 — Adaptive Temporal Method Mixtures

- **Family / inputs:** Machine learning, external & combinations; `R`. **Development effort:** M.
- **Experimental question and rationale:** Allow E-method mixture weights or switching rules to respond to past observed real performance or state signatures over time.
- **Proposed next-draw signal:** Issue one-step rankings using only prior real-data outcomes and previously frozen update rules.
- **Technical challenge or potential failure mode:** It is easy to choose a winner after seeing the target draw. Requires strict real-time updates, separate E-identity and versioned forecast archive.
- **Possible packages:** NumPy. No installation is authorised by this research entry.
- **Research character:** Project-specific ensemble construction. **Reference anchor(s):** S03.


---

## 4.7 Pilot-wave / de Broglie–Bohm-inspired mathematical family — accepted for R1 (E_57–E_60)

**User decision:** all four proposed C-PW1–C-PW4 candidates are added, without exclusions, and the existing E_1–E_56 remain untouched. They are **analogy-inspired modelling experiments**, not assertions that the lottery machine exhibits quantum wave functions or Bohmian trajectories. The shared provenance of these ideas is scientifically interesting but cannot by itself confer predictive validity. This distinction is about the strength of the *claim*, not a rule for excluding a heterodox experiment.

**Physics background and interpretation.** de Broglie–Bohm theory describes particles with definite trajectories guided by a wave function. Quantum equilibrium can yield Born-rule statistics and an associated notion of absolute uncertainty [S27]. Valentini investigated non-equilibrium distributions and relaxation toward Born-rule statistics [S28]. The existence of these physical theories does **not** supply a measured pilot wave for the draw apparatus. These papers inspire precise mathematical *structures* worth testing on lottery histories. Determinantal point processes (DPPs) and tensor-network Born machines have independent mathematical/machine-learning literatures [S29, S30]. Neither is a validated physical explanation for lottery balls.

**Scope:** the primary sample is unchanged (Draw 1144 onward, seven distinct main numbers from 35 plus one Powerball from 20); physical order can be used where a candidate warrants it, but is not a prerequisite for these four. There is no use of old-rule draws.

### E_57 — Fixed-Size Determinantal Seven-Set Model (C-PW1; Fermion-Style Diversity)

- **Family / inputs:** Quantum-inspired set probability and subset repulsion; `U` main-barrel sets. **Development effort:** H; in-memory 35×35 linear algebra is feasible, but valid learning and probability computation require care.
- **Hypothesis:** the propensity of a *whole* seven-number set may contain structured pairwise exclusion/diversity beyond the combinatorial fact of seven unique numbers. This allows a legal set-level forecast, unlike independent Bernoulli picks.
- **Mathematical construction:** let `L` be a real positive-semidefinite 35×35 matrix. For any seven-element set `S`, define the **fixed-size L-ensemble DPP**:

  `P(S | |S|=7, L) = det(L[S,S]) / Z_7(L)` where `Z_7(L) = sum_{|T|=7} det(L[T,T])` (equivalently the seventh elementary symmetric polynomial of the eigenvalues of `L`).

  Taking `L = I` yields **exactly uniform probability for every legal seven-set**: `1 / C(35,7)`. A diagonal unequal `L` controls item propensities; off-diagonal entries describe similarity and lead to diversity/repulsion **subject to the positive-semidefinite requirement** [S29]. The sample-size constraint itself also introduces negative association, so reported repulsion must not be conflated with mere sampling without replacement.
- **Proposed next-draw output:** full seven-set score/probability; optionally per-number inclusion marginals for compatibility with ranking-based experiments. For a joint draw, select the Powerball via an independently defined one-of-20 model or a separately registered combination method. The Powerball barrel has no interesting seven-set DPP analogue when only one number is drawn.
- **Experiment families / controls to discuss at R2:** identity `L`, diagonal `L`, low-rank-plus-diagonal `L`, constrained similarity features, rolling parameter fits, and comparisons against E_16, E_23–E_24 and E_31. Preserve each variant's identity, regardless of correlation.
- **Critical technical limits:** a standard DPP is *repulsive*; it cannot represent all forms of positive co-selection attraction, and the fixed-size constraint complicates interpretation. An unrestricted 35×35 matrix has far more flexibility than a 444-draw history can identify reliably. Use explicit parameterisation and regularisation as *implementation choices*, not as exclusion gates. Ordinary NumPy/SciPy are potential dependencies; no new package needs installation at the R1 stage.
- **Evidence status:** DPP mathematics is established [S29]; its claimed advantage on Powerball is **unverified**. The quantum/fermion analogy establishes no physical mechanism.

### E_58 — Unconditioned Coupled Latent-Wave Field (C-PW2)

- **Family / inputs:** Latent field, complex amplitudes, coupled oscillations; `U`, with optional covariates only as a separately declared variant. **Development effort:** H.
- **Hypothesis:** a hidden shared dynamical state may contain coupled, phase-dependent temporal structure that can be inferred from past draws and extrapolated, even where each individual number's history is weak.
- **Provisional construction:** define a 35-component complex state `psi_t` and a norm-preserving evolution `psi_(t+1) = U psi_t`, with `U` a constrained unitary matrix (a separate 20-component state for Powerball, if used). Number-specific *weights* are `w_i(t) = |psi_i(t)|^2`. The coupling and phases can create interference-like patterns and common spectral components. A fixed evolution matrix makes norm conservation precise; a time-varying rule would need its own declaration.
- **Crucial sample-space requirement:** `sum_i |psi_i|^2 = 1` describes **one categorical choice**, not a seven-without-replacement selection. To generate seven main numbers, **an explicitly specified legal fixed-size selection rule is mandatory**: e.g., sequential probability-proportional-to-weight sampling without replacement, or a set-level kernel derived from the weights. These options are mathematically distinct variants with distinct probabilities. Multiplying `|psi_i|^2` by seven is **not generally a valid inclusion-probability formula**, since an entry can exceed one and the dependence among seven choices is not defined. A Powerball-only amplitude state directly supports a one-of-20 categorical distribution.
- **What 'unconditioned' means:** given previously fitted initial state and evolution parameters, the latent field evolves without an additional draw-by-draw *state correction*. Past draws are used for **historical model fitting**, so this is not a claim that observed results are ignored entirely. It is also **not** a physical reproduction of Bohmian guidance.
- **Proposed testable output:** next-draw seven-set score/marginals and Powerball score, with explicit comparison against E_33 and other harmonic models whose oscillations are per-number rather than coupled. Record whether measured apparent improvements are due to coupling or merely the added flexibility of a larger parameter family.
- **Model capacity:** a free dense complex coupling model is strongly underconstrained by ~444 historical draws. Consider a sparse/neighbor-coupled, low-rank, banded or few-mode version for an initial *implementation*, but retain unconstrained versions as research leads rather than deleting them. NumPy/SciPy are candidate dependencies.
- **Evidence status:** Schrödinger-style amplitude mathematics and Born-type generative modelling exist [S30]; their **proposed time-evolving use here is a project-specific construction**, not a direct published recipe for forecasting lottery draws.

### E_59 — Draw-Conditioned Coupled Latent-Wave Field (C-PW3)

- **Family / inputs:** Latent dynamics with observation-conditioned state update; `U`. **Development effort:** H.
- **Hypothesis:** observed draw outcomes might provide information that updates an underlying hidden-field state, and that update could improve next-draw prediction over the unconditioned propagation in E_58.
- **Provisional construction:** start with the constrained field and legal fixed-size observation likelihood in E_58. At each completed draw `t`, update a filtered estimate of the hidden state using **only the observed draw available by t**; propagate that posterior/filtered state to make the forecast for `t+1`. An observation-conditioned Bayesian update, measurement-like map or learned state-space filter are possible **distinct, versioned variants**. This is an *analogy* to conditioning and does not claim that a lottery observation physically collapses a Bohmian wave function.
- **Proposed outputs:** one-step-ahead seven-set and Powerball rankings or probabilities; a direct paired comparison with E_58 that isolates the contribution of observation conditioning.
- **Critical constraints:** the next target draw must **never** enter its own latent-state filter or initialisation. A freely learned update rule may memorize the history; specify parameter counting, regularisation and temporal fitting windows at R2. If an update breaks state normalisation or the seven-set sampling rule, re-normalisation and legal-set probabilities must be explicitly defined.
- **Evidence status:** observation-conditioned hidden-state methods are legitimate; the wave-labelled adaptation and claimed predictive potential remain speculative and untested.

### E_60 — Post-Change Non-Equilibrium Relaxation Analogue (C-PW4)

- **Family / inputs:** Transient non-stationarity, change-point and decay models; `U`, optional `X` for **documented, time-available** equipment, ball-set or maintenance events. **Development effort:** M/H.
- **Hypothesis:** a process may exhibit a transient deviation in selection propensities after a change and subsequently relax toward a reference pattern. Motivated by non-equilibrium relaxation analogies in pilot-wave theory [S28], but **not** asserted to be a quantum process in a lottery machine.
- **Provisional mathematical structure:** for ball `i` after an epoch-start or independently documented event `t0`, define a time-dependent deviation such as `delta_i(t) = A_i exp(-(t-t0)/tau_i)`; combine this with a valid probability model for seven-number sets and a separate model for Powerball. Other decay laws (stretched-exponential, oscillatory decay, regime mixtures) may become named variants. The reference tendency need **not** be assumed uniform in all variants.
- **No equipment-data barrier:** first examine **observable** dates within the same-rule period (including the 19 April 2018 rule/equipment transition) as explicitly declared epochs; independently documented apparatus events can improve interpretation if available, but are optional. The primary same-rule dataset has no preceding observations under the *same* conditions before Draw 1144, which limits what an initial-transient model can claim. A variant may infer latent change points using only historical data available at each forecasting origin. Never use a post-event future draw to select a past change point for that forecast.
- **Proposed outputs:** next-draw propensities conditioned on time since a declared/inferred event, plus diagnostic estimates of whether and how a transient changes. Compare with E_11 and E_15, retaining all even if very correlated.
- **Evidence status:** Valentini studies relaxation toward equilibrium in a pilot-wave context [S28]; exponential decay of *lottery draw-number bias* is an **independent speculative hypothesis**, not a result established by that paper. Without documented event metadata, causal claims about equipment are not warranted.

### 4.7.1 Fifth lead: individual guided latent trajectories (not yet an E-number)

A proposal to assign each numbered ball a location in an abstract hidden space and update that location using a fitted guiding field is **retained** as research lead `C-PW5-OPEN`. It has **not** been rejected. Currently, the state geometry, update law, mapping from hidden coordinates to a legal seven-number selection, and identifiable parameter constraints are not determined. Assign a stable E-number once at least one fully testable concrete formulation is proposed; the idea stays visible meanwhile. This under-specification is an actionable design question, **not** a conclusion that the approach is scientifically forbidden or necessarily futile.

### 4.7.2 Distinctions to preserve in R2/R3

1. **Do not infer a mechanism from a fit.** A fitted DPP, coupled oscillation or post-event relaxation is a statistical claim about recorded observations, not evidence that de Broglie–Bohm theory governs the draw mechanism.
2. **Avoid a false equivalence with Pauli exclusion.** Drawing seven distinct lottery balls is sampling without replacement; fermionic antisymmetry motivates a *mathematical* analogy only.
3. **Keep outcome constraints exact.** Seven unique main balls, one Powerball, legal ranges and valid probability normalisation hold for every candidate claiming full probabilities. Candidates may still output non-probability scores if that is explicit.
4. **Keep the original experiments and correlated methods.** E_57 may be related to E_16/E_23; E_58/E_59 to E_33/E_52; E_60 to E_11/E_15. Similarity is a reporting variable, never a veto or reason to discard a model.
5. **Preserve the synthetic/real firewall.** Null-world and planted-effect investigations of E_57–E_60 remain separate and **cannot** choose parameterisations, initial states, coupling strengths, weights, priorities or versions used for real-data predictions. Any real-production choices must follow separately declared methods and permitted **real** observations, not synthetic findings.
6. **Keep the implementation order flexible.** Inclusion of all four is already accepted for R1. We may discuss order based on software dependencies, testability or user preference, but **not** exclude an idea because accepted physics would predict no advantage.

---

## 5. Candidate inventory cross-check and implementation distinctions

The expanded 60-method catalogue above deliberately represents several **different definitions of forecast** rather than forcing every experiment through the same model:

| Kind of output | Illustrative methods | How it could become a valid final prediction |
|---|---|---|
| Per-number scores | E_7, E_9, E_17, E_49, E_58, E_59, E_60 | Rank each barrel separately; top seven main + top one Powerball; E_58/E_59 also require legal fixed-size draw construction when claiming probabilities |
| Full-set distributions or energies | E_16, E_23, E_24, E_57 | Search/sample legal seven-element sets, separately selecting Powerball |
| Physical ordered sequence | E_29–E_32 | Generate seven distinct ordered values, then collapse to unordered set for matching if desired |
| Other descriptive diagnostics | E_39, E_47 | Specify a prospective mapping to ranks or preserve as conditioning/analysis signal |
| External conditionals | E_48, E_54 | Use only data available before the target draw, with missing-input handling |
| Method combinations | E_55–E_56 | Receive predictions/scores from registered E-methods, produce distinct combined rank/forecast |

### 5.1 Why numeric labels may or may not matter

Balls are physical objects with printed identifiers, but their labels also form an ordered numerical system that may or may not be causally meaningful. Statistical notions such as numerical proximity, parity, residues and adjacent numbers are testable constructions; no assumption of a physical relationship between printed labels is required to try them. If two descriptions are observationally equivalent on the supplied history, retain their separate conceptual identities and make the equivalence visible in the reports.

### 5.2 The reported draw order substantially enlarges the problem

An unordered seven-number set has `C(35,7) = 6,724,520` possible values; seven distinct ordered picks have `35 × 34 × … × 29` possible sequences, a factor of `7!` more. That increases expressive power **and** sparsity. The whole-permutation space cannot reasonably be estimated by naive frequency counting from 444 sequences. Position/transition, ordered-choice, ordinal motif and model-based approaches are more tractable than unregularized full-sequence histograms.

### 5.3 Separate barrels — but permit cross-barrel conditioning as a declared hypothesis

The agreement is to **model the two barrels separately**, with their own candidate spaces, predictions and scores. A speculative experiment may nevertheless use *past known Powerball results as a feature for forecasting the next main draw*, or vice versa, without pooling or confusing the barrels. This is a **cross-variable temporal hypothesis**, not combining past number counts in a shared barrel. The method must document the conditioning and report predictions separately for each barrel. If the user intends stricter separation, that is an explicit R2 choice.

### 5.4 Data-hungry methods remain included

Reservoirs, GP classifiers, high-order graph models, CCM and flexible symbolic regression may be difficult to fit informatively from only about 444 draws. **This is a precision/estimation caveat, not an argument for deleting or ruling out the approach.** Variants that require more observations can wait while remaining in the permanent registry. No model will be declared 'impossible' on grounds that an ideal lottery should not be predictable.

### 5.5 Overlapping and complementary hypotheses

Examples of relationships worth investigating *without exclusion*:

- E_1, E_9 and E_36 may respond to similar recent-frequency patterns but differ in temporal smoothness and boundary behaviour.
- E_2, E_17, E_18 and E_19 all concern recurrence timing, yet peak alignment, hazard modelling and multimodal return periods are distinguishable.
- E_23, E_25, E_29 and E_31 examine distinct aspects of dependency in or within sequences.
- E_33–E_40 describe several fundamentally different decompositions of time series; agreement is not independent corroboration without further work.
- E_41–E_48 search for symbols, conditional dependence, reconstructed state or potential coupling; detection does not automatically supply a forecasting rule.
- E_55 and E_56 demonstrate how all preceding experiments — including poor or very highly correlated ones — remain eligible as inputs.

---

## 6. Research programme for external data and unusual connections

The guiding challenge to perceived reality **must be given testable operational meaning**; it cannot be satisfied merely by writing a paragraph about connectedness. R1 therefore recommends an optional external-data schema even before any source has been selected:

- Dataset identity and exact source URL / document metadata.
- Observation timestamp, timezone and location, where relevant.
- **First time the observation was actually available**, including release/publication lag and subsequent revisions.
- What is known *before* a forthcoming draw; distinguish an advance forecast from a subsequently measured quantity.
- Units, sampling frequency, missingness, transformations and precise alignment rule.
- Candidate relationships and lag ranges; numbered feature families that can evolve without erasing prior experiments.
- An external-data-only or combined observation branch, with a description of why it could be relevant; no prerequisite causal mechanism.

**Examples of hypotheses that may later be investigated:** meteorological pressure/temperature, geomagnetic indexes, lunar phase, solar activity, tide cycles, regional electromagnetic measurements, other game outputs under their *own consistent rules*, worldwide public event time series, mathematical constants as phase generators, and cross-domain temporal synchrony. These are **research leads**, not R1 findings. They must not be silently populated from retrospective websites whose values were unavailable before the draw. Numerological-style constructions can be given explicit algorithms and tested; the fact that their mechanism is obscure is not grounds to exclude them, and a post-hoc coincidence alone cannot establish that a mechanism exists.

**Equipment metadata:** Draw machine ID, ball-set ID, maintenance, replacement, operator or site may be sought where publicly recorded reliably. If unavailable, no delay. The actual extraction-order CSV already permits order-based work independent of such labels.

---

## 7. Research methodology: recommended separation of five streams

This separation is proposed as an implementation and reporting architecture; details remain subject to R2/R3 agreement.

### Stream A — Real-data development and genuine forecasting

- Use only validated, same-rule historical observations and eligible external observations known by the applicable cutoff.
- Independently fit each retained method, including poor and related variants; retain every version and outcome.
- Any method selection, ensemble weighting or optimisation used for a **real** prediction is computed **only from permitted real historical data** and declared procedures. No synthetic-analysis scores, rankings, sensitivity thresholds, 'most detectable effects' or generated parameter preferences may feed this stream.
- Hold the most recent ten completed draws untouched for final evaluation until the user explicitly authorises their use; live next-draw predictions may use all completed draws available at the time, with the distinction disclosed.
- Never fill an unavailable real value with a synthetic example and then present it as a real measurement.

### Stream B — Synthetic null-world research, fully isolated

Use synthetic histories generated from **specified artificial rules** (perhaps a reference uniform model) to inspect how each method behaves under that artificial system. The complete pipeline — including variants, combinations and selection operations — can be analysed in this stream. Thousands or more repetitions are acceptable. All synthetic reports and calibration plots are separately titled, stored and labelled.

**Firewall:** This stream does not select, prune, tune, weight or otherwise influence the predictors or forecasts in Stream A. An interesting synthetic finding may motivate a *scientific discussion* or a future separately proposed experiment, but must not be imported automatically as a real-production rule. If a future relaxation is ever proposed, it would require a new user decision and documented charter change; v0.2 forbids it.

### Stream C — Synthetic planted-effect research, fully isolated

Construct artificial sequences containing known effects such as a biased ball, temporal recurrence peaks, a state transition, cross-number coupling, seasonal clocking, a phase shift, or a nonlinear conditional signal. Check which analytic procedures respond and how uncertain the diagnostics are. These results describe detection sensitivity **within the planted-effect world only**.

**Firewall identical to Stream B.** Neither a null-world result nor an artificially planted effect changes a real-data E-method or real forecast.

### Stream D — Source/data integrity and implementation correctness

Check format validity, draw numbers, date chronology, correct barrel boundaries, internal agreement, deterministic function contracts and absence of temporal leakage. Small **test fixtures** to establish code correctness are distinct from synthetic *method effectiveness* research. Correcting a software defect on the basis of a failed unit test is permitted because it restores stated functionality, not because an artificial history happened to reward some real prediction strategy. Any ambiguous boundary belongs in R3 for explicit treatment.

### Stream E — Independent research literature and proposal discussion

May introduce further candidate hypotheses, mathematics or source-acquisition ideas, including radical interpretations. A **published theorem about another domain** is not itself validation on Australian Powerball. External critique and user's evolving ideas can add new methods; the proposal and registry must identify their origin and version.

**Separate folders proposed:** `results/real/`, `results/synthetic_null/`, `results/synthetic_planted/`, `results/data_validation/`; proposed only, not imposed on the repo yet.

---

## 8. Evaluation questions explicitly deferred to R3

The user has reserved detailed scoring design for later. R1 records the questions without deciding them:

1. Exact-match count of main balls, separate binary Powerball match, complete combined prediction and ranking metrics.
2. Whether a method outputs score, calibrated probability, a set distribution, partial order, information feature or confidence diagnostic.
3. How scores from the two barrels are presented jointly without confusing their sample spaces.
4. What historical walk-forward ranges are reported: last ten (held back), last 50/100, all feasible origins and differing minimum-training lengths.
5. Whether to report theoretical reference expectations, confidence intervals, comparison with alternative baseline forecasts and assessment of model-search effects.
6. For methods tuned through real-data results, how to ensure their tuning/backtesting does not accidentally consume the final ten.
7. Whether and when the holdout is retired, frozen, renewed or converted into ordinary training data for real next-draw prediction; subsequent holdout claims must reflect all prior access.
8. How to score methods that naturally emit an ordered draw or joint probability for whole combinations.
9. How to compare models with different input data requirements and missing external data.
10. How to ensure ensemble eligibility for weak or highly correlated methods while limiting accidental hindsight advantage.
11. How to archive **genuine pre-draw forecasts** with hashes and timestamps (a Git commit is one useful option, but timestamps alone may be insufficient without an externally fixed reference).
12. What constitutes a surprising result, how to investigate it and what language is justified in reporting it.

No performance-based exclusion has been authorised by this section.

---

## 9. Candidate software dependencies (research only; no installations requested)

The project's current `requirements.txt` contains `beautifulsoup4`, `requests` and their dependencies; **it does not yet contain the modelling stack**. A pragmatic staged environment plan, to be ratified later:

| Layer | Possible PyPI packages | Why | Caution |
|---|---|---|---|
| Baseline arrays and distributions | `numpy`, `scipy` | numeric matrices, optimisers, distributions, Fourier and signal tools | Check Python 3.14 / Windows wheel availability at installation time |
| Data tables & figures | `pandas`, `matplotlib` | clear input, reports, visual inspection | Optional conveniences; arrays may suffice |
| Regression/ML | `scikit-learn`, `statsmodels` | regularised classifiers, forests, GP, time-series models | Avoid indiscriminate hyperparameter search |
| Segmentation | `ruptures` | regime-change research | Verify prebuilt Windows wheels and Python-version support |
| Symbolic/entropy | `antropy`, `PyWavelets`, `networkx` | diagnostic features, multiscale signals, graphs | `antropy` may add compiled/JIT dependencies |
| More specialised | `hmmlearn`, `pyEDM`, `pyunicorn`, `IDTxl`, `nolds`, PySR, `gplearn`, `PyEMD` | distinct optional branches | Treat names, version support and transitive dependencies as *unverified* until actually needed. `PyEMD` name is ambiguous across different libraries. PySR additionally uses Julia. |

**No dependency installation is requested during R1.** Later installation instructions should use `python -m pip` only after activating the existing per-project `.venv`. Reproducibility should track versions in `requirements.txt` or a future dependency specification. Do not use global pip to install experiment packages.

---

## 10. Explicit R1 recommendations for user decision

**R1-01 — Adopt the 54-current-additional-candidate catalogue for further examination, not as a frozen implementation commitment.** Keep E_1–E_6 and provisional identifiers E_7–E_60; allow up to **100 additional** R1 research candidates (through E_106 if warranted), without a quota. Nothing is rejected due to orthodoxy, low expected performance, weak stand-alone results, or high correlation.

**R1-02 — Allow multiple prediction-output kinds**, especially ranked numbers, valid seven-set models, draw-order models and diagnostics with explicit adapters. Do not silently force a physical-order predictor into a sorted-number time series.

**R1-03 — Treat the supplied 444-row Lotterywest-order file as available input** for order-based research after source validation, not as a reason to defer or to assume its reported sequence reveals bias.

**R1-04 — Put the synthetic firewall in the software architecture from the beginning.** Null-world and planted-effect results have no direct **or indirect** effect on predictions made from real data.

**R1-05 — Preserve the uncompromising method-retention rule.** Correlation between E-methods is a *measurable property*, never a veto. Retain every variant and original method through versioned identities.

**R1-06 — Permit speculative environmental, noncausal and cross-domain associations** where there is a defined observable and time-aligned data. Equipment metadata is optional, and unrelated datasets must not mix historical lottery game configurations.

**R1-07 — Defer exact maths, parameters, packages and scoring to R2/R3** as previously planned. An R1 research profile is neither executable specification nor a claim of validated prediction.

**R1-08 — Consider later follow-up families beyond the 54 currently catalogued additional methods**: e.g., fractal geometry of weighted co-occurrence graphs; cellular-automaton rule searches; Bayesian networks; causal-invariant feature search; topological data analysis; a broader class of information-geometric ensembles; evolutionary portfolio selectors; more exotic astronomy/physics connections. The research ceiling is now **up to 100 additional E-methods if needed**, not a fixed quota, and never a constraint on the project lifetime.

**R1-09 — Incorporate all four pilot-wave-inspired candidates (user accepted).** Map C-PW1–C-PW4 to E_57–E_60; do not claim pilot-wave physics has been observed; keep the fifth unconstrained guided-trajectory concept as an explicitly unresolved lead (`C-PW5-OPEN`).

**R1-10 — Expand research breadth when warranted (user accepted).** Up to **100 additional** E-methods may be investigated on their merits, including highly unconventional methods. No obligation to exhaust the ceiling; all existing numbered entries remain retained, with no predictive-performance exclusion.

### Decisions not assumed by this document

- No method has been selected as a real-world winner.
- No method implementation or parameter defaults have been authorised.
- No statistical significance threshold or final scoring system has been ratified.
- No synthetic-effect finding has been applied to real-data predictions.
- No external feed has been accepted as trustworthy or sufficiently time-indexed.
- No restriction on highly correlated, weak or heterodox methods has been introduced.
- No changes to the scraper or source CSVs are required just to review R1.

---

## 11. Annotated research reference list

The following are **real external references** used to establish the existence, purpose or limitations of mathematical techniques. They are not claimed as evidence that Australian Powerball is predictable. When applying a technique to lottery data was devised for this project, the E-entry says so. URLs were inspected or checked through web search in October 2026.

- **[S01]** Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, §5.10, rolling-origin cross-validation — https://otexts.com/fpp3/tscv.html
- **[S02]** Gneiting & Raftery, *Strictly Proper Scoring Rules, Prediction, and Estimation* (JASA, 2007) — https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf
- **[S03]** White, *A Reality Check for Data Snooping*, *Econometrica* 68 (2000) — https://doi.org/10.1111/1468-0262.00152
- **[S04]** NIST, *SP 800-22 Rev. 1a*, statistical randomness-testing limitations — https://csrc.nist.gov/pubs/sp/800/22/r1/upd1/final
- **[S05]** NIST, *SP 800-90B*, entropy-source assessment (distinct from physical lottery drawing) — https://csrc.nist.gov/pubs/sp/800/90/b/final
- **[S06]** SciPy distribution and empirical-Bayes foundations; standard categorical/Beta/Dirichlet methods — https://docs.scipy.org/doc/scipy/reference/stats.html
- **[S07]** Truong/Oudre/Vayatis, *Selective review of offline change point detection methods*, and `ruptures` — https://github.com/deepcharles/ruptures ; https://centre-borelli.github.io/ruptures-docs/code-reference/detection/pelt-reference/
- **[S08]** Biased-urn / Wallenius framework — https://search.r-project.org/CRAN/refmans/BiasedUrn/html/BiasedUrn-1-Package.html ; https://docs.scipy.org/doc/scipy/tutorial/stats/discrete_nchypergeom_wallenius.html
- **[S09]** Event-history and survival concepts (general) — https://www.statsmodels.org/stable/duration.html
- **[S10]** Harmonic time series components and Fourier foundations — https://docs.scipy.org/doc/scipy/reference/signal.html
- **[S11]** Schreiber, *Measuring Information Transfer*, PRL (2000), transfer entropy — https://doi.org/10.1103/PhysRevLett.85.461
- **[S12]** Number-set / graph representations: NetworkX documentation — https://networkx.org/documentation/stable/
- **[S13]** scikit-learn, supervised learning and random forests — https://scikit-learn.org/stable/supervised_learning.html ; https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- **[S14]** Plackett–Luce ordered-choice models (R documentation) — https://hturner.github.io/PlackettLuce/
- **[S15]** Bandt–Pompe permutation entropy and Python implementations; `antropy` — https://github.com/raphaelvallat/antropy
- **[S16]** SciPy signal processing and spectral methods — https://docs.scipy.org/doc/scipy/reference/signal.html
- **[S17]** Golyandina & Zhigljavsky, *Singular Spectrum Analysis for Time Series* — https://doi.org/10.1007/978-3-662-62436-4
- **[S18]** scikit-learn, Gaussian-process models — https://scikit-learn.org/stable/modules/gaussian_process.html
- **[S19]** Huang et al., *The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis* (1998) — https://doi.org/10.1098/rspa.1998.0193
- **[S20]** Willems, Shtarkov & Tjalkens, *The Context-Tree Weighting Method: Basic Properties* (IEEE Trans. Info. Theory, 1995) — https://www.cs.cmu.edu/~aarti/Class/10704_Fall16/CTW.pdf
- **[S21]** Marwan et al., *Recurrence plots for the analysis of complex systems*, *Physics Reports* (2007) — https://doi.org/10.1016/j.physrep.2006.11.001
- **[S22]** Young & Graham, delay-coordinate dynamics and nonlinear forecasting, *Phys. Rev. E* 107 (2023) — https://doi.org/10.1103/PhysRevE.107.034215
- **[S23]** Sugihara et al., *Detecting causality in complex ecosystems*, *Science* (2012) — https://pubmed.ncbi.nlm.nih.gov/22997134/
- **[S24]** Pathak et al., *Model-Free Prediction of Large Spatiotemporally Chaotic Systems from Data*, *Phys. Rev. Lett.* 120 (2018) — https://doi.org/10.1103/PhysRevLett.120.024102
- **[S25]** PySR symbolic regression and its Julia engine — https://github.com/astroautomata/PySR ; https://pysr.ai/
- **[S26]** tsfresh systematic time-series feature extraction, alternative later branch — https://tsfresh.readthedocs.io/en/stable/

- **[S27]** Dürr, Goldstein & Zanghì (1992), *Quantum Equilibrium and the Origin of Absolute Uncertainty*, *Journal of Statistical Physics* 67, 843–907 — https://doi.org/10.1007/BF01049004 ; accessible manuscript https://arxiv.org/abs/quant-ph/0308039 . Relevant for physical interpretation and its constraints, not lottery forecasting.
- **[S28]** Valentini (1991), *Signal-locality, uncertainty, and the subquantum H-theorem. I*, *Physics Letters A* 156, 5–11 — https://doi.org/10.1016/0375-9601(91)90116-P . Establishes a theoretical non-equilibrium / relaxation proposal in pilot-wave foundations; it does **not** study mechanical lottery equipment.
- **[S29]** Kulesza & Taskar (2012), *Determinantal Point Processes for Machine Learning*, *Foundations and Trends in Machine Learning* 5, 123–286 — https://doi.org/10.1561/2200000044 ; https://mlanthology.org/ftml/2012/kulesza2012ftml-determinantal/ . Establishes DPP subset-diversity mathematics and tractable operations.
- **[S30]** Han, Wang, Fan, Wang & Zhang (2018), *Unsupervised Generative Modeling Using Matrix Product States*, *Physical Review X* 8, 031012 — https://doi.org/10.1103/PhysRevX.8.031012 . Demonstrates Born-rule-inspired generative modelling; **not** the time-varying coupled field proposed for E_58/E_59.

### Source strength and limitations

- The core theoretical sources (peer-reviewed articles, NIST guidance, established statistics texts) establish **methods or cautionary principles**, not a Powerball outcome.
- Maintainer documentation establishes **software availability and approximate capability**, not Python 3.14 Windows-wheel compatibility, which must be checked at installation.
- Multiple E-methods are deliberate **novel applications**, not direct literature replications. This is a feature of experimental discovery and should not be misreported as an externally validated predictive result.
- Bibliographic pages may expose abstracts but not full papers; R2 may need deeper scrutiny of formulas before implementation.

---

## 12. Handback and requested review

R1 v0.2 is ready for the user's critical review. The document is **deliberately broad and non-exclusionary**. Some approaches are plausible for finding physical or statistical departures from an assumed reference; others involve deliberately speculative assumptions about memory, coupling, hidden states and connectedness. None was tested or ranked by predictive merit, and none was barred because conventional theory expects an independent draw.

**Next phase proposed:** R2 — turn the research catalogue into a ratified numbered experiment/variant registry with exact mathematical definitions, feature availability rules and an implementation order determined by logistics and user interest rather than presumed conformity to orthodoxy. R3 can then decide scoring and validation details. The user's original six experiments retain their meaning; the 50 pre-existing additional methods are preserved; E_57–E_60 add the four accepted pilot-wave-inspired constructions. The research ceiling is now up to 100 additional candidates if needed. The rules about the final ten draws, permanent method retention, and complete synthetic/real separation remain binding.

**No program implementing E_1–E_60 has been written as part of this R1 deliverable.**
