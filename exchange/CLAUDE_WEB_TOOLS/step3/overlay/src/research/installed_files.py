"""The list of installed files of a QA or PROD tree: records/INSTALLED_FILES.json.

What this file is for
    A QA or PROD tree keeps one list of every installed software file with its SHA-256, each installed variant's
    fingerprint, and each variant's status file by name only (a status file's content changes, so its hash is
    not kept). The list is a check against accidents: a research job refuses to run in a tree that does not
    match it, and a file that is not on it is never run. This file works out what a tree's software is now,
    writes and reads the list, and says every way a tree differs from its list. It repairs nothing. DEV keeps
    no such list: its software is its working files.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 4 ("each tree keeps one list of every installed
    software file and its hash");
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 2 (what the list holds), section 8 (the tree and
    its list differ: every launcher refuses, naming the file) and section 9 (nothing else lies under src).

Which of the project's own modules it uses
    research.code_identity     read_manifest, MANIFEST_PATH: the infrastructure's files
    research.variant_folders   find_variants: every installed variant, its hashed files and its fingerprint
    research.job_lock          check_real_folder, is_link: the records folder is a real folder; a link is named
    research.windows_text      windows_lines: the list is a text file, written with every line ending CRLF

What uses it
    deploy/check_tree.py (Check_Tree.bat), the launch guard, the install tools of build step 3, and its tests.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from research import code_identity, variant_folders
from research.job_lock import RECORDS_FOLDER, LaunchRefused, check_real_folder, is_link
from research.windows_text import windows_lines

# Where the list lies in a tree, from the tree root (deployment design section 2).
LIST_PATH = f'{RECORDS_FOLDER}/INSTALLED_FILES.json'
# The word that says what kind of record the file is, so that another JSON file is never taken for it.
LIST_KIND = 'INSTALLED_FILES_V1'
# The list is written whole under this added ending, then renamed into place: never a half-written list.
WRITING_SUFFIX = '.writing'
# The one folder in which nothing but listed files and status files may lie (deployment design section 9).
SOFTWARE_FOLDER = 'src'
# Where the variants lie, from the tree root; a variant's hashed paths are given from this folder.
METHODS_FOLDER = 'src/methods'
# Python's cache folder. The launchers of an installed tree write none, so one under src is named, as a whole.
CACHE_FOLDER_NAME = '__pycache__'
# What the owner is told when a tree differs from its list (deployment design section 8, last row).
WHAT_TO_DO = ('Something changed this tree\'s software outside the project\'s commands. No command repairs it. '
              'The way back is a restore from a backup you choose; in QA, also the QA software replacement from '
              'PROD.')


class InstalledFilesRefused(ValueError):
    """The list cannot be made, written or read. The message says what was found, where, and what to do."""


def software_now(tree_root: Path) -> dict:
    """Work out, from the files on disk, what the list of a tree's software holds now.

    tree_root: the tree's folder.
    Returns the list's content, for example
        {'kind': 'INSTALLED_FILES_V1',
         'files': [{'path': 'deploy/INFRA_MANIFEST.ini', 'sha256': 'ab12...'},
                   {'path': 'src/methods/E_002/RECUR_MEAN_ALL_V1/method.py', 'sha256': 'cd34...'}, ...],
         'variants': [{'family': 'E_002', 'variant': 'RECUR_MEAN_ALL_V1', 'fingerprint': 'ef56...'}, ...],
         'status_files': ['src/methods/E_002/RECUR_MEAN_ALL_V1/VARIANT_STATUS.ini', ...]}
    'files' is the manifest, every infrastructure file it lists, and every variant's declaration, declared files
    and helpers, each once, sorted by path, with paths from the tree root.
    Refuses (InstalledFilesRefused): a manifest the reader refuses, or a variant folder that fails its checks.
    """
    root = Path(tree_root)
    try:
        manifest = code_identity.read_manifest(root)
    except code_identity.ManifestRefused as refusal:
        raise InstalledFilesRefused(str(refusal)) from None
    variants, refused = variant_folders.find_variants(root / METHODS_FOLDER)
    if refused:
        raise InstalledFilesRefused(f'{len(refused)} variant folder(s) of {root} fail their checks, the first: '
                                    f'{refused[0][1]} A list of installed files cannot be made of a tree that '
                                    f'holds one.')
    digest_of = {path: variant_folders.sha256_of_file(root / path)
                 for path in (code_identity.MANIFEST_PATH, *manifest)}
    for variant in variants:
        for path, digest in variant.fingerprint_lines:
            digest_of[f'{METHODS_FOLDER}/{path}'] = digest
    return {'kind': LIST_KIND,
            'files': [{'path': path, 'sha256': digest_of[path]} for path in sorted(digest_of)],
            'variants': [{'family': variant.family, 'variant': variant.variant, 'fingerprint': variant.fingerprint}
                         for variant in variants],
            'status_files': [f'{METHODS_FOLDER}/{variant.family}/{variant.variant}/{variant_folders.STATUS_FILE_NAME}'
                             for variant in variants]}


def list_bytes(content: dict) -> bytes:
    """The exact bytes of the list file: the same content always gives the same bytes.

    content: the list, as software_now gives it.  Returns ASCII JSON, keys sorted, two spaces of indent, every
    line ending CRLF (the file-form standard: a JSON document is a text file), for example
    b'{\\r\\n  "files": [...],\\r\\n  "kind": "INSTALLED_FILES_V1",\\r\\n  ...}\\r\\n'.
    """
    return windows_lines(json.dumps(content, indent=2, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')


def write_list(tree_root: Path, content: dict) -> None:
    """Write a tree's list: the whole file under a temporary name beside it, then one rename.

    tree_root: the tree's folder.  content: the list, as software_now gives it.
    Before the rename the old list (or none) is in place; after it the new one: never a mixture.
    Refuses (InstalledFilesRefused), having written nothing, a records folder that is not a real folder of the
    tree.
    """
    root = Path(tree_root)
    try:
        records = check_real_folder(root, RECORDS_FOLDER)
    except LaunchRefused as refusal:
        raise InstalledFilesRefused(f'{refusal} The list of installed files was not written.') from None
    records.mkdir(parents=True, exist_ok=True)
    target = root / LIST_PATH
    temporary = target.with_name(target.name + WRITING_SUFFIX)
    with open(temporary, 'wb') as handle:
        handle.write(list_bytes(content))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)


def _is_a_hashed_path_list(entries: object) -> bool:
    """True if entries is a list of {'path': text, 'sha256': 64 hexadecimal characters}, as 'files' must be."""
    return isinstance(entries, list) and all(
        isinstance(entry, dict) and set(entry) == {'path', 'sha256'} and isinstance(entry['path'], str)
        and isinstance(entry['sha256'], str) and len(entry['sha256']) == 64 for entry in entries)


def read_list(tree_root: Path) -> dict:
    """Read a tree's list of installed files and check that it is one.

    tree_root: the tree's folder.  Returns the content, as software_now gives it.
    Refuses (InstalledFilesRefused): no list (the tree was not created by Init_Tree, or the file was removed); a
    file that is not JSON; a file that is not of this kind or lacks one of its parts.
    """
    path = Path(tree_root) / LIST_PATH
    if not path.is_file():
        raise InstalledFilesRefused(f'{path}: this tree has no list of installed files. A QA or PROD tree gets one '
                                    f'when Init_Tree.bat creates it. {WHAT_TO_DO}')
    try:
        content = json.loads(path.read_text(encoding='ascii'))
    except (ValueError, UnicodeDecodeError) as error:
        raise InstalledFilesRefused(f'{path}: not readable JSON ({error}). {WHAT_TO_DO}') from None
    well_formed = (isinstance(content, dict) and content.get('kind') == LIST_KIND
                   and set(content) == {'kind', 'files', 'variants', 'status_files'}
                   and _is_a_hashed_path_list(content['files'])
                   and isinstance(content['variants'], list)
                   and all(isinstance(entry, dict) and set(entry) == {'family', 'variant', 'fingerprint'}
                           for entry in content['variants'])
                   and isinstance(content['status_files'], list)
                   and all(isinstance(name, str) for name in content['status_files']))
    if not well_formed:
        raise InstalledFilesRefused(f'{path}: it is not a list of installed files of the kind {LIST_KIND} (a part '
                                    f'is missing or of the wrong shape). {WHAT_TO_DO}')
    return content


def _files_lying_under_src(root: Path) -> tuple:
    """Walk the tree's src folder as it is on disk.

    root: the tree's folder.  Returns (files, others): the paths of the files found, from the tree root with
    forward slashes, and one sentence for each thing that is neither entered nor read: a link, and Python's cache
    folder. For example (['src/research/reader.py', ...], ['src/research/__pycache__: Python\\'s cache folder ...']).
    """
    files, others = [], []
    for current, folders, names in os.walk(root / SOFTWARE_FOLDER):
        def from_root(name: str) -> str:
            return os.path.relpath(os.path.join(current, name), root).replace('\\', '/')
        entered = []
        for name in sorted(folders):
            if is_link(Path(current) / name):
                others.append(f'{from_root(name)}: a link or a junction lies under {SOFTWARE_FOLDER}; nothing behind '
                              f'it was read')
            elif name == CACHE_FOLDER_NAME:
                others.append(f'{from_root(name)}: Python\'s cache folder lies under {SOFTWARE_FOLDER}; the launchers '
                              f'of an installed tree write none, and it is not on the list of installed files')
            else:
                entered.append(name)
        folders[:] = entered
        for name in sorted(names):
            if is_link(Path(current) / name):
                others.append(f'{from_root(name)}: a link lies under {SOFTWARE_FOLDER}; it was not read')
            else:
                files.append(from_root(name))
    return files, others


def differences(tree_root: Path, content: dict) -> list:
    """Every way a tree's software differs from its list of installed files. Nothing is changed.

    tree_root: the tree's folder.  content: the tree's list, as read_list gives it.
    Returns one sentence for each difference, sorted, empty when the tree matches its list; for example
        ['src/methods/_shared/recurrence_gaps_v1.py: its bytes are not the bytes that were installed',
         'src/research/extra.py: it lies under src and is not on the list of installed files'].
    Found: a listed file that is missing or whose SHA-256 differs; and anything under src that is neither a
    listed file nor a listed status file (a link and Python's cache folder among them). A status file is on the
    list by name only, so that it is known to belong under src: its content is not compared, and whether it is
    present and passes its own check is the research job's own check, game by game (specification 3.5).
    """
    root = Path(tree_root)
    found = []
    listed = {entry['path']: entry['sha256'] for entry in content['files']}
    for path, installed_digest in listed.items():
        file = root / path
        if not file.is_file():
            found.append(f'{path}: it is on the list of installed files and is missing')
        elif hashlib.sha256(file.read_bytes()).hexdigest() != installed_digest:
            found.append(f'{path}: its bytes are not the bytes that were installed')
    status_files = set(content['status_files'])
    files, others = _files_lying_under_src(root)
    found.extend(others)
    for path in files:
        if path not in listed and path not in status_files:
            found.append(f'{path}: it lies under {SOFTWARE_FOLDER} and is not on the list of installed files')
    return sorted(found)
