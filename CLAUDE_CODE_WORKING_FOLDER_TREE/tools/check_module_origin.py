"""Check that the project modules a test run uses come from the task clone, not from the main repository.

Written by the Claude web chat, 29 October 2026 (v2: uses the CODE-1 v2 registry accessors). Read-only: it imports modules (no program is run) and
loads the installed contract registry from the clone's own contract_data. It reads no source_data,
results or transitory_data.
Usage: <venv python> -I check_module_origin.py --repo <task clone>
Prints ORIGIN PASS or ORIGIN STOP.
"""
import argparse, importlib, os, site, sys, sysconfig
from pathlib import Path

MODULES = [
    '_common.contract_vocab', '_common.contract_records', '_common.contract_task', '_common.contract_forecast',
    '_common.contract_receipts', '_common.contract_registry', '_common.canonical_encoding',
    '_common.game_profiles', '_common.game_draws_reader', 'E_001.multigame_e1', 'e2r_fixtures',
]
MAIN = Path(__file__).resolve().parents[2]


def norm(p):
    return os.path.normcase(str(Path(p).resolve()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    repo = ap.parse_args().repo.resolve()
    bad = []
    print('python:', sys.executable, sys.version.split()[0])
    # 1. Nothing in the venv points at the main repository (for example an editable install or a .pth file).
    for d in {*site.getsitepackages(), sysconfig.get_paths()['purelib']}:
        for pth in sorted(Path(d).glob('*.pth')) if Path(d).is_dir() else []:
            text = pth.read_text(encoding='utf-8', errors='replace')
            if 'analysing_perceived' in text or norm(MAIN) in os.path.normcase(text):
                bad.append(f'{pth} refers to the main repository')
        print('checked .pth files in', d)
    # 2. Import from the clone only, and check where each module came from.
    sys.path[:0] = [str(repo / 'src' / 'methods'), str(repo / 'src'), str(repo / 'tests')]
    for name in MODULES:
        mod = importlib.import_module(name)
        f = Path(mod.__file__).resolve()
        ok = norm(f).startswith(norm(repo) + os.sep)
        print(f'{"ok  " if ok else "BAD "} {name:<36} {f}')
        if not ok:
            bad.append(f'{name} imported from {f}')
    # 3. The installed registry loads from the clone's contract_data, with its line endings as checked out.
    from _common import contract_registry as CR
    data = Path(CR.DATA_ROOT)
    files = sorted(data.rglob('*.json'))
    crlf = sum(1 for p in files if b'\r\n' in p.read_bytes())
    reg = CR.InstalledRegistry()
    print(f'contract_data: {data}')
    print(f'contract_data files: {len(files)}, with CRLF line endings: {crlf}')
    # CODE-1 v2 accessors (E2RC1-B01); v1's public attributes were removed in v2.
    print(f'registry loaded: {len(reg.declaration_digests())} declarations, {len(reg.chain_keys())} registry chains')
    if not norm(data).startswith(norm(repo) + os.sep):
        bad.append(f'contract_data is outside the clone: {data}')
    if bad:
        print('ORIGIN STOP:')
        for b in bad:
            print('  ' + b)
        sys.exit(1)
    print('ORIGIN PASS: every checked module and the contract data come from the task clone')


if __name__ == '__main__':
    main()
