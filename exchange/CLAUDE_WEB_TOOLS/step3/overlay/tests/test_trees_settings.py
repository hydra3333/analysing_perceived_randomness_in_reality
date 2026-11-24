"""Tests of the settings file as DEV's tools read it: DEV's entries for QA and PROD and the checks across trees.

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; deployment design v0.12 section 1, checks 1 to 5, and section 15,
"Settings"). The checks that concern one tree alone are tested in tests/test_research_identity.py.

Which of the project's own modules it uses
    research.settings    the reader under test

What uses it
    The project's test suite.
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from research import settings


class DevViewOfTheThreeTrees(unittest.TestCase):
    """Deployment design section 1: DEV's file names the QA and PROD trees, and the three must be separate."""

    def setUp(self):
        """Invented places for three trees and two backup roots, laid out as the owner's real ones are: the QA
        tree and both backup roots on one "drive" (here one folder), PROD on another."""
        self.folder = tempfile.TemporaryDirectory()
        base = Path(self.folder.name).resolve()
        self.dev = base / 'e_drive' / 'project'
        self.qa = base / 't_drive' / 'a_p_r_i_r'
        self.prod = base / 'g_drive' / 'a_p_r_i_r'
        self.qa_backups = base / 't_drive' / 'a_p_r_i_r_backups' / 'QA'
        self.prod_backups = base / 't_drive' / 'a_p_r_i_r_backups' / 'PROD'
        (self.dev / '.venv').mkdir(parents=True)
        self.lines = {
            'environment': {'role': 'DEV', 'tree_root': self.dev, 'venv_dir': self.dev / '.venv'},
            'QA': {'tree_root': self.qa, 'backup_root': self.qa_backups, 'venv_dir': self.qa / '.venv'},
            'PROD': {'tree_root': self.prod, 'backup_root': self.prod_backups, 'venv_dir': self.prod / '.venv'},
        }

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def write_dev_file(self) -> None:
        """Write DEV's settings file from self.lines (a section or a key removed from it is left out)."""
        text = ''.join(f'[{section}]\n' + ''.join(f'{key} = {value}\n' for key, value in keys.items())
                       for section, keys in self.lines.items())
        (self.dev / 'ENVIRONMENT.ini').write_text(text, encoding='utf-8')

    def write_tree_file(self, which_tree: str, **changed) -> None:
        """Create the QA or PROD tree's folder and its own settings file, as Init_Tree would from DEV's entry;
        `changed` replaces a value, for example role='PROD' or backup_root=<another folder>."""
        entry = dict(self.lines[which_tree])
        keys = {'role': which_tree, 'tree_root': entry['tree_root'], 'backup_root': entry['backup_root'],
                'venv_dir': entry['venv_dir']}
        keys.update(changed)
        Path(entry['tree_root']).mkdir(parents=True, exist_ok=True)
        text = '[environment]\n' + ''.join(f'{key} = {value}\n' for key, value in keys.items())
        (Path(entry['tree_root']) / 'ENVIRONMENT.ini').write_text(text, encoding='utf-8')

    def refused(self, pattern: str):
        """Write DEV's file and expect read_dev_view to refuse with a message matching `pattern`."""
        self.write_dev_file()
        return self.assertRaisesRegex(settings.SettingsRefused, pattern)

    # ---- a valid file

    def test_a_valid_file_gives_dev_and_both_entries(self):
        self.write_dev_file()
        view = settings.read_dev_view(self.dev)
        self.assertEqual(view.own.role, 'DEV')
        self.assertEqual(sorted(view.entries), ['PROD', 'QA'])
        self.assertEqual((view.entries['QA'].tree_root, view.entries['QA'].backup_root, view.entries['QA'].venv_dir),
                         (self.qa, self.qa_backups, self.qa / '.venv'))
        self.assertEqual(view.entries['PROD'].role, 'PROD')

    def test_a_file_with_no_other_tree_is_valid_and_has_no_entries(self):
        del self.lines['QA'], self.lines['PROD']
        self.write_dev_file()
        self.assertEqual(settings.read_dev_view(self.dev).entries, {})

    def test_the_owners_layout_is_accepted_a_backup_root_beside_a_tree_whose_name_it_begins_with(self):
        # 't_drive/a_p_r_i_r_backups' begins with the text 't_drive/a_p_r_i_r' but is not inside that folder.
        self.write_dev_file()
        self.assertEqual(settings.read_dev_view(self.dev).entries['QA'].backup_root, self.qa_backups)

    # ---- the file is DEV's

    def test_a_tree_that_is_not_dev_refuses(self):
        self.lines['environment'] = {'role': 'QA', 'tree_root': self.dev, 'venv_dir': self.dev / '.venv',
                                     'backup_root': self.qa_backups}
        del self.lines['QA']
        with self.refused('run from DEV only'):
            settings.read_dev_view(self.dev)

    # ---- every key of an entry is needed, and every path is absolute and real (check 1)

    def test_each_missing_key_of_an_entry_refuses_naming_section_and_key(self):
        for role in ('QA', 'PROD'):
            for key in ('tree_root', 'backup_root', 'venv_dir'):
                with self.subTest(role=role, key=key):
                    kept = self.lines[role].pop(key)
                    with self.refused(rf'\[{role}\] {key}: this setting is missing'):
                        settings.read_dev_view(self.dev)
                    self.lines[role][key] = kept

    def test_a_relative_path_in_an_entry_refuses(self):
        self.lines['PROD']['backup_root'] = 'backups'
        with self.refused(r'\[PROD\] backup_root: "backups" is not an absolute path'):
            settings.read_dev_view(self.dev)

    def test_a_link_in_an_entrys_path_refuses(self):
        real_place = Path(self.folder.name).resolve() / 'real_place'
        real_place.mkdir()
        link = Path(self.folder.name).resolve() / 'a_link'
        try:
            os.symlink(real_place, link, target_is_directory=True)
        except OSError:
            self.skipTest('this account cannot create a link')
        self.lines['QA']['tree_root'] = link / 'a_p_r_i_r'
        self.lines['QA']['venv_dir'] = link / 'a_p_r_i_r' / '.venv'
        with self.refused(r'\[QA\] tree_root: .* is not its own real path'):
            settings.read_dev_view(self.dev)

    # ---- check 3: the environment folder lies inside its own tree

    def test_an_entrys_environment_outside_its_tree_refuses(self):
        self.lines['PROD']['venv_dir'] = self.qa / '.venv'
        with self.refused(r'\[PROD\] venv_dir: .* is not inside that tree'):
            settings.read_dev_view(self.dev)

    def test_an_entrys_environment_that_is_the_tree_itself_refuses(self):
        self.lines['QA']['venv_dir'] = self.qa
        with self.refused(r'\[QA\] venv_dir: .* is not inside that tree'):
            settings.read_dev_view(self.dev)

    # ---- check 2: three separate trees; backup roots outside every tree

    def test_two_trees_in_the_same_folder_refuse(self):
        self.lines['PROD']['tree_root'] = self.qa
        self.lines['PROD']['venv_dir'] = self.qa / '.venv'
        with self.refused(r'\[QA\] tree_root .* and \[PROD\] tree_root .* three separate folders'):
            settings.read_dev_view(self.dev)

    def test_a_tree_inside_another_tree_refuses(self):
        self.lines['QA']['tree_root'] = self.prod / 'qa'
        self.lines['QA']['venv_dir'] = self.prod / 'qa' / '.venv'
        with self.refused('three separate folders'):
            settings.read_dev_view(self.dev)

    def test_a_tree_inside_dev_refuses(self):
        self.lines['PROD']['tree_root'] = self.dev / 'prod'
        self.lines['PROD']['venv_dir'] = self.dev / 'prod' / '.venv'
        with self.refused(r'\[environment\] tree_root .* and \[PROD\] tree_root'):
            settings.read_dev_view(self.dev)

    def test_dev_inside_another_tree_refuses(self):
        self.lines['QA']['tree_root'] = self.dev.parent
        self.lines['QA']['venv_dir'] = self.dev.parent / '.venv'
        with self.refused('three separate folders'):
            settings.read_dev_view(self.dev)

    def test_a_backup_root_inside_its_own_tree_refuses(self):
        self.lines['QA']['backup_root'] = self.qa / 'backups'
        with self.refused(r'\[QA\] backup_root .* lie one inside the other'):
            settings.read_dev_view(self.dev)

    def test_a_backup_root_inside_another_tree_refuses(self):
        self.lines['QA']['backup_root'] = self.prod / 'qa_backups'
        with self.refused(r'\[QA\] backup_root .* and \[PROD\] tree_root .* lie one inside the other'):
            settings.read_dev_view(self.dev)

    def test_a_backup_root_inside_dev_refuses(self):
        self.lines['PROD']['backup_root'] = self.dev / 'backups'
        with self.refused(r'\[PROD\] backup_root .* and \[environment\] tree_root'):
            settings.read_dev_view(self.dev)

    def test_a_tree_inside_a_backup_root_refuses(self):
        self.lines['PROD']['tree_root'] = self.qa_backups / 'prod'
        self.lines['PROD']['venv_dir'] = self.qa_backups / 'prod' / '.venv'
        with self.refused(r'\[QA\] backup_root .* lie one inside the other'):
            settings.read_dev_view(self.dev)

    def test_the_same_backup_root_for_qa_and_prod_refuses(self):
        self.lines['PROD']['backup_root'] = self.qa_backups
        with self.refused('backup root of its own'):
            settings.read_dev_view(self.dev)

    # ---- check 5: a backup root on its tree's own volume is allowed, with a warning

    def test_a_backup_root_on_its_trees_volume_warns_and_another_volume_does_not(self):
        self.write_dev_file()

        def invented_volume(path: Path) -> str:
            """The folder two levels under the temporary folder stands for the drive."""
            return Path(path).relative_to(Path(self.folder.name).resolve()).parts[0]

        with mock.patch.object(settings, '_volume_of', invented_volume):
            warnings = settings.read_dev_view(self.dev).warnings
        self.assertEqual(len(warnings), 1)                 # QA and its backups share 't_drive'; PROD is on 'g_drive'
        self.assertRegex(warnings[0], r'WARNING: .*\[QA\] backup_root .* same disk volume')

    def test_the_volume_of_a_folder_that_does_not_exist_yet_is_that_of_the_nearest_folder_that_does(self):
        self.assertEqual(settings._volume_of(self.qa / 'not' / 'made' / 'yet'), settings._volume_of(self.dev))

    # ---- a tool asked for a tree: DEV's entry, and check 4 (a tree is what its own file says)

    def test_a_role_with_no_section_refuses_and_says_which_sections_there_are(self):
        del self.lines['PROD']
        self.write_dev_file()
        view = settings.read_dev_view(self.dev)
        with self.assertRaisesRegex(settings.SettingsRefused, r'no section for the PROD tree \(it has: \[QA\]\)'):
            settings.entry_for(view, 'PROD')

    def test_a_role_that_is_not_qa_or_prod_refuses(self):
        self.write_dev_file()
        view = settings.read_dev_view(self.dev)
        for typed in ('DEV', 'qa', 'STAGING', ''):
            with self.subTest(typed=typed), self.assertRaisesRegex(settings.SettingsRefused, 'Type QA or PROD'):
                settings.entry_for(view, typed)

    def test_an_existing_tree_that_agrees_with_devs_entry_is_read(self):
        self.write_dev_file()
        self.write_tree_file('QA')
        found = settings.tree_as_dev_names_it(settings.read_dev_view(self.dev), 'QA')
        self.assertEqual((found.role, found.tree_root, found.backup_root), ('QA', self.qa, self.qa_backups))

    def test_a_tree_folder_with_no_settings_file_refuses(self):
        self.write_dev_file()
        self.qa.mkdir(parents=True)
        with self.assertRaisesRegex(settings.SettingsRefused, 'the settings file is missing'):
            settings.tree_as_dev_names_it(settings.read_dev_view(self.dev), 'QA')

    def test_a_tree_whose_own_file_says_another_role_refuses(self):
        self.write_dev_file()
        self.write_tree_file('QA', role='PROD')
        with self.assertRaisesRegex(settings.SettingsRefused, 'own file says it is PROD, but .* as \\[QA\\]'):
            settings.tree_as_dev_names_it(settings.read_dev_view(self.dev), 'QA')

    def test_a_tree_whose_own_file_names_another_folder_refuses(self):
        self.write_dev_file()
        self.write_tree_file('QA', tree_root=self.prod)
        with self.assertRaisesRegex(settings.SettingsRefused, 'not what its file says'):
            settings.tree_as_dev_names_it(settings.read_dev_view(self.dev), 'QA')

    def test_a_backup_root_that_differs_between_the_two_files_refuses_and_prints_both(self):
        self.write_dev_file()
        elsewhere = Path(self.folder.name).resolve() / 'f_drive' / 'backups'
        self.write_tree_file('PROD', backup_root=elsewhere)
        with self.assertRaises(settings.SettingsRefused) as caught:
            settings.tree_as_dev_names_it(settings.read_dev_view(self.dev), 'PROD')
        self.assertIn('backup_root disagrees for the PROD tree', str(caught.exception))
        self.assertIn(str(self.prod_backups), str(caught.exception))
        self.assertIn(str(elsewhere), str(caught.exception))

    def test_an_environment_folder_that_differs_between_the_two_files_refuses(self):
        self.write_dev_file()
        self.write_tree_file('QA', venv_dir=self.qa / 'another_venv')
        with self.assertRaisesRegex(settings.SettingsRefused, 'venv_dir disagrees for the QA tree'):
            settings.tree_as_dev_names_it(settings.read_dev_view(self.dev), 'QA')


class TheTrackedExample(unittest.TestCase):
    """Deployment design section 1: the owner makes DEV's file by copying the tracked example, so the example must
    hold what the reader asks for (the owner's observation of 24 November 2026, decision log entry 211)."""

    def setUp(self):
        """Parse the example as the reader parses a settings file (its paths are Windows paths, so the reader
        itself is not run on it here)."""
        import configparser
        self.example = Path(__file__).resolve().parents[1] / settings.EXAMPLE_FILE_NAME
        self.parser = configparser.ConfigParser(interpolation=None, delimiters=('=',), strict=True)
        self.parser.optionxform = str
        self.parser.read_string(self.example.read_text(encoding='ascii'), source=str(self.example))

    def test_it_holds_devs_own_section_and_an_entry_for_each_other_tree_with_every_key(self):
        self.assertEqual(self.parser.sections(), ['environment', 'QA', 'PROD'])
        self.assertEqual(sorted(self.parser['environment']), ['role', 'tree_root', 'venv_dir'])
        self.assertEqual(self.parser['environment']['role'], 'DEV')
        for role in settings.OTHER_TREE_ROLES:
            self.assertEqual(sorted(self.parser[role]), ['backup_root', 'tree_root', 'venv_dir'])

    def test_its_paths_keep_the_rules_the_reader_checks(self):
        from pathlib import PureWindowsPath as Windows
        roots = [Windows(self.parser[section]['tree_root']) for section in self.parser.sections()]
        backups = [Windows(self.parser[role]['backup_root']) for role in settings.OTHER_TREE_ROLES]
        for section in self.parser.sections():
            for key, value in self.parser[section].items():
                if key != 'role':
                    self.assertTrue(Windows(value).is_absolute(), f'[{section}] {key} is not absolute')
            self.assertIn(Windows(self.parser[section]['tree_root']), Windows(self.parser[section]['venv_dir']).parents)
        for first in roots + backups:
            for second in roots + backups:
                if first is not second:
                    self.assertNotEqual(first, second)
                    self.assertNotIn(first, second.parents, f'{second} lies inside {first}')

    def test_it_says_whose_file_it_is_and_that_init_tree_writes_the_others(self):
        text = self.example.read_text(encoding='ascii')
        for said in ('WHOSE FILE IS THIS?', 'Init_Tree.bat writes each of them once', 'This file stays in DEV',
                     'FOR COMPARISON ONLY'):
            self.assertIn(said, text)


class NoProgramWritesASettingsFile(unittest.TestCase):
    """Deployment design section 1: the reader never writes; a settings file is opened for reading only."""

    def test_the_reader_opens_nothing_for_writing(self):
        source = Path(settings.__file__).read_text(encoding='utf-8')
        for forbidden in ('write_text', 'write_bytes', "'w'", '"w"', "'a'", "'x'", 'os.replace', 'os.rename',
                          'unlink', 'mkdir'):
            self.assertNotIn(forbidden, source, f'research/settings.py holds {forbidden}: the reader must not write')


if __name__ == '__main__':
    unittest.main()
