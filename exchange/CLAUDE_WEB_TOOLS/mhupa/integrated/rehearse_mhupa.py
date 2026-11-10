#!/usr/bin/env python3
"""Rehearse the DRAFT MHUP-A install package in scratch clones (Claude web chat, 11 November 2026; a working tool).

  rehearse_mhupa.py positive  MIRROR PKG WORK PYTHON lf|crlf [--suite]
      Appendix J steps 0 to 18 in order, in a FULL scratch clone of the frozen mirror (step 19, the push, is omitted).
      Any step that does not give its expected output ends the run at that step with REHEARSAL STOP: nothing after
      a STOP is run (owner decision D07, finding S1). With --suite, step 10 runs the whole suite with U, E and P
      in place; without it the run is labelled as omitting step 10.
  rehearse_mhupa.py negatives MIRROR PKG WORK PYTHON
      Every negative on a synthetic root (the data folders removed by a local commit; empty source_data/ and
      results/ placeholders). Each case must STOP at the named step with the named message; where Appendix J
      prescribes a STOP handling (steps 16 and 17: re-create P, U stays held), the handling is applied and the end
      state is checked; nothing continues past a STOP.
Nothing is pushed; WORK is the only place written. The tools are run from a staging copy of the package, with the
interpreter options the instructions give.
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

GITID = ['-c', 'user.name=rehearsal', '-c', 'user.email=rehearsal@invalid']


class Ctx:
    def __init__(self, pkg_src, work, python):
        self.work, self.python = Path(work), python
        self.pkg = self.work / 'stage'
        shutil.copytree(pkg_src, self.pkg)
        self.man = self.pkg / 'PACKAGE_MANIFEST_MHUP_A.json'
        self.m = json.loads(self.man.read_text(encoding='ascii'))

    def tools(self, repo):
        py = [self.python, '-I', '-B']
        pyx = py + ['-X', f'pycache_prefix={repo}/transitory_data/no_pycache_ever']
        pc = pyx + [str(self.pkg / 'repo_overlay/src/package_tools/process_check.py')]
        ir = pyx + [str(self.pkg / 'repo_overlay/src/package_tools/install_records.py')]
        ver = py + [str(self.pkg / 'VERIFY_MHUP_A.py'), '--repo', str(repo), '--phase']
        cp = py + [str(self.pkg / 'MHUPA_COPY.py')]
        r, man = str(repo), str(self.man)
        g = ['git', '-C', r, *GITID]
        return {
            'pre': ver + ['pre'], 'check': pc + ['check-no-runs', '--root', r, '--install', man],
            'takeU': pc + ['take-install-lock', '--root', r, '--package', 'MHUP_A'],
            'mkE': cp + ['barrier', '--create', 'E', '--repo', r], 'mkP': cp + ['barrier', '--create', 'P', '--repo', r],
            'gate': cp + ['copy', '--part', 'gate', '--repo', r], 'rest': cp + ['copy', '--part', 'rest', '--repo', r],
            'post': ver + ['post'],
            'suite': [self.python, '-I', str(self.pkg / 'RUN_MHUP_A_SUITE.py'), '--repo', r, '--shadow'],
            'irec': ir + ['install-record', '--root', r, '--package', 'MHUP_A', '--manifest', man],
            'add1': g + ['add', f'--pathspec-from-file={self.pkg / "STAGE_PACKAGE_COMMIT.txt"}'],
            'commit1': g + ['commit', '-q', '-m', 'MHUP-A rehearsal: package commit'],
            'staged': ver + ['staged'], 'committed': ver + ['committed'],
            'rmE': cp + ['barrier', '--remove', 'E', '--repo', r], 'rmP': cp + ['barrier', '--remove', 'P', '--repo', r],
            'rrec': ir + ['release-record', '--root', r, '--package', 'MHUP_A', '--manifest', man],
            'add2': g + ['add', f'--pathspec-from-file={self.pkg / "STAGE_RELEASE_COMMIT.txt"}'],
            'commit2': g + ['commit', '-q', '-m', 'MHUP-A rehearsal: release commit'],
            'released': ver + ['released'], 'validate': ir + ['validate', '--root', r],
            'dropU': pc + ['release-install-lock', '--root', r, '--package', 'MHUP_A'],
        }


def sh(cmd, **kw):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, **kw)
    return r.returncode, r.stdout


def git(repo, *args):
    rc, out = sh(['git', '-C', str(repo), *GITID, *args])
    if rc:
        raise SystemExit(f'git {" ".join(args)} failed: {out}')
    return out


def clone(mirror, dest, mode, synthetic):
    extra = ['-c', 'core.autocrlf=true'] if mode == 'crlf' else []
    rc, out = sh(['git', *extra, 'clone', '-q', str(mirror), str(dest)])
    if rc:
        raise SystemExit(out)
    if mode == 'crlf':
        git(dest, 'config', 'core.autocrlf', 'true')
    if synthetic:
        git(dest, 'rm', '-r', '-q', '--cached', 'source_data', 'results', 'transitory_data')
        for d in ('source_data', 'results', 'transitory_data'):
            shutil.rmtree(dest / d, ignore_errors=True)
        (dest / 'source_data').mkdir()
        (dest / 'results').mkdir()
        git(dest, 'commit', '-q', '-m', 'SYNTHETIC ROOT for the rehearsal: data folders removed (local only)')


# (step label, tool key, text the output must contain)
FORWARD = [
    ('1 PRE', 'pre', 'PRE PASS'), ('2 install check', 'check', 'CLEAN'), ('3 take U', 'takeU', 'CLEAN; install lock taken'),
    ('4 create E', 'mkE', 'BARRIER PASS: E created'), ('4 create P', 'mkP', 'BARRIER PASS: P created'),
    ('5 install check', 'check', 'CLEAN'), ('6 copy gate', 'gate', 'COPY PASS: part gate'),
    ('7 install check', 'check', 'CLEAN'), ('8 copy rest', 'rest', 'COPY PASS: part rest'), ('9 POST', 'post', 'POST PASS'),
    ('10 suite', 'suite', 'SUITE PASS'), ('11 install check', 'check', 'CLEAN'),
    ('12 install record', 'irec', 'INSTALL RECORD PASS'), ('12 stage', 'add1', ''), ('12 STAGED', 'staged', 'STAGED PASS'),
    ('12 commit', 'commit1', ''),
    ('13 COMMITTED', 'committed', 'COMMITTED PASS'), ('14 install check', 'check', 'CLEAN'),
    ('15 remove E', 'rmE', 'BARRIER PASS: E removed'), ('15 remove P', 'rmP', 'BARRIER PASS: P removed'),
    ('16 release record', 'rrec', 'RELEASE RECORD PASS'), ('17 stage', 'add2', ''), ('17 STAGED', 'staged', 'STAGED PASS'),
    ('17 commit', 'commit2', ''), ('17 RELEASED', 'released', 'RELEASED PASS'),
    ('(rehearsal only) the project reader validates the records', 'validate', 'RECORDS PASS'),
    ('18 RELEASED again', 'released', 'RELEASED PASS'), ('18 release U', 'dropU', 'CLEAN; install lock released'),
]


def forward(ctx, repo, upto=None, skip=(), quiet=True, log=print):
    """Run the forward steps in order until (and including) the step whose label is `upto`. Returns (ok, label)."""
    t = ctx.tools(repo)
    for label, key, want in FORWARD:
        if key in skip:
            if not quiet:
                log(f'--- step {label}: OMITTED in this run')
        else:
            rc, out = sh(t[key])
            ok = rc == 0 and want in out
            if not quiet or not ok:
                keep = [ln for ln in out.splitlines() if not ln.startswith('warning: in the working copy')]
                log(f'--- step {label}\n' + '\n'.join('    ' + ln[:220] for ln in keep[-6 if quiet else -60:]) + f'\n    (exit {rc})')
            if not ok:
                return False, label
        if label == upto:
            break
    return True, upto


def state(ctx, repo):
    b = ctx.m['barriers']
    u = repo / b['U']
    return {'U': u.read_text().split()[1] if u.is_file() else None, 'E': (repo / b['E']).is_file(), 'P': (repo / b['P']).is_file()}


def positive(mirror, pkg, work, python, mode, with_suite):
    work = Path(work)
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    ctx = Ctx(pkg, work, python)
    repo = work / 'repo'
    clone(mirror, repo, mode, synthetic=False)
    print(f'REHEARSAL (PRELIMINARY, DRAFT package): positive path, {mode} clone, Python {python}; base '
          f'{ctx.m["base_commit"][:7]}; HEAD {git(repo, "rev-parse", "HEAD").strip()[:7]}; step 10 '
          + ('INCLUDED (the suite runs with U, E and P in place)' if with_suite else 'OMITTED'), flush=True)
    rc, out = sh(['git', '-C', str(repo), 'status', '--short'])
    print('--- step 0 (rehearsal form: no pull; clean tree): ' + ('clean' if not out.strip() else 'NOT CLEAN'))
    if out.strip():
        print('REHEARSAL STOP at step 0')
        return 1
    ok, label = forward(ctx, repo, skip=() if with_suite else ('suite',), quiet=False, log=lambda s: print(s, flush=True))
    if not ok:
        print(f'REHEARSAL STOP at step {label}; nothing after it was run; barrier state {state(ctx, repo)}')
        return 1
    st = state(ctx, repo)
    nopyc = (repo / 'transitory_data' / 'no_pycache_ever').exists()
    caches = sum(1 for _ in (ctx.pkg).rglob('__pycache__'))
    print(f'end state: barriers {st}; no_pycache_ever exists: {nopyc}; __pycache__ in staging: {caches}; '
          f'status lines: {len(git(repo, "status", "--short").splitlines())}')
    print(git(repo, 'log', '--oneline', '-3').rstrip())
    if st != {'U': None, 'E': False, 'P': False} or nopyc or caches:
        print('REHEARSAL STOP: unexpected end state')
        return 1
    print(f'REHEARSAL PASS ({mode}; step 10 ' + ('included' if with_suite else 'OMITTED') + '; step 19 omitted)')
    return 0


# ------------------------------------------------------------------ negatives

class Neg:
    def __init__(self, ctx, mirror):
        self.ctx, self.mirror, self.n, self.bad = ctx, mirror, 0, 0
        self.base = ctx.work / 'base'
        clone(mirror, self.base, 'lf', synthetic=True)
        self.snaps = {}

    def snap(self, upto):
        """A prepared repository: the forward steps (the suite omitted) run up to and including `upto`."""
        if upto not in self.snaps:
            d = self.ctx.work / ('snap_' + upto.replace(' ', '_'))
            shutil.copytree(self.base, d, symlinks=True)
            if upto != 'base':
                ok, label = forward(self.ctx, d, upto=upto, skip=('suite',))
                if not ok:
                    raise SystemExit(f'could not prepare the state after step {upto}: stopped at {label}')
            self.snaps[upto] = d
        self.n_case = getattr(self, 'n_case', 0) + 1
        d = self.ctx.work / f'case_{self.n_case:02d}'
        shutil.copytree(self.snaps[upto], d, symlinks=True)
        return d

    def expect(self, label, cmd, want_text, stop=True):
        rc, out = sh(cmd)
        hit = [ln for ln in out.splitlines() if want_text in ln]
        ok = (rc != 0 if stop else rc == 0) and bool(hit)
        self.n += 1
        self.bad += not ok
        verdict = ('STOPPED as required' if stop else 'PASSED as required') if ok else 'NEGATIVE FAILED'
        shown = (hit[0] if hit else (out.strip().splitlines() or ['(no output)'])[-1]).strip()
        print(f'[{self.n:02d}] {verdict}: {label}\n       -> {shown[:230]}', flush=True)
        return ok

    def check_state(self, repo, want, note):
        got = state(self.ctx, repo)
        got['U'] = got['U'] == 'MHUP_A'
        ok = got == want
        self.n += 1
        self.bad += not ok
        print(f'[{self.n:02d}] ' + ('STATE as required' if ok else 'NEGATIVE FAILED (state)') + f': {note}\n       -> {got}', flush=True)


def negatives(mirror, pkg, work, python):
    work = Path(work)
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    ctx = Ctx(pkg, work, python)
    N = Neg(ctx, mirror)
    m = ctx.m
    print('NEGATIVES (PRELIMINARY, DRAFT package) on a synthetic root; each must STOP; nothing continues past a STOP.\n')

    print('A. The package and PRE (step 1)')
    r = N.snap('base'); t = ctx.tools(r)
    victim = ctx.pkg / 'repo_overlay' / m['gate_files'][0]
    orig = victim.read_bytes(); victim.write_bytes(orig + b'#x\n')
    N.expect('a damaged package file: PRE', t['pre'], 'package file missing or damaged')
    victim.write_bytes(orig)
    (r / 'stray.txt').write_text('stray\n')
    N.expect('an untracked file: PRE', t['pre'], 'working tree or index not clean')
    r = N.snap('base'); t = ctx.tools(r)
    (r / 'source_data' / '.results_master.lock').write_text('some update')
    N.expect('an updater lock already present: PRE', t['pre'], 'barrier U: an updater lock exists')
    r = N.snap('base'); t = ctx.tools(r)                      # F1 (owner decision D03): later non-package commits
    for p in ('CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md', '.claude/settings.json'):
        with open(r / p, 'ab') as fh:
            fh.write(b'\n')
        git(r, 'add', p)
    git(r, 'commit', '-q', '-m', 'a rulebook and settings commit after the base (no package path)')
    N.expect('F1: a descendant with only rulebook and settings commits: PRE passes', t['pre'], 'PRE PASS', stop=False)
    with open(r / '.gitignore', 'ab') as fh:
        fh.write(b'# later line\n')
    git(r, 'add', '.gitignore'); git(r, 'commit', '-q', '-m', 'a later change to a package path')
    N.expect('F1: a later commit that changes a package path (.gitignore): PRE', t['pre'], 'file to be replaced is not its base version')
    r = N.snap('base'); t = ctx.tools(r)
    (r / 'src' / 'later_module.py').write_text('x = 1\n')
    git(r, 'add', 'src/later_module.py'); git(r, 'commit', '-q', '-m', 'a later change under src')
    N.expect('F1: a later commit under src/: PRE', t['pre'], 'src/ or tests/ changed since the base commit')

    print('\nB. The barrier order, enforced by the copy tool (steps 3 to 8, 15)')
    r = N.snap('base'); t = ctx.tools(r)
    N.expect('create E before U is taken', t['mkE'], 'barrier U (the updater lock) is not held')
    N.expect('copy the gate files with no barrier at all', t['gate'], 'barrier U (the updater lock) is not held')
    r = N.snap('3 take U'); t = ctx.tools(r)
    N.expect('create P before E', t['mkP'], 'barrier P follows barrier E')
    N.expect('copy the gate files with U only', t['gate'], 'barrier E is absent')
    sh(t['mkE'])
    N.expect('copy the gate files with U and E but no P', t['gate'], 'barrier P is absent')
    r = N.snap('4 create P'); t = ctx.tools(r)
    N.expect('copy the rest before the gate files', t['rest'], 'the gate files are not in place')
    N.expect('remove E before the package commit', t['rmE'], 'does not pass now')
    (r / m['barriers']['U']).write_text('INSTALL OTHER_PKG 2026-11-11T00:00:00.000000Z')
    N.expect('copy the gate files while U names another package', t['gate'], 'not this package\'s install lock')
    r = N.snap('4 create P'); t = ctx.tools(r)
    (r / m['barriers']['P']).write_text('not ours\n')
    N.expect('copy the gate files with a foreign P', t['gate'], 'does not hold this package\'s text')
    r = N.snap('6 copy gate'); t = ctx.tools(r)
    N.expect('copy the gate files a second time', t['gate'], 'not at its base bytes')
    N.expect('restore-removal of E while package files are in place', t['rmE'] + ['--restore'], 'restore: a')
    r = N.snap('13 COMMITTED'); t = ctx.tools(r)
    N.expect('remove P before E (step 15 order)', t['rmP'], 'barrier P is removed after E')
    (r / 'stray.txt').write_text('x\n')
    N.expect('remove E when COMMITTED would not pass now (a stray file)', t['rmE'], 'does not pass now')
    r = N.snap('4 create P'); t = ctx.tools(r)               # the restore path at step 4: nothing copied yet
    N.expect('restore-removal of E with nothing copied: passes', t['rmE'] + ['--restore'], 'BARRIER PASS: E removed', stop=False)
    N.expect('restore-removal of P with nothing copied: passes', t['rmP'] + ['--restore'], 'BARRIER PASS: P removed', stop=False)

    print('\nC. POST (step 9)')
    r = N.snap('8 copy rest'); t = ctx.tools(r)
    (r / m['gate_files'][-1]).unlink()
    N.expect('a missing new file: POST names it MISSING (R-008)', t['post'], 'MISSING (expected, not seen): ' + m['gate_files'][-1])
    r = N.snap('8 copy rest'); t = ctx.tools(r)
    (r / 'src' / 'extra.py').write_text('x = 1\n')
    N.expect('an extra file: POST names it UNEXPECTED', t['post'], 'UNEXPECTED (seen, not expected): src/extra.py')
    r = N.snap('8 copy rest'); t = ctx.tools(r)
    with open(r / m['gate_files'][0], 'ab') as fh:
        fh.write(b'#\n')
    N.expect('one wrong byte: POST', t['post'], 'wrong bytes: ' + m['gate_files'][0])
    r = N.snap('8 copy rest'); t = ctx.tools(r)
    (r / m['barriers']['P']).unlink()
    N.expect('P missing at POST', t['post'], 'barrier P is absent')

    print('\nD. The package commit and COMMITTED (steps 12 and 13)')
    r = N.snap('12 stage'); t = ctx.tools(r)
    (r / 'extra.txt').write_text('x\n'); git(r, 'add', 'extra.txt')
    N.expect('an extra staged file before the package commit: STAGED', t['staged'], 'UNEXPECTED: A extra.txt')
    r = N.snap('12 stage'); t = ctx.tools(r)
    git(r, 'reset', '-q', '--', m['gate_files'][0])
    N.expect('a package file left unstaged before the package commit: STAGED', t['staged'], 'MISSING or wrongly staged: ' + m['gate_files'][0])
    r = N.snap('9 POST'); t = ctx.tools(r)
    other = ctx.work / 'OTHER_MANIFEST.json'
    other.write_bytes(ctx.man.read_bytes() + b'\n')
    sh(t['irec'][:-1] + [str(other)]); sh(t['add1']); sh(t['commit1'])
    N.expect('a wrong install record (it names another manifest): COMMITTED', t['committed'], 'the install record names another manifest')
    r = N.snap('9 POST'); t = ctx.tools(r)
    sh(t['irec']); sh(t['add1']); (r / 'extra.txt').write_text('x\n'); git(r, 'add', 'extra.txt'); sh(t['commit1'])
    N.expect('an extra file in the package commit: COMMITTED', t['committed'], 'did not change exactly the expected paths')
    r = N.snap('9 POST'); t = ctx.tools(r)
    short = ctx.work / 'STAGE_WITHOUT_RECORD.txt'
    short.write_text(''.join(ln for ln in (ctx.pkg / 'STAGE_PACKAGE_COMMIT.txt').read_text().splitlines(True)
                             if ln.strip() != m['install_record']))
    git(r, 'add', f'--pathspec-from-file={short}'); sh(t['commit1'])
    N.expect('the package commit without the install record: COMMITTED', t['committed'], 'did not change exactly the expected paths')
    r = N.snap('12 commit'); t = ctx.tools(r)
    (r / m['barriers']['E']).unlink()
    N.expect('E missing at COMMITTED', t['committed'], 'barrier E is absent')
    r = N.snap('12 commit'); t = ctx.tools(r)
    (r / m['barriers']['U']).unlink()
    N.expect('U not held at COMMITTED', t['committed'], 'barrier U (the install lock) is not held')

    print('\nE. The release record (step 16)')
    r = N.snap('15 remove E'); t = ctx.tools(r)
    N.expect('the release record while P still exists', t['rrec'], 'the install barrier P still exists')
    N.check_state(r, {'U': True, 'E': False, 'P': True}, 'after that STOP: P present, U held, nothing released')
    r = N.snap('15 remove P'); t = ctx.tools(r)               # a tracked file changed between steps 15 and 16
    with open(r / 'README.md', 'ab') as fh:
        fh.write(b'\n')
    N.expect('the release record while a tracked file differs from HEAD', t['rrec'], 'tracked files differ from HEAD')
    N.expect('   handling: P can be re-created although a tracked file differs', t['mkP'], 'BARRIER PASS: P created', stop=False)
    N.check_state(r, {'U': True, 'E': False, 'P': True}, '   end state: P re-created, E absent, U held')
    r = N.snap('17 stage'); t = ctx.tools(r)
    (r / 'extra.txt').write_text('x\n'); git(r, 'add', 'extra.txt')
    N.expect('an extra staged file before the release commit: STAGED', t['staged'], 'UNEXPECTED: A extra.txt')
    r = N.snap('13 COMMITTED'); t = ctx.tools(r)
    N.expect('the released phase before any release commit', t['released'], 'barrier E exists')

    print('\nF. The release commit and RELEASED (step 17): each STOP is followed by its Appendix J handling\n'
          '   (re-create P; U stays held; step 18 is NOT run), and the end state is checked')

    def handled(r, t, label, text):
        if N.expect(label + ': RELEASED', t['released'], text):
            N.expect('   handling: re-create P', t['mkP'], 'BARRIER PASS: P created', stop=False)
            N.check_state(r, {'U': True, 'E': False, 'P': True}, '   end state: P re-created, E absent, U held; step 18 not run')
            N.expect('   and with P back, RELEASED cannot pass until the fix', t['released'], 'barrier P exists')

    r = N.snap('17 stage'); t = ctx.tools(r)
    (r / 'extra.txt').write_text('x\n'); git(r, 'add', 'extra.txt'); sh(t['commit2'])
    handled(r, t, 'an extra file in the release commit', 'did not add exactly the release record')
    r = N.snap('16 release record'); t = ctx.tools(r)
    (r / 'between.txt').write_text('x\n'); git(r, 'add', 'between.txt'); git(r, 'commit', '-q', '-m', 'a commit in between')
    sh(t['add2']); sh(t['commit2'])
    handled(r, t, 'the wrong parent (a commit between the package commit and the release commit)', 'only parent is not the package commit')
    r = N.snap('16 release record'); t = ctx.tools(r)
    git(r, 'checkout', '-q', '-b', 'side', 'HEAD~1'); (r / 'side.txt').write_text('x\n'); git(r, 'add', 'side.txt')
    git(r, 'commit', '-q', '-m', 'side'); git(r, 'checkout', '-q', '-')
    sh(t['add2']); git(r, 'stash', '-q'); git(r, 'merge', '-q', '--no-ff', '--no-commit', 'side'); git(r, 'stash', 'pop', '-q')
    sh(t['add2']); sh(t['commit2'])
    handled(r, t, 'the release commit is a merge (two parents)', 'has 2 parents')

    def forged(change, label, text):
        r = N.snap('16 release record'); t = ctx.tools(r)
        p = r / m['release_record']
        rec = json.loads(p.read_text())
        change(rec)
        p.write_bytes((json.dumps(rec, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii'))
        sh(t['add2']); sh(t['commit2'])
        handled(r, t, label, text)

    forged(lambda rec: rec['entries'].pop(), 'a release record naming one game only', 'entries are not exactly the manifest')
    forged(lambda rec: rec.__setitem__('install_record_sha256', '0' * 64), 'a release record naming another install record', 'does not name the committed install record')
    forged(lambda rec: rec.__setitem__('local_date', '2026-10-01'), 'a release record dated before the install record', 'local date is before the install record')
    forged(lambda rec: rec.__setitem__('released_utc', '2026-01-01T00:00:00.000000Z'), 'a release record timed before the install record', 'the recorded order is not')
    forged(lambda rec: rec.__setitem__('retires', [rec['entries'][0]]), 'a release record with a retirement the manifest lacks', 'retirements are not the manifest')
    r = N.snap('16 release record'); t = ctx.tools(r)
    p = r / m['release_record']; p.write_bytes(p.read_bytes().replace(b',', b', ', 1)); sh(t['add2']); sh(t['commit2'])
    handled(r, t, 'a release record that is not canonical bytes', 'not its canonical bytes')
    r = N.snap('17 commit'); t = ctx.tools(r)
    p = r / m['release_record']; p.write_bytes(p.read_bytes().replace(b'\n', b'\r\n'))
    git(r, 'update-index', '--assume-unchanged', m['release_record'])
    handled(r, t, 'the release record converted to CRLF in the working tree (N1)', 'not the committed bytes')
    r = N.snap('17 commit'); t = ctx.tools(r)
    (r / 'untracked.txt').write_text('x\n')
    handled(r, t, 'an untracked file after the release commit', 'not clean after the release commit')
    r = N.snap('17 commit'); t = ctx.tools(r)
    sh(t['dropU'])
    N.expect('U released early (step 18 before RELEASED): RELEASED', t['released'], 'barrier U (the install lock) is not held')
    r = N.snap('17 commit'); t = ctx.tools(r)
    (r / m['barriers']['U']).write_text('INSTALL OTHER_PKG 2026-11-11T00:00:00.000000Z')
    N.expect('U naming another package: RELEASED', t['released'], 'not this package\'s install lock')
    N.expect('   and step 18 refuses to remove a lock that is not this package\'s', t['dropU'], 'does not name this package')
    r = N.snap('17 commit'); t = ctx.tools(r)
    N.expect('control: the unaltered state passes RELEASED', t['released'], 'RELEASED PASS', stop=False)
    N.expect('control: and the project\'s own reader validates the records', t['validate'], 'RECORDS PASS', stop=False)

    print(f'\nNEGATIVES: {N.n} checks, {N.bad} failed')
    print('NEGATIVES PASS' if not N.bad else 'NEGATIVES STOP')
    return 1 if N.bad else 0


# ------------------------------------------------------------------ step 10 (N5): the barrier-free copy's negatives

def step10(mirror, pkg, work, python):
    """On a FULL clone brought to the state after step 9: the real runner's refusals from the command line, and the
    failures that need an injection, through the runner imported as a module (subprocess-free stubs only)."""
    import importlib.util, io, contextlib, tempfile
    work = Path(work)
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    ctx = Ctx(pkg, work, python)
    base = work / 'post9'
    clone(mirror, base, 'lf', synthetic=False)
    ok, label = forward(ctx, base, upto='9 POST', skip=('suite',))
    if not ok:
        raise SystemExit(f'could not reach step 9: {label}')
    n = bad = 0
    tmp = Path(tempfile.gettempdir())
    leftovers = lambda: sorted(p.name for p in tmp.glob('MHUPA_step10_*'))
    start_left = leftovers()

    def fresh(i):
        d = work / f'case_{i:02d}'
        shutil.copytree(base, d, symlinks=True)
        return d

    def judge(label, ok_stop, out, repo, want_state):
        nonlocal n, bad
        n += 1
        st = state(ctx, repo)
        st['U'] = st['U'] == 'MHUP_A'
        clean = leftovers() == start_left
        good = ok_stop and st == want_state and clean
        bad += not good
        line = next((ln for ln in out.splitlines() if 'STOP' in ln), out.strip().splitlines()[-1] if out.strip() else '')
        print(f'[{n:02d}] ' + ('STOPPED as required' if good else 'NEGATIVE FAILED') + f': {label}\n       -> {line[:230]}\n'
              f'       barriers after: {st}; temporary copies left: {"none" if clean else leftovers()}', flush=True)

    cli = lambda r: [python, '-I', str(ctx.pkg / 'RUN_MHUP_A_SUITE.py'), '--repo', str(r), '--shadow']
    barred = {'U': True, 'E': True, 'P': True}
    r = fresh(1); (r / ctx.m['barriers']['P']).unlink()
    rc, out = sh(cli(r)); judge('live P missing: the runner refuses before copying', rc != 0 and 'POST on the live tree does not pass before' in out, out, r, {'U': True, 'E': True, 'P': False})
    r = fresh(2); (r / ctx.m['barriers']['P']).write_text('not ours\n')
    rc, out = sh(cli(r)); judge('live P foreign: the runner refuses before copying', rc != 0 and 'barrier P is absent or not this package' in out, out, r, barred)
    r = fresh(3); (r / ctx.m['barriers']['U']).write_text('INSTALL OTHER 2026-11-11T00:00:00.000000Z')
    rc, out = sh(cli(r)); judge('live U names another package: refused', rc != 0 and "not this package's install lock" in out, out, r, {'U': False, 'E': True, 'P': True})

    spec = importlib.util.spec_from_file_location('mhupa_suite_runner', ctx.pkg / 'RUN_MHUP_A_SUITE.py')
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    orig = {k: getattr(R, k) for k in ('copy_into', 'suite_env', 'run_suite')}

    def inject(label, i, check, **patches):
        r = fresh(i)
        for k, v in orig.items():
            setattr(R, k, v)
        for k, v in patches.items():
            setattr(R, k, v(r))          # each patch is made for this case's live tree
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            res = R.shadow_mode(r)
        out = buf.getvalue()
        judge(label, res is False and check in out, out, r, barred)

    def corrupt(live, shadow, paths):
        orig['copy_into'](live, shadow, paths)
        with open(shadow / 'src' / 'methods' / '_common' / 'contract_dispatch.py', 'ab') as fh:
            fh.write(b'# changed\n')
    inject('a changed code file in the copy: refused before the suite', 4, 'differs from the live file', copy_into=lambda live: corrupt)

    def leaky_env(live):
        def env_for(repo):
            env = orig['suite_env'](repo)
            env['PYTHONPATH'] = os.pathsep.join([str(live / 'src' / 'methods'), env['PYTHONPATH']])
            return env
        return env_for
    inject('the import path reaching into the live tree: refused before the suite', 5, "import path includes the live tree", suite_env=leaky_env)

    def failing(live):
        def run(repo, expected=None):
            print('SUITE STOP: (injected) one module failed')
            return False
        return run
    inject('a failing suite: STOP; the live tree still barred and checked again', 6, 'live tree after the suite: POST PASS', run_suite=failing)

    def escaping(rel):
        def factory(live):
            def run(repo, expected=None):
                (live / rel).parent.mkdir(parents=True, exist_ok=True)
                (live / rel).write_text('a test wrote into the live tree')
                return True
            return run
        return factory
    inject('a test writing an untracked file into the live tree: STOP (POST sees it)', 7,
           'UNEXPECTED (seen, not expected): transitory_data/escape_probe.txt', run_suite=escaping('transitory_data/escape_probe.txt'))
    inject('a test writing into a Git-ignored path of the live tree: STOP (the before/after listing sees it)', 9,
           'the live tree gained or lost', run_suite=escaping('source_data/grabs/escape_probe.txt'))

    def edits_copy(live):
        def run(repo, expected=None):
            with open(repo / 'tests' / 'test_e2r_prefix.py', 'ab') as fh:
                fh.write(b'# changed by a test\n')
            return True
        return run
    inject('a test changing a code or test file in the copy: STOP', 8, 'differs from the live file', run_suite=edits_copy)

    for k, v in orig.items():
        setattr(R, k, v)
    print(f'\nSTEP 10 NEGATIVES: {n} checks, {bad} failed')
    print('STEP 10 NEGATIVES PASS' if not bad else 'STEP 10 NEGATIVES STOP')
    return 1 if bad else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 6 and a[0] == 'positive' and a[5] in ('lf', 'crlf'):
        sys.exit(positive(a[1], a[2], a[3], a[4], a[5], '--suite' in a[6:]))
    if len(a) == 5 and a[0] == 'step10':
        sys.exit(step10(a[1], a[2], a[3], a[4]))
    if len(a) == 5 and a[0] == 'negatives':
        sys.exit(negatives(a[1], a[2], a[3], a[4]))
    print(__doc__)
    sys.exit(2)
