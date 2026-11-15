# OUTLANDISH_01 — Q3 v0.3 synthetic 4 MB vs 8 MB benchmark

**Status:** optional performance measurement only, **not** Q3/Q4 production qualification or Q5 approval. Created 15 November 2026. No production 5 GB constants, historical source_data, receipts or REAL/NULL results are consulted.

## Purpose

Measure elapsed scan/write time, scanned packed-MB/sec, and **peak process resident/working-set memory** independently for `chunk_bytes=4_000_000` and `8_000_000` with both game adapters. Verify that the output event counts, CSV SHA-256, family totals and packed source hashes agree between the two chunk sizes. Explicitly avoid inferring an 8 MB speedup without measurement.

The only new dependency is the existing, committed `OUTLANDISH_01_Q3_Packed_Matcher_v0_3.py` in the same directory. This harness uses Python stdlib, NumPy via that module, and separate short-lived Python worker processes; it **does not** modify that module or spawn production workers.

## Installation

Extract this ZIP into the repository root, preserving `GAIS/OUTLANDISH_01/` paths. It introduces only this benchmark file and this README. Do not overwrite or alter any existing scanner, classifier, living record, or overarching project data.

Run from a Windows CMD prompt at the repository root:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Synthetic_Performance_Benchmark_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Synthetic_Performance_Benchmark_v0_1.py" --run
```

Default is **32 MB synthetic packed BCD input** (64 million logical decimal digits) and **433 invented draws per game**. It runs four fresh-process scans total: 4/8 MB Powerball, 8/4 MB Oz, then discards the temporary input and CSVs. It plants a few valid matches crossing chunk boundaries. The benchmark may take noticeably longer on the i5; no exact runtime is promised.

For a shorter initial run, select 16 MB:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Synthetic_Performance_Benchmark_v0_1.py" --run --size-mb 16
```

If desired, `--game powerball` or `--game oz` restricts the comparison, and `--draw-count 433` is the default. `--size-mb` accepts 16..128 decimal MB. **Do not pass production packed file paths to this harness.** The private worker mode rejects input filenames outside the synthetic benchmark naming convention.

Expected final line begins `Q3 SYNTHETIC BENCHMARK PASS`.

## Interpretation and limitations

- **Peak process MiB** includes the Python interpreter, NumPy, draw indexes and native allocation overhead; Windows uses `GetProcessMemoryInfo().PeakWorkingSetSize`. Each 4 MB/8 MB test runs in a **new subprocess**, avoiding high-water-mark contamination.
- **Time** covers the scanner + streaming CSV writer and full input SHA check; synthetic fixture creation and subprocess startup are excluded from the timing. Results will vary with caching, CPU contention, thermal throttling and filesystem performance. The Oz and Powerball scans differ in matching workload.
- Local development trial on a different Linux host with 16 MB synthetic input: PB 4 MB ~0.479 s / 386 MiB peak, PB 8 MB ~0.506 s / 646 MiB peak; Oz 4 MB ~1.295 s / 342 MiB peak, Oz 8 MB ~1.381 s / 556 MiB peak. **This is only one non-Ryzen trial**, not a reliable performance conclusion. Larger chunks raised memory but did not clearly improve speed; retain the RAM policy as *provisional* pending Ryzen results.
- Source bytes are generated with a **deterministic synthetic** random seed and mapped to valid BCD pairs, with a few planted patterns; no lottery outcomes are read.
- Comparisons demonstrate chunk-size-invariant output, **not** scientific matching correctness on 10^10 digits. Existing independent-oracle Q3 qualification is unchanged.
- A full scan of six production constants is still explicitly **NOT AUTHORISED**. This benchmark does not create production manifests, REAL/NULL run directories or forecasting outputs.

Send the four `BENCH ...` lines and the final `Q3 SYNTHETIC BENCHMARK PASS` line. We can then decide whether the automatic 8 MB choice is worthwhile on the actual Ryzen and whether to leave 4 MB as a safer baseline for concurrency.

**Git policy:** stage only `GAIS/OUTLANDISH_01/` after inspecting its staged files, and avoid committing the downloaded ZIP itself. Leave unrelated uncommitted parent-project files alone.
