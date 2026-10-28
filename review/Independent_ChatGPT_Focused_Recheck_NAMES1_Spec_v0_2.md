# NAMES-1 — Independent ChatGPT focused HIGH-tier R-3 RECHECK of specification v0.2

**Date:** 28 October 2026 (Adelaide). **Author:** Claude. **Reviewer:** ChatGPT. **Source:** `NAMES1_Spec_Recheck_v0_2.zip`. **Scope:** the previously raised N1-C01..C04, N1-O01 and N1-REC01, their associated proof and owner choices. **Design only:** no rename, installation, execution or scientific permission is conveyed.

## Verdict

**PASS — 0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER remaining within this focused recheck.** The NAMES-1 v0.2 design is suitable for owner ratification consideration with the separately communicated **OPEN-N1 = A, OPEN-N2 = defer, OPEN-N3 = accept** choices. The future code/overlay package is a **separate HIGH-tier implementation**, and because it changes always-review reader and coordinator code, its actual source diff requires independent **RECHECK** regardless of size.

## Independent evidence checks

| Item | SHA-256 / observation |
|---|---|
| Uploaded ZIP | `fddf24f147406038653673e49350a7737b97c518849e46fc8c7b178d06b442a6` — matched |
| v0.2 spec | `07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a` — matched |
| Reviewed v0.1 spec | `88379b2800f0b660242ece361178eff7c0a2ebc70c68a83916cb187d1fa9dce5` — matched earlier provided ZIP |
| Exact v0.1-to-v0.2 patch | `304768c45377698c5db73f4d85bdaede42a1464c39f551f9ce383f46c983625b` — matched, successfully applied to v0.1, reproducing v0.2 byte-for-byte |
| `allowlist.tsv` | `2074f152b52f0adadd581546ef704341962cffe0c2d00a4d59d8301e1a3c315f` — matched; 94 sites across 27 edited files |
| Author's static/negative evidence | `negative_checks_output.txt` records 94 PASS checks; `t02_check_output.txt` records allowlisted equality; these are **author-side logs**, not independent re-execution by ChatGPT |
| Author's Linux test evidence | Nine per-module counts: 10+6+11+18+6+7+2+13+6 = **79**, unchanged before/after; zero reported Linux skips. **Windows tests were not run in this review** |

The mapping covers 18 runtime modules and 9 test modules. The allowlist classifies **82 normal imports, 2 mock-patch strings, 3 issuer-origin sites, 2 contract-file hash-key names, 2 source-read literals, 2 forbidden reader-import checks and 1 docstring** (94 total). I inspected the allowlist-building and verification scripts, the reported mutation outcomes, and the relevant reader-firewall and exit-receipt source at the stated Git commit. The present review does not certify the future installed tree or assert that the supplied logs were independently reproduced.

## Disposition by finding

**N1-C01 — CLOSED, PASS.** N1-R01A, N1-R01B, §5A and N1-T02/T05A explicitly distinguish textual substitutions needed to preserve active import and safety intent from unchanged scientific identity. The two negative firewall assertions now reject imports of the **renamed** reader; the mutation control demonstrates why leaving the old reader literal would be unsafe. The literal changes are not misdescribed as unchanged test text. N1-T02 constrains changes to an exact categorised 94-site allowlist.

**N1-C02 — CLOSED, PASS at design stage.** N1-T09 now mandates the complete **79-test** applicable Windows suite, broken down by all nine modules and their counts; symlink skips are possibilities, not an assumed result. Unexpected skips, failed cases or changed counts stop installation. No destructive Windows/process tests are authorised by the design. The author's successful 79-test Linux trial is informative but **not** Windows acceptance evidence.

**N1-C03 — CLOSED, PASS at design stage.** N1-T01/T05/T05A add live-file and wrapper-reference checks, absence of old paths, new-name import origins checked using a fresh isolated interpreter, issuer-origin refusal controls, and negative firewall mutations. Historical `review/` and `doc/` files are explicitly exempt. The documented file scan is a text check, not a generic semantic analyser; the complete future overlay must still satisfy the exact, read-only install verifier.

**N1-C04 — CLOSED, PASS.** N1-T10 now qualifies `git revert` as a **one-time immediate recovery demonstration** in a disposable clone while the introducing commit is available. It is not a permanent rollback or historical-replay guarantee if the owner later rewrites Git history.

**N1-O01 — CLOSED, PASS.** The owner tools, historical tests and data-acquisition utilities remain out of NAMES-1; their disposition is optional and owner-scoped. They are not automatically labelled obsolete, imported or executed.

**N1-REC01 — CLOSED by owner choice.** The owner explicitly selected **OPEN-N1 = A**: executable method entry files remain flat in `src/methods/`, with method-specific modules/flags in `src/methods/E_<nnn>/`. The owner deferred OPEN-N2 and accepted OPEN-N3. These decisions were transmitted separately on 28 October; NAMES-1 v0.2 predates that decision and still uses `OPEN` wording. Record the choices in the NAMES-1 ratification/register edition, rather than pretending they were present in the submitted candidate bytes. The subsequent separately scoped E1-ALIGN proposal (accepted **in principle**) aims to move E_1-specific modules later; it is not part of NAMES-1.

## Notable, explicitly accepted scope consequence: N1-R01B

The active coordinator exit-receipt record contains `contract_modules_sha256` with keys based on two module filenames. NAMES-1 changes those filename keys to their new stable names. A receipt created before this change will **fail closed** when verified against the new files. This is a controlled compatibility effect, not bitwise identity of receipt representations, and must not be concealed under the phrase “pure rename.” The proposed v0.2 design describes it correctly. The installed science switches remain disabled and the scientific allowlist empty at the stated base; consequently, the author does not claim that existing scientific receipts can be migrated. At implementation review, independently check the change and any retained synthetic evidence; never bypass the existing receipt/firewall checks or silently convert old receipts.

## Conditions for subsequent package (not a new finding)

1. The owner ratifies the **actual v0.2 design and OPEN-N1..N3 decisions**. The text's historical `OPEN` labels are not implementation authority by themselves.
2. The implementation overlay is owner-scoped, HIGH tier and independently RECHECKED: exact file/line allowlist, no other changes, protected v0.6 coordinator ASTs, firewall mutation and source-origin tests, source and test identities, and intact synthetic/legacy goldens.
3. All **79** current applicable tests are run by the owner on Windows, with per-module counts, skipped-test reasons and environment recorded; Linux author-side results do not substitute.
4. All three switches remain False, the coordinated scientific result allowlist remains empty, no process termination/orphan bypass is permitted, and no new scientific or holdout execution is authorised.
5. Later widening of the firewall to per-method folders belongs to its own owner-authorised E1-ALIGN/E2R stage, **before any such folders can bypass the check**. E1-ALIGN is only an in-principle proposal at this point.

## REVIEWER-DECIDED — continuation of oversight review 6 of 6

- **N1-RD-07:** Close N1-C01 — PASS; controlled exceptions and negative firewall proofs are explicit, with N1-R01B receipt-key consequence retained.
- **N1-RD-08:** Close N1-C02 — PASS at design stage; complete 79-test Windows requirement remains mandatory for code installation.
- **N1-RD-09:** Close N1-C03 — PASS at design stage; exact live-reference and clean-interpreter origin/firewall proofs remain installation requirements.
- **N1-RD-10:** Close N1-C04 — PASS; Git history is an optional immediate recovery mechanism, not persistent replay identity.
- **N1-RD-11:** Close N1-O01 and N1-REC01 — owner choices A/defer/accept govern the next register edition; no out-of-scope owner tools are changed.
- **N1-RD-12:** PASS specification v0.2 for owner ratification consideration. Preserve HIGH-tier and mandatory independent RECHECK for the later implementation; no automatic E2R admission-gate activation.

**Oversight:** These items extend N1-RD-01..RD-06 from the original review and continue the sixth distinct package review. Claude should check each under the owner's current exception-based reporting policy. No departure from ratified safety, scientific integrity or reviewer process is authorised or identified.

**Boundary:** This was a focused documentary, hash, patch, and evidence inspection. I did not run project code, tests, Windows procedures, data acquisition, beacon retrieval, scientific experiments, holdout actions, process controls or Git writes.

*End of focused NAMES-1 design review.*
