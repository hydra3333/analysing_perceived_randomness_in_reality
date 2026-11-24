#!/usr/bin/env python3
"""Builds the candidate v0.2 of the file-form standard from the installed v0.1: one narrow amendment and two
corrections of fact.

What this file is for
    While the conversion was being prepared Claude found three statements of the ratified standard
    (doc/FILE_FORM_STANDARD_v0_1.md, RAT-47) that do not hold: the root attribute line does reach GAIS, so the
    file needs three lines (the owner approved them, decision log entry 251); the count and the place of the
    writes that name no line ending; and how the working copy is refreshed. This script reads v0.1 from Git at
    HEAD (asserted by SHA-256), makes counted replacements (each old passage must occur exactly once), and
    writes the candidate and the exact difference beside itself. Nothing else of the standard is changed.

Which part of the project's rules it carries out
    H-1 section 8.5 (a new edition from the exact Git blob by counted replacements, the builder travelling with
    it).

Which of the project's own modules it uses
    None (standard library and Git only).

What uses it
    Claude, in the cloud workspace. Usage:  python3 -I make_standard_v0_2.py <repository root>
"""
import difflib
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V01 = 'doc/FILE_FORM_STANDARD_v0_1.md'
# The installed standard's SHA-256 (decision log entry 237).
V01_SHA = '97034474f1a7e9c54a14b9554b45666cb1fa031d566545433a0412d4312f8335'
OUT_NAME = 'FILE_FORM_STANDARD_v0_2_CANDIDATE.md'
DIFF_NAME = 'FILE_FORM_STANDARD_v0_1_TO_v0_2.diff'

REPLACEMENTS = [
    # ---- the edition's own statements
    ("# The project's standard for the form of its text files (line endings) - v0.1 (OWNER-RATIFIED, RAT-47, 24 November 2026)",
     "# The project's standard for the form of its text files (line endings) - v0.2 CANDIDATE (v0.1, RAT-47, with one narrow amendment and two corrections of fact)"),
    ("**Date:** 24 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status: OWNER-RATIFIED on 24 November 2026\n"
     "(RAT-47, decision log entry 237),**",
     "**This edition: v0.2 CANDIDATE, 24 November 2026, evening.** It is v0.1 with three passages changed, each marked\n"
     "\"v0.2\", all found by Claude while the conversion was being prepared and simulated (decision log entries 242,\n"
     "245 and 250): **(A) section 5 and section 8 item 7: the root `.gitattributes` holds three lines, not one,** because\n"
     "the one line does reach `GAIS\\`, which v0.1 denied; the owner approved the three lines (decision log entry 251);\n"
     "**(B) section 4:** how many writes name no line ending, where they are, and which can be corrected; **(C) section\n"
     "5 and section 11:** the refresh of the owner's working copy and the staging of the converted files are done by a\n"
     "program, because plain Git commands do not do it. **The policy is unchanged, and nothing else is changed.**\n"
     "Built from v0.1's Git bytes by `exchange/CLAUDE_WEB_TOOLS/standards/make_standard_v0_2.py`;\n"
     "`FILE_FORM_STANDARD_v0_1_TO_v0_2.diff` beside it is the exact difference. **Not ratified, and not yet read by the\n"
     "reviewer; v0.1 stays in force until the owner ratifies this.**\n\n"
     "**Date of v0.1:** 24 November 2026. **Author:** the Claude web chat (on Fable (High)). **Status of v0.1: OWNER-RATIFIED on 24 November 2026\n"
     "(RAT-47, decision log entry 237),**"),
    # ---- (B) section 4
    ("- **A test reads the code and fails on any write that names none** (found today, to be corrected: 17 in the old\n"
     "  system's code, most of them in its self-tests; none in the new engine).",
     "- **A test reads the code and fails on any write that names none.** (v0.2: v0.1 said here \"found today, to be\n"
     "  corrected: 17 in the old system's code\". The test's own search finds eighteen in the project's programs, all\n"
     "  in old self-tests, and none in the new engine. **Sixteen are in `src/results_master_v0_2.py`, which section 3A\n"
     "  leaves exactly as it is: they stay,** and the test leaves that file out by name with the other five. Two, in\n"
     "  `src/two_site_results_check_v0_7.py`, are corrected. The search reads the project's programs; what a test\n"
     "  writes in a temporary folder is outside this standard by section 2, so the tests' own code is not searched.)"),
    # ---- (A) section 5: the three lines
    ("- **The root `.gitattributes` says one thing: `* -text`.** Git then never changes a line ending, in either\n"
     "  direction, on any PC, whatever its own `core.autocrlf` setting is. The existing special lines are no longer\n"
     "  needed.",
     "- **The root `.gitattributes` holds three lines** (v0.2; the owner, section 8 item 7):\n"
     "\n"
     "      * -text\n"
     "      GAIS/** !text\n"
     "      GAIS/**/*.bat text eol=crlf\n"
     "\n"
     "  By the first, Git never changes a line ending of this project's files, in either direction, on any PC,\n"
     "  whatever its own `core.autocrlf` setting is; the project's earlier special lines are no longer needed. The\n"
     "  second and the third are for `GAIS\\` alone (the next point)."),
    ("- **It does not reach `GAIS\\`, and this standard says so** (EX_303 FFS-C03; the owner assented: section 8 item\n"
     "  6). That folder is another project's. It has two attribute files of its own\n"
     "  (`GAIS/OUTLANDISH_01/.gitattributes`, `GAIS/OUTLANDISH_01/OUTLANDISH_WSL/.gitattributes`), which Git obeys for the\n"
     "  paths under them, and the second tells Git to convert that project's `.py`, `.sh`, `.md` and `.bat` files.\n"
     "  Claude never writes under `GAIS\\`. So the true statement is: **Git converts nothing anywhere in this project;\n"
     "  under `GAIS\\` that other project's own rules stay as they are.** The repository holds no other attribute file.",
     "- **`GAIS\\` is left exactly as it is, and it takes two lines of the root file to do that** (v0.2; EX_303\n"
     "  FFS-C03; the owner: section 8 items 6 and 7). That folder is another project's. It has two attribute files of\n"
     "  its own (`GAIS/OUTLANDISH_01/.gitattributes`, `GAIS/OUTLANDISH_01/OUTLANDISH_WSL/.gitattributes`), which Git obeys\n"
     "  for the paths they name, and the second tells Git to convert that project's `.py`, `.sh`, `.md` and `.bat`\n"
     "  files. **v0.1 said that the root line `* -text` \"does not reach `GAIS\\`\". That was wrong.** Those two files\n"
     "  name only some kinds of file: of GAIS's 204 tracked files (24 November 2026), 173 are named by neither, and\n"
     "  the root line would have governed them. On a PC whose Git converts line endings their working copies would\n"
     "  then have differed from Git's bytes, unseen. The line `GAIS/** !text` takes the root file's say about text\n"
     "  away for everything under `GAIS\\`, so that Git does there exactly what it did before this standard (GAIS's\n"
     "  own two files, and each PC's own settings). The line `GAIS/**/*.bat text eol=crlf` keeps, for GAIS alone, the\n"
     "  one earlier line of the root file that applied to it. Checked by Claude in a clone made with\n"
     "  `core.autocrlf=true`: with the three lines every GAIS file's stored form, form on disk and attribute are,\n"
     "  file by file, what they were. Claude never writes under `GAIS\\`. So the true statement is: **Git converts\n"
     "  nothing anywhere in this project; under `GAIS\\` Git does exactly what it did before.** The repository holds\n"
     "  no other attribute file."),
    # ---- (C) section 5: the refresh
    ("- **The owner's working copy needs one refresh,** on the day: with `core.autocrlf=true` Git has, until now, written\n"
     "  CRLF copies of files it stores as LF (every document he has pulled). Under `* -text` those copies would all show\n"
     "  as changed. The exact, rehearsed commands for that one refresh are part of the conversion's sheet.",
     "- **The owner's working copy needs one refresh,** on the day: with `core.autocrlf=true` Git has, until now, written\n"
     "  CRLF copies of files it stores as LF (every document he has pulled). **v0.2: v0.1 said that under `* -text`\n"
     "  those copies \"would all show as changed\" and that rehearsed commands would refresh them. Neither holds.**\n"
     "  Git goes by each file's remembered size and time and does not read the file again: it shows none of those\n"
     "  copies as changed, it passes over a converted file that it believes unchanged when asked to stage it, and\n"
     "  it rewrites no working copy that it believes current, even when told to force it (Claude's simulation,\n"
     "  decision log entry 250). Left so, a later `git add` could put a CRLF copy of frozen history into Git. **So\n"
     "  the refresh and the staging are done by a small program of the conversion's package, by content:** it stages\n"
     "  each listed file with exactly the bytes it has on disk; it rewrites, with Git's own bytes, the working copy\n"
     "  of every other tracked file that Git converts nothing for and that differs from Git's bytes in line endings\n"
     "  only; it refuses a file that differs in more; it proves that what is on disk is what is staged or\n"
     "  committed; and it commits and pushes nothing. It calls Git, as the check of a commit in the point above\n"
     "  does: that is what Git is for, and it is never a check of whether a tree may run. It is rehearsed by the\n"
     "  runner before the day."),
    # ---- (A) section 8: the owner's decision
    ("   the statement of section 5 stands: nothing converts anywhere in this project; `GAIS\\` keeps that other\n"
     "   project's own rules, and nothing under it is changed.",
     "   the statement of section 5 stands: nothing converts anywhere in this project; `GAIS\\` keeps that other\n"
     "   project's own rules, and nothing under it is changed. (v0.2: it takes two more lines of the root file to\n"
     "   make that true: item 7.)\n"
     "\n"
     "**Put to the owner on 24 November 2026 with the fault of fact of section 5 (decision log entry 250), and decided\n"
     "by him the same evening, 21:48 (decision log entry 251):**\n"
     "\n"
     "7. **The root attribute file holds three lines** (section 5). His words: \"yes to Question: may the root attribute\n"
     "   file hold three lines instead of the one the standard ratified? yes to Recommendation: approve the three\n"
     "   lines\"."),
    # ---- (C) section 11
    ("- The exact commands of the one refresh of the owner's working copy under `* -text`, rehearsed by the runner in a",
     "- (v0.2: not commands but a program: section 5.) The one refresh of the owner's working copy, rehearsed by the runner in a"),
]


def git_bytes(root: str, path: str) -> bytes:
    """The bytes Git holds for a path at HEAD. Refuses (CalledProcessError) a path HEAD does not have."""
    return subprocess.run(['git', '-C', root, 'show', f'HEAD:{path}'], check=True, capture_output=True).stdout


def sha(data: bytes) -> str:
    """SHA-256 of some bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def main(root: str) -> int:
    """Build the candidate and the difference; print each output's SHA-256; return 0. Refuses (assertion) a
    wrong input hash, an old passage not found exactly once, a non-ASCII byte in new text, or a CR."""
    old_bytes = git_bytes(root, V01)
    assert sha(old_bytes) == V01_SHA, 'not the installed standard v0.1'
    old = old_bytes.decode('utf-8')
    new = old
    for old_piece, new_piece in REPLACEMENTS:
        assert old.count(old_piece) == 1, f'not exactly once in v0.1 ({old.count(old_piece)}): {old_piece[:70]!r}'
        assert new.count(old_piece) == 1, f'an earlier replacement disturbed: {old_piece[:70]!r}'
        new_piece.encode('ascii')
        new = new.replace(old_piece, new_piece)
    assert '\r' not in new and new.endswith('\n')
    difference = ''.join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                              V01, OUT_NAME))
    for name, text in ((OUT_NAME, new), (DIFF_NAME, difference)):
        with open(os.path.join(HERE, name), 'wb') as handle:
            handle.write(text.encode('utf-8'))
        print(sha(text.encode('utf-8')), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
