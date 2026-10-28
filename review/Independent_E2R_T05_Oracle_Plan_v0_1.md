# Independent R-4 T-05 oracle: synthetic contract record invariance plan v0.1

Date: 2026-10-28. Input authority: owner-ratified E2R-1 v0.3r3, E2R-T03, E2R-R25/R26/R38, plus the installed reader at 1b23fd9. Design artifact only; no authorisation to run a real method or inspect actual outcomes.

## Inputs

1. The unchanged project checkout containing the installed `_common.game_draws_reader` and `_common.game_profiles` Python modules. The oracle imports these existing modules for synthetic-only prefix parsing. It does not import forthcoming CODE-1 modules.
2. A new scratch directory **outside** the repository, generated deterministically by this oracle. Every synthetic master/ledger/INIT record is created there, never under real `source_data/`. The INIT's required `source` marker is present solely because the frozen reader mandates it; it does NOT make the synthetic fixture authentic lottery provenance.
3. Per game: four development-prefix targets chosen from `first_draw+2`, midpoint, `holdout_first-2`, and `holdout_first-1`; three views (`UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC`); dates off/on; suffixes `BASE`, `SAME_A`, `SAME_B`, `LONG`. All data values are invented and legal as CSV fields. Only rows at and after N change.
4. A placeholder method ID `E_9000` and variant `REVIEWER_T05_SYNTHETIC_V1`, for this temporary oracle only. Neither is installed, registered or authorised as a scientific method.
5. When CODE-1 is ready, Claude exports canonical `C1.json`, `C2.json`, `D1.json`, `TASK_C1.json` and `TASK_C2.json` per case, in the folder layout stated in the Python tool. These are purely synthetic exports. MethodTask field sets are E2R section 6.2; C1 and C2 have their distinct section-9 product kinds.

## Oracle's independently determined expected outputs

- 2 games x 4 targets x 3 views x 2 date modes = 48 independent contexts; 4 suffixes each = **192 synthetic cases**.
- For every context, four full-master SHA-256 values are distinct; `BASE`, `SAME_A`, `SAME_B` have equal file byte counts; `LONG` has a different byte count.
- For every context, all four installed-reader `DrawView` slot snapshots, `simple_rows()`, and the prefix-only permitted-view digest are identical. View digest is explicitly calculated as `view.e1_view_digest(data_kind='SYNTHETIC_CONTRACT_TEST')`, because the reader defaults to a real-development label. C01 in the R-3 review asks Claude to pin this rule.
- A deterministic toy count-based ranking and an independent prefix-size diagnostic (not claimed as a ratified C1/C2 wire format) have identical reference digests across suffixes.
- The 192 exported C1s and 192 exported C2s have valid canonical digest fields, contain no master SHA/file path, and are byte-for-byte invariant across suffixes within each of 48 contexts. No fixed CODE-1-specific record hash is invented before CODE-1 exists.
- Each C1's D1 freeze receipt binds that C1's file SHA/digest and the **variant-specific** master SHA (which must differ across suffixes). D1 is NOT required to be byte-invariant.
- For each context, four `TASK_C1` and four `TASK_C2` dumps match the exact method-visible expected fields. Those dumps must be derived from the actual runtime object; a separate CODE-1 test must walk all `MethodTask` slots/attributes to prove there is no hidden field.
- The final checker expects 192 x 5 = **960** exported JSON files. It compares fields, digest claims and invariant bytes and emits a PASS only on a complete set. It is not a replacement for CODE-1 shape, tie-rule, seed, or ledger validators; the HIGH-tier code review and mutation tests remain mandatory.

## Commands for later authorised offline use

```
python Independent_E2R_T05_Oracle_v0_1.py prepare --repo E:\PATH\TO\REPO --out E:\SCRATCH\E2R_T05_ORACLE_NEW
python Independent_E2R_T05_Oracle_v0_1.py check --out E:\SCRATCH\E2R_T05_ORACLE_NEW --records E:\SCRATCH\CODE1_RECORD_EXPORTS
```

The `prepare` directory must not exist and must be outside the repository. The code never reads or writes the project's real `source_data/`. The checker reads only the synthetic fixture manifest and Claude's explicitly supplied synthetic contract output exports.

## Review status

The Python module compiled to bytecode successfully. In a disposable synthetic-only environment, the frozen E1-ALIGN reader (SHA de463157...819ee5) together with deliberately mocked game profiles prepared all 192 cases; the checker passed on 960 synthetic example exports and caught a planted C2 suffix mutation. This is a functionality smoke test, NOT a test against the authentic installed game_profiles module or Claude CODE-1, and not E2R-T03 acceptance evidence yet.

End.
