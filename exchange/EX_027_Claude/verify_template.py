#!/usr/bin/env python3
"""Read-only installation verifier for E1-ALIGN (E_1 into its method folder; register v0.10).

Claude, 28 October 2026. Standard library only; does not import project code, run tests, change
files or touch Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0). It never
reads source_data/, results/ or transitory_data/.
The exact check (E1A-T01) rebuilds every changed code file from its predecessor's Git blob at the base
commit using ONLY the frozen, reviewed allowlist's (old block -> new block) edits, each of which must
occur exactly once, and requires byte equality (LF-normalised, so Windows CRLF copies compare equal).
Phases:
  pre        clean tree; HEAD descends from the base commit; src/ and tests/ in HEAD are exactly the
             base commit's; every new path is absent; guarded files unchanged.
  post       after RENAME_FILES.cmd and copying the overlay: the index holds exactly the 5 moves; the
             working tree differs from the index in exactly the 10 allowlisted edited files; exactly the
             new files are untracked; every edited file equals predecessor + allowlist; the moved-
             unchanged file and every added file have their expected bytes; no old path remains.
  committed  after the commit: clean tree; HEAD has one parent whose src/ and tests/ are the base's;
             the last commit deleted the 5 old paths, added the 5 new ones and the new files, and
             modified exactly the 6 edited-in-place files, all with the expected Git blobs.
On any STOP in the committed phase the verifier prints the identities needed to decide what to do.
Do NOT push and do NOT reset: send Claude the whole output.
Usage: python VERIFY_E1ALIGN_INSTALL.py --repo . --phase pre|post|committed
"""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

BASE = '@@BASE@@'
ALLOW_PATH = 'review/E1ALIGN_Code_Install_v1/e1align_allowlist.json'
ALLOW_SHA = '@@ALLOW_SHA@@'          # the reviewed frozen allowlist (E1-ALIGN v0.2r1 design evidence)
DATA = json.loads(r'''@@DATA@@''')
NEW_SHA = DATA['new_sha']            # every path with new bytes (edited, added, docs) -> SHA-256 (LF)
DOCS = DATA['docs']                  # added non-code files (register, review evidence, manifest)
GUARDED = DATA['guarded']            # must stay byte-identical in Git
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
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


def name_status(out):
    got = {}
    for ln in out.decode(errors='replace').splitlines():
        if ln:
            code, path = ln.split('\t', 1)
            got[path.strip('"')] = code
    return got


def identities(repo):
    print('--- identities for Claude (read-only) ---', file=sys.stderr)
    for label, args in [('HEAD and parents', ['log', '-1', '--format=%H %P %s', 'HEAD']),
                        ('last 3 commits', ['log', '--oneline', '-3']),
                        ('last commit paths', ['diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD']),
                        ('upstream', ['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}']),
                        ('commits not yet pushed', ['log', '--oneline', '@{u}..HEAD']),
                        ('working tree and index', ['status', '--porcelain=v1', '--untracked-files=all'])]:
        r = run(repo, *args)
        out = (r.stdout if r.returncode == 0 else r.stderr).decode(errors='replace').rstrip()
        print(f'[{label}]\n{out[:2500] or "(none)"}', file=sys.stderr)
    print('--- Do NOT push. Do NOT reset. Send Claude this whole output. ---', file=sys.stderr)


def rebuild(base_text, edits, label):
    t = base_text
    for ed in edits:
        need(t.count(ed['old']) == 1, f'{label}: an allowlisted old block does not occur exactly once')
        t = t.replace(ed['old'], ed['new'])
    return t.encode('utf-8')


def main(a):
    repo = a.repo.resolve()
    need((repo / '.git').exists(), f'not a Git checkout: {repo}')
    allow_bytes = norm((HERE / 'repo_overlay' / ALLOW_PATH).read_bytes())
    need(sha(allow_bytes) == ALLOW_SHA, 'package allowlist is not the reviewed one')
    allow = json.loads(allow_bytes.decode('utf-8'))
    moves = allow['moves']
    edited = {e['new_path']: e for e in allow['edited']}
    in_place = sorted(p for p, e in edited.items() if e['old_path'] == p)
    added = dict(allow['added'])
    for p, h in NEW_SHA.items():  # the package itself must be intact
        need(sha(norm((HERE / 'repo_overlay' / p).read_bytes())) == h, f'package file damaged: {p}')
    for p, h in added.items():
        need(NEW_SHA.get(p) == h, f'package added file differs from the allowlist: {p}')
    new_files = sorted(set(added) | set(DOCS))
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    need(run(repo, 'merge-base', '--is-ancestor', BASE, 'HEAD').returncode == 0,
         f'HEAD {head} does not descend from base {BASE}; STOP')
    print('HEAD:', head, '(descends from base', BASE[:7] + ')')
    for p, h in GUARDED.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'guarded file changed in Git: {p}')
    print(f'{len(GUARDED)} guarded files unchanged in Git HEAD')
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode(errors='replace')
    base_blob = lambda p: git(repo, 'show', f'{BASE}:{p}')

    if a.phase == 'pre':
        need(not status.strip(), 'working tree or index not clean:\n' + status[:600])
        diff = git(repo, 'diff', '--name-only', BASE, 'HEAD', '--', 'src', 'tests').decode().split()
        need(not diff, 'src/ or tests/ changed since the base commit: ' + ', '.join(diff[:20]))
        for p in list(moves.values()) + new_files:
            need(not (repo / p).exists(), f'new path already exists: {p}; STOP')
        print(f'PRE PASS: clean tree; src/ and tests/ exactly as at base {BASE[:7]}; '
              f'{len(moves) + len(new_files)} new paths absent. Nothing was changed.')
        return

    if a.phase == 'post':
        idx = name_status(git(repo, 'diff', '--cached', '--no-renames', '--name-status'))
        want_idx = dict({o: 'D' for o in moves}, **{n: 'A' for n in moves.values()})
        need(idx == want_idx, 'index is not exactly the 5 moves: ' + ', '.join(map(str, sorted(set(idx.items()) ^ set(want_idx.items()))))[:900])
        for o, n in moves.items():  # what git mv staged is the predecessor's bytes
            need(git(repo, 'show', f':{n}') == base_blob(o), f'staged move does not carry the base bytes: {n}')
        wt = name_status(git(repo, 'diff', '--no-renames', '--name-status'))
        want_wt = {p: 'M' for p in edited}
        need(wt == want_wt, 'working-tree changes are not exactly the 10 edited files: ' + ', '.join(map(str, sorted(set(wt.items()) ^ set(want_wt.items()))))[:900])
        untracked = {ln[3:].strip().strip('"') for ln in status.splitlines() if ln.startswith('??')}
        need(untracked == set(new_files), 'untracked files are not exactly the new files: ' + ', '.join(sorted(untracked ^ set(new_files)))[:900])
        for p, e in sorted(edited.items()):  # E1A-T01: predecessor + allowlist, exactly
            f = repo / p
            need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
            want = rebuild(base_blob(e['old_path']).decode('utf-8'), e['edits'], p)
            need(norm(f.read_bytes()) == want, f'{p}: differs from predecessor + allowlist')
            need(sha(want) == NEW_SHA[p], f'{p}: rebuilt bytes differ from the package')
        for p in allow['moved_unchanged']:
            old = next(o for o, n in moves.items() if n == p)
            need(norm((repo / p).read_bytes()) == base_blob(old), f'moved-unchanged file changed: {p}')
        for p in new_files:
            f = repo / p
            need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
            need(sha(norm(f.read_bytes())) == NEW_SHA[p], f'wrong bytes: {p}')
        for o in moves:
            need(not (repo / o).exists(), f'old path still present: {o}')
        print(f'POST PASS: index has exactly the {len(moves)} moves; the {len(edited)} edited files equal '
              f'predecessor + reviewed allowlist ({sum(len(e["edits"]) for e in edited.values())} blocks); '
              f'{len(new_files)} new files with the expected bytes; no old path remains.')
        return

    need(not status.strip(), 'working tree or index not clean after commit:\n' + status[:600])
    parents = git(repo, 'log', '-1', '--format=%P', 'HEAD').decode().split()
    need(len(parents) == 1, f'HEAD has {len(parents)} parents, expected 1')
    diff = git(repo, 'diff', '--name-only', BASE, 'HEAD~1', '--', 'src', 'tests').decode().split()
    need(not diff, "the commit's parent has src/ or tests/ changes since the base: " + ', '.join(diff[:20]))
    got = name_status(git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD'))
    want = dict({o: 'D' for o in moves}, **{n: 'A' for n in moves.values()},
                **{p: 'A' for p in new_files}, **{p: 'M' for p in in_place})
    need(got == want, 'the last commit did not change exactly the expected paths: ' + ', '.join(map(str, sorted(set(got.items()) ^ set(want.items()))))[:900])
    for p, h in NEW_SHA.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'wrong Git blob in HEAD: {p}')
    for p in allow['moved_unchanged']:
        old = next(o for o, n in moves.items() if n == p)
        need(git(repo, 'show', f'HEAD:{p}') == base_blob(old), f'moved-unchanged blob changed: {p}')
    print(f'COMMITTED PASS: the last commit ({head[:7]}) made the {len(moves)} moves, edited {len(edited)} files '
          f'and added {len(new_files)}; all Git blobs match.')


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
