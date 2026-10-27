# E2R-1 v0.3r2 — independent ChatGPT focused design recheck

**Review date:** 28 October 2026 (Adelaide)  
**Author:** Claude, primary designer/coder  
**Reviewer:** ChatGPT, independent R-3 design reviewer  
**Scope:** The five findings against E2R v0.3r1 (F-B01, F-C01..F-C04), plus the new owner decisions D-9/D-10 in E2R-R63. Specification and document evidence only.  
**Verdict:** **REVISIONS REQUIRED — 0 BLOCKER / 2 CORRECTION / 0 OPTIONAL / 0 RECONSIDER.** One normative seed-policy correction requires **RECHECK**; one non-normative version-label correction is **FIX AND PROCEED**. This is a focused continuation of the already counted E2R review 4 of 6, not a separate design package review 5.

## 1. Mechanical identity and scope

- Submitted `E2R_Spec_Recheck_v0_3r2.zip` SHA-256: **`39f3aa96ab2329cb9d074e6f03841d3b6ec3e9f9ec646fce3dc776f2afb37429`** — verified.
- Specification `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r2.md` SHA-256: **`2c69a9a8469ef1415b90d15e48d9de490310cfebe18d8be8694d0eb5483da115`** — verified (ASCII, LF, 754 lines).
- Supplied exact diff `evidence/spec_v0_3r1_to_v0_3r2.diff` SHA-256: **`ebd2e6eedfbbe66c5fce0095086ed7e838a4ead8c92148361a2ce4a792097f15`** — verified. Applied as a unified patch with zero fuzz to retained v0.3r1 SHA-256 `7211f4c9d6f8e51a83629e68d03c9fe2d7593acca11a1b904ec75123dde5dbd0`; result reproduced v0.3r2 **byte-for-byte**.
- Builder `evidence/make_v03r2.py` SHA-256 `c739382470af6459d8c1caa4bc5645b2f63769aa310ce7b08d5b0d4da388752c` — hash verified; its claimed 32 replacements were **not independently executed**. The supplied diff and final bytes were independently reconciled instead.
- Source consulted for the substantive seed boundary: owner-ratified R2 v0.5, I-05 and §9.2, and R3 v0.5 §0.4. For NIST beacon mechanics, NIST's official v2.0 service description documents a time-indexed, signed, chained, public pulse, including access by timestamp or chain/pulse index: https://csrc.nist.gov/Projects/interoperable-randomness-beacons/beacon-20 . These references were consulted without obtaining any particular pulse or accessing lottery outcomes.

No project code was executed, no project tests or scientific runs were performed, and no holdout, lottery outcome, source-data file, switch, process, Git history or allowlist was accessed or modified.

## 2. Disposition of all five prior findings

| Prior finding | v0.3r2 response | Recheck result |
|---|---|---|
| **F-B01** — declaration immutable vs changing registry status | §§5.1, 5.5, 12A.3 and E2R-T14 separate immutable scientific `METHOD_DECLARATION_V1` from append-only administrative `REGISTRY_ENTRY_V1`; active digest pinned in request/receipts/terminal, and old records retained | **CLOSED — PASS.** Changing `FORMULA_OPEN` to `SUPPORTED` for an accepted declaration does not mutate its scientific identity or circumvent the flag/registry/owner gates. |
| **F-C01** — interrupted output/receipt before SUCCESS terminal | E2R-R38/R38A and T16 require a valid `SUCCESS` D2 with matching receipts/outputs and unchanged group/firewall gates; stray D1 remains quarantined without cleanup/killing | **CLOSED — PASS.** Does not imply that a crashed method creates a terminal record; an absent D2 is non-consumable. |
| **F-C02** — broad helper compatibility exception | E2R-R14A and T13 mandate successor method revisions for actual behaviourally relevant changes; the only permitted compatibility findings are genuinely unused/irrelevant changes, plus separately scoped NAMES-1 migration | **CLOSED — PASS.** No source hashes or Git-history requirements introduced. |
| **F-C03** — multiple pre-draw publications | E2R-R40C and T17 preserve all publications and evidence, require pre-outcome official designation if one forecast per track/target is reported, disclose denominators, and defer FINAL implementation | **CLOSED — PASS for stage-1 design.** D-8's two reporting views remain binding. |
| **F-C04** — stochastic placeholder contradictory to T08 | §§5.1, 5.5, 7.6, T08 distinguish null seed-policy placeholders on non-`SUPPORTED` stochastic declarations from admission requiring a reviewed policy; stage 1 still supports no stochastic methods | **CLOSED — PASS**, subject only to the **new owner D-9/D-10 seed-root clarification** below. |

The v0.3r2 changes do not reopen any of the original 16 consolidated design findings. The five-family architecture, current-only source tree, commit-independent archives, deliberate release AND-gate, unchanged E_1 goldens, and separately gated NAMES-1 are retained. Neither owner decision D-9 nor D-10 authorises stochastic method implementation or execution.

## 3. New focused findings

### R2-F-C01 — E2R-R63 needs a temporal/identity distinction for NIST beacon roots

**Class:** CORRECTION. **Disposition:** **RECHECK** (normative fit-seed contract; always-review subject).  
**Location:** v0.3r2 §7.6, **E2R-R63**, particularly its *Source* and *Switching* bullets (spec lines 364–368); read with E2R-R61 (lines 351–363), R2 v0.5 I-05 and §9.2, and E2R-T08.

**Failure scenario:** The owner pre-announces a beacon pulse in October 2026, fetches its value once after publication, and uses it as the fixed fitting root for a *retrospective* walk-forward experiment targeting a draw from an earlier year. This may be legitimate **retrospective algorithmic randomisation** if the full series of roots tried and the experiment's hindsight are declared. But the root was **not available before the historical target**, so it must not be described as a historically available external covariate or proof of a genuinely pre-target forecast. R2 §9.2 requires a stable, outcome-independent pre-target fit configuration and pre-target admission of external features; R63 currently does not distinguish a randomisation choice made for a retrospective experiment from a time-available predictor input. Conversely, a genuinely prospective forecast must fail closed if its declared pulse was not yet published, was unavailable or was substituted after selection. A root chosen following observation of retrospective results also creates method-selection multiplicity, which D-10 correctly asks to count; it cannot retrospectively improve the evidential status of those records.

**Required bounded clarification (without changing D-9 or D-10):**

1. Define the beacon value as an **external source of algorithmic seed entropy**, *not* as an observational draw-history covariate. The policy identifies the beacon version/service, exactly which pulse is selected by a rule fixed **before the pulse**, which value/field becomes the root, and how that value is durably recorded and checked. No latest-available, next-best or silent fallback pulse.
2. For **genuine prospective/FINAL** forecasts, require that the selected value was actually published, manually fetched, verified and frozen **before that forecast's pre-outcome freeze**. If unavailable, refuse or record failure; never fetch during a run. The separate FINAL gates remain closed.
3. For **retrospective historical WF development**, permit a later-published root *only if explicitly described as a retrospective, pre-experiment randomisation choice*, not a historically available external predictor input. Preserve N−1 draw-data isolation and all target/suffix tests; label, preserve and count root trials and tuning/selection honestly. Do not imply that a pulse published after historical draw N was available when N originally occurred. If the owner instead intends the stronger condition that the pulse must predate **each historical target**, say so explicitly, and apply it consistently. This is a policy choice for owner acceptance, not one the reviewer silently makes.
4. Clarify the two-stage process: preannounce the *pulse-selection rule* before the pulse exists, then bind its actual published value into the reviewed immutable seed policy **before the method is `SUPPORTED`**. Distinguish a provisional, non-runnable policy from a reviewed usable policy; no mutable policy ID that silently changes an already supported fit identity. If the immutable declaration originally has a null `fit_seed_policy_id`, moving to a reviewed non-null policy requires a new declaration and, where E2R-R21 demands it, a successor scientific revision; **do not edit the old declaration in place**. The future first stochastic-method specification fixes the exact derivation, word ordering, and verification procedure.
5. Retain D-10: each root change obtains a new policy ID and method revision or variant, with all prior roots/results and attempt counts retained; no retroactive overwrite.

**Acceptance evidence:** a specification-level scenario for a not-yet-published selected pulse, a correct manual retrieval, a missing/incorrect pulse, a historical target predating the root, and a new root/revision attempt. Show that no stochastic `SUPPORTED` record can be created in stage 1 and that a genuinely prospective forecast never uses an unpublished pulse. This may be an extension of E2R-T08 or a separately numbered future seed-policy scenario. **No actual beacon fetch, historical run or owner-gate change is requested.**

**Reproducibility qualification within this finding:** The R63 statement that a fixed root and derivation make *every run exactly reproducible* is too broad standing alone. Reproducibility also depends on fixed method/configuration, admissible view, platform/numerical environment, and the later seed-derivation implementation; retain R2 §9.3 and E2R-T12's matched-environment byte-identity standard. Change the sentence to say the root and derivation **make deterministic replay possible under the separately specified matched inputs/environment and validation requirements**, not an unconditional promise.

This correction resolves a temporal and wording boundary; it does **not** reject NIST, constrain how many roots the owner may investigate, or seek per-file hashes, Git provenance or runtime attestation.

### R2-F-C02 — Front-matter edition typo

**Class:** CORRECTION. **Disposition:** **FIX AND PROCEED** (non-normative, exact replacement).  
**Location:** v0.3r2 line 4, version metadata.  
**Issue:** The title correctly names `v0.3r2`, but the **Version** metadata begins `v0.3r1 DRAFT for focused recheck`.  
**Exact replacement:** Change that opening substring only to `v0.3r2 DRAFT for focused recheck`. No other part of the chronology needs revision for this finding. Retain exact diff and updated file SHA-256 for the next handback. If more than this specified substring is changed under this disposition, return it for RECHECK.

## 4. Review 4-of-6 oversight: explicit REVIEWER-DECIDED record

The current E2R-1 iteration remains a **focused continuation of review 4 of 6**; it does not consume review 5. Previously reported E2R-RD-01 through E2R-RD-13 remain in force. The following new decisions must also be reported to the owner by Claude:

| ID | REVIEWER-DECIDED determination | Reporting consequence |
|---|---|---|
| **E2R-RD-14** | Close F-B01 and F-C01–F-C04 as substantively resolved for the current stage-1 design. | No remaining original recheck blocker/correction; retain HIGH tier and downstream gates. |
| **E2R-RD-15** | Require normative **RECHECK** of R63's historical/prospective time-of-availability, policy finalisation, and bounded reproducibility semantics (R2-F-C01). | No relaxation of N−1, seed identity, or real/prospective admission; owner decisions D-9/D-10 remain binding. |
| **E2R-RD-16** | Assign **FIX AND PROCEED** solely to the exact non-normative v0.3r2 front-matter version-label correction (R2-F-C02). | Claude retains exact diff/hash; no separate reviewer round for that one change. |
| **E2R-RD-17** | Count v0.3r2 as a continuation of E2R-1 **review 4**, not independent package review 5. | Existing owner oversight is preserved for later distinct reviews 5 and 6. |

**Departure from ratified rules:** None authorised. The need to distinguish beacon-root chronology from external-feature availability is a request to clarify, not an allegation that any actual run has violated N−1. The owner retains sole ratification and execution approval. Every seed-related normative change comes back for RECHECK.

## 5. Recommendation and bounded next step

Claude should prepare a narrowly changed v0.3r3 addressing **R2-F-C01** and applying the exact **R2-F-C02** text correction. Supply the exact v0.3r2→v0.3r3 diff, revised SHA-256 and short response matrix. Do not revisit the five closed findings or reopen the eight-subject always-review list. If the temporal interpretation requires a new owner decision, present the two explicit historical-root options to the owner before calling the schema ratified.

**Verdict: REVISIONS REQUIRED — 0 BLOCKER / 2 CORRECTION (one RECHECK, one FIX AND PROCEED).**

*End of independent focused review.*
