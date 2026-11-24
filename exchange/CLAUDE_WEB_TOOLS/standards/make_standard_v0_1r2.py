"""Write the file-form standard's candidate v0.1r2 from the candidate v0.1r1, and the exact difference.

What this file is for
    The reviewer's EX_304 passed FFS-C01 to FFS-C03 and asked one narrow correction of FFS-C04: the candidate
    v0.1r1 promised that the conversion could be undone from its list of hashes alone, which is not generally
    true (two different files can become the same bytes when their line endings are made uniform). This script
    removes that promise and makes the owner's checked copy the way back, by replacements that must each match
    exactly once, and writes FILE_FORM_STANDARD_v0_1r2_CANDIDATE.md and the unified difference beside it. Nothing
    else is changed; v0.1r1 and the trial's evidence stay as they were.

Which part of the specification it carries out
    None; the standard is to become a note of ratification to the specification v0.6.

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_standard_v0_1r2.py   (run in this folder)
"""
import difflib
import hashlib
import sys
from pathlib import Path

OLD_NAME = 'FILE_FORM_STANDARD_v0_1r1_CANDIDATE.md'
NEW_NAME = 'FILE_FORM_STANDARD_v0_1r2_CANDIDATE.md'
DIFF_NAME = 'FILE_FORM_STANDARD_v0_1r1_TO_v0_1r2.diff'
# The SHA-256 of v0.1r1 as the reviewer checked it in EX_304.
OLD_SHA = '5a4d8a234a02951635e1c01032007d84ee82f80befacd2806098ea4a89f8485c'

# Passages replaced, each occurring exactly once in v0.1r1.
PASSAGES = [
    ("# The project's standard for the form of its text files (line endings) - v0.1r1 CANDIDATE",
     "# The project's standard for the form of its text files (line endings) - v0.1r2 CANDIDATE"),
    ("FFS-C04 (section 7: a second run, undoing, locks, a copy first,\n"
     "what is and is not proved).",
     "FFS-C04 (section 7: a second run, locks, a copy first,\n"
     "what is and is not proved)."),
    ("and the trial's evidence stay as they were; `FILE_FORM_STANDARD_v0_1_TO_v0_1r1.diff` is the exact difference.\n",
     "and the trial's evidence stay as they were; `FILE_FORM_STANDARD_v0_1_TO_v0_1r1.diff` is the exact difference.\n"
     "**v0.1r2 (24 November 2026):** the one narrow correction of the reviewer's EX_304 (which passed FFS-C01, C02 and\n"
     "C03): v0.1r1 promised that the conversion could be undone from its list alone. That is not generally true and\n"
     "is removed; the way back is the owner's copy, checked before the conversion begins (section 7). Nothing else\n"
     "is changed; `FILE_FORM_STANDARD_v0_1r1_TO_v0_1r2.diff` is the exact difference.\n"),
    ("   **It can be undone from the same list:** asked to undo, it turns each file whose hash is the \"after\" back into\n"
     "   the \"before\".\n",
     "   **The way back is the owner's copy, not the list.** Recovery is from the owner's pre-conversion copy of the\n"
     "   project folder, checked before the conversion begins: the program reads the copy and goes on only if every\n"
     "   file it is about to convert, and every file that is about to be removed, is in the copy with the same\n"
     "   SHA-256 as in the tree. The \"before\" hashes it records verify, afterwards, that the original files have been\n"
     "   recovered exactly. **The conversion list is not itself a backup:** making line endings uniform can turn two\n"
     "   different files into the same bytes, so a path and two hashes cannot rebuild an original. No undo is built.\n"),
    ("   **Before it runs** the owner makes his own copy of the project folder; the ways back are the undo, or that\n"
     "   copy.\n",
     "   **Before it runs** the owner makes his own copy of the project folder. That copy is the one way back, for\n"
     "   the converted files, for DEV's own settings file and for the derived outputs that are removed.\n"),
]


def main() -> int:
    """Apply every replacement exactly once and write the new candidate and the difference; return 0.
    Refuses (assert) if v0.1r1 is not the bytes the reviewer checked, or a passage is not found exactly once."""
    here = Path(__file__).resolve().parent
    old_bytes = (here / OLD_NAME).read_bytes()
    assert hashlib.sha256(old_bytes).hexdigest() == OLD_SHA, 'v0.1r1 is not the bytes the reviewer checked'
    old_text = old_bytes.decode('ascii')
    new_text = old_text
    for old_piece, new_piece in PASSAGES:
        assert old_text.count(old_piece) == 1, f'not exactly once in v0.1r1: {old_piece[:70]!r}'
        new_text = new_text.replace(old_piece, new_piece)
    for promise in ('asked to undo', 'the undo, or', 'undoing', 'It can be undone'):
        assert promise not in new_text, f'the promise of an undo is left: {promise!r}'
    old_lines = set(old_text.split('\n'))
    too_long = [line for line in new_text.split('\n') if len(line) > 120 and line not in old_lines]
    assert not too_long, f'a new line is longer than 120 characters: {too_long[0][:60]!r}'
    (here / NEW_NAME).write_bytes(new_text.encode('ascii'))
    difference = ''.join(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                              OLD_NAME, NEW_NAME))
    (here / DIFF_NAME).write_bytes(difference.encode('ascii'))
    for name in (OLD_NAME, NEW_NAME, DIFF_NAME):
        print(hashlib.sha256((here / name).read_bytes()).hexdigest(), name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
