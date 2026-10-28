"""E1-ALIGN guards (proposed new test module; offline, no data, no processes, nothing created).

1. Shared code imports no method code: no module under src/methods/_common, src/coordinator_private
   or the coordinator imports from a method folder (E_<nnn>) or names an E_1-only module, whether as
   the imported module or as a name imported from a package (symbol-aware, E1A2-C01).
2. E_1 keeps its old symbols: the E_1 core module's canonical_bytes and _length32_tuple are the shared
   functions themselves, and the reader uses the same canonical_bytes.
3. The five E_1-only modules exist only in src/methods/E_001/ and are imported from there.
4. E_1's real-mode orphan-marker path still resolves to the project marker (path arithmetic only;
   the marker is never created, read or removed).
5. Encoder regression alarm: the six live copies of the canonical JSON encoding give identical bytes on
   a fixed corpus and reject the same invalid inputs. The coordinator's copy is taken from its source by
   AST, so the coordinator is not imported or run. This is an alarm, not licence to change any of them.
"""
import ast
import importlib
import importlib.util
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHODS = ROOT / 'src' / 'methods'
for p in (str(ROOT / 'src'), str(METHODS)):
    if p not in sys.path:
        sys.path.insert(0, p)

E1_ONLY = ('e1_historical_appearance_frequency', 'e1_training_view', 'e1_standalone_contract',
           'e1_common_reader_bridge', 'multigame_e1')


def _imports(path):
    # Yields the module of every import AND, for 'from M import N', each 'M.N', so that
    # 'from methods import E_001' or 'from _common import e1_training_view' is seen.
    tree = ast.parse(path.read_text('utf-8'))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            base = ('.' * node.level) + (node.module or '')
            yield base
            for alias in node.names:
                if alias.name != '*':
                    yield base + '.' + alias.name
        elif isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name


def _coordinator_encoder():
    src = (ROOT / 'src' / 'Powerball_Experiment_Coordinator.py').read_text('utf-8')
    fns = [n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == 'canonical_bytes']
    assert len(fns) == 1
    mod = ast.Module(body=[ast.Import(names=[ast.alias(name='json')]), fns[0]], type_ignores=[])
    ns = {}
    exec(compile(ast.fix_missing_locations(mod), '<coordinator canonical_bytes>', 'exec'), ns)
    return ns['canonical_bytes']


CORPUS = [
    None, True, False, 0, -1, 1, 2**31 - 1, 2**32, 2**53 + 1, -2**63, 2**64 + 7, 0.5, -0.0, 1e-7, 1.0e300,
    '', 'abc', '\u00e9', '\u2028\u2029', '\U0001F600', '\x00\x1f\x7f', '"\\/', 'line\nbreak',
    [], {}, [1, [2, [3, []]]], {'b': 1, 'a': 2, 'A': 3, '\u00e9': 4, '': 5}, {'z': {'y': {'x': [None]}}},
    (1, 'two', (3,)), {1: 'int key', 2: [True, None, 1.25]},
    {'records': [{'draw': 1144, 'main': [1, 2, 3, 4, 5, 6, 7], 'powerball': 20}], 'schema': 'S'},
]
INVALID = [(float('nan'), ValueError), (float('inf'), ValueError), (-math.inf, ValueError),
           ({'a': {1, 2}}, TypeError), (b'bytes', TypeError), ({1: 'a', 'b': 2}, TypeError)]


class E1AlignGuards(unittest.TestCase):

    def test_shared_code_imports_no_method_code(self):
        shared = [*(METHODS / '_common').glob('*.py'), *(ROOT / 'src' / 'coordinator_private').glob('*.py'),
                  ROOT / 'src' / 'Powerball_Experiment_Coordinator.py']
        for path in shared:
            for ref in _imports(path):
                parts = ref.lstrip('.').split('.')
                self.assertFalse(any(p.startswith('E_') for p in parts), f'{path.name} imports {ref}')
                self.assertFalse(any(p in E1_ONLY for p in parts), f'{path.name} imports {ref}')

    def test_e1_symbols_are_the_shared_functions(self):
        enc = importlib.import_module('_common.canonical_encoding')
        core = importlib.import_module('E_001.e1_historical_appearance_frequency')
        reader_src = (METHODS / '_common' / 'game_draws_reader.py').read_text('utf-8')
        self.assertIs(core.canonical_bytes, enc.canonical_bytes)
        self.assertIs(core._length32_tuple, enc.length32_tuple)
        self.assertIn('from _common.canonical_encoding import canonical_bytes', reader_src)

    def test_e1_only_modules_live_in_the_method_folder(self):
        for name in E1_ONLY:
            self.assertFalse((METHODS / '_common' / f'{name}.py').exists(), name)
            m = importlib.import_module(f'E_001.{name}')
            self.assertEqual(Path(m.__file__).resolve(), (METHODS / 'E_001' / f'{name}.py').resolve())
            self.assertIsNone(importlib.util.find_spec(f'_common.{name}'))
        self.assertTrue((METHODS / 'E_001_Historical_Appearance_Frequency.py').is_file())

    def test_e1_orphan_marker_path_unchanged(self):
        contract = importlib.import_module('E_001.e1_standalone_contract')
        src = Path(contract.__file__).read_text('utf-8')
        self.assertEqual(src.count("Path(__file__).resolve().parents[3] / 'transitory_data' / 'poc_runs' / "
                                   "'UNRESOLVED_ORPHAN.json'"), 1)
        self.assertEqual(Path(contract.__file__).resolve().parents[3], ROOT.resolve())

    def test_six_encoder_copies_agree(self):
        encoders = {
            'shared canonical_bytes': importlib.import_module('_common.canonical_encoding').canonical_bytes,
            'multigame json_bytes': importlib.import_module('_common.multigame_standalone_contract').json_bytes,
            'POC canonical_json': importlib.import_module('_common.experiment_console_and_file_output').canonical_json,
            'E_1 standalone canonical_json': importlib.import_module('E_001.e1_standalone_contract').canonical_json,
            'exit receipt _canonical': importlib.import_module(
                'coordinator_private.multigame_coordinator_exit_receipt')._canonical,
            'coordinator canonical_bytes (AST copy)': _coordinator_encoder(),
        }
        for value in CORPUS:
            expected = (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'),
                                   allow_nan=False) + '\n').encode('ascii')
            for name, enc in encoders.items():
                with self.subTest(value=repr(value)[:40], encoder=name):
                    self.assertEqual(enc(value), expected)
        for value, exc in INVALID:
            for name, enc in encoders.items():
                with self.subTest(value=repr(value)[:40], encoder=name):
                    with self.assertRaises(exc):
                        enc(value)


if __name__ == '__main__':
    unittest.main()
