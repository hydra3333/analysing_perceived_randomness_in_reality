#!/usr/bin/env python3
"""MHUPA_COPY.py - the manifest-controlled copy helper of the MHUP-A install package (design Appendix J steps 4, 6, 8, 15).

DRAFT (item 2 of the integrated package work list; not yet reviewed). Claude web chat, 10 November 2026.
Standard library only. It imports no project code, runs no Git command that writes, and touches no path the package
manifest does not name. Run with the venv's Python from the package folder:
  python -I -B MHUPA_COPY.py copy --part gate --repo REPO       step 6: exactly the manifest's gate_files
  python -I -B MHUPA_COPY.py copy --part rest --repo REPO       step 8: the manifest's rest_files and its deletions
  python -I -B MHUPA_COPY.py barrier --create E --repo REPO     step 4 (then P): create-only, the fixed barrier text
  python -I -B MHUPA_COPY.py barrier --remove E --repo REPO     step 15 (then P): only a file holding exactly that text
Every command prints one PASS or STOP line and exits 0 or 1. Before writing anything it checks the whole package
(every overlay file against the manifest) and every target's present state; it writes nothing if any check fails.
Each written file is read back and compared. Barrier U (the updater lock) is not this tool's: process_check.py
take-install-lock and release-install-lock own it.
"""
import argparse, hashlib, json, os, sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'PACKAGE_MANIFEST_MHUP_A.json'
OVERLAY = HERE / 'repo_overlay'
BARRIER_TEXT = 'MHUP_A install barrier {name} (design Appendix J). Removed only by the install steps or Claude\'s reviewed restore steps.\n'


class Stop(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(b):
    return b.replace(b'\r\n', b'\n')


def safe_rel(p):
    pp = PurePosixPath(p)
    if pp.is_absolute() or '..' in pp.parts or '\\' in p or not pp.parts or p != pp.as_posix():
        raise Stop(f'unsafe path in the manifest: {p!r}')
    return pp


def target(repo, rel):
    t = repo.joinpath(*safe_rel(rel).parts)
    for parent in [t, *t.parents]:
        if parent == repo:
            break
        if parent.is_symlink():
            raise Stop(f'a symlink on the path of {rel}')
    return t


def load():
    m = json.loads(MANIFEST.read_text(encoding='ascii'))
    if m.get('package') != 'MHUP_A':
        raise Stop('the manifest is not MHUP_A\'s')
    expected = {**m['new'], **{p: h[1] for p, h in m['modified'].items()}}
    if sorted(expected) != sorted(m['gate_files'] + m['rest_files']):
        raise Stop('the manifest\'s gate_files and rest_files do not partition its new and modified files')
    for p, h in expected.items():                       # the whole package must be intact before any write
        f = OVERLAY.joinpath(*safe_rel(p).parts)
        if not f.is_file() or f.is_symlink() or sha(norm(f.read_bytes())) != h:
            raise Stop(f'package file missing or damaged: {p}')
    return m, expected


def repo_root(arg):
    repo = Path(arg).resolve()
    if not (repo / '.git').exists():
        raise Stop(f'not a Git checkout: {repo}')
    return repo


def copy(m, expected, repo, part):
    paths = m['gate_files'] if part == 'gate' else m['rest_files']
    dels = m['deleted'] if part == 'rest' else {}
    for p in paths:                                     # check every target first; write nothing on any failure
        t = target(repo, p)
        if p in m['new']:
            if t.exists() or t.is_symlink():
                raise Stop(f'new path already exists: {p}')
        else:
            if not t.is_file() or sha(norm(t.read_bytes())) != m['modified'][p][0]:
                raise Stop(f'file to be replaced is not at its base bytes: {p}')
    for p, h in dels.items():
        t = target(repo, p)
        if not t.is_file() or sha(norm(t.read_bytes())) != h:
            raise Stop(f'file to be deleted is not at its base bytes: {p}')
    for p in paths:
        src, t = OVERLAY.joinpath(*safe_rel(p).parts), target(repo, p)
        t.parent.mkdir(parents=True, exist_ok=True)
        data = src.read_bytes()
        with open(t, 'wb') as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        if sha(norm(t.read_bytes())) != expected[p]:
            raise Stop(f'written file does not read back with the expected bytes: {p}')
    for p in dels:
        target(repo, p).unlink()
        if target(repo, p).exists():
            raise Stop(f'deleted file still present: {p}')
    return f'COPY PASS: part {part}: {len(paths)} files written and read back' + \
        (f', {len(dels)} deleted' if dels else '')


def barrier(m, repo, name, create):
    if name not in ('E', 'P'):
        raise Stop('barrier must be E or P (U belongs to process_check.py)')
    rel = m['barriers'][name]
    t = target(repo, rel)
    text = BARRIER_TEXT.format(name=name).encode('ascii')
    if create:
        t.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(t, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_BINARY', 0))
        except FileExistsError:
            raise Stop(f'barrier {name} already exists: {rel}') from None
        try:
            os.write(fd, text)
            os.fsync(fd)
        finally:
            os.close(fd)
        return f'BARRIER PASS: {name} created ({rel})'
    if not t.is_file() or t.is_symlink():
        raise Stop(f'barrier {name} is absent or not a plain file: {rel}')
    if t.read_bytes() != text:
        raise Stop(f'barrier {name} does not hold this package\'s text; nothing removed: {rel}')
    t.unlink()
    return f'BARRIER PASS: {name} removed ({rel})'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('copy')
    c.add_argument('--part', required=True, choices=['gate', 'rest'])
    c.add_argument('--repo', required=True)
    b = sub.add_parser('barrier')
    g = b.add_mutually_exclusive_group(required=True)
    g.add_argument('--create', choices=['E', 'P'])
    g.add_argument('--remove', choices=['E', 'P'])
    b.add_argument('--repo', required=True)
    a = ap.parse_args(argv)
    try:
        m, expected = load()
        repo = repo_root(a.repo)
        if a.cmd == 'copy':
            print(copy(m, expected, repo, a.part))
        else:
            print(barrier(m, repo, a.create or a.remove, bool(a.create)))
        return 0
    except (Stop, OSError, ValueError, KeyError) as exc:
        print(f'COPY STOP: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
