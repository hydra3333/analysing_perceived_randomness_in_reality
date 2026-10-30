# Independent ChatGPT wave-2 design v0.1r2 focused R-3 RECHECK

Date: 2026-10-30
Scope: EX_072_Claude.zip; W2R1-C01, W2R1-C02 and W2R1-O01. DESIGN/REFERENCE ONLY.
Verdict: PASS UNCHANGED. 0 BLOCKER; 0 CORRECTION; 0 OPTIONAL; 0 RECONSIDER.

## Input and identity

- Incoming ZIP SHA-256 d8c78908742eae687dd1154e90104e8201df3da39e7489b7f6606254012e4b8f. ZIP integrity PASS. 9 flat members, of which 8 are covered by the dual-hash table. All 8 stored and CRLF-to-LF SHA-256 pairs match exactly.
- Ratified status is not claimed: predecessor v0.1r1 is a reviewed design, LF SHA-256 2b832830a4489cc1fd742e1eb0042571b521e7decbdbfbb963b4e97eea06e4b0, independently available from EX_070. The supplied six-edit builder accepted that predecessor and reproduced the submitted v0.1r2 exactly.
- All three patches (design, reference_wave2.py and probe_logage_sign.py) replayed against exact prior LF bytes with zero fuzz and yielded precisely the new submitted LF bytes. The first trial of the design diff was an output-filename harness mistake; re-running against the unchanged predecessor confirmed byte identity. It was not a source defect.
- Resulting design LF SHA-256 2ab342911701edf1e93ad590e4765a3efac54a76d732b7fd2c5875c7d363fe74. Reference LF SHA-256 078006f5394b67a73f0815b73cdf5abd42b8151b551845efee2ba67b5fda07ed. Changed probe LF SHA-256 9b74c6575379dc9a07341b0ac22048c74e66925b4cb3229d5ec4c04c0622a4d1.

## W2R1-C01: exact-zero verifier

PASS. Let a_k be the integer age coefficients and S=sum_k a_k ln k. By unique integer factorisation, S=0 iff all e_p=sum_k a_k v_p(k) vanish. This handles cancellations with nonzero a_k, including 6 ln 1 -12 ln 2 + 6 ln 4=0. The author now specifies two separately implemented factorisation methods: method route uses trial division to find prime exponents; verifier uses a smallest-prime-factor sieve and derives its own exponent map. Both have an explicit empty-map zero result. On a nonzero sieve result, direct rational atanh intervals on ln k (not prime-log intervals) determine the sign, with a 1,024-term refusal cap.

This is appropriately independent at algorithmic level while intentionally sharing the mathematical exact-zero identity. The cap is fail-closed: if the direct bounds do not certify, a ValueError is raised; a sign is never guessed. The proof that direct bounds eventually separate a genuinely nonzero real value is sound, although a finite implementation can refuse if 1,024 terms are insufficient. That is expressly part of the design and not a defect.

Independent execution, isolated from project files:
- python3 -I reference_wave2.py: all example assertions PASS, including the eight-draw zero witness and explicit cap-refusal check. The primary sign of zero and verifier sign of zero agree; Method A slope-sign score sigma=0 in that fixture.
- python3 -I probe_logage_sign.py: 312 synthetic targets across the three game barrels; primary trial-factorisation sign, sieve-plus-direct-bounds sign and 60-digit Decimal sign all agree; -1 counterexample remains and +1 example is covered.
- Reviewer-written exhaustive cross-check for all 5^6=15,625 integer coefficient vectors with ages 1..6 and each coefficient in {-2,-1,0,1,2}: prime maps from trial division and SPF sieve match in every case; 65 exact-zero combinations were correctly recognised. Sampled 162 nonzero combinations matched 90-digit Decimal signs using the verifier. A synthetic source-isolation test replaces the method route with a deliberate exception and confirms verifier operation remains unaffected.
- For EX_071's witness, raw direct bounds without the zero branch refuse under the cap (measured about 0.14 s here), rather than looping indefinitely.

The independent exhaustive coefficient test is an auxiliary verifier test, not evidence of predictive performance. The enclosed script exercises the submitted reference code; it is not project source and is not a replacement for an implementation-stage HIGH-tier review.

## W2R1-C02 and W2R1-O01

W2R1-C02 PASS. The design's section 13 now says that wave-2 construction of Method A A1-A5 diagnostics was not selected under W2-3 and would require a new owner decision plus prior R-004 resolution. No owner decision has been reversed.

W2R1-O01 ADOPTED. Section 4.4 now cautiously says that a future survival likelihood addressing right censoring and window/left-boundary ascertainment effects *could* address the E_18 completed-gap biases. It does not imply the present fitted weights include an open stretch or that a future likelihood automatically cures all selection problems.

## Scope, standing scientific review and decisions

The reviewed math retains the owner's faithful log(age) E_17 ranking, rather than the rejected harmonic substitute. No new scientific choice or variant change is proposed. E_2, E_18 and E_19 remain as reviewed in EX_069/EX_071. W2-1, W2-2, W2-4, W2-5, W2-6 and W2-8 remain owner proposals unless separately ratified; W2-3 and W2-7 remain described as owner-decided. The package is a draft design, not running code or a permission to access master/holdout data.

- W2-073-RD-09: close W2R1-C01, focused RECHECK PASS.
- W2-073-RD-10: close W2R1-C02; accept W2R1-O01 adoption.
- W2-073-RD-11: wave-2 design v0.1r2 R-3 PASS unchanged; advance to owner-ratification consideration, subject to existing project safety and future independent code review.

No project, Git, release switches, real draws, holdouts or coordinator state were accessed or modified.

End of review.
