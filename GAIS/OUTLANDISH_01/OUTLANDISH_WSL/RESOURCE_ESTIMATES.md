# OUTLANDISH_WSL packed-decimal size and timing evidence — v0.2

**Date:** 2026-11-07. `N` counts decimal digits **including the integer digit**. The packed format holds two digits/byte. These are separate from y-cruncher's temporary disk-swap allocation and text output.

## Exact format sizes

| Digits per constant | Existing byte/digit | New nibble-packed `.packed.bin` | Six packed binaries | y-cruncher text (observed simple format) |
|---|---:|---:|---:|---:|
| 10^9 | 1,000,000,000 B | 500,000,000 B (0.466 GiB) | 3 GB | 1,000,000,001 B |
| 10^10 | 10,000,000,000 B | 5,000,000,000 B (4.657 GiB) | 30 GB | 10,000,000,001 B |
| 10^11 | 100,000,000,000 B | 50,000,000,000 B (46.566 GiB) | 300 GB | 100,000,000,001 B |

For odd `N`, file size is `ceil(N / 2)` and the LOW nibble of the last byte is **zero padding**, not a digit. The receipt explicitly records `N`. Decimal text output may contain further whitespace; transient y-cruncher output allowances can exceed the exact content length.

## Measured Linux/WSL φ (Golden Ratio), owner report

| Decimal digits incl. integer | Mode | TD | Verification | Observed wall | Logical disk estimate |
|---|---|---:|---|---:|---:|
| 100,000 | RAM | 1 | Enabled | 0.086 s | none beyond output |
| 1,000,000 | Disk swap | 1 | Enabled | 1.727 s | 73.6 MiB + text |
| 10,000,000 | Disk swap | 1 | Enabled | 6.982 s | 101 MiB + text |
| 100,000,000 | Disk swap | 1 | Enabled | 50.108 s | 373 MiB + text |

The successful 100-million-digit Linux test was *not* yet a measured packed-converter/Windows-NTFS staging run. At 10^10 φ the interactive estimator reported ~41.0 GiB RAM-only versus ~37 GiB temporary disk + ~17 GiB output when swap was selected (with a large RAM allocation). A 4 GiB cap is **proposed, not independently measured at 10^10**. The accidental interactive calculation was interrupted; do not treat it as a benchmark. WSL2 then exposed ~15.6 GiB RAM and the ext4 volume had ~955 GiB available.

## Existing 10^9 native Windows RAM generation — user-reported timings

| Constant | Approximate observed 10^9 |
|---|---:|
| φ | ~15 seconds |
| e | ~44 seconds |
| π | ~71 seconds |
| ln(2) | ~180 seconds |
| γ | ~2,447 seconds (~41 min) |
| Lemniscate | on scale of minutes; actual time not captured |

These are earlier Windows runs, with different hardware usage, mode, thread and verification settings. **Do not label them as WSL2 timings.**

### Illustrative compute-only scaling (not forecast wall times)

Assume, for demonstration only, cost proportional to `N × ln(N)^2`: factor 12.35 from 10^9 to 10^10 and 149.38 to 10^11.

| Constant | 10^9 owner observation | 10^10 artificial scaling | 10^11 artificial scaling |
|---|---:|---:|---:|
| φ | 15 s | 3.1 min | 37 min |
| e | 44 s | 9.1 min | 1.83 h |
| π | 71 s | 14.6 min | 2.95 h |
| ln(2) | 180 s | 37 min | 7.47 h |
| γ | 2,447 s | 8.4 h | 4.23 days |
| Lemniscate | minutes (unspecified) | not calculable | not calculable |

**These are NOT plausible promised elapsed-time estimates for WSL2 disk-backed work on a physical HDD.** Disk I/O, CPU parallelization, memory cap, FFT transitions, numerical verification, long-division for lemniscate, NTFS writes, and scanning are unmodelled and could dominate. Collect real benchmarks at comparable WSL settings, plus converter throughput and scanner throughput, before presenting ranges as empirical estimates.

## Verification cost and new choices

* Source is read and all decimal characters validated **once while converting**. Packed bytes are hashed in the same write pass.
* Exactly a bounded set of reproducible **4 KiB readback samples** are compared with the bytes generated in RAM, after create-only publication. The receipt stores the sample positions/digests and the **source-streamed** SHA-256, not an independently reconstructed on-disk digest.
* Windows sampled read-only check compares receipt samples and optionally a sample of the overlapping legacy reference prefix, without another full-file read.
* **A complete packed Powerball scan computes a full-file SHA-256 during its ordinary input scan**, comparing it to the converter's digest with no extra I/O pass. A prefix-only scan does not make that claim.
* The accepted reduced verification policy cannot detect corruption in unsampled regions before the first full scan, and does not mathematically prove newly generated digits. y-cruncher's own `-verify:1` is retained.
* No old files or registered active data are auto-retired. The old registry remains byte-oriented and cannot accept packed files.

## Next benchmarks

1. Rehearse 100m φ conversion with output in **T: experimental staging**, `--keep-text`, and record conversion duration and Windows read-only sample comparison against the 1e9 legacy φ reference on G:.
2. Benchmark packed P1/P2/P3 scan on the 100m sample and compare with the old scanner on an equivalent digit count if practical. The same 0-based digit offsets must be retained.
3. Measure actual conversion and scan I/O on G: with a disposable, unregistered candidate before authorising production-scale runs.
4. At most one numerical constant computed at a time; review host/T/G free space and WSL ext4 virtual-disk ceiling before 10^10 or 10^11. No automatic conversion on unverified y-cruncher failure.
