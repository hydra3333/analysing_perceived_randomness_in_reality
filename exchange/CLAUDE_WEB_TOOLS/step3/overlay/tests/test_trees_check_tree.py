"""Tests of Check_Tree, the owner's read-only look at a tree.

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; specification v0.6 sections 14.1 and 16: "read-only: what is installed,
each variant's status, what is ready, any drift, the backup ZIPs, locks"; deployment design v0.12 sections 1, 8
and 10; the file-form standard v0.2 section 6, the checker's third place).

Which of the project's own modules it uses
    research_fixtures           invented trees, toy variants and invented results
    test_trees_readiness        write_crlf, bring_to_form: an invented tree in the form the standard gives its files
    check_tree (deploy/)        the code under test
    install_readiness (deploy/), research.installed_files, research.settings, research.status_file

What uses it
    The project's test suite.
"""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# The install tools are imported from deploy/, as the launcher program imports them.
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import check_tree                                           # noqa: E402  (after the path line above)
import install_readiness                                    # noqa: E402
import research_fixtures as fixtures                        # noqa: E402
from research import environment_marker, installed_files, settings, status_file    # noqa: E402
from test_trees_readiness import bring_to_form, write_crlf  # noqa: E402

FAMILY, VARIANT, SECOND_VARIANT = 'E_901', 'TOY_COUNTS_V1', 'TOY_COUNTS_V2'
HELPER = f'{FAMILY}/toy_helper_v1.py'
GAMES = ('POWERBALL', 'OZLOTTO')


def every_file_of(folder: Path) -> dict:
    """Every file under a folder with the SHA-256 of its bytes: {path: sha256}. Two equal results mean that
    nothing was written, changed, added or removed."""
    return {str(path.relative_to(folder)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(folder.rglob('*')) if path.is_file()}


class InventedDevAndQa(unittest.TestCase):
    """An invented DEV tree and an invented QA tree that holds DEV's software: one toy variant, its helper, its
    status file and its list of installed files. DEV's settings file names the QA tree."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        base = Path(self.folder.name).resolve()
        self.dev = fixtures.make_tree(base / 'dev')
        self.qa = fixtures.make_tree(base / 'qa', role='QA')
        self.qa_backups = base / 'qa_backups'
        with open(self.dev / 'ENVIRONMENT.ini', 'a', encoding='utf-8', newline='\r\n') as handle:
            handle.write(f'[QA]\ntree_root = {self.qa}\nbackup_root = {self.qa_backups}\nvenv_dir = {self.qa / ".venv"}\n')
        for tree in (self.dev, self.qa):
            folder = fixtures.add_toy_variant(tree, FAMILY, VARIANT, games=GAMES,
                                              helpers=(f'{FAMILY}/__init__.py', HELPER))
            write_crlf(tree / 'src' / 'methods' / HELPER, '"""An invented helper."""\nLIMIT = 3\n')
            bring_to_form(tree)
        self.qa_variant = folder
        self.qa_status = self.qa_variant / 'VARIANT_STATUS.ini'
        status_file.create_active(self.qa_status, FAMILY, VARIANT, GAMES)
        installed_files.write_list(self.qa, installed_files.software_now(self.qa))

    def tearDown(self):
        self.folder.cleanup()

    def look(self, *words) -> tuple:
        """Run Check_Tree with the words typed; return (exit code, everything it printed as one text)."""
        lines = []
        code = check_tree.main(list(words), settings.read_dev_view(self.dev), say=lines.append)
        return code, '\n'.join(lines)


class ItOnlyLooks(InventedDevAndQa):
    """Specification section 16: Check_Tree is read-only."""

    def test_it_changes_nothing_in_the_tree_it_looks_at_nor_in_dev_nor_in_the_backup_folder(self):
        (self.qa_backups / 'QA_20261201_101500_RESEARCH.zip').write_bytes(b'PK invented')
        before = [every_file_of(folder) for folder in (self.dev, self.qa, self.qa_backups)]
        for role in ('QA', 'DEV'):
            self.look(role)
        self.assertEqual([every_file_of(folder) for folder in (self.dev, self.qa, self.qa_backups)], before)

    def test_a_word_that_is_not_a_role_prints_the_usage_and_looks_at_nothing(self):
        for words in ((), ('LIVE',), ('QA', 'PROD')):
            code, text = self.look(*words)
            self.assertEqual(code, check_tree.EXIT_COULD_NOT_LOOK)
            self.assertIn('Usage:  Check_Tree.bat DEV', text)


class TheSettings(InventedDevAndQa):
    """Deployment design section 1: it prints how the settings are read; a tree is what its own file says."""

    def test_it_prints_devs_own_places_and_its_entry_for_each_other_tree(self):
        code, text = self.look('QA')
        self.assertIn(f'DEV names QA as tree_root {self.qa}; backup_root {self.qa_backups}', text)
        self.assertIn('says role QA and agrees', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)

    def test_a_tree_whose_own_file_says_another_role_is_refused_and_not_looked_at(self):
        own = self.qa / 'ENVIRONMENT.ini'
        own.write_bytes(own.read_bytes().replace(b'role = QA', b'role = PROD'))
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_COULD_NOT_LOOK)
        self.assertIn('REFUSED:', text)
        self.assertNotIn('Installed:', text)

    def test_a_tree_that_is_not_created_yet_is_said_as_such_with_the_command_that_creates_it(self):
        with open(self.dev / 'ENVIRONMENT.ini', 'a', encoding='utf-8', newline='\r\n') as handle:
            handle.write(f'[PROD]\ntree_root = {self.dev.parent / "prod"}\n'
                         f'backup_root = {self.dev.parent / "prod_backups"}\n'
                         f'venv_dir = {self.dev.parent / "prod" / ".venv"}\n')
        code, text = self.look('PROD')
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND)
        self.assertIn('PROD is not created yet', text)
        self.assertIn('Init_Tree.bat PROD', text)


class WhatIsInstalledAndDrift(InventedDevAndQa):
    """Deployment design section 8: the tree and its list differ: the file is named."""

    def test_a_tree_as_installed_has_nothing_found(self):
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)
        self.assertIn('Drift: 0 difference(s)', text)
        self.assertIn('Nothing was found by the checks this command makes.', text)
        self.assertIn('it does not say that the tree is ready to run', text)

    def test_a_helper_changed_outside_the_tools_is_found_and_the_way_back_is_said(self):
        with open(self.qa / 'src' / 'methods' / HELPER, 'ab') as handle:
            handle.write(b'LIMIT = 4\r\n')
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_FOUND)
        self.assertIn(f'FOUND: src/methods/{HELPER}: its bytes are not the bytes that were installed', text)
        self.assertIn('restore from a backup you choose', text)

    def test_an_unlisted_file_under_src_is_found(self):
        write_crlf(self.qa / 'src' / 'stray.py', '# not installed by any command\n')
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_FOUND)
        self.assertIn('FOUND: src/stray.py: it lies under src and is not on the list of installed files', text)

    def test_a_tree_without_its_list_is_found(self):
        (self.qa / installed_files.LIST_PATH).unlink()
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_FOUND)
        self.assertIn('this tree has no list of installed files', text)

    def test_dev_keeps_no_list_and_that_is_said_not_found(self):
        code, text = self.look('DEV')
        self.assertIn('DEV keeps no list of installed files', text)
        self.assertIn(f'{FAMILY}/{VARIANT}: no status file yet', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)


class EachVariantsStatus(InventedDevAndQa):
    """Specification 3.5: the status file beside the software is what the owner is shown."""

    def test_an_active_variant_and_a_withdrawn_one_are_shown_with_draw_reason_and_eligibility(self):
        statuses = status_file.read_status(self.qa_status, GAMES)
        statuses['POWERBALL'] = status_file.with_eligibility(
            status_file.with_withdrawal(statuses['POWERBALL'], 1161, 'an invented reason', 'noted'), 1158, 'noted')
        status_file.write_status(self.qa_status, FAMILY, VARIANT, statuses)
        code, text = self.look('QA')
        self.assertIn('POWERBALL: WITHDRAWN from draw 1161 (an invented reason), prevailing OV-1 from draw 1158', text)
        self.assertIn('OZLOTTO: ACTIVE, no eligibility draw yet', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)

    def test_a_status_file_edited_by_hand_is_found(self):
        self.qa_status.write_bytes(self.qa_status.read_bytes().replace(b'status = ACTIVE', b'status = WITHDRAWN', 1))
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_FOUND)
        self.assertIn('FOUND:', text)
        self.assertIn('VARIANT_STATUS.ini', text)


class WhatIsReadyAndTheComparisonWithDev(InventedDevAndQa):
    """Deployment design section 14, examples 2 and 6: what is ready in DEV and not installed, and what is
    installed with other bytes, are information for the owner and never a fault of the tree."""

    def test_a_variant_ready_in_dev_and_not_installed_is_listed_as_information(self):
        fixtures.add_toy_variant(self.dev, FAMILY, SECOND_VARIANT, games=GAMES, behaviour={'scale': 2})
        bring_to_form(self.dev)
        install_readiness.mark_variant(self.dev, FAMILY, SECOND_VARIANT)
        code, text = self.look('QA')
        self.assertIn(f'{FAMILY}/{SECOND_VARIANT}: ready in DEV, not installed', text)
        self.assertIn(f'not ready: {FAMILY}/{VARIANT}: it is not marked', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)

    def test_a_variant_changed_in_dev_after_its_installation_is_said_to_be_installed_with_different_bytes(self):
        with open(self.dev / 'src' / 'methods' / FAMILY / VARIANT / 'method.py', 'ab') as handle:
            handle.write(b'# edited in DEV afterwards\r\n')
        code, text = self.look('QA')
        self.assertIn(f'{FAMILY}/{VARIANT}: installed with different bytes than DEV now holds', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)

    def test_infrastructure_that_is_devs_is_said_so_and_a_file_that_differs_is_named(self):
        self.assertIn('the infrastructure is file for file DEV\'s.', self.look('QA')[1])
        with open(self.dev / 'src' / 'toy_other.py', 'ab') as handle:
            handle.write(b'# DEV has moved on\r\n')
        code, text = self.look('QA')
        self.assertIn('the infrastructure differs from DEV\'s in 1 file(s): src/toy_other.py', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)


class TheFormOfATreesFiles(InventedDevAndQa):
    """The file-form standard, section 6: Check_Tree checks the installed files, the settings file, every status
    file and what the project's programs wrote, each by its kind."""

    def test_a_record_written_with_bare_line_feeds_is_found(self):
        (self.qa / 'records' / 'INSTALL_LOG.json').write_bytes(b'{\n"invented": true\n}\n')
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_FOUND)
        self.assertRegex(text, r'FOUND: records/INSTALL_LOG\.json: must be CRLF')

    def test_a_line_record_file_is_right_with_line_feeds_and_wrong_with_carriage_returns(self):
        log = self.qa / 'records' / 'INSTALL_LOG.jsonl'
        log.write_bytes(b'{"invented": 1}\n')
        self.assertEqual(self.look('QA')[0], check_tree.EXIT_NOTHING_FOUND)
        log.write_bytes(b'{"invented": 1}\r\n')
        code, text = self.look('QA')
        self.assertEqual(code, check_tree.EXIT_FOUND)
        self.assertIn('FOUND: records/INSTALL_LOG.jsonl', text)

    def test_the_settings_file_and_a_results_master_in_the_wrong_form_are_found(self):
        fixtures.write_results(self.qa, 'POWERBALL', 1150)
        bring_to_form(self.qa)
        self.assertEqual(self.look('QA')[0], check_tree.EXIT_NOTHING_FOUND)
        for name in ('ENVIRONMENT.ini', 'source_data/POWERBALL_results_master.csv'):
            with self.subTest(name=name):
                path = self.qa / name
                kept = path.read_bytes()
                path.write_bytes(kept.replace(b'\r\n', b'\n'))
                code, text = self.look('QA')
                self.assertEqual(code, check_tree.EXIT_FOUND)
                self.assertIn(f'FOUND: {name}: must be CRLF', text)
                path.write_bytes(kept)

    def test_the_retired_opening_record_and_the_updaters_kept_copies_are_left_as_they_are(self):
        (self.dev / 'source_data' / 'grabs').mkdir(parents=True)
        (self.dev / 'source_data' / 'HOLDOUT_OPENED_POWERBALL.json').write_bytes(b'{"frozen": "history"}\n')
        (self.dev / 'source_data' / 'grabs' / 'page_0001.html').write_bytes(b'<html>\n</html>\n')
        code, text = self.look('DEV')
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)


class TheBackupsAndTheLocks(InventedDevAndQa):
    """Specification 14.1 and deployment design section 10: the backup ZIPs are listed and none is verified; the
    locks present are shown."""

    def test_every_backup_zip_is_listed_with_its_full_path_and_size_and_none_is_verified(self):
        first = self.qa_backups / 'QA_20261201_101500_RESEARCH.zip'
        first.write_bytes(b'this is not even a ZIP: listing it must not open it')
        (self.qa_backups / 'QA_20261208_101500_RESEARCH.zip.partial').write_bytes(b'unfinished')
        code, text = self.look('QA')
        self.assertIn(f'Backups: 1 ZIP file(s) in {self.qa_backups}. This command lists them and verifies none.', text)
        self.assertIn(f'{first}  {first.stat().st_size:,} bytes', text)
        self.assertNotIn('.partial', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)

    def test_dev_has_no_backup_folder_and_that_is_said(self):
        self.assertIn('Backups: DEV has no backup folder', self.look('DEV')[1])

    def test_the_locks_that_are_present_are_shown_and_the_orphan_marker_is_said_to_block_every_launch(self):
        self.assertIn('Locks and unfinished operations: 0 present.', self.look('QA')[1])
        (self.qa / 'records').mkdir(exist_ok=True)
        (self.qa / 'records' / 'JOB.lock').write_bytes(b'an invented job\r\n')
        marker = self.qa / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'
        marker.parent.mkdir(parents=True)
        marker.write_bytes(b'{}\r\n')
        text = self.look('QA')[1]
        self.assertIn('Locks and unfinished operations: 2 present.', text)
        self.assertIn('THE ORPHAN MARKER: it blocks every launch', text)
        self.assertIn(f'{self.qa / "records" / "JOB.lock"}: the job lock', text)

    def test_an_unfinished_operation_is_shown_with_what_it_means_and_the_way_on(self):
        (self.qa / 'records' / 'INSTALL_IN_PROGRESS.json').write_bytes(b'{}\r\n')
        text = self.look('QA')[1]
        self.assertIn('Locks and unfinished operations: 1 present.', text)
        self.assertIn('did not finish in this tree. Run that same command again from DEV', text)

    def test_an_environment_without_its_marker_is_not_verified_and_a_marker_is_only_said_to_be_present(self):
        self.assertIn('Environment: NOT VERIFIED; every launcher of this tree refuses', self.look('QA')[1])
        environment_marker.write_marker(self.qa / '.venv')
        code, text = self.look('QA')
        self.assertIn('Environment: verification marker present', text)
        self.assertIn('This command did not check the environment\'s files or packages against it', text)
        self.assertNotIn('Environment: verified', text)
        self.assertEqual(code, check_tree.EXIT_NOTHING_FOUND, text)
        (self.qa / '.venv' / 'Scripts' / 'added.exe').write_bytes(b'MZ')     # changed after it was verified:
        again = self.look('QA')[1]                                           # this command cannot know, and
        self.assertIn('Environment: verification marker present', again)     # does not say "verified"
        self.assertNotIn('Environment: verified', again)
        self.assertIn('Environment: DEV\'s environment has no verification marker', self.look('DEV')[1])


if __name__ == '__main__':
    unittest.main()
