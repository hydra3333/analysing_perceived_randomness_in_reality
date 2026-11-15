# OUTLANDISH_01 — Claude Review Point B Brief (Q4h v0.1)

**Date:** 16 November 2026 (Australia/Adelaide)  
**Sender:** ChatGPT, OUTLANDISH implementer; owner-mediated  
**Recipient:** Claude, independent OUTLANDISH technical/scientific reviewer  
**Status:** **Request for focused design/code review; not implementation authorisation or Q5 approval.**

## 1. Context and source of authority

The binding science is `GAIS/OUTLANDISH_01/OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md`. Current status is `GAIS/OUTLANDISH_01/OUTLANDISH_01_Living_Decisions_and_Progress.md` §14/§14.5. Claude's completed Review A memo is `GAIS/OUTLANDISH_01/REVIEW/OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md` with independently reproducible checks in the same `REVIEW/` directory.

Review A found no scientific defect in the shared Q3 v0.4 matcher/classifier or Q4d statistical arithmetic within the tested synthetic scope. It identified required **production-design** corrections F1–F4: (F1) six-constant REAL Holm cannot require NULL; (F2) historical code hashes are advisory, not a report-load gate; (F3) ordinary report load must not recalculate all statistics and permutations; (F4) primary permutations are fixed at 10,000, with a declared reproducible seed rule. Review A recommended building a small production path and **not refactoring** the older passing Q4a–Q4g synthetic suites.

**New Q4h v0.1 prototype:** six files under `GAIS/OUTLANDISH_01/` with prefix `OUTLANDISH_01_Q4h_`. They must be committed to GitHub before a repository-based review; if not yet committed, the owner can send `OUTLANDISH_01_Q4h_Minimal_Powerball_Test_v0_1.zip` directly. Review the exact source revision supplied, and identify its commit when available. This brief itself is optional working correspondence and not a new governance requirement.

## 2. Windows qualification evidence (owner-run)

From the owner's Windows Ryzen project virtual environment using the **actual installed Q3 v0.4 matcher and classifier**, not development stand-ins:

```text
Q4H POWERBALL SYNTHETIC GUARDS PASS: runs=0 reports=0 aggregates=0 guard-refusals=5 permutations-per-report=10000 production-scans=0 REAL-history-reads=0
Q4H POWERBALL SYNTHETIC INTEGRATION PASS: runs=6 reports=6 aggregates=1 guard-refusals=27 permutations-per-report=10000 production-scans=0 REAL-history-reads=0
```

Q4h generated six distinct tiny synthetic packed constants, used an isolated fabricated three-draw Powerball history, ran the Q3 packed streamer and Q3 classifier, generated six reports with 10,000 permutations each, and aggregated six REAL-like reports with no NULL inputs. It checked digest-bound ordinary report/aggregate loading, explicit statistical audit, refusal on output/source/history/receipt tampering, type/identity refusals, create-only behaviour, preserved INCOMPLETE runs, no permutation replay on ordinary loads, nonblocking code-hash changes, and replay after synthetic packed sources were removed. No REAL history, published G: constant or parent holdout was used. This is **synthetic qualification only**; a three-draw fixture does not measure full-history permutation runtime.

## 3. Compact design to review

| File | Responsibility |
|---|---|
| `OUTLANDISH_01_Q4h_Events_v0_1.py` | Strict canonical four-column raw-event loader; uses the existing Q3 classifier to validate order, identity, offset, roles and EOF. |
| `OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1.py` | TEST_REAL-only Powerball runner using Q4b receipt/history/root gates, Q3 v0.4 one-pass scanner/SHA, create-only INCOMPLETE to COMPLETE run manifest. |
| `OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1.py` | Q4d-derived categories, physical overlaps, transitions and **10,000** whole-draw permutations; compute once; ordinary load verifies hashes and identities; explicit optional audit recomputes; historical code hashes are advisory. |
| `OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1.py` | Fixed six-constant Holm from six TEST_REAL reports alone; records NULL comparison as optional/not run; ordinary replay verifies stored report summaries without re-running permutations. |
| `OUTLANDISH_01_Q4h_Powerball_Test_Qualification_v0_1.py` | Self-test and six-constant synthetic integration tests; no REAL CLI. |
| `OUTLANDISH_01_Q4h_Minimal_Powerball_Test_v0_1_README.md` | Boundary, commands and test coverage. |

Dependencies reused unchanged: Q3 packed matcher v0.4, Q3 classifier v0.1, Q4b source/history guards v0.1, and Q4d statistical core v0.1. Q4h's test harness reuses earlier fixture setup utilities; these are **not** intended dependencies of the future production entry point.

## 4. Requested Review B questions, in order

1. **Scientific correctness and F1–F4:** Does this proposed four-component shape faithfully preserve v0.2 semantics? Is REAL-only six-constant Holm independent of NULL? Are the 10,000 permutations genuinely fixed for qualified primary results, with N/A treated conservatively, and code hashes advisory rather than gating? Is ordinary load sufficiently cheap and digest/provenance-bound without reanalysis? Identify a concrete failure before suggesting additional protection.
2. **Production boundary and simple safety:** How should these TEST-only functions be connected to the already known, fixed Powerball production profile, existing receipts and G: root, while **remaining disabled until the owner's explicit Q5 authorisation**? Would a small dedicated entry-point wrapper be sufficient, rather than lifting each synthetic sandbox guard? Are the manifest COMPLETE and failure semantics sound?
3. **KISS:** Identify code and process we can *remove, avoid duplicating, or defer*. Do not migrate every Q4a–Q4g validator or manifest variant into production. Avoid registries, signing systems, repeated 5 GB reads, mandatory historical code-exact replay, new review gates or approval workflow. A minimal correct solution is the objective.
4. **Targeted remaining tests:** Which *few* tests remain necessary to justify the Powerball production wrapper? Review A suggested four synthetic guard-removal canaries (REAL/NULL root/type, history SHA, full-source digest, duplicate identity); determine whether each can be covered simply. Avoid additional broad test frameworks.
5. **Performance and data shape:** Q4h full event CSV is loaded in memory after streaming; Powerball is expected modest, but assess whether any obvious unbounded risk matters for the initial Powerball REAL workflow. Do not optimise optional NULL K=99 or Oz before they are in scope.

Please classify findings as **blocking correctness/safety**, **worthwhile KISS simplification**, **optional/deferred**, or **not warranted**, with file/line references and the smallest feasible remedy. A short findings memo is preferred. **Read-only review: no code changes by default.** If the existing design is suitable for a minimal production wrapper, say so rather than inventing more work.

## 5. Still open — owner decisions and unimplemented production work

- **No genuine Powerball REAL API/CLI exists in Q4h.** Q4h is test-only; do not infer permission to scan the six 5 GB published sources or to access `POWERBALL_preholdout_only.csv` through a production run.
- Proposed Powerball `P3_any` and Oz `O3_any` W→W+1 primary statistics remain owner-vetoable before qualified REAL science.
- Q4h uses **seed 271828** labelled *PROVISIONAL_TEST_ONLY*. A simple per-game reproducible seed convention must be agreed and recorded before genuine reports. The 10,000 permutation count itself is binding.
- The approved isolated modern-era Oz Lotto history, column roles, first draw and exclusive cutoff are still missing from the production adapter. Do not guess them or read the parent holdout.
- Optional NULL runner, NULL K parameter, and Oz production work are later steps; neither is necessary to aggregate six Powerball REAL reports.
- Production receipt preflight on actual G: files, qualification against production pathways, Review C, and owner Q5 approval are all outstanding.

## 6. Strict repository / communication boundary

**All review correspondence and any future approved code changes must stay within `GAIS/OUTLANDISH_01/` and subfolders.** In particular, do not modify, stage, overwrite, read for experimental input, or commit anything under parent `results/`, `source_data/`, `src/`, top-level `exchange/`, or the parent project's holdout. Reviewer correspondence may be relayed by the owner as a standalone Markdown file or saved in `GAIS/OUTLANDISH_01/REVIEW/`; there is no extra approval ledger, sequence registry or recovery document. Do not rewrite old evidence. Q5 remains blocked.

**Expected output:** a focused Review B findings memo, owner-relayed to ChatGPT. No additional review stage is implied unless a consequential issue is demonstrated.
