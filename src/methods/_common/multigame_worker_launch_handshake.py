"""Method-side synthetic launch argument/namespace check; no coordinator privilege.

A worker may check its own requested identity, but cannot certify ancestry,
process exit, a group manifest, or create a coordinator exit receipt.
"""
from __future__ import annotations
from pathlib import Path
import re

from _common.game_profiles import get_profile
from _common.multigame_method_registry import method_status, SUPPORTED
from _common.multigame_result_registry import require_synthetic_variant


def verify_synthetic_worker_request(*, game_id: str, draw_number: int,
                                    method_id: str, variant_id: str,
                                    run_id: str, group_id: str,
                                    worker_sequence: int, root: Path) -> tuple[dict, Path, str]:
    if (type(group_id) is not str or not re.fullmatch(r'[A-Za-z0-9_-]{1,85}', group_id, re.ASCII) or
            type(worker_sequence) is not int or not 1 <= worker_sequence <= 6 or
            type(run_id) is not str or not re.fullmatch(r'mg-[a-z0-9][a-z0-9_-]{7,95}', run_id, re.ASCII) or
            type(variant_id) is not str or not re.fullmatch(r'[A-Z0-9_]{3,96}', variant_id, re.ASCII) or
            not isinstance(root, Path) or root.name != 'multigame_synthetic_runs' or root.is_symlink() or
            any(x.casefold() in ('source_data','results','p3_standalone_runs') for x in root.resolve().parts)):
        raise ValueError('invalid synthetic worker launch handshake')
    profile=get_profile(game_id)
    if (type(draw_number) is not int or not profile.historical_development_target_allowed(draw_number) or
            method_id != 'E_1' or method_status(game_id,method_id) != SUPPORTED):
        raise ValueError('unsupported method or historical target')
    require_synthetic_variant(game_id, method_id, variant_id)
    identity={'group_id':group_id,'worker_sequence':worker_sequence,'run_id':run_id,
              'game_id':game_id,'draw_number':draw_number,
              'method_id':method_id,'variant_id':variant_id}
    return identity, root/game_id/run_id, profile.version
