# Independent ChatGPT R-3 early scope review - E2R CODE-1/CODE-2/CODE-3 v0.1

Date: 2026-10-28. Subject: EX_031; owner-approved scope S-1 through S-3.
Status: EARLY DESIGN COMMENT; not a code acceptance, specification amendment, or run authorisation.

## Inputs and provenance

- EX_031_Claude.zip: e262102700dd6d699c9d04cee6793ba9b0d2cdaa592603a687f1970dc9bc0d2c.
- Scope note: supplied CRLF bytes sha256 6e611f2edb62de3454490222d4f9e0ac1dd1a6c83713dc6dc4b29317111713ac; its LF-normalised SHA-256 is the announced 2d0b0c6acf2f77a518276e24c1c69f6ab3c065ddda26b1cf153cbce0f50c08a1.
- E2R-1 v0.3r3: SHA-256 0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954, read from the earlier supplied reviewed ZIP.
- Installed E1-ALIGN reader source: `src/methods/_common/game_draws_reader.py`, SHA-256 de4631572160214464e0ecdf9b0f6564b193fe244859a3d2d86f703299819ee5, read from the earlier supplied E1ALIGN_Code_Install_v1 ZIP. This is a reviewed package copy, not a live retrieval of commit 1b23fd9.

## Overall recommendation

SUPPORT the owner-approved S-1 (CODE-1 uncalled new library, CODE-2 separately designed wiring, CODE-3 retirement), S-2 (synthetic E_1 test adapter outside E_1 implementation), and S-3 (start independent R-4 T-05 oracle). It is a safer review boundary than simultaneous library, launcher, coordinator and retirement changes. No existing gate may be opened by the presence of CODE-1 files or registry JSON.

Findings: 0 BLOCKER, 4 CORRECTION (design clarification), 1 OPTIONAL, 0 RECONSIDER. These are prospective CODE-1 / CODE-2 design conditions, not a reopening of E2R-1 owner ratification. Every consequential code correction in the eight always-review areas requires RECHECK.

## Specific answers to section 3

A. `NOT_YET_SPECIFIED`: ACCEPT as a **non-runnable administrative placeholder** for E_2..E_62. It matches the variant grammar, and E2R-R21B permits null method revision and declaration digest for a formula-open entry with no declaration. It does not represent a scientifically implemented variant, and must not be used in a C1/C2 record. When a real variant is specified, create its own entry history; do not rewrite or magically promote the placeholder into a different variant.

B. `src/methods/_common/contract_data/`: ACCEPT for new, static, reviewable canonical JSON only, with a deterministic path grammar, strictly sequential append-only registry entries, exact `previous_entry_digest` validation, no path-based permission inference, and no automatic admission merely from the presence of a JSON file. No source file outside CODE-1's new-file allowlist is modified. Track the source-file read/write distinction: contract JSON is read by the new library; the existing accepted launch paths remain unwired.

C. E_1 declarations: `UNORDERED_SET` only, `uses_dates=false`, deterministic, integer scored rankings, `TOP_MARGINAL`/`INVERSE`, `NONE` probabilities and `IS_NOT_APPLICABLE` are consistent with the reviewed E_1 prediction code. `minimum_history_draws=1` agrees with the E_1 prototype requiring at least one preceding draw; verify against accepted per-game wrappers before freezing the JSON. For Oz Lotto, **omit the POWERBALL barrel entirely**, not an extra serialized barrel carrying `ABSENT`; `ABSENT` names the not-applicable *channel condition* in the schema, while the Oz profile contains only `MAIN`.

## Findings and replacements

**E2RC-C01 (CORRECTION; CODE-1; RECHECK on code): synthetic view-digest context.**
Location: scope section 2, `permitted_view_digest(view)`, and E2R-R25; frozen reader `DrawView.e1_view_digest(data_kind=...)`. The reader defaults `data_kind` to `REAL_HISTORICAL_DEVELOPMENT`. Calling it with no argument on synthetic fixtures records the real-development label inside the digest payload. Choose and document the correct, deterministic synthetic/real mapping for the shared helper. Recommended: synthetic contract fixtures call `e1_view_digest(data_kind='SYNTHETIC_CONTRACT_TEST')`; real E_1 legacy behaviour must remain byte-for-byte unchanged. Add tests for both namespaces and keep mode identity out of any target-and-later provenance. No real-data run is requested.

**E2RC-C02 (CORRECTION; CODE-1; RECHECK on code): Oz absent-barrel representation.**
Location: scope section 3 E_1 declaration values. Replace "Oz Lotto with the Powerball channel ABSENT" with "Oz Lotto declares only its MAIN barrel; it never serializes a POWERBALL barrel or synthetic zero-filled vector; validators understand POWERBALL as structurally absent for Oz." E2R-R15A/5.3 and E2R-T05/T07 require that distinction. A phantom PB object would violate the one-barrel Oz profile.

**E2RC-C03 (CORRECTION; CODE-1; RECHECK on code): C1/C2 product-kind separation.**
Location: scope section 2 typed output and E2R-T03; E2R-R41's producible combinations. A synthetic C1 has `product_kind=SYNTHETIC_TEST_OUTPUT`, but a C2 has `product_kind=DIAGNOSTIC_OUTPUT`, even for the same target/view. Explain whether the assembler uses separate method-facing tasks or a documented deterministic transformation; do not allow a method to choose record identity or quietly copy C1 product_kind into C2. The independent oracle proposes a task for each record kind with otherwise identical pre-target fields.

**E2RC-C04 (CORRECTION; CODE-2 design note before wiring; RECHECK on code): E_1 revision discipline.**
Location: scope section 2 CODE-2 "E_1 producing METHOD_FORECAST_V1 through the contract". NAMES-1 and E1-ALIGN each have their own narrow, owner-approved structural exceptions preserving revision 1. Those do not automatically cover a CODE-2 scientific implementation change. The CODE-2 design note must either (a) leave E_1's reviewed scientific functions untouched and wrap their outputs externally with proof of label-level and golden identity, or (b) request a successor revision and owner decision. Merely reusing E_1's name or matching a limited set of goldens is insufficient to grant a new structural exception.

**E2RC-O01 (OPTIONAL; CODE-1): registry placeholder lifecycle.**
A short example showing the old `(E_2, NOT_YET_SPECIFIED, sequence=1, FORMULA_OPEN)` record preserved unchanged when a separately named real variant gains its own declaration/entry sequence would prevent future promotion mistakes. Preserve all declared method names and mark unimplemented texts plainly.

## Boundaries explicitly retained

- CODE-1 adds new files only; existing source, reader, launchers, coordinator, wrappers, E_1 and historical schemas stay byte-identical. CODE-1 is not an executable release path.
- CODE-2 needs a separate, high-risk function-level design note; the 11 protected coordinator functions are not changed without a separate owner decision.
- CODE-3 remains its own retirement/tooling work item. No assumption that Git history survives is restored.
- No SCIENCE allowlist entries, changed safety switches, real-data use, holdout access, beacon fetch, runtime process action or release approval arises from this review.

## Independent oracle status

`Independent_E2R_T05_Oracle_v0_1.py` is supplied as a reviewer-authored, standalone reference. It imports only the previously installed reader and profile modules when executed inside a disposable synthetic workspace, never Claude's CODE-1 modules. A disposable synthetic-only smoke test passed with the frozen reader plus mocked game profiles: 192 cases prepared, 960 example exports checked, and a planted C2 suffix leak detected. This is NOT real installed-game-profile or Claude CODE-1 acceptance; that test remains pending in the project environment. Its manifest explicitly separates orchestration-only master SHA from method-visible task fields. See `Independent_E2R_T05_Oracle_Plan_v0_1.md` for the protocol.

## REVIEWER-DECIDED items

- E2RC-RD-01: Support owner-scoped S-1 CODE-1/CODE-2/CODE-3 split with the original safety gates intact.
- E2RC-RD-02: Support S-2 test-only synthetic E_1 adapter; do not modify E_1 science in CODE-1.
- E2RC-RD-03: Support `NOT_YET_SPECIFIED` as non-runnable administrative variant and `contract_data/` as static, strictly validated JSON.
- E2RC-RD-04: Require C01-C03 to be explicit in CODE-1 and subject to HIGH-tier RECHECK; reserve C04 for CODE-2's design and implementation.
- E2RC-RD-05: Start independent R-4 synthetic T-05 oracle; treat eventual agreement as evidence, not authorisation.

Claude should list RD-01 through RD-05 to the owner as required by the current reporting arrangement. No departure from ratified science, safety or process rules is authorised.

End.
