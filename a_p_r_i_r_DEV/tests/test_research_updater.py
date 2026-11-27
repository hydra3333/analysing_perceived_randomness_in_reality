"""Tests of the results updater and of the research job's use of it. No test reaches a website: every update here
reads invented pages, and the class that starts a real browser is replaced by one that refuses.

Each test is named for the rule it proves and plants the fault that rule must catch.
(The simple scheme v0.2 sections 8 and 5 step 3; the owner's four points of decision log entry 356.)
"""
import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

TREE_OF_THIS_FILE = Path(__file__).resolve().parents[1]
if str(TREE_OF_THIS_FILE / 'deploy') not in sys.path:
    sys.path.insert(0, str(TREE_OF_THIS_FILE / 'deploy'))

import compare_updater_with_frozen as compare               # noqa: E402  (after the path line above)
import research_command                                     # noqa: E402
import research_fixtures as fx                              # noqa: E402
from research import code_identity, job_lock, research_job  # noqa: E402

# The updater under test, loaded from its file with its real fetcher replaced by one that refuses.
updater = compare.load(compare.NEW_FILE, 'updater_under_test')
TODAY, HELD = compare.TODAY, compare.HELD
# The last draw dated on or before TODAY in each game, by the weekly rule: what an update on TODAY brings a tree to
# (Powerball 1600, Oz Lotto 1718).
LATEST = {game: max(n for n in range(era.first_draw, era.first_draw + 600) if updater.derived_date(game, n) <= TODAY)
          for game, era in updater.ERAS.items()}


def update(tree: Path, games=('POWERBALL', 'OZLOTTO'), months_back: int = 5, plant=None, pause: float = 2.0):
    """Run the updater's update in a tree on invented pages. Returns the exit code; a refusal is raised."""
    with contextlib.redirect_stdout(io.StringIO()):
        return updater.cmd_update(tree, list(games), months_back, 'chrome', pause,
                                  fetcher_factory=lambda: compare.InventedPages(updater, plant), today=TODAY)


class WithATree(unittest.TestCase):
    """A temporary tree that holds nothing but invented results: no owner record, no seal, nothing of Mode H."""

    def setUp(self):
        """Make the tree: both games' results files and ledgers, written by the updater's own functions."""
        self._temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary.cleanup)
        self.tree = compare.make_tree(updater, Path(self._temporary.name).resolve(), HELD, frozen=False)

    def held(self, game: str) -> tuple:
        """(the results file's bytes, the ledger's lines) of a game in the tree."""
        store = updater.Store(self.tree, game)
        return store.master.read_bytes(), store.ledger_rows()


class TheRules(unittest.TestCase):
    """The pure rules: windows, dates, a draw's validity, the one official host."""

    def test_the_window_runs_from_the_first_of_an_earlier_month_to_today_and_is_searched_in_overlapping_parts(self):
        self.assertEqual(updater.month_window(date(2027, 3, 15), 5), (date(2026, 10, 1), date(2027, 3, 15)))
        self.assertEqual(updater.month_window(date(2027, 3, 15), 0), (date(2027, 3, 1), date(2027, 3, 15)))
        for bad in (-1, 61):
            with self.assertRaises(updater.Refused):
                updater.month_window(date(2027, 3, 15), bad)
        windows = updater.split_windows(date(2022, 1, 1), date(2027, 1, 10))
        self.assertTrue(windows[0][0] < date(2022, 1, 1) and windows[-1][1] == date(2027, 1, 10))
        self.assertTrue(all(later[0] < earlier[1] for earlier, later in zip(windows, windows[1:])), 'they overlap')
        for game in updater.ERAS:
            for a, b in windows:
                self.assertLess(len([n for n in range(updater.ERAS[game].first_draw, 3000)
                                     if a < updater.derived_date(game, n) < b]), 100, 'under the page\'s limit')

    def test_a_draw_is_checked_for_its_weekday_its_numbers_and_its_game(self):
        good = updater.Draw('POWERBALL', 1600, '2027-01-14', (1, 2, 3, 4, 5, 6, 7), (9,))
        self.assertEqual(updater.validate_draw(good), [])
        for bad in (updater.Draw('POWERBALL', 1600, '2027-01-15', good.main, good.secondary),       # a Friday
                    updater.Draw('POWERBALL', 1600, '2027-01-14', (1, 2, 3, 4, 5, 6, 6), good.secondary),
                    updater.Draw('POWERBALL', 1600, '2027-01-14', (1, 2, 3, 4, 5, 6, 36), good.secondary),
                    updater.Draw('POWERBALL', 1600, '2027-01-14', good.main, (21,)),
                    updater.Draw('POWERBALL', 1100, '2027-01-14', good.main, good.secondary),       # before the game's first
                    updater.Draw('OZLOTTO', 1717, '2027-01-12', (1, 2, 3, 4, 5, 6, 7), (7, 8, 9))):     # a supplementary repeats a main
            with self.assertRaises(updater.VerifyFail, msg=bad):
                updater.validate_draw(bad)
        self.assertEqual(len(updater.validate_draw(updater.Draw('POWERBALL', 1600, '2027-01-21', good.main, (9,)))), 1,
                         'a date off the weekly rule is a warning')

    def test_a_draw_of_any_date_is_an_ordinary_draw_there_is_no_quarantine(self):
        for game, number in (('POWERBALL', 1577), ('OZLOTTO', 1694), ('POWERBALL', 1700)):
            main, secondary = compare.invented_draw(game, number)
            draw = updater.Draw(game, number, updater.derived_date(game, number).isoformat(), tuple(main), tuple(secondary))
            self.assertEqual(updater.validate_draw(draw), [], (game, number))
        source = compare.NEW_FILE.read_text(encoding='ascii')
        code = source[source.index('from __future__'):]
        for word in ('quarantine', 'holdout', 'MODE_H', 'freeze', 'ACTIVE_SESSION', 'results/real', '"results"'):
            self.assertNotIn(word.lower(), code.lower(), f'the updater\'s code still names {word}')

    def test_only_https_on_exactly_the_official_host_passes_and_there_is_no_fallback(self):
        updater.check_final_url('https://www.lotterywest.wa.gov.au/results/powerball?fromDate=x')
        updater.check_final_url('HTTPS://WWW.LOTTERYWEST.WA.GOV.AU/results')
        for bad in ('http://www.lotterywest.wa.gov.au/results', 'https://oz.lotterywest.com/results',
                    'https://lotterywest.wa.gov.au/results', 'https://www.lotterywest.wa.gov.au.example.net/x',
                    'https://www.thelott.com/powerball/results', 'https://user@evil.example/www.lotterywest.wa.gov.au',
                    '', 'about:blank', 'data:text/html,x'):
            with self.assertRaises(updater.Refused, msg=bad):
                updater.check_final_url(bad)
        with self.assertRaisesRegex(updater.Refused, r'oz\.lotterywest\.com.*no fallback'):
            updater.check_final_url('https://oz.lotterywest.com/results')
        for game in updater.ERAS:
            updater.check_final_url(updater.gov_url(game, date(2026, 1, 1), date(2026, 1, 31)))

    def test_no_test_can_start_a_real_browser(self):
        with self.assertRaisesRegex(RuntimeError, 'never starts a browser'):
            updater.BrowserFetcher('chrome', 2.0)

    @unittest.skipUnless(importlib.util.find_spec('selenium'), 'selenium is not in this environment')
    def test_a_page_that_is_somewhere_else_once_it_has_loaded_is_refused_before_anything_is_parsed(self):
        # The real fetcher's own fetch, driven by a stand-in for the browser: its __init__, which starts the
        # browser, is never run, so nothing is started and nothing is requested.
        spec = importlib.util.spec_from_file_location('updater_with_its_fetcher', compare.NEW_FILE)
        real = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = real
        spec.loader.exec_module(real)
        a, b = date(2026, 12, 1), date(2027, 1, 20)

        class Body:
            """The page's body: the text of an invented results page."""
            text = compare.page_text(real, 'POWERBALL', a, b)

        class Browser:
            """A stand-in for the browser: it loads nothing, and says where it is each time it is asked."""
            title = 'Results'

            def __init__(self, places):
                """places: what current_url gives, one for each time it is read."""
                self.places, self.loaded = list(places), []

            def get(self, url):
                """Note the address asked for."""
                self.loaded.append(url)

            @property
            def current_url(self):
                """Where the browser is now."""
                return self.places.pop(0)

            def find_element(self, by, value):
                """The page's body."""
                return Body

        official = real.gov_url('POWERBALL', a, b)
        for places, refused in (((official, official), False), ((official, 'https://www.example.net/results'), True),
                                (('https://www.example.net/results', official), True)):
            fetcher = object.__new__(real.BrowserFetcher)
            fetcher.driver, fetcher.pause, fetcher.last, fetcher.log = Browser(places), 2.0, 0.0, []
            with mock.patch.object(real, 'parse_gov', wraps=real.parse_gov) as parsed:
                if refused:
                    with self.assertRaisesRegex(real.Refused, 'www.example.net.*no fallback source'):
                        fetcher.fetch('POWERBALL', a, b)
                    self.assertFalse(parsed.called, 'nothing is parsed from a page that is not the official one')
                else:
                    draws = fetcher.fetch('POWERBALL', a, b)
                    self.assertEqual([draw.number for draw in draws], list(range(1594, 1601)))
            self.assertEqual(fetcher.driver.loaded, [official])


class AnUpdate(WithATree):
    """What an update writes, and what each fault leaves unchanged."""

    def test_new_draws_are_added_the_old_file_is_kept_and_one_ledger_line_says_what_was_done(self):
        self.assertEqual(update(self.tree), 0)
        for game in updater.ERAS:
            store = updater.Store(self.tree, game)
            draws, data, last = store.load_verified_master()
            self.assertEqual((draws[-1].number, last['action'], int(last['added_first']), int(last['added_last'])),
                             (LATEST[game], 'UPDATE', HELD[game] + 1, LATEST[game]), game)
            self.assertEqual((last['version'], last['tool_version'], last['tool_sha256']),
                             ('2', '0.3', updater.sha(compare.NEW_FILE.read_bytes())))
            self.assertEqual(data.count(b'\r\n'), data.count(b'\n'), 'the results file is CRLF')
            backups = [path for path in store.backups.iterdir() if path.name.startswith(game + '_')]
            grabs = [path for path in store.grabs.iterdir() if path.name.startswith(game + '_')]
            self.assertEqual((len(backups), len(grabs)), (1, 1))
            self.assertEqual(updater.from_csv_bytes(game, backups[0].read_bytes())[-1].number, HELD[game])
            self.assertEqual(updater.sha(backups[0].read_bytes()), last['backup_sha256'])
            self.assertEqual(updater.sha(grabs[0].read_bytes()), last['grab_sha256'])
        self.assertFalse((self.tree / 'source_data' / '.results_master.lock').exists())
        self.assertEqual(sorted(path.name for path in self.tree.iterdir()), ['source_data'],
                         'the updater writes in its own tree\'s source_data and nowhere else')

    def test_with_nothing_new_the_results_file_is_untouched_and_the_ledger_says_no_change(self):
        compare.make_tree(updater, self.tree / 'current', LATEST, frozen=False)
        before = updater.Store(self.tree / 'current', 'POWERBALL').master.read_bytes()
        self.assertEqual(update(self.tree / 'current', games=('POWERBALL',)), 0)
        store = updater.Store(self.tree / 'current', 'POWERBALL')
        self.assertEqual(store.master.read_bytes(), before)
        self.assertEqual([row['action'] for row in store.ledger_rows()], ['INIT', 'NO_CHANGE'])
        self.assertFalse(store.backups.exists())

    def test_each_fault_changes_neither_the_results_file_nor_the_ledger_and_says_why(self):
        for plant, games, refusal, said in (
                (('differs', 1585), ('POWERBALL',), updater.VerifyFail, '1 overlapping draw.s. disagree with the master .draws 1585.'),
                (('skipped', 1595), ('POWERBALL',), updater.Stop, 'the grab has a gap in draw numbers; nothing written'),
                (('skipped', 1591), ('POWERBALL',), updater.Stop, 'the grab has a gap'),
                (('repeated', 1593), ('POWERBALL',), updater.Stop, 'draw 1593: main numbers invalid'),
                (('label', 1702), ('OZLOTTO',), updater.Stop, "draw 1702: 'Supplementary' not where expected"),
                (('label', 1592), ('POWERBALL',), updater.Stop, "draw 1592: 'Powerball:' not where expected")):
            game = games[0]
            before = self.held(game)
            with self.assertRaisesRegex(refusal, said, msg=plant):
                update(self.tree, games=games, plant=plant)
            self.assertEqual(self.held(game), before, plant)
            self.assertFalse(updater.Store(self.tree, game).backups.exists(), plant)
            self.assertFalse((self.tree / 'source_data' / '.results_master.lock').exists(), plant)

    def test_a_tree_whose_results_end_before_the_window_is_refused_and_a_wider_window_is_the_way(self):
        behind = compare.make_tree(updater, self.tree / 'behind', {'POWERBALL': 1500, 'OZLOTTO': 1650}, frozen=False)
        with self.assertRaisesRegex(updater.Refused, 'does not overlap the master .gap risk.; widen --months-back'):
            update(behind, games=('POWERBALL',))
        self.assertEqual(update(behind, games=('POWERBALL',), months_back=30), 0)
        self.assertEqual(updater.Store(behind, 'POWERBALL').load_verified_master()[0][-1].number, LATEST['POWERBALL'])

    def test_a_results_file_edited_outside_the_updater_is_found_before_anything_is_fetched(self):
        store = updater.Store(self.tree, 'OZLOTTO')
        data = bytearray(store.master.read_bytes())
        data[-5] = ord('9') if data[-5] != ord('9') else ord('8')
        store.master.write_bytes(bytes(data))
        with self.assertRaisesRegex(updater.VerifyFail, 'does not match the last ledger entry'):
            update(self.tree, games=('OZLOTTO',))
        self.assertFalse(store.grabs.exists(), 'nothing was fetched')

    def test_a_lock_left_behind_refuses_and_a_grab_or_a_backup_is_never_written_over(self):
        lock = self.tree / 'source_data' / '.results_master.lock'
        lock.write_text('x', encoding='ascii')
        with self.assertRaisesRegex(updater.Refused, 'another run is active, or a previous run crashed'):
            update(self.tree)
        self.assertTrue(lock.exists(), 'never removed for the owner')
        path = self.tree / 'x.csv'
        updater.write_new(path, b'a')
        with self.assertRaises(FileExistsError):
            updater.write_new(path, b'b')

    def test_a_tree_with_no_results_file_is_refused_and_told_where_results_come_from(self):
        with self.assertRaisesRegex(updater.Refused, 'holds no accepted results for POWERBALL'):
            update(self.tree / 'empty', games=('POWERBALL',))

    def test_the_pause_between_pages_may_be_lengthened_but_never_shortened(self):
        with self.assertRaisesRegex(updater.Refused, '--pause must be at least 2.0'):
            update(self.tree, pause=1.9)


class TheCommandLine(WithATree):
    """Run_Results_Updater.bat: the options, the exit codes, and the tree's lock."""

    def run_main(self, *arguments) -> tuple:
        """(exit code, what was printed) of the updater's main for some arguments in the tree."""
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed), contextlib.redirect_stderr(printed):
            try:
                code = updater.main(list(arguments), self.tree)
            except SystemExit as stopped:
                code = f'argparse stopped with {stopped.code}'
        return code, printed.getvalue()

    def test_a_refusal_is_exit_code_3_and_names_the_reason(self):
        code, printed = self.run_main('--games', 'POWERBALL', '--pause', '1')
        self.assertEqual(code, 3)
        self.assertIn('[MASTER] REFUSED: --pause must be at least 2.0', printed)
        code, printed = self.run_main('--games', 'LOTTO')
        self.assertEqual((code, 'games must be POWERBALL and/or OZLOTTO' in printed), (3, True))

    def test_a_check_that_fails_is_exit_code_1_and_a_stop_is_exit_code_2(self):
        with mock.patch.object(updater, 'cmd_update', side_effect=updater.VerifyFail('the files disagree')):
            self.assertEqual(self.run_main()[0], 1)
        with mock.patch.object(updater, 'cmd_update', side_effect=updater.Stop('a block page')):
            code, printed = self.run_main()
        self.assertEqual((code, '[MASTER] STOP: a block page' in printed), (2, True))
        with mock.patch.object(updater, 'cmd_update', return_value=0) as called:
            self.assertEqual(self.run_main('--months-back', '11', '--games', 'ozlotto')[0], 0)
        self.assertEqual(called.call_args.args, (self.tree, ['OZLOTTO'], 11, 'chrome', 2.0))

    def test_the_one_off_init_command_and_the_old_self_test_are_gone(self):
        for arguments in (('init',), ('update',), ('--self-test',)):
            self.assertEqual(self.run_main(*arguments)[0], 'argparse stopped with 2', arguments)
        for name in ('cmd_init', 'self_test', 'holdout_opened', 'freeze_state'):
            self.assertFalse(hasattr(updater, name), name)

    def test_started_by_itself_the_updater_holds_the_trees_lock_and_refuses_while_a_job_holds_it(self):
        tree = fx.make_tree(self.tree / 'whole_tree')
        lock = tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME
        seen = []

        def stand_in(arguments, root):
            """In place of the updater's main: note what it was given and whether the tree's lock is held."""
            seen.append((arguments, root, lock.exists()))
            return 0

        path_before, printed = list(sys.path), io.StringIO()
        try:
            with mock.patch.object(research_command, 'TREE_ROOT', tree), \
                    mock.patch.object(research_command, 'IMPORT_FOLDERS', (TREE_OF_THIS_FILE / 'src',)), \
                    mock.patch.object(sys, 'prefix', str(tree / '.venv')), \
                    mock.patch('updater.results_updater.main', stand_in), contextlib.redirect_stdout(printed):
                self.assertEqual(research_command.run_command(['update', '--months-back', '11']), 0)
                self.assertEqual(seen, [(['--months-back', '11'], tree, True)])
                self.assertFalse(lock.exists(), 'released when the updater ends')
                lock.parent.mkdir(exist_ok=True)
                lock.write_text('research job; started earlier\n', encoding='ascii')
                self.assertEqual(research_command.run_command(['update']), research_command.EXIT_BAD_COMMAND)
        finally:
            sys.path[:] = path_before
        self.assertEqual(len(seen), 1, 'the updater was not started while a job held the tree')
        self.assertIn('REFUSED: a process of this tree is running', printed.getvalue())

    def test_the_launcher_names_its_command_and_runs_python_isolated_without_a_cache(self):
        text = (TREE_OF_THIS_FILE / 'Run_Results_Updater.bat').read_bytes().decode('ascii')
        self.assertIn('"%PY%" -I -B -u "%TOOL%" update %*\r\n', text)
        self.assertEqual(text.count('\r\n'), text.count('\n'), 'CRLF line endings throughout')


class TheJobFetchesFirst(fx.JobCase):
    """Scheme section 5 step 3, as the owner settled it (entry 356)."""

    def tree_of_both(self) -> Path:
        """A tree whose source_data is the updater's own (results through draw 1590 of Powerball) and which
        holds one toy method that begins late, so that a job has little to fill."""
        tree = self.tree(variants=())
        shutil.rmtree(tree / 'source_data')
        compare.make_tree(updater, tree, HELD, frozen=False)
        self.add_variant(tree, 'TOY_A_V1', minimum=440)
        return tree

    @staticmethod
    def stand_in(plant=None):
        """In place of the real updater: the updater's own update, reading invented pages."""
        def fetch(tree_root, game_id):
            """Update one game from invented pages."""
            update(Path(tree_root), games=(game_id,), plant=plant)
        return fetch

    def test_new_results_are_fetched_under_the_jobs_lock_and_worked_in_the_same_job(self):
        tree = self.tree_of_both()
        lock, held = tree / job_lock.RECORDS_FOLDER / job_lock.JOB_LOCK_NAME, []
        fetch = self.stand_in()

        def watched(tree_root, game_id):
            """Note whether the job's lock is held while the updater runs."""
            held.append(lock.exists())
            fetch(tree_root, game_id)

        code, said = fx.run_job(tree, no_update=False, update=watched)
        self.assertEqual(code, 0, said)
        self.assertEqual(held, [True])
        self.assertTrue(any('fetching new official results with the results updater' in line for line in said), said)
        self.assertTrue(any(f'results on file through draw {LATEST["POWERBALL"]}' in line for line in said), said)
        targets = [line['content']['target'] for line in fx.list_lines(tree, 'E_901', 'TOY_A_V1')]
        self.assertEqual(targets[-1], LATEST['POWERBALL'] + 1, 'the next draw\'s forecast is made too')
        self.assertEqual(self.status(tree, 'TOY_A_V1').eligible_from, LATEST['POWERBALL'] + 1,
                         'the establishment draw is the last draw held once the results were fetched')

    def test_if_the_updater_does_not_finish_the_job_says_so_loudly_goes_on_and_does_not_end_as_a_clean_one(self):
        tree = self.tree_of_both()
        code, said = fx.run_job(tree, no_update=False, update=self.stand_in(('skipped', 1595)))
        self.assertEqual(code, 1)
        loud = [line for line in said if 'THE RESULTS UPDATER DID NOT FINISH' in line]
        self.assertEqual(len(loud), 2, 'said when it happens and again at the end')
        self.assertIn('Stop: POWERBALL: the grab has a gap in draw numbers', loud[0])
        self.assertIn('DID NOT FINISH NORMALLY', loud[0])
        self.assertIn('The job goes on with the accepted results on file for POWERBALL', loud[0])
        self.assertNotIn('No new results were added', loud[0], 'an update can fail after it has published')
        targets = [line['content']['target'] for line in fx.list_lines(tree, 'E_901', 'TOY_A_V1')]
        self.assertEqual(targets[-1], HELD['POWERBALL'] + 1, 'the research was done on the results held')
        self.assertEqual(said[-1], 'The job finished, but not cleanly: the results updater or a method did not finish. '
                                   'See the warnings above.')

        def broken(tree_root, game_id):
            """An updater that fails in a way of its own (no browser on this PC, say)."""
            raise OSError('chromedriver was not found')

        code, said = fx.run_job(tree, no_update=False, update=broken)
        self.assertEqual(code, 1)
        self.assertTrue(any('THE RESULTS UPDATER DID NOT FINISH NORMALLY (OSError: chromedriver was not found)' in line
                            for line in said), said)

    def tree_of_both_games(self) -> Path:
        """As tree_of_both, with a toy method that works both games."""
        tree = self.tree(variants=())
        shutil.rmtree(tree / 'source_data')
        compare.make_tree(updater, tree, HELD, frozen=False)
        self.add_variant(tree, 'TOY_A_V1', games=('POWERBALL', 'OZLOTTO'), minimum=220)
        return tree

    def test_after_the_website_stops_the_updater_nothing_more_is_fetched_in_that_job_and_both_games_are_worked(self):
        tree = self.tree_of_both_games()
        asked = []

        def blocked(tree_root, game_id):
            """The website serves a block page."""
            asked.append(game_id)
            raise updater.Stop('www.lotterywest.wa.gov.au served a block/challenge page; nothing was bypassed')

        code, said = fx.run_job(tree, games=('POWERBALL', 'OZLOTTO'), no_update=False, update=blocked)
        self.assertEqual(code, 1)
        self.assertEqual(asked, ['POWERBALL'], 'the other game is not asked for once the website has stopped the updater')
        self.assertTrue(any('The website stopped it: nothing more is fetched in this job, for either game' in line
                            for line in said), said)
        self.assertTrue(any(line.startswith('OZLOTTO: nothing is fetched: the website stopped the results updater '
                                            'earlier in this job') for line in said), said)
        for game in ('POWERBALL', 'OZLOTTO'):
            self.assertTrue(any(line.startswith(f'{game}: finished') for line in said), (game, said))
            targets = [line['content']['target'] for line in fx.list_lines(tree, 'E_901', 'TOY_A_V1', game_id=game)]
            self.assertEqual(targets[-1], HELD[game] + 1, game)

    def test_a_failure_that_is_not_the_websites_stop_does_not_keep_the_other_game_from_being_fetched(self):
        tree = self.tree_of_both_games()
        asked, fetch = [], self.stand_in()

        def disagrees_for_powerball(tree_root, game_id):
            """One game's fetched draws disagree with the tree's; the other game's update is ordinary."""
            asked.append(game_id)
            if game_id == 'POWERBALL':
                raise updater.VerifyFail('POWERBALL: 1 overlapping draw(s) disagree with the master')
            fetch(tree_root, game_id)

        code, said = fx.run_job(tree, games=('POWERBALL', 'OZLOTTO'), no_update=False, update=disagrees_for_powerball)
        self.assertEqual(code, 1)
        self.assertEqual(asked, ['POWERBALL', 'OZLOTTO'])
        self.assertTrue(any(f'OZLOTTO: results on file through draw {LATEST["OZLOTTO"]}' in line for line in said), said)
        self.assertFalse(any('nothing more is fetched' in line for line in said), said)

    def test_with_no_update_the_updater_is_never_called(self):
        tree = self.tree_of_both()
        code, said = fx.run_job(tree)                       # the fixtures' stand-in raises if it is ever called
        self.assertEqual(code, 0, said)
        self.assertFalse(any('fetching' in line for line in said), said)
        self.assertIs(research_job.run.__kwdefaults__['update'], research_job.update_with_the_trees_updater)

    def test_a_change_to_the_updater_is_not_a_change_to_the_engine(self):
        tree = self.tree_of_both()
        before = code_identity.infrastructure_fingerprint(tree)
        (tree / 'src' / 'updater').mkdir()
        (tree / 'src' / 'updater' / 'results_updater.py').write_text('# the updater\n', encoding='ascii')
        self.assertEqual(code_identity.infrastructure_fingerprint(tree), before)
        self.assertNotIn('src/updater/results_updater.py', code_identity.infrastructure_files(tree))
        (tree / 'src' / 'research').mkdir()
        (tree / 'src' / 'research' / 'updater').mkdir()
        (tree / 'src' / 'research' / 'updater' / 'x.py').write_text('# engine code in a folder of that name\n',
                                                                    encoding='ascii')
        self.assertNotEqual(code_identity.infrastructure_fingerprint(tree), before, 'only src/updater is left out')


@unittest.skipUnless(compare.FROZEN_FILE.is_file(), 'the first system\'s updater is kept in the repository only')
class TheSameAsTheFrozenUpdater(unittest.TestCase):
    """deploy/compare_updater_with_frozen.py: the new updater is the reviewed one with its Mode H states out."""

    def test_definition_by_definition_and_on_the_same_invented_pages_they_are_the_same(self):
        said = []
        self.assertTrue(compare.compare_definitions(compare.FROZEN_FILE, compare.NEW_FILE, say=said.append), said)
        frozen = compare.load(compare.FROZEN_FILE, 'frozen_updater_under_test')
        self.assertTrue(compare.compare_behaviour(frozen, updater, say=said.append), said)
        self.assertEqual(len([line for line in said if line.startswith('SAME')]), 13, said)

    def test_a_changed_statement_in_the_new_updater_is_found_both_ways(self):
        source = compare.NEW_FILE.read_text(encoding='ascii')
        for old, new, in_which in (
                ('if any(y.number != x.number + 1 for x, y in zip(grab, grab[1:])):',
                 'if any(y.number != x.number + 2 for x, y in zip(grab, grab[1:])):', 'update_game'),
                ('if len(d.main) != 7 or len(set(d.main)) != 7', 'if len(d.main) != 7', 'validate_draw')):
            self.assertEqual(source.count(old), 1, old)
            with tempfile.TemporaryDirectory() as folder:
                changed_file = Path(folder) / 'results_updater.py'
                changed_file.write_text(source.replace(old, new), encoding='ascii')
                said = []
                compare.compare_definitions(compare.FROZEN_FILE, changed_file, say=said.append)
                frozen = compare.load(compare.FROZEN_FILE, 'frozen_updater_under_test')
                changed = compare.load(changed_file, 'changed_updater_under_test')
                self.assertFalse(compare.compare_behaviour(frozen, changed, say=said.append), in_which)
            self.assertTrue(any(line.startswith('DIFFERENT') and ':' in line for line in said), said)
        # A change inside a definition that is not on the declared list is found by the first part alone.
        with tempfile.TemporaryDirectory() as folder:
            changed_file = Path(folder) / 'results_updater.py'
            changed_file.write_text(source.replace('return hashlib.sha256(data).hexdigest()',
                                                   'return hashlib.sha256(data + b"").hexdigest()'), encoding='ascii')
            said = []
            self.assertFalse(compare.compare_definitions(compare.FROZEN_FILE, changed_file, say=said.append))
            self.assertTrue(any('are changed:' in line and ' sha,' in line for line in said), said)


if __name__ == '__main__':
    unittest.main()
