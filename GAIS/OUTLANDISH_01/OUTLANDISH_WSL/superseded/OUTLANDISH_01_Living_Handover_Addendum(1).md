# OUTLANDISH_01 — Living Handover Addendum

**Document filename:** `OUTLANDISH_01_Living_Handover_Addendum.md`  
**Internal revision:** 0.5  
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
- For disk I/O tuning the owner prefers **large, not numerous small, jumps**. The previously contemplated **1, 8 and 12 MiB/seek** tests are **superseded** by the 1 MiB/seek `benchio` result below: the installed y-cruncher specifically recommended a **smaller** value. Any next test should use a materially lower setting, provisionally 256 KiB/seek, after scratch inspection and explicit owner approval. These are MiB or KiB per seek, not GiB of RAM. The generation baseline remains `1.00 MiB/seek, no parallelism`.
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

All figures below are **owner-pasted y-cruncher output**, not assistant-run measurements. Constant = **golden ratio (phi)**; **disk-swap mode**; static Linux y-cruncher v0.8.7 Build 9547; swap/output under `/home/u/outlandish-work/` on ext4. The first four rows had y-cruncher output verification **ON**; the final 3e9 row had it explicitly **OFF**, was a disposable benchmark, and is **not eligible for packing or production registration**. All returned `EXIT=0` and reported an internal good spot check; that spot check is not equivalent to full y-cruncher verification.

| Decimal digits (including integer) | Memory cap | `--td` / framework | CPU affinity requested | Actual working memory | Logical memory needed | Logical disk required, excluding output | Output allowance | Verification | y-cruncher wall | Shell `real` | Result |
|---:|---:|---|---|---:|---:|---:|---:|---|---:|---:|---|
| 300,000,000 | 1 GiB | 1 / none | no | 947 MiB | 1.00 GiB | 1.11 GiB | 286 MiB | ON | **151.780 s** | 153.406 s | PASS |
| 300,000,000 | 8 GiB | 1 / none | no | 1.23 GiB | 1.31 GiB | 1.11 GiB | 286 MiB | ON | **134.769 s** | 136.356 s | PASS |
| 300,000,000 | 8 GiB | 4 / taskqueue | `0,2,4,6` | 1.24 GiB | 1.31 GiB | 1.11 GiB | 286 MiB | ON | **136.334 s** | 137.730 s | PASS |
| 1,000,000,000 | 8 GiB | 4 / taskqueue | `0,2,4,6` | 4.17 GiB | 4.25 GiB | 3.78 GiB | 954 MiB | ON | **406.015 s** | 407.965 s | PASS |
| **3,000,000,000** | **12 GiB** | **4 / taskqueue** | **`0,2,4,6`** | **10.3 GiB** | **10.3 GiB** | **9.82 GiB** | **2.79 GiB** | **OFF** | **637.385 s** | **640.195 s** | **BENCHMARK PASS; UNVERIFIED** |

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

## 5. NEW: 3e9 calibration completed — owner-reported PASS, unverified benchmark only

**OWNER-REPORTED OUTPUT, 7 Nov 2026:** Run of **3,000,000,000 total decimal digits including integer** of phi. The owner launched it with the newly installed explicit benchmark opt-out; this is **not** a production or verified-digit source.

```bash
time taskset -c 0,2,4,6 bash wsl_generate.sh \
  --constant phi \
  --digits 3000000000 \
  --mode swap \
  --memory 12g \
  --td 4 \
  --benchmark-no-verify \
  --run \
  --ack-large-run 3000000000
```

- Run class printed: `RUN_CLASS=BENCHMARK_UNVERIFIED VERIFY_OUTPUT=OFF`; y-cruncher command contained `-verify:0`. The launcher prominently warned against packed conversion, registration and production use. Preview before the run had passed, and the actual run created its own unique work directory.
- Actual work directory: `/home/u/outlandish-work/phi_3000000000_20261107T112633Z_3791` (native ext4 in T:-backed Debian VHDX).
- Y-cruncher validation/report filename printed: `Golden Ratio - 20261107-220713.txt`; **do not treat this file's title or internal spot-check as evidence of enabled full verification**. Run log expected `run.log` by launcher convention, but its post-run existence has not yet been re-listed.
- Mode: `swap`; `-M:12g` (ceiling), `-TD:4 -PF:taskqueue`; requested `taskset -c 0,2,4,6`; `1.00 MiB/seek, no parallelism`; maximum four physical cores remains binding. The y-cruncher `4 / ? / 24 (all cores)` topology report does not independently prove actual per-thread affinity; no live affinity sample was captured.
- Reported `Logical Memory Needed: 10.3 GiB` using `POSIX mmap()`; **actual working memory 10.3 GiB**, plus reported twiddle tables **13.9 MiB** and I/O buffers **64.0 MiB**. The 12 GiB RAM ceiling was **not reached**. This does **not** prove that no disk-swap I/O occurred.
- Reported `Logical Disk Needed: 9.82 GiB + 2.79 GiB for output`; largest checkpoint **6.45 GiB**. These are y-cruncher estimates of disk *requirements*, not measured physical bytes read/written or residual scratch usage.
- Golden-ratio core calculation **116.715 s**. Processing hexadecimal digits **8.398 s**. Base converting **444.219 s**. Writing decimal output **54.607 s**. No full base-conversion or decimal-output verification was done.
- Reported `Total Computation Time: 560.954 s`; **start-to-end wall 637.385 s** (10m37.385s); shell `real` **10m40.195s**. Exit code **0**.
- Internal `Spot Check: Good through 2,500,000,000` and final displayed digits; **not a replacement for full verification**. CPU utilization reported `24.09% + 0.22% kernel overhead`; do not infer CPU counts or verify affinity from this percentage alone.
- Pre-run Debian resources: ~15 GiB reported memory total, ~14 GiB available, OS swap 4.0 GiB with **0 B used**; ext4 `/` 955 GiB available. **Post-run OS-swap usage was not reported**, so do not claim it stayed at zero throughout.

### Interpretation and comparisons

- Actual 3e9 logical memory requirement **10.3 GiB**, below the 12 GiB cap but **above an 8 GiB cap**. Accordingly a same-workload **8 GiB versus 12 GiB** comparison would now be meaningful if testing memory effects remains the priority. Earlier 1e9 used only 4.25 GiB and could not answer this question.
- The 3e9 run demonstrates successful use of the installed benchmark-only verification-off flag, not the correctness of its decimal digits for production.
- Do **not** claim a 3e9 speedup over the 1e9 406.015-second run: verification settings and workload differ. There is no comparable 3e9 verified run or 8 GiB run yet. Base conversion **444.219 s** remains the dominant timed phase.
- No evidence yet isolates Bytes/Seek, disk seeks, physical I/O, or cache benefit. For future tuning, owner prefers a small number of large-step measurements. Prospective Bytes/Seek settings **1, 8 and 12 MiB/seek** remain **unverified proposals**, subject to y-cruncher support and the actual HDD's characteristics.
- **Superseded next-step note:** The owner explicitly preferred **not** to run the lower-memory 3e9 / 8 GiB comparison; retain the 12 GiB cap and investigate disk I/O instead. The owner confirmed removal of the disposable 3e9 decimal output with `rm -i` and `y` after verifying no running y-cruncher; an independent post-deletion directory listing has not yet been supplied. The 3e9 `swap/` directory was present before deletion; inspect before considering its removal. Subsequent I/O benchmark and the new next step are recorded in Section 6.

## 6. NEW: first dedicated y-cruncher I/O benchmark — owner-reported PASS; disk bottleneck

**OWNER-REPORTED OUTPUT, 7 Nov 2026:** The owner located the installed `Command Lines.txt` for **Linux static y-cruncher v0.8.7 Build 9547** and checked the exact `benchio`, `-minIO` and `-swap:raid0` syntax. Documentation states `-minIO:{size}` sets **logical Min I/O Bytes (Bytes/Seek)**. `-swap` must be the final switch because the arguments after it are paths. The disk I/O benchmark writes scratch data; it is not a non-destructive preview.

The owner ran the following benchmark from a dedicated ext4 work directory (backed by the **T: WD6003FZBX mechanical HDD**), not from the E: source folder or the G: production root:

```bash
BENCH="$HOME/outlandish-work/benchio_1m_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$BENCH/swap"
cd "$BENCH" || exit 1
YC="$HOME/outlandish-test/y-cruncher v0.8.7.9547-static/y-cruncher"
{ time taskset -c 0,2,4,6 "$YC" benchio \
  -M:12g -TD:4 -PF:taskqueue -minIO:1m \
  -swap:raid0 "$BENCH/swap"; } 2>&1 | tee "$BENCH/run.log"
echo "BENCHIO_EXIT=${PIPESTATUS[0]}"
```

The **actual directory** was `/home/u/outlandish-work/benchio_1m_20261107T120842Z` (distinct from any forecasted name). Its `run.log` was written using `tee`. The owner had first run `pgrep -af y-cruncher` with no matching process output.

| Metric | Owner-reported result |
|---|---:|
| Working RAM requested/reported | 12.0 GiB |
| I/O benchmark swap-file size indicated by y-cruncher | 48.0 GiB |
| Task queue | 4 (reported topology still says `4 / ? / 24 (all cores)`) |
| Bytes/Seek | 1.00 MiB |
| Sequential write bandwidth | **61.5 MiB/s** |
| Sequential read bandwidth | **182 MiB/s** |
| Threshold strided write bandwidth | **123 MiB/s** |
| Threshold strided read bandwidth | **123 MiB/s** |
| Reported overlapped disk/computation ratio | **0.0762008** |
| Shell elapsed | **22m11.006s** |
| Shell user / sys | 2m21.379s / 23.174s |
| BENCHIO_EXIT | **0** |

**Interpretation, constrained to this run:**

- y-cruncher warned that overall disk bandwidth is **very poor relative to CPU performance**, so sufficiently large external-memory calculations will be **disk-limited**. Its indicated goal for overlapped streaming is an I/O-to-compute ratio >2.0; observed **0.0762** is far below it. This is the tool's comparative diagnostic, not a measured fraction of physical cores.
- It warned that **threshold non-sequential bandwidth is unusually high** relative to sequential bandwidth, potentially selecting inefficient algorithms, and explicitly recommended **decreasing Bytes/Seek** and rerunning. Accordingly, earlier proposals to test **8 or 12 MiB/seek are withdrawn for now**. The official y-cruncher swap-mode guide explains that a too-high Bytes/Seek setting can force unnecessary traffic, while too-low settings can increase seeks: smaller does not automatically mean better. A **256 KiB/seek** comparison is one *candidate*, not authorised or executed.
- The reported sequential write bandwidth **61.5 MiB/s** is much lower than sequential read **182 MiB/s**. The cause is **unknown**. Possibilities requiring separate evidence include disk load, write-cache behaviour, ext4/VHDX allocation overhead, physical-drive characteristics or benchmarking artefacts. Do not attribute it to any one cause without measurement.
- The strided write result exceeding sequential write means direct ratio calculations using the write figures are **not a clean physical-drive characteristic**; OS caching and access patterns may affect the measured rates. Treat this first benchio as a diagnostic baseline rather than conclusive optimization.
- The **48 GiB** value is the size configured for the I/O benchmark, **not a measurement of currently occupied persistent storage or a user-selected preallocation**. The owner has **not yet supplied a post-benchmark scratch listing, `du`, or `df`**, so no claim is made about reclaimed vs leftover swap data or ext4 VHDX growth. The 22-minute run reinforces the preference for **few high-information experiments**.
- The user previously requested to **avoid increasing WSL2's memory from ~15.6 GiB** to preserve Windows usability, maintain **12 GiB y-cruncher ceiling**, **4 physical cores maximum**, and prefer large but reasoned setting changes. No production data on G: was used.

**NEXT — read-only scratch audit before additional testing:**

```bash
pgrep -af y-cruncher
BENCH="$HOME/outlandish-work/benchio_1m_20261107T120842Z"
du -sh "$BENCH" "$BENCH/swap" 2>/dev/null
df -h /
ls -lah "$BENCH" "$BENCH/swap"
```

Only once the actual remaining files and swap usage are known should a **specific, narrowly scoped deletion** be prepared. Preserve `run.log`; do not remove the y-cruncher install, Debian VHDX, the 100m reference, or G: artifacts. No additional `benchio` or large generation run is currently authorised. A possible next optimization is either investigating write throughput/host disk interference or running **one** carefully bounded lower-Bytes/Seek benchmark if it will answer a meaningful question.

## 7. Boundaries unchanged from v5

- No Windows Sandbox restoration. New source on E: only, native Debian computation on ext4 backed by T:, temporary packed rehearsal artifacts on T:, production packed integration on G: **only after designed and reviewed**.
- Six existing production one-byte-per-digit 10^9 constants and existing Windows registry on G:/E: are **untouched** by this test programme.
- **Owner-approved on 7 Nov:** verified/prod generation remains `-verify:1`; explicitly labelled **throwaway performance benchmarks only** may set `-verify:0`. These outputs are NEVER eligible for packed conversion, production registration/promotion or claims of verified digits. The existing `wsl_convert.py` report-verification gate stays unchanged. Baseline benchmarks above all have verification ON; do not directly compare end-to-end wall times across different verification policies.
- **Installed and owner-exercised:** Updated `wsl_generate.sh` accepts `--benchmark-no-verify`, with `-verify:1` remaining default. The owner first demonstrated the preview `VERIFY_OUTPUT=OFF RUN_CLASS=BENCHMARK_UNVERIFIED`, then successfully completed a real 3e9 unverified benchmark. This does **not** authorize changing the converter's verification requirement or allowing unverified output into production.
- The 1e9 phi run spent **126.186 s** verifying base conversion and **8.686 s** verifying decimal output, total **134.872 s** (~33.2% of reported 406.015-s wall). This supports the benchmark-only option, but it is not a directly measured same-workload saving; the new 3e9 benchmark was run only with verification OFF.
- Only approved **pre-holdout** Powerball results are used in development. Oz Lotto and the extra any-order matching schemes remain deferred; no lottery pooling.
- All large experiments require explicit launch authorisation; do not inadvertently start y-cruncher's interactive menu option `0`.

## 8. Addendum update log

| Revision | Date | Change |
|---|---|---|
| **0.1** | **2026-11-07** | Created living v5 companion; recorded completed 1e9 phi 8 GiB/4-task benchmark, measured phase timings, latest memory/CPU/disk decisions, outstanding cleanups, proposed 3e9 preview, and pending Bytes/Seek tuning. Earlier 300m results retained as comparison data. |
| **0.2** | **2026-11-07** | Recorded confirmed four-dir output cleanup, ext4 free space, 3e9 / 12 GiB / four-task preview PASS, extrapolated (not measured) resources, and explicit no-execution state. |
| **0.3** | **2026-11-07** | Owner approved disabling y-cruncher base-conversion and output verification for explicitly labelled throwaway performance benchmarks only; verified production unchanged. Candidate opt-in launcher update prepared, not yet owner-installed **at that revision**. |
| **0.4** | **2026-11-07** | Recorded owner's installed benchmark-only launcher preview and completed unverified 3e9 phi run (637.385 s; 10.3 GiB actual working memory; 9.82 GiB logical disk), phase times, strict nonproduction status, corrected previously pending run state, outstanding cleanup, and options for next memory/disk comparison. |
| **0.5** | **2026-11-07** | Recorded 3e9 text deletion confirmation (without inferring post-deletion contents); owner decision to skip lowering the 3e9 RAM cap to 8 GiB; successful 22m11s y-cruncher `benchio` 12 GiB/4-task/1 MiB-per-seek run and exact I/O rates; benchmark’s recommendation to **decrease** Bytes/Seek; withdrawal of 8/12 MiB seek experiments; read-only scratch audit and no new authorised runs. |

**End of living addendum revision 0.5.**
