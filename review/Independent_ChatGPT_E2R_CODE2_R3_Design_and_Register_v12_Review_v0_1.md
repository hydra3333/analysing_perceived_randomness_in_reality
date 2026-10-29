# Independent ChatGPT review - EX_038: Register v0.12 and E2R-CODE-2 design v0.1

Date: 2026-10-29 (Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Review role: independent reviewer, R-3 design stage
Scope: content review of Register v0.12, CODE-2 design stage, and the conditional CODE-2 code review decision

## 1. Separate verdicts

A. Register v0.12: CONTENT PASS. 0 BLOCKER, 0 CORRECTION, 0 OPTIONAL, 0 RECONSIDER. Owner ratification and document-only installation remain separate.

B. E2R-CODE-2 design note v0.1: REVISIONS REQUIRED. 2 BLOCKER, 3 CORRECTION, 1 OPTIONAL, 0 RECONSIDER. Retain the overall CODE-2 package boundary and E_1 option (a). This is a design-stage verdict, not a finding that candidate code has failed.

C. CODE-2 candidate implementation: NOT REVIEWED, NOT RUN. The EX_038 request expressly permits a HIGH-tier code RECHECK with R-2 ONLY IF the design passes unchanged. It has not. The candidate's hashes and presence have been inventoried, but there is no source audit, implementation PASS, mutation verification, or 156/166 test result from this reviewer. Return a corrected design for focused R-3 RECHECK first.

## 2. Evidence and mechanical checks

- Outer EX_038 archive SHA-256: fef339ddcdb550e4f718bd6fdb81690b17ac636cbc1e43646cfb4f699bf9d7c2.
- E2R-CODE-2 note, as stored in EX_038: 1f050b2e30661e742481476f7414a1efe1f43937b755115f770e6b3c12f5c245.
- Register v0.12 in EX_038: stored CRLF SHA-256 5c84715b5385830c358d5c408007093b2cf597f9dafecc045aa3200e4fc0b72a; LF SHA-256 e1ac8b550267e6067e3b12ef651a071f59a0b4d4a43474b2a981fecf45fe567c.
- Reconstructed the ratified Register v0.11 (704dbd6383fcef5a4501b8dbc867eedcdabd8df82d1945e80dcddb5a2e0996ea) by applying its documented ratification-only version-line change to the retained v0.11 candidate. Ran Claude's three-counted-edit builder. It produced the submitted v0.12 LF bytes exactly.
- Compared the CODE-2 design against ratified E2R-1 v0.3r3 (SHA-256 0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954) and the owner decisions in the register. The original source bytes were available from earlier supplied project packages.
- The enclosed CODE-2 code ZIP (SHA-256 a5e8ac89e658ae4f67165d6f230b5afd39ace1ee0bc8e5609057c7e439154a49) and base snapshot ZIP (8de9f1615a0017f0715be72922845d2f50373e20dcfa87fd8e2a5832de066ac2) were identified, but NOT tested or audited, in accordance with EX_038's conditional request.
- I have not independently fetched current GitHub HEAD. Reported remote commits, Linux runs, mutations and Windows evidence from Claude/the owner remain reported evidence, not an independent reproduction in this review.

## 3. Register v0.12 - content review

PASS. Its new section records CODE-1 v2 installation at 205ae73, the owner's post-push rather than pre-commit suite run (and separate owner-machine rehearsal), the EX_034 / EX_036 reviews and RD-01..RD-08, the 29 October owner decisions, and the bounded role of the local Claude Code runner. The technical and procedural evidence sources remain distinguished. No new ratification is inferred from the candidate, and the older register's historical text remains intact.

The single RATIFICATION CANDIDATE placeholder is to be resolved upon the owner's actual ratification; the resulting final bytes need their own identity. The document-only installation and Claude's later GitHub check remain outstanding. No DOC-2-style install verifier or reviewer review of a document-only ZIP is requested.

## 4. CODE-2 design findings

### E2RC2-B01 - Legacy standalone runner versus mandatory normal-dispatch gate (BLOCKER; RECHECK)

Location: CODE-2 note sections 1, 3, 5, 10 (D2-3). Authority: E2R-R57 and R58 (ratified v0.3r3); E2R-R50/R52 legacy preservation.

Failure scenario: the design says a normal standalone/coordinate contract dispatch must use an active SUPPORTED variant, exact pin, and absent development flag. Yet `E_001_Historical_Appearance_Frequency.py` remains runnable directly, unchanged and un-gated. If E_1's registry status is subsequently withdrawn or its development flag installed, an operator could still invoke this standalone path. The note calls it a frozen legacy regression route, but does not define a binding boundary separating it from normal scientific dispatch. Preserving legacy goldens is correct; silently exempting a normal runnable path from E2R-R57 is not.

Required design resolution: specify an enforceable and tested classification for the legacy path, for example a narrowly scoped owner-ratified **legacy regression-only exception** that does not permit normal new E2R scientific publications, or introduce a separately approved gate/launcher restriction without changing frozen E_1 scientific code. State explicitly whether the legacy path can still read real development data and write historical E1 records, and how its operation differs from normal supported-method dispatch. If an exception to the ratified release rule is needed, bring that normative change to the owner, not merely to a comment in CODE-2. Retain legacy goldens and E_1 revision 1 unless the owner ratifies otherwise. Add a negative scenario with E_1 registry status non-SUPPORTED and/or flag present.

This is a design ambiguity about a concrete bypass, not a demand to edit the 11 coordinator-protected functions.

### E2RC2-B02 - Unauthenticated consumption-gate boolean (BLOCKER; RECHECK)

Location: CODE-2 note section 4, `read_run(folder, declaration, gates_pass)`; section 8 interrupted/failure consumption tests. Authority: E2R-R38A and existing result/exit-receipt/orphan firewalls.

Failure scenario: `read_run()` advertises `gates_pass` as a caller-provided result for all existing group and firewall gates. Without defining who may compute it, when it is recomputed, and what proves it, a caller can pass `True` even with a currently unresolved orphan marker or missing required exit-receipt evidence and receive a result marked consumable. The terminal SUCCESS check alone does not replace those gates. This is especially serious if later code treats `read_run()` as the accepted-consumption API.

Required design resolution: either (preferred) make the authoritative consumption path derive the applicable gate results itself from verified, current evidence, fail-closed on absent/unknown evidence, and clearly specify standalone versus coordinator-only gates; or define a private trusted gate-evidence object that only the verified orchestration consumer can construct, rather than accepting an arbitrary boolean at the public trust boundary. A boolean is permissible only as an internal low-level validator argument under an independently enforced, documented outer consumer gate. Add negative tests for forged `gates_pass=True`, an active orphan marker, and absent/mismatched applicable group or exit evidence. No cleanup or termination is proposed.

### E2RC2-C01 - Prove atomic create-only publication rather than relying on os.rename (CORRECTION; RECHECK)

Location: CODE-2 note section 4, "How files are written". Authority: E2R-R36, R38A and create-only identity rules.

`os.rename()` does not universally guarantee no-overwrite: on POSIX, renaming a temporary file to an existing regular-file destination can silently replace that destination. A pre-rename `exists()` check is a race. Merely saying the destination "must not exist" does not establish the required property. Specify a no-clobber, cross-platform publish primitive (for example exclusive destination creation with appropriate atomic/failure semantics, or a verified safe alternative), with directory durability and cleanup of *only* owned temporary files. Test existing-target refusal and concurrent writers on both Linux and Windows, without ever overwriting a prior output or receipt. Preserve the no-delete/no-recovery policy for published records.

### E2RC2-C02 - Distinguish legitimate no-ticket/no-diagnostic from invalid output (CORRECTION; RECHECK)

Location: CODE-2 note section 4 choices (a) and (b); authority E2R-R03/R04, section 7.4 and E2R-R35/R38.

Ratified section 7.4 expressly permits a method with no ticket to write C2 or nothing when no diagnostic exists, and says such targets are counted as unscored `DIAGNOSTIC_ONLY`. The CODE-2 note instead makes every "no record" a `VALIDATION_FAILURE` (`NO_RECORD`). Differentiate a valid no-prediction/no-diagnostic outcome from an invalid output of a method that promised a record. If choosing to retain terminal `VALIDATION_FAILURE` as a technical status, explicitly require reporting to count a legitimate empty target as DIAGNOSTIC_ONLY, never as a scientific invalidity, and explain how the contract distinguishes the cases. Otherwise propose a separately approved schema-consistent terminal disposition. Do not invent a C1/score and do not silently drop the target.

INSUFFICIENT_HISTORY with a valid C1 plus successful D2 is coherent in principle because C1 carries the scientific status; ensure it is still unscored and not conflated with PREDICTION_AVAILABLE. No change to the frozen D2 vocabulary may be implicit.

### E2RC2-C03 - Per-method Package 2 roster is not a variant admission authority (CORRECTION; RECHECK)

Location: CODE-2 note section 7 and section 8 roster tests; authority E2R-R19/R57.

`method_status(game, method)` returns SUPPORTED if **any** variant is supported and no flag exists. That is a useful informational roll-up but cannot approve a request for another, FORMULA_OPEN or stale variant. The note says normal dispatch is variant-exact, but it also says Package 2's synthetic plumbing consumes this per-method status. Specify and test that a SUPPORTED roll-up never alone grants a run, never selects a different variant and cannot bypass the exact entry pin at the true dispatch boundary. The proof must include a method with two differently admitted variants, not only the current E_1 SUPPORTED/E_2..E_62 FORMULA_OPEN snapshot.

### E2RC2-O01 - Diagnostic-only command-line entry limitation (OPTIONAL; reviewer does not block)

Location: CODE-2 section 4 choice (c). E2R-R41 and R62 permit C2-only products, but the initial command line can only request the forecast product. Label this plainly as a CODE-2 *launcher capability limit*, not a limitation of the approved stage-1 contract. Preserve C2-only fixtures in the library tests and identify which later owner-scoped package would expose them via the command line. Do not introduce a new launcher mode merely for this optional finding.

## 5. Owner decisions D2-1 to D2-4

- D2-1: SUPPORT in principle. Coordinator-side gate refuses all admitted coordinated requests, and no coordinator protected function changes. The sidecar is not yet an installed invocation from coordinator_main; do not claim a working coordinated launch gate, only an intentionally rejecting entry point for future integration.
- D2-2: SUPPORT. The additional real-development switch defaults False and is tested. Keep all other three False and the coordinated allowlist empty. No owner permission to turn on any switch follows.
- D2-3: NOT YET CLEARED as written, for B01. Legacy compatibility should not become an unrecorded exception to R57. Owner can resolve a scoped exception or authorise a separately reviewed gating boundary.
- D2-4: SUPPORT subject to C03. A registry-backed roll-up is useful but variant-exact dispatch remains authoritative.

The E_1 adapter outside `E_001/`, its unchanged method implementation, and exact label-for-label independent verification are supported at design stage. The proof must remain exact and cannot rely on ordinary tests alone. There is no authorisation to create a method revision or alter legacy scientific code.

## 6. Reviewer decisions and next package

All changes that affect normal method dispatch, scientific publication, or result consumption concern always-review subjects. Dispositions: B01, B02, C01, C02, C03 = RECHECK; O01 = OPTIONAL with no corrective gate. No FIX AND PROCEED applies.

REVIEWER-DECIDED (new for this review):
- E2RC2-RD-01: Register v0.12 content PASS with ratification and finalisation/install gates preserved.
- E2RC2-RD-02: Retain HIGH-tier design review; B01 and B02 block unchanged approval, and all five required design corrections receive RECHECK.
- E2RC2-RD-03: Do NOT commence R-2 code RECHECK or execute the supplied candidate; EX_038 condition (design passes unchanged) is false.
- E2RC2-RD-04: Support D2-1 and D2-2, and D2-4 with variant-exact safeguard. Request owner resolution of D2-3; no protected-function or E_1 scientific change authorised.
- E2RC2-RD-05: Preserve the one revision E_1 wrapper plan and prohibit undocumented registry/legacy-gate exceptions.

No departure from the existing rules is authorised by this review. The DOC-only simplification affects installation transport, not substantive content review or code-package proof. Please report every REVIEWER-DECIDED item under the project's current oversight/reporting arrangement.

Recommended next handoff: a focused CODE-2 design note v0.1r1 with exact diff, review matrix and owner disposition for D2-3. Only after an unchanged-PASS at design recheck should the candidate receive the independent HIGH-tier R-2 code audit and synthetic offline tests. The code candidate may need updates then. Keep the owner, real masters, holdout, beacon, switches, science allowlist and Git operations outside this review.

End of review.
