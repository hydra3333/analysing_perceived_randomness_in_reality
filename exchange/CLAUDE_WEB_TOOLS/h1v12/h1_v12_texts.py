"""The texts of H-1 v12: the counted replacements in H-1 v11 and its blurb, and the new section 0E.

What this file is for
    make_h1_v12.py (beside this file) builds H-1 v12 from the installed H-1 v11. The words it puts in are kept
    here, apart from the mechanism, so that a reader can check each against the decision log. Every "old" text
    must occur exactly once in H-1 v11 (or its blurb); the builder asserts it.

Which part of the project's rules it carries out
    H-1 section 8.5 (a new edition from the exact Git blob by counted replacements, the builder travelling with it).

Which of the project's own modules it uses
    None.

What uses it
    make_h1_v12.py only.
"""

# (old text, new text) for the handover. Each old text occurs exactly once in H-1 v11.
HANDOVER_REPLACEMENTS = [
    ("# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v11\n",
     "# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v12\n"),
    ("**This edition: v11, 24 November 2026, evening (Adelaide, UTC+10:30). OWNER-RATIFIED the same evening (RAT-48;\n",
     "**This edition: v12, 25 November 2026, morning (Adelaide, UTC+10:30). OWNER-RATIFIED IN ADVANCE (RAT-51; decision\n"
     "log entry 262): the owner's words, 25 November 2026, 07:15, when he asked for it: \"i ratify your new handover docs\n"
     "in advance\". IT WAS NOT READ BY THE REVIEWER BEFORE IT WAS INSTALLED; the reviewer's cold read against the\n"
     "repository is owed, and what it finds is corrected in a next revision.** H-1 v11 brought up to date after the\n"
     "file-form standard v0.2 (RAT-49), the conversion of DEV to it (RAT-50; the owner's commit `691f58e`) and the\n"
     "correction of the lock file's line (`fe1c310`): decision log entries 244 to 261. Built from the installed H-1 v11's\n"
     "Git bytes by `exchange/CLAUDE_WEB_TOOLS/h1v12/make_h1_v12.py`: counted replacements of the statements those events\n"
     "made out of date, each marked \"v12\", and **one new section, 0E, which holds everything since H-1 v11**;\n"
     "`H1_v11_TO_v12_DIFFERENCE.txt` beside the builder is the exact difference (line endings set aside: this file is\n"
     "CRLF, as the standard gives every new text file; H-1 v11 is LF). Sections 1, 2 and 2A are unchanged (the builder\n"
     "asserts it). **Where section 0E and an older statement of this file disagree, section 0E and the decision log\n"
     "prevail.** **This is the installed Claude handover.** H-1 v11 (RAT-48) stays in `doc/HANDOVER/` as history.\n"
     "`exchange/CONTINUITY_NOW.md` with the decision log carries whatever is newer. It authorises nothing.\n"
     "**The edition it is built from: v11, 24 November 2026, evening (Adelaide, UTC+10:30). OWNER-RATIFIED the same evening (RAT-48;\n"),
    ("difference from H-1 v10. **This is the installed Claude handover.** It is the ratified candidate\n",
     "difference from H-1 v10. (v12: H-1 v11 was the installed Claude handover until this edition.) It is the ratified candidate\n"),
    ("**Baseline described:** `main` on 24 November 2026 after build step 2's install (`5f16b35`) and its record (entry\n"
     "212). ",
     "**Baseline described:** (v12) `main` on 25 November 2026 after the conversion of DEV to the file-form standard\n"
     "(`691f58e`) and the lock line (`fe1c310`), with their records (entries 260 and 261); before that, build step 2's\n"
     "install (`5f16b35`, entry 212). "),
    ("**Replaces:** H-1 v10 and its blurb (RAT-45), which stay where they are as history.\n",
     "**Replaces:** (v12) H-1 v11 and its blurb (RAT-48), which stay where they are as history, as H-1 v10 (RAT-45) does.\n"),
    ("     `doc/FILE_FORM_STANDARD_v0_1.md` (RAT-47), which is short and governs every file you will write;\n",
     "     `doc/FILE_FORM_STANDARD_v0_2.md` (v12: RAT-49; v0.1, RAT-47, is history), which is short and governs every file\n"
     "     you will write, with decision log entry 258 (RAT-50, a narrow change for the one conversion, now past);\n"),
    ("the change of reviewer chat and the probe's run: section\n     0D**);\n",
     "the change of reviewer chat and the probe's run: section\n     0D**; (v12) **entries 244 to 261 are the standard v0.2 (RAT-49), the conversion of DEV (RAT-50; entries 255 to\n"
     "     260) and the lock line (entry 261): section 0E**);\n"),
    ("## 0D. After H-1 v10: 24 November 2026, afternoon and evening (v11; this section prevails over older statements)\n",
     "## 0D. After H-1 v10: 24 November 2026, afternoon and evening (v11; it prevails over older statements, and section 0E prevails over it)\n"),
    ("**Next numbers at this edition: EX_308, decision log entry 245, RAT-49.** Fetch `main` and confirm before using any:\n",
     "**Next numbers at this edition: EX_308, decision log entry 245, RAT-49** (v12: those were v11's; the present ones\n"
     "are at the head of section 0E)**.** Fetch `main` and confirm before using any:\n"),
    ("9. **THE FILE-FORM STANDARD, RAT-47 (entries 226 to 237): `doc/FILE_FORM_STANDARD_v0_1.md`. Read it; it replaces\n",
     "9. **THE FILE-FORM STANDARD, RAT-47 (entries 226 to 237): `doc/FILE_FORM_STANDARD_v0_1.md`** (v12: now v0.2, RAT-49,\n"
     "   which holds one fault of fact of v0.1 corrected: section 0E item 2)**. Read it; it replaces\n"),
    ("10. **The conversion is the next work, before slice A is packaged** (the standard's section 7): a conversion list\n",
     "10. (v12: **DONE on 24 and 25 November 2026, and not as this item describes it:** one attempt with no second\n"
     "    run, the owner's whole-folder copy as the way back, no rehearsal by the runner (RAT-50). Section 0E items 3 to\n"
     "    6 have what happened; what follows is v11's text, kept as the record of what was planned.)\n"
     "    **The conversion is the next work, before slice A is packaged** (the standard's section 7): a conversion list\n"),
    ("15. **The owner's PC is as H-1 v10 describes it.** DEV at `5f16b35` with his first fill; no QA or PROD; nothing of\n"
     "    build step 3 installed; nothing converted; `.gitattributes` unchanged; the prevailing OV-1 not started.\n",
     "15. **The owner's PC is as H-1 v10 describes it.** DEV at `5f16b35` with his first fill; no QA or PROD; nothing of\n"
     "    build step 3 installed; nothing converted; `.gitattributes` unchanged; the prevailing OV-1 not started.\n"
     "    (v12: no longer so: DEV is converted, filled again and at `fe1c310`; section 0E item 8.)\n"),
    ("    ratified, RAT-48). On Claude, in order: the conversion (item 10); the rest of slice A, to the standard; slices\n",
     "    ratified, RAT-48). On Claude, in order: the conversion (item 10; v12: done, so the list now begins with slice\n"
     "    A: section 0E item 10); the rest of slice A, to the standard; slices\n"),
    ("| `doc/FILE_FORM_STANDARD_v0_1.md` (v11: RAT-47, 24 November 2026, entry 237; a note of ratification beside the coding practices) | `97034474f1a7e9c54a14b9554b45666cb1fa031d566545433a0412d4312f8335` |\n",
     "| `doc/FILE_FORM_STANDARD_v0_2.md` (v12: RAT-49, 24 November 2026, entry 253: **the standard in force**) | `@@STANDARD_SHA@@` |\n"
     "| `doc/FILE_FORM_STANDARD_v0_1.md` (v11: RAT-47, 24 November 2026, entry 237; v12: history since RAT-49) | `97034474f1a7e9c54a14b9554b45666cb1fa031d566545433a0412d4312f8335` |\n"),
    ("exact difference is in `exchange/CLAUDE_WEB_TOOLS/rat47/`). The\n",
     "exact difference is in `exchange/CLAUDE_WEB_TOOLS/rat47/`). (v12) The standard v0.2 is the candidate v0.2r1 the\n"
     "reviewer passed in EX_311, ratified as RAT-49 and installed the same way (`exchange/CLAUDE_WEB_TOOLS/standards/rat49/`);\n"
     "RAT-50 (entry 258) changed its section 7 narrowly for the one conversion without re-issuing it. The\n"),
    ("- Line endings: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`. `git archive` applies the `.bat` rule, so hash `.bat` files from `git show`.\n",
     "- Line endings: (v12: superseded on 25 November 2026. Git now converts nothing in this project, `* -text`, and stores every file exactly as committed: the living project's text files CRLF, `.jsonl` LF, frozen history as it was. Section 0E items 2 and 7.) Before that: Git stores `.md` and `.py` as LF; `.bat` is `text eol=crlf`; `source_data/**` is `-text`. `git archive` applies the `.bat` rule, so hash `.bat` files from `git show`.\n"),
    ("  line endings for `src/` in `.gitattributes` avoids it (specification section 20). The owner's checkout uses\n"
     "  `core.autocrlf=true`.\n",
     "  line endings for `src/` in `.gitattributes` avoids it (specification section 20). The owner's checkout uses\n"
     "  `core.autocrlf=true`. (v12: settled by the file-form standard: the root `.gitattributes` says `* -text`, so that\n"
     "  setting no longer rewrites any file of the project; `GAIS/` keeps its own rules.)\n"),
    ("- **The suite's known result** (owner's PC and cloud, 24 November 2026): **52 modules, 762 tests** (the old 45\n",
     "- (v12) **The suite's known result since the conversion (owner's PC, 25 November 2026): 54 modules, 830 tests:**\n"
     "  the 52 modules and 762 tests below, with the same three failing tests, and two new modules, `test_file_form`\n"
     "  (52 tests) and `test_research_file_form` (16). On the night, one of the 68 new tests failed on Windows (the\n"
     "  lock file's line); it passes since `fe1c310` (116 tests of the three affected modules run by the owner, `OK`).\n"
     "  **The whole suite has not been run since that one-line commit:** the next package's run is the first.\n"
     "- **The suite's known result** (owner's PC and cloud, 24 November 2026): **52 modules, 762 tests** (the old 45\n"),
    ("   (RAT-48, entry 244) after EX_306 and EX_307. The reviewer has written its own\n",
     "   (RAT-48, entry 244) after EX_306 and EX_307; (v12) **the file-form standard v0.2 (RAT-49, entry 253), the\n"
     "   conversion of DEV (RAT-50, entry 258; `691f58e`, entry 260), the lock line (`fe1c310`, entry 261) and H-1 v12\n"
     "   (RAT-51, entry 262): section 0E.** The reviewer has written its own\n"),
    ("   conversion to the file-form standard comes before its first package.** Every operation on his PC is still his\n",
     "   conversion to the file-form standard comes before its first package** (v12: **the conversion is done; slice A,\n"
     "   brought to the standard, is the next work: section 0E item 10**)**.** Every operation on his PC is still his\n"),
    ("- Windows 11; 12 cores, 24 logical processors. Git with `core.autocrlf=true`. Downloads go to `E:\\TEMP`, never into\n",
     "- Windows 11; 12 cores, 24 logical processors. Git with `core.autocrlf=true` (v12: without effect on this project\n"
     "  since `* -text`; his working copy is byte for byte what Git holds). Downloads go to `E:\\TEMP`, never into\n"),
    ("### 12.8 Open items at this edition (24 November 2026)\n",
     "### 12.8 Open items at this edition (v12: 25 November 2026; section 0E item 10 is the current list and prevails)\n"),
    ("  3. The rewrite of `ENVIRONMENT.example.ini` (entry 211) and (v11) the conversion to the file-form standard, in\n"
     "     place of the LF pin, before slice A is packaged.\n",
     "  3. The rewrite of `ENVIRONMENT.example.ini` (entry 211), in slice A. (v12: the conversion to the file-form\n"
     "     standard, which v11 listed here, is done.)\n"),
    ("  5. The next register edition, when a code package or a handover next travels (section 1.6): it records RAT-41's\n",
     "  5. The next register edition (v12: **overdue**; it now also records RAT-45 to RAT-52, the conversion and the\n"
     "     lock line), when a code package or a handover next travels (section 1.6): it records RAT-41's\n"),
    ("US-ASCII; LF; one final newline. The carried sections 1, 2 and 2A are identical to H-1 v9's (the builder asserts\n"
     "it). Every replacement's old text is found exactly once in H-1 v9. The builder refuses on any failure.\n"
     "\nEnd of H-1 v10.\n",
     "(v12) US-ASCII; **CRLF** (the file-form standard: a new text file); one final line ending. The carried sections 1,\n"
     "2 and 2A are identical to H-1 v11's, and so to H-1 v7r1's (the builder asserts it against v11). Every\n"
     "replacement's old text is found exactly once in H-1 v11. The builder refuses on any failure. (This paragraph\n"
     "still described H-1 v9 and v10 in H-1 v11, whose last line read \"End of H-1 v10\": a stale statement, put right\n"
     "here.)\n"
     "\nEnd of H-1 v12.\n"),
]

# The files whose SHA-256 section 0E lists (the Git content at HEAD, computed by the builder).
IDENTITY_FILES = [
    'doc/FILE_FORM_STANDARD_v0_2.md',
    '.gitattributes',
    'deploy/file_form.py',
    'src/research/windows_text.py',
    'src/research/job_lock.py',
    'exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2.zip',
    'exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2/CONVERSION_LIST.json',
    'exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2/INSTALL_AND_RUN_SHEET.md',
    'exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2_REVIEW_NOTE.md',
    'exchange/CLAUDE_WEB_TOOLS/conversion/day_result/OWNERS_WINDOWS_20261124_25.txt',
    'exchange/CLAUDE_WEB_TOOLS/lock_fix/package/FILE_FORM_Lock_Fix_v1.zip',
    'exchange/EX_312_ChatGPT.md',
    'exchange/EX_313_ChatGPT.md',
    'exchange/EX_314_ChatGPT.md',
    'exchange/EX_315_ChatGPT.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_20261125.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_introductory_blurb_20261125.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v11.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v11_introductory_blurb.md',
]

SECTION_0E = """## 0E. After H-1 v11: the night of 24 November and 25 November 2026 (v12; this section prevails over every older statement, section 0D included)

Everything here is from the decision log (entries 244 to 262), the EX messages (EX_308 to EX_315) and the files named.
**Next numbers at this edition: EX_316, decision log entry 263, RAT-53.** Fetch `main` and confirm before using any.

1. **Records.** RAT-48: H-1 v11 (entry 244). **RAT-49: the file-form standard v0.2** (entry 253). **RAT-50** (entry
   258): for the one conversion of DEV, one attempt and no resumption; the package `FILE_FORM_Conversion_v2`
   accepted; the runner's rehearsal dropped. **RAT-51** (entry 262): this handover, **ratified by the owner in
   advance** ("i ratify your new handover docs in advance") and so installed without the reviewer's read; that
   read is owed. **RAT-52** (entry 262): the reviewer's own H-2 v7, which the owner ratified in advance the same
   morning and the reviewer installed (item 9). The register edition is overdue and records RAT-45 to RAT-52
   (item 10).

2. **THE FILE-FORM STANDARD IN FORCE IS v0.2: `doc/FILE_FORM_STANDARD_v0_2.md` (RAT-49). Read it.** v0.1 (RAT-47) is
   history. The rule is unchanged: every text file of the living project is CRLF; **every `.jsonl` file is LF**;
   every program names the line ending it writes; Git converts nothing; frozen history is never converted; six
   files of the retired Mode H machinery are left out by name. **What v0.2 corrected:** v0.1 said that the one
   line `* -text` in the root `.gitattributes` "does not reach GAIS". A simulation showed it reached 173 of
   GAIS's 204 tracked files. The root file therefore holds **three lines**, approved by the owner (entry 251):
   `* -text`, `GAIS/** !text` and `GAIS/**/*.bat text eol=crlf`. v0.2 also says: of 18 writes that named no line
   ending, the 16 in the frozen `src/results_master_v0_2.py` stay and the 2 in `src/two_site_results_check_v0_7.py`
   are corrected; the search covers programs, not tests' temporary fixtures, and "Any test that writes an actual
   in-scope project file remains subject to the standard" (EX_310); the staging and the refresh of the owner's
   working copy are done by a program, by content. Reviewed in EX_310 and EX_311 (FOCUSED PASS).

3. **THE OWNER'S FINDING, WHICH IS NOW A STANDING LESSON (entry 255; 24 November 2026, 22:33): "we have absolutely
   overengineered and wasted time and money."** And: "i do not understand how simple conversion of EOF could be
   made into such a drawn out process. there are no binary files that i know of, we could more easily easily have
   just done the lot and rebuilt all draws and data". Claude had built, for a job of line endings in some 650
   files, one Git setting and a refill: a conversion program with resume logic, a second program, a verifier, a
   look-only kit, 130 tests and planted-fault scripts; the reviewer's recheck (EX_312, five corrections C01 to
   C05) asked for more of the same. **EX_313 (the reviewer, on the owner's direction) superseded it:** one
   attempt; a verified copy of the whole project folder first; on any STOP the whole folder put back on the
   owner's go; only the small direct safeguards kept; no resume, no recovery machinery, no further testing. The
   edits to the existing programs took under half an hour. **What needed care in that job was two things only:**
   the short list of files that must not be converted, and one content-based staging step in Git (item 7).

4. **THE CONVERSION IS DONE (entries 255 to 260).** Package `FILE_FORM_Conversion_v2`
   (`exchange/CLAUDE_WEB_TOOLS/conversion/package/`; reviewed in EX_314, FOCUSED PASS; v1 is kept beside it as
   evidence). The owner ran its sheet in DEV on the night of 24 November, each part on his own go: the whole
   project folder copied to `E:\\TEMP` and proved (107,135 files, `COPY PASS`); the package's 12 files copied in
   (`PRE PASS`, `POST PASS`); **650 listed files and `ENVIRONMENT.ini` converted, line endings only; DEV's 1,578
   research results and status files removed** on his typed `CONVERT` and `REMOVE`; the four results masters and
   ledgers proved unchanged; **685 files staged by content and 1,873 working copies of frozen documents put back to
   Git's own bytes** on his typed `STAGE`; the suite compared with a baseline made from a clean clone (762 of 762
   earlier tests with the same result); **his commit `691f58e4e171761f47f407dce2a4b7b7a687c271`**, `COMMITTED PASS`;
   the fill (47 minutes): POWERBALL 15118 forecasts and 15078 scores through draw 1591, OZLOTTO 6598 and 6558
   through draw 1708, **the counts of build step 2**; the repeat run wrote nothing; the comparison with the old
   development records `RESULT: PASS - COMPLETE - both games` (34800 score records and 20436 forecasts equal,
   `DIFFERENT: 0`); **pushed by the owner on 25 November at 07:02.** Verified by Claude from GitHub: all 686 listed
   files at the list's "after" bytes and in their form; 685 paths changed, none off the list; no `GAIS/` path
   and no `.jsonl` file changed. His windows: `conversion/day_result/OWNERS_WINDOWS_20261124_25.txt`. The whole-folder
   copy was never needed.

5. **One fault found that night, and corrected (entries 260, 261).** One of the 68 new tests failed on Windows
   only: `test_research_file_form ... test_a_lock_file_is_one_line_ending_crlf`. **Cause:** `src/research/job_lock.py`
   opened the lock file with `os.open` without `O_BINARY`; Windows' C runtime then writes a carriage return of
   its own before a line feed, so the line ended CR CR LF. Linux does not, so the cloud passed; and the standard's
   search for writes that name no line ending passes over `os.open` by design, which is where it hid. The owner
   chose to go on that night and correct it afterwards, and the reviewer agreed. **`FILE_FORM_Lock_Fix_v1`**
   (`exchange/CLAUDE_WEB_TOOLS/lock_fix/`; EX_315, FOCUSED PASS): one line gains `| getattr(os, 'O_BINARY', 0)`;
   installed by the owner as **commit `fe1c3108c10b77035a824968c9760803eb1b523a`**, 116 tests of the three affected
   modules `OK`, pushed. No rebuild: `job_lock.py` is class `derived`, and the engine writes that digest into new
   lines and compares it nowhere.

6. **What changed in the living project, in sum.** New: `deploy/file_form.py` (the standard's one rule, the checker's
   core, and the search for writes that name no line ending), `src/research/windows_text.py` (`windows_lines`,
   `LINE_ENDING`), `tests/test_file_form.py`, `tests/test_research_file_form.py`. Changed: the engine's four writers
   of text (`reports.py`, `status_file.py`, `derived_check.py`, `job_lock.py`) write CRLF; a status file's own check
   is over its CRLF bytes and a file in the old form is refused; two lines of the old
   `src/two_site_results_check_v0_7.py`; `deploy/INFRA_MANIFEST.ini` (the helper, class `derived`); `.gitattributes`
   (three lines); `.gitignore` (the two readiness markers). **No `.jsonl` writer and no calculation was touched.**
   The conversion changed the bytes of `forecast`-class files, so the forecasting-code identity changed: that is
   why DEV's results were removed and filled again, and DEV's lists now carry the new identity. **`Make_Installable`
   and `Check_Tree` are not yet wired to the checker:** that is slice A's.

7. **Working rules that follow. Each replaces an older habit of this file.**
   - **Every text file Claude adds is CRLF** (`.sh` and `.jsonl` apart), checked before each commit with the
     project's own rule, for example `file_form.faults_of_files(Path('.'), paths)` from `deploy/file_form.py`. The
     cloud workspace has no automatic conversion: write bytes, or name the line ending. **Files that existed
     before 25 November 2026 stay as they are:** the decision log and `exchange/CONTINUITY_NOW.md` are LF and are
     appended to as bytes; older files under `exchange/`, `doc/` and `review/` are frozen history.
   - **A file's bytes are now the same in Git, in a clone and on the owner's disk.** Hashes are compared exactly;
     nothing is "normalised" first. This supersedes section 1.6's "Verifiers must tolerate CRLF working copies"
     (a carried section, so its text stands unedited) and section 6's notes on line endings.
   - **A package's own files are delivered in their form** (CRLF), and a sheet's `certutil` hash of a file in DEV
     equals the hash of the Git content.
   - **Any low-level write of text is binary** (`os.open` with `O_BINARY`, or `open(..., 'wb')`), with the line
     ending written by the program. Only a run on Windows shows Windows' own translation.
   - **Git does not notice a change of line endings by itself** once `* -text` is set (it trusts the size and time
     it remembers): staging after such a change is by content (`git hash-object -w --no-filters`, then
     `git update-index --index-info`), as `conversion/tools/stage_and_refresh.py` did. That program and the
     conversion program are one-off tools, used once and not project code; do not reuse them.
   - **Nothing is pushed by Claude between the owner's pull and his push on a day of install** (it happened twice,
     entries 210 and 260; EX_315 asks the same of both chats). Records are written after his push.

8. **The owner's PC now.** DEV at `fe1c310` plus the records' commits, converted, filled, Git clean; its
   `ENVIRONMENT.ini` is CRLF. No QA or PROD; nothing of build step 3 installed; the prevailing OV-1 not started.
   Leftovers he may delete: `E:\\TEMP\\FILE_FORM_copy_of_project`, `E:\\TEMP\\FILE_FORM_baseline_clone`,
   `E:\\TEMP\\FILE_FORM_Conversion_v2`, `E:\\TEMP\\FILE_FORM_Lock_Fix_v1`, `E:\\TEMP\\FILE_FORM_evidence_v2` and
   `D:\\DELETE_ME\\a_p_r_i_r\\T028`. `E:\\TEMP\\STEP2_evidence` no longer exists: **a sheet must not name a baseline
   folder on his PC without saying how to make it again** (it is made from a clean clone: entries 210 and 260).

9. **The chats.** The reviewer chat is the one that started on the evening of 24 November (EX_304 to EX_315); it
   commits its own EX files and handover. **In force for the reviewer: H-2 v7 (RAT-52),**
   `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_20261125.md` with its blurb beside it: written and installed by the
   reviewer on 25 November 2026 at 07:17, ratified by the owner in advance, current to entry 261 and EX_315. It is
   the reviewer's: Claude has not reviewed it and does not edit it. H-2 v6 (RAT-46) is history, and Claude's
   refresh H-2 v6r2, never ratified, is superseded by it.
   **The owner's plan for this Claude chat ends on the night of 25 November 2026;** this edition is written so that
   a new chat can take over from it.

10. **What waits, at this edition.** On the reviewer: its cold read of this handover (item 1). On the owner:
    nothing. **On Claude, in order:**
    (a) **slice A of build step 3** (section 0D items 2 to 7): its working files in
    `exchange/CLAUDE_WEB_TOOLS/step3/overlay/` were written before the standard and against `main` at `5f16b35`;
    bring them to the standard (CRLF; every write names its line ending), rebase them on `main` as it is now, wire
    `deploy/file_form.py` into `Make_Installable` and `Check_Tree`, write what section 0D item 7 lists as not yet
    written, and put the slice to the reviewer with the unratified amendment of the deployment design's section 2
    (how processes are read, section 0D item 5) and the two readings of the specification;
    (b) slices B, C and D, the joined rehearsal, the one install into DEV, then QA, the transition check and PROD,
    each on his go;
    (c) the register edition (overdue);
    (d) the operations manual's skeleton after build step 3; its "Standards" section names the `.jsonl` exception.
    **Apply item 3 to all of it: say the simplest safe route first.**

11. **Lessons of these two days, for whoever continues** (in the manner of section 8.8).
    (a) For a one-off migration, begin from "a verified copy of the whole folder, one attempt, put it back on a
    STOP". Do not build resumption. When the owner asks for a standard, tell him at once what the smallest job
    is that would meet it.
    (b) A reviewer's recheck can itself over-engineer. Say so to the owner, with the risk each demand guards
    against and whether that state can exist; the decision is his.
    (c) A comparison that lists a new test as NEW does not say whether it passes. A sheet says that each new
    module ends `OK`, and Claude reads the suite's own lines, not only the comparison's.
    (d) What a program prints is promised by its sheet: a finding about a file is fixed words, never the file's
    content (EX_308).
    (e) A statement of fact in a document for ratification is tried before it is ratified: "does not reach GAIS"
    was written, reviewed and ratified, and was false (entry 250).
    (f) The cloud's evidence is not Windows'. Three Windows facts cost time here: the C runtime's text mode, the
    refusal of a rename while a file is open (TASK_T028), and that every program started from an environment is
    two processes.
    (g) Do not push during the owner's install (item 7).
    (h) When the owner says stop, stop; put the options, recommend one, and do only what he chooses.

12. **What changed from H-1 v11.** The header; section 0 item 2 (the standard's edition; entries 244 to 261); section
    0D (its heading, its next numbers, items 9, 10, 15 and 16: each a note that v12 supersedes it; the text is
    kept); section 4.1 (the standard v0.2 and its hash); section 6 (two notes on line endings); section 7.1 (the
    suite's known result since the conversion); section 10 items 2 and 3; section 12.6; section 12.8 (its heading,
    items 3 and 5); Appendix B.3 and the last line; and this section. Sections 1, 2 and 2A are byte for byte H-1
    v11's. Nothing binding was dropped. **Not re-read for this edition:** sections 3, 5, 8, 9, 11, 12.1 to 12.5,
    12.9 and Appendix A, which are H-1 v11's text; Appendix A's hashes were computed at H-1 v10 and v11 from
    files that Git then held LF, and for files of the living project they are **no longer the hashes of the
    present files** (the conversion changed their bytes). Compute afresh from `HEAD`.

**Identities added at this edition** (SHA-256 of the Git content at `HEAD`, computed by the builder):

@@IDENTITIES@@
"""

# (old text, new text) for the blurb. Each old text occurs exactly once in H-1 v11's blurb.
BLURB_REPLACEMENTS = [
    ("# Introductory blurb for H-1 v11: for a new Claude chat (paste everything below the line)\n",
     "# Introductory blurb for H-1 v12: for a new Claude chat (paste everything below the line)\n"),
    ("The previous Claude chat left you a handover, H-1 v11 (ratified on 24 November 2026, RAT-48: H-1 v10 brought up to date the same day, with one new section, 0D).",
     "The previous Claude chat left you a handover, H-1 v12 (ratified by me in advance on 25 November 2026, RAT-51: H-1 v11 brought up to date, with one new section, 0E; the reviewer had not yet read it when it was installed)."),
    ("A standard for the form of every file (line endings) was ratified on 24 November 2026 (RAT-47, doc/FILE_FORM_STANDARD_v0_1.md); converting the project to it comes before step 3's first package.",
     "A standard for the form of every file (line endings) is in force (doc/FILE_FORM_STANDARD_v0_2.md, RAT-49), and DEV was converted to it on 24 and 25 November 2026 (RAT-50): every text file of the living project is CRLF, every .jsonl file is LF, and Git converts nothing. Step 3's first package (slice A) is the next work."),
    ("doc/HANDOVER/Claude_Primary_Handover_H1_v11.md and follow its section 0, then read its section 0D, which holds everything since H-1 v10 (its reading order and the staged takeover).",
     "doc/HANDOVER/Claude_Primary_Handover_H1_v12.md and follow its section 0, then read its sections 0D and 0E: 0E holds everything since H-1 v11 and prevails over every older statement (its reading order and the staged takeover)."),
    ("chat. Do not over-engineer: the science, N-1, scoring and recoverability are the main game.",
     "chat. Do not over-engineer: the science, N-1, scoring and recoverability are the main game. On 24 November 2026 I had to stop a simple job that had been over-built (\"we have absolutely overengineered and wasted time and money\"): tell me the simplest safe route first."),
]
