"""Fixtures for the research engine's tests: invented trees, invented draws and toy variants.

What this file is for
    The engine's tests run on disposable trees made here: a settings file, a small infrastructure manifest,
    results files of invented draws (made by a seeded generator, never real draws) with their version ledgers,
    and toy variants whose behaviour at chosen targets is planted (a failure of the method's own mathematics, an
    environmental fault, too little history, a bad output, a verify that disagrees).

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 18 ("on invented games and toy variants").

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
import random
import sys
from pathlib import Path

from _common.game_profiles import get_profile
from research.reader import header_for

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
    scale = BEHAVIOUR.get('scale', 1.0)
    return MethodOutput(barrels={barrel: BarrelOutput(ranking=ScoredRanking({j: scale * c for j, c in s.items()}))
                                 for barrel, s in counts.items()})


def verify(task, view, forecast, diagnostic):
    """Recompute and compare, or the disagreement planted for this target."""
    if task.target_draw_number in BEHAVIOUR.get('verify_fail_at', ()):
        raise ValueError('toy: verify disagrees')
    if len(view.draw_number) < BEHAVIOUR.get('short_below', 0):
        if forecast['record_status'] != 'INSUFFICIENT_HISTORY':
            raise ValueError('toy: too few draws, but the record is not INSUFFICIENT_HISTORY')
        return
    scale = BEHAVIOUR.get('scale', 1.0)
    for barrel, s in _counts(task, view).items():
        if forecast['barrels'][barrel]['scores'] != [scale * s[j] for j in sorted(s)]:
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


def make_tree(root: Path, role: str = 'DEV', copy_from: Path | None = None) -> Path:
    """Make an empty invented tree: its settings file, a small manifest and the folders the engine expects.

    root: an existing empty folder.  role: 'DEV', 'QA' or 'PROD'.  copy_from: the tree its results are copied
    from, if any.  Returns the tree's real path.
    """
    tree = Path(root).resolve()
    (tree / 'src' / 'methods').mkdir(parents=True)
    (tree / 'deploy').mkdir()
    (tree / '.venv').mkdir()
    for name, text in (('toy_forecast_code.py', '# invented forecasting code\n'),
                       ('toy_derived_code.py', '# invented scoring code\n'), ('toy_other.py', '# a launcher\n')):
        (tree / 'src' / name).write_text(text, encoding='ascii')
    (tree / 'deploy' / 'INFRA_MANIFEST.ini').write_text(
        '[files]\nsrc/toy_forecast_code.py = forecast\nsrc/toy_derived_code.py = derived\nsrc/toy_other.py = other\n',
        encoding='ascii')
    lines = ['[environment]', f'role = {role}', f'tree_root = {tree}', f'venv_dir = {tree / ".venv"}']
    if role != 'DEV':
        backups = tree.parent / (tree.name + '_backups')
        backups.mkdir(exist_ok=True)
        lines.append(f'backup_root = {backups}')
    if copy_from is not None:
        lines += ['[results]', f'copy_from = {copy_from}']
    (tree / 'ENVIRONMENT.ini').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return tree


def add_toy_variant(tree: Path, family: str, variant: str, games=('POWERBALL', 'OZLOTTO'), minimum: int = 3,
                    behaviour: dict | None = None, helpers=()) -> Path:
    """Add a toy variant folder (method.py and VARIANT.json) to a tree; return the folder.

    family, variant: for example 'E_901' and 'TOY_COUNTS_V1'.  minimum: the earlier draws it declares it needs.
    behaviour: what is planted, by target: {'fail_at': [...], 'crash_at': [...], 'bad_output_at': [...],
    'verify_fail_at': [...], 'short_below': n, 'scale': x}.  helpers: helper paths its declaration lists.
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
