#!/usr/bin/env python3
"""After the conversion: stages the converted files in Git exactly as they lie on disk, and puts every other
tracked file's working copy back to Git's own bytes, so that what is on disk is what is committed.

What this file is for
    The project's standard says that Git converts nothing: the root .gitattributes says "-text". On the owner's
    PC Git has, until now, written CRLF working copies of files it stores with LF (his core.autocrlf is true).
    Once Git converts nothing, two things must be put right, once, and plain Git commands do not do it: Git
    does not look again at a file whose size and time are unchanged, so it neither stages a converted file it
    believes unchanged nor rewrites a working copy it believes current. This program does both by content, not
    by belief:
      1. each file of the conversion list is staged with exactly the bytes it has on disk, after a check that
         those bytes are the list's "after";
      2. every other tracked file for which Git now converts nothing, and whose bytes on disk differ from Git's
         in line endings only, has its working copy rewritten with Git's own bytes (frozen history goes back to
         exactly what was committed; nothing in Git changes for it).
    It prints what it will do and waits for a typed word; it proves the result; it commits nothing and pushes
    nothing: the owner does that. Unlike the conversion program, this one does call Git: staging a commit is
    what Git is for. It is never a check of whether a tree may run.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_2.md section 5 ("What is on disk is what is committed"; "The owner's working copy
    needs one refresh, on the day"; "the commit is checked: the bytes staged for it are in the standard's form").

Which of the project's own modules it uses
    file_form (the copy beside this program, checked against the conversion list as the conversion program
    checks it)     differ_in_line_endings_only, faults_in_bytes, form_of
    convert_to_file_form (beside this program)     read_list, load_rule, sha256_of, ConversionStopped: the same
                                                   reading of the list and of the rule

What uses it
    The project owner, in DEV, from the conversion's sheet, after the conversion program has finished, on his
    own go; and its tests. Usage:
        python stage_and_refresh.py --tree <tree root> --list <conversion list .json>
        ... --look      print what would be done and change nothing
    Standard library and Git only. It ends no process, changes no date or time, and contacts nothing: it runs
    no Git command that reaches a remote.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Python must leave no compiled copy of the two modules beside it.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import convert_to_file_form as conversion                  # noqa: E402  (after the path line above)

# The word the owner types.
WORD_TO_GO_ON = 'STAGE'
# The ending of the temporary name a working copy is written under before one rename puts it in place.
TEMPORARY_SUFFIX = '.refreshing'
# The value Git reports for the attribute "text" where the root file's "-text" governs a path.
ATTRIBUTE_UNSET = 'unset'
# Another project's own folder, with its own rules for Git: never a candidate here, for staging or for refreshing.
OTHER_PROJECTS = ('GAIS/',)
# What Git already stored byte for byte before this conversion (the old root attribute file's "-text" lines): such
# a file's bytes on disk are Git's own already. One that differs is never put back: it is named, and the run stops.
STORED_BYTE_FOR_BYTE_BEFORE = ('source_data/', 'results/', 'src/methods/_common/contract_data/install_records/',
                               'src/package_tools/process_check.py',
                               'tests/fixtures/results_master_v0_1_reference.py.txt', 'src/results_master_v0_2.py')
# The mode of an ordinary file in Git's index; anything else (a link, a submodule) is not this program's.
ORDINARY_MODES = ('100644', '100755')
# How many names of a long class are printed before the rest are counted.
NAMES_SHOWN = 12
# The exit codes, as the conversion program's.
EXIT_DONE, EXIT_STOPPED, EXIT_NOT_CONFIRMED = 0, 1, 2

Stopped = conversion.ConversionStopped


def git(tree: Path, *arguments: str, given: bytes | None = None) -> bytes:
    """Run one Git command in the tree and return what it printed.

    tree        the repository's folder.  arguments: the command, for example ('ls-files', '-s', '-z')
    given       bytes for the command's standard input, or None
    Refuses (Stopped) when Git is not found or the command fails, with Git's own words.
    """
    try:
        done = subprocess.run(['git', '-C', str(tree), *arguments], input=given, capture_output=True, check=False)
    except OSError as failure:
        raise Stopped(f'Git could not be started ({failure}). Run this in a window where "git" works.') from None
    if done.returncode != 0:
        said = done.stderr.decode('utf-8', 'replace').strip().splitlines()
        raise Stopped(f'git {" ".join(arguments[:2])} failed: {said[-1] if said else "no message"}. Nothing '
                      f'further was done. Send this line to Claude.')
    return done.stdout


def tracked_files(tree: Path) -> dict:
    """Every ordinary tracked file with the id Git's index holds for it: {'src/a.py': ('100644', '3b18e5...')}.
    Refuses (Stopped) an index that holds an unmerged path: a merge is in progress."""
    found = {}
    for record in git(tree, 'ls-files', '-s', '-z').split(b'\0'):
        if not record:
            continue
        head, path = record.split(b'\t', 1)
        mode, blob_id, stage = head.decode('ascii').split()
        if stage != '0':
            raise Stopped(f'{path.decode("utf-8")} is unmerged in Git\'s index: a merge is in progress. Nothing '
                          f'was done. Tell Claude.')
        if mode in ORDINARY_MODES:
            found[path.decode('utf-8')] = (mode, blob_id)
    return found


def ids_of_disk_bytes(tree: Path, paths: list) -> dict:
    """The id Git would give each file's bytes exactly as they lie on disk, with no conversion at all.

    Returns {path: id}; a path that is not on disk has no entry.
    """
    present = [path for path in paths if (tree / path).is_file()]
    if not present:
        return {}
    printed = git(tree, 'hash-object', '--no-filters', '--stdin-paths',
                  given=''.join(path + '\n' for path in present).encode('utf-8'))
    return dict(zip(present, printed.decode('ascii').split()))


def paths_git_converts_nothing_for(tree: Path, paths: list) -> set:
    """Those of the paths for which the attribute "text" is unset: the paths the root file's "-text" governs.
    A path under another project's own rules (text left unspecified or set there) is not among them."""
    if not paths:
        return set()
    printed = git(tree, 'check-attr', '-z', '--stdin', 'text', given='\0'.join(paths).encode('utf-8') + b'\0')
    fields = printed.split(b'\0')
    return {fields[position].decode('utf-8') for position in range(0, len(fields) - 2, 3)
            if fields[position + 2] == ATTRIBUTE_UNSET.encode('ascii')}


def make_plan(tree: Path, entries: dict, rule) -> dict:
    """Read the disk and Git's index, and decide what is to be done. Changes nothing.

    tree, entries, rule     the tree, the conversion list, the module file_form
    Returns {'to_stage': {path: mode}, 'to_refresh': {path: blob id}, 'problems': [...]}:
      to_stage    listed files whose bytes on disk are the list's "after" and are not what the index holds
      to_refresh  other tracked files Git converts nothing for, whose bytes on disk differ from Git's in line
                  endings only
      problems    anything else: a listed file not at its "after"; a tracked file that differs from Git's bytes
                  in more than line endings; a tracked file that is missing
    """
    tracked = tracked_files(tree)
    plan = {'to_stage': {}, 'to_refresh': {}, 'problems': []}
    on_disk = ids_of_disk_bytes(tree, sorted(set(tracked) | set(entries)))
    for path, entry in sorted(entries.items()):
        full = tree / path
        if not full.is_file() or conversion.sha256_of_file(full) != entry['sha256_after']:
            plan['problems'].append(f'{path}: on the conversion list but not at the list\'s "after" on disk. '
                                    f'Run the conversion program to its end first.')
        elif tracked.get(path, (None, None))[1] != on_disk[path]:
            plan['to_stage'][path] = tracked.get(path, ('100644', None))[0]
    others = [path for path in sorted(tracked) if path not in entries and not path.startswith(OTHER_PROJECTS)]
    unconverted = paths_git_converts_nothing_for(tree, others)
    for path in others:
        if path not in on_disk:
            plan['problems'].append(f'{path}: tracked by Git but not on disk. Nothing may be missing; tell Claude.')
        elif on_disk[path] != tracked[path][1] and path.startswith(STORED_BYTE_FOR_BYTE_BEFORE):
            plan['problems'].append(f'{path}: Git stored this file byte for byte before today, and its bytes on '
                                    f'disk are not Git\'s: it was changed here. It is not touched. Tell Claude.')
        elif on_disk[path] != tracked[path][1] and path in unconverted:
            blob = git(tree, 'cat-file', 'blob', tracked[path][1])
            if rule.differ_in_line_endings_only((tree / path).read_bytes(), blob):
                plan['to_refresh'][path] = tracked[path][1]
            else:
                plan['problems'].append(f'{path}: its bytes on disk differ from Git\'s in more than line endings: '
                                        f'it was changed here and not committed. It is not touched. Tell Claude.')
    return plan


def staged_paths(tree: Path) -> set:
    """Every path whose entry in Git's index differs from the last commit: what a commit made now would change."""
    return {name.decode('utf-8') for name in git(tree, 'diff', '--cached', '--name-only', '-z', 'HEAD').split(b'\0')
            if name}


def by_top_folder(paths) -> str:
    """Counts for the screen, by the first folder of each path: 'exchange 2,104; doc 211; (root) 3'."""
    counts = {}
    for path in paths:
        top = path.split('/', 1)[0] if '/' in path else '(root)'
        counts[top] = counts.get(top, 0) + 1
    return '; '.join(f'{top} {count:,}' for top, count in sorted(counts.items(), key=lambda item: -item[1]))


def describe_plan(plan: dict, entries: dict, say) -> None:
    """Print what the plan holds, before anything is changed."""
    say(f'  TO BE STAGED, exactly as on disk ....... {len(plan["to_stage"])} of the {len(entries)} listed file(s) '
        f'(the others are in Git already as they are on disk)')
    say('  WORKING COPIES TO BE PUT BACK to Git\'s own bytes (line endings only; nothing in Git changes):')
    say(f'      {len(plan["to_refresh"])} file(s): {by_top_folder(plan["to_refresh"]) or "none"}')
    say(f'  NOT AS EXPECTED ........................ {len(plan["problems"])}')
    for problem in plan['problems'][:NAMES_SHOWN]:
        say(f'      {problem}')
    if len(plan['problems']) > NAMES_SHOWN:
        say(f'      ... and {len(plan["problems"]) - NAMES_SHOWN} more')


def stage_exactly(tree: Path, to_stage: dict) -> None:
    """Put each file into Git's index with exactly the bytes it has on disk, whatever Git believes of it.

    to_stage    {path: mode}
    The bytes are written into Git's store unconverted, and the index entry is set to that object by name: no
    setting of Git and no remembered size or time has a say.
    """
    paths = sorted(to_stage)
    written = git(tree, 'hash-object', '-w', '--no-filters', '--stdin-paths',
                  given=''.join(path + '\n' for path in paths).encode('utf-8')).decode('ascii').split()
    lines = ''.join(f'{to_stage[path]} {blob_id}\t{path}\n' for path, blob_id in zip(paths, written))
    git(tree, 'update-index', '--add', '--index-info', given=lines.encode('utf-8'))


def refresh_one(tree: Path, path: str, blob_id: str, rule) -> None:
    """Rewrite one working copy with Git's own bytes: under a temporary name, then one rename. Refuses (Stopped)
    and leaves the file as it was if it no longer differs from Git's bytes in line endings only."""
    full = tree / path
    blob = git(tree, 'cat-file', 'blob', blob_id)
    if not rule.differ_in_line_endings_only(full.read_bytes(), blob):
        raise Stopped(f'{path} changed while this program ran. It was not touched.')
    temporary = full.with_name(full.name + TEMPORARY_SUFFIX)
    with open(temporary, 'wb') as handle:
        handle.write(blob)
        handle.flush()
        os.fsync(handle.fileno())
    # The new file keeps the old one's permission bits, so that where Git records them (not on Windows) it
    # sees none changed.
    shutil.copymode(full, temporary)
    os.replace(temporary, full)


def note_refreshed(tree: Path, paths: list) -> None:
    """Have Git read the rewritten working copies again, so that it knows each is what its index holds.

    paths   the files whose working copies were rewritten
    Git remembers each working file's size and time, and takes a changed size for a changed file without
    reading it. Each file is therefore handed to Git once more; its bytes are the index's own, so no entry of
    the index changes its content, only what Git remembers of the file.
    """
    if paths:
        git(tree, 'update-index', '-z', '--stdin', given='\0'.join(paths).encode('utf-8') + b'\0')


def prove(tree: Path, entries: dict, rule, say) -> None:
    """The proof at the end: every listed file is in Git's index with its "after" bytes and in its form; every
    tracked file Git converts nothing for has on disk exactly the bytes the index holds; and Git itself reports
    no file changed on disk and not staged. Refuses (Stopped) otherwise."""
    git(tree, 'update-index', '-q', '--refresh')
    left = make_plan(tree, entries, rule)
    tracked = tracked_files(tree)
    faults = []
    for path, entry in sorted(entries.items()):
        staged = git(tree, 'cat-file', 'blob', tracked[path][1]) if path in tracked else None
        if staged is None or conversion.sha256_of(staged) != entry['sha256_after']:
            faults.append(f'{path}: what is staged is not the list\'s "after"')
        elif rule.faults_in_bytes(staged, rule.form_of(path)):
            faults.append(f'{path}: what is staged is not in its form')
    unstaged = [name.decode('utf-8') for name in git(tree, 'diff-files', '--name-only', '-z').split(b'\0') if name]
    faults.extend(f'{path}: Git still sees a change on disk that is not staged' for path in unstaged)
    faults.extend(f'{path}: staged, but not on the conversion list' for path in sorted(staged_paths(tree) - set(entries)))
    remaining = len(left['to_stage']) + len(left['to_refresh']) + len(left['problems']) + len(faults)
    if remaining:
        for line in (list(left['to_stage']) + list(left['to_refresh']) + left['problems'] + faults)[:NAMES_SHOWN]:
            say(f'      {line}')
        raise Stopped('the proof at the end did not hold; the lines above say where.')
    say(f'  PROVED: all {len(entries)} listed files are staged with the list\'s "after" bytes and are in their '
        f'form; every tracked file Git converts nothing for has on disk exactly the bytes Git holds; Git sees no '
        f'change on disk that is not staged; nothing is staged that is not on the list.')


def run(tree, list_path, look_only=False, ask=input, say=print, checkpoint=lambda path: None,
        rule_path=None) -> int:
    """The whole of it for one tree.

    tree, list_path     the tree root and the conversion list
    look_only           True to print what would be done and change nothing
    ask, say            how a question is asked and a line printed (a test passes its own)
    checkpoint          called with each path before its working copy is rewritten (a test plants a failure)
    rule_path           the copy of file_form.py to use; None for the one beside this program
    Returns EXIT_DONE, EXIT_NOT_CONFIRMED or EXIT_STOPPED.
    """
    tree = Path(tree).resolve()
    say(f'STAGE AND REFRESH - START - the tree at {tree}' + (' - LOOK ONLY: nothing will be changed'
                                                              if look_only else ''))
    try:
        entries, list_sha256 = conversion.read_list(Path(list_path))
        say(f'  The conversion list: {len(entries)} files; its SHA-256 is {list_sha256}')
        rule = conversion.load_rule(rule_path or Path(__file__).with_name(conversion.RULE_FILE_NAME), entries)
        plan = make_plan(tree, entries, rule)
        already_staged = sorted(staged_paths(tree))
        if already_staged:
            plan['problems'].append(f'{len(already_staged)} file(s) are staged in Git already (the first: '
                                    f'{already_staged[0]}). This program stages into an index that is exactly the '
                                    f'last commit, so that the commit holds the conversion and nothing else.')
        describe_plan(plan, entries, say)
        if look_only:
            say('STAGE AND REFRESH - END - LOOKED ONLY; nothing was changed.'
                + (' The findings above would stop a real run.' if plan['problems'] else ''))
            return EXIT_STOPPED if plan['problems'] else EXIT_DONE
        if plan['problems']:
            raise Stopped(f'{len(plan["problems"])} finding(s) above. Nothing was changed.')
        if plan['to_stage'] or plan['to_refresh']:
            typed = ask(f'Type {WORD_TO_GO_ON} to stage {len(plan["to_stage"])} file(s) and put back '
                        f'{len(plan["to_refresh"])} working copies, or anything else to stop: ')
            if typed.strip() != WORD_TO_GO_ON:
                say('STAGE AND REFRESH - END - not confirmed; nothing was changed.')
                return EXIT_NOT_CONFIRMED
            if plan['to_stage']:
                stage_exactly(tree, plan['to_stage'])
            for path, blob_id in sorted(plan['to_refresh'].items()):
                checkpoint(path)
                refresh_one(tree, path, blob_id, rule)
            note_refreshed(tree, sorted(plan['to_refresh']))
            say(f'  Staged: {len(plan["to_stage"])} file(s). Working copies put back: {len(plan["to_refresh"])}.')
        else:
            say('  Nothing is left to stage or to put back.')
        prove(tree, entries, rule, say)
        say('STAGE AND REFRESH - END - FINISHED. Nothing was committed or pushed: that is the next part of the '
            'sheet.')
        return EXIT_DONE
    except Stopped as stop:
        say(f'STOP: {stop}')
    except OSError as failure:
        say(f'STOP: Windows refused to read or write a file: {failure}.')
    say(f'STAGE AND REFRESH - END - STOPPED. Read the STOP line above. Do not commit. {conversion.AFTER_A_STOP}')
    return EXIT_STOPPED


def main(arguments) -> int:
    """The command line. arguments: for example ['--tree', '.', '--list', 'CONVERSION_LIST.json', '--look'].
    Returns the exit code."""
    parser = argparse.ArgumentParser(description='Stage the converted files and refresh the working copy.')
    parser.add_argument('--tree', required=True, help='the tree root (the project folder)')
    parser.add_argument('--list', required=True, dest='list_path', help='the conversion list of the package')
    parser.add_argument('--look', action='store_true', help='print what would be done and change nothing')
    options = parser.parse_args(arguments)
    return run(options.tree, options.list_path, options.look)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
