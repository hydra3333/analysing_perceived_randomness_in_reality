"""Tests of the research job: one command that reads the files, makes again what is out of date, catches up and
makes the reports, the same in every tree.

Each test is named for the rule it proves and plants the fault or the change that rule is about. Everything runs
on invented draws and toy methods (tests/research_fixtures.py).
(The simple scheme v0.2, exchange/Claude_The_Simple_Scheme_v0_2_20261126.md, sections 4 and 5.)
"""
import ast
import contextlib
import csv
import io
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

import research_command
import research_fixtures as fx
from research import code_identity, method_flags, reports, research_job, tree_lock

GAME = fx.GAME
TREE_OF_THIS_FILE = Path(__file__).resolve().parents[1]
LAST_AT_START, LAST_AFTER_NEW = fx.LAST_AT_START, fx.LAST_AFTER_NEW
# Words the engine's own files must never hold: it starts no program and opens no connection.
FORBIDDEN_IMPORTS = ('subprocess', 'socket', 'urllib', 'http', 'requests', 'ftplib', 'smtplib', 'multiprocessing')
FORBIDDEN_CALLS = ('system', 'popen', 'startfile', 'spawnl', 'spawnv', 'execl', 'execv', 'kill')


class Killed(BaseException):
    """A planted crash: not an Exception, so that nothing in the job catches it, as nothing catches a kill."""


def contents(tree: Path, variant: str, which: str = 'forecasts', family: str = 'E_901') -> list:
    """The scientific content of every line of one of a method's lists."""
    return [line['content'] for line in fx.list_lines(tree, family, variant, which)]


def list_path(tree: Path, variant: str, which: str = 'forecasts', family: str = 'E_901') -> Path:
    """One of a method's two list files."""
    return tree / 'results/research' / GAME / 'variants' / family / variant / f'{which}.jsonl'


def job_log(tree: Path) -> list:
    """The lines of a tree's job log, as records."""
    path = tree / research_job.JOB_LOG
    return [json.loads(line) for line in path.read_text(encoding='ascii').splitlines()]


class Records(fx.JobCase):
    """What a method's lists hold, and what happens when a calculation fails."""

    def test_a_method_failure_is_a_line_of_its_own_and_the_job_goes_on(self):
        tree = self.tree(variants=(('TOY_A_V1', {'fail_at': [1150], 'verify_fail_at': [1152]}),))
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        lines = {line['content']['target']: line for line in fx.list_lines(tree, 'E_901', 'TOY_A_V1')}
        scored = {content['target'] for content in contents(tree, 'TOY_A_V1', 'scores')}
        self.assertEqual([lines[t]['content']['status'] for t in (1149, 1150, 1151, 1152)],
                         ['FORECAST', 'NO_FORECAST', 'FORECAST', 'NO_FORECAST'])
        self.assertEqual(lines[1150]['content']['reason'], 'METHOD_FAILED')
        self.assertIn('compute() declared a failure', lines[1150]['envelope']['detail'])
        self.assertIn('verify() refused', lines[1152]['envelope']['detail'])
        self.assertEqual(scored, set(range(fx.FIRST_TOY_TARGET, LAST_AT_START + 1)) - {1150, 1152})

    def test_the_first_target_is_fixed_by_the_minimum_history_and_too_little_history_is_a_typed_line(self):
        tree = self.tree(variants=(('TOY_A_V1', {'short_below': 6}),))
        fx.run_job(tree)
        lines = contents(tree, 'TOY_A_V1')
        self.assertEqual(lines[0]['target'], fx.FIRST_TOY_TARGET)
        self.assertEqual([(content['status'], content.get('reason')) for content in lines[:4]],
                         [('NO_FORECAST', 'INSUFFICIENT_HISTORY')] * 3 + [('FORECAST', None)])

    def test_a_calculation_that_raises_writes_no_line_is_reported_and_the_other_methods_go_on(self):
        tree = self.tree(variants=(('TOY_A_V1', {'crash_at': [1152]}), 'TOY_B_V1'))
        code, said = fx.run_job(tree)
        self.assertEqual(code, 1, 'a job in which a method failed does not end as a clean one')
        self.assertTrue(any('E_901/TOY_A_V1: its forecast for draw 1152 failed and no line was written' in line
                            and 'an environmental fault' in line for line in said), said)
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], 1151, 'never recorded as a result')
        self.assertEqual(contents(tree, 'TOY_B_V1')[-1]['target'], LAST_AT_START + 1, 'the other method is whole')
        self.assertIn('finished with 1 methods failed', said[-4] + said[-3] + said[-2])
        self.assertIn('its forecast for draw 1152 failed', job_log(tree)[-1]['failed'][0])
        # The fault goes away (here: the method is corrected, so its results are made again); the next job is clean.
        method = fx.method_folder(tree, 'E_901', 'TOY_A_V1') / 'method.py'
        method.write_text(method.read_text(encoding='ascii').replace("'crash_at': [1152]", "'crash_at': []"),
                          encoding='ascii')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], LAST_AT_START + 1)

    def test_a_list_that_cannot_be_used_is_made_again_and_nothing_is_refused(self):
        tree = self.tree()
        fx.run_job(tree)
        whole = fx.files_under(tree)
        path = list_path(tree, 'TOY_A_V1', 'scores')
        lines = path.read_bytes().split(b'\r\n')
        for planted in (b'\r\n'.join(lines[:3] + lines[4:]),                # one score line taken out
                        b'\r\n'.join(lines[:2] + [b'not a record'] + lines[3:])):
            path.write_bytes(planted)
            code, said = fx.run_job(tree)
            self.assertEqual(code, 0, said)
            self.assertTrue(any(line.startswith(f'REBUILD: {GAME}: E_901/TOY_A_V1:') for line in said), said)
            self.assertFalse(any(line.startswith(f'REBUILD: {GAME}: E_901/TOY_B_V1') for line in said), said)
            self.assertEqual(fx.files_under(tree), whole)
        path.write_bytes(b'')                                               # an empty file is simply begun again
        code, said = fx.run_job(tree)
        self.assertTrue(any('0 forecasts, 14 scores' in line for line in said), said)
        self.assertEqual(fx.files_under(tree), whole)
        list_path(tree, 'TOY_A_V1').unlink()                                # scores without their forecasts
        code, said = fx.run_job(tree)
        self.assertTrue(any('a score list without its forecast list' in line for line in said), said)
        self.assertEqual(fx.files_under(tree), whole)

    def test_a_torn_last_line_in_each_list_is_cut_and_redone(self):
        tree = self.tree()
        fx.run_job(tree)
        whole = fx.files_under(tree)
        stored = [name for name in whole if '/variants/' in name]
        self.assertEqual(len(stored), 4, stored)
        for name in stored:
            (tree / name).write_bytes(whole[name][:-40])                    # a crash while the last line was written
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertFalse(any(line.startswith('REBUILD') for line in said), said)
        self.assertEqual(fx.files_under(tree), whole)

    def test_every_record_is_a_plain_line_with_no_link_to_the_line_before(self):
        tree = self.tree()
        fx.run_job(tree)
        for name, data in fx.files_under(tree).items():
            if name.endswith('.jsonl'):
                for line in data.decode('ascii').splitlines():
                    self.assertNotIn('prev', json.loads(line), name)
        target, score = fx.list_lines(tree, 'E_901', 'TOY_A_V1')[0], fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores')[0]
        self.assertEqual(sorted(target['envelope']), ['computed_in', 'results_sha256', 'results_version',
                                                      'target_result_on_file', 'time'])
        self.assertEqual(sorted(score['envelope']), ['computed_in', 'results_sha256', 'results_version', 'time'])
        header = json.loads(list_path(tree, 'TOY_A_V1').read_text(encoding='ascii').splitlines()[0])
        self.assertEqual(header['variant_fingerprint'], method_flags.read_flag(
            fx.method_folder(tree, 'E_901', 'TOY_A_V1') / method_flags.IN_PLACE_NAME)['fingerprint'])


class CrashResume(fx.JobCase):
    """What to do next is read from the files, never remembered."""

    def test_a_crash_between_any_two_writes_then_the_job_again_gives_the_bytes_of_an_uninterrupted_run(self):
        tree = self.tree(variants=('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5, 'fail_at': [1163]})))
        fx.run_job(tree)                                                # in place since 1160 for all three
        fx.write_results(tree, GAME, LAST_AT_START + 3, version=2)      # three draws now wait to be caught up
        pristine = self.root / 'pristine'
        shutil.copytree(tree, pristine)
        labels = []
        code, said = fx.run_job(tree, checkpoint=labels.append)
        self.assertEqual(code, 0, said)
        reference = {**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'src/methods')}
        self.assertEqual(sorted(set(labels)), ['forecast line written', 'score line written'])
        self.assertEqual(len(fx.ledger_lines(tree)), 3)
        for crash_after in range(1, len(labels) + 1):
            shutil.rmtree(tree)
            shutil.copytree(pristine, tree)
            seen = []

            def checkpoint(label, seen=seen, crash_after=crash_after):
                """Count the writes and die after the chosen one."""
                seen.append(label)
                if len(seen) == crash_after:
                    raise Killed(label)

            with self.assertRaises(Killed):
                fx.run_job(tree, checkpoint=checkpoint)
            code, said = fx.run_job(tree)
            self.assertEqual(code, 0, (crash_after, labels[crash_after - 1], said))
            again = {**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'src/methods')}
            self.assertEqual(sorted(again), sorted(reference), (crash_after, labels[crash_after - 1]))
            for name in reference:
                self.assertEqual(again[name], reference[name], (crash_after, labels[crash_after - 1], name))


class WhatIsOutOfDateIsMadeAgain(fx.JobCase):
    """Scheme section 5 step 4: a difference never refuses; it means "make that part again"."""

    def test_a_second_job_with_nothing_changed_writes_nothing(self):
        tree = self.tree()
        fx.run_job(tree)
        before = {**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'src')}
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('0 forecasts, 0 scores, 0 series files, 0 report files' in line for line in said), said)
        self.assertEqual({**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'src')}, before)

    def test_a_changed_engine_file_rebuilds_everything_and_keeps_the_establishment_draws(self):
        tree = self.tree()
        fx.run_job(tree)
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        fx.run_job(tree)
        whole = fx.files_under(tree)
        stored = code_identity.stored_fingerprint(tree)
        (tree / 'src' / fx.ENGINE_FILE).write_text('# the engine, changed\n', encoding='ascii')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertTrue(any(line.startswith('REBUILD: everything, in both games (2 stored method results deleted): '
                                            'the engine is not the one these results were made with')
                            for line in said), said)
        self.assertNotEqual(code_identity.stored_fingerprint(tree), stored)
        self.assertEqual(code_identity.stored_fingerprint(tree), code_identity.infrastructure_fingerprint(tree))
        again = fx.files_under(tree)
        for name in whole:
            if '/variants/' in name:                                     # the same science; the lines made anew
                kind = 'scores' if name.endswith('scores.jsonl') else 'forecasts'
                self.assertEqual([json.loads(line).get('content') for line in again[name].splitlines()],
                                 [json.loads(line).get('content') for line in whole[name].splitlines()], (name, kind))
        self.assertEqual(self.status(tree, 'TOY_A_V1').eligible_from, LAST_AT_START + 1,
                         'the method\'s own code did not change: its establishment draw stays')
        earlier = [json.loads(line) for line in whole[f'results/research/{GAME}/ov1/prevailing.jsonl'].splitlines()[1:]]
        self.assertEqual([line['content'] for line in fx.ledger_lines(tree)], [line['content'] for line in earlier])
        self.assertEqual((earlier[0]['audit']['counted_before_result'], earlier[0]['audit']['counted_after_result']),
                         (2, 0))
        self.assertEqual(fx.ledger_lines(tree)[0]['audit']['counted_after_result'], 2,
                         'the audit says honestly that the forecasts were made again after their results')
        self.assertIn('the engine is not the one', job_log(tree)[-1]['rebuilt'][0])

    def test_the_small_files_and_pythons_cache_are_not_part_of_the_engines_fingerprint(self):
        tree = self.tree()
        before = code_identity.infrastructure_fingerprint(tree)
        folder = fx.method_folder(tree, 'E_901', 'TOY_A_V1')
        method_flags.write_retired(folder, {GAME: 1161}, 'a test')
        (tree / 'src' / method_flags.INSTALLABLE_NAME).write_bytes(b'; the engine may be installed\r\n')
        (tree / 'src' / '__pycache__').mkdir()
        (tree / 'src' / '__pycache__' / 'x.pyc').write_bytes(b'cache')
        (folder / 'method.py').write_text('# another method\n', encoding='ascii')     # a method is not the engine
        self.assertEqual(code_identity.infrastructure_fingerprint(tree), before)
        (tree / 'src' / 'methods' / '_common').mkdir()
        (tree / 'src' / 'methods' / '_common' / 'shared.py').write_text('# shared engine code\n', encoding='ascii')
        self.assertNotEqual(code_identity.infrastructure_fingerprint(tree), before)

    def test_a_changed_method_is_rebuilt_alone_and_its_establishment_draw_is_written_afresh(self):
        tree = self.tree()
        fx.run_job(tree)
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        fx.run_job(tree)
        other = {name: data for name, data in fx.files_under(tree).items() if 'TOY_B_V1' in name}
        old_top = [content['barrels']['MAIN']['top'] for content in contents(tree, 'TOY_A_V1')]
        method = fx.method_folder(tree, 'E_901', 'TOY_A_V1') / 'method.py'
        method.write_text(method.read_text(encoding='ascii').replace('BEHAVIOUR = {}', "BEHAVIOUR = {'rotate': 4}"),
                          encoding='ascii')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        rebuilt = [line for line in said if line.startswith('REBUILD')]
        self.assertEqual(len(rebuilt), 1, said)
        self.assertIn('E_901/TOY_A_V1: its stored results were made by other files than the method has now', rebuilt[0])
        self.assertEqual({name: data for name, data in fx.files_under(tree).items() if 'TOY_B_V1' in name}, other)
        self.assertNotEqual([content['barrels']['MAIN']['top'] for content in contents(tree, 'TOY_A_V1')], old_top)
        self.assertEqual(len(contents(tree, 'TOY_A_V1')), LAST_AFTER_NEW + 1 - fx.FIRST_TOY_TARGET + 1)
        self.assertEqual(self.status(tree, 'TOY_A_V1').eligible_from, LAST_AFTER_NEW + 1, 'written afresh')
        self.assertEqual(self.status(tree, 'TOY_B_V1').eligible_from, LAST_AT_START + 1, 'not touched')

    def test_rebuild_names_one_method_and_rebuild_all_names_everything(self):
        tree = self.tree()
        fx.run_job(tree)
        whole = fx.files_under(tree)
        code, said = fx.run_job(tree, rebuild=['E_901/TOY_B_V1'])
        self.assertEqual(code, 0, said)
        self.assertEqual([line for line in said if line.startswith('REBUILD: ')],
                         [f'REBUILD: {GAME}: E_901/TOY_B_V1: --rebuild names it'])
        self.assertEqual(fx.files_under(tree), whole)
        code, said = fx.run_job(tree, rebuild_all=True)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('REBUILD: everything' in line and '--rebuild-all was given' in line for line in said))
        self.assertEqual(fx.files_under(tree), whole)
        code, said = fx.run_job(tree, rebuild=['E_901/NO_SUCH_V1'])
        self.assertEqual(code, 2)
        self.assertTrue(any('--rebuild names no method of this tree: E_901/NO_SUCH_V1' in line for line in said), said)

    def test_results_with_nothing_to_say_which_engine_made_them_are_made_again(self):
        tree = self.tree()
        fx.run_job(tree)
        whole = fx.files_under(tree)
        (tree / 'results/research' / code_identity.STORED_NAME).unlink()
        code, said = fx.run_job(tree)
        self.assertTrue(any('nothing says which engine made these results' in line for line in said), said)
        self.assertEqual(fx.files_under(tree), whole)

    def test_a_corrected_draw_remakes_its_scores_and_every_forecast_computed_from_it_and_nothing_earlier(self):
        tree = self.tree()
        fx.run_job(tree)
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        fx.run_job(tree)                                                # lines made before and after their results
        corrected = 1158
        before = {which: fx.list_lines(tree, 'E_901', 'TOY_A_V1', which) for which in ('forecasts', 'scores')}
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=3, reseed_from=corrected)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        dropped = (LAST_AFTER_NEW + 1) - corrected
        self.assertTrue(any(f'E_901/TOY_A_V1: the results on file are no longer what its lines were made from: '
                            f'{dropped} forecasts (from draw {corrected + 1}) and {dropped} scores (from draw '
                            f'{corrected})' in line for line in said), said)
        after = {which: fx.list_lines(tree, 'E_901', 'TOY_A_V1', which) for which in ('forecasts', 'scores')}
        kept_forecasts = corrected - fx.FIRST_TOY_TARGET + 1                # targets up to the corrected draw
        self.assertEqual(after['forecasts'][:kept_forecasts], before['forecasts'][:kept_forecasts])
        self.assertEqual(after['scores'][:kept_forecasts - 1], before['scores'][:kept_forecasts - 1])
        self.assertNotEqual(after['scores'][kept_forecasts - 1]['content'], before['scores'][kept_forecasts - 1]['content'])
        fresh = self.tree(name='fresh', last_draw=LAST_AT_START)
        fx.write_results(fresh, GAME, LAST_AFTER_NEW, version=3, reseed_from=corrected)
        fx.run_job(fresh)
        for variant in ('TOY_A_V1', 'TOY_B_V1'):
            for which in ('forecasts', 'scores'):
                self.assertEqual(contents(tree, variant, which), contents(fresh, variant, which), (variant, which))
        self.assertEqual([line['content'] for line in fx.ledger_lines(tree, which='exploratory')],
                         [line['content'] for line in fx.ledger_lines(fresh, which='exploratory')])

    def test_a_stored_score_that_no_longer_follows_from_the_results_is_made_again(self):
        tree = self.tree()
        fx.run_job(tree)
        whole = fx.files_under(tree)

        def spoil(record):
            """Give the score one more TOP hit than it had."""
            record['content']['matches']['MAIN']['top'] += 1

        fx.alter_list_line(list_path(tree, 'TOY_A_V1', 'scores'), 5, spoil)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('0 forecasts (from draw None)' in line and f'scores (from draw {fx.FIRST_TOY_TARGET + 5})'
                            in line for line in said), said)
        self.assertEqual(fx.files_under(tree), whole)

    def test_results_that_became_shorter_drop_the_lines_beyond_them(self):
        tree = self.tree(last_draw=LAST_AFTER_NEW)
        fx.run_job(tree)
        fx.write_results(tree, GAME, LAST_AT_START, version=2)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], LAST_AT_START + 1)
        self.assertEqual(contents(tree, 'TOY_A_V1', 'scores')[-1]['target'], LAST_AT_START)
        # The league reports of the six draws no longer on file, and the next-draw report of the draw after them.
        self.assertTrue(any(f'{GAME}: 14 report files that the records no longer give were removed' in line
                            for line in said), [line for line in said if 'removed' in line])
        fresh = self.tree(name='fresh')
        fx.run_job(fresh)
        self.assertEqual(contents(tree, 'TOY_A_V1'), contents(fresh, 'TOY_A_V1'))
        # The same report files as a tree that never held the later draws; but for the next-draw report of draw
        # 1161, which only the fresh tree has, because only there was that forecast made before its result.
        reports_of = f'results/research/{GAME}/reports'
        self.assertEqual(set(fx.files_under(fresh, reports_of, leave_out=())) - set(fx.files_under(tree, reports_of, leave_out=())),
                         {f'{reports_of}/next/next_draw_{GAME}_d{LAST_AT_START + 1:05d}.{kind}' for kind in ('csv', 'txt')})
        self.assertEqual(set(fx.files_under(tree, reports_of, leave_out=())) - set(fx.files_under(fresh, reports_of, leave_out=())), set())
        times = fx.report_text(tree, reports.MADE_TIMES_NAME)
        self.assertNotIn(f'd{LAST_AFTER_NEW:05d}', times, 'the side file of making times names no removed report')

    def test_an_ordinary_job_leaves_alone_the_results_of_a_method_it_has_no_software_for_and_counts_them_nowhere(self):
        tree = self.tree(variants=('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5})))
        fx.run_job(tree)
        shutil.rmtree(fx.method_folder(tree, 'E_901', 'TOY_C_V1'))
        left = {name: data for name, data in fx.files_under(tree).items() if 'TOY_C_V1' in name and '/variants/' in name}
        self.assertEqual(len(left), 2)
        for options in ({}, {'rebuild': ['E_901/TOY_A_V1']}):
            code, said = fx.run_job(tree, **options)
            self.assertEqual(code, 0, said)
            self.assertTrue(any('stored results of E_901/TOY_C_V1 are left alone: this tree has no software for it'
                                in line for line in said), said)
            self.assertEqual({name: data for name, data in fx.files_under(tree).items()
                              if 'TOY_C_V1' in name and '/variants/' in name}, left)
        text = fx.report_text(tree, f'league/league_{GAME}_d{LAST_AT_START:05d}.txt')
        self.assertIn('Methods: 2', text)
        self.assertIn('E_901/TOY_C_V1 (not installed here)', text)
        self.assertEqual({member['variant'] for line in fx.ledger_lines(tree, which='exploratory')
                          for member in line['content']['cohort']}, {'E_901/TOY_A_V1', 'E_901/TOY_B_V1'})

    def test_a_rebuild_of_everything_deletes_them_too_so_a_method_that_comes_back_is_never_taken_as_up_to_date(self):
        tree = self.tree(variants=('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5})))
        fx.run_job(tree)
        software, away = fx.method_folder(tree, 'E_901', 'TOY_C_V1'), self.root / 'TOY_C_V1_away'
        shutil.move(software, away)
        (tree / 'src' / fx.ENGINE_FILE).write_text('# the engine, changed\n', encoding='ascii')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('REBUILD: everything, in both games (3 stored method results deleted)' in line
                            for line in said), said)
        self.assertFalse(list_path(tree, 'TOY_C_V1').parent.exists(), 'made by another engine: it may not stay')
        self.assertFalse(any('left alone' in line for line in said), said)
        shutil.move(away, software)                                     # the same software comes back, unchanged
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        made = 2 * (LAST_AT_START - fx.FIRST_TOY_TARGET + 1) + 1
        self.assertTrue(any(f'written: {LAST_AT_START - fx.FIRST_TOY_TARGET + 2} forecasts' in line for line in said),
                        (made, said))
        fresh = self.tree(variants=('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5})), name='fresh')
        fx.run_job(fresh)
        for which in ('forecasts', 'scores'):
            self.assertEqual(contents(tree, 'TOY_C_V1', which), contents(fresh, 'TOY_C_V1', which))


class RetiredAndInPlace(fx.JobCase):
    """Scheme section 4: I_AM_RETIRED and IN_PLACE_SINCE."""

    def test_the_first_job_writes_each_methods_establishment_draw_and_later_jobs_leave_it(self):
        tree = self.tree(variants=())
        self.add_variant(tree, 'TOY_A_V1', games=('POWERBALL', 'OZLOTTO'))
        fx.write_results(tree, 'OZLOTTO', 1480)
        fx.run_job(tree, games=(GAME,))
        path = fx.method_folder(tree, 'E_901', 'TOY_A_V1') / method_flags.IN_PLACE_NAME
        self.assertEqual(sorted(method_flags.read_flag(path)), ['fingerprint', 'in_place_since_POWERBALL'])
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        fx.run_job(tree, games=('POWERBALL', 'OZLOTTO'))
        flag = method_flags.read_flag(path)
        self.assertEqual((flag['in_place_since_POWERBALL'], flag['in_place_since_OZLOTTO']), (str(LAST_AT_START), '1480'))

    def test_a_retired_method_makes_no_later_forecast_keeps_its_earlier_results_and_comes_back_when_the_file_goes(self):
        tree = self.tree()
        fx.run_job(tree)
        folder = fx.method_folder(tree, 'E_901', 'TOY_B_V1')
        (folder / method_flags.RETIRED_NAME).write_bytes(b'')           # made by hand, empty: from the next draw
        before = contents(tree, 'TOY_B_V1', 'scores')
        code, said = fx.run_job(tree)                                   # the job writes the draw into the file
        self.assertEqual(code, 0, said)
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        status = self.status(tree, 'TOY_B_V1')
        self.assertEqual((status.withdrawn_from, status.withdrawn_reason), (LAST_AT_START + 1, 'no reason was written'))
        self.assertEqual(contents(tree, 'TOY_B_V1', 'scores'), before, 'its earlier results stay')
        self.assertEqual(contents(tree, 'TOY_B_V1')[-1]['target'], LAST_AT_START,
                         'no forecast for its retirement draw or later: the one it held for that draw is dropped')
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], LAST_AFTER_NEW + 1)
        text = fx.report_text(tree, f'league/league_{GAME}_d{LAST_AFTER_NEW:05d}.txt')
        self.assertIn(f'RETIRED from draw {LAST_AT_START + 1}: no reason was written', text)
        for line in fx.ledger_lines(tree):
            self.assertEqual([member['variant'] for member in line['content']['cohort']], ['E_901/TOY_A_V1'])
        (folder / method_flags.RETIRED_NAME).unlink()
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(contents(tree, 'TOY_B_V1')[-1]['target'], LAST_AFTER_NEW + 1, 'it is back and caught up')
        self.assertEqual(len(contents(tree, 'TOY_B_V1', 'scores')), LAST_AFTER_NEW - fx.FIRST_TOY_TARGET + 1)

    def test_a_method_retired_from_an_earlier_draw_loses_what_it_held_from_that_draw_on(self):
        tree = self.tree()
        fx.run_job(tree)
        method_flags.write_retired(fx.method_folder(tree, 'E_901', 'TOY_B_V1'), {GAME: 1155}, 'the table was wrong')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('E_901/TOY_B_V1: retired from draw 1155: 7 forecasts and 6 scores for that draw or later '
                            'dropped' in line for line in said), said)
        self.assertEqual(contents(tree, 'TOY_B_V1')[-1]['target'], 1154)
        self.assertEqual(contents(tree, 'TOY_B_V1', 'scores')[-1]['target'], 1154)
        self.assertIn('RETIRED from draw 1155: the table was wrong',
                      fx.report_text(tree, f'league/league_{GAME}_d{LAST_AT_START:05d}.txt'))
        code, said = fx.run_job(tree)
        self.assertTrue(any('0 forecasts, 0 scores, 0 series files, 0 report files' in line for line in said), said)

    def test_a_method_retired_as_draws_arrive_and_the_same_method_rebuilt_hold_the_same_history(self):
        tree = self.tree()
        fx.run_job(tree)                                                # it holds its forecast for draw 1161
        method_flags.write_retired(fx.method_folder(tree, 'E_901', 'TOY_B_V1'), {GAME: LAST_AT_START + 1}, 'a test')
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        fx.run_job(tree)
        as_draws_arrived = {which: contents(tree, 'TOY_B_V1', which) for which in ('forecasts', 'scores')}
        code, said = fx.run_job(tree, rebuild=['E_901/TOY_B_V1'])
        self.assertEqual(code, 0, said)
        self.assertEqual({which: contents(tree, 'TOY_B_V1', which) for which in ('forecasts', 'scores')},
                         as_draws_arrived)
        self.assertEqual(as_draws_arrived['forecasts'][-1]['target'], LAST_AT_START)

    def test_a_small_file_that_cannot_be_read_passes_its_method_over_and_the_job_goes_on(self):
        tree = self.tree()
        fx.run_job(tree)
        (fx.method_folder(tree, 'E_901', 'TOY_B_V1') / method_flags.RETIRED_NAME).write_bytes(b'retired, I think\r\n')
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 1)
        self.assertTrue(any('E_901/TOY_B_V1 is passed over' in line and 'not "key = value"' in line for line in said))
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], LAST_AFTER_NEW + 1)
        self.assertEqual(contents(tree, 'TOY_B_V1')[-1]['target'], LAST_AT_START + 1, 'its results are as they were')

    def test_an_establishment_file_that_cannot_be_read_never_stops_its_method_and_is_written_afresh(self):
        tree = self.tree()
        fx.run_job(tree)
        path = fx.method_folder(tree, 'E_901', 'TOY_B_V1') / method_flags.IN_PLACE_NAME
        for damaged in (b'in place since, I think\r\n', b'fingerprint = ab12\r\nin_place_since_POWERBALL = soon\r\n'):
            path.write_bytes(damaged)
            fx.write_results(tree, GAME, fx.read_last_draw(tree) + 1, version=2)
            last = fx.read_last_draw(tree)
            code, said = fx.run_job(tree)
            self.assertEqual(code, 0, said)
            self.assertTrue(any(f'E_901/TOY_B_V1: its {method_flags.IN_PLACE_NAME} could not be read and was written '
                                f'afresh: it now counts in the second OV-1 series from draw {last + 1}' in line
                                for line in said), said)
            self.assertEqual(contents(tree, 'TOY_B_V1')[-1]['target'], last + 1, 'the method was worked as usual')
            self.assertEqual(self.status(tree, 'TOY_B_V1').eligible_from, last + 1)
            self.assertEqual(self.status(tree, 'TOY_A_V1').eligible_from, LAST_AT_START + 1, 'not touched')

    def test_a_job_stopped_while_a_small_file_was_written_leaves_nothing_that_stops_the_next_job(self):
        tree = self.tree()
        fx.run_job(tree)
        folder = fx.method_folder(tree, 'E_901', 'TOY_A_V1')
        (folder / (method_flags.IN_PLACE_NAME + method_flags.STAGED_SUFFIX)).write_bytes(b'; half')
        before = code_identity.infrastructure_fingerprint(tree)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertFalse(any('REBUILD' in line or 'WARNING' in line for line in said), said)
        self.assertEqual(code_identity.infrastructure_fingerprint(tree), before)


class Reports(fx.JobCase):
    """The reports and both OV-1 series are made again by every job from the lists, the results and the small
    files alone."""

    def test_the_same_records_give_the_same_report_bytes(self):
        tree = self.tree()
        fx.run_job(tree)
        first = fx.files_under(tree, f'results/research/{GAME}/reports')
        code, said = fx.run_job(tree)
        self.assertTrue(any('0 report files' in line for line in said), said)
        shutil.rmtree(tree / 'results/research' / GAME / 'reports')
        shutil.rmtree(tree / 'results/research' / GAME / 'ov1')
        fx.run_job(tree)
        self.assertEqual(fx.files_under(tree, f'results/research/{GAME}/reports'), first)

    def test_a_next_draw_report_of_a_forecast_since_made_again_is_removed(self):
        tree = self.tree()
        fx.run_job(tree)
        fx.write_results(tree, GAME, LAST_AFTER_NEW, version=2)
        fx.run_job(tree)
        folder = tree / 'results/research' / GAME / 'reports/next'
        both = [f'next_draw_{GAME}_d{draw:05d}.{kind}' for draw in (LAST_AT_START + 1, LAST_AFTER_NEW + 1)
                for kind in ('csv', 'txt')]
        self.assertEqual(sorted(path.name for path in folder.iterdir()), both)
        (folder / 'left_half_written.txt.writing').write_bytes(b'half')
        code, said = fx.run_job(tree, rebuild_all=True)                 # every forecast is now made after its result
        self.assertEqual(code, 0, said)
        self.assertEqual(sorted(path.name for path in folder.iterdir()), both[2:])
        self.assertFalse(any(f'd{LAST_AT_START + 1:05d}' in line and line.startswith('next/')
                             for line in fx.report_text(tree, reports.MADE_TIMES_NAME).splitlines()))

    def test_a_changed_report_formatter_leaves_no_file_of_the_old_format(self):
        tree = self.tree()
        fx.run_job(tree)
        with mock.patch.object(reports, 'LEAGUE_HEADLINE', 'A NEW HEADLINE. It selects nothing.'):
            fx.run_job(tree)
        league = sorted((tree / 'results/research' / GAME / 'reports/league').iterdir())
        self.assertEqual(len(league), 2 * (LAST_AT_START - fx.FIRST_TOY_TARGET + 1))
        for path in league:
            self.assertIn('A NEW HEADLINE', path.read_text(encoding='ascii'), path.name)

    def test_the_league_figures_are_those_of_the_score_list(self):
        tree = self.tree()
        fx.run_job(tree)
        through = [content for content in contents(tree, 'TOY_A_V1', 'scores') if content['target'] <= 1155]
        top_hits = sum(s['matches']['MAIN']['top'] for s in through)
        worst_hits = sum(s['matches']['MAIN']['worst'] for s in through)
        rows = list(csv.reader(io.StringIO(fx.report_text(tree, f'league/league_{GAME}_d01155.csv'))))
        header = next(row for row in rows if row and row[0] == 'order_top')
        row = dict(zip(header, next(row for row in rows if len(row) > 1 and row[1] == 'E_901/TOY_A_V1')))
        self.assertEqual((row['draws_scored'], row['top_hits'], row['worst_hits']),
                         (str(len(through)), str(top_hits), str(worst_hits)))
        self.assertEqual(row['top_hits_a_draw'], f'{top_hits / len(through):.3f}')
        self.assertEqual(row['chance_hits_a_draw'], '1.400')
        self.assertEqual(row['first_scored_draw'], str(fx.FIRST_TOY_TARGET))
        self.assertEqual(row['scored_forecasts_made_before_result'], '0')
        self.assertEqual(row['prevailing_ov1_first_draw'], str(LAST_AT_START + 1))
        self.assertEqual(row[f'top_last_{reports.LAST_DRAWS_SHOWN}'],
                         ''.join(str(s['matches']['MAIN']['top']) for s in through[-reports.LAST_DRAWS_SHOWN:]))
        text = fx.report_text(tree, f'league/league_{GAME}_d01155.txt')
        for wanted in (reports.LEAGUE_HEADLINE, f'the DEV tree at {tree}', 'Runs to draw: 1155', 'Methods: 2',
                       'Foreign lists ignored: none'):
            self.assertIn(wanted, text)

    def test_the_next_draw_report_shows_each_forecast_as_its_list_holds_it(self):
        tree = self.tree()
        fx.run_job(tree)
        forecast = contents(tree, 'TOY_A_V1')[-1]
        self.assertEqual(forecast['target'], 1161)
        rows = list(csv.reader(io.StringIO(fx.report_text(tree, f'next/next_draw_{GAME}_d01161.csv'))))
        row = next(row for row in rows if row and row[0] == 'E_901/TOY_A_V1')
        self.assertEqual(row[1], 'FORECAST')
        self.assertEqual(row[2], ' '.join(str(n) for n in sorted(forecast['barrels']['MAIN']['top'])))
        self.assertEqual(row[3], ' '.join(str(n) for n in sorted(forecast['barrels']['MAIN']['worst'])))
        self.assertEqual(row[6], 'yes')

    def test_the_time_of_making_is_in_the_side_file_and_in_no_report(self):
        tree = self.tree()
        fx.run_job(tree)
        made = fx.FIXED_TIME.astimezone().strftime('%Y-%m-%d %H:%M')
        times = fx.report_text(tree, reports.MADE_TIMES_NAME)
        self.assertIn(f'league/league_{GAME}_d01160.txt,{made}', times)
        for name, data in fx.files_under(tree, f'results/research/{GAME}/reports').items():
            self.assertNotIn(made.encode('ascii'), data, name)

    def test_the_job_log_gains_one_line_a_job_with_the_python_and_package_versions(self):
        tree = self.tree()
        fx.run_job(tree)
        fx.run_job(tree, rebuild=['E_901/TOY_A_V1'])
        log = job_log(tree)
        self.assertEqual(len(log), 2)
        self.assertEqual(log[0]['python'], '.'.join(str(part) for part in sys.version_info[:3]) if sys.version_info[3]
                         == 'final' else log[0]['python'])
        self.assertIn('numpy', log[0]['packages'])
        self.assertEqual((log[0]['how'], log[0]['rebuilt'], log[0]['failed']), ('finished', [], []))
        self.assertEqual(log[1]['rebuilt'], [f'{GAME}: E_901/TOY_A_V1: --rebuild names it'])
        self.assertEqual(log[1]['infrastructure_fingerprint'], code_identity.infrastructure_fingerprint(tree))
        self.assertEqual(log[0]['written'][GAME]['forecasts'], 2 * (LAST_AT_START + 1 - fx.FIRST_TOY_TARGET + 1))
        self.assertTrue((tree / research_job.JOB_LOG).read_bytes().endswith(b'}\r\n'))


class StartingAndStopping(fx.JobCase):
    """What stops the job before any game, and the games kept apart."""

    def test_a_lock_that_exists_refuses_and_is_never_removed_by_another_job(self):
        tree = self.tree()
        lock = tree / tree_lock.RECORDS_FOLDER / tree_lock.LOCK_NAME
        lock.parent.mkdir(exist_ok=True)
        lock.write_text('research job; started earlier\n', encoding='ascii')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 2)
        self.assertTrue(any('a process of this tree is running' in line and 'delete that one file by hand' in line
                            for line in said), said)
        self.assertTrue(lock.is_file())
        lock.unlink()
        self.assertEqual(fx.run_job(tree)[0], 0)
        self.assertFalse(lock.exists(), 'a finished job leaves no lock')

    def test_a_tree_that_is_not_what_its_settings_say_refuses(self):
        tree = self.tree()
        for name, why in (('moved', 'does not end with DEV'), ('moved_DEV', 'but the file lies in')):
            moved = self.root / name
            shutil.copytree(tree, moved)
            code, said = fx.run_job(moved)
            self.assertEqual(code, 2, name)
            self.assertTrue(any(line.startswith('REFUSED:') and why in line
                                and 'This folder is not the tree its file says: nothing is done here' in line
                                for line in said), said)
            self.assertFalse((moved / 'results').exists(), 'nothing was written in it')

    def test_the_games_are_worked_apart_and_one_stopping_leaves_the_other_finished(self):
        tree = self.tree(variants=())
        self.add_variant(tree, 'TOY_A_V1', games=('POWERBALL', 'OZLOTTO'))
        fx.write_results(tree, 'OZLOTTO', 1480)
        master = tree / 'source_data' / 'OZLOTTO_results_master.csv'
        master.write_bytes(master.read_bytes() + b'\n')                   # changed outside the updater
        code, said = fx.run_job(tree, games=('OZLOTTO', 'POWERBALL'))
        self.assertEqual(code, 1)
        self.assertTrue(any(line.startswith('OZLOTTO: STOPPED:') for line in said), said)
        self.assertTrue(any(line.startswith('POWERBALL: finished.') for line in said), said)
        self.assertEqual(said[-1], 'A STOP is a STOP: at least one game did not finish; nothing retries by itself.')
        self.assertFalse((tree / 'results/research/OZLOTTO').exists())
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], LAST_AT_START + 1)

    def test_a_method_folder_that_fails_its_checks_is_named_and_passed_over_and_the_job_goes_on(self):
        tree = self.tree()
        (fx.method_folder(tree, 'E_901', 'TOY_B_V1') / 'method.py.bak').write_text('x', encoding='ascii')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 1)
        self.assertTrue(any('the method folder' in line and 'TOY_B_V1' in line and 'passed over' in line
                            for line in said), said)
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], LAST_AT_START + 1)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1'), [])

    def test_the_engine_starts_no_program_and_opens_no_connection(self):
        engine = sorted((TREE_OF_THIS_FILE / 'src' / 'research').glob('*.py')) + [TREE_OF_THIS_FILE / 'src'
                                                                                  / 'research_command.py']
        self.assertGreater(len(engine), 15)
        for path in engine:
            tree = ast.parse(path.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module or '']
                for name in names:
                    self.assertNotIn(name.split('.')[0], FORBIDDEN_IMPORTS, f'{path.name} imports {name}')
                if isinstance(node, ast.Attribute):
                    self.assertNotIn(node.attr, FORBIDDEN_CALLS, f'{path.name} uses .{node.attr}')
            text = path.read_text(encoding='utf-8')
            for word in ('results_master_v0', 'lotterywest', 'thelott', 'selenium', 'webdriver'):
                self.assertNotIn(word.lower(), text.lower(), f'{path.name} names {word}')

    def test_the_engine_loads_the_updater_in_one_place_only_and_never_when_the_file_is_read(self):
        for path in sorted((TREE_OF_THIS_FILE / 'src' / 'research').glob('*.py')) + [TREE_OF_THIS_FILE / 'src'
                                                                                     / 'research_command.py']:
            tree = ast.parse(path.read_text(encoding='utf-8'))
            at_the_top = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
            for node in at_the_top:
                names = [alias.name for alias in node.names] + [getattr(node, 'module', None) or '']
                self.assertFalse(any(name.split('.')[0] == 'updater' for name in names), f'{path.name}, at its top')
            inside = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
                      and node not in at_the_top and (getattr(node, 'module', None) or node.names[0].name
                                                      ).split('.')[0] == 'updater']
            expected = {'research_job.py': 1, 'research_command.py': 1}.get(path.name, 0)
            self.assertEqual(len(inside), expected, path.name)


class TheCommandProgram(fx.JobCase):
    """src/research_command.py, the one program behind the launchers."""

    def test_an_unknown_command_is_refused(self):
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            self.assertEqual(research_command.run_command(['tidy']), research_command.EXIT_BAD_COMMAND)
        self.assertIn('the first word must be one of', printed.getvalue())

    def tree_with_the_engine(self) -> Path:
        """An invented tree that holds the engine's own files, as a real tree does."""
        tree = self.tree()
        for folder in ('research', 'evaluation', 'methods/_common'):
            shutil.copytree(TREE_OF_THIS_FILE / 'src' / folder, tree / 'src' / folder,
                            ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy(TREE_OF_THIS_FILE / 'src/research_command.py', tree / 'src/research_command.py')
        return tree

    def launch(self, tree: Path, *arguments) -> subprocess.CompletedProcess:
        """Start the command program as a launcher does: this Python, isolated, writing no cache."""
        return subprocess.run([sys.executable, '-I', '-B', str(tree / 'src/research_command.py'), *arguments],
                              capture_output=True, text=True, timeout=300, cwd=str(self.root))

    def test_a_python_that_is_not_the_trees_own_environment_is_refused(self):
        tree = self.tree_with_the_engine()
        done = self.launch(tree, 'research', '--no-update')
        self.assertEqual(done.returncode, research_command.EXIT_BAD_COMMAND, done.stdout + done.stderr)
        self.assertIn('REFUSED: the Python running is', done.stdout)
        self.assertFalse((tree / 'results').exists())
        self.assertEqual(list((tree / 'src').rglob('__pycache__')), [], 'started this way Python writes no cache')

    def test_with_the_trees_own_python_the_command_runs_the_job_in_the_tree_the_program_lies_in(self):
        tree = self.tree()
        path_before = list(sys.path)
        printed = io.StringIO()
        try:
            with mock.patch.object(research_command, 'TREE_ROOT', tree), \
                    mock.patch.object(research_command, 'IMPORT_FOLDERS', (tree / 'src', tree / 'src' / 'methods')), \
                    mock.patch.object(sys, 'prefix', str(tree / '.venv')), contextlib.redirect_stdout(printed):
                code = research_command.run_command(['research', '--game', GAME, '--no-update'])
        finally:
            sys.path[:] = path_before
            fx.ImportPath._forget()
        said = printed.getvalue().splitlines()
        self.assertEqual(code, 0, said)
        self.assertIn(f'the DEV tree at {tree}', said[0])
        self.assertEqual(said[-1], 'The job finished.')
        self.assertEqual(contents(tree, 'TOY_A_V1')[-1]['target'], LAST_AT_START + 1)

    def test_the_launcher_names_its_command_and_runs_python_isolated_without_a_cache(self):
        text = (TREE_OF_THIS_FILE / 'Run_Research.bat').read_bytes().decode('ascii')
        self.assertIn('"%PY%" -I -B -u "%TOOL%" research %*\r\n', text)
        self.assertEqual(text.count('\r\n'), text.count('\n'), 'CRLF line endings throughout')


if __name__ == '__main__':
    unittest.main()
