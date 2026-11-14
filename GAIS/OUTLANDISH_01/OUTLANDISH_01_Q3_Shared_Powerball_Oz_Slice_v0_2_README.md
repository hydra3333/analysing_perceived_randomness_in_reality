# OUTLANDISH_01 — Q3 shared matcher v0.2, Powerball + Oz (synthetic-only)

**Prepared 14 November 2026. Status: new implementation slice; assistant-local synthetic test PASS. The owner's Windows test is still pending. This is NOT Q3-wide qualification, Q4, a REAL/NULL production entry point, or permission to start a full scientific scan.**

## Source and authority

- Ratified `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md` B1–B4, B7 controls the scientific rules.
- Independent `OUTLANDISH_01_Q2_Independent_Oracle_v0_1.py` is unchanged and SHA-pinned by Git blob ID `6ea5562ed681c854f8c552e9600af5d8f9d3be00` (line endings canonicalised for the check).
- Existing `OUTLANDISH_01_Q3_Packed_Matcher_v0_1.py` and `OUTLANDISH_01_Q3_Powerball_Qualification_v0_1.py` stay unchanged. The latter is rerun **against the new shared v0.2 engine** as a regression check.
- New files: `OUTLANDISH_01_Q3_Packed_Matcher_v0_2.py` and `OUTLANDISH_01_Q3_Shared_Qualification_v0_2.py`. Both belong in `GAIS/OUTLANDISH_01/`.

## What changed

The shared NumPy packed-reader/chunk-owner/checksum loop now dispatches independently indexed Powerball `K7S`, `K7`, `K6S` and Oz `K7`, `K7mix`, `K6` family lookups. For Oz the 7-main and 3-supplementary values must all be unique in 1..47. `K7mix` matches **six selected mains and one of the three supplementaries, at any slot**, with its exact role/slot derived by the **later classifier** using the associated original draw; it is not a seventh main and is not constrained to the last field. Repeated draw keys retain every genuine draw attribution. The engine uses family-specific `start+12/14/16 <= effective_N` boundaries and permits both digit/nibble phases.

Raw CSV events are exactly `draw_number,family,start_digit_offset,matched_digits`, with leading zeros kept as text. The fixture writer is create-only. Source BCD SHA-256 covers each physical packed byte once, even when a shorter logical prefix is being matched. The public scan APIs take explicit in-memory fixture draw records; **they do not enforce the published-source/receipt/REAL-NULL/era firewall, which must be built in Q4 before any REAL data use**. The classifying and reporting phases also remain unfinished.

## Windows commands

Extract the ZIP **into the repository root** while preserving `GAIS\OUTLANDISH_01\`. From the repository root on the Ryzen, use the existing `.venv` (NumPy required):

```bat
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Shared_Qualification_v0_2.py" --self-test
".venv\Scripts\python.exe" "GAIS\OUTLANDISH_01\OUTLANDISH_01_Q3_Shared_Qualification_v0_2.py" --run
```

`--self-test`: no writes; verifies pinned oracle and planted Oz fixture definitions. `--run`: uses temporary synthetic files only, reruns the entire prior Powerball qualification against the new shared v0.2 matcher, then runs Oz planted/seeded fixtures and error canaries. The script checks full packed-byte SHA, exact oracle-event tuples, four-column CSV roundtrips, create-only outputs, chunk boundaries, odd/even starts, all seven supplementary slots, true multiple draw attribution, EOF for 12/14-digit families, shorter requested prefixes, wrong barrel roles, invalid BCD, odd padding, truncated file and bad SHA. Temporary outputs are deleted on exit.

**Expected last line if all tests pass:**

```text
Q3 SHARED ENGINE PASS: Powerball preserved (22 fixtures/114 configs/7 refusals); Oz fixtures=21 chunk-configurations=107 negative-refusals=10; exact independent-oracle tuples, full-byte SHA, create-only CSV, effective EOF; TEMP FIXTURES ONLY / NO REAL SCANS / Q5 NOT AUTHORISED
```

This final line was obtained in the assistant's isolated local test using NumPy 2.3.5; reproduction on the owner's Windows venv is a separate evidence checkpoint. For failure, report first traceback and the failing fixture name.

## After owner Windows PASS

Commit new source and harness plus any uncommitted earlier `v0_1` Q3 files; **do not commit this downloaded ZIP**. Keep historical scanner unchanged. Update the existing living decisions/progress Markdown, recording the owner's exact Windows result and noting that Oz qualification so far uses invented fixture draws **not** the modern-era REAL Oz drawset. Next planned slice: pure classifier/role provenance and real drawset profile/manifest validation design, then Q4 REAL/NULL firewalls and reporting. No Q5 REAL scientific scan and no parked forecasting implementation.
