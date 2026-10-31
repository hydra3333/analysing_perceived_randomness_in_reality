"""Build WF-1B's MEASURE_REGISTRY_V1.json and FAMILY_REGISTRY_V1.json (Claude, 31 Oct 2026).

Usage: python3 -I make_wf1b_registries.py REPO_TREE OUT_DIR
- Measure texts are taken word for word from R3 v0.5 section 17 (17.6's "One line" and "Short explanation" for the
  stage-2 measures; 17.3.5A's mode texts; 17.5.2's labels; 17.3.7's statuses; 17.3.9's tiers and PO-1..PO-4).
- Families (design v0.1r1 6.7, WF1-6): MR7.MAIN for both games and MR7.PB for Powerball, over TOP and WORST of every
  released variant in the installed registry (40 per game since E_1 revision 2), M = 80, default windows (R3 17.3.6).
Reads only the R3 document and the installed contract registry (no data folder)."""
import hashlib, json, re, sys
from pathlib import Path

repo, out = Path(sys.argv[1]), Path(sys.argv[2])
R3 = repo / 'doc' / 'Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md'
raw = R3.read_bytes()
assert hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest() == '53e30a3e649b48b8a88923d08bf578caf04a4ce93d6ea6468891ca97e93a57b6'
lines = raw.decode('utf-8').replace('\r\n', '\n').split('\n')


def section(start_heading, stop_prefix):
    i = next(k for k, l in enumerate(lines) if l.startswith(start_heading))
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith(stop_prefix))
    return lines[i:j]


def field(block, name):
    hits = [l for l in block if l.startswith(f'- **{name}:**')]
    assert len(hits) == 1, (name, block[0])
    return hits[0][len(f'- **{name}:** '):]


measures = []
for mid in ('MR0', 'MR1', 'MR4', 'MR5', 'MR7', 'MR16'):
    blk = section(f'#### {mid} - ', ('#### ', '### '))
    heading = blk[0][len('#### '):]
    measures.append({'id': mid, 'heading': heading, 'one_liner': field(blk, 'One line'),
                     'short_explanation': field(blk, 'Short explanation')})

modes_blk = section('#### 17.3.5A', '**Rules:**')
modes = {}
for code in ('WF', 'IS'):
    k = next(i for i, l in enumerate(modes_blk) if l.startswith(f'**{code} - '))
    modes[code] = {'display': modes_blk[k].strip('*'), 'plain_meaning': modes_blk[k + 1][2:]}

lab_blk = section('#### 17.5.2', '#### 17.5.3')
labels = [{'label': m.group(1), 'meaning': m.group(2)} for l in lab_blk
          for m in [re.match(r'\| `([A-Z0-9_]+)` \| (.*) \|$', l)] if m]
stat_blk = section('#### 17.3.7 ', '#### 17.3.7A')
statuses = [{'status': m.group(1), 'meaning': m.group(2)} for l in stat_blk
            for m in [re.match(r'  - `([A-Z_]+)` \((.*)\);?\.?$', l)] if m]
tier_blk = section('#### 17.3.9', '### 17.4')
tiers = [{'tier': m.group(1), 'meaning': m.group(2)} for l in tier_blk for m in [re.match(r'- `([A-Z0-9_]+)`: (.*?);?$', l)] if m]
origins = [{'id': m.group(1), 'origin': m.group(2), 'distinguished_by': m.group(3)} for l in tier_blk
           for m in [re.match(r'\| (PO-[1-4]) \| (.*?) \| (.*) \|$', l)] if m]
assert len(labels) == 8 and len(statuses) == 5 and len(tiers) == 4 and len(origins) == 4, (len(labels), len(statuses), len(tiers), len(origins))
src = {'document': R3.name, 'sha256_lf': hashlib.sha256(raw.replace(b'\r\n', b'\n')).hexdigest()}
mreg = {'schema': 'MEASURE_REGISTRY_V1', 'source': src, 'stage': 2, 'measures': measures, 'modes': modes,
        'calibration_labels': labels, 'report_statuses': statuses, 'evidence_tiers': tiers, 'pattern_origins': origins}

# ---- families
sys.path[:0] = [str(repo / 'src' / 'methods')]
from _common.contract_registry import InstalledRegistry
import _common.contract_registry as REG
reg = InstalledRegistry(Path(REG.DATA_ROOT))
fams = []
windows = {'POWERBALL': (1286, 1576), 'OZLOTTO': (1474, 1693)}
for game in ('POWERBALL', 'OZLOTTO'):
    roster = []
    for (g, m, v) in sorted(reg.chain_keys(), key=lambda k: (int(k[1][2:]), k[2])):
        if g == game and reg.active_entry(g, m, v)['registry_status'] == 'SUPPORTED':
            roster += [f'{game}:{m}:{v}:{ro}:WF' for ro in ('TOP', 'WORST')]
    assert len(roster) == 80, (game, len(roster))
    for ch in (('MAIN', 'PB') if game == 'POWERBALL' else ('MAIN',)):
        fams.append({'family_id': f'WF1_{game}_MR7_{ch}_V1', 'game_id': game, 'measure': f'MR7.{ch}',
                     'statistic': 'P_up', 'mode': 'WF', 'window_first': windows[game][0], 'window_last': windows[game][1],
                     'grid': 'OWN_SET', 'M': len(roster), 'roster': roster,
                     'roster_digest': hashlib.sha256('\n'.join(roster).encode('ascii')).hexdigest(),
                     'decision': 'WF1-6 (owner, 30 October 2026); design v0.1r1 section 6.7'})
freg = {'schema': 'FAMILY_REGISTRY_V1', 'registered': 'installed with WF-1B, before any RANKING_REPORT', 'families': fams}
out.mkdir(parents=True, exist_ok=True)
for name, obj in (('MEASURE_REGISTRY_V1.json', mreg), ('FAMILY_REGISTRY_V1.json', freg)):
    (out / name).write_bytes((json.dumps(obj, indent=1, ensure_ascii=True, sort_keys=False) + '\n').encode('ascii'))
print('measures', len(measures), 'labels', len(labels), 'families', [f['family_id'] for f in fams])
