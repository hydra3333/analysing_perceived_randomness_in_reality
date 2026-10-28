# Predictive Randomness - E_2-readiness method-generic contract specification, v0.3r3

**Document:** the stage-1 contract-field schema and acceptance list required before E_2 (R2 v0.5 section 5.6; R3 v0.5 section 17.13 stage 1; Architecture v0.8 section 20A; agreed roles position section 10 item 1).
**Version:** v0.3r3 DRAFT for focused recheck, 28 October 2026 (Adelaide, UTC+10:30). v0.3r3 answers the reviewer's second focused recheck (`Independent_ChatGPT_E2R_v0_3r2_Focused_Recheck_v0_1.md`, `865edd97...def2`: R2-F-C01 on seed roots, and R2-F-C02 on this version label), and records owner decision D-11; Appendix C maps both. v0.3r2 answered the reviewer's focused recheck of v0.3r1 (`Independent_ChatGPT_E2R_v0_3r1_Focused_Recheck_v0_1.md`, `866974a7...e392`: 1 BLOCKER, 4 CORRECTION), and records the owner's seed decisions D-9 and D-10; Appendix B maps each item. v0.3r1 differed from v0.3 (never sent for review) only by recording the owner's decision D-8 on OPEN-4. v0.3 answers the reviewer's consolidated R-3 review of v0.2 (`E2R_R3_Review_Commit_Independent.md`, `17087f57...b2b2`: 3 BLOCKER, 10 CORRECTION, 2 OPTIONAL, 1 RECONSIDER) and records the owner's source-tree and release decisions of 28 October 2026. Appendix A maps every finding to its resolution. v0.2 (`4254128d...c4a4`) is superseded.
**Author:** Claude (primary designer and coder). **Independent reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner.
**Status:** DRAFT. It becomes binding only when the owner ratifies it. Nothing in it authorises any run, data access, holdout access, switch change, allowlist entry, method registration, source move, NAMES-1 work or code acceptance. Declaring a field, status or capability authorises nothing.
**Base:** repository commit `be185485693f29cf9ab28292dc6eebad00bbc32c`.
**Holdout statement:** no draw outcome appears in or was used for this document. The only numbers are rule constants (barrel sizes, era first draws, development boundaries) already in the ratified documents.

**Tags.** Each requirement is labelled:
- **DECIDED**, citing the owner-ratified source it restates, or an owner decision of 28 October 2026 recorded in section 14;
- **RECOMMENDED**, a design choice Claude proposes for ratification with this document;
- **OPEN**, a decision for the owner, with a recommendation (section 14; none remain at v0.3r3).

Requirement IDs are `E2R-Rnn`; acceptance tests are `E2R-Tnn`.

**Three kinds of content (reviewer's ADD-C10).** To keep authority clear, this document separates:
1. **Schema duties:** the records, fields and validators of sections 3 to 11. These are what the E_2-readiness code package implements.
2. **Source-tree and release policy:** section 12A. It is specified now, but is put into practice by the separate NAMES-1 package and by later method packages, not by this document.
3. **Future authorisations:** NAMES-1, the E_2-readiness code and every later run. Each needs its own owner decision (section 13A).

---

## 1. Purpose in plain English

E_1 was built with its own one-off conventions: an `e1-` run-ID prefix, hard-coded method and variant constants, Powerball-only result checks, a target ceiling written into the code, and an E_1-shaped result schema. Before E_2 (or any later method) is built, those must be replaced by one shared contract that every method meets (Architecture 20A, DECIDED).

This document specifies that contract. It covers:
- what a method **declares** about itself, once per game, variant and revision;
- what a method **returns** for a target draw, in whichever form it genuinely has, and how that output is checked before it is frozen;
- what the **orchestration side** records around a run: the freeze receipt for a valid forecast, and a terminal record for every run;
- the **scorer-only** record written after an outcome is opened;
- how source code is kept, retired and released (section 12A);
- the **acceptance tests** that must pass before E_2 is built;
- how schemas are **versioned and migrated**.

It does not specify E_2's mathematics. That is a separate, later specification under R2 section 7.1.

---

## 2. Principles carried into every record

- **E2R-R01 (DECIDED; R2 3.1, R3 17.3.3, T-05).** Strict N-1: a forecast for target N is computed only from eligible same-game draws with `draw_number < N`.
- **E2R-R02 (DECIDED; register "B1", R2 9.2 and R2-C19).** The whole-master SHA-256, the file length and any other value derived from target-and-later bytes are **orchestration-only provenance**. They never reach a method, a method-facing object, a seed, a cache key or a forecast's content identity.
- **E2R-R03 (DECIDED; R2-C10, R2-C12).** Nothing is fabricated to satisfy an interface. A missing ranking, score, inverse or probability is recorded as unavailable with a reason. Non-finite numbers, duplicate labels, wrong counts and wrong sums are validation failures, never silently corrected.
- **E2R-R04 (DECIDED; the owner's foundational points of 26 October 2026, H-1 v1r2 section 2A, points 3 and 6).** Mark, never suppress. The contract never makes a method ineligible because of its results, and never discards a legitimate method output because it is not a ticket. A status records what happened; it does not hide a record.
- **E2R-R05 (DECIDED; R3 17.3.1, R2 3.6).** One game per record. Draws are identified by `(game_id, draw_number)`. Labels and rank positions are 1-based and as printed. Internal 0-based indices never appear in a record.
- **E2R-R06 (RECOMMENDED).** Fail closed. Every validator rejects unknown schemas, unknown fields, missing fields and values outside a closed vocabulary. There is no "best effort" parsing of a scientific record.
- **E2R-R07 (RECOMMENDED; revised for E2R-B01).** The **method computes; the contract assembles.** A method returns only a typed method output (section 7.0): for each barrel, whichever of a scored ranking, an order-only ranking or a native set it genuinely has, plus optional probabilities, and optionally a typed diagnostic. The shared contract module adds every identity field from the declaration and the view, applies the tie rule, then validates and freezes the record. A method therefore cannot mislabel its game, target, variant or view.

---

## 3. The five record families

```text
 (A1) Method declaration (immutable) ---------+
      game, method, variant, revision,        |
      capabilities                            |
 (A2) Registry entries (append-only) ---------+
      status, reason, texts; newest is active |
                                              v
 (B) Run request (orchestration) --> reader --> DrawView (prefix only)
     pin: master file, ledger version,        |   + MethodTask (no master SHA)
     master SHA (orchestration only)          v
                                     method computes a typed output
                                              |
                                              v
 (C) Method output records (canonical, pre-target; content identity suffix-invariant)
     C1 METHOD_FORECAST_V1   (tickets, rankings, probabilities)
     C2 METHOD_DIAGNOSTIC_V1 (typed diagnostic signal; never a ticket)
                                              |
                                              v
 (D) Orchestration receipts
     D1 FORECAST_FREEZE_RECEIPT_V1 (only after a valid C1 is frozen; immutable)
     D2 RUN_TERMINAL_RECORD_V1     (every run: success or failure, with reason)
                                              |
                     ... outcome opened later, separately gated ...
                                              v
 (E) Post-outcome score record (evaluator only; never read by a predictor)
```

- **E2R-R08 (RECOMMENDED).** Families A, C and E are separate schemas, as are B and D, and no record of one family embeds another. They are linked by digests:
  - C names A's declaration digest;
  - B, D1 and D2 name the active registry entry's digest as well (section 5.5);
  - D1 names C1's content digest;
  - D2 names the run and, on success, the D1 digest;
  - E names C1's and D1's digests.
- **E2R-R09 (DECIDED as a principle, R2 8.2 and R3 2.2; RECOMMENDED as structure).** A method-facing object never contains anything from B or D except the fields listed as method-visible in section 6.2.

---

## 4. Common encoding rules

- **E2R-R10 (RECOMMENDED; matches the existing `canonical_bytes`).** Canonical JSON: UTF-8 restricted to ASCII (`ensure_ascii`), keys sorted, separators `,` and `:`, `allow_nan=False`, one trailing newline. A record's digest is the lowercase hexadecimal SHA-256 of its canonical bytes.
- **E2R-R11 (DECIDED; R2 5.6 field 3, MRT-12, owner decision 26 October 2026).**
  - Every integer field fits in int64.
  - Every floating value is a finite IEEE-754 float64.
  - Canonical JSON writes floats with Python's shortest round-trip representation, so a float64 value round-trips exactly.
- **E2R-R12 (RECOMMENDED).** Negative zero is rejected by the validator. `0.0` and `-0.0` compare equal but serialise differently, so they would give two digests for one forecast. Methods normalise it before returning.
- **E2R-R13 (RECOMMENDED).** Schema IDs are immutable upper-case names ending `_V<n>`, for example `METHOD_FORECAST_V1`. Once a schema is used to freeze a record, its meaning never changes (section 12).
- **E2R-R14 (DECIDED; R2 5.3).** `method_id` is the permanent `E_n`. `method_revision` changes when the method's specification or implementation changes (see E2R-R14A). `variant_id` names an estimator, fit, view or selection alternative under the same hypothesis. IDs are never reused or renumbered. Formats:
  - `method_id`: `E_[1-9][0-9]*`;
  - `variant_id`: `[A-Z0-9_]{3,96}` (as Package 2);
  - `method_revision`: a positive integer written as text.
- **E2R-R14A (RECOMMENDED; reviewer's ADD-C06).** One approved revision means one fixed, reviewed implementation, including the behaviourally relevant shared helpers it depends on. "Behaviourally relevant" means in-repository code used in computation, selection, encoding or method-facing data preparation.
  - If an approved method's specification or behaviourally relevant implementation actually changes, including a change to a behaviourally relevant shared helper it uses (arithmetic, selection, encoding or view preparation, directly or through other helpers), that method **must** get a successor revision. This applies even if its own entry file is unchanged (reviewer's F-C02).
  - A documented compatibility finding may establish only that a changed helper is **not used** by a method, or that the changed part is **not behaviourally relevant** to it. It never excuses a known change to that method's implementation.
  - A revision is never reused after an implementation change merely by asserting that outputs did not change.
  - Methods that do not use the changed helper keep their revisions.
  - `FORMULA_OPEN` and `UNSUPPORTED_FOR_GAME` entries need no invented implementation.
  - *Example:* E_2 r1 and E_3 r1 both use shared helper H r1. A package changes H's arithmetic, making H r2. That package also declares E_2 r2 and E_3 r2, and moves H r1 and both methods' r1 files to the archive (section 12A). E_4, which does not use H, stays at its revision, and the package records that finding.
  - The one scoped exception is NAMES-1's purely structural rename, decided and reviewed in that package (12A.5). It is not a precedent for later substantive changes.
  - This is package-time release governance. It is not a run-time hashing or code-recording mechanism. Source paths, file hashes and commit IDs never enter a declaration or a forecast's content digest.
- **E2R-R15 (RECOMMENDED).** Vectors indexed by label are JSON arrays in ascending label order, element 1 for label 1. The record also states `label_low` and `label_high`, so the order is never implicit.

---

## 5. (A) Method declaration - stage-1 field 1, and fields 3 and 4 as declarations

One declaration exists per `(game_id, method_id, variant_id, method_revision)`. It is static and immutable: it never depends on a target or on data, and it never changes after it is installed. Status, reason and descriptive texts are not part of it. They live in registry entries (section 5.5), so releasing a method never changes its declaration (reviewer's F-B01).

### 5.1 Fields (schema `METHOD_DECLARATION_V1`)

| Field | Type | Rule | Source |
|---|---|---|---|
| `schema` | text | `METHOD_DECLARATION_V1` | E2R-R13 |
| `game_id` | text | `POWERBALL` or `OZLOTTO` | field 1 |
| `profile_version`, `era_id` | text | must equal the frozen game profile | field 1 |
| `method_id`, `variant_id`, `method_revision` | text | E2R-R14 | field 1 |
| `observation_views` | list | non-empty subset of `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER`, `PAIRED_DIAGNOSTIC` | R2 4; Architecture 20A |
| `uses_dates` | bool | true only if the method reads dates (opt-in; Architecture 20A) | R2 5.6 |
| `minimum_history_draws` | int | at least 1; for fewer eligible prior draws, status `INSUFFICIENT_HISTORY` | R3 17.3.6 |
| `stochastic_fit` | bool | true if fitting uses random numbers (section 7.6) | R2 9.2 |
| `fit_seed_policy_id` | text or null | null when `stochastic_fit` is false. When `stochastic_fit` is true: null means "seed policy not yet specified", a legal placeholder for a non-runnable method; otherwise the ID of a reviewed seed policy. A `SUPPORTED` registry entry requires a reviewed policy (E2R-R21C, E2R-R61) | R2 9.2; E2R-C01; F-C04 |
| `fit_sampling_model_version` | text | the fit's observation model | R3 0.4 (ERR-R2-04) |
| `channels` | object | one entry per barrel of the profile (5.2) | fields 2 and 3 |
| `diagnostic_schema_id` | text or null | the method's own diagnostic payload schema (section 7.7), or null | R2 5.1 item 7, R2 6.4 |
| `is_capability` | enum | `IS_STATIC`, `IS_STATEFUL`, `IS_NOT_APPLICABLE` | field 4; R2 8.4.3 |
| `is_interface_version` | text or null | null unless a reviewed IS fit/apply interface exists for this variant (section 11) | field 4 |
| `source_method_dependencies` | list | empty for ordinary methods; reserved for ensembles (section 11) | R2 5.3, 8.3 |

### 5.2 Per-barrel channel declaration (revised for E2R-B01)

For each barrel in the game profile (Powerball: `MAIN` 1-35 choose 7 and `POWERBALL` 1-20 choose 1; Oz Lotto: `MAIN` 1-47 choose 7):

| Field | Values |
|---|---|
| `ranking_kind` | `RANKING_WITH_SCORES` (a genuine score for every label, and the complete ranking those scores give); `RANKING_ORDER_ONLY` (a genuine complete order with no numerical scores); or `NONE` |
| `score_type` | `INTEGER` or `FLOAT64` with `RANKING_WITH_SCORES`; `NONE` otherwise |
| `order_ties` | with `RANKING_ORDER_ONLY` only: `STRICT` (no ties) or `GROUPED` (the method states which labels it ranks equal); `NOT_APPLICABLE` otherwise |
| `top_rule_id` | `TOP_MARGINAL` (first k of the ranking; requires a ranking), `MAP_SET` (a native joint-set choice; a ranking is optional), or `TOP_UNAVAILABLE` |
| `worst_rule_id` | `INVERSE` (requires a ranking and `TOP_MARGINAL`), `INVERSE_FROM_MARGINALS` (requires a ranking and `MAP_SET`), or `INVERSE_UNAVAILABLE` |
| `readout_selection_rule_version` | the version of the readout rule (R3 0.4) |
| `ranking_tie_readout_version` | `TIE_SHA256_V1` (DECIDED; TIE v0.2), or `NOT_APPLICABLE` when `ranking_kind` is `NONE` |
| `probability_kind` | see 5.3 |
| `probability_sum_tolerance` | a float64; required unless the kind is `NONE` or `ABSENT` |
| `smoothing_note`, `calibration_note` | text; required unless the kind is `NONE` or `ABSENT` |

**The legal channel combinations (E2R-R15A, RECOMMENDED):**

| `ranking_kind` | `top_rule_id` | `worst_rule_id` | Example |
|---|---|---|---|
| `RANKING_WITH_SCORES` or `RANKING_ORDER_ONLY` | `TOP_MARGINAL` | `INVERSE` | E_1 (counts); an order-only ranking method |
| `RANKING_WITH_SCORES` or `RANKING_ORDER_ONLY` | `MAP_SET` | `INVERSE_FROM_MARGINALS` | a joint-set model that also gives marginals |
| `NONE` | `MAP_SET` | `INVERSE_UNAVAILABLE` | a set-only method with no ranking |
| `NONE` | `TOP_UNAVAILABLE` | `INVERSE_UNAVAILABLE` | a diagnostic-only method, or a method with nothing for this barrel |

Every other combination is invalid. A method may declare both a channel output and a diagnostic schema.

### 5.3 Probability kinds (DECIDED; R2 5.6 field 3)

| Barrel | Allowed `probability_kind` | Vector rule |
|---|---|---|
| `MAIN` (either game) | `NONE` | no vector |
| | `NORMALIZED_LABEL_PROBABILITY` | length = number of labels; each in [0, 1]; sum 1 within tolerance |
| | `MARGINAL_INCLUSION_PROBABILITY` | length = number of labels; each in [0, 1]; sum 7 within tolerance |
| `POWERBALL` (Powerball only) | `NONE` | no vector |
| | `PB_CATEGORICAL` | length 20; each in [0, 1]; sum 1 within tolerance |
| Powerball channel in Oz Lotto | `ABSENT` | no channel, no vector, no field values |

- **E2R-R16 (DECIDED).** A probability kind is declared, never inferred from scores or from a theoretical claim. A declared kind with no lawful vector is a validation failure, not a silent downgrade.
- **E2R-R17 (RECOMMENDED).** The default tolerance is an absolute error of at most 1e-12 on the sum (the example in R2 5.6). A method may declare a different value with its reason; values above 1e-9 need reviewer agreement.
- **E2R-R18 (DECIDED; R2 2.5, R2 5.6 field 7).** No declaration, request, view, record or vector of a predictor ever names or carries Oz Lotto supplementary numbers. Methods never forecast supplementaries.

### 5.4 Declaration rules

- **E2R-R19 (DECIDED; current registry).** E_1's active registry entry is `SUPPORTED` for both games. E_2 to E_62 have `FORMULA_OPEN` entries until each method's specification is ratified, implemented and reviewed. A `FORMULA_OPEN` or `UNSUPPORTED_FOR_GAME` entry is valid and stays registered. It can never produce a method output record.
- **E2R-R20 (RECOMMENDED).** `UNSUPPORTED_FOR_GAME` is used only for a structural reason, for example a method that needs a Powerball barrel declared for Oz Lotto. It is never used because of performance.
- **E2R-R21A (DECIDED; owner decision D-3, 28 October 2026).** `method_name`, `one_liner` and `short_explanation` (held in registry entries, section 5.5) are written, in plain English, for E_1 and E_2 in the E_2-readiness code package. For E_3..E_62 they are written with each method's own specification. Until then, those registry entries carry the exact R1/R2 name, and their one-liner and explanation say plainly that the method is not yet specified. Every text is reviewed with the package that introduces it.
- **E2R-R21 (RECOMMENDED).** The declaration's digest (canonical bytes) is quoted by every method output record it governs. Changing any declared field means a new declaration, with a new `method_revision` or `variant_id` where the science changed. The declaration holds no source path, file hash or commit ID (E2R-R14A).

### 5.5 Registry entries: administrative status, kept apart from the declaration (new for F-B01)

- **E2R-R21B (DECIDED principle, R2 5.6 field 1 and R2-C13; RECOMMENDED structure).** The registry status, its reason and the descriptive texts live in **registry entries**, not in the declaration. The declaration therefore never changes when a method is released, and forecast records keep the same declaration digest.
- Each `(game_id, method_id, variant_id)` has an append-only sequence of `REGISTRY_ENTRY_V1` records. The newest entry is the **active** one, and earlier entries are never edited or deleted.

| Field | Rule |
|---|---|
| `schema` | `REGISTRY_ENTRY_V1` |
| `game_id`, `method_id`, `variant_id` | the method variant |
| `entry_sequence` | 1, 2, 3 ... with no gaps, per method variant |
| `method_revision`, `declaration_digest` | the revision and immutable declaration this entry governs; null only while no declaration exists (`FORMULA_OPEN` with no specification yet) |
| `registry_status` | `SUPPORTED`, `FORMULA_OPEN` or `UNSUPPORTED_FOR_GAME` |
| `registry_status_reason` | non-empty, always |
| `method_name` | the exact registered name (R2 section 7.1) |
| `one_liner`, `short_explanation` | plain English (E2R-R21A) |
| `text_provenance` | `author`, `date`, `text_version`, `source_reference` (field 1, "per-version provenance") |
| `effective_date` | the date the entry was installed |
| `previous_entry_digest` | the digest of entry `entry_sequence - 1`, or null for the first |

- **E2R-R21C (RECOMMENDED).** Rules for registry entries:
  - Only an active entry with status `SUPPORTED` can admit a run, and only for its own declaration digest (section 12A.3). `FORMULA_OPEN` and `UNSUPPORTED_FOR_GAME` entries never have method output records.
  - Release, a text correction or a status change appends a new entry. None of them changes the declaration, and none forces a new scientific revision.
  - A new revision always gets a new declaration, plus a new entry that points to it, normally starting as `FORMULA_OPEN` until release (E2R-R58).
  - Every past declaration and registry entry stays readable. Historical records are validated against the declaration digest they quote.
  - A `SUPPORTED` entry may point only to a declaration whose `stochastic_fit` is false, or whose `fit_seed_policy_id` names a reviewed seed policy (E2R-R61).

---

## 6. (B) Run request and the method-facing task

### 6.1 Run request (orchestration side; schema `RUN_REQUEST_V1`)

The run request extends today's development pin (`DEVELOPMENT_MASTER_PIN_V1_REVIEW`):
- **identity:** `game_id`; `method_id`; `variant_id`; `method_revision`; the target `draw_number`; `observation_view`; `include_dates`; `run_mode`; `product_kind`; the declaration digest; the active registry entry digest;
- **run ID:** `mg-...` (Package 2's game-qualified format), which replaces the `e1-` prefix;
- **pin:** `master_file`, `ledger_version`, `master_sha256`.

- **E2R-R22 (DECIDED; Architecture 20A).** The reader verifies the pin, the ledger and the INIT record. It refuses symlinks and hard links and parses no row at or after N. The pin is orchestration-only.
- **E2R-R23 (RECOMMENDED).** The run ID, the pin, file paths, times, process IDs and worker numbers never enter the method task or a method output record's content.
- **E2R-R23A (RECOMMENDED; reviewer's ADD-C08).** A request is admitted only through the dispatch gate of section 12A.3. A refused request reads no data.

### 6.2 Method-facing task (what a method receives)

A method receives exactly:
- the `DrawView` (prefix only);
- a read-only `MethodTask` holding `game_id`, `profile_version`, `era_id`, `method_id`, `variant_id`, `method_revision`, `target_draw_number`, `observation_view`, `include_dates`, `run_mode` and `product_kind`;
- for a stochastic method only, the reviewed pre-target seed inputs its seed policy names (section 7.6).

None of these depends on target-and-later bytes.

- **E2R-R24 (RECOMMENDED).** `MethodTask` is frozen (no setters) and holds no path, master hash, ledger or INIT data. The T-05 harness walks its fields exactly as it walks `DrawView.__slots__`.
- **E2R-R25 (RECOMMENDED).** The permitted-view digest is the reader's existing generic digest. For legacy E_1 it is the frozen legacy digest. The contract module exposes it under the neutral name `permitted_view_digest(view)` by calling the existing reader method. **The reader's behaviour is not changed by this package.** NAMES-1 changes only the reader's file name and import lines (section 12A.5).

---

## 7. (C) Method output records - stage-1 fields 2, 3 (vectors) and 6 (method-visible identity)

### 7.0 Typed method output (non-normative sketch; reviewer's E2R-O01)

Inside the code, a method returns a disposable `MethodOutput` value with no identity fields:
- per barrel, one of:
  - `ScoredRanking(scores)`: the contract derives the equal-score groups;
  - `OrderOnlyRanking(ranked_groups)`: groups best first, each a set of labels; with `STRICT`, every group has one label;
  - `NativeSet(labels)`: a joint selection;
  - `NoOutput(reason)`;
- an optional `MAP_SET` selection, alongside a ranking;
- optional probability vectors;
- optionally a diagnostic payload.

The contract turns this into C1 and/or C2 records. The shape is a sketch for the code package, not a schema. The frozen schemas below are normative.

### 7.1 Forecast record header (schema `METHOD_FORECAST_V1`)

- **E2R-R25A (DECIDED principle, R2 3.1 and 8.4; RECOMMENDED wording; reviewer's E2R-B02).** `METHOD_FORECAST_V1` is **exclusively a pre-target prediction contract**. Its N-1 rule and suffix-invariant content apply to every record. In stage 1 it can be produced only for:
  - `run_mode` `REAL_DEVELOPMENT` (walk-forward on the development prefix, once separately authorised);
  - the `SYNTHETIC_*` prefix-only test modes.

  `REAL_HOLDOUT` and `FINAL_NEXT_DRAW` are reserved vocabulary and are refused (E2R-R44). `IN_SAMPLE_DIAGNOSTIC` never uses this schema (section 9.3). Benchmarks never use it (E2R-R41A).

| Field | Rule |
|---|---|
| `schema` | `METHOD_FORECAST_V1` |
| `game_id`, `profile_version`, `era_id` | from the profile |
| `method_id`, `variant_id`, `method_revision`, `declaration_digest` | from the declaration |
| `target_draw_number` | N |
| `draw_key` | display only (`POWERBALL_1300`); never an identity |
| `training_last_draw_number` | N - 1 (R2-C07A) |
| `observation_view`, `include_dates` | as requested; must be declared |
| `permitted_view_digest` | E2R-R25 |
| `fit_sampling_model_version` | from the declaration |
| `fit_seed_policy_id`, `fit_seed_identity` | both null if `stochastic_fit` is false; otherwise section 7.6 |
| `run_mode`, `product_kind` | section 9 |
| `record_status` | section 7.4 |
| `barrels` | one object per profile barrel (7.2) |
| `warnings` | list of text; empty if none |
| `canonical_content_digest` | SHA-256 of the canonical bytes of the record without this field |

- **E2R-R26 (DECIDED; R2 5.3, R2-C19, T-05, T-16; wording revised for E2R-C02).** The content digest covers only pre-target, suffix-invariant content. It excludes run IDs, times, environment, worker identity, paths, code identity and every whole-file or ledger hash. Two runs must produce byte-identical records if they agree on all of:
  - the game and target;
  - the method, variant and revision;
  - the observation view and date mode;
  - the declared configuration and seed policy;
  - the run mode and product kind;
  - the implementation environment.

  For such runs, changing only target-and-later master bytes changes no field and no byte. Runs with different declared pre-target configurations may legitimately have different content.

### 7.2 Per-barrel output (revised for E2R-B01 and E2R-C04)

| Field | Present when | Rule |
|---|---|---|
| `barrel_id`, `label_low`, `label_high`, `selected_count` | always | from the profile |
| `ranking_kind` | always | as declared |
| `ranking_status` | always | `AVAILABLE`; or `UNAVAILABLE` with `ranking_unavailable_reason` (for example `INSUFFICIENT_HISTORY`); `NOT_DECLARED` when `ranking_kind` is `NONE` |
| `scores` | `RANKING_WITH_SCORES`, available | score per label, label order; type per `score_type` |
| `score_direction` | `RANKING_WITH_SCORES`, available | `HIGHER_IS_BETTER` (the only value in V1) |
| `ranked_groups` | any ranking, available | the weak order, best first: a list of groups, each a list of labels sorted ascending. With scores, groups are the labels with exactly equal scores. Order-only `STRICT` gives groups of one; `GROUPED` gives the method's own groups |
| `ranking` | any ranking, available | the complete frozen ranking: the groups in order, each group ordered by `TIE_SHA256_V1` (E2R-R28) |
| `tie_identity` | any ranking, available | the seven shared fields of the ratified tuple: `domain` (`PREDICTIVE_RANDOMNESS/TIE_SHA256_V1`), `training_view_sha256` (the `permitted_view_digest`), `target_draw_number`, `method_id`, `variant_id`, `barrel_id`, `ranking_tie_readout_version`. The eighth field, the tied label, is appended per label |
| `ranking_digest` | any ranking, available | SHA-256 of canonical `{"digest_version": "RANKING_DIGEST_V1", "ranking_kind", "scores" (or null for order-only), "ranked_groups", "ranking", "ranking_tie_readout_version"}` |
| `top` | always | `{status, rule_id, rule_version, labels}`; `labels` absent when unavailable |
| `worst` | always | `{status, rule_id, rule_version, labels}`; `labels` absent when unavailable |
| `probability` | channel present | `{kind, vector, tolerance, smoothing_note, calibration_note, provenance, digest}`; or `{kind: NONE}`. Omitted entirely for an `ABSENT` channel |

- **E2R-R26A (RECOMMENDED).** A ranking that does not exist has no `ranked_groups`, `ranking`, `tie_identity` or `ranking_digest`. No placeholder or fabricated digest is ever written.

### 7.3 Validation rules (the "shape and numeric contracts")

- **E2R-R27.** `ranking` contains each label exactly once. With scores, scores are non-increasing along `ranking`, and `ranked_groups` equals the equal-score groups, so it is recomputed, not trusted. Order-only `ranked_groups` partition the labels exactly. With `STRICT`, every group has size one.
- **E2R-R28 (DECIDED; R3 2.4, TIE v0.2; detail for E2R-C04).** Within each group of `ranked_groups`, labels are ordered by ascending `TIE_SHA256_V1` digest. A label's digest is the SHA-256 of the eight fields (the seven of `tie_identity`, then the label as signless base-10 ASCII), each encoded as a uint32 little-endian UTF-8 byte length followed by those bytes, concatenated. Ascending numeric label is the fallback, used only on a digest collision. The validator recomputes every digest. Groups of size one need no digest.
- **E2R-R29 (DECIDED; R3 2.4, T-31).** With `TOP_MARGINAL`, `top.labels` equals the first k labels of `ranking`, and with `INVERSE`, `worst.labels` equals the first k labels of the exact reversal of `ranking` (k = `selected_count`). Both come from the one frozen ranking. Neither is re-ranked or refitted.
- **E2R-R30 (DECIDED; R2-C11, T-32).** With `MAP_SET`, `top.labels` is the method's native joint choice, recorded as given and validated for size, range and uniqueness. If a ranking exists, `worst` uses `INVERSE_FROM_MARGINALS` from it, and overlap with TOP is allowed. If no ranking exists, `worst` is `INVERSE_*_UNAVAILABLE`.
- **E2R-R31 (DECIDED; R2 5.6 field 2, R3 2.3).** TOP and WORST statuses are recorded **independently**, per barrel:
  - available: `PREDICTION_AVAILABLE`;
  - unavailable, with a reason: `TOP_MAIN_UNAVAILABLE`, `TOP_PB_UNAVAILABLE`, `INVERSE_MAIN_UNAVAILABLE`, `INVERSE_PB_UNAVAILABLE`. In the R3 evaluation vocabulary the inverse ones count as `INVERSE_UNAVAILABLE`.
  - An inverse is never manufactured. Without a full ranking, `worst` is unavailable whatever TOP is.
- **E2R-R32.** Labels in any selection are distinct integers within the barrel's range, and there are exactly k of them.
- **E2R-R33.** Every score is a finite value of the declared type (no NaN, no infinity, no negative zero). A method that wants an "infinite" or "never seen" value either maps it to a finite score under its own ratified method specification, or declares `RANKING_ORDER_ONLY`. The contract has no sentinel values.
- **E2R-R34.** A probability vector has the declared length. Every element is in [0, 1] and finite, and the sum is within the declared tolerance of 1 (or 7). Its `digest` is the SHA-256 of the canonical vector.
- **E2R-R35.** A validation failure produces no method output record. It produces a failed `RUN_TERMINAL_RECORD_V1` (section 8.3), and the failure is counted, never hidden (R3 3.6).

### 7.4 Record status (method-level)

`record_status` uses the R3 evaluation vocabulary, kept separate from the benchmark and registry vocabularies (DECIDED; R3 3.6, H-1 5.2):
- `PREDICTION_AVAILABLE`: at least one barrel has an available TOP or WORST;
- `INSUFFICIENT_HISTORY`: fewer than `minimum_history_draws` eligible prior draws. No numbers are recorded.

`DIAGNOSTIC_ONLY` is not a C1 status. A method with no ticket for a target writes a C2 diagnostic record (section 7.7) and no C1 record, or nothing if it has no diagnostic either. The track's target is then counted as unscored with status `DIAGNOSTIC_ONLY` (R3 3.6). R2-C10's `NOT_PREDICTIVE_YET` is recorded under this R3 name. `RUNTIME_FAILURE` and `NUMERIC_INVALID` never appear in a method output record. They belong in the terminal record (section 8.3).

### 7.5 The frozen tickets

For each track (section 8.4), the **ticket** for a target is the barrel selections of that readout:
- Powerball: 7 main labels plus 1 Powerball;
- Oz Lotto: 7 labels.

A ticket with any barrel unavailable is unscored for that track, and the status is counted (R3 17.3.4).

### 7.6 Stochastic fits: seed policy (always-review subject; revised for E2R-C01)

- **E2R-R61 (RECOMMENDED; R2 9.2, R2-C19, R3 0.4).** Stage 1 only reserves the fields and states the requirements:
  - a declaration with `stochastic_fit: true` may carry a null `fit_seed_policy_id` (a placeholder: seed policy not yet specified) only while its registry entry is not `SUPPORTED`; a `SUPPORTED` entry requires a reviewed policy (E2R-R21C);
  - each forecast record carries `fit_seed_policy_id` and `fit_seed_identity`.

  No seed policy exists yet, so in stage 1 no `SUPPORTED` entry can point to a stochastic declaration, and no stochastic fit runs. Typed placeholders for future stochastic methods are legal.
- **Before the first stochastic method is implemented,** its separately reviewed specification defines the seed policy. Every component must be pre-target and independent of the target outcome and of later rows. The policy defines:
  - the owner-declared root seed or root policy;
  - the fitting-configuration digest and how it is built;
  - any admitted external-input digest and its pre-target cutoff;
  - the exact length-prefixed canonical tuple (expected to follow R2 9.2: namespace, method, revision, variant, observation view, fit sampling model version, target, permitted-view digest, the inputs above, and restart index);
  - a portable conversion of the resulting SHA-256 into NumPy `SeedSequence` entropy words, with word order and byte order stated.
- The seed never includes the whole-file hash, a time, a process ID, a run ID or a worker position. No unreviewed default may fill a missing component. The readout rule is excluded, so changing only the TOP or WORST readout cannot change the fit (ERR-R2-04).
- The reviewer verifies outcome-independence and suffix-invariance. Code for this always gets RECHECK (review-disposition procedure, section 4).
- **E2R-R63 (DECIDED; owner decisions D-9 and D-10, 28 October 2026; RECOMMENDED wording).** Root seeds and switching between them:
  - **What a root is (R2-F-C01):** seed entropy for a fitting algorithm. It is **not** data: not an observational input, a covariate or a draw-history feature, and it carries no information about any draw. The N-1 rule and every suffix test apply to the draw data exactly as before.
  - **Source (D-9), in three separate stages:**
    1. **Announce.** Before the pulse exists, a provisional, non-runnable seed policy fixes the selection rule: the service and version (the NIST Randomness Beacon, version 2.0), the chain and the exact pulse (by its timestamp or pulse index), and which output field becomes the root. There is no "latest available", "next best" or fallback pulse.
    2. **Retrieve.** After the pulse is published, the owner fetches that one pulse by hand. Its value and identifiers are recorded and checked against NIST's public archive by someone other than the person who fetched it (the reviewer or Claude, reading the public page). Runs never fetch anything.
    3. **Approve.** The verified value is bound into the reviewed, immutable seed policy. Only then may a declaration name that policy, and only then may its method become `SUPPORTED`. A missing, wrong or substituted pulse means the policy is not approved. Nothing falls back.
  - **Declarations stay immutable:** a declaration that carries a null `fit_seed_policy_id` is never edited. Moving to a reviewed policy means a new declaration under a new revision or variant (E2R-R21).
  - **Timing (owner decision D-11):**
    - **Real forecasts made before a draw** (prospective / FINAL, separately gated): the root must already have been fetched, verified and approved before that forecast is frozen. Otherwise the run is refused.
    - **Retrospective development walk-forward:** a root published after the historical targets is allowed. It is described as randomness chosen for the experiment, never as something that was available when those draws happened. Root trials are labelled, preserved and counted (below). These records are already labelled retrospective development evidence (`DEVELOPMENT_WF_EXPLORATORY`), and the root changes nothing about that.
  - **Reproducibility:** a fixed root and derivation make deterministic replay **possible**, given the same inputs, configuration and computing environment and the validation requirements of R2 9.3 and E2R-T12. It is not an unconditional promise.
  - **One policy per tune:** each revision or variant may name its own pulse in its own policy.
  - **Switching (D-10):** the owner may replace a root, for example on intuition. A replacement is a new seed policy ID, under a new revision (replacing the old one) or a new variant (running alongside it). Results under every earlier root are kept and remain reportable.
  - **Counting:** every seed policy tried for a method is logged in the programme search log, and reports state how many were tried for each method. This is how luck from trying several roots is judged; it is never a limit on trying (pattern origin PO-3, R3 17.3.9).

### 7.7 Diagnostic record (schema `METHOD_DIAGNOSTIC_V1`; new for E2R-B01)

A method that declares a `diagnostic_schema_id` may write one diagnostic record per target, with or without a forecast record:
- **header:** the same identity fields as 7.1 (`schema` = `METHOD_DIAGNOSTIC_V1`, with game, method, variant, revision, declaration digest, target, view, permitted-view digest, run mode), plus `product_kind` `DIAGNOSTIC_OUTPUT`;
- **payload:** `diagnostic_schema_id`, and `values`, a list of `{name, unit, value}`. Each `value` is a finite int64 or float64, or a list of them, with a stated length;
- **trailer:** `canonical_content_digest`.

- **E2R-R62 (RECOMMENDED).** A diagnostic record is pre-target, follows N-1 and has a suffix-invariant digest. It is never a ticket, never scored by the R3 evaluator, never counted as evidence of prediction, and never feeds a method or meta-method, until a separately reviewed adapter (R2 6.4) maps it to a forecast under a new variant. It is kept, never discarded (E2R-R04).
- The method's own diagnostic payload schema is defined in that method's specification. Stage 1 validates only the generic shape.

---

## 8. (D) Orchestration receipts and tracks - stage-1 fields 5 and 6

### 8.1 Freeze receipt (schema `FORECAST_FREEZE_RECEIPT_V1`; revised for E2R-B03)

Issued **only after** a valid forecast record is frozen. It records only facts known at freeze time, and it is **never rewritten**.

| Field | Meaning |
|---|---|
| `forecast_content_digest` | the record's `canonical_content_digest` |
| `forecast_file_sha256` | SHA-256 of the frozen file's bytes |
| `game_id`, `target_draw_number` | the target `(game_id, draw_number)` |
| `method_id`, `variant_id`, `method_revision` | from the record |
| `master_file`, `ledger_version`, `master_sha256`, `ledger_sha256`, `init_record_sha256` | provenance only (E2R-R02) |
| `environment_identity` | Python version, NumPy version, psutil version, OS name and build, and the digest of the installed package list |
| `run_id`, `execution_path` | `mg-...`; `STANDALONE` or `COORDINATED` |
| `registry_entry_digest` | the active registry entry that admitted the run (orchestration side only; it never enters the forecast content) |
| `run_mode`, `product_kind`, `evidence_tier` | section 9 |
| `window` | `[S, L]` when part of a declared window, else null |
| `cohort_id` | a predeclared cohort ID, `EXPLORATORY_COHORT`, or null |
| `status_at_freeze` | the per-barrel TOP and WORST statuses and the record status |
| `outcome_opened_at_freeze` | always `false` |
| `frozen_at_utc` | orchestration clock (informational; R2 8.2A says commit times are not proof of timeliness) |

- **E2R-R36 (RECOMMENDED).** The receipt is create-only (`os.rename` / exclusive create; never `os.replace`).
- **E2R-R37 (DECIDED; R2 5.6 field 6).** The receipt may differ between two runs that see the same prefix, for example when the master grew. The forecast record must not.
- **E2R-R37A (RECOMMENDED; E2R-B03).** The receipt has **no scoring field**. Whether a forecast has been scored is **derived** at report time, by a validated join to post-outcome records (section 10), as one of:
  - `NOT_YET_SCORED`;
  - `SCORED`;
  - `NEVER_SCORED` (non-scientific products).

### 8.2 Diagnostic receipt

A diagnostic record gets the same kind of immutable receipt (`DIAGNOSTIC_FREEZE_RECEIPT_V1`), with the same fields minus `cohort_id` and `status_at_freeze`. It is never joined to a post-outcome record.

### 8.3 Terminal record for every run (schema `RUN_TERMINAL_RECORD_V1`; new for E2R-B03)

- **E2R-R38 (DECIDED; failed-group firewall, register 23 October 2026; structure RECOMMENDED; revised for F-C01).** A run that completes the terminal-publication protocol ends with one create-only terminal record holding:
  - the run ID, game, method, variant, revision and target;
  - the execution path;
  - `outcome`: `SUCCESS`, `RUNTIME_FAILURE`, `NUMERIC_INVALID`, `VALIDATION_FAILURE`, `TIMEOUT`, `INSUFFICIENT_HISTORY` or `ORPHAN_SUSPECTED`, with a reason;
  - the active registry entry digest;
  - on success, the digests of the freeze receipt(s) issued.

  The terminal record is written by the orchestration side (the coordinator or the standalone runner wrapper), never assumed to be written by a failed method process. In the code package, it generalises Package 2's existing status and manifest records, which keep their firewall semantics. A refused dispatch (section 12A.3) is reported, not run, and gets no terminal record, because no run started.
- **E2R-R38A (RECOMMENDED; F-C01).** Publication order and consumption:
  1. The method output file (C1 or C2) is created, create-only.
  2. It is validated, then its freeze receipt (D1 or the diagnostic receipt) is created, create-only.
  3. Only then is a `SUCCESS` terminal record (D2) created, naming those receipts.

  An output is consumable **only if** all of these hold:
  - a valid `SUCCESS` D2 exists;
  - its receipts and output files match;
  - every existing group and firewall gate passes, including the coordinator's exit receipt and the orphan-marker interlock.

  An absent, invalid, incomplete or non-`SUCCESS` D2 means **not successful**, whatever other files exist. A D1 left by an interrupted run is preserved and treated as quarantined. It never counts as an accepted freeze, and it never triggers automatic cleanup, deletion or termination. The no-status/no-kill rule and the global orphan marker apply unchanged. There is no automatic recovery: any later disposition of such a run is a separate, owner-approved inspection.

### 8.4 Tracks

- **E2R-R39 (DECIDED; R3 17.3.4).** A track is `(game_id, method_id, variant_id, readout, mode)`, with readout `TOP` or `WORST` and mode `WF` or `IS`. TOP and WORST of one method and variant come from one ranking, are dependent, and are never counted as unrelated evidence.
- **E2R-R40 (RECOMMENDED format; DECIDED content, owner decision D-1).** `track_id` is the text `GAME:METHOD:VARIANT:READOUT:MODE`, for example `POWERBALL:E_2:EXAMPLE_VARIANT:TOP:WF`. `method_revision` is carried in every record, but is not part of `track_id`. Reports never pool different revisions in one series without a disclosed policy (R3 3.5).
- **E2R-R40A (DECIDED principle, owner decision D-1 and the owner's question of 28 October 2026; RECOMMENDED wording).** Which revision a report uses:
  - A track continues across revisions. Each report or table uses **one declared revision per track** and states it. The default is the latest revision whose method specification is ratified and whose implementation is accepted.
  - Records of other revisions are kept. They are never silently mixed in, and appear only when a report explicitly asks for a labelled side-by-side comparison, or in the "as published" prospective history (E2R-R40B).
  - Re-running a revision on past draws adds new records for the same targets. It never modifies or replaces earlier records (R2 8.2A, T-36).
  - Prospective records (published before the draw) of every revision are permanent. A later revision re-run over those draws is labelled retrospective development walk-forward, never prospective (R3 17.3.5, 17.3.9).
  - A default single-revision report states how many earlier-revision records it left out, and which revisions they belong to (reviewer's E2R-REC01).
  - Why superseded results are kept: prospective forecasts cannot be recreated; comparing revisions on the same development draws shows how much of an apparent gain could be tuning to known results (pattern origin PO-3, R3 17.3.9 and 6.2); and the record is never made to look tidier than it was (mark, never suppress).
- **E2R-R40B (DECIDED; owner decision D-8, 28 October 2026, on the reviewer's E2R-REC01; RECOMMENDED wording).** Prospective results are shown in two separately labelled views:
  - **"As published":** for each target, the forecast that was actually frozen and published before the draw, with its revision named on every row, and no re-runs or later revisions substituted. This is the honest record of what the project published. Totals over this view are labelled as a publication record spanning the revisions shown, never as one revision's performance.
  - **"Current methods":** the default single-revision view of E2R-R40A, which shows the declared current revision only and states what it left out.
  - Neither view mixes revisions into one model's statistics, and comparisons and league tables use the single-revision rule.
- **E2R-R40C (RECOMMENDED; F-C03).** More than one publication for the same target:
  - **Every** genuine before-draw publication stays visible, in an immutable publication history, with its revision and its publication evidence.
  - If the "as published" series shows **one official forecast per track and target**, which one is official is fixed **before the outcome** by a predeclared rule or an official-batch designation. Other publications for that target are counted and listed separately. Nothing is chosen after the outcome.
  - If a view lists several publications for one target, its totals state the publication denominator, and several attempts at one target are never counted as independent target outcomes.
  - `frozen_at_utc` is a local time, not proof of timely publication (R2 8.2A). Publications without independent publication evidence are labelled unverified and counted. Retained archives remain valid if Git history is later cleaned, but they are not themselves publication evidence.
  - The exact publication and evidence mechanism belongs to the later, separately reviewed FINAL and publication specification. Stage 1 does not assume one publication per target.

---

## 9. Separate product, mode, scoring and evidence tier - stage-1 field 5

### 9.1 Vocabularies

Today the code and documents use overlapping words: Package 2's `SYNTHETIC_CONTRACT_TEST`, `COORDINATED` and `FINAL`; E_1's `REAL_HISTORICAL_DEVELOPMENT`; R2 8.1's run modes; and R3's `WF` / `IS`. The contract keeps separate fields:

| Field | Values (closed) | Meaning |
|---|---|---|
| `run_mode` | `REAL_DEVELOPMENT`, `REAL_HOLDOUT`, `FINAL_NEXT_DRAW`, `IN_SAMPLE_DIAGNOSTIC`, `SYNTHETIC_CONTRACT_TEST`, `SYNTHETIC_NULL`, `SYNTHETIC_PLANTED`, `SYNTHETIC_IDENTIFIABILITY`, `BENCHMARK_REAL`, `BENCHMARK_SYNTHETIC` | the data namespace and purpose (R2 8.1, plus Package 2's synthetic contract mode) |
| `product_kind` | `WF_FORECAST`, `DIAGNOSTIC_OUTPUT`, `SYNTHETIC_TEST_OUTPUT`, `IS_DIAGNOSTIC_ENTRY` (reserved), `BENCHMARK_TIMING` | what the record is |
| `execution_path` | `STANDALONE`, `COORDINATED` | how it was run (receipts only) |
| `evidence_tier` | `DEVELOPMENT_WF_EXPLORATORY`, `HOLDOUT_MODE_H`, `PROSPECTIVE`, `IS_DESCRIPTIVE`, `NOT_EVIDENCE` | R3 17.3.9, plus `NOT_EVIDENCE` for synthetic, benchmark and diagnostic records (owner decision D-2, 28 October 2026) |
| derived scoring state | `NOT_YET_SCORED`, `SCORED`, `NEVER_SCORED` | report-time only (E2R-R37A); never stored in a receipt |

### 9.2 Legal combinations

- **E2R-R41 (DECIDED as principle; R2 5.6 field 5, R2 8.4.4; RECOMMENDED as table; revised for E2R-B02 and E2R-C05).** Only these combinations are legal. The validator rejects every other one.

**Producible in stage 1 (synthetic only, until a real run is separately authorised):**

| `run_mode` | Schema | `product_kind` | `evidence_tier` | Derived scoring |
|---|---|---|---|---|
| `REAL_DEVELOPMENT` | C1 forecast | `WF_FORECAST` | `DEVELOPMENT_WF_EXPLORATORY` | `NOT_YET_SCORED` or `SCORED` |
| `REAL_DEVELOPMENT` | C2 diagnostic | `DIAGNOSTIC_OUTPUT` | `NOT_EVIDENCE` | `NEVER_SCORED` |
| any `SYNTHETIC_*` | C1 forecast | `SYNTHETIC_TEST_OUTPUT` | `NOT_EVIDENCE` | `NEVER_SCORED` (synthetic evaluators write only synthetic-namespace records) |
| any `SYNTHETIC_*` | C2 diagnostic | `DIAGNOSTIC_OUTPUT` | `NOT_EVIDENCE` | `NEVER_SCORED` |

**Reserved, refused in stage 1 (vocabulary only):**

| `run_mode` | Future schema | `product_kind` | `evidence_tier` |
|---|---|---|---|
| `REAL_HOLDOUT` | C1 | `WF_FORECAST` | `HOLDOUT_MODE_H` |
| `FINAL_NEXT_DRAW` | C1 | `WF_FORECAST` | `PROSPECTIVE` |
| `IN_SAMPLE_DIAGNOSTIC` | a later IS schema (9.3), never C1 | `IS_DIAGNOSTIC_ENTRY` | `IS_DESCRIPTIVE` |

- **E2R-R41A (RECOMMENDED; E2R-C05).** `BENCHMARK_*` runs produce only timing and technical records (R2 section 10, R2-C20). They produce no C1 or C2 record, no freeze receipt and no post-outcome record, and need not satisfy `METHOD_FORECAST_V1`. Their evidence tier is `NOT_EVIDENCE`.
- **E2R-R42 (DECIDED; R2 8.4.4, R3 17.7).** An in-sample entry never enters the R3 scientific score ledger or the result allowlist. It is never counted as WF, holdout or prospective evidence, and never feeds a method or meta-method. WF and IS are modes, not readout variants.
- **E2R-R43 (DECIDED; Package 2).** The coordinated science allowlist `_COORDINATED_SCIENCE_ALLOWLIST` stays strict and **empty** until separately authorised. This contract adds no entry. When entries are later authorised, its key is recommended to bind `(game_id, method_id, variant_id, run_mode, product_kind, schema)`, a migration made then and separately reviewed.
- **E2R-R44 (DECIDED; R2 3.5, Package 2).** `REAL_HOLDOUT` and `FINAL_NEXT_DRAW` exist only as vocabulary. Every code path that would act on them stays refused. Mode H and FINAL stay shut.

### 9.3 In-sample work (reviewer's E2R-B02)

- **E2R-R44A (DECIDED principle, R2 8.4 and R3 17.13; RECOMMENDED wording).** Stage 1 declares IS capability only (`is_capability`). No IS record schema is defined or produced in stage 1.
- A later, separately reviewed IS fit/apply schema must state:
  - the full-fit cutoff L;
  - the fitted-parameter digest;
  - which recent-state inputs from H(N) are allowed;
  - the IS namespace.
- It must also forbid any treatment of an IS entry as a pre-target forecast or as walk-forward evidence. Listing IS in the vocabulary above authorises nothing.

---

## 10. (E) Post-outcome score record - stage-1 field 7 (type only; revised for E2R-C03)

Schema `POST_OUTCOME_SCORE_RECORD_V1`:

| Field | Powerball | Oz Lotto |
|---|---|---|
| `game_id`, `draw_number`, `track_id`, `mode`, `method_revision` | yes | yes |
| `forecast_content_digest`, `freeze_receipt_digest` | yes | yes |
| `drawn_main` | 7 labels, ascending | 7 labels, ascending |
| `drawn_powerball` | 1 label | absent |
| `main_matches` | 0..7 | 0..7 |
| `powerball_match` | 0..1 | absent |
| `supplementary_matches` | absent | 0..3, at most 7 - `main_matches` |
| `division` | 0..9 (R3 17.4.2) | 0..7 (R3 17.4.3) |
| `evaluator_version` | text | text |

- **E2R-R45 (DECIDED; R2 2.5, R3 17.4.1, R2 5.6 field 7).** Only the evaluator writes this record, after the target's outcome is opened and the track's frozen forecast exists. It is never fed to a predictor. Supplementary numbers themselves are not stored, only their match count.
- **E2R-R45A (RECOMMENDED; E2R-C03).** One record scores one specific frozen forecast. Its create-only key is `(track_id, draw_number, method_revision, forecast_content_digest, freeze_receipt_digest, evaluator_version)`. A second valid run, or another revision, for the same track and target adds distinct evidence. It never overwrites or displaces an earlier score record. A report states its revision and receipt selection policy (E2R-R40A) and the target cohort that policy produces.
- **E2R-R46 (RECOMMENDED; agreed roles position section 10 item 2).** In the E_2-readiness code package, this record exists as a **type and validator only, with no data path**: no function that reads an outcome, and no import from any predictor module. Quarantine opening and the R3 scorer stay separately gated (R3 17.13 stage 2).
- **E2R-R47 (RECOMMENDED).** Mid-rank and other evaluator measures (R3 3.1) are not in this record. Stage 2 adds them in their own versioned evaluator records. Mid-ranks use the frozen `ranked_groups` (both scored and order-only), never the digest order.

---

## 11. Not-applicable behaviour and extension points

### 11.1 Per capability

| Declared | Required behaviour |
|---|---|
| `ranking_kind: NONE` | no `scores`, `ranked_groups`, `ranking`, `tie_identity` or `ranking_digest`. TOP is `MAP_SET` (if declared) or `TOP_*_UNAVAILABLE`, and WORST `INVERSE_*_UNAVAILABLE`. Ranking measures later show `MR_NOT_APPLICABLE` |
| `RANKING_ORDER_ONLY` | no `scores`; `ranked_groups` from the method; `scores` is null in the ranking digest. Score-based measures later show `MR_NOT_APPLICABLE`; rank-based measures apply |
| `probability_kind: NONE` | no vector; probability measures (MR6, MR14) later show `MR_NOT_APPLICABLE` |
| `probability_kind: ABSENT` (Oz Powerball) | the barrel does not exist in the record; no zero-padding; nothing for that channel at all |
| `diagnostic_schema_id: null` | no C2 record may be written |
| `is_capability: IS_NOT_APPLICABLE` | the method appears in WF tables only; any IS request is refused |
| `IS_STATIC` / `IS_STATEFUL` | a declaration only; no IS run is possible until a reviewed IS schema and `is_interface_version` exist and the owner authorises IS |
| `stochastic_fit: true` | not `SUPPORTED` in stage 1 (E2R-R61) |
| registry `FORMULA_OPEN` / `UNSUPPORTED_FOR_GAME` | refused at dispatch before any data is read (section 12A.3); the method stays registered and listed |
| no ticket for a target | a C2 record if declared, else nothing. The track's target is counted as unscored, `DIAGNOSTIC_ONLY` |

### 11.2 Extension points, reserved but not implemented

- **E2R-R48 (DECIDED; R2 5.6 acceptance list, R3 17.13).** The following are reserved by name only. None is implemented in the E_2-readiness package:
  - the IS fit/apply interface and schema (`is_interface_version`; section 9.3);
  - seed policies (section 7.6);
  - ranking and league-table code (R3 17.13 stages 2-4);
  - ensembles and source dependencies (`source_method_dependencies`, which must form an acyclic graph; R2 5.3);
  - ordered-sequence and joint-set distribution channels (R2 5.1 items 5 and 6), which arrive as a new schema version;
  - adapters from diagnostics to forecasts (R2 6.4);
  - external covariates (E_54).

---

## 12. Versioning and migration rule

- **E2R-R49 (RECOMMENDED).** A frozen schema's meaning never changes. Any change to a field, vocabulary or rule is a new schema ID (`_V2`). Old schemas stay readable by validators, for history and reports, and can never be written again.
- **E2R-R50 (DECIDED; R2 5.5).** Legacy E_1 records and goldens are frozen and never rewritten or re-hashed:
  - the `E1_*` schemas;
  - the legacy view digest;
  - the three synthetic goldens and the 1577 forecast-only pair.

  The `legacy_powerball_game_id` compatibility rule applies only to those legacy schemas.
- **E2R-R51 (RECOMMENDED).** E_1 is migrated by adding a `METHOD_DECLARATION_V1` for E_1 (`RANKING_WITH_SCORES`, integer counts, `TOP_MARGINAL` and `INVERSE`) and allowing it to write `METHOD_FORECAST_V1` records in synthetic contract tests. A new schema has a new hash (R2 5.5, "a distinct version and distinct hash"). The acceptance test (E2R-T09) requires, for the same synthetic fixture:
  - the new record's scores, ranking, TOP and WORST to equal the legacy ones label for label;
  - the legacy goldens to still reproduce.
- **E2R-R52 (DECIDED; Architecture 20A).** The E_1-only conventions are retired for new work:
  - the `e1-` run-ID prefix (new runs use `mg-`);
  - hard-coded method, variant and schema constants (now from the declaration);
  - Powerball-only output names and checks (now game-namespaced: `<root>/<game_id>/<method_id>/<variant_id>/<run_id>/`);
  - hard-coded target ceilings (now the profile's `historical_development_target_allowed`). The E_1 1577 forecast-only regression stays as a named legacy test.

---

## 12A. Source tree, retirement and release policy (owner decisions of 28 October 2026)

This section is policy. It is put into practice by NAMES-1 and by later method packages, not by the E_2-readiness schema code. Where it touches the reader, the coordinator or dispatch, the work is HIGH tier and always gets RECHECK.

### 12A.1 Current code only (owner decision D-4)

- **E2R-R53 (DECIDED; owner decision D-4).** `src/` holds only current code, approved or in development, with stable file names that carry no version.
- Each method has its own folder, `src/methods/E_<nnn>/`, where `<nnn>` is the method number zero-padded to three digits, for example `src/methods/E_002/` for `E_2`. The folder name is a **locator only**. The scientific identity is always `method_id` (`E_2`), and the one documented mapping between the two is that zero-padding rule (reviewer's ADD-C07).
- The exact entry-file and module layout inside each folder is fixed by NAMES-1, within Architecture's "one standalone `.py` per method", and is recorded in the next Architecture edition.

### 12A.2 Retirement into revision-labelled archives (owner decision D-5)

- **E2R-R54 (DECIDED; owner decision D-5; reviewer's ADD-C09).**
  - The package that introduces a successor revision moves the **unchanged bytes** of the outgoing method revision to `archive/methods/E_<nnn>/r<k>/`.
  - A superseded shared-helper revision moves, when it is superseded, to `archive/common/<name>/r<k>/`. There are no duplicate helper copies inside method archives.
  - Each archive entry has a `README.md` stating:
    - the method or helper and its revision;
    - the retirement date;
    - the previous path under `src/`;
    - for a method, the names and revisions of the shared helpers it used.
  - **No Git commit ID, and no stored file hash, is recorded.** Git history is not relied on: the owner may clean or rewrite it.
- **E2R-R55 (RECOMMENDED).** The read-only install verifier compares each archived file with the corresponding still-current file in the **pre-installation** `src/` baseline, and confirms the move. This is a package-time check, not a stored hash. The installation proof also covers:
  - relative-path naming, case on Windows, and unique revision folders;
  - package traversal (`__init__.py`);
  - that each README's helper references resolve to a current or archived helper.
- **E2R-R56 (RECOMMENDED).** `archive/` is outside every normal import path, and a static check rejects imports from it. Normal reviewed runners never dispatch an archived revision.
  - This is a normal-workflow control, not an access-control guarantee: an archived `.py` file can still be run directly by hand.
  - Re-running an archived revision is a separate, owner-approved act. It is attempted only if the preserved code, configuration and dependencies are sufficient, and otherwise the project says plainly that an exact re-run cannot be reconstructed. **Exact historical replay is not promised.**
- Later cleanups preserve archive contents and the helper revisions they reference, if historical source reading or reconstruction is still wanted.

### 12A.3 Release: the development flag AND the registry (owner decision D-6)

- **E2R-R57 (DECIDED; owner decision D-6; reviewer's ADD-C08).** A normal dispatch, standalone or coordinated, requires all three of:
  1. an **active SUPPORTED registry entry** for the requested game, method and variant, whose revision and declaration digest exactly match the request, and whose entry digest the request pins (section 5.5);
  2. no `src/methods/E_<nnn>/IN_DEVELOPMENT.txt` file;
  3. every independent safety, environment, data-admission and owner-authorisation gate that already applies.
- How the gate behaves:
  - A missing, stale (not the active entry) or non-SUPPORTED registry entry denies, as does a declaration digest that does not match. An approval for a retired revision is not an approval for its successor.
  - A present flag file always denies. Deleting it never turns `FORMULA_OPEN` or `UNSUPPORTED_FOR_GAME` into `SUPPORTED`.
  - A refused request reads **no data**.
  - Both the standalone runner and the coordinator refuse with the same rule and a clear warning naming the method, the revision and the reason, and printing no data.
  - Neither removing the flag nor updating the registry, alone or together, authorises a scientific run. Those gates stay separate.
- **E2R-R58 (RECOMMENDED).** Safe release sequence:
  - A package that introduces new or revised method code installs it **non-runnable**: the flag file is present, the new declaration is installed, and the active registry entry for the new revision is not `SUPPORTED`.
  - Release is a separate, small, reviewed package the owner installs. It deletes the flag and appends a `SUPPORTED` registry entry for the same declaration: the owner's two deliberate actions. The declaration and earlier entries are not changed.
  - No intermediate installed state may make an unaccepted revision runnable.
  - The flag is an application-level dispatch safeguard, not operating-system protection.

### 12A.4 Sequence and separate checkpoints (owner decision D-7; reviewer's ADD-C10)

- **E2R-R59 (DECIDED; owner decision D-7).** The owner has affirmed this order, each step with its own review and owner authorisation:
  1. ratification of this specification;
  2. NAMES-1, the one-off rename package (12A.5);
  3. the E_2-readiness stage-1 code.

  Ratifying this document authorises none of steps 2 and 3.

### 12A.5 NAMES-1 (separate package; requirements recorded here, proof specified there)

- **E2R-R60 (RECOMMENDED; reviewer's ADD-C07).** NAMES-1 moves existing files to stable names and updates imports and references. It changes no behaviour. Its own reviewed specification provides:
  - the complete old-to-new path map;
  - the import and reference graph;
  - byte comparison of each moved body against the installed baseline;
  - AST equality of every module apart from the permitted import changes;
  - all eleven protected coordinator function ASTs unchanged;
  - import-origin, `__file__` and `__module__`, dynamic-reference, standalone-launch and Windows CMD wrapper checks;
  - the E_1 legacy goldens and the prefix-only and view regressions;
  - the three switches still False and the allowlist still empty;
  - Linux and owner-run Windows suite evidence;
  - a rollback procedure.
- It touches the reader and the coordinator (two import lines, in `coordinator_main`, outside the protected functions), so it is HIGH tier with RECHECK.
- **On revisions:** Claude recommends that NAMES-1 keeps E_1 at revision 1, because its proof shows the code identical apart from import paths. NAMES-1 records that decision explicitly for review; unchanged goldens alone would not be enough. This structural exception is scoped to NAMES-1 only (E2R-R14A).

---

## 13. Acceptance before E_2 (DECIDED list, R2 5.6; tests RECOMMENDED)

All tests are offline. They use synthetic fixtures and, where noted, the accepted development masters read only through the reader at targets below the development boundary. No outcome at or after the boundary is read.

| Test | Acceptance item | What it checks |
|---|---|---|
| E2R-T01 | Shape and numeric contracts | Each rule E2R-R27..R34 has a passing case and at least one failing case: wrong length, duplicate label, out-of-range label, NaN, infinity, negative zero, wrong sum, an int beyond int64, unknown field, unknown schema, a non-partitioning `ranked_groups`, and scores that disagree with `ranked_groups` |
| E2R-T02 | Profile separation between games | Powerball and Oz Lotto declarations, records and vectors cannot be cross-validated. Barrel sizes come only from the profile. A record for one game is refused under the other |
| E2R-T03 | Prefix-only view and digest independence (T-05) | The TH-1 harness extended to records. For a synthetic contract method, at four targets per game, three views and two date modes, with two equal-length suffix rewrites and one longer, the C1 and C2 records' canonical bytes and digests are identical, and the freeze receipt's master SHA differs. `MethodTask` fields are walked like `DrawView` slots |
| E2R-T04 | R3 tie and WORST consistency | The tie order is recomputed from TIE_SHA256_V1 for scored and order-only `GROUPED` rankings. TOP is the first k and WORST the reversal (T-31). `MAP_SET` with `INVERSE_FROM_MARGINALS` is allowed to overlap (T-32). Set-only and no-ranking channels give explicit unavailable statuses with no ranking fields (T-33) |
| E2R-T05 | No Powerball or supplementaries in Oz predictor views | Static: no predictor or contract module names supplementary columns. Runtime: an Oz `DrawView`, `MethodTask` and record carry no Powerball or supplementary field |
| E2R-T06 | Mode firewall | Every combination outside the E2R-R41 producible table is rejected, including every reserved row. Benchmarks produce no C1 or C2 record. IS records cannot be built. Coverage: at least one accepted case per producible row, and one rejected case per reserved row and per wrong field pairing (reviewer's E2R-O02) |
| E2R-T07 | Not-applicable behaviour per capability | Each row of the 11.1 table, including Oz `ABSENT` with no zero-padding, order-only with no scores, set-only with no ranking, diagnostic-only, and stochastic declarations refused as SUPPORTED |
| E2R-T08 | Extension points without early implementation | Static check: no IS engine, seed policy, ranking code, ensemble execution or diagnostic adapter exists. `is_interface_version` is null in every declaration. Every declaration that a stage-1 `SUPPORTED` entry points to is deterministic, with a null `fit_seed_policy_id`. A typed stochastic placeholder (`stochastic_fit` true, null policy, entry not `SUPPORTED`) validates. A `SUPPORTED` entry pointing to a stochastic declaration without a reviewed policy is rejected (F-C04) |
| E2R-T09 | Schema versioning and migration | Old schemas are readable and refused for writing. An unknown schema is refused. E_1's legacy goldens reproduce. E_1's `METHOD_FORECAST_V1` equals legacy label for label (E2R-R51) |
| E2R-T10 | B1 hygiene (R2-C19) | No master, ledger or INIT hash, path or code identity appears anywhere in a `MethodTask` or a C1 or C2 record. Mutation checks (disposable copies only) put the master SHA, the file length or a tail of bytes into the task and expect E2R-T03 to fail |
| E2R-T11 | Post-outcome record has no data path | The type validates synthetic values only. A static import check shows no predictor module imports it, and it contains no function that opens a file. Two score records for the same track and target with different revisions or receipts both validate and never collide (E2R-R45A) |
| E2R-T12 | Determinism (R2 9.3; scope revised for E2R-C05) | The same inputs give byte-identical records across two runs and across one and six workers, within the identified synthetic offline executor and its tested concurrency settings. This is not acceptance of the Windows coordinator or of process lifecycle, which stay separately gated |
| E2R-T13 | Revision rollover (ADD-C06, F-C02) | In synthetic identities, a changed arithmetic helper with an unchanged dependent revision fails, even when a narrow fixture happens to give the same numbers; dependent runnable methods require successor declarations; genuinely unaffected methods keep their revisions with a recorded finding; the NAMES-1 structural exception is recognised only for that package. No path, file hash or commit enters a declaration or content digest |
| E2R-T14 | Dispatch gate truth table and release transition (ADD-C08, F-B01) | SUPPORTED or not, times flag present or absent; missing and stale registry entries; a retired-revision approval against new code; both launchers; refusal before any data read; the refusal text. Release transition (synthetic): declaration D and entry 1 (`FORMULA_OPEN`) are refused; entry 2 (`SUPPORTED`, same D) is appended and dispatch is admitted once the flag is gone; entry 1 and D are unchanged; records made under D stay valid; a request pinning a stale entry digest or a mismatched declaration digest is refused. No existing gate is bypassed |
| E2R-T15 | Retirement proof and archive exclusion (ADD-C09) | On a disposable synthetic source tree and successor overlay: archived bytes equal the pre-installation `src/` bytes; the old path is removed; README helper references resolve; normal imports and dispatch cannot reach `archive/`. The same check repeated in a tree **with no Git history** passes |
| E2R-T16 | Receipts and terminal records (E2R-B03, F-C01) | A freeze receipt is issued only after a valid C1 and has no scoring field. Consumption needs a valid SUCCESS terminal record with matching receipts. Simulated cases, all non-consumable: interruption after the freeze receipt but before the SUCCESS terminal record; no terminal record at all; a failed terminal record; an orphan-suspected group. Each leaves its files preserved, triggers no cleanup or termination, and counts as unsuccessful. No real process is killed and no destructive fault is injected |
| E2R-T17 | Multiple publications for one target (F-C03; specification-level scenario) | Two timely published revisions for one track and target, one designated official before the draw, plus one late or unverified candidate: all three are retained and labelled; the "as published" series shows the official one and counts the others; nothing is chosen after the outcome; publication totals state their denominator. Checked as a scenario on synthetic records now; the publication mechanism itself waits for the FINAL specification |
| E2R-T18 | Seed-policy stages and timing (R2-F-C01; specification-level scenarios, synthetic only, no real beacon fetch) | A provisional policy whose pulse is not yet published cannot be approved and cannot make a method `SUPPORTED`. A correctly retrieved and verified pulse can be approved. A missing or mismatched pulse is refused, with no fallback. A historical target that predates the root is accepted only as labelled retrospective development. A prospective request whose root is not yet approved is refused. A new root is a new policy ID under a new revision or variant, and the earlier root's records stay intact. In stage 1, no stochastic `SUPPORTED` entry can exist |

- **R-4 oracle (agreed roles position section 10, item 2).** The reviewer may write an independent T-05 oracle from this specification without reading Claude's implementation. Agreement with it is evidence, not authorisation.
- **Mutation checks.** For each of E2R-T01, T03, T04, T06, T10, T14 and T16, Claude shows that a planted defect makes the test fail, on disposable copies only.
- **E2R-T14 and T15** test policy code that NAMES-1 and the code package introduce. They join the suite in the package that introduces the code they test.

### 13A. What each later step needs (no authorisation here)

| Step | Needs |
|---|---|
| NAMES-1 | its own HIGH-tier specification and review (RECHECK), owner execution authorisation, Linux and Windows evidence, and owner-controlled installation |
| E_2-readiness code | owner scoping after NAMES-1, review with R-2 reproduction and an R-4 T-05 oracle, and owner installation |
| Any real-data run | its own owner gate, as today |

---

## 14. Owner decisions recorded, and what remains

**Owner decisions, 28 October 2026:**
- **D-1:** `track_id` does **not** include the method revision. A track continues across revisions, and every record carries `method_revision` (E2R-R40, E2R-R40A).
- **D-2:** synthetic and benchmark records get the evidence tier **`NOT_EVIDENCE`**. It is never shown in a league table (section 9). v0.3 RECOMMENDS the same tier for diagnostic records, which are not evidence of prediction.
- **D-3:** the method name, one-liner and short explanation are written for **E_1 and E_2** in the E_2-readiness code package. Each later method's texts are written with its own specification (E2R-R21A).
- **D-4:** only current code lives under `src/`, with stable names and per-method folders (12A.1).
- **D-5:** superseded revisions move to revision-labelled archives with a README, and no commit IDs (12A.2). No per-file hashes and no run-time code-identity recording (the owner withdrew those proposals).
- **D-6:** a method runs only if the registry supports its current revision **and** no `IN_DEVELOPMENT.txt` flag is present. Release is the owner's two deliberate actions (12A.3).
- **D-7:** NAMES-1 comes before the E_2-readiness code (12A.4, 12A.5).
- **D-9:** a seed policy's root comes from a pre-announced NIST Randomness Beacon pulse, fetched once by hand; runs never fetch (E2R-R63).
- **D-10:** the owner may switch roots ("another universe") as a new revision or variant; every root tried is logged and counted in reports (E2R-R63).
- **D-11:** a root published after the historical targets may be used for retrospective development runs, described as randomness chosen for the experiment; a real forecast made before a draw may use only a root already fetched, verified and approved (E2R-R63). The owner chose this over requiring each historical target to have its own earlier pulse.
- **D-8 (was OPEN-4, the reviewer's E2R-REC01):** prospective results are shown both "as published", with the revision named per draw, and separately "per current methods", the single-revision view (E2R-R40B).

**RECOMMENDED** for ratification with the document, unless the reviewer or owner objects: the structure and typed outputs (sections 3 and 7); the encoding rules (section 4); the field tables (sections 5, 7, 8 and 10); the vocabulary and the producible and reserved tables (section 9); the seed-policy requirements (7.6); the versioning rule (section 12); the policy wording of 12A; and the test list (section 13).

**OPEN:** none. The reviewer may raise new questions for the owner.

*Document references: R2 v0.5 sections 2.5, 3.1, 3.5, 3.6, 5.1-5.6, 6, 8.1-8.4, 9.2-9.3, 10, 11.1; R3 v0.5 sections 0.4, 2.1-2.4, 3, 17.3, 17.4, 17.7, 17.13; Architecture v0.8 section 20A; TIE_SHA256_V1 v0.2; agreed roles position section 10; register v0.6; review-disposition procedure (`review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`).*

---

## Appendix A. Resolution of the v0.2 review findings

| Finding | Class | Resolution in v0.3 |
|---|---|---|
| E2R-B01 ranking-only, set-only and diagnostic-only methods | BLOCKER | Adopted: `ranking_kind` with scored, order-only and none (5.2); the legal channel combinations table (E2R-R15A); `ranked_groups`, conditional ranking fields and no fabricated digests (7.2, E2R-R26A); the C2 diagnostic record (7.7); the typed-output sketch (7.0) |
| E2R-B02 IS conflicts with the pre-target schema | BLOCKER | Adopted: C1 is pre-target only (E2R-R25A); IS is reserved with its future schema requirements (9.3); producible and reserved tables split (9.2) |
| E2R-B03 the receipt cannot carry scoring or failure state | BLOCKER | Adopted: the receipt has no scoring field, and scoring is derived (E2R-R37A); a separate terminal record for every run (8.3); test E2R-T16 |
| E2R-C01 seed fields insufficient | CORRECTION | Adopted: `fit_seed_policy_id` reserved; the requirements are listed and the formula is deferred to the first stochastic method's reviewed specification; no stochastic method can be SUPPORTED in stage 1 (7.6). The wrong "section 6.5" reference is corrected |
| E2R-C02 reproducibility claim too broad | CORRECTION | Adopted: E2R-R26 reworded with the reviewer's conditions |
| E2R-C03 score-record keys | CORRECTION | Adopted: `method_revision` added; the create-only key (E2R-R45A); test E2R-T11 |
| E2R-C04 tie identity and ranking digest | CORRECTION | Adopted: seven shared fields plus the label as eighth, with the encoding (7.2, E2R-R28); `RANKING_DIGEST_V1` defined, including the order-only case; nothing written for an absent ranking |
| E2R-C05 benchmarks and worker scope | CORRECTION | Adopted: E2R-R41A; E2R-T12 scope wording |
| ADD-C06 revision meaning with shared helpers | CORRECTION | Adopted: E2R-R14A with the two-method example; test E2R-T13 |
| ADD-C07 NAMES-1 proof | CORRECTION | Adopted as requirements on the separate package (12A.5), plus the method-ID and folder-locator mapping (12A.1); the revision effect is to be decided explicitly in NAMES-1 |
| ADD-C08 the AND gate and release sequence | CORRECTION | Adopted: E2R-R57, E2R-R58; test E2R-T14 |
| ADD-C09 commit-independent retirement | CORRECTION | Adopted: E2R-R54..R56 (no commit IDs, no stored hashes, pre-installation byte comparison, no promise of replay); test E2R-T15 |
| ADD-C10 separate checkpoints | CORRECTION | Adopted: the three kinds of content (front matter), 12A.4, 13A |
| E2R-O01 a `MethodOutput` sketch | OPTIONAL | Adopted as a non-normative sketch (7.0) |
| E2R-O02 combination coverage | OPTIONAL | Adopted in E2R-T06 |
| E2R-REC01 prospective history view | RECONSIDER | Decided by the owner as D-8: both an "as published" view and a "current methods" view (E2R-R40B); the omitted-records disclosure is kept in E2R-R40A |

## Appendix B. Resolution of the focused recheck of v0.3r1

| Finding | Class | Resolution in v0.3r2 |
|---|---|---|
| F-B01 immutable declaration versus changing registry status | BLOCKER | Status, reason and texts moved out of the declaration into append-only `REGISTRY_ENTRY_V1` records (5.5, E2R-R21B/C). The declaration is immutable; release appends a `SUPPORTED` entry for the same declaration; the run request, receipts and terminal record pin the active entry digest; stale and mismatched digests are refused (E2R-R57); test E2R-T14 extended with the release transition |
| F-C01 interruption between freeze receipt and terminal record | CORRECTION | E2R-R38 limited to runs that complete the protocol; E2R-R38A defines the publication order, consumption only with a valid `SUCCESS` D2 plus all existing gates, quarantine of stray D1s, no automatic cleanup or termination, and no assumption that a failed process writes its own D2; test E2R-T16 extended |
| F-C02 compatibility exception too broad | CORRECTION | E2R-R14A: a successor revision is mandatory when the behaviourally relevant implementation changes, including through helpers; compatibility findings only for "not used" or "not relevant"; the NAMES-1 structural exception is scoped to that package; test E2R-T13 extended |
| F-C03 several publications for one target | CORRECTION | E2R-R40C: all publications retained with evidence; a predeclared official designation if one per target is shown; others counted; denominators stated; local times not proof; the mechanism is deferred to the FINAL specification; new test scenario E2R-T17 |
| F-C04 stochastic placeholder versus T08 | CORRECTION | A null `fit_seed_policy_id` is a legal placeholder for a non-`SUPPORTED` stochastic method; `SUPPORTED` requires a reviewed policy (5.1, E2R-R21C, E2R-R61); test E2R-T08 revised |
| Owner D-9, D-10 (not findings) | - | E2R-R63: NIST beacon root, one pulse per policy, switching roots as a new revision or variant, and every root tried logged and counted |

## Appendix C. Resolution of the second focused recheck (of v0.3r2)

| Finding | Class / disposition | Resolution in v0.3r3 |
|---|---|---|
| R2-F-C01 seed roots: time of availability, stages, reproducibility | CORRECTION / RECHECK | E2R-R63 now: the root is seed entropy, not data; three stages (announce the selection rule, retrieve by hand with independent verification against the public archive, approve into an immutable policy before `SUPPORTED`); no fallback pulse; null-policy declarations never edited (a new declaration under a new revision or variant); timing per owner decision D-11 (prospective: the root must already be approved; retrospective development: a later root allowed, labelled); reproducibility qualified to matched inputs and environment. New scenario test E2R-T18 |
| R2-F-C02 version label | CORRECTION / FIX AND PROCEED | The front-matter label is corrected. Because this edition is v0.3r3, the label reads `v0.3r3 DRAFT for focused recheck` rather than the `v0.3r2` text the finding specified for v0.3r2; the version sentence records both editions. The change is visible in the exact diff and is under this edition's RECHECK anyway |

*End of specification draft v0.3r3.*
