#!/usr/bin/env python3
"""VERIFY_MHUP_A.py - the read-only installation verifier of the MHUP-A install package (design Appendix J).

DRAFT (item 2 of the integrated package work list; not yet reviewed; NOT installation-ready): the phases pre, post
and committed are built; the phase `released` (Appendix J step 17: the release commit, the release record, the
two-commit and barrier-order proofs, EX_148 (ix)) is item 3 and here only refuses.
Claude web chat, 10 November 2026, from wf1/verifier_template.py. Standard library only; imports no project code,
runs no test, changes no file and no Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0).
It reads its expectations from PACKAGE_MANIFEST_MHUP_A.json beside it, whose SHA-256 is fixed below.
Phases:
  pre        Appendix J step 1. The package is intact (every overlay file, the manifest, the copy tool) and the
             staged process_check.py has the manifest's SHA-256; the working tree and index are clean; HEAD
             descends from the base commit; src/ and tests/ in HEAD are exactly the base commit's; the new paths,
             the install and release records and barriers E and P are absent; every file to be replaced or deleted
             has its base bytes in Git and on disk; transitory_data/no_pycache_ever does not exist. Changes since the
             base outside src/ and tests/ are listed for information.
  post       Appendix J step 9, after the two copy steps: the working-tree changes are exactly the new paths
             (untracked), the modified files and the deletion (unstaged), all with the expected bytes (CRLF
             tolerated: LF-normalised comparison).
  committed  Appendix J step 13, after the package commit: clean tree; HEAD has one parent, which descends from the
             base with src/ and tests/ unchanged; the commit added exactly the new paths and the install record,
             modified exactly the modified files and deleted exactly the deleted file, with the expected Git blobs;
             the install record names this package, this manifest's SHA-256 and the manifest's entries.
  released   NOT BUILT (item 3). Refuses.
On any STOP: do NOT push and do NOT reset; send Claude the whole output (Appendix J's STOP column applies).
Usage: python -I -B VERIFY_MHUP_A.py --repo REPO --phase pre|post|committed|released
"""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

MANIFEST_SHA256 = '@@MANIFEST_SHA256@@'
COPY_SHA256 = '@@COPY_SHA256@@'
INSTALL_SCHEMA = 'INSTALL_RECORD_V1'
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


def status_entries(repo):
    """Parsed `git status --porcelain=v1 -z --untracked-files=all`: list of (XY, path)."""
    raw = git(repo, 'status', '--porcelain=v1', '-z', '--untracked-files=all').decode('utf-8', errors='replace')
    out, items, i = [], raw.split('\0'), 0
    while i < len(items):
        it = items[i]
        i += 1
        if not it:
            continue
        xy, path = it[:2], it[3:]
        if xy[0] in 'RC':
            i += 1                                       # the rename's source follows; no rename is ever expected
        out.append((xy, path))
    return out


def identities(repo):
    """Read-only facts for deciding after a STOP."""
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


def load_package():
    mraw = (HERE / 'PACKAGE_MANIFEST_MHUP_A.json').read_bytes()
    need(sha(mraw) == MANIFEST_SHA256, 'the package manifest is not the one this verifier was built with')
    need(sha((HERE / 'MHUPA_COPY.py').read_bytes()) == COPY_SHA256, 'the package copy tool is damaged')
    m = json.loads(mraw.decode('ascii'))
    expected = {**m['new'], **{p: h[1] for p, h in m['modified'].items()}}
    for p, h in expected.items():
        f = HERE / 'repo_overlay' / p
        need(f.is_file() and not f.is_symlink() and sha(norm(f.read_bytes())) == h, f'package file missing or damaged: {p}')
    for t, h in m['tool_sha256'].items():
        need(expected.get(t) == h, f'the manifest\'s tool hash disagrees with its file list: {t}')
    return m, expected


def phase_pre(repo, m, expected):
    pc = 'src/package_tools/process_check.py'
    print(f'staged process_check.py SHA-256 {m["tool_sha256"][pc]} matches the manifest')
    st = status_entries(repo)
    need(not st, 'working tree or index not clean:\n' + '\n'.join(f'{x} {p}' for x, p in st[:30]))
    diff = git(repo, 'diff', '--name-only', m['base_commit'], 'HEAD', '--', 'src', 'tests').decode().split()
    need(not diff, 'src/ or tests/ changed since the base commit: ' + ', '.join(diff[:20]))
    other = git(repo, 'diff', '--name-only', m['base_commit'], 'HEAD').decode().split()
    other = [p for p in other if not p.startswith('exchange/')]
    print(f'changes since the base outside exchange/ (information): {len(other)}' +
          ''.join(f'\n  {p}' for p in other[:40]))
    for p in [*m['new'], m['install_record'], m['release_record'], m['barriers']['E'], m['barriers']['P']]:
        need(not (repo / p).exists() and not (repo / p).is_symlink(), f'path already exists: {p}; STOP')
    for p, (old, _new) in m['modified'].items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == old, f'file to be replaced is not its base version in Git: {p}')
        need(sha(norm((repo / p).read_bytes())) == old, f'file to be replaced differs on disk: {p}')
    for p, old in m['deleted'].items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == old, f'file to be deleted is not its base version in Git: {p}')
        need(sha(norm((repo / p).read_bytes())) == old, f'file to be deleted differs on disk: {p}')
    need(not (repo / 'transitory_data' / 'no_pycache_ever').exists(), 'transitory_data/no_pycache_ever exists (design 4.1)')
    print(f'PRE PASS: package intact; clean tree; {len(m["new"])} new paths absent; {len(m["modified"])} files to replace '
          f'and {len(m["deleted"])} to delete at their base version. Nothing was changed.')


def phase_post(repo, m, expected):
    st = status_entries(repo)
    new = {p for x, p in st if x == '??'}
    mod = {p for x, p in st if x == ' M'}
    dele = {p for x, p in st if x == ' D'}
    other = [(x, p) for x, p in st if x not in ('??', ' M', ' D')]
    need(not other, 'changes other than new files, modified files and unstaged deletions: ' + repr(other[:20]))
    for label, seen, want in (('new', new, set(m['new'])), ('modified', mod, set(m['modified'])),
                              ('deleted', dele, set(m['deleted']))):   # R-008: missing and unexpected named apart
        need(seen == want, f'{label} paths differ; MISSING (expected, not seen): ' +
             (', '.join(sorted(want - seen)) or 'none') + '; UNEXPECTED (seen, not expected): ' +
             (', '.join(sorted(seen - want)) or 'none'))
    for p in m['deleted']:
        need(not (repo / p).exists(), f'deleted path still on disk: {p}')
    for p, h in expected.items():
        f = repo / p
        need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
        need(sha(norm(f.read_bytes())) == h, f'wrong bytes: {p}')
    print(f'POST PASS: exactly the {len(m["new"])} expected new paths, {len(m["modified"])} modified files and '
          f'{len(m["deleted"])} deletion, all with the expected bytes.')


def phase_committed(repo, m, expected):
    st = status_entries(repo)
    need(not st, 'working tree or index not clean after commit:\n' + '\n'.join(f'{x} {p}' for x, p in st[:30]))
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    parents = git(repo, 'log', '-1', '--format=%P', 'HEAD').decode().split()
    need(len(parents) == 1, f'HEAD has {len(parents)} parents, expected 1')
    need(run(repo, 'merge-base', '--is-ancestor', m['base_commit'], 'HEAD~1').returncode == 0,
         'the package commit\'s parent does not descend from the base')
    diff = git(repo, 'diff', '--name-only', m['base_commit'], 'HEAD~1', '--', 'src', 'tests').decode().split()
    need(not diff, "the commit's parent has src/ or tests/ changes since the base: " + ', '.join(diff[:20]))
    for p, h in expected.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'wrong Git blob in HEAD: {p}')
    for p, (old, _n) in m['modified'].items():
        need(sha(git(repo, 'show', f'HEAD~1:{p}')) == old, f'parent does not hold the base version: {p}')
    for p, old in m['deleted'].items():
        need(sha(git(repo, 'show', f'HEAD~1:{p}')) == old, f'parent does not hold the deleted file: {p}')
        need(run(repo, 'cat-file', '-e', f'HEAD:{p}').returncode != 0, f'deleted file still in HEAD: {p}')
    names = git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD').decode().splitlines()
    got = {ln.split('\t', 1)[1]: ln.split('\t', 1)[0] for ln in names if ln}
    want = {**{p: 'A' for p in m['new']}, m['install_record']: 'A', **{p: 'M' for p in m['modified']},
            **{p: 'D' for p in m['deleted']}}
    need(got == want, 'the package commit did not change exactly the expected paths; differences (path, status): ' +
         repr(sorted(set(got.items()) ^ set(want.items()))))
    raw = git(repo, 'show', f'HEAD:{m["install_record"]}')
    rec = json.loads(raw.decode('ascii'))
    need(rec.get('schema') == INSTALL_SCHEMA and rec.get('package') == m['package'], 'the install record names another schema or package')
    need(rec.get('manifest_sha256') == MANIFEST_SHA256, 'the install record names another manifest')
    need(rec.get('registry_entries_added') == m['registry_entries_added'], 'the install record\'s registry entries differ')
    need(rec.get('release_entries_planned') == m['release_entries'] and rec.get('retires_planned') == m['retires'],
         'the install record\'s planned release entries differ from the manifest')
    print(f'COMMITTED PASS: the package commit ({head[:7]}) added exactly {len(m["new"])} files and the install record, '
          f'modified {len(m["modified"])} and deleted {len(m["deleted"])}; all Git blobs match; the install record '
          f'names this package and manifest.')


def main(a):
    repo = a.repo.resolve()
    need((repo / '.git').exists(), f'not a Git checkout: {repo}')
    if a.phase == 'released':
        raise RuntimeError('FAIL: the released phase is not built yet (item 3 of the work list). This verifier is a DRAFT.')
    m, expected = load_package()
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    need(run(repo, 'merge-base', '--is-ancestor', m['base_commit'], 'HEAD').returncode == 0,
         f'HEAD {head} does not descend from base {m["base_commit"]}; STOP')
    print('HEAD:', head, '(descends from base', m['base_commit'][:7] + ')')
    {'pre': phase_pre, 'post': phase_post, 'committed': phase_committed}[a.phase](repo, m, expected)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--phase', required=True, choices=['pre', 'post', 'committed', 'released'])
    args = ap.parse_args()
    try:
        main(args)
        print('Read-only: no project code imported, nothing run, nothing changed.')
    except Exception as exc:
        print('VERIFICATION STOP:', exc, file=sys.stderr)
        if args.phase in ('committed', 'released'):
            try:
                identities(args.repo.resolve())
            except Exception as exc2:
                print('(could not list identities:', exc2, ')', file=sys.stderr)
        sys.exit(2)
