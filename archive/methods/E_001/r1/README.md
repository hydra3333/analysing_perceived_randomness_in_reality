# E_1 revision 1 (archived)

- **Method:** E_1, Historical Appearance Frequency, revision 1; variants: `FULL_HISTORY_RAW_COUNTS_V1`; games: POWERBALL, OZLOTTO.
- **Prepared:** 2026-10-31 (the date this archive was prepared by its package).
- **Retired:** when the owner installs that package. The installation date and commit are recorded in the ratification register, not here.
- **Superseded by:** revision 2.
- **Why retired:** revision 1's multi-game function (`E_001/multigame_e1.py`) accepted synthetic contract data only, so E_1 could not run walk-forward on past draws; revision 2 also admits real development runs, with the same counting, ranking and tie order (owner decision WF1-13; CODE-3 and E_1 revision 2 design v0.1r2). E_1's legacy runner moved to revision 2's release check at the same time. Revision 2 reuses all seven paths: five files unchanged, and `E_001/multigame_e1.py` and `E_001_Historical_Appearance_Frequency.py` changed.

## Previous paths under `src/methods/`

- `E_001/__init__.py`
- `E_001/e1_common_reader_bridge.py`
- `E_001/e1_historical_appearance_frequency.py`
- `E_001/e1_standalone_contract.py`
- `E_001/e1_training_view.py`
- `E_001/multigame_e1.py`
- `E_001_Historical_Appearance_Frequency.py`

## Shared helpers used

- `_common/canonical_encoding.py` (revision 1)
- `_common/game_profiles.py` (revision 1)
- `_common/game_draws_reader.py` (revision 1)
- `_common/experiment_runtime_status_and_resources.py` (revision 1)
- `_common/contract_dispatch.py` (revision 1)

## Replay

These files are kept for reading. Nothing imports or runs them: no project code or test refers to a path or module inside `archive/` (a static and a runtime check enforce this), and normal runners never dispatch an archived revision (E2R-R56). `archive/` has no `__init__.py` files, but that alone would not stop an import (Python 3 namespace packages). Re-running revision 1 would be a separate, owner-approved act, attempted only if the preserved code, configuration and dependencies are sufficient; exact historical replay is not promised. The shared helpers listed above are revision 1 of the shared code; none was revised by the package that archived this revision.
