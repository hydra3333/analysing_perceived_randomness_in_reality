#!/usr/bin/env python3
"""Builds the Claude handover H-1 v13 and its blurb from the installed H-1 v12.

What this file is for
    H-1 v12 was installed on the morning of 25 November 2026 (RAT-51). The same morning the ratification register
    v0.33 was ratified (RAT-53), the owner decided where the file-form checker belongs and slice A of build step 3
    was resumed. At the owner's request (decision log entry 267) this script brings the handover up to date for a
    change of Claude chat: it reads the installed H-1 v12 and its blurb from Git at HEAD (each asserted by
    SHA-256), makes counted replacements (each old text must occur exactly once, line endings set aside), adds
    four items to section 0E, computes the SHA-256 of the files those items name, asserts that sections 1, 2 and
    2A are identical, and writes into out/, each in the standard's form (CRLF):
        Claude_Primary_Handover_H1_v13_<CANDIDATE or FINAL>.md  and  ..._introductory_blurb.md
        H1_v12_TO_v13_<...>_DIFFERENCE.txt  and  H1_v12_TO_v13_<...>_blurb_DIFFERENCE.txt

Which part of the project's rules it carries out
    H-1 section 8.5 (a new edition from the exact Git blob by counted replacements, the builder travelling with
    it); doc/FILE_FORM_STANDARD_v0_2.md section 5 (every text file Claude adds is CRLF).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:
        python3 -I make_h1_v13.py <repository root> candidate
        python3 -I make_h1_v13.py <repository root> final "<status words of the handover>" "<status words of the blurb>"
It refuses (an assertion) on any failure: a wrong input hash, an anchor not found exactly once, a changed carried
region, a non-ASCII byte in new text, or a leftover placeholder.
"""
import difflib
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The texts lie beside this file; isolated mode (-I) leaves that folder off Python's path, so it is put on it.
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
from h1_v13_texts import (BLURB_REPLACEMENTS, HANDOVER_REPLACEMENTS, IDENTITY_FILES, INSERT_BEFORE,   # noqa: E402
                          NEW_ITEMS)

OUT = os.path.join(HERE, 'out')
# The installed handover and blurb (RAT-51), with the SHA-256 the decision log's entry 262 records.
V12 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v12.md'
V12_SHA = '41a20b7ddac9fee4fcb4ed2e5592c8dafafa8b50b1cf2dae9e2c8a91deaa29cd'
V12_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v12_introductory_blurb.md'
V12_BLURB_SHA = 'ed150c814e392203d380124023692a7d60af714ec08b76e758c87bb5371f38c0'
# The status words of a candidate: of the handover's header, and of the blurb's first paragraph.
CANDIDATE_STATUS = ('CANDIDATE: not ratified and not read by the reviewer; H-1 v12 (RAT-51) is the installed Claude '
                    'handover until the owner ratifies this one.')
CANDIDATE_BLURB_STATUS = 'a candidate until I ratify it'
# Sections 1, 2 and 2A are carried unchanged: from the first heading to the second.
CARRIED_FROM, CARRIED_TO = '## 1. Roles and workflow', '### 2B.'
# The line ending of every file this script writes (the standard: a new text file is CRLF).
LINE_ENDING = '\r\n'


def git_bytes(root: str, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD. Refuses (CalledProcessError) a path HEAD does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    """Replace one passage that must occur exactly once; the new text must be ASCII. Refuses (assertion) otherwise."""
    assert text.count(old) == 1, f'not exactly once ({text.count(old)}): {old[:70]!r}'
    new.encode('ascii')
    return text.replace(old, new)


def write(name: str, text: str) -> str:
    """Write one output file as ASCII with every line ending CRLF; return its SHA-256."""
    assert '\r' not in text and text.endswith('\n'), f'{name}: built with LF and one final line ending'
    data = text.replace('\n', LINE_ENDING).encode('ascii')
    with open(os.path.join(OUT, name), 'wb') as handle:
        handle.write(data)
    return sha(data)


def main(root: str, kind: str, status: str, blurb_status: str) -> int:
    """Build the two documents and the two differences; print each output's SHA-256; return 0."""
    old_bytes, old_blurb_bytes = git_bytes(root, V12), git_bytes(root, V12_BLURB)
    assert sha(old_bytes) == V12_SHA and sha(old_blurb_bytes) == V12_BLURB_SHA, 'not the installed H-1 v12'
    # H-1 v12 is CRLF in Git; the texts are matched and built with LF and written CRLF.
    old = old_bytes.decode('ascii').replace('\r\n', '\n')
    old_blurb = old_blurb_bytes.decode('ascii').replace('\r\n', '\n')
    new = old
    for old_piece, new_piece in HANDOVER_REPLACEMENTS:
        assert old.count(old_piece) == 1, f'not exactly once in H-1 v12: {old_piece[:70]!r}'
        new = replace_once(new, old_piece, new_piece)
    identities = '| File | SHA-256 |\n|---|---|\n' + ''.join(
        f'| `{path}` | `{sha(git_bytes(root, path))}` |\n' for path in IDENTITY_FILES)
    items = NEW_ITEMS.replace('@@IDENTITIES@@', identities.rstrip('\n'))
    new = replace_once(new, INSERT_BEFORE, items + INSERT_BEFORE)
    new = replace_once(new, '@@STATUS@@', status)
    carried = lambda text: text[text.index(CARRIED_FROM):text.index(CARRIED_TO)]
    assert carried(old) == carried(new), 'sections 1, 2 and 2A are not carried unchanged'
    assert '@@' not in new and new.endswith('\n')
    new_blurb = old_blurb
    for old_piece, new_piece in BLURB_REPLACEMENTS:
        assert old_blurb.count(old_piece) == 1, f'not exactly once in the blurb: {old_piece[:70]!r}'
        new_blurb = replace_once(new_blurb, old_piece, new_piece)
    new_blurb = replace_once(new_blurb, '@@BLURB_STATUS@@', blurb_status)
    # The new blurb names H-1 v12 twice, each on purpose: what v13 is built from, and what items 13 to 16 follow.
    assert new_blurb.count('v12') == 2, f'the blurb names v12 {new_blurb.count("v12")} times, not the two intended'
    os.makedirs(OUT, exist_ok=True)
    tag = kind.upper()
    out_name = f'Claude_Primary_Handover_H1_v13_{tag}.md'
    out_blurb = f'Claude_Primary_Handover_H1_v13_{tag}_introductory_blurb.md'
    print(write(out_name, new), out_name)
    print(write(out_blurb, new_blurb), out_blurb)
    for name, before, after, label, target in (
            (f'H1_v12_TO_v13_{tag}_DIFFERENCE.txt', old, new, V12, out_name),
            (f'H1_v12_TO_v13_{tag}_blurb_DIFFERENCE.txt', old_blurb, new_blurb, V12_BLURB, out_blurb)):
        difference = ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                                  label, 'out/' + target))
        print(write(name, difference), name)
    return 0


if __name__ == '__main__':
    assert sys.argv[2] in ('candidate', 'final')
    if sys.argv[2] == 'candidate':
        sys.exit(main(sys.argv[1], 'candidate', CANDIDATE_STATUS, CANDIDATE_BLURB_STATUS))
    sys.exit(main(sys.argv[1], 'final', sys.argv[3], sys.argv[4]))
