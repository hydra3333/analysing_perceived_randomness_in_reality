# MHUP-A item 3 independent focused review - N5, N4, F2, and release safety

Date: 11 November 2026 (Adelaide)
Repository: hydra3333/analysing_perceived_randomness_in_reality
Checkpoint reviewed: 374409c0becfdf53aacb1100b7521f709725029d
Base identified by Claude: c48ac3c393d2eab30014e6200d427b76d90f47ac
Author: ChatGPT independent reviewer. Not an EX message. Read-only inspection; no code run, repository edits, test execution, or owner authorisations.

## 1. Disposition

- Item 3 tooling: PRELIMINARY PROGRESS ACCEPTED, not final package approval. The draft `released` and `staged` phases, barrier-order tests, and STOP-aware rehearsal are meaningful progress. The recorded 88 negative checks report 0 failed expectations. These were inspected as evidence, not independently reproduced by ChatGPT.
- N5: CONFIRMED BLOCKER to the ratified Appendix J step 10 as written. Recommend Option A IN PRINCIPLE, with a narrow owner-ratified design amendment and the safeguards below. Do not silently rewrite the ratified Appendix J rule.
- N4: ALREADY OWNER APPROVED in this ChatGPT conversation (two path-specific -text rules); Claude should implement and retest. No second decision needed.
- F2: RECHECK required for rows 8 and 9 and for integrating N5 into the T016 matrix, before a T016 go. Windows rehearsal and owner-run probes remain unauthorised.
- Return to Opus for the next authorised development/review preparation is reasonable. The owner's decision on N5 Option A is still needed.

## 2. N5: why Option A is preferable, and exact bounds

The reviewed design Appendix J step 10 assumes the whole suite can run with barriers U, E and P present because all tests patch barrier paths. The evidence shows otherwise: 21 modules encounter deliberate refusals from the live gate or E_1 development flag; no method-computation fault was established. The same candidate bytes in a barrier-free copy passed 570/570 (Linux Python 3.13). This is consistent with N5. The safe engineering choice is to keep the real tree barred and run the suite on a detached copy.

A short, explicitly reviewed amendment must replace BOTH (a) the Appendix J step-10 sentence and (b) the associated negative-oracle statement asserting that a suite without P must fail. The replacement oracle should prove the REAL installation root retains correct U/E/P throughout step 10; that the step-10 runner refuses if the real barriers are missing or wrong; and that only the isolated test root omits them. The original package gate/barrier refusal oracles still apply in their own synthetic tests. No released scientific or runtime method code needs to change for N5.

Minimum acceptance requirements for the shadow-suite runner:

1. Begin only after POST PASS on the just-installed live tree, with U held by this package and E/P present and intact. Recheck the live barriers before and after the suite, and on error. Never remove, edit, or temporarily hide live barriers to make tests pass.
2. Materialise an ordinary byte copy of the actual just-installed source/tests and the other test dependencies in a dedicated private temporary root. Prove the copied code and test files are byte-identical to the live tree and the validated package/base; no hard links, junctions, or symlinks back to the live tree. All test imports, subprocesses and relative output paths must resolve to the shadow root (not the live installation). Show this with one focused negative test.
3. Supply only the development data the accepted suite needs, within the already-approved test-data rules. Do not casually duplicate holdout or prospective records. Treat any data written to the shadow as disposable; no data publication, Git push, or real science mode. The current ad hoc `N5_shadow_copy_adhoc.py` copies all tracked paths, including potentially protected results and source_data, so it is proof of feasibility, NOT a finished safety-reviewed data-selection policy.
4. A failed shadow copy, provenance check, test, or live-barrier check is a genuine step-10 STOP: no step 11, no record/commit/release, and E/P/U stay installed. Temp cleanup is bounded and must not affect live paths, even on STOP.
5. Rehearse positive LF and core.autocrlf=true paths including step 10, plus missing/foreign live P, a changed shadow code file, accidental test-root escape and failed-suite negatives. The full 570-test suite must pass after N4. An isolated 570/570 in a shadow copy alone is NOT proof of a complete install.

This is a functional simplification, not a request for more permanent hashes or registers. Reuse the current manifest/verifier checks rather than inventing duplicate administrative machinery.

## 3. N4 (already approved)

The owner has approved these exact `.gitattributes` additions to the DRAFT package:

    src/package_tools/process_check.py -text
    tests/fixtures/results_master_v0_1_reference.py.txt -text

The fresh autocrlf clone previously failed two specific byte-sensitive tests (568/570). The change should remain narrowly scoped; retest a genuinely fresh autocrlf clone and the two target tests, and rebuild all package counts/hashes. Do not treat prior LF-only 570/570 as evidence for N4.

## 4. F2/T016 matrix: corrections required before review and owner go

- Row 6 Windows real Python/venv inventory and row 7 scratch planted-orphan negative are appropriate proposed oracles, provided the harness and its scope are reviewed and the real venv is not changed.
- Row 8 incorrectly claims that `process_check.py check-no-runs --install` "opens no data file." The actual `process_check.py` (in exchange/CLAUDE_WEB_TOOLS/mhupa/slice2_new/src/package_tools/) calls `unfinished_weekly_set` for roster-changing installs and may read weekly sessions' attempts JSONL and the forecast ledger under `results/real/weekly/`. It also checks session and updater locks. Correct the data-access statement and identify exactly what the owner-run command may read. Its output should be value-free.
- Row 9's proposed `POC_Coordinator_Probe.py --case=sleep-timeout` is genuinely an engineering-only sleep, but it creates status and result files under the REAL repository's `transitory_data/poc_runs` and is therefore not a read-only check. Before approving this owner-run procedure, require exact Windows commands, a fresh run identifier, a no-termination guarantee, a documented successful natural exit, the state of process/orphan safeguards and whether remaining synthetic records are harmless. Verify that `check-no-runs` actually lists the worker's PID and creation time while it is alive. Neither the runner nor Claude Code may launch it under current v0.4 restrictions. Do not replace the probe with a bare sleeper without design review.
- N5 changes row 2 versus row 3: a separate full-suite run on a clone with the permitted development master is useful but not an end-to-end step-10 rehearsal in the synthetic, data-free clone. State precisely what evidence each route supplies and whether the amended Appendix J still requires an additional live end-to-end owner rehearsal.
- Route A remains recommended: focused review and owner installation of rulebook v0.5 before separately authorised T016, not the reverse. The prior R-020(g) owner exception remains narrow and T016-only.

## 5. Cold-read findings: prioritise functional safety rather than paperwork

Two operational checks merit focused correction before final release:

A. `install_records.py release-record` checks P absence, the committed install record, sessions and unfinished sets, but does not verify U held by the correct package or E absent before creating the permanent create-only release record. The later RELEASED verifier checks these, but cannot undo publication. Add or propose a narrowly scoped prepublication guard and dedicated negatives, or present an equally safe reviewed argument. This is a genuine barrier-order/safety concern, not administrative enhancement.

B. Appendix J permits a further fix/revert commit after step 13 or step 17 STOP, whereas the new `released` proof expects precisely the package commit followed immediately by the release-record commit. Do not paper over this: give a reviewed STOP/recovery branch (possibly abandon and rebuild rather than continue) that preserves barriers, immutable evidence and commit identity. A recovery is not automatically authorised by the ordinary procedure.

Other cold-read observations: a few Python tracebacks rather than standard STOP lines should still give an unambiguous nonzero STOP; `post_pass_utc` is currently the step-12 record time, not the literal moment POST passed, so clarify its label/semantics rather than add another record. These are lower priority than A/B and N5.

## 6. Recommended next owner decisions and scope

1. Approve N5 Option A IN PRINCIPLE only, subject to the narrow Appendix J/negative-oracle amendment, isolation and STOP tests in section 2, and later independent reviewer RECHECK. No production code changes or weakening of P/E/U permitted for the solution.
2. N4 was already approved: simply carry it into the next draft and retest.
3. Defer approval of F2 rows 8-9 and T016 until the exact task and owner-run commands are reviewed. Do not authorise real Windows actions yet.
4. Claude can prepare the revised item-3 package/tools and the Route A amendment on Opus, but freezing final evidence, running T016, changing rulebook/settings, and installing remain separate gates under the existing process.

References: GitHub `exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/ITEM_3_CHECKPOINT_2026_11_11.md`, `evidence_2026_11_11/N5_*`, `evidence_2026_11_11/PRELIMINARY_negatives_88_py313.txt`, `src/methods/POC_Coordinator_Probe.py`, `exchange/CLAUDE_WEB_TOOLS/mhupa/slice2_new/src/package_tools/process_check.py`, `install_records.py`, and ratified `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r6.md` Appendix J.

No EX number consumed. No GitHub writes, tests or owner-run activities performed by ChatGPT.
