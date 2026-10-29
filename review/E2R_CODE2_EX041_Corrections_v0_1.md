# E2R-CODE-2 candidate v3 - corrections for the reviewer's EX_041 code RECHECK, v0.1

**Document:** what changed between the CODE-2 candidate v2 (EX_040) and v3, and why. It answers `review/Independent_ChatGPT_E2R_CODE2_v2_HIGH_RECHECK_v0_1.md` (EX_041: 2 BLOCKER, both RECHECK). The design note v0.1r1 is unchanged, as the reviewer passed it (E2RC2-RD-06); these are implementation fixes within it.
**Author:** Claude, 29 October 2026. **Exact change:** `review/E2R_CODE2_Install_v3/code_v2_to_v3.diff`.

## E2RC2-CODE-B01 (BLOCKER): no caller-chosen gate evidence

**Finding:** the public run, dispatch, consumption and coordinator-gate functions accepted `orphan_marker`, `data_root` and `methods_root`. So a caller could point them at a harmless marker or at an alternate registry.

**Change:**
- **No locator parameters.** Every public function now takes none:
  - `contract_dispatch.dispatch_gate(request)`, `legacy_gate(game, method, variant, revision)`, `variant_released(game, method, variant)` and `active_pins(game, method, variant)`;
  - `contract_runner.run_contract_method(request, *, compute, verify, repo_root, run_root)`;
  - `contract_publication.read_run(folder)`;
  - `coordinator_private.contract_coordinated_gate.gate_coordinated_contract_request(request)`.
- **Where the evidence comes from:** the installed registry, the method folders and the global orphan marker are the fixed module constants, read at call time:
  - `contract_registry.DATA_ROOT`;
  - `contract_dispatch.METHODS_ROOT`;
  - `contract_runner.ORPHAN_MARKER`.

  There is no command-line flag, environment variable or gate toggle.
- **The tests:** they patch those constants in-process, through one test-harness helper (`tests/e2r_code2_fixtures.installed()`), as the reviewer allowed.
- **The data source is fixed as well:**
  - a synthetic run may read only a workspace outside the project's data, results, code and record folders. This check now sits inside `run_contract_method` itself, not only in the command line;
  - a `REAL_DEVELOPMENT` run, which is still switched off, may read only the project itself.

  Either refusal is `DATA_SOURCE_REFUSED`, before any data is read or any folder is created.

## E2RC2-CODE-B02 (BLOCKER): no coordinated publication

**Finding:** `run_contract_method(..., execution_path='COORDINATED')` published a SUCCESS terminal record labelled COORDINATED.

**Change:**
- **No execution-path parameter:** neither `run_contract_method` nor `RunPublication` has one any more. `RunPublication` always writes `STANDALONE`.
- **Passing one fails immediately:** a call with `execution_path=...` raises `TypeError` before any folder is created or anything is read.
- **Defence in depth:** `read_run` still refuses any folder whose records claim the COORDINATED path.

## Tests and evidence

**The new test class `NoCallerChosenAuthority` (5 tests):**
- **Signatures:** no public function has a locator, gate or execution-path parameter.
- **Locator arguments refused:** `orphan_marker`, `data_root`, `methods_root` and `execution_path` are refused with `TypeError`, by the runner and by `read_run`, and no folder is created.
- **A genuine marker:** a marker at the fixed location always refuses the run and blocks consumption.
- **Standalone only:** every run's terminal record and receipt say STANDALONE.
- **The data source:** a synthetic run reading the project, and a real run reading anything else, are both refused.

**Existing tests:** the earlier "coordinated" consumption test now fabricates a COORDINATED folder, because CODE-2 can no longer publish one.

**Evidence (Claude, Linux; author evidence, not authorisation):**
- **The suite:** 190 tests (84 + 54 + 52) pass on Python 3.13.17 and 3.15.0b4.
- **Mutation checks:** 22 of 22 caught, with the controls passing. The 4 new ones:
  - `read_run` accepts a caller marker;
  - the gate accepts a registry root;
  - the runner publishes COORDINATED;
  - a synthetic run may read the project.
- **The reviewer's own reproducer** (`E2RC2_Trust_Boundary_Synthetic_Repro_v0_1.py`): against v2 it reproduces all three bypasses. Against v3, the first forbidden use stops with `TypeError: run_contract_method() got an unexpected keyword argument 'orphan_marker'`. The tests above check each of the three uses separately.
- **Install run-throughs** in disposable clones, LF and CRLF, on both Pythons.
