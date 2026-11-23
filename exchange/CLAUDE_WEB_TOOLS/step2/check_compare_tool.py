"""Check the comparison tool on old run folders made up from a real fill (build step 2, after TASK_T026).

What this file is for
    compare_fill_with_old_records.py compares a first fill with the old system's records. Its second part reads
    the old run folders, which exist only on the owner's PC, so that part could not be run in the cloud; on the
    owner's PC it stopped (TASK_T026) because the tool asked for a line the new lists rightly do not hold. This
    check makes old run folders up from the new lists of a filled tree, in the old system's own form, with an
    INSUFFICIENT_HISTORY record for every target of the old walk-forward that lies before a variant's first
    target, and runs the tool on them. Then it plants four differences, one at a time, and requires the tool to
    report each. It writes only into a temporary folder and prints its findings.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 17.3 (the transition check), as a check of the
    tool that makes it early.

Which of the project's own modules it uses
    None; it runs compare_fill_with_old_records.py, which lies beside it, as a program.

What uses it
    Claude, in the cloud workspace. Usage:  python check_compare_tool.py <a filled tree> <python>
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / 'compare_fill_with_old_records.py'
# The old development walk-forward's targets in each game: (first, last).
OLD_TARGETS = {'POWERBALL': (1145, 1576), 'OZLOTTO': (1475, 1693)}


def old_method_id(family: str) -> str:
    """The old method ID of a family folder, for example 'E_002' -> 'E_2'."""
    prefix, number = family.split('_')
    return f'{prefix}_{int(number)}'


def make_old_run_folders(filled: Path, tree: Path) -> dict:
    """Write old-form forecast records for every variant and old target; return what was written, per game.

    Returns for example {'POWERBALL': {'forecasts': 14478, 'insufficient': 2802}}.
    """
    written = {}
    for game_id, (first_old, last_old) in OLD_TARGETS.items():
        counts = {'forecasts': 0, 'insufficient': 0}
        for path in sorted((filled / 'results' / 'research' / game_id / 'variants').glob('*/*/forecasts.jsonl')):
            lines = path.read_text(encoding='ascii').splitlines()
            header = json.loads(lines[0])
            by_target = {json.loads(line)['content']['target']: json.loads(line)['content'] for line in lines[1:]}
            method_id = old_method_id(header['family'])
            for target in range(first_old, last_old + 1):
                record = {'run_mode': 'REAL_DEVELOPMENT', 'method_id': method_id, 'variant_id': header['variant'],
                          'target_draw_number': target}
                if target < header['first_target']:
                    record.update(record_status='INSUFFICIENT_HISTORY', permitted_view_digest='made-up')
                    counts['insufficient'] += 1
                else:
                    content = by_target[target]
                    record.update(record_status='PREDICTION_AVAILABLE',
                                  permitted_view_digest=content['permitted_view_digest'],
                                  barrels={barrel_id: {'scores': barrel['scores'], 'ranking': barrel['ranking'],
                                                       'top': {'labels': barrel['top']},
                                                       'worst': {'labels': barrel['worst']}}
                                           for barrel_id, barrel in content['barrels'].items()})
                    counts['forecasts'] += 1
                folder = (tree / 'results' / 'real' / 'development' / 'contract_runs' / game_id / method_id
                          / header['variant'] / f'run-{target}')
                folder.mkdir(parents=True)
                (folder / 'forecast.json').write_text(json.dumps(record), encoding='utf-8')
        written[game_id] = counts
    return written


def run_tool(python: str, tree: Path) -> tuple:
    """Run the tool on the tree; return (exit code, the lines that are not per-variant lines)."""
    finished = subprocess.run([python, '-I', '-B', str(TOOL), '--tree', str(tree)], capture_output=True, text=True)
    return finished.returncode, [line for line in finished.stdout.splitlines() if not line.endswith(' equal')]


def one_record(tree: Path, game_id: str, wanted_status: str) -> Path:
    """The path of one made-up old record of a game with the given status (the first in sorted order)."""
    folder = tree / 'results' / 'real' / 'development' / 'contract_runs' / game_id
    for path in sorted(folder.glob('*/*/*/forecast.json')):
        if json.loads(path.read_text(encoding='utf-8'))['record_status'] == wanted_status:
            return path
    raise AssertionError(f'no old record with status {wanted_status}')


def main(filled: Path, python: str) -> int:
    """Run the whole check, print what was found, and return 0 only if every expectation held."""
    failures = []
    with tempfile.TemporaryDirectory() as temporary:
        tree = Path(temporary) / 'tree'
        (tree / 'src' / 'methods').mkdir(parents=True)
        shutil.copytree(filled / 'results' / 'research', tree / 'results' / 'research')
        shutil.copytree(filled / 'results' / 'real' / 'development' / 'scores',
                        tree / 'results' / 'real' / 'development' / 'scores')
        written = make_old_run_folders(filled, tree)
        print('made up, in the old form:', written)
        code, lines = run_tool(python, tree)
        print('\n'.join(lines))
        print(f'exit code {code}')
        if code != 0 or not lines[-1].startswith('RESULT: PASS - COMPLETE'):
            failures.append('the made-up old records, which agree with the lists, did not give PASS - COMPLETE')
        for game_id, counts in written.items():
            wanted = (f'equal in the new lists: {counts["forecasts"]}; INSUFFICIENT_HISTORY records before the '
                      f'variant\'s first target, where the new list has no line: {counts["insufficient"]}; DIFFERENT: 0;')
            if not any(line.startswith(f'{game_id}: part 2: old development forecasts') and wanted in line for line in lines):
                failures.append(f'{game_id}: the part 2 line does not hold "{wanted}"')
        plants = (
            ('an old forecast whose TOP set differs', 'PREDICTION_AVAILABLE',
             lambda r: r['barrels'][sorted(r['barrels'])[0]]['top']['labels'].reverse()),
            ('an old forecast for a target before the first target (the new list has no line)', 'PREDICTION_AVAILABLE',
             lambda r: r.update(target_draw_number=OLD_TARGETS['POWERBALL'][0] - 1)),
            ('an old INSUFFICIENT_HISTORY record at a target the new list forecasts', 'PREDICTION_AVAILABLE',
             lambda r: r.update(record_status='INSUFFICIENT_HISTORY')),
            ('an old forecast whose view digest differs', 'PREDICTION_AVAILABLE',
             lambda r: r.update(permitted_view_digest='another view')),
        )
        for what, status, change in plants:
            path = one_record(tree, 'POWERBALL', status)
            # The variant must start late for the second plant to mean anything: take a late-starting one for it.
            if 'before the first target' in what:
                late = [p for p in sorted(path.parents[3].glob('*/*/*/forecast.json'))
                        if json.loads(p.read_text(encoding='utf-8'))['record_status'] == 'INSUFFICIENT_HISTORY']
                path = late[0]
                original = path.read_text(encoding='utf-8')
                record = json.loads(original)
                record.update(record_status='PREDICTION_AVAILABLE', barrels={})
            else:
                original = path.read_text(encoding='utf-8')
                record = json.loads(original)
                change(record)
            path.write_text(json.dumps(record), encoding='utf-8')
            code, lines = run_tool(python, tree)
            caught = code == 1 and lines[-1].startswith('RESULT: STOP') and any('DIFFERENT: 1;' in line for line in lines)
            print(f'planted: {what}: {"caught" if caught else "NOT CAUGHT"} (exit code {code})')
            if not caught:
                failures.append(f'not caught: {what}')
            path.write_text(original, encoding='utf-8')
        code, lines = run_tool(python, tree)
        if code != 0:
            failures.append('after the plants were taken back the tool did not pass again')
    print('RESULT: ' + ('PASS - the tool agrees with records that agree, counts the insufficient-history records '
                        'apart, and reports each of the four planted differences'
                        if not failures else 'FAIL - ' + '; '.join(failures)))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve(), sys.argv[2]))
