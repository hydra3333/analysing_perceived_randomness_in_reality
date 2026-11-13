# E_1 revision 2 (archived)

- **Method:** E_1, Historical Appearance Frequency, revision 2; variants: `FULL_HISTORY_RAW_COUNTS_V1`; games: POWERBALL, OZLOTTO.
- **Prepared:** 2026-11-11 (the date this archive was prepared by its package).
- **Retired:** when the owner installs that package. The installation date and commit are recorded in the ratification register, not here.
- **Superseded by:** revision 3.
- **Why retired:** revision 2's multi-game function (`E_001/multigame_e1.py`) refused, in its own code, every run mode other than SYNTHETIC_CONTRACT_TEST and REAL_DEVELOPMENT and every target beyond the development prefix, so E_1 could take part in neither Mode H nor the weekly session; revision 3 takes the view data kind instead of a run mode and leaves the target ceiling to the shared target and mode gates, with the same counting, ranking and tie order (MHUP-1 design v0.1r5 section 2; owner decision MHUP-Q10, 3 November 2026). The legacy runner's release check names revision 3 at the same time. Revision 3 reuses all seven paths: five files unchanged, and `E_001/multigame_e1.py` and `E_001_Historical_Appearance_Frequency.py` changed.

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

These files are kept for reading. Nothing imports or runs them: no project code or test refers to a path or module inside `archive/` (a static and a runtime check enforce this), and normal runners never dispatch an archived revision (E2R-R56). `archive/` has no `__init__.py` files, but that alone would not stop an import (Python 3 namespace packages). Re-running revision 2 would be a separate, owner-approved act, attempted only if the preserved code, configuration and dependencies are sufficient; exact historical replay is not promised. The shared helpers listed above are revision 1 of the shared code as revision 2 used them; `_common/game_draws_reader.py` and `_common/contract_dispatch.py` are revised by the package that archives this revision (MHUP-A), and their revision-1 bytes are in the Git history of the commit that installs it.
