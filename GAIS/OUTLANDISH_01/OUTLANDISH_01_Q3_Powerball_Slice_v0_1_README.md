# OUTLANDISH_01 — Q3 Powerball packed-matcher first slice v0.1

**14 November 2026. Status: TEST-ONLY first implementation slice.** This package is based on the repository's ratified matching/reporting specification v0.2 and the committed Q3 interface review at `8326397`. It does **not** amend either specification, qualify Oz Lotto, create a REAL/NULL entry point, or permit Q5.

## What is new

- `OUTLANDISH_01_Q3_Packed_Matcher_v0_1.py`: new low-level, read-only **Powerball** packed-BCD matching engine; NumPy candidate filtering, independent canonical `K7S`/`K7`/`K6S` indexes, all real digit start offsets (including odd), distinct mains with separately ranged/repeat-permitted Powerball, correct per-family effective-prefix end, and one SHA-256 update per owned physical byte even where lookahead is reread. Returns exactly the ratified raw event facts; **does not classify order in the scanner**. Source may be a synthetic fixture only until Q4 adds REAL input/profile restrictions.
- `OUTLANDISH_01_Q3_Powerball_Qualification_v0_1.py`: fixture-only test runner, using the **unchanged independently written Q2 oracle** and saved Q2 scenarios. Creates tiny disposable packed inputs and create-only CSVs exclusively under the system temporary directory. No real game data, source receipts, G: datasets or REAL result folders are read/written by the test run.

Both scripts belong directly in `GAIS/OUTLANDISH_01/` alongside the already-committed Q2 oracle and Q3 interface smoke. Do **not** modify or replace `OUTLANDISH_WSL/wsl_scan_packed_powerball.py` (historical reference), the oracle or the v0.2 specification.

## Run on the Ryzen Windows project venv

Extract the ZIP **into the repository root**, preserving paths. From the repository root in Windows CMD:

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Powerball_Qualification_v0_1.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Powerball_Qualification_v0_1.py" --run
```

The first command checks the pinned independent Q2 oracle's Git blob identity and the saved fixture contract, creating no data. The second uses only `TemporaryDirectory` for synthetic fixture binaries and generated CSVs, then automatically removes them. It requires the project's existing NumPy and Python 3.11+ (your `.venv` already supplies these). It does **not** invoke the old scanner.

Expected final successful line starts:

`Q3 POWERBALL SLICE PASS: fixtures=22 chunk-configurations=114 negative-refusals=7`

The independent assistant-side dry run produced that PASS. **Please send the final line only, or the first failure's traceback if it fails.** The test output includes 22 individual PASS lines if you want to review them locally.

## Exact scope of validation

The harness compares complete `K7S`, `K7`, and `K6S` `(draw, family, start, text)` sets to the Q2 plain-Python oracle over seven byte-chunk sizes (or three for seeded cases). It exercises 341-physical/332-effective digits, zero/odd starts, last-valid 14/16-digit family starts, repeated PB/main equality, multi-draw attributions, chunk boundaries, duplicate suppression, decimal leading zeros, physical full SHA-256, strict four-column CSV roundtrip, create-only writes, nonzero pad, malformed BCD, truncated input, wrong digest, duplicate draw identity and bad PB range.

**Important performance limitation:** To guarantee a complete physical-input digest in this simple correctness slice, even an effective-prefix scan reads and hashes the entire *physical* packed file. No 5 GB scans should be attempted now. Prefix-only I/O optimisation can be separately benchmarked later without relaxing REAL integrity validation.

**Q2/Q3 status:** A new engine passing the known prefix defect does not retroactively qualify the historical scanner; retain the old source/output as diagnostics. Neither this small module nor its test harness is a finished v0.2 matcher, classifier, reporter, profile/receipt gate or REAL/NULL-safe runner. Oz `K7`, `K7mix`, `K6` must be implemented using the same core in the next slice, with independent oracle comparison; then Q4 REAL/NULL safeguards and qualification before any production scans. The old one-byte/digit registry remains deactivated and must not be repopulated with packed data.

## Source control

After running the local tests, stage just these three new files and inspect the diff. The ZIP itself need **not** be committed into the repository. Windows LF→CRLF warnings are informational; the test pins the oracle's canonical Git blob bytes with CRLF normalisation for your Windows checkout.
