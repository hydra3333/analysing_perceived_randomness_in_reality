# DOC-2 — Independent ChatGPT HIGH-tier review of Register v0.7 candidate

**Date:** 28 October 2026 (Adelaide). **Package:** `DOC2_Register_v0_7_Review_v1.zip`. **Author:** Claude. **Reviewer:** ChatGPT. **Scope:** the normative status/authority record only. **No scientific or execution authority granted.**

## Verdict

**REVISIONS REQUIRED before owner ratification: 0 BLOCKER / 2 CORRECTION / 1 OPTIONAL / 0 RECONSIDER.** Both corrections are narrowly bounded documentary changes. This is the fifth distinct review under the extended 4–6 reviewer-oversight arrangement. Their HIGH-tier authority-document nature warrants **RECHECK** (at least a targeted documentary/diff check); the owner may decide the appropriate scope but has not granted an exception.

## Independently checked evidence

- Submitted ZIP SHA-256 **PASS**: `d70d8ce5fff6b10b26ebc012ef95a65885ec9bc7d3c356440450d96aededea2b`.
- Candidate register SHA-256 **PASS**: `92e73afba1f7cdb55f38959df67c01d5312f4bc4d50ab3fce6ab1b26f89ce4b1`; UTF-8/LF.
- Supplied five-hunk exact diff **PASS**: `7e00bc93cd64273ec37d91ce82abac6967d056858bbd93758e20b789ba57cd10`.
- **Predecessor authenticity and complete diff independently reproduced:** reverse-applied the supplied patch to candidate v0.7 and obtained SHA-256 `5e677dce3f2ae01cd7a3f6cc1ff408c8e32e268150fe0c956e42bf703a9b074c`, identical to Git-stored v0.6. Ran `tools/make_register_v07.py` against those reconstructed predecessor bytes; produced candidate bytes **identical** to the supplied file.
- Checked GitHub commits `be185485693f29cf9ab28292dc6eebad00bbc32c` (DOC-1), `319fd11` (review archive), `38fc60e03ea0766f72476cbab7c0e1eb5bd59d07` (checkpoint/interim review). No source changes were made.
- Independently matched the E2R-1 v0.3r3 specification SHA-256 `0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954` to the file in the earlier supplied spec ZIP. Its **owner ratification date**, however, remains a finalisation field, not independently established by reading Git history.

## Findings

### DOC2-C01 — CORRECTION — RECHECK — NAMES-1 does not implement the folder rule

**Location:** register v0.7's new **Out-of-date statements** section, first bullet: “Architecture v0.8, 'one standalone `.py` per method': extended by D-4 (a folder per method). **NAMES-1 puts it into practice**, and the next Architecture edition folds it in.”

**Failure scenario:** The simultaneously submitted NAMES-1 §4/N1-R05 explicitly proposes *no* per-method folder creation or movement of E_1; it keeps executable entry files flat under `src/methods/` and postpones any new `E_<nnn>/` layout. If the register already declares NAMES-1 implements D-4's folder rule, a later reader may mistakenly treat OPEN-N1 as decided or assume per-method folders actually exist after NAMES-1.

**Required replacement:** “Architecture v0.8's standalone `.py` wording is extended by owner decision D-4. NAMES-1 proposes stable filename renaming only, without implementing per-method folders; its exact entry-file/folder layout is subject to the owner's separate OPEN-N1 decision. The next Architecture edition will incorporate the settled layout.” Preserve D-4's existing authority and do not pre-ratify the NAMES-1 alternative through DOC-2.

### DOC2-C02 — CORRECTION — RECHECK — Clarify verification baseline, new artifact exception

**Location:** register v0.7 **Basis** paragraph: “the v0.7 entries [were cross-checked] against GitHub HEAD `38fc60e`”. README says the as-yet-uninstalled E2R-1 specification is an exception. The unqualified register statement could be read as a claim that the proposed specification is committed at that snapshot.

**Failure scenario:** A cold-start reviewer attempting to retrieve `doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md` at `38fc60e` will not find it, despite the register claiming the v0.7 entries were checked there.

**Required replacement:** Qualify the final clause along these lines: “The already-committed v0.7 references were cross-checked against GitHub commit `38fc60e` (28 October 2026); the E2R-1 v0.3r3 specification is not yet present at that commit and is independently verified by its ratified-package content hash, with installation subject to the owner's separate decision.” No change to E2R status or hashes.

### DOC2-O01 — OPTIONAL — Wording for oversight-reporting transition

**Location:** new **Process decisions** paragraph, now describing review reporting *by exception*. Earlier owner communications required Claude to send every REVIEWER-DECIDED item; the submitted candidate documents a subsequent owner decision to check every item but forward only disagreement or matters of owner interest. **No independent contradiction is established if the owner made this later decision.** For an unambiguous audit trail, state explicitly that this is a *newer* owner instruction superseding the earlier all-items-to-owner reporting requirement. The reviewer still enumerates every decision; Claude still inspects all; the authority cannot be delegated. As a substantive reporting-policy update, the owner's explicit acceptance at DOC-2 ratification should be retained.

## Checked, accepted without findings

- Current status of H-1 v1r2, H-2 v1r3 and register v0.6; the documentary E2R-1 review history and the available hashes.
- D-1 through D-11 summaries at the level appropriate to a register, including no Git commit or persistent file hash requirement in retirement archives and **no** automatic permission to run anything.
- The register's separation of *owner ratification* from *software implementation/installation/release*.
- The 28 October Git-history-cleanup possibility is a statement about later repository administration, not an E2R dependency.
- R2 v0.5 §6.2's older registry-field language is naturally implemented by the newer E2R scientific-declaration / append-only registry-entry separation; no additional contradiction has been established requiring a register erratum now.

## REVIEWER-DECIDED — fifth review, list all

- **DOC2-RD-01:** Treat DOC-2 as HIGH-tier normative review; accept reproduced baseline, diff and candidate identities.
- **DOC2-RD-02:** Require DOC2-C01 correction and narrowly focused RECHECK; do not allow a proposed NAMES-1 deviation to acquire authority via register wording.
- **DOC2-RD-03:** Require DOC2-C02 verification-scope correction and narrowly focused RECHECK.
- **DOC2-RD-04:** Keep DOC2-O01 nonblocking and explicitly defer any change to owner reporting obligations to the owner's ratified decision. Reviewer independent rights unchanged.

No departure from scientific or safety controls is authorised. Do not finalise placeholders or mark OWNER-RATIFIED absent the owner's dated decision. The draft's file-content SHA changes when placeholders or corrections are finalised; record the **final** hash.

**Disposition:** Claude should prepare a corrected register candidate with precise diff, hash and evidence; the owner makes the final ratification/installation decisions. **No scientific runs, source changes, holdout access, switch operations or Git writes were performed in this review.**
