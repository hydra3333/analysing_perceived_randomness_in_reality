# CHECKPOINT - MHUP-A slice 2, 5 November 2026

State: candidate v1r1 sent to the reviewer as EX_149 (exchange/EX_149_Claude/, exchange/EX_149_Claude.zip), answering
EX_148. Evidence: 569 tests on Python 3.13 and 3.15 (SUITE PASS), 99 mutants (85 caught, 14 equivalent with reasons,
0 survived), plus the after-run re-check of test_mhupa_mode_h and mutant [54]. Windows: TASK_T021 (v1r1) is in the inbox
for the owner. Amendment A1 (the whole score ledger published once; the corrective run deferred to MHUP-B) awaits the
reviewer's review and then the owner's final approval (reminder R-021).

Next: read EX_150 when the owner relays it, and the owner's REPORT_T021. If RECHECK: build from these tools
(build_dev_slice2.sh BASE DEV TOOLS 2026-11-04 over a git archive of 2061055), fix, run new mutants alone first, then one
full chain. If PASS: the integrated MHUP-A install package (installer, verifier, LF/CRLF rehearsals, T016), with E_1 r3's
effective_date set to the package's preparation date (C01) and the package manifest's release_entries naming E_1 r3 (R-020).
