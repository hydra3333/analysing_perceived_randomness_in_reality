"""E_2-readiness contract acceptance tests E2R-T01, T02, T04..T09, T11..T13, T16..T18 (E2R-CODE-1). OFFLINE.

Synthetic only: invented masters in temporary folders, the synthetic contract test double from
e2r_fixtures, and E_1's own accepted code for the migration check (T09). No file under source_data/
is opened, no real draw value is read, no process is started or stopped, no network is used.
T03 and T10 (prefix-only and B1 hygiene with the reader) are in test_e2r_prefix.py.
"""
from __future__ import annotations

import ast
import copy
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import multiprocessing
from pathlib import Path
import tempfile
import unittest

import e2r_fixtures as F
from e2r_fixtures import ROOT
import _common.contract_vocab as V
from _common.canonical_encoding import length32_tuple
from _common.contract_records import (
    canonical, check_json_value, content_digest, record_digest, validate_declaration,
    validate_entry_declaration_pair, validate_registry_chain, validate_registry_entry, validate_run_request,
)
from _common.contract_forecast import (
    BarrelOutput, MethodOutput, NoRanking, OrderOnlyRanking, ProbabilityVector, ScoredRanking,
    assemble_diagnostic, assemble_forecast, validate_diagnostic, validate_forecast,
)
from _common.contract_receipts import (
    consumable, score_record_key, track_id, validate_diagnostic_receipt, validate_freeze_receipt,
    validate_score_record, validate_terminal,
)
from _common.contract_registry import InstalledRegistry, revision_rollover_findings
from _common.contract_task import MethodTask, TASK_FIELDS
from _common.game_profiles import POWERBALL, OZLOTTO

CONTRACT_MODULES = ('contract_vocab', 'contract_records', 'contract_task', 'contract_forecast',
                    'contract_receipts', 'contract_registry')
COMMON = ROOT / 'src' / 'methods' / '_common'


def rebuild(rec):
    """Re-stamp the content digest after a deliberate edit, so only the planted defect is tested."""
    rec = copy.deepcopy(rec)
    rec['canonical_content_digest'] = content_digest(rec)
    return rec


class T01ShapeAndNumericContracts(unittest.TestCase):
    """E2R-T01: each rule E2R-R27..R34 passes once and fails for each planted defect."""

    @classmethod
    def setUpClass(cls):
        cls.decl, cls.req, cls.view, cls.task, cls.out, cls.c1, cls.c2 = F.one_record('POWERBALL', False, 'UNORDERED_SET')

    def bad(self, edit):
        rec = copy.deepcopy(self.c1)
        edit(rec)
        with self.assertRaises(ValueError):
            validate_forecast(rebuild(rec), self.decl)

    def test_valid_record_passes(self):
        validate_forecast(self.c1, self.decl)
        validate_diagnostic(self.c2, self.decl)

    def test_planted_defects_fail(self):
        M = lambda r: r['barrels']['MAIN']
        cases = {
            'wrong length': lambda r: M(r)['scores'].pop(),
            'duplicate label in ranking': lambda r: M(r)['ranking'].__setitem__(1, M(r)['ranking'][0]),
            'out-of-range TOP label': lambda r: M(r)['top']['labels'].__setitem__(0, 36),
            'NaN score': lambda r: M(r)['scores'].__setitem__(0, float('nan')),
            'infinite score': lambda r: M(r)['scores'].__setitem__(0, float('inf')),
            'negative zero': lambda r: M(r)['scores'].__setitem__(0, -0.0),
            'wrong probability sum': lambda r: M(r)['probability']['vector'].__setitem__(0, 0.5),
            'int beyond int64': lambda r: r.__setitem__('target_draw_number', 2 ** 63),
            'unknown field': lambda r: r.__setitem__('extra', 1),
            'unknown schema': lambda r: r.__setitem__('schema', 'METHOD_FORECAST_V2'),
            'non-partitioning ranked_groups': lambda r: M(r)['ranked_groups'][0].append(M(r)['ranked_groups'][-1][-1]),
            'scores disagree with ranked_groups': lambda r: M(r)['scores'].__setitem__(
                M(r)['ranking'][0] - 1, M(r)['scores'][M(r)['ranking'][0] - 1] + 100.0),
            'integer score where FLOAT64 declared': lambda r: M(r)['scores'].__setitem__(0, 1),
            'TOP not read from ranking': lambda r: M(r)['top']['labels'].reverse(),
            'WORST re-ranked': lambda r: M(r)['worst']['labels'].sort(),
            'missing field': lambda r: r.pop('warnings'),
            'wrong ranking digest': lambda r: M(r).__setitem__('ranking_digest', '0' * 64),
            'probability above 1': lambda r: M(r)['probability']['vector'].__setitem__(0, 1.5),
            'probability digest wrong': lambda r: M(r)['probability'].__setitem__('digest', '0' * 64),
        }
        for name, edit in cases.items():
            with self.subTest(defect=name):
                self.bad(edit)

    def test_defects_hidden_behind_restamped_digests_still_fail(self):
        """Each defect is planted and every digest re-stamped, so only the rule itself can catch it."""
        from _common.contract_records import ranking_digest
        def restamp(r):
            b = r['barrels']['MAIN']
            b['ranking_digest'] = ranking_digest(b['ranking_kind'], b.get('scores'), b['ranked_groups'],
                                                 b['ranking'], 'TIE_SHA256_V1')
            b['probability']['digest'] = record_digest(b['probability']['vector'])
            return rebuild(r)
        M = lambda r: r['barrels']['MAIN']
        cases = {
            'scores disagree with ranked_groups': lambda r: M(r)['scores'].__setitem__(
                M(r)['ranking'][-1] - 1, M(r)['scores'][M(r)['ranking'][0] - 1] + 100.0),
            'wrong probability sum': lambda r: M(r)['probability']['vector'].__setitem__(0, 0.5),
            'ranking not in tie order': lambda r: M(r).__setitem__('ranking', sorted(M(r)['ranking'][:7]) + M(r)['ranking'][7:]),
        }
        for name, edit in cases.items():
            rec = copy.deepcopy(self.c1)
            edit(rec)
            with self.subTest(defect=name), self.assertRaises(ValueError):
                validate_forecast(restamp(rec), self.decl)

    def test_content_digest_is_checked(self):
        rec = copy.deepcopy(self.c1)
        rec['warnings'] = ['changed after freezing']
        with self.assertRaises(ValueError):
            validate_forecast(rec, self.decl)

    def test_encoding_rules(self):
        for bad in (float('nan'), float('-inf'), -0.0, 2 ** 63, -(2 ** 63) - 1, (1, 2), {1: 2}, b'x'):
            with self.subTest(value=repr(bad)), self.assertRaises(ValueError):
                check_json_value({'x': bad})
        check_json_value({'x': [0.0, 2 ** 63 - 1, -(2 ** 63), 'text', None, True]})
        self.assertTrue(canonical({'b': 1, 'a': 0.1}).endswith(b'\n'))
        self.assertEqual(canonical({'b': 1, 'a': 0.1}), b'{"a":0.1,"b":1}\n')

    def test_order_only_strict_and_grouped(self):
        ch = F.channel(rk='RANKING_ORDER_ONLY', st='NONE', ot='STRICT')
        decl = F.declaration('OZLOTTO', channels={'MAIN': ch}, diagnostic=None)
        with tempfile.TemporaryDirectory() as td:
            sha, _, _ = F.write_master(Path(td), OZLOTTO, OZLOTTO.first_draw + 4, 0)
            _, v, task = F.load_view(Path(td), decl, OZLOTTO.first_draw + 4, 'UNORDERED_SET', sha)
        strict = MethodOutput({'MAIN': BarrelOutput(OrderOnlyRanking([[x] for x in range(47, 0, -1)]))})
        rec = assemble_forecast(decl, task, v, strict)
        self.assertEqual(rec['barrels']['MAIN']['ranking'], list(range(47, 0, -1)))
        grouped = MethodOutput({'MAIN': BarrelOutput(OrderOnlyRanking([list(range(1, 48))]))})
        with self.assertRaises(ValueError):
            assemble_forecast(decl, task, v, grouped)  # STRICT requires groups of one
        with self.assertRaises(ValueError):
            assemble_forecast(decl, task, v, MethodOutput({'MAIN': BarrelOutput(OrderOnlyRanking([[1], [1]]))}))


class T02ProfileSeparation(unittest.TestCase):
    """E2R-T02: Powerball and Oz Lotto declarations, records and vectors cannot be cross-validated."""

    def test_cross_game_refused(self):
        pb = F.one_record('POWERBALL')
        oz = F.one_record('OZLOTTO')
        with self.assertRaises(ValueError):
            validate_forecast(oz[5], pb[0])
        with self.assertRaises(ValueError):
            validate_forecast(pb[5], oz[0])

    def test_barrel_sizes_only_from_profile(self):
        oz = F.one_record('OZLOTTO')
        rec = copy.deepcopy(oz[5])
        rec['barrels']['POWERBALL'] = copy.deepcopy(F.one_record('POWERBALL')[5]['barrels']['POWERBALL'])
        with self.assertRaises(ValueError):
            validate_forecast(rebuild(rec), oz[0])          # an Oz record with a Powerball barrel
        rec = copy.deepcopy(oz[5])
        rec['barrels']['MAIN']['label_high'] = 35
        with self.assertRaises(ValueError):
            validate_forecast(rebuild(rec), oz[0])
        d = F.declaration('OZLOTTO')
        d['channels']['POWERBALL'] = F.channel()
        with self.assertRaises(ValueError):
            validate_declaration(d)
        d = F.declaration('POWERBALL')
        d['profile_version'] = OZLOTTO.version
        with self.assertRaises(ValueError):
            validate_declaration(d)

    def test_probability_vector_lengths(self):
        d = F.declaration('OZLOTTO')
        d['channels']['MAIN']['probability_kind'] = 'PB_CATEGORICAL'
        with self.assertRaises(ValueError):
            validate_declaration(d)  # a Powerball probability kind on an Oz main barrel


def independent_tie(identity, label):
    """Independent re-implementation of TIE_SHA256_V1 from TIE v0.2, for T04."""
    fields = [identity['domain'], identity['training_view_sha256'], str(identity['target_draw_number']),
              identity['method_id'], identity['variant_id'], identity['barrel_id'],
              identity['ranking_tie_readout_version'], str(label)]
    blob = b''.join(len(f.encode()).to_bytes(4, 'little') + f.encode() for f in fields)
    return hashlib.sha256(blob).hexdigest()


class T04TieAndWorst(unittest.TestCase):
    """E2R-T04: tie order recomputed from TIE_SHA256_V1; TOP first k, WORST the reversal (T-31);
    MAP_SET with INVERSE_FROM_MARGINALS may overlap (T-32); set-only and no-ranking channels (T-33)."""

    def test_scored_and_grouped_tie_order(self):
        for game in ('POWERBALL', 'OZLOTTO'):
            rec = F.one_record(game, False, 'UNORDERED_SET')[5]
            for bid, b in rec['barrels'].items():
                with self.subTest(game=game, barrel=bid):
                    expect = []
                    for g in b['ranked_groups']:
                        expect += sorted(g, key=lambda x: (independent_tie(b['tie_identity'], x), x))
                    self.assertEqual(b['ranking'], expect)
                    k = b['selected_count']
                    self.assertEqual(b['top']['labels'], expect[:k])
                    self.assertEqual(b['worst']['labels'], expect[::-1][:k])
                    self.assertEqual(length32_tuple(['ab']), b'\x02\x00\x00\x00ab')

    def _decl_and_view(self, channels, game='OZLOTTO'):
        produces = any(c['ranking_kind'] != 'NONE' or c['top_rule_id'] != 'TOP_UNAVAILABLE' for c in channels.values())
        decl = F.declaration(game, channels=channels, diagnostic=None if produces else 'SYNTHETIC_DIAGNOSTIC_V1')
        p = OZLOTTO if game == 'OZLOTTO' else POWERBALL
        with tempfile.TemporaryDirectory() as td:
            sha, _, _ = F.write_master(Path(td), p, p.first_draw + 4, 0)
            _, v, task = F.load_view(Path(td), decl, p.first_draw + 4, 'UNORDERED_SET', sha)
        return decl, v, task

    def test_map_set_with_inverse_from_marginals_may_overlap(self):
        decl, v, task = self._decl_and_view({'MAIN': F.channel(top='MAP_SET', worst='INVERSE_FROM_MARGINALS')})
        scores = {lab: float(lab) for lab in range(1, 48)}
        native = [1, 2, 3, 4, 5, 6, 7]  # also the inverse: overlap with WORST allowed
        rec = assemble_forecast(decl, task, v, MethodOutput({'MAIN': BarrelOutput(ScoredRanking(scores), map_set=native)}))
        b = rec['barrels']['MAIN']
        self.assertEqual(b['top']['labels'], native)
        self.assertEqual(sorted(b['worst']['labels']), native)

    def test_set_only_and_no_ranking(self):
        decl, v, task = self._decl_and_view({'MAIN': F.channel(rk='NONE', st='NONE', top='MAP_SET', worst='INVERSE_UNAVAILABLE')})
        rec = assemble_forecast(decl, task, v, MethodOutput({'MAIN': BarrelOutput(map_set=[3, 9, 12, 20, 33, 40, 47])}))
        b = rec['barrels']['MAIN']
        self.assertEqual(b['ranking_status'], 'NOT_DECLARED')
        for f in ('scores', 'ranked_groups', 'ranking', 'tie_identity', 'ranking_digest'):
            self.assertNotIn(f, b)
        self.assertEqual(b['worst']['status'], 'INVERSE_MAIN_UNAVAILABLE')
        decl2, v2, task2 = self._decl_and_view({'MAIN': F.channel(rk='NONE', st='NONE', top='TOP_UNAVAILABLE',
                                                                   worst='INVERSE_UNAVAILABLE')})
        self.assertIsNone(assemble_forecast(decl2, task2, v2, MethodOutput({})))  # nothing for this barrel

    def test_inverse_never_manufactured(self):
        decl, v, task = self._decl_and_view({'MAIN': F.channel()})
        rec = assemble_forecast(decl, task, v, MethodOutput({'MAIN': BarrelOutput(NoRanking('SYNTHETIC_NO_FIT'))}))
        self.assertIsNone(rec)  # no barrel available: no C1 record (7.4)


class T05NoPowerballOrSupplementariesInOz(unittest.TestCase):
    """E2R-T05: static and runtime checks."""

    def test_static_no_supplementary_columns(self):
        for m in CONTRACT_MODULES:
            src = (COMMON / f'{m}.py').read_text(encoding='utf-8')
            self.assertNotIn('Supp_', src, m)

    def test_runtime_oz_carries_no_powerball_or_supplementary(self):
        decl, req, v, task, out, c1, c2 = F.one_record('OZLOTTO')
        self.assertIsNone(v.powerball)
        blob = json.dumps([task.as_dict(), c1, c2, v.simple_rows()]).lower()
        self.assertNotIn('powerball', blob)
        self.assertNotIn('supp', blob)


class T06ModeFirewall(unittest.TestCase):
    """E2R-T06: every combination outside the producible table is refused."""

    def test_producible_rows_accept_and_reserved_rows_refuse(self):
        for mode in ('REAL_DEVELOPMENT', *sorted(V.SYNTHETIC_MODES)):
            for schema in (V.FORECAST, V.DIAGNOSTIC):
                with self.subTest(mode=mode, schema=schema):
                    V.producible(mode, schema)
        for mode in sorted(V.RESERVED_MODES | V.BENCHMARK_MODES):
            for schema in (V.FORECAST, V.DIAGNOSTIC, V.SCORE):
                with self.subTest(mode=mode, schema=schema), self.assertRaises(ValueError):
                    V.producible(mode, schema)

    def test_records_with_wrong_pairings_refused(self):
        decl, req, v, task, out, c1, c2 = F.one_record('POWERBALL')
        for mode, product in (('REAL_HOLDOUT', 'WF_FORECAST'), ('FINAL_NEXT_DRAW', 'WF_FORECAST'),
                              ('IN_SAMPLE_DIAGNOSTIC', 'IS_DIAGNOSTIC_ENTRY'), ('BENCHMARK_REAL', 'BENCHMARK_TIMING'),
                              ('REAL_DEVELOPMENT', 'SYNTHETIC_TEST_OUTPUT'), ('SYNTHETIC_NULL', 'WF_FORECAST'),
                              ('REAL_DEVELOPMENT', 'DIAGNOSTIC_OUTPUT')):
            with self.subTest(mode=mode, product=product):
                rec = copy.deepcopy(c1)
                rec['run_mode'], rec['product_kind'] = mode, product
                with self.assertRaises(ValueError):
                    validate_forecast(rebuild(rec), decl)
        for mode in ('REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC', 'BENCHMARK_SYNTHETIC'):
            with self.subTest(request_mode=mode), self.assertRaises(ValueError):
                validate_run_request(F.request(decl, req['target_draw_number'], 'UNORDERED_SET',
                                               run_mode=mode, product='WF_FORECAST'))

    def test_benchmarks_and_is_produce_nothing(self):
        decl, req, v, task, out, c1, c2 = F.one_record('POWERBALL')
        for mode in ('BENCHMARK_REAL', 'BENCHMARK_SYNTHETIC', 'IN_SAMPLE_DIAGNOSTIC', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW'):
            d = task.as_dict()
            d['run_mode'] = mode
            t = MethodTask(**d)
            with self.subTest(mode=mode):
                with self.assertRaises(ValueError):
                    assemble_forecast(decl, t, v, out)
                with self.assertRaises(ValueError):
                    assemble_diagnostic(decl, t, v, out)

    def test_real_development_row_accepted_on_synthetic_bytes(self):
        """The REAL_DEVELOPMENT row is exercised on an invented master: no real data is read."""
        decl, req, v, task, out, c1, c2 = F.one_record('POWERBALL')
        d = task.as_dict()
        d.update(run_mode='REAL_DEVELOPMENT', product_kind='WF_FORECAST')
        rec = assemble_forecast(decl, MethodTask(**d), v, out)
        self.assertEqual((rec['run_mode'], rec['product_kind']), ('REAL_DEVELOPMENT', 'WF_FORECAST'))


class T07NotApplicable(unittest.TestCase):
    """E2R-T07: the 11.1 table, one row at a time."""

    def view(self, decl, p):
        with tempfile.TemporaryDirectory() as td:
            sha, _, _ = F.write_master(Path(td), p, p.first_draw + 4, 0)
            return F.load_view(Path(td), decl, p.first_draw + 4, 'UNORDERED_SET', sha)[1:]

    def test_rows(self):
        # Oz ABSENT: no Powerball barrel anywhere, no zero-padding
        oz = F.one_record('OZLOTTO')[5]
        self.assertEqual(sorted(oz['barrels']), ['MAIN'])
        # order-only: no scores; scores null in the ranking digest
        pbrec = F.one_record('POWERBALL')[5]['barrels']['POWERBALL']
        self.assertNotIn('scores', pbrec)
        # probability NONE: no vector
        d = F.declaration('OZLOTTO', channels={'MAIN': F.channel()}, diagnostic=None)
        v, t = self.view(d, OZLOTTO)
        r = assemble_forecast(d, t, v, MethodOutput({'MAIN': BarrelOutput(ScoredRanking({i: 1.0 for i in range(1, 48)}))}))
        self.assertEqual(r['barrels']['MAIN']['probability'], {'kind': 'NONE'})
        with self.assertRaises(ValueError):  # a vector returned for a NONE channel is refused, not dropped
            assemble_forecast(d, t, v, MethodOutput({'MAIN': BarrelOutput(ScoredRanking({i: 1.0 for i in range(1, 48)}),
                                                                       probability=ProbabilityVector([1 / 47] * 47, 'x'))}))
        # diagnostic_schema_id null: no C2 record
        with self.assertRaises(ValueError):
            assemble_diagnostic(d, t, v, MethodOutput(diagnostic=[F.DiagnosticValue('x', 'u', 1)]))
        # diagnostic-only: no ticket, C2 only
        dd = F.declaration('OZLOTTO', channels={'MAIN': F.channel(rk='NONE', st='NONE', top='TOP_UNAVAILABLE',
                                                                  worst='INVERSE_UNAVAILABLE')})
        v2, t2 = self.view(dd, OZLOTTO)
        out = MethodOutput(diagnostic=[F.DiagnosticValue('rows', 'draws', 4)])
        self.assertIsNone(assemble_forecast(dd, t2, v2, out))
        self.assertEqual(assemble_diagnostic(dd, t2, v2, out)['product_kind'], 'DIAGNOSTIC_OUTPUT')
        # declared probability with no lawful vector is a failure, not a downgrade (E2R-R16)
        dp = F.declaration('OZLOTTO', channels={'MAIN': F.channel(pk='NORMALIZED_LABEL_PROBABILITY')}, diagnostic=None)
        v3, t3 = self.view(dp, OZLOTTO)
        with self.assertRaises(ValueError):
            assemble_forecast(dp, t3, v3, MethodOutput({'MAIN': BarrelOutput(ScoredRanking({i: 1.0 for i in range(1, 48)}))}))
        # IS_NOT_APPLICABLE etc.: no IS request is possible in stage 1
        with self.assertRaises(ValueError):
            V.producible('IN_SAMPLE_DIAGNOSTIC', V.FORECAST)
        # stochastic: never SUPPORTED, never a record
        ds = F.declaration('OZLOTTO', stochastic=True)
        validate_declaration(ds)
        v4, t4 = self.view(ds, OZLOTTO)
        with self.assertRaises(ValueError):
            assemble_forecast(ds, t4, v4, MethodOutput())

    def test_insufficient_history_records_no_numbers(self):
        d = F.declaration('OZLOTTO', minimum=10)
        v, t = self.view(d, OZLOTTO)  # 4 eligible prior draws < 10
        r = assemble_forecast(d, t, v, F.probe_method(v, t))
        self.assertEqual(r['record_status'], 'INSUFFICIENT_HISTORY')
        b = r['barrels']['MAIN']
        self.assertEqual((b['ranking_status'], b['ranking_unavailable_reason']), ('UNAVAILABLE', 'INSUFFICIENT_HISTORY'))
        self.assertNotIn('labels', b['top'])
        self.assertNotIn('vector', b['probability'])


class T08ExtensionPoints(unittest.TestCase):
    """E2R-T08: extension points are reserved, not implemented."""

    def test_static_no_reserved_engines(self):
        banned = ('seed_sequence', 'seedsequence', 'derive_seed', 'fit_in_sample', 'apply_in_sample',
                  'league_table', 'run_ensemble', 'diagnostic_adapter', 'numpy.random', 'random.')
        for m in CONTRACT_MODULES:
            src = (COMMON / f'{m}.py').read_text(encoding='utf-8').lower()
            for word in banned:
                self.assertNotIn(word, src, f'{m} contains {word}')
        from _common import contract_records
        self.assertEqual(contract_records.REVIEWED_SEED_POLICIES, frozenset())

    def test_installed_declarations_and_supported_entries(self):
        reg = InstalledRegistry()
        for dig in reg.declaration_digests():
            self.assertIsNone(reg.declaration(dig)['is_interface_version'])
        for key in reg.chain_keys():
            active = reg.active_entry(*key)
            if active['registry_status'] == 'SUPPORTED':
                d = reg.declaration(active['declaration_digest'])
                self.assertFalse(d['stochastic_fit'])
                self.assertIsNone(d['fit_seed_policy_id'])

    def test_stochastic_placeholder_and_supported_refusal(self):
        d = F.declaration('POWERBALL', stochastic=True)
        validate_declaration(d)  # typed placeholder: stochastic, null policy
        entry = F_entry(d, 'FORMULA_OPEN')
        validate_entry_declaration_pair(entry, d)
        with self.assertRaises(ValueError):
            validate_entry_declaration_pair(F_entry(d, 'SUPPORTED'), d)
        d2 = dict(d, is_interface_version='IS_V1')
        with self.assertRaises(ValueError):
            validate_declaration(d2)
        with self.assertRaises(ValueError):
            validate_declaration(dict(d, source_method_dependencies=['E_1']))


def F_entry(decl, status, seq=1, prev=None, *, variant=None):
    return {'schema': 'REGISTRY_ENTRY_V1', 'game_id': decl['game_id'], 'method_id': decl['method_id'],
            'variant_id': variant or decl['variant_id'], 'entry_sequence': seq,
            'method_revision': decl['method_revision'], 'declaration_digest': record_digest(decl),
            'registry_status': status, 'registry_status_reason': 'synthetic', 'method_name': 'Synthetic probe',
            'one_liner': 'x', 'short_explanation': 'y',
            'text_provenance': {'author': 'test', 'date': '2026-10-28', 'text_version': 'v1', 'source_reference': 'test'},
            'effective_date': '2026-10-28', 'previous_entry_digest': prev}


class T09VersioningAndMigration(unittest.TestCase):
    """E2R-T09: old schemas readable and refused for writing; unknown refused; E_1's legacy goldens
    reproduce; E_1's METHOD_FORECAST_V1 equals the legacy result label for label (E2R-R51)."""

    def test_legacy_schemas_refused_for_writing(self):
        rec = copy.deepcopy(F.one_record('POWERBALL')[5])
        for schema in sorted(V.LEGACY_READ_ONLY_SCHEMAS) + ['METHOD_FORECAST_V9']:
            r = dict(rec, schema=schema)
            with self.subTest(schema=schema), self.assertRaises(ValueError):
                validate_forecast(r, F.declaration('POWERBALL'))

    def test_legacy_goldens_reproduce(self):
        from test_e1_standalone import csv_rows, TARGET
        from E_001.e1_training_view import load_permitted_u_view, build_e1_forecast
        from E_001.e1_standalone_contract import canonical_json, sha
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'synthetic.csv'
            csv_rows(path)
            records, digest = load_permitted_u_view(path, TARGET, source_kind='SYNTHETIC_CONTRACT_TEST')
            forecast = build_e1_forecast(records, digest, TARGET, source_kind='SYNTHETIC_CONTRACT_TEST')
        self.assertEqual(digest, '3851fa46400f44a1be6fb85fee72dfc4cc93585cef81b2a394bc0d86c4b895c9')
        self.assertEqual(sha(canonical_json(forecast)), '8a7f917ac8deb9307d31100e7cd811f87897b563d907d5ab5eab911708545eb9')

    def test_e1_method_forecast_v1_equals_legacy(self):
        from E_001.multigame_e1 import forecast as e1_forecast
        reg = InstalledRegistry()
        for p in (POWERBALL, OZLOTTO):
            entry = reg.active_entry(p.game_id, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
            decl = reg.declaration(entry['declaration_digest'])
            for target in F.targets(p)[:2]:
                with self.subTest(game=p.game_id, target=target), tempfile.TemporaryDirectory() as td:
                    sha_, _, _ = F.write_master(Path(td), p, target, 0)
                    req, v, task = F.load_view(Path(td), decl, target, 'UNORDERED_SET', sha_)
                    rows = [{'draw': r['draw'], 'MAIN': r['main'],
                             **({'POWERBALL': [r['powerball']]} if 'powerball' in r else {})} for r in v.simple_rows()]
                    digest = task_digest(v, task)
                    legacy = e1_forecast(p, rows, digest, target, data_kind='SYNTHETIC_CONTRACT_TEST')
                    # test-only adapter (scope S-2): E_1's own counts become a ScoredRanking
                    out = MethodOutput({bid: BarrelOutput(ScoredRanking({int(k): c for k, c in b['scores'].items()}))
                                        for bid, b in legacy['barrels'].items()})
                    rec = assemble_forecast(decl, task, v, out)
                    for bid, b in legacy['barrels'].items():
                        nb = rec['barrels'][bid]
                        self.assertEqual(nb['scores'], [b['scores'][str(x)] for x in range(nb['label_low'], nb['label_high'] + 1)])
                        self.assertEqual(nb['ranking'], b['ranking'])
                        self.assertEqual(nb['top']['labels'], b['top'])
                        self.assertEqual(nb['worst']['labels'], b['worst'])


def task_digest(view, task):
    from _common.contract_task import permitted_view_digest
    return permitted_view_digest(view, task.run_mode)


class T11PostOutcomeRecord(unittest.TestCase):
    """E2R-T11: the score record is a type with no data path."""

    def score(self, rev='1', receipt='d' * 64, game='POWERBALL'):
        s = {'schema': 'POST_OUTCOME_SCORE_RECORD_V1', 'game_id': game, 'draw_number': 1300,
             'track_id': track_id(game, 'E_2', 'SYNTHETIC_CONTRACT_PROBE', 'TOP', 'WF'), 'mode': 'WF',
             'method_revision': rev, 'forecast_content_digest': 'c' * 64, 'freeze_receipt_digest': receipt,
             'drawn_main': [1, 2, 3, 4, 5, 6, 7], 'main_matches': 2, 'division': 0, 'evaluator_version': 'SYNTHETIC_EVAL_V1'}
        if game == 'POWERBALL':
            s.update(drawn_powerball=3, powerball_match=0)
        else:
            s.update(draw_number=1500, supplementary_matches=1)
        return s

    def test_type_validates_and_keys_never_collide(self):
        a, b = validate_score_record(self.score()), validate_score_record(self.score(rev='2', receipt='e' * 64))
        self.assertNotEqual(score_record_key(a), score_record_key(b))
        validate_score_record(self.score(game='OZLOTTO'))
        bad = self.score(game='OZLOTTO')
        bad['supplementary_matches'] = 1
        bad['main_matches'] = 7
        with self.assertRaises(ValueError):
            validate_score_record(bad)
        with self.assertRaises(ValueError):
            validate_score_record(dict(self.score(game='OZLOTTO'), drawn_powerball=1))

    def test_no_data_path_and_no_predictor_import(self):
        tree = ast.parse((COMMON / 'contract_receipts.py').read_text(encoding='utf-8'))
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | {
            n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        for word in ('open', 'read_bytes', 'read_text', 'write_bytes', 'write_text', 'rename', 'replace',
                     'unlink', 'remove', 'kill', 'terminate', 'Popen', 'system'):
            self.assertNotIn(word, names, word)
        for f in [*(ROOT / 'src' / 'methods').glob('*.py'), *(ROOT / 'src' / 'methods').glob('E_[0-9][0-9][0-9]/**/*.py')]:
            self.assertNotIn('contract_receipts', f.read_text(encoding='utf-8'), f.name)


def _determinism_job(args):
    game, dates, view = args
    rec = F.one_record(game, dates, view)
    return canonical(rec[5]), canonical(rec[6])


class T12Determinism(unittest.TestCase):
    """E2R-T12: byte-identical records across two runs and across one and six workers, within the
    synthetic offline executor (concurrent.futures, spawn). Not acceptance of the Windows coordinator."""

    def test_two_runs_and_worker_counts(self):
        jobs = [(g, d, v) for g in ('POWERBALL', 'OZLOTTO') for d in (False, True) for v in F.VIEWS]
        first = [_determinism_job(j) for j in jobs]
        second = [_determinism_job(j) for j in jobs]
        self.assertEqual(first, second)
        ctx = multiprocessing.get_context('spawn')
        with ProcessPoolExecutor(max_workers=1, mp_context=ctx) as ex:
            one = list(ex.map(_determinism_job, jobs))
        with ProcessPoolExecutor(max_workers=6, mp_context=ctx) as ex:
            six = list(ex.map(_determinism_job, jobs))
        self.assertEqual(one, first)
        self.assertEqual(six, first)


class T13RevisionRollover(unittest.TestCase):
    """E2R-T13: synthetic identities only; no path, file hash or commit enters a declaration."""

    base = {'helpers': {'H': '1', 'K': '1'},
            'methods': {'E_2': {'revision': '1', 'helpers': {'H': '1'}, 'implementation_changed': False, 'runnable': True},
                        'E_3': {'revision': '1', 'helpers': {'H': '1'}, 'implementation_changed': False, 'runnable': True},
                        'E_4': {'revision': '1', 'helpers': {'K': '1'}, 'implementation_changed': False, 'runnable': True}}}

    def successor(self, e2=('1', '1'), e3=('1', '1'), structural=False):
        s = copy.deepcopy(self.base)
        s['helpers']['H'] = '2'
        for m, (rev, h) in (('E_2', e2), ('E_3', e3)):
            s['methods'][m].update(revision=rev, helpers={'H': h})
        if structural:
            s['structural_only'] = True
        return s

    def test_changed_helper_needs_successor_revisions(self):
        with self.assertRaises(ValueError):  # unchanged dependent revision fails, whatever numbers a fixture gives
            revision_rollover_findings(self.base, self.successor(), package_id='SYNTHETIC_PKG')
        with self.assertRaises(ValueError):  # successor still naming the superseded helper
            revision_rollover_findings(self.base, self.successor(('2', '1'), ('2', '2')), package_id='SYNTHETIC_PKG')
        f = revision_rollover_findings(self.base, self.successor(('2', '2'), ('2', '2')), package_id='SYNTHETIC_PKG')
        self.assertIn('E_4: unaffected by this package; keeps revision 1', f)

    def test_structural_exception_only_for_its_own_package(self):
        revision_rollover_findings(self.base, self.successor(structural=True), package_id='NAMES-1')
        revision_rollover_findings(self.base, self.successor(structural=True), package_id='E1-ALIGN')
        with self.assertRaises(ValueError):
            revision_rollover_findings(self.base, self.successor(structural=True), package_id='E2R-CODE-1')

    def test_no_path_hash_or_commit_in_declarations(self):
        for field, value in (('source_path', 'src/methods/E_002/x.py'), ('file_sha256', 'a' * 64), ('commit', 'abc1234')):
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_declaration(dict(F.declaration('POWERBALL'), **{field: value}))


class T16ReceiptsAndTerminalRecords(unittest.TestCase):
    """E2R-T16: a freeze receipt follows a valid C1 and has no scoring field; consumption needs a valid
    SUCCESS terminal record; every simulated failure is non-consumable and touches no file."""

    @classmethod
    def setUpClass(cls):
        cls.decl, _r, _v, _t, _o, cls.c1, cls.c2 = F.one_record('POWERBALL')
        cls.rc = F.receipt_for(cls.c1)
        cls.rd = F.receipt_for(cls.c2)

    def test_receipt_validates_and_has_no_scoring_field(self):
        validate_freeze_receipt(self.rc, self.c1)
        self.assertFalse({k for k in self.rc if 'scor' in k})
        with self.assertRaises(ValueError):
            validate_freeze_receipt(dict(self.rc, scored=False), self.c1)
        with self.assertRaises(ValueError):
            validate_freeze_receipt(dict(self.rc, outcome_opened_at_freeze=True), self.c1)
        with self.assertRaises(ValueError):
            validate_freeze_receipt(dict(self.rc, evidence_tier='PROSPECTIVE'), self.c1)

    def test_consumption_rules_and_files_untouched(self):
        ok_term = F.terminal_for([self.rc, self.rd], record=self.c1)
        with tempfile.TemporaryDirectory() as td:
            files = {}
            for name, rec in (('forecast.json', self.c1), ('receipt.json', self.rc), ('terminal.json', ok_term)):
                (Path(td) / name).write_bytes(canonical(rec))
                files[name] = (Path(td) / name).read_bytes()
            cases = {
                'interrupted after the freeze receipt, before the SUCCESS terminal record': (None, True),
                'failed terminal record': (F.terminal_for([], outcome='RUNTIME_FAILURE', record=self.c1), True),
                'orphan suspected': (F.terminal_for([], outcome='ORPHAN_SUSPECTED', record=self.c1), True),
                'terminal record names other receipts': (F.terminal_for([self.rd], record=self.c1), True),
                'invalid terminal record': (dict(ok_term, outcome='MAYBE'), True),
                'group or firewall gate failed': (ok_term, False),
            }
            for name, (term, gates) in cases.items():
                with self.subTest(case=name):
                    ok, reason = consumable(self.c1, self.rc, term, gates_pass=gates, declaration=self.decl)
                    self.assertFalse(ok, reason)
            ok, reason = consumable(self.c1, self.rc, ok_term, gates_pass=True, declaration=self.decl)
            self.assertTrue(ok, reason)
            ok, _ = consumable(self.c2, self.rd, ok_term, gates_pass=True, declaration=self.decl)
            self.assertTrue(ok)
            for name, raw in files.items():  # nothing deleted, moved or rewritten
                self.assertEqual((Path(td) / name).read_bytes(), raw)

    def test_terminal_record_rules(self):
        validate_terminal(F.terminal_for([self.rc], record=self.c1))
        with self.assertRaises(ValueError):
            validate_terminal(F.terminal_for([], record=self.c1))  # SUCCESS must name receipts
        bad = F.terminal_for([], outcome='TIMEOUT', record=self.c1)
        bad['receipt_digests'] = [record_digest(self.rc)]
        with self.assertRaises(ValueError):
            validate_terminal(bad)


class T17MultiplePublications(unittest.TestCase):
    """E2R-T17 (specification-level scenario on synthetic records; the publication mechanism waits for FINAL)."""

    def test_all_publications_retained_and_none_chosen_after_outcome(self):
        decl, req, v, task, out, c1, _ = F.one_record('POWERBALL')
        d2 = dict(decl, method_revision='2')
        t2 = MethodTask(**dict(task.as_dict(), method_revision='2'))
        c1b = assemble_forecast(d2, t2, v, out)
        late = copy.deepcopy(c1b)
        late['warnings'] = ['late candidate: timeliness unverified']
        late = rebuild(late)
        validate_forecast(late, d2)
        pubs = [('official', c1), ('second revision', c1b), ('late unverified', late)]
        digests = {p[1]['canonical_content_digest'] for p in pubs}
        self.assertEqual(len(digests), 3)  # all retained, none collide
        official_before_draw = c1['canonical_content_digest']  # designation fixed before any outcome
        as_published = [p for p in pubs if p[1]['canonical_content_digest'] == official_before_draw]
        self.assertEqual(len(as_published), 1)
        self.assertEqual(len(pubs) - len(as_published), 2)  # the others are counted, never dropped


class T18SeedPolicyStages(unittest.TestCase):
    """E2R-T18 (scenarios; synthetic only; no beacon is fetched): in stage 1 no stochastic SUPPORTED entry can exist."""

    def test_no_policy_is_approved_and_nothing_falls_back(self):
        for policy in (None, 'PROVISIONAL_BEACON_POLICY_V1', 'ANY_OTHER_POLICY_V1'):
            d = F.declaration('POWERBALL', stochastic=True)
            d['fit_seed_policy_id'] = policy
            validate_declaration(d)
            validate_entry_declaration_pair(F_entry(d, 'FORMULA_OPEN'), d)
            with self.subTest(policy=policy), self.assertRaises(ValueError):
                validate_entry_declaration_pair(F_entry(d, 'SUPPORTED'), d)

    def test_a_new_root_is_a_new_declaration(self):
        d1 = dict(F.declaration('POWERBALL', stochastic=True), fit_seed_policy_id='ROOT_A_V1')
        d2 = dict(d1, fit_seed_policy_id='ROOT_B_V1', method_revision='2')
        self.assertNotEqual(record_digest(d1), record_digest(d2))
        validate_declaration(d1)
        validate_declaration(d2)


class ReviewerScopeConditions(unittest.TestCase):
    """The reviewer's E2RC-C01, C03 and O01 (EX_032), made explicit in CODE-1."""

    def test_c01_view_digest_namespaces(self):
        from _common.contract_task import permitted_view_digest
        decl, req, v, task, out, c1, c2 = F.one_record('POWERBALL', False, 'UNORDERED_SET')
        synthetic = permitted_view_digest(v, 'SYNTHETIC_CONTRACT_TEST')
        self.assertEqual(synthetic, v.e1_view_digest(data_kind='SYNTHETIC_CONTRACT_TEST'))
        self.assertEqual(c1['permitted_view_digest'], synthetic)
        real = permitted_view_digest(v, 'REAL_DEVELOPMENT')
        self.assertEqual(real, v.e1_view_digest())          # the reader's real label, unchanged
        self.assertNotEqual(real, synthetic)
        self.assertNotEqual(permitted_view_digest(v, 'SYNTHETIC_NULL'), synthetic)

    def test_c01_legacy_e1_digest_unchanged(self):
        """For legacy E_1 the contract's real-namespace digest is exactly the reader's frozen legacy digest."""
        reg = InstalledRegistry()
        decl = reg.declaration(reg.active_entry('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')['declaration_digest'])
        from _common.contract_task import permitted_view_digest
        with tempfile.TemporaryDirectory() as td:
            sha_, _, _ = F.write_master(Path(td), POWERBALL, POWERBALL.first_draw + 5, 0)
            _, v, _ = F.load_view(Path(td), decl, POWERBALL.first_draw + 5, 'UNORDERED_SET', sha_)
        import hashlib
        from _common.canonical_encoding import canonical_bytes
        legacy = hashlib.sha256(canonical_bytes({'schema': 'E1_REAL_U_TRAINING_VIEW_V1',
                                                 'data_kind': 'REAL_HISTORICAL_DEVELOPMENT',
                                                 'records': v.simple_rows()})).hexdigest()
        self.assertEqual(permitted_view_digest(v, 'REAL_DEVELOPMENT'), legacy)

    def test_c03_record_product_kinds_fixed_by_the_contract(self):
        from _common.contract_task import record_task
        decl, req, v, task, out, c1, c2 = F.one_record('POWERBALL')
        self.assertEqual((c1['product_kind'], c2['product_kind']), ('SYNTHETIC_TEST_OUTPUT', 'DIAGNOSTIC_OUTPUT'))
        self.assertEqual(record_task(task, V.DIAGNOSTIC).as_dict(), dict(task.as_dict(), product_kind='DIAGNOSTIC_OUTPUT'))
        self.assertEqual(record_task(task, V.FORECAST).as_dict(), task.as_dict())
        rec = copy.deepcopy(c2)
        rec['product_kind'] = 'SYNTHETIC_TEST_OUTPUT'            # C1's product copied into C2
        with self.assertRaises(ValueError):
            validate_diagnostic(rebuild(rec), decl)
        diag_task = MethodTask(**dict(task.as_dict(), product_kind='DIAGNOSTIC_OUTPUT'))
        with self.assertRaises(ValueError):                       # a diagnostic-only request makes no C1
            assemble_forecast(decl, diag_task, v, out)
        self.assertEqual(assemble_diagnostic(decl, diag_task, v, out), c2)

    def test_o01_placeholder_lifecycle(self):
        """A real variant gets its own chain; the NOT_YET_SPECIFIED placeholder is never promoted or edited."""
        reg = InstalledRegistry()
        placeholder = dict(reg.active_entry('POWERBALL', 'E_2', 'NOT_YET_SPECIFIED'))
        d = F.declaration('POWERBALL', variant='EXAMPLE_REAL_VARIANT')
        first = F_entry(d, 'FORMULA_OPEN')                       # the new variant's own entry 1
        validate_registry_chain([first])
        validate_entry_declaration_pair(first, d)
        promoted = dict(placeholder, entry_sequence=2, previous_entry_digest=record_digest(placeholder),
                        registry_status='SUPPORTED', method_revision='1', declaration_digest=record_digest(d))
        with self.assertRaises(ValueError):                      # the placeholder cannot become a real variant
            validate_registry_entry(promoted)
        self.assertEqual(dict(reg.active_entry('POWERBALL', 'E_2', 'NOT_YET_SPECIFIED')), placeholder)


class RegistryAndDeclarations(unittest.TestCase):
    """Installed data: E_1..E_62 registered in both games (E2R-R19); chains are append-only."""

    def test_installed_registry(self):
        reg = InstalledRegistry()
        for game in ('POWERBALL', 'OZLOTTO'):
            e1 = reg.active_entry(game, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
            self.assertEqual(e1['registry_status'], 'SUPPORTED')
            for i in range(2, 63):
                e = reg.active_entry(game, f'E_{i}', 'NOT_YET_SPECIFIED')
                self.assertEqual(e['registry_status'], 'FORMULA_OPEN')
                self.assertIsNone(e['declaration_digest'])
            e2 = reg.active_entry(game, 'E_2', 'NOT_YET_SPECIFIED')
            self.assertNotEqual(e2['one_liner'], 'Not yet specified.')  # owner decision D-3
            self.assertEqual(reg.active_entry(game, 'E_3', 'NOT_YET_SPECIFIED')['one_liner'], 'Not yet specified.')

    def test_registry_loads_from_a_crlf_checkout_and_still_refuses_noncanonical_data(self):
        import shutil
        from _common.contract_registry import DATA_ROOT
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'contract_data'
            shutil.copytree(DATA_ROOT, root)
            for f in root.rglob('*.json'):
                f.write_bytes(f.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))  # as Windows core.autocrlf would
            # Every installed chain folder still loads (124 at CODE-1; each method package adds its own).
            self.assertEqual(len(InstalledRegistry(root).chain_keys()),
                             len({p.parent for p in (root / 'registry').glob('*/*/*/entry_*.json')}))
            f = next(root.rglob('entry_0001.json'))
            f.write_bytes(json.dumps(json.loads(f.read_bytes()), indent=1).encode('ascii'))
            with self.assertRaises(ValueError):
                InstalledRegistry(root)

    def test_append_only_chain(self):
        d = F.declaration('POWERBALL')
        e1 = F_entry(d, 'FORMULA_OPEN')
        e2 = F_entry(d, 'SUPPORTED', 2, record_digest(e1))
        self.assertEqual(validate_registry_chain([e1, e2])['registry_status'], 'SUPPORTED')
        edited = dict(e1, one_liner='edited later')
        with self.assertRaises(ValueError):
            validate_registry_chain([edited, e2])
        with self.assertRaises(ValueError):
            validate_registry_chain([e1, dict(e2, entry_sequence=3)])
        with self.assertRaises(ValueError):
            validate_registry_entry(dict(e1, variant_id='NOT_YET_SPECIFIED'))  # names a declaration
        with self.assertRaises(ValueError):
            validate_entry_declaration_pair(e1, dict(d, method_revision='2'))

    def test_method_task_is_frozen_and_minimal(self):
        decl, req, v, task, out, c1, c2 = F.one_record('POWERBALL')
        self.assertEqual(MethodTask.__slots__[:-1], TASK_FIELDS)
        with self.assertRaises(AttributeError):
            task.target_draw_number = 1
        with self.assertRaises(AttributeError):
            task.extra = 1
        with self.assertRaises(ValueError):
            MethodTask(**dict(task.as_dict(), master_sha256='a' * 64))

    def test_archive_is_not_importable(self):
        """E2R-R56 static guard (no archive/ exists yet): nothing under src/ or tests/ imports from archive."""
        for f in [*(ROOT / 'src').rglob('*.py'), *(ROOT / 'tests').glob('*.py')]:
            tree = ast.parse(f.read_text(encoding='utf-8'))
            for n in ast.walk(tree):
                mods = [n.module or ''] if isinstance(n, ast.ImportFrom) else (
                    [a.name for a in n.names] if isinstance(n, ast.Import) else [])
                for m in mods:
                    self.assertFalse(m == 'archive' or m.startswith('archive.'), f'{f.name} imports {m}')


class RegistryImmutability(unittest.TestCase):
    """E2RC1-B01 (EX_034): the installed registry is immutable at every depth. Accessors return new,
    caller-owned copies; changing a copy, however deep, changes nothing installed, and a changed copy
    can never carry the installed digest."""

    @classmethod
    def setUpClass(cls):
        cls.reg = InstalledRegistry()
        cls.key = ('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')

    def test_nested_declaration_mutation_changes_nothing_installed(self):
        dig = self.reg.active_entry(*self.key)['declaration_digest']
        before = canonical(self.reg.declaration(dig))
        for name, change in {
                'channel readout rule': lambda d: d['channels']['MAIN'].__setitem__('top_rule_id', 'MAP_SET'),
                'channel removed': lambda d: d['channels'].pop('POWERBALL'),
                'observation views': lambda d: d['observation_views'].append('OPERATOR_DRAWN_ORDER'),
                'top-level field': lambda d: d.__setitem__('minimum_history_draws', 99)}.items():
            with self.subTest(change=name):
                d = self.reg.declaration(dig)
                change(d)
                self.assertNotEqual(record_digest(d), dig)            # a changed copy has its own identity
                self.assertNotIn(record_digest(d), self.reg.declaration_digests())
                with self.assertRaises(ValueError):
                    self.reg.declaration(record_digest(d))
                again = self.reg.declaration(dig)
                self.assertEqual(canonical(again), before)
                self.assertEqual(record_digest(again), dig)
                self.assertIsNot(again, d)

    def test_nested_entry_mutation_changes_nothing_installed(self):
        before = [canonical(e) for e in self.reg.chain(*self.key)]
        for name, get in {'active entry': lambda: self.reg.active_entry(*self.key),
                          'chain entry': lambda: self.reg.chain(*self.key)[0]}.items():
            with self.subTest(source=name):
                e = get()
                e['text_provenance']['author'] = 'someone else'
                e['text_provenance'].clear()
                e['registry_status'] = 'FORMULA_OPEN'
                self.assertEqual([canonical(x) for x in self.reg.chain(*self.key)], before)
                self.assertEqual(canonical(self.reg.active_entry(*self.key)), before[-1])
        a, b = self.reg.active_entry(*self.key), self.reg.active_entry(*self.key)
        self.assertIsNot(a, b)
        self.assertIsNot(a['text_provenance'], b['text_provenance'])

    def test_no_writable_state(self):
        reg = self.reg
        for attempt in (lambda: setattr(reg, 'extra', 1), lambda: setattr(reg, '_declarations', {}),
                        lambda: delattr(reg, '_chains')):
            with self.assertRaises(AttributeError):
                attempt()
        with self.assertRaises(TypeError):
            reg._declarations[next(iter(reg._declarations))] = b'{}'
        with self.assertRaises(TypeError):
            reg._chains[self.key] = ()
        self.assertFalse(hasattr(reg, '__dict__'))
        # What is stored is bytes and tuples only, all the way down, and each digest is of its bytes.
        for dig, raw in reg._declarations.items():
            self.assertIs(type(raw), bytes)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), dig)
        for chain in reg._chains.values():
            self.assertIs(type(chain), tuple)
            for dig, raw in chain:
                self.assertIs(type(raw), bytes)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), dig)


class ReceiptTimestamps(unittest.TestCase):
    """E2RC1-C01 (EX_034): frozen_at_utc is a real UTC date-time, YYYY-MM-DDTHH:MM:SS[.ffffff]Z, in
    both receipt types. It stays informational: not proof that publication preceded an outcome."""

    GOOD = ('2026-10-28T12:00:00Z', '2026-10-28T12:00:00.5Z', '2026-10-28T12:00:00.123456Z',
            '2024-02-29T23:59:59Z', '2026-01-01T00:00:00Z')
    BAD = ('2026-10-28T12:30:00+10:30Z', '2026-10-28Z', '2026-10-28T00:00:00-05:00Z',   # the reviewer's three
           '2026-10-28T12:00:00+00:00', '2026-10-28T12:00:00', '2026-10-28T12:00:00ZZ', '2026-10-28T12:00Z',
           '2026-10-28 12:00:00Z', '2026-10-28t12:00:00Z', '2026-10-28T12:00:00z', '2026-10-28T12:00:00.Z',
           '2026-10-28T12:00:00.1234567Z', '2026-02-30T12:00:00Z', '2025-02-29T12:00:00Z',
           '2026-13-01T12:00:00Z', '2026-10-28T24:00:00Z', '2026-10-28T12:60:00Z', '2026-10-28T23:59:60Z',
           '\u0662026-10-28T12:00:00Z', '2026-10-28T12:00:00Z\n', ' 2026-10-28T12:00:00Z', '', 'Z', 20261028, None)

    @classmethod
    def setUpClass(cls):
        _d, _r, _v, _t, _o, cls.c1, cls.c2 = F.one_record('POWERBALL')
        cls.rc, cls.rd = F.receipt_for(cls.c1), F.receipt_for(cls.c2)

    def check(self, validate, receipt, record):
        validate(receipt, record)
        for v in self.GOOD:
            with self.subTest(good=v):
                validate(dict(receipt, frozen_at_utc=v), record)
        for v in self.BAD:
            with self.subTest(bad=v):
                with self.assertRaises(ValueError):
                    validate(dict(receipt, frozen_at_utc=v), record)

    def test_forecast_freeze_receipt(self):
        self.check(validate_freeze_receipt, self.rc, self.c1)

    def test_diagnostic_receipt(self):
        self.check(validate_diagnostic_receipt, self.rd, self.c2)


if __name__ == '__main__':
    unittest.main()
