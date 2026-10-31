"""WF-1A (Claude, 31 October 2026): the two existing tests that pinned ENABLE_CONTRACT_REAL_DEVELOPMENT to False now
pin it to True (design v0.1r1 5.5; owner decision WF1-3), and the runner's refusal is still tested with the switch
patched off. Every old string must occur exactly once. Usage: python3 -I edit_tests_wf1a.py TREE"""
import sys
from pathlib import Path
T = Path(sys.argv[1]) / 'tests'
def edit(name, pairs):
    p = T / name; t = p.read_text('utf-8')
    for o, n in pairs:
        assert t.count(o) == 1, (name, o[:60]); t = t.replace(o, n)
    assert t.isascii(); p.write_text(t, 'utf-8'); print(f'{name}: {len(pairs)} edits')
edit('test_e2r_runner.py', [
    ("""    def test_real_development_is_switched_off(self):
        self.assertIs(CR.ENABLE_CONTRACT_REAL_DEVELOPMENT, False)
""", """    def test_real_development_switch_is_on_since_wf1a_and_refuses_when_off(self):
        self.assertIs(CR.ENABLE_CONTRACT_REAL_DEVELOPMENT, True)          # WF-1A (design v0.1r1 5.5; WF1-3)
"""),
    ("""        with mock.patch.object(CR, 'load_pinned_draw_view', side_effect=AssertionError('data read')):
            with self.assertRaises(CR.RunRefused) as cm:
                CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=self.td,
                                       run_root=self.td / 'runs')
        self.assertEqual(cm.exception.reason, 'REAL_DEVELOPMENT_DISABLED')""",
     """        with mock.patch.object(CR, 'ENABLE_CONTRACT_REAL_DEVELOPMENT', False), \\
                mock.patch.object(CR, 'load_pinned_draw_view', side_effect=AssertionError('data read')):
            with self.assertRaises(CR.RunRefused) as cm:
                CR.run_contract_method(req, compute=e_001.compute, verify=e_001.verify, repo_root=self.td,
                                       run_root=self.td / 'runs')
        self.assertEqual(cm.exception.reason, 'REAL_DEVELOPMENT_DISABLED')"""),
])
edit('test_e2r_dispatch.py', [
    ("""    def test_switch_closed_and_no_flag_in_the_tree(self):
        self.assertIs(CR.ENABLE_CONTRACT_REAL_DEVELOPMENT, False)""",
     """    def test_switch_open_since_wf1a_and_no_flag_in_the_tree(self):
        self.assertIs(CR.ENABLE_CONTRACT_REAL_DEVELOPMENT, True)          # WF-1A (design v0.1r1 5.5; WF1-3)"""),
])
