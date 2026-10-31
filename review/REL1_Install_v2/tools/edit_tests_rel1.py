"""REL-1 (Claude, 31 October 2026): the status-expectation edits to five existing test files (design v0.1r1 section 4).

After REL-1 the 39 variants are SUPPORTED and their flags are gone, so the "as installed" tests expect release,
and the "through the contract" tests use the installed SUPPORTED entries instead of appending a simulated release
to a copy. No numerical expectation changes. Every old string must occur exactly once (or the stated number of
times). Usage: python3 -I edit_tests_rel1.py TREE
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
T = tree / 'tests'

SIM20 = """                    e2 = dict(e1, entry_sequence=2, registry_status='SUPPORTED', previous_entry_digest=record_digest(e1),
                              registry_status_reason='test harness: simulated release')
                    C.append_entry(self.data, e2)
"""
REL20 = """                    e2 = e1                    # REL-1: the installed entry_0002 is already SUPPORTED
                    self.assertEqual((e2['entry_sequence'], e2['registry_status']), (2, 'SUPPORTED'))
"""
CHAIN = "[(1, 'FORMULA_OPEN')])"
CHAIN_NEW = "[(1, 'FORMULA_OPEN'), (2, 'SUPPORTED')])   # REL-1"
REFUSED20 = """                    with self.assertRaises(DispatchRefused) as cm:
                        dispatch_gate(req)
                    self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
                self.assertEqual(method_status(profile.game_id, name), 'FORMULA_OPEN')
"""
ADMITTED20 = """                    entry, _decl = dispatch_gate(req)                  # REL-1: admitted; reads no data
                    self.assertEqual(record_digest(entry), record_digest(e))
                self.assertEqual(method_status(profile.game_id, name), 'SUPPORTED')
"""
FLAGS = "            self.assertTrue((METHODS_ROOT / method_folder(name) / 'IN_DEVELOPMENT.txt').is_file())\n"
FLAGS_NEW = "            self.assertFalse((METHODS_ROOT / method_folder(name) / 'IN_DEVELOPMENT.txt').exists())   # REL-1\n"
LIST = "['IN_DEVELOPMENT.txt', '__init__.py', 'contract.py', 'variants.py'])"
LIST_NEW = "['__init__.py', 'contract.py', 'variants.py'])   # REL-1 removed the flag"


def edit(name, pairs):
    p = T / name
    t = p.read_text('utf-8')
    for old, new, count in pairs:
        n = t.count(old)
        assert n == count, (name, n, count, old[:70])
        t = t.replace(old, new)
    assert t.isascii(), name
    p.write_text(t, 'utf-8')
    print(f'{name}: {len(pairs)} edits')


for name, refused_name, flags_name in (
        ('test_e3_e4_polynomial.py', 'test_every_request_is_refused_and_the_roster_says_formula_open',
         'test_flags_present_and_runner_lists_both'),
        ('test_wave1_frequency.py', 'test_every_request_is_refused_and_the_roster_says_formula_open',
         'test_flags_present_and_runner_lists_each'),
        ('test_wave2_recurrence.py', 'test_every_request_is_refused_and_the_roster_says_formula_open',
         'test_flags_present_and_runner_lists_each')):
    edit(name, [
        (SIM20, REL20, 1),
        (CHAIN, CHAIN_NEW, 1),
        (REFUSED20, ADMITTED20, 1),
        (f'def {refused_name}(self):', 'def test_every_request_is_admitted_and_the_roster_says_supported(self):', 1),
        (FLAGS, FLAGS_NEW, 1),
        (f'def {flags_name}(self):', f'def {flags_name.replace("present", "absent")}(self):', 1),
        (LIST, LIST_NEW, 1),
    ])

edit('test_e6_beta_bernoulli.py', [
    ("""                e2 = dict(e1, entry_sequence=2, registry_status='SUPPORTED', previous_entry_digest=record_digest(e1),
                          registry_status_reason='test harness: simulated release')
                C.append_entry(self.data, e2)
""", """                e2 = e1                        # REL-1: the installed entry_0002 is already SUPPORTED
                self.assertEqual((e2['entry_sequence'], e2['registry_status']), (2, 'SUPPORTED'))
""", 1),
    ('# ---------------------------------------------------------------- 6.6 as installed: in development, refused',
     '# ---------------------------------------------------------------- 6.6 as installed: released by REL-1', 1),
    ("                self.assertEqual([(e['entry_sequence'], e['registry_status']) for e in chain], [(1, 'FORMULA_OPEN')])",
     "                self.assertEqual([(e['entry_sequence'], e['registry_status']) for e in chain], [(1, 'FORMULA_OPEN'), (2, 'SUPPORTED')])   # REL-1", 1),
    ("""    def test_every_e6_request_is_refused_before_any_data_is_read(self):""",
     """    def test_every_e6_request_is_admitted_and_the_roster_says_supported(self):""", 1),
    ("""                    with self.assertRaises(DispatchRefused) as cm:
                        dispatch_gate(req)
                    self.assertEqual(cm.exception.reason, 'NOT_SUPPORTED')
            self.assertEqual(method_status(game, 'E_6'), 'FORMULA_OPEN')
""", """                    entry, _decl = dispatch_gate(req)                  # REL-1: admitted; reads no data
                    self.assertEqual(record_digest(entry), record_digest(e))
            self.assertEqual(method_status(game, 'E_6'), 'SUPPORTED')
""", 1),
    ("""    def test_supported_but_flagged_is_still_refused(self):
        self.assertTrue((METHODS_ROOT / 'E_006' / 'IN_DEVELOPMENT.txt').is_file())
        with tempfile.TemporaryDirectory() as td:
            data = C.copy_data_root(Path(td))
            reg = InstalledRegistry(data)
            e1 = reg.active_entry('POWERBALL', 'E_6', FULL)
            e2 = dict(e1, entry_sequence=2, registry_status='SUPPORTED', previous_entry_digest=record_digest(e1))
            C.append_entry(data, e2)
            req = C.request(reg.declaration(e1['declaration_digest']), e2, POWERBALL.first_draw + 10, 'f' * 64)
            with C.installed(data=data):                              # the real method folders, flag present
                with self.assertRaises(DispatchRefused) as cm:
                    dispatch_gate(req)
            self.assertEqual(cm.exception.reason, 'IN_DEVELOPMENT_FLAG_PRESENT')
""", """    def test_supported_but_flagged_is_still_refused(self):
        self.assertFalse((METHODS_ROOT / 'E_006' / 'IN_DEVELOPMENT.txt').exists())   # REL-1 removed it
        with tempfile.TemporaryDirectory() as td:
            methods = Path(td) / 'methods'                            # a method tree where E_6 is flagged again
            (methods / 'E_006').mkdir(parents=True)
            (methods / 'E_006' / 'IN_DEVELOPMENT.txt').write_text('test harness')
            reg = InstalledRegistry()
            e2 = reg.active_entry('POWERBALL', 'E_6', FULL)
            self.assertEqual(e2['registry_status'], 'SUPPORTED')
            req = C.request(reg.declaration(e2['declaration_digest']), e2, POWERBALL.first_draw + 10, 'f' * 64)
            with C.installed(methods=methods):                        # the installed registry, flag present
                with self.assertRaises(DispatchRefused) as cm:
                    dispatch_gate(req)
            self.assertEqual(cm.exception.reason, 'IN_DEVELOPMENT_FLAG_PRESENT')
""", 1),
    ("['IN_DEVELOPMENT.txt', '__init__.py', 'beta_bernoulli.py', 'contract.py'])",
     "['__init__.py', 'beta_bernoulli.py', 'contract.py'])   # REL-1 removed the flag", 1),
])

edit('test_e2r_dispatch.py', [
    ("""            want = {f'E_{i}': ('SUPPORTED' if i == 1 else 'FORMULA_OPEN') for i in range(1, 63)}""",
     """            released = {1, 2, 3, 4, 6, 7, 8, 9, 10, 17, 18, 19}          # E_1, and REL-1's eleven methods
            want = {f'E_{i}': ('SUPPORTED' if i in released else 'FORMULA_OPEN') for i in range(1, 63)}""", 1),
])
