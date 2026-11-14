# OUTLANDISH_01 — Q2 supplemental refusal/mutation tests — 2026-11-14

**Purpose:** Complete the *next portion* of Q2 independent qualification after the unchanged historical packed scanner passed five positive Powerball fixtures and demonstrated the known `PREFIX_END_EOF_ELIGIBILITY` defect. This new harness is **synthetic-only**, leaves the old scanner intact, and does **not** launch REAL scans, modify the six 10^10 packed files, or write to REAL results.

## Prerequisites

Ryzen Windows checkout at `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`, running the project's `.venv` Python. The following original files must remain at `GAIS\OUTLANDISH_01`:

- `OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py` (pinned by previous harness).
- `OUTLANDISH_01_Q2_LegacyScanner_Comparison_v0_1.py` (previously executed, pinned source preflight).
- `OUTLANDISH_WSL\wsl_scan_packed_powerball.py` and its existing `wsl_format.py` and `wsl_verify_windows.py` libraries — **do not edit**.

Extract this ZIP at the **repository root**, preserving paths; it adds just this README and the new `OUTLANDISH_01_Q2_Remaining_Qualification_v0_1.py`.

## Commands — Windows CMD, from the repository root

1. Self-test (read-only):

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_Remaining_Qualification_v0_1.py" --self-test
```

2. Execute tiny synthetic tests in Windows TEMP:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q2_Remaining_Qualification_v0_1.py" --run
```

The `--run` creates a fresh temporary test tree, reads the original scanner source, constructs **eight deliberately faulty shadow copies** and tests whether the exact independent oracle can detect those faults. The original scanner's two positive control fixtures must pass. It also exercises **twelve extra invalid-input cases** and confirms the REAL results listing/metadata did not change. Temporary files are removed on exit. No actual lottery drawset is opened; the fixture uses tiny synthetic draw IDs below the historical cutoff.

Expected successful ending:

```text
PASS: REAL results directory listing/metadata unchanged
Q2 EXTENSION PASS: controls=2/2 mutations=8/8 refusals=12/12; historical scanner unchanged; KNOWN Q2 FINDING PREFIX_END_EOF_ELIGIBILITY retained for Q3
This is not Q3 or Q5 approval, and old scanner remains unqualified.
```

If there is any `FAIL`, `Q2 EXTENSION INCOMPLETE`, or `Q2 EXTENSION STOP`, **stop and paste those lines**; do not alter the old scanner to make a test pass. On success, the final summary is sufficient for chat review; only send full logs if a specific failure needs investigation.

## What this establishes (and what it does not)

- Positive controls: old scanner still agrees exactly with the plain-Python oracle on selected completed-file fixtures.
- Mutation tests: chosen specific scanner mistakes cause observable mismatches or duplicate/invalid rows; cannot establish the absence of all possible bugs.
- Refusal tests: selected damaged inputs are rejected via controlled scanner errors; these are not a complete security audit.
- **Known historical bug remains:** original scanner's requested-prefix lookahead can emit events ending beyond effective N; the new shared matcher must reject them. Do not rewrite old reports or claim old scanner qualified.
- **Q2 overall remains open** until all owner-ratified Q2 fixtures and relevant controls are reviewed, including the new matcher requirements that the old PB-only scanner cannot implement (Oz O1/O2/O3, order flags, universal family-specific EOF, distinct REAL/NULL output safety).

## Recording and next phase

Once test results are reviewed, update the existing `OUTLANDISH_01_Living_Decisions_and_Progress.md` **once** with the completed six-file legacy deletion and Q2 findings. Then perform the short event/manifest compatibility review against the **unratified** forecast proposal, *before* substantial Q3 implementation. Keep scientific matching v0.2 ratified and unchanged; parent-project method admission is a separate process. Do not run any Q5 full production scan here.

Source baseline: reviewed GitHub `3d25f61`, old scanner blob `675d0f1592d417483c051605d77093a3e716ac03`; previous Q2 harness explicitly pins these identities. New script was statically checked and its fixture-source mutation self-test was run in an isolated Linux container with a mock source scaffold; real scanner subprocess execution must be performed on the owner's Windows machine.
