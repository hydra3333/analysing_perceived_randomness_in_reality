# Predictive Randomness - E_2-readiness code: scope and package split, v0.1

**Document:** the owner scoping that E2R-1 section 13A requires before the E_2-readiness code ("owner scoping after NAMES-1, review with R-2 reproduction and an R-4 T-05 oracle, and owner installation").
**Version:** v0.1 DRAFT, 28 October 2026 (Adelaide, UTC+10:30). Author: Claude. Reviewer: the ChatGPT reviewer chat (R-3 design-stage view of the split). Ratifier: the project owner.
**Status:** a scoping proposal. It authorises no code, run, data access, switch or allowlist change. The ratified design is E2R-1 v0.3r3 (`0a73c92d...a954`); nothing here changes it.
**Base:** commit `1b23fd9` (E1-ALIGN installed and verified).

## 1. Why split

E2R-1 specifies five record families, their validators, the method-facing task, the dispatch gate, receipts and terminal records, registry entries, and the release and retirement policy. Done as one package it would change the shared contract layer, both launchers and the coordinator at once. That is hard to review and hard to undo. Most of it, however, can be built and proved as **new code that nothing yet calls**, which keeps every existing path unchanged until a second, smaller package wires it in.

## 2. Proposed packages (RECOMMENDED)

**E2R-CODE-1: the contract library (HIGH tier; new files only).**
- **New shared modules** under `src/methods/_common/`, importing no method code:
  - the closed vocabularies and the producible/reserved mode table (section 9);
  - the record schemas and fail-closed validators for A1 `METHOD_DECLARATION_V1`, A2 `REGISTRY_ENTRY_V1`, B `RUN_REQUEST_V1`, C1 `METHOD_FORECAST_V1`, C2 `METHOD_DIAGNOSTIC_V1`, D1 `FORECAST_FREEZE_RECEIPT_V1`, the diagnostic receipt, D2 `RUN_TERMINAL_RECORD_V1` and E `POST_OUTCOME_SCORE_RECORD_V1` (type only, no data path);
  - the frozen `MethodTask`, built from a run request and a `DrawView`, and `permitted_view_digest(view)` calling the existing reader method;
  - the typed `MethodOutput` values and the assembler: equal-score groups, `TIE_SHA256_V1` order, TOP and WORST, the ranking and probability digests, then validate and freeze;
  - the consumption predicate of E2R-R38A, as a pure function over records (no file or process action).
- **Registry and declaration data** (canonical JSON, append-only): E_1's `METHOD_DECLARATION_V1` for both games; E_1's `SUPPORTED` entries; `FORMULA_OPEN` entries for E_2..E_62 in both games; the plain-English texts for E_1 and E_2 (D-3); for E_3..E_62 the exact R1/R2 name and a plain "not yet specified" text.
- **Tests:** E2R-T01 to T13, T16 at record level, T17 and T18 (scenarios, synthetic only), with the mutation checks the specification requires for T01, T03, T04, T06, T10 and T16.
- **Untouched:** every existing file. That means the reader, the coordinator (all 11 protected functions), `coordinator_private`, both launchers, the wrappers, E_1's code and folder, Package 2's modules (including `multigame_method_registry.py`), the three switches and the empty allowlist. E_1 therefore stays revision 1 with no exception needed. Every existing guard test, including E1-ALIGN's firewall and shared-code guards, must still pass, now covering the new modules.

**E2R-CODE-2: wiring (HIGH tier; separate design note first).**
- **What it wires in:**
  - the dispatch gate in both launchers (E2R-R57, T14): an active `SUPPORTED` entry, no `IN_DEVELOPMENT.txt`, and refusal before any data read, with the same text from both;
  - `mg-` run IDs and game-namespaced output paths (E2R-R52);
  - publication of receipts and terminal records in the runner and coordinator (E2R-R38A, T16 at run level), generalising Package 2's status and manifest records;
  - E_1 producing `METHOD_FORECAST_V1` through the contract.
- **Before any code:** its design note states exactly which coordinator and launcher functions change. If any of the 11 protected functions would change, that is an owner decision first.

**E2R-CODE-3: retirement tooling (T15)**, with the first successor revision, or earlier if the owner wants it. The static "no import from `archive/`" guard can be in CODE-1 at no cost; there is no `archive/` yet.

## 3. Points needing a choice in CODE-1 (RECOMMENDED unless the reviewer objects)

- **E_1's synthetic `METHOD_FORECAST_V1` (E2R-R51, T09):** the adapter that turns E_1's counts into a `MethodOutput` lives in the **tests**, not in `src/methods/E_001/`. The test then compares it label for label with the legacy records and reproduces the legacy goldens. Putting it in E_1's folder would be an E_1 implementation change (E2R-R14A) for no runtime benefit; CODE-2 makes the real migration.
- **The variant ID for `FORMULA_OPEN` entries with no specification:** E2R-R21B requires a `variant_id` per entry, but E_2..E_62 have none yet. Proposed: the reserved `NOT_YET_SPECIFIED` (it matches `[A-Z0-9_]{3,96}`), with null revision and declaration digest, as E2R-R21B allows.
- **Where the data lives:** one canonical JSON file per declaration and per registry entry, under `src/methods/_common/contract_data/`, named by game, method, variant and sequence. The loader verifies the sequence and `previous_entry_digest` chain and fails closed.
- **E_1's declaration values:** `UNORDERED_SET` only; `uses_dates` false; `RANKING_WITH_SCORES`, `INTEGER`, `TOP_MARGINAL` and `INVERSE`; `probability_kind` `NONE`; `minimum_history_draws` as E_1's accepted code enforces it (confirmed in CODE-1); deterministic; `is_capability` `IS_NOT_APPLICABLE`; Oz Lotto with the Powerball channel `ABSENT`. These are taken from E_1's accepted code and R2; the reviewer confirms them against the frozen E_1.

## 4. Proof and review plan for CODE-1

- **Claude:**
  - Linux runs on Python 3.13 and 3.15;
  - the mutation checks;
  - an exact new-files-only install package (PRE, POST, COMMITTED before the push, as for E1-ALIGN);
  - a per-module suite runner covering the 84 existing tests plus the new ones.
- **The reviewer:**
  - **R-2:** reproduction of the offline tests;
  - **R-4:** an **independent T-05 oracle** written from E2R-1 without reading Claude's code. Proposed: the reviewer starts the oracle now, in parallel, so that it is ready when CODE-1 arrives;
  - the HIGH-tier code RECHECK.
- **The owner:** the Windows run of the full suite before the commit; the install.

## 5. Decisions for the owner

- **S-1:** split as in section 2: CODE-1 the library, CODE-2 the wiring, CODE-3 retirement. Recommendation: yes.
- **S-2:** the E_1 adapter for T09 lives in the tests (section 3). Recommendation: yes.
- **S-3:** ask the reviewer to start the R-4 T-05 oracle now, in parallel. Recommendation: yes.
