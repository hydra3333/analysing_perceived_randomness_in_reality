#!/usr/bin/env python3
"""Builds the H-1 v8 candidate and its introductory blurb.

Purpose: fill H1_v8_template.md (beside this file) and write
  out/Claude_Primary_Handover_H1_v8.md
  out/Claude_Primary_Handover_H1_v8_introductory_blurb.md
Usage (from anywhere):  python3 -I make_h1_v8.py <repository root>
Every input is read from Git at HEAD ("git show HEAD:<path>"), so the working tree's line endings do not matter.
It refuses (an assertion) on any failure: a missing file, a carried line not found exactly once in H-1 v7r1,
a non-ASCII byte, a CR, or an unfilled placeholder.
"""
import hashlib, os, re, subprocess, sys

# ---- constants -------------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
V7R1 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md'            # the installed handover the carried text comes from
OLD_BLURB = 'exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21_blurb.md'      # the blurb of 21 November 2026 (the owner's rules)
CARRY_FIRST = '## 1. Roles and workflow (agreed position v0.1r1, ratified)'   # first line of the carried region
CARRY_AFTER = '## 3. Project in one paragraph'                       # the carried region ends before this heading
# Files listed in Appendix A, in this order.
ID_PATHS = [
 'doc/Predictive_Randomness_System_Specification_v0_6.md',
 'doc/Predictive_Randomness_Deployment_Design_v0_12.md',
 'doc/CODING_PRACTICES_v0_1.md',
 'exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_6.md',
 'exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_12.md',
 'exchange/CLAUDE_WEB_TOOLS/simplify/DRAFT_CONTRADICTIONS_FOR_REVIEWER_v0_1.md',
 'exchange/EX_266_Claude.md', 'exchange/EX_267_ChatGPT.md', 'exchange/EX_268_Claude.md',
 'exchange/EX_269_ChatGPT.md', 'exchange/EX_270_Claude.md', 'exchange/EX_271_ChatGPT.md',
 'exchange/ChatGPT_to_Claude_QA_and_EX266_Decisions_2026_11_21.md',
 'exchange/ChatGPT_to_Claude_QA_Scientific_Equivalence_Variant_Status_Q1_Q4_2026_11_21.md',
 'exchange/ChatGPT_to_Claude_R6_F01_Slipstream_Correction_OV1_Reclosed_2026_11_22.md',
 'exchange/DECISIONS/AGREED_APPROACH_2026_11_16.md',
 'exchange/DECISIONS/WORKING_PRINCIPLE_2026_11_18_MAIN_GAME_PRIORITY.md',
 'exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21.md',
 'exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21_blurb.md',
 'exchange/README.md',
 'exchange/CLAUDE_WEB_TOOLS/check_task_commands.py',
 'exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/src/evaluation/ov1_numeric.py',
 'exchange/CLAUDE_WEB_TOOLS/mhupb/slice2/slice2_new/tests/test_mhupb_ov1_numeric.py',
 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md',
 'doc/HANDOVER/Claude_Primary_Handover_H1_v7r1.md',
 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r4_RATIFICATION_CANDIDATE_20261118.md',
 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v3r10_CONTINUITY_CANDIDATE_20261121.md',
 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122.md',
 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v4_RAT40_FULL_CANDIDATE_20261122_introductory_blurb.md',
 'doc/HANDOVER/HANDOVER_CHANGED_AI_Roles_Agreed_v0_1r1_RATIFIED.md',
 'doc/HANDOVER/AI_Roles_Transition_Record_H3_v1r1.md',
 'review/REVIEWER_FIX-and-PROCEED_RECHECK_PROCEDURE_v1.md',
 'doc/RATIFICATION_REGISTER_v0_31.md',
 'source_data/POWERBALL_results_master.csv',
 'source_data/OZLOTTO_results_master.csv',
]

def git_bytes(repo, path):
    """Return the bytes of <path> at HEAD. Example: git_bytes(repo, 'exchange/README.md') -> b'# exchange/ ...'."""
    return subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + path], check=True, capture_output=True).stdout

def sha(data):
    """SHA-256 of bytes as 64 lower-case hex characters."""
    return hashlib.sha256(data).hexdigest()

def main():
    assert len(sys.argv) == 2, 'usage: make_h1_v8.py <repository root>'
    repo = os.path.abspath(sys.argv[1])
    template = open(os.path.join(HERE, 'H1_v8_template.md'), encoding='ascii', newline='').read()
    v7 = git_bytes(repo, V7R1).decode('ascii')
    v7_lines = v7.split('\n')

    # 1. The carried region: v7r1's sections 1, 2 and 2A, byte for byte.
    first = [i for i, l in enumerate(v7_lines) if l == CARRY_FIRST]
    after = [i for i, l in enumerate(v7_lines) if l.startswith(CARRY_AFTER)]
    assert len(first) == 1 and len(after) == 1, (first, after)
    region = v7_lines[first[0]:after[0]]
    while region and region[-1].strip() in ('', '---'):      # drop the rule and blank lines before section 3
        region.pop()
    carried = '\n'.join(region)
    assert carried.count('### 2A. The owner') == 1 and '\n## 2. How the owner wants work presented' in carried
    assert v7.count(carried) == 1                            # it is one unbroken piece of v7r1

    # 2. Single carried lines: {{B:<start of line>}} becomes the one v7r1 line that starts with that text.
    def carried_line(m):
        start = m.group(1)
        hits = [l for l in v7_lines if l.startswith(start)]
        assert len(hits) == 1, ('carried line', len(hits), start)
        return hits[0]
    out = re.sub(r'\{\{B:(.+?)\}\}', carried_line, template)

    # 3. The owner's hard rules, from the blurb of 21 November 2026.
    blurb = git_bytes(repo, OLD_BLURB).decode('ascii').replace('\r\n', '\n')   # that file is stored CRLF; work in LF
    a = blurb.index('- The one production results source'); b = blurb.index('- A PASS or a ratified design authorises no install or run.')
    hard = blurb[a:b] + '- A PASS or a ratified design authorises no install or run.'
    assert hard.count('\n- ') == 6
    out = out.replace('{{HARD_RULES}}', hard)

    # 4. Hashes.
    out = re.sub(r'\{\{SHA:(.+?)\}\}', lambda m: sha(git_bytes(repo, m.group(1))), out)
    rows = ['| File | SHA-256 |', '|---|---|'] + ['| `%s` | `%s` |' % (p, sha(git_bytes(repo, p))) for p in ID_PATHS]
    out = out.replace('{{IDTABLE}}', '\n'.join(rows))
    out = out.replace('{{CARRIED_1_2}}', carried)
    out = out.replace('{{CARRIED_SHA}}', sha(carried.encode('ascii')))
    out = out.replace('{{CARRIED_BYTES}}', str(len(carried.encode('ascii'))))
    out = out.replace('{{CARRIED_LINES}}', str(len(region)))

    # 5. The blurb: the blurb of 21 November 2026 with counted changes.
    def rep(s, old, new):
        assert s.count(old) == 1, ('blurb', s.count(old), old[:60]); return s.replace(old, new)
    nb = blurb
    nb = rep(nb, '# Blurb for a new Claude chat, 21 November 2026 (paste everything below the line)',
                 '# Introductory blurb for H-1 v8: for a new Claude chat (paste everything below the line)')
    nb = rep(nb, 'The previous Claude chat became too long. It left you a takeover note. The project is in the middle of a redesign\n'
                 'from the root, and nothing of the new design is ratified, coded or installed.',
                 'The previous Claude chat left you a handover, H-1 v8. The project was redesigned from the root in November 2026.\n'
                 'The new design was ratified on 22 November 2026 (RAT-40). None of it is coded or installed unless the\n'
                 'repository says so: the code in src/ is the old system.')
    nb = rep(nb, 'exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21.md and follow its reading order (section 1). Verify what you read against the\n'
                 'repository; do not take summaries on trust.',
                 'doc/HANDOVER/Claude_Primary_Handover_H1_v8.md and follow its section 0 (its reading order and the staged takeover).\n'
                 'Verify what you read against the repository; do not take summaries on trust.')
    nb = rep(nb, 'authorised, what the next deliverable is, and anything you found unclear or inconsistent. Implement and design\n'
                 'nothing yet. The ChatGPT reviewer will then ask you some blind questions, which I will relay, and I will decide\n'
                 'whether to accept your takeover (procedure HO-2).',
                 'authorised, what the next deliverable is, and anything you found unclear or inconsistent. Implement, design,\n'
                 'build and commit nothing yet. The ChatGPT reviewer will then ask you some blind questions, which I will relay,\n'
                 'and I will decide whether to accept your takeover (procedure HO-2).')
    nb = rep(nb, 'HARD RULES, binding now (the installed handover H-1 v7r1 has them in full):',
                 'HARD RULES, binding now (H-1 v8 has them in full):')
    nb = rep(nb, '  ratified. Code and tests never go into src/ or tests/ from you. Never edit the reviewer\'s files.',
                 '  ratified. Code and tests never go into src/ or tests/ from you. You never write under transitory_data/ or GAIS/.\n'
                 '  Never edit the reviewer\'s files.')
    nb = rep(nb, 'chat. Do not over-engineer: the science, N-1, scoring and recoverability are the main game. Discuss my queries with\n'
                 'me first; issue or revise an EX message only when I ask.',
                 'chat. Do not over-engineer: the science, N-1, scoring and recoverability are the main game. Discuss my queries with\n'
                 'me first; issue or revise an EX message only when I ask. Use the project\'s own words (restore from backup,\n'
                 'catch-up, walk-forward, historical walk-forward rerun), and explain any finding code in plain words with an example.')

    # 6. Checks, then write.
    for name, text in (('handover', out), ('blurb', nb)):
        assert '{{' not in text and '}}' not in text, (name, 'unfilled placeholder')
        data = text.encode('ascii')                          # refuses any non-ASCII character
        assert b'\r' not in data and data.endswith(b'\n') and not data.endswith(b'\n\n'), (name, 'line endings')
    assert out.count(carried) == 1
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    for fn, text in (('Claude_Primary_Handover_H1_v8.md', out), ('Claude_Primary_Handover_H1_v8_introductory_blurb.md', nb)):
        with open(os.path.join(HERE, 'out', fn), 'w', encoding='ascii', newline='\n') as f:
            f.write(text)
        print('%s  %d bytes  %d lines  %s' % (sha(text.encode('ascii')), len(text), text.count('\n'), fn))
    print('carried region: %d lines, %d bytes, %s' % (len(region), len(carried), sha(carried.encode('ascii'))))

if __name__ == '__main__':
    main()
