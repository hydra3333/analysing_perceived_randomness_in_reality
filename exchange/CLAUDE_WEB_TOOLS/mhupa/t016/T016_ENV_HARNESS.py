"""T016 rows 6 and 7 (F2-C01): the environment inventory of MHUP-A's closure module on the real Windows interpreter.

DRAFT for review (Claude web chat, 11 November 2026). A development check for T016 only; not part of the package and
not production code. Standard library plus the clone's own src/methods/_common/closure.py (the installed bytes).

  inventory --src <CLONE>\\src
      Row 6. environment_inventory(Environment.current()) for the interpreter running this program (the main venv
      and its base installation). Reads only: the venv's pyvenv.cfg, Scripts\\ and site-packages, and the base
      installation's interpreter files, DLLs\\ and Lib\\. Writes nothing. Prints counts and the digest only.
      ENV INVENTORY PASS, or ENV INVENTORY STOP naming the first orphan or mismatch (a reviewed fix follows; never
      a hand deletion).
  orphan --src <CLONE>\\src --scratch <new folder inside scratch\\T016>
      Row 7. Copies one small real distribution (its dist-info and every file its RECORD lists, a script under
      Scripts\\ included) into <scratch>, in the venv's own layout, checks that this copy alone passes (the control), then plants
      one file no RECORD lists and checks that the inventory refuses, naming that file. Writes only inside
      <scratch>, which must not exist yet and must be inside the task's scratch folder. The real venv is only read.
      ORPHAN CHECK PASS, or ORPHAN CHECK STOP.

Never reads source_data, results or transitory_data; contacts nothing; starts no process.
"""
import argparse, os, shutil, sys
from pathlib import Path, PurePath

PLANT = 'T016_PLANTED_ORPHAN.txt'


def stop(what, msg):
    print(f'{what} STOP: {msg}')
    sys.exit(2)


def task_path_ok(p: Path, tail) -> bool:
    parts = [x.lower() for x in PurePath(os.path.normcase(str(p))).parts]
    want = ['claude_code_working_folder_tree', 'scratch', 't016'] + [t.lower() for t in tail]
    return any(parts[i:i + len(want)] == want for i in range(len(parts)))


def load_closure(src_arg):
    src = Path(src_arg)
    if not src.is_absolute() or not src.is_dir() or not task_path_ok(src, ['r', 'src']):
        stop('ENV HARNESS', f'--src must be the absolute path of the T016 task clone\'s src folder, not {src_arg!r}')
    sys.path.insert(0, str(src / 'methods'))
    from _common import closure
    origin = Path(closure.__file__).resolve()
    if origin != (src / 'methods' / '_common' / 'closure.py').resolve():
        stop('ENV HARNESS', f'closure imported from {origin}, not from the clone')
    print(f'closure module: {origin}')
    return closure


def summary(inv):
    n = sum(len(d['files']) for d in inv['distributions'])
    return (f"Python {inv['python_version']} ({inv['implementation']}); {inv['platform']}\n"
            f"interpreter files {len(inv['interpreter'])}; base-tree files {len(inv['base_trees'])}; "
            f"Scripts files {len(inv['scripts'])}; distributions {len(inv['distributions'])} with {n} recorded files\n"
            f"environment digest {inv['digest']}")


def cmd_inventory(a):
    closure = load_closure(a.src)
    env = closure.Environment.current()
    print(f'venv: {env.venv_prefix}\nbase: {env.base_prefix}')
    try:
        inv = closure.environment_inventory(env)
    except closure.ClosureRefused as exc:
        stop('ENV INVENTORY', str(exc))
    print(summary(inv))
    print('ENV INVENTORY PASS')


def pick_distribution(env, closure):
    """The smallest distribution whose RECORD files (caches aside) are all present inside the venv. Returns
    (bytes, dist-info folder, [(RECORD path, path relative to the venv)])."""
    sp, venv = env.site_packages, env.venv_prefix.resolve()
    best = None
    for info in sorted(p for p in sp.iterdir() if p.is_dir() and p.name.endswith('.dist-info')):
        rec = info / 'RECORD'
        if not rec.is_file():
            continue
        rows = [r for r, _ in closure._parse_record(rec.read_text(encoding='utf-8', errors='replace'))
                if '__pycache__' not in PurePath(r).parts]
        files, ok = [], bool(rows)
        for r in rows:
            target = Path(os.path.normpath(sp / r)).resolve()
            if not target.is_file() or venv not in target.parents:
                ok = False
                break
            files.append((r, target.relative_to(venv)))
        if ok:
            size = sum((venv / v).stat().st_size for _, v in files)
            if best is None or size < best[0]:
                best = (size, info, files)
    return best


def cmd_orphan(a):
    closure = load_closure(a.src)
    scratch = Path(a.scratch)
    if not scratch.is_absolute() or scratch.exists() or not task_path_ok(scratch.parent, []):
        stop('ORPHAN CHECK', f'--scratch must be a new absolute folder directly inside scratch\\T016, not {a.scratch!r}')
    real = closure.Environment.current()
    best = pick_distribution(real, closure)
    if best is None:
        stop('ORPHAN CHECK', 'no distribution in the venv is suitable for the copy')
    size, info, files = best
    venv = real.venv_prefix.resolve()
    sp = scratch / real.site_packages.resolve().relative_to(venv)     # the venv's layout, mirrored inside scratch
    sp.mkdir(parents=True)
    for _, v in files:                                               # a script in Scripts\ lands in scratch\Scripts
        dst = scratch / v
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(venv / v, dst)
    print(f'copied {info.name}: {len(files)} files, {size} bytes, into {scratch} (the venv\'s layout)')
    env = closure.Environment(venv_prefix=real.venv_prefix, base_prefix=real.base_prefix, site_packages=sp,
                              scripts=real.scripts, windows=real.windows)
    try:
        inv = closure.environment_inventory(env)
    except closure.ClosureRefused as exc:
        stop('ORPHAN CHECK', f'the control (the copy alone) was refused: {exc}')
    print(f'control PASS: {len(inv["distributions"])} distribution, no orphan')
    (sp / PLANT).write_bytes(b'planted by T016 row 7; not a module\n')
    try:
        closure.environment_inventory(env)
    except closure.ClosureRefused as exc:
        msg = str(exc)
        print(f'refused: {msg}')
        if PLANT not in msg:
            stop('ORPHAN CHECK', 'refused, but not naming the planted file')
        print('ORPHAN CHECK PASS: the planted file was refused by name')
        return
    stop('ORPHAN CHECK', 'the planted file was NOT refused')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('inventory'); s.add_argument('--src', required=True)
    s = sub.add_parser('orphan'); s.add_argument('--src', required=True); s.add_argument('--scratch', required=True)
    a = ap.parse_args()
    (cmd_inventory if a.cmd == 'inventory' else cmd_orphan)(a)


if __name__ == '__main__':
    main()
