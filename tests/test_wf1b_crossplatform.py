"""WF-1B cross-platform byte identity of the scorer's figures (design v0.1r1 section 6.6, "Byte identity"; MRT-08).

Fixed invented per-target codes for 12 tracks in each game go through every stage-2 measure; every figure the report
prints (counts, exact rationals, p-values with their log10 text, sigma, intervals, labels) is written as CSV text,
and its SHA-256 is compared with the value pinned on Linux. The owner's Windows run of this test is the
cross-platform evidence. No method, master or outcome is involved."""
from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from evaluation import divisions as DV   # noqa: E402
from evaluation import measures as MS    # noqa: E402
from evaluation import numerics as NU    # noqa: E402

PINNED = 'cd203c154971f683b5c25fd1f85ee8e3edee2819c199dc0aeed55391d6ed3cd5'


def codes(game: str, track: int, n: int) -> list[dict]:
    out = []
    for i in range(n):
        h = hashlib.sha256(f'{game}:{track}:{i}'.encode()).digest()
        m = [0, 0, 1, 1, 1, 2, 2, 3, 4, 5][h[0] % 10] if track % 3 else [0, 1, 1, 2, 2, 3, 3, 4, 6, 7][h[0] % 10]
        t = {'draw_number': 1300 + i, 'main_matches': m}
        if game == 'POWERBALL':
            t['powerball_match'] = int(h[1] % 20 == 0 or (track == 5 and h[1] % 4 == 0))
            t['division'] = DV.division(game, m, powerball_match=t['powerball_match'])
        else:
            t['supplementary_matches'] = min(7 - m, h[1] % 3)
            t['division'] = DV.division(game, m, supplementary_matches=t['supplementary_matches'])
        out.append(t)
    return out


def text(v) -> str:
    if isinstance(v, dict):
        return '{' + ';'.join(f'{k}={text(v[k])}' for k in sorted(v, key=str)) + '}'
    if isinstance(v, (list, tuple)):
        return '[' + ';'.join(text(x) for x in v) + ']'
    if isinstance(v, float):
        return v.hex()
    return str(v)


def figures() -> bytes:
    lines = []
    for game in ('POWERBALL', 'OZLOTTO'):
        for track in range(12):
            n = [291, 220, 12, 1][track % 4]
            tg = codes(game, track, n)
            for fn in (MS.mr0, MS.mr1, MS.mr4, MS.mr7, MS.mr16):
                for sid, sub in fn(game, tg, 'GRID_COMPLETE')['sub_measures'].items():
                    keep = {k: sub[k] for k in sub if k not in ('descriptive_key', 'significance_key', 'significance',
                                                                'approx', 'n1')}
                    sig = sub.get('significance') or {}
                    keep['sig'] = {k: sig.get(k) for k in ('label', 'P_up', 'P_lo', 'P_up_output', 'Z_plus', 'Z_minus')}
                    lines.append(f'{game},{track},{sid},{text(keep)}')
    return ('\n'.join(lines) + '\n').encode('ascii')


class CrossPlatform(unittest.TestCase):
    def test_figures_are_byte_identical_to_the_linux_run(self):
        self.assertEqual(hashlib.sha256(figures()).hexdigest(), PINNED)


if __name__ == '__main__':
    print(hashlib.sha256(figures()).hexdigest())
