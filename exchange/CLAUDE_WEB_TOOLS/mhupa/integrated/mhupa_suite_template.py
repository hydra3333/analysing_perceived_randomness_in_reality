#!/usr/bin/env python3
"""RUN_MHUP_A_SUITE.py - the suite runner of the MHUP-A install package (design Appendix J step 10).

DRAFT (not reviewed). Claude web chat, 10-11 November 2026, from the slice 2 runner.
Runs every test module, each in its own `python -B -m unittest -v` process (no byte-code written), and compares each
module's count with the count the package builder took from the unittest loader. The tests are offline: temporary
registries, method folders, invented masters and run folders, and the project's accepted tests, some of which read
the development masters through the project's reader. They read no holdout, start no Windows process beyond
E2R-T12's ordinary local workers (it needs the owner's approval for each run context), and make no network access.
A skip is allowed only where a test skips because Windows cannot create a symlink (four modules). Anything else
stops. A failing module's output is printed: test failure output; inspect before sharing (R-010).

Two modes:
  --repo REPO            the suite on REPO itself (a tree with no install barriers, e.g. a task clone).
  --repo LIVE --shadow   Appendix J step 10 (N5, owner decision of 11 November 2026, option A in principle): the live
                         tree stays barred throughout; the suite runs on a barrier-free BYTE COPY of the just-installed
                         tree in a private temporary folder. In order, each failure being a STOP:
                         1. the package verifier's POST phase on LIVE passes (U held by this package, E and P present
                            and intact, exactly the package's changes with the expected bytes);
                         2. a new temporary folder outside LIVE; ordinary file copies (no links) of: every tracked
                            file outside source_data/, results/ and transitory_data/, plus the package's new files,
                            minus its deleted file and the barriers; and of the data the accepted tests read, which is
                            only the files listed in DATA_FILES below; each copy compared byte for byte with LIVE, and
                            each package file also with the manifest;
                         3. an escape check: under the suite's own environment, the project's key modules import from
                            the copy, and nothing on the import path is inside LIVE except LIVE's own .venv (the
                            interpreter and installed packages, as on the owner's PC);
                         4. the suite on the copy;
                         5. again, also after any failure: the copy's code and test files still equal LIVE's; POST on
                            LIVE passes again; LIVE gained no file, ignored or not;
                         then the temporary folder is removed (only that folder; checked before removal); a copy
                         that cannot be removed is a STOP too (N5-C01).
Usage: python -I RUN_MHUP_A_SUITE.py --repo REPO [--shadow]
"""
import argparse, hashlib, json, os, platform, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

EXPECTED = [
@@EXPECTED@@
]
TOTAL = sum(n for _m, n in EXPECTED)
SYMLINK_SKIP_OK = {'tests.test_multigame_reader_contracts', 'tests.test_multigame_exit_receipt',
                   'tests.test_e2r_runner', 'tests.test_wf1b_outcome_reader'}
DATA_FILES = [@@DATA_FILES@@]      # the only data the copy receives (the accepted tests read them; nothing else)
DATA_DIRS = ('source_data/', 'results/', 'transitory_data/')
KEY_MODULES = ['_common.contract_dispatch', '_common.contract_runner', '_common.owner_records', '_common.release_records',
               '_common.game_draws_reader', '_common.walk_forward', 'E_001.multigame_e1', 'evaluation.mode_h',
               'evaluation.report', 'test_mhupa_gates']
PREFIX = 'MHUPA_step10_'
HERE = Path(__file__).resolve().parent
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')


class Stop(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(b):
    return b.replace(b'\r\n', b'\n')


def nc(p):
    return os.path.normcase(os.path.realpath(str(p)))


def inside(child, parent):
    c, p = nc(child), nc(parent)
    return c == p or c.startswith(p.rstrip(os.sep) + os.sep)


def suite_env(repo):
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(repo / p) for p in ('src', os.path.join('src', 'methods'), 'tests'))
    return env


def git_lines(repo, *args):
    r = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=GIT_ENV)
    if r.returncode != 0:
        raise Stop(f'git {" ".join(args)} failed: {r.stderr.decode(errors="replace")[:200]}')
    return [x for x in r.stdout.decode('utf-8', errors='replace').split('\0') if x]


# ------------------------------------------------------------------ the suite itself

def run_suite(repo, expected=None):
    expected = EXPECTED if expected is None else expected
    total_want = sum(n for _m, n in expected)
    present = sorted(p.stem for p in (repo / 'tests').glob('test_*.py'))
    listed = sorted(m.split('.', 1)[1] for m, _ in expected)
    if present != listed:
        print('SUITE STOP: the test modules on disk are not the package\'s list:', sorted(set(present) ^ set(listed)))
        return False
    env = suite_env(repo)
    t_all = time.perf_counter()
    bad, total, skipped = [], 0, 0
    for mod, want in expected:
        t0 = time.perf_counter()
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', mod], cwd=repo, env=env,
                           capture_output=True, text=True)
        secs = time.perf_counter() - t0
        err = r.stderr
        m = re.search(r'^Ran (\d+) tests?', err, re.M)
        ran = int(m.group(1)) if m else -1
        last = err.strip().splitlines()[-1] if err.strip() else '(no output)'
        skips = [ln.strip() for ln in err.splitlines() if re.search(r"\.\.\. skipped|\) \.\.\. skipped|skipped '", ln)]
        total += max(ran, 0); skipped += len(skips)
        print(f'{mod:<52} ran {ran:3d} (expected {want:2d})  skipped {len(skips)}  {last}  ({secs:.1f} s)', flush=True)
        for s in skips:
            print('    skip:', s[:200])
        if r.returncode != 0 or ran != want or not last.startswith('OK'):
            bad.append(f'{mod}: exit {r.returncode}, ran {ran} expected {want}, "{last}"')
            detail = [ln for ln in (err + r.stdout).splitlines() if ln.strip()]
            start = next((i for i, ln in enumerate(detail) if ln.startswith(('ERROR:', 'FAIL:'))), max(len(detail) - 40, 0))
            print('    detail (test failure output; inspect before sharing):')
            for ln in detail[start:start + 60]:
                print('    | ' + ln[:200])
        for s in skips:
            if mod not in SYMLINK_SKIP_OK or 'symlink' not in s.lower():
                bad.append(f'{mod}: unexpected skip: {s[:120]}')
    print(f'total ran {total} (expected {total_want}); skips {skipped}; elapsed {time.perf_counter() - t_all:.0f} s')
    if bad:
        print('SUITE STOP:'); [print('  ' + b) for b in bad]
        return False
    return True


# ------------------------------------------------------------------ step 10: the barrier-free copy

def manifest():
    return json.loads((HERE / 'PACKAGE_MANIFEST_MHUP_A.json').read_text(encoding='ascii'))


def post_on_live(live, when):
    r = subprocess.run([sys.executable, '-I', '-B', str(HERE / 'VERIFY_MHUP_A.py'), '--repo', str(live), '--phase', 'post'],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode(errors='replace')
    if r.returncode != 0 or 'POST PASS' not in out:
        raise Stop(f'POST on the live tree does not pass {when}: ' + ' | '.join(out.strip().splitlines()[-3:])[:600])
    print(f'live tree {when}: POST PASS (U held by this package; E and P present; exactly the package\'s changes)')


def live_snapshot(live):
    """Every untracked or ignored path in the live tree (so a test that wrote into it is seen)."""
    return set(git_lines(live, 'status', '--porcelain=v1', '-z', '--ignored', '--untracked-files=all'))


def plan_copy(live, m):
    tracked = git_lines(live, 'ls-files', '-z')
    skip = set(m['deleted']) | set(m['barriers'].values())
    code = sorted((set(p for p in tracked if not p.startswith(DATA_DIRS)) | set(m['new'])) - skip)
    return code, list(DATA_FILES)


def make_shadow(live):
    shadow = Path(tempfile.mkdtemp(prefix=PREFIX)).resolve()
    if inside(shadow, live) or inside(live, shadow):
        raise Stop(f'the temporary folder {shadow} overlaps the live tree')
    return shadow


def copy_into(live, shadow, paths):
    for p in paths:
        src, dst = live / p, shadow / p
        if src.is_symlink() or not src.is_file():
            raise Stop(f'not a plain file in the live tree: {p}')
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)                 # an ordinary copy: never a link back to the live tree


def verify_copy(live, shadow, paths, m):
    expected = {**m['new'], **{p: h[1] for p, h in m['modified'].items()}}
    for p in paths:
        dst = shadow / p
        if dst.is_symlink() or not dst.is_file():
            raise Stop(f'the copy of {p} is missing or not a plain file')
        b = dst.read_bytes()
        if b != (live / p).read_bytes():
            raise Stop(f'the copy of {p} differs from the live file')
        if p in expected and sha(norm(b)) != expected[p]:
            raise Stop(f'the copy of {p} is not the package\'s bytes')


def escape_check(shadow, live):
    env = suite_env(shadow)
    for part in env['PYTHONPATH'].split(os.pathsep):
        if inside(part, live):
            raise Stop(f'the suite\'s import path includes the live tree: {part}')
    code = ('import importlib, json, sys\n'
            'out = {"sys.path": sys.path, "modules": {}}\n'
            'for name in sys.argv[1:]:\n'
            '    out["modules"][name] = importlib.import_module(name).__file__\n'
            'print(json.dumps(out))\n')
    r = subprocess.run([sys.executable, '-B', '-c', code, *KEY_MODULES], cwd=shadow, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        raise Stop('the escape check could not import the key modules from the copy: ' + r.stderr.strip()[-400:])
    got = json.loads(r.stdout.strip().splitlines()[-1])
    for name, f in got['modules'].items():
        if not inside(f, shadow) or inside(f, live):
            raise Stop(f'{name} imports from outside the copy: {f}')
    venv = live / '.venv'               # the project venv lives inside the live tree on the owner's PC: its interpreter
    for p in got['sys.path']:           # and installed packages are not project code, so they are allowed
        if p and inside(p, live) and not inside(p, venv):
            raise Stop(f'the suite\'s sys.path includes the live tree: {p}')
    print(f'escape check: {len(got["modules"])} key modules import from the copy; nothing on the import path is in the live '
          f'tree except its own .venv (interpreter and installed packages)')


def remove_shadow(shadow, live):
    """Remove the temporary copy, and only it. Returns True when it is gone; a copy left behind is a STOP (N5-C01)."""
    if shadow is None:
        return True
    tmp = Path(tempfile.gettempdir()).resolve()
    if not (shadow.name.startswith(PREFIX) and inside(shadow, tmp) and not inside(shadow, live) and shadow != tmp):
        print(f'SUITE STOP: the temporary copy was NOT removed (it failed the removal check): {shadow}')
        return False
    shutil.rmtree(shadow, ignore_errors=True)
    if shadow.exists():
        print(f'SUITE STOP: the temporary copy could not be removed completely: {shadow} (delete that folder by hand '
              f'once nothing uses it; it is outside the repository and holds only copies)')
        return False
    print(f'temporary copy removed: {shadow}')
    return True


def shadow_mode(live):
    m = manifest()
    shadow, ok, code, data, before = None, False, [], [], None
    try:
        post_on_live(live, 'before the suite')
        before = live_snapshot(live)
        code, data = plan_copy(live, m)
        shadow = make_shadow(live)
        copy_into(live, shadow, code + data)
        verify_copy(live, shadow, code + data, m)
        print(f'barrier-free copy at {shadow}: {len(code)} code and test files, {len(data)} data files, each equal to '
              f'the live tree byte for byte; no barrier copied')
        escape_check(shadow, live)
        ok = run_suite(shadow)
    except Stop as exc:
        print('SUITE STOP:', exc)
        ok = False
    finally:
        try:
            if shadow is not None and code:
                verify_copy(live, shadow, code, m)
                print('after the suite: the copy\'s code and test files still equal the live tree')
            post_on_live(live, 'after the suite')
            after = live_snapshot(live)
            if before is not None and after != before:
                raise Stop('the live tree gained or lost untracked or ignored files during the suite: ' +
                           ', '.join(sorted(after ^ before))[:600])
            if before is not None:
                print('after the suite: the live tree gained no file')
        except Stop as exc:
            print('SUITE STOP:', exc)
            ok = False
        ok = remove_shadow(shadow, live) and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--shadow', action='store_true', help='Appendix J step 10: run on a barrier-free copy of the live tree')
    a = ap.parse_args()
    repo = a.repo.resolve()
    print('environment:', platform.system(), platform.release(), 'Python', platform.python_version(), sys.executable, flush=True)
    ok = shadow_mode(repo) if a.shadow else run_suite(repo)
    if not ok:
        print('SUITE STOP: see above. Step 10 has not passed; do not run step 11.' if a.shadow else 'SUITE STOP: see above.')
        sys.exit(1)
    print(f'SUITE PASS: all {TOTAL} tests ran and passed; only the allowed symlink skips, if any' +
          ('; on a barrier-free copy, the live tree barred throughout.' if a.shadow else '.'))


if __name__ == '__main__':
    main()
