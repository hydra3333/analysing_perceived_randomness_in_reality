"""Tests of a tree's list of installed files (records/INSTALLED_FILES.json).

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; specification v0.6 section 4; deployment design v0.12 sections 2, 8 and 9:
the list holds every installed software file with its SHA-256, each variant's fingerprint and each status file by
name only; a tree that differs from its list is named file by file; nothing else lies under src).

Which of the project's own modules it uses
    research_fixtures           invented trees and toy variants
    test_trees_readiness        write_crlf, bring_to_form: an invented tree in the form the standard gives its files
    research.installed_files    the code under test
    research.status_file, research.variant_folders, research.code_identity    what the list is made from

What uses it
    The project's test suite.
"""
import tempfile
import unittest
from pathlib import Path

import research_fixtures as fixtures
from research import code_identity, installed_files, status_file, variant_folders
from test_trees_readiness import bring_to_form, write_crlf

FAMILY, VARIANT = 'E_901', 'TOY_COUNTS_V1'
HELPER = f'{FAMILY}/toy_helper_v1.py'
GAMES = ('POWERBALL', 'OZLOTTO')


class InventedInstalledTree(unittest.TestCase):
    """An invented QA tree with one installed toy variant, its helper, its status file and its list."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'qa', role='QA')
        self.methods = self.tree / 'src' / 'methods'
        self.variant_folder = fixtures.add_toy_variant(self.tree, FAMILY, VARIANT, games=GAMES,
                                                       helpers=(f'{FAMILY}/__init__.py', HELPER))
        write_crlf(self.methods / HELPER, '"""An invented helper."""\nLIMIT = 3\n')
        bring_to_form(self.tree)
        self.status = self.variant_folder / 'VARIANT_STATUS.ini'
        status_file.create_active(self.status, FAMILY, VARIANT, GAMES)
        installed_files.write_list(self.tree, installed_files.software_now(self.tree))
        self.content = installed_files.read_list(self.tree)

    def tearDown(self):
        self.folder.cleanup()

    def differences(self) -> list:
        """The tree against the list made in setUp."""
        return installed_files.differences(self.tree, self.content)


class WhatTheListHolds(InventedInstalledTree):
    """Deployment design section 2: every installed software file with its SHA-256, each variant's fingerprint,
    and each status file by name only."""

    def test_it_holds_the_manifest_the_infrastructure_and_each_variants_files_and_helpers_each_once(self):
        paths = [entry['path'] for entry in self.content['files']]
        self.assertEqual(paths, sorted(['deploy/INFRA_MANIFEST.ini', 'src/toy_forecast_code.py',
                                        'src/toy_derived_code.py', 'src/toy_other.py',
                                        f'src/methods/{FAMILY}/{VARIANT}/VARIANT.json',
                                        f'src/methods/{FAMILY}/{VARIANT}/method.py',
                                        f'src/methods/{FAMILY}/__init__.py', f'src/methods/{HELPER}']))
        for entry in self.content['files']:
            self.assertEqual(entry['sha256'], variant_folders.sha256_of_file(self.tree / entry['path']))

    def test_it_holds_each_variants_fingerprint(self):
        variant = variant_folders.read_variant(self.methods, FAMILY, VARIANT)
        self.assertEqual(self.content['variants'],
                         [{'family': FAMILY, 'variant': VARIANT, 'fingerprint': variant.fingerprint}])

    def test_a_status_file_is_on_it_by_name_only_never_with_a_hash(self):
        name = f'src/methods/{FAMILY}/{VARIANT}/VARIANT_STATUS.ini'
        self.assertEqual(self.content['status_files'], [name])
        self.assertNotIn(name, [entry['path'] for entry in self.content['files']])

    def test_the_same_software_gives_the_same_bytes_and_every_line_ends_crlf(self):
        first = (self.tree / installed_files.LIST_PATH).read_bytes()
        installed_files.write_list(self.tree, installed_files.software_now(self.tree))
        self.assertEqual((self.tree / installed_files.LIST_PATH).read_bytes(), first)
        self.assertGreater(first.count(b'\r\n'), 10)
        self.assertEqual(first.count(b'\n'), first.count(b'\r\n'))

    def test_it_is_written_whole_and_no_temporary_file_is_left(self):
        self.assertEqual(sorted(path.name for path in (self.tree / 'records').iterdir()
                                if path.name.startswith('INSTALLED_FILES')), ['INSTALLED_FILES.json'])

    def test_a_variant_folder_that_fails_its_checks_refuses_the_making_of_a_list(self):
        write_crlf(self.variant_folder / 'notes.py', '# an editor left this\n')
        with self.assertRaisesRegex(installed_files.InstalledFilesRefused, 'not on the declaration'):
            installed_files.software_now(self.tree)

    def test_a_records_folder_that_is_not_a_folder_refuses_the_write_and_writes_nothing(self):
        other = fixtures.make_tree(Path(self.folder.name) / 'other', role='QA')
        bring_to_form(other)
        (other / 'records').write_bytes(b'not a folder\r\n')
        with self.assertRaisesRegex(installed_files.InstalledFilesRefused, 'was not written'):
            installed_files.write_list(other, installed_files.software_now(other))
        self.assertEqual((other / 'records').read_bytes(), b'not a folder\r\n')


class ReadingTheList(InventedInstalledTree):
    """A file is the tree's list only if it is one."""

    def test_a_tree_with_no_list_refuses_and_names_init_tree(self):
        (self.tree / installed_files.LIST_PATH).unlink()
        with self.assertRaisesRegex(installed_files.InstalledFilesRefused, 'no list of installed files.*Init_Tree'):
            installed_files.read_list(self.tree)

    def test_a_file_that_is_not_json_refuses(self):
        (self.tree / installed_files.LIST_PATH).write_bytes(b'{ not json\r\n')
        with self.assertRaisesRegex(installed_files.InstalledFilesRefused, 'not readable JSON'):
            installed_files.read_list(self.tree)

    def test_a_json_file_of_another_kind_or_with_a_part_missing_refuses(self):
        for change in ({'kind': 'SOMETHING_ELSE'}, {'files': 'none'}, {'status_files': None}):
            with self.subTest(change=change):
                damaged = {**self.content, **change}
                (self.tree / installed_files.LIST_PATH).write_bytes(installed_files.list_bytes(damaged))
                with self.assertRaisesRegex(installed_files.InstalledFilesRefused, 'not a list of installed files'):
                    installed_files.read_list(self.tree)
        without_a_part = {key: value for key, value in self.content.items() if key != 'variants'}
        (self.tree / installed_files.LIST_PATH).write_bytes(installed_files.list_bytes(without_a_part))
        with self.assertRaisesRegex(installed_files.InstalledFilesRefused, 'not a list of installed files'):
            installed_files.read_list(self.tree)


class ATreeAgainstItsList(InventedInstalledTree):
    """Deployment design sections 8 and 9: a tree that differs from its list is named, file by file; nothing else
    lies under src; a status file's content is free to change."""

    def test_a_tree_as_it_was_installed_has_no_difference(self):
        self.assertEqual(self.differences(), [])

    def test_a_legitimate_change_of_a_status_file_is_no_difference(self):
        statuses = status_file.read_status(self.status, GAMES)
        statuses['POWERBALL'] = status_file.with_withdrawal(statuses['POWERBALL'], 1161, 'an invented reason',
                                                            'recorded for the test')
        status_file.write_status(self.status, FAMILY, VARIANT, statuses)
        self.assertEqual(self.differences(), [])

    def test_a_helper_changed_outside_the_tools_is_named(self):
        with open(self.methods / HELPER, 'ab') as handle:
            handle.write(b'LIMIT = 4\r\n')
        self.assertEqual(self.differences(),
                         [f'src/methods/{HELPER}: its bytes are not the bytes that were installed'])

    def test_a_listed_file_that_is_missing_is_named(self):
        (self.tree / 'src' / 'toy_other.py').unlink()
        self.assertEqual(self.differences(), ['src/toy_other.py: it is on the list of installed files and is missing'])

    def test_a_status_file_is_known_to_belong_under_src_and_its_presence_is_left_to_the_jobs_own_check(self):
        # With the status file listed by name, it is never taken for a stray file; without the name it would be.
        unnamed = {**self.content, 'status_files': []}
        self.assertEqual(installed_files.differences(self.tree, unnamed),
                         [f'src/methods/{FAMILY}/{VARIANT}/VARIANT_STATUS.ini: it lies under src and is not on the '
                          f'list of installed files'])
        self.status.unlink()
        self.assertEqual(self.differences(), [])

    def test_an_unlisted_python_file_under_src_is_named(self):
        write_crlf(self.tree / 'src' / 'stray.py', '# not installed by any command\n')
        self.assertEqual(self.differences(),
                         ['src/stray.py: it lies under src and is not on the list of installed files'])

    def test_pythons_cache_folder_under_src_is_named_once_and_is_not_entered(self):
        cache = self.tree / 'src' / '__pycache__'
        cache.mkdir()
        (cache / 'toy_other.cpython-315.pyc').write_bytes(b'\x00')
        (cache / 'another.cpython-315.pyc').write_bytes(b'\x00')
        found = self.differences()
        self.assertEqual(len(found), 1)
        self.assertRegex(found[0], r"^src/__pycache__: Python's cache folder")

    def test_a_folder_link_under_src_is_named_and_nothing_behind_it_is_read(self):
        outside = Path(self.folder.name) / 'outside'
        outside.mkdir()
        write_crlf(outside / 'hidden.py', '# behind a link\n')
        if fixtures.make_folder_link(self.tree / 'src' / 'linked', outside) is None:
            self.skipTest('this account cannot make a folder link')
        found = self.differences()
        self.assertEqual(len(found), 1)
        self.assertRegex(found[0], '^src/linked: a link or a junction')

    def test_a_file_outside_src_is_not_this_checks_business(self):
        write_crlf(self.tree / 'scratch_note.txt', 'the owner may keep a note beside the launchers\n')
        self.assertEqual(self.differences(), [])


class TheManifestInAnInstalledTree(InventedInstalledTree):
    """Specification 12.4: the install tool's own files are never installed in a QA or PROD tree, whose manifest
    still names them. The manifest must be readable there, and DEV must still refuse a missing tool file."""

    def setUp(self):
        super().setUp()
        with open(self.tree / 'deploy' / 'INFRA_MANIFEST.ini', 'a', encoding='ascii', newline='\r\n') as handle:
            handle.write('[install_tool]\ndeploy/a_tool_that_lies_in_dev_only.py = other\n')

    def test_the_engine_reads_the_manifest_of_a_tree_that_does_not_hold_the_install_tools(self):
        self.assertIn('src/toy_other.py', code_identity.read_manifest(self.tree))
        self.assertEqual(len(installed_files.software_now(self.tree)['files']), len(self.content['files']))

    def test_asking_for_the_install_tools_still_refuses_one_that_is_missing(self):
        with self.assertRaisesRegex(code_identity.ManifestRefused, 'listed but does not exist'):
            code_identity.read_install_tool_list(self.tree)

    def test_an_infrastructure_file_that_is_missing_still_refuses_everywhere(self):
        (self.tree / 'src' / 'toy_other.py').unlink()
        with self.assertRaisesRegex(code_identity.ManifestRefused, 'listed but does not exist'):
            code_identity.read_manifest(self.tree)


if __name__ == '__main__':
    unittest.main()
