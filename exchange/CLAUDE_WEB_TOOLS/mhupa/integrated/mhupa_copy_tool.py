#!/usr/bin/env python3
"""MHUPA_COPY.py - the manifest-controlled copy helper of the MHUP-A install package (design Appendix J steps 4, 6, 8, 15).

DRAFT (items 2 and 3 of the integrated package work list; not yet reviewed). Claude web chat, 10-11 November 2026.
Standard library only. It imports no project code, runs no Git command that writes (two read-only Git queries), and
touches no path the package manifest does not name. Run with the venv's Python from the package folder:
  python -I -B MHUPA_COPY.py barrier --create E --repo REPO     step 4 (then P): create-only, the fixed barrier text
  python -I -B MHUPA_COPY.py copy --part gate --repo REPO       step 6: exactly the manifest's gate_files
  python -I -B MHUPA_COPY.py copy --part rest --repo REPO       step 8: the manifest's rest_files and its deletions
  python -I -B MHUPA_COPY.py barrier --remove E --repo REPO     step 15 (then P): only a file holding exactly that text
  python -I -B MHUPA_COPY.py barrier --remove E --restore --repo REPO   restore steps only (Claude's reviewed steps)
Every command prints one PASS or STOP line and exits 0 or 1. Before writing anything it checks the whole package
(every overlay file against the manifest), the barrier order below and every target's present state; it writes
nothing if any check fails. Each written file is read back and compared. Barrier U (the updater lock) is not this
tool's: process_check.py take-install-lock and release-install-lock own it; this tool only reads its content.

The barrier order of Appendix J, enforced here step by step (EX_148 (ix): U, then E and P, then the gate):
  create E      needs U held by this package, and the package not yet committed
  create P      needs U held by this package, and E present (or, for the STOP handling of steps 16 and 17, the
                install record already committed: P is re-created without E, whatever else has changed)
  copy gate     needs U held, E and P present
  copy rest     needs U held, E and P present, and every gate file already at its new bytes
  remove E      needs U held, P present, and COMMITTED PASS now: it runs the verifier's own committed phase
                (read-only) and refuses unless that passes
  remove P      needs U held, E absent, and the package commit made (a staged release record alone is tolerated, for
                the rerun of step 17)
  remove --restore   needs U held and none of the package's changes left in the working tree (every replaced file
                at its base bytes, every new path and the install record absent, the deleted file back)
"""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'PACKAGE_MANIFEST_MHUP_A.json'
OVERLAY = HERE / 'repo_overlay'
MANIFEST_SHA256 = '@@MANIFEST_SHA256@@'      # the manifest this copy of the tool was built with
INSTALL_LOCK = re.compile(r'INSTALL (?P<package>[A-Za-z0-9_.-]+) (?P<utc>\S+)\Z')   # process_check.py's own format
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')


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
    raw = MANIFEST.read_bytes()
    if sha(raw) != MANIFEST_SHA256:
        raise Stop('the package manifest is not the one this tool was built with')
    m = json.loads(raw.decode('ascii'))
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


def barrier_bytes(m, name):
    return m['barrier_text'].format(name=name).encode('ascii')


def barrier_present(m, repo, name):
    """True only for a plain file holding exactly this package's barrier text; a foreign file is a STOP."""
    t = target(repo, m['barriers'][name])
    if not t.exists() and not t.is_symlink():
        return False
    if t.is_symlink() or not t.is_file() or t.read_bytes() != barrier_bytes(m, name):
        raise Stop(f'barrier {name} exists but does not hold this package\'s text: {m["barriers"][name]}')
    return True


def need_u(m, repo):
    """Barrier U must be held by this package (taken at step 3 by process_check.py, released only at step 18)."""
    t = target(repo, m['barriers']['U'])
    if t.is_symlink() or not t.is_file():
        raise Stop('barrier U (the updater lock) is not held: take-install-lock comes first (Appendix J step 3)')
    mt = INSTALL_LOCK.fullmatch(t.read_text(encoding='ascii', errors='replace').strip())
    if mt is None or mt.group('package') != m['package']:
        raise Stop('barrier U (the updater lock) is not this package\'s install lock')


def rgit(repo, *args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=GIT_ENV)


def install_record_committed(m, repo):
    """The install record is committed at HEAD with the working tree's bytes (read-only)."""
    rec = target(repo, m['install_record'])
    r = rgit(repo, 'show', f'HEAD:{m["install_record"]}')
    return r.returncode == 0 and rec.is_file() and rec.read_bytes() == r.stdout


def committed_pass(repo):
    """COMMITTED PASS itself, now: the package verifier's own committed phase (read-only), not a stand-in."""
    r = subprocess.run([sys.executable, '-I', '-B', str(HERE / 'VERIFY_MHUP_A.py'), '--repo', str(repo), '--phase',
                        'committed'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode == 0 and b'COMMITTED PASS' in r.stdout, r.stdout.decode(errors='replace').strip()


def package_committed(m, repo, allow=()):
    """The package commit has been made: the install record is committed at HEAD with the working tree's bytes, and
    no tracked file differs from HEAD (paths in `allow` excepted). Read-only."""
    rec = target(repo, m['install_record'])
    r = rgit(repo, 'show', f'HEAD:{m["install_record"]}')
    if r.returncode != 0 or not rec.is_file() or rec.read_bytes() != r.stdout:
        return False
    st = rgit(repo, 'status', '--porcelain=v1', '-z', '--no-renames', '--untracked-files=no')
    if st.returncode != 0:
        raise Stop('git status failed: ' + st.stderr.decode(errors='replace')[:200])
    changed = [it[3:] for it in st.stdout.decode('utf-8', errors='replace').split('\0') if it]
    return all(p in allow for p in changed)


def unchanged_tree(m, repo):
    """None of the package's changes is in the working tree (the state the restore steps reach)."""
    for p in m['new']:
        if target(repo, p).exists():
            raise Stop(f'restore: a package file is still present: {p}')
    for p, (old, _new) in m['modified'].items():
        t = target(repo, p)
        if not t.is_file() or sha(norm(t.read_bytes())) != old:
            raise Stop(f'restore: a replaced file is not back at its base bytes: {p}')
    for p, old in m['deleted'].items():
        t = target(repo, p)
        if not t.is_file() or sha(norm(t.read_bytes())) != old:
            raise Stop(f'restore: the deleted file is not back at its base bytes: {p}')
    for p in (m['install_record'], m['release_record']):
        if target(repo, p).exists():
            raise Stop(f'restore: a record exists: {p}')


def repo_root(arg):
    repo = Path(arg).resolve()
    if not (repo / '.git').exists():
        raise Stop(f'not a Git checkout: {repo}')
    return repo


def copy(m, expected, repo, part):
    paths = m['gate_files'] if part == 'gate' else m['rest_files']
    dels = m['deleted'] if part == 'rest' else {}
    need_u(m, repo)                                     # the barrier order: U, then E and P, then the gate
    for name in ('E', 'P'):
        if not barrier_present(m, repo, name):
            raise Stop(f'barrier {name} is absent: no file is copied without U, E and P in place (Appendix J step 4)')
    if part == 'rest':
        for p in m['gate_files']:
            t = target(repo, p)
            if not t.is_file() or sha(norm(t.read_bytes())) != expected[p]:
                raise Stop(f'the gate files are not in place (step 6 comes before step 8): {p}')
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
        tmp = t.with_name(t.name + '.mhupa_tmp')        # written whole beside the target, then put in place in one
        with open(tmp, 'wb') as fh:                     # step, so no reader ever sees a half-written file
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, t)
        if sha(norm(t.read_bytes())) != expected[p]:
            raise Stop(f'written file does not read back with the expected bytes: {p}')
    for p in dels:
        target(repo, p).unlink()
        if target(repo, p).exists():
            raise Stop(f'deleted file still present: {p}')
    return f'COPY PASS: part {part}: {len(paths)} files written and read back' + \
        (f', {len(dels)} deleted' if dels else '')


def barrier(m, repo, name, create, restore=False):
    if name not in ('E', 'P'):
        raise Stop('barrier must be E or P (U belongs to process_check.py)')
    rel = m['barriers'][name]
    t = target(repo, rel)
    text = barrier_bytes(m, name)
    need_u(m, repo)
    if create:
        if restore:
            raise Stop('--restore applies to --remove only')
        if name == 'E':
            if target(repo, m['install_record']).exists():
                raise Stop('barrier E is created at step 4 only; the install record already exists')
        elif not barrier_present(m, repo, 'E') and not install_record_committed(m, repo):
            raise Stop('barrier P follows barrier E (step 4); it is re-created without E only after the package commit '
                       '(the STOP handling of steps 16 and 17)')
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
    if restore:
        unchanged_tree(m, repo)
    elif name == 'E':
        if not barrier_present(m, repo, 'P'):
            raise Stop('barrier E is removed before P (step 15); P is absent')
        ok, out = committed_pass(repo)
        if not ok:
            raise Stop('barrier E is removed only after COMMITTED PASS (step 15), and the verifier\'s committed phase '
                       'does not pass now: ' + (out.splitlines() or ['(no output)'])[0][:300])
    else:
        if barrier_present(m, repo, 'E'):
            raise Stop('barrier P is removed after E (step 15); E is still present')
        if not package_committed(m, repo, allow=(m['release_record'],)):
            raise Stop('barrier P is removed only after the package commit (step 15): the install record is not '
                       'committed at HEAD, or tracked files differ from HEAD')
    t.unlink()
    return f'BARRIER PASS: {name} removed ({rel})' + (' (restore)' if restore else '')


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
    b.add_argument('--restore', action='store_true', help='with --remove: the restore steps (no package change left)')
    b.add_argument('--repo', required=True)
    a = ap.parse_args(argv)
    try:
        m, expected = load()
        repo = repo_root(a.repo)
        if a.cmd == 'copy':
            print(copy(m, expected, repo, a.part))
        else:
            print(barrier(m, repo, a.create or a.remove, bool(a.create), a.restore))
        return 0
    except (Stop, OSError, ValueError, KeyError) as exc:
        print(f'COPY STOP: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
