"""Write the file-form standard's candidate v0.1r1 from the candidate v0.1, and the exact difference.

What this file is for
    The reviewer's EX_303 asked four focused clarifications of the candidate v0.1 (FFS-C01 to FFS-C04) before the
    owner's ratification. This script applies each change to the text of v0.1 as a replacement that must match
    exactly once (a passage, or a whole line found by its beginning), writes FILE_FORM_STANDARD_v0_1r1_CANDIDATE.md
    beside it and the unified difference, so that the recheck can be made on the difference alone. v0.1 and the
    trial's evidence are not changed.

Which part of the specification it carries out
    None; the standard is to become a note of ratification to the specification v0.6.

Which of the project's own modules it uses
    None.

What uses it
    Claude, in the cloud workspace. Usage:  python make_standard_v0_1r1.py   (run in this folder)
"""
import difflib
import hashlib
import sys
from pathlib import Path

OLD_NAME = 'FILE_FORM_STANDARD_v0_1_CANDIDATE.md'
NEW_NAME = 'FILE_FORM_STANDARD_v0_1r1_CANDIDATE.md'
DIFF_NAME = 'FILE_FORM_STANDARD_v0_1_TO_v0_1r1.diff'
# The SHA-256 of v0.1 as the reviewer checked it in EX_303.
OLD_SHA = '00ec02b005813b88927ae22d2afef9e83f22efae3555d760363174248c236872'

# Whole lines replaced, each found by its beginning (a table row is one long line).
LINES = [
    ("| **The living project** |",
     "| **The living project: the project's own files** | what the project's packages deliver and what the project's programs write, in these places of the repository and of a DEV, QA or PROD tree: the root's own files (launchers, settings, the licence, Git's settings files); `src\\`; `deploy\\`; `tests\\`; the runner's tools; `source_data\\`; `results\\research\\`; `records\\`; `scratch\\` | section 3, without exception |"),
    ("| **Not text** |",
     "| **Not the project's own** | a tree's `.venv\\` (other people's packages: thousands of files in their own forms; the environment's digest and verification of specification 13 govern it, never this standard); `.git\\`; Python's cache folders; whatever a test writes in a temporary folder (some tests make malformed files on purpose) | **never converted, never checked by this standard** |\n"
     "| **Not text, by kind** | `.zip`, `.pdf` and the other kinds section 3 names as binary | no line endings. A file of a text kind is never excused as \"binary\" because of what it holds (section 3B) |"),
    ("| Lock and flag files |",
     "| Lock and flag files | `JOB.lock`, `SNAPSHOT_DUE`, and the like | programs | LF | **CRLF** |\n"
     "| Git's own settings files; project text without an extension | `.gitattributes`, `.gitignore`; `LICENSE` | Claude's packages; the owner | LF | **CRLF** (Git reads both files correctly in this form: tried by Claude with Git 2.43) |"),
    ("| **Hash-chained record lists** |",
     "| **Line-record files** | `*.jsonl`: every variant's forecast list and score list and the OV-1 ledger (hash-chained), and the logs under `records\\` (one record a line; not all of them chained) | programs only; never a person | LF | **LF: the one exception** (below) |"),
]

# Passages replaced, each occurring exactly once.
PASSAGES = [
    ("# The project's standard for the form of its text files (line endings) - v0.1 CANDIDATE",
     "# The project's standard for the form of its text files (line endings) - v0.1r1 CANDIDATE"),
    ("`.gitattributes`. Made from the draft of the same day (`FILE_FORM_STANDARD_v0_1_DRAFT.md`, kept beside it).\n",
     "`.gitattributes`. Made from the draft of the same day (`FILE_FORM_STANDARD_v0_1_DRAFT.md`, kept beside it).\n"
     "**v0.1r1 (24 November 2026):** the four clarifications of the reviewer's EX_303 are made: FFS-C01 (sections 2,\n"
     "6 and 7: what is the project's own, what a tree's own untracked files become, the checker's exact scope);\n"
     "FFS-C02 (sections 3 and 3B: two more kinds, the `.jsonl` wording, what conforming means exactly); FFS-C03\n"
     "(section 5: `GAIS\\`, and commits from the cloud); FFS-C04 (section 7: a second run, undoing, locks, a copy first,\n"
     "what is and is not proved). One point is put to the owner (section 8 item 6). The policy is unchanged. v0.1\n"
     "and the trial's evidence stay as they were; `FILE_FORM_STANDARD_v0_1_TO_v0_1r1.diff` is the exact difference.\n"),
    ("   whether a person or a program wrote it. One kind of file is the exception, by its nature: the hash-chained\n"
     "   record lists (`.jsonl`, section 3). The retired Mode H release machinery is left out by name (section 3A).",
     "   whether a person or a program wrote it. One kind of file is the exception, by its nature: the line-record\n"
     "   files (`.jsonl`, section 3). The retired Mode H release machinery is left out by name (section 3A)."),
    ("3. **Git converts nothing.** What is on disk is what is committed, and what GitHub shows is what the tools hash.",
     "3. **Git converts nothing in this project's part of the repository** (section 5 says exactly where). What is on\n"
     "   disk is what is committed, and what GitHub shows is what the tools hash."),
    ("**The one exception, and why it is not a halfway house.** A line of a `.jsonl` list is the canonical encoding of one\n"
     "record, byte for byte, and that encoding ends in one LF.",
     "**The one exception, and why it is not a halfway house.** Every `.jsonl` file of the project is LF, so that one\n"
     "name has one rule. The reason lies in the lists: a line of a forecast list, a score list or the OV-1 ledger is the\n"
     "canonical encoding of one record, byte for byte, and that\n"
     "encoding ends in one LF."),
    ("## 4. Every program says what it writes\n",
     "## 3B. What \"conforms\" means, exactly (so that every checker gives the same answer)\n"
     "\n"
     "- **A CRLF file:** every line ending in it is CRLF. It holds no LF that does not follow a CR, and no CR that is\n"
     "  not followed by an LF. **An LF file (`.jsonl`):** it holds no CR at all.\n"
     "- **An empty file conforms.** **A last line with no line ending is allowed** and is left as it is: the conversion\n"
     "  changes line endings and never adds or removes one. (Whether a list's last line is torn is the engine's own\n"
     "  check, not this standard's.)\n"
     "- **A file of a text kind must read as UTF-8 and hold no zero byte.** One that does not is REFUSED and named; it is\n"
     "  never passed over as \"binary\". Binary kinds are excused by their kind alone: `.zip`, `.pdf`, images (`.png`,\n"
     "  `.jpg`, `.gif`, `.ico`), and Python's compiled files.\n"
     "- **A file of a kind this table does not name,** found in a place the checker covers, is REFUSED and named: the\n"
     "  table is extended by the owner's recorded decision before such a file is accepted. Nothing is assumed.\n"
     "\n"
     "## 4. Every program says what it writes\n"),
    ("## 5. Git and GitHub: nothing converts\n"
     "\n"
     "- **`.gitattributes` says one thing for the whole repository: `* -text`.** Git then never changes a line ending, in\n"
     "  either direction, on any PC, whatever its own `core.autocrlf` setting is. The existing special lines are no\n"
     "  longer needed.\n",
     "## 5. Git and GitHub: nothing converts\n"
     "\n"
     "- **The root `.gitattributes` says one thing: `* -text`.** Git then never changes a line ending, in either\n"
     "  direction, on any PC, whatever its own `core.autocrlf` setting is. The existing special lines are no longer\n"
     "  needed.\n"
     "- **It does not reach `GAIS\\`, and this standard says so** (EX_303 FFS-C03; for the owner's assent, section 8 item\n"
     "  6). That folder is another project's. It has two attribute files of its own\n"
     "  (`GAIS/OUTLANDISH_01/.gitattributes`, `GAIS/OUTLANDISH_01/OUTLANDISH_WSL/.gitattributes`), which Git obeys for the\n"
     "  paths under them, and the second tells Git to convert that project's `.py`, `.sh`, `.md` and `.bat` files.\n"
     "  Claude never writes under `GAIS\\`. So the true statement is: **Git converts nothing anywhere in this project;\n"
     "  under `GAIS\\` that other project's own rules stay as they are.** The repository holds no other attribute file.\n"),
    ("reports for other hosting products, none authoritative for GitHub). So the rule does not depend on it: **no file\n"
     "  of the living project is edited or created in the browser;** files reach GitHub by a commit from a PC. If one\n"
     "  ever arrives in the wrong form, the project's own checker names it at the next suite run.",
     "reports for other hosting products, none authoritative for GitHub). So the rule does not depend on it: **no file\n"
     "  of the living project is edited or created in the browser.** Files reach GitHub by a commit from the owner's\n"
     "  PC or from Claude's cloud workspace, and either way the commit is checked: the bytes staged for it are in the\n"
     "  standard's form (Git's own listing of the staged bytes is read for this). That is a check of a commit, which\n"
     "  is what Git is for; it is never a check of whether a tree may run. If a file ever arrives in the wrong form,\n"
     "  the project's own checker names it at the next suite run."),
    ("One piece of code, used in three places: a test of the suite (every file of the living project against section 3);\n"
     "`Make_Installable` (nothing in the wrong form can be marked ready, so nothing in the wrong form can be installed);\n"
     "and `Check_Tree` (the same for a tree). It names each file that does not conform and says what to do. A file with\n"
     "mixed endings is a fault of its own kind.",
     "One piece of code, used in three places, each with a scope that is written down (EX_303 FFS-C01). It reads files\n"
     "from the disk; it never asks Git what exists.\n"
     "\n"
     "| Where | Exactly which files it checks |\n"
     "|---|---|\n"
     "| **A test of the suite, in DEV** | every file under `src\\`, `deploy\\` and `tests\\` and the root's own files, by walking those folders; Python's cache folders left out; the six files of section 3A left out by name |\n"
     "| **`Make_Installable`** | exactly the files the marker it is about to write lists (a variant's declaration, its files and helpers; or the manifest, the infrastructure and the install tools). Nothing in the wrong form can be marked ready, so nothing in the wrong form can be installed |\n"
     "| **`Check_Tree`, for a tree** | the files on the tree's list of installed files; its `ENVIRONMENT.ini`; every status file; and what the project's programs have written under `source_data\\`, `results\\research\\` and `records\\`, each by its kind |\n"
     "\n"
     "**Never checked, in any of the three:** a tree's `.venv\\`; `.git\\`; frozen history; `GAIS\\`. It names each file that\n"
     "does not conform, says which rule of section 3B it breaks, and says what to do."),
    ("1. **A conversion list, made in the cloud from the repository:** every file to be converted, with its SHA-256 before\n"
     "   and after.\n"
     "2. **A conversion program** (standard library), run by the owner in DEV from a sheet. For each file it checks the\n"
     "   SHA-256 before, writes the new file under a temporary name and renames it, checks the SHA-256 after, and proves\n"
     "   that the new bytes differ from the old in line endings only. Anything unexpected refuses and changes nothing\n"
     "   more. Run a second time it finds nothing to do.\n",
     "1. **A conversion list, made in the cloud from the repository:** every tracked file to be converted, with its\n"
     "   SHA-256 before and after.\n"
     "2. **A conversion program** (standard library; it never calls Git), run by the owner in DEV from a sheet, on his\n"
     "   own go. **Before it changes anything it walks DEV's own folders itself and prints what it found, by class,**\n"
     "   and he confirms:\n"
     "\n"
     "   | Class | Which files | What happens |\n"
     "   |---|---|---|\n"
     "   | Listed | the files of the conversion list | converted, by the rule below |\n"
     "   | DEV's own settings | `ENVIRONMENT.ini` (made by hand; in no list) | converted by rule: line endings only; its SHA-256 before and after go into the conversion's record |\n"
     "   | Made again, not converted | DEV's research results `results\\research\\`; each variant's `VARIANT_STATUS.ini` in DEV; leftovers in `records\\` | removed on the owner's own go and written afresh by the corrected engine at the fill. A status file holds a check over its own bytes, and DEV's hold nothing but `ACTIVE`; **if one holds a withdrawal or an eligibility draw, the program stops for his decision** |\n"
     "   | Untouched, and proved untouched | the results masters and their ledgers (CRLF already: the SHA-256 of each is the same before and after, and the ledger's record of its master's hash stays true); the updater's grabs and backups under `source_data\\`, whose hashes the ledger records; the Mode H opening records; the old run folders and every other record of the old system; `transitory_data\\`; the six files of section 3A; `.venv\\` | nothing; the program reads the masters and ledgers and shows their hashes unchanged |\n"
     "   | Anything else in those folders | a file of a text kind that is in no class above | named, and the program stops before changing anything |\n"
     "\n"
     "   **The rule for a listed file, which also makes a second run safe** (EX_303 FFS-C04): its SHA-256 equals the\n"
     "   list's \"after\": already converted; checked and passed over. It equals the list's \"before\": it is converted\n"
     "   (the new file written under a temporary name and renamed into place, then hashed again), and the program\n"
     "   proves that the new bytes differ from the old in line endings only. **Any third value is a STOP.** A run that\n"
     "   was interrupted is therefore simply run again; the files are not claimed to change all at once.\n"
     "   **It can be undone from the same list:** asked to undo, it turns each file whose hash is the \"after\" back into\n"
     "   the \"before\".\n"
     "   **While it runs nothing else does:** it holds the tree's job lock and the updater's own lock, so no research job\n"
     "   and no results update can start, and the sheet has the owner close everything else of the project first.\n"
     "   **Before it runs** the owner makes his own copy of the project folder; the ways back are the undo, or that\n"
     "   copy.\n"),
    ("5. **Proof:** the whole suite before and after, in the cloud and on the owner's PC; the comparison of DEV's new fill\n"
     "   with the old system's records once more (it compares scientific content, which no line ending changes); the\n"
     "   checker passing on every file.\n",
     "5. **Proof:** the whole suite before and after, in the cloud and on the owner's PC, its tests of N-1 isolation\n"
     "   among them; the comparison of DEV's new fill with the old system's records once more (it compares scientific\n"
     "   content, which no line ending changes); the checker passing on every file. **A changed line ending is no\n"
     "   licence to change a calculation or to read a later draw:** the conversion's list proves, file by file, that\n"
     "   nothing but line endings changed. **Old lists are not repaired:** DEV's old lists are removed, not edited, and\n"
     "   no digest of an old `.jsonl` line and no sealed record is touched.\n"
     "   **What is proved so far, and what is not:** the cloud's trial (section 9) covers the conversion of the tracked\n"
     "   code only. It did not cover `source_data\\`, the engine's changed writers, the refresh of the owner's working\n"
     "   copy, or Windows. Each of those is tested, in the cloud and then on Windows, before the conversion is called\n"
     "   proved; none of them is needed to ratify the standard itself.\n"),
    ("5. **The six files of the retired release machinery** are left out by name: \"yes to your recommendation ignoring\n"
     "   retired machinery and we should note that in the standard\" (section 3A).\n",
     "5. **The six files of the retired release machinery** are left out by name: \"yes to your recommendation ignoring\n"
     "   retired machinery and we should note that in the standard\" (section 3A).\n"
     "\n"
     "**Put to the owner, not yet answered (v0.1r1; EX_303 FFS-C03):**\n"
     "\n"
     "6. **`GAIS\\` keeps its own Git rules.** His decision 3 was \"`* -text` for the whole repository\". The root file\n"
     "   cannot govern `GAIS\\`, which has attribute files of its own (section 5), and Claude does not write there.\n"
     "   Recommended: he assents to the statement of section 5 (\"nothing converts anywhere in this project; `GAIS\\`\n"
     "   keeps that other project's own rules\"). The other way is that he himself changes the two attribute files\n"
     "   under `GAIS\\`.\n"),
    ("- A list of every program in the living project that writes a file, with the form it writes (section 4's test finds\n"
     "  the writes; 17 are known in old code).\n"
     "- Whether any file of the living project is of a kind the table of section 3 does not name; the checker refuses an\n"
     "  unnamed kind, so that the table is always complete.\n",
     "- A list of every program in the living project that writes a file, with the form it writes (section 4's test finds\n"
     "  the writes; 17 are known in old code).\n"
     "- Whether any file of the living project is of a kind the table of section 3 does not name (section 3B refuses\n"
     "  one); Claude's count of the tracked living files found none beyond the table as it now stands.\n"
     "- What the owner's DEV holds under `source_data\\` and `records\\` that Git does not track (the preflight of section\n"
     "  7 prints it before anything is changed).\n"),
]


def main() -> int:
    """Apply every replacement exactly once and write the new candidate and the difference; return 0.
    Refuses (assert) if v0.1 is not the bytes the reviewer checked, or a line or passage is not found exactly once."""
    here = Path(__file__).resolve().parent
    old_bytes = (here / OLD_NAME).read_bytes()
    assert hashlib.sha256(old_bytes).hexdigest() == OLD_SHA, 'v0.1 is not the bytes the reviewer checked'
    old_text = old_bytes.decode('ascii')
    lines = old_text.split('\n')
    for beginning, new_line in LINES:
        found = [index for index, line in enumerate(lines) if line.startswith(beginning)]
        assert len(found) == 1, f'not exactly one line begins: {beginning!r}'
        lines[found[0]] = new_line
    new_text = '\n'.join(lines)
    for old_piece, new_piece in PASSAGES:
        assert old_text.count(old_piece) == 1, f'not exactly once in v0.1: {old_piece[:70]!r}'
        assert new_text.count(old_piece) == 1, f'not exactly once in the text so far: {old_piece[:70]!r}'
        new_text = new_text.replace(old_piece, new_piece)
    old_lines = set(old_text.split('\n'))
    too_long = [line for line in new_text.split('\n')
                if len(line) > 120 and line not in old_lines and not line.lstrip().startswith(('|', '#'))]
    assert not too_long, f'a new line of prose is longer than 120 characters: {too_long[0][:60]!r}'
    (here / NEW_NAME).write_bytes(new_text.encode('ascii'))
    difference = ''.join(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                              OLD_NAME, NEW_NAME))
    (here / DIFF_NAME).write_bytes(difference.encode('ascii'))
    for name in (OLD_NAME, NEW_NAME, DIFF_NAME):
        print(hashlib.sha256((here / name).read_bytes()).hexdigest(), name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
