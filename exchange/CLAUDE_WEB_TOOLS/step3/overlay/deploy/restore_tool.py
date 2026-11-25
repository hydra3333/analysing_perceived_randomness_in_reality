"""The restore tool: put back exactly one chosen backup of a tree, at the path it came from.

What this file is for
    It is the whole of a restore, in ONE file that needs only Python's standard library, so that it runs from an
    unpacked recovery kit with any installed Python when no tree of the project can be used. It checks its own
    kit, verifies the backup in full before anything is touched, refuses while any other Python program runs on
    the PC, renames the old tree aside (nothing is copied or deleted), unpacks the backup into a fresh folder,
    reads the result back, writes one record of what it did, and says whether the restored environment starts.
    It installs nothing, rebuilds nothing, applies no withdrawal and reads nothing from DEV, QA or the tree it
    set aside. No program of this project ends a process: it lists what it found and the owner closes it.

    Because it must stand alone it imports nothing of the project, and the few things it shares with the
    backup's writer (the names of the control files and of the manifest) are written out here again.

Which part of the specification it carries out
    doc/Predictive_Randomness_Deployment_Design_v0_12.md section 12 (restore; the reconciliation after an unzip
    by hand; the one exception for a stale orphan marker), section 11 (the kit checks itself) and section 9 (no
    Python program at all on the PC but the restore tool, read from Windows' process table with the standard
    library; a table that cannot be read refuses); doc/Predictive_Randomness_System_Specification_v0_6.md 14.1.

Which of the project's own modules it uses
    None.

What uses it
    Restore.bat in an unpacked recovery kit; deploy/recovery_kit.py, which puts it into every kit; its tests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

# The kit's own list of its files, and the word that says what kind of record it is (deployment design 11).
KIT_MANIFEST_NAME = 'KIT_MANIFEST.json'
KIT_MANIFEST_KIND = 'KIT_MANIFEST_V1'
# The three files every kit holds beside its manifest; the self-check requires exactly these, each listed once.
KIT_FILES = ('HOW_TO_RESTORE.txt', 'Restore.bat', 'restore_tool.py')
# The last member of every backup ZIP, and its kind (as research/snapshot.py writes it).
SNAPSHOT_MANIFEST_NAME = 'SNAPSHOT_MANIFEST.json'
SNAPSHOT_MANIFEST_KIND = 'SNAPSHOT_MANIFEST_V1'
# Two members of a backup that are not unpacked with the rest: the settings file is written last, so that no
# launcher runs in a tree that is not whole; an orphan marker is never restored as a live marker.
SETTINGS_FILE = 'ENVIRONMENT.ini'
ORPHAN_MARKER = 'transitory_data/poc_runs/UNRESOLVED_ORPHAN.json'
# The roles whose trees are backed up, and so can be restored (DEV has no backup root).
BACKED_UP_ROLES = ('QA', 'PROD')
# What marks a tree in which a restore did not finish; every launcher of the tree refuses while it lies there.
PROGRESS_FILE = 'records/RESTORE_IN_PROGRESS.json'
RECORDS_FOLDER = 'records'
# What is looked for in the old tree, for the record only: {path from the tree root: what it means}.
LOOKED_FOR = {'records/JOB.lock': 'a job lock', 'source_data/.results_master.lock': 'the results updater\'s lock',
              'records/SNAPSHOT_IN_PROGRESS.lock': 'a backup\'s lock',
              'records/INSTALL_IN_PROGRESS.json': 'an unfinished install',
              'records/RERUN_IN_PROGRESS.json': 'an unfinished historical walk-forward rerun',
              'records/RESEED_IN_PROGRESS.json': 'an unfinished research-data reseeding',
              PROGRESS_FILE: 'an unfinished restore', ORPHAN_MARKER: 'AN ORPHAN MARKER'}
# The program names that are Python on Windows: python.exe, pythonw.exe, python3.15.exe, py.exe, pyw.exe.
PYTHON_NAME = re.compile(r'^(python[0-9.]*w?|pyw?)\.exe$', re.IGNORECASE)
# The third-party modules the project's programs import; the restored environment is started once to import them.
THIRD_PARTY_MODULES = ('numpy', 'psutil')
# The sentence the owner types to have a stale orphan marker set aside as evidence (deployment design 12, (d)).
ORPHAN_ACKNOWLEDGEMENT = 'I HAVE RESTARTED THE PC AND NO JOB OF THIS PROJECT IS RUNNING'
CHUNK = 1024 * 1024
# How Windows reports the proper end of its process table (ERROR_NO_MORE_FILES).
ERROR_NO_MORE_FILES = 18
# A ZIP keeps a file's time to two seconds, rounded down: a time read from one may be this much too early.
ZIP_TIME_STEP = 2
# The exit codes: restored; refused before anything was touched; stopped part-way (the same command again).
EXIT_RESTORED, EXIT_REFUSED, EXIT_STOPPED = 0, 2, 1


class RestoreRefused(Exception):
    """The restore cannot be made. The message says what was found and what to do."""


def sha256_of(path: Path) -> str:
    """The SHA-256 of a file's bytes, read a piece at a time."""
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for piece in iter(lambda: handle.read(CHUNK), b''):
            digest.update(piece)
    return digest.hexdigest()


def check_kit(kit_folder: Path) -> dict:
    """The kit's self-check, before anything else: its manifest lists exactly the kit's three files, each once,
    and each is there with those bytes.

    kit_folder: the folder the kit was unpacked into (where this file lies).  Returns the manifest.
    Refuses (RestoreRefused): no manifest, or one that is not a kit's or does not list exactly the three files;
    a file missing or of other bytes. A digest is a check against damage, not a signature.
    """
    path = Path(kit_folder) / KIT_MANIFEST_NAME
    try:
        manifest = json.loads(path.read_text(encoding='ascii'))
        listed = {entry['path']: entry['sha256'] for entry in manifest['files']}
        if manifest['kind'] != KIT_MANIFEST_KIND:
            raise ValueError('another kind of record')
        if sorted(entry['path'] for entry in manifest['files']) != sorted(KIT_FILES):
            raise ValueError(f'it does not list exactly {", ".join(KIT_FILES)}, each once')
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise RestoreRefused(f'{path}: this is not a whole recovery kit ({error}). Unpack the kit\'s ZIP again '
                             f'into an empty folder, or use another kit from the backup root.') from None
    for name, expected in sorted(listed.items()):
        file = Path(kit_folder) / name
        if not file.is_file() or sha256_of(file) != expected:
            raise RestoreRefused(f'{file}: it is missing or is not the file the kit was made with. Unpack the '
                                 f'kit\'s ZIP again into an empty folder, or use another kit.')
    return manifest


def _same_place(one: str, other: str) -> bool:
    """True if two paths name the same place, compared as Windows does (case and slashes set aside)."""
    return os.path.normcase(os.path.abspath(one)) == os.path.normcase(os.path.abspath(other))


def _lies_inside(inner: str, outer: str) -> bool:
    """True if a path lies inside a folder (and is not that folder)."""
    return os.path.normcase(os.path.abspath(inner)).startswith(
        os.path.normcase(os.path.abspath(outer)).rstrip('\\/') + os.sep)


def _is_a_full_real_path(text) -> bool:
    """True if a path of a settings file is one the settings reader of the project would accept: not empty, a full
    path (on Windows with its drive), and its own real path. The folder need not exist."""
    if not text or not Path(text).is_absolute():
        return False
    return os.path.normcase(os.path.realpath(text)) == os.path.normcase(str(Path(text)))


def check_destination(backup: Path, manifest: dict, settings_bytes: bytes) -> None:
    """The one place a backup may be put back: the tree root its manifest names must be the root its own settings
    file names, for the same role; and those settings must be settings every launcher of the project would
    accept (deployment design section 1): the role QA or PROD (no other tree is backed up); the root, the
    environment and the backup root each present, a full path and its own real path; the environment inside the
    tree and the backup root outside it. Everything is read from the backup's own bytes: no folder need exist,
    and the old tree is not asked. Refuses (RestoreRefused) otherwise, before anything is touched."""
    import configparser
    settings = configparser.ConfigParser(interpolation=None)
    try:
        settings.read_string(settings_bytes.decode('utf-8-sig'))
        role, root, environment = (settings.get('environment', key) for key in ('role', 'tree_root', 'venv_dir'))
        backup_root = settings.get('environment', 'backup_root', fallback=None)
    except (configparser.Error, UnicodeDecodeError) as error:
        raise RestoreRefused(f'{backup}: the settings file it holds ({SETTINGS_FILE}) cannot be read as one '
                             f'({type(error).__name__}).') from None
    named = str(manifest.get('tree_root') or '')
    if (not Path(named).is_absolute() or not Path(root).is_absolute() or not _same_place(named, root)
            or manifest.get('role') != role):
        raise RestoreRefused(f'{backup}: its manifest says it is the {manifest.get("role")} tree at "{named}", but the '
                             f'settings file it holds is of the {role} tree at "{root}". A backup is put back only '
                             f'at the path its own settings name; this one is not put back anywhere.')
    if (role not in BACKED_UP_ROLES
            or not all(_is_a_full_real_path(text) for text in (named, root, environment, backup_root))
            or not _lies_inside(environment, root) or _same_place(backup_root, root)
            or _lies_inside(backup_root, root) or _lies_inside(root, backup_root)):
        raise RestoreRefused(f'{backup}: the settings file it holds does not describe a tree of this project that '
                             f'could be run after a restore (its role must be QA or PROD; its tree root, its '
                             f'environment and its backup root must each be given as a full, real path; the '
                             f'environment must lie inside the tree and the backup root outside it). It is not '
                             f'put back anywhere.')


def read_backup(backup: Path) -> dict:
    """Verify a backup in full, before anything is touched, and return its manifest.

    backup: the ZIP.  Returns the manifest with three keys added: 'backup_sha256'; 'manifest_bytes' (the
    manifest's exact bytes in the ZIP); and 'orphan_marker_time' (the time the ZIP keeps for the backup's orphan
    marker, in seconds, or None if it holds none).
    Refuses (RestoreRefused): not a ZIP; the manifest not its last member or not a backup's; a member that the
    list does not name, or a listed file that is missing or of other bytes; a name that would leave the tree; no
    settings file, or one that does not agree with the manifest (check_destination); a ".sha256" file beside the
    backup that does not agree with it.
    """
    backup = Path(backup)
    if not backup.is_file() or backup.name.endswith('.partial'):
        raise RestoreRefused(f'{backup}: there is no such backup. A file ending ".partial" is never a backup.')
    digest = sha256_of(backup)
    beside = Path(str(backup) + '.sha256')
    if beside.is_file() and beside.read_text(encoding='ascii', errors='replace').split()[:1] != [digest]:
        raise RestoreRefused(f'{backup}: it is not the file its ".sha256" was written for. It was damaged or '
                             f'changed; choose another backup.')
    try:
        with zipfile.ZipFile(backup) as archive:
            names = archive.namelist()
            if not names or names[-1] != SNAPSHOT_MANIFEST_NAME or names.count(SNAPSHOT_MANIFEST_NAME) != 1:
                raise RestoreRefused(f'{backup}: its last member is not its manifest; it is not a backup of this '
                                     f'project, or it is damaged.')
            manifest_bytes = archive.read(SNAPSHOT_MANIFEST_NAME)
            manifest = json.loads(manifest_bytes.decode('ascii'))
            if manifest.get('kind') != SNAPSHOT_MANIFEST_KIND:
                raise RestoreRefused(f'{backup}: its manifest is not a backup\'s.')
            listed = {entry['path']: entry['sha256'] for entry in manifest['files']}
            expected = sorted(list(listed) + [folder + '/' for folder in manifest['empty_folders']])
            if sorted(names[:-1]) != expected:
                raise RestoreRefused(f'{backup}: it does not hold exactly the files its manifest lists.')
            for name in expected:
                parts = name.rstrip('/').split('/')
                if name.startswith('/') or ':' in name or '\\' in name or '..' in parts or '' in parts:
                    raise RestoreRefused(f'{backup}: the member "{name}" is not a path inside a tree.')
            for name, wanted in listed.items():
                found = hashlib.sha256()
                with archive.open(name, mode='r') as member:
                    for piece in iter(lambda: member.read(CHUNK), b''):
                        found.update(piece)
                if found.hexdigest() != wanted:
                    raise RestoreRefused(f'{backup}: "{name}" is not the file that was backed up. The backup is '
                                         f'damaged; choose another.')
            if SETTINGS_FILE not in listed:
                raise RestoreRefused(f'{backup}: it holds no {SETTINGS_FILE}. Every backup of a tree holds the '
                                     f'tree\'s settings file; this is not one, and it is not put back anywhere.')
            check_destination(backup, manifest, archive.read(SETTINGS_FILE))
            marker_time = (time.mktime(archive.getinfo(ORPHAN_MARKER).date_time + (0, 0, -1))
                           if ORPHAN_MARKER in listed else None)
    except (zipfile.BadZipFile, OSError, ValueError, KeyError, TypeError, EOFError, zlib.error) as error:
        raise RestoreRefused(f'{backup}: it cannot be read as a backup ({type(error).__name__}: {error}).') from None
    return dict(manifest, backup_sha256=digest, manifest_bytes=manifest_bytes, orphan_marker_time=marker_time)


def check_table_was_read_to_its_end(error_code: int) -> None:
    """Windows ends the reading of its process table by reporting that there are no more entries. Any other
    report means the reading stopped part-way: such a table is refused (RestoreRefused), never taken as whole."""
    if error_code != ERROR_NO_MORE_FILES:
        raise RestoreRefused(f'Windows\' process table could not be read to its end (error {error_code}). A restore '
                             f'is not made on a table that may be incomplete. Run the command again.')


def read_windows_processes() -> list:
    """Windows' process table, read with the standard library: [(process number, parent's number, program name,
    when it started as a number that grows with time, or None if Windows would not say)], for example
    [(4120, 4096, 'python.exe', 133771234567890000)]. Refuses (RestoreRefused) on a system that is not Windows
    and whenever the table cannot be read, or its reading stops before Windows reports its end: a table that
    cannot be read whole is never taken for a quiet PC."""
    if os.name != 'nt':
        raise RestoreRefused('this is not Windows: the process table cannot be read here, and a restore is not '
                             'made without it.')
    import ctypes
    from ctypes import wintypes

    class ProcessEntry(ctypes.Structure):
        _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD), ('th32ProcessID', wintypes.DWORD),
                    ('th32DefaultHeapID', ctypes.c_void_p), ('th32ModuleID', wintypes.DWORD),
                    ('cntThreads', wintypes.DWORD), ('th32ParentProcessID', wintypes.DWORD),
                    ('pcPriClassBase', wintypes.LONG), ('dwFlags', wintypes.DWORD),
                    ('szExeFile', wintypes.WCHAR * 260)]

    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel.Process32FirstW.argtypes = kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    table = kernel.CreateToolhelp32Snapshot(0x00000002, 0)               # TH32CS_SNAPPROCESS: every process
    if table in (None, wintypes.HANDLE(-1).value):
        raise RestoreRefused(f'Windows would not give its process table (error {ctypes.get_last_error()}). A '
                             f'restore is not made without it. Run the command again.')
    found = []
    try:
        entry = ProcessEntry()
        entry.dwSize = ctypes.sizeof(ProcessEntry)
        more = kernel.Process32FirstW(table, ctypes.byref(entry))
        if not more:
            raise RestoreRefused(f'Windows\' process table could not be read (error {ctypes.get_last_error()}).')
        while more:
            started = None
            handle = kernel.OpenProcess(0x1000, False, entry.th32ProcessID)   # PROCESS_QUERY_LIMITED_INFORMATION
            if handle:
                times = [wintypes.FILETIME() for _ in range(4)]
                if kernel.GetProcessTimes(handle, *[ctypes.byref(one) for one in times]):
                    started = (times[0].dwHighDateTime << 32) + times[0].dwLowDateTime
                kernel.CloseHandle(handle)
            found.append((entry.th32ProcessID, entry.th32ParentProcessID, entry.szExeFile, started))
            more = kernel.Process32NextW(table, ctypes.byref(entry))
        ended_with = ctypes.get_last_error()                 # read at once, before any other call to Windows
    finally:
        kernel.CloseHandle(table)
    check_table_was_read_to_its_end(ended_with)
    return found


def other_python_programs(table, own_number: int) -> list:
    """The Python programs in a process table other than this tool.

    table: as read_windows_processes gives it.  own_number: this process's number.
    Returns the (number, parent, name, started) entries whose program name is Python's and that are neither this
    process nor a process above it. A process above is followed only while it did not start after the one below
    it (a number that Windows has given to a newer program is not a parent); so too little may be left out,
    never too much.
    """
    by_number = {entry[0]: entry for entry in table}
    own, current = set(), by_number.get(own_number)
    while current is not None and current[0] not in own:
        own.add(current[0])
        above = by_number.get(current[1])
        if above is None or above[3] is None or current[3] is None or above[3] > current[3]:
            break
        current = above
    return [entry for entry in table if PYTHON_NAME.match(entry[2] or '') and entry[0] not in own]


def check_no_other_python(read_processes, when: str) -> None:
    """Refuse (RestoreRefused) while any Python program but this tool runs on the PC, each one named; or if the
    process table cannot be read, or does not hold this tool's own process (it was then not read whole).
    when: 'before the old tree is renamed' or 'after it', for the message."""
    table = read_processes()
    if os.getpid() not in {entry[0] for entry in table}:
        raise RestoreRefused(f'the process table that was read ({len(table)} entries) does not hold this tool\'s own '
                             f'process: it was not read whole. A restore is not made without it. Run the command '
                             f'again.')
    others = other_python_programs(table, os.getpid())
    if others:
        lines = '\n  '.join(f'process {number} ({name}), started by process {parent}'
                            for number, parent, name, _started in others)
        raise RestoreRefused(f'{len(others)} other Python program(s) are running on this PC ({when}):\n  {lines}\n'
                             f'A restore is made only when none is. Close each one yourself (Claude Code and any '
                             f'editor that runs Python among them); no program of this project ends a process. '
                             f'Then run the same command again.')


def windows_started_at() -> float:
    """When this PC was last started, as a time in seconds; on Windows from the count of milliseconds since."""
    import ctypes
    ctypes.windll.kernel32.GetTickCount64.restype = ctypes.c_uint64
    return time.time() - ctypes.windll.kernel32.GetTickCount64() / 1000.0


def look_at_old_tree(tree_root: Path) -> list:
    """Step 1: what the old tree holds, for the record only. Returns sentences, for example
    ['G:\\\\a_p_r_i_r\\\\records\\\\JOB.lock: a job lock']; ['there was no folder at G:\\\\a_p_r_i_r'] if none."""
    if not os.path.lexists(tree_root):
        return [f'there was no folder at {tree_root}']
    found = []
    for relative, meaning in LOOKED_FOR.items():
        try:
            if os.path.lexists(Path(tree_root) / relative):
                found.append(f'{Path(tree_root) / relative}: {meaning}')
        except OSError as error:
            found.append(f'{Path(tree_root) / relative}: could not be read ({error})')
    return found or [f'{tree_root}: no lock, no unfinished operation and no orphan marker were found in it']


def check_orphan_condition(markers, started_at, read_processes, ask, say) -> None:
    """The one exception for a stale orphan marker (deployment design 12): all four parts, none waived.

    markers: (where it lies, the latest moment it can have been written, in seconds) for each orphan marker
    found: in the old tree, in the backup. A PC started at or before that moment is not shown to have been
    started after the marker.
    started_at: gives when the PC was last started.  read_processes, ask, say: the tool's own.
    Refuses (RestoreRefused): the PC was not started after a marker was written; another Python program runs;
    the owner does not type the fixed sentence.
    """
    say('WARNING: AN ORPHAN MARKER WAS FOUND. It means a job of the old system may have been left running when '
        'it was written. It will not be restored as a live marker: its bytes are kept beside the restore record '
        'as evidence, and the old tree is set aside whole. RESTART THE PC before a restore if you have not done '
        'so since the marker was written.')
    for where, written in markers:
        say(f'  The marker: {where}, written no later than '
            f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(written))}.')
    if any(started_at() <= written for _where, written in markers):
        raise RestoreRefused('this PC has not been restarted since the orphan marker was written. Two ways '
                             'forward: restart the PC and run the same command again; or clear the marker by '
                             'the existing reviewed clearance procedure.')
    check_no_other_python(read_processes, 'the fresh check that the orphan marker asks for')
    if ask(f'Type exactly  {ORPHAN_ACKNOWLEDGEMENT}  to go on; anything else leaves everything as it is: ') \
            != ORPHAN_ACKNOWLEDGEMENT:
        raise RestoreRefused('the sentence was not typed. Nothing was touched.')


def _tree_now(tree_root: Path) -> tuple:
    """Every file under a tree with its SHA-256, and every folder under it: ({path: sha256}, {paths}). A folder
    that cannot be listed raises its OSError: it is never left out of the reading."""
    files, folders = {}, set()

    def stop(error: OSError) -> None:
        raise error

    for current, _folders, names in os.walk(tree_root, onerror=stop):
        relative = os.path.relpath(current, tree_root).replace('\\', '/')
        prefix = '' if relative == '.' else relative + '/'
        if prefix:
            folders.add(relative)
        for name in names:
            files[prefix + name] = sha256_of(Path(current) / name)
    return files, folders


def _write_whole(path: Path, data: bytes) -> None:
    """Write a file's bytes and have the system put them on the disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def _folders_of(files, empty_folders) -> set:
    """The folders a tree must hold for a set of files and of empty folders: each empty folder, and every folder
    above each file and each empty folder; for example {'records', 'src', 'src/research'}."""
    wanted = set()
    for path in list(files) + [folder + '/.' for folder in empty_folders]:
        parts = path.split('/')[:-1]
        wanted.update('/'.join(parts[:count]) for count in range(1, len(parts) + 1))
    return wanted


def unpack(backup: Path, manifest: dict, tree_root: Path, stamp: str, found: list, set_aside,
           old_marker: dict) -> dict:
    """Steps 3 to 6: the fresh folder, the progress file first, every member of the payload but the settings
    file and an orphan marker, the fresh tree read back (its files and its folders, exactly), the restore record
    and the orphan evidence added, the settings file last, the progress file removed.

    found: what was seen in the old tree.  set_aside: where the old tree is now, or None.  old_marker: what was
    read of an orphan marker in the old tree before it was renamed: {'found', 'bytes', 'note'}.
    Returns what the record says of orphan markers (None if there was none anywhere).
    Refuses (RestoreRefused) if the fresh tree is not exactly the payload, or a member held back does not have
    the bytes the manifest lists; the progress file then stays, and the same command again sets the unfinished
    tree aside.
    """
    listed = {entry['path']: entry['sha256'] for entry in manifest['files']}
    held_back = {name for name in (SETTINGS_FILE, ORPHAN_MARKER) if name in listed}
    tree_root.mkdir(parents=True)
    _write_whole(tree_root / PROGRESS_FILE, (json.dumps(
        {'kind': 'RESTORE_IN_PROGRESS_V1', 'backup': backup.name, 'started': stamp}, sort_keys=True) + '\r\n').encode('ascii'))
    held = {}
    with zipfile.ZipFile(backup) as archive:
        for folder in manifest['empty_folders']:
            (tree_root / folder).mkdir(parents=True, exist_ok=True)
        for name in sorted(set(listed) - held_back):
            target = tree_root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name, mode='r') as member, open(target, 'wb') as handle:
                for piece in iter(lambda: member.read(CHUNK), b''):
                    handle.write(piece)
            changed = time.mktime(archive.getinfo(name).date_time + (0, 0, -1))
            os.utime(target, (changed, changed))
        for name in held_back:                               # read once more, so checked once more
            data = archive.read(name)
            if hashlib.sha256(data).hexdigest() != listed[name]:
                raise RestoreRefused(f'"{name}" read from the backup a second time is not the file its manifest '
                                     f'lists. The fresh tree is left marked unfinished.')
            held[name] = (data, time.mktime(archive.getinfo(name).date_time + (0, 0, -1)))
    files, folders = _tree_now(tree_root)
    wanted = {name: digest for name, digest in listed.items() if name not in held_back}
    del files[PROGRESS_FILE]
    if files != wanted or folders != _folders_of(list(wanted) + [PROGRESS_FILE], manifest['empty_folders']):
        wrong = sorted(set(files.items()) ^ set(wanted.items()))[:1]
        raise RestoreRefused(f'the fresh tree at {tree_root} is not exactly what the backup holds '
                             f'({wrong[0][0] if wrong else "its folders are not the backup\'s"}). It is left as it '
                             f'is, marked unfinished. Run the same command again: it sets this attempt aside and '
                             f'begins afresh.')
    name = f'{RECORDS_FOLDER}/RESTORE_{stamp}'
    evidence, orphan = None, None
    if ORPHAN_MARKER in held:
        evidence, evidence_from = held[ORPHAN_MARKER][0], 'the backup'
    elif old_marker['bytes'] is not None:
        evidence, evidence_from = old_marker['bytes'], 'the old tree'
    if ORPHAN_MARKER in held or old_marker['found']:
        orphan = {'in_the_backup': ORPHAN_MARKER in held, 'in_the_old_tree': old_marker['found'],
                  'old_tree_marker_now_at': (str(Path(set_aside) / ORPHAN_MARKER) if old_marker['found'] and set_aside
                                             else None),
                  'old_tree_marker_note': old_marker['note'],
                  'evidence_file': f'{name}_ORPHAN_MARKER.json' if evidence is not None else None,
                  'evidence_is_the_marker_of': evidence_from if evidence is not None else None}
    record = {'kind': 'RESTORE_RECORD_V1', 'restored_at': stamp, 'backup': backup.name,
              'backup_sha256': manifest['backup_sha256'], 'backup_made_utc': manifest.get('made_utc'),
              'role': manifest.get('role'), 'tree_root': str(tree_root), 'files': len(wanted),
              'what_was_found': found, 'set_aside_as': str(set_aside) if set_aside else None,
              'orphan_marker': orphan}
    _write_whole(tree_root / f'{name}.json', (json.dumps(record, indent=1, sort_keys=True).replace('\n', '\r\n')
                                              + '\r\n').encode('ascii'))
    if evidence is not None:
        _write_whole(tree_root / f'{name}_ORPHAN_MARKER.json', evidence)
    settings_bytes, settings_time = held[SETTINGS_FILE]
    _write_whole(tree_root / SETTINGS_FILE, settings_bytes)
    os.utime(tree_root / SETTINGS_FILE, (settings_time, settings_time))
    (tree_root / PROGRESS_FILE).unlink()
    return orphan


def environment_starts(tree_root: Path) -> bool:
    """Step 7: start the restored environment's own Python once and have it import the project's third-party
    modules. True only if it did; anything else is "not ready", never a guess. It waits for that Python for as
    long as it takes: no time limit is set, because a limit would end the process when it ran out, and no
    program of this project ends a process. If it never returns, the owner closes its window himself."""
    folder = Path(tree_root) / '.venv'
    try:                                                 # the tree's own settings say where its environment lies
        import configparser
        settings = configparser.ConfigParser(interpolation=None)
        settings.read(Path(tree_root) / SETTINGS_FILE, encoding='utf-8')
        folder = Path(settings.get('environment', 'venv_dir', fallback=str(folder)))
    except (OSError, configparser.Error):
        pass
    python = folder / 'Scripts' / 'python.exe'
    try:
        done = subprocess.run([str(python), '-I', '-B', '-c', 'import ' + ', '.join(THIRD_PARTY_MODULES)],
                              capture_output=True)
        return done.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def restore(backup: Path, *, kit_folder: Path, read_processes=read_windows_processes, started_at=windows_started_at,
            environment=environment_starts, ask=input, say=print, now=None) -> int:
    """Restore one backup at the path it came from (deployment design section 12).

    backup: the ZIP the owner chose.  kit_folder: the unpacked kit this tool lies in.
    read_processes, started_at, environment: how the process table, the PC's start and the restored environment
    are read (a test passes its own; Windows' are the defaults).  ask, say: the owner's typing and reading.
    now: gives the present time; a test passes a fixed one.
    Returns EXIT_RESTORED, EXIT_REFUSED (nothing was touched) or EXIT_STOPPED (the old tree was set aside and
    the fresh one is unfinished: the same command again).
    """
    now = now or (lambda: datetime.now(timezone.utc))
    stamp = now().astimezone().strftime('%Y%m%d_%H%M%S')
    touched = False
    try:
        say(f'RESTORE - START - {stamp} - the backup {backup}')
        check_kit(kit_folder)
        say('The backup is being read in full before anything is touched; it can take several minutes.')
        manifest = read_backup(Path(backup))
        tree_root = Path(manifest['tree_root'])
        say(f'It is a backup of the {manifest.get("role")} tree at {tree_root}, made {manifest.get("made_local")} '
            f'({len(manifest["files"]):,} files). It will be put back at that path and nowhere else.')
        check_no_other_python(read_processes, 'before the old tree is renamed')
        found = look_at_old_tree(tree_root)
        for line in found:
            say(f'  In the old tree: {line}')
        markers, old_marker = [], {'found': os.path.lexists(tree_root / ORPHAN_MARKER), 'bytes': None, 'note': None}
        if old_marker['found']:
            markers.append((str(tree_root / ORPHAN_MARKER), os.path.getmtime(tree_root / ORPHAN_MARKER)))
            try:                                             # its bytes are read now, before the tree is renamed
                old_marker['bytes'] = (tree_root / ORPHAN_MARKER).read_bytes()
            except OSError as error:
                old_marker['note'] = f'its bytes could not be read ({error}); it lies in the tree set aside'
        if manifest['orphan_marker_time'] is not None:       # a ZIP keeps a time to two seconds, rounded down
            markers.append((f'{ORPHAN_MARKER} inside the backup', manifest['orphan_marker_time'] + ZIP_TIME_STEP))
        if markers:
            check_orphan_condition(markers, started_at, read_processes, ask, say)
        set_aside = None
        if os.path.lexists(tree_root):
            set_aside = Path(f'{tree_root}_SET_ASIDE_{stamp}')
            if os.path.lexists(set_aside):
                raise RestoreRefused(f'{set_aside} exists already. Run the command again.')
            os.rename(tree_root, set_aside)                  # one rename; nothing is copied or deleted
            touched = True
            if (set_aside / SETTINGS_FILE).is_file():        # so that no launcher runs in the tree set aside
                os.rename(set_aside / SETTINGS_FILE, set_aside / (SETTINGS_FILE + '.SET_ASIDE'))
            say(f'The old tree is set aside whole as {set_aside}. Nothing in it was changed but the name of its '
                f'settings file.')
        check_no_other_python(read_processes, 'after the old tree was renamed')
        touched = True
        orphan = unpack(Path(backup), manifest, tree_root, stamp, found, set_aside, old_marker)
        ready = environment(tree_root)
    except RestoreRefused as refusal:
        say(f'REFUSED: {refusal}')
        say('RESTORE - END - ' + ('STOPPED PART-WAY. The old tree is set aside and is whole; the tree at the path is '
                                  'not usable. Put right what is said above and run the same command again.'
                                  if touched else 'refused; nothing was touched.'))
        return EXIT_STOPPED if touched else EXIT_REFUSED
    except OSError as failure:
        say(f'STOPPED: a file or a folder could not be read, written or renamed: {failure}')
        say('RESTORE - END - ' + ('STOPPED PART-WAY. The old tree is set aside and is whole. Run the same command '
                                  'again.' if touched else 'stopped; nothing was touched. Close whatever holds the '
                                  'tree\'s folder (a window, an editor, a command prompt in it) and run the same '
                                  'command again.'))
        return EXIT_STOPPED if touched else EXIT_REFUSED
    say(f'The record of this restore is {tree_root / RECORDS_FOLDER / f"RESTORE_{stamp}.json"}.')
    if orphan is not None:
        say(f'The orphan marker\'s bytes ({orphan["evidence_is_the_marker_of"]}\'s) are kept as evidence in '
            f'{tree_root / orphan["evidence_file"]}; no live marker was restored.' if orphan['evidence_file'] else
            f'WARNING: THE ORPHAN MARKER\'S BYTES COULD NOT BE READ AND ARE NOT KEPT BESIDE THE RECORD. The marker '
            f'lies only in the tree that was set aside: {orphan["old_tree_marker_now_at"]}. Keep that tree.')
    say('RESTORE - END - ' + ('RESTORED AND READY TO RUN.' if ready else 'RESTORED; ENVIRONMENT NOT READY. The '
        'tree\'s files are exactly the backup\'s, but its Python did not start and import what the project needs. '
        'What to do next is your decision.'))
    say('Nothing else was done: nothing was installed, rebuilt or withdrawn. The research job, when you run it, '
        'catches up from what this backup held.')
    return EXIT_RESTORED


def reconcile_after_hand_unzip(backup: Path, *, kit_folder: Path, read_processes=read_windows_processes,
                               say=print, now=None) -> int:
    """After the owner unzipped a backup by hand into an empty folder at the tree's path: check every file and
    every folder, and that the manifest the unzip left at the tree's root is this backup's own; write the
    restore record with its time labelled "reconciliation recorded at"; and move that manifest beside the record.
    An orphan marker the backup held is live and is left so.

    Returns EXIT_RESTORED, or EXIT_REFUSED with nothing changed: the tree is not exactly the backup unzipped;
    another Python program is running; the kit or the backup fails its check; the tree cannot be read.
    """
    now = now or (lambda: datetime.now(timezone.utc))
    stamp = now().astimezone().strftime('%Y%m%d_%H%M%S')
    try:
        say(f'RESTORE, AFTER AN UNZIP BY HAND - START - {stamp} - the backup {backup}')
        check_kit(kit_folder)
        manifest = read_backup(Path(backup))
        tree_root = Path(manifest['tree_root'])
        check_no_other_python(read_processes, 'before the tree is read')
        listed = {entry['path']: entry['sha256'] for entry in manifest['files']}
        try:
            files, folders = _tree_now(tree_root) if tree_root.is_dir() else ({}, set())
            lying = tree_root / SNAPSHOT_MANIFEST_NAME
            its_own = lying.is_file() and lying.read_bytes() == manifest['manifest_bytes']
        except OSError as error:
            raise RestoreRefused(f'the tree at {tree_root} could not be read ({error}). Nothing was changed.') from None
        files.pop(SNAPSHOT_MANIFEST_NAME, None)
        if not its_own or files != listed or folders != _folders_of(listed, manifest['empty_folders']):
            wrong = sorted(set(files.items()) ^ set(listed.items()))[:1]
            what = (wrong[0][0] if wrong else 'its folders are not the backup\'s' if its_own
                    else f'{SNAPSHOT_MANIFEST_NAME} at its root is missing or is not this backup\'s')
            raise RestoreRefused(f'the tree at {tree_root} is not exactly this backup unzipped, with its manifest at '
                                 f'the root ({what}). Nothing was changed.')
        record = {'kind': 'RESTORE_RECORD_V1', 'reconciliation_recorded_at': stamp, 'backup': Path(backup).name,
                  'backup_sha256': manifest['backup_sha256'], 'backup_made_utc': manifest.get('made_utc'),
                  'role': manifest.get('role'), 'tree_root': str(tree_root), 'files': len(listed),
                  'unzipped_by_hand': True, 'orphan_marker_is_live': ORPHAN_MARKER in listed}
        name = f'{RECORDS_FOLDER}/RESTORE_{stamp}'
        _write_whole(tree_root / f'{name}.json', (json.dumps(record, indent=1, sort_keys=True).replace('\n', '\r\n')
                                                  + '\r\n').encode('ascii'))
        os.rename(lying, tree_root / f'{name}_{SNAPSHOT_MANIFEST_NAME}')
    except RestoreRefused as refusal:
        say(f'REFUSED: {refusal}')
        say('RESTORE, AFTER AN UNZIP BY HAND - END - refused; nothing was changed.')
        return EXIT_REFUSED
    say(f'Every file is the backup\'s. The record is {tree_root / (name + ".json")}; the manifest lies beside it.')
    if ORPHAN_MARKER in listed:
        say('WARNING: THE BACKUP HELD AN ORPHAN MARKER. IT IS LIVE AND BLOCKS EVERY LAUNCH, AS ALWAYS.')
    say('RESTORE, AFTER AN UNZIP BY HAND - END - RECONCILED. The environment was not started by this command.')
    return EXIT_RESTORED


def main(arguments=None) -> int:
    """The command line of Restore.bat, from an unpacked kit: --snapshot <zip> [--after-hand-unzip]."""
    parser = argparse.ArgumentParser(prog='Restore.bat', description='Put back exactly one backup of a tree, at '
                                                                     'the path it came from.')
    parser.add_argument('--snapshot', required=True, help='the backup ZIP you chose, with its full path')
    parser.add_argument('--after-hand-unzip', action='store_true',
                        help='you unzipped the backup by hand into an empty folder at the tree\'s path: check it '
                             'and write the record')
    chosen = parser.parse_args(arguments)
    kit_folder = Path(__file__).resolve().parent
    if chosen.after_hand_unzip:
        return reconcile_after_hand_unzip(Path(chosen.snapshot), kit_folder=kit_folder)
    return restore(Path(chosen.snapshot), kit_folder=kit_folder)


if __name__ == '__main__':
    sys.exit(main())
