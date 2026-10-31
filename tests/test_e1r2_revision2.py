"""E_1 revision 2 tests (CODE-3 and E_1 revision 2 design v0.1r2, owner-ratified 31 October 2026). OFFLINE.

E1R2-T01: r2's synthetic contract records equal E_1 revision 1's frozen reference (tests/fixtures/
e1_r1_reference_v1.json, computed from the base commit outside the repository) apart from method_revision,
declaration_digest and the content digest. T02 (Powerball) and T02B (Oz Lotto): REAL_DEVELOPMENT forecasts through
the walk-forward driver on invented masters, against E_1's legacy function (Powerball) and an independent oracle
written from the specification (Oz Lotto). T03: data kinds and the development boundary. T04: the registry. T05:
the legacy runner's release gate. T06: the driver. T09: the install barrier's states (design section 5).
Every master is invented in a temporary folder; nothing under archive/ is read; no real draw is read.
"""
from __future__ import annotations

import contextlib
import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import e2r_code2_fixtures as C
import e2r_fixtures as F
from test_e6_beta_bernoulli import write_varied_master
import _common.contract_dispatch as CD
import _common.contract_runner as CR
import _common.walk_forward as WF
from _common.contract_records import record_digest
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from contract_adapters import e_001

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'tests' / 'fixtures' / 'e1_r1_reference_v1.json'
VARIANT = C.E1[1]
DIFFERS = ('method_revision', 'declaration_digest', 'canonical_content_digest')


def chain(game):
    reg = InstalledRegistry()
    return reg, reg.chain(game, *C.E1)


def pins(game, revision):
    reg, ch = chain(game)
    e = next(x for x in ch if x['method_revision'] == revision)
    return e, reg.declaration(e['declaration_digest'])


class Project(unittest.TestCase):
    """A temporary project holding invented masters for both games; the runner's root and marker point there."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.td = Path(self._td.name)
        self.proj = self.td / 'project'
        self.sha = {g.game_id: write_varied_master(self.proj, g, g.holdout_first, 0) for g in (POWERBALL, OZLOTTO)}
        self.marker = self.proj / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(mock.patch.object(CR, 'PROJECT_ROOT', self.proj))
        self.stack.enter_context(mock.patch.object(CR, 'ORPHAN_MARKER', self.marker))
        import Method_Contract_Runner as M
        self.adapters = {'E_1': M.ADAPTERS['E_1']}

    def tearDown(self):
        self.stack.close()
        self._td.cleanup()

    def batch_forecasts(self, game, first, last):
        plan = WF.make_plan(game, first, last, self.adapters)
        self.assertEqual([(m['method_id'], m['method_revision']) for m in plan['cohort']], [('E_1', '2')])
        self.assertEqual(WF.run_batch(game, plan['batch_id'], self.adapters, echo=lambda *_: None), 0)
        self.assertEqual(WF.pending(plan), [])
        out = {}
        for f in (WF.roots()['runs'] / game / 'E_1' / VARIANT).glob('*/forecast.json'):
            rec = json.loads(f.read_bytes())
            out[rec['target_draw_number']] = rec
        self.assertEqual(sorted(out), list(range(first, last + 1)))
        return out


class IdentityWithRevision1(unittest.TestCase):
    """E1R2-T01 (EX_087 C01)."""

    def test_reference_provenance(self):
        ref = json.loads(REFERENCE.read_bytes())
        self.assertEqual(ref['schema'], 'E1_R1_REFERENCE_V1')
        self.assertEqual(sorted(ref['base_r1_sources_sha256']), sorted([
            'src/methods/E_001/__init__.py', 'src/methods/E_001/e1_historical_appearance_frequency.py',
            'src/methods/E_001/multigame_e1.py', 'src/methods/contract_adapters/e_001.py']))
        self.assertEqual(len(ref['records']), 8)
        for rec in ref['records']:
            self.assertEqual((rec['method_revision'], rec['run_mode']), ('1', 'SYNTHETIC_CONTRACT_TEST'))
        # The counting and tie code did not change: those two r1 sources equal today's bytes.
        for rel in ('src/methods/E_001/__init__.py', 'src/methods/E_001/e1_historical_appearance_frequency.py'):
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                             ref['base_r1_sources_sha256'][rel], rel)

    def test_r2_equals_r1_label_for_label(self):
        ref = json.loads(REFERENCE.read_bytes())
        with tempfile.TemporaryDirectory() as td, C.installed(marker=Path(td) / 'no_marker'):
            td = Path(td)
            for r1 in ref['records']:
                game, t = r1['game_id'], r1['target_draw_number']
                e2, d2 = pins(game, '2')
                e1, d1 = pins(game, '1')
                sha = write_varied_master(td / f'{game}_{t}', get_profile(game), t, 0)
                res = CR.run_contract_method(C.request(d2, e2, t, sha, run_id='mg-' + '1' * 32), compute=e_001.compute,
                                             verify=e_001.verify, repo_root=td / f'{game}_{t}', run_root=td / f'runs_{game}_{t}')
                self.assertEqual(res.outcome, 'SUCCESS')
                r2 = json.loads((res.folder / 'forecast.json').read_bytes())
                self.assertEqual({k: v for k, v in r2.items() if k not in DIFFERS},
                                 {k: v for k, v in r1.items() if k not in DIFFERS}, (game, t))
                self.assertEqual((r1['method_revision'], r2['method_revision']), ('1', '2'))
                self.assertEqual((r1['declaration_digest'], r2['declaration_digest']),
                                 (e1['declaration_digest'], e2['declaration_digest']))
                self.assertNotEqual(r1['canonical_content_digest'], r2['canonical_content_digest'])


class RealNamespacePowerball(Project):
    """E1R2-T02 (scoped to Powerball by EX_087 C02): against E_1's legacy function on the same rows."""

    def test_driver_forecast_equals_the_legacy_function(self):
        from E_001.e1_common_reader_bridge import prepared_e1_forecast
        e2, d2 = pins('POWERBALL', '2')
        for t, rec in self.batch_forecasts('POWERBALL', 1574, 1576).items():
            self.assertEqual((rec['run_mode'], rec['method_revision'], rec['training_last_draw_number']),
                             ('REAL_DEVELOPMENT', '2', t - 1))
            _req, view, _task = F.load_view(self.proj, d2, t, 'UNORDERED_SET', self.sha['POWERBALL'])
            legacy, digest = prepared_e1_forecast(view)
            self.assertEqual(rec['permitted_view_digest'], digest)
            main, pb = rec['barrels']['MAIN'], rec['barrels']['POWERBALL']
            self.assertEqual(main['scores'], [legacy['MAIN']['scores'][str(x)] for x in range(1, 36)])
            self.assertEqual((main['ranking'], main['top']['labels'], main['worst']['labels']),
                             (legacy['MAIN']['ranking'], legacy['MAIN']['top'], legacy['MAIN']['worst']))
            self.assertEqual(pb['scores'], [legacy['POWERBALL']['scores'][str(x)] for x in range(1, 21)])
            self.assertEqual((pb['ranking'], pb['top']['labels'], pb['worst']['labels']),
                             (legacy['POWERBALL']['ranking'], [legacy['POWERBALL']['top']],
                              [legacy['POWERBALL']['worst']]))


# ---------------------------------------------------------------- T02B: an oracle written from the specification

OZ_ERA, OZ_PROFILE, OZ_LABELS, OZ_SELECTED = 'OZLOTTO_CURRENT_2022', 'OZLOTTO_PROFILE_V2_FIXED_HOLDOUT', 47, 7


def oracle_canonical(value) -> bytes:
    """The project's canonical JSON: sorted keys, no spaces, ASCII escapes, no NaN, one closing newline."""
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()


def oracle_tie(view_digest: str, target: int, label: int) -> str:
    """TIE_SHA256_V1: SHA-256 of the fields, each as a 4-byte little-endian UTF-8 length then the bytes."""
    fields = ('PREDICTIVE_RANDOMNESS/TIE_SHA256_V1', view_digest, str(target), 'E_1', VARIANT, 'MAIN',
              'TIE_SHA256_V1', str(label))
    return hashlib.sha256(b''.join(len(f.encode()).to_bytes(4, 'little') + f.encode() for f in fields)).hexdigest()


def oracle(master_csv: Path, first_draw: int, target: int) -> dict:
    rows = []
    with master_csv.open(newline='') as fh:
        for r in csv.reader(fh):
            if r[0].isdigit() and first_draw <= int(r[0]) < target:
                rows.append({'draw': int(r[0]), 'main': sorted(int(x) for x in r[2:2 + OZ_SELECTED])})
    rows.sort(key=lambda r: r['draw'])
    assert [r['draw'] for r in rows] == list(range(first_draw, target))           # exactly the draws before it
    payload = {'schema': f'OZLOTTO_{OZ_ERA}_{OZ_PROFILE}_UNORDERED_SET_VIEW_V1', 'data_kind': 'REAL_HISTORICAL_DEVELOPMENT',
               'game_id': 'OZLOTTO', 'era_id': OZ_ERA, 'profile_version': OZ_PROFILE, 'method_id': 'E_1',
               'variant_id': VARIANT, 'target': target, 'observation_view': 'UNORDERED_SET', 'includes_dates': False,
               'order_assumption': None, 'order_evidence_record': None, 'records': rows}
    digest = hashlib.sha256(oracle_canonical(payload)).hexdigest()
    counts = {n: 0 for n in range(1, OZ_LABELS + 1)}
    for r in rows:
        for n in r['main']:
            counts[n] += 1
    ranking = sorted(counts, key=lambda n: (-counts[n], oracle_tie(digest, target, n), n))
    return {'digest': digest, 'scores': [counts[n] for n in range(1, OZ_LABELS + 1)], 'ranking': ranking,
            'top': ranking[:OZ_SELECTED], 'worst': list(reversed(ranking))[:OZ_SELECTED]}


class RealNamespaceOzLotto(Project):
    """E1R2-T02B (EX_087 C02): no E_1 code and no contract ranking, tie or digest helper is used by the oracle."""

    def test_driver_forecast_equals_the_independent_oracle(self):
        master = self.proj / 'source_data' / 'OZLOTTO_results_master.csv'
        last = OZLOTTO.holdout_first - 1
        for t, rec in self.batch_forecasts('OZLOTTO', last - 2, last).items():
            want = oracle(master, OZLOTTO.first_draw, t)
            self.assertEqual((rec['game_id'], rec['era_id'], rec['profile_version'], rec['run_mode']),
                             ('OZLOTTO', OZ_ERA, OZ_PROFILE, 'REAL_DEVELOPMENT'))
            self.assertEqual((rec['target_draw_number'], rec['training_last_draw_number'], rec['draw_key']),
                             (t, t - 1, f'OZLOTTO_{t}'))
            self.assertEqual(rec['permitted_view_digest'], want['digest'])
            self.assertEqual(sorted(rec['barrels']), ['MAIN'])
            b = rec['barrels']['MAIN']
            self.assertEqual((b['label_low'], b['label_high'], b['selected_count']), (1, OZ_LABELS, OZ_SELECTED))
            self.assertEqual((b['scores'], b['ranking'], b['top']['labels'], b['worst']['labels']),
                             (want['scores'], want['ranking'], want['top'], want['worst']))
            self.assertEqual(b['probability'], {'kind': 'NONE'})                      # scores, not probabilities

    def test_the_oracle_is_sensitive(self):
        """A changed tie order or a draw too many would be caught."""
        master = self.proj / 'source_data' / 'OZLOTTO_results_master.csv'
        t = OZLOTTO.holdout_first - 1
        a, b = oracle(master, OZLOTTO.first_draw, t), oracle(master, OZLOTTO.first_draw, t - 1)
        self.assertNotEqual(a['digest'], b['digest'])
        flat = [n for n in a['ranking']]
        self.assertEqual(sorted(flat), list(range(1, OZ_LABELS + 1)))


class DataKinds(unittest.TestCase):
    """E1R2-T03."""

    def rows(self, profile, target):
        rows = []
        for d in range(profile.first_draw, target):
            row = {'draw': d, 'MAIN': list(range(1, 8))}
            if profile is POWERBALL:
                row['POWERBALL'] = [1]
            rows.append(row)
        return rows

    def test_admitted_and_refused(self):
        from E_001.multigame_e1 import forecast
        for p in (POWERBALL, OZLOTTO):
            t = p.first_draw + 3
            rows = self.rows(p, t)
            for kind in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):
                self.assertEqual(forecast(p, rows, '0' * 64, t, data_kind=kind)['data_kind'], kind)
            for kind in ('REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC', 'REAL_HISTORICAL_DEVELOPMENT',
                         'real_development', '', None):
                with self.assertRaises(ValueError, msg=(p.game_id, kind)):
                    forecast(p, rows, '0' * 64, t, data_kind=kind)
            # The development boundary: the holdout's first draw and beyond are refused, in both games.
            for t in (p.holdout_first, p.holdout_first + 1):
                with self.assertRaises(ValueError, msg=(p.game_id, t)):
                    forecast(p, self.rows(p, t), '0' * 64, t, data_kind='REAL_DEVELOPMENT')
            last = p.holdout_first - 1
            forecast(p, self.rows(p, last), '0' * 64, last, data_kind='REAL_DEVELOPMENT')


class Registry(unittest.TestCase):
    """E1R2-T04."""

    def test_chains_and_declarations(self):
        for game in ('POWERBALL', 'OZLOTTO'):
            reg, ch = chain(game)
            self.assertEqual([(e['entry_sequence'], e['method_revision'], e['registry_status']) for e in ch],
                             [(1, '1', 'SUPPORTED'), (2, '2', 'SUPPORTED')])
            self.assertEqual(ch[1]['previous_entry_digest'], record_digest(ch[0]))
            d1, d2 = (reg.declaration(e['declaration_digest']) for e in ch)
            self.assertEqual(dict(d2, method_revision='1'), d1)
            self.assertEqual(d2['method_revision'], '2')
            texts = ('method_name', 'one_liner', 'short_explanation', 'text_provenance', 'game_id', 'method_id',
                     'variant_id', 'schema')
            self.assertEqual({k: ch[1][k] for k in texts}, {k: ch[0][k] for k in texts})

    def test_a_request_pinning_revision_1_is_stale(self):
        for game in ('POWERBALL', 'OZLOTTO'):
            e1, d1 = pins(game, '1')
            e2, d2 = pins(game, '2')
            with self.assertRaises(CD.DispatchRefused) as cm:
                CD.dispatch_gate(C.request(d1, e1, 1300 if game == 'POWERBALL' else 1500, '0' * 64))
            self.assertEqual(cm.exception.reason, 'STALE_REGISTRY_ENTRY')
            entry, decl = CD.dispatch_gate(C.request(d2, e2, 1300 if game == 'POWERBALL' else 1500, '0' * 64))
            self.assertEqual((entry['method_revision'], decl['method_revision']), ('2', '2'))


class LegacyRunner(unittest.TestCase):
    """E1R2-T05: D2-3's release gate is kept; only the pinned revision changes (WF1-13)."""

    def test_gate_names_revision_2(self):
        src = (ROOT / 'src' / 'methods' / 'E_001_Historical_Appearance_Frequency.py').read_text()
        self.assertEqual(src.count('legacy_gate('), 1)
        self.assertEqual(src.count("legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '2')"), 1)
        entry, _decl = CD.legacy_gate('POWERBALL', *C.E1, '2')
        self.assertEqual((entry['method_revision'], entry['registry_status']), ('2', 'SUPPORTED'))
        with self.assertRaises(CD.DispatchRefused) as cm:
            CD.legacy_gate('POWERBALL', *C.E1, '1')
        self.assertEqual(cm.exception.reason, 'REVISION_MISMATCH')

    def test_withdrawn_revision_2_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            data = C.copy_data_root(Path(td))
            e2, d2 = pins('POWERBALL', '2')
            C.append_entry(data, dict(e2, entry_sequence=3, registry_status='FORMULA_OPEN',
                                      registry_status_reason='test harness: withdrawn',
                                      previous_entry_digest=record_digest(e2)))
            with C.installed(data=data):
                with self.assertRaises(CD.DispatchRefused) as cm:
                    CD.legacy_gate('POWERBALL', *C.E1, '2')
            self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')


class Driver(Project):
    """E1R2-T06."""

    def test_e1_is_in_the_cohort(self):
        import Method_Contract_Runner as M
        self.assertEqual(WF.NOT_REAL_CAPABLE, {})
        adapters = {m: M.ADAPTERS[m] for m in ('E_1', 'E_6')}
        plan = WF.make_plan('POWERBALL', 1576, 1576, adapters)
        self.assertEqual(plan['not_in_cohort'], [])
        self.assertEqual([(m['method_id'], m['method_revision']) for m in plan['cohort']],
                         [('E_1', '2')] + [('E_6', '1')] * 3)
        self.assertEqual(WF.run_batch('POWERBALL', plan['batch_id'], adapters, echo=lambda *_: None), 0)
        states, ignored = WF.pair_states(plan)
        self.assertEqual(ignored, 0)
        self.assertEqual(set(states.values()), {'DONE'})


# ---------------------------------------------------------------- T09: the install barrier (design section 5)

REQUESTS = ('r1 contract', 'r2 contract', 'legacy 1', 'legacy 2')
ADMIT, FLAG, STALE, REV = 'ADMIT', 'IN_DEVELOPMENT_FLAG_PRESENT', 'STALE_REGISTRY_ENTRY', 'REVISION_MISMATCH'
# Section 5's table (EX_089 C03): the gate's order is unchanged, so the reason depends on the request and the state.
TABLE = {
    'pre':       (ADMIT, STALE, ADMIT, REV),
    'barrier':   (FLAG, STALE, FLAG, REV),
    'code':      (FLAG, STALE, FLAG, REV),
    'release':   (STALE, FLAG, REV, FLAG),
    'post':      (STALE, ADMIT, REV, ADMIT),
    'rebarrier': (STALE, FLAG, REV, FLAG),     # a STOP after step 4, gate closed again by the owner (O02)
}
# What the walk-forward driver does in each state (O03): which driver code is installed, whether planning refuses.
DRIVER = {'pre': ('wf1a', False), 'barrier': ('wf1a', True), 'code': ('e1r2', True), 'release': ('e1r2', True),
          'post': ('e1r2', False), 'rebarrier': ('e1r2', True)}
WF1A_NOT_REAL_CAPABLE = {'E_1': "E_1 revision 1's multi-game function accepts synthetic contract data only"}


class InstallBarrier(Project):
    """E1R2-T09 (EX_087 B01; EX_089 C03, O02, O03), on synthetic copies of the contract data and method folders."""

    def state(self, name):
        """(data root, methods root) for one state of section 5."""
        base = self.td / name
        data = C.copy_data_root(base)
        if name in ('pre', 'barrier', 'code'):                                    # no r2 entries yet
            for g in ('POWERBALL', 'OZLOTTO'):
                (data / 'registry' / g / 'E_1' / VARIANT / 'entry_0002.json').unlink()
        if name in ('pre', 'barrier'):                                            # no r2 declarations yet
            for g in ('POWERBALL', 'OZLOTTO'):
                (data / 'declarations' / g / 'E_1' / VARIANT / 'r2.json').unlink()
        methods = base / 'methods'
        (methods / 'E_001').mkdir(parents=True)
        if name in ('barrier', 'code', 'release', 'rebarrier'):
            (methods / 'E_001' / CD.FLAG_NAME).write_text('barrier\n')
        return data, methods

    def results(self, data, methods):
        e1, d1 = pins('POWERBALL', '1')
        e2, d2 = pins('POWERBALL', '2')
        calls = (lambda: CD.dispatch_gate(C.request(d1, e1, 1300, '0' * 64)),
                 lambda: CD.dispatch_gate(C.request(d2, e2, 1300, '0' * 64)),
                 lambda: CD.legacy_gate('POWERBALL', *C.E1, '1'),
                 lambda: CD.legacy_gate('POWERBALL', *C.E1, '2'))
        out = []
        with C.installed(data=data, methods=methods):
            for call in calls:
                try:
                    call()
                    out.append(ADMIT)
                except CD.DispatchRefused as exc:
                    out.append(exc.reason)
        return tuple(out)

    def test_each_state_admits_nothing_until_step_4_and_gives_the_tabled_reason(self):
        for name, want in TABLE.items():
            got = self.results(*self.state(name))
            with self.subTest(state=name):
                # Property 1: admission. Nothing admits after steps 1, 2 or 3, or in the re-barriered state.
                admitted = [r for r, g in zip(REQUESTS, got) if g == ADMIT]
                if name in ('barrier', 'code', 'release', 'rebarrier'):
                    self.assertEqual(admitted, [])
                # Property 2: the exact refusal code, cell by cell.
                self.assertEqual(dict(zip(REQUESTS, got)), dict(zip(REQUESTS, want)))

    def test_the_driver_in_each_state(self):
        import Method_Contract_Runner as M
        adapters = {m: M.ADAPTERS[m] for m in ('E_1', 'E_6')}
        with_e1 = WF.make_plan('POWERBALL', 1575, 1575, adapters)     # the installed registry: E_1 revision 2
        self.assertEqual(with_e1['cohort'][0]['method_revision'], '2')
        without_e1 = None
        for name, (driver, refuses) in DRIVER.items():
            data, methods = self.state(name)
            nrc = WF1A_NOT_REAL_CAPABLE if driver == 'wf1a' else {}
            with self.subTest(state=name), C.installed(data=data, methods=methods), \
                    mock.patch.dict(WF.NOT_REAL_CAPABLE, nrc, clear=True):
                if not refuses:
                    plan = WF.make_plan('POWERBALL', 1576, 1576, adapters)
                    ids = [(m['method_id'], m['method_revision']) for m in plan['cohort']]
                    if name == 'pre':          # the baseline (O03): ordinary planning works, E_1 not in the cohort
                        self.assertNotIn('E_1', [i for i, _r in ids])
                        without_e1 = plan
                    else:                      # after step 4: E_1 revision 2 joins the cohort
                        self.assertEqual(ids[0], ('E_1', '2'))
                    WF.start_checks(plan, adapters)
                    continue
                with self.assertRaises(WF.BatchRefused) as cm:              # planning refuses while flagged
                    WF.make_plan('POWERBALL', 1576, 1576, adapters)
                self.assertIn('E_1', str(cm.exception))
                with self.assertRaises(WF.BatchRefused):                    # a plan including E_1 cannot start
                    WF.start_checks(with_e1, adapters)
                # An E_1-free plan is not blocked by E_1's flag (O03); the install instructions forbid running it.
                WF.start_checks(without_e1, adapters)
        self.assertIsNotNone(without_e1)


if __name__ == '__main__':
    unittest.main()
