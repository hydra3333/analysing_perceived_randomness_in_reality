<!-- OUTLANDISH_CURRENT_HANDOVER_2026_11_09 -->
> **Current generation checkpoint — 9 November 2026.** This README below documents the older 7-Nov WSL packed-code candidate and is retained as historical implementation documentation. Four 10^10-digit packed files have been completed on Ryzen/WSL; two remain. Due to Ryzen shutdowns, final gamma and lemniscate are now planned via one **elevated native-Windows BAT on an i5-4670** (its G:/T:, no E:). Its two-constant 1e6+1e6 full end-to-end test PASSED; full 10^10 production has **not started**. Read `OUTLANDISH_01_Generation_Workflow_Update_2026-11-09.md` and the parent `../OUTLANDISH_01_Consolidated_Handover_v7.md` first. The child is for generation; return to `GAIS/OUTLANDISH_01` for matching, null-world evaluation and eventual parent-project method design. No generation or scan is authorised by this banner. Original README follows intact.

---

# OUTLANDISH_WSL — packed-decimal WSL integration candidate v0.2

**7 November 2026 — DEVELOPMENT CANDIDATE, NOT INSTALLED OR PRODUCTION-RATIFIED.**

This is a **complete replacement for the earlier `OUTLANDISH_WSL_Integration_v0_1` source candidate**, implementing packed nibbles and fewer whole-file verification passes. It does NOT replace the established parent `outlandish_*.py` programs, modify `outlandish.local.toml`, manipulate the legacy active registry, move/retire the six 10^9-byte/digit reference binaries, or start a new large computation.

## Architectural placement

| Location | Role |
|---|---|
| `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\GAIS\OUTLANDISH_01\OUTLANDISH_WSL\` | THESE scripts, BAT launchers, docs, source-controlled tests. Never generated large files. |
| `T:\OUTLANDISH_WSL\Debian\ext4.vhdx` | Linux OS on WSL2, y-cruncher executable, text, swap and logs via `/home/u/outlandish-test` or `/home/u/outlandish-work`. |
| `T:\OUTLANDISH_WSL\rehearsal_artifacts\` | Disposable staging/results, on NTFS, initially used in all rehearsals. |
| `G:\OUTLANDISH_01\large_artifacts\` | Existing native-Windows production artifacts; separate staging possible in a later authorised exercise, but **old registered active files stay unchanged**. |

### Python and venv (important)

* All **Windows-side Python** (`WSL_Tests.bat`, `WSL_Verify_Packed.bat`, `WSL_Scan_Packed_Powerball.bat`) runs through the *existing project* interpreter at repo-root `.venv\Scripts\python.exe` after calling repo-root `activate_venv.bat` (both are resolved relative to this source folder). The existing dependency BAT `install_upgrade_dependencies_into_venv.bat` is **not changed or invoked**. The scanner uses the installed NumPy.
* Linux cannot execute the Windows `.venv` interpreter. Debian uses its own `python3` **standard library only** for `wsl_convert.py` and the shell launcher uses bash. No Debian NumPy, pip or copied virtual environment is required for conversion; check `python3 --version` before using it.
* No separate WSL TOML is needed yet: source paths and destinations are explicit CLI parameters. There is **no second mutable active registry** hiding under E:. The accompanying JSON receipts are per-file evidence, not a current-production registry.

## Canonical digit format v1 (incompatible with original .bin files)

`OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`: digit 0 is in high nibble of packed byte 0, digit 1 in low nibble, digit 2 in high nibble of byte 1, and so on. `1.61803...` becomes `16 18 03 ...` in hex (decimal point omitted). Only nibble values 0–9 are legitimate. For odd digit counts the final low nibble **must be zero padding**. The receipt carries exact original digit count `N`; size is `ceil(N / 2)` bytes.

Six constants are supported. `lemniscate` input comes from y-cruncher's full perimeter `5.244...` and is halved *exactly* while streaming to OUTLANDISH's chosen half-perimeter `2.622...`, before nibble packing. The pure-Python per-digit operation is slower than native packing; benchmark before planning 10^11. `wsl_format.py` is the common format specification. **Never feed a `.packed.bin` to the old byte-per-digit scanner, verifier, or registrar.**

## Revised lean verification policy

1. y-cruncher is run with `-verify:1`. The converter requires its small completion report with the expected constant, decimal places and successful spot check.
2. Linux converter reads the entire text **once** (unavoidable), validates all characters/digit count/point location/known 32-digit prefix, streams packed bytes to one create-only staging file, computes both source and packed SHA-256 inline. It flushes and fsyncs the binary.
3. It publishes the file **without overwriting**, then rereads deterministic bounded 4 KiB samples at start/middle/end and other offsets; stores samples' SHA-256, exact size and the source-streamed packed digest in a small create-only receipt.
4. **Only after receipt publication does it remove the exact large text file**, unless `--keep-text` is selected. On errors it preserves the source and does not replace an existing destination. It never deletes the y-cruncher report, its log, or arbitrary files. Warning: a crash between publication and receipt can leave an orphan output; inspect it manually rather than force-retry.
5. Windows verifier checks the staged receipt's deterministic samples (and optionally sampled overlap with existing legacy reference) in small random-access reads; **does not hash the full staged file**.
6. The separate packed Powerball scanner, when instructed to process the **complete** file, calculates the full SHA-256 during its required one-pass scan and compares it to the converter's hash. Partial scans do **not** make an equivalent full-integrity claim.

**Limitation explicitly accepted for this candidate:** corruption outside sampled regions can go undetected until a full scan; a source-streamed hash plus samples does not authenticate all persisted bytes. None of this independently proves y-cruncher's mathematical output. The old byte-oriented registry uses its own full-read requirements and is not called. A new packed promotion/retention mechanism would need separate design, review and authorisation; automatic deletion of the earlier 1-billion-digit references is NOT implemented.

## Contents

| File | Use |
|---|---|
| `wsl_generate.sh` | Preview-by-default conservative Linux y-cruncher wrapper; optional explicit calculation. Uses `-verify:1`, default swap, `-TD:1 -PF:none`, proposed `-M:4g`, unique ext4 attempt folder. **No auto converter**. |
| `wsl_format.py` | Versioned packed BCD format, known prefixes, sample policy and path checks. |
| `wsl_convert.py` | Linux native text-to-packed staging converter with source cleanup after validation/receipt; preview default. |
| `wsl_verify_windows.py` | Windows read-only sampled verifier, optional sampled cross-format comparison with legacy numeric-byte reference. |
| `wsl_scan_packed_powerball.py` | Windows NumPy bounded-chunk packed-digit scanner, preserving existing Powerball P1/P2/P3 definitions and *all decimal-digit start offsets*. Creates new CSV/JSON reports. Preview default. |
| `WSL_Tests.bat`, `WSL_Verify_Packed.bat`, `WSL_Scan_Packed_Powerball.bat` | Existing project venv launchers. Do not overwrite root-level BAT files. |
| `test_wsl_packed.py` | Synthetic tests: 6 constants, odd padding, source cleanup/failure, sample tamper, legacy sample comparison, P1/P2/P3 cross-boundary matching, cutoff refusal. |
| `RESOURCE_ESTIMATES.md` | Exact old/new file sizes and carefully qualified timing illustrations. |

## 1. Extract and check without running large calculations

Extract only this ZIP's files **directly into the existing** `E:\...\GAIS\OUTLANDISH_01\OUTLANDISH_WSL\` directory (not into the parent `OUTLANDISH_01`). Back up/replace the v0.1 WSL candidate scripts if you previously copied them; this is a versioned replacement, not a parallel second WSL toolset. Do not copy production `outlandish.local.toml` into it.

In an ordinary **Windows CMD** at that WSL source directory:

```bat
WSL_Tests.bat
```

This uses the repo-root project's existing venv and NumPy. The synthetic tests do not read real draw outcomes, 1e9 G: binaries, or update registered state. Package creation tests passed in a Linux container with Python 3.13/NumPy 2.3.5; actual Windows CMD and Debian mount behavior remain to be validated on the owner's PC.

## 2. Controlled 100-million-digit rehearsal — T: only

Your current verified source is still in Debian:

```text
/home/u/outlandish-test/phi_100m_swap/Golden Ratio - Dec - Newton.txt
/home/u/outlandish-test/phi_100m_swap/Golden Ratio - 20261107-172852.txt
```

In **Debian** (on the E: source folder):

```bash
cd /mnt/e/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/GAIS/OUTLANDISH_01/OUTLANDISH_WSL
python3 --version
mkdir -p /mnt/t/OUTLANDISH_WSL/rehearsal_artifacts/staging
python3 wsl_convert.py \
  --constant phi --digits 100000000 \
  --source-root /home/u/outlandish-test \
  --input '/home/u/outlandish-test/phi_100m_swap/Golden Ratio - Dec - Newton.txt' \
  --report '/home/u/outlandish-test/phi_100m_swap/Golden Ratio - 20261107-172852.txt' \
  --output-root /mnt/t/OUTLANDISH_WSL/rehearsal_artifacts \
  --output /mnt/t/OUTLANDISH_WSL/rehearsal_artifacts/staging/digits_golden_ratio_10_to_8.packed.bin \
  --keep-text
```

That is a **preview only**, with no write or deletion. If acceptable, repeat the same invocation with `--run` appended (KEEP `--keep-text` specifically for this initial rehearsal). Expected packed file size is exactly **50,000,000 bytes**. The receipt lives next to it, named `.packed.bin.wsl-receipt.json`. If the NTFS/DrvFS create-only hard-link publication fails, report the error; do **not** change it to overwrite-prone `mv`/rename or bypass a failure.

Then, from **Windows CMD** in the E: WSL source directory:

```bat
WSL_Verify_Packed.bat --input "T:\OUTLANDISH_WSL\rehearsal_artifacts\staging\digits_golden_ratio_10_to_8.packed.bin" --constant phi --digits 100000000 --reference "G:\OUTLANDISH_01\large_artifacts\digits\digits_golden_ratio_10_to_9.bin"
```

Verify the exact G: reference filename against live `outlandish.local.toml` before running; the G: file is accessed **read-only**. This compares SAMPLED blocks only (not all 100m digits), by explicit owner preference.

## 3. Packed Powerball scanner rehearsal

First prepare an isolated **T: result directory** in Windows CMD:

```bat
mkdir "T:\OUTLANDISH_WSL\rehearsal_artifacts\results"
```

Then preview in the E: WSL source folder:

```bat
WSL_Scan_Packed_Powerball.bat --input "T:\OUTLANDISH_WSL\rehearsal_artifacts\staging\digits_golden_ratio_10_to_8.packed.bin" --draws "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\GAIS\OUTLANDISH_01\POWERBALL_preholdout_only.csv" --output-root "T:\OUTLANDISH_WSL\rehearsal_artifacts\results" --prefix-digits 1000000
```

No computation or reports are generated in preview. For a small scanner rehearsal add `--run`. After correctness/throughput evaluation, scan all 100m digits by omitting `--prefix-digits`; the **full scan** checks the entire staged file's SHA-256 against the conversion receipt as part of normal scanning, not an extra pass. The scanner is single-threaded and bounded in memory, and does not touch original Powerball master files. It rejects draw number 1577 and beyond before reading those rows' outcomes.

## 4. Future generation preview ONLY

In Debian:

```bash
cd /mnt/e/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/GAIS/OUTLANDISH_01/OUTLANDISH_WSL
bash wsl_generate.sh --constant phi --digits 10000000000
```

The wrapper **prints** the proposed Linux y-cruncher command but does nothing. Its `--run` flag starts a calculation; >=1e9 additionally requires `--ack-large-run N`. The 4g memory setting is **proposed, not verified safe or optimal for this scale**. Do not start 10^10 or 10^11 until resource estimate/free-space/temperature/power strategy and owner authorisation are settled.

## Scientific scope and deferred work

* **Powerball**: current packed scanner maintains the previous P1/P2/P3 definitions (P1/P2 drawn order; P3 any six main balls in any order + Powerball). **Drawn-order vs any-order extensions for P1/P2/P3 are deferred**, see `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md` (previously agreed; do not silently add them).
* **Oz Lotto**: O1/O2/O3 matching remains an unimplemented proposal; six/supplementary order semantics must be ratified first. Never pool games.
* **No nibble migration of the six legacy 1e9 binaries is performed** here. The packed candidate is a new, explicitly versioned representation. Files generated with new WSL scripts remain staged and independent until a safe registry/retention design is agreed.
* y-cruncher's full text input is assumed valid only with matching report and known prefix. Report authenticity is not cryptographically guaranteed. Receipt format is not a signed artifact. The `--keep-text` option exists for debugging/benchmarking.
* The user-supplied `activate_venv.bat` and `install_upgrade_dependencies_into_venv.bat` are treated as existing, **unchanged** project-root scripts. Do not reinstall packages or create a second Windows Python environment for this work.
