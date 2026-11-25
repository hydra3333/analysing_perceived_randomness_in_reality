"""Tests of deploy/install_common.py: what every install shares (build step 3, slice C, part C2).

What this file is for
    It shows, on invented trees in temporary folders, that what DEV offers is exactly what its markers cover; that
    a plan has one form; that the barrier tells this install from another (deployment design section 8); that a
    file is put in place only with the plan's bytes and that no installed file is changed unless the plan
    overwrites it; that a plan stopped part-way is finished by carrying it out again; that the tree's software
    is checked whole against the plan; that the ending writes the list, the log line and removes the barrier
    last; that the target is reserved before anything in it is changed; that the one question tells the backup's
    and the kit's results exactly and that only YES is yes; and how the checks are asked of the target's own
    Python.

Which of the project's own modules it uses
    deploy/install_common.py, deploy/install_readiness.py; research.installed_files, research.snapshot,
    research.status_file; the fixtures of tests/research_fixtures.py and tests/test_trees_readiness.py.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT / 'deploy') not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT / 'deploy'))

import install_common as common                             # noqa: E402  (after the path line above)
import install_readiness                                    # noqa: E402
import recovery_kit                                         # noqa: E402
import research_fixtures as fixtures                        # noqa: E402
import suite_on_copy                                        # noqa: E402
from research import installed_files, job_lock, process_rule, snapshot, status_file, tree_checks    # noqa: E402
from research.settings import read_settings                 # noqa: E402
from test_trees_readiness import bring_to_form, write_crlf  # noqa: E402

FAMILY, FIRST, SECOND = 'E_901', 'TOY_COUNTS_V1', 'TOY_COUNTS_V2'
HELPER = f'{FAMILY}/toy_helper_v1.py'
GAMES = ('POWERBALL', 'OZLOTTO')
METHODS = 'src/methods'


def whole_tree(tree: Path) -> dict:
    """Every file of a folder with the SHA-256 of its bytes."""
    return {path.relative_to(tree).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(tree.rglob('*')) if path.is_file()}


def sha(path: Path) -> str:
    """The SHA-256 of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


class InventedDevAndTarget(unittest.TestCase):
    """An invented DEV whose infrastructure and first toy variant are marked ready, and an empty target folder."""

    def setUp(self):
        """Make DEV and mark it; the target is an empty folder."""
        self._temporary = tempfile.TemporaryDirectory()
        base = Path(self._temporary.name).resolve()
        self.dev = fixtures.make_tree(base / 'dev')
        self.target = base / 'target'
        self.target.mkdir()
        self.add_variant(FIRST)
        install_readiness.mark_infrastructure(self.dev)
        self.clock = lambda: fixtures.FIXED_TIME

    def tearDown(self):
        """Remove everything."""
        self._temporary.cleanup()

    def add_variant(self, name: str, mark: bool = True) -> Path:
        """Add a toy variant to DEV, with the family's helper, in the standard's form; mark it unless told not."""
        folder = fixtures.add_toy_variant(self.dev, FAMILY, name, games=GAMES,
                                          helpers=(f'{FAMILY}/__init__.py', HELPER))
        write_crlf(self.dev / METHODS / HELPER, '"""An invented helper."""\nLIMIT = 3\n')
        bring_to_form(self.dev)
        if mark:
            install_readiness.mark_variant(self.dev, FAMILY, name)
        return folder

    def creation_plan(self) -> dict:
        """The plan of a tree's creation from DEV as it stands: the infrastructure and every ready variant."""
        infrastructure = common.dev_infrastructure(self.dev)
        ready, _ = common.dev_variants(self.dev)
        add = dict(infrastructure['files'])
        for entry in ready.values():
            add.update(entry['files'])
        return common.make_plan(common.INIT, 'QA', self.target, add, variants=ready.values(),
                                infrastructure_fingerprint=infrastructure['fingerprint'])

    def installed(self) -> tuple:
        """Carry the creation plan out whole; return (the plan, the list the tree must have)."""
        plan = self.creation_plan()
        common.write_barrier(self.target, plan, 'now')
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        common.create_status_files(self.target, plan)
        expected = common.expected_list(None, plan)
        common.finish(self.target, plan, expected, self.clock)
        return plan, expected


class WhatDevOffers(InventedDevAndTarget):
    """Deployment design 3.1: what can be installed from DEV, and only this."""

    def test_the_infrastructure_is_the_manifest_and_its_files_with_the_markers_hashes(self):
        offered = common.dev_infrastructure(self.dev)
        self.assertEqual(sorted(offered['files']), ['deploy/INFRA_MANIFEST.ini', 'src/toy_derived_code.py',
                                                    'src/toy_forecast_code.py', 'src/toy_other.py'])
        self.assertEqual(offered['files']['src/toy_other.py'], sha(self.dev / 'src' / 'toy_other.py'))
        self.assertEqual(offered['classes']['src/toy_forecast_code.py'], 'forecast')
        self.assertEqual(offered['fingerprint'], install_readiness.infrastructure_readiness(self.dev).fingerprint)

    def test_an_install_tool_file_is_in_the_fingerprint_and_is_never_offered(self):
        write_crlf(self.dev / 'deploy' / 'toy_tool.py', '"""An invented install tool."""\n')
        with open(self.dev / 'deploy' / 'INFRA_MANIFEST.ini', 'a', encoding='ascii', newline='\r\n') as handle:
            handle.write('[install_tool]\ndeploy/toy_tool.py = other\n')
        with self.assertRaises(common.InstallRefused):   # the manifest changed: the marker no longer matches
            common.dev_infrastructure(self.dev)
        install_readiness.mark_infrastructure(self.dev)
        self.assertNotIn('deploy/toy_tool.py', common.dev_infrastructure(self.dev)['files'])

    def test_infrastructure_that_is_not_marked_or_changed_since_is_refused_with_the_command_to_run(self):
        (self.dev / 'src' / 'toy_other.py').write_bytes(b'# changed after it was marked\r\n')
        with self.assertRaisesRegex(common.InstallRefused, 'Make_Installable.bat INFRA'):
            common.dev_infrastructure(self.dev)

    def test_a_ready_variant_is_offered_with_its_declaration_its_files_and_its_helpers_and_nothing_else(self):
        ready, not_ready = common.dev_variants(self.dev)
        self.assertEqual((list(ready), not_ready), ([f'{FAMILY}/{FIRST}'], {}))
        entry = ready[f'{FAMILY}/{FIRST}']
        self.assertEqual(sorted(entry['files']), [f'{METHODS}/{FAMILY}/{FIRST}/VARIANT.json',
                                                  f'{METHODS}/{FAMILY}/{FIRST}/method.py',
                                                  f'{METHODS}/{FAMILY}/__init__.py', f'{METHODS}/{HELPER}'])
        self.assertEqual(entry['files'][f'{METHODS}/{HELPER}'], sha(self.dev / METHODS / HELPER))
        self.assertEqual((entry['games'], entry['family'], entry['variant']), (list(GAMES), FAMILY, FIRST))

    def test_a_variant_that_is_not_marked_or_was_changed_or_is_broken_is_not_offered_and_its_reason_is_given(self):
        self.add_variant(SECOND, mark=False)
        third = self.add_variant('TOY_COUNTS_V3')
        (third / 'method.py').write_bytes((third / 'method.py').read_bytes() + b'# changed\r\n')
        fourth = self.add_variant('TOY_COUNTS_V4')
        (fourth / 'stray.py').write_bytes(b'# not declared\r\n')
        ready, not_ready = common.dev_variants(self.dev)
        self.assertEqual(list(ready), [f'{FAMILY}/{FIRST}'])
        self.assertIn('it is not marked', not_ready[f'{FAMILY}/{SECOND}'])
        self.assertIn('its marker does not match its files', not_ready[f'{FAMILY}/TOY_COUNTS_V3'])
        self.assertIn('stray.py', not_ready[f'{FAMILY}/TOY_COUNTS_V4'])


class ThePlanHasOneForm(InventedDevAndTarget):
    """The same intent always gives the same plan, so that a plan found in a barrier can be compared."""

    def test_the_order_in_which_the_parts_are_given_does_not_matter(self):
        one = common.make_plan(common.REINSTALL_INFRA, 'PROD', self.target, {'b': '2', 'a': '1'},
                               overwrite={'d': ('0', '4'), 'c': ('0', '3')}, remove={'f': '6', 'e': '5'},
                               variants=[{'family': 'E_2', 'variant': 'B', 'fingerprint': 'y', 'games': ['OZLOTTO']},
                                         {'family': 'E_2', 'variant': 'A', 'fingerprint': 'x', 'games': ['OZLOTTO']}])
        two = common.make_plan(common.REINSTALL_INFRA, 'PROD', self.target, {'a': '1', 'b': '2'},
                               overwrite={'c': ('0', '3'), 'd': ('0', '4')}, remove={'e': '5', 'f': '6'},
                               variants=[{'family': 'E_2', 'variant': 'A', 'fingerprint': 'x', 'games': ['OZLOTTO']},
                                         {'family': 'E_2', 'variant': 'B', 'fingerprint': 'y', 'games': ['OZLOTTO']}])
        self.assertEqual(one, two)
        self.assertEqual([entry['path'] for entry in one['add'] + one['overwrite'] + one['remove']], list('abcdef'))
        self.assertEqual(one['overwrite'][0], {'path': 'c', 'was': '0', 'sha256': '3'})

    def test_a_plan_keeps_no_file_content_and_nothing_of_a_variant_but_what_names_it(self):
        plan = self.creation_plan()
        self.assertEqual(plan['variants'], [{'family': FAMILY, 'variant': FIRST, 'games': list(GAMES),
                                             'fingerprint': plan['variants'][0]['fingerprint']}])
        self.assertEqual(json.loads(json.dumps(plan)), plan, 'it is plain values, so it can be written and read')

    def test_the_lines_for_the_owner_name_the_target_the_counts_the_variants_and_every_file(self):
        lines = common.plan_lines(self.creation_plan())
        self.assertEqual(lines[0], f'The plan (INIT into the QA tree at {self.target}): 8 file(s) to add, 0 to '
                                   f'overwrite, 0 to remove.')
        self.assertEqual(lines[1], f'  variant to add: {FAMILY}/{FIRST} (POWERBALL, OZLOTTO)')
        self.assertEqual(len(lines), 2 + 8)


class TheBarrier(InventedDevAndTarget):
    """Deployment design section 8: the barrier tells this install, continued, from another."""

    def other_plan(self, operation: str = common.INSTALL) -> dict:
        """A plan that is not the creation plan."""
        return common.make_plan(operation, 'QA', self.target, {'src/another.py': 'ff'})

    def test_a_tree_without_one_is_a_new_install(self):
        self.assertIsNone(common.read_barrier(self.target))
        self.assertFalse(common.check_barrier(self.target, self.creation_plan()))

    def test_the_same_plan_found_means_this_install_is_continued(self):
        plan = self.creation_plan()
        common.write_barrier(self.target, plan, 'now')
        self.assertEqual(common.read_barrier(self.target), plan)
        self.assertTrue(common.check_barrier(self.target, self.creation_plan()))

    def test_another_plan_found_is_refused_and_both_plans_are_shown(self):
        common.write_barrier(self.target, self.other_plan(), 'now')
        with self.assertRaises(common.InstallRefused) as refusal:
            common.check_barrier(self.target, self.creation_plan())
        text = str(refusal.exception)
        self.assertIn('THE UNFINISHED PLAN:\nThe plan (INSTALL into the QA tree', text)
        self.assertIn('  add: src/another.py', text)
        self.assertIn('THE PLAN NOW:\nThe plan (INIT into the QA tree', text)
        self.assertIn('Nothing was changed.', text)

    def test_dev_changed_since_the_install_began_is_another_plan(self):
        common.write_barrier(self.target, self.creation_plan(), 'now')
        self.add_variant(SECOND)
        with self.assertRaises(common.InstallRefused):
            common.check_barrier(self.target, self.creation_plan())

    def test_replace_unfinished_goes_on_only_from_one_infrastructure_reinstall_to_another(self):
        old = self.other_plan(common.REINSTALL_INFRA)
        new = common.make_plan(common.REINSTALL_INFRA, 'QA', self.target, {'src/corrected.py': 'aa'})
        common.write_barrier(self.target, old, 'now')
        with self.assertRaises(common.InstallRefused):
            common.check_barrier(self.target, new)
        self.assertTrue(common.check_barrier(self.target, new, replace_unfinished=True))
        with self.assertRaises(common.InstallRefused):
            common.check_barrier(self.target, self.other_plan(common.INSTALL), replace_unfinished=True)
        common.write_barrier(self.target, new, 'later')
        self.assertEqual(common.read_barrier(self.target), new)

    def test_the_barrier_of_an_operation_this_command_does_not_carry_out_is_refused_by_its_name(self):
        barrier = self.target / common.BARRIER_PATH
        barrier.parent.mkdir()
        barrier.write_text(json.dumps({'kind': common.BARRIER_KIND, 'started': 'now',
                                       'plan': {'operation': 'QA_SOFTWARE_REPLACEMENT'}}), encoding='ascii')
        with self.assertRaisesRegex(common.InstallRefused, "an operation named 'QA_SOFTWARE_REPLACEMENT', which "
                                                           "this command does not carry out"):
            common.check_barrier(self.target, self.creation_plan(), replace_unfinished=True)
        reinstall = common.make_plan(common.REINSTALL_INFRA, 'QA', self.target, {'src/corrected.py': 'aa'})
        with self.assertRaisesRegex(common.InstallRefused, 'QA_SOFTWARE_REPLACEMENT'):
            common.check_barrier(self.target, reinstall, replace_unfinished=True)
        barrier.unlink()
        common.write_barrier(self.target, self.other_plan(common.INSTALL), 'now')
        with self.assertRaisesRegex(common.InstallRefused, 'THE UNFINISHED PLAN:\nThe plan \\(INSTALL into'):
            common.check_barrier(self.target, reinstall, replace_unfinished=True)

    def test_a_barrier_that_cannot_be_read_is_refused_and_nothing_is_continued(self):
        barrier = self.target / common.BARRIER_PATH
        barrier.parent.mkdir()
        for content in (b'', b'{"kind": "SOMETHING_ELSE", "plan": {}}', b'{"kind": "INSTALL_IN_PROGRESS_V1"}'):
            barrier.write_bytes(content)
            with self.assertRaisesRegex(common.InstallRefused, 'cannot be read as the record of an unfinished'):
                common.check_barrier(self.target, self.creation_plan())

    def test_it_is_written_whole_in_the_standards_form_and_the_same_plan_is_not_written_again(self):
        plan = self.creation_plan()
        common.write_barrier(self.target, plan, 'the first time')
        barrier = self.target / common.BARRIER_PATH
        data = barrier.read_bytes()
        self.assertEqual(data, common.barrier_bytes(plan, 'the first time'))
        self.assertEqual(data.count(b'\n'), data.count(b'\r\n'))
        common.write_barrier(self.target, plan, 'the second time')
        self.assertEqual(barrier.read_bytes(), data)
        self.assertEqual([path.name for path in barrier.parent.iterdir()], [barrier.name], 'no temporary file left')

    def test_a_records_folder_that_is_a_link_is_refused(self):
        elsewhere = self.target.parent / 'elsewhere'
        elsewhere.mkdir()
        try:
            os.symlink(elsewhere, self.target / 'records', target_is_directory=True)
        except OSError as refusal:
            self.skipTest(f'this account may not make a link ({refusal})')
        with self.assertRaisesRegex(common.InstallRefused, 'must be an ordinary folder'):
            common.write_barrier(self.target, self.creation_plan(), 'now')
        self.assertEqual(list(elsewhere.iterdir()), [])


class AFileIsPutInPlace(InventedDevAndTarget):
    """Deployment design 4 step 4 and 5 step 7: temporary name, hash, rename; no existing file opened for writing."""

    def setUp(self):
        """One file of DEV to copy."""
        super().setUp()
        self.relative = 'src/toy_other.py'
        self.source = self.dev / self.relative
        self.digest = sha(self.source)

    def put(self, **options) -> bool:
        """Put the file in place."""
        return common.copy_into_place(self.source, self.target, self.relative, self.digest, **options)

    def test_it_arrives_with_the_plans_bytes_and_no_temporary_file_is_left(self):
        self.assertTrue(self.put())
        self.assertEqual(whole_tree(self.target), {self.relative: self.digest})

    def test_a_file_already_in_place_with_the_plans_bytes_is_passed_over_and_not_written(self):
        self.put()
        with mock.patch.object(common.os, 'replace', side_effect=AssertionError('it must not be written again')):
            self.assertFalse(self.put())

    def test_an_installed_file_with_other_bytes_is_never_changed_by_an_addition(self):
        (self.target / 'src').mkdir()
        (self.target / self.relative).write_bytes(b'# installed earlier, other bytes\r\n')
        before = whole_tree(self.target)
        with self.assertRaisesRegex(common.InstallRefused, 'already installed with different bytes'):
            self.put()
        self.assertEqual(whole_tree(self.target), before)

    def test_a_file_the_plan_overwrites_is_replaced_by_one_rename(self):
        (self.target / 'src').mkdir()
        (self.target / self.relative).write_bytes(b'# the old infrastructure file\r\n')
        self.assertTrue(self.put(replace=True))
        self.assertEqual(whole_tree(self.target), {self.relative: self.digest})

    def test_a_source_that_is_no_longer_the_plans_bytes_puts_nothing_in_place(self):
        self.source.write_bytes(b'# DEV changed after the plan was made\r\n')
        with self.assertRaisesRegex(common.InstallRefused, 'its bytes are not the bytes of the plan'):
            self.put()
        self.assertEqual(whole_tree(self.target), {})
        (self.target / 'src' / 'toy_other.py').write_bytes(b'# the old infrastructure file\r\n')
        with self.assertRaises(common.InstallRefused):
            self.put(replace=True)
        self.assertEqual((self.target / self.relative).read_bytes(), b'# the old infrastructure file\r\n')

    def test_a_temporary_file_left_by_a_copy_that_was_cut_short_does_not_stop_the_next_one(self):
        (self.target / 'src').mkdir()
        (self.target / (self.relative + common.INSTALLING_SUFFIX)).write_bytes(b'half a fi')
        self.assertTrue(self.put())
        self.assertEqual(whole_tree(self.target), {self.relative: self.digest})

    def test_a_folder_where_the_file_belongs_is_refused(self):
        (self.target / self.relative).mkdir(parents=True)
        with self.assertRaisesRegex(common.InstallRefused, 'not an ordinary file'):
            self.put()

    def test_a_link_on_the_way_is_refused_and_nothing_is_written_through_it(self):
        elsewhere = self.target.parent / 'elsewhere'
        elsewhere.mkdir()
        try:
            os.symlink(elsewhere, self.target / 'src', target_is_directory=True)
        except OSError as refusal:
            self.skipTest(f'this account may not make a link ({refusal})')
        with self.assertRaisesRegex(common.InstallRefused, 'is a link'):
            self.put()
        self.assertEqual(list(elsewhere.iterdir()), [])


class APlanIsCarriedOut(InventedDevAndTarget):
    """The files of a plan, the status files, and the same command again after a stop."""

    def test_a_creation_puts_every_planned_file_in_place_byte_for_byte_and_nothing_else(self):
        plan = self.creation_plan()
        said = []
        common.carry_out(self.dev, self.target, plan, say=said.append)
        self.assertEqual(whole_tree(self.target), {entry['path']: entry['sha256'] for entry in plan['add']})
        self.assertEqual(said, ['Files: 8 copied (each to a temporary name, hashed, renamed); 0 already in place; '
                                '0 removed.'])
        self.assertFalse((self.target / METHODS / FAMILY / FIRST / 'I_AM_INSTALLABLE.json').exists(),
                         'DEV\'s marker is never copied')

    def test_stopped_part_way_the_same_plan_carried_out_again_finishes_it(self):
        plan = self.creation_plan()
        real, calls = common.copy_into_place, []

        def stop_at_the_fourth(*arguments, **options):
            """Copy three files, then fail as a full disk would."""
            calls.append(arguments[2])
            if len(calls) == 4:
                raise OSError('an invented fault: no space left')
            return real(*arguments, **options)

        with mock.patch.object(common, 'copy_into_place', stop_at_the_fourth):
            with self.assertRaises(OSError):
                common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        self.assertEqual(len(whole_tree(self.target)), 3)
        said = []
        common.carry_out(self.dev, self.target, plan, say=said.append)
        self.assertIn('5 copied', said[0])
        self.assertIn('3 already in place', said[0])
        self.assertEqual(whole_tree(self.target), {entry['path']: entry['sha256'] for entry in plan['add']})

    def test_overwrites_are_made_and_removals_come_after_every_copy(self):
        self.installed()
        new_bytes = b'# corrected infrastructure\r\n'
        (self.dev / 'src' / 'toy_other.py').write_bytes(new_bytes)
        (self.dev / 'src' / 'toy_new.py').write_bytes(b'# a new infrastructure file\r\n')
        old = sha(self.target / 'src' / 'toy_other.py')
        doomed = sha(self.target / 'src' / 'toy_derived_code.py')
        plan = common.make_plan(common.REINSTALL_INFRA, 'QA', self.target,
                                {'src/toy_new.py': sha(self.dev / 'src' / 'toy_new.py')},
                                overwrite={'src/toy_other.py': (old, hashlib.sha256(new_bytes).hexdigest())},
                                remove={'src/toy_derived_code.py': doomed})
        order = []
        real_copy, real_unlink = common.copy_into_place, Path.unlink

        def note_copy(*arguments, **options):
            """Note each copy."""
            order.append('copy')
            return real_copy(*arguments, **options)

        def note_unlink(path, *arguments, **options):
            """Note the removal of an installed file."""
            if path.name == 'toy_derived_code.py':
                order.append('remove')
            return real_unlink(path, *arguments, **options)

        with mock.patch.object(common, 'copy_into_place', note_copy), mock.patch.object(Path, 'unlink', note_unlink):
            common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        self.assertEqual(order, ['copy', 'copy', 'remove'])
        self.assertEqual((self.target / 'src' / 'toy_other.py').read_bytes(), new_bytes)
        self.assertFalse((self.target / 'src' / 'toy_derived_code.py').exists())
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)       # again: nothing left to do

    def test_a_plan_that_adds_a_file_the_tree_holds_with_other_bytes_changes_nothing_of_it(self):
        self.installed()
        path = self.target / 'src' / 'toy_other.py'
        (self.dev / 'src' / 'toy_other.py').write_bytes(b'# changed in DEV\r\n')
        plan = common.make_plan(common.INSTALL, 'QA', self.target,
                                {'src/toy_other.py': sha(self.dev / 'src' / 'toy_other.py')})
        kept = path.read_bytes()
        with self.assertRaisesRegex(common.InstallRefused, 'already installed with different bytes'):
            common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        self.assertEqual(path.read_bytes(), kept)

    def test_a_file_to_remove_that_holds_other_bytes_than_the_plan_found_is_not_removed(self):
        self.installed()
        plan = common.make_plan(common.REINSTALL_INFRA, 'QA', self.target, {},
                                remove={'src/toy_derived_code.py': 'not what lies there'})
        with self.assertRaisesRegex(common.InstallRefused, 'Nothing was removed'):
            common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        self.assertTrue((self.target / 'src' / 'toy_derived_code.py').exists())

    def test_each_arriving_variant_gets_a_status_file_that_is_active_in_each_of_its_games(self):
        plan = self.creation_plan()
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        self.assertEqual(common.create_status_files(self.target, plan), 1)
        path = self.target / METHODS / FAMILY / FIRST / 'VARIANT_STATUS.ini'
        statuses = status_file.read_status(path, GAMES)
        self.assertEqual(statuses, {game: status_file.GameStatus() for game in GAMES},
                         'active in each game: nothing withdrawn, no eligibility draw set')
        data = path.read_bytes()
        self.assertEqual(common.create_status_files(self.target, plan), 0, 'continued: it is read and left')
        self.assertEqual(path.read_bytes(), data)

    def test_a_status_file_found_there_that_fails_its_own_check_stops_the_install(self):
        plan = self.creation_plan()
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        (self.target / METHODS / FAMILY / FIRST / 'VARIANT_STATUS.ini').write_bytes(b'not a status file\r\n')
        with self.assertRaisesRegex(common.InstallRefused, 'fails its own check'):
            common.create_status_files(self.target, plan)


class TheTreesSoftwareAgainstThePlan(InventedDevAndTarget):
    """Deployment design 3.3 items 2 and 3, 4 step 7, 5 step 8: the whole tree's software against the plan."""

    def carried_out(self) -> tuple:
        """The creation plan carried out, not yet finished; return (the plan, the list expected)."""
        plan = self.creation_plan()
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        common.create_status_files(self.target, plan)
        return plan, common.expected_list(None, plan)

    def test_a_tree_just_created_is_exactly_what_its_plan_says(self):
        _, expected = self.carried_out()
        self.assertEqual(common.software_differences(self.target, expected), [])
        self.assertEqual(installed_files.software_now(self.target), expected)

    def test_a_changed_a_missing_an_added_and_a_half_copied_file_are_each_found(self):
        _, expected = self.carried_out()
        path = self.target / 'src' / 'toy_other.py'
        kept = path.read_bytes()
        for change, words in ((lambda: path.write_bytes(kept + b'#\r\n'), 'its bytes are not the bytes'),
                              (path.unlink, 'is missing'),
                              (lambda: (self.target / 'src' / 'extra.py').write_bytes(b'#\r\n'), 'is not on the list'),
                              (lambda: (self.target / 'src' / 'toy_x.py.installing').write_bytes(b'#'),
                               'is not on the list')):
            change()
            found = common.software_differences(self.target, expected)
            self.assertEqual(len(found), 1, found)
            self.assertIn(words, found[0])
            path.write_bytes(kept)
            for extra in ('extra.py', 'toy_x.py.installing'):
                (self.target / 'src' / extra).unlink(missing_ok=True)
        self.assertEqual(common.software_differences(self.target, expected), [])

    def test_an_install_into_an_existing_tree_expects_the_old_list_and_the_plan_together(self):
        self.installed()
        before = installed_files.read_list(self.target)
        self.add_variant(SECOND)
        ready, _ = common.dev_variants(self.dev)
        entry = ready[f'{FAMILY}/{SECOND}']
        held = {item['path'] for item in before['files']}
        plan = common.make_plan(common.INSTALL, 'QA', self.target,
                                {path: digest for path, digest in entry['files'].items() if path not in held},
                                variants=[entry])
        self.assertEqual([item['path'] for item in plan['add']], [f'{METHODS}/{FAMILY}/{SECOND}/VARIANT.json',
                                                                  f'{METHODS}/{FAMILY}/{SECOND}/method.py'])
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        common.create_status_files(self.target, plan)
        expected = common.expected_list(before, plan)
        self.assertEqual([item['variant'] for item in expected['variants']], [FIRST, SECOND])
        self.assertEqual(len(expected['files']), len(before['files']) + 2)
        self.assertEqual(common.software_differences(self.target, expected), [])
        self.assertNotEqual(common.software_differences(self.target, before), [], 'the old list no longer fits')

    def test_overwrites_and_removals_are_in_what_is_expected(self):
        _, before = self.installed()
        plan = common.make_plan(common.REINSTALL_INFRA, 'QA', self.target, {'src/toy_new.py': 'aa'},
                                overwrite={'src/toy_other.py': ('00', 'bb')}, remove={'src/toy_derived_code.py': '00'})
        expected = {item['path']: item['sha256'] for item in common.expected_list(before, plan)['files']}
        self.assertEqual((expected['src/toy_new.py'], expected['src/toy_other.py']), ('aa', 'bb'))
        self.assertNotIn('src/toy_derived_code.py', expected)

    def test_a_variant_whose_fingerprint_in_the_tree_is_not_the_plans_is_found(self):
        plan, expected = self.carried_out()
        expected['variants'][0]['fingerprint'] = 'not the fingerprint of what was copied'
        found = common.software_differences(self.target, expected)
        self.assertEqual(len(found), 1)
        self.assertIn('the tree\'s own reading of its variants is not the plan\'s', found[0])

    def test_every_status_file_must_be_there_and_pass_its_own_check(self):
        self.carried_out()
        self.assertEqual(common.status_file_faults(self.target), [])
        path = self.target / METHODS / FAMILY / FIRST / 'VARIANT_STATUS.ini'
        kept = path.read_bytes()
        path.write_bytes(kept.replace(b'ACTIVE', b'ACTIVF', 1))
        self.assertEqual(len(common.status_file_faults(self.target)), 1)
        path.unlink()
        (fault,) = common.status_file_faults(self.target)
        self.assertIn(f'{FAMILY}/{FIRST}', fault)


class TheEnding(InventedDevAndTarget):
    """Deployment design 5 step 10: the list, the log line, the barrier removed, last."""

    def test_the_list_is_written_the_log_gains_one_line_and_the_barrier_goes_last(self):
        plan = self.creation_plan()
        common.write_barrier(self.target, plan, 'now')
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        common.create_status_files(self.target, plan)
        expected = common.expected_list(None, plan)
        seen = {}
        real = common.remove_barrier

        def look_then_remove(tree_root):
            """Note what exists at the moment the barrier is removed."""
            seen['list'] = (self.target / installed_files.LIST_PATH).is_file()
            seen['log'] = (self.target / common.TREE_LOG_PATH).is_file()
            real(tree_root)

        with mock.patch.object(common, 'remove_barrier', look_then_remove):
            fingerprint = common.finish(self.target, plan, expected, self.clock, extra={'suite': 'PASSED'})
        self.assertEqual(seen, {'list': True, 'log': True})
        self.assertFalse((self.target / common.BARRIER_PATH).exists())
        self.assertEqual((self.target / installed_files.LIST_PATH).read_bytes(), installed_files.list_bytes(expected))
        self.assertEqual(fingerprint, snapshot.software_fingerprint(self.target))
        (line,) = (self.target / common.TREE_LOG_PATH).read_text(encoding='ascii').splitlines()
        record = json.loads(line)
        self.assertEqual((record['operation'], record['role'], record['added'], record['variants'], record['suite']),
                         ('INIT', 'QA', 8, [f'{FAMILY}/{FIRST}'], 'PASSED'))
        self.assertEqual((record['time'], record['software_fingerprint'], record['infrastructure_fingerprint']),
                         ('2026-12-01T09:40:12Z', fingerprint, plan['infrastructure_fingerprint']))

    def test_a_fault_before_the_end_leaves_the_barrier_in_place(self):
        plan = self.creation_plan()
        common.write_barrier(self.target, plan, 'now')
        common.carry_out(self.dev, self.target, plan, say=lambda line: None)
        with mock.patch.object(common, 'log_line', side_effect=OSError('an invented fault')):
            with self.assertRaises(OSError):
                common.finish(self.target, plan, common.expected_list(None, plan), self.clock)
        self.assertEqual(common.read_barrier(self.target), plan)

    def test_after_the_ending_the_tree_matches_its_own_list(self):
        _, expected = self.installed()
        content = installed_files.read_list(self.target)
        self.assertEqual(content, expected)
        self.assertEqual(installed_files.differences(self.target, content), [])


class InventedDevAndQa(InventedDevAndTarget):
    """The invented DEV, and a QA tree that the fixtures leave as installed, with a backup root of its own."""

    def setUp(self):
        """Make the QA tree."""
        super().setUp()
        self.qa = fixtures.make_tree(self.target.parent / 'qa', role='QA')
        fixtures.as_installed(self.qa)
        self.settings = read_settings(self.qa)
        self.records = self.qa / 'records'

    def plan(self) -> dict:
        """A small plan for the QA tree."""
        return common.make_plan(common.INSTALL, 'QA', self.qa, {'src/toy_added.py': 'aa'})


class TheTargetIsReserved(InventedDevAndQa):
    """Deployment design 5 step 6 (EX_269 R7-F04): the job lock by an exclusive create, then the process check."""

    def refused(self, error, pattern: str) -> None:
        """Expect the reservation to refuse, the block not to run, and no lock file to be left."""
        ran = []
        with self.assertRaisesRegex(error, pattern):
            with common.reserved(self.settings, 'an install', 'now', say=lambda line: None):
                ran.append(True)
        self.assertEqual(ran, [])
        self.assertFalse((self.records / job_lock.JOB_LOCK_NAME).exists(), 'its own lock is not left behind')

    def test_the_job_lock_is_held_inside_the_block_and_released_after_it(self):
        said = []
        with common.reserved(self.settings, 'an install', 'now', say=said.append):
            self.assertIn(b'an install; started now', (self.records / job_lock.JOB_LOCK_NAME).read_bytes())
            with self.assertRaises(job_lock.LaunchRefused):
                job_lock.job_lock(self.qa, 'a job', 'now').__enter__()
        self.assertFalse((self.records / job_lock.JOB_LOCK_NAME).exists())
        self.assertIn('The target is reserved: its job lock is held, and no other Python process', said[0])

    def test_a_job_that_holds_the_lock_refuses_the_install_and_its_lock_is_left_alone(self):
        with job_lock.job_lock(self.qa, 'a research job', 'now'):
            with self.assertRaisesRegex(job_lock.LaunchRefused, 'a process of this tree is running'):
                with common.reserved(self.settings, 'an install', 'now', say=lambda line: None):
                    self.fail('the block must not run')
            self.assertIn(b'a research job', (self.records / job_lock.JOB_LOCK_NAME).read_bytes())

    def test_the_process_check_is_made_while_the_lock_is_held(self):
        seen = []

        def rule(tree_root):
            """Note whether the lock is held when the rule is asked."""
            seen.append((tree_root, (self.records / job_lock.JOB_LOCK_NAME).exists()))
            return 7

        with mock.patch.object(process_rule, 'check_no_other_process_of_tree', rule):
            with common.reserved(self.settings, 'an install', 'now', say=lambda line: None):
                pass
        self.assertEqual(seen, [(self.qa, True)])

    def test_another_python_process_of_the_tree_refuses(self):
        error = process_rule.ProcessRuleRefused('1 other Python process(es) of the tree are running')
        with mock.patch.object(process_rule, 'check_no_other_process_of_tree', side_effect=error):
            self.refused(process_rule.ProcessRuleRefused, '1 other Python process')

    def test_the_orphan_marker_refuses(self):
        orphan = self.qa / job_lock.ORPHAN_MARKER
        orphan.parent.mkdir(parents=True)
        orphan.write_text('[{"run": "invented"}]', encoding='ascii')
        self.refused(job_lock.LaunchRefused, 'UNRESOLVED_ORPHAN.json')

    def test_a_results_update_that_holds_its_lock_refuses(self):
        (self.qa / job_lock.UPDATER_LOCK).parent.mkdir(exist_ok=True)
        (self.qa / job_lock.UPDATER_LOCK).write_bytes(b'an update\r\n')
        self.refused(job_lock.LaunchRefused, 'a results update holds its lock')

    def test_another_unfinished_operation_refuses_and_an_unfinished_install_is_left_to_the_barriers_check(self):
        self.records.mkdir(exist_ok=True)
        (self.records / 'RERUN_IN_PROGRESS.json').write_text('{}', encoding='ascii')
        self.refused(job_lock.LaunchRefused, 'RERUN_IN_PROGRESS.json exists')
        (self.records / 'RERUN_IN_PROGRESS.json').unlink()
        common.write_barrier(self.qa, self.plan(), 'earlier')
        with common.reserved(self.settings, 'an install', 'now', say=lambda line: None):
            self.assertTrue(common.check_barrier(self.qa, self.plan()))


class TheBarrierTheUpdatersLockAndTheNote(InventedDevAndQa):
    """Deployment design 5 steps 6 and 10: the barrier, the updater's lock, SNAPSHOT_DUE; and their release."""

    def test_inside_the_block_all_three_are_in_place(self):
        with common.changing(self.settings, self.plan(), 'now'):
            self.assertEqual(common.read_barrier(self.qa), self.plan())
            self.assertIn(b'INSTALL of software; started now', (self.qa / job_lock.UPDATER_LOCK).read_bytes())
            self.assertTrue(snapshot.is_due(self.qa))

    def test_a_block_that_ends_by_a_fault_leaves_the_barrier_and_lets_the_updaters_lock_go(self):
        with self.assertRaises(RuntimeError):
            with common.changing(self.settings, self.plan(), 'now'):
                raise RuntimeError('an invented failed check')
        self.assertEqual(common.read_barrier(self.qa), self.plan(), 'no launcher works until the install is finished')
        self.assertFalse((self.qa / job_lock.UPDATER_LOCK).exists())
        self.assertTrue(snapshot.is_due(self.qa))

    def test_a_held_updaters_lock_refuses_after_the_barrier_is_written_and_is_left_alone(self):
        (self.qa / job_lock.UPDATER_LOCK).parent.mkdir(exist_ok=True)
        (self.qa / job_lock.UPDATER_LOCK).write_bytes(b'an update\r\n')
        with self.assertRaises(job_lock.LaunchRefused):
            with common.changing(self.settings, self.plan(), 'now'):
                self.fail('the block must not run')
        self.assertEqual((self.qa / job_lock.UPDATER_LOCK).read_bytes(), b'an update\r\n')

    def test_the_ending_releases_the_updaters_lock_before_it_removes_the_barrier_and_the_barrier_goes_last(self):
        plan = self.plan()
        expected = installed_files.read_list(self.qa)
        seen = {}
        real = common.remove_barrier

        def look_then_remove(tree_root):
            """Note what is still held at the moment the barrier is removed."""
            seen['updater lock'] = (self.qa / job_lock.UPDATER_LOCK).exists()
            seen['job lock'] = (self.records / job_lock.JOB_LOCK_NAME).exists()
            real(tree_root)

        with mock.patch.object(common, 'remove_barrier', look_then_remove):
            with common.reserved(self.settings, 'an install', 'now', say=lambda line: None):
                with common.changing(self.settings, plan, 'now') as release:
                    common.finish(self.qa, plan, expected, self.clock, release=release)
        self.assertEqual(seen, {'updater lock': False, 'job lock': True})
        left = sorted(path.name for path in self.records.iterdir())
        self.assertEqual(left, ['INSTALLED_FILES.json', 'INSTALL_LOG.jsonl', 'SNAPSHOT_DUE'],
                         'no barrier and no lock; a backup is owed')


class TheRollbackPointAndTheOneQuestion(InventedDevAndQa):
    """Deployment design 5 steps 3 to 5 and specification 12.3: each result told exactly; Enter is NO."""

    KIT = recovery_kit.KitResult(True, path=Path('T:/backups/KIT_20261201_201000_5d0c9a1e77aa.zip'))
    NO_KIT = recovery_kit.KitResult(False, reason='the backup root cannot be written.')
    BACKUP = snapshot.SnapshotResult(True, path=Path('T:/backups/QA_20261201_201000_PRE_INSTALL.zip'), files=10,
                                     size=2_000_000, seconds=3)
    NO_BACKUP = snapshot.SnapshotResult(False, reason='another Python process of the tree is running.')

    def test_both_made_the_question_names_both_and_warns_of_nothing(self):
        lines = common.question_lines(self.KIT, self.BACKUP)
        self.assertEqual(lines, [f'The backup taken just now: {self.BACKUP.line()}',
                                 f'The recovery kit: {self.KIT.line()}',
                                 'Type YES to proceed. Anything else, Enter included, is NO.'])
        self.assertIn('QA_20261201_201000_PRE_INSTALL.zip', lines[0])

    def test_no_backup_is_said_in_capitals_and_no_backup_is_named(self):
        lines = common.question_lines(self.KIT, self.NO_BACKUP)
        self.assertEqual(lines[0], 'The backup taken just now: BACKUP NOT MADE: another Python process of the tree '
                                   'is running.')
        self.assertEqual(lines[2], 'NO ROLLBACK POINT WAS CREATED BY THIS INSTALL.')
        self.assertNotIn('.zip', lines[0] + lines[2])
        self.assertEqual(len(lines), 4)

    def test_no_kit_is_said_in_capitals_with_what_still_works(self):
        lines = common.question_lines(self.NO_KIT, self.BACKUP)
        self.assertEqual(lines[2], 'THE RESTORE TOOL COULD NOT BE WRITTEN: an existing kit in your backup folder '
                                   'still works for older backups.')
        self.assertEqual(len(lines), 4)

    def test_both_failing_gives_both_warnings(self):
        lines = common.question_lines(self.NO_KIT, self.NO_BACKUP)
        self.assertEqual([line.split(':')[0] for line in lines[2:4]],
                         ['NO ROLLBACK POINT WAS CREATED BY THIS INSTALL.', 'THE RESTORE TOOL COULD NOT BE WRITTEN'])

    def test_only_yes_in_capitals_is_yes(self):
        for answer, wanted in (('YES', True), (' YES \n', True), ('', False), ('yes', False), ('Y', False),
                               ('YES please', False), ('NO', False)):
            said = []
            self.assertEqual(common.owner_says_yes(['the question'], ask=lambda prompt: answer, say=said.append),
                             wanted, repr(answer))
            self.assertEqual(said, ['the question'])

    def test_an_input_that_has_ended_is_no(self):
        def ended(prompt):
            """No one is there to answer."""
            raise EOFError

        self.assertFalse(common.owner_says_yes([], ask=ended, say=lambda line: None))

    def test_the_kit_is_asked_for_the_software_state_to_come_and_the_backup_by_its_name(self):
        expected = installed_files.read_list(self.qa)
        with mock.patch.object(recovery_kit, 'build_kit', return_value=self.KIT) as kit, \
                mock.patch.object(snapshot, 'attempt_snapshot', return_value=self.NO_BACKUP) as backup:
            said = []
            found = common.attempt_rollback_point(self.dev, self.settings, 'PRE_INSTALL', expected, self.clock,
                                                  say=said.append)
        self.assertEqual(found, (self.KIT, self.NO_BACKUP))
        kit.assert_called_once_with(self.dev, self.settings.backup_root,
                                    hashlib.sha256(installed_files.list_bytes(expected)).hexdigest(), self.clock)
        backup.assert_called_once_with(self.settings, 'PRE_INSTALL', self.clock)
        self.assertEqual((said[0], said[-1]), (self.KIT.line(), self.NO_BACKUP.line()))

    def test_a_real_attempt_on_an_invented_tree_makes_the_backup_and_says_why_there_is_no_kit(self):
        expected = installed_files.read_list(self.qa)
        kit, backup = common.attempt_rollback_point(self.dev, self.settings, 'PRE_INSTALL', expected, self.clock,
                                                    say=lambda line: None)
        self.assertTrue(backup.made, backup.reason)
        self.assertTrue(backup.path.name.endswith('_PRE_INSTALL.zip'))
        self.assertFalse(kit.made, 'the invented DEV holds no restore tool')
        self.assertIn('RECOVERY KIT NOT WRITTEN: ', kit.line())


class TheChecksWithTheTargetsOwnPython(InventedDevAndQa):
    """Deployment design 3.3 items 4 to 7: with the target's Python."""

    def test_the_targets_python_is_its_environments_own_and_a_tree_without_one_is_refused(self):
        self.assertEqual(common.target_python(self.settings), self.qa / '.venv' / 'Scripts' / 'python.exe')
        (self.qa / '.venv' / 'Scripts' / 'python.exe').unlink()
        with self.assertRaisesRegex(common.InstallRefused, 'create_venv.bat, then install_upgrade_dependencies'):
            common.target_python(self.settings)

    def test_a_tree_is_file_for_file_devs_only_if_every_infrastructure_file_and_the_manifest_agree(self):
        dev_files = common.dev_infrastructure(self.dev)['files']
        same = {'files': [{'path': path, 'sha256': digest} for path, digest in dev_files.items()]
                + [{'path': 'src/methods/E_901/X_V1/method.py', 'sha256': 'a variant is not infrastructure'}]}
        self.assertEqual(common.infrastructure_differences(dev_files, same), [])
        for changed in ('src/toy_other.py', 'deploy/INFRA_MANIFEST.ini'):
            other = {'files': [dict(entry, sha256='other bytes') if entry['path'] == changed else entry
                               for entry in same['files']]}
            self.assertEqual(common.infrastructure_differences(dev_files, other), [changed])
        lacking = {'files': [entry for entry in same['files'] if entry['path'] != 'src/toy_other.py']}
        self.assertEqual(common.infrastructure_differences(dev_files, lacking), ['src/toy_other.py'])

    def test_the_suite_is_not_run_for_a_tree_whose_infrastructure_is_not_devs_and_the_line_says_so(self):
        dev_files = common.dev_infrastructure(self.dev)['files']
        with mock.patch.object(suite_on_copy, 'run_suite', side_effect=AssertionError('it must not be run')):
            verdict, line = common.suite_if_it_is_the_trees(self.dev, dev_files, {'files': []}, Path('python.exe'))
        self.assertIsNone(verdict)
        self.assertTrue(line.startswith('The test suite: the tests in DEV are for newer code than this tree holds; '
                                        'not run (the tree differs from DEV in: deploy/INFRA_MANIFEST.ini, '))

    def test_the_suite_is_run_with_the_targets_python_when_the_infrastructure_is_devs(self):
        dev_files = common.dev_infrastructure(self.dev)['files']
        installed = {'files': [{'path': path, 'sha256': digest} for path, digest in dev_files.items()]}
        for passed in (True, False):
            result = suite_on_copy.SuiteResult(passed=passed, modules=[('test_x', 0 if passed else 1, 3)],
                                               folder=None if passed else Path('C:/Temp/copy'))
            with mock.patch.object(suite_on_copy, 'run_suite', return_value=result) as run:
                verdict, line = common.suite_if_it_is_the_trees(self.dev, dev_files, installed, Path('python.exe'),
                                                                say=print)
            run.assert_called_once_with(self.dev, Path('python.exe'), print)
            self.assertEqual((verdict, line), (passed, result.line()))
        with mock.patch.object(suite_on_copy, 'run_suite', side_effect=suite_on_copy.SuiteRefused('no list')):
            with self.assertRaisesRegex(common.InstallRefused, 'no list'):
                common.suite_if_it_is_the_trees(self.dev, dev_files, installed, Path('python.exe'))

    def checks(self, run, **options) -> dict:
        """Ask for the checks through a stand-in for the program's start."""
        return common.checks_with_target_python(Path('the/python.exe'), Path('the/software'), self.qa,
                                                options.get('smoke', common.ALL_VARIANTS),
                                                options.get('sample', True), options.get('derived', True),
                                                say=lambda line: None, run=run)

    def test_the_program_is_started_isolated_with_no_cache_and_its_result_is_read_and_its_folder_removed(self):
        started = {}

        def run(words, **options):
            """Do what the program does: write what it found to the file it was told."""
            started['words'], started['options'] = words, options
            result = Path(words[words.index('--result') + 1])
            started['folder'] = result.parent
            result.write_text(json.dumps({'kind': 'TREE_CHECKS_V1', 'smoke': {'asked': 'ALL', 'failures': []},
                                          'unreadable': {}, 'sample': None, 'derived': None}), encoding='ascii')
            return mock.Mock(returncode=0)

        found = self.checks(run)
        self.assertEqual(found['smoke'], {'asked': 'ALL', 'failures': []})
        words = started['words']
        self.assertEqual(words[:6], [str(Path('the/python.exe')), '-I', '-B', '-u',
                                     str(Path('the/software') / 'src' / 'tree_checks_command.py'), 'checks'])
        self.assertEqual(words[6:8], ['--data', str(self.qa)])
        self.assertEqual(words[10:], ['--smoke', 'ALL', '--sample', '--derived'])
        self.assertNotIn('timeout', started['options'], 'no time limit: a limit would end the process')
        self.assertFalse(started['folder'].exists(), 'the temporary folder is removed')
        self.assertNotIn(self.qa, started['folder'].parents, 'and it never lay in the tree')

    def test_named_variants_and_unasked_checks_are_passed_on_as_they_are(self):
        seen = []

        def run(words, **options):
            """Note the words and answer as the program would."""
            seen.append(words[10:])
            Path(words[words.index('--result') + 1]).write_text('{"kind": "TREE_CHECKS_V1"}', encoding='ascii')
            return mock.Mock(returncode=0)

        self.checks(run, smoke=['E_901/A_V1', 'E_901/B_V1'], sample=False, derived=False)
        self.checks(run, smoke=common.NO_VARIANT, sample=False, derived=True)
        self.assertEqual(seen, [['--smoke', 'E_901/A_V1,E_901/B_V1'], ['--smoke', 'NONE', '--derived']])

    def test_any_ending_but_zero_with_a_result_of_the_right_kind_is_refused_and_nothing_passes(self):
        def ending(code: int, text: str | None):
            """A stand-in that ends with `code` and leaves `text` as its result, or none."""
            def run(words, **options):
                """End as told."""
                if text is not None:
                    Path(words[words.index('--result') + 1]).write_text(text, encoding='ascii')
                return mock.Mock(returncode=code)
            return run

        good = '{"kind": "TREE_CHECKS_V1"}'
        for code, text in ((2, None), (2, good), (1, good), (0, None), (0, 'not json'), (0, '{"kind": "OTHER"}'),
                           (0, '[]')):
            with self.assertRaisesRegex(common.InstallRefused, 'the checks could not be made with the target'):
                self.checks(ending(code, text))
        self.assertEqual(self.checks(ending(0, good)), {'kind': 'TREE_CHECKS_V1'})

    def test_the_words_the_install_tool_uses_are_the_commands_own(self):
        self.assertEqual((common.ALL_VARIANTS, common.NO_VARIANT, common.CHECKS_RESULT_KIND),
                         (tree_checks.ALL_VARIANTS, tree_checks.NO_VARIANT, tree_checks.RESULT_KIND))
        self.assertTrue((REPOSITORY_ROOT / common.CHECKS_PROGRAM).is_file())

    def test_what_stops_an_install_and_what_does_not(self):
        nothing = {'smoke': {'asked': 'ALL', 'failures': []}, 'unreadable': {}, 'sample': {'compared': 6,
                   'differences': []}, 'derived': {'POWERBALL': None, 'OZLOTTO': None}}
        self.assertEqual(common.faults_that_stop(nothing), [])
        self.assertEqual(common.faults_that_stop({'smoke': None, 'unreadable': None, 'sample': None,
                                                  'derived': None}), [], 'what was not asked stops nothing')
        known = dict(nothing, derived={'POWERBALL': {'from_draw': 1600, 'detail': 'd', 'known': True}})
        self.assertEqual(common.faults_that_stop(known), [], 'a difference the tree already marks is expected')
        found = dict(nothing, smoke={'asked': 'ALL', 'failures': ['E_901/X_V1 for POWERBALL: the smoke case failed']},
                     unreadable={'OZLOTTO': 'a list breaks its rule'},
                     sample={'compared': 6, 'differences': ['E_901/A_V1 for POWERBALL, draw 1200: not the same']},
                     derived={'POWERBALL': {'from_draw': 1600, 'detail': 'the score differs', 'known': False}})
        faults = common.faults_that_stop(found)
        self.assertEqual(len(faults), 4)
        self.assertIn('the smoke case failed', faults[0])
        self.assertIn('OZLOTTO: its stored records could not be read: a list breaks its rule', faults[1])
        self.assertIn('draw 1200', faults[2])
        self.assertIn('POWERBALL: stored scores or OV-1 lines are not what the installed software computes, from '
                      'draw 1600: the score differs', faults[3])


if __name__ == '__main__':
    unittest.main()
