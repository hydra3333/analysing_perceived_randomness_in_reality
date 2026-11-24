"""Finalise RAT-48: install H-1 v11 and its blurb in doc/HANDOVER/.

What this file is for
    The owner ratified the candidate H-1 v11r1 on 24 November 2026 (RAT-48; decision log entry 244), after the
    reviewer's PASS for continuity (EX_306) and its focused PASS of revision r1 (EX_307). This script reads the
    candidate and its blurb from Git at HEAD (each checked by its SHA-256), applies counted replacements (each
    old text must be found exactly once) to the status statements and to the statements the ratification itself
    makes out of date (the owner's standing instruction, entry 153), and writes the installed handover and blurb.
    H-1 v10 and its blurb stay where they are as history. The exact differences from the ratified candidates are
    written beside this file.

Which part of the project's rules it carries out
    H-1 section 8.5: "Finalising after ratification changes only the status line"; as at RAT-41, RAT-43 and
    RAT-45, with the owner's instruction on out-of-date statements.

Which of the project's own modules it uses
    None (the standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python finalise_rat48.py <repository clone>
"""
import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

CANDIDATE = 'exchange/CLAUDE_WEB_TOOLS/h1v11r1/out/Claude_Primary_Handover_H1_v11r1.md'
CANDIDATE_BLURB = 'exchange/CLAUDE_WEB_TOOLS/h1v11r1/out/Claude_Primary_Handover_H1_v11r1_introductory_blurb.md'
# The candidate and its blurb as the reviewer passed them (EX_307) and the owner ratified them (entry 244).
CANDIDATE_SHA256 = 'bb68f9b6ea7c8ad65a3c172698c0e1ceffd274a0a0a60663cb4aa527a42e13c9'
BLURB_SHA256 = '5d7e64fe13fba2bb094707d86616664aef58f7422f99fc75fd5a612c9f4c6663'
INSTALLED = 'doc/HANDOVER/Claude_Primary_Handover_H1_v11.md'
INSTALLED_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v11_introductory_blurb.md'
DIFF_NAME = 'H1_v11r1_CANDIDATE_TO_FINAL.diff'
BLURB_DIFF_NAME = 'H1_v11r1_CANDIDATE_TO_FINAL_blurb.diff'
# Sections 1, 2 and 2A are carried byte for byte: from the first heading to the second.
CARRIED_FROM, CARRIED_TO = '## 1. Roles and workflow', '### 2B.'

# (old text, new text, what it is)
CHANGES = (
    ('# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v11 CANDIDATE',
     '# H-1 - Claude primary designer and coder handover - Predictive Randomness project, v11',
     'the title'),
    ('**This edition: v11 CANDIDATE, revision r1, 24 November 2026, evening (Adelaide, UTC+10:30). H-1 v10 brought up\n'
     'to date the same day,**',
     '**This edition: v11, 24 November 2026, evening (Adelaide, UTC+10:30). OWNER-RATIFIED the same evening (RAT-48;\n'
     'decision log entry 244). H-1 v10 brought up to date the same day,**',
     'the edition line'),
    ('**It is a CANDIDATE: not ratified.** The reviewer passed v11 for continuity and preservation of authority in\n'
     'EX_306, with two narrow corrections and three observations. **Revision r1** makes them and adds what happened\n'
     'after v11 was written (entries 239 to 243), by `exchange/CLAUDE_WEB_TOOLS/h1v11r1/make_h1_v11r1.py`;\n'
     '`H1_v11_TO_v11r1.diff` beside it is the exact difference for the reviewer\'s confirmation, and\n'
     '`H1_v10_TO_v11r1.diff` the whole difference from the installed edition. H-1 v10 stays\n'
     'installed and unchanged in `doc/HANDOVER/`.',
     '**Status: OWNER-RATIFIED 24 November 2026 (RAT-48; decision log entry 244),** after the reviewer\'s PASS for\n'
     'continuity and preservation of authority (EX_306, with two narrow corrections and three observations) and its\n'
     'focused PASS of the corrected candidate, revision r1 (EX_307). Revision r1 made those corrections and added\n'
     'what happened after v11 was first written (entries 239 to 243), by\n'
     '`exchange/CLAUDE_WEB_TOOLS/h1v11r1/make_h1_v11r1.py`; `H1_v10_TO_v11r1.diff` beside that builder is the whole\n'
     'difference from H-1 v10. **This is the installed Claude handover.** It is the ratified candidate\n'
     '(`exchange/CLAUDE_WEB_TOOLS/h1v11r1/out/Claude_Primary_Handover_H1_v11r1.md`, SHA-256\n'
     f'`{CANDIDATE_SHA256}`) with its status statements and the\n'
     'statements the ratification made out of date changed; `exchange/CLAUDE_WEB_TOOLS/rat48/H1_v11r1_CANDIDATE_TO_FINAL.diff`\n'
     'is the exact difference. H-1 v10 (RAT-45) stays in `doc/HANDOVER/` as history. `exchange/CONTINUITY_NOW.md` with\n'
     'the decision log carries whatever is newer. It authorises nothing.',
     'the status statement'),
    ('**Replaces, once ratified:** H-1 v10 and its blurb (RAT-45), which stay where they are as history.',
     '**Replaces:** H-1 v10 and its blurb (RAT-45), which stay where they are as history.',
     'the "replaces" line'),
    ('   edition: the last RAT is RAT-45 (this handover); the newest EX is EX_296 (the reviewer\'s focused PASS of this\n'
     '   edition); the newest decision log entry is 215 (RAT-45).',
     '   edition (v11): the last RAT is RAT-48 (this handover); the newest EX is EX_307 (the reviewer\'s focused PASS\n'
     '   of this edition); the newest decision log entry is 244 (RAT-48).',
     'section 0A item 3: the newest numbers'),
    ('**Next numbers at this edition (r1): EX_307, decision log entry 244, RAT-48.**',
     '**Next numbers at this edition: EX_308, decision log entry 245, RAT-49.**',
     'section 0D: the next numbers'),
    ('RAT-47: the file-form standard (entry 237). The next\n'
     '   register edition is still owed (section 12.8 item 5) and now also records RAT-45, RAT-46 and RAT-47.',
     'RAT-47: the file-form standard (entry 237). RAT-48: this handover (entry 244). The next\n'
     '   register edition is still owed (section 12.8 item 5) and now also records RAT-45 to RAT-48.',
     'section 0D item 1: the records'),
    ('It read this handover\'s v11 in EX_306 (PASS for continuity; two narrow corrections, made in r1), and the',
     'It read this handover\'s v11 in EX_306 (PASS for continuity; two narrow corrections, made in r1) and passed r1\n'
     '    in EX_307, and the',
     'section 0D item 14: the reviewer\'s review of this handover'),
    ('16. **What waits, at this edition (r1).** On the reviewer: its confirmation of `H1_v11_TO_v11r1.diff`. On the\n'
     '    owner: then his decision on this H-1 v11 (it would be RAT-48).',
     '16. **What waits, at this edition.** On the reviewer: nothing. On the owner: nothing (this handover is\n'
     '    ratified, RAT-48).',
     'section 0D item 16: who is waited on'),
    ('2. **Done: this edition ratified (RAT-45, entry 215)** after EX_295 and EX_296.',
     '2. **Done: H-1 v10 ratified (RAT-45, entry 215)** after EX_295 and EX_296, and this edition, H-1 v11, ratified\n'
     '   (RAT-48, entry 244) after EX_306 and EX_307.',
     'section 10 item 2: which edition was ratified when'),
)

BLURB_CHANGES = (
    ('# Introductory blurb for H-1 v11 CANDIDATE: for a new Claude chat (paste everything below the line)',
     '# Introductory blurb for H-1 v11: for a new Claude chat (paste everything below the line)',
     'the blurb\'s title'),
    ('H-1 v11 (a candidate: the installed H-1 v10 brought up to date the same day, with one new section, 0D; check '
     'it against H-1 v10 with the exact difference beside it).',
     'H-1 v11 (ratified on 24 November 2026, RAT-48: H-1 v10 brought up to date the same day, with one new section, '
     '0D).',
     'what the handover is'),
    ('exchange/CLAUDE_WEB_TOOLS/h1v11r1/out/Claude_Primary_Handover_H1_v11r1.md (or '
     'doc/HANDOVER/Claude_Primary_Handover_H1_v11.md if it has been installed there) and follow its section 0',
     'doc/HANDOVER/Claude_Primary_Handover_H1_v11.md and follow its section 0',
     'where the handover is'),
)


def git_bytes(repository: Path, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD; it refuses if the path is not there."""
    return subprocess.run(['git', '-C', str(repository), 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha256_of(data: bytes) -> str:
    """The SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def changed(text: str, changes) -> str:
    """Apply counted replacements: each old text must be found exactly once and each new text must be ASCII.
    Returns the new text; refuses (assertion) otherwise."""
    final = text
    for old, new, what in changes:
        assert final.count(old) == 1, f'{what}: the old text is found {final.count(old)} times, not once'
        new.encode('ascii')
        final = final.replace(old, new)
    return final


def exact_difference(before: str, after: str, before_label: str, after_label: str) -> str:
    """The unified difference of two texts with no context lines, as one text."""
    return ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                        before_label, after_label, n=0))


def main(repository: Path) -> int:
    """Check the candidate and its blurb, write the installed files and the two diffs, print their hashes;
    return 0."""
    candidate, blurb = git_bytes(repository, CANDIDATE), git_bytes(repository, CANDIDATE_BLURB)
    assert sha256_of(candidate) == CANDIDATE_SHA256, 'the candidate at HEAD is not the one the owner ratified'
    assert sha256_of(blurb) == BLURB_SHA256, 'the blurb at HEAD is not the one the owner ratified'
    assert not (repository / INSTALLED).exists() and not (repository / INSTALLED_BLURB).exists(), 'already installed'
    text, blurb_text = candidate.decode('utf-8'), blurb.decode('utf-8')
    final, final_blurb = changed(text, CHANGES), changed(blurb_text, BLURB_CHANGES)
    carried = lambda t: t[t.index(CARRIED_FROM):t.index(CARRIED_TO)]
    assert carried(final) == carried(text), 'sections 1, 2 and 2A are not carried byte for byte'
    for written in (final, final_blurb):
        assert '\r' not in written and written.endswith('\n')
    assert 'CANDIDATE' not in final_blurb and 'h1v11r1' not in final_blurb
    (repository / INSTALLED).write_bytes(final.encode('utf-8'))
    (repository / INSTALLED_BLURB).write_bytes(final_blurb.encode('utf-8'))
    here = Path(__file__).resolve().parent
    (here / DIFF_NAME).write_bytes(exact_difference(text, final, 'H-1 v11r1 candidate (as passed in EX_307)',
                                                    'H-1 v11 (installed)').encode('utf-8'))
    (here / BLURB_DIFF_NAME).write_bytes(exact_difference(blurb_text, final_blurb,
                                                          'H-1 v11r1 candidate blurb (as passed in EX_307)',
                                                          'H-1 v11 blurb (installed)').encode('utf-8'))
    print(f'{sha256_of(final.encode("utf-8"))}  {len(final.splitlines())} lines  {INSTALLED}')
    print(f'{sha256_of(final_blurb.encode("utf-8"))}  {INSTALLED_BLURB}')
    for name in (DIFF_NAME, BLURB_DIFF_NAME):
        print(f'{sha256_of((here / name).read_bytes())}  {name}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
