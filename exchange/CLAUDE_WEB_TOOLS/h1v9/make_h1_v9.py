#!/usr/bin/env python3
"""Builds the H-1 v9 candidate and its introductory blurb from the installed H-1 v8.

What this file is for
    It brings the ratified Claude handover H-1 v8 up to date after build step 1 and the light tidy-up were installed
    (23 November 2026), as the owner agreed (decision log entry 166). It reads H-1 v8 and its blurb from Git at HEAD,
    replaces whole sections and single passages by counted replacements (each old text must occur exactly once), keeps
    sections 1, 2 and 2A byte for byte, rebuilds Appendix A's hashes from HEAD, and writes
        out/Claude_Primary_Handover_H1_v9.md
        out/Claude_Primary_Handover_H1_v9_introductory_blurb.md
        out/H1_v8_TO_v9.diff  and  out/H1_v8_TO_v9_blurb.diff

Which part of the project's rules it carries out
    H-1 v8 section 8.5 (a new candidate edition from the exact ratified Git blob with counted replacements, the builder
    travelling with the candidate); the owner's standing instruction on out-of-date statements (entry 153).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_h1_v9.py <repository root>
It refuses (an assertion) on any failure: a file missing at HEAD, an anchor not found exactly once, a changed carried
region, a non-ASCII byte, a CR, or an unfilled placeholder.
"""
import hashlib
import os
import subprocess
import sys

# ---- constants -------------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
V8 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v8.md'                      # the installed handover (RAT-41)
V8_SHA = '8230e3dfecca528d185153e46a2173ef8a7a4d8fbc41695cc3b2bbbfcb20c45e'   # as installed and verified at the takeover
V8_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md'
V8_BLURB_SHA = '586ececea64fca65b1ef3872a9fec60f1d7c659e0da408eb61e62d996d556d66'
CARRY_FIRST = '## 1. Roles and workflow (agreed position v0.1r1, ratified)'  # first line of the carried region
CARRY_AFTER = '### 2B. Added since v7r1 (owner, 21 and 22 November 2026)'   # the carried region ends before this
CARRY_SHA = '80987a07aabe734ea35013a10f8b500bafc5b535062dcf020eb5fdbb51764427'  # sections 1, 2 and 2A (H-1 v8 B.3)
OUT = os.path.join(HERE, 'out')
OUT_H1 = 'Claude_Primary_Handover_H1_v9.md'
OUT_BLURB = 'Claude_Primary_Handover_H1_v9_introductory_blurb.md'

# Files listed in Appendix A, in this order (all must exist at HEAD).
ID_PATHS = [
    'doc/Predictive_Randomness_System_Specification_v0_6.md',
    'doc/Predictive_Randomness_Deployment_Design_v0_12.md',
    'doc/CODING_PRACTICES_v0_1.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v8.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122_introductory_blurb.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md',
    'doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md',
    'doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md',
    'doc/RATIFICATION_REGISTER_v0_32.md',
    'review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md',
    'exchange/README.md',
    'exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md',
    'exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md',
    'exchange/EX_271_ChatGPT.md',
    'exchange/EX_274_ChatGPT.md',
    'exchange/EX_276_ChatGPT.md',
    'exchange/EX_277_Claude/EX_277_Claude.md',
    'exchange/EX_278_ChatGPT.md',
    'exchange/EX_279_Claude/EX_279_Claude.md',
    'exchange/EX_280_ChatGPT.md',
    'exchange/CLAUDE_WEB_TOOLS/step1/STEP1_PACKAGE_NOTE_v0_3.md',
    'exchange/CLAUDE_WEB_TOOLS/step1/check_layout_equivalence.py',
    'exchange/CLAUDE_WEB_TOOLS/step1/run_suite.py',
    'exchange/CLAUDE_WEB_TOOLS/step1/compare_suite_reports.py',
    'exchange/CLAUDE_WEB_TOOLS/tidy1/TIDY1_PACKAGE_NOTE_v0_1.md',
    'exchange/CLAUDE_WEB_TOOLS/tidy1/check_comments_only.py',
    'exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py',
    'exchange/CLAUDE_WEB_TOOLS/check_task_commands.py',
    'exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py',
    'exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/tests/test_mhupb_ov1_numeric.py',
    'src/methods/_common/method_table.py',
    'src/methods/Method_Contract_Runner.py',
    'source_data/POWERBALL_results_master.csv',
    'source_data/OZLOTTO_results_master.csv',
]


def git_bytes(root: str, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD. Refuses (CalledProcessError) a path that HEAD does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    """Replace one passage that must occur exactly once. Refuses (assertion) otherwise, naming the passage."""
    count = text.count(old)
    assert count == 1, f'anchor found {count} times: {old[:90]!r}'
    return text.replace(old, new)


def replace_section(text: str, heading: str, next_heading: str, body: str) -> str:
    """Replace everything from a heading line up to (not including) the next heading line, keeping the heading.

    heading, next_heading: whole heading lines, each found exactly once, in that order.
    body: the new text that follows the heading (it ends with a blank line before the next heading).
    """
    start, end = text.find(heading + '\n'), text.find('\n' + next_heading + '\n')
    assert text.count(heading + '\n') == 1 and text.count('\n' + next_heading + '\n') == 1, heading
    assert start < end, heading
    return text[:start] + heading + '\n\n' + body.strip('\n') + '\n' + text[end:]


# ---- the new text ----------------------------------------------------------------------------------------------
HEADER = """# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v9

**Document:** H-1 under the agreed roles position v0.1r1, section 9 item 4.
**Version:** v9 CANDIDATE, 23 November 2026 (Adelaide, UTC+10:30). **H-1 v8 brought up to date** after build step 1
and the light tidy-up were installed, as the owner agreed (decision log entry 166). Built from the installed H-1 v8's
Git bytes by `exchange/CLAUDE_WEB_TOOLS/h1v9/make_h1_v9.py`, with counted replacements; `H1_v8_TO_v9.diff` beside it is
the exact difference. **Sections 1, 2 and 2A are still H-1 v7r1's bytes, unchanged** (the builder asserts it). The
sections rewritten are listed in Appendix B; everything else is v8's text.
**Status:** CANDIDATE, NOT RATIFIED. The installed Claude handover is H-1 v8 (RAT-41) until the owner ratifies this
edition. It authorises nothing.
**Audience:** any later Claude chat that takes over as primary designer and coder; the ChatGPT reviewer chat; the
project owner.
**Repository:** `hydra3333/analysing_perceived_randomness_in_reality`, public GitHub, branch `main`.
**Baseline described:** `main` on 23 November 2026 after the tidy-up's install (`c7e6ed8`) and its record (`6c3a0fa`).
**The method files are now in the new layout** (build step 1, `0aea10a`) **and commented** (the tidy-up, `c7e6ed8`);
everything else under `src/` and `tests/`, the root `.bat` files and `requirements.txt` is still the old system, as at
`cc0ab73`. Nothing of the new system's engine, trees or commands is coded.
**Replaces, once ratified:** H-1 v8 and its blurb (RAT-41), which stay where they are as history.
**Authority:** the ratified documents and the decision log prevail over this handover wherever they differ. This file
summarises and points to them.
**Draw values:** none appear in this file.
"""

S0_ITEM2_OLD = """   - `exchange/DECISIONS/DECISION_LOG.md`, entries 121 to the latest (the owner's own words; entry 147 is RAT-40, entry
     153 is RAT-41);"""
S0_ITEM2_NEW = """   - `exchange/DECISIONS/DECISION_LOG.md`, entries 121 to the latest (the owner's own words; entry 147 is RAT-40, entry
     153 is RAT-41, entry 156 is RAT-42; entries 158 to 169 are build step 1 and the tidy-up);
   - the two installed code packages' notes, which show how a package is built, proved and installed here:
     `exchange/CLAUDE_WEB_TOOLS/step1/STEP1_PACKAGE_NOTE_v0_3.md` and `exchange/CLAUDE_WEB_TOOLS/tidy1/TIDY1_PACKAGE_NOTE_v0_1.md`,
     with the reviewer's findings on the first (`exchange/EX_276_ChatGPT.md`) and its passes (`EX_278`, `EX_280`);"""

S0_ITEM4_OLD = """   EX numbers is the owner's choice: the takeover of 21 November 2026 used none and was recorded in the decision log
   (entry 134)."""
S0_ITEM4_NEW = """   EX numbers is the owner's choice: the takeovers of 21 and 22 November 2026 used none and were recorded in the
   decision log (entries 134, 157)."""

A0_ITEM1_OLD = """1. **Two systems share this repository.** The code under `src/` is the OLD system (the proof-of-concept coordinator,
   the contract runner, Mode H, the walk-forward driver and report tool). The ratified design describes a NEW system
   that is **not coded at all**."""
A0_ITEM1_NEW = """1. **Two systems share this repository.** The code under `src/` is the OLD system (the proof-of-concept coordinator,
   the contract runner, Mode H, the walk-forward driver and report tool), **except that its method files are now in
   the new system's layout** (build step 1) and carry the coding practices' headers (the tidy-up). The old runner
   still computes them, through a table built from the folder tree. The ratified design's engine, trees and commands
   are **not coded at all**."""

A0_ITEM3_OLD = """   log for the last RAT number, the last entry number and the last EX number before using a new one. At this
   edition: the last RAT is RAT-41; the newest EX is EX_273; the newest decision log entry is 153 (RAT-41)."""
A0_ITEM3_NEW = """   log for the last RAT number, the last entry number and the last EX number before using a new one. At this
   edition: the last RAT is RAT-42 (the runner's rulebook v0.6); the newest EX is EX_280; the newest decision log
   entry is 169 (the tidy-up installed), and entry 170 records this candidate."""

A0_NEW_ITEMS_OLD = """9. **No more general design rounds.** The owner and the reviewer both want the effort to go to building and testing
   code (entries 142, 144, 146). A gap found while coding is settled in that step's package, in the leanest way that
   keeps the science right, or put to the owner as one plain question."""
A0_NEW_ITEMS_NEW = A0_NEW_ITEMS_OLD + """
10. **Some tests read the method files as text.** They refuse words such as `open(`, `import math`, `float(`, `numpy`,
    `subprocess` or `contract_` in particular files, and two archive tests pin six E_1 modules byte for byte
    (`tests/test_code3_retirement.py`, `tests/test_e1r3_revision3.py`; the references are never refreshed). Even a
    comment can fail them: run the whole suite after any change to a method file (section 7.1).
11. **`.gitignore` holds `*.log`,** and `git add` skips an ignored file without a word. Name evidence files `.txt`, and
    build every hash table from the bytes Git holds (`git show :<path>`), never from the working copy (EX_276 C03)."""

B0_BODY = """1. **The first study, Mode H, is complete and sealed in both games** (Oz Lotto 15 November 2026, Powerball
   16 November 2026). Its result, in the words agreed for the record (EX_205 section 5; register v0.31): "No
   statistically significant predictive advantage was demonstrated under the predeclared Mode H tests." The sealed
   records are never altered, rerun or rescored. They are an archive, never a gate in normal work, and they are not
   part of the new trees (specification 17.1).
2. **All draws are equal research targets** (owner, 16 and 18 November 2026). The former holdout draws are ordinary
   draws. No holdout is needed for future method development.
3. **The course correction** (owner, 20 and 21 November 2026; EX_258, EX_259; entries 121, 122): families and variants
   only, no revisions; a clean new baseline, nothing destroyed; three separate trees; minimum administrative software.
   The design rounds that followed are EX_260 to EX_271; the reviewer's PASS (DESIGN) is EX_271.
4. **The approach the owner agreed on 16 November 2026** (`exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md`; reviewed
   with conditions in EX_206; in force since RAT-34), unchanged by the redesign:
   - The AI chats may read draw values, the masters and the results. They never write there.
   - Three protections stay: no lottery website and no results search by any AI (the owner's reviewed updater is the
     only source); results count only from the reviewed programs and their logged runs, and anything an AI works
     out in a chat is labelled "suggestive"; method-facing N-1 isolation, forecast identities and append-only records.
   - **Claude's writing:** documents and records are committed and pushed by Claude directly (named paths; fetch and
     fast-forward first; nothing deleted or overwritten): freely under `exchange/` and
     `CLAUDE_CODE_WORKING_FOLDER_TREE/`, and into `doc/` only once reviewed and ratified. **Code and tests never go into
     `src/` or `tests/` from Claude:** they travel as a reviewed package that the owner installs (section 1.6).
   - The reviewer commits its own EX replies to `exchange/` and its own handover files to `doc/HANDOVER/`.
5. **RAT-40 (22 November 2026, 13:33; entry 147).** The owner ratified the system specification v0.6 and the
   deployment design v0.12, with four notes binding on the code: (a) wherever variants are held or results are not
   current, the job says so plainly at its start and at its end, names the cause and gives the exact command; (b)
   `doc/CODING_PRACTICES_v0_1.md`, which **the owner applied to all coding, build step 1 included** (entry 158); (c) a
   light tidy-up of the existing method files after build step 1 is proved and before anything is installed into QA
   or PROD (**done**, item 7); (d) the one test of EX_271 section 3, owed in build step 4.
6. **Build step 1, the folder layout, is INSTALLED and proved** (entries 158 to 164; `main` `0aea10a`, 23 November
   2026). Reviewed in EX_275 to EX_278 (one RECHECK of four narrow corrections). Before it the owner made his own ZIP of
   the whole project folder on E:, with `.git` and the Git-ignored old run folders, on four external drives (entry
   163): it is the way back to the old system (specification 17.2). On his PC: the suite identical before and after;
   **the equivalence check `RESULT: PASS - COMPLETE`**: every old development forecast (Powerball 17,280, Oz Lotto
   8,760) computed again with the moved code and equal by `canonical_content_digest`.
7. **The light tidy-up is INSTALLED and proved** (entries 165 to 169; `main` `c7e6ed8`). 37 method files got the coding
   practices' headers and comments; no code changed. The owner accepted leaving E_1's six byte-pinned modules as they
   are (entry 166). Reviewed in EX_279 and EX_280 (PASS). On his PC: a new comments-only check (`RESULT: PASS`), the
   suite unchanged, and the equivalence check again `RESULT: PASS - COMPLETE`.
8. **What is authorised now:** documents and records. Build step 2 needs the owner's own go (section 10); so does
   every install and every run on his PC.
9. **What is owed** is listed once, in section 12.8.
10. **The chats.** This Claude chat took over on 22 November 2026 from H-1 v8 (HO-2 accepted, entry 157) and did build
    step 1 and the tidy-up. The ChatGPT reviewer chat is the one that took over on 21 November 2026; it reviewed EX_266
    to EX_280. On 23 November 2026 the reviewer committed its own H-2 v5 candidate (section 4.4), and the owner agreed
    that Claude refresh H-1 before build step 2 (entry 166): this edition. The owner has not decided on a chat switch."""

C0_ITEM2_OLD = """2. **Section 1.1, the local runner.** Rulebook v0.5 names the old system's programs. A new edition is owed
   before any rehearsal of the new system (section 8.6)."""
C0_ITEM2_NEW = """2. **Section 1.1, the local runner.** The rulebook is now v0.6 (RAT-42, entry 156): a restrictive baseline that
   names the new system's commands as never run. A narrowly scoped, reviewed amendment is owed before any runner
   rehearsal of the new system (section 8.6)."""

C0_ITEM4_OLD = """4. **Section 1.6, the register.** v0.32 is the newest (RAT-41; section 4.4)."""
C0_ITEM4_NEW = """4. **Section 1.6, the register and the protocol.** Register v0.32 is still the newest (RAT-41; section 4.4); the next
   edition is owed (section 12.8). `exchange/README.md` is now v0.6 (entry 155), where 1.6 says v0.5."""

S3_OLD = """scores per game and forecasts the next draw; and every result as one appended line in a list. It is designed and
ratified, and none of it is coded. It runs on Windows 11 with Python 3.15."""
S3_NEW = """scores per game and forecasts the next draw; and every result as one appended line in a list. It is designed and
ratified; of it, only the method files' layout is built (build step 1). It runs on Windows 11 with Python 3.15."""

S44_OLD = """  reviewer chat was lost. `exchange/CONTINUITY_NOW.md` names the edition in force."""
S44_NEW = """  reviewer chat was lost. **RAT-41 also covers the reviewer's refreshed H-2 v4** (entry 154: main `79406e4`, SHA-256
  `b2837f08f8fd89134aebfbbed5815ca28b00f0ccebd1cb54c92f2f13c50cea2b`; its blurb at `35a2ebf`): those are the bytes in force.
  **H-2 v5** (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5_CANDIDATE_20261123.md` and its blurb, committed by the
  reviewer on 23 November 2026 at `23689ef` and `31db13b`) is a candidate, not ratified. `exchange/CONTINUITY_NOW.md`
  names the edition in force."""

S6_OLD = """- **New in this edition: DEV's working files are the install source.**"""
S6_NEW = """- **Run times measured on the owner's PC (23 November 2026):** the whole suite, one module per process, about 25
  minutes; the equivalence check of every old development forecast about 40 minutes (Powerball about 31, Oz Lotto
  about 9; E_18 and the minimax fits take most of it). In the cloud workspace the suite took about 10 minutes and
  the scored-only equivalence check about 35.
- **New in H-1 v8: DEV's working files are the install source.**"""

S7_BODY = """### 7.1 The installed code

- **The method files are in the new layout** (build step 1, `0aea10a`): `src/methods/E_0nn/` holds each family's
  `core_v1.py` (the shared calculation; E_6 also `beta_bernoulli.py`), `variants.py` (each variant's fixed settings)
  and one folder per variant with `method.py` (calls the core) and `VARIANT.json` (the scientific declaration of
  specification 3.4). Shared helpers are `src/methods/_shared/{recurrence_gaps_v1,occurrence_counts_v1,polynomial_fits_v1}.py`.
  The old contract runner's table of methods is built from the folder tree (`src/methods/_common/method_table.py`;
  `ADAPTERS = build_method_table()` in `Method_Contract_Runner.py`); `contract_adapters/` is gone, E_1's wrapper is
  `E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py`, and E_1's own modules stay where the proof-of-concept suite imports them.
- **The tidy-up** (`c7e6ed8`) gave 37 of those files the coding practices' headers and a comment on every function;
  no code changed. **Six E_1 modules are pinned byte for byte by two archive tests** (section 0A item 10) and were
  left as they are (entry 166).
- Twelve method families, 40 variants per game: E_1 (one variant), E_3 and E_4 (six each), and E_2, E_6, E_7, E_8,
  E_9, E_10, E_17, E_18, E_19 (three each).
- **Everything else** under `src/` and `tests/`, the root `.bat` files and `requirements.txt` is the old system, as at
  `cc0ab73`, apart from step 1's changes named above and the lines it changed in 14 test files for the moved paths.
- **The suite's known result** (owner's PC and cloud, 22 and 23 November 2026): 45 modules, 571 tests; **three tests
  fail, with eight failed assertions**, on `main` since before step 1: `test_mhupa_launchers` `test_gitignore_lines`
  (one; the owner un-ignored a results folder at `cc665ce`; it prints a set, in a different order each run) and in
  `test_multigame_reader_contracts` `test_master_source_and_ledger_file_hashes` (two sub-tests, pinned to the
  version-1 masters) and `test_only_legacy_e1_allowed_at_boundary` (five). On Windows four symlink tests skip
  (section 6). Compare before and after with `compare_suite_reports.py` (section 12.2), test by test.
- The three safety switches are False and the allowlist is empty in `src/`. A fourth, older switch,
  `ENABLE_CONTRACT_REAL_DEVELOPMENT`, is True in the old contract runner (owner, 31 October 2026).

### 7.2 Data and records

- **Masters, version 2:** Powerball draws 1144 to 1591 (448 rows),
  `e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0`; Oz Lotto draws 1474 to 1708 (235 rows),
  `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e`.
- **In Git:** the sealed Mode H records and reports (`c7622fa`); the development and Mode H score records (`cc665ce`);
  the earlier ranking reports; and the development batch records
  (`results/real/development/wf_batches/<GAME>/<batch>/plan.json` and `segment_*.json`), which list every published
  development forecast: 17,280 Powerball and 8,760 Oz Lotto.
- **Not in Git:** the old forecast run folders (26,040 development, three files each, and 800 Mode H) and attempts
  ledgers exist only on the owner's PC, in his backups and in his ZIP of entry 163. 5,838 Powerball and 2,802 Oz Lotto
  development forecasts were never scored, so they exist only there. The transition check of build step 3 reads them;
  **they stay until then** (entry 163; their cleanup is the owner's own act).

### 7.3 Staged work that is not installed and will not be installed as built

- **The three MHUP-B slices** under `exchange/CLAUDE_WEB_TOOLS/mhupb/` (slice 1, EX_231 PASS; slice 2, EX_237 PASS;
  slice 3, EX_242 PASS) implement the weekly-session design that the course correction replaced. They are a source
  of reviewed code and tests to draw on, never a package to install.
- **The OV-1 kernel** is `exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py`
  (`2858075e37d2fed447388c770aafe2de9c6d296cd84808078f4cff8cba8d8234`), with its tests beside
  it. The specification's 1.2 names it as the implementation of OV-1's mathematics; the reviewer accepted its proofs
  P1 to P8 at source level (EX_233). Build step 2 carries it into the new system: reuse it, do not rewrite it; any
  change to it is HIGH work.

### 7.4 The design's working record, and the build's

- `exchange/CLAUDE_WEB_TOOLS/simplify/`: every draft of the specification (v0.1 to v0.6) and of the deployment design
  (v0.7 to v0.12), the exact diff between each pair of editions, the builders, and
  `DRAFT_CONTRADICTIONS_FOR_REVIEWER_v0_1.md`. The specification's section 21 says where each finding and decision landed.
- `exchange/CLAUDE_WEB_TOOLS/step1/` and `tidy1/`: the two installed packages, their builders, tools, notes and
  evidence, including the owner's own outputs (`evidence/owner_pc_2026_11_23/` in each). Section 12.2.

### 7.5 Not tested by anyone

**Nothing of the new system's engine, trees or commands has run.** What has run is the moved and commented method
code, under the old runner, on the owner's PC (section 6 has the times). The specification's section 20 and the
deployment design's section 17 list the uncertainties; the costs still to measure in the first rehearsal are the
derived check at each job, a first full fill, a `Check_Forecasts --all`, a rerun, and a backup of a whole tree with
its environment."""

S86_OLD = """  clones that cannot push, and reports what happened. Its rulebook is `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`
  (v0.5, RAT-30). Its reports are owner-machine evidence, not reviewer evidence and not acceptance.
- **Rulebook v0.5 is written for the old system.** It names the old programs it must never run and holds a
  finished one-task allowance (its section 2A). **Before any rehearsal of the new system a new edition is owed,**
  reviewed and ratified, naming the new commands, with matching deny entries in `.claude/settings.json` that the owner
  edits. Until then the runner can still run the existing suite in a task clone, as task T024 did."""
S86_NEW = """  clones that cannot push, and reports what happened. Its rulebook is `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`
  (v0.6, RAT-42, entry 156). Its reports are owner-machine evidence, not reviewer evidence and not acceptance.
- **Rulebook v0.6 is a restrictive baseline.** It allows nothing new: it names the new system's seventeen commands
  as never run, keeps QA, PROD and their backups out of reach (rule 11), and forbids reading `results/`,
  `source_data/` and `transitory_data/` (rule 5). **Before any runner rehearsal of the new system,** write a narrowly
  scoped amendment for that rehearsal, for review and ratification (EX_274). Three deny lines for
  `.claude/settings.json` are proposed in `exchange/CLAUDE_WEB_TOOLS/rulebook_v0_6/COVER_NOTE.md` section 5; the file is
  the owner's. The runner can still run the existing suite in a task clone, as task T024 did.
- **Build step 1 and the tidy-up did not use the runner.** Their checks read the old records under `results/`, which
  rule 5 forbids it, so they ran as reviewed owner-run sheets (section 12.3)."""

S88_OLD = """**From the redesign (20 to 22 November 2026):**"""
S88_NEW = """**From build step 1 and the tidy-up (22 and 23 November 2026):**

- **A check must say what it covered, not only that nothing differed.** The first equivalence checker could report a
  complete PASS without the never-scored forecasts or for one game (EX_276 C01). Take the list of what must be found
  from an independent record (here the tracked batch segments), require every item, and print `PARTIAL` with each
  reason otherwise. A cloud run that covers only part is called PARTIAL, never PASS.
- **A comparison tool must account for every item or fail closed.** The first suite comparison identified 563 of 571
  tests (EX_276 C02). Count against the tool's own summary and refuse when they differ.
- **`git add` skips ignored files silently** (EX_276 C03; section 0A item 11). Hash from Git's bytes; check every
  named file on `origin/main` after the push.
- **A sheet that says "any FAIL is a STOP" must also say which failures are expected** (EX_276 C04).
- **Make the change mechanical:** a builder from a clean clone, every new word in one file, counted replacements, and
  a direct proof (for the tidy-up, the code with comments and docstrings removed, compared by `ast.dump`). The reviewer
  then reads one file, and the owner's PC repeats the proof.
- **Check each citation against its document while writing.** Four wrong section references and a wrong error type
  were caught that way before any proof ran.
- **A sheet's extraction step must say "extract to `E:\\TEMP`":** the ZIP holds its own top folder, and Windows'
  "Extract all" otherwise nests it one level deeper (entry 169).
- **Push nothing while the owner runs a sheet** that ends with his push: record the go first, then wait.

**From the redesign (20 to 22 November 2026):**"""

S9_OLD = """3. **Code in DEV:** a folder per variant with `method.py` and `VARIANT.json`; shared computation in the family folder
   or in `_shared/`, each helper versioned by its file name (specification 3.2 to 3.4); tests, among them the N-1"""
S9_NEW = """3. **Code in DEV:** a folder per variant with `method.py` and `VARIANT.json`; shared computation in the family folder
   or in `_shared/`, each helper versioned by its file name (specification 3.2 to 3.4; the twelve existing families
   are the worked example since build step 1, section 7.1); tests, among them the N-1"""

S10_BODY = """1. **Done:** H-1 v8, H-2 v4 and register v0.32 ratified (RAT-41); rulebook v0.6 (RAT-42); the takeover of this chat
   (entry 157); **build step 1** (entry 164, `0aea10a`); **the light tidy-up** (entry 169, `c7e6ed8`).
2. **This edition** (H-1 v9), for the reviewer's check and the owner's ratification, as with v8. The reviewer's own
   H-2 v5 candidate is its business; ratifying the two together is the owner's choice.
3. **Build step 2: the research engine, in DEV** (specification sections 3 to 11), on the owner's own go: the lists,
   the job with its fill and catch-up, scoring, the reports, both OV-1 scores (with the kernel of section 7.3), the
   status file and withdrawal; the checks of 5.6A and 5.8 and both header identities from the first day; RAT-40's
   start-and-end warnings. **Settle in that package:** the exact clause list for E2R-1 section 7 (specification 20);
   specification 17.3's stale pointer to the simplification design v0.1 (entry 157 item 6); pinned line endings for
   `src/` wherever a byte-bound marker is first built (section 6). Build it as steps 1 and the tidy-up were built:
   a builder from a clean clone, the whole suite before and after, planted faults, a reviewed package and an owner-run
   sheet (section 12.3).
4. **Build step 3: trees, installs, backups and restore** (specification 12.1 to 12.6, 13, 14.1), then the transition
   check and PROD's first job. **The owner's question on the updater** (the watchpoint below) is put to him before
   that part is coded. Before a runner rehearsal: the narrow rulebook amendment (section 8.6). The old run folders
   stay until the transition check (section 7.2). **After this step PROD exists and forecasts every week, and new
   methods can be added: the main game.**
5. **Build step 4: the laboratory tools** (specification 12.7, 14.2, 7A, 12.8, `Check_Forecasts`), with the test of
   EX_271 section 3. Until it is built, a fault found in shared code is not improvised around: the affected work is
   held, or the owner restores a backup (specification 17.4).
6. **Then, in the owner's order:** new methods and waves; OUTLANDISH_01's family; the housekeeping of section 12.8.

**A watchpoint for build steps 2 and 3** (found on 22 November 2026; register v0.32; EX_273 section 2; entry 157 item
5). The installed code still has checks from the Mode H study that the ratified design does not make a gate:
`src/methods/_common/contract_dispatch.py` and `master_versions.py` consult the opening record
`source_data/HOLDOUT_OPENED_<GAME>.json` for targets at or after the former holdout, and the updater
`src/results_master_v0_2.py` refuses an update for a game that has none (`holdout_opened`, line 157, used at lines
243, 721 and 817),
although specification 7.1 says it runs "unchanged". The reviewer prefers a narrowly reviewed correction in step 3
that removes ONLY the obsolete Mode H precondition and keeps every Lotterywest-GOV source, overlap, chronology,
record, ledger and concurrency check. **The owner decides before it is implemented.** Fresh DEV, QA and PROD trees
must work under RAT-40 with no Mode H opening or seal as a prerequisite; the obsolete record is not silently copied
into a new tree merely to satisfy old code; no genuine source or ledger check is removed. No design change.

**Models (MC-1; suggestions, the owner decides):** Opus for packaging, sheets, task files, records and handovers.
**Fable (High) for the core of step 2** (the list writer and its invariants, the job's fill and catch-up, the derived
check, OV-1's integration), for the install, backup and restore state machines of step 3, for the rerun and
correction steps of step 4, and for any unexplained STOP. Cold reads before a review round may be helpers on Opus.

**Genuinely OPEN** (do not present as decided): the identities, form and order of OUTLANDISH_01's methods; each
remaining catalogue family's formula; E_63 and later identities; whether any of the first study's significance
machinery is used again (section 5.2); the old system's undecided items, which H-1 v7r1 section 10 lists and which
may never be needed."""

S12_INTRO_OLD = """This section describes practice, not rules. **This chat did document work only:** it built no code workspace and
ran no suite. Sections 12.3 and 12.4 are carried from H-1 v7r1 in short form and were not exercised here."""
S12_INTRO_NEW = """This section describes practice, not rules. Section 12.3 is now the practice of build step 1 and the tidy-up, both
installed; section 12.4 is carried from H-1 v7r1 in short form and was not exercised by this chat."""

S121_OLD = """  went" note (P6). The documents themselves stay at their repository paths and are named by path and hash; no zip
  is needed unless a code package travels."""
S121_NEW = """  went" note (P6). The documents themselves stay at their repository paths and are named by path and hash; no zip
  is needed unless a code package travels. **With a code package** (EX_275, EX_277, EX_279): the message is
  `exchange/EX_NNN_Claude/EX_NNN_Claude.md` beside the package ZIP and its member list, the package also extracted
  there, and all three in `exchange/EX_NNN_Claude.zip`; an `assemble_exNNN.py` in the package's tool folder builds
  both hash tables from Git's staged bytes."""

S122_OLD = """New since v7r1: `simplify/` (section 7.4) and `h1v8/` (this edition's template and builder). The workspace paths
inside older scripts are a previous chat's; change them at the top before use."""
S122_NEW = """New since v7r1: `simplify/` (section 7.4), `h1v8/` and `h1v9/` (the handover builders), `register/`, `rulebook_v0_6/`,
and the two installed packages' folders:
- **`step1/`** (build step 1): `make_step1_layout.py` (the layout change from a clean clone), `build_step1_pkg.py`,
  `templates/` (the folder-built method table and the variant `method.py`), and three reusable tools:
  `run_suite.py` (`python run_suite.py <tree> <report folder>`: one `python -B -m unittest -v <module>` per process,
  one report per module and `MODULES.txt`), `compare_suite_reports.py` (`<before> <after>`: identifies every test,
  compares each test's result and each module's counts, fails closed; its last line says whether anything changed),
  and `check_layout_equivalence.py` (`--tree <root> [--game] [--part K/N] [--sample N]`: computes every old development
  forecast again in memory through the runner's own functions and compares `canonical_content_digest`; coverage is
  required against the tracked batch segments; `RESULT: PASS - COMPLETE` only for both games with `MISSING: 0`).
- **`tidy1/`** (the tidy-up): `tidy_texts.py` (every new word), `make_tidy_up.py`, `build_tidy_pkg.py`, and
  `check_comments_only.py` (compares every Python file under `src` and `tests` with a commit, with comments and
  docstrings removed; reusable for any comments-only change).
The workspace paths inside older scripts are a previous chat's; change them at the top before use."""

S123_HEAD_OLD = '### 12.3 Building and rehearsing a code package (carried; not exercised by this chat)'
S123_HEAD_NEW = '### 12.3 Building, proving and installing a code package (as done for build step 1 and the tidy-up)'
S123_BODY = """- **Base tree:** a fresh clone at the base commit. **Dev tree:** a second clone, changed by the package's builder.
  Never the owner's checkout.
- **The Python 3.15 environment** does not exist in a new workspace: `uv python install 3.15`, `uv venv --python 3.15
  <dir>`, then `uv pip install numpy scipy psutil pandas pyahocorasick selenium beautifulsoup4 requests html5lib`
  (the direct packages of `install_upgrade_dependencies_into_venv.bat`; a bare interpreter fails modules on `numpy` and
  `psutil`).
- **The suite:** `run_suite.py` on the base tree and on the dev tree (two background runs at once are fine), then
  `compare_suite_reports.py`; the result needed is "no module and no test changed". E2R-T12 starts ordinary worker
  processes; the owner allows it in Claude's cloud runs (entry 159).
- **Science-preserving changes:** the equivalence check on the dev tree. In the cloud it can only be `PARTIAL` (the
  never-scored forecasts are only on the owner's PC); `--part 1/2` and `--part 2/2` in parallel save time.
- **Planted faults:** for every check the package relies on, plant a fault in a disposable copy and show the check
  STOPs.
- **The package:** `repo_overlay/`, `DELETE_PATHS.txt` if anything is deleted, the read-only verifier made from
  `exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py` (phases `pre`, `post`, `committed`; guarded files), the tools
  the sheet uses, the manifest, and `INSTALL_AND_RUN_SHEET.md` (CRLF) with every count derived from the files. Rehearse
  the install in an LF clone and a `core.autocrlf=true` clone, with planted cases that must STOP.
- **The owner's sheet:** part 1 the baseline suite; part 2 PRE, copy (and `git rm`), POST and any direct proof; part
  3 the suite again and the comparison; part 4 the equivalence check (`PASS - COMPLETE` only); part 5 `git add`,
  commit, COMMITTED, and push only after `COMMITTED PASS`. A paragraph says which baseline failures are expected.
  The owner sends each part's output as he goes; check each before he continues; file the outputs unedited as
  evidence; verify the pushed commit from GitHub against the manifest and the tested tree.
- **Coding practices:** every package says "coding practices met" or lists the exceptions with their reasons."""

S126_OLD = """- The owner is sometimes on a phone only: then give only steps that need no PC."""
S126_NEW = """- The owner is sometimes on a phone only: then give only steps that need no PC.
- He saves a package ZIP to `E:\\TEMP` and extracts it there; the evidence folders of a sheet are `E:\\TEMP\\<name>_evidence`.
  His ZIP of the whole project folder (entry 163) is on four external drives."""

S128_HEAD_OLD = '### 12.8 Open items at this edition (22 November 2026)'
S128_HEAD_NEW = '### 12.8 Open items at this edition (23 November 2026)'
S128_BODY = """The live state is `exchange/CONTINUITY_NOW.md`; it overtakes this list.

- **Waiting on the reviewer:** its check of this candidate, when the owner asks.
- **Waiting on the owner:** ratification of this edition; his go for build step 2; his word on reminders R-007
  (proposed dropped) and R-017 (proposed done) (entry 155); the three deny lines for `.claude/settings.json` when he
  chooses (entry 156).
- **Owed by Claude, in order of need:**
  1. Build steps 2, 3 and 4, each on its go, with what section 10 says each must settle.
  2. The owner's question on the updater's Mode H precondition, before that part of step 3 is coded (section 10).
  3. A narrowly scoped rulebook amendment before any runner rehearsal of the new system (section 8.6).
  4. The test of EX_271 section 3, in build step 4.
  5. The next register edition, when a code package or a handover next travels (section 1.6): it records RAT-41's
     install, RAT-42, build step 1, the tidy-up and what follows.
  6. A new draft of `doc/METHOD_TEMPLATE/` for the new layout, after build step 3.
  7. The measurements of section 7.5, in the first rehearsal.
- **Done since H-1 v8:** the owner's ZIP (entry 163); the suite's result established (section 7.1); the pass over
  `exchange/OWNER_REMINDERS.md` and `exchange/OWNER_ROADMAP.md` (entry 155; two reminders await his word, above).
- **Later, and only when the owner asks:** the deferred performance study (R-006;
  `doc/Deferred_Performance_Engineering_Proposal_v0_1.md`: profile real run times before choosing any speed-up) and the
  simplicity review after full implementation (KISS-1).
- **Small leftovers the owner may choose to clear:** deleting `venv.bak` and Python 3.14; the duplicate exploration
  note in `doc/`; the old EX copies in `review/`; after step 3's transition check, the old run folders."""

S129_OLD = """4. Only after his authorisation, and only when a build step is given its go: set up a workspace (section 12.3) and
   run the whole suite once to prove the tools before any change."""
S129_NEW = """4. Only after his authorisation, and only when a build step is given its go: set up a workspace (section 12.3) and
   run the whole suite once with `run_suite.py` to prove the tools before any change; it should give section 7.1's
   known result."""

APPA_INTRO = """SHA-256 of the Git content at `HEAD` (LF unless noted), computed by the builder. A file cannot name its own hash:
this file's and its blurb's are in the decision log entry that records each edition."""

APPB_BODY = """### B.1 What changed from H-1 v8

| v8 section | In v9 |
|---|---|
| Header | rewritten for the state after the tidy-up; status CANDIDATE |
| 0 First actions | item 2: the newer entries and the two package notes added to the reading list, and the protocol's and rulebook's editions; item 4: the takeover of 22 November 2026 added |
| 0A Things that trip a new chat | item 1: the method files are in the new layout; item 3: the newest numbers; items 10 and 11 added (text-reading tests and pinned E_1 files; `.gitignore` and `*.log`) |
| 0B The state | rewritten: items 1 to 4 kept; item 5 notes (b) and (c) brought up to date; items 6 and 7 (step 1, the tidy-up) new; items 8 to 10 rewritten |
| 0C Notes on sections 1, 2, 2A | items 2 (rulebook v0.6), 4 (register, `exchange/README.md` v0.6) and 6 (the owner's lists) brought up to date |
| 1, 2, 2A | **carried byte for byte** (still H-1 v7r1's bytes) |
| 2B, 4.1 to 4.3, 5.1, 5.2, 5.4, 11 | unchanged |
| 5.3 The owner's decisions | one line: the owner's ZIP is done (entry 163) |
| 3 Project in one paragraph | one sentence: the layout is built |
| 4.4 History and working documents | the refreshed H-2 v4 (entry 154) and the H-2 v5 candidate added |
| 6 Verified technical facts | one line added (run times on the owner's PC and in the cloud) |
| 7 What exists today | rewritten (the installed layout and tidy-up; the suite's known result; the records and run folders; the build's record) |
| 8.6 The local runner | rulebook v0.6 and the narrow amendment; why the build did not use the runner |
| 8.8 Lessons | eight lessons from step 1 and the tidy-up added at the top; the rest unchanged |
| 9 Adding a new method | one clause: the existing families are the worked example |
| 10 Next work | rewritten from step 2 on; the watchpoint now names the owner's question and the reviewer's preference |
| 12 intro, 12.1, 12.2, 12.3, 12.6, 12.8, 12.9 | brought up to date; 12.3 rewritten as the practice of the two installed packages |
| Appendix A | rebuilt from HEAD with the files a new chat now needs |
| Appendix B | this one |

Nothing binding was dropped: every v8 passage that was replaced described a state that has since moved on, and the
decision log entries 154 to 169 hold the record.

### B.2 Known limits

- **Verified with tools for this edition:** every hash in section 4 and Appendix A (computed by the builder from
  `HEAD`); that sections 1, 2 and 2A equal v8's and v7r1's bytes; the layout's counts (40 `VARIANT.json`, 40 `method.py`);
  the suite's and the equivalence check's results (the owner's unedited outputs, filed as evidence).
- **Not re-checked for this edition:** the hashes in section 4.2 and 4.3 beyond the builder's comparison with v8
  (unchanged files); statements about the owner's PC other than those in his outputs.
- Of the reviewer's H-2 v5 candidate Claude read the status lines only; reviewing it is not part of this edition.

### B.3 Integrity

US-ASCII; LF; one final newline. The carried sections 1, 2 and 2A are identical to H-1 v8's and to H-1 v7r1's (the
builder asserts both). Every replacement's old text is found exactly once in H-1 v8. The builder refuses on any failure.

End of H-1 v9."""

S0_ITEM2B_OLD = """   - `exchange/README.md` (the exchange protocol) and `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local runner's
     rulebook; section 8.6 says why it is out of date)."""
S0_ITEM2B_NEW = """   - `exchange/README.md` (the exchange protocol, v0.6) and `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` (the local
     runner's rulebook, v0.6; section 8.6)."""

C0_ITEM6_OLD = """6. **Section 2, the owner's two working lists** (`OWNER_ROADMAP.md`, `OWNER_REMINDERS.md`) were last updated on 18 and
   14 November 2026. Under P3 the roadmap's NOW block points to `CONTINUITY_NOW.md`. A pass over both is owed
   (section 12.8)."""
C0_ITEM6_NEW = """6. **Section 2, the owner's two working lists** (`OWNER_ROADMAP.md`, `OWNER_REMINDERS.md`) were brought up to date on
   22 November 2026 (entry 155). Under P3 the roadmap's NOW block points to `CONTINUITY_NOW.md`. Two reminders await
   the owner's word (section 12.8)."""

S53_OLD = """- **The owner makes one full ZIP of the project folder on E: himself** before phase 1 moves any source file (entry
  131). No tool is built for it. Claude tells him when it is time (section 10)."""
S53_NEW = """- **The owner makes one full ZIP of the project folder on E: himself** before phase 1 moves any source file (entry
  131). No tool is built for it. **Done on 23 November 2026** (entry 163), before build step 1 was installed."""

BLURB_EDITS = [
    ('# Introductory blurb for H-1 v8: for a new Claude chat', '# Introductory blurb for H-1 v9: for a new Claude chat'),
    ("""The previous Claude chat left you a handover, H-1 v8. The project was redesigned from the root in November 2026.
The new design was ratified on 22 November 2026 (RAT-40). None of it is coded or installed unless the
repository says so: the code in src/ is the old system.""",
     """The previous Claude chat left you a handover, H-1 v9. The project was redesigned from the root in November 2026.
The new design was ratified on 22 November 2026 (RAT-40). Build step 1 (the method files' new layout) and the light
tidy-up are installed and proved; the rest of the new system is not coded unless the repository says so, and the
rest of the code in src/ is the old system."""),
    ('doc/HANDOVER/Claude_Primary_Handover_H1_v8.md and follow its section 0',
     'doc/HANDOVER/Claude_Primary_Handover_H1_v9.md and follow its section 0'),
    ('HARD RULES, binding now (H-1 v8 has them in full):', 'HARD RULES, binding now (H-1 v9 has them in full):'),
]


def main() -> int:
    """Build the candidate, its blurb and the two diffs; print their hashes; return 0."""
    root = os.path.abspath(sys.argv[1])
    v8 = git_bytes(root, V8)
    assert sha(v8) == V8_SHA, 'H-1 v8 at HEAD is not the installed edition'
    blurb = git_bytes(root, V8_BLURB)
    assert sha(blurb) == V8_BLURB_SHA, 'the H-1 v8 blurb at HEAD is not the installed edition'
    text = v8.decode('ascii')

    carried = text[text.index(CARRY_FIRST):text.index(CARRY_AFTER)].rstrip('\n')   # as H-1 v8's builder hashed it
    head_end = text.index('\n---\n\n## 0. First actions')
    text = HEADER + text[head_end:]
    text = replace_once(text, S0_ITEM2_OLD, S0_ITEM2_NEW)
    text = replace_once(text, S0_ITEM4_OLD, S0_ITEM4_NEW)
    text = replace_once(text, S0_ITEM2B_OLD, S0_ITEM2B_NEW)
    text = replace_once(text, C0_ITEM6_OLD, C0_ITEM6_NEW)
    text = replace_once(text, S53_OLD, S53_NEW)
    text = replace_once(text, A0_ITEM1_OLD, A0_ITEM1_NEW)
    text = replace_once(text, A0_ITEM3_OLD, A0_ITEM3_NEW)
    text = replace_once(text, A0_NEW_ITEMS_OLD, A0_NEW_ITEMS_NEW)
    text = replace_once(text, '## 0B. The state at this edition (22 November 2026)',
                        '## 0B. The state at this edition (23 November 2026)')
    text = replace_section(text, '## 0B. The state at this edition (23 November 2026)',
                           '## 0C. Sections 1, 2 and 2A are carried unchanged: read them with these notes', B0_BODY)
    text = replace_once(text, C0_ITEM2_OLD, C0_ITEM2_NEW)
    text = replace_once(text, C0_ITEM4_OLD, C0_ITEM4_NEW)
    text = replace_once(text, S3_OLD, S3_NEW)
    text = replace_once(text, S44_OLD, S44_NEW)
    text = replace_once(text, S6_OLD, S6_NEW)
    text = replace_section(text, '## 7. What exists today', '## 8. How to work as primary designer and coder',
                           S7_BODY + '\n\n---\n')
    text = replace_once(text, S86_OLD, S86_NEW)
    text = replace_once(text, S88_OLD, S88_NEW)
    text = replace_once(text, S9_OLD, S9_NEW)
    text = replace_section(text, '## 10. Next work, in order (planned; the owner decides each step)',
                           '## 11. Gates that stay closed', S10_BODY + '\n\n---\n')
    text = replace_once(text, S12_INTRO_OLD, S12_INTRO_NEW)
    text = replace_once(text, S121_OLD, S121_NEW)
    text = replace_once(text, S122_OLD, S122_NEW)
    text = replace_once(text, S123_HEAD_OLD, S123_HEAD_NEW)
    text = replace_section(text, S123_HEAD_NEW, '### 12.4 Claude Code task files', S123_BODY + '\n')
    text = replace_once(text, S126_OLD, S126_NEW)
    text = replace_once(text, S128_HEAD_OLD, S128_HEAD_NEW)
    text = replace_section(text, S128_HEAD_NEW, '### 12.9 The first hour in a new chat', S128_BODY + '\n')
    text = replace_once(text, S129_OLD, S129_NEW)

    rows = ['| File | SHA-256 |', '|---|---|'] + [f'| `{p}` | `{sha(git_bytes(root, p))}` |' for p in ID_PATHS]
    commits = ("Commits named in this file: `c7e6ed8` (the tidy-up installed) and `6c3a0fa` (its record); `0aea10a` (build\n"
               "step 1 installed); `31db13b` and `23689ef` (the reviewer's H-2 v5 candidate); `79406e4` and `35a2ebf` (the\n"
               "refreshed H-2 v4 and its blurb); `cc0ab73` (the old code baseline); `c7622fa` (the Mode H results and version-2\n"
               "masters); `cc665ce` (the score records); `cf1c6d9` (the first commit after the history clean-up). H-1 v8\n"
               "Appendix A names the commits of the design rounds.")
    text = replace_section(text, '## Appendix A. Identities',
                           '## Appendix B. What changed from H-1 v7r1, and where what was dropped now lives',
                           APPA_INTRO + '\n\n' + '\n'.join(rows) + '\n\n' + commits + '\n\n---\n')
    text = replace_once(text, '## Appendix B. What changed from H-1 v7r1, and where what was dropped now lives',
                        '## Appendix B. What changed from H-1 v8')
    start = text.index('## Appendix B. What changed from H-1 v8')
    text = text[:start] + '## Appendix B. What changed from H-1 v8\n\n' + APPB_BODY + '\n'

    assert text[text.index(CARRY_FIRST):text.index(CARRY_AFTER)].rstrip('\n') == carried, 'the carried region changed'
    v7r1 = git_bytes(root, 'doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md').decode('ascii')
    assert carried in v7r1, 'the carried region is no longer H-1 v7r1 bytes'
    assert sha(carried.encode()) == CARRY_SHA, 'the carried region is not the one H-1 v8 B.3 names'
    for check in (text,):
        assert check.isascii() and '\r' not in check and check.endswith('\n') and not check.endswith('\n\n')
        assert '@@' not in check
    new_blurb = blurb.decode('ascii')
    for old, new in BLURB_EDITS:
        new_blurb = replace_once(new_blurb, old, new)
    assert new_blurb.isascii() and '\r' not in new_blurb

    os.makedirs(OUT, exist_ok=True)
    for name, data in ((OUT_H1, text), (OUT_BLURB, new_blurb)):
        with open(os.path.join(OUT, name), 'wb') as f:
            f.write(data.encode('ascii'))
    print('carried sections 1, 2, 2A:', len(carried.splitlines()), 'lines,', sha(carried.encode()))
    for name in (OUT_H1, OUT_BLURB):
        data = open(os.path.join(OUT, name), 'rb').read()
        print(sha(data), len(data), 'bytes', name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
