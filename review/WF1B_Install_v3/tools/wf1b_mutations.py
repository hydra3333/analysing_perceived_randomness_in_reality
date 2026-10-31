"""WF-1B mutation checks (Claude, 31 Oct 2026): each planted defect must make a WF-1B test fail.
Usage: python3 -I wf1b_mutations.py DEV_TREE"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

DEV = Path(sys.argv[1]).resolve()
E = 'src/evaluation/'
MUTANTS = [
    ('outcome reader admits a holdout target', E + 'outcome_reader.py',
     "if type(t) is not int or not (p.first_draw + 1 <= t <= p.holdout_first - 1):",
     "if type(t) is not int or not (p.first_draw + 1 <= t <= p.holdout_first):", ['test_wf1b_outcome_reader']),
    ('outcome reader decodes rows that are not requested', E + 'outcome_reader.py',
     "        if number not in want:\n            continue                                 # never decoded\n", "", ['test_wf1b_outcome_reader']),
    ('outcome reader skips the master hash check', E + 'outcome_reader.py',
     "        if hashlib.sha256(raw).hexdigest() != master_sha256:", "        if False:", ['test_wf1b_outcome_reader']),
    ('outcomes read before the search-log row', E + 'report.py',
     "    # ---------------------------------------------------------------- step 4: the search-log row (before outcomes)\n",
     "    _early = OR.read_outcomes(repo_root=roots()['project'], game_id=game_id, master_sha256=plan['master_sha256'],\n"
     "                              targets=sorted({k[2] for k, c in collected['cells'].items() if c['valid']}))\n", ['test_wf1b_report']),
    ('a refused window appends a row', E + 'report.py',
     "    if last > p.holdout_first - 1:\n        raise ReportRefused(",
     "    if last > p.holdout_first - 1:\n        WF._append_search_row({'row_type': 'RANKING_REPORT'})\n        raise ReportRefused(", ['test_wf1b_report']),
    ('unequal duplicates accepted', E + 'collect.py',
     "            elif len({f['content_digest'] for f in found}) > 1:", "            elif False:", ['test_wf1b_report']),
    ('family guarantee ignores incomplete tracks', E + 'report_writer.py',
     "            if tr['status'] != 'GRID_COMPLETE':\n                broke.append((tid, tr['status']))\n            elif",
     "            if False:\n                pass\n            elif", ['test_wf1b_report']),
    ('Bonferroni M reduced to the tracks with a p-value', E + 'report_writer.py',
     "            b = MS.bonferroni(pmin, fam['M'])", "            b = MS.bonferroni(pmin, len(ps))", ['test_wf1b_report']),
    ('a significance label shown in Part A', E + 'report_writer.py',
     "            w(f\"{'':7}{r['method_id']} {name}: {key}\")",
     "            w(f\"{'':7}{r['method_id']} {name}: {key} {sub['calibration']} EXACT_LOCAL\")", ['test_wf1b_report']),
    ('Part B before the glossary', E + 'report_writer.py',
     "    w('GLOSSARY')", "    w(PART_B)\n    w('GLOSSARY')", ['test_wf1b_report']),
    ('N1 root accepts lower case', E + 'n1_generator.py',
     "ROOT = re.compile(r'[0-9A-F]{128}\\Z', re.ASCII)", "ROOT = re.compile(r'[0-9A-Fa-f]{128}\\Z', re.ASCII)", ['test_wf1b_n1_generator']),
    ('N1 word read big-endian', E + 'n1_generator.py',
     "        w = int.from_bytes(self.buf[self.pos:self.pos + 8], 'little')",
     "        w = int.from_bytes(self.buf[self.pos:self.pos + 8], 'big')", ['test_wf1b_n1_generator']),
    ('binomial upper tail off by one', E + 'numerics.py',
     "    return Fraction(_upper_num(n, a, b, k), b ** n)", "    return Fraction(_upper_num(n, a, b, max(1, k - 1)), b ** n)", ['test_wf1b_numerics']),
    ('sigma precision loss for small p (the fixed bug)', E + 'numerics.py',
     "    q = ((num >> sn) << (2 * _BITS)) // (den >> sd)\n    e2 = sn - sd - 2 * _BITS",
     "    q = ((num >> sn) << _BITS) // (den >> sd)\n    e2 = sn - sd - _BITS", ['test_wf1b_numerics']),
    ('a method may import the evaluator', 'src/methods/_common/game_profiles.py',
     "from __future__ import annotations", "from __future__ import annotations\ntry:\n    import evaluation  # noqa\nexcept ImportError:\n    pass",
     ['test_wf1b_static']),
    ('supplementaries stored in the match record', E + 'divisions.py',
     "    return {'main_matches': m, 'supplementary_matches': s,", "    return {'main_matches': m, 'supplementary_matches': s, 'supps': list(supps),",
     ['test_wf1b_divisions']),
    ('seed record time stamp not checked', E + 'seed_policies.py',
     "    if rec['time_stamp'] != ann['time_stamp']:", "    if False:", ['test_wf1b_seed_policy']),
    ('seed record sources not checked', E + 'seed_policies.py',
     "            srcs[0]['read_by'] == srcs[1]['read_by']):", "            False):\n        pass\n    if False:", ['test_wf1b_seed_policy']),
    ('an unannounced policy accepted', E + 'seed_policies.py',
     "    if pid not in ANNOUNCED:\n        raise", "    if pid not in ANNOUNCED:\n        return rec\n        raise", ['test_wf1b_seed_policy']),
    ('range label replaced by the calibration label', E + 'report_writer.py',
     "    labels = [sig.get('label')] + [x.get('label') if isinstance(x, dict) else None for x in (po, zp)]",
     "    labels = [sig.get('label')]", ['test_wf1b_report']),
    ('N1 Monte Carlo interval not printed in Part B', E + 'report_writer.py',
     "            if mc_text(sig):\n                w(f\"{'':7}{mc_text(sig)}\")\n", "", ['test_wf1b_report']),
    ('Oz Lotto supplementaries replayed against the main draw', E + 'n1.py',
     "        second = _popcount(sim['extra'][:, cols] & tick[None, :])", "        second = _popcount(sim['main'][:, cols] & tick[None, :]) * 0",
     ['test_wf1b_n1_replay']),
    ('the reader admits a hard-linked master',
     'src/methods/_common/game_draws_reader.py',
     "        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:",
     "        if not stat.S_ISREG(before.st_mode):", ['test_wf1b_outcome_reader']),
]


def run(tree: Path, mods) -> bool:
    env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
    env['PYTHONPATH'] = os.pathsep.join(str(tree / p) for p in ('src', 'src/methods', 'tests'))
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest'] + [f'tests.{m}' for m in mods], cwd=tree, env=env,
                       capture_output=True, text=True, timeout=1200)
    return r.returncode == 0


ok = run(DEV, sorted({m for x in MUTANTS for m in x[4]}))
print('baseline (unmutated) passes:', ok)
caught = 0
for name, rel, old, new, mods in MUTANTS:
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td) / 't'
        shutil.copytree(DEV, tree, ignore=shutil.ignore_patterns('__pycache__'))
        f = tree / rel
        text = f.read_text(encoding='utf-8')
        if text.count(old) != 1:
            print(f'MUTANT NOT APPLIED ({text.count(old)} matches): {name}')
            continue
        f.write_text(text.replace(old, new), encoding='utf-8')
        passed = run(tree, mods)
        caught += not passed
        print(('CAUGHT   ' if not passed else 'SURVIVED ') + name)
print(f'{caught} of {len(MUTANTS)} mutants caught')
