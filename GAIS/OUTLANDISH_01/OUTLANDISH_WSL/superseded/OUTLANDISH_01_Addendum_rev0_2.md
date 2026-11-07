# OUTLANDISH_01 — Living Handover Addendum

**Document filename:** `OUTLANDISH_01_Living_Handover_Addendum.md`  
**Internal revision:** 0.2  
**Updated:** 7 November 2026, Australia/Adelaide  
**Companion baseline:** `OUTLANDISH_01_2026-11-07_Project_Status_and_Packed_WSL2_Performance_Plan_v5.md`  
**Status:** ACTIVE, incremental handover; **not** a replacement for v5 or for the source code, logs, receipts or live configuration.

## How to maintain this document

- This is a **living delta** to the consolidated v5 handover. Read v5 for project history and the established packed workflow; then read this addendum for findings and decisions made **after v5**.
- When new tests or owner decisions occur, **revise this complete file under the same filename**, increment its internal revision number, and append a dated entry to the change log. Do not silently delete earlier results or replace measurements with estimates.
- Keep three categories distinct: **VERIFIED/OWNER-REPORTED OUTPUT**, **OWNER DECISION**, and **PROPOSED/NOT YET DONE**. Dates/times of runs and their output paths are evidence identifiers, not guessed timestamps.
- The owner can place this file alongside v5 on E:; it does not authorize code changes, a large calculation, production promotion, or deletions.
- If this grows unwieldy, consolidate into a later full handover, retaining this addendum as an evidence trail until then.

## 1. Current executive checkpoint — 7 Nov 2026

**Work order (owner-approved):**

1. Optimise y-cruncher **disk-swap/far-memory** generation for **10^10** and ultimately **10^11** decimal digits, using a small number of informative, larger-jump benchmarks.
2. **Skip** the legacy byte-per-digit versus nibble-packed scanner speed comparison.
3. Then build and qualify the **new packed-format production registry**, isolated G: staging, registration, retention, and guarded promotion. The existing G: legacy binaries and E: legacy `outlandish.local.toml` are not to be changed by current tests.

**Hardware / operating preferences:**

- Ryzen 9 3900X; 12 physical/24 logical CPUs; **hard owner ceiling of four physical cores for y-cruncher**.
- Selected four distinct physical cores correspond to Linux logical CPUs **0,2,4,6**. Use `taskset -c 0,2,4,6` together with `--td 4` for intended four-way runs, subject to effective-affinity verification; do not globally limit Debian or Windows.
- Keep WSL2's current **~15.6 GiB** memory limit for now; Windows has 32 GiB total host RAM and must remain usable for browsing, video, etc. Do **not** increase WSL's allowance to 24 GiB without a new owner decision.
- Consider y-cruncher RAM caps up to approximately **12 GiB** within the existing WSL memory allocation, but only where the workload can use them and Linux remains free of memory pressure. `-M` is a cap, not the actual memory consumed. A formerly discussed 18 GiB cap is **not part of the present plan**.
- T: is a Western Digital WD6003FZBX SATA **mechanical HDD**; Linux native ext4 is housed in `T:\OUTLANDISH_WSL\Debian\ext4.vhdx`. Host T: showed about 2.90 TB free, while Debian ext4 has a separate ~1007 GiB total filesystem capacity. These are not interchangeable free-space limits.
- Linux OS swap (~4 GiB) is **different from** y-cruncher's disk-swap files. Avoid making the OS page y-cruncher's working RAM.
- For disk I/O tuning the owner prefers **large, not numerous small, jumps**. Proposed Bytes/Seek candidates: **1, 8 and 12 MiB/seek**, only after confirming support, meaning, and whether such large values make sense on this HDD. These are **MiB per seek**, not GiB of y-cruncher memory; a larger value is not inherently faster. The baseline was `1.00 MiB/seek, no parallelism`.
- No computation at 10^10 or 10^11 has been authorised or performed. Preview-first launcher and explicit `--ack-large-run N` for runs >=10^9 remain in force.

## 2. Scientific / packed pipeline baseline (already in v5; carried for continuity)

On 7 Nov the actual **100,000,000-digit golden-ratio** WSL2 -> packed conversion -> Windows verification -> full packed Powerball scan succeeded:

- Decimal source in native WSL2 ext4; nibble-packed binary **50,000,000 bytes**, format `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, staged on T:, not G:.
- Conversion **1.581 s**; streamed packed SHA-256 `4cb6f6288b72f3a0ff738e72b261dc05ef5e507cfb62d29cf86b934dfd635e7e`.
- Windows sampled verification PASS (12 samples; **not** a full independent persisted-file verification).
- Windows packed Powerball scan across **100,000,000 digits**, 433 pre-holdout draws, wall **2.819 s**, P1/P2/P3 matches **0/0/3**, full scanned digest matched the conversion receipt. No production registration was performed.
- The three P3 matches are descriptive, not evidence of predictive success. The matched offsets and draw IDs are in the retained `matches.csv`.
- Keep the successful 100m input/report, T: packed receipt, and scanner output for the ongoing integration work until a specific cleanup decision.

## 3. NEW: completed generation-performance benchmarks after v5

All figures below are **owner-pasted y-cruncher output**, not assistant-run measurements. Constant = **golden ratio (phi)**; **disk-swap mode**; y-cruncher output verification ON; static Linux y-cruncher v0.8.7 Build 9547; swap/output under `/home/u/outlandish-work/` on ext4. All returned `EXIT=0` and reported a good spot check.

| Decimal digits (including integer) | y-cruncher memory cap | `--td` / framework | `taskset` | Actual working memory | Logical memory needed | Logical disk needed, excluding output | Output allowance | y-cruncher wall time | Shell `real` | Result |
|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 300,000,000 | 1 GiB | 1 / none | no | 947 MiB | 1.00 GiB | 1.11 GiB | 286 MiB | **151.780 s** | 153.406 s | PASS |
| 300,000,000 | 8 GiB | 1 / none | no | 1.23 GiB | 1.31 GiB | 1.11 GiB | 286 MiB | **134.769 s** | 136.356 s | PASS |
| 300,000,000 | 8 GiB | 4 / taskqueue | `0,2,4,6` | 1.24 GiB | 1.31 GiB | 1.11 GiB | 286 MiB | **136.334 s** | 137.730 s | PASS |
| **1,000,000,000** | **8 GiB** | **4 / taskqueue** | **`0,2,4,6`** | **4.17 GiB** | **4.25 GiB** | **3.78 GiB** | **954 MiB** | **406.015 s** | **407.965 s** | **PASS** |

**New one-billion-digit record:**

- Work directory: `/home/u/outlandish-work/phi_1000000000_20261107T105358Z_9352`.
- y-cruncher saved validation report: `Golden Ratio - 20261107-213045.txt` inside that directory; run output additionally recorded in `run.log`.
- Base y-cruncher computation (phi): **40.332 s**.
- Base conversion: **199.919 s**; writing decimal text **22.030 s**.
- Verifying base conversion: **126.186 s**; verifying decimal output: **8.686 s**.
- Total computation time reported: **240.294 s** (different from end-to-end wall time; do not compare the two as if interchangeable).
- Start-to-end wall time: **406.015 s**, shell `real` **6m47.965s**.
- y-cruncher reported CPU utilisation **16.48% + 0.25% kernel overhead**, spot check good through **750,000,000**, `EXIT=0`.
- Four-task output displayed `Task Queue -> 4 / ? / 24 (all cores)`. This label does **not** establish that 24 cores were actually used; however, the effective affinity of all y-cruncher child threads **was not independently inspected during the run**. Maintain the four-core limit and verify affinity in a future controlled run.
- At 1e9 digits, the **8 GiB memory cap was not reached**. Accordingly, repeating **the same** billion-digit workload with a 12 GiB cap is not expected to test the desired higher-memory regime effectively.

**Interpretation:**

- Increasing the 300m memory cap from 1 GiB to 8 GiB reduced wall time by **17.011 s (~11.2%)**, but the latter run used only ~1.23 GiB working memory; the change did not force 8 GiB allocation.
- Switching 300m / 8 GiB from one to four tasks increased wall time by **1.565 s (~1.16%)** in one comparison; it did not demonstrate a throughput win. Small elapsed differences may be noise, and the heavier one-billion workload has **no same-size one-core comparison**.
- At 1e9 digits, base conversion and its verification dominate the elapsed work. Do not assume RAM alone is the bottleneck; investigate external-memory behaviour, I/O and algorithmic phase profiles in representative larger workloads.
- The 1e9 result is **not** a validated time forecast for 1e10 or 1e11. Constant choice matters; phi is not representative of gamma and every other constant.

## 4. Storage/cleanup checkpoint — VERIFIED complete through 1e9

**OWNER-REPORTED VERIFIED (7 Nov 2026):** The owner removed the large decimal output from the 1e9 run using the explicitly targeted `rm -i`, confirmed `y`, and inspected the state with `df -h /` and `du -sh`. All four completed benchmark work directories are now **48 KiB each**. This confirms the earlier 300m large output cleanup as well as the 1e9 cleanup. Small `run.log` and y-cruncher validation reports remain (original directory listings documented the files before deletion):

- `/home/u/outlandish-work/phi_300000000_20261107T102056Z_12274` — 48 KiB
- `/home/u/outlandish-work/phi_300000000_20261107T102748Z_22348` — 48 KiB
- `/home/u/outlandish-work/phi_300000000_20261107T104001Z_8098` — 48 KiB
- `/home/u/outlandish-work/phi_1000000000_20261107T105358Z_9352` — 48 KiB

Owner-reported Debian `df -h /`: `/dev/sdd` size **1007G**, used **780M**, available **955G**, utilization **1%**. The 1e9 output had been ~1,000,000,001 bytes; this and three 300,000,001-byte prior outputs have now been removed. The supplied `du` command verifies directory sizes but **does not re-list exact remaining filenames**; rely on earlier file listings for report names and verify any files before future deletion. y-cruncher was not shown running in the earlier read-only checks.

**Keep** the separate 100m original reference, T: packed artifact and receipt, Powerball scan reports, y-cruncher installation, Debian's `ext4.vhdx`, and **all** G: production artifacts untouched. Continue targeted cleanup after future benchmark output is no longer needed.

## 5. Next decision: 3e9 calibration preview VERIFIED; execution NOT YET DONE

A **3,000,000,000-digit phi** calibration was proposed, using disk-swap, a **12 GiB y-cruncher memory cap**, four task-queue workers, and `taskset -c 0,2,4,6`. It is intended to exercise a higher RAM regime without jumping directly to 10 billion digits.

**OWNER-REPORTED PREVIEW PASS (7 Nov 2026, 11:07:30 UTC):**

```bash
taskset -c 0,2,4,6 bash wsl_generate.sh \
  --constant phi \
  --digits 3000000000 \
  --mode swap \
  --memory 12g \
  --td 4
```

The actual preview printed: `CONSTANT=phi TOTAL_DIGITS_INCLUDING_INTEGER=3000000000`, `MODE=swap TD=4 FRAMEWORK=taskqueue MEMORY_CAP=12g VERIFY_OUTPUT=ON`, `PREVIEW ONLY: no computation, files or directories created.` It displayed a **prospective only** attempt path `/home/u/outlandish-work/phi_3000000000_20261107T110730Z_25366`; the eventual execution creates its **own** attempt path. The command line uses `-dec:2999999999`, `-M:12g`, `-TD:4`, `-PF:taskqueue`, and ext4-backed `-swap:raid0`.

**Resource assessment — extrapolations, NOT y-cruncher-reported 3e9 estimates:** The measured 1e9 phi run needed **4.25 GiB logical memory** and **3.78 GiB logical disk**, plus **954 MiB output**. Naive proportional scaling to 3e9 suggests approximately **12.75 GiB logical memory**, **11.34 GiB logical disk**, and **2.86 GiB output**. Algorithm thresholds, overhead and storage decomposition may change these values; do not treat them as guaranteed or exact. The **12 GiB** y-cruncher memory cap will likely cause real disk-backed work, unlike the earlier 1e9 benchmark. Available Debian ext4 free space **955G** is ample versus these tentative estimates. WSL has **~15.6 GiB total RAM**; a 12 GiB cap leaves only about **3.6 GiB nominal RAM headroom**, and use of Linux OS swap must be monitored. The user's primary requirement is continued Windows usability and ≤4 physical cores; retain existing WSL limit and stop testing on instability.

**Execution NOT YET REPORTED:** A preview is not a run. No 3e9 output, timings, measured resource requirements or CPU-affinity observations exist yet. The user previously used `time taskset -c 0,2,4,6` for real runs, but no command has yet been reported with `--run --ack-large-run 3000000000`. Do not record a PASS or create/delete any 3e9 output until actual logs exist. The current launcher directly starts a computation when `--run` is provided; it does not offer a true resource-estimate-only y-cruncher invocation. The above is a bounded extrapolative resource review rather than a verified internal y-cruncher preflight.

**Disk tuning still pending:** baseline ~1.00 MiB/seek, no parallelism. Proposed large-jump candidates 8 and 12 MiB/seek are **not yet tested and may not be beneficial** on the single physical T: HDD. Verify exact y-cruncher option support/algorithmic semantics before altering the launcher or launching another expensive run. Do not confuse disk capacity with disk-access strategy; disk-swap scratch capacity is generally derived from workload and y-cruncher algorithm.

## 6. Boundaries unchanged from v5

- No Windows Sandbox restoration. New source on E: only, native Debian computation on ext4 backed by T:, temporary packed rehearsal artifacts on T:, production packed integration on G: **only after designed and reviewed**.
- Six existing production one-byte-per-digit 10^9 constants and existing Windows registry on G:/E: are **untouched** by this test programme.
- Verification remains `-verify:1` for y-cruncher, with recorded validation output and receipts as appropriate; no unapproved reduction of integrity checks to improve speed.
- Only approved **pre-holdout** Powerball results are used in development. Oz Lotto and the extra any-order matching schemes remain deferred; no lottery pooling.
- All large experiments require explicit launch authorisation; do not inadvertently start y-cruncher's interactive menu option `0`.

## 7. Addendum update log

| Revision | Date | Change |
|---|---|---|
| **0.1** | **2026-11-07** | Created living v5 companion; recorded completed 1e9 phi 8 GiB/4-task benchmark, measured phase timings, latest memory/CPU/disk decisions, outstanding cleanups, proposed 3e9 preview, and pending Bytes/Seek tuning. Earlier 300m results retained as comparison data. |
| **0.2** | **2026-11-07** | Recorded confirmed four-dir output cleanup, ext4 free space, 3e9 / 12 GiB / four-task preview PASS, extrapolated (not measured) resources, and explicit no-execution state. |

**End of living addendum revision 0.2.**
