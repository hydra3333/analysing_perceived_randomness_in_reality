"""MHUP-A (design v0.1r5 section 4.3; Appendix J steps 12 and 16; Appendix L items L-D1-L-D3 and the record tool's
refusals): install_records.py on a temporary Git repository that carries a copy of the installed registry and the
install records. OFFLINE; the repository is never touched. The baseline release record is validated against the
installed registry, and its released set plus E_1 revision 3 (released by MHUP-A's own release record at install)
is shown to be exactly the registry's released set.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'src' / 'package_tools' / 'install_records.py'
DATA = Path('src') / 'methods' / '_common' / 'contract_data'
GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@example.invalid', GIT_COMMITTER_NAME='t',
               GIT_COMMITTER_EMAIL='t@example.invalid', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')     # no user or system Git config on any platform


def load():
    spec = importlib.util.spec_from_file_location('install_records', TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['install_records'] = mod
    spec.loader.exec_module(mod)
    return mod


IR = load()
BASELINE_SHA256 = 'a480cbe125a574344fc9c47f47576c49d22d42d77e1abcf1636d8340090126cd'


def git(root: Path, *args) -> str:
    return subprocess.run(['git', '-C', str(root), *args], env=GIT_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=True).stdout.decode()


class Repo(unittest.TestCase):
    """A temporary repository: the installed registry and install records copied, committed as HEAD."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name).resolve() / 'repo'
        shutil.copytree(ROOT / DATA / 'registry', self.root / DATA / 'registry', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / DATA / 'install_records', self.root / DATA / 'install_records')
        (self.root / 'src' / 'package_tools').mkdir(parents=True)
        shutil.copy2(TOOL, self.root / 'src' / 'package_tools' / 'install_records.py')
        shutil.copy2(ROOT / 'src' / 'package_tools' / 'process_check.py', self.root / 'src' / 'package_tools' / 'process_check.py')
        git(self.root, 'init', '-q')
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'base')
        self.manifest = Path(self._td.name) / 'PACKAGE_MANIFEST.json'
        self.manifest.write_text(json.dumps({'package': 'TESTPKG', 'release_entries': [
            {'game_id': 'POWERBALL', 'method_id': 'E_1', 'method_revision': '3', 'variant_id': 'FULL_HISTORY_RAW_COUNTS_V1'},
            {'game_id': 'OZLOTTO', 'method_id': 'E_1', 'method_revision': '3', 'variant_id': 'FULL_HISTORY_RAW_COUNTS_V1'}],
            'registry_entries_added': ['src/methods/_common/contract_data/registry/POWERBALL/E_1/FULL_HISTORY_RAW_COUNTS_V1/entry_0003.json']}))
        self.barrier = self.root / IR.BARRIER_REL

    def tearDown(self):
        self._td.cleanup()

    def run_tool(self, *argv) -> tuple[int, str]:
        buf = io.StringIO()
        with mock.patch.object(sys, 'stdout', buf):
            rc = IR.main([*argv])
        return rc, buf.getvalue().strip()

    def install(self):
        self.barrier.write_text('install in progress')
        rc, out = self.run_tool('install-record', '--root', str(self.root), '--package', 'TESTPKG', '--manifest', str(self.manifest))
        self.assertEqual(rc, 0, out)
        self.barrier.unlink()
        return self.root / IR.RECORDS_REL / 'INSTALL_TESTPKG_V1.json'


class Baseline(Repo):

    def test_baseline_record_validates_against_the_installed_registry(self):
        path = ROOT / IR.RECORDS_REL / IR.BASELINE_NAME
        raw = path.read_bytes()
        self.assertEqual(IR.sha256(raw), BASELINE_SHA256)
        rec = json.loads(raw.decode('ascii'))
        self.assertEqual(IR.canonical(rec), raw)
        self.assertEqual((rec['schema'], rec['package'], rec['local_date']), ('RELEASE_RECORD_V1', 'BASELINE_20261031', '2026-10-31'))
        self.assertEqual(len(rec['entries']), 80)
        per_game = {g: [e for e in rec['entries'] if e['game_id'] == g] for g in IR.GAMES}
        self.assertEqual({g: len(v) for g, v in per_game.items()}, {'POWERBALL': 40, 'OZLOTTO': 40})
        superseded = [e for e in rec['entries'] if e.get('superseded_by')]
        self.assertEqual([(e['game_id'], e['method_id'], e['method_revision'], e['superseded_by']) for e in superseded],
                         [('OZLOTTO', 'E_1', '2', '3'), ('POWERBALL', 'E_1', '2', '3')])
        self.assertIsNone(rec['install_record_sha256'])
        recs = IR.validate_records(ROOT)
        self.assertEqual([r['_file'] for r in recs['releases']], [IR.BASELINE_NAME])
        released = IR.released_variants(ROOT)
        self.assertEqual(len(released), 78)
        self.assertEqual(set(released.values()), {'2026-10-31'})
        # the registry's released set (SUPPORTED, active) = the baseline's unretired entries + E_1 revision 3, which
        # MHUP-A's own release record names at its install (design 4.3)
        sys.path.insert(0, str(ROOT / 'src' / 'methods'))
        from _common.contract_registry import InstalledRegistry
        reg = InstalledRegistry()
        supported = set()
        for (g, m, v) in reg.chain_keys():
            e = reg.active_entry(g, m, v)
            if e['registry_status'] == 'SUPPORTED':
                supported.add((g, m, e['method_revision'], v))
        expected = set(released) | {(g, 'E_1', '3', 'FULL_HISTORY_RAW_COUNTS_V1') for g in IR.GAMES}
        self.assertEqual(supported, expected)
        # the baseline's two dates agree with each other; what makes it the exception is that no install record
        # precedes it (install_record_sha256 is null): as an ordinary record it would be refused by validate_records
        IR.validate_release(rec, ROOT, is_baseline=True)
        IR.validate_release(rec, ROOT, is_baseline=False)

    def test_validate_command_and_tampering(self):
        rc, out = self.run_tool('validate', '--root', str(self.root))
        self.assertEqual(rc, 0, out)
        self.assertIn('RECORDS PASS: 0 install record(s), 1 release record(s), 78 released unretired entries', out)
        path = self.root / IR.RECORDS_REL / IR.BASELINE_NAME
        rec = json.loads(path.read_bytes())
        rec['entries'][0]['method_revision'] = '9'
        path.write_bytes(IR.canonical(rec))
        rc, out = self.run_tool('validate', '--root', str(self.root))
        self.assertEqual(rc, 1)
        self.assertIn('has no registry chain entry', out)
        path.write_bytes(IR.canonical(rec) + b' ')
        rc, out = self.run_tool('validate', '--root', str(self.root))
        self.assertIn('not its canonical bytes', out)
        # the baseline copied under another name is an ordinary record: no install record precedes it
        path.write_bytes(raw := (ROOT / IR.RECORDS_REL / IR.BASELINE_NAME).read_bytes())
        copy = path.with_name('RELEASE_COPY_V1.json')
        copy.write_bytes(raw)
        rc, out = self.run_tool('validate', '--root', str(self.root))
        self.assertEqual(rc, 1)
        self.assertIn('install record is not present', out)
        copy.unlink()
        rc, out = self.run_tool('validate', '--root', 'relative')
        self.assertEqual(rc, 1)


class Records(Repo):

    def test_install_record_needs_the_barrier_and_is_create_only(self):
        rc, out = self.run_tool('install-record', '--root', str(self.root), '--package', 'TESTPKG', '--manifest', str(self.manifest))
        self.assertEqual(rc, 1)
        self.assertIn('barrier P is absent', out)
        self.assertEqual(sorted(p.name for p in (self.root / IR.RECORDS_REL).iterdir()), [IR.BASELINE_NAME])
        path = self.install()
        rec = json.loads(path.read_bytes())
        self.assertEqual((rec['schema'], rec['package']), ('INSTALL_RECORD_V1', 'TESTPKG'))
        self.assertEqual(rec['manifest_sha256'], IR.sha256(self.manifest.read_bytes()))
        self.assertEqual(rec['local_date'], date.today().isoformat())
        self.assertEqual(len(rec['release_entries_planned']), 2)
        self.assertIn('qualifies no variant', rec['statement'])
        self.barrier.write_text('again')
        rc, out = self.run_tool('install-record', '--root', str(self.root), '--package', 'TESTPKG', '--manifest', str(self.manifest))
        self.assertEqual(rc, 1)
        self.assertIn('already exists (create-only)', out)
        rc, out = self.run_tool('install-record', '--root', str(self.root), '--package', 'OTHER', '--manifest', str(self.manifest))
        self.assertIn('does not match the manifest', out)
        # L-D1: a STOP after POST leaves the install record only; the variant is not released
        self.assertEqual(IR.released_variants(self.root).get(('POWERBALL', 'E_1', '3', 'FULL_HISTORY_RAW_COUNTS_V1')), None)
        rc, out = self.run_tool('validate', '--root', str(self.root))
        self.assertEqual(rc, 0)
        self.assertIn('1 install record(s), 1 release record(s), 78 released', out)

    def test_release_record_conditions_in_order(self):
        path = self.install()
        args = ('release-record', '--root', str(self.root), '--package', 'TESTPKG', '--manifest', str(self.manifest))
        # P present
        self.barrier.write_text('x')
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 1)
        self.assertIn('barrier P still exists', out)
        self.barrier.unlink()
        # the install record not committed
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 1)
        self.assertIn('not committed at HEAD', out)
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'package')
        # tracked changes
        reg_file = next((self.root / DATA / 'registry').glob('POWERBALL/E_6/*/entry_0001.json'))
        original = reg_file.read_bytes()
        reg_file.write_bytes(original + b'\n')
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 1)
        self.assertIn('tracked files differ from HEAD', out)
        reg_file.write_bytes(original)
        # a session lock
        lock = self.root / 'results' / 'real' / 'weekly' / 'OZLOTTO' / 'ACTIVE_SESSION.lock'
        lock.parent.mkdir(parents=True)
        lock.write_text('x')
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 1)
        self.assertIn('OZLOTTO: a session lock exists', out)
        lock.unlink()
        # an unfinished weekly set (a roster-changing release waits; EX_129 C01)
        sessions = self.root / 'results' / 'real' / 'weekly' / 'POWERBALL' / 'sessions'
        sessions.mkdir(parents=True)
        (sessions / ('SESSION_' + 'a' * 32 + '_attempts.jsonl')).write_text(
            json.dumps({'schema': 'TICKET_V1', 'kind': 'SET_STARTED', 'target_draw_number': 1590}) + '\n')
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 1)
        self.assertIn('unfinished weekly set (targets [1590])', out)
        (self.root / 'results' / 'real' / 'weekly' / 'POWERBALL' / 'FORECAST_LEDGER_V1.jsonl').write_text(
            json.dumps({'schema': 'FREEZE_LINE_V1', 'target_draw_number': 1590}) + '\n')
        # nothing written so far
        self.assertEqual(sorted(p.name for p in (self.root / IR.RECORDS_REL).iterdir()), ['INSTALL_TESTPKG_V1.json', IR.BASELINE_NAME])
        # a committed, clean tree: the release record is written, dated today, naming the install record's digest
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 0, out)
        rel = json.loads((self.root / IR.RECORDS_REL / 'RELEASE_TESTPKG_V1.json').read_bytes())
        self.assertEqual((rel['schema'], rel['package'], rel['local_date']), ('RELEASE_RECORD_V1', 'TESTPKG', date.today().isoformat()))
        self.assertEqual(rel['install_record_sha256'], IR.sha256(path.read_bytes()))
        self.assertEqual(len(rel['entries']), 2)
        released = IR.released_variants(self.root)
        self.assertEqual(released[('POWERBALL', 'E_1', '3', 'FULL_HISTORY_RAW_COUNTS_V1')], date.today().isoformat())
        self.assertEqual(len(released), 80)
        self.assertNotIn(('POWERBALL', 'E_1', '2', 'FULL_HISTORY_RAW_COUNTS_V1'), released)      # superseded stays retired
        # create-only, and L-D3: a second record naming an entry already named is refused
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 1)
        self.assertIn('already exists (create-only)', out)
        other = Path(self._td.name) / 'OTHER.json'
        other.write_text(json.dumps({'package': 'OTHER', 'release_entries': [
            {'game_id': 'POWERBALL', 'method_id': 'E_1', 'method_revision': '3', 'variant_id': 'FULL_HISTORY_RAW_COUNTS_V1'}]}))
        self.barrier.write_text('x')
        rc, out = self.run_tool('install-record', '--root', str(self.root), '--package', 'OTHER', '--manifest', str(other))
        self.assertEqual(rc, 0, out)
        self.barrier.unlink()
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'other')
        rc, out = self.run_tool('release-record', '--root', str(self.root), '--package', 'OTHER', '--manifest', str(other))
        self.assertEqual(rc, 1)
        self.assertIn('already named by an earlier release record', out)
        # a planted duplicate is caught by validation too
        dup = self.root / IR.RECORDS_REL / 'RELEASE_DUP_V1.json'
        dup.write_bytes(IR.canonical(dict(rel, package='DUP')))
        rc, out = self.run_tool('validate', '--root', str(self.root))
        self.assertEqual(rc, 1)
        self.assertIn('both name', out)
        dup.unlink()
        # an entry with no registry chain entry is refused at writing
        bad = Path(self._td.name) / 'BAD.json'
        bad.write_text(json.dumps({'package': 'BAD', 'release_entries': [
            {'game_id': 'POWERBALL', 'method_id': 'E_99', 'method_revision': '1', 'variant_id': 'X'}]}))
        self.barrier.write_text('x')
        self.run_tool('install-record', '--root', str(self.root), '--package', 'BAD', '--manifest', str(bad))
        self.barrier.unlink()
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'bad')
        rc, out = self.run_tool('release-record', '--root', str(self.root), '--package', 'BAD', '--manifest', str(bad))
        self.assertEqual(rc, 1)
        self.assertIn('has no registry chain entry', out)
        self.assertFalse((self.root / IR.RECORDS_REL / 'RELEASE_BAD_V1.json').exists())

    def test_release_date_is_the_day_of_writing(self):
        # L-D2: 23:58 and 00:02 local: the date comes from the PC clock at the release step; across midnight UTC and
        # local may differ by one day, never more; an earlier date is refused for every record but the baseline
        rec = {'schema': IR.RELEASE_SCHEMA, 'package': 'X', 'entries': [], 'retires': [], 'local_date': '2026-11-21',
               'released_utc': '2026-11-20T23:58:00.000000Z', 'install_record_sha256': '0' * 64}
        IR.validate_release(rec, self.root, is_baseline=False)
        rec['released_utc'] = '2026-11-21T00:02:00.000000Z'
        IR.validate_release(rec, self.root, is_baseline=False)
        rec['local_date'] = '2026-10-31'
        with self.assertRaises(IR.Refused) as cm:
            IR.validate_release(rec, self.root, is_baseline=False)
        self.assertIn('not the day it was written', str(cm.exception))
        IR.validate_release(rec, self.root, is_baseline=True)
        with mock.patch.object(IR, 'now', return_value=('2026-11-20T23:58:30.000000Z', '2026-11-21')):
            self.install()
            git(self.root, 'add', '-A')
            git(self.root, 'commit', '-q', '-m', 'p')
            rc, out = self.run_tool('release-record', '--root', str(self.root), '--package', 'TESTPKG', '--manifest', str(self.manifest))
        self.assertEqual(rc, 0, out)
        rel = json.loads((self.root / IR.RECORDS_REL / 'RELEASE_TESTPKG_V1.json').read_bytes())
        self.assertEqual((rel['released_utc'], rel['local_date']), ('2026-11-20T23:58:30.000000Z', '2026-11-21'))
        self.assertEqual(IR.released_variants(self.root)[('OZLOTTO', 'E_1', '3', 'FULL_HISTORY_RAW_COUNTS_V1')], '2026-11-21')
        # a release record dated before its install record is refused by validation (no retroactive standing)
        rel_path = self.root / IR.RECORDS_REL / 'RELEASE_TESTPKG_V1.json'
        rel['released_utc'], rel['local_date'] = '2026-11-01T00:00:00.000000Z', '2026-11-01'
        rel_path.write_bytes(IR.canonical(rel))
        with self.assertRaises(IR.Refused) as cm:
            IR.validate_records(self.root)
        self.assertIn('released before its install record', str(cm.exception))


class Statics(unittest.TestCase):

    def test_tool_is_standalone_and_read_only_on_git(self):
        text = TOOL.read_text(encoding='ascii')
        self.assertNotIn('\r', text)
        import ast
        tree = ast.parse(text)
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names |= {a.name.split('.')[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                names.add((node.module or '').split('.')[0])
        self.assertTrue(names <= {'__future__', 'argparse', 'datetime', 'hashlib', 'json', 'os', 'pathlib', 're', 'subprocess',
                                  'sys', 'process_check'}, names)
        git_calls = [ast.unparse(n) for n in ast.walk(tree) if isinstance(n, ast.Call) and ast.unparse(n.func) == 'subprocess.run']
        self.assertEqual(len(git_calls), 2)
        for call in git_calls:
            self.assertTrue("'show'" in call or "'status'" in call, call)         # read-only Git only
        for bad in ("'add'", "'commit'", "'push'", "'checkout'", "'reset'", 'shutil', 'unlink', 'rmtree'):
            self.assertNotIn(bad, text, bad)


if __name__ == '__main__':
    unittest.main()
