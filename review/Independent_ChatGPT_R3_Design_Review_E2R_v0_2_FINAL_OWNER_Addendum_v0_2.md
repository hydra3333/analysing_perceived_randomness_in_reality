# Independent ChatGPT R-3 design review — E2R-1 v0.2 plus FINAL owner addendum

**Date:** 28 October 2026 (Australia/Adelaide)  
**Author/reviewer:** Claude primary designer / ChatGPT independent reviewer  
**Scope:** The supplied E2R-1 v0.2 *design specification only*, assessed against installed R2 v0.5, R3 v0.5, Architecture v0.8 and the owner-ratified TIE_SHA256_V1 v0.2. No implementation or execution approval.  
**Base represented in handback:** `be185485693f29cf9ab28292dc6eebad00bbc32c`  
**Submitted ZIP SHA-256 (verified):** `e5860b7f02827a4539c8da3510e244f1bf54b3af93f3d5f5064df93780ebfeee`  
**Spec SHA-256 (verified):** `4254128d20a3f9fa3a7d65658bcca99e8f72045145b1514d570b3c4f21ebc4a4`  
**Status:** HIGH-tier R-3 design-stage review **including the FINAL owner addendum of 28 October, superseding the preceding addendum**. **NOT READY for owner ratification without resolution of the BLOCKERs.**  
**Findings (final consolidated):** **3 BLOCKER / 10 CORRECTION / 2 OPTIONAL / 1 RECONSIDER.** Original v0.2 findings: 3/5/2/1; FINAL addendum findings: 0/5/0/0. Withdrawn interim proposals/findings are documented as superseded, **not** counted.  
**Execution:** No project code, unit tests, scientific experiments, Windows lifecycle commands, lottery-result searches or holdout access. Review was static analysis of supplied documents, the relayed addendum and local authoritative copies. The authoritative R2/R3/Architecture copies have full SHA-256 identities matching the E2R handback's source identities.

**Addendum source status:** Both the interim and the FINAL owner addenda were relayed as messages. Neither changes the verified v0.2 specification bytes; neither has a separate source file or hash. The FINAL addendum expressly **WITHDRAWS** items 1 and 2 of the earlier addendum and **REPLACES** them with A–C. The owner retains item 3 (NAMES-1 before E_2-readiness coding). All proposal references indicate future v0.3 integration locations, not already-written v0.3 text.

## Assessment and competing design

The five-family separation is a strong architectural starting point: the method sees a prefix-only view and limited task; orchestration retains file/snapshot provenance; evaluator outputs are separate. The method-computes/contract-assembles principle, unchanged legacy E_1 golden identities, per-channel declarations and explicit record vocabularies should be **retained**. They reduce B1-style metadata leakage and make eventual tests precise.

I recommend **retaining the five families but making family C a typed output union**, rather than prescribing numerical marginal scores to every method. Define the families' temporal scopes explicitly: a pre-target WF/synthetic forecast; a separately future-defined IS diagnostic (not a forecast); an immutable successful freeze receipt; and a separate terminal/failure record for unsuccessful runs. This is a bounded correction to the present design, not a proposal to replace the repository's architecture or add runtime scope.

## BLOCKER findings — design must change before ratification

### E2R-B01 — Ranking-only and diagnostic-only methods cannot be faithfully represented

**Locations:** spec lines 42–43 (E2R-R07), 125–135 (5.2), 188–240 (7.1–7.4), 364–372 (11.1). **Authority:** R2 v0.5 section 5.1 `MAIN_RANK` / `POWERBALL_RANK` explicitly allows native scores **when available**; `DIAGNOSTIC_SIGNAL` is a legitimate typed output; R2-C10 forbids fabricating a score/ranking to satisfy an interface. The owner's “mark, never suppress” rule is operative.

`FULL_RANKING` currently entails scores for **every** label, while `score_type: NONE` entails **no** ranking. A real complete ranking without underlying numerical scores therefore cannot pass validation without invented data. In parallel, `DIAGNOSTIC_ONLY` has a status but no declared payload for a genuine numerical diagnostic or intermediate signal. R07's list of permissible method outputs excludes diagnostics. It would silently lose legitimate speculative method products.

**Required replacement/design text:**

> A method output is a discriminated typed payload. `FULL_RANKING_WITH_SCORES` contains a complete order and lawful native scores; `FULL_RANKING_ORDER_ONLY` contains a genuine complete order without fabricated numeric scores; `NATIVE_SET` contains a declared legal joint TOP even without a marginal ranking; and `DIAGNOSTIC_SIGNAL` preserves the declared typed diagnostic output without fabricating tickets. A method may legitimately produce more than one capability, under an explicit versioned schema. Ranking-only records must state how native ties, if any, are represented; the tie validator may not infer unrecorded scores or ties. Fields requiring unavailable scores/rankings are absent or explicitly unavailable, with reasons. `DIAGNOSTIC_ONLY` preserves typed diagnostics in a separately versioned and firewalled scientific-output record, not merely a status. No output is a prediction/evidence claim without its applicable reviewed mapping.

Claude may choose different precise enum names. Acceptance condition is that ranking-only, joint-set-only and diagnostic-only cases are representable without fabrication, and `ranking_digest`/`tie_groups` have explicit conditional rules when there is no native score vector.

**Disposition:** RECHECK. New normative schema/capability design affects TOP/WORST and the always-review area.

### E2R-B02 — In-sample work conflicts with the mandatory pre-target forecast schema

**Locations:** lines 37, 60, 176–182, 188–208, 259–269, 315–332, 369–370 and E2R-T06 at 416. **Authority:** R2 v0.5 section 8.4 explicitly fits the IS state on `H(L+1)` (including the targets later scored); R3 17.3.5 distinguishes IS from WF; the N-1 requirement governs *forecasts* for N.

The draft associates `IN_SAMPLE_DIAGNOSTIC` with `IS_DIAGNOSTIC_ENTRY`, but also puts `run_mode` into the single pre-target `METHOD_FORECAST_V1` schema and specifies one `DrawView` containing only `<N` and content that is suffix-invariant. An authentic IS diagnostic for target N can have a fit depending on N..L. It cannot simultaneously obey the forecast record's N-1/content-invariance rule. The first substantive IS implementation would either violate this schema or silently misrepresent IS as WF. Stage 1 authorises **only an IS capability declaration**, not an IS engine.

**Required replacement/design text:**

> `METHOD_FORECAST_V1` is exclusively a pre-target prediction contract. Its permitted input digest and N-1 invariant apply to WF and any appropriate synthetic prefix-only forecasting test. `IN_SAMPLE_DIAGNOSTIC` is not produced by this schema in Stage 1. `IS_capability` is declarative only. A later, separately reviewed IS fit/apply schema must explicitly identify the full-fit cutoff L, fitted-parameter digest, allowed H(N) recent-state inputs, and IS namespace, and must prohibit treatment as a pre-target forecast or scientific WF evidence. Listing an IS mode in a future vocabulary does not authorise constructing an IS record now.

Adjust the legal-combination table and tests to distinguish **reserved future combinations** from schema types that Stage 1 can actually produce. Benchmark timing products likewise must not be forced into `METHOD_FORECAST_V1` (see C05).

**Disposition:** RECHECK. Required to protect N-1 and the IS firewall.

### E2R-B03 — Immutable freeze receipt cannot simultaneously carry post-score and failed-run state

**Locations:** lines 275–295 (8.1), 315–333 (9), 338–355 (10); especially R36, R38 and R41. **Authority:** R2 5.6 fields 5–7; R2 8.2A and R3's freeze-before-score/firewall obligations.

D is described as one receipt **per valid frozen forecast**, create-only, written after validation, with `outcome_opened_at_freeze: false`. Yet it carries `score_status` and permits `SCORED`, a state that can occur only **later**. Updating D would violate its immutability; marking it SCORED at freeze would be false. Separately R38 states that a failed run has a D receipt with no forecast digest, contrary to D being one per valid forecast and written only after its file is frozen. Failure provenance still needs its own durable status, but it is not a successful freeze receipt.

**Required replacement/design text:**

> `FORECAST_FREEZE_RECEIPT_V1` is an immutable receipt issued **only after** a valid forecast is frozen, with recorded status and evidence available *at freeze time*. It is never rewritten to say `SCORED`. A later evaluator's create-only post-outcome record supplies scoring state; report-level `SCORED` is derived by a validated join to that record. Failed/invalid/orphan-suspected runs publish their existing separately firewalled orchestration terminal/failure evidence (or a separately named terminal-receipt schema), without issuing a successful forecast-freeze receipt. Neither failure evidence nor an orphan-suspected file is a consumable forecast.

If `score_status` remains in the D schema, restrict it at freeze to an explicitly defined pre-scoring value, and define `NEVER_SCORED` for non-scientific outputs. Explain that `SCORED` is legal only in the derived post-score view, never the immutable D document.

**Disposition:** RECHECK. This is a provenance and scientific result-consumer firewall issue.

## CORRECTION findings

### E2R-C01 — Stochastic seed/configuration fields are not sufficient to implement the proposed identity

**Locations:** lines 110–119, 165–182, 200–201, 259–269. The seed tuple cites `fitting_config_digest`, `external_input_digest`, and implicitly a root/entropy policy, but the declaration/request/task tables do not define their creation, admission, or identity. R2 9.2's illustrative tuple includes a root seed, namespace and fit/selection model configuration. A `SeedSequence` mapping from digest bytes to a typed sequence of integers is likewise not yet specified. The pointer in line 201 incorrectly says `section 6.5` (actual section **7.6**).

**Suggested replacement:**

> The Stage-1 declaration reserves a versioned `fit_seed_policy_id` and declares stochastic capability only. Before the first stochastic method is implemented, its separately reviewed specification must define the owner-declared root seed/policy, configuration digest, admitted external-input digest and pre-target cutoff, exact length-prefixed canonical tuple, and portable conversion of the resulting digest into `SeedSequence` entropy words. The reviewer verifies that every component is outcome-independent for target N and suffix-invariant. The method task receives only those reviewed pre-target seed inputs necessary for fitting. No unreviewed default, process/run ID or master SHA may fill a missing field.

If the precise 7.6 formula is retained as normative now, add all its input fields and their construction in the declaration, run request and method task, and make the `SeedSequence` word order explicit. Correct the line-201 section reference to 7.6.

**Disposition:** RECHECK: fit seeds are always-review.

### E2R-C02 — Reproducibility identity claim is too broad

**Location:** line 208, E2R-R26. “Two runs that see the same permitted prefix produce byte-identical records” omits differences in method revision, variant, allowed configuration, declared run mode, stochastic root/seed and output policy; all affect legitimate record fields.

**Replacement sentence:**

> For the **same** game, target, method/variant/revision, allowed observation view, declared configuration, seed policy, run/product mode and implementation environment, changing only target-and-later master bytes cannot change any method-visible field or the canonical forecast bytes/digest. Runs with different declared pre-target configurations may legitimately produce different content identities.

**Disposition:** RECHECK in the E2R design revision because it defines the N-1 invariant.

### E2R-C03 — Revision-free tracks need unique, create-only score-record keys

**Locations:** lines 298–305 (R40/R40A), 338–354 (post-outcome schema). D-1 legitimately excludes revision from `track_id`, and re-runs never overwrite older records. But “one per track per scored target” is ambiguous when two revisions, or two runs of a revision, have frozen evidence for the same track and target. `method_revision` is absent from the post-outcome table, although forecast/receipt digests appear.

**Replacement text:**

> A post-outcome record identifies its `method_revision` and the **specific immutable forecast and freeze receipt** that were scored. Its create-only key includes the track, target, revision, forecast-content digest, freeze-receipt digest and evaluator version (or an equivalent collision-free immutable receipt identity). A second valid re-run adds distinct evidence and never overwrites or silently displaces the earlier score record. A report states the frozen revision/receipt selection policy and its resulting target cohort.

**Disposition:** RECHECK. This fixes a collision/lineage ambiguity; owner D-1 stays binding.

### E2R-C04 — TIE identity and the barrel ranking digest need a complete conditional definition

**Locations:** lines 216–230. `tie_identity` lists the common tuple information but does not explicitly say the **label** is added individually for each tie-key, as required by TIE_SHA256_V1's exact eight-field encoding; `ranking_digest` hashes only `{scores, ranking, tie_version}`, without a stated canonical schema for the no-score or no-ranking cases. The frozen overall content digest covers the larger context, so this is an avoidable ambiguity rather than evidence of a broken accepted golden.

**Replacement text:**

> `tie_identity` identifies the exact ratified seven shared fields; for each tied label j the validator appends the **eighth field, j**, with the prescribed uint32 little-endian length-prefixed UTF-8 encoding, then sorts by ascending SHA-256 (numeric-label collision fallback). `ranking_digest` is a versioned, canonical, barrel-scoped digest of the actually available ranking fields and tie policy; its exact keys, scores-absent encoding and absent-ranking behaviour are specified here. A ranking that does not exist has no fabricated digest or tie groups.

**Disposition:** RECHECK as it concerns tie/readout semantics.

### E2R-C05 — Distinguish benchmark evidence from a forecast artefact, and scope worker determinism

**Locations:** lines 309–334, E2R-T06 (416) and E2R-T12 (422). The mode table properly labels benchmarks `NOT_EVIDENCE`, but should clarify that a timing-only benchmark need not produce a `METHOD_FORECAST_V1` scientific forecast or freeze receipt. Additionally “across one and six workers (synthetic, in-process)” does not by itself verify the ordinary multi-process coordinator's Windows behaviour.

**Replacement text:**

> `BENCHMARK_*` permits only timing/technical evidence and no scientific forecast-freeze receipt or post-outcome scoring; a timing-only execution need not satisfy `METHOD_FORECAST_V1`. Stage-1 E2R-T12 proves repeatability within the explicitly identified synthetic offline executor and its tested concurrency settings; it does not claim operational Windows coordinator or protected-process acceptance. Those remain separately gated.

**Disposition:** RECHECK if changes affect the mode-family matrix; purely explanatory test-scope wording can be FIX AND PROCEED only when specifically assigned later.

## OPTIONAL findings

### E2R-O01 — Define an explicit method-return protocol independent from the frozen forecast schema

**Locations:** R07 (43), sections 6–7. The recommended method/contract split is sound. It would become easier to implement and test if the document names an internal, disposable `MethodOutput` type, carrying a **typed** payload and no identities, and leaves all identity assembly/freeze to the contract. This can be a non-normative sketch now; do not implement beyond Stage 1. **Disposition:** OPTIONAL, RECHECK if adopted as a normative schema change.

### E2R-O02 — Record case counts for the legal-combination matrix

**Locations:** section 9 and E2R-T06. In addition to rejecting every forbidden tuple, document the intended coverage of each allowed row, including synthetic benchmark and reserved IS cases, rather than relying on an unspecified “every combination” enumeration. **Disposition:** OPTIONAL, FIX AND PROCEED if confined to a clearly non-normative testing note; any test-logic change requires RECHECK.

## RECONSIDER (nonblocking; owner decision remains binding)

### E2R-REC01 — Does the default “latest revision” view inadvertently hide historic prospective evidence?

**Location:** E2R-R40A, lines 300–305. D-1 has been explicitly owner-decided: `track_id` excludes revision; each report uses a declared revision per track; superseded/prospective records are permanent. I **do not** reverse or suspend that decision.

A potential consequence deserves the owner's consideration: if revision 1 was actually published prospectively for earlier targets and revision 2 only for later targets, a default “latest revision” report may omit revision-1 prospective evidence from its headline series. That does not delete it from the archive but can make the displayed prospective record selectively incomplete. A side-by-side request is possible, but may not be the natural view of the cumulative prospective history.

**Suggested owner question:** Should the ordinary *prospective-history report* additionally offer a separate, labelled “as genuinely frozen at each target” chronology (with explicit revision per target), while the single-revision-per-track rule remains binding for revision-comparison and development league tables? This would be a separately named longitudinal display, not a silent mixing of revision results into one model's evidence. If the owner rejects this exception, retain D-1 unchanged and ensure the default report plainly discloses the omitted earlier revisions and their count.

**Disposition:** RECONSIDER; nonblocking by itself and requiring an explicit owner decision before policy change.

## Safety, scope and R-3 conclusions

- No approved code, E_1 golden, tie encoding, scientific result allowlist, coordinator protection or holdout rule is modified by this review.
- The owner's 28 October decisions D-1 (revision-free `track_id`), D-2 (`NOT_EVIDENCE`) and D-3 (method descriptions) remain binding. Only E2R-REC01 invites a separately decided refinement.
- A new contract field/schema is **not** permission to run IS, Mode H, FINAL, scientific scoring, new real-data evaluation, source acquisition or Windows lifecycle tests.
- Stage-1 acceptance remains synthetic/development-prefix only. The current source is inspected statically; no project code/test run was conducted here.
- The disposition rules are followed: proposed changes affecting the eight always-review subjects (N-1, seeds, TOP/WORST/ties, firewall) all require **RECHECK**, never FIX AND PROCEED. Other purely documentary non-normative changes may receive FIX AND PROCEED only through an explicit later reviewer finding.

## REVIEWER-DECIDED register — review 4 of 6

| ID | Decision | Oversight reporting |
|---|---|---|
| `E2R-RD-01` | Maintain HIGH-tier status, demand resolution of B01–B03 before owner ratification, and classify the response as a targeted design RECHECK rather than source-code review. | Report to project owner; no departure from ratified rule by making this decision. |
| `E2R-RD-02` | Preserve the five-family architectural direction while recommending a typed output union; do **not** accept fabricated ranking scores or suppression of diagnostic outputs. | Report; this addresses R2's existing contract. |
| `E2R-RD-03` | Apply the absolute RECHECK rule to all revised N-1, tie/readout, seed and firewall contracts; no FIX AND PROCEED for those corrections. | Report; no departure. |
| `E2R-RD-04` | Treat E2R-REC01 as **RECONSIDER, nonblocking**, leaving owner D-1 intact until expressly changed. | Report; no unilateral policy change. |

## FINAL owner addendum — current sources, Git-based retirement, two release gates, and NAMES-1

**Owner-relayed final decision (28 October 2026):** The earlier proposed `implementation_files` path-to-SHA map, `code_commit` in every freeze receipt, pre-run source-file hash verification, per-method source-locking scheme, duplicated copies of all helpers in each method archive, and post-commit retirement receipt **are WITHDRAWN**. Do **not** carry their requirements, fields, tests or associated findings forward to E2R v0.3 by inertia. The earlier interim addendum's `ADD-B04`, `ADD-B05`, `ADD-C06`, `ADD-C09`, `ADD-O03`, and `ADD-REC02` as originally worded are **superseded**, not unresolved current findings. This final review **reuses** `ADD-C06` through `ADD-C10` for *rewritten* findings against the owner's final A–C design. No new schema requirement for code hashes or per-run code-commit recording is authorised or recommended.

The FINAL proposal is:

- **A — Current sources only:** active code lives under `src/`, in per-method directories with stable, unversioned names, e.g. `src/methods/E_002/`.
- **B — Retirement in the successor package:** move a superseded method revision to `archive/methods/<E_n>/r<k>/`; a superseded shared-helper revision goes to `archive/common/<name>/r<k>/`. The archive README states revision, retirement date, shared helpers used, and **the last Git commit where the revision was current**, i.e. the *parent commit*. The install verifier proves archived bytes equal the prior current bytes. Archives are off every normal import path, and a static rule forbids imports from `archive/`. An exact historical rerun is a separate owner-authorised checkout of the recorded historical commit.
- **C — Two independent release gates:** a method/variant can run under the normal coordinator or standalone runner only when its reviewed registry status is **SUPPORTED** **and** `src/methods/<E_n>/IN_DEVELOPMENT.txt` is absent. The marker only blocks; its deletion does not confer SUPPORT in the registry. Both entry points refuse with an informative warning while the marker is present. Owner release deliberately removes the marker and approves the registry transition. All existing scientific/operational gates continue independently.
- **Item 3 retained:** a separately packaged, HIGH-tier **NAMES-1** one-off rename before E_2-readiness code, including reader/coordinator imports. The owner has reaffirmed this sequencing. No RECONSIDER on whether NAMES-1 should exist or precede E_2 code is raised in this final review.

### Assessment of A–C

**Support, with bounded corrections.** This is considerably simpler than the discarded per-file attestation scheme and meets the owner's **repository-management** intent. It makes Git history and immutable method-revision discipline the source-of-truth for historical code. It avoids inadvertently placing code identity in `declaration_digest` or the canonical forecast-content digest; it also avoids the same-commit-hash paradox by naming the **parent** Git commit.

**Important assurance boundary:** `method_revision` plus Git history can identify the *approved historical implementation* **only if** the project enforces a one-to-one version/revision lifecycle. They do **not**, without runtime code-identity capture, independently prove the bytes a particular process actually imported during a run, nor protect against out-of-band edits. That is an explicit tradeoff of the owner's simplified design, not a defect to 'fix' by restoring rejected hash fields. Claims in v0.3 must distinguish **repository-level reconstructibility** from **runtime binary attestation**. The normal no-status/no-kill rules, holdout controls, source-data restrictions and result firewall remain intact.

### ADD-C06 — Make `method_revision` meaningful when sources or shared helpers change

**Classification:** CORRECTION. **Disposition:** RECHECK (scientific identity, seed/forecast and possible TOP/WORST consequences).

**Owner addendum:** A/B and traceability sentence. **Spec locations:** E2R-R14/R21 (§4–5), E2R-R49–R52 (§12), and any new §12 archive rules.

The statement “traceability is by `method_revision` in every record, the archive README and Git history” relies on a lifecycle invariant not fully specified in v0.2: a method can execute different code under the **same** revision if its entry-point code or a common helper is changed without retiring the dependent method revision. The revision alone would then fail to distinguish historical implementations. R14 already requires a revision when the method implementation changes, but does not state the shared-helper propagation boundary.

**Required replacement:**

> Each approved runnable method/variant revision denotes one fixed reviewed implementation *including the behaviourally relevant shared-helper revisions on which it depends*. A change to an approved method specification or implementation—including an affected behaviourally relevant shared-helper revision—must trigger the existing R2/R14 revision rule and a reviewed successor/compatibility decision for each **affected runnable dependent method**, even if that method's entry point is byte-unchanged. Do not silently reuse a declared revision following an implementation change merely by asserting unchanged outputs. An unchanged helper does not force a revision bump merely because an unrelated method is retired. `FORMULA_OPEN` and `UNSUPPORTED_FOR_GAME` entries need not acquire invented runnable implementations. The reviewer/owner acceptance package verifies the code transition from the recorded parent Git tree, registry/declaration revisions and each affected historical archive README. Results keep `method_revision` but neither source paths, per-file hashes nor run-time code-commit fields enter the declaration or forecast-content digest.

Also identify the scope of “behaviourally relevant”: in-repository imported helpers and other owned runtime dependencies used in computation, selection, encoding and method-facing data preparation, including shared code. This is **package-time provenance/release governance**, not a proposed run-time source-hashing or identity-recording mechanism. Where a helper changes for two active dependent methods, provide an explicit two-method successor example. If the owner knowingly accepts a revision-only record without guaranteeing one-code-version-per-revision, the spec must say that precise implementation attribution for a past run is **not** guaranteed; the reviewer recommends the lifecycle invariant instead.

### ADD-C07 — Strengthen the separate NAMES-1 acceptance proof, without changing the owner's sequencing

**Classification:** CORRECTION. **Disposition:** RECHECK; mandatory for reader and coordinator changes on the always-review list.

**Owner addendum:** standing item 3. **Spec locations:** migration notes (§12) and the Stage-1 boundary (§13); full proof belongs in the future owner-scoped NAMES-1 task/spec, **not** the E2R schema.

The originally proposed AST equality “apart from imports,” identical ASTs for eleven protected functions, and E_1 golden reproduction are useful, but not conclusive for import-path changes. Altering module paths affects import origins, Python module identity, package-relative resolution, `__file__`/`__module__`, plugin/CLI launch, references in wrappers/tests, and Windows path behaviour. Distinguish method-ID (`E_2`) from the *folder locator* (`E_002`) with one documented stable mapping; do not silently make a zero-padded directory name a scientific identity.

**Required NAMES-1 acceptance/evidence:** complete old/new path map and import/reference graph; exact source moves and hashes as mechanical evidence **in the package**, not runtime contract fields; AST comparisons for bodies other than permitted import changes; **all eleven protected function ASTs structurally unchanged**, including the coordinator's protected functions; import-origin, standalone invocation, dynamic/module-name references and Windows CMD wrapper tests; E_1 legacy goldens and allowed prefix-only/view regressions; unchanged three safety switches and empty scientific-result allowlist; owner-run Windows acceptance as well as Linux offline evidence; rollback procedure and clear isolation from later E2R coding. All permitted checks must remain within their existing authorisations. NAMES-1 must also explicitly decide how import-only implementation changes affect `method_revision` under R2 5.3/E2R-R14; unchanged numeric E_1 goldens do not, by themselves, prove that a new source implementation may reuse its prior revision identifier. The owner decides the NAMES-1 implementation start separately; approval of E2R's specification is not execution authority for that migration.

### ADD-C08 — Specify the AND gate, registry revision, and safe release sequence

**Classification:** CORRECTION. **Disposition:** RECHECK (method dispatch and protective release gating).

**Owner addendum:** C. **Spec locations:** declaration `registry_status` (§5), run admission (§6), the mode table (§9), not-applicable handling (§11), and acceptance tests (§13).

C's AND rule is coherent and is stronger than the marker alone. Make it explicit that **each requested game/method/variant/revision** must be approved by the reviewed registry and the active current source selected for that revision; an approval for a previously retired revision is not approval for a new one. Failure of either condition denies dispatch *before method data is read*. `FORMULA_OPEN` and `UNSUPPORTED_FOR_GAME` are never transformed into SUPPORTED by deleting a file. Both standalone and coordinator must implement identical refusal semantics. A warning must identify the method and reason without printing sensitive or method-ineligible inputs.

**Required replacement:**

> A normal method dispatch requires: (i) an exactly matching **SUPPORTED** approved registry declaration for the selected game/method/variant/current revision, (ii) absence of the per-method `IN_DEVELOPMENT.txt`, and (iii) success of all already applicable independent safety, environment, data-admission and owner-authorisation gates. A missing, stale, or non-SUPPORTED registry entry is deny-by-default. A present development marker is always deny. Every blocked request is refused **before any method data access**. Neither a flag deletion nor a registry change alone grants authorisation for a scientific run. Both standalone and coordinator report the refusal.

**Release controls:** the successor package must begin in a **non-runnable** state (reviewed registry not yet SUPPORTING the successor and/or marker present); owner-approved release deliberately performs *both* actions. The order must never accidentally make an unaccepted successor runnable, including during intermediate installation states; retain the existing owner execution gates. Since the marker is a conventional file, this is an **application-level dispatch safeguard**, not an OS-level access-control or anti-tamper guarantee. A directly invoked Python module is not magically prevented from executing simply by the presence of the marker.

**Proposed tests, not run here:** truth table (SUPPORTED/other × flag present/absent), missing or stale registry, retired-vs-current revision mismatch, both launch paths, abort-before-read, report/refusal text, and no bypass of existing gates. These tests must be designed for authorised synthetic/offline fixtures, without opening any real scientific-result path.

### ADD-C09 — Define verifiable retirement, shared-helper archives and historical reruns

**Classification:** CORRECTION. **Disposition:** RECHECK where sources, dispatch or scientific provenance are affected.

**Owner addendum:** B. **Spec locations:** §12 versioning/migration and a new acceptance-test note in §13.

**Accepted:** the README may name the **parent commit**, so the self-referential commit problem from the *withdrawn* addendum no longer exists. No post-commit retirement receipt is needed. The owner deliberately selects Git history rather than copying all current helper bytes into every method archive. This means an exact historical replay obtains the *complete matching historical tree* by checking out the cited parent commit, not by importing a retired method alongside today's active helpers.

**Required archival rules:**

> At retirement, the package moves the exact bytes of the outgoing method to `archive/methods/<E_n>/r<k>/` (and a superseded common-helper revision to `archive/common/<name>/r<k>/` when that helper itself is replaced). The archive README identifies retired revision, retirement date, prior current path, the **last commit where it was current (the installation parent)**, and the shared helpers and versions used. The read-only verifier compares every moved source byte against the exact parent-commit blob and confirms that the old active path is no longer present. The archive is excluded from all normal import/search/dispatch paths; a static import check rejects repository imports from it. Unchanged helpers that are still current are not retired merely because one dependent method changes. Historical replay is a distinct, owner-authorised checkout of the cited complete commit and does not automatically become a normal run or change historical records.

The README itself is descriptive metadata and may differ from the old source; verify source-byte movement independently from README creation. The “parent commit” assumes a controlled clean baseline and one owner-installed successor commit; if a preparation/snapshot commit intervenes, refer to the actual **last Git commit in which that revision was current**, verified by source history, rather than guessing. Define relative-path naming, case handling, unique revision directory allocation, `__init__.py`/package traversal and the current/archived helper mapping in the installation proof, particularly for Windows. Do not permit an `archive/` import through an indirect loader or a normal registry selection.

**Scope statement:** Excluding archives from `PYTHONPATH` plus static tests is a useful **normal workflow** control but not proof that arbitrary readable `.py` files cannot be executed directly. The actual guarantee should be “normal reviewed runners never dispatch archived revisions”; historic manual replay is separately owner approved.

### ADD-C10 — Preserve owner-controlled sequencing and distinct work packages

**Classification:** CORRECTION. **Disposition:** RECHECK for consequential NAMES-1/reader/coordinator work.

**Owner addendum:** retained item 3, and A–C. **Spec locations:** scope (§1), migration (§12), owner decision summary (§14).

The owner has **affirmed** NAMES-1 before E2R coding. Record this faithfully as owner direction, not an unresolved alternative or permission for Claude to begin. Keep separate authorisation and acceptance checkpoints:

1. This E2R v0.3 **design-stage** resolution and owner decision on its contracts.
2. A separate HIGH-tier NAMES-1 design, independent reviewer assessment, explicit owner execution authorisation, exact reviewed whole-file moves/import updates, Linux and Windows verification, and owner-controlled Git installation.
3. Later E2R Stage-1 code work, separately scoped and authorised by the owner.

The reviewer is **not reopening** the owner's choice of sequence. A bounded NAMES-1 migration remains HIGH because import changes touch always-review reader/coordinator subjects, regardless of superficial AST similarity. No ratified R2/R3/Architecture text is silently rewritten by this prospective proposal.

## Proposed v0.3 acceptance additions (spec/test design only)

- **E2R-T13 — Revision continuity and shared helper rollover:** in synthetic model identities, a changed behaviourally relevant shared helper causes successor revision declarations for all dependent runnable methods; unaffected methods keep their revision. Future records carry the correct revision; no source paths, per-file code hashes, or run-time commit identity enter declaration or forecast-content bytes. Include a negative that an obsolete approved registry entry cannot authorise newly installed code under a different revision.
- **E2R-T14 — Development marker and registry AND truth table:** all combinations of SUPPORTED/non-SUPPORTED and marker present/absent, including stale/missing registry and both launchers, refuse before data read unless all independent gates are satisfied. Show both deliberate owner release actions without exposing outcomes or enabling real runs.
- **E2R-T15 — Retirement proof and archive exclusion:** on a disposable synthetic Git fixture or read-only Git test repository, verifier matches outgoing source bytes to the actual last-current parent commit, checks path removal and README/helper mapping, and rejects a normal import/dispatch to archives. No runtime source-code hash attestation or post-commit receipt is introduced.
- **NAMES-T01+ (separate future authorised package):** inventory/import graph, unchanged protected ASTs, E_1 goldens, Windows CMD wrappers and Python direct launches, registry+marker admission, safety switches and allowlist. These are **not** implicit permission to begin migration.

**Preserve** existing E2R-T01..T12, subject to corrections from the original v0.2 review. In particular, the original always-review requirements for N-1 isolation, readout/ties, seed identity and the result firewall remain unaltered.

## Original findings that remain open; findings withdrawn or closed

- **Still open:** `E2R-B01`–`B03`; `E2R-C01`–`C05`; `E2R-O01`–`O02`; `E2R-REC01`. A–C do not repair the ranking-only/diagnostic-only schema, the IS temporal conflict, or the freeze receipt lifecycle inconsistency.
- **WITHDRAWN / superseded from interim addendum:** old `ADD-B04` and `ADD-B05` (code-hash/declaration leak, retirement-commit self-reference); old transitive code-hash runtime-lock proposal; runtime `code_commit` fields and their dependent tests; old duplicate-helper-archive suggestion; old `ADD-REC02` asking the owner to reconsider the NAMES-1 sequence. They are **not open findings** and are **not counted**. The predecessor review's `E2R-RD-05`–`RD-08` descriptions are likewise superseded by the updated four decisions below.
- **Accepted in principle:** A (only current code in `src/`), B (Git parent provenance and byte-verified retirement archives), C (registry **AND** development-marker blocking). The owner decides the design; this review requires the bounded clarifications above before accepting v0.3's normative wording.

**FINAL combined counts:** **3 BLOCKER / 10 CORRECTION / 2 OPTIONAL / 1 RECONSIDER.** Five corrections in the final A–C review are **not** the discarded five corrections from the earlier addendum; they are newly scoped against the owner's replacement design.

## Updated REVIEWER-DECIDED register — review 4 of 6

The original `E2R-RD-01`–`E2R-RD-04` in the earlier section of this document remain effective. The four decisions below **replace** the interim addendum's earlier, never-forwarded `E2R-RD-05`–`RD-08` descriptions. This remains **one** review 4, not review 5.

| ID | Independent reviewer decision | Required owner reporting |
|---|---|---|
| `E2R-RD-05` | Accept the owner's withdrawal of runtime code-identity/hashing proposals; close interim `ADD-B04/B05` and related tests. Preserve existing forecast-digest and N-1 invariants. | Report; no deviation from ratified rules. |
| `E2R-RD-06` | Support Git-parent/README provenance and source-byte-preserving retirement subject to `ADD-C06/C09`; do **not** require a post-commit receipt or content-addressed helper archive. | Report; distinguish approved-history traceability from runtime-byte attestation. |
| `E2R-RD-07` | Accept the two-condition SUPPORTED **AND** no-development-marker proposal subject to `ADD-C08`; require both launchers' fail-closed handling and existing independent owner/scientific gates. | Report; no gate opened by this review. |
| `E2R-RD-08` | Treat the owner's NAMES-1 sequencing preference as **affirmed**, close interim `ADD-REC02`, and require a separately scoped HIGH-tier NAMES-1 with mandatory RECHECK for reader/coordinator changes and Windows verification. | Report; owner choice respected and always-review restriction enforced. |

No RECHECK decision concerning the eight standing always-review subjects is eligible for FIX AND PROCEED. No deviation from governing process/safety/scientific restrictions is identified or authorised. All **eight** `E2R-RD-01..08` are to be relayed to the owner under the extended oversight instruction.

## Consolidated next handback to Claude

Prepare **one revised E2R v0.3** from v0.2 (not separate ratified addenda), with a mechanical exact diff and complete SHA-256, responding to the original 3 blockers, 5 corrections and 2 optionals plus the FINAL A–C design corrections. Retain `E2R-REC01` as an owner RECONSIDER question unless independently decided; do **not** re-raise the now-affirmed NAMES-1 sequencing as a reconsideration question.

The v0.3 document should distinguish clearly: (1) current/future E2R schema duties, (2) source-tree/archive/revision and release **policy** that may be specified now but not implemented here, and (3) future owner-scoped NAMES-1 and E2R Stage-1 execution/test authorisations. Cite the owner's withdrawal of interim hash/commit fields, keep all source paths/code-byte fingerprints outside forecast identities, and state the deliberate limits of revision+Git-history provenance. Do **not** restore the cancelled per-run `code_commit`, `implementation_files` or source-hash preflight scheme.

No project source edits, NAMES-1 work, code runs, scientific experiments, holdout reads, source acquisition, operational gate changes, or Git commits are authorised by this document review.

*End of FINAL consolidated E2R-1 independent R-3 design review.*
