"""Install the ratified local runner rulebook v0.7 (RAT-44; 23 November 2026).

What this file is for
    The project owner ratified the candidate v0.7r2 as RAT-44. This script reads that candidate from Git at HEAD
    (checked by its SHA-256), changes only the status words of its version line, and writes the result over
    CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md, which must hold the installed v0.6 bytes when this runs (Git keeps
    v0.6 in its history). It also writes, beside itself, the exact diff from the candidate to the installed file.
    It stops, with nothing written, on a wrong candidate, a wrong installed file, or if the status words are not
    found exactly once.

Which part of the specification it carries out
    None of the system specification; H-1 v9 section 8.6 (the rulebook amendment before a runner rehearsal).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python finalise_rat44.py <repository clone>
"""
import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

CANDIDATE = 'exchange/CLAUDE_WEB_TOOLS/rulebook_v0_7/CLAUDE_v0_7r2_CANDIDATE.md'
# The candidate the owner ratified (decision log entries 190 and 192).
CANDIDATE_SHA256 = 'faed89593e49c60f67789955a7e54f4bf3dd7a79c3cd5e76d4d7fdc71dc00e43'
TARGET = 'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md'
# The rulebook v0.6 as installed (RAT-42; decision log entry 156).
TARGET_SHA256 = 'f92f17f60db63990fc10a663778ec8d6a2b0737c9232895f1ee0af76ffdfa632'
DIFF_NAME = 'CLAUDE_v0_7r2_CANDIDATE_TO_FINAL.diff'
# The status words of the version line: the only text that differs between the candidate and the installed file.
OLD_STATUS = ('**Version:** v0.7r2 CANDIDATE, 23 November 2026 (r1: the three corrections of wording of the reviewer\'s '
              'EX_286; r2: the one correction of EX_287, the STOP sentence of rule 11). **NOT YET REVIEWED OR RATIFIED: '
              'until it is, v0.6 is the rulebook.** (v0.7:')
NEW_STATUS = ('**Version:** v0.7, 23 November 2026, ratified by the project owner the same day (RAT-44) after the '
              'reviewer\'s two reviews (EX_286 and EX_287), with every correction they asked made (the candidate '
              'v0.7r2; its last three edits, which EX_287 asked for, were ratified without a further review). (v0.7:')


def sha256_of(data: bytes) -> str:
    """The SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def main(repository: Path) -> int:
    """Check both files, write the installed rulebook and the diff, print the new hash; return 0."""
    candidate = subprocess.run(['git', '-C', str(repository), 'show', f'HEAD:{CANDIDATE}'], check=True,
                               capture_output=True).stdout
    assert sha256_of(candidate) == CANDIDATE_SHA256, 'the candidate at HEAD is not the one the owner ratified'
    target = repository / TARGET
    assert sha256_of(target.read_bytes().replace(b'\r\n', b'\n')) == TARGET_SHA256, 'the installed rulebook is not v0.6'
    text = candidate.decode('ascii')
    assert text.count(OLD_STATUS) == 1, f'the status words are found {text.count(OLD_STATUS)} times, not once'
    final = text.replace(OLD_STATUS, NEW_STATUS)
    data = final.encode('ascii')
    assert b'\r' not in data and data.endswith(b'\n')
    diff = ''.join(difflib.unified_diff(text.splitlines(keepends=True), final.splitlines(keepends=True),
                                        'CLAUDE.md (v0.7r2 CANDIDATE, as ratified)', 'CLAUDE.md (v0.7, installed)', n=0))
    target.write_bytes(data)
    (Path(__file__).resolve().parent / DIFF_NAME).write_text(diff, encoding='ascii', newline='\n')
    print(f'{sha256_of(data)}  {len(data)} bytes  {TARGET}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
