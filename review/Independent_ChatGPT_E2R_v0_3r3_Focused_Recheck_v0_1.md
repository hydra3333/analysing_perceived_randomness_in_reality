# E2R-1 v0.3r3 — independent ChatGPT focused design recheck

**Date:** 28 October 2026 (Adelaide)  
**Primary author:** Claude  
**Independent reviewer:** ChatGPT  
**Scope:** Only R2-F-C01 (normative seed-root chronology, identity and reproducibility), R2-F-C02 (version label), owner decision D-11, E2R-T18 and the necessary documentation of these changes. The original E2R architecture and previously closed findings are not reopened.  
**Verdict: PASS — 0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER.** Recommend presenting specification v0.3r3 to the project owner for ratification consideration. This review grants no execution or implementation authorisation.

## 1. Independent artifact verification

| Item | SHA-256 verified |
|---|---|
| `E2R_Spec_Recheck_v0_3r3.zip` | `d198966c04fd990fa58f8d41d226f786efbe04a3cb8fa68f9f534dc1f1cf6f6c` |
| `Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` | `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954` |
| `evidence/spec_v0_3r2_to_v0_3r3.diff` | `054f9517fe383d6acdca928f073934242fce9c8aecd5acb3786b782436bec7ec` |
| `evidence/make_v03r3.py` | `7f23a1302e9bd8d2bf15e61c721611f46d797ff193cbcd1634aada7e67cef9fa` |
| Retained v0.3r2 input specification | `2c69a9a8469ef1415b90d15e48d9de490310cfebe18d8be8694d0eb5483da115` |

I applied the supplied unified diff to the retained v0.3r2 file, on a disposable review copy, and reproduced the submitted v0.3r3 **byte-for-byte**. The resulting text is ASCII, LF, no CR, 81,859 bytes, and 772 lines. The ZIP contains the README, one specification, the diff, and the builder. I inspected but did **not** execute the builder; its claimed seven counted substitutions are consistent with its source and the diff but not separately execution-verified. This was a **document-only** patch replay, not a project test or scientific run.

## 2. Closure of R2-F-C01 — E2R-R63 (RECHECK)

**CLOSED — PASS.** The revision now provides all required normative distinctions:

1. **Input type:** NIST Beacon root is algorithmic seed entropy, not an observational draw-history covariate. The draw-data N−1 reader boundary and suffix invariance remain unchanged.
2. **Selection:** A provisional, non-runnable policy names the NIST Beacon version, chain, *exact* pulse by timestamp or index, and output field **before** the pulse exists; silent substitutions and fallback pulses are prohibited.
3. **Retrieval and verification:** The owner manually retrieves the selected published pulse, retaining its value and identifiers; a separate person checks it against the public NIST archive. No method run fetches a pulse.
4. **Approval and immutability:** Only a verified root can enter an approved immutable seed policy; a stochastic method cannot become `SUPPORTED` otherwise. Null-policy declarations are not edited to add a root; a new declaration, revision or variant is required according to the contract.
5. **Owner decision D-11:** A later-published root is permitted as **retrospective experiment randomisation**, explicitly not a historically available draw predictor. Genuine pre-draw prospective/FINAL forecasts require the root to have been retrieved, verified and approved **before forecast freeze**. Other prospectivity and FINAL gates remain in place. D-11 deliberately rejects the stronger rule that every historical target needs its own earlier pulse; that owner choice is preserved.
6. **Search multiplicity:** Changing a root requires a new policy ID and revision/variant; all prior trials remain preserved, logged and counted for each method, without limiting exploratory investigation.
7. **Reproducibility:** The text no longer promises identical output merely because the root is fixed; it conditions deterministic replay on matched inputs, configuration, environment and R2 §9.3 / E2R-T12 requirements.
8. **Acceptance:** New E2R-T18 explicitly tests synthetic policy stages, missing/wrong root refusal, historical versus prospective timing, root switches, retention and the stage-1 prohibition on a stochastic `SUPPORTED` entry. No actual pulse fetch is needed.

**Independent external context (no actual pulse retrieved):** NIST's 2.0 Beacon project description describes indexed, timestamped, signed, chained public pulses and published access by chain/pulse index or pulse time. This makes the specified exact-pulse selection meaningful: https://csrc.nist.gov/Projects/interoperable-randomness-beacons/beacon-20 . The service remains described by NIST as a *beta/prototype*; failure/no-pulse/no-fallback semantics are therefore important. A future implementation must reject any response for a different pulse (including a time-based endpoint returning a nearby pulse) rather than accepting it silently. This last point is already required by E2R-R63's exact-pulse/no-fallback clause and E2R-T18's mismatched-pulse refusal, so it is **not a new finding**.

**Implementation-stage observation, not a new finding or ratification condition:** The future seed-policy work should retain a checkable, dated copy of the provisional selection rule as evidence that it preceded pulse publication. That need not be a Git commit and does not reinstate commit-history dependencies, per-file hashes or runtime code attestation. This stage-1 specification already requires the prepublication selection rule; its eventual operational evidence format remains for the independently reviewed implementation/policy package.

## 3. Closure of R2-F-C02 — front-matter label (FIX AND PROCEED)

**CLOSED — PASS.** The title, version metadata, `OPEN` status sentence, chronology and concluding footer now consistently identify v0.3r3. The changed metadata correctly describes v0.3r2 as an earlier draft. The correction is visible in the exact diff and included within this focused RECHECK. No unreviewed discretionary change is apparent.

## 4. Owner authority, existing contracts and the next stage

- D-9, D-10 and D-11 are recorded as **owner decisions**; the other recommendations of the document remain **draft** pending owner ratification.
- The five record-family design, source-archive simplification without stored code hashes or historical Git commit IDs, current-only `src/`, registry AND marker gate, and separate owner-gated NAMES-1 package are unchanged by this revision.
- No change to the E_1 goldens, tie machinery, ranking, N−1 reader, process safety or result firewall is proposed or authorised.
- The stage-1 schema does not authorise stochastic `SUPPORTED` entries, NAMES-1 work, E2R implementation, a beacon fetch, scientific runs, unsealing, FINAL operations or release.
- No code was executed, no project tests or scientific runs were performed, and no lottery draws, holdout records, switches, allowlists, external beacon pulses or Git history were accessed or changed. The only execution performed was a local document diff replay and integrity hashing.

## 5. Review 4 of 6 — explicit REVIEWER-DECIDED determinations

Under the owner's extended oversight, this is a **focused continuation of E2R-1 review 4 of 6**, not the start of a separate design review 5. Earlier reviewer decisions E2R-RD-01 through RD-17 were reported and remain in force. New determinations:

| ID | REVIEWER-DECIDED determination | Reporting consequence |
|---|---|---|
| **E2R-RD-18** | Close **R2-F-C01** as PASS for the E2R design stage. E2R-R63 and E2R-T18 now implement the required temporal/identity distinctions, including owner D-11. | Normative fit-seed corrections have received the required **RECHECK**; no always-review waiver. |
| **E2R-RD-19** | Close **R2-F-C02** as PASS; version text is consistent and the change is included in the independently verified diff. | Earlier narrow FIX AND PROCEED corrected without expanding its authority. |
| **E2R-RD-20** | Issue **PASS** on E2R-1 v0.3r3 with **0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER**; recommend owner ratification consideration without another design-recheck round. | No code, tests, data, releases or gates are thereby authorised. |
| **E2R-RD-21** | Treat v0.3r3 as part of the same E2R-1 independent review **4 of 6**, preserving distinct reviews 5 and 6 for subsequent packages. | Claude should report the decision; monitoring is reporting-only and does not narrow reviewer rights. |

**Departures from ratified safety, scientific, compliance or process rules:** None identified or authorised by this focused review. The owner remains sole ratifier and execution authoriser.

## 6. Final recommendation

**PASS E2R-1 specification v0.3r3 for owner ratification consideration.** The full specification remains a draft until the owner ratifies it, and downstream implementation stages remain individually gated. No additional E2R design revision is requested on the basis of the reviewed changes.

*End of focused independent review.*
