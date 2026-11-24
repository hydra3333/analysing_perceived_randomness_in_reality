"""RAT-47: install the ratified file-form standard in doc/, with its status statements brought up to date.

What this file is for
    The owner ratified the exact candidate FILE_FORM_STANDARD_v0_1r2_CANDIDATE.md as RAT-47 (decision log entry
    237) after the reviewer's FOCUSED PASS (EX_305). This script reads that candidate (asserted by SHA-256),
    changes only the statements the ratification itself made out of date (the title, the status paragraph, where
    the working files lie, and the status of section 8 item 6, which the owner decided in entry 234), each by a
    replacement that must match exactly once, and writes doc/FILE_FORM_STANDARD_v0_1.md and, beside this script,
    the exact difference from the candidate. The candidate is not changed.

Which part of the project's rules it carries out
    H-1 v10 section 8.5 (a ratified text is installed by a script, the status statements changed by counted
    replacements, the exact difference kept); the reviewer's EX_304 and EX_305 (section 8 item 6's status is
    brought up to date at the documentary installation).

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python finalise_rat47.py <repository root>
"""
import difflib
import hashlib
import sys
from pathlib import Path

CANDIDATE = 'exchange/CLAUDE_WEB_TOOLS/standards/FILE_FORM_STANDARD_v0_1r2_CANDIDATE.md'
# The SHA-256 of the candidate the reviewer passed (EX_305) and the owner ratified.
CANDIDATE_SHA = '4f515726bceb31e6d92df422c8b4c0c1e8df349a780430d28bcbf40bd9204f51'
INSTALLED = 'doc/FILE_FORM_STANDARD_v0_1.md'
DIFF = 'exchange/CLAUDE_WEB_TOOLS/rat47/FILE_FORM_STANDARD_v0_1r2_CANDIDATE_TO_FINAL.diff'

# Passages replaced, each occurring exactly once in the candidate.
PASSAGES = [
    ("# The project's standard for the form of its text files (line endings) - v0.1r2 CANDIDATE",
     "# The project's standard for the form of its text files (line endings) - v0.1 (OWNER-RATIFIED, RAT-47, 24 November 2026)"),
    ("**Status:** a CANDIDATE for the\n"
     "reviewer's reading and then the project owner's ratification, as a note of ratification to the specification v0.6,\n"
     "beside the coding practices. The owner has decided its five open points (section 8; decision log entry 231). It is\n"
     "not ratified, changes nothing by itself, and authorises nothing on the owner's PC. Ratified, it replaces the words\n"
     "\"LF pinned\" of decision log entry 181 and the advice in the specification's section 20 on pinning line endings in\n"
     "`.gitattributes`. Made from the draft of the same day (`FILE_FORM_STANDARD_v0_1_DRAFT.md`, kept beside it).\n",
     "**Status: OWNER-RATIFIED on 24 November 2026\n"
     "(RAT-47, decision log entry 237),** as a note of ratification to the specification v0.6, beside the coding\n"
     "practices, after the reviewer's FOCUSED PASS (EX_305) of the exact candidate v0.1r2 (SHA-256\n"
     "`4f515726bceb31e6d92df422c8b4c0c1e8df349a780430d28bcbf40bd9204f51`), of which this is the installed text. The\n"
     "owner decided its open points (section 8; decision log entries 231 and 234). **It changes nothing by itself and\n"
     "authorises nothing on the owner's PC:** the conversion, every install and every run are each his own go. It\n"
     "replaces the words \"LF pinned\" of decision log entry 181 and the advice in the specification's section 20 on\n"
     "pinning line endings in `.gitattributes`. The draft, the candidates, their exact differences, the builders and\n"
     "the trial's evidence are kept in `exchange/CLAUDE_WEB_TOOLS/standards/`; the exact difference from the ratified\n"
     "candidate to this text is `exchange/CLAUDE_WEB_TOOLS/rat47/FILE_FORM_STANDARD_v0_1r2_CANDIDATE_TO_FINAL.diff`.\n"),
    ("what is and is not proved). One point is put to the owner (section 8 item 6). The policy is unchanged.",
     "what is and is not proved). One point was put to the owner (section 8 item 6); he has decided it. The policy is\n"
     "unchanged."),
    ("(EX_303 FFS-C03; for the owner's assent, section 8 item",
     "(EX_303 FFS-C03; the owner assented: section 8 item"),
    ("**Put to the owner, not yet answered (v0.1r1; EX_303 FFS-C03):**\n"
     "\n"
     "6. **`GAIS\\` keeps its own Git rules.** His decision 3 was \"`* -text` for the whole repository\". The root file\n"
     "   cannot govern `GAIS\\`, which has attribute files of its own (section 5), and Claude does not write there.\n"
     "   Recommended: he assents to the statement of section 5 (\"nothing converts anywhere in this project; `GAIS\\`\n"
     "   keeps that other project's own rules\"). The other way is that he himself changes the two attribute files\n"
     "   under `GAIS\\`.\n",
     "**Put to the owner in v0.1r1 (EX_303 FFS-C03), and decided by him on 24 November 2026, 18:59 (decision log entry\n"
     "234):**\n"
     "\n"
     "6. **`GAIS\\` keeps its own Git rules.** His decision 3 was \"`* -text` for the whole repository\". The root file\n"
     "   cannot govern `GAIS\\`, which has attribute files of its own (section 5), and Claude does not write there.\n"
     "   His words: \"ok \"`GAIS\\`\" tree is out of scope as historical subproject, so yes to your recommendation.\" So\n"
     "   the statement of section 5 stands: nothing converts anywhere in this project; `GAIS\\` keeps that other\n"
     "   project's own rules, and nothing under it is changed.\n"),
    ("test-by-test comparison is `TRIAL_CRLF_SUITE_COMPARISON.txt` beside this file).",
     "test-by-test comparison is `exchange/CLAUDE_WEB_TOOLS/standards/TRIAL_CRLF_SUITE_COMPARISON.txt`)."),
]


def main(root: Path) -> int:
    """Install the ratified text and write the exact difference; print both SHA-256; return 0.
    Refuses (assert) if the candidate is not the ratified bytes, a passage is not found exactly once, the
    installed file exists already, or the result is not ASCII."""
    candidate_bytes = (root / CANDIDATE).read_bytes()
    assert hashlib.sha256(candidate_bytes).hexdigest() == CANDIDATE_SHA, 'the candidate is not the ratified bytes'
    old_text = candidate_bytes.decode('ascii')
    new_text = old_text
    for old_piece, new_piece in PASSAGES:
        assert old_text.count(old_piece) == 1, f'not exactly once in the candidate: {old_piece[:70]!r}'
        new_text = new_text.replace(old_piece, new_piece)
    assert 'CANDIDATE for' not in new_text and 'not yet answered' not in new_text, 'a candidate status is left'
    target = root / INSTALLED
    assert not target.exists(), f'{INSTALLED} exists already: nothing is overwritten'
    target.write_bytes(new_text.encode('ascii'))
    difference = ''.join(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                              CANDIDATE, INSTALLED))
    (root / DIFF).write_bytes(difference.encode('ascii'))
    for name in (INSTALLED, DIFF):
        print(hashlib.sha256((root / name).read_bytes()).hexdigest(), name)
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
