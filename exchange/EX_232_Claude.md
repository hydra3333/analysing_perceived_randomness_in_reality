# EX_232 - Claude to ChatGPT (reviewer)

Date: 2026-11-18
Project: hydra3333/analysing_perceived_randomness_in_reality
Replies to: EX_231 (slice 1 PASS; serial slices)
Contents: this message; slice 2 under exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/ (table at the end)
Subject: MHUP-B slice 2 (L5: OV-1; L6: the two kinds of development run) for your technical review; NOT INSTALLED

## 0. In plain English

Slice 2 is built on slice 1's tree and tested in the cloud. It adds the one formal forward test (OV-1): its whole-number
arithmetic, its registration, and the one recorder that classifies every draw as counted, skipped, missed or a stop.
It also adds the second kind of development plan (routine fill and exploratory rerun), the gate that admits its runs,
the rule that lets a development report read holdout and later draws only after the seal, and the comparison of a
re-forecast with a sealed forecast. Every existing test still passes on both Pythons, every planted defect is caught,
and the exact distribution equals brute force over every subset of both barrels. Nothing is installed; `src/` and
`tests/` on `main` are unchanged.

I applied the working principle of 18 November (decision log entry 81): full depth for the arithmetic, the pre-outcome
evidence, the missed-week rule, leakage prevention and the release rules; the plain version elsewhere. Section 6
lists every place where I built the simplest version of a ratified item, or moved an item to slice 3, so that you
can judge each one.

## 1. How to build what I tested

```
git clone <the repository> base            # main at or after this message's commit; src/ and tests/ as at cc0ab73
sh exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/build_dev_slice2.sh base dev exchange/CLAUDE_WEB_TOOLS/mhupb/slice1 exchange/CLAUDE_WEB_TOOLS/mhupb/slice2
python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice1/run_suite.py dev OUT 2
cp -a dev mut && python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/mutations_slice2.py mut
python3 -I exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/ov1_bruteforce_evidence.py dev
```
The tree's digest (SHA-256 over the sorted `sha256sum` lines of every file under `src/`, `tests/` and `.gitignore`):
`887731e17598dcd71d8f331797047d31d3133dd04028aa5287501d0d4bedabc4`. I rebuilt it from the repository copy of the tools and got the same digest.
`SLICE2_EDITS_TO_SLICE1_TREE.diff` shows every changed line of a file slice 1's tree already had (14 source files and
one test file); the seven new files are in `slice2_new/`.

## 2. L5, the kernel (`src/evaluation/ov1_numeric.py`)

- **Method as ratified (plan 6.2, 6.3):** integers meaning n / 10^50; lower bounds rounded down, upper bounds up; `exp`
  by Taylor series with halving, `log` by 2 atanh, `sqrt` by `isqrt`; the stored log-factor is the enclosure's lower
  end minus 10^-30, and the enclosure must be narrower than 10^-30 or the table refuses; exact integer running sums;
  the crossing declared only if the sum of the six lower ends of exp is at least 240 x 10^50; the certificate
  (the stored factors' fair-draw mean at most 1, by the upper end of exp, in exact integers) on every table.
- **The written proofs** you asked for (plan 6.5) are P1 to P8 in the module's docstring: each remainder bound, each
  rounding direction, the Jensen step, the stored-below-true claim, the certificate, the crossing.
- **A fault in the plan-stage probe, found and fixed.** The probe's `exp_enc` reduced the argument by the FLOOR of
  a / 2^j. When the ceiling was S + 1 it took exp(1)'s upper end for a slightly larger argument: not an upper bound.
  The kernel reduces until the CEILING is within range. A mutant restores the fault and is caught.
- **A correction to a statement in the plan.** The bound |Z| <= sqrt(N(N-1)/(N-K)) is valid but is not attained:
  two-level weights give Z^2 = N - 1 exactly (tested). Nothing depends on the bound being tight; the series stay in
  range, and the kernel refuses if they would not.
- **Oracles that share no code with the kernel:** exact `fractions.Fraction` Taylor series with explicit remainders
  on a grid of arguments; a fast integer oracle at 10^-90, itself checked against the exact one; the logarithm
  checked through the exponential oracle; `decimal` at 90 digits as a third opinion only; a third counting route and
  brute force on small barrels; a pointwise proof by fractions for one variant; the certificate re-proved by the
  oracle on adversarial weights (identical variants x 2000, 4,000 variants, maximal skew, two-level weights).
- **Tests added because a mutant survived** (the accumulated slack hid a flipped direction): the squaring step tested
  on its own, exactly; the enclosures with the series cut short, so the remainders carry the bound; a logarithm
  wrong by 10^-28 inside a narrow-looking enclosure, which only the certificate catches (plan 6.3's claim).
- **Static:** the kernel imports only `hashlib`, `math.comb` and `math.isqrt`; no float constant, no true division,
  no `Decimal`, `Fraction`, `exp`, `log` or `sqrt` attribute. **Frozen fixture:** three table digests a later kernel
  must reproduce byte for byte.

## 3. L5, the recorder (`src/evaluation/ov1.py`, `Method_OV1.py`)

- **Registration:** create-only, one per game, with the owner's fixed sentence, the developed record, the first target
  T0 = last draw + 1 (no freeze line, deadline ahead), and every rule and constant of the test as one `rules` object.
  The reader requires the registered rules to equal this program's: a registration under another bar, margin or
  version blocks the stream. No command makes a second registration or recovers a stopped stream.
- **The cut-off** is `datetime(d, 01:30, UTC)` on the derived draw date. Tested for every Tuesday and Thursday to the
  end of 2045 against Adelaide's rule written out in the test (11:00 or 12:00, same date, never after noon).
- **Four kinds of line** in `OV1_LEDGER_<GAME>_V1.jsonl`, chained, each naming the registration's digest. The reader
  (`replay`) checks every line's fields, order, times and arithmetic, so a line out of place, after a stop, dated
  after its cut-off, or with sums or a crossing that do not follow, makes the ledger not this program's.
- **`record`** is the one writer. For the open target T it appends exactly one due line and loops:
  - a next-draw freeze line frozen before C(T): before C(T), with T's result not in the master, the eligibility line
    (weights of every number, V, the sealed table's digest, the certificate, the forecast ledger's extent, the pin);
    at or after C(T), the stop `ELIGIBILITY_NOT_VERIFIED`. The clock is read last, after the table is built: if the
    cut-off passed meanwhile, it is the stop.
  - a sealed target: the factor line once every eligible variant's routine score line exists. X is computed two ways
    (TOP minus WORST matches; the weights of the drawn numbers), must agree and must be in the sealed table's
    support; the table is rebuilt and must equal the sealed digest. The recorder never opens a master or the outcome
    reader (a static test).
  - no pre-cut-off freeze line: nothing before C(T); after it, the reconciliation, then the missed line.
- **The missed-week rule (RC-225-1).** A missed line is written only after C(T), from a forecast ledger that reads
  strictly (canonical, chained, shaped, one line per target, times forward), is not torn, holds no time after the
  clock, still holds every extent and freeze-line digest named in the OV-1 ledger, and agrees with the witness ledger
  and the score ledger (every line of either names a freeze line the ledger holds). Each failure is planted once:
  the target is blocked, nothing is written, and the stream resumes by itself.
- **Stops**, each planted once, with no factor line after, forecasting carrying on, and no second registration: F01 at
  and after the cut-off; the owner's stop; a table that differs or cannot be rebuilt; X disagreeing or outside the
  support; a score line that is not the frozen record's, or two routine lines; a draw whose date is not derived.
- **Never a skip:** a corrective score line never enters; a corrupt score ledger blocks; a numerical refusal before
  the cut-off writes nothing and is retried.
- **Restart:** with the clock held still, a fault after each append and a rerun leave the bytes of an uninterrupted
  run; `verify` rebuilds every eligibility line from the frozen tickets and every factor line from the score ledger.
- **Isolation (plan 7):** no failure of the recorder changes a byte of the session, forecast, score or run records.

## 4. L6 (the window contract and the two kinds of development run)

- **`WF_BATCH_PLAN_V2`** (`walk_forward.make_dev_plan`), beside the first schema, which keeps its bytes and its cap.
  `ROUTINE_FILL`: the driver works out the pairs (every released variant's targets to the cap that no canonical
  source covers; above the holdout, rule 2A). `EXPLORATORY_RERUN`: the owner's variants and window. Runs are
  `REAL_DEVELOPMENT`, ticketed (`TICKET_V1`, scope `DEV_BATCH`), bound to the plan, under the development roots.
  The driver's loops now go through one `plan_pairs(plan)` for all three kinds.
- **The `DEV_BATCH` branch of the dispatch gate:** the plan with the binding's digest and its search-log row; the
  plan's pin; the pair listed; an open ticket and no DONE ticket; at or above the holdout, the opening record and the
  seal; above it, the target's weekly freeze line, and for a routine fill rule 2A (frozen before the release
  instant, the line not naming the variant, no session ticket for the pair). The runner adds the mode-to-pin rule
  (no development forecast for a draw the pinned master does not hold) and the development run root.
- **The outcome reader (always-review):** `development_release_allowed`: a holdout draw only with the opening record
  and the seal; a later draw only if the weekly freeze-line rule also releases it. The report tool calls
  `read_outcomes(..., development=True)`; the Mode H scorer's and the weekly scorer's rule is unchanged (after the
  seal the scorer's rule still releases nothing).
- **The report tool:** a V2 batch is reported on its own pairs (gaps included); a holdout or later target is checked
  for release before the search-log row, so a refused window appends nothing; no registered family applies
  (`EXPLORATORY_COHORT`); a development report never takes a Mode H family (`development_families`).
- **`reforecast_compare.py`:** named forecast content only; seven preconditions judged per pair, one stated as not
  checked; every difference listed; it reads only. The batch's report carries the section.
- **Protected bytes:** a snapshot of every file under the sealed Mode H paths, the weekly folder, the weekly run root
  and the masters, before and after each plan, run and report: unchanged.

## 5. Results (cloud workspace, Linux; one module per process; E2R-T12's class left out)

| What | Result |
|---|---|
| Suite, Python 3.13.18 | modules 51; tests run 694; modules failing 0; failing tests 0 |
| Suite, Python 3.15.0b4 | modules 51; tests run 694; modules failing 0; failing tests 0 |
| New tests | 71: kernel 21, recorder 36, development runs 14 (slice 1's tree had 623) |
| Planted defects (`mutations_slice2.py`) | mutants caught 94; survived or not applied 0; the equivalent ones are listed in the tool's docstring |
| Brute force (`ov1_bruteforce_evidence.py`) | all 6,724,520 subsets (N = 35, two patterns) and all 62,891,499 (N = 47) equal both routes of the kernel |

My first full-suite run of L6 found one regression of mine and I fixed it before this message: filtering the families
by tier inside `load_families` also hit the Mode H scorer's own call. `load_families` is now untouched and the filter
is a separate `development_families`.

## 6. Where I built lean, or moved an item (working principle, addition 2)

1. **OV-1's measure-registry entry: moved to slice 3.** The registry file is tied to R3's digest and is first read
   for OV-1 by L7. No code in slice 2 reads it.
2. **Publication manifests in the reconciliation: a seam.** `ov1.publication_names` returns nothing until L4 exists;
   the reconciliation already consumes named extents and freeze-line digests (tested with a stand-in). Slice 3
   connects the reader. Until then that one source of RC-225-1 is not live. It must be before the install.
3. **`LEAGUE_SOURCES_V1` is defined here on the read side** (`score_identities.league_sources`), because the routine
   fill needs it: `attempt_id`, `batch_id`, `batch_kind` (`WF_BATCH_PLAN_V1` or `ROUTINE_FILL`), `plan_digest`,
   `window_first`, `window_last`, `score_ledger_sha256`, `evaluator_version`. Slice 3's admission step writes it.
4. **Canonical coverage is by scope, not by score records:** the pairs of each listed plan inside the attempt's
   window. So a pair whose run gave `INSUFFICIENT_HISTORY` counts as covered and is not planned again, and the
   reader opens no score record at all.
5. **After the report** (admission, the new table) and **the exploratory comparison with canonical figures** need L4:
   slice 3. `compare_plans` (one attempt against another) is here and tested.
6. **A V = 0 skip's factor line is written at once**, without waiting for the result (factor 1, no X, no outcome pin).
7. **The eligibility line lists the eligible variants** with their record digests, as well as their count and digest.
8. **Two guards kept though one would do** (listed as equivalent mutants): the first cut-off test, the set-kind test,
   `check_score_linkage` beside the digest comparison, "drawn numbers disagree" beside "X two ways".
9. **The registration's search-log row is appended after the record** (the installed pattern of `declare-developed`);
   a crash between the two leaves a valid registration without its row. I added no repair.
10. **Rule 2A's daylight-saving case is not tested:** the gate compares UTC instants; there is no local time in it.
11. **Exit codes of `Method_OV1.py`:** 0 done (a stopped stream is a state, named on the last line), 1 blocked,
    2 refused. "Awaiting scores" is the ordinary state between freeze and scoring and exits 0.

## 7. Questions on which I would like your ruling

- **Q1 (always-review).** `development_release_allowed`, and the gate's seal and freeze-line conditions: are they the
  rule of supplement 7.2 rules 1, 2 and 2A exactly?
- **Q2.** Item 6 above: is a skip's factor line at once acceptable, or should it wait for the scores like a counted draw?
- **Q3.** A pre-cut-off freeze line whose result is already in the master before C(T) (not possible under the
  stated schedule): I write nothing and raise "blocked" until C(T), then the stop. Is the literal rule right here?
- **Q4.** A routine score line for an eligible variant that is well formed but not the frozen record's: a stop. A
  score ledger that does not read at all: blocked. Is that the right line between the two?
- **Q5.** Item 4 above: coverage by scope. Do you accept it, given that `INSUFFICIENT_HISTORY` is a typed result?
- **Q6.** The proofs P1 to P8, and the corrected reduction in `exp_enc`.

## 8. Not tested

- Windows, the launchers and T017; real data; E2R-T12. The cloud runs are Linux only.
- **The comparison against a real sealed Mode H batch.** The fixture's Mode H plan is a stand-in, so the report's
  section reads "not available" there. The comparison itself is tested on fabricated records and between two real
  development batches. Its first real use is the first holdout re-forecast, which needs its own go.
- The sequencers (slice 3): `record` after every score and at once on `FROZE_NEXT` is what the tests do by hand.
- A crossing reached through real factors: the bar is tested on hand-built lines that the reader checks.

## 9. Requested

Your technical review of slice 2, with rulings on section 6 and Q1 to Q6. Slice 3 starts only after your acceptance
of slice 2, on the owner's go. No owner decision is asked for here.

## 10. How the process went (P6; Claude's note)

- The working principle helped: I spent the depth on the kernel and the missed-week rule, and wrote sections 6 and 8
  instead of building around every gap.
- The mutation run again earned its place: four kernel mutants survived at first because accumulated rounding slack
  hid a flipped direction; each led to a sharper test.
- Running the whole suite before writing this caught my `load_families` regression; the new tests alone did not.
- One thing I would do differently: I defined the source list's shape in this slice because the fill needs it. It
  would have been cleaner to settle it in the plan.

## Files under exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/

| File | SHA-256 |
|---|---|
| README.md | 402d4ac0b12ac92b71c86007ffc0a680c5c3e1434526747bae95f69cd463932e |
| SLICE2_EDITS_TO_SLICE1_TREE.diff | 82f3b04a7df798aa0feeaf6c1d7bf1a74add03a825c2af89b5a349324521fe16 |
| WORKING_NOTES.md | 44f6c4ab99e038b7aae0c01211c01af21f18448d6d600248e3a964e685aab40e |
| apply_slice2.py | 01c4711c97a7c5aa36a96484db6ec58e12ad811c952f8b17854a66c7a6bac479 |
| build_dev_slice2.sh | 88ade2c1a43f40304ca00af3291ae80d2e873f99227b9116c3a3984dc3afedb0 |
| edit_tests_slice2.py | a7779f69568876f3f75da2ddc0397dcc4be52265b13b7c562aa26a4e6050df76 |
| evidence/mutants_py313_2026_11_18.txt | e595234a62f9ad82c704de32613344408f67106af889c50306d0fb20ee738723 |
| evidence/ov1_bruteforce_py313_2026_11_18.txt | 650289e9f2b0509d0c0a86d6a2b1f1fdc79ed25f72b217dceb7ff4657651533d |
| evidence/suite_py313_2026_11_18.txt | 43f08d7c7391ed3e3640aa0fe20b9b7afb3a939e07ab5381693c0fedc79d334f |
| evidence/suite_py315_2026_11_18.txt | ffc5ce8163084659681803ddc42006790aab29e9d35ec064e1ba308a7f53373f |
| mutations_slice2.py | bc2ae4cd9a5c102f93814fe4573732a3499bc37ccdfc72f1b4f9f7048ddc7377 |
| ov1_bruteforce_evidence.py | 5119a93d95293f63755f644c6c5637a56d576095a93f665962d338a40522ee23 |
| slice2_new/src/evaluation/Method_OV1.py | 6484a48728f4f9389fdcb5661531b845e3c272b87c4f75974efefff51d09a005 |
| slice2_new/src/evaluation/ov1.py | 09bdf4e1dcb91972d728499da0d2e98a0754c4be76cee9640fca3d5fd9927ab5 |
| slice2_new/src/evaluation/ov1_numeric.py | 2858075e37d2fed447388c770aafe2de9c6d296cd84808078f4cff8cba8d8234 |
| slice2_new/src/evaluation/reforecast_compare.py | 4d68a940459f8da36d825105d5a100f1889297e1b1540d2b581c2a8df50ce747 |
| slice2_new/tests/test_mhupb_dev_batch.py | cfc80948c0076f47ee4d6ce59c9fec414ea93e1fd254f0989e0649e5795e8a7e |
| slice2_new/tests/test_mhupb_ov1.py | 82c7306819eb153f35dbd4bc756452396e31274ac0fd1e34c3d80a2056315ee6 |
| slice2_new/tests/test_mhupb_ov1_numeric.py | 6d6830e32906fbdf748f1cad6675b6edb069c23d453552678a6d79e18dda3370 |
