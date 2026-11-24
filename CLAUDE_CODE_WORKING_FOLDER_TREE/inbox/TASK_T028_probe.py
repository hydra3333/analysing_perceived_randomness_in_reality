"""TASK_T028 probe: three facts about the owner's Windows PC that build step 3 is designed around.

What it is for. Build step 3 (trees, installs, backups and restore) has three things the cloud workspace cannot tell:
how Windows answers a rename or a replacement when something is open; how long a backup ZIP of a tree with its `.venv`
takes and how large it is; and what a Python program can read of the other processes on the PC, with the standard
library alone and with psutil. This probe measures them and prints what it found. It decides nothing.

Which part of the design it serves: deployment design v0.12 section 9 (the process rules; the restore reads Windows'
process table with the standard library), section 10 (backups: Deflate level 9, every file hashed, read twice),
section 12 (restore: the old tree is renamed aside in one rename) and specification 13 (the environment's digest).

Which of the project's own modules it uses: none. The standard library only; psutil is imported if it is there, for
a comparison, and its absence is reported, not refused.

What uses it: the runner task TASK_T028, in the scratch folder, once. It is not part of the project's software and is
installed nowhere.

What it never does: it ends no process (the helper program it starts ends by itself), contacts nothing, changes no
date or time, and writes only under the work folder given to it. It prints counts, times, sizes, program names and
Windows' answers: never the contents of a file, and never a path under a user's folder.

Use:  python -I -B TASK_T028_probe.py <part> --work <folder> [options]      parts: rename, zip, processes
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path

# How many bytes are read at a time when a file is hashed or compressed. 1 MiB: large enough that the read loop is
# not what is measured, small enough to hold in memory for any file.
READ_CHUNK_BYTES = 1024 * 1024

# How many times the "write a temporary file, then replace the real one" cycle is repeated. Windows can refuse a
# replacement for a moment while another program (a virus scanner, the indexer) holds the file; a thousand cycles
# is enough to see whether that occurs on this PC, and takes seconds.
REPLACE_CYCLES = 1000

# The size of the small file written in each replace cycle: about the size of one of the project's status files.
REPLACE_FILE_BYTES = 1024

# How long this probe waits for its helper program to say it is ready, and how long the helper waits before it ends
# by itself if it is never told to stop. The helper must always end by itself: no program of this project ends
# another process.
HELPER_READY_SECONDS = 30
HELPER_LIFETIME_SECONDS = 120

# The two Deflate levels compared. 9 is the level the deployment design fixes for backups; 6 is zlib's default,
# measured only so that the cost of level 9 is known.
DESIGN_DEFLATE_LEVEL = 9
COMPARISON_DEFLATE_LEVEL = 6

# The ZIP part refuses to start unless the work drive has this many times the bytes it is about to read free, because
# it writes two ZIPs and neither is removed by this probe.
FREE_SPACE_FACTOR = 3

# A ZIP cannot hold a file time before this year; a file older than that is counted, and its time in the ZIP is
# set to the start of this year.
EARLIEST_ZIP_YEAR = 1980

# Windows marks a link, a junction or another reparse point with this file attribute bit.
FILE_ATTRIBUTE_REPARSE_POINT = 0x400

# The helper program: it holds one file open for reading, says it is ready by creating a file, and ends by itself
# when the stop file appears or its lifetime is over, whichever is first. Arguments: the file to hold open, the
# ready file, the stop file, the lifetime in seconds.
HELPER_PROGRAM = (
    "import os, sys, time\n"
    "held_open = open(sys.argv[1], 'rb')\n"
    "open(sys.argv[2], 'w').close()\n"
    "end_at = time.monotonic() + float(sys.argv[4])\n"
    "while not os.path.exists(sys.argv[3]) and time.monotonic() < end_at:\n"
    "    time.sleep(0.1)\n"
    "held_open.close()\n"
)

# A path under a user's folder is never printed: the user's name is a personal detail.
USER_FOLDER_PATTERN = re.compile(r'(?i)([A-Z]:[\\/]+Users[\\/]+)[^\\/\'"]+')


# Plain words for the kinds of "no" the operating system gives; the number printed beside them is the exact answer.
REFUSAL_KINDS = {'PermissionError': 'permission refused', 'FileExistsError': 'the name exists already',
                 'FileNotFoundError': 'not found', 'OSError': 'refused'}


class ProbeRefused(Exception):
    """The probe cannot go on, for a reason its message gives in full."""


def say(line: str) -> None:
    """Print one line of findings at once (so that nothing is lost if a later step fails).
    line: the text. Returns nothing. Never refuses."""
    print(safe_text(line), flush=True)


def safe_text(text: str) -> str:
    """Return the text with the name of any user's folder replaced.
    text: any text, for example an exception's message.
    Returns: the same text, for example 'C:\\Users\\[withheld]\\x.txt' for a path under a user's folder. Never refuses."""
    return USER_FOLDER_PATTERN.sub(lambda found: found.group(1) + '[withheld]', text)


def describe_exception(error: BaseException) -> str:
    """Say what kind of answer an operating-system exception is, without its file names. The words are chosen so
    that a line of findings never looks like a failure of the probe: the answer "no" is what is being measured.
    error: the exception caught.
    Returns: for example 'permission refused, Windows code 32' or 'the name exists already, code 17'. Never refuses."""
    kind = REFUSAL_KINDS.get(type(error).__name__, type(error).__name__.replace('Error', ''))
    windows_code = getattr(error, 'winerror', None)
    if windows_code is not None:
        return f'{kind}, Windows code {windows_code}'
    error_number = getattr(error, 'errno', None)
    if error_number is not None:
        return f'{kind}, code {error_number}'
    return kind


def attempt(action) -> str:
    """Try one file operation and say how Windows answered.
    action: a function of no arguments that does the operation.
    Returns: 'DONE', or for example 'WINDOWS SAID NO (permission refused, Windows code 32)'. An exception that is not an
    operating-system refusal is not caught: it is a fault of this probe and stops it."""
    try:
        action()
    except OSError as error:
        return f'WINDOWS SAID NO ({describe_exception(error)})'
    return 'DONE'


def fresh_folder(folder: Path) -> Path:
    """Create a folder that must not exist yet, so that a second run never mixes with a first.
    folder: the full path. Returns: the same path. Refuses if it is there already."""
    if os.path.lexists(folder):
        raise ProbeRefused(f'{folder} is there already. This probe part has run before in this work folder; it is '
                           f'not run twice. Give it a new, empty work folder.')
    folder.mkdir(parents=True)
    return folder


class WaitingHelper:
    """The helper program: a second Python process that holds a file open and sits in a folder until told to stop."""

    def __init__(self, working_folder: Path, file_to_hold_open: Path, flag_folder: Path) -> None:
        """Start the helper and wait until it says it is ready.
        working_folder: the helper's working folder. file_to_hold_open: a file it opens for reading and keeps open.
        flag_folder: where its ready file and stop file are written (outside the folders under test).
        Refuses if the helper is not ready in HELPER_READY_SECONDS."""
        self.ready_file = flag_folder / 'helper_is_ready.flag'
        self.stop_file = flag_folder / 'helper_may_stop.flag'
        self.process = subprocess.Popen(
            [sys.executable, '-I', '-c', HELPER_PROGRAM, str(file_to_hold_open), str(self.ready_file),
             str(self.stop_file), str(HELPER_LIFETIME_SECONDS)],
            cwd=str(working_folder), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        wait_until = time.monotonic() + HELPER_READY_SECONDS
        while not self.ready_file.exists():
            if self.process.poll() is not None or time.monotonic() > wait_until:
                raise ProbeRefused(f'the helper program did not become ready within {HELPER_READY_SECONDS} seconds '
                                   f'(its exit code so far: {self.process.poll()}). Nothing was measured with it. '
                                   f'It ends by itself within {HELPER_LIFETIME_SECONDS} seconds.')
            time.sleep(0.1)

    def let_it_end(self) -> int:
        """Tell the helper it may stop and wait for it to end by itself. It is never ended by this probe.
        Returns: its exit code, for example 0. Refuses if it has not ended after its whole lifetime."""
        self.stop_file.write_text('stop\n', encoding='ascii')
        try:
            return self.process.wait(timeout=HELPER_LIFETIME_SECONDS + 30)
        except subprocess.TimeoutExpired:
            raise ProbeRefused('the helper program has not ended by itself. It is NOT ended by this probe. Look for '
                               'a python.exe in Task Manager; the owner decides what to do.') from None


# ---------------------------------------------------------------------------------------------------------------
# Part "rename": how Windows answers a rename, a replacement and a removal when something is open
# ---------------------------------------------------------------------------------------------------------------

def replace_cycles(folder: Path, flush_to_disk: bool) -> tuple[int, dict[str, int], float]:
    """Write a small temporary file and replace the real file with it, REPLACE_CYCLES times.
    folder: an empty folder to work in. flush_to_disk: whether each temporary file is forced to the disk (os.fsync)
    before the replacement, as a careful writer does.
    Returns: (cycles that worked, refusals counted by kind, seconds), for example (1000, {}, 1.84) or
    (998, {'permission refused, Windows code 5': 2}, 2.10). Never refuses."""
    real_file = folder / 'status.json'
    temporary_file = folder / 'status.json.tmp'
    content = (b'{"probe": "replace cycle"}\n' * 64)[:REPLACE_FILE_BYTES]
    real_file.write_bytes(content)
    cycles_done = 0
    refusals: dict[str, int] = {}
    started = time.perf_counter()
    for _ in range(REPLACE_CYCLES):
        try:
            with open(temporary_file, 'wb') as handle:
                handle.write(content)
                if flush_to_disk:
                    handle.flush()
                    os.fsync(handle.fileno())
            os.replace(temporary_file, real_file)
            cycles_done += 1
        except OSError as error:
            kind = describe_exception(error)
            refusals[kind] = refusals.get(kind, 0) + 1
    return cycles_done, refusals, time.perf_counter() - started


def part_rename(work_folder: Path) -> None:
    """Measure and print how Windows answers renames, replacements and removals when something is open.
    work_folder: this task's scratch folder; the part works in its own new subfolder 'rename_part'.
    Returns nothing. Refuses if the subfolder is there already or the helper program does not start."""
    part_folder = fresh_folder(work_folder / 'rename_part')
    say(f'R00 this part works in {part_folder}')

    # R1: the plain case the restore relies on: a folder with files in it, nothing open, one rename.
    plain_folder = part_folder / 'r1_tree'
    (plain_folder / 'inner').mkdir(parents=True)
    (plain_folder / 'inner' / 'a_file.txt').write_text('probe\n', encoding='ascii')
    say('R01 rename a folder that holds files, nothing open: '
        + attempt(lambda: os.rename(plain_folder, part_folder / 'r1_tree_SET_ASIDE')))

    # R2: the same rename while this program has a file inside the folder open for reading, the ordinary way.
    open_file_folder = part_folder / 'r2_tree'
    (open_file_folder / 'inner').mkdir(parents=True)
    file_inside = open_file_folder / 'inner' / 'a_file.txt'
    file_inside.write_text('probe\n', encoding='ascii')
    with open(file_inside, 'rb'):
        say('R02 rename a folder while a file inside it is open for reading in this program: '
            + attempt(lambda: os.rename(open_file_folder, part_folder / 'r2_tree_SET_ASIDE')))
    say('R03 the same rename after the file is closed: '
        + (attempt(lambda: os.rename(open_file_folder, part_folder / 'r2_tree_SET_ASIDE'))
           if open_file_folder.exists() else 'not needed: the rename of R02 was done'))

    # R4, R5: a file that is open for reading in this program: can it be replaced, can it be removed?
    replace_folder = part_folder / 'r4_files'
    replace_folder.mkdir()
    target_file = replace_folder / 'report.txt'
    target_file.write_text('old\n', encoding='ascii')
    new_content_file = replace_folder / 'report.txt.tmp'
    new_content_file.write_text('new\n', encoding='ascii')
    with open(target_file, 'rb'):
        say('R04 replace a file (os.replace) while it is open for reading in this program: '
            + attempt(lambda: os.replace(new_content_file, target_file)))
        say('R05 remove a file while it is open for reading in this program: '
            + attempt(lambda: os.remove(target_file)))

    # R6 to R9: the same questions when ANOTHER process is the one in the way: its working folder is inside the
    # folder to be renamed, and it holds another file open.
    helper_home = part_folder / 'r6_tree'
    (helper_home / 'inner').mkdir(parents=True)
    held_folder = part_folder / 'r7_files'
    held_folder.mkdir()
    held_file = held_folder / 'report.txt'
    held_file.write_text('old\n', encoding='ascii')
    replacement_file = held_folder / 'report.txt.tmp'
    replacement_file.write_text('new\n', encoding='ascii')
    flag_folder = part_folder / 'helper_flags'
    flag_folder.mkdir()
    helper = WaitingHelper(helper_home / 'inner', held_file, flag_folder)
    say('R06 rename a folder while another process has its working folder inside it: '
        + attempt(lambda: os.rename(helper_home, part_folder / 'r6_tree_SET_ASIDE')))
    say('R07 replace a file (os.replace) while another process has it open for reading: '
        + attempt(lambda: os.replace(replacement_file, held_file)))
    say('R08 remove a file while another process has it open for reading: '
        + attempt(lambda: os.remove(held_file)))
    say(f'R09 the helper program ended by itself, exit code {helper.let_it_end()}')
    say('R10 the rename of R06 again, after the other process has ended: '
        + (attempt(lambda: os.rename(helper_home, part_folder / 'r6_tree_SET_ASIDE'))
           if helper_home.exists() else 'not needed: the rename of R06 was done'))

    # R11, R12: the careful writer's cycle, many times, to see whether Windows ever refuses a replacement for a
    # moment and what forcing each file to the disk costs on this drive.
    for line_id, flush_to_disk, label in (('R11', False, 'without forcing to disk'),
                                          ('R12', True, 'each file forced to disk first (os.fsync)')):
        cycle_folder = part_folder / f'{line_id.lower()}_cycles'
        cycle_folder.mkdir()
        cycles_done, refusals, seconds = replace_cycles(cycle_folder, flush_to_disk)
        say(f'{line_id} write a temporary file then replace the real one, {REPLACE_CYCLES} times, {label}: '
            f'{cycles_done} done; Windows said no: {refusals if refusals else "never"}; {seconds:.2f} seconds')


# ---------------------------------------------------------------------------------------------------------------
# Part "zip": the size and time of a backup of a tree with its `.venv`
# ---------------------------------------------------------------------------------------------------------------

def is_a_link(path: str) -> bool:
    """Whether a file or folder is a link, a junction or another reparse point (a backup must fail on one).
    path: the full path. Returns: True or False. A path that cannot be examined counts as a link, so it is seen."""
    try:
        status = os.lstat(path)
    except OSError:
        return True
    if stat.S_ISLNK(status.st_mode):
        return True
    return bool(getattr(status, 'st_file_attributes', 0) & FILE_ATTRIBUTE_REPARSE_POINT)


def list_tree(root: Path, parts: list[str] | None) -> dict:
    """List what a backup of a tree would hold, without reading any file's content.
    root: the tree's root. parts: the folders directly under the root (or deeper, as 'results\\research') that are
    taken, with every file lying in the root itself; None takes everything under the root.
    Returns a record, for example {'files': [(relative path, bytes), ...] sorted, 'empty_folders': ['scratch'],
    'links': 0, 'unreadable': 0, 'longest_path': 143, 'largest_file_bytes': 51234567, 'too_old_for_zip': 0}. Links are counted and not
    entered. Never refuses; a folder that cannot be listed is counted under 'unreadable'."""
    start_folders = [root] if parts is None else [root / part for part in parts if (root / part).is_dir()]
    files: list[tuple[str, int]] = []
    empty_folders: list[str] = []
    counts = {'links': 0, 'unreadable': 0, 'longest_path': 0, 'largest_file_bytes': 0, 'too_old_for_zip': 0}

    def note_unreadable(_error: OSError) -> None:
        counts['unreadable'] += 1

    def take_file(full_path: str) -> None:
        if is_a_link(full_path):
            counts['links'] += 1
            return
        size_bytes = os.path.getsize(full_path)
        files.append((os.path.relpath(full_path, root), size_bytes))
        counts['longest_path'] = max(counts['longest_path'], len(full_path))
        counts['largest_file_bytes'] = max(counts['largest_file_bytes'], size_bytes)
        if time.localtime(os.path.getmtime(full_path)).tm_year < EARLIEST_ZIP_YEAR:
            counts['too_old_for_zip'] += 1

    if parts is not None:
        for entry in sorted(os.listdir(root)):
            if os.path.isfile(root / entry):
                take_file(str(root / entry))
    for start_folder in start_folders:
        for folder, subfolder_names, file_names in os.walk(start_folder, onerror=note_unreadable):
            real_subfolders = []
            for name in sorted(subfolder_names):
                if is_a_link(os.path.join(folder, name)):
                    counts['links'] += 1
                else:
                    real_subfolders.append(name)
            subfolder_names[:] = real_subfolders           # os.walk goes only into the folders left in this list
            for name in sorted(file_names):
                take_file(os.path.join(folder, name))
            if not real_subfolders and not file_names:
                empty_folders.append(os.path.relpath(folder, root))
    files.sort()
    return {'files': files, 'empty_folders': sorted(empty_folders), **counts}


def hash_file(full_path: Path) -> str:
    """Read a whole file and return its SHA-256.
    full_path: the file. Returns: 64 hexadecimal characters, for example 'e3b0c442...b855'. An unreadable file
    raises OSError to the caller."""
    digest = hashlib.sha256()
    with open(full_path, 'rb') as handle:
        while True:
            chunk = handle.read(READ_CHUNK_BYTES)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def is_in_environment_digest(relative_path: str) -> bool:
    """Whether a file belongs to the fixed inventory of specification 13, over which the environment's digest is
    taken: `.venv\\pyvenv.cfg`, every file under `.venv\\Scripts\\`, and every file under `.venv\\Lib\\site-packages\\`
    except `__pycache__` folders and `.pyc` files.
    relative_path: the file's path from the tree's root. Returns: True or False. Never refuses."""
    pieces = [piece.lower() for piece in Path(relative_path).parts]
    if not pieces or pieces[0] != '.venv':
        return False
    if pieces[1:] == ['pyvenv.cfg']:
        return True
    if len(pieces) > 2 and pieces[1] == 'scripts':
        return True
    if len(pieces) > 3 and pieces[1] == 'lib' and pieces[2] == 'site-packages':
        return '__pycache__' not in pieces and not pieces[-1].endswith('.pyc')
    return False


def write_zip(root: Path, listing: dict, zip_path: Path, deflate_level: int) -> tuple[dict[str, str], float]:
    """Write one ZIP of the listed files as a backup would: each file read once, hashed while it is compressed.
    root: the tree's root. listing: the record of list_tree. zip_path: the ZIP to write (must not exist).
    deflate_level: 1 to 9.
    Returns: (SHA-256 of every file by relative path, seconds), for example ({'src\\a.py': 'ab12...'}, 61.3).
    A file that cannot be read raises OSError: a backup would fail there too."""
    hashes: dict[str, str] = {}
    started = time.perf_counter()
    with zipfile.ZipFile(zip_path, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=deflate_level,
                         allowZip64=True) as archive:
        for relative_path, _size in listing['files']:
            member = zipfile.ZipInfo.from_file(root / relative_path, Path(relative_path).as_posix(),
                                               strict_timestamps=False)
            member.compress_type = zipfile.ZIP_DEFLATED
            # The level of a member given as a ZipInfo is the member's own; the attribute's public name is newer
            # than its private one, so whichever this Python has is set.
            if hasattr(member, 'compress_level'):
                member.compress_level = deflate_level
            else:
                member._compresslevel = deflate_level
            digest = hashlib.sha256()
            with open(root / relative_path, 'rb') as source, archive.open(member, 'w', force_zip64=True) as target:
                while True:
                    chunk = source.read(READ_CHUNK_BYTES)
                    if not chunk:
                        break
                    digest.update(chunk)
                    target.write(chunk)
            hashes[relative_path] = digest.hexdigest()
        for relative_folder in listing['empty_folders']:
            archive.write(root / relative_folder, Path(relative_folder).as_posix())
    return hashes, time.perf_counter() - started


def read_zip_back(zip_path: Path, expected_hashes: dict[str, str]) -> tuple[int, float]:
    """Read every file member of a ZIP back and compare its SHA-256 with the one taken when it was written.
    zip_path: the ZIP. expected_hashes: SHA-256 by relative path, as write_zip returned.
    Returns: (members that differ or are missing, seconds), for example (0, 9.7). Never refuses."""
    expected_by_member = {Path(relative_path).as_posix(): sha for relative_path, sha in expected_hashes.items()}
    different = 0
    seen = 0
    started = time.perf_counter()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            digest = hashlib.sha256()
            with archive.open(member) as handle:
                while True:
                    chunk = handle.read(READ_CHUNK_BYTES)
                    if not chunk:
                        break
                    digest.update(chunk)
            seen += 1
            if expected_by_member.get(member.filename) != digest.hexdigest():
                different += 1
    different += len(expected_by_member) - seen if seen < len(expected_by_member) else 0
    return different, time.perf_counter() - started


def megabytes(byte_count: int) -> str:
    """Return a byte count as text in megabytes and bytes, for example '254.3 MB (266,653,771 bytes)'."""
    return f'{byte_count / 1_000_000:.1f} MB ({byte_count:,} bytes)'


def part_zip(work_folder: Path, tree_root: Path | None, tree_parts: list[str], otherwise_environment_of: Path | None) -> None:
    """Measure and print the size and time of a backup of a tree with its `.venv`.
    work_folder: this task's scratch folder; the two ZIPs are written in its new subfolder 'zip_part' and left there.
    tree_root: a whole tree with its own `.venv` (the scratch tree of an earlier task), or None.
    tree_parts: the folders of that tree a QA or PROD tree would also hold; only they, and the files in the tree's
    root, go into the ZIP. otherwise_environment_of: a folder whose `.venv` alone is measured when tree_root is not
    there. Returns nothing. Refuses if neither source is there, if a link is found, or if the work drive is short of
    free space."""
    part_folder = fresh_folder(work_folder / 'zip_part')
    if tree_root is not None and (tree_root / '.venv' / 'pyvenv.cfg').is_file():
        source_root, source_parts = tree_root, tree_parts
        say(f'Z00 the source is the tree {source_root}; the ZIP holds the files in its root and these folders: '
            f'{", ".join(source_parts)}')
        whole = list_tree(source_root, None)
        top_level: dict[str, list[int]] = {}
        for relative_path, size_bytes in whole['files']:
            pieces = Path(relative_path).parts
            first = pieces[0] if len(pieces) > 1 else '(files in the root)'
            entry = top_level.setdefault(first, [0, 0])
            entry[0] += 1
            entry[1] += size_bytes
        for name in sorted(top_level):
            say(f'Z01 the whole tree, by top-level folder: {name}: {top_level[name][0]:,} files, '
                f'{megabytes(top_level[name][1])}')
    elif otherwise_environment_of is not None and (otherwise_environment_of / '.venv' / 'pyvenv.cfg').is_file():
        source_root, source_parts = otherwise_environment_of, ['.venv']
        say('Z00 the tree named by --tree-root is not there (or has no .venv); the source is the `.venv` folder alone '
            f'of {source_root}, read only. The research results are not in this measurement.')
    else:
        raise ProbeRefused('neither the tree named by --tree-root nor the folder named by --otherwise-environment-of '
                           'holds a `.venv` with a pyvenv.cfg. Nothing was measured. Check the two paths.')

    listing = list_tree(source_root, source_parts if source_root == tree_root else ['.venv'])
    if source_root != tree_root:
        listing['files'] = [entry for entry in listing['files'] if Path(entry[0]).parts[0] == '.venv']
    total_bytes = sum(size_bytes for _path, size_bytes in listing['files'])
    say(f'Z02 what the ZIP will hold: {len(listing["files"]):,} files, {megabytes(total_bytes)}; '
        f'{len(listing["empty_folders"]):,} empty folders; largest file {megabytes(listing["largest_file_bytes"])}; '
        f'longest full path {listing["longest_path"]} characters')
    say(f'Z03 links, junctions or other reparse points found: {listing["links"]}; folders that could not be listed: '
        f'{listing["unreadable"]}; files dated before {EARLIEST_ZIP_YEAR}, whose time a ZIP cannot hold: '
        f'{listing["too_old_for_zip"]}')
    if listing['links'] or listing['unreadable']:
        raise ProbeRefused('the source holds a link or a folder that cannot be listed. A backup would fail on it '
                           '(deployment design section 10), so nothing more is measured. The count is the finding.')
    free_bytes = shutil.disk_usage(part_folder).free
    say(f'Z04 free space on the work drive: {megabytes(free_bytes)}')
    if free_bytes < FREE_SPACE_FACTOR * total_bytes:
        raise ProbeRefused(f'the work drive has less than {FREE_SPACE_FACTOR} times the bytes to be read free. '
                           f'No ZIP was written. Free some space on the work drive, or measure a smaller source.')

    digest_files = [entry for entry in listing['files'] if is_in_environment_digest(entry[0])]
    digest_bytes = sum(size_bytes for _path, size_bytes in digest_files)
    started = time.perf_counter()
    for relative_path, _size in digest_files:
        hash_file(source_root / relative_path)
    say(f'Z05 the environment digest (specification 13): {len(digest_files):,} files, {megabytes(digest_bytes)}; '
        f'read and hashed in {time.perf_counter() - started:.1f} seconds (the first reading in this run)')

    design_zip = part_folder / f'probe_level{DESIGN_DEFLATE_LEVEL}.zip'
    first_hashes, seconds = write_zip(source_root, listing, design_zip, DESIGN_DEFLATE_LEVEL)
    design_zip_bytes = design_zip.stat().st_size
    say(f'Z06 the ZIP at Deflate level {DESIGN_DEFLATE_LEVEL} (the design\'s level), each file hashed as it is '
        f'compressed: {seconds:.1f} seconds; {megabytes(design_zip_bytes)}; '
        f'{100 * design_zip_bytes / max(total_bytes, 1):.1f}% of the source')

    different, seconds = read_zip_back(design_zip, first_hashes)
    say(f'Z07 the ZIP read back, every member hashed and compared: {seconds:.1f} seconds; members that differ: '
        f'{different}')

    started = time.perf_counter()
    changed = sum(1 for relative_path, _size in listing['files']
                  if hash_file(source_root / relative_path) != first_hashes[relative_path])
    say(f'Z08 every source file read and hashed a second time: {time.perf_counter() - started:.1f} seconds; '
        f'files that changed between the two readings: {changed}')

    comparison_zip = part_folder / f'probe_level{COMPARISON_DEFLATE_LEVEL}.zip'
    _hashes, seconds = write_zip(source_root, listing, comparison_zip, COMPARISON_DEFLATE_LEVEL)
    comparison_zip_bytes = comparison_zip.stat().st_size
    say(f'Z09 for comparison only, the ZIP at Deflate level {COMPARISON_DEFLATE_LEVEL}: {seconds:.1f} seconds; '
        f'{megabytes(comparison_zip_bytes)}; {100 * comparison_zip_bytes / max(total_bytes, 1):.1f}% of the source')

    started = time.perf_counter()
    for relative_path, _size in digest_files:
        hash_file(source_root / relative_path)
    say(f'Z10 the environment digest once more, the files now lately read: {time.perf_counter() - started:.1f} seconds')
    say(f'Z11 the two ZIPs are left in {part_folder}; this probe removes nothing')


# ---------------------------------------------------------------------------------------------------------------
# Part "processes": what a Python program can read of the other processes on this PC
# ---------------------------------------------------------------------------------------------------------------

def is_python_program_name(program_name: str) -> bool:
    """Whether a process's program name is a Python interpreter's or the Python launcher's.
    program_name: for example 'python.exe', 'pythonw.exe', 'python3.15.exe', 'py.exe'.
    Returns: True for those, False for 'pycharm64.exe' or 'cmd.exe'. Never refuses."""
    return re.fullmatch(r'(?i)(python[0-9.]*w?|pyw?)(_d)?(\.exe)?', program_name or '') is not None


def place_of(program_path: str | None, scratch_root: Path) -> str:
    """Say where a running program's file lies, in words, so that no path of the PC is printed.
    program_path: the full path of the program's file, or None if it could not be read. scratch_root: the scratch
    folder of the project's rehearsals.
    Returns one of: 'could not be read'; 'the environment that runs this probe'; 'the base Python of that
    environment'; 'under the scratch folder'; 'elsewhere on the PC'. Never refuses."""
    if not program_path:
        return 'could not be read'
    normal = os.path.normcase(os.path.abspath(program_path))

    def is_under(folder: str) -> bool:
        base = os.path.normcase(os.path.abspath(folder)).rstrip('\\/')
        return normal == base or normal.startswith(base + os.sep)

    if is_under(sys.prefix):
        return 'the environment that runs this probe'
    if is_under(sys.base_prefix):
        return 'the base Python of that environment'
    if is_under(str(scratch_root)):
        return 'under the scratch folder'
    return 'elsewhere on the PC'


def describe_relation(process_id: int, parent_of: dict[int, int], own_id: int, helper_ids: set[int]) -> str:
    """Say what a process is to this probe.
    process_id: the process. parent_of: each process's parent, by ID. own_id: this probe's process ID.
    helper_ids: the IDs of the helper program's processes.
    Returns one of: 'this probe'; 'an ancestor of this probe'; 'the helper program'; 'another program'."""
    if process_id == own_id:
        return 'this probe'
    if process_id in helper_ids:
        return 'the helper program'
    ancestor, steps = parent_of.get(own_id), 0
    while ancestor and steps < 64:                         # 64: far deeper than any real chain; guards a cycle of reused IDs
        if ancestor == process_id:
            return 'an ancestor of this probe'
        ancestor, steps = parent_of.get(ancestor), steps + 1
    return 'another program'


def descendants_of(process_id: int, parent_of: dict[int, int]) -> set[int]:
    """Return the IDs of every process started, directly or not, by one process.
    process_id: the process. parent_of: each process's parent, by ID.
    Returns: for example {4120, 9876}; empty if it started none. Never refuses."""
    found: set[int] = set()
    grew = True
    while grew:
        grew = False
        for child_id, parent_id in parent_of.items():
            if child_id not in found and child_id != process_id and (parent_id == process_id or parent_id in found):
                found.add(child_id)
                grew = True
    return found


def read_table_with_psutil(scratch_root: Path, helper_folder: Path) -> dict | None:
    """Read the process table with psutil, as the project's reviewed process tool does.
    scratch_root: the scratch folder (to describe where a program lies). helper_folder: the helper's working folder.
    Returns None if psutil is not installed; otherwise a record, for example {'count': 312, 'parent_of': {...},
    'python': {4120: {'name': 'python.exe', 'place': '...', 'unreadable': ['cwd'], 'cwd_is_helper_folder': False,
    'start_time': 1795500000.1}}, 'other_command_lines_unreadable': 41}. Never refuses."""
    try:
        import psutil
    except ImportError:
        return None
    record = {'count': 0, 'parent_of': {}, 'python': {}, 'other_command_lines_unreadable': 0,
              'boot_time': psutil.boot_time(), 'version': psutil.__version__}
    for process in psutil.process_iter(['pid', 'ppid', 'name']):
        record['count'] += 1
        process_id, name = process.info['pid'], process.info.get('name') or ''
        record['parent_of'][process_id] = process.info.get('ppid') or 0
        if not is_python_program_name(name):
            try:
                process.cmdline()
            except Exception:
                record['other_command_lines_unreadable'] += 1
            continue
        details = {'name': name, 'unreadable': [], 'place': 'could not be read', 'cwd_is_helper_folder': False,
                   'start_time': None}
        for detail in ('exe', 'cwd', 'cmdline', 'create_time'):
            try:
                value = getattr(process, detail)()
            except Exception as error:
                details['unreadable'].append(f'{detail} ({type(error).__name__})')
                continue
            if detail == 'exe':
                details['place'] = place_of(value, scratch_root)
            elif detail == 'cwd':
                details['cwd_is_helper_folder'] = os.path.normcase(value or '') == os.path.normcase(str(helper_folder))
            elif detail == 'create_time':
                details['start_time'] = value
        record['python'][process_id] = details
    return record


class WindowsProcessTable:
    """Windows' own process table, read with the standard library alone (ctypes and kernel32), read-only."""

    SNAPSHOT_OF_PROCESSES = 0x00000002                     # TH32CS_SNAPPROCESS: the snapshot holds the process list
    QUERY_LIMITED_INFORMATION = 0x1000                     # the least access right that still gives a program's path and times
    LONGEST_PROGRAM_PATH = 32768                           # the longest path Windows can return, in characters
    SECONDS_FROM_1601_TO_1970 = 11644473600                # Windows counts time from 1601; Python from 1970

    def __init__(self) -> None:
        """Declare the few kernel32 functions used, each with its exact argument and return types.
        Refuses (OSError or AttributeError) outside Windows; the caller prints that as a finding."""
        from ctypes import wintypes

        class ProcessEntry(ctypes.Structure):              # PROCESSENTRY32W, field for field as Windows declares it
            _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD),
                        ('th32ProcessID', wintypes.DWORD), ('th32DefaultHeapID', ctypes.c_size_t),
                        ('th32ModuleID', wintypes.DWORD), ('cntThreads', wintypes.DWORD),
                        ('th32ParentProcessID', wintypes.DWORD), ('pcPriClassBase', wintypes.LONG),
                        ('dwFlags', wintypes.DWORD), ('szExeFile', wintypes.WCHAR * 260)]

        self.ProcessEntry = ProcessEntry
        self.wintypes = wintypes
        self.invalid_handle = ctypes.c_void_p(-1).value
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        kernel.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
        kernel.Process32FirstW.restype = wintypes.BOOL
        kernel.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(ProcessEntry)]
        kernel.Process32NextW.restype = wintypes.BOOL
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR,
                                                      ctypes.POINTER(wintypes.DWORD)]
        kernel.QueryFullProcessImageNameW.restype = wintypes.BOOL
        kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
        kernel.GetProcessTimes.restype = wintypes.BOOL
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        kernel.GetTickCount64.argtypes = []
        kernel.GetTickCount64.restype = ctypes.c_ulonglong
        self.kernel = kernel

    def list_processes(self) -> list[tuple[int, int, str]]:
        """Return every process as (process ID, parent's ID, program name), for example
        [(4, 0, 'System'), (4120, 3988, 'python.exe')]. Refuses (OSError) if Windows gives no snapshot."""
        snapshot = self.kernel.CreateToolhelp32Snapshot(self.SNAPSHOT_OF_PROCESSES, 0)
        if snapshot is None or snapshot == self.invalid_handle:
            raise OSError(f'CreateToolhelp32Snapshot gave no snapshot (Windows error {ctypes.get_last_error()})')
        found: list[tuple[int, int, str]] = []
        try:
            entry = self.ProcessEntry()
            entry.dwSize = ctypes.sizeof(self.ProcessEntry)
            more = self.kernel.Process32FirstW(snapshot, ctypes.byref(entry))
            while more:
                found.append((int(entry.th32ProcessID), int(entry.th32ParentProcessID), str(entry.szExeFile)))
                more = self.kernel.Process32NextW(snapshot, ctypes.byref(entry))
        finally:
            self.kernel.CloseHandle(snapshot)
        return found

    def program_path_and_start_time(self, process_id: int) -> tuple[str | None, float | None]:
        """Return a process's full program path and its start time (seconds since 1970), each None if Windows will
        not give it; for example ('D:\\x\\python.exe', 1795500000.1) or (None, None). Never refuses."""
        handle = self.kernel.OpenProcess(self.QUERY_LIMITED_INFORMATION, False, process_id)
        if not handle:
            return None, None
        try:
            program_path = None
            buffer = ctypes.create_unicode_buffer(self.LONGEST_PROGRAM_PATH)
            length = self.wintypes.DWORD(self.LONGEST_PROGRAM_PATH)
            if self.kernel.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(length)):
                program_path = buffer.value
            start_time = None
            created, exited, kernel_time, user_time = (self.wintypes.FILETIME() for _ in range(4))
            if self.kernel.GetProcessTimes(handle, ctypes.byref(created), ctypes.byref(exited),
                                           ctypes.byref(kernel_time), ctypes.byref(user_time)):
                ticks = (created.dwHighDateTime << 32) | created.dwLowDateTime     # units of 100 nanoseconds
                start_time = ticks / 10_000_000 - self.SECONDS_FROM_1601_TO_1970
            return program_path, start_time
        finally:
            self.kernel.CloseHandle(handle)

    def seconds_since_windows_started(self) -> float:
        """Return how long Windows has been running, in seconds, for example 93784.5. Never refuses."""
        return self.kernel.GetTickCount64() / 1000.0


def local_time_text(seconds_since_1970: float) -> str:
    """Return a time as local date and time to the second, for example '2026-11-24 08:15:02'."""
    return datetime.fromtimestamp(seconds_since_1970).strftime('%Y-%m-%d %H:%M:%S')


def part_processes(work_folder: Path, scratch_root: Path) -> int:
    """Measure and print what this Python can read of the other processes, with psutil and with the standard
    library alone, with one helper process of known place, working folder and parentage as the test object.
    work_folder: this task's scratch folder; the part works in its new subfolder 'processes_part'.
    scratch_root: the rehearsals' scratch folder, to describe where a program lies.
    Returns: how many of its measurements could not be made through a fault of the probe itself (0 when all were
    made). Refuses if its subfolder is there already or the helper does not start."""
    part_folder = fresh_folder(work_folder / 'processes_part')
    helper_folder = part_folder / 'helper_working_folder'
    helper_folder.mkdir()
    held_file = part_folder / 'held_open.txt'
    held_file.write_text('probe\n', encoding='ascii')
    flag_folder = part_folder / 'helper_flags'
    flag_folder.mkdir()
    own_id = os.getpid()
    faults = 0
    with_psutil = None                                     # stays None if psutil is absent or its reading fails
    say(f'P00 this probe is process {own_id}; started as {Path(sys.executable).name} of '
        f'{place_of(sys.executable, scratch_root)}; Python {sys.version.split()[0]}')
    helper = WaitingHelper(helper_folder, held_file, flag_folder)
    say(f'P01 the helper program was started with the same Python; the process ID Windows gave for it: '
        f'{helper.process.pid}')
    try:
        # ---- with psutil
        try:
            with_psutil = read_table_with_psutil(scratch_root, helper_folder)
            if with_psutil is None:
                say('P10 psutil is not installed in this Python: no comparison with it')
            else:
                helper_ids = {helper.process.pid} | descendants_of(helper.process.pid, with_psutil['parent_of'])
                say(f'P10 psutil {with_psutil["version"]}: {with_psutil["count"]} processes; '
                    f'{len(with_psutil["python"])} with a Python program name; command lines of other programs it '
                    f'could not read: {with_psutil["other_command_lines_unreadable"]}')
                for process_id in sorted(with_psutil['python']):
                    details = with_psutil['python'][process_id]
                    say(f'P11 psutil: {details["name"]}: '
                        f'{describe_relation(process_id, with_psutil["parent_of"], own_id, helper_ids)}; its program '
                        f'file: {details["place"]}; details it could not read: '
                        f'{", ".join(details["unreadable"]) if details["unreadable"] else "none"}; working folder is '
                        f'the helper\'s folder: {"yes" if details["cwd_is_helper_folder"] else "no"}')
                say(f'P12 psutil: the helper program appears as {len(helper_ids & set(with_psutil["python"]))} Python '
                    f'process(es)')
                say(f'P13 psutil: Windows was started at {local_time_text(with_psutil["boot_time"])} (local time)')
        except Exception as error:
            faults += 1
            say(f'P19 the psutil measurements were NOT MADE, through a fault of this probe: '
                f'{type(error).__name__}: {error}')

        # ---- with the standard library alone
        try:
            windows = WindowsProcessTable()
            listed = windows.list_processes()
            parent_of = {process_id: parent_id for process_id, parent_id, _name in listed}
            name_of = {process_id: name for process_id, _parent_id, name in listed}
            python_ids = sorted(process_id for process_id, name in name_of.items() if is_python_program_name(name))
            helper_ids = {helper.process.pid} | descendants_of(helper.process.pid, parent_of)
            names_like_python: dict[str, int] = {}
            for name in name_of.values():
                if name.lower().startswith('py'):
                    names_like_python[name.lower()] = names_like_python.get(name.lower(), 0) + 1
            say(f'P20 standard library (the Toolhelp snapshot): {len(listed)} processes; {len(python_ids)} with a '
                f'Python program name; every program name that begins "py", with its count: '
                f'{dict(sorted(names_like_python.items()))}')
            paths_read = times_read = 0
            for process_id in python_ids:
                program_path, start_time = windows.program_path_and_start_time(process_id)
                paths_read += program_path is not None
                times_read += start_time is not None
                say(f'P21 standard library: {name_of[process_id]}: '
                    f'{describe_relation(process_id, parent_of, own_id, helper_ids)}; its program file: '
                    f'{place_of(program_path, scratch_root)}; its start time: '
                    f'{"read" if start_time is not None else "could not be read"}')
            say(f'P22 standard library: of the {len(python_ids)} Python processes, program path read for '
                f'{paths_read}, start time read for {times_read}')
            say(f'P23 standard library: the helper program appears as {len(helper_ids & set(python_ids))} Python '
                f'process(es)')
            chain, ancestor = [name_of.get(own_id, '?')], parent_of.get(own_id)
            while ancestor and ancestor in name_of and len(chain) < 12:      # 12: enough to show the shell and its starter
                chain.append(name_of[ancestor])
                ancestor = parent_of.get(ancestor)
            say(f'P24 standard library: this probe and what started it, by program name: {" <- ".join(chain)}')
            started_at = time.time() - windows.seconds_since_windows_started()
            running_for = windows.seconds_since_windows_started()
            say(f'P25 standard library (the tick count): Windows was started at {local_time_text(started_at)} (local '
                f'time); running for {int(running_for // 86400)} days {int(running_for % 86400 // 3600)} hours '
                f'{int(running_for % 3600 // 60)} minutes')
            if with_psutil is not None:
                same_ids = set(python_ids) == set(with_psutil['python'])
                say(f'P26 the two readings name the same Python processes: {"yes" if same_ids else "NO"}; their '
                    f'start times of Windows differ by {abs(started_at - with_psutil["boot_time"]):.1f} seconds')
                _own_path, own_start = windows.program_path_and_start_time(own_id)
                psutil_start = with_psutil['python'].get(own_id, {}).get('start_time')
                if own_start is not None and psutil_start is not None:
                    say(f'P27 this probe\'s own start time by the two readings differs by '
                        f'{abs(own_start - psutil_start):.3f} seconds')
        except Exception as error:
            faults += 1
            say(f'P29 the standard-library measurements were NOT MADE: {type(error).__name__}: {error}')
    finally:
        say(f'P30 the helper program ended by itself, exit code {helper.let_it_end()}')
    return faults


# ---------------------------------------------------------------------------------------------------------------
# The command line
# ---------------------------------------------------------------------------------------------------------------

def main(arguments: list[str] | None = None) -> int:
    """Run one part of the probe and say how it finished.
    arguments: the command line, or None for the real one.
    Returns the exit code: 0 the part ran to its end and made every measurement; 1 it refused or a measurement
    was not made."""
    parser = argparse.ArgumentParser(description='TASK_T028 probe (see the header of this file).')
    parser.add_argument('part', choices=('rename', 'zip', 'processes'))
    parser.add_argument('--work', required=True, type=Path, help="this task's scratch folder (must exist)")
    parser.add_argument('--scratch-root', type=Path, help='processes: the rehearsals\' scratch folder')
    parser.add_argument('--tree-root', type=Path, help='zip: a whole scratch tree with its own .venv')
    parser.add_argument('--tree-part', action='append', default=[], help='zip: a folder of that tree to take')
    parser.add_argument('--otherwise-environment-of', type=Path,
                        help='zip: the folder whose .venv alone is measured if the tree is not there')
    options = parser.parse_args(arguments)
    # Every path is made absolute at once: the helper program runs in another working folder, where a relative
    # path would name another place. (abspath, not resolve: a path is used as it was given, never followed.)
    for name in ('work', 'scratch_root', 'tree_root', 'otherwise_environment_of'):
        if getattr(options, name) is not None:
            setattr(options, name, Path(os.path.abspath(getattr(options, name))))
    say(f'PROBE PART {options.part}: STARTED {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}; work folder '
        f'{options.work}; platform {sys.platform}')
    try:
        if not options.work.is_dir():
            raise ProbeRefused(f'the work folder {options.work} is not there. The task file creates it in an '
                               f'earlier step; nothing was measured.')
        faults = 0
        if options.part == 'rename':
            part_rename(options.work)
        elif options.part == 'zip':
            part_zip(options.work, options.tree_root, options.tree_part, options.otherwise_environment_of)
        else:
            if options.scratch_root is None:
                raise ProbeRefused('the part "processes" needs --scratch-root. Nothing was measured.')
            faults = part_processes(options.work, options.scratch_root)
    except ProbeRefused as refusal:
        say(f'PROBE PART {options.part}: REFUSED: {refusal}')
        return 1
    if faults:
        say(f'PROBE PART {options.part}: FINISHED WITH {faults} MEASUREMENT(S) NOT MADE')
        return 1
    say(f'PROBE PART {options.part}: FINISHED')
    return 0


if __name__ == '__main__':
    sys.exit(main())
