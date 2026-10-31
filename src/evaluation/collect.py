"""WF-1B: the fixed grid and the frozen forecasts (releases and WF-1 design v0.1r1 sections 6.1 steps 2-3, 6.2, 6.2A).

Reads no outcome. It uses the plan alone for the grid, and for each grid cell it finds the batch's own attempts
(the WF-1A attempt binding), checks each through the driver's `attempt_state` and the contract's `read_run` (which
establishes every gate itself, the orphan marker included), and selects the earliest consumable forecast by its
freeze receipt's `frozen_at_utc` (the receipt selection policy, E2R-R40A). If several consumable forecasts exist
for one cell, their `canonical_content_digest`s must be equal; otherwise the cell is `REPRODUCIBILITY_FAIL`.

A track is (method, variant, readout) with readout TOP or WORST, mode WF. A cell is valid for a track when its
selected forecast is `PREDICTION_AVAILABLE` and gives that readout's entry for every barrel of the game (Powerball:
7 main and 1 Powerball; Oz Lotto: 7 main). Every other case is an invalid cell with a reason, counted, never hidden.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import _common.contract_publication as CP
import _common.walk_forward as WF
from _common.contract_records import canonical, record_digest
from _common.game_profiles import get_profile

READOUTS = ('TOP', 'WORST')
_SIDE = {'TOP': 'top', 'WORST': 'worst'}


def grid(plan: dict, member: dict, first: int, last: int) -> list[int]:
    """Design 6.2: every target N in [first, last] with N - E(G) >= max(1, minimum_history_draws). It depends only
    on draw numbers and the declaration."""
    e = get_profile(plan['game_id']).first_draw
    need = max(1, member['minimum_history_draws'])
    return [n for n in range(first, last + 1) if n - e >= need]


def _load(path: Path):
    if not path.is_file() or path.is_symlink():
        return None
    raw = path.read_bytes()
    try:
        rec = json.loads(raw.decode('ascii'))
    except (ValueError, UnicodeDecodeError):
        return None
    return rec if isinstance(rec, dict) and canonical(rec) == raw else None


def _entry(forecast: dict, readout: str, game_id: str):
    """(main labels, powerball or None) for one readout, or None with a reason."""
    if forecast['record_status'] != 'PREDICTION_AVAILABLE':
        return None, forecast['record_status']
    side = _SIDE[readout]
    main = forecast['barrels']['MAIN'][side]
    if main.get('status') != 'PREDICTION_AVAILABLE':
        return None, f"MAIN_{main.get('status')}"
    pb = None
    if game_id == 'POWERBALL':
        sel = forecast['barrels']['POWERBALL'][side]
        if sel.get('status') != 'PREDICTION_AVAILABLE':
            return None, f"POWERBALL_{sel.get('status')}"
        pb = sel['labels'][0]
    return (tuple(main['labels']), pb), None


def collect(plan: dict, first: int, last: int) -> dict:
    """For every member and grid target: the selected forecast's identity and both readouts' entries, or the
    reason the cell is invalid. Returns {'cells': {...}, 'grids': {...}}; reads no outcome."""
    attempts, _bad = WF._attempts(plan)
    reg = WF._registry()
    runs = WF.roots()['runs']
    cells, grids = {}, {}
    for mem in plan['cohort']:
        key = (mem['method_id'], mem['variant_id'])
        g = grid(plan, mem, first, last)
        grids[key] = g
        decl = reg.declaration(mem['declaration_digest'])
        for t in g:
            found = []
            for rid in attempts.get((mem['method_id'], mem['variant_id'], t), ()):
                state, why = WF.attempt_state(plan, mem, t, rid, decl)
                if state != 'DONE':
                    continue
                folder = runs / plan['game_id'] / mem['method_id'] / mem['variant_id'] / rid
                ok, reason = CP.read_run(folder).get('forecast', (False, 'NO_FORECAST'))
                if not ok:
                    continue
                fc = _load(folder / CP.FILES['forecast'])
                rc = _load(folder / CP.FILES['forecast_receipt'])
                if fc is None or rc is None:
                    continue
                found.append({'run_id': rid, 'frozen_at_utc': rc['frozen_at_utc'],
                              'content_digest': fc['canonical_content_digest'], 'receipt_digest': record_digest(rc),
                              'forecast': fc})
            cell = {'consumable_runs': len(found)}
            if not found:
                cell.update(valid=False, reason='NO_CONSUMABLE_FORECAST')
            elif len({f['content_digest'] for f in found}) > 1:
                cell.update(valid=False, reason='REPRODUCIBILITY_FAIL',
                            digests=sorted({f['content_digest'] for f in found}))
            else:
                sel = min(found, key=lambda f: (f['frozen_at_utc'], f['run_id']))
                cell.update(valid=True, run_id=sel['run_id'], forecast_content_digest=sel['content_digest'],
                            freeze_receipt_digest=sel['receipt_digest'],
                            method_revision=sel['forecast']['method_revision'], entries={}, unavailable={})
                for ro in READOUTS:
                    entry, why = _entry(sel['forecast'], ro, plan['game_id'])
                    if entry is None:
                        cell['unavailable'][ro] = why
                    else:
                        cell['entries'][ro] = entry
                fr = sel['forecast'].get('barrels', {})
                cell['ranked_groups'] = {b: fr[b].get('ranked_groups') for b in fr}
            cells[(mem['method_id'], mem['variant_id'], t)] = cell
    return {'cells': cells, 'grids': grids}


def track_cells(collected: dict, method_id: str, variant_id: str, readout: str) -> tuple[list[int], Counter]:
    """(valid targets for one track, Counter of invalid-cell reasons). Design 6.2A."""
    valid, invalid = [], Counter()
    for t in collected['grids'][(method_id, variant_id)]:
        c = collected['cells'][(method_id, variant_id, t)]
        if not c['valid']:
            invalid[c['reason']] += 1
        elif readout not in c['entries']:
            invalid[c['unavailable'][readout]] += 1
        else:
            valid.append(t)
    return valid, invalid


def track_status(valid: list, invalid: Counter) -> str:
    if not valid:
        return 'GRID_EMPTY'
    return 'GRID_INCOMPLETE' if sum(invalid.values()) else 'GRID_COMPLETE'
