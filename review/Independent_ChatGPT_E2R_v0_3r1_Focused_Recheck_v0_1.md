# Independent ChatGPT focused recheck — E2R-1 v0.3r1

**Date:** 28 October 2026 (Adelaide)  
**Reviewer:** ChatGPT, independent R-3 design reviewer  
**Author:** Claude, primary designer/coder  
**Scope:** E2R method-generic contract *specification only*. This is a **focused continuation of E2R review 4 of 6**, not a distinct new package review.  
**Disposition:** **REVISIONS REQUIRED — 1 BLOCKER, 4 CORRECTION, 0 OPTIONAL, 0 RECONSIDER**. All five findings: **RECHECK**, not FIX AND PROCEED. No execution, code-installation or scientific permission is conferred.

## 1. Integrity and scope of the handback

- Submitted `E2R_Spec_Recheck_v0_3r1.zip` SHA-256 **`a395277c978b09181b9a8e8b524a2cfa60cf679d29088470d9eddf5154042980`** — VERIFIED.
- `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r1.md` SHA-256 **`7211f4c9d6f8e51a83629e68d03c9fe2d7593acca11a1b904ec75123dde5dbd0`** — VERIFIED; ASCII/LF, 691 lines.
- `evidence/spec_v0_2_to_v0_3r1.diff` SHA-256 **`04b45be7850ec66d91059119120dd88bcad863f05d2d9108885d5a132782b782`** — VERIFIED. The supplied unified diff applies cleanly to the independently retained v0.2 file (SHA-256 `4254128d20a3f9fa3a7d65658bcca99e8f72045145b1514d570b3c4f21ebc4a4`) and produces the byte-identical submitted v0.3r1 document. This tests the *effect* of the diff, rather than assuming identical diff-tool hunk formatting.
- ZIP contents: specification, README and exact diff only; no source-code changes. Governing references inspected locally: R2 v0.5 §5.3 and §5.6, R3 v0.5 §§2.3–2.4, 3.6 and prospective-publication requirements, Architecture v0.8, TIE_SHA256_V1 v0.2, and the previously issued consolidated review `17087f57…b2b2`.
- No scientific run, project test, numerical fitting, source-data reading, Git mutation, holdout use, process-management action or Windows acceptance was performed. Local document-hash/diff checks are not project acceptance tests.

## 2. Previous findings — focused recheck assessment

The 16 findings in the original consolidated review have **substantive design responses**, with Appendix A supplying a traceable map. Key progress:

- **B01 substantially resolved:** scored, order-only and absent ranking capabilities; native weak-order groups; conditional tie/ranking digests; separate typed diagnostic C2 and no invented scores. `E2R-R15A`, §§7.0–7.7 and tests T01/T04/T07 provide a coherent implementation target.
- **B02 resolved:** C1 is explicitly pre-target only (`E2R-R25A`); in-sample fitting and records remain separately gated and unimplemented, with the reserved-mode matrix visible.
- **B03 structurally resolved, but one lifecycle edge remains:** frozen forecast receipt no longer stores scoring state, and D2 terminal record is separate. A possible freeze-then-failure/interruption path is not yet fully reconciled (finding F-C01 below).
- **C01–C05:** the new seed-policy deferral, scoped determinism, create-only score key, eight-field tie encoding and ranking digest, and benchmark exclusion answer the core concerns. The frozen `TIE_SHA256_V1` tuple is preserved; E_1 goldens are explicitly left unchanged.
- **ADD-C06–C10:** current-only `src/`, no durable source hashes or commit-ID dependencies, revision-labelled archives, pre-install outgoing-byte comparisons, marker/registry AND gate, and NAMES-1's separate HIGH-tier checkpoint are accurately carried forward. No withdrawn per-file hashing or runtime code-attestation proposal has reappeared.
- **O01–O02:** typed return sketch and combination test coverage are incorporated.
- **REC01:** the owner decided D-8: distinct “as published” and “current methods” views. The reviewer's reconsideration is closed. The publication policy needs a bounded multi-publication edge clarification (F-C03).

There is **no proposal here to replace the five-family architecture or reconsider the owner's commit-independent archive, release-gate or NAMES-1 decisions**.

## 3. Findings requiring correction

### F-B01 — Immutable declaration identity conflicts with changing registry status

**Class:** BLOCKER. **Disposition:** RECHECK.  
**Exact location:** §5.1 (`registry_status` in `METHOD_DECLARATION_V1`; “One declaration exists per `(game_id, method_id, variant_id, method_revision)`”); §5.4 `E2R-R19` and `R21` (static declaration whose canonical digest is quoted by method records); §12A.3 `E2R-R57/R58` (registry changed during a two-action release).

**Failure scenario:** A pre-release E_2 r1 declaration says `FORMULA_OPEN`, with declaration digest A. The owner's separate release package changes its status to `SUPPORTED` **without changing the approved scientific implementation/revision**, giving canonical declaration digest B. Overwriting A breaks immutability and historical audit. Keeping A and B breaks the rule “one declaration exists per [four-field identity]” unless their distinct, create-only administrative identities are specified. Forcing an E_2 r2 merely because a registry flag changed confuses administrative admission with scientific revision.

**Required remedy:** Specify the relationship among immutable declaration snapshots, the currently operative registry entry and the admission gate. A bounded implementation consistent with the owner's choices is: retain each published declaration snapshot create-only and digest-addressed; permit successive administrative snapshots for the *same* scientific revision (only one active at a time); have the current registry refer to the active accepted declaration digest; and pin that digest in the run request. A release may change administrative status/digest without silently rewriting old records or forcing a scientific revision. Alternatively Claude may propose a comparably precise separation that still satisfies ratified R2 §5.6's status-and-reason requirement. Explicitly define which statuses can have forecast records and which historical declarations remain readable.

**Acceptance:** Add a synthetic transition test to E2R-T14 covering pre-release declaration A, approved release declaration B, absence of overwrite, old-record validity, correct current dispatch, and refusal of mismatched/stale registry digests. Document and check the release transition without enabling any real run.

### F-C01 — Terminal-record and freeze-receipt failure edge is overstated

**Class:** CORRECTION. **Disposition:** RECHECK.  
**Exact location:** §§8.1–8.3 (`E2R-R36`, `R38`); E2R-T16.

**Failure scenario:** A valid forecast file and freeze receipt can be created, followed by a crash, timeout, orphan suspicion or failure before a successful terminal record is durably committed. The current text says both “every admitted run ends with” a terminal record and “a failed run ... never gets a freeze receipt.” Neither is an unconditional physical guarantee after interruption. Claiming it could cause a consumer to regard a stray D1 as proof of success, or pressure cleanup/termination contrary to the no-status/no-kill rule.

**Required remedy:** Say every run **that completes the terminal-publication protocol** must have one create-only D2, while an absent/invalid/incomplete D2 is conclusively **not successful** and is non-consumable. A valid successful D2 with matching D1 (or matching diagnostic receipt where appropriate), together with all pre-existing group/firewall gates, is necessary for consumption. Any D1 left by an interrupted/non-successful run stays preserved/quarantined, **never counts as an accepted freeze**, and does not induce automatic killing or cleanup. Preserve the existing orphan-marker interlock; do not assume the failed process can write its own D2. State the receipt/terminal publication order and the recovery semantics without weakening the owner safety controls.

**Acceptance:** E2R-T16 includes a simulated interruption **after writing D1 but before publishing SUCCESS D2**, an absent-D2 case, and an orphan-suspected group; all must be non-consumable even with valid-looking forecast files/receipts. No actual process killing or destructive fault injection is authorised by this specification review.

### F-C02 — Shared-helper revision compatibility exception is too broad

**Class:** CORRECTION. **Disposition:** RECHECK.  
**Exact location:** `E2R-R14A` §4 and its example; §§12A.2 and 12A.5; E2R-T13.

**Failure scenario:** E_2 r1 and E_3 r1 use helper H r1. H's arithmetic changes in r2; the draft permits either successor method revisions **or a “reviewed compatibility decision”** for each. If that exemption preserves method r1 despite a behaviourally relevant implementation change, the historical E_2 r1 identity can describe two different computations. The existing R2 §5.3 revision principle says the method revision changes when its specification or implementation changes.

**Required remedy:** Make a successor method revision mandatory whenever the method's **behaviourally relevant implementation actually changes**, including transitive helper arithmetic/selection/encoding/view-preparation changes. A documented compatibility finding may establish that a helper is *not* used or is *not* behaviourally relevant for a particular unaffected method; it must not excuse a known change to that method's implementation. Keep NAMES-1's separately reviewed purely structural import/path migration as its expressly scoped decision (without silently treating it as general immunity for future substantive helper changes). No source hashes or commit identity need be added.

**Acceptance:** E2R-T13 fails a changed arithmetic helper with an unchanged dependent revision, even when a narrow fixture happens to yield the same numbers; it permits unchanged revisions for genuinely unaffected methods and separately recognises the approved NAMES-1 structural exception.

### F-C03 — “As published” needs a multiple-publication and proof rule

**Class:** CORRECTION. **Disposition:** RECHECK for this normative prospective-history rule; no prospective implementation is authorised now.  
**Exact location:** `E2R-R40A/R40B` §8.4 and the owner D-8 text in §14.

**Failure scenario:** Two different genuine forecasts/revisions may be frozen and **published before the same target draw**. “For each target, the forecast that was actually ... published” is singular and does not identify which publication appears in an “as published” series. Choosing whichever later performed better would violate the owner’s mark-never-suppress rule and R3's anti-selection provisions. Also `frozen_at_utc` alone is not externally verifiable evidence of timely publication (R3 prospective evidence requirements); later Git-history cleanup must not retrospectively invalidate the retained source archive, but cannot be taken as a substitute for independent publication evidence either.

**Required remedy:** State that **all** genuine before-draw published attempts stay visible in an immutable publication/audit history with revision and publication evidence. If the scientific “as published” series reports *one* official forecast per track/target, require a predeclared immutable selection rule/official-batch designation **before observing the outcome**, and separately count other publications/attempts and unverified publication timestamps. If it instead lists multiple rows, totals must identify the publication denominator and not falsely count several attempts at one target as independent target outcomes. A later independently reviewed FINAL/publication specification may define the exact mechanism; this stage-1 contract must not silently assume uniqueness or equate a local timestamp with proof.

**Acceptance:** Add a specification-level test scenario with two timely published candidate revisions for one target, one designated official before the draw, and one late/unverified candidate. Verify all are retained and labelled, while per-track performance selection is not decided after outcome access. Preserve D-8's owner-chosen two-view structure.

### F-C04 — Stochastic placeholder declarations contradict the stage-1 test

**Class:** CORRECTION. **Disposition:** RECHECK (fit seeds are an always-review subject).  
**Exact location:** §5.1 (`stochastic_fit`, `fit_seed_policy_id`); §7.6 `E2R-R61`; E2R-T08.

**Failure scenario:** The field table requires a **non-null** seed policy ID whenever `stochastic_fit` is true. Stage 1 has no seed policy yet, accepts no stochastic method as `SUPPORTED`, and T08 demands a **null** `fit_seed_policy_id` in *every* declaration, including non-runnable `FORMULA_OPEN` declarations. A declared future stochastic method cannot satisfy the schema and T08 simultaneously without being falsely labelled deterministic or given a fictional reviewed policy.

**Required remedy:** Define a legal non-runnable seed-policy-placeholder state separately from a reviewed usable seed policy, without pretending a seed is available. For example, permit a null seed-policy ID for an **unspecified/unimplemented** `FORMULA_OPEN` stochastic method while requiring a reviewed non-null policy before `SUPPORTED`; or define a precise tri-state capability and its versioned migration rule. Do not use an unreviewed default or enable stochastic fits in stage 1. Revise T08 to assert that all *SUPPORTED stage-1* declarations have null seed-policy IDs and are deterministic, while properly typed non-runnable placeholders remain legal.

**Acceptance:** Synthetic declaration tests exercise a valid reserved stochastic placeholder, reject a `SUPPORTED` stochastic declaration lacking its reviewed policy, and verify the stage-1 no-stochastic-execution rule.

## 4. Reviewer decisions — owner oversight

**Accounting:** This is the focused **recheck of the same E2R-1 design package reviewed as review 4 of 6**. I elect to treat it as a continuation of **review 4**, not consume a separate slot 5. The owner's instruction to explicitly list *every* REVIEWER-DECIDED action remains operative for subsequent independent package reviews 5 and 6. Previously transmitted `E2R-RD-01..08` remain recorded; these new decisions are additional, not replacements.

| ID | REVIEWER-DECIDED action | Reporting to the project owner |
|---|---|---|
| `E2R-RD-09` | Accept the substantive B01 (ranking/diagnostics) and B02 (IS separation) redesigns for this design stage; keep the five-family architecture. | Report: no deviation. |
| `E2R-RD-10` | Treat the immutable-declaration/registry transition as a **new design BLOCKER** until a deterministic create-only status lifecycle is specified. | Report: RECHECK; no owner release gate opened. |
| `E2R-RD-11` | Require focused RECHECK of interrupted-run D1/D2 consumability and shared-helper revision discipline (F-C01/C02). | Report: safety/identity boundaries protected. |
| `E2R-RD-12` | Accept owner D-8 and close original REC01, with a focused publication-count/proof correction (F-C03) and seed-placeholder consistency (F-C04); do not reopen the owner's two-view choice. | Report: prospective controls remain closed. |
| `E2R-RD-13` | Count this focused revision as **continuation of review 4**, not a new fifth independent package review. | Report oversight accounting; reviewer rights unchanged. |

No deviation from ratified science, safety, compliance or owner-authorisation rules is proposed or approved. Relevant always-review areas (N−1, tie/readout, revisions and safety/firewall) require RECHECK. The owner alone ratifies and authorises execution, release and commits.

## 5. Recommendation to Claude and owner

Prepare a *targeted* v0.3r2 (or next appropriately named draft), changing only the affected sections, Appendix A as needed, and the corresponding acceptance scenarios. Supply the exact v0.3r1-to-revised diff, updated SHA-256 and a concise response matrix. The original 16 findings do **not** need to be reviewed from scratch; the remaining contract-level corrections are enumerated here. No NAMES-1 work, code implementation, runs, source acquisitions, holdout actions, dependency operations, switch/allowlist changes or Git changes are authorised by this review.

**Verdict: REVISIONS REQUIRED.**

*End of independent focused recheck.*
