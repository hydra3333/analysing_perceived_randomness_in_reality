"""Build step 2 (the research engine): the early comparison of DEV's first fill with the old development records.

What this file is for
    After the research job has filled DEV's lists for the first time, this check compares them with what the old
    system recorded, in two parts. It reads only; it writes nothing and computes no forecast. It prints its
    findings and ends with one plain line.
    Part 1, the scores: every score the old development walk-forward recorded (Git tracks them, so this part
    works in every copy of the project) must be in the new score lists with the same numbers drawn, the same
    matches and the same prize division, for TOP and for WORST.
    Part 2, the forecasts: every development forecast the old system kept in its run folders must be in the new
    forecast lists with the same view digest and, for every barrel, the same scores, the same ranking and the
    same TOP and WORST sets.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3 ("the transition check", made early and
    in DEV: the new engine against the old development records) and section 18 ("(real) ... the transition
    check"). The complete transition check, with QA and PROD, belongs to build step 3.

Where the old records come from (read-only)
    results/real/development/scores/<GAME>/<batch>/<attempt>/score_ledger.jsonl      part 1: one line a score
    results/real/development/scores/<GAME>/<batch>/<attempt>/rank_ledger.jsonl       names every scored forecast
    results/real/development/contract_runs/<GAME>/<method>/<variant>/<run id>/forecast.json     part 2
    The run folders are ignored by Git and exist only on the owner's PC. Without them part 2 cannot compare
    anything and the check says so (RESULT: PARTIAL); it never reports agreement it has not seen. As a floor on
    part 2's coverage, every forecast the rank ledgers name must be among the forecasts it compared.

Where the new records come from (read-only)
    results/research/<GAME>/variants/<FAMILY>/<VARIANT>/forecasts.jsonl and scores.jsonl     (specification 5.1)

Which of the project's own modules it uses
    None: it reads the two kinds of record as JSON, so that it does not depend on the code it checks.

What uses it
    The owner, from the step 2 run sheet, after DEV's first fill. Nothing in src/ imports it.

Usage
    python -B compare_fill_with_old_records.py [--tree <project root>] [--game POWERBALL|OZLOTTO|BOTH]
    Exit code 0 only for the complete result: both games, every old score equal, the old run folders present,
    every old development forecast found in the new lists and equal, and every forecast the rank ledgers name
    among them.
"""
from __future__ import annotations

import sys

# No byte-code cache is written into the tree being checked.
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path

# ---------------------------------------------------------------- constants

GAMES = ('POWERBALL', 'OZLOTTO')
OLD_RUN_FOLDERS = Path('results') / 'real' / 'development' / 'contract_runs'
OLD_SCORE_RECORDS = Path('results') / 'real' / 'development' / 'scores'
NEW_LISTS = Path('results') / 'research'
OLD_FORECAST_NAME = 'forecast.json'
RANK_LEDGER_NAME = 'rank_ledger.jsonl'
SCORE_LEDGER_NAME = 'score_ledger.jsonl'
NEW_FORECASTS_NAME = 'forecasts.jsonl'
NEW_SCORES_NAME = 'scores.jsonl'
# The old score record names its track as <GAME>:<method>:<variant>:<TOP or WORST>:<mode>; this is how many parts.
TRACK_PARTS = 5
# Only the old system's development forecasts are compared: its Mode H records are sealed and are not touched.
DEVELOPMENT_RUN_MODE = 'REAL_DEVELOPMENT'
# The old record's two statuses and what each must be in a new list.
OLD_AVAILABLE, OLD_INSUFFICIENT = 'PREDICTION_AVAILABLE', 'INSUFFICIENT_HISTORY'
# How many differing forecasts are printed in full before the rest are only counted.
DIFFERENCES_SHOWN = 10

EXIT_ALL_EQUAL = 0      # complete: both games, every old development forecast found in the new lists and equal
EXIT_DIFFERENCE = 1     # at least one forecast differs or is missing from the new lists: STOP
EXIT_REFUSED = 2        # the check could not start (not a project root; no new lists)
EXIT_PARTIAL = 3        # nothing differed, but the result is not complete; the last line says why


def family_folder_of(method_id: str) -> str:
    """The family folder of an old method ID, for example 'E_2' -> 'E_002' and 'E_17' -> 'E_017'."""
    prefix, number = method_id.split('_')
    return f'{prefix}_{int(number):03d}'


def old_forecasts(tree_root: Path, game_id: str) -> dict:
    """Read every old development forecast of one game from the old run folders.

    Returns {(method ID, variant ID, target draw number): [record, ...]}, each record being
    {'view': the view digest, 'status': the old record status, 'barrels': {barrel: (scores, ranking, top, worst)},
     'where': the run folder}. A forecast computed in several runs has several records; all are compared.
    Returns {} if the run folders are not there.
    """
    found = {}
    game_folder = tree_root / OLD_RUN_FOLDERS / game_id
    if not game_folder.is_dir():
        return found
    for path in sorted(game_folder.glob(f'*/*/*/{OLD_FORECAST_NAME}')):
        record = json.loads(path.read_text(encoding='utf-8'))
        if record.get('run_mode') != DEVELOPMENT_RUN_MODE:
            continue
        barrels = {}
        if record['record_status'] == OLD_AVAILABLE:
            barrels = {barrel_id: (barrel['scores'], barrel['ranking'], barrel['top']['labels'], barrel['worst']['labels'])
                       for barrel_id, barrel in record['barrels'].items()}
        key = (record['method_id'], record['variant_id'], record['target_draw_number'])
        found.setdefault(key, []).append({'view': record['permitted_view_digest'], 'status': record['record_status'],
                                          'barrels': barrels, 'where': str(path.parent)})
    return found


def tracked_forecast_keys(tree_root: Path, game_id: str) -> set:
    """The forecasts the tracked score records name: {(method ID, variant ID, target draw number)}."""
    keys = set()
    for path in sorted((tree_root / OLD_SCORE_RECORDS / game_id).glob(f'*/*/{RANK_LEDGER_NAME}')):
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                row = json.loads(line)
                keys.add((row['method_id'], row['variant_id'], row['draw_number']))
    return keys


def new_forecasts(tree_root: Path, game_id: str) -> dict:
    """Read the new lists of one game.

    Returns {(family folder, variant, target): {'view', 'status', 'reason', 'barrels'}} with the barrels in the
    same form as old_forecasts gives them. Returns {} if the game has no list yet.
    """
    found = {}
    for path in sorted((tree_root / NEW_LISTS / game_id / 'variants').glob(f'*/*/{NEW_FORECASTS_NAME}')):
        for line in path.read_text(encoding='ascii').splitlines()[1:]:
            if not line.strip():
                continue
            content = json.loads(line)['content']
            barrels = {barrel_id: (barrel['scores'], barrel['ranking'], barrel['top'], barrel['worst'])
                       for barrel_id, barrel in content.get('barrels', {}).items()}
            found[(content['family'], content['variant'], content['target'])] = {
                'view': content['permitted_view_digest'], 'status': content['status'],
                'reason': content.get('reason'), 'barrels': barrels}
    return found


def new_scores(tree_root: Path, game_id: str) -> dict:
    """Read the new score lists of one game: {(family folder, variant, target): the score line's content}."""
    found = {}
    for path in sorted((tree_root / NEW_LISTS / game_id / 'variants').glob(f'*/*/{NEW_SCORES_NAME}')):
        family, variant = path.parent.parent.name, path.parent.name
        for line in path.read_text(encoding='ascii').splitlines()[1:]:
            if line.strip():
                content = json.loads(line)['content']
                found[(family, variant, content['target'])] = content
    return found


def score_difference(old: dict, which: str, new: dict | None) -> str | None:
    """Say how a new score line differs from an old score record, or None if they agree.

    old: one line of an old score ledger.  which: 'top' or 'worst', the old record's track.
    new: the new score line's content for the same variant and draw, or None.
    Returns for example 'the new list has no score for it' or 'the main matches differ'.
    """
    if new is None:
        return 'the new list has no score for it'
    if sorted(new['drawn']['MAIN']) != sorted(old['drawn_main']):
        return 'the numbers drawn differ'
    if new['matches']['MAIN'][which] != old['main_matches']:
        return 'the main matches differ'
    if 'drawn_powerball' in old and (new['drawn']['POWERBALL'] != [old['drawn_powerball']]
                                     or new['matches']['POWERBALL'][which] != old['powerball_match']):
        return 'the Powerball drawn or its match differs'
    if 'supplementary_matches' in old and new['supplementary_matches'][which] != old['supplementary_matches']:
        return 'the supplementary matches differ'
    if new['divisions'][which] != old['division']:
        return 'the prize divisions differ'
    return None


def check_scores(tree_root: Path, game_id: str) -> dict:
    """Part 1 for one game: every old score record against the new score lists; prints its findings.

    Returns {'compared': n, 'different': n}.
    """
    new = new_scores(tree_root, game_id)
    compared, different, shown, by_variant = 0, 0, 0, {}
    for path in sorted((tree_root / OLD_SCORE_RECORDS / game_id).glob(f'*/*/{SCORE_LEDGER_NAME}')):
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            old = json.loads(line)
            parts = old['track_id'].split(':')
            if len(parts) != TRACK_PARTS or parts[3] not in ('TOP', 'WORST'):
                raise ValueError(f'{path}: a track is not <GAME>:<method>:<variant>:<TOP or WORST>:<mode>: {old["track_id"]}')
            method_id, variant_id, which = parts[1], parts[2], parts[3].lower()
            found = score_difference(old, which, new.get((family_folder_of(method_id), variant_id, old['draw_number'])))
            compared += 1
            counts = by_variant.setdefault((method_id, variant_id), [0, 0])
            counts[0] += 1
            counts[1] += found is None
            if found is not None:
                different += 1
                if shown < DIFFERENCES_SHOWN:
                    shown += 1
                    print(f'DIFFERENT  {game_id} {method_id} {variant_id} {parts[3]} draw {old["draw_number"]}: {found}')
    for (method_id, variant_id), (total, equal) in sorted(by_variant.items()):
        print(f'{game_id}  scores     {method_id:5s} {variant_id}: {equal} of {total} equal')
    print(f'{game_id}: part 1: old score records (TOP and WORST): {compared}; equal in the new score lists: '
          f'{compared - different}; DIFFERENT: {different}')
    return {'compared': compared, 'different': different}


def difference(old: dict, new: dict | None) -> str | None:
    """Say how a new list line differs from an old forecast record, or None if they agree.

    old: one record from old_forecasts.  new: the line from new_forecasts for the same forecast, or None.
    Returns for example 'the new list has no line for it' or 'barrel MAIN: the TOP sets differ'.
    """
    if new is None:
        return 'the new list has no line for it'
    if new['view'] != old['view']:
        return 'the view digests differ: the two were not computed from the same earlier draws'
    if old['status'] == OLD_INSUFFICIENT:
        if (new['status'], new['reason']) != ('NO_FORECAST', 'INSUFFICIENT_HISTORY'):
            return f'the old record is INSUFFICIENT_HISTORY but the new line is {new["status"]} {new["reason"] or ""}'
        return None
    if new['status'] != 'FORECAST':
        return f'the old record is a forecast but the new line is {new["status"]}: {new["reason"]}'
    if sorted(new['barrels']) != sorted(old['barrels']):
        return 'the two name different barrels'
    for barrel_id in sorted(old['barrels']):
        for part, was, now in zip(('scores', 'rankings', 'TOP sets', 'WORST sets'), old['barrels'][barrel_id],
                                  new['barrels'][barrel_id]):
            if was != now:
                return f'barrel {barrel_id}: the {part} differ'
    return None


def check_game(tree_root: Path, game_id: str) -> dict:
    """Compare one game, both parts, and print its findings.

    Returns {'compared': n, 'different': n, 'old_present': bool, 'new_present': bool, 'tracked_missing': n,
    'scores_compared': n} where 'different' counts the differences of both parts.
    """
    old, new = old_forecasts(tree_root, game_id), new_forecasts(tree_root, game_id)
    scores = check_scores(tree_root, game_id) if new else {'compared': 0, 'different': 0}
    tracked = tracked_forecast_keys(tree_root, game_id)
    by_variant, shown, different, compared = {}, 0, 0, 0
    for (method_id, variant_id, target), records in sorted(old.items()):
        line = new.get((family_folder_of(method_id), variant_id, target))
        counts = by_variant.setdefault((method_id, variant_id), [0, 0])
        for record in records:
            compared += 1
            counts[0] += 1
            found = difference(record, line)
            if found is None:
                counts[1] += 1
                continue
            different += 1
            if shown < DIFFERENCES_SHOWN:
                shown += 1
                print(f'DIFFERENT  {game_id} {method_id} {variant_id} target {target}: {found}  [{record["where"]}]')
    for (method_id, variant_id), (total, equal) in sorted(by_variant.items()):
        print(f'{game_id}  forecasts  {method_id:5s} {variant_id}: {equal} of {total} equal')
    tracked_missing = sorted(tracked - set(old))
    new_only = len(new) - len({(family_folder_of(m), v, t) for (m, v, t) in old})
    print(f'{game_id}: part 2: old development forecasts read from the run folders: {compared} (for {len(old)} '
          f'variant and target pairs); equal in the new lists: {compared - different}; DIFFERENT: {different}; '
          f'lines the new lists hold for other targets (never forecast by the old development runs): {new_only}')
    print(f'{game_id}: part 2: forecasts named by the tracked rank ledgers: {len(tracked)}; of those not among '
          f'the old forecasts compared: {len(tracked_missing)}'
          + (f' (for example {tracked_missing[0]})' if tracked_missing else ''))
    return {'compared': compared, 'different': different + scores['different'], 'old_present': bool(old),
            'new_present': bool(new), 'tracked_missing': len(tracked_missing), 'scores_compared': scores['compared']}


def main(argv: list | None = None) -> int:
    """Run the comparison; print the findings and the one result line; return the exit code."""
    parser = argparse.ArgumentParser(description='Compare DEV\'s first fill with the old development records.')
    parser.add_argument('--tree', default='.', help='the project root (default: the current folder)')
    parser.add_argument('--game', default='BOTH', choices=GAMES + ('BOTH',))
    chosen = parser.parse_args(argv)
    tree_root = Path(chosen.tree).resolve()
    if not (tree_root / 'src' / 'methods').is_dir():
        print(f'RESULT: REFUSED - {tree_root} has no src/methods folder, so it is not a project root. Give the '
              f'project folder with --tree.')
        return EXIT_REFUSED
    games = GAMES if chosen.game == 'BOTH' else (chosen.game,)
    findings = {game_id: check_game(tree_root, game_id) for game_id in games}
    if any(f['different'] for f in findings.values()):
        print('RESULT: STOP - at least one old score or old development forecast is not in the new lists with the same '
              'content. Change nothing and send Claude this whole output.')
        return EXIT_DIFFERENCE
    if any(not f['new_present'] for f in findings.values()):
        print('RESULT: REFUSED - a game has no new list yet. Run the research job first (the run sheet says how).')
        return EXIT_REFUSED
    reasons = []
    if chosen.game != 'BOTH':
        reasons.append('only one game was checked')
    if any(not f['old_present'] for f in findings.values()):
        reasons.append('part 2 compared nothing for at least one game, because the old run folders are not in this '
                       'copy of the project (they exist only on the owner\'s PC)')
    if any(f['tracked_missing'] and f['old_present'] for f in findings.values()):
        reasons.append('the tracked rank ledgers name forecasts that are not among the old run folders read')
    if any(not f['scores_compared'] for f in findings.values()):
        reasons.append('part 1 found no old score record for at least one game')
    scores_total = sum(f['scores_compared'] for f in findings.values())
    if reasons:
        print(f'RESULT: PARTIAL - nothing differed ({scores_total} old scores were compared in part 1), but the '
              f'comparison is not complete: ' + '; '.join(reasons) + '.')
        return EXIT_PARTIAL
    total = sum(f['compared'] for f in findings.values())
    print(f'RESULT: PASS - COMPLETE - both games; all {scores_total} old score records equal the new score lists; '
          f'all {total} old development forecasts in the run folders were found in the new lists with the same view '
          f'digest, scores, ranking, TOP and WORST; every forecast the tracked rank ledgers name is among them.')
    return EXIT_ALL_EQUAL


if __name__ == '__main__':
    sys.exit(main())
