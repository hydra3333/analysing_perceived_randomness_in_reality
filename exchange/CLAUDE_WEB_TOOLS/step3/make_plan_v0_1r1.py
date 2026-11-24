"""Write the build plan v0.1r1 of build step 3 from v0.1, by named replacements, and the exact difference.

What this file is for
    The reviewer's EX_299 (as narrowed by EX_300) asked four focused corrections of the build plan v0.1, and the
    owner gave his four decisions (decision log entry 219). This script applies each change to the text of v0.1
    as one replacement that must match exactly once, writes STEP3_BUILD_PLAN_v0_1r1.md beside it, and writes the
    unified difference, so that the recheck can be made on the difference alone. v0.1 is not changed.

Which part of the specification it carries out
    None; the plan is a working document for specification v0.6 section 17.4, build step 3.

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_plan_v0_1r1.py   (run in this folder)
"""
import difflib
import hashlib
import sys
from pathlib import Path

OLD_NAME = 'STEP3_BUILD_PLAN_v0_1.md'
NEW_NAME = 'STEP3_BUILD_PLAN_v0_1r1.md'
DIFF_NAME = 'STEP3_BUILD_PLAN_v0_1_TO_v0_1r1.diff'

# Each pair: the exact text of v0.1, and what stands in its place in v0.1r1.
REPLACEMENTS = [
    # --- the title and the note of what changed
    ("first job) - build plan v0.1\n", "first job) - build plan v0.1r1\n"),
    ("ratified documents leave open is marked RECOMMENDED, with the alternative. Section 7 lists what the owner decides.\n",
     "ratified documents leave open is marked RECOMMENDED, with the alternative. Section 7 lists what the owner decided.\n"
     "**v0.1r1 (24 November 2026):** the reviewer's four focused corrections of EX_299, as narrowed by EX_300, are made\n"
     "(S3P-C01: section 5; S3P-C02: sections 4 and 4A; S3P-C03: section 6; S3P-C04: section 6A), and the owner's four\n"
     "decisions are recorded in section 7 (decision log entry 219). Nothing else is changed; v0.1 stays in the\n"
     "repository as it was, and `STEP3_BUILD_PLAN_v0_1_TO_v0_1r1.diff` beside this file is the exact difference.\n"),
    # --- S3P-C02: the process tool is not reused as a file
    ("`Check_Tree.bat`; the launch guard with the process rule (the reviewed `src\\package_tools\\process_check.py` is reused) |",
     "`Check_Tree.bat`; the launch guard with the process rule (the rule and the refusals of the reviewed process tool are kept; the file itself is not reused: section 4A) |"),
    ("- **RECOMMENDED: a short probe task first** (TASK_T028, scratch only, a few minutes), before slices B and C are\n"
     "  coded: on the owner's PC, what the standard library reads from Windows' process table; how a rename behaves when\n"
     "  the old file is open; how long a ZIP of a whole tree with its `.venv` takes and how large it is. These are the\n"
     "  three things the cloud cannot tell, and the state machines are designed around them.\n",
     "- **A short probe task first** (TASK_T028, scratch only, about a quarter of an hour; the owner agreed, entry 219):\n"
     "  on the owner's PC, what the standard library reads from Windows' process table and what psutil reads, side by\n"
     "  side; how a rename, a replacement and a removal behave when a file is open or another program sits in the\n"
     "  folder; how long a ZIP of a whole tree with its `.venv` takes and how large it is. These are the three things\n"
     "  the cloud cannot tell, and the state machines are designed around them. The task file is written\n"
     "  (`CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T028.md` and its probe); it runs only after the reviewer has read\n"
     "  it and on the owner's own go.\n"
     "\n"
     "## 4A. Reading Windows' processes: what is kept, what is not reused, and one question (EX_299 S3P-C02; EX_300)\n"
     "\n"
     "- **The fact (the reviewer is right).** `src\\package_tools\\process_check.py` reads the process table through psutil\n"
     "  and also holds the old system's lock clearances and Mode H figures. It cannot be installed as the new system's\n"
     "  process check. v0.1 said it was \"reused\"; what is kept is **its rule and its refusals**: a Python process whose\n"
     "  details cannot be read is a refusal, never a pass; ancestors are examined; no program ever ends a process.\n"
     "- **Two different questions are asked of the process table** (deployment design section 9):\n"
     "  (1) *the restore:* \"is any Python program at all running on this PC, other than this restore?\" This needs each\n"
     "  process's program name, its parent and its start time, and nothing more. The standard library reads those from\n"
     "  Windows directly, in a few dozen lines.\n"
     "  (2) *every other rule:* \"is another Python process **of this tree** running?\" (its program file is the tree's,\n"
     "  or its working folder is under the tree, or its command line or an ancestor's names the tree). The working\n"
     "  folder and the command line of another process are **not** readable with the standard library except by\n"
     "  hand-written reading of that process's memory, which is exactly the fragile part psutil exists to do.\n"
     "- **Where psutil is available:** in every tree's own environment (it is one of the 39 packages the owner's\n"
     "  environment script installs) and in DEV's. **Where it may not be:** in whatever Python runs a restore from an\n"
     "  unpacked kit when every tree is unusable.\n"
     "- **RECOMMENDED (for the owner; see section 7 item 5):** the restore keeps its ratified contract (the kit, the\n"
     "  backup and any installed Python; standard library only), with its own small reader for question (1); every\n"
     "  other check uses **one** new psutil reader written for the new system. That is two readers, but for two\n"
     "  different questions, and the second is the one already proved in use. It needs one narrow amendment, for\n"
     "  ratification: the deployment design section 2 says the install tools in `deploy\\` are \"standard library\n"
     "  only\", and the same design's section 9 gives them the process rule that needs psutil; the amendment would say\n"
     "  \"standard library only, except the process rule, which uses psutil from the Python that runs the tool\".\n"
     "  *The alternatives:* (a) psutil for the restore too: one reader, but a restore then needs a Python that has\n"
     "  psutil, checked before anything is touched, and the kit's promise \"any installed Python\" is weakened;\n"
     "  (b) the standard library for everything: hand-written memory reading, which Claude advises against.\n"
     "- **Nothing is relaxed either way:** the scopes of section 9 stay as they are, an unreadable process refuses, and\n"
     "  the restore is tested from an unpacked kit with no tree's environment in reach.\n"
     "- TASK_T028 shows both readings on the owner's PC before any of this is coded.\n"),
    # --- S3P-C01: the updater's proof
    ("- **Kept, each with a test that maps to a test of `v0_2`:** the one source and its exact host; the parse; the\n"
     "  overlap with the draws on file; chronology; the version ledger and the verification records; the lock; the\n"
     "  refusal outside PROD (new: by the settings file's role).\n",
     "- **Kept, each mapped and tested** (the reviewer's inventory, EX_299 S3P-C01, to be confirmed line by line\n"
     "  against `v0_2` when slice D begins): the exact official HTTPS host and the final address after every redirect;\n"
     "  no fallback source; refusal of a block or challenge page; the browser's pacing; the date windows and the era\n"
     "  and number validation; the completeness of a source page; chronological, contiguous updates; the overlap with\n"
     "  the draws on file; the integrity of master and ledger; create-only grabs and backups; a correct `NO_CHANGE`;\n"
     "  the verification records; the updater's lock; and the refusal outside PROD (new: by the settings file's role).\n"),
    ("- **Proof:** `v0_2` and `v0_3` run on the same invented source pages (the cases of `v0_2`'s own offline self-test, and\n"
     "  more invented pages) and on the same starting masters give byte-identical masters and ledgers; a table lists\n"
     "  every check of `v0_2` and where it is in `v0_3`, or why it is gone; planted faults in each kept check. `v0_2` is\n"
     "  1,270 lines and its tests compare it with `v0_1` by syntax tree: the same method is used for `v0_3`.\n",
     "- **Proof (corrected, EX_299 S3P-C01; v0.1 wrongly promised byte-identical ledgers and a syntax-tree comparison).**\n"
     "  `v0_2` and `v0_3` are run on the same invented source pages (the cases of `v0_2`'s own offline self-test, and\n"
     "  more) and the same starting masters, `v0_2` in a made-up opened state so that its Mode H precondition is not\n"
     "  what refuses. Then:\n"
     "  - **Equal byte for byte:** the master CSV; and so the accepted draws, in order. **Equal case by case:** whether\n"
     "    each case was accepted or refused.\n"
     "  - **The version ledger and the verification records are compared field by field,** not as bytes: the version\n"
     "    progression, `UPDATE` or `NO_CHANGE`, the master's hash, the range and the counts, the added range, the\n"
     "    content hashes of grabs and backups, and that history is only ever appended to. **The only differences\n"
     "    allowed are a written list of truthful provenance fields** (the tool's version and its own SHA-256; times\n"
     "    and the names made from them). Nothing is normalised away beyond that list, and no tool identity is faked.\n"
     "  - **A refused case leaves master and ledger untouched;** a diagnostic grab it is allowed to keep is recorded\n"
     "    correctly.\n"
     "  - **Old ledger rows stay as they are:** a made-up ledger with rows written by `v0_2`, then an `UPDATE` and a\n"
     "    `NO_CHANGE` by `v0_3`: the old rows are byte for byte unchanged and keep their own tool's name; the new rows\n"
     "    name `v0_3`.\n"
     "  - **No Mode H:** `v0_3` runs with no opening, freeze, holdout, seal or session record present, and a test shows\n"
     "    it neither reads, writes nor asks for one.\n"
     "  - **A table lists every check of `v0_2`** and where it is in `v0_3`, or why it is gone; each kept check has\n"
     "    normal, edge and planted-fault cases on invented data. A syntax-tree comparison is used only for a helper\n"
     "    that really is unchanged; it does not certify the rewrite.\n"),
    ("- **Never by Claude:** a live run. Claude contacts no lottery website. The owner's first real update with `v0_3` is\n"
     "  his own go, in PROD.\n",
     "- **Never by Claude, the reviewer or the runner:** a live run. Claude contacts no lottery website, and the\n"
     "  runner's rulebook forbids the updater in every version, in scratch trees too (v0.7 section 2A item 6). Its\n"
     "  tests use offline, injected pages; on Windows they run only inside the suite. The owner's first real update\n"
     "  with `v0_3` is his own go, in PROD.\n"
     "- **The launcher:** `Run_Results_Updater.bat` today starts `v0_2`. The package of slice D says exactly how it\n"
     "  becomes the PROD-only launcher of `v0_3` behind the new guard, while `src\\results_master_v0_2.py` stays in\n"
     "  DEV unchanged.\n"),
    # --- S3P-C03: the real sequence
    ("- **Then the real sequence, each step the owner's own go** (specification 17.3): `Init_Tree.bat QA`; the transition\n"
     "  check in QA; `Init_Tree.bat PROD`; PROD's first job.\n",
     "- **Then the real sequence, each step the owner's own go** (specification 17.3; corrected, EX_299 S3P-C03: v0.1\n"
     "  left out QA's first fill, without which QA holds no forecast to compare):\n"
     "  1. `Init_Tree.bat QA`: it copies the software and the accepted results, no forecast, score, report or OV-1\n"
     "     record, and stops for the environment.\n"
     "  2. The owner builds QA's `.venv` from a plain CMD window; `Init_Tree.bat QA` again verifies, writes the kit and\n"
     "     attempts the `INIT` backup.\n"
     "  3. **QA's first fill:** `Run_Research.bat --game BOTH --no-update` in QA. `--no-update` because QA's results\n"
     "     come from PROD, which does not exist yet. The fill is retrospective: it starts no prevailing OV-1.\n"
     "  4. **The transition check,** read-only, against the old records kept in DEV: the 20,436 old forecasts compared\n"
     "     on their scientific content (the score of every number, the ranking, TOP and WORST), never on whole-record\n"
     "     digests; the 5,604 old `INSUFFICIENT_HISTORY` records counted apart, each before its variant's first target,\n"
     "     where the new list rightly has no line; old scores, if compared, reported under their own heading. Any\n"
     "     unexpected difference stops the transition for review.\n"
     "  5. `Init_Tree.bat PROD`, its `.venv`, `Init_Tree.bat PROD` again.\n"
     "  6. PROD's first job.\n"
     "  QA first is the recommended order for the transition (and the owner's choice, entry 219); it is not a standing\n"
     "  condition for PROD.\n"
     "\n"
     "## 6A. Before the one install into DEV: the slices joined and proved together (EX_299 S3P-C04)\n"
     "\n"
     "A PASS of each slice does not show that the joined software is safe. Before the cumulative package is put to the\n"
     "owner for DEV, the exact joined files are rehearsed in scratch trees, and the package note answers each of these:\n"
     "\n"
     "- **A with the installed step 2:** every launcher that writes (research, withdrawal, updater) calls the new guard\n"
     "  before its first write: tree and settings, markers, the file inventory, status, the environment's digest, the\n"
     "  job lock and the process rule, and a refusal at every unfinished barrier. The manifest's `[install_tool]` list\n"
     "  and its classes cover every real import, and no forecast-class file is listed as anything else.\n"
     "- **B with the job and with C:** `SNAPSHOT_DUE`, the backup at a job's end and the standing warning at its start\n"
     "  and end are joined to the installed research job. Every attempt of specification 14.1 is covered: a job's\n"
     "  end, the first tree, before and after an install and a reinstall, before and after `Verify_Tree`, and\n"
     "  `Run_Snapshot`. Shown: the whole tree with its `.venv` in the ZIP; every member read back; every source file\n"
     "  read a second time; the quiet checks; a failed `.partial`; no backup named that was not made and verified; the\n"
     "  due flag kept until a verified backup. The kit is not a backup of the tree.\n"
     "- **C with A and B:** an install stays add-only with its one question; a helper mismatch refuses; \"nothing to\n"
     "  do\" is said as such; no QA pass is a gate. A new variant's smoke case must end in a complete forecast for each\n"
     "  game, not merely in a call. The fixed forecast sample and the full check of derived results are two checks.\n"
     "  The suite runs with the target's Python only where the tree's infrastructure is file for file DEV's, and the\n"
     "  tool says so when it is not run; the package says which tests are the new system's, and the three old known\n"
     "  failing tests are named as such, neither passed over nor copied to PROD. The digest's inventory and the\n"
     "  marker's exclusion are those of specification 13; forecast-sample differences after an environment change\n"
     "  are reported for the W-23 review and are not a failed smoke case.\n"
     "- **The infrastructure reinstall:** it refuses any forecast-class file added, changed or removed; it never\n"
     "  overwrites a variant's or a helper's scientific bytes; it shows the full difference in scores and OV-1 before\n"
     "  its question; cutoffs and stale reports are told truthfully when derived content changes; print-outs are made\n"
     "  again when only their presentation changes; and it names no rerun command that step 4 has yet to build. A\n"
     "  half-finished operation stays barred until the same command finishes it, its approved replacement, or the\n"
     "  owner's own restore.\n"
     "- **D with A, C and the results step:** the new updater stands behind the same role, path and guard, its lock\n"
     "  and the `source_data` boundary; it is never started in QA or DEV.\n"
     "- **Also reviewed then:** the joined manifest and exact file inventory, and one same-command way on for every\n"
     "  half-finished state of slice C.\n"),
    # --- section 7: decided
    ("## 7. What the owner decides now\n",
     "## 7. What the owner decided (24 November 2026, 16:03; decision log entry 219), and one question that is open\n"),
    ("1. **Slices and installs** (section 4): four reviewed slices and one install into DEV at the end (recommended), or\n"
     "   an install per slice.\n",
     "1. **Slices and installs** (section 4): four reviewed slices and one install into DEV at the end (recommended), or\n"
     "   an install per slice. **DECIDED: \"one at the end.\"** (The reviewer adds, and Claude agrees: only after section\n"
     "   6A's joined rehearsal, and on the owner's separate go.)\n"),
    ("2. **The probe task first** (section 4): yes (recommended) or no.\n",
     "2. **The probe task first** (section 4): yes (recommended) or no. **DECIDED: yes.** Its run is his own go.\n"),
    ("   20,436 old forecasts equal, so the check in QA is expected to pass; it is still the one made by an installed tree.\n",
     "   20,436 old forecasts equal, so the check in QA is expected to pass; it is still the one made by an installed tree.\n"
     "   **DECIDED: yes, QA first.**\n"),
    ("4. **Whether this plan goes to the reviewer before slice A is coded** (recommended: yes, for its slice boundaries\n"
     "   and section 5), or only with slice A.\n",
     "4. **Whether this plan goes to the reviewer before slice A is coded** (recommended: yes, for its slice boundaries\n"
     "   and section 5), or only with slice A. **DECIDED: yes.** Done: EX_299 and EX_300, answered by this v0.1r1.\n"
     "5. **OPEN, for the owner, after TASK_T028's report:** how Windows' processes are read (section 4A).\n"
     "   Recommended: the restore stays standard library only; every other check uses psutil; one narrow amendment of\n"
     "   the deployment design section 2 for ratification. It is needed before slice A's guard is put to the reviewer.\n"),
    # --- section 8
    ("- What the standard library can read of another process on this Windows (its executable, working folder, command\n"
     "  line, start time): the process rule and the restore depend on it. The probe answers it.\n",
     "- What the standard library can read of another process on this Windows (its program file, parent and start\n"
     "  time), and what psutil can (also its working folder and command line): the process rule and the restore\n"
     "  depend on it (section 4A). The probe shows both.\n"),
]


def main() -> int:
    """Apply every replacement exactly once and write the new plan and the difference; return 0.
    Refuses (assert) if a text of v0.1 is not found exactly once, if a new line of prose is longer than 120
    characters, or if the result is not ASCII."""
    here = Path(__file__).resolve().parent
    old_text = (here / OLD_NAME).read_text(encoding='ascii')
    new_text = old_text
    for old_piece, new_piece in REPLACEMENTS:
        assert old_text.count(old_piece) == 1, f'not exactly once in v0.1: {old_piece[:70]!r}'
        assert new_text.count(old_piece) == 1, f'not exactly once in the text so far: {old_piece[:70]!r}'
        new_text = new_text.replace(old_piece, new_piece)
    old_lines = set(old_text.split('\n'))
    too_long = [line for line in new_text.split('\n')
                if len(line) > 120 and line not in old_lines and not line.startswith(('|', '#'))]
    assert not too_long, f'a new line is longer than 120 characters: {too_long[0][:60]!r}'
    (here / NEW_NAME).write_bytes(new_text.encode('ascii'))
    difference = ''.join(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                              OLD_NAME, NEW_NAME))
    (here / DIFF_NAME).write_bytes(difference.encode('ascii'))
    for name in (OLD_NAME, NEW_NAME, DIFF_NAME):
        print(hashlib.sha256((here / name).read_bytes()).hexdigest(), name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
