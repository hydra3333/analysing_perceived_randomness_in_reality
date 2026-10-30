# Independent ChatGPT wave-2 R-3 design review v0.1

Date: 2026-10-30
Project: hydra3333/analysing_perceived_randomness_in_reality
Input: EX_068_Claude.zip, wave-2 design note v0.1 and its nine reference/probe/evidence files
Scope: R-3 design only. No code candidate, installation, master data, holdout, science run or release action.

## Verdict

REVISIONS REQUIRED: 1 BLOCKER, 1 CORRECTION, 1 OPTIONAL, 0 RECONSIDER.

The four approaches are mathematically meaningful exploratory experiments. E_2's relative gap alignment, E_17's binned hazard, E_19's de-trended and level-adjusted periodic score, and E_18's finite exact mixture fit are suitable concepts. The central outstanding issue is not the validity of using harmonic ages; it is the explicit, consequential assertion that the harmonic-age slope is exactly Method A's log-age logistic predictor in ranking. It is not. Resolve that scientific identity before owner ratification and code development.

## Findings

### W2-B01 - E_17 Method A exact-ranking identity is false (BLOCKER; focused R-3 RECHECK)

Design section 4.2 and owner decision W2-3 state that replacing log(k) by H_k yields exactly the same Method A rankings, relying on the true sign-equivalence between profiled-intercept logistic regression and the corresponding covariance with the SAME covariate. That equivalence does NOT extend to replacing the covariate by another strictly increasing transform. The covariance sign may change, reversing the ranking of different projected ages. Ridge shrinkage cannot fix a covariate-induced sign reversal.

Independent constructive counterexample: 104 invented draws, L=35, K=7, generated deterministically by selecting the seven labels with lowest SHA-256 digests of ASCII `32|draw_position|label` at each draw (labels 1..35). The companion `w2_methodA_counterexample.py` independently accumulates valid at-risk and event exposures after first appearance. For n=sum(R_k), e=sum(E_k), let a_k=n E_k-e R_k. Then:

  S_log = (1/n) * sum_k a_k log(k)
  S_H   = (1/n) * sum_k a_k H_k.

The script certifies sign(S_log) NEGATIVE by comparing two exact integer products after prime factorisation of the k^a_k terms, with no floating-point logarithms. It certifies sign(S_H) POSITIVE using Fraction. The observed projected ages include 1, 2, 3, 5, 11, 12, 20 and 21: Method A's log-age logistic form ranks younger ages first; proposed E_17 harmonic-slope ranks older ages first. Both fit directions are nonzero. This counterexample uses the actual Powerball MAIN barrel dimensions, synthetic history, and a deterministic no-RNG generator. Run `python3 -I w2_methodA_counterexample.py`.

The statement that the signs can differ only when the trend is 'close to zero' has no general mathematical guarantee or defined closeness criterion. Nor does a maximum additive change of 0.43 between H_k and log(k) establish sign invariance of covariance.

Accepted focused resolution choices, requiring an explicit owner decision:
 A. Preserve the claim 'Method A's predictor' and specify a mathematically faithful log-age ranking sign. The sign can in principle be obtained without floating point: it is the exact comparison between products of integer powers k^a_k. Production feasibility, canonical ties and a suitable certified algorithm remain to be designed/tested, not presumed from this toy proof. The intercept-profiled logistic/ridge sign argument then uses the original covariate.
 B. Keep the present exact harmonic-age least-squares experiment, but label it honestly as a Method-A-inspired SURROGATE rather than an exact reconstruction; distinguish its identity and variant nomenclature (e.g. `HAZARD_HARMONIC_SLOPE_V1` instead of `HAZARD_LOGSLOPE_V1`); expressly ratify the deviation under W2-3. The binned E_17 variants can stay as proposed.

Either is scientifically legitimate. Do not silently choose on the owner's behalf. No general objection to the H_k model itself.

### W2-C01 - shared right-censoring statement wrongly includes E_18 fitting (CORRECTION; focused R-3 RECHECK)

Design section 3.2 says the open stretch since last appearance 'enters the hazard estimates only as at-risk exposures without an event (right-censored)'. The supplied E_18 equation and reference implementation in section 4.4 fit mixture weights from COMPLETED gaps, not from the right-censored open stretch: it is used only as the projected age for querying the fitted mixture hazard. E_17/E_19 do include the at-risk non-event exposures. E_2 also uses the projected age, not a hazard estimator.

Clarify 3.2 and E_18's fitting description so that this distinction is explicit. If the owner intentionally retains a completed-gaps-only descriptive estimator, say so, including its finite-window selection/censoring limitation; there is no obligation to change the mathematical method. If instead the author wants right-censoring likelihood contributions in E_18 fitting, that is a scientific change requiring its own design review and revised worked examples.

### W2-O01 - template draft-3 proposed floating-point prohibition is overly categorical (OPTIONAL)

Section 12 item 1 says 'No iterative floating-point fits in published values', suggesting all logistic/EM/other iterative floating-point fits necessarily break reproducibility. Cross-platform bitwise divergence is a real risk, and exact or certified deterministic methods are desirable here. But a blanket scientific ban would needlessly exclude unusual exploratory methods that can provide a rigorously specified deterministic publication, fixed rounding and stable tie handling. Consider wording as a byte-reproducibility requirement, with exact arithmetic preferred and any iterative floating-point publication requiring objective cross-platform proof and canonical output rules. No Wave-2 source or variant change is requested by this optional item.

## Independent checks and answers to EX_068's six highlighted questions

1. E_17 logistic sign argument: conditional on using the SAME covariate and a profiled intercept, the slope-sign argument is sound (including a nonnegative slope ridge penalty). It does not justify H_k replacing log(k). W2-B01 demonstrates actual reversal. Original Method A document was not enclosed; the comparison is against its description in EX_068.
2. E_19: pooled trend b(k), per-residue O/X and per-label division by overall level are algebraically specified and reproducible. The planted single-label-cycle probe's adjusted comparison is meaningful. It remains a relative score, not a probability, and should be evaluated as such. No blocking concern.
3. E_18: independently constructed exact bin vectors for all three real barrels. Each set has four linearly independent rows and positive FAIR denominators, making the stated quadratic strictly convex on the feasible affine simplex; KKT stationarity and complementary inequalities are an appropriate exact optimality certificate. Strict convexity proves unique weights for the declared library/binning, not stable physical attribution; the author's fair-data probe already discloses that FAST/SLOW can imitate FAIR.
4. Overlap: E_17 age-ordering and age-bin ties, E_19 multiplicative ratio identity, and the E_18 FAIR nested case hold as mathematical relationships. E_18's partial frequency overlap and the TOP-7 figures are descriptions of the supplied deterministic invented probes, not population-level inference. The author fairly reports weak component identification and failure on the single-age spike planted case. No redundancy-based veto is appropriate.
5. W2-3 and W2-8: separating simulated-envelope diagnostics A1-A5 from the present deterministic predictor is reasonable; their root seed belongs at or before the first relevant simulation design (WF-1 as proposed, subject to the governing R3/seed documents not present in this archive). This procedural choice does NOT cure W2-B01's predictor-identity discrepancy. No simulation or NIST download is authorised by this review.
6. Template draft-3 findings: the sign/monotonicity trap, planted single-label checks, and removal of already-modelled effects are useful. Item 1 warrants W2-O01's qualification. The code-stage template text must be checked when it is actually submitted.

## Evidence and boundaries

- EX_068 outer ZIP: SHA-256 `4589a228e25d703993ebeecbaa81a1b07607f7b0ffe769698ff0377a1f9fb6fd` and ZIP CRC PASS; 11 flat members.
- All ten non-message members' stored-byte and CRLF-to-LF SHA-256 values match EX_068's dual-hash inventory.
- Design note canonical LF SHA-256 `3192c255e0817fa139bf8d85d4762686c0888bc080c0a4e5cb60b038c4923c01`.
- Reference script canonical LF SHA-256 `c8ee4de378146e26798b740467b1bf49d2e244c1927ad9eed3524d69895cb55a`; `python3 -I reference_wave2.py` PASS including all exact worked-example assertions and the second-route exposure check.
- Independently reproduced E_18 exact four-component rank=4 and positive FAIR bin shares for (35,7), (20,1), (47,7) and the (10,2) worked-example barrel.
- `python3 -I probe_bias.py` and `probe_e2_rhythm.py` completed with their author-stated outputs. The longer `probe_e19pl.py` exceeded a 12-second local bound and is NOT claimed independently reproduced; its results remain author-provided. The complete historical probe table was inspected as evidence, not treated as independent replication.
- Independent exact-sign counterexample in the enclosed script PASS on synthetic Powerball-sized data. It changes no repository or evidence file.
- No independent access to the installed repository, original Method A proposal, other governing documents or final histories. Installed Wave-1 state at commit 947c370 is Claude-reported in EX_068 and was not independently verified by this review.

## Owner decisions W2-1..W2-8

W2-1 SUPPORT shared helper. W2-2 SUPPORT the method/variant breadth and fixed windows, but E_17's slope identity/nomenclature is conditional on W2-B01. W2-3 REQUIRES explicit owner resolution of faithful Method A versus harmonic surrogate; SUPPORT deferring A1-A5 diagnostic package independently. W2-4 SUPPORT score-only. W2-5 SUPPORT fixed four-law exact chi-square library, with W2-C01's honest completed-gap censoring description. W2-6 SUPPORT fixed per-label T=2,3,4 periodic adjustment. W2-7 SUPPORT the template findings subject to optional W2-O01. W2-8 SUPPORT settling the seed no later than the first simulated WF-1 design, conditional on its actual dependencies.

## REVIEWER-DECIDED dispositions

W2-069-RD-01 (REVIEWER-DECIDED): R-3 design v0.1 requires focused correction/recheck, with W2-B01 scientific identity and W2-C01 censoring wording. Do not ratify unchanged or treat the present design as an implementation authorisation.
W2-069-RD-02 (REVIEWER-DECIDED): retain all four exploratory methods and their general architecture; invite a bounded correction, not a redesign or redundancy veto.
W2-069-RD-03 (REVIEWER-DECIDED): W2-O01 is optional advisory; no general prohibition on iterative floating-point research methods is endorsed without the owner's rule decision.
W2-069-RD-04 (REVIEWER-DECIDED): the original Method A-versus-surrogate choice is consequential science and must be OWNER-DECIDED. Neither option is silently selected by the reviewer.

End of report.
