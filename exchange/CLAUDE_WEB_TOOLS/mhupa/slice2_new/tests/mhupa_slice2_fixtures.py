"""MHUP-A slice 2 test fixtures: a temporary project that carries a copy of the code closure, an invented fake Python
environment for the environment inventory, a small Mode H cohort, and the invented first update. Everything is
INVENTED or copied from the repository's own code; no real draw is read or written (design v0.1r5 sections 4.1,
4.2, 5.1, Appendix H).
"""
from __future__ import annotations

import base64
import contextlib
import hashlib
import importlib.util
import shutil
import sys
from pathlib import Path
from unittest import mock

from mhupa_fixtures import grow_master
from test_e6_beta_bernoulli import write_varied_master
import _common.contract_dispatch as CD
import _common.contract_runner as CR
import _common.walk_forward as WF
from _common import closure as CL

ROOT = Path(__file__).resolve().parents[1]
SMALL_COHORT = ('E_6', 'E_7')


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- the project folder

def copy_closure(proj: Path) -> None:
    """The code closure of 4.1 into the temporary project: src/ (without __pycache__), every root .bat,
    requirements.txt. The project root the runner is patched to then has the same closure as the repository."""
    shutil.copytree(ROOT / 'src', proj / 'src', ignore=shutil.ignore_patterns('__pycache__'))
    for p in ROOT.glob('*.bat'):
        shutil.copy2(p, proj / p.name)
    for name in CL.ROOT_FILES:
        if (ROOT / name).is_file():
            shutil.copy2(ROOT / name, proj / name)


def project(tmp: Path, profile, *, variant: int = 0) -> Path:
    """A temporary project with the invented version-1 master (last row holdout_first - 1) and the code closure."""
    proj = Path(tmp) / 'project'
    write_varied_master(proj, profile, profile.holdout_first, variant)
    copy_closure(proj)
    return proj


def first_update(proj: Path, profile, *, upto: int | None = None, variant: int = 0) -> list[dict]:
    """The invented first update of design 4.1: one UPDATE row (version 2) that extends the master from
    holdout_first to `upto` (default holdout_last). Returns the ledger rows written."""
    upto = profile.holdout_last if upto is None else upto
    return grow_master(proj, profile, [list(range(profile.holdout_first, upto + 1))], variant=variant)


# ---------------------------------------------------------------- the fake environment (Appendix H rows 5-6)

def _record_hash(raw: bytes) -> str:
    return 'sha256=' + base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b'=').decode('ascii')


def fake_environment(tmp: Path) -> CL.Environment:
    """An invented venv over an invented base installation, with one installed distribution whose RECORD lists its
    files with pip's hashes. Small, so every test re-enumerates it in milliseconds."""
    base = Path(tmp) / 'base'
    venv = Path(tmp) / 'venv'
    (base / 'bin').mkdir(parents=True)
    (base / 'bin' / 'python3.99').write_bytes(b'#!fake interpreter\n')
    (base / 'lib' / 'python3.99').mkdir(parents=True)
    (base / 'lib' / 'python3.99' / 'os.py').write_bytes(b'# fake stdlib module\n')
    (base / 'lib' / 'python3.99' / '__pycache__').mkdir()
    (base / 'lib' / 'python3.99' / '__pycache__' / 'os.cpython-399.pyc').write_bytes(b'cache, irrelevant')
    (venv / 'bin').mkdir(parents=True)
    (venv / 'bin' / 'python').write_bytes(b'#!redirector\n')
    (venv / 'pyvenv.cfg').write_text(f'home = {base / "bin"}\ninclude-system-site-packages = false\nversion = 3.99.0\n')
    sp = venv / 'lib' / 'python3.99' / 'site-packages'
    pkg = sp / 'fakepkg'
    pkg.mkdir(parents=True)
    files = {'fakepkg/__init__.py': b'VALUE = 1\n', 'fakepkg/core.py': b'def f():\n    return 2\n'}
    for rel, raw in files.items():
        (sp / rel).write_bytes(raw)
    info = sp / 'fakepkg-1.0.dist-info'
    info.mkdir()
    (info / 'METADATA').write_text('Metadata-Version: 2.1\nName: fakepkg\nVersion: 1.0\n')
    rows = [f'{rel},{_record_hash(raw)},{len(raw)}' for rel, raw in files.items()]
    rows += ['fakepkg-1.0.dist-info/METADATA,' + _record_hash((info / 'METADATA').read_bytes()) + ',0',
             'fakepkg-1.0.dist-info/RECORD,,', 'fakepkg/__pycache__/core.cpython-399.pyc,,']
    (info / 'RECORD').write_text('\n'.join(rows) + '\n')
    return CL.Environment(venv_prefix=venv, base_prefix=base, site_packages=sp, scripts=venv / 'bin', windows=False)


# ---------------------------------------------------------------- the small cohort and the patches

def small_adapters():
    import Method_Contract_Runner as M
    return {m: M.ADAPTERS[m] for m in SMALL_COHORT}


_real_cohort = WF.cohort


def _small_cohort(game_id, adapters):
    members, excluded = _real_cohort(game_id, adapters)
    return [m for m in members if m['method_id'] in SMALL_COHORT], excluded


@contextlib.contextmanager
def patched(proj: Path, env: CL.Environment, *, small_cohort: bool = True):
    """The runner's and the dispatch gate's project root, the orphan marker, the environment the closure module sees, and (by default) the
    cohort restricted to E_6 and E_7 in every caller (the manifest, the plan, the runs and the score agree on it)."""
    with contextlib.ExitStack() as stack:
        stack.enter_context(mock.patch.object(CR, 'PROJECT_ROOT', proj))
        stack.enter_context(mock.patch.object(CD, 'PROJECT_ROOT', proj))
        stack.enter_context(mock.patch.object(CR, 'ORPHAN_MARKER', proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'))
        stack.enter_context(mock.patch.object(CL.Environment, 'current', staticmethod(lambda: env)))
        if small_cohort:
            stack.enter_context(mock.patch.object(WF, 'cohort', _small_cohort))
        yield


# ---------------------------------------------------------------- the updater as a module

def updater_module():
    """results_master_v0_2.py imported from src/ by path (it is a standalone tool, not a package member)."""
    path = ROOT / 'src' / 'results_master_v0_2.py'
    spec = importlib.util.spec_from_file_location('results_master_v0_2', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault('results_master_v0_2', mod)
    spec.loader.exec_module(mod)
    return mod
