# Independent ChatGPT focused HIGH-tier RECHECK - E2R-CODE-2 candidate v3 - v0.1

Date: 2026-10-29
Project: hydra3333/analysing_perceived_randomness_in_reality
Review input: EX_042_Claude.zip; E2R_CODE2_Install_v3_candidate.zip
Review predecessor: EX_041 code findings on the EX_040 v2 candidate
Status: INDEPENDENT FOCUSED RECHECK PASS; owner installation and Windows acceptance pending

## 1. Verdict and limits

PASS for the two specifically returned code blockers E2RC2-CODE-B01 and E2RC2-CODE-B02.
0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER remaining from this focused recheck.
Both dispositions remain RECHECK, not FIX AND PROCEED. E2R-CODE-2 design v0.1r1 is unchanged and retains its previously reviewed PASS. No new design review is needed for these corrections.

This is a HIGH-tier source review, not project-owner ratification or installation approval. Candidate v3 is suitable for owner acceptance consideration and final package preparation, with subsequent full owner Windows acceptance, guarded installation and Git verification still required. The prior v2 candidate must not be installed.

## 2. Independently verified package identities and change scope

EX_042_Claude.zip SHA-256 (as received):
  dde93a5ae9e2a5e8da2cbe300d5c11064f8dc0cd1259aa807a7c6de7cbbf5881
E2R_CODE2_Install_v3_candidate.zip SHA-256 (enclosed):
  0f4b6600d3a239a0de124ce8365c382450eb6df24a07750457a58505f3ebd69f
Supplied BASE_b846519_src_tests.zip SHA-256 (EX_040, used for offline tests):
  c6cd0be836c0ff4cbf9b213556382e1f702762e23c7743556f12bf4fd716f3f6
Supplied v2 candidate used for comparison (EX_040) SHA-256:
  cea050a0a6ab8c5e15a3d4c58abe03b18a500e64d20029b9a73c2694aea57e00

Independent manifest check: 22/22 paths and canonical LF SHA-256s match (19 A, 3 M).
Independent patch replay: all seven v2-to-v3 modified files matched the candidate byte-for-byte after CRLF/LF normalisation. They are:
  src/coordinator_private/contract_coordinated_gate.py
  src/methods/_common/contract_dispatch.py
  src/methods/_common/contract_publication.py
  src/methods/_common/contract_runner.py
  tests/e2r_code2_fixtures.py
  tests/test_e2r_dispatch.py
  tests/test_e2r_runner.py

The E_1 scientific implementation and three predecessor-modification files retain their v2 bytes. The unchanged design note also matches the v2 copy exactly. No other shared v2 overlay source or test file was altered. The new or renamed review-evidence members are separate and checked by the v3 manifest.

## 3. E2RC2-CODE-B01 - PASS, RECHECK closed

Previously the public runner/dispatch/consumer accepted caller-chosen orphan-marker and registry or method-folder roots; the prior synthetic reproducer demonstrated actual safety-gate bypass.

Candidate v3:
- dispatch_gate, legacy_gate, variant_released, active_pins, gate_coordinated_contract_request, run_contract_method and read_run no longer accept the relevant caller-selected locator parameters.
- The dispatch gate obtains DATA_ROOT and METHODS_ROOT from fixed installed-module constants, and reloads the installed registry on admission. run_contract_method checks its fixed ORPHAN_MARKER before reading data or creating output. read_run uses the same marker and installed registry on each consumption call.
- The production run API independently checks synthetic workspace boundaries; REAL_DEVELOPMENT still refuses while its code-level switch is False, and its data source is restricted to the project root if that switch is ever separately authorised.
- Only a specifically scoped test fixture patches these module constants in-process, for synthetic temporary data.

The five new NoCallerChosenAuthority tests passed independently, including forbidden-keyword TypeError, the genuine marker refusal/consumption interlock, STANDALONE outputs and data-source refusal. The previous reviewer's v2 reproducer no longer proceeds through its first bypass call: it raises TypeError, consistent with Claude's supplied evidence.

Finding CLOSED. This establishes no caller-selected authority parameter in the reviewed production interfaces; it is not a claim that arbitrary untrusted Python able to monkeypatch process globals is a supported security boundary.

## 4. E2RC2-CODE-B02 - PASS, RECHECK closed

run_contract_method and RunPublication no longer take an execution_path argument. Publication fixes execution_path to STANDALONE in the terminal and receipts. Calls attempting to pass execution_path=COORDINATED are rejected at the Python signature boundary, without creating a run folder. The coordinated gate continues to deny coordinated contract dispatch. read_run also refuses records claiming COORDINATED, as defence in depth.

The independent offline tests validated STANDALONE terminal/receipt identity and tested forbidden keywords. No successful COORDINATED publication through the reviewed standalone API was observed.

Finding CLOSED. CODE-2 has not enabled coordinated execution or real-development scientific runs.

## 5. R-2 test reproduction and exclusions

Environment: isolated disposable source/test snapshot assembled from EX_040 BASE_b846519 and the reviewed v3 src/tests overlay; Linux, CPython 3.13.5. PYTHONPATH restricted to snapshot src, src/methods, tests. No real master files or holdout files mounted into the snapshot. No project installation and no network or beacon operations.

PASS: 179/179 selected unit tests, zero skips and zero failures:
- 127 tests in twelve independent offline modules, including 18 dispatch and 34 runner tests.
- 52 CODE-1 contract tests, selected to omit the one six-worker T12 test.
- The five NoCallerChosenAuthority tests passed individually as well as within the runner module.

NOT independently reproduced here:
- 10 reader-contract tests needing real master inputs (intentionally excluded).
- 1 six-worker E2R-T12 case (optional for this focused review).
Therefore NOT a 190/190 acceptance claim. Claude reports 190/190 on Python 3.13.17 and 3.15.0b4 and 22/22 mutation catches; these are AUTHOR evidence, not independent reproduction here. Full owner Windows tests and install checks remain mandatory.

An initial test-enumeration helper failed to find the local tests package because of an incomplete PYTHONPATH. It ran no contract tests; after correcting the import path, all 52 selected tests passed. This harness setup issue was not a CODE-2 test failure.

## 6. Explicit REVIEWER-DECIDED items

E2RC2-RD-12: Close E2RC2-CODE-B01 after independent source and synthetic-test RECHECK - PASS. Reviewer disposition RECHECK completed.
E2RC2-RD-13: Close E2RC2-CODE-B02 after independent source and synthetic-test RECHECK - PASS. Reviewer disposition RECHECK completed.
E2RC2-RD-14: Accept the bounded R-2 evidence of 179 selected tests, and expressly reserve the ten real-master-dependent tests and T12 to owner/author acceptance. Do not equate this with 190-test acceptance.
E2RC2-RD-15: Recommend E2R-CODE-2 candidate v3 for owner acceptance consideration and subsequent owner-controlled finalisation/installation. Preserve all existing owner gates, Windows acceptance, protected-code requirements and post-push Git verification.

Claude should report RD-12 through RD-15 to the project owner. No departure from ratified safety, scientific or process rules is authorised or identified by this recheck.

## 7. Next step and prohibitions

Claude may prepare the final owner-reviewed package, including the appropriate later register edition, without reopening the unchanged E2R-CODE-2 design. This PASS does not ratify D2-1, D2-2 or D2-4; those owner decisions remain separate.

No install, source mutation in the user's repository, real lottery data access, holdout inspection, beacon fetch, worker termination, switch change or Git action was performed by ChatGPT.

End of independent review.
