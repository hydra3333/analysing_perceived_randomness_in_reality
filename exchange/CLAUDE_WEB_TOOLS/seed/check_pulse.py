"""Check the owner's saved NIST pulse against EX_103's acceptance row (design v0.1r1 8.1-8.2). Usage: check_pulse.py FILE"""
import hashlib, json, re, sys
raw = open(sys.argv[1], 'rb').read()
print('file sha256', hashlib.sha256(raw).hexdigest(), 'bytes', len(raw), 'BOM' if raw.startswith(b'\xef\xbb\xbf') else 'no BOM')
p = json.loads(raw.decode('utf-8-sig'))['pulse']
checks = {
    'version 2.0': p.get('version') == '2.0',
    'chainIndex 2': p.get('chainIndex') == 2,
    'timeStamp 2026-10-31T10:30:00.000Z': p.get('timeStamp') == '2026-10-31T10:30:00.000Z',
    'statusCode 0': p.get('statusCode') == 0,
    'outputValue 128 upper-case hex': isinstance(p.get('outputValue'), str) and re.fullmatch(r'[0-9A-F]{128}', p['outputValue']) is not None,
}
for k, v in checks.items():
    print(('PASS ' if v else 'FAIL ') + k)
print('uri', p.get('uri')); print('pulseIndex', p.get('pulseIndex')); print('certificateId', p.get('certificateId'))
ov = p.get('outputValue', '')
print('outputValue pieces', [ov[i:i + 32] for i in range(0, 128, 32)])
print('ALL PASS' if all(checks.values()) else 'NOT ACCEPTED')
