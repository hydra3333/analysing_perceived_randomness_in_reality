# OUTLANDISH_01 — Q4 published-source / profile / run-root validation v0.1

**15 November 2026 — implementation slice for synthetic qualification.**

Authority: `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md`, especially B3–B4 and Q4, and `OUTLANDISH_01_Living_Decisions_and_Progress.md` §13. These files do **not** amend the ratified rules. This slice follows Q1/Q2 PASS, Q3 synthetic PASS, and Q4 fixture guards PASS (4 runs, 53 refusals, 51 regression comparisons).

## Files in this archive

- `OUTLANDISH_01_Q4_Published_Source_Guards_v0_1.py` — small read-only validators for the eventual REAL adapter; **does not run a scanner or publish a manifest**.
- `OUTLANDISH_01_Q4_Published_Source_Qualification_v0_1.py` — artificial receipt/BCD/history/run-root test harness, using its own marked `TemporaryDirectory` only.
- This README.

No changes to existing source files, project dependencies, published binaries/receipts, previous results, historical evidence, parent-game master files, or overarching project working files.

## Run synthetic-only qualification on the Windows project venv

From the repository root in CMD, install the archive so these three files land under `GAIS\OUTLANDISH_01\`. Run:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4_Published_Source_Qualification_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q4_Published_Source_Qualification_v0_1.py" --run
```

Both run the same complete synthetic adversarial suite. The second flag is an explicit full-qualification label, **not** a REAL production-run command. Expected on PASS:

```
Q4 PUBLISHED-SOURCE ADAPTER SYNTHETIC PASS: refusals=70 real-production-scans=0 real-history-reads=0
```

The author ran the suite under Python 3.13 locally: PASS, 70 refusals. Python files compile successfully. **Owner Windows 3.15 qualification remains pending** until the owner executes these commands and returns the output. The tests do not attempt to read G: or any genuine lottery history/packed input. `installed_history_profile('powerball')` is constructed but not opened during the tests.

## What was implemented

1. **Exact six published names.** Fixed installed production root `G:\OUTLANDISH_01\large_artifacts\digits\`, filenames `digits_<stem>_10_to_10.packed.bin` (with `golden_ratio` for phi) and same-name `.wsl-receipt.json`. Production requires 10,000,000,000 logical digits and 5,000,000,000 bytes. No caller-selected production binary/root, symlink/junction path chain, or legacy-registry lookup. The synthetic policy uses a separate marked `TemporaryDirectory` and explicit tiny digit counts, never passed as REAL.
2. **Converter receipt contract.** Verify `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, version 1, retained converter scope `PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY`, constant/basename/digit/byte counts, lowercase full-file SHA, and **all exact deterministic converter `sample_plan()` entries** (`sample_block_length`, sorted offset/length/digest, original 4,096-byte / 12-position deterministic algorithm). Read and hash every prescribed sample. Receipt bytes themselves get an ordinary SHA-256 for future manifest provenance. The fixture uses >4 KB packed data so the genuine multi-block plan is exercised.
3. **Mandatory whole-source completion gate.** The immutable `CheckedSource.check_completed_stream(actual_sha256, bytes_hashed)` refuses an incorrect entire-file SHA or byte count. This check must be wired immediately before future `COMPLETE` publication. It is **not** an instruction to hash real 5 GB files in a separate preflight pass. An adversarial 60,005-byte fixture alters a digit outside every sampled block: receipt samples still pass, but the full-file completion gate catches the modification. Do not treat sample checks alone as source authenticity.
4. **Approved REAL Powerball history profile.** Fixed isolated file `GAIS/OUTLANDISH_01/POWERBALL_preholdout_only.csv`; exact column header, no column sorting, IDs **1144–1576 inclusive** (`cutoff_exclusive=1577`), exactly 433 contiguous rows, strict numeric/canonical values and roles (seven distinct mains 1–35, separately ranged PB 1–20; PB may equal a main). Validate every row ID against the cutoff **before processing any outcomes**; reject missing, extra, duplicate, out-of-order and future IDs. Return its SHA-256 and drawn-order rows for later immutable manifest/replay use. Reopening the drawset with an expected manifest hash refuses changed outcomes.
5. **Oz REAL remains fail-closed.** The real Oz `installed_history_profile('oz')` raises until the previously approved *isolated* 7+3 modern-era file, approved first/cutoff IDs and exact header are verified. No parent Oz master/holdout file is opened. Artificial Oz test histories (seven plus three distinct balls, 1–47) exercise role and cutoff validation; their header and bounds are **not** a fabricated approved REAL Oz profile.
6. **Fixed create-only output selection.** REAL and NULL production parents are respectively `G:\OUTLANDISH_01\large_artifacts\results\` and `...\results_null\`, with `REAL_...` and `NULL_...` run IDs required. Synthetic analogues use `TEST_REAL_...` and `TEST_NULL_...` and only marked test roots. Refuse path traversal, root substitution, type spoof, pre-existing run directory, and linked paths. These guards do not themselves create any production directory.

The suite also tests erroneous receipt metadata/sample shapes/digests, physical truncation, byte corruption, bogus SHA/byte counts, path substitution, game/header/era/cutoff/role mutations, changed outcomes with unchanged recorded SHA, and exact converter sample-plan vector. Its refusal count is test evidence, not a blanket claim that all Q4 conditions are qualified.

## Explicit boundaries / next work

**Q4 is NOT complete.** There is no command-line REAL/NULL scanner, no `COMPLETE` manifest publication here, no persisted decoy generator, no raw-event/replay integration, no scientific reporter, and no Q5 authority. The production-source adapter has *not* been invoked on the genuine 5 GB files. The approved receipt schema was established by inspecting the current converter source, not by opening all six private production receipts; check actual receipts under a separately approved non-scanning preflight before qualifying REAL runs.

Next, after Windows fixture PASS: qualify the actual preflight's integration into create-only manifests and the REAL/NULL streaming pipeline; implement durable NULL decoy bytes/seeds and read-only replay; then complete independent hand-computed reporting/Monte Carlo tests. Confirm the isolated Oz historical profile from the approved prior-game source (without opening held-out outcomes) before enabling Oz REAL. Preserve the owner-veto checkpoint for the W→W+1 primary statistic. **No Q5 until owner ratification.**

After tests, append a dated **pending / Windows-verified** status to the current living document §13 or its next section; do not claim owner PASS until owner output arrives. Then stage only these three names, e.g.:

```bat
git status --short --branch
git add GAIS/OUTLANDISH_01/OUTLANDISH_01_Q4_Published_Source_Guards_v0_1.py GAIS/OUTLANDISH_01/OUTLANDISH_01_Q4_Published_Source_Qualification_v0_1.py GAIS/OUTLANDISH_01/OUTLANDISH_01_Q4_Published_Source_Guards_v0_1_README.md
git diff --cached --name-only
```

Review the three staged paths before committing. Do **not** use `git add .`, and do not stage the overarching project's unrelated uncommitted files. No branch or remote commit is created by this package.
