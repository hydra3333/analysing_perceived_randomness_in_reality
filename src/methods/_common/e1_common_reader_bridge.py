"""Forecast-only E_1 bridge; consumes a permitted DrawView, never a table.

It does no I/O, scoring, process control or result publication.
"""
from __future__ import annotations

from .game_draws_reader import DrawView
from .e1_training_view import build_e1_forecast

def prepared_e1_forecast(view: DrawView) -> tuple[dict, str]:
    if (not isinstance(view, DrawView) or view.game_id != 'POWERBALL' or
            view.method_id != 'E_1' or view.variant_id != 'FULL_HISTORY_RAW_COUNTS_V1' or
            view.kind != 'UNORDERED_SET' or view.draw_date is not None):
        raise ValueError('E_1 bridge accepts only the legacy date-free Powerball U view')
    digest = view.e1_view_digest(data_kind='REAL_HISTORICAL_DEVELOPMENT')
    forecast = build_e1_forecast(view.simple_rows(), digest, view.target,
                                 source_kind='REAL_HISTORICAL_DEVELOPMENT')
    return forecast, digest
