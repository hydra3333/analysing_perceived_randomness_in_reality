"""E_2-readiness contract (E2R-1 v0.3r3): the frozen method-facing task (section 6.2).

Stage-1 contract library (E2R-CODE-1). A method receives exactly a prefix-only DrawView and this
MethodTask. The task holds no run ID, pin, master or ledger hash, path, time, process or worker
identity (E2R-R23, E2R-R24). The permitted-view digest is the reader's existing digest; the
reader's behaviour is not changed (E2R-R25).
"""
from __future__ import annotations

from collections.abc import Mapping

from _common.contract_records import validate_declaration, validate_run_request, record_digest
import _common.contract_vocab as V

TASK_FIELDS = ('game_id', 'profile_version', 'era_id', 'method_id', 'variant_id', 'method_revision',
               'target_draw_number', 'observation_view', 'include_dates', 'run_mode', 'product_kind')
REAL_VIEW_DATA_KIND = 'REAL_HISTORICAL_DEVELOPMENT'  # the reader's existing real-data label


class MethodTask:
    """Read-only: no setters, no extra attributes, plain immutable values only."""
    __slots__ = TASK_FIELDS + ('_sealed',)

    def __init__(self, **fields):
        object.__setattr__(self, '_sealed', False)
        if set(fields) != set(TASK_FIELDS):
            raise ValueError('MethodTask needs exactly its eleven fields')
        for k in TASK_FIELDS:
            v = fields[k]
            if type(v) not in (str, int, bool):
                raise ValueError(f'MethodTask.{k} must be a plain value')
            object.__setattr__(self, k, v)
        object.__setattr__(self, '_sealed', True)

    def __setattr__(self, key, value):
        raise AttributeError('MethodTask is frozen')

    def __delattr__(self, key):
        raise AttributeError('MethodTask is frozen')

    def as_dict(self) -> dict:
        return {k: getattr(self, k) for k in TASK_FIELDS}


def view_data_kind(run_mode: str) -> str:
    return REAL_VIEW_DATA_KIND if run_mode == 'REAL_DEVELOPMENT' else run_mode


def permitted_view_digest(view, run_mode: str) -> str:
    """The reader's existing generic digest (frozen legacy digest for legacy E_1), by its neutral name."""
    return view.e1_view_digest(data_kind=view_data_kind(run_mode))


def build_method_task(request: Mapping, declaration: Mapping, view) -> MethodTask:
    """Check the request against the declaration and the view, then build the task.

    The request must name this declaration by digest; the view must be the one the request pinned.
    """
    validate_run_request(request)
    validate_declaration(declaration)
    if record_digest(declaration) != request['declaration_digest']:
        raise ValueError('run request names a different declaration')
    for f in ('game_id', 'method_id', 'variant_id', 'method_revision'):
        if request[f] != declaration[f]:
            raise ValueError(f'run request and declaration disagree on {f}')
    if request['observation_view'] not in declaration['observation_views']:
        raise ValueError('observation view is not declared by the method')
    if request['include_dates'] and not declaration['uses_dates']:
        raise ValueError('dates may be included only for a method that declares uses_dates')
    if (view.game_id, view.method_id, view.variant_id, view.target, view.kind) != (
            request['game_id'], request['method_id'], request['variant_id'],
            request['target_draw_number'], request['observation_view']):
        raise ValueError('DrawView does not match the run request')
    if (view.draw_date is not None) != request['include_dates']:
        raise ValueError('DrawView date mode does not match the run request')
    return MethodTask(game_id=declaration['game_id'], profile_version=declaration['profile_version'],
                      era_id=declaration['era_id'], method_id=declaration['method_id'],
                      variant_id=declaration['variant_id'], method_revision=declaration['method_revision'],
                      target_draw_number=request['target_draw_number'],
                      observation_view=request['observation_view'], include_dates=request['include_dates'],
                      run_mode=request['run_mode'], product_kind=request['product_kind'])


def record_task(task: MethodTask, schema: str) -> MethodTask:
    """The task identity under which one record kind is assembled (reviewer's E2RC-C03).

    A method computes once from one task. Each record's product_kind is then fixed by the contract
    from the producible table for that record's schema (E2R-R41), never chosen by the method and never
    copied from another record: C1 gets the forecast product of the run mode, C2 DIAGNOSTIC_OUTPUT.
    All other fields are unchanged."""
    if not isinstance(task, MethodTask):
        raise ValueError('a MethodTask is required')
    product, _tier = V.producible(task.run_mode, schema)
    return MethodTask(**dict(task.as_dict(), product_kind=product))
