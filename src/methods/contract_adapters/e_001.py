"""E_1 through the E_2-readiness contract: an external wrapper, outside E_1's folder (E2R-CODE-2).

Reviewer's E2RC-C04, option (a): E_1's reviewed scientific functions are not touched. This wrapper
calls E_1's own multi-game function, E_001.multigame_e1.forecast, unchanged, and turns its counts
into a contract MethodOutput. Then verify() recomputes E_1's own result and requires the contract
record to equal it label for label (scores, ranking, TOP, WORST) before anything is published, so a
published record can never differ from what E_1 itself computes. Since E_1 revision 2 (owner decision
WF1-13), E_1's function accepts SYNTHETIC_CONTRACT_TEST and REAL_DEVELOPMENT data, with revision 1's counting.
The wrapper reads only the DrawView and the MethodTask it is given.
"""
from __future__ import annotations

from E_001.multigame_e1 import forecast as e1_forecast
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.contract_task import permitted_view_digest
from _common.game_profiles import get_profile

METHOD_ID = 'E_1'


def _e1_result(task, view) -> dict:
    if task.method_id != METHOD_ID:
        raise ValueError('this wrapper is for E_1 only')
    rows = [{'draw': r['draw'], 'MAIN': r['main'], **({'POWERBALL': [r['powerball']]} if 'powerball' in r else {})}
            for r in view.simple_rows()]
    return e1_forecast(get_profile(task.game_id), rows, permitted_view_digest(view, task.run_mode),
                       task.target_draw_number, data_kind=task.run_mode)


def compute(task, view) -> MethodOutput:
    result = _e1_result(task, view)
    return MethodOutput({bid: BarrelOutput(ScoredRanking({int(k): c for k, c in b['scores'].items()}))
                         for bid, b in result['barrels'].items()})


def verify(task, view, forecast, diagnostic) -> None:
    """Raise ValueError unless the contract record equals E_1's own result label for label."""
    if diagnostic is not None:
        raise ValueError('E_1 declares no diagnostic record')
    if forecast is None:
        raise ValueError('E_1 always has a forecast record')
    result = _e1_result(task, view)
    if set(forecast['barrels']) != set(result['barrels']):
        raise ValueError('E_1 identity check: barrels differ')
    for bid, b in result['barrels'].items():
        rec = forecast['barrels'][bid]
        scores = [b['scores'][str(x)] for x in range(rec['label_low'], rec['label_high'] + 1)]
        if (rec['scores'], rec['ranking'], rec['top']['labels'], rec['worst']['labels']) != (
                scores, b['ranking'], b['top'], b['worst']):
            raise ValueError(f'E_1 identity check: the contract record differs from E_1 in barrel {bid}')
