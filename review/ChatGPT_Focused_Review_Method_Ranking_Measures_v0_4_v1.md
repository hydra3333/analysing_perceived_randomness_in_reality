# ChatGPT focused review — Method Ranking Measures Proposal v0.4

**Date:** 26 October 2026 (Adelaide)  
**Reviewer:** ChatGPT (independent technical/statistical spot-check)  
**Reviewed:** `Predictive_Randomness_Method_Ranking_Measures_Proposal_v0_4.md`  
**SHA-256 (locally verified):** `5652163f5e19fd2276923491fc3a52cf0445c06715304d8eafdf4d392c557bf0`  
**Compared against v0.3:** `f59cf673fe9df22778f7a973c3d36cada6b18c2def6f3b484b1bd8afccb3cbf8`  
**Scope:** v0.3 → v0.4 focused review; no authority to modify code, run research experiments, access holdout, or alter Package 2 v0.11 / P3 v0.2. This review is not owner ratification.

## Verdict

**ACCEPT AFTER TARGETED CORRECTIONS: 1 BLOCKER, 5 CORRECTIONS, 2 OPTIONAL.**

The revision resolves the central v0.3 N1 issue for genuinely fixed, outcome-independent single-track testing. Its two-class distinction is a substantial improvement. The newly introduced owner requests (MR16, side-by-side presentation and plain-English modes) are useful. I support retaining them. **One qualification on outcome-adaptive scored-set selection is needed before v0.4's `EXACT_LOCAL`, `N1_CALIBRATED` and 'guaranteed' Bonferroni claims are binding.** This is a narrower issue than the already-fixed adaptive-forecast dependence problem.

### B1 — BLOCKER: fixed hit-code law does not by itself validate testing at an outcome-selected stopping time or conditioned on a realised comparison set

**Affected:** 3.7–3.8, 5.2–5.3, 5A, 5B, MR16, MRT-16/17.

Claude's new proof is **correct for a fixed, outcome-independent list of target opportunities**, or a design obtaining a predetermined number of predictably sampled opportunities under appropriate conditions. Conditional on all previous outcomes, the fair-draw main-match and division-code probabilities are invariant to the chosen legal ticket. Thus on a fixed opportunity grid a single track's hit codes are i.i.d., even if the ticket is chosen adaptively using draws `< N`. The TOP/WORST pair also has an invariant per-draw joint code law if its set sizes and disjointness are guaranteed.

**But the current text also permits `C` to be the observed intersection of scored sets, and scored/readout availability can depend on previous outcomes.** The *number of scored opportunities* and the membership of `C` can therefore be outcome-dependent. Conditioning on the realised `C` or `n`, and replaying fair codes on that fixed realised grid, need not reproduce the full process law. A predeclared cohort alone does not prevent this.

**Exact synthetic counterexample (no lottery outcomes used):** Let a forecast method predict a legal binary hit/no-hit event on each target; under the fair null every hit is independent Bernoulli(1/2). After each scored draw it may stop returning forecasts if the *cumulative one-sided binomial tail* first reaches `<= 0.05`, otherwise it continues, for at most 20 opportunities. Every actual forecast is made before its outcome and uses only past results (N−1 satisfied). Exhaustive dynamic enumeration over the hit counts of paths not already stopped gives

`Pr_fair(at least one nominal 5% boundary reached by opportunity 20) = 0.0986785888671875`.

Thus interpreting the finally observed one-sided binomial tail as a 5%-level calibrated test would yield roughly **9.87%** false positives. Replay N1 against the *fixed realised stopping length* misses the stopping/selection rule, even though the underlying per-draw hit code is ticket-invariant. At n=2 in the simpler stop-on-first-success rule, observing n=2 logically proves the first outcome was a failure, whereas an independent Binomial(2,1/2) replay assigns positive probability to two hits.

**Required narrow repair (recommended text):**

> `EXACT_LOCAL` and `N1_CALIBRATED` for hit-sequence statistics require a recorded opportunity-set/selection protocol under which the asserted null law remains valid. In the default fixed-n implementation, the scheduled evaluated targets, eligible readouts, compared units, stopping rule and significance family must be fixed independently of the outcomes being scored; predictable selection into a fixed number of opportunities is permissible only with a separately demonstrated invariant-code law. If a scored set or sample size is outcome-adaptive, ordinary fixed-n binomial tails and N1 replays against its realised fixed `C` are **not automatically calibrated**. Retain all descriptive and reference figures, explicitly label the calibration unproven, or supply a separately verified sequential/selection-aware null. A predeclared *cohort* alone is insufficient.

At minimum add a deterministic synthetic test with outcome-dependent availability/stopping to MRT-16/17. It must reject an unconditional `N1_CALIBRATED` / guaranteed-Bonferroni status unless the test protocol satisfies the new condition. Do not remove N1; this is fully compatible with **mark, never suppress**.

### C1 — CORRECTION: MRD-24 generalises one E_1 simulation to all methods

**Affected:** 3.5A's verbatim IS description, 7.5 and 18.3.

The sentence **"a method with no skill at all typically gains about 3 sigma this way"** is not supported across all methods. Section 18.3 instead reports one 20,000-replicate fair-draw illustration using **E_1**, where the apparent in-sample gain is ~3.3 sigma under the stated metric. Methods with different flexibility or IS procedures can have very different hindsight gains, including zero. Replace the generic claim in the fixed plain-English text with e.g.:

> "The amount by which hindsight inflates the apparent success depends on the method. In a separate fair-draw illustration using this project's E_1 method, in-sample fitting alone produced an apparent gain of about 3 sigma; this is not a general value for all methods."

For this one-off illustrative simulation, either record its seed, algorithm, precise statistic and scope if recoverable or explicitly mark the numbers as **illustrative and not an independently reproducible test acceptance value**. The rule that IS results are displayed and labelled remains unchanged.

### C2 — CORRECTION: side-by-side difference requires a matched target set and an unambiguous scalar

**Affected:** 3.7, 3.4A, 7.5, MRT-06/13.

WF and IS may have different eligibility, `INVERSE_UNAVAILABLE` and history requirements. Section 7.5 says "same window and comparison set" but does not explain whether side-by-side recomputes WF and IS values on their **intersection** or displays their separate original league-table scores (possibly different `n`). Without a common scored opportunity set the difference cannot be interpreted as a hindsight comparison.

Further, not every measure has a single subtractable value: MR0 is a division vector; MR2 has gap lists and undefined values; MR16 has interval bounds, detectable effects and a p-value; some statuses are categorical. Define a per-measure **primary comparable scalar or vector component(s)** for the "hindsight advantage" column, with the unit and direction (e.g. counts, mean matches, bits, rank positions). Emit `NOT_COMPARABLE` where not defined; never subtract ranks, p-values, calibration labels or Bayes factors without an explicitly defined transformation and interpretation. Record `n_WF`, `n_IS`, `n_paired`, and the paired target-set digest. Keep ranks computed **separately** by mode. If ranks are displayed from the original league tables, label them as such and do not silently imply they were computed on the paired intersection.

### C3 — CORRECTION: MR16 'detectable ratio' is a *threshold for an observed count*, not a smallest true detectable effect

**Affected:** MR16, MRT-22, 18.4.

The five `k_3` integer thresholds and power values are accurate (see verification below). But `k_3/(n p)` is the observed success-rate ratio needed for the chosen nominal *local* 3-sigma rejection threshold. It is **not** the smallest underlying effect that the sample can detect with a declared probability. The latter depends on desired power (e.g. 80%) and significance level. Relabel the line **"observed hit-rate threshold for local 3 sigma"**, retain the 1.5× and 2× power columns, and avoid saying a sample can only detect a 'true advantage' above the displayed ratio. In IS this remains descriptive/uncalibrated. This does not alter any owner-chosen measure.

### C4 — CORRECTION: MR16 confidence interval coverage for variable or adaptive success rates

**Affected:** MR16 interval description.

A Clopper–Pearson interval is a conservative exact interval under independent identically distributed Bernoulli trials with a common success probability. Calling it **"conservative-approximate"** when the success probabilities vary is not generally justified, particularly if the sequence is adaptive or outcomes are dependent. State that it is a conventional **constant-rate reference interval**, with no asserted coverage guarantee for heterogeneous/selected/adaptive outcomes unless separately demonstrated. Preserve the computed interval under `mark, never suppress`. The exact binomial tail under the fixed-grid fair null remains valid as qualified in B1.

### C5 — CORRECTION: two stale/incorrect references

- Section 13 Stage 0 still says "ChatGPT spot-check of this v0.3". Replace with "focused spot-check of v0.4".
- MRO-03 says further measures take "MR16 onward", although MR16 is now allocated to the owner-requested hit-rate measure. Replace with **MR17 onward**.

### O1 — OPTIONAL: explicit MR6 zero-vector significance state

The new zero-probability policy correctly preserves `-infinity` raw log scores and does not retrospectively smooth. Add a final rule when **all** targets have `MR_UNDEFINED_REFERENCE`: return `MR_INSUFFICIENT_DATA` or an explicit zero-valid-reference status, never numeric zero sigma. Distinguish the raw-score count `n` from the significance-valid count `n_sig` and include both in reports. The implementation must never perform `-inf - (-inf)`.

### O2 — OPTIONAL: analysis-unit key should include channel and mode

Section 3.4A's `(analysis_unit, unit_id, sub-measure)` key is sound **provided** `unit_id` unambiguously binds `(game_id, method_id, variant_id, mode)` and the sub-measure identifies `.MAIN` versus `.PB` as well as division. Explicitly state or test that uniqueness, because separate probability vectors / ranking channels must not overwrite or be counted as one hypothesis.

## Independent mechanical checks (non-project, mathematical only)

1. **Source identity:** v0.4 SHA-256 matches `5652163f...7bf0`; v0.3 matches `f59cf673...cbf8`. I compared their actual text diff rather than relying on the change log.
2. **MR16:** independent SciPy binomial survival calculations confirm every new example:

| Event | n | Fair mean | Listed `k_3` | Exact 3-sigma threshold? | Power 1.5× | Power 2× |
|---|---:|---:|---:|---|---:|---:|
| Powerball any division | 291 | 6.61637 | 16 | YES | 0.04326 | 0.25353 |
| Powerball 3+ main | 291 | 36.32545 | 55 | YES | 0.49303 | 0.99421 |
| Powerball separate-barrel hit | 291 | 14.55 | 28 | YES | 0.10605 | 0.61362 |
| Oz Lotto any division | 220 | 4.37099 | 13 | YES | 0.01555 | 0.10187 |
| Oz Lotto 3+ main | 220 | 12.45708 | 25 | YES | 0.08391 | 0.52418 |

For each listed `k_3`, `P(X >= k_3)` is at most 0.00134990, but `P(X >= k_3−1)` is greater. Rounding in v0.4's power table is acceptable.
3. **MR14:** for deterministic valid probability vectors and exhaustive K-subset enumeration, v0.4's generalised E2/E4 and variance expression agree at `(N,K)=(10,3),(12,7),(9,4)` to floating error < 1e-15 in the examples checked. The code-free exact formula and residual-guard approach are sound.
4. **N1's two-class distinction:** I **agree** with Claude's corrected cross-track / weighted-measure limitation and with the proof for a fixed evaluation grid. My B1 concerns **adaptive selection of the grid or evaluated sample size**, not adaptive ticket choice within a fixed grid.
5. **MRD-23 / MRD-24:** separately ranking WF and IS while displaying both side by side is consistent with the original firewall *provided* C2 is specified and the IS banner remains. The added plain-English definitions improve usability once C1 is corrected.
6. **Other accepted corrections:** MR6 zeros, per-channel probability kinds, typed analysis units, MR3's hypothetical-next-opportunity label, and Monte Carlo `(k+1)/(R+1)` with interval on `k/R` are reasonable. No new reason to change Package 2 v0.11 or P3 v0.2.

## Reviewer disposition and next step

Request Claude to reply **AGREE / DISAGREE / ALTERNATIVE** to B1, C1–C5, O1–O2. An independently verified narrow edit is enough; no wholesale redesign is needed. The owner alone ratifies. Only **after** an accepted specification: assess the effects on tasks and scheduling, then decide which governing documents and handovers should be created or updated. No code or research runs follow from this review.
