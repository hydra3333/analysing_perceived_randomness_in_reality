#!/usr/bin/env python3
"""Builds the Claude handover H-1 v11 candidate and its blurb from the installed H-1 v10.

What this file is for
    H-1 v10 was installed on 24 November 2026 (RAT-45). The same day the owner gave his go for build step 3, its
    plan was reviewed, he decided its open points, the file-form standard was written and ratified (RAT-47) and
    the reviewer chat changed. At the owner's request (decision log entry 238) this script brings the handover up
    to date: it reads the installed H-1 v10 and its blurb from Git at HEAD (each asserted by SHA-256), makes
    counted replacements of the status statements those events made out of date (each old text must occur exactly
    once), inserts one new section, 0D, with everything since, computes the SHA-256 of the files that section
    names, asserts that sections 1, 2 and 2A are byte-identical, and writes into out/:
        Claude_Primary_Handover_H1_v11.md  and  Claude_Primary_Handover_H1_v11_introductory_blurb.md
        H1_v10_TO_v11.diff  and  H1_v10_TO_v11_blurb.diff

Which part of the project's rules it carries out
    H-1 v10 section 8.5 (a new edition from the exact Git blob by counted replacements, the builder travelling
    with it).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_h1_v11.py <repository root>
It refuses (an assertion) on any failure: a wrong input hash, an anchor not found exactly once, a changed carried
region, a non-ASCII byte in new text, a CR, or a leftover placeholder.
"""
import difflib
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The texts lie beside this file; isolated mode (-I) leaves that folder off Python's path, so it is put on it.
sys.path.insert(0, HERE)
from h1_v11_texts import (BLURB_REPLACEMENTS, HANDOVER_REPLACEMENTS, IDENTITY_FILES,     # noqa: E402
                          SECTION_0D)

OUT = os.path.join(HERE, 'out')
# The installed handover and blurb (RAT-45), with the SHA-256 the decision log's entry 215 records.
V10 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v10.md'
V10_SHA = '824e7f251d0ae43a8c045c42495537fa6a8a242c531eb677132882ccb467a69b'
V10_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v10_introductory_blurb.md'
V10_BLURB_SHA = '6c0ab5cf4133628edcfbe602e2aa7b362b13c2f9f331054bba9cf4fd4761cfb9'
# Sections 1, 2 and 2A are carried byte for byte: from the first heading to the second.
CARRIED_FROM, CARRIED_TO = '## 1. Roles and workflow', '### 2B.'
# The new section goes in before this heading (after section 0B).
INSERT_BEFORE = '## 0C. Sections 1, 2 and 2A are carried unchanged'
STANDARD = 'doc/FILE_FORM_STANDARD_v0_1.md'
OUT_NAME = 'Claude_Primary_Handover_H1_v11.md'
OUT_BLURB = 'Claude_Primary_Handover_H1_v11_introductory_blurb.md'


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
    """Write one output file as UTF-8 with LF; return its SHA-256."""
    data = text.encode('utf-8')
    assert b'\r' not in data, f'{name} holds a CR'
    with open(os.path.join(OUT, name), 'wb') as handle:
        handle.write(data)
    return sha(data)


def main(root: str) -> int:
    """Build the two candidates and the two differences; print each output's SHA-256; return 0."""
    old_bytes, old_blurb_bytes = git_bytes(root, V10), git_bytes(root, V10_BLURB)
    assert sha(old_bytes) == V10_SHA and sha(old_blurb_bytes) == V10_BLURB_SHA, 'not the installed H-1 v10'
    old, old_blurb = old_bytes.decode('utf-8'), old_blurb_bytes.decode('utf-8')
    new = old
    for old_piece, new_piece in HANDOVER_REPLACEMENTS:
        assert old.count(old_piece) == 1, f'not exactly once in H-1 v10: {old_piece[:70]!r}'
        new = replace_once(new, old_piece, new_piece)
    identities = '| File | SHA-256 |\n|---|---|\n' + ''.join(
        f'| `{path}` | `{sha(git_bytes(root, path))}` |\n' for path in IDENTITY_FILES)
    section = SECTION_0D.replace('@@IDENTITIES@@', identities.rstrip('\n'))
    section.encode('ascii')
    new = replace_once(new, INSERT_BEFORE, section + '\n' + INSERT_BEFORE)
    new = replace_once(new, '@@STANDARD_SHA@@', sha(git_bytes(root, STANDARD)))
    carried = lambda text: text[text.index(CARRIED_FROM):text.index(CARRIED_TO)]
    assert carried(old) == carried(new), 'sections 1, 2 and 2A are not carried byte for byte'
    assert '@@' not in new and '\r' not in new and new.endswith('\n')
    new_blurb = old_blurb
    for old_piece, new_piece in BLURB_REPLACEMENTS:
        assert old_blurb.count(old_piece) == 1, f'not exactly once in the blurb: {old_piece[:70]!r}'
        new_blurb = replace_once(new_blurb, old_piece, new_piece)
    # The new blurb names H-1 v10 three times, each on purpose: what v11 is built from, what to check it
    # against, and what section 0D follows.
    assert new_blurb.count('v10') == 3, f'the blurb names v10 {new_blurb.count("v10")} times, not the three intended'
    os.makedirs(OUT, exist_ok=True)
    print(write(OUT_NAME, new), OUT_NAME)
    print(write(OUT_BLURB, new_blurb), OUT_BLURB)
    for name, before, after, label, target in (('H1_v10_TO_v11.diff', old, new, V10, OUT_NAME),
                                               ('H1_v10_TO_v11_blurb.diff', old_blurb, new_blurb, V10_BLURB, OUT_BLURB)):
        difference = ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                                  label, 'out/' + target))
        print(write(name, difference), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
