#!/usr/bin/env python3
"""Builds the candidate v0.2r1 of the file-form standard from the candidate v0.2: the reviewer's one narrow
qualification of wording (EX_310 FFS2-C01) and its observation on section 5's wording.

What this file is for
    The reviewer read the candidate v0.2 in EX_310: A and C PASS, B's corrected count PASS, and one narrow
    qualification of section 4's wording before ratification, with an observation on how section 5 describes
    what ordinary Git commands did. This script reads the candidate v0.2 from Git at HEAD (asserted by SHA-256),
    makes counted replacements (each old passage must occur exactly once), and writes beside itself the
    candidate v0.2r1, its exact difference from v0.2 (what the reviewer confirms) and its exact difference from
    the installed v0.1 (the whole amendment).

Which part of the project's rules it carries out
    H-1 section 8.5 (counted replacements in the exact Git blob, the builder travelling with the candidate).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_standard_v0_2r1.py <repository root>
"""
import difflib
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V01 = 'doc/FILE_FORM_STANDARD_v0_1.md'
V01_SHA = '97034474f1a7e9c54a14b9554b45666cb1fa031d566545433a0412d4312f8335'
V02 = 'exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_2_CANDIDATE.md'
# The candidate the reviewer read in EX_310.
V02_SHA = '8a6ae261e57c467b72cfbd0b1c23dd6b4bf5a16fc6ab84d7c04de51c6b7d56c6'
OUT_NAME = 'FILE_FORM_STANDARD_v0_2r1_CANDIDATE.md'

REPLACEMENTS = [
    # ---- the edition's own statements
    ("5 and section 11:** the refresh of the owner's working copy and the staging of the converted files are done by a\n"
     "program, because plain Git commands do not do it.",
     "5 and section 11:** the refresh of the owner's working copy and the staging of the converted files are done by a\n"
     "program, because ordinary Git commands were not reliable for it in the simulated working copy."),
    ("**Not ratified, and not yet read by the\n"
     "reviewer; v0.1 stays in force until the owner ratifies this.**",
     "**r1 (24 November 2026):** the reviewer's EX_310 passed (A) and (C) and (B)'s corrected count, and asked one\n"
     "narrow qualification of section 4's wording (FFS2-C01), made here together with its observation on section 5's\n"
     "wording; `FILE_FORM_STANDARD_v0_2_TO_v0_2r1.diff` is the exact difference from the candidate it read, and\n"
     "`FILE_FORM_STANDARD_v0_1_TO_v0_2r1.diff` the whole difference from v0.1. **Not ratified; v0.1 stays in force\n"
     "until the owner ratifies this.**"),
    # ---- EX_310 FFS2-C01: section 4
    ("The search reads the project's programs; what a test\n"
     "  writes in a temporary folder is outside this standard by section 2, so the tests' own code is not searched.)",
     "The search covers the project's programs and excludes\n"
     "  tests' own temporary-fixture writes, which section 2 exempts. **Any test that writes an actual in-scope\n"
     "  project file remains subject to the standard** (r1; EX_310 FFS2-C01). That the tests' outputs are confined to\n"
     "  disposable fixtures is confirmed in the review of the conversion's package.)"),
    # ---- EX_310's observation on section 5
    ("those copies \"would all show as changed\" and that rehearsed commands would refresh them. Neither holds.**\n"
     "  Git goes by each file's remembered size and time and does not read the file again: it shows none of those\n"
     "  copies as changed, it passes over a converted file that it believes unchanged when asked to stage it, and\n"
     "  it rewrites no working copy that it believes current, even when told to force it (Claude's simulation,\n"
     "  decision log entry 250). Left so, a later `git add` could put a CRLF copy of frozen history into Git.",
     "those copies \"would all show as changed\" and that rehearsed commands would refresh them. Neither proved\n"
     "  reliable.** Where Git finds a file's remembered size and time unchanged it does not read the file again.\n"
     "  In Claude's simulated working copy (decision log entry 250; r1, worded as EX_310 asked) ordinary commands\n"
     "  were therefore not reliable for this migration: `git status` showed none of those copies as changed; a plain\n"
     "  `git add` passed over the converted files it believed unchanged (a second command with another option did\n"
     "  stage them); and a forced checkout rewrote none of the 2,298 stale working copies. Left so, a later\n"
     "  `git add` could put a CRLF copy of frozen history into Git."),
]


def git_bytes(root: str, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD. Refuses (CalledProcessError) a path HEAD does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def main(root: str) -> int:
    """Build the candidate and the two differences; print each output's SHA-256; return 0. Refuses (assertion)
    a wrong input hash, an old passage not found exactly once, a non-ASCII byte in new text, or a CR."""
    v01_bytes, v02_bytes = git_bytes(root, V01), git_bytes(root, V02)
    assert sha(v01_bytes) == V01_SHA and sha(v02_bytes) == V02_SHA, 'not the installed v0.1 or the candidate v0.2'
    v01, v02 = v01_bytes.decode('utf-8'), v02_bytes.decode('utf-8')
    new = v02
    for old_piece, new_piece in REPLACEMENTS:
        assert v02.count(old_piece) == 1, f'not exactly once in v0.2 ({v02.count(old_piece)}): {old_piece[:70]!r}'
        assert new.count(old_piece) == 1, f'an earlier replacement disturbed: {old_piece[:70]!r}'
        new_piece.encode('ascii')
        new = new.replace(old_piece, new_piece)
    assert '\r' not in new and new.endswith('\n')
    outputs = {OUT_NAME: new}
    for name, before, label in (('FILE_FORM_STANDARD_v0_2_TO_v0_2r1.diff', v02, V02),
                                ('FILE_FORM_STANDARD_v0_1_TO_v0_2r1.diff', v01, V01)):
        outputs[name] = ''.join(difflib.unified_diff(before.splitlines(keepends=True),
                                                     new.splitlines(keepends=True), label, OUT_NAME))
    for name, text in outputs.items():
        with open(os.path.join(HERE, name), 'wb') as handle:
            handle.write(text.encode('utf-8'))
        print(sha(text.encode('utf-8')), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
