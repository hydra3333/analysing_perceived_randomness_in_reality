"""REL-1 (Claude, 31 October 2026): release the 39 variants of E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18
and E_19 in both games (design v0.1r1 section 4; owner decisions WF1-1, WF1-2, ratified 31 October 2026).

For every (game, method, variant) chain of those methods except the NOT_YET_SPECIFIED placeholder, it appends
entry_0002.json: entry_0001 with entry_sequence 2, registry_status SUPPORTED, a REL-1 reason, the release date and
previous_entry_digest = the digest of entry_0001; every other field (revision, declaration digest, texts) unchanged.
It deletes the 11 IN_DEVELOPMENT.txt flags. It refuses if any chain is not exactly [entry_0001 FORMULA_OPEN].
Usage: python3 -I make_rel1_release.py TREE   (TREE: a repository tree; writes into it)
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'src' / 'methods'))
from _common.contract_records import canonical, record_digest      # noqa: E402
from _common.contract_registry import InstalledRegistry            # noqa: E402

METHODS = ('E_2', 'E_3', 'E_4', 'E_6', 'E_7', 'E_8', 'E_9', 'E_10', 'E_17', 'E_18', 'E_19')
REASON = ('Released by package REL-1 (releases and WF-1 design v0.1r1, owner decisions WF1-1 and WF1-2, '
          'ratified 31 October 2026). Contract runs on real data need the separate real-development gate.')
DATE = '2026-10-31'
data = tree / 'src' / 'methods' / '_common' / 'contract_data'
reg = InstalledRegistry(data)
n = 0
for (g, m, v) in sorted(reg.chain_keys()):
    if m not in METHODS or v == 'NOT_YET_SPECIFIED':
        continue
    chain = reg.chain(g, m, v)
    assert [(e['entry_sequence'], e['registry_status']) for e in chain] == [(1, 'FORMULA_OPEN')], (g, m, v)
    e1 = chain[0]
    e2 = dict(e1, entry_sequence=2, registry_status='SUPPORTED', registry_status_reason=REASON,
              effective_date=DATE, previous_entry_digest=record_digest(e1))
    p = data / 'registry' / g / m / v / 'entry_0002.json'
    with p.open('xb') as fh:
        fh.write(canonical(e2))
    n += 1
flags = sorted((tree / 'src' / 'methods').glob('E_[0-9][0-9][0-9]/IN_DEVELOPMENT.txt'))
assert [f.parent.name for f in flags] == ['E_%03d' % int(m[2:]) for m in METHODS], [f.parent.name for f in flags]
for f in flags:
    f.unlink()
reg2 = InstalledRegistry(data)          # reloads and validates every chain
sup = sorted((g, m, v) for (g, m, v) in reg2.chain_keys() if reg2.active_entry(g, m, v)['registry_status'] == 'SUPPORTED')
assert n == 78 and len(sup) == 80, (n, len(sup))
print(f'REL-1: {n} entry_0002 records appended; {len(flags)} flags deleted; {len(sup)} SUPPORTED chains in all (E_1 x 2 + 78)')
