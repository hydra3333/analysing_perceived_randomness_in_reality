"""WF-1B: N1's fair-draw generator (design v0.1r1 sections 7.2 and 9.3). Invented roots only; never a beacon value."""
from __future__ import annotations

import hashlib
import sys
import unittest
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from evaluation import n1_generator as G   # noqa: E402

ROOT = 'AB' * 64                    # the design's invented test root (section 9.3)
POL = 'N1_ROOT_TEST_ONLY_V1'


class PublishedValues(unittest.TestCase):
    """The values published in exchange/EX_077_Claude/ev_wf1_reference.txt, so a second implementation can match."""

    def test_key_and_first_word(self):
        key = G.stream_key(ROOT, POL, 'POWERBALL', 17, 1400)
        self.assertEqual(hashlib.sha256(key).hexdigest(),
                         'fe3ba4409dbde0e31a78dced448659df574147a296014cb49f81e66a88ffd741')
        self.assertEqual(G.first_word(ROOT, POL, 'POWERBALL', 17, 1400), 0x4609bee9cffb0e7d)

    def test_published_draws(self):
        self.assertEqual(G.fair_draw(ROOT, POL, 'POWERBALL', 17, 1400), ((9, 12, 13, 17, 27, 28, 35), 8))
        self.assertEqual(G.fair_draw(ROOT, POL, 'OZLOTTO', 1, 1500), ((1, 5, 12, 18, 19, 21, 44), (3, 15, 39)))

    def test_published_match_counts(self):
        """R = 200 replicates x 291 targets from 1286, ticket 1..7: the published counts, exactly."""
        counts, pb = [0] * 8, 0
        ticket = set(range(1, 8))
        for r in range(1, 201):
            for t in range(1286, 1286 + 291):
                m, b = G.fair_draw(ROOT, POL, 'POWERBALL', r, t)
                counts[len(ticket.intersection(m))] += 1
                pb += b == 7
        self.assertEqual(counts, [10070, 22774, 17944, 6284, 1055, 71, 2, 0])
        self.assertEqual(pb, 2954)
        exp = [Fraction(comb(7, m) * comb(28, 7 - m), comb(35, 7)) * 58200 for m in range(8)]
        chi = sum((counts[m] - exp[m]) ** 2 / exp[m] for m in range(5)) + \
            (sum(counts[5:]) - sum(exp[5:])) ** 2 / sum(exp[5:])
        self.assertLess(float(chi), 20.5)       # 5 df; 20.5 is about p = 0.001. Published: 8.69
        self.assertAlmostEqual(float(chi), 8.69, places=2)


class Shape(unittest.TestCase):

    def test_determinism_and_keying(self):
        a = G.fair_draw(ROOT, POL, 'POWERBALL', 3, 1300)
        self.assertEqual(a, G.fair_draw(ROOT, POL, 'POWERBALL', 3, 1300))
        self.assertNotEqual(a, G.fair_draw(ROOT, POL, 'POWERBALL', 4, 1300))
        self.assertNotEqual(a, G.fair_draw(ROOT, 'N1_OTHER_POLICY_V1', 'POWERBALL', 3, 1300))
        self.assertEqual(G.fair_draws_for_targets(ROOT, POL, 'POWERBALL', 3, [1300, 1301]),
                         [a, G.fair_draw(ROOT, POL, 'POWERBALL', 3, 1301)])

    def test_ranges(self):
        for r in range(1, 30):
            m, b = G.fair_draw(ROOT, POL, 'POWERBALL', r, 1500)
            self.assertEqual(len(set(m)), 7)
            self.assertEqual(list(m), sorted(m))
            self.assertTrue(all(1 <= x <= 35 for x in m) and 1 <= b <= 20)
            m, s = G.fair_draw(ROOT, POL, 'OZLOTTO', r, 1600)
            self.assertEqual(len(set(m) | set(s)), 10)
            self.assertTrue(all(1 <= x <= 47 for x in m + s))
            self.assertEqual((list(m), list(s)), (sorted(m), sorted(s)))

    def test_rejection_and_extension(self):
        """A stream that needs more than the first chunk extends it consistently (SHAKE prefix property)."""
        s = G._Stream(G.stream_key(ROOT, POL, 'OZLOTTO', 1, 1500))
        words = [s.word() for _ in range(80)]      # 640 bytes: beyond two chunks
        raw = hashlib.shake_256(s.key).digest(640)
        self.assertEqual(words, [int.from_bytes(raw[i:i + 8], 'little') for i in range(0, 640, 8)])

    def test_uniform_below_rule(self):
        class Fixed(G._Stream):
            def __init__(self, seq):
                self.seq = list(seq)

            def word(self):
                return self.seq.pop(0)
        k = 35
        limit = (1 << 64) - ((1 << 64) % k)
        s = Fixed([limit, limit + 5, 2 * k + 3])      # two rejected words, then 73 % 35 = 3
        self.assertEqual(s.below(k), 3)
        self.assertEqual(s.seq, [])


class Validation(unittest.TestCase):

    def test_root_and_inputs(self):
        for bad in ('ab' * 64, 'AB' * 63, 'AB' * 64 + 'A', 'G' * 128, None):
            with self.assertRaises(ValueError):
                G.fair_draw(bad, POL, 'POWERBALL', 1, 1300)
        for args in ((ROOT, '', 'POWERBALL', 1, 1300), (ROOT, POL, 'LOTTO', 1, 1300),
                     (ROOT, POL, 'POWERBALL', 0, 1300), (ROOT, POL, 'POWERBALL', 1, 0),
                     (ROOT, POL, 'POWERBALL', True, 1300), (ROOT, 'P\u00e9', 'POWERBALL', 1, 1300)):
            with self.assertRaises(ValueError):
                G.fair_draw(*args)


if __name__ == '__main__':
    unittest.main()
