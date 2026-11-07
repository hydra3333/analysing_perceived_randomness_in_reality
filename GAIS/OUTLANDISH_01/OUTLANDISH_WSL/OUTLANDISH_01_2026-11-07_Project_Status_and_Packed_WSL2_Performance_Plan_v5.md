# OUTLANDISH_01 — consolidated handover: packed WSL2 baseline and performance-first plan

**Document:** `OUTLANDISH_01_2026-11-07_Project_Status_and_Packed_WSL2_Performance_Plan_v5.md`  
**Date:** 7 November 2026 (Australia/Adelaide)  
**Version:** **v5** — supersedes v4/v3/v2/v1 **as the current conversation handover only**. Installed source code, the actual E: configuration, G: registry, on-disk artifacts and verified result files remain the operational evidence.  
**Status:** Real 100-million-digit WSL2 → Linux nibble conversion → Windows sampled verification → full packed Powerball scan **completed successfully**; resource inventory and **three successful 300-million-digit phi disk-swap benchmarks** have now been performed (1 GiB/one core, 8 GiB/one core, and 8 GiB/`--td 4` with `taskset`). Owner's work order is **(1) optimise WSL2/y-cruncher disk-backed generation for 10^10 and 10^11, (2) SKIP legacy-versus-packed scan benchmarks, (3) implement an independently versioned packed-format G: production registry/promotion workflow**. **At most four physical cores** are permitted for y-cruncher. No 10^10/10^11 calculation, WSL memory-limit change, or G: packed promotion is authorised by this handover.  
**Scope:** Only the standalone `GAIS/OUTLANDISH_01` side experiment. **Not** the main predictive-randomness method project, its release gates, or the protected holdout.

> **Next-chat reading rule:** Read this Part I first, especially §3A (new benchmarking evidence) and §6 (next steps). Part II retains the earlier native-Windows and Windows Sandbox history for provenance, **not** current operational instructions. Earlier v3 Part I said the WSL conversion was unimplemented and that Debian needed no Python; both are now obsolete. New WSL code exists, Debian Python 3.13.5 is installed, and real packed data has been generated and scanned. No access to the owner's live disks is claimed by this handover.

---

# Part I — CURRENT state, evidence, decisions and safe next steps

## Executive summary / owner decisions

1. **Keep the new WSL workflow:** Debian 13 (trixie) under WSL2 on T:, static Linux y-cruncher v0.8.7 Build 9547, scripts committed/edited on E:, controlled temporary work on T:, verified future production artifacts on G:. The six legacy one-byte-per-digit 10^9 files on G: and original Windows `outlandish.local.toml` must remain unchanged in ongoing development.
2. **Adopt nibble-packed format** `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`: two decimal digit values (0–9) per byte, first digit in high nibble; final low nibble must be zero for odd counts. It saves **exactly 50%** for even digit counts. This is intentionally incompatible with the old one-digit-per-byte `.bin` format, verifier, scanner and registry.
3. **Adopt lean verification:** Linux y-cruncher `-verify:1`; Linux converter validates every input digit while streaming, records source and packed digests, rereads bounded output samples and emits a receipt; Windows checks bounded samples; a complete packed scanner pass computes the whole packed-file SHA-256 as part of its existing I/O. Do not perform redundant whole-file scans purely for ceremony. But a sample check is **not** a complete persisted-file integrity guarantee; protection during eventual registration must be explicitly designed.
4. **Source-text lifecycle:** Ordinary completed production conversion should automatically remove *only its exact owned large decimal input* after successful conversion, bounded checks, receipt publication and safe cleanup preconditions. On failure retain the source text; `--keep-text` preserves it for rehearsals. Retain small y-cruncher reports/logs. The successful 100m rehearsal deliberately used `--keep-text`.
5. **Revised work order:** **First optimise actual WSL2 external-memory y-cruncher generation**, aiming for 10^10 and where feasible 10^11; **skip** comparison of old byte-per-digit scanner speed versus packed scanner; **then** develop and qualify isolated packed G: staging, registry, prefix comparison, promotion and retention. Keep the separate deferred drawn-order/any-order enhancements for both Powerball and Oz Lotto on the backlog.
6. **At most four physical cores:** Owner expressly approves benchmarking up to four, not beyond. Latest test requested four task-queue workers and ran through `taskset -c 0,2,4,6`; y-cruncher also printed `4 / ? / 24 (all cores)`, so the real child-thread affinity has **not yet been independently observed**. Do not assume the CPU limit was enforced merely because `taskset` was used.
7. **No large compute by default:** Prior interactive menu accident started a 10^10 job with ~79.7 MiB total y-cruncher memory; Ctrl+C stopped it, no process remained. It is a cautionary example. Use read-only resource checks and preview-by-default scripted configurations, with explicit owner approval before running bounded benchmarks or any real 10^10/10^11 job. Earlier owner-observed high-concurrency hard power-offs make threading changes safety-significant.

## 1. Actual source, runtime and data locations

| Place | Exact role and restrictions |
|---|---|
| `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\GAIS\OUTLANDISH_01\` | Existing native-Windows source, original `outlandish.local.toml` with six active 10^9 records; do **not** replace or hand-edit generated state. |
| `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\GAIS\OUTLANDISH_01\OUTLANDISH_WSL\` | **Single edited / Git-managed WSL source tree**: Bash/Python tools, BAT launchers, tests, docs; no large generated artifacts or mutable active registry. |
| `/mnt/e/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/GAIS/OUTLANDISH_01/OUTLANDISH_WSL` | Debian's view of the same code on E:. Run Bash or Python scripts from this location; do not maintain a second editable copy inside Debian. |
| `T:\OUTLANDISH_WSL\Debian\ext4.vhdx` | **Verified** WSL2 Debian virtual disk; Linux native `/home/u/outlandish-test/` holds y-cruncher and test outputs. Future heavy FFT/swap and decimal text should remain on ext4, rather than `/mnt/e` or `/mnt/t`. |
| `T:\OUTLANDISH_WSL\rehearsal_artifacts\` | Actual tested disposable NTFS staging/results; current 50,000,000-byte packed phi file and its receipt, plus full packed scanner reports. |
| `G:\OUTLANDISH_01\large_artifacts\` | Existing managed **production** byte-per-digit constants; future isolated packed staging and verified packed data would go here **only after registry support is reviewed**. No WSL rehearsal writes to this area. |

Debian installation: WSL 2.5.7.0, Linux kernel 6.6.87.1-1; Debian Trixie (WSL2) under `/home/u`, ext4 filesystem ~1007 GiB virtual capacity (earlier ~955 GiB available), with the VHDX physically on T:. Host T: previously showed ~2.9 TB physical free; virtual-disk *capacity* and host physical free space are distinct limits. Linux VM usable RAM ~15.6 GiB; Linux **OS** swap 4 GiB, distinct from y-cruncher's managed disk-swap files. Host Ryzen 9 3900X (12 cores/24 logical), 32 GiB RAM, T: HDD backing, G: separate production drive.

**Python environments:** Debian now has **Python 3.13.5**, sufficient for standard-library-only `wsl_convert.py`; no Linux NumPy or pip was required. Windows WSL BAT launchers call the repository-root `activate_venv.bat` / `.venv` and successfully imported **NumPy 2.5.4**. The existing dependency-upgrade BAT was neither needed nor modified. Do not try to run Windows `.venv` binaries in Debian.

## 2. Current WSL-specific implementation and deployed fixes

**Latest installed/tested candidate as reported by owner:** `OUTLANDISH_WSL_Packed_v0_2r2` (7 Nov 2026). Earlier `OUTLANDISH_WSL_Integration_v0_1`, packed v0.2 and v0.2r1 are superseded. The original Windows v0.2r4 modules and legacy registry have not been converted to packed format.

| File in `OUTLANDISH_WSL/` | Role / operational contract |
|---|---|
| `wsl_generate.sh` | Preview-by-default Linux y-cruncher wrapper. Conservative starter `-TD:1 -PF:none`, swap-mode `-verify:1`, proposed `-M:4g`, isolated ext4 attempt path. `--run` explicitly starts; >=10^9 also requires matching `--ack-large-run N`. **4g is not a benchmarked optimum or a verified 10^10 memory cap.** |
| `wsl_format.py` | Format ID, packed digit layout, canonical prefixes and sample policy. |
| `wsl_convert.py` | Debian standard-library stream converter; reports, exact digit validation, source/packed SHA-256, sampled persisted readback, receipt, owned source-text deletion after successful publication unless `--keep-text`; preview unless `--run`. Lemniscate uses exact streaming division by two of full-perimeter source before packing. |
| `wsl_verify_windows.py` | Windows read-only sampled receipt verifier and optional sampled cross-format legacy-prefix check. Does **not** independently full-hash staged data. |
| `wsl_scan_packed_powerball.py` | Windows NumPy packed P1/P2/P3 scan at all digit offsets, computes packed SHA-256 during a **full** scan and matches converter receipt, writes CSV/JSON. Does not update a registry. |
| `WSL_Tests.bat`, `WSL_Verify_Packed.bat`, `WSL_Scan_Packed_Powerball.bat` | Existing Windows repo-root venv activation and tool invocation; no second Windows interpreter. |
| `test_wsl_packed.py` | Synthetic regression suite (12 tests, one Windows symlink skip as observed). |
| `README.md`, `RESOURCE_ESTIMATES.md`, `CHANGES_v0_2.md` | Operational notes, size/projection qualifications and version delta. |

Fixes: **v0.2r1** repaired `%~dp0` quoting in `WSL_Tests.bat`; **v0.2r2** repaired y-cruncher saved-report recognition (requires completed base-conversion/decimal-output verification and positive spot check, not a console-only `Verify Output: Enabled` line). Windows tests then ran **12 tests in 2.781 s, OK (skipped=1)**; the skipped symlink case is unverified under that particular Windows environment, not a failed safety oracle. Linux preview and real 100m conversion then succeeded.

The new WSL candidate currently has **no second mutable active registry and no separate active TOML**; source/destination are explicit CLI options and each staged binary has a JSON receipt. If a format-aware registry/TOML is introduced in Priority 3, put versioned configuration templates under E:, persistent mutable test state on T:, and production state only at a guarded designated location on G:. **Do not simply place another TOML beside a launcher and assume existing `outlandish_config.py` will read it:** that old module anchors its `outlandish.local.toml` to its own module directory.

### New packed binary format and size

`OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1` places digit 0 in byte 0's high nibble, digit 1 in byte 0's low nibble, and repeats. Values 10–15 are invalid; when `N` is odd the last low nibble is zero padding. The exact digit count, format ID, constant name and digest must accompany the binary in a validated receipt or registry record. A decimal point and any text formatting are **not** written to `.packed.bin`.

| Digits per constant | Legacy numeric-byte file | Packed file (`ceil(N/2)`) | Unformatted decimal source text, approximately |
|---:|---:|---:|---:|
| 10^9 | 1,000,000,000 B (0.931 GiB) | **500,000,000 B (0.466 GiB)** | 1,000,000,001 B |
| 10^10 | 10,000,000,000 B (9.313 GiB) | **5,000,000,000 B (4.657 GiB)** | 10,000,000,001 B |
| 10^11 | 100,000,000,000 B (93.132 GiB) | **50,000,000,000 B (46.566 GiB)** | 100,000,000,001 B |

Six packed constants at a common size require **3 GB / 30 GB / 300 GB**, respectively, for the final binaries alone. These exclude y-cruncher far-memory/scratch, checkpoints, receipts, report files, duplicated intermediates, and deliberately retained original references. The Windows original six byte-per-digit 10^9 files together occupy about 6 GB and are not to be retired implicitly.

## 3. Measured real-data validation — completed 7 November 2026

**This table is actual owner-supplied console and result-file evidence; it is not a speed forecast.**

| Operation | Result |
|---|---|
| WSL2 static Linux y-cruncher phi RAM-only 100,000 digits, `-TD:1 -PF:none`, verification on | PASS, **0.086 s** end-to-end wall, 0 exit |
| WSL2 phi swap 1,000,000 digits, 256 MiB request, TD1, verify on | PASS, **1.727 s** wall |
| WSL2 phi swap 10,000,000 digits, 256 MiB request, TD1, verify on | PASS, **6.982 s** wall |
| WSL2 phi swap 100,000,000 digits, 256 MiB request, TD1, verify on | PASS, **50.108 s** wall; output report `Golden Ratio - 20261107-172852.txt`, spot check through 75m |
| Debian Python 3.13.5 conversion of the 100m phi decimal text | PASS, **1.581 s** converter-reported elapsed; **50,000,000 B** packed, `--keep-text`; no full output reread |
| Windows `.venv` sampled verification of 50m-byte packed file | PASS, **12 samples**, no full digest recomputation and no promotion |
| Windows `.venv` packed Powerball scanner, entire 100m decimal digits | PASS, **2.819 s** scan wall; scanned full input; recomputed SHA-256 matched converter receipt |

**Actual packed 100m phi file:** `T:\OUTLANDISH_WSL\rehearsal_artifacts\staging\digits_golden_ratio_10_to_8.packed.bin`. Converter/scanner SHA-256:

`4cb6f6288b72f3a0ff738e72b261dc05ef5e507cfb62d29cf86b934dfd635e7e`

**Actual packed scan report directory:** `T:\OUTLANDISH_WSL\rehearsal_artifacts\results\packed_run_20261107T094409Z_c89da00e`. `summary.json` records `format=OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, `constant=phi`, 433 historical pre-holdout draws, exclusive cutoff 1577, full scan, candidate offsets after filtering 64,762, P1=0, P2=0, P3=3, and `digest_compared_to_conversion_receipt=true` (full match). The scan is about **35.47 million decimal digits/s** in this specific 100m run, **not** a prediction for 10^10/10^11.

Actual P3 matches, with zero-based decimal-digit start offsets:

| Draw | Start offset | Matched 6 mains (sequence seen) | PB |
|---:|---:|---|---:|
| 1244 | 20,048,101 | 10, 11, 27, 18, 01, 20 | 20 |
| 1274 | 71,806,090 | 32, 07, 27, 15, 31, 09 | 07 |
| 1373 | 95,105,831 | 31, 23, 25, 13, 15, 21 | 10 |

`transitions.csv` was header-only. No P1/P2 matches; these exploratory P3 occurrences do **not** imply predictability. This is the **accepted packed scanner real-data baseline**; do not rerun old-versus-packed comparative benchmarking solely to revisit the representation choice.

### Verification meaning and limitations

- Y-cruncher internal verification and spot checks are **not independent proof of mathematical correctness** at every digit; positive reports provide useful algorithm-native evidence.
- Linux converter necessarily processes **every source character** and validates format/count/known prefix; it calculates hashes during this pass, then performs bounded sample readback. The recorded streamed packed digest is not by itself proof that every byte persisted correctly.
- Windows sample verification alone can miss unsampled corruption. A full packed Powerball scan reads the whole file anyway and compares SHA-256 to the receipt, so it gives the additional stored-data integrity evidence *without an extra complete read just for verification*.
- Future packed registration must define when it relies on a prior verified full scan versus when it needs an integrated full read, especially with cross-format prefix comparison and possible predecessor retirement. **Never bypass the old safe-registry protections by pointing a packed file at the byte-oriented registry.**

## 3A. NEW — Host inventory, bounded performance benchmarks, and cleanup (7 Nov 2026)

**This is the latest verified operational checkpoint.** Values below come from owner-supplied Windows/WSL terminal output, not from the assistant running y-cruncher. Distinguish internal y-cruncher elapsed time from the shell `time` measurement. All three calculations were **golden ratio phi, 300,000,000 decimal digits including the integer digit, `-mode:swap`, `-verify:1`, output text, native ext4 backed by T:, and y-cruncher v0.8.7 Build 9547**. Each returned `EXIT=0` and a positive spot check good through 250,000,000 digits; the last 50 decimal digits in the reports were identical. All benchmark results were **rehearsals, not candidates registered on G:**.

### 3A.1 Host and WSL inventory (observed, not assumptions)

- Windows host: AMD Ryzen 9 3900X, **12 physical cores / 24 SMT logical CPUs**, 32 GiB physical RAM; Windows 11. T: identified as **WDC WD6003FZBX-00K5WB0**, SATA, physical disk no. 2, nominal 6 TB, NTFS. Windows reported **2,897,650,704,384 bytes available on T:** at inventory time. This is physical host-drive free space, not a reserved budget for OUTLANDISH.
- No `%USERPROFILE%\.wslconfig` was present. Debian reports **15.6 GiB usable VM RAM** (shell `free -h` approximately 15 GiB), 4 GiB OS swap initially unused; **24 online logical CPUs**. `/dev/sdd` ext4 virtual capacity approximately 1007 GiB, with approximately **955 GiB** available; `/mnt/t` is a separate Windows NTFS mount. The T:-hosted `ext4.vhdx` was **1,326,448,640 bytes** at inventory time (dynamic allocation). The virtual disk's approximately 1007 GiB capacity may eventually constrain large runs even if T: has plenty of physical free space.
- Debian `vm.swappiness=60` was observed, **not changed**. It is **not** evidence of actual swapping. OS swap was 0 used immediately after the 1 GiB run; swap use/peak memory was not instrumented during all runs.
- `lscpu -e=CPU,CORE,SOCKET,ONLINE` shows SMT siblings (0,1) core 0; (2,3) core 1; (4,5) core 2; (6,7) core 3; and so on. **Logical CPUs 0,2,4,6 correspond to four distinct physical cores.**

### 3A.2 Measured 300-million-digit benchmark matrix

| Benchmark | y-cruncher `-M` **ceiling** | `-TD` and `-PF` | CPU launch affinity | Working RAM reported | Logical memory needed | Base converting | Base-conversion verification | y-cruncher start→end wall | Shell `time real` | Result |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| A: baseline | 1 GiB | `-TD:1 -PF:none` | none explicit | **947 MiB** | 1.00 GiB | **74.902 s** | 49.970 s | **151.780 s** | 153.406 s | `EXIT=0`, PASS |
| B: increased cache | 8 GiB | `-TD:1 -PF:none` | none explicit | **1.23 GiB** | 1.31 GiB | **65.029 s** | 47.920 s | **134.769 s** | 136.356 s | `EXIT=0`, PASS |
| C: four-way task queue | 8 GiB | `-TD:4 -PF:taskqueue` | `taskset -c 0,2,4,6` on wrapper | **1.24 GiB** | 1.31 GiB | **64.310 s** | 49.364 s | **136.334 s** | 137.730 s | `EXIT=0`, PASS; child affinity not directly inspected |

Other phase data (seconds):

| Benchmark | Golden Ratio calculation | Decimal output writing | Decimal-output verification | y-cruncher `Total Computation Time` (distinct from wall) | Logical swap-disk estimate | Decimal output estimate |
|---|---:|---:|---:|---:|---|---|
| A | 15.326 | 5.220 | 2.208 | 90.243 | 1.11 GiB | 286 MiB |
| B | 10.665 | 5.123 | 2.286 | 75.718 | 1.11 GiB | 286 MiB |
| C | 9.441 | 6.487 | 2.685 | 73.772 | 1.11 GiB | 286 MiB |

**Interpretation (bounded):** Increasing the RAM cap from 1 to 8 GiB at one y-cruncher task reduced measured overall y-cruncher wall time from 151.780 to 134.769 seconds (**17.011 s / 11.2% faster in this run**). At an 8 GiB ceiling, switching from one task to the four-way task queue gave 136.334 seconds, **1.565 seconds / 1.16% slower overall**, even though the calculation subphase improved 10.665 → 9.441 seconds. This is **one measurement per configuration**, not a statistically established performance ordering. Large base-conversion/verification costs and disk/cache variation plausibly mask modest compute-phase differences; do not infer that four cores are universally slower or that memory changes alone explain every second.

**Important small-workload limitation:** With `-M:8g`, y-cruncher reported only ~1.31 GiB **logical memory needed** for 300 million digits. Therefore a **12 GiB repeat at 300 million digits is unlikely to distinguish useful memory settings**; the owner's requested progression is to a larger but still bounded test before making claims about optimal RAM for 10^10/10^11. The 8 GiB value is a *cap*, not an observed 8 GiB allocation. The computed swap-disk requirement shown on the y-cruncher menu is a logical resource estimate; after successful completion the retained work directories primarily hold the decimal output and small reports.

**Four-core safety uncertainty:** The third test was launched with `time taskset -c 0,2,4,6 bash wsl_generate.sh --constant phi --digits 300000000 --mode swap --memory 8g --td 4 --run`, and the wrapper printed `FRAMEWORK=taskqueue`; y-cruncher printed `Task Queue -> 4 / ? / 24 (all cores)` and reported the full 0–23 hardware topology. The printed topology can reflect hardware discovery rather than actual affinity, **but it does not certify that every y-cruncher worker stayed within CPUs 0,2,4,6**. `taskset` sets an inherited Linux affinity mask; a child could change its affinity explicitly. Before treating the owner's four-core maximum as *verified enforced*, inspect `Cpus_allowed_list` for the **actual running y-cruncher worker threads** during a later bounded test. No such contemporaneous observation was supplied for this completed run. If any thread is permitted to run on more than the four selected CPUs, stop/adjust the next test rather than assuming `-TD:4` or the wrapper is a hard core cap. No evidence of a power-off was supplied for these completed runs.

### 3A.3 Exact run directories and current cleanup status

The owner first confirmed no running `y-cruncher` process via `pgrep -af y-cruncher` (no output) and removed three **old early-test directories** using an explicit `rm -rI` invocation, affirmatively answering its prompt: `/home/u/outlandish-test/phi_100k_ram`, `phi_1m_swap`, `phi_10m_swap`. No post-deletion `du` was supplied, so treat it as user-reported completion. The 100m reference `/home/u/outlandish-test/phi_100m_swap` (96 MiB) and T: `rehearsal_artifacts` (48 MiB) were **deliberately retained**.

The three **new** benchmark directories, each under `/home/u/outlandish-work/` (backed by T: VHDX), are:

```text
phi_300000000_20261107T102056Z_12274  # A, cap 1g, TD1
phi_300000000_20261107T102748Z_22348  # B, cap 8g, TD1
phi_300000000_20261107T104001Z_8098   # C, cap 8g, TD4 + taskset
```

Each contains an owner-reported `run.log`, the decimal `Golden Ratio - Dec - Newton.txt` (approximately 300 MB), and a small timestamped y-cruncher `Golden Ratio - *.txt` validation report. **These three 300m outputs have NOT been shown deleted.** Their run-specific text/report names and exact sizes should be listed before removal, since G: registration and packed conversion were *not* undertaken for the 300m tests.

**Safe cleanup plan, not yet executed:** First verify `pgrep -af y-cruncher` shows no running job; inspect `find /home/u/outlandish-work -maxdepth 2 -type f -printf '%p %s bytes\n'`. Copy **each attempt's `run.log` and timestamped validation report** to a unique, non-G: evidence directory, e.g. `/mnt/t/OUTLANDISH_WSL/benchmark_evidence/<run-dir-name>/`, verify copies/size/hash as desired, and only then delete the **three explicitly listed** attempt directories with interactive `rm -rI --` (no wildcards, and only after inspection). Retain the original 100m decimal source and packed references until the project decides to retire them. Do **not** delete `/home/u/outlandish-test`, the y-cruncher installation, `T:\OUTLANDISH_WSL\Debian\ext4.vhdx`, or any G: files. Deleting files inside WSL ext4 restores ext4 space but does **not necessarily shrink the physical VHDX immediately**; VHDX compaction is a separate, potentially hazardous administrative task, not automatically authorised.

### 3A.4 Next bounded optimisation stage (proposed, not executed)

1. Preserve the three 300m benchmark logs/validation reports and perform the inspected cleanup. Do not blindly remove earlier successful 100m rehearsal artifacts.
2. **Verify actual per-thread CPU affinity** during a subsequent benchmark, because a report showing `4 / ? / 24 (all cores)` by itself proves neither compliance nor noncompliance with the four-physical-core ceiling. Any future instrumentation must remain read-only and bounded; no blanket WSL processor count change is needed.
3. Select a **larger calibration workload**, starting with preview/resource examination around **10^9 golden-ratio digits** (not an automatic `--run`); `wsl_generate.sh` itself previews the command but **does not run y-cruncher's resource-estimation menu**. At `>=10^9`, launch additionally requires the exact `--ack-large-run N`; this safety interlock must be preserved. Consider comparing **8 GiB versus 12 GiB only if the reported logical memory/disk requirement is large enough to exercise both caps**. The old 300m benchmark was too small. Longer runs, other constants and 10^10/10^11 targets require separately checked resource limits and explicit authorisation.
4. For the longer-term large-target goal, owner is open to a conditional **~20 GiB WSL VM / 14–16 GiB y-cruncher** or **24 GiB WSL VM / ~18 GiB y-cruncher** configuration if host RAM pressure, disk I/O, performance and stability justify it. These settings are **options to evaluate**, not approved modifications; with only 32 GiB physical host RAM, Windows headroom matters. Current `.wslconfig` is absent; leave it unchanged until explicitly approved. Never rely on OS paging for y-cruncher's far-memory cache; retain native ext4 scratch backed by T: HDD.
5. Record CPU load, disk throughput/latency, actual working-memory/high-water use, Linux OS swapping and full elapsed phases; single-run timings are diagnostic, and a constant-specific 10^11 forecast remains unsupported by these 300m runs alone. The owner authorises **no more than four physical cores** for this work; do not let y-cruncher expand beyond them.

---

## 4. New owner-approved work order: first optimise WSL2 speed, skip old comparison, then packed registry

### PRIORITY 1 — optimise disk-backed y-cruncher for 10^10 and 10^11 (in progress)

**Objective:** Optimise *end-to-end* real-world generation on this host's T: HDD-backed WSL2, rather than benchmarking Windows versus Linux RAM-only operation or pursuing a RAM-disk solution by default. Targets are **10 billion** and potentially **100 billion** decimal digits, for **each of the six constants**. The slow constants (notably gamma) must be assessed separately; a phi-only tune is not a universal optimum. Prefer cost-effective measurable tuning and conservative host stability over speculative maximum CPU utilisation.

**Current hardware/starting facts:** Ryzen 9 3900X 12C/24T, 32 GiB host RAM, WSL2 reports 15.6 GiB usable, 4 GiB Linux OS swap, T: physical HDD with ~2.9 TB free in the 7-Nov check, ext4 virtual capacity ~1 TB. G: is a separate Windows production drive. Linux y-cruncher v0.8.7.9547 static works without `sudo` (warning about thread priority was nonfatal). Earlier native Windows higher-concurrency y-cruncher attempts caused sudden host power-offs. **Owner's ceiling is four physical cores; one and four have now been exercised at 300m with no reported host power-off.** Treat actual thread affinity as unverified (see §3A).

**Current y-cruncher configuration is a baseline, not a recommendation to run 10^10:** swap mode with `-verify:1`, explicit dedicated ext4 `-swap:raid0` path, per-attempt working directory. `wsl_generate.sh` defaults to `-TD:1 -PF:none -M:4g`; at `--td 4`, the **source snapshot** selects `-TD:4 -PF:taskqueue` (and the live launcher output confirmed this). `-M:1g` and `-M:8g` have been run at 300m; 4 GiB and 12 GiB were intentionally skipped at 300m. **No memory cap has been validated as optimum for 10^10/10^11.** The `--td` number governs task decomposition, *not* a verified OS-wide core cap. Four-core taskset experiment and unverified effective thread affinity are described in §3A.

**Known 10^10 phi interactive resource indications (not a completed run):** RAM-only menu predicted ~41.0 GiB memory. Swap-mode menu initially predicted **14.1 GiB** memory and **37.0 GiB logical swap plus 17.0 GiB output** (its displayed output estimate need not equal the exact final raw-text length). An attempted interactive **`4GB`** memory entry was **not reliably validated**: the menu later showed **79.7 MiB**, *not* the intended 4 GB; the subsequent accidental 10^10 launch used only ~2.76 MiB working memory and was stopped with Ctrl+C. Treat `-M:4g` as **unproven** until checked in a safe dry run / preflight. No process remained afterward; a ~21 MiB `ycs-0-0` scratch folder was identified. Its later removal was proposed, **not confirmed** in the evidence available here.

**RAM-disk assessment:** Do **not** assume a RAM disk (`tmpfs`) is optimal. It would draw from the same ~15.6 GiB WSL2 RAM already needed for y-cruncher's cache, page cache and OS. It cannot accommodate likely multi-tens-of-GiB swap sets at 10^10 or potentially far more at 10^11. Start with native ext4 scratch on the T:-backed VHDX and optimise y-cruncher's direct working-memory allocation and I/O behaviour. Compare a RAM disk only if a bounded benchmark and measured headroom demonstrate a plausible benefit; never size `tmpfs` for an unbounded production run. Do not confuse y-cruncher's managed **disk swap** with Debian's 4 GiB **OS swap**.

**Proposed safe, reversible tuning sequence (items 1 and initial 300m portions of 3–5 have been executed; see §3A for actual evidence):**

1. **Read-only inventory:** Record existing `.wslconfig` state (if any), `free -h`, `df -h /`, physical T: free space, virtual VHDX capacity, CPU/core counts, Windows host responsiveness and power/thermal baseline. `.wslconfig` changes affect the entire WSL2 VM, not only Debian. No Windows privilege grants.
2. **Preflight estimates:** For phi, e, pi, log2, gamma, and the full-perimeter y-cruncher lemniscate source, inspect estimates at 10^10 and 10^11 (10^9 as helpful calibration), with exact digits/output format. Prefer safe tool previews. Interactive menu entry **`0` at top-level custom compute starts the calculation**; do not repeat the accidental launch. Do not assert uniform algorithms or resource usage among constants.
3. **Bounded benchmark design:** Choose one or more representative external-memory jobs **after resource preflight**, with explicit owner-approved maximum digits, scratch cap, memory cap, CPU/affinity setting, expected disk use and stop conditions. Avoid launching 10^10/10^11 just to measure a setting. Use unique create-only scratch paths, leave ext4 swap free space and G: production untouched.
4. **Observe bottlenecks:** Measure true start-to-end wall time, y-cruncher computation vs base conversion/output verification, CPU utilisation, peak WSL/process memory, Linux OS swap activity, disk throughput/latency, T: and G: I/O and host responsiveness. Distinguish cold and cache-warm runs and expensive HDD seeking; account for filesystem caching and report temperature/power concerns.
5. **Tune one variable at a time:** Initial 1 GiB versus 8 GiB memory and TD1 versus TD4 comparisons have been completed at 300m. For a **larger representative workload**, explore memory caps up to 12 GiB under the current VM where justified, then consider conditional 14–18 GiB caps only with reviewed WSL memory expansion and host headroom; also assess far-memory seek/I/O strategy and filesystem/disk placement. Respect the owner's four-core maximum and verify the effective worker affinity. WSL VM memory/processors settings require separate explicit approval and a controlled `wsl --shutdown` restart after backing up `%UserProfile%\.wslconfig`.
6. **Compare and project conservatively:** For every constant and digit target (10^9 / 10^10 / 10^11) report observed configuration, verified results, file sizes, full run phases and tentative time ranges, each clearly labelled **measured**, **interpolated/extrapolated**, or **unknown**. A 100m HDD-swap phi run does not calibrate a 100b gamma job.
7. **Do not launch full production by implication.** Separate explicit owner sign-offs for the first real 10^10/10^11 compute, each large storage allocation, and any later G: packed promotion. Preserve small reports/logs and verify process exit before deleting failed scratch.

**Speed/efficiency considerations:** More *actual RAM* dedicated to y-cruncher's disk cache may reduce I/O; excessive allocation can trigger Linux OS paging and catastrophic HDD thrash, so preserve headroom. Physical RAM disks do not create more RAM. Direct Linux-to-NTFS packed output on `/mnt/g` minimises copies, but its real conversion/write throughput and durability must be measured against local ext4 and NTFS behavior before declaring it optimal. A failed conversion retains text and must not overwrite any staged destination. A full scan provides a later whole-file hash without an extra verification-only pass.

**Projections and file sizes:** The verified N-to-bytes relationship above is exact. The historical native-Windows 10^9 golden-ratio/e/pi/log2/gamma timings were collected under different modes/settings and can be listed as **context**, not as calibrated WSL swap timing. In particular the old `RESOURCE_ESTIMATES.md` contains illustrative non-linear compute scaling that deliberately excludes major disk-I/O effects; do **not** present its 10^10/10^11 numbers as expected wall times. Compute and log actual per-constant resource estimates first.

### PRIORITY 2 — SKIPPED by owner

Do **not** run a comparative performance project for legacy one-byte-per-digit scanning versus nibble-packed scanning. Packed is adopted on its storage merits; continue normal correctness tests and collect the new scanner's ordinary throughput as part of actual work. The historical legacy scanner remains valid for existing byte-format files.

### PRIORITY 3 — after performance optimisation: safe packed production integration

Implement a separate **versioned** packed-format registry/manifest and guarded staging, prefix-compatibility and promotion flow for **G:**, using current proven WSL code under E: and T: as the non-destructive testbed. Requirements:

- Bind constant ID, decimal digit count, format `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, exact byte count, content digest, provenance/receipt and active identity. Reject mixed packed/byte declarations and invalid odd-nibble padding.
- Before promoting a 10^10 packed replacement, compare its **entire first 10^9 digits** to the existing active byte-per-digit original, reading/decoding in bounded chunks; compare at every original decimal-digit offset, not a few samples. Prove rejection on prefix mismatch and unchanged production state.
- Keep a clean isolation boundary: tests, collisions/crash/recovery/retry and deliberately corrupted staged files on T:; no test registry bound to live G: state. Do not change the six current G: originals or original TOML until explicitly reviewed and authorised.
- Define atomic create-only staging and validated commit, no overwrite, clear orphan/recovery states, and an explicit idle/reader-interlock policy. Legacy `[state.active]` and `[state.pending_retirement]` fields and `[settings.retention] delete_superseded = true` must **not** silently auto-retire the existing byte files. Decide backup/retention before a real packed promotion; no automatic original deletion without a separate owner decision.
- Preserve the reduced-verification intent, but be explicit about the *one required persisted integrity assurance before promotion*: a valid full-scanner hash/receipt or an integrated read/compare that hashes the staged packed file; sample-only evidence is not enough for a destructive replacement. No unnecessary duplicate complete reads.
- Complete integration tests, negative tests, isolated realistic rehearsal and review before any G: production registration. 100m packed rehearsal is **not** eligible to replace 10^9 active files because it is shorter.

## 5. Scientific scope and deferred Powerball/Oz Lotto enhancement

The Powerball `POWERBALL_preholdout_only.csv` contains **433 eligible draws, 1144–1576**, held-out cutoff exclusive **1577**. The new packed scanner currently preserves P1 (seven mains in operator-drawn order + PB), P2 (seven mains in operator-drawn order), and P3 (any six of the seven main balls in any order + PB), searching every decimal-digit offset including odd nibble alignment. It reports actual positions and transitions; no post-holdout outcomes are used in development. Keep games strictly separate.

The owner separately approved **deferred** additions for *both* games in `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md`: report drawn-order, any-order and reordered-only variants for P1/P2/P3 and proposed Oz Lotto O1/O2/O3, preserving original categories and non-double-counted totals. Oz Lotto O2/O3 supplementary-ball positioning and selection order remain **unsettled**, as does an actual Oz Lotto scanner/data adapter. **Do not implement these during performance optimisation or packed registry integration unless the owner re-prioritises.** No conclusion of predictive validity from chance positional hits.

## 6. Immediate next-chat handoff, authorisations and non-goals

**Do next:** Priority 1 is **under way**. The read-only resource inventory and three 300m phi benchmarks are completed; see §3A. **First** preserve per-run `run.log` and small validation reports from the three exact 300m directories, then inspect and remove only those superseded **large decimal outputs** via deliberate, named-path cleanup. **Second** design a bounded, larger representative benchmark (preview around 10^9 phi), explicitly measuring real memory use, I/O and actual worker-thread CPU affinity before relying on the four-core ceiling; retain the wrapper's preview / exact large-run acknowledgment. Before any new command, inspect the installed `wsl_generate.sh` and verify the working and output paths. Do not launch 10^10/10^11, change `.wslconfig`, lift four-core ceiling, or touch G: because this handover suggests future evaluation.

**Do not do:** Windows Sandbox revival; alternative VM installation; native-Windows volume privilege change; conversion of the six old G: binaries; legacy-versus-packed performance benchmark; speculative Oz Lotto scanner development; changes to protected research project's holdout or governance; automatic registration or predecessor deletion.

**Preserve:** `OUTLANDISH_01_2026-11-07_Project_Status_and_WSL2_Primary_Design_v3.md`, historical v2/v1 and 5-November bundle, `OUTLANDISH_WSL_Packed_v0_2r2` source and its change notes, `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md`, and optionally the separate short `OUTLANDISH_WSL_2026-11-07_Baseline_and_Revised_Priority_Plan_v0_1.md`. This v5 is the single **current handover**, not the source of truth for generated state.

---

# Part II — retained earlier baseline and Windows Sandbox evidence (historical)

The sections below are preserved substantially from the 7-November v2 handover to avoid losing technical details, safety rationale or evidence. **They describe the state *before* WSL2 installation and should not be read as current instructions where they say WSL is merely planned or name v2 as the latest handover.** Part I of **v5** is the current authority for next actions and architecture; current source/TOML remain authoritative for implementation.

## 1. Project identity, scope and division of work

- GitHub repository: `https://github.com/hydra3333/analysing_perceived_randomness_in_reality`.
- OUTLANDISH source directory **now**: `GAIS/OUTLANDISH_01/` at repository root, not the former `src/GAIS/OUTLANDISH_01/`.
- Primary host: Windows 11; Ryzen 9 3900X (12 physical / 24 logical processors), 32 GiB RAM. Repository and main project virtual environment live on E:; large digit data and OUTLANDISH run artifacts live on G:; T: is a separate WD Black HDD with substantial space, reserved for possible WSL/Sandbox trials.
- OUTLANDISH_01 is an **independent, speculative mathematical-constant digit-stream thought experiment**. It is not the governed E_1..E_62 main predictive-randomness method suite, and it does **not** demonstrate lottery predictability. It nonetheless preserves the independent pre-holdout dataset and does not inspect held-out outcomes in development.
- The owner has authorised direct development/testing of this standalone OUTLANDISH workstream; do **not** infer authority to change the main research project's methods, orchestration, scientific gates, or held-out data.
- The owner strongly prefers pragmatic, reviewable implementations, precise claims, no fabricated runtimes or verification, and command-line procedures appropriate to Windows CMD. Code/diagnostic changes should be isolated and should not unnecessarily proliferate administrative machinery.

## 2. Established pre-Sandbox implementation: what is already in place

### 2.1 Main files and roles

Located under `GAIS/OUTLANDISH_01/` unless stated otherwise:

| File | Role |
|---|---|
| `outlandish_big_constants.py` | Native-Windows y-cruncher launcher, digit conversion, verification and registered `pipeline`; supports previews and explicit `--run`. |
| `outlandish_artifacts.py` | Shared artifact paths, pre/postflight safeguards, active-digit registry, verification, promotion, locking, retirement and recovery. Installed version reported as **v0.2r4**. |
| `outlandish_config.py` | TOML parsing / configuration helpers. |
| `outlandish_powerball_stage_a.py` | Fixed-width, NumPy-vectorised digit scanning and reports for the Powerball historical pre-holdout dataset. |
| `test_outlandish_v02.py` | Standalone regression tests and synthetic safety cases. |
| `outlandish.local.toml` | **Intentionally Git-tracked** local configuration **and machine-maintained active-digit registry**. User section may be edited deliberately; generated state must not be hand-edited. |
| `POWERBALL_preholdout_only.csv` | Pre-holdout-only development data; not a live-results fetcher. |
| `OUTLANDISH_01_v0_2_README.md`, `README.md` | Operational reference; inspect the installed version before relying on old handover excerpts. |
| `generate_1e10.cmd`, `scan_1e9.cmd`, `scan_1e10.cmd` | Convenience launchers; check their current contents and preview semantics before running. |
| `y-cruncher v0.8.7.9547b/` | Local Windows y-cruncher installation, **ignored by Git**. Contains binaries/libraries. |
| `ycruncher_digits/` | Legacy local folder; ignored, not the active large-artifact root. |

The historical standalone handover spec, old v0.1/v0.2 installers and earlier 10^10 README versions are **not** superior to the installed v0.2r4 code, TOML and README. Some older text predates G: relocation, automatic retirement, and the new GAIS root path.

### 2.2 Six constant streams and encoding

| CLI ID | Constant | First digits (decimal point shown for explanation only) |
|---|---|---|
| `pi` | π | `3.1415926535...` |
| `phi` | Golden ratio | `1.6180339887...` |
| `e` | e | `2.7182818284...` |
| `log2` | ln 2 | `0.6931471805...` |
| `gamma` | Euler–Mascheroni γ | `0.5772156649...` |
| `lemniscate` | **Half-perimeter** lemniscate constant | `2.6220575542...` |

Each output file contains **one numeric byte 0–9 per decimal digit** (NOT ASCII `'0'`–`'9'`), beginning with the integer digit and containing **no decimal point**. Thus a `10^9` file has exactly 1,000,000,000 bytes; a `10^10` file will have 10,000,000,000 bytes.

**Lemniscate convention matters:** the y-cruncher built-in source returns approximately `5.244115...` (full perimeter). The OUTLANDISH Python converter applies an exact streaming division by 2 to obtain the chosen `2.622057...` stream before verification and registration. Do not silently change this convention.

### 2.3 Existing large-file state, G:

The owner reported that **all six** constants had successfully completed native-Windows RAM-only pipelines to **10^9 digits each** by the end of 2026-11-06. The six 1,000,000,000-byte binaries were verified and registered active; no pending retirements remained at that checkpoint. This is **owner-reported and previously checked in conversation**, not freshly revalidated by this handover.

Established live artifact parent:

```text
G:\OUTLANDISH_01\large_artifacts\
    digits\       six registered, verified 10^9 numeric-byte binaries
    scratch\      calculation attempts, retained small reports
    staging\      in-progress candidates
    results\      scanner reports
    logs\         receipts and diagnostics
```

Important controls:

- Read the current `outlandish.local.toml` and run `python outlandish_artifacts.py status` / `audit` before new operations. Its `[state.active]` and `[state.pending_retirement]` are **program-generated; do not manually edit**. A `.toml.bak` is only the previous registry snapshot, **not** a backup of the big binaries.
- Live owner policy: `[settings.retention] delete_superseded = true`. In **v0.2r4**, after successful replacement validation and an atomic state publication, precisely the verified predecessor may be auto-retired. This is **not** an authorisation to manually delete files or bypass lock/identity checks. Third-party readers must be idle.
- Registered active files must be strictly extended; a second same-length `pipeline` is not an appropriate test. Full previous-prefix comparison is required for promotion. On handled failures, owned large scratch/intermediates are cleaned but small error evidence remains; crashes may leave recovery material.
- The output location and generated-large-file audits are important. The old project had an accidental history of large generated files under Git-tracked paths; that has been corrected. Large files should not be reintroduced into Git.
- The root `.gitignore` covers OUTLANDISH large artifacts and local y-cruncher, including `/GAIS/**/*.bin`, `/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/`, and `/GAIS/OUTLANDISH_01/ycruncher_digits/`. Confirm the latest ignored-root entry in the current repository if relevant.

### 2.4 Known native-Windows execution characteristics

- Installed y-cruncher version: `v0.8.7.9547b`.
- Owner observed actual **hard instantaneous power-offs** under some higher-concurrency y-cruncher settings. `-TD:4` was used for the established stable runs and is the cautious default for follow-up tests. **`-TD:4` sets y-cruncher's task decomposition, not a strict four-OS-thread/core cap**; observed CPU usage can exceed four cores. Do not raise it automatically or suggest stress tests to find a failure threshold.
- With `[settings.generator] mode = 'auto'`, the installed implementation selects RAM mode for inputs **below** 5 billion digits and disk-swap mode at/above that boundary. `[settings.generator] memory_gib` concerns requested working memory in swap mode, **not** a RAM cap for normal RAM-only calculations.
- The live `[settings.generator]` values must be read from current TOML; historical README examples vary (`threads = 4` and `threads = 12` both appear in different explanatory contexts). Do not infer current live settings from a README example.
- `ycruncher_verify_output = false` was selected in the newer pipeline for speed. Python format, reference-prefix and full SHA-256 checks remain, but **do not independently re-prove newly computed mathematical digits**. Preserve this limitation in scientific claims.
- Owner-supplied order-of-magnitude 10^9 generator observations: `phi` ~15 s y-cruncher; `e` ~44 s; `pi` ~71 s; `log2` ~180 s; `gamma` ~2,447 s (~41 min); lemniscate on the scale of minutes. These are individual observed runs, **not** credible extrapolations to 10^10/10^11 disk-backed computation.

### 2.5 Tests and evidence

Earlier native-Windows owner test run of `test_outlandish_v02.py`: **25 tests total**, 24 PASS and one allowed symlink skip. Separate generator/scanner self-tests existed. The full set of real 10^9 promotions was reported complete and the project committed/pushed; no 10^10 real run has been demonstrated.

`status` reflects registry metadata; `audit` checks path/placement/symlink/large-file safety. Neither substitutes for a **new** full-byte verification of every binary. Full-source digest verification happens in the relevant pipeline/whole-active-file scan paths.

## 3. Established Stage-A Powerball exploration

- Historical Powerball **pre-holdout only**: **433 draws, draw numbers 1144–1576**, cutoff exclusive `1577`. No later draws in development scans.
- Each selected ball is exactly two decimal digits (`03`, `12`, etc.). Search scans **every possible digit-byte offset**, including odd alignment and chunk boundaries.
- Pattern definitions:
  - **P1:** all seven main numbers in operator-drawn order, plus Powerball.
  - **P2:** all seven main numbers in operator-drawn order.
  - **P3:** any six distinct main numbers in any order, plus Powerball.
- A measured **π 10^9** run with `chunk_bytes = 4,000,000` took **27.278917 s** of scan time, yielding **P1=0, P2=0, P3=29**. This result is descriptive only, not evidence of causal structure or predictive power. A one-trillion-byte scan estimate based on it is merely a rough scan-only extrapolation, not a generation forecast.
- Scans use the OUTLANDISH-only historical CSV and do not pool games or consult future/holdout outcomes. The various other-constant scan statuses and report results should be read from the actual reports rather than assumed complete from the existence of six digit binaries.

## 4. Pre-Sandbox open problem: moving from 10^9 to 10^10 (possibly 10^11)

### 4.1 Windows y-cruncher disk-swap privilege obstacle

A 10^10 computation generally exceeds the comfortable 32 GiB RAM-only budget, making y-cruncher's **disk-backed swap mode** necessary. On native Windows, y-cruncher requested **`SeManageVolumePrivilege`** (“Perform volume maintenance tasks”) to use `SetFileValidData()` when preparing large swap files. A conventional non-elevated user did not have the needed privilege. The exact y-cruncher command / performance and safe swap-mode operation remain **untested for a substantive real 10^10 calculation**.

This privilege is security-sensitive and is **not restricted merely to T: or G:**. Do not casually grant it to the everyday user or change system policy. The owner considered a temporary grant/relogin/revoke sequence, but deferred it, preferring a potentially safer Linux route. No authorisation to alter this privilege has been given in this handover.

### 4.2 Research on replacement external-memory numerical engines

The owner sought a **mature, reusable** alternative capable of 10^10–10^11 digits, not a new numerical-HPC software project. Research included FLINT/Arb, python-flint, GMP, apfloat, TachusPI, binary splitting, external-memory FFT, and specialized constant algorithms. An external AI's initial report contained substantial errors and overconfident predictions; a requested correction concluded **NO-GO for a new independent engine**, **GO for further y-cruncher evaluation**. The corrected conclusion is a research judgment, **not** proof that no alternative can work. A function that streams a slice of output still may require enormous RAM to compute the preceding digits.

### 4.3 Historical pre-WSL planning notes — superseded by current results

Before diverting to Windows Sandbox, the preferred next *exploratory* route was the **Linux edition of y-cruncher under Debian/WSL2**, potentially avoiding Windows's `SetFileValidData()` requirement.

Known WSL host observations at that time:

```text
WSL version 2.5.7.0; kernel 6.6.87.1-1
Default WSL version: 2
No Linux distributions installed
```

The owner selected **Debian** rather than Ubuntu. Intended *host* area: `T:\OUTLANDISH_WSL\Debian\` holding the guest ext4 VHDX and Linux-side y-cruncher/swap scratch, without repartitioning or formatting T:. The six active result binaries remain on **G:**. Host T: was reported to have approximately **2.62 TB free** at the time; verify current free space before allocating anything.

Important planned controls:

- Complete the owner's **comprehensive backups and recovery-media checks** before Linux installation, privilege edits, disk-layout work, or heavy stress tests. The exact **current** backup completion status should be confirmed with owner; do not infer it from this handover.
- Before WSL installation set/inspect `.wslconfig` memory and WSL **VM swap-file location**, which otherwise may use C:. Beware of WSL virtual-disk max size and dynamic VHDX growth; verify current Microsoft guidance rather than assuming 2.62 TB is automatically addressable.
- Test Linux y-cruncher CLI and external-memory scratch on the ext4 filesystem. `/mnt/t` Windows/WSL cross-filesystem I/O is not equivalent to native ext4 random I/O and may be much slower. Preserve established converter, verification and registry contracts; a **new** Linux-runner integration is not installed.
- Start with a small Linux execution smoke test, then a calculation proven to exercise swap (small 10^5/10^6 calculations may not), then evaluate storage, speed and safety. No guessed runtimes for 10^10 or 10^11.
- `wsl --unregister Debian` would **delete** the Debian guest/data. Do not use casual cleanup commands against a live guest or running computation.

### 4.4 Remaining work (historical pre-Sandbox list; updated current plan in §7)

1. Protect the existing production source/TOML and six verified G: binaries; confirm backup/recovery readiness.
2. Establish a controlled, genuinely disk-backed y-cruncher execution mode (Debian/WSL2 was preferred; native Windows temporary privilege only with explicit owner decision; Windows Sandbox has now been abandoned as an unsuccessful test environment).
3. Verify scratch/data placement, required temporary capacity, runtime characteristics, bounded concurrency, log evidence, and uninterrupted/restorable behaviour before long calculations.
4. Assess feasibility and resource budgeting **per constant**, particularly much slower `gamma`; don't jump directly to six 10^10 calculations or extrapolate RAM-mode timings.
5. Integrate, if necessary, a reviewed Linux / external-swap generation adapter feeding **the same numeric-byte, verified, registered files** on G:, with safe restart/cleanup semantics. Do not bypass the existing content and predecessor-prefix integrity checks.
6. Only then generate larger numbers and use the pre-holdout scanner; interpret matches with chance baselines and guard against exploratory overfitting.

## 5. Safe baseline commands on the original Windows project

These commands are for the original **native project** with its actual project-root `.venv` activated, executed from `GAIS\OUTLANDISH_01`. They are **not** an instruction to run now without reviewing state. Commands without `--run` do not start the real generator.

```bat
python outlandish_artifacts.py validate
python outlandish_artifacts.py paths
python outlandish_artifacts.py status
python outlandish_artifacts.py audit
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test
python test_outlandish_v02.py
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000
```

Do not issue the final command with `--run` until swap privilege/WSL adapter, storage, disk budget, safety and owner approval have been addressed. In particular, never run an unverified same-length `10^9` promotion against an already active 10^9 binary.

## 6. Repository and evidence boundary

The Git repository underwent a **completed** GAIS relocation and targeted history rewrite on 2026-11-06. Its authoritative record is under `exchange/HISTORY_CLEANUP_2026_11_06/` (including `CLOSEOUT.md` and `commit-map.txt`). Old references to `src/GAIS` and old pre-rewrite Git SHAs in earlier records are historical, **not** necessarily current locations or commit identities. Handover material from before v0.2r4 must not be read as the latest code state. The owner reported a committed, pushed clean state for OUTLANDISH after the six 10^9 files were established, but the new chat should inspect actual status rather than assuming today's working tree is unchanged.

---



---

## Historical Appendix A — Completed Windows Sandbox experiment: configuration and scope

**Purpose:** Test the Windows y-cruncher/OUTLANDISH pipeline on `10^5 = 100,000` golden-ratio digits in an isolated disposable Windows Sandbox, with copied source on T: and scratch/results under a separate T: data tree. Goal was to avoid native Windows's disk-swap privilege at larger sizes. **Outcome: the real test never computed digits; Windows y-cruncher failed at process load time.** This appendix is forensic/historical. Its T: files were being deleted at owner's decision and should not be presumed available.

## A.1 Snapshot of host-to-guest setup (historical, not to recreate by default)

```text
HOST (T:)
T:\OUTLANDISH_01_SANDBOX\                 copied stand-alone source, local y-cruncher, PYTHON/, SANDBOX/
  PYTHON\python-3.15.2-amd64.exe         installer
  PYTHON\000-Pip-Install-Dependencies.bat   owner's full dependency BAT (v5 later edited for compiler)
  SANDBOX\OUTLANDISH_01_sandbox.wsb
  SANDBOX\OUTLANDISH_01_Setup.bat
  SANDBOX\OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat
  SANDBOX\OUTLANDISH_01_Python_Env.bat
T:\OUTLANDISH_01_SANDBOX_DATA\            writable test-data tree
  python_candidate\Python315\          installed Python and pip; persisted between guest restarts
  outlandish_run\large_artifacts\     separate scientific data root

GUEST
C:\HOST_OUTLANDISH_SOURCE\          read-only mapping of first T: tree
C:\HOST_OUTLANDISH_DATA\            writable mapping of second T: tree
C:\HOST_SOFTWARE\                  read-only host software/Notepad++ mapping
C:\OUTLANDISH_WORK\                disposable cloned source, y-cruncher, test TOML
```

The .wsb mapped folders correctly. GUI and user preferences were re-applied by startup, while the guest C: filesystem, Windows registry and installed system toolchains were discarded on closing Sandbox. The host-mapped T: data retained any changes made there, including pip updates and installed binaries. **Never confuse this with isolation from the host writable folder.**

The owner originally had nine Explorer registry preferences, a Notepad++ context-menu integration and desktop shortcuts; early assistant setup packages inadvertently removed them, then restored them. Explorer **compact view** (`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\UseCompactMode = 1`) was explicitly added. Three shortcuts were verified:

```text
HOST_software.lnk
HOST_OUTLANDISH_01.lnk
HOST_OUTLANDISH_DATA.lnk
```

The first `.bat` used VBScript through `cscript` and failed because the guest lacked a `.vbs` script engine; PowerShell with `WScript.Shell` COM `CreateShortcut` succeeded. A subsequent automatic setup with **no pauses**, logging and no Python install passed all five startup stages. Manual scripts were separate and allowed diagnostic pauses. **No files or settings in the T: Sandbox test should be installed into E: production.**

## A.2 Python on ephemeral C: — extremely slow and ultimately invalid

A Windows Sandbox guest ran Python installer `python-3.15.2-amd64.exe` (owner-selected **per-user** standard location, PATH on, without documentation, Tcl/Tk/IDLE, Python test suite or standard-library precompilation). The installer took an unusually long time. The initially successful test reported:

```text
C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python315\python.exe
size: 105,696 bytes
Python 3.15.2
pip 26.2.2
```

Existing CMD didn't pick up new PATH until the owner explicitly added Python315 and `Scripts` directories. The original full pip BAT later produced Windows's blue **"This app cannot run on your PC"** popup, pip launcher failure and `Access is denied`. At 10:36 local, `dir` reported **`python.exe` = 0 bytes**. `certutil -hashfile` failed with `0x800703EE` / Win32 1006 `ERROR_FILE_INVALID` (*"volume ... externally altered ... opened file ... no longer valid"*). This proves an invalid executable, **not its cause**. The exact process that truncated or invalidated the file was never identified. Do **not** infer host T:/G: corruption from it.

System event query for IDs 55/98/153/7 returned `Microsoft-Windows-Kernel-Processor-Power` Event 55 (**informational CPU power-management capability**), not NTFS disk corruption. Defender Operational queries for events 1116/1117 returned no output; no Code Integrity enforcement event was established. An empty or broad event query cannot prove the absence of relevant security or volume events.

## A.3 Persistent Python on T: — demonstrated feasible

A later candidate used Windows Python installer's documented `TargetDir` to install once under:

```text
C:\HOST_OUTLANDISH_DATA\python_candidate\Python315
(Host: T:\OUTLANDISH_01_SANDBOX_DATA\python_candidate\Python315)
```

Python installation returned **exit code 0** with the owner's requested exclusions. Direct startup and `-m pip` worked; its `sys.prefix` and `pip` `Lib\site-packages` both resolved within the T: mapped tree. A baseline SHA-256 was saved. A fresh Sandbox restart **independently passed** the provided `VERIFY` phase. Another restart after substantial dependency updates also passed:

```text
Python 3.15.2
pip 26.3
sys.prefix = C:\HOST_OUTLANDISH_DATA\python_candidate\Python315
site-packages = C:\HOST_OUTLANDISH_DATA\python_candidate\Python315\Lib\site-packages
```

`numpy` imported successfully at version **2.5.4**, and owner reports also confirmed Scipy/pandas imports in dependency checks. This is a *real positive result*: a Python installation and packages **can** remain usable across Windows Sandbox restarts when the guest mapping path is stable. The path used for temporary downloads/builds was under `%TEMP%` (disposable C:), which does **not** mean pip's final installation went there. This positive result **did not fix the y-cruncher launch failure** and is not a recommendation to retain Sandbox.

## A.4 Full owner dependency BAT: not required for OUTLANDISH smoke; compiler failure

The owner's original `PYTHON\000-Pip-Install-Dependencies.bat` requested many upgrades, `--upgrade-strategy eager`, `pip-review --auto`, and packages not used by OUTLANDISH. It also contained a bad `python -m python -m pipdeptree` command, which a later draft proposed correcting. The owner expressly wanted the original package list preserved; early assistant NumPy-only substitutions were rejected. One replacement v5 included compiler installation/prerequisites and fail-fast pip error tracking, but this was a Sandbox-only candidate, **not** part of the main project requirements.

A supplied pip log of 1,605 lines showed **six build failures for five distinct packages**:

| Package | Attempts failed | Interpretation |
|---|---:|---|
| PyYAML | 2 | Compiled extension build attempted; missing MSVC toolchain |
| inflate64 | 1 | Compiled archive dependency; missing compiler |
| pybcj | 1 | Compiled archive dependency; missing compiler |
| pyppmd | 1 | Compiled archive dependency; missing compiler |
| pyahocorasick | 1 | Compiled pattern-matching extension; missing compiler |

Representative error:

```text
error: Microsoft Visual C++ 14.0 or greater is required.
Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**This is not a VC++ Redistributable runtime failure.** These packages fell back to compiling from source on Python 3.15 because suitable wheels were unavailable/unsuitable at the time. Many other packages, including NumPy 2.5.4, SciPy and pandas, were usable. OUTLANDISH's scanner uses NumPy; generation is primarily standard-library Python plus external y-cruncher. The five failed packages were **not a demonstrated prerequisite** of the `10^5` OUTLANDISH test.

Attempted Build Tools installer (`vs_BuildTools.exe`) ran the Visual Studio Installer on Sandbox disposable C: and made very slow progress, **stalled at 35% / package 149 of 268**, and was abandoned by closing the entire Sandbox. That is an **abandoned incomplete install**, not proof that Microsoft's toolchain would never install. No completed compiler toolchain survived the guest restart. The owner decided not to spend further effort on full dependency/toolchain installation.

## A.5 OUTLANDISH smoke tests: 25 tests individually accounted for

After the successful persistent Python setup and source copy, the complete Python suite ran:

```text
Ran 25 tests in 51.830s
24 passed ('ok'), 1 ERROR: test_all_launchers_use_manifest_not_hardcoded_drive
FileNotFoundError: C:\OUTLANDISH_WORK\scan_1e9.cmd
```

The failure was **packaging**, not computation: the startup copy routine omitted the three launcher `.cmd` files. The owner copied `scan_1e9.cmd`, `scan_1e10.cmd`, `generate_1e10.cmd` from read-only source to C: worktree and reran the one failing test:

```text
Ran 1 test in 0.013s
OK
```

Therefore **each of the 25 tests passed in aggregate**, but a full 25-test run was **not repeated after copying**. Do not misreport a single clean 25/25 suite execution. The full suite was slow (~52 s) in the mapped persistent Python environment; this does not directly measure numeric calculation performance.

## A.6 Artifact audit and correct test data root

The original clean test TOML had:

```toml
[settings.storage]
main_root = 'C:\HOST_OUTLANDISH_DATA'
```

OUTLANDISH's audit correctly identified **eight unsafe misplaced entries** within `python_candidate`, including large NumPy/SciPy DLLs (`~20 MB`) and `chardet` `.bin` model files. The audit was working as specified; the configuration wrongly placed **all persistent Python files beneath a scientific-artifact-scanned root**. Nothing was deleted and audit rules were not bypassed.

The owner fixed only the test TOML and created a separate root:

```toml
[settings.storage]
main_root = 'C:\HOST_OUTLANDISH_DATA\outlandish_run'
```

```text
T:\OUTLANDISH_01_SANDBOX_DATA\
   python_candidate\Python315\        (outside the audit root)
   outlandish_run\large_artifacts\    (scientific-only subtree)
```

Then:

```text
ARTIFACT AUDIT PASS (standalone audit): no misplaced generated/large files
CONFIG C:\OUTLANDISH_WORK\outlandish.local.toml root=C:\HOST_OUTLANDISH_DATA\outlandish_run
pi/phi/e/log2/gamma/lemniscate: active=NONE pending_retire=NONE
```

The generator's `phi --digits 100000` **dry run passed**, reporting the exact CLI and `-TD:4`:

```text
[phi] TARGET: 100,000 digits INCLUDING integer digit.
[phi] MODE=RAM THREADS_REQUESTED=4 (TD task decomposition, not strict OS thread count)
[phi] COMMAND: "C:\OUTLANDISH_WORK\y-cruncher v0.8.7.9547b\y-cruncher.exe" custom goldenratio -dec:99999 -hex:0 -od:1 -compress:0 -verify:0 -mode:ram -TD:4 -PF:taskqueue
[phi] DRY RUN: nothing launched or modified.
ARTIFACT AUDIT PASS (post-run): no misplaced generated/large files
```

The `-dec:99999` argument yields exactly **100,000 digits including the integer digit**. This was a correct preview and does **not** mean the actual digit output existed.

## A.7 Actual y-cruncher invocation: launch failure, no generated digits

The owner then ran:

```bat
python outlandish_big_constants.py pipeline --constant phi --digits 100000 --run
```

It completed only the safe Python preflight and y-cruncher launch step. y-cruncher immediately failed:

```text
[phi] y-cruncher exit code=3221225595; wall=0.1s
[phi] FAILURE CLEANUP: removed 0 failed-run data file(s); kept small reports
ARTIFACT AUDIT PASS (post-run / error-path): no misplaced generated/large files
ERROR: y-cruncher exit 3221225595
```

**Interpretation:** `3221225595` (unsigned) and `-1073741701` (signed) are both `0xC000007B`, Windows `STATUS_INVALID_IMAGE_FORMAT`. Likely failure to load an executable image or dependency/DLL. That code is not a mathematical failure, Python artifact-registry failure or disk-swap privilege failure. Its **specific cause was not determined**.

Direct execution of `C:\OUTLANDISH_WORK\y-cruncher v0.8.7.9547b\y-cruncher.exe` likewise printed nothing and returned `-1073741701`. Given the very recent y-cruncher Windows launcher and suspected runtime dependency, the owner attempted the official Microsoft VC++ **x64 Redistributable** (`vc_redist.x64.exe`) from the source SANDBOX mapped folder. Its installation appeared very slow; it was launched with `start` (asynchronous), and **successful installation was never conclusively verified**. Running y-cruncher afterwards still produced `0xC000007B`. Do **not** claim the correct Redistributable was definitely installed and failed to fix it; equally do not claim that `STATUS_INVALID_IMAGE_FORMAT` proves a missing runtime is the sole cause.

This is the decisive failure of the Sandbox experiment. The zero-byte ephemeral C: Python issue was separate; the **persistent Python actually worked well enough for all Python tests and checks**. Running the same Windows y-cruncher natively outside Sandbox had previously succeeded at 10^9 digits, so the obstacle is specific to this test guest/toolchain combination, but exact cause remains unproven.

## A.8 Operational disposition

- Owner judged Windows Sandbox not worth further effort and is deleting `T:\OUTLANDISH_01_SANDBOX\` and `T:\OUTLANDISH_01_SANDBOX_DATA\`, plus redundant Sandbox source-copy material on E: (exact deletion completion **not verified**).
- Any `.wsb`, copied production registry, persistent Python candidate, compiler bootstrappers and interim result logs within those trees are **temporary failed-test material**, not needed for ongoing OUTLANDISH operation. Do **not** delete G: active artifacts or E: working source.
- The guest test TOML had **no active registered constants**; the production registry on E: and verified six G: 10^9 files were not involved in a real Sandbox pipeline run.
- Retain narrative evidence in this handover. No future chat should propose spending more time on Sandbox as the default next step.

---

## Historical Appendix B — Explanation of Windows Sandbox errors and limits of findings

| Symptom / output | What is established | What is *not* established |
|---|---|---|
| Silent/slow classic Python MSI installation | The owner observed extreme delays; Python eventually launched once on ephemeral C: | Exact responsible security policy; whether installing to T: resolves guest filesystem cause |
| `python.exe` = 0 bytes and `certutil 0x800703EE` | Guest C: executable was unusable after pip attempts | Root cause; host disk damage or driver fault |
| `cscript` no `.vbs` engine | Original shortcut creation couldn't execute | Whether all scripting methods fail (PowerShell COM succeeded) |
| Missing C++ 14+ while building PyYAML etc | Wheels fell back to source builds requiring MSVC compiler | Need for Visual C++ **runtime** or all packages to run OUTLANDISH |
| Visual Studio installer 35% / 149 of 268 | An expensive guest-C: compiler install stalled and was abandoned | That compiler *could never* complete on a normal machine |
| Eight artifact audit violations under `python_candidate` | Scientific scan root was overly broad | Corruption/misplacement of genuine scientific output |
| `0xC000007B` from y-cruncher | Windows guest couldn't load y-cruncher image/dependency | Which DLL failed, a y-cruncher algorithm bug, a `10^10` swap problem, or proof runtime redist succeeded |
| Power-management provider Event 55 logs | CPU capabilities enumerated at guest startup | NTFS file corruption or host disk errors |

**Relevant background research retained from previous conversation (7 Nov 2026):**

- Microsoft Windows Sandbox slow-MSI issues and trust verification: https://github.com/microsoft/Windows-Sandbox/issues/85 and https://github.com/microsoft/Windows-Sandbox/issues/68. These are relevant to extreme installation time, not proven causes of zero-byte `python.exe` or `0xC000007B`.
- Microsoft Q&A slow Python install in Sandbox: https://learn.microsoft.com/en-us/answers/questions/3898205/the-setup-process-performance-inside-windows-sandb
- Microsoft Sandbox configuration and mapping semantics: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file
- Windows error 1006 `ERROR_FILE_INVALID`: https://learn.microsoft.com/openspecs/windows_protocols/ms-erref/18d8fbe8-a967-4f1c-ae50-99ca8e491d2d
- Windows `STATUS_INVALID_IMAGE_FORMAT` code and y-cruncher Windows launcher notes were discussed in chat; recheck official release notes and dependency diagnostics if ever revisiting, but owner has closed Sandbox path.

---

## Historical Appendix C — Historical handover filenames and their proper authority

The E: folder listing on 7 November contained these three documents (before owner agreed to clearer filenames). The following **renames were recommended; actual renaming was not independently verified**:

| Original | Suggested new name | What it represents |
|---|---|---|
| `OUTLANDISH_01_Standalone_Handover_Spec_v0_1.md` | `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md` | **5 Nov historical** early two-constant status, proposed Oz Lotto work, coding and experiment specification. Not latest implementation. |
| `OUTLANDISH_01_Standalone_Handover_Bundle_v0_1.zip` | `OUTLANDISH_01_2026-11-05_Historical_Source_and_Evidence_Bundle_v0_1.zip` | **5 Nov evidence bundle** accompanying the early handover; historical code/results snapshot, not current release. |
| `OUTLANDISH_01_Handover_2026-11-07_v1.md` | `OUTLANDISH_01_2026-11-07_Project_Status_and_Early_Sandbox_Diagnostics_v1.md` | **7 Nov early checkpoint**, pre-final Sandbox, before persistent T: Python verification and y-cruncher load failure. Superseded as conversation handover by v2, subsequently v3, v4 and v5. |

**Historical provenance note:** At the time v2 was written, that document was the current consolidated handover; it has since been superseded by v3, v4 and now v5. It is a guide, not a replacement for installed source code, actual live TOML, current repository README or original scientific evidence. Keep the historical files for provenance, but don't follow their obsolete paths and operational assumptions without checking current source.

---


---


---

## Provenance and version history (current as of v5)

- Owner-supplied Windows/WSL transcripts and uploaded 2026-11-07 `summary.json`, `matches.csv`, and `transitions.csv` underpin the measured v4 baseline. No assistant ran on the owner’s PC, inspected live G: binaries, or verified the currently mounted registry independently. The owner reported normal local tests and conversion/scanning commands passing.
- `OUTLANDISH_01.zip` is the source-review snapshot of established native Windows code, not permission to overwrite it. `OUTLANDISH_WSL_Packed_v0_2r2.zip` is the latest WSL-specific packed implementation candidate reported as locally exercised. Historical v3/v2 references remain useful but are superseded as *handover*.
- All timing figures in Part I are owner-reported observations on stated workloads or labelled as unverified projections; the 300m timing and host-inventory data are from the additional 7-Nov user transcript. 10^10 and 10^11 time budgets have **not** been validated. Future forecasts require appropriate measured workload and disk-mode provenance.
- Version chronology: 5 Nov historical standalone report/bundle; 7 Nov v1 early handover; v2 Windows Sandbox closure; v3 WSL2 primary architectural design (before Linux converter was implemented); **v4 real packed workflow baseline + owner’s performance-first decision + production registry plan**; **v5 hardware inventory, controlled 300m disk-swap performance results, four-core ceiling, cleanup, and refined next steps**.
- Current accepted high-level design: E: controlled code; T: native WSL2 ext4 generation/text/swap and testing; G: future guarded packed production staging and output. Important unresolved decisions include effective four-core worker affinity, representative larger-workload RAM and disk tuning, 10^11 VHDX sizing, stage-to-G: performance/durability, deletion/retention policy during legacy-to-packed migration, and exact packed registry contract.

**End — OUTLANDISH_01 v5 consolidated handover, 7 November 2026.**
