#!/usr/bin/env python3
"""Q4g six-constant per-game verified *synthetic-only* report aggregation.

Reads ONLY the independently verified Q4e TEST_REAL and TEST_NULL reports.
No packed file read, original historical source read, production-root discovery,
REAL/NULL production API, or Q5 permission. One game per aggregate, fixed
six-constant Holm family. Each aggregate is create-only and replayable.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Mapping

import OUTLANDISH_01_Q4_Published_Source_Guards_v0_1 as G
import OUTLANDISH_01_Q4c_Synthetic_Run_Processing_v0_1 as P
import OUTLANDISH_01_Q4d_Statistical_Core_v0_1 as S
import OUTLANDISH_01_Q4e_Synthetic_Report_Bundle_v0_1 as R

SCHEMA = 'OUTLANDISH_Q4G_SYNTHETIC_GAME_AGGREGATE_V1'
SCOPE = 'SYNTHETIC_Q4G_NO_REAL_PRODUCTION_OR_Q5'
GAMES = ('powerball', 'oz')
PRIMARY = {'powerball': 'K6S', 'oz': 'K6'}
GROUP_ID = re.compile(r'TEST_AGGREGATE_(?:powerball|oz)_[A-Za-z0-9_-]{1,40}\Z')
RUN_ID = re.compile(r'TEST_(?:REAL|NULL)_[A-Za-z0-9_-]{1,48}\Z')


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _serialized(data: dict) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+'\n').encode('utf-8')


def _read(path: Path) -> bytes:
    G._no_links(path.absolute())
    if not path.is_file():
        raise ValueError('ordinary TEST provenance file required')
    return path.read_bytes()


def _json(raw: bytes) -> dict:
    try:
        obj = json.loads(raw.decode('utf-8'))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError('invalid aggregate JSON') from exc
    if not isinstance(obj, dict):
        raise ValueError('aggregate JSON is not an object')
    return obj


def _create(path: Path, data: bytes):
    G._no_links(path.absolute())
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _impl_hashes() -> dict[str,str]:
    """Snapshot actual Q4a-e implementation + this aggregation module."""
    return R._codes() | {Path(__file__).name: _sha(_read(Path(__file__).absolute()))}


def _validate_inputs(roots: G.FixedRoots, game: str, real_runs: Mapping[str,str],
                     null_runs: Mapping[str,str]) -> tuple[dict,dict]:
    P._check_test_root(roots)
    if game not in GAMES:
        raise ValueError('game must be one independently scoped synthetic test game')
    if not isinstance(real_runs, Mapping) or not isinstance(null_runs, Mapping):
        raise ValueError('exactly two game-specific TEST run rosters required')
    constants=set(S.CONSTANTS)
    if set(real_runs)!=constants or set(null_runs)!=constants:
        raise ValueError('exact six named constants required in each typed TEST roster')
    for kind, roster in (('TEST_REAL',real_runs),('TEST_NULL',null_runs)):
        ids=[]
        for constant in S.CONSTANTS:
            name=roster[constant]
            if not isinstance(name,str) or RUN_ID.fullmatch(name) is None \
                    or not name.startswith(kind+'_'):
                raise ValueError('TEST run ID/type disagreement')
            # Q4e replay, not the spelling of an arbitrary TEST label, binds
            # each run ID to its exact game/constant/kind manifest.
            ids.append(name)
        if len(set(ids))!=6:
            raise ValueError('duplicate TEST run ID in fixed six-constant roster')
    if set(real_runs.values()) & set(null_runs.values()):
        raise ValueError('REAL-like and NULL-like run IDs must be disjoint')
    return dict(real_runs),dict(null_runs)


def _aggregate_folder(roots: G.FixedRoots, game: str, group_id: str,
                      *, create: bool) -> Path:
    P._check_test_root(roots)
    if game not in GAMES or not isinstance(group_id,str) or GROUP_ID.fullmatch(group_id) is None \
            or not group_id.startswith(f'TEST_AGGREGATE_{game}_'):
        raise ValueError('invalid synthetic game aggregate identity')
    parent=G._inside(roots.base,roots.base/'reports_test_aggregate'/game)
    if create:
        parent.mkdir(parents=True, exist_ok=True)
    if not parent.is_dir():
        raise ValueError('aggregate game root absent')
    destination=G._inside(roots.base,parent/group_id)
    if create and (destination.exists() or destination.is_symlink()):
        raise FileExistsError('aggregate is create-only')
    return destination


def compute_verified_test_game_aggregate(roots: G.FixedRoots, game: str,
                                         real_runs: Mapping[str,str],
                                         null_runs: Mapping[str,str]) -> dict:
    """Recompute six-constant Holm and NULL summary-only tails from Q4e replay.

    No unverified report dictionaries are accepted as arguments. This function
    derives them from verified TEST run IDs inside the fixed marked sandbox.
    """
    real_runs,null_runs=_validate_inputs(roots,game,real_runs,null_runs)
    history_shas=set()
    lengths=set()
    iterations=set()
    k_values=set()
    source_sha={}
    pvalues={}
    per_constant={}
    provenance={}
    for constant in S.CONSTANTS:
        rid,nid=real_runs[constant],null_runs[constant]
        real=R.load_verified_synthetic_report(roots,game,constant,'TEST_REAL',rid)
        null=R.load_verified_synthetic_report(roots,game,constant,'TEST_NULL',nid)
        # Exact upstream type, game and constant already checked by Q4e's replay.
        # Constrain this aggregation to the proposed game-specific primary.
        if real.get('transitions_summary',{}).get('family')!=PRIMARY[game]:
            raise ValueError('wrong predeclared synthetic primary family')
        if real.get('primary_is_proposed_owner_vetoable') is not True:
            raise ValueError('primary owner-veto boundary lost')
        perm=real.get('permutation')
        if not isinstance(perm,dict):
            raise ValueError('missing REAL-like permutation provenance')
        raw=perm.get('centered_two_sided_p')
        if raw is not None and (type(raw) not in (int,float) or not math.isfinite(raw)
                                or not 0 <= raw <= 1):
            raise ValueError('invalid primary p-value')
        length=real.get('effective_digits')
        if type(length) is not int or length < 32 or null.get('effective_digits')!=length:
            raise ValueError('inconsistent REAL-like/NULL-like logical source dimensions')
        packed_real=real['provenance']['verified_input_sha256']
        packed_null=null['provenance']['verified_input_sha256']
        if packed_real != packed_null or not G.SHA256.fullmatch(packed_real):
            raise ValueError('REAL-like and NULL-like source digest disagreement')
        source_sha[constant]=packed_real
        history_shas.add(real['history_sha256'])
        lengths.add(length)
        iterations.add(perm.get('iterations_requested'))
        k_values.add(null.get('k'))
        pvalues[constant]=raw
        comparisons=R.compare_verified_summary_counts(real,null)
        # Summarize without injecting any NULL raw event rows into the output.
        per_constant[constant]={
            'raw_primary_p':raw,
            'observed_median_gap':perm.get('observed_median'),
            'primary_evaluable_pairs':perm.get('observed_evaluable_pairs'),
            'primary_permutations_valid':perm.get('valid_permutations'),
            'primary_undefined_reason':perm.get('undefined_reason'),
            'primary_permutation_seed':perm.get('seed'),
            'source_sha256':packed_real,
            'real_like_run':rid,'null_like_run':nid,
            'null_seed':null.get('decoy_seed'),
            'null_generated_history_sha256':null.get('decoy_histories_sha256'),
            'null_k':null.get('k'),
            'summary_only_decoy_comparisons':comparisons,
        }
        provenance[constant]={}
        for kind,run_id in (('TEST_REAL',rid),('TEST_NULL',nid)):
            path=G._inside(roots.base,R._report_folder(roots,kind,run_id,new=False))
            provenance[constant][kind]={
                'report_manifest_sha256':_sha(_read(path/'report_manifest.json')),
                'report_json_sha256':_sha(_read(path/'report.json')),
                'run_id':run_id,
            }
    if len(history_shas)!=1 or len(lengths)!=1:
        raise ValueError('six REAL-like runs must share one isolated game history and N')
    if len(iterations)!=1 or len(k_values)!=1:
        raise ValueError('mixed permutation budgets or decoy K in one game aggregate')
    if type(next(iter(iterations))) is not int or type(next(iter(k_values))) is not int:
        raise ValueError('invalid common permutation/decoy counts')
    if len(set(source_sha.values())) != 6:
        raise ValueError('six distinct fixed TEST constant source digests required')
    adjusted=S.holm_six_constants(pvalues)
    for constant in S.CONSTANTS:
        per_constant[constant]['holm_adjusted_primary_p']=adjusted[constant]
    return {
        'schema':SCHEMA,'scope':SCOPE,'game':game,
        'run_type':'SYNTHETIC_TEST_AGGREGATE_ONLY',
        'constants':list(S.CONSTANTS),
        'primary_family':PRIMARY[game],
        'primary_is_proposed_owner_vetoable':True,
        'fixed_holm_family_size':6,
        'historical_fixture_sha256':next(iter(history_shas)),
        'common_logical_digits':next(iter(lengths)),
        'permutation_iterations':next(iter(iterations)),
        'decoy_K_per_constant':next(iter(k_values)),
        'null_histories_shared_across_constants':len({
            per_constant[c]['null_generated_history_sha256']
            for c in S.CONSTANTS}) == 1,
        'per_constant':per_constant,
        'verified_report_provenance':provenance,
        'note':'EXPLORATORY SYNTHETIC ONLY; NO REAL HISTORY OR PRODUCTION CLAIMS',
    }


def create_verified_test_game_aggregate(roots: G.FixedRoots, game: str,
                                        group_id: str, real_runs: Mapping[str,str],
                                        null_runs: Mapping[str,str],
                                        *, inject_failure_before_complete: bool=False) -> Path:
    """Create-only aggregate publication with explicit INCOMPLETE barrier."""
    body=compute_verified_test_game_aggregate(roots,game,real_runs,null_runs)
    destination=_aggregate_folder(roots,game,group_id,create=True)
    codes=_impl_hashes()
    destination.mkdir(exist_ok=False)
    manifest=destination/'aggregate_manifest.json'
    data={'schema':SCHEMA,'scope':SCOPE,'status':'INCOMPLETE','game':game,
          'group_id':group_id,'aggregate_filename':'aggregate.json',
          'real_runs':dict(real_runs),'null_runs':dict(null_runs),
          'implementation_sha256':codes}
    _create(manifest,_serialized(data))
    payload=_serialized(body)
    _create(destination/'aggregate.json',payload)
    if inject_failure_before_complete:
        raise RuntimeError('injected aggregate failure; remains INCOMPLETE')
    # Require all verified reports to remain unchanged and reproducible before
    # marking the aggregate COMPLETE.
    if _read(destination/'aggregate.json') != _serialized(
            compute_verified_test_game_aggregate(roots,game,real_runs,null_runs)):
        raise ValueError('aggregate changed before publication')
    complete={**data,'status':'COMPLETE','aggregate_sha256':_sha(payload)}
    staging=destination/'aggregate_manifest.next.json'
    _create(staging,_serialized(complete))
    os.replace(staging,manifest)  # only within this new synthetic-owned directory
    return destination


def load_verified_test_game_aggregate(roots: G.FixedRoots, game: str,
                                      group_id: str) -> dict:
    """Replays the complete six-constant aggregate with no packed-source reads."""
    destination=_aggregate_folder(roots,game,group_id,create=False)
    manifest=_json(_read(G._inside(roots.base,destination/'aggregate_manifest.json')))
    expected={'schema':SCHEMA,'scope':SCOPE,'status':'COMPLETE',
              'game':game,'group_id':group_id,'aggregate_filename':'aggregate.json'}
    if any(manifest.get(field)!=value for field,value in expected.items()):
        raise ValueError('unqualified aggregate manifest/status')
    if manifest.get('implementation_sha256')!=_impl_hashes():
        raise ValueError('aggregate implementation changed since publication')
    real_runs,null_runs=_validate_inputs(roots,game,manifest.get('real_runs'),
                                        manifest.get('null_runs'))
    regenerated=compute_verified_test_game_aggregate(roots,game,real_runs,null_runs)
    payload=_read(G._inside(roots.base,destination/'aggregate.json'))
    if _sha(payload)!=manifest.get('aggregate_sha256') or payload!=_serialized(regenerated):
        raise ValueError('aggregate SHA or verified replay mismatch')
    return regenerated


if __name__=='__main__':
    raise SystemExit('NO production aggregate entry point. Use synthetic qualification harness.')
