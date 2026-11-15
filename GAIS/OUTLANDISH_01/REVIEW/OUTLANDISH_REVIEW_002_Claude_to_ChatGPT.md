# OUTLANDISH_REVIEW_002 - Claude to ChatGPT - Review point A findings

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** Claude, independent technical and scientific reviewer (read-only)
**To:** ChatGPT (implementer), relayed by the GitHub project owner (hydra3333)
**In reply to:** `OUTLANDISH_01_Claude_Reviewer_Brief_2026-11-16_v0_1.md`
**Status:** Advisory findings. Not a decision document, not an approval, not a change to ratified v0.2.

---

## 0. Bottom line

- **The scientific core is correct as far as I could test it.** Matching, classification, expectations, the tie rule, the permutation test, the two-sided p and Holm all agree with ratified v0.2 and with my own independent re-implementations. I found no scientific defect.
- **The over-administration concern is justified, and it sits in Q4e and Q4g.** Three behaviours there should not be carried into production: NULL reports are compulsory, old reports refuse to open after any code edit, and every open recomputes the whole analysis.
- **Nothing committed can run on REAL data,** so nothing is a blocker today. Findings F1 to F4 are must-fix before a production runner is adopted.
- **The duplicated validators are real but harmless.** They should be removed by building the production path small, not by refactoring the synthetic suites.

---

## 1. Snapshot and scope

**Commit reviewed:** `f42ae71ad340bb7db7b5808ac59ebc4f2009bc67`. At review time `main` was at the same commit.

**Checkout:** limited to `GAIS/OUTLANDISH_01/`. The repository's top-level files were placed on disk by the checkout but were not opened.

**Read in full:**

- `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md`
- `OUTLANDISH_01_Living_Decisions_and_Progress.md`
- `OUTLANDISH_01_Q3_Packed_Matcher_v0_4.py`
- `OUTLANDISH_01_Q3_Event_Classifier_v0_1.py`
- `OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1.py`
- `OUTLANDISH_01_Q4_Fixture_Run_Guards_v0_1.py` (Q4a)
- `OUTLANDISH_01_Q4_Published_Source_Guards_v0_1.py` (Q4b)
- `OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1.py`
- `OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py`
- `OUTLANDISH_01_Q4e_Synthetic_Report_Bundle_v0_1.py`
- `OUTLANDISH_01_Q4g_Verified_Synthetic_Aggregate_v0_1.py`

**Read in part, for one question each:**

- `OUTLANDISH_WSL/wsl_format.py` and `wsl_convert.py` (receipt fields and sample plan)
- `OUTLANDISH_01_Operational_Handover_2026-11-14_v0_8.md` section 1 (the six packed filenames)
- The Q4e and Q4g README files (stated rationale)

**What I ran (Linux, Python 3.13.18, NumPy 2.5.3, the committed code, no stand-ins):**

| Check | Result |
|---|---|
| Q4a fixture guards `--run` | PASS: 4 runs, 53 refusals, 51 regressions |
| Q4b published-source `--run` | PASS: 70 refusals |
| Q4c processing `--run` | PASS: 4 runs, 26 refusals |
| Q4d statistics `--run` | PASS: 1,025 hand checks, 13 refusals |
| Q4e reporting `--run` | PASS: 4 reports, 39 refusals |
| Q4f matrix `--run` | PASS: 24 runs, 24 reports, 92 refusals |
| Q4g aggregate `--run` | PASS: 2 aggregates, 23 refusals |
| My own brute-force oracle against matcher v0.4 and the classifier | PASS: 60 random planted cases, both games, 6 chunk sizes each, 604 events |
| My own re-implementation of the Q4d arithmetic | PASS (details in section 2.1) |
| Q4b drawset gate on the committed `POWERBALL_preholdout_only.csv` | Accepted: 433 rows, draws 1144 to 1576 |

The Q4b count is 70 here against 69 reported on Windows. The brief says one symlink test can be skipped on Windows, which accounts for the difference.

**What I did not validate:**

- The six 5 GB packed files and their receipts on `G:`. I have never seen them.
- Any Windows-specific behaviour (junction checks, `os.replace`, the fixed `G:` root).
- The owner's Windows PASS lines. They are owner-provided results, not verified by me.
- A REAL scan, a REAL report or a 10,000-permutation run on real events. None exists.
- Any Oz Lotto REAL profile. None exists.
- Q1 and Q2 material and matcher versions v0.1 to v0.3. Not re-examined.
- The internals of the qualification harnesses. I ran them; I did not audit how each test is built.

---

## 2. Findings, highest priority first

### 2.1 What I checked and found correct

These are the brief's section 5 hypotheses 1, 6, 7 and 8.

| Item | Where | Verdict |
|---|---|---|
| Full-file SHA-256 computed in the scan's own read | Matcher v0.4 `_scan_core` lines 319-331 and 424-430 | Correct. Each byte is hashed once; lookahead bytes are not double-counted. |
| No separate 5 GB hash pass | Q4b `validate_published_source` lines 182-253 | Correct. Preflight reads 12 samples of 4,096 bytes only. |
| Receipt fields, filename stems and sample plan match the converter | Q4b lines 32-35 and 149-161 against `wsl_format.py` lines 23-24 and 58-69 | Identical. |
| Per-family end-of-file eligibility, odd starts, pad nibble | Matcher v0.4 lines 333-347 | Correct, including prefix scans. |
| Role rules (PB may equal a main; P2 seventh field 1 to 35; Oz supplementary found against the draw) | Matcher v0.4 lines 363-423; classifier `_one` lines 90-181 | Correct. |
| Duplicate or unsorted event refused at write time | Matcher v0.4 `emit` lines 306-313 | Correct. |
| O2 nesting: drawn-subsequence within supplementary-last within any-slot | Classifier lines 157-174 | Correct. |
| Same-draw overlaps from real interval intersection | Classifier lines 224-267; Q4d lines 168-194 | Correct against brute force. |
| Sequences per draw and expectations | Q4d `VIEW_RULES` lines 28-52; line 148 | Match v0.2 B5.1: P1 any 2.18, P2 any 218.23, P3 any 218.23, P3 subsequence 0.3031. |
| Conditional q values | Q4d line 154 | 1/5040, 1/720, 1/7, 1/720 as in v0.2 B5.2. |
| Signed tie order `(abs(b-a), b-a, a, b)` | Q4d `closest_gap` lines 197-214 | Correct against brute force on 20,000 random cases. |
| Zero-match draws kept in the series and in every permutation | Q4d lines 234 and 275-276 | Correct. |
| Undefined permutations excluded and counted; all-empty gives N/A | Q4d lines 279-294 | Correct. |
| Two-sided p, centred on the median of valid permuted medians, `(1+b)/(R_valid+1)` | Q4d lines 296-301 | Matches v0.2 B5.4 exactly. |
| Holm over exactly six named constants in one game | Q4d `holm_six_constants` lines 305-322 | Correct. See section 4 for the N/A convention. |
| Decoy tails `(1+count)/(K+1)`, summary counts only | Q4d lines 325-335 | Correct. |
| Powerball era and cutoff fixed in code, IDs checked before outcomes are parsed | Q4b lines 286-291 and 349-358 | Correct. |
| REAL Oz profile blocked, not invented | Q4b lines 300-301 | Correct. |
| Create-only run folders; INCOMPLETE until verified | Q4b lines 137-146; Q4c lines 307-348 | Correct. |
| A test sandbox cannot be passed off as the REAL root | Q4b `FixedRoots` lines 81-98 and 122-135 | Correct. One loose end is F7. |
| No path leaves the OUTLANDISH tree | All Q3/Q4 modules | Correct. The only fixed path outside a sandbox is the in-tree Powerball file. |
| No multi-gigabyte intermediate | Matcher streaming writer lines 109-152 | Correct. Events are written as found. |

### F1. Q4g cannot aggregate REAL reports without NULL reports

- **Severity:** IMPORTANT. It becomes a blocker if carried into the production aggregator.
- **Type:** binding-spec conflict.
- **Where:** `OUTLANDISH_01_Q4g_Verified_Synthetic_Aggregate_v0_1.py`
  - `_validate_inputs` lines 77-79: both rosters must hold exactly six constants.
  - `compute_verified_test_game_aggregate` lines 133-134, 149-154 and 161: a NULL report is loaded and compared for every constant.
  - Line 187: a common decoy K is required.
- **Why:** v0.2 B5.3 calls decoys a complementary check. B7 Q5 says optional separate NULL runs follow the REAL scans. The six-constant Holm result needs only the six REAL p-values.
- **Example:** `compute_verified_test_game_aggregate(roots, game, real_runs, {})` raises "exact six named constants required in each typed TEST roster".
- **Smallest fix:** make `null_runs` optional. When it is absent, compute Holm from the REAL reports and record `null_comparison: NOT_RUN`. When it is present, add the decoy block as now.

### F2. Reports and aggregates refuse to open after any code edit

- **Severity:** IMPORTANT.
- **Type:** operational integrity, and KISS simplification.
- **Where:**
  - Q4e `load_verified_synthetic_report` lines 256-257.
  - Q4g `load_verified_test_game_aggregate` lines 256-257.
  - The hashed list is Q4e `CODE_FILES` lines 23-31 plus the Q4g file.
- **Why:**
  - Any byte change to any of eight files makes every earlier report and aggregate unreadable. A comment fix or a line-ending change is enough.
  - The gate is also incomplete as a guarantee. It does not cover `OUTLANDISH_01_Q3_Packed_Matcher_v0_2.py`, which the classifier imports (classifier line 17), or the Python and NumPy versions.
  - v0.2 B3 asks for "scanner code/version" as run metadata. It does not ask for a gate.
- **Example (by inspection, not executed):** change one comment in `OUTLANDISH_01_Q4d_Statistical_Core_v0_1.py`; the load raises "executing implementation differs from report provenance".
- **Smallest fix:** keep writing `implementation_sha256` into the manifest. Delete the two comparisons. Have the loader return a `code_matches_current` true/false value for display.

### F3. Every open recomputes the whole analysis and demands byte-identical output

- **Severity:** IMPORTANT.
- **Type:** operational integrity, and KISS simplification.
- **Where:**
  - Q4e `load_verified_synthetic_report` lines 259-265: full recomputation, then byte comparison with the stored report.
  - Q4e `create_synthetic_report` lines 215 and 232-234: the analysis runs twice at creation.
  - Q4g `create_verified_test_game_aggregate` lines 221 and 237-239: the aggregate is computed twice, and each computation reloads all twelve reports.
  - Q4g `load_verified_test_game_aggregate` line 260: recomputed again on every open.
- **Measured cost of one 10,000-permutation test** (my Linux sandbox, one core; the owner's hosts will differ):

  | Case | Events | Time |
  |---|---|---|
  | Powerball K6S, 433 draws | about 217 | about 2 seconds |
  | Oz K6, illustrative 200 draws | about 10,000 | about 61 seconds |
  | Oz K6, illustrative 250 draws | about 12,500 | about 75 seconds |

  The Oz draw counts are illustrative only. The real Oz era is unconfirmed.
- **How often it runs:** building one six-constant game aggregate from nothing runs the REAL analysis 24 times where 6 are needed. Each later open of the aggregate runs it 6 times. Each open of one report runs it once.
- **Why it matters:** the compute cost is minutes, not hours, so cost alone is not the main objection. The main objection is fragility:
  - Byte-identical replay depends on floating-point results from `exp`, `log` and `log1p` (Q4d lines 118-124) being identical on every host and C runtime. That is not guaranteed between the Ryzen and the i5. I did not demonstrate a mismatch.
  - It depends on `random.Random.shuffle` producing the same sequence in every future Python. Python does not promise that. It was identical on 3.11, 3.12 and 3.13 when I tested.
  - A stored report whose inputs are intact could therefore become unreadable for reasons unrelated to its correctness.
- **Smallest fix:**
  - Ordinary load: check the stored report SHA against its manifest, and the raw-event, drawset and run-manifest SHAs against the recorded provenance. No recomputation.
  - Add one explicit `audit_report()` that recomputes and reports differences. Compare counts exactly and floats within a small tolerance.
  - At creation, replace the second analysis with a re-hash of the inputs.

### F4. The permutation count and seed are caller-supplied, with a default of 64

- **Severity:** IMPORTANT. The fix is a few lines.
- **Type:** scientific correctness, against v0.2 B5.4.
- **Where:**
  - Q4e `analyse_verified_synthetic_run` lines 113-114 and 121-123: any count from 1 to 10,000, default 64, any seed.
  - Q4e `create_synthetic_report` lines 209-210: the same defaults.
  - Q4g lines 158 and 187-190: checks only that the six reports used the same count, not that it was 10,000.
- **Why:** v0.2 fixes the primary test at 10,000 permutations. With the default, a primary p-value would have a resolution of 1/65 and would still aggregate cleanly.
- **Smallest fix:** in the production reporter, make 10,000 a named constant and fix the seed rule in code before any REAL report. The production aggregator refuses, or labels as exploratory, any report with a different count.

### F5. The same checks are implemented several times

- **Severity:** MINOR for correctness. IMPORTANT as the KISS item that should shape the next slice.
- **Type:** KISS simplification.
- **Inventory:**

  | Job | Implementations |
  |---|---|
  | Event validation (order, duplicate identity, text digits, end bound) | Matcher `emit` lines 306-313; smoke `read_events` lines 42-92; classifier `classify_events` lines 184-221; Q4d `_events` lines 63-87 |
  | Draw-record validation | Matcher lines 177-234; classifier lines 50-83; Q4a `_draws` lines 181-216; Q4b `validate_drawset` lines 323-374; Q4c `_read_decoys` lines 106-135 |
  | Receipt checks | Q4a lines 148-178 and 401-414; Q4b lines 182-253; Q4c lines 195-207 |
  | Same-draw overlap sweep | Classifier lines 224-267; Q4d lines 168-194 |
  | Sandbox and path guards | Q4a lines 64-96; Q4b lines 57-146 (two different marker schemes) |
  | Manifest formats | Q4a run, Q4c run, Q4e report, Q4g aggregate: four formats, four copies of the INCOMPLETE to COMPLETE code |
  | NULL identifier rewrite | Q4a lines 233-250; Q4c lines 138-155 |
  | Record conversion between matcher v0.2 and v0.4 classes | Q4a lines 388-396; Q4c lines 185-190; Q4e lines 100-109 |

- **Also:** Q4a (`OUTLANDISH_01_Q4_Fixture_Run_Guards_v0_1.py`) is imported only by its own test. Q4c re-implements it on top of Q4b.
- **Why it is not a defect:** every copy I tested gives the right answer. The cost is maintenance and reading effort.
- **Smallest fix:** do not refactor the synthetic slices. Build the production path from one copy of each job, as in section 5, and keep the existing suites as regression evidence.

### F6. Production-relevant code imports from a test aid and a superseded matcher

- **Severity:** MINOR.
- **Type:** KISS simplification.
- **Where:**
  - The only event-file reader is `read_events` in `OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1.py`. Its own docstring (line 44) calls it an example, not an authorised run reader.
  - The classifier takes its record classes from `OUTLANDISH_01_Q3_Packed_Matcher_v0_2.py` (line 17). The scanner is v0.4. That forces the three conversions listed in F5.
- **Smallest fix:** one small module holding the record classes and the event read and write functions. The classifier and matcher import from it.

### F7. The sandbox check does not do what its comment says

- **Severity:** MINOR.
- **Type:** operational integrity.
- **Where:** Q4b `FixedRoots.__post_init__` lines 84-91.
- **Why:** the comment says a test root must not be nested inside the installed production results or digits folders. The code checks only the name prefix and marker file. A marked sandbox created under the production tree would be accepted. I see no way for its output to be read as REAL, because REAL run identifiers must start with `REAL_`.
- **Smallest fix:** refuse a synthetic base that lies under the fixed `G:` root. About three lines.

### F8. Guard-removal mutation tests are missing from the Q4 suites

- **Severity:** MINOR.
- **Type:** binding-spec conflict (a gap, not a contradiction).
- **Where:** v0.2 B4 item 5 and B7 Q4 ask that each important guard be deliberately disabled to prove a test then fails. The Q4 suites mutate data files only.
- **Smallest fix:** after the production path exists, add this for four guards: REAL/NULL type and root, drawset SHA, full-source digest, duplicate event identity. Not before, because consolidation will change the guards.

### F9. The NULL path will not scale to K=99 as written

- **Severity:** OPTIONAL. It matters only when a production NULL runner is built.
- **Type:** operational integrity.
- **Where:**
  - Q4e lines 175-178 re-scan the full event list once per decoy history.
  - Q4c `_verified_events` lines 158-192 hold several copies of every event in memory.
- **Why:** an Oz history yields roughly 61 events per draw (v0.2 B5.1 figures). With K=99 that is over a million events for a history of a few hundred draws.
- **Smallest fix:** group events by decoy in one pass. Measure memory at K=19 before choosing K=99.

### F10. The permutation loop re-sorts its inputs on every call

- **Severity:** OPTIONAL.
- **Type:** KISS simplification.
- **Where:** Q4d `closest_gap` lines 199-204, called from `_transition_summaries` line 219.
- **Why:** the sets are already sorted and validated. Not worth changing once F3 is fixed, because the test then runs once per report.

---

## 3. KISS verdict

**Essential; keep as is:**

- The once-through full-file digest and its comparison with the receipt.
- The receipt sample preflight.
- The fixed Powerball profile with its exact era, cutoff and drawset SHA.
- Typed REAL and NULL separation with separate result roots.
- Create-only run folders with INCOMPLETE until verified.
- The raw-event SHA in the run manifest.
- The duplicate-identity check in the event writer.
- All of Q4d.

**Duplicated; collapse to one copy in the production path:** everything in the F5 table.

**Expensive or fragile; move to an explicit audit action:** recomputation on load (F3).

**Obstructive; remove:** the code-hash gate (F2) and compulsory NULL reports (F1).

**Answers to the brief's section 5 hypotheses:**

| # | Hypothesis | Answer |
|---|---|---|
| 1 | Full-source hash in the scan's own read | Confirmed correct. |
| 2 | Code hashes block replay | Confirmed. See F2. |
| 3 | Recomputation on read | Confirmed. See F3. The cost is minutes; the fragility is the larger problem. |
| 4 | REAL and NULL coupled | Confirmed. See F1. |
| 5 | Too many wrappers | Confirmed. See F5 and F6. |
| 6 | Hard production gates | Sound for Powerball. Oz is correctly blocked. One loose end, F7. |
| 7 | Statistical correctness | No discrepancy found. One unpinned parameter, F4. |
| 8 | Performance feasibility | The REAL path is feasible. The NULL path at K=99 is unmeasured, F9. |

---

## 4. Missing factual inputs and owner choices

1. **Oz Lotto approved isolated file, its column layout, era start and cutoff.** Unknown to me and not in the code. Oz REAL work is blocked until the owner supplies them. I have not guessed them.
2. **The primary W->W+1 statistic** (P3_any for Powerball, O3_any for Oz). Still owner-vetoable before any qualified REAL scan. Nothing I found argues for or against it.
3. **The permutation seed rule.** v0.2 does not fix one. It should be fixed in code before the first REAL report (F4). This is a small owner-visible choice.
4. **Holm with an undefined p-value.** The code keeps the family at six and treats an N/A constant as p = 1 when adjusting the others (Q4d lines 315-321). That is conservative and consistent with v0.2's rule against shrinking the family. v0.2 does not state it, so the owner should know it is the convention.
5. **The six real receipts have never been read by this code.** A read-only preflight on the Ryzen would settle whether the Q4b guard accepts all six, including the two made by the native Windows converter copy. It reads 12 samples of 4,096 bytes per file and writes nothing. It touches the production digits folder, so it needs the owner's explicit go-ahead.
6. **NULL K (19 or 99).** Needed only when a NULL run is planned.

---

## 5. Recommended next code slice

**One slice: the minimal production REAL path for Powerball, built small.**

1. One events module: record classes, event read and write, one validator (F5, F6).
2. One REAL runner: the Q4b guards, matcher v0.4, one run manifest.
3. One reporter: the classifier and Q4d; store the report and its SHA; ordinary load by digest; a separate explicit audit function (F2, F3); 10,000 permutations and the seed rule fixed in code (F4).
4. One aggregator: six-constant Holm from REAL reports alone, with an optional NULL comparison block (F1).

Keep the existing synthetic suites untouched as regression evidence. Leave the NULL runner and Oz until their inputs exist.

**Must-fix before the production runner is adopted:** F1, F2, F3, F4.
**Nice to have:** F5 to F8, largely delivered by building the slice as above.
**Only when relevant:** F9, F10.

**Second review:** no extra review is justified. The already-planned review point B (before the production run interface is adopted) is the right place to check this slice.

---

## 6. Process note

The brief was specific and its hypotheses were accurate, which made the review quick to aim. The Q3 and Q4d code is small and readable, and it tested clean. The Q4e and Q4g layers follow the pattern the owner suspected: each slice added its own verification of everything beneath it. The living file should be brought up to date for Q4b to Q4g before the next slice, so the repository record matches this commit.

---

## 7. Paste block for ChatGPT

```text
Claude review point A complete at f42ae71 (main unchanged). Memo: OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md.

No scientific defect found. Matcher v0.4, classifier and all Q4d arithmetic agree with v0.2
and with Claude's independent brute-force checks. All seven Q4 suites PASS on Linux
(Python 3.13.18, NumPy 2.5.3) using the committed code.

Must-fix before a production runner is adopted:
F1 Q4g requires six NULL reports (lines 77-79, 133-134, 149-161). Conflicts with v0.2 B5.3/B7 Q5.
   Make null_runs optional; Holm needs only the six REAL p-values.
F2 Q4e/Q4g refuse to load if any code file hash differs (both at lines 256-257).
   Keep recording the hashes; delete the two comparisons.
F3 Q4e/Q4g recompute the full analysis on every load and at creation (Q4e 215, 232-234,
   259-265; Q4g 221, 237-239, 260) and require byte-identical output. Load by digest;
   add one explicit audit function.
F4 Permutation count and seed are caller-supplied, default 64 (Q4e 113-114, 209-210).
   Fix 10,000 and the seed rule in code for the primary test.

KISS: build the production REAL path small (one events module, one runner, one reporter,
one aggregator) and leave the synthetic slices as regression evidence. Do not refactor them.

Open inputs: Oz approved file/era/cutoff; owner veto on the primary statistic; seed rule.
No extra review needed before review point B.
```

**End of memo.**
