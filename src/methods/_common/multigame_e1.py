"""Generic E_1 scoring engine, candidate. No IO or execution on import.

Kept separate from accepted e1_historical_appearance_frequency.
Legacy Powerball SHA/rank regression is compulsory before any migration.
"""
from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence

from _common.e1_historical_appearance_frequency import (
    _length32_tuple, canonical_bytes, DOMAIN, METHOD_ID, VARIANT_ID, TIE_VERSION,
)
from _common.game_profiles import GameProfile


def _digest(view_sha256: str, target: int, barrel_id: str, label: int) -> str:
    if re.fullmatch(r'[0-9a-f]{64}', view_sha256, re.ASCII) is None:
        raise ValueError('invalid permitted-view digest')
    if type(target) is not int or type(label) is not int or target <= 0 or label <= 0:
        raise ValueError('invalid tie-key integers')
    values = (DOMAIN, view_sha256, str(target), METHOD_ID, VARIANT_ID,
              barrel_id, TIE_VERSION, str(label))
    return hashlib.sha256(_length32_tuple(values)).hexdigest()


def forecast(profile: GameProfile, records: Sequence[Mapping], digest: str, target: int,
             *, data_kind: str) -> dict:
    if data_kind != 'SYNTHETIC_CONTRACT_TEST':
        # This new multi-game science runner remains OFF until later review.
        raise ValueError('multi-game E_1 real execution not authorised')
    if not profile.historical_development_target_allowed(target):
        raise ValueError('historical target outside development boundary')
    if len(records) != target - profile.first_draw:
        raise ValueError('incomplete training view')
    barrel_outputs = {}
    for desc in profile.barrels:
        counts = {label: 0 for label in range(desc.low, desc.high + 1)}
        for i, record in enumerate(records):
            if record.get('draw') != profile.first_draw + i:
                raise ValueError('non-consecutive N-1 training view')
            nums = record.get(desc.barrel_id)
            if (not isinstance(nums, (tuple,list)) or len(nums) != desc.selected or
                    len(set(nums)) != len(nums) or
                    any(type(x) is not int or x not in counts for x in nums)):
                raise ValueError('invalid barrel record')
            for value in nums:
                counts[value] += 1
        ranking = sorted(counts, key=lambda n:(-counts[n], _digest(digest,target,desc.barrel_id,n),n))
        barrel_outputs[desc.barrel_id] = {
            'scores': {str(k):v for k,v in counts.items()},
            'ranking': ranking,
            'top': ranking[:desc.selected],
            'worst': list(reversed(ranking))[:desc.selected],
        }
    return {
        'schema': 'MULTIGAME_E1_FORECAST_V1_REVIEW',
        'game_id': profile.game_id, 'profile_version': profile.version,
        'era_id': profile.era_id, 'draw_number': target,
        'draw_key': profile.draw_key(target), 'last_training_draw': target - 1,
        'method_id': METHOD_ID, 'variant_id': VARIANT_ID,
        'data_kind': data_kind, 'training_view_sha256': digest,
        'ranking_tie_readout_version': TIE_VERSION, 'barrels': barrel_outputs,
    }
