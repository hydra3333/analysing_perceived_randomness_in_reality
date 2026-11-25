"""A backup of a whole tree: one verified ZIP in the tree's own backup root.

What this file is for
    A backup is one ordinary ZIP of everything under a QA or PROD tree's root, its Python environment included.
    It is written under a name ending ".partial", checked twice (the archive read back against its own list;
    every source file read and hashed a second time, the set of files unchanged), and only then given its name,
    its ".sha256" file and a line in the tree's backup log. The tree must be quiet throughout: the backup's own
    lock file makes every launcher of the tree refuse, no job or results update may hold its lock, and no other
    Python process of the tree may be running before the first reading or after the second. A backup is always
    an attempt: this file returns what happened as a plain result and never stops the work that asked for it.

    It also keeps the tree's note that a backup is owed (records/SNAPSHOT_DUE): a job writes it before its first
    write, and only a verified backup removes it. While it lies there every job says so in capitals, at its
    start and at its end. DEV has no backup root and none of this applies there.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 10 (backups) and section 9 (the process rule of
    a backup, before and after); doc/Predictive_Randomness_System_Specification_v0_6.md section 14.1.

Which of the project's own modules it uses
    research.settings        read_settings, TreeSettings: the tree's role, folder and backup root
    research.job_lock        FileLock, LaunchRefused, is_link, the names of the job's and the updater's locks
    research.process_rule    check_no_other_process_of_tree
    research.installed_files LIST_PATH: the software fingerprint is the SHA-256 of the tree's list
    research.windows_text    windows_lines: the manifest and the ".sha256" file are text, every line ending CRLF

What uses it
    research/research_job.py (the note that a backup is owed; the backup at a job's start if one is owed, and at
    its end); src/research_command.py for Run_Snapshot.bat; the install tools of build step 3; and its tests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from research import installed_files, process_rule
from research.job_lock import JOB_LOCK_NAME, RECORDS_FOLDER, UPDATER_LOCK, FileLock, LaunchRefused, is_link
from research.settings import SettingsRefused, TreeSettings, read_settings
from research.windows_text import windows_lines

# The two control files a backup leaves out, from the tree root (deployment design section 10). Nothing else is.
DUE_PATH = f'{RECORDS_FOLDER}/SNAPSHOT_DUE'
LOCK_PATH = f'{RECORDS_FOLDER}/SNAPSHOT_IN_PROGRESS.lock'
LEFT_OUT = (DUE_PATH, LOCK_PATH)
# The tree's log of backups made: one line a verified backup.
LOG_PATH = f'{RECORDS_FOLDER}/SNAPSHOT_LOG.jsonl'
# The last member of every backup ZIP: the list the archive is checked against, and what a restore reads first.
MANIFEST_NAME = 'SNAPSHOT_MANIFEST.json'
MANIFEST_KIND = 'SNAPSHOT_MANIFEST_V1'
# The names a backup may carry for the work that asked for it (deployment design section 10).
JOBS = ('RESEARCH', 'MANUAL', 'INIT', 'PRE_INSTALL', 'POST_INSTALL', 'PRE_INFRA', 'POST_INFRA', 'PRE_REPLACE',
        'POST_REPLACE', 'RERUN', 'PRE_VERIFY', 'POST_VERIFY', 'PRE_CORRECTION')
# The ending of a backup that is being written. A file with this ending is never a backup.
PARTIAL_SUFFIX = '.partial'
# How much of a file is read at a time, in bytes.
CHUNK = 1024 * 1024
# The exit codes of Run_Snapshot.bat: a verified backup was made; none was made; the command refused.
EXIT_MADE, EXIT_NOT_MADE, EXIT_REFUSED = 0, 1, 2


class BackupNotMade(Exception):
    """A backup could not be made or did not pass its checks. The message says what was found. Raised and caught
    inside this file only: whoever asked for the backup gets a SnapshotResult."""


@dataclass(frozen=True)
class SnapshotResult:
    """What an attempt at a backup came to.

    made: True only for a backup that passed both checks and has its name.  path: the ZIP, or None.
    reason: when not made, why, in a sentence.  files, size, seconds: of a backup that was made.
    """
    made: bool
    path: Path | None = None
    reason: str = ''
    files: int = 0
    size: int = 0
    seconds: float = 0.0

    def line(self) -> str:
        """One line for the owner; for example 'BACKUP MADE AND VERIFIED: T:\\...\\PROD_20261201_201000_RESEARCH.zip
        (11,204 files; 184.2 MB; 96 s).' or 'BACKUP NOT MADE: <why>.'"""
        if self.made:
            return (f'BACKUP MADE AND VERIFIED: {self.path} ({self.files:,} files; {self.size / 1e6:.1f} MB; '
                    f'{self.seconds:.0f} s).')
        return f'BACKUP NOT MADE: {self.reason}'


def is_due(tree_root: Path) -> bool:
    """True while the tree's note that a backup is owed lies in it."""
    return (Path(tree_root) / DUE_PATH).exists()


def mark_due(settings: TreeSettings) -> None:
    """Write the tree's note that a backup is owed, before a job's first write. In DEV nothing is written.
    Only a verified backup removes it."""
    if settings.backup_root is None:
        return
    path = settings.tree_root / DUE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as handle:
        handle.write(windows_lines('This tree has been written to since its last verified backup.\n').encode('ascii'))


def software_fingerprint(tree_root: Path) -> str | None:
    """The fingerprint of a tree's software state: the SHA-256 of its list of installed files, for example
    '5d0c...9a1e'; None for a tree that has no list."""
    path = Path(tree_root) / installed_files.LIST_PATH
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def _inventory(tree_root: Path) -> tuple:
    """Everything under a tree's root but the two control files, as (files, empty folders): paths from the root
    with forward slashes, each sorted; for example (['ENVIRONMENT.ini', 'records/JOB_LOG.txt'], ['scratch']).
    Refuses (BackupNotMade) a link or a junction anywhere in the tree, and a folder that cannot be listed."""
    files, empty = [], []

    def stop(error: OSError) -> None:
        raise BackupNotMade(f'a folder of the tree could not be listed ({error}).')

    for current, folders, names in os.walk(tree_root, onerror=stop):
        relative = os.path.relpath(current, tree_root).replace('\\', '/')
        prefix = '' if relative == '.' else relative + '/'
        for name in folders + names:
            if is_link(os.path.join(current, name)):
                raise BackupNotMade(f'{prefix}{name} is a link or a junction to another place; a backup holds '
                                    f'only what lies in the tree itself. Remove the link (never what it points to).')
        kept = [prefix + name for name in names if prefix + name not in LEFT_OUT]
        files.extend(kept)
        if not folders and not kept and prefix:
            empty.append(relative)
    return sorted(files), sorted(empty)


def _hash_of_file(path: Path) -> str:
    """The SHA-256 of a file's bytes, read a piece at a time."""
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for piece in iter(lambda: handle.read(CHUNK), b''):
            digest.update(piece)
    return digest.hexdigest()


def _write_archive(tree_root: Path, partial: Path, files, empty, heading: dict) -> dict:
    """The first reading: every file hashed and then written into the ZIP by the library's own streaming write
    (which keeps the file's time, to two seconds); every empty folder; and the manifest as the last member. A
    file that changed between its hashing and its writing is caught when the archive is read back.
    Returns {path: sha256}."""
    hashes = {}
    with zipfile.ZipFile(partial, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9,
                         strict_timestamps=False) as archive:                    # a time before 1980 is kept as 1980
        for relative in empty:
            archive.writestr(zipfile.ZipInfo(relative + '/'), b'')
        for relative in files:
            hashes[relative] = _hash_of_file(tree_root / relative)
            archive.write(tree_root / relative, arcname=relative, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        manifest = dict(heading, kind=MANIFEST_KIND, empty_folders=list(empty),
                        files=[{'path': relative, 'sha256': hashes[relative]} for relative in files])
        text = windows_lines(json.dumps(manifest, indent=1, sort_keys=True, ensure_ascii=True) + '\n')
        archive.writestr(zipfile.ZipInfo(MANIFEST_NAME, date_time=time.localtime()[:6]), text.encode('ascii'),
                         compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return hashes


def _check_archive(partial: Path, hashes: dict, empty) -> None:
    """The first verification: the archive read back, every member against the list. Refuses (BackupNotMade) a
    member missing, added or of other bytes, or a manifest that is not the last member."""
    with zipfile.ZipFile(partial) as archive:
        names = archive.namelist()
        if not names or names[-1] != MANIFEST_NAME or names.count(MANIFEST_NAME) != 1:
            raise BackupNotMade('the archive read back does not end with its manifest.')
        if sorted(names[:-1]) != sorted(list(hashes) + [folder + '/' for folder in empty]):
            raise BackupNotMade('the archive read back does not hold exactly the files that were read.')
        for relative, expected in hashes.items():
            digest = hashlib.sha256()
            with archive.open(relative, mode='r') as member:
                for piece in iter(lambda: member.read(CHUNK), b''):
                    digest.update(piece)
            if digest.hexdigest() != expected:
                raise BackupNotMade(f'{relative} read back from the archive is not the file that was read.')


def _check_sources_again(tree_root: Path, hashes: dict, empty) -> None:
    """The second verification, and the second reading: every source file hashed again, the set of files and of
    empty folders unchanged. Refuses (BackupNotMade), naming the first difference: the tree was not quiet."""
    files, empty_now = _inventory(tree_root)
    if files != sorted(hashes) or empty_now != sorted(empty):
        different = sorted(set(files) ^ set(hashes)) + sorted(set(empty_now) ^ set(empty))
        raise BackupNotMade(f'the tree changed while it was being backed up ({different[0]} appeared or went). '
                            f'A backup is made only of a quiet tree.')
    for relative in files:
        if _hash_of_file(tree_root / relative) != hashes[relative]:
            raise BackupNotMade(f'the tree changed while it was being backed up ({relative} has other bytes now). '
                                f'A backup is made only of a quiet tree.')


def _newest_kit(backup_root: Path, fingerprint: str | None) -> str | None:
    """The name of the newest recovery kit in a backup root for a software fingerprint, for example
    'KIT_20261201_101500_5d0c1f3a9b7e.zip'; None if there is none."""
    if fingerprint is None or not backup_root.is_dir():
        return None
    kits = sorted(entry.name for entry in backup_root.iterdir()
                  if entry.name.startswith('KIT_') and entry.name.endswith(f'_{fingerprint[:12]}.zip'))
    return kits[-1] if kits else None


def attempt_snapshot(settings: TreeSettings, job: str, now=None) -> SnapshotResult:
    """Try to make one verified backup of a tree. It never raises for a backup that cannot be made.

    settings: the tree's settings.  job: one of JOBS, the work that asks.  now: gives the present time (UTC); a
    test passes a fixed one.
    Returns a SnapshotResult; its line() is what the owner is told. Not made, with the reason, when: the tree is
    DEV; a job or a results update holds its lock; a backup is already in progress; another Python process of
    the tree is running; a link lies in the tree; a file or the backup root cannot be read or written; the
    archive or the tree fails a check. A ZIP that failed is removed if it can be: a ".partial" is never a backup.
    """
    assert job in JOBS, job
    now = now or (lambda: datetime.now(timezone.utc))
    tree_root, backup_root = settings.tree_root, settings.backup_root
    if backup_root is None:
        return SnapshotResult(False, reason='DEV has no backup root: its backups are Git and your own copy of the '
                                            'project folder.')
    moment = now()
    name = f'{settings.role}_{moment.astimezone().strftime("%Y%m%d_%H%M%S")}_{job}.zip'
    final, partial, began = backup_root / name, backup_root / (name + PARTIAL_SUFFIX), time.monotonic()
    try:
        for held, what in ((f'{RECORDS_FOLDER}/{JOB_LOCK_NAME}', 'a job of this tree holds its lock'),
                           (UPDATER_LOCK, 'a results update holds its lock')):
            if (tree_root / held).exists():
                raise BackupNotMade(f'{what} ({tree_root / held}). A backup is made only of a quiet tree.')
        with FileLock(tree_root / LOCK_PATH, f'backup {name}', moment.astimezone().strftime('%Y-%m-%d %H:%M')):
            try:
                process_rule.check_no_other_process_of_tree(tree_root)
                backup_root.mkdir(parents=True, exist_ok=True)
                if (tree_root / MANIFEST_NAME).exists():
                    raise BackupNotMade(f'{tree_root / MANIFEST_NAME} lies at the tree\'s root: a backup was unzipped '
                                        f'here by hand and not yet checked. Run Restore.bat --after-hand-unzip '
                                        f'--snapshot <that backup> from an unpacked recovery kit first.')
                if final.exists() or partial.exists():
                    raise BackupNotMade(f'{final} or its ".partial" exists already. Run the command again.')
                files, empty = _inventory(tree_root)
                fingerprint = software_fingerprint(tree_root)
                heading = {'made_utc': moment.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                           'made_local': moment.astimezone().strftime('%Y-%m-%d %H:%M:%S'), 'role': settings.role,
                           'tree_root': str(tree_root), 'job': job, 'software_fingerprint': fingerprint,
                           'recovery_kit': _newest_kit(backup_root, fingerprint)}
                hashes = _write_archive(tree_root, partial, files, empty, heading)
                _check_archive(partial, hashes, empty)
                _check_sources_again(tree_root, hashes, empty)
                process_rule.check_no_other_process_of_tree(tree_root)
                archive_digest, size = _hash_of_file(partial), partial.stat().st_size
                os.replace(partial, final)
            except BaseException:
                try:
                    partial.unlink()
                except OSError:
                    pass
                raise
            with open(Path(str(final) + '.sha256'), 'wb') as handle:
                handle.write(windows_lines(f'{archive_digest} *{name}\n').encode('ascii'))
            record = dict(heading, backup=name, sha256=archive_digest, size=size, files=len(files))
            with open(tree_root / LOG_PATH, 'a', encoding='ascii', newline='\n') as stream:
                stream.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + '\n')
            try:
                (tree_root / DUE_PATH).unlink()
            except FileNotFoundError:
                pass
    except (BackupNotMade, LaunchRefused, OSError, zipfile.BadZipFile, zipfile.LargeZipFile) as failure:
        return SnapshotResult(False, reason=f'{failure}')
    return SnapshotResult(True, path=final, files=len(files), size=size, seconds=time.monotonic() - began)


# What every job says, in capitals, while the tree is owed a backup that could not be made (specification 14.1).
STANDING_WARNING = ('WARNING: THIS TREE HAS NO VERIFIED BACKUP OF ITS PRESENT STATE. THE WORK GOES ON. EVERY JOB '
                    'SAYS THIS UNTIL A BACKUP IS MADE: RUN Run_Snapshot.bat WHEN THE TREE IS QUIET, AND READ WHY '
                    'THE LAST ONE FAILED.')


def backup_for_a_job(settings: TreeSettings, moment: str, now, say) -> None:
    """The backup a research job owes, at one of its two moments. In DEV nothing happens and nothing is said.

    moment: 'start' (only if the tree's note says a backup is owed from earlier work, tried before the job takes
    its lock) or 'end' (always, after the job has released its lock).  now, say: the job's own.
    Says the result on one line; if no backup could be made, the standing warning in capitals. Never refuses.
    """
    if settings.backup_root is None or (moment == 'start' and not is_due(settings.tree_root)):
        return
    if moment == 'start':
        say('A backup is owed from earlier work in this tree; it is tried first.')
    result = attempt_snapshot(settings, 'RESEARCH', now)
    say(result.line())
    if not result.made:
        say(STANDING_WARNING)


def main(arguments, tree_root: Path, say=print) -> int:
    """The command line of Run_Snapshot.bat: one backup of the tree it lies in, now, if the tree is quiet.

    arguments: none.  tree_root: the tree the launcher lies in.  Returns the exit code: 0 a verified backup was
    made; 1 none was made (the line says why); 2 the command refused (the settings).
    """
    argparse.ArgumentParser(prog='Run_Snapshot.bat', description='Make one verified backup of this tree '
                                                                 '(specification 14.1).').parse_args(arguments)
    try:
        settings = read_settings(Path(tree_root))
    except SettingsRefused as refusal:
        say(f'REFUSED: {refusal}')
        return EXIT_REFUSED
    say(f'BACKUP - START - the {settings.role} tree at {settings.tree_root}. The whole tree is read twice; it can '
        f'take several minutes.')
    result = attempt_snapshot(settings, 'MANUAL')
    say(result.line())
    say('BACKUP - END')
    return EXIT_MADE if result.made else EXIT_NOT_MADE
