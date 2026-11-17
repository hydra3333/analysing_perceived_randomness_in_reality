"""MHUP-B slice 1: counted edits to the existing tests (code plan v0.3 section 3 and Appendix L of the design).

1. The three baseline failures (plan section 3), each fixed so the test keeps what it proves:
   - tests/test_multigame_reader_contracts.py, two tests tied to the version-1 masters (readiness finding F-2);
   - tests/test_mhupa_launchers.py, the ignore-list test (the owner committed the score records at cc665ce).
2. The tests that named FINAL_NEXT_DRAW as reserved (it is unreserved by this package, design 6.4).
3. The static firewall's allowances for the new evaluator program.
Every old string must occur exactly once. Usage: python3 -I edit_tests_slice1.py TREE
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()


def edit(rel, pairs):
    p = tree / rel
    s = p.read_bytes().decode('ascii')
    assert '\r' not in s, rel
    for a, b in pairs:
        assert s.count(a) == 1, (rel, s.count(a), a[:80])
        s = s.replace(a, b)
    p.write_bytes(s.encode('ascii'))
    print('edited', rel, len(pairs))


# ---------------------------------------------------------------- 1a. the reader tests (F-2)
edit('tests/test_multigame_reader_contracts.py', [
    ("""    def test_master_source_and_ledger_file_hashes(self):
        for game in SHA:
            with self.subTest(game=game):
                b=(ROOT/'source_data'/f'{game}_results_master.csv').read_bytes()
                self.assertEqual(hashlib.sha256(b).hexdigest(),SHA[game])
                p=POWERBALL if game=='POWERBALL' else OZLOTTO
                self.assertEqual((p.holdout_first,p.holdout_last),
                                 (1577,1586) if game=='POWERBALL' else (1694,1703))
""",
     """    def test_master_source_and_ledger_file_hashes(self):
        \"\"\"The master is bound to its ledger by SHA-256. MHUP-B slice 1 (readiness finding F-2): the real masters grow
        with every update, so the pinned values below are the VERSION-1 hashes, which stay true for ever: the ledger's
        INIT row carries them and the master's version-1 prefix must still hash to them. The current master is checked
        with no pinned value at all, through the installed version-2 chain and prefix rules. And the same binding is
        proved on a synthetic INIT master whose hash this test computes from the bytes it wrote.\"\"\"
        from _common import master_versions as MV
        for game in SHA:
            with self.subTest(game=game):
                p=POWERBALL if game=='POWERBALL' else OZLOTTO
                raw,rows,_evidence=MV.load_verified_source(ROOT,game)        # refuses unless the whole chain passes
                self.assertEqual((rows[0].version,rows[0].action,rows[0].master_sha256),(1,'INIT',SHA[game]))
                self.assertEqual(hashlib.sha256(MV.prefix_bytes(raw,rows[0])).hexdigest(),SHA[game])
                self.assertEqual(rows[0].last_draw,p.holdout_first-1)
                self.assertEqual(hashlib.sha256(raw).hexdigest(),rows[-1].master_sha256)
                self.assertEqual(MV.current_pin(ROOT,game),(rows[-1].version,rows[-1].master_sha256))
                self.assertEqual((p.holdout_first,p.holdout_last),
                                 (1577,1586) if game=='POWERBALL' else (1694,1703))
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for game in SHA:
                with self.subTest(synthetic=game):
                    sha,_target=fake_root(root,game)
                    written=(root/'source_data'/f'{game}_results_master.csv').read_bytes()
                    self.assertEqual(hashlib.sha256(written).hexdigest(),sha)
                    raw,rows,_evidence=MV.load_verified_source(root,game)
                    self.assertEqual((len(rows),rows[0].master_sha256,raw),(1,sha,written))
                    flipped=written[:-2]+bytes([written[-2]^1])+written[-1:]    # one bit, same length and lines
                    self.assertEqual((len(flipped),flipped.count(b'\\n')),(len(written),written.count(b'\\n')))
                    (root/'source_data'/f'{game}_results_master.csv').write_bytes(flipped)
                    with self.assertRaisesRegex(MV.LedgerRefused,'SHA-256'):
                        MV.load_verified_source(root,game)
"""),
    ("""    def test_only_legacy_e1_allowed_at_boundary(self):
        for change in (dict(method_id='E_2'),dict(variant_id='SYNTHETIC'),
                       dict(view_kind='PAIRED_DIAGNOSTIC'),dict(include_dates=True)):
            with self.subTest(change=change),self.assertRaises(ValueError):
                load_pinned_draw_view(repo_root=ROOT,run_manifest={**pin('POWERBALL',1577),**change})
        for bad in (1578,1586,1600):
            with self.assertRaises(ValueError):load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('POWERBALL',bad))
        with self.assertRaises(ValueError):load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('OZLOTTO',1694))
""",
     """    def test_only_legacy_e1_allowed_at_boundary(self):
        \"\"\"At the first holdout target of an UNOPENED game the reader admits only the legacy E_1 forecast-only request.
        MHUP-B slice 1 (readiness finding F-2): proved on a synthetic unopened project this test builds, because the
        real games were opened on 14 November 2026 and their masters now hold these draws. The positive half is
        test_boundary_admitted_once_opened.\"\"\"
        from test_e6_beta_bernoulli import write_varied_master
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            sha={g.game_id:write_varied_master(root,g,g.holdout_first,0) for g in (POWERBALL,OZLOTTO)}
            first=pin('POWERBALL',1577,sha=sha['POWERBALL'])
            v=load_pinned_draw_view(repo_root=root,run_manifest=first)          # the one legacy exception
            self.assertEqual((int(v.draw_number[0]),int(v.draw_number[-1])),(1144,1576))
            for m in self.boundary_requests(sha):
                with self.subTest(unopened=m),self.assertRaisesRegex(ValueError,'opening record'):
                    load_pinned_draw_view(repo_root=root,run_manifest=m)
            for bad in (1578,1586,1600):
                with self.assertRaises(ValueError):
                    load_pinned_draw_view(repo_root=root,run_manifest=pin('POWERBALL',bad,sha=sha['POWERBALL']))
        for bad in (1578,1586,1600):                    # the real master at its version-1 pin: beyond last draw + 1
            with self.assertRaisesRegex(ValueError,'outside the pinned version'):
                load_pinned_draw_view(repo_root=ROOT,run_manifest=pin('POWERBALL',bad))

    @staticmethod
    def boundary_requests(sha):
        first=pin('POWERBALL',1577,sha=sha['POWERBALL'])
        return [{**first,**change} for change in (dict(method_id='E_2'),dict(variant_id='SYNTHETIC'),
                dict(view_kind='PAIRED_DIAGNOSTIC'),dict(include_dates=True))]+[pin('OZLOTTO',1694,sha=sha['OZLOTTO'])]

    def test_boundary_admitted_once_opened(self):
        \"\"\"The same five requests on the same synthetic project once each game has a valid opening record: the reader
        admits them (which run modes may then use them is the request validator's, the dispatch gate's and the
        runner's business, tested in test_mhupa_gates and test_mhupb_l1_gates). An invalid opening record refuses.\"\"\"
        from test_e6_beta_bernoulli import write_varied_master
        import mhupa_fixtures as X
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            sha={g.game_id:write_varied_master(root,g,g.holdout_first,0) for g in (POWERBALL,OZLOTTO)}
            for g in (POWERBALL,OZLOTTO):
                X.write_opening_record(root,g.game_id,freeze_version=1,freeze_sha=sha[g.game_id])
            for m in self.boundary_requests(sha):
                with self.subTest(opened=m):
                    v=load_pinned_draw_view(repo_root=root,run_manifest=m)
                    self.assertEqual(int(v.draw_number[-1]),m['draw_number']-1)
            X.write_opening_record(root,'OZLOTTO',freeze_version=1,freeze_sha=sha['OZLOTTO'],owner_statement='')
            with self.assertRaisesRegex(ValueError,'opening record refused'):
                load_pinned_draw_view(repo_root=root,run_manifest=pin('OZLOTTO',1694,sha=sha['OZLOTTO']))
"""),
])

# ---------------------------------------------------------------- 1b. the ignore list
edit('tests/test_mhupa_launchers.py', [
    ("""                   'results/real/holdout/contract_runs/', 'results/real/holdout/wf_batches/**/attempts.jsonl',
                   'results/real/holdout/scores/', 'transitory_data/lock_clearances/', 'transitory_data/no_pycache_ever']
""",
     """                   'results/real/holdout/contract_runs/', 'results/real/holdout/wf_batches/**/attempts.jsonl',
                   'transitory_data/lock_clearances/', 'transitory_data/no_pycache_ever',
                   # MHUP-B (design 6.4): the weekly run folders, the session attempts ledgers and the session lock
                   'results/real/weekly/contract_runs/', 'results/real/weekly/**/SESSION_*_attempts.jsonl',
                   'results/real/weekly/**/ACTIVE_SESSION.lock', 'results/real/diagnostic/contract_runs/']
# The score records are tracked since the owner committed them on 17 November 2026 (cc665ce; decision log entry 70):
# no ignore line, commented out or not, may name either scores folder.
NEVER_IGNORED = ('results/real/development/scores', 'results/real/holdout/scores', 'results/real/weekly/POWERBALL/',
                 'results/real/weekly/OZLOTTO/', 'results/method_rankings')
"""),
    ("""        for line in GITIGNORE_LINES:
            self.assertIn(line, present, line)
""",
     """        for line in GITIGNORE_LINES:
            self.assertIn(line, present, line)
        for line in text.splitlines():
            for path in NEVER_IGNORED:
                self.assertFalse(line.strip().lstrip('#!/ ').startswith(path), line)
"""),
])

# ---------------------------------------------------------------- 2. FINAL_NEXT_DRAW is no longer reserved (design 6.4)
edit('tests/test_mhupa_gates.py', [
    ("""        # FINAL_NEXT_DRAW stays reserved in this package (no producible product), whatever its binding
        with self.assertRaises(ValueError):
            V.producible('FINAL_NEXT_DRAW', V.FORECAST)
""",
     """        # MHUP-B unreserved FINAL_NEXT_DRAW and added CATCH_UP (design v0.1r7 section 6.4); neither has a diagnostic row
        self.assertEqual(V.producible('FINAL_NEXT_DRAW', V.FORECAST), ('WF_FORECAST', 'PROSPECTIVE'))
        self.assertEqual(V.producible('CATCH_UP', V.FORECAST), ('WF_FORECAST', 'CATCH_UP'))
        for weekly_mode in ('FINAL_NEXT_DRAW', 'CATCH_UP'):
            with self.assertRaises(ValueError):
                V.producible(weekly_mode, V.DIAGNOSTIC)
"""),
])

# ---------------------------------------------------------------- 3. the static firewall (design Appendix L)
edit('tests/test_wf1b_static.py', [
    ("""                  '_common.release_records'}       # MHUP-A slice 2: the release records' one reader (4.3; EX_148 B03)
""",
     """                  '_common.release_records',       # MHUP-A slice 2: the release records' one reader (4.3; EX_148 B03)
                  # MHUP-B slice 1: the weekly records' shapes, the ledger write discipline and the score identities.
                  # All three are value-free orchestration modules; none imports method code.
                  '_common.weekly_records', '_common.jsonl_ledger', '_common.score_identities'}
"""),
    ("""        self.assertEqual(sorted(users), ['mode_h.py', 'report.py'])     # MHUP-A: the Mode H scorer (design 5.3, 6.1)
""",
     """        # MHUP-A: the Mode H scorer (design 5.3, 6.1); MHUP-B: the weekly scoring half (design 6.1, Appendix L)
        self.assertEqual(sorted(users), ['mode_h.py', 'report.py', 'weekly_score.py'])
"""),
])

# ---------------------------------------------------------------- 4. which files name the master (MHUP-A's static list)
edit('tests/test_mhupa_master_versions.py', [
    ("""            'src/methods/_common/walk_forward.py', 'src/results_master_v0_2.py'])        # MHUP-A slice 2: v0.2 (design 7)
""",
     """            'src/methods/_common/walk_forward.py',
            'src/methods/_common/weekly_records.py',      # MHUP-B: names the master file in a session's run request, as
            'src/results_master_v0_2.py'])                # the driver does; it opens no master (asserted below)
        weekly = (ROOT / 'src' / 'methods' / '_common' / 'weekly_records.py').read_text(encoding='ascii')
        self.assertEqual(weekly.count('_results_master'), 1)
        for word in ('open(', 'read_bytes', 'read_text', '_trusted_file_bytes', 'load_verified_source', 'csv.'):
            self.assertNotIn(word, weekly.split('def request_for')[1].split('def run_folder')[0])
"""),
])
