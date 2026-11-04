"""MHUP-A slice 1: counted edits to the existing tests that change (design v0.1r5 Appendix L, and the further ones this
slice found; the handback lists every one). Every old string must occur exactly once. Usage: edit_tests_slice1.py TREE"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()


def edit(rel, pairs):
    p = tree / rel
    s = p.read_bytes().decode('ascii')
    for a, b in pairs:
        assert s.count(a) == 1, (rel, s.count(a), a[:90])
        s = s.replace(a, b)
    p.write_bytes(s.encode('ascii'))
    print('edited', rel, len(pairs))


# ---------------------------------------------------------------- test_code3_retirement.py (Appendix L: line 91; plus
# the r1 baseline is now rebuilt through revision 3's edits, and the r2 archive gets the same check)
edit('tests/test_code3_retirement.py', [
    ("ARCHIVE = ROOT / 'archive' / 'methods' / 'E_001' / 'r1'\n",
     "ARCHIVE = ROOT / 'archive' / 'methods' / 'E_001' / 'r1'\nARCHIVE_R2 = ROOT / 'archive' / 'methods' / 'E_001' / 'r2'\n"),
    ("# The only files that may name the archive's folders: they compare archived bytes, or are the tooling itself.\n",
     "# Revision 3's only code changes (MHUP-1 design v0.1r5 section 2): r2 text -> r3 text, each occurring once.\n"
     "R3_CHANGES = {\n"
     "    'E_001/multigame_e1.py': [(\n"
     "        \"    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):\\n\"\n"
     "        \"        # Revision 2 (owner decision WF1-13): synthetic contract tests and real development runs only.\\n\"\n"
     "        \"        raise ValueError('multi-game E_1 real execution not authorised')\\n\"\n"
     "        \"    if not profile.historical_development_target_allowed(target):\\n\"\n"
     "        \"        raise ValueError('historical target outside development boundary')\\n\",\n"
     "        \"    if data_kind not in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT'):\\n\"\n"
     "        \"        # Revision 3 (MHUP-R, design v0.1r5 section 2; owner decision MHUP-Q10): the method takes the VIEW data kind,\\n\"\n"
     "        \"        # never a run mode. Every real run mode maps to the one real view kind (design 3.3); the target ceiling is\\n\"\n"
     "        \"        # the shared target gate and mode gates of design section 3, not the method's own check.\\n\"\n"
     "        \"        raise ValueError('multi-game E_1: unknown view data kind')\\n\"\n"
     "        \"    if type(target) is not int or target <= profile.first_draw:\\n\"\n"
     "        \"        raise ValueError('target has no history')\\n\")],\n"
     "    'E_001_Historical_Appearance_Frequency.py': [(\n"
     "        \"        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '2')\\n\",\n"
     "        \"        legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '3')\\n\")],\n"
     "}\n"
     "# The only files that may name the archive's folders: they compare archived bytes, or are the tooling itself.\n"),
    ("    '_common.contract_runner', '_common.walk_forward', '_common.occurrence_counts', '_common.polynomial_fits',\n",
     "    '_common.contract_runner', '_common.walk_forward', '_common.master_versions', '_common.owner_records',\n"
     "    '_common.occurrence_counts', '_common.polynomial_fits',\n"),
    ("def r1_bytes_from_live(rel: str) -> bytes:\n"
     "    \"\"\"Revision 1's bytes, rebuilt from the live revision-2 file by reversing the two known edits.\"\"\"\n"
     "    text = (ROOT / 'src' / 'methods' / rel).read_bytes().replace(b'\\r\\n', b'\\n').decode('ascii')\n"
     "    for r1, r2 in R2_CHANGES.get(rel, []):\n",
     "def r2_bytes_from_live(rel: str) -> bytes:\n"
     "    \"\"\"Revision 2's bytes, rebuilt from the live revision-3 file by reversing revision 3's known edits.\"\"\"\n"
     "    text = (ROOT / 'src' / 'methods' / rel).read_bytes().replace(b'\\r\\n', b'\\n').decode('ascii')\n"
     "    for r2, r3 in R3_CHANGES.get(rel, []):\n"
     "        assert text.count(r3) == 1, rel\n"
     "        text = text.replace(r3, r2)\n"
     "    return text.encode('ascii')\n\n\n"
     "def r1_bytes_from_live(rel: str) -> bytes:\n"
     "    \"\"\"Revision 1's bytes, rebuilt from the live revision-3 file by reversing revision 3's and then revision 2's edits.\"\"\"\n"
     "    text = r2_bytes_from_live(rel).decode('ascii')\n"
     "    for r1, r2 in R2_CHANGES.get(rel, []):\n"),
    ("        for rel in R1_FILES:                                  # the live paths hold revision 2 (all reused, ER-3)\n"
     "            self.assertTrue((ROOT / 'src' / 'methods' / rel).is_file(), rel)\n"
     "        changed = [rel for rel in R1_FILES if (ARCHIVE / rel).read_bytes().replace(b'\\r\\n', b'\\n') !=\n"
     "                   (ROOT / 'src' / 'methods' / rel).read_bytes().replace(b'\\r\\n', b'\\n')]\n"
     "        self.assertEqual(changed, sorted(R2_CHANGES))\n",
     "        for rel in R1_FILES:                                  # the live paths hold revision 3 (all reused, ER-3)\n"
     "            self.assertTrue((ROOT / 'src' / 'methods' / rel).is_file(), rel)\n"
     "        changed = [rel for rel in R1_FILES if (ARCHIVE / rel).read_bytes().replace(b'\\r\\n', b'\\n') !=\n"
     "                   r2_bytes_from_live(rel)]\n"
     "        self.assertEqual(changed, sorted(R2_CHANGES))\n\n"
     "    def test_archive_holds_revision_2_complete(self):\n"
     "        \"\"\"MHUP-A: revision 2 archived complete under r2/, its bytes equal to the pre-install live files.\"\"\"\n"
     "        baseline = {rel: r2_bytes_from_live(rel) for rel in R1_FILES}\n"
     "        self.assertEqual(MR.check_archive(ROOT, 'E_1', '2', R1_FILES, baseline, normalise_eol=True), [])\n"
     "        changed = [rel for rel in R1_FILES if (ARCHIVE_R2 / rel).read_bytes().replace(b'\\r\\n', b'\\n') !=\n"
     "                   (ROOT / 'src' / 'methods' / rel).read_bytes().replace(b'\\r\\n', b'\\n')]\n"
     "        self.assertEqual(changed, sorted(R3_CHANGES))\n"
     "        text = (ARCHIVE_R2 / 'README.md').read_bytes().decode('ascii').replace('\\r\\n', '\\n')\n"
     "        self.assertIn('# E_1 revision 2 (archived)', text)\n"
     "        self.assertIn('- **Superseded by:** revision 3.', text)\n"
     "        self.assertIn('MHUP-Q10', text)\n"
     "        for rel in R1_FILES:\n"
     "            self.assertTrue((ARCHIVE_R2 / rel).is_file(), rel)\n"),
    ("        self.assertEqual(sorted(p.name for p in (ROOT / 'archive' / 'methods' / 'E_001').iterdir()), ['r1'])\n",
     "        self.assertEqual(sorted(p.name for p in (ROOT / 'archive' / 'methods' / 'E_001').iterdir()), ['r1', 'r2'])\n"),
    ("    def test_the_archive_is_no_package_and_only_r1_exists(self):\n",
     "    def test_the_archive_is_no_package_and_only_r1_and_r2_exist(self):\n"),
])

# ---------------------------------------------------------------- test_wf1b_static.py (Appendix L: ALLOWED_COMMON)
edit('tests/test_wf1b_static.py', [
    ("                  '_common.walk_forward', '_common.game_profiles', '_common.game_draws_reader'}\n",
     "                  '_common.walk_forward', '_common.game_profiles', '_common.game_draws_reader',\n"
     "                  '_common.master_versions'}       # MHUP-A: the version-2 master rules (design 3.2, Appendix L)\n"),
])

# ---------------------------------------------------------------- test_wf1a_walk_forward.py (not in Appendix L's list;
# the driver's one ledger read moved into master_versions, and E_1 revision 3 takes view kinds)
edit('tests/test_wf1a_walk_forward.py', [
    ("        self.assertEqual(wf.count('_trusted_file_bytes('), 1)            # the ledger line only\n",
     "        self.assertEqual(wf.count('_trusted_file_bytes('), 0)            # MHUP-A: the ledger pin is master_versions'\n"
     "        self.assertEqual(wf.count('MV.current_pin('), 1)                  # one read of the ledger and master bytes\n"),
    ("    def test_e1_revision_2_admits_real_development(self):\n"
     "        \"\"\"E_1 revision 1's function refused real data; revision 2's admits it and still refuses a holdout run.\"\"\"\n"
     "        from E_001.multigame_e1 import forecast\n"
     "        rows = [{'draw': POWERBALL.first_draw, 'MAIN': [1, 2, 3, 4, 5, 6, 7], 'POWERBALL': [1]}]\n"
     "        forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='SYNTHETIC_CONTRACT_TEST')\n"
     "        forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='REAL_DEVELOPMENT')\n"
     "        with self.assertRaises(ValueError):\n"
     "            forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='REAL_HOLDOUT')\n",
     "    def test_e1_revision_3_takes_view_kinds(self):\n"
     "        \"\"\"E_1 revision 3 (MHUP-A) takes the view data kind, never a run mode: the real view kind is admitted, a run\n"
     "        mode name is refused (the adapter maps every real mode to the one real view kind).\"\"\"\n"
     "        from E_001.multigame_e1 import forecast\n"
     "        rows = [{'draw': POWERBALL.first_draw, 'MAIN': [1, 2, 3, 4, 5, 6, 7], 'POWERBALL': [1]}]\n"
     "        forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='SYNTHETIC_CONTRACT_TEST')\n"
     "        forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind='REAL_HISTORICAL_DEVELOPMENT')\n"
     "        for mode in ('REAL_DEVELOPMENT', 'REAL_HOLDOUT'):\n"
     "            with self.assertRaises(ValueError):\n"
     "                forecast(POWERBALL, rows, '0' * 64, POWERBALL.first_draw + 1, data_kind=mode)\n"),
])

# ---------------------------------------------------------------- test_e2r_runner.py (not in Appendix L's list: the
# command line now takes the pinned ledger version)
edit('tests/test_e2r_runner.py', [
    ("                '--master-sha256', sha, '--workspace', str(ws)]\n",
     "                '--master-sha256', sha, '--ledger-version', '1', '--workspace', str(ws)]\n"),
])

# ---------------------------------------------------------------- test_e1r2_revision2.py (Appendix L: lines 223-239 and
# the r2-equals-r1 test; in fact every assertion that revision 2 is the active revision retargets to revision 3)
edit('tests/test_e1r2_revision2.py', [
    ("\"\"\"E_1 revision 2 tests (CODE-3 and E_1 revision 2 design v0.1r2, owner-ratified 31 October 2026). OFFLINE.\n",
     "\"\"\"E_1 revision 2 tests (CODE-3 and E_1 revision 2 design v0.1r2, owner-ratified 31 October 2026). OFFLINE.\n\n"
     "MHUP-A (design v0.1r5 section 2, Appendix L): E_1 revision 3 holds the active SUPPORTED entry, so every check of\n"
     "'the active revision' below reads 3, revision 2 is a superseded chain entry like revision 1, and the identity test\n"
     "compares revision 3 with revision 1's frozen reference (the revision 2 reference is tests/test_e1r3_revision3.py's).\n"
     "T03 checks revision 3's admission by view data kind. T09's install-barrier states are MHUP-A's (E_1's own\n"
     "IN_DEVELOPMENT.txt around the revision 3 entries); barrier P and the gate's binding rules are tested in\n"
     "tests/test_mhupa_gates.py.\n"),
    ("        self.assertEqual([(m['method_id'], m['method_revision']) for m in plan['cohort']], [('E_1', '2')])\n",
     "        self.assertEqual([(m['method_id'], m['method_revision']) for m in plan['cohort']], [('E_1', '3')])\n"),
    ("    def test_r2_equals_r1_label_for_label(self):\n", "    def test_r3_equals_r1_label_for_label(self):\n"),
    ("                e2, d2 = pins(game, '2')\n                e1, d1 = pins(game, '1')\n",
     "                e2, d2 = pins(game, '3')\n                e1, d1 = pins(game, '1')\n"),
    ("                self.assertEqual((r1['method_revision'], r2['method_revision']), ('1', '2'))\n",
     "                self.assertEqual((r1['method_revision'], r2['method_revision']), ('1', '3'))\n"),
    ("        e2, d2 = pins('POWERBALL', '2')\n        for t, rec in self.batch_forecasts('POWERBALL', 1574, 1576).items():\n"
     "            self.assertEqual((rec['run_mode'], rec['method_revision'], rec['training_last_draw_number']),\n"
     "                             ('REAL_DEVELOPMENT', '2', t - 1))\n",
     "        e2, d2 = pins('POWERBALL', '3')\n        for t, rec in self.batch_forecasts('POWERBALL', 1574, 1576).items():\n"
     "            self.assertEqual((rec['run_mode'], rec['method_revision'], rec['training_last_draw_number']),\n"
     "                             ('REAL_DEVELOPMENT', '3', t - 1))\n"),
    ("    def test_admitted_and_refused(self):\n"
     "        from E_001.multigame_e1 import forecast\n"
     "        for p in (POWERBALL, OZLOTTO):\n"
     "            t = p.first_draw + 3\n"
     "            rows = self.rows(p, t)\n"
     "            for kind in ('SYNTHETIC_CONTRACT_TEST', 'REAL_DEVELOPMENT'):\n"
     "                self.assertEqual(forecast(p, rows, '0' * 64, t, data_kind=kind)['data_kind'], kind)\n"
     "            for kind in ('REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC', 'REAL_HISTORICAL_DEVELOPMENT',\n"
     "                         'real_development', '', None):\n"
     "                with self.assertRaises(ValueError, msg=(p.game_id, kind)):\n"
     "                    forecast(p, rows, '0' * 64, t, data_kind=kind)\n"
     "            # The development boundary: the holdout's first draw and beyond are refused, in both games.\n"
     "            for t in (p.holdout_first, p.holdout_first + 1):\n"
     "                with self.assertRaises(ValueError, msg=(p.game_id, t)):\n"
     "                    forecast(p, self.rows(p, t), '0' * 64, t, data_kind='REAL_DEVELOPMENT')\n"
     "            last = p.holdout_first - 1\n"
     "            forecast(p, self.rows(p, last), '0' * 64, last, data_kind='REAL_DEVELOPMENT')\n",
     "    def test_admitted_and_refused(self):\n"
     "        \"\"\"Revision 3 (MHUP-A): the VIEW data kinds are admitted, every run-mode name is refused, and the method has\n"
     "        no target ceiling of its own: any target with a complete prefix is computed (the shared gates decide which\n"
     "        targets a run may name), and an incomplete prefix is refused.\"\"\"\n"
     "        from E_001.multigame_e1 import forecast\n"
     "        for p in (POWERBALL, OZLOTTO):\n"
     "            t = p.first_draw + 3\n"
     "            rows = self.rows(p, t)\n"
     "            for kind in ('SYNTHETIC_CONTRACT_TEST', 'REAL_HISTORICAL_DEVELOPMENT'):\n"
     "                self.assertEqual(forecast(p, rows, '0' * 64, t, data_kind=kind)['data_kind'], kind)\n"
     "            for kind in ('REAL_DEVELOPMENT', 'REAL_HOLDOUT', 'FINAL_NEXT_DRAW', 'IN_SAMPLE_DIAGNOSTIC', 'CATCH_UP',\n"
     "                         'real_historical_development', '', None):\n"
     "                with self.assertRaises(ValueError, msg=(p.game_id, kind)):\n"
     "                    forecast(p, rows, '0' * 64, t, data_kind=kind)\n"
     "            for t in (p.holdout_first - 1, p.holdout_first, p.holdout_first + 1, p.holdout_last + 5):\n"
     "                forecast(p, self.rows(p, t), '0' * 64, t, data_kind='REAL_HISTORICAL_DEVELOPMENT')\n"
     "                with self.assertRaises(ValueError, msg=(p.game_id, t)):              # one row short of the target\n"
     "                    forecast(p, self.rows(p, t)[:-1], '0' * 64, t, data_kind='REAL_HISTORICAL_DEVELOPMENT')\n"
     "            with self.assertRaises(ValueError):\n"
     "                forecast(p, [], '0' * 64, p.first_draw, data_kind='REAL_HISTORICAL_DEVELOPMENT')\n"),
    ("            self.assertEqual([(e['entry_sequence'], e['method_revision'], e['registry_status']) for e in ch],\n"
     "                             [(1, '1', 'SUPPORTED'), (2, '2', 'SUPPORTED')])\n"
     "            self.assertEqual(ch[1]['previous_entry_digest'], record_digest(ch[0]))\n"
     "            d1, d2 = (reg.declaration(e['declaration_digest']) for e in ch)\n"
     "            self.assertEqual(dict(d2, method_revision='1'), d1)\n"
     "            self.assertEqual(d2['method_revision'], '2')\n"
     "            texts = ('method_name', 'one_liner', 'short_explanation', 'text_provenance', 'game_id', 'method_id',\n"
     "                     'variant_id', 'schema')\n"
     "            self.assertEqual({k: ch[1][k] for k in texts}, {k: ch[0][k] for k in texts})\n",
     "            self.assertEqual([(e['entry_sequence'], e['method_revision'], e['registry_status']) for e in ch],\n"
     "                             [(1, '1', 'SUPPORTED'), (2, '2', 'SUPPORTED'), (3, '3', 'SUPPORTED')])\n"
     "            self.assertEqual(ch[1]['previous_entry_digest'], record_digest(ch[0]))\n"
     "            self.assertEqual(ch[2]['previous_entry_digest'], record_digest(ch[1]))\n"
     "            d1, d2, d3 = (reg.declaration(e['declaration_digest']) for e in ch)\n"
     "            self.assertEqual(dict(d2, method_revision='1'), d1)\n"
     "            self.assertEqual(dict(d3, method_revision='2'), d2)\n"
     "            self.assertEqual((d2['method_revision'], d3['method_revision']), ('2', '3'))\n"
     "            texts = ('method_name', 'one_liner', 'short_explanation', 'text_provenance', 'game_id', 'method_id',\n"
     "                     'variant_id', 'schema')\n"
     "            for e in ch[1:]:\n"
     "                self.assertEqual({k: e[k] for k in texts}, {k: ch[0][k] for k in texts})\n"),
    ("    def test_a_request_pinning_revision_1_is_stale(self):\n"
     "        for game in ('POWERBALL', 'OZLOTTO'):\n"
     "            e1, d1 = pins(game, '1')\n"
     "            e2, d2 = pins(game, '2')\n"
     "            with self.assertRaises(CD.DispatchRefused) as cm:\n"
     "                CD.dispatch_gate(C.request(d1, e1, 1300 if game == 'POWERBALL' else 1500, '0' * 64))\n"
     "            self.assertEqual(cm.exception.reason, 'STALE_REGISTRY_ENTRY')\n"
     "            entry, decl = CD.dispatch_gate(C.request(d2, e2, 1300 if game == 'POWERBALL' else 1500, '0' * 64))\n"
     "            self.assertEqual((entry['method_revision'], decl['method_revision']), ('2', '2'))\n",
     "    def test_a_request_pinning_revision_1_or_2_is_stale(self):\n"
     "        for game in ('POWERBALL', 'OZLOTTO'):\n"
     "            for old in ('1', '2'):\n"
     "                e_old, d_old = pins(game, old)\n"
     "                with self.assertRaises(CD.DispatchRefused) as cm:\n"
     "                    CD.dispatch_gate(C.request(d_old, e_old, 1300 if game == 'POWERBALL' else 1500, '0' * 64))\n"
     "                self.assertEqual(cm.exception.reason, 'STALE_REGISTRY_ENTRY')\n"
     "            e3, d3 = pins(game, '3')\n"
     "            entry, decl = CD.dispatch_gate(C.request(d3, e3, 1300 if game == 'POWERBALL' else 1500, '0' * 64))\n"
     "            self.assertEqual((entry['method_revision'], decl['method_revision']), ('3', '3'))\n"),
    ("    def test_gate_names_revision_2(self):\n"
     "        src = (ROOT / 'src' / 'methods' / 'E_001_Historical_Appearance_Frequency.py').read_text()\n"
     "        self.assertEqual(src.count('legacy_gate('), 1)\n"
     "        self.assertEqual(src.count(\"legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '2')\"), 1)\n"
     "        entry, _decl = CD.legacy_gate('POWERBALL', *C.E1, '2')\n"
     "        self.assertEqual((entry['method_revision'], entry['registry_status']), ('2', 'SUPPORTED'))\n"
     "        with self.assertRaises(CD.DispatchRefused) as cm:\n"
     "            CD.legacy_gate('POWERBALL', *C.E1, '1')\n"
     "        self.assertEqual(cm.exception.reason, 'REVISION_MISMATCH')\n",
     "    def test_gate_names_revision_3(self):\n"
     "        src = (ROOT / 'src' / 'methods' / 'E_001_Historical_Appearance_Frequency.py').read_text()\n"
     "        self.assertEqual(src.count('legacy_gate('), 1)\n"
     "        self.assertEqual(src.count(\"legacy_gate('POWERBALL', 'E_1', 'FULL_HISTORY_RAW_COUNTS_V1', '3')\"), 1)\n"
     "        entry, _decl = CD.legacy_gate('POWERBALL', *C.E1, '3')\n"
     "        self.assertEqual((entry['method_revision'], entry['registry_status']), ('3', 'SUPPORTED'))\n"
     "        for old in ('1', '2'):\n"
     "            with self.assertRaises(CD.DispatchRefused) as cm:\n"
     "                CD.legacy_gate('POWERBALL', *C.E1, old)\n"
     "            self.assertEqual(cm.exception.reason, 'REVISION_MISMATCH')\n"),
    ("    def test_withdrawn_revision_2_is_refused(self):\n"
     "        with tempfile.TemporaryDirectory() as td:\n"
     "            data = C.copy_data_root(Path(td))\n"
     "            e2, d2 = pins('POWERBALL', '2')\n"
     "            C.append_entry(data, dict(e2, entry_sequence=3, registry_status='FORMULA_OPEN',\n"
     "                                      registry_status_reason='test harness: withdrawn',\n"
     "                                      previous_entry_digest=record_digest(e2)))\n"
     "            with C.installed(data=data):\n"
     "                with self.assertRaises(CD.DispatchRefused) as cm:\n"
     "                    CD.legacy_gate('POWERBALL', *C.E1, '2')\n",
     "    def test_withdrawn_revision_3_is_refused(self):\n"
     "        with tempfile.TemporaryDirectory() as td:\n"
     "            data = C.copy_data_root(Path(td))\n"
     "            e3, d3 = pins('POWERBALL', '3')\n"
     "            C.append_entry(data, dict(e3, entry_sequence=4, registry_status='FORMULA_OPEN',\n"
     "                                      registry_status_reason='test harness: withdrawn',\n"
     "                                      previous_entry_digest=record_digest(e3)))\n"
     "            with C.installed(data=data):\n"
     "                with self.assertRaises(CD.DispatchRefused) as cm:\n"
     "                    CD.legacy_gate('POWERBALL', *C.E1, '3')\n"),
    ("                         [('E_1', '2')] + [('E_6', '1')] * 3)\n", "                         [('E_1', '3')] + [('E_6', '1')] * 3)\n"),
    # T09: the same six states, one revision later: the barrier is E_1's own flag around the revision 3 entries.
    ("REQUESTS = ('r1 contract', 'r2 contract', 'legacy 1', 'legacy 2')\n",
     "REQUESTS = ('r2 contract', 'r3 contract', 'legacy 2', 'legacy 3')\n"),
    ("# What the walk-forward driver does in each state (O03): which driver code is installed, whether planning refuses.\n"
     "DRIVER = {'pre': ('wf1a', False), 'barrier': ('wf1a', True), 'code': ('e1r2', True), 'release': ('e1r2', True),\n"
     "          'post': ('e1r2', False), 'rebarrier': ('e1r2', True)}\n"
     "WF1A_NOT_REAL_CAPABLE = {'E_1': \"E_1 revision 1's multi-game function accepts synthetic contract data only\"}\n",
     "# What the walk-forward driver does in each state (O03): whether planning refuses (the driver code is the same in all).\n"
     "DRIVER = {'pre': False, 'barrier': True, 'code': True, 'release': True, 'post': False, 'rebarrier': True}\n"),
    ("        if name in ('pre', 'barrier', 'code'):                                    # no r2 entries yet\n"
     "            for g in ('POWERBALL', 'OZLOTTO'):\n"
     "                (data / 'registry' / g / 'E_1' / VARIANT / 'entry_0002.json').unlink()\n"
     "        if name in ('pre', 'barrier'):                                            # no r2 declarations yet\n"
     "            for g in ('POWERBALL', 'OZLOTTO'):\n"
     "                (data / 'declarations' / g / 'E_1' / VARIANT / 'r2.json').unlink()\n",
     "        if name in ('pre', 'barrier', 'code'):                                    # no r3 entries yet\n"
     "            for g in ('POWERBALL', 'OZLOTTO'):\n"
     "                (data / 'registry' / g / 'E_1' / VARIANT / 'entry_0003.json').unlink()\n"
     "        if name in ('pre', 'barrier'):                                            # no r3 declarations yet\n"
     "            for g in ('POWERBALL', 'OZLOTTO'):\n"
     "                (data / 'declarations' / g / 'E_1' / VARIANT / 'r3.json').unlink()\n"),
    ("        e1, d1 = pins('POWERBALL', '1')\n        e2, d2 = pins('POWERBALL', '2')\n"
     "        calls = (lambda: CD.dispatch_gate(C.request(d1, e1, 1300, '0' * 64)),\n"
     "                 lambda: CD.dispatch_gate(C.request(d2, e2, 1300, '0' * 64)),\n"
     "                 lambda: CD.legacy_gate('POWERBALL', *C.E1, '1'),\n"
     "                 lambda: CD.legacy_gate('POWERBALL', *C.E1, '2'))\n",
     "        e1, d1 = pins('POWERBALL', '2')\n        e2, d2 = pins('POWERBALL', '3')\n"
     "        calls = (lambda: CD.dispatch_gate(C.request(d1, e1, 1300, '0' * 64)),\n"
     "                 lambda: CD.dispatch_gate(C.request(d2, e2, 1300, '0' * 64)),\n"
     "                 lambda: CD.legacy_gate('POWERBALL', *C.E1, '2'),\n"
     "                 lambda: CD.legacy_gate('POWERBALL', *C.E1, '3'))\n"),
    ("        with_e1 = WF.make_plan('POWERBALL', 1575, 1575, adapters)     # the installed registry: E_1 revision 2\n"
     "        self.assertEqual(with_e1['cohort'][0]['method_revision'], '2')\n"
     "        without_e1 = None\n"
     "        for name, (driver, refuses) in DRIVER.items():\n"
     "            data, methods = self.state(name)\n"
     "            nrc = WF1A_NOT_REAL_CAPABLE if driver == 'wf1a' else {}\n"
     "            with self.subTest(state=name), C.installed(data=data, methods=methods), \\\n"
     "                    mock.patch.dict(WF.NOT_REAL_CAPABLE, nrc, clear=True):\n"
     "                if not refuses:\n"
     "                    plan = WF.make_plan('POWERBALL', 1576, 1576, adapters)\n"
     "                    ids = [(m['method_id'], m['method_revision']) for m in plan['cohort']]\n"
     "                    if name == 'pre':          # the baseline (O03): ordinary planning works, E_1 not in the cohort\n"
     "                        self.assertNotIn('E_1', [i for i, _r in ids])\n"
     "                        without_e1 = plan\n"
     "                    else:                      # after step 4: E_1 revision 2 joins the cohort\n"
     "                        self.assertEqual(ids[0], ('E_1', '2'))\n",
     "        with_e1 = WF.make_plan('POWERBALL', 1575, 1575, adapters)     # the installed registry: E_1 revision 3\n"
     "        self.assertEqual(with_e1['cohort'][0]['method_revision'], '3')\n"
     "        without_e1 = None\n"
     "        for name, refuses in DRIVER.items():\n"
     "            data, methods = self.state(name)\n"
     "            with self.subTest(state=name), C.installed(data=data, methods=methods):\n"
     "                if not refuses:\n"
     "                    plan = WF.make_plan('POWERBALL', 1576, 1576, adapters)\n"
     "                    ids = [(m['method_id'], m['method_revision']) for m in plan['cohort']]\n"
     "                    if name == 'pre':          # the baseline: ordinary planning works, E_1 revision 2 in the cohort\n"
     "                        self.assertEqual(ids[0], ('E_1', '2'))\n"
     "                        without_e1 = WF.make_plan('POWERBALL', 1576, 1576, {'E_6': adapters['E_6']})\n"
     "                    else:                      # after the release record: E_1 revision 3 joins the cohort\n"
     "                        self.assertEqual(ids[0], ('E_1', '3'))\n"),
])
# ---------------------------------------------------------------- test_e2r_dispatch.py (further to Appendix L: the legacy
# runner's release check and the roster test name the active revision, now 3; the standalone launcher needs --ledger-version)
edit('tests/test_e2r_dispatch.py', [
    ("                '--target', '1300', '--view', 'UNORDERED_SET', '--mode', 'SYNTHETIC_CONTRACT_TEST',\n"
     "                '--declaration-digest', e['declaration_digest'], '--registry-entry-digest', record_digest(ph),\n",
     "                '--target', '1300', '--view', 'UNORDERED_SET', '--mode', 'SYNTHETIC_CONTRACT_TEST', '--ledger-version', '1',\n"
     "                '--declaration-digest', e['declaration_digest'], '--registry-entry-digest', record_digest(ph),\n"),
    ("            CD.legacy_gate('POWERBALL', *C.E1, '2')                                      # still released\n",
     "            CD.legacy_gate('POWERBALL', *C.E1, '3')                                      # still released\n"),
    ("            with self.assertRaises(DispatchRefused) as cm:\n"
     "                CD.legacy_gate('POWERBALL', *C.E1, '2')\n",
     "            with self.assertRaises(DispatchRefused) as cm:\n"
     "                CD.legacy_gate('POWERBALL', *C.E1, '3')\n"),
    ("        self.assertIn(f'DISPATCH REFUSED: POWERBALL E_1 FULL_HISTORY_RAW_COUNTS_V1 revision 2: {expect}: ', err.getvalue())\n",
     "        self.assertIn(f'DISPATCH REFUSED: POWERBALL E_1 FULL_HISTORY_RAW_COUNTS_V1 revision 3: {expect}: ', err.getvalue())\n"),
    ("        entry, decl = CD.legacy_gate('POWERBALL', *C.E1, '2')                         # E_1 revision 2 (WF1-13)\n",
     "        entry, decl = CD.legacy_gate('POWERBALL', *C.E1, '3')                         # E_1 revision 3 (MHUP-A)\n"),
])

# ---------------------------------------------------------------- test_rel1_release.py (further to Appendix L: E_1's chain
# gained revision 3)
edit('tests/test_rel1_release.py', [
    ("            # E_1's chain gained revision 2 (CODE-3 and E_1 revision 2 package); REL-1 itself left it unchanged.\n"
     "            self.assertEqual([(e['entry_sequence'], e['registry_status'], e['method_revision']) for e in e1],\n"
     "                             [(1, 'SUPPORTED', '1'), (2, 'SUPPORTED', '2')])\n",
     "            # E_1's chain gained revision 2 (CODE-3 and E_1 revision 2 package) and revision 3 (MHUP-A); REL-1\n"
     "            # itself left it unchanged.\n"
     "            self.assertEqual([(e['entry_sequence'], e['registry_status'], e['method_revision']) for e in e1],\n"
     "                             [(1, 'SUPPORTED', '1'), (2, 'SUPPORTED', '2'), (3, 'SUPPORTED', '3')])\n"),
])
print('test edits applied')
