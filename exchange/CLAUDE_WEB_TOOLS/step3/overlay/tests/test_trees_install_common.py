"""Tests of deploy/install_common.py: what every install shares (build step 3, slice C, part C2).

What this file is for
    It shows, on invented trees in temporary folders, that what DEV offers is exactly what its markers cover; that
    a plan has one form; that the barrier tells this install from another (deployment design section 8); that a
    file is put in place only with the plan's bytes and that no installed file is changed unless the plan
    overwrites it; that a plan stopped part-way is finished by carrying it out again; that the tree's software
    is checked whole against the plan; and that the ending writes the list, the log line and removes the barrier
    last.

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
import research_fixtures as fixtures                        # noqa: E402
from research import installed_files, snapshot, status_file    # noqa: E402
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


if __name__ == '__main__':
    unittest.main()
