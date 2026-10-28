#!/usr/bin/env python3
"""Read-only installation verifier for DOC-3 (H-1 v1r3, register v0.9 and their review history).

Claude, 28 October 2026. Standard library only; does not import project code, run tests, change
files or touch Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0).
Phases:
  pre        clean tree; HEAD descends from the base commit; the @@N@@ new paths are absent;
             guarded files unchanged in Git.
  post       after copying the overlay: exactly the @@N@@ new paths appear, all with the expected
             bytes (CRLF tolerated: the comparison is on LF-normalised bytes).
  committed  after the commit: clean tree; HEAD has one parent; the last commit added exactly
             those paths and nothing else, all with the expected Git blobs.
On any STOP in the committed phase, the verifier prints the identities needed to decide what
to do (HEAD, its parent, the last commit's paths, the working-tree status). Do NOT push and do
NOT reset: send Claude the whole output.
Usage: python VERIFY_DOC3_INSTALL.py --repo . --phase pre|post|committed
"""
import argparse, hashlib, os, subprocess, sys
from pathlib import Path

BASE = '@@BASE@@'
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
NEW = {  # path: Git-content SHA-256 (LF)
@@NEW@@
}
GUARDED = {  # must stay byte-identical in Git (hashes of the Git blobs at the base commit)
@@GUARDED@@
}
HERE = Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(b):
    return b.replace(b'\r\n', b'\n')


def run(repo, *args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=GIT_ENV)


def git(repo, *args):
    r = run(repo, *args)
    if r.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)} failed: {r.stderr.decode(errors="replace")[:300]}')
    return r.stdout


def need(cond, msg):
    if not cond:
        raise RuntimeError('FAIL: ' + msg)


def identities(repo):
    """Read-only facts for deciding after a committed-phase STOP."""
    print('--- identities for Claude (read-only) ---', file=sys.stderr)
    for label, args in [('HEAD and parents', ['log', '-1', '--format=%H %P %s', 'HEAD']),
                        ('last 3 commits', ['log', '--oneline', '-3']),
                        ('last commit paths', ['diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD']),
                        ('upstream', ['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}']),
                        ('commits not yet pushed', ['log', '--oneline', '@{u}..HEAD']),
                        ('working tree and index', ['status', '--porcelain=v1', '--untracked-files=all'])]:
        r = run(repo, *args)
        out = (r.stdout if r.returncode == 0 else r.stderr).decode(errors='replace').rstrip()
        print(f'[{label}]\n{out[:1500] or "(none)"}', file=sys.stderr)
    print('--- Do NOT push. Do NOT reset. Send Claude this whole output. ---', file=sys.stderr)


def main(a):
    repo = a.repo.resolve()
    need((repo / '.git').exists(), f'not a Git checkout: {repo}')
    for p, h in NEW.items():  # the package itself must be intact
        need(sha(norm((HERE / 'repo_overlay' / p).read_bytes())) == h, f'package file damaged: {p}')
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    anc = run(repo, 'merge-base', '--is-ancestor', BASE, 'HEAD')
    need(anc.returncode == 0, f'HEAD {head} does not descend from base {BASE}; STOP')
    print('HEAD:', head, '(descends from base', BASE[:7] + ')')
    for p, h in GUARDED.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'guarded file changed in Git: {p}')
    print(f'{len(GUARDED)} guarded files unchanged in Git HEAD')
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode(errors='replace')

    if a.phase == 'pre':
        need(not status.strip(), 'working tree or index not clean:\n' + status[:600])
        for p in NEW:
            need(not (repo / p).exists(), f'new path already exists: {p}; STOP')
        print(f'PRE PASS: clean tree; {len(NEW)} new paths absent. Nothing was changed.')
        return

    if a.phase == 'post':
        lines = status.splitlines()
        need(all(ln.startswith('?? ') for ln in lines), 'changes other than new files:\n' + status[:600])
        changed = {ln[3:].strip().strip('"').replace('\\', '/') for ln in lines}
        need(changed == set(NEW), 'unexpected new paths: ' + ', '.join(sorted(changed ^ set(NEW))))
        for p, h in NEW.items():
            f = repo / p
            need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
            need(sha(norm(f.read_bytes())) == h, f'wrong bytes: {p}')
        print(f'POST PASS: exactly the {len(NEW)} expected new paths, all with the expected bytes.')
        return

    need(not status.strip(), 'working tree or index not clean after commit:\n' + status[:600])
    parents = git(repo, 'log', '-1', '--format=%P', 'HEAD').decode().split()
    need(len(parents) == 1, f'HEAD has {len(parents)} parents, expected 1')
    for p, h in NEW.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'wrong Git blob in HEAD: {p}')
    names = git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD').decode().splitlines()
    got = {ln.split('\t', 1)[1]: ln.split('\t', 1)[0] for ln in names if ln}
    need(got == {p: 'A' for p in NEW}, 'the last commit did not add exactly the expected paths: ' + repr(sorted(got.items())))
    print(f'COMMITTED PASS: the last commit ({head[:7]}) added exactly {len(NEW)} files; all Git blobs match.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--phase', required=True, choices=['pre', 'post', 'committed'])
    args = ap.parse_args()
    try:
        main(args)
        print('Read-only: no project code imported, nothing run, nothing changed.')
    except Exception as exc:
        print('VERIFICATION STOP:', exc, file=sys.stderr)
        if args.phase == 'committed':
            try:
                identities(args.repo.resolve())
            except Exception as exc2:
                print('(could not list identities:', exc2, ')', file=sys.stderr)
        sys.exit(2)
