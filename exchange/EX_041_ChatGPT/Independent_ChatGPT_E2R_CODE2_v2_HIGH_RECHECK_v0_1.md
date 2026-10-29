# Independent ChatGPT R-3 / HIGH-tier R-2 review - E2R-CODE-2 v0.1r1 / candidate v2

Date: 2026-10-29
Project: hydra3333/analysing_perceived_randomness_in_reality
Review role: ChatGPT independent reviewer
Scope: focused design RECHECK of EX_039 findings, then conditional HIGH-tier code RECHECK and authorised synthetic/offline R-2

## 1. Separate verdicts

A. DESIGN v0.1r1: PASS, unchanged, 0 remaining BLOCKER/CORRECTION/OPTIONAL/RECONSIDER at the design stage. The five required EX_039 findings (B01, B02, C01, C02, C03) and O01 are adequately resolved in the design. The v0.1 to v0.1r1 exact diff reproduces the revised design after line-ending normalisation. E_1 remains revision 1 conditionally: its scientific implementation must remain unchanged, and the legacy entry change must be confined to the extra pre-computation release gate.

B. CONDITIONAL CODE v2: REVISIONS REQUIRED. Two new BLOCKER findings, both RECHECK, 0 CORRECTION/OPTIONAL/RECONSIDER. The code exposes caller-controllable safety/registry evidence overrides, and it permits a standalone runner call to publish a SUCCESS D2 labelled COORDINATED. Do not install this v2 candidate.

C. R-2: 174 selected offline tests passed with 0 skips; no full 185-test acceptance is claimed. The 10 tests requiring unsupplied real master fixtures were excluded, and the one optional six-worker T12 case was not run. Three additional synthetic negative probes reproduced the new findings. The author's 185/185 tests and 18/18 mutation results remain author-reported, not independently reproduced as complete acceptance.

## 2. Verified identities and code scope

EX_040_Claude.zip SHA-256: 982195ba56ebe466b75f208b9cbf2c4ec232b2102f1a5bcb3e279f98308c3774.
BASE_b846519_src_tests.zip SHA-256: c6cd0be836c0ff4cbf9b213556382e1f702762e23c7743556f12bf4fd716f3f6.
E2R_CODE2_Install_v2_candidate.zip SHA-256: cea050a0a6ab8c5e15a3d4c58abe03b18a500e64d20029b9a73c2694aea57e00.
Design v0.1r1 stored SHA-256: 06414d6d2e85f6302cae4c0ca63f3d3cf95ea610a47d068cf00973718a973323. Git/LF form: f0c36fd3dabb83dcc5f21d8b92bd9b5c3eaf9647da069a4e5bff63514a26f2dd.

The design patch replayed exactly after explicit CRLF to LF conversion. The installed-base snapshot was used as supplied, not independently fetched from live GitHub. The candidate's 19 manifest rows passed SHA-256 verification (16 new paths listed in the manifest, plus the manifest file itself = 17 new paths; 3 modified paths). All three modified-file base hashes match the snapshot. The legacy E_1 executable has exactly eight inserted lines; the E_1 scientific modules, shared reader, main coordinator and protected coordinator functions were not changed in the overlay. No live Git or Windows acceptance claim is made.

## 3. EX_039 design finding closure

- E2RC2-B01: CLOSED at DESIGN. Owner D2-3 requires legacy_gate on both legacy modes before input or output; no blanket legacy exception. The eight-line insertion plan preserves E_1 calculation code.
- E2RC2-B02: CLOSED at DESIGN. read_run(folder) is specified to gather its own applicable orphan, installed registry, declaration, standalone and receipt evidence, with no caller-supplied gates_pass boolean. Coordinated outputs cannot be consumed through CODE-2.
- E2RC2-C01: CLOSED at DESIGN. Exclusive temporary creation and os.link create-only publication refuse existing destinations and fail closed without hard links; no rename fallback.
- E2RC2-C02: CLOSED at DESIGN. Valid empty target with no diagnostic is unscored DIAGNOSTIC_ONLY by explicit reporting disposition, while the frozen terminal vocabulary is left unchanged. The technical D2 VALIDATION_FAILURE/NO_TICKET_NO_DIAGNOSTIC representation is qualified and must never be reported as scientific invalidity.
- E2RC2-C03: CLOSED at DESIGN. The method-level SUPPORTED roster is informational. Both dispatch and synthetic Package 2 admission are variant-specific; mixed and withdrawn variants are negative cases.
- E2RC2-O01: CLOSED at DESIGN. CLI diagnostic-only omission is explicitly a CODE-2 launcher limitation, not a restriction of the underlying contract.

Owner D2-1, D2-2 and D2-4 remain owner choices, not ratified by this reviewer PASS. D2-3 is owner-decided. This review grants no permission to enable switches or real/scientific runs.

## 4. New CODE finding E2RC2-CODE-B01 - caller-chosen authoritative gate evidence

Class: BLOCKER. Disposition: RECHECK. Always-review scope: process/orphan safety, registry release, result firewall.

Exact locations:
- src/methods/_common/contract_runner.py lines 96-112: run_contract_method accepts orphan_marker, data_root and methods_root, and uses them for the supposedly global orphan/installed gate checks.
- src/methods/_common/contract_publication.py lines 236-257 and 277-302: read_run accepts orphan_marker and data_root and passes them into the otherwise validated consumption path.
- src/methods/_common/contract_dispatch.py lines 47-80, 83-129: dispatch_gate, legacy_gate, variant_released and active_pins allow alternate registry or flag roots.
- src/coordinator_private/contract_coordinated_gate.py lines 19-23: the entry also forwards alternate roots.

Synthetic reproduction (see accompanying Python repro):
1. With the global unresolved-orphan marker present in a temporary fixture, run_contract_method with default marker refuses UNRESOLVED_ORPHAN_MARKER. The same function with orphan_marker set to a missing path completes SUCCESS, while the global marker remains present.
2. For a completed synthetic run and the same global marker, read_run using the default marker reports (False, UNRESOLVED_ORPHAN_MARKER); read_run with orphan_marker set to a missing path reports (True, CONSUMABLE) on the same frozen forecast. This directly defeats the requirement that the consumer establishes its own real gate evidence.
3. With the installed registry root set in a temporary fixture to FORMULA_OPEN, dispatch_gate refuses NOT_SUPPORTED; with a caller-provided data_root naming a different synthetic SUPPORTED registry, it admits the identical request.

These are API-level trust-boundary gaps, not an assertion of OS-level security against malicious Python code running in the same process. Test seams are legitimate, but the public normal-run / authoritative-consumption interfaces must not accept caller-selected authority evidence.

Required resolution: make the public run, dispatch and consumption APIs obtain the actual installed registry/method-flag roots and actual global unresolved-orphan marker themselves; remove caller-controlled locator overrides from those production APIs. If tests require isolated roots, provide a narrowly private test-only injection seam or temporarily patch fixed module-level source constants within the test harness. Do not create a CLI flag, environment override, generic gates_pass toggle or bypass. Preserve the no-status/no-kill and orphan refusal. Add independent negative tests demonstrating that normal public APIs cannot redirect the marker, registry or method flag root and that a genuine active marker and withdrawn/flagged variant always refuse. Recheck the changed APIs and all affected code/tests.

## 5. New CODE finding E2RC2-CODE-B02 - standalone API publishes coordinated SUCCESS

Class: BLOCKER. Disposition: RECHECK. Always-review scope: coordinated-science gate and failed-result firewall.

Exact locations: src/methods/_common/contract_runner.py lines 96-112; src/methods/_common/contract_publication.py lines 110-115, 179-195; src/coordinator_private/contract_coordinated_gate.py lines 19-28.

Synthetic reproduction: call run_contract_method(..., execution_path='COORDINATED') with a supported E_1 request and invented master. The standalone method API publishes a RUN_TERMINAL_RECORD_V1 with execution_path=COORDINATED, outcome=SUCCESS. The intended rejecting coordinated gate was never invoked. The read_run consumer correctly refuses the output with COORDINATED_EVIDENCE_NOT_AVAILABLE, limiting downstream impact, but creating the bogus successful coordinated run is itself outside CODE-2's declared scope.

Required resolution: the CODE-2 standalone execution API must refuse execution_path other than STANDALONE before creating a run folder or reading draw data. Do not permit a caller-supplied coordinated execution path through this shared runner. Future coordinated execution must be a separately authorised and independently reviewed interface. Add a negative test that the direct API refuses COORDINATED with no folder, no output and no SUCCESS D2; keep the downstream read_run rejection as defence in depth. Do not change the protected coordinator or science allowlist.

## 6. Independent R-2 test reproduction and boundaries

Environment: Linux, Python 3.13.5, NumPy 2.3.5, psutil 7.2.2. Only the supplied base snapshot and candidate repo_overlay were used. No real master or holdout datasets were available or accessed. The tests use synthetic/temp fixtures; no process kill or switch change was performed.

Test counts:
- Earlier accepted modules excluding the 10 reader-contract tests: 74 PASS, 0 skips.
- CODE-1 prefix test: 1 PASS, 0 skips.
- CODE-1 contract tests excluding six-worker T12: 52 PASS, 0 skips.
- CODE-2 tests.test_e2r_dispatch + tests.test_e2r_runner: 47 PASS, 0 skips.
- Total independently run: 174 PASS, 0 errors, 0 failures, 0 skips.

Not independently reproduced: 10 real-master-dependent reader tests, six-worker T12, 18/18 mutation suite, Windows run and the actual installation/committed state. The synthetic reproducer uses temp files and test mocks only; it deliberately exercises the current public keyword overrides, never the real orphan marker on disk.

The fact that 174 tests pass while the three independent negative probes demonstrate the above defects establishes a test-coverage gap. It does NOT establish success of the proposed installation.

## 7. REVIEWER-DECIDED - explicitly recorded

- E2RC2-RD-06: PASS the corrected R-3 design v0.1r1 unchanged, closing EX_039 B01/B02/C01/C02/C03/O01.
- E2RC2-RD-07: Support E_1 remaining revision 1 for this bounded new legacy gate, conditioned on the source diff containing only the proposed gate insertion and unchanged E_1 scientific calculation/goldens. The candidate satisfies this source-diff condition.
- E2RC2-RD-08: The condition for beginning the HIGH-tier CODE-2 review was met. Independent R-2 executed 174 selected synthetic/offline tests; T12 and ten real-master tests were not run.
- E2RC2-RD-09: Assign E2RC2-CODE-B01 BLOCKER/RECHECK; no caller-chosen orphan/registry/flag authority path in production interfaces.
- E2RC2-RD-10: Assign E2RC2-CODE-B02 BLOCKER/RECHECK; no coordinated SUCCESS publication via the standalone runner.
- E2RC2-RD-11: Do not recommend candidate v2 for owner installation. Require a narrowly corrected candidate, exact diff, updated hashes, new negative tests and focused independent RECHECK. The owner retains all decisions and execution authorisation.

No departure from existing owner-ratified science/safety/review rules is permitted or recommended. Reviewer dispositions concern always-review code and cannot be FIX AND PROCEED.

## 8. Next handback

Claude should prepare a corrected CODE-2 candidate and response matrix for the two blockers; preserve the design v0.1r1 unless the implementation fix actually requires a normative change. Include exact changed-file paths/hashes and revised suite counts. Both regression probes must fail against the corrected implementation's forbidden use and the legitimate paths must still PASS. Submit for focused HIGH-tier RECHECK. Do not rerun or relabel any genuine real-data experiments. No installation, run authorization, release, Git action, switch flip or holdout operation follows from this review.

End of review.
