"""Build the releases and WF-1 design note v0.1r1 from v0.1 by counted edits (Claude, 30 October 2026).

v0.1r1 answers EX_078 (WF1-R3-B01, C01..C04, O01, O02) and records the owner's decisions WF1-6 and
WF1-12 and his D-10 reading. Every old string must occur exactly once; all text is ASCII.
Input: v0.1 as sent in EX_077 (LF 12282930...bdf). Usage: python3 -I make_design_v0_1r1.py IN OUT
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read().replace(b'\r\n', b'\n')
assert hashlib.sha256(raw).hexdigest() == '12282930e226d70391d80285efa60e70bce369b2ad738ffa8203c18dd6beabdf'
t = raw.decode('ascii')

E = []
E.append(("**Version:** v0.1 DRAFT for the reviewer's design review (R-3), 30 October 2026. Author: Claude. Ratifier: the project owner.",
"**Version:** v0.1r1 DRAFT for the reviewer's focused RECHECK, 30 October 2026. It resolves EX_078 (`exchange/EX_078_ChatGPT.md`, `465a8ce2...84f3`; RECHECK: 1 BLOCKER, 4 CORRECTION, 2 OPTIONAL): WF1-R3-B01 (the driver's STOP rule now classifies the runner's terminal reasons and fails closed; section 5.3), C01 (the seed's trust basis is stated, owner decision WF1-12; section 8), C02 (the search-log row is written before any outcome is read; section 6.1), C03 (the downgrade rules for missing opportunities; section 6.2A), C04 (the numerics wording, accuracy budget and bounds; section 6.6), O01 (the plan checks the flags too; 5.2) and O02 (batch and report windows shown apart; 5.6, 9.1). It also records the owner's decisions WF1-6 and WF1-12 and his reading of D-10 (section 12). Appendix A maps every finding. v0.1 (`12282930...6bdf`) is superseded. Author: Claude. Ratifier: the project owner."))
E.append(("- **Base:** `main` at `1d836c6` (wave 2 installed at `b61b1a2`; the handovers and register v0.20 at `03f7da4`).",
"- **Base:** `main` at `b4b83c1` (EX_077 at `4bdb060`, EX_078 at `b4b83c1`; wave 2 installed at `b61b1a2`; the handovers and register v0.20 at `03f7da4`)."))
# O01
E.append(("- the **cohort**: every (method, variant) with an active `SUPPORTED` entry in the installed registry for the game and a runner adapter, in method-number then variant order.",
"- the **cohort**: every (method, variant) with an active `SUPPORTED` entry in the installed registry for the game, no `IN_DEVELOPMENT.txt` flag in its method folder (O01), and a runner adapter, in method-number then variant order. The dispatch gate still rechecks both at every run."))
E.append(("an empty cohort; a ledger that is not the version-1 INIT line.",
"an empty cohort; a method with a `SUPPORTED` entry whose flag is still present (an inconsistent installed state, reported by name: O01); a ledger that is not the version-1 INIT line."))
# B01
E.append(("""- **A refusal stops the batch** (A STOP is a STOP). If the runner refuses (`RunRefused` or `DispatchRefused`), the driver stops at once, records the refusal, and runs nothing more.
- **A method failure does not stop it.** A run ending in `RUNTIME_FAILURE`, `NUMERIC_INVALID` or `VALIDATION_FAILURE` is the method's own result for that target. It stays on disk, is counted, and the batch goes on. It is never retried automatically.
- **Resume:** a (variant, target) pair is done when a terminal record exists for it under the plan's pins, with any outcome except `RUNTIME_FAILURE` whose reason is `INTERRUPTED` or `PUBLICATION_FAILED:`. Those two are run again. Every attempt's folder stays as it is; nothing is deleted or moved.
- **Ctrl-C** ends the current run with its `INTERRUPTED` terminal record (existing behaviour). The driver then writes its segment record and exits.
- **Segment records:** each `run` invocation writes `segment_<UTC>.json` (create-only) at its end, listing the run IDs it created and why it stopped. The scorer does not depend on them (section 6.1); they are for the owner's audit.""",
"""- **The STOP rule (A STOP is a STOP; EX_078 WF1-R3-B01).** The driver classifies each run by the terminal record's **reason**, not by its outcome alone, and it fails closed: a reason it does not recognise is a STOP. The installed runner is not changed; the classification lives in the driver.

  | The run ends with | Class | The driver |
  |---|---|---|
  | `RunRefused` or `DispatchRefused` raised (orphan marker, switch, data source, dispatch gate) | STOP | stops at once; nothing was created for that run |
  | reason `DATA_ADMISSION_REFUSED: ...` (outcome `VALIDATION_FAILURE`): the reader refused the pinned ledger, master, INIT record or prefix | STOP | stops at once: the data source is no longer admitted |
  | reason `PUBLICATION_FAILED: ...` or `INTERRUPTED` | STOP | stops at once |
  | any exception escaping `run_contract_method` (including a run folder that cannot be created, a terminal record that cannot be written, and Ctrl-C before the run folder exists) | STOP | stops at once |
  | any other reason prefix | STOP | fails closed and names the reason |
  | reason `METHOD_FAILED: ...` (`RUNTIME_FAILURE` or `NUMERIC_INVALID`) | CONTINUE | the method's own result for that target: counted, never retried |
  | reason `CONTRACT_REFUSED_OUTPUT: ...` (`VALIDATION_FAILURE` or `NUMERIC_INVALID`) | CONTINUE | the method's output failed validation: counted, never retried |
  | reason `NO_TICKET_NO_DIAGNOSTIC: ...` | CONTINUE | a valid empty target (`DIAGNOSTIC_ONLY`), counted |
  | reason `PUBLISHED: ...` (`SUCCESS`) | CONTINUE | the forecast is frozen |

- **Checks at the start of every `run` (also on resume), before any run:** the orphan marker is absent; for every cohort member, the installed registry's active entry digest and declaration digest still equal the plan's, and no flag is present. Any change refuses the whole invocation before anything is created (exit code 2). These are registry reads only; the driver opens no data file.
- **Between targets:** an orphan marker that appears mid-batch makes the next run raise `RunRefused`, which is a STOP; nothing runs after it.
- **Resume:** a (variant, target) pair is **done** when it has a terminal record, under the plan's pins, whose class is CONTINUE. Every other pair is run again on resume: no terminal record at all (including a run folder left without one); `INTERRUPTED`; `PUBLICATION_FAILED`; `DATA_ADMISSION_REFUSED`. Each new attempt gets a new run ID and folder; earlier attempts stay exactly as they are, and nothing is deleted, moved or rewritten.
- **If the cause persists on resume:** a runner refusal stops it again before anything is created. A data-admission failure stops it after one recorded attempt, the first pair it tries. A resume therefore never makes more than one failed attempt.
- **Ctrl-C** during a run ends that run with its `INTERRUPTED` terminal record (existing behaviour). If it lands before the run folder exists, nothing is created. Either way the driver stops, as in the table.
- **Segment records:** each `run` invocation tries to write `segment_<UTC>.json` (create-only) when it stops, listing the run IDs it created, the pairs it classified and why it stopped. If that write fails, the same lines go to the console, and the driver exits with code 1. No evidence depends on it: run folders describe themselves, and the scorer does not read segment records (section 6.1).
- **Exit codes:** 0 every pair done; 1 stopped (by the STOP rule or Ctrl-C); 2 refused before any run."""))
# O02 5.6
E.append(("For each game, in your order (decision WF1-5):\n1. `Run_Experiment.bat Method_Walk_Forward.py plan --game POWERBALL --first 1145 --last 1576`, which prints the batch ID.\n2. `Run_Experiment.bat Method_Walk_Forward.py run --batch <ID>` (about 100 minutes for Powerball on the probe's speed; section 9.1).",
"""For each game, in your order (decision WF1-5). **The batch range and the report window are different things (O02):**

| Game | Batch: targets predicted | Report window (R3 17.3.6) | Notes |
|---|---|---|---|
| Powerball | 1145-1576 (432 targets) | 1286-1576 (291 draws) | the batch also covers 1145-1285, for later exploratory windows |
| Oz Lotto | 1475-1693 (219 targets) | 1474-1693 (220 draws) | 1474 is in the window but in no track's grid: it has no history, so it is never predicted or scored |

1. `Run_Experiment.bat Method_Walk_Forward.py plan --game POWERBALL --first 1145 --last 1576`, which prints the batch ID.
2. `Run_Experiment.bat Method_Walk_Forward.py run --batch <ID>`. On the Linux probe's speed this is about 105 minutes for Powerball's 432 targets (section 9.1); that is planning evidence, not a Windows result."""))
# C02 6.1
E.append(("""4. **The scoring plan** (`SCORING_PLAN_V1`, create-only) records the grid, the selected forecasts' content and receipt digests, and the availability counts. It is written **before** any outcome is read.
5. **The outcomes** of the grid's targets only (6.3).
6. **Records:** the score ledger and the rank-position ledger (6.4).
7. **Measures, N1, and the report files;** then exactly one search-log row (6.7).""",
"""4. **The search-log row (EX_078 WF1-R3-C02).** One `RANKING_REPORT` row is appended to the search log (6.7) **before any outcome is read**. It holds the report attempt ID (`rr-<32 hex>`), the UTC time, the game, mode and window, the cohort and grid digests, the family IDs, the measures, the declared number of tests, the batch ID and the digest of the scoring plan about to be written.
5. **The scoring plan** (`SCORING_PLAN_V1`, create-only) records the attempt ID and the search-log row number, the grid, the selected forecasts' content and receipt digests, and the availability counts. It is written **before** any outcome is read.
6. **The outcomes** of the grid's targets only (6.3).
7. **Records:** the score ledger and the rank-position ledger (6.4).
8. **Measures, N1, and the report files.** The report's JSON names the attempt ID and the row number.

**Attempts that do not finish stay counted.** Every invocation that gets past step 3 has its row, whether or not it reaches a report; a later failure (even after outcomes were read) never removes it, and no row is ever edited. Every report header states the number of `RANKING_REPORT` rows for its game, and how many of them have no completed report (an attempt ID with no report file). A crash between steps 4 and 5 leaves a row without a scoring plan: it is counted as an unfinished attempt, which errs on the side of counting more searching, never less. An invocation refused at step 1, which reads nothing, appends nothing."""))
# C03 6.2A
E.append(("  Bonferroni over exact per-track p-values stays guaranteed with own-set grids, because each test is valid on its own fixed grid (R3 17.5.3 needs valid inputs and a predeclared family, not equal n). The N1 maximum statistic replays each track on its own grid.",
"""  Bonferroni over exact per-track p-values stays guaranteed with own-set grids, because each test is valid on its own fixed grid (R3 17.5.3 needs valid inputs and a predeclared family, not equal n). The N1 maximum statistic replays each track on its own grid. The owner agreed to this on 30 October 2026 (WF1-6), subject to the rules of 6.2A.

### 6.2A Missing opportunities: how labels are downgraded (EX_078 WF1-R3-C03)

**Per track.** A grid cell is **valid** when it has exactly one selected consumable forecast with an available ticket for that readout and no reproducibility failure. A track's status is:

| Track status | When | Its local significance labels |
|---|---|---|
| `GRID_COMPLETE` | every cell of its grid is valid | as R3 assigns (`EXACT_LOCAL` for MR4, MR7 and MR16; `N1_CALIBRATED` for MR1 once N1 runs) |
| `GRID_INCOMPLETE` | at least one cell is not valid: a failed or non-consumable run, no run at all, an `INSUFFICIENT_HISTORY` record the declaration does not predict, or a `REPRODUCIBILITY_FAIL` | `SELECTION_UNVERIFIED`; the figures are still computed on the valid cells and shown, with the count of invalid cells by reason |
| `GRID_EMPTY` | no valid cell at all | `MR_INSUFFICIENT_DATA` (n = 0): no p-value, never zero sigma |

With own-set grids, one track's invalid cells change no other track's local figures, because no other track's grid depends on them.

**Per family** (6.7):
- **The roster and M are fixed at registration** (M = 80). A track that is incomplete or empty stays in the roster and in M, and is listed by name with its status. It is never removed or replaced.
- **The guaranteed label** (Bonferroni, guaranteed) is given only if all M tracks are `GRID_COMPLETE`, every input p-value is `EXACT_LOCAL`, and the family was registered before its first use (checked against the search log, MRT-17).
- **Otherwise**, the same arithmetic, min(1, M x p), is shown labelled `BONFERRONI_REFERENCE_UNCALIBRATED`, with the number of tracks that broke the condition. An empty track contributes no p-value, but M is not reduced.
- **The N1 maximum statistic** is `N1_FIXED_FORECAST_REFERENCE` in any case. A family with any incomplete track also carries `SELECTION_UNVERIFIED` on it.

**Per table.**
- An own-set table's local figures follow each row's track status.
- The common-set descriptive table (6.2) is the intersection of the valid cells, so any invalid cell can change it for every row. If any cohort track is `GRID_INCOMPLETE`, every significance figure in that table is `SELECTION_UNVERIFIED` (R3 17.3.7A, applied table-wide as R3 writes it)."""))
# C04 6.6
E.append(("""### 6.6 Exact arithmetic everywhere (decision WF1-7)

R3 17.11 makes production tails log-space sums via `lgamma`, with an exact `Fraction` oracle in the tests. At this project's sizes (n <= 432) the exact route is fast (section 9.3), so the proposal reverses the roles:
- **Counts, sums and divisions** are integers.
- **Tails** are exact: binomial tails as `Fraction`s; MR7's null as integer polynomial coefficients.
- **Sigma** is solved from the exact tail by a `decimal` bisection on the normal tail, at 80 digits. It never forms 1 - p in floating point.
- **Clopper-Pearson bounds** are found by exact bisection.
- **MR1** uses `decimal` logarithms.
- **Conversion to float64 happens once,** at output, by correctly rounded conversion.
- **The `lgamma` route** becomes the tests' independent cross-check (MRT-04 unchanged in substance).

`decimal` and integer arithmetic are the same on every platform, so a report on Windows and Linux is byte-identical, apart from its header time and environment lines. That is W2-7's rule, applied to the scorer. MRT-08 (determinism) then holds across platforms, not only on one machine.""",
"""### 6.6 Exact counts and tails; deterministic high-precision transforms (decision WF1-7; EX_078 WF1-R3-C04)

R3 17.11 makes production tails log-space sums via `lgamma`, with an exact `Fraction` oracle in the tests. At this project's sizes the exact route is fast (sections 9.3 and 9.5), so the proposal reverses the roles. Precisely:
- **Exact integer and rational values:** counts, sums and divisions (integers); binomial tails (`Fraction`s, summed on the shorter side over the common denominator b^n, so exactly and without cancellation); MR7's null distribution (integer polynomial coefficients); N1's comparisons (section 7.4).
- **Deterministic, bounded-accuracy decimal transforms** (not exact values): sigma, MR1's logarithms, and the Clopper-Pearson bounds.
  - **Sigma:** 80-digit `decimal` arithmetic. The normal tail Q(z) uses the erf series for z/sqrt(2) < 5 and the continued fraction (400 terms) from 5 up. Sigma is solved by bisection to an interval far below float64 resolution, and never forms 1 - p in floating point. p >= 1/2 gives 0 sigma exactly.
  - **MR1:** `decimal` logarithms at 80 digits.
  - **Clopper-Pearson:** bisection on the exact binomial tail, to an interval below float64 resolution.
- **Error budget:** each decimal transform is accurate to a relative 1e-30 or better before it is rounded to float64. That is far inside R3 17.11's 1e-6 for sigma. The evidence (section 9.5): the two tail routes agree to 1.7e-47 where both apply; the continued fraction does not change between 400 and 4000 terms; ln Q agrees with an independent asymptotic series to 2e-17 absolute from 12 to 60 sigma.
- **Output:** each value is converted to float64 once, by correctly rounded conversion. Each p-value is also written as `log10` text with 15 significant digits.
  - A p-value below float64's normal range carries the label `P_BELOW_FLOAT64_RANGE`; its float field is the correctly rounded subnormal or 0.0, and its `log10` text is kept.
  - A sigma above 1000 (a p-value below about 10^-217000) is reported as `SIGMA_ABOVE_BOUND`, shown as ">= 1000".
  - No tail is ever silently replaced by an approximation.
- **Bounds on exact work:**
  - binomial tails are exact for every n the project meets (n = 5000 with p = 1e-9 in 0.1 s; section 9.5);
  - MR7's exact null is computed for n <= 1000 (24 s at n = 1000; WF-1's largest n is 432). Above that bound MR7's tail is `MR_EXACT_BOUND_EXCEEDED`, and the normal approximation is shown beside it, labelled `APPROX_UNCALIBRATED`, never unlabelled.
- **The `lgamma` route** becomes the tests' independent cross-check (MRT-04 in substance).
- **Byte identity:** integer, `Fraction` and `decimal` arithmetic and correctly rounded conversion are deterministic and the same on every platform. So a report's CSV and its data fields should be byte-identical on Windows and Linux, excluding the header's time, environment and tool-provenance lines. This is a design property, not yet evidence: WF-1B's tests compare the bytes (on the same synthetic inputs, on Linux in the package's runs and on the owner's Windows run). That is W2-7's rule applied to the scorer, so MRT-08 then holds across platforms, not only on one machine."""))
E.append(("  - each report run appends exactly one `RANKING_REPORT` row;",
"  - each report invocation that gets past its refusals appends exactly one `RANKING_REPORT` row, before any outcome is read (6.1, step 4);"))
# C01 / WF1-12 section 8
E.append(("| Accepted only if | `version` \"2.0\", `chainIndex` 2, that exact `timeStamp`, `statusCode` 0, and a 128-hex-character `outputValue` |",
"| Accepted only if | `version` \"2.0\", `chainIndex` 2, that exact `timeStamp`, `statusCode` 0, and a 128-hex-character `outputValue` (upper-case hexadecimal, as NIST publishes it) |\n| Trust basis | NIST's official HTTPS service (`beacon.nist.gov`). The pulse's signature and certificate are **not** validated (owner decision WF1-12) |"))
E.append(("""1. **After the pulse time,** you open NIST's page for that pulse in your browser: `https://beacon.nist.gov/beacon/2.0/pulse/time/1793923200000`. Save the JSON to `E:\\TEMP`, and attach it to the Claude chat. Nothing in the project fetches it.
2. **Claude checks it field by field** against the acceptance row above.
3. **Claude independently reads the same pulse** from NIST's public archive at its permanent address (`https://beacon.nist.gov/beacon/2.0/chain/2/pulse/<pulseIndex>`) and compares `uri`, `chainIndex`, `pulseIndex`, `timeStamp`, `statusCode` and `outputValue`. The reviewer may also check (E2R-R63: "someone other than the person who fetched it").""",
"""1. **After the pulse time,** you open NIST's page for that pulse in your browser: `https://beacon.nist.gov/beacon/2.0/pulse/time/1793923200000`. Save the JSON to `E:\\TEMP`, and attach it to the Claude chat. Nothing in the project fetches it.
2. **Claude checks it field by field** against the acceptance row above, and records the SHA-256 of the saved file's bytes.
3. **Claude independently reads the same pulse** from NIST's public archive over HTTPS, at its permanent address (`https://beacon.nist.gov/beacon/2.0/chain/2/pulse/<pulseIndex>`), and compares `chainIndex`, `pulseIndex`, `timeStamp`, `statusCode` and `outputValue` (and `uri`). This is D-9's second-person check (E2R-R63: "someone other than the person who fetched it"). The reviewer may also check.

**What is and is not verified (EX_078 WF1-R3-C01; owner decision WF1-12, 30 October 2026).**
- **Verified:** that two separate HTTPS reads of NIST's official service, by two different people, return the same pulse with the announced chain, time stamp and field, a normal status code and a well-formed value.
- **Not verified:** the pulse's cryptographic signature and certificate. That check is recorded as `NOT_PERFORMED`. D-9 to D-11 never required it, and none of them changes.
- **NIST's notice of 23 October 2026** (on its Beacon 2.0 page, `https://csrc.nist.gov/projects/interoperable-randomness-beacons/beacon-20`) says that pulses issued since 3 September 2026 refer to an incorrect certificate, and that verification for that period will need a different certificate. The 6 November pulse may be affected. Because no signature check is made, the notice does not block approval. It is recorded in the policy, with the pulse's `certificateId` as published.
- **The residual risk, accepted by the owner (WF1-12):** that the value both reads returned was not NIST's genuine output. The seed's purpose is to be externally generated and fixed in advance, so that no one can choose a favourable seed after seeing results. The project does not run a security-critical system. For that purpose, two independent HTTPS reads of NIST's own service are proportionate.
- **Not proposed, but available:** NIST's chain links can be checked without a certificate (the next pulse's `previous` value equals this `outputValue`; SHA-512 of the next pulse's `localRandomValue` equals this `precommitmentValue`). Both links hold on two public chain 1 pulses (section 9.5). The owner may ask for this check later; it is not a condition of approval."""))
E.append(("- **The approved policy record** (`SEED_POLICY_V1`, `APPROVED`) binds the verified value, the pulse's `uri` and `pulseIndex`, who fetched it and when, and who verified it and when.",
"- **The approved policy record** (`SEED_POLICY_V1`, `APPROVED`) binds:\n  - the exact accepted `outputValue`, the pulse's `uri`, `pulseIndex`, `timeStamp`, `statusCode` and `certificateId` as published;\n  - the source (the two HTTPS addresses read) and the SHA-256 of the owner's saved file;\n  - who fetched it and when, and who verified it and when;\n  - `signature_verification: NOT_PERFORMED`, the trust basis (NIST's official HTTPS service; WF1-12), and the reference to NIST's notice of 23 October 2026.\n\n "))
E.append(("- **Switching:** you may replace the root at any time. A new root is a new policy ID; earlier policies and their reports are kept.",
"- **Switching (D-10 as ratified; confirmed by the owner, 30 October 2026):** the 6 November value is N1's single root unless you later replace it. A replacement is never a quiet substitution: it is a new policy ID with its own pulse, announced in `exchange/` before that pulse exists, approved by the same procedure. Earlier policies and their reports are kept. There is no automatic replacement for a refused pulse either."))
# 9: new 9.5
E.append(("""## 10. Tests (per package; synthetic only)""",
"""### 9.5 Added for v0.1r1 (EX_078 WF1-R3-C04 and C01)

`probe_tails.py` (output `ev_wf1_tails.txt`) and `probe_numerics2.py` (output `ev_wf1_numerics2.txt`), fair-draw arithmetic only:
- **The two tail routes,** with the switch at z/sqrt(2) = 5: they agree to a relative 1.7e-47 on [5, 6]. The continued fraction does not change between 400 and 4000 terms at x = 5, 8, 20 and 45. (With v0.1's switch at 3, the overlap on [2.5, 3.5] agreed only to 2.6e-11, which is why the switch moves.)
- **Large sigma:** ln Q(z) agrees with an independent asymptotic series to 1.95e-17 absolute for z = 12 to 60.
- **Extreme and boundary tails:**

  | p | sigma | Q(sigma)/p - 1 | time |
  |---|---|---|---|
  | 1e-300 | 37.0470962993612 | 2.8e-14 | 0.1 s |
  | 1e-700 | 56.68955328257109 | 1.8e-13 | 0.1 s |
  | 1/2 - 1e-20 | 2.5066282746310004e-20 | 4.3e-37 | 6 ms |
  | 1/2 | 0 (exact rule) | 0 | 0 |

  The float64 rounding of sigma accounts for the residuals.
- **MRT-04 sizes,** exact, on the shorter side:
  - n = 5000, p = 1e-9: P(X >= 40) is 10^-260.021 (0.09 s) and P(X >= 3) is 10^-16.682 (0.03 s);
  - n = 5000, p = 51597/3362260: P(X >= 120) is 10^-5.610 (0.13 s).

  Summing the long side, as the first probe did, took about 180 s for the same values.
- **MR7's exact null:** 2.1 s at n = 432 and 23.7 s at n = 1000, hence the bound of 6.6.
- **NIST chain links,** on public chain 1 pulses 1705577 and 1705578: SHA-512 of the next pulse's `localRandomValue` equals the earlier pulse's `precommitmentValue`, and the next pulse's `previous` equals its `outputValue`. Both hold. No certificate is needed (section 8.2: available, not proposed).

## 10. Tests (per package; synthetic only)"""))
# tests
E.append(("""- **Resume after a simulated interruption:**
  - no folder is touched;
  - `INTERRUPTED` and `PUBLICATION_FAILED` pairs run again; others do not.
- **A runner refusal stops the batch at once.** A method failure is counted and the batch goes on.""",
"""- **Resume after a simulated interruption:**
  - no folder is touched;
  - pairs with no terminal record, `INTERRUPTED`, `PUBLICATION_FAILED` or `DATA_ADMISSION_REFUSED` run again; CONTINUE-class pairs do not.
- **The STOP rule (B01), each with zero runs after the stop:**
  - a runner refusal;
  - **an invented master changed after the plan,** so that dispatch admits the request but the reader refuses the pin (`DATA_ADMISSION_REFUSED`). The test counts zero target executions after it, and on resume with the cause still present, exactly one attempt and a stop;
  - an orphan marker created between two targets;
  - an exception escaping the runner (a run folder that cannot be created; a terminal record that cannot be written);
  - Ctrl-C before the run folder exists;
  - an unknown reason prefix (fails closed).
- **CONTINUE:** a method failure, an invalid output and a valid empty target are each counted, and the batch goes on.
- **Start-of-run checks:** a changed active entry, a changed declaration, or a flag added after the plan refuses the invocation before any run.
- **Plan (O01):** a `SUPPORTED` entry with its flag present is refused at `plan`, by name."""))
E.append(("""  - a refusal not stopping the batch;
  - the plan written after the first run.""",
"""  - a refusal not stopping the batch;
  - `DATA_ADMISSION_REFUSED` classified as CONTINUE;
  - an unknown reason classified as CONTINUE;
  - the plan written after the first run."""))
E.append(("""- **the search log:** one row per run of each type;
- **mutation checks.**""",
"""- **the search log (C02):** the `RANKING_REPORT` row precedes the first outcome read (an instrumented reader); a failure injected after outcomes are read leaves the row in place, and the next report counts it as an attempt without a report; a crash injected between the row and the scoring plan is counted the same way; a refused invocation appends nothing; one row per driver `plan`;
- **the downgrade rules (C03):** a synthetic family of 79 complete tracks and 1 track with a failed cell gives `BONFERRONI_REFERENCE_UNCALIBRATED` with M = 80 and the failed track listed; a complete 80-track grid gives the guaranteed label; an empty track gives `MR_INSUFFICIENT_DATA` and keeps M = 80; a `REPRODUCIBILITY_FAIL` cell makes its track `GRID_INCOMPLETE`; an incomplete track leaves other tracks' local labels unchanged; the common-set table turns `SELECTION_UNVERIFIED`;
- **the numerics (C04):**
  - MRT-04 at n = 5000 with p down to 1e-9, including tails below 1e-300;
  - sigma at p = 1e-300 and 1e-700, near and at 1/2, against the asymptotic oracle;
  - `P_BELOW_FLOAT64_RANGE`, `SIGMA_ABOVE_BOUND` and `MR_EXACT_BOUND_EXCEEDED` each produced and labelled;
  - the two tail routes agree on their overlap;
- **the seed policy record (WF1-12):** an `APPROVED` record without `signature_verification`, the file SHA-256, the `certificateId` or the two source addresses is refused; a lower-case or wrong-length `outputValue` is refused;
- **N1's word convention:** SHAKE-256 words are unsigned 64-bit little-endian (a test pins the published first word);
- **mutation checks.**"""))
# 12
E.append(("- **WF1-6 (RECOMMENDED): own-set grids, and the two MR7 families** (sections 6.2 and 6.7). The options: R3's default intersection (Oz Lotto: 12 draws); other or extra families, for example your own MR4 sets C.3, B.2-3 and X.3 as a calibrated family (they are always computed and shown in any case).",
"- **WF1-6 (OWNER-DECIDED 30 October 2026, subject to the review): own-set grids, and the two MR7 families** (sections 6.2, 6.2A and 6.7). The owner agreed to the departure from R3's default intersection set. The options not chosen: R3's default intersection (Oz Lotto: 12 draws). Other or extra families remain possible, registered before first use; for example your own MR4 sets C.3, B.2-3 and X.3 (they are always computed and shown in any case)."))
E.append(("- **WF1-9 (YOUR CHOICE): N1's beacon pulse.** Recommended: the pulse at `2026-11-06T00:00:00.000Z` (section 8.1). The option: any later whole minute you prefer, recorded in `exchange/` before it arrives.",
"- **WF1-9 (YOUR CHOICE): N1's beacon pulse.** Recommended: the pulse at `2026-11-06T00:00:00.000Z` (section 8.1); the owner and the reviewer have both said to keep it. The option: any later whole minute you prefer, recorded in `exchange/` before it arrives. Under D-10, as the owner confirmed on 30 October 2026, any later replacement is a new pre-announced policy, with every root kept and counted."))
E.append(("- **WF1-11 (RECOMMENDED): template finding T-1** goes into draft 4 at the next method package (wave 3).",
"- **WF1-11 (RECOMMENDED): template finding T-1** goes into draft 4 at the next method package (wave 3).\n- **WF1-12 (OWNER-DECIDED 30 October 2026, after EX_078 C01): the seed's trust basis is NIST's official HTTPS service.** The pulse's signature and certificate are not validated (`NOT_PERFORMED`), and NIST's certificate notice of 23 October 2026 does not block approval. D-9's two-person check stays: the owner fetches the pulse by hand, and Claude independently reads it from NIST's archive and compares the five fields. The owner accepts the residual authenticity risk (section 8.2). D-9 to D-11 are unchanged. The options not chosen: require a signature check (approval would wait for NIST's corrected certificate), or drop the second read as well (an amendment of E2R-R63 stage 2)."))
# 13
E.append(("## 13. What the reviewer is asked to check (R-3)\n",
"## 13. What the reviewer is asked to check (R-3)\n\n**For the focused RECHECK of v0.1r1:** whether each EX_078 finding is resolved (Appendix A): the STOP classification table and its fail-closed default (5.3); the trust-basis wording and policy fields (8.2, 8.3); the search-log order (6.1); the downgrade rules (6.2A); and the numerics wording and bounds (6.6, 9.5). The eight original items follow.\n"))
E.append(("The gates and the orphan-marker rule apply unchanged.\n",
"""The gates and the orphan-marker rule apply unchanged.

## Appendix A. Resolution of EX_078

| Finding | Class | Resolution in v0.1r1 |
|---|---|---|
| WF1-R3-B01 source-admission failures continued | BLOCKER / RECHECK | 5.3: the STOP rule classifies the terminal **reason** and fails closed. `DATA_ADMISSION_REFUSED`, `PUBLICATION_FAILED`, `INTERRUPTED`, escaping exceptions and unknown reasons STOP; only `METHOD_FAILED`, `CONTRACT_REFUSED_OUTPUT`, `NO_TICKET_NO_DIAGNOSTIC` and `PUBLISHED` continue. It adds start-of-run registry checks, the mid-batch marker case, the no-terminal and no-segment cases, and resume while the cause persists (at most one failed attempt). The installed runner is unchanged. Tests in section 10, including the changed-master test with zero subsequent runs |
| WF1-R3-C01 NIST certificate notice; meaning of verification | CORRECTION / RECHECK | 8.1 trust-basis row; 8.2 states what is and is not verified, records NIST's notice and the residual risk, and keeps D-9's second-person check; 8.3 adds the policy fields (`certificateId`, file SHA-256, sources, `signature_verification: NOT_PERFORMED`). Owner decision WF1-12. The announced pulse is unchanged |
| WF1-R3-C02 search-log write too late | CORRECTION / RECHECK | 6.1 step 4: the `RANKING_REPORT` row (attempt ID, scope, grids, families, declared tests, scoring-plan digest) is appended before the scoring plan and before any outcome is read. Unfinished attempts stay counted and are reported. Tests in section 10 |
| WF1-R3-C03 own-set Bonferroni eligibility | CORRECTION / RECHECK | 6.2A: track statuses `GRID_COMPLETE` / `GRID_INCOMPLETE` / `GRID_EMPTY`; the family's roster and M are fixed; the guaranteed label only with all M tracks complete and `EXACT_LOCAL` and registration before first use; otherwise `BONFERRONI_REFERENCE_UNCALIBRATED`; the common-set table goes `SELECTION_UNVERIFIED` table-wide. Tests: 79 + 1, complete 80, empty, reproducibility failure |
| WF1-R3-C04 "exact everywhere" overstated | CORRECTION / RECHECK | 6.6 reworded: exact integer and rational counts and tails; deterministic bounded-accuracy decimal transforms (1e-30 relative budget); once-only float64 output with `log10` text. It adds `P_BELOW_FLOAT64_RANGE`, `SIGMA_ABOVE_BOUND` and the MR7 bound (n <= 1000, else `MR_EXACT_BOUND_EXCEEDED` with a labelled approximation). Byte identity is a design property, to be tested. The route switch moves to 5 (9.5). Extreme-tail and MRT-04-size evidence is in 9.5 |
| WF1-R3-O01 plan-time flag check | OPTIONAL | Adopted (5.2) |
| WF1-R3-O02 batch and report windows | OPTIONAL | Adopted (5.6 table; 9.1 timing labelled planning evidence) |
| Item 5 note: SHAKE word sign and root case | (in item 5) | Unsigned 64-bit little-endian words; upper-case hexadecimal root, as published; both pinned by tests (section 10) |
"""))

for old, new in E:
    n = t.count(old)
    assert n == 1, (n, old[:90])
    assert all(ord(c) < 128 for c in new), old[:60]
    t = t.replace(old, new)
assert all(ord(c) < 128 for c in t)
open(out, 'wb').write(t.encode('ascii'))
print(out, hashlib.sha256(t.encode()).hexdigest(), len(t.splitlines()), 'lines', len(E), 'edits')
