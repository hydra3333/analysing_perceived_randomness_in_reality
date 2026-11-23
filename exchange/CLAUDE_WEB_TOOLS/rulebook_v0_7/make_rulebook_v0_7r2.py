"""Make the CANDIDATE v0.7r2 of the runner's rulebook from the v0.7r1 candidate, by counted edits (after EX_287).

What this file is for
    The reviewer's EX_287 closed the three findings of EX_286 and asked one last correction of wording before
    RAT-44, F287-C01: the last sentence of rule 11 said that a task step that so much as names the owner's real DEV
    tree is a STOP, which would refuse the copy from DEV into a scratch tree by reading that section 2A item 3
    permits (owner, decision log entry 184). It also asked that a stale "(rule 11 is unchanged)" in section 2A
    item 5 be put right. This script reads the v0.7r1 candidate as reviewed (checked by its SHA-256), applies the
    edits below, each of which must match exactly once, and writes the corrected candidate with two exact diffs:
    from the installed v0.6 and from the v0.7r1 candidate. The candidate has no force until the owner ratifies it
    (RAT-44).

Which part of the specification it carries out
    None of the system specification; H-1 v9 section 8.6 (the rulebook amendment before a runner rehearsal).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_rulebook_v0_7r2.py <repository clone>
"""
import difflib
import hashlib
import sys
from pathlib import Path

INSTALLED = 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'
REVIEWED_NAME = 'CLAUDE_v0_7r1_CANDIDATE.md'
# The SHA-256 of the v0.7r1 candidate as the reviewer read it (EX_287 section 1).
REVIEWED_SHA256 = 'a0fd3526c333941a3bc54c362b9d3c0621d71ed38336d20a624d931ffddceb11'
CANDIDATE_NAME = 'CLAUDE_v0_7r2_CANDIDATE.md'
DIFF_FROM_INSTALLED = 'CLAUDE_v0_6_TO_v0_7r2_CANDIDATE.diff'
DIFF_FROM_REVIEWED = 'CLAUDE_v0_7r1_TO_v0_7r2_CANDIDATE.diff'

# (old text, new text, what it is)
EDITS = (
    ('**Version:** v0.7r1 CANDIDATE, 23 November 2026 (r1: the three corrections of wording of the reviewer\'s EX_286).',
     '**Version:** v0.7r2 CANDIDATE, 23 November 2026 (r1: the three corrections of wording of the reviewer\'s EX_286; r2: the one correction of EX_287, the STOP sentence of rule 11).',
     'the version line'),
    ('This exception never grants access to the owner\'s real DEV, QA or PROD trees, their backup folders or their settings. If a task step names one of these places, that is a STOP.',
     'This exception never permits a write to the owner\'s real DEV tree beyond what sections 3 and 4 allow, any access to his real QA or PROD trees or their backup folders, or reading or editing a real tree\'s `ENVIRONMENT.ini`. A task step that asks for any of those is a STOP. Copying from the real DEV tree into a scratch tree by reading, which section 2A item 3 permits, is not.',
     'rule 11, its last two sentences (F287-C01)'),
    ('is a STOP (rule 11 is unchanged).',
     'is a STOP (rule 11\'s protections for the real trees still apply).',
     'section 2A item 5, the stale parenthesis (EX_287 section 3)'),
)


def sha256_of_text(text: str) -> str:
    """The SHA-256 of ASCII text as 64 hexadecimal characters."""
    return hashlib.sha256(text.encode('ascii')).hexdigest()


def main(repository: Path) -> int:
    """Write the corrected candidate and the two diffs beside this file; print what was done; return 0."""
    here = Path(__file__).resolve().parent
    installed = (repository / INSTALLED).read_text(encoding='ascii')
    reviewed = (here / REVIEWED_NAME).read_text(encoding='ascii')
    assert sha256_of_text(reviewed) == REVIEWED_SHA256, 'the v0.7r1 candidate is not the one the reviewer read'
    new = reviewed
    for old, replacement, what in EDITS:
        assert new.count(old) == 1, f'{what}: the old text is found {new.count(old)} times, not once'
        new = new.replace(old, replacement)
    (here / CANDIDATE_NAME).write_text(new, encoding='ascii', newline='\n')
    for name, before, label in ((DIFF_FROM_INSTALLED, installed, 'CLAUDE.md (v0.6, installed)'),
                                (DIFF_FROM_REVIEWED, reviewed, 'CLAUDE.md (v0.7r1 CANDIDATE, as reviewed in EX_287)')):
        diff = ''.join(difflib.unified_diff(before.splitlines(keepends=True), new.splitlines(keepends=True),
                                            label, 'CLAUDE.md (v0.7r2 CANDIDATE)', n=0))
        (here / name).write_text(diff, encoding='ascii', newline='\n')
    print(f'{len(EDITS)} edits, each matched once; v0.7r1 candidate {REVIEWED_SHA256[:12]}... -> v0.7r2 candidate '
          f'{sha256_of_text(new)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
