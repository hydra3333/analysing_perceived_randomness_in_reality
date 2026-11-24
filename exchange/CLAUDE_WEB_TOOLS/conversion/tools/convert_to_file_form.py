#!/usr/bin/env python3
"""The conversion program of the project's file-form standard: brings the DEV tree's own files to their form
(line endings), safely, once.

What this file is for
    The project's standard (doc/FILE_FORM_STANDARD_v0_1.md, RAT-47) gives every text file of the living project
    the Windows form, CRLF, and every line-record file (.jsonl) LF. This program brings an existing DEV tree to
    it. It walks the tree's own folders itself and never asks Git anything. Before it changes anything it prints
    what it found, class by class, and waits for the owner's typed word. A file on the conversion list is
    converted only if its SHA-256 is the list's "before"; one that already has the list's "after" is passed
    over; any other value stops the run before anything is changed. It changes line endings and nothing else,
    and proves that for each file. DEV's research results, status files and control-folder leftovers are not
    converted: they are removed, on a second typed word, to be written afresh by the engine. The results masters
    and their ledgers are read and proved untouched. There is no undo: the way back is the owner's own copy of
    the project folder, which this program checks before it changes anything, and on a second run checks
    against the hashes recorded at the first run, not against files it has already converted.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_1.md section 7 (the conversion), with sections 3, 3A and 3B; the reviewer's
    watchpoint of EX_305 on a resumed run.

Which of the project's own modules it uses
    file_form (the copy that lies beside this program, checked by its SHA-256 against the conversion list
    before it is used; it is byte for byte the deploy/file_form.py the package delivers)
              form_of, to_form, differ_in_line_endings_only, faults_in_bytes, faults_of_files, files_under,
              is_left_out_by_name: the standard's one rule

What uses it
    The project owner, in DEV, from the conversion's sheet, on his own go; and its tests. Usage:
        python convert_to_file_form.py --tree <tree root> --list <conversion list .json>
                                       --copy <the owner's copy: a folder or a .zip> --record <record .json>
        ... --look      print what would be done and change nothing (no copy or record is needed, and the
                        package's files need not have been copied into the tree yet)
    Standard library only. It ends no process, changes no date or time, and contacts nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Python must leave no compiled copy of the rule beside it, in a look as in a run: a look writes nothing at all.
sys.dont_write_bytecode = True

# What the two documents say they are, so that a file of another kind is never taken for one.
LIST_KIND = 'FILE_FORM_CONVERSION_LIST_V1'
RECORD_KIND = 'FILE_FORM_CONVERSION_RECORD_V1'
# The standard's rule, as the package delivers it into a tree, from the tree root. The copy this program uses
# lies beside it under the same file name, and must have the SHA-256 the list gives for this path.
RULE_MODULE = 'deploy/file_form.py'
RULE_FILE_NAME = 'file_form.py'
# The tree's own settings file: made by hand, in no list, converted by rule (standard section 7).
SETTINGS_FILE = 'ENVIRONMENT.ini'
# The folders this program walks, from the tree root: the living project's own places (standard section 2).
# Nothing else of the tree is entered: not .venv, not .git, not the frozen history, not transitory_data.
WALKED_FOLDERS = ('src', 'deploy', 'tests', '.claude', '.vscode', 'CLAUDE_CODE_WORKING_FOLDER_TREE/tools',
                  'source_data', 'results/research', 'results/research_set_aside', 'records', 'scratch')
# Made again, not converted: everything under these folders is removed on the owner's word ...
REMOVED_FOLDERS = ('results/research/', 'results/research_set_aside/', 'records/')
# ... and every variant's status file, wherever it lies under the methods folder.
STATUS_FILE_NAME = 'VARIANT_STATUS.ini'
METHODS_FOLDER = 'src/methods/'
# The only thing a status file of DEV may say: a withdrawal or an eligibility draw is a fact that cannot be made
# again, so a file holding one stops the run for the owner's decision.
PLAIN_STATUS_LINE = 'status = ACTIVE'
RECORDED_FACT_PREFIXES = ('withdrawn_', 'prevailing_ov1_')
# Untouched, and proved untouched: the results masters and their ledgers, by the ends of their names.
PROVED_UNTOUCHED_ENDINGS = ('_results_master.csv', '_results_master_ledger.csv')
# Untouched, and not read: the updater's grabs and backups, and the two Mode H opening records.
UNTOUCHED_FOLDERS = ('source_data/grabs/', 'source_data/backups/')
UNTOUCHED_PREFIX = 'source_data/HOLDOUT_OPENED_'
# The two locks held while the program works, exactly where the engine and the updater make their own.
JOB_LOCK = 'records/JOB.lock'
UPDATER_LOCK = 'source_data/.results_master.lock'
# The words the owner types.
WORD_TO_CONVERT = 'CONVERT'
WORD_TO_REMOVE = 'REMOVE'
# The ending of the temporary name a converted file is written under before one rename puts it in place.
TEMPORARY_SUFFIX = '.converting'
# A file in the owner's copy that marks the copy's top folder: it exists in every tree this program is run in.
COPY_MARKER = 'src/research_command.py'
# How much of a file is read at a time when it is only hashed.
HASH_BLOCK_BYTES = 1024 * 1024
# How many names of a long class are printed before the rest are counted.
NAMES_SHOWN = 12
# The exit codes.
EXIT_DONE, EXIT_STOPPED, EXIT_NOT_CONFIRMED = 0, 1, 2


class ConversionStopped(Exception):
    """The run cannot go on. The message says what was found, where, and what to do."""


@dataclass
class Survey:
    """What the walk found, class by class. Every path is from the tree root with forward slashes.

    to_convert          listed files whose SHA-256 is the list's "before", for example ['src/a.py']
    already_converted   listed files whose SHA-256 is the list's "after"
    awaiting_package    listed files that the package itself delivers and that are not yet in this tree in
                        that form: for a look, something to know; for a run, a problem
    settings            {'ENVIRONMENT.ini': (sha256 now, sha256 it will have)} or {} when there is none
    to_remove           files made again, not converted: {'results/research/...': sha256 now}
    proved_untouched    the results masters and ledgers: {'source_data/POWERBALL_results_master.csv': sha256}
    untouched           how many files were recognised as untouched and not read (the six left out by name,
                        the grabs, the backups, the opening records, binary kinds)
    problems            what stops the run, each a plain sentence naming the file
    """
    to_convert: list = field(default_factory=list)
    already_converted: list = field(default_factory=list)
    awaiting_package: list = field(default_factory=list)
    settings: dict = field(default_factory=dict)
    to_remove: dict = field(default_factory=dict)
    proved_untouched: dict = field(default_factory=dict)
    untouched: int = 0
    problems: list = field(default_factory=list)


def sha256_of_file(path: Path) -> str:
    """The SHA-256 of a file's bytes as 64 hexadecimal characters, read a block at a time."""
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(HASH_BLOCK_BYTES), b''):
            digest.update(block)
    return digest.hexdigest()


def sha256_of(data: bytes) -> str:
    """The SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def read_list(list_path: Path) -> tuple:
    """Read the conversion list and check that it is one.

    list_path   the list, a JSON document made by make_conversion_list.py
    Returns ({path: entry}, the list's own SHA-256), for example
    ({'src/a.py': {'path': 'src/a.py', 'form': 'CRLF', 'sha256_before': 'ab..', 'sha256_after': 'cd..'}}, 'ef..').
    Refuses (ConversionStopped) a file that is missing, is not JSON, is not a conversion list, or names a path
    twice.
    """
    try:
        data = Path(list_path).read_bytes()
        document = json.loads(data.decode('ascii'))
    except (OSError, ValueError) as error:
        raise ConversionStopped(f'the conversion list {list_path} could not be read ({error}). Give --list the '
                                f'file CONVERSION_LIST.json of the package.') from None
    if not isinstance(document, dict) or document.get('kind') != LIST_KIND:
        raise ConversionStopped(f'{list_path} is not a conversion list (its "kind" is not {LIST_KIND}). Give --list '
                                f'the file CONVERSION_LIST.json of the package.')
    entries = {entry['path']: entry for entry in document['files']}
    if len(entries) != len(document['files']):
        raise ConversionStopped(f'{list_path} names a file twice. Use the list exactly as the package holds it.')
    return entries, sha256_of(data)


def load_rule(rule_path: Path, entries: dict):
    """Load the standard's rule, after checking that it is the file the list expects.

    rule_path   the copy of file_form.py to use (the one beside this program)
    entries     the conversion list, as read_list returns it
    Returns the module file_form. Refuses (ConversionStopped) when that file is missing or is not byte for byte
    the deploy/file_form.py the list names: the program, the rule and the list must be of one package.
    """
    path = Path(rule_path)
    wanted = entries.get(RULE_MODULE, {}).get('sha256_after')
    found = sha256_of_file(path) if path.is_file() else None
    if wanted is None or found != wanted:
        raise ConversionStopped(f'{path} is not the rule the conversion list expects (found '
                                f'{found or "no such file"}). Use the program, the file {RULE_FILE_NAME} beside it '
                                f'and the list exactly as one package holds them.')
    specification = importlib.util.spec_from_file_location('file_form', path)
    module = importlib.util.module_from_spec(specification)
    sys.modules['file_form'] = module
    specification.loader.exec_module(module)
    return module


def status_file_problem(data: bytes) -> str | None:
    """Whether a status file of DEV holds anything but ACTIVE.

    data    the file's bytes, in the old form or the new
    Returns None when every "status" line says ACTIVE and no withdrawal or eligibility draw is recorded;
    otherwise a few words saying what was found, for example 'it records "withdrawn_from_draw = 1601"'.
    """
    try:
        lines = data.decode('ascii').splitlines()
    except UnicodeDecodeError:
        return 'it is not plain text'
    for line in lines:
        line = line.strip()
        if line.startswith('status') and line != PLAIN_STATUS_LINE:
            return f'it says "{line}"'
        if line.startswith(RECORDED_FACT_PREFIXES):
            return f'it records "{line}"'
    return None


def look_at_tree(tree: Path, entries: dict, rule) -> Survey:
    """Walk the tree's own folders and sort every file into its class. Reads only.

    tree        the tree root
    entries     the conversion list
    rule        the module file_form
    Returns a Survey. Nothing is changed. A file that fits no class, a listed file that is missing or has a
    third SHA-256, a status file that holds more than ACTIVE, and a results file that is not in its form are
    each a problem, named. A file the package itself delivers, not yet in the tree in that form, is set apart
    (awaiting_package): the caller decides what that means.
    """
    survey = Survey()
    found = rule.files_under(tree, WALKED_FOLDERS, with_root_files=True)
    for path in sorted(set(entries) - set(found)):
        if entries[path].get('delivered_by_package'):
            survey.awaiting_package.append(path)
            continue
        survey.problems.append(f'{path}: on the conversion list but not in the tree. Nothing may be missing; put '
                               f'the file back from your copy or tell Claude.')
    for path in found:
        full = tree / path
        name = path.rsplit('/', 1)[-1]
        if path in entries:
            digest = sha256_of_file(full)
            if digest == entries[path]['sha256_after']:
                survey.already_converted.append(path)
            elif digest == entries[path]['sha256_before']:
                survey.to_convert.append(path)
            elif entries[path].get('delivered_by_package'):
                survey.awaiting_package.append(path)
            else:
                survey.problems.append(f'{path}: its SHA-256 is neither the list\'s "before" nor its "after" '
                                       f'({digest}). The file differs from the one the list was made from: it '
                                       f'was edited here, or the tree is not at the list\'s commit.')
        elif path in (JOB_LOCK, UPDATER_LOCK):
            survey.problems.append(f'{path}: a lock file exists. A job or a results update is running, or one was '
                                   f'killed and left it. When you are sure nothing of the project is running, '
                                   f'delete that one file by hand and run this again.')
        elif path == SETTINGS_FILE:
            data = full.read_bytes()
            try:
                survey.settings[path] = (sha256_of(data), sha256_of(rule.to_form(data, rule.CRLF)))
            except rule.FileFormRefused as refusal:
                survey.problems.append(f'{path}: {refusal}')
        elif path.startswith(REMOVED_FOLDERS) or (path.startswith(METHODS_FOLDER) and name == STATUS_FILE_NAME):
            if name == STATUS_FILE_NAME:
                fault = status_file_problem(full.read_bytes())
                if fault:
                    survey.problems.append(f'{path}: {fault}. A status file of DEV is removed and made again only '
                                           f'while it says nothing but ACTIVE; this one holds a fact that cannot '
                                           f'be made again. It is your decision: tell Claude.')
                    continue
            survey.to_remove[path] = sha256_of_file(full)
        elif path.startswith('source_data/') and path.endswith(PROVED_UNTOUCHED_ENDINGS):
            faults = rule.faults_of_file(tree, path)
            if faults:
                survey.problems.append(f'{path}: {faults[0].what}. The results files are never converted; this '
                                       f'one was expected to be in its form already. Tell Claude.')
            survey.proved_untouched[path] = sha256_of_file(full)
        elif (rule.is_left_out_by_name(path) or path.startswith(UNTOUCHED_FOLDERS)
              or path.startswith(UNTOUCHED_PREFIX) or rule.form_of(path) == rule.BINARY):
            survey.untouched += 1
        else:
            kind = 'a text file' if rule.form_of(path) else 'a file of a kind the standard does not name'
            survey.problems.append(f'{path}: {kind} that is in no class this program knows (not on the list, not '
                                   f'the settings file, not a result made again, not a results file). Move it '
                                   f'out of the project folder, or tell Claude what it is.')
    return survey


def shown(paths, limit: int = NAMES_SHOWN) -> str:
    """Some names for the screen: the first few, each on its own line, and a count of the rest."""
    paths = list(paths)
    lines = [f'      {path}' for path in paths[:limit]]
    if len(paths) > limit:
        lines.append(f'      ... and {len(paths) - limit} more')
    return '\n'.join(lines)


def describe_survey(survey: Survey, entries: dict, say) -> None:
    """Print what the walk found, class by class (standard section 7: before anything is changed)."""
    say(f'  LISTED, to be converted now ............ {len(survey.to_convert)} file(s) of the {len(entries)} listed')
    say(f'  LISTED, in their form already .......... {len(survey.already_converted)} file(s) (passed over)')
    if survey.awaiting_package:
        say(f'  THE PACKAGE\'S OWN FILES, not yet here .. {len(survey.awaiting_package)} file(s) (the package '
            f'delivers them in their form; they are copied in before a real run)')
    for path, (now, then) in survey.settings.items():
        say(f'  THE TREE\'S OWN SETTINGS ................ {path}: '
            + ('in its form already' if now == then else 'to be converted (line endings only)'))
    say('  MADE AGAIN, NOT CONVERTED (removed on your second word; the engine writes them afresh):')
    say(f'      {len(survey.to_remove)} file(s): research results, status files, control-folder leftovers')
    if survey.to_remove:
        say(shown(survey.to_remove))
    say(f'  UNTOUCHED, AND PROVED UNTOUCHED ........ {len(survey.proved_untouched)} results file(s):')
    for path, digest in survey.proved_untouched.items():
        say(f'      {digest}  {path}')
    say(f'  UNTOUCHED, NOT READ .................... {survey.untouched} file(s) (the six left out by name, the '
        f'updater\'s grabs and backups, the opening records, binary kinds)')
    say(f'  IN NO CLASS, OR NOT AS EXPECTED ........ {len(survey.problems)}')
    for problem in survey.problems:
        say(f'      {problem}')


class OwnersCopy:
    """The owner's pre-conversion copy of the project folder: a folder, or a ZIP of it. Read only.

    Use sha256_of(path) with a path from the tree root; it returns the SHA-256 of that file in the copy, or None
    when the copy does not hold it.
    """

    def __init__(self, place: Path):
        """place: the copy. Refuses (ConversionStopped) one that is not there or is not a copy of the project."""
        self.place = Path(place)
        self.archive = None
        self.prefix = ''
        if self.place.is_dir():
            if not (self.place / COPY_MARKER).is_file():
                raise ConversionStopped(f'{self.place} does not look like a copy of the project folder: it has no '
                                        f'{COPY_MARKER}. Give --copy the folder that holds src, tests and deploy.')
        elif self.place.is_file() and zipfile.is_zipfile(self.place):
            self.archive = zipfile.ZipFile(self.place)
            self.members = set(self.archive.namelist())
            tops = sorted((name[:-len(COPY_MARKER)] for name in self.members if name.endswith(COPY_MARKER)), key=len)
            if not tops:
                raise ConversionStopped(f'{self.place} does not look like a ZIP of the project folder: it holds no '
                                        f'{COPY_MARKER}.')
            self.prefix = tops[0]
        else:
            raise ConversionStopped(f'{self.place} is neither a folder nor a ZIP file. Give --copy your copy of '
                                    f'the project folder, made before this conversion.')

    def sha256_of(self, path: str) -> str | None:
        """The SHA-256 of one file of the copy, or None when the copy does not hold it."""
        if self.archive is None:
            full = self.place / path
            return sha256_of_file(full) if full.is_file() else None
        member = self.prefix + path
        if member not in self.members:
            return None
        digest = hashlib.sha256()
        with self.archive.open(member) as handle:
            for block in iter(lambda: handle.read(HASH_BLOCK_BYTES), b''):
                digest.update(block)
        return digest.hexdigest()


def read_record(record_path: Path, tree: Path, list_sha256: str) -> dict | None:
    """Read the record of an earlier, unfinished or finished run, if there is one.

    Returns the record (a dictionary), or None when there is no file. Refuses (ConversionStopped) a record that
    cannot be read, or that belongs to another tree or another list: it must never be mixed with this run.
    """
    if not Path(record_path).exists():
        return None
    try:
        record = json.loads(Path(record_path).read_bytes().decode('ascii'))
    except (OSError, ValueError) as error:
        raise ConversionStopped(f'the record {record_path} could not be read ({error}). Do not delete it: send it '
                                f'to Claude.') from None
    if (record.get('kind') != RECORD_KIND or record.get('tree') != str(tree)
            or record.get('conversion_list_sha256') != list_sha256):
        raise ConversionStopped(f'the record {record_path} is of another tree or another conversion list. Give '
                                f'--record the file of this conversion, or a new name for a first run.')
    return record


def write_record(record_path: Path, record: dict, rule) -> None:
    """Write the record whole, in the standard's form (CRLF), under a temporary name and then one rename."""
    text = json.dumps(record, indent=1, ensure_ascii=True, sort_keys=True) + '\n'
    record_path = Path(record_path)
    record_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = record_path.with_name(record_path.name + TEMPORARY_SUFFIX)
    with open(temporary, 'wb') as handle:
        handle.write(rule.to_form(text.encode('ascii'), rule.CRLF))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, record_path)


def check_copy(copy: OwnersCopy, originals: dict) -> list:
    """Check that the owner's copy holds every original this conversion changes or removes.

    originals   {path: the SHA-256 the file had before the conversion's first run}
    Returns a list of problems, empty when the copy holds every file with exactly that SHA-256. On a second run
    the originals are the first run's recorded hashes, never the hashes of files already converted (EX_305).
    """
    problems = []
    for path, wanted in sorted(originals.items()):
        found = copy.sha256_of(path)
        if found is None:
            problems.append(f'{path}: not in your copy.')
        elif found != wanted:
            problems.append(f'{path}: your copy holds other bytes ({found}) than the tree held before the '
                            f'conversion ({wanted}).')
    return problems


class HeldLock:
    """One lock file, made by an exclusive create and removed when the work ends, as the engine makes its own.

    Use it as `with HeldLock(path, rule):`. Refuses (ConversionStopped) if the file already exists.
    """

    def __init__(self, path: Path, rule):
        """path: the lock file.  rule: the module file_form, for the form of the one line written into it."""
        self.path, self.rule = Path(path), rule

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise ConversionStopped(f'{self.path} exists: a job or a results update is running, or one was killed '
                                    f'and left it. When you are sure nothing of the project is running, delete '
                                    f'that one file by hand and run this again.') from None
        line = f'file-form conversion; process {os.getpid()}\n'.encode('ascii')
        os.write(descriptor, self.rule.to_form(line, self.rule.CRLF))
        os.close(descriptor)
        return self

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def convert_one(tree: Path, path: str, form: str, before: str, after: str, rule) -> None:
    """Convert one file: line endings only, proved, written under a temporary name and renamed into place.

    tree, path  the file.  form: CRLF or LF.  before, after: the SHA-256 it must have now and afterwards.
    Refuses (ConversionStopped) and leaves the file exactly as it was when its bytes are no longer the "before",
    when the converted bytes are not the "after", or when more than line endings would change. A failure of
    Windows to write or rename (the file is open in another program) is an OSError for the caller.
    """
    full = tree / path
    old = full.read_bytes()
    if sha256_of(old) != before:
        raise ConversionStopped(f'{path} changed while this program ran (it no longer has the SHA-256 it had '
                                f'when it was looked at). Nothing was written to it. Close every other program '
                                f'of the project and run this again.')
    new = rule.to_form(old, form)
    if not rule.differ_in_line_endings_only(old, new) or sha256_of(new) != after:
        raise ConversionStopped(f'{path}: the converted bytes are not the ones the conversion list expects. '
                                f'Nothing was written to it. Send this line to Claude.')
    temporary = full.with_name(full.name + TEMPORARY_SUFFIX)
    with open(temporary, 'wb') as handle:
        handle.write(new)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, full)
    if sha256_of_file(full) != after:
        raise ConversionStopped(f'{path} was written but does not read back as written. Stop here and send this '
                                f'line to Claude; your copy holds the original.')


def remove_listed(tree: Path, paths, checkpoint) -> int:
    """Remove exactly the named files, then every folder under the removed places that is left empty.

    paths       the files to remove, from the tree root
    checkpoint  called with each path just before it is removed (a test plants a failure here)
    Returns how many files were removed. A file that is already gone is passed over.
    """
    removed = 0
    for path in sorted(paths):
        checkpoint(path)
        try:
            (tree / path).unlink()
            removed += 1
        except FileNotFoundError:
            pass
    for folder in REMOVED_FOLDERS:
        for current, _folders, _names in os.walk(tree / folder, topdown=False):
            if not os.listdir(current) and Path(current) != tree / 'records':
                os.rmdir(current)
    return removed


def run(tree, list_path, copy_place=None, record_path=None, look_only=False, ask=input, say=print,
        now=datetime.now, checkpoint=lambda path: None, rule_path=None) -> int:
    """The whole conversion of one tree.

    tree            the tree root.  list_path: the conversion list.  copy_place: the owner's copy (a folder or a
                    ZIP).  record_path: where the conversion's record is kept (outside the folders it changes).
    look_only       True to print what would be done and change nothing
    ask, say        how a question is asked and a line printed (a test passes its own)
    now             gives the present time, for the record only.  checkpoint: called before each file is changed
    rule_path       the copy of file_form.py to use; None for the one beside this program
    Returns EXIT_DONE when the tree is converted (or, with look_only, when the look found nothing to stop it);
    EXIT_NOT_CONFIRMED when the owner did not type the word; EXIT_STOPPED on anything else.
    """
    tree = Path(tree).resolve()
    say(f'FILE-FORM CONVERSION - START - the tree at {tree}'
        + (' - LOOK ONLY: nothing will be changed' if look_only else ''))
    try:
        entries, list_sha256 = read_list(Path(list_path))
        say(f'  The conversion list: {len(entries)} files; its SHA-256 is {list_sha256}')
        rule = load_rule(rule_path or Path(__file__).with_name(RULE_FILE_NAME), entries)
        if look_only:
            return _look(tree, entries, rule, say)
        if not copy_place or not record_path:
            raise ConversionStopped('--copy and --record are both needed for a run that changes anything.')
        with HeldLock(tree / JOB_LOCK, rule), HeldLock(tree / UPDATER_LOCK, rule):
            return _convert(tree, entries, list_sha256, rule, Path(copy_place), Path(record_path), ask, say, now,
                            checkpoint)
    except ConversionStopped as stop:
        say(f'STOP: {stop}')
    except OSError as failure:
        say(f'STOP: Windows refused to read or write a file: {failure}. Each file is the old one or the new one, '
            f'whole. Close every other program that has a file of the project open and run this again; it goes '
            f'on from where it stopped.')
    say('FILE-FORM CONVERSION - END - STOPPED. Read the STOP line above. Nothing is half-written.')
    return EXIT_STOPPED


def _look(tree: Path, entries: dict, rule, say) -> int:
    """The look-only run: the walk and its print-out, with no lock taken and nothing changed."""
    survey = look_at_tree(tree, entries, rule)
    # A look takes no lock, so a lock file that exists is reported like any other finding.
    describe_survey(survey, entries, say)
    if survey.problems:
        say('FILE-FORM CONVERSION - END - LOOKED ONLY; nothing was changed. The findings above would stop a real '
            'run before it changed anything.')
        return EXIT_STOPPED
    say('FILE-FORM CONVERSION - END - LOOKED ONLY; nothing was changed. A real run would find nothing to stop it.')
    return EXIT_DONE


def _convert(tree, entries, list_sha256, rule, copy_place, record_path, ask, say, now, checkpoint) -> int:
    """The run that changes the tree, with both locks held. See run() for the parameters and the result."""
    own_locks = {JOB_LOCK, UPDATER_LOCK}
    survey = look_at_tree(tree, entries, _WithoutOwnLocks(rule, own_locks))
    describe_survey(survey, entries, say)
    if survey.awaiting_package:
        raise ConversionStopped(f'{len(survey.awaiting_package)} of the package\'s own files are not in this tree '
                                f'as the package delivers them (the first: {survey.awaiting_package[0]}). Copy '
                                f'the package\'s files into the tree first, as the sheet says. Nothing was changed.')
    if survey.problems:
        raise ConversionStopped(f'{len(survey.problems)} finding(s) above. Nothing was changed.')
    record = read_record(record_path, tree, list_sha256)
    if record is None:
        originals = {path: entries[path]['sha256_before'] for path in survey.to_convert}
        originals.update({path: now_sha for path, (now_sha, then_sha) in survey.settings.items()
                          if now_sha != then_sha})
        record = {'kind': RECORD_KIND, 'tree': str(tree), 'conversion_list_sha256': list_sha256,
                  'first_run_started': now().strftime('%Y-%m-%d %H:%M:%S'), 'finished': None,
                  'originals_converted': originals, 'originals_removed': dict(survey.to_remove),
                  'settings_file': {path: {'sha256_before': a, 'sha256_after': b}
                                    for path, (a, b) in survey.settings.items()},
                  'proved_untouched': dict(survey.proved_untouched)}
        say('  This is a first run: the SHA-256 of every file to be changed or removed is recorded before '
            'anything is changed.')
    else:
        say(f'  This is a second run of a conversion begun {record["first_run_started"]}: your copy is checked '
            f'against the hashes recorded then, not against files already converted.')
        unknown = [path for path in list(survey.to_convert) + list(survey.to_remove)
                   if path not in record['originals_converted'] and path not in record['originals_removed']]
        if unknown:
            raise ConversionStopped(f'{len(unknown)} file(s) to change now were not there, or not to be changed, '
                                    f'at the first run (the first: {unknown[0]}). Something was added or put '
                                    f'back since. Nothing was changed. Tell Claude.')
    copy = OwnersCopy(copy_place)
    problems = check_copy(copy, {**record['originals_converted'], **record['originals_removed']})
    if problems:
        for problem in problems[:NAMES_SHOWN]:
            say(f'      {problem}')
        raise ConversionStopped(f'your copy at {copy_place} does not hold {len(problems)} of the '
                                f'{len(record["originals_converted"]) + len(record["originals_removed"])} '
                                f'original file(s) this conversion changes or removes. Nothing was changed. The '
                                f'copy is the one way back: make it again from the project folder as it is now '
                                f'only if this is a first run; otherwise tell Claude.')
    say(f'  Your copy holds every one of the {len(record["originals_converted"])} file(s) to be converted and '
        f'the {len(record["originals_removed"])} to be removed, each with the SHA-256 it had before.')
    write_record(record_path, record, rule)
    settings_to_convert = [path for path, (a, b) in survey.settings.items() if a != b]
    if survey.to_convert or settings_to_convert:
        typed = ask(f'Type {WORD_TO_CONVERT} to change the line endings of {len(survey.to_convert)} listed file(s)'
                    + (' and the settings file' if settings_to_convert else '') + ', or anything else to stop: ')
        if typed.strip() != WORD_TO_CONVERT:
            say('FILE-FORM CONVERSION - END - not confirmed; nothing was changed.')
            return EXIT_NOT_CONFIRMED
        for path in survey.to_convert:
            checkpoint(path)
            entry = entries[path]
            convert_one(tree, path, entry['form'], entry['sha256_before'], entry['sha256_after'], rule)
        for path in settings_to_convert:
            checkpoint(path)
            convert_one(tree, path, rule.CRLF, *survey.settings[path], rule)
        say(f'  Converted: {len(survey.to_convert)} listed file(s)'
            + (', and the settings file' if settings_to_convert else '')
            + '. Each differs from what it was in line endings only, and reads back as written.')
    else:
        say('  Nothing is left to convert.')
    if survey.to_remove:
        typed = ask(f'Type {WORD_TO_REMOVE} to remove the {len(survey.to_remove)} file(s) that are made again, not '
                    f'converted (each is in your copy), or anything else to stop here: ')
        if typed.strip() != WORD_TO_REMOVE:
            say('FILE-FORM CONVERSION - END - the files are converted; the removal was not confirmed. Run this '
                'again to remove them; until then the research job refuses the old status files.')
            return EXIT_NOT_CONFIRMED
        removed = remove_listed(tree, survey.to_remove, checkpoint)
        say(f'  Removed: {removed} file(s), and the folders left empty.')
    return _prove(tree, entries, rule, record, record_path, own_locks, say, now)


class _WithoutOwnLocks:
    """The module file_form with one difference: its walk leaves out the two lock files this program itself
    holds, so that they are not taken for another job's."""

    def __init__(self, rule, own_locks):
        self._rule, self._own_locks = rule, own_locks

    def __getattr__(self, name):
        return getattr(self._rule, name)

    def files_under(self, root, folders, with_root_files):
        return [path for path in self._rule.files_under(root, folders, with_root_files)
                if path not in self._own_locks]


def _prove(tree, entries, rule, record, record_path, own_locks, say, now) -> int:
    """The proof at the end: every listed file has the list's "after" and conforms; the results files have the
    SHA-256 they had at the first run; nothing made-again is left. Writes the finished record. Returns the exit
    code."""
    survey = look_at_tree(tree, entries, _WithoutOwnLocks(rule, own_locks))
    faults = rule.faults_of_files(tree, sorted(entries))
    changed_results = [path for path, digest in record['proved_untouched'].items()
                       if survey.proved_untouched.get(path) != digest]
    left = (len(survey.to_convert) + len(survey.to_remove) + len(survey.problems) + len(faults)
            + len(changed_results) + len(survey.awaiting_package))
    if left or any(a != b for a, b in survey.settings.values()):
        for line in ([f'{path}: still to convert' for path in survey.to_convert] + survey.problems
                     + [f'{fault.path}: {fault.what}' for fault in faults]
                     + [f'{path}: a results file changed' for path in changed_results])[:NAMES_SHOWN]:
            say(f'      {line}')
        raise ConversionStopped('the proof at the end did not hold; the lines above say where. Do not go on to '
                                'the next part of the sheet. Send this output to Claude.')
    record['finished'] = now().strftime('%Y-%m-%d %H:%M:%S')
    write_record(record_path, record, rule)
    say(f'  PROVED: all {len(entries)} listed files have the list\'s "after" SHA-256 and are in their form; the '
        f'{len(record["proved_untouched"])} results file(s) have the SHA-256 they had before; nothing made-again '
        f'is left.')
    say(f'  {rule.RULE_IN_SHORT}')
    say(f'  The record: {record_path}')
    say('FILE-FORM CONVERSION - END - FINISHED. Go on with the next part of the sheet.')
    return EXIT_DONE


def main(arguments) -> int:
    """The command line. arguments: for example ['--tree', '.', '--list', 'CONVERSION_LIST.json', '--look'].
    Returns the exit code."""
    parser = argparse.ArgumentParser(description='Bring a DEV tree to the project\'s file-form standard.')
    parser.add_argument('--tree', required=True, help='the tree root (the project folder)')
    parser.add_argument('--list', required=True, dest='list_path', help='the conversion list of the package')
    parser.add_argument('--copy', dest='copy_place', help='your copy of the project folder: a folder or a ZIP')
    parser.add_argument('--record', dest='record_path', help='where the record is kept (outside the tree)')
    parser.add_argument('--look', action='store_true', help='print what would be done and change nothing')
    parser.add_argument('--rule', dest='rule_path', help=f'the copy of {RULE_FILE_NAME} to use (default: beside '
                                                         f'this program)')
    options = parser.parse_args(arguments)
    return run(options.tree, options.list_path, options.copy_place, options.record_path, options.look,
               rule_path=options.rule_path)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
