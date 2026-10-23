"""Write only an invented U-view CSV; NEVER read Powerball source_data."""
from __future__ import annotations
import csv
import hashlib
import io
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests' / 'p3_e1_synthetic_v0_3.json'
DEST = ROOT / 'transitory_data' / 'p3_synthetic_fixtures' / 'e1_synthetic_u_1152.csv'
COLUMNS = ['Draw_Number', 'Date', *[f'Ball_{k}' for k in range(1, 8)], 'Powerball']

def main() -> None:
    fixture = json.loads(FIXTURE.read_text(encoding='utf-8'))
    text = io.StringIO(newline='')
    writer = csv.writer(text, lineterminator='\n')
    writer.writerow(COLUMNS)
    for row in fixture['rows']:
        when = date(2018, 4, 19) + timedelta(days=7*(row['draw']-1144))
        writer.writerow([row['draw'], when.isoformat(), *row['main'], row['powerball']])
    data = text.getvalue().encode('utf-8')
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        if DEST.is_symlink() or not DEST.is_file() or DEST.read_bytes() != data:
            raise RuntimeError('Existing synthetic fixture differs: REFUSE OVERWRITE')
    else:
        with DEST.open('xb') as fd:
            fd.write(data)
            fd.flush()
            import os
            os.fsync(fd.fileno())
    print(f'SYNTHETIC CSV READY: {DEST}')
    print(f'SHA-256: {hashlib.sha256(data).hexdigest()}')

if __name__ == '__main__':
    main()
