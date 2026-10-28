#!/usr/bin/env python3
"""Read-only installation verifier for NAMES-1 (one-off rename to stable file names; register v0.8).

Claude, 28 October 2026. Standard library only; does not import project code, run tests, change
files or touch Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0). It never
reads source_data/, results/ or transitory_data/.
Phases:
  pre        clean tree; HEAD descends from the base commit and has register v0.7 (DOC-2 installed);
             every file NAMES-1 touches is at its base bytes in Git; every new path is absent;
             guarded files unchanged.
  post       after RENAME_FILES.cmd and copying the overlay: the index holds exactly the 27 renames;
             the working tree differs from the index in exactly the edited files; exactly the new
             files are untracked; every file has its expected bytes (CRLF tolerated for text);
             no old path remains; no live file names an old module (N1-T01).
  committed  after the commit: clean tree; the last commit deleted the 27 old paths, added the 27
             new ones and the new files, and modified exactly the 3 edited-in-place files, all with
             the expected Git blobs; each pure rename's blob equals its predecessor's.
Usage: python VERIFY_NAMES1_INSTALL.py --repo . --phase pre|post|committed
"""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path

BASE = '@@BASE@@'
REG_V07 = ('doc/RATIFICATION_REGISTER_v0_7.md', 'f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015')
DATA = json.loads(r'''@@DATA@@''')
RENAMES = DATA['renames']            # old path -> new path (27)
BASE_SHA = DATA['base_sha']          # every touched base path -> its Git blob SHA-256
NEW_SHA = DATA['new_sha']            # every path with new bytes (edited files and new files) -> SHA-256
IN_PLACE = DATA['in_place']          # edited without a rename (3)
NEW_FILES = DATA['new_files']        # added files (docs, history, evidence)
OLD_NAMES = DATA['old_names']        # old module base names, for the N1-T01 scan
GUARDED = DATA['guarded']            # must stay byte-identical in Git
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
HERE = Path(__file__).resolve().parent
SKIP_SCAN = ('review', 'doc', 'transitory_data', 'exchange', 'source_data', 'results', '.git', '.venv')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(p, b):
    return b if p.endswith('.zip') else b.replace(b'\r\n', b'\n')


def git(repo, *args):
    r = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=GIT_ENV)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--phase', required=True, choices=['pre', 'post', 'committed'])
    a = ap.parse_args()
    repo = a.repo.resolve()
    need((repo / '.git').exists(), f'not a Git checkout: {repo}')
    for p, h in NEW_SHA.items():  # the package itself must be intact
        need(sha(norm(p, (HERE / 'repo_overlay' / p).read_bytes())) == h, f'package file damaged: {p}')
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    anc = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), 'merge-base', '--is-ancestor', BASE, 'HEAD'],
                         env=GIT_ENV)
    need(anc.returncode == 0, f'HEAD {head} does not descend from base {BASE}; STOP')
    print('HEAD:', head, '(descends from base', BASE[:7] + ')')
    reg = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), 'show', f'HEAD:{REG_V07[0]}'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=GIT_ENV)
    need(reg.returncode == 0 and sha(reg.stdout) == REG_V07[1], 'register v0.7 not installed: install DOC-2 first; STOP')
    for p, h in GUARDED.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'guarded file changed in Git: {p}')
    print(f'{len(GUARDED)} guarded files unchanged in Git HEAD')
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode(errors='replace')

    if a.phase == 'pre':
        need(not status.strip(), 'working tree or index not clean:\n' + status[:600])
        for p, h in BASE_SHA.items():
            need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'file to be renamed or edited is not at its base bytes: {p}')
        for p in list(RENAMES.values()) + list(NEW_FILES):
            need(not (repo / p).exists(), f'new path already exists: {p}; STOP')
        print(f'PRE PASS: clean tree; DOC-2 installed; {len(BASE_SHA)} files at their base bytes; '
              f'{len(RENAMES) + len(NEW_FILES)} new paths absent. Nothing was changed.')
        return

    if a.phase == 'post':
        idx = name_status(git(repo, 'diff', '--cached', '--no-renames', '--name-status'))
        want_idx = dict({o: 'D' for o in RENAMES}, **{n: 'A' for n in RENAMES.values()})
        need(idx == want_idx, 'index is not exactly the 27 renames: ' + ', '.join(map(str, sorted(set(idx.items()) ^ set(want_idx.items()))))[:900])
        wt = name_status(git(repo, 'diff', '--no-renames', '--name-status'))
        edited = sorted(p for p in NEW_SHA if p not in NEW_FILES)
        want_wt = {p: 'M' for p in edited}
        need(wt == want_wt, 'working tree changes are not exactly the edited files: ' + ', '.join(map(str, sorted(set(wt.items()) ^ set(want_wt.items()))))[:900])
        untracked = {ln[3:].strip().strip('"') for ln in status.splitlines() if ln.startswith('??')}
        need(untracked == set(NEW_FILES), 'untracked files are not exactly the new files: ' + ', '.join(sorted(untracked ^ set(NEW_FILES)))[:900])
        for p, h in NEW_SHA.items():
            f = repo / p
            need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
            need(sha(norm(p, f.read_bytes())) == h, f'wrong bytes: {p}')
        for o, n in RENAMES.items():
            need(not (repo / o).exists(), f'old path still present: {o}')
            if n not in NEW_SHA:  # pure rename: bytes unchanged
                need(sha(norm(n, (repo / n).read_bytes())) == BASE_SHA[o], f'pure rename changed bytes: {n}')
        pat = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, OLD_NAMES), key=len, reverse=True)) + r')\b')
        hits, stray = [], []
        live = []
        for root, dirs, names in os.walk(repo):
            r = Path(root)
            dirs[:] = sorted(d for d in dirs if d != '__pycache__' and not (r == repo and d in SKIP_SCAN))
            live.extend(r / n for n in sorted(names))
        for f in live:
            rel = f.relative_to(repo)
            if f.is_symlink() or not f.is_file():
                continue
            if rel.parts[0] in ('src', 'tests') and f.suffix in ('.py', '.pyc') and f.stem.split('.')[0] in OLD_NAMES:
                stray.append(rel.as_posix())
            try:
                txt = f.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                continue
            if pat.search(txt):
                hits.append(rel.as_posix())
        need(not stray, 'old-name .py/.pyc outside __pycache__: ' + ', '.join(stray))
        need(not hits, 'live files still name an old module: ' + ', '.join(hits))
        print(f'POST PASS: index has exactly the {len(RENAMES)} renames; exactly {len(edited)} edited and '
              f'{len(NEW_FILES)} new files, all with the expected bytes; no old path or old name in live files.')
        return

    need(not status.strip(), 'working tree or index not clean after commit:\n' + status[:600])
    got = name_status(git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD'))
    want = dict({o: 'D' for o in RENAMES}, **{n: 'A' for n in RENAMES.values()},
                **{p: 'A' for p in NEW_FILES}, **{p: 'M' for p in IN_PLACE})
    need(got == want, 'the last commit did not change exactly the expected paths: ' + ', '.join(map(str, sorted(set(got.items()) ^ set(want.items()))))[:900])
    for p, h in NEW_SHA.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'wrong Git blob in HEAD: {p}')
    for o, n in RENAMES.items():
        if n not in NEW_SHA:
            need(git(repo, 'show', f'HEAD:{n}') == git(repo, 'show', f'HEAD~1:{o}'), f'pure rename changed bytes: {n}')
    print(f'COMMITTED PASS: the last commit made the {len(RENAMES)} renames, edited {len(NEW_SHA) - len(NEW_FILES)} files '
          f'and added {len(NEW_FILES)}; all Git blobs match.')


if __name__ == '__main__':
    try:
        main()
        print('Read-only: no project code imported, nothing run, nothing changed.')
    except Exception as exc:
        print('VERIFICATION STOP:', exc, file=sys.stderr)
        sys.exit(2)
