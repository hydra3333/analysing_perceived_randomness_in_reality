"""MHUP-A slice 1: E_1 revision 3 by the CODE-3 pattern (design v0.1r5 section 2; owner decision MHUP-Q10).

Applies to a dev TREE whose src/methods/E_001/ files are still revision 2's BASE bytes (run before apply_slice1.py):
  1. Retires E_1 revision 2 with CODE-3 (src/package_tools/method_retirement.py): its seven files are copied
     unchanged to archive/methods/E_001/r2/ (paths relative to src/methods/), with the README; revision 3 reuses every
     path, so none is dropped (E2R-R54; as ER-3 did for revision 1).
  2. Contract data: declarations r3.json (r2's fields with method_revision "3") and registry entry_0003.json
     (SUPPORTED, revision 3, linked to entry_0002) for both games. The entries are shipped behind E_1's own
     IN_DEVELOPMENT.txt barrier at install time (ER-2r1 extended, Appendix J), so revision 3 is never runnable before
     the release record.
The code edits of revision 3 themselves are apply_slice1.py's. Usage: python3 -I make_e1r3.py TREE PREPARED_DATE
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
assert (tree / 'archive' / 'methods' / 'E_001' / 'r1').is_dir(), 'revision 1 archive missing'
assert not (tree / 'archive' / 'methods' / 'E_001' / 'r2').exists(), 'r2 archive already exists'
assert not (M / 'E_001' / 'IN_DEVELOPMENT.txt').exists()
# The tree must still hold revision 2's bytes: its admission check names the run modes it admitted.
assert "if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):" in (M / 'E_001' / 'multigame_e1.py').read_text()

R2_FILES = ['E_001/__init__.py', 'E_001/e1_common_reader_bridge.py', 'E_001/e1_historical_appearance_frequency.py',
            'E_001/e1_standalone_contract.py', 'E_001/e1_training_view.py', 'E_001/multigame_e1.py',
            'E_001_Historical_Appearance_Frequency.py']
assert sorted(p.relative_to(M).as_posix() for p in (M / 'E_001').glob('*.py')) == sorted(R2_FILES[:-1])
HELPERS = {'_common/canonical_encoding.py': '1', '_common/game_profiles.py': '1', '_common/game_draws_reader.py': '1',
           '_common/experiment_runtime_status_and_resources.py': '1', '_common/contract_dispatch.py': '1'}
README = MR.readme_text(
    method_id='E_1', method_name='Historical Appearance Frequency', revision='2', successor_revision='3',
    variants=['FULL_HISTORY_RAW_COUNTS_V1'], games=['POWERBALL', 'OZLOTTO'], prepared=prepared, previous_paths=R2_FILES,
    helpers=HELPERS,
    reason=("revision 2's multi-game function (`E_001/multigame_e1.py`) refused, in its own code, every run mode other "
            'than SYNTHETIC_CONTRACT_TEST and REAL_DEVELOPMENT and every target beyond the development prefix, so E_1 '
            'could take part in neither Mode H nor the weekly session; revision 3 takes the view data kind instead of '
            'a run mode and leaves the target ceiling to the shared target and mode gates, with the same counting, '
            'ranking and tie order (MHUP-1 design v0.1r5 section 2; owner decision MHUP-Q10, 3 November 2026). The '
            "legacy runner's release check names revision 3 at the same time. Revision 3 reuses all seven paths: five "
            'files unchanged, and `E_001/multigame_e1.py` and `E_001_Historical_Appearance_Frequency.py` changed.'),
    replay_note=('These files are kept for reading. Nothing imports or runs them: no project code or test refers '
                 'to a path or module inside `archive/` (a static and a runtime check enforce this), and normal '
                 'runners never dispatch an archived revision (E2R-R56). `archive/` has no `__init__.py` files, but '
                 'that alone would not stop an import (Python 3 namespace packages). Re-running revision 2 would be a '
                 'separate, owner-approved act, attempted only if the preserved code, configuration and dependencies '
                 'are sufficient; exact historical replay is not promised. The shared helpers listed above are '
                 'revision 1 of the shared code as revision 2 used them; `_common/game_draws_reader.py` and '
                 '`_common/contract_dispatch.py` are revised by the package that archives this revision (MHUP-A), '
                 'and their revision-1 bytes are in the Git history of the commit that installs it.'))
MR.retire(tree, 'E_1', '2', R2_FILES, README)

REASON = ('Revision 3 (MHUP-1 design v0.1r5 section 2; owner decisions MHUP-Q10 and MHUP-R, ratified 3 November 2026): '
          'the multi-game function takes the view data kind, never a run mode, so E_1 runs in Mode H and the weekly '
          'session under the shared target and mode gates; counting, ranking and tie order are unchanged. Revision 2 '
          'is archived in archive/methods/E_001/r2/. effective_date is the date this entry was prepared and frozen for '
          'review in its package, not an installation or release date (owner decision, 4 November 2026, EX_142 C01): '
          'the release date comes only from the create-only release record (design 4.3).')
reg = InstalledRegistry(CD)
for game in ('POWERBALL', 'OZLOTTO'):
    chain = reg.chain(game, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
    assert [(e['entry_sequence'], e['registry_status'], e['method_revision']) for e in chain] == [
        (1, 'SUPPORTED', '1'), (2, 'SUPPORTED', '2')], chain
    e2 = chain[1]
    d2 = reg.declaration(e2['declaration_digest'])
    d3 = dict(d2, method_revision='3')
    dp = CD / 'declarations' / game / 'E_1' / 'FULL_HISTORY_RAW_COUNTS_V1' / 'r3.json'
    with dp.open('xb') as fh:
        fh.write(canonical(d3))
    e3 = dict(e2, entry_sequence=3, method_revision='3', declaration_digest=record_digest(d3),
              registry_status='SUPPORTED', registry_status_reason=REASON, effective_date=prepared,
              previous_entry_digest=record_digest(e2))
    ep = CD / 'registry' / game / 'E_1' / 'FULL_HISTORY_RAW_COUNTS_V1' / 'entry_0003.json'
    with ep.open('xb') as fh:
        fh.write(canonical(e3))
reg3 = InstalledRegistry(CD)                 # reloads and validates every chain
for game in ('POWERBALL', 'OZLOTTO'):
    a = reg3.active_entry(game, 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1')
    assert (a['method_revision'], a['registry_status']) == ('3', 'SUPPORTED')
print('E1R3: E_1 revision 2 archived (7 files and the README); 2 declarations and 2 entries added')
