#!/usr/bin/env python3
"""Builds the reviewer handover H-2 v6r2 candidate and its blurb from the reviewer's own installed H-2 v6.

What this file is for
    The ChatGPT reviewer chat ended on 24 November 2026 without notice, after committing EX_303. At the owner's
    request (decision log entry 232) Claude brings the reviewer's handover up to date so that a new reviewer chat
    can be started, as it did on 21 and 23 November 2026 (H-2 v3r10 and H-2 v5r1). This script reads the installed
    H-2 v6 and its blurb from Git at HEAD (each asserted by SHA-256), replaces a few status statements of chapter 0
    and of the blurb by counted replacements (each old text must occur exactly once), adds one new section 0.13
    that holds everything since H-2 v6's evidence cutoff, asserts that sections 0.4 and 0.5 and everything from the
    historical chapters' heading to the end are byte-identical, and writes into out/:
        ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124.md  and  ..._introductory_blurb.md
        H2_v6_TO_v6r2.diff  and  H2_v6_TO_v6r2_blurb.diff
    The reviewer's files are not changed. No reviewer right, scientific rule or owner permission is changed.

Which part of the project's rules it carries out
    H-1 v10 section 8.5 (a new candidate from the exact Git blob by counted replacements, the builder travelling
    with it) and section 4.4 (Claude writes a reviewer continuity candidate when the reviewer chat is lost).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_h2_v6r2.py <repository root>
It refuses (an assertion) on any failure: a wrong input hash, an anchor not found exactly once, a changed carried
region, a non-ASCII byte in new text, or a CR.
"""
import difflib
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The texts lie beside this file; isolated mode (-I) leaves that folder off Python's path, so it is put on it.
sys.path.insert(0, HERE)
from h2_v6r2_texts import BLURB_REPLACEMENTS, HANDOVER_REPLACEMENTS, SECTION_0_13      # noqa: E402

OUT = os.path.join(HERE, 'out')
# The reviewer's installed handover and blurb (RAT-46), with the SHA-256 the decision log's entry 216 records.
V6 = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124.md'
V6_SHA = '588c52b9c08781956330676a3c13bda99b0c8fd90211139f74c26503adf174a1'
V6_BLURB = 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v6_20261124_introductory_blurb.md'
V6_BLURB_SHA = '58c8f5b2b13dabc63f3739c04a42dd6bb30784fcf9c40b504e65da72c8c8efe3'
# From this heading to the end the handover is carried byte for byte; so are sections 0.4 and 0.5.
HISTORY_HEADING = '# HISTORICAL INHERITED H-2 CHAPTERS (1-19)'
CARRIED_FROM, CARRIED_TO = '### 0.4 Current scientific identity', '### 0.6 Ratification notes'
# The new section goes in after section 0.12, before the rule line that precedes the historical chapters.
INSERT_BEFORE = '\n---\n\n' + HISTORY_HEADING
OUT_NAME = 'ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124.md'
OUT_BLURB = 'ChatGPT_Reviewer_Handover_H2_v6r2_CANDIDATE_20261124_introductory_blurb.md'


def git_text(root: str, path: str, expected_sha: str) -> str:
    """The text Git holds for a path at HEAD, its SHA-256 asserted. Refuses a path HEAD lacks or other bytes."""
    data = subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout
    assert hashlib.sha256(data).hexdigest() == expected_sha, f'{path}: not the bytes expected'
    assert b'\r' not in data, f'{path}: holds a CR'
    return data.decode('utf-8')


def replace_once(text: str, old: str, new: str) -> str:
    """Replace one passage that must occur exactly once; the new text must be ASCII. Refuses (assertion) otherwise."""
    assert text.count(old) == 1, f'not exactly once ({text.count(old)}): {old[:70]!r}'
    new.encode('ascii')
    return text.replace(old, new)


def write(name: str, text: str) -> str:
    """Write one output file as UTF-8 with LF; return its SHA-256."""
    data = text.encode('utf-8')
    assert b'\r' not in data
    with open(os.path.join(OUT, name), 'wb') as handle:
        handle.write(data)
    return hashlib.sha256(data).hexdigest()


def main(root: str) -> int:
    """Build the two candidates and the two differences; print each output's SHA-256; return 0."""
    old = git_text(root, V6, V6_SHA)
    new = old
    for old_piece, new_piece in HANDOVER_REPLACEMENTS:
        assert old.count(old_piece) == 1, f'not exactly once in H-2 v6: {old_piece[:70]!r}'
        new = replace_once(new, old_piece, new_piece)
    SECTION_0_13.encode('ascii')
    new = replace_once(new, INSERT_BEFORE, '\n' + SECTION_0_13 + INSERT_BEFORE)
    carried = lambda text: text[text.index(CARRIED_FROM):text.index(CARRIED_TO)]
    assert carried(old) == carried(new), 'sections 0.4 and 0.5 changed'
    assert old[old.index(HISTORY_HEADING):] == new[new.index(HISTORY_HEADING):], 'the historical chapters changed'

    old_blurb = git_text(root, V6_BLURB, V6_BLURB_SHA)
    new_blurb = old_blurb
    for old_piece, new_piece in BLURB_REPLACEMENTS:
        assert old_blurb.count(old_piece) == 1, f'not exactly once in the blurb: {old_piece[:70]!r}'
        new_blurb = replace_once(new_blurb, old_piece, new_piece)

    os.makedirs(OUT, exist_ok=True)
    print(write(OUT_NAME, new), OUT_NAME)
    print(write(OUT_BLURB, new_blurb), OUT_BLURB)
    for name, before, after, label in (('H2_v6_TO_v6r2.diff', old, new, V6), ('H2_v6_TO_v6r2_blurb.diff', old_blurb, new_blurb, V6_BLURB)):
        difference = ''.join(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                                  label, 'out/' + (OUT_NAME if after is new else OUT_BLURB)))
        print(write(name, difference), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
