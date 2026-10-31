"""E1R2-T01's frozen r1 reference (Claude, 31 October 2026; CODE-3 and E_1 r2 design v0.1r2 section 6, EX_087 C01).

Computes E_1 revision 1's synthetic contract forecast records from a BASE tree (the repository before the E_1 r2
package), in a temporary copy of that tree's src/ and tests/ OUTSIDE the repository, in a separate Python process,
and writes them as tests/fixtures/e1_r1_reference_v1.json. Nothing under archive/ is read or run.
Inputs: the invented masters of tests/test_e6_beta_bernoulli.write_varied_master (variant 0) at each game's
e2r_fixtures.targets(); the installed E_1 revision-1 pins of the base tree; run ID mg-<32 x '1'>.
Usage: python3 -I make_e1_r1_reference.py BASE_TREE OUT_JSON
"""
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

base, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
R1_FILES = ('src/methods/E_001/__init__.py', 'src/methods/E_001/e1_historical_appearance_frequency.py',
            'src/methods/E_001/multigame_e1.py', 'src/methods/contract_adapters/e_001.py')
CHILD = r'''
import json, sys, tempfile
from pathlib import Path
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
        assert e['method_revision'] == '1' and e['registry_status'] == 'SUPPORTED'
        for t in F.targets(get_profile(game)):
            ws = td / f'ws_{game}_{t}'
            sha = write_varied_master(ws, get_profile(game), t, 0)
            req = C.request(d, e, t, sha, run_id='mg-' + '1' * 32)
            runs = td / f'runs_{game}_{t}'
            res = CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=ws, run_root=runs)
            f, = runs.rglob('forecast.json')
            recs.append(json.loads(f.read_bytes()))
print(json.dumps(recs))
'''
with tempfile.TemporaryDirectory() as td:
    copy = Path(td) / 'base_copy'
    for sub in ('src', 'tests'):
        shutil.copytree(base / sub, copy / sub, ignore=shutil.ignore_patterns('__pycache__'))
    assert not (copy / 'archive').exists()
    env = {'PYTHONPATH': ':'.join(str(copy / p) for p in ('src', 'src/methods', 'tests')), 'PATH': '/usr/bin:/bin'}
    r = subprocess.run([sys.executable, '-B', '-c', CHILD], cwd=copy, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr)
    records = json.loads(r.stdout)
sys.path.insert(0, str(base / 'src' / 'methods'))
from _common.contract_records import canonical          # noqa: E402  (the base tree's canonical encoder)
doc = {'schema': 'E1_R1_REFERENCE_V1',
       'purpose': ('E_1 revision 1 synthetic contract forecast records, frozen before the E_1 revision 2 package, for '
                   'E1R2-T01 (r2 must equal them apart from method_revision, declaration_digest and '
                   'canonical_content_digest)'),
       'made_by': 'review/E1R2_Install_v3/tools/make_e1_r1_reference.py, run on the base tree in a copy outside the repository',
       'inputs': ('tests/test_e6_beta_bernoulli.write_varied_master(variant 0) at e2r_fixtures.targets() per game; '
                  "the base tree's installed E_1 revision-1 pins; run_id mg-11111111111111111111111111111111"),
       'base_r1_sources_sha256': {p: hashlib.sha256((base / p).read_bytes()).hexdigest() for p in R1_FILES},
       'records': records}
raw = canonical(doc)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(raw)
print(f'{len(records)} records; {out} {hashlib.sha256(raw).hexdigest()}')
