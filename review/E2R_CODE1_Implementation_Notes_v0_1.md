# E2R-CODE-1 - implementation notes, v0.1

**Document:** the choices made while implementing the E_2-readiness contract library (E2R-CODE-1) within E2R-1 v0.3r3, where the specification leaves a detail open or where Claude chose the stricter reading. For the reviewer's RECHECK; each is RECOMMENDED unless the reviewer objects.
**Author:** Claude, 28 October 2026. **Scope:** `src/methods/_common/contract_*.py`, `src/methods/_common/contract_data/`, `tests/test_e2r_*.py`, `tests/e2r_fixtures.py`.

## Records and fields

1. **Probability objects carry a `status`.** E2R-1 7.2 shows `{kind, vector, tolerance, smoothing_note, calibration_note, provenance, digest}` or `{kind: NONE}`. A record with `INSUFFICIENT_HISTORY` records no numbers (7.4), yet a channel may declare a vector kind, and E2R-R16 forbids silently downgrading the kind. CODE-1 therefore writes:
   - `{kind, status: AVAILABLE, ...}` normally;
   - `{kind, status: UNAVAILABLE, unavailable_reason: INSUFFICIENT_HISTORY}` with insufficient history, and only then.

   A missing vector in any other case is a validation failure.
2. **Digests.**
   - The probability `digest` is the SHA-256 of the canonical vector itself.
   - The `ranking_digest` is exactly the E2R-1 7.2 object.
   - A record digest, also used for declarations, entries and receipts, is the SHA-256 of canonical bytes (E2R-R10).
3. **`ABSENT` is never written.** An Oz Lotto declaration and record name only the `MAIN` barrel. A `POWERBALL` barrel or channel in Oz Lotto is refused, which is how "no channel, no vector, no field values, no zero-padding" is enforced.
4. **Receipts and terminal records carry a `schema` field**, like every other record.
   - The diagnostic receipt names its digests `diagnostic_content_digest` and `diagnostic_file_sha256`; E2R-1 8.2 says "the same fields", and the forecast names would mislead.
   - `frozen_at_utc` is ISO time ending in `Z`.
   - The terminal record has no timestamp, because E2R-1 8.3 lists none.
5. **Diagnostic list values carry `length`**: "with a stated length" (7.7).
6. **MAP_SET labels are recorded as given** (E2R-R30), in the method's order, after the size, range and uniqueness checks.
7. **Readout rule versions** use `[A-Z0-9_]{3,64}`. E_1 uses `TOP_MARGINAL_AND_INVERSE_V1`.

## Rules applied fail-closed

8. **Dates:** a request may include dates only for a method that declares `uses_dates`. A method that declares dates may also be run without them, which is how T03 runs one method variant in both date modes, as E2R-T03 and the reviewer's oracle require.
9. **`permitted_view_digest(view, run_mode)`** (reviewer's E2RC-C01) calls the reader's existing `e1_view_digest`. Its `data_kind` is `REAL_HISTORICAL_DEVELOPMENT` for `REAL_DEVELOPMENT`, as the reader already labels real data, and the run mode itself for the synthetic modes. For legacy E_1 (Powerball, `FULL_HISTORY_RAW_COUNTS_V1`, unordered, date-free) this is the frozen legacy digest. The reader is unchanged.
10. **Declarations refuse, in stage 1:**
    - a non-null `is_interface_version`;
    - non-empty `source_method_dependencies`;
    - a probability tolerance above 1e-9 (E2R-R17 allows that only with reviewer agreement, which code cannot record);
    - an unsorted or duplicated `observation_views`;
    - a declaration with no output of any kind.
11. **Run requests refuse:**
    - the reserved modes, and benchmarks: benchmarks have their own R2 section 10 path and never produce C1 or C2;
    - any target outside the profile's development prefix, for every mode: synthetic masters use the same profile boundaries. The reader's legacy 1577 forecast-only exception is not available through the contract.
12. **Insufficient history** is decided by the contract from the view length against `minimum_history_draws`, not by the method.
12A. **Each record kind's product kind is fixed by the contract** (reviewer's E2RC-C03). A method computes once, from one task. `record_task(task, schema)` gives the identity each record is assembled under: the same fields, with `product_kind` taken from the producible table for that schema. So a synthetic C1 is `SYNTHETIC_TEST_OUTPUT` and its C2 `DIAGNOSTIC_OUTPUT`; the method never chooses either, and a C2 carrying C1's product kind is refused. A request whose product is `DIAGNOSTIC_OUTPUT` can produce a C2 but no C1.
13. **No ticket:** when no barrel has an available TOP or WORST, `assemble_forecast` returns no record. The caller then writes a C2 record if one is declared, or nothing (7.4).
14. **Seed policies:** the set of reviewed policies is empty. A stochastic declaration validates as a placeholder, but it can never be paired with a `SUPPORTED` entry or produce a record (E2R-R61, T08, T18).

## Registry and policy

15. **Registry data:**
    - one canonical JSON file per declaration (`declarations/<GAME>/<METHOD>/<VARIANT>/r<rev>.json`) and per registry entry (`registry/<GAME>/<METHOD>/<VARIANT>/entry_<nnnn>.json`);
    - the loader requires canonical bytes, matching file locations, an unbroken `previous_entry_digest` chain, every declaration it names, and all of E_1..E_62 registered in both games;
    - it compares the bytes after CRLF to LF, because a Windows checkout with `core.autocrlf` gives the data files CRLF. The CRLF install run-through found this: without it, the registry would not load on Windows after any checkout. A test loads a CRLF copy and still refuses non-canonical data;
    - `FORMULA_OPEN` entries with no specification use the reserved variant `NOT_YET_SPECIFIED`, with a null revision and declaration digest.
16. **E_1's declaration**, from its accepted code and R2:
    - `UNORDERED_SET` only, no dates;
    - `minimum_history_draws` 1 (E_1 refuses a target with no earlier draw);
    - deterministic, with `RAW_APPEARANCE_COUNTS_V1`;
    - each barrel `RANKING_WITH_SCORES`/`INTEGER` with `TOP_MARGINAL`/`INVERSE` and `TIE_SHA256_V1`, and no probability;
    - no diagnostic; `IS_NOT_APPLICABLE`.

    T09 shows its contract record equals E_1's own multi-game output label for label, scores, ranking, TOP and WORST, in both games.
17. **Revision rollover (T13)** is a pure check over synthetic identity manifests:
    - a successor revision must be a higher number;
    - a structural exception is recognised only for the package that owns it (`NAMES-1`, `E1-ALIGN`);
    - unaffected methods get a recorded finding.

## Tests and evidence

- **The reviewer's EX_032 conditions:**
  - E2RC-C01 (view-digest namespaces), C02 (no Oz `POWERBALL` barrel) and C03 (product kinds) are implemented and tested in `ReviewerScopeConditions` and T02/T07;
  - O01 is shown by a test: a real variant gets its own chain, and the `NOT_YET_SPECIFIED` placeholder can never be promoted into it;
  - C04 is for CODE-2's design note.
- **The reviewer's R-4 T-05 oracle** (`Independent_E2R_T05_Oracle_v0_1.py`, EX_032) was run by Claude on Linux:
  - `prepare` built its 192 synthetic cases;
  - CODE-1 then exported 960 records (`tools/e2r_oracle_export.py`): C1, C2, D1 and the two record tasks;
  - `check` reported `RECORD CHECK PASS: 384 canonical C1/C2 records, 192 D1, 384 TASK; 48 invariant contexts`;
  - a planted change in one `LONG` C1 was rejected.

  This is agreement evidence, not authorisation. The reviewer may repeat it.

18. **The test double:** T03 uses an E_2-numbered synthetic contract test double. It is not an E_2 implementation and is not installed in the registry.
19. **T12's executor** is `concurrent.futures.ProcessPoolExecutor` with the `spawn` context, at 1 and 6 workers. This is not acceptance of the Windows coordinator or of process lifecycle.
20. **T17 and T18 are scenarios on synthetic records.** The publication mechanism and the seed-policy stages (announce, retrieve, approve) are not implemented (E2R-R48). The tests show what the library already enforces.
21. **Mutation checks** (E2R-1 13; Claude-side, disposable copies):
    - 12 planted defects across T01, T03, T04, T06, T10 and T16, each making its test fail;
    - two first-draft mutations were equivalent, because other guards also caught them. They were replaced by mutations that remove both guards, and the T01 tests were strengthened so that a defect hidden behind re-stamped digests still fails.
22. **Left for CODE-2:**
    - the dispatch gate (T14);
    - publishing receipts and terminal records in the runner and coordinator;
    - `mg-` run IDs and game-namespaced output paths;
    - E_1 producing `METHOD_FORECAST_V1` at run time;
    - replacing the use of Package 2's roster.
