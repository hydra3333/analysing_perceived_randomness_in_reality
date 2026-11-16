#!/usr/bin/env python3
"""Q4 source/receipt/history/run-root guards; NO production scan entry point.

This module contains validation primitives for a future separately authorised
REAL/NULL runner. It cannot launch a scanner, create a run, or publish outputs.
The accompanying qualification harness only uses marked temporary sandboxes.

Production paths are fixed in code; there is no caller-supplied REAL input or
results-root override. Oz REAL profile is pinned to the owner-isolated
modern-era pre-holdout export and is not scan authorisation.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
import hashlib
import io
import json
import os
from pathlib import Path
import re
from typing import Literal

FORMAT = 'OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1'
SCOPE = 'PACKED_STAGING_ONLY_NO_LEGACY_REGISTRY'
MAGIC = b'OUTLANDISH_Q4_SOURCE_PROFILE_SYNTHETIC_V1\n'
SHA256 = re.compile(r'[a-f0-9]{64}\Z')
INTEGER = re.compile(r'(?:0|[1-9][0-9]*)\Z')
RUN_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z')
DIGITS_PRODUCTION = 10_000_000_000
BYTES_PRODUCTION = 5_000_000_000
CONSTANT_STEMS = {
    'pi': 'pi', 'phi': 'golden_ratio', 'e': 'e',
    'log2': 'log2', 'gamma': 'gamma', 'lemniscate': 'lemniscate',
}
PB_HEADER = ('Draw_Number', 'Date', *(f'Drawn_{i}' for i in range(1, 8)), 'Powerball')
# The following Oz layout is intentionally used by *synthetic tests only*.
# It MUST NOT be assumed to describe an approved REAL source file.
SYNTHETIC_OZ_HEADER = ('Draw_Number', 'Date', *(f'Drawn_{i}' for i in range(1, 8)),
                       'Supplementary_1', 'Supplementary_2', 'Supplementary_3')
OZ_HEADER = SYNTHETIC_OZ_HEADER  # confirmed modern operator-drawn 7+3 from 47
OZ_HISTORY_SHA256 = '82557ea5ad01aef075b4031014714417eddbd7d7128666f464f79c416c9bd44c'


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(data)
    return digest.hexdigest()


def _digest(value: object, what: str) -> str:
    if not isinstance(value, str) or SHA256.fullmatch(value) is None:
        raise ValueError(f'invalid {what} SHA-256')
    return value


def _no_links(path: Path) -> None:
    """Reject symlink/junction components, including an existing parent."""
    for component in (path, *path.parents):
        if component.is_symlink() or bool(getattr(component, 'is_junction', lambda: False)()):
            raise ValueError(f'linked path prohibited: {component}')


def _inside(root: Path, path: Path) -> Path:
    root, path = Path(root).absolute(), Path(path).absolute()
    _no_links(root)
    _no_links(path)
    if not path.is_relative_to(root):
        raise ValueError('path outside fixed OUTLANDISH scope')
    if not path.resolve(strict=False).is_relative_to(root.resolve(strict=False)):
        raise ValueError('resolved path escaped fixed OUTLANDISH scope')
    return path


@dataclass(frozen=True)
class FixedRoots:
    """One immutable path policy: installed production OR marked temporary test."""
    base: Path
    synthetic: bool = False

    def __post_init__(self) -> None:
        base = Path(self.base).absolute()
        _no_links(base)
        if self.synthetic:
            # A test root must be a standalone TemporaryDirectory marker, not a
            # directory nested inside installed production results/digits.
            if not (base.name.startswith('OUTLANDISH_Q4_SOURCE_SYNTHETIC_ONLY_')
                    and base.is_dir() and (base/'SYNTHETIC_MARKER').is_file()
                    and (base/'SYNTHETIC_MARKER').read_bytes() == MAGIC):
                raise ValueError('not a marked Q4 synthetic sandbox')
            _inside(base, base/'SYNTHETIC_MARKER')
        else:
            # Fixed on-disk installation; no runtime root substitution. On a
            # non-Windows host, constructing this policy is disallowed.
            if os.name != 'nt' or os.path.normcase(str(base)) != os.path.normcase(
                    str(Path(r'G:\OUTLANDISH_01\large_artifacts').absolute())):
                raise ValueError('REAL published root is fixed to the Windows G: installation')
        object.__setattr__(self, 'base', base)

    @classmethod
    def production(cls) -> 'FixedRoots':
        return cls(Path(r'G:\OUTLANDISH_01\large_artifacts'), False)

    @classmethod
    def test_sandbox(cls, path: Path) -> 'FixedRoots':
        return cls(Path(path), True)

    @property
    def digit_root(self) -> Path:
        return _inside(self.base, self.base/'digits')

    def published_binary(self, constant: str) -> Path:
        if constant not in CONSTANT_STEMS:
            raise ValueError('unknown published constant')
        return _inside(self.base, self.digit_root / (
            f'digits_{CONSTANT_STEMS[constant]}_10_to_10.packed.bin'))

    def receipt(self, constant: str) -> Path:
        binary = self.published_binary(constant)
        return _inside(self.base, binary.with_name(binary.name+'.wsl-receipt.json'))

    def output_parent(self, run_type: Literal['REAL','NULL','TEST_REAL','TEST_NULL']) -> Path:
        expected = ('TEST_REAL', 'TEST_NULL') if self.synthetic else ('REAL', 'NULL')
        if run_type not in expected:
            raise ValueError('run type incompatible with fixed root policy')
        name = 'results' if run_type.endswith('REAL') else 'results_null'
        return _inside(self.base, self.base/name)

    def run_location(self, run_type: str, run_id: str) -> Path:
        if not isinstance(run_id, str) or RUN_ID.fullmatch(run_id) is None:
            raise ValueError('invalid run identifier')
        # Type is encoded in the directory name, not taken from arbitrary path.
        if not run_id.startswith(run_type+'_'):
            raise ValueError('run identifier/type disagreement')
        return _inside(self.base, self.output_parent(run_type)/run_id)

    def validate_run_location(self, run_type: str, run_id: str, requested: Path) -> Path:
        expected = self.run_location(run_type, run_id)
        checked = _inside(self.base, requested)
        if checked != expected:
            raise ValueError('output-root substitution or run identity mismatch')
        if expected.exists() or expected.is_symlink():
            raise FileExistsError('run destination must be new (create-only)')
        if not self.output_parent(run_type).is_dir():
            raise ValueError('fixed results parent absent')
        return expected


def sample_plan(total_bytes: int) -> tuple[tuple[int, int], ...]:
    """Exact deterministic converter plan, OUTLANDISH_SAMPLES_V1."""
    if type(total_bytes) is not int or total_bytes < 1:
        raise ValueError('invalid sample source size')
    length = min(4096, total_bytes)
    hi = total_bytes - length
    offsets = {0, hi, hi//2, hi//4, (3*hi)//4}
    nonce = 0
    while len(offsets) < min(12, hi+1):
        digest = hashlib.sha256(f'{total_bytes}:{nonce}:OUTLANDISH_SAMPLES_V1'.encode()).digest()
        offsets.add(int.from_bytes(digest[:8], 'big') % (hi+1))
        nonce += 1
    return tuple((position, length) for position in sorted(offsets))


@dataclass(frozen=True)
class CheckedSource:
    constant: str
    path: Path
    receipt_path: Path
    receipt_sha256: str
    packed_sha256: str
    digits: int
    packed_bytes: int

    def check_completed_stream(self, actual_sha256: str, bytes_hashed: int) -> None:
        """To be called BEFORE a future runner may mark a manifest COMPLETE."""
        if _digest(actual_sha256, 'scanned source') != self.packed_sha256:
            raise ValueError('entire packed source SHA-256 differs from receipt')
        if type(bytes_hashed) is not int or bytes_hashed != self.packed_bytes:
            raise ValueError('full physical packed-byte count not verified')


def validate_published_source(roots: FixedRoots, constant: str, *,
                              fixture_digits: int | None = None) -> CheckedSource:
    """Read-only preflight; checks exact converter sample plan + sampled bytes.

    Production requires 10^10 logical digits. This does NOT itself hash all
    5GB; the future scanner's once-through actual SHA must be checked via
    CheckedSource.check_completed_stream before COMPLETE. Fixture tests can
    independently hash their tiny entire file and exercise this final gate.
    """
    if not isinstance(roots, FixedRoots):
        raise TypeError('fixed roots policy required')
    if roots.synthetic:
        if type(fixture_digits) is not int or fixture_digits < 32:
            raise ValueError('synthetic source requires explicit logical digit count')
        expected_digits = fixture_digits
    else:
        if fixture_digits is not None:
            raise ValueError('REAL source cannot override 10^10 digit count')
        expected_digits = DIGITS_PRODUCTION
    packed = roots.published_binary(constant)
    receipt = roots.receipt(constant)
    for path in (packed, receipt):
        _inside(roots.base, path)
        if not path.is_file():
            raise ValueError('missing ordinary published source/receipt')
    stat = packed.stat()
    expected_bytes = (expected_digits + 1)//2
    if stat.st_size != expected_bytes:
        raise ValueError('packed source size differs from fixed logical size')
    try:
        raw = receipt.read_bytes()
        record = json.loads(raw.decode('utf-8'))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('invalid converter receipt JSON') from exc
    if not isinstance(record, dict):
        raise ValueError('converter receipt must be an object')
    if (record.get('format') != FORMAT or type(record.get('format_version')) is not int
            or record['format_version'] != 1 or record.get('scope') != SCOPE
            or record.get('constant') != constant
            or record.get('binary_name') != packed.name
            or type(record.get('digits_including_integer')) is not int
            or record['digits_including_integer'] != expected_digits
            or type(record.get('packed_bytes')) is not int
            or record['packed_bytes'] != expected_bytes):
        raise ValueError('converter receipt format, identity, scope or size mismatch')
    binary_digest = _digest(record.get('binary_sha256_streamed'), 'receipt packed source')
    expected_plan = sample_plan(expected_bytes)
    if (type(record.get('sample_block_length')) is not int
            or record['sample_block_length'] != expected_plan[0][1]):
        raise ValueError('converter receipt sample block size mismatch')
    samples = record.get('samples')
    if not isinstance(samples, list) or len(samples) != len(expected_plan):
        raise ValueError('converter receipt sample count mismatch')
    with packed.open('rb') as stream:
        for entry, (start, length) in zip(samples, expected_plan):
            if (not isinstance(entry, dict)
                    or type(entry.get('offset_bytes')) is not int
                    or entry['offset_bytes'] != start
                    or type(entry.get('size')) is not int
                    or entry['size'] != length):
                raise ValueError('converter receipt sample plan mismatch')
            stream.seek(start)
            actual = stream.read(length)
            if len(actual) != length or hashlib.sha256(actual).hexdigest() != _digest(
                    entry.get('sha256'), 'sample'):
                raise ValueError('sampled packed source SHA-256 mismatch')
    # A concurrent replacement can invalidate sampled checks. A final full
    # SHA check must still be performed by the future scanner before COMPLETE.
    if packed.stat().st_size != expected_bytes:
        raise ValueError('packed source changed size during receipt validation')
    return CheckedSource(constant, packed, receipt, hashlib.sha256(raw).hexdigest(),
                         binary_digest, expected_digits, expected_bytes)


@dataclass(frozen=True)
class HistoryProfile:
    game: str
    source: Path
    era_first_draw: int
    cutoff_exclusive: int
    header: tuple[str, ...]
    synthetic: bool = False

    def __post_init__(self) -> None:
        if self.game not in ('powerball', 'oz'):
            raise ValueError('unknown game')
        if (type(self.era_first_draw) is not int
                or type(self.cutoff_exclusive) is not int
                or not 0 < self.era_first_draw < self.cutoff_exclusive):
            raise ValueError('invalid era/cutoff')
        if self.game == 'powerball' and self.header != PB_HEADER:
            raise ValueError('incorrect Powerball source-column profile')
        if self.game == 'oz' and self.header != OZ_HEADER:
            raise ValueError('incorrect Oz source-column profile')
        if self.synthetic:
            source = Path(self.source).absolute()
            roots = [node for node in source.parents
                     if node.name.startswith('OUTLANDISH_Q4_SOURCE_SYNTHETIC_ONLY_')
                     and (node/'SYNTHETIC_MARKER').is_file()]
            if not roots or source.parent != roots[0]/'histories':
                raise ValueError('synthetic history must live inside marked test histories')
            FixedRoots.test_sandbox(roots[0])
            _inside(roots[0], source)
        if not self.synthetic:
            # No caller-selected REAL history: pinned isolated game-specific bytes.
            root = Path(__file__).absolute().parent
            if self.game == 'powerball':
                required = (1144, 1577, root/'POWERBALL_preholdout_only.csv')
            else:
                required = (1474, 1694, root/'OZLOTTO_preholdout_only.csv')
            if (self.era_first_draw != required[0]
                    or self.cutoff_exclusive != required[1]
                    or Path(self.source).absolute() != required[2]):
                raise ValueError('unapproved REAL historical profile')
        _no_links(Path(self.source).absolute())


def installed_history_profile(game: str) -> HistoryProfile:
    if game == 'powerball':
        return HistoryProfile('powerball',
                              Path(__file__).absolute().parent/'POWERBALL_preholdout_only.csv',
                              1144, 1577, PB_HEADER)
    if game == 'oz':
        return HistoryProfile('oz',
                              Path(__file__).absolute().parent/'OZLOTTO_preholdout_only.csv',
                              1474, 1694, OZ_HEADER)
    raise ValueError('unknown game')


@dataclass(frozen=True)
class CheckedDrawset:
    profile: HistoryProfile
    sha256: str
    draw_count: int
    # Source order, including the drawn seven / supplemental roles, is retained.
    draw_rows: tuple[tuple[int, tuple[int, ...]], ...]


def _number(raw: str, *, min_value: int, max_value: int) -> int:
    if INTEGER.fullmatch(raw) is None:
        raise ValueError('noncanonical integer field')
    number = int(raw)
    if number < min_value or number > max_value:
        raise ValueError('historical outcome out of game range')
    return number


def validate_drawset(profile: HistoryProfile, *,
                     expected_sha256: str | None = None) -> CheckedDrawset:
    """Validate COMPLETE ordered isolated history; never peek past cutoff.

    Pass 1 checks *all* IDs before examining any outcome field, preventing a
    contaminated/extended history from being partly analysed. Pass 2 parses
    role-ordered outcomes. The small CSV is read once into immutable bytes.
    """
    if not isinstance(profile, HistoryProfile):
        raise TypeError('explicit installed or synthetic profile required')
    source = Path(profile.source).absolute()
    _no_links(source)
    if not source.is_file():
        raise ValueError('missing isolated historical drawset')
    raw = source.read_bytes()
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    # For REAL Oz, bind exact source bytes before parsing ANY rows or outcomes.
    if not profile.synthetic and profile.game == 'oz' and actual_sha256 != OZ_HISTORY_SHA256:
        raise ValueError('pinned Oz historical CSV SHA-256 mismatch')
    if expected_sha256 is not None and actual_sha256 != _digest(expected_sha256, 'manifest drawset'):
        raise ValueError('drawset SHA-256 differs from run manifest')
    try:
        text = raw.decode('utf-8-sig')
        csv_rows = list(csv.reader(io.StringIO(text, newline=''), strict=True))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('historical CSV invalid') from exc
    if not csv_rows or tuple(csv_rows[0]) != profile.header:
        raise ValueError('wrong historical game/role/header')
    rows = csv_rows[1:]
    count = profile.cutoff_exclusive-profile.era_first_draw
    if len(rows) != count:
        raise ValueError('incomplete or extended isolated historical era')
    # First pass: no outcome access until the *whole* draw-number firewall passes.
    for index, row in enumerate(rows):
        if len(row) != len(profile.header):
            raise ValueError('wrong historical draw field count')
        actual_id = _number(row[0], min_value=1, max_value=2_000_000_000)
        if actual_id != profile.era_first_draw + index:
            raise ValueError('out-of-era, duplicate, shuffled or cutoff-violating draw number')
    result = []
    for index, row in enumerate(rows):
        if not row[1].strip():
            raise ValueError('missing historical draw date')
        highest = 35 if profile.game == 'powerball' else 47
        mains = tuple(_number(v, min_value=1, max_value=highest) for v in row[2:9])
        if len(set(mains)) != 7:
            raise ValueError('duplicate main ball in historical draw')
        if profile.game == 'powerball':
            extra = (_number(row[9], min_value=1, max_value=20),)
        else:
            extra = tuple(_number(v, min_value=1, max_value=47) for v in row[9:12])
            if len(set((*mains, *extra))) != 10:
                raise ValueError('repeated Oz main/supplementary in historical draw')
        result.append((profile.era_first_draw + index, (*mains, *extra)))
    return CheckedDrawset(profile, actual_sha256, count, tuple(result))


if __name__ == '__main__':
    raise SystemExit('No Q4 production CLI: execute the separate synthetic qualification script only')
