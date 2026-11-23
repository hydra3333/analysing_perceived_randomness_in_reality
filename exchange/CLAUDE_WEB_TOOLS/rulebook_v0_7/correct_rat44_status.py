"""Correct the status words of the installed rulebook v0.7's version line (after EX_289; owner, 23 November 2026).

What this file is for
    The rulebook v0.7 was installed (RAT-44) with a version line that said the candidate's last three edits "were
    ratified without a further review". Two minutes after the owner ratified, the reviewer passed those exact bytes
    (EX_289). The owner asked for the line to say so. This script changes those words and nothing else: it checks
    the installed file by its SHA-256, makes one replacement that must match exactly once, and writes the file and
    the exact diff. No rule text is touched.

Which part of the specification it carries out
    None of the system specification; H-1 v9 section 8.6 (the rulebook amendment before a runner rehearsal).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python correct_rat44_status.py <repository clone>
"""
import difflib
import hashlib
import sys
from pathlib import Path

TARGET = 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'
# The rulebook v0.7 as installed for RAT-44 (decision log entry 192).
TARGET_SHA256 = '3e6125f137e12266a3979c4fe173d8752207bf7163ac53c11bf6f6cf14bb121f'
DIFF_NAME = 'CLAUDE_v0_7_STATUS_CORRECTION.diff'
OLD_WORDS = ('after the reviewer\'s two reviews (EX_286 and EX_287), with every correction they asked made (the candidate '
             'v0.7r2; its last three edits, which EX_287 asked for, were ratified without a further review).')
NEW_WORDS = ('after the reviewer\'s two reviews (EX_286 and EX_287), with every correction they asked made (the candidate '
             'v0.7r2), and passed by the reviewer in those exact bytes the same evening (EX_289).')


def main(repository: Path) -> int:
    """Check the installed file, change the status words, write the file and the diff, print the new hash; return 0."""
    target = repository / TARGET
    data = target.read_bytes()
    assert hashlib.sha256(data).hexdigest() == TARGET_SHA256, 'the installed rulebook is not v0.7 as installed for RAT-44'
    text = data.decode('ascii')
    assert text.count(OLD_WORDS) == 1, f'the status words are found {text.count(OLD_WORDS)} times, not once'
    final = text.replace(OLD_WORDS, NEW_WORDS)
    assert '\r' not in final and final.endswith('\n')
    diff = ''.join(difflib.unified_diff(text.splitlines(keepends=True), final.splitlines(keepends=True),
                                        'CLAUDE.md (v0.7, as installed for RAT-44)', 'CLAUDE.md (v0.7, status words corrected)',
                                        n=0))
    target.write_bytes(final.encode('ascii'))
    (Path(__file__).resolve().parent / DIFF_NAME).write_text(diff, encoding='ascii', newline='\n')
    print(f'{hashlib.sha256(final.encode("ascii")).hexdigest()}  {len(final)} bytes  {TARGET}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
