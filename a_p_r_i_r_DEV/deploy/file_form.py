"""The project's standard for the form of its text files (line endings): the list of kinds, what "conforms"
means, the one way a file is brought to its form, and the search of Python code for a write that names no line
ending.

What this file is for
    Every text file of the living project ends its lines CRLF, whoever wrote it; the line-record files (.jsonl)
    end them LF, because a list line is the canonical encoding whose bytes, ending included, the hash chain is
    computed from. This file is the one piece of code that knows that rule. It says which form a file must have
    from its name alone, reads a file's bytes and says exactly how they break the rule, changes line endings and
    nothing else, and reads Python source to find a file write that leaves the line ending to the platform. It
    reads the disk only: it never asks Git anything, and it never looks inside a tree's .venv.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_2.md (RAT-49): section 3 (the list), 3A (the six files left out by name), 3B (what
    conforms means), 4 (every program says what it writes) and 6 (the checker).

Which of the project's own modules it uses
    None: standard library only, so that the conversion program can use it before anything else is installed.

What uses it
    tests/test_file_form.py (the suite's check of DEV's own files); the conversion program of the standard's
    section 7; Make_Installable and Check_Tree of build step 3.
"""
from __future__ import annotations

import ast
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path

# The three forms a kind of file can have. CRLF: every line ends carriage return, line feed. LF: no carriage
# return anywhere. BINARY: not text; it has no line endings and is never read by this file.
CRLF = 'CRLF'
LF = 'LF'
BINARY = 'BINARY'

# The standard's table (section 3), by the end of a file's name, in lower case. A kind is here only because the
# standard names it; a kind that is not here is refused, never guessed (section 3B).
FORM_BY_SUFFIX = {
    '.py': CRLF,        # Python code
    '.bat': CRLF,       # batch files
    '.cmd': CRLF,
    '.ini': CRLF,       # settings, manifests, status files
    '.json': CRLF,      # JSON documents: declarations, markers, records, verification records
    '.csv': CRLF,       # tables: the results masters, their ledgers, report tables
    '.txt': CRLF,       # reports, read-me files
    '.log': CRLF,       # logs
    '.md': CRLF,        # documents
    '.lock': CRLF,      # lock files (JOB.lock and the like)
    '.jsonl': LF,       # THE ONE EXCEPTION: line-record files; the line ending is part of what is hashed
    '.sh': LF,          # shell scripts of the cloud helpers; none is part of the living project
    '.zip': BINARY,
    '.pdf': BINARY,
    '.png': BINARY,
    '.jpg': BINARY,
    '.gif': BINARY,
    '.ico': BINARY,
    '.pyc': BINARY,     # Python's compiled files
}
# The standard's table for files known by their whole name (text without an extension; flag files).
FORM_BY_NAME = {
    '.gitattributes': CRLF,
    '.gitignore': CRLF,
    'LICENSE': CRLF,
    'SNAPSHOT_DUE': CRLF,
}
# The six files of the retired Mode H release machinery (standard section 3A), from the tree root with forward
# slashes. They are pinned to their exact bytes by that machinery's own tests; they are neither converted nor
# checked, and stay exactly as they are.
LEFT_OUT_BY_NAME = (
    'src/methods/_common/contract_data/install_records/INSTALL_MHUP_A_V1.json',
    'src/methods/_common/contract_data/install_records/RELEASE_BASELINE_20261031_V1.json',
    'src/methods/_common/contract_data/install_records/RELEASE_MHUP_A_V1.json',
    'src/package_tools/process_check.py',
    'src/results_master_v0_2.py',
    'tests/fixtures/results_master_v0_1_reference.py.txt',
)
# Folders that are never walked: Python's own cache folders, which hold nothing the project wrote.
NEVER_WALKED_FOLDERS = ('__pycache__',)
# The mark Windows puts on a link, a junction or any other reparse point (stat.FILE_ATTRIBUTE_REPARSE_POINT).
REPARSE_POINT_ATTRIBUTE = 0x400
# The rule in one paragraph, with its exception: the standard requires that the exception is said wherever the
# rule is summarised (section 3), so every message of the checker ends with this.
RULE_IN_SHORT = ('The standard (doc/FILE_FORM_STANDARD_v0_2.md): every text file of the project ends its lines CRLF. '
                 'The one exception: every .jsonl file ends its lines LF, because the line ending is part of what '
                 'its hash chain is computed from.')
# What a person does about a file in the wrong form (standard section 10).
WHAT_TO_DO = ('To correct a file by hand: in VS Code, click LF or CRLF at the bottom right and choose; in Notepad++, '
              'Edit, EOL Conversion. A .jsonl file is never edited by hand.')

# A carriage return that no line feed follows, and a line feed that no carriage return precedes.
_BARE_CR = re.compile(rb'\r(?!\n)')
_BARE_LF = re.compile(rb'(?<!\r)\n')
# The mode letters of open() that mean the file may be written.
_WRITING_MODE_LETTERS = 'wax+'
# The calls that open a file the way open() does: the mode is the second argument.
_OPEN_LIKE_NAMES = ('open', 'fdopen')
# Modules whose own open() takes the file first and the mode second, as the built-in does; any other
# <something>.open(...) is taken to be a path's, whose mode comes first.
_MODULES_WITH_AN_OPEN = ('io', 'codecs', 'builtins')
# The temporary-file makers of the standard library whose mode is a keyword (their default mode is binary).
_TEMPORARY_FILE_NAMES = ('NamedTemporaryFile', 'TemporaryFile', 'SpooledTemporaryFile')
# Calls that write a text file with the platform's own line ending whatever they are given.
_ALWAYS_PLATFORM_NAMES = ('FileHandler',)


class FileFormRefused(ValueError):
    """A file cannot be brought to its form, or its form cannot be decided. The message says what was found,
    where, and what to do."""


@dataclass(frozen=True)
class Fault:
    """One file that does not conform.

    path    the file, from the tree root with forward slashes, for example 'src/research/reader.py'
    what    what is wrong and which rule of the standard's section 3B it breaks, for example
            'must be CRLF but 12 line(s) end LF alone, the first at line 3 (section 3B: a CRLF file)'
    """
    path: str
    what: str


def as_root_path(relative_path: str | os.PathLike) -> str:
    """A path from the tree root in the one spelling this file uses: forward slashes.

    relative_path   a path from the tree root, in either spelling
    Returns, for example, 'src/research/reader.py' for 'src\\research\\reader.py'.
    """
    return str(relative_path).replace('\\', '/')


def is_left_out_by_name(relative_path: str | os.PathLike) -> bool:
    """Whether a file is one of the six the standard leaves out by name (section 3A).

    relative_path   the file, from the tree root
    Returns True or False. Windows does not tell upper case from lower in a path, so neither does this.
    """
    wanted = as_root_path(relative_path).lower()
    return any(wanted == left_out.lower() for left_out in LEFT_OUT_BY_NAME)


def form_of(relative_path: str | os.PathLike) -> str | None:
    """The form the standard gives a file, decided from its name alone.

    relative_path   the file, from the tree root or just its name
    Returns CRLF, LF or BINARY; or None when the standard's table does not name this kind of file (the caller
    refuses such a file: section 3B). For example 'CRLF' for 'Run_Research.bat', 'LF' for 'FORECASTS.jsonl',
    None for 'notes.docx'.
    """
    name = as_root_path(relative_path).rsplit('/', 1)[-1]
    if name in FORM_BY_NAME:
        return FORM_BY_NAME[name]
    return FORM_BY_SUFFIX.get(os.path.splitext(name)[1].lower())


def _line_number_at(data: bytes, position: int) -> int:
    """The number of the line (from 1) that holds the byte at a position, counting line feeds before it."""
    return data.count(b'\n', 0, position) + 1


def faults_in_bytes(data: bytes, form: str) -> list[str]:
    """How some bytes break the rule for their form (standard section 3B).

    data    the whole content of a file
    form    CRLF or LF (a BINARY file is never given to this function)
    Returns a list of plain sentences, empty when the bytes conform; for example
    ['must be CRLF but 12 line(s) end LF alone, the first at line 3 (section 3B: a CRLF file)'].
    An empty file conforms, and a last line with no line ending is allowed.
    Refuses (FileFormRefused) a form that is neither CRLF nor LF.
    """
    if form not in (CRLF, LF):
        raise FileFormRefused(f'the form {form!r} is not one this check reads; it reads {CRLF} and {LF} files only')
    faults = []
    if b'\x00' in data:
        faults.append(f'holds a zero byte, the first at byte {data.index(bytes(1)) + 1} (section 3B: a file of a text '
                      'kind must hold none, and is never passed over as binary)')
    try:
        data.decode('utf-8')
    except UnicodeDecodeError as error:
        faults.append(f'does not read as UTF-8 at byte {error.start + 1} (section 3B: a file of a text kind must)')
    bare_carriage_returns = _BARE_CR.findall(data)
    if form == CRLF:
        bare_line_feeds = list(_BARE_LF.finditer(data))
        if bare_line_feeds:
            faults.append(f'must be CRLF but {len(bare_line_feeds)} line(s) end LF alone, the first at line '
                          f'{_line_number_at(data, bare_line_feeds[0].start())} (section 3B: a CRLF file)')
        if bare_carriage_returns:
            faults.append(f'holds {len(bare_carriage_returns)} carriage return(s) that no line feed follows, the '
                          f'first at line {_line_number_at(data, _BARE_CR.search(data).start())} (section 3B: a '
                          'CRLF file)')
    elif b'\r' in data:
        faults.append(f'must be LF but holds {data.count(bytes([13]))} carriage return(s), the first at line '
                      f'{_line_number_at(data, data.index(bytes([13])))} (section 3B: an LF file holds none)')
    return faults


def faults_of_file(root: str | os.PathLike, relative_path: str | os.PathLike) -> list[Fault]:
    """Check one file of a tree against the standard.

    root            the tree's root folder
    relative_path   the file, from that root
    Returns a list of Fault, empty when the file conforms, is BINARY by kind, or is left out by name; for example
    [Fault('src/x.py', 'must be CRLF but 3 line(s) end LF alone, the first at line 1 (section 3B: a CRLF file)')].
    A file of a kind the standard does not name, and a file that cannot be read, are each a Fault: nothing is
    assumed and nothing is skipped.
    """
    path = as_root_path(relative_path)
    if is_left_out_by_name(path):
        return []
    form = form_of(path)
    if form is None:
        return [Fault(path, 'is of a kind the standard does not name (section 3B: the table is extended by the '
                            "owner's recorded decision before such a file is accepted)")]
    if form == BINARY:
        return []
    try:
        data = (Path(root) / path).read_bytes()
    except OSError as error:
        return [Fault(path, f'could not be read ({error.strerror or error})')]
    return [Fault(path, what) for what in faults_in_bytes(data, form)]


def faults_of_files(root: str | os.PathLike, relative_paths) -> list[Fault]:
    """Check several files of a tree; the faults of all of them, in the order the files were given.

    root            the tree's root folder
    relative_paths  the files, each from that root
    Returns a list of Fault, empty when every file conforms.
    """
    faults = []
    for relative_path in relative_paths:
        faults.extend(faults_of_file(root, relative_path))
    return faults


def is_link(path: str | os.PathLike) -> bool:
    """Whether a path is a link, a junction or any other Windows reparse point. The path is never followed.

    path    a file or a folder
    Returns True for a symbolic link anywhere and, on Windows, for anything that carries the reparse-point mark
    (a junction, a link to a folder or a file, a placeholder of a cloud drive); False for an ordinary file or
    folder and for a path that is not there.
    """
    try:
        status = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(status.st_mode) or bool(getattr(status, 'st_file_attributes', 0) & REPARSE_POINT_ATTRIBUTE)


def files_and_links_under(root: str | os.PathLike, folders, with_root_files: bool) -> tuple[list[str], list[str]]:
    """What a walk of the disk finds: the files under the named folders and, if asked, the files that lie
    directly in the root; and, apart, every link met on the way. Git is not asked what exists.

    root              the tree's root folder
    folders           folders from the root, for example ('src', 'results/research'); one that is not there
                      contributes nothing
    with_root_files   True to add the files lying directly in the root (not its other folders)
    Returns (files, links), each a sorted list of paths from the root with forward slashes, for example
    (['LICENSE', 'src/research/reader.py'], ['results/research']).
    A link is never entered and never read: a named folder that is a link, or lies under one, is not walked; a
    folder or a file met in the walk that is a link is set apart. Python's cache folders are not entered.
    """
    root = Path(root)
    files, links = [], []
    if with_root_files:
        for entry in os.scandir(root):
            if is_link(entry.path):
                # A link in the root counts only if it stands where a file would: the root's other folders are
                # not this walk's business, and a named folder is checked below.
                if not os.path.isdir(entry.path):
                    links.append(entry.name)
            elif not entry.is_dir(follow_symlinks=False):
                files.append(entry.name)
    for folder in folders:
        parts = [part for part in as_root_path(folder).split('/') if part not in ('', '.')]
        linked_part = next(('/'.join(parts[:count]) for count in range(1, len(parts) + 1)
                            if is_link(root.joinpath(*parts[:count]))), None)
        if linked_part is not None:
            links.append(linked_part)
            continue
        for current, subfolders, names in os.walk(root / folder):
            def from_root(name: str) -> str:
                return as_root_path(os.path.relpath(os.path.join(current, name), root))
            kept = []
            for name in sorted(subfolders):
                if is_link(os.path.join(current, name)):
                    links.append(from_root(name))
                elif name not in NEVER_WALKED_FOLDERS:
                    kept.append(name)
            subfolders[:] = kept
            for name in names:
                (links if is_link(os.path.join(current, name)) else files).append(from_root(name))
    return sorted(files), sorted(set(links))


def files_under(root: str | os.PathLike, folders, with_root_files: bool) -> list[str]:
    """The files a walk of the disk finds: everything under the named folders and, if asked, the files that lie
    directly in the root. Git is not asked what exists.

    root, folders, with_root_files    as for files_and_links_under
    Returns the paths from the root with forward slashes, sorted, for example ['LICENSE', 'src/research/reader.py'].
    Refuses (FileFormRefused) when the walk meets a link, a junction or another reparse point: the project's own
    folders hold none, and what lies behind one is not the tree's to read.
    """
    files, links = files_and_links_under(root, folders, with_root_files)
    if links:
        raise FileFormRefused(f'{len(links)} link(s), junction(s) or other reparse point(s) lie where only the '
                              f'project\'s own files and folders belong, the first at {links[0]}. Nothing behind a '
                              f'link was entered or read. Remove the link (never what it points to), or tell '
                              f'Claude what it is.')
    return files


def describe(faults: list[Fault]) -> str:
    """What the checker prints for a list of faults: each file and what is wrong, the rule with its exception, and
    what to do.

    faults  what faults_of_files returned
    Returns the text, several lines joined by '\\n'; for no faults, one line saying that every file conforms,
    then the rule. The rule's one exception is always said (standard section 3).
    """
    if not faults:
        return 'Every file checked is in the form the standard gives it.\n' + RULE_IN_SHORT
    lines = [f'{len(faults)} fault(s) against the standard for the form of files:']
    lines.extend(f'  {fault.path}: {fault.what}' for fault in faults)
    lines.extend([RULE_IN_SHORT, WHAT_TO_DO])
    return '\n'.join(lines)


def to_form(data: bytes, form: str) -> bytes:
    """Bring some bytes to their form by changing line endings and nothing else.

    data    the whole content of a file
    form    CRLF or LF
    Returns the new bytes; the same bytes when they conform already. A last line with no line ending keeps none:
    no line ending is added or removed, only changed.
    Refuses (FileFormRefused) bytes that hold a zero byte, that do not read as UTF-8, or that hold a carriage
    return no line feed follows: whether that is a line ending cannot be known, so it is never guessed.
    """
    for fault in faults_in_bytes(data, form):
        if 'zero byte' in fault or 'UTF-8' in fault or 'no line feed follows' in fault:
            raise FileFormRefused(f'the content {fault}; nothing was changed')
    if _BARE_CR.search(data):
        raise FileFormRefused('the content holds a carriage return that no line feed follows; whether it ends a '
                              'line cannot be known; nothing was changed')
    line_feed_only = data.replace(b'\r\n', b'\n')
    return line_feed_only.replace(b'\n', b'\r\n') if form == CRLF else line_feed_only


def differ_in_line_endings_only(old: bytes, new: bytes) -> bool:
    """Whether two contents are the same but for their line endings: the proof the conversion gives for each file.

    old, new    two whole contents
    Returns True when, with every CRLF read as LF, the two are byte for byte the same; otherwise False.
    """
    return old.replace(b'\r\n', b'\n') == new.replace(b'\r\n', b'\n')


def _called_name(call: ast.Call) -> str:
    """The last name of what a call calls: 'open' for open(...), io.open(...) and path.open(...)."""
    function = call.func
    return function.attr if isinstance(function, ast.Attribute) else getattr(function, 'id', '')


def _keyword(call: ast.Call, name: str) -> ast.expr | None:
    """The value given to one keyword of a call, or None when the call does not give it."""
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def _mode_of(call: ast.Call, position: int) -> tuple[bool, str]:
    """The mode a call names, as (known, mode).

    call        the call
    position    where the mode stands among the positional arguments (1 for open(file, mode))
    Returns (True, 'w') when the mode is written out as text; (True, '') when none is given (open() then reads);
    (False, '') when a mode is given but is not written-out text, so that what it is cannot be read here.
    """
    mode = _keyword(call, 'mode')
    if mode is None and len(call.args) > position:
        mode = call.args[position]
    if mode is None:
        return True, ''
    if isinstance(mode, ast.Constant) and isinstance(mode.value, str):
        return True, mode.value
    return False, ''


def _is_os_open(call: ast.Call) -> bool:
    """Whether a call is os.open(...): the low-level open, which takes flags, gives a descriptor and writes
    only the bytes it is handed, so it has no line ending of its own to name."""
    function = call.func
    return (isinstance(function, ast.Attribute) and function.attr == 'open'
            and isinstance(function.value, ast.Name) and function.value.id == 'os')


def _writes_text(known: bool, mode: str) -> bool:
    """Whether a mode opens a text file for writing; a mode that cannot be read counts as one, to be safe."""
    return not known or ('b' not in mode and any(letter in mode for letter in _WRITING_MODE_LETTERS))


def writes_without_a_named_line_ending(python_source: str) -> list[tuple[int, str]]:
    """Read Python source and find each place that writes a text file without saying which line ending it writes
    (standard section 4). Such a write gives CRLF on Windows and LF elsewhere.

    python_source   the text of a .py file
    Returns a list of (line number, what was found), in the order of the lines, empty when there is none; for
    example [(41, "open() in mode 'w' without newline=")].
    Found: open(), io.open(), os.fdopen() and a path's .open() in a writing text mode without newline=; a path's
    .write_text() without newline=; a temporary file opened in a writing text mode without newline=; and
    logging's FileHandler, which cannot name one. A file written in binary names its bytes itself and is not
    found. Refuses (SyntaxError) source that Python cannot read.
    """
    found = []
    for node in ast.walk(ast.parse(python_source)):
        if not isinstance(node, ast.Call) or _is_os_open(node):
            continue
        name = _called_name(node)
        has_newline = _keyword(node, 'newline') is not None
        if name in _OPEN_LIKE_NAMES and not has_newline:
            # A path's .open(mode) has the mode first; open(file, mode) and os.fdopen(fd, mode) have it second.
            is_method_of_a_path = (isinstance(node.func, ast.Attribute) and name == 'open'
                                   and not (isinstance(node.func.value, ast.Name)
                                            and node.func.value.id in _MODULES_WITH_AN_OPEN))
            known, mode = _mode_of(node, 0 if is_method_of_a_path else 1)
            if _writes_text(known, mode):
                found.append((node.lineno, f'{name}() in mode {mode!r} without newline=' if known
                              else f'{name}() with a mode that is not written out, without newline='))
        elif name == 'write_text' and not has_newline:
            found.append((node.lineno, 'write_text() without newline='))
        elif name in _TEMPORARY_FILE_NAMES and not has_newline:
            known, mode = _mode_of(node, 0)
            if (known and mode and _writes_text(known, mode)) or not known:
                found.append((node.lineno, f'{name}() in a writing text mode without newline='))
        elif name in _ALWAYS_PLATFORM_NAMES:
            found.append((node.lineno, f'{name}() writes the platform\'s own line ending'))
    return sorted(found)
