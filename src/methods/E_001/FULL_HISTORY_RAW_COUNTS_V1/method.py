"""E_1 variant FULL_HISTORY_RAW_COUNTS_V1: the variant's own entry file.

What this file is for
    It is the one file the research code calls for E_1's only variant. It calls E_1's own counting function
    (E_001/multigame_e1.py, forecast) unchanged and turns its counts into the output every method returns.
    verify() then works E_1's own result out again and requires the assembled record to equal it number for
    number (scores, ranking, TOP and WORST), so a published record can never differ from what E_1 itself
    computes. Until build step 1 this file was the wrapper src/methods/contract_adapters/e_001.py.

Which part of the specification it carries out
    The wrapper: doc/Predictive_Randomness_E2R_CODE2_Design_v0_1r1.md section 5.
    Its place in the layout: doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2, and section 17.3's
    table of what moves where.

Which of the project's own modules it uses
    E_001.multigame_e1           forecast: E_1's own count of how often each number was drawn, with its ranking
    _common.contract_forecast    the types a method returns (MethodOutput, BarrelOutput, ScoredRanking)
    _common.contract_task        permitted_view_digest and view_data_kind: the identity of the earlier-draws view
    _common.game_profiles        get_profile: each game's barrels

What uses it
    src/methods/_common/method_table.py imports it when it builds the runner's table of methods; and E_1's tests.

The header this file had while it was that wrapper, outside E_1's folder; kept
    E_1 through the E_2-readiness contract: an external wrapper, outside E_1's folder (E2R-CODE-2).

    Reviewer's E2RC-C04, option (a): E_1's reviewed scientific functions are not touched. This wrapper
    calls E_1's own multi-game function, E_001.multigame_e1.forecast, unchanged, and turns its counts
    into a contract MethodOutput. Then verify() recomputes E_1's own result and requires the contract
    record to equal it label for label (scores, ranking, TOP, WORST) before anything is published, so a
    published record can never differ from what E_1 itself computes. Since E_1 revision 3 (MHUP-R, design v0.1r5
    section 2), E_1's function takes the view data kind (SYNTHETIC_CONTRACT_TEST or REAL_HISTORICAL_DEVELOPMENT) and
    never a run mode, with revision 1's counting, ranking and tie order.
    The wrapper reads only the DrawView and the MethodTask it is given.
"""
from __future__ import annotations

from E_001.multigame_e1 import forecast as e1_forecast
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.contract_task import permitted_view_digest, view_data_kind
from _common.game_profiles import get_profile

# The fixed identity and output settings of this family; they never change:
#   METHOD_ID  the method's ID as the records name it
METHOD_ID = 'E_1'


def _e1_result(task, view) -> dict:
    """Run E_1's own counting function on the earlier draws.

    task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
    Returns E_1's own result, a dict with one entry for each barrel under 'barrels', each with 'scores' (how often
    each number was drawn), 'ranking', 'top' and 'worst'; for example
        {'barrels': {'MAIN': {'scores': {'1': 61, '2': 58, ...}, 'ranking': [...], 'top': [...], 'worst': [...]}}}.
    Refuses (ValueError) a task that is not for E_1.
    """
    if task.method_id != METHOD_ID:
        raise ValueError('this wrapper is for E_1 only')
    rows = [{'draw': r['draw'], 'MAIN': r['main'], **({'POWERBALL': [r['powerball']]} if 'powerball' in r else {})}
            for r in view.simple_rows()]
    return e1_forecast(get_profile(task.game_id), rows, permitted_view_digest(view, task.run_mode),
                       task.target_draw_number, data_kind=view_data_kind(task.run_mode))


def compute(task, view) -> MethodOutput:
    """Compute E_1's counts for one target draw, from the draws before it only.

    task: the frozen MethodTask.  view: the permitted view (the draws before the target, and nothing else).
    Returns a MethodOutput holding, for each barrel, how often each number was drawn, for example
        MethodOutput({'MAIN': BarrelOutput(ScoredRanking({1: 61, 2: 58, ...}))}).
    """
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
