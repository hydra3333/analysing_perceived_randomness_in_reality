"""Shared synthetic fixtures for the E_2-readiness contract tests (E2R-CODE-1). OFFLINE, synthetic only.

Every master here is invented and written to a temporary folder; no file under the repository's
source_data/ is opened and no real draw value is read. The "synthetic contract method" is a test
double, not a project method: it exists only to exercise the contract on every view and date mode.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT / 'src' / 'methods', ROOT / 'tests'):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from _common.game_profiles import POWERBALL, OZLOTTO, get_profile  # noqa: E402
from _common.contract_records import record_digest  # noqa: E402
from _common.contract_forecast import (  # noqa: E402
    BarrelOutput, DiagnosticValue, MethodOutput, OrderOnlyRanking, ProbabilityVector, ScoredRanking,
)
from _common.contract_task import build_method_task  # noqa: E402
from _common.game_draws_reader import load_pinned_draw_view  # noqa: E402
from test_t05_hardening import write_master  # noqa: E402  (the TH-1 synthetic master writer)

PROBE_METHOD = 'E_2'
PROBE_VARIANT = 'SYNTHETIC_CONTRACT_PROBE'
VIEWS = ('OPERATOR_DRAWN_ORDER', 'PAIRED_DIAGNOSTIC', 'UNORDERED_SET')
RUN_ID = 'mg-synthetic-contract-0001'
FAKE_SHA = 'f' * 64


def channel(rk='RANKING_WITH_SCORES', st='FLOAT64', ot='NOT_APPLICABLE', top='TOP_MARGINAL',
            worst='INVERSE', pk='NONE', tol=None):
    return {'ranking_kind': rk, 'score_type': st, 'order_ties': ot, 'top_rule_id': top, 'worst_rule_id': worst,
            'readout_selection_rule_version': 'SYNTHETIC_READOUT_V1',
            'ranking_tie_readout_version': 'TIE_SHA256_V1' if rk != 'NONE' else 'NOT_APPLICABLE',
            'probability_kind': pk,
            'probability_sum_tolerance': (tol if tol is not None else 1e-12) if pk != 'NONE' else None,
            'smoothing_note': 'synthetic: no smoothing' if pk != 'NONE' else None,
            'calibration_note': 'synthetic: not calibrated' if pk != 'NONE' else None}


def declaration(game='POWERBALL', *, dates=False, method=PROBE_METHOD, variant=None, views=VIEWS,
                channels=None, diagnostic='SYNTHETIC_DIAGNOSTIC_V1', stochastic=False, minimum=1):
    p = get_profile(game)
    if channels is None:
        channels = {'MAIN': channel(pk='NORMALIZED_LABEL_PROBABILITY')}
        if game == 'POWERBALL':
            channels['POWERBALL'] = channel(rk='RANKING_ORDER_ONLY', st='NONE', ot='GROUPED',
                                            pk='PB_CATEGORICAL')
    return {'schema': 'METHOD_DECLARATION_V1', 'game_id': game, 'profile_version': p.version,
            'era_id': p.era_id, 'method_id': method, 'variant_id': variant or PROBE_VARIANT,
            'method_revision': '1', 'observation_views': sorted(views), 'uses_dates': dates,
            'minimum_history_draws': minimum, 'stochastic_fit': stochastic, 'fit_seed_policy_id': None,
            'fit_sampling_model_version': 'SYNTHETIC_FIT_V1', 'channels': channels,
            'diagnostic_schema_id': diagnostic, 'is_capability': 'IS_NOT_APPLICABLE',
            'is_interface_version': None, 'source_method_dependencies': []}


def request(decl, target, view, *, run_mode='SYNTHETIC_CONTRACT_TEST', product=None, sha=FAKE_SHA,
            run_id=RUN_ID, entry_digest=None, include_dates=None):
    product = product or ('WF_FORECAST' if run_mode == 'REAL_DEVELOPMENT' else 'SYNTHETIC_TEST_OUTPUT')
    return {'schema': 'RUN_REQUEST_V1', 'game_id': decl['game_id'], 'method_id': decl['method_id'],
            'variant_id': decl['variant_id'], 'method_revision': decl['method_revision'],
            'target_draw_number': target, 'observation_view': view,
            'include_dates': decl['uses_dates'] if include_dates is None else include_dates,
            'run_mode': run_mode, 'product_kind': product, 'declaration_digest': record_digest(decl),
            'registry_entry_digest': entry_digest or 'e' * 64, 'run_id': run_id,
            'master_file': f'{decl["game_id"]}_results_master.csv', 'ledger_version': 1, 'master_sha256': sha}


def probe_method(view, task):
    """Deterministic synthetic test double. It reads only the DrawView it is given."""
    p = get_profile(task.game_id)
    rows = view.simple_rows()
    out = {}
    for b in p.barrels:
        n = b.high - b.low + 1
        weight = [0.0] * n
        for r in rows:
            if b.barrel_id == 'MAIN':
                seq = r['drawn_main'] if task.observation_view == 'PAIRED_DIAGNOSTIC' else r['main']
                for pos, lab in enumerate(seq):
                    w = 1.0 + (0.125 * pos if task.observation_view != 'UNORDERED_SET' else 0.0)
                    if 'date' in r:
                        w += 0.0625 * (int(r['date'][-2:]) % 3)
                    weight[lab - b.low] += w
            else:
                weight[r['powerball'] - b.low] += 1.0
        total = sum(weight) or 1.0
        prob = [w / total for w in weight]
        if b.barrel_id == 'MAIN':
            ranking = ScoredRanking({b.low + i: weight[i] + 0.0 for i in range(n)})
        else:
            groups = {}
            for i, w in enumerate(weight):
                groups.setdefault(w, []).append(b.low + i)
            ranking = OrderOnlyRanking([groups[w] for w in sorted(groups, reverse=True)])
        out[b.barrel_id] = BarrelOutput(ranking=ranking, probability=ProbabilityVector(prob, 'synthetic weights'))
    diag = [DiagnosticValue('rows', 'draws', len(rows)),
            DiagnosticValue('weight_total_main', 'weight', float(sum(sum(r['main']) for r in rows)) + 0.5)]
    return MethodOutput(barrels=out, diagnostic=diag)


def load_view(root: Path, decl, target, view, sha, include_dates=None):
    req = request(decl, target, view, sha=sha, include_dates=include_dates)
    from _common.contract_records import reader_pin
    v = load_pinned_draw_view(repo_root=root, run_manifest=reader_pin(req))
    return req, v, build_method_task(req, decl, v)


def targets(profile):
    last = profile.holdout_first - 1
    return sorted({profile.first_draw + 2, (profile.first_draw + last) // 2, last - 1, last})


def deep(x):
    return copy.deepcopy(x)


def receipt_for(record, *, run_mode=None, sha=FAKE_SHA, path='STANDALONE', schema='FORECAST_FREEZE_RECEIPT_V1'):
    from _common.contract_receipts import status_at_freeze
    from _common.contract_records import canonical, sha256_hex
    import _common.contract_vocab as V
    mode = run_mode or record['run_mode']
    is_fc = record['schema'] == 'METHOD_FORECAST_V1'
    product, tier = V.producible(mode, record['schema'])
    r = {'schema': schema, 'game_id': record['game_id'], 'target_draw_number': record['target_draw_number'],
         'method_id': record['method_id'], 'variant_id': record['variant_id'],
         'method_revision': record['method_revision'], 'master_file': f'{record["game_id"]}_results_master.csv',
         'ledger_version': 1, 'master_sha256': sha, 'ledger_sha256': 'a' * 64, 'init_record_sha256': 'b' * 64,
         'environment_identity': {'python_version': '3.15.2', 'numpy_version': '2.5.4', 'psutil_version': '7.2.2',
                                  'os_name': 'Windows', 'os_build': '10.0.26300', 'installed_packages_digest': 'c' * 64},
         'run_id': RUN_ID, 'execution_path': path, 'registry_entry_digest': 'e' * 64, 'run_mode': mode,
         'product_kind': product, 'evidence_tier': tier, 'window': None,
         'outcome_opened_at_freeze': False, 'frozen_at_utc': '2026-10-28T12:00:00Z'}
    if is_fc:
        r.update({'forecast_content_digest': record['canonical_content_digest'],
                  'forecast_file_sha256': sha256_hex(canonical(record)), 'cohort_id': 'EXPLORATORY_COHORT',
                  'status_at_freeze': status_at_freeze(record)})
    else:
        r.update({'schema': 'DIAGNOSTIC_FREEZE_RECEIPT_V1',
                  'diagnostic_content_digest': record['canonical_content_digest'],
                  'diagnostic_file_sha256': sha256_hex(canonical(record))})
    return r


def terminal_for(receipts, *, outcome='SUCCESS', record=None, path='STANDALONE'):
    rec = record
    return {'schema': 'RUN_TERMINAL_RECORD_V1', 'run_id': RUN_ID, 'game_id': rec['game_id'],
            'method_id': rec['method_id'], 'variant_id': rec['variant_id'], 'method_revision': rec['method_revision'],
            'target_draw_number': rec['target_draw_number'], 'execution_path': path, 'outcome': outcome,
            'outcome_reason': 'synthetic', 'registry_entry_digest': 'e' * 64,
            'receipt_digests': sorted({record_digest(r) for r in receipts}) if outcome == 'SUCCESS' else []}


def one_record(game='POWERBALL', dates=False, view='UNORDERED_SET'):
    """A valid synthetic C1 and C2 for one game, from a fresh synthetic master."""
    from _common.contract_forecast import assemble_forecast, assemble_diagnostic
    p = get_profile(game)
    decl = declaration(game, dates=dates)
    target = p.first_draw + 6
    with tempfile.TemporaryDirectory() as td:
        sha, _, _ = write_master(Path(td), p, target, 0)
        req, v, task = load_view(Path(td), decl, target, view, sha)
        out = probe_method(v, task)
        return decl, req, v, task, out, assemble_forecast(decl, task, v, out), assemble_diagnostic(decl, task, v, out)
