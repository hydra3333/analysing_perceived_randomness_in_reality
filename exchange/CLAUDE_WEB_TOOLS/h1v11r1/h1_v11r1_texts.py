"""The texts of the Claude handover candidate H-1 v11r1: the counted replacements made in the candidate v11.

What this file is for
    make_h1_v11r1.py builds H-1 v11r1 from the candidate H-1 v11. This file holds what changes: pairs (the exact
    old passage of v11, what stands in its place), each old passage occurring exactly once. They are the two
    narrow corrections and three observations of the reviewer's EX_306, and the events after v11 was written
    (decision log entries 239 to 243). @@REPORT_SHA@@ and @@EX306_SHA@@ stand for hashes the builder computes.

Which part of the project's rules it carries out
    H-1 v10 section 8.5 (counted replacements, the builder travelling with the candidate).

Which of the project's own modules it uses
    None.

What uses it
    make_h1_v11r1.py, beside it.
"""

HANDOVER_REPLACEMENTS = [
    # ---- the edition's own statements
    ("**This edition: v11 CANDIDATE, 24 November 2026, evening (Adelaide, UTC+10:30). H-1 v10 brought up to date the\n"
     "same day,**",
     "**This edition: v11 CANDIDATE, revision r1, 24 November 2026, evening (Adelaide, UTC+10:30). H-1 v10 brought up\n"
     "to date the same day,**"),
    ("standard (RAT-47) and a change of reviewer chat (decision log entries 216 to 238).",
     "standard (RAT-47), a change of reviewer chat and the run of the probe TASK_T028 (decision log entries 216 to\n"
     "243)."),
    ("**It is a CANDIDATE: not ratified, and the reviewer has not read it.**",
     "**It is a CANDIDATE: not ratified.** The reviewer passed v11 for continuity and preservation of authority in\n"
     "EX_306, with two narrow corrections and three observations. **Revision r1** makes them and adds what happened\n"
     "after v11 was written (entries 239 to 243), by `exchange/CLAUDE_WEB_TOOLS/h1v11r1/make_h1_v11r1.py`;\n"
     "`H1_v11_TO_v11r1.diff` beside it is the exact difference for the reviewer's confirmation, and\n"
     "`H1_v10_TO_v11r1.diff` the whole difference from the installed edition."),
    ("**entries 217 to 238 are build step 3's go and\n"
     "     plan, the file-form standard (RAT-47, entry 237) and the change of reviewer chat: section 0D**",
     "**entries 217 to 243 are build step 3's go and\n"
     "     plan, the file-form standard (RAT-47, entry 237), the change of reviewer chat and the probe's run: section\n"
     "     0D**"),
    ("Everything here is from the decision log (entries 216 to 238), the EX messages (EX_297 to EX_305) and the files named.\n"
     "**Next numbers at this edition: EX_306, decision log entry 239, RAT-48.**",
     "Everything here is from the decision log (entries 216 to 243), the EX messages (EX_297 to EX_306) and the files named.\n"
     "**Next numbers at this edition (r1): EX_307, decision log entry 244, RAT-48.**"),
    # ---- EX_306 observation (b): the second Init_Tree in QA
    ("**E** the transition (QA, its own `.venv`, `Run_Research.bat --game BOTH --no-update` in\n"
     "   QA, the transition check there, then PROD).",
     "**E** the transition (`Init_Tree.bat QA`, which stops for the owner to build QA's own `.venv`; `Init_Tree.bat QA`\n"
     "   again; `Run_Research.bat --game BOTH --no-update` in QA; the transition check there; then PROD)."),
    # ---- the probe's answer on the process readers
    ("put its wording to the reviewer\n   with slice A.",
     "put its wording to the reviewer\n   with slice A. (r1) TASK_T028 showed the standard library's reading agreeing "
     "exactly with psutil's on the owner's\n   PC: option A stands, and option B is not needed (entry 240)."),
    # ---- the probe has run
    ("6. **TASK_T028, a probe of three Windows facts: written, reviewed, NOT RUN; it waits for the owner's go.**",
     "6. **TASK_T028, a probe of three Windows facts: RAN on the owner's PC on 24 November 2026, on his go; PASS, every\n"
     "   measurement made (r1; entries 239 to 242).**"),
    ("**Its part that calls Windows through\n"
     "   ctypes has run nowhere:** a fault there stops the task's last step after the other two are recorded. The\n"
     "   install, backup and restore logic of slices B and C is designed around its answers.",
     "The\n"
     "   install, backup and restore logic of slices B and C is designed around its answers. **What it found (entry\n"
     "   240; `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T028.md`):** Windows refuses, wholly, a folder's rename and a\n"
     "   file's replacement or removal while a file in it is open or another process stands in the folder, and lets\n"
     "   them through at once afterwards; 1,000 write-then-replace cycles were never refused; the main `.venv` is\n"
     "   19,059 files and 508.9 MB; the environment digest's inventory took 150.6 seconds on first reading and 5.2\n"
     "   when lately read; its ZIP is 180.2 MB in 80.1 seconds at Deflate level 9 (184.5 MB in 20.7 seconds at level\n"
     "   6); the standard library's reading of the process table agrees exactly with psutil's; and **every Python\n"
     "   program started from an environment is two processes** (the environment's `python.exe` and the base Python\n"
     "   under it), so every process rule counts a pair as one program. **The owner keeps Deflate level 9** (entry\n"
     "   243), against the reviewer's informal preference for level 6. One evening, drives D: and E: only; T: and G:\n"
     "   are measured in the joined rehearsal. After the steps the runner ran one line of its own that its report\n"
     "   does not record (entries 240, 241): no measurement is affected, and the reviewer asked for no rerun. The\n"
     "   scratch folder `D:\\DELETE_ME\\a_p_r_i_r\\T028` may be deleted by the owner."),
    # ---- EX_306 H11-C01: the cause of DEV's refill
    ("**At the conversion `game_profiles.py` changes bytes, so every list in DEV becomes\n"
     "    foreign: DEV's research results and its status files are removed on his own go and filled again (about 47\n"
     "    minutes).**",
     "**The conversion of `forecast`-class files changes the forecasting-code identity, so DEV's existing research\n"
     "    lists become foreign: DEV's research results and its status files are removed on his own go and filled\n"
     "    again (about 47 minutes); a status file that holds anything but ACTIVE is a STOP for his decision, and his\n"
     "    checked pre-conversion copy is the way back.** (r1, EX_306 H11-C01: `game_profiles.py` itself is CRLF on his\n"
     "    disk already, entry 226, and need not change; it is the other `forecast`-class files that do.) **Begun\n"
     "    (entry 242), as working files, not a package:** `exchange/CLAUDE_WEB_TOOLS/conversion/overlay/` holds\n"
     "    `deploy/file_form.py`, the one piece of code with the standard's rule, and `tests/test_file_form.py` (44 tests;\n"
     "    the two that check the real tree fail until it is converted). The search for writes that name no line\n"
     "    ending found two in the project's programs outside the six files left out by name."),
    # ---- EX_306 observation (a): the cheat sheet is to be considered
    ("a command cheat sheet as an index;",
     "a short command cheat sheet in an appendix is to be considered, not decided (r1);"),
    # ---- the reviewer's review of this handover
    ("**In force for the reviewer: H-2 v6 (RAT-46).**",
     "It read this handover's v11 in EX_306 (PASS for continuity; two narrow corrections, made in r1), and the\n"
     "    owner confirmed its established commit rights (entry 243). **In force for the reviewer: H-2 v6 (RAT-46).**"),
    ("16. **What waits, at this edition.** On the owner: his go for TASK_T028 r1; his decision on this H-1 v11. On the\n"
     "    reviewer: nothing.",
     "16. **What waits, at this edition (r1).** On the reviewer: its confirmation of `H1_v11_TO_v11r1.diff`. On the\n"
     "    owner: then his decision on this H-1 v11 (it would be RAT-48)."),
    ("(entries 227, 228).",
     "(entries 227, 228). (h, r1) A task file that leaves the runner a need unmet (how the time is to be written; a\n"
     "    check of its own report) invites an invented command: give the command in the task file (entries 240, 241)."),
    # ---- EX_306 H11-C02: what RAT-46 ratified
    ("(v11) the owner\n   ratified it (RAT-46, entry 216) and the reviewer installed it as H-2 v6; section 0D has what followed.",
     "(v11) the\n   reviewer corrected it as the candidate H-2 v6r1\n"
     "   (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6r1_CANDIDATE_20261124.md`; EX_297); the owner ratified that corrected\n"
     "   candidate (RAT-46, entry 216) and the reviewer installed it as H-2 v6; section 0D has what followed."),
    ("1. **Records.** RAT-46: the reviewer's H-2 v6 (entry 216).",
     "1. **Records.** RAT-46: the reviewer's H-2 v6, ratified as its corrected candidate v6r1 (entry 216)."),
    # ---- EX_306 observation (c): which review each ratified document passed
    ("Each design document is the candidate the reviewer passed in EX_271 with its status paragraph alone changed.",
     "Each of the two design documents (the specification and the deployment design) is the candidate the reviewer\n"
     "passed in EX_271 with its status paragraph alone changed. (v11) The file-form standard is the candidate v0.1r2\n"
     "the reviewer passed in EX_305, ratified as RAT-47, with its status statements changed at installation (the\n"
     "exact difference is in `exchange/CLAUDE_WEB_TOOLS/rat47/`)."),
    # ---- two more identities
    ("| `exchange/CLAUDE_WEB_TOOLS/standards/TRIAL_CRLF_SUITE_COMPARISON.txt` | `8baac6b033e2b60fb9f5f1ed6bb2f666bae4e455d7779b9db906c4da9d2e26af` |\n",
     "| `exchange/CLAUDE_WEB_TOOLS/standards/TRIAL_CRLF_SUITE_COMPARISON.txt` | `8baac6b033e2b60fb9f5f1ed6bb2f666bae4e455d7779b9db906c4da9d2e26af` |\n"
     "| `CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T028.md` (r1) | `@@REPORT_SHA@@` |\n"
     "| `exchange/EX_306_ChatGPT.md` (r1) | `@@EX306_SHA@@` |\n"),
]

BLURB_REPLACEMENTS = [
    ("exchange/CLAUDE_WEB_TOOLS/h1v11/out/Claude_Primary_Handover_H1_v11.md",
     "exchange/CLAUDE_WEB_TOOLS/h1v11r1/out/Claude_Primary_Handover_H1_v11r1.md"),
]
