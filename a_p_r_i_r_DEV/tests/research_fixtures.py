"""Fixtures for the research engine's tests: invented trees, invented draws and toy variants.

What this file is for
    The engine's tests run on disposable trees made here: a settings file, results files of invented draws (made
    by a seeded generator, never real draws) with their version ledgers, and toy methods whose behaviour at
    chosen targets is planted (a failure of the method's own mathematics, a fault, too little history, a bad
    output, a verify that disagrees).

Which part of the scheme it carries out
    exchange/Claude_The_Simple_Scheme_v0_2_20261126.md section 9 (tests on invented games and toy methods).

Which of the project's own modules it uses
    _common.game_profiles    get_profile: the two games' first draws, barrels and draw dates
    research.reader          header_for: the results file's columns

What uses it
    tests/test_research_*.py.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import random
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from _common.game_profiles import get_profile
from research.reader import header_for

# The fixed time every test job runs at, so that two runs of the same work write the same bytes.
FIXED_TIME = datetime(2026, 12, 1, 9, 40, 12, tzinfo=timezone.utc)
# The game most tests use, and the first target of a toy variant that declares three earlier draws in it.
GAME = 'POWERBALL'
FIRST_TOY_TARGET = 1147
# The last draw on file when a job test's tree is made, and after new results have "arrived" in a test.
LAST_AT_START = 1160
LAST_AFTER_NEW = 1166
# The one file every invented tree holds as "the engine": changing it changes the infrastructure's fingerprint.
ENGINE_FILE = 'toy_engine.py'
# The version ledger's columns as the fixtures write them (the reader uses the first six).
LEDGER_COLUMNS = ('version', 'utc', 'action', 'master_sha256', 'first_draw', 'last_draw', 'draw_count')
# The toy method every toy variant uses; BEHAVIOUR is replaced by the planted behaviour of each variant.
TOY_METHOD = '''"""A toy method for the engine's tests: it scores each number by how often it was drawn before the target."""
from _common.contract_forecast import BarrelOutput, MethodOutput, ScoredRanking
from _common.game_profiles import get_profile
from research.method_api import MethodFailed

BEHAVIOUR = @@BEHAVIOUR@@


def _counts(task, view):
    """{barrel: {number: how often it was drawn in the earlier draws}}."""
    rows = view.simple_rows()
    out = {}
    for barrel in get_profile(task.game_id).barrels:
        counts = {j: 0 for j in range(barrel.low, barrel.high + 1)}
        for row in rows:
            for number in (row['main'] if barrel.barrel_id == 'MAIN' else [row['powerball']]):
                counts[number] += 1
        out[barrel.barrel_id] = counts
    return out


def _scores(counts):
    """The toy's score for each number of one barrel, from the counts: the count times the planted 'scale'. With
    'reverse' planted a number scores by how far it is below the largest count (the order the other way round);
    with 'rotate': k planted, number j takes the count of the number k places further on (another order again)."""
    numbers = sorted(counts)
    turn, most = BEHAVIOUR.get('rotate', 0), max(counts.values())
    turned = {j: counts[numbers[(index + turn) % len(numbers)]] for index, j in enumerate(numbers)}
    return {j: BEHAVIOUR.get('scale', 1.0) * ((most - c) if BEHAVIOUR.get('reverse') else c) for j, c in turned.items()}


def compute(task, view):
    """The toy forecast, or the behaviour planted for this target."""
    target = task.target_draw_number
    if target in BEHAVIOUR.get('crash_at', ()):
        raise RuntimeError('toy: an environmental fault')
    if target in BEHAVIOUR.get('fail_at', ()):
        raise MethodFailed('toy: no fit can be made at this target')
    if len(view.draw_number) < BEHAVIOUR.get('short_below', 0):
        return MethodOutput(barrels={})
    counts = _counts(task, view)
    if target in BEHAVIOUR.get('bad_output_at', ()):
        counts.pop('MAIN')
    return MethodOutput(barrels={barrel: BarrelOutput(ranking=ScoredRanking(_scores(s)))
                                 for barrel, s in counts.items()})


def verify(task, view, forecast, diagnostic):
    """Recompute and compare, or the disagreement planted for this target."""
    if task.target_draw_number in BEHAVIOUR.get('verify_fail_at', ()):
        raise ValueError('toy: verify disagrees')
    if len(view.draw_number) < BEHAVIOUR.get('short_below', 0):
        if forecast['record_status'] != 'INSUFFICIENT_HISTORY':
            raise ValueError('toy: too few draws, but the record is not INSUFFICIENT_HISTORY')
        return
    for barrel, s in _counts(task, view).items():
        expected = _scores(s)
        if forecast['barrels'][barrel]['scores'] != [expected[j] for j in sorted(expected)]:
            raise ValueError('toy: the record differs from the recomputation')
'''


def invented_row(game_id: str, draw: int, seed) -> str:
    """One invented results row for a draw, from a seeded generator (never a real draw).

    For example invented_row('POWERBALL', 1144, 1) is '1144,2018-04-19,' and eight invented numbers.
    """
    profile = get_profile(game_id)
    rng = random.Random(f'{game_id}:{seed}:{draw}')
    main_high = profile.barrels[0].high
    main = rng.sample(range(1, main_high + 1), 7)
    if game_id == 'POWERBALL':
        extra = [rng.randint(1, 20)]
    else:
        extra = rng.sample([n for n in range(1, main_high + 1) if n not in main], 3)
    return ','.join([str(draw), profile.derived_date(draw).isoformat()] + [str(n) for n in main + extra])


def results_bytes(game_id: str, last_draw: int, seed=1, reseed_from: int | None = None, reseed=2) -> bytes:
    """The bytes of an invented results file from the game's first draw to last_draw.

    seed: the generator's seed.  reseed_from, reseed: draws at and after reseed_from are generated with the
    other seed (a results file "changed at and after" that draw).
    """
    profile = get_profile(game_id)
    rows = [','.join(header_for(game_id))]
    for draw in range(profile.first_draw, last_draw + 1):
        rows.append(invented_row(game_id, draw, reseed if reseed_from is not None and draw >= reseed_from else seed))
    return ('\n'.join(rows) + '\n').encode('ascii')


def write_results(tree: Path, game_id: str, last_draw: int, version: int = 1, **generator) -> bytes:
    """Write an invented results file and its version ledger into a tree; return the results bytes.

    tree: the tree's folder.  last_draw: the last draw on file.  version: the version the ledger's last row
    gives.  generator: results_bytes' other arguments.
    """
    raw = results_bytes(game_id, last_draw, **generator)
    folder = tree / 'source_data'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f'{game_id}_results_master.csv').write_bytes(raw)
    profile = get_profile(game_id)
    ledger = [','.join(LEDGER_COLUMNS)]
    for v in range(1, version + 1):
        sha = hashlib.sha256(raw).hexdigest() if v == version else '0' * 64
        ledger.append(','.join([str(v), '2026-01-01T00:00:00+00:00', 'INIT' if v == 1 else 'UPDATE', sha,
                                str(profile.first_draw), str(last_draw), str(last_draw - profile.first_draw + 1)]))
    (folder / f'{game_id}_results_master_ledger.csv').write_bytes(('\n'.join(ledger) + '\n').encode('ascii'))
    return raw


def make_tree(root: Path, role: str = 'DEV') -> Path:
    """Make an empty invented tree: its settings file, one invented file of "the engine" (so that a test can
    change the engine's fingerprint) and the folders the engine expects.

    root: an existing empty folder.  role: 'DEV', 'QA' or 'PROD'.  Returns the tree's real path.
    """
    tree = Path(root).resolve()
    (tree / 'src' / 'methods').mkdir(parents=True)
    (tree / '.venv').mkdir()
    (tree / 'src' / ENGINE_FILE).write_text('# an invented file of the engine\n', encoding='ascii')
    lines = ['[environment]', f'role = {role}', f'tree_root = {tree}', f'venv_dir = {tree / ".venv"}']
    if role != 'DEV':
        backups = tree.parent / (tree.name + '_backups')
        backups.mkdir(exist_ok=True)
        lines.append(f'backup_root = {backups}')
    (tree / 'ENVIRONMENT.ini').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return tree


def add_toy_variant(tree: Path, family: str, variant: str, games=('POWERBALL', 'OZLOTTO'), minimum: int = 3,
                    behaviour: dict | None = None, helpers=()) -> Path:
    """Add a toy variant folder (method.py and VARIANT.json) to a tree; return the folder.

    family, variant: for example 'E_901' and 'TOY_COUNTS_V1'.  minimum: the earlier draws it declares it needs.
    behaviour: what is planted, by target: {'fail_at': [...], 'crash_at': [...], 'bad_output_at': [...],
    'verify_fail_at': [...], 'short_below': n, 'scale': x, 'reverse': True, 'rotate': k}.  helpers: helper paths
    its declaration lists.
    """
    folder = tree / 'src' / 'methods' / family / variant
    folder.mkdir(parents=True)
    (folder.parent / '__init__.py').write_text('"""An invented family for the engine\'s tests."""\n', encoding='ascii')
    (folder / 'method.py').write_text(TOY_METHOD.replace('@@BEHAVIOUR@@', repr(behaviour or {})), encoding='ascii')
    declaration = {'family': family, 'variant': variant, 'title': f'{family} - a toy method',
                   'description': 'Counts how often each number was drawn. Invented, for tests.',
                   'games': list(games), 'minimum_earlier_draws': {g: minimum for g in games},
                   'observation_view': 'UNORDERED_SET', 'files': ['method.py'], 'helpers': list(helpers)}
    (folder / 'VARIANT.json').write_text(json.dumps(declaration, indent=2) + '\n', encoding='ascii')
    return folder


class ImportPath:
    """Puts an invented tree's src/methods first on Python's import path for a test, and takes it and every toy
    module off again afterwards, so that two trees with a family of the same name never mix.

    Use:  with ImportPath(tree): ...
    """

    def __init__(self, tree: Path):
        """tree: the invented tree whose variants the test imports."""
        self.methods_root = str(tree / 'src' / 'methods')

    def __enter__(self):
        """Put the tree's methods folder first on the import path."""
        self._forget()
        sys.path.insert(0, self.methods_root)
        importlib.invalidate_caches()
        return self

    def __exit__(self, *exc):
        """Take the folder off the import path and forget every toy module."""
        sys.path.remove(self.methods_root)
        self._forget()
        return False

    @staticmethod
    def _forget():
        """Forget every imported toy family (E_9xx), so that the next tree imports its own files."""
        for name in [n for n in sys.modules if n.startswith('E_9')]:
            del sys.modules[name]
        importlib.invalidate_caches()


def run_job(tree: Path, games=(GAME,), **options) -> tuple:
    """Run the research job in an invented tree at the fixed time.

    tree: the tree.  games: the games to work.  options: run()'s other arguments (no_update, rebuild,
    rebuild_all, checkpoint); the updater is left out unless a test says otherwise.
    Returns (the exit code, the lines the job said), for example (0, ['RESEARCH JOB - START - ...', ...]).
    """
    from research import research_job
    said = []
    with ImportPath(tree):
        code = research_job.run(tree, games, now=lambda: FIXED_TIME, say=said.append,
                                **{'no_update': True, **options})
    return code, said


def files_under(tree: Path, folder: str = 'results/research', leave_out=('made_times.csv',)) -> dict:
    """Every file under a folder of a tree with its bytes: {path from the tree, forward slashes: bytes}.

    leave_out: file names not to include (the side file of making times, by default).
    """
    top = tree / folder
    return {path.relative_to(tree).as_posix(): path.read_bytes() for path in sorted(top.rglob('*'))
            if path.is_file() and path.name not in leave_out}


def list_lines(tree: Path, family: str, variant: str, which: str = 'forecasts', game_id: str = GAME) -> list:
    """The lines of a variant's list after the header, as records; which is 'forecasts' or 'scores'."""
    path = tree / 'results' / 'research' / game_id / 'variants' / family / variant / f'{which}.jsonl'
    return [json.loads(line) for line in path.read_text(encoding='ascii').splitlines()][1:] if path.is_file() else []


def ledger_lines(tree: Path, game_id: str = GAME, which: str = 'prevailing') -> list:
    """The lines of one of a game's two OV-1 series after the header, as records ([] if the file is not there);
    which is 'prevailing' (each method from its establishment draw) or 'exploratory' (every draw)."""
    path = tree / 'results' / 'research' / game_id / 'ov1' / f'{which}.jsonl'
    return [json.loads(line) for line in path.read_text(encoding='ascii').splitlines()][1:] if path.is_file() else []


def alter_list_line(path: Path, position: int, change) -> None:
    """Alter one line of a list file, leaving every other byte as it was.

    path: the list file.  position: which line after the header, from 0.  change: called with that line's record,
    which it alters in place.
    """
    from research.variant_lists import record_bytes
    records = [json.loads(line) for line in path.read_text(encoding='ascii').splitlines()]
    change(records[position + 1])
    path.write_bytes(b''.join(record_bytes(record) for record in records))


def make_folder_link(link: Path, target: Path) -> str | None:
    """Make `link` a name for the folder `target`, as an accident or a tool might: a symbolic link where the
    account may make one, otherwise (on Windows) a junction.

    Returns 'symbolic link' or 'junction', or None if this machine allows neither (the test then skips).
    """
    try:
        os.symlink(target, link, target_is_directory=True)
        return 'symbolic link'
    except (OSError, NotImplementedError):
        pass
    try:
        import _winapi
        _winapi.CreateJunction(str(target), str(link))
        return 'junction'
    except (ImportError, AttributeError, OSError):
        return None


def read_last_draw(tree: Path, game_id: str = GAME) -> int:
    """The last draw of the results a tree holds for a game, read from the results file's last row."""
    rows = (tree / 'source_data' / f'{game_id}_results_master.csv').read_text(encoding='ascii').splitlines()
    return int(rows[-1].split(',')[0])


def method_folder(tree: Path, family: str, variant: str) -> Path:
    """A method's own folder in a tree, where its software and its small files lie."""
    return tree / 'src' / 'methods' / family / variant


def set_in_place(tree: Path, family: str, variant: str, since: int, game_id: str = GAME) -> None:
    """Write a method's IN_PLACE_SINCE as if this version of it had first been used when the tree held results
    through `since`: it then counts in the second OV-1 series from the draw after."""
    from research.method_flags import IN_PLACE_NAME, write_flag
    from research.variant_folders import read_variant
    folder = method_folder(tree, family, variant)
    write_flag(folder / IN_PLACE_NAME, {'fingerprint': read_variant(tree / 'src' / 'methods', family, variant).fingerprint,
                                        f'in_place_since_{game_id}': str(since)}, 'Written by a test.')


def report_text(tree: Path, name: str, game_id: str = GAME) -> str:
    """The text of one report file of a game, by its name from the reports folder, for example
    'league/league_POWERBALL_d01161.txt'."""
    return (tree / 'results' / 'research' / game_id / 'reports' / name).read_text(encoding='ascii')


class JobCase(unittest.TestCase):
    """A temporary folder in which each test makes its invented trees."""

    def setUp(self):
        """Make the folder; the trees are made by each test."""
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name).resolve()

    def tearDown(self):
        """Remove the folder."""
        self._temporary.cleanup()

    def tree(self, variants=('TOY_A_V1', 'TOY_B_V1'), role: str = 'DEV', last_draw: int = LAST_AT_START,
             name: str = 'tree') -> Path:
        """Make a tree with invented results and toy methods of family E_901. Returns its folder.

        variants: names, or (name, behaviour) pairs; TOY_B_V1 is given the reversed order unless a behaviour is
        named.
        """
        folder = self.root / name
        folder.mkdir()
        tree = make_tree(folder, role=role)
        write_results(tree, GAME, last_draw)
        for entry in variants:
            self.add_variant(tree, *((entry,) if isinstance(entry, str) else entry))
        return tree

    @staticmethod
    def add_variant(tree: Path, name: str, behaviour: dict | None = None, family: str = 'E_901',
                    games=(GAME,), minimum: int = 3) -> None:
        """Add one toy method."""
        if behaviour is None:
            behaviour = {'reverse': True} if name == 'TOY_B_V1' else {}
        add_toy_variant(tree, family, name, games=games, minimum=minimum, behaviour=behaviour)

    def status(self, tree: Path, name: str, family: str = 'E_901'):
        """A method's status in the test game, read from the small files in its folder."""
        from research.method_flags import status_of
        return status_of(method_folder(tree, family, name), GAME)
