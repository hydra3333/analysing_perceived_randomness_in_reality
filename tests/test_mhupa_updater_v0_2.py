"""MHUP-A (design v0.1r5 sections 4.1, 4.2, 7): the results updater v0.2 is v0.1 plus exactly the permitted
differences, shown by comparing the two files' syntax trees; and its offline self-test passes.

The reference copy of v0.1 is tests/fixtures/results_master_v0_1_reference.py.txt (the file committed as
src/results_master_v0_1.py at the MHUP-A base, SHA-256 pinned below). The permitted differences (section 7):
(1) the two refusals of 4.1, before any fetch, lock or ledger write and re-checked under the updater's lock;
(2) the final-host rule of A6; (3) the first-update admission of 4.1; (4) a self-test case for each; TOOL_VERSION
"0.1" -> "0.2"; the module docstring; the file name; and the self-test fixture edits the additions need.
Every other top-level definition (the eras, the parser, the validators, the CSV codec, Store, Lock, the
transaction, init) has an identical syntax tree.

Integration (EX_146 items 1 and 5; R-019 (a), (e)): the ledger and master bytes the updater v0.2 itself emits (an INIT
as cmd_init writes it, then its UPDATE and NO_CHANGE rows from a synthetic fetcher) pass the strict version-2 rules
of master_versions and the outcome reader; the admitted first update of an opened game is read back by the Mode H
study checks. OFFLINE; invented draws only.
"""
from __future__ import annotations

import ast
import hashlib
import subprocess
import sys
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'tests' / 'fixtures' / 'results_master_v0_1_reference.py.txt'
NEW = ROOT / 'src' / 'results_master_v0_2.py'
OLD_SHA256 = '3436da9f560172606f4b9e010cd85a806b58e55597685f2ab7f65c3e17523619'

NEW_TOP_LEVEL = {'HOLDOUT_DRAWS', 'RESULTS_HOST', 'SEAL_SCHEMA', 'BATCH_ID_SCHEMA', 'ADVANCE_SCHEMA',
                 'holdout_last', '_owner_json', 'mode_h_sealed', 'study_version_advance', 'session_lock_present',
                 'freeze_state', 'check_final_url'}
CHANGED_TOP_LEVEL = {'TOOL_VERSION', 'holdout_opened', 'BrowserFetcher', 'update_game', 'cmd_update', 'self_test'}
NEW_SELF_TEST_CASES = {'seal', 't_refusal_unsealed_window', 't_refusal_session_lock', 't_first_update_admission',
                       't_final_host'}
CHANGED_SELF_TEST_FIXTURES = {'t_gate', 'opened_root', 't_update_adds'}
# the value-free paths the additions may name (design 4.1: "both read value-free markers only")
ALLOWED_PATH_LITERALS = {'results', 'real', 'holdout', 'wf_batches', 'weekly', 'source_data', 'MODE_H_BATCH_ID.json',
                         'MODE_H_SEALED.json', 'ACTIVE_SESSION.lock', 'STUDY_VERSION_ADVANCE_{}_V1.json',
                         'HOLDOUT_OPENED_{}.json'}


def name_of(node: ast.stmt) -> str | None:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return node.name
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
        return '<docstring>'
    return None


def by_name(body: list[ast.stmt]) -> dict[str, ast.stmt]:
    out = {}
    for node in body:
        n = name_of(node)
        if n is not None:
            assert n not in out, n
            out[n] = node
    return out


def dump(node: ast.AST) -> str:
    return ast.dump(node, include_attributes=False)


def subsequence_insertions(old: list[ast.stmt], new: list[ast.stmt]) -> list[ast.stmt]:
    """The statements of `new` not in `old`, when `old` (by syntax tree) is a subsequence of `new`; else fail."""
    inserted, i = [], 0
    old_dumps = [dump(s) for s in old]
    for s in new:
        if i < len(old_dumps) and dump(s) == old_dumps[i]:
            i += 1
        else:
            inserted.append(s)
    if i != len(old_dumps):
        raise AssertionError(f'an original statement was removed or changed: {ast.unparse(old[i])[:120]}')
    return inserted


def is_raise_of(node: ast.stmt, exc_name: str) -> bool:
    return (isinstance(node, ast.If) and len(node.body) == 1 and isinstance(node.body[0], ast.Raise)
            and isinstance(node.body[0].exc, ast.Call) and isinstance(node.body[0].exc.func, ast.Name)
            and node.body[0].exc.func.id == exc_name and not node.orelse)


def string_constants(node: ast.AST) -> set[str]:
    out, pieces = set(), set()
    for n in ast.walk(node):
        if isinstance(n, ast.JoinedStr):       # an f-string as one template, each expression written {}
            out.add(''.join(v.value if isinstance(v, ast.Constant) else '{}' for v in n.values))
            pieces |= {id(v) for v in n.values}
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in pieces:
            out.add(n.value)
    return out


class UpdaterV02Identity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.old_src = OLD.read_bytes()
        cls.new_src = NEW.read_bytes()
        cls.old = ast.parse(cls.old_src.decode('ascii'))
        cls.new = ast.parse(cls.new_src.decode('ascii'))
        cls.old_top = by_name(cls.old.body)
        cls.new_top = by_name(cls.new.body)

    def test_reference_is_the_base_v0_1_and_v0_1_is_gone(self):
        self.assertEqual(hashlib.sha256(self.old_src).hexdigest(), OLD_SHA256)
        self.assertFalse((ROOT / 'src' / 'results_master_v0_1.py').exists())
        self.assertEqual(sorted(p.name for p in (ROOT / 'src').glob('results_master_v0_*.py')), ['results_master_v0_2.py'])
        self.new_src.decode('ascii')
        self.assertNotIn(b'\r', self.new_src)

    def test_top_level_names(self):
        old, new = set(self.old_top), set(self.new_top)
        self.assertEqual(new - old, NEW_TOP_LEVEL)
        self.assertEqual(old - new, set())
        # the order of the original definitions is kept (the additions are inserted, nothing is moved)
        kept = [n for n in self.new_top if n in old]
        self.assertEqual(kept, list(self.old_top))

    def test_unchanged_definitions_have_identical_syntax_trees(self):
        for name, node in self.old_top.items():
            if name in CHANGED_TOP_LEVEL or name == '<docstring>':
                continue
            self.assertEqual(dump(node), dump(self.new_top[name]), name)
        # module-level statements without a name (imports, __main__ guard) are identical too
        unnamed = lambda tree: [dump(s) for s in tree.body if name_of(s) is None]
        self.assertEqual(unnamed(self.old), unnamed(self.new))

    def test_tool_version(self):
        self.assertEqual(self.old_top['TOOL_VERSION'].value.value, '0.1')
        self.assertEqual(self.new_top['TOOL_VERSION'].value.value, '0.2')

    def test_docstring_changed_and_names_the_additions(self):
        doc = self.new_top['<docstring>'].value.value
        self.assertNotEqual(doc, self.old_top['<docstring>'].value.value)
        for phrase in ('v0.2', 'MODE_H_SEALED', 'ACTIVE_SESSION.lock', 'www.lotterywest.wa.gov.au', 'FIRST_QUARANTINED_DRAW + 9',
                       'no fallback', 'results_master_v0_2.py'):
            self.assertIn(phrase, doc)
        self.assertNotIn('results_master_v0_1.py', doc)

    def test_holdout_opened_gains_only_the_freeze_field_refusal(self):
        old, new = self.old_top['holdout_opened'], self.new_top['holdout_opened']
        inserted = subsequence_insertions(old.body, new.body)
        self.assertEqual(len(inserted), 1)
        self.assertTrue(is_raise_of(inserted[0], 'Refused'))
        self.assertTrue({'freeze_version', 'freeze_master_sha256'} <= string_constants(inserted[0].test))
        self.assertIsInstance(new.body[-1], ast.Return)        # the refusal sits before the final `return True`
        self.assertEqual(dump(new.body[-1]), dump(old.body[-1]))

    def test_browser_fetcher_gains_only_the_final_host_check(self):
        old, new = self.old_top['BrowserFetcher'], self.new_top['BrowserFetcher']
        old_m, new_m = by_name(old.body), by_name(new.body)
        self.assertEqual(set(old_m), set(new_m))
        for name in old_m:
            if name != 'fetch':
                self.assertEqual(dump(old_m[name]), dump(new_m[name]), name)
        inserted = subsequence_insertions(old_m['fetch'].body, new_m['fetch'].body)
        self.assertEqual([ast.unparse(s) for s in inserted], ['check_final_url(self.driver.current_url)'])
        # placed after the block-page check and before the wait for results and the parse
        idx = next(i for i, s in enumerate(new_m['fetch'].body) if ast.unparse(s) == 'check_final_url(self.driver.current_url)')
        before, after = new_m['fetch'].body[:idx], new_m['fetch'].body[idx + 1:]
        self.assertTrue(any('self.driver.get(url)' in ast.unparse(s) for s in before))
        self.assertTrue(any('block/challenge' in ast.unparse(s) for s in before))
        self.assertTrue(all('parse_gov' not in ast.unparse(s) for s in before))
        self.assertTrue(any('parse_gov' in ast.unparse(s) for s in after))

    def test_check_final_url_is_pure_and_names_the_one_host(self):
        fn = self.new_top['check_final_url']
        text = ast.unparse(fn)
        self.assertIn('urlsplit', text)
        for bad in ('driver', 'get(', 'requests', 'urlopen', 'oz.lotterywest', 'thelott'):
            self.assertNotIn(bad, text, bad)
        self.assertEqual(self.new_top['RESULTS_HOST'].value.value, 'www.lotterywest.wa.gov.au')
        self.assertIn("'https'", text)
        self.assertEqual(self.new_top['HOLDOUT_DRAWS'].value.value, 10)

    def test_update_game_gains_only_refusals_and_the_admission(self):
        old, new = self.old_top['update_game'], self.new_top['update_game']
        inserted = subsequence_insertions(old.body, new.body)
        texts = [ast.unparse(s) for s in inserted]
        self.assertEqual(len(inserted), 3, texts)
        state, lock, admission = inserted
        self.assertEqual(ast.unparse(state), 'state = freeze_state(root, game, st.ledger_rows())')
        self.assertTrue(is_raise_of(lock, 'Refused') and 'session_lock_present' in ast.unparse(lock.test))
        self.assertTrue(is_raise_of(admission, 'Stop'))
        self.assertIn("state == 'FIRST_UPDATE'", ast.unparse(admission.test))
        self.assertIn('holdout_last(game)', ast.unparse(admission.test))
        # positions: the re-checks right after the verified master is loaded; the admission immediately before
        # `version = int(last['version']) + 1`, after the grab, overlap and numbering checks
        lines = [ast.unparse(s) for s in new.body]
        i_load = next(i for i, t in enumerate(lines) if t.startswith('master, master_bytes, last = st.load_verified_master'))
        self.assertEqual(lines[i_load + 1], ast.unparse(state))
        self.assertEqual(lines[i_load + 2], ast.unparse(lock))
        i_adm = lines.index(ast.unparse(admission))
        self.assertEqual(lines[i_adm + 1], "version = int(last['version']) + 1")
        self.assertTrue(any('grab_sha = write_new' in t for t in lines[:i_adm]))
        self.assertTrue(any('new draws not consecutive' in t for t in lines[:i_adm]))
        self.assertTrue(all('backup' not in t and 'replace_atomically' not in t and 'append_ledger' not in t
                            for t in lines[:i_adm]))

    def test_cmd_update_gains_only_the_two_refusals_before_the_lock(self):
        old, new = self.old_top['cmd_update'], self.new_top['cmd_update']
        self.assertEqual(len(old.body), len(new.body))
        changed = [(a, b) for a, b in zip(old.body, new.body) if dump(a) != dump(b)]
        self.assertEqual(len(changed), 1)
        old_for, new_for = changed[0]
        self.assertIsInstance(old_for, ast.For)
        self.assertEqual(dump(old_for.target), dump(new_for.target))
        self.assertEqual(dump(old_for.iter), dump(new_for.iter))
        inserted = subsequence_insertions(old_for.body, new_for.body)
        self.assertEqual(len(inserted), 2)
        self.assertTrue(is_raise_of(inserted[0], 'Refused') and 'session_lock_present' in ast.unparse(inserted[0].test))
        self.assertEqual(ast.unparse(inserted[1]), 'freeze_state(root, g, Store(root, g).ledger_rows())')
        # the loop still precedes the lock and the fetcher
        i_for = new.body.index(new_for)
        self.assertTrue(any(isinstance(s, ast.With) and 'Lock(root)' in ast.unparse(s) for s in new.body[i_for + 1:]))

    def test_new_readers_touch_only_value_free_paths(self):
        for name in ('_owner_json', 'mode_h_sealed', 'study_version_advance', 'session_lock_present', 'freeze_state'):
            fn = self.new_top[name]
            text = ast.unparse(fn)
            for bad in ('results_master.csv', 'grab', 'backup', 'write', 'open(', 'unlink', 'mkdir', 'fetch', 'driver'):
                self.assertNotIn(bad, text, (name, bad))
            paths = {c for c in string_constants(fn) if '/' in c or c.endswith(('.json', '.lock', '.csv'))
                     or c in ('results', 'real', 'holdout', 'wf_batches', 'weekly', 'source_data')}
            self.assertTrue(paths <= ALLOWED_PATH_LITERALS, (name, paths - ALLOWED_PATH_LITERALS))
        # the refusals are refusals: each reader's failure path raises Refused only
        for name in ('_owner_json', 'mode_h_sealed', 'study_version_advance', 'freeze_state'):
            for n in ast.walk(self.new_top[name]):
                if isinstance(n, ast.Raise) and isinstance(n.exc, ast.Call):
                    self.assertEqual(n.exc.func.id, 'Refused', name)

    def test_self_test_gains_the_four_cases_and_the_fixture_edits(self):
        old, new = self.old_top['self_test'], self.new_top['self_test']
        old_n, new_n = by_name(old.body), by_name(new.body)
        self.assertEqual(set(new_n) - set(old_n), NEW_SELF_TEST_CASES)
        self.assertEqual(set(old_n) - set(new_n), set())
        for name in old_n:
            if name in CHANGED_SELF_TEST_FIXTURES:
                continue
            self.assertEqual(dump(old_n[name]), dump(new_n[name]), name)
        # t_gate and t_update_adds: original statements kept, lines added
        for name in ('t_gate', 't_update_adds'):
            inner_old, inner_new = old_n[name].body[0].body, new_n[name].body[0].body       # inside the `with`
            subsequence_insertions(inner_old, inner_new)
        # opened_root: the one changed statement writes the record with the two freeze fields
        o, n = old_n['opened_root'].body, new_n['opened_root'].body
        self.assertEqual([dump(s) for s in o if not isinstance(s, ast.For)], [dump(s) for s in n if not isinstance(s, ast.For)])
        new_loop = next(s for s in n if isinstance(s, ast.For))
        self.assertTrue({'freeze_version', 'freeze_master_sha256'} <= string_constants(new_loop))
        # the case list: the original entries in order with the four new ones inserted before init
        old_for = next(s for s in old.body if isinstance(s, ast.For))
        new_for = next(s for s in new.body if isinstance(s, ast.For))
        old_cases = [e.elts[1].id for e in old_for.iter.elts]
        new_cases = [e.elts[1].id for e in new_for.iter.elts]
        self.assertEqual([c for c in new_cases if c in old_cases], old_cases)
        self.assertEqual(set(new_cases) - set(old_cases), NEW_SELF_TEST_CASES - {'seal'})
        self.assertEqual(new_cases[-1], 't_init')
        self.assertEqual(dump(old_for.body[0]), dump(new_for.body[0]))

    def test_the_self_test_passes_offline(self):
        r = subprocess.run([sys.executable, '-I', str(NEW), '--self-test'], capture_output=True, text=True, timeout=600)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('[SELF-TEST] 13/13 PASS', r.stdout)
        self.assertEqual(r.stderr, '')


class EmittedBytesReconciliation(unittest.TestCase):
    """What the updater writes, the strict readers accept (EX_146 B03r1 and item 5): a failure here is a STOP."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('results_master_v0_2_under_test', NEW)
        cls.up = importlib.util.module_from_spec(spec)
        sys.modules['results_master_v0_2_under_test'] = cls.up
        spec.loader.exec_module(cls.up)

    def synth(self, game, n):
        up = self.up
        era = up.ERAS[game]
        main, x = [], (n * 11) % era.main_max + 1
        while len(main) < 7:
            if x not in main:
                main.append(x)
            x = x % era.main_max + 1
        if game == 'POWERBALL':
            sec = [(n * 7) % era.secondary_max + 1]
        else:
            sec, y = [], (n * 5) % era.secondary_max + 1
            while len(sec) < 3:
                if y not in main and y not in sec:
                    sec.append(y)
                y = y % era.secondary_max + 1
        return up.Draw(game, n, up.derived_date(game, n).isoformat(), tuple(main), tuple(sec))

    def init_root(self, tmp: Path, game: str) -> Path:
        """The INIT the updater's cmd_init writes (its ledger row and record fields), on invented draws."""
        up = self.up
        root = tmp / 'root'
        st = up.Store(root, game)
        st.dir.mkdir(parents=True)
        draws = [self.synth(game, n) for n in range(up.ERAS[game].first_draw, up.FIRST_QUARANTINED_DRAW[game])]
        data = up.to_csv_bytes(game, draws)
        h = up.write_new(st.master, data)
        record = {'schema': 'RESULTS_MASTER_INIT_VERIFICATION_V1', 'game': game, 'tool_version': up.TOOL_VERSION,
                  'tool_sha256': up.tool_sha(), 'utc': '2026-10-24T00:00:00+00:00', 'master_file': st.master.name,
                  'master_sha256': h, 'first_draw': draws[0].number, 'last_draw': draws[-1].number,
                  'draw_count': len(draws), 'source': 'LOTTERYWEST_GOV_RESULTS_SEARCH',
                  'quarantine': {'start_date': up.QUARANTINE_START_DATE.isoformat(),
                                 'first_quarantined_draw': up.FIRST_QUARANTINED_DRAW[game]},
                  'build': {'run': 'invented'}, 'warnings': 0}
        up.write_new(st.init_record, (json.dumps(record, indent=1, sort_keys=True) + '\n').encode('ascii'))
        st.append_ledger({'version': 1, 'utc': record['utc'], 'action': 'INIT', 'master_sha256': h,
                          'first_draw': draws[0].number, 'last_draw': draws[-1].number, 'draw_count': len(draws),
                          'added_count': len(draws), 'added_first': draws[0].number, 'added_last': draws[-1].number,
                          'tool_version': up.TOOL_VERSION, 'tool_sha256': up.tool_sha(),
                          'note': f'from invented; verified (see {st.init_record.name})'})
        return root

    def fetcher(self):
        test = self

        class Fetcher:
            def fetch(self, game, a, b, *, quarantine_closed):
                n = test.up.ERAS[game].first_draw
                out = []
                while test.up.derived_date(game, n) <= b:
                    if a <= test.up.derived_date(game, n) and (not quarantine_closed or n < test.up.FIRST_QUARANTINED_DRAW[game]):
                        out.append(test.synth(game, n))
                    n += 1
                return out
        return Fetcher()

    def update(self, root, game, today, months_back=5):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.up.cmd_update(root, [game], months_back, 'chrome', 2.0, fetcher_factory=self.fetcher, today=today)

    def test_emitted_ledger_and_master_pass_the_version_2_rules(self):
        import _common.master_versions as MV
        import _common.owner_records as OR
        from _common.game_profiles import get_profile
        from evaluation import outcome_reader as OREAD
        for game in ('POWERBALL', 'OZLOTTO'):
            with self.subTest(game=game), tempfile.TemporaryDirectory() as td:
                up, p = self.up, get_profile(game)
                root = self.init_root(Path(td), game)
                raw1, rows, ev = MV.load_verified_source(root, game)                  # the INIT as the updater writes it
                self.assertEqual([(r.version, r.action, r.last_draw) for r in rows], [(1, 'INIT', p.holdout_first - 1)])
                self.assertEqual(MV.current_pin(root, game), (1, rows[0].master_sha256))
                # the opening record (as Method_Mode_H writes it) names v_f; the updater reads it with its own checks
                OR.write_record(OR.opening_record_path(root, game),
                                {'schema': OR.OPENING_SCHEMA, 'game': game, 'study_manifest_sha256': 'a' * 64,
                                 'opened_utc': '2026-11-20T10:00:00Z', 'owner_statement': OR.OPENING_STATEMENT,
                                 'freeze_version': 1, 'freeze_master_sha256': rows[0].master_sha256})
                self.assertTrue(up.holdout_opened(root, game))
                self.assertEqual(up.freeze_state(root, game, up.Store(root, game).ledger_rows()), 'FIRST_UPDATE')
                # the admitted first update: through holdout_last and beyond, in one UPDATE row
                self.assertEqual(self.update(root, game, up.derived_date(game, p.holdout_last + 3)), 0)
                raw2, rows, ev = MV.load_verified_source(root, game)
                self.assertEqual([(r.version, r.action) for r in rows], [(1, 'INIT'), (2, 'UPDATE')])
                self.assertEqual(rows[1].last_draw, p.holdout_last + 3)
                raw_rows = up.Store(root, game).ledger_rows()                         # the updater's own reading
                self.assertEqual((int(raw_rows[1]['added_first']), raw_rows[1]['tool_version']), (p.holdout_first, '0.2'))
                self.assertEqual(raw_rows[1]['backup_sha256'], rows[0].master_sha256)
                self.assertTrue(raw2.startswith(raw1))                                 # the prefix rule, on real bytes
                self.assertEqual(MV.current_pin(root, game), (2, rows[1].master_sha256))
                # the admitted version is what the Mode H study checks compute (design 4.1): v_a = v_f + 1
                opening = OR.validate_opening_record(json.loads(OR.opening_record_path(root, game).read_bytes()), game)
                self.assertEqual(OR.admitted_version(opening, None, rows), 2)
                # the window is now closed for the updater until the seal (a NO_CHANGE is refused, nothing appended)
                ledger_bytes = up.Store(root, game).ledger.read_bytes()
                with self.assertRaises(up.Refused):
                    self.update(root, game, up.derived_date(game, p.holdout_last + 3))
                self.assertEqual(up.Store(root, game).ledger.read_bytes(), ledger_bytes)
                # the outcome reader serves a development target from the pinned version-2 prefix, and refuses a
                # holdout target without the freeze-before-outcome records (as the development reader must)
                out = OREAD.read_outcomes(repo_root=root, game_id=game, master_sha256=rows[1].master_sha256,
                                          targets=[p.holdout_first - 1], ledger_version=2)
                self.assertEqual(set(out), {p.holdout_first - 1})
                with self.assertRaises(OREAD.OutcomeRefused):
                    OREAD.read_outcomes(repo_root=root, game_id=game, master_sha256=rows[1].master_sha256,
                                        targets=[p.holdout_first], ledger_version=2)
                # the closed game (no opening record): the quarantine refusal stands as in v0.1
                (root / 'source_data' / f'HOLDOUT_OPENED_{game}.json').unlink()
                with self.assertRaises(up.Refused):
                    self.update(root, game, date(2026, 12, 1))

    def test_emitted_no_change_row_after_the_seal_passes_too(self):
        import _common.master_versions as MV
        from _common.game_profiles import get_profile
        game, up, p = 'POWERBALL', self.up, get_profile('POWERBALL')
        with tempfile.TemporaryDirectory() as td:
            root = self.init_root(Path(td), game)
            rows = MV.load_verified_source(root, game)[1]
            (root / 'source_data' / f'HOLDOUT_OPENED_{game}.json').write_text(json.dumps(
                {'schema': 'HOLDOUT_OPENED_V1', 'game': game, 'study_manifest_sha256': 'a' * 64, 'opened_utc': 'x',
                 'owner_statement': 'opened', 'freeze_version': 1, 'freeze_master_sha256': rows[0].master_sha256}))
            self.assertEqual(self.update(root, game, up.derived_date(game, p.holdout_last + 1)), 0)
            # plant the seal as Method_Mode_H leaves it
            hold = root / 'results' / 'real' / 'holdout'
            bid = 'wf-' + '1' * 32
            (hold / game).mkdir(parents=True)
            (hold / game / 'MODE_H_BATCH_ID.json').write_text(json.dumps({'schema': up.BATCH_ID_SCHEMA, 'game_id': game, 'batch_id': bid}))
            (hold / 'wf_batches' / game / bid).mkdir(parents=True)
            (hold / 'wf_batches' / game / bid / 'MODE_H_SEALED.json').write_text(json.dumps({'schema': up.SEAL_SCHEMA, 'batch_id': bid}))
            import time
            time.sleep(1.1)
            self.assertEqual(self.update(root, game, up.derived_date(game, p.holdout_last + 1)), 0)        # NO_CHANGE
            time.sleep(1.1)
            self.assertEqual(self.update(root, game, up.derived_date(game, p.holdout_last + 4)), 0)        # UPDATE
            rows = MV.load_verified_source(root, game)[1]
            self.assertEqual([(r.version, r.action, r.last_draw) for r in rows],
                             [(1, 'INIT', 1576), (2, 'UPDATE', 1587), (3, 'NO_CHANGE', 1587), (4, 'UPDATE', 1590)])
            self.assertEqual(rows[2].master_sha256, rows[1].master_sha256)
            self.assertEqual(MV.current_pin(root, game), (4, rows[3].master_sha256))


if __name__ == '__main__':
    unittest.main()
