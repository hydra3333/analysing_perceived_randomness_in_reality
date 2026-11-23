"""The job lock of a tree, the updater's own lock, the orphan-marker check, and the check that the tree's working
folders are its own.

What this file is for
    Only one job may work in a tree at a time. The job lock is the file records/JOB.lock, made by an exclusive
    create when a job starts and removed when it ends: while the file exists, every other job, install or copy
    refuses. No program ever ends another process, and none removes another's lock: a lock left by a job that
    was killed is removed by the owner by hand, once he has seen that no job of the tree is running. The same
    holds for the results updater's own lock, which this file can also take, so that a withdrawal or a checked
    copy of the results never overlaps a results update. This file also makes the orphan-marker check.
    And it makes one check of place (EX_285 F285-B01): the folders a job writes in, or removes its own unfinished
    files from, must be real folders inside the tree. A folder that is a link or a junction to somewhere else
    refuses the launch before anything is written or deleted, so that no job can touch files outside its tree.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 7.1 (one job lock), 11 (a withdrawal holds
    the job lock and the updater's own lock) and 15; doc/Predictive_Randomness_Deployment_Design_v0_12.md
    sections 2 (records\\JOB.lock) and 9. The process-table rule of section 9 arrives with build step 3.

Which of the project's own modules it uses
    None.

What uses it
    research/research_job.py, research/results_step.py, research/status_file.py and research/withdraw.py, and
    the engine's tests.
"""
from __future__ import annotations

import os
from pathlib import Path

# The tree's control folder and the job lock in it (deployment design section 2).
RECORDS_FOLDER = 'records'
JOB_LOCK_NAME = 'JOB.lock'
# The results updater's own lock, exactly where the reviewed results updater makes its own.
UPDATER_LOCK = 'source_data/.results_master.lock'
# The folders of a tree that a job or a withdrawal writes in (from the tree root, forward slashes). Each must be
# a real folder of the tree, or not exist yet.
WORKING_FOLDERS = ('records', 'records/status_staging', 'source_data', 'results', 'results/research')
# The old system's marker of an unresolved process. Any entry at this path blocks every launch (owner, binding).
ORPHAN_MARKER = 'transitory_data/poc_runs/UNRESOLVED_ORPHAN.json'


class LaunchRefused(RuntimeError):
    """A job may not start now. The message says what was found and what to do."""


def check_no_orphan_marker(tree_root: Path) -> None:
    """Refuse (LaunchRefused) if the orphan marker exists in the tree. Nothing clears or bypasses it but the
    owner's approved manual clearance."""
    marker = Path(tree_root) / ORPHAN_MARKER
    if marker.exists() or marker.is_symlink():
        raise LaunchRefused(f'orphan marker present: {marker}. Every launch is blocked until the owner\'s approved '
                            f'clearance procedure has removed it.')


def is_link(path: Path) -> bool:
    """True if a path is itself a symbolic link or, on Windows, a junction: a name that stands for another
    place. False for an ordinary file or folder and for a path that does not exist."""
    is_junction = getattr(os.path, 'isjunction', None)          # Python 3.12 and later
    return os.path.islink(path) or bool(is_junction and is_junction(path))


def check_real_folder(tree_root: Path, relative: str) -> Path:
    """Check that a folder of a tree is a real folder inside that tree, or does not exist yet.

    tree_root: the tree (its own real path; the settings check has seen to that).
    relative: the folder, from the tree root, with forward slashes, for example 'records/status_staging'.
    Returns the folder's path, for example <tree>/records/status_staging.
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
    the tree or does not exist yet. Made before the job lock is taken, so that even the lock file is never
    created through a link."""
    for relative in WORKING_FOLDERS:
        check_real_folder(tree_root, relative)


class FileLock:
    """A lock that is the existence of one file: made by an exclusive create, removed when the block ends.

    Use it as `with FileLock(path, 'research job', when):`. Refuses (LaunchRefused) if the file already exists.
    """

    def __init__(self, path: Path, purpose: str, when: str):
        """path: the lock file.  purpose: what holds it, for example 'research job'.  when: the time, as text;
        purpose and time are written into the file for whoever finds it."""
        self.path = Path(path)
        self.purpose = purpose
        self.when = when

    def __enter__(self):
        """Take the lock, or refuse if the file exists."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise LaunchRefused(
                f'a process of this tree is running: {self.path} exists. Another job holds it, or an earlier job '
                f'was killed and left it. Wait for the job to finish. If you are sure no job of this tree is '
                f'running, delete that one file by hand and run the command again; nothing ends a job for '
                f'you.') from None
        os.write(descriptor, f'{self.purpose}; started {self.when}; process {os.getpid()}\n'.encode('ascii'))
        os.close(descriptor)
        return self

    def __exit__(self, *exc):
        """Release the lock: remove the file."""
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        return False


def job_lock(tree_root: Path, purpose: str, when: str) -> FileLock:
    """The tree's job lock, for example `with job_lock(tree_root, 'research job', '2026-12-01 20:10'):`."""
    return FileLock(Path(tree_root) / RECORDS_FOLDER / JOB_LOCK_NAME, purpose, when)


def updater_lock(tree_root: Path, purpose: str, when: str) -> FileLock:
    """The results updater's own lock in a tree: while it is held no results update can run there."""
    return FileLock(Path(tree_root) / UPDATER_LOCK, purpose, when)
