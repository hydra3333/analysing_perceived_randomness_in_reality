"""The one lock of a tree, and the check that a tree's working folders are its own.

What this file is for
    Only one command may work in a tree at a time: a research job, the results updater started by itself, a
    backup, and (from DEV) an install, a retirement, a copy or a restore. The lock is the file
    records/TREE.lock, made by an exclusive create when a command starts and removed when it ends: while the file
    exists, every other command in that tree refuses. No program ever ends another process, and none removes
    another's lock: a lock left by a command that was killed is removed by the owner by hand, once he has seen
    that nothing of the tree is running. The one exception is DEV's Who_Uses, which only reads and prints: it
    makes the first step below but takes no lock.

    A command of DEV that installs into another tree takes that tree's lock and then starts that tree's own
    research job. The job must not take the lock a second time, and must not run under anyone else's: each lock
    file holds a key made for it, the installing command gives the key to the job it starts, and the job works
    only if the lock file is there and holds that key (HeldLock). It leaves the lock for its owner to remove.

    It also gives every command its first step, enter_tree: the settings file is read and the folder is checked
    to be the tree the file says (research/settings.py), and the folders a command writes in must be real
    folders inside the tree. A folder that is a link or a junction to somewhere else refuses the command before
    anything is written or deleted, so that nothing can touch files outside its tree.

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 5 steps 1 and 2, and section 6 (every command
    that touches a tree takes that tree's lock).

Which of the project's own modules it uses
    research.settings          read_settings: the tree's identity
    research.windows_text      windows_lines: the lock file's one line is written with a CRLF ending

What uses it
    src/research_command.py, research/research_job.py, the tools of deploy/, and the tests.
"""
from __future__ import annotations

import os
import secrets
from pathlib import Path

from research.settings import TreeSettings, read_settings
from research.windows_text import windows_lines

# The tree's folder of records (the lock and the job log), and the lock file in it.
RECORDS_FOLDER = 'records'
LOCK_NAME = 'TREE.lock'
# The folders of a tree that its commands write in (from the tree root, forward slashes). Each must be a real
# folder of the tree, or not exist yet.
WORKING_FOLDERS = ('records', 'source_data', 'results', 'results/research')


class LaunchRefused(RuntimeError):
    """A command may not start now. The message says what was found and what to do."""


def is_link(path: Path) -> bool:
    """True if a path is itself a symbolic link or, on Windows, a junction: a name that stands for another
    place. False for an ordinary file or folder and for a path that does not exist."""
    is_junction = getattr(os.path, 'isjunction', None)          # Python 3.12 and later
    return os.path.islink(path) or bool(is_junction and is_junction(path))


def check_real_folder(tree_root: Path, relative: str) -> Path:
    """Check that a folder of a tree is a real folder inside that tree, or does not exist yet.

    tree_root: the tree (its own real path; the settings check has seen to that).
    relative: the folder, from the tree root, with forward slashes, for example 'results/research'.
    Returns the folder's path, for example <tree>/results/research.
    Refuses (LaunchRefused), having written and deleted nothing: the folder or a folder above it inside the tree
    is a link or a junction; the name exists and is not a folder; or the folder's real place is not that path
    inside the tree.
    """
    tree = Path(tree_root)
    parts = relative.split('/')
    folder = tree.joinpath(*parts)
    step = tree
    for name in parts:
        step = step / name
        if is_link(step):
            raise LaunchRefused(f'{step} is a link or a junction to another place, not a real folder of this tree. '
                                f'Nothing was written or deleted. Remove the link (never what it points to) and '
                                f'run the command again.')
    if os.path.lexists(folder):
        real_place = os.path.normcase(os.path.realpath(folder))
        expected = os.path.normcase(os.path.join(os.path.realpath(tree), *parts))
        if not folder.is_dir() or real_place != expected:
            raise LaunchRefused(f'{folder} is not a real folder of this tree (it is a file, or its real place is '
                                f'{os.path.realpath(folder)}). Nothing was written or deleted. Put it right by '
                                f'hand and run the command again.')
    return folder


def check_working_folders(tree_root: Path) -> None:
    """Refuse (LaunchRefused) unless every working folder of the tree (WORKING_FOLDERS) is a real folder inside
    the tree or does not exist yet. Made before the lock is taken, so that even the lock file is never created
    through a link."""
    for relative in WORKING_FOLDERS:
        check_real_folder(tree_root, relative)


class FileLock:
    """A lock that is the existence of one file: made by an exclusive create, removed when the block ends.

    Use it as `with FileLock(path, 'research job', when):`. Refuses (LaunchRefused) if the file already exists.
    key: a few random characters written into the file; a job started under this lock is given them (HeldLock).
    """

    def __init__(self, path: Path, purpose: str, when: str):
        """path: the lock file.  purpose: what holds it, for example 'research job'.  when: the time, as text;
        purpose and time are written into the file for whoever finds it."""
        self.path = Path(path)
        self.purpose = purpose
        self.when = when
        self.key = secrets.token_hex(8)

    def __enter__(self):
        """Take the lock, or refuse if the file exists."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            # O_BINARY (Windows only): without it Windows opens the file in its text mode and writes a carriage
            # return of its own before every line feed, so that the line below would end CR CR LF.
            descriptor = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_BINARY', 0))
        except FileExistsError:
            raise LaunchRefused(
                f'a process of this tree is running: {self.path} exists. Another command holds it, or an earlier one '
                f'was killed and left it. Wait for it to finish. If you are sure nothing of this tree is running, '
                f'delete that one file by hand and run the command again; nothing ends a process for you.') from None
        os.write(descriptor,
                 windows_lines(f'{self.purpose}; started {self.when}; process {os.getpid()}; key {self.key}\n')
                 .encode('ascii'))
        os.close(descriptor)
        return self

    def __exit__(self, *exc):
        """Release the lock: remove the file."""
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        return False


class HeldLock:
    """The tree's lock as a job sees it that was started by the command holding it: the lock file must be there
    and hold the key the job was given. Nothing is made and nothing is removed.

    Use it as `with HeldLock(path, key):`. Refuses (LaunchRefused) if the file is missing or holds another key.
    """

    def __init__(self, path: Path, key: str):
        """path: the lock file.  key: the key the starting command gave, for example '3f9a0c1d2b4e5f60'."""
        self.path = Path(path)
        self.key = key

    def __enter__(self):
        """Check that the lock is there and is the one meant."""
        try:
            words = self.path.read_text(encoding='ascii').split()
        except (OSError, UnicodeDecodeError):
            words = []
        if not self.key or words[-2:] != ['key', self.key]:
            raise LaunchRefused(
                f'this job was started to work under a lock another command holds (--under-lock), but {self.path} '
                f'is not there or is not that command\'s lock. Nothing is done. That option is given only by the '
                f'commands of DEV that install; start an ordinary job with the launcher alone.')
        return self

    def __exit__(self, *exc):
        """Leave the lock where it is: the command that made it removes it."""
        return False


def tree_lock(tree_root: Path, purpose: str, when: str, held_key: str | None = None):
    """The tree's lock, for example `with tree_lock(tree_root, 'research job', '2026-12-01 20:10'):`.

    held_key: None to take the lock; or the key of a lock another command already holds for this job, which is
    then checked and left alone (see HeldLock)."""
    path = Path(tree_root) / RECORDS_FOLDER / LOCK_NAME
    return FileLock(path, purpose, when) if held_key is None else HeldLock(path, held_key)


def enter_tree(tree_folder: Path, must_be: str | None = None) -> TreeSettings:
    """The first step of every command in a tree: read its settings, check that the folder is the tree the file
    says (and, if must_be is given, that it has that role), and check that its working folders are its own.

    tree_folder: the folder the launcher lies in, or another tree's folder.  must_be: None, or the role meant.
    Returns the tree's settings. Refuses (SettingsRefused, LaunchRefused) as read_settings and
    check_working_folders do; nothing has been written when it refuses.
    """
    settings = read_settings(tree_folder, must_be)
    check_working_folders(settings.tree_root)
    return settings
