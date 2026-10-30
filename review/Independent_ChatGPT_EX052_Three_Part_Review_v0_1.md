# Independent ChatGPT review: EX_052 three-part R-3 and package-content round v0.1

Date: 2026-10-30 (Australia/Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Source: EX_052_Claude.zip, SHA-256 33ca3a06569f5707efe964a0060d24ddba2bbfd73e6111af5ca6c6113fa26257
Authority: independent reviewer; not an owner ratification or permission to install/run

## Verdicts

1. E_6 v2 versus approved v1: NARROW CONTENT/IDENTITY PASS. No new code review of otherwise unchanged v1 functionality is claimed.
2. Ratification Register v0.15 candidate: CONTENT PASS, exact predecessor reconstruction PASS. Owner ratification and [T12-E6] are pending.
3. E_3/E_4 polynomial-fit design v0.1: R-3 DESIGN PASS UNCHANGED, with two OPTIONAL code-review/test clarifications. D34-1 through D34-5 are supported for owner decision, not ratified by this review.

Counts for this round: 0 BLOCKER; 0 CORRECTION; 2 OPTIONAL (E_3/E_4); 0 RECONSIDER.

## Evidence and limitations

- Outer uploaded EX_052 archive: SHA-256 verified against owner-supplied full hash; ZIP integrity PASS; all nine declared member hashes checked (raw and canonical LF; binary treated as binary).
- Inner E6_Install_v2_candidate.zip: SHA-256 7678c6acff271ba715b3644f9a098eeb47ce95b08e7d0bb68dac34b7f61008aa; ZIP integrity PASS.
- All 46 non-directory ZIP member identities match E6_Install_v2_zip_members.txt.
- All 42 installation-manifest payload identities match the inner archive: 39 additions, 3 replacements. This is a candidate package integrity check, not an install.
- The v1 archive used for comparison was the previously independently reviewed E6_Install_v1_candidate.zip from EX_050, not an invented predecessor.
- candidate_v1_to_v2.diff applied cleanly to a disposable extraction of the v1 source/template/test overlay and reproduced every affected v2 file byte-for-byte. No real data or experiments were used.
- The full-memory declarations and registry entries (both games) remain byte-identical. The runner, existing common libraries, release switches, coordinator, and E_6 flag are unchanged. No mathematical statement or executable arithmetic has changed in beta_bernoulli.py; its delta is text/docstrings. The contract.py delta is PROVENANCE text only. The test update asserts the fit version distinction.
- The author reports 210 tests on two Python versions, 14/14 mutation catches, and LF/CRLF installer rehearsals. These are AUTHOR EVIDENCE, not independently rerun in this narrow round. Owner Windows suite, T12 decision, PRE/POST/COMMITTED and subsequent Git verification remain mandatory.

## 1. E_6 v2 review

The two lambda < 1 variants now use BETA_BERNOULLI_DISCOUNTED_UPDATE_V1 rather than the plain posterior-mean fit label, and the relevant declaration calibration notes, registry explanations, generator, template examples, source comments and PROVENANCE consistently distinguish discounted (power-likelihood) updates. Their canonical declaration digests and associated registry references change accordingly, as expected. BETA_BERNOULLI_FULL_MEMORY_V1 retains the original declaration, registry, and mathematics. The E_6 design note v0.1 is unchanged; its earlier terminology is explicitly marked out of date in the new register.

The use of a proper generalised/power-likelihood update should not be confused with the posterior of the ordinary undiscounted independent-Bernoulli model. The new texts make that distinction without implying that discounted estimates are calibrated or physically predictive.

Verdict: PASS. E6-052-RD-01 (REVIEWER-DECIDED): accept the narrow v2 terminology/identity changes, without reopening the accepted E_6 design or changing its revision. This does not install v2.

## 2. Register v0.15 candidate

Reconstruction: starting from the previously reviewed v0.14 candidate, apply the documented ratification finalisation: replace its version header, fill [H-STATUS] in both rows with OWNER-RATIFIED 29 Oct 2026, and fill [H2-V1R5-SHA] in both positions with 67a1b3eaa3e1f51415eceba513fd7e1a39de91619296f0efba97ba108570a094. The resulting canonical LF SHA-256 is exactly 74d2ae89a16d2c7a971db1b62e89c3e9aa7f6a2803a9102516507fa705e2bfa4, the stated installed v0.14 identity.

Running make_register_v15.py against that exact predecessor applies precisely three counted edits and produces the submitted v0.15 canonical LF content byte-for-byte: SHA-256 97f134bddbf6153f91e57c5aec3326a6c5d9a2ba7f623d1bb0d4309a486d557e (755 LF lines).

Content: it accurately separates the owner-reported purpose restatement, DOC-6 and duplicate-EX cleanup as Claude-reported Git evidence, EX_051 reviewer verdicts, D6-1 through D6-5 as owner decisions, E_6's intended non-runnable install, and later WF-1 as planning only. Its historical E_6 terminology exception, H-1 contract-entry-file supersession, and pending owner acceptance are explicit. It correctly refrains from declaring the candidate owner-ratified or an install complete.

The version-line RATIFICATION CANDIDATE and [T12-E6] remain intentional placeholders; they must be resolved by the owner and final package preparation before installation. Current public Git history was not fetched independently in this review; the document explicitly attributes that verification to Claude.

Verdict: PASS. REG15-052-RD-02 (REVIEWER-DECIDED): content acceptable for owner ratification; future hash-affecting finalisation remains a distinct mechanical operation.

## 3. E_3 and E_4 polynomial fits: R-3 design review

Scientific scope: two exploratory rankers of the same per-label indicator histories for each barrel. E_3 uses the exact fitted polynomial's p(0); E_4 uses its exact p'(0). The input at target N ends at N-1, using the UNORDERED_SET view without dates. Six predeclared configurations per method, both games, yield 24 method declarations, installed initially FORMULA_OPEN and IN_DEVELOPMENT. Publishing score-only rankings with probability_kind NONE is correct: extrapolated polynomial values/slopes are not calibrated probabilities.

Mathematics: plain rational least squares on a finite integer grid has a unique solution when M>D; interpolation at the five fixed distinct integer Chebyshev-node positions uniquely defines its degree-4 polynomial; and discrete polynomial minimax is unique on the stated grid because the polynomial space satisfies the Haar property and M>=D+2. The exact alternation certificate is an appropriate independent optimality test. All stated variant windows and degrees meet these conditions.

Independent hand checks: the specified M=52, D=4 node rule gives [50,40,26,11,1]; least squares for y=[0,0,1,1] at t=[-4,-3,-2,-1] gives p(t)=3/2+(2/5)t; the three-point worked interpolation gives p(0)=-3, p'(0)=-4. The exact rational coefficients, deterministic float64 conversion at publication and explicit tie policy support cross-platform identity.

The centered H=4 smoother is confined to the historical window, including truncated boundary averages; it is not an N-1 leak. The design correctly acknowledges that endpoint extrapolation is vulnerable, that least squares is polynomial LS regardless of basis in exact arithmetic, and that raw 0/1 minimax often degenerates to a constant fit. These are interpretive limitations, not reasons to veto exploratory work.

OPTIONAL E34-O01 (implementation proof and test): In the implementation and R-2 evidence, specify/test deterministic Stiefel single-point exchange in detail: violating-index ties, reference replacement, sign orientation, an intermediate h=0 reference with errors elsewhere, the exactly-polynomial case, certificate failure, and the 10,000-iteration cap. The current design specifies the objective, uniqueness, initial reference, tie for largest error and exact certificate; no mathematical variant is left open. This is a code-stage assurance, not a precondition for R-3 PASS.

OPTIONAL E34-O02 (independent cross-label invariants): For LS and interpolation only, exploit the fact that each draw contains exactly K labels and smoothing is linear. Therefore the exact per-label polynomials must sum to the constant K: sum_j p_j(0)=K and sum_j p'_j(0)=0 (per barrel; before float rounding). This supplies a powerful independent synthetic regression oracle. Do not impose this invariant on MINIMAX, whose nonlinear fit need not preserve it. These tests do not change any scientific setting.

D34-1: SUPPORT one jointly versioned shared helper. D34-2: SUPPORT six frozen variants and node positions. D34-3: SUPPORT raw LS and H=4-smoothed interpolation/minimax; treat the boundary smoother as part of the scientific hypothesis, not a physical causal explanation. D34-4: SUPPORT scores only, with no fabricated probability vector. D34-5: SUPPORT precise naming: ordinary polynomial least squares, Chebyshev nodes and minimax criterion where applicable.

Verdict: DESIGN PASS UNCHANGED. E34-052-RD-03 (REVIEWER-DECIDED): the primary designer may prepare the E_3/E_4 code candidate following the owner's method-level decisions, using this frozen design; the new code still requires its own HIGH-tier R-2, tests, owner ratification and controlled install.

## Standing boundaries

No owner decision is presumed. E_6 remains non-runnable in the proposed installed state. E_3/E_4 remain unimplemented and non-runnable as of this review. No Python project science was run, no real master or holdout data were accessed, and no process-kill, orphan interlock, registry gate, release switch, launch wrapper, or coordinator change was authorised.
