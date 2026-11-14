# OUTLANDISH_01 — operational handover v0.8

**Checkpoint:** 14 November 2026, Australia/Adelaide, following completion of the six 10^10-digit source datasets.  
**Purpose:** current, concise operating state and safe restart route.  
**Document status:** ChatGPT-prepared operational update requested by the owner; it records already established decisions and owner-supplied evidence. It does **not** amend or re-ratify the scientific rules, grant permission for Q5 production scans, or claim changes are already committed.  
**Suggested repository location:** `GAIS/OUTLANDISH_01/OUTLANDISH_01_Operational_Handover_2026-11-14_v0_8.md`.

## 1. First-read status — current, overriding older production snapshots

**SIX OF SIX COMPLETED.** All six named constants are stored on the Ryzen 3900X at `G:\OUTLANDISH_01\large_artifacts\digits\` as 5,000,000,000-byte **high-nibble-first packed BCD** binaries, each paired with a `.wsl-receipt.json` conversion record. Each represents 10,000,000,000 logical decimal digits **including the integer digit**. The owner reported whole-file SHA-256 verification on the destination Ryzen. Earlier documents' “four of six”, “five of six”, “gamma not started”, and “lemniscate not started” refer to historical snapshots and are **superseded only for operational status**.

| Constant ID | Packed binary basename (under `digits\`) | Destination SHA-256, owner-reported |
|---|---|---|
| `pi` | `digits_pi_10_to_10.packed.bin` | `62ab5b9a511eb0fcf5d09717df9ee51f8bd29ea09acf379e6f1045c537ababe2` |
| `phi` | `digits_golden_ratio_10_to_10.packed.bin` | `dd80be0c3fdb330fe4e1780c2d53bf03bde297a5dea83b5785cd3349838ad36d` |
| `e` | `digits_e_10_to_10.packed.bin` | `522f088b013432f775098df863b851ad87a4f5d0f0296b54cb00d6f13f72720f` |
| `log2` | `digits_log2_10_to_10.packed.bin` | `6993b8b6c6f46ae13b5e213aae0d46e784c8acae510f10e6862aecde83a15694` |
| `gamma` | `digits_gamma_10_to_10.packed.bin` | `68e4a47d27759632dd8c608af973fa5bd22fb2aa7290d5e92f59e485ceb85e6a` |
| `lemniscate` | `digits_lemniscate_10_to_10.packed.bin` | `958210dcda823fd1951b8487fbfe3cb98aeda9748c2b0dea4db9684608d21369` |

**Status precision:** These are six verified production *inputs*, not six scientifically qualified REAL matching scans; no finding about lottery predictability follows. `-verify:1` and the converter validation are production checks, not independent mathematical recomputation of all 10 billion digits. File sizes and receipt/hash comparisons were reported from the owner's actual PCs; ChatGPT did not open the 5-GB local files remotely.

### Sixth-constant completion evidence — important distinctive details

- Native Windows 10 on i5-4670, 16 GiB physical RAM, elevated y-cruncher v0.8.7.9547b, `-TD:4 -PF:taskqueue -M:12g -mode:swap -verify:1`, scratch on i5 **T: HDD** and decimal output on i5 **G: HDD**, with **no E: drive on the i5**. The `SeLockMemoryPrivilege` warning was nonfatal.
- Lemniscate start **14 Nov 11:01:07** and end **15:12:18** Adelaide. Calculation wall time 15,070.446 seconds; y-cruncher reported completed base-conversion and decimal-output verifications, `Spot Check: Good through 7,500,000,000`; validation report `Lemniscate - 20261114-151223.txt`.
- Decimal source `Lemniscate - Dec - Zuniga (2023-x).txt`, **10,000,000,001 bytes**, is **full lemniscate perimeter** near 5.244115, *not* our target. Existing tested `wsl_convert.py` stream-divides by exactly two to produce the **half-perimeter**, before packing. Preserve this identity distinction in all future scientific interpretations.
- Native converter receipt: format `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, `digits_including_integer=10000000000`, `packed_bytes=5000000000`, streamed/source validation and sampled readback, source text SHA `93f36cd1ef2d89816d29adcd1865239c9c29a2b67f5038b044a20befc91bae92`, report SHA `0c9dd99f3d7850cccc7cbf5cea40e8d2c6d753929bb327166f8189a9df71a682`, packed SHA as above, output verification true. Converter wall 1,125.746 seconds.
- Ryzen's `certutil -hashfile ... SHA256` matched the converter's streamed binary digest **exactly**. First 16 BCD bytes decoded `26220575542921198104648395898911`, consistent with half-perimeter 2.6220575542921198104648395898911… and **not** full-perimeter 5.244…. This is a useful prefix sanity check, not a substitute for full independent arithmetic recomputation.
- Five other packed files had been transferred and SHA-verified earlier, including gamma. The `wsl-receipt` suffix is a historic converter name and does **not** mean every file was calculated under WSL.

## 2. Machines, code locations and boundaries

- **Ryzen 3900X:** Windows 11; VS Code and Git checkout at `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`; verified 5-GB packed files on Ryzen G:. The existing project venv is Python 3.15.2 with NumPy 2.5.4 / SciPy 1.18.1. The 39-package venv installer v8 ran with `COMPUTERNAME=3900X`, source builds permitted, all 39 installed and `pip check` passed; program-level project tests still needed. Earlier unexpected Ryzen power-offs make long unattended full-scale runs a reliability risk (root cause not proven).
- **i5-4670:** Windows 10; verified stable 16 GiB Patriot RAM, native Python 3.15.2; project working copies `G:\OUTLANDISH_01`, tool at `G:\OUTLANDISH_01\tools\y-cruncher v0.8.7.9547b`, converter at `G:\OUTLANDISH_01\scripts\OUTLANDISH_NATIVE_WIN_v0_1\wsl_convert.py`; scratch T: HDD. **No E: drive.** Do not require VS Code, Visual Studio IDE or MSVC builds for routine i5 scientific processing. Prefer prebuilt Python wheels on that host.
- **Git/authority:** `GAIS/OUTLANDISH_01/` is the scientific and operational source-document authority. `OUTLANDISH_WSL/` retains generator/packed-reader history. No `.bin`, raw digit text, scratch, or full results in Git. `POWERBALL_preholdout_only.csv` is the isolated approved historical Powerball drawset. Older code/scripts are historical, not automatically the new ratified matcher.
- **Delegation:** ChatGPT may make ordinary correctness/test/software/interface choices, use independent review when useful, and maintain one living decisions/progress document. Scientific hypotheses/ratified-rule changes, restricted data boundaries, costly scientific campaigns and data deletion require owner-level decision. Code and large runs execute on the user's machines, not in ChatGPT.

## 3. Binding scientific design and current phase

**Ratified source:** `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md` (owner ratified 9 November 2026; the file's internal historical “proposed” language is not the current owner decision). Preserve bytes/content, do not quietly rewrite it. **Forecasting:** `OUTLANDISH_01_PostMatch_Adaptive_Forecasting_Proposed_Spec_v0_1_FOR_OWNER_REVIEW-2026.11.10.md` remains **NOT RATIFIED, PARKED** pending post-Q1–Q5 owner review and approval; don't implement forecasting now. The already-agreed early **interface compatibility review** for future forecast event consumers belongs after initial Q1/Q2 and *before substantial Q3 construction*, without implementing the parked pilots.

**Matcher contract highlights:** One common packed reader, one REAL scan per `(constant, game, drawset version)`, all logical digit starts including odd offsets and per-family EOF. Original Powerball baseline P1/P2/P3, Oz O1/O2/O3, five discriminated canonical families `K7`, `K7S`, `K6S`, `K6`, `K7mix`; preserve actual operator-drawn order and role constraints. PB may equal a main; Oz's three supplements are distinct from mains. Preserve same-start and shifted overlap and multiple draw attributions, leading-zero `matched_digits` as text. REAL event schema EXACTLY `draw_number,family,start_digit_offset,matched_digits`; manifest carries game/constant/drawset/digests. Separate REAL/NULL input indexes and output roots, distinct receipt verification and complete input-file hash. Do not merge games, data eras or decoys.

**Powerball firewall:** `1144..1576`, 433 draws, exclusive cutoff `1577`, from `GAIS/OUTLANDISH_01/POWERBALL_preholdout_only.csv` (drawn-order columns). No reading parent master/future outcomes for matching qualification. Oz modern 7+3 configuration only, with its own preapproved isolated set and independent holdout; check the actual established effective boundary at integration, do not guess it.

**Q1–Q5 (now allowed to start as development/qualification work, not automatic production run permission):**

1. **Q1** saved 100m/1e9/10e9 `phi` P3 CSV exact-row reconciliation, first without a re-scan. Old counts 3/25 and unqualified packed-10e9 count 227. Compare `(draw_number, baseline_category, start_digit_offset_0_based, matched_decimal_digits)` and derived `start+length<=prefix`. Preserve old evidence.
2. **Q2** independent simple Python oracle, planted known-hit fixtures and deliberate mutations against *unchanged* existing scanner, output outside production REAL results. Test odd/even starts, PB/main equality, proper seventh-field role, EOF, overlaps, leading zeroes, chunk ownership, corrupt/padded inputs, and multiple draw IDs. Negative findings stay documented.
3. **Q3** minimal shared production engine; Powerball baseline oracle equivalence first, Oz after validation. Early compatibility review for parked forecasting event readers **before significant Q3 implementation**, no forecasting logic.
4. **Q4** REAL/NULL firewall and reporting/receipt/hash tests; W→W+1 signed min-gap tie `(abs(b-a), b-a, a, b)`, full draw-label permutation including zero-match draws, 10,000 permutations, within-game Holm over six constants. Primary P3-any/O3-any statistic remains **owner-vetoable before qualified REAL runs**.
5. **Q5** after Q1–Q4 PASS and owner ratifies final implementation: new create-only REAL scans of six constants for Powerball, Oz independently when its validated source is available. No implicit parent-project method registration or use of held-out draws.

Current desk-reconciliation finding: repository 1e9 numeric-byte φ matches CSV has 25 P3 rows and **three** within the first 100 million, at `(draw, offset)` `(1244,20048101)`, `(1274,71806090)`, `(1373,95105831)`, consistent with the known 100m rehearsal. **The packed-10e9 CSV comparison is still OPEN.** This is partial evidence, not a qualified scientific result.

## 4. Legacy 10^9 cleanup: never make the registry lie

The Ryzen G: directory still contains six `digits_*_10_to_9.bin` files, each **1,000,000,000 bytes** of *numeric-byte-per-digit* data plus six packed files/receipts. Current GitHub `outlandish.local.toml` has `[state.active.pi/phi/e/log2/gamma/lemniscate]` pointing to the six **legacy 10^9 byte** files and `digits=1000000000`. This schema/old tools do **not** magically support the new high-first BCD format by renaming or changing digit counts. The repository's tracked file also says “keep it out of Git” in a historical comment; the owner's later tracking decision supersedes that comment, so **do not automatically untrack or delete the file**.

**Cleanup order:** (a) preserve a copy and hashes of this legacy TOML, all earlier event CSVs/results, and old scanner source; (b) finish Q1 or secure independently checked, inspectable fallback binary evidence needed to resolve any discrepancy; (c) run the separate **read-only** legacy inventory/check, check actual active local TOML and no readers are using the old binaries; (d) explicitly retire old *registry state* using a reviewed one-time migration that archives its previous bytes/sha and marks old active entries no longer active **without falsely registering packed files as numeric-byte entries**; (e) only after a verified dry-run and owner assent, delete the specifically named six legacy files, not wildcard bins, preserving small receipts/reports. If no retained fallback exists and Q1 is unresolved, postpone deletion. Never delete the 10e10 `.packed.bin` inputs or receipts, y-cruncher validation evidence or relevant saved `matches.csv`/reports. Do **not** run `outlandish_artifacts.py retire` as-is: it requires a registered compatible successor and compares old/new content, so it is not a drop-in packed-format migration.

**Operational cleanup now:** avoid *new uses* of the legacy registry/scanner; inventory/segregate old outputs logically and archive small evidence. Physical removal and registry mutation are **pending safety preconditions**, not reported completed.

## 5. Data and source retention

Keep unchanged until reviewed: all six final `.packed.bin` and `.wsl-receipt.json`; the y-cruncher verification reports and converter logs/receipts; the original 10e10 phi diagnostic `matches.csv` even though scientifically unqualified; the preholdout CSV; the 100m and 1e9 historical CSV/metadata; previous scanner versions; the i5 lemniscate decimal source and any scratch/checkpoints until cleanup specifically reviewed; existing legacy `outlandish.local.toml` and its hashes. The 1e9 raw binaries are removable **only after** the Q1/residual-risk condition above is met.

**No new generation target:** six 10^10 complete; 10^11 deferred. The speculative scientific goal stands; a surprising match can motivate carefully separated further exploration but must not be reported as forecast evidence without prospective frozen testing.

## 6. Immediate handoff / commands

On **Ryzen**, identify saved 10e10 φ report paths without running any scans:

```bat
where /r "G:\OUTLANDISH_01\large_artifacts" matches.csv
```

For full source and scientific context, read ratified v0.2 Sections A1–A4 and B1–B8, the parked forecasting proposal only as a future interface consumer, and this handover with `OUTLANDISH_01_Living_Decisions_and_Progress.md`. Run the companion `OUTLANDISH_01_Q1_Reconcile_Saved_Phi_Events.py` with the saved CSV file paths; it is read-only. Keep all writes to bounded test outputs on E:/scratch or designated G: testing, never production REAL results during qualification.

**Suggested repository action:** install the new operational handover and living record under `GAIS/OUTLANDISH_01/` in a normal source review/commit. Do not replace historical v7/rev0.7, the ratified v0.2, or the unratified forecasting v0.1. Confirm local Git working tree before adding/committing. No repo write or machine cleanup is claimed here.

**Provenance:** inspected GitHub `main` source docs and code paths 14 Nov, together with the owner's 14 Nov command transcripts, exact final directory inventory, receipts and certutil verification. This document intentionally prioritises the newer 14 Nov physical-file evidence over older 9 Nov status snapshots without changing their historical content.
