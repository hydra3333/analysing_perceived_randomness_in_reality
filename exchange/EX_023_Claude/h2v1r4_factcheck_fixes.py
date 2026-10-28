"""Apply Claude's proposed H-2 v1r4 factual corrections H2F-01..03 (Claude, 28 Oct 2026). For the reviewer's disposition.
Usage: python3 -I h2v1r4_factcheck_fixes.py H2_V1R4_DRAFT H2_V1R3 OUT
Each old string must occur exactly once; inserted text is ASCII; the rights region (## 2 up to ## 4) must stay byte-identical to v1r3."""
import hashlib, sys
src, v13, out = sys.argv[1:4]
b = open(src, 'rb').read(); assert hashlib.sha256(b).hexdigest() == 'f27b7612f74ae89a242cb5618d4c3808e41e4c7196e1d71945d119e3eaac3d91'
t = b.decode('utf-8')
OLD_CMD = ('```bat\nset PYTHONPATH=src;src\\methods;tests\n.venv\\Scripts\\python.exe -m unittest tests.test_multigame_v011_reader_contracts '
           'tests.test_multigame_v011_static_and_timing tests.test_multigame_launch_and_manifest_v0_8 tests.test_multigame_exit_receipt_v0_8 '
           'tests.test_multigame_science_allowlist_v0_8 tests.test_multigame_console_and_synthetic_scorer_v0_4 tests.test_p2_r1_t05_hardening_v1\nset PYTHONPATH=\n```')
NEW_CMD = ('```bat\nset PYTHONPATH=src;src\\methods;tests\n.venv\\Scripts\\python.exe -m unittest tests.test_multigame_reader_contracts '
           'tests.test_multigame_static_and_timing tests.test_multigame_launch_and_manifest tests.test_multigame_exit_receipt '
           'tests.test_multigame_science_allowlist tests.test_multigame_console_and_synthetic_scorer tests.test_t05_hardening\nset PYTHONPATH=\n```\n\n'
           'The other 19 current offline tests run with the same `PYTHONPATH`: `tests.test_e1_standalone tests.test_multigame_windows_lifecycle_review` '
           '(79 in all; H-1 v1r3 section 7.1).')
EDITS = [
    # H2F-01: the suite command used the pre-NAMES-1 module names
    ('The updated suite includes `tests.test_p2_r1_t05_hardening_v1` and the non-skipping protected AST test. The TH-1 v1r2 owner-installation '
     'instructions give the revised seven-module offline suite invocation for **Windows CMD**, including its temporary environment assignment '
     'and restoration, as follows:',
     'The updated suite included `tests.test_p2_r1_t05_hardening_v1` (since NAMES-1 at `52ebeaa`: `tests.test_t05_hardening`) and the '
     'non-skipping protected AST test. The TH-1 v1r2 owner-installation instructions gave a seven-module offline suite invocation for '
     '**Windows CMD** under the pre-NAMES-1 module names. **Since NAMES-1, the current seven-module standard suite (60 tests) is**, with its '
     'temporary environment assignment and restoration:'),
    (OLD_CMD, NEW_CMD),
    # H2F-02: DOC-2 sequence
    ('the original install had a recorded STOP/deviation followed by owner-accepted two-commit finalisation. Never describe the initial installer itself as PASS.',
     'it arrived in two commits: the owner had already committed four of its eight files, byte-identical, in `2c76664` (merged as `f300f2d`), '
     'and `908db9e` added the other four. The installer\'s committed check STOPped on its one-commit rule only (its blob checks had passed for '
     'all eight files); the owner accepted the two-commit delivery as a one-off exception, not a precedent (register v0.8). Never describe that STOP as PASS.'),
    ('One DOC-2 installation required two commits and a separately owner-accepted STOP/deviation record;',
     'The DOC-2 installation arrived in two commits, its committed check STOPped on the one-commit rule, and the owner separately accepted that deviation as a one-off exception;'),
    # H2F-03: exchange records are pushed and checked
    ('EX_021 was received with DOC-3 status; do not assume it was already pushed unless checked.',
     'EX_021 (DOC-3 installed) is recorded at `edc0f07` and EX_022 (this draft) at `2bb0a3e`; check the highest recorded number before choosing the next.'),
]
for old, new in EDITS:
    assert t.count(old) == 1, (t.count(old), old[:70])
    assert all(ord(c) < 128 for c in new)
    t = t.replace(old, new)
r = lambda x: x[x.index(b'\n## 2') + 1: x.index(b'\n## 4') + 1]
o = t.encode('utf-8')
assert r(o) == r(open(v13, 'rb').read()), 'rights region changed'
open(out, 'wb').write(o)
print(out, hashlib.sha256(o).hexdigest(), len(t.splitlines()), 'lines; rights region identical', len(r(o)), 'bytes')
