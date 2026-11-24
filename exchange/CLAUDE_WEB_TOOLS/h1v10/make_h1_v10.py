"""Build the H-1 v10 CANDIDATE and its blurb from the installed H-1 v9, by counted replacements.

What this file is for
    H-1 is the handover from which a new Claude chat takes over as primary designer and coder. v10 brings v9 up to
    date after build step 2 was reviewed, rehearsed, installed and run. This script reads H-1 v9 and its blurb from
    Git at HEAD (each checked by its SHA-256), applies the short replacements and the whole-section replacements of
    h1_v10_texts.py (each old text or marker must be found exactly once), rebuilds Appendix A's table with every
    hash computed from Git at HEAD, checks that sections 1, 2 and 2A are carried byte for byte, and writes the
    candidate, its blurb and the two exact diffs into out/ beside itself. It refuses on any failure.

Which part of the specification it carries out
    None; H-1 is the Claude chat's handover (agreed roles position v0.1r1, section 9 item 4).

Which of the project's own modules it uses
    h1_v10_texts.py, beside it (the new words).

What uses it
    Claude, in the cloud workspace. Usage:  python make_h1_v10.py <repository clone>
"""
import difflib
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import h1_v10_texts as texts

V9 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v9.md'
V9_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v9_introductory_blurb.md'
# The installed H-1 v9 and its blurb (RAT-43), as `sha256sum` printed them on 24 November 2026.
V9_SHA256 = '8c28f82c0662be75d683bd37b13d6b0596b3b6424584d5674f09f1d965b182b1'
V9_BLURB_SHA256 = '1cbe95bedb9741a610760b25de80e24eb3c798d9814287a4d28d8256c551dbe5'
OUT_NAME = 'Claude_Primary_Handover_H1_v10.md'
OUT_BLURB_NAME = 'Claude_Primary_Handover_H1_v10_introductory_blurb.md'
# The carried region: sections 1, 2 and 2A (still H-1 v7r1's bytes).
CARRIED_FROM, CARRIED_TO = '## 1. Roles and workflow', '### 2B.'
# (first marker, end marker or None for the end of the file, the new text): the passage from the first marker up
# to, not including, the end marker is replaced.
SECTIONS = (
    ('# H-1 - Claude primary designer and coder handover', '\n---\n\n## 0. First actions', texts.HEADER),
    ('8. **What is authorised now:** documents and records.', '## 0C. Sections 1, 2 and 2A', texts.STATE_ITEMS),
    ('- **Everything else** under `src/` and `tests/`', '- The three safety switches are False', texts.INSTALLED_CODE),
    ('### 7.5 Not tested by anyone', '## 8. How to work as primary designer and coder', texts.NOT_TESTED),
    ('### 8.6 The Claude Code local runner', '### 8.7 Rebuilding', texts.RUNNER),
    ('## 10. Next work, in order', '**Genuinely OPEN**', texts.NEXT_WORK),
    ('### 12.4 Claude Code task files', '### 12.5 Traps in the cloud workspace', texts.TASK_FILES),
    ('### 12.8 Open items at this edition', '### 12.9 The first hour in a new chat', texts.OPEN_ITEMS),
    ('## Appendix B. What changed from H-1 v8', None, texts.APPENDIX_B),
)
# (the marker a new passage goes in front of, the new passage).
INSERTIONS = (
    ('\n### 7.3 Staged work that is not installed', texts.DEV_RESULTS),
    ('**From build step 1 and the tidy-up (22 and 23 November 2026):**', texts.LESSONS),
)
# Appendix A: a v9 row's path that is replaced by another, and the rows added after v9's.
ROW_PATH_CHANGES = {
    'doc/HANDOVER/Claude_Primary_Handover_H1_v8.md': V9,
    'doc/HANDOVER/Claude_Primary_Handover_H1_v8_introductory_blurb.md': V9_BLURB,
}
NEW_ROWS = (
    'exchange/EX_283_ChatGPT.md', 'exchange/EX_285_ChatGPT.md', 'exchange/EX_286_ChatGPT.md',
    'exchange/EX_287_ChatGPT.md', 'exchange/EX_289_ChatGPT.md', 'exchange/EX_290_ChatGPT.md',
    'exchange/EX_291_ChatGPT.md', 'exchange/EX_292_ChatGPT.md', 'exchange/EX_293_Claude/EX_293_Claude.md',
    'exchange/EX_294_ChatGPT.md',
    'exchange/CLAUDE_WEB_TOOLS/step2/STEP2_PACKAGE_NOTE_v0_3.md',
    'exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/STEP2_Research_Engine_v1r3.zip',
    'exchange/CLAUDE_WEB_TOOLS/step2/package_v1r3/INSTALL_AND_RUN_SHEET.md',
    'exchange/CLAUDE_WEB_TOOLS/step2/build_step2_pkg.py',
    'exchange/CLAUDE_WEB_TOOLS/step2/compare_fill_with_old_records.py',
    'exchange/CLAUDE_WEB_TOOLS/step2/check_compare_tool.py',
    '.claude/settings.json',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T025.md', 'CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T026.md',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/inbox/TASK_T027.md', 'CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T025.md',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T026.md', 'CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T027.md',
    'src/research/ov1_numeric.py', 'src/research_command.py', 'Run_Research.bat', 'Withdraw_Variant.bat',
    'deploy/INFRA_MANIFEST.ini', 'ENVIRONMENT.example.ini',
)
# The blurb: (old text, new text), each old text found the stated number of times in v9's blurb.
BLURB_CHANGES = (
    ('H-1 v9', 'H-1 v10', 3),
    ('doc/HANDOVER/Claude_Primary_Handover_H1_v9.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v10.md', 1),
    ('The new design was ratified on 22 November 2026 (RAT-40). Build step 1 (the method files\' new layout) and the light\n'
     'tidy-up are installed and proved; the rest of the new system is not coded unless the repository says so, and the\n'
     'rest of the code in src/ is the old system.',
     'The new design was ratified on 22 November 2026 (RAT-40). Build step 1 (the method files\' new layout), the light\n'
     'tidy-up and build step 2 (the research engine, in DEV) are installed and proved. The trees QA and PROD, the\n'
     'installs, the backups and the laboratory tools are not coded unless the repository says so, and the old\n'
     'system\'s code is still in src/ beside the new engine.', 1),
)


def git_bytes(repository: Path, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD; it refuses if the path is not there."""
    return subprocess.run(['git', '-C', str(repository), 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha256_of(data: bytes) -> str:
    """The SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def replace_once(text: str, old: str, new: str, what: str) -> str:
    """Replace old by new in text; refuse unless old is found exactly once."""
    assert text.count(old) == 1, f'{what}: the old text is found {text.count(old)} times, not once'
    return text.replace(old, new)


def rebuild_identities(text: str, repository: Path) -> str:
    """Give Appendix A's table its rows again, every hash computed from Git at HEAD, with the new rows after them."""
    start, end = text.index('## Appendix A. Identities'), text.index('## Appendix B.')
    section, rows, seen = text[start:end], [], set()
    lines = section.split('\n')
    row_numbers = [n for n, line in enumerate(lines) if re.match(r'\| `[^`]+` \| `[0-9a-f]{64}` \|$', line)]
    assert row_numbers and row_numbers == list(range(row_numbers[0], row_numbers[-1] + 1)), 'the table is not one block'
    for n in row_numbers:
        path = re.match(r'\| `([^`]+)` \|', lines[n]).group(1)
        path = ROW_PATH_CHANGES.get(path, path)
        seen.add(path)
        rows.append(f'| `{path}` | `{sha256_of(git_bytes(repository, path))}` |')
    for path in NEW_ROWS:
        assert path not in seen, f'{path} is already a row of the table'
        rows.append(f'| `{path}` | `{sha256_of(git_bytes(repository, path))}` |')
    lines[row_numbers[0]:row_numbers[-1] + 1] = rows
    return text[:start] + '\n'.join(lines) + text[end:]


def main(repository: Path) -> int:
    """Build the candidate and its blurb, check them, write them with their diffs; return 0."""
    out = Path(__file__).resolve().parent / 'out'
    out.mkdir(exist_ok=True)
    old_bytes, old_blurb_bytes = git_bytes(repository, V9), git_bytes(repository, V9_BLURB)
    assert sha256_of(old_bytes) == V9_SHA256 and sha256_of(old_blurb_bytes) == V9_BLURB_SHA256, 'not the installed H-1 v9'
    old = old_bytes.decode('ascii')
    new = old
    for old_text, new_text, what in texts.SMALL:
        new = replace_once(new, old_text, new_text, what)
    for marker, passage in INSERTIONS:
        assert old.count(marker) == 1, f'the marker is found {old.count(marker)} times in v9: {marker!r}'
        new = replace_once(new, marker, passage + marker if marker.startswith('\n') else passage + marker, marker)
    for first, last, passage in SECTIONS:
        assert old.count(first) == 1 and (last is None or old.count(last) == 1), f'a marker is not found once in v9: {first!r}'
        begin = new.index(first)
        finish = len(new) if last is None else new.index(last)
        assert begin < finish, f'the markers are out of order: {first!r}'
        new = new[:begin] + passage + new[finish:]
    new = rebuild_identities(new, repository)
    carried = lambda text: text[text.index(CARRIED_FROM):text.index(CARRIED_TO)]
    assert carried(new) == carried(old), 'sections 1, 2 and 2A are not carried byte for byte'
    assert '@@' not in new and '\r' not in new and new.endswith('\n') and not new.endswith('\n\n')
    new.encode('ascii')
    blurb = old_blurb_bytes.decode('ascii')
    for old_text, new_text, count in BLURB_CHANGES:
        assert blurb.count(old_text) == count, f'the blurb holds {blurb.count(old_text)} of {old_text!r}, not {count}'
        blurb = blurb.replace(old_text, new_text)
    assert 'v9' not in blurb, 'the blurb still names v9'
    for name, before, after, label in ((OUT_NAME, old, new, 'H1_v9_TO_v10.diff'),
                                       (OUT_BLURB_NAME, old_blurb_bytes.decode('ascii'), blurb, 'H1_v9_TO_v10_blurb.diff')):
        (out / name).write_text(after, encoding='ascii', newline='\n')
        diff = ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                            'H-1 v9 (installed)', 'H-1 v10 (candidate)', n=0))
        (out / label).write_text(diff, encoding='ascii', newline='\n')
        print(f'{sha256_of(after.encode("ascii"))}  {len(after.splitlines())} lines  {name}')
    print(f'{len(texts.SMALL)} short replacements, {len(INSERTIONS)} insertions, {len(SECTIONS)} sections replaced, '
          f'Appendix A rebuilt; sections 1, 2 and 2A carried byte for byte')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
