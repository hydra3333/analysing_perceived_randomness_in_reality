# OUTLANDISH_01 — Mathematical Constants Digit Search
## Standalone project handover and working experiment specification — v0.1

**Status date:** 5 November 2026 (Australia/Adelaide)  
**Purpose:** Enable a new, separate ChatGPT conversation to continue this *mathematical-constants digit-search thought experiment* with the owner's actual software, evidence, preferences and unresolved questions, without inheriting responsibility for the unrelated principal randomness-research development/review.  
**Status:** Powerball FIXED2 scanner and 10^9-digit pi/golden-ratio workflow demonstrated on the owner's Windows PC; 10^10 generation **blocked by y-cruncher's Windows disk-swap administrator requirement**; alternatives not yet resolved. Oz Lotto and alternative compact encodings are *not implemented*.  
**Authority:** This is an as-built handover plus a **draft** forward specification. Do not treat proposals as tested capabilities, and do not modify any main-project procedures on its authority.

---

## 0. First-read summary: what the owner wants

The owner proposed an intentionally unconventional, exploratory exercise: generate long decimal-digit sequences of mathematical constants, encode each digit as an unsigned byte with value 0–9, and search those sequences for representations of real Australian Powerball and Oz Lotto historical winning results. Record **which historical draws and prize-pattern categories appear, the exact digit positions, and whether occurrences for consecutive draws W and W+1 have interesting positional relationships**. First test throughput at 10^6 digits, then 10^9, 10^10, perhaps 10^11 and 10^12 if resources permit. Consider alternative compact/combination-index representations later. This is an experiment in computational feasibility and exploratory relationships, **not a claim that historical matches predict future draws**.

Important owner choices:

- Use **actual draw histories**, not invented/hard-coded sample draws, for the real searches; preserve operator-reported draw order. Keep the games strictly separate.
- Work only from an isolated **pre-holdout development CSV copy**. Do not read or use holdout and later draw outcomes, or modify the authoritative master files.
- Current ball format is **FIXED2**: every lottery ball uses two decimal digits (`3` -> `03`, `12` -> `12`). The constant files, by contrast, hold **one numerical decimal digit per byte** (`3` -> byte `0x03`, not ASCII `0x33`). Allow a later change to natural-width representation (`3` -> `3`) through an explicit, separately tested format version; that variant is **not supported by the active scanner**.
- Scan at every possible decimal-digit offset, including odd offsets and matches spanning chunk boundaries.
- Keep the **searcher single-threaded** for now. A later owner request changed **constant generation only** to `--threads N`, **default 4** (y-cruncher task decomposition, not guaranteed exact OS worker-thread count).
- Use periodic progress/status diagnostics; record throughput, memory where practical, file sizes, checksums and detailed match/transition outputs.
- Prefer normal (non-administrator) Windows operation. The owner does **not** want to elevate y-cruncher merely to run disk-swap mode.
- Eventually support the additional mathematical constants the owner selected from GAIS's list: **1=e**, **2=ln(2)**, **4=Euler–Mascheroni gamma**, **8=lemniscate constant**.
- Automatically clean up **large owned intermediate digit-text/scratch files only after the final binary has been converted and verified**; retain small generation evidence. Never delete on error.

A careful next chat should not reinterpret this as part of the main project's approved method catalogue, workflow or experiment-governance pipeline. It is currently a **standalone side investigation** that happens to reside in a subfolder of that Git working tree and to use an explicitly isolated historical-data export.

---

## 1. Origins and intended scientific questions (original draft, not retrofitted)

The owner's original source is `0_outlandish_thought_experiment_01_scope.txt` (included in the companion handover ZIP). Its initial goals:

1. Generate digit files for pi and the golden ratio, initially M=10^9 digits, with a small T=10^6 performance trial, one digit encoded as one 0–9 byte. Estimate runtime extrapolations.
2. **Powerball**, seven main balls from 1–35 in drawn order, plus a Powerball from 1–20:
   - **P1 / proposed Division-1 pattern:** all seven main numbers in drawn order, followed by the Powerball.
   - **P2 / proposed Division-2 pattern:** seven main numbers in drawn order, without the Powerball.
   - **P3 / proposed Division-3 pattern:** any six of the seven main numbers in **any order**, followed by that draw's Powerball.
   - Generate consolidated searchable patterns with references back to their draw numbers and P category; find *all* occurrences and positions in each constant.
   - For each consecutive historical draw pair W and W+1, examine positions of W's **P1** occurrences against W+1's P1/P2/P3 occurrences, and report any relevant counts/statistics. The intention was to examine *positions and relationships*, not merely whether both draws have a match somewhere.
3. **Oz Lotto** (separate, future program): seven main drawn numbers plus three supplementary numbers, all from 1–47, with proposed patterns:
   - **O1:** seven main numbers in drawn order;
   - **O2:** any six main numbers and any one supplementary number (the exact ordering/permutation semantics **still need explicit specification and tests**);
   - **O3:** any six main numbers (likewise clarify order assumptions);
   - find all positions and investigate W to W+1 in its own data, never pooled with Powerball.
4. Later evaluate a **Representation 2 / Combination Index / Compact Encoding** or similar approach for both games. This is only a research direction, not a finished format or code.

**Terminology warning:** P1/P2/P3 and O1/O2/O3 are the owner's *experimental search-pattern labels*. Do not silently substitute the official lottery division win criteria or treat finding a pattern as actually winning a ticket. The owner deliberately chose specific drawn-order and permutation rules. If official prize-rule comparisons are useful later, keep them as a separate, explicitly labelled study.

### What does a hit mean?

The first digit of the integer part is present (pi starts `3`, phi starts `1`); then digits follow continuously with the decimal point **omitted** in `.bin`. Given the FIXED2 encoding, a P3 pattern has 14 digit-bytes and P1 has 16. A match at `start_digit_offset_0_based = k` means those exact numeric-byte values occur at offsets `k..k+length-1`, where `0` is the leading integer digit. Positional arithmetic must use this convention consistently.

A pair of historic draws both occurring as P3 patterns in the same constant is *not* a prediction by draw W of draw W+1. No tested mapping from W's position to W+1's position or winning numbers exists yet.

---

## 2. Physical location, software and dependencies

Owner's Windows 11 workspace (as reported):

```text
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\src\GAIS\OUTLANDISH_01\
```

Project's master (DO NOT read directly during a normal scan):

```text
E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\source_data\POWERBALL_results_master.csv
```

The preparation command **already executed** by the owner created `POWERBALL_preholdout_only.csv` next to the scripts. It extracted and validated **433 consecutive eligible Powerball draws, 1144 through 1576**, stopping on draw number >=1577 before parsing its other fields. The ordinary scanner reads **that copy**, not the master. The CSV schema is exactly:

```csv
Draw_Number,Date,Drawn_1,Drawn_2,Drawn_3,Drawn_4,Drawn_5,Drawn_6,Drawn_7,Powerball
```

Date is ISO `YYYY-MM-DD`; main balls retain operator-reported order. Do not upload the full source master, invent histories, run the project's retired GAIS fetcher, or bypass the cutoff. The actual CSV copy is **not** included in the portable handover bundle, but is on the owner's PC.

Environment recorded in user logs:

- Windows 11, Command Prompt with activated `...\analysing_perceived_randomness_in_reality\.venv` (the user calls `..\..\..\activate_venv.bat` from `OUTLANDISH_01`).
- AMD **Ryzen 9 3900X**, 12 physical cores / 24 logical processors, **32 GiB RAM**.
- NumPy **2.5.4** reported by `python -c "import numpy; print(numpy.__version__)"`.
- y-cruncher **v0.8.7 build 9547**, installed locally as `y-cruncher v0.8.7.9547b\y-cruncher.exe` with `Binaries\` and constant definitions. Not a Python package.
- User originally requested Python 3.15.2; **the interpreter's actual `python --version` in this side experiment has not been supplied**. Obtain that if version-specific problems arise rather than guessing.
- The generator uses standard-library Python modules plus installed local y-cruncher. The scanner requires **NumPy**. No original `pyahocorasick` dependency remains in the replacement scanner.

**Portability:** This is not yet a separate Git repository. A future move to its own folder/repository may be useful, but must preserve the local dataset-copy boundaries and existing binary paths; do not relocate files without owner's approval. Keep large `.bin` files, y-cruncher outputs and copied draw CSVs out of Git.

---

## 3. Exact current binary format and search implementation

### 3.1 Constant files

- File contains **N bytes for N digits**, no header or decimal-point byte, no packing or compression. Each byte's numeric value is between 0 and 9 inclusive.
- Example first ten bytes of pi: `[3,1,4,1,5,9,2,6,5,3]` and phi: `[1,6,1,8,0,3,3,9,8,8]`.
- `digits_pi_10_to_9.bin` and `digits_golden_ratio_10_to_9.bin` each have exactly **1,000,000,000 bytes**.
- Source text files from y-cruncher contain N digit characters plus a decimal point (observed **N+1** bytes in the 10^6 and 10^9 trials); strict conversion removes the point and stores digit numeric byte values.
- Later constants with leading integer zero such as `ln 2` and gamma also **retain that leading `0` digit**.
- All input windows are prefixes from the integer digit, not arbitrary digits starting farther down the constant. `--max-bytes` can limit the current scanner to a prefix for benchmarking.

### 3.2 Lottery balls and P patterns

Current format identifier: **FIXED2**. Examples: `3 -> [0,3]`, `12 -> [1,2]`, seven main balls yield 14 bytes, P1 including Powerball yields 16 bytes. Every decimal-digit starting offset is eligible (including odd offsets); numeric values do not have to form a globally aligned partition into two-digit balls.

`outlandish_powerball_stage_a.py` (latest package: **1e10 Pipeline v2**) uses **single-threaded NumPy vectorised, chunked scanning**, not `mmap` and not an Aho–Corasick automaton. The program is bounded-memory by its configured chunk size (`--chunk-bytes`), with overlap/edge logic to find matches crossing chunk boundaries. It screens candidate positions and matches:

- P1 key: exact ordered tuple of 7 mains + PB;
- P2 key: exact ordered tuple of 7 mains;
- P3 key: **sorted six-main-number combination plus exact PB**. For each draw there are 7 choices of the omitted main number and 6! permutations, so **7 × 720 = 5,040 logically accepted sequences**. The index stores only the 7 unordered combinations per draw (coalescing duplicate keys across draws and retaining draw attribution), but **still recognises all 5,040 orders** at scan time. At 433 draws the observed index contained 433 P1 keys, 433 P2 keys and 3,030 unique P3 keys.

The reported `candidate_starts_examined` is the number passing a preliminary range filter, **not** the number of draws searched, digit offsets scanned, or actual matches. At 10^9, it was 642,075 for pi and 644,210 for phi. Full digit-offset coverage is intended and was exercised by planted synthetic tests, including chunk boundaries and end-of-file.

Matches are saved in CSV, including constant identifier, draw number, P category, **zero-based start offset**, exclusive end offset and matched decimal digit text. Separate transition CSV and JSON summaries are written. Full scanned-prefix SHA-256 is computed during the scan; it agreed with the verified billion-byte binary SHA-256 values.

**Format-switch caution:** A function in the code can *encode* natural-width balls, but the current vectorised scanner, pattern lengths and filters assume FIXED2. There is **no working `--encoding natural` mode**. Supporting it later requires a distinct versioned end-to-end search implementation and self-tests, not merely changing one helper.

### 3.3 Original GAIS program — superseded

- `generate_and_convert_10_to_6.py` generated pi using downloaded text from a public MIT-hosted pi source and phi through Python big-integer square roots. The resulting 10^6 `.bin` files passed prefix checks, but this is *not* the large-scale generator.
- Original `powerball_search.py` used **11 hard-coded sample draws**, `pyahocorasick`, built/stored up to 5,040 P3 strings per draw, turned numeric-byte streams back into ASCII for matching, reported pattern end positions and offered only a rudimentary transition count. It did **not** read historical CSVs and did **not** implement the proposed positional-correlation analysis. It is superseded; do not run it as the current benchmark or treat its sample draw data as historical evidence.

---

## 4. File inventory and version lineage

These paths describe the owner's workspace as reported in logs, **not an independently refreshed live directory listing**.

| Path/name relative to `OUTLANDISH_01` | Role/status |
|---|---|
| `0_outlandish_thought_experiment_01_scope.txt` | **Original owner concept**, preserve unmodified. |
| `Potential_Other_constants.txt` | GAIS's candidate-constants discussion; owner selected list numbers 1, 2, 4, 8. Claims/CLI command names from it are hypotheses until tested against the installed y-cruncher. |
| `outlandish_big_constants.py` | **Active v2 generator/converter/verifier/pipeline**, in `OUTLANDISH_01_1e10_Pipeline_v2.zip`. |
| `outlandish_powerball_stage_a.py` | **Active v2 Powerball scanner** (new constant-prefix support; core scan unchanged). |
| `OUTLANDISH_01_1e10_README.md` | Detailed active v2 usage. |
| `generate_1e10.cmd` / `scan_1e10.cmd` | v2 convenience commands (only if extracted/installed). |
| `POWERBALL_preholdout_only.csv` | Owner's local 433-draw isolated CSV; do not embed in portable public repo. |
| `digits_pi_10_to_6.bin`, `digits_golden_ratio_10_to_6.bin` | Original 1,000,000-byte numerical references. |
| `digits_pi_ycruncher_smoke.bin`, `digits_golden_ratio_ycruncher_smoke.bin` | Extra 10^6 regenerated/verifiable smoke binary copies; redundant for searching. |
| `digits_pi_10_to_9.bin`, `digits_golden_ratio_10_to_9.bin` | **Current verified 1,000,000,000-byte** numerical-digit datasets, retained. |
| `ycruncher_digits/` | Generation output subfolders; v2 deletes owned large text/scratch after **successful** pipeline verification and retains small logs; failure folders remain. |
| `OUTLANDISH_01_results/run_20261105_231343/` | Actual 10^9 pi/phi scan outputs, including `_matches.csv`, `_transitions.csv`, `_summary.json`, `run_summary.json`. Compact copy: `run_20261105_231343.zip`. |
| `OUTLANDISH_01_Stage_A_v1.zip` | First Powerball scanner, plus `convert_constant_ascii_to_bin.py` and Stage A README. Historical package. |
| `OUTLANDISH_01_1e9_Pipeline_v1.zip` | Initial y-cruncher automation. Historical, superseded. |
| `OUTLANDISH_01_1e9_Pipeline_v1r1.zip` | Fixed y-cruncher output location by running in the intended output folder. Historical, superseded by v2. |
| `OUTLANDISH_01_1e10_Pipeline_v2.zip` | **Latest supplied software package**; includes both current Python scripts, README, generation/scan `.cmd` wrappers. |
| `ARCHIVE/`, original `Pi - Dec - Chudnovsky.txt`, timestamped validation logs | Historical/manual files seen in owner listings, not necessarily still present. Inspect before removal; don't conflate them with the v2-managed output directory. |

**Suggested new-chat material:** attach the handover bundle (contains the active v2 source, original owner scope, constants candidates, compact measured-results ZIP) and keep the 1-GB/10-GB binaries on the owner's PC. Attach actual run logs or source files again if a later revision replaces v2. The companion bundle does **not** contain the large numeric binaries or private draw CSV.

---

## 5. Verified real tests and outputs as of 5 November 2026

### 5.1 At 10^6 digits

- Two 1,000,000-byte pi/phi files existed; first ten numeric bytes and initial 32-digit prefixes passed.
- The owner prepared 433 eligible draws via `prepare`; the scanner's synthetic P1/P2/P3 self-test passed, including cross-chunk, odd-offset and EOF cases.
- Both constant scans processed **all 1,000,000 bytes** and found P1=0, P2=0, P3=0, as expected given very low match probability.
- Measured scan times: pi **0.023 s**, phi **0.027 s** (startup effects mean not a reliable long-range performance predictor alone).
- y-cruncher independently regenerated 1,000,000 pi digits using Chudnovsky (0.222 s reported internal wall time), converted and compared all one million bytes **identically** to the reference. Golden ratio via Newton (0.133 s internal wall), similarly regenerated and compared (the owner reported both smoke binaries). y-cruncher originally wrote the pi output to the wrong working directory in v1; fixed with v1r1; see §7.

### 5.2 At 10^9 digits — completed

- y-cruncher v0.8.7 generated both constants, with internal output verification. Golden ratio: **62.015 seconds internal start-to-end wall**, 4.18 GiB logical RAM, single-thread. Pi completed too; **its actual billion-digit generation duration is not recorded in the material available here**; do not invent it.
- Numerical-byte conversion + independent full-file reread verification passed for both.
- Full prior **one-million-digit prefix** agreed in each case.
- Pi: convert **13.4 s**, verify **8.9 s**, SHA-256 **`2e633867ad0ed7d866bcc0b3defc29b7704d0808cf62bba1dee1935fc357316e`**.
- Phi: convert **12.5 s**, verify **8.8 s**, SHA-256 **`6be7059e971a6c710074682bfac76d415d1eff32c310bdb32c3c91283238d6d8`**.
- Powerball scan used the real 433-draw CSV (1144–1576), FIXED2, NumPy, **4,000,000-byte chunks**, single-thread, and time-gated progress approximately every 5 seconds.

| Metric | Pi 10^9 | Golden ratio 10^9 |
|---|---:|---:|
| Numeric digit bytes searched | 1,000,000,000 | 1,000,000,000 |
| P1 matches | 0 | 0 |
| P2 matches | 0 | 0 |
| **P3 occurrences** | **29** | **25** |
| Preliminary candidate starts | 642,075 | 644,210 |
| Scan elapsed | **27.598385 s** | **27.871085 s** |
| Scan throughput | **36.234 MB/s** | **35.879 MB/s** |
| Draw pairs considered | 432 | 432 |
| Adjacent-draw pairs where both have *any* match | 3 | 2 |
| W P1 to W+1 any transitions | **0** | **0** |

The **54 combined P3 occurrences** are not necessarily 54 distinct draws, and they are not predictions. Historical consecutive pairs having a P3 somewhere in the same constant were:

| Constant | W → W+1 | Start offsets W, W+1 (zero-based) | Signed delta W+1 minus W |
|---|---|---|---:|
| Pi | 1195 → 1196 | 974,512,578 ; 803,790,670 | -170,721,908 |
| Pi | 1470 → 1471 | 769,827,143 ; 491,947,932 | -277,879,211 |
| Pi | 1490 → 1491 | 17,628,072 ; 564,308,006 | +546,679,934 |
| Golden ratio | 1233 → 1234 | 655,598,637 ; 722,416,094 | +66,817,457 |
| Golden ratio | 1552 → 1553 | 102,146,164 ; 901,318,284 | +799,172,120 |

**Critical interpretation:** P1 was never found, so the owner's *original P1-anchored positional correlation test* has **no observations**. The five P3/P3 adjacent-draw cases are exploratory observations with no demonstrated position-to-position mechanism. The current `_transitions.csv` does **not** calculate P3→P3 positional deltas; the table above was derived from the actual match CSVs. Do not attribute a predictive relationship.

### 5.3 Why sparse matches are expected

For a convenient *uniform independent decimal-digit reference model* (not an assertion that pi/phi digits are independently random), about 433 draws give a rough P3 mean of `433 × 5040 × N / 10^14` occurrences per constant, neglecting dependencies/collisions and stream ends. At N=10^9, this is **21.82**, consistent with seeing 29 and 25. P1 rough mean is `433 × N / 10^16`; P2 is `433 × N / 10^14`. Even at 10^12 digits P1 expectation is only about **0.043 per constant**. Therefore zero P1 is entirely expected and larger windows do not guarantee one. Explain this honestly without dismissing the user's interest in unusual exploratory relationships.

### 5.4 Linear **scan-only** projections from actual 10^9 timing

| Digits per constant | Numeric binary size per constant | Pi extrapolation | Phi extrapolation |
|---|---:|---:|---:|
| 10^6 | 1 MB (0.954 MiB) | Actual 0.023 s | Actual 0.027 s |
| 10^9 | 1 GB (0.931 GiB) | **Actual 27.60 s** | **Actual 27.87 s** |
| 10^10 | 10 GB (9.313 GiB) | ~4.60 min | ~4.65 min |
| 10^11 | 100 GB (93.132 GiB) | ~46.0 min | ~46.5 min |
| 10^12 | 1 TB (931.323 GiB) | ~7.67 h | ~7.74 h |

These **exclude generation time, y-cruncher scratch, text-to-binary conversion, reread verification and OS/disk effects**. The extrapolations are tentative, particularly at 10^11–10^12. Two 10^12 binaries alone require 2 TB; the owner's E: drive had about **909 GB free** following the billion-digit runs, so 10^12 is infeasible there without additional capacity or changed storage strategy. Two 10^11 binaries require 200 GB, plus text and scratch space.

---

## 6. Latest generator (v2): intended end-to-end behaviour and commands

### 6.1 Supported commands and parameters

`outlandish_big_constants.py` provides `self-test`, `generate`, `pipeline`, `inspect`, `convert`, and `verify`.

- `pipeline --constant <pi|phi|e|log2|gamma|lemniscate|both> --digits N [--threads K] [--mode auto|ram|swap] [--memory-gib G] [--run] [--keep-text]`
- `--digits` means **total digits including the leading integer digit**; hence y-cruncher is invoked with `-dec:N-1` fractional digits. With `--run` omitted, the command is a **dry-run preview** with no generation or output-folder creation.
- `--threads` defaults to **4**; for `K=1`, y-cruncher gets `-TD:1 -PF:none`. For `K>1`, it gets `-TD:K -PF:taskqueue`. These settings control task-decomposition style, **not a hard four-OS-thread limit**. Owner's y-cruncher 10^10 preflight printed `Task Queue -> 4 / ? / 24 (all cores)`. The **Powerball scanner remains single-threaded**.
- `--mode auto` selects RAM for fewer than 5 billion digits and disk swap for >=5 billion. `--mode ram` is **explicitly refused by the Python CLI at N>=5,000,000,000**, a safety guard introduced before obtaining a measured RAM-only 10^10 estimate. This guard must be reconsidered deliberately if testing RAM-only at 10^10, not silently bypassed.
- Swap mode configures 16 GiB working memory by default, creates an owned `_outlandish_owned_swap` directory, and passes `-mode:swap -M:16g -swap:raid0 <scratch>`; on this Windows installation, swap mode **requires elevation** (see §7).
- `pipeline` generates text, strictly converts digits to a temporary numeric-byte file, publishes create-only binary, independently rereads/verifies byte range and SHA-256, verifies *the entire available previous prefix* (10^9 for a 10^10 pi/phi run), writes `OUTLANDISH_01_verified.json`, then removes owned large text and scratch **only after full success**. Small calculation and validation logs remain. `--keep-text` keeps intermediates.
- No existing output dir or final `.bin` is overwritten. Failures preserve the output dir and source files for diagnosis. In particular a failed attempted 10^10 job is **not equivalent to a successful generation** even if y-cruncher returns exit code 0.
- The converter does not generate digits itself; y-cruncher does. It accepts the observed simple plain-text output of N digit characters plus decimal point (N+1 bytes). Novel/split output formats need deliberate handling; don't blindly feed y-cruncher logs as digit text.

10^10 dry-run (works and was owner-tested):

```bat
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000
```

Proposed run **only after the RAM/swap decision is resolved**:

```bat
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000 --run
python outlandish_big_constants.py pipeline --constant phi --digits 10000000000 --run
```

Proposed scan if both binaries successfully exist and have been verified:

```bat
python outlandish_powerball_stage_a.py scan --draws POWERBALL_preholdout_only.csv --digits digits_pi_10_to_10.bin digits_golden_ratio_10_to_10.bin --chunk-bytes 4000000 --progress-seconds 5
```

**No 10^10 `.bin` files have yet been produced or searched** in the provided evidence.

### 6.2 The four proposed additional constants

| Owner's list no. | CLI name | Constant | y-cruncher identifier in v2 | First digits for checking |
|---|---|---|---|---|
| 1 | `e` | Euler's number | `e` | `2.718281828459...` |
| 2 | `log2` | Natural log 2 | `log:2` | `0.693147180559...` |
| 4 | `gamma` | Euler–Mascheroni constant | `gamma` | `0.577215664901...` |
| 8 | `lemniscate` | Lemniscate constant | `lemniscate` | `2.622057554292...` |

The **v2 source implements** command identifiers and prefix checks for these; all six constants passed synthetic generator/converter self-tests in the owner's environment. **Real Windows y-cruncher generation for these four has not been demonstrated**; the suggested next step for each is a 10^6 smoke run, *not* 10^10 directly. The GAIS source list contains wider physical interpretations that are not evidence of lottery relationships; preserve it as an idea list rather than scientific validation.

Example future smoke command:

```bat
python outlandish_big_constants.py pipeline --constant e --digits 1000000 --run
```

Do the analogous `log2`, `gamma`, `lemniscate` runs individually once desired. Existing 10^9 pi/phi binary reference comparisons are specific to those constants; new constants need to establish their own verified 10^6 references.

---

## 7. Issues encountered: resolved, partially resolved, unresolved

| Issue | Observation | Resolution / current state |
|---|---|---|
| Initial GAIS scanner used fabricated examples | 11 hard-coded draw tuples and no project CSV input | **Resolved for Powerball.** New `prepare` creates safe local copy; scanner used all 433 actual pre-holdout draws. |
| Initial GAIS scanner used per-permutation Aho–Corasick | Up to 5,040 P3 strings/draw; huge index and ASCII intermediate | **Resolved for FIXED2.** NumPy chunk scanner + sorted-six/Powerball index accepts all permutations and retains draw attribution. |
| Early scanner only printed rudimentary W→W+1 counts | No real positional-correlation analysis | **Partially resolved.** Actual start/end positions and summaries captured; P1-anchored deltas would be calculated if P1 existed. Rich, tested P3/P3 positional statistics still **future**. |
| Need large stream without huge RAM | Reading 10^12 digit bytes into Python string infeasible | **Resolved for scanning.** Chunked bounded-memory search; no `mmap` required, but may benchmark later. Generation is separate. |
| Original 10^6 pi source downloaded existing digits; phi used Python huge integer | Works at small scale, not suitable for trillion digits | **Resolved at 10^9.** y-cruncher computation + strict streaming conversion, verified bin; scaling beyond 10^9 not yet proven. |
| Initial y-cruncher command `-o <folder>` did not place pi output there | Pi text appeared in current `OUTLANDISH_01` instead of intended folder | **Resolved in v1r1** by running subprocess with `cwd=out`; tested with phi on Windows. |
| Plaintext is one byte larger than binary | Decimal point included in y-cruncher `.txt` | **Understood**; N+1 plaintext bytes versus N binary digit bytes. |
| Tiny 10^6 scans saw no matches | P1/P2/P3 zero in both constants | Expected; 10^9 scan found **29/25 P3**, demonstrating real matching. |
| Confusion over "consecutive pair" | Earlier possibility to interpret W match as predicting W+1 | **Clarified:** two historic draws each had an independently found P3, no prediction or verified positional rule. |
| Temporary 10^9 plaintext and small reports | About 2 GB redundant source text after verified conversion | Safe manual deletion of large text; preserve small generation logs optionally. v2 adds safe post-verify automatic cleanup. |
| Four threads might mean exactly four OS workers | `-TD:4 -PF:taskqueue` displayed `4 / ? / 24 (all cores)` | **Clarified:** task decomposition 4, not hard Windows thread ceiling. Searcher unchanged single-thread. |
| **10^10 swap-mode attempt** | y-cruncher emitted `Swap mode requires administrator privileges ... SeManageVolumePrivilege`, reported **exit code 0** but no digit output | **UNRESOLVED.** Wrapper correctly rejected the apparent-success exit code because no files were present and performed no cleanup. Owner prefers **not** to use administrator rights. |
| Need 10^10 without swap | Owner asks if RAM-only can be used | **UNRESOLVED.** y-cruncher RAM-only preflight estimate for 10^10 was not obtained. Python v2 blocks RAM at >=5e9. See next steps. |
| Failed 10^10 output directory exists | v2 creates `ycruncher_digits\pi_10000000000_digits` before launching; no digits created | Preserve/inspect any scratch marker/log; **do not force overwrite**. Later safely rename or remove after confirming no live y-cruncher process or valuable files; no automatic deletion of failures. |
| Other constants e, ln 2, gamma, lemniscate | Only code-level support and synthetic tests | **Not yet Windows validated** with real y-cruncher; start at 10^6. |
| Oz Lotto | In original specification | **Not yet implemented.** Need its own trustworthy pre-holdout CSV/schema and explicit O2/O3 permutation semantics. |
| Natural-width balls / compact encoding | Owner wants ability to change format later | **Not implemented** as live scan mode; code is modular enough to plan a separate representation. |

### Exact last 10^10 failure

The owner ran:

```bat
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000 --run
```

y-cruncher's own preflight (swap mode, requested task decomposition 4) said:

```text
Computation Mode:       Swap Mode
Multi-Threading:        Task Queue -> 4 / ? / 24 (all cores)
Logical Memory Needed:  16.0 GiB
Logical Disk Needed:    47.5 GiB + 9.31 GiB for output
Warning: Swap mode requires administrator privileges.
System Exception Encountered: SystemException
Swap mode requires administrator privileges.
Please run y-cruncher as administrator with SeManageVolumePrivilege.
[pi] y-cruncher exit code=0; wall=3.7s
ERROR: y-cruncher exit 0 but no output files; no cleanup performed
```

The **47.5 GiB disk scratch** is y-cruncher's *own temporary files*, **not** Windows `pagefile.sys`. There is no demonstrated non-admin switch to run this Windows swap mode in the installed build. The swap's system privilege is `SeManageVolumePrivilege`; earlier nonfatal `SeLockMemoryPrivilege` warnings during RAM-only jobs are a different matter. Windows paging is **not** a substitute we should rely on for a RAM calculation exceeding physical memory.

---

## 8. Next work, ordered by dependencies

### Immediate blocker: resource planning for 10^10 without elevation

1. **Do not retry the same swap-mode command in an ordinary CMD box**; it is known to fail. Do not request admin elevation as the default solution.
2. Obtain **y-cruncher's real RAM-only logical-memory estimate** for pi at `9,999,999,999` decimal places and desired parallelism, **without starting the calculation**. Interactive `y-cruncher.exe` custom-compute preflight is a known route: select pi, RAM only, decimal places, inspect displayed memory requirement, **do not select Start Computation**. Check phi too if the pi result fits. Do not assume the phi 10^9 4.18 GiB will scale linearly or that pi equals phi. Leave Windows headroom rather than relying on pagefile thrashing.
3. The existing Python v2 **refuses `--mode ram` at >=5e9**; if RAM-only genuinely fits, make a narrowly reviewed adjustment allowing an **explicit opt-in/preflight** rather than silently removing the guard. Preserve create-only outputs, prefix/full-file verification and post-success cleanup.
4. If 10^10 does not fit, discuss with owner a smaller RAM-only target (e.g. 2–4 billion, subject to measured preflight) or the tradeoff of alternative storage/generation setups. Investigate documented options before assuming a chunk-by-chunk independent computation of decimal prefixes is possible. **Owner currently favours no elevation**.
5. Check any failed output directory left by swap attempt before new runs. y-cruncher's exit code zero was misleading; a verified **numeric binary and manifest** are the success criterion.

### Once viable generation is established

6. Generate pi and phi **separately** at the agreed size (generator defaults to `--threads 4`, but that is not a strict worker limit), convert and independently verify full output with old 10^9 prefix; delete only owned intermediates on verified success. Record actual generation, conversion, verify times, memory/scratch and checksums.
7. Search the new numeric binaries with the same **433 pre-holdout-only Powerball draws** and FIXED2 definitions; collect all match CSVs, per-constant transitions and summaries. Evaluate actual sustained throughput vs 10^9 projections.
8. **Analyse historical match positions more substantially:** W and W+1 categorical hits, signed distances, nearest-neighbour distances, ordering, density, duplicate draw matches, multi-hit cases and baseline/null-world comparisons. Preserve exact distinction between the originally requested **P1 anchored** analysis and newly proposed **P3/P3** exploratory analysis. Correct for the immense number of possible relationships and avoid retrofitting a successful rule from chance coincidences.
9. Smoke-test `e`, `log2`, `gamma`, `lemniscate` at 10^6 each with real Windows y-cruncher; separately plan any 10^9/10^10 expansions based on observed compute/memory costs, not GAIS's unverified list.
10. Implement a **separate Oz Lotto program** only after the Powerball pipeline is stable, with real local pre-holdout-only Oz Lotto history, authoritative source schema/order, explicit O1/O2/O3 semantics, planted-match tests and distinct reports. Never combine games.
11. Formally describe and implement **Representation 2 / Compact Combination Index** only after choosing a reversible, unambiguous encoding with independent reference examples. New representation IDs must be prominent in output/report headings and not silently change existing FIXED2 results.
12. Consider `mmap`, larger chunks, lower-overhead I/O or multi-thread/multi-process scanning **only if actual sustained scan performance justifies it**. The owner explicitly requested single-thread scanning for now. Hard memory/disk numbers and accurate timing matter more than complexity for its own sake.
13. A future actual predictive test, if one is ever proposed, requires a **predefined mapping** from information known at W to a forecast of W+1, **strict time-direction/N-1 and independent unseen evaluation**; the present retrospective scan is *not* that.

### Acceptance checks for any later release

- Constant generation fails closed on bad output format, wrong length, wrong known prefix, prior-prefix mismatch, SHA mismatch or reused destination; **never cleans up on failure**.
- Separate full-file reread verify and hashes; write a durable manifest before deleting plaintext; maintain bounded memory.
- Scanner refuses invalid numeric digit bytes, invalid CSV or excluded draw rows **before reading their restricted winning fields**; preserves actual draw identifiers and operator order.
- Planted synthetic P1/P2/P3 matches cover all permutations expected, odd offsets, overlaps, chunk boundaries and EOF; compare optimized results against a small exhaustive reference on synthetic data.
- Scan receipts identify constant, digit count, encoding version, draw range/count, scanned SHA-256, detailed positions, match category and exact measurement boundaries.
- Failures and interruptions are diagnosable; no background tasks, silent retries, downloading lottery results or main-project modifications.

---

## 9. Practical command reference (current v2; paths relative to `OUTLANDISH_01`)

```bat
REM Activate existing Python venv (if not already active)
call "..\..\..\activate_venv.bat"

REM Confirm installed versions
python --version
python -c "import numpy; print(numpy.__version__)"

REM Harmless self-tests; no real draw data opened
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test

REM Already completed historically; do NOT overwrite existing local copy
REM python outlandish_powerball_stage_a.py prepare --source "..\..\..\source_data\POWERBALL_results_master.csv"

REM Re-run EXISTING 10^9 scans using current local pre-holdout-only CSV
python outlandish_powerball_stage_a.py scan --draws POWERBALL_preholdout_only.csv --digits digits_pi_10_to_9.bin digits_golden_ratio_10_to_9.bin --chunk-bytes 4000000 --progress-seconds 5

REM Dry-run 10^10 generator (no calculation; swap-mode preview by default)
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000

REM Example small new-constant smoke test (real generation on owner's PC)
python outlandish_big_constants.py pipeline --constant e --digits 1000000 --run

REM Inspect options
python outlandish_big_constants.py --help
python outlandish_big_constants.py pipeline --help
python outlandish_powerball_stage_a.py scan --help
```

**Operational note:** A terminal path like `E:\...\OUTLANDISH_01\` may contain other older scripts. Use **the active v2 file names above**; do not accidentally run the original `powerball_search.py` with fabricated examples.

---

## 10. What the next chat should and should not assume

**Known:** Original owner concept, files, currently implemented code, 433 real development draws, 10^9 verified pi/phi binaries, actual scan receipt and CSV evidence, 10^10 failed swap preflight, four additional constants requested, owner's no-admin preference and generator four-way task decomposition default.

**Not known/verified:** Current exact live `OUTLANDISH_01` directory after any cleanup, owner's actual Python version, pi 10^9 generation runtime, RAM-only 10^10 y-cruncher estimate, whether a non-admin swap workaround exists in the installed binary, real Windows generation success for the four extra constants, 10^10 results, Oz Lotto data schema/availability, or any prospective predictive method. Do not invent these.

**Suggested new-chat opening request** (the owner may paste this):

> This ZIP contains `OUTLANDISH_01` standalone mathematical-constants digit-search handover v0.1, current v2 source, original scope, selected extra-constants list and the real 10^9 Powerball results archive. Please read the handover and the latest source. This is a separate project and does not authorise access to my primary randomness project's holdout or new draw data. First confirm your understanding of current P1/P2/P3, FIXED2, the verified billion-digit results, and the unresolved no-admin 10-billion-digit RAM/swap issue. Then recommend the least intrusive way to measure y-cruncher's **RAM-only** memory requirement for 10^10 without starting a calculation or bypassing safeguards. Do not modify the official randomness project or begin a large generation until we agree.

---

## 11. Provenance of this handover

Prepared from the owner's original scope file, the latest locally available `OUTLANDISH_01_1e10_Pipeline_v2.zip` source and README, the owner's pasted Windows generation/test/scan logs, `Potential_Other_constants.txt`, and the actual supplied `run_20261105_231343.zip` result archive. Exact positions and signed consecutive-pair differences in §5.2 were independently calculated from the attached match CSVs. No lottery result records, holdout data or external website outputs were fetched for this handover; no project software or real draw data were executed here.

**End of handover v0.1.**
