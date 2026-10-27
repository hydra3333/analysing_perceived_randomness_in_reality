# Claude fact check of H-2 v1r2 (ChatGPT reviewer handover), v1

**Work-item card:** fact check of H-2 v1r2 | H-2 author: ChatGPT reviewer chat | fact checker: Claude (new Claude chat); facts only, rights are the project owner's alone | input `ChatGPT_Reviewer_Handover_H2_v1r2.md`, SHA-256 `53f3af3f0845ea8534e25e896ffc8790fe685a7df9ecad8f7d7e48cd53f234a2` (UTF-8, LF, 225 lines) | HIGH | REVIEWED (facts).
**Date:** 27 October 2026 (Adelaide). **Holdout statement:** no draw outcome was read or shown.

## Verdict

**Facts: PASS, with one erratum.** The owner ratified H-2 v1r2 on 27 October 2026, including the proposed rights R-8..R-11 and section 3.1.

## Checked

- The diff from H-2 v1r1 (`0f9a8a98...68b5`) contains exactly the four changes the author declared: version and target path; a note on the source-level closure of C-INSTALL-01; the new section 3.1; the cold-start Git example path.
- The R-1..R-7 table, the oracle-subjects paragraph and the T-05 reference test remain byte-identical to `doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md` (checked mechanically).
- Section 3.1 records the owner's 27 October decision accurately: the six examples match the 23 October grant word for word (reviewer handover v10 section 1); it applies from the effective commit only; it does not pass to Claude as author; consequential questions stay with the owner. It also states limits the reviewer places on itself (no unilateral waiver of a required test or acceptance condition; no removal of a required independent review), consistent with the 23 October rule that consequential items go to the owner. Its cross-references (H-1 section 1.5, H-3 section 7 item 4, the transition register) exist.
- Non-ASCII appears only inside the verbatim rights block and three section signs.

## Erratum

The closing line (line 224) reads "End of H-2 v1r1 DRAFT." The file is v1r2. Owner decision, 27 October 2026: recorded as an erratum in register v0.5; the file is installed unchanged.

*End of fact check.*
