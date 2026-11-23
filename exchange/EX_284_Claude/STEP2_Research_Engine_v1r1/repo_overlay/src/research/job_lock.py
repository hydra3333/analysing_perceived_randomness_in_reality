"""The job lock of a tree, the updater's own lock, and the orphan-marker check.

What this file is for
    Only one job may work in a tree at a time. The job lock is the file records/JOB.lock, made by an exclusive
    create when a job starts and removed when it ends: while the file exists, every other job, install or copy
    refuses. No program ever ends another process, and none removes another's lock: a lock left by a job that
    was killed is removed by the owner by hand, once he has seen that no job of the tree is running. The same
    holds for the results updater's own lock, which this file can also take, so that a withdrawal or a checked
    copy of the results never overlaps a results update. This file also makes the orphan-marker check.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 7.1 (one job lock), 11 (a withdrawal holds
    the job lock and the updater's own lock) and 15; doc/Predictive_Randomness_Deployment_Design_v0_12.md
    sections 2 (records\\JOB.lock) and 9. The process-table rule of section 9 arrives with build step 3.

Which of the project's own modules it uses
    None.

What uses it
    research/research_job.py, research/results_step.py and research/withdraw.py, and the engine's tests.
"""
from __future__ import annotations

import os
from pathlib import Path

# The tree's control folder and the job lock in it (deployment design section 2).
RECORDS_FOLDER = 'records'
JOB_LOCK_NAME = 'JOB.lock'
# The results updater's own lock, exactly where the reviewed results updater makes its own.
UPDATER_LOCK = 'source_data/.results_master.lock'
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
