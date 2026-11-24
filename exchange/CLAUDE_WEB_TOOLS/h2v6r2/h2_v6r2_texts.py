"""The texts of the reviewer handover refresh H-2 v6r2: the counted replacements and the new section 0.13.

What this file is for
    make_h2_v6r2.py builds the H-2 v6r2 candidate and its blurb from the reviewer's installed H-2 v6. This file
    holds what changes: for the handover, pairs (the exact old passage of H-2 v6, what stands in its place), each
    old passage occurring exactly once; the new section 0.13; and the same kind of pairs for the blurb.

Which part of the project's rules it carries out
    H-1 v10 section 8.5 (counted replacements, the builder travelling with the candidate).

Which of the project's own modules it uses
    None.

What uses it
    make_h2_v6r2.py, beside it.
"""

# ------------------------------------------------------------------------------------------------ the handover
HANDOVER_REPLACEMENTS = [
    ("# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v6 (OWNER-RATIFIED RAT-46; 24 November 2026)",
     "# Predictive Randomness - ChatGPT Independent Reviewer Handover H-2 v6r2 CANDIDATE (Claude's continuity refresh, "
     "24 November 2026, of the installed H-2 v6, RAT-46)"),
    ("**Status: OWNER-RATIFIED AND INSTALLED (RAT-46, 24 November 2026).** The owner expressly ratified",
     "**Refresh notice (v6r2; written by Claude, the primary designer and coder, on 24 November 2026, evening).** The "
     "reviewer chat that wrote H-2 v6 ended that day, without notice, after committing EX_303. At the owner's request "
     "(decision log entry 232) Claude refreshed H-2 v6 so that a new reviewer chat can be started, as it did on 21 and "
     "23 November 2026 (H-2 v3r10, H-2 v5r1). **This file is the installed H-2 v6, byte for byte, except for:** the "
     "title; this notice; a few status statements of chapter 0, each marked \"v6r2\"; and **one new section, 0.13, "
     "which holds everything that happened after H-2 v6's evidence cutoff.** Sections 0.4 and 0.5 and the inherited "
     "chapters 1-19 are unchanged. The builder (`exchange/CLAUDE_WEB_TOOLS/h2v6r2/make_h2_v6r2.py`) asserts all of "
     "that, and `out/H2_v6_TO_v6r2.diff` beside this file is the exact difference. **It is a CANDIDATE: not ratified, "
     "and no reviewer has checked it.** H-2 v6 stays installed and unchanged in `doc/HANDOVER/`. A new reviewer "
     "should verify this refresh against H-2 v6, the decision log and the repository, and say what it finds. Where "
     "section 0.13 and an older statement of chapter 0 disagree, section 0.13 and the decision log prevail. The "
     "refresh's own evidence cutoff: `main` at `27a18a2` (the reviewer's EX_303), decision log entry 232.\n\n"
     "**Status of H-2 v6, the edition this refresh is built from: OWNER-RATIFIED AND INSTALLED (RAT-46, 24 November "
     "2026).** The owner expressly ratified"),
    ("The owner's RAT-46 decision-log entry is to be recorded by Claude; do not invent its number or assert it has "
     "already been written.",
     "(v6r2: RAT-46 is recorded as decision log entry 216.)"),
    ("and awaits a corresponding append-only decision-log entry by Claude;",
     "and (v6r2) in decision log entry 216;"),
    ("Decision-log recording by Claude is pending at this snapshot.",
     "(v6r2: it is recorded as decision log entry 216.)"),
    ("**Build step 3, NOT built, NOT authorised merely by this handover:**",
     "**Build step 3 (v6r2: the owner gave his GO for its design and cloud coding on 24 November, entry 217; nothing "
     "of it is installed; section 0.13 says where it stands). NOT built, NOT authorised merely by this handover:**"),
    ("Pin code line endings to LF via `.gitattributes` before the first tree.",
     "(v6r2: H-2 v6 said here \"Pin code line endings to LF via `.gitattributes` before the first tree\"; the owner's "
     "later decisions supersede that: section 0.13, the file-form standard.)"),
    ("the next substantive work is **build step 3**, on separate explicit owner GO.",
     "the substantive work is **build step 3**; the owner gave his GO for its design and cloud coding on 24 November "
     "(entry 217; v6r2: section 0.13 says what has been planned, reviewed and decided since), and every operation on "
     "his PC still needs its own GO."),
    ("Claude should record the ratification and installation in the append-only decision log and refresh "
     "`CONTINUITY_NOW.md`; the reviewer does not edit Claude's or the owner's records.",
     "Claude recorded the ratification and installation in the decision log (entry 216) and refreshed "
     "`CONTINUITY_NOW.md`; the reviewer does not edit Claude's or the owner's records. (v6r2: the reviewer chat that "
     "wrote H-2 v6 ended on 24 November 2026, without notice, after committing EX_303; this edition is Claude's "
     "refresh of it for starting a new reviewer chat.)"),
    ("This owner-ratified H-2 v6 has ONE live chapter 0.",
     "This H-2 v6r2 has ONE live chapter 0: that of the owner-ratified H-2 v6, with the few status statements marked "
     "\"v6r2\" changed and the new section 0.13 added by Claude."),
]

SECTION_0_13 = """### 0.13 After H-2 v6: what happened on 24 November 2026 up to this refresh (v6r2; written by Claude; verify it)

Everything here is from the decision log (entries 216 to 232), the EX messages (EX_297 to EX_303) and the files named;
each can be checked there. Hashes are SHA-256. **Next shared numbers at this refresh: EX_304, decision log entry 233,
RAT-47.** Fetch current `main` and confirm before using any.

**1. Records.** RAT-46 is recorded (entry 216). Both handovers were current at 15:52: H-1 v10 (RAT-45) and H-2 v6
(RAT-46). H-1 v10 does not yet know anything of this section; `exchange/CONTINUITY_NOW.md` does.

**2. Build step 3 has the owner's GO (entry 217, 15:53): for design within the ratified documents, cloud coding and
testing, and the reviewed packages. Not for any install, run, tree creation, backup, restore or runner task on his
PC.** The build plan: `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`
(`6eb18f0e38279a9b68e88dec304dbea205a64b62bc8e80bfc8dc9723c39b3195`). Four code slices, each a package for the reviewer: A foundations
(settings of the three trees, readiness markers, `Make_Installable`, the import check, the list of installed files,
the environment digest, `Check_Tree`, the launch guard); B backups, the recovery kit, restore; C `Init_Tree`,
`Install`, `Reinstall_Infra`, `Verify_Tree` and the half-finished states; D the clean-sheet updater
`results_master_v0_3.py`; then E, the transition. **The reviewer's review of the plan:** EX_299 (four findings: the
updater's proof promised byte-identical ledgers; the old process tool is not reusable as a file; QA's first fill was
missing before the transition check; the slices need a joined acceptance), narrowed by EX_300 (psutil is a
legitimate simpler option), all corrected in v0.1r1; **EX_301: FOCUSED PASS of the plan.** It is a working plan, not
a ratified design.

**3. The owner's decisions on the plan (entry 219):** one install into DEV at the end, after the slices have each
passed and been rehearsed together; a probe task first; QA before PROD (`Init_Tree QA`, QA's own `.venv`,
`Run_Research.bat --game BOTH --no-update` in QA, the transition check there, then PROD); the plan to the reviewer.

**4. How Windows' processes are read (entry 222; plan section 4A).** The owner chose: the restore stays standard
library only, as ratified (the kit, the backup and any installed Python); every other process check uses psutil;
if that proves too hard Claude may use psutil for the restore too, saying so first. **The narrow amendment of the
deployment design section 2 ("standard library only" for the install tools) is NOT ratified;** its wording comes
with slice A. EX_301 recommended the same split.

**5. TASK_T028, a probe of three Windows facts, is written, reviewed, and NOT RUN.**
`CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` r1 (`96e2a6cf86873a9f6a1df1f9e9d3ec2c884e3a8f19b767395498b7ab7f88b02c`, CRLF) and its
probe `inbox/TASK_T028_probe.py` r1 (`57fde59dc4f56526c1a73e95e006fee63b80bbffa223206740ee64776c6128bf`, LF). It measures, in a new folder
`D:\\DELETE_ME\\a_p_r_i_r\\T028` under rulebook v0.7 section 2A: how Windows answers a rename, replacement or removal
when something is open; the size and time of a ZIP of the main `.venv` alone (an environment-only proxy: the
scratch tree of TASK_T025 has been deleted by the owner); what psutil and the standard library each read of the
PC's Python processes. **EX_301: RECHECK, three findings (a possible link above the task folder; "background and
wait" over a line that did neither; the process part able to pass with psutil absent); all corrected as r1; EX_302:
cold recheck PASS.** The part that calls Windows through ctypes has run nowhere. **It waits only for the owner's
own go.**

**6. The operations manual (entry 220; EX_298; entries 171, 182).** Deferred until build step 3 is finished and
proved: short, for a human, a practical how-to; the owner's topics are the least it covers; finding and reading the
reports is a necessary topic; a short command cheat sheet as an index is to be considered; Claude and the reviewer
propose its structure together for the owner's approval. Since then the owner added a "Standards" section to it
(entry 230).

**7. Slice A's working files (entries 222, 225), in `exchange/CLAUDE_WEB_TOOLS/step3/overlay/`: NOT a package, NOT
reviewed, nothing installed.** The settings of the three trees (`src/research/settings.py`, with every check of the
deployment design's section 1 across trees) and a rewritten `ENVIRONMENT.example.ini`; the static import check; the
two readiness markers; `Make_Installable`; the manifest's `[install_tool]` section; tests. Two readings of the
specification Claude will put to the reviewer with the slice: a variant may import its own listed files as well as
its helpers; and the tool itself refuses a variant that imports an infrastructure file not classed `forecast`.

**8. The owner's principle (entry 227, his words):** "git should never be used as an operational gatekeeper/checker
nor for gating/checking deployments etc, github is a tool for managing commits and project statuses." It is already
the ratified rule (specification section 2), and no tool of the new system consults Git. The readiness markers are
not tracked by Git.

**9. Line endings: from "LF pinned" to a written standard (entries 226 to 231).** On the owner's disk three files
under `src` are CRLF where Git holds LF; one of them, `src/methods/_common/game_profiles.py`, is `forecast`-class
shared code, so its bytes are part of the identity every list in DEV records. The owner rejected leaving that as
it lies ("a halfway house which will most definitely catch us out later"), asked what Windows' own conventions are,
and directed (entry 230): a written standard listing each kind of file and its exact form; everything conforms, by
a conversion program and its list, done safely; Git's and GitHub's settings to match. **The candidate:**
`exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1_CANDIDATE.md`
(`00ec02b005813b88927ae22d2afef9e83f22efae3555d760363174248c236872`). In short: every text file of the living project is CRLF, whoever wrote
it; the `.jsonl` record lists stay LF, because each line is the canonical encoding whose bytes the hash chain and
the content digests are computed from; every program names the line ending it writes; Git converts nothing
(`* -text`); the project's own checker enforces it; a conversion program works from a list with each file's SHA-256
before and after. **Claude's trial in the cloud** (`TRIAL_CRLF_SUITE_COMPARISON.txt` beside it,
`8baac6b033e2b60fb9f5f1ed6bb2f666bae4e455d7779b9db906c4da9d2e26af`; Claude's evidence, not the reviewer's and not Windows evidence): 669 files
under `src`, `deploy`, `tests` and the root made CRLF in a copy; 732 of 762 tests the same; 30 changed from passing
to failing, all in five `test_mhupa_*` modules, tracing to six files that tests pin to their bytes; with those six
put back, all five modules passed again. **The owner's five decisions (entry 231):** frozen history (what people
only read and no program running in DEV, QA or PROD uses) is left as it is; the `.jsonl` lists stay LF, said so in
the standard and the operations manual; `* -text` for the whole repository; the results' verification records in
`source_data` are converted with everything else; the six files of the retired Mode H release machinery are left
out by name. His principle for the conversion: redo a hash where the conversion needs it; the priority is a safe
conversion and an operational system. Claude carries that out openly: each file's SHA-256 before beside its SHA-256
after, nothing made to look as if it had always been so, no record of the frozen history rewritten. **This replaces
"code line endings pinned LF" in H-2 v6 section 0.6 and in its blurb.**

**10. EX_303, the last message of the reviewer chat that ended (main `27a18a2`,
`bb88b1ca53c560c20360d949550843907c94c4b66c97e5b170b2a1fc6f90172c`): FOCUSED RECHECK of the standard's wording before ratification, not a
rejection of its policy.** Four clarifications: FFS-C01, "everything a tree holds" must not take in the third-party
`.venv`, and the conversion list must say what happens to a tree's own untracked files (`ENVIRONMENT.ini`, status
files, records, grabs and backups); FFS-C02, the table needs rows for Git's own files and extensionless text such
as `LICENSE`, must not call every `.jsonl` log hash-chained, and must refuse (not exempt) an expected-text file
that holds a zero byte, and say what an empty file and an unterminated last line are; FFS-C03, `* -text` at the
root does not govern `GAIS\\`, which has its own attribute files, and "a commit from a PC" wrongly excludes Claude's
cloud commits; FFS-C04, the conversion's rule for a second run (the after-hash: checked and skipped; the
before-hash: converted; anything else: STOP), a backup and a recovery route first, and the boundaries of what the
trial proved. It accepts the six named exceptions. **Claude answers it with a v0.1r1 candidate, its exact
difference and hashes. A new reviewer chat's likely first task, when the owner asks: the focused recheck of that
v0.1r1, and then the owner's ratification of the standard.**

**11. Mode H.** The owner (17:43, entry 230): "I dop not currently care about obsoleted Mode H stuff." Read
narrowly: the retired machinery need not be maintained or made to conform, and is not to veto the standard. **The
binding rule that the sealed Mode H records are never altered is unchanged,** and the candidate standard leaves
them, and every other record of the old system, exactly as they are.

**12. The owner's PC, unchanged since H-2 v6.** DEV is as his first fill left it (commit `5f16b35` installed; research
results under `results\\research\\`). Nothing of build step 3 is installed; no QA or PROD tree exists; nothing has
been converted; `.gitattributes` is as it was; the prevailing OV-1 has not started. Whichever standard is ratified,
`game_profiles.py` changes bytes at the conversion, so DEV's research results are then removed by hand and filled
again once (about 47 minutes), on his own go.

**13. What a new reviewer chat is asked to hold in mind.** The order of work now is: the file-form standard
(recheck, ratification, then the conversion program, the writers, the checker, the Git settings, a sheet and a
rehearsal), before slice A is packaged, because the markers and the list of installed files hash these bytes; the
probe TASK_T028 on the owner's go; then slices A to D, the joined rehearsal, the one install into DEV, QA, the
transition check, PROD. Each week before PROD's first job is one draw of each game that cannot count in the
prevailing OV-1: a reason not to dawdle, and no reason to cut a check.
"""

# --------------------------------------------------------------------------------------------------- the blurb
BLURB_REPLACEMENTS = [
    ("# Introductory blurb - ChatGPT independent reviewer H-2 v6 (RAT-46; 24 November 2026)",
     "# Introductory blurb - ChatGPT independent reviewer H-2 v6r2 CANDIDATE (Claude's continuity refresh of H-2 v6; "
     "24 November 2026)"),
    ("**H-2 v6 is owner-ratified and installed under RAT-46.** When the owner chooses to start a new independent "
     "ChatGPT reviewer chat, paste everything BELOW the divider into that chat. Ratification does not itself start a "
     "new chat or authorise any project operation.",
     "**The reviewer chat that wrote H-2 v6 ended on 24 November 2026, without notice, after committing EX_303.** At "
     "the owner's request Claude refreshed the installed H-2 v6 (RAT-46) as H-2 v6r2: H-2 v6's own text with a few "
     "status statements changed and one new section, 0.13, for everything since. It is a CANDIDATE: not ratified, and "
     "no reviewer has checked it. To start a new independent ChatGPT reviewer chat, paste everything BELOW the "
     "divider into that chat. Starting a chat authorises no project operation."),
    ("read the ENTIRE current installed reviewer handover at "
     "doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md (or the actual ratified install path the owner names). "
     "Read its chapter 0 then inherited rights/history chapters 1-19; verify exact document identity and current "
     "ratification.",
     "read the ENTIRE refreshed reviewer handover at "
     "exchange/CLAUDE_WEB_TOOLS/h2v6r2/out/ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124.md (or the path the "
     "owner names). It is the installed H-2 v6 (doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md, RAT-46) with "
     "a few status statements marked \"v6r2\" changed and a new section 0.13. Claude, the primary designer, wrote that "
     "refresh after your predecessor's chat ended: check it against H-2 v6 with the exact difference beside it "
     "(H2_v6_TO_v6r2.diff), against the decision log and against the repository, and tell the owner what you find. "
     "Read its chapter 0, section 0.13 above all, then inherited rights/history chapters 1-19; verify exact document "
     "identity and what is and is not ratified."),
    ("The reviewer handover now in force is H-2 v6 (RAT-46), finalised from the v6r1 candidate; H-2 v5r1 remains "
     "history.",
     "The reviewer handover in force is H-2 v6 (RAT-46), finalised from the v6r1 candidate; H-2 v5r1 remains history; "
     "H-2 v6r2 is Claude's unratified refresh of H-2 v6."),
    ("Build step 3 is NEXT only on explicit owner GO.",
     "Build step 3 has the owner's GO for design and cloud coding only (decision entry 217, 24 November); nothing of "
     "it is installed, and section 0.13 of the handover says where it stands."),
    ("code line endings pinned LF;",
     "line endings no longer \"pinned LF\" (see SINCE H-2 v6 below);"),
    ("Before substantive work: tell the owner",
     "SINCE H-2 v6 (24 November, afternoon and evening; handover section 0.13 has it in full): the step-3 build plan "
     "v0.1r1 has your predecessor's FOCUSED PASS (EX_301) after four corrections (EX_299, EX_300). The owner decided: "
     "one install into DEV at the end; a probe task first; QA before PROD; the restore's process check standard "
     "library only and every other process check through psutil (the design amendment for that is NOT yet ratified). "
     "The probe TASK_T028 r1 passed your predecessor's cold recheck (EX_302) and has NOT run: it waits for the owner's "
     "go. The owner's principle: Git is never an operational gatekeeper or checker. LINE ENDINGS: the owner directed "
     "a written standard for the form of every kind of file; the candidate is "
     "exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1_CANDIDATE.md (project-owned text CRLF; .jsonl record "
     "lists LF; every program names the ending it writes; Git converts nothing; the project's own checker; a "
     "conversion program with each file's SHA-256 before and after); he decided its five open points (entry 231); "
     "Claude's cloud trial found 732 of 762 tests unchanged and 30 failing in the retired Mode H release machinery, "
     "tracing to six byte-pinned files that the standard leaves out by name. Your predecessor's last message, EX_303, "
     "is a FOCUSED RECHECK of that standard's wording before ratification, with four clarifications (FFS-C01 to "
     "FFS-C04); Claude answers it with a v0.1r1 candidate. YOUR LIKELY FIRST TASK, when the owner asks: the focused "
     "recheck of that v0.1r1. The owner has said he does not currently care about the retired Mode H machinery; the "
     "sealed Mode H records are still never altered. Next shared numbers at the refresh: EX_304, decision log entry "
     "233, RAT-47; fetch and confirm.\n\nBefore substantive work: tell the owner"),
]
