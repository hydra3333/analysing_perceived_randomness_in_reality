"""Package 2 candidate: coordinator-owned, game-qualified launch specification.

PURE PREFLIGHT ONLY: no process creation, no network, no filesystem writes.
A valid LaunchSpec is NOT authorisation for a scientific coordinator run.
The ratified POC's --poc-only command parser and both safety switches remain off.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

_SAFE_GROUP = re.compile(r'[A-Za-z0-9_-]{1,85}\Z', re.ASCII)
_SAFE_RUN = re.compile(r'mg-[a-z0-9][a-z0-9_-]{7,95}\Z', re.ASCII)
_ALLOWED = {'E_1': 'POC_MultiGame_Synthetic_Worker.py'}


@dataclass(frozen=True)
class LaunchSpec:
    group_id: str
    worker_sequence: int
    run_id: str
    game_id: str
    draw_number: int
    method_id: str
    variant_id: str
    profile_version: str
    mode: str
    script_name: str
    run_dir: Path
    # This does not include a user-supplied source path. Scientific sources
    # require a separately reviewed source-view binding contract.
    command_arguments: tuple[str, ...]

    def identity(self) -> dict:
        return {'group_id': self.group_id, 'worker_sequence': self.worker_sequence,
                'run_id': self.run_id, 'game_id': self.game_id,
                'draw_number': self.draw_number, 'method_id': self.method_id,
                'variant_id': self.variant_id}


def build_synthetic_launch_spec(*, group_id: str, worker_sequence: int,
                                run_id: str, game_id: str, draw_number: int,
                                method_id: str, variant_id: str,
                                synthetic_root: Path) -> LaunchSpec:
    """Trusted coordinator input only; no ambient data, paths or modes from CLI.

    Output argv contains only safe ASCII values, never file paths or shell chars.
    Every run dir is under a deliberately selected game-qualified synthetic root.
    A real loader is impossible through this interface.
    """
    from _common.game_profiles import get_profile
    from _common.multigame_method_registry import method_status, SUPPORTED
    from _common.multigame_result_registry import require_synthetic_variant
    if (type(group_id) is not str or _SAFE_GROUP.fullmatch(group_id) is None or
            type(worker_sequence) is not int or not 1 <= worker_sequence <= 6 or
            type(run_id) is not str or _SAFE_RUN.fullmatch(run_id) is None or
            type(draw_number) is not int or type(method_id) is not str or
            type(variant_id) is not str or not re.fullmatch(r'[A-Z0-9_]{3,96}', variant_id, re.ASCII) or
            not isinstance(synthetic_root, Path) or synthetic_root.is_symlink()):
        raise ValueError('invalid synthetic coordinator launch specification')
    profile = get_profile(game_id)
    if not profile.historical_development_target_allowed(draw_number):
        raise ValueError('synthetic historical-development boundary denied')
    if method_status(game_id, method_id) != SUPPORTED or method_id not in _ALLOWED:
        raise ValueError('method is not implemented/supported for coordinated synthetic run')
    require_synthetic_variant(game_id, method_id, variant_id)
    if synthetic_root.name != 'multigame_synthetic_runs':
        raise ValueError('run root must be explicitly game-separated synthetic namespace')
    resolved = synthetic_root.resolve(strict=False)
    if any(part.casefold() in ('source_data', 'results', 'p3_standalone_runs')
           for part in resolved.parts):
        raise ValueError('synthetic root overlaps real data/results namespace')
    run_dir = synthetic_root / game_id / run_id
    argv = (_ALLOWED[method_id], '--synthetic-contract-probe',
            '--game=' + game_id, '--target=' + str(draw_number),
            '--run-id=' + run_id, '--group-id=' + group_id,
            '--worker-sequence=' + str(worker_sequence), '--variant=' + variant_id)
    return LaunchSpec(group_id, worker_sequence, run_id, game_id, draw_number,
                      method_id, variant_id, profile.version, 'SYNTHETIC_CONTRACT_TEST',
                      _ALLOWED[method_id], run_dir, argv)
