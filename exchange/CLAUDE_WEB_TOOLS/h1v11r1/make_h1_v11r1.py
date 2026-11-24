#!/usr/bin/env python3
"""Builds the Claude handover candidate H-1 v11r1 and its blurb from the candidate H-1 v11.

What this file is for
    The reviewer read the candidate H-1 v11 in EX_306: PASS for continuity, with two narrow corrections (H11-C01,
    H11-C02) and three observations. This script makes them, and adds what happened after v11 was written
    (decision log entries 239 to 243), by counted replacements in v11's exact Git bytes (each old text must occur
    exactly once). It asserts that sections 1, 2 and 2A are still byte for byte those of the installed H-1 v10,
    and writes into out/:
        Claude_Primary_Handover_H1_v11r1.md  and  Claude_Primary_Handover_H1_v11r1_introductory_blurb.md
        H1_v11_TO_v11r1.diff  and  H1_v11_TO_v11r1_blurb.diff     (what the reviewer confirms)
        H1_v10_TO_v11r1.diff  and  H1_v10_TO_v11r1_blurb.diff     (the whole difference from the installed edition)

Which part of the project's rules it carries out
    H-1 v10 section 8.5 (a new edition from the exact Git blob by counted replacements, the builder travelling
    with it).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_h1_v11r1.py <repository root>
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
from h1_v11r1_texts import BLURB_REPLACEMENTS, HANDOVER_REPLACEMENTS     # noqa: E402

OUT = os.path.join(HERE, 'out')
# The candidate v11 and its blurb, with the SHA-256 that decision log entry 238 records and EX_306 confirmed.
V11 = 'exchange/CLAUDE_WEB_TOOLS/h1v11/out/Claude_Primary_Handover_H1_v11.md'
V11_SHA = '71b3f08c369dd38ccbe40690fa947e8ef4e2094a33a9419e1739beb43b94e2e5'
V11_BLURB = 'exchange/CLAUDE_WEB_TOOLS/h1v11/out/Claude_Primary_Handover_H1_v11_introductory_blurb.md'
V11_BLURB_SHA = '1ebcb8eae3660d49647004f59078900281c5c6538ab8a354d7439ae459606495'
# The installed edition (RAT-45), for the carried region and the whole difference.
V10 = 'doc/HANDOVER/Claude_Primary_Handover_H1_v10.md'
V10_SHA = '824e7f251d0ae43a8c045c42495537fa6a8a242c531eb677132882ccb467a69b'
V10_BLURB = 'doc/HANDOVER/Claude_Primary_Handover_H1_v10_introductory_blurb.md'
V10_BLURB_SHA = '6c0ab5cf4133628edcfbe602e2aa7b362b13c2f9f331054bba9cf4fd4761cfb9'
# Sections 1, 2 and 2A are carried byte for byte from the installed edition: from the first heading to the second.
CARRIED_FROM, CARRIED_TO = '## 1. Roles and workflow', '### 2B.'
# The two files whose SHA-256 the new rows of section 0D's table hold.
REPORT, EX306 = 'CLAUDE_CODE_WORKING_FOLDER_TREE/outbox/REPORT_T028.md', 'exchange/EX_306_ChatGPT.md'
OUT_NAME = 'Claude_Primary_Handover_H1_v11r1.md'
OUT_BLURB = 'Claude_Primary_Handover_H1_v11r1_introductory_blurb.md'


def git_bytes(root: str, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD. Refuses (CalledProcessError) a path HEAD does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def git_text(root: str, path: str, expected_sha: str) -> str:
    """The text Git holds for a path at HEAD, refused (assertion) unless its SHA-256 is the one expected."""
    data = git_bytes(root, path)
    assert sha(data) == expected_sha, f'{path} is not the file expected: {sha(data)}'
    return data.decode('utf-8')


def replace_all_once(text: str, replacements, what: str) -> str:
    """Make each counted replacement: the old passage must occur exactly once in the text as it was given, and
    the new text must be ASCII. Refuses (assertion) otherwise. Returns the new text."""
    new = text
    for old_piece, new_piece in replacements:
        assert text.count(old_piece) == 1, f'not exactly once in {what} ({text.count(old_piece)}): {old_piece[:70]!r}'
        assert new.count(old_piece) == 1, f'an earlier replacement disturbed: {old_piece[:70]!r}'
        new_piece.encode('ascii')
        new = new.replace(old_piece, new_piece)
    return new


def write(name: str, text: str) -> str:
    """Write one output file as UTF-8 with LF; return its SHA-256. Refuses (assertion) a CR."""
    data = text.encode('utf-8')
    assert b'\r' not in data, f'{name} holds a CR'
    with open(os.path.join(OUT, name), 'wb') as handle:
        handle.write(data)
    return sha(data)


def difference(before: str, after: str, before_label: str, after_label: str) -> str:
    """The unified difference of two texts, as one text."""
    return ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                        before_label, after_label))


def main(root: str) -> int:
    """Build the two candidates and the four differences; print each output's SHA-256; return 0."""
    v11, v11_blurb = git_text(root, V11, V11_SHA), git_text(root, V11_BLURB, V11_BLURB_SHA)
    v10, v10_blurb = git_text(root, V10, V10_SHA), git_text(root, V10_BLURB, V10_BLURB_SHA)
    new = replace_all_once(v11, HANDOVER_REPLACEMENTS, 'H-1 v11')
    new = new.replace('@@REPORT_SHA@@', sha(git_bytes(root, REPORT))).replace('@@EX306_SHA@@', sha(git_bytes(root, EX306)))
    carried = lambda text: text[text.index(CARRIED_FROM):text.index(CARRIED_TO)]
    assert carried(v10) == carried(new), 'sections 1, 2 and 2A are not carried byte for byte from H-1 v10'
    assert '@@' not in new and '\r' not in new and new.endswith('\n')
    new_blurb = replace_all_once(v11_blurb, BLURB_REPLACEMENTS, 'the v11 blurb')
    os.makedirs(OUT, exist_ok=True)
    print(write(OUT_NAME, new), OUT_NAME)
    print(write(OUT_BLURB, new_blurb), OUT_BLURB)
    for name, before, after, label in (('H1_v11_TO_v11r1.diff', v11, new, V11),
                                       ('H1_v11_TO_v11r1_blurb.diff', v11_blurb, new_blurb, V11_BLURB),
                                       ('H1_v10_TO_v11r1.diff', v10, new, V10),
                                       ('H1_v10_TO_v11r1_blurb.diff', v10_blurb, new_blurb, V10_BLURB)):
        target = OUT_BLURB if 'blurb' in name else OUT_NAME
        print(write(name, difference(before, after, label, 'out/' + target)), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
