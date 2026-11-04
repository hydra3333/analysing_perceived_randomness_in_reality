"""E_1 revision 3's frozen r2 reference (MHUP-1 design v0.1r5 section 2; EX_125 C01): tests/fixtures/e1_r2_reference_v1.json.

Computes E_1 revision 2's contract forecast records from a BASE tree (the repository before MHUP-A), in a temporary
copy of that tree's src/ and tests/ OUTSIDE the repository, in a separate Python process; nothing under archive/ is
read or run. Two record sets per game, on the same invented masters (tests/test_e6_beta_bernoulli.write_varied_master,
variant 0) at e2r_fixtures.targets():
  - SYNTHETIC_CONTRACT_TEST through run_contract_method with a synthetic workspace;
  - REAL_DEVELOPMENT through run_contract_method with the runner's PROJECT_ROOT patched to the workspace (the real
    development switch is on at the base), so the record is the real view kind's.
Revision 3 must equal both label for label (scores, ranking, tie order, TOP, WORST, permitted_view_digest) apart from
method_revision, declaration_digest and the content digest; and its REAL_HOLDOUT record on the same prefix must equal
the REAL_DEVELOPMENT one in the same way (one data kind, design 3.3).
Usage: python3 -I make_e1_r2_reference.py BASE_TREE OUT_JSON
"""
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

base, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
R2_FILES = ('src/methods/E_001/__init__.py', 'src/methods/E_001/e1_historical_appearance_frequency.py',
            'src/methods/E_001/multigame_e1.py', 'src/methods/contract_adapters/e_001.py')
CHILD = r'''
import json, sys, tempfile
from pathlib import Path
from unittest import mock
import e2r_code2_fixtures as C
import e2r_fixtures as F
import _common.contract_runner as CR
from _common.contract_registry import InstalledRegistry
from _common.game_profiles import get_profile
from contract_adapters import e_001
from test_e6_beta_bernoulli import write_varied_master
td = Path(tempfile.mkdtemp())
recs = []
with C.installed(marker=td / 'no_marker'):
    for game in ('POWERBALL', 'OZLOTTO'):
        reg = InstalledRegistry()
        e = reg.active_entry(game, *C.E1)
        d = reg.declaration(e['declaration_digest'])
        assert e['method_revision'] == '2' and e['registry_status'] == 'SUPPORTED'
        for t in F.targets(get_profile(game)):
            ws = td / f'ws_{game}_{t}'
            sha = write_varied_master(ws, get_profile(game), t, 0)
            for mode in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):
                req = C.request(d, e, t, sha, run_id='mg-' + '2' * 32)
                req['run_mode'] = mode
                req['product_kind'] = 'WF_FORECAST' if mode == 'REAL_DEVELOPMENT' else 'SYNTHETIC_TEST_OUTPUT'
                runs = td / f'runs_{game}_{t}_{mode}'
                if mode == 'REAL_DEVELOPMENT':
                    with mock.patch.object(CR, 'PROJECT_ROOT', ws):
                        res = CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=ws, run_root=runs)
                else:
                    res = CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=ws, run_root=runs)
                assert res.outcome == 'SUCCESS', (game, t, mode, res.reason)
                f, = runs.rglob('forecast.json')
                recs.append(json.loads(f.read_bytes()))
print(json.dumps(recs))
'''
with tempfile.TemporaryDirectory() as td:
    copy = Path(td) / 'base_copy'
    for sub in ('src', 'tests'):
        shutil.copytree(base / sub, copy / sub, ignore=shutil.ignore_patterns('__pycache__'))
    env = {'PYTHONPATH': ':'.join(str(copy / p) for p in ('src', 'src/methods', 'tests')), 'PATH': '/usr/bin:/bin'}
    r = subprocess.run([sys.executable, '-B', '-c', CHILD], cwd=copy, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr)
    records = json.loads(r.stdout)
sys.path.insert(0, str(base / 'src' / 'methods'))
from _common.contract_records import canonical          # noqa: E402  (the base tree's canonical encoder)
doc = {'schema': 'E1_R2_REFERENCE_V1',
       'purpose': ('E_1 revision 2 contract forecast records, synthetic and real-development, frozen before the MHUP-A '
                   'package, for E1R3-T01 (revision 3 must equal them apart from method_revision, declaration_digest and '
                   'canonical_content_digest, and its REAL_HOLDOUT record on the same prefix must equal the real one)'),
       'made_by': 'review/MHUPA_Slice1/tools/make_e1_r2_reference.py, run on the base tree in a copy outside the repository',
       'inputs': ('tests/test_e6_beta_bernoulli.write_varied_master(variant 0) at e2r_fixtures.targets() per game; '
                  "the base tree's installed E_1 revision-2 pins; run_id mg-22222222222222222222222222222222; "
                  'run modes SYNTHETIC_CONTRACT_TEST and REAL_DEVELOPMENT (PROJECT_ROOT patched to the workspace)'),
       'base_r2_sources_sha256': {p: hashlib.sha256((base / p).read_bytes()).hexdigest() for p in R2_FILES},
       'records': records}
raw = canonical(doc)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(raw)
print(f'{len(records)} records; {out} {hashlib.sha256(raw).hexdigest()}')
