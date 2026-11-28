"""The infrastructure's fingerprint: one number that changes when any file of the engine changes.

What this file is for
    The infrastructure is every file under src/ outside the method families, the results updater and the
    reporting part: the engine in src/research, the shared modules in src/methods/_common, the evaluation
    helpers and the command program. (The updater, src/updater, fetches results and computes none: a change to
    it cannot change a forecast or a score, so it does not make everything again; the owner, decision log entry
    356. The reporting part, src/reporting, only prints what is stored, so a change to it makes reports again
    and nothing else; RAT-74, Part B section 3.) Each of the two has a fingerprint of its own, for installing.
    The research job takes one SHA-256 over all of it and keeps it beside the results it computes. When the
    fingerprint of the software in the tree is not the one kept there, everything is made again. Nothing is
    refused on its account.
    The three small files beside a method and Python's own cache files are never part of it.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md sections 4 and 5 step 4, as amended by RAT-74 Part B
    section 3 (doc/Predictive_Randomness_Reporting_Design_And_Specification_Amendment_A1_v0_5.md).

Which of the project's own modules it uses
    research.method_flags   PASSED_OVER_NAMES, read_flag, write_flag
    research.variant_lists  RESEARCH_FOLDER

What uses it
    research/research_job.py, research/science_identity.py, reporting/, deploy/ and the tests.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

from research.method_flags import PASSED_OVER_NAMES, FlagFault, read_flag, write_flag
from research.variant_lists import RESEARCH_FOLDER

# The one folder under src/methods that is infrastructure; every other folder there belongs to the methods.
COMMON_FOLDER = '_common'
# The folders under src/ of the results updater and of the reporting part: not part of the fingerprint.
UPDATER_FOLDER = 'updater'
REPORTING_FOLDER = 'reporting'
# Where the tree keeps the fingerprint its results were made with, under the research folder.
STORED_NAME = 'INFRASTRUCTURE'


def sha256_of_file(path: Path) -> str:
    """The SHA-256 of a file's bytes, as 64 hexadecimal characters."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def infrastructure_files(tree_root: Path) -> list:
    """Every infrastructure file of a tree (the updater's and the reporting part's left out), as paths from
    the tree root with forward slashes, in order; for example ['src/methods/_common/__init__.py', ...,
    'src/research/scoring.py', 'src/research_command.py']."""
    source = Path(tree_root) / 'src'
    found = []
    for current, folders, names in os.walk(source):
        here = Path(current).relative_to(source).parts
        folders[:] = sorted(name for name in folders if name != '__pycache__'
                            and not (here == ('methods',) and name != COMMON_FOLDER)
                            and not (here == () and name in (UPDATER_FOLDER, REPORTING_FOLDER)))
        for name in names:
            if name in PASSED_OVER_NAMES or name.endswith(('.pyc', '.pyo')):
                continue
            found.append((Path(current) / name).relative_to(tree_root).as_posix())
    return sorted(found)


def infrastructure_fingerprint(tree_root: Path) -> str:
    """One SHA-256 over every infrastructure file of a tree: over the lines '<path><TAB><sha256><LF>' in path
    order. For example 'ab12...' (64 hexadecimal characters)."""
    text = ''.join(f'{relative}\t{sha256_of_file(Path(tree_root) / relative)}\n'
                   for relative in infrastructure_files(tree_root))
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def files_of_part(tree_root: Path, part: str) -> list:
    """Every file of one part of a tree that has a fingerprint of its own (src/updater or src/reporting), as paths
    from the tree root with forward slashes, in order; for example ['src/updater/__init__.py',
    'src/updater/results_updater.py']; [] if the part's folder does not exist."""
    folder = Path(tree_root) / 'src' / part
    return sorted(path.relative_to(tree_root).as_posix() for path in folder.rglob('*')
                  if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo'))


def fingerprint_of_files(tree_root: Path, relatives: list) -> str:
    """One SHA-256 over some files of a tree, made as the infrastructure's is: over the lines
    '<path><TAB><sha256><LF>' in the order given."""
    text = ''.join(f'{relative}\t{sha256_of_file(Path(tree_root) / relative)}\n' for relative in relatives)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def updater_files(tree_root: Path) -> list:
    """Every file of a tree's results updater (src/updater), as files_of_part gives them."""
    return files_of_part(tree_root, UPDATER_FOLDER)


def updater_fingerprint(tree_root: Path) -> str:
    """One SHA-256 over every file of a tree's results updater (src/updater). The updater is not part of the
    engine's fingerprint; this one lets an install see whether it differs."""
    return fingerprint_of_files(tree_root, updater_files(tree_root))


def reporting_files(tree_root: Path) -> list:
    """Every file of a tree's reporting part (src/reporting), as files_of_part gives them."""
    return files_of_part(tree_root, REPORTING_FOLDER)


def reporting_fingerprint(tree_root: Path) -> str:
    """One SHA-256 over every file of a tree's reporting part (src/reporting). The reporting part is not part of
    the engine's fingerprint; this one lets an install see whether it differs, and is kept with the reports."""
    return fingerprint_of_files(tree_root, reporting_files(tree_root))


def stored_fingerprint(tree_root: Path) -> str | None:
    """The infrastructure fingerprint the tree's results were made with, or None if none is kept (or the small
    file that keeps it cannot be read)."""
    try:
        return read_flag(Path(tree_root) / RESEARCH_FOLDER / STORED_NAME).get('fingerprint')
    except FlagFault:
        return None


def store_fingerprint(tree_root: Path, fingerprint: str) -> None:
    """Keep the infrastructure fingerprint beside the results that are about to be made with it."""
    folder = Path(tree_root) / RESEARCH_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    write_flag(folder / STORED_NAME, {'fingerprint': fingerprint},
               'Written by the research job: the fingerprint of the engine these results were made with.')
