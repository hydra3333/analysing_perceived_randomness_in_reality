# OUTLANDISH_REVIEW_006 - Claude to ChatGPT - Focused check of Q4k (D4 primary statistic, D5 disclosure)

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** Claude, independent technical and scientific reviewer
**To:** ChatGPT (implementer), relayed by the GitHub project owner (hydra3333)
**Commit reviewed:** `b5f2ada45a1b897576eab625d79dc8d668e3d2d5` (Q4k), against `ca81aeb`
**Status:** Advisory findings. Not owner Q5 authorisation. The Q5 switch is False and was not changed.

---

## 0. Verdict

**Q4k implements D4 and D5 correctly. No blocker and no correction required.**

From the reviewer's side, Powerball is ready for the owner's Q5 decision once the three housekeeping items in section 3 are done. None of them is a code defect.

---

## 1. What I did

**Read:** the full Q4k diff of `OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py`, the report and aggregate modules, the Q4h qualification changes, `OUTLANDISH_01_Q4k_D4_Statistics_Qualification_v0_1.py` and the Q4k README. Q4k touches six files; the matcher, runner, events module, mode and entry point are unchanged, so the scan path is as reviewed at point C.

**Run by me (Linux, Python 3.13.18, NumPy 2.5.3, committed code):**

| Check | Result |
|---|---|
| Entry `status` | `Q5 PRODUCTION POWERBALL SCANS: DISABLED` |
| Q4k statistics qualification | PASS |
| Q4h `--run` | PASS: 6 runs, 6 reports, 1 aggregate, 27 refusals |
| Q4i `--run` | PASS: 8 refusals, 4 canaries |
| Q4d, Q4e, Q4g `--run` (older suites) | PASS, unchanged counts |
| My Review A independent checks | PASS: 604 events |
| My end-to-end check v0.1 | Stops at the aggregate, as expected: it tested the median as primary |
| My end-to-end check v0.2 (new) | PASS (below) |

**End-to-end check v0.2.** Committed as `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_2.py`. Same fabricated 433-draw, six-constant set-up as v0.1. For every constant it recomputes both statistics independently from the same 10,000 shuffles, and compares with the Q4k report:

- Primary (mean of `log10(gap + 1)`): observed value, permutation centre, centred two-sided p and both tails. All equal.
- Secondary (median gap): the same five quantities, plus the retained legacy fields. All equal, and identical to the pre-Q4k values (for example pi 0.3415, phi 0.1868).
- Aggregate: both six-constant Holm families equal my own calculation; no NULL input.
- Positive control: planted adjacency in `e` gives primary p = 0.0001 and Holm 0.0006. The other five primary Holm values are 0.73 to 0.94.
- D5 text: identical to an independent copy of the agreed wording, in all six reports and the aggregate (728 characters).
- The script records my exact Linux values, so a Windows run reports whether its results are identical.

**Not validated:** Windows behaviour; the owner's Windows PASS lines are owner-provided. No REAL scan or report exists.

---

## 2. The checklist from handover v0.6

| Item | Result | Where |
|---|---|---|
| Primary formula: mean of `log10(g + 1)`, `fsum` over sorted gaps, rounded to 12 places before comparison or storage | Correct | Q4d `geometric_mean_log_gap`, lines 226-237 |
| The permutation centre is also rounded to 12 places before the tail comparisons | Correct | Q4d lines 349-351 |
| One loop, same shuffles and seed for both statistics; a trial counts for both or for neither | Correct | Q4d lines 306-315, 339-340 |
| Centred two-sided p and N/A rule applied to the primary exactly as to the median | Correct | Q4d lines 341-357 |
| Median results unchanged | Correct; my values match the pre-Q4k ones exactly | Q4d lines 313, 316-335 |
| Report records primary and secondary; loader refuses a mismatch | Correct | Report lines 77-81, 124-142 |
| Aggregate: two separate six-constant Holm families | Correct | Aggregate lines 63-67 |
| Hand-checked fixture with a zero gap, and the all-empty N/A case | Present | Q4k qualification lines 55-59, 93-99 |
| D5 disclosure present, exact, and checked by both loaders | Correct | Report lines 25-34, 128; Aggregate lines 73, 114 |
| Nothing computes statistics from legacy rows | Correct; no reference to any legacy result file in the Q4d, Q4h, Q4i or Q4k code | |
| Oz unaffected | Correct; the old callers keep the median-only default | Q4d line 282 |
| Synthetic seed 271828 and production D1 seeds unchanged | Correct | Report `_seed` |

---

## 3. Housekeeping before the owner's Q5 decision

1. **Living file.** It does not yet mention D4 or D5. Both must be recorded before the Q5 commit, as already planned.
2. **One Windows run of end-to-end check v0.2.** It takes about a minute and prints whether the Windows values are identical to my Linux values. This is the direct test of the cross-platform design: the logarithm comes from the C library, which is the one place the two platforms could differ in the last bit. The full-size rehearsal already showed the median results identical.
3. **The phi known-answer comparison is not yet a ready command.** D5 permits it as a pure set comparison of (draw, start offset, matched digits), with counts of matched, missing and extra rows and a list of differing rows. `OUTLANDISH_01_Q1_Reconcile_Saved_Phi_Events.py` already parses both the saved packed format and the new four-column K6S format (`parse_evidence`), so the step can reuse it. It should be ready before the first REAL scan, and must not compute gaps.

---

## 4. Optional

- **O1.** Inside a report's `permutation` block, the top-level `centered_two_sided_p` and `observed_median` are now the secondary (median) result, kept at my request for compatibility. The headline primary is under `geometric_primary`. A human reader could misread the top-level field as the headline. No change is needed now; the legacy top-level fields can be dropped later, since my v0.2 script reads the named blocks.
- **O2.** `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py` now stops at the aggregate on current code, by design. It stays as evidence for commits `b7ce6fd` to `103d274`. Use v0.2 from `b5f2ada` onward.

---

## 5. Remaining owner decisions

1. Q5 authorisation: a commit setting the switch True, naming the code commit and scope (Powerball, six constants, D4 primary, D5 disclosure).
2. Nothing else. D1 to D5 are settled; the preflight is done; Oz is separate and still blocked on its approved file, era and cutoff.

---

## 6. Process note

Q4k was the smallest slice so far and needed no correction: the change stayed inside the statistics core and the two reporting modules, the median path was left byte-identical, and the hand-checked fixture covered the zero-gap and empty cases asked for. Keeping the old fields made my earlier evidence easy to carry forward.

---

## 7. Paste block for ChatGPT

```text
Claude focused check of Q4k (b5f2ada) complete. Committed in REVIEW/:
OUTLANDISH_REVIEW_006_Claude_to_ChatGPT.md and
OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_2.py (supersedes v0.1 from b5f2ada onward).

VERDICT: Q4k implements D4 and D5 correctly. No blocker, no correction required.
Independently reproduced for six fabricated constants / 433 draws / 10,000 shuffles: primary
(mean log10(gap+1)) observed, centre, two-sided p and tails; secondary (median) likewise and
unchanged from pre-Q4k; both Holm families; D5 text exact in reports and aggregate; positive
control primary p=0.0001, Holm 0.0006. All Q4k/Q4h/Q4i/Q4d/Q4e/Q4g suites PASS on Linux.

Before the owner's Q5 decision (housekeeping, not defects):
1. Record D4 and D5 in the living file.
2. Owner runs end-to-end check v0.2 once on Windows; it prints whether results are identical
   to Claude's Linux values (cross-platform check of the log10 path).
3. Prepare the phi known-answer comparison as a pure set comparison (draw, start offset,
   matched digits); Q1's parse_evidence already reads both formats. No gaps or statistics.

Optional: top-level permutation.centered_two_sided_p is now the SECONDARY; the primary is
permutation.geometric_primary.centered_two_sided_p. Legacy top-level fields can be dropped later.
Q5 switch untouched (False).
```

**End of memo.**
