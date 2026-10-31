"""WF-1B: the outcome reader's guards (design v0.1r1 sections 6.3 and 10). Invented masters only."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / 'src'), str(HERE.parent / 'src' / 'methods'), str(HERE)]
from _common.game_profiles import get_profile                  # noqa: E402
from evaluation import outcome_reader as R                     # noqa: E402
from test_e6_beta_bernoulli import FILES, varied_row, write_varied_master   # noqa: E402


def _master(root: Path, game: str, extra_lines=(), corrupt=None) -> str:
    """An invented master (draws E(G)..holdout_first-1), optionally with lines appended after it and one row's
    data columns replaced by undecodable bytes; the ledger and INIT record pin whatever bytes result."""
    p = get_profile(game)
    write_varied_master(root, p, p.holdout_first, 0)
    path = root / 'source_data' / FILES[0].format(g=game)
    raw = path.read_bytes()
    if corrupt is not None:
        lines = raw.split(b'\n')
        i = corrupt - p.first_draw + 1
        lines[i] = str(corrupt).encode() + b',\xff\xfe broken'
        raw = b'\n'.join(lines)
    raw += b''.join(extra_lines)
    path.write_bytes(raw)
    sha = hashlib.sha256(raw).hexdigest()
    led = root / 'source_data' / FILES[1].format(g=game)
    led.write_text('version,utc,action,master_sha256,first_draw,last_draw,draw_count\n'
                   f'1,fixture,INIT,{sha},{p.first_draw},{p.holdout_first - 1},{p.holdout_first - p.first_draw}\n')
    ev = root / 'source_data' / FILES[2].format(g=game)
    rec = json.loads(ev.read_text())
    rec['master_sha256'] = sha
    ev.write_text(json.dumps(rec))
    return sha


class Reading(unittest.TestCase):

    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.root = Path(self.td.name)

    def tearDown(self):
        self.td.cleanup()

    def test_only_grid_targets_returned(self):
        for game in ('POWERBALL', 'OZLOTTO'):
            with self.subTest(game=game):
                root = self.root / game
                sha = _master(root, game)
                p = get_profile(game)
                targets = [p.first_draw + 1, p.first_draw + 50, p.holdout_first - 1]
                got = R.read_outcomes(repo_root=root, game_id=game, master_sha256=sha, targets=targets)
                self.assertEqual(sorted(got), targets)
                for t in targets:
                    row = varied_row(p, t, 0).split(',')
                    main = tuple(sorted(int(x) for x in row[2:9]))
                    extra = int(row[9]) if game == 'POWERBALL' else tuple(sorted(int(x) for x in row[9:12]))
                    self.assertEqual(got[t], (main, extra))
                if game == 'OZLOTTO':
                    m, s = got[targets[0]]
                    self.assertEqual(len(s), 3)
                    self.assertFalse(set(m) & set(s))

    def test_targets_outside_the_prefix_refused_before_any_read(self):
        sha = _master(self.root, 'POWERBALL')
        p = get_profile('POWERBALL')
        for bad in ([p.first_draw], [p.holdout_first], [p.holdout_first + 5], [p.first_draw + 1, p.holdout_first],
                    [], ['1400'], [1400.0], [True]):
            with self.subTest(bad=bad), mock.patch.object(R, '_trusted_file_bytes',
                                                          side_effect=AssertionError('read')) as rd:
                with self.assertRaises(R.OutcomeRefused):
                    R.read_outcomes(repo_root=self.root, game_id='POWERBALL', master_sha256=sha, targets=bad)
                rd.assert_not_called()

    def test_rows_after_the_last_target_and_holdout_rows_are_never_decoded(self):
        """A planted line beyond 1576 (in an invented master) is never parsed; nor is an undecodable non-grid row."""
        p = get_profile('POWERBALL')
        planted = f'{p.holdout_first},2026-08-06,1,2,3,4,5,6,7,8\n'.encode() + b'\xff\xfe\n'
        sha = _master(self.root, 'POWERBALL', extra_lines=[planted], corrupt=p.first_draw + 10)
        got = R.read_outcomes(repo_root=self.root, game_id='POWERBALL', master_sha256=sha,
                              targets=[p.first_draw + 9, p.first_draw + 11, p.holdout_first - 1])
        self.assertEqual(len(got), 3)
        with self.assertRaises(R.OutcomeRefused):        # the corrupt row itself, when asked for, is refused
            R.read_outcomes(repo_root=self.root, game_id='POWERBALL', master_sha256=sha, targets=[p.first_draw + 10])

    def test_source_checks(self):
        p = get_profile('OZLOTTO')
        sha = _master(self.root, 'OZLOTTO')
        t = [p.first_draw + 3]
        with self.assertRaises(R.OutcomeRefused):
            R.read_outcomes(repo_root=self.root, game_id='OZLOTTO', master_sha256='0' * 64, targets=t)
        with self.assertRaises(R.OutcomeRefused):
            R.read_outcomes(repo_root=self.root, game_id='OZLOTTO', master_sha256='XYZ', targets=t)
        path = self.root / 'source_data' / FILES[0].format(g='OZLOTTO')
        path.write_bytes(path.read_bytes() + b'\n')       # master changed after the pin
        with self.assertRaises(R.OutcomeRefused):
            R.read_outcomes(repo_root=self.root, game_id='OZLOTTO', master_sha256=sha, targets=t)
        sha = _master(self.root, 'OZLOTTO')
        ev = self.root / 'source_data' / FILES[2].format(g='OZLOTTO')
        rec = json.loads(ev.read_text())
        rec['source'] = 'SOMEWHERE_ELSE'
        ev.write_text(json.dumps(rec))
        with self.assertRaises(R.OutcomeRefused):
            R.read_outcomes(repo_root=self.root, game_id='OZLOTTO', master_sha256=sha, targets=t)
        sha = _master(self.root, 'OZLOTTO')
        led = self.root / 'source_data' / FILES[1].format(g='OZLOTTO')
        led.write_text(led.read_text() + f'2,fixture,UPDATE,{sha},1,2,3\n')
        with self.assertRaises(R.OutcomeRefused):
            R.read_outcomes(repo_root=self.root, game_id='OZLOTTO', master_sha256=sha, targets=t)

    def test_a_hard_linked_master_is_refused(self):
        """A master with a second name (a hard link) is refused. This runs on every platform, Windows included."""
        sha = _master(self.root, 'POWERBALL')
        path = self.root / 'source_data' / FILES[0].format(g='POWERBALL')
        R.read_outcomes(repo_root=self.root, game_id='POWERBALL', master_sha256=sha, targets=[1200])   # control
        os.link(path, self.root / 'second_name.csv')
        with self.assertRaises(R.OutcomeRefused):
            R.read_outcomes(repo_root=self.root, game_id='POWERBALL', master_sha256=sha, targets=[1200])

    def test_a_symlinked_master_is_refused(self):
        """A master that is a symbolic link is refused. Skipped where the platform cannot make a symlink (Windows
        without the symlink privilege), as the other symlink tests are."""
        sha = _master(self.root, 'POWERBALL')
        path = self.root / 'source_data' / FILES[0].format(g='POWERBALL')
        other = self.root / 'copy.csv'
        other.write_bytes(path.read_bytes())
        path.unlink()
        try:
            path.symlink_to(other)
        except (OSError, NotImplementedError):
            self.skipTest('platform disallows symlinks')
        with self.assertRaises(R.OutcomeRefused):
            R.read_outcomes(repo_root=self.root, game_id='POWERBALL', master_sha256=sha, targets=[1200])

if __name__ == '__main__':
    unittest.main()
