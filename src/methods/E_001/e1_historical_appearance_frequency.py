"""E_1 synthetic-only lead implementation prototype, v0.3 (NOT a production runner).

No CLI, source-file reads, real-data training, outcome access, or process signals.
Production status publication and immutable forecast storage await reviewed contracts.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence

from _common.canonical_encoding import canonical_bytes, length32_tuple as _length32_tuple

METHOD_ID = 'E_1'
VARIANT_ID = 'FULL_HISTORY_RAW_COUNTS_V1'
TIE_VERSION = 'TIE_SHA256_V1'
DOMAIN = 'PREDICTIVE_RANDOMNESS/TIE_SHA256_V1'


def _integer(x: object, what: str) -> int:
    if type(x) is not int:  # Reject bool as int.
        raise ValueError(f'{what} must be an integer')
    return x


def training_prefix(rows: Sequence[Mapping[str, object]], target: int) -> list[dict]:
    """Build target-limited view from validated prefix; reject gaps and duplicate IDs.

    This is a synthetic-only TEST adapter. Real source validation, mode gating,
    and holdout isolation belong to a separately reviewed production loader.
    """
    target = _integer(target, 'target')
    if target < 1145:
        raise ValueError('need at least one preceding draw')
    all_rows: list[dict] = []
    seen: set[int] = set()
    for obj in rows:
        n = _integer(obj['draw'], 'draw')
        # Enforce cutoff BEFORE inspecting any future payloads. T-05 may poison
        # draw N and later with malformed labels; they must not affect fit.
        if n >= target:
            continue
        if n in seen:
            raise ValueError('duplicate draw')
        seen.add(n)
        if n < 1144:
            raise ValueError('pre-current-format draw')
        main = obj['main']
        if not isinstance(main, (list, tuple)) or len(main) != 7:
            raise ValueError('main must contain seven labels')
        labels = [_integer(v, 'main label') for v in main]
        if len(set(labels)) != 7 or not all(1 <= v <= 35 for v in labels):
            raise ValueError('illegal main combination')
        pb = _integer(obj['powerball'], 'powerball')
        if not 1 <= pb <= 20:
            raise ValueError('illegal powerball')
        all_rows.append({'draw': n, 'main': sorted(labels), 'powerball': pb})
    all_rows.sort(key=lambda r: r['draw'])
    if not all_rows or all_rows[0]['draw'] != 1144:
        raise ValueError('synthetic fixture must start at draw 1144')
    if [r['draw'] for r in all_rows] != list(range(1144, all_rows[-1]['draw'] + 1)):
        raise ValueError('draw chronology must be consecutive')
    selected = all_rows
    if not selected or selected[-1]['draw'] != target - 1:
        raise ValueError('missing target-1')
    return selected


def training_sha256(prefix: Sequence[Mapping[str, object]]) -> str:
    # Synthetic-only provenance marker prevents accidental real/synthetic mixing.
    identity = {'schema': 'E1_SYNTHETIC_TRAINING_VIEW_V0_1',
                'source_kind': 'SYNTHETIC_TEST_ONLY', 'records': prefix}
    return hashlib.sha256(canonical_bytes(identity)).hexdigest()


def tie_digest(training_digest: str, target: int, barrel: str, label: int) -> str:
    if barrel not in ('MAIN', 'POWERBALL'):
        raise ValueError('unknown barrel')
    if type(training_digest) is not str or re.fullmatch(r'[0-9a-f]{64}', training_digest) is None:
        raise ValueError('training digest must be 64 lowercase hexadecimal characters')
    target = _integer(target, 'target')
    label = _integer(label, 'label')
    if target < 1145:
        raise ValueError('target must be >=1145')
    if not (1 <= label <= (35 if barrel == 'MAIN' else 20)):
        raise ValueError('label is outside barrel')
    # All integer tuple fields are canonical, signless base-10 ASCII.
    # The exact tuple is fixed by the owner-ratified D2 decision.
    return hashlib.sha256(_length32_tuple((
        DOMAIN, training_digest, str(target), METHOD_ID, VARIANT_ID, barrel,
        TIE_VERSION, str(label)))).hexdigest()


def rank_counts(counts: Mapping[int, int], training_digest: str,
                target: int, barrel: str) -> list[int]:
    n = 35 if barrel == 'MAIN' else 20 if barrel == 'POWERBALL' else None
    if n is None or set(counts) != set(range(1, n + 1)):
        raise ValueError('full barrel required')
    if any(type(v) is not int or v < 0 for v in counts.values()):
        raise ValueError('counts must be nonnegative integers')
    # Digest tie-order is a readout operation; it has no role in score fitting.
    return sorted(counts, key=lambda label: (-counts[label],
                  tie_digest(training_digest, target, barrel, label), label))


def candidate_forecast(rows: Sequence[Mapping[str, object]], target: int, *,
                       source_kind: str = 'SYNTHETIC_TEST_ONLY') -> dict:
    if source_kind != 'SYNTHETIC_TEST_ONLY':
        raise ValueError('E1 synthetic prototype refuses real dataset execution')
    prefix = training_prefix(rows, target)
    digest = training_sha256(prefix)
    scores_main = {i: 0 for i in range(1, 36)}
    scores_pb = {i: 0 for i in range(1, 21)}
    for record in prefix:
        for label in record['main']:
            scores_main[label] += 1
        scores_pb[record['powerball']] += 1
    rank_main = rank_counts(scores_main, digest, target, 'MAIN')
    rank_pb = rank_counts(scores_pb, digest, target, 'POWERBALL')
    result = {
        'schema': 'E1_SYNTHETIC_FORECAST_V0_1_NOT_FINAL',
        'data_kind': 'SYNTHETIC_TEST_ONLY',
        'method_id': METHOD_ID, 'variant_id': VARIANT_ID,
        'fit_sampling_model_version': 'RAW_APPEARANCE_COUNTS_V1',
        'ranking_tie_readout_version': TIE_VERSION,
        'target_draw': target, 'last_training_draw': target - 1,
        'training_view_sha256': digest,
        'MAIN': {'scores': scores_main, 'ranking': rank_main,
                 'top': rank_main[:7], 'worst': list(reversed(rank_main))[:7]},
        'POWERBALL': {'scores': scores_pb, 'ranking': rank_pb,
                      'top': rank_pb[0], 'worst': rank_pb[-1]},
    }
    return result
