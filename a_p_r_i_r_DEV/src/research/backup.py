"""A backup of a tree: one plain ZIP in the tree's backup folder.

What this file is for
    Everything a tree computes can be made again, so a backup is a convenience and a protection of what cannot:
    the accepted results (source_data), and the state of the software and of the small files beside the methods.
    A backup is one ordinary ZIP file of the whole tree at maximum compression, named with the role, the date
    and time and why it was made, for example PROD_20261201_201012_after_job.zip. Any ZIP program opens it.
    It leaves out the tree's Python environment (.venv, rebuilt by the owner's two scripts; the job log records
    the versions) and the lock file. Nothing is read twice, no digest is kept, and no backup is ever written
    over or deleted by this project.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 7.

Which of the project's own modules it uses
    research.settings      TreeSettings: the tree's folder and its backup folder; ENVIRONMENT_FOLDER
    research.tree_lock     the lock file's place, to leave it out

What uses it
    research/research_job.py (after every job), src/research_command.py (Backup.bat), the tools of deploy/ (before
    every replacement), and the tests.
"""
from __future__ import annotations

import os
import re
import zipfile
from pathlib import Path

from research.settings import ENVIRONMENT_FOLDER, TreeSettings
from research.tree_lock import LOCK_NAME, RECORDS_FOLDER

# The compression of a backup: the ordinary ZIP method every ZIP program reads, at its highest level.
ZIP_METHOD, ZIP_LEVEL = zipfile.ZIP_DEFLATED, 9
# A backup is written under its name plus this ending and renamed when it is whole, so that a file ending .zip
# in the backup folder is always a finished backup.
UNFINISHED_SUFFIX = '.writing'
# Python's own cache folders, which hold nothing the project wrote, are left out as well.
CACHE_FOLDER = '__pycache__'


class BackupFailed(RuntimeError):
    """A backup could not be made. The message says where and why. After a job the job's results stand; before a
    replacement the replacement does not start."""


def backup_name(role: str, moment, why: str) -> str:
    """A backup's file name, for example backup_name('PROD', <1 Dec 2026 20:10:12>, 'after job') is
    'PROD_20261201_201012_after_job.zip'. why: a few words; anything but letters and digits becomes '_'."""
    reason = re.sub(r'[^A-Za-z0-9]+', '_', why).strip('_') or 'backup'
    return f'{role}_{moment.strftime("%Y%m%d_%H%M%S")}_{reason}.zip'


def files_to_back_up(tree_root: Path) -> list:
    """Every file of a tree that goes into a backup, as paths from the tree root with forward slashes, in order:
    all of them but the Python environment, the lock file and Python's caches.

    Raises OSError if any folder of the tree cannot be listed (the tree itself included): a backup that silently
    lacked a folder would look whole, and a replacement would then go ahead on the strength of it."""
    tree_root = Path(tree_root)
    lock = f'{RECORDS_FOLDER}/{LOCK_NAME}'
    found = []

    def not_listed(fault: OSError):
        """os.walk passes over a folder it cannot list unless told otherwise: raise the fault instead."""
        raise fault

    for current, folders, names in os.walk(tree_root, onerror=not_listed):
        at_root = Path(current) == tree_root
        folders[:] = sorted(name for name in folders
                            if name != CACHE_FOLDER and not (at_root and name == ENVIRONMENT_FOLDER))
        for name in names:
            relative = (Path(current) / name).relative_to(tree_root).as_posix()
            if relative != lock:
                found.append(relative)
    return sorted(found)


def make_backup(settings: TreeSettings, why: str, moment) -> Path:
    """Make a backup of a tree now.

    settings: the tree's settings (its folder, and its backup folder, which is made if it does not exist).
    why: a few words for the file's name, for example 'after job' or 'before install'.
    moment: the present time on the PC's clock, for the file's name.
    Returns the backup's path, for example T:\\a_p_r_i_r_backups\\PROD\\PROD_20261201_201012_after_job.zip.
    Raises BackupFailed if the backup folder cannot be made, a folder or a file of the tree cannot be read or
    the ZIP cannot be written; what was begun is removed, so that no half backup is left looking like a whole
    one. A backup of the same name is never written over: the new one is given a number.
    """
    tree_root, folder = settings.tree_root, settings.backup_root
    try:
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / backup_name(settings.role, moment, why)
        number = 1
        while path.exists():
            number += 1
            path = folder / backup_name(settings.role, moment, f'{why} {number}')
        unfinished = path.with_name(path.name + UNFINISHED_SUFFIX)
        try:
            with zipfile.ZipFile(unfinished, 'w', compression=ZIP_METHOD, compresslevel=ZIP_LEVEL) as archive:
                for relative in files_to_back_up(tree_root):
                    archive.write(tree_root / relative, relative)
            os.replace(unfinished, path)
        except BaseException:
            if unfinished.exists():
                unfinished.unlink()
            raise
    except (OSError, zipfile.BadZipFile, ValueError) as fault:
        raise BackupFailed(f'the backup of the {settings.role} tree into {folder} was not made: '
                           f'{type(fault).__name__}: {fault}') from None
    return path
