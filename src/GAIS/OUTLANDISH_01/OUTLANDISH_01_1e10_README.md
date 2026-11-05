# OUTLANDISH_01 — 10^10 digit pipeline v2

Standalone, experimental Powerball search on pre-holdout draw copies. This software does not fetch lottery data, contact Lotterywest, change the main project registry, or touch project holdout/result sources.

## Changes from the validated 10^9 pipeline

- `--threads N` controls y-cruncher's task decomposition; **default 4**. For `N=1`, uses `-TD:1 -PF:none` for true single-thread computation. For `N>1`, uses `-TD:N -PF:taskqueue`. The value is a parallelism setting, not an absolute guarantee that exactly N OS threads will exist. **The Powerball scanner remains single-threaded**.
- `pipeline` performs **generate → strict convert → independent binary re-read verification → cleanup** automatically. Delete only the selected freshly generated large source text, and the scratch subdirectory created for this run; preserve y-cruncher's small calculation/validation reports and `OUTLANDISH_01_verified.json`. `--keep-text` opts out of cleanup.
- With an existing `digits_pi_10_to_9.bin` / `digits_golden_ratio_10_to_9.bin`, the full **first billion digit bytes** of the new 10-billion-digit binary must match the old one. The comparison is streamed using bounded memory. If no billion-digit reference exists, falls back to the million-digit file; for >=1e9 an existing reference is mandatory.
- Six supported constants: `pi`, `phi`, `e` (Euler's number), `log2` (natural logarithm of 2), `gamma` (Euler–Mascheroni constant), `lemniscate`. The scanner's known-prefix validation was extended for the four additions; the search algorithm and FIXED2 P1/P2/P3 definitions are unchanged.
- For jobs of **5 billion or more digits**, the default `--mode auto` selects y-cruncher's `-mode:swap`, rather than attempting a large RAM-only allocation on a PC with 32 GiB physical RAM. Default swap working-memory setting is **16 GiB** (`--memory-gib 16`); a dedicated scratch folder on E: is created for each calculation.
- Existing outputs are never overwritten. Errors leave source files/checkpoints in place for examination. No cleanup after generation, conversion or verification failure.

## Installation

Extract into your existing directory:

`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\src\GAIS\OUTLANDISH_01`

Replace these two Python scripts with the supplied versions:

- `outlandish_big_constants.py` (new generation/conversion pipeline)
- `outlandish_powerball_stage_a.py` (only new constant prefix identifiers; scan unchanged)

Keep your existing `POWERBALL_preholdout_only.csv`, prior `.bin` files and `OUTLANDISH_01_results` intact. Activate your existing project virtual environment.

```
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test
```

No additional PyPI dependency for the generator; the scanner continues to use installed NumPy.

## PI and GOLDEN RATIO at 10^10 — recommended commands

**Run one generator at a time**, particularly in disk-swap mode. The previous 10^9 run used 4.18 GiB for phi; multiplying its input size by 10 may exceed available RAM. The disk-swap mode is an intentional precaution, not a measured 10^10 requirement. y-cruncher documentation notes swap mode may require an **elevated Windows process**; check its actual preflight memory/disk estimate. Do not disable OS protections to force a run. If the program refuses, keep the output for inspection; do not blindly retry/deleting checkpoints.

Preview; **no file or folder is created**:

```
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000
python outlandish_big_constants.py pipeline --constant phi --digits 10000000000
```

The preview should contain `MODE=SWAP THREADS_REQUESTED=4` and `-TD:4 -PF:taskqueue -M:16g -swap:raid0 ...`.

Generate, convert, verify, clean up in one command per constant:

```
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000 --run
python outlandish_big_constants.py pipeline --constant phi --digits 10000000000 --run
```

Alternatively use `generate_1e10.cmd`, which runs the two commands *sequentially* and stops on failure. The BAT has `THREADS=4` at the top for convenience. To request a different setting:

```
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000 --threads 2 --run
```

The output files are `digits_pi_10_to_10.bin` and `digits_golden_ratio_10_to_10.bin`, each **10,000,000,000 bytes** (10 GB decimal, about 9.31 GiB). At peak, also allow roughly 10 GB for uncompressed text, plus the disk-swap workspace, conversion temporary file, and OS/other application headroom. The generator checks only a lower bound for free disk, not y-cruncher's detailed storage needs.

Each success leaves `ycruncher_digits\pi_10000000000_digits\` or `...\phi_10000000000_digits\` containing small y-cruncher stats/validation TXT files and `OUTLANDISH_01_verified.json`. The 10 GB plaintext file and the newly owned scratch folder are removed only after **CONVERSION PASS**, **VERIFY PASS**, identical SHA-256 hashes, and full reference-prefix comparison.

If it fails at any stage, **leave the directory in place** for diagnosis: the script deliberately refuses to overwrite/re-use an existing output directory.

## Search both 10-billion-digit binaries

```
python outlandish_powerball_stage_a.py scan --draws POWERBALL_preholdout_only.csv --digits digits_pi_10_to_10.bin digits_golden_ratio_10_to_10.bin --chunk-bytes 4000000 --progress-seconds 5
```

Or `scan_1e10.cmd`.

- Uses the **433 eligible, pre-holdout-only Powerball draws** in the existing CSV, not fabricated examples.
- Searches **all 10 billion digit-byte starting positions**, including odd alignments and chunk crossings, for P1/P2/P3 with FIXED2 ball representation.
- Uses one scanner thread; prints time-gated progress and writes per-constant match/transition/summary files in a fresh results directory.
- Based solely on your measured 10^9 performance (~27.6–27.9 s), linear scan-only extrapolation is ~4.6 min per constant. This does not predict y-cruncher disk-swap generation runtime, which could be much longer.

## Extra constants — your list items 1, 2, 4 and 8

| Your # | CLI identifier | Mathematical constant | y-cruncher constant parameter | First digits (decimal point for clarity) |
|---|---|---|---|---|
| 1 | `e` | Euler's number | `e` | `2.718281828459...` |
| 2 | `log2` | Natural logarithm of two | `log:2` | `0.693147180559...` |
| 4 | `gamma` | Euler–Mascheroni constant | `gamma` | `0.577215664901...` |
| 8 | `lemniscate` | Lemniscate constant | `lemniscate` | `2.622057554292...` |

The code supports all four, **but none has yet undergone a real Windows y-cruncher smoke test**. Start at 10^6 digits, not 10^10:

```
python outlandish_big_constants.py pipeline --constant e --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant log2 --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant gamma --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant lemniscate --digits 1000000 --run
```

These small tests use y-cruncher's own verification plus the independently known 32-digit constant prefix; the new `.bin` files become the one-million-digit references for later larger runs. Each command defaults to 4 threads. Later, use the same `pipeline --digits 1000000000` once the 10^6 result passes and you choose to extend it.

To search another constant, explicitly name its `.bin` file to the existing scanner's `--digits` option, e.g. `--digits digits_e_10_to_6.bin`. Each search is independent. Do not pool constants or lottery games in the analytical outputs.

## Important limitations and precautions

- **Generation mode is separate from search threading.** `--threads` applies only to y-cruncher's computation. Actual thread counts and benefits depend on the algorithm and its task decomposition.
- Swap calculations use a dedicated scratch folder underneath the current run's output directory and `-swap:raid0`. Whether this exact setting is accepted by your y-cruncher v0.8.7.9547b Windows executable must be established by its own preflight/run. This code has not launched real Windows y-cruncher, only synthetic subprocesses.
- `pipeline` accepts one detected uncompressed plain-text digit file of exactly `N+1` bytes (N digits plus decimal point), consistent with your 10^6 and 10^9 observations. If y-cruncher emits a different or split format, it **REFUSES** to convert or delete anything; inspect the output instead.
- The streamed full-prior-reference comparison and known 32-digit prefix are strong consistency checks, but do not independently compute all 10^10 digits by a second algorithm.
- `--mode ram` is disallowed for >=5e9 in this workflow. `--mode swap` may be specified explicitly for smaller experiments; `--memory-gib` adjusts its requested working memory.
- The generator will not overwrite existing binary files or re-use the same output directory. Keep source binaries and evidence reports outside Git; never commit large .bin files or draw-data copies to the project's main repository.
- The historical dataset and holdout cutoff are not modified. No draw data is used by the generator at all; only by the separate pre-holdout scanner.

## Local synthetic test evidence

`outlandish_big_constants.py self-test` passed for all six constants, including strict conversion/refusal cases. A separate synthetic mock-y-cruncher integration harness passed: successful end-to-end pipeline with cleanup for all six constants, requested 4 threads, true single-thread option, swap command preview, swap workspace cleanup, wrong-reference failure retaining plaintext, and wrong-digit-count failure retaining plaintext. The Powerball scanner's existing overlapping/chunk-crossing P1/P2/P3 self-test also passed. **No 10^10 real digit generation or 10^10 real scanner execution has been performed here.**
