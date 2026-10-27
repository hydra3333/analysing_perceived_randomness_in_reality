# Claude fact check - H-2 v1r3 (DOC-1) - v1

**Date:** 28 October 2026 (Adelaide). **Checker:** Claude (primary designer and coder). **Scope:** facts only (Git identities, paths, chronology, evidence labels), as H-2 section 11 asks. The reviewer rights are the project owner's alone. This is the one check that H-2 v1r3 gets (owner, 28 October 2026). **Holdout statement:** no draw outcome was read or shown.

**Input:** `ChatGPT_Reviewer_Handover_H2_v1r3.md`, SHA-256 `ac61d06a0612e1f126a0c68fbb2e48c698df368ae481289ffcad8984ed310397` (matches the stated hash), LF, 249 lines. Compared with the installed H-2 v1r2 (`53f3af3f...34a2`) at `b14116b`.

## Verdict

**Facts PASS, with 3 CORRECTION and 3 OPTIONAL.** None of them touches the rights.

## Checked and correct

- **Rights block:** sections 2, 3 and 3.1 (R-1..R-11, the T-05 reference text and the latitude decision) are byte-identical to v1r2 (7,672 characters compared).
- **Git identities and parents**, checked against a fresh fetch of GitHub:
  - effective commit `d36735da777b7d8403718af9e1d9d65c1cad47cc`, parent `6460ae3385f467401ce43513b5850a29bdd79198`, 15 files added;
  - TH-1 `744afea085c9fabc62c18ee5c18ee400d0853a9d`, parent `151f393`;
  - procedure commit `b14116b394574ab50ffce2937aa007f439b8c181`, parent `744afea`, adding only the procedure file;
  - Package 2 at `c5424839...` and the integration at `ae76c29...` are unchanged.
- **TH-1 facts:**
  - only tests, the fixture and the verification note changed; the reader, the coordinator, the switches and the allowlist did not;
  - the grammar check has 48 subtests (2 games x 4 variants x 3 kinds x 2 date modes);
  - the reviewer's own Linux evidence (60 OK, 0 skipped; 11/11 mutants) matches `review/Independent_ChatGPT_Focused_Recheck_TH1_Test_Hardening_v1r2.md`;
  - the Windows result is correctly labelled owner-reported.
- **Procedure summary (section 5.1):** it matches `review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md`, including RECHECK by default, the reviewer alone assigning dispositions, the owner override, the absolute eight-subject exclusion for code, and the evidence list.
- **Other points:**
  - the footer now reads "End of H-2 v1r3 DRAFT", which also resolves the v1r2 footer erratum for future editions;
  - there is no owner name;
  - outside the rights block the text is ASCII, except the section sign in lesson 2, which is unchanged from v1r2.

## CORRECTION

**F-C1 - section 8.1, third bullet: register v0.4 reads as current.** The bullet lists `doc/RATIFICATION_REGISTER_v0_4.md` (`cdb8c24e...85d7`) among "the installed editions". Since `d36735d`, the current register is v0.5 (`551c1b42e99b58ad313dabe7d533e5650db83edce58e04f954b2f616c77afb3f`). A cold-start reviewer could take v0.4 as current. **Suggested addition at the end of the bullet:** "Register v0.4 was superseded by register v0.5 (`551c1b42e99b58ad313dabe7d533e5650db83edce58e04f954b2f616c77afb3f`, installed at `d36735d`); DOC-1 proposes v0.6."

**F-C2 - section 8.2, the seven-module suite invocation is quoted without its environment lines.** The text says the TH-1 v1r2 instructions "give the revised seven-module suite invocation as" one `.venv\Scripts\python.exe -m unittest ...` line. In `INSTALL_INSTRUCTIONS.md` inside `review/TH1_Test_Hardening_v1r2.zip`, that line sits between `set PYTHONPATH=src;src\methods;tests` and `set PYTHONPATH=` (lines 18 to 20). Several modules import from `src/`, so the line alone is not the full invocation. **Suggested replacement:** quote all three lines, in order.

**F-C3 - section 0 and lesson 9, "NumPy 2.5.4" on Windows.** Claude cannot confirm the NumPy version of the owner's Windows run from the material it holds; Python 3.14.8 and the test result are what Claude recorded. (The reviewer's own TH-1 recheck records NumPy 2.3.5 for its Linux run, so the figure is not from there.) **Suggested fix:** keep "NumPy 2.5.4" only if the owner confirms it from his log; otherwise drop the version and keep "Python 3.14.8".

## OPTIONAL

**F-O1 - section 10: cite the operative text for the E_2-readiness stage.** "MR v0.5 section 13 Stage 1" is correct as a source (MR v0.5 section 13 is "Phasing"), but MR v0.5 is integrated history. The operative texts are R3 v0.5 section 17.13 stage 1, R2 v0.5 section 5.6 and Architecture v0.8 section 20A. **Suggested:** "(R2 section 5.6; R3 section 17.13 stage 1; Architecture section 20A; from MR v0.5 section 13)".

**F-O2 - section 8.1, first bullet.** "Its exact Git ID is established from the subsequent committed history" is now known. **Suggested:** append "(it is `d36735da777b7d8403718af9e1d9d65c1cad47cc`)".

**F-O3 - section 8.2, "Delivery practice (unchanged, ...)".** The delivery method is now an owner decision (27 October 2026), and it settles the transport question left open in the agreed roles position section 11. Register v0.6 records it that way. **Suggested label:** "Delivery method (owner decision, 27 October 2026)".

## Not checked

- Unchanged text carried over from v1r2 was fact-checked for v1r2 and is not re-checked here.
- Claude did not check the owner's Windows environment.
- The rights themselves are not checked: that is for the owner.

*End of fact check.*
