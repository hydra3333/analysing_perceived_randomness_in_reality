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
