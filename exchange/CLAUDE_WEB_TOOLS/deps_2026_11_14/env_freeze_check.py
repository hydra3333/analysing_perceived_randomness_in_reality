#!/usr/bin/env python3
"""Read-only: would Mode H's environment freeze accept the Python environment running this script? (Claude web chat,
14 November 2026, after the owner's dependency change.) It imports the installed closure module from a clone (--repo),
calls its own environment_inventory() on the running interpreter's venv exactly as `manifest` would, and prints the
result. On a refusal it also lists every problem it can find (orphans, RECORD mismatches), not only the first.
It writes nothing, reads only the venv and its base Python, and prints file names, package names, versions and hashes.

Usage (the project venv's Python, isolated): python -I -B env_freeze_check.py --repo <clone>
Prints `ENV PASS: ...` or `ENV REFUSED: ...`; exit code 0 for PASS, 3 for REFUSED, 2 for a usage problem.
"""
import argparse
import sys
from pathlib import Path


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--repo', required=True)
    args = a.parse_args()
    repo = Path(args.repo).resolve()
    src = repo / 'src' / 'methods'
    if not (src / '_common' / 'closure.py').is_file():
        print(f'USAGE: {src}/_common/closure.py not found'); return 2
    sys.path[:0] = [str(src), str(repo / 'src')]
    from _common import closure as C
    env = C.Environment.current()
    print(f'interpreter: {sys.executable}')
    print(f'venv: {env.venv_prefix}; base: {env.base_prefix}; site-packages: {env.site_packages}')
    print(f'closure module: {Path(C.__file__).resolve()}')
    try:
        inv = C.environment_inventory(env)
    except C.ClosureRefused as exc:
        print(f'ENV REFUSED: {exc}')
        sp = env.site_packages
        listed, bad = set(), []
        for info in sorted(p for p in sp.iterdir() if p.is_dir() and p.name.endswith('.dist-info')):
            rec = info / 'RECORD'
            if not rec.is_file():
                bad.append(f'no RECORD: {info.name}'); continue
            for rel, digest in C._parse_record(rec.read_text(encoding='utf-8', errors='replace')):
                t = (sp / rel).resolve(); listed.add(t)
                if '__pycache__' in Path(rel).parts:
                    continue
                if not t.is_file():
                    bad.append(f'missing: {info.name}: {rel}')
                elif digest is not None and C._sha(t) != digest:
                    bad.append(f'differs from RECORD: {info.name}: {rel}')
        orphans = [C._rel(p, sp) for p in C._files(sp) if p.resolve() not in listed]
        print(f'problems: {len(bad)} RECORD problem(s), {len(orphans)} orphan file(s) under site-packages')
        for line in bad[:40]:
            print('  ' + line)
        for o in orphans[:40]:
            print('  orphan: ' + o)
        return 3
    d = inv['distributions']
    print(f'distributions: {len(d)}')
    for x in d:
        print(f"  {x['name']}=={x['version']}")
    print(f"ENV PASS: {len(d)} distributions, no orphan, every RECORD file present and matching; "
          f"python {inv['python_version']}; environment digest {inv['digest']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
