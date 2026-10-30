# Independent ChatGPT review - Wave 1 R-3 and new-method template draft 2, v0.1

Date: 2026-10-30
Project: hydra3333/analysing_perceived_randomness_in_reality
Input: EX_061_Claude.zip; design note v0.1; README and specification-template draft 2; counted diffs and builder; reference script.
Status: independent design and document review, not owner ratification or code review.

## 1. Dispositions

| Subject | Disposition | BLOCKER | CORRECTION | OPTIONAL | RECONSIDER |
|---|---|---:|---:|---:|---:|
| Wave 1 design, E_7/E_8/E_9/E_10, R-3 | NARROW CORRECTION; focused RECHECK before code | 0 | 1 (W1-C01, shared) | 1 (W1-O01) | 0 |
| Template draft 2: README + specification template | NARROW CORRECTION; same W1-C01 | 0 | 0 additional | 1 (T2-O01) | 0 |

W1-C01 is a single cross-document finding, not two independent corrections. The four specified algorithms are mathematically coherent; no variant change, additional hypothesis, or different model family is requested. Design is NOT an unchanged PASS, therefore no code is authorised by this review. The next review should examine the exact bounded text correction, not reopen all of wave 1.

## 2. Archive and provenance evidence

- EX_061_Claude.zip: SHA-256 c0df4030b556e8f3da9c313fc5e5ed2bf057763ea5d4a6fecc5c4167ebf11833; ZIP integrity PASS, eight members.
- EX_061_Claude.md: as-stored SHA-256 d7c9ab5fdff8b616e23f9db6221f60c862749234ee8a6d141240e8b92fd69d19.
- Wave 1 design note: as-stored SHA-256 b3126ea80751e029690b003a8f574b742687867c6e07650c2fd7a7e224596b64; canonical LF SHA-256 c9501103619d3aaa6848e2f356cf7692e892732ddd2f5d07316e524191e9d93c.
- README draft 2: canonical LF SHA-256 92c9db9bedb30d18e3f88340d2e8f7573792c50f8d8560da814fa2a394ff1261.
- METHOD_SPECIFICATION_TEMPLATE.md draft 2: canonical LF SHA-256 759ad3a0151e7292a45abfc0ea8b8b1f9ba70210511b19ebf38e5be7425a31c3.
- Reversed and then reapplied all 8 README and 3 specification-template builder replacements; each required string was unique and both final LF outputs matched exactly.
- Reconstructed README draft-1 LF SHA-256 f17e2d6eb489797415252689038078047011b7aa7ba2e24f987c265078df3e26, equal to the builder's pinned predecessor hash.
- Reconstructed specification-template draft-1 LF SHA-256 3812f671977382fc94e89477de5c417133800e71d0002397c40843b051fbadf6. This hash is reconstruction evidence, NOT independent authentication against a live installed Git blob: the supplied builder pins only the README predecessor.
- GitHub installation claim at 8defe9d and subsequent working order are Claude/owner-reported context; not independently verified from live GitHub here.

## 3. Scientific and mathematical assessment

### E_7: windowed Beta shrinkage

For every barrel, s_j = (c*r + k_j(M))/(c+M). The same positive affine transformation of each label's count preserves ranked score groups. Since sum_j k_j(M)=K*M and L*r=K, sum_j s_j=K exactly; with c>0 and 0<r<1, every marginal lies strictly between 0 and 1. The 52/104 window variants differ from full-history counting; the full-history version has E_1's score groups, but different tie-breaking and model probabilities. Keeping this calibration comparator is scientifically reasonable.

### E_9: weighted occurrence counts

s_j = sum_i lambda^age(i)*x_i(j) is exact as a rational number, with age zero for the newest draw. At the SAME lambda, E_6's discounted Beta means are a common positive affine function of this sum, so they give the same score groups. The three chosen factors differ from E_6's listed 74/75 and 149/150. Score-only semantics are correct.

### E_10: disjoint-window contrasts

s_j = k_j(S)/S - (k_j(Lw)-k_j(S))/(Lw-S), with Lw>S, is a well-defined exact signed score. The short and preceding windows have no common draws. Under independent fair draws, their observations for one label are independent across the two windows; this does not assert within-draw independence across labels. The fixed fair-draw standardisation would be a common positive scale and so does not affect ranking. No probability vector is justified.

### E_8: pooled moment estimate for period-level variation

Write q_j=mu_j(1-mu_j), and suppose independent periods have latent inclusion rate theta_{j,b} with mean mu_j and variance tau_j^2; within a period there are P conditionally independent Bernoulli indicators for a given label. Then

Var(p_{j,b}) = tau_j^2 + (q_j - tau_j^2)/P.

For n independent periods, the unbiased rate sample variance V_j has expectation Var(p); the empirical m_j obeys E[m_j(1-m_j)] = q_j - Var(p)/n. Consequently E[m_j(1-m_j)+V_j/n] = q_j and

E[ (V_j - (m_j(1-m_j)+V_j/n)/P) * P/(P-1) ] = tau_j^2.

This validates the stated un-clamped moment formula for P>=2,n>=2 under its stated mixture assumptions. After averaging across labels and clamping t to [0,r(1-r)], the chosen rational weight

w = P*t / ((P-1)*t + r(1-r))

satisfies 0<=w<=1. The common weight, rather than label-dependent weights, gives sum_j s_j=K because every complete period has K*P selections. These are per-label marginal estimates, not a coherent joint model for K labels drawn without replacement. The specification already makes that limitation explicit. The moment plug-in, pooled fair-rate denominator and clamp make the output an approximate empirical-Bayes-style construction, not an exact full Dirichlet-multinomial posterior; the note substantially acknowledges this.

Reference checks: all five worked-example outputs agree with the source formulas. An independently written integer-count/sum-of-squares E_8 calculation matched the supplied two-pass-rate implementation on all C(5,2)^4 = 10,000 synthetic histories of four draws, plus the 4-label, 6-draw upper-cap example (t=1/4, w=1). All checked cases preserve sum_j s_j=K and scores in [0,1]. Script included in EX_062. This is a mathematics check, NOT the future implementation's R-2 tests.

### Honest overlap, selection and independence

The stated E_7-full/E_1, E_9/E_6-at-matching-lambda, and E_8-at-w=0 equivalences are appropriately scoped to ranked groups. Distinct TIE_SHA256_V1 identities can change the ordering INSIDE tied groups; TOP/WORST tickets should not be used as an oracle for ranking equivalence. E_8 with w=0 coincides with E_1 over all W only when n*P=W, a condition already stated in section 7. No reason to exclude the overlapping E_7 calibration variant: method correlation is to be recorded, not prohibited.

## 4. Findings

### W1-C01 - Count-only does not imply monotonicity (CORRECTION; focused RECHECK)

Locations: wave-1 design note section 1, paragraph beginning "A design point found while specifying them"; template README draft 2, "Things that bite", bullet "The same-count ranking trap".

The documents claim that a score depending only on a label's own occurrence count over the same draws is therefore monotonic, and hence ranks exactly as counting. Equal exposure alone does NOT establish monotonicity. A common, deliberately non-monotonic count transform such as f(k)=-(k-5)^2 is count-only yet orders labels differently from increasing raw counts. This is a real scientific overstatement, particularly in a project deliberately open to unconventional methods.

Required narrow correction: say that **a common strictly increasing function of each label's count over the same draws** preserves ranked score groups; name posterior mean / fixed positive shrinkage and E_8 at w=0 as examples, and explicitly avoid excluding non-monotonic count-only scores. Retain all method equations, windows, variants and W1-3 calibration rationale. Align the design text and README bullet. Suggested wording:

"When all labels share the same exposure, any score given by the SAME strictly increasing function of each label's count has exactly the ranked groups of raw counts over that window. E_7's fixed-strength posterior means and E_8 when w=0 have this property. Count-only scores need not be monotonic in general; this observation does not exclude deliberately non-monotonic methods."

Reason for RECHECK: this corrects a general scientific/ranking claim in the design, even though it does not change the four formulas. Focused text-only review of the replacement suffices; do not initiate code review until the corrected design is passed and owner decisions are settled.

### W1-O01 - Make the upper-cap worked example explicit in the reference script (OPTIONAL)

Location: design section 9 example 5; reference_wave1_examples.py's __main__ demonstration.

The E_8 cap example is mathematically correct and the reference function computes it when called. However, the script's __main__ currently prints a different 5-label, 8-draw `ex2` and does NOT visibly exercise the design's stated 4-label, 6-draw cap case. Add an explicit exact assertion and print of that cap example to make the "script computed every worked example" claim directly repeatable. This is a traceability improvement, not a scientific defect or prerequisite to design approval.

### T2-O01 - Pin the draft-1 specification template identity too (OPTIONAL)

Location: make_template_draft2.py WANT dictionary.

The builder pins README.md but does not pin the installed draft-1 METHOD_SPECIFICATION_TEMPLATE.md. Its counted replacement still replayed exactly against the reconstructed predecessor. For stronger provenance in the final package, verify the installed specification-template bytes and pin their LF SHA-256 in the builder as well. Do not treat the reconstruction hash above as authenticated from GitHub without that verification.

## 5. Template draft 2 assessment

The additions for shared helpers, score-only channels, insufficient history, multiple methods, per-variant mutation tests, externally computed examples, explicit ranking coincidence and the owner-requested keep-current policy are useful and do not alter the governing E2R or R2/R3 contracts. The score-only case correctly avoids inventing probabilities. The template's README shares W1-C01 and should be corrected in the same edit round. The deferred *.py.txt skeleton modifications are explicitly part of the later code package and are not reviewed here.

## 6. Owner decisions and reviewer dispositions

- W1-1 shared occurrence-count helper: SUPPORT, provided it has its own tests and dependent method revision discipline.
- W1-2 twelve listed variants: SUPPORT as frozen initial explorations; choice of horizons remains owner-ratified, not claimed optimised.
- W1-3 retain E_7 full-history calibration variant: SUPPORT. Identical ranked groups do not make its probability estimates equivalent to E_1, and correlation is not exclusion grounds.
- W1-4 E_9/E_10 scores only; E_7/E_8 marginal probabilities: SUPPORT with the existing calibration and joint-law caveats.
- W1-5 template draft 2: SUPPORT after correcting the shared W1-C01 wording.
- W1-6 E_8 rational method of moments rather than sampled full Bayesian model: SUPPORT. The construction is explicit, checkable and exploratory; its physical/forecast merit remains to be measured.

REVIEWER-DECIDED:
- W1-RD-01: R-3 design scientifically viable, but W1-C01 requires a narrow corrected design before PASS; no code review or implementation authorisation from this result.
- W1-RD-02: template draft 2 viable with the SAME W1-C01 correction; no additional template blocker.
- W1-RD-03: W1-O01 and T2-O01 optional, to be accepted or declined without reopening scientific formulas.
- W1-RD-04: R-3 independent checks limited to supplied docs and synthetic mathematical fixtures; owner ratification and any later HIGH-tier code R-2 remain separate.

No code candidate was supplied or reviewed. No real/holdout data, scientific run, installation, repository mutation, flag flip or coordinator process action occurred.
