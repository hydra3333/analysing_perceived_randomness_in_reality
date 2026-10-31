"""E1R2: CODE-3's first use and E_1 revision 2 (Claude, 31 October 2026; design v0.1r2, owner-ratified 31 October 2026).

Applies to a repository TREE (writes into it), which must be the base: REL-1 and WF-1A installed, no archive/.
  1. Retires E_1 revision 1 with CODE-3 (src/package_tools/method_retirement.py, which must already be in TREE):
     its seven files are copied unchanged to archive/methods/E_001/r1/ (paths relative to src/methods/), with the
     README; revision 2 reuses every path, so none is dropped (ER-3).
  2. E_1 revision 2: multigame_e1.py's data-kind check (and its comment) admits REAL_DEVELOPMENT as well; the
     legacy entry file's release gate names revision '2' (WF1-13; D2-3's gate is kept); the contract adapter's
     stale docstring sentence is corrected (ER-4); WF-1A's NOT_REAL_CAPABLE becomes empty.
  3. Contract data: declarations r2.json (r1's fields with method_revision "2") and registry entry_0002.json
     (SUPPORTED, revision 2, linked to entry_0001) for both games. The builder ships the two entries separately,
     in release_overlay/ (ER-2r1).
Every edit replaces text that must occur exactly once. Usage: python3 -I make_e1r2.py TREE PREPARED_DATE
"""
import sys
from pathlib import Path

tree, prepared = Path(sys.argv[1]).resolve(), sys.argv[2]
sys.path[:0] = [str(tree / 'src'), str(tree / 'src' / 'methods')]
from _common.contract_records import canonical, record_digest          # noqa: E402
from _common.contract_registry import InstalledRegistry                 # noqa: E402
from package_tools import method_retirement as MR                       # noqa: E402

M = tree / 'src' / 'methods'
CD = M / '_common' / 'contract_data'
assert not (tree / 'archive').exists(), 'archive/ already exists'
assert not (M / 'E_001' / 'IN_DEVELOPMENT.txt').exists()

R1_FILES = ['E_001/__init__.py', 'E_001/e1_common_reader_bridge.py', 'E_001/e1_historical_appearance_frequency.py',
            'E_001/e1_standalone_contract.py', 'E_001/e1_training_view.py', 'E_001/multigame_e1.py',
            'E_001_Historical_Appearance_Frequency.py']
assert sorted(p.relative_to(M).as_posix() for p in (M / 'E_001').glob('*.py')) == sorted(R1_FILES[:-1])
HELPERS = {'_common/canonical_encoding.py': '1', '_common/game_profiles.py': '1', '_common/game_draws_reader.py': '1',
           '_common/experiment_runtime_status_and_resources.py': '1', '_common/contract_dispatch.py': '1'}
README = MR.readme_text(
    method_id='E_1', method_name='Historical Appearance Frequency', revision='1', successor_revision='2',
    variants=['FULL_HISTORY_RAW_COUNTS_V1'], games=['POWERBALL', 'OZLOTTO'], prepared=prepared, previous_paths=R1_FILES,
    helpers=HELPERS,
    reason=("revision 1's multi-game function (`E_001/multigame_e1.py`) accepted synthetic contract data only, so E_1 "
            'could not run walk-forward on past draws; revision 2 also admits real development runs, with the same '
            "counting, ranking and tie order (owner decision WF1-13; CODE-3 and E_1 revision 2 design v0.1r2). E_1's "
            "legacy runner moved to revision 2's release check at the same time. Revision 2 reuses all seven paths: "
            'five files unchanged, and `E_001/multigame_e1.py` and `E_001_Historical_Appearance_Frequency.py` '
            'changed.'),
    replay_note=('These files are kept for reading. Nothing imports or runs them: no project code or test refers '
                 'to a path or module inside `archive/` (a static and a runtime check enforce this), and normal '
                 'runners never dispatch an archived revision (E2R-R56). `archive/` has no `__init__.py` files, but '
                 'that alone would not stop an import (Python 3 namespace packages). Re-running revision 1 would be a '
                 'separate, owner-approved act, attempted only if the preserved code, configuration and dependencies '
                 'are sufficient; exact historical replay is not promised. The shared helpers listed above are '
                 'revision 1 of the shared code; none was revised by the package that archived this revision.'))
MR.retire(tree, 'E_1', '1', R1_FILES, README)


def edit(rel, pairs):
    p = tree / rel
    s = p.read_bytes().decode('ascii')
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:60])
        s = s.replace(a, b)
    p.write_bytes(s.encode('ascii'))


edit('src/methods/E_001/multigame_e1.py', [(
    "    if data_kind != 'SYNTHETIC_CONTRACT_TEST':\n"
    "        # This new multi-game science runner remains OFF until later review.\n",
    "    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):\n"
    "        # Revision 2 (owner decision WF1-13): synthetic contract tests and real development runs only.\n")])
edit('src/methods/E_001_Historical_Appearance_Frequency.py', [(
    "        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '1')\n",
    "        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '2')\n")])
edit('src/methods/contract_adapters/e_001.py', [(
    "published record can never differ from what E_1 itself computes. E_1 keeps revision 1: no E_1 byte\n"
    "changes. E_1's function itself accepts only SYNTHETIC_CONTRACT_TEST data; real runs stay off there.\n",
    "published record can never differ from what E_1 itself computes. Since E_1 revision 2 (owner decision\n"
    "WF1-13), E_1's function accepts SYNTHETIC_CONTRACT_TEST and REAL_DEVELOPMENT data, with revision 1's counting.\n")])
edit('src/methods/_common/walk_forward.py', [(
    "NOT_REAL_CAPABLE = {'E_1': (\"E_1 revision 1's multi-game function accepts synthetic contract data only (E2RC-C04 \"\n"
    "                            \"option (a)); E_1 joins walk-forward batches as revision 2 (owner decision WF1-13)\")}\n",
    "# Empty since E_1 revision 2 (owner decision WF1-13), whose multi-game function admits real development runs.\n"
    "NOT_REAL_CAPABLE: dict[str, str] = {}\n")])

REASON = ('Revision 2 (CODE-3 and E_1 revision 2 design v0.1r2, owner decisions WF1-13 and ER-2r1, ratified '
          "31 October 2026): the multi-game function also admits REAL_DEVELOPMENT runs; counting, ranking and tie "
          'order are unchanged. Revision 1 is archived in archive/methods/E_001/r1/.')
reg = InstalledRegistry(CD)
for game in ('POWERBALL', 'OZLOTTO'):
    chain = reg.chain(game, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
    assert [(e['entry_sequence'], e['registry_status'], e['method_revision']) for e in chain] == [(1, 'SUPPORTED', '1')]
    e1 = chain[0]
    d1 = reg.declaration(e1['declaration_digest'])
    d2 = dict(d1, method_revision='2')
    dp = CD / 'declarations' / game / 'E_1' / 'FULL_HISTORY_RAW_COUNTS_V1' / 'r2.json'
    with dp.open('xb') as fh:
        fh.write(canonical(d2))
    e2 = dict(e1, entry_sequence=2, method_revision='2', declaration_digest=record_digest(d2),
              registry_status='SUPPORTED', registry_status_reason=REASON, effective_date='2026-10-31',
              previous_entry_digest=record_digest(e1))
    ep = CD / 'registry' / game / 'E_1' / 'FULL_HISTORY_RAW_COUNTS_V1' / 'entry_0002.json'
    with ep.open('xb') as fh:
        fh.write(canonical(e2))
reg2 = InstalledRegistry(CD)                 # reloads and validates every chain
for game in ('POWERBALL', 'OZLOTTO'):
    a = reg2.active_entry(game, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
    assert (a['method_revision'], a['registry_status']) == ('2', 'SUPPORTED')
print('E1R2: E_1 revision 1 archived (7 files and the README); revision 2 applied; 2 declarations and 2 entries added')
