"""P2-R1-O1: T-05 hardening - intermediate targets and equal-length suffix rewrites (OFFLINE).

Synthetic masters only: every row is invented, no real draw value is read, and no file under
the repository's source_data/ is opened. For each game, at several development targets N, the
rows at and after N are rewritten in two ways that keep the master's byte length identical
(so a leak of file size, or of anything length-derived, would not show up as a difference
between the variants and must instead be caught by comparing the views), plus one way that
changes the length. Every DrawView slot, array byte, dtype, shape, simple_rows() and
e1_view_digest() must be identical across all variants, and no slot may carry any master,
ledger or INIT-record hash. A second test proves every variant row is itself a valid row, by
loading it as part of an eligible prefix (TH-1 v1r2, reviewer finding TH1-C01).
"""
from collections.abc import Mapping
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src' / 'methods'))
from _common.game_draws_reader_v1 import DrawView, load_pinned_draw_view, header_for
from _common.game_profiles_v1 import POWERBALL, OZLOTTO

KINDS = ('UNORDERED_SET', 'OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC')
FILES = ('{g}_results_master.csv', '{g}_results_master_ledger.csv',
         '{g}_results_master_init_verification.json')


def synthetic_row(profile, draw, variant):
    """An invented, structurally valid row. variant 0 is the base; 1 and 2 have the same byte
    length as 0 but different values; 3 is longer. Never a real result."""
    if profile is POWERBALL:
        main = [10, 11, 12, 13, 14, 15, 16]
        extra = [2]
    else:
        main = [20, 21, 22, 23, 24, 25, 26]
        extra = [40, 41, 42]
    if variant == 1:
        main = [m + 7 for m in main]          # same two-digit widths
    elif variant == 2:
        main = list(reversed(main))           # same values, different drawn order
        extra = [e + 1 for e in extra] if profile is OZLOTTO else [3]
    elif variant == 3:
        main = [1, 2, 3, 4, 5, 6, 7]          # one-digit values: a shorter row ...
    seq = [draw, profile.derived_date(draw).isoformat(), *main, *extra]
    fields = list(map(str, seq))
    if variant == 3:
        # ... with every number field quoted: still a valid CSV row, but longer, so the
        # whole file grows (reviewer's TH1-C01 replacement; trailing padding was invalid).
        fields[2:] = [f'"{field}"' for field in fields[2:]]
    return ','.join(fields)


def write_master(root, profile, target, variant):
    game = profile.game_id
    folder = root / 'source_data'
    folder.mkdir(parents=True, exist_ok=True)
    rows = [','.join(header_for(game))]
    for draw in range(profile.first_draw, profile.holdout_first):
        rows.append(synthetic_row(profile, draw, 0 if draw < target else variant))
    raw = ('\n'.join(rows) + '\n').encode('ascii')
    sha = hashlib.sha256(raw).hexdigest()
    (folder / FILES[0].format(g=game)).write_bytes(raw)
    ledger = ('version,utc,action,master_sha256,first_draw,last_draw,draw_count\n'
              f'1,fixture,INIT,{sha},{profile.first_draw},{profile.holdout_first - 1},'
              f'{profile.holdout_first - profile.first_draw}\n')
    (folder / FILES[1].format(g=game)).write_bytes(ledger.encode('ascii'))
    evidence = {'master_sha256': sha, 'master_file': FILES[0].format(g=game), 'game': game,
                'first_draw': profile.first_draw, 'last_draw': profile.holdout_first - 1,
                'draw_count': profile.holdout_first - profile.first_draw,
                'source': 'LOTTERYWEST_GOV_RESULTS_SEARCH'}
    (folder / FILES[2].format(g=game)).write_text(json.dumps(evidence))
    hashes = {hashlib.sha256((folder / f.format(g=game)).read_bytes()).hexdigest() for f in FILES}
    return sha, len(raw), hashes


def pin(game, target, kind, dates, sha):
    return dict(schema='DEVELOPMENT_MASTER_PIN_V1_REVIEW', game_id=game, method_id='E_2',
                variant_id='SYNTHETIC_DIAGNOSTIC', draw_number=target, view_kind=kind,
                include_dates=dates, master_file=f'{game}_results_master.csv',
                ledger_version=1, master_sha256=sha)


class T05HardeningTests(unittest.TestCase):

    def snapshot(self, view, forbidden):
        def scan(obj, field):
            if isinstance(obj, str):
                for h in forbidden:
                    self.assertNotIn(h, obj, f'{field} carries an orchestration hash')
            elif isinstance(obj, Mapping):
                for k, v in obj.items():
                    scan(k, field)
                    scan(v, field)
            elif isinstance(obj, (list, tuple)):
                for v in obj:
                    scan(v, field)
            elif isinstance(obj, np.ndarray) and obj.dtype.kind in 'US':
                scan(obj.tolist(), field)
        out = []
        for field in DrawView.__slots__:
            value = getattr(view, field)
            scan(value, field)
            if isinstance(value, np.ndarray):
                self.assertIs(type(value.base), bytes)
                self.assertEqual(len(value.base), value.nbytes)
                self.assertFalse(value.flags.writeable)
                out.append((field, 'array', str(value.dtype), value.shape, value.tobytes(order='C')))
            elif isinstance(value, Mapping):
                out.append((field, 'mapping', tuple(sorted(value.items()))))
            else:
                out.append((field, 'scalar', value))
        return tuple(out), view.e1_view_digest(), json.dumps(view.simple_rows())

    def test_intermediate_targets_and_equal_length_suffix_rewrites(self):
        for profile in (POWERBALL, OZLOTTO):
            last = profile.holdout_first - 1
            targets = sorted({profile.first_draw + 2, (profile.first_draw + last) // 2,
                              last - 1, last})
            for target in targets:
                self.assertTrue(profile.historical_development_target_allowed(target))
                for kind in KINDS:
                    for dates in (False, True):
                        with self.subTest(game=profile.game_id, target=target, kind=kind,
                                          dates=dates), tempfile.TemporaryDirectory() as td:
                            root = Path(td)
                            seen, lengths, forbidden, shas = [], [], set(), set()
                            for variant in (0, 1, 2, 3):
                                sha, size, hashes = write_master(root, profile, target, variant)
                                forbidden |= hashes
                                shas.add(sha)
                                lengths.append(size)
                                view = load_pinned_draw_view(
                                    repo_root=root,
                                    run_manifest=pin(profile.game_id, target, kind, dates, sha))
                                seen.append(view)
                            # The rewrites really changed the file, two of them at equal length.
                            self.assertEqual(len(shas), 4)
                            self.assertEqual(lengths[0], lengths[1])
                            self.assertEqual(lengths[0], lengths[2])
                            self.assertNotEqual(lengths[0], lengths[3])
                            snaps = [self.snapshot(v, forbidden) for v in seen]
                            for other in snaps[1:]:
                                self.assertEqual(other, snaps[0])
                            self.assertEqual(len(seen[0].simple_rows()),
                                             target - profile.first_draw)

    def test_every_suffix_variant_row_is_a_valid_row(self):
        """Grammar check: load each variant's first changed row as part of an eligible prefix.

        The changed rows start at `start`; the view is taken at start + 1, so the reader must
        decode row `start` as an ordinary development row. Only synthetic data is involved.
        """
        for profile in (POWERBALL, OZLOTTO):
            start = (profile.first_draw + profile.holdout_first - 1) // 2
            for variant in (0, 1, 2, 3):
                for kind in KINDS:
                    for dates in (False, True):
                        with self.subTest(game=profile.game_id, variant=variant, kind=kind,
                                          dates=dates), tempfile.TemporaryDirectory() as td:
                            root = Path(td)
                            sha, _, _ = write_master(root, profile, start, variant)
                            view = load_pinned_draw_view(
                                repo_root=root,
                                run_manifest=pin(profile.game_id, start + 1, kind, dates, sha))
                            self.assertEqual(len(view.simple_rows()),
                                             start + 1 - profile.first_draw)


if __name__ == '__main__':
    unittest.main()
