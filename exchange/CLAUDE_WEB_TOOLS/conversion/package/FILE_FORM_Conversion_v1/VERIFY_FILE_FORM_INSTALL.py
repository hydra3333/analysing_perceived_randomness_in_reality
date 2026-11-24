#!/usr/bin/env python3
"""Verifier for the file-form conversion package: before its files are copied into the tree, after they are
copied, and after the commit. It reads only; it changes no file and no Git state.

What this file is for
    The conversion's sheet copies the package's own files into the DEV tree, runs the conversion, stages, and
    commits. This script is the check at three of those moments:
      pre        every file the package replaces still holds the content the package was built against (line
                 endings apart), and every file the package adds is absent;
      post       every one of the package's files lies in the tree with exactly the package's bytes;
      committed  after the commit: every file of the conversion list is in the commit with exactly the list's
                 "after" bytes, and the commit changed those paths and no others.
    It prints one line a finding and a last line PRE PASS, POST PASS, COMMITTED PASS or STOP.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_2.md sections 5 and 7 ("the commit is checked: the bytes staged for it are in the
    standard's form"; "the conversion's list proves, file by file, that nothing but line endings changed").

Which of the project's own modules it uses
    None. Standard library only; the phase "committed" asks Git what the last commit holds, which is what Git is
    for. It is never a check of whether a tree may run.

What uses it
    The project owner, from the conversion's sheet. Usage:
        python VERIFY_FILE_FORM_INSTALL.py --repo <tree root> --phase pre|post|committed
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

# Python must leave no compiled copy beside this file.
sys.dont_write_bytecode = True

PACKAGE = Path(__file__).resolve().parent
# The package's own files, as they are copied into the tree.
OVERLAY = PACKAGE / 'repo_overlay'
# The manifest: one line a file of the overlay.
#   N <sha256 of the package's bytes>  <path>                                   a new file
#   M <sha256 of the package's bytes>  <sha256 of the replaced content, LF>  <path>   a replaced file
MANIFEST = PACKAGE / 'INSTALL_MANIFEST_SHA256.txt'
CONVERSION_LIST = PACKAGE / 'CONVERSION_LIST.json'
# Git is asked without taking its optional locks, so that asking changes nothing.
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
# How many findings are printed before the rest are counted.
FINDINGS_SHOWN = 20


def sha256_of(data: bytes) -> str:
    """The SHA-256 of some bytes as 64 hexadecimal characters."""
    return hashlib.sha256(data).hexdigest()


def read_manifest() -> list:
    """The manifest's entries: [('N', package sha, None, path), ('M', package sha, replaced sha, path), ...].
    Refuses (SystemExit) a manifest line that is not one of the two forms."""
    entries = []
    for line in MANIFEST.read_text(encoding='ascii').splitlines():
        if not line or line.startswith('#'):
            continue
        fields = line.split()
        if fields[0] == 'N' and len(fields) == 3:
            entries.append(('N', fields[1], None, fields[2]))
        elif fields[0] == 'M' and len(fields) == 4:
            entries.append(('M', fields[1], fields[2], fields[3]))
        else:
            sys.exit(f'STOP: the manifest holds a line that is not understood: {line!r}')
    return entries


def git(repo: Path, *arguments: str) -> bytes:
    """What one Git command prints, asked in the tree without optional locks. Refuses (SystemExit) if it fails."""
    done = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *arguments], capture_output=True,
                          env=GIT_ENV, check=False)
    if done.returncode != 0:
        sys.exit(f'STOP: git {" ".join(arguments[:2])} failed: {done.stderr.decode("utf-8", "replace").strip()}')
    return done.stdout


def pre(repo: Path) -> list:
    """Findings before the package's files are copied: a replaced file that no longer holds the content the
    package was built against (compared with every CRLF read as LF), and a new file that is there already."""
    findings = []
    for kind, _package_sha, replaced_sha, path in read_manifest():
        full = repo / path
        if kind == 'N':
            if full.exists():
                findings.append(f'{path}: the package adds this file, but it is in the tree already')
        elif not full.is_file():
            findings.append(f'{path}: the package replaces this file, but it is not in the tree')
        elif sha256_of(full.read_bytes().replace(b'\r\n', b'\n')) != replaced_sha:
            findings.append(f'{path}: its content is not what the package was built against')
    return findings


def post(repo: Path) -> list:
    """Findings after the copy: a file of the package that is not in the tree with exactly the package's bytes."""
    findings = []
    for _kind, package_sha, _replaced_sha, path in read_manifest():
        full = repo / path
        if sha256_of((OVERLAY / path).read_bytes()) != package_sha:
            findings.append(f'{path}: the package\'s own copy does not have the manifest\'s SHA-256')
        elif not full.is_file() or sha256_of(full.read_bytes()) != package_sha:
            findings.append(f'{path}: not in the tree with exactly the package\'s bytes')
    return findings


def committed(repo: Path) -> list:
    """Findings after the commit: a listed file whose committed bytes are not the list's "after"; a path the
    commit changed that is not on the list; a listed path that changed bytes but is not in the commit."""
    listed = {entry['path']: entry for entry in json.loads(CONVERSION_LIST.read_bytes().decode('ascii'))['files']}
    findings = []
    for path, entry in sorted(listed.items()):
        blob = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), 'show', f'HEAD:{path}'],
                              capture_output=True, env=GIT_ENV, check=False)
        if blob.returncode != 0:
            findings.append(f'{path}: not in the commit')
        elif sha256_of(blob.stdout) != entry['sha256_after']:
            findings.append(f'{path}: the committed bytes are not the list\'s "after"')
    changed = {name.decode('utf-8') for name in
               git(repo, 'diff-tree', '-r', '--no-commit-id', '--name-only', '-z', 'HEAD').split(b'\0') if name}
    findings.extend(f'{path}: changed by the commit but not on the conversion list'
                    for path in sorted(changed - set(listed)))
    if not changed:
        findings.append('the last commit changed no file: the conversion has not been committed')
    if git(repo, 'status', '--porcelain'):
        findings.append('the working tree is not clean after the commit (run "git status --short")')
    return findings


def main(arguments) -> int:
    """The command line. Returns 0 for a PASS, 1 for a STOP."""
    parser = argparse.ArgumentParser(description='Verify the file-form conversion package against a tree.')
    parser.add_argument('--repo', required=True, help='the tree root (the project folder)')
    parser.add_argument('--phase', required=True, choices=('pre', 'post', 'committed'))
    options = parser.parse_args(arguments)
    repo = Path(options.repo).resolve()
    findings = {'pre': pre, 'post': post, 'committed': committed}[options.phase](repo)
    for finding in findings[:FINDINGS_SHOWN]:
        print(f'  {finding}')
    if len(findings) > FINDINGS_SHOWN:
        print(f'  ... and {len(findings) - FINDINGS_SHOWN} more')
    if findings:
        print(f'STOP: {len(findings)} finding(s) in phase {options.phase}. Change nothing; send Claude this output.')
        return 1
    counts = {'pre': f'{len(read_manifest())} package files checked against the tree',
              'post': f'{len(read_manifest())} package files in the tree with the package\'s bytes',
              'committed': 'every listed file is committed with the list\'s "after" bytes; the commit changed '
                           'listed paths only; the working tree is clean'}[options.phase]
    print(f'{options.phase.upper()} PASS ({counts})')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
