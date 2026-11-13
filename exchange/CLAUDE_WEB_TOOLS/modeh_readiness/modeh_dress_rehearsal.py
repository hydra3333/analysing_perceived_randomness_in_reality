#!/usr/bin/env python3
"""Mode H dress rehearsal on INVENTED data, with the installed code and the FULL released cohort (Claude web chat,
13 November 2026; a development check for the Approval 1 readiness sheet, not production code).

For each game, in a temporary project that holds a copy of the repository's src/ (its real install and release records
included), the root .bat files and an INVENTED master (the test fixtures' varied master up to holdout_first - 1):
  manifest -> opening record -> an invented first update that, like the real one will, goes PAST the holdout's last draw
  -> the one Mode H plan (the real runner adapters) -> the batch (every released variant x ten targets) -> the one score
  with the approved N1 policy -> the seal; then a second plan, a second score and an update-free rerun are shown refused.
It reads nothing under the repository's source_data/, results/ or transitory_data/; every draw it uses is invented.
The environment inventory is the fixtures' invented one (the real one was checked on the owner's venv by T016 row 6).
Usage (from a clone): PYTHONPATH=src:src/methods:tests python -B modeh_dress_rehearsal.py [EXTRA_DRAWS [KEEP_FOLDER]]
"""
import collections, contextlib, json, shutil, sys, tempfile, time
from pathlib import Path

import mhupa_slice2_fixtures as X
from mhupa_fixtures import grow_master
from test_e6_beta_bernoulli import write_varied_master
import Method_Contract_Runner as MCR
import _common.walk_forward as WF
import _common.owner_records as OR
import _common.closure as CL
from _common.game_profiles import POWERBALL, OZLOTTO
from evaluation import mode_h as MH, n1 as N1, seed_policies as SP

ROOT = X.ROOT
EXTRA = int(sys.argv[1]) if len(sys.argv) > 1 else 5
KEEP = sys.argv[2] if len(sys.argv) > 2 else None       # optional: keep the INVENTED-data reports and console lines here


def build(tmp: Path, profile) -> Path:
    proj = tmp / 'project'
    write_varied_master(proj, profile, profile.holdout_first, 0)
    shutil.copytree(ROOT / 'src', proj / 'src', ignore=shutil.ignore_patterns('__pycache__'))   # the installed state
    for p in ROOT.glob('*.bat'):
        shutil.copy2(p, proj / p.name)
    for name in CL.ROOT_FILES:
        if (ROOT / name).is_file():
            shutil.copy2(ROOT / name, proj / name)
    return proj


def one(profile) -> bool:
    g, ok, t0 = profile.game_id, True, time.time()

    def say(text):
        print(f'[{g}] {text}', flush=True)
    with tempfile.TemporaryDirectory() as td, contextlib.ExitStack() as stack:
        tmp = Path(td)
        proj, env = build(tmp, profile), X.fake_environment(tmp)
        stack.enter_context(X.patched(proj, env, small_cohort=False))
        man = MH.manifest(g)
        say(f"manifest: cohort {len(man['cohort'])} variants of {len({m['method_id'] for m in man['cohort']})} methods; targets "
            f"{man['targets'][0]}-{man['targets'][-1]}; families {man['families']}; exposure flags {sorted(man['exposure'])}; "
            f"closure {man['closure']['count']} files; freeze version {man['freeze_version']}")
        MH.open_holdout(g, OR.OPENING_STATEMENT)
        grow_master(proj, profile, [list(range(profile.holdout_first, profile.holdout_last + EXTRA + 1))])
        import _common.master_versions as MV
        last = MV.load_verified_source(proj, g)[1][-1]
        say(f'invented first update: version {last.version} ({last.action}), last draw {last.last_draw} (holdout_last + {EXTRA})')
        plan = WF.make_mode_h_plan(g, MCR.ADAPTERS)
        bid = plan['batch_id']
        say(f"plan: {len(plan['cohort'])} variants x {len(plan['targets'])} targets = {len(plan['cohort']) * len(plan['targets'])} pairs")
        t1, out = time.time(), []
        rc = WF.run_batch(g, bid, MCR.ADAPTERS, echo=out.append)
        say(f'run: exit {rc} in {time.time() - t1:.0f} s; last line: {out[-1] if out else ""}')
        ok &= rc == 0
        tk = OR.tickets(WF._attempts_path(plan), scope_kind='MODE_H_BATCH', scope_id=bid, game_id=g)
        kinds = collections.Counter(t['kind'] for t in tk)
        classes = collections.Counter(t.get('terminal_class') for t in tk if t['kind'] == 'DONE')
        say(f'tickets: {dict(kinds)}; DONE terminal classes: {dict(classes)}')
        if kinds['DONE'] != len(plan['cohort']) * len(plan['targets']) or set(classes) != {'SUCCESS PUBLISHED'}:
            say('NOTE: not every pair is DONE with a published forecast')
            ok = False
        policy = SP.approved_policy()
        t2, prog = time.time(), []
        res = MH.score(g, echo=prog.append, n1_runner=N1.runner(policy), seed_line=f"policy {policy['policy_id']}, R = {N1.R}",
                       n1_policies_on_file=SP.count_policies(), environment={})
        markers = OR.lifecycle_markers_present(proj, g, bid)
        say(f"score: {res['scores']} score lines, {res['ranks']} rank lines in {time.time() - t2:.0f} s; markers {markers}")
        ok &= markers == ['BATCH_COMPLETE', 'SCORING_STARTED', 'SCORE_COMPLETE', 'MODE_H_SEALED']
        texts = {p.suffix: p.read_bytes() for p in res['paths']}
        say('report files: ' + ', '.join(f'{p.name} ({len(texts[p.suffix])} bytes)' for p in res['paths']))
        ledger = (WF.roots('MODE_H_BATCH')['scores'] / g / bid / res['attempt_id'] / MH.SCORE_LEDGER).read_bytes()
        drawn = {tuple(r['drawn_main']) for r in map(json.loads, ledger.splitlines()) if 'drawn_main' in r}
        leak = [ext for ext, raw in texts.items() if any(json.dumps(list(d))[1:-1].encode() in raw or
                                                         ' '.join(map(str, d)).encode() in raw for d in drawn)]
        say(f'drawn numbers in a report file (invented draws; must be none): {leak or "none"}')
        if KEEP:
            (Path(KEEP) / g).mkdir(parents=True, exist_ok=True)
            for p in res['paths']:
                shutil.copy2(p, Path(KEEP) / g / p.name)
            (Path(KEEP) / g / 'progress.txt').write_text('\n'.join(prog + out) + '\n')
        ok &= not leak
        for name, fn, exc in (('a second plan', lambda: WF.make_mode_h_plan(g, MCR.ADAPTERS), WF.BatchRefused),
                              ('a second score', lambda: MH.score(g, echo=None, n1_runner=None, seed_line='x',
                                                                  n1_policies_on_file=0, environment={}), MH.ModeHRefused)):
            try:
                fn()
                say(f'{name}: NOT REFUSED')
                ok = False
            except exc as e:
                say(f'{name}: refused ({str(e)[:90]})')
        rc2 = WF.run_batch(g, bid, MCR.ADAPTERS, echo=out.append)
        say(f'a rerun of the batch after the seal: exit {rc2} ({out[-1][:100]})')
        ok &= rc2 == 2
    say(f'{"PASS" if ok else "CHECK"} in {time.time() - t0:.0f} s')
    return bool(ok)


if __name__ == '__main__':
    print(f'MODE H DRESS REHEARSAL (invented data; installed code; full cohort; first update {EXTRA} draws past the holdout)')
    results = [one(p) for p in (POWERBALL, OZLOTTO)]
    print('DRESS REHEARSAL PASS' if all(results) else 'DRESS REHEARSAL: see the lines marked NOTE, NOT REFUSED or CHECK')
    sys.exit(0 if all(results) else 1)
