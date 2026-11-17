"""Build H-1 v4 and its blurb (the ratification candidate; first written as a DRAFT on 16 November 2026).
Usage: python3 -I make_h1_v4.py REPO_ROOT OUT_DIR

Reads doc/HANDOVER/Claude_Primary_Handover_H1_v3.md and its blurb from REPO_ROOT (asserted by SHA-256), applies counted
edits (each old text must occur exactly once) and whole-part replacements from the fragments beside this script, asserts
that section 2A is unchanged byte for byte, and writes the two drafts to OUT_DIR. Reads nothing else; writes nothing else.
"""
import hashlib, os, sys
assert len(sys.argv) == 3, 'usage: make_h1_v4.py REPO_ROOT OUT_DIR'
REPO, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = 'ddefe7006aa17cfd0a9a8996bd7122aed537d8d66accee92b2e5d737aefbaa54'
V3B = 'd1df63bf18bc7becc96212ac0d76d519a2a5c4d6b367251116b294382573dd4d'

def rd(path, sha):
    b = open(os.path.join(REPO, path), 'rb').read()
    assert hashlib.sha256(b).hexdigest() == sha, f'{path}: not the ratified bytes'
    t = b.decode('utf-8'); assert '\r' not in t
    return t
def frag(name):
    t = open(os.path.join(HERE, name), encoding='utf-8', newline='').read(); assert '\r' not in t
    return t
def one(s, old, new, label):
    n = s.count(old); assert n == 1, f'{label}: expected one occurrence, found {n}'
    return s.replace(old, new)
def line_starting(s, start, label):
    i = s.index(start); assert s.count(start) == 1, label
    return s[i:s.index('\n', i) + 1]
def part(s, start, end, new, label):
    assert s.count(start) == 1 and s.count(end) == 1, label
    a, b = s.index(start), s.index(end); assert a < b, label
    return s[:a] + new + s[b:]
def section(s, start, end):
    return s[s.index(start):s.index(end)]

s = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v3.md', V3)
S2A = section(s, '### 2A. ', '## 3. Project in one paragraph')

s = one(s, '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v3\n',
        '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v4\n', 'title')
s = one(s, line_starting(s, '**Version:** v3, 15 November 2026', 'version'),
        '**Version:** v4, 17 November 2026 (Adelaide, UTC+10:30). A **full edition** built from H-1 v3\'s ratified bytes by counted edits and whole-part replacements (`exchange/CLAUDE_WEB_TOOLS/h1v4/make_h1_v4.py`), as the owner prefers. It brings the handover to the state after Mode H: both games sealed and read, D5 done, the approach the owner agreed on 16 November 2026, and the MHUP-B design supplement ratified (RAT-33). **Section 0B is new and prevails over older statements below it**; Appendix B lists what changed.\n', 'version line')
s = one(s, line_starting(s, '**Status:** OWNER-RATIFIED 15 November 2026', 'status'),
        '**Status:** CANDIDATE for the owner\'s ratification with register v0.31 (RAT-34), after the reviewer\'s documentary review (EX_214). Until then the installed handover is H-1 v3 (RAT-32), read together with `exchange/CONTINUITY_NOW.md`. When ratified it replaces H-1 v3, which stays in `doc/HANDOVER/` as history.\n', 'status line')
s = one(s, line_starting(s, '**Baseline described:**', 'baseline'),
        '**Baseline described:** `main` on 17 November 2026: the code as installed by MHUP-A (package commit `2860e86`, release commit `effc179`, 13 November 2026) with the test-only fix `87c4219` and the owner\'s dependency change `cc0ab73`; no file under `src/`, no root `.bat` and no `requirements.txt` has changed since. The data: both masters at version 2 and the sealed Mode H records (`c7622fa`).\n', 'baseline line')
s = one(s, line_starting(s, '**Replaces, for future roles:**', 'replaces'),
        '**Replaces, for future roles:** H-1 v3 and its blurb (RAT-32), kept as history; and, as before, H-1 v2, v1r8, its deltas and the older editions listed in v1r3\'s header. D-1 and ADD-2 are inputs, not authority.\n', 'replaces line')
s = one(s, 'Never display, paste or compute with an outcome for Powerball >= 1577 or Oz Lotto >= 1694.\n\n---\n\n## 0. First actions',
        'The older rule against displaying or computing with an outcome for Powerball >= 1577 or Oz Lotto >= 1694 is replaced, from RAT-34, by the approach the owner agreed on 16 November 2026 and the reviewer agreed with conditions (section 0B, item 4).\n\n---\n\n## 0. First actions', 'holdout discipline')
s = one(s, 'Claude_Primary_Handover_H1_v3_introductory_blurb.md', 'Claude_Primary_Handover_H1_v4_introductory_blurb.md', 'blurb name')
s = one(s, '## 1. Roles and workflow (agreed position v0.1r1, ratified)\n', frag('frag_0B.md') + '## 1. Roles and workflow (agreed position v0.1r1, ratified)\n', 'insert 0B')
s = one(s, '- **Code packages** (anything touching',
        '- **Since 16 and 17 November 2026 (section 0B, item 4; in force from RAT-34):** a document that has been reviewed and ratified is committed by Claude directly (named paths, after `git fetch` and a fast-forward, never over the owner\'s push) and checked from GitHub; the owner only pulls. The install instructions below remain for code packages. The reviewer commits its own EX replies to `exchange/` and its H-2 files to `doc/HANDOVER/`; fetch before reading or numbering anything, and never edit its files.\n- **Code packages** (anything touching', '1.6 first bullet')
s = one(s, line_starting(s, '- **Q7 DECIDED (owner, 13 November 2026, 22:08):**', 'q7'),
        '- **Q7 (owner, 13 November 2026) is REPLACED**, from RAT-34, by the approach the owner agreed on 16 November 2026 (`exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md`; the reviewer agreed with conditions, EX_206): all draws are treated the same and the AI chats may read draw values, the masters and the results. Still binding: no lottery website and no results search by any AI; results count only from the reviewed programs and their logged runs, and anything an AI computes in a chat is labelled suggestive; method-facing N-1 isolation, forecast identities and append-only records; already-known draws give development evidence only; the sealed Mode H records are never altered or rescored; the local runner\'s rules 4 and 5 stay binding until MHUP-B\'s rulebook edition (EX_206 Q4).\n', 'q7 line')
s = one(s, '- **The Mode H freeze (design 4.1, MHUP-B04; owner, 13 November 2026):**',
        '- **The Mode H freeze (design 4.1, MHUP-B04; owner, 13 November 2026; ENDED 16 November 2026, when both games were sealed, EX_199; kept as history):**', '5.4 freeze')
row = line_starting(s, "| `cc0ab73` | The owner's dependency change", 'cc0ab73 row')
s = one(s, row, row + "| `5b4df41` | RAT-32 documentation install (not a package) | H-1 v3, its blurb and register v0.30, installed by the owner on 15 November 2026 (decision log entry 7) |\n| `c7622fa` | The Mode H results, D5 (an owner data commit, not a package) | Both masters and ledgers at version 2, the search log, the Mode H batch records and markers, and the six report files, committed by the owner on 16 November 2026 (decision log entry 48) |\n", '7.1 rows')
s = one(s, line_starting(s, '- Masters: Powerball `ce0ae7e77e09', 'masters'),
        '- Masters: **version 2 since Mode H** (committed at `c7622fa`): Powerball `e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0` (last row 1591); Oz Lotto `63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e` (last row 1708). Version 1 (Powerball `ce0ae7e77e09...`, last row 1576; Oz Lotto `4a6cecc27fb6...`, last row 1693) is history. Each game\'s first update ran on its Approval 2 (15 and 16 November 2026), so the updater has run live once per game.\n', 'masters line')
s = one(s, line_starting(s, "- **Mode H's records, when they exist** (none at this edition):", 'modeh records'),
        "- **Mode H's records (both games; committed by the owner at `9eb5e33`, `c302871` and `c7622fa`):** the study manifest `results/real/holdout/<GAME>/MODE_H_STUDY_MANIFEST_V1.json`, the opening record `source_data/HOLDOUT_OPENED_<GAME>.json`, the batch-id record `results/real/holdout/<GAME>/MODE_H_BATCH_ID.json`, each batch folder under `results/real/holdout/wf_batches/<GAME>/` (plan, segment record, `BATCH_COMPLETE`, `SCORING_STARTED`, `SCORE_COMPLETE`, `MODE_H_SEALED`) and the reports `results/method_rankings/<GAME>/mode_h_*`. The run folders, attempts ledgers and score ledgers are git-ignored and stay on the owner's PC and in his backups. Sealed: never altered, rerun or rescored.\n", 'modeh records line')
row = line_starting(s, '- **Dress-rehearse an irreversible run', '8.8 last')
s = one(s, row, row + frag('frag_8_8_add.md'), '8.8 lessons')
s = one(s, 'At this edition the newest is EX_190 (Claude: this edition and register v0.30 for review); check before taking the next.',
        'At this edition the newest is EX_214 (Claude: this edition and register v0.31 for review). The reviewer now commits its own replies to `exchange/`, so fetch before taking the next number; a reply the owner pastes without a number is filed under a letter suffix (EX_203A).', '12.1 EX line')
s = one(s, line_starting(s, '6. **Models (MC-1):**', 'models'),
        '6. **Models (MC-1):** take over on Opus; suggest Fable (High) for MHUP-B\'s code plan and its core code (the evidence score, the live path), a BLOCKER-level finding, an unexplained STOP, or a cold read before a review round; say when the Fable work is done.\n', '12.9 models')
s = one(s, '| Register v0.29 (RAT-31; installed at `5a8527b`) |', frag('frag_appA_reg.md') + '| Register v0.29 (RAT-31; installed at `5a8527b`) |', 'app A register row')
s = one(s, '| H-1 v2 (predecessor;', frag('frag_appA_add.md') + '| H-1 v2 (', 'app A H-1 v3 row')
s = one(s, '| The history clean-up crosswalk (6 November 2026) |', frag('frag_appA_new.md') + '| The history clean-up crosswalk (6 November 2026) |', 'app A new rows')
s = one(s, '### 5.1 Data and holdout\n\n',
        '### 5.1 Data and holdout\n\n**Read section 0B first.** Both holdouts are now opened, scored and sealed, and their draws are ordinary history. The bullets below are kept as the record of how the data was protected up to the seals. Where they forbid the AI chats to see draw values (the quarantine\'s display rule; Q7) they are replaced, from RAT-34, by the approach the owner agreed on 16 November 2026. Still in force: Lotterywest-GOV as the only source through the owner\'s updater, and no lottery-results searches by any AI. Out of date: "the updater has never run live" (it ran each game\'s first update on 15 and 16 November 2026; both masters are at version 2, section 7.5).\n\n', '5.1 lead')
s = part(s, '1. **Done since v2 (14 November 2026, afternoon and evening):**', '5. **WF-1C** (WORKERS-1; roadmap item 10d)', frag('frag_10_head.md'), 'section 10 items 1-4')
s = one(s, '## 11. Gates that stay closed\n\n',
        '## 11. Gates that stay closed\n\n**At this edition (section 0B):** Mode H\'s gates are behind us; the sealed studies are never reopened or rescored. Ratified designs, including the MHUP-B supplement (RAT-33), authorise no code or run. Still closed until the owner\'s own go, each separately: every code package and install; every real-data run, results update, catch-up, weekly session, re-forecast and score; the registration of OV-1; every walk-forward batch and report run (the Powerball 1145-1285 report included); Windows lifecycle and destructive tests; any dependency change. The paragraph below is v3\'s and describes the gates as they stood before Mode H.\n\n', '11 lead')
s = part(s, '### 12.8 Open items at this edition (15 November 2026)', '- **The reminders** (`exchange/OWNER_REMINDERS.md`', frag('frag_12_8.md'), '12.8 head')
s = part(s, '## Appendix B. Changes in v3', '*End of H-1.*', frag('frag_appB.md'), 'appendix B')

assert section(s, '### 2A. ', '## 3. Project in one paragraph') == S2A, 'section 2A changed'
assert '\r' not in s and s.endswith('\n') and not s.endswith('\n\n')
assert s.count('## 0B. ') == 1 and s.count('## Appendix B. Changes in v4\n') == 1

b = rd('doc/HANDOVER/Claude_Primary_Handover_H1_v3_introductory_blurb.md', V3B)
b = one(b, '- goes with H-1 v3\n', '- goes with H-1 v4\n', 'blurb title')
b = one(b, line_starting(b, 'Written by Claude on 15 November 2026 with H-1 v3', 'blurb written'),
        'Written by Claude on 17 November 2026 with H-1 v4, the full edition that replaces H-1 v3 (its status is in the register).\n', 'blurb written line')
b = one(b, '- the handover **H-1 v3** (`doc/HANDOVER/Claude_Primary_Handover_H1_v3.md`), one complete file: read all of it, including\n',
        '- the handover **H-1 v4** (`doc/HANDOVER/Claude_Primary_Handover_H1_v4.md`), one complete file: **read its section 0B first**,\n  then all of it, including\n', 'blurb handover name')
b = one(b, '   Read H-1 v3 in full. Then: the newest register\'s new sections (`doc/RATIFICATION_REGISTER_v0_30.md` or later, just before\n',
        '   Read H-1 v4 in full, section 0B first. Then: the newest register\'s new sections\n   (`doc/RATIFICATION_REGISTER_v0_31.md` or later, just before\n', 'blurb read')
b = one(b, 'the readiness\n   sheet `exchange/CLAUDE_WEB_TOOLS/modeh_readiness/APPROVAL_1_READINESS_SHEET_DRAFT.md` with its reviews EX_167, EX_168 and EX_177; H-2\n   v2 (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md`);',
        'the MHUP-B\n   design supplement `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md` with its reviews EX_207 to EX_213; H-2 v2\n   (`doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md`) and the reviewer\'s own H-2 v3 candidate beside it;', 'blurb reading list')
i0 = b.index('**Note for the owner: which model, when**'); j0 = b.index('**Before you paste it:**')
b = b[:i0] + ('**Note for the owner: which model, when** (Claude\'s recommendation, 17 November 2026):\n'
    '1. **Start the new chat on Opus 5.5.** The takeover is reading and explaining, which Opus does well and cheaply.\n'
    '2. **Stay on Opus** for documents, task files, packaging and reading run outputs.\n'
    '3. **Switch to Fable (High)** for MHUP-B\'s code plan and the core of its code (the evidence score, the live path), any\n'
    '   BLOCKER-level review finding, any unexplained STOP, or a cold read before a review round. The new chat should say\n'
    '   "Suggest switching to Fable (High) for this" at those points and wait for your "go"; when the Fable work is done it should\n'
    '   say so.\n\n') + b[j0:]
b = one(b, 'Check the hashes H-1 quotes with a tool. Never open\n   anything under `source_data/`, `results/` or `transitory_data/`.',
        'Check the hashes H-1 quotes with a tool. Since RAT-34\n   you may read `source_data/` and `results/` (H-1 section 0B, item 4); never write there.', 'blurb open rule')
b = one(b, '**Where things stood on 15 November 2026.**\n',
        '**Where things stood on 17 November 2026 (this overrides the older bullets below; H-1 section 0B has the detail).**\n'
        '- **Mode H is complete:** Oz Lotto sealed 15 November, Powerball 16 November; both reports read independently by the reviewer\n'
        '  and Claude, and the readings agree: no statistically significant predictive advantage was demonstrated under the predeclared\n'
        '  Mode H tests (EX_200 to EX_205). The freeze has ended. The owner committed the results at `c7622fa` (D5).\n'
        '- **The approach the owner agreed on 16 November 2026**, reviewed (EX_206) and in force from RAT-34\n'
        '  (`exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md`): all draws are treated the same and the AI chats may read draw values\n'
        '  and results; no lottery websites or results searches by the AIs; results count only from the reviewed programs (chat\n'
        '  calculations are "suggestive"); nothing runs without his go; Claude commits reviewed and ratified documents directly, code\n'
        '  still goes by reviewed package and his Windows install, Claude never writes the data folders, nothing is deleted. The\n'
        '  reviewer commits its own replies to `exchange/`: fetch before reading or numbering anything.\n'
        '- **The MHUP-B design supplement is ratified** (RAT-33; `doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md`):\n'
        '  eight tested layers, a league table of every method with `current` and archive folders, re-forecasting of every draw as\n'
        '  development evidence, and one exact evidence score per game as the only confirmatory forward test. Design only.\n'
        '- **Next:** the MHUP-B code plan (Fable, High), reviewed before any code.\n'
        '\n**Where things stood on 15 November 2026 (history).**\n', 'blurb where things stood')
b = one(b, '- Never display, paste or compute with an outcome for Powerball draw 1577 or later, or Oz Lotto draw 1694 or later. Never open\n  `source_data`, `results` or `transitory_data`.\n',
        '- (Replaced from RAT-34 by the owner\'s agreed approach of 16 November 2026: the AI chats may see draw values and read\n  `source_data` and `results`. They never write there, and they never fetch results themselves.)\n', 'blurb display rule')
b = one(b, 'Since 15 November 2026: <"see exchange/CONTINUITY_NOW.md", plus anything newer>.', 'Since 17 November 2026: <"see exchange/CONTINUITY_NOW.md", plus anything newer>.', 'blurb since')
assert '\r' not in b and b.endswith('\n')

os.makedirs(OUT, exist_ok=True)
for name, text in (('Claude_Primary_Handover_H1_v4.md', s), ('Claude_Primary_Handover_H1_v4_introductory_blurb.md', b)):
    data = text.encode('utf-8'); open(os.path.join(OUT, name), 'wb').write(data)
    print(name, len(data), hashlib.sha256(data).hexdigest())
