"""MHUP-B slice 3: counted edits to the existing tests.

 test_mhupb_ov1  slice 2's static test pins the exact set of modules OV-1's recorder imports. Slice 3 connects
                 `ov1.publication_names` to the league's publication manifests (supplement 6.8; EX_237 section 5), so
                 the league's read-only source module joins that set. Nothing else of the test changes.
Every old string must occur exactly once. Usage: python3 -I edit_tests_slice3.py TREE
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


edit('tests/test_mhupb_ov1.py', [
    ("'_common.contract_records.sha256_hex', '_common.game_profiles.get_profile', '..collect', '..ov1_numeric'})\n",
     "'_common.contract_records.sha256_hex', '_common.game_profiles.get_profile', '..collect', '..ov1_numeric',\n"
     "            '..league_sources'})        # slice 3: the reader of the league's publication manifests (read-only)\n"),
])
