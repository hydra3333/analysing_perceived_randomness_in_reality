"""Review candidate: target-bounded E_1 U-view CSV loader. No method execution.

The ONLY input from source content permitted to model E_1 is draw number,
set of seven main labels (sorted), and Powerball. All other fields are validated
where explicitly permitted but never enter the model-content identity.

Original ten-draw historical holdout stays sealed for development. No FINAL mode.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from E_001.e1_historical_appearance_frequency import canonical_bytes

FIRST_DRAW = 1144
HOLDOUT_FIRST = 1578
HOLDOUT_LAST = 1587
HISTORICAL_LAST_TARGET = HOLDOUT_FIRST - 1  # 1577; target itself must not be holdout.
FIRST_DATE = date(2018, 4, 19)
U_COLUMNS = ('Draw_Number', 'Date', 'Ball_1', 'Ball_2', 'Ball_3', 'Ball_4',
             'Ball_5', 'Ball_6', 'Ball_7', 'Powerball')
REAL_U_VIEW_SCHEMA = 'E1_REAL_U_TRAINING_VIEW_V1'
SYNTH_U_VIEW_SCHEMA = 'E1_SYNTHETIC_CSV_U_TRAINING_VIEW_V1'
SAFE_NAME = re.compile(r'australian_powerball_history_[0-9]{8}\.csv\Z', re.ASCII)


def _int_field(raw: str, lo: int, hi: int, what: str) -> int:
    if not re.fullmatch(r'0|[1-9][0-9]*', raw, re.ASCII):
        raise ValueError(f'{what}: noncanonical positive decimal integer')
    n = int(raw)
    if not lo <= n <= hi:
        raise ValueError(f'{what}: out of range')
    return n


def validate_target(target: int) -> None:
    if type(target) is not int:
        raise ValueError('target must be an integer')
    if not FIRST_DRAW + 1 <= target <= HISTORICAL_LAST_TARGET:
        raise ValueError('historical target outside pre-holdout development range 1145..1577')


def _prefix_from_csv(path: Path, target: int) -> list[dict[str, Any]]:
    """Read EXACTLY target-1144 records. Never read row N or later.

    This deliberate prefix-only mechanism is an anti-leakage *model adapter*;
    comprehensive whole-file/audit validation is a separate, gated workflow.
    No opening secondary drawn-order CSV or computing entire-file digests.
    """
    validate_target(target)
    records: list[dict[str, Any]] = []
    # newline='' follows csv's documented text input behaviour.
    with path.open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.reader(handle, strict=True)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError('missing CSV header') from exc
        if header != list(U_COLUMNS):
            raise ValueError('unexpected U-view CSV columns; drawn-order input forbidden')
        for expected in range(FIRST_DRAW, target):
            try:
                row = next(reader)
            except StopIteration as exc:
                raise ValueError(f'missing required draw {expected}') from exc
            if len(row) != len(U_COLUMNS):
                raise ValueError(f'draw {expected}: wrong field count')
            number = _int_field(row[0], FIRST_DRAW, target-1, 'Draw_Number')
            if number != expected:
                raise ValueError(f'nonconsecutive/duplicate draw: expected {expected}, received {number}')
            try:
                local_date = date.fromisoformat(row[1])
            except ValueError as exc:
                raise ValueError(f'draw {expected}: invalid date') from exc
            if local_date.isoformat() != row[1] or local_date != FIRST_DATE + timedelta(days=7*(expected-FIRST_DRAW)):
                raise ValueError(f'draw {expected}: date not current-format weekly chronology')
            main = [_int_field(v, 1, 35, 'Ball_n') for v in row[2:9]]
            if len(set(main)) != 7:
                raise ValueError(f'draw {expected}: duplicate main labels')
            pb = _int_field(row[9], 1, 20, 'Powerball')
            records.append({'draw': number, 'main': sorted(main), 'powerball': pb})
        # Deliberately NO peek, file stat, source-byte hash, or next(reader).
    return records


def load_permitted_u_view(source: Path, target: int, *, source_kind: str,
                          trusted_source_dir: Path | None = None) -> tuple[list[dict], str]:
    if source_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT'):
        raise ValueError('unrecognised source kind: refuse')
    if not isinstance(source, Path):
        raise ValueError('source must be an explicit Path')
    if source_kind == 'REAL_HISTORICAL_DEVELOPMENT':
        if trusted_source_dir is None:
            raise ValueError('real source needs trusted source directory')
        if source.parent.resolve(strict=True) != trusted_source_dir.resolve(strict=True):
            raise ValueError('real source must be in the trusted source_data directory')
        if not SAFE_NAME.fullmatch(source.name):
            raise ValueError('real source must have approved unordered-file name')
        if source.is_symlink() or not source.is_file():
            raise ValueError('real source must be a regular nonsymlink file')
        schema = REAL_U_VIEW_SCHEMA
    else:
        # Calling code must ensure synthetic inputs are not filed as real data.
        schema = SYNTH_U_VIEW_SCHEMA
    records = _prefix_from_csv(source, target)
    payload = {'schema': schema, 'data_kind': source_kind, 'records': records}
    return records, hashlib.sha256(canonical_bytes(payload)).hexdigest()


def build_e1_forecast(records: list[dict], digest: str, target: int, *, source_kind: str) -> dict:
    # Delayed import to keep STARTED publication ahead of heavy future dependencies.
    from E_001.e1_historical_appearance_frequency import rank_counts, METHOD_ID, VARIANT_ID, TIE_VERSION
    if source_kind not in ('REAL_HISTORICAL_DEVELOPMENT', 'SYNTHETIC_CONTRACT_TEST'):
        raise ValueError('source kind not allowed')
    if len(records) != target-FIRST_DRAW or records[0]['draw'] != FIRST_DRAW or records[-1]['draw'] != target-1:
        raise ValueError('invalid permitted training prefix')
    scores_main = {i: 0 for i in range(1,36)}
    scores_pb = {i: 0 for i in range(1,21)}
    for record in records:
        for label in record['main']:
            scores_main[label] += 1
        scores_pb[record['powerball']] += 1
    rm = rank_counts(scores_main, digest, target, 'MAIN')
    rp = rank_counts(scores_pb, digest, target, 'POWERBALL')
    return {'schema': 'E1_HISTORICAL_DEVELOPMENT_FORECAST_V0_1_REVIEW',
            'data_kind': source_kind, 'method_id': METHOD_ID, 'variant_id': VARIANT_ID,
            'fit_sampling_model_version': 'RAW_APPEARANCE_COUNTS_V1',
            'ranking_tie_readout_version': TIE_VERSION,
            'target_draw': target, 'last_training_draw': target-1,
            'training_view_sha256': digest,
            'MAIN': {'scores': {str(k): v for k, v in scores_main.items()}, 'ranking': rm,
                     'top': rm[:7], 'worst': list(reversed(rm))[:7]},
            'POWERBALL': {'scores': {str(k): v for k, v in scores_pb.items()}, 'ranking': rp,
                          'top': rp[0], 'worst': rp[-1]}}
