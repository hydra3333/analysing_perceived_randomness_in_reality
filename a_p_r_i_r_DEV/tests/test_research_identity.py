"""Tests of the engine's identity code: the settings file, method folders and their fingerprints, and the engine's
own fingerprint.

Each test is named for the rule it proves and plants the fault that rule must catch.
(The simple scheme v0.2 section 4; the settings file is still the first form and is replaced in step 4 of the work
order, with its tests.)
"""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import research_fixtures as fixtures
from research import code_identity, method_flags, settings, variant_folders


class SettingsFile(unittest.TestCase):
    """Specification section 2 and deployment design section 1: a tree is what its own file says."""

    def setUp(self):
        """An invented DEV tree in a temporary folder."""
        self.folder = tempfile.TemporaryDirectory()
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'dev')

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def edit(self, old: str, new: str) -> None:
        """Replace one piece of text in the tree's settings file."""
        path = self.tree / 'ENVIRONMENT.ini'
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def test_a_valid_file_gives_the_role_and_the_roots(self):
        found = settings.read_settings(self.tree)
        self.assertEqual((found.role, found.tree_root, found.backup_root, found.results_copy_from),
                         ('DEV', self.tree, None, None))

    def test_a_missing_file_refuses_and_says_how_to_make_it(self):
        (self.tree / 'ENVIRONMENT.ini').unlink()
        with self.assertRaisesRegex(settings.SettingsRefused, 'ENVIRONMENT.example.ini'):
            settings.read_settings(self.tree)

    def test_a_missing_key_refuses_naming_file_section_and_key(self):
        self.edit(f'venv_dir = {self.tree / ".venv"}\n', '')
        with self.assertRaisesRegex(settings.SettingsRefused, r'\[environment\] venv_dir'):
            settings.read_settings(self.tree)

    def test_an_unknown_role_refuses(self):
        self.edit('role = DEV', 'role = STAGING')
        with self.assertRaisesRegex(settings.SettingsRefused, 'STAGING'):
            settings.read_settings(self.tree)

    def test_a_tree_copied_to_another_place_refuses(self):
        other = fixtures.make_tree(Path(self.folder.name) / 'copy')
        (other / 'ENVIRONMENT.ini').write_text((self.tree / 'ENVIRONMENT.ini').read_text())
        with self.assertRaisesRegex(settings.SettingsRefused, 'not what its file says'):
            settings.read_settings(other)

    def test_a_relative_path_refuses(self):
        self.edit(f'tree_root = {self.tree}', 'tree_root = some/folder')
        with self.assertRaisesRegex(settings.SettingsRefused, 'not an absolute path'):
            settings.read_settings(self.tree)

    def test_a_path_through_a_link_refuses(self):
        link = Path(self.folder.name) / 'link'
        try:
            link.symlink_to(self.tree, target_is_directory=True)
        except OSError:
            self.skipTest('this account cannot create a symbolic link')
        self.edit(f'tree_root = {self.tree}', f'tree_root = {link}')
        with self.assertRaisesRegex(settings.SettingsRefused, 'not its own real path'):
            settings.read_settings(link)

    def test_an_environment_folder_outside_the_tree_refuses(self):
        self.edit(f'venv_dir = {self.tree / ".venv"}', f'venv_dir = {self.tree.parent / "elsewhere"}')
        with self.assertRaisesRegex(settings.SettingsRefused, 'not inside the tree'):
            settings.read_settings(self.tree)

    def test_a_backup_root_inside_the_tree_refuses(self):
        qa = fixtures.make_tree(Path(self.folder.name) / 'qa', role='QA')
        path = qa / 'ENVIRONMENT.ini'
        path.write_text(path.read_text().replace(f'backup_root = {qa.parent / "qa_backups"}',
                                                 f'backup_root = {qa / "backups"}'))
        with self.assertRaisesRegex(settings.SettingsRefused, 'outside the tree'):
            settings.read_settings(qa)

class VariantFolders(unittest.TestCase):
    """Specification 3.4: the declaration, the folder's files, and the fingerprint."""

    def setUp(self):
        """An invented tree with one toy variant that lists one helper."""
        self.folder = tempfile.TemporaryDirectory()
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'dev')
        self.methods = self.tree / 'src' / 'methods'
        (self.methods / '_shared').mkdir()
        (self.methods / '_shared' / 'toy_helper_v1.py').write_text('VALUE = 1\n')
        self.variant_folder = fixtures.add_toy_variant(self.tree, 'E_901', 'TOY_COUNTS_V1',
                                                       helpers=['_shared/toy_helper_v1.py'])

    def tearDown(self):
        """Remove the temporary folder."""
        self.folder.cleanup()

    def fingerprint(self) -> str:
        """The toy variant's fingerprint as the tree stands."""
        return variant_folders.read_variant(self.methods, 'E_901', 'TOY_COUNTS_V1').fingerprint

    def rewrite_declaration(self, **changes) -> None:
        """Change keys of the toy variant's VARIANT.json (None removes a key)."""
        path = self.variant_folder / 'VARIANT.json'
        declaration = json.loads(path.read_text())
        for key, value in changes.items():
            if value is None:
                declaration.pop(key)
            else:
                declaration[key] = value
        path.write_text(json.dumps(declaration))

    def test_the_fingerprint_is_the_sha256_of_the_sorted_hashed_file_list(self):
        variant = variant_folders.read_variant(self.methods, 'E_901', 'TOY_COUNTS_V1')
        self.assertEqual([path for path, _ in variant.fingerprint_lines],
                         ['E_901/TOY_COUNTS_V1/VARIANT.json', 'E_901/TOY_COUNTS_V1/method.py',
                          '_shared/toy_helper_v1.py'])
        self.assertEqual(variant.fingerprint, variant_folders.fingerprint_of(variant.fingerprint_lines))
        self.assertEqual(variant.method_id, 'E_901')
        self.assertEqual(variant.fingerprint, self.fingerprint())

    def test_a_changed_byte_in_each_listed_file_changes_the_fingerprint(self):
        for path in (self.variant_folder / 'method.py', self.variant_folder / 'VARIANT.json',
                     self.methods / '_shared' / 'toy_helper_v1.py'):
            before, original = self.fingerprint(), path.read_bytes()
            path.write_bytes(original + b'\n')
            self.assertNotEqual(self.fingerprint(), before, path.name)
            path.write_bytes(original)
            self.assertEqual(self.fingerprint(), before)

    def test_the_three_small_files_and_pythons_cache_do_not_enter_the_fingerprint(self):
        before = self.fingerprint()
        for name in method_flags.PASSED_OVER_NAMES:
            (self.variant_folder / name).write_text('x')
        (self.variant_folder / '__pycache__').mkdir()
        (self.variant_folder / '__pycache__' / 'method.cpython-315.pyc').write_bytes(b'\0')
        self.assertEqual(self.fingerprint(), before)

    def test_an_editors_backup_file_in_the_folder_is_named_and_refused(self):
        (self.variant_folder / 'method.py.bak').write_text('x')
        with self.assertRaisesRegex(variant_folders.VariantRefused, r'method\.py\.bak.*remove it or list it'):
            self.fingerprint()

    def test_a_missing_helper_and_a_missing_listed_file_refuse(self):
        (self.methods / '_shared' / 'toy_helper_v1.py').unlink()
        with self.assertRaisesRegex(variant_folders.VariantRefused, 'toy_helper_v1.py.*missing'):
            self.fingerprint()
        self.rewrite_declaration(helpers=[], files=['method.py', 'extra.py'])
        with self.assertRaisesRegex(variant_folders.VariantRefused, 'extra.py.*missing'):
            self.fingerprint()

    def test_each_fault_in_a_declaration_refuses(self):
        original = (self.variant_folder / 'VARIANT.json').read_text()
        for changes, message in (
                ({'title': None}, 'exactly the keys'),
                ({'variant': 'OTHER_NAME_V1'}, 'equal the folder names'),
                ({'games': ['POWERBALL', 'KENO'], 'minimum_earlier_draws': {'POWERBALL': 3, 'KENO': 3}}, 'not a game'),
                ({'minimum_earlier_draws': {'POWERBALL': 0, 'OZLOTTO': 3}}, 'whole number of 1 or more'),
                ({'minimum_earlier_draws': {'POWERBALL': 3}}, 'exactly those games'),
                ({'observation_view': 'EVERYTHING'}, 'observation_view'),
                ({'files': ['other.py']}, 'method.py among them'),
                ({'helpers': ['..\\\\outside.py']}, 'forward slashes'),
                ({'helpers': ['../outside.py']}, 'forward slashes')):
            (self.variant_folder / 'VARIANT.json').write_text(original)
            self.rewrite_declaration(**changes)
            with self.assertRaisesRegex(variant_folders.VariantRefused, message, msg=str(changes)):
                self.fingerprint()

    def test_find_variants_returns_valid_folders_and_names_refused_ones(self):
        fixtures.add_toy_variant(self.tree, 'E_901', 'TOY_BROKEN_V1')
        (self.methods / 'E_901' / 'TOY_BROKEN_V1' / 'scratch.txt').write_text('x')
        (self.methods / 'E_901' / '__pycache__').mkdir()
        (self.methods / 'not_a_family').mkdir()
        found, refused = variant_folders.find_variants(self.methods)
        self.assertEqual([v.identity for v in found], ['E_901/TOY_COUNTS_V1'])
        self.assertEqual([identity for identity, _ in refused], ['E_901/TOY_BROKEN_V1'])
        self.assertIn('scratch.txt', refused[0][1])

    def test_load_method_imports_this_trees_file_and_refuses_another_trees(self):
        variant = variant_folders.read_variant(self.methods, 'E_901', 'TOY_COUNTS_V1')
        with fixtures.ImportPath(self.tree):
            module = variant_folders.load_method(variant)
            self.assertEqual(Path(module.__file__).resolve(), (self.variant_folder / 'method.py').resolve())
            other = fixtures.make_tree(Path(self.folder.name) / 'other')
            fixtures.add_toy_variant(other, 'E_901', 'TOY_COUNTS_V1')
            elsewhere = variant_folders.read_variant(other / 'src' / 'methods', 'E_901', 'TOY_COUNTS_V1')
            with self.assertRaisesRegex(variant_folders.VariantRefused, 'Another tree'):
                variant_folders.load_method(elsewhere)

    def test_a_method_file_without_verify_refuses(self):
        path = self.variant_folder / 'method.py'
        path.write_text(path.read_text().replace('def verify(', 'def check('))
        with fixtures.ImportPath(self.tree):
            with self.assertRaisesRegex(variant_folders.VariantRefused, r'no verify\(\)'):
                variant_folders.load_method(variant_folders.read_variant(self.methods, 'E_901', 'TOY_COUNTS_V1'))


class TheEnginesFingerprint(unittest.TestCase):
    """Scheme section 4: one SHA-256 over every file under src/ outside the method families."""

    def setUp(self):
        """An invented tree with one engine file, a shared module and one method."""
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'dev')
        (self.tree / 'src' / 'methods' / '_common').mkdir()
        (self.tree / 'src' / 'methods' / '_common' / 'shared.py').write_text('# shared\n', encoding='ascii')
        self.method = fixtures.add_toy_variant(self.tree, 'E_901', 'TOY_A_V1')

    def test_it_is_the_sha256_of_the_sorted_hashed_file_list(self):
        files = code_identity.infrastructure_files(self.tree)
        self.assertEqual(files, ['src/methods/_common/shared.py', f'src/{fixtures.ENGINE_FILE}'])
        text = ''.join(f'{name}\t{hashlib.sha256((self.tree / name).read_bytes()).hexdigest()}\n' for name in files)
        self.assertEqual(code_identity.infrastructure_fingerprint(self.tree),
                         hashlib.sha256(text.encode('utf-8')).hexdigest())

    def test_a_changed_added_or_removed_engine_file_changes_it(self):
        seen = {code_identity.infrastructure_fingerprint(self.tree)}
        (self.tree / 'src' / fixtures.ENGINE_FILE).write_text('# changed\n', encoding='ascii')
        seen.add(code_identity.infrastructure_fingerprint(self.tree))
        (self.tree / 'src' / 'research').mkdir()
        (self.tree / 'src' / 'research' / 'new_module.py').write_text('# new\n', encoding='ascii')
        seen.add(code_identity.infrastructure_fingerprint(self.tree))
        (self.tree / 'src' / 'methods' / '_common' / 'shared.py').unlink()
        seen.add(code_identity.infrastructure_fingerprint(self.tree))
        self.assertEqual(len(seen), 4)

    def test_the_methods_the_small_files_and_pythons_cache_are_not_part_of_it(self):
        before = code_identity.infrastructure_fingerprint(self.tree)
        (self.method / 'method.py').write_text('# another method\n', encoding='ascii')
        (self.method.parent / 'family_helper.py').write_text('# a helper of the family\n', encoding='ascii')
        (self.tree / 'src' / 'methods' / '_shared').mkdir()
        (self.tree / 'src' / 'methods' / '_shared' / 'helper.py').write_text('# a helper methods list\n', encoding='ascii')
        for name in method_flags.PASSED_OVER_NAMES:
            (self.tree / 'src' / name).write_bytes(b'; a flag\r\n')
            (self.method / name).write_bytes(b'; a flag\r\n')
        (self.tree / 'src' / '__pycache__').mkdir()
        (self.tree / 'src' / '__pycache__' / 'toy_engine.cpython-315.pyc').write_bytes(b'\0')
        self.assertEqual(code_identity.infrastructure_fingerprint(self.tree), before)

    def test_it_is_kept_beside_the_results_and_read_back(self):
        self.assertIsNone(code_identity.stored_fingerprint(self.tree))
        code_identity.store_fingerprint(self.tree, 'ab12')
        self.assertEqual(code_identity.stored_fingerprint(self.tree), 'ab12')
        path = self.tree / 'results' / 'research' / code_identity.STORED_NAME
        self.assertTrue(path.read_bytes().endswith(b'fingerprint = ab12\r\n'))
        path.write_bytes(b'damaged')
        self.assertIsNone(code_identity.stored_fingerprint(self.tree), 'unreadable is the same as not kept')


if __name__ == '__main__':
    unittest.main()
