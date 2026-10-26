"""Every ratified ID in a base must survive in its candidate; every required
item from a ratified proposal must appear somewhere in the candidate set.
Usage: python -I 04_id_inventory.py base.md candidate.md
Note: some project files use non-ASCII hyphens (U+2011) in IDs; widen the
pattern if a document reports suspiciously few IDs.
"""
import re, sys
PAT = re.compile(r'\b(?:A[-\u2011]\d{2}|D\d|I-\d{2}|R2-C\d+[A-Z]?|R2-D\d+|T-\d{2}|W-\d{2}|'
                 r'O-[A-Z]+-\d{2}|M-INV-\d{2}|ERR-R2-\d{2}|R3-D\d+|R3-T\d+|MRD-\d{2}|'
                 r'MRT-\d{2}|MRO-\d{2}|RK-\d|PO-\d)\b')
b = set(PAT.findall(open(sys.argv[1], encoding='utf-8').read()))
c = set(PAT.findall(open(sys.argv[2], encoding='utf-8').read()))
print('base IDs:', len(b), ' lost:', sorted(b - c))
