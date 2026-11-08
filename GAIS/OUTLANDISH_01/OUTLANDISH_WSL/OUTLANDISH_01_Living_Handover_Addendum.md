# OUTLANDISH_01 — Living Handover Addendum

**Internal revision:** **0.5**  
**Updated:** 8 November 2026 (Australia/Adelaide)  
**Current consolidated baseline:** `OUTLANDISH_01_Consolidated_Handover_v6.md`, owner approved on 8 November 2026.  
**Status:** ACTIVE — post-v6 owner decisions and observations. The 10^10-digit phi y-cruncher generation **passed** (`-verify:1`, exit 0). The 5,000,000,000-byte nibble-packed binary was converted **directly into G: staging** and the Windows 12-sample verifier **passed**. **A separate complete persisted-file SHA-256 match, G: publication in `digits/`, and mandatory deletion of the 10,000,000,001-byte decimal source are pending.** A potential difference between early/scanned match counts and smaller-file baselines has been reported but **not yet established or diagnosed**. The owner has decided to **defer all scientific scanning until all six 10^10 production binaries have been verified, and the scanner has passed deliberate synthetic fixtures and shared-prefix reconciliation.**
**Scope:** This is an incremental delta, **not** a replacement for v6, live source code, actual runtime logs, receipts, G: registry, or other on-disk evidence. Earlier addendum rev0.5 is historical and preserved separately. Rev0.1 was the initially empty post-v6 template.

## 1. Executive checkpoint and immediately applicable instructions

1. **OWNER DECISION — Final format:** Focus production and research on nibble-packed `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1` only. The legacy one-decimal-digit-per-byte files and byte-oriented production workflow may be retired. Preserve valuable historical code, matching/reporting definitions, tests and evidence as references; do not rewrite functioning generation or packed-scanning code merely to tidy the project.
2. **OWNER DECISION — Correctness assurance:** **Every production generation uses y-cruncher `-verify:1`.** `-verify:0` remains permissible solely for clearly marked, throwaway performance benchmarks; their output is ineligible for conversion, production registry, scientific matching and parent-project handoff. The owner explicitly accepts the residual risk of **not** performing a second, computationally independent mathematical verification. This does **not** waive converter digit validation, output receipts/hashes, persisted-file integrity checks, or safe registration.
3. **OWNER DECISION — No legacy-prefix comparison:** The owner explicitly waived the formerly proposed complete first-10^9-digit comparison between new packed files and the six original byte-format files. The old G: byte-format binaries are approved for **eventual deletion**, including before a packed replacement exists, subject to careful inspection of exact paths, live registry references, ongoing readers, locks, and recovery requirements. **No deletion or registry change has been performed by this chat.** Do not silently leave six active TOML entries pointing to deleted files. No cross-format comparison utility is required merely to enable retirement.
4. **OWNER DECISION — Tuning sufficiently complete:** Stop general-purpose `benchio`/Bytes-per-Seek optimisation unless a concrete production problem justifies reopening it. Initial production baseline: static Linux y-cruncher v0.8.7 Build 9547; Debian ext4 backed by T: HDD; swap mode; `-M:12g`, `-TD:4 -PF:taskqueue`, logical Bytes/Seek **1 MiB**, verification ON; no WSL memory-limit change. Initial RAM/disk **capacity checks** remain necessary but are **not** a mandate for a new optimisation campaign.
5. **COMPLETED GENERATION — 10^10 phi:** Launched 8 Nov 2026 at **00:53:58 Adelaide time** (2026-11-07 14:23:58 UTC), under `/home/u/outlandish-work/phi_10000000000_20261107T142358Z_3975`. Produced a y-cruncher verified-generation result for **10,000,000,000 total digits including integer** (`-dec:9999999999`). y-cruncher end time **02:17:00 local**, start-to-end **4,981.736 s (83.029 min)**, shell `real` **83m06.072s**, **EXIT=0** and `GENERATION_EXIT=0`; both base-conversion and decimal-output verification stages completed; spot check good through 7.5 billion. Terminal named saved validation report `Golden Ratio - 20261108-021703.txt`. This is a **successful y-cruncher run**, not evidence that the decimal file has been separately examined or that a packed `.bin` has been produced, full-hashed, scanned or registered.
6. **CRITICAL NEW OBSERVATION — CPU affinity:** The wrapper inherited the requested `taskset -c 0,2,4,6` mask, but **all nine threads of the actual Kagari calculation process** were permitted logical CPUs **0–23**. The intended four-physical-core OS scheduling restriction was **NOT enforced** in this run. `-TD:4` requests four tasks; it is not equivalent to a four-core hard limit. The thread state and lifetime CPU percentages **do not prove** how many cores were simultaneously busy. The owner, informed of this unexpected condition and previous hard-power-off risk, **chose to let this particular run continue**; it subsequently completed successfully. This is **not blanket approval** to disregard the original four-physical-core limit on future runs. The observed scheduling confinement problem remains unresolved; consider a minimal reliable restriction **before later large launches**, with separately agreed intervention.
7. **OWNER DECISION — Final size:** After observing 83 minutes for verified 10^10 phi, the owner judged six 10^11-digit computations not worth the expected additional cost for this speculative project. **The agreed target is now six 10^10-digit packed constants**, one at a time. This is a value/cost decision, not a claim that 10^11 runtime can be forecast linearly. Retain the successful 10^10 phi source as production-intended, not a disposable benchmark.
8. **COMPLETED PACKING, NOT YET PUBLISHED — phi:** `wsl_convert.py` created `G:\OUTLANDISH_01\large_artifacts\staging\digits_golden_ratio_10_to_10.packed.bin`, exact 5,000,000,000 bytes, streamed SHA-256 `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d`, receipt published, `CONVERSION_EXIT=0`, converter elapsed 159.875 s. The Windows sampled verifier checked 12 samples and returned `VERIFIER_EXIT=0`. The converter was run with `--keep-text`; the 10,000,000,001-byte source has **not** been deleted. Sample success is not the complete persisted-file SHA check. The file is still **staged**, not in `digits/` or registered.
9. **OWNER DECISION — SCANNER QUALIFICATION GATE:** Postpone scientific matching/scanning until **all six 10^10 packed binaries are generated, independently full-hash-verified, published and large intermediate sources cleaned up**. Then review the scanner source, run independently constructed synthetic packed fixtures with **at least two known hits per category P1, P2, P3**, negative, odd/even offset and chunk-boundary cases, and reconcile shared-prefix matches with earlier baselines. Only after this qualification should the six full scientific scans run. Reported differences in early match counts are a **suspected discrepancy**, not yet a proven defect.
10. **IMMEDIATE NEXT:** Verify the entire stored phi packed file's SHA-256 by an independent streaming read from G: and compare against its receipt; **do not rely on the scientific scanner for this verification**. Inspect G: target/receipt and implement or agree a narrow, safe same-volume staging-to-`digits/` publication. Upon successful full-file integrity check and durable publication, **mandatory exact-path deletion** of the large decimal source; preserve small y-cruncher report, `run.log`, receipt and verification evidence. No further scientific scanning at this stage.

## 2. Owner decisions since v6 — details and qualifications

### D-01. Production verification; independently recomputing constants waived

**OWNER DECISION, 8 Nov:** All production computations at 10^10 and any eventual 10^11 use `-verify:1`. The owner accepted the residual risk of not doing a separate independent mathematical computation. Existing `wsl_convert.py` validation/report acceptance must remain unchanged. `-verify:0` continues to be restricted to explicitly labelled nonproduction speed tests. The decision avoids redundant second calculations, **not** the normal verified-generation and packed-integrity chain.

### D-02. Packed-only end state; legacy file retirement and comparison waiver

**OWNER DECISION, 8 Nov:** Nibble-packed data replace the old numeric-byte format as the sole active production/research target. The owner explicitly waived any byte-versus-packed full-prefix comparison and authorised deletion of legacy byte-format files. Before any destructive action, inspect the actual G: paths, existing `outlandish.local.toml` state and any active reader/lock; establish a consistent retirement/de-registration/recovery procedure. Never infer that the uploaded historical TOML exactly matches live state. Existing G: files have **not** been deleted based on the supplied evidence. The historical native-Windows code/docs remain scientific and engineering reference material.

### D-03. End targeted tuning; proceed with meaningful production data

**OWNER DECISION, 8 Nov:** The previously completed 300m, 1e9, 3e9 and 1-MiB/seek `benchio` tests are sufficient for initial production choices. Keep the current 1 MiB logical Bytes/Seek baseline (not claimed optimal), ~12 GiB y-cruncher cap, and intended four-physical-core limit. Per-constant resource estimation and capacity precautions are sensible. Produce one or two real, verified 10^10-digit files to inform the later owner decision: if 10^11 is practicable and acceptable, aim directly for six at 10^11; otherwise complete six at 10^10. This strategic target choice was already in v6 and remains unchanged.

### D-04. Proceed with the present run despite effective affinity anomaly

**OWNER DECISION during live 10^10 phi run, 8 Nov:** After seeing `/proc/353/task/*/status` report all nine Kagari threads permitted CPUs `0-23`, and after being advised to interrupt, the owner stated: **“I am going to let it run and if it crashes so be it.”** Record as an informed **run-specific** continuation decision. Do not relabel this as verified four-core compliance or as general relaxation of the four-core safety limit. The computational result remains eligible for assessment only if the process exits successfully and its verification evidence passes; exposure to an affinity anomaly neither automatically proves digit corruption nor supplies assurance against it.

### D-05. Final target: six 10^10-digit production files; do not pursue 10^11

**OWNER DECISION, 8 Nov:** Based on the successful verified 10^10 phi run (~83 minutes), the owner decided that the time, space and effort of six 10^11-digit runs would not be warranted for this speculative programme. **Commit to six 10^10-digit packed files**, generated, independently full-hash-verified and published one at a time, with scientific scanning deferred to a separately qualified phase; do not conduct further 10^11 tuning or capacity work by default. The rough '10x time' comparison was the owner's planning heuristic, **not a measured linear scaling law**. This decision supersedes the earlier D-03/v6 conditional choice of six at 10^11 versus 10^10. Continue with `-verify:1`, existing 12 GiB and TD4/1 MiB settings as the working baseline, with per-constant capacity checks. The unresolved actual CPU-affinity nonconfinement is not thereby erased.

### D-06. Defer scientific scanning; qualify implementation with synthetic known-hit fixtures

**OWNER DECISION, 8 Nov:** The owner reported that initial matching counts during scanning of the new 10^10 phi packed data appeared inconsistent with historical scanning on smaller files. The exact observed values, input provenance and comparison conditions have **not** yet been supplied, so this is an **unresolved anomaly requiring investigation**, not a confirmed scanner defect. The owner explicitly deferred scientific scanning until **all six 10^10 packed files have been produced, full-hash-verified, durably published and intermediate source text cleaned up**. Before any full scientific scan, inspect/review source code (including nibble unpacking, start/end offset conventions, all alignment cases, overlapping P1/P2/P3 classification, drawn-order versus any-order logic, historical-draw selection, chunk boundaries and reporting). Run artificial fixtures with at least **two deliberately placed, independently expected hits in each currently implemented category** P1, P2 and P3, including odd/even offsets and cross-chunk cases, plus negative controls and exact expected counts/offsets. Compare the common digit prefix against historical runs under demonstrably equivalent data, definitions and filters; investigate any discrepancy before accepting scientific results. This postpones the *scientific scan*, **not persisted-file SHA-256 assurance**. The latter must be independently checked from G: without invoking the questioned scanner. Retain suspect/partial scan outputs as diagnostic-only until reconciled; do not claim scientific PASS from them.

## 3. New experimental findings — first 10^10 phi run (completed generation; packed pipeline pending)

### E-01. Preflight, launcher preview and launch configuration

**OWNER-REPORTED OUTPUT, 8 Nov:** In Debian under WSL2, from E:-mounted `GAIS/OUTLANDISH_01/OUTLANDISH_WSL`:

| Preflight item | Owner-reported result |
|---|---|
| y-cruncher process before launch | No matching process |
| Debian RAM | `free -h`: 15 GiB total, about 15 GiB initially available |
| Debian OS swap | 4.0 GiB, 0 B used |
| ext4 `/` | `/dev/sdd`: 1007 GiB capacity, 955 GiB available before run |
| Windows T: mount | 5.5 TiB total, 2.6 TiB available at preflight |
| Windows G: mount | 5.5 TiB total, 3.5 TiB available at preflight |
| Existing work directory | `/home/u/outlandish-work`: 268 KiB before run |
| Executable | `/home/u/outlandish-test/y-cruncher v0.8.7.9547-static/y-cruncher` |
| Bash syntax | `bash -n wsl_generate.sh`: PASS |
| Preview | `PREVIEW ONLY`, no computation or directories created; `VERIFY_OUTPUT=ON`, `RUN_CLASS=VERIFIED_GENERATION` |

The owner then ran:

```bash
time taskset -c 0,2,4,6 bash wsl_generate.sh \
  --constant phi \
  --digits 10000000000 \
  --mode swap \
  --memory 12g \
  --td 4 \
  --run \
  --ack-large-run 10000000000

echo "GENERATION_EXIT=$?"
```

The exact **actual** attempt was `/home/u/outlandish-work/phi_10000000000_20261107T142358Z_3975`. This is not the earlier preview-only timestamp/attempt directory. The launched command contained `custom goldenratio -dec:9999999999 -hex:0 -od:1 -compress:0 -verify:1 -mode:swap -TD:4 -PF:taskqueue -M:12g -swap:raid0 <attempt>/swap`.

### E-02. y-cruncher reported resource estimates and actual initial allocation

**OWNER-REPORTED OUTPUT (run start):**

| Value | Reported |
|---|---:|
| Decimal digits | 9,999,999,999 places, hence 10,000,000,000 total incl. integer |
| Verify Output | Enabled (`-verify:1`) |
| Mode/framework | Swap; Task Queue 4 / ? / 24 (all cores) — topology/task report, **not proof of physical-core use** |
| Far-memory tuning | **1.00 MiB/seek, no parallelism** |
| Logical memory needed | **12.0 GiB** POSIX mmap |
| Working memory at computation start | **11.9 GiB** |
| Additional twiddle tables | 13.9 MiB |
| I/O buffers | 64.0 MiB |
| Logical disk requirement | **37.0 GiB**, plus **9.31 GiB for output** |
| Largest checkpoint | **21.4 GiB** |
| Warning | Cannot set thread priority without elevated privileges; previously observed as nonfatal |

These resource figures are y-cruncher's reported requirements/allocations, **not** measured peak physical disk traffic, a complete run high-water mark or proof of end-to-end success. The output estimate corrects a much earlier approximate 17 GiB menu allowance for a different preflight. The exact intended decimal source is approximately 10,000,000,001 bytes if written as one integer digit, point, and 9,999,999,999 fractional digits (subject to the actual output contract).

### E-03. Actual child process affinity anomaly — confirmed

**OWNER-REPORTED LIVE OBSERVATIONS:**

- `pgrep` showed wrapper process PID **350**, shell PID **352**, and actual `Binaries/19-ZN2 ~ Kagari` computation PID **353**. **PIDs are ephemeral diagnostic identifiers, not reusable commands or permanent process identity.**
- Initial inspection mistakenly targeted wrapper PID 350 and showed one thread allowed `0,2,4,6`. **This does not establish the real computation's affinity.**
- Corrected inspection, when PID 353 was at approximately **12m05s elapsed**, found **nine calculation threads and `9 0-23`** in their `Cpus_allowed_list` values. Therefore all were allowed all 24 logical CPUs; the mask requested at launcher level was absent for the real worker process.
- A later `ps -L -p 353 -o tid,psr,pcpu,stat,comm` snapshot reported nine threads with `PSR` values **5, 8, 11, 7, 14, 16, 19, 9, 17** (all outside or partly outside the selected mask) and lifetime `%CPU` values approximately **3.9, 1.9, 1.0, 1.3, 1.3, 1.7, 1.2, 0.0, 0.0**. The displayed scheduling states were mostly `S`, with one `D` (uninterruptible kernel wait). These observations establish that execution was **not confined** to logical CPUs 0,2,4,6; **they do not establish simultaneous 9-core work**, and neither `PSR` nor lifetime `%CPU` is a concurrency ceiling measurement.
- **Mechanism unresolved:** The separate Kagari executable or its runtime may reset thread affinity, but the evidence does not establish which component changed the mask. Do not report a proven cause.

**UNRESOLVED FOR FUTURE RUNS:** Select and validate a robust CPU-confinement mechanism for the actual child and all threads, while respecting the owner's existing four-physical-core ceiling. No code adjustment, cgroup configuration or process-affinity change has yet been applied by this chat.

### E-04. Live resource snapshots — no capacity failure apparent

**OWNER-REPORTED LIVE OBSERVATIONS:**

| Measure | Initial monitoring snapshot | Later corrected-affinity snapshot / subsequent check |
|---|---:|---:|
| Debian RAM | ~12 GiB used, 3.0 GiB available | ~12 GiB used, 3.0 GiB available |
| Debian OS swap | **0 B used** | **0 B used** |
| ext4 `/` used | **6.0 GiB** | **22 GiB** (935 GiB available) |
| Calculation PID 353 RSS | Not collected on initial wrapper-only inspection | **12,598,144 KiB** (`ps` RSS) |

The later lightweight snapshot reconfirmed ~12 GiB used, ~3.0 GiB available and 0 B OS swap. These are **snapshots, not peak measurements or proof that all later phases will fit**. Growth from 6 to 22 GiB ext4 used is expected for an active disk-backed calculation but does not by itself establish the eventual peak or the exact remaining scratch size. These were intermediate observations; final y-cruncher exit and verification results were subsequently supplied in E-05.


### E-05. First verified 10^10 phi run — completed successfully (8 Nov 2026)

**OWNER-REPORTED TERMINAL OUTPUT (not an assistant-executed test):** The exact attempt described in E-01 completed with **`EXIT=0`** from the `wsl_generate.sh` wrapper and **`GENERATION_EXIT=0`** in the calling terminal. y-cruncher reported **`Verify Output: Enabled`**, and printed completed **`Verifying Base Conversion`** and **`Verifying Decimal Output`** phases. Its internal `Spot Check: Good through 7,500,000,000` is positive but by itself does not prove all 10^10 digits; the verification-enabled run is the accepted generation-assurance level, with independent mathematical recomputation expressly waived by the owner. The validation file reported is `Golden Ratio - 20261108-021703.txt`; its bytes and existence have not yet been inspected in this chat. No packed `.bin` has yet been demonstrated or registered.

| Measurement (owner's output) | Actual result |
|---|---:|
| Total decimal digits including integer | **10,000,000,000** (`-dec:9999999999`) |
| Golden Ratio computational stage | 1713.867 s (28.564 min) |
| InvSqrt(5) within computational stage | 1434.397 s (23.907 min) |
| Small Multiply / Accumulate / Shift | 97.351 / 91.558 / 89.356 s |
| Processing hexadecimal digits | 27.066 s |
| Base converting | **1806.782 s** (30.113 min) |
| Writing decimal digits | 246.445 s (4.107 min) |
| Verifying base conversion | **1073.155 s** (17.886 min) |
| Verifying decimal output | **99.045 s** (1.651 min) |
| Combined reported verification phases | **1172.200 s** (~19.537 min; 23.53% of start-to-end wall) |
| `Total Computation Time` (y-cruncher's separately defined metric) | 3520.682 s (58.678 min) |
| y-cruncher start-to-end wall | **4981.736 s (83.029 min)** |
| Shell `real` / `user` / `sys` | **83m06.072s / 10m55.058s / 0m26.366s** |
| Start / end (local, Adelaide) | **8 Nov 2026 00:53:58 / 02:17:00** |
| CPU utilization / multi-core efficiency (y-cruncher's labels) | 14.59% + 0.21% kernel / 0.61% + 0.01% kernel |
| Reported validation filename | `Golden Ratio - 20261108-021703.txt` |
| Wrapper / shell exit | **`EXIT=0`; `GENERATION_EXIT=0`** |

**Interpretation and qualifications:** This single run establishes a practical verified phi 10^10 baseline using 12 GiB memory cap, TD4/taskqueue, 1 MiB/seek, native ext4 scratch and verification ON. The owner expressed a preference to **keep the present tuning** rather than undertake further optimisation. Base conversion and verification are major real costs. Do not equate `Total Computation Time` to wall time or apply phi's time to other constants or 10^11 by linear scaling. The earlier **CPU-affinity anomaly remains open**: successful completion does not prove four-physical-core confinement. The console's initial y-cruncher launcher identification showed Build 9547-gcc while the final calculation report identified Build 9547-icx; the selected `Kagari` compute binary and 9547 build remained consistent, so the different compiler suffixes are recorded as an observation, not asserted to be a failure. **No evidence yet of post-run file inventory, actual retained scratch, converter execution, packed scanner result, G: registration or deletion.**

### E-06. Historical immediate post-run plan (now superseded by E-09/E-10)

Read-only inspect the actual `/home/u/outlandish-work/phi_10000000000_20261107T142358Z_3975` directory; list exact `.txt` decimal source and validation report; check their sizes and the saved report's verification lines; list/measure residual `swap/`; check ext4/T:/G: capacity. Do not delete, move or regenerate the source. After file identity and destination checks, preview current `wsl_convert.py` conversion into a **new** T:-staging `.packed.bin`, specifying `--keep-text` and the correct 10^10 digit count. Only execute conversion after checking its preview. Then run Windows sampled packed verification and a **full 10^10-digit packed Powerball scan** whose independently read digest matches the conversion receipt. Once packed data have passed and durable placement is agreed, remove only explicitly inspected, unneeded intermediates and retain small logs/verification evidence. Existing G: byte-format retirement and packed registry/promotions remain separate operations.

### E-07. Owner-supplied post-run filesystem inventory (8 Nov 2026)

**OWNER-REPORTED TERMINAL OUTPUT:** `pgrep -af '[y]-cruncher|[K]agari'` had no matching processes. The exact run directory `/home/u/outlandish-work/phi_10000000000_20261107T142358Z_3975` contained:

| Entry | Size / evidence |
|---|---:|
| `Golden Ratio - Dec - Newton.txt` | **10,000,000,001 bytes** (10^10 decimal digits + decimal point) |
| `Golden Ratio - 20261108-021703.txt` | **14,252 bytes**, saved validation report |
| `run.log` | **27,659 bytes** |
| `swap/` | **8.0 KiB**; only small `ycs-0-0/` structure listed, no substantive residual swap data shown |
| Work directory as a whole | **9.4 GiB** |
| ext4 `/dev/sdd` | 1007 GiB total, **946 GiB available**, 11 GiB used |
| Host T: mount | **2.6 TiB available** |
| Host G: mount | **3.5 TiB available** |

Saved report contained the expected constant name, 9,999,999,999 decimal places, positive 7.5e9 spot-check and the `Verifying Base Conversion` and `Verifying Decimal Output` phase labels. This inspection is consistent with a verified-generation output; converter's own report-validation gate remains binding. **No packed file or receipt was reported yet.**

### E-08. Historical G: staging plan (G: path and scanner prerequisite superseded by later owner decisions)

The owner requires each constant's **5,000,000,000-byte** packed output to be created successfully under the designated G: production root, with minimal redevelopment and prompt cleanup of verified large intermediates. Direct conversion into a new isolated **G: packed staging subdirectory** was recommended (proposed folder `G:\OUTLANDISH_01\large_artifacts\packed_v1\staging\`, to be confirmed on disk) to avoid a redundant 5 GB T: copy. Existing `wsl_convert.py` insists on pre-existing `output-root/staging`, uses create-only hard-link publication and produces a nearby `*.wsl-receipt.json` with **`PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY`** scope; success at G: cannot be assumed until tested. Keep the source decimal text with `--keep-text` until a sample verification and full packed scan independently confirm the stored file/digest. Then perform **exact-path** cleanup of the decimal source, not a wildcard deletion. Real packed registration/atomic promotion remains to be implemented or separately addressed; do not claim that a staged file is registered merely because it is on G:. Legacy byte-format data and the still-active old registry must be retired coherently in a separately controlled operation.

### E-09. First 10^10 phi packed conversion and sampled check (owner-reported PASS)

**OWNER-REPORTED OUTPUT, 8 Nov 2026:** The owner first tested G: staging hard-link creation/publication with tiny disposable files and obtained **G: HARD-LINK TEST PASS**; test files were removed. `wsl_convert.py` preview confirmed the correct `G:\OUTLANDISH_01\large_artifacts\staging` destination, exact 5,000,000,000-byte packed size, source/report identity and `--keep-text`. Actual conversion then completed with:

- Input: `/home/u/outlandish-work/phi_10000000000_20261107T142358Z_3975/Golden Ratio - Dec - Newton.txt` (10,000,000,001 bytes).
- Output: `/mnt/g/OUTLANDISH_01/large_artifacts/staging/digits_golden_ratio_10_to_10.packed.bin` (5,000,000,000 bytes reported).
- Receipt: same output name plus `.wsl-receipt.json` in staging.
- **Streamed packed SHA-256:** `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d`.
- Converter reported `PACKED CONVERSION PASS`, elapsed **159.875 s**, shell `real` **2m39.957s**, `CONVERSION_EXIT=0`, and **no complete persisted-file readback**.
- Windows `WSL_Verify_Packed.bat` reported **`PACKED STAGING SAMPLE VERIFICATION PASS`**, 12 samples, correct declared length, `full_file_sha_independently_recomputed=false`, `no_registration=true`, and `VERIFIER_EXIT=0`.

Neither check establishes that the *entire persisted packed file on G:* matches the receipt. This remains pending. Owner previously approved mandatory deletion of the exact large decimal source **after full-file integrity confirmation and durable publication**, with small logs/reports/receipts retained. Reruns may intentionally replace an existing published binary, but do **not delete the old target in advance** of having a complete validated replacement ready; use a reviewed same-volume replacement approach. The established directory names are `staging`, `digits`, `results`, `logs`, `scratch` under `G:\OUTLANDISH_01\large_artifacts`; the proposed separate `packed_v1/` subtree was withdrawn.

### E-10. Scientific scan discrepancy reported; scan result not accepted

**OWNER-REPORTED OBSERVATION, 8 Nov 2026:** While attempting the new packed Powerball scan, the owner noticed that initial match results appeared different from earlier results obtained on shorter constant files for what should be the shared starting digits. The owner did not provide the exact differing counts, locations, whether the earlier file used the same constant, or a completed `SCAN PASS` report. Therefore neither a scanner defect nor the source of the difference is established. The current scan, if still active, may be interrupted without touching the binary; any partial CSV/report remains **diagnostic only**. The scientific scanner is not a prerequisite for independent complete-file digest checking or completion of the six production binaries. Qualification and reconciliation are deferred as specified in D-06.

## 4. Source, test, documentation and production-state changes since v6

- **SOURCE / TEST:** No Python, Bash, BAT, converter, scanner, registry or test-file modification has been reported or performed in this chat since v6. A scanner source re-review and synthetic fixture tests are now required *before* full scientific scans.
- **PRODUCTION G:** The new 5,000,000,000-byte phi packed file and its receipt were published **to G: `staging/` only**, not yet `digits/`, and a 12-sample Windows verification passed. No packed promotion, registry edit or legacy byte deletion has been reported. Legacy retirement remains approved in principle; actual safe execution is pending.
- **DOCUMENTATION:** This file is now living addendum rev0.5. The approved v6 consolidated handover is retained unchanged as the baseline; where it still directs legacy prefix comparisons or treats 10^10 generation as unstarted, this addendum records the later controlling owner decisions and actual launch evidence.

## 5. Risks, anomalies, follow-ups and completion checkpoints

| Topic | Current state | Next handling |
|---|---|---|
| Phi y-cruncher generation | **PASS**: 10^10 digits, verification enabled, EXIT=0, saved report/text present | Preserve small `run.log` and validation report |
| Phi nibble conversion | **PASS at staging:** 5,000,000,000 bytes reported, streamed digest and receipt, 159.875 s | Independently stream/read all of G: packed file; match digest to receipt |
| Windows staged sample verification | **PASS**: 12 samples, VERIFIER_EXIT=0 | Does not substitute for full stored-file hash |
| Phi full-file integrity on G: | **PENDING**; earlier scanner-based hash plan now superseded | Use independent streaming SHA-256 with strict receipt/size/identity match; do not rely on scientific scanner |
| Phi published production in `digits/` | **PENDING** | Safe staging-to-production same-volume move/replacement; maintain corresponding receipt/provenance, no misleading legacy registry state |
| Decimal-source deletion | **MANDATORY AFTER SUCCESS, PENDING**: 10,000,000,001-byte phi source retained with `--keep-text` | Delete exact owned path only after full-file integrity and durable publication; preserve small evidence |
| Scientific scanning / matching results | **DEFERRED; possible shared-prefix discrepancy** | After all six files finished, review scanner source, test at least two known hits per P1/P2/P3 plus negatives/boundaries, reconcile earlier baselines, then scan six |
| CPU affinity | **CONFIRMED NONCONFINEMENT** on Kagari threads (0–23 permitted), notwithstanding `taskset 0,2,4,6`; completed successfully | Preserve as an unresolved safety/configuration risk for later production runs; do not claim enforced four-core limit |
| OS memory and swap | Samples around 12 GiB RAM used, 3 GiB available, Linux OS swap 0 B | Continue capacity checks for other constants; no general retuning or larger WSL limit approved |
| Legacy byte files | Owner approves retirement and waives old-format prefix comparison | Exact-path, registry-coherent cleanup; do not silently leave active entries referencing deleted files |
| Scale | **Six 10^10-digit files**, not 10^11 | Generate, independently full-hash-verify and publish sequentially; do scientific scans in later qualified phase |

## 6. Addendum revision history

| Revision | Date | Entry |
|---|---|---|
| 0.1 | 2026-11-08 | Created clean post-v6 incremental template; no new findings at that time. |
| 0.2 | 2026-11-08 | Added decisions on production `-verify:1`, independent computation waiver, nibble-only production, legacy-prefix comparison waiver and retirement, tuning closure, first 10^10 phi launch, actual resource observations, **Kagari 9-thread `0-23` CPU-affinity anomaly**, and owner decision to let the then-in-progress run continue. |
| 0.3 | 2026-11-08 | Recorded the **verified 10^10 phi generation completion**: end-to-end 4981.736 s (83.029 min), shell `real` 83m06.072s, both verification phases completed, `EXIT=0` and `GENERATION_EXIT=0`, phase breakdown, final validation-report filename and accepted continuing tuning baseline. Affinity nonconfinement remains unresolved; packed conversion, stored digest/scanner verification, promotion and cleanup still pending. |
| **0.4** | **2026-11-08** | Recorded owner commitment to **six 10^10 packed constants** (dropping 10^11), inspected phi source/report/log/swap exact sizes, capacity and no running y-cruncher; established planned direct G: isolated packed staging and delete-source-only-after-full-scanner-hash workflow. Packed conversion and formal registration not yet done. |
| **0.5** | **2026-11-08** | Recorded actual phi 10^10 packed conversion on G: staging, SHA-256 and Windows sample-verifier PASS, and the owner-reported early match discrepancy. Owner deferred all scientific scanning until six packed files are independently full-hash-verified and scanner source/known-hit synthetic fixtures are qualified. Replaced full-scanner-dependent stored-file integrity requirement with standalone SHA-256 readback. Mandatory source cleanup and safe G: publication remain pending. |

## Recording rules for subsequent revisions

- Keep evidence types clear: **OWNER DECISION**, **OWNER-REPORTED OUTPUT**, **SOURCE-INSPECTED**, **PROPOSED**, **UNKNOWN**. A terminal message from the owner's machine is evidence **reported by the owner**, not an assistant-executed test.
- Do not conflate running, process exit 0, y-cruncher verification PASS, successful packed conversion, complete persisted packed-file hash match, registry promotion or scientific validation. Each has separate evidence requirements.
- Preserve exact run paths, output reports, settings, actual data sizes and warnings; include significant failures/anomalies without retroactively replacing them with later success.
- Future changes to this living document keep the filename `OUTLANDISH_01_Living_Handover_Addendum.md`, increment internal revision, and append a dated revision-history entry. The next consolidation merges the accumulated deltas into a successor baseline before resetting the addendum.
- This document does not itself authorise further large runs, destructive G: operations, code changes or parent-project integration changes. Execution approval remains with the owner.
