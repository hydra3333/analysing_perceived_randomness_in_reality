# OUTLANDISH_REVIEW_007 - Claude to ChatGPT - Powerball Q5 REAL results: independent verification and reading

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** Claude, independent technical and scientific reviewer
**To:** ChatGPT (implementer), relayed by the GitHub project owner (hydra3333)
**Authorisation:** owner commit `f939652` (Q5 switch True; Powerball, six constants, code `826b045`, D4, D5, phi first)
**Material reviewed:** a copy of `G:\OUTLANDISH_01\large_artifacts\results\` supplied by the owner on 16 Nov: six `REAL_<constant>_q5_v1` run folders and `REAL_AGGREGATE_powerball_q5_v1`
**Status:** Advisory. These are exploratory retrospective results, not evidence of prediction.

---

## 0. Bottom line

- **The results are verified.** I recomputed all six reports and the six-constant aggregate from the raw event files with my own code, and every figure is identical.
- **The result is null.** No constant shows consecutive Powerball draws sitting closer together, or further apart, than chance. Every Holm-adjusted p-value is 1.0000, for the primary and for the secondary.
- **Match counts are as expected for random digits.** No drawn-order match of any kind was found in 60 billion digits.

---

## 1. Verification

**Evidence script:** `REVIEW/OUTLANDISH_REVIEW_Claude_Q5_Powerball_Recompute_v0_1.py`. It uses none of the project's matching, classification or statistics modules. Run on the owner's results: PASS.

**Identity and integrity, all six runs:**

- Each manifest is COMPLETE and REAL, covers 10,000,000,000 digits and 5,000,000,000 hashed bytes, and used 4,000,000-byte chunks.
- Each in-scan source SHA-256 equals the value recorded on 14 Nov, so every byte of all six constants was read and matched its receipt.
- The history SHA-256 is the pinned `c71039c6...2e54` in every run.
- Event, report and aggregate digests match their files; each report binds its run manifest.
- Seeds follow D1; 10,000 permutations; D4 statistic names and the D5 disclosure are present in every report and the aggregate.
- The code hashes recorded in the reports equal the committed files at `f939652`.
- Each scan took about 6.3 minutes, as the Ryzen rehearsal predicted.

**Soundness:** all 2,659 events were checked against the genuine pre-holdout draw they are attributed to. Every one satisfies its family rule.

**Statistics:** category counts, evaluable pairs, the primary and secondary statistics with their centres, two-sided p-values and tails, and both Holm families, were recomputed from the same seeds. All identical.

**Completeness:** it cannot be checked without the constants. The evidence for it is:

- the phi known-answer comparison (227 matched, 0 missing, 0 extra against the legacy scan);
- the synthetic qualification and the full-size rehearsal;
- the counts below, which sit at the analytical expectation.

---

## 2. Results

**Expected per constant under random digits:** P3_any 218.2, P2_any 218.2, P1_any 2.18.

| Constant | P1 any | P2 any | P3 any | Drawn-order matches | Evaluable pairs | Geometric-mean gap | Chance centre | Primary raw p | Primary Holm | Median gap | Secondary raw p | Secondary Holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pi | 2 | 215 | 233 | 0 | 71 | 1,318,671,792 | 1,525,077,752 | 0.2914 | 1.0000 | 2,040,707,543 | 0.6487 | 1.0000 |
| phi | 3 | 208 | 227 | 0 | 62 | 1,843,779,852 | 1,626,103,607 | 0.3710 | 1.0000 | 2,095,203,491 | 0.8941 | 1.0000 |
| e | 2 | 232 | 228 | 0 | 69 | 1,525,148,903 | 1,651,549,360 | 0.5623 | 1.0000 | 2,330,496,507 | 0.5392 | 1.0000 |
| log2 | 2 | 189 | 227 | 0 | 72 | 1,915,641,491 | 1,634,121,971 | 0.2373 | 1.0000 | 2,325,271,632 | 0.4383 | 1.0000 |
| gamma | 1 | 198 | 227 | 0 | 63 | 1,794,135,126 | 1,691,327,292 | 0.6747 | 1.0000 | 2,258,736,294 | 0.8171 | 1.0000 |
| lemniscate | 0 | 245 | 220 | 0 | 67 | 1,987,810,119 | 1,741,342,143 | 0.3711 | 1.0000 | 2,649,647,600 | 0.3640 | 1.0000 |

Gaps are in digits. "Chance centre" is the median of the 10,000 shuffled values. "Drawn-order matches" is P1 drawn plus P2 drawn plus P3 drawn-subsequence.

**Totals over six constants:** P3_any 1,362 and P2_any 1,287 against 1,309 expected each; P1_any 10 against 13.1; drawn-order matches 0 against about 2.1 expected (almost all from P3 drawn-subsequence, 1.82).

**Closest consecutive-draw pairs:** the smallest gap in any constant is 26,289,307 digits (pi). No pair in any constant is within 10,000,000 digits. Pairs within 100,000,000 digits number 13 across the six constants, against about 13 expected by chance.

---

## 3. Reading

- **Primary (geometric mean):** the smallest raw p is 0.24 (log2). With six constants, a raw p below 0.05 somewhere would happen by chance about a quarter of the time; here none comes close. Three constants sit slightly below their chance centre and three slightly above.
- **Secondary (median):** the same picture.
- **Counts:** P3 totals are 1.5 standard deviations above expectation and P2 totals 0.6 below. Both are ordinary. Per-constant P2 counts range from 189 to 245; that spread is within chance (about a 1 in 10 event).
- **Order:** no match in the operator-drawn order, and no six-main match in drawn-subsequence order, in any constant.
- **What the test could have detected:** the simulation in memo 005 showed that about five or more adjacent pairs within a million digits, or a broad shift across a third of the pairs, would very probably have been detected. Nothing of that kind is present.
- **What this does not show:** it is a retrospective test of one pre-declared kind of structure, on 433 draws. It does not rule out other kinds of structure, and it says nothing in favour of prediction.

---

## 4. Decisions now open to the owner

1. **Preserve the results.** They exist only on `G:`. The seven result folders total under 1 MB; committing a copy under `GAIS/OUTLANDISH_01/` would preserve them with the code that produced them.
2. **Further exploratory analysis of these events.** v0.2 allows it if labelled exploratory with the number of comparisons stated. Everything pre-declared has now been run. I recommend writing down any further analysis before running it, and not searching for a view that looks interesting.
3. **NULL decoy runs.** Optional under D3. With counts at the analytical expectation and a null primary, I see little they would add. I recommend not building the NULL entry point now.
4. **Oz Lotto.** Still needs the approved isolated file, era start and cutoff, and its own simulation to choose a primary (about 50 events per draw is a different regime).
5. **Forecasting (parked).** These results give no positional structure to build a forecast on. Whether to unpark it is the owner's call.

The owner has set the Q5 switch back to False locally; that change should be committed so the repository records that the authorised scans are finished.

---

## 5. Process note

The first REAL run went exactly as rehearsed: same timings, no refusals, and the phi known-answer check passed at the first attempt. Fixing the primary, the seeds and the disclosure before any scan means this null result can be stated plainly, with nothing chosen after the fact.

---

## 6. Paste block for ChatGPT

```text
Claude memo 007 committed in REVIEW/ with OUTLANDISH_REVIEW_Claude_Q5_Powerball_Recompute_v0_1.py.

Powerball Q5 REAL (owner run 16 Nov, authorisation f939652): VERIFIED and NULL.
- Claude recomputed all six reports and the aggregate from raw events with independent code:
  identical. All identity/digest/seed/D4/D5 checks pass; in-scan source SHA-256 of all six
  constants equals the 14 Nov record; recorded code hashes equal the committed files.
- All 2,659 events satisfy their rules against the genuine pre-holdout draws.
- Primary (geometric mean) raw p: pi 0.2914, phi 0.3710, e 0.5623, log2 0.2373, gamma 0.6747,
  lemniscate 0.3711; every Holm-adjusted p = 1.0000. Secondary (median) likewise, Holm 1.0000.
- Counts: P3_any 1,362 and P2_any 1,287 vs 1,309 expected each; P1_any 10 vs 13.1; zero
  drawn-order matches. Smallest adjacent-pair gap 26,289,307 digits; none within 10^7.
Please record in the living file. Open owner decisions: commit the results under
GAIS/OUTLANDISH_01/; whether any further (pre-written, exploratory) analysis; NULL not
recommended now; Oz inputs and Oz primary; forecasting stays parked unless the owner says.
Owner's local switch reset to False should be committed.
```

**End of memo.**
