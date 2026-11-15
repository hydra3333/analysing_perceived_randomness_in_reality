# OUTLANDISH_01 — Q3 shared matcher v0.3: streaming + adjustable RAM chunk defaults

**15 November 2026. Synthetic-only implementation and qualification aid.**

## Why this slice

The owner verified that Q3 v0.2 matches the independently written Q2 oracle for both Powerball and Oz Lotto. v0.2 kept **all** events in a Python list until the end. Expected real counts appear small; this is nevertheless a useful, simple future-proofing change before integrating OUTLANDISH as modules controlled by the parent project. No production Q5 scans are authorised by this package.

## Installation

Extract this ZIP **at the repository root**, preserving `GAIS/OUTLANDISH_01/` paths. The ZIP adds only:

- `OUTLANDISH_01_Q3_Packed_Matcher_v0_3.py` — successor, keeping v0.2 intact.
- `OUTLANDISH_01_Q3_Streaming_Qualification_v0_3.py` — fixture-only regression suite.
- This README.

The test harness imports already-installed Q2 oracle/fixtures, v0.2 matcher and Powerball/Oz qualification harnesses. It deliberately does **not** update the living record before Windows confirmation.

## Run on Ryzen (one-line commands)

From `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality`:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Streaming_Qualification_v0_3.py" --self-test
```

The output prints installed physical RAM, presently available physical RAM and selected packed chunk size on **this** Windows machine, followed by `Q3 STREAM SELF-TEST PASS`.

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Streaming_Qualification_v0_3.py" --run
```

Expect the final line beginning:

`Q3 STREAMING PASS: fixtures=43 streamed-comparisons=175; ...`

The full run also replays the existing Powerball 22 fixtures/114 configurations/7 negative checks and Oz 21 fixtures/107 configurations/10 negatives against v0.3, compares the new streaming output **byte-for-byte** and by SHA-256 with the v0.2 event CSV, confirms full physical input SHA, independently verifies raw event tuples against the Q2 reference and checks that an invalid whole-input SHA removes an incomplete CSV. It tests all family-specific prefix EOF cases, including the historical 341-physical/332-effective bug.

**Safety:** synthetic fixture files and result CSVs are created only under automatically deleted Windows TEMP directories. This utility does not select REAL files, modify the six packed constants, read the REAL histories, read/update the legacy registry or touch REAL results. Do not invoke v0.3 directly on production paths; Q4 needs approved REAL/NULL source, receipt, manifest and output-root checks first.

## RAM policy: named code constants + simple optional override

At the top of `OUTLANDISH_01_Q3_Packed_Matcher_v0_3.py`:

```python
GIB = 1024 ** 3
AUTO_LARGE_RAM_THRESHOLD_BYTES = 17 * GIB
AUTO_MIN_AVAILABLE_BYTES_FOR_LARGE = 4 * GIB
AUTO_SMALL_CHUNK_BYTES = 4_000_000
AUTO_LARGE_CHUNK_BYTES = 8_000_000
```

- `chunk_bytes=None` (default): choose **4,000,000 packed bytes** when installed RAM is **at most 17 GiB** or available RAM is **under 4 GiB**, or if the RAM probe is unavailable. Otherwise choose **8,000,000 packed bytes**.
- `chunk_bytes=4_000_000` (or any explicit positive integer up to 64,000,000) overrides automatic selection without probing RAM. Parent project can choose smaller chunks for multiple concurrent workers.
- A physical RAM snapshot is taken **once per scan**. Chunk size remains fixed through that invocation; it is not an adaptive scheduler. Built-in Windows detection uses `ctypes`/`GlobalMemoryStatusEx`; no new package is required.
- These numbers are initial **engineering defaults**, *not* measured optimal values; do not infer a throughput advantage without timing comparable synthetic workloads and recording peak process memory. 4/8 MB refer to **packed** input size, not the larger NumPy workspace.

## API boundary and streaming semantics

The existing convenience functions `scan_packed()` and `scan_packed_oz()` remain available and continue returning all events as `ScanResult.events`. They may be convenient for the expected small result sets, but retain an unbounded growing list of events.

The new **fixture-stage** `scan_packed_stream()` and `scan_packed_oz_stream()` use a create-only `output_csv` argument, and return a `StreamScanResult` with `event_count`, `family_counts`, `event_sha256`, source full-file SHA, bytes hashed, chunks and resolved `chunk_bytes`. The event CSV uses the frozen four-column schema, written in `(start_digit_offset,family,draw_number)` order. Each event is emitted once; only the small list of attributions at a single starting offset is retained for ordering, not the entire event collection.

Lookahead bytes do not own event starting offsets, and family-specific effective-prefix EOF remains enforced. Every source byte is hashed once, even in a prefix scan; the full packed SHA check is performed before the result is returned. CSV bytes are SHA-hashed **as they are written**. If the scan fails, the newly created incomplete CSV is removed; existing files are never overwritten.

The parent project's eventual integration phase must own invocation parameters, worker/thread scheduling, cancellation, memory budget, run identity, source access, result contracts and holdout boundaries. **No such parent-project interface or scheduler is implemented here.** This streaming output is not yet a Q4-qualified REAL or NULL event file; Q4 will create incomplete/complete run directories and mandatory provenance checks.

The existing independent event classifier and overlap reporter still accept in-memory event iterables and typically will encounter far fewer records than the packed-digit scanner. Any decision to stream classification can follow actual event-count and memory measurements, rather than adding complexity immediately.

## After the Windows PASS

Commit the two new Python files and this README. Do not commit this ZIP. Return the final `Q3 STREAMING PASS` line plus the `HOST RAM` line. Then update the living progress record, investigate measured 4MB versus 8MB throughput/RSS on representative synthetic data, and proceed with Q3/Q4 production-entry safety and reporting qualification. **No full 5 GB scan authorised.**
