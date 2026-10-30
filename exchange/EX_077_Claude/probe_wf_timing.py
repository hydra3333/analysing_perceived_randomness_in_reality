"""WF-1 design probe (Claude, 30 Oct 2026): time a synthetic walk-forward of every installed variant.
Invented master only (tests' varied_row), simulated release in a temporary copy of the contract data.
Never reads source_data/, results/ or transitory_data/."""
import sys, time, tempfile, json
from pathlib import Path
REPO = Path(sys.argv[1]); GAME = sys.argv[2]; STEP = int(sys.argv[3])
sys.path[:0] = [str(REPO / 'src' / 'methods'), str(REPO / 'tests')]
import e2r_code2_fixtures as C
from test_e6_beta_bernoulli import write_varied_master
import _common.contract_runner as CR, _common.contract_publication as CP
from _common.contract_registry import InstalledRegistry
from _common.contract_records import record_digest
from _common.game_profiles import get_profile
import Method_Contract_Runner as MCR
p = get_profile(GAME)
S = 1286 if GAME == 'POWERBALL' else 1475
L = p.holdout_first - 1
targets = list(range(S, L + 1, STEP))
with tempfile.TemporaryDirectory() as td:
    td = Path(td); data = C.copy_data_root(td); reg = InstalledRegistry(data)
    rel = []
    for (g, m, v) in reg.chain_keys():
        if g != GAME or v == 'NOT_YET_SPECIFIED': continue
        e1 = reg.active_entry(g, m, v); d = reg.declaration(e1['declaration_digest'])
        if e1['registry_status'] != 'SUPPORTED':
            e2 = dict(e1, entry_sequence=e1['entry_sequence'] + 1, registry_status='SUPPORTED',
                      previous_entry_digest=record_digest(e1), registry_status_reason='probe: simulated release')
            C.append_entry(data, e2); e1 = e2
        rel.append((m, v, d, e1))
    methods = td / 'methods'; methods.mkdir()
    ws = td / 'ws'
    sha = write_varied_master(ws, p, L + 1, 0)
    per = {}
    with C.installed(data=data, methods=methods, marker=td / 'no_marker'):
        for (m, v, d, e) in rel:
            ad = MCR.ADAPTERS[m]; t0 = time.perf_counter(); outs = {}
            for t in targets:
                req = C.request(d, e, t, sha, run_id=CP.new_run_id())
                req['run_mode'] = 'SYNTHETIC_CONTRACT_TEST'
                r = CR.run_contract_method(req, compute=ad.compute, verify=ad.verify, repo_root=ws, run_root=td / 'runs')
                outs[r.reason] = outs.get(r.reason, 0) + 1
            per[(m, v)] = ((time.perf_counter() - t0) / len(targets), outs)
tot = sum(x[0] for x in per.values())
for k, (s, o) in sorted(per.items(), key=lambda kv: -kv[1][0]):
    print(f'{k[0]:5} {k[1]:40} {s*1000:8.1f} ms/target  {o}')
print(f'{GAME}: {len(per)} variants, {len(targets)} sampled targets; mean sum over variants {tot:.2f} s per target;'
      f' full window {L-S+1} targets -> about {tot*(L-S+1)/60:.1f} min')
