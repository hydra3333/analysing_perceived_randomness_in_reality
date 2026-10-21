# Claude review of R2 v0.2 - consolidated, with the project owner's decisions to date

**Reviewed document:** `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_2.md`
**Review version:** v1, 22 October 2026
**Reviewer:** Claude (Anthropic), at the request of the GitHub project owner (hydra3333)
**Scope:** serious issues only; spelling and wording that do not change meaning are ignored.

---

## 0. Summary

R2 v0.2 is sound as a framework. The items below were raised in review and then discussed with the project owner. Their current status is:

| Item | Subject | Status |
|---|---|---|
| 1 | Seed rule breaks the strongest leakage test | **FIX required** before ratification |
| 2 | Chance hits from many weekly forecasts | **GUARD required** in the R2 record design; interpretation stays with R3 |
| 3 | When to start real weekly forecasts | **CLOSED** - the owner's cycle stands; one requirement kept (section 4) |
| 4 | Inverse predictions for every ranking method | **NEW**, proposed by the project owner |
| 5 | Rank-position measure | **NEW**, proposed as an **additional** measure, not a replacement |

**Checked and found correct:**

- E_61 reference mathematics carried over from R1 v0.4: guidance law, beta = 2*alpha, epsilon = 0, node-free condition, kappa = 0 nesting, and the ordered/unordered likelihoods.
- Benchmark and holdout arithmetic: holdout 1578-1587; B1/B10 targets 1568-1577 with 424-433 prior draws; the W=100 window for target 1577 is 1477-1576.
- R2-C03 frozen-snapshot assertion: all 444 draws (1144-1587) fall on Thursdays exactly 7 days apart.

---

## 1. FIX - the seed rule breaks the strongest leakage test

**Problem.** R2 section 9.2 includes `source_snapshot_id` (the hash of the whole CSV file) in the seed identity. When a new draw is appended, the file hash changes. Every stochastic method's historical forecast for an old target N then changes, even though its permitted training data (draws before N) has not changed.

**Consequences:**

- The project proposal's own perturbation test (Proposal v0.3 section 15.2: alter draw N and every later draw; the forecast for N must not change) would fail for every stochastic method, for a reason unrelated to leakage. A test that always fails cannot detect real leakage.
- Historical forecasts would not be reproducible from one data snapshot to the next.

**Required change:**

1. Derive the seed, and the forecast's content identity, from a digest of the **permitted training view** (rows up to N-1, plus any other inputs actually permitted for target N). Do not derive them from the whole file.
2. Keep the whole-file hash as provenance metadata only.
3. Make the perturbation test an explicit mandatory test. T-05 as written only checks that the predictor is handed rows up to N-1, so it would not catch a feature or cache computed from the full file. The perturbation test compares prediction content only, not provenance fields.

Refs: R2 sections 9.2 and 5.2, T-05; Proposal v0.3 sections 11.3 and 15.2

---

## 2. GUARD - many weekly forecasts will produce chance hits regularly

**Reference-model figures** (used as comparison context only, never as a veto):

- One forecast gets 4 or more main numbers about 1 draw in 55, and 5 or more about 1 draw in 830.

| Forecasts per weekly batch | Weeks with some 4+ main hit | Some 5+ main hit | Expected Powerball hits per week |
|---|---|---|---|
| 6 (E_1-E_6, top picks only) | about 1 week in 10 | about 1 week in 138 | 0.3 |
| 62 (all methods, top picks only) | about 68% of weeks | about 1 week in 14 | 3.1 |
| 124 (all methods, top and inverse - section 5) | about 90% of weeks | about 1 week in 7 | 6.2 |

Correlated methods lower these figures somewhat; extra variants raise them.

**Why this matters.** None of this says a hit is meaningless. It is the comparison figure any hit has to be read against, and it is what lets a real effect show. A method that keeps beating its own chance rate stands out; "some method did well this week" never will.

**Required in the R2 record design:**

1. Each weekly FINAL run is **one complete batch**: every runnable registered method and variant, including inverse selections (section 5), committed and pushed before the draw. Nothing can be added for that target afterwards.
2. The record keeps a **separate series per method and per selection rule**, so each prospective track can be judged on its own.
3. Any report of a hit shows its **reference chance rate alongside**, as context. This is neither a dismissal nor an endorsement, and is consistent with I-13: stating a base rate is not calling a result a coincidence.

Refs: R2 I-13, sections 3.5 and 8.2A, T-25, T-29

---

## 3. CLOSED - when to start real weekly forecasts

The reviewer had suggested starting the weekly real-forecast loop early with partly finished methods, so that the prospective record would begin sooner. The project owner prefers the cycle as R2 describes it, and that stands:

1. Finish experimenting and modelling.
2. Train every method on all draws in the dataset (1144..L).
3. Produce a full set of predictions from all methods for draw L+1.
4. After the draw, compare every prediction with the actual result.
5. Append the new draw to the dataset and return to step 2.

**Kept from the original item:** decide the scoring for step 4 (sections 5 and 6) **before the first real forecast**, so that no measure can be chosen after results are seen.

Refs: R2 sections 3.5 and 14 (S5)

---

## 4. NEW - inverse predictions (project owner's proposal)

**Idea.** Every method that ranks numbers also implies the opposite prediction: the numbers it rates **least** likely. One method's inverse could turn out to be a good real-world predictor. A reliably wrong method has found real structure with the sign reversed.

**Cost.** No extra modelling or fitting. The inverse is the same full ranking read from the bottom: the 7 lowest-ranked main numbers and the lowest-ranked Powerball.

**Reference figures.** Under the fair-draw reference, the inverse has exactly the same chance figures as the top picks (1.4 expected main matches, 5% Powerball), so both are judged on the same footing. Top-7 and inverse-7 from one ranking are disjoint sets.

**Required R2 changes:**

1. **Full rankings always.** Every ranking-capable method emits complete rankings of all 35 main numbers and all 20 Powerball numbers, never only its top picks.
2. **`INVERSE` as a declared selection rule.** Add it beside the existing rules in R2-C11 (top by marginal ranking, maximum-probability whole set, sampled). It is a selection-rule variant of the same fitted model, recorded in every forecast batch. It does not create 62 new E-numbers.
3. **Whole-set methods (E_57, E_16 and similar).** The "least probable whole set" can be degenerate, because many sets have near-zero probability. For these methods the inverse is the 7 lowest-ranked numbers by the method's declared marginal ranking, declared as such.
4. **Ordered-output methods (E_29-E_32, E_31).** The inverse uses the method's declared marginal main-number ranking.
5. **No ranking available.** Diagnostic-only methods, or set-only methods without marginals, record `INVERSE_UNAVAILABLE`. Nothing is fabricated.
6. **Test.** Inverse output equals the exact reversal of the same frozen ranking, under the same tie policy.

Consistent with Proposal v0.3 section 9.2 (methods may be informative when inverted).

---

## 5. NEW - rank-position measure (additional, not a replacement)

**Decision by the project owner:** report this measure **in addition to** the top-pick and inverse-pick results. All three are kept:

| Reported result per method per draw | Main barrel | Powerball |
|---|---|---|
| Top picks | matches among the 7 highest-ranked (0-7) | hit / miss of the highest-ranked |
| Inverse picks | matches among the 7 lowest-ranked (0-7) | hit / miss of the lowest-ranked |
| Rank position (new) | mean rank of the 7 drawn numbers in the full 35-ranking | rank of the drawn Powerball in the full 20-ranking |

**Why add it.** One number per method per draw shows both directions and uses the whole ranking, not just its two ends:

- **Main barrel:** chance mean 18.0 (of 35), standard deviation about 3.46 per draw. Consistently below 18 means the top end works; consistently above 18 means the inverse works.
- **Powerball:** chance mean 10.5 (of 20), standard deviation about 5.77 per draw.

**Ties.** For this measure, tied scores take the average of their tied positions (mid-rank). A method that cannot separate numbers is then neither credited nor penalised by the tie-break, and the chance means stay at 18 and 10.5.

**Placement.** The measure itself belongs to R3, but it should be fixed with the other measures **before the first real forecast** (section 3). R2 only needs the full rankings from section 4.

---

## 6. Proposed R2 v0.3 changes - checklist

| # | Location | Change |
|---|---|---|
| 1 | Section 9.2 | Seed and content identity from the digest of the permitted training view, not `source_snapshot_id` |
| 2 | Section 11.1 | Add a mandatory perturbation test (alter N and later; forecast for N byte-identical); strengthen T-05 |
| 3 | Sections 3.5 / 8.2A | FINAL weekly run = one complete pre-draw batch, pushed before the draw; nothing added afterwards |
| 4 | Section 8.2A / reports | Separate series per method and selection rule; reference chance rate shown with any reported hit |
| 5 | Sections 5.1 / 5.2 | Full 35 and 20 rankings mandatory for ranking-capable methods |
| 6 | R2-C11 | Add `INVERSE` selection rule; whole-set and ordered methods use declared marginal ranking; `INVERSE_UNAVAILABLE` status |
| 7 | Section 11.1 | Add a test: inverse equals the exact reversal of the same frozen ranking |
| 8 | Section 13.2 (R3 list) | Add the rank-position measure, reported in addition to top-pick and inverse results; mid-rank ties |
| 9 | Section 14 / S5 | Measures for step 4 fixed before the first real forecast |

*End of review.*
