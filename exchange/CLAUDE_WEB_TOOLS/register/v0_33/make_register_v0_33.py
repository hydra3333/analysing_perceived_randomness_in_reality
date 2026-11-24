#!/usr/bin/env python3
"""Builds the ratification register v0.33 from the installed register v0.32.

What this file is for
    The register v0.32 was installed on 22 November 2026 (RAT-41). This script brings it up to date at the owner's
    request (25 November 2026): it reads v0.32 from Git at HEAD (asserted by SHA-256), changes the one version
    line, inserts one new section before "Interpretation and verification", computes every hash that section
    names from Git, and writes into this folder, each in the standard's form (CRLF; the register is UTF-8):
        RATIFICATION_REGISTER_v0_33_<CANDIDATE or FINAL>.md   and   REGISTER_v0_32_TO_v0_33_DIFFERENCE.txt

Which part of the project's rules it carries out
    H-1 section 8.5 (a new edition from the exact Git blob, the builder travelling with it); the register's own
    "Change discipline"; doc/FILE_FORM_STANDARD_v0_2.md section 5 (every text file Claude adds is CRLF).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_register_v0_33.py <repository root> candidate
                                            python3 -I make_register_v0_33.py <repository root> final "<status words>"
It refuses (an assertion) on a wrong input hash, an anchor not found exactly once or a leftover placeholder.
"""
import difflib
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V32 = 'doc/RATIFICATION_REGISTER_v0_32.md'
V32_SHA = 'f59d1911279e7e95a952a14c3a0c68422ba0f4e67f91ffd5369eb73c606c9acb'
INSERT_BEFORE = '## Interpretation and verification\n'
OLD_VERSION = '**Register version:** v0.32, 22 November 2026, OWNER-RATIFIED 22 November 2026, 17:34 (RAT-41,'
NEW_VERSION = ('**Register version:** v0.33, 25 November 2026, @@STATUS@@ (written by Claude from the records), recording '
               'RAT-41\'s install (`53b1056`), RAT-42 to RAT-52, build step 1, the light tidy-up and build step 2 installed in '
               'DEV, the file-form standard and the conversion of DEV to it (`691f58e`, `fe1c310`), and EX_273 to EX_315; '
               'v0.32, 22 November 2026, OWNER-RATIFIED 22 November 2026, 17:34 (RAT-41,')
CANDIDATE_STATUS = 'CANDIDATE: not reviewed and not ratified; register v0.32 (RAT-41) is the installed register until the owner ratifies this one'
# The files whose hashes the new section quotes: {placeholder: path at HEAD, or (commit, path)}.
HASHED = {
    'H1V8': 'doc/HANDOVER/Claude_Primary_Handover_H1_v8.md',
    'R32': V32,
    'RB06': ('4229a13', 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'),
    'H1V9': 'doc/HANDOVER/Claude_Primary_Handover_H1_v9.md',
    'H2V5': 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123.md',
    'RB07': 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md',
    'H1V10': 'doc/HANDOVER/Claude_Primary_Handover_H1_v10.md',
    'H2V6': 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md',
    'FF01': 'doc/FILE_FORM_STANDARD_v0_1.md',
    'H1V11': 'doc/HANDOVER/Claude_Primary_Handover_H1_v11.md',
    'FF02': 'doc/FILE_FORM_STANDARD_v0_2.md',
    'ZIP2': 'exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2.zip',
    'H1V12': 'doc/HANDOVER/Claude_Primary_Handover_H1_v12.md',
    'H2V7': 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_20261125.md',
}

SECTION = """## The new system's first three installs in DEV, the file-form standard and the conversion, and RAT-41's install to RAT-52 (register v0.33)

Paths in this section are from the repository root. In this section, "this register" means register v0.33. Every commit
named here was checked by Claude from GitHub, and every hash was computed by the builder from Git's stored bytes at `HEAD`
(or at the commit named). This section records decisions already taken and events that happened; it makes no new
decision, and nothing in it authorises code, a check, a run, a package or an install. It is kept short on purpose: the
owner's exact words and the detail of each event are in `exchange/DECISIONS/DECISION_LOG.md`, entries 153 to 262, which
this section indexes.

**The position at this edition (read this first).**
- **The new system (RAT-40) is part-built.** In DEV, the owner's repository on E:, three reviewed packages of it are
  installed and proved: build step 1 (the method files' new layout), the light tidy-up, and build step 2 (the research
  engine, with DEV's first fill). **Build step 3** (the trees QA and PROD, installs, backups, restore) has the owner's go
  for design and cloud coding only (entry 217); none of it is reviewed as a package or installed. No QA or PROD tree exists.
- **A standard for the form of every file is in force and DEV conforms to it:** `doc/FILE_FORM_STANDARD_v0_2.md` (RAT-49).
  Every text file of the living project is CRLF and every `.jsonl` file is LF, with the standard's own explicit
  exceptions (`.sh` files, frozen history, `GAIS/`, other people's files such as a tree's `.venv`, the six files it
  leaves out by name, and tests' temporary fixtures); for the project Git converts nothing (`* -text`). The owner
  converted DEV on 24 and 25 November 2026 (commit `691f58e`), and one line was corrected afterwards (`fe1c310`).
- **From this edition on a hash in this register is the hash of the file's bytes as committed** (EX_316's wording). For
  tracked files governed by `-text`, Git stores the bytes committed without line-ending conversion; a clean checkout of
  the same commit has those bytes. `GAIS/` retains its own rules. Untracked and locally generated files are governed by
  their own standard scopes, not by Git. The earlier sections' words "UTF-8 Git-stored file content with LF line
  endings" describe the files as they were committed then, and those files are unchanged; a text file newly added
  within the standard's scope takes the form the standard prescribes (normally CRLF; `.jsonl` LF).
- **The old system's code is still in `src/` beside the new engine.** The sealed Mode H records are unchanged. No science
  switch was turned on; the allowlist is empty; no program ends another process.

**Ratifications since register v0.32, in order.** Each is the owner's; the decision log entry holds his words.

| Number | When (Adelaide); entry | What was ratified | Reviewed in | Installed as; commit; SHA-256 |
|---|---|---|---|---|
| RAT-41 (install) | 22 Nov 2026, 17:34; 153, 154 | H-1 v8, the reviewer's H-2 v4 and register v0.32 (recorded in v0.32 itself; its install is recorded here) | EX_272, EX_273 | `doc/HANDOVER/Claude_Primary_Handover_H1_v8.md` `@@H1V8@@`; `doc/RATIFICATION_REGISTER_v0_32.md` `@@R32@@`; both `53b1056` |
| RAT-42 | 22 Nov 2026, 18:05; 156 | the local runner's rulebook v0.6 | EX_274 | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` at `4229a13`: `@@RB06@@`; superseded by v0.7 |
| RAT-43 | 23 Nov 2026; 174 | H-1 v9 (Claude) and H-2 v5r1 (the reviewer) | entry 174 names the reviews | `doc/HANDOVER/Claude_Primary_Handover_H1_v9.md` `@@H1V9@@`; `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v5r1_20261123.md` `@@H2V5@@`; `e454f36`; both history now |
| RAT-44 | 23 Nov 2026; 192, 195 | the local runner's rulebook v0.7 (a scratch folder on the owner's D: drive for rehearsals; its section 2A) | EX_286, EX_287, EX_289 | `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md`, `063630f`, its version line corrected at the owner's word in `5ed2c7f`: `@@RB07@@`; **in force** |
| RAT-45 | 24 Nov 2026; 215, 216 | H-1 v10 | EX_295, EX_296 | `doc/HANDOVER/Claude_Primary_Handover_H1_v10.md` `@@H1V10@@`; `a6eceb9`; history now |
| RAT-46 | 24 Nov 2026; 216 | the reviewer's H-2 v6 (its corrected candidate v6r1), installed by the reviewer | the reviewer's own; EX_297 | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md` `@@H2V6@@`; `8d7bb1e`; history since RAT-52 |
| RAT-47 | 24 Nov 2026, 19:38; 237 | the file-form standard v0.1 | EX_303, EX_304, EX_305 | `doc/FILE_FORM_STANDARD_v0_1.md` `@@FF01@@`; `6d3a6ac`; **superseded by v0.2 (RAT-49): it held one fault of fact** |
| RAT-48 | 24 Nov 2026, 20:27; 244 | H-1 v11 | EX_306, EX_307 | `doc/HANDOVER/Claude_Primary_Handover_H1_v11.md` `@@H1V11@@`; `9f27bc0`; history since RAT-51 |
| RAT-49 | 24 Nov 2026, 22:01; 253 | **the file-form standard v0.2** (three lines in the root attribute file, so that `GAIS/` keeps its own rules; entry 251) | EX_310, EX_311 | `doc/FILE_FORM_STANDARD_v0_2.md` `@@FF02@@`; `dd95e7d`; **in force** |
| RAT-50 | 24 Nov 2026, 22:59; 258 | for the one conversion of DEV: (a) one attempt, never resumed, the whole project folder put back from the owner's verified copy on a STOP; (b) the package `FILE_FORM_Conversion_v2`; (c) no rehearsal by the runner (his decision of entry 256). The standard is not re-issued. | EX_313, EX_314 | no document; the package's ZIP `exchange/CLAUDE_WEB_TOOLS/conversion/package/FILE_FORM_Conversion_v2.zip` `@@ZIP2@@`; spent: the conversion is done |
| RAT-51 | 25 Nov 2026, 07:15; 262 | H-1 v12, **ratified in advance** ("i ratify your new handover docs in advance") | **not read by the reviewer before installation; its cold read is owed** | `doc/HANDOVER/Claude_Primary_Handover_H1_v12.md` `@@H1V12@@`; `ff1c7a8`; **the installed Claude handover** |
| RAT-52 | 25 Nov 2026; 262 | the reviewer's H-2 v7, **ratified in advance** ("good please update your handover docs now, I ratify them in advance.", as its header quotes him), installed by the reviewer | the reviewer's own; not reviewed by Claude | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v7_20261125.md` `@@H2V7@@`; `1444a9f`, its blurb `4eedbc3`; **the installed reviewer handover** |

**Code installed in DEV since register v0.32.** Each by the owner, from a reviewed package and its sheet, on his own go; each
commit verified by Claude from GitHub. No ratification number belongs to an install: a PASS or a ratified design
authorises none, and each had his separate go.

| What | Commit; entries | What it did | Proved by |
|---|---|---|---|
| Build step 1 | `0aea10a`; 158 to 164 | the method files moved to the family and variant layout; shared helpers to `src/methods/_common/`; no calculation changed | the reviewed sheet on his PC, with the complete equivalence check against every old development record (EX_276, EX_278, EX_280) |
| The light tidy-up | `c7e6ed8`; 165 to 169 | headers, dependency lists and missing comments in the existing method files (RAT-40 note 3); no calculation changed | the reviewed sheet on his PC, with the complete equivalence check |
| Build step 2 | `5f16b35`; 176 to 212 | the research engine in DEV (`src/research/`, `Run_Research.bat`, `Withdraw_Variant.bat`, the manifest, its tests); the old system not changed | rehearsed on Windows by the local runner (TASK_T025 to T027, entries 199 to 208); installed; DEV's first fill; the comparison with the old records `PASS - COMPLETE` (EX_283, EX_285, EX_290, EX_294) |
| The conversion to the file-form standard | `691f58e`; 245 to 260 | 685 files: four new (`deploy/file_form.py`, `src/research/windows_text.py`, two test modules), eight changed in content (the engine's four writers of text now write CRLF; two lines of the old two-site checker; the manifest; `.gitattributes`, three lines; `.gitignore`) and the rest changed in line endings only; DEV's research results removed and filled again | one attempt on the owner's PC (RAT-50); the fill's counts those of build step 2; the comparison with the old records `PASS - COMPLETE`; verified from GitHub against the conversion list (EX_308 to EX_314) |
| The lock file's line | `fe1c310`; 260, 261 | one line of `src/research/job_lock.py` (`O_BINARY`): on Windows the lock file's line ended CR CR LF | the three affected test modules on his PC, 116 tests `OK` (EX_315) |

**The suite's known result in DEV at this edition:** 54 modules, 830 tests; three tests fail, as they did before build
step 1 (`test_gitignore_lines`, and two tests of `test_multigame_reader_contracts`). The whole suite has not been run
since `fe1c310`.

**Recorded, and not ratified.**
- `exchange/CLAUDE_WEB_TOOLS/step3/STEP3_BUILD_PLAN_v0_1r1.md`: build step 3's working plan (EX_299 to EX_301, FOCUSED
  PASS); a plan, not a design, and never put for ratification.
- **A narrow amendment of the deployment design's section 2** ("standard library only" for the install tools; how Windows'
  processes are read, the owner's option A of entry 222, confirmed by TASK_T028, entries 239 to 242): **not ratified**;
  its wording goes to the reviewer with slice A of build step 3.
- Claude's refresh of the reviewer's handover, H-2 v6r2 (entry 232): never ratified; superseded by H-2 v7.
- The local runner's tasks TASK_T025 to TASK_T028 and their reports are in `CLAUDE_CODE_WORKING_FOLDER_TREE/`; a task
  ran on the owner's go and ratified nothing.
- `exchange/DECISIONS/DECISION_LOG.md` and `exchange/CONTINUITY_NOW.md` are living files with no fixed hash.

**The owner's standing directions given since register v0.32** (his words are in the entries named): fix statements found
out of date (entry 153); Git is never an operational gatekeeper or a check of a deployment (entry 227); everything
conforms to the written standards (entry 230); and **"we have absolutely overengineered and wasted time and money"**
(entry 255): the simplest safe route is put to him first.

**Future actions (replacing register v0.32's list; not authorisations).**
1. The reviewer's cold read of H-1 v12, when the owner asks for it; what it finds goes into a next revision.
2. Slice A of build step 3, brought to the file-form standard, then slices B, C and D, the joined rehearsal, one install
   into DEV, QA, the transition check and PROD: each package reviewed, each operation on the owner's own go.
3. The operations manual's skeleton, agreed with the reviewer, after build step 3.
4. The next register edition records this register's own ratification and install, and what follows.

"""


def git_bytes(root: str, path: str, commit: str = 'HEAD') -> bytes:
    """The bytes Git holds for a path at a commit. Refuses (CalledProcessError) a path the commit does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'{commit}:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def write(name: str, text: str) -> str:
    """Write one output file as UTF-8 with every line ending CRLF; return its SHA-256."""
    assert '\r' not in text and text.endswith('\n')
    data = text.replace('\n', '\r\n').encode('utf-8')
    with open(os.path.join(HERE, name), 'wb') as handle:
        handle.write(data)
    return sha(data)


def main(root: str, kind: str, status: str) -> int:
    """Build the register and the difference; print each output's SHA-256; return 0."""
    old_bytes = git_bytes(root, V32)
    assert sha(old_bytes) == V32_SHA, 'not the installed register v0.32'
    old = old_bytes.decode('utf-8')
    section = SECTION
    for key, where in HASHED.items():
        data = git_bytes(root, where[1], where[0]) if isinstance(where, tuple) else git_bytes(root, where)
        assert section.count(f'@@{key}@@') == 1, key
        section = section.replace(f'@@{key}@@', sha(data))
    assert old.count(OLD_VERSION) == 1 and old.count(INSERT_BEFORE) == 1
    new = old.replace(OLD_VERSION, NEW_VERSION.replace('@@STATUS@@', status)).replace(INSERT_BEFORE, section + INSERT_BEFORE)
    assert '@@' not in new
    name = f'RATIFICATION_REGISTER_v0_33_{kind.upper()}.md'
    print(write(name, new), name)
    difference = ''.join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), V32, name))
    print(write(f'REGISTER_v0_32_TO_v0_33_{kind.upper()}_DIFFERENCE.txt', difference),
          f'REGISTER_v0_32_TO_v0_33_{kind.upper()}_DIFFERENCE.txt')
    if kind == 'final':
        # What ratification changed in the reviewed candidate: its bytes are read from the file committed beside this one.
        with open(os.path.join(HERE, 'RATIFICATION_REGISTER_v0_33_CANDIDATE.md'), 'rb') as handle:
            candidate = handle.read().decode('utf-8').replace('\r\n', '\n')
        difference = ''.join(difflib.unified_diff(candidate.splitlines(keepends=True), new.splitlines(keepends=True),
                                                  'RATIFICATION_REGISTER_v0_33_CANDIDATE.md', name))
        print(write('REGISTER_v0_33_CANDIDATE_TO_FINAL_DIFFERENCE.txt', difference),
              'REGISTER_v0_33_CANDIDATE_TO_FINAL_DIFFERENCE.txt')
    return 0


if __name__ == '__main__':
    assert sys.argv[2] in ('candidate', 'final')
    sys.exit(main(sys.argv[1], sys.argv[2], CANDIDATE_STATUS if sys.argv[2] == 'candidate' else sys.argv[3]))
