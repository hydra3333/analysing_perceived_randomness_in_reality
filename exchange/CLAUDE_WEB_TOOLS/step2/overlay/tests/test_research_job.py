"""Tests of the research job (specification v0.6 sections 5.3, 5.6A, 5.7, 7.1, 7.2 and 9), on invented draws and
toy variants.

Each test is named for the rule it proves. The examples of section 7.2 are followed line for line, with draw 1160
standing for the specification's 1600. A crash is planted between every two writes of section 5.7 and the job run
again must give the bytes of an uninterrupted run.
"""
import ast
import contextlib
import csv
import io
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

import research_command
import research_fixtures as fx
from research import job_lock, reports, results_step, status_file
from research.reader import results_on_file
from research.status_file import GameStatus, write_status
from research.variant_folders import find_variants

GAME = fx.GAME
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LAST_AT_START, LAST_IN_SOURCE = fx.LAST_AT_START, fx.LAST_IN_SOURCE
# Words the engine's own files must never hold: it starts no program and opens no connection.
FORBIDDEN_IMPORTS = ('subprocess', 'socket', 'urllib', 'http', 'requests', 'ftplib', 'smtplib', 'multiprocessing')
FORBIDDEN_CALLS = ('system', 'popen', 'startfile', 'spawnl', 'spawnv', 'execl', 'execv', 'kill')


class Killed(BaseException):
    """A planted crash: not an Exception, so that nothing in the job catches it, as nothing catches a kill."""


class Records(fx.JobCase):
    """Specification 5.3 and 5.6 as the job applies them (F01)."""

    def test_a_method_failure_is_a_line_of_its_own_and_the_job_goes_on(self):
        tree = self.tree(variants=(('TOY_A_V1', {'fail_at': [1150], 'verify_fail_at': [1152]}),))
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        lines = {line['content']['target']: line for line in fx.list_lines(tree, 'E_901', 'TOY_A_V1')}
        scored = {line['content']['target'] for line in fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores')}
        self.assertEqual([lines[t]['content']['status'] for t in (1149, 1150, 1151, 1152)],
                         ['FORECAST', 'NO_FORECAST', 'FORECAST', 'NO_FORECAST'])
        self.assertEqual(lines[1150]['content']['reason'], 'METHOD_FAILED')
        self.assertIn('compute() declared a failure', lines[1150]['envelope']['detail'])
        self.assertIn('verify() refused', lines[1152]['envelope']['detail'])
        self.assertEqual(scored, set(range(fx.FIRST_TOY_TARGET, LAST_AT_START + 1)) - {1150, 1152})

    def test_the_first_target_is_fixed_by_the_minimum_history_and_too_little_history_is_a_typed_line(self):
        tree = self.tree(variants=(('TOY_A_V1', {'short_below': 6}),))
        fx.run_job(tree, no_update=True)
        lines = fx.list_lines(tree, 'E_901', 'TOY_A_V1')
        self.assertEqual(lines[0]['content']['target'], fx.FIRST_TOY_TARGET)
        self.assertEqual([(l['content']['status'], l['content'].get('reason')) for l in lines[:4]],
                         [('NO_FORECAST', 'INSUFFICIENT_HISTORY')] * 3 + [('FORECAST', None)])

    def test_any_other_exception_writes_no_line_and_stops_the_game(self):
        tree = self.tree(variants=(('TOY_A_V1', {'crash_at': [1152]}), 'TOY_B_V1'))
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 1)
        self.assertTrue(any('STOPPED by a fault' in line and 'an environmental fault' in line for line in said), said)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1')[-1]['content']['target'], 1151)
        before = fx.files_under(tree)
        code, _ = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 1)
        self.assertEqual(fx.files_under(tree), before, 'running it again tries again and writes nothing new')

    def test_a_broken_list_refuses_its_game_and_names_the_line(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        path = tree / 'results/research' / GAME / 'variants/E_901/TOY_A_V1/scores.jsonl'
        lines = path.read_bytes().split(b'\n')
        path.write_bytes(b'\n'.join(lines[:3] + lines[4:]))             # one score line taken out: the chain breaks
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 1)
        self.assertTrue(any('REFUSED' in line and 'scores.jsonl line 4' in line and 'chain is broken' in line
                            for line in said), said)

    def test_a_torn_last_line_in_each_file_is_cut_and_redone(self):
        tree = self.tree()
        self.source(LAST_IN_SOURCE)
        fx.run_job(tree)                                                # eligibility draws 1167
        self.source(LAST_IN_SOURCE + 2, version=3)
        fx.run_job(tree)                                                # prevailing lines for 1167 and 1168
        whole = fx.files_under(tree)
        stored = [name for name in whole if name.endswith('.jsonl')]
        self.assertEqual(len(stored), 5, stored)
        for name in stored:
            (tree / name).write_bytes(whole[name][:-40])                # a crash while the last line was written
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(fx.files_under(tree), whole)


class CrashResume(fx.JobCase):
    """Specification 5.7: what to do next is read from the files, never remembered."""

    def test_a_crash_between_any_two_writes_then_the_job_again_gives_the_bytes_of_an_uninterrupted_run(self):
        tree = self.tree(variants=('TOY_A_V1', 'TOY_B_V1', ('TOY_C_V1', {'rotate': 5, 'fail_at': [1163]})))
        self.source(LAST_AT_START + 1)
        fx.run_job(tree)                                                # eligibility draws 1162 for all three
        self.source(LAST_AT_START + 4, version=3)                       # three draws now wait to be caught up
        pristine = self.root / 'pristine'
        shutil.copytree(tree, pristine)
        labels = []
        code, said = fx.run_job(tree, checkpoint=labels.append)
        self.assertEqual(code, 0, said)
        reference = {**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'src/methods')}
        self.assertEqual(sorted(set(labels)), ['eligibility draw written', 'forecast line written',
                                               'league report written', 'prevailing line written',
                                               'score line written'][1:])
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

    def test_a_crash_while_the_first_eligibility_draws_are_written_is_continued_by_the_next_job(self):
        tree = self.tree()
        seen = []

        def checkpoint(label):
            """Die after the first eligibility draw is written."""
            seen.append(label)
            if label == 'eligibility draw written':
                raise Killed(label)

        with self.assertRaises(Killed):
            fx.run_job(tree, checkpoint=checkpoint)
        self.assertEqual((self.status(tree, 'TOY_A_V1').eligible_from, self.status(tree, 'TOY_B_V1').eligible_from),
                         (LAST_AT_START + 1, None))
        code, _ = fx.run_job(tree)
        self.assertEqual(code, 0)
        self.assertEqual(self.status(tree, 'TOY_B_V1').eligible_from, LAST_AT_START + 1)


class InterruptedStatusWrite(fx.JobCase):
    """EX_283 F283-B01: an interrupted status write never leaves a file that disables a variant. After each
    planted interruption the real variant scanner and the real job are run."""

    VARIANTS = ('TOY_A_V1', 'TOY_B_V1')

    def assert_variants_whole(self, tree: Path, with_status: bool = True) -> None:
        """Each variant folder holds exactly its own files, and the scanner accepts both variants."""
        wanted = ['VARIANT.json'] + (['VARIANT_STATUS.ini'] if with_status else []) + ['method.py']
        for name in self.VARIANTS:
            folder = tree / 'src/methods/E_901' / name
            self.assertEqual(sorted(p.name for p in folder.iterdir() if p.name != '__pycache__'), wanted, name)
        variants, refused = find_variants(tree / 'src/methods')
        self.assertEqual((len(variants), refused), (2, []))

    @staticmethod
    def staged(tree: Path) -> list:
        """The names in the tree's status staging folder."""
        folder = tree / status_file.STAGING_FOLDER
        return sorted(p.name for p in folder.iterdir()) if folder.is_dir() else []

    def test_an_eligibility_write_interrupted_by_a_kill_a_failure_or_a_half_written_copy_is_continued(self):
        tree = self.tree()
        pristine = self.root / 'pristine'
        shutil.copytree(tree, pristine)
        self.assertEqual(fx.run_job(tree)[0], 0)
        reference = {**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'src/methods')}
        real_rename = status_file._rename_into_place
        for how in ('killed at the first rename', 'the second rename fails', 'a half-written copy left behind'):
            with self.subTest(how=how):
                shutil.rmtree(tree)
                shutil.copytree(pristine, tree)
                calls = []

                def rename(temporary, path, how=how, calls=calls):
                    """The rename, with the interruption planted for this case."""
                    calls.append(path)
                    if how == 'killed at the first rename':
                        raise Killed('at the rename')
                    if how == 'the second rename fails' and len(calls) == 2:
                        raise OSError('planted: the rename failed')
                    real_rename(temporary, path)

                if how == 'a half-written copy left behind':
                    staging = tree / status_file.STAGING_FOLDER
                    staging.mkdir(parents=True, exist_ok=True)
                    (staging / 'E_901__TOY_A_V1__VARIANT_STATUS.ini.writing').write_bytes(b'; E_901 / TOY_A')
                else:
                    with mock.patch.object(status_file, '_rename_into_place', rename):
                        if how == 'killed at the first rename':
                            with self.assertRaises(Killed):
                                fx.run_job(tree)
                        else:
                            code, said = fx.run_job(tree)
                            self.assertEqual(code, 1)
                            self.assertTrue(any('STOPPED by a fault' in line and 'the rename failed' in line
                                                for line in said), said)
                            self.assertEqual((self.status(tree, 'TOY_A_V1').eligible_from,
                                              self.status(tree, 'TOY_B_V1').eligible_from), (LAST_AT_START + 1, None))
                self.assertEqual(len(self.staged(tree)), 1, 'the unfinished copy lies in the staging folder only')
                self.assert_variants_whole(tree)
                code, said = fx.run_job(tree)
                self.assertEqual(code, 0, said)
                self.assertFalse(any('fails its checks' in line for line in said), said)
                self.assertTrue(any('its unfinished copy was removed' in line for line in said), said)
                self.assertEqual(self.staged(tree), [])
                self.assert_variants_whole(tree)
                again = {**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'src/methods')}
                self.assertEqual(sorted(again), sorted(reference))
                for name in reference:
                    self.assertEqual(again[name], reference[name], name)

    def test_in_dev_the_first_creation_of_a_status_file_interrupted_at_the_rename_is_made_again(self):
        tree = self.tree(role='DEV', with_source=False)
        for name in self.VARIANTS:
            fx.status_path(tree, 'E_901', name).unlink()
        with mock.patch.object(status_file, '_rename_into_place', side_effect=Killed('at the rename')):
            with self.assertRaises(Killed):
                fx.run_job(tree, no_update=True)
        self.assertEqual(len(self.staged(tree)), 1)
        self.assert_variants_whole(tree, with_status=False)
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 0, said)
        self.assert_variants_whole(tree)
        for name in self.VARIANTS:
            self.assertEqual(self.status(tree, name), GameStatus())
            self.assertEqual(fx.list_lines(tree, 'E_901', name)[-1]['content']['target'], LAST_AT_START + 1)

    def test_a_withdrawal_interrupted_at_the_rename_leaves_the_variant_active_and_whole_and_can_be_made_again(self):
        from research import withdraw
        for how, planted in (('killed', Killed('at the rename')), ('failed', OSError('planted: the rename failed'))):
            with self.subTest(how=how):
                tree = self.tree(with_source=False, name=f'tree_{how}')
                self.assertEqual(fx.run_job(tree, no_update=True)[0], 0)
                before = fx.status_path(tree, 'E_901', 'TOY_B_V1').read_bytes()
                results_before = fx.files_under(tree)
                arguments = (tree, [('E_901', 'TOY_B_V1')], (GAME,), 'wrong column')
                options = {'ask': lambda question: 'WITHDRAW', 'now': lambda: fx.FIXED_TIME}
                said = []
                with mock.patch.object(status_file, '_rename_into_place', side_effect=planted):
                    if how == 'killed':
                        with self.assertRaises(Killed):
                            withdraw.withdraw(*arguments, say=said.append, **options)
                    else:
                        self.assertEqual(withdraw.withdraw(*arguments, say=said.append, **options), withdraw.EXIT_STOPPED)
                        self.assertIn('No status file is half-written', said[-1])
                self.assertEqual(fx.status_path(tree, 'E_901', 'TOY_B_V1').read_bytes(), before)
                self.assert_variants_whole(tree)
                self.assertFalse((tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME).exists())
                code, job_said = fx.run_job(tree, no_update=True)          # a job in between: the variant runs
                self.assertEqual(code, 0, job_said)
                self.assertEqual(fx.files_under(tree), results_before, 'nothing scientific changed')
                said = []
                self.assertEqual(withdraw.withdraw(*arguments, say=said.append, **options), withdraw.EXIT_DONE)
                self.assertEqual(self.status(tree, 'TOY_B_V1').withdrawn_from, LAST_AT_START + 1)
                self.assertEqual(self.staged(tree), [])
                self.assert_variants_whole(tree)


class InterruptedResultsCopy(fx.JobCase):
    """EX_283 F283-B02: from an accepted pair and a source that extends it, an interruption at any point of the
    copy leaves the old pair or the new pair, never a mixture, and the next job gives the uninterrupted bytes."""

    def setUp(self):
        """A tree whose variants count from 1161, a source two draws longer, and the uninterrupted job's result."""
        super().setUp()
        self.tree_folder = self.tree()
        self.assertEqual(fx.run_job(self.tree_folder)[0], 0)
        self.source(LAST_AT_START + 2, version=2)
        self.pristine = self.root / 'pristine'
        shutil.copytree(self.tree_folder, self.pristine)
        self.master = self.tree_folder / 'source_data' / f'{GAME}_results_master.csv'
        self.ledger = self.tree_folder / 'source_data' / f'{GAME}_results_master_ledger.csv'
        self.old_pair = (self.master.read_bytes(), self.ledger.read_bytes())
        self.new_pair = ((self.root / 'source/source_data' / self.master.name).read_bytes(),
                         (self.root / 'source/source_data' / self.ledger.name).read_bytes())
        self.assertEqual(fx.run_job(self.tree_folder)[0], 0)
        self.reference = self.everything()
        self.assertEqual(self.pair(), self.new_pair)

    def everything(self) -> dict:
        """Every file of the tree that a job can write: research results, accepted results, status files."""
        tree = self.tree_folder
        return {**fx.files_under(tree, leave_out=()), **fx.files_under(tree, 'source_data'),
                **fx.files_under(tree, 'src/methods')}

    def pair(self) -> tuple:
        """The accepted results file and ledger now on disk."""
        return self.master.read_bytes(), self.ledger.read_bytes()

    def restore(self) -> None:
        """Put the tree back as it was before the copy."""
        shutil.rmtree(self.tree_folder)
        shutil.copytree(self.pristine, self.tree_folder)

    def staged(self) -> list:
        """The staged files now beside the accepted ones."""
        return sorted(p.name for p in self.master.parent.iterdir() if p.name.endswith(results_step.INCOMING_SUFFIX))

    def assert_the_next_job_gives_the_uninterrupted_bytes(self, label: str) -> None:
        """Run the job again and compare every file with the uninterrupted run's."""
        code, said = fx.run_job(self.tree_folder)
        self.assertEqual(code, 0, (label, said))
        again = self.everything()
        self.assertEqual(sorted(again), sorted(self.reference), label)
        for name in self.reference:
            self.assertEqual(again[name], self.reference[name], (label, name))

    def test_every_state_a_crash_can_leave_is_finished_or_discarded_to_a_consistent_pair(self):
        new_master, new_ledger = self.new_pair
        half = lambda data: data[:len(data) // 2]
        states = {                                  # label: (staged results, staged ledger, results replaced, expected pair)
            'half the results staged': (half(new_master), None, False, 'old'),
            'the results staged': (new_master, None, False, 'old'),
            'the results staged and half the ledger': (new_master, half(new_ledger), False, 'old'),
            'both staged, nothing replaced': (new_master, new_ledger, False, 'old'),
            'the results replaced, the ledger still staged': (None, new_ledger, True, 'new'),
            'a staged ledger alone beside the OLD results (the state EX_283 found)': (None, new_ledger, False, 'old'),
            'half a staged ledger alone beside the old results': (None, half(new_ledger), False, 'old'),
        }
        for label, (staged_master, staged_ledger, replaced, expected) in states.items():
            with self.subTest(state=label):
                self.restore()
                if staged_master is not None:
                    Path(str(self.master) + results_step.INCOMING_SUFFIX).write_bytes(staged_master)
                if staged_ledger is not None:
                    Path(str(self.ledger) + results_step.INCOMING_SUFFIX).write_bytes(staged_ledger)
                if replaced:
                    self.master.write_bytes(new_master)
                said = results_step.finish_interrupted_copy(self.tree_folder, GAME)
                self.assertIn('completed' if expected == 'new' else 'discarded', said)
                self.assertEqual(self.staged(), [])
                self.assertEqual(self.pair(), self.new_pair if expected == 'new' else self.old_pair, label)
                results_on_file(self.tree_folder, GAME)                 # the accepted pair agrees with itself
                self.assert_the_next_job_gives_the_uninterrupted_bytes(label)

    def test_a_kill_or_a_failure_at_every_step_of_the_copy_never_leaves_a_mixed_pair(self):
        real_stage, real_put = results_step._stage, results_step._put_in_place
        steps = [('stage', 1, 'the results staged'), ('stage', 2, 'the ledger staged'),
                 ('put', 1, 'the results put in place'), ('put', 2, 'the ledger put in place')]
        cases = [(kind, number, label, moment, how) for kind, number, label in steps
                 for moment in (('before', 'half-way', 'after') if kind == 'stage' else ('before', 'after'))
                 for how in ('killed', 'failed')]
        self.assertEqual(len(cases), 20)
        for kind, number, label, moment, how in cases:
            name = f'{how} {moment} "{label}"'
            with self.subTest(case=name):
                self.restore()
                counts = {'stage': 0, 'put': 0}

                def planted():
                    """The planted interruption: a kill, or a failure the job survives."""
                    return Killed(name) if how == 'killed' else OSError(f'planted: {name}')

                def stage(path, data):
                    """Stage a file, interrupted at the chosen moment of the chosen call."""
                    counts['stage'] += 1
                    if kind == 'stage' and counts['stage'] == number:
                        if moment == 'before':
                            raise planted()
                        if moment == 'half-way':
                            path.write_bytes(data[:len(data) // 2])
                            raise planted()
                        real_stage(path, data)
                        raise planted()
                    real_stage(path, data)

                def put(staged, accepted):
                    """Put a staged file in place, interrupted at the chosen moment of the chosen call."""
                    counts['put'] += 1
                    if kind == 'put' and counts['put'] == number:
                        if moment == 'after':
                            real_put(staged, accepted)
                        raise planted()
                    real_put(staged, accepted)

                with mock.patch.object(results_step, '_stage', stage), mock.patch.object(results_step, '_put_in_place', put):
                    if how == 'killed':
                        with self.assertRaises(Killed):
                            fx.run_job(self.tree_folder)
                    else:
                        code, said = fx.run_job(self.tree_folder)
                        self.assertEqual(code, 1, said)
                        self.assertTrue(any('STOPPED by a fault' in line for line in said), said)
                master_now, ledger_now = self.pair()
                self.assertIn(master_now, (self.old_pair[0], self.new_pair[0]), 'the accepted results are never partial')
                self.assertIn(ledger_now, (self.old_pair[1], self.new_pair[1]), 'the accepted ledger is never partial')
                self.assertNotEqual((master_now, ledger_now), (self.old_pair[0], self.new_pair[1]),
                                    'the new ledger is never put beside the old results')
                self.assertFalse((self.tree_folder / job_lock.UPDATER_LOCK).exists(), 'the updater\'s lock is released')
                self.assert_the_next_job_gives_the_uninterrupted_bytes(name)
                self.assertEqual(self.staged(), [])


class TheExamplesOfSection72(fx.JobCase):
    """Specification 7.2, line for line; draw 1160 stands for the specification's 1600."""

    def established(self) -> Path:
        """A tree whose two variants already count: their eligibility draw is 1161 and 1161 is forecast."""
        tree = self.tree()
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(self.status(tree, 'TOY_A_V1').eligible_from, 1161)
        return tree

    def test_an_install_with_no_backlog(self):
        tree = self.established()
        before = fx.files_under(tree)
        self.add_variant(tree, 'TOY_NEW_V1', {'rotate': 9})
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        new_lines = fx.list_lines(tree, 'E_901', 'TOY_NEW_V1')
        self.assertEqual([l['content']['target'] for l in new_lines], list(range(fx.FIRST_TOY_TARGET, 1162)),
                         'the new variant is filled from its first target to 1160 and forecast for 1161')
        self.assertTrue(all(l['envelope']['target_result_on_file'] for l in new_lines[:-1]))
        self.assertFalse(new_lines[-1]['envelope']['target_result_on_file'])
        for name, data in before.items():
            if '/variants/' in name:
                self.assertEqual(fx.files_under(tree)[name], data, f'{name}: the others compute nothing')
        self.assertIn('E_901/TOY_NEW_V1', fx.report_text(tree, f'league/league_{GAME}_d01150.txt'),
                      'the reports are rebuilt with the new variant in them')
        self.assertEqual(self.status(tree, 'TOY_NEW_V1').eligible_from, 1161)
        self.source(1161, version=2)                                    # the next week: 1161 arrives
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        for name in ('TOY_A_V1', 'TOY_B_V1', 'TOY_NEW_V1'):
            self.assertEqual(fx.list_lines(tree, 'E_901', name, 'scores')[-1]['content']['target'], 1161)
            self.assertEqual(fx.list_lines(tree, 'E_901', name)[-1]['content']['target'], 1162)
        ledger = fx.ledger_lines(tree)
        self.assertEqual([line['content']['draw'] for line in ledger], [1161])
        self.assertEqual([member['state'] for member in ledger[0]['content']['cohort']], ['counted'] * 3)
        self.assertTrue((tree / 'results/research' / GAME / f'reports/league/league_{GAME}_d01161.txt').is_file())

    def test_an_install_with_six_draws_waiting(self):
        tree = self.established()
        self.add_variant(tree, 'TOY_NEW_V1', {'rotate': 9})
        self.source(LAST_IN_SOURCE)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        new_lines = fx.list_lines(tree, 'E_901', 'TOY_NEW_V1')
        made_before = [l['content']['target'] for l in new_lines if not l['envelope']['target_result_on_file']]
        self.assertEqual(made_before, [1161, 1167], 'it reuses the 1161 forecast just made; 1162 to 1166 were '
                                                    'computed with their results on file, and say so')
        self.assertEqual(self.status(tree, 'TOY_NEW_V1').eligible_from, 1167)
        ledger = fx.ledger_lines(tree)
        self.assertEqual([line['content']['draw'] for line in ledger], list(range(1161, 1167)))
        for line in ledger:
            self.assertEqual([member['variant'] for member in line['content']['cohort']],
                             ['E_901/TOY_A_V1', 'E_901/TOY_B_V1'], 'the two counted at all six; the new one at none')
        for draw in range(1161, 1167):
            league = fx.report_text(tree, f'league/league_{GAME}_d{draw:05d}.csv')
            self.assertIn('E_901/TOY_NEW_V1', league)
        exploratory = list(csv.reader(io.StringIO(fx.report_text(tree, f'ov1/ov1_exploratory_{GAME}.csv'))))
        counted_at = {row[0]: row[1] for row in exploratory if row and row[0].isdigit()}
        self.assertEqual(counted_at['1161'], '3', 'the exploratory score counts the new variant at 1161')

    def test_the_very_first_job_of_a_new_tree(self):
        tree = self.tree()
        self.source(LAST_IN_SOURCE)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        for name in ('TOY_A_V1', 'TOY_B_V1'):
            self.assertEqual([l['content']['target'] for l in fx.list_lines(tree, 'E_901', name)],
                             list(range(fx.FIRST_TOY_TARGET, 1168)))
            self.assertEqual([l['content']['target'] for l in fx.list_lines(tree, 'E_901', name, 'scores')],
                             list(range(fx.FIRST_TOY_TARGET, 1167)))
            self.assertEqual(self.status(tree, name).eligible_from, 1167)
        self.assertEqual(fx.ledger_lines(tree), [], 'no prevailing line: no variant had an eligibility draw yet')
        self.assertFalse((tree / 'results/research' / GAME / 'ov1/prevailing.jsonl').exists())
        for draw in range(1161, 1167):
            self.assertTrue((tree / 'results/research' / GAME / f'reports/league/league_{GAME}_d{draw:05d}.txt').is_file())
        self.assertIn('prevailing OV-1: starts at draw 1167', fx.report_text(tree, f'ov1/ov1_prevailing_{GAME}.txt'))

    def test_the_first_job_with_the_results_step_failing_absent_or_left_out(self):
        for case in ('failing', 'absent', 'left out'):
            with self.subTest(case=case):
                tree = self.tree(name=f'tree_{case.replace(" ", "_")}', with_source=(case != 'absent'))
                if case == 'failing':
                    (self.root / 'source/source_data' / f'{GAME}_results_master_ledger.csv').write_bytes(b'damaged\n')
                code, said = fx.run_job(tree, no_update=(case == 'left out'))
                self.assertEqual(code, 0, said)
                wanted = {'failing': 'the results step failed: nothing new was read', 'absent': 'names no tree to copy',
                          'left out': 'left out (--no-update)'}[case]
                self.assertTrue(any(wanted in line for line in said), said)
                self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1')[-1]['content']['target'], 1161,
                                 'history is filled and the next draw is forecast')
                self.assertIsNone(self.status(tree, 'TOY_A_V1').eligible_from, 'no eligibility draw is written')
                self.assertIn(reports.NOT_STARTED_TEXT, fx.report_text(tree, f'ov1/ov1_prevailing_{GAME}.txt'))
                self.assertIn(reports.NOT_STARTED_TEXT, fx.report_text(tree, f'next/next_draw_{GAME}_d01161.txt'))
                if case == 'failing':
                    shutil.rmtree(self.root / 'source')

    def test_qa_as_prods_mirror_keeps_a_copied_eligibility_draw_however_many_draws_arrive(self):
        tree = self.tree()
        for name in ('TOY_A_V1', 'TOY_B_V1'):                           # the status files that came with PROD's software
            write_status(fx.status_path(tree, 'E_901', name), 'E_901', name,
                         {GAME: GameStatus(eligible_from=1150, eligibility_recorded='in PROD; results on file through 1149')})
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(fx.ledger_lines(tree)[0]['content']['draw'], 1150)
        before = fx.status_path(tree, 'E_901', 'TOY_A_V1').read_bytes()
        self.source(LAST_AT_START + 100, version=2)                     # QA receives a hundred more draws
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(fx.status_path(tree, 'E_901', 'TOY_A_V1').read_bytes(), before)
        self.assertEqual([line['content']['draw'] for line in fx.ledger_lines(tree)], list(range(1150, 1261)))

    def test_two_trees_with_the_same_software_status_and_results_agree_line_for_line(self):
        first = self.tree(name='first')
        second = self.tree(name='second')
        self.source(LAST_IN_SOURCE)
        for tree in (first, second):
            fx.run_job(tree)
        self.source(LAST_IN_SOURCE + 3, version=3)
        for tree in (first, second):
            self.assertEqual(fx.run_job(tree)[0], 0)
        self.assertEqual([line['content'] for line in fx.ledger_lines(first)],
                         [line['content'] for line in fx.ledger_lines(second)])
        self.assertEqual(len(fx.ledger_lines(first)), 3)
        for which in ('forecasts', 'scores'):
            self.assertEqual([l['content'] for l in fx.list_lines(first, 'E_901', 'TOY_A_V1', which)],
                             [l['content'] for l in fx.list_lines(second, 'E_901', 'TOY_A_V1', which)])
        self.assertNotEqual(fx.ledger_lines(first)[0]['envelope']['computed_in'],
                            fx.ledger_lines(second)[0]['envelope']['computed_in'],
                            'each line still says truthfully where it was computed')


class TheResultsStep(fx.JobCase):
    """Specification 7.1: results that changed other than by growing; nothing ever starts the updater."""

    def test_results_changed_other_than_by_growing_refuse_the_game_and_name_the_draw(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        before = fx.files_under(tree)
        fx.write_results(tree, GAME, LAST_AT_START, reseed_from=1155)   # the same length, changed from 1155 on
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 1)
        self.assertTrue(any('results changed other than by growing: draw 1155' in line for line in said), said)
        self.assertEqual(fx.files_under(tree), before)
        fx.write_results(tree, GAME, 1158)                              # shorter than the lists reach
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 1)
        self.assertTrue(any('results changed other than by growing' in line and 'end at draw 1158' in line
                            for line in said), said)

    def test_a_source_that_is_not_these_results_grown_longer_is_refused_and_nothing_is_copied(self):
        tree = self.tree()
        self.source(LAST_IN_SOURCE, reseed_from=1150)
        master = tree / 'source_data' / f'{GAME}_results_master.csv'
        before = master.read_bytes()
        code, said = fx.run_job(tree)
        self.assertEqual(code, 1)
        self.assertTrue(any('results changed other than by growing' in line and 'draw 1150' in line for line in said), said)
        self.assertEqual(master.read_bytes(), before)

    def test_the_source_tree_is_only_read(self):
        tree = self.tree()
        self.source(LAST_IN_SOURCE)
        before = fx.files_under(self.root / 'source', folder='.')
        fx.run_job(tree)
        self.assertEqual(fx.files_under(self.root / 'source', folder='.'), before)

    def test_prod_leaves_the_results_step_out_until_its_updater_launch_exists(self):
        tree = self.tree(role='PROD', with_source=False)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('arrives with build step 3' in line for line in said), said)
        self.assertIsNone(self.status(tree, 'TOY_A_V1').eligible_from)

    def test_the_engine_starts_no_program_and_opens_no_connection(self):
        engine = sorted((REPOSITORY_ROOT / 'src' / 'research').glob('*.py')) + [REPOSITORY_ROOT / 'src' / 'research_command.py']
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
            for word in ('Run_Results_Updater', 'results_master_v0', 'lotterywest', 'thelott'):
                self.assertNotIn(word.lower(), text.lower(), f'{path.name} names {word}')


class Reports(fx.JobCase):
    """Specification 9: reports are a function of the lists, the results and the status files alone."""

    def test_the_same_records_give_the_same_report_bytes(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        first = fx.files_under(tree, f'results/research/{GAME}/reports')
        code, said = fx.run_job(tree, no_update=True)
        self.assertTrue(any('0 report files' in line for line in said), said)
        shutil.rmtree(tree / 'results/research' / GAME / 'reports')
        fx.run_job(tree, no_update=True)
        self.assertEqual(fx.files_under(tree, f'results/research/{GAME}/reports'), first)

    def test_an_eligibility_draw_written_at_the_end_of_a_job_shows_in_that_jobs_league_reports(self):
        tree = self.tree()
        code, said = fx.run_job(tree)                                   # this job writes eligibility draws 1161
        self.assertEqual(code, 0, said)
        for draw in (fx.FIRST_TOY_TARGET, LAST_AT_START):
            rows = list(csv.reader(io.StringIO(fx.report_text(tree, f'league/league_{GAME}_d{draw:05d}.csv'))))
            header = next(row for row in rows if row and row[0] == 'order_top')
            row = dict(zip(header, next(row for row in rows if len(row) > 1 and row[1] == 'E_901/TOY_A_V1')))
            self.assertEqual(row['prevailing_ov1_first_draw'], str(LAST_AT_START + 1), draw)
        code, said = fx.run_job(tree)
        self.assertTrue(any('0 report files' in line for line in said), 'the next job finds every report as it would make it')

    def test_a_changed_report_formatter_leaves_no_file_of_the_old_format_in_the_active_folder(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        with mock.patch.object(reports, 'LEAGUE_HEADLINE', 'A NEW HEADLINE. It selects nothing.'):
            fx.run_job(tree, no_update=True)
        league = sorted((tree / 'results/research' / GAME / 'reports/league').iterdir())
        self.assertEqual(len(league), 2 * (LAST_AT_START - fx.FIRST_TOY_TARGET + 1))
        for path in league:
            self.assertIn('A NEW HEADLINE', path.read_text(encoding='ascii'), path.name)

    def test_the_league_figures_are_those_of_the_score_list(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        scores = fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores')
        through = [s['content'] for s in scores if s['content']['target'] <= 1155]
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
        self.assertEqual(row[f'top_last_{reports.LAST_DRAWS_SHOWN}'],
                         ''.join(str(s['matches']['MAIN']['top']) for s in through[-reports.LAST_DRAWS_SHOWN:]))
        text = fx.report_text(tree, f'league/league_{GAME}_d01155.txt')
        for wanted in (reports.LEAGUE_HEADLINE, reports.REBUILT_NOTE, f'the QA tree at {tree}', 'Runs to draw: 1155',
                       'Variants: 2', 'Foreign lists ignored: none'):
            self.assertIn(wanted, text)

    def test_the_next_draw_report_shows_each_forecast_as_its_list_holds_it(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        forecast = fx.list_lines(tree, 'E_901', 'TOY_A_V1')[-1]['content']
        self.assertEqual(forecast['target'], 1161)
        rows = list(csv.reader(io.StringIO(fx.report_text(tree, f'next/next_draw_{GAME}_d01161.csv'))))
        row = next(row for row in rows if row and row[0] == 'E_901/TOY_A_V1')
        self.assertEqual(row[1], 'FORECAST')
        self.assertEqual(row[2], ' '.join(str(n) for n in sorted(forecast['barrels']['MAIN']['top'])))
        self.assertEqual(row[3], ' '.join(str(n) for n in sorted(forecast['barrels']['MAIN']['worst'])))
        self.assertEqual(row[6], 'yes')

    def test_the_time_of_making_is_in_the_side_file_and_in_no_report(self):
        tree = self.tree()
        fx.run_job(tree, no_update=True)
        made = fx.FIXED_TIME.astimezone().strftime('%Y-%m-%d %H:%M')
        times = fx.report_text(tree, reports.MADE_TIMES_NAME)
        self.assertIn(f'league/league_{GAME}_d01160.txt,{made}', times)
        for name, data in fx.files_under(tree, f'results/research/{GAME}/reports').items():
            self.assertNotIn(made.encode('ascii'), data, name)


class StartingAndStopping(fx.JobCase):
    """Specification 15 and 16: the refusals before any game, and the games kept apart."""

    def test_an_orphan_marker_blocks_the_launch(self):
        tree = self.tree()
        marker = tree / job_lock.ORPHAN_MARKER
        marker.parent.mkdir(parents=True)
        marker.write_text('{}', encoding='ascii')
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 2)
        self.assertTrue(any('REFUSED: orphan marker present' in line for line in said), said)
        self.assertFalse((tree / 'results').exists())
        self.assertTrue(marker.is_file(), 'the job never clears the marker')

    def test_a_job_lock_that_exists_refuses_and_is_never_removed_by_another_job(self):
        tree = self.tree()
        lock = tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME
        lock.parent.mkdir(exist_ok=True)
        lock.write_text('research job; started earlier\n', encoding='ascii')
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 2)
        self.assertTrue(any('a process of this tree is running' in line and 'delete that one file by hand' in line
                            for line in said), said)
        self.assertTrue(lock.is_file())
        lock.unlink()
        self.assertEqual(fx.run_job(tree, no_update=True)[0], 0)
        self.assertFalse(lock.exists(), 'a finished job leaves no lock')

    def test_a_tree_that_is_not_what_its_settings_say_refuses(self):
        tree = self.tree()
        moved = self.root / 'moved'
        shutil.copytree(tree, moved)
        code, said = fx.run_job(moved, no_update=True)
        self.assertEqual(code, 2)
        self.assertTrue(any('This tree is not what its file says' in line for line in said), said)

    def test_only_limits_the_job_to_the_named_variants_and_an_unknown_name_refuses(self):
        tree = self.tree()
        code, said = fx.run_job(tree, no_update=True, only=['E_901/TOY_A_V1'])
        self.assertEqual(code, 0, said)
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1'), [])
        self.assertEqual(len(fx.list_lines(tree, 'E_901', 'TOY_A_V1')), LAST_AT_START + 1 - fx.FIRST_TOY_TARGET + 1)
        code, said = fx.run_job(tree, no_update=True, only=['E_901/NO_SUCH_V1'])
        self.assertEqual(code, 2)
        self.assertTrue(any('--only names no variant of this tree: E_901/NO_SUCH_V1' in line for line in said), said)

    def test_the_games_are_worked_apart_and_one_refusing_leaves_the_other_finished(self):
        tree = self.tree(variants=(), with_source=False)
        fx.write_results(tree, 'OZLOTTO', 1560)
        self.add_variant(tree, 'TOY_A_V1', games=('POWERBALL', 'OZLOTTO'))
        code, said = fx.run_job(tree, games=('POWERBALL', 'OZLOTTO'), no_update=True)
        self.assertEqual(code, 0, said)
        oz = fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores', game_id='OZLOTTO')
        self.assertIn('supplementary_matches', oz[0]['content'])
        self.assertEqual(sorted(oz[0]['content']['matches']), ['MAIN'])
        self.assertTrue((tree / 'results/research/OZLOTTO/reports/league').is_dir())
        fx.write_results(tree, 'OZLOTTO', 1560, reseed_from=1500)
        code, said = fx.run_job(tree, games=('POWERBALL', 'OZLOTTO'), no_update=True)
        self.assertEqual(code, 1)
        self.assertTrue(any(line.startswith('POWERBALL: finished.') for line in said), said)
        self.assertTrue(any(line.startswith('OZLOTTO: REFUSED: OZLOTTO: results changed other than by growing')
                            for line in said), said)
        self.assertEqual(said[-1], 'A STOP is a STOP: at least one game did not finish; nothing retries by itself.')

    def test_dev_creates_a_missing_status_file_and_qa_refuses_one_naming_the_file(self):
        dev = self.tree(role='DEV', with_source=False, name='dev')
        fx.status_path(dev, 'E_901', 'TOY_A_V1').unlink()
        code, said = fx.run_job(dev, no_update=True)
        self.assertEqual(code, 0, said)
        self.assertEqual(self.status(dev, 'TOY_A_V1'), GameStatus())
        qa = self.tree(name='qa')
        fx.status_path(qa, 'E_901', 'TOY_A_V1').unlink()
        code, said = fx.run_job(qa, no_update=True)
        self.assertEqual(code, 1)
        self.assertTrue(any('a status file fails its check' in line and 'the status file is missing' in line
                            and str(fx.status_path(qa, 'E_901', 'TOY_A_V1')) in line for line in said), said)

    def test_a_hand_edited_status_file_refuses_the_game_and_names_the_file(self):
        tree = self.tree()
        path = fx.status_path(tree, 'E_901', 'TOY_B_V1')
        path.write_bytes(path.read_bytes().replace(b'status = ACTIVE', b'status = WITHDRAWN'))
        code, said = fx.run_job(tree, no_update=True)
        self.assertEqual(code, 1)
        self.assertTrue(any('REFUSED' in line and str(path) in line for line in said), said)
        self.assertFalse((tree / 'results').exists())

    def test_in_dev_an_unfinished_variant_folder_is_named_and_left_out_and_in_qa_it_refuses_the_job(self):
        for role, expected in (('DEV', 0), ('QA', 2)):
            with self.subTest(role=role):
                tree = self.tree(role=role, with_source=False, name=f'tree_{role}')
                (tree / 'src/methods/E_901/TOY_B_V1/method.py.bak').write_text('an editor backup\n', encoding='ascii')
                code, said = fx.run_job(tree, no_update=True)
                self.assertEqual(code, expected, said)
                self.assertTrue(any('E_901/TOY_B_V1' in line and 'method.py.bak' in line for line in said), said)
                self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_B_V1'), [])


class TheCommandProgram(fx.JobCase):
    """src/research_command.py, the one program behind the launchers."""

    def test_an_unknown_command_is_refused(self):
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            self.assertEqual(research_command.run_command(['tidy']), research_command.EXIT_BAD_COMMAND)
        self.assertIn('the first word must be one of', printed.getvalue())

    def installed_tree(self) -> Path:
        """An invented tree that holds the engine's own files, as an installed tree does."""
        tree = self.tree(role='DEV', with_source=False)
        for folder in ('research', 'evaluation'):
            shutil.copytree(REPOSITORY_ROOT / 'src' / folder, tree / 'src' / folder,
                            ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(REPOSITORY_ROOT / 'src/methods/_common', tree / 'src/methods/_common',
                        ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy(REPOSITORY_ROOT / 'src/research_command.py', tree / 'src/research_command.py')
        shutil.copy(REPOSITORY_ROOT / 'deploy/INFRA_MANIFEST.ini', tree / 'deploy/INFRA_MANIFEST.ini')
        for name in ('Run_Research.bat', 'Withdraw_Variant.bat'):
            shutil.copy(REPOSITORY_ROOT / name, tree / name)
        return tree

    def launch(self, tree: Path, *arguments) -> subprocess.CompletedProcess:
        """Start the command program as a launcher does: this Python, isolated, writing no cache."""
        return subprocess.run([sys.executable, '-I', '-B', str(tree / 'src/research_command.py'), *arguments],
                              capture_output=True, text=True, timeout=300, cwd=str(self.root))

    def test_a_python_that_is_not_the_trees_own_environment_is_refused(self):
        tree = self.installed_tree()
        done = self.launch(tree, 'research', '--game', GAME, '--no-update')
        self.assertEqual(done.returncode, research_command.EXIT_BAD_COMMAND, done.stdout + done.stderr)
        self.assertIn('REFUSED: the Python running is', done.stdout)
        self.assertFalse((tree / 'results').exists())
        self.assertEqual(list((tree / 'src').rglob('__pycache__')), [], 'started this way Python writes no cache')

    def test_with_the_trees_own_python_the_command_runs_the_job_in_the_tree_the_program_lies_in(self):
        tree = self.tree(role='DEV', with_source=False)
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
        self.assertEqual(fx.list_lines(tree, 'E_901', 'TOY_A_V1')[-1]['content']['target'], LAST_AT_START + 1)


class TheManifestListsTheLaunchers(unittest.TestCase):
    """Deployment design section 2: the launchers of a tree are infrastructure."""

    def test_the_two_launchers_and_the_command_program_are_on_the_manifest_as_other(self):
        from research.code_identity import read_manifest
        manifest = read_manifest(REPOSITORY_ROOT)
        for name in ('Run_Research.bat', 'Withdraw_Variant.bat', 'src/research_command.py'):
            self.assertEqual(manifest.get(name), 'other', name)

    def test_each_launcher_names_its_command_and_runs_python_isolated_without_a_cache(self):
        for name, command in (('Run_Research.bat', 'research'), ('Withdraw_Variant.bat', 'withdraw')):
            text = (REPOSITORY_ROOT / name).read_bytes().decode('ascii')
            self.assertIn(f'"%PY%" -I -B -u "%TOOL%" {command} %*\r\n', text, name)
            self.assertEqual(text.count('\r\n'), text.count('\n'), f'{name}: CRLF line endings throughout')


if __name__ == '__main__':
    unittest.main()
