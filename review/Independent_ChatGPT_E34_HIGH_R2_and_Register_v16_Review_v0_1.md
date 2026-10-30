# Independent ChatGPT E_3/E_4 HIGH-tier R-2 and Register v0.16 content review v0.1

Date: 2026-10-30 (Australia/Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Basis: EX_055_Claude.zip and its two inner archives; frozen EX_052/EX_053 design; earlier reviewed register v0.15 candidate.
Reviewer scope: independent code/design-identity review, synthetic/offline tests, candidate register content only. Not an installation, scientific execution, or owner ratification.

## Verdicts

1. E_3/E_4 code candidate E34_Install_v1_candidate.zip: HIGH-tier R-2 PASS; 0 BLOCKER, 0 CORRECTION, 0 OPTIONAL, 0 RECONSIDER.
2. Register v0.16 RATIFICATION CANDIDATE: CONTENT PASS; 0 BLOCKER, 0 CORRECTION, 0 OPTIONAL, 0 RECONSIDER.
3. Owner's separate ratification and acceptance still required; no current release or live-data run is authorised. E_3 and E_4 remain non-runnable at package installation.

## Package and predecessor integrity

- EX_055_Claude.zip SHA-256 verified: de0bc8a2776880ea26992d058283797f1b46ea5da9e34a09fad8de3335cefd61.
- E34_Install_v1_candidate.zip SHA-256 verified: cb303f5364fd3c6cb33870078ad29f84de5a5a7e82c903062b5fb9b7df916e7c.
- BASE_7c93320_src_tests.zip SHA-256 verified: ec6b0720960d651f94d77b1e9dd641e0fd4c4d46db1ece04067a1048eadb52a4.
- Each ZIP passed its CRC/integrity test. Verified both the stored and CRLF-to-LF SHA-256 identities of all 224 baseline files and all 73 inner package files against the supplied inventories. Outer EX_055 member digests matched its table.
- Installation manifest contains 68 A records and 1 M record, each matching its payload bytes. The manifest excludes itself from its own list; including that additional overlay file yields exactly 69 added and 1 replaced files as claimed. The sole replacement, Method_Contract_Runner.py, reconstructed byte-for-byte from the baseline by adding two imports and two adapter entries, with no other change.
- Prior frozen E_3/E_4 design v0.1 SHA-256 b9d60b4c753bb90c6a7ca302fb4802c353b0ae23fbe82c2b417ae7b089fad072 equals the packaged design exactly.
- Registry declarations/entries: 24 declarations plus 24 FORMULA_OPEN entries; both method flags present, separate existing NOT_YET_SPECIFIED placeholders retained. The package does not alter project coordinator, reader, contract libraries, E_1, E_6, switches or allowlist.

## Mathematics and code-path review

- Shared helper uses exact Fraction coefficients and exact fixed-window t = -M..-1; target t = 0, no target-row use. E_3 scores exact polynomial coefficient a_0, E_4 scores a_1, each converted to float64 once at the output boundary. These are score-only readouts with probability_kind NONE.
- Least squares: shared normal-matrix inverse over labels; separate orthogonal-polynomial (Forsythe) recurrence cross-check. Interpolation: fixed five Chebyshev-derived integer nodes, Lagrange/Newton cross-check. Minimax: deterministic single-point exchange with lowest-index tie rule, bounded iteration and an exact D+2 alternating-extremal-error certificate.
- The window/degree/half-width configurations match all six owner-selected frozen variants. Smoothing is clipped to the eligible window; fewer than M draws yields INSUFFICIENT_HISTORY. Only the view supplied through the contract is used by the scientific method code.
- E34-O01 is implemented as tests of minimax alternation, tie ordering, zero reference level, exchange cap, exact-polynomial zero error and rejection of an insufficient alternation certificate. E34-O02 is implemented as exact coefficient-sum [K,0,...,0] invariants for LS and interpolation across both games/barrels and both algorithms; not wrongly imposed on nonlinear minimax.
- Through-the-contract synthetic tests confirm correct forecast/verification and publication, N-1/suffix invariance, and refusal under the installed FORMULA_OPEN gate. No protected-function modifications detected in the supplied overlay.

## Independent execution evidence

- 32/32 new tests passed, zero skips: 19 tests.test_polynomial_fits and 13 tests.test_e3_e4_polynomial.
- 127/127 selected predecessor tests passed, zero skips: static/timing, launch/manifest, exit receipts, allowlist, synthetic scorer, T05, E1-ALIGN, E1 standalone, Windows lifecycle review, E2R prefix, E2R dispatch and E2R runner.
- 52/52 selected E2R contract tests passed with the six-worker T12 test explicitly excluded.
- 20/20 E_6 tests passed in a separate isolated run.
- TOTAL: 231/231 selected independent offline tests passed, zero failures or skips, against the supplied baseline plus uninstalled E_3/E_4 overlay. Ten real-master-dependent reader-contract tests and one owner-controlled E2R-T12 test were intentionally not run. Consequently this is NOT full 242-test Windows acceptance.
- Additional independent stress test: 1,968 exhaustive synthetic binary sequences at windows 4 through 8 and degrees 0 through 3 (where allowed), each with half-width-1 smoothing, completed with exact worst-error equality and alternation-certificate validity. This is a supplementary check, not a change to the frozen variants.
- Claude reports 242 tests passing on Python 3.13.17 and Python 3.15.0b4, with 27/27 planted defects detected. These are author-side claims, not independently certified here. An attempted run of the complete mutation harness exceeded this review environment's execution limit before yielding a complete result; no independent 27/27 claim is made. A first combined older-test run likewise hit a timeout; all 231 selected cases were subsequently completed in separate runs.

## Register v0.16 content and exact reconstruction

- Reconstructed the installed v0.15 bytes from the previously reviewed v0.15 candidate with exactly two finalisations: ratification status and E2R-T12 E_6 owner-approval text. SHA-256 matched installed v0.15: 405cc2f964db5a86cdf6a94bfc1382d01911ef9f41162b047c43c7f1af04ea2e.
- Reapplied make_register_v16.py's three counted edits against that predecessor. All occurrence counts were one; the resulting LF bytes exactly match the submitted candidate's LF-normalised bytes: SHA-256 66f3c977714960cb64193bf87daa612f970fb25edf1980c4434ac6935be85ab1.
- The inserted section distinguishes Claude Code TASK_T005 author-reported rehearsal from owner Windows installation and Claude GitHub verification, and records the temporary redirected status file as a deviation rather than hiding it. It records EX_053 review decisions, owner D34-1..D34-5, the owner-reminders file's non-rule status, the planned non-runnable E_3/E_4 package, and explicit historical statements superseded by v0.16.
- The register does not falsely state E_3/E_4 is already installed: the package is phrased as an installation with this register, with acceptance recorded only afterwards. Both intentional placeholders are preserved: RATIFICATION CANDIDATE and [T12-E34]. The owner must decide the latter; the E_6 T12 approval does not automatically extend to E_3/E_4.
- The source SHA and claims about a live GitHub commit rely on Claude's reports unless separately confirmed by the owner. This review independently verifies only the supplied files and their content relationships.

## REVIEWER-DECIDED dispositions

- E34-056-RD-01 (REVIEWER-DECIDED): HIGH-tier R-2 scientific-method candidate PASS unchanged, provided the install overlay remains byte-identical to the reviewed science and its owner-controlled acceptance remains in force. No source changes or revision increments requested.
- REG16-056-RD-02 (REVIEWER-DECIDED): Register v0.16 CONTENT PASS for the owner's ratification consideration. Only owner-approved finalisation of the candidate status and [T12-E34], and the dependent manifest/verifier identities, may be treated as narrow final-package edits; any other scientific change requires RECHECK.
- E34-056-RD-03 (REVIEWER-DECIDED): Both EX_053 optional test expectations are satisfied; no follow-on design change requested.

## Outstanding gates / recommended owner action

Owner ratification of register v0.16, a separate decision on E2R-T12 for this installation, preparation of final ZIP with dependent identities, Claude Code rehearsal if authorised, owner's Windows PRE/POST/full 242-test/COMMITTED acceptance before push, and subsequent independent GitHub commit verification. Keep E_3 and E_4 installed non-runnable. Do not use real lottery/holdout data or start coordinated/scientific runs merely because the code candidate passed review.

End of independent review.
