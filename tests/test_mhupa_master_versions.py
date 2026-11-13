"""MHUP-A slice 1: the version-2 master rules (design v0.1r5 section 3.2; Appendix L: oracles, L-U5). OFFLINE.

Every master is invented in a temporary folder (tests/mhupa_fixtures.grow_master); no real draw is read. The prefix
oracle (independent_prefix_sha) finds line endings by a byte scan, not by the module's splitlines, and T-05 is rerun
on a version-3 synthetic master: every development target's view bytes and digest equal version 1's.
"""
from __future__ import annotations

import ast
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import e2r_fixtures as F
import mhupa_fixtures as X
from _common import master_versions as MV
from _common.game_draws_reader import load_pinned_draw_view
from _common.game_profiles import OZLOTTO, POWERBALL, get_profile
from evaluation import outcome_reader as OREAD

ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> bytes:
    return path.read_bytes()


class LedgerColumns(unittest.TestCase):
    """The module's own copy of the updater's LEDGER_COLUMNS equals the owner's tool's, read with ast (never imported)."""

    def test_equal_to_the_updater(self):
        src = (ROOT / 'src' / 'results_master_v0_2.py').read_text(encoding='utf-8')     # MHUP-A slice 2: v0.2 (design 7)
        found = None
        for n in ast.parse(src).body:
            if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'LEDGER_COLUMNS':
                found = ast.literal_eval(n.value)
        self.assertEqual(found, MV.LEDGER_COLUMNS)
        self.assertEqual(X.LEDGER_COLUMNS, MV.LEDGER_COLUMNS)


class Grammar(unittest.TestCase):
    """Design 3.2 rule 1: one INIT, two UPDATE and one NO_CHANGE rows pass; each rule broken once refuses."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name)
        self.p = POWERBALL
        self.rows = X.grow_master(self.root, self.p, [[1577, 1578, 1579], [1580], None])
        self.master, self.ledger, self.evidence = X.master_paths(self.root, 'POWERBALL')

    def tearDown(self):
        self._td.cleanup()

    def parse(self):
        return MV.parse_ledger(read(self.ledger), 'POWERBALL')

    def test_a_good_chain_parses_and_binds_the_master(self):
        rows = self.parse()
        self.assertEqual([(r.version, r.action, r.last_draw, r.draw_count) for r in rows],
                         [(1, 'INIT', 1576, 433), (2, 'UPDATE', 1579, 436), (3, 'UPDATE', 1580, 437), (4, 'NO_CHANGE', 1580, 437)])
        MV.verify_master_against_ledger(read(self.master), rows, 'POWERBALL')
        raw, rows2, ev = MV.load_verified_source(self.root, 'POWERBALL')
        self.assertEqual(rows2, rows)
        self.assertEqual(MV.current_pin(self.root, 'POWERBALL'), (4, rows[-1].master_sha256))

    def broken(self, mutate, msg):
        rows = [dict(r) for r in self.rows]
        mutate(rows)
        X.write_ledger(self.ledger, rows)
        with self.assertRaises(MV.LedgerRefused, msg=msg):
            MV.parse_ledger(read(self.ledger), 'POWERBALL')

    def test_each_grammar_rule_broken_once_refuses(self):
        self.broken(lambda r: r.__setitem__(1, dict(r[1], version=3)), 'version gap')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], version=1)), 'duplicate version')
        self.broken(lambda r: r.__setitem__(2, dict(r[2], utc=X.utc_at(1))), 'utc decreases')
        self.broken(lambda r: r.__setitem__(2, dict(r[2], utc='yesterday')), 'utc not an instant')
        self.broken(lambda r: r.__setitem__(2, dict(r[2], first_draw=1145)), 'first_draw changed')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], master_sha256='zz' * 32)), 'bad hex')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], added_first=1580)), 'UPDATE added_first not previous last + 1')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], added_last=1578)), 'UPDATE added_last not last_draw')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], draw_count=435)), 'UPDATE draw_count wrong')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], backup_sha256='0' * 64)), 'backup not the previous master')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], backup_file='')), 'UPDATE without backup_file')
        self.broken(lambda r: r.__setitem__(3, dict(r[3], added_count=1)), 'NO_CHANGE added_count')
        self.broken(lambda r: r.__setitem__(3, dict(r[3], master_sha256=r[1]['master_sha256'])), 'NO_CHANGE sha differs from previous')
        self.broken(lambda r: r.__setitem__(3, dict(r[3], backup_sha256=r[2]['master_sha256'])), 'NO_CHANGE with backup')
        self.broken(lambda r: r.__setitem__(3, dict(r[3], action='CORRECTION')), 'unknown action')
        self.broken(lambda r: r.__setitem__(3, dict(r[3], grab_file='')), 'missing grab_file')
        self.broken(lambda r: r.__setitem__(3, dict(r[3], tool_version='')), 'empty tool_version')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], action='UPDATE')), 'first row not INIT')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], last_draw=1575, draw_count=432, added_count=432, added_last=1575)),
                    'INIT not the development prefix')
        # each of these breaks ONE rule only (every other cross-row rule still holds), so a redundant check cannot
        # mask the rule under test (the slice's mutation checks plant exactly these defects)
        self.broken(lambda r: r.__delitem__(slice(1, None)) or r.__setitem__(0, dict(r[0], last_draw=1575, draw_count=432,
                                                                                      added_count=432, added_last=1575)),
                    'a one-row ledger whose INIT stops short of the development prefix (its own fields consistent)')
        self.broken(lambda r: r.__setitem__(1, dict(r[1], added_first=1578, added_count=2)),
                    'UPDATE added range starts after the previous last draw (own range and counts consistent)')
        self.broken(lambda r: (r.__setitem__(1, dict(r[1], master_sha256=r[0]['master_sha256'])),
                               r.__setitem__(2, dict(r[2], backup_sha256=r[0]['master_sha256']))),
                    'UPDATE repeats the previous master_sha256 (the next backup agrees)')
        # EX_142 B03: the universally required fields are required of the INIT row too
        self.broken(lambda r: r.__setitem__(0, dict(r[0], utc='fixture')), 'INIT utc not an instant')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], utc='')), 'INIT utc missing')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], tool_version='')), 'INIT tool_version empty')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], tool_sha256='')), 'INIT tool_sha256 missing')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], added_count=432)), 'INIT added_count disagrees')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], grab_file='grab_1.csv')), 'INIT with a grab file')
        self.broken(lambda r: r.__setitem__(0, dict(r[0], backup_sha256='0' * 64)), 'INIT with a backup')
        # the physical shape: a wrong header, a renamed column, a truncated last line, an extra field, a blank line, a
        # record spanning two physical lines, a non-ASCII byte (B03)
        X.write_ledger(self.ledger, [dict(r) for r in self.rows])
        raw = read(self.ledger)
        with self.assertRaises(MV.LedgerRefused):
            MV.parse_ledger(raw.replace(b'version,utc,action', b'version,utc,act'), 'POWERBALL')
        with self.assertRaises(MV.LedgerRefused):                      # every column name present but one renamed
            MV.parse_ledger(raw.replace(b',note\r\n', b',notes\r\n', 1), 'POWERBALL')
        with self.assertRaises(MV.LedgerRefused):
            MV.parse_ledger(raw[:-3], 'POWERBALL')
        with self.assertRaises(MV.LedgerRefused):
            MV.parse_ledger(raw[:-2] + b',extra\r\n', 'POWERBALL')
        with self.assertRaises(MV.LedgerRefused):                      # a blank physical line between rows
            MV.parse_ledger(raw.replace(b'fixture INIT\r\n', b'fixture INIT\r\n\r\n', 1), 'POWERBALL')
        with self.assertRaises(MV.LedgerRefused):                      # a blank line at the end
            MV.parse_ledger(raw + b'\r\n', 'POWERBALL')
        with self.assertRaises(MV.LedgerRefused):                      # a quoted field spanning two lines
            MV.parse_ledger(raw.replace(b'fixture INIT\r\n', b'"fixture\r\nINIT"\r\n', 1), 'POWERBALL')
        with self.assertRaises(MV.LedgerRefused):                      # not ASCII
            MV.parse_ledger(raw.replace(b'fixture INIT', b'fixture \xe9', 1), 'POWERBALL')
        MV.parse_ledger(raw, 'POWERBALL')                    # and the unbroken ledger still parses
        MV.parse_ledger(raw.replace(b'\r\n', b'\n'), 'POWERBALL')   # LF line endings are accepted too
        # EX_144 B03r1: the CSV lexical boundary. A note the updater's writer would quote (a comma) is accepted when
        # quoted as the writer quotes it; an unclosed quote, a stray quote after a quoted field, a quote inside an
        # unquoted field and unnecessary quoting are each refused, on the INIT row and on a later row.
        MV.parse_ledger(raw.replace(b'fixture INIT', b'"from grab, verified"', 1), 'POWERBALL')
        MV.parse_ledger(raw.replace(b'fixture UPDATE', b'"he said ""x"", then"', 1), 'POWERBALL')
        for row_note in (b'fixture INIT', b'fixture UPDATE'):
            for bad in (b'"unfinished note', b'"closed" stray', b'bad"quote', b'"needless"'):
                with self.assertRaises(MV.LedgerRefused, msg=(row_note, bad)):
                    MV.parse_ledger(raw.replace(row_note, bad, 1), 'POWERBALL')

    def test_a_one_row_ledger_binds_the_whole_file_and_the_init_record(self):
        """A version-1-only ledger: the whole master must hash to row 1 (today's check, unchanged), and the INIT
        verification record must still match row 1."""
        grown = read(self.master)
        X.write_ledger(self.ledger, [dict(self.rows[0])])
        with self.assertRaises(MV.LedgerRefused):                      # the grown master is not version 1's bytes
            MV.load_verified_source(self.root, 'POWERBALL')
        v1 = b''.join(grown.splitlines(keepends=True)[:1 + self.rows[0]['draw_count']])
        self.master.write_bytes(v1)
        _raw, rows, _ev = MV.load_verified_source(self.root, 'POWERBALL')
        self.assertEqual([r.version for r in rows], [1])
        # EX_142 B03: the full grammar and rule 2 apply to a one-row ledger: the old seven-column fixture header, a
        # placeholder utc, a master one line short or one line long, and a wrong last draw each refuse
        seven = ('version,utc,action,master_sha256,first_draw,last_draw,draw_count\r\n'
                 f"1,fixture,INIT,{self.rows[0]['master_sha256']},1144,1576,433\r\n").encode('ascii')
        self.ledger.write_bytes(seven)
        with self.assertRaises(MV.LedgerRefused):
            MV.load_verified_source(self.root, 'POWERBALL')
        X.write_ledger(self.ledger, [dict(self.rows[0], utc='fixture')])
        with self.assertRaises(MV.LedgerRefused):
            MV.load_verified_source(self.root, 'POWERBALL')
        good_one_row = X.ledger_bytes([dict(self.rows[0])])
        self.ledger.write_bytes(good_one_row.replace(b'fixture INIT\r\n', b'"unfinished note\r\n'))   # EX_144 B03r1
        with self.assertRaises(MV.LedgerRefused):
            MV.load_verified_source(self.root, 'POWERBALL')
        self.ledger.write_bytes(good_one_row.replace(b'fixture INIT\r\n', b'"from grab, verified"\r\n'))
        MV.load_verified_source(self.root, 'POWERBALL')                 # a writer-style quoted note is accepted
        lines = v1.split(b'\n')
        ev = json.loads(read(self.evidence))
        for bad_master in (b'\n'.join(lines[:-2]) + b'\n', v1 + lines[-2] + b'\n',
                           b'\n'.join(lines[:-2] + [b'1575' + lines[-2][4:]]) + b'\n'):
            # the ledger and the INIT record are re-pinned to the bad bytes, so only rule 2's line rules can refuse
            self.master.write_bytes(bad_master)
            bad_sha = hashlib.sha256(bad_master).hexdigest()
            X.write_ledger(self.ledger, [dict(self.rows[0], master_sha256=bad_sha)])
            self.evidence.write_text(json.dumps(dict(ev, master_sha256=bad_sha)))
            with self.assertRaises(MV.LedgerRefused):
                MV.load_verified_source(self.root, 'POWERBALL')
        self.master.write_bytes(v1)
        X.write_ledger(self.ledger, [dict(self.rows[0])])
        self.evidence.write_text(json.dumps(ev))
        MV.load_verified_source(self.root, 'POWERBALL')
        ev['master_sha256'] = '0' * 64
        self.evidence.write_text(json.dumps(ev))
        with self.assertRaises(MV.LedgerRefused):                      # the INIT record disagrees with row 1
            MV.load_verified_source(self.root, 'POWERBALL')

    def test_prefix_oracle_and_every_row_verified(self):
        raw = read(self.master)
        rows = self.parse()
        for r in rows:
            self.assertEqual(X.independent_prefix_sha(raw, r.draw_count), r.master_sha256, r.version)
        MV.verify_master_against_ledger(raw, rows, 'POWERBALL')

    def test_a_corrected_earlier_row_refuses(self):
        """A change to a row inside version 1 breaks every later version's prefix check (design 3.2 rule 2)."""
        raw = read(self.master)
        lines = raw.split(b'\n')
        lines[5] = lines[5].replace(b',', b',', 1)[:-1] + (b'9' if not lines[5].endswith(b'9') else b'8')
        bad = b'\n'.join(lines)
        rows = self.parse()
        rows_fixed = [MV.LedgerRow(r.version, r.action, (hashlib.sha256(bad).hexdigest() if r.version >= 3 else r.master_sha256),
                                   r.first_draw, r.last_draw, r.draw_count) for r in rows]
        with self.assertRaises(MV.LedgerRefused):
            MV.verify_master_against_ledger(bad, rows_fixed, 'POWERBALL')
        self.master.write_bytes(bad)
        with self.assertRaises(MV.LedgerRefused):
            MV.load_verified_source(self.root, 'POWERBALL')

    def test_an_interrupted_update_refuses(self):
        """Master replaced, ledger not appended (finding A7): the master matches no row; every reader refuses."""
        raw = read(self.master) + X.varied_row(self.p, 1581, 0).encode('ascii') + b'\n'
        self.master.write_bytes(raw)
        with self.assertRaises(MV.LedgerRefused):
            MV.load_verified_source(self.root, 'POWERBALL')
        with self.assertRaises(ValueError):
            load_pinned_draw_view(repo_root=self.root, run_manifest=self.pin(1300, 4, self.rows[3]['master_sha256']))

    def pin(self, target, version, sha):
        return {'schema': 'DEVELOPMENT_MASTER_PIN_V1_REVIEW', 'game_id': 'POWERBALL', 'method_id': 'E_2',
                'variant_id': 'SYNTHETIC_CONTRACT_PROBE', 'draw_number': target, 'view_kind': 'UNORDERED_SET',
                'include_dates': False, 'master_file': 'POWERBALL_results_master.csv', 'ledger_version': version,
                'master_sha256': sha}

    def test_pins_resolve_only_to_their_own_row(self):
        rows = self.parse()
        for r in rows:
            self.assertEqual(MV.resolve_pin(rows, r.version, r.master_sha256), r)
        with self.assertRaises(MV.LedgerRefused):
            MV.resolve_pin(rows, 2, rows[2].master_sha256)        # version 2 with version 3's sha
        with self.assertRaises(MV.LedgerRefused):
            MV.resolve_pin(rows, 5, rows[3].master_sha256)        # no such version
        with self.assertRaises(MV.LedgerRefused):
            MV.resolve_pin(rows, '2', rows[1].master_sha256)      # not an int
        with self.assertRaises(MV.LedgerRefused):
            MV.resolve_pin(rows, 0, rows[0].master_sha256)

    def test_target_gate_by_version(self):
        rows = self.parse()
        self.assertTrue(MV.target_admissible('POWERBALL', 1577, rows[0]))      # last_draw(1) + 1
        self.assertFalse(MV.target_admissible('POWERBALL', 1578, rows[0]))
        self.assertTrue(MV.target_admissible('POWERBALL', 1580, rows[1]))      # last_draw(2) + 1
        self.assertFalse(MV.target_admissible('POWERBALL', 1581, rows[1]))
        self.assertTrue(MV.target_admissible('POWERBALL', 1581, rows[3]))
        self.assertFalse(MV.target_admissible('POWERBALL', 1144, rows[3]))
        self.assertFalse(MV.target_admissible('POWERBALL', '1300', rows[3]))


class ReaderOnAGrownMaster(unittest.TestCase):
    """The reader under the version-2 rules, both games; T-05 on a version-3 synthetic master."""

    def view(self, root, game, target, version, sha, dates=False):
        """The reader's own manifest, built directly (the request validator's mode rules are tested elsewhere)."""
        manifest = {'schema': 'DEVELOPMENT_MASTER_PIN_V1_REVIEW', 'game_id': game, 'method_id': 'E_2',
                    'variant_id': 'SYNTHETIC_CONTRACT_PROBE', 'draw_number': target, 'view_kind': 'UNORDERED_SET',
                    'include_dates': dates, 'master_file': f'{game}_results_master.csv', 'ledger_version': version,
                    'master_sha256': sha}
        return load_pinned_draw_view(repo_root=root, run_manifest=manifest)

    def test_version1_pin_and_current_pin_give_byte_identical_views_for_development_targets(self):
        """T-05 extended (Appendix L): on a version-3 master, every development target's view bytes, arrays and digest
        under a version-1 pin equal those under the current pin, and equal the version-1-only master's."""
        for p in (POWERBALL, OZLOTTO):
            with tempfile.TemporaryDirectory() as td1, tempfile.TemporaryDirectory() as td3:
                one, three = Path(td1), Path(td3)
                X.write_varied_master(one, p, p.holdout_first, 0)
                sha1 = json.loads(X.master_paths(one, p.game_id)[2].read_text())['master_sha256']
                rows = X.grow_master(three, p, [[p.holdout_first, p.holdout_first + 1], [p.holdout_first + 2]])
                self.assertEqual(rows[0]['master_sha256'], sha1)
                for t in F.targets(p):
                    a = self.view(one, p.game_id, t, 1, sha1)
                    b = self.view(three, p.game_id, t, 1, sha1)
                    c = self.view(three, p.game_id, t, 3, rows[2]['master_sha256'])
                    for x in (b, c):
                        self.assertEqual(x.main.tobytes(), a.main.tobytes(), (p.game_id, t))
                        self.assertEqual(x.draw_number.tobytes(), a.draw_number.tobytes())
                        if a.powerball is not None:
                            self.assertEqual(x.powerball.tobytes(), a.powerball.tobytes())
                        self.assertEqual(x.e1_view_digest(), a.e1_view_digest())
                        self.assertEqual(x.simple_rows(), a.simple_rows())

    def test_holdout_targets_need_the_opening_record(self):
        for p in (POWERBALL, OZLOTTO):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                rows = X.grow_master(root, p, [list(range(p.holdout_first, p.holdout_last + 3))])
                v2, sha2 = 2, rows[1]['master_sha256']
                # within the prefix: fine under either pin; one past the pinned version's last draw: fine below the holdout
                self.view(root, p.game_id, p.holdout_first - 1, v2, sha2)
                # a holdout target without an opening record: refused, with the pin otherwise valid
                with self.assertRaisesRegex(ValueError, 'opening record'):
                    self.view(root, p.game_id, p.holdout_first, v2, sha2)
                with self.assertRaisesRegex(ValueError, 'opening record'):
                    self.view(root, p.game_id, p.holdout_last + 3, v2, sha2)
                # beyond last_draw(v) + 1: refused by the version, whatever the record
                X.write_opening_record(root, p.game_id, freeze_version=1, freeze_sha=rows[0]['master_sha256'])
                with self.assertRaisesRegex(ValueError, 'pinned version'):
                    self.view(root, p.game_id, p.holdout_last + 4, v2, sha2)
                # with the record: the holdout targets and the next draw read their prefix only
                for t in (p.holdout_first, p.holdout_last, p.holdout_last + 3):
                    v = self.view(root, p.game_id, t, v2, sha2)
                    self.assertEqual(int(v.draw_number[-1]), t - 1)
                    self.assertEqual(len(v.draw_number), t - p.first_draw)
                # a version-1 pin never reaches the holdout, record or not
                with self.assertRaisesRegex(ValueError, 'pinned version'):
                    self.view(root, p.game_id, p.holdout_first + 1, 1, rows[0]['master_sha256'])
                # an invalid or mismatched opening record refuses
                X.write_opening_record(root, p.game_id, freeze_version=1, freeze_sha=rows[0]['master_sha256'],
                                       manifest_sha='a' * 64)
                with self.assertRaisesRegex(ValueError, 'opening record'):
                    self.view(root, p.game_id, p.holdout_first, v2, sha2)

    def test_crlf_master_and_a_no_change_row(self):
        p = OZLOTTO
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = X.grow_master(root, p, [None, [p.holdout_first]], crlf=True)
            self.assertEqual([r['action'] for r in rows], ['INIT', 'NO_CHANGE', 'UPDATE'])
            raw, parsed, _ev = MV.load_verified_source(root, 'OZLOTTO')
            self.assertEqual(parsed[1].master_sha256, parsed[0].master_sha256)
            for t in F.targets(p):
                a = self.view(root, 'OZLOTTO', t, 1, rows[0]['master_sha256'])
                b = self.view(root, 'OZLOTTO', t, 3, rows[2]['master_sha256'])
                self.assertEqual(a.e1_view_digest(), b.e1_view_digest())

    def test_the_legacy_1577_exception_is_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sha = X.write_varied_master(root, POWERBALL, 1577, 0)
            manifest = {'schema': 'DEVELOPMENT_MASTER_PIN_V1_REVIEW', 'game_id': 'POWERBALL', 'method_id': 'E_1',
                        'variant_id': 'FULL_HISTORY_RAW_COUNTS_V1', 'draw_number': 1577, 'view_kind': 'UNORDERED_SET',
                        'include_dates': False, 'master_file': 'POWERBALL_results_master.csv', 'ledger_version': 1,
                        'master_sha256': sha}
            v = load_pinned_draw_view(repo_root=root, run_manifest=manifest)
            self.assertEqual(int(v.draw_number[-1]), 1576)
            with self.assertRaises(ValueError):                       # any other method at 1577 needs the opening record
                self.view(root, 'POWERBALL', 1577, 1, sha)


class OutcomeReaderVersions(unittest.TestCase):
    """Design 3.2 rule 5: the outcome reader applies the same chain and pin rules; targets at or above the holdout's
    first draw stay refused until the freeze-before-outcome rule arrives with the Mode H scorer."""

    def test_version_pins_and_refusals(self):
        p = POWERBALL
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rows = X.grow_master(root, p, [[1577, 1578]])
            want = [1300, 1576]
            got1 = OREAD.read_outcomes(repo_root=root, game_id='POWERBALL', master_sha256=rows[0]['master_sha256'],
                                       targets=want, ledger_version=1)
            got2 = OREAD.read_outcomes(repo_root=root, game_id='POWERBALL', master_sha256=rows[1]['master_sha256'],
                                       targets=want, ledger_version=2)
            self.assertEqual(got1, got2)
            self.assertEqual(sorted(got1), want)
            with self.assertRaises(OREAD.OutcomeRefused):              # version 1's sha under version 2
                OREAD.read_outcomes(repo_root=root, game_id='POWERBALL', master_sha256=rows[0]['master_sha256'],
                                    targets=want, ledger_version=2)
            # the pinned version's own bytes are served, not the grown file (design 3.2 rule 5)
            served1 = OREAD._verify_source(root, 'POWERBALL', rows[0]['master_sha256'], 1)
            served2 = OREAD._verify_source(root, 'POWERBALL', rows[1]['master_sha256'], 2)
            self.assertEqual(hashlib.sha256(served1).hexdigest(), rows[0]['master_sha256'])
            self.assertEqual(hashlib.sha256(served2).hexdigest(), rows[1]['master_sha256'])
            self.assertTrue(served2.startswith(served1) and len(served2) > len(served1))
            with self.assertRaises(OREAD.OutcomeRefused):              # a holdout target: still refused in this slice
                OREAD.read_outcomes(repo_root=root, game_id='POWERBALL', master_sha256=rows[1]['master_sha256'],
                                    targets=[1577], ledger_version=2)
            with self.assertRaises(OREAD.OutcomeRefused):              # a corrected prefix
                m = X.master_paths(root, 'POWERBALL')[0]
                raw = m.read_bytes().split(b'\n')
                raw[3] = raw[3][:-1] + (b'9' if not raw[3].endswith(b'9') else b'8')
                m.write_bytes(b'\n'.join(raw))
                OREAD.read_outcomes(repo_root=root, game_id='POWERBALL', master_sha256=rows[1]['master_sha256'],
                                    targets=want, ledger_version=2)


class Static(unittest.TestCase):
    """L-U5: no module reads the master except through the reader's trusted-file helper or master_versions."""

    def test_only_the_readers_open_the_masters(self):
        names = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'src').rglob('*.py')
                       if '_results_master' in p.read_text(encoding='utf-8', errors='replace'))
        self.assertEqual(names, [
            'src/methods/Method_Contract_Runner.py', 'src/methods/_common/contract_receipts.py',
            'src/methods/_common/contract_records.py', 'src/methods/_common/contract_runner.py',
            'src/methods/_common/game_draws_reader.py', 'src/methods/_common/master_versions.py',
            'src/methods/_common/walk_forward.py', 'src/results_master_v0_2.py'])        # MHUP-A slice 2: v0.2 (design 7)
        mv = (ROOT / 'src' / 'methods' / '_common' / 'master_versions.py').read_text(encoding='ascii')
        for word in ('import numpy', 'Drawn_', 'simple_rows', 'header_for', '_parse_prefix', 'DrawView('):
            self.assertNotIn(word, mv)                                # nothing of a view, no decoded draw column
        self.assertEqual(mv.count('csv.reader('), 1)                  # the one CSV parse is the ledger's physical lines
        self.assertIn('csv.reader(physical', mv)


if __name__ == '__main__':
    unittest.main()
