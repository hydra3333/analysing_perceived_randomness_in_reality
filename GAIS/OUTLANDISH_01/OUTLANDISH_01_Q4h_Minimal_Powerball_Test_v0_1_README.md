# OUTLANDISH_01 — Q4h minimal Powerball REAL-path-shaped prototype v0.1

**Scope:** `GAIS/OUTLANDISH_01/` only. **SYNTHETIC TEST ONLY** — not an authorised REAL scanner, not Q5, and not a change to ratified matching/reporting v0.2. The four small scientific/operational modules and one qualification harness in this package are *new* files; Q3 v0.4, classifier, Q4b and Q4d are unchanged. This is the first production-shaped Powerball implementation slice following Claude review point A, pending owner Windows qualification and subsequent reviewer point B.

## The deliberate minimal architecture

1. `OUTLANDISH_01_Q4h_Events_v0_1.py` — read the canonical four-column CSV, verify SHA-256, and use the existing Q3 classifier for semantic/duplicate/ordering/EOF checks; no new family matching algorithm.
2. `OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1.py` — fixed marked synthetic root and synthetic history, existing Q4b receipt/sample/history guards, Q3 v0.4 streamed matching and full-source hash **in the scan**, create-only TEST_REAL folder and one INCOMPLETE-to-COMPLETE run manifest. No production root/REAL entry point.
3. `OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1.py` — existing Q4d category/overlap/adjacent-draw/permutation logic. Exactly **10,000 whole-draw permutations**, fixed **provisional synthetic-only seed 271828**. Compute once on creation; ordinary digest-validated load **does not recalculate**; separate optional `audit_test_report` recalculates. Historical code hashes are recorded but a mismatch is **advisory**, not a load refusal.
4. `OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1.py` — six REAL-like reports alone give fixed six-constant Holm within Powerball; `null_comparison: NOT_RUN_OPTIONAL`. No NULL scans or compulsory NULL report inputs. Regular aggregate load verifies source reports and cheap Holm, not Monte Carlo.

This prototype deliberately does **not** refactor Q4a–Q4g synthetic evidence, add an approval ledger/registry/allowlist, re-read the packed BCD on report load, implement the optional NULL runner, or guess the Oz Lotto modern-era profile. The real production entry must be designed and reviewed separately. The recorded per-game seed must be an owner-visible decision before any REAL report. The proposed primary `P3_any` remains owner-vetoable.

## Windows CMD from the repository root

Extract the package into your repository root (paths already start `GAIS/OUTLANDISH_01/`), then run:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4h_Powerball_Test_Qualification_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4h_Powerball_Test_Qualification_v0_1.py" --run
```

Expected final lines:

```text
Q4H POWERBALL SYNTHETIC GUARDS PASS: runs=0 reports=0 aggregates=0 guard-refusals=5 permutations-per-report=10000 production-scans=0 REAL-history-reads=0
Q4H POWERBALL SYNTHETIC INTEGRATION PASS: runs=6 reports=6 aggregates=1 guard-refusals=27 permutations-per-report=10000 production-scans=0 REAL-history-reads=0
```

The qualification creates a marked `TemporaryDirectory` with six **tiny distinct** artificial BCD files/receipts and three fabricated Powerball draws; it uses the **actual installed Q3 v0.4 scanner and classifier**. It tests create-only run/report/aggregate output, incomplete crash refusal, event/receipt/history/report/aggregate tamper, cross-constant confusion, replay without BCD binaries, code-hash mismatch as nonblocking, optional explicit audit, and a sentinel proving ordinary load does not recompute permutations. It does not access `G:` production sources, any real history, parent files or parent holdout.

**Development-environment limitation:** Initial local rehearsal returned the expected two PASS lines using temporary, deliberately simplified stand-ins for Q3 matcher/classifier because those older source modules were unavailable in the assistant's local container. **Those stand-ins are NOT distributed in this package and are not evidence that the installed scanner integration passed.** The owner's Windows `--run` using the repository's real Q3 v0.4/classifier is the decisive qualification for this slice.

## Next stage

After owner Windows results, repair any actual integration issue. Evaluate architecture/KISS with Claude at agreed reviewer point B before adopting any production run interface. Production REAL source access and Q5 require their own separate owner authorisation. Keep all commits and review files strictly under `GAIS/OUTLANDISH_01/`; do not stage the parent project's unrelated uncommitted files.
