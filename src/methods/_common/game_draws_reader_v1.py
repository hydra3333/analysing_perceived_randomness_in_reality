"""Package 2 v0.11: ledger-pinned, prefix-only development observation reader.

Scientific caller receives DrawView only. The accepted owner-maintained INIT master
and ledger are the structural authority; this module *hashes* all source bytes
for provenance but parses only rows strictly below target N. No network,
scoring, process management or master mutation. This is REVIEW code, not an
approved scientific-run entry point.
"""
from __future__ import annotations

import csv
from datetime import date
import hashlib
import io
import json
import os
from pathlib import Path
import re
from types import MappingProxyType

import numpy as np
from _common.game_profiles_v1 import get_profile

_DIGIT = re.compile(rb'(0|[1-9][0-9]*)\Z', re.ASCII)
_METHOD = re.compile(r'E_[1-9][0-9]*\Z', re.ASCII)
_VARIANT = re.compile(r'[A-Z0-9_]{3,96}\Z', re.ASCII)
_SHA = re.compile(r'[a-f0-9]{64}\Z', re.ASCII)
VIEW_KINDS = frozenset(('UNORDERED_SET', 'OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC'))
_REAL = 'REAL_HISTORICAL_DEVELOPMENT'
_ORDER_STATUS = 'OPERATOR_DRAWN_ORDER_ASSUMED_OWNER_DECISION'
_E1_VARIANT = 'FULL_HISTORY_RAW_COUNTS_V1'
_PIN_SCHEMA = 'DEVELOPMENT_MASTER_PIN_V1_REVIEW'


def header_for(game_id: str) -> tuple[str, ...]:
    get_profile(game_id)
    common = ('Draw_Number', 'Date') + tuple(f'Drawn_{i}' for i in range(1, 8))
    return common + (('Powerball',) if game_id == 'POWERBALL' else ('Supp_1', 'Supp_2', 'Supp_3'))


def _owned(values, dtype):
    """Every array owns a distinct *bytes* prefix; .base is exactly bytes.

    Unlike `np.frombuffer(...).reshape(...)`, ndarray(...,buffer=bytes)
    preserves `.base is bytes` even for the 2-D main-ball representation.
    """
    arr = np.asarray(values, dtype=dtype)
    raw = arr.tobytes(order='C')
    view = np.ndarray(shape=arr.shape, dtype=arr.dtype, buffer=raw, order='C')
    if type(view.base) is not bytes or view.flags.writeable or len(raw) != view.nbytes:
        raise RuntimeError('array prefix ownership invariant failed')
    return view


class DrawView:
    """Frozen metadata and independently byte-owned read-only prefix arrays.

    No path, master table, source bytes or supplementary outcomes are retained.
    The only prediction inputs are the published representations named here.
    """
    __slots__ = ('game_id', 'method_id', 'variant_id', 'target', 'kind',
                 'draw_number', 'draw_date', 'main', 'powerball', 'drawn_main',
                 'order_verification_status', 'order_evidence',
                 '_sealed')

    def __init__(self, *, game_id, method_id, variant_id, target, kind, numbers,
                 dates, main, powerball=None, drawn_main=None, order_status,
                 order_evidence):
        object.__setattr__(self, '_sealed', False)
        self.game_id, self.method_id, self.variant_id = game_id, method_id, variant_id
        self.target, self.kind = target, kind
        self.draw_number = _owned(numbers, np.int64)
        self.draw_date = _owned(dates, 'datetime64[D]') if dates is not None else None
        self.main = _owned(main, np.int64)
        self.powerball = _owned(powerball, np.int64) if powerball is not None else None
        self.drawn_main = _owned(drawn_main, np.int64) if drawn_main is not None else None
        self.order_verification_status = order_status
        self.order_evidence = (MappingProxyType(dict(order_evidence))
                               if order_evidence is not None else None)
        if (self.main.shape != (len(self.draw_number), 7) or
                (self.powerball is not None and self.powerball.shape != self.draw_number.shape) or
                (self.drawn_main is not None and self.drawn_main.shape != self.main.shape) or
                (self.draw_date is not None and self.draw_date.shape != self.draw_number.shape)):
            raise ValueError('inconsistent prefix-array shapes')
        object.__setattr__(self, '_sealed', True)

    def __setattr__(self, key, value):
        if getattr(self, '_sealed', False):
            raise AttributeError('DrawView fields are frozen')
        object.__setattr__(self, key, value)

    def simple_rows(self) -> list[dict]:
        """Plain Python integers; neither arrays nor table/paths escape."""
        rows = []
        for i, number in enumerate(self.draw_number):
            row = {'draw': int(number), 'main': [int(x) for x in self.main[i]]}
            if self.kind == 'PAIRED_DIAGNOSTIC':
                row['drawn_main'] = [int(x) for x in self.drawn_main[i]]
            if self.powerball is not None:
                row['powerball'] = int(self.powerball[i])
            if self.draw_date is not None:
                row['date'] = str(self.draw_date[i])
            rows.append(row)
        return rows

    def e1_view_digest(self, *, data_kind: str = _REAL) -> str:
        """Legacy E1 date-free digest is immutable; new schemas bind dates."""
        from _common.e1_historical_appearance_frequency_v0_3 import canonical_bytes
        rows = self.simple_rows()
        legacy = (self.game_id == 'POWERBALL' and self.method_id == 'E_1' and
                  self.variant_id == _E1_VARIANT and self.kind == 'UNORDERED_SET' and
                  self.draw_date is None)
        if legacy:
            payload = {'schema': 'E1_REAL_U_TRAINING_VIEW_V1',
                       'data_kind': data_kind, 'records': rows}
        else:
            p = get_profile(self.game_id)
            order = self.kind != 'UNORDERED_SET'
            payload = {
                'schema': f'{p.game_id}_{p.era_id}_{p.version}_{self.kind}_VIEW_' +
                          ('DATES_V2' if self.draw_date is not None else 'V1'),
                'data_kind': data_kind, 'game_id': p.game_id,
                'era_id': p.era_id, 'profile_version': p.version,
                'method_id': self.method_id, 'variant_id': self.variant_id,
                'target': self.target,
                'observation_view': self.kind, 'includes_dates': self.draw_date is not None,
                'order_assumption': self.order_verification_status if order else None,
                # Whole-master SHA/ledger/INIT identity are orchestration-only:
                # neither stored in DrawView nor included in this digest.
                'order_evidence_record': (self.order_evidence['record'] if order else None),
                'records': rows,
            }
        return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def _trusted_file_bytes(path: Path) -> bytes:
    """Refuse symbolic/hard links; read the opened regular file, not a symlink."""
    if not isinstance(path, Path) or path.is_symlink():
        raise ValueError('unsafe source path (symbolic link)')
    flags = os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise ValueError('missing or unsafe source file') from exc
    try:
        import stat
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise ValueError('source must be a regular non-hardlinked file')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            raw = stream.read()
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError('source changed while pinned bytes were read')
        return raw
    finally:
        os.close(fd)


def _parse_prefix(raw: bytes, game_id: str, target: int, *, include_dates: bool):
    """Read no data columns of N or later. `raw` suffix is never decoded.

    Master completeness, dates and supplementary structure were already
    certified on creation by the owner-managed master tool. This routine
    rechecks only the rows needed by the particular N-1 prediction view.
    """
    profile = get_profile(game_id)
    length = target - profile.first_draw
    stream = io.BytesIO(raw)
    head = stream.readline()
    if head.rstrip(b'\r\n').decode('ascii') != ','.join(header_for(game_id)):
        raise ValueError('wrong pinned master header')
    numbers, dates, drawn, sorted_main, balls = [], [], [], [], []
    for i in range(length):
        line = stream.readline()
        first = line.split(b',', 1)[0]  # RAW FIRST FIELD ONLY, before CSV decode.
        if not _DIGIT.fullmatch(first) or int(first) != profile.first_draw + i:
            raise ValueError('missing or nonconsecutive prefix draw')
        row = next(csv.reader([line.decode('utf-8', errors='strict')], strict=True))
        if len(row) != len(header_for(game_id)):
            raise ValueError('malformed eligible prefix row')
        high = 35 if game_id == 'POWERBALL' else 47
        if any(not x.isascii() or not x.isdecimal() or x.startswith('0') for x in row[2:9]):
            raise ValueError('invalid prefix main number')
        main = [int(x) for x in row[2:9]]
        if not all(1 <= x <= high for x in main) or len(set(main)) != 7:
            raise ValueError('invalid eligible main set')
        if game_id == 'POWERBALL':
            if not row[9].isascii() or not row[9].isdecimal() or row[9].startswith('0'):
                raise ValueError('invalid prefix Powerball')
            pb = int(row[9])
            if not 1 <= pb <= 20:
                raise ValueError('invalid prefix Powerball')
            balls.append(pb)
        # Oz supplementary columns: already audited at master INIT; do NOT
        # parse, convert, store or expose them in predictor observation views.
        if include_dates:
            try:
                d = date.fromisoformat(row[1])
            except ValueError as exc:
                raise ValueError('invalid opted-in prefix date') from exc
            if d.isoformat() != row[1] or d != profile.derived_date(profile.first_draw + i):
                raise ValueError('date-dependent method halted: date discrepancy')
            dates.append(d.isoformat())
        numbers.append(profile.first_draw + i)
        drawn.append(main)
        sorted_main.append(sorted(main))
    return numbers, (dates if include_dates else None), drawn, sorted_main, (balls if game_id == 'POWERBALL' else None)


def load_pinned_draw_view(*, repo_root: Path, run_manifest: dict) -> DrawView:
    """Orchestration-only entry point, never imported by a method implementation.

    Manifest pins the current Phase-1 version-1 INIT master. No caller may
    supply a source path, alternative master, or raw future/outcome records.
    """
    if not isinstance(repo_root, Path) or type(run_manifest) is not dict:
        raise ValueError('invalid source root or manifest')
    required = {'schema', 'game_id', 'method_id', 'variant_id', 'draw_number',
                'view_kind', 'include_dates', 'master_file', 'ledger_version', 'master_sha256'}
    if set(run_manifest) != required or run_manifest['schema'] != _PIN_SCHEMA:
        raise ValueError('unsupported reviewed run manifest')
    game_id = run_manifest['game_id']
    p = get_profile(game_id)
    method, variant, target = (run_manifest[k] for k in ('method_id', 'variant_id', 'draw_number'))
    kind, dates = run_manifest['view_kind'], run_manifest['include_dates']
    if (type(method) is not str or not _METHOD.fullmatch(method) or
            type(variant) is not str or not _VARIANT.fullmatch(variant) or
            type(target) is not int or kind not in VIEW_KINDS or type(dates) is not bool):
        raise ValueError('invalid method/view/target identity')
    # Only one tightly specified *forecast-only* exception at first sealed N:
    # Powerball E_1, legacy variant, unordered, date-free, prior rows only.
    legacy_exception = (game_id == 'POWERBALL' and target == 1577 and
                        method == 'E_1' and variant == _E1_VARIANT and
                        kind == 'UNORDERED_SET' and not dates)
    if not (p.historical_development_target_allowed(target) or legacy_exception):
        raise ValueError('target is outside authorised development prefix')
    name = f'{game_id}_results_master.csv'
    sha = run_manifest['master_sha256']
    if (run_manifest['master_file'] != name or type(sha) is not str or
            not _SHA.fullmatch(sha) or type(run_manifest['ledger_version']) is not int or
            run_manifest['ledger_version'] != 1):
        raise ValueError('unapproved source identity')
    folder = repo_root / 'source_data'
    ledger_name = f'{game_id}_results_master_ledger.csv'
    ledger_bytes = _trusted_file_bytes(folder / ledger_name)
    ledger = list(csv.DictReader(io.StringIO(ledger_bytes.decode('ascii'))))
    if (len(ledger) != 1 or ledger[0].get('version') != '1' or
            ledger[0].get('action') != 'INIT' or ledger[0].get('master_sha256') != sha or
            ledger[0].get('first_draw') != str(p.first_draw) or
            ledger[0].get('last_draw') != str(p.holdout_first - 1) or
            ledger[0].get('draw_count') != str(p.holdout_first - p.first_draw)):
        raise ValueError('ledger does not bind approved version-1 development master')
    raw = _trusted_file_bytes(folder / name)
    if hashlib.sha256(raw).hexdigest() != sha:
        raise ValueError('complete master bytes differ from pinned ledger SHA-256')
    evidence_name = f'{game_id}_results_master_init_verification.json'
    evidence = json.loads(_trusted_file_bytes(folder / evidence_name))
    if (type(evidence) is not dict or evidence.get('master_sha256') != sha or
            evidence.get('master_file') != name or evidence.get('game') != game_id or
            evidence.get('first_draw') != p.first_draw or
            evidence.get('last_draw') != p.holdout_first - 1 or
            evidence.get('draw_count') != p.holdout_first - p.first_draw or
            evidence.get('source') != 'LOTTERYWEST_GOV_RESULTS_SEARCH'):
        raise ValueError('INIT verification does not match the pinned source')
    nums, d, drawn, sorted_main, pb = _parse_prefix(raw, game_id, target, include_dates=dates)
    # Outcome-independent method-facing evidence only. Whole-master SHA and
    # INIT/ledger verification remain confined to this orchestration loader
    # and the caller's pinned run manifest, never returned in DrawView.
    order_evidence = {'record': evidence_name, 'status': _ORDER_STATUS}
    return DrawView(game_id=game_id, method_id=method, variant_id=variant,
                    target=target, kind=kind, numbers=nums, dates=d,
                    main=(drawn if kind == 'OPERATOR_DRAWN_ORDER' else sorted_main),
                    powerball=pb, drawn_main=(drawn if kind == 'PAIRED_DIAGNOSTIC' else None),
                    order_status=_ORDER_STATUS,
                    order_evidence=(order_evidence if kind != 'UNORDERED_SET' else None))
