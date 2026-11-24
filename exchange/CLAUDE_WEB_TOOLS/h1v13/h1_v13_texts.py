"""The texts of H-1 v13: the counted replacements in H-1 v12 and its blurb, and the items added to section 0E.

What this file is for
    make_h1_v13.py (beside this file) builds H-1 v13 from the installed H-1 v12. The words it puts in are kept
    here, apart from the mechanism, so that a reader can check each against the decision log. Every "old" text
    must occur exactly once in H-1 v12 (or its blurb), read with its line endings set aside; the builder asserts it.

Which part of the project's rules it carries out
    H-1 section 8.5 (a new edition from the exact Git blob by counted replacements, the builder travelling with it).

Which of the project's own modules it uses
    None.

What uses it
    make_h1_v13.py only.
"""

# (old text, new text) for the handover. Each old text occurs exactly once in H-1 v12. @@STATUS@@ is the builder's.
HANDOVER_REPLACEMENTS = [
    ("# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v12\n",
     "# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v13\n"),
    ("**This edition: v12, 25 November 2026, morning (Adelaide, UTC+10:30). OWNER-RATIFIED IN ADVANCE (RAT-51; decision\n",
     "**This edition: v13, 25 November 2026, 08:00 (Adelaide, UTC+10:30). @@STATUS@@** H-1 v12 brought up to date the same\n"
     "morning, at the owner's request (\"lets update hour handover doc and blurb etc fully and do a handover now\n"
     "please\", 07:51; decision log entry 267), so that a new Claude chat can take over: since H-1 v12 the ratification\n"
     "register v0.33 was ratified and installed (RAT-53), the owner decided where the file-form checker belongs, and\n"
     "slice A of build step 3 was resumed (entries 263 to 266). Built from the installed H-1 v12's Git bytes by\n"
     "`exchange/CLAUDE_WEB_TOOLS/h1v13/make_h1_v13.py`: counted replacements, each marked \"v13\", and **four items added\n"
     "to section 0E (13 to 16), which hold everything since H-1 v12**; `H1_v12_TO_v13_DIFFERENCE.txt` beside the builder\n"
     "is the exact difference. Sections 1, 2 and 2A are unchanged (the builder asserts it). **Section 0E and the\n"
     "decision log prevail over every older statement of this file, and within 0E its items 13 to 16 over the\n"
     "earlier ones.** H-1 v12 (RAT-51) and H-1 v11 (RAT-48) stay in `doc/HANDOVER/` as history.\n"
     "`exchange/CONTINUITY_NOW.md` with the decision log carries whatever is newer. It authorises nothing.\n"
     "**The edition it is built from: v12, 25 November 2026, morning (Adelaide, UTC+10:30). OWNER-RATIFIED IN ADVANCE (RAT-51; decision\n"),
    ("prevail.** **This is the installed Claude handover.** H-1 v11 (RAT-48) stays in `doc/HANDOVER/` as history.\n",
     "prevail.** (v13: H-1 v12 was the installed Claude handover until this edition.) H-1 v11 (RAT-48) stays in `doc/HANDOVER/` as history.\n"),
    ("**Replaces:** (v12) H-1 v11 and its blurb (RAT-48), which stay where they are as history, as H-1 v10 (RAT-45) does.\n",
     "**Replaces:** (v13) H-1 v12 and its blurb (RAT-51), which stay where they are as history, as H-1 v11 (RAT-48) and H-1 v10 (RAT-45) do.\n"),
    ("     260) and the lock line (entry 261): section 0E**);\n",
     "     260) and the lock line (entry 261): section 0E**; (v13) **entries 262 to 268 are H-1 v12, the reviewer's H-2 v7\n"
     "     and the register v0.33 (RAT-51 to RAT-53), slice A resumed, and this edition: section 0E items 13 to 16**);\n"),
    ("## 0E. After H-1 v11: the night of 24 November and 25 November 2026 (v12; this section prevails over every older statement, section 0D included)\n",
     "## 0E. After H-1 v11: the night of 24 November and 25 November 2026 (v12, with items 13 to 16 added in v13; this section prevails over every older statement, section 0D included)\n"),
    ("Everything here is from the decision log (entries 244 to 262), the EX messages (EX_308 to EX_315) and the files named.\n"
     "**Next numbers at this edition: EX_316, decision log entry 263, RAT-53.** Fetch `main` and confirm before using any.\n",
     "Everything here is from the decision log (entries 244 to 268), the EX messages (EX_308 to EX_316) and the files named.\n"
     "**Next numbers at this edition (v13): EX_317, decision log entry 269, RAT-56.** Fetch `main` and confirm before using\n"
     "any: the reviewer commits its own files, and did so twice on 25 November while Claude was building.\n"),
    ("   morning and the reviewer installed (item 9). The register edition is overdue and records RAT-45 to RAT-52\n"
     "   (item 10).\n",
     "   morning and the reviewer installed (item 9). (v13) **RAT-53** (entry 265): the ratification register v0.33,\n"
     "   installed, which records RAT-41's install to RAT-52. **RAT-54** (entry 268): this edition, H-1 v13. **RAT-55**\n"
     "   (entry 268): the reviewer's own H-2 v8 (item 13).\n"),
    ("   commits its own EX files and handover. **In force for the reviewer: H-2 v7 (RAT-52),**\n",
     "   commits its own EX files and handover. (v13: **H-2 v8 is now ratified, RAT-55: item 13.**) **In force for the\n"
     "   reviewer when H-1 v12 was written: H-2 v7 (RAT-52),**\n"),
    ("10. **What waits, at this edition.** On the reviewer: its cold read of this handover (item 1). On the owner:\n",
     "10. (v13: **item 15 is the present list;** in this item (a) is under way, item 14, and (c) is done, RAT-53.)\n"
     "    **What waits, at this edition.** On the reviewer: its cold read of this handover (item 1). On the owner:\n"),
    ("- **The register:** `doc/RATIFICATION_REGISTER_v0_32.md`, ratified with this handover (RAT-41; documentary PASS in EX_273).",
     "- **The register:** (v13) `doc/RATIFICATION_REGISTER_v0_33.md` (RAT-53, entry 265; documentary PASS in EX_316), which records RAT-41's install to RAT-52 and the five installs in DEV. Before it: `doc/RATIFICATION_REGISTER_v0_32.md`, ratified with H-1 v8 (RAT-41; documentary PASS in EX_273)."),
    ("  5. The next register edition (v12: **overdue**; it now also records RAT-45 to RAT-52, the conversion and the\n"
     "     lock line), when a code package or a handover next travels (section 1.6): it records RAT-41's\n",
     "  5. The next register edition (v13: **done as register v0.33, RAT-53;** the edition after it records RAT-53's\n"
     "     install and RAT-54), when a code package or a handover next travels (section 1.6): it records RAT-41's\n"),
    ("(v12) US-ASCII; **CRLF** (the file-form standard: a new text file); one final line ending.",
     "(v12, and v13, which is built the same way from H-1 v12's bytes) US-ASCII; **CRLF** (the file-form standard: a new text file); one final line ending."),
    ("\nEnd of H-1 v12.\n", "\nEnd of H-1 v13.\n"),
]

# The new items go in before the table of identities that section 0E already has.
INSERT_BEFORE = ("**Identities added at this edition** (SHA-256 of the Git content at `HEAD`, computed by the builder):\n\n"
                 "| File | SHA-256 |\n|---|---|\n| `doc/FILE_FORM_STANDARD_v0_2.md` |")

# The files whose SHA-256 the new items list (the Git content at HEAD, computed by the builder).
IDENTITY_FILES = [
    'doc/RATIFICATION_REGISTER_v0_33.md',
    'exchange/EX_316_ChatGPT.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v8_CANDIDATE_20261125.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v8_CANDIDATE_introductory_blurb_20261125.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v12.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v12_introductory_blurb.md',
    'exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md',
    'exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/ENVIRONMENT.example.ini',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/Make_Installable.bat',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/INFRA_MANIFEST.ini',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/deploy_command.py',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/install_import_check.py',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/install_readiness.py',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/deploy/make_installable.py',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/src/research/code_identity.py',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/src/research/settings.py',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/tests/test_trees_readiness.py',
    'exchange/CLAUDE_WEB_TOOLS/step3/overlay/tests/test_trees_settings.py',
]

NEW_ITEMS = """13. **(v13) Since H-1 v12: the morning of 25 November 2026 (entries 263 to 268; EX_316).**
    - **The ratification register v0.33 is ratified and installed: `doc/RATIFICATION_REGISTER_v0_33.md` (RAT-53, entry
      265).** It is v0.32 with its version line changed and one new section: RAT-41's install to RAT-52, each with
      its entry, review, installed file, commit and hash; the five installs of code in DEV; what is recorded and
      not ratified. Reviewed in EX_316 (DOCUMENTARY PASS); its two clarifications of wording were made at
      installation (`exchange/CLAUDE_WEB_TOOLS/register/v0_33/`, with the candidate, the builder and both differences).
    - **The owner's decision (entry 265, 07:33): `deploy/file_form.py` is infrastructure, installed into every tree**
      (the manifest's `[files]`, class `other`), not a DEV-side install tool. One checker serves DEV's suite,
      `Make_Installable` and `Check_Tree` in DEV, QA and PROD. The reviewer concurs (EX_316): no duplicate module, and
      it is not to be imported into `forecast`-class code.
    - **This edition (RAT-54, entry 268)** was asked for at 07:51 so that a new chat can take over; the reviewer's
      cold read, owed since H-1 v12, now falls on it.
    - **The reviewer's H-2 v8 (RAT-55, entry 268).** At the owner's word the reviewer brought its own handover up
      to date through entry 266 and committed it as a candidate
      (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v8_CANDIDATE_20261125.md`, with its blurb beside it); it differs from
      H-2 v7 in its header and its chapter 0 only. **The owner ratified it and this edition together, 07:58: "both
      chatgpt and claude are ratified now."** The reviewer installs its own final file; when this edition was
      installed only the candidate was on `main`. `exchange/CONTINUITY_NOW.md` names the reviewer handover in force.
      It names H-1 v12 as the Claude handover, which was true at its cutoff; this edition replaces H-1 v12.

14. **(v13) SLICE A OF BUILD STEP 3: EXACTLY WHERE IT STANDS (entries 264 to 266). Working files; not a package; not
    reviewed; nothing installed.** The files are `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`, laid out as they go into
    the tree: eleven files, **all CRLF, and sitting on `main` as it is now** (the conversion changed
    `deploy/INFRA_MANIFEST.ini`; the slice's copy is merged with it).
    - **How to work on it:** clone `main` into a work folder, then
      `bash exchange/CLAUDE_WEB_TOOLS/step3/sync_and_test.sh <clone> <python> <test modules>` copies the overlay in and
      runs the modules. Never run the slice against the repository clone you commit from.
    - **Written and tested:** `src/research/settings.py` (DEV's entries for QA and PROD, and every cross-tree check
      of the deployment design's section 1) and the rewritten `ENVIRONMENT.example.ini`; `src/research/code_identity.py`
      (reads the manifest's `[install_tool]` list); `deploy/install_import_check.py` (the static import check);
      `deploy/install_readiness.py` (the two readiness markers, written CRLF, **and the file-form checker: nothing in
      the wrong form can be marked ready, and reading readiness makes the same check**); `deploy/make_installable.py`,
      `deploy/deploy_command.py` and `Make_Installable.bat`; the manifest, with the `[install_tool]` section and
      `deploy/file_form.py = other` under `[files]`; the tests `tests/test_trees_settings.py` (32) and
      `tests/test_trees_readiness.py` (40).
    - **The cloud's evidence at entry 266** (Claude's, not Windows'): those two modules with `test_file_form` (52),
      `test_research_manifest` (9) and `test_research_identity` (25), 158 tests, all OK in a clone of `main` with the
      overlay; and, read-only in that clone, **all 40 real variants and the real infrastructure (34 files, 5
      install-tool files, the manifest) pass every readiness check, the form check included.** The whole suite has
      not been run with the slice.
    - **STILL TO WRITE, in this order:** (1) `records\\INSTALLED_FILES.json` (deployment design section 2: every
      installed software file with its SHA-256, each variant's fingerprint, each status file by name only); (2) the
      check of the environment's digest over the fixed inventory (specification section 13; the engine's
      `environment_digest` exists already; on the owner's PC the inventory is 11,997 files, 150.6 seconds on first
      reading and 5.2 when lately read, TASK_T028); (3) `Check_Tree.bat` (specification section 16; deployment design
      sections 1 and 10: read-only; what is installed, each variant's status, what is ready, any drift, the backup
      ZIPs, locks), **with the checker in it** (the standard's section 6: the files on the tree's list of installed
      files, its `ENVIRONMENT.ini`, every status file, and what the project's programs have written under
      `source_data\\`, `results\\research\\` and `records\\`, each by its kind); (4) the launch guard with the process rule
      (deployment design section 9; the build plan's section 4A: the rule and the refusals of the reviewed
      `src\\package_tools\\process_check.py` are kept, the file is not reused; psutil for every process check but the
      restore's; **every program started from an environment is two processes and counts as one**).
    - **To go to the reviewer with the slice:** the narrow, UNRATIFIED amendment of the deployment design's section
      2 ("standard library only" for the install tools; section 0D item 5); and two readings of the
      specification (a variant may import its own listed files as well as its helpers; the tool itself refuses a
      variant that imports an infrastructure file not classed `forecast`).
    - **What the slice changes in DEV when it is one day installed:** the forecasting-code identity stays as it is
      (no forecast is made again); the derived-code digest changes (`settings.py` and `code_identity.py` are of that
      class), which the engine writes into new lines and compares nowhere.
    - **Two things found on the way, to keep in mind.** `tests/research_fixtures.py`, the engine tests' shared
      helper, writes with Python's default line ending, which is CRLF on the owner's PC and LF in the cloud; it is
      not changed: a test that needs files in their form brings its invented tree to form itself (`bring_to_form`
      and `write_crlf` in `tests/test_trees_readiness.py`). And a test that edits a file "afterwards" must append a
      line in its form, or it tests the form check and not what it means to test.
    - **The plan is unchanged** (`step3/STEP3_BUILD_PLAN_v0_1r1.md`): slice A goes to the reviewer as its own package
      on the owner's word; nothing is installed in DEV until slices A to D have passed and been rehearsed. The
      reviewer has said it will assess the completed package, not each increment. The plan gives slice A's plainer
      parts to Opus and slices B and C to Fable; the owner switches.

15. **(v13) What waits now.** On the reviewer: the cold read of this handover, when the owner asks. On the owner:
    nothing. **On Claude, in order:** the four parts of item 14 still to write; slice A's package and its note;
    slices B, C and D; the joined rehearsal; the one install into DEV; QA, the transition check and PROD, each on
    his go; the operations manual's skeleton after build step 3. **Before any of it, the staged takeover of
    section 0 item 4 if this is a new chat.** Apply item 3 throughout: the simplest safe route is said first.

16. **(v13) Two more lessons, and what changed from H-1 v12.** (i) Fetch `main` immediately before installing a
    handover or a register: the reviewer installed its own H-2 v7 while H-1 v12 was being built, and H-1 v12 had
    to be rebuilt to name it. (j) When the owner asks for something "now" and has ratified a like thing in advance
    the same day, his advance word does not stretch to the next document: ask for it (the register, RAT-53, and
    this edition, RAT-54, each had his own word). **Changed from H-1 v12:** the header; section 0 item 2; this
    section's heading, its first lines, items 1 and 10, and these items 13 to 16 with their table; the line on the
    register in section 4.4; section 12.8 item 5; Appendix B.3 and the last line. Nothing else; sections 1, 2 and
    2A are byte for byte H-1 v12's.

**Identities added in v13** (SHA-256 of the Git content at `HEAD`, computed by the builder):

@@IDENTITIES@@

"""

# (old text, new text) for the blurb. Each old text occurs exactly once in H-1 v12's blurb. @@BLURB_STATUS@@ is the builder's.
BLURB_REPLACEMENTS = [
    ("# Introductory blurb for H-1 v12: for a new Claude chat (paste everything below the line)\n",
     "# Introductory blurb for H-1 v13: for a new Claude chat (paste everything below the line)\n"),
    ("The previous Claude chat left you a handover, H-1 v12 (ratified by me in advance on 25 November 2026, RAT-51: H-1 v11 brought up to date, with one new section, 0E; the reviewer had not yet read it when it was installed).",
     "The previous Claude chat left you a handover, H-1 v13 (@@BLURB_STATUS@@: H-1 v12 brought up to date the same morning; its section 0E holds everything since H-1 v11, and items 13 to 16 of that section everything since H-1 v12; the reviewer had not yet read it when it was installed)."),
    ("Step 3's first package (slice A) is the next work.",
     "Step 3's first package (slice A) is the work in hand: part-built as working files, not reviewed, nothing installed; the handover's section 0E item 14 says exactly where it stands."),
    ("doc/HANDOVER/Claude_Primary_Handover_H1_v12.md and follow its section 0, then read its sections 0D and 0E: 0E holds everything since H-1 v11 and prevails over every older statement (its reading order and the staged takeover).",
     "doc/HANDOVER/Claude_Primary_Handover_H1_v13.md and follow its section 0, then read its sections 0D and 0E: 0E holds everything since H-1 v11 and prevails over every older statement, and its items 13 to 16 are the newest (its reading order and the staged takeover)."),
]
