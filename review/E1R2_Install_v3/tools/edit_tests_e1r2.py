"""E1R2: edits to existing tests for E_1 revision 2 (Claude, 31 October 2026; design v0.1r2 section 6, "(edits)").

E_1's active entry is now revision 2 (entry_0002), its legacy gate names revision '2', and WF-1A's NOT_REAL_CAPABLE
is empty. Each edit replaces text that must occur exactly once. Usage: python3 -I edit_tests_e1r2.py TREE
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()


def edit(rel, pairs):
    p = tree / rel
    s = p.read_bytes().decode('ascii')
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:70])
        s = s.replace(a, b)
    p.write_bytes(s.encode('ascii'))


edit('tests/test_e2r_dispatch.py', [
    ("            CD.legacy_gate('POWERBALL', *C.E1, '1')                                      # still released\n",
     "            CD.legacy_gate('POWERBALL', *C.E1, '2')                                      # still released\n"),
    ("        C.append_entry(self.data, C.entry(d1, 'FORMULA_OPEN', seq=2, prev=e1))\n",
     "        C.append_entry(self.data, C.entry(d1, 'FORMULA_OPEN', seq=e1['entry_sequence'] + 1, prev=e1))\n"),
    ("            with self.assertRaises(DispatchRefused) as cm:\n                CD.legacy_gate('POWERBALL', *C.E1, '1')\n",
     "            with self.assertRaises(DispatchRefused) as cm:\n                CD.legacy_gate('POWERBALL', *C.E1, '2')\n"),
    ("        self.assertIn(f'DISPATCH REFUSED: POWERBALL E_1 FULL_HISTORY_RAW_COUNTS_V1 revision 1: {expect}: ', err.getvalue())\n",
     "        self.assertIn(f'DISPATCH REFUSED: POWERBALL E_1 FULL_HISTORY_RAW_COUNTS_V1 revision 2: {expect}: ', err.getvalue())\n"),
    ("        C.append_entry(self.data, C.entry(reg.declaration(e1['declaration_digest']), 'FORMULA_OPEN', seq=2, prev=e1))\n",
     "        C.append_entry(self.data, C.entry(reg.declaration(e1['declaration_digest']), 'FORMULA_OPEN',\n"
     "                                          seq=e1['entry_sequence'] + 1, prev=e1))\n"),
    ("        entry, decl = CD.legacy_gate('POWERBALL', *C.E1, '1')\n",
     "        entry, decl = CD.legacy_gate('POWERBALL', *C.E1, '2')                         # E_1 revision 2 (WF1-13)\n"),
])
edit('tests/test_rel1_release.py', [
    ("            self.assertEqual([(e['entry_sequence'], e['registry_status']) for e in e1], [(1, 'SUPPORTED')])\n",
     "            # E_1's chain gained revision 2 (CODE-3 and E_1 revision 2 package); REL-1 itself left it unchanged.\n"
     "            self.assertEqual([(e['entry_sequence'], e['registry_status'], e['method_revision']) for e in e1],\n"
     "                             [(1, 'SUPPORTED', '1'), (2, 'SUPPORTED', '2')])\n"),
])
edit('tests/test_wf1a_walk_forward.py', [
    ("constants to that folder, as the existing tests patch fixed constants; the installed registry and method folders\n"
     "are used as installed (after REL-1). A small cohort (E_6 and E_7, six variants; E_1 revision 1 is not real-capable, so it is named in each plan as not in\n"
     "the cohort) over three targets keeps it fast.\n",
     "constants to that folder, as the existing tests patch fixed constants; the installed registry and method folders\n"
     "are used as installed. A small cohort (E_6 and E_7, six variants) over three targets keeps it fast; E_1, in the\n"
     "cohort since its revision 2 (owner decision WF1-13), is run by test_e1r2_revision2.\n"),
    ("    return {'E_1': M.ADAPTERS['E_1'], 'E_6': M.ADAPTERS['E_6'], 'E_7': M.ADAPTERS['E_7']}\n",
     "    return {'E_6': M.ADAPTERS['E_6'], 'E_7': M.ADAPTERS['E_7']}\n"),
    ("        self.assertEqual([(x['method_id'], x['variant_id']) for x in plan['not_in_cohort']],\n"
     "                         [('E_1', 'FULL_HISTORY_RAW_COUNTS_V1')])           # named with its reason, not run\n",
     "        self.assertEqual(plan['not_in_cohort'], [])                         # empty since E_1 revision 2\n"),
    ("        self.assertEqual(set(WF.NOT_REAL_CAPABLE), {'E_1'})             # E_1 r1 until its revision 2 (WF1-13)\n",
     "        self.assertEqual(WF.NOT_REAL_CAPABLE, {})                       # empty since E_1 revision 2 (WF1-13)\n"),
    ("                         sorted([('E_1', WF.NOT_REAL_CAPABLE['E_1'])] + [('E_6', 'test harness: not real-capable')] * 3))\n",
     "                         [('E_6', 'test harness: not real-capable')] * 3)\n"),
    ("    def test_why_e1_revision_1_is_not_in_the_cohort(self):\n"
     "        \"\"\"E_1's frozen revision-1 function refuses real data, so a run of it would only ever fail.\"\"\"\n",
     "    def test_e1_revision_2_admits_real_development(self):\n"
     "        \"\"\"E_1 revision 1's function refused real data; revision 2's admits it and still refuses a holdout run.\"\"\"\n"),
    ("        with self.assertRaises(ValueError):\n"
     "            forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='REAL_DEVELOPMENT')\n",
     "        forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='REAL_DEVELOPMENT')\n"
     "        with self.assertRaises(ValueError):\n"
     "            forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='REAL_HOLDOUT')\n"),
])
print('E1R2: 3 existing test files edited')
