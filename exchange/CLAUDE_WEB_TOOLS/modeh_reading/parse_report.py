"""Parse a Mode H method-rankings report (.txt, value-free) into tables. Reads only the report text."""
import re, sys, json
from collections import OrderedDict

def parse(path):
    lines = open(path, encoding='ascii').read().split('\n')
    part = None; tables = OrderedDict(); cur = None; meta = {'families': []}
    head = re.compile(r'^(MR[0-9A-Za-z.\-]+) - (descriptive|significance) ranking')
    rowA = re.compile(r'^\s*(\d+)(=?)\s+(\S+)\s+(\d+)\s+(.*)$')
    for i, ln in enumerate(lines):
        if ln.startswith('PART A'): part = 'A'
        elif ln.startswith('PART B'): part = 'B'
        elif ln.startswith('GLOSSARY') or ln.startswith('Families (global') or ln.startswith('PER-TRACK'): cur = None
        m = head.match(ln)
        if m:
            cur = (part, m.group(1)); tables[cur] = []; continue
        if ln.startswith('  MODEH_') or ln.startswith('    N1 maximum'):
            meta['families'].append(ln.strip())
        if cur is None: continue
        m = rowA.match(ln)
        if m and ':' in m.group(3):
            tables[cur].append({'rank': int(m.group(1)), 'tie': bool(m.group(2)), 'unit': m.group(3), 'n': int(m.group(4)), 'rest': m.group(5).strip(), 'extra': []})
        elif tables[cur] and ln.startswith('       ') and ln.strip():
            tables[cur][-1]['extra'].append(ln.strip())
    return lines, tables, meta

if __name__ == '__main__':
    lines, tables, meta = parse(sys.argv[1])
    for k, v in tables.items():
        print(k, len(v))
    print(json.dumps(meta, indent=1))
