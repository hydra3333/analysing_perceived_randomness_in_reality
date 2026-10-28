"""Independent reviewer R-4 / E2R-T03 synthetic oracle, v0.1.

NO real draw files, holdout files, beacon requests, network or repository writes.
Uses the installed, frozen reader only to parse synthetic files in an external
scratch directory. Does not import or call E2R-CODE-1 implementation.

Usage (from an arbitrary working directory, with the project venv):
  python Independent_E2R_T05_Oracle_v0_1.py prepare --repo PATH_TO_REPO --out SCRATCH
  python Independent_E2R_T05_Oracle_v0_1.py check --out SCRATCH --records RECORDS

For check, CODE-1 independently exports canonical C1.json and C2.json to:
  RECORDS/GAME/TARGET/VIEW/DATES_FLAG/SUFFIX_VARIANT/{C1,C2,D1,TASK_C1,TASK_C2}.json
DATES_FLAG: DATES or NO_DATES. SUFFIX_VARIANT: BASE, SAME_A, SAME_B, LONG.
A complete check requires 960 files (192 cases x five exported records).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
from types import MappingProxyType

ORACLE_SCHEMA = 'REVIEWER_E2R_T05_ORACLE_V0_1'
SUFFIXES = ('BASE', 'SAME_A', 'SAME_B', 'LONG')
KINDS = ('UNORDERED_SET', 'OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC')
GAMES = ('POWERBALL', 'OZLOTTO')
TOY_METHOD = 'E_9000' # purely synthetic fixture identity; not registered or executable
TOY_VARIANT = 'REVIEWER_T05_SYNTHETIC_V1'
FIELD_NAMES = ('game_id', 'profile_version', 'era_id', 'method_id', 'variant_id',
               'method_revision', 'target_draw_number', 'observation_view',
               'include_dates', 'run_mode', 'product_kind')


def canonical(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=True, sort_keys=True, separators=(',', ':'),
                       allow_nan=False) + '\n').encode('ascii')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(raw: bytes):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError('duplicate JSON key: ' + k)
            result[k] = v
        return result
    return json.loads(raw.decode('ascii'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def verified_repo_imports(repo: Path):
    """Import ONLY already-installed reader/profile modules; never CODE-1."""
    base = repo / 'src' / 'methods'
    sys.path.insert(0, str(base))
    from _common.game_draws_reader import DrawView, header_for, load_pinned_draw_view
    from _common.game_profiles import get_profile
    if not Path(sys.modules[DrawView.__module__].__file__).resolve().is_relative_to(base.resolve()):
        raise RuntimeError('reader imported from unexpected location')
    return DrawView, header_for, load_pinned_draw_view, get_profile


def row_for(profile, draw: int, choice: str) -> str:
    """Entirely invented structurally legal data; no lottery-result source."""
    if profile.game_id == 'POWERBALL':
        main, extra = [10, 11, 12, 13, 14, 15, 16], [2]
    else:
        main, extra = [20, 21, 22, 23, 24, 25, 26], [40, 41, 42]
    if choice == 'SAME_A':
        main = [x + 7 for x in main]
        extra = [3] if profile.game_id == 'POWERBALL' else [43, 44, 45]
    elif choice == 'SAME_B':
        main = main[::-1]
        extra = [4] if profile.game_id == 'POWERBALL' else [41, 42, 43]
    elif choice == 'LONG':
        main = [1, 2, 3, 4, 5, 6, 7]
        extra = [8] if profile.game_id == 'POWERBALL' else [8, 9, 10]
    fields = [str(draw), profile.derived_date(draw).isoformat()]
    numerics = [str(x) for x in main + extra]
    if choice == 'LONG':
        numerics = ['"' + x + '"' for x in numerics]
    fields.extend(numerics)
    return ','.join(fields)


def build_synthetic_master(root: Path, profile, target: int, choice: str, header_for):
    folder = root / 'source_data'
    folder.mkdir(parents=True, exist_ok=False)
    game = profile.game_id
    lines = [','.join(header_for(game))]
    for draw in range(profile.first_draw, profile.holdout_first):
        lines.append(row_for(profile, draw, 'BASE' if draw < target else choice))
    raw = ('\n'.join(lines) + '\n').encode('ascii')
    master_sha = sha(raw)
    name = f'{game}_results_master.csv'
    (folder / name).write_bytes(raw)
    ledger = ('version,utc,action,master_sha256,first_draw,last_draw,draw_count\n'
              f'1,synthetic,INIT,{master_sha},{profile.first_draw},'
              f'{profile.holdout_first - 1},'
              f'{profile.holdout_first - profile.first_draw}\n')
    (folder / f'{game}_results_master_ledger.csv').write_bytes(ledger.encode('ascii'))
    evidence_name = f'{game}_results_master_init_verification.json'
    evidence = {'master_sha256': master_sha, 'master_file': name, 'game': game,
                'first_draw': profile.first_draw, 'last_draw': profile.holdout_first - 1,
                'draw_count': profile.holdout_first - profile.first_draw,
                'source': 'LOTTERYWEST_GOV_RESULTS_SEARCH'}
    # The existing reader mandates this marker. All files are stored under a
    # synthetic-only scratch root: this marker is NOT authentic provenance.
    (folder / evidence_name).write_bytes(canonical(evidence))
    return raw, master_sha, name


def view_fingerprint(view, DrawView) -> str:
    import numpy as np
    result = {}
    for slot in DrawView.__slots__:
        value = getattr(view, slot)
        if isinstance(value, np.ndarray):
            assert type(value.base) is bytes and not value.flags.writeable
            result[slot] = {'dtype': str(value.dtype), 'shape': list(value.shape),
                            'sha256': sha(value.tobytes(order='C'))}
        elif isinstance(value, MappingProxyType):
            result[slot] = dict(value)
        else:
            result[slot] = value
    result['rows'] = view.simple_rows()
    return sha(canonical(result))


def toy_reference(view, target: int, digest: str) -> dict:
    """Independent toy reference; NOT a replacement for CODE-1 schema validation.

    Shared-prefix count ranking and a diagnostic are enough to expose suffix
    leakage. Exact C1/C2 bytes are checked only after CODE-1 exports records.
    """
    def tie(barrel: str, label: int):
        fields = ('PREDICTIVE_RANDOMNESS/TIE_SHA256_V1', digest, str(target),
                  TOY_METHOD, TOY_VARIANT, barrel, 'TIE_SHA256_V1', str(label))
        return sha(b''.join(len(f.encode('utf-8')).to_bytes(4, 'little') +
                            f.encode('utf-8') for f in fields))
    counts = {'MAIN': {i: 0 for i in range(1, 36 if view.game_id == 'POWERBALL' else 48)}}
    if view.game_id == 'POWERBALL':
        counts['POWERBALL'] = {i: 0 for i in range(1, 21)}
    for row in view.simple_rows():
        for x in row['main']:
            counts['MAIN'][x] += 1
        if 'powerball' in row:
            counts['POWERBALL'][row['powerball']] += 1
    ranked = {}
    for barrel, counter in counts.items():
        order = sorted(counter, key=lambda x: (-counter[x], tie(barrel, x), x))
        k = 7 if barrel == 'MAIN' else 1
        ranked[barrel] = {'scores': [counter[i] for i in range(1, len(counter)+1)],
                          'ranking': order, 'top': order[:k],
                          'worst': list(reversed(order))[:k]}
    return {'toy_c1': ranked,
            'toy_c2': {'diagnostic_schema_id': 'REVIEWER_PREFIX_SIZE_V1',
                       'values': [{'name': 'prior_draw_count', 'unit': 'draws',
                                   'value': len(view.simple_rows())}]}}


def refuse_repo_output(repo: Path, out: Path):
    if out.resolve().is_relative_to(repo.resolve()):
        raise ValueError('synthetic fixtures must be outside the repository')
    if out.exists():
        raise ValueError('output directory already exists; no overwrite permitted')


def prepare(repo: Path, out: Path):
    DrawView, header_for, load_view, get_profile = verified_repo_imports(repo)
    refuse_repo_output(repo, out)
    out.mkdir(parents=True)
    manifest = {'schema': ORACLE_SCHEMA, 'scope': 'SYNTHETIC_ONLY',
                'source_spec_sha256': '0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954',
                'cases': []}
    for game in GAMES:
        profile = get_profile(game)
        last = profile.holdout_first - 1
        targets = sorted({profile.first_draw + 2, (profile.first_draw + last) // 2,
                          last - 1, last})
        assert len(targets) == 4
        for target in targets:
            if not profile.historical_development_target_allowed(target):
                raise AssertionError('target outside development prefix')
            for view_kind in KINDS:
                for use_dates in (False, True):
                    group = []
                    for choice in SUFFIXES:
                        dates_name = 'DATES' if use_dates else 'NO_DATES'
                        relative = Path(game) / str(target) / view_kind / dates_name / choice
                        root = out / 'fixtures' / relative
                        raw, master_sha, name = build_synthetic_master(root, profile,
                                                                        target, choice, header_for)
                        pin = dict(schema='DEVELOPMENT_MASTER_PIN_V1_REVIEW', game_id=game,
                                   method_id=TOY_METHOD, variant_id=TOY_VARIANT,
                                   draw_number=target, view_kind=view_kind,
                                   include_dates=use_dates, master_file=name,
                                   ledger_version=1, master_sha256=master_sha)
                        view = load_view(repo_root=root, run_manifest=pin)
                        # Label the synthetic nature explicitly; the reader's default
                        # e1_view_digest data_kind denotes REAL development.
                        digest = view.e1_view_digest(data_kind='SYNTHETIC_CONTRACT_TEST')
                        task = dict(game_id=game, profile_version=profile.version,
                                    era_id=profile.era_id, method_id=TOY_METHOD,
                                    variant_id=TOY_VARIANT, method_revision='1',
                                    target_draw_number=target, observation_view=view_kind,
                                    include_dates=use_dates, run_mode='SYNTHETIC_CONTRACT_TEST',
                                    product_kind='SYNTHETIC_TEST_OUTPUT')
                        assert set(task) == set(FIELD_NAMES)
                        task_c2 = dict(task, product_kind='DIAGNOSTIC_OUTPUT')
                        toy = toy_reference(view, target, digest)
                        obj = dict(case=str(relative).replace('\\', '/'), game_id=game,
                                   target_draw_number=target, observation_view=view_kind,
                                   include_dates=use_dates, suffix_variant=choice,
                                   master_sha256=master_sha, master_length=len(raw),
                                   permitted_view_digest=digest,
                                   view_fingerprint=view_fingerprint(view, DrawView),
                                   method_task_c1=task, method_task_c2=task_c2,
                                   toy_output_sha256=sha(canonical(toy)))
                        group.append(obj)
                        manifest['cases'].append(obj)
                    assert len({c['master_sha256'] for c in group}) == 4
                    assert group[0]['master_length'] == group[1]['master_length'] == group[2]['master_length']
                    assert group[0]['master_length'] != group[3]['master_length']
                    for field in ('permitted_view_digest', 'view_fingerprint',
                                  'method_task_c1', 'method_task_c2', 'toy_output_sha256'):
                        assert all(c[field] == group[0][field] for c in group[1:]), field
    assert len(manifest['cases']) == 192
    (out / 'oracle_manifest.json').write_bytes(canonical(manifest))
    print('PREPARE PASS: 192 synthetic cases; 48 contexts x 4 suffixes; no real dataset opened')
    print('Manifest:', out / 'oracle_manifest.json')


def verified_record(path: Path, schema: str) -> tuple[bytes, dict]:
    raw = path.read_bytes()
    obj = strict_json(raw)
    if type(obj) is not dict or obj.get('schema') != schema:
        raise ValueError(f'wrong schema in {path}')
    claimed = obj.get('canonical_content_digest')
    if type(claimed) is not str:
        raise ValueError(f'missing digest in {path}')
    without = {k:v for k,v in obj.items() if k != 'canonical_content_digest'}
    if sha(canonical(without)) != claimed:
        raise ValueError(f'wrong claimed digest in {path}')
    if raw != canonical(obj):
        raise ValueError(f'noncanonical bytes in {path}')
    return raw, obj


def check(out: Path, records: Path):
    manifest = strict_json((out / 'oracle_manifest.json').read_bytes())
    assert manifest['schema'] == ORACLE_SCHEMA and len(manifest['cases']) == 192
    keys = ['game_id', 'target_draw_number', 'observation_view', 'include_dates']
    groups = {}
    all_shas = {c['master_sha256'] for c in manifest['cases']}
    for c in manifest['cases']:
        stem = records / c['case']
        observed = {}
        for code, schema in (('C1','METHOD_FORECAST_V1'),('C2','METHOD_DIAGNOSTIC_V1')):
            raw, obj = verified_record(stem / (code+'.json'), schema)
            if obj.get('permitted_view_digest') != c['permitted_view_digest']:
                raise ValueError(f'{code} wrong permitted view digest at {stem}')
            if obj.get('target_draw_number') != c['target_draw_number'] or obj.get('game_id') != c['game_id']:
                raise ValueError(f'{code} wrong target/game at {stem}')
            if obj.get('observation_view') != c['observation_view'] or obj.get('include_dates') != c['include_dates']:
                raise ValueError(f'{code} wrong view/date at {stem}')
            if any(h.encode('ascii') in raw for h in all_shas):
                raise ValueError(f'{code} leaked an orchestration source hash at {stem}')
            if any(k in obj for k in ('master_sha256','master_file','ledger_version','run_id','source_path')):
                raise ValueError(f'{code} leaked orchestration field at {stem}')
            observed[code] = raw
        d1raw = (stem / 'D1.json').read_bytes()
        d1 = strict_json(d1raw)
        if d1.get('schema') != 'FORECAST_FREEZE_RECEIPT_V1':
            raise ValueError(f'bad D1 schema at {stem}')
        if d1.get('master_sha256') != c['master_sha256']:
            raise ValueError(f'D1 provenance failed to bind changed master at {stem}')
        if (d1.get('forecast_content_digest') != strict_json(observed['C1'])['canonical_content_digest']
                or d1.get('forecast_file_sha256') != sha(observed['C1'])):
            raise ValueError(f'D1 failed to bind C1 output at {stem}')
        for task_kind in ('c1', 'c2'):
            task = strict_json((stem / ('TASK_' + task_kind.upper() + '.json')).read_bytes())
            if task != c['method_task_' + task_kind] or set(task) != set(FIELD_NAMES):
                raise ValueError(f'MethodTask {task_kind} mismatch at {stem}')
        key = tuple(c[k] for k in keys)
        groups.setdefault(key, []).append((c['suffix_variant'], observed))
    assert len(groups) == 48
    for key, items in groups.items():
        assert {c for c, _ in items} == set(SUFFIXES), key
        base = dict(items)['BASE']
        for choice, got in items:
            for code in ('C1','C2'):
                if got[code] != base[code]:
                    raise AssertionError(f'{code} suffix leak at {key} {choice}')
    print('RECORD CHECK PASS: 384 canonical C1/C2 records, 192 D1, 384 TASK; 48 invariant contexts')
    print('NOTE: separate CODE-1 schema validation, task-slot checks and mutation tests still required')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='cmd',required=True)
    prep = sub.add_parser('prepare'); prep.add_argument('--repo',type=Path,required=True);prep.add_argument('--out',type=Path,required=True)
    chk = sub.add_parser('check');chk.add_argument('--out',type=Path,required=True);chk.add_argument('--records',type=Path,required=True)
    a = ap.parse_args()
    if a.cmd == 'prepare':prepare(a.repo.resolve(),a.out.resolve())
    else:check(a.out.resolve(),a.records.resolve())

if __name__ == '__main__':
    main()
