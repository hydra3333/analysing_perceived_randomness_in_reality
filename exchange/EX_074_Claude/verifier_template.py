#!/usr/bin/env python3
"""Read-only installation verifier for the wave 2 package (E_2, E_17, E_18 and E_19 revision 1 with their shared helper, installed non-runnable; the template's draft 3).

Claude, 30 October 2026 (from the E_3/E_4 package verifier). Standard library only; does not import project code, run tests, change
files or touch Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0).
Phases:
  pre        clean tree; HEAD descends from the base commit; src/ and tests/ in HEAD are exactly the
             base commit's; the @@N@@ new paths are absent; the @@M@@ modified files still have their
             base bytes; guarded files unchanged in Git.
  post       after copying the overlay: exactly the @@N@@ new paths appear and exactly the @@M@@
             modified files change, all with the expected bytes (CRLF tolerated: the comparison is on
             LF-normalised bytes).
  committed  after the commit: clean tree; HEAD has one parent; the last commit added exactly the
             new paths and modified exactly the modified files, all with the expected Git blobs.
On any STOP in the committed phase, the verifier prints the identities needed to decide what
to do (HEAD, its parent, the last commit's paths, the working-tree status). Do NOT push and do
NOT reset: send Claude the whole output.
Usage: python VERIFY_W2_INSTALL.py --repo . --phase pre|post|committed
"""
import argparse, hashlib, os, subprocess, sys
from pathlib import Path

BASE = '@@BASE@@'
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
NEW = {  # path: Git-content SHA-256 (LF)
@@NEW@@
}
MODIFIED = {  # path: (base Git-content SHA-256, new Git-content SHA-256), LF
@@MODIFIED@@
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
    for p, h in [*NEW.items(), *((p, n) for p, (_o, n) in MODIFIED.items())]:  # the package must be intact
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
        diff = git(repo, 'diff', '--name-only', BASE, 'HEAD', '--', 'src', 'tests').decode().split()
        need(not diff, 'src/ or tests/ changed since the base commit: ' + ', '.join(diff[:20]))
        for p in NEW:
            need(not (repo / p).exists(), f'new path already exists: {p}; STOP')
        for p, (old, _new) in MODIFIED.items():
            need(sha(git(repo, 'show', f'HEAD:{p}')) == old, f'file to be replaced is not its base version in Git: {p}')
            need(sha(norm((repo / p).read_bytes())) == old, f'file to be replaced differs on disk: {p}')
        print(f'PRE PASS: clean tree; {len(NEW)} new paths absent; {len(MODIFIED)} files at their base version. '
              'Nothing was changed.')
        return

    if a.phase == 'post':
        lines = status.splitlines()
        new = {ln[3:].strip().strip('"').replace('\\', '/') for ln in lines if ln.startswith('?? ')}
        mod = {ln[3:].strip().strip('"').replace('\\', '/') for ln in lines if ln.startswith(' M ')}
        need(len(new) + len(mod) == len(lines), 'changes other than new files and modified files:\n' + status[:600])
        need(new == set(NEW), 'unexpected new paths: ' + ', '.join(sorted(new ^ set(NEW))))
        need(mod == set(MODIFIED), 'unexpected modified paths: ' + ', '.join(sorted(mod ^ set(MODIFIED))))
        for p, h in [*NEW.items(), *((p, n) for p, (_o, n) in MODIFIED.items())]:
            f = repo / p
            need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
            need(sha(norm(f.read_bytes())) == h, f'wrong bytes: {p}')
        print(f'POST PASS: exactly the {len(NEW)} expected new paths and {len(MODIFIED)} modified files, '
              'all with the expected bytes.')
        return

    need(not status.strip(), 'working tree or index not clean after commit:\n' + status[:600])
    parents = git(repo, 'log', '-1', '--format=%P', 'HEAD').decode().split()
    need(len(parents) == 1, f'HEAD has {len(parents)} parents, expected 1')
    diff = git(repo, 'diff', '--name-only', BASE, 'HEAD~1', '--', 'src', 'tests').decode().split()
    need(not diff, "the commit's parent has src/ or tests/ changes since the base: " + ', '.join(diff[:20]))
    for p, h in [*NEW.items(), *((p, n) for p, (_o, n) in MODIFIED.items())]:
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'wrong Git blob in HEAD: {p}')
    for p, (old, _n) in MODIFIED.items():
        need(sha(git(repo, 'show', f'HEAD~1:{p}')) == old, f'parent does not hold the base version: {p}')
    names = git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD').decode().splitlines()
    got = {ln.split('\t', 1)[1]: ln.split('\t', 1)[0] for ln in names if ln}
    want = {**{p: 'A' for p in NEW}, **{p: 'M' for p in MODIFIED}}
    need(got == want, 'the last commit did not change exactly the expected paths: ' + repr(sorted(got.items())))
    print(f'COMMITTED PASS: the last commit ({head[:7]}) added exactly {len(NEW)} files and modified '
          f'{len(MODIFIED)}; all Git blobs match.')


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
