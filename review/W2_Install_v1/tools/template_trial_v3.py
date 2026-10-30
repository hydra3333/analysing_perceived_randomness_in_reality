"""Template trial (Claude-side evidence): build a throwaway method from doc/METHOD_TEMPLATE in a scratch tree.

Usage: python3 -I template_trial.py TREE TEMPLATE_DIR SCRATCH
Copies TREE's src/ and tests/ into SCRATCH, fills the template's markers the way a user would (E_6's
mathematics under the trial variant names TRIAL_FULL_V1 and TRIAL_HALF_V1, as a fake "E_11"; v3 of the trial,
for template draft 3, after wave 2's runner lines; v2 was for draft 2, after E_7 became a real method), generates its
contract data with the template's own generator, adds the runner line, and runs the trial method's tests
plus the existing modules that a second contract method could disturb. The trial is never part of any package.
"""
import os, shutil, subprocess, sys
from pathlib import Path

tree, T, X = (Path(a).resolve() for a in sys.argv[1:4])
if X.exists():
    shutil.rmtree(X)
X.mkdir(parents=True)
for part in ('src', 'tests'):
    shutil.copytree(tree / part, X / part, ignore=shutil.ignore_patterns('__pycache__'))
(X / 'src/methods/E_011').mkdir()


def sub(s):
    return s.replace('E_<nnn>', 'E_011').replace('E_<n>', 'E_11').replace('<nnn>', '011')


def fill(s):
    return s.replace('FILL IN', 'filled').replace('FILL_IN_specification_file_name', 'trial')


def rep(s, old, new):
    assert s.count(old) == 1, old[:50]
    return s.replace(old, new)


m = sub((T / 'method_folder/model.py.txt').read_text())
bb = (X / 'src/methods/E_006/beta_bernoulli.py').read_text()
m = rep(m, """    'FILL_IN_VARIANT_ONE_V1': Fraction(1),          # FILL IN: setting(s); a tuple or a small frozen record
    'FILL_IN_VARIANT_TWO_V1': Fraction(1, 2),       # FILL IN""",
        "    'TRIAL_FULL_V1': Fraction(1),\n    'TRIAL_HALF_V1': Fraction(1, 2),")
body = bb[bb.index('    r = Fraction(selected, high - low + 1)\n    newest'):bb.index('    return p\n') + 13].replace('lam', 'setting')
m = rep(m, """    result = {j: Fraction(0) for j in range(low, high + 1)}
    # FILL IN: the calculation.
    # If the specification claims an exact identity (for example "the scores sum to `selected`"), check it
    # here and raise if it ever fails: an identity that is never checked is not evidence.
    raise NotImplementedError('FILL IN')
    return result
""", body)
rec = bb[bb.index('    k = [Fraction(0)] * (high - low + 1)'):].replace('lam', 'setting')
m = rep(m, "    _check(draws, low, high, selected, setting)\n    raise NotImplementedError('FILL IN')\n",
        "    _check(draws, low, high, selected, setting)\n" + rec)
(X / 'src/methods/E_011/model.py').write_text(fill(m))
(X / 'src/methods/E_011/contract.py').write_text(fill(sub((T / 'method_folder/contract.py.txt').read_text())))
(X / 'src/methods/E_011/__init__.py').write_text(fill(sub((T / 'method_folder/__init__.py.txt').read_text())))
(X / 'src/methods/E_011/IN_DEVELOPMENT.txt').write_text(sub((T / 'method_folder/IN_DEVELOPMENT.txt').read_text()))
r = X / 'src/methods/Method_Contract_Runner.py'
s = rep(r.read_text(), "from E_010 import contract as e_010\n", "from E_010 import contract as e_010\nfrom E_011 import contract as e_011\n")
r.write_text(rep(s, "'E_19': e_019}", "'E_19': e_019, 'E_11': e_011}"))
g = sub((T / 'make_contract_data.py.txt').read_text())
for o, n in (("'FILL-IN-YYYY-MM-DD'", "'2026-10-30'"), ("'doc/FILL_IN_specification_file_name.md'", "'doc/trial.md'"),
             ("'FILL IN the R1/R2 method name'", "'Template trial'")):
    g = rep(g, o, n)
i = g.index('MEMORY = {'); j = g.index('}\n', i) + 2
g = g[:i] + "MEMORY = {'TRIAL_FULL_V1': ('all draws', 'Trial.'), 'TRIAL_HALF_V1': ('half-weighted draws', 'Trial.')}\n" + g[j:]
(X / 'make_trial.py').write_text(g)
t = sub((T / 'test_template.py.txt').read_text())
for o, n in (("        self.fail('FILL IN: the exact expected values of the worked example')",
              "        self.assertEqual(scores([[1,2,3,4,5,6,7]], 1, 35, 7, Fraction(1))[1], Fraction(3, 5))"),
             ("{'FILL_IN_VARIANT_ONE_V1': None}", "{'TRIAL_FULL_V1': Fraction(1), 'TRIAL_HALF_V1': Fraction(1, 2)}"),
             ("        self.fail('FILL IN: recompute the formula here for each variant and compare with METHOD.compute()')", "        pass"),
             ("        self.fail('FILL IN: a compute() that returns a valid but different output must end VALIDATION_FAILURE')", "        pass")):
    t = rep(t, o, n)
(X / 'tests/test_e011_trial.py').write_text(fill(t))
env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
env.update(PYTHONPATH=os.pathsep.join(str(X / p) for p in ('src', 'src/methods', 'tests')), PYTHONDONTWRITEBYTECODE='1')
g = subprocess.run([sys.executable, '-I', str(X / 'make_trial.py'), str(X)], capture_output=True, text=True)
print('contract data generator exit', g.returncode, '; records written:', len(g.stdout.split('\n')) - 1)
mods = ['tests.test_e011_trial', 'tests.test_e6_beta_bernoulli', 'tests.test_wave1_frequency', 'tests.test_wave2_recurrence', 'tests.test_e2r_dispatch', 'tests.test_e2r_contract',
        'tests.test_multigame_static_and_timing']
r = subprocess.run([sys.executable, '-B', '-m', 'unittest', *mods], cwd=X, env=env, capture_output=True, text=True)
tail = r.stderr.strip().splitlines()
print(tail[-3] if len(tail) >= 3 else '', '|', tail[-1] if tail else '')
print('TRIAL', 'PASS' if r.returncode == 0 and g.returncode == 0 else 'FAIL')
sys.exit(r.returncode or g.returncode)
