"""Compare the simplified engine of this tree with the frozen engine, from the same results.

What this file is for
    The simple scheme took the administration out of the engine and left the science alone. This tool is the
    proof that it did: given the same results, the simplified engine (in a_p_r_i_r_DEV) and the frozen engine
    (the code at the top level of the repository, as reviewed) must give the same forecasts, the same scores,
    the same two OV-1 series, line by line, and the same reports. It runs each engine in its own Python
    process, each importing only the code of its own tree, and compares what the two trees then hold. It changes
    nothing in the repository and reads no draw value itself.

    The reports' wording was changed on purpose after the engine was proved the same (the scheme's words:
    "retired" for "withdrawn", "method" for "variant", the second OV-1 series exploratory with no error bound
    claimed, nothing "set aside"). So before the report files are compared byte for byte, the frozen engine's
    report files are given the new wording by the declared list WORDING_CHANGES below, and nothing else. A
    change of wording that is not on the list, or a figure that differs, still shows as DIFFERENT.

    Commands (the first word after the program's name):
      run <tree> [job arguments]      run the research job of the engine that lies in <tree>, with this Python
      align <frozen tree> <new tree>  give the methods of both trees the same starting draws for the second
                                      OV-1 series (a spread of them, so that the cohort changes from draw to
                                      draw); run both jobs again afterwards
      trees <frozen tree> <new tree>  compare what the two trees hold
      code <frozen tree> <new tree>   list each source file as the same, the same but for comments, changed, or
                                      in one tree only
      invented <folder>               the whole comparison on invented results, in a new folder: make the two
                                      trees, run both jobs, align, run both again, compare

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 9 (how we know the science did not move).

Which of the project's own modules it uses
    none in its own process. The small programs it starts in each tree use that tree's research package.

What uses it
    the people and the task files that make the comparison; nothing in the engine.
"""
from __future__ import annotations

import argparse
import ast
import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

GAMES = ('POWERBALL', 'OZLOTTO')
RESEARCH = 'results/research'
# What a frozen tree needs of the repository's top level, and a new tree of a_p_r_i_r_DEV, to run its engine.
FROZEN_PARTS = ('src/research', 'src/evaluation', 'src/methods', 'src/research_command.py',
                'deploy/INFRA_MANIFEST.ini', 'Run_Research.bat', 'Withdraw_Variant.bat')
NEW_PARTS = ('src', 'tests/research_fixtures.py')
# The spread of starting draws "align" gives: method number i of a game (in identity order) counts from the
# draw SPREAD_BACK - SPREAD_STEP * (i % SPREAD_GROUPS) before the last draw on file, or from its own first
# target if that is later (the frozen engine never lets a method count before it has a line).
SPREAD_BACK, SPREAD_STEP, SPREAD_GROUPS = 40, 8, 5

# The text the second OV-1 series' print-out prints after its preamble: the frozen engine's (specification
# 10.6), and the simplified engine's (research/reports.py PREVAILING_CLAIM). Both print it wrapped at 110 columns.
FROZEN_CLAIM = (
    'If this game\'s draws are fair, and if nothing that decided a draw\'s forecasts or which variants counted at '
    'it was influenced by that draw\'s result (that includes what code was installed, corrected or withdrawn and '
    'when, which backup was restored, and any rerun), the chance that this score ever reaches 40 is at most 2.5%. '
    'The software checks that each forecast was computed from earlier draws only, that the variants counted are '
    'those fixed by draw number, and that every draw is taken once. It cannot check the second \'if\'.')
NEW_CLAIM = (
    'An exploratory indicator, like the series over all draws: the same OV-1 calculation, with each method counted '
    'only from the draw after its establishment draw (the last draw this tree held when that version of the '
    'method was first used here) up to, and not including, the draw it is retired from. No error bound is claimed '
    'for it: methods are added, corrected and retired as the research goes on, and those choices may be influenced '
    'by observed results. 40 is a reference line only. Forecasts are computed using the permitted earlier-draw '
    'view, and each draw contributes at most once. These safeguards do not establish that method choices were '
    'independent of observed results.')
CLAIM_WIDTH = 110


def claim_changes() -> tuple:
    """The claim's change as it stands in the two kinds of report file: as plain lines in the .txt, and as lines
    beginning '# ' in the .csv."""
    frozen, new = textwrap.wrap(FROZEN_CLAIM, CLAIM_WIDTH), textwrap.wrap(NEW_CLAIM, CLAIM_WIDTH)
    return (('\r\n'.join(frozen), '\r\n'.join(new)),
            ('\r\n'.join(f'# {line}' for line in frozen), '\r\n'.join(f'# {line}' for line in new)))


# The declared changes of the reports' wording, as (the frozen engine's text, the simplified engine's text), applied
# in this order to the frozen engine's report files (whose lines end CRLF) before they are compared. Each keeps the
# columns of a table where it stands: a column's name is replaced together with the spaces that pad it.
WORDING_CHANGES = claim_changes() + (
    ('a variant\'s figures at draws before its installation', 'a method\'s figures at draws before its installation'),
    ('    Variants: ', '    Methods: '),
    ('What each variant forecast for this draw', 'What each method forecast for this draw'),
    ('score (proved lower bound) ', 'score (numerical lower bound) '),
    ('; bar 40; REACHED', '; reference line 40: reached'),
    ('; bar 40; not reached', '; reference line 40: not reached'),
    ('prevailing OV-1: not started; waiting for a successful results step',
     'prevailing OV-1: not started; no method has an establishment draw yet'),
    ('OV-1 EXPLORATORY RETROSPECTIVE - not the prevailing score;', 'OV-1 EXPLORATORY RETROSPECTIVE - over all draws;'),
    ('counting every variant wherever it has one', 'counting every method wherever it has one'),
    ('WITHDRAWN from draw ', 'RETIRED from draw '),
    ('not scored: withdrawn)', 'not scored: retired)'),
    ('  variant ', '  method  '),                          # a .txt table's column name, not the first column
    ('\r\nvariant ', '\r\nmethod  '),                      # a .txt table's column name, the first column
    ('order_top,variant,', 'order_top,method,'),            # the league .csv's column names
    ('\r\nvariant,line,', '\r\nmethod,line,'),              # the next-draw .csv's column names
    ('each variant over every draw up to that one', 'each method over every draw up to that one'),
    ('    What each variant forecast for a draw.', '    What each method forecast for a draw.'),
    ('    The prevailing OV-1 score: one line a draw from its start, with the claim it supports and the counts\r\n'
     '    that say what kind of evidence it is.',
     '    The second OV-1 series: one line a draw, each method counted from its establishment draw until it\r\n'
     '    is retired. Exploratory, like the one below; with the counts that say what kind of evidence it is.'),
    ('\r\nnot_current/\r\n    Reports the job moved out of view because the stored results they were made from are '
     'not current\r\n    (see NOT_CURRENT_FROM.json one folder up, and what the job said).', ''),
)


def with_new_wording(data: bytes) -> tuple:
    """A frozen engine's report file given the new wording. Returns (the bytes, how many replacements were made)."""
    made = 0
    for frozen, new in WORDING_CHANGES:
        made += data.count(frozen.encode('ascii'))
        data = data.replace(frozen.encode('ascii'), new.encode('ascii'))
    return data, made


# The small programs run inside a tree. Each puts that tree's code, and no other, first on the import path.
PREAMBLE = """
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(tree / 'src'), str(tree / 'src' / 'methods')]
GAMES = ('POWERBALL', 'OZLOTTO')
"""
RUN_JOB = PREAMBLE + """
from research.research_job import main
sys.exit(main(sys.argv[2:], tree))
"""
SPREAD = PREAMBLE + f"""
from research.reader import first_target, results_on_file
from research.variant_folders import find_variants
variants, refused = find_variants(tree / 'src' / 'methods')
last = {{game_id: results_on_file(tree, game_id).last_draw for game_id in GAMES}}
def first_counted(game_id, variant):
    order = sorted(v.identity for v in variants if v.supports(game_id))
    spread = last[game_id] - {SPREAD_BACK} + {SPREAD_STEP} * (order.index(variant.identity) % {SPREAD_GROUPS})
    return max(spread, first_target(game_id, variant.minimum_earlier_draws(game_id)))
"""
ALIGN_FROZEN = SPREAD + """
from research.status_file import STATUS_FILE_NAME, GameStatus, read_status, write_status
for variant in variants:
    games = [game_id for game_id in GAMES if variant.supports(game_id)]
    path = variant.folder / STATUS_FILE_NAME
    statuses = read_status(path, games)
    for game_id in games:
        statuses[game_id] = GameStatus(eligible_from=first_counted(game_id, variant),
                                       eligibility_recorded='set by compare_with_frozen.py for the comparison')
    write_status(path, variant.family, variant.variant, statuses)
print(f'frozen tree: {len(variants)} status files given their first counted draws')
"""
ALIGN_NEW = SPREAD + """
from research import method_flags
for variant in variants:
    pairs = {'fingerprint': variant.fingerprint}
    for game_id in GAMES:
        if variant.supports(game_id):
            pairs[f'in_place_since_{game_id}'] = str(first_counted(game_id, variant) - 1)
    method_flags.write_flag(variant.folder / method_flags.IN_PLACE_NAME, pairs,
                            'Set by compare_with_frozen.py for the comparison.')
print(f'new tree: {len(variants)} IN_PLACE_SINCE files given the same draws')
"""
# The frozen engine keeps no file of its series over all draws: this makes it from the frozen tree's stored
# lists with the frozen engine's own code, and prints it as one JSON line.
FROZEN_EXPLORATORY = PREAMBLE + """
import json
from research import ov1_ledger
from research.code_identity import forecasting_code_identity, read_manifest
from research.game_state import MAIN_BARREL, load_variant_state
from research.reader import results_on_file
from research.scoring import read_outcome
from research.status_file import STATUS_FILE_NAME, read_status
from research.variant_folders import find_variants
game_id = sys.argv[2]
variants, refused = find_variants(tree / 'src' / 'methods')
code_identity = forecasting_code_identity(tree, read_manifest(tree))
results = results_on_file(tree, game_id)
states = []
for variant in variants:
    if variant.supports(game_id):
        statuses = read_status(variant.folder / STATUS_FILE_NAME, [g for g in GAMES if variant.supports(g)])
        states.append(load_variant_state(tree, game_id, variant, statuses[game_id], code_identity))
drawn = {draw: read_outcome(results, draw)[MAIN_BARREL]
         for state in states for draw in state.score_contents if draw <= results.last_draw}
series = ov1_ledger.exploratory_series(game_id, states, drawn, results.last_draw)
print(json.dumps([[line['content'], line['audit']] for line in series]))
"""
INVENT_RESULTS = PREAMBLE + """
sys.path.insert(0, str(tree / 'tests'))
from research.reader import first_target
from research.variant_folders import find_variants
from research_fixtures import write_results
variants, refused = find_variants(tree / 'src' / 'methods')
for game_id in GAMES:
    latest = max(first_target(game_id, v.minimum_earlier_draws(game_id)) for v in variants if v.supports(game_id))
    write_results(tree, game_id, latest + int(sys.argv[2]) - 1, seed=20261126)
    print(f'{game_id}: invented results written through draw {latest + int(sys.argv[2]) - 1}')
"""


def in_tree(tree: Path, program: str, *arguments) -> int:
    """Run one of the small programs above in its own Python process, for a tree. Returns its exit code."""
    return subprocess.run([sys.executable, '-I', '-B', '-u', '-c', program, str(tree), *arguments]).returncode


def records_of(path: Path) -> list:
    """The records of a list file after its header ([] if the file does not exist)."""
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_bytes().decode('ascii').splitlines() if line.strip()][1:]


def methods_with_results(tree: Path, game_id: str) -> list:
    """The identities of the methods that have results for a game in a tree, in order."""
    top = tree / RESEARCH / game_id / 'variants'
    return sorted(f'{path.parent.name}/{path.name}' for path in top.glob('*/*') if path.is_dir())


def series_over_all_draws(tree: Path, game_id: str) -> list:
    """The series over all draws of a game in a tree, as [content, audit] pairs in draw order: read from the
    tree's own file of it (the simplified engine writes one), or, for a tree of the frozen engine, made from the
    tree's stored lists by the frozen engine's own code in its own process."""
    stored = tree / RESEARCH / game_id / 'ov1' / 'exploratory.jsonl'
    if stored.is_file():
        return [[line['content'], line['audit']] for line in records_of(stored)]
    done = subprocess.run([sys.executable, '-I', '-B', '-c', FROZEN_EXPLORATORY, str(tree), game_id],
                          capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(f'the series over all draws could not be made in {tree}: {done.stderr[-2000:]}')
    return json.loads(done.stdout)


def report_files(tree: Path, game_id: str) -> dict:
    """Every report file of a game with its bytes, the tree's own path replaced by <TREE>; the side file of
    making times and anything the frozen engine set aside are left out."""
    top = tree / RESEARCH / game_id / 'reports'
    found = {}
    for path in sorted(top.rglob('*')):
        relative = path.relative_to(top).as_posix()
        if path.is_file() and relative != 'made_times.csv' and not relative.startswith('not_current/'):
            found[relative] = path.read_bytes().replace(str(tree).encode('ascii'), b'<TREE>')
    return found


def frozen_report_files(tree: Path, game_id: str) -> tuple:
    """The frozen engine's report files as report_files gives them, each given the new wording; and how many
    replacements that took in all."""
    found, made = {}, 0
    for relative, data in report_files(tree, game_id).items():
        found[relative], times = with_new_wording(data)
        made += times
    return found, made


def compare_trees(frozen: Path, new: Path, say=print) -> bool:
    """Compare what two trees hold. Says one line for each thing compared; returns True if all are the same."""
    same = True

    def check(what: str, a, b, detail: str = '') -> None:
        """Say SAME or DIFFERENT for one thing."""
        nonlocal same
        if a == b:
            say(f'SAME       {what}{detail}')
        else:
            same = False
            say(f'DIFFERENT  {what}{detail}')

    for game_id in GAMES:
        frozen_methods, new_methods = methods_with_results(frozen, game_id), methods_with_results(new, game_id)
        check(f'{game_id}: the methods that have results', frozen_methods, new_methods,
              f' ({len(frozen_methods)} and {len(new_methods)})')
        counts = {'forecast lines': 0, 'FORECAST': 0, 'NO_FORECAST': 0, 'score lines': 0}
        differing = []
        for identity in sorted(set(frozen_methods) & set(new_methods)):
            pair = [(records_of(tree / RESEARCH / game_id / 'variants' / identity / 'forecasts.jsonl'),
                     records_of(tree / RESEARCH / game_id / 'variants' / identity / 'scores.jsonl'))
                    for tree in (frozen, new)]
            forecasts = [[(line['content'], line['content_digest'], line['envelope']['target_result_on_file'])
                          for line in lines] for lines, _ in pair]
            scores = [[line['content'] for line in lines] for _, lines in pair]
            if forecasts[0] != forecasts[1] or scores[0] != scores[1]:
                differing.append(identity)
            counts['forecast lines'] += len(forecasts[1])
            counts['score lines'] += len(scores[1])
            for content, _, _ in forecasts[1]:
                counts[content['status']] += 1
        check(f'{game_id}: every forecast and every score of every method', differing, [],
              f' ({counts["forecast lines"]} forecast lines: {counts["FORECAST"]} forecasts and '
              f'{counts["NO_FORECAST"]} no-forecasts; {counts["score lines"]} scores)'
              + (f'; differing: {", ".join(differing[:10])}' if differing else ''))
        series = [[(line['content'], line['audit']) for line in
                   records_of(tree / RESEARCH / game_id / 'ov1' / 'prevailing.jsonl')] for tree in (frozen, new)]
        last = series[1][-1][0] if series[1] else None
        check(f'{game_id}: the second OV-1 series, line by line', series[0], series[1],
              f' ({len(series[0])} and {len(series[1])} lines'
              + (f'; draws {series[1][0][0]["draw"]} to {last["draw"]}' if last else '') + ')')
        every = [series_over_all_draws(tree, game_id) for tree in (frozen, new)]
        check(f'{game_id}: the OV-1 series over all draws, line by line', every[0], every[1],
              f' ({len(every[0])} and {len(every[1])} lines)')
        (frozen_reports, reworded), new_reports = frozen_report_files(frozen, game_id), report_files(new, game_id)
        check(f'{game_id}: the names of the report files', sorted(frozen_reports), sorted(new_reports),
              f' ({len(frozen_reports)} and {len(new_reports)})')
        unlike = [name for name in sorted(set(frozen_reports) & set(new_reports))
                  if frozen_reports[name] != new_reports[name]]
        check(f'{game_id}: every report file, byte for byte (league, next draw, both OV-1 print-outs, README)',
              unlike, [], f' (the frozen engine\'s given the new wording: {reworded} replacements of '
                          f'{len(WORDING_CHANGES)} declared kinds)' + (f'; differing: {", ".join(unlike[:10])}'
                                                                     if unlike else ''))
    say(f'RESULT: {"SAME" if same else "DIFFERENT"}: the frozen engine at {frozen} and the simplified engine at '
        f'{new}')
    return same


def without_comments(source: bytes) -> str:
    """A Python file's program with its comments and docstrings taken out, as one text to compare."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        body = getattr(node, 'body', None)
        if (isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and body
                and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            node.body = body[1:] or [ast.Pass()]
    return ast.dump(tree)


def compare_code(frozen: Path, new: Path, say=print) -> None:
    """List every source file of the two trees' engines and methods by how it differs."""
    def files(tree: Path) -> dict:
        """{path from src: bytes} for every file of the engine and the methods, caches and flags left out."""
        found = {}
        for path in sorted((tree / 'src').rglob('*')):
            relative = path.relative_to(tree / 'src').as_posix()
            if (path.is_file() and '__pycache__' not in relative and '/contract_data/' not in relative
                    and path.name not in ('VARIANT_STATUS.ini', 'I_AM_INSTALLABLE', 'I_AM_RETIRED',
                                          'IN_PLACE_SINCE')):
                found[relative] = path.read_bytes()
        return found

    frozen_files, new_files = files(frozen), files(new)
    groups = {'the same bytes': [], 'the same program (comments and docstrings differ)': [], 'changed': [],
              'only in the simplified engine': sorted(set(new_files) - set(frozen_files)),
              'only in the frozen tree': sorted(set(frozen_files) - set(new_files))}
    for name in sorted(set(frozen_files) & set(new_files)):
        if frozen_files[name] == new_files[name]:
            groups['the same bytes'].append(name)
        elif name.endswith('.py') and without_comments(frozen_files[name]) == without_comments(new_files[name]):
            groups['the same program (comments and docstrings differ)'].append(name)
        else:
            groups['changed'].append(name)
    for title, names in groups.items():
        methods = [name for name in names if name.startswith('methods/') and not name.startswith('methods/_common/')]
        engine = [name for name in names if name not in methods]
        say(f'{title}: {len(engine)} engine files, {len(methods)} method and helper files')
        if title != 'the same bytes' or len(engine) <= 40:
            for name in engine if title != 'only in the frozen tree' else [n for n in engine
                                                                           if n.startswith('research')]:
                say(f'    {name}')
        if methods and title not in ('the same bytes', 'only in the frozen tree'):
            for name in methods:
                say(f'    {name}')


def copy_parts(source: Path, tree: Path, parts) -> None:
    """Copy the named files and folders of a source folder into a new tree, Python's caches left out."""
    for part in parts:
        origin, destination = source / part, tree / part
        destination.parent.mkdir(parents=True, exist_ok=True)
        if origin.is_dir():
            shutil.copytree(origin, destination, ignore=shutil.ignore_patterns('__pycache__', 'VARIANT_STATUS.ini',
                                                                               'IN_PLACE_SINCE', 'I_AM_RETIRED'))
        else:
            shutil.copyfile(origin, destination)


def invented(folder: Path, frozen_from: Path, new_from: Path, draws: int) -> bool:
    """The whole comparison on invented results. Returns True if both comparisons came out the same."""
    folder = folder.resolve()
    if folder.exists() and any(folder.iterdir()):
        print(f'REFUSED: {folder} is not empty. Give a folder that does not exist yet.')
        return False
    frozen, new = folder / 'frozen_DEV', folder / 'new_DEV'
    copy_parts(frozen_from, frozen, FROZEN_PARTS)
    copy_parts(new_from, new, NEW_PARTS)
    # Each tree's settings file in its own engine's form: the frozen engine's first form, and the scheme's.
    (frozen / 'ENVIRONMENT.ini').write_bytes(
        f'[environment]\r\nrole = DEV\r\ntree_root = {frozen}\r\nvenv_dir = {frozen / ".venv"}\r\n'.encode('ascii'))
    places = {'DEV': new, 'QA': folder / 'no_such_tree_QA', 'PROD': folder / 'no_such_tree_PROD'}
    (new / 'ENVIRONMENT.ini').write_bytes(('[environment]\r\nrole = DEV\r\n' + ''.join(
        f'[{role}]\r\ntree_root = {place}\r\nbackup_root = {folder / "backups" / role}\r\n'
        for role, place in places.items())).encode('ascii'))
    if in_tree(new, INVENT_RESULTS, str(draws)):
        return False
    shutil.copytree(new / 'source_data', frozen / 'source_data')
    job = ('--game', 'BOTH', '--no-update')
    for step in ('the fill', 'the second OV-1 series from the same starting draws'):
        for tree in (frozen, new):
            if in_tree(tree, RUN_JOB, *job):
                print(f'STOP: the job in {tree} did not finish cleanly ({step}).')
                return False
        if step == 'the fill' and (in_tree(frozen, ALIGN_FROZEN) or in_tree(new, ALIGN_NEW)):
            return False
    compare_code(frozen, new)
    return compare_trees(frozen, new)


def main(arguments) -> int:
    """The command line. Returns 0 if what was asked came out the same (or was done), 1 if not."""
    parser = argparse.ArgumentParser(prog='compare_with_frozen.py', description=__doc__.split('\n')[0])
    commands = parser.add_subparsers(dest='command', required=True)
    run = commands.add_parser('run')
    run.add_argument('tree', type=Path)
    run.add_argument('job_arguments', nargs=argparse.REMAINDER)
    for name in ('align', 'trees', 'code'):
        two = commands.add_parser(name)
        two.add_argument('frozen', type=Path)
        two.add_argument('new', type=Path)
    made_up = commands.add_parser('invented')
    made_up.add_argument('folder', type=Path)
    made_up.add_argument('--frozen-from', type=Path, default=Path(__file__).resolve().parents[2],
                         help='the repository\'s top level (default: two folders above this file\'s folder)')
    made_up.add_argument('--new-from', type=Path, default=Path(__file__).resolve().parents[1],
                         help='the tree of the simplified engine (default: the tree this file lies in)')
    made_up.add_argument('--draws', type=int, default=10, help='draws every method is scored on (default 10)')
    chosen = parser.parse_args(arguments)
    if chosen.command == 'run':
        return in_tree(chosen.tree.resolve(), RUN_JOB, *chosen.job_arguments)
    if chosen.command == 'invented':
        return 0 if invented(chosen.folder, chosen.frozen_from, chosen.new_from, chosen.draws) else 1
    frozen, new = chosen.frozen.resolve(), chosen.new.resolve()
    if chosen.command == 'align':
        return 1 if in_tree(frozen, ALIGN_FROZEN) or in_tree(new, ALIGN_NEW) else 0
    if chosen.command == 'code':
        compare_code(frozen, new)
        return 0
    return 0 if compare_trees(frozen, new) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
