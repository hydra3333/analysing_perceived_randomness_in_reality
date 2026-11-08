# OUTLANDISH_01 — Integrated Research, Generation, Matching and Parent-Project Handover

**Consolidated handover v6 — DRAFT FOR OWNER REVIEW**  
**Prepared:** 7 November 2026 (Australia/Adelaide), from the owner's two uploaded source/document archives and prior v5 + living-addendum v0.5  
**Status:** PROPOSED CONSOLIDATION ONLY. **Not ratified, not installed, not a change to running source, and not authorisation to run calculations, delete files, alter registries or change WSL settings.**  
**Supersedes, if and only if approved by the owner:** `OUTLANDISH_01_2026-11-07_Project_Status_and_Packed_WSL2_Performance_Plan_v5.md` plus `OUTLANDISH_01_Living_Handover_Addendum.md` revision 0.5 *as the primary conversation handover*. Both originals remain retained, immutable provenance documents.  
**Scope:** The standalone `GAIS/OUTLANDISH_01` mathematical-constant digit investigation, its native-Windows predecessor, its `OUTLANDISH_WSL` branch and the eventual interface to `hydra3333/analysing_perceived_randomness_in_reality`.

> **First-read rule for any successor AI:** Read §§1–6, 10–13, 16–18 before proposing any command or change. The owner is presently finishing *targeted performance/feasibility assessment*, NOT initiating a new implementation rewrite. Read the actual installed code and current runtime state before making operational claims. The most recent completed run was a 1 MiB/seek y-cruncher `benchio`; **its scratch-directory inspection is the next pending action**. No new benchmark or large calculation is yet authorised.

---

## 1. Mission, success criteria and boundaries

### 1.1 Why OUTLANDISH_01 exists

The owner is exploring an unconventional, intentionally speculative question: whether long digit streams of mathematical constants contain patterns, positions or positional transitions related to historical lottery results that are worth investigating as candidate prediction methods. The primary purpose is **to obtain scientifically usable constant-digit inputs and investigate matching/positional rules**, eventually contributing well-specified methods and data to the separate, larger predictive-randomness research programme.

That is an experimental programme, not a claim that π, φ or any other constant predicts lottery draws. Large coincidence spaces, historical selection and multiple testing must be acknowledged; surprising results may nevertheless be investigated without automatically dismissing exploratory methods.

There are **three interacting deliverables**:

1. **Production-quality numerical data:** Generate and verify all **six** selected constants to **10^10 total decimal digits each** in a reasonable owner-acceptable elapsed time, using the new nibble-packed representation. Then obtain defensible **per-constant** compute/disk/RAM/time feasibility and limits for **10^11 digits each**. The owner decides whether the cost is acceptable before any 10^11 production job. The earlier 10^12 idea is historical aspiration, **not** the current programme target.
2. **Matching and experimental research:** Run fully specified Powerball and, later, Oz Lotto matching/position/transition/reporting experiments on those streams. Preserve the original definitions and established results; consider drawn-order versus any-order/reordered-only variants, and additional representation-based approaches under separately reviewed specifications.
3. **Parent-project transfer and support:** Eventually prepare a practical package of source, format/data inventory, hashes, verification, matching algorithms, tests, reports, scientific method definitions and explicit limitations. Provide continued two-way clarification through the owner to the **Claude primary designer/coder** and **ChatGPT independent reviewer** of `analysing_perceived_randomness_in_reality`. Each constant-derived approach can become one or more separately specified candidate methods in that parent project; actual admission, integration, scoring and ranking remain under the parent's own rules and review process.

The six constants are **data sources**, not automatically six fully specified predictors. Different matching/transition constructions using one constant may constitute different candidate methods. A proposed method requires an explicit algorithm to produce a forecast using only permitted past information; historical matched positions alone do not yet do that.

### 1.2 Pragmatic completion criteria

- A usable, versioned, checked format for each production file; a manifest with constant identity, total digits, precise length, SHA-256, source/report provenance, applicable transformations, status and retention information.
- All six **10^10** streams generated/validated/available, unless the owner consciously revises scope after measured resource evidence; reliable regeneration/diagnosis commands and controlled scratch management.
- A defensible table for **10^11** feasibility by constant, including generation **and** decimal-to-packed conversion, transfers, scanner and temporary storage costs, with observed vs estimated vs unknown clearly separated.
- Existing scanned historical results remain reproducible; any new order or representation variant is separately versioned and tested, not silently substituted.
- Demonstrable handover to the parent project with code/data packaging that does not place multi-GB binaries in Git; questions can be answered by this OUTLANDISH chat or a documented successor.

### 1.3 Non-goals and authority firewall

- **Do not change the parent project's** method registry, experiments, protected holdout, runner, source policy, coordinator or scientific evaluation procedures from this subproject's authority. Integration requires the parent Claude/ChatGPT/owner process.
- **Do not redevelop functioning Python/Bash code simply to make the documentation tidier.** Only targeted correctness, safety or interoperability modifications after evidence and approval.
- **Do not repeat** the legacy byte-per-digit versus packed scanner *speed-comparison project*: the owner decided to skip it. Ordinary correctness regressions and useful measured scan timings remain warranted.
- **Do not revive** Windows Sandbox, privilege modifications for native-Windows disk swap, an independent arbitrary-precision/external-FFT engine, alternative VM routes or high-concurrency stress testing by default.
- **No implicit calculation** at 10^10/10^11, no WSL RAM or CPU expansion, no wholesale G: changes, no automatic deletion of legacy originals, no unreviewed Oz Lotto code, no claims of predictive success from historical matches.

## 2. Decision/evidence vocabulary and authority hierarchy

Use these labels in subsequent documentation and discussion:

- **OWNER DECISION:** Explicitly accepted intent or boundary. It may be changed only by a new owner decision.
- **SOURCE-INSPECTED:** The supplied snapshot actually contains the described code or data. This is *not* evidence that the same bytes are currently installed on the owner's PC.
- **OWNER-REPORTED VERIFIED:** Real user-supplied terminal/log/run output or operator confirmation. No assistant has direct access to live E:/T:/G: volumes.
- **MEASURED:** A value directly observed in a stated run. Distinguish process internal wall, shell `real`, CPU time, peak resident memory, logical resource estimates and benchmark-generated results.
- **PROPOSED/DEFERRED:** Research direction or recommended step not implemented/authorised.
- **UNKNOWN/REQUIRES CHECK:** Evidence not supplied, unresolved semantics or live runtime uncertainty.
- **HISTORICAL/SUPERSEDED:** Retained for provenance; not an instruction to apply in the current environment.

**Operational evidence, highest to lowest:** live files/configuration/results/receipts and actual observed commands; current installed source; separately reviewed science definitions and decisions; this ratified handover (once approved); earlier v5 and addendum; early v1–v3/5-Nov notes, candidates and historic source. An archived source snapshot must not override a newer tested implementation merely because its README is detailed.

The **owner's new clarification** in this conversation is part of the intended v6 scope: the constant datasets and experimental work are to be fed into the parent project, not merely scanned as a self-contained curiosity; a support/dialogue relationship is a completion requirement. The document records that intent but does not create parent-project approval.

## 3. Canonical constants, digits and mathematical conventions

| ID | Quantity | Conventional beginning including integer digit | y-cruncher source / transform |
|---|---|---|---|
| `pi` | π | `3.1415926535...` | `pi`; no transformation |
| `phi` | Golden ratio | `1.6180339887...` | `goldenratio`; no transformation |
| `e` | Euler's number | `2.7182818284...` | `e`; no transformation |
| `log2` | Natural log 2 | `0.6931471805...` | `log:2`; no transformation |
| `gamma` | Euler–Mascheroni constant | `0.5772156649...` | `gamma`; no transformation |
| `lemniscate` | Lemniscate **half-perimeter** constant | `2.6220575542...` | y-cruncher `lemniscate` yields full perimeter ~`5.244115...`; apply exact *streaming division by two* before packing |

**Count convention:** `N` is always the number of decimal digits **including the leading integer digit**. The decimal point is discarded, not a digit. y-cruncher uses `-dec:(N-1)` for the fractional digits. All match positions are **zero-based decimal-digit offsets**, beginning at the integer digit. This is independent of physical byte layout. No implicit leading-zero trimming is allowed (`log2` and `gamma` both begin with `0`).

The selected set is fixed at six for this phase. The historical `Potential_Other_constants.txt` is speculative reference material, not approval to enlarge the production set.

### 3.1 Physical binary formats are different contracts

**Legacy numeric-byte file:** one byte per digit, numeric byte values 0–9 (not ASCII `0x30`–`0x39`); `N` decimal digits require **N bytes**. Current six G: active files are in this format.

**New packed file:** `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`: byte `i` contains digit `2i` in the high nibble and digit `2i+1` in the low nibble; all real nibble values must be 0–9. If `N` is odd, the last low nibble is **zero padding, not a real digit**; exact `N` must be in the receipt/registry. No decimal point/header. Example `1.61803...` starts bytes `0x16 0x18 0x03...`. File size = `ceil(N/2)` bytes.

**Never** pass packed files to the legacy byte reader, verifier or legacy registry; the two are intentionally incompatible, even if both filenames end in `.bin`. The new package uses `.packed.bin`, format ID and JSON receipt. Historical `CHANGES_v0_2.md` loosely mentions "ASCII digits per byte"; the above is the actual **numeric BCD** contract, not ASCII storage.

| Total decimal digits per constant | Legacy byte/digit | New packed bytes | Six final packed files | Plain source decimal text ~minimum |
|---:|---:|---:|---:|---:|
| 10^9 | 1,000,000,000 B | 500,000,000 B (0.466 GiB) | 3 GB | 1,000,000,001 B |
| 10^10 | 10,000,000,000 B | **5,000,000,000 B (4.657 GiB)** | **30 GB** | ~10,000,000,001 B |
| 10^11 | 100,000,000,000 B | **50,000,000,000 B (46.566 GiB)** | **300 GB** | ~100,000,000,001 B |

These figures are **exact format/output capacities**, not y-cruncher scratch, checkpoints, text conversion staging, logs, backups, copies or proof that a generation run fits. Six legacy 10^9 active files use approximately 6 GB and remain separately protected. Production retention of originals or repeated candidates adds storage.

### 3.2 Scientific sequence encoding is a different question from file packing

The current scanned pattern representation is `FIXED2`: every selected lottery ball is encoded as two **decimal digits** (`03`, `12`, etc.) in the mathematical constant stream. This has **nothing to do with BCD byte packing**: a packed reader must decode the correct decimal digit at every logical offset.

The original owner's **Representation 2 / Combination Index / Compact Encoding** concept is a future alternative *scientific encoding* of lottery combinations, not a physical storage choice. It was proposed for both games but lacks a ratified specification and implementation. Likewise natural-width ball representations (`3` instead of `03`) were noted historically but are not current methods. Keep these ideas separate, explicitly versioned and deferred unless reprioritised.

## 4. Platform, locations and environment (last known evidence)

| Location | Role | Current restriction |
|---|---|---|
| Git repo `https://github.com/hydra3333/analysing_perceived_randomness_in_reality`, subfolder `GAIS/OUTLANDISH_01/` on E: | Existing native-Windows code, `.toml`, original project docs and pre-holdout Powerball CSV | Do not rewrite, relocate or edit generated TOML state merely for the handover |
| `GAIS/OUTLANDISH_01/OUTLANDISH_WSL/` on E: | **Single source-controlled editable WSL tool tree:** scripts, BAT wrappers, tests, docs | Do not create a second divergent editable Debian copy; no large generated data on E: |
| `/mnt/e/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/GAIS/OUTLANDISH_01/OUTLANDISH_WSL` | Debian view of E: WSL source | Bash scripts and Linux converter may run from here |
| `T:\OUTLANDISH_WSL\Debian\ext4.vhdx` | Debian WSL2 native ext4 filesystem on physical T: HDD | **Never delete/compact/unregister casually**; ext4 capacity differs from host T: free |
| `/home/u/outlandish-test/` | Linux y-cruncher binary and retained 100m reference | Do not delete the executable/reference |
| `/home/u/outlandish-work/` | Dedicated per-attempt Linux y-cruncher ext4 scratch/text/reports and `benchio` | Inspect exact directories before any cleanup |
| `T:\OUTLANDISH_WSL\rehearsal_artifacts\` | Tested disposable NTFS packed staging and full Powerball scan reports | Preserve 100m example until authorised |
| `G:\OUTLANDISH_01\large_artifacts\` | Existing registered production **legacy** 10^9 numeric-byte files and future guarded packed staging | No WSL rehearsal writes or production promotion until separately reviewed |

Hardware: **AMD Ryzen 9 3900X**, 12 physical / 24 logical CPUs; **32 GiB host RAM**, Windows 11. T: = **WDC WD6003FZBX-00K5WB0**, ~6 TB SATA mechanical HDD (physical disk no. 2), with **2,897,650,704,384 B** host free at earlier 7-Nov inventory. Debian 13 (Trixie) in WSL2 v2.5.7.0, Linux kernel 6.6.87.1-1. Static Linux y-cruncher **v0.8.7 Build 9547**, binary under `/home/u/outlandish-test/y-cruncher v0.8.7.9547-static/y-cruncher`. Native-Windows y-cruncher v0.8.7.9547b exists separately.

Debian: **Python 3.13.5**, standard library sufficient for WSL converter; WSL usable RAM ~**15.6 GiB**, OS swap ~4 GiB. `%USERPROFILE%\.wslconfig` was **absent** at inventory; no subsequent setting change reported. Native ext4 `/dev/sdd` capacity ~**1007 GiB**, previously **955 GiB available**. VHDX physical allocation at inventory 1,326,448,640 B; dynamic growth is not the same as ext4 free space. `vm.swappiness=60` observed, not tuned. No demonstrated Linux-OS-swap peak during the longer benchmarks. Host T: physical free and ext4 filesystem maximum are separate constraints.

Windows project root `.venv` was used for existing source and Windows WSL wrapper BATs (NumPy **2.5.4** observed). `activate_venv.bat` is existing and not modified. Do **not** use Windows `.venv` inside Linux, modify the common dependency-install BAT or install an extra Linux numerical environment without need.

**Four-core maximum is an owner safety limit.** `taskset -c 0,2,4,6` selects four distinct physical cores (SMT sibling pairs 0/1, 2/3, 4/5, 6/7); `-TD:4 -PF:taskqueue` does **not** itself enforce OS affinity. y-cruncher printed `4 / ? / 24 (all cores)` in a topology display; whether each worker thread actually retained the mask was **not directly checked**. Future read-only `/proc/<pid>/task/*/status` `Cpus_allowed_list` inspection during a bounded, separately approved run is needed before declaring enforcement proven. Previous *native-Windows* high-concurrency operations led to abrupt host power-offs; do not run stress-to-failure tests.

**Current memory decision:** Keep WSL2's ~15.6 GiB allocation for now; cap y-cruncher at about **12 GiB** in current comparative work while preserving Windows RAM and host responsiveness. Earlier 20/24 GiB WSL proposals and 14–18 GiB y-cruncher caps are **not approved current settings**. `-M` is a requested maximum, not necessarily observed working RAM. y-cruncher's file-based far memory/swap is **not** the Debian OS swap; avoid OS paging. Do not propose `tmpfs` as a solution for multi-tens-of-GiB scratch without evidence and separate approval.

## 5. Current software inventory, as supplied (read-only snapshot)

### 5.1 Native-Windows predecessor — installed lineage v0.2r4 (indicative original archive)

- `outlandish_big_constants.py`: preview/explicit-run native Windows y-cruncher pipeline, text conversion to numeric-byte `.bin`, integrity/prefix verification and promotion.
- `outlandish_artifacts.py`: path restrictions, symlink/junction refusal, artifact audit, registry promotion, shared lock, pending retirement, manual recovery; v0.2r4 allows controlled automatic predecessor retirement **when enabled**.
- `outlandish_config.py`: fixed-location `outlandish.local.toml`, user parameters and generated registry sections.
- `outlandish_powerball_stage_a.py`: NumPy single-process FIXED2 Powerball P1/P2/P3 historical matching, location CSV, summaries and P1-anchored consecutive-draw transitions.
- `test_outlandish_v02.py`: synthetic tests; earlier owner Windows run **25 tests, 24 passed and 1 allowed symlink skip** (later Sandbox package run is different evidence, see §14).
- `README.md`, historical v0.2 README, original scope, `POWERBALL_preholdout_only.csv`, convenience CMD launchers, G: active registry `outlandish.local.toml` and its backup.

**Original registry and data snapshot:** all six constants recorded active at **10^9 digits each**, each exactly 1,000,000,000 numeric bytes. `outlandish.local.toml` in the indicative archive has six `[state.active.*]` entries, no `[state.pending_retirement]` entries and `settings.retention.delete_superseded = true`. The file's header still says "keep it out of Git", but the owner deliberately chose to **track the local TOML in Git**; treat the header as outdated, not as a policy reversal. This archive is **not live validation of G: files**.

Native-Windows v0.2r4 allows automatic retirement of a *precisely verified* predecessor after a successful newer promotion, a published pending record and file identity checks. It cannot ensure arbitrary external readers are idle; `retire` and `recover-retirement` exist. **Do not inherit the `delete_superseded = true` behaviour into a new packed registry**: whether/how to retain six originals for packed promotion must be explicitly reviewed and owner-decided. No same-length `10^9` regeneration/promotion is appropriate merely as a check.

The old file tree and source history moved from `src/GAIS/` to `GAIS/` following a GAIS relocation and targeted Git history rewrite on 6 Nov. History cleanup evidence resides in `exchange/HISTORY_CLEANUP_2026_11_06/`; old commit IDs or locations may not describe present HEAD.

### 5.2 WSL/packed branch — owner-installed and exercised candidate

**As last reported:** `OUTLANDISH_WSL_Packed_v0_2r2` plus installed benchmark-only launcher change described in `README_Benchmark_Verification_v0_2r3.md`. The ZIP snapshot contains the opt-out flag in `wsl_generate.sh`. Its older `README.md`, `RESOURCE_ESTIMATES.md`, `CHANGES_v0_2.md` and v0.2r3 README predate successful later field tests in their wording. They are **not** current status documents.

| Source | Current role / interface |
|---|---|
| `wsl_generate.sh` | Bash native Linux generation, **preview by default**, unique ext4 attempt, swap mode default, `-verify:1` default, `-TD:1 -PF:none`, initial `-M:4g`; `--run` required, plus exact `--ack-large-run N` for N>=10^9; `--td` accepts 1–4. `--benchmark-no-verify` separately makes throwaway `-verify:0` outputs, ineligible for packing/promotion. **No auto-conversion.** |
| `wsl_format.py` | Six known decimal prefixes, packed high-first BCD version, nibble checks, sample plan, format helpers. |
| `wsl_convert.py` | Debian `python3` stdlib streaming text validation, packed conversion, source and packed hashes, bounded persisted sample readback, create-only publication, JSON receipt, exact owned text cleanup after success (unless `--keep-text`). Enforces saved report evidence including base-conversion and decimal-output verification. |
| `wsl_verify_windows.py` | Windows read-only receipt/sample verification and optional sampled comparison to old G: numeric-byte prefix. **Not a complete full-file digest.** |
| `wsl_scan_packed_powerball.py` | Windows NumPy bounded-memory P1/P2/P3 scanner, every logical digit offset, CSV/JSON, W→W+1 reports. Full-file scan hashes entire packed input and compares it to converter receipt without extra verification-only read. Preview default; `--run` for actual scan. |
| `WSL_Tests.bat`, `WSL_Verify_Packed.bat`, `WSL_Scan_Packed_Powerball.bat` | Launch existing Windows root `.venv` and relevant source; no new venv. |
| `test_wsl_packed.py` | Synthetic test suite: odd padding, source handling, receipt tamper, optional legacy prefix, P categories/cross-boundary/holdout gate; owner reported **12 tests, OK, 1 skipped symlink case**. |

**Known implemented fixes:** v0.2r1 fixed `%~dp0` quoting in `WSL_Tests.bat`; v0.2r2 corrected recognition of the *saved* y-cruncher report (not a misleading console `Verify Output: Enabled` line). v0.2r3 benchmark opt-out was owner-installed and exercised by the successful 3e9 disposable run. Source-inspected new wrapper permits `--benchmark-no-verify`, `--run`, exact large-run acknowledgement and bound `--td 1..4`.

**Separation deliberately retained:** no second mutable packed TOML/active registry yet; receipts and staged file are not production registration. Do not assume copying a new TOML beside a WSL BAT makes `outlandish_config.py` read it: the old module anchors its settings file beside its own Python module. A future packed registry will be separately versioned and isolated.

## 6. Current production and scientific status dashboard

| Subject | Status | Precise evidence / qualification |
|---|---|---|
| Six legacy 10^9 numeric-byte streams | **Owner-reported verified and active** | Native-Windows v0.2r4/TOML snapshot, 6 files × 1,000,000,000 B on G:; not rehashed in this chat |
| Linux y-cruncher calculations | **Working** | Verified sample up to 10^9; owner ran disposable unverified 3×10^9 and `benchio` successfully |
| 100m φ WSL text → packed → Windows checks → Powerball scan | **PASS** | 50,000,000 B packed, digest and scans below; on T:, **not G:** |
| Packed format/reader | **Working for this demonstrated pipeline** | `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, synthetic tests; not a registered production replacement |
| Six **10^10** packed production streams | **NOT generated** | First major numerical production objective |
| Six **10^11** streams | **NOT approved / feasibility unknown** | Per-constant estimates and owner cost decision required first |
| Physical I/O performance | **Bottleneck under investigation** | First 1 MiB/seek `benchio` gave low throughput ratio and unexpected write/read asymmetry |
| Packed active production registry/promotion | **Not implemented** | Needs isolated design/testing and explicit preservation/retention decision |
| Packed Powerball P1/P2/P3 | **Implemented/tested on 100m φ** | Baseline matching semantics preserved; does not implement deferred variants |
| Oz Lotto scanner | **Not implemented** | Historical O1/O2/O3 research idea, several ordering questions unresolved |
| Extra Powerball drawn/any/reordered classes | **Deferred** | Separate proposal record, no code yet |
| Position-to-prediction mapping | **Not demonstrated** | Matches and W→W+1 summaries are descriptive, not a validated forecast algorithm |
| Parent-project integration | **Future, cooperative** | Requires package and two-way communication with parent Claude/ChatGPT and owner |

## 7. Original scientific design and implemented matching

### 7.1 Historical dataset isolation

Original Powerball Stage A uses `POWERBALL_preholdout_only.csv`: **433 historical draws**, IDs **1144–1576**, exclusive cutoff **1577**, starting after the 2018 rule change. The supplied indicative CSV was inspected: 433 rows, first `1144` dated 2018-04-19; last `1576` dated 2026-07-30. Schema:

```csv
Draw_Number,Date,Drawn_1,Drawn_2,Drawn_3,Drawn_4,Drawn_5,Drawn_6,Drawn_7,Powerball
```

Main balls preserve operator-reported draw order. Use the **isolated development copy**, not the live/authoritative master or any draws >=1577, when developing matching/predictive ideas. WSL scanner explicitly refuses at/after-cutoff IDs before parsing the other restricted fields. The original master/data fetcher belongs to the separate parent architecture, and its source rules and holdout protections may not be weakened here. **Oz Lotto requires its own separate authorised pre-holdout dataset and reader**; it must never be pooled with Powerball, nor should an Oz Lotto cutoff be invented.

### 7.2 Experimental Powerball patterns (FIXED2)

These are **exploratory category names**, not assertions about official Powerball prize-division requirements:

| Existing ID | Exact pattern at the constant's decimal offsets | Digits | Status |
|---|---|---:|---|
| **P1** | Seven mains in **operator-drawn order**, followed by the same draw's Powerball | 16 | Implemented |
| **P2** | Seven mains in **operator-drawn order**, PB not required | 14 | Implemented |
| **P3** | Any **six distinct mains** out of seven, in **any order**, followed by the same draw's PB | 14 | Implemented |

The implementation indexes P1/P2 exact ordered tuples and P3 sorted canonical six-ball sets plus PB. It does **not** materialise all 5040 permutations. Scan every decimal-digit offset (including starts at odd positions, byte/nibble boundaries, chunk boundaries and valid final starts); record exact `FIXED2` matched digit string, 0-based start, exclusive end, draw number and category. A matched offset can legitimately count under multiple draw/categories if defined; never silently force disjointness across categories.

### 7.3 Matching and reporting requirements from the original scope

- Consolidate per-draw keys and scan all eligible data, retaining **all matching positions**, not only the first hit or aggregated totals. Record constant/data identity, draw ID and category per hit.
- For each consecutive historical draw pair **W, W+1**, examine whether W has hits and W+1 has hits, and report category-specific counts and positional relationships (signed deltas, nearest position pairs and other explicitly defined statistics).
- The **original specification was P1-anchored**: W's P1 positions versus W+1 P1/P2/P3 positions. Both the original and packed scanners retain a `transitions.csv` output with rows when both adjacent draws have any category hit; but **the signed-delta columns are calculated from W's P1**. When no P1 exists those deltas are blank. Reporting adjacent P3/P3 pairs by independently inspecting `matches.csv` is a *different exploratory analysis*, not an implemented predictive law.
- Preserve exact start offsets and all matching rows; record complete input-size, duration, candidate starts, count, format, CSV cutoff, code/method version and source digest evidence.
- A compact scan summary and full `matches.csv`/`transitions.csv` enable later postprocessing without rescanning multi-GB digit files for every exploratory statistic. Further reports should use clear, consistent denominators and disclose whether multiple matches per draw are retained or collapsed.
- Original scanner is one NumPy-vectorised process. Do not introduce multiprocessing simply for cosmetic modernisation. Bounded-chunk scanning supports inputs much larger than RAM.

### 7.4 Original one-billion-digit Powerball observations (native-Windows legacy format)

The **5-Nov historical evidence bundle** contains real compact scanner reports for π and φ, N=10^9, 433 draws. Its earlier measured figures (from that report snapshot) are:

| Metric | π 10^9 | φ 10^9 |
|---|---:|---:|
| P1 | 0 | 0 |
| P2 | 0 | 0 |
| P3 occurrences | **29** | **25** |
| Candidate starts | 642,075 | 644,210 |
| Reported Stage-A scan wall | **27.598385 s** | **27.871085 s** |
| Adjacent historical draw pairs with any hits at both ends | 3 | 2 |
| W P1 → W+1 any transitions | **0** | **0** |

A later v5 summary separately cites a π 10^9 scan of **27.278917 s**. These are **not to be forcibly reconciled into one "correct" time**: preserve both with their provenance/run context; do not assume they are the identical invocation. If needed compare actual per-run `summary.json`. The older five adjacent P3/P3 exploratory pairs (derived separately, not generated by P1 transition calculation) were:

| Constant | W → W+1 | Position W | Position W+1 | Signed Δ |
|---|---|---:|---:|---:|
| π | 1195→1196 | 974,512,578 | 803,790,670 | −170,721,908 |
| π | 1470→1471 | 769,827,143 | 491,947,932 | −277,879,211 |
| π | 1490→1491 | 17,628,072 | 564,308,006 | +546,679,934 |
| φ | 1233→1234 | 655,598,637 | 722,416,094 | +66,817,457 |
| φ | 1552→1553 | 102,146,164 | 901,318,284 | +799,172,120 |

These numbers are **historical descriptions, not next-draw forecasts**. A convenient IID uniform-decimal benchmark gives rough expected P3 hits of `433 × 5040 × N / 10^14` (approximately 21.8 at 10^9 per constant), omitting dependencies and repeated keys. Approximate P1 expected hits are `433 × N / 10^16`, so **zero P1 is unsurprising even at considerably greater sizes**. The uniform model is a *reference/null*, not a claim that mathematical-constant digits are proven IID. Preserve space for exploratory unusual-pattern diagnostics, but control chance/multiplicity claims.

### 7.5 Completed packed 100-million φ rehearsal (new format)

**OWNER-REPORTED VERIFIED 7 Nov:** 100,000,000 total phi digits generated in Debian, Linux conversion to **50,000,000 packed bytes**, Windows sample validation PASS (12 blocks), full packed Powerball scan PASS in **2.819 s**, full scanned SHA-256 matched the converter receipt. Conversion reported **1.581 s**. The output remains on experimental **T:**, never registered on G:.

- Staged packed file: `T:\OUTLANDISH_WSL\rehearsal_artifacts\staging\digits_golden_ratio_10_to_8.packed.bin`.
- SHA-256 (converter and full-scanner agreement): `4cb6f6288b72f3a0ff738e72b261dc05ef5e507cfb62d29cf86b934dfd635e7e`.
- Scan report: `T:\OUTLANDISH_WSL\rehearsal_artifacts\results\packed_run_20261107T094409Z_c89da00e`.
- Full 100m scan; 433 eligible draws, exclusive cutoff 1577; 64,762 candidate starts; **P1=0, P2=0, P3=3**. `transitions.csv` header only. P3 occurrences:

| Draw | Zero-based start | Six mains matched | PB |
|---:|---:|---|---:|
| 1244 | 20,048,101 | 10, 11, 27, 18, 01, 20 | 20 |
| 1274 | 71,806,090 | 32, 07, 27, 15, 31, 09 | 07 |
| 1373 | 95,105,831 | 31, 23, 25, 13, 15, 21 | 10 |

The scanner's **~35.47 million digits/s** in this 100m case is measured, **not** a validated 10^10/10^11 speed forecast. The original byte and new packed representations have different sizes but preserve logical digit-offset semantics.

## 8. Deferred scientific development — preserve intent, do not begin implementation now

### 8.1 Proposed Powerball order refinements

The dedicated `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md` is an **owner-recorded proposal/decision to defer**, not a ratified implementation spec:

| Original category | Preserve current | Add later if specified/reviewed |
|---|---|---|
| P1: 7 main + PB | `P1_drawn_order` | `P1_any_order` (same mains any permutation, same PB last); `P1_reordered_only = any_order \ drawn_order` |
| P2: 7 main | `P2_drawn_order` | `P2_any_order`; `P2_reordered_only` |
| P3: 6 main + PB | `P3_any_order` | `P3_drawn_subsequence_order` (six mains retain relative original draw order after omitting one of seven); `P3_reordered_only` |

**Important:** *Any-order* is not shorthand for one numerical ascending string; it means every possible ordering of the selected distinct values. P3's original `any-order` semantics already exist. Sorted canonical **keys** are an implementation technique, not a requirement that the digits appear numerically sorted. PB remains in its specified final position in the proposed P1/P3 patterns. Drawn-order and any-order are **nested**, not disjoint; `reordered_only` excludes the narrower drawn-order/subsequence class. Per-category intersections must be reported clearly.

No existing P1/P2/P3 definitions are to be silently broadened or re-labelled, and no deferred design should delay the data-production pipeline. Synthetic planted/reordered/chunk/EOF/invalid/dedup tests and regression against original counts are required before adding such reporting.

### 8.2 Oz Lotto: initial research definitions and unresolved semantics

Historical owner scope: seven main numbers plus three supplementary numbers, each from 1–47; separate data, program, outcomes and reports. Experimental labels are **not official division definitions**:

- **O1:** seven main numbers (historically operator-drawn order).
- **O2:** any six mains plus any one supplementary number.
- **O3:** any six mains.

Proposed extension: drawn-order, any-order and reordered-only for each; O2/O3 need owner-approved exact relative ordering and deduplication. In particular, O2 must decide whether supplementary number is always last or may appear among the seven; whether supplementary draw order matters; whether multiple eligible selections per offset create one or several records; which relative main order is meant. Confirm authentic historical Oz Lotto drawn-order source fields and its permitted pre-holdout isolation *before* designing a reader. **No current Oz Lotto scanner or data adapter is demonstrated.** Never pool games or transfer Powerball cutoff numerically.

### 8.3 Other exploratory ideas

Investigate independently versioned alternative combination-index/compact encodings, natural-width sequences or positional transformations *if they support an explicit testable hypothesis*, with appropriate null cases and own experiment IDs. The six constants can support multiple candidate methods, but the parent project makes final decisions about admission, variants, TOP/WORST comparison, scoring and ensembles. Do not inflate the near-term work by automatically implementing every historical idea.

### 8.4 From matches to prediction-method specifications

For each proposed method, eventual transferable specification should include: input constant and physical/data format; permitted pre-cutoff historical outcome view; exact training/scoring windows; no look-ahead at draw N when predicting N; deterministic algorithm for extracting a forecast for the **next** draw; fallback/tie/absence-of-hit handling; parameters and computational cost; validation/null-world tests; output schema/seed and identity provenance; and evidence distinguishing exploratory pattern discovery from demonstrated out-of-sample performance. An observed P3 positional match or arbitrary W→W+1 delta **is not itself an implementable prediction method**.

## 9. Verification, persistence and registry contracts

### 9.1 Latest accepted WSL lean verification policy

1. Normal production-eligible generation: y-cruncher **`-verify:1`**; positive saved validation report for the correct constant/count, completed `Verifying Base Conversion`, `Verifying Decimal Output` stages and positive spot-check. This is useful built-in algorithm evidence, **not independent mathematical proof of every digit**.
2. Linux converter checks every streamed source character, correct decimal-point position and exact digit count, known 32-digit prefix, and exact lemniscate halving. It hashes source text and packed bytes **inline** while creating the packed file.
3. Create-only binary publication with flush/fsync, bounded deterministic **4 KiB persisted readback samples** (normally 12) and create-only JSON receipt recording hash, sample data, file and y-cruncher report provenance. No overwrite. A crash after publication but before receipt leaves an orphan to inspect; do not force-retry over it.
4. After output and receipt publication, **only the owned exact large source text** may be deleted on a completed normal conversion. Failures retain source text; `--keep-text` allows deliberate reference retention. Small logs and verification reports remain.
5. Windows check reads samples and optionally *sampled* legacy-prefix evidence. It cannot prove untouched unsampled bytes. The complete packed scanner computes the entire persisted-file SHA-256 **as part of the existing scan** and compares to the converter-streamed hash; a *prefix-only scan cannot substitute for that full-integrity claim*.
6. Before future production registration, enforce **one sufficient persisted full-file integrity basis** (e.g. a fresh applicable full scan, or an integrated full streamed hash/prefix comparison) without gratuitous duplicate whole-file reads. Version the evidence and ensure it still applies to the exact staged file and state.

**Unverified benchmark exception (owner-approved 7 Nov):** `--benchmark-no-verify` sets `-verify:0` for disposable timing runs, warns in output/log and labels `RUN_CLASS=BENCHMARK_UNVERIFIED`. Such text is **not eligible for packed conversion, verified production, registry/promotion or scientific source claims**. `wsl_convert.py` verification gate remains in place. Comparing verification-OFF and verification-ON whole-run times as if equivalent is invalid.

### 9.2 Future packed G: registry/promotion (NOT IMPLEMENTED)

- Separate **format-aware, versioned packed identity**; bind constant, count, exact packed size, format ID, SHA-256, source/receipt and verification/promotion history. Reject mixed byte and packed declarations and invalid odd-nibble padding.
- Stage create-only under a guarded G: location after the design is reviewed. Test/negative/collision/recovery scenarios on **T:** against dummy registries first; never bind test registry to the live G: tree.
- A 10^10 packed upgrade must compare **every first 10^9 logical digit** against the old active numeric-byte file in bounded chunks. This is a *complete semantic cross-format prefix comparison* at every digit offset, not merely 12 samples. Also apply full persisted packed integrity assurance before promotion.
- Define atomic create-only staging and registry commit, fixed identity, orphan recovery, cooperative lock/reader interlock, restart and audit. Preserve original byte files by default during initial adoption. Do **not** silently inherit old `delete_superseded = true` or delete any predecessor without explicit new owner retention/backup decision.
- Decide how to expose active data to original scanners versus new packed scanners, whether different sizes co-exist and how the parent project consumes the manifest. Keep G: artifacts out of Git. A 100m rehearsal cannot replace a 10^9 active predecessor.
- Only after an isolated realistic rehearsal, negative testing, review and owner approval may a real G: packed promotion occur.

### 9.3 Resource/safety integrity principles

- Preview by default, explicit scoped `--run` and exact large-run acknowledgement; scrutinise actual command for digits, mode, verification, constant, working tree and disk limits. No accidental interactive y-cruncher menu option `0` (previously triggered an unplanned 10^10 calculation, promptly interrupted).
- One large calculation at a time unless the owner authorises otherwise; do not rely on unknown host memory, CPU affinity, ext4 free space or VHDX growth limits.
- Physical T:, guest ext4 filesystem, WSL OS swap and y-cruncher managed swap have different capacities and behaviours. Deleting ext4 files may not shrink VHDX on host. Avoid `wsl --unregister Debian`, global WSL CPU changes, uncontrolled VHDX compaction, blanket `rm`, permissions/elevation and host-stability experiments.
- Keep full hashes, exact paths, source-count convention, source report, attempt identifiers, command/runs/logs, verified/unverified classification, result files and provenance reproducible. Audit before and after deletions. Do not assume `pgrep` means a process was never running; it is a point-in-time check.

## 10. Generation and benchmarking evidence — through 7 Nov 2026

**All values below are from user-supplied output and handovers, not new assistant-run benchmarks on the host.** Unless specified, phi is the constant; WSL static y-cruncher 0.8.7.9547 with native ext4 on T:. `wall` may be y-cruncher internal elapsed, distinct from shell `real`.

### 10.1 Small verified WSL rehearsals

| Digits incl. integer | Mode / memory | Verification | y-cruncher wall | Observation |
|---:|---|---|---:|---|
| 100,000 | RAM, TD1 | ON | **0.086 s** | PASS |
| 1,000,000 | swap, 256 MiB request, TD1 | ON | **1.727 s** | PASS |
| 10,000,000 | swap, 256 MiB request, TD1 | ON | **6.982 s** | PASS |
| 100,000,000 | swap, 256 MiB request, TD1 | ON | **50.108 s** | PASS; source/reference retained, packed workflow separately PASS |

### 10.2 Measured 300m / 1e9 / 3e9 phi comparison matrix

| N digits | `-M` cap | TD/framework | Requested affinity | Actual working RAM | Logical memory needed | Disk need excl. output (reported) | Verify | y-cruncher wall | Shell real | Classification |
|---:|---:|---|---|---:|---:|---:|---|---:|---:|---|
| 300,000,000 | 1 GiB | 1/none | unspecified | 947 MiB | 1.00 GiB | 1.11 GiB | ON | **151.780 s** | **153.406 s** | PASS |
| 300,000,000 | 8 GiB | 1/none | unspecified | 1.23 GiB | 1.31 GiB | 1.11 GiB | ON | **134.769 s** | **136.356 s** | PASS |
| 300,000,000 | 8 GiB | 4/taskqueue | 0,2,4,6 | 1.24 GiB | 1.31 GiB | 1.11 GiB | ON | **136.334 s** | **137.730 s** | PASS; thread affinity not directly measured |
| 1,000,000,000 | 8 GiB | 4/taskqueue | 0,2,4,6 | **4.17 GiB** | 4.25 GiB | 3.78 GiB | ON | **406.015 s** | **407.965 s** | PASS; thread affinity not directly measured |
| 3,000,000,000 | **12 GiB** | 4/taskqueue | 0,2,4,6 | **10.3 GiB** | 10.3 GiB | **9.82 GiB** | **OFF** | **637.385 s** | **640.195 s** | **Unverified benchmark PASS ONLY** |

At 300m, the 1→8 GiB cap change shortened wall **17.011 s (~11.2%)** for one TD1 comparison, even though 8 GiB was not actually needed. The 8 GiB TD1→TD4 comparison was **1.565 s (~1.16%) slower overall** but had a slightly faster core calculation; one run per condition does not establish a ranking. At 1e9 the 8 GiB cap did not bind. At 3e9 the 12 GiB cap was *not* reached but logical memory 10.3 GiB is greater than an 8 GiB cap; owner **declined an 8 GiB repeat**, choosing I/O investigation instead. Do not redo the rejected comparison without renewed approval.

**Detailed 300m phase times, seconds:**

| Phase | 1 GiB TD1 | 8 GiB TD1 | 8 GiB TD4 |
|---|---:|---:|---:|
| Core phi calculation | 15.326 | 10.665 | 9.441 |
| Base conversion | 74.902 | 65.029 | 64.310 |
| Verify base conversion | 49.970 | 47.920 | 49.364 |
| Write decimal output | 5.220 | 5.123 | 6.487 |
| Verify decimal output | 2.208 | 2.286 | 2.685 |
| `Total Computation Time` as reported (not total wall) | 90.243 | 75.718 | 73.772 |

**1e9 / verified:** core 40.332 s; base conversion **199.919 s**; write decimal 22.030 s; verify base conversion **126.186 s**; verify decimal 8.686 s; reported computation 240.294 s; overall 406.015 s; CPU use reported **16.48% + 0.25% kernel**; spot check good through 750m. Base conversion plus its verification dominated.

**3e9 / unverified only:** core **116.715 s**, processing hex digits 8.398 s, base converting **444.219 s**, decimal writing **54.607 s**, `Total Computation Time` 560.954 s, total wall **637.385 s**, CPU use **24.09% + 0.22% kernel**. Logical disk 9.82 GiB + 2.79 GiB output, largest checkpoint 6.45 GiB; twiddle tables 13.9 MiB, I/O buffers 64 MiB. Spot check good through 2.5e9 and exit 0 **do not turn unverified output into verified digits**. No post-run Linux-OS-swap peak was supplied. Do not claim an improvement over 1e9 without matching verification policy, workload and setup.

Prior **native-Windows** 10^9 approximate generation times from the later owner inventory: phi ~15 s; e ~44 s; pi ~71 s; log2 ~180 s; gamma **~2,447 s (~41 min)**; lemniscate minutes, no exact timing recorded. The earlier 5-Nov historical handover separately records a **62.015 s** internal y-cruncher 10^9 phi generation (single-task configuration). These observations need not represent the same settings or generation run; retain both with provenance, rather than picking one as a universal phi benchmark. None calibrates WSL 10^10/10^11. Gamma may be substantially more expensive; benchmark constants individually. Old `RESOURCE_ESTIMATES.md` illustrative `N ln(N)^2` scaling is **not** an empirical HDD-backed runtime prediction and should not be quoted as one.

### 10.3 Dedicated 1 MiB/seek y-cruncher I/O benchmark — latest completed operation

**Run folder:** `/home/u/outlandish-work/benchio_1m_20261107T120842Z`  
**Tool:** y-cruncher 0.8.7.9547 `benchio`, `-M:12g -TD:4 -PF:taskqueue -minIO:1m -swap:raid0 <dedicated ext4 swap dir>`; `taskset -c 0,2,4,6`; shell captured `run.log`.  
**Classification:** OWNER-REPORTED PASS, exit 0, **not** digit generation. **Reported 48 GiB benchmark swap allocation** is *configuration*, not verified post-run disk consumption.

| Measurement | Reported value |
|---|---:|
| Shell elapsed | **22m11.006s** |
| Sequential write | **61.5 MiB/s** |
| Sequential read | **182 MiB/s** |
| Threshold strided write | **123 MiB/s** |
| Threshold strided read | **123 MiB/s** |
| Overlapped disk/computation ratio | **0.0762008** |
| Benchmark working RAM | 12.0 GiB |
| Benchmark swap size specified | 48.0 GiB |
| Shell user / sys | 2m21.379s / 23.174s |

**Result interpretation:** y-cruncher warned disk bandwidth was **very poor relative to CPU**, with displayed desirable overlapped ratio >2.0 versus observed ~0.0762. It recommended **decreasing Bytes/Seek** because threshold strided read (~123/182 = 0.68 of sequential read) was unusually high compared with its preferred algorithm-selection regime near 1/3. The original ideas to compare **8 and 12 MiB/seek are withdrawn**. A single **256 KiB/seek** comparison is a *possible* later test, not approved nor guaranteed to help. A smaller value can cause more HDD seeks if taken too far.

The **61.5 MiB/s write versus 182 MiB/s read** asymmetry is noteworthy. Strided write apparently exceeding sequential write underscores that benchmark caching/patterns may affect the numbers. Potential causes include physical HDD/other load, ext4 allocation, WSL2 dynamic VHDX, cache/writeback, competing disk activity or benchmark specifics; **none has been identified**. These are software-benchmark figures, not direct proof of raw drive performance. A repeated 22-minute `benchio` has real time and 48 GiB logical-storage cost; do not serially test small tuning increments without clear diagnostic value.

### 10.4 Work directories and cleanup provenance

Owner confirmed deletion of three early tiny-test folders `/home/u/outlandish-test/phi_100k_ram`, `phi_1m_swap`, `phi_10m_swap`; retain `/home/u/outlandish-test/phi_100m_swap` (~96 MiB initial report) and T: `rehearsal_artifacts` (~48 MiB initial report).

The following four benchmark directories had their **large decimal text removed by targeted, confirmed `rm -i`**; owner reported `du -sh` ~48 KiB each at that checkpoint, with small reports/logs retained:

```text
/home/u/outlandish-work/phi_300000000_20261107T102056Z_12274
/home/u/outlandish-work/phi_300000000_20261107T102748Z_22348
/home/u/outlandish-work/phi_300000000_20261107T104001Z_8098
/home/u/outlandish-work/phi_1000000000_20261107T105358Z_9352
```

3e9 unverified benchmark directory: `/home/u/outlandish-work/phi_3000000000_20261107T112633Z_3791`; saved y-cruncher report `Golden Ratio - 20261107-220713.txt`, expected `run.log`. Owner confirmed removal of the **3e9 decimal text** using `rm -i`; post-deletion contents/swap state were **not re-listed**. No blanket deletion is justified. Its 3e9 output is not a scientifically verified/packed reference.

At an earlier checkpoint, Debian `df -h /` showed ~1007G capacity / **780M used** / **955G available** (rounded), before the latest benchmark. **Current physical `ext4.vhdx` size, 3e9 swap remainder, `benchio` scratch remainder and host T: free have not been re-inspected after the 22-minute benchio.** Deletion inside ext4 restores guest free space, but host VHDX need not shrink at once.

### 10.5 Immediate safe read-only checkpoint — NOT YET DONE

In Debian, from the owner's own environment, the previous chat requested this **read-only** inventory; it does not start y-cruncher or delete data:

```bash
pgrep -af y-cruncher
BENCH="$HOME/outlandish-work/benchio_1m_20261107T120842Z"
du -sh "$BENCH" "$BENCH/swap" 2>/dev/null
df -h /
ls -lah "$BENCH" "$BENCH/swap"
```

Interpret the results first. If any y-cruncher is active, **do not delete**. Later specific cleanup, if justified, must retain `run.log` and other small evidence and must be narrow enough to avoid the y-cruncher executable, retained 100m reference, Windows T: rehearsal data, Debian VHDX or G: registry. This handover **does not pre-authorise deletion**.

## 11. Outstanding 10^10 / 10^11 feasibility investigation (not a blank cheque)

**Objective:** Finish *proportionate* generation optimisation, not indefinitely tune HDD benchmarks. We need safe, credible per-constant 10^10 production settings, then assess 10^11 feasibility including final, source and scratch storage. Resolve the largest bottlenecks with as few expensive experiments as possible.

1. **Finish the read-only scratch audit** in §10.5. Preserve logs/reports, then decide on narrowly specified cleanup if needed.
2. **Inspect write-path bottleneck with cheap read-only measurements first:** host T: competing I/O, remaining drive/VM free, process/thread affinity and observed WSL swapping; compare native-drive condition and ext4/VHDX effects only with separately approved, bounded tests. Avoid inferring "HDD is broken" or "WSL is slow" from `benchio` alone. A 256 KiB/seek comparison remains optional, owner-approved per run if information value merits 22+ minutes.
3. **Preflight each of six constants** for 10^10: y-cruncher mode/working memory, scratch+text requirement, likely phase costs, number of threads, disk capacity/host pressure. Use **safe preview** only first; note a generator wrapper preview does not query y-cruncher's true estimator. Avoid interactive menu mistakes. Do not extrapolate all constants from φ. If necessary use one or two **bounded calibration** calculations, not a full 10^10 accidental run.
4. **Make an explicit owner go/no-go decision** on a conservative production 10^10 setting (currently WSL memory unchanged, up to 12 GiB y-cruncher, max 4 physical cores, verified output ON, native ext4 scratch), including verification and capacity. A long calculation is a new explicit authorisation, not implied by this document.
5. **End-to-end 10^10 production** one constant at a time: verified generation → packed conversion → Windows samples → complete packed scan/full persisted hash where scientifically useful → guarded G: staging/registry when ready; ensure 10^9 exact cross-format prefix and retention before replacing anything. Keep unverified data clearly separate.
6. **Then analyse 10^11 feasibility** per constant from realistic algorithm-specific resource estimators and calibrated disk-backed workloads; report optimistic/central/pessimistic ranges only where justified. Explicitly check WSL ext4 capacity (~1 TB) versus potential large scratch, 100 GB source text, 50 GB per-constant packed output, retained files, host T: physical headroom, G: capacity, disk write rates, machine stability and the lemniscate pure-Python halving cost. Decide *whether* and *which* 10^11 runs are owner-acceptable. No 10^11 execution by implication.

If, after a few targeted checks, the HDD clearly dominates and no realistic tuning yields an acceptable 10^10 throughput, revisit the practical architecture/storage allocation with the owner rather than continue low-information iterative benchmarking. No requirement to build a custom arbitrary-precision engine: prior research produced a conditional NO-GO for that route due to engineering complexity and uncertain scaling on 32 GiB RAM.

## 12. Forward design for packed-data production and matching

This is a **future work programme**, not an implementation request today.

- Validate an integrated packed-format registry and guarded G: path with *small isolated dummy artifacts on T:*. Preserve the native-Windows verified 10^9 originals until explicit retention/prefix/reader decisions. Consider binary size, G: free space, create-only promotion, audit and crash recovery.
- Reuse the already successful WSL packed scan as the production reader where possible. Avoid rewriting the functioning scanner merely to adopt the new documentation structure. Test full-file hashing, exact counts and chunk boundaries at larger depths. The original Windows v0.2r4 registry and scanner remain useful **reference implementations** but are not compatible with packed files as-is.
- Conduct the **deferred matching-extension design** later and separately: existing P1/P2/P3 remain unchanged; decide Powerball extra order classes and Oz Lotto O1/O2/O3 exact semantics; define independent variant labels and null-world comparisons; test small fabricated inputs and compare original real results. Match-count expansions from any-order conditions are expected; do not mislabel them improved prediction.
- Define **actual forecast algorithms** (for parent consideration) only after the owner chooses scientific candidates and the permitted data-view and N−1 contract is clear. A method can use one constant or a deliberately declared combination, may have variants and may ultimately be ranked poor; that does not mandate its deletion from the parent catalogue.

## 13. Planned parent-project handover and ongoing dialogue

**Destination:** `https://github.com/hydra3333/analysing_perceived_randomness_in_reality`. The parent project's Claude primary designer/coder and ChatGPT independent reviewer are separate from the OUTLANDISH research chat. Preserve independent owner approvals and the parent's protection of holdout, prediction identity, method ranking/ensemble and evaluation policy. OUTLANDISH is currently an independent side experiment despite living in the same repository tree.

**Deliverable set at handback:**

1. **Code snapshot and provenance:** exact source files/versions for Linux generation, conversion, packed format, Windows sampled/full scanner, legacy reference, tests, safe launchers and environment/runtime requirements. Include code-tree manifest and hashes. No unnecessary project-wide fork or dependency reinstalls.
2. **Data manifest and transfer instructions:** per-constant format ID, digit count including integer, leading-digit convention, exact byte count, SHA-256, verification status, packed/legacy distinction, generation command/report, conversion receipt, full persisted digest evidence, prefix comparison and permitted data paths. Binaries will be **5 GB each at 10^10 / 50 GB at 10^11**: keep outside normal Git; design a practical same-host path/volume arrangement or other approved transfer, not a 300 GB Git commit.
3. **Scientific methods and tests:** category/version definitions, pre-holdout isolation, match-offset conventions, draw-order semantics, deduplication, W→W+1 positional output, example reports, null/chance baselines, cross-format test vectors and any actual deterministic next-draw forecast algorithms separately specified. Explicitly distinguish *historical matches* from *validated prediction methods*.
4. **Integration specification:** planned read-only digit access API, streaming/random access and data-view assumptions, performance estimates, how to keep games separate, N−1 isolation, fallback when no historical hit exists, logging and method ranking constraints for discussion with the parent designer/reviewer.
5. **Two-way dialogue:** The owner relays self-contained numbered/versioned questions and responses between this chat (or successor) and parent Claude/ChatGPT. Maintain a small question/decision/issues log; resolve ambiguities with source snippets and tests. Changes to parent governance/method admission occur only through its approved process.
6. **Reproducibility and caveats:** exact measured results, failed attempts, tool versions, disk environment and unresolved limitations, plus a list of deferred features not included in the transfer.

This chat's support obligation persists **after** the initial package is handed over; do not declare OUTLANDISH complete solely because a ZIP exists. Actual final acceptance criteria and size/transport will be settled with parent AIs and owner near handback.

## 14. Historical lessons preserved without reviving abandoned work

### 14.1 Native-Windows generation, old resources and privilege obstacle

Earlier native-Windows y-cruncher could produce and register six 10^9 legacy `.bin` streams. Some higher-concurrency activity caused sudden power-offs, motivating a cautious four-physical-core maximum for the Linux programme. At ~10^10 digits RAM-only φ estimator indicated ~**41.0 GiB**, beyond host RAM comfort; WSL interactive swap estimator once showed **14.1 GiB** memory and **37 GiB logical swap + 17 GiB output**, but an attempt to enter a 4 GB memory limit displayed **79.7 MiB**, not the intended setting, and the accidental large job was interrupted. Do not interpret that as measured 10^10 performance or reliable `-M:4g` tuning. For fixed-size workloads, actual working memory may be much less than cap; compare real values, not command labels.

Native-Windows y-cruncher external-memory mode encountered the need for `SeManageVolumePrivilege` to use `SetFileValidData()`. A grant to the everyday user would be security-sensitive and broad; owner chose not to elevate/reconfigure the main PC. Debian/WSL2 Linux y-cruncher avoids that particular Windows privilege route, but its ext4 VHDX and HDD I/O impose different constraints.

Alternative arithmetic research examined FLINT/Arb, python-flint, GMP, apfloat, external-memory FFT, TachusPI, etc. The outcome was to **prefer the established y-cruncher** unless a demonstrably straightforward and realistically scalable independent external-memory solution is found on 32 GiB; no one should restart a major numerical library project casually. A digit-output streaming API does not imply the underlying computation uses bounded RAM.

### 14.2 Closed Windows Sandbox diversion

The Windows Sandbox experiment tested isolation with host T: copied source and mapped data, and hoped to exercise a small y-cruncher calculation. The path is **closed**, not a current fallback.

- Early guest ephemeral-C: Python installation was extraordinarily slow; after subsequent pip work `python.exe` appeared **0 bytes**, with Windows `ERROR_FILE_INVALID` `0x800703EE`. Root cause was **not proven**, and this is not evidence of host T:/G: disk corruption.
- Installing **Python 3.15.2 persistently on mapped T:** succeeded, including `pip`, NumPy 2.5.4 and subsequent fresh Sandbox `VERIFY` checks. This positive result did not cure y-cruncher.
- Full dependency BAT attempted excess packages; five distinct packages requiring compiled wheels/toolchain (PyYAML, inflate64, pybcj, pyppmd, pyahocorasick) had six failed builds with missing MSVC C++ 14+ compiler. A large Build Tools setup reached 35% then was abandoned. These are not proven requirements for the OUTLANDISH smoke test, nor proof of a VC++ runtime problem.
- Initial missing launcher files caused one test failure; after the missing `.cmd` launchers were copied, the synthetic smoke suite reached **24 pass, 1 allowed symlink skip**. This tested Python/package wiring, not numerical generation.
- The actual guest y-cruncher invocation returned **0xC000007B (`STATUS_INVALID_IMAGE_FORMAT`)** on process startup. Its precise missing/malformed module was never identified; direct executable launch also failed. No digits were generated in Sandbox. The attempted VC++ redist installation was not conclusively verified as successful.
- Separate issues with VBScript shortcut creation (`cscript` unavailable script engine), Notepad++/Explorer preferences and path-audit overbreadth were resolved or diagnostic only. Windows power-management Event 55 was informational, not a confirmed disk error. Owner abandoned Sandbox rather than spend more effort.

**Do not** recreate guest configuration, full Python compiler installs, `.wsb` files, copied TOML, transient C: artifacts or host-map deletion procedures in the current WSL workstream. Keep old v1/v2/v3 handovers and nested evidence for forensic provenance only.

### 14.3 Why not a RAM disk or full rewrite?

At 10^10/10^11, scratch estimates may reach many tens to hundreds of GB. A `tmpfs` cache competes with the existing ~15.6 GiB WSL memory that y-cruncher needs; Linux OS swapping to HDD could be catastrophic. The working Linux + packed pipeline has already passed real tests, so the near-term return lies in *measured I/O/working-memory configuration and reliable production packaging*, not rebuilding algorithms or duplicating whole-file verification. The first `benchio` already suggests disk throughput dominates sufficiently large problems.

## 15. Document/source genealogy, conflict handling and archival requirements

### 15.1 Two owner-provided archives inspected for this draft

- `OUTLANDISH_WSL.zip` — SHA-256 `0073cf1df3399d44186290a28f8f61b1cd3a32c69bbd172022b9d31564d62f87`; contains **15** WSL files, including v5 main handover, addendum revision 0.5, scripts, tests and operational/reference docs.
- `OUTLANDISH_01_indicative_original.zip` — SHA-256 `b6ce855f9a16f1a5999d4826ed4e3f49cc48af1106b08e980ef43c3b23da429b`; contains **21** predecessor files including native-Windows code/TOML/CSV, early v1–v3 handovers, original scope and deferred order-matching proposal, plus nested historical source/evidence ZIP. **Indicative, not a replacement for live G:/E: code**.
- The earlier separately uploaded v5 and living-addendum v0.5 copies match the corresponding WSL ZIP members byte-for-byte, as assessed in the preceding chat.

The original standalone handover and nested evidence ZIP remain valuable for exact π/φ 10^9 results and early method definitions. `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md` should remain a separately stored **deferred source record** and not be dissolved into a vague future-work bullet. The original `0_outlandish_thought_experiment_01_scope.txt` should remain a preserved genesis document. The 6-constant TOML, backup and lock file in the predecessor archive are local machine-state snapshots, **not portable mutable registry templates**; avoid distributing their mutable state uncritically.

### 15.2 Superseded or contradictory statements corrected in this draft

| Previous statement/location | Current interpretation |
|---|---|
| WSL `README.md`: candidate not installed; 100m conversion not yet run | Historical packaging text: owner later installed/tested and completed conversion + scan |
| WSL `RESOURCE_ESTIMATES.md`: old-vs-packed comparison and 100m staging future | Both superseded by owner decision to skip comparison and measured 100m workflow |
| v5 §3A: next step clean 300m/1e9 and preview 1e9 | Done in addendum revs 0.1–0.5; now pending `benchio` scratch audit |
| Addendum earlier idea: compare 8 and 12 MiB/seek | Withdrawn after `benchio` recommended *decreasing* Bytes/Seek |
| Original TOML header: keep it out of Git | Owner later intentionally tracks the local TOML; protect generated state |
| Earlier v3: WSL generation/conversion not yet implemented | Implemented/tested on 100m; original v3 retained only as architecture/history |
| Old Windows project: `src/GAIS/` current path | Moved to `GAIS/` after repo relocation; old paths historical |
| Early format: all `.bin` are numeric-byte per digit | Legacy format remains; new `.packed.bin` is BCD high-first and incompatible |
| Source `README_Benchmark_Verification_v0_2r3`: owner installation pending | Owner later installed and completed an explicit 3e9 unverified benchmark |
| Old original scanner is P1/P2/P3 and "any-order" addition | P3 already any-order; only new P1/P2 variants and P3 relative-order subsets are deferred |
| Historical old `-verify:0` Windows setting | Current WSL **production-eligible** generation requires `-verify:1`; benchmark-only waiver distinct |
| Old 1e9 π scan report 27.598385 vs later v5 27.278917 s | Preserve both as separate reported observations; compare exact run evidence before asserting contradiction |

### 15.3 Archive and reconciliation controls (for owner approval)

- **Keep existing originals unchanged**: v5, living addendum v0.5, early v1/v2/v3, 5-Nov handover, historical nested ZIP, genesis scope, deferred matching proposal and historical change records.
- If ratified, make v6 the **single primary handover** and a **fresh, empty living addendum revision 0.1**, pointing at v6, with sections for measured findings, owner decisions, source/test changes, unresolved questions and update log. The new addendum has **no fabricated test entries**. Do not overwrite/add to the old v0.5 document and pretend it is blank.
- Keep up-to-date operational user instructions in the WSL and legacy READMEs as a **later, light, separately reviewed documentation task**, not an urgent rewrite or source refactor. Preserve historical `CHANGES` records as they were. The new handover explicitly calls out stale passages meanwhile.
- Before next consolidation, reconcile every new addendum fact into the correct subject section, retain a dated decision/benchmark ledger and verify no owner decisions, exact run paths or non-success findings were dropped. Version the whole document and retain past baselines.
- No Git changes, local production file mutation, live registry action or tests were performed to prepare this draft. It is a documentation artifact based on uploaded snapshots and cited historical owner evidence.

## 16. Open questions, risks and explicit owner approvals still required

| Issue | Current state / boundary | When to resolve |
|---|---|---|
| Latest `benchio` 48 GiB scratch leftovers | **Unknown** until read-only `du/ls/df` | **Next immediate operation** |
| Actual y-cruncher per-worker CPU affinity | Not independently measured | During next approved bounded run; no more than four physical cores |
| Why sequential writes ~61.5 MiB/s | Unknown; possible caching/VHDX/HDD/competition effects | Before expensive repetition; low-cost diagnostics first |
| Best Bytes/Seek | 1 MiB tested; tool recommends smaller, 256 KiB *candidate only* | Only if additional controlled comparison is worth cost |
| Truly useful per-constant 10^10 `-M` and disk budget | Not established by phi alone; current WSL cap ~12 GiB | Preflight/owner explicit 10^10 launch decision |
| 10^11 per-constant resources/feasibility | Unknown; G:/T:/ext4 headroom and gamma/lemniscate cost matter | Following representative production/calibration evidence |
| Packed G: registry and retention of legacy six | Design/testing and owner signoff outstanding | Before any G: promotion/deletion |
| Full persisted integrity before packed promotion | Samples alone insufficient | Registry specification and end-to-end qualifying rehearsal |
| Exact Oz Lotto O2/O3 and order variants | Unsettled | Later science design, not benchmark phase |
| Value and definitions of compact/alternative encodings | Speculative historical idea | Later owner-selected experimental method work |
| Forecast mechanism from matched positions | No validated deterministic rule yet | Before presenting any method as a predictor to parent |
| Parent integration contracts, storage sharing and review schedule | Parent project still undergoing coordinated implementation | Near handback, through Claude and ChatGPT reviewers |

## 17. Recommended next-work sequence — PROPOSAL, NOT RATIFIED

**Phase A — Documentation continuity (now, no code):** Review this complete candidate v6 for omissions/incorrect emphasis. After owner acceptance, freeze earlier handovers as archives and create a **new blank incremental addendum**. Do not rework functioning scripts merely to align READMEs.

**Phase B — Finish lean, targeted tuning and define safe 10^10 budget:** (i) read-only `benchio` scratch inventory, (ii) preserve log and deliberate narrow cleanup if needed, (iii) investigate low write throughput and actual CPU affinity with cheap observations, (iv) do **only** a small number of owner-approved high-information calibration tests, (v) record per-constant 10^10 and indicative 10^11 budgets. Abandon repetitive benchmarking once conclusions are actionable.

**Phase C — Complete necessary packed-production integration without redevelopment:** Define/test the *smallest* safe format-aware packed G: staging/registry/whole-prefix contract and retention policy; keep G: originals unchanged pending owner approval. Reuse working generator, converter and scanner. Benchmark conversion costs (especially lemniscate) only where they materially affect planning.

**Phase D — Generate and validate six 10^10 packed files, one at a time:** Owner approvals for each storage/computation step, verified output ON, receipts and full persisted integrity, complete legacy-prefix equality, controlled G: handling. Keep small reports and reproducibility metadata; avoid unnecessary duplicate data passes.

**Phase E — Matching, reports and 10^11 decision:** Run existing matching/reporting on generated streams; analyse useful positional evidence with chance baselines. Finalise defensible **10^11 feasibility** per constant and seek owner go/no-go. Separately resolve and implement only approved additional order variants and Oz Lotto requirements, preserving historical baselines.

**Phase F — Parent-project methods, delivery and ongoing support:** Prepare tested input-data/code/method package, external large-binary transfer plan, exact interfaces, validation and provenance. Discuss with parent Claude/ChatGPT under the owner's relay and change-control workflow. Continue answering technical questions and revising handback definitions until integration is accepted.

**Sequencing flexibility:** B and document review of original scientific requirements may overlap. A minimum packed-registry integration may need to precede G: production promotion; some verified 10^10 generation could be staged on T: before final registry completion **only if its long-lived storage/verification and recovery are explicitly reviewed first**. Avoid creating 60+ GB of intermediate data without an agreed survival and transfer route. The order is a rational proposal, not permission to launch.

## 18. First response expected of successor chat and status checklist

A receiving chat should acknowledge, without inventing live verification:

1. Six-source goal (10^10), feasibility question (10^11), scientific matching/position work and eventual parent integration with ongoing dialogue.
2. Current accepted WSL2+BCD approach, six existing G: legacy active files, one successful 100m φ full packed pipeline, owner-approved verification policy and **no packed G: registry yet**.
3. Last benchmark: **22m11s `benchio`, 1 MiB/seek, 12 GiB, four-task, 48 GiB configured scratch, 61.5/182 MiB/s sequential write/read, 0.0762 ratio**; smaller Bytes/Seek only a proposed experiment.
4. Binding safety: no more than four physical cores, WSL memory unchanged, y-cruncher <=about 12 GiB current tests, verify-on for production, unverified test data never promoted, no unapproved large run, G: legacy untouched.
5. **Immediate operation**: request results of §10.5 read-only `pgrep`, `du`, `df`, `ls` if not supplied; do not propose cleanup until evidence is known.
6. Historical matching semantics P1/P2 drawn order, P3 any six unordered + PB; W→W+1 transition report P1-anchored; deferred Powerball order expansion and Oz Lotto O1/O2/O3 unresolved.
7. State clearly that no assistant executed commands on the owner's machine, and no 10^10 or 10^11 file currently exists based on the supplied evidence.

---

## Appendix A. Evidence identifiers and reproducibility details

**WSL operational result identifiers**

- Retained 100m input/report: `/home/u/outlandish-test/phi_100m_swap/Golden Ratio - Dec - Newton.txt`, `Golden Ratio - 20261107-172852.txt`.
- 100m packed stage/digest: see §7.5; report `packed_run_20261107T094409Z_c89da00e`.
- 300m A: `phi_300000000_20261107T102056Z_12274`.
- 300m B: `phi_300000000_20261107T102748Z_22348`.
- 300m C: `phi_300000000_20261107T104001Z_8098`.
- 1e9: `phi_1000000000_20261107T105358Z_9352`, saved validation report `Golden Ratio - 20261107-213045.txt`.
- 3e9 unverified: `phi_3000000000_20261107T112633Z_3791`, saved report `Golden Ratio - 20261107-220713.txt` (report file existence after text cleanup not re-listed).
- `benchio` 1 MiB: `/home/u/outlandish-work/benchio_1m_20261107T120842Z/run.log`; scratch audit outstanding.

**Historical native-Windows output identifiers**

- Nested historical bundle includes `evidence/actual_1e9_powerball_results/run_20261105_231343.zip` with compact results and earlier two-constant facts; archive `OUTLANDISH_01_2026-11-05_Historical_Source_and_Evidence_Bundle_v0_1.zip` should remain intact.
- Six active legacy file names in the provided TOML: `digits_pi_10_to_9.bin`, `digits_golden_ratio_10_to_9.bin`, `digits_e_10_to_9.bin`, `digits_log2_10_to_9.bin`, `digits_gamma_10_to_9.bin`, `digits_lemniscate_10_to_9.bin` under `G:\OUTLANDISH_01\large_artifacts\digits\`. Exact hashes are contained in original TOML; always verify against **live** state before acting.
- Supplied pre-holdout Powerball CSV SHA-256 (original ZIP member, not live master): `ce0ae7e77e09e5a93389eb98191b455926ec44c0bb38dda0ef721b9f710d66b8`.

**Source files that remain primary references**

- Latest archived handover v5; full living addendum rev 0.5; `OUTLANDISH_WSL/README.md`, `RESOURCE_ESTIMATES.md`, `CHANGES_v0_2.md`, `README_Benchmark_Verification_v0_2r3.md`.
- Original `0_outlandish_thought_experiment_01_scope.txt`, `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md`, its historical evidence ZIP, original `README.md`, native-Windows v0.2r4 source/tests/TOML snapshot, and `OUTLANDISH_01_Deferred_Powerball_OzLotto_Order_Matching_v0_1.md`.
- v1/v2/v3 historical handovers and Windows Sandbox diagnostics, retained for detailed forensic source information; this v6 summarises principal technical lessons without reissuing retired Sandbox procedures.

## Appendix B. Future living-addendum template (create **only after** owner approves v6)

Proposed new file: `OUTLANDISH_01_Living_Handover_Addendum.md`, **new internal revision 0.1**, links v6, starts empty of findings. It should contain:

1. **Current delta since ratified v6** — none at creation.
2. **Owner decisions since v6** — initially none.
3. **Measured runs / evidence / resources since v6** — initially none.
4. **Code/docs changes since v6** — initially none.
5. **Open questions, pending authorisations and next action** — inherit identifiers from v6 rather than copying the entire handover.
6. **Dated change log** — first row "created fresh addendum after v6 acceptance" (not a new benchmark).

Never replace historical v0.5 without preserving it separately. At the next consolidation, fold every material delta into the next self-contained main handover and reset the addendum again.

---

**End of OUTLANDISH_01 v6 DRAFT — candidate for owner review; no operational authorisation.**
