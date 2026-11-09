# Native-Windows generation source archive — evidence only (9 Nov 2026)

This directory preserves the exact **model-created and owner-tested** Windows 10 i5-4670 gamma/lemniscate generation package, version **v0.1r3**. It was not present in the GitHub tree at the source-checked commit `06c26a66bfcca12d02e36c49a0b476732d6d3a13`; it is a **new source-provenance archive**, not a migration of runtime state and not a new release. It is intentionally alongside the existing WSL generation implementation under `GAIS/OUTLANDISH_01/OUTLANDISH_WSL/`; no tracked WSL script is overwritten.

**File:** `OUTLANDISH_NATIVE_WIN_v0_1r3_FULL_END_TO_END_RERUN.zip`  
**SHA-256:** `48539fdfc828dc47382fa79be547e76c9186c589e8e2caa0a3e65e14262948f4`  
**Archive integrity:** ZIP CRC test passed at packaging. All 12 internal files preserved unchanged.

Contains `RUN_TEST_AS_ADMIN.bat`, `RUN_PRODUCTION_AS_ADMIN.bat`, `outlandish_windows_production.py`, copied converter/format modules, test launchers/tests, README. The native Windows scripts are intended for **i5 G:/T:**, NOT for execution on the Ryzen E: Git checkout. The owner's actual i5 elevated **1,000,000 γ + 1,000,000 lemniscate** end-to-end run finished `OUTLANDISH_TEST_EXIT=0`, and each 500,000-byte published test binary had an independently re-read matching SHA-256. **No 10^10 Windows production run was started as of the recorded pause.** A 10^10 dry preflight of y-cruncher's true logical disk requirements remains outstanding; the scripts' conservative free-space thresholds do NOT prove sufficiency.

This snapshot has **not** been independently installed/run from GitHub, and it must not silently replace a newer local script if the i5 version changed. Before production, compare the locally installed scripts to this archived source, confirm operational feasibility and receive the owner's explicit go-ahead. Do not unzip runtime outputs into E:, commit 5-GB binaries, restart work on matching, or alter a frozen scientific specification as a consequence of adding this evidence.
