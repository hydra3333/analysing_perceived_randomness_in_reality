"""Recompute the ratified R2 5.5 / TIE v0.2 synthetic E_1 goldens with the
committed v0.3 module. Run from the repository root:
  python -I scripts/06_e1_synthetic_goldens.py
Expected: df21871f... / 7ce5ab1b... / 7b43d659...
"""
import hashlib, json, sys
sys.path.insert(0, 'src/methods')
from _common import e1_historical_appearance_frequency_v0_3 as m
d = json.load(open('tests/p3_e1_synthetic_v0_3.json'))
prefix = m.training_prefix(d['rows'], d['target'])
td = m.training_sha256(prefix)
print('training view  ', td)
print('MAIN label 3   ', m.tie_digest(td, d['target'], 'MAIN', 3))
print('forecast       ', hashlib.sha256(m.canonical_bytes(m.candidate_forecast(d['rows'], d['target']))).hexdigest())
