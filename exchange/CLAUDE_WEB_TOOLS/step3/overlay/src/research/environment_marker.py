"""A tree's own Python environment: its digest over the fixed inventory, and the marker ENVIRONMENT_VERIFIED.json.

What this file is for
    Each tree has its own Python environment (its .venv folder), built by the owner. Before a QA or PROD tree is
    used, Verify_Tree checks it and writes a small marker inside that same folder, holding the environment's
    digest. A launcher of that tree refuses without the marker, and a job compares the digest at its start, so
    that a tree is never run on an environment that changed after it was verified. This file computes the digest,
    and writes, reads and compares the marker. A tree looks only at its own environment and its own marker: no
    tree ever reads another tree's.

    The digest is taken over a fixed inventory (specification section 13): pyvenv.cfg; every file under Scripts;
    every file under Lib/site-packages except Python's cache folders and compiled files; and the base Python's
    version and the bytes of its program file. An environment that lacks one of those three parts, or a folder or
    file of them that cannot be read, is refused: a digest is never given for a part of the inventory. The marker
    lies beside pyvenv.cfg, outside all of these, so writing it changes nothing that is hashed.

    The layout is Windows' own (Scripts, Lib\site-packages), which is where the project runs. The tests give it
    invented folders of that layout; nothing here verifies an environment laid out as Linux lays one out.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 13 ("Verified before use"; "The digest does
    not include its own marker");
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 9 (the marker at every launch as a cheap first
    gate; the digest at the start of a job).

Which of the project's own modules it uses
    research.job_lock        LaunchRefused: a refusal of this file stops a launch like any other
    research.windows_text    windows_lines: the marker is a text file, written with every line ending CRLF

What uses it
    research/launch_guard.py; Verify_Tree and Init_Tree of build step 3, which write the marker; and its tests.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import sys
from pathlib import Path

from research.job_lock import LaunchRefused
from research.windows_text import windows_lines

# The marker's name; it lies directly in the environment's folder, beside pyvenv.cfg (specification 13).
MARKER_NAME = 'ENVIRONMENT_VERIFIED.json'
# The word that says what kind of record the marker is.
MARKER_KIND = 'ENVIRONMENT_VERIFIED_V1'
# The fixed inventory, as names directly in the environment's folder (compared as Windows does, case set aside).
SETTINGS_FILE_OF_AN_ENVIRONMENT = 'pyvenv.cfg'
PROGRAMS_FOLDER = 'Scripts'
PACKAGES_FOLDER = ('Lib', 'site-packages')
# Left out of the inventory under the packages folder: Python's cache folders and its compiled files.
CACHE_FOLDER_NAME = '__pycache__'
COMPILED_SUFFIX = '.pyc'
# What the owner is told when the environment is not the one that was verified.
WHAT_TO_DO = ('If you changed this tree\'s Python environment on purpose, run Verify_Tree.bat in this tree; '
              'otherwise the way back is a restore from a backup you choose.')


class EnvironmentRefused(LaunchRefused):
    """The tree's environment is not verified, or is not the environment that was verified. The message says
    what was found, where, and what to do."""


def base_python() -> tuple:
    """The base Python this environment runs on: its version and its program file, for example
    ('3.13.1 (tags/v3.13.1:0671451, ...) [MSC v.1942 64 bit (AMD64)]', 'C:\\Python313\\python.exe'). On Windows
    the environment's own python.exe starts that program, so it is part of what a forecast was computed with."""
    return sys.version, getattr(sys, '_base_executable', None) or sys.executable


def _inventory(venv_dir: Path) -> list:
    """The files of the fixed inventory, as paths from the environment's folder with forward slashes, sorted; for
    example ['Lib/site-packages/numpy/__init__.py', 'Scripts/python.exe', 'pyvenv.cfg'].
    Refuses (EnvironmentRefused) an environment that lacks one of the three parts, naming each part missing."""
    found, parts_found = [], set()
    for entry in sorted(os.listdir(venv_dir)):
        lowered = entry.lower()
        if lowered == SETTINGS_FILE_OF_AN_ENVIRONMENT and (venv_dir / entry).is_file():
            found.append(entry)
            parts_found.add(SETTINGS_FILE_OF_AN_ENVIRONMENT)
        elif lowered == PROGRAMS_FOLDER.lower() and (venv_dir / entry).is_dir():
            found.extend(_files_below(venv_dir, entry, leave_out_caches=False))
            parts_found.add(PROGRAMS_FOLDER)
        elif lowered == PACKAGES_FOLDER[0].lower() and (venv_dir / entry).is_dir():
            for inner in sorted(os.listdir(venv_dir / entry)):
                if inner.lower() == PACKAGES_FOLDER[1].lower() and (venv_dir / entry / inner).is_dir():
                    found.extend(_files_below(venv_dir, f'{entry}/{inner}', leave_out_caches=True))
                    parts_found.add('/'.join(PACKAGES_FOLDER))
    missing = [part for part in (SETTINGS_FILE_OF_AN_ENVIRONMENT, PROGRAMS_FOLDER, '/'.join(PACKAGES_FOLDER))
               if part not in parts_found]
    if missing:
        raise EnvironmentRefused(f'{venv_dir}: this is not a whole Python environment of this tree: it has no '
                                 f'{" and no ".join(missing)}. Nothing was started. Build it in this tree with '
                                 f'create_venv.bat and install_upgrade_dependencies_into_venv.bat.')
    return sorted(found)


def _stop_at_a_folder_that_cannot_be_read(error: OSError) -> None:
    """What os.walk is given to call when it cannot list a folder: the error goes on to the caller, so that a
    folder that cannot be read refuses the digest instead of being left out of it."""
    raise error


def _files_below(venv_dir: Path, folder: str, leave_out_caches: bool) -> list:
    """Every file under a folder of the environment, as paths from the environment's folder with forward slashes;
    with leave_out_caches, Python's cache folders are not entered and compiled files are passed over. A folder
    that cannot be listed raises its OSError."""
    files = []
    for current, folders, names in os.walk(venv_dir / folder, onerror=_stop_at_a_folder_that_cannot_be_read):
        if leave_out_caches:
            folders[:] = [name for name in folders if name != CACHE_FOLDER_NAME]
        for name in names:
            if leave_out_caches and name.lower().endswith(COMPILED_SUFFIX):
                continue
            files.append(os.path.relpath(os.path.join(current, name), venv_dir).replace('\\', '/'))
    return files


def environment_digest(venv_dir: Path) -> tuple:
    """The digest of a tree's Python environment over the fixed inventory. It reads every file of the inventory,
    which can take minutes when the files have not been read lately; the caller says so before it calls.

    venv_dir: the environment's folder, as the tree's settings name it.
    Returns (digest, files read): 64 hexadecimal characters and a count, for example ('9c1f...e07a', 11998). The
    digest is the SHA-256 of one line a file, '<path><TAB><sha256><LF>', sorted by path, followed by one line for
    the base Python: 'base python<TAB><its version><TAB><its program file><TAB><the sha256 of that file's
    bytes><LF>'. The count is of the files whose bytes were hashed, the base Python's program file among them.
    The same environment under the same base Python gives the same digest; the marker is not in the inventory.
    Refuses (EnvironmentRefused): an environment folder that does not exist; one that lacks pyvenv.cfg, Scripts or
    Lib/site-packages; a folder or a file of the inventory, or the base Python's program file, that cannot be read.
    """
    venv_dir = Path(venv_dir)
    if not venv_dir.is_dir():
        raise EnvironmentRefused(f'{venv_dir}: this tree\'s Python environment folder does not exist. Build it in '
                                 f'this tree with create_venv.bat and install_upgrade_dependencies_into_venv.bat.')
    lines = []
    try:
        paths = _inventory(venv_dir)
        for path in paths:
            lines.append(f'{path}\t{hashlib.sha256((venv_dir / path).read_bytes()).hexdigest()}\n')
        version, program = base_python()
        program_digest = hashlib.sha256(Path(program).read_bytes()).hexdigest()
        lines.append(f'base python\t{version}\t{program}\t{program_digest}\n')
    except OSError as error:
        raise EnvironmentRefused(f'{venv_dir}: a folder or a file of this tree\'s Python environment, or the base '
                                 f'Python\'s program file, could not be read ({error}). Nothing was started. Close '
                                 f'whatever holds it and run the command again.') from None
    return hashlib.sha256(''.join(lines).encode('utf-8')).hexdigest(), len(paths) + 1


def installed_distributions() -> list:
    """The packages installed in the Python that runs this, as sorted 'name version' texts, for example
    ['numpy 2.5.5', 'psutil 7.2.2']. Quick to read: the cheap first gate of every launch compares it with the
    marker's list."""
    return sorted(f'{distribution.metadata["Name"]} {distribution.version}'
                  for distribution in importlib.metadata.distributions())


def marker_bytes(digest: str, distributions) -> bytes:
    """The exact bytes of the marker for a digest and a list of installed packages: ASCII JSON, keys sorted, two
    spaces of indent, every line ending CRLF; for example
    b'{\\r\\n  "digest": "9c1f...",\\r\\n  "distributions": [...],\\r\\n  "kind": "ENVIRONMENT_VERIFIED_V1"\\r\\n}\\r\\n'."""
    content = {'kind': MARKER_KIND, 'digest': digest, 'distributions': list(distributions)}
    return windows_lines(json.dumps(content, indent=2, sort_keys=True, ensure_ascii=True) + '\n').encode('ascii')


def write_marker(venv_dir: Path) -> str:
    """Write the marker for the environment as it is now: the whole file under a temporary name, then one rename.
    Called only by the commands that have just verified the tree (Verify_Tree, Init_Tree).

    venv_dir: the environment's folder.  Returns the digest written.
    Refuses (EnvironmentRefused) whatever environment_digest refuses.
    """
    venv_dir = Path(venv_dir)
    digest, _files_read = environment_digest(venv_dir)
    target = venv_dir / MARKER_NAME
    temporary = target.with_name(target.name + '.writing')
    with open(temporary, 'wb') as handle:
        handle.write(marker_bytes(digest, installed_distributions()))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)
    return digest


def read_marker(venv_dir: Path) -> dict:
    """Read the marker of a tree's environment and check that it is one.

    venv_dir: the environment's folder.  Returns {'kind': ..., 'digest': '9c1f...', 'distributions': [...]}.
    Refuses (EnvironmentRefused): no marker ("environment not verified"); a file that is not JSON or not of this
    kind.
    """
    path = Path(venv_dir) / MARKER_NAME
    if not path.is_file():
        raise EnvironmentRefused(f'{path}: environment not verified. This tree\'s Python environment has no marker: '
                                 f'it was built or changed and not yet checked. Run Verify_Tree.bat in this tree.')
    try:
        content = json.loads(path.read_text(encoding='ascii'))
    except (ValueError, UnicodeDecodeError) as error:
        raise EnvironmentRefused(f'{path}: not readable JSON ({error}). {WHAT_TO_DO}') from None
    if not (isinstance(content, dict) and set(content) == {'kind', 'digest', 'distributions'}
            and content['kind'] == MARKER_KIND and isinstance(content['digest'], str)
            and isinstance(content['distributions'], list)):
        raise EnvironmentRefused(f'{path}: it is not an environment marker of the kind {MARKER_KIND}. {WHAT_TO_DO}')
    return content


def check_marker_lists_what_is_installed(venv_dir: Path) -> None:
    """The cheap first gate of every launch in QA and PROD: the marker is there and lists exactly the packages
    installed now. It reads no file of the inventory.

    Refuses (EnvironmentRefused): whatever read_marker refuses; a package added, removed or of another version
    since the environment was verified, each named.
    """
    marker = read_marker(venv_dir)
    then, now = set(marker['distributions']), set(installed_distributions())
    if then != now:
        changed = sorted(f'no longer installed: {name}' for name in then - now) \
            + sorted(f'installed since: {name}' for name in now - then)
        raise EnvironmentRefused(f'{Path(venv_dir) / MARKER_NAME}: environment not verified. The packages '
                                 f'installed are not those that were verified ({"; ".join(changed)}). {WHAT_TO_DO}')


def check_digest_is_the_markers(venv_dir: Path, digest: str) -> None:
    """At the start of a job in QA and PROD: the environment's digest, computed now, equals the marker's.

    venv_dir: the environment's folder.  digest: environment_digest's result for it, computed in this job.
    Refuses (EnvironmentRefused) when they differ: a file of the environment changed after it was verified.
    """
    marker = read_marker(venv_dir)
    if marker['digest'] != digest:
        raise EnvironmentRefused(f'{Path(venv_dir) / MARKER_NAME}: environment not verified. A file of this tree\'s '
                                 f'Python environment is not as it was when the environment was verified (digest '
                                 f'now {digest}; verified {marker["digest"]}). {WHAT_TO_DO}')
