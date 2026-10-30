# Independent ChatGPT review: Wave 2 R-2, template draft 3, register v0.19

Date: 2026-10-30
Project: hydra3333/analysing_perceived_randomness_in_reality
Input: EX_074_Claude.zip
Review: HIGH-tier R-2 for E_2, E_17, E_18, E_19 and shared gaps helper; separate document reviews

## 1. Verdict

- WAVE 2 CODE (R-2, HIGH tier): PASS, 0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER. Exact reviewed candidate only; not ratification or installation permission.
- NEW-METHOD TEMPLATE DRAFT 3: CONTENT PASS, 0 findings.
- REGISTER v0.19 RATIFICATION CANDIDATE: CONTENT PASS, 0 findings. The version and T12-W2 markers remain unresolved by design and require owner decisions.

All four methods are installed-as-non-runnable candidates. Do not interpret this PASS as authorising real draw data, scientific results, holdout access, method release, or coordinated execution.

## 2. Input identity and mechanical verification

- Outer EX_074_Claude.zip SHA-256: 41ad8a9c945cbd2a0e88a5f391c1e7c0b0e1b4715c8e8d0cd8b8fba8fbb732c1.
- Inner W2_Install_v1_candidate.zip SHA-256: 30219330cd73687b12d2442fb176712c59966f92f8da6977ae7ca50d020e0515.
- BASE_8f44d50_src_tests_template.zip SHA-256: e2162b35e51ccbd43aee8a087a380669dc52ed1f8a17348c2445b5add260e8da.
- ZIP integrity PASS for outer and inner ZIPs. All 11 dual-hash records in EX_074 agree with the actual bytes, and all 360 file rows in the baseline inventory and all 93 file rows in the candidate inventory match both as-stored and canonical-LF SHA-256 values.
- Installation manifest: 89 file hashes independently matched the candidate (86 A + 3 M). The manifest is itself the 87th added overlay file: 87 A + 3 M overall, precisely as reported.
- The three replacements are Method_Contract_Runner.py, doc/METHOD_TEMPLATE/README.md, and doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md. The supplied unified diff reverse-applied onto the candidate to reproduce all three baseline files exactly, and forward-applied to reproduce all three candidate bytes exactly.
- No previous existing coordinator, reader, scientific method, contract library, switch, allowlist or safety-gate file is replaced. The four new method folders each retain IN_DEVELOPMENT.txt. All 24 new registry entries are FORMULA_OPEN; eight preexisting NOT_YET_SPECIFIED placeholders account for the remainder in these methods' registry folders.
- Evidence is from these supplied artifacts, not a live GitHub checkout; I have not independently established that the baseline matches remote HEAD 8f44d50.

## 3. Mathematical and software review

- Shared helper recurrence_gaps.py: appearances, completed and windowed gaps, censored age-exposures, bins and log-age signs agree with the frozen v0.1r2 rules. The two exposure routes are different constructions; the zero-case prime-factor checks are independent (trial division vs smallest-prime-factor sieve); nonzero signs use rational interval certification with a refusal cap. The historical W2-B01 and W2R1-C01 failure witnesses are asserted in tests.
- E_2: mean/median/last-eight gap variants, fair recurrence fallback, projected-age relative-distance score, and telescoping/counting verification agree with specification.
- E_17: binned hazards use the declared prior, windows and ages. Log-age variant uses the faithful log(age) covariance sign, not the withdrawn harmonic surrogate, and both certification routes are checked.
- E_18: FAST/FAIR/SLOW/REGULAR laws, completed-gap-only fitting, exact simplex support enumeration and exact KKT optimality certificate agree with the frozen design; alternate survival is computed by summing gap probabilities. Its verify route refits weights with the same fit routine, but an independent KKT certificate is checked. This shared-code limitation is openly acknowledged, not silently represented as a wholly independent optimiser.
- E_19: exact age-residue pooling, per-label factors and level normalisation agree with the formula; the second route computes pooled residues from pooled age counts rather than summing label residue arrays.
- All four methods are score-only (NONE probability), use the unordered view with dates off, enforce their minimum histories, and rely on the established contract to assemble ties/TOP/WORST. Contract-level synthetic release tests and installed-state refusal checks passed.
- The new tests contain independent from-specification rules, source-boundary checks, mutation-sensitive tests, and the proven relations among methods. No apparent mathematical change to the ratified design or scientific-identity break was found.

## 4. Independent tests: precise scope

Python 3.13.5, Linux; supplied BASE_8f44d50 source/test/template snapshot plus candidate overlay, isolated scratch copy; no project master draw data or holdout file was accessed.

- Wave 2 method module: 19/19 PASS (33.9 seconds), run separately.
- Shared recurrence-gaps module: 12/12 PASS, run separately.
- Applicable predecessor tests: 257/257 PASS, including 52 selected contract tests with the T12Determinism case excluded, 34 CODE-2 runner tests, 18 dispatch tests, 20 E_6 tests, 32 E_3/E_4 and helper tests, 26 Wave 1/helper tests, and other legacy/guard tests. No failures or skips in these selected runs.
- TOTAL INDEPENDENTLY REPRODUCED: 288/288 selected tests passed; the runs were separate rather than a successful single invocation of RUN_W2_SUITE.py.
- Not reproduced: ten reader-contract tests requiring real master files and the single E2R-T12 six-worker test (owner approval for W2 rehearsal/install remains pending). The full 299-test Windows suite is NOT claimed to have been run by this reviewer.
- Author evidence, independently read but not rerun: 299/299 on Python 3.13.17 and 3.15.0b4, 39/39 planted defects, fake-method template trial and LF/CRLF installation negatives. Their outcome is not counted as independent test reproduction.

## 5. Template draft 3

README.md exact reconstruction: eight counted edits; specification template: two counted edits. Both built from the supplied, hash-pinned installed draft-2 files using the enclosed draft-3 builder, and both produced the candidate bytes exactly.

The revisions correctly require byte-identical published outputs while permitting objectively verified floating-point methods, flag the sign/covariate-equivalence traps, encourage planted label effects and removing already-measured factors, require proved loop exits and refusal caps, and require computed expectations even inside tests. The code skeletons remain untouched. CONTENT PASS.

## 6. Register v0.19

- Candidate canonical-LF SHA-256: d6822419bf76a9232e59b37cd805efe9dd402b91d786dd2be7726d0d91a16197.
- Reverse-applying the provided diff reproduced installed register v0.18 SHA-256 85125c4900dabee53d2674d0ca3a18abbed64d5179b7f0b178300f928de93c97.
- Running make_register_v19.py with that predecessor re-created the candidate byte-for-byte, with its three counted edits.
- The new section faithfully distinguishes Wave 1's reported owner installation and Claude's GitHub verification, the Wave 2 design's two earlier revisions, EX_069/071 findings (including Claude's acknowledged mistakes), EX_073 PASS, the owner's Wave 2 decisions, and planned non-runnable package contents. It does not predeclare Wave 2 acceptance.
- The version line still says RATIFICATION CANDIDATE and the W2 test-authorisation marker remains [T12-W2]. These are explicit OWNER-DECIDED items, not review failures. No extra register-only review round is recommended.

## 7. Decisions and gates

W2-075-RD-01 (REVIEWER-DECIDED): R-2 PASS on the exact candidate's code and safety boundaries; 0/0/0/0 findings.
W2-075-RD-02 (REVIEWER-DECIDED): template draft 3 CONTENT PASS with byte-exact builder reconstruction.
W2-075-RD-03 (REVIEWER-DECIDED): register v0.19 candidate CONTENT PASS; owner ratification and subsequent status/hash finalisation remain separate.
W2-075-RD-04 (REVIEWER-DECIDED): independent offline evidence is 288 selected PASS, not a substitute for the owner's Windows 299-test acceptance. T12-W2 is not decided by the reviewer.

For owner action: ratify candidate/design attachments and decide T12-W2 as appropriate; then Claude prepares the final package with only authorised register status/T12 and dependent manifest/verifier changes. Follow the established owner Windows PRE/POST/299-test/COMMITTED gates, then independent GitHub committed-blob verification. The owner's prior waiver of a final-ZIP reviewer check is respected; no new check is demanded.

No repository installation, real scientific runs, raw real draws, holdout accesses, or process termination performed by this reviewer.
