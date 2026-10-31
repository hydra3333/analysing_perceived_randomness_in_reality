"""CODE-3 tests: the revision-labelled archive (E2R-R54 to R56, T15; CODE-3 and E_1 revision 2 design v0.1r2,
owner-ratified 31 October 2026). OFFLINE.

E1R2-T07: E_1 revision 1's installed archive (file list, bytes, README, helper references, no package marker) and the
archive-exclusion checks (static over src/ and tests/, and at run time after a listed import inventory and E_1's
contract path in both games). E1R2-T08 (E2R-T15): the retirement tooling on an invented method E_998 in temporary
trees, with and without Git history, for a dropped path, a reused path with new bytes and a reused unchanged path.
Archive files are read as bytes only; nothing under archive/ is imported or run. No real data is read.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from package_tools import method_retirement as MR

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'archive' / 'methods' / 'E_001' / 'r1'
R1_FILES = ['E_001/__init__.py', 'E_001/e1_common_reader_bridge.py', 'E_001/e1_historical_appearance_frequency.py',
            'E_001/e1_standalone_contract.py', 'E_001/e1_training_view.py', 'E_001/multigame_e1.py',
            'E_001_Historical_Appearance_Frequency.py']
# Revision 2's only code changes (design v0.1r2 section 3): r1 text -> r2 text, each occurring once.
R2_CHANGES = {
    'E_001/multigame_e1.py': [(
        "    if data_kind != 'SYNTHETIC_CONTRACT_TEST':\n"
        "        # This new multi-game science runner remains OFF until later review.\n",
        "    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):\n"
        "        # Revision 2 (owner decision WF1-13): synthetic contract tests and real development runs only.\n")],
    'E_001_Historical_Appearance_Frequency.py': [(
        "        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '1')\n",
        "        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '2')\n")],
}
# The only files that may name the archive's folders: they compare archived bytes, or are the tooling itself.
BYTE_COMPARISON_FILES = [ROOT / 'src' / 'package_tools' / 'method_retirement.py',
                         ROOT / 'tests' / 'test_code3_retirement.py']
# T07's runtime import inventory: library modules only, each without side effects on import (no entry-point
# script such as a Method_*.py, E_001_Historical_Appearance_Frequency.py, the coordinator or a scraper).
IMPORT_INVENTORY = [
    '_common.canonical_encoding', '_common.game_profiles', '_common.game_draws_reader', '_common.contract_vocab',
    '_common.contract_records', '_common.contract_registry', '_common.contract_dispatch', '_common.contract_task',
    '_common.contract_forecast', '_common.contract_receipts', '_common.contract_publication',
    '_common.contract_runner', '_common.walk_forward', '_common.occurrence_counts', '_common.polynomial_fits',
    '_common.recurrence_gaps', 'E_001.e1_historical_appearance_frequency', 'E_001.multigame_e1',
    'E_001.e1_training_view', 'E_001.e1_common_reader_bridge', 'E_001.e1_standalone_contract',
    'contract_adapters.e_001', 'package_tools.method_retirement',
]


def r1_bytes_from_live(rel: str) -> bytes:
    """Revision 1's bytes, rebuilt from the live revision-2 file by reversing the two known edits."""
    text = (ROOT / 'src' / 'methods' / rel).read_bytes().replace(b'\r\n', b'\n').decode('ascii')
    for r1, r2 in R2_CHANGES.get(rel, []):
        assert text.count(r2) == 1, rel
        text = text.replace(r2, r1)
    return text.encode('ascii')


class InstalledArchive(unittest.TestCase):
    """E1R2-T07 (E2R-R54, R55)."""

    def test_archive_holds_revision_1_complete(self):
        baseline = {rel: r1_bytes_from_live(rel) for rel in R1_FILES}
        self.assertEqual(MR.check_archive(ROOT, 'E_1', '1', R1_FILES, baseline, normalise_eol=True), [])
        for rel in R1_FILES:                                  # the live paths hold revision 2 (all reused, ER-3)
            self.assertTrue((ROOT / 'src' / 'methods' / rel).is_file(), rel)
        changed = [rel for rel in R1_FILES if (ARCHIVE / rel).read_bytes().replace(b'\r\n', b'\n') !=
                   (ROOT / 'src' / 'methods' / rel).read_bytes().replace(b'\r\n', b'\n')]
        self.assertEqual(changed, sorted(R2_CHANGES))

    def test_readme_fields(self):
        text = (ARCHIVE / 'README.md').read_bytes().decode('ascii').replace('\r\n', '\n')
        self.assertIn('# E_1 revision 1 (archived)', text)
        self.assertIn('- **Prepared:** ', text)
        self.assertIn('- **Retired:** when the owner installs that package. The installation date and commit are '
                      'recorded in the ratification register, not here.', text)
        self.assertIn('- **Superseded by:** revision 2.', text)
        self.assertIn('exact historical replay is not promised', text)
        self.assertEqual(MR.HELPER_LINE.findall(text), [
            ('_common/canonical_encoding.py', '1'), ('_common/game_profiles.py', '1'),
            ('_common/game_draws_reader.py', '1'), ('_common/experiment_runtime_status_and_resources.py', '1'),
            ('_common/contract_dispatch.py', '1')])

    def test_the_archive_is_no_package_and_only_r1_exists(self):
        self.assertEqual(sorted(p.name for p in (ROOT / 'archive').iterdir()), ['methods'])
        self.assertEqual(sorted(p.name for p in (ROOT / 'archive' / 'methods').iterdir()), ['E_001'])
        self.assertEqual(sorted(p.name for p in (ROOT / 'archive' / 'methods' / 'E_001').iterdir()), ['r1'])


class ArchiveIsNeverExecuted(unittest.TestCase):
    """E1R2-T07 (E2R-R56; EX_087 C01): no test-only exception."""

    def test_static(self):
        files = [*(ROOT / 'src').rglob('*.py'), *(ROOT / 'tests').glob('*.py')]
        self.assertEqual(MR.archive_execution_findings(files, allowed=BYTE_COMPARISON_FILES), [])

    def test_static_check_catches_loading(self):
        with tempfile.TemporaryDirectory() as td:
            cases = {
                'a.py': 'import archive.methods.E_001\n',
                'b.py': 'import importlib\nimportlib.import_module("archive.methods.E_001.r1")\n',
                'c.py': 'import importlib.util as u\nu.spec_from_file_location("m", "archive/methods/x.py")\n',
                'd.py': 'import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(".") / "archive"))\n',
                'e.py': 'import runpy\nrunpy.run_path("archive/methods/E_001/r1/E_001/multigame_e1.py")\n',
                'f.py': 'p = "archive\\\\methods\\\\E_001\\\\r1"\n',
                'ok.py': 'u = "https://example.invalid/australia/archive/"\nw = "archive"\n',
            }
            for name, src in cases.items():
                (Path(td) / name).write_text(src)
            found = MR.archive_execution_findings(sorted(Path(td).glob('*.py')))
            self.assertEqual(sorted({f.split(':')[0] for f in found}), ['a.py', 'b.py', 'c.py', 'd.py', 'e.py', 'f.py'])
            for specific in ('a.py:1: imports archive.methods.E_001',                 # each rule is caught by itself
                             'b.py:2: importlib.import_module() names an archive path',
                             'c.py:2: u.spec_from_file_location() names an archive path',
                             'd.py:3: sys.path.insert() names an archive path',
                             'e.py:2: runpy.run_path() names an archive path',
                             'f.py: names an archive path but is not an allowed byte-comparison file'):
                self.assertIn(specific, found)

    def test_static_check_catches_constructed_paths(self):
        """EX_093 B01: a path into the archive built from parts is found, whatever builds it; each case gives its own
        finding. Ordinary uses of the word "archive" are not flagged. Nothing here is run."""
        with tempfile.TemporaryDirectory() as td:
            cases = {
                'counterexample.py': ('from pathlib import Path\n'
                                      'p = Path("archive") / "methods" / "E_001" / "r1" / "E_001" / "multigame_e1.py"\n'
                                      'exec(p.read_text())\n'),
                'div.py': 'from pathlib import Path\nx = Path("archive") / "methods"\n',
                'args.py': 'from pathlib import Path\nx = Path("archive", "methods", "E_001")\n',
                'joinpath.py': 'from pathlib import Path\nx = Path("archive").joinpath("common")\n',
                'rootdiv.py': 'from pathlib import Path\nroot = Path(".")\nx = root / "archive" / "methods"\n',
                'plus.py': 'x = "archive" + "/methods"\n',
                'starjoin.py': 'import os\nx = os.path.join(*["archive", "methods"])\n',
                'pure.py': 'from pathlib import PurePosixPath\nx = PurePosixPath("archive", "common", "h")\n',
                'o02.py': ('from pathlib import Path\nroot = Path("archive")\n'           # EX_095 O02: across statements
                           'path = root / "methods" / "E_001" / "r1" / "E_001" / "multigame_e1.py"\nexec(path.read_text())\n'),
                'o02cwd.py': 'from pathlib import Path\nbase = Path.cwd() / "archive"\n',
                'o02join.py': 'import os\nbase = os.path.join("archive")\n',
                'ok.py': ('u = "https://example.invalid/australia/archive/"\nw = "archive"\n'
                          'msg = "archive the ORIGINAL marker"\nfrom pathlib import Path\ny = Path("results") / "methods"\n'
                          'z = Path("results") / "archive_notes.txt"\n'),
            }
            for name, src in cases.items():
                (Path(td) / name).write_text(src)
            found = MR.archive_execution_findings(sorted(Path(td).glob('*.py')))
            for name in cases:
                want = f'{name}: names an archive path but is not an allowed byte-comparison file'
                if name == 'ok.py':
                    self.assertNotIn(want, found)
                else:
                    self.assertIn(want, found)
            self.assertEqual(len(found), len(cases) - 1)

    def test_runtime(self):
        """In a fresh process: import the inventory, then run E_1's contract path in both games on invented data;
        no loaded module comes from archive/: no module file, no namespace package (PEP 420: a folder without
        __init__.py can still be imported, so the check does not rely on that) and no module named archive...;
        and no sys.path entry lies inside archive/. The child runs from the repository root, as the suite does."""
        child = r'''
import importlib, json, sys, tempfile
from pathlib import Path
for m in json.loads(sys.argv[1]):
    importlib.import_module(m)
import e2r_code2_fixtures as C
import _common.contract_runner as CR
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import get_profile
from contract_adapters import e_001
from test_e6_beta_bernoulli import write_varied_master
td = Path(tempfile.mkdtemp())
outcomes = []
with C.installed(marker=td / 'no_marker'):
    for game, t in (('POWERBALL', 1360), ('OZLOTTO', 1583)):
        reg = InstalledRegistry()
        e = reg.active_entry(game, *C.E1)
        d = reg.declaration(e['declaration_digest'])
        sha = write_varied_master(td / game, get_profile(game), t, 0)
        res = CR.run_contract_method(C.request(d, e, t, sha, run_id='mg-' + '2' * 32), compute=e_001.compute,
                                     verify=e_001.verify, repo_root=td / game, run_root=td / 'runs')
        outcomes.append(json.loads((res.folder / 'terminal.json').read_bytes())['outcome'])
arch = (Path(sys.argv[2]) / 'archive').resolve()
def inside(p):
    return p is not None and Path(p).resolve().is_relative_to(arch)
bad = sorted(n for n, m in list(sys.modules.items())
             if n == 'archive' or n.startswith('archive.') or inside(getattr(m, '__file__', None))
             or any(inside(p) for p in (getattr(m, '__path__', None) or [])))
paths = [p for p in sys.path if 'archive' in Path(p).parts]
print(json.dumps({'bad': bad, 'paths': paths, 'outcomes': outcomes, 'n': len(sys.modules)}))
'''
        r = subprocess.run([sys.executable, '-B', '-c', child, json.dumps(IMPORT_INVENTORY), str(ROOT)],
                           capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])
        out = json.loads(r.stdout.strip().splitlines()[-1])
        self.assertEqual((out['bad'], out['paths']), ([], []))
        self.assertEqual(out['outcomes'], ['SUCCESS', 'SUCCESS'])


# ---------------------------------------------------------------- E1R2-T08: E2R-T15 on an invented method

E998 = {
    'E_998/__init__.py': b'',
    'E_998/kept.py': b'VALUE = 1  # unchanged by revision 2\n',
    'E_998/changed.py': b'RULE = "revision 1"\n',
    'E_998/dropped.py': b'OLD = True  # revision 2 does not reuse this path\n',
}
E998_R2 = {'E_998/changed.py': b'RULE = "revision 2"\n'}


def synthetic_tree(root: Path) -> None:
    for rel, raw in E998.items():
        p = root / 'src' / 'methods' / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
    for helper in ('canonical_encoding.py', 'game_profiles.py'):
        p = root / 'src' / 'methods' / '_common' / helper
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b'# invented helper\n')


def git(root: Path, *args) -> None:
    subprocess.run(['git', '-C', str(root), '-c', 'user.name=t', '-c', 'user.email=t@t', *args], check=True,
                   capture_output=True)


class RetirementT15(unittest.TestCase):
    """E1R2-T08 (E2R-T15): retire E_998 revision 1 and install revision 2, with and without Git history."""

    def retire_and_check(self, with_git: bool):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'repo'
            synthetic_tree(root)
            if with_git:
                git(root, 'init', '-q')
                git(root, 'add', '-A')
                git(root, 'commit', '-q', '-m', 'r1')
            self.assertEqual((root / '.git').exists(), with_git)
            baseline = {rel: (root / 'src' / 'methods' / rel).read_bytes() for rel in E998}   # saved pre-install bytes
            readme = MR.readme_text(method_id='E_998', method_name='Invented', revision='1', successor_revision='2',
                                    variants=['V1'], games=['POWERBALL'], prepared='2026-10-31',
                                    previous_paths=list(E998), helpers={'_common/canonical_encoding.py': '1',
                                                                        '_common/game_profiles.py': '1'},
                                    reason='a test.', replay_note='Not replayed.')
            MR.retire(root, 'E_998', '1', list(E998), readme, drop=['E_998/dropped.py'])
            for rel, raw in E998_R2.items():                                      # the successor's overlay
                (root / 'src' / 'methods' / rel).write_bytes(raw)
            self.assertEqual(MR.check_archive(root, 'E_998', '1', list(E998), baseline), [])
            live = root / 'src' / 'methods'
            self.assertFalse((live / 'E_998' / 'dropped.py').exists())                # dropped: old path absent
            self.assertEqual((live / 'E_998' / 'changed.py').read_bytes(), E998_R2['E_998/changed.py'])
            self.assertEqual((live / 'E_998' / 'kept.py').read_bytes(), E998['E_998/kept.py'])
            arch = root / 'archive' / 'methods' / 'E_998' / 'r1'
            for rel, raw in E998.items():                                           # r1 complete in the archive
                self.assertEqual((arch / rel).read_bytes(), raw)
            files = [*(root / 'src').rglob('*.py')]
            self.assertEqual(MR.archive_execution_findings(files), [])
            # Damage is found: a changed archived byte, a missing file, a package marker, an unresolved helper.
            (arch / 'E_998' / 'kept.py').write_bytes(b'VALUE = 2\n')
            (arch / 'E_998' / 'dropped.py').unlink()
            (root / 'archive' / '__init__.py').write_bytes(b'')
            (live / '_common' / 'game_profiles.py').unlink()
            problems = '\n'.join(MR.check_archive(root, 'E_998', '1', list(E998), baseline))
            for needle in ('kept.py: bytes differ', "missing ['E_998/dropped.py']", 'archive/__init__.py',
                           'helper _common/game_profiles.py revision 1 resolves to nothing'):
                self.assertIn(needle, problems)

    def test_with_git_history(self):
        if shutil.which('git') is None:
            self.skipTest('git is not installed')
        self.retire_and_check(True)

    def test_without_git_history(self):
        self.retire_and_check(False)

    def test_retire_checks_every_input_before_writing(self):
        """EX_093 O01: a missing or repeated input is refused before anything is created."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            synthetic_tree(root)
            for files in (['E_998/kept.py', 'E_998/missing.py'], ['E_998/kept.py', 'E_998/kept.py'],
                          ['E_998/kept.py', 'E_998']):
                with self.assertRaises(ValueError):
                    MR.retire(root, 'E_998', '1', files, 'x')
                self.assertFalse((root / 'archive').exists(), files)

    def test_refusals(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            synthetic_tree(root)
            with self.assertRaises(ValueError):
                MR.retire(root, 'E_998', '1', list(E998), 'x', drop=['E_998/other.py'])   # drop must be archived
            MR.retire(root, 'E_998', '1', ['E_998/kept.py'], 'x')
            with self.assertRaises(ValueError):
                MR.retire(root, 'E_998', '1', ['E_998/kept.py'], 'x')                    # never overwrites
            for bad in ('E998', 'E_0', 'E_1000'):
                with self.assertRaises(ValueError):
                    MR.method_folder(bad)
            with self.assertRaises(ValueError):
                MR.readme_text(method_id='E_998', method_name='\u00e9', revision='1', successor_revision='2',
                               variants=[], games=[], prepared='d', previous_paths=[], helpers={}, reason='',
                               replay_note='')


if __name__ == '__main__':
    unittest.main()
