"""The texts of the Claude handover refresh H-1 v11: the counted replacements and the new section 0D.

What this file is for
    make_h1_v11.py builds the H-1 v11 candidate and its blurb from the installed H-1 v10. This file holds what
    changes: pairs (the exact old passage of H-1 v10, what stands in its place), each old passage occurring exactly
    once; the new section 0D, in which @@IDENTITIES@@ stands for a table the builder computes from Git; and the
    same kind of pairs for the blurb.

Which part of the project's rules it carries out
    H-1 v10 section 8.5 (counted replacements, the builder travelling with the candidate).

Which of the project's own modules it uses
    None.

What uses it
    make_h1_v11.py, beside it.
"""

# The files whose SHA-256 the builder computes from Git at HEAD for section 0D's table, in this order.
IDENTITY_FILES = [
    'doc/FILE_FORM_STANDARD_v0_1.md',
    'exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028_probe.py',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124_introductory_blurb.md',
    'exchange/CLAUDE_WEB_TOOLS/h2v6r2/out/ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124.md',
    'exchange/CLAUDE_WEB_TOOLS/h2v6r2/out/ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124_introductory_blurb.md',
    'exchange/CLAUDE_WEB_TOOLS/standards/TRIAL_CRLF_SUITE_COMPARISON.txt',
]

# ------------------------------------------------------------------------------------------------ the handover
HANDOVER_REPLACEMENTS = [
    ("# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v10",
     "# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v11 CANDIDATE"),
    ("**Version:** v10, 24 November 2026 (Adelaide, UTC+10:30). **H-1 v9 brought up to date**",
     "**This edition: v11 CANDIDATE, 24 November 2026, evening (Adelaide, UTC+10:30). H-1 v10 brought up to date the\n"
     "same day,** after the owner's go for build step 3, the review of its plan, his decisions on it, the file-form\n"
     "standard (RAT-47) and a change of reviewer chat (decision log entries 216 to 238). Built from the installed\n"
     "H-1 v10's Git bytes by `exchange/CLAUDE_WEB_TOOLS/h1v11/make_h1_v11.py`: counted replacements of the status\n"
     "statements those events made out of date, each marked \"v11\", and **one new section, 0D, which holds everything\n"
     "since H-1 v10**; `H1_v10_TO_v11.diff` beside it is the exact difference. Sections 1, 2 and 2A are unchanged (the\n"
     "builder asserts it). **Where section 0D and an older statement of this file disagree, section 0D and the\n"
     "decision log prevail.** **It is a CANDIDATE: not ratified, and the reviewer has not read it.** H-1 v10 stays\n"
     "installed and unchanged in `doc/HANDOVER/`.\n"
     "**The edition it is built from:** v10, 24 November 2026 (Adelaide, UTC+10:30). **H-1 v9 brought up to date**"),
    ("**Status:** OWNER-RATIFIED 24 November 2026 (RAT-45; decision log entry 215),",
     "**Status of H-1 v10:** OWNER-RATIFIED 24 November 2026 (RAT-45; decision log entry 215),"),
    ("**Replaces:** H-1 v9 and its blurb (RAT-43), which stay where they are as history.",
     "**Replaces, once ratified:** H-1 v10 and its blurb (RAT-45), which stay where they are as history."),
    ("the deployment design, and the coding practices;",
     "the deployment design, and the coding practices; and (v11) the fourth, the file-form standard\n"
     "     `doc/FILE_FORM_STANDARD_v0_1.md` (RAT-47), which is short and governs every file you will write;"),
    ("runner's rulebook v0.7 (RAT-44, entry 192) and the rehearsal on Windows (entries 199 to 208));",
     "runner's rulebook v0.7 (RAT-44, entry 192) and the rehearsal on Windows (entries 199 to 208); (v11) entries\n"
     "     213 to 216 are H-1 v10 and H-2 v6 (RAT-45, RAT-46), and **entries 217 to 238 are build step 3's go and\n"
     "     plan, the file-form standard (RAT-47, entry 237) and the change of reviewer chat: section 0D**);"),
    ("line\n    endings pinned to LF for the project's code in `.gitattributes`, in step 3, before the first tree is made;",
     "(v11: H-1 v10 said here \"line endings pinned to LF for the project's code in `.gitattributes`, in step 3, before\n"
     "    the first tree is made\"; the file-form standard, RAT-47, replaces that: section 0D);"),
    ("11. **What is authorised now:** documents and records. Build step 3 needs the owner's own go (section 10); so does\n"
     "    every install and every run on his PC.",
     "11. **What is authorised now (v11):** documents and records; and, since the owner's go of 24 November 2026 (entry\n"
     "    217), build step 3's design within the ratified documents, its coding and testing in the cloud, and its\n"
     "    reviewed packages. Every install, run, tree creation, conversion, backup, restore and runner task on his PC\n"
     "    still needs his own go."),
    ("(entry 175) and reviewed EX_282 to EX_294.",
     "(entry 175) and reviewed EX_282 to EX_294. (v11: that reviewer chat wrote H-2 v6, RAT-46, and ended on 24\n"
     "    November 2026 after EX_303; a new reviewer chat started that evening from Claude's refresh H-2 v6r2 and has\n"
     "    written EX_304 and EX_305: section 0D.)"),
    ("**The present reviewer chat took over from H-2 v5r1 on 23 November 2026** (entry 175; 0B item 13), with",
     "The chat that took over from H-2 v5r1 on 23 November 2026 (entry 175; 0B item 13) ended on 24 November after\n"
     "   EX_303. **(v11) The present reviewer chat started on 24 November 2026 from Claude's refresh H-2 v6r2** (entries\n"
     "   232 and 234; section 0D), with"),
    ("| `doc/CODING_PRACTICES_v0_1.md` | `d64f0101a4fdb21998b2871765bd9b3f06ccb6c7409c7a2d0e9f230cebbd7ddd` |\n"
     "\n"
     "Each design document is the candidate the reviewer passed in EX_271",
     "| `doc/CODING_PRACTICES_v0_1.md` | `d64f0101a4fdb21998b2871765bd9b3f06ccb6c7409c7a2d0e9f230cebbd7ddd` |\n"
     "| `doc/FILE_FORM_STANDARD_v0_1.md` (v11: RAT-47, 24 November 2026, entry 237; a note of ratification beside the coding practices) | `@@STANDARD_SHA@@` |\n"
     "\n"
     "Each design document is the candidate the reviewer passed in EX_271"),
    ("**The one installed reviewer handover now, in force since RAT-43 (entry 174): H-2 v5r1,**",
     "**(v11: the installed reviewer handover is now H-2 v6, RAT-46, entry 216, "
     "`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md`; the present reviewer chat started from Claude's "
     "unratified refresh of it, H-2 v6r2: section 0D.) Before RAT-46 the one installed reviewer handover, in force "
     "since RAT-43 (entry 174), was H-2 v5r1,**"),
    ("it awaits the\n   owner's separate decision, and H-2 v5r1 stays the installed reviewer handover until then.",
     "(v11) the owner\n   ratified it (RAT-46, entry 216) and the reviewer installed it as H-2 v6; section 0D has what followed."),
    ("then the transition\n   check and PROD's first job, on the owner's own go.",
     "then the transition\n   check and PROD's first job. **(v11) The owner gave his go for its design and cloud coding on 24 November 2026\n"
     "   (entry 217). Its plan, the plan's review, his decisions and where the work stands are in section 0D; the\n"
     "   conversion to the file-form standard comes before its first package.** Every operation on his PC is still his\n"
     "   own go."),
    ("LF pinned in `.gitattributes` before\n   the first tree;",
     "(v11: not \"LF pinned\": the\n   file-form standard, RAT-47);"),
    ("his decision on the reviewer's H-2 v6 candidate (section 10 item 2); his go for build\n  step 3; his word on reminders",
     "(v11: H-2 v6 is ratified and build step 3 has his go; section 0D item 16 lists what waits\n  now) his word on reminders"),
    ("and the LF pin in `.gitattributes`, in build step 3.",
     "and (v11) the conversion to the file-form standard, in\n     place of the LF pin, before slice A is packaged."),
    ("  9. The reviewer's handover: H-2 v5r1 describes the state before build step 2; the reviewer has written H-2 v6\n"
     "     as a candidate, which is its own to finalise once the owner decides.",
     "  9. (v11) The reviewer's handover: H-2 v6 is installed (RAT-46); Claude's refresh H-2 v6r2 is unratified; the\n"
     "     present reviewer chat writes its own next edition when it chooses."),
    ("the scratch folder `D:\\DELETE_ME\\a_p_r_i_r\\T025` and\n  `E:\\TEMP\\STEP2_baseline_clone` (no longer needed, entry 212);",
     "`E:\\TEMP\\STEP2_baseline_clone` (no longer needed, entry 212; v11: the\n  scratch folder of TASK_T025 has been deleted by the owner, entry 222);"),
]

SECTION_0D = """## 0D. After H-1 v10: 24 November 2026, afternoon and evening (v11; this section prevails over older statements)

Everything here is from the decision log (entries 216 to 238), the EX messages (EX_297 to EX_305) and the files named.
**Next numbers at this edition: EX_306, decision log entry 239, RAT-48.** Fetch `main` and confirm before using any:
the reviewer took five numbers in a row this afternoon while Claude was working.

1. **Records.** RAT-46: the reviewer's H-2 v6 (entry 216). RAT-47: the file-form standard (entry 237). The next
   register edition is still owed (section 12.8 item 5) and now also records RAT-45, RAT-46 and RAT-47.

2. **Build step 3 has the owner's GO (entry 217, 15:53): "Build step 3, go now please."** It covers design within
   the ratified documents, coding and testing in the cloud, and the reviewed packages. It covers no install, run,
   tree creation, backup, restore or runner task on his PC.

3. **The build plan:** `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`. Four code slices, each a package
   for the reviewer, then the transition: **A** foundations (the settings of the three trees, the readiness
   markers and `Make_Installable`, the static import check, the list of installed files, the environment's digest,
   `Check_Tree`, the launch guard); **B** backups, the recovery kit, the restore; **C** `Init_Tree`, `Install`,
   `Reinstall_Infra`, `Verify_Tree` and the half-finished states; **D** the clean-sheet updater
   `results_master_v0_3.py`; **E** the transition (QA, its own `.venv`, `Run_Research.bat --game BOTH --no-update` in
   QA, the transition check there, then PROD). Its section 6A lists what the joined slices must show before the
   one install into DEV. **Reviewed:** EX_299 (four findings), narrowed by EX_300; all corrected in v0.1r1;
   **EX_301 FOCUSED PASS.** A working plan, not a ratified design.

4. **The owner's decisions on the plan (entry 219):** one install into DEV at the end; a probe task first; QA
   before PROD; the plan to the reviewer.

5. **How Windows' processes are read (entry 222; plan section 4A).** The reviewed `src\\package_tools\\process_check.py`
   uses psutil and holds the old system's lock clearances: its rule and its refusals are kept, the file is not
   reused. **The owner chose:** the restore stays standard library only (a few dozen lines read names, parents and
   start times from Windows; the probe has such a reader); every other process check uses psutil; psutil for the
   restore too only if that proves too hard, said beforehand. **The narrow amendment of the deployment design
   section 2 ("standard library only" for the install tools) is NOT ratified yet;** put its wording to the reviewer
   with slice A.

6. **TASK_T028, a probe of three Windows facts: written, reviewed, NOT RUN; it waits for the owner's go.**
   `CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` r1 and `inbox/TASK_T028_probe.py` r1 (builder and template in
   `exchange/CLAUDE_WEB_TOOLS/t028/`). EX_301 found three faults in the first edition; EX_302 passed r1. It
   measures how Windows answers a rename, replacement or removal when something is open; the size and time of a
   ZIP of the main `.venv` alone (an environment-only proxy: the scratch tree of TASK_T025 is deleted); and what
   psutil and the standard library each read of the PC's Python processes. **Its part that calls Windows through
   ctypes has run nowhere:** a fault there stops the task's last step after the other two are recorded. The
   install, backup and restore logic of slices B and C is designed around its answers.

7. **Slice A's working files exist** (entries 222, 225): `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, copied into a
   work clone and tested by `step3/sync_and_test.sh <clone> <python> <test modules>`. **Not a package, not reviewed,
   nothing installed.** Done: `src/research/settings.py` (DEV's entries for QA and PROD and every cross-tree check
   of the deployment design's section 1), the rewritten `ENVIRONMENT.example.ini`, `deploy/install_import_check.py`,
   `deploy/install_readiness.py` (the two markers), `deploy/make_installable.py`, `deploy/deploy_command.py`,
   `Make_Installable.bat`, the manifest's `[install_tool]` section, and the tests `test_trees_settings.py` (32) and
   `test_trees_readiness.py` (38). **Two readings of the specification to put to the reviewer with the slice:** a
   variant may import its own listed files as well as its helpers; the tool itself refuses a variant that imports
   an infrastructure file not classed `forecast`. **Not yet written:** the list of installed files, the
   environment's digest over the fixed inventory, `Check_Tree`, the launch guard. **All of it was written before
   the file-form standard:** its files and the bytes its programs write must be brought to the standard.

8. **The owner's principle (entry 227, his words):** "git should never be used as an operational gatekeeper/checker
   nor for gating/checking deployments etc, github is a tool for managing commits and project statuses." No tool
   of the new system consults Git. The readiness markers are not tracked by Git.

9. **THE FILE-FORM STANDARD, RAT-47 (entries 226 to 237): `doc/FILE_FORM_STANDARD_v0_1.md`. Read it; it replaces
   "LF pinned".** How it came about: three files under `src` are CRLF on the owner's disk where Git holds LF, and
   one of them, `src/methods/_common/game_profiles.py`, is `forecast`-class, so its bytes are part of the identity
   every list in DEV records. The owner would not leave that as it lay, asked what Windows' own conventions are,
   and directed a written standard to which everything conforms. **The standard:** every text file of the living
   project is CRLF, whoever wrote it; **every `.jsonl` file is LF** (a list line is the canonical encoding whose
   bytes, ending included, the hash chain and the content digests are computed from); every program names the
   line ending it writes (Python's default differs between his PC and the cloud); Git converts nothing (`* -text`
   at the root; `GAIS\\` keeps its own rules, entry 234); the project's own checker enforces it, in the suite, in
   `Make_Installable` and in `Check_Tree`; frozen history is never converted; six files of the retired Mode H
   release machinery are left out by name (its section 3A). **Reviewed** in EX_303 (four clarifications), EX_304
   (one: no undo from the list; the way back is the owner's copy) and EX_305 (FOCUSED PASS).

10. **The conversion is the next work, before slice A is packaged** (the standard's section 7): a conversion list
    made in the cloud (each tracked file's SHA-256 before and after); a conversion program the owner runs in DEV
    (it walks the folders itself and never calls Git; prints what it found by class and waits for his word; a
    listed file whose hash is the "after" is passed over, "before" is converted, any third value is a STOP; it
    holds the job lock and the updater's lock; it checks his pre-conversion copy first, and **on a second run
    checks that copy against the "before" hashes recorded at the first run, not against files already
    converted** (the reviewer's watchpoint, EX_305)); the engine's writers changed to the standard's forms; the
    checker; `.gitattributes` and `.gitignore`; the one refresh of his working copy under `* -text`; a sheet; a
    rehearsal by the runner. **At the conversion `game_profiles.py` changes bytes, so every list in DEV becomes
    foreign: DEV's research results and its status files are removed on his own go and filled again (about 47
    minutes).** Claude's own new files are CRLF from that day, not before.

11. **What Claude's trial in the cloud showed, and did not** (`exchange/CLAUDE_WEB_TOOLS/standards/`): 669 files
    under `src`, `deploy`, `tests` and the root made CRLF in a copy; 732 of 762 tests the same; 30 failing, all in
    five `test_mhupa_*` modules, tracing to the six files left out by name; with those six put back, all five pass.
    It did not cover `source_data\\`, the changed writers, the refresh of his working copy, or Windows.

12. **Mode H.** The owner (entry 230): "I dop not currently care about obsoleted Mode H stuff." Read narrowly: the
    retired machinery is not maintained and is no veto. **The binding rule that the sealed Mode H records are never
    altered is unchanged.**

13. **The operations manual** (entries 220 and 230; EX_298), after build step 3 is proved: short, for a human, a
    practical how-to; finding and reading the reports is a necessary topic; a command cheat sheet as an index; a
    "Standards" section that names the `.jsonl` exception; its structure proposed by Claude and the reviewer
    together for the owner's approval.

14. **The reviewer chats.** The chat that wrote H-2 v6 ended on 24 November without notice after EX_303. At the
    owner's request Claude refreshed H-2 v6 as the candidate H-2 v6r2 (`exchange/CLAUDE_WEB_TOOLS/h2v6r2/`; entry
    232): unratified, and written by Claude, not by a reviewer. The owner started a new reviewer chat from its
    blurb (entry 234); it wrote EX_304 and EX_305. **In force for the reviewer: H-2 v6 (RAT-46).**

15. **The owner's PC is as H-1 v10 describes it.** DEV at `5f16b35` with his first fill; no QA or PROD; nothing of
    build step 3 installed; nothing converted; `.gitattributes` unchanged; the prevailing OV-1 not started.

16. **What waits, at this edition.** On the owner: his go for TASK_T028 r1; his decision on this H-1 v11. On the
    reviewer: nothing. On Claude, in order: the conversion (item 10); the rest of slice A, to the standard; slices
    B, C and D; the joined rehearsal; the one install into DEV; then QA, the transition check and PROD, each on
    his go. Each week before PROD's first job is one draw of each game that cannot count in the prevailing OV-1.

17. **Lessons of the day, for whoever continues** (in the manner of section 8.8). (a) A script that writes a
    record and a commit command must not be two unchained lines: when the script stopped, the commit ran and
    named an entry that did not yet exist (entry 223); begin such a block with `set -e`. (b) The decision log is
    not pure ASCII (the owner's quoted words): append to it as bytes. (c) Never install on the owner's relay of
    the reviewer's recommendation; wait for his own words (entries 215, 236). (d) A task file is read cold for:
    every existing folder above the place it first writes; whether each command line does what the prose around
    it says; and whether "finished" can be printed when a measurement was not made (EX_301). (e) Before promising
    that a change can be undone, ask whether the change is one-to-one: making line endings uniform is not
    (EX_304). (f) Say what a reader's summary is evidence of: a cloud trial is Claude's evidence, not the
    reviewer's and not Windows'. (g) The owner's first answer to "which option" may be a principle; put the
    options again in its light instead of choosing for him (entries 227, 228).

**Identities added at this edition** (SHA-256 of the Git content at `HEAD`, computed by the builder):

@@IDENTITIES@@
"""

# --------------------------------------------------------------------------------------------------- the blurb
BLURB_REPLACEMENTS = [
    ("# Introductory blurb for H-1 v10: for a new Claude chat (paste everything below the line)",
     "# Introductory blurb for H-1 v11 CANDIDATE: for a new Claude chat (paste everything below the line)"),
    ("The previous Claude chat left you a handover, H-1 v10.",
     "The previous Claude chat left you a handover, H-1 v11 (a candidate: the installed H-1 v10 brought up to date the "
     "same day, with one new section, 0D; check it against H-1 v10 with the exact difference beside it)."),
    ("(the research engine, in DEV) are installed and proved.",
     "(the research engine, in DEV) are installed and proved. Build step 3 has my go for its design and cloud coding "
     "only. A standard for the form of every file (line endings) was ratified on 24 November 2026 (RAT-47, "
     "doc/FILE_FORM_STANDARD_v0_1.md); converting the project to it comes before step 3's first package."),
    ("doc/HANDOVER/Claude_Primary_Handover_H1_v10.md and follow its section 0",
     "exchange/CLAUDE_WEB_TOOLS/h1v11/out/Claude_Primary_Handover_H1_v11.md (or "
     "doc/HANDOVER/Claude_Primary_Handover_H1_v11.md if it has been installed there) and follow its section 0, then "
     "read its section 0D, which holds everything since H-1 v10"),
    ("HARD RULES, binding now (H-1 v10 has them in full):",
     "HARD RULES, binding now (the handover has them in full):"),
]
