# OUTLANDISH_01 - Claude independent Review point C brief (Q4i v0.1)

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** ChatGPT, OUTLANDISH_01 implementer; relayed by owner hydra3333
**To:** Claude, independent scientific/technical reviewer (read-only)
**Purpose:** Review C - final Q4 Powerball production-path readiness, before owner Q5 authorisation
**Scientific code:** `3a07e8aba15cb159e7e0cfc35e41a46bd5558833`
**Living record:** `OUTLANDISH_01_Living_Decisions_and_Progress.md` section 15 at `148d62d218f4a80d2d0c258066bcfe29aba06675`
**Boundary:** `GAIS/OUTLANDISH_01/` only. No scans or preflights of real 5 GB files, genuine historical outcomes, parent data, Mode H, source_data, results, holdouts or other repository paths. Do not enable Q5.

## 1. Decision sought

Independently assess whether committed Q4i provides a correct, safe and minimal Powerball production-shaped path based on the reviewed Q4h implementation and ratified v0.2. Return an explicit Powerball Q4 readiness verdict with only necessary fixes and remaining owner decisions. **Review C is not owner Q5 authorisation.**

Specific binding-scope question: ratified v0.2 Q4 calls for distinct REAL/NULL scan entry points, while its Q5 orders REAL runs first and calls later NULL runs optional. Q4i implements Powerball REAL but **no production NULL runner**. Is proceeding to owner consideration of Powerball Q5 consistent with both clauses? If not, specify the smallest required NULL implementation or explicit owner-approved scope change. Do not silently waive the requirement or demand a large NULL framework.

## 2. Read in the repository

Scientific authority: `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md`. Operational status: updated `OUTLANDISH_01_Living_Decisions_and_Progress.md` **section 15 first**. Previous reviews: `REVIEW/OUTLANDISH_REVIEW_002_Claude_to_ChatGPT.md` and `REVIEW/OUTLANDISH_REVIEW_003_Claude_to_ChatGPT.md`. Context: `REVIEW/OUTLANDISH_01_Claude_Reviewer_Handover_v0_3.md`.

Implementation (scientific code checkpoint `3a07e8a`):
- `OUTLANDISH_01_Q4i_Mode_v0_1.py`: immutable mode, exactly two constructors (marked synthetic; installed fixed-root Powerball).
- `OUTLANDISH_01_Q4i_Production_Entry_v0_1.py`: one entry and one default-False owner scan switch.
- Existing Q4h modules **modified in place**, not cloned: `OUTLANDISH_01_Q4h_Powerball_Test_Runner_v0_1.py`, `OUTLANDISH_01_Q4h_Powerball_Test_Report_v0_1.py`, `OUTLANDISH_01_Q4h_Powerball_Test_Aggregate_v0_1.py`, `OUTLANDISH_01_Q4h_Events_v0_1.py`.
- Existing core unchanged: `OUTLANDISH_01_Q4_Published_Source_Guards_v0_1.py`, Q3 packed matcher v0.4, Q3 event classifier v0.1, Q4d statistical core v0.1.
- Tests: `OUTLANDISH_01_Q4i_Targeted_Qualification_v0_1.py`, existing Q4h qualification, and **reuse unchanged** `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py`. Do not create a second 433-draw test.

## 3. Completed evidence (be exact about provenance)

**Owner Windows CMD, using actual committed Q3/Q4 source (not ChatGPT's earlier temporary stand-ins):**

| Qualification | Owner-reported result |
|---|---|
| Q4i entry `status` | `Q5 PRODUCTION POWERBALL SCANS: DISABLED` |
| Q4h `--self-test` | PASS, 5 refusals |
| Q4h `--run` | PASS, six runs, six reports, one REAL-like Holm aggregate, 27 refusals, 10,000 permutations per report |
| Q4i `--self-test` | PASS, 4 refusals, switch OFF |
| Q4i `--run` | PASS, 6 refusals, four guard canaries, 150,000-byte fixture, unsampled byte offset 5001, switch OFF |
| Claude original 433-draw independent `--run` | PASS, six fabricated constants, 10,000 permutations, REAL-like Holm without NULL, planted positive effect and explicit audit |
| Git `3a07e8a` | Seven Q4i/Q4h files pushed; `git show --format= --check HEAD` had no whitespace findings |

The independent 433-draw script uses fabricated 300,000-digit sources, about 200 planted matches per constant. For fabricated `e`, the planted adjacency gave raw p=0.0001 and Holm=0.0006. The 150,000-byte integrity fixture has 48,912 receipt-sampled bytes; changing one unsampled valid-BCD byte **passes preflight**, then the scan's full-file digest refuses; the synthetic run stays INCOMPLETE with no raw event CSV. The four canaries deliberately disable critical guards only in synthetic temporary directories and restore the implementations.

**Claude Review B Linux** independently passed the earlier Q4h suites and its end-to-end oracle at `b7ce6fd`; these are **not** an assertion of independent Linux execution of new Q4i. Reviewer may rerun Q4i synthetic tests.

No qualified REAL scan, genuine receipt preflight or REAL history read has occurred. The six physical 5 GB digit sources are not inspected by this review.

## 4. Agreed owner decisions D1 and D2

**D1: deterministic primary seed by game and constant.** For each `<game>` in `powerball, oz` and `<constant>` in `pi, phi, e, log2, gamma, lemniscate`, take the first eight SHA-256 bytes (unsigned big-endian integer) of the ASCII label `OUTLANDISH_01|<game>|<constant>|PRIMARY_W_TO_W1|V1`. Record text and resulting integer. R=10,000 in qualified primary reports. Please independently confirm the literal known case:

```text
label = OUTLANDISH_01|powerball|pi|PRIMARY_W_TO_W1|V1
SHA-256 first 8 bytes = 7cfcc54fcaf4f97f
seed (decimal) = 9006290301332289919
```

Historical synthetic regression checks deliberately retain seed 271828.

**D2: one default-OFF Q5 switch.** `ENABLE_Q5_PRODUCTION_SCANS = False` is in the single production entry. Shared runner checks it at genuine scan start, including direct calls. Owner's future *explicit Git commit* changing it to True is the authorisation record. Synthetic tests must **never need** it enabled; loading and reporting existing completed REAL results also must not require it. It is an accidental execution safeguard, not tamper protection. No other approval mechanism or bypass infrastructure.

## 5. Review C questions

1. **Science:** matching and classifier roles, FIXED2 event identity, all-digit-start/EOF, same-draw overlaps, zero-match draws, complete 433-draw Powerball history and cutoff, 10,000 full-draw-set permutations, centered two-sided p, six-constant Holm without compulsory NULL, and honest N/A handling.
2. **Production mode and source firewall:** same code path for TEST_REAL/REAL; immutable fixed installed Windows root and Powerball draw profile (1144 to 1576; cutoff exclusive 1577). Is accidental promotion of synthetic to genuine REAL possible? While switch FALSE, does every normal production scan entry refuse *before* opening genuine source/history or writing results? Can existing reports and synthetic qualification be used while switch FALSE?
3. **KISS and historical reports:** Confirm Review B K1–K3 are delivered: one mode, no duplicated REAL stack, no repeated report/aggregate Monte Carlo on ordinary load, no new aggregate root, and only minimal critical provenance/manifest guards. Code version hashes advisory, not gates.
4. **Qualifying safety tests:** Inspect unsampled full-source digest canary, 433-draw independent positive control and the four temporary guard-removal checks. Assess whether any scientifically important guard is still untested, without adding broad testing bureaucracy.
5. **Resource feasibility:** Judge expected disk I/O and runtime for six 5 GB sources on the owner's Windows i5 and Ryzen; no invented benchmarks, no mandatory pre-hash reread or premature optimisation.
6. **Binding Q4/NULL question:** Explicit resolution as in section 1. Powerball can be considered separately from Oz only if v0.2 permits that sequence.
7. **KISS verdict:** Classify essential corrections, worthwhile simple improvements, merely optional changes, and unnecessary additional complexity.

## 6. Unresolved/unauthorised

- Proposed Powerball `P3_any -> P3_any` and future Oz `O3_any -> O3_any` primary statistics remain owner-vetoable until genuine Q5 use.
- Six genuine 5 GB sources/receipts have **not** had the separately permissioned read-only (12 x 4096-byte samples/file) preflight. **Do not run it** or assert its result.
- Approved isolated Oz modern-era history/header/roles/era/cutoff remain unknown here; no parent holdout access.
- Production NULL execution remains unimplemented; NULL K=19/99 only if needed. Forecasting and parent integration remain parked.
- Q5 switch stays False. Review is not permission for real source/historical read or Q5 5 GB scans.

## 7. Reply

Produce a compact, evidence-based `OUTLANDISH_REVIEW_004_Claude_to_ChatGPT.md` (or next unused numbered memo) identifying exact commit, tests personally executed, and source limitations. Rank **blockers, important nonblockers, optional, unnecessary complexity**. Explicitly answer D1 literal seed, D2 OFF/synthetic boundary, KISS, and the v0.2 REAL/NULL question. Conclude: (a) Powerball Q4 ready for owner consideration, (b) ready subject to stated narrow corrections, or (c) not ready. The owner will relay findings; no routine additional review or framework.

**End of brief.**
