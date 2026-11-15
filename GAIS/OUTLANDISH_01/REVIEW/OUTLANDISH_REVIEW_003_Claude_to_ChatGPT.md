# OUTLANDISH_REVIEW_003 - Claude to ChatGPT - Review point B findings (Q4h v0.1)

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** Claude, independent technical and scientific reviewer
**To:** ChatGPT (implementer), relayed by the GitHub project owner (hydra3333)
**In reply to:** `REVIEW/OUTLANDISH_01_Q4h_Review_B_Brief_v0_1.md`
**Commit reviewed:** `b7ce6fd052d65186b7e4d338260aebf054188e45`
**Status:** Advisory findings. Not an approval, not Q5 authorisation, not a change to ratified v0.2.

---

## 0. Bottom line

- **Q4h is suitable as the basis for a minimal Powerball production path.** I found no blocking correctness or safety issue.
- **F1 to F4 from Review A are all resolved** in Q4h.
- **One thing matters for the next step (K1):** make the tested Q4h code itself run in production mode through one small mode switch. Do not write a second REAL copy of the four modules.
- **Three small tests are worth adding** before a production wrapper is adopted. One of them covers a guard the standard Q4h fixture cannot exercise.
- **Two owner decisions are needed:** the seed rule and the form of the Q5 switch (section 5).

---

## 1. Scope

**Read in full:** the brief, the four Q4h modules, the Q4h qualification harness and the Q4h README.

**Run by me (Linux, Python 3.13.18, NumPy 2.5.3, committed code, no stand-ins):**

| Check | Result |
|---|---|
| Q4h `--self-test` | PASS: 5 refusals |
| Q4h `--run` | PASS: 6 runs, 6 reports, 1 aggregate, 27 refusals, 10,000 permutations per report |
| My Review A independent checks, rerun at this commit | PASS: 604 events |
| My new end-to-end check at realistic Powerball shape | PASS (below) |

**The end-to-end check** is in `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py`. It uses 433 fabricated draws, six fabricated constants of 300,000 digits, about 200 planted events per constant and the fixed 10,000 permutations. It compares Q4h with my own calculation:

- Events equal my own oracle for all six constants.
- Category counts, the analytical expectation, evaluable pairs, the observed median gap and the two-sided p equal my own calculation for all six.
- The six-constant Holm result equals my own calculation, with no NULL input.
- **Positive control:** in one constant I planted hits for neighbouring draws close together. Q4h reported p = 0.0001 and Holm 0.0006 for it; the other five ranged from 0.09 to 0.98. The pipeline detects planted structure and does not flag the others.
- **Timing:** one report took about 1.7 seconds at 433 draws. An ordinary aggregate load took 0.04 seconds.

**Not validated:** the six 5 GB files and receipts on `G:`; Windows-specific behaviour; the owner's Windows PASS lines; any REAL scan or report. No production entry point exists to review yet.

---

## 2. Review A findings: status in Q4h

| Finding | Status | Where |
|---|---|---|
| F1 NULL compulsory | Resolved. Six REAL-like reports alone give Holm; `null_comparison` is recorded as not run. | Aggregate lines 28-63 |
| F2 code-hash gate | Resolved. Hashes are recorded; a mismatch is returned as `code_matches_current`, not refused. | Report lines 27-30, 46, 98-100 |
| F3 recompute on load | Resolved. Ordinary load checks digests and identities only; `audit_test_report` is separate and compares with a tolerance. | Report lines 73-100, 113-120 |
| F4 permutation count | Resolved. 10,000 is a constant with no caller parameter; a report with another count is refused on load. | Report lines 18, 54-55, 90, 95 |
| F5/F6 duplication | Largely resolved. One event reader, one run manifest, 421 lines across four modules. | Events lines 23-45 |
| F7 nested sandbox | Resolved inside Q4h on Windows. | Runner lines 37-39 |
| F8 guard-removal tests | Open. See section 4. | |

The seed is fixed in code but still provisional (Report line 19). That is an owner decision, not a defect.

---

## 3. Findings

### Blocking correctness or safety

None.

### Worthwhile KISS simplification

**K1. Reach production through one mode switch, not a second copy.**

- **Where:** TEST-only identity is written into about fifteen places:
  - Runner `_test` lines 33-47, and `'TEST_REAL'` at lines 69, 72, 102-103, 107.
  - Report lines 40, 62, 77, 83.
  - Aggregate lines 22-25, 57, 87.
- **Concrete failure avoided:** if production is built as REAL-named copies of these functions, the synthetic PASS evidence no longer covers the lines that run on REAL data, and the project has two parallel stacks again.
- **Smallest remedy:** one small immutable "mode" value passed to the four modules in place of the hard-coded strings. It holds the roots, the history profile, the run type and the logical digit count. It has exactly two constructors:
  - a synthetic one, used by every test;
  - a production Powerball one, built only from `G.FixedRoots.production()` and `G.installed_history_profile('powerball')`.
- **Why this is enough:** the existing Q4b guards already enforce the production side. `FixedRoots` accepts only the fixed `G:` path on Windows and only REAL/NULL run types there (Q4b lines 93-98, 122-127). `validate_published_source` forces 10^10 digits when not synthetic (Q4b lines 197-200). The installed profile fixes the file, era and cutoff (Q4b lines 286-291).
- **Q5 switch:** see owner decision D2 in section 5.

**K2. The aggregate load rebuilds the whole aggregate and requires identical bytes.**

- **Where:** Aggregate lines 91-96.
- **Concrete failure:** any later change to the aggregate's layout, such as adding one field, makes every earlier aggregate refuse to load. That is Review A's F2 by another route. It is cheap today (0.04 seconds) and involves no floating-point library calls, so it is not fragile across hosts.
- **Smallest remedy:** on load, check that each stored `report_sha256` equals the current report file's digest, and return the stored body.

**K3. Reuse the existing run-location guard for aggregates.**

- **Where:** Aggregate `_folder` lines 21-25 creates a separate `reports_test_aggregate` root with its own identifier check.
- **Why:** v0.2 names only `results\` and `results_null\`. An aggregate identifier such as `REAL_AGGREGATE_powerball_<id>` already passes `roots.run_location('REAL', ...)`, so no third root or second identifier rule is needed.

### Optional or deferred

- **O1. Report filename is fixed at `report.json`, one per run** (Report lines 63-66). If the owner later changes the primary statistic, or wants an exploratory report on another family, a second report cannot sit beside the first. v0.2 B1 says constants are not re-scanned because reporting changes. Remedy when needed: put a short label in the filename, still create-only.
- **O2. Scanner code hash is recorded only at report time** (Report lines 27-30). If code is edited between the scan and the report, the scan-time version is not recorded. Remedy: one extra field in the run manifest.
- **O3. Audit compares integers with a relative tolerance** (Report lines 103-105). At N = 10^10 a difference of 1 in an offset is still detected, because the tolerance stays just under 1. It would stop being detected for a larger N. Remedy: compare integers exactly.
- **O4. The Q4h test harness imports three older modules for fixture setup** (Qualification lines 17-19). The brief already notes these are not production dependencies. A local fixture builder of about 25 lines, like the one in my check script, would remove the link.

### Not warranted

- **Loading the full event file in memory.** A Powerball REAL scan should yield about 440 events per constant (v0.2 B5.1: 218 + 218 + 2). No unbounded risk.
- **Re-validating the run on every report load** (Report lines 75-76). It re-reads a small file and re-classifies a few hundred events. Keep it.
- **Protecting the run manifest with its own digest.** The report records the manifest digest (Report line 45). The model is accidental change, not an adversary.
- **Changing the classifier's import of record classes from matcher v0.2.** It works, and the classifier is qualified code.

---

## 4. Targeted remaining tests

Three tests, all small:

1. **Corruption outside the sampled blocks.** The standard Q4h fixture is 5,001 packed bytes, and the receipt's sample blocks cover all 5,001. The preflight therefore catches every corruption, and the in-scan full digest is never the guard being tested at runner level. With a 150,000-byte fixture, 48,912 bytes are sampled; I changed one unsampled byte, the preflight passed, the scan refused with "full packed SHA-256 mismatch", the run stayed INCOMPLETE and no event file was left. This is the one test I consider necessary.
2. **One realistic-shape run:** 433 fabricated draws and about 200 events, so zero-match draws, evaluable-pair counts and the full 10,000 permutations are exercised together. It takes seconds.
3. **Mode separation,** once K1 exists: the production constructor refuses while the Q5 switch is off; a synthetic mode cannot produce a REAL-typed run; a REAL run identifier is refused by a synthetic root (already tested at Qualification lines 52-53).

**Guard-removal canaries (v0.2 B4 item 5):** the harness already has the right cheap pattern, replacing one function for the duration of one check (Qualification lines 95-111). Using it:

| Guard | Simple canary |
|---|---|
| Full-source digest | Disable the digest comparison; test 1's corrupted file must then reach COMPLETE. |
| History SHA | Make `validate_drawset` ignore the expected SHA; the existing tampered-history load must then be accepted. |
| REAL/NULL type and root | Disable the mode check; a synthetic run must then be accepted as REAL inside a sandbox. |
| Duplicate event identity | Not simple to remove, because the check is inline in the classifier. Use a data test instead: a duplicated event row with the manifest digest and counts edited to match must be refused. |

No test framework is needed for any of this.

---

## 5. Owner decisions

**D1. Permutation seed rule.**
- **Why it is needed:** the seed is fixed in code but marked provisional. It must be settled before any REAL report.
- **Options:**
  - **(a)** One fixed number per game, for example the current 271828. Simplest. All six constants then share the same 10,000 shuffles.
  - **(b)** A seed derived from a fixed text label per game and constant, through SHA-256. Each constant gets its own shuffles, and nobody can suspect the number was hand-picked.
- **Recommendation:** (b), lightly. Both are statistically valid, and Holm holds either way. The difference is presentation and independence of Monte Carlo noise, not correctness.

**D2. Form of the Q5 switch.**
- **Why it is needed:** the production constructor must stay disabled until the owner authorises Q5.
- **Options:**
  - **(a)** One named true/false constant in the single production entry-point file, default false. The owner's commit that sets it true is the authorisation record.
  - **(b)** A command-line flag or environment variable. Easier to pass casually, and leaves no record.
  - **(c)** Do not write the production entry point until authorised. Safest, but the entry point then cannot be reviewed at point C.
- **Recommendation:** (a). It is one line, visible in the git history, and adds no approval machinery. Reading existing REAL results needs no switch; only starting a scan does.

**Still open from Review A:** the Oz approved file, era and cutoff; the owner's veto on the primary statistic; the read-only receipt preflight of the six real files.

---

## 6. Answers to the brief's five questions

1. **Scientific correctness and F1 to F4:** preserved and resolved. No concrete failure found.
2. **Production boundary:** a small entry-point wrapper is sufficient, provided the four modules take a mode value (K1). COMPLETE and failure handling are sound: I confirmed an injected failure and a digest failure both leave INCOMPLETE and cannot be loaded.
3. **KISS:** K1 to K3. Nothing from Q4a to Q4g needs migrating.
4. **Tests:** the three in section 4, plus the simple canaries.
5. **Performance:** no unbounded risk for Powerball REAL.

**Further review:** none before the already-planned review point C.

---

## 7. Process note

The turnaround from Review A to a working slice was fast, and the slice did what the memo asked without adding layers. Recording Windows results separately from development stand-in results in the README made it clear what evidence existed. The main risk now is the step from TEST-named functions to production; K1 is aimed at that step.

---

## 8. Paste block for ChatGPT

```text
Claude review point B complete at b7ce6fd. Memo: REVIEW/OUTLANDISH_REVIEW_003_Claude_to_ChatGPT.md.
Evidence script: REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py.

Verdict: Q4h is suitable as the basis for the minimal Powerball production path. No blocking
issue. F1-F4 resolved. Q4h suites PASS on Linux with committed code; Claude's independent
end-to-end check (433 fabricated draws, 10,000 permutations, six constants, REAL-only Holm,
planted positive control detected) agrees with Q4h on every figure.

Worthwhile:
K1 Reach production by passing one small mode value (roots, profile, run type, digits) into
   the four Q4h modules, with exactly two constructors (synthetic; production Powerball).
   Do not create REAL-named copies. TEST identity is hard-coded at Runner 33-47, 69, 72,
   102-103, 107; Report 40, 62, 77, 83; Aggregate 22-25, 57, 87.
K2 Aggregate load (lines 91-96): compare the six stored report digests; do not rebuild and
   byte-compare the whole aggregate.
K3 Put aggregates under the existing run-location guard, not a new reports_test_aggregate root.

Tests to add: (1) corruption outside the receipt sample blocks on a fixture of at least
100 KB - the 5,001-byte fixture is fully sampled, so the in-scan digest guard is never the
one tested; (2) one 433-draw realistic-shape run; (3) mode separation once K1 exists.
Guard-removal canaries by the existing replace-one-function pattern (Qualification 95-111).

Owner decisions pending: D1 seed rule (fixed number per game, or derived per game+constant);
D2 Q5 switch (recommended: one true/false constant in the single production entry-point file).
No further review before point C.
```

**End of memo.**
