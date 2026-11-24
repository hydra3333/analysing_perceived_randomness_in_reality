"""Finalise RAT-49: install the file-form standard v0.2 in doc/.

What this file is for
    The owner ratified the candidate v0.2r1 of the file-form standard on 24 November 2026 (RAT-49; decision log
    entry 253), after the reviewer's review (EX_310) and its focused PASS (EX_311). This script reads the
    candidate from Git at HEAD (checked by its SHA-256), applies counted replacements (each old text must be
    found exactly once) to its title and its statements of status, and writes doc/FILE_FORM_STANDARD_v0_2.md.
    The standard v0.1 (RAT-47) stays in doc/ as history. The exact difference from the ratified candidate is
    written beside this file.

Which part of the project's rules it carries out
    H-1 section 8.5: finalising after ratification changes only the statements of status; as at RAT-47.

Which of the project's own modules it uses
    None (the standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python finalise_rat49.py <repository clone>
"""
import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

CANDIDATE = 'exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_2r1_CANDIDATE.md'
# The candidate as the reviewer passed it (EX_311) and the owner ratified it (entry 253).
CANDIDATE_SHA256 = '6939095c5cd23bb1910559966bfad51d32b94a4c6d2a7d1fde2f2bb405a67a69'
INSTALLED = 'doc/FILE_FORM_STANDARD_v0_2.md'
DIFF_NAME = 'FILE_FORM_STANDARD_v0_2r1_CANDIDATE_TO_FINAL.diff'

# (old text, new text, what it is)
CHANGES = (
    ("# The project's standard for the form of its text files (line endings) - v0.2 CANDIDATE (v0.1, RAT-47, with one narrow amendment and two corrections of fact)",
     "# The project's standard for the form of its text files (line endings) - v0.2 (OWNER-RATIFIED, RAT-49, 24 November 2026)",
     'the title'),
    ('**This edition: v0.2 CANDIDATE, 24 November 2026, evening.** It is v0.1 with three passages changed, each marked\n',
     '**This edition: v0.2, OWNER-RATIFIED on 24 November 2026 (RAT-49, decision log entry 253),** as a note of\n'
     'ratification to the specification v0.6, beside the coding practices, after the reviewer\'s review (EX_310) and\n'
     'its FOCUSED PASS (EX_311) of the exact candidate v0.2r1 (SHA-256\n'
     f'`{CANDIDATE_SHA256}`), of which this is the installed text;\n'
     '`exchange/CLAUDE_WEB_TOOLS/rat49/FILE_FORM_STANDARD_v0_2r1_CANDIDATE_TO_FINAL.diff` is the exact difference. The\n'
     'owner\'s words: "I ratify it per EX_311_ChatGPT.md". **It replaces v0.1 (RAT-47), which stays in `doc/` as\n'
     'history. It changes nothing by itself and authorises nothing on the owner\'s PC:** the conversion, every install\n'
     'and every run are each his own go.\n'
     '\n'
     '**What v0.2 is:** v0.1 with three passages changed, each marked\n',
     'the edition and status statement'),
    ('**Not ratified; v0.1 stays in force\n'
     'until the owner ratifies this.**',
     '**Ratified since (RAT-49): the\n'
     'statement at the head of this file.**',
     'the candidate\'s own "not ratified"'),
)


def git_bytes(repository: Path, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD; it refuses if the path is not there."""
    return subprocess.run(['git', '-C', str(repository), 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha256_of(data: bytes) -> str:
    """The SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def main(repository: Path) -> int:
    """Check the candidate, write the installed file and the diff, print their hashes; return 0. Refuses
    (assertion) a candidate that is not the ratified bytes, an old text not found exactly once, a file already
    installed, or a result that is not ASCII with LF."""
    candidate = git_bytes(repository, CANDIDATE)
    assert sha256_of(candidate) == CANDIDATE_SHA256, 'the candidate at HEAD is not the one the owner ratified'
    assert not (repository / INSTALLED).exists(), 'already installed'
    text = candidate.decode('ascii')
    final = text
    for old, new, what in CHANGES:
        assert final.count(old) == 1, f'{what}: the old text is found {final.count(old)} times, not once'
        new.encode('ascii')
        final = final.replace(old, new)
    assert '\r' not in final and final.endswith('\n') and 'CANDIDATE (v0.1' not in final
    (repository / INSTALLED).write_bytes(final.encode('ascii'))
    diff = ''.join(difflib.unified_diff(text.splitlines(keepends=True), final.splitlines(keepends=True),
                                        'the standard v0.2r1 candidate (as passed in EX_311)',
                                        'the standard v0.2 (installed)', n=0))
    (Path(__file__).resolve().parent / DIFF_NAME).write_bytes(diff.encode('ascii'))
    print(f'{sha256_of(final.encode("ascii"))}  {len(final.splitlines())} lines  {INSTALLED}')
    print(f'{sha256_of(diff.encode("ascii"))}  {DIFF_NAME}')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
