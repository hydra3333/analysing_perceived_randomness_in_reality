"""Build step 2: the counted edits to files that already exist (the overlay holds only new files).

What this file is for
    The step 2 package adds new files (the overlay folder) and changes a few lines of existing files. Each change
    is listed here as (file, old text, new text) with its reason; the old text must be found exactly once, or the
    new text must already be there (so that the script can be run again on a tree it has already changed).

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3, phase 2 ("new code is added in DEV beside
    the old"); H-1 v9 section 12.3 (a builder from a clean clone).

Which of the project's own modules it uses
    None.

What uses it
    sync_and_test.sh and the package builder. Usage:  python apply_edits.py <tree root>
"""
import sys
from pathlib import Path

# (file, old text, new text, reason)
EDITS = (
    ('tests/test_mhupa_master_versions.py',
     "            'src/methods/_common/walk_forward.py', 'src/results_master_v0_2.py'])        # MHUP-A slice 2: v0.2 (design 7)\n",
     "            'src/methods/_common/walk_forward.py', 'src/research/reader.py',             # build step 2: the new reader\n"
     "            'src/results_master_v0_2.py'])                                                 # MHUP-A slice 2: v0.2 (design 7)\n",
     'the old static test lists every file under src/ that names a results master; the new system\'s reader is one'),
    ('.gitignore',
     None,
     "\n# The research system (RAT-40): the state of one tree, never tracked (owner, decision log entry 177).\n"
     "/ENVIRONMENT.ini\n/results/research/\n/results/research_set_aside/\n/records/\n/scratch/\nVARIANT_STATUS.ini\n",
     'DEV\'s settings file, research results, control files and status files are not tracked by Git'),
)


def main() -> int:
    """Apply every edit to the tree named on the command line; print what was done; return 0."""
    tree = Path(sys.argv[1])
    for path, old, new, reason in EDITS:
        target = tree / path
        text = target.read_text(encoding='utf-8')
        if new in text:
            print(f'already applied: {path}')
            continue
        if old is None:
            text = text + ('' if text.endswith('\n') else '\n') + new
        else:
            assert text.count(old) == 1, f'{path}: the text to replace was found {text.count(old)} times'
            text = text.replace(old, new)
        target.write_text(text, encoding='utf-8')
        print(f'edited: {path} ({reason})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
