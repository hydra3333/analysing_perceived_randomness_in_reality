"""Tests of slice S1 of the reporting work: the print-outs moved out of the engine, the science identity, and
Run_Reports.bat without a research job.

Each test is named for the rule it proves and plants the fault that rule must catch. All on invented draws; no
test lets the real updater run.
(doc/Predictive_Randomness_Reporting_Design_And_Specification_Amendment_A1_v0_5.md, RAT-74, A2, A11 and A12;
the code plan v0.2 sections 3 and 10, with the reviewer's C03; decision log entries 426 and 428.)
"""
import hashlib
import json
import shutil
import unittest
from pathlib import Path
from unittest import mock

import research_fixtures as fx
from reporting import report_job
from research import code_identity, method_flags, science_identity

GAMES = ('POWERBALL', 'OZLOTTO')
# The invented history of the same-bytes test: last draws on file at the first and the second job, and the
# retirement made between them.
FIRST_LAST = {'POWERBALL': 1160, 'OZLOTTO': 1490}
SECOND_LAST = {'POWERBALL': 1164, 'OZLOTTO': 1494}
RETIRED_FROM = {'POWERBALL': 1163, 'OZLOTTO': 1493}
# The SHA-256 over the sorted lines '<file><TAB><sha256 of its bytes, the tree's path as <TREE>><LF>' of every
# report and series file that history gives. It was made once, with the engine as it was before S1 (commit
# 7b30d26), and S1's moved code must give the same: 94 files, the league, next-draw and OV-1 print-outs and the
# README of both games, and both games' series. A later slice that changes a report on purpose changes it here.
BEFORE_S1 = ('c3ec383e866796dde073e56df0448d68808353cba8e0cdb8cde488e078451ef1', 94)


def report_and_series_files(tree: Path) -> dict:
    """{path from the tree: sha256} of every report and series file of both games, the tree's own path in the
    files replaced by <TREE> (every report names the tree that made it)."""
    found = {}
    for game_id in GAMES:
        for folder in ('reports', 'ov1'):
            for name, data in fx.files_under(tree, f'results/research/{game_id}/{folder}').items():
                found[name] = hashlib.sha256(data.replace(str(tree).encode(), b'<TREE>')).hexdigest()
    return found


def combined(found: dict) -> tuple:
    """(one SHA-256 over the sorted name and digest lines, how many files)."""
    text = ''.join(f'{name}\t{digest}\n' for name, digest in sorted(found.items()))
    return hashlib.sha256(text.encode('utf-8')).hexdigest(), len(found)


def run_reports(tree: Path, games=GAMES) -> tuple:
    """Run Run_Reports.bat's program in an invented tree at the fixed time. Returns (exit code, lines said)."""
    said = []
    with fx.ImportPath(tree):
        code = report_job.run_reports(tree, games, now=lambda: fx.FIXED_TIME, say=said.append)
    return code, said


class TheMove(fx.JobCase):
    """S1 is a pure move: every report comes out with the same bytes as before it, and the engine no longer
    makes or deletes reports itself."""

    def history(self) -> Path:
        """The invented history of BEFORE_S1: three methods in both games, two jobs, and a retirement between
        them, so that the league, next-draw reports, both OV-1 series and a retired method are all exercised."""
        tree = fx.make_tree(self.root / 'same_bytes')
        for game_id in GAMES:
            fx.write_results(tree, game_id, FIRST_LAST[game_id])
        fx.add_toy_variant(tree, 'E_901', 'TOY_A_V1')
        fx.add_toy_variant(tree, 'E_901', 'TOY_B_V1', behaviour={'reverse': True})
        fx.add_toy_variant(tree, 'E_902', 'TOY_C_V1', minimum=5, behaviour={'rotate': 3})
        code, said = fx.run_job(tree, games=GAMES)
        self.assertEqual(code, 0, said)
        for game_id in GAMES:
            fx.write_results(tree, game_id, SECOND_LAST[game_id])
        method_flags.write_retired(fx.method_folder(tree, 'E_902', 'TOY_C_V1'), RETIRED_FROM,
                                   'an invented retirement for the test')
        code, said = fx.run_job(tree, games=GAMES)
        self.assertEqual(code, 0, said)
        return tree

    def test_every_report_has_the_same_bytes_as_before_the_move(self):
        tree = self.history()
        self.assertEqual(combined(report_and_series_files(tree)), BEFORE_S1)

    def test_run_reports_alone_makes_the_same_report_bytes_as_the_job(self):
        tree = self.history()
        made_by_the_job = report_and_series_files(tree)
        for game_id in GAMES:
            shutil.rmtree(tree / 'results/research' / game_id / 'reports')
        code, said = run_reports(tree)
        self.assertEqual(code, report_job.EXIT_DONE, said)
        self.assertEqual(report_and_series_files(tree), made_by_the_job)

    def test_an_engine_rebuild_leaves_the_reports_folder_to_the_reporting_part(self):
        tree = self.tree()
        fx.run_job(tree)
        keep = tree / 'results/research' / fx.GAME / 'reports' / 'KEEP_ME.txt'
        keep.write_bytes(b'a file the reporting part did not make\r\n')
        code, said = fx.run_job(tree, rebuild_all=True)
        self.assertEqual(code, 0, said)
        self.assertTrue(any('REBUILT' in line and 'everything' in line for line in said), said)
        self.assertTrue(keep.is_file(), 'the engine deleted the reports folder')

    def test_a_fault_in_the_reporting_part_leaves_the_science_and_ends_not_cleanly(self):
        tree = self.tree()
        with mock.patch.object(report_job, 'make_reports', side_effect=RuntimeError('a planted fault')):
            code, said = fx.run_job(tree)
        self.assertEqual(code, 1, said)
        self.assertTrue(any('THE REPORTS WERE NOT MADE' in line and 'a planted fault' in line for line in said), said)
        self.assertTrue(fx.list_lines(tree, 'E_901', 'TOY_A_V1', 'scores'), 'the scores stand')
        self.assertIsNotNone(science_identity.read_identity(tree, fx.GAME), 'the identity stands')
        code, said = run_reports(tree, (fx.GAME,))
        self.assertEqual(code, report_job.EXIT_DONE, said)

    def test_the_reporting_part_is_not_part_of_the_engines_fingerprint_but_has_its_own(self):
        tree = self.tree()
        engine, reporting = code_identity.infrastructure_fingerprint(tree), code_identity.reporting_fingerprint(tree)
        (tree / 'src' / 'reporting').mkdir()
        (tree / 'src' / 'reporting' / 'printouts.py').write_text('# an invented print-out\n', encoding='ascii')
        self.assertEqual(code_identity.infrastructure_fingerprint(tree), engine)
        self.assertNotEqual(code_identity.reporting_fingerprint(tree), reporting)
        self.assertEqual(code_identity.reporting_files(tree), ['src/reporting/printouts.py'])


class TheScienceIdentity(fx.JobCase):
    """The reviewer's C03: what each game's stored science was made from is written by the job when, and only
    when, the game's scientific work has finished; the reporting part makes nothing unless it still holds."""

    def test_it_is_written_when_a_game_finishes_with_the_engine_and_every_methods_status(self):
        tree = self.tree()
        method_flags.write_retired(fx.method_folder(tree, 'E_901', 'TOY_B_V1'), {fx.GAME: 1158},
                                   'an invented reason')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        stored = science_identity.read_identity(tree, fx.GAME)
        self.assertEqual(stored['engine_fingerprint'], code_identity.infrastructure_fingerprint(tree))
        self.assertIn(science_identity.BLOCKED_KEY, stored)
        self.assertIsNone(stored[science_identity.BLOCKED_KEY], 'no block is an explicit null')
        methods = {method['identity']: method for method in stored['methods']}
        self.assertEqual((methods['E_901/TOY_B_V1']['retired_from'], methods['E_901/TOY_B_V1']['retired_reason']),
                         (1158, 'an invented reason'))
        self.assertEqual(methods['E_901/TOY_A_V1']['last_scored'], fx.LAST_AT_START)
        self.assertEqual(methods['E_901/TOY_A_V1']['last_target'], fx.LAST_AT_START + 1)
        raw = science_identity.identity_path(tree, fx.GAME).read_bytes()
        self.assertTrue(raw.endswith(b'\r\n') and b'\n' not in raw.replace(b'\r\n', b''), 'CRLF, the standard')

    def test_a_missing_blocked_key_is_not_an_identity(self):
        tree = self.tree()
        fx.run_job(tree)
        path = science_identity.identity_path(tree, fx.GAME)
        document = json.loads(path.read_bytes())
        del document[science_identity.BLOCKED_KEY]
        path.write_bytes(json.dumps(document).encode('ascii'))
        self.assertIsNone(science_identity.read_identity(tree, fx.GAME))
        code, said = run_reports(tree, (fx.GAME,))
        self.assertEqual(code, report_job.EXIT_REFUSED, said)
        self.assertTrue(any('there is no record of what its stored science was made from' in line for line in said))

    def test_a_game_that_stops_leaves_no_identity(self):
        tree = self.tree()
        fx.run_job(tree)
        self.assertIsNotNone(science_identity.read_identity(tree, fx.GAME))
        (tree / 'source_data' / f'{fx.GAME}_results_master.csv').write_bytes(b'not a results file\n')
        code, said = fx.run_job(tree)
        self.assertEqual(code, 1, said)
        self.assertTrue(any('STOPPED' in line for line in said), said)
        self.assertIsNone(science_identity.read_identity(tree, fx.GAME))

    def test_a_corrected_supplementary_number_is_refused_until_the_job_has_run(self):
        tree = fx.make_tree(self.root / 'oz')
        fx.write_results(tree, 'OZLOTTO', 1490)
        fx.add_toy_variant(tree, 'E_901', 'TOY_A_V1', games=('OZLOTTO',))
        code, said = fx.run_job(tree, games=('OZLOTTO',))
        self.assertEqual(code, 0, said)
        results = tree / 'source_data' / 'OZLOTTO_results_master.csv'
        rows = results.read_bytes().split(b'\n')
        fields = rows[-2].split(b',')                     # the last draw; its last field is a supplementary number
        main_and_supplementary = {int(field) for field in fields[2:]}
        fields[-1] = str(next(n for n in range(1, 48) if n not in main_and_supplementary)).encode('ascii')
        rows[-2] = b','.join(fields)
        fx.write_results(tree, 'OZLOTTO', 1490)            # the version ledger, then the corrected bytes over it
        results.write_bytes(b'\n'.join(rows))
        ledger = tree / 'source_data' / 'OZLOTTO_results_master_ledger.csv'
        lines = ledger.read_bytes().split(b'\n')
        cells = lines[1].split(b',')
        cells[3] = hashlib.sha256(results.read_bytes()).hexdigest().encode('ascii')
        lines[1] = b','.join(cells)
        ledger.write_bytes(b'\n'.join(lines))
        reports_before = report_and_series_files(tree)
        code, said = run_reports(tree, ('OZLOTTO',))
        self.assertEqual(code, report_job.EXIT_REFUSED, said)
        self.assertTrue(any('the accepted results file' in line for line in said), said)
        self.assertEqual(report_and_series_files(tree), reports_before, 'a refused game is left as it was')
        code, said = fx.run_job(tree, games=('OZLOTTO',))
        self.assertEqual(code, 0, said)
        code, said = run_reports(tree, ('OZLOTTO',))
        self.assertEqual(code, report_job.EXIT_DONE, said)

    def test_a_changed_score_list_is_refused_until_the_job_has_run(self):
        tree = self.tree()
        fx.run_job(tree)
        scores = tree / 'results/research' / fx.GAME / 'variants' / 'E_901' / 'TOY_A_V1' / 'scores.jsonl'
        fx.alter_list_line(scores, 2, lambda line: line['content']['matches']['MAIN'].update(top=7))
        code, said = run_reports(tree, (fx.GAME,))
        self.assertEqual(code, report_job.EXIT_REFUSED, said)
        self.assertTrue(any('E_901/TOY_A_V1: scores' in line for line in said), said)
        code, said = fx.run_job(tree)
        self.assertEqual(code, 0, said)
        self.assertEqual(run_reports(tree, (fx.GAME,))[0], report_job.EXIT_DONE)

    def test_a_method_installed_since_the_last_job_is_refused_until_the_job_has_run(self):
        tree = self.tree()
        fx.run_job(tree)
        self.add_variant(tree, 'TOY_NEW_V1')
        code, said = run_reports(tree, (fx.GAME,))
        self.assertEqual(code, report_job.EXIT_REFUSED, said)
        self.assertTrue(any('E_901/TOY_NEW_V1: a method now installed' in line for line in said), said)

    def test_one_game_refused_and_one_made_is_incomplete(self):
        tree = fx.make_tree(self.root / 'both')
        for game_id in GAMES:
            fx.write_results(tree, game_id, FIRST_LAST[game_id])
        fx.add_toy_variant(tree, 'E_901', 'TOY_A_V1')
        fx.run_job(tree, games=GAMES)
        science_identity.remove_identity(tree, 'OZLOTTO')
        code, said = run_reports(tree)
        self.assertEqual(code, report_job.EXIT_INCOMPLETE, said)
        self.assertTrue(any(line.startswith('POWERBALL: reports made') for line in said), said)
        self.assertTrue(any(line.startswith('OZLOTTO: REFUSED') for line in said), said)


if __name__ == '__main__':
    unittest.main()
