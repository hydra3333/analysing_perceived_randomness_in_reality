## Appendix B. Changes in v2, and where everything went

v2 is a full consolidated edition (owner, 14 November 2026: "fully updated docs rather than more addendums or deltas"). It is made from H-1 v1r8's ratified bytes (`09e579ba...a801`) by counted edits, each asserted to occur exactly once, and by replacing whole sections (`exchange/CLAUDE_WEB_TOOLS/h1v2/make_h1_v2.py`; the diff from v1r8 travels with it). It changes no rule; where it states a rule, the ratified documents and the register prevail. Nothing in v1r8 or in the v1r10r3 delta was dropped except what is superseded below. v1r8's own change list stays in v1r8.

### B.1 What changed, by section

1. **Header:** v2; the baseline (`main` at `ac2c063`); what it replaces; the author and status.
2. **Section 0:** clone with full history; the reading list (H-2 v1r9 with its deltas, register v0.29, design v0.1r7 and A1, direction v0.3r1, rulebook v0.5, template draft 5, the decision records, the readiness files); item 3 asks what has advanced since 14 November, by Git file names only; item 4's last sentence made general. **Section 0A (new):** the four traps (the 6 November renumbering with the crosswalk table, from the v1r10r3 delta; the lost workspace; shallow clones; register v0.27's RAT-28).
3. **Section 1:** the reviewer chats' history to EX_170; the rulebook's version; oversight through EX_170; document installs since DOC-12; EX_163 among the for-the-record packages.
4. **Section 2:** the model names and attribution; full editions rather than layers (owner, 14 November 2026); proportion restated (13 November 2026); the gate D push lesson. **Section 2A is unchanged, byte for byte** (the builder asserts the whole section).
5. **Section 3:** the design's current edition; MHUP-A installed; Mode H first; the fixed cohort; no holdout opened.
6. **Section 4:** the design row (v0.1r7, with A1 and RAT-30's amendments folded in); the direction document v0.3r1; the template draft 5; the register pointer (v0.28 installed, v0.29 with this file).
7. **Section 5:** 5.1 the updater v0.2 installed and never run live, the first update's order and the retry rule (EX_167 B02, R-018 (a)); TSC-1; **Q7 decided**. 5.3 the installed data (E_1 revision 3 released; the install records; 84, 284, 3 and 371 files; the fixed cohort); the owner's decisions from 4 to 14 November 2026; Q7's old OPEN line marked decided. 5.4 the launchers' byte-code lines; DEP-1; **the Mode H freeze**.
8. **Section 6:** the updater v0.2 (line references); the v0.1 bullet kept as history; the closure and environment; the `.gitattributes` rules added by MHUP-A; the tests pinned to the version-1 masters.
9. **Section 7:** 7.1 MHUP-A and the test fix; the document installs and the owner's commits since DOC-11. 7.2 the MHUP-A modules. 7.3 E_1 revision 3. 7.4 571 tests in 45 modules. 7.5 the updater v0.2, the masters still version 1, where Mode H's records will live. 7.6 the updater's live fetch, Mode H on real data and the POC rerun not yet tested.
10. **Section 8:** 8.6 rulebook v0.5, `cc_clone.py` v0.4's commands, `check_task_commands.py`, F1's denied strings, T016 run and T017 next, the tasks since T015, how T023 recorded cleanly; 8.7 the MHUP-A, document and readiness rebuild records; 8.8 thirteen lessons added (the v1r10r3 delta's and those of 11-14 November).
11. **Section 9:** template draft 5; records since MHUP-A; later variants never in Mode H's cohort.
12. **Section 10:** rewritten: done since v1r8; the documentation round; Mode H game by game (D1-D7, the preparatory checks, the approvals, the freeze); MHUP-B after both seals with everything it must carry; then WF-1C and the waves. Q7 removed from the OPEN questions.
13. **Section 11:** rewritten for the present gates (the preparatory checks, the freeze, no AI contact with any lottery website).
14. **Section 12:** 12.1 the EX numbers (EX_170 newest); 12.2 `check_task_commands.py` and the folders added since DOC-11; 12.3 `pyahocorasick` and 571 tests; 12.6 the working tree after MHUP-A and after Approval 2; 12.8 rewritten as the open items at this edition (including the readiness findings F-1 to F-6); 12.9 rewritten (full history; the pinned tests; models).
15. **Appendix A:** H-1 v1r8, the v1r10r3 delta, H-2 v1r9 (with its rights-region hash), its v1r10 delta and the v1r11 r1 candidate; registers v0.24 to v0.28; design v0.1r5 to v0.1r7, A1 and the Appendix J amendments; the direction document v0.3r1; rulebook v0.5 and v0.4; the settings after F1; the family registry after MHUP-A; MHUP-A's package, the updater v0.2, the test fix, the decision records, the readiness files and the crosswalk. Every hash was computed with `git show HEAD:<path> | sha256sum` at `ac2c063`.

### B.2 Where the v1r10r3 delta went (it was the last supplement to v1r8; the v1r9 delta was folded into v1r10 and its successors before it)

| Delta section | Now |
|---|---|
| Header and status | Header; Appendix A |
| 0. The two things that trip a new chat | Section 0A, items 1 and 2 (the crosswalk table verbatim) |
| 1. The position on 8 November | Overtaken: section 3; section 10, item 1 |
| 2. Roles, chats and models | Section 1.1 (the reviewer chats); section 2 (models); section 8.6 (Claude Code and its tasks); section 7.1 (the owner's own commits) |
| 3. The hard rules | Unchanged in sections 2, 2A, 5 and 11 (the delta pointed to them) |
| 4.1 The reviewer takeover (EX_153-EX_156, RAT-25, DOC-12) | Section 1.1; section 5.3; section 7.1; section 10, item 1 |
| 4.2 Windows evidence (T022, T021) | Section 8.6 (the tasks since T015) |
| 4.3 The owner's decisions of 6 November (DEP-1, GAIS-1, the waived bundle test, the lost signatures) | Section 5.3; section 5.4 (DEP-1); section 12.3 |
| 4.4 The reviewer's documents on the clean-up | Section 0A, item 1; Appendix A (the crosswalk) |
| 4.5 The history clean-up | Section 0A, item 1; section 8.8 (the history-rewrite lesson) |
| 4.6 The owner's later commits (OUTLANDISH, `.gitignore`, `create_venv.bat`) | Section 7.1; section 8.6 (`create_venv.bat` in rule 7); section 8.8 (look before building) |
| 4.7 The integrated package started | Overtaken by its completion: section 7.1; section 8.7; section 10, item 1 |
| 4.8 RAT-26, DOC-13, RAT-27 | Section 5.3; section 7.1; section 4 (the design and template rows) |
| 4.9 The state on 10 November; R-020 (g) | Section 5.3; section 8.6 (rulebook v0.5's section 2A, ended) |
| 5. Where everything is | Section 8.7; section 12.2; Appendix A |
| 6. Decisions and obligations for the integrated package: (1) A1 | Section 4 (design row); section 5.3; section 8.8 (A1's order) |
| (2) C01-EFF | Section 7.3 |
| (3) R-020 (a)-(g) | Section 5.3 (released set, decisions); section 6 (the orphan refusal); section 10, item 3 (the POC rerun) |
| (4) R-019 | (a), (d), (e) carried and installed with MHUP-A; (b), (c) section 10, item 4 |
| (5) The integrated review's scope | Done: EX_164 PASS (section 1.1, section 10, item 1) |
| (6) MHUP-B's timing | Settled by Route 2: section 3; section 5.3; section 10, items 3 and 4 |
| (7) R-018 (a), (d), (h) | Section 5.1 (retries); section 5.3; section 10, item 4 |
| (8) What register v0.26 must record | Done (register v0.26) |
| (9) Q7 | Decided: section 5.1 |
| (10) The owner's backup | Section 10, item 3 (a prerequisite before Approval 1) |
| 7. The integrated package's work list | Done (MHUP-A installed); its items 8 and 9 are section 10, items 2 to 5 |
| 8. Working lessons | Section 8.8 (all eleven, merged with v1r8's) |
| 9. The first hour in a new chat | Section 12.9 |
| 10. Integrity | Appendix B.3 |

### B.3 Integrity

Every fact added here was checked against the repository at `ac2c063` (14 November 2026; full history) or taken from the records named; every hash was computed with a tool. The builder asserts v1r8's input hash, that each counted edit's old text occurs exactly once, that section 2A is byte-identical to v1r8's, and that the output is US-ASCII with LF line endings and one final newline. Nothing in this edition was run against real data, and nothing is installed by it. What is not in this file, the register, the readiness files, the reminders or the roadmap does not exist.

*End of H-1.*
