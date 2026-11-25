"""Tests of readiness in DEV: the two markers, the static import check, and the command Make_Installable.

Each test is named for the rule it proves and plants the fault that rule must catch
(doc/CODING_PRACTICES_v0_1.md section 6; specification v0.6 sections 3.4, 4 and 12.2; deployment design v0.12
sections 3.1 and 15: "the two kinds of marker (matching; one file edited afterwards; made by hand with a wrong
hash; made twice, identical; never listing itself)" and "an imported module not listed").

Which of the project's own modules it uses
    research_fixtures      invented trees and toy variants
    install_readiness, install_import_check, make_installable (deploy/)     the code under test
    research.code_identity the manifest reader's new list of install tool files

What uses it
    The project's test suite.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# The install tools are imported from deploy/, as the launcher program imports them.
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import file_form                                            # noqa: E402  (after the path line above)
import install_import_check                                 # noqa: E402
import install_readiness                                    # noqa: E402
import make_installable                                     # noqa: E402
import research_fixtures as fixtures                        # noqa: E402
from research import code_identity, job_lock, launch_guard, variant_folders        # noqa: E402

FAMILY, VARIANT = 'E_901', 'TOY_COUNTS_V1'


def write_crlf(path: Path, text: str) -> None:
    """Write one invented file with every line ending CRLF, whatever the platform: the form the project's standard
    gives a text file, which Make_Installable now requires of everything it marks ready."""
    path.write_bytes(text.replace('\n', '\r\n').encode('ascii'))


def bring_to_form(tree: Path) -> None:
    """Bring every file of an invented tree to the form the standard gives its kind (CRLF; .jsonl LF). The shared
    fixtures write with Python's default line ending, which differs between Windows and the cloud."""
    for path in sorted(tree.rglob('*')):
        form = file_form.form_of(path.relative_to(tree).as_posix()) if path.is_file() else None
        if form in (file_form.CRLF, file_form.LF):
            path.write_bytes(file_form.to_form(path.read_bytes(), form))
HELPER = f'{FAMILY}/toy_helper_v1.py'


class InventedDev(unittest.TestCase):
    """An invented DEV tree with one toy variant that lists one helper; the base of the classes below."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.tree = fixtures.make_tree(Path(self.folder.name) / 'dev')
        self.methods = self.tree / 'src' / 'methods'
        self.variant_folder = fixtures.add_toy_variant(self.tree, FAMILY, VARIANT,
                                                       helpers=(f'{FAMILY}/__init__.py', HELPER))
        write_crlf((self.methods / HELPER), '"""An invented helper."""\nLIMIT = 3\n')
        self.marker = self.variant_folder / 'I_AM_INSTALLABLE.json'
        self.infra_marker = self.tree / 'deploy' / 'INFRA_IS_INSTALLABLE.json'
        bring_to_form(self.tree)

    def tearDown(self):
        self.folder.cleanup()

    def add_to_manifest(self, text: str) -> None:
        """Append lines to the invented tree's manifest."""
        with open(self.tree / 'deploy' / 'INFRA_MANIFEST.ini', 'a', encoding='ascii', newline='\r\n') as handle:
            handle.write(text)


class AVariantsMarker(InventedDev):
    """Specification section 4: the marker is bound to content and is the whole of readiness."""

    def test_an_unmarked_variant_is_not_ready_and_the_reason_names_the_command(self):
        found = install_readiness.variant_readiness(self.tree, FAMILY, VARIANT)
        self.assertFalse(found.ready)
        self.assertIn('it is not marked', found.reason)
        self.assertIn(f'Make_Installable.bat {FAMILY} {VARIANT}', found.reason)

    def test_a_marked_variant_is_ready_and_its_marker_holds_the_fingerprint_and_the_hashed_list(self):
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        found = install_readiness.variant_readiness(self.tree, FAMILY, VARIANT)
        self.assertTrue(found.ready, found.reason)
        content = json.loads(self.marker.read_text(encoding='ascii'))
        variant = variant_folders.read_variant(self.methods, FAMILY, VARIANT)
        self.assertEqual(content['fingerprint'], variant.fingerprint)
        self.assertEqual([(entry['path'], entry['sha256']) for entry in content['files']],
                         list(variant.fingerprint_lines))
        self.assertEqual(sorted(entry['path'] for entry in content['files']),
                         sorted([f'{FAMILY}/{VARIANT}/VARIANT.json', f'{FAMILY}/{VARIANT}/method.py',
                                 f'{FAMILY}/__init__.py', HELPER]))

    def test_the_marker_never_lists_itself_nor_the_status_file(self):
        write_crlf((self.variant_folder / 'VARIANT_STATUS.ini'), '[check]\n')
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)          # made again with the marker present
        listed = [entry['path'] for entry in json.loads(self.marker.read_text(encoding='ascii'))['files']]
        self.assertFalse([path for path in listed if 'I_AM_INSTALLABLE' in path or 'VARIANT_STATUS' in path])

    def test_made_twice_on_unchanged_files_the_marker_has_the_same_bytes_and_is_not_rewritten(self):
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        first = self.marker.read_bytes()
        # The marker is a text file of the project: every line ends CRLF (the file-form standard).
        self.assertGreater(first.count(b'\r\n'), 3)
        self.assertNotIn(b'\n', first.replace(b'\r\n', b''))
        self.marker.unlink()
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertEqual(self.marker.read_bytes(), first)
        with mock.patch.object(install_readiness, '_write_whole') as write:
            line = install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        write.assert_not_called()
        self.assertIn('already marked', line)

    def test_each_listed_file_edited_after_marking_makes_the_variant_not_ready(self):
        for edited in (self.variant_folder / 'method.py', self.variant_folder / 'VARIANT.json',
                       self.methods / HELPER, self.methods / FAMILY / '__init__.py'):
            with self.subTest(edited=edited.name):
                install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
                kept = edited.read_bytes()
                edited.write_bytes(kept + b'\r\n')
                found = install_readiness.variant_readiness(self.tree, FAMILY, VARIANT)
                self.assertFalse(found.ready)
                self.assertIn('does not match its files', found.reason)
                edited.write_bytes(kept)
                self.assertTrue(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)

    def test_a_marker_made_by_hand_with_a_wrong_hash_does_not_count(self):
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        content = json.loads(self.marker.read_text(encoding='ascii'))
        content['files'][0]['sha256'] = '0' * 64
        write_crlf(self.marker, json.dumps(content))
        self.assertFalse(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)

    def test_a_marker_made_by_hand_counts_only_if_it_holds_exactly_what_the_tool_writes(self):
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        content = json.loads(self.marker.read_text(encoding='ascii'))
        self.marker.write_bytes(json.dumps(content).replace(' ', '').encode('ascii') + b'\r\n')   # other bytes, same content
        self.assertTrue(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)
        for spoiled in (dict(content, fingerprint='0' * 64), dict(content, extra='x'),
                        {key: value for key, value in content.items() if key != 'kind'}, [content], 'ready'):
            with self.subTest(spoiled=str(spoiled)[:40]):
                write_crlf(self.marker, json.dumps(spoiled))
                self.assertFalse(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)
        write_crlf(self.marker, 'this is not JSON')
        self.assertFalse(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)

    def test_a_listed_file_that_is_not_in_the_standards_form_refuses_and_writes_no_marker(self):
        method = self.variant_folder / 'method.py'
        method.write_bytes(method.read_bytes().replace(b'\r\n', b'\n'))            # the whole file LF
        with self.assertRaisesRegex(install_readiness.ReadinessRefused,
                                    r'(?s)not in the form the project.s standard gives.*method\.py: must be CRLF'):
            install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertFalse(self.marker.exists())

    def test_an_undeclared_file_in_the_folder_refuses_and_writes_no_marker(self):
        write_crlf((self.variant_folder / 'method.py.bak'), 'an editor backup')
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, "not on the declaration's list"):
            install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertFalse(self.marker.exists())

    def test_a_missing_helper_refuses_and_writes_no_marker(self):
        (self.methods / HELPER).unlink()
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, 'helper listed in .* is missing'):
            install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertFalse(self.marker.exists())

    def test_an_interrupted_write_leaves_nothing_in_the_variant_folder(self):
        before = sorted(item.name for item in self.variant_folder.iterdir())
        with mock.patch.object(install_readiness.os, 'replace', side_effect=OSError('the PC lost power')):
            with self.assertRaises(OSError):
                install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertEqual(sorted(item.name for item in self.variant_folder.iterdir()), before)
        variant_folders.read_variant(self.methods, FAMILY, VARIANT)        # the folder is still a valid variant
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)         # and the next attempt succeeds
        self.assertTrue(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)

    def test_a_staging_folder_that_is_a_link_to_another_place_refuses(self):
        outside = Path(self.folder.name) / 'outside'
        outside.mkdir()
        (self.tree / 'records').mkdir()
        try:
            (self.tree / 'records' / 'marker_staging').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('this account cannot create a link')
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, 'No marker was written'):
            install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse(self.marker.exists())

    def test_unmark_removes_the_marker_and_says_so_when_there_is_none(self):
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertIn('was removed', install_readiness.unmark_variant(self.tree, FAMILY, VARIANT))
        self.assertFalse(self.marker.exists())
        self.assertFalse(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)
        self.assertIn('has no marker', install_readiness.unmark_variant(self.tree, FAMILY, VARIANT))
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, 'no such variant folder'):
            install_readiness.unmark_variant(self.tree, FAMILY, 'NOT_A_VARIANT_V1')


class TheStaticImportCheck(InventedDev):
    """Specification 3.4: imports are plain statements naming a listed file or the infrastructure."""

    def write_method(self, extra_lines: str) -> None:
        """Add lines of Python to the toy variant's method.py."""
        path = self.variant_folder / 'method.py'
        write_crlf(path, path.read_text(encoding='ascii') + '\n' + extra_lines + '\n')

    def refused_with(self, pattern: str) -> None:
        """Expect marking to refuse with `pattern`, to write no marker, and readiness to say not ready."""
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, pattern):
            install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertFalse(self.marker.exists())
        self.assertFalse(install_readiness.variant_readiness(self.tree, FAMILY, VARIANT).ready)

    def test_an_import_of_a_listed_helper_passes_by_every_plain_form(self):
        self.write_method(f'import {FAMILY}.toy_helper_v1\nfrom {FAMILY} import toy_helper_v1\n'
                          f'from {FAMILY}.toy_helper_v1 import LIMIT\n\n\ndef late():\n    from {FAMILY} import toy_helper_v1 as again\n    return again')
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertTrue(self.marker.exists())

    def test_an_import_of_a_project_file_on_no_list_refuses_and_names_file_and_line(self):
        write_crlf((self.methods / FAMILY / 'unlisted_v1.py'), 'VALUE = 1\n')
        self.write_method(f'from {FAMILY} import unlisted_v1')
        self.refused_with(rf'method\.py line \d+: it imports src/methods/{FAMILY}/unlisted_v1\.py, which is neither')

    def test_an_unlisted_import_made_by_a_helper_or_inside_a_function_is_found_too(self):
        write_crlf((self.methods / FAMILY / 'unlisted_v1.py'), 'VALUE = 1\n')
        write_crlf((self.methods / HELPER), f'def late():\n    import {FAMILY}.unlisted_v1\n')
        self.refused_with(r'toy_helper_v1\.py line 2: it imports')

    def test_a_relative_import_is_resolved_and_an_unlisted_one_refuses(self):
        write_crlf((self.methods / FAMILY / 'unlisted_v1.py'), 'VALUE = 1\n')
        write_crlf((self.methods / HELPER), 'from . import unlisted_v1\n')
        self.refused_with(rf'it imports src/methods/{FAMILY}/unlisted_v1\.py')
        write_crlf((self.methods / HELPER), 'from .unlisted_v1 import VALUE\n')
        self.refused_with(rf'it imports src/methods/{FAMILY}/unlisted_v1\.py')

    def test_an_import_of_infrastructure_passes_only_if_its_class_is_forecast(self):
        self.write_method('import toy_forecast_code')                 # src/toy_forecast_code.py = forecast
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.marker.unlink()
        for module, its_class in (('toy_derived_code', 'derived'), ('toy_other', 'other')):
            with self.subTest(module=module):
                kept = (self.variant_folder / 'method.py').read_text(encoding='ascii')
                self.write_method(f'import {module}')
                self.refused_with(f'an infrastructure file of class {its_class}')
                write_crlf((self.variant_folder / 'method.py'), kept)

    def test_each_way_of_importing_by_a_computed_name_refuses(self):
        for lines, found in (('import importlib', 'importlib'), ('from importlib import import_module', 'importlib'),
                             ('import importlib.util', 'importlib'), ("X = __import__('json')", '__import__'),
                             ("exec('import json')", 'exec'), ("X = eval('1')", 'eval'),
                             ("import builtins\nX = builtins.eval('1')", 'eval'),
                             ("import sys\nsys.path.insert(0, 'x')", r'sys\.path'), ('from sys import path', r'sys\.path'),
                             ('import sys\nY = sys.path', r'sys\.path'),
                             ("import sys as s\ns.path.insert(0, 'x')", r'sys\.path'),
                             ('import os, sys as system\nY = system.path', r'sys\.path')):
            with self.subTest(lines=lines):
                kept = (self.variant_folder / 'method.py').read_text(encoding='ascii')
                self.write_method(lines)
                self.refused_with(rf'method\.py line \d+: it uses {found}')
                write_crlf((self.variant_folder / 'method.py'), kept)

    def test_a_forbidden_construct_in_a_helper_refuses(self):
        write_crlf((self.methods / HELPER), 'import importlib\n')
        self.refused_with(r'toy_helper_v1\.py line 1: it uses importlib')

    def test_a_listed_file_that_is_not_valid_python_refuses(self):
        write_crlf((self.methods / HELPER), 'def broken(:\n')
        self.refused_with('cannot be read as Python')

    def test_the_words_in_a_comment_or_a_text_are_not_a_use(self):
        self.write_method('# importlib, exec and eval are only named here\nNOTE = "sys.path and __import__"')
        install_readiness.mark_variant(self.tree, FAMILY, VARIANT)
        self.assertTrue(self.marker.exists())

    def test_every_real_variant_of_this_repository_passes_the_check(self):
        manifest = code_identity.read_manifest(REPOSITORY_ROOT)
        variants, refused = variant_folders.find_variants(REPOSITORY_ROOT / 'src' / 'methods')
        self.assertEqual(refused, [])
        self.assertGreaterEqual(len(variants), 40)
        for variant in variants:
            own = [f'src/methods/{path}' for path, _ in variant.fingerprint_lines
                   if path.startswith(f'{variant.family}/{variant.variant}/')]
            helpers = [f'src/methods/{helper}' for helper in variant.declaration['helpers']]
            self.assertEqual(install_import_check.variant_import_faults(REPOSITORY_ROOT, own, helpers, manifest), [],
                             variant.identity)


class TheInfrastructuresMarker(InventedDev):
    """Specification 12.2 and deployment design 3.1: the infrastructure has a marker of the same kind."""

    def test_unmarked_it_is_not_ready_and_marked_it_is(self):
        reason = install_readiness.infrastructure_readiness(self.tree).reason
        self.assertIn('is not marked', reason)
        self.assertIn('Make_Installable.bat INFRA', reason)
        install_readiness.mark_infrastructure(self.tree)
        self.assertTrue(install_readiness.infrastructure_readiness(self.tree).ready)

    def test_it_hashes_the_manifest_every_listed_file_and_every_install_tool_file_and_never_itself(self):
        write_crlf((self.tree / 'deploy' / 'toy_tool.py'), '# an invented install tool\n')
        self.add_to_manifest('[install_tool]\ndeploy/toy_tool.py = other\n')
        install_readiness.mark_infrastructure(self.tree)
        install_readiness.mark_infrastructure(self.tree)                     # made again with the marker present
        content = json.loads(self.infra_marker.read_text(encoding='ascii'))
        self.assertEqual(content['manifest']['path'], 'deploy/INFRA_MANIFEST.ini')
        self.assertEqual([(entry['path'], entry['class']) for entry in content['files']],
                         [('src/toy_derived_code.py', 'derived'), ('src/toy_forecast_code.py', 'forecast'),
                          ('src/toy_other.py', 'other')])
        self.assertEqual([entry['path'] for entry in content['install_tool']], ['deploy/toy_tool.py'])
        everything = [content['manifest']] + content['files'] + content['install_tool']
        self.assertEqual(content['fingerprint'], variant_folders.fingerprint_of(
            (entry['path'], entry['sha256']) for entry in everything))
        self.assertNotIn('INFRA_IS_INSTALLABLE', json.dumps(content['files'] + content['install_tool']))
        for entry in everything:
            self.assertEqual(entry['sha256'], variant_folders.sha256_of_file(self.tree / entry['path']))

    def test_made_twice_on_unchanged_files_it_has_the_same_bytes(self):
        install_readiness.mark_infrastructure(self.tree)
        first = self.infra_marker.read_bytes()
        self.infra_marker.unlink()
        install_readiness.mark_infrastructure(self.tree)
        self.assertEqual(self.infra_marker.read_bytes(), first)

    def test_the_manifest_or_any_listed_file_edited_afterwards_makes_it_not_ready(self):
        write_crlf((self.tree / 'deploy' / 'toy_tool.py'), '# an invented install tool\n')
        self.add_to_manifest('[install_tool]\ndeploy/toy_tool.py = other\n')
        for edited in ('deploy/INFRA_MANIFEST.ini', 'src/toy_forecast_code.py', 'src/toy_other.py',
                       'deploy/toy_tool.py'):
            with self.subTest(edited=edited):
                install_readiness.mark_infrastructure(self.tree)
                kept = (self.tree / edited).read_bytes()
                (self.tree / edited).write_bytes(kept + b'; a later change\r\n' if edited.endswith('.ini')
                                                 else kept + b'# a later change\r\n')
                found = install_readiness.infrastructure_readiness(self.tree)
                self.assertFalse(found.ready)
                self.assertIn('does not match the files', found.reason)
                (self.tree / edited).write_bytes(kept)
                self.assertTrue(install_readiness.infrastructure_readiness(self.tree).ready)

    def test_a_marker_made_by_hand_with_a_wrong_hash_does_not_count(self):
        install_readiness.mark_infrastructure(self.tree)
        content = json.loads(self.infra_marker.read_text(encoding='ascii'))
        content['files'][1]['sha256'] = '0' * 64
        write_crlf(self.infra_marker, json.dumps(content))
        self.assertFalse(install_readiness.infrastructure_readiness(self.tree).ready)

    def test_a_listed_file_that_does_not_exist_refuses_and_writes_no_marker(self):
        (self.tree / 'src' / 'toy_other.py').unlink()
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, 'listed but does not exist'):
            install_readiness.mark_infrastructure(self.tree)
        self.assertFalse(self.infra_marker.exists())

    def test_an_imported_project_file_that_is_not_listed_refuses(self):
        write_crlf((self.tree / 'src' / 'toy_unlisted.py'), 'VALUE = 1\n')
        write_crlf((self.tree / 'src' / 'toy_derived_code.py'), 'import toy_unlisted\n')
        with self.assertRaisesRegex(install_readiness.ReadinessRefused,
                                    r'toy_derived_code\.py line 1: it imports src/toy_unlisted\.py, which is not on'):
            install_readiness.mark_infrastructure(self.tree)
        self.assertFalse(self.infra_marker.exists())
        self.add_to_manifest('src/toy_unlisted.py = derived\n')
        install_readiness.mark_infrastructure(self.tree)                     # listed, it passes

    def test_the_marker_or_the_manifest_listed_on_the_manifest_refuses(self):
        write_crlf(self.infra_marker, '{}')
        self.add_to_manifest('deploy/INFRA_IS_INSTALLABLE.json = other\n')
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, 'lists the manifest or the marker itself'):
            install_readiness.mark_infrastructure(self.tree)

    def test_an_infrastructure_file_that_is_not_in_the_standards_form_refuses_and_writes_no_marker(self):
        manifest = self.tree / 'deploy' / 'INFRA_MANIFEST.ini'
        manifest.write_bytes(manifest.read_bytes().replace(b'\r\n', b'\n'))
        with self.assertRaisesRegex(install_readiness.ReadinessRefused,
                                    r'(?s)INFRA: 1 file\(s\) are not in the form.*INFRA_MANIFEST\.ini: must be CRLF'):
            install_readiness.mark_infrastructure(self.tree)
        self.assertFalse(self.infra_marker.exists())

    def test_a_file_listed_under_both_sections_refuses(self):
        self.add_to_manifest('[install_tool]\nsrc/toy_other.py = other\n')
        with self.assertRaisesRegex(install_readiness.ReadinessRefused, r'both \[files\] and \[install_tool\]'):
            install_readiness.mark_infrastructure(self.tree)

    def test_the_real_infrastructure_imports_nothing_that_is_not_on_the_real_manifest(self):
        manifest = code_identity.read_manifest(REPOSITORY_ROOT)
        self.assertEqual(install_import_check.infrastructure_import_faults(REPOSITORY_ROOT, manifest), [])

    def test_the_real_manifest_lists_every_program_under_deploy_as_infrastructure_or_as_an_install_tool(self):
        # A program under deploy/ is either infrastructure, installed into every tree (the checker
        # deploy/file_form.py: the owner's decision of 25 November 2026, decision log entry 265), or a DEV-side
        # install tool, never installed. None may be on neither list.
        tools = set(code_identity.read_install_tool_list(REPOSITORY_ROOT))
        infrastructure = set(code_identity.read_manifest(REPOSITORY_ROOT))
        programs = {path.relative_to(REPOSITORY_ROOT).as_posix() for path in (REPOSITORY_ROOT / 'deploy').glob('*.py')}
        self.assertEqual(sorted(programs - tools - infrastructure), [])
        self.assertIn('deploy/file_form.py', infrastructure)
        self.assertNotIn('deploy/file_form.py', tools)
        self.assertIn('Make_Installable.bat', tools)
        self.assertEqual(sorted(tools & infrastructure), [])


class TheCommandMakeInstallable(InventedDev):
    """Specification section 4: one variant, several at once, the infrastructure, and --unmark."""

    def run_command(self, *typed):
        """Run the command as typed; return (the exit code, the lines it said)."""
        said = []
        return make_installable.main(list(typed), self.tree, say=said.append), said

    def test_a_family_and_a_variant_as_two_words_marks_that_variant(self):
        code, said = self.run_command(FAMILY, VARIANT)
        self.assertEqual(code, 0)
        self.assertTrue(self.marker.exists())
        self.assertRegex(said[0], rf'MAKE INSTALLABLE - START - tree DEV .* to mark ready: {FAMILY}/{VARIANT}')
        self.assertEqual(said[-1], 'MAKE INSTALLABLE - END - 1 done, 0 REFUSED')

    def test_several_things_at_once_are_each_done_and_one_refusal_does_not_stop_the_others(self):
        second = fixtures.add_toy_variant(self.tree, 'E_902', 'TOY_OTHER_V1')
        write_crlf((second / 'scratch.txt'), 'left by an editor')
        code, said = self.run_command(f'{FAMILY}/{VARIANT}', 'E_902/TOY_OTHER_V1', 'INFRA')
        self.assertEqual(code, 1)
        self.assertTrue(self.marker.exists())
        self.assertTrue(self.infra_marker.exists())
        self.assertFalse((second / 'I_AM_INSTALLABLE.json').exists())
        self.assertEqual(len([line for line in said if line.startswith('REFUSED: ')]), 1)
        self.assertTrue(said[-1].startswith('MAKE INSTALLABLE - END - 2 done, 1 REFUSED. What was refused is not ready'))

    def test_an_unfinished_operation_or_the_orphan_marker_refuses_and_no_marker_is_made_or_removed(self):
        self.assertEqual(self.run_command('INFRA')[0], 0)    # so that --unmark would have a marker to remove
        for relative in (launch_guard.UNFINISHED_OPERATIONS[1][0], job_lock.ORPHAN_MARKER):
            with self.subTest(relative=relative):
                barrier = self.tree / relative
                barrier.parent.mkdir(parents=True, exist_ok=True)
                barrier.write_bytes(b'{}\r\n')
                before = fixtures.files_under(self.tree, '.')
                for typed in ((FAMILY, VARIANT), ('INFRA', '--unmark'), (f'{FAMILY}/{VARIANT}', 'INFRA')):
                    code, said = self.run_command(*typed)
                    self.assertEqual(code, 2, said)
                    self.assertEqual(len(said), 1, said)
                    self.assertRegex(said[0], r'^REFUSED: .* No readiness marker was made or removed\.$')
                self.assertIn(str(barrier), said[0])
                self.assertEqual(fixtures.files_under(self.tree, '.'), before)
                barrier.unlink()
        self.assertFalse(self.marker.exists())
        self.assertTrue(self.infra_marker.exists())
        self.assertEqual(self.run_command(FAMILY, VARIANT)[0], 0)

    def test_unmark_removes_the_markers_named(self):
        self.run_command(f'{FAMILY}/{VARIANT}', 'INFRA')
        code, said = self.run_command('--unmark', f'{FAMILY}/{VARIANT}', 'INFRA')
        self.assertEqual(code, 0)
        self.assertFalse(self.marker.exists())
        self.assertFalse(self.infra_marker.exists())
        self.assertIn('to remove the readiness marker of', said[0])

    def test_what_cannot_be_understood_does_nothing_and_shows_the_usage(self):
        for typed in ((), ('--unmark',), (FAMILY,), ('../../outside', 'x'), (f'{FAMILY}/{VARIANT}/more',),
                      ('E_901/lowercase',), (FAMILY, VARIANT, 'INFRA'), ('e_901/TOY_COUNTS_V1',)):
            with self.subTest(typed=typed):
                code, said = self.run_command(*typed)
                self.assertEqual(code, 2)
                self.assertIn('Nothing was done', said[0])
                self.assertIn('Usage:', said[0])
                self.assertFalse(self.marker.exists())

    def test_a_thing_named_twice_is_done_once(self):
        code, said = self.run_command(f'{FAMILY}/{VARIANT}', f'{FAMILY}/{VARIANT}')
        self.assertEqual((code, said[-1]), (0, 'MAKE INSTALLABLE - END - 1 done, 0 REFUSED'))


if __name__ == '__main__':
    unittest.main()
