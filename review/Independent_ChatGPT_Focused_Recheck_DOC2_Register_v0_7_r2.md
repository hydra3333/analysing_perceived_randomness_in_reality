# DOC-2 — Independent ChatGPT focused RECHECK of Ratification Register v0.7 r2

**Date:** 28 October 2026 (Adelaide). **Author:** Claude. **Reviewer:** ChatGPT. **Source:** `DOC2_Register_v0_7_Recheck_r2.zip`. **Scope:** review only the previously raised DOC2-C01, DOC2-C02 and DOC2-O01, their immediately relevant context, and the exact documentary diff. **Risk:** HIGH (authority/register). **No installation or execution authority is conveyed.**

## Verdict

**PASS — 0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER outstanding from this focused recheck.** The corrected register is suitable for the project owner's final ratification/installation consideration, subject to its ordinary finalisation checks. This is a continuation of DOC-2's fifth distinct review, not a new oversight review.

## Independent mechanical checks

| Item | SHA-256 / result |
|---|---|
| Uploaded ZIP | `f0bba314f2650142472c42f97cb5da0c955b4dfb896e783367785e655d291978` — matched |
| Register r2, exact LF bytes | `8b751a878e0626165b6c01bbc49d7d3014b3bd83a171200b4247eb5ec761796d` — matched |
| Original reviewed register r1 | `92e73afba1f7cdb55f38959df67c01d5312f4bc4d50ab3fce6ab1b26f89ce4b1` — matched earlier supplied archive |
| r1-to-r2 diff | `aa15cb72f56309185fd4ee0d08ee1c834e3efd4d7284f049f17e3bea6ce53c33` — matched and re-applied; reproduced r2 byte-for-byte |
| v0.6-to-r2 diff | `b112ad10c031a28473433744220f7b9e0baa8f6a5359eaf3f5a20541a5bf033b` — matched |
| v0.6-to-r2 builder | Input v0.6 hash `5e677dce3f2ae01cd7a3f6cc1ff408c8e32e268150fe0c956e42bf703a9b074c`; builder executed with this archived baseline and reproduced r2 byte-for-byte |

The r1-to-r2 patch changes only the three relevant register lines (two diff hunks), with no changes to R2/R3/Architecture, the D-1..D-11 content, existing historical identities, or safety gates. The builder's count remains five replacements.

## Disposition by finding

**DOC2-C01 — CLOSED, PASS.** The out-of-date statement now accurately says NAMES-1 renames filenames but does not itself create per-method folders. It avoids importing an unratified OPEN-N1 choice into a separate earlier register. The later owner decision **OPEN-N1 = A**, supplied on 28 October 2026 in `Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md`, should be recorded in the register edition accompanying NAMES-1, as the owner/Claude plan specifies. Thus the candidate's mention of the separate OPEN-N1 decision is treated as drafting chronology, not as a current claim that the owner has not decided. No new DOC-2 correction is required.

**DOC2-C02 — CLOSED, PASS.** The Basis clause now explicitly limits the `38fc60e` verification to already-committed references and independently identifies E2R-1 v0.3r3 by content hash rather than claiming it existed in that Git snapshot. The owner's subsequent 28 October E2R-1 ratification does not retroactively install it at `38fc60e`.

**DOC2-O01 — CLOSED, PASS.** The process entry now identifies the **newer** 28 October owner instruction as superseding the earlier all-items-to-owner reporting requirement. Every REVIEWER-DECIDED item is still explicitly listed by the reviewer and checked by Claude; Claude reports by exception/owner interest, without authority to change reviewer decisions. This aligns with the separately communicated newer owner instruction.

## Finalisation limitations

- The candidate intentionally still contains `[E2R-DATE]` and `RATIFICATION CANDIDATE`; **do not install them as final text**. The owner has since reported E2R-1 ratified on 28 October 2026; use the actual confirmed date. Mark this register OWNER-RATIFIED only after the owner's separate DOC-2 ratification.
- Recompute SHA-256 for the **finalised** register bytes; it will not equal the r2 candidate hash above. Keep an exact candidate-to-final diff and installation manifest evidence. No assumption of repository installation is made.
- Owner choice OPEN-N1 = A, OPEN-N2 deferred, OPEN-N3 accepted belongs in the subsequent NAMES-1 register edition, rather than being silently inserted into DOC-2 finalisation.

## REVIEWER-DECIDED — continuation of oversight review 5 of 6

- **DOC2-RD-05:** Close DOC2-C01: PASS on the precise correction, preserving separate owner OPEN-N1 authority and later owner decision.
- **DOC2-RD-06:** Close DOC2-C02: PASS; verification scope and E2R installation are correctly distinguished.
- **DOC2-RD-07:** Close DOC2-O01: PASS; newer owner oversight reporting instruction is clearly differentiated; reviewer rights unchanged.
- **DOC2-RD-08:** PASS DOC-2 r2 for owner ratification consideration, subject to the usual exact finalisation diff, identity and installation checks. No new authority or operation is granted.

**Oversight:** These items extend the previously enumerated DOC2-RD-01..RD-04 and are not a new review 7. Claude should check each, and use the owner's latest reporting-by-exception rule. No departure from ratified scientific, safety, compliance or process constraints identified.

**Boundary:** No project tests, scientific runs, holdout reads, source edits, switch changes, process management or Git mutations were performed. Only the documentary builder and patch were run on isolated copies.

*End of focused DOC-2 review.*
