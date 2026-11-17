"""MHUP-B slice 2: counted edits to the existing tests.

The static firewall (tests/test_wf1b_static.py) lists what an evaluator file may import. OV-1's recorder reads times
(the cut-off is an instant), so `datetime` joins the standard-library allowance. Nothing else changes: the recorder and
the comparison module import only `_common` modules already allowed, and neither imports the outcome reader.
Every old string must occur exactly once. Usage: python3 -I edit_tests_slice2.py TREE
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()


def edit(rel, pairs):
    p = tree / rel
    s = p.read_bytes().decode('ascii')
    assert '\r' not in s, rel
    for a, b in pairs:
        assert s.count(a) == 1, (rel, s.count(a), a[:80])
        s = s.replace(a, b)
    p.write_bytes(s.encode('ascii'))
    print('edited', rel, len(pairs))


edit('tests/test_wf1b_static.py', [
    ("STDLIB_OK = {'__future__', 'argparse', 'csv', 'collections', 'decimal', 'fractions', 'functools', 'hashlib', 'io',\n",
     "STDLIB_OK = {'__future__', 'argparse', 'csv', 'collections', 'datetime', 'decimal', 'fractions', 'functools', 'hashlib', 'io',\n"),
])


# ---------------------------------------------------------------- slice 1's tests of the weekly readiness check
# The owner's clarification of 18 November 2026 (decision log entry 84; EX_234 section 3): the developed record is the
# owner's declaration and the archived Mode H study is not consulted. Slice 1's two tests asserted the opposite
# (EX_230 F-230-A tied the record to the seal); they now assert the clarified rule.
edit('tests/test_mhupb_weekly_forecast.py', [
    ("""        # a developed record is believed only as the declaration of this game's sealed Mode H study (design 6.7)
        genuine = OR.developed_record_path(self.proj, self.GAME).read_bytes()
        for change in (dict(mode_h_score_digest='d' * 64), dict(mode_h_batch_id='wf-' + 'e' * 32),
                       dict(owner_statement='I say so'), dict(mode_h_batch_id=None)):
            with self.subTest(developed=change):
                self.write_developed(**change)
                OR.validate_developed_record(json.loads(OR.developed_record_path(self.proj, self.GAME).read_bytes()), self.GAME)
                with self.assertRaisesRegex(WS.SessionRefused, 'NOT_DEVELOPED'):
                    self.open()
        OR.developed_record_path(self.proj, self.GAME).write_bytes(genuine)
        seal = OR.marker_path(self.proj, self.GAME, self.BATCH, 'MODE_H_SEALED')
        seal.rename(self.td / 'seal.json')
        with self.assertRaisesRegex(WS.SessionRefused, 'not sealed'):
            self.open()
        (self.td / 'seal.json').rename(seal)
""",
     """        # a developed record is the owner's declaration: well formed, with his fixed sentence (design 6.7). The archived
        # Mode H study is not consulted (the owner's clarification of 18 November 2026): what the record says of it,
        # and whether its seal is there, do not gate the weekly session.
        genuine = OR.developed_record_path(self.proj, self.GAME).read_bytes()
        self.write_developed(owner_statement='I say so')
        OR.validate_developed_record(json.loads(OR.developed_record_path(self.proj, self.GAME).read_bytes()), self.GAME)
        with self.assertRaisesRegex(WS.SessionRefused, 'NOT_DEVELOPED'):
            self.open()
        for change in (dict(mode_h_score_digest='d' * 64), dict(mode_h_batch_id='wf-' + 'e' * 32)):
            self.write_developed(**change)
            self.assertEqual(WR.developed(self.proj, self.GAME)['owner_statement'], OR.DEVELOPED_STATEMENT)
        OR.developed_record_path(self.proj, self.GAME).write_bytes(genuine)
        seal = OR.marker_path(self.proj, self.GAME, self.BATCH, 'MODE_H_SEALED')
        seal.rename(self.td / 'seal.json')
        self.assertEqual(WR.developed(self.proj, self.GAME)['owner_statement'], OR.DEVELOPED_STATEMENT)
        (self.td / 'seal.json').rename(seal)
"""),
])
edit('tests/test_mhupb_weekly_score.py', [
    ("        self.write_developed(mode_h_score_digest='d' * 64)               # well formed, but not this game's sealed score\n",
     "        self.write_developed(owner_statement='I say so')                 # well formed, but not the owner's declaration\n"),
])
