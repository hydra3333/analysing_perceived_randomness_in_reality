"""MHUP-A slice 2: counted edits to the existing tests that change (design v0.1r5 Appendix L: tests/test_wf1b_static.py
lines 12-16 and 63; and slice 1's test_mhupa_master_versions.py, which names the updater file; the handback lists every one). Every old string must occur exactly once.
Usage: edit_tests_slice2.py TREE"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()


def edit(rel, pairs):
    p = tree / rel
    s = p.read_bytes().decode('ascii')
    for a, b in pairs:
        assert s.count(a) == 1, (rel, s.count(a), a[:90])
        s = s.replace(a, b)
    p.write_bytes(s.encode('ascii'))
    print('edited', rel, len(pairs))


# ---------------------------------------------------------------- test_wf1b_static.py (Appendix L)
edit('tests/test_wf1b_static.py', [
    # lines 12-15: the evaluator may import the two new _common modules (value-free owner records; the closure)
    ("                  '_common.master_versions'}       # MHUP-A: the version-2 master rules (design 3.2, Appendix L)\n",
     "                  '_common.master_versions',       # MHUP-A: the version-2 master rules (design 3.2, Appendix L)\n"
     "                  '_common.owner_records',         # MHUP-A slice 2: the value-free owner records, plans, tickets, markers\n"
     "                  '_common.closure'}               # MHUP-A slice 2: the closure and environment inventories (4.1)\n"),
    # line 63: Method_Mode_H.py's module mode_h.py may import the outcome reader (design 6.1: the Mode H scorer)
    ("        users = [p.name for p in EVAL.glob('*.py') if any(n.endswith('outcome_reader') for n in imports(p))]\n"
     "        self.assertEqual(sorted(users), ['report.py'])\n",
     "        users = [p.name for p in EVAL.glob('*.py') if any(n.endswith('outcome_reader') for n in imports(p))]\n"
     "        self.assertEqual(sorted(users), ['mode_h.py', 'report.py'])     # MHUP-A: the Mode H scorer (design 5.3, 6.1)\n"),
])

# ---------------------------------------------------------------- test_mhupa_master_versions.py (slice 1's test; the updater is
# now v0.2 and the old file is gone, design 7)
edit('tests/test_mhupa_master_versions.py', [
    ("        src = (ROOT / 'src' / 'results_master_v0_1.py').read_text(encoding='utf-8')\n",
     "        src = (ROOT / 'src' / 'results_master_v0_2.py').read_text(encoding='utf-8')     # MHUP-A slice 2: v0.2 (design 7)\n"),
    ("            'src/methods/_common/walk_forward.py', 'src/results_master_v0_1.py'])\n",
     "            'src/methods/_common/walk_forward.py', 'src/results_master_v0_2.py'])        # MHUP-A slice 2: v0.2 (design 7)\n"),
])
