"""Make the CANDIDATE v0.7r1 of the runner's rulebook from the v0.7 candidate, by counted edits (after EX_286).

What this file is for
    The reviewer's EX_286 asked for three narrow corrections of wording in the v0.7 candidate before RAT-44:
    F286-B01 (rule 11 forbade what section 2A allows in a scratch tree), F286-C01 (section 7 was narrower than
    the owner's decision of entry 186) and F286-C02 (what the two scratch environment scripts themselves call).
    This script reads the v0.7 candidate as reviewed (checked by its SHA-256), applies the edits below, each of
    which must match exactly once, and writes the corrected candidate with two exact diffs: from the installed
    v0.6 and from the v0.7 candidate. The candidate has no force until the owner ratifies it (RAT-44).

Which part of the specification it carries out
    None of the system specification; H-1 v9 section 8.6 (the rulebook amendment before a runner rehearsal).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_rulebook_v0_7r1.py <repository clone>
"""
import difflib
import hashlib
import sys
from pathlib import Path

INSTALLED = 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'
REVIEWED_NAME = 'CLAUDE_v0_7_CANDIDATE.md'
# The SHA-256 of the v0.7 candidate as the reviewer read it (EX_286 section 6).
REVIEWED_SHA256 = '52797e44a83188f5938c30b471072ad549824ad049c5849df2229dd65ee4bcdf'
CANDIDATE_NAME = 'CLAUDE_v0_7r1_CANDIDATE.md'
DIFF_FROM_INSTALLED = 'CLAUDE_v0_6_TO_v0_7r1_CANDIDATE.diff'
DIFF_FROM_REVIEWED = 'CLAUDE_v0_7_TO_v0_7r1_CANDIDATE.diff'

# (old text, new text, what it is)
EDITS = (
    ('**Version:** v0.7 CANDIDATE, 23 November 2026.',
     '**Version:** v0.7r1 CANDIDATE, 23 November 2026 (r1: the three corrections of wording of the reviewer\'s EX_286).',
     'the version line'),
    ('rules 3, 4, 5, 7, 9 and 10 and sections 3, 5 and 7 point to it and are otherwise unchanged;',
     'rules 3, 4, 5, 7, 9 and 10 and sections 3, 5 and 7 point to it and are otherwise unchanged; rule 11 says that it means the owner\'s real QA and PROD trees and gains the one scratch-only qualification for a tree and its settings file;',
     'the version line: rule 11'),
    ('**The QA and PROD trees are not yours.** Never read, list, write, create, rename or delete anything in the QA tree, the PROD tree or their backup folders, wherever the owner\'s settings place them (for example `D:\\TEST_BED`, `D:\\TEST_BED_backups`, `G:\\a_p_r_i_r` and `T:\\a_p_r_i_r_backups`). Never read or edit an `ENVIRONMENT.ini` file. Never create a tree.',
     '**The owner\'s real QA and PROD trees are not yours.** Never read, list, write, create, rename or delete anything in the owner\'s real QA tree, his real PROD tree or their backup folders, wherever his settings place them (for example `T:\\a_p_r_i_r`, `G:\\a_p_r_i_r` and `T:\\a_p_r_i_r_backups`). A scratch tree that is given the role QA or PROD for a rehearsal is not one of them, and gives no access to them. Never read or edit an `ENVIRONMENT.ini` file and never create a tree, except within a task-authorised scratch tree wholly under `D:\\DELETE_ME\\` as section 2A permits. This exception never grants access to the owner\'s real DEV, QA or PROD trees, their backup folders or their settings.',
     'rule 11 (F286-B01), with its example places brought up to date (decision log entry 181)'),
    ('Rules 1, 2, 6, 8, 11 and 12 are not touched by it.',
     'Rules 1, 2, 6, 8 and 12 are not touched by it. Rule 11 keeps the owner\'s real QA and PROD trees and their backups out of reach without exception; its one qualification, written into the rule itself, is for a scratch tree and that tree\'s own settings file.',
     'section 2A, the opening line (F286-B01)'),
    ('each only when the task file names it and only against a tree whose root lies under `D:\\DELETE_ME\\`.',
     'each only when the task file names it and only against a tree whose root lies under `D:\\DELETE_ME\\`. A name in this list is no permission by itself: only a program that has been reviewed and installed, and that the task file names with its arguments, is run.',
     'section 2A item 5: a name is not permission (EX_286 4(d))'),
    ('The package downloads those two scripts make are the one network use this section adds.',
     'The package downloads those two scripts make are the one network use this section adds. What those two scripts call themselves (the tree\'s own activation script, and `pip`) is part of running them; you never run an activation script or `pip` yourself.',
     'section 2A item 7 (F286-C02)'),
    ('or anything from outside this repository (what the commands of a section 2A task print excepted).',
     'or anything from outside this repository. **The one exception, for a section 2A task:** what its commands print, and text that the task file names to be copied from under `D:\\DELETE_ME\\` into this one report, under a heading that says where each came from. Nothing else is copied out, nothing goes to another place than this report, and personal details stay out in every case.',
     'section 7 (F286-C01)'),
)


def sha256_of_text(text: str) -> str:
    """The SHA-256 of ASCII text as 64 hexadecimal characters."""
    return hashlib.sha256(text.encode('ascii')).hexdigest()


def main(repository: Path) -> int:
    """Write the corrected candidate and the two diffs beside this file; print what was done; return 0."""
    here = Path(__file__).resolve().parent
    installed = (repository / INSTALLED).read_text(encoding='ascii')
    reviewed = (here / REVIEWED_NAME).read_text(encoding='ascii')
    assert sha256_of_text(reviewed) == REVIEWED_SHA256, 'the v0.7 candidate is not the one the reviewer read'
    new = reviewed
    for old, replacement, what in EDITS:
        assert new.count(old) == 1, f'{what}: the old text is found {new.count(old)} times, not once'
        new = new.replace(old, replacement)
    (here / CANDIDATE_NAME).write_text(new, encoding='ascii', newline='\n')
    for name, before, label in ((DIFF_FROM_INSTALLED, installed, 'CLAUDE.md (v0.6, installed)'),
                                (DIFF_FROM_REVIEWED, reviewed, 'CLAUDE.md (v0.7 CANDIDATE, as reviewed in EX_286)')):
        diff = ''.join(difflib.unified_diff(before.splitlines(keepends=True), new.splitlines(keepends=True),
                                            label, 'CLAUDE.md (v0.7r1 CANDIDATE)', n=0))
        (here / name).write_text(diff, encoding='ascii', newline='\n')
    print(f'{len(EDITS)} edits, each matched once; v0.7 candidate {REVIEWED_SHA256[:12]}... -> v0.7r1 candidate '
          f'{sha256_of_text(new)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
