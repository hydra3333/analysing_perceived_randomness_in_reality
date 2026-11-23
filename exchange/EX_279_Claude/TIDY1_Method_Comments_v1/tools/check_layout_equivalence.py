"""Build step 1 (the folder layout): the equivalence check.

What this file is for
    It proves that moving the method files into the family and variant folder layout changed no forecast.
    For every development forecast the old system made, it computes the forecast again with the code of the
    project tree it is pointed at, in memory, and requires the new forecast's content digest to equal the old
    record's `canonical_content_digest` exactly. It writes nothing: no forecast, score, report or record, and
    no byte-code cache. It prints its findings and ends with one plain line.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3, phase 1, "the equivalence oracle":
    "every existing variant, both games, every target with an old development forecast, recomputed by the moved
    code and compared by the old content digest. It reads the old records, writes no research record".

Where the old digests come from (both are read-only)
    1. The development walk-forward records that Git tracks, in every copy of the project:
       results/real/development/wf_batches/<GAME>/<batch>/plan.json            the variants and the data version
       results/real/development/scores/<GAME>/<batch>/<attempt>/rank_ledger.jsonl   one digest per scored forecast
    2. The old run folders, which Git ignores and which exist only on the owner's PC (or in his ZIP):
       results/real/development/contract_runs/<GAME>/<method>/<variant>/<run id>/forecast.json  (+ its receipt)
       These also hold the forecasts that were never scored (for example "not enough history" records).
    A forecast found in both places is checked once.

How it knows that nothing is missing
    The tracked batch records also list every run of the old development walk-forward:
       results/real/development/wf_batches/<GAME>/<batch>/segment_*.json      one entry per run, with its outcome
    Every published run in them is an old forecast that must be found and checked. The check counts, for each
    game, how many of those it found an old digest for and how many it did not. Only when both games were checked
    in full and none is missing does it say PASS - COMPLETE. A copy without the old run folders (a fresh clone, the
    cloud workspace) can therefore never report the complete result: it reports PARTIAL and says what is missing.

Which of the project's own modules it uses (all from the tree being checked, <tree>/src/methods)
    Method_Contract_Runner          ADAPTERS: the table of methods the project's own runner dispatches through
    _common.contract_registry       InstalledRegistry: the installed method declarations, looked up by digest
    _common.contract_records        reader_pin: turns a run request into the reader's data-version pin
    _common.game_draws_reader       load_pinned_draw_view: the one reader; builds the earlier-draws-only view
    _common.contract_task           build_method_task: the frozen task a method is given
    _common.contract_forecast       assemble_forecast: ranking, ties, TOP and WORST, and the content digest
    These are the same functions, in the same order, that the project's runner uses before it publishes
    (_common/contract_runner.py, run_contract_method); only the publication step is left out.

What uses it
    The owner, from the step 1 run sheet, on his own PC; and Claude, in a disposable copy, before sending the
    package for review. Nothing in src/ imports it.

Usage
    python -B check_layout_equivalence.py [--tree <project root>] [--game POWERBALL|OZLOTTO|BOTH]
                                          [--part K/N] [--sample N]
    Exit code 0 only for the complete result: both games, every forecast the batch records list found, computed
    again and equal.
"""
from __future__ import annotations

import sys

# No byte-code cache is written into the tree being checked: the check must leave every folder as it found it.
sys.dont_write_bytecode = True

import argparse
import json
import time
from pathlib import Path

# ---------------------------------------------------------------- constants

# The games the old system forecast. Never pooled: each game is checked and reported by itself.
GAMES = ('POWERBALL', 'OZLOTTO')

# Where the old records are, relative to the project root (see the header for what each holds).
BATCH_PLANS_FOLDER = Path('results') / 'real' / 'development' / 'wf_batches'
SCORE_RECORDS_FOLDER = Path('results') / 'real' / 'development' / 'scores'
OLD_RUN_FOLDERS = Path('results') / 'real' / 'development' / 'contract_runs'
RANK_LEDGER_NAME = 'rank_ledger.jsonl'         # one line per scored forecast, with its content digest
BATCH_PLAN_NAME = 'plan.json'                  # the batch's variants and the data version it pinned
FORECAST_RECORD_NAME = 'forecast.json'         # a run folder's frozen forecast record
FORECAST_RECEIPT_NAME = 'forecast_receipt.json'  # its receipt: names the data version the run pinned
BATCH_SEGMENT_PATTERN = 'segment_*.json'       # a batch's run-by-run record: every run with its outcome

# In a batch segment, a run that published a forecast record has this outcome and this start of its reason.
PUBLISHED_OUTCOME = 'SUCCESS'
PUBLISHED_REASON_PREFIX = 'PUBLISHED'

# How many missing forecasts are named one by one before the rest are only counted.
MISSING_EXAMPLES_SHOWN = 5

# The project's rule: an entry at this path blocks every launch, for both games. This check honours it.
ORPHAN_MARKER = Path('transitory_data') / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'

# The only run mode whose old forecasts this check reproduces: the development walk-forward.
DEVELOPMENT_RUN_MODE = 'REAL_DEVELOPMENT'

# A run request must carry a run ID of the project's form. None is published here; this fixed one is a filler.
FILLER_RUN_ID = 'mg-' + '0' * 32

# How often a progress line is printed (in forecasts checked), so a long run is seen to be alive.
PROGRESS_EVERY = 500

EXIT_ALL_EQUAL = 0          # complete: both games, every forecast the batch records list found, computed again, equal
EXIT_DIFFERENCE = 1         # at least one forecast differed or could not be computed: STOP
EXIT_REFUSED = 2            # the check could not start (wrong folder, missing records, orphan marker)
EXIT_PARTIAL = 3            # nothing differed, but the run was not complete: one game, --sample, --part, or
                            # forecasts the batch records list that have no old record in this copy


class CheckRefused(Exception):
    """The check cannot start or cannot go on. The message says what was found, where, why, and what to do."""


# ---------------------------------------------------------------- reading the old records

def read_json_file(path: Path) -> dict:
    """Read one JSON file and return its content.

    path: the file to read.
    Returns the parsed content, for example {'schema': 'WF_BATCH_PLAN_V1', 'game_id': 'POWERBALL', ...}.
    Refuses (CheckRefused) if the file cannot be read or is not valid JSON, naming the file.
    """
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as problem:
        raise CheckRefused(f'Could not read {path}: {problem}. The old records must be complete and unaltered. '
                           'Do not repair the file: stop and send this message to the Claude chat.') from None


def expected_from_tracked_records(tree_root: Path, game_id: str) -> dict:
    """Collect the old forecasts of one game from the records Git tracks (batch plans and rank ledgers).

    tree_root: the project root being checked.
    game_id: 'POWERBALL' or 'OZLOTTO'.
    Returns {forecast key: expected forecast}, where the key is
        (game, method, variant, revision, target draw number, data version, master SHA-256)
    and the value is a dict with everything needed to compute the forecast again, for example
        {'game_id': 'POWERBALL', 'method_id': 'E_2', 'variant_id': 'RECUR_MEAN_ALL_V1', 'method_revision': '1',
         'target_draw_number': 1300, 'declaration_digest': '9c64...', 'registry_entry_digest': 'c28a...',
         'observation_view': 'UNORDERED_SET', 'include_dates': False, 'product_kind': 'WF_FORECAST',
         'master_file': 'POWERBALL_results_master.csv', 'ledger_version': 1, 'master_sha256': 'ce0a...',
         'expected_digest': 'e62a...', 'found_in': 'rank ledger <path>'}.
    Refuses if a ledger names a variant its batch plan does not hold, or gives two digests for one forecast.
    """
    expected = {}
    plans_folder = tree_root / BATCH_PLANS_FOLDER / game_id
    for plan_path in sorted(plans_folder.glob(f'*/{BATCH_PLAN_NAME}')):
        plan = read_json_file(plan_path)
        if plan.get('run_mode') != DEVELOPMENT_RUN_MODE:
            continue
        members = {(m['method_id'], m['variant_id'], m['method_revision']): m for m in plan['cohort']}
        batch_id = plan_path.parent.name
        for ledger_path in sorted((tree_root / SCORE_RECORDS_FOLDER / game_id / batch_id).glob(f'*/{RANK_LEDGER_NAME}')):
            with open(ledger_path, encoding='utf-8') as ledger:
                for line_number, line in enumerate(ledger, start=1):
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    member = members.get((row['method_id'], row['variant_id'], row['method_revision']))
                    if member is None:
                        raise CheckRefused(f'{ledger_path} line {line_number} names {row["method_id"]} '
                                           f'{row["variant_id"]} revision {row["method_revision"]}, which its batch '
                                           f'plan {plan_path} does not hold. The old records disagree with each '
                                           'other: stop and send this message to the Claude chat.')
                    item = {'game_id': game_id, 'method_id': row['method_id'], 'variant_id': row['variant_id'],
                            'method_revision': row['method_revision'], 'target_draw_number': row['draw_number'],
                            'declaration_digest': member['declaration_digest'],
                            'registry_entry_digest': member['registry_entry_digest'],
                            'observation_view': plan['observation_view'], 'include_dates': plan['include_dates'],
                            'product_kind': plan['product_kind'], 'master_file': plan['master_file'],
                            'ledger_version': plan['ledger_version'], 'master_sha256': plan['master_sha256'],
                            'expected_digest': row['forecast_content_digest'],
                            'found_in': f'rank ledger {ledger_path}'}
                    add_expected(expected, item)
    return expected


def batch_inventory(tree_root: Path, game_id: str) -> dict:
    """List every forecast the old development batches of one game published, from the tracked batch records.

    tree_root: the project root being checked.
    game_id: 'POWERBALL' or 'OZLOTTO'.
    Returns {forecast key: where it is listed}, the key as in expected_from_tracked_records, for example
        {('POWERBALL', 'E_2', 'RECUR_MEAN_ALL_V1', '1', 1145, 1, 'ce0a...'): 'segment results/real/...json', ...}.
    This is the list that the old records found must cover: a published run with no old digest in this copy is
    a missing forecast. Refuses if a game has no batch record, or a segment names a variant its plan does not hold.
    """
    inventory = {}
    for plan_path in sorted((tree_root / BATCH_PLANS_FOLDER / game_id).glob(f'*/{BATCH_PLAN_NAME}')):
        plan = read_json_file(plan_path)
        if plan.get('run_mode') != DEVELOPMENT_RUN_MODE:
            continue
        revisions = {(m['method_id'], m['variant_id']): m['method_revision'] for m in plan['cohort']}
        for segment_path in sorted(plan_path.parent.glob(BATCH_SEGMENT_PATTERN)):
            for run in read_json_file(segment_path)['runs']:
                if run['outcome'] != PUBLISHED_OUTCOME or not run['reason_prefix'].startswith(PUBLISHED_REASON_PREFIX):
                    continue
                revision = revisions.get((run['method_id'], run['variant_id']))
                if revision is None:
                    raise CheckRefused(f'{segment_path} lists a run of {run["method_id"]} {run["variant_id"]}, which '
                                       f'its batch plan {plan_path} does not hold. The old records disagree with '
                                       'each other: stop and send this message to the Claude chat.')
                key = (game_id, run['method_id'], run['variant_id'], revision, run['target'],
                       plan['ledger_version'], plan['master_sha256'])
                inventory[key] = f'segment {segment_path.relative_to(tree_root).as_posix()}'
    if not inventory:
        raise CheckRefused(f'No batch record of {game_id} was found under {tree_root / BATCH_PLANS_FOLDER}. Git tracks '
                           'these records, so every copy of the project has them: check that --tree names the '
                           'project root.')
    return inventory


def expected_from_old_run_folders(tree_root: Path, game_id: str) -> dict:
    """Collect the old forecasts of one game from the old run folders, where they exist (the owner's PC).

    tree_root: the project root being checked.
    game_id: 'POWERBALL' or 'OZLOTTO'.
    Returns the same kind of dict as expected_from_tracked_records; empty if the folder does not exist.
    A run folder without a frozen forecast record (a run that failed before publishing) is not a forecast
    and is skipped; a forecast record without its receipt is refused, because the receipt names the data
    version the run pinned.
    """
    expected = {}
    game_folder = tree_root / OLD_RUN_FOLDERS / game_id
    if not game_folder.is_dir():
        return expected
    for forecast_path in sorted(game_folder.glob(f'*/*/*/{FORECAST_RECORD_NAME}')):
        forecast = read_json_file(forecast_path)
        if forecast.get('run_mode') != DEVELOPMENT_RUN_MODE:
            continue
        receipt_path = forecast_path.with_name(FORECAST_RECEIPT_NAME)
        if not receipt_path.is_file():
            raise CheckRefused(f'{forecast_path} has no {FORECAST_RECEIPT_NAME} beside it, so the data version '
                               'it was computed from is not known. Stop and send this message to the Claude chat.')
        receipt = read_json_file(receipt_path)
        item = {'game_id': game_id, 'method_id': forecast['method_id'], 'variant_id': forecast['variant_id'],
                'method_revision': forecast['method_revision'],
                'target_draw_number': forecast['target_draw_number'],
                'declaration_digest': forecast['declaration_digest'],
                'registry_entry_digest': receipt['registry_entry_digest'],
                'observation_view': forecast['observation_view'], 'include_dates': forecast['include_dates'],
                'product_kind': forecast['product_kind'], 'master_file': receipt['master_file'],
                'ledger_version': receipt['ledger_version'], 'master_sha256': receipt['master_sha256'],
                'expected_digest': forecast['canonical_content_digest'],
                'found_in': f'run folder {forecast_path.parent}'}
        add_expected(expected, item)
    return expected


def forecast_key(item: dict) -> tuple:
    """The identity of one old forecast: what was forecast, for which draw, from which data version.

    item: an expected forecast (see expected_from_tracked_records).
    Returns for example ('POWERBALL', 'E_2', 'RECUR_MEAN_ALL_V1', '1', 1300, 1, 'ce0a...').
    """
    return (item['game_id'], item['method_id'], item['variant_id'], item['method_revision'],
            item['target_draw_number'], item['ledger_version'], item['master_sha256'])


def add_expected(expected: dict, item: dict) -> None:
    """Add one old forecast to the collection, once; refuse two different digests for the same forecast.

    expected: the collection being built ({forecast key: expected forecast}); changed in place.
    item: the old forecast to add.
    Returns nothing. The same forecast with the same digest, met again (in a second run folder, or in the
    run folders after the rank ledger), is kept once. Two different digests for one forecast identity means the
    old records disagree, and is refused: this check must not choose between them.
    """
    key = forecast_key(item)
    already = expected.get(key)
    if already is None:
        expected[key] = item
    elif already['expected_digest'] != item['expected_digest']:
        raise CheckRefused(f'Two old records give different content digests for the same forecast {key}: '
                           f'{already["expected_digest"]} ({already["found_in"]}) and {item["expected_digest"]} '
                           f'({item["found_in"]}). Stop and send this message to the Claude chat.')


# ---------------------------------------------------------------- computing one forecast again

class ProjectCode:
    """The project's own functions, imported once from the tree being checked."""

    def __init__(self, tree_root: Path):
        """Put the tree's code first on Python's search path and import what the check needs from it.

        tree_root: the project root being checked. Refuses if it has no src/methods folder.
        """
        methods_folder = tree_root / 'src' / 'methods'
        if not methods_folder.is_dir():
            raise CheckRefused(f'{tree_root} has no src/methods folder, so it is not a project root. Give the '
                               'project folder with --tree, or run this file from inside the project.')
        sys.path[:0] = [str(methods_folder), str(tree_root / 'src')]
        import Method_Contract_Runner
        from _common.contract_forecast import assemble_forecast
        from _common.contract_records import reader_pin
        from _common.contract_registry import InstalledRegistry
        from _common.contract_task import build_method_task
        from _common.game_draws_reader import load_pinned_draw_view
        from _common.contract_vocab import RUN_REQUEST
        imported_from = Path(Method_Contract_Runner.__file__).resolve().parent
        if imported_from != methods_folder.resolve():
            raise CheckRefused(f'The method code was imported from {imported_from}, not from {methods_folder}. '
                               'Another copy of the project is on PYTHONPATH: clear PYTHONPATH and run again.')
        self.tree_root = tree_root
        self.method_table = Method_Contract_Runner.ADAPTERS
        self.registry = InstalledRegistry()
        self.assemble_forecast = assemble_forecast
        self.reader_pin = reader_pin
        self.build_method_task = build_method_task
        self.load_pinned_draw_view = load_pinned_draw_view
        self.run_request_schema = RUN_REQUEST


def recompute_content_digest(code: ProjectCode, item: dict) -> str:
    """Compute one old forecast again, in memory, and return its content digest.

    code: the project's functions from the tree being checked.
    item: the old forecast (see expected_from_tracked_records).
    Returns the new forecast record's canonical_content_digest, for example 'e62ac325...ad91514'.
    Raises whatever the project's own code raises (an unknown declaration, a data version the ledger does
    not hold, a method failure, a failed self-check): the caller reports it as a failure of that forecast.
    The steps are the runner's own, in its order: the pinned earlier-draws-only view; the task; the method's
    compute(); the contract's assembly (ranking, ties, TOP, WORST, digest); the method's verify().
    """
    request = {'schema': code.run_request_schema, 'game_id': item['game_id'], 'method_id': item['method_id'],
               'variant_id': item['variant_id'], 'method_revision': item['method_revision'],
               'target_draw_number': item['target_draw_number'], 'observation_view': item['observation_view'],
               'include_dates': item['include_dates'], 'run_mode': DEVELOPMENT_RUN_MODE,
               'product_kind': item['product_kind'], 'declaration_digest': item['declaration_digest'],
               'registry_entry_digest': item['registry_entry_digest'], 'run_id': FILLER_RUN_ID,
               'master_file': item['master_file'], 'ledger_version': item['ledger_version'],
               'master_sha256': item['master_sha256']}
    declaration = code.registry.declaration(item['declaration_digest'])
    view = code.load_pinned_draw_view(repo_root=code.tree_root, run_manifest=code.reader_pin(request))
    task = code.build_method_task(request, declaration, view)
    method = code.method_table[item['method_id']]
    output = method.compute(task, view)
    record = code.assemble_forecast(declaration, task, view, output)
    if record is None:
        raise ValueError('the method returned a valid output with no TOP or WORST, so no forecast record exists')
    method.verify(task, view, record, None)
    return record['canonical_content_digest']


# ---------------------------------------------------------------- the check of one game

def check_game(code: ProjectCode, game_id: str, part: tuple, sample_per_variant: int | None) -> dict:
    """Check every old forecast of one game and print the findings.

    code: the project's functions from the tree being checked.
    game_id: 'POWERBALL' or 'OZLOTTO'.
    part: (K, N): check only the K-th of N equal parts of the variants (1, 1 means all of them). It lets the
        owner run several windows at once; the parts together cover everything.
    sample_per_variant: None for the real check; a number checks only that many forecasts of each variant
        (a quick trial, never the evidence).
    Returns the counts, for example
        {'game_id': 'POWERBALL', 'listed': 17280, 'missing': 5838, 'expected': 11442, 'from_run_folders': 0,
         'checked': 11442, 'equal': 11442, 'different': 0, 'failed': 0, 'variants': 40},
    where 'listed' is how many forecasts the batch records say were published, 'missing' is how many of those
    have no old digest in this copy, and 'expected' is how many old digests were found (in or outside the list).
    """
    tracked = expected_from_tracked_records(code.tree_root, game_id)
    in_run_folders = expected_from_old_run_folders(code.tree_root, game_id)
    expected = dict(tracked)
    for item in in_run_folders.values():
        add_expected(expected, item)
    if not expected:
        raise CheckRefused(f'No old development forecast of {game_id} was found under {code.tree_root / "results"}. '
                           f'The tracked records ({SCORE_RECORDS_FOLDER.as_posix()}) should be in every copy of '
                           'the project: check that --tree names the project root.')
    listed = batch_inventory(code.tree_root, game_id)
    missing = sorted(set(listed) - set(expected))
    by_variant = {}
    for key, item in expected.items():
        by_variant.setdefault(key[1:4], []).append(item)
    variant_keys = sorted(by_variant)
    part_number, part_count = part
    chosen = [v for position, v in enumerate(variant_keys) if position % part_count == part_number - 1]
    counts = {'game_id': game_id, 'listed': len(listed), 'missing': len(missing),
              'expected': len(expected), 'from_run_folders': len(in_run_folders),
              'only_in_run_folders': len(set(in_run_folders) - set(tracked)),
              'checked': 0, 'equal': 0, 'different': 0, 'failed': 0, 'variants': len(chosen)}
    print(f'[{game_id}] old development forecasts found: {len(expected)} '
          f'({len(tracked)} in the tracked rank ledgers; {len(in_run_folders)} in old run folders, of which '
          f'{counts["only_in_run_folders"]} are in no rank ledger); variants: {len(variant_keys)}'
          + (f'; this run checks part {part_number} of {part_count}: {len(chosen)} variants' if part_count > 1 else ''),
          flush=True)
    print(f'[{game_id}] coverage: the batch records list {len(listed)} published forecasts; an old digest was found '
          f'for {len(listed) - len(missing)} of them; MISSING: {len(missing)}; found outside the batch records: '
          f'{len(set(expected) - set(listed))}', flush=True)
    for key in missing[:MISSING_EXAMPLES_SHOWN]:
        print(f'[{game_id}] missing, for example: {key[1]} {key[2]} revision {key[3]} target draw {key[4]} '
              f'(listed in {listed[key]}; no rank-ledger line and no run folder for it here)', flush=True)
    started = time.monotonic()
    for variant_key in chosen:
        items = sorted(by_variant[variant_key], key=lambda i: (i['target_draw_number'], i['ledger_version']))
        if sample_per_variant is not None:
            items = items[:sample_per_variant]
        variant_equal = 0
        for item in items:
            counts['checked'] += 1
            where = (f'{game_id} {item["method_id"]} {item["variant_id"]} revision {item["method_revision"]} '
                     f'target draw {item["target_draw_number"]} (data version {item["ledger_version"]})')
            try:
                new_digest = recompute_content_digest(code, item)
            except Exception as problem:   # every kind is reported: nothing is swallowed, and the check goes on
                counts['failed'] += 1
                print(f'FAILED    {where}: could not be computed again: {type(problem).__name__}: {problem}; '
                      f'old record: {item["found_in"]}', flush=True)
            else:
                if new_digest == item['expected_digest']:
                    counts['equal'] += 1
                    variant_equal += 1
                else:
                    counts['different'] += 1
                    print(f'DIFFERENT {where}: old digest {item["expected_digest"]}, new digest {new_digest}; '
                          f'old record: {item["found_in"]}', flush=True)
            if counts['checked'] % PROGRESS_EVERY == 0:
                print(f'[{game_id}] ... {counts["checked"]} checked, {time.monotonic() - started:.0f} s', flush=True)
        print(f'[{game_id}] {variant_key[0]} {variant_key[1]} revision {variant_key[2]}: '
              f'{variant_equal} of {len(items)} equal', flush=True)
    return counts


# ---------------------------------------------------------------- the command

def parse_part(text: str) -> tuple:
    """Read the --part value.

    text: 'K/N', for example '2/4' (the second of four parts).
    Returns (K, N) as whole numbers, for example (2, 4). Refuses anything else.
    """
    try:
        part_number, part_count = (int(piece) for piece in text.split('/'))
    except ValueError:
        raise argparse.ArgumentTypeError('--part must look like 2/4 (the second of four parts)') from None
    if not 1 <= part_number <= part_count:
        raise argparse.ArgumentTypeError('--part K/N needs 1 <= K <= N')
    return part_number, part_count


def main(argv: list | None = None) -> int:
    """Run the equivalence check and return the exit code (see the EXIT_ constants)."""
    parser = argparse.ArgumentParser(description='Build step 1: every old development forecast computed again and compared.')
    parser.add_argument('--tree', type=Path, default=Path(__file__).resolve().parents[3],
                        help='the project root to check (default: the project this file is in)')
    parser.add_argument('--game', choices=GAMES + ('BOTH',), default='BOTH')
    parser.add_argument('--part', type=parse_part, default=(1, 1),
                        help='K/N: check only the K-th of N parts of the variants (to use several windows)')
    parser.add_argument('--sample', type=int, default=None,
                        help='a quick trial: only this many forecasts of each variant. NOT the evidence')
    arguments = parser.parse_args(argv)
    tree_root = arguments.tree.resolve()
    games = GAMES if arguments.game == 'BOTH' else (arguments.game,)
    partial_reasons = []
    if arguments.game != 'BOTH':
        partial_reasons.append(f'only {arguments.game} was checked (--game)')
    if arguments.sample is not None:
        partial_reasons.append('--sample was used')
    if arguments.part != (1, 1):
        partial_reasons.append('--part was used (every part must be run)')
    print(f'Equivalence check of build step 1 (specification 17.3). Tree: {tree_root}. Games: {", ".join(games)}. '
          'It computes every old development forecast again, in memory, and compares content digests. '
          'It writes nothing.', flush=True)
    try:
        marker = tree_root / ORPHAN_MARKER
        if marker.exists() or marker.is_symlink():
            raise CheckRefused(f'The orphan marker {marker} exists. It blocks every launch until the owner\'s '
                               'approved clearance; this check does not run while it is there.')
        code = ProjectCode(tree_root)
        all_counts = [check_game(code, game_id, arguments.part, arguments.sample) for game_id in games]
    except CheckRefused as refusal:
        print(f'REFUSED: {refusal}', flush=True)
        print('RESULT: STOP - the equivalence check did not run to its end.', flush=True)
        return EXIT_REFUSED
    for counts in all_counts:
        print(f'[{counts["game_id"]}] checked {counts["checked"]} of {counts["expected"]} old forecasts in '
              f'{counts["variants"]} variants: {counts["equal"]} equal, {counts["different"]} different, '
              f'{counts["failed"]} could not be computed; listed by the batch records {counts["listed"]}, '
              f'MISSING here {counts["missing"]}', flush=True)
        if counts['missing']:
            partial_reasons.append(f'{counts["missing"]} {counts["game_id"]} forecasts that the batch records list '
                                   'have no old record in this copy (their run folders are not here)')
    wrong = sum(c['different'] + c['failed'] for c in all_counts)
    if wrong:
        print(f'RESULT: STOP - {wrong} forecast(s) differ or could not be computed. Build step 1 is not accepted. '
              'Change nothing and retry nothing: send this whole output to the Claude chat.', flush=True)
        return EXIT_DIFFERENCE
    if partial_reasons:
        print('RESULT: PARTIAL - nothing that was checked differed, but this run is NOT the complete equivalence '
              'evidence, because: ' + '; '.join(partial_reasons) + '.', flush=True)
        return EXIT_PARTIAL
    print('RESULT: PASS - COMPLETE - both games; every forecast the batch records list was found, computed again '
          'with this tree\'s code, and has the same content digest.', flush=True)
    return EXIT_ALL_EQUAL


if __name__ == '__main__':
    sys.exit(main())
