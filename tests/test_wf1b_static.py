"""WF-1B static checks (design v0.1r1 sections 6.1 and 6.3; Architecture 12.5; MRT-05): the report tool runs no method
and no method can reach the evaluator or the outcome reader."""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'src' / 'evaluation'
METHODS = ROOT / 'src' / 'methods'
ALLOWED_COMMON = {'_common.contract_publication', '_common.contract_runner', '_common.contract_vocab',
                  '_common.contract_receipts', '_common.contract_records', '_common.contract_registry',
                  '_common.walk_forward', '_common.game_profiles', '_common.game_draws_reader'}
STDLIB_OK = {'__future__', 'argparse', 'csv', 'collections', 'decimal', 'fractions', 'functools', 'hashlib', 'io',
             'json', 'math', 'pathlib', 'platform', 're', 'struct', 'sys', 'uuid', 'numpy', 'evaluation'}


def imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            base = ('.' * node.level) + (node.module or '')
            out.add(base)
            out |= {(base + '.' if node.module else base) + a.name for a in node.names}
    return out


class Static(unittest.TestCase):

    def test_no_method_file_imports_the_evaluator(self):
        for p in METHODS.rglob('*.py'):
            for name in imports(p):
                self.assertFalse(name == 'evaluation' or name.startswith('evaluation.'), (p, name))
            self.assertNotIn('outcome_reader', p.read_text(encoding='utf-8'), p)

    def test_the_evaluator_imports_no_method_code(self):
        for p in EVAL.glob('*.py'):
            for name in imports(p):
                if name.startswith('.'):
                    self.assertTrue(name.startswith('.') and name.count('.') <= 2, (p.name, name))
                    continue
                top = name.split('.')[0]
                if top == '_common':
                    self.assertIn('.'.join(name.split('.')[:2]), ALLOWED_COMMON, (p.name, name))
                else:
                    self.assertIn(top, STDLIB_OK, (p.name, name))
            text = p.read_text(encoding='ascii')
            for bad in ('Method_Contract_Runner', 'ADAPTERS', 'run_contract_method', 'E_0', 'subprocess', 'os.kill'):
                self.assertNotIn(bad, text, (p.name, bad))

    def test_only_the_outcome_reader_touches_the_masters(self):
        for p in EVAL.glob('*.py'):
            text = p.read_text(encoding='ascii')
            if p.name != 'outcome_reader.py':
                self.assertNotIn('source_data', text, p.name)
                self.assertNotIn('_trusted_file_bytes', text, p.name)
                self.assertNotIn('ledger_pin', text, p.name)
        users = [p.name for p in EVAL.glob('*.py') if any(n.endswith('outcome_reader') for n in imports(p))]
        self.assertEqual(sorted(users), ['report.py'])

    def test_sources_are_ascii(self):
        for p in list(EVAL.glob('*.py')) + list((EVAL / 'registry').glob('*.json')):
            p.read_bytes().decode('ascii')


if __name__ == '__main__':
    unittest.main()
