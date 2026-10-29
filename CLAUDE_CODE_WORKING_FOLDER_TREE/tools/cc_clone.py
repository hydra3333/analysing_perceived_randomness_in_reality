"""Task clones for the Claude Code local runner, and the one permitted commit in the main repository.

Written by the Claude web chat, 29 October 2026 (rulebook CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md v0.1).
Every command checks where it is before it does anything, and prints PASS or STOP.

  make          clone the repository from GitHub into scratch/<TASK>/r, remove the link back to
                GitHub, refuse every push with a hook, and run the guard
  guard         check that scratch/<TASK>/r is a task clone with no remote and the refusing hook
  unzip         check a ZIP inside the clone by SHA-256 and extract it into scratch/<TASK>/p
  overlay       copy an extracted repo_overlay into the clone; new files only, except the tracked
                files named with --replace (v0.2, 29 Oct 2026, for E2R-CODE-2's 3 replacements)
  git           run one Git command in the clone (add, commit, status, log, diff, show, rev-parse,
                ls-files), with the guard before and after
  remove        delete scratch/<TASK> after checking the path
  commit-report commit one report file outbox/REPORT_<TASK>.md in the main repository, and nothing else

Usage: <venv python> -I cc_clone.py <command> --task T001 [options]
Task IDs are T followed by three digits. Nothing here pushes, and nothing here touches source_data,
results or transitory_data.
"""
import argparse, hashlib, os, re, shutil, stat, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath

WF = Path(__file__).resolve().parents[1]          # CLAUDE_CODE_WORKING_FOLDER_TREE
MAIN = WF.parent                                  # the owner's main clone
SCRATCH = WF / 'scratch'
GITHUB = 'https://github.com/hydra3333/analysing_perceived_randomness_in_reality'
WF_NAME = 'CLAUDE_CODE_WORKING_FOLDER_TREE'
HOOK = ('#!/bin/sh\n'
        'echo "pre-push refused: this is a Claude Code task clone; it never pushes." >&2\n'
        'exit 1\n')
CLONE_GIT_ALLOWED = {'add', 'commit', 'status', 'log', 'diff', 'show', 'rev-parse', 'ls-files'}
ENV = {**os.environ, 'GIT_TERMINAL_PROMPT': '0', 'GIT_OPTIONAL_LOCKS': '0'}


class Stop(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Stop(msg)


def git(cwd, *args, check=True):
    r = subprocess.run(['git', '-C', str(cwd), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV)
    if check and r.returncode != 0:
        raise Stop(f'git {" ".join(args)} failed ({r.returncode}): {r.stderr.decode(errors="replace").strip()[:400]}')
    return r


def out(r):
    return r.stdout.decode(errors='replace').strip()


def same(a, b):
    return os.path.normcase(str(Path(a).resolve())) == os.path.normcase(str(Path(b).resolve()))


def inside(child, parent):
    c, p = os.path.normcase(str(Path(child).resolve())), os.path.normcase(str(Path(parent).resolve()))
    return c != p and c.startswith(p.rstrip('\\/') + os.sep)


def task_dir(task):
    need(re.fullmatch(r'T\d{3}', task or ''), f'task ID must be T followed by three digits, not {task!r}')
    t = SCRATCH / task
    need(inside(t, SCRATCH) and inside(SCRATCH, WF) and inside(WF, MAIN), f'unexpected task path {t}')
    return t


def check_main():
    """The main repository is the owner's clone, on main, linked to GitHub, with scratch/ ignored."""
    need(same(out(git(MAIN, 'rev-parse', '--show-toplevel')), MAIN), f'{MAIN} is not the top of its Git repository')
    url = out(git(MAIN, 'remote', 'get-url', 'origin')).rstrip('/')
    need(url in (GITHUB, GITHUB + '.git'), f'main repository origin is {url!r}, expected {GITHUB}')
    need(out(git(MAIN, 'branch', '--show-current')) == 'main', 'main repository is not on branch main')
    probe = f'{WF_NAME}/scratch/T000/r/x'
    need(git(MAIN, 'check-ignore', '-q', probe, check=False).returncode == 0, 'scratch/ is not ignored by Git')
    need(out(git(MAIN, 'ls-files', f'{WF_NAME}/scratch')) == '', 'files under scratch/ are tracked by Git')


def guard(task, quiet=False):
    t = task_dir(task)
    r = t / 'r'
    need(r.is_dir() and (r / '.git').is_dir(), f'no task clone at {r}')
    need(not same(r, MAIN) and inside(r, SCRATCH), f'{r} is not inside {SCRATCH}')
    need(same(out(git(r, 'rev-parse', '--show-toplevel')), r), f'{r} is not the top of its own Git repository')
    need(same(out(git(r, 'rev-parse', '--absolute-git-dir')), r / '.git'), 'the clone uses a Git folder outside itself')
    need(out(git(r, 'remote')) == '', 'the task clone has a remote; it must have none')
    rc = git(r, 'config', '--get-regexp', r'^(remote|branch)\..*\.(url|pushurl|remote|pushremote)$', check=False)
    need(rc.returncode == 1 and out(rc) == '', f'the task clone still has remote settings: {out(rc)}')
    need(git(r, 'config', '--get', 'remote.pushDefault', check=False).returncode == 1, 'remote.pushDefault is set')
    hooks = Path(out(git(r, 'config', '--get', 'core.hooksPath')))
    need(same(hooks, r / '.git' / 'hooks'), f'core.hooksPath is {hooks}, expected the clone\'s own hooks folder')
    hook = r / '.git' / 'hooks' / 'pre-push'
    need(hook.is_file() and hook.read_bytes() == HOOK.encode('ascii'), 'the refusing pre-push hook is missing or changed')
    if not quiet:
        print(f'GUARD PASS: {r} is a task clone with no remote and a refusing pre-push hook')
    return r


def cmd_make(a):
    check_main()
    t = task_dir(a.task)
    need(not t.exists(), f'{t} already exists; STOP (remove it only with the remove command)')
    t.mkdir(parents=True)
    r = t / 'r'
    print('cloning from', GITHUB)
    git(t, '-c', 'core.longpaths=true', 'clone', '-q', GITHUB, str(r))
    git(r, 'remote', 'remove', 'origin')
    for key, value in (('core.longpaths', 'true'), ('core.hooksPath', str((r / '.git' / 'hooks').resolve())),
                       ('user.name', 'Claude Code task clone'), ('user.email', 'task-clone@invalid')):
        git(r, 'config', '--local', key, value)
    (r / '.git' / 'hooks').mkdir(exist_ok=True)
    (r / '.git' / 'hooks' / 'pre-push').write_bytes(HOOK.encode('ascii'))
    os.chmod(r / '.git' / 'hooks' / 'pre-push', 0o755)   # needed outside Windows; harmless on Windows
    guard(a.task)
    print('git remote -v:', repr(out(git(r, 'remote', '-v'))))
    print('clone HEAD:', out(git(r, 'rev-parse', 'HEAD')))
    print('main repository HEAD:', out(git(MAIN, 'rev-parse', 'HEAD')))
    print('core.autocrlf in the clone:', out(git(r, 'config', '--get', 'core.autocrlf', check=False)) or '(not set)')
    print('MAKE PASS')


def cmd_guard(a):
    guard(a.task)


def cmd_unzip(a):
    r = guard(a.task, quiet=True)
    t = task_dir(a.task)
    rel = PurePosixPath(a.zip.replace('\\', '/'))
    need(not rel.is_absolute() and '..' not in rel.parts, 'the ZIP path must be relative to the clone')
    z = r / Path(*rel.parts)
    need(z.is_file(), f'no file {z}')
    h = hashlib.sha256(z.read_bytes()).hexdigest()
    print('ZIP SHA-256:', h)
    need(h == a.sha256.lower(), f'ZIP SHA-256 is {h}, expected {a.sha256}')
    p = t / 'p'
    need(not p.exists(), f'{p} already exists')
    with zipfile.ZipFile(z) as zf:
        names = zf.namelist()
        for n in names:
            parts = PurePosixPath(n).parts
            need(not n.startswith(('/', '\\')) and '..' not in parts and ':' not in n, f'unsafe ZIP member {n!r}')
        zf.extractall(p)
    print(f'UNZIP PASS: {sum(1 for n in names if not n.endswith("/"))} files extracted into {p}')


def cmd_overlay(a):
    r = guard(a.task, quiet=True)
    src = Path(a.src).resolve()
    need(inside(src, task_dir(a.task) / 'p') and src.is_dir(), f'{src} is not an extracted folder of this task')
    files = sorted(p for p in src.rglob('*') if p.is_file())
    rels = {f.relative_to(src).as_posix() for f in files}
    replace = set(a.replace or [])
    for x in sorted(replace):
        need(x in rels, f'--replace {x} is not in the overlay')
        need(out(git(r, 'ls-files', '--error-unmatch', '--', x, check=False)) == x, f'--replace {x} is not a tracked file of the clone')
    for f in files:
        rel = f.relative_to(src).as_posix()
        if rel not in replace:
            need(not (r / rel).exists(), f'would overwrite an existing file: {rel}')
    for f in files:
        dst = r / f.relative_to(src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, dst)
    print(f'OVERLAY PASS: {len(files)} files copied into {r} ({len(files) - len(replace)} new, {len(replace)} replaced)')


def cmd_git(a):
    r = guard(a.task, quiet=True)
    args = list(a.args)
    if args and args[0] == '--':
        args = args[1:]
    need(args and args[0] in CLONE_GIT_ALLOWED, f'git {args[:1]} is not allowed through this tool')
    print('GUARD PASS (before)')
    res = subprocess.run(['git', '-C', str(r), *args], env=ENV)
    guard(a.task, quiet=True)
    print(f'GUARD PASS (after); git {args[0]} exit code {res.returncode}')
    sys.exit(res.returncode)


def _unlock(func, path, *_):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def cmd_remove(a):
    t = task_dir(a.task)
    need(t.is_dir(), f'nothing to remove at {t}')
    r = t / 'r'
    if r.exists():
        need(not same(r, MAIN) and inside(r, SCRATCH), f'{r} is not inside {SCRATCH}')
        if (r / '.git').is_dir():
            top = git(r, 'rev-parse', '--show-toplevel', check=False)
            need(top.returncode != 0 or same(out(top), r), 'the clone reports a different top folder; STOP')
    if sys.version_info >= (3, 12):
        shutil.rmtree(t, onexc=_unlock)
    else:
        shutil.rmtree(t, onerror=_unlock)
    need(not t.exists(), f'{t} still exists')
    print(f'REMOVE PASS: {t} deleted')


def cmd_commit_report(a):
    check_main()
    task_dir(a.task)
    rel = f'{WF_NAME}/outbox/REPORT_{a.task}.md'
    f = MAIN / Path(*rel.split('/'))
    need(f.is_file(), f'no report at {f}')
    need(not (SCRATCH / a.task).exists(), f'the task clone {SCRATCH / a.task} still exists; remove it first')
    staged = out(git(MAIN, 'diff', '--cached', '--name-only'))
    need(staged == '', f'the main repository already has staged changes; STOP:\n{staged}')
    git(MAIN, 'add', '--', rel)
    git(MAIN, 'commit', '-q', '-m', f'{WF_NAME}: report for task {a.task} (Claude Code local runner)', '--', rel)
    files = out(git(MAIN, 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD')).splitlines()
    need(files == [rel], f'the commit holds {files}, expected only {rel}; do not push; STOP')
    print('commit:', out(git(MAIN, 'log', '-1', '--format=%H %s')))
    print('COMMIT-REPORT PASS: one file committed; not pushed. The project owner pushes.')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    for name in ('make', 'guard', 'unzip', 'overlay', 'git', 'remove', 'commit-report'):
        sp = sub.add_parser(name)
        sp.add_argument('--task', required=True)
        if name == 'unzip':
            sp.add_argument('--zip', required=True, help='path of the ZIP inside the clone, e.g. exchange/EX_033_Claude/x.zip')
            sp.add_argument('--sha256', required=True)
        if name == 'overlay':
            sp.add_argument('--src', required=True)
            sp.add_argument('--replace', nargs='+', help='repository paths (with /) that the overlay may replace')
        if name == 'git':
            sp.add_argument('args', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    try:
        globals()['cmd_' + a.command.replace('-', '_')](a)
    except Stop as exc:
        print(f'{a.command.upper()} STOP: {exc}', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
