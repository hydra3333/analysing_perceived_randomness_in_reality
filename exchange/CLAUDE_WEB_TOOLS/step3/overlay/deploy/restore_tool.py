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
from datetime import datetime, timezone
from pathlib import Path

# The kit's own list of its files, and the word that says what kind of record it is (deployment design 11).
KIT_MANIFEST_NAME = 'KIT_MANIFEST.json'
KIT_MANIFEST_KIND = 'KIT_MANIFEST_V1'
# The last member of every backup ZIP, and its kind (as research/snapshot.py writes it).
SNAPSHOT_MANIFEST_NAME = 'SNAPSHOT_MANIFEST.json'
SNAPSHOT_MANIFEST_KIND = 'SNAPSHOT_MANIFEST_V1'
# Two members of a backup that are not unpacked with the rest: the settings file is written last, so that no
# launcher runs in a tree that is not whole; an orphan marker is never restored as a live marker.
SETTINGS_FILE = 'ENVIRONMENT.ini'
ORPHAN_MARKER = 'transitory_data/poc_runs/UNRESOLVED_ORPHAN.json'
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
    """The kit's self-check, before anything else: every file its manifest lists is there with those bytes.

    kit_folder: the folder the kit was unpacked into (where this file lies).  Returns the manifest.
    Refuses (RestoreRefused): no manifest, or one that is not a kit's; a listed file missing or of other bytes.
    A digest is a check against damage, not a signature.
    """
    path = Path(kit_folder) / KIT_MANIFEST_NAME
    try:
        manifest = json.loads(path.read_text(encoding='ascii'))
        listed = {entry['path']: entry['sha256'] for entry in manifest['files']}
        if manifest['kind'] != KIT_MANIFEST_KIND:
            raise ValueError('another kind of record')
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise RestoreRefused(f'{path}: this is not a whole recovery kit ({error}). Unpack the kit\'s ZIP again '
                             f'into an empty folder, or use another kit from the backup root.') from None
    for name, expected in sorted(listed.items()):
        file = Path(kit_folder) / name
        if not file.is_file() or sha256_of(file) != expected:
            raise RestoreRefused(f'{file}: it is missing or is not the file the kit was made with. Unpack the '
                                 f'kit\'s ZIP again into an empty folder, or use another kit.')
    return manifest


def read_backup(backup: Path) -> dict:
    """Verify a backup in full, before anything is touched, and return its manifest.

    backup: the ZIP.  Returns the manifest with two keys added: 'backup_sha256' and 'orphan_marker_time' (when
    the backup's orphan marker was last written, as a time in seconds, or None if it holds none).
    Refuses (RestoreRefused): not a ZIP; the manifest not its last member or not a backup's; a member that the
    list does not name, or a listed file that is missing or of other bytes; a name that would leave the tree; a
    ".sha256" file beside the backup that does not agree with it.
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
            manifest = json.loads(archive.read(SNAPSHOT_MANIFEST_NAME).decode('ascii'))
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
            marker_time = (time.mktime(archive.getinfo(ORPHAN_MARKER).date_time + (0, 0, -1))
                           if ORPHAN_MARKER in listed else None)
    except (zipfile.BadZipFile, OSError, ValueError, KeyError, TypeError) as error:
        raise RestoreRefused(f'{backup}: it cannot be read as a backup ({type(error).__name__}: {error}).') from None
    return dict(manifest, backup_sha256=digest, orphan_marker_time=marker_time)


def read_windows_processes() -> list:
    """Windows' process table, read with the standard library: [(process number, parent's number, program name,
    when it started as a number that grows with time, or None if Windows would not say)], for example
    [(4120, 4096, 'python.exe', 133771234567890000)]. Refuses (RestoreRefused) on a system that is not Windows
    and whenever the table cannot be read: a table that cannot be read is never an empty one."""
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
    finally:
        kernel.CloseHandle(table)
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
    process table cannot be read. when: 'before the old tree is renamed' or 'after it', for the message."""
    others = other_python_programs(read_processes(), os.getpid())
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

    markers: (where it lies, when it was written in seconds) for each orphan marker found: in the old tree, in
    the backup.
    started_at: gives when the PC was last started.  read_processes, ask, say: the tool's own.
    Refuses (RestoreRefused): the PC was not started after a marker was written; another Python program runs;
    the owner does not type the fixed sentence.
    """
    say('WARNING: AN ORPHAN MARKER WAS FOUND. It means a job of the old system may have been left running when '
        'it was written. It will not be restored as a live marker: its bytes are kept beside the restore record '
        'as evidence, and the old tree is set aside whole. RESTART THE PC before a restore if you have not done '
        'so since the marker was written.')
    for where, written in markers:
        say(f'  The marker: {where}, written {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(written))}.')
    if any(started_at() <= written for _where, written in markers):
        raise RestoreRefused('this PC has not been restarted since the orphan marker was written. Two ways '
                             'forward: restart the PC and run the same command again; or clear the marker by '
                             'the existing reviewed clearance procedure.')
    check_no_other_python(read_processes, 'the fresh check that the orphan marker asks for')
    if ask(f'Type exactly  {ORPHAN_ACKNOWLEDGEMENT}  to go on; anything else leaves everything as it is: ') \
            != ORPHAN_ACKNOWLEDGEMENT:
        raise RestoreRefused('the sentence was not typed. Nothing was touched.')


def _tree_now(tree_root: Path) -> tuple:
    """Every file under a tree with its SHA-256, and every empty folder: ({path: sha256}, [paths])."""
    files, empty = {}, []
    for current, folders, names in os.walk(tree_root):
        relative = os.path.relpath(current, tree_root).replace('\\', '/')
        prefix = '' if relative == '.' else relative + '/'
        for name in names:
            files[prefix + name] = sha256_of(Path(current) / name)
        if not folders and not names and prefix:
            empty.append(relative)
    return files, sorted(empty)


def _write_whole(path: Path, data: bytes) -> None:
    """Write a file's bytes and have the system put them on the disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def unpack(backup: Path, manifest: dict, tree_root: Path, stamp: str) -> None:
    """Steps 3 to 6: the fresh folder, the progress file first, every member of the payload but the settings
    file and an orphan marker, the fresh tree read back, the restore record and the orphan evidence added, the
    settings file last, the progress file removed. Refuses (RestoreRefused) if the fresh tree is not exactly
    the payload; the progress file then stays, and the same command again sets the unfinished tree aside."""
    listed = {entry['path']: entry['sha256'] for entry in manifest['files']}
    held_back = {name for name in (SETTINGS_FILE, ORPHAN_MARKER) if name in listed}
    tree_root.mkdir(parents=True)
    _write_whole(tree_root / PROGRESS_FILE, (json.dumps(
        {'kind': 'RESTORE_IN_PROGRESS_V1', 'backup': backup.name, 'started': stamp}, sort_keys=True) + '\r\n').encode('ascii'))
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
        settings_bytes = archive.read(SETTINGS_FILE) if SETTINGS_FILE in listed else None
        orphan_bytes = archive.read(ORPHAN_MARKER) if ORPHAN_MARKER in listed else None
    files, _empty = _tree_now(tree_root)
    wanted = {name: digest for name, digest in listed.items() if name not in held_back}
    del files[PROGRESS_FILE]
    if files != wanted or not all((tree_root / folder).is_dir() for folder in manifest['empty_folders']):
        wrong = sorted(set(files.items()) ^ set(wanted.items()))[:1]
        raise RestoreRefused(f'the fresh tree at {tree_root} is not exactly what the backup holds '
                             f'({wrong[0][0] if wrong else "an empty folder is missing"}). It is left as it is, '
                             f'marked unfinished. Run the same command again: it sets this attempt aside and '
                             f'begins afresh.')
    record = {'kind': 'RESTORE_RECORD_V1', 'restored_at': stamp, 'backup': backup.name,
              'backup_sha256': manifest['backup_sha256'], 'backup_made_utc': manifest.get('made_utc'),
              'role': manifest.get('role'), 'tree_root': str(tree_root), 'files': len(wanted),
              'what_was_found': manifest['what_was_found'], 'set_aside_as': manifest['set_aside_as'],
              'orphan_marker_kept_as_evidence': orphan_bytes is not None}
    name = f'{RECORDS_FOLDER}/RESTORE_{stamp}'
    _write_whole(tree_root / f'{name}.json', (json.dumps(record, indent=1, sort_keys=True).replace('\n', '\r\n')
                                              + '\r\n').encode('ascii'))
    if orphan_bytes is not None:
        _write_whole(tree_root / f'{name}_ORPHAN_MARKER.json', orphan_bytes)
    if settings_bytes is not None:
        _write_whole(tree_root / SETTINGS_FILE, settings_bytes)
    (tree_root / PROGRESS_FILE).unlink()


def environment_starts(tree_root: Path) -> bool:
    """Step 7: start the restored environment's own Python once and have it import the project's third-party
    modules. True only if it did; anything else is "not ready", never a guess."""
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
                              capture_output=True, timeout=300)
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
        markers = []
        if os.path.lexists(tree_root / ORPHAN_MARKER):
            markers.append((str(tree_root / ORPHAN_MARKER), os.path.getmtime(tree_root / ORPHAN_MARKER)))
        if manifest['orphan_marker_time'] is not None:
            markers.append((f'{ORPHAN_MARKER} inside the backup', manifest['orphan_marker_time']))
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
        unpack(Path(backup), dict(manifest, what_was_found=found, set_aside_as=str(set_aside) if set_aside else None),
               tree_root, stamp)
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
    say('RESTORE - END - ' + ('RESTORED AND READY TO RUN.' if ready else 'RESTORED; ENVIRONMENT NOT READY. The '
        'tree\'s files are exactly the backup\'s, but its Python did not start and import what the project needs. '
        'What to do next is your decision.'))
    say('Nothing else was done: nothing was installed, rebuilt or withdrawn. The research job, when you run it, '
        'catches up from what this backup held.')
    return EXIT_RESTORED


def reconcile_after_hand_unzip(backup: Path, *, kit_folder: Path, read_processes=read_windows_processes,
                               say=print, now=None) -> int:
    """After the owner unzipped a backup by hand into an empty folder at the tree's path: check every file, write
    the restore record with its time labelled "reconciliation recorded at", and move the manifest, which the
    unzip left at the tree's root, beside the record. An orphan marker the backup held is live and is left so.

    Returns EXIT_RESTORED, or EXIT_REFUSED with nothing changed: the tree is not exactly the backup's payload
    with its manifest at the root; another Python program is running; the kit or the backup fails its check.
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
        files, _empty = _tree_now(tree_root) if tree_root.is_dir() else ({}, [])
        lying = tree_root / SNAPSHOT_MANIFEST_NAME
        if files.pop(SNAPSHOT_MANIFEST_NAME, None) is None or files != listed:
            wrong = sorted(set(files.items()) ^ set(listed.items()))[:1]
            raise RestoreRefused(f'the tree at {tree_root} is not exactly this backup unzipped, with its manifest at '
                                 f'the root ({wrong[0][0] if wrong else SNAPSHOT_MANIFEST_NAME + " is not there"}). '
                                 f'Nothing was changed.')
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
