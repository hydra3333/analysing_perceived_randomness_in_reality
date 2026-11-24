#!/usr/bin/env python3
"""Builds the Claude handover H-1 v12 and its blurb from the installed H-1 v11.

What this file is for
    H-1 v11 was installed on 24 November 2026 (RAT-48). That night and the next morning the file-form standard
    v0.2 was ratified (RAT-49), DEV was converted to it (RAT-50) and the lock file's line was corrected. At the
    owner's request (decision log entry 262) this script brings the handover up to date: it reads the installed
    H-1 v11 and its blurb from Git at HEAD (each asserted by SHA-256), makes counted replacements of the
    statements those events made out of date (each old text must occur exactly once), inserts one new section,
    0E, computes the SHA-256 of the files that section names, asserts that sections 1, 2 and 2A are identical,
    and writes into out/, each in the standard's form (CRLF):
        Claude_Primary_Handover_H1_v12.md  and  Claude_Primary_Handover_H1_v12_introductory_blurb.md
        H1_v11_TO_v12_DIFFERENCE.txt  and  H1_v11_TO_v12_blurb_DIFFERENCE.txt  (line endings set aside)

Which part of the project's rules it carries out
    H-1 section 8.5 (a new edition from the exact Git blob by counted replacements, the builder travelling with
    it); doc/FILE_FORM_STANDARD_v0_2.md section 5 (every text file Claude adds is CRLF).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_h1_v12.py <repository root>
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
from h1_v12_texts import BLURB_REPLACEMENTS, HANDOVER_REPLACEMENTS, IDENTITY_FILES, SECTION_0E   # noqa: E402

OUT = os.path.join(HERE, 'out')
# The installed handover and blurb (RAT-48), with the SHA-256 the decision log's entry 244 records.
V11 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v11.md'
V11_SHA = '91a9c1814587bcbe0ee9ce23de51a6ed5008932d4c721e9f52c0467930c09318'
V11_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v11_introductory_blurb.md'
V11_BLURB_SHA = '16d7feedc6102bc87e62d5e6d4a464a38013ffd6f8e2262d0a80320387d9b5ec'
# Sections 1, 2 and 2A are carried unchanged: from the first heading to the second.
CARRIED_FROM, CARRIED_TO = '## 1. Roles and workflow', '### 2B.'
# The new section goes in before this heading (after section 0D).
INSERT_BEFORE = '## 0C. Sections 1, 2 and 2A are carried unchanged'
STANDARD = 'doc/FILE_FORM_STANDARD_v0_2.md'
OUT_NAME = 'Claude_Primary_Handover_H1_v12.md'
OUT_BLURB = 'Claude_Primary_Handover_H1_v12_introductory_blurb.md'
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


def main(root: str) -> int:
    """Build the two documents and the two differences; print each output's SHA-256; return 0."""
    old_bytes, old_blurb_bytes = git_bytes(root, V11), git_bytes(root, V11_BLURB)
    assert sha(old_bytes) == V11_SHA and sha(old_blurb_bytes) == V11_BLURB_SHA, 'not the installed H-1 v11'
    old, old_blurb = old_bytes.decode('utf-8'), old_blurb_bytes.decode('utf-8')
    new = old
    for old_piece, new_piece in HANDOVER_REPLACEMENTS:
        assert old.count(old_piece) == 1, f'not exactly once in H-1 v11: {old_piece[:70]!r}'
        new = replace_once(new, old_piece, new_piece)
    identities = '| File | SHA-256 |\n|---|---|\n' + ''.join(
        f'| `{path}` | `{sha(git_bytes(root, path))}` |\n' for path in IDENTITY_FILES)
    section = SECTION_0E.replace('@@IDENTITIES@@', identities.rstrip('\n'))
    section.encode('ascii')
    new = replace_once(new, INSERT_BEFORE, section + '\n' + INSERT_BEFORE)
    new = replace_once(new, '@@STANDARD_SHA@@', sha(git_bytes(root, STANDARD)))
    carried = lambda text: text[text.index(CARRIED_FROM):text.index(CARRIED_TO)]
    assert carried(old) == carried(new), 'sections 1, 2 and 2A are not carried unchanged'
    assert '@@' not in new and new.endswith('\n')
    new_blurb = old_blurb
    for old_piece, new_piece in BLURB_REPLACEMENTS:
        assert old_blurb.count(old_piece) == 1, f'not exactly once in the blurb: {old_piece[:70]!r}'
        new_blurb = replace_once(new_blurb, old_piece, new_piece)
    # The new blurb names H-1 v11 twice, each on purpose: what v12 is built from, and what section 0E follows.
    assert new_blurb.count('v11') == 2, f'the blurb names v11 {new_blurb.count("v11")} times, not the two intended'
    os.makedirs(OUT, exist_ok=True)
    print(write(OUT_NAME, new), OUT_NAME)
    print(write(OUT_BLURB, new_blurb), OUT_BLURB)
    for name, before, after, label, target in (
            ('H1_v11_TO_v12_DIFFERENCE.txt', old, new, V11, OUT_NAME),
            ('H1_v11_TO_v12_blurb_DIFFERENCE.txt', old_blurb, new_blurb, V11_BLURB, OUT_BLURB)):
        difference = ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                                  label, 'out/' + target))
        print(write(name, difference), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
