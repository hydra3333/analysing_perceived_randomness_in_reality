"""The light tidy-up: the proof that only comments changed (reads only).

What this file is for
    It compares every Python file under src/ and tests/ of a checkout with the same file at a Git commit, after
    taking every comment and every docstring out of both. If what is left is identical for every file, then
    nothing that Python runs has changed: no calculation, no import, no constant, no message. It reads the
    files and asks Git for the earlier versions; it writes nothing and runs none of the project's code.

Which part of the specification it carries out
    The owner's note of ratification RAT-40, item 3 (decision log entry 147): "No calculation changes", and
    doc/CODING_PRACTICES_v0_1.md section 6.

Which of the project's own modules it uses
    None (standard library only).

What uses it
    make_tidy_up.py (the function code_only), and the tidy-up package's install and run sheet, part 2.

Usage:  python -B check_comments_only.py [--tree <project folder>] [--base <commit>]
        --tree  the checkout to check; the default is the current folder.
        --base  the commit to compare with; the default is HEAD (what was last committed).
Result line and exit code:
        RESULT: PASS ...   exit 0   every file's code is identical; only comments and docstrings differ
        RESULT: STOP ...   exit 1   a file's code differs, or a Python file was added or removed
        REFUSED ...        exit 2   the folder is not a Git checkout, or Git could not answer
"""
from __future__ import annotations

import argparse
import ast
import os
import subprocess
import sys
from pathlib import Path

# The folders whose Python files are compared: the project's code and its tests.
CODE_FOLDERS = ('src', 'tests')

# Git is asked to read only: it must not take its optional locks or refresh its index.
GIT_READ_ONLY = dict(os.environ, GIT_OPTIONAL_LOCKS='0')

# The kinds of node whose first statement can be a docstring.
DOCSTRING_OWNERS = (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


class Refused(Exception):
    """The check could not be made at all (for example, the folder is not a Git checkout)."""


def code_only(source: str) -> str:
    """The code of a Python file with every docstring removed (comments are never part of it).

    source: the file's text.
    Returns a text form of the parsed code, for example 'Module(body=[ImportFrom(...), ...])'. Two files give
    the same text exactly when they differ in nothing but comments, docstrings, blank lines and layout.
    Refuses (SyntaxError) text that is not Python.
    """
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, DOCSTRING_OWNERS):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return ast.dump(tree)


def git_output(tree: Path, *arguments: str) -> bytes:
    """Run one read-only Git command in a checkout and return what it printed.

    tree: the checkout.  arguments: the command, for example ('show', 'HEAD:src/a.py').
    Returns the output bytes. Refuses (Refused) if Git fails, with Git's own message.
    """
    done = subprocess.run(['git', '--no-optional-locks', '-C', str(tree), *arguments],
                          capture_output=True, env=GIT_READ_ONLY)
    if done.returncode != 0:
        raise Refused(f'git {" ".join(arguments)} failed in {tree}: {done.stderr.decode(errors="replace").strip()[:300]}')
    return done.stdout


def python_files_on_disk(tree: Path) -> set:
    """The Python files under the code folders of a checkout, as paths from its root with forward slashes.

    tree: the checkout.
    Returns for example {'src/methods/E_007/core_v1.py', 'tests/test_e7.py', ...}; Python's own cache folders
    (__pycache__) are left out.
    """
    return {path.relative_to(tree).as_posix() for folder in CODE_FOLDERS for path in (tree / folder).rglob('*.py')
            if '__pycache__' not in path.parts}


def python_files_at(tree: Path, base: str) -> set:
    """The Python files under the code folders at a commit, for example {'src/methods/E_007/core_v1.py', ...}.

    tree: the checkout.  base: the commit.  Refuses (Refused) if Git does not know the commit.
    """
    listing = git_output(tree, 'ls-tree', '-r', '--name-only', '-z', base, '--', *CODE_FOLDERS).decode()
    return {path for path in listing.split('\0') if path.endswith('.py')}


def compare(tree: Path, base: str) -> int:
    """Compare every Python file of the checkout with the commit, print the findings, and return the exit code.

    tree: the checkout.  base: the commit.
    Returns 0 after 'RESULT: PASS', or 1 after 'RESULT: STOP' (each differing file is named on its own line).
    """
    on_disk, at_base = python_files_on_disk(tree), python_files_at(tree, base)
    problems = [f'ADDED (not in {base}): {path}' for path in sorted(on_disk - at_base)]
    problems += [f'REMOVED (in {base}, not on disk): {path}' for path in sorted(at_base - on_disk)]
    text_changed = 0
    for path in sorted(on_disk & at_base):
        before = git_output(tree, 'show', f'{base}:{path}').replace(b'\r\n', b'\n')
        after = (tree / path).read_bytes().replace(b'\r\n', b'\n')
        if before == after:
            continue
        text_changed += 1
        try:
            same_code = code_only(before.decode('utf-8')) == code_only(after.decode('utf-8'))
        except (SyntaxError, UnicodeDecodeError) as error:
            problems.append(f'NOT READABLE AS PYTHON: {path}: {error}')
            continue
        if same_code:
            print(f'comments only: {path}')
        else:
            problems.append(f'CODE CHANGED: {path}')
    for problem in problems:
        print(problem)
    commit = git_output(tree, 'rev-parse', base).decode().strip()
    print(f'compared with commit {commit}: {len(on_disk & at_base)} Python files under {" and ".join(CODE_FOLDERS)}; '
          f'{text_changed} with changed text; {len(problems)} with a problem')
    if problems:
        print('RESULT: STOP - something other than comments and docstrings differs (see the lines above). '
              'Change nothing and send Claude this output.')
        return 1
    print(f'RESULT: PASS - in all {text_changed} changed files only comments and docstrings differ; '
          'the code Python runs is identical.')
    return 0


def main() -> int:
    """Read the command line, make the comparison, and return the exit code (0 PASS, 1 STOP, 2 REFUSED)."""
    parser = argparse.ArgumentParser(description='Prove that only comments and docstrings changed (reads only).')
    parser.add_argument('--tree', type=Path, default=Path('.'), help='the checkout to check (default: this folder)')
    parser.add_argument('--base', default='HEAD', help='the commit to compare with (default: HEAD)')
    arguments = parser.parse_args()
    tree = arguments.tree.resolve()
    try:
        if not (tree / '.git').exists():
            raise Refused(f'{tree} is not a Git checkout (it has no .git). Run this in the project folder, '
                          'or name it with --tree.')
        return compare(tree, arguments.base)
    except Refused as refusal:
        print(f'REFUSED: {refusal}')
        return 2


if __name__ == '__main__':
    sys.exit(main())
