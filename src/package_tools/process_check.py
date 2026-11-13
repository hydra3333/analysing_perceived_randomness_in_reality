"""MHUP-A: the one process tool (design v0.1r5 section 6.1, section 7 A7, Appendix J). It never acts on a process.

It lists, through psutil and without touching anything, every Python process that belongs to this project by the
rule of 6.1, and judges CLEAN only if there is none. It writes only its own value-free records: resume tokens
(beside a game's session record), lock-clearance records (under transitory_data/lock_clearances/) and the install
lock's own content. It imports nothing under src/methods/ or src/evaluation/, and contains no terminate, kill,
taskkill or signal call (a static test says so; a human closes a process through its own console).

Run directly with the venv's Python, never through a launcher:
  .venv\\Scripts\\python.exe -I -B -X pycache_prefix=<root>\\transitory_data\\no_pycache_ever src\\package_tools\\process_check.py
      <command> --root <project root> [options]
  (for the MHUP-A install, from the package staging folder after PRE has verified this file's SHA-256)

Commands (every one prints CLEAN or REFUSED and exits 0 or 1; nothing else changes on REFUSED):
  check-no-runs       [--game G | --install PACKAGE_MANIFEST]   the rule of 6.1; with --game and the game's session
                      lock present, CLEAN also writes a resume token; with --install, the install check of Appendix J
  clear-session-lock  --game G        clears results/real/weekly/<G>/ACTIVE_SESSION.lock only on CLEAN, with a record
  clear-updater-lock                  clears source_data/.results_master.lock only on CLEAN (Python processes whose
                                      command line names results_master), never a lock whose content names an install
  take-install-lock   --package P     creates the updater lock with the content "INSTALL <P> <utc>" (Appendix J step 3)
  release-install-lock --package P    deletes the updater lock only if its content names that package (step 18)

The rule of 6.1, exactly: a process whose executable name is python.exe or pythonw.exe (any python* name outside
Windows), other than this process and its own parent chain, is listed when (a) its executable is the venv's Python
redirector or the base interpreter named in pyvenv.cfg, or (b) its current directory is under the project root, or
(c) its command line, or any ancestor's, names the project root. A Python process whose details cannot be read is a
refusal, never CLEAN. Known false positive: an unrelated Python started from the same base installation; the owner
closes it. Known limit: nothing outside this rule is examined.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys
from pathlib import Path

TOOL_VERSION = 'PROCESS_CHECK_V1'
RESUME_TOKEN_SCHEMA = 'RESUME_TOKEN_V1'
CLEARANCE_SCHEMA = 'LOCK_CLEARANCE_V1'
INSTALL_LOCK = re.compile(r'INSTALL (?P<package>[A-Za-z0-9_.-]+) (?P<utc>\S+)\Z')
GAMES = ('POWERBALL', 'OZLOTTO')
HOLDOUT_LAST = {'POWERBALL': 1586, 'OZLOTTO': 1703}       # the games' profiles are method code; the figures are the design's


class Refused(Exception):
    pass


@dataclass
class Proc:
    pid: int
    ppid: int | None
    name: str
    exe: str | None
    cwd: str | None
    cmdline: list[str] | None
    create_time: float | None
    error: str | None = None            # set when a detail could not be read (access denied)
    reasons: list[str] = field(default_factory=list)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def _norm(p: str | None) -> str:
    if not p:
        return ''
    try:
        return os.path.normcase(str(Path(p).resolve()))
    except OSError:
        return os.path.normcase(p)


def _under(child: str, parent: str) -> bool:
    c, p = _norm(child), _norm(parent)
    return bool(c) and bool(p) and (c == p or c.startswith(p.rstrip('\\/') + os.sep))


def _is_python_name(name: str) -> bool:
    n = (name or '').lower()
    return n in ('python.exe', 'pythonw.exe') or (os.name != 'nt' and n.startswith('python'))


# ---------------------------------------------------------------- the process table (psutil, read-only)

def read_table() -> list[Proc]:
    """Every process, read-only. A Python-named process gets all its details (one that cannot be read is recorded as
    an error, and the rule then refuses); any other process gets only its name, parent and command line, so the
    ancestor test of 6.1 (c) sees a non-Python parent such as the cmd.exe that runs a launcher (EX_148 C01). An
    unreadable non-Python command line is simply absent: it can neither list nor clear anything by itself."""
    import psutil
    out = []
    for p in psutil.process_iter(['pid', 'ppid', 'name']):
        try:
            name = p.info.get('name') or ''
        except Exception:
            name = ''
        proc = Proc(pid=p.info['pid'], ppid=p.info.get('ppid'), name=name, exe=None, cwd=None, cmdline=None, create_time=None)
        if _is_python_name(name):
            for attr in ('exe', 'cwd', 'cmdline', 'create_time'):
                try:
                    setattr(proc, attr, getattr(p, attr)())
                except psutil.NoSuchProcess:
                    proc.error = 'exited during the read'
                except (psutil.AccessDenied, psutil.ZombieProcess, OSError) as exc:
                    proc.error = f'{attr}: {type(exc).__name__}'
        else:
            try:
                proc.cmdline = p.cmdline()
            except Exception:                                   # access denied, exited: no command line to test
                proc.cmdline = None
        out.append(proc)
    return out


def own_chain(table_pids: set[int]) -> set[int]:
    """This process and its parent chain, by PID (through psutil; falls back to os.getpid alone)."""
    chain = {os.getpid()}
    try:
        import psutil
        p = psutil.Process(os.getpid())
        while True:
            parent = p.parent()
            if parent is None:
                break
            chain.add(parent.pid)
            p = parent
    except Exception:
        pass
    return chain


def project_processes(table: list[Proc], root: Path, venv_python: Path, base_python: Path | None,
                      exclude: set[int], *, cmdline_filter: str | None = None) -> list[Proc]:
    """The listed processes under the rule of 6.1 (reasons filled in). A process with an unreadable detail is
    listed with its error (a refusal for the caller). `cmdline_filter` narrows to command lines naming a string
    (clear-updater-lock: results_master)."""
    by_pid = {p.pid: p for p in table}            # every process: ancestors of any name are walked (6.1 (c))
    rootn = _norm(str(root)).lower()
    listed = []
    for p in table:
        if p.pid in exclude or not _is_python_name(p.name):      # the rule names Python processes only
            continue
        if p.error:
            p.reasons.append(f'unreadable: {p.error}')
            listed.append(p)
            continue
        if cmdline_filter is not None and not any(cmdline_filter in a for a in (p.cmdline or [])):
            continue
        if p.exe and (_norm(p.exe) == _norm(str(venv_python)) or (base_python and _norm(p.exe) == _norm(str(base_python)))):
            p.reasons.append('executable is the project venv or its base interpreter')
        if p.cwd and _under(p.cwd, str(root)):
            p.reasons.append('current directory under the project root')
        q, seen = p, set()
        while q is not None and q.pid not in seen:
            seen.add(q.pid)
            if any(rootn in _norm(a).lower() or str(root).lower() in a.lower() for a in (q.cmdline or [])):
                p.reasons.append('command line names the project root' + ('' if q is p else f' (ancestor {q.pid})'))
                break
            q = by_pid.get(q.ppid) if q.ppid is not None else None
        if p.reasons:
            listed.append(p)
    return listed


def describe(p: Proc, by_pid: dict) -> str:
    chain, q, seen = [], by_pid.get(p.ppid) if p.ppid is not None else None, set()
    while q is not None and q.pid not in seen:
        seen.add(q.pid)
        chain.append(str(q.pid))
        q = by_pid.get(q.ppid) if q.ppid is not None else None
    created = datetime.fromtimestamp(p.create_time, timezone.utc).isoformat() if p.create_time else '?'
    return (f'  PID {p.pid} created {created} parents [{" > ".join(chain) or "-"}] exe {p.exe!r} cwd {p.cwd!r} '
            f'cmdline {p.cmdline!r}: {"; ".join(p.reasons)}')


def table_digest(table: list[Proc]) -> str:
    rows = sorted((p.pid, p.ppid, p.name, p.exe, p.cwd, tuple(p.cmdline or []), p.create_time, p.error) for p in table)
    return hashlib.sha256(json.dumps(rows, sort_keys=True, default=str).encode('utf-8')).hexdigest()


# ---------------------------------------------------------------- roots, locks and records

def project_root(arg: str) -> Path:
    root = Path(arg)
    if not root.is_absolute():
        raise Refused('--root must be an absolute path')
    root = root.resolve()
    for sub in ('src', 'source_data', 'results', '.git'):
        if not (root / sub).exists():
            raise Refused(f'{root} does not look like the project root (no {sub})')
    return root


def venv_python(root: Path) -> Path:
    return root / '.venv' / ('Scripts' if os.name == 'nt' else 'bin') / ('python.exe' if os.name == 'nt' else 'python')


def base_python(root: Path) -> Path | None:
    cfg = root / '.venv' / 'pyvenv.cfg'
    if not cfg.is_file():
        return None
    for line in cfg.read_text(encoding='utf-8', errors='replace').splitlines():
        if line.split('=', 1)[0].strip() == 'home':
            home = Path(line.split('=', 1)[1].strip())
            return home / ('python.exe' if os.name == 'nt' else 'python')
    return None


def session_lock(root: Path, game: str) -> Path:
    return root / 'results' / 'real' / 'weekly' / game / 'ACTIVE_SESSION.lock'


def updater_lock(root: Path) -> Path:
    return root / 'source_data' / '.results_master.lock'


def read_lock(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise Refused(f'{path.name} exists but is not a plain file')
    return path.read_text(encoding='ascii', errors='replace').strip()


def write_record(path: Path, rec: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(rec, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')
    with open(path, 'xb') as fh:
        fh.write(raw)
        fh.flush()
        os.fsync(fh.fileno())


def clearance_record(root: Path, kind: str, details: dict) -> Path:
    stamp = utc_now()
    path = root / 'transitory_data' / 'lock_clearances' / f'CLEARANCE_{kind}_{stamp.replace(":", "").replace("-", "").replace(".", "")}.json'
    write_record(path, {'schema': CLEARANCE_SCHEMA, 'kind': kind, 'utc': stamp, 'tool_version': TOOL_VERSION, **details})
    return path


# ---------------------------------------------------------------- the checks

def check_no_runs(root: Path, table: list[Proc], *, exclude: set[int], game: str | None = None,
                  install: dict | None = None, out=print) -> list[Proc]:
    """The rule of 6.1 (and the install check of Appendix J with `install`). Prints every listed process. Returns
    the listed processes (empty means CLEAN so far; the caller decides the rest)."""
    listed = project_processes(table, root, venv_python(root), base_python(root), exclude)
    by_pid = {p.pid: p for p in table}
    for p in listed:
        out(describe(p, by_pid))
    if install is not None:
        for g in GAMES:
            lock = session_lock(root, g)
            if lock.exists() or lock.is_symlink():
                raise Refused(f'{g}: a session lock exists ({lock.name}); resume or close that session first')
        ul = updater_lock(root)
        if ul.exists() or ul.is_symlink():
            content = read_lock(ul)
            m = INSTALL_LOCK.fullmatch(content)
            if m is None:
                raise Refused('the updater lock exists with content that is not an install\'s: an update is running or '
                              'crashed (section 7 A7); not CLEAN')
            if m.group('package') != install['package']:
                raise Refused(f'the updater lock names another install ({m.group("package")}); not CLEAN')
        if install.get('changes_roster'):
            for g in GAMES:
                open_set = unfinished_weekly_set(root, g)
                if open_set:
                    raise Refused(f'{g}: an unfinished weekly set (targets {sorted(open_set)} have a weekly ticket and no '
                                  f'freeze line); a roster-changing install waits (EX_129 C01)')
    return listed


def unfinished_weekly_set(root: Path, game: str) -> set[int]:
    """Targets above holdout_last with a ticket in any weekly session's attempts ledger and no freeze line in the game's
    forecast ledger (Mode H and WF-1A ledgers are not read). Malformed lines refuse."""
    weekly = root / 'results' / 'real' / 'weekly' / game
    ticketed: set[int] = set()
    sessions = weekly / 'sessions'
    if sessions.is_dir():
        for path in sorted(sessions.glob('SESSION_*_attempts.jsonl')):
            for rec in _jsonl(path):
                if rec.get('schema') == 'TICKET_V1' and type(rec.get('target_draw_number')) is int and \
                        rec['target_draw_number'] > HOLDOUT_LAST[game]:
                    ticketed.add(rec['target_draw_number'])
    frozen = {rec['target_draw_number'] for rec in _jsonl(weekly / 'FORECAST_LEDGER_V1.jsonl')
              if rec.get('schema') == 'FREEZE_LINE_V1' and type(rec.get('target_draw_number')) is int}
    return ticketed - frozen


def _jsonl(path: Path) -> list[dict]:
    if not path.exists() and not path.is_symlink():
        return []
    if path.is_symlink() or not path.is_file():
        raise Refused(f'{path.name} exists but is not a plain file')
    raw = path.read_bytes()
    complete = raw[:raw.rfind(b'\n') + 1] if raw and not raw.endswith(b'\n') else raw
    out = []
    for line in complete.split(b'\n')[:-1]:
        try:
            rec = json.loads(line.decode('ascii'))
        except (ValueError, UnicodeDecodeError):
            raise Refused(f'{path.name}: an undecodable line') from None
        if type(rec) is not dict:
            raise Refused(f'{path.name}: a line that is not an object')
        out.append(rec)
    return out


def load_install_manifest(path: Path) -> dict:
    """The package manifest's name and whether it changes the roster (release entries or retirements)."""
    if not path.is_file():
        raise Refused(f'no package manifest at {path}')
    rec = json.loads(path.read_text(encoding='ascii'))
    name = rec.get('package')
    if type(name) is not str or not re.fullmatch(r'[A-Za-z0-9_.-]+', name):
        raise Refused('the package manifest names no package')
    return {'package': name, 'changes_roster': bool(rec.get('release_entries')) or bool(rec.get('retires'))}


def resume_token(root: Path, game: str, table: list[Proc]) -> Path | None:
    """With the game's session lock present and the check CLEAN: the token open-session --resume needs (6.1)."""
    lock = session_lock(root, game)
    if not (lock.exists() or lock.is_symlink()):
        return None
    content = read_lock(lock)
    m = re.match(r'(?P<session>[0-9a-f]{32})\b', content)
    if m is None:
        raise Refused('the session lock does not name a session id; not cleared, no token written')
    stamp = utc_now()
    path = root / 'results' / 'real' / 'weekly' / game / 'sessions' / \
        f'RESUME_{m.group("session")}_{stamp.replace(":", "").replace("-", "").replace(".", "")}.json'
    write_record(path, {'schema': RESUME_TOKEN_SCHEMA, 'game_id': game, 'session_id': m.group('session'), 'utc': stamp,
                        'process_table_sha256': table_digest(table), 'tool_version': TOOL_VERSION})
    return path


# ---------------------------------------------------------------- commands

def cmd_check_no_runs(args, table, exclude, out=print) -> int:
    root = project_root(args.root)
    install = load_install_manifest(Path(args.install)) if args.install else None
    listed = check_no_runs(root, table, exclude=exclude, game=args.game, install=install, out=out)
    if listed:
        out(f'REFUSED: {len(listed)} project Python process(es) listed above (a human lets each end or closes it through '
            f'its own console; this tool never terminates anything)')
        return 1
    token = resume_token(root, args.game, table) if args.game else None
    out('CLEAN' + (f'; resume token written: {token.name}' if token else ''))
    return 0


def cmd_clear_session_lock(args, table, exclude, out=print) -> int:
    root = project_root(args.root)
    lock = session_lock(root, args.game)
    if not (lock.exists() or lock.is_symlink()):
        out(f'REFUSED: no session lock for {args.game}')
        return 1
    content = read_lock(lock)
    listed = check_no_runs(root, table, exclude=exclude, out=out)
    if listed:
        out(f'REFUSED: {len(listed)} project Python process(es) listed; the lock stays')
        return 1
    rec = clearance_record(root, 'SESSION_LOCK', {'game_id': args.game, 'lock_content': content,
                                                  'process_table_sha256': table_digest(table)})
    lock.unlink()
    out(f'CLEAN; session lock cleared; clearance record {rec.name}')
    return 0


def cmd_clear_updater_lock(args, table, exclude, out=print) -> int:
    root = project_root(args.root)
    lock = updater_lock(root)
    if not (lock.exists() or lock.is_symlink()):
        out('REFUSED: no updater lock')
        return 1
    content = read_lock(lock)
    if INSTALL_LOCK.fullmatch(content):
        out('REFUSED: the updater lock names an install; only the install\'s own release step or its restore steps '
            'remove it (Appendix J)')
        return 1
    listed = project_processes(table, root, venv_python(root), base_python(root), exclude, cmdline_filter='results_master')
    by_pid = {p.pid: p for p in table}
    for p in listed:
        out(describe(p, by_pid))
    if listed:
        out(f'REFUSED: {len(listed)} updater process(es) listed; the lock stays')
        return 1
    rec = clearance_record(root, 'UPDATER_LOCK', {'lock_content': content, 'process_table_sha256': table_digest(table)})
    lock.unlink()
    out(f'CLEAN; updater lock cleared; clearance record {rec.name}')
    return 0


def cmd_take_install_lock(args, table, exclude, out=print) -> int:
    root = project_root(args.root)
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', args.package):
        out('REFUSED: invalid package name')
        return 1
    lock = updater_lock(root)
    if lock.exists() or lock.is_symlink():
        content = read_lock(lock)
        if INSTALL_LOCK.fullmatch(content):
            out(f'REFUSED: the updater lock already names an install ({content}); an earlier install did not finish')
        else:
            out('REFUSED: the updater lock exists with an update\'s content; an update is running or crashed (A7)')
        return 1
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)       # the updater's own create-exclusive open
    try:
        os.write(fd, f'INSTALL {args.package} {utc_now()}'.encode('ascii'))
    finally:
        os.close(fd)
    out(f'CLEAN; install lock taken for {args.package}')
    return 0


def cmd_release_install_lock(args, table, exclude, out=print) -> int:
    root = project_root(args.root)
    lock = updater_lock(root)
    if not (lock.exists() or lock.is_symlink()):
        out('REFUSED: no updater lock to release')
        return 1
    m = INSTALL_LOCK.fullmatch(read_lock(lock))
    if m is None or m.group('package') != args.package:
        out('REFUSED: the updater lock does not name this package; nothing removed')
        return 1
    lock.unlink()
    out(f'CLEAN; install lock released for {args.package}')
    return 0


def main(argv=None, table=None, exclude=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='command', required=True)
    for name in ('check-no-runs', 'clear-session-lock', 'clear-updater-lock', 'take-install-lock', 'release-install-lock'):
        sp = sub.add_parser(name)
        sp.add_argument('--root', required=True, help='the project root, an absolute path')
        if name == 'check-no-runs':
            g = sp.add_mutually_exclusive_group()
            g.add_argument('--game', choices=GAMES)
            g.add_argument('--install', help='the package manifest (the install check of Appendix J)')
        if name == 'clear-session-lock':
            sp.add_argument('--game', required=True, choices=GAMES)
        if name in ('take-install-lock', 'release-install-lock'):
            sp.add_argument('--package', required=True)
    args = ap.parse_args(argv)
    if table is None:
        table = read_table()
    if exclude is None:
        exclude = own_chain({p.pid for p in table})
    fn = {'check-no-runs': cmd_check_no_runs, 'clear-session-lock': cmd_clear_session_lock,
          'clear-updater-lock': cmd_clear_updater_lock, 'take-install-lock': cmd_take_install_lock,
          'release-install-lock': cmd_release_install_lock}[args.command]
    try:
        return fn(args, table, exclude)
    except Refused as exc:
        print(f'REFUSED: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
