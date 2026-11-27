"""Compare the results updater of this tree with the first system's reviewed updater.

What this file is for
    The simple scheme keeps the reviewed updater "with every Mode H state taken out and nothing else changed".
    This tool shows it in two ways, and reaches no website in either:
      1. Definition by definition: every function, method, class and constant of the new updater is the frozen
         one's, comments apart, except a short declared list (each changed only by taking a Mode H state out),
         and the frozen updater has nothing more than a declared list of what was removed.
      2. By running both on the same invented pages: in each of a dozen situations (new draws, nothing new, a
         draw that disagrees, a gap, a page that cannot be read, a lock left behind, a results file edited by
         hand ...) both must end the same way, with the same message, and leave the same results file, ledger
         lines, grab and backup. The frozen updater is given invented owner records that put it in its ordinary
         state after Mode H (holdout opened and sealed), which is the state the new updater is always in.
    The pages are made from invented draws by a formula; no real draw is read. In both updaters the class that
    starts a real browser is replaced, for the length of the comparison, by one that refuses.

    Command:  compare_updater_with_frozen.py [the frozen updater's file]
              (default: src/results_master_v0_2.py two folders above this file's folder)

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 8.

Which of the project's own modules it uses
    none by import: it loads the two updaters from their files, each under a name of its own.

What uses it
    the people and the task files that make the comparison, and tests/test_research_updater.py.
"""
from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import json
import re
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

NEW_FILE = Path(__file__).resolve().parents[1] / 'src' / 'updater' / 'results_updater.py'
FROZEN_FILE = Path(__file__).resolve().parents[2] / 'src' / 'results_master_v0_2.py'
# The definitions of the new updater that may differ from the frozen one's, each because a Mode H state was
# taken out of it (or, for the version and the command line, because the program is no longer the same edition).
CHANGED = ('BrowserFetcher.fetch', 'Store.__init__', 'Store.load_verified_master', 'TOOL_VERSION', 'check_constants',
           'cmd_update', 'main', 'parse_gov', 'update_game', 'validate_draw', 'validate_series')
# What the frozen updater has and the new one has not: the Mode H states, the one-off "init" and the self-test.
REMOVED = ('ADVANCE_SCHEMA', 'BATCH_ID_SCHEMA', 'FIRST_QUARANTINED_DRAW', 'HOLDOUT_DRAWS', 'OLD_HISTORY', 'OLD_ORDER',
           'OLD_POWERBALL_COMMIT', 'QUARANTINE_START_DATE', 'SEAL_SCHEMA', '_owner_json', 'cmd_init', 'freeze_state',
           'holdout_last', 'holdout_opened', 'mode_h_sealed', 'old_powerball_dev_rows', 'read_build_run',
           'read_lott_check_run', 'self_test', 'session_lock_present', 'study_version_advance')
# The day every invented update is made on, and the last draw each invented tree holds before it.
TODAY = date(2027, 1, 20)
HELD = {'POWERBALL': 1590, 'OZLOTTO': 1700}
# The time stamp in the name of a grab or a backup, which differs from run to run.
STAMP = re.compile(r'_as_at_\d{8}_\d{6}Z')
# Ledger columns that differ by design: the time, and which program wrote the line.
LEDGER_COLUMNS_LEFT_OUT = ('utc', 'tool_version', 'tool_sha256')


def load(path: Path, name: str):
    """Load an updater from its file as a module of the given name, and replace its real fetcher by one that
    refuses, so that nothing in this comparison can start a browser."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

    class NoBrowser:
        """Stands in for the real fetcher: the comparison never fetches."""

        def __init__(self, *arguments):
            """Refuse to be made."""
            raise RuntimeError('the comparison never starts a browser')

    module.BrowserFetcher = NoBrowser
    return module


def definitions(path: Path) -> dict:
    """{name: its program text without comments} for every top-level function, constant and class of a Python
    file; a class's methods are given apart, as 'Class.method', and the class as what is left without them."""
    def bare(node) -> str:
        """A definition as text, docstrings taken out."""
        for inner in ast.walk(node):
            body = getattr(inner, 'body', None)
            if (isinstance(inner, (ast.ClassDef, ast.FunctionDef)) and body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)):
                inner.body = body[1:] or [ast.Pass()]
        return ast.dump(node)

    found = {}
    for node in ast.parse(path.read_bytes()).body:
        if isinstance(node, ast.FunctionDef):
            found[node.name] = bare(node)
        elif isinstance(node, ast.ClassDef):
            methods = [inner for inner in node.body if isinstance(inner, ast.FunctionDef)]
            for method in methods:
                found[f'{node.name}.{method.name}'] = bare(method)
            node.body = [inner for inner in node.body if inner not in methods] or [ast.Pass()]
            found[node.name] = bare(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    found[target.id] = ast.dump(node)
    return found


def compare_definitions(frozen_file: Path, new_file: Path, say=print) -> bool:
    """Part 1. Says what is the same, what is changed and what was removed; returns True if the changed and the
    removed are exactly the declared lists and the new updater has nothing the frozen one has not."""
    frozen, new = definitions(frozen_file), definitions(new_file)
    same = sorted(name for name in new if name in frozen and new[name] == frozen[name])
    changed = sorted(name for name in new if name in frozen and new[name] != frozen[name])
    removed, added = sorted(set(frozen) - set(new)), sorted(set(new) - set(frozen))
    say(f'{len(same)} definitions of the new updater are the frozen updater\'s, comments apart: {", ".join(same)}')
    say(f'{len(changed)} are changed: {", ".join(changed)}')
    say(f'{len(removed)} of the frozen updater are not in the new one: {", ".join(removed)}')
    say(f'{len(added)} are in the new updater only: {", ".join(added) or "none"}')
    as_declared = changed == sorted(CHANGED) and removed == sorted(REMOVED) and not added
    say(('SAME       ' if as_declared else 'DIFFERENT  ') + 'the changed and the removed definitions are exactly the '
        'declared lists (CHANGED and REMOVED in this tool)')
    return as_declared


def invented_draw(game: str, number: int) -> tuple:
    """An invented draw by a formula (never a real one): (the seven main numbers, the secondary numbers)."""
    highest = 35 if game == 'POWERBALL' else 47
    main = []
    for k in range(7):
        x = ((number * 7 + k * 5) % highest) + 1
        while x in main:
            x = x % highest + 1
        main.append(x)
    if game == 'POWERBALL':
        return main, [(number % 20) + 1]
    secondary, x = [], (number * 3) % 47 + 1
    while len(secondary) < 3:
        if x not in main and x not in secondary:
            secondary.append(x)
        x = x % 47 + 1
    return main, secondary


class InventedPages:
    """A fetcher that reads invented results pages instead of the website, for one updater.

    plant: None, or what is wrong with the pages: ('differs', draw) the main numbers of that draw are in another
    order; ('skipped', draw) the page leaves that draw out; ('repeated', draw) that draw shows a number twice;
    ('label', draw) the label before that draw's secondary numbers is missing.
    """

    def __init__(self, module, plant=None):
        """module: the updater whose own page parser reads the pages."""
        self.module, self.plant = module, plant

    def fetch(self, game, a, b, **mode_h):
        """The draws the invented page for a game and the dates a..b shows, read by the updater's own parser.
        mode_h: what the frozen updater passes besides (its quarantine switch), handed on unchanged."""
        module, lines, number = self.module, [], self.module.ERAS[game].first_draw
        what, which = self.plant or (None, None)
        while module.derived_date(game, number) <= b:
            day = module.derived_date(game, number)
            if a <= day <= b and not (what == 'skipped' and number == which):
                main, secondary = invented_draw(game, number)
                if number == which and what == 'differs':
                    main = main[1:] + main[:1]
                if number == which and what == 'repeated':
                    main = main[:6] + main[:1]
                label = 'Powerball:' if game == 'POWERBALL' else 'Supplementary numbers:'
                heading = f'{day.strftime("%A")} {day.day} {module.MONTH_NAMES[day.month - 1]} {day.year}'
                lines += [f'Draw {number}', heading, 'Winning numbers:', *map(str, main),
                          *([] if number == which and what == 'label' else [label]), *map(str, secondary),
                          'View prizes']
            number += 1
        return module.parse_gov(game, '\n'.join(lines), a, b, **mode_h)


def make_tree(module, folder: Path, held: dict, frozen: bool) -> Path:
    """An invented tree holding each game's results through held[game], written by the updater's own functions.
    For the frozen updater the owner records of an opened and sealed holdout are planted too (invented, and
    holding no draw value), so that it is in its ordinary state after Mode H."""
    for game in module.ERAS:
        draws = [module.Draw(game, number, module.derived_date(game, number).isoformat(),
                             *(tuple(part) for part in invented_draw(game, number)))
                 for number in range(module.ERAS[game].first_draw, held[game] + 1)]
        store = module.Store(folder, game)
        store.dir.mkdir(parents=True, exist_ok=True)
        digest = module.write_new(store.master, module.to_csv_bytes(game, draws))
        store.append_ledger({'version': 1, 'utc': 't', 'action': 'INIT', 'master_sha256': digest,
                             'first_draw': draws[0].number, 'last_draw': held[game], 'draw_count': len(draws),
                             'added_count': len(draws), 'tool_version': 'invented'})
        if frozen:
            batch = 'wf-' + '0' * 32
            holdout = folder / 'results' / 'real' / 'holdout'
            (holdout / 'wf_batches' / game / batch).mkdir(parents=True)
            (holdout / game).mkdir(parents=True)
            for path, record in (
                    (folder / 'source_data' / f'HOLDOUT_OPENED_{game}.json',
                     {'schema': 'HOLDOUT_OPENED_V1', 'game': game, 'opened_utc': 'x', 'study_manifest_sha256': 'b' * 64,
                      'owner_statement': 'opened', 'freeze_version': 1, 'freeze_master_sha256': digest}),
                    (holdout / game / 'MODE_H_BATCH_ID.json',
                     {'schema': module.BATCH_ID_SCHEMA, 'game_id': game, 'batch_id': batch}),
                    (holdout / 'wf_batches' / game / batch / 'MODE_H_SEALED.json',
                     {'schema': module.SEAL_SCHEMA, 'batch_id': batch})):
                path.write_bytes(json.dumps(record).encode('ascii'))
    return folder


def run_update(module, tree: Path, games, months_back: int, plant=None, pause: float = 2.0) -> tuple:
    """Run an updater's update in a tree on invented pages. Returns (how it ended, what it printed): how it
    ended is ('returned', 0) or (the refusal's kind, its message), time stamps taken out."""
    printed = io.StringIO()
    try:
        with contextlib.redirect_stdout(printed):
            code = module.cmd_update(tree, list(games), months_back, 'chrome', pause,
                                     fetcher_factory=lambda: InventedPages(module, plant), today=TODAY)
        ended = ('returned', code)
    except (module.Refused, module.Stop, module.VerifyFail) as refusal:
        ended = (type(refusal).__name__, STAMP.sub('_as_at_<T>', str(refusal)))
    return ended, STAMP.sub('_as_at_<T>', printed.getvalue())


def what_a_tree_holds(module, tree: Path) -> dict:
    """Everything an updater keeps in a tree's source_data, in a form two trees can be compared by: each results
    file's bytes; each ledger line without its time and the writing program's version; each grab and backup by
    its name (time stamp taken out) and bytes; whether the lock was left behind."""
    held = {'lock left behind': (tree / 'source_data' / '.results_master.lock').exists()}
    for game in module.ERAS:
        store = module.Store(tree, game)
        held[game] = {
            'results file': store.master.read_bytes(),
            'ledger': [{key: STAMP.sub('_as_at_<T>', value) for key, value in row.items()
                        if key not in LEDGER_COLUMNS_LEFT_OUT} for row in store.ledger_rows()],
            'grabs and backups': sorted((STAMP.sub('_as_at_<T>', path.name), path.read_bytes())
                                        for folder in (store.grabs, store.backups) if folder.is_dir()
                                        for path in folder.iterdir() if path.name.startswith(game + '_'))}
    return held


def compare_behaviour(frozen, new, say=print) -> bool:
    """Part 2. Runs both updaters through the situations below; says one line for each; returns True if in every
    one both ended the same way, printed the same and left the same files."""
    situations = (
        ('new draws arrive for both games', {}),
        ('then the same again: nothing new', {'after': 'new draws arrive for both games'}),
        ('a wider window: thirty months, in several searches that overlap', {'months_back': 30}),
        ('one game only', {'games': ('OZLOTTO',)}),
        ('a draw the tree holds reads differently on the page', {'plant': ('differs', 1585), 'games': ('POWERBALL',)}),
        ('the tree\'s results end long before the window', {'held': {'POWERBALL': 1500, 'OZLOTTO': 1650}}),
        ('the page leaves out a draw', {'plant': ('skipped', 1595), 'games': ('POWERBALL',)}),
        ('a draw on the page shows a number twice', {'plant': ('repeated', 1593), 'games': ('POWERBALL',)}),
        ('the label before the secondary numbers is missing', {'plant': ('label', 1702), 'games': ('OZLOTTO',)}),
        ('the updater\'s lock was left behind', {'lock': True}),
        ('the results file was edited outside the updater', {'edited': 'OZLOTTO'}),
        ('a pause shorter than the least allowed', {'pause': 1.0}),
    )
    all_same = True
    with tempfile.TemporaryDirectory() as folder:
        kept = {}
        for index, (title, how) in enumerate(situations):
            results = []
            for which, module in (('frozen', frozen), ('new', new)):
                if 'after' in how:
                    tree = kept[how['after'], which]
                else:
                    tree = make_tree(module, Path(folder) / f'{index}_{which}', how.get('held', HELD),
                                     which == 'frozen')
                kept[title, which] = tree
                if how.get('lock'):
                    (tree / 'source_data' / '.results_master.lock').write_bytes(b'x')
                if how.get('edited'):
                    master = module.Store(tree, how['edited']).master
                    data = bytearray(master.read_bytes())
                    data[-5] = ord('9') if data[-5] != ord('9') else ord('8')
                    master.write_bytes(bytes(data))
                ended, printed = run_update(module, tree, how.get('games', tuple(module.ERAS)),
                                            how.get('months_back', 5), how.get('plant'), how.get('pause', 2.0))
                results.append((ended, printed, what_a_tree_holds(module, tree)))
            if 'after' not in how and any('after' in later for _, later in situations[index + 1:index + 2]):
                time.sleep(1.1)                 # a grab's name carries the second it was made in
            same = results[0] == results[1]
            all_same = all_same and same
            ended = results[1][0]
            lines = sum(len(results[1][2][game]['ledger']) for game in new.ERAS)
            say(('SAME       ' if same else 'DIFFERENT  ') + f'{title}: the new updater '
                + ('finished' if ended[0] == 'returned' else f'ended with {ended[0]} ("{ended[1][:70]}...")')
                + f'; ledger lines in the tree afterwards: {lines}')
    return all_same


def main(arguments) -> int:
    """The command line. Returns 0 if both parts came out the same, 1 if not."""
    frozen_file = Path(arguments[0]).resolve() if arguments else FROZEN_FILE
    print(f'The frozen updater: {frozen_file}')
    print(f'The new updater:    {NEW_FILE}')
    definitions_same = compare_definitions(frozen_file, NEW_FILE)
    behaviour_same = compare_behaviour(load(frozen_file, 'frozen_updater'), load(NEW_FILE, 'new_updater'))
    same = definitions_same and behaviour_same
    print(f'RESULT: {"SAME" if same else "DIFFERENT"}: the new updater is the frozen updater with its Mode H states '
          f'taken out' + ('' if same else '; see the lines that say DIFFERENT'))
    return 0 if same else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
