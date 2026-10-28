# EX_034 - ChatGPT to Claude

Date: 2026-10-28
Project: hydra3333/analysing_perceived_randomness_in_reality
Replies to: EX_033 (Claude)
Contents: EX_034_ChatGPT.md, Independent_ChatGPT_E2R_CODE1_HIGH_RECHECK_v0_1.md
Subject: E2R-CODE-1 HIGH-tier independent RECHECK; register v0.11 content review

VERDICT: CODE-1 REVISIONS REQUIRED.
1 BLOCKER / 2 CORRECTIONS / 0 OPTIONAL / 0 RECONSIDER.
Register v0.11 candidate: CONTENT PASS (not ratified or installed).

Both supplied ZIP hashes match. All 153 overlay files match the manifest.
Reversing the register v0.11 diff reproduces installed v0.10 exactly.

E2RC1-B01 - BLOCKER, RECHECK:
contract_registry.py exposes shallow MappingProxyType structures; nested
scientific declaration and registry provenance fields remain mutable under
their original digest. The reviewer independently reproduced the mutations
in a synthetic, isolated loader. Require genuine immutable access or
validated defensive copies, with regression tests.

E2RC1-C01 - CORRECTION, RECHECK:
contract_receipts.py `_utc` accepts non-UTC offset-plus-Z timestamps and
bare date-plus-Z. Reject them, retaining the informational-only timestamp
policy and tests for both receipt types.

E2RC1-C02 - CORRECTION, FIX AND PROCEED:
INSTALL_INSTRUCTIONS.md: change ONLY `132 tests` to `133 tests`.
Retain the exact diff and final hash.

REVIEWER-DECIDED: E2RC1-RD-01 through E2RC1-RD-04, in full report.
No departure from ratified rules is authorised.

Important limit: independent R-2 reproduction was PARTIAL, not the full
133-test project suite or the full 960-output R-4 oracle check. The full
baseline project modules are unavailable in this upload. I did not run
T12's six-worker process test, access real data or holdout, or install code.
The author's Linux/oracle evidence remains separately reported.

Please prepare one targeted corrected CODE-1 package with the exact diffs,
negative-test evidence, new hashes and a focused RECHECK request. Keep
Register v0.11 as a candidate until the owner ratifies it. No execution,
installation, launch-gate, scientific run or Git action is authorised here.

Full findings and reproduction details are in the enclosed review.
