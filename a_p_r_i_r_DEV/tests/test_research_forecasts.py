"""Tests of the engine's forecasting code: the reader and the permitted view, the readout, one target's content.

Each test is named for the rule it proves and plants the fault that rule must catch. Three are oracles against
the old system's code, which stays in DEV: the copied view code is the old reader's; the new view equals the old
loader's on the masters in this tree (real; no draw value is printed); and the new readout equals the old
assembly for every existing variant (on invented draws).
(Specification v0.6 sections 5.3, 5.4, 6 and 18 "Records", "N-1"; build plan v0.1 section 3 items 1 and 2.)
"""
import ast
import glob
import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

import research_fixtures as fixtures
from _common import game_draws_reader as old_reader
from _common.contract_forecast import (BarrelOutput, MethodOutput, ProbabilityVector, ScoredRanking,
                                       assemble_forecast)
from _common.contract_records import tie_digest, tie_identity_for
from _common.contract_task import MethodTask
from _common.game_profiles import get_profile
import _common.contract_vocab as vocab
from research import forecast_engine, reader, readout, variant_folders

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
COPIED_NAMES = ('_DIGIT', 'VIEW_KINDS', '_REAL', '_ORDER_STATUS', '_E1_VARIANT', 'header_for', '_owned', 'DrawView',
                '_trusted_file_bytes', '_parse_prefix')


def definitions(path: Path) -> dict:
    """{name: the parsed code of each top-level definition or assignment of a Python file, as text}."""
    found = {}
    for node in ast.parse(path.read_text(encoding='utf-8')).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            found[node.name] = ast.dump(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    found[target.id] = ast.dump(node)
    return found


class CopiedReaderCode(unittest.TestCase):
    """Build plan 3.1: the view class and the prefix parser are the old reader's, unchanged."""

    def test_every_copied_definition_is_identical_to_the_old_readers(self):
        new, old = definitions(Path(reader.__file__)), definitions(Path(old_reader.__file__))
        for name in COPIED_NAMES:
            self.assertEqual(new[name], old[name], name)

    def test_the_comparison_sees_a_planted_change(self):
        text = Path(reader.__file__).read_text(encoding='utf-8').replace('high = 35 if', 'high = 36 if')
        with tempfile.TemporaryDirectory() as folder:
            changed = Path(folder) / 'reader.py'
            changed.write_text(text, encoding='utf-8')
            self.assertNotEqual(definitions(changed)['_parse_prefix'],
                                definitions(Path(old_reader.__file__))['_parse_prefix'])

    def test_the_new_reader_does_not_import_the_old_systems_gates(self):
        imported = set()
        for node in ast.walk(ast.parse(Path(reader.__file__).read_text(encoding='utf-8'))):
            if isinstance(node, ast.ImportFrom):
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
        self.assertFalse({name for name in imported if name and ('master_versions' in name or 'owner_records' in name
                                                               or 'game_draws_reader' in name)})


class ResultsOnFile(unittest.TestCase):
    """Specification 7.1: the accepted results on file are whole and are the file the ledger names."""

    def setUp(self):
        """An invented tree with invented Powerball results through draw 1200."""
        self.folder = tempfile.TemporaryDirectory()
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'dev')
        fixtures.write_results(self.tree, 'POWERBALL', 1200, version=2)
        self.master = self.tree / 'source_data' / 'POWERBALL_results_master.csv'

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def test_the_results_on_file_give_the_last_draw_the_version_and_the_hash(self):
        found = reader.results_on_file(self.tree, 'POWERBALL')
        self.assertEqual((found.first_draw, found.last_draw, found.version), (1144, 1200, 2))
        self.assertEqual(found.raw, self.master.read_bytes())

    def test_a_results_file_changed_outside_the_updater_refuses(self):
        self.master.write_bytes(fixtures.results_bytes('POWERBALL', 1200, reseed_from=1190))
        with self.assertRaisesRegex(reader.ResultsRefused, 'not the one its ledger'):
            reader.results_on_file(self.tree, 'POWERBALL')

    def test_a_missing_draw_a_blank_line_and_a_wrong_header_each_refuse(self):
        lines = self.master.read_bytes().split(b'\n')
        for damaged, message in ((lines[:20] + lines[21:], 'should be draw'), (lines[:20] + [b''] + lines[20:], 'should be draw'),
                                 ([b'Draw,Date'] + lines[1:], 'results header'), (lines[:1] + [b''], 'holds no draw')):
            self.master.write_bytes(b'\n'.join(damaged))
            with self.assertRaisesRegex(reader.ResultsRefused, message):
                reader.results_on_file(self.tree, 'POWERBALL')

    def test_a_missing_file_or_ledger_refuses(self):
        (self.tree / 'source_data' / 'POWERBALL_results_master_ledger.csv').unlink()
        with self.assertRaisesRegex(reader.ResultsRefused, 'restore them from a backup'):
            reader.results_on_file(self.tree, 'POWERBALL')

    def test_the_first_target_is_the_first_draw_with_enough_earlier_draws(self):
        self.assertEqual(reader.first_target('POWERBALL', 104), 1248)
        self.assertEqual(reader.first_target('OZLOTTO', 1), 1475)


class PermittedView(unittest.TestCase):
    """Specification 6: for target T a method receives the draws before T and nothing else (N-1)."""

    def results(self, tree_name: str, game_id: str, last_draw: int, **generator) -> reader.ResultsOnFile:
        """Invented results in a fresh invented tree."""
        tree = fixtures.make_tree(Path(self.folder.name) / tree_name)
        fixtures.write_results(tree, game_id, last_draw, **generator)
        return reader.results_on_file(tree, game_id)

    def view(self, results, target, kind='UNORDERED_SET', dates=False):
        """The permitted view of a toy identity for a target."""
        return reader.permitted_view(results, method_id='E_901', variant_id='TOY_COUNTS_V1', target=target,
                                     observation_view=kind, include_dates=dates)

    def setUp(self):
        """A temporary folder for the invented trees."""
        self.folder = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def test_the_view_holds_exactly_the_draws_before_the_target(self):
        for game_id, first in (('POWERBALL', 1144), ('OZLOTTO', 1474)):
            results = self.results(game_id.lower(), game_id, first + 60)
            view = self.view(results, first + 40)
            self.assertEqual([int(n) for n in view.draw_number], list(range(first, first + 40)))
            self.assertEqual(view.main.shape, (40, 7))
            self.assertEqual(view.powerball is None, game_id == 'OZLOTTO')

    def test_draws_at_and_after_the_target_changed_and_appended_leave_the_view_and_its_digest_unchanged(self):
        for game_id, first in (('POWERBALL', 1144), ('OZLOTTO', 1474)):
            target = first + 40
            base = self.view(self.results(f'a{game_id}', game_id, first + 60), target)
            later_changed = self.view(self.results(f'b{game_id}', game_id, first + 90, reseed_from=target), target)
            self.assertEqual(base.e1_view_digest(), later_changed.e1_view_digest())
            self.assertTrue(np.array_equal(base.main, later_changed.main))
            earlier_changed = self.view(self.results(f'c{game_id}', game_id, first + 60, reseed_from=target - 1), target)
            self.assertNotEqual(base.e1_view_digest(), earlier_changed.e1_view_digest())

    def test_a_malformed_row_after_the_target_is_never_decoded_and_one_before_it_refuses(self):
        tree = fixtures.make_tree(Path(self.folder.name) / 'dev')
        raw = fixtures.write_results(tree, 'POWERBALL', 1200)
        lines = raw.split(b'\n')
        good = reader.results_on_file(tree, 'POWERBALL')

        def with_damaged_row(draw: int) -> reader.ResultsOnFile:
            """The same results with one row's numbers replaced by letters."""
            changed = list(lines)
            changed[draw - 1144 + 1] = str(draw).encode() + b',not,a,row'
            return reader.ResultsOnFile('POWERBALL', b'\n'.join(changed), good.sha256, 1144, 1200, 1)

        self.assertEqual(self.view(with_damaged_row(1190), 1180).e1_view_digest(), self.view(good, 1180).e1_view_digest())
        with self.assertRaises(ValueError):
            self.view(with_damaged_row(1170), 1180)

    def test_a_target_outside_the_results_on_file_and_an_unknown_view_refuse(self):
        results = self.results('dev', 'POWERBALL', 1200)
        self.assertEqual(len(self.view(results, 1201).draw_number), 57)
        for target in (1144, 1202, 1100, '1180'):
            with self.assertRaisesRegex(reader.ResultsRefused, 'a target must be'):
                self.view(results, target)
        with self.assertRaisesRegex(reader.ResultsRefused, 'not an observation view'):
            self.view(results, 1180, kind='EVERYTHING')


class TheOldLoaderAgrees(unittest.TestCase):
    """Build plan 3.1 (real): on the masters in this tree the new view is the old loader's, array for array and
    digest for digest. Only digests and array equality are compared; no draw value is printed."""

    def test_the_new_view_equals_the_old_loaders_for_targets_across_both_masters(self):
        from _common import master_versions
        compared = 0
        for game_id in ('POWERBALL', 'OZLOTTO'):
            if not reader.results_paths(REPOSITORY_ROOT, game_id)[0].is_file():
                self.skipTest('this tree holds no results master (the oracle is for DEV)')
            results = reader.results_on_file(REPOSITORY_ROOT, game_id)
            version, sha = master_versions.current_pin(REPOSITORY_ROOT, game_id)
            self.assertEqual((version, sha), (results.version, results.sha256))
            cases = [('E_2', 'RECUR_MEAN_ALL_V1', 'UNORDERED_SET', False), ('E_1', 'FULL_HISTORY_RAW_COUNTS_V1', 'UNORDERED_SET', False),
                     ('E_2', 'RECUR_MEAN_ALL_V1', 'OPERATOR_DRAWN_ORDER', True), ('E_2', 'RECUR_MEAN_ALL_V1', 'PAIRED_DIAGNOSTIC', False)]
            for target in list(range(results.first_draw + 1, results.last_draw + 2, 23)) + [results.last_draw + 1]:
                for method_id, variant_id, kind, dates in cases:
                    new = reader.permitted_view(results, method_id=method_id, variant_id=variant_id, target=target,
                                                observation_view=kind, include_dates=dates)
                    old = old_reader.load_pinned_draw_view(repo_root=REPOSITORY_ROOT, run_manifest={
                        'schema': 'DEVELOPMENT_MASTER_PIN_V1_REVIEW', 'game_id': game_id, 'method_id': method_id,
                        'variant_id': variant_id, 'draw_number': target, 'view_kind': kind, 'include_dates': dates,
                        'master_file': f'{game_id}_results_master.csv', 'ledger_version': version, 'master_sha256': sha})
                    self.assertEqual(new.e1_view_digest(), old.e1_view_digest(), (game_id, target, kind))
                    for name in ('draw_number', 'main', 'powerball', 'drawn_main', 'draw_date'):
                        a, b = getattr(new, name), getattr(old, name)
                        self.assertTrue((a is None and b is None) or np.array_equal(a, b), (game_id, target, name))
                    compared += 1
        self.assertGreater(compared, 100)


class Readout(unittest.TestCase):
    """Specification 1.2 and 5.3: ranking, ties, TOP and WORST from the one frozen ranking."""

    IDENTITY = dict(view_digest='ab' * 32, target=1300, method_id='E_901', variant_id='TOY_COUNTS_V1')

    def output(self, main=None, powerball=None) -> MethodOutput:
        """A Powerball output with the given scores (by default, a different score for every number)."""
        main = {j: float(j) for j in range(1, 36)} if main is None else main
        powerball = {j: float(-j) for j in range(1, 21)} if powerball is None else powerball
        return MethodOutput(barrels={'MAIN': BarrelOutput(ranking=ScoredRanking(main)),
                                     'POWERBALL': BarrelOutput(ranking=ScoredRanking(powerball))})

    def test_higher_scores_rank_first_and_top_and_worst_are_the_two_ends_of_one_ranking(self):
        records = readout.read_out('POWERBALL', self.output(), **self.IDENTITY)
        main = records['MAIN']
        self.assertEqual(main['ranking'], list(range(35, 0, -1)))
        self.assertEqual(main['top'], main['ranking'][:7])
        self.assertEqual(main['worst'], main['ranking'][::-1][:7])
        self.assertEqual(main['scores'], [float(j) for j in range(1, 36)])
        self.assertEqual((records['POWERBALL']['top'], records['POWERBALL']['worst']), ([1], [20]))

    def test_equal_scores_are_ordered_by_the_ratified_tie_digest_not_by_number(self):
        records = readout.read_out('POWERBALL', self.output(main={j: 1.0 for j in range(1, 36)}), **self.IDENTITY)
        tie = tie_identity_for({'permitted_view_digest': self.IDENTITY['view_digest'], 'target_draw_number': 1300,
                                'method_id': 'E_901', 'variant_id': 'TOY_COUNTS_V1'}, 'MAIN', 'TIE_SHA256_V1')
        expected = sorted(range(1, 36), key=lambda label: (tie_digest(tie, label), label))
        self.assertEqual(records['MAIN']['ranking'], expected)
        self.assertNotEqual(expected, list(range(1, 36)))
        other_target = readout.read_out('POWERBALL', self.output(main={j: 1.0 for j in range(1, 36)}),
                                        **dict(self.IDENTITY, target=1301))
        self.assertNotEqual(other_target['MAIN']['ranking'], expected)

    def test_whole_number_scores_are_accepted_and_kept_as_whole_numbers(self):
        records = readout.read_out('POWERBALL', self.output(main={j: j % 5 for j in range(1, 36)}), **self.IDENTITY)
        self.assertTrue(all(type(s) is int for s in records['MAIN']['scores']))

    def test_no_barrels_means_not_enough_history(self):
        self.assertIsNone(readout.read_out('POWERBALL', MethodOutput(barrels={}), **self.IDENTITY))
        self.assertEqual(readout.method_facing_record(None), {'record_status': 'INSUFFICIENT_HISTORY', 'barrels': {}})

    def test_each_output_that_is_not_a_forecast_is_refused(self):
        full = {j: float(j) for j in range(1, 36)}
        cases = {
            'not a MethodOutput': {'MAIN': full},
            'a barrel missing': MethodOutput(barrels={'MAIN': BarrelOutput(ranking=ScoredRanking(full))}),
            'a number missing': self.output(main={j: float(j) for j in range(1, 35)}),
            'mixed types': self.output(main={**full, 3: 2}),
            'a boolean': self.output(main={**full, 3: True}),
            'not finite': self.output(main={**full, 3: math.nan}),
            'negative zero': self.output(main={**full, 3: -0.0}),
            'a joint selection': MethodOutput(barrels={
                'MAIN': BarrelOutput(ranking=ScoredRanking(full), map_set=[1, 2, 3, 4, 5, 6, 7]),
                'POWERBALL': BarrelOutput(ranking=ScoredRanking({j: 0.0 for j in range(1, 21)}))}),
            'a short probability vector': MethodOutput(barrels={
                'MAIN': BarrelOutput(ranking=ScoredRanking(full), probability=ProbabilityVector([0.2] * 34, 'x')),
                'POWERBALL': BarrelOutput(ranking=ScoredRanking({j: 0.0 for j in range(1, 21)}))}),
        }
        for name, output in cases.items():
            with self.assertRaises(readout.ReadoutRefused, msg=name):
                readout.read_out('POWERBALL', output, **self.IDENTITY)

    def test_the_record_given_to_verify_has_the_keys_the_methods_read(self):
        output = MethodOutput(barrels={
            'MAIN': BarrelOutput(ranking=ScoredRanking({j: 0.2 for j in range(1, 36)}),
                                 probability=ProbabilityVector([0.2] * 35, 'toy')),
            'POWERBALL': BarrelOutput(ranking=ScoredRanking({j: 0.05 for j in range(1, 21)}))})
        record = readout.method_facing_record(readout.read_out('POWERBALL', output, **self.IDENTITY))
        self.assertEqual(record['record_status'], 'PREDICTION_AVAILABLE')
        self.assertEqual(record['barrels']['MAIN']['probability']['vector'], [0.2] * 35)
        self.assertEqual(record['barrels']['POWERBALL']['probability'], {'kind': 'NONE'})
        self.assertEqual(set(record['barrels']['MAIN']['top']), {'labels'})
        self.assertEqual(len(record['barrels']['MAIN']['top']['labels']), 7)
        self.assertEqual(len(record['barrels']['MAIN']['worst']['labels']), 7)
        self.assertEqual((record['barrels']['MAIN']['label_low'], record['barrels']['MAIN']['label_high']), (1, 35))


class TheOldAssemblyAgrees(unittest.TestCase):
    """Build plan 3.2: for every existing variant, in both games, the new engine's scores, ranking, TOP, WORST
    and view digest are the old assembly's. Invented draws; the old declarations and assembly are DEV's."""

    def test_every_existing_variant_reads_out_as_the_old_assembly_does(self):
        methods_root = REPOSITORY_ROOT / 'src' / 'methods'
        declarations = {}
        for path in glob.glob(str(methods_root / '_common' / 'contract_data' / 'declarations' / '**' / '*.json'),
                              recursive=True):
            declaration = json.loads(Path(path).read_text(encoding='utf-8'))
            key = (declaration['game_id'], declaration['method_id'], declaration['variant_id'])
            if key not in declarations or int(declaration['method_revision']) > int(declarations[key]['method_revision']):
                declarations[key] = declaration
        variants, refused = variant_folders.find_variants(methods_root)
        self.assertEqual((len(variants), refused), (40, []))
        product = vocab.producible('REAL_DEVELOPMENT', vocab.FORECAST)[0]
        compared = 0
        with tempfile.TemporaryDirectory() as folder:
            tree = fixtures.make_tree(Path(folder) / 'dev')
            for game_id in ('POWERBALL', 'OZLOTTO'):
                fixtures.write_results(tree, game_id, get_profile(game_id).first_draw + 230)
                results = reader.results_on_file(tree, game_id)
                for variant in variants:
                    method = variant_folders.load_method(variant)
                    declaration = declarations[(game_id, variant.method_id, variant.variant)]
                    for target in (reader.first_target(game_id, variant.minimum_earlier_draws(game_id)),
                                   results.last_draw + 1):
                        content, detail = forecast_engine.compute_target(variant, method, results, target)
                        self.assertEqual((content['status'], detail), ('FORECAST', None), (variant.identity, target))
                        task = forecast_engine.make_task(variant, game_id, target)
                        old_task = MethodTask(**dict(task.as_dict(), method_revision=declaration['method_revision'],
                                                     product_kind=product))
                        view = reader.permitted_view(results, method_id=variant.method_id, variant_id=variant.variant,
                                                     target=target, observation_view='UNORDERED_SET')
                        old = assemble_forecast(declaration, old_task, view, method.compute(old_task, view))
                        self.assertEqual(content['permitted_view_digest'], old['permitted_view_digest'])
                        for barrel_id, new in content['barrels'].items():
                            was = old['barrels'][barrel_id]
                            self.assertEqual((new['scores'], new['ranking'], new['top'], new['worst']),
                                             (was['scores'], was['ranking'], was['top']['labels'], was['worst']['labels']),
                                             (game_id, variant.identity, target, barrel_id))
                        compared += 1
        self.assertEqual(compared, 160)


class OneTargetOfOneVariant(unittest.TestCase):
    """Specification 5.3, 5.4 and 6: FORECAST, the two NO_FORECAST reasons, and what is never recorded."""

    BEHAVIOUR = {'short_below': 10, 'fail_at': [1170], 'verify_fail_at': [1171], 'bad_output_at': [1172],
                 'crash_at': [1173]}

    def setUp(self):
        """An invented tree with one toy variant whose behaviour at four targets is planted."""
        self.folder = tempfile.TemporaryDirectory()
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'dev')
        fixtures.write_results(self.tree, 'POWERBALL', 1200)
        fixtures.add_toy_variant(self.tree, 'E_901', 'TOY_COUNTS_V1', behaviour=self.BEHAVIOUR)
        self.variant = variant_folders.read_variant(self.tree / 'src' / 'methods', 'E_901', 'TOY_COUNTS_V1')
        self.results = reader.results_on_file(self.tree, 'POWERBALL')
        self.path = fixtures.ImportPath(self.tree)
        self.path.__enter__()
        self.method = variant_folders.load_method(self.variant)

    def tearDown(self):
        """Forget the toy modules and remove the temporary folder."""
        self.path.__exit__()
        self.folder.cleanup()

    def content(self, target: int, results=None) -> tuple:
        """compute_target for the toy variant."""
        return forecast_engine.compute_target(self.variant, self.method, results or self.results, target)

    def test_a_forecast_holds_scores_ranking_top_and_worst_for_every_barrel_and_nothing_of_the_envelope(self):
        content, detail = self.content(1180)
        self.assertIsNone(detail)
        self.assertEqual(set(content), {'game', 'family', 'variant', 'target', 'permitted_view_digest',
                                        'configuration', 'seed', 'status', 'barrels'})
        self.assertEqual((content['game'], content['family'], content['variant'], content['target'], content['status']),
                         ('POWERBALL', 'E_901', 'TOY_COUNTS_V1', 1180, 'FORECAST'))
        self.assertEqual(content['configuration'], {'variant_fingerprint': self.variant.fingerprint})
        self.assertEqual(set(content['barrels']), {'MAIN', 'POWERBALL'})
        for barrel in content['barrels'].values():
            self.assertEqual(set(barrel), {'label_low', 'label_high', 'selected_count', 'scores', 'ranking', 'top', 'worst'})
            self.assertEqual(len(barrel['ranking']), barrel['label_high'] - barrel['label_low'] + 1)
            self.assertEqual((len(barrel['top']), len(barrel['worst'])), (barrel['selected_count'],) * 2)

    def test_a_method_declared_shortage_of_history_is_no_forecast_insufficient_history(self):
        content, detail = self.content(1150)
        self.assertEqual((content['status'], content['reason'], detail), ('NO_FORECAST', 'INSUFFICIENT_HISTORY', None))
        self.assertNotIn('barrels', content)

    def test_the_declared_failure_a_refused_output_and_a_disagreeing_verify_are_method_failed(self):
        for target, said in ((1170, 'declared a failure'), (1171, 'verify() refused'), (1172, 'readout refused')):
            content, detail = self.content(target)
            self.assertEqual((content['status'], content['reason']), ('NO_FORECAST', 'METHOD_FAILED'), target)
            self.assertIn(said, detail)

    def test_any_other_exception_is_passed_on_and_gives_no_content(self):
        with self.assertRaisesRegex(RuntimeError, 'environmental fault'):
            self.content(1173)

    def test_the_content_digest_ignores_later_draws_and_follows_earlier_ones(self):
        digest = forecast_engine.content_digest(self.content(1180)[0])
        self.assertEqual(digest, forecast_engine.content_digest(self.content(1180)[0]))
        for name, generator, same in (('later', dict(last_draw=1230, reseed_from=1180), True),
                                      ('earlier', dict(last_draw=1200, reseed_from=1179), False)):
            other = fixtures.make_tree(Path(self.folder.name) / name)
            fixtures.write_results(other, 'POWERBALL', generator.pop('last_draw'), **generator)
            changed = forecast_engine.content_digest(self.content(1180, reader.results_on_file(other, 'POWERBALL'))[0])
            self.assertEqual(changed == digest, same, name)

    def test_the_task_carries_the_identity_and_fixed_values_for_the_retired_fields(self):
        task = forecast_engine.make_task(self.variant, 'POWERBALL', 1180)
        self.assertEqual((task.method_id, task.variant_id, task.target_draw_number, task.observation_view,
                          task.include_dates), ('E_901', 'TOY_COUNTS_V1', 1180, 'UNORDERED_SET', False))
        self.assertEqual((task.method_revision, task.run_mode, task.product_kind),
                         ('NOT_USED', 'REAL_DEVELOPMENT', 'NOT_USED'))


if __name__ == '__main__':
    unittest.main()
