# EX_060 independent H-1 and register content review - v0.1

Date: 2026-10-30 (Adelaide)
Author: ChatGPT independent reviewer
Scope: EX_059's H-1 v1r5 and Register v0.17 candidate; H-2 v1r6 r1 revision after Claude factual check.
No ratification, Git operation, test execution, real-data access or scientific-use grant is conferred.

## Input integrity and exact reconstruction

- EX_059 outer ZIP SHA-256: a9307045505202cbca70086b4477ec6dae5fcaf454fb328db7ba8faebf8b66af. ZIP integrity PASS; all 8 members' stored and LF-normalized hashes match the EX_059 table.
- H-1 v1r4 predecessor extracted from EX_047_Claude.zip: SHA-256 2050e9363d841634ecf2a9c308d3efb1ed51b359fbdaf2aa3531a60eb1f1c16a. make_h1_v1r5.py replays its 37 counted edits and builds EX_059's H-1 v1r5 exactly, SHA-256 95e0f096de9d63070a24c7715e5a5333199560ee0fed6320b8ef730c20e988ae. Its normal diff also reverse-applies exactly.
- Register v0.16 predecessor reverse-rebuilt from EX_059's candidate and supplied normal diff: SHA-256 d84fc3ddd5978f0a5529bad20f9db9d1f95142c7e06e3dd78599cc0d4fa1c220. make_register_v17.py applies three counted edits and reproduces EX_059's v0.17 candidate exactly, SHA-256 e49b97ee3c3b8efa076903020625b830ebad6cf612fe0ec870dad8b6bafec1bc.
- The review is a file/document content review, not first-hand verification of live GitHub HEAD or the owner's Windows reports. Claude's reported GitHub verification is attributed to Claude.

## 1. H-1 v1r5 content review

Verdict: CORRECTION 1; no other findings. Substantive handover content, installed-state checkpoint, methods, order of work, runner separation, templates, and safety boundaries are acceptable subject to the precise correction below. Not PASS unchanged.

H1F5-C01 (CORRECTION; proposed disposition FIX AND PROCEED, REVIEWER-DECIDED): H-1's header, builder and Appendix B call its *section 2A* byte-identical/unchanged. The seven numbered foundational points are indeed byte-identical, but H-1 v1r5 inserted an additional 164-byte paragraph inside section 2A after point 7:
"The owner restated the purpose on 30 October 2026, with the reviewer chat's six working principles (register v0.15). It restates these points and changes no rule."
Using section bytes from '### 2A.' through immediately before '## 3. Project in one paragraph', the old and new sections are 1,359 and 1,523 bytes. Therefore the claimed complete-section byte identity is FALSE, though the seven points are unchanged. This is a protected-foundational-text placement/identity issue, not an objection to the restatement's content.

Exact permitted fix: MOVE that exact paragraph, with no wording edits, from after point 7 to immediately BEFORE the '### 2A.' heading, outside the binding section, and adjust make_h1_v1r5.py to perform this move without changing the seven points or the resulting content. The attached H1_C01_PROPOSED_ONLY.diff is the exact candidate-level move, not an authorised substitute H-1. After this move section 2A is byte-identical to v1r4 (1,359 bytes). Independently reconstructed expected H-1 corrected LF SHA-256: 1214bd971058ddd6cc680526fd80375bdbbd6db17397e41ba4c14ae5467101e1, total 69,781 bytes. Claude should verify the patch, regenerate its builder/diff and record that identity. No other H-1 edits are within this FIX AND PROCEED disposition; any different change requires RECHECK.

This fixes the claim in the body and Appendix B without weakening the binding points. Under the owner's tightly scoped documentary FIX AND PROCEED procedure, a second substantive H-1 review is unnecessary **only if** Claude reproduces that exact output hash, verifies whole-section identity, and installs solely with the owner's ratification. This does not grant ratification to Claude.

## 2. Register v0.17 candidate content review

Verdict: CONTENT PASS, conditional on mechanical finalisation. The reconstruction is exact; the register correctly distinguishes EX_055-EX_057, the T006 rehearsal from the owner Windows post-push test, the installation at 5b9edb4, reviewer RDs, 30 October owner work ordering, the non-authoritative working lists and planned handovers. No independent second content finding.

Dependent fix for H1F5-C01: the H-1 v1r5 SHA must change from 95e0f096de9d63070a24c7715e5a5333199560ee0fed6320b8ef730c20e988ae to 1214bd971058ddd6cc680526fd80375bdbbd6db17397e41ba4c14ae5467101e1 in exactly TWO places in the register v0.17 candidate, and ONCE in the register builder's H1 constant; rebuild the diff and verify the exact updated content. This is an identity-reference consequence, not a new scientific or register-policy decision. The existing 'RATIFICATION CANDIDATE', [H-STATUS] (2), [H2-V1R6-SHA] (2) and [H2-CHECK] (1) placeholders remain for owner ratification and documented finalisation. Fill H-2's two hash placeholders with the exact hash below if owner-ratified unchanged.

## 3. H-2 v1r6 r1 (revised reviewer handover)

- Adopts H2F6-01, 02 and 03 (all required CORRECTION) and H2F6-04, 05 and 06 (all three OPTIONAL), without changes to reviewer rights or scientific execution authority.
- New canonical LF file is ChatGPT_Reviewer_Handover_H2_v1r6_r1.md, SHA-256 db40f40ef22995fc65a949243001858f1d7d1285713c9954531ae6b601fc5616, 24,894 bytes. H-2 v1r6 in EX_058 is 24,700 bytes; ratified H-2 v1r5 was 25,106 bytes. The revised document remains below the v1r5 size cap.
- The complete rights region from the genuine heading '## 2.' to immediately before heading '## 4.' is 7,676 bytes, SHA-256 70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db, exactly equal to both earlier v1r5 and v1r6. No rights change proposed. The v1r6-to-r1 unified diff replays byte-for-byte.
- The revised document remains a DRAFT. The owner's planned joint ratification of H-1, H-2 and the register is not presumed.

## Reviewer-decided dispositions

HROUND-060-RD-01: H-1 v1r5 review: one H1F5-C01 correction, exact documentary move only, FIX AND PROCEED if byte-for-byte and same-section assertions verified; otherwise RECHECK. No substantive H-1 PASS before the correction.
HROUND-060-RD-02: Register v0.17 content PASS with the exact H-1 hash references and ordinary owner-finalisation placeholders updated; any non-identity change returns to review.
HROUND-060-RD-03: H-2 v1r6 r1 incorporates H2F6-01..06; protected rights unchanged; draft suitable for owner's joint ratification consideration.

## Next steps / owner boundary

Claude checks the three dispositions, applies H1F5-C01 exactly, verifies its own corrected H-1 builder and both changed register references, and reports any exception. The owner alone ratifies the corrected H-1, the attached H-2 r1, and the updated register together. They then use the existing document-only installation workflow, followed by Git verification. Nothing in exchange/ is itself ratified.
