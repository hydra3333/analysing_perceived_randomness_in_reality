#!/usr/bin/env python3
"""VERIFY_MHUP_A.py - the read-only installation verifier of the MHUP-A install package (design Appendix J).

DRAFT (items 2 and 3 of the integrated package work list; not yet reviewed; NOT installation-ready).
Claude web chat, 10-11 November 2026, from wf1/verifier_template.py. Standard library only; imports no project
code, runs no test, changes no file and no Git state (every Git call uses --no-optional-locks and
GIT_OPTIONAL_LOCKS=0). It reads its expectations from PACKAGE_MANIFEST_MHUP_A.json beside it, whose SHA-256 is
fixed below. Of the data folders it reads one thing only: the install lock U (source_data/.results_master.lock),
a value-free lock file, to check the barrier state.

Phases, with the barrier state each one requires (Appendix J; EX_148 (ix): both commits, the barrier order and
record/repository agreement):
  pre        Step 1. Barriers: U, E and P all ABSENT. The package is intact (every overlay file, the manifest, the
             copy tool) and the staged process_check.py has the manifest's SHA-256; the working tree and index are
             clean; HEAD descends from the base commit; src/ and tests/ in HEAD are exactly the base commit's; the
             new paths and both records are absent; every file to be replaced or deleted has its base bytes in Git
             and on disk; transitory_data/no_pycache_ever does not exist. Changes since the base outside src/ and
             tests/ are listed for information (a later commit that touches no package path is allowed).
  post       Step 9, after the two copy steps. Barriers: U held by this package, E and P PRESENT. The working-tree
             changes are exactly the new paths (untracked), the modified files and the deletion (unstaged), all
             with the expected bytes (CRLF tolerated: LF-normalised comparison).
  staged     Steps 12 and 17, after `git add` and before each commit: the index holds exactly that commit's paths
             (the package and the install record; or the release record alone) and nothing else is changed.
  committed  Step 13, after the package commit. Barriers: U held, E and P PRESENT. Clean tree; HEAD is the package
             commit: one parent, which descends from the base with src/ and tests/ unchanged; it added exactly the
             new paths and the install record, modified exactly the modified files and deleted exactly the deleted
             file, with the expected Git blobs; the install record is canonical, names this package, this
             manifest's SHA-256 and the manifest's entries, and was written after U was taken.
  released   Step 17, after the release commit. Barriers: U STILL held (it is released only at step 18), E and P
             ABSENT. Clean tree. The two-commit proof: HEAD is the release commit, with exactly one parent; that
             parent passes every check of the package commit above; the release commit adds exactly the release
             record and changes nothing else. The release record: canonical bytes, identical in the working tree
             and in Git (no line-ending conversion); this package; exactly the manifest's release entries and
             retirements; the SHA-256 of the committed install record; written after the install record (UTC), on a
             local date not before the install record's and within a day of its own UTC date. Record/repository
             agreement: each released entry is the newest registry chain entry of its variant at HEAD, with status
             SUPPORTED and that revision; the baseline record marks the same variant's earlier revision superseded by
             it; the released set is the manifest's expected number per game; no barrier file and no
             IN_DEVELOPMENT flag is committed. The order U, then the install record, then the release record is
             checked from their recorded UTC times.
On any STOP: do NOT push and do NOT reset; send Claude the whole output (Appendix J's STOP column applies).
Usage: python -I -B VERIFY_MHUP_A.py --repo REPO --phase pre|post|staged|committed|released
"""
import argparse, hashlib, json, os, re, subprocess, sys
from datetime import date, datetime
from pathlib import Path

MANIFEST_SHA256 = '@@MANIFEST_SHA256@@'
COPY_SHA256 = '@@COPY_SHA256@@'
INSTALL_SCHEMA, RELEASE_SCHEMA = 'INSTALL_RECORD_V1', 'RELEASE_RECORD_V1'
INSTALL_KEYS = {'schema', 'package', 'manifest_sha256', 'post_pass_utc', 'local_date', 'registry_entries_added',
                'release_entries_planned', 'retires_planned', 'statement'}
RELEASE_KEYS = {'schema', 'package', 'entries', 'retires', 'released_utc', 'local_date', 'install_record_sha256',
                'statement'}
INSTALL_LOCK = re.compile(r'INSTALL (?P<package>[A-Za-z0-9_.-]+) (?P<utc>\S+)\Z')     # process_check.py's own format
UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
HERE = Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(b):
    return b.replace(b'\r\n', b'\n')


def canonical(rec):
    """The records' canonical bytes (the same form as src/methods/_common/release_records.py)."""
    return (json.dumps(rec, sort_keys=True, separators=(',', ':'), ensure_ascii=True) + '\n').encode('ascii')


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


def utc(text, what):
    try:
        return datetime.strptime(text, UTC_FORMAT)
    except (TypeError, ValueError):
        raise RuntimeError(f'FAIL: {what} is not a UTC time of the expected form') from None


def status_entries(repo):
    """Parsed `git status --porcelain=v1 -z --untracked-files=all`: list of (XY, path)."""
    raw = git(repo, 'status', '--porcelain=v1', '-z', '--no-renames', '--untracked-files=all').decode('utf-8', errors='replace')
    return [(it[:2], it[3:]) for it in raw.split('\0') if it]


def identities(repo):
    """Read-only facts for deciding after a STOP."""
    print('--- identities for Claude (read-only) ---', file=sys.stderr)
    for label, args in [('HEAD and parents', ['log', '-1', '--format=%H %P %s', 'HEAD']),
                        ('last 4 commits', ['log', '--oneline', '-4']),
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
    for t, h in m['tool_sha256'].items():       # the tools are run from this folder: their exact bytes, not normalised
        need(expected.get(t) == h, f'the manifest\'s tool hash disagrees with its file list: {t}')
        need(sha((HERE / 'repo_overlay' / t).read_bytes()) == h, f'a staged tool is not byte for byte the manifest\'s: {t}')
    return m, expected


# ------------------------------------------------------------------ the barrier state (EX_148 (ix))

def barriers(repo, m, *, u, e, p):
    """Require the barrier state of the phase. u: 'absent' or 'held'; e, p: True (present) or False (absent).
    Returns the UTC time U was taken, when held."""
    taken = None
    lock = repo / m['barriers']['U']
    if u == 'absent':
        need(not lock.exists() and not lock.is_symlink(),
             'barrier U: an updater lock exists; before step 3 no lock at all is allowed (send the output)')
    else:
        need(lock.is_file() and not lock.is_symlink(), 'barrier U (the install lock) is not held; it is taken at step 3 '
             'and released only at step 18')
        mt = INSTALL_LOCK.fullmatch(lock.read_text(encoding='ascii', errors='replace').strip())
        need(mt is not None and mt.group('package') == m['package'], 'barrier U is not this package\'s install lock')
        taken = utc(mt.group('utc'), 'the install lock\'s time')
    for name, want in (('E', e), ('P', p)):
        f = repo / m['barriers'][name]
        if want:
            need(f.is_file() and not f.is_symlink() and
                 f.read_bytes() == m['barrier_text'].format(name=name).encode('ascii'),
                 f'barrier {name} is absent or not this package\'s: {m["barriers"][name]}')
        else:
            need(not f.exists() and not f.is_symlink(), f'barrier {name} exists: {m["barriers"][name]}')
    print('barriers: U ' + ('held by this package' if taken else 'absent') + '; E ' + ('present' if e else 'absent') +
          '; P ' + ('present' if p else 'absent') + ' (as this phase requires)')
    return taken


# ------------------------------------------------------------------ the phases

def phase_pre(repo, m, expected):
    barriers(repo, m, u='absent', e=False, p=False)
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
    for p in [*m['new'], m['install_record'], m['release_record']]:
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
    barriers(repo, m, u='held', e=True, p=True)
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


def phase_staged(repo, m, expected):
    """Steps 12 and 17, before each commit: the index holds exactly what the commit must contain, and the working
    tree holds nothing else. Which commit is next is read from HEAD (the install record committed or not)."""
    st = status_entries(repo)
    got = {p: x for x, p in st}
    if run(repo, 'cat-file', '-e', f'HEAD:{m["install_record"]}').returncode != 0:
        barriers(repo, m, u='held', e=True, p=True)
        want = {**{p: 'A ' for p in m['new']}, m['install_record']: 'A ', **{p: 'M ' for p in m['modified']},
                **{p: 'D ' for p in m['deleted']}}
        what = 'the package commit'
    else:
        barriers(repo, m, u='held', e=False, p=False)
        want = {m['release_record']: 'A '}
        what = 'the release commit'
    need(got == want, f'the index is not exactly {what}; MISSING or wrongly staged: ' +
         (', '.join(sorted(p for p in want if got.get(p) != want[p])[:12]) or 'none') + '; UNEXPECTED: ' +
         (', '.join(f'{got[p]}{p}' for p in sorted(got) if p not in want)[:600] or 'none'))
    print(f'STAGED PASS: the index holds exactly {what} ({len(want)} paths) and nothing else is changed. Commit now.')


def check_package_commit(repo, m, expected, c):
    """Every check of the package commit, at commit-ish `c`. Returns the install record (dict) and its blob."""
    parents = git(repo, 'log', '-1', '--format=%P', c).decode().split()
    need(len(parents) == 1, f'the package commit has {len(parents)} parents, expected 1')
    need(run(repo, 'merge-base', '--is-ancestor', m['base_commit'], f'{c}~1').returncode == 0,
         'the package commit\'s parent does not descend from the base')
    diff = git(repo, 'diff', '--name-only', m['base_commit'], f'{c}~1', '--', 'src', 'tests').decode().split()
    need(not diff, "the package commit's parent has src/ or tests/ changes since the base: " + ', '.join(diff[:20]))
    names = git(repo, 'diff', '--no-renames', '--name-status', f'{c}~1', c).decode().splitlines()
    got = {ln.split('\t', 1)[1]: ln.split('\t', 1)[0] for ln in names if ln}
    want = {**{p: 'A' for p in m['new']}, m['install_record']: 'A', **{p: 'M' for p in m['modified']},
            **{p: 'D' for p in m['deleted']}}
    need(got == want, 'the package commit did not change exactly the expected paths; differences (path, status): ' +
         repr(sorted(set(got.items()) ^ set(want.items()))[:12]))
    for p, h in expected.items():
        need(sha(git(repo, 'show', f'{c}:{p}')) == h, f'wrong Git blob in the package commit: {p}')
    for p, (old, _n) in m['modified'].items():
        need(sha(git(repo, 'show', f'{c}~1:{p}')) == old, f'the package commit\'s parent does not hold the base version: {p}')
    for p, old in m['deleted'].items():
        need(sha(git(repo, 'show', f'{c}~1:{p}')) == old, f'the package commit\'s parent does not hold the deleted file: {p}')
        need(run(repo, 'cat-file', '-e', f'{c}:{p}').returncode != 0, f'deleted file still in the package commit: {p}')
    raw = git(repo, 'show', f'{c}:{m["install_record"]}')
    try:
        rec = json.loads(raw.decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        raise RuntimeError('FAIL: the install record is not ASCII JSON') from None
    need(type(rec) is dict and canonical(rec) == raw, 'the install record is not its canonical bytes in Git')
    need(set(rec) == INSTALL_KEYS, 'the install record\'s fields are not the expected ones')
    need(rec['schema'] == INSTALL_SCHEMA and rec['package'] == m['package'], 'the install record names another schema or package')
    need(rec['manifest_sha256'] == MANIFEST_SHA256, 'the install record names another manifest')
    need(rec['registry_entries_added'] == m['registry_entries_added'], 'the install record\'s registry entries differ')
    need(rec['release_entries_planned'] == m['release_entries'] and rec['retires_planned'] == m['retires'],
         'the install record\'s planned release entries differ from the manifest')
    t = utc(rec['post_pass_utc'], 'the install record\'s time')
    try:
        d = date.fromisoformat(rec['local_date'])
    except (TypeError, ValueError):
        raise RuntimeError('FAIL: the install record\'s local date is malformed') from None
    need(abs((d - t.date()).days) <= 1, 'the install record\'s local date is not the day it was written')
    return rec, raw


def phase_committed(repo, m, expected):
    taken = barriers(repo, m, u='held', e=True, p=True)
    st = status_entries(repo)
    need(not st, 'working tree or index not clean after commit:\n' + '\n'.join(f'{x} {p}' for x, p in st[:30]))
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    rec, raw = check_package_commit(repo, m, expected, 'HEAD')
    need((repo / m['install_record']).read_bytes() == raw, 'the install record on disk is not the committed bytes')
    need(taken <= utc(rec['post_pass_utc'], 'the install record\'s time'),
         'the install record was written before the install lock U was taken (barrier order)')
    need(not (repo / m['release_record']).exists(), 'a release record exists before step 16')
    print(f'COMMITTED PASS: the package commit ({head[:7]}) added exactly {len(m["new"])} files and the install record, '
          f'modified {len(m["modified"])} and deleted {len(m["deleted"])}; all Git blobs match; the install record '
          f'names this package and manifest; barriers U, E and P in place.')


def phase_released(repo, m, expected):
    taken = barriers(repo, m, u='held', e=False, p=False)
    st = status_entries(repo)
    need(not st, 'working tree or index not clean after the release commit:\n' + '\n'.join(f'{x} {p}' for x, p in st[:30]))
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    # --- the two-commit proof
    parents = git(repo, 'log', '-1', '--format=%P', 'HEAD').decode().split()
    need(len(parents) == 1, f'the release commit has {len(parents)} parents, expected exactly 1 (the package commit)')
    names = git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD').decode().splitlines()
    got = {ln.split('\t', 1)[1]: ln.split('\t', 1)[0] for ln in names if ln}
    need(got == {m['release_record']: 'A'}, 'the release commit did not add exactly the release record; it changed '
         '(path, status): ' + repr(sorted(got.items())[:12]))
    try:
        inst, inst_raw = check_package_commit(repo, m, expected, 'HEAD~1')     # the only parent IS the package commit
    except RuntimeError as exc:
        raise RuntimeError('FAIL: the release commit\'s only parent is not the package commit: ' + str(exc)[6:]) from None
    need(git(repo, 'show', f'HEAD:{m["install_record"]}') == inst_raw, 'the install record changed in the release commit')
    need((repo / m['install_record']).read_bytes() == inst_raw,
         'the install record on disk is not the committed bytes (line endings converted?)')
    # --- the release record
    raw = git(repo, 'show', f'HEAD:{m["release_record"]}')
    need((repo / m['release_record']).read_bytes() == raw,
         'the release record on disk is not the committed bytes (line endings converted?)')
    try:
        rec = json.loads(raw.decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        raise RuntimeError('FAIL: the release record is not ASCII JSON') from None
    need(type(rec) is dict and canonical(rec) == raw, 'the release record is not its canonical bytes')
    need(set(rec) == RELEASE_KEYS, 'the release record\'s fields are not the expected ones')
    need(rec['schema'] == RELEASE_SCHEMA and rec['package'] == m['package'], 'the release record names another schema or package')
    need(rec['entries'] == m['release_entries'], 'the release record\'s entries are not exactly the manifest\'s release entries')
    need(rec['retires'] == m['retires'], 'the release record\'s retirements are not the manifest\'s')
    need(rec['install_record_sha256'] == sha(inst_raw), 'the release record does not name the committed install record\'s SHA-256')
    t_inst, t_rel = utc(inst['post_pass_utc'], 'the install record\'s time'), utc(rec['released_utc'], 'the release record\'s time')
    need(taken <= t_inst <= t_rel, 'the recorded order is not: install lock U taken, then the install record, then the '
         f'release record ({taken.strftime(UTC_FORMAT)}, {inst["post_pass_utc"]}, {rec["released_utc"]})')
    try:
        d_inst, d_rel = date.fromisoformat(inst['local_date']), date.fromisoformat(rec['local_date'])
    except (TypeError, ValueError):
        raise RuntimeError('FAIL: a record\'s local date is malformed') from None
    need(d_rel >= d_inst, 'the release record\'s local date is before the install record\'s')
    need(abs((d_rel - t_rel.date()).days) <= 1, 'the release record\'s local date is not the day it was written')
    # --- record/repository agreement at HEAD
    tree = git(repo, 'ls-tree', '-r', '--name-only', '-z', 'HEAD').decode('utf-8', errors='replace').split('\0')
    for name in ('E', 'P', 'U'):
        need(m['barriers'][name] not in tree, f'barrier {name} is committed: {m["barriers"][name]}')
    flags = [p for p in tree if p.startswith('src/methods/') and p.endswith('/IN_DEVELOPMENT.txt')]
    need(not flags, 'an IN_DEVELOPMENT flag is committed: ' + ', '.join(flags[:5]))
    baseline = json.loads(git(repo, 'show', f'HEAD:{m["baseline_record"]}').decode('ascii'))
    for e in rec['entries']:
        key = (e['game_id'], e['method_id'], e['method_revision'], e['variant_id'])
        folder = f'src/methods/_common/contract_data/registry/{e["game_id"]}/{e["method_id"]}/{e["variant_id"]}/'
        chain = sorted(p for p in tree if p.startswith(folder) and re.fullmatch(r'entry_\d+\.json', p[len(folder):]))
        need(chain and chain[-1] in m['registry_entries_added'], f'{key}: the newest registry entry is not one this package added')
        top = json.loads(git(repo, 'show', f'HEAD:{chain[-1]}').decode('ascii'))
        need((top.get('game_id'), top.get('method_id'), top.get('method_revision'), top.get('variant_id')) == key and
             top.get('registry_status') == 'SUPPORTED' and top.get('entry_sequence') == len(chain),
             f'{key}: the newest registry chain entry is not this revision, SUPPORTED and last in sequence')
        sup = [b for b in baseline['entries'] if (b['game_id'], b['method_id'], b['variant_id']) ==
               (e['game_id'], e['method_id'], e['variant_id'])]
        need(len(sup) == 1 and sup[0].get('superseded_by') == e['method_revision'] and
             sup[0]['method_revision'] != e['method_revision'],
             f'{key}: the baseline record does not mark this variant\'s earlier revision superseded by it')
    for g, n in sorted(m['expected_released_per_game'].items()):
        have = sum(1 for b in baseline['entries'] if b['game_id'] == g and 'superseded_by' not in b) + \
            sum(1 for e in rec['entries'] if e['game_id'] == g)
        need(have == n, f'{g}: the released set is {have}, expected {n}')
    counts = ', '.join(f'{g} {n}' for g, n in sorted(m['expected_released_per_game'].items()))
    print(f'RELEASED PASS: two commits proved: the release commit ({head[:7]}) has one parent, the package commit '
          f'({parents[0][:7]}), and adds exactly the release record; the record is canonical, names '
          f'{len(rec["entries"])} released entries and the committed install record; order U, install record, release '
          f'record; released set {counts}; E and P absent, U still held (release it at step 18).')


def main(a):
    repo = a.repo.resolve()
    need((repo / '.git').exists(), f'not a Git checkout: {repo}')
    m, expected = load_package()
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    need(run(repo, 'merge-base', '--is-ancestor', m['base_commit'], 'HEAD').returncode == 0,
         f'HEAD {head} does not descend from base {m["base_commit"]}; STOP')
    print('HEAD:', head, '(descends from base', m['base_commit'][:7] + ')')
    {'pre': phase_pre, 'post': phase_post, 'staged': phase_staged, 'committed': phase_committed,
     'released': phase_released}[a.phase](repo, m, expected)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--phase', required=True, choices=['pre', 'post', 'staged', 'committed', 'released'])
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
