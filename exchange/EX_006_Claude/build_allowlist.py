"""NAMES-1 v0.2 design evidence: list and classify every authorised literal change (N1-C01).

Usage: python3 -I build_allowlist.py BASE_TREE OUT_TSV
BASE_TREE is an export of commit 38fc60e. Every whole-word occurrence of an old map name in an
in-scope .py file under src/ or tests/ is one row: new path, old path, line, old token, new token,
category. An import line is category A-IMPORT. Every other occurrence must appear in the exact
table NON_IMPORT below, and every entry of that table must occur; otherwise the script stops.
So nothing unclassified can be authorised, and nothing authorised can go missing.
"""
import re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rename_map as R

NON_IMPORT = {  # (old path, line, old token) -> category
    ('src/Powerball_Experiment_Coordinator.py', 1105, 'multigame_coordinator_exit_receipt_v2'): 'B1-ORIGIN',
    ('tests/test_multigame_exit_receipt_v0_8.py', 261, 'multigame_coordinator_exit_receipt_v2'): 'B1-ORIGIN',
    ('tests/test_multigame_exit_receipt_v0_8.py', 280, 'multigame_coordinator_exit_receipt_v2'): 'B1-ORIGIN',
    ('src/coordinator_private/multigame_coordinator_exit_receipt_v2.py', 31, 'multigame_result_registry_v1'): 'B2-CONTRACT-FILE',
    ('src/coordinator_private/multigame_coordinator_exit_receipt_v2.py', 31, 'multigame_console_protocol_v1'): 'B2-CONTRACT-FILE',
    ('tests/test_multigame_v011_static_and_timing.py', 78, 'multigame_windows_lifecycle_v1'): 'B3-SOURCE-READ',
    ('tests/test_multigame_windows_lifecycle_review_v0_9.py', 112, 'multigame_windows_lifecycle_v1'): 'B3-SOURCE-READ',
    ('tests/test_multigame_v011_static_and_timing.py', 99, 'game_draws_reader_v1'): 'C-FIREWALL',
    ('tests/test_multigame_v011_static_and_timing.py', 102, 'game_draws_reader_v1'): 'C-FIREWALL',
    ('tests/test_p3_e1_standalone_v0_1.py', 213, 'e1_training_view_v0_1'): 'A-PATCH',
    ('tests/test_p3_e1_standalone_v0_1.py', 261, 'e1_training_view_v0_1'): 'A-PATCH',
    ('src/methods/_common/multigame_e1_v1.py', 3, 'e1_historical_appearance_frequency_v0_3'): 'D-DOC',
}
IMPORT_LINE = re.compile(r'(from\s+\S+\s+import\b|import\s+\S+)')

base, out = Path(sys.argv[1]), sys.argv[2]
bare, fmap = R.bare(), R.files()
pat = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, bare), key=len, reverse=True)) + r')\b')
rows, seen = [], set()
for p in sorted({*(base / 'src').rglob('*.py'), *(base / 'tests').rglob('*.py')}):
    rel = p.relative_to(base).as_posix()
    src = p.read_text(encoding='utf-8')
    lines = src.splitlines()
    for m in pat.finditer(src):
        ln = src.count('\n', 0, m.start()) + 1
        key = (rel, ln, m.group(1))
        if key in NON_IMPORT:
            cat = NON_IMPORT[key]
            seen.add(key)
        elif IMPORT_LINE.match(lines[ln - 1].strip()):
            cat = 'A-IMPORT'
        else:
            sys.exit(f'UNCLASSIFIED {rel}:{ln}: {lines[ln - 1].strip()}')
        rows.append((fmap.get(rel, rel), rel, ln, m.group(1), bare[m.group(1)], cat))
missing = set(NON_IMPORT) - seen
if missing:
    sys.exit(f'EXPECTED BUT NOT FOUND: {sorted(missing)}')
with open(out, 'w', newline='\n') as f:
    f.write('new_path\told_path\tline\told_token\tnew_token\tcategory\n')
    for r in rows:
        f.write('\t'.join(map(str, r)) + '\n')
print(len(rows), 'rows;', len({r[1] for r in rows}), 'files;', dict(sorted(Counter(r[5] for r in rows).items())))
