"""Export CODE-1's synthetic C1, C2, D1 and task records for the reviewer's independent R-4 T-05 oracle (EX_032).

Usage: python3 -I e2r_oracle_export.py TREE ORACLE_OUT RECORDS_OUT
Reads the oracle's manifest and its synthetic fixtures (outside the repository); for each of the 192
cases, loads the DrawView through the installed reader, builds the task through CODE-1, runs the
synthetic contract test double and assembles C1 and C2 through CODE-1, and writes canonical C1, C2,
D1 (freeze receipt binding that case's master SHA), TASK_C1 and TASK_C2 in the oracle's layout.
"""
import json, sys
from pathlib import Path

tree, oracle_out, records = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
for p in (tree / 'src' / 'methods', tree / 'tests'):
    sys.path.insert(0, str(p))
import e2r_fixtures as F
import _common.contract_vocab as V
from _common.contract_forecast import assemble_diagnostic, assemble_forecast
from _common.contract_receipts import validate_diagnostic_receipt, validate_freeze_receipt
from _common.contract_records import canonical, validate_declaration
from _common.contract_task import record_task

manifest = json.loads((oracle_out / 'oracle_manifest.json').read_bytes())
assert not records.exists()
decls = {g: F.declaration(g, dates=True, method='E_9000', variant='REVIEWER_T05_SYNTHETIC_V1') for g in ('POWERBALL', 'OZLOTTO')}
for d in decls.values():
    validate_declaration(d)
n = 0
for c in manifest['cases']:
    decl = decls[c['game_id']]
    root = oracle_out / 'fixtures' / c['case']
    req, view, task = F.load_view(root, decl, c['target_draw_number'], c['observation_view'], c['master_sha256'],
                                  include_dates=c['include_dates'])
    out = F.probe_method(view, task)
    c1 = assemble_forecast(decl, task, view, out)
    c2 = assemble_diagnostic(decl, task, view, out)
    d1 = F.receipt_for(c1, sha=c['master_sha256'])
    validate_freeze_receipt(d1, c1)
    validate_diagnostic_receipt(F.receipt_for(c2, sha=c['master_sha256']), c2)
    stem = records / c['case']
    stem.mkdir(parents=True)
    for name, rec in (('C1', c1), ('C2', c2), ('D1', d1), ('TASK_C1', record_task(task, V.FORECAST).as_dict()),
                      ('TASK_C2', record_task(task, V.DIAGNOSTIC).as_dict())):
        (stem / f'{name}.json').write_bytes(canonical(rec))
        n += 1
print(n, 'files exported to', records)
