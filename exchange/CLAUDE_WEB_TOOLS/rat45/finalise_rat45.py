"""Finalise RAT-45: install H-1 v10 and its blurb in doc/HANDOVER/.

What this file is for
    The owner ratified the corrected H-1 v10 candidate on 24 November 2026 (RAT-45; decision log entry 215), after the
    reviewer's focused PASS (EX_296). This script reads the candidate and its blurb from Git at HEAD (each checked
    by its SHA-256), applies counted replacements (each old text must be found exactly once) to the status paragraph
    and to the statements the ratification itself makes out of date (the owner's standing instruction, entry 153),
    and writes the installed handover. The blurb is installed with its bytes unchanged. H-1 v9 and its blurb stay
    where they are as history. The exact difference from the candidate is written beside this file.

Which part of the project's rules it carries out
    H-1 section 8.5: "Finalising after ratification changes only the status line"; as at RAT-41 and RAT-43, with the
    owner's instruction on out-of-date statements.

Which of the project's own modules it uses
    None (the standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python finalise_rat45.py <repository clone>
"""
import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

CANDIDATE = 'exchange/CLAUDE_WEB_TOOLS/h1v10/out/Claude_Primary_Handover_H1_v10.md'
CANDIDATE_BLURB = 'exchange/CLAUDE_WEB_TOOLS/h1v10/out/Claude_Primary_Handover_H1_v10_introductory_blurb.md'
# The corrected candidate and its blurb as the reviewer passed them (EX_296; decision log entry 214).
CANDIDATE_SHA256 = 'a769316d0f886595966a73e1d047173036dd4523a362921cdf18bfd15b07960b'
BLURB_SHA256 = '6c0ab5cf4133628edcfbe602e2aa7b362b13c2f9f331054bba9cf4fd4761cfb9'
INSTALLED = 'doc/HANDOVER/Claude_Primary_Handover_H1_v10.md'
INSTALLED_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v10_introductory_blurb.md'
DIFF_NAME = 'H1_v10_CANDIDATE_TO_FINAL.diff'
H2_V6 = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_CANDIDATE_20261124.md'

# (old text, new text, what it is)
CHANGES = (
    ('**Status:** CANDIDATE, 24 November 2026, corrected after the reviewer\'s review (EX_295: three corrections of\n'
     'wording, all made), for its focused recheck and the owner\'s ratification (RAT-45). Until it is ratified, H-1 v9 '
     '(RAT-43) is the installed Claude handover, and `exchange/CONTINUITY_NOW.md` with the decision log\n'
     'carries whatever is newer. It authorises nothing.',
     '**Status:** OWNER-RATIFIED 24 November 2026 (RAT-45; decision log entry 215), after the reviewer\'s review (EX_295:\n'
     'three corrections of wording, all made) and its focused PASS (EX_296). The owner\'s words, given to the reviewer\n'
     'before its recheck and recorded in EX_296: "If this is any good then I ratify it now". It is the installed\n'
     'Claude handover; H-1 v9 (RAT-43) stays as history. It is the reviewed candidate\n'
     '(`exchange/CLAUDE_WEB_TOOLS/h1v10/out/Claude_Primary_Handover_H1_v10.md`, SHA-256\n'
     f'`{CANDIDATE_SHA256}`) with this status paragraph and the\n'
     'statements the ratification made out of date changed; `exchange/CLAUDE_WEB_TOOLS/rat45/H1_v10_CANDIDATE_TO_FINAL.diff`\n'
     'is the exact difference. `exchange/CONTINUITY_NOW.md` with the decision log carries whatever is newer. It\n'
     'authorises nothing.',
     'the status paragraph'),
    ('   edition: the last RAT is RAT-44 (the runner\'s rulebook v0.7); the newest EX is EX_295 (the reviewer\'s review of\n'
     '   this edition\'s first candidate); the newest decision log entry is 214 (this candidate corrected).',
     '   edition: the last RAT is RAT-45 (this handover); the newest EX is EX_296 (the reviewer\'s focused PASS of this\n'
     '   edition); the newest decision log entry is 215 (RAT-45).',
     'section 0A item 3: the newest numbers'),
    ('2. **This edition:** to the reviewer, then the owner\'s ratification (RAT-45).',
     '2. **Done: this edition ratified (RAT-45, entry 215)** after EX_295 and EX_296. The reviewer has written its own\n'
     f'   H-2 v6 as a CANDIDATE (`{H2_V6}`; EX_296): it awaits the\n'
     '   owner\'s separate decision, and H-2 v5r1 stays the installed reviewer handover until then.',
     'section 10 item 2'),
    ('- **Waiting on the reviewer:** its review of this candidate.\n'
     '- **Waiting on the owner:** RAT-45 for this edition; his go for build step 3;',
     '- **Waiting on the reviewer:** nothing.\n'
     '- **Waiting on the owner:** his decision on the reviewer\'s H-2 v6 candidate (section 10 item 2); his go for build\n'
     '  step 3;',
     'section 12.8: who is waited on'),
    ('  9. The reviewer\'s handover: H-2 v5r1 describes the state before build step 2; the reviewer writes its own.',
     '  9. The reviewer\'s handover: H-2 v5r1 describes the state before build step 2; the reviewer has written H-2 v6\n'
     '     as a candidate, which is its own to finalise once the owner decides.',
     'section 12.8 item 9'),
)


def git_bytes(repository: Path, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD; it refuses if the path is not there."""
    return subprocess.run(['git', '-C', str(repository), 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha256_of(data: bytes) -> str:
    """The SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def main(repository: Path) -> int:
    """Check the candidate and its blurb, write the installed files and the diff, print their hashes; return 0."""
    candidate, blurb = git_bytes(repository, CANDIDATE), git_bytes(repository, CANDIDATE_BLURB)
    assert sha256_of(candidate) == CANDIDATE_SHA256, 'the candidate at HEAD is not the one the reviewer passed'
    assert sha256_of(blurb) == BLURB_SHA256, 'the blurb at HEAD is not the one the reviewer passed'
    git_bytes(repository, H2_V6)
    assert not (repository / INSTALLED).exists() and not (repository / INSTALLED_BLURB).exists(), 'already installed'
    text = candidate.decode('ascii')
    final = text
    for old, new, what in CHANGES:
        assert final.count(old) == 1, f'{what}: the old text is found {final.count(old)} times, not once'
        new.encode('ascii')
        final = final.replace(old, new)
    carried = lambda t: t[t.index('## 1. Roles and workflow'):t.index('### 2B.')]
    assert carried(final) == carried(text), 'sections 1, 2 and 2A are not carried byte for byte'
    assert '\r' not in final and final.endswith('\n')
    (repository / INSTALLED).write_bytes(final.encode('ascii'))
    (repository / INSTALLED_BLURB).write_bytes(blurb)
    diff = ''.join(difflib.unified_diff(text.splitlines(keepends=True), final.splitlines(keepends=True),
                                        'H-1 v10 candidate (as passed in EX_296)', 'H-1 v10 (installed)', n=0))
    (Path(__file__).resolve().parent / DIFF_NAME).write_text(diff, encoding='ascii', newline='\n')
    print(f'{sha256_of(final.encode("ascii"))}  {len(final.splitlines())} lines  {INSTALLED}')
    print(f'{sha256_of(blurb)}  {INSTALLED_BLURB} (the candidate blurb, bytes unchanged)')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
