"""Hash a markdown section (heading to next heading of same or higher level)
in a base and a candidate; protected blocks must hash identically.
Usage: python -I 03_protected_blocks.py base.md candidate.md "<heading regex>" [...]
Example patterns: r'^#+\s+0\.4\b'  r'^#+\s+7\.?\s'  r'^## 5C'  r'^#+\s+E_1\b'
Check each pattern matches exactly one heading (it prints NOHEAD otherwise).
"""
import hashlib, re, sys
def section(path, pat):
    lines = open(path, encoding='utf-8').read().split('\n')
    idx = [i for i, l in enumerate(lines) if re.match(pat, l)]
    if len(idx) != 1:
        return ('NOHEAD', len(idx))
    i = idx[0]; level = len(re.match(r'^(#+)', lines[i]).group(1)); j = i + 1
    while j < len(lines):
        m = re.match(r'^(#+)\s', lines[j])
        if m and len(m.group(1)) <= level:
            break
        j += 1
    return (hashlib.sha256('\n'.join(lines[i:j]).encode()).hexdigest()[:16], j - i)
base, cand = sys.argv[1], sys.argv[2]
for pat in sys.argv[3:]:
    a, b = section(base, pat), section(cand, pat)
    print('SAME' if a == b and a[0] != 'NOHEAD' else 'DIFFERENT', pat, a, b)
