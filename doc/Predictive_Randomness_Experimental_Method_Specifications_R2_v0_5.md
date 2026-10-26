# Predictive Randomness — R2 Experimental Method Specifications and Software Contracts

**Version:** 0.5 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026): R2 v0.4 plus the integration of the owner-ratified Method Ranking Measures Proposal v0.5. Predecessor: R2 v0.4 CONSOLIDATED, OWNER-RATIFIED 26 October 2026.  
**Edition status: OWNER-RATIFIED 27 October 2026; R2 v0.4 is historical.** R2 v0.4 (OWNER-RATIFIED 26 October 2026) superseded R2 v0.3 and the operative errata incorporated here; ERR-R2-02/Option F remains PROVISIONAL. Document ratification grants no run, Mode H, holdout, process-termination, scraper/update or scientific-use authority.

**Governing charter:** Owner-ratified consolidated Proposal v0.6 (27 October 2026); Proposal v0.5 remains historical.  
**Research catalogue:** R1 v0.4, unchanged and authoritative.  
**Scope:** Powerball and Oz Lotto, independent per-game runs, approved versioned master data.

> **Project philosophy (binding):** The purpose is to test whether perceived randomness conceals predictive structure—including unlikely, unknown, surprising, or heterodox relationships. Conventional independence and chance models are **reference instruments, never vetoes** on which hypotheses may be researched. Every method remains permanently registered and eligible for future combinations, even if weak, correlated, expensive, unstable, or unorthodox. Sound mathematical bookkeeping and honest prospective testing make unconventional hypotheses more testable; they are not permission to remove them.

## 0. Document controls, errata incorporation and decision classification

The 24 October ratified R2 v0.3 and approved erratum record v0.3 are the historical predecessors. This owner-ratified consolidated edition integrates their operative decisions into the corresponding sections **without withdrawing any unchanged method or acceptance-test contract**. PRECISE authority remains with owner ratification. The ERR-R2 index is:

| Erratum | Current operative location | Status |
|---|---|---|
| ERR-R2-01 | §§9, 10, 12.4, 14; Architecture §§10, 15 | DECIDED, initial workers 1–6 |
| ERR-R2-02 | Architecture §5C, R2 §§9, 14 | PROVISIONAL, never automatic process kill authority |
| ERR-R2-03 | §§12.3, 13 and Architecture §5A.2; R3 §10 | DECIDED, dependency evidence |
| ERR-R2-04 | §5.4 and R3 §§0.4, 2.4 | DECIDED, tie encoding and seed identity |
| ERR-R2-05 | §§1–3, 6, 8, 12–16; R3 §§6, 10 | DECIDED, multi-game/holdout/OPEN as subsequently amended |
| ERR-R2-06 | §§2–4, 5.5, 8–10 and Architecture §20A | DECIDED, master/reader/N−1 and numerical widths |

The prior R2 header's DRAFT statement referred to its authoring time; the owner later ratified v0.3. The 24 October erratum is now a historical predecessor, with its operative decisions incorporated here. Original `[PROPOSED]` mathematical choices continue to be RECOMMENDED or OPEN unless explicitly approved; there is no promotion by consolidation.

Edition 0.5 integrates the owner-ratified Method Ranking Measures Proposal v0.5 (26 October 2026): I-01, the section 2 data paragraph and 2.1 (Oz Lotto supplementary numbers), new sections 2.5, 3.6, 5.6 and 8.4, and pointer lines in 2.4, 4.2, 6.2, 8.1 and 13.2. The protected method inventory (section 7) and 4.1 are unchanged; no other ratified text changes.

---

### 0.3 Change and review requirements [PROPOSED]

- Never edit a ratified file in place: issue v0.2, v0.3, etc. with a meaningful change log.
- A substantive algorithm, data-source policy, fitted objective, conditioning rule or selection-rule change creates a new **version of the method specification** and, when it changes the scientific hypothesis, a **new E-number** by user decision. Do not renumber older E-methods.
- Preserve inactive/blocked/error methods and variants in the registry, not delete them.
- Record both proposed design decisions and what the user has actually ratified. An omission or a default in software is **not** a decision.

## 1. Agreed scientific and operational invariants

**I-01 — Eligible game era:** POWERBALL uses draw 1144+ with 7/35 main and 1/20 PB; OZLOTTO uses draw 1474+ with 7/47 main, with supplementary numbers excluded from every method view, fit, seed, digest and forecast; the evaluator alone may read a target draw's supplementaries to classify prize divisions (section 2.5). No older game configuration may enter any scientific draw-history training, including powerball-only. Development ends at draw 1576 and 1693, respectively.

**I-02 — Two distinct prediction targets:** A method works against the selected game\'s **actual barrel list**: Powerball MAIN and POWERBALL separately, or Oz Lotto MAIN only (7/47). No fabricated Oz PB channel; any permitted cross-barrel covariate remains pre-target.

**I-03 — Reality hypothesis remains open:** A method is not barred because independent-draw mathematics predicts it cannot help. A surprising retrospective match alone is not sufficient evidence of a new physical or probabilistic mechanism; nor is it automatically declared mere coincidence. Explanations are investigated, not assumed, and repeatedly frozen prospective forecasts can add relevant real-world evidence.

**I-04 — All methods retained:** Every E-method and documented variant survives poor results, correlation, numerical expense, synthetic failure, or failure to fit. Inclusion in an ensemble is never forbidden merely by poor stand-alone ranking.

**I-05 — Draw-number temporal availability:** For historical prediction of draw `N`, no result from draw `N` or a later draw may enter fitting, model choice or the forecast. For a FINAL future target `L+1`, all actually completed eligible results through `L` are permitted. Optional external covariates must obey their own declared before-forecast availability rule when used for an honest historical or genuine future forecast. Neither a timestamp nor an external dataset is required for ordinary draw-history-only modelling. Computational warm starts may only carry valid states from earlier forecast origins.

**I-06 — Final historical holdout (historical evaluation and comparison only):** The fixed 1 August 2026 quarantine begins POWERBALL 1577 and OZLOTTO 1694. `FINAL_HOLDOUT_10` is Powerball 1577–1586 and Oz Lotto 1694–1703. No silent shifting, no development exposure, and a holdout used for tuning loses pristine independence; target-1577 E_1 is forecast-only with no result access or score. Mode H / FINAL remain unauthorised.

**I-07 — FINAL next-draw prediction:** FINAL is owner-gated and not open. Once separately ratified for prospective operation, select the latest legitimately completed eligible draw L in the selected game, fit on admissible draws < L+1, freeze before observing target, then score separately. Previously exposed data must be disclosed; no touched holdout may be described as pristine. All previous-owner decisions on freeze and R3 apply.

**I-08 — Synthetic separation with useful feedback:** Synthetic null-world, planted-effect, identifiability and other artificial research is executed, stored and reported separately. It **may** inform disclosed model design, debugging, sensitivity, feasibility, computational priority and interpretation. It must never insert synthetic draws, synthetic fitted hidden states or simulation outcomes into real-history fitting, real forecast outputs or real evidence scores. Synthetic failure cannot disqualify a method or forbid real-data testing.

**I-09 — Draw order:** Published source sequence in accepted masters is `OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`, based on owner interpretation of official published views and separate corroboration. It is not independently verified physical order, and set and order views of the same rows are not independent samples.

**I-10 — Evaluation design separation:** R2 fixes the owner-agreed requirement to preserve TOP and WORST predictions and, after an actual draw, to report their hit comparisons plus rank-position summaries. R3 will finalise their exact computation, statistical aggregation, uncertainty, comparison, interpretation and qualification **before the first genuine FINAL forecast**. Rank-position measurements are never inputs to pre-draw selection or prediction. No R2 benchmark evaluates predictive merit.

**I-11 — Compute availability:** One process per E-method, configurable **1–6** worker processes initially (six default/maximum), one-thread numerical libraries in a worker; higher-worker evidence trials are not initially required. Beyond six, owner-approved extension is required. Runtime and scientific eligibility are separate.

**I-12 — Same-input determinism:** On the same host and pinned software/numerics configuration, **1-worker and 6-worker predictions must be bit-identical by default**; exceptions require a specific documented technical reason and explicit user approval, not an automatic tolerance waiver.
**I-13 — Interpretation must remain empirically open:** A surprising retrospective result or real-world forecast is not automatically dismissed as a coincidence, synthetic artefact or implementation error merely because it conflicts with a conventional reference model. Interpretations remain **provisional** until sufficiently investigated, including repeated properly frozen genuine future predictions as appropriate. Conversely, repeated apparent wins are not automatic proof of a novel mechanism, and failures are not automatic proof of impossibility. Distinguish a **verified programming/data defect** (which can be established by direct inspection or independent reproduction) from an **unconfirmed explanation** for unusual prediction results. R3 will specify evidence standards; R2 shall not prelabel outcomes as invalid or confirmed discoveries.


**I-14 — Two simultaneous inverse-direction predictions, never post-hoc:** For every ranking-capable method, the original/native TOP forecast and the WORST/INVERSE forecast are **both determined, archived and presented side by side before the draw**, from the same fitted method and frozen ranking; unavailable outputs are explicitly unavailable. A later actual result cannot choose which direction to call successful or modify either selection. Primary joint-set TOP rules retain their native identity.

**I-15 — Rank position cannot influence TOP/WORST:** The rank-position evaluation is computed **only after the actual target result is known**, from rankings already archived before that draw. Its result and its mid-rank treatment of ties cannot affect TOP/WORST selection, ordering, fitted parameters, tie-breaking, or the immutable pre-draw forecast. Any future proposal to use rank-derived information as a new **separately declared predictive hypothesis** would require a new approved method/variant and prospective testing; it cannot silently redefine the existing outputs.

**I-16 — Permitted-input identity:** For any historical target, predictions, stochastic seeds, warm starts and canonical forecast content must be invariant under modifications or additions of results at `N` and later. Whole-source hashes are provenance metadata and cannot influence forecasts. Perturbation tests must enforce this even in feature preparation and caching.

**I-17 — Prospective batch integrity:** Every genuine target receives one immutable, pushed-before-the-draw registered-method/variant batch, including TOP/WORST when available and explicit unavailable/failure statuses. Later actual results and analyses are separate; never retrospectively populate a missing prediction in that batch. Genuine forecasting starts on the owner's chosen schedule after agreed preparations.

---

## 2. Current data contract and admissibility

**Current development data (25 October 2026, master version 1):** `POWERBALL` draw 1144–1576 (433 rows; master SHA-256 `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8`) and `OZLOTTO` draw 1474–1693 (220 rows; master SHA-256 `4a6cecc27fb6a5b8aafc0451858f1ea00f31c0eaf83c15c6ba66a0940e83f93f`). Authoritative versioned files are `source_data/<GAME>_results_master.csv`, `source_data/<GAME>_results_master_ledger.csv` and `source_data/<GAME>_results_master_init_verification.json`; the `INIT` ledger record and initialisation record bind these identities. These are the owner's accepted development masters, confirmed by Claude against Git HEAD `3ddb8a6` on 25 October 2026; verify identities again against the current Git HEAD before coding. Lotterywest's ordinary results-search pages were acquired with the committed owner-run tools. The published number sequence is **`OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION`**, not verified physical drawing order. Three supplementary Oz Lotto labels are never method inputs; the evaluator alone may read a target draw's supplementaries, after the target is opened and its forecast frozen, solely to classify prize divisions (R2 section 2.5). Results from 1 August 2026 onward are quarantined: Powerball 1577+ and Oz Lotto 1694+. `FINAL_HOLDOUT_10` is Powerball 1577–1586 and Oz Lotto 1694–1703; development caps are 1576 and 1693, respectively. The E_1 target-1577 regression is strictly a *forecast-only* exception using 1144–1576, not a permission to read or score its outcome. These constraints are normative in R2 v0.5 (data/views) and R3 v0.5 (evaluation/freeze).

**Current training and numeric contract:** Each target N is fitted afresh on only eligible preceding draws, with `int64` internal and output integer arrays and `float64` floating arrays, and readonly isolated owned prefix views. The entire master may be SHA-256 hashed bytewise for integrity, but row N and later must not be parsed/converted; the whole-master hash must not determine model features, seeds or forecast content. Dates are optional and digest-bound when consumed; ordinary E_1 view digest stays unchanged. Automatic dependency install-and-upgrade is retained, but requires offline suites and golden/boundary checks to PASS before further work, and is prohibited between freeze and score or within Mode H. Incremental fit caches require reviewed byte-identical equivalence to scratch fit.



**Cross-game machine identity (ERR-R2-05, DECIDED):** A draw is identified by the structured pair `(game_id, draw_number)`; a draw number alone is not globally unique. The derived `draw_key` (for example, `POWERBALL_1576`) is a **display-only** convenience and must never replace those two machine fields in a method request, dataset, run/status record, frozen forecast or scoring lookup. The older Powerball-only records lacking `game_id` may be interpreted through an explicitly versioned legacy compatibility rule, not silently rewritten. Each game's provenance, development, holdout, synthetic and result namespaces remain separate.

### 2.1 Accepted source file roles (DECIDED)

Use only the pinned `source_data/<GAME>_results_master.csv` matched to its `source_data/<GAME>_results_master_ledger.csv` and corresponding init verification record. Versions are immutable; an authenticated whole-file SHA reads all bytes **without decoding** later rows, but the scientific loader first filters raw `Draw_Number` and **never parses or converts any field in row N or beyond**. Reject master symlinks and unexpected hard links, and never pass unrestricted table/master paths to method code. Old two-CSV inputs and direct API/saved-web-page parsers are historical, not current scientific sources. The scientific result seed/digest uses permitted-view data only; master SHA is provenance only. Plain date fields are opt-in and date consumption changes the digest schema; the legacy E_1 digest remains frozen. Oz Lotto supplementary labels remain structural checks only for every method-facing reader and view; their only other use is the evaluator-only division scoring of section 2.5.

**R2-C01 [DECIDED, as amended]:** A canonical versioned per-game `DrawRecord` comes from the accepted master and ledger pinned to the run. `UNORDERED_SET` and `OPERATOR_DRAWN_ORDER` are two logical representations of one draw, not independently counted CSV sources; `PAIRED_DIAGNOSTIC` combines them for diagnostics only. Preserve raw provenance and fail closed on master/version disagreements.

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

**R2-C03 [DECIDED, current validation]:** For each pinned accepted master version verify its full SHA-256 against the per-game ledger INIT/version row and its verification record, the game-specific 433 (POWERBALL) or 220 (OZLOTTO) development rows as at master v1, legal ball shapes/ranges/uniqueness, date cadence and draw-number continuity through the declared cap. Master SHA reads all bytes without decoding. A target-specific scientific reader filters raw draw-number text first and parses/converts no fields in row N or beyond. New accepted versions require independent evidence; no `L` or first-draw target is silently hard-coded from the October 2026 quarantine suffix.

**R2-C04:** An optional order sequence must consist of exactly the same seven numbers as `main_set`, once each. A missing or unverifiable order view may block an **ordered** variant, but it must not block compatible unordered methods or remove them from the registry.

### 2.3 Primary draw-number control; optional external data [AGREED/PROPOSED]

**The core forecast engine is indexed by actual draw number, not clock time.** Each historical evaluation target `N` gets only the valid draw rows `1144 .. N-1` (or an approved shorter history window); a FINAL prediction for next draw `L+1` gets all available valid rows `1144 .. L` (subject only to that method's mathematical window definition). The existing `Date` field is retained as metadata for checking weekly continuity, displaying results, and supporting future date-related hypotheses. **No exact timestamps are required for ordinary draw-result prediction, benchmark fitting or historical-score matching.**

**External observations are entirely optional.** If a later E-method proposes weather, apparatus changes, astronomical phases, external signals or other phenomena, R2/R3 must separately define its temporal indexing and admissibility. Some may be unambiguously linked by **draw number or calendar date**, needing no exact clock time. Where publication/release time matters to prove a feature was actually knowable before a historical or genuine future forecast, record the available publication date/time to the **precision necessary for that hypothesis**; do not invent missing times. A same-day value released only after a draw is not allowed to masquerade as a pre-draw predictor merely because its observation date matches. If only retrospective alignment is supported, it may still be studied in a **separately labelled retrospective-association mode**, explicitly not assessed as an advance prediction. This preserves unconventional investigations rather than excluding them.

**R2-C05:** The runner constructs an immutable **draw-number-limited** source view: for historical target `N`, rows `< N` only, and for FINAL genuine future target `L+1`, all validated actual rows `<= L`. Methods cannot access the target's unknown actual result, global post-target observations, scoring tables or other time-leaked derived information. For the **development** namespace, the frozen holdout outcomes additionally remain inaccessible. For an **authorised FINAL** namespace, the holdout rows are accessible because they are completed past draws. The forecast method does not receive future outcomes through hidden metadata or helper functions.

**Separate proof-of-prior-forecast from model features.** A prospective forecast should be archived before the target is drawn, with immutable bytes, a digest and some verifiable creation/commit evidence. Such an audit record may contain a wall-clock timestamp or Git commit metadata; that timestamp **is not a required predictive input** and does not alter the draw-number forecasting logic.

### 2.4 Separate dataset namespaces and provenance [PROPOSED]

Every run has one explicit namespace: `REAL_DEVELOPMENT`, `REAL_HOLDOUT`, `REAL_PROSPECTIVE`, `SYNTHETIC_NULL`, `SYNTHETIC_PLANTED`, `SYNTHETIC_IDENTIFIABILITY`, or `BENCHMARK_REAL` / `BENCHMARK_SYNTHETIC`. Each stores results in a segregated directory and writes a namespace manifest. A benchmark run carrying real history is **not** a training-data augmentation and never scores or exposes benchmark predictions. In-sample diagnostic runs (section 8.4) use their own separate namespace, `IN_SAMPLE_DIAGNOSTIC`.

### 2.5 Oz Lotto supplementary numbers: evaluator-only scoring use (DECIDED, MRD-03)

Owner-ratified on 26 October 2026 in the Method Ranking Measures Proposal v0.5 (proposal section 8).

**Earlier ratified text (replaced by this rule on 26 October 2026):** in R2, Architecture section 0 and the Proposal: "Three supplementary Oz Lotto labels are provenance only and never become scientific inputs"; supplementaries are "excluded from every method view/scorer".

**Replacement rule:**
- The Oz Lotto supplementary numbers of a **target** draw may be read **by the evaluator only**, after (a) the target's outcome is opened and (b) the track's frozen forecast for that target exists.
- They are used solely to compute `supplementary_matches` and the prize division.
- They remain excluded from every method view, fit, seed, view digest, readout and forecast.
- Methods never forecast supplementaries.
- The main and Powerball match channels are unchanged, and Oz Lotto has no Powerball channel (`ABSENT`).
- The master already stores `Supp_1..Supp_3`, so there is no data change.

**Scope confirmed by the owner:** scoring and measuring only, never predicting. Using supplementaries as method inputs would be a separate scientific decision, outside this rule.

---

## 3. Historical cutoffs, training windows and holdout boundaries

### 3.1 N-1 principle [AGREED]

For a historical target draw `N`, a method may fit to eligible draws **1144 through N−1 inclusive**, or a declared most-recent subset ending at `N−1`. It must not inspect any result or derived value from `N` or later. This includes hindsight-fitted trends, smoothed series using future boundary points, fitted transforms, extracted optional covariates, precomputed full-history similarities, model-selection heuristics and state initialisers. **The evaluator** may subsequently compare the frozen prediction for `N` with the known actual record for `N`, without returning that outcome to the predictor.

**R2-C06 [PROPOSED]:** The runner constructs a `ForecastRequest` containing an explicit target ID, last accessible draw, a frozen source digest, a named data-view policy, a training-window policy, reproducible seed identity, and an execution namespace. Method functions receive only this object plus their permitted training records.

### 3.1A Derived weekly date integrity and game-local refusal (ERR-R2-05, DECIDED)

Each approved immutable game-era profile includes `first_draw_number` and `era_start_date`. For a valid current-era draw number `N`, derive its weekly calendar date as `era_start_date + 7 days × (N − first_draw_number)`. The game-specific structural source validator compares source and derived dates across accepted master rows, including quarantined rows **only through its separately restricted, value-free audit capability**. This does not authorise an N−1 scientific method or its loader to decode or convert any field from row N or later.

Any discrepancy produces a prominent **value-free warning** (bounded status/count/field identity; no held-out ball values). It **stops all date-dependent methods for the affected game**, including E_14, E_54 and approved equivalents, pending an explicit owner decision. It does **not** automatically stop unrelated `UNORDERED_SET` methods when their independently required data remain valid. Dates are calendar dates only; no timezone or draw clock is fabricated. E_54's external-feed information-availability contract remains OPEN, and this calculation does not approve its execution.

### 3.2 Current benchmark targets, pre-quarantine (DECIDED)

- POWERBALL B1: target 1576, trained on 1144–1575 (432 prior draws); W=100 trains 1476–1575.
- POWERBALL B10: targets 1567–1576, with 423–432 preceding draws; every target fitted anew using its strict prefix.
- No development or timing benchmark reads quarantined outcomes, including draw 1577. The independent frozen E_1 target-1577 regression is forecast-only and never scored; see §5.5 and the exposure record.
- Extend to Oz Lotto only by separately approved matching per-game target windows bounded at 1693; no implied Oz method run authorisation.

**R2-C07 [DECIDED, as amended]:** B1/B10 use X=1 or X=10 development-only target origins ending at 1576, with W=100 or W=ALL_PERMITTED preceding observations; ten timing targets never means ten training draws. Additional settings must be declared, and no benchmark touches the quarantine.

### 3.3 Windows and warm starts [PROPOSED]

- `EXPANDING`: available history from the first eligible draw through N−1.
- `ROLLING_W`: most recent `W` eligible draws preceding N.
- Minimum viable sample size is a **method-specific, reported requirement**, not a reason to delete a method. If history is insufficient, status `INSUFFICIENT_HISTORY` is recorded without inventing a forecast.
- A warm start used for target N may come only from earlier legitimate target states, with code/config/data lineage recorded. Warm-start chaining prevents indiscriminate parallel execution of consecutive origins; alternate cold-start target blocks are separately declared computation variants.
- If a method refits only every `k` draws, this is an explicit, versioned policy. Never silently treat a stale fit as a new fit to N−1.

### 3.4 Holdout lifecycle (DECIDED boundary, OPEN release)

The fixed 1 August 2026 boundary is binding; per-game FINAL_HOLDOUT_10 remains sealed and cannot silently shift. A held-out sample used for method design, tuning, ranking or software selection is not pristine for that method and must be disclosed. Read-only structure auditing may report bounded pass/fail, counts and field names but **never quarantined ball values**, including through charts, fixtures, dumps and exceptions. The future Mode H opening, one-draw-at-a-time release and FINAL are OPEN and unauthorised; see R3 §6, §10.

### 3.5 Two operating modes and the genuine-forecast cycle [AGREED; execution gate CLOSED]

**HISTORICAL_EVALUATION:** For eligible target N, fit anew on the approved same-game prefix through N−1, freeze prediction, then and only then hand its saved identity to a separate evaluator with lawful target outcome access. The development range ends Powerball 1576 / Oz 1693. The E_1 1577 case is an immutable **forecast-only** regression without result access or scoring.

**FINAL_NEXT_DRAW:** Defined but not yet authorised. When the owner opens prospective operation after acceptance, determine L from the current completed eligible game history under an approved isolation/freeze protocol, fit afresh on all applicable pre-target draws (or a preregistered method window), freeze and publish the complete batch before the target draw, and evaluate only after the outcome becomes known. Earlier holdout use must be disclosed, and any previously tuned/observed holdout ceases to be pristine. Future Mode H sequential outcome release is OPEN; nothing in a proposed record schema authorises its execution.

**R2-C07A [DECIDED as a contract; no execution enabled]:** Workflow names remain `HISTORICAL_EVALUATION` and `FINAL_NEXT_DRAW`. The manifest includes `training_last_draw_number` derived from allowed draw numbers: at most N−1 for historical, exactly validated L for an approved FINAL forecast. The builder may not interpret ordinary holdout rows as a default FINAL training exclusion once FINAL is separately authorised.

### 3.6 Numbering conventions (DECIDED, MRD-11)

Owner-ratified on 26 October 2026 in the Method Ranking Measures Proposal v0.5 (proposal 3.2). They apply project-wide.

There is no zero-based or one-based re-indexing of draws. Where R2/R3 already fix a convention, it is used unchanged.

| Quantity | Convention |
|---|---|
| Draws | Always by **official draw number** (for example Powerball 1286), never by position. |
| Ball labels | Printed values: Powerball main 1-35, Powerball 1-20, Oz Lotto 1-47. (Existing convention.) |
| Rank positions | **1-based, 1 = best.** Matches R3's mid-rank convention (1 = highest predicted). |
| Training set for target N | Era first draw through N-1 inclusive (R3 section 17.3.3). |
| Draw-number gap, a < b | b - a; consecutive draws have gap 1. |
| Scored-opportunity index | Within a stated comparison set C, sorted by draw number, the 1st scored target has index 1, the 2nd index 2, and so on (R3 section 17.3.8). |
| Counts | Plain counts from 0. |
| Internal array indices | May be 0-based internally; **never** appear in records, files, file names or reports. |

## 4. Single common ordered/unordered observation policy

**Current scientific view contract (ERR-R2-06, DECIDED):** `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, and `PAIRED_DIAGNOSTIC` are caller-selected observations of the same approved prefix, never separate independent draw samples. `OPERATOR_DRAWN_ORDER` is expressly an owner assumption. Every numeric table and NumPy `DrawView` uses `int64` integers and `float64` floating-point data, with an owned immutable byte-backed prefix-only view and no `.base` chain exposing later values. A method only receives `DrawView`, not the master path or full table. The selected view is frozen in method configuration/manifest, not enforced through a duplicate entitlement registry; the scientific result-schema/data-kind/variant allowlist remains empty until owner review. Dates opt-in with own schema/digest. No N-or-later parsing; see §2.1.



**R2-C08 [DECIDED, ERR-R2-06]:** Define `observation_view` per method variant from `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, or `PAIRED_DIAGNOSTIC`. This is a shared policy for all E-methods, not 62 independent ad hoc definitions.

- `UNORDERED_SET`: the observation is exactly the seven-number set; sorting is only a storage convention. The likelihood or model ignores the originally reported extraction order.
- `OPERATOR_DRAWN_ORDER`: the observation is the ordered sequence of the seven numbers as published by the operator. Only methods with a valid ordered model may consume this view (for example sequential weighted selection).
- `PAIRED_DIAGNOSTIC`: a controlled comparison of two fitting/view configurations using the **same actual draws**, clearly labelled as paired views rather than independent draws. **No double-likelihood multiplication** for a set and its own order unless the joint factorisation is mathematically specified and does not count the same event twice.

**R2-C09 [DECIDED, ERR-R2-06]:** The view selected, source identity, ordered likelihood formula and tie or unavailable-order treatment are included in the model configuration and forecast manifest. Switching `UNORDERED_SET` to `OPERATOR_DRAWN_ORDER` does **not automatically** create another E-number; it creates a separately versioned, retained experimental **variant** unless its underlying scientific question changes and the user approves a new E-identity.

**New scientific-view identity (ERR-R2-05, DECIDED):** Every **new** permitted observation-view schema in either game—including any new Powerball E_2+ `UNORDERED_SET`, ordered, `PAIRED_DIAGNOSTIC`, derived-date or external-input schema—binds `game_id`, game era and immutable profile version in its domain/schema and permitted-view digest. Dates are incorporated when a method actually requests them, creating an explicitly new view schema/digest. The **sole legacy exception** is `E1_REAL_U_TRAINING_VIEW_V1`, whose existing Powerball domain, canonical encoding and frozen digests must remain byte-for-byte unchanged. A master/ledger whole-file SHA is provenance and never substitutes for the permitted-view digest, seed or predictive-content identity.

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
- Per-channel probability capability (`main_probability_kind`, `powerball_probability_kind`) is declared under section 5.6, field 3, and is never inferred from arbitrary scores. The ranking measures MR6 and MR14 (R3 section 17.6) use it.

---

## 5. Forecast result schema and method adapter contract

### 5.1 Supported output types [PROPOSED]

A method may produce one or several typed channels, without inventing unsupported outputs:

1. `MAIN_RANK`: a **complete frozen ranking of all 35 labels** (and original 35 scores when available) for every ranking-capable method. Store the full order, tie groups and deterministic prediction-time tie resolution; a top-seven-only list is insufficient.
2. `POWERBALL_RANK`: a **complete frozen ranking of all 20 labels** (and original scores when available) for every ranking-capable Powerball component. Store ties separately from the deterministic prediction ordering.
3. `MAIN_MARGINAL_PROB`: 35 valid inclusion probabilities derived from or justified by a legal 7-set model.
4. `POWERBALL_CATEGORICAL_PROB`: 20 probabilities summing to one.
5. `MAIN_SET_DISTRIBUTION`: lawful probabilities/scores over seven-number combinations, exact or computable via a declared score/probability API without enumerating all sets.
6. `MAIN_ORDER_DISTRIBUTION`: legal ordered-sequence likelihood/scores.
7. `DIAGNOSTIC_SIGNAL`: anomaly/regime/coupling or other intermediate feature that may require an explicitly defined **adapter** to produce a prediction; a valid output, not grounds to delete a method.
8. `ENSEMBLE_RESULT`: combination of already-frozen, time-legitimate source-method outputs under a versioned combination policy.

**R2-C10:** Do not fabricate a numerical probability, complete ranking or inverse result merely to satisfy an interface. A diagnostic-only method may return `NOT_PREDICTIVE_YET` until a mapping from diagnostics to forecast is specified and validated; it remains registered.

### 5.2 Provisional `ForecastResult` conceptual fields

```text
ForecastResult:
    method_id, method_name, method_revision, variant_id
    run_namespace, observation_view, game_rule_id
    target_draw_number, target_date_if_known, training_last_draw_number
    history_window, permitted_training_view_digest
    source_snapshot_hashes, source_information_cutoff_if_applicable  # provenance ONLY
    fitting_algorithm_id, hyperparameters, random_seed_identity
    outputs: typed channels (full frozen rankings / scores / probabilities /
             joint sets / diagnostic; include tie and marginal status)
    top_main_set: exactly 7 unique eligible numbers, when supplied
    top_powerball: exactly 1 eligible number, when supplied
    top_selection_rule_id: TOP_MARGINAL / MAP_SET / SAMPLED / other declared rule
    worst_main_set: 7 lowest frozen marginal ranks, when available
    worst_powerball: lowest frozen Powerball rank, when available
    worst_selection_rule_id: INVERSE / INVERSE_UNAVAILABLE
    worst_unavailable_reason: when applicable
    batch_target_id, prospective_series_ids, pre_draw_freeze_status
    fit_provenance, warm_start_parent, source_method_dependencies
    status, warnings, numeric_validity, effective_sample_size_if_meaningful
    canonical_content_hash  # digest of canonical content (excluding digest field itself and whole-source hash)
    archived_at_if_recorded, remote_commit_evidence  # separate audit metadata
```

**R2-C11 [PROPOSED, revised]:** A ranking-capable method emits both pre-draw selection outputs from **one frozen model**:

- `TOP` (report label **TOP**): the method's **original declared primary** legal selection. For a marginal-ranking method this is the seven highest-ranked main labels and highest-ranked Powerball. A joint-set method may instead have a declared `MAP_SET` or other native joint choice; preserve and label that rule rather than silently replacing it with a top-marginal set.
- `INVERSE` (report label **WORST**): seven lowest-ranked main labels and the lowest-ranked Powerball **from the same complete frozen marginal rankings**, not the mathematically least-likely joint seven-set. In a method with a native joint-set TOP, the inverse is explicitly named `INVERSE_FROM_MARGINALS`. TOP and WORST need not be disjoint for a joint-set TOP method.
- An ordered-sequence method may use a distinct native ordered TOP, but WORST remains based on its frozen **main-label marginals**, when those can be defined. Do not manufacture an implausible inverse order by simply reversing an ordered draw sequence.
- A component without a valid full ranking returns `INVERSE_UNAVAILABLE` and a reason for that component. A diagnostic-only method without a valid forecast remains diagnostic. If a method produces only a main or Powerball forecast, report the other component's availability explicitly; never quietly substitute another model's values.
- Every selection rule is identified by a stable selection-rule ID and version. Each forecast must explain its meaning and whether any channel is an uncalibrated score. `INVERSE` does **not** create a new E-number automatically, but is preserved as its own prospective performance series.

**R2-C11A [PROPOSED, owner requirement]:** A pre-draw report shows **TOP and WORST next to each other in the same E-method row**, for the main numbers and Powerball separately. Freeze both simultaneously. Evaluations after the draw show TOP matches, WORST matches and **separately** the rank-position metric; they never modify the frozen predictions. Rank position is an **R3-only post-draw evaluator calculation**, not a third selection rule. In particular, neither actual-result rank positions nor mid-rank tie scores may alter BEST/TOP or WORST selections. The full frozen rankings support future analysis without changing the original prediction.

**R2-C12 [PROPOSED]:** All numerical outputs must use a defined finite-number policy; NaN/Inf, integer range errors, malformed ordering, duplicate main numbers and mismatched probability normalisation produce a visible validation failure. Numeric failures never silently coerce to an apparently valid forecast.

### 5.3 Consistency and versioning [PROPOSED]

- `method_id` is a permanent stable `E_x` for a scientific hypothesis; `method_revision` changes when its specification or implementation changes.
- `variant_id` records alternative estimators, fits, kernels, conditioning policies, data views or legal selection models while retaining the E-number where the core scientific hypothesis is the same.
- `run_id` identifies one concrete execution and may include the whole-source snapshot hash for audit. **Separately**, the stable **forecast-content identity**, permitted-training-view digest and stochastic seed depend only on actually permitted pre-target inputs and fixed task configuration; they must not contain a growing whole-file hash, creation timestamp, worker ID, result of N, or any future row. The same historical forecast content must be reproducible when the source grows without altering its permitted prefix.
- If a later combination experiment becomes a distinct scientific method, allocate **a new E-number** by the user-approved method registry procedure. Never re-use or re-number an old ID.
- Dependencies on earlier forecasts or ensembles are recorded as a **directed acyclic graph**; no current-target evaluation outcome feeds a prediction-time combination.

### 5.4 Ties and rankings [OPEN decision]

A consistent **prediction-time** default could resolve equal scores by increasing ball number, with tie metadata recorded. Seeded tie-breaking could be a separately declared, deterministic variant. The project has **not** ratified one TOP/WORST tie policy yet; it must be fixed before producing affected real forecasts. TOP and WORST are selected using that **frozen prediction policy** alone. **Only** the later rank-position evaluation uses **mid-ranks** for tied scores (mean of the occupied rank positions); the actual result and mid-ranks cannot alter the original ranking order, TOP, WORST or tie rule.

---

### 5.5 Frozen E_1 numerical and forecast regression identities

**DECIDED — immutable acceptance goldens:**
- Synthetic permitted-view training SHA-256: `df21871f8067e5405b4fdb1eec50c65dddbaa35958872bad3230d3c10a791fd4`.
- Synthetic MAIN label-3 tie SHA-256: `7ce5ab1bae014adf61f1f02dd152d4b500cb405b65cb3886cdcee8dd9e2c9932`.
- Synthetic canonical forecast SHA-256: `7b43d659d611791deb14d106a72984f153d9f79cc63b3d25000365de4c811d1e`.
- Real E_1 forecast-only target `POWERBALL/1577`, trained only on 1144–1576: permitted-view SHA-256 `d47fbbd6e60e6abc429fb74f47d8bbeafc6560152c2ecddb3b75d79932df4339`; legacy canonical result SHA-256 `7f1130872b3afaa222ff4e8c2396cd2c2872583544dfa6b31cc5a07cd067164e`.
- Frozen E_1 forecast outputs for this regression are **TOP** main `[9,17,7,11,18,30,12]`, Powerball `2`; **WORST** main `[31,13,8,29,26,33,35]`, Powerball `12`. **These are forecast outputs, not published outcomes.** No row-1577 outcome may be read or scored during this test.

Any new wrapper schema must report a distinct version and distinct hash without silently rewriting legacy frozen evidence. Offline synthetic E_1 mathematical/tie checks and the forecast-only real 1577 check are gates after dependency upgrades and before scientific acceptance. The real v0.11 offline test may retrieve legacy pre-boundary rows from Git `06f6e0f` **only after filtering raw first-field draw number to `<1577` before decoding other fields**, or use the accepted version-1 master; it must never read/score outcome 1577.

### 5.6 Method-generic contract fields before E_2 (stage 1) (DECIDED; Method Ranking Measures Proposal v0.5 section 13)

Owner-ratified on 26 October 2026. These fields belong to the E_2-readiness package, the method-generic contract that must replace the E_1-specific conventions before E_2 (Architecture section 20A), after Package 2 v0.11 is accepted. They are not part of v0.11, and P3 v0.2 is not edited. The owner ratifies the field schema first (R3 section 17.13, stage 1). Declaring a field or capability authorises nothing.

**Stage-1 contract fields** (adopted from ChatGPT's section E):
1. `game_id`; method and variant IDs and version; the immutable schema ID; era and profile version; registry status (`SUPPORTED` / `FORMULA_OPEN` / `UNSUPPORTED_FOR_GAME`) with its reason; the method **name, one-liner and short explanation**, with per-version provenance.
2. TOP and WORST readout status recorded **independently**; `INVERSE_UNAVAILABLE` is never manufactured. The frozen ticket; the main ranking and per-label scores; the Powerball ranking and scores where applicable; the `TIE_SHA256_V1` identity and digest.
3. **Per-channel probability capability:**
   - `main_probability_kind`: `NONE`, `NORMALIZED_LABEL_PROBABILITY` (length N, values in [0,1], sum 1) or `MARGINAL_INCLUSION_PROBABILITY` (length N, values in [0,1], sum 7).
   - `powerball_probability_kind`: `NONE` or `PB_CATEGORICAL` (length 20, sum 1); `ABSENT` for Oz Lotto.
   - Normalisation tolerance is stated per kind (for example an absolute error of at most 1e-12 on the sum).
   - Never inferred from arbitrary scores or from a theoretical claim. A method may declare both channels.
   - Recorded per channel: the vector order, float64 representation, smoothing and calibration notes, provenance and a digest.
4. `IS_capability`: `IS_STATIC`, `IS_STATEFUL` or `IS_NOT_APPLICABLE`, with a versioned future fit/apply interface where genuinely supported. Declaring a capability authorises nothing.
5. Separate `product_kind`, `run_mode`, `score_status`, evidence tier and forecast-freeze receipt. WF and IS are not readout variants. IS cannot enter the R3 ledger. The allowlist stays strict and empty until authorised.
6. Per track: the canonical pre-target forecast identity; the target `(game_id, draw_number)`; master and ledger provenance; a view digest excluding post-target content; the environment identity; the window and cohort; the status captured before the outcome is opened. The master SHA is provenance only.
7. A scorer-only post-outcome record: drawn main set, Powerball where applicable, Oz supplementary matches and division. Never fed to a predictor. Quarantine opening is separately gated.

**Acceptance before E_2:**
- shape and numeric contracts;
- profile separation between games;
- prefix-only view and digest independence (T-05);
- R3 tie and WORST consistency;
- no Powerball or supplementaries in Oz predictor views;
- the mode firewall;
- not-applicable behaviour per capability;
- extension points without early implementation of ranking or IS;
- a schema versioning and migration rule.

## 6. Method interface, registry and independent testability

### 6.1 Proposed method lifecycle

```text
register -> validate input capabilities -> prepare/freeze training view
  -> fit_or_update(training <= N-1) -> freeze model/rank channels
  -> generate native TOP + marginal-based WORST (if available) for target N
  -> validate both outputs -> canonicalize/archive pre-draw predictions
  -> (separate evaluator, later R3, may reveal N and compute scores/rank positions)
```

The experiment itself **never** calls the evaluator for the result of its own target. Its model-fit and prediction path cannot access scoring records. The program may offer a high-level CLI wrapper later; this R2 document specifies interfaces, not a finished `.py` file.

### 6.2 Registry fields [PROPOSED]

Each E-method has `id`, exact `name`, `research_source=R1_v0_4`, `scientific_hypothesis`, `input_capability`, `output_capability`, `minimum_history_requirement`, `default_variant` (if ratified), `supported_variants`, `math_spec_status`, `implementation_status`, `dependency_status`, `regression_fixtures`, `numeric_validation`, `resource_profile`, and `reason_for_any_blocker`. From the stage-1 contract (section 5.6, field 1), each entry also holds the method's name, one-line summary and short explanation, with per-version provenance; every report prints them (MRD-09; R3 section 17.10.3).

Per-game method **support** status (ERR-R2-05, DECIDED): `SUPPORTED`, `FORMULA_OPEN`, or `UNSUPPORTED_FOR_GAME`, with a recorded structural reason, versioned method identity and applicable barrel/view capabilities. This is distinct from the following proposed *implementation-lifecycle* status vocabulary. The absence of a second Oz Lotto barrel must be represented explicitly, not fabricated.

Suggested implementation status enumeration: `RESEARCH_CANDIDATE`, `FORMULA_OPEN`, `SPECIFIED`, `IMPLEMENTING`, `IMPLEMENTED`, `TESTED`, `RUNTIME_FAILURE`, `INSUFFICIENT_DATA`, `SUSPENDED_BY_USER` (never silently dropped). A method can retain its permanent identity regardless of status. "Suspended" is an explicit operational choice, **not deletion**.

### 6.3 Reusable services [PROPOSED]

- Typed/cutoff-limited CSV loader and external-feature provider.
- Lag/recurrence and occurrence indicator sequence generator (not globally precomputed using future rows).
- Legal unordered-set/ordered-sequence probability utilities.
- Stable seeded random-stream service derived from the **permitted training view**, plus immutable full-rank storage, deterministic TOP/WORST selection adapters, and a **separate post-result mid-rank evaluation** utility (not callable from predictor path).
- Optimisation and validation wrappers, with predictable timeouts/failure reporting.
- Immutable forecast archiving, logging, provenance hashing and manifest generation.
- Resource and timing instrumentation independent of prediction performance.
- Distinct synthetic-generating research utility with namespace-specific provenance.

### 6.4 Handling outputs other than full predictions [PROPOSED]

An information-theory diagnostic or chaos feature that has no direct seven-number ranking **remains a valid registered experimental method**. Do not invent an inverse or ranking for it. An explicit, versioned adapter may translate it to a legal forecast (for example, features to a separate fitted predictive head). The adapter must obey N−1 fitting and use no target outcomes; until specified, the status is `DIAGNOSTIC_ONLY`, not a forced random projection.

---

**R2-C13 DECIDED multi-game extension (ERR-R2-05):** For **each** retained E-method identity and **each** game, record exactly `SUPPORTED`, `FORMULA_OPEN` or `UNSUPPORTED_FOR_GAME`, with any unsupported structural capability and reason. That per-game support status is owner-decided. The original R2-C13 research-registry paragraph, retained verbatim in §7 as part of the protected method inventory, uses `[PROPOSED]` for its remaining implementation/lifecycle details; its status is **not** a withdrawal of this separately ratified per-game support requirement.

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
| `IN_SAMPLE_DIAGNOSTIC` | One full fit on the eligible development draws E(G)..L of the declared window (section 8.4) | Diagnostic: how well a fitted method describes draws it has already seen | **Yes, by design:** the scored draws are part of the fit, so it is never a forecast | IS namespace only; labelled `IN_SAMPLE_DIAGNOSTIC`; never in the R3 ledger or allowlist |

**R2-C16 [PROPOSED]:** Synthetic calibrations may inform subsequent *disclosed* choices of numerical algorithm, model parameterisation, architecture and investigation priorities. They cannot inject synthetic data into the *actual fitted forecast state* or count artificial successes as real-world evidence. Synthetic diagnostics do not function as methodological vetoes or give a method preferential claims about reality.

**R2-C17 [PROPOSED]:** Code paths for real prediction do not import or read `results/synthetic/...`, synthetic fit checkpoints, planted truth values or synthetic evaluation scores. Shared general numerical utilities are permitted; shared trained states are not. A generated synthetic fixture must have a manifest that plainly says `SYNTHETIC` and cannot masquerade as the real source CSV.

### 8.2 Predict then evaluate, not the reverse

For a historical draw N, the runner first freezes and archives the method's **TOP and WORST predictions together** (where available), plus its complete rankings; only an independent evaluator authorised under R3 may load the actual draw N and calculate scores, including the agreed **additional rank-position measure**. The predictor interface must not accept a target-outcome argument. An evaluator's result is a separately versioned record that does not rewrite original prediction bytes. Early development can test mechanics on invented fixtures with known answers without counting this as actual research success.

### 8.2A Prospective evidence and unbiased interpretation [AGREED intention; R3 interpretation DEFERRED]

The project does **not** assume that statistically unusual outcomes are defective simply because conventional models consider them unlikely. Historical walk-forward scores may identify intriguing patterns, but the strongest practical test of prospective usefulness is the repeated **FINAL** sequence: store each `L+1` forecast before the draw; after publication, separately append its actual outcome and evaluation; refresh the source and forecast the next `L+1`. Preserve every attempted target, including abstentions, timeouts, failed fits, and poor predictions, so selection does not hide failures.

**Weekly batch and prospective series (R2-C17A, PROPOSED):** One complete, versioned batch must be produced and pushed **before** each genuine target draw. Freeze the registered method/variant roster and each method's declared TOP and WORST selection-rule outputs. Record failures, abstentions, inverse-unavailable components and not-yet-runnable registered entries explicitly; do not silently omit them. Preserve distinct prospective tracks per `(method, revision, variant, observation view, barrel, selection rule)` even if they coincide or are highly correlated. No post-result rerun can be inserted into the original batch; keep later reanalyses separate and clearly marked as retrospective. The batch's commit ID and evidence of pre-draw push/publication are archived; commit timestamps alone are not accepted as incontrovertible evidence of timely publication.

**Context for later result reports (R2-C17B, PROPOSED):** Any report highlighting a TOP or WORST hit includes its predeclared reference-model chance rate **alongside** the observed result where mathematically applicable. Under a fair, independent draw, a fixed seven-number main-set selection has mean 1.4 matches and a fixed one-number Powerball prediction has 5% hit probability. Batch-level chance estimates require explicit handling of dependent methods and selection multiplicity; naïve independent-method approximations are not universal baselines. These comparisons must **never** automatically dismiss or endorse a real result. R3 fixes the presentation, uncertainty, multiple-testing interpretation and preregistered score definitions before the first FINAL forecast.

For reports, distinguish at least: **observed result**, **possible explanation under investigation**, **independently confirmed data/code fault**, and **provisional interpretation**. “Coincidental fit,” “synthetic artefact,” and “implementation error” are **hypotheses about a result until evidence establishes them**; they must not be imposed as unexplained labels. Clear-cut software defects or source contradictions remain actionable whenever verified, rather than deferred until a series of future draws has accumulated. Repeated prospective successes or failures update evidential confidence, but they do not, without sufficient analysis, conclusively prove a departure from randomness or disprove unconventional mechanisms. R3 decides the statistical framework, adjustment for repeated model changes, and reporting language.

A real-data method must not import fitted synthetic states; independent synthetic diagnostics may help investigate suspicious effects, but cannot overwrite or invalidate an observed prospective result merely by disagreeing with it.


### 8.3 Combination methods [PROPOSED]

E_55/E_56 and future ensembles consume **frozen origin-matched source-method forecasts**, never retrospective score tables or future outcomes. Their dependencies are versioned, their constituent selection policies are frozen before the relevant target, and the dependency graph is acyclic. A combination can include a method that is poor, correlated, contrarian, diagnostic, slow or speculative; adaptors and weights must be explicit. Exact evaluation and selection rules belong to R3.

### 8.4 In-sample diagnostic mode (IS) (DECIDED; Method Ranking Measures Proposal v0.5 section 7)

Owner-ratified on 26 October 2026; proposal 7.1-7.4 are carried here as 8.4.1-8.4.4. The side-by-side display (proposal 7.5) is a reporting rule in R3 section 17.7.5. H(N), E(G) and the window [S, L] are defined in R3 sections 17.3.3 and 17.3.6.

**8.4.1 Purpose.** To see how each method's fully trained state fares over the window. The owner knowingly accepts the bias: the window's draws are part of the training data. IS answers "how well does the method describe the draws it has seen", never "how well does it predict".

**8.4.2 Procedure** (per game, method, variant; window [S, L]):

1. **Full fit** on F = H(L + 1), the eligible draws E(G)..L. It reads no draw after L.
   - Record the frozen parameter digest, the master version and SHA, and the environment.
   - In Phase 1 the fit never touches quarantined draws.
2. **Apply:** for each target N in [S, L] ascending, produce the entry from the frozen parameters plus, where used, the recent-state inputs from H(N) only.
3. **Score** against draw N (R3 section 17.4).

**8.4.3 Capability** (declared in the method-generic contract, section 5.6):
- `IS_STATIC`: one fixed entry scored against every target (for example E_1's raw counts).
- `IS_STATEFUL`: fixed parameters, with state from before N.
- `IS_NOT_APPLICABLE`: the method appears in WF tables only.

Declaring a capability authorises nothing, and does not require all methods to implement IS.

**8.4.4 Firewall and labelling:**
- Product label `IN_SAMPLE_DIAGNOSTIC`; evidence tier `IS_DESCRIPTIVE`.
- Every IS page carries: "IN-SAMPLE DIAGNOSTIC - the scored draws were part of the training data; this is NOT evidence of prediction."
- **All IS numbers are calculated and shown (MRD-21)**, including sigma, p-values and Bayes factors. Every significance figure is labelled `IS_NOT_CALIBRATED`, because fitting on these outcomes means fair-draw tails no longer apply.
  - The label may be applied once per IS table rather than repeated on every figure; the owner's choice of presentation.
  - An unusually high IS figure is kept as an observation worth checking on genuinely new data. It is never a calibrated finding.
- N1 is not used to calibrate IS. A whole-pipeline null (refitting on simulated histories) is a possible later design (MRO-10).
- IS records never enter the R3 scientific score ledger or the result allowlist, are never counted as WF, holdout or prospective evidence, and are never used by any method or meta-method.
- **IS and WF tracks never compete in one ranking.** They are shown side by side (R3 section 17.7.5).
- After holdout draws are opened and scored, IS windows may include them, and the report states that they are in-sample for IS.

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
**Scaling beyond six workers is OPEN**, requiring owner-approved design and testing.

**R2-C18:** Worker count, operating-system scheduling and completion order must never determine seed streams, choose model weights, change historical cutoffs or alter method identity.

### 9.2 Stable random-stream assignment [PROPOSED]

**Mandatory correction from Claude's R2 v0.2 review:** **Never** put the hash of the *whole source CSV/snapshot* into the seed or forecast-content identity. Appending draw `N` or later would change the earlier target `N` prediction for stochastic methods even though the legitimately visible prefix has not changed; this defeats the perturbation leakage test.

Before any fit, derive an immutable **permitted training view** containing exactly the observations and external inputs actually admissible for target `N`, through `N-1` for historical runs (through `L` for FINAL `L+1`), in a documented canonical encoding. Compute its `training_view_sha256`; a method-specific rolling window is reflected in the view. Build the stochastic task identity from that digest and stable, declared pre-target configuration, e.g.:

```text
(root_seed, namespace, method_id, method_revision, variant_id,
 observation_view, selection_model_version, target_draw_number,
 training_view_sha256, admitted_external_input_digest,
 fitting_config_digest, start_or_restart_index)
```

For external inputs, the digest includes **only** inputs truly available before the target and selected by the declared method. Include permissible warm-start lineage in stable input identity if and only if that lineage itself obeyed its preceding cutoffs. `ROOT_SEED`, method configuration and any relevant identities must not secretly incorporate the whole-file hash or future-source change. Use stable binary serialization/digests and NumPy `SeedSequence` (or an equivalently specified derivation), never Python's salted `hash()`, process IDs, worker positions or job completion order.

**R2-C19 [MANDATORY FIX]:** The **forecast's content identity and randomness stream** must be invariant to changes or additions to draws `N` and later. Retain the full-source SHA-256 **only as separate audit/provenance metadata**; a new snapshot may produce a new *run/manifest identity* while the unchanged earlier prediction's **content identity and canonical bytes** remain identical. A predictor must not read whole-source information in precomputed features, caches, seeds, fitter selection or warm starts. Check this by controlled N-and-later mutation and append tests, not by simple inspection of the adapter's parameter list.

### 9.3 What bit-identical means [PROPOSED]

Compare **canonical prediction payloads**, including the method's full rankings, original TOP and inverse WORST output or explicit unavailable statuses, and excluding creation timestamps, **whole-source snapshot provenance**, remote archive/batch IDs, elapsed time, CPU time, worker IDs and temporary paths. Canonicalise field ordering and representations (including floats if used) under a documented serialization rule. Record SHA-256 of the canonical payload and require equality of both bytes and digest for 1-worker and 6-worker runs on a matched environment. Equal digests are useful but checking actual bytes where feasible is preferred. Do not compare logs that necessarily differ by scheduling timestamps.

A mismatch is `REPRODUCIBILITY_FAIL` until fixed or until the user approves a justified method-specific exception with clear scope and alternative reproducibility criterion. Merely declaring a general numeric tolerance is **not** an automatic waiver. Parallel floating-point summations or nondeterministic native kernels, if encountered, must be diagnosed rather than assumed impossible.

### 9.4 Resource safety and failure semantics [PROPOSED]

- Record wall-clock startup/import, fit, forecast, output validation and total pool times separately; also per-worker process CPU time.
- Capture worker process peak resident/working-set memory and, when available, aggregate peak worker memory. `tracemalloc` alone is insufficient for NumPy/native allocations; `psutil` is a candidate dependency subject to venv installation approval.
- Configure per-method timeouts; an exceeded timeout is `TIMEOUT` with partial elapsed time, never a fabricated completion duration.
- Worker exception, crash, OOM, non-finite output, invalid set, missing input, insufficient history and unsupported view receive distinct statuses.
- Do not interpret CPU seconds greater than elapsed seconds as conclusive evidence of incorrect thread pinning; inspect per-process scopes and actual thread-pool configuration.
- Keep the host responsive. A 32-GB total system cannot safely grant six unconstrained workers 32 GB each. Resource thresholds and worker reductions should be measured and configurable.
- Record the Windows power plan and the CPU model when comparing time series of benchmarks.

### 9.5 Later acceleration is optional

Parallelising independent synthetic histories, independent restarts, and origin blocks can be considered later. Warm-started origin sequences are **not** freely independent: block splitting needs explicitly declared cold starts or state handoffs. Numba, JAX, PyTorch or compiled kernels are optional only after representative benchmarks and current Python 3.14 Windows-wheel checking. No promised 10× or 50× acceleration is assumed. Slow E-methods remain scientific candidates.

---

## 10. Computational benchmark specification — independent of predictive evaluation

**Purpose:** Measure how the system executes and scales on the **user's actual machine**. Benchmarks must not judge whether a method correctly predicted the historical result.

### 10.1 Single benchmark facility, two presets

- `B1`: `X=1`, Powerball target **N=1576**, training 1144–1575 (432 draws), or W=100 1476–1575.
- `B10`: `X=10`, targets **N=1567..1576**, with full-history counts 423–432 or corresponding W=100 lawful prefixes.
- `W=ALL_PERMITTED` or `W=100` preceding observations; other W values need explicit names and verification.
- These are purely execution-time/diagnostic targets strictly before quarantined observations; report no forecast numbers, scores, rankings, winnings or predictive merit.

### 10.2 Required timing comparison

1. Execute matching work with one active worker.
2. Execute exactly the same task identities with **six** active workers, subject to strict RAM and safety gates.
3. Compare canonical predictions byte-for-byte, not wall times or scheduling-order artifacts.
4. Compare full-permitted and W=100 histories only at the same permitted target origins.
5. Use median of three fresh repeats when practicable; declare any lower repeat count without invented medians.
6. Synthetic throughput probes must be explicitly `BENCHMARK_SYNTHETIC`, with no consumption by scientific result evaluators.
7. More than six workers, or method-created subprocesses, requires a distinct owner-approved extension. It is not inferred from an older 12/24-worker suggestion.

**R2-C20:** A benchmark job writes `SUCCESS`, `TIMEOUT`, `ERROR`, `INSUFFICIENT_HISTORY`, `BLOCKED_DEPENDENCY`, `NUMERIC_INVALID` or an explicitly declared status, plus actually observed wall/CPU/resource measurements. Partial timing is labelled as such; failures never turn into scientific outcomes.

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
| T-05 | **MANDATORY adversarial leakage test:** run a stochastic and deterministic historical target N, then modify N and every later row (and append later rows), with training rows `<N` unmodified | Identical complete canonical prediction bytes, rankings, TOP, WORST, content IDs and seeds; only external provenance metadata may change. Fail if a whole-file seed, cache or warm start introduces change |
| T-06 | Post-draw external datum with earlier event date | Not admitted if publication time is after cutoff |
| T-07 | Fake synthetic source flagged as REAL | Namespace/provenance check rejects it |
| T-08 | Synthetic fit checkpoint offered to real predictor | Rejected; no latent state can cross namespace boundary |
| T-09 | Probability with negative entries/invalid sum | Numeric validation failure, not an invented winner |
| T-10 | Main set contains repeat/incorrect count | Forecast validation failure |
| T-11 | Order view absent for ordered-only method | `UNSUPPORTED_INPUT_VIEW`, not method deletion |
| T-12 | Warm start derived from a future target | Reject dependency lineage |
| T-13 | One vs six workers, same job identities | Bit-identical canonical forecast bytes by default |
| T-14 | Worker timeout/crash/out-of-memory | Explicit status with no fabricated duration |
| T-15 | Benchmark report generation | Contains only resource/timing/status/digest fields; no scores or predicted numbers |
| T-16 | Repeated source with altered bytes | Full source digest/run provenance reflects changed snapshot. If alteration is only at/after target N, unchanged permitted training implies **unchanged forecast content/seed**; never silently overwrite the archived original |
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
| T-29 | Repeated real FINAL forecasts and later known results | All pre-draw TOP/WORST forecasts archived intact, outcomes and later rank-position scores added separately, unsuccessful/failed targets retained |
| T-30 | Ranking-capable method freezes full main/Powerball rankings | All 35 and all 20 labels respectively in complete deterministic order, with tie metadata and no missing/duplicate labels |
| T-31 | TOP/WORST prediction generation for an ordinary marginal-ranking method | TOP uses highest seven/highest one; WORST is obtained by **exactly reversing the same frozen complete ranking** and selecting its first seven/first one, under the separately declared prediction-time tie policy; no refit or rerank is permitted |
| T-32 | Joint-set TOP model with available marginals | Preserve native TOP set; WORST uses seven lowest marginal ranks, **not** a fabricated minimum-probability joint set; native TOP/WORST overlap is permitted |
| T-33 | Diagnostic/set-only method with no genuine full ranking | Explicit per-barrel `INVERSE_UNAVAILABLE` with reason; no fabricated marginal, result or missing-method suppression |
| T-34 | After actual draw, calculate rank-position mean using tied frozen scores | Mid-rank applied only in evaluator; TOP/WORST archived canonical content stays byte-identical before and after revealing actual target |
| T-35 | One real target run with all registered runnable variants | Exactly one frozen complete pre-draw batch; all TOP/WORST or unavailable/failure records present; pushed remotely before draw and auditable as such |
| T-36 | Attempt post-result insert/replace in the prospective batch | Immutable batch rejects mutation; later changes recorded as labelled retrospective reruns with distinct lineage |
| T-37 | Serial-versus-6-worker TOP/WORST stochastic run | Identical complete canonical bytes, including full frozen rankings and inverse status, for matched environment and seed identity |
| T-38 | Report a successful prospective TOP/WORST hit | Preserve separate track for each method/variant/selection rule; report reference chance rate as comparison, never automatic coincidence verdict; keep rank-position metric post-draw and separate |
| T-39 | Weekly live-cycle start before scoring definitions are ratified | Block prospective production mode until R3 predeclares TOP, WORST and rank-position evaluation and reporting rules; do not replace a scheduled actual draw with retrospective predictions |


### 11.2 Method-specific numerical fixtures [PROPOSED]

For each implemented method, provide at least one small deterministic fixture with an independently checkable mathematical result, a no-look-ahead fixture, a seeded-run fixture if stochastic, a numeric-failure fixture, and a result-type validation fixture. Diagnostic-only methods validate their advertised diagnostic output without inventing a seven-number selection. More elaborate synthetic tests do **not** automatically serve as eligibility gates; they are distinct research diagnostics.

For E_57 test positivity/PSD, finite `Z_7`, valid fixed-size distribution and `L=I` uniformity. For E_31/61 test sequential likelihood normalisation on tractable toy cases, then validate the equivalence of ordered sum and unordered legal-set likelihood at testable small dimensions. For E_61/62 test the difference between zero-noise order preservation and outcome-conditioned reinjection; check the reference field and state dynamics with an independently verifiable small numerical example.

### 11.3 Reproducibility and process robustness [PROPOSED]

- Run repeat-test on one and six workers under identical environment/seed/configuration and verify **canonical payload bytes**, including complete rankings and TOP/WORST outputs. Separately run the mandatory N-and-later source mutation/append leakage tests, comparing forecast content but not legitimately changing snapshot audit metadata.
- Verify worker exceptions propagate as status records and that partial results cannot be counted as completed method forecasts.
- Verify per-method timeout, interruption and restart do not import stale hidden states from a different target or dataset revision.
- Verify the source/variant/method revision is frozen in forecast provenance.
- Later R3 supplies statistical evaluation-specific tests and reporting requirements; R2 must not silently add a significance threshold now.

---

## 12. Repository organization and development workflow

### 12.1 Current repository: do not silently relocate or replace files

The project repository `hydra3333/analysing_perceived_randomness_in_reality` contains the current `doc/`, `src/`, `source_data/`, `tests/`, `results/`, `Run_Results_Updater.bat`, `install_upgrade_dependencies_into_venv.bat`, its project `.venv`, and Git evidence. Accepted owner-run tools are `src/two_site_results_check_v0_7.py` and `src/results_master_v0_1.py`; current per-game master CSVs and associated ledgers/INIT records reside under `source_data/`. Historical October 21 two-file inputs and the original scraper have been removed from the active working tree and remain in Git history. The source API/saved-page tool proposals from ChatGPT v0.10-r1 are retired, not a competing acquisition authority. Do not invent or relocate a current path merely because this design shows an illustrative structure.

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

The retired original scraper is historical. The accepted owner-run master updater and two-site checker remain untouched; any source policy change requires a separate owner-reviewed change, outside this documentation consolidation.

**Clarification of “shared data”:** `src/predictive_randomness/` refers to reusable **Python modules** and, as needed, a common immutable **in-memory view of source observations** permitted for the target draw. It does **not** designate a pool of fitted states or intermediate prediction results that another experiment or a repeated run may transparently consume. Experiments may share common stateless numerical routines; model A's fitted intermediate state is **not** implicitly input data for model B. Deliberate ensemble inputs use only explicitly frozen and versioned source-method forecasts under their defined method-combination contract.

**Proposed `transitory_data/` discipline:** Create this root directory **only if** an algorithm actually requires temporary disk-backed data. Default to in-memory calculations. A temporary artifact is scoped to a particular namespace, run ID and method or worker; concurrent workers use noncolliding paths. The directory must be added to `.gitignore` as `/transitory_data/`; contents are **disposable** and must never automatically become `source_data/`, `results/` or a valid input to any subsequent or parallel run. Cleanup and crash residue handling must be controlled. If a later expensive method needs persistent checkpoints or restart after interruption, that capability must be **separately specified, approved and provenance-validated**: a resumable state is not automatically authorised merely because a temporary file exists. Real and synthetic scratch spaces may never exchange fitted states.


### 12.3 Python environment, dependencies, and installation policy [AGREED/PROPOSED]

- Preserve the user's working standard Python 3.14.8 project `.venv`. Do not install modelling libraries globally and do not change VS Code configuration without a demonstrated reason.
- To run in an independent CMD: `call .venv\Scripts\activate.bat` (or the user's working `activate_venv.bat`). VS Code's working custom CMD terminal profile activates it automatically.
- Historical nonauthoritative dependency records may contain retired scraper packages (not a complete predictor numerical stack). Any additional PyPI package must be **announced before installation**, its Python 3.14/Windows support checked at the time, and its version recorded in the authoritative installer revision and resolved package-version evidence specification.
- Probable first numerical layer: `numpy`, `scipy`; optional `psutil`, `threadpoolctl`; later model-specific libraries only as needed. A dependency in R1 is a research suggestion, not a current installation requirement.
- Keep `.venv/` excluded from Git. Include source, documentation, appropriately licensed observational data, tests and manifest/requirements files as the user approves.

### 12.4 Future command-line experience — draft, not frozen CLI

Potential commands might have forms such as:

```text
python -m predictive_randomness validate-data --snapshot <...>
python -m predictive_randomness registry --list
python -m predictive_randomness benchmark --preset B1 --window 100 --workers 1
python -m predictive_randomness benchmark --preset B10 --window all --workers 6
python -m predictive_randomness forecast --mode development --methods E_1,E_2
python -m predictive_randomness forecast --mode final-next-draw --all-runnable  # full frozen batch, infer L -> L+1
```

These illustrate *purpose*, not installed scripts or approved flags. Versioned command semantics are for a later implementation ticket.

---

**Dependency evidence (ERR-R2-03, DECIDED):** Record the resolved Python/PyPI versions and the installer version/digest alongside each consequential benchmark and every future FINAL batch. Default automatic dependency upgrading is approved, but after an upgrade the complete applicable offline suites, strict N−1 and numeric boundary checks, Windows W-suite (including W-23) and E_1 regression goldens must PASS before further work. Never upgrade between freeze and score or inside a Mode H study; environment identities are pinned by the study manifest (R3-T50).

## 13. R2/R3 interface and explicit deferred decisions

### 13.1 What R2 controls if ratified

R2 should fix the source schema, registry and immutable method identities, fit/forecast separation, forecast-result types, data-cutoff enforcement, common ordered/unordered view semantics, namespace firewall, canonical reproducibility, initial benchmark instrumentation and method-specification worksheets. It should record what remains mathematically unspecified, not force every candidate into an arbitrary algorithm.

### 13.2 What R3 must decide later

**R2 explicitly does not ratify**:

- Exact computation, uncertainty, significance and aggregation of the **three owner-agreed reporting components**: TOP-selection main matches/Powerball hit, WORST-selection main matches/Powerball hit, and separate full-ranking mean actual-number rank (main) / actual-number rank (Powerball). These must all be reported **in addition to** one another where output capability permits; no replacement of TOP/WORST by rank position.
- Definition of any *additional* scores (likelihood, calibration, proper scoring rules, etc.), methods of comparison and any winner threshold. The agreed three reporting components are required; their precise statistical reporting is deferred, **not optional to omit before live launch**.
- Mid-rank handling of tied scores **only for the post-draw rank-position metric**: the seven actually drawn main numbers' mid-ranks are averaged; the actual Powerball number receives its mid-rank. Under the fair reference, means are 18.0 and 10.5 respectively. The evaluator must not modify the frozen TOP/WORST forecast.
- Multiplicity correction, uncertainty intervals and standards for a surprising result.
- Method and ensemble selection/reweighting policy (including apparently poor methods), selection freeze, and holdout disclosure timing beyond established rules.
- Forecast comparison windows, repeated prospective-forecast evidence, per-method/per-selection-rule track reporting, reference chance rates and minimum statistically relevant training/evaluation lengths, including how many real future draws can meaningfully support a conclusion. **All three required score definitions must be frozen before the first genuine FINAL forecast**, not selected after its results are seen.
- Any conclusion about perceived reality, independence, quantum causes, equipment physics, or nonlocal association based on research mathematics alone; and rules for avoiding premature “coincidence,” “synthetic artefact” or “implementation error” classifications without excluding demonstrable faults.

R3 section 17 (method ranking measures, owner-ratified 26 October 2026) settles part of this list for ranking reports only: the league-table measures, their significance labels and multiplicity rules. Everything else above remains for R3 as stated.

### 13.3 Mathematical specification questions to ratify in later R2 iterations

- Exactly which mathematical **variant** of each E-method will be first implemented, with complete equations and parameter bounds.
- Which E-methods are diagnostic-only pending a forecast adapter, and which initially generate direct predictions.
- **Prediction-time** TOP/WORST ranking tie policy (distinct from post-draw rank-position mid-ranks); legality and normalization tolerance rules; rounding/serialization of floating-point values.
- How a whole-set method chooses its **native TOP** seven-number set, how its **WORST** derives from truthful marginals if present, what `INVERSE_UNAVAILABLE` means, and how a Powerball companion is selected or declared unavailable where not internally modelled.
- Which data view is the default for eligible sequential models, while retaining both permitted views.
- Inference algorithm, seed/restart count, convergence and resource budgets for E_57–E_62.
- Exact worker timeout, memory management and checkpoint resume rules.
- Source-data correction handling across repository versions and real forecast immutability mechanism.
- Exact user interaction for authorising final holdout and real next-draw prediction.

### 13.4 Approval discipline

A proposal here marked `[PROPOSED]` is **not ratified merely because this document was delivered**. The user may ratify (a) the common R2 framework first and (b) individual mathematical method worksheets in stages. This prevents a large document from silently resolving dozens of open statistical or model-fitting questions. Claude or another reviewer may provide voluntary critique, but no further external review is a standing prerequisite; the user remains the decision authority.

---

### 13.5 ERR-R2-05 decisions intentionally left OPEN (no implied authorisation)

The following remain **OPEN**, despite approval of the multi-game architecture: the exact E_54 external-feed and before-draw availability contract; each method-specific `FORMULA_OPEN` mathematical setting; the first real Oz Lotto method experiment; the start of either game's FINAL track; cross-game scientific features; and historical walk-forward window pre-registration (Powerball targets 1145–1576, Oz Lotto 1475–1693). Nominal operator closing/draw times and time-zone/DST conversions also remain pending source verification where those become scientifically relevant. The master initialisation and hash validation are already accepted and are **not** still awaiting a first scrape.

**No authorisation:** Ratification of these data and method contracts alone permits no Oz Lotto method execution, modification or replacement of an already frozen Powerball result, access or disclosure of quarantined outcomes, destructive process tests, process termination switch changes, Mode H, FINAL forecasting, or bypass/removal of any unresolved-orphan interlock. Existing owner controls and separate approval gates continue to bind.

## 14. Suggested implementation plan after R2 and R3 decisions

**Stage S0 — Freeze documentation handoff:** Ratify, install and commit the current consolidated Proposal/R2/R3/Architecture/P3 revisions after independent review; R1 v0.4 remains unchanged. Confirm repository source/data hashes and data-availability cutoff.

**Stage S1 — Data/registry skeleton:** Implement immutable ledger-pinned prefix-only reader, owner-approved game profiles, 62-entry registry, value-free validators, N−1 numerical isolation and strict result allowlist. No new scientific run authority.

**Stage S2 — Minimal methods and single-target runner:** After approving their first precise formulas, implement selected transparent E-methods (original E_1–E_6 are natural initial candidates, but not the only legitimate selection). Test numeric behaviour and store canonical pre-evaluation forecasts.

**Stage S3 — 1/6-worker equivalence, Windows gates and B1/B10:** Verify safe process ownership, manual/coordinated output equality, deterministic one/six-worker outputs, B1 target 1576 and B10 1567–1576, without reading quarantine.

**Stage S4 — Expand all-method catalogue implementation iteratively:** Implement additional E-methods and variants without any exclusion based on speculative status, poor results or correlation. Resource-heavy E_57–E_62 may need separate implementation tickets and benchmarks. Preserve all unimplemented identities and potential future E_63–E_106 research additions.

**Stage S5 — R3-governed scoring/holdout/FINAL forecast:** **Before the first prospective prediction**, ratify R3 definitions for all three owner-agreed evaluation outputs (TOP, WORST, rank-position), their reference-rate presentation and per-selection-rule prospective tracks. Only after R3 is ratified, run authorised historical evaluations and (when requested) the reserved independent holdout. Each user-authorised genuine forecast must derive `L` from the validated actual-data CSV, fit from every available eligible actual draw through `L` (subject only to an explicitly defined method window), and forecast `L+1`. Record every runnable method and variant in **one complete pre-draw TOP-and-WORST batch**, recording unavailable/failure statuses, **commit and push before the draw**, and preserve evidence of timely publication. Append the later actual-result comparison and rank-position evaluation separately, then repeat using updated history for the following week. No later rerun is represented as having been in the original batch. Draw numbers, not clock timestamps, control the model chronology; archive timestamps are optional evidentiary metadata, not fitted predictors.

**Stop rule:** At each step, a failure should identify the blocked unit and its evidence. Do not mark the whole method scientifically invalid because implementation is not yet available.

---

## 15. R2 review checklist and decision register

The following are proposed decisions requiring user consideration; retaining them as a list ensures no implicit approvals:

| ID | Question / proposed decision | Proposed position | Status |
|---|---|---|---|
| R2-D01 | Treat the currently ratified Proposal v0.4 and R1 v0.4 as controlling; v0.5 is a replacement candidate until ratified | Yes | **Already agreed** |
| R2-D02 | Register all 62 E-method identities from R1, including diagnostic-only and pilot-wave methods | Yes | **Agreed on retention; software mechanism proposed** |
| R2-D03 | Use one pinned master version and a prefix-only logical reader; former joined two-CSV model withdrawn | Yes | **DECIDED** |
| R2-D04 | UNORDERED_SET / OPERATOR_DRAWN_ORDER / PAIRED_DIAGNOSTIC on one approved prefix with no double counting | Yes | **DECIDED** |
| R2-D05 | Support typed ranks, marginals, whole sets, ordered distributions and diagnostic-only methods | Yes | **PROPOSED** |
| R2-D06 | Use a runner-enforced cutoff and distinct execution namespaces | Yes | **PROPOSED** |
| R2-D07 | Initial worker pool configurable 1–6 and one method per process, pinned single-thread numerics | Yes | **DECIDED** |
| R2-D08 | Implement B1/B10 with W=100/all, timing-only and explicit statuses | Yes | **Direction already agreed; mechanics proposed** |
| R2-D09 | Canonical bit-identity 1 vs 6 workers; exceptions require separate owner approval | Yes | **DECIDED** |
| R2-D10 | Keep synthetic learning allowed but prohibit synthetic training-state contamination | Yes | **Already agreed** |
| R2-D11 | Retain variants without forcing a new E-number solely for observation view | Yes | **PROPOSED** |
| R2-D12 | Stage approval of numerical method formulas rather than auto-freeze all 62 now | Yes | **PROPOSED** |
| R2-D13 | Freeze exact tie policy, mathematical first variants and time budgets after review | Defer concrete choices | **OPEN** |
| R2-D14 | Defer scores, uncertainties, ensembles' evaluation and promotion to R3 | Yes | **Already agreed** |
| R2-D15 | Historical-evaluation mode uses actual draw IDs and only N-1 history; evaluator compares later | Yes | **User clarified; proposed software contract** |
| R2-D16 | Future FINAL, only after separate owner ratification: derive L from validated completed game draws; fit permitted pre-target history and freeze L+1, score only later | Yes | **DECIDED protocol; execution NOT AUTHORISED** |
| R2-D17 | External series optional; timestamps not required for core forecast; retrospective-only associations labelled distinctly | Yes | **User clarification; detailed contract PROPOSED** |
| R2-D18 | Shared data means common software and permitted in-memory source views; no implicit intermediate-state reuse | Yes | **User clarification; detailed contract PROPOSED** |
| R2-D19 | Introduce optional Git-ignored `transitory_data/` only for necessary isolated scratch; persistent checkpoint reuse requires a separate approval | Yes | **User requested; detailed contract PROPOSED** |
| R2-D20 | Do not pre-judge surprising fits as coincidence, synthetic artefact or implementation error; maintain prospective forecast/evaluation trail while recording verified faults | Yes | **User explicitly required; R3 standards DEFERRED** |
| R2-D21 | Derive stochastic seed and content ID from **permitted training-view digest**, not whole source snapshot | Yes, mandatory bug fix | **Review-identified fix; proposed contract** |
| R2-D22 | Mandate N-and-later mutation/append leakage test on complete canonical forecasts | Yes | **Review-identified fix; proposed acceptance test** |
| R2-D23 | Each rank-capable E-method supplies frozen native **TOP** plus **WORST/INVERSE** from same ranking, displayed side by side | Yes | **User explicitly agreed; exact contracts proposed** |
| R2-D24 | All complete 35/20 rankings retained where method capability supports them; unavailable inverse never fabricated | Yes | **User-approved direction; details proposed** |
| R2-D25 | Preserve **rank-position** as an additional **post-draw metric**; never influence TOP/WORST predictions | Yes | **User explicitly mandated; R3 details deferred** |
| R2-D26 | One complete immutable/pushed-before-draw FINAL batch with all runnable registered methods/variants and explicit unavailable/failure statuses; no retroactive additions | Yes | **Claude recommendation; proposed audit contract** |
| R2-D27 | Separate TOP/WORST prospective tracks and contextual reference rates, without automatically judging unusual successes | Yes | **Review recommendation; statistical policy to R3** |
| R2-D28 | Define TOP, WORST and rank-position scoring/reporting before first genuine real forecast; retain owner's agreed start timing | Yes | **Owner's previously agreed real-forecast cycle; detailed R3 rule proposed** |


### What acceptance of this document would mean

If the owner ratifies consolidated R2 v0.4 **as a framework**, the common contracts and administrative approach become the implementation design basis, while explicitly open mathematical choices remain open. If the user instead requests **complete frozen mathematics for all 62 before any coding**, an additional R2 method-by-method ratification revision will be necessary. Both paths preserve all experimental ideas and do not weaken the project philosophy.

---

## 16. Source traceability and handback

### 16.1 Authoritative source documents

1. **Project Proposal:** consolidated v0.5 candidate (ratified v0.4 remains authority until owner acceptance), current charter and philosophy.
2. **R1 v0.4:** `Predictive_Randomness_Experimental_Methods_Research_R1_v0_4.md`, especially §4 (all numbered methods), §4.7 (pilot-wave family and precise candidate mathematical constraints), §7 (separated research streams), §8 (R3 deferral), §8A (benchmarking), §9 (possible dependencies), §10 (decision proposals), and §11 (technical bibliography).
3. **Current owner-accepted master data:** POWERBALL and OZLOTTO per-game version-1 masters and ledger SHA identities documented in §2, not the withdrawn October 21 data sources.
4. **Claude's review of R2 v0.2:** `Claude_Review_of_R2_v0_2_v1.md`, 22 October 2026, explicitly reviewing `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_2.md`; it identified the full-file seed leakage defect, proposed a complete weekly batch and chance-context guard, and recorded the owner's requests for inverse predictions and an additional rank-position measure.
5. **Owner's subsequent R2 clarifications:** explicit in this conversation: **TOP and WORST are shown next to each other from each method**, and the rank-position measure is **evaluation only** and must **never affect either prediction**. Previous user ratification of Proposal v0.3 and R1 v0.4 remains binding. Ratification is an external approval event, not retroactively changed historical file text.

This R2 consolidated candidate builds on those sources and deliberately **does not reproduce the full R1 research references or all derivations**; those remain authoritative in R1. When a method-specific mathematical claim is in doubt, consult its complete R1 entry and cited technical source before writing code. Any new inference or proposed design rule in R2 is marked accordingly.

### 16.2 Explicit non-claims

No E-method has been coded, statistically scored, accepted as predictive, or used to infer an altered law of reality in this document. No null-world or planted-effect study has been run by this document. No holdout draw has been used for selecting methods. No PyPI modelling package has been installed on the user's PC by this document. No change has been made to original CSVs, source scripts or existing ratified Markdown files.

### 16.3 Recommended next review action

Review this consolidated R2 v0.4 candidate for scientific intent, the corrected permitted-input seed rule, TOP/WORST reporting and evaluation separation, and software-contract boundaries. Approve or revise R2-D02–D28 individually as needed, then decide whether to (a) ratify the common framework and specify method mathematics iteratively or (b) demand complete first-variant mathematics for every method before starting implementation. There is no requirement to convene Claude unless a new substantive mathematical disagreement warrants it.

**Closing principle:** We do not claim to know in advance what patterns can or cannot exist in perceived reality. We make even unusual hypotheses precise enough to be tested without giving conventional theory veto power. Unexpected results remain worthy of continued, documented investigation—not prematurely classified as a coincidence, artificial-data artefact or bug on theoretical grounds. Verified data/software faults are reported as such; meaningful evidence for (or against) predictive structure is assessed through faithfully archived, repeated real-world forecasts and their subsequent actual results, with the statistical interpretation reserved for R3.


## Appendix S — Superseded R2 provisions (history only)

- The older Powerball holdout 1578–1587, development cap 1577, Oz Lotto first-snapshot highest-ten seal and DEV_TO_DATE 2026-08-07 are withdrawn; §§2–3 and R3 govern the fixed August 2026 quarantine.
- The obsolete two-CSV Powerball acquisition model and `Run_Scraper.bat` are replaced by owner-run master version/ledger updating and caller-selected scientific views; see §2.
- Former 1–12/24-worker trial requirements and command examples are replaced by the owner-approved 1–6-worker default; additional capacity is OPEN.
- `ERR-R2-02` remains provisional; no language here enables process termination, Mode H, holdout exposure, unreviewed scoring or FINAL.
- Approved errata ERR-R2-01 through ERR-R2-06 remain identifiable at §0; their historical wording is retained in the original erratum record in Git.
