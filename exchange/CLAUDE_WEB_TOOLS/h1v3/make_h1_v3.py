#!/usr/bin/env python3
"""Make H-1 v3 and its blurb from the ratified H-1 v2 and its blurb (Claude, 15 November 2026).

Usage: python3 -I make_h1_v3.py REPO_ROOT OUT_DIR
Reads doc/HANDOVER/Claude_Primary_Handover_H1_v2.md and its blurb from REPO_ROOT (asserted by SHA-256), applies counted
edits (each old text must occur exactly once) and whole-part replacements from the fragments beside this script, asserts
section 2A is byte-identical, and writes Claude_Primary_Handover_H1_v3.md and its blurb into OUT_DIR (US-ASCII, LF)."""
import hashlib, os, sys

assert len(sys.argv) == 3, 'usage: make_h1_v3.py REPO_ROOT OUT_DIR'
repo, outdir = sys.argv[1:3]
here = os.path.dirname(os.path.abspath(__file__))
H1V2_SHA = '8f15109ff6e789e5760f704e8b9177ba3e745838889008151a51a40234938a30'
H1V2B_SHA = 'f5a0e35df5ef9361c063cb0772827214120fdfff85cea289a4961afc4c8695b5'


def rd(path, sha=None):
    b = open(path, 'rb').read()
    if sha:
        assert hashlib.sha256(b).hexdigest() == sha, f'{path}: not the ratified bytes'
    return b.decode('ascii')


def frag(name):
    t = rd(os.path.join(here, name))
    assert '\r' not in t
    return t


def apply(s, edits):
    for label, old, new in edits:
        n = s.count(old)
        assert n == 1, f'{label}: expected one occurrence, found {n}'
        s = s.replace(old, new)
    return s


def section(s, start, end):
    i = s.index(start); j = s.index(end, i)
    return s[i:j]


src = rd(os.path.join(repo, 'doc/HANDOVER/Claude_Primary_Handover_H1_v2.md'), H1V2_SHA)
s = src
S2A = section(src, '### 2A. ', '## 3. Project in one paragraph')

# ---- header -------------------------------------------------------------------------------------------------------
i = s.index('**Version:** v2, 14 November 2026'); j = s.index('\n', i)
s = s[:i] + ('**Version:** v3, 15 November 2026 (Adelaide, UTC+10:30). A **full edition** built from H-1 v2\'s ratified bytes by '
             'counted edits and whole-part replacements (`exchange/CLAUDE_WEB_TOOLS/h1v3/make_h1_v3.py`), as the owner prefers '
             '(full editions, not layers; section 2). It brings the handover to the checkpoint of 15 November 2026: the '
             'documentation round installed (`5a8527b`); the owner\'s dependency change (`cc0ab73`) and TASK_T024; the '
             'replacement reviewer chat (14 November 2026, evening); the owner\'s decisions of 14 November 2026 (D1-D7, EX_177 '
             'C02 and B01, the working approach P0-P6, OUTLANDISH_01\'s methods); and the first two Mode H prerequisites run and '
             'passed (the POC rerun and the updater\'s offline self-test). It changes no rule; section 1.7 records the working '
             'approach the owner adopted as guidance. Appendix B lists what changed. Author: Claude (the chat that took over on '
             '10 November 2026 and wrote H-1 v2). The project owner ratifies.') + s[j:]
i = s.index('**Status:** OWNER-RATIFIED 14 November 2026, about 14:36'); j = s.index('\n', i)
s = s[:i] + ('**Status:** CANDIDATE, 15 November 2026, for the reviewer\'s documentary review (EX_190) and the owner\'s '
             'ratification; once ratified and installed it replaces H-1 v2 (RAT-31), which stays in `doc/HANDOVER/` as history. '
             'Nothing here grants any run, test, data-access, holdout, termination or Git permission.') + s[j:]
i = s.index('**Baseline described:** `main` at `ac2c063`'); j = s.index('\n', i)
s = s[:i] + ('**Baseline described:** `main` at `a74cfd9` (15 November 2026): the code as installed by MHUP-A (package commit '
             '`2860e86`, release commit `effc179`, 13 November 2026) plus the test-only fix `87c4219` and the owner\'s dependency '
             'installer change `cc0ab73` (no file under `src/`, no root `.bat` and no `requirements.txt` has changed since '
             '`cc0ab73`); documents: H-1 v2, H-2 v2 r1 and register v0.29 at `5a8527b`; exchange records through EX_189; the '
             'owner\'s OUTLANDISH_01 commits under `GAIS/` (outside the code closure). The commit that installs this file cannot '
             'name itself; the next register edition records it.') + s[j:]
i = s.index('**Replaces, for future roles:** H-1 v1r8 and its blurb'); j = s.index('\n', i)
s = s[:i] + ('**Replaces, for future roles:** H-1 v2 and its blurb (RAT-31), kept as history; and, as v2 did, H-1 v1r8, its '
             'deltas and the older editions listed in v1r3\'s header. D-1 and ADD-2 are inputs, not authority.') + s[j:]

EDITS = [
    ('title', '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v2\n',
     '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v3\n'),
    # ---- section 0
    ('0.2 head',
     '2. Read, in order: the introductory blurb that started your chat (`doc/HANDOVER/Claude_Primary_Handover_H1_v2_introductory_blurb.md`); '
     'this file, **including section 0A and section 12 (Working knowledge)**; H-2 (the reviewer\'s handover: once installed, the '
     'reviewer\'s own full edition `ChatGPT_Reviewer_Handover_H2_v2.md`, one file; until then `ChatGPT_Reviewer_Handover_H2_v1r9.md` '
     'in full with its v1r10 delta: what the reviewer checks and its rights); the **current register\'s newest sections** '
     '(register v0.29 and later; v0.24\'s section has the MHUP-1 decisions, v0.25 to v0.28 the MHUP-A round);',
     '2. Read, in order: the introductory blurb that started your chat (`doc/HANDOVER/Claude_Primary_Handover_H1_v3_introductory_blurb.md`); '
     '**`exchange/CONTINUITY_NOW.md`** (the one-page recovery index, kept current after every milestone; section 1.7) and '
     '`exchange/DECISIONS/DECISION_LOG.md`; this file, **including section 0A and section 12 (Working knowledge)**; H-2 (the '
     'reviewer\'s handover: its own full edition `ChatGPT_Reviewer_Handover_H2_v2.md`, r1, installed at `5a8527b`, or a later '
     'edition if the register records one: what the reviewer checks and its rights); the **current register\'s newest sections** '
     '(register v0.30 and later; v0.29\'s section has the decisions of 13 November and the handover round, v0.24\'s the MHUP-1 '
     'decisions, v0.25 to v0.28 the MHUP-A round);'),
    ('0.2 readiness',
     '**the Mode H readiness files** in `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/` with the reviews EX_167 and EX_168;',
     '**the Mode H readiness files** in `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/` with the reviews EX_167, EX_168 and EX_177, '
     'and the owner\'s run records in `exchange/RUNS/`;'),
    ('0.3',
     'in particular, ask which of the readiness decisions D1 to D7 he has made, which preparatory checks have run, and whether '
     'any Mode H approval has been given.',
     'in particular, compare `exchange/CONTINUITY_NOW.md` with what the owner tells you: which preparatory checks have run since '
     'it was last updated (at this edition D1-D7 are decided, and the POC rerun and the updater\'s self-test have passed) and '
     'whether any Mode H approval has been given.'),
    ('0.6',
     '6. Keep a running checkpoint of decisions and hashes at each package boundary, so no state lives only in the chat.',
     '6. Keep `exchange/CONTINUITY_NOW.md` current after every milestone, and a checkpoint of decisions and hashes at each package '
     'boundary, so no state lives only in the chat (P0, section 1.7).'),
    # ---- section 1
    ('1.1 next', 'The owner started the **present reviewer chat** on 6 November 2026 from H-2 v1r9',
     'The owner started the **next reviewer chat** on 6 November 2026 from H-2 v1r9'),
    ('1.1 present',
     'together with its documentary review of this file (EX_172). Treat it exactly as the old ones: same rights, same independence.',
     'together with its documentary review of H-1 v2 (EX_172), and the owner\'s dependency change (EX_177: PASS WITH CORRECTIONS). '
     '**It reached its maximum length on 14 November 2026, about 18:00, after EX_177.** The owner started the **present reviewer '
     'chat** that evening from H-2 v2 r1\'s blurb with its placeholders filled (`exchange/HANDOVER_2026_11_14_REVIEWER/NEW_REVIEWER_START_PASTE.md`). '
     'It verified the rights region from Git\'s bytes, answered Claude\'s twelve blind questions 12 of 12 (EX_178 the questions, '
     'EX_179 its answers, EX_180 the key the owner had held sealed, with Claude\'s comparison) and was accepted by the owner; since '
     'then it has advised on D1-D7 (EX_181) and on the working approach (EX_183), and agreed or checked each run (EX_185, EX_187, '
     'EX_189). Some of its replies are pasted by the owner rather than uploaded; Claude records them as EX files (section 12.1). '
     'Treat it exactly as the old ones: same rights, same independence.'),
    ('1.7', '- **Already-committed files:** if a file a package would add is already committed byte-identical, the verifier treats it '
     'as guarded, not new, and the builder asserts the identity first.\n',
     '- **Already-committed files:** if a file a package would add is already committed byte-identical, the verifier treats it '
     'as guarded, not new, and the builder asserts the identity first.\n' + frag('frag_1_7.md')),
    # ---- section 2
    ('2 bullets', 'add no administrative machinery that does not serve one of those.\n',
     'add no administrative machinery that does not serve one of those.\n'
     '- **Show the reasoning (owner, 14 November 2026):** explain not just the recommendation but why, with the reasonable '
     'alternatives and the uncertainties; the owner sometimes finds something important in them. At each substantial milestone, '
     'the short process note of P6 (section 1.7).\n'
     '- **Chat length, restated (owner, 14 November 2026):** he once lost both AI chats at once in another project. At every stage '
     'judge whether to pause and refresh the handovers, and say so; `exchange/CONTINUITY_NOW.md` (P0) keeps the gap small. Today\'s '
     'reviewer takeover (EX_178-EX_180) showed that the installed handover plus that page is enough to restart a chat.\n'),
    # ---- section 4
    ('4 register',
     'At this edition the installed register is **v0.28** (`doc/RATIFICATION_REGISTER_v0_28.md`, '
     '`79ff491ffebae33715f1d434104324ff8301e6adf78177080c784e5f18a38e62`, installed at `cce4858`); register **v0.29** is written '
     'with this file and records it.',
     'At this edition the installed register is **v0.29** (`doc/RATIFICATION_REGISTER_v0_29.md`, '
     '`03efd2bac52272494a177a2654f6bcc852a3337eb5f506a73a2784064042f752`, RAT-31, installed at `5a8527b`); register **v0.30** is '
     'written with this file and records it.'),
    # ---- section 5.3
    ('5.3 decisions', '- **The owner\'s decisions in register v0.24 (2 and 3 November 2026;',
     '- **The owner\'s decisions of 14 November 2026** (`exchange/DECISIONS/OWNER_DECISIONS_2026_11_14_DOC_ROUND_RAT31.md`, '
     '`exchange/DECISIONS/OWNER_DECISIONS_2026_11_14b_C02_AND_REVIEWER.md` and `exchange/DECISIONS/DECISION_LOG.md` entries 1 to 5; '
     'register v0.30 has each): RAT-31 (H-1 v2, H-2 v2 r1, register v0.29; the old handovers left in place); dependency upgrades '
     'stay an always-review topic (W-23); the replacement reviewer accepted; EX_177 C02 closed without a `pip check` (the '
     'installer\'s own output is gone; a separate ChatGPT conversation went through it with the owner, which is the owner\'s report, '
     'not evidence held here); **D1-D7 as recommended** (section 10, item 3); **the working approach P0-P6** (section 1.7); '
     '**OUTLANDISH_01\'s method family** into this project\'s method backlog, probably first, only through the normal route '
     '(section 10, item 6); **B01 closed as a scoped W-23 acceptance** of the dependency change only (section 5.4). Each decision '
     'authorises only what it names.\n'
     '- **The owner\'s decisions in register v0.24 (2 and 3 November 2026;'),
    # ---- section 5.4
    ('5.4 deps',
     'The owner\'s data tools have not yet been run under 3.15 (the updater\'s offline self-test is a prerequisite before Approval 1).',
     '**The owner\'s dependency change of 14 November 2026** (`cc0ab73`; the installer now upgrades every package on every run): '
     'TASK_T024 (ENV PASS, 90 distributions, 571 tests PASS) and the POC rerun of the same night were accepted by the owner as a '
     '**scoped W-23 acceptance for that change only** (decision log entry 5; never "W-23 PASS"; the timeout, Ctrl+C, memory-stress '
     'and other lifecycle cases not run, their risk accepted as not reliably quantifiable). Any rerun of the installer before the '
     'first Approval 1 means T024 again and a new expected digest; the owner plans no more installs and will ask Claude first '
     '(OUTLANDISH_01 uses this venv too). The updater\'s offline self-test passed under 3.15 on 14 November 2026 (13/13).'),
    ('5.4 freeze', 'A pull only after checking that every incoming path is under `exchange/`.',
     'A pull only after checking that every incoming path is under `exchange/`. The owner\'s OUTLANDISH_01 commits stage '
     '`GAIS/OUTLANDISH_01/` by name, never `git add -A` (after Approval 2 it would stage the updated master and ledger, D5).'),
    # ---- section 6
    ('6 digest',
     'the environment digest of the owner\'s venv was `966a27926d23e6764d17a058d0cefaefc320786837f4f7eab58a611883b9b31a` at T016 '
     '(13 November 2026; 27 distributions, no orphan).',
     'the environment digest of the owner\'s venv is `5bf4eb8a36ddb9063fbcb27ff1b692d38de3847321518e563f70c7219999a3f9` '
     '(TASK_T024, 14 November 2026, after the owner\'s dependency change `cc0ab73`; 90 distributions, no orphan; it was '
     '`966a27926d23e6764d17a058d0cefaefc320786837f4f7eab58a611883b9b31a` at T016 with 27 distributions). Approval 1\'s manifest '
     'must show the T024 value; any other is a STOP.'),
    # ---- section 7
    ('7.1 row', 'tests only, outside the closure (EX_165, EX_166, T023 PASS; register v0.27) |\n',
     'tests only, outside the closure (EX_165, EX_166, T023 PASS; register v0.27) |\n'
     '| `cc0ab73` | The owner\'s dependency change (not a package) | `install_upgrade_dependencies_into_venv.bat` edited and run by the '
     'owner, 14 November 2026: 39 direct packages, every package upgraded on every run; the venv now holds 90 distributions. '
     'TASK_T024 PASS (report `811d0cc`); EX_176, EX_177; scoped W-23 acceptance (section 5.4) |\n'),
    ('7.4 T024', 'T016 (Appendix J step 10 on a barrier-free copy) and T023 (the installed `main` with the fix) each 571 pass',
     'T016 (Appendix J step 10 on a barrier-free copy), T023 (the installed `main` with the fix) and T024 (after the owner\'s '
     'dependency change) each 571 pass'),
    ('8.6 T024', 'T023 (the post-install test fix: PASS, `179699c`).',
     'T023 (the post-install test fix: PASS, `179699c`); T024 (the environment after the owner\'s dependency change: '
     '`exchange/CLAUDE_WEB_TOOLS/deps_2026_11_14/env_freeze_check.py` ENV PASS, 90 distributions, digest `5bf4eb8a36dd...`, and '
     'the whole suite, 571 pass with 4 symlink skips: PASS, report `811d0cc`).'),
    ('7.1 docs', 'register v0.28 at `cce4858`.',
     'register v0.28 at `cce4858`; H-1 v2, H-2 v2 r1, their blurbs and register v0.29 at `5a8527b` (RAT-31; the owner\'s install, '
     'COMMITTED PASS).'),
    ('7.6 tools', 'the owner\'s data tools under 3.15;',
     'the owner\'s data tools under 3.15 beyond the updater\'s offline self-test (13/13 PASS, 14 November 2026);'),
    ('7.6 poc', 'the Windows POC suite after MHUP-A\'s launcher change (R-015 (b), drafted, not run); ', ''),
    ('7.6 note', '(Walk-forward batches, `Run_Experiment.bat` with the contract runner and the report tool have now run on Windows, owner-run.)',
     '(Walk-forward batches, `Run_Experiment.bat` with the contract runner and the report tool have now run on Windows, owner-run. '
     'The Windows POC suite and the launchers\' byte-code refusals after MHUP-A\'s change passed on 14 November 2026, R-015 (b), '
     'EX_186; the timeout case was excluded.)'),
    # ---- section 10
    ('10 digest', 'and the environment digest beginning `966a27926d23`;',
     'and the environment digest beginning `5bf4eb8a36dd` (TASK_T024);'),
    ('10 item 6', '6. **Then, in the owner\'s order:** the efficiency items after WF-1C',
     '6. **Then the methods still to do, and the rest, in the owner\'s order:** first, probably, **OUTLANDISH_01\'s method family** '
     '(owner, 14 November 2026, decision log entry 3: developed and run in `GAIS/OUTLANDISH_01/` with its own ChatGPT chat, but not '
     'usable here as it is; each method comes in only through this project\'s normal route: an identity decision and a catalogue '
     'amendment for E_63 onward, design review, N-1 isolation, rework to the method contract, release, and Q7; its OUTLANDISH runs '
     'are not evidence here); then the efficiency items after WF-1C'),
    ('10 backlog', 'the final performance study only when the owner activates it (R-006; roadmap item 22).',
     'the final performance study only when the owner activates it (R-006; roadmap item 22). The ideas backlog (P5, section 1.7) '
     'starts after Mode H.'),
    ('10 open', 'the owner\'s D1 to D7; walk-forward preregistration;',
     'walk-forward preregistration; the identities, form and order of OUTLANDISH_01\'s methods;'),
    # ---- section 11
    ('11', 'no Windows POC rerun, updater self-test or official-page check without its own go;',
     'no official-page check, backup step or tree check without its own go (the POC rerun and the updater\'s self-test ran on '
     '14 November 2026, each on its own go);'),
    # ---- section 12
    ('12.1', 'At this edition the newest is EX_175 (Claude\'s check of the reviewer\'s H-2 v2 r1); check before taking the next.',
     'At this edition the newest is EX_190 (Claude: this edition and register v0.30 for review); check before taking the next. A '
     'reviewer reply the owner pastes into the chat instead of uploading is recorded as `EX_NNN_ChatGPT.md`: a header saying so, '
     'then the text unchanged below a rule (EX_185, EX_187, EX_189). An owner run\'s CMD window is recorded unchanged in '
     '`exchange/RUNS/`.'),
    ('12.6', 'that is expected, never a reason to reset, restore or clean.\n',
     'that is expected, never a reason to reset, restore or clean.\n'
     '- **The owner\'s OUTLANDISH_01 work** (`GAIS/OUTLANDISH_01/`, with its own ChatGPT chat; outside the reviewed line and the '
     'code closure) uses this project\'s `.venv`. The owner plans no further package installs and will ask Claude first (14 November '
     '2026): any install changes the environment digest, which before Approval 1 means T024 again and after it is forbidden until '
     'both seals. He commits that work with `git pull --ff-only`, then `git add GAIS/OUTLANDISH_01/`, never `-A`. A pull after a '
     'local commit makes a harmless merge commit (`a6c2894`, 14 November 2026).\n'),
    ('12.9', 'At this edition: the documentation round\'s review and install; then the owner\'s readiness decisions.',
     'At this edition: `exchange/CONTINUITY_NOW.md`\'s NOW section says what is waiting.'),
    # ---- Appendix A
    ('A h1v2', '| H-1 v1r8 (predecessor; OWNER-RATIFIED 4 November 2026, DOC-11) |',
     '| H-1 v2 (predecessor; OWNER-RATIFIED 14 November 2026, RAT-31; installed at `5a8527b`) | '
     '`doc/HANDOVER/Claude_Primary_Handover_H1_v2.md`, `8f15109ff6e789e5760f704e8b9177ba3e745838889008151a51a40234938a30`; its '
     'blurb `f5a0e35df5ef9361c063cb0772827214120fdfff85cea289a4961afc4c8695b5` |\n'
     '| H-1 v1r8 (OWNER-RATIFIED 4 November 2026, DOC-11; replaced by H-1 v2) |'),
    ('A v1r10r3', '(working supplement to v1r8, RAT-29; replaced by this edition)', '(working supplement to v1r8, RAT-29; replaced by H-1 v2)'),
    ('A h2v1r9', '| H-2 v1r9 (the reviewer handover in force; OWNER-RATIFIED 6 November 2026, RAT-25;',
     '| H-2 v1r9 (OWNER-RATIFIED 6 November 2026, RAT-25; replaced by H-2 v2 r1;'),
    ('A h2v2',
     '| H-2 v2 r1 (the reviewer\'s own full edition, replacing H-2 v1r9 and its deltas once installed; EX_172, Claude\'s factual check '
     'EX_173, r1 EX_174, Claude\'s diff check EX_175) | `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md` and '
     '`..._v2_introductory_blurb.md`; their final hashes are in register v0.29\'s table.',
     '| H-2 v2 r1 (the reviewer handover in force; OWNER-RATIFIED 14 November 2026, RAT-31; installed at `5a8527b`; its header still '
     'reads CANDIDATE r1, and the register decides its status; its rights region is H-2 v1r9\'s, unchanged) | '
     '`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md`, `dee6e106957e0c4f918349510fe948e98d180c7d784159eecfae9ee166045803`; its '
     'blurb `e607f114d8ee00cea623180136a0980aee08c9512c00ef76b341ee407098ca11`; the filled-in starter text used on 14 November 2026, '
     '`exchange/HANDOVER_2026_11_14_REVIEWER/NEW_REVIEWER_START_PASTE.md`, `8334967adf923e506ca47925a80df7ee0a07bfbffbf39d7aa285a83010d6e6ac`.'),
    ('A reg', '| Register v0.28 (installed at `cce4858`) |',
     '| Register v0.29 (RAT-31; installed at `5a8527b`) | `doc/RATIFICATION_REGISTER_v0_29.md`, '
     '`03efd2bac52272494a177a2654f6bcc852a3337eb5f506a73a2784064042f752` |\n'
     '| Register v0.28 (installed at `cce4858`) |'),
    ('A sheet',
     '| The Mode H readiness sheet, reviewed draft r2a (EX_168 PASS; not authorised) | '
     '`exchange/CLAUDE_WEB_TOOLS/modeh_readiness/APPROVAL_1_READINESS_SHEET_DRAFT.md`, as stored '
     '`7f85d98fc948499b0841e5de9546bb801d649c01dd87528d3176738eca71b583`; the POC rerun instructions r3 '
     '`c0f1c59f38290dc53773efa534f95df1c8df285aa9520797d98a9ea3af99959a`;',
     '| The Mode H readiness sheet, reviewed draft r2c (EX_168 PASS; r2b and r2c from EX_176 and EX_177; not authorised) | '
     '`exchange/CLAUDE_WEB_TOOLS/modeh_readiness/APPROVAL_1_READINESS_SHEET_DRAFT.md`, as stored '
     '`8f31c5ba1fd12984ce266f52e1e27a77d7208164e1974895bf9f774a4af357a1`; the POC rerun instructions r3 '
     '`c0f1c59f38290dc53773efa534f95df1c8df285aa9520797d98a9ea3af99959a` (Git blob `1105ff1c6c37f8be9bbb99e8b833dfd8dfa0a097`; '
     'run 14 November 2026, PASS);'),
    ('A records', '| The history clean-up crosswalk (6 November 2026) |',
     '| The owner\'s decision records of 14 November 2026 | `exchange/DECISIONS/OWNER_DECISIONS_2026_11_14_DOC_ROUND_RAT31.md` '
     '`1ea13f7772059972806836dfbccf019d5ccb7aaf095bf91379c81169235ced44`; `..._2026_11_14b_C02_AND_REVIEWER.md` '
     '`7ba931c6d2cc1e216e851afb73bd3feba6243ab70371edffaa08e6becc62d6ac` (as stored); the living decision log '
     '`exchange/DECISIONS/DECISION_LOG.md` and the recovery index `exchange/CONTINUITY_NOW.md` (living files: no fixed hash; Git '
     'keeps their history) |\n'
     '| The owner\'s dependency change and its evidence | `install_upgrade_dependencies_into_venv.bat` at `cc0ab73`, '
     '`c45cc336b758c39d6ccf33269fc2d1e96dd508192719c638bcc2416096f388b3`; TASK_T024\'s report '
     '`CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T024.md` (`811d0cc`), '
     '`a68a05771e4dfb06cda610bec881e80dba5facfaa48ee5441e33c10780b900ee` |\n'
     '| The owner\'s runs of 14 November 2026 (CMD windows, as stored) | the POC rerun '
     '`exchange/RUNS/POC_R015b_2026_11_14_owner_window.txt`, `8179ca7d56d0378e57ba4902f63bef10ea94042e0f21ed393f9c6ccb16fbb6d1`; '
     'the updater self-test `exchange/RUNS/SELFTEST_2026_11_14_owner_window.txt`, '
     '`62b37f5c14d16715ac5d788b5129cf3cf8ff1d26ea237464d57b44f030a596da` |\n'
     '| The history clean-up crosswalk (6 November 2026) |'),
]
s = apply(s, EDITS)

# ---- whole-part replacements ----------------------------------------------------------------------------------------
i = s.index('1. **Done since v1r8 (4 to 14 November 2026):**'); j = s.index('   - **Per game, each a separate go,', i)
s = s[:i] + frag('frag_10_head.md') + s[j:]
i = s.index('### 12.8 Open items at this edition (14 November 2026)'); j = s.index('### 12.9 The first hour in a new chat', i)
s = s[:i] + frag('frag_12_8.md') + s[j:]
i = s.index('## Appendix B. Changes in v2, and where everything went')
s = s[:i] + frag('frag_appB.md')

assert section(s, '### 2A. ', '## 3. Project in one paragraph') == S2A, 'section 2A changed'
s.encode('ascii')
assert '\r' not in s and s.endswith('\n') and not s.endswith('\n\n')
for stale in ('966a27926d23`;', 'reviewed draft r2a, is the operating text', 'EX_175 (Claude'):
    assert stale not in s, f'stale text left: {stale}'

# ---- the blurb -----------------------------------------------------------------------------------------------------
b = rd(os.path.join(repo, 'doc/HANDOVER/Claude_Primary_Handover_H1_v2_introductory_blurb.md'), H1V2B_SHA)
BLURB = [
    ('title', '- goes with H-1 v2\n', '- goes with H-1 v3\n'),
    ('written',
     'Written by Claude on 14 November 2026 with H-1 v2, the full consolidated edition that replaces H-1 v1r8 and all its deltas\n'
     '(OWNER-RATIFIED 14 November 2026, RAT-31). The ChatGPT reviewer chat that took over on 6 November 2026 is in place\n'
     'and checks the new Claude chat\'s first reply.',
     'Written by Claude on 15 November 2026 with H-1 v3, the full edition that replaces H-1 v2 (its status is in the register).\n'
     'The ChatGPT reviewer chat that took over on 14 November 2026 is in place and checks the new Claude chat\'s first reply.'),
    ('rec date', '(Claude\'s recommendation, 14 November 2026)', '(Claude\'s recommendation, 15 November 2026)'),
    ('before',
     '**Before you paste it:** fill in which of the readiness decisions D1 to D7 you have made and which preparatory checks or Mode H\n'
     'approvals have run since 14 November 2026, in the last paragraph, or tell the new chat in your first message.',
     '**Before you paste it:** fill in the last paragraph. "See exchange/CONTINUITY_NOW.md" is usually enough, as that page is kept\n'
     'current; add anything that happened after its last update.'),
    ('h1', '- the handover **H-1 v2** (`doc/HANDOVER/Claude_Primary_Handover_H1_v2.md`), one complete file: read all of it, including',
     '- the handover **H-1 v3** (`doc/HANDOVER/Claude_Primary_Handover_H1_v3.md`), one complete file: read all of it, including'),
    ('cont', '- its tools in `exchange/CLAUDE_WEB_TOOLS/`, and the Mode H readiness files in `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/`.\n',
     '- its tools in `exchange/CLAUDE_WEB_TOOLS/`, and the Mode H readiness files in `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/`;\n'
     '- the one-page recovery index `exchange/CONTINUITY_NOW.md`: read it first; it says what is waiting now.\n'),
    ('reviewer',
     '- **The ChatGPT reviewer chat** (handover H-2 v2, one full document; before its installation H-2 v1r9 with its v1r10 delta): the independent reviewer of your designs, code and\n'
     '  documents. It took over on 6 November 2026.',
     '- **The ChatGPT reviewer chat** (handover H-2 v2 r1, one full document): the independent reviewer of your designs, code and\n'
     '  documents. It took over on 14 November 2026 (12 of 12 on Claude\'s blind questions).'),
    ('read', 'Read H-1 v2 in full. Then: the newest register\'s new sections (`doc/RATIFICATION_REGISTER_v0_29.md` or later,',
     'Read H-1 v3 in full. Then: the newest register\'s new sections (`doc/RATIFICATION_REGISTER_v0_30.md` or later,'),
    ('reviews', 'with its reviews EX_167 and EX_168; H-2', 'with its reviews EX_167, EX_168 and EX_177; H-2'),
    ('stood', '**Where things stood on 14 November 2026.**', '**Where things stood on 15 November 2026.**'),
    ('ready',
     '- **Ready but not authorised:** the readiness sheet (reviewed, PASS) with decisions D1 to D7 for the owner, the preparatory\n'
     '  checks (the Windows POC rerun, the updater\'s offline self-test, a read-only check of the official results page, backups and\n'
     '  tree checks) and the four approvals per game. No holdout is opened; the updater has never run live.',
     '- **Decided and run on 14 November 2026:** the owner\'s dependency change (TASK_T024 PASS; a scoped W-23 acceptance, never\n'
     '  "W-23 PASS"); D1 to D7 as recommended (Oz Lotto first); the working approach P0-P6 (H-1 section 1.7); the POC rerun and the\n'
     '  updater\'s offline self-test, both PASS.\n'
     '- **Ready but not authorised:** on one day, each on its own go: the read-only check of the official results page (it must run\n'
     '  on the day of the first Approval 1), backups, tree checks, then Oz Lotto\'s Approval 1; then the four approvals per game. No\n'
     '  holdout is opened; the updater has never run live.'),
    ('after', 'then WF-1C and the method waves.',
     'then WF-1C and the methods still to do (OUTLANDISH_01\'s\n  family probably first, through the normal route).'),
    ('checkpoint',
     '- **Checkpoint often:** commit tools and a checkpoint note before every review message, so nothing lives only in the chat. When\n'
     '  the chat grows long, say so and offer to write the next handover first.',
     '- Show your reasoning: why, the alternatives, the uncertainties; at each substantial milestone a short, independent "how the\n'
     '  process went" note (H-1 section 1.7, P6).\n'
     '- **Checkpoint often:** keep `exchange/CONTINUITY_NOW.md` current after every milestone and commit tools before every review\n'
     '  message, so nothing lives only in the chat. At every stage judge whether to refresh the handovers; when the chat grows long,\n'
     '  say so and offer to write the next handover first.'),
    ('since', 'Since 14 November 2026: <what the owner has decided or run since, or "nothing">.',
     'Since 15 November 2026: <"see exchange/CONTINUITY_NOW.md", plus anything newer>.'),
]
b = apply(b, BLURB)
b.encode('ascii')
assert '\r' not in b and b.endswith('\n')

os.makedirs(outdir, exist_ok=True)
for name, text in (('Claude_Primary_Handover_H1_v3.md', s), ('Claude_Primary_Handover_H1_v3_introductory_blurb.md', b)):
    p = os.path.join(outdir, name)
    open(p, 'wb').write(text.encode('ascii'))
    print(f'{name}: {len(text.encode())} bytes, {text.count(chr(10))} lines, SHA-256 {hashlib.sha256(text.encode()).hexdigest()}')
print(f'{len(EDITS)} counted edits + 4 header lines + 3 part replacements (H-1); {len(BLURB)} counted edits (blurb); section 2A unchanged')
