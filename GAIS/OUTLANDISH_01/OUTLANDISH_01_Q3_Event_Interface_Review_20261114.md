# OUTLANDISH_01 — Q3 event/manifest interface review, 14 November 2026

**Status:** ChatGPT engineering review / implementation guidance, **not a replacement for ratified matching/reporting v0.2** or ratification of proposed forecasting v0.1. No real datasets scanned; no parent-project method admission. Owner-reported Q2 extension results are recorded below.

## 1. Inputs and precedence

- `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md` (repository blob SHA-1 `9ebba65a6af42b4f825b899d09c492d79b3329b5`), especially B1–B4 and B7.
- `OUTLANDISH_01_PostMatch_Adaptive_Forecasting_Proposed_Spec_v0_1_FOR_OWNER_REVIEW-2026.11.10.md` (blob SHA-1 `47d811b650e62bab9843f107fd20a42bf53578b6`), especially §§1–2 and §10. **Unratified and implementation parked**.
- Owner's 14-Nov Windows outputs: Q1 full comparison PASS, six legacy 10^9 files independently rehashed and deleted under narrowly archived retirement, Q2 prior five oracle-equal controls and prefix-EOF defect, Q2 extension two further controls PASS, 8/8 mutations detected, 12/12 malformed-input refusals and REAL directory isolation PASS.

## 2. Interface review finding: compatible without changing v0.2

**No new raw-event column is necessary.** Ratified, exact CSV header:

```csv
draw_number,family,start_digit_offset,matched_digits
```

`draw_number` is a genuine integer draw ID for REAL; `family` is one of `K7S`, `K7`, `K6S` (Powerball) or `K7`, `K7mix`, `K6` (Oz), resolved by **manifest game**; `start_digit_offset` is logical, zero-based (both nibble phases legal); `matched_digits` is an *ASCII text* field of exactly the family length (16/14/12), retaining leading zeros. Numeric type coercion of `matched_digits` is forbidden. A REAL run belongs to **one game, constant and exact isolated drawset**. Events are unique by `(draw_number,family,start_digit_offset)`, but other draws/families can legitimately share the same physical start. Sort `(start_digit_offset,family,draw_number)`. A historical `P3` maps to raw family `K6S`, not to a new extra category row.

For every emitted event, require `start_digit_offset + family_length <= effective_scanned_logical_N`. Lookahead may read beyond a chunk's owned starts for computation, but must **not** extend effective-prefix match eligibility. The historical `PREFIX_END_EOF_ELIGIBILITY` failure must be a mandatory new-engine regression.

**Small sibling `run_manifest.json`:** Ratified v0.2 calls for `REAL`/`NULL` run type, game, constant, published packed input/receipt digest and format, complete input logical size and effective scanned scope, authorized historical drawset ID and SHA-256, scanner/code identity, start/end/status, results/event-file identity and event SHA-256, counts and completed integrity checks. The spec fixes these **facts**, not a precise JSON key naming scheme; avoid inventing a new authoritative schema by treating a fixture as ratified. Reporters and classifiers must rehash the historical drawset and event CSV against recorded digests, fail closed on inconsistencies, and **not reread the 5 GB constants**. Do not create a parallel packed registry or allowlist.

**REAL/NULL separation** remains binding: REAL runs use profile-selected, complete, correct-era isolated drawsets (Powerball exactly 1144–1576), genuine integer IDs, published sources and fixed REAL result root; NULL uses separate synthetic drawsets/text decoy IDs and separate `results_null/`, never mixed into a REAL classifier or parent outcome history. An internal fixture test must never be published as a REAL run, even if its rows look like genuine draw IDs.

## 3. Compatibility with parked forecasting v0.1: temporal access is the key

The *proposed* forecast workbench can reuse v0.2 events and derived classification, but for origin `W` a forecasting method must see only **draw-attributed events and learned state with draw_number <= W**; target `W+1` and every later draw are unavailable. No global ranks, nearest-neighbour lookup, best offset, fitted parameters, counts, index statistics or tie-breaking derived from future-labelled event rows may enter the method. Precomputing the complete index for efficiency is not itself prohibited, provided the origin-specific interface exposes only the filtered past and all selected quantities are recomputed/past-filtered accordingly.

The full-run/drawset SHA-256 hashes are provenance/integrity metadata, **not statistical features**. Under proposed L1 future-scramble, the prediction and canonical forecast-derived trace at W must remain identical when *all* future-labelled outcome/event material changes; full-drawset provenance digest may necessarily change and is excluded from the forecast trace comparison. This is a *future research interface compatibility condition*, **not authorisation to build or run a forecasting method**. Forecast scoring/pilots, D1/D2, M2/M3, S0–S4, and parent-method admission remain on hold.

A deliberately simple future-facing function shape is `events_at_origin(qualified_event_rows, origin_W) -> immutable past-only event view`; any derived indices or matching anchors accessible to the forecaster must be created from that view. Implementation should avoid giving a candidate pilot direct access to unfiltered raw events. Q3 need only retain the data necessary to support this; implementing a forecast workbench is out of scope.

## 4. Q2 status and remaining boundaries

- **PASS, owner-run:** extension `controls=2/2`, `mutations=8/8`, `refusals=12/12`, REAL results unchanged; initial independent oracle for Powerball and Oz self-tested. Combined with five earlier historical packed-scanner controls matching the oracle exactly, this gives strong targeted Powerball scanner coverage.
- **KNOWN FAIL IN HISTORICAL SOURCE:** prefix-effective EOF, reproducible four extra events. Preserve old scanner/source/results as evidence, not a qualified reference for that case.
- **NOT YET A CLAIM OF COMPLETE Q2/Q3 PASS:** the old scanner has **no Oz support**, so full Oz oracle-versus-scanner equivalence must wait for the shared Q3 Oz implementation. Ratified v0.2 Q2 asks for at least two independent planted hits per **original category**, multiple draw attributions, explicit interval overlap checks, truncation and mutation coverage including role/EOF cases. Treat any coverage not demonstrated by the current test outputs as remaining to be checked, not silently passed. Some Q2 tests necessarily become red tests against the old known-buggy scanner and green tests against Q3.

## 5. Next implementation slice — lean and test-first

1. Keep the independent plain-Python oracle immutable as the qualification reference. Add any missing small fixtures in separate test code, including the fixed effective-prefix regression and multiple draw attributions. Preserve old scanner bytes unchanged.
2. Implement a **read-only BCD chunk reader + exact raw-event writer** for one Powerball game profile, with per-family EOF eligibility and one-time physical-byte hashing across lookahead; create-only results only in isolated TEST until qualification. Test exact oracle tuple equality for entire fixture sets; test chunk sizes and even/odd starts.
3. Add Oz `K7`, `K7mix`, `K6` on the same matching core, with independent roles/slot/subsequence flags and an already-approved Oz isolated modern-era drawset adapter. Do not guess Oz era cutoff from this note.
4. Only later implement REAL/NULL protected entry points, manifest rechecks, reporter/overlap/permutation logic, qualified runs and the owner gate prescribed by v0.2 Q4–Q5. Avoid full-file scientific scans or methodological additions in this slice.

### Local interface smoke test (non-authoritative)

`OUTLANDISH_01_Q3_Event_Interface_Smoke_v0_1.py --self-test` is a dependency-free, **in-memory fixture-only** demonstration of the four-column type/length/sort/duplicate/effective-EOF contract and a past-only event view with future-scramble canaries. It neither opens REAL/NULL data nor validates a real manifest. It must not be used as evidence of a qualified scanner or a prospective forecasting system.

**Conclusion:** The frozen event and manifest concepts of v0.2 are sufficient for future proposed forecasting access. The only crucial design precaution before Q3 is that the interface must never expose future-labelled events or statistics to an origin-W consumer. No amendment to ratified v0.2 and no new owner decision is required for this ordinary implementation review.
