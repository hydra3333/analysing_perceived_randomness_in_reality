"""Package 2 synthetic-only, barrel-aware scoring behind the result firewall.

The trusted consumer is invoked BEFORE the outcome-provider callback. No real
results, draw N lookup or held-out data are accessible from this module.
This is NOT a real scoring/walk-forward implementation and has no FINAL mode.
"""
from __future__ import annotations

import math
from collections.abc import Callable
from pathlib import Path

from _common.game_profiles import GameProfile
from _common.multigame_standalone_contract import verify_synthetic_and_consume


def _native_mid_ranks(scores: dict, *, low: int, high: int) -> dict[int, float]:
    if (type(scores) is not dict or set(scores) != {str(n) for n in range(low, high+1)}):
        raise ValueError('native-score labels incomplete')
    values: dict[int, int | float] = {}
    for label in range(low, high+1):
        val = scores[str(label)]
        if type(val) not in (int, float) or not math.isfinite(val):
            raise ValueError('invalid native score')
        values[label] = val
    by_value = sorted(values, key=lambda x: -values[x])
    ranks: dict[int,float] = {}
    i=0
    while i < len(by_value):
        j=i+1
        while j<len(by_value) and values[by_value[j]]==values[by_value[i]]:
            j+=1
        rank=(i+1+j)/2  # arithmetic mean of one-based ranks [i+1, j]
        for lab in by_value[i:j]:
            ranks[lab]=rank
        i=j
    return ranks


def score_verified_synthetic(*, run_dir: Path, run_id: str, profile: GameProfile,
                             method_id: str, variant_id: str, target: int,
                             global_orphan_marker: Path,
                             outcome_loader: Callable[[], dict]) -> dict:
    """Validate frozen success artifact first; only then retrieve the outcome.

    An outcome loader is a test fixture provider. Never pass a real file/DB
    loader here: this routine is hard-limited to SYNTHETIC_CONTRACT_TEST.
    """
    result = verify_synthetic_and_consume(run_dir,run_id=run_id,profile=profile,
        method_id=method_id,variant_id=variant_id,target=target,
        global_orphan_marker=global_orphan_marker)
    if result.get('data_kind') != 'SYNTHETIC_CONTRACT_TEST':
        raise ValueError('real scoring disabled')
    if not callable(outcome_loader):
        raise ValueError('outcome provider required')
    outcome = outcome_loader()  # This MUST be after the consumer firewall.
    if (type(outcome) is not dict or outcome.get('kind') != 'SYNTHETIC_CONTRACT_TEST' or
            outcome.get('game_id') != profile.game_id or
            outcome.get('draw_number') != target or
            outcome.get('draw_key') != profile.draw_key(target) or
            outcome.get('profile_version') != profile.version or
            type(outcome.get('barrels')) is not dict or
            set(outcome['barrels']) != {b.barrel_id for b in profile.barrels}):
        raise ValueError('synthetic outcome identity mismatch')
    if type(result.get('barrels')) is not dict or set(result['barrels']) != set(outcome['barrels']):
        raise ValueError('frozen barrel identity mismatch')
    rows = {}
    for barrel in profile.barrels:
        frozen = result['barrels'][barrel.barrel_id]
        if type(frozen) is not dict:
            raise ValueError('invalid frozen barrel')
        ranking=frozen.get('ranking'); top=frozen.get('top'); worst=frozen.get('worst')
        legal=set(range(barrel.low,barrel.high+1))
        if (type(ranking) is not list or len(ranking)!=len(legal) or
                any(type(x) is not int for x in ranking) or set(ranking)!=legal or
                type(top) is not list or type(worst) is not list or
                top!=ranking[:barrel.selected] or
                worst!=list(reversed(ranking))[:barrel.selected]):
            raise ValueError('malformed frozen ranking')
        actual=outcome['barrels'][barrel.barrel_id]
        if (type(actual) not in (tuple,list) or len(actual)!=barrel.selected or
                any(type(n) is not int or n not in legal for n in actual) or
                len(set(actual))!=barrel.selected):
            raise ValueError('invalid synthetic outcome barrel')
        native = _native_mid_ranks(frozen.get('scores'),low=barrel.low,high=barrel.high)
        # Ensure the digest tie-order is only resolving equal scores.
        if any(frozen['scores'][str(ranking[i])] < frozen['scores'][str(ranking[i+1])]
               for i in range(len(ranking)-1)):
            raise ValueError('ranking inconsistent with native scores')
        outcome_set=set(actual)
        rows[barrel.barrel_id]={
            'top_matches':len(outcome_set.intersection(top)),
            'worst_matches':len(outcome_set.intersection(worst)),
            'mean_native_mid_rank':sum(native[n] for n in actual)/barrel.selected,
            'reference_top_matches':barrel.selected**2/len(legal),
            'reference_mean_rank':(len(legal)+1)/2,
        }
    return {
        'schema':'MULTIGAME_SYNTHETIC_SCORE_V1_REVIEW',
        'kind':'SYNTHETIC_CONTRACT_TEST',
        'game_id':profile.game_id,'profile_version':profile.version,
        'draw_number':target,'draw_key':profile.draw_key(target),
        'method_id':method_id,'variant_id':variant_id,'run_id':run_id,
        'source_training_view_sha256':result['training_view_sha256'],
        'barrels':rows,
    }
