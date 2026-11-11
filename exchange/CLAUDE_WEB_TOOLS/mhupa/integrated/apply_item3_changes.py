#!/usr/bin/env python3
"""Changes to the reviewed MHUP-A code made after the slice reviews, applied by counted edits to the DEV tree
(build_dev_integrated.sh calls this last). Claude web chat, 11 November 2026. A working tool. Each change is owner-
approved for the DRAFT package and goes to the reviewer with it; none is installed.

  N4  (owner, 11 November 2026): two line-ending-sensitive files never converted by Git, so the two tests that read
      their raw bytes pass in a fresh core.autocrlf=true clone (.gitattributes).
  A   (reviewer's item 3 review, section 5 A): install_records.py release-record refuses before writing the
      permanent, create-only release record unless the install lock U is held by this package and no released
      method still has its IN_DEVELOPMENT flag (barrier E for E_1); one new test with its negatives.
Usage: apply_item3_changes.py DEV
"""
import sys
from pathlib import Path

dev = Path(sys.argv[1])


def edit(rel, pairs):
    p = dev / rel
    s = p.read_bytes().decode('utf-8')
    for old, new in pairs:
        assert s.count(old) == 1, f'{rel}: anchor not found exactly once: {old[:70]!r}'
        s = s.replace(old, new)
    p.write_bytes(s.encode('utf-8'))
    print(f'edited {rel} ({len(pairs)} counted edit(s))')


# ---- N4
ga = dev / '.gitattributes'
s = ga.read_bytes()
anchor = b'src/methods/_common/contract_data/install_records/** -text\n'
assert s.endswith(anchor) and s.count(anchor) == 1, '.gitattributes does not end with the N1 line'
s += (b'# Two files whose raw bytes tests check (a no-CR assertion; a reference SHA-256): never converted (N4)\n'
      b'src/package_tools/process_check.py -text\n'
      b'tests/fixtures/results_master_v0_1_reference.py.txt -text\n'
      b'src/results_master_v0_2.py -text\n')      # N4b: the same test's third assertion; awaits the owner's yes
ga.write_bytes(s)
print('appended the N4 and N4b lines (owner-approved, 11 November 2026) to .gitattributes')

# ---- A: the release-record guard
edit('src/package_tools/install_records.py', [
    ("""BARRIER_REL = Path('src') / 'methods' / '_common' / 'contract_data' / 'INSTALL_IN_PROGRESS.txt'
""", """BARRIER_REL = Path('src') / 'methods' / '_common' / 'contract_data' / 'INSTALL_IN_PROGRESS.txt'
UPDATER_LOCK_REL = Path('source_data') / '.results_master.lock'           # barrier U (Appendix J step 3)
INSTALL_LOCK = re.compile(r'INSTALL (?P<package>[A-Za-z0-9_.-]+) (?P<utc>\\S+)\\Z')   # process_check.py's own content
FLAG_NAME = 'IN_DEVELOPMENT.txt'                                          # barrier E is E_1's flag
"""),
    ("""    install_rel = RECORDS_REL / f'INSTALL_{package}_V1.json'
    if not (root / install_rel).is_file():
        raise Refused('no install record for this package')""",
     """    lock = root / UPDATER_LOCK_REL                  # U must still be held: it is released only at step 18
    held = None
    if lock.is_file() and not lock.is_symlink():
        held = INSTALL_LOCK.fullmatch(lock.read_text(encoding='ascii', errors='replace').strip())
    if held is None or held.group('package') != package:
        raise Refused('the install lock U is not held by this package; the release record is written while the install '
                      'still holds it (Appendix J steps 16 to 18)')
    for e in man['release_entries']:                # E (and any released method's flag) must be gone (step 15)
        flag = Path('src') / 'methods' / f'E_{int(e["method_id"][2:]):03d}' / FLAG_NAME
        if (root / flag).exists() or (root / flag).is_symlink():
            raise Refused(f'{flag.as_posix()} still exists; the release record follows the removal of E and P (step 15)')
    install_rel = RECORDS_REL / f'INSTALL_{package}_V1.json'
    if not (root / install_rel).is_file():
        raise Refused('no install record for this package')"""),
])

edit('tests/test_mhupa_install_records.py', [
    ("""        git(self.root, 'init', '-q')
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'base')""",
     """        git(self.root, 'init', '-q')
        (self.root / '.git' / 'info' / 'exclude').write_text('/source_data/.results_master.lock\\n')   # never committed
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'base')
        self.hold_u('TESTPKG')"""),
    ("""    def tearDown(self):
        self._td.cleanup()""",
     """    def tearDown(self):
        self._td.cleanup()

    def hold_u(self, package):
        \"\"\"The install lock U, as process_check.py take-install-lock writes it.\"\"\"
        lock = self.root / 'source_data' / '.results_master.lock'
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_text(f'INSTALL {package} 2026-11-11T00:00:00.000000Z')"""),
    ("""        rc, out = self.run_tool('release-record', '--root', str(self.root), '--package', 'OTHER', '--manifest', str(other))""",
     """        self.hold_u('OTHER')
        rc, out = self.run_tool('release-record', '--root', str(self.root), '--package', 'OTHER', '--manifest', str(other))"""),
    ("""        rc, out = self.run_tool('release-record', '--root', str(self.root), '--package', 'BAD', '--manifest', str(bad))""",
     """        self.hold_u('BAD')
        rc, out = self.run_tool('release-record', '--root', str(self.root), '--package', 'BAD', '--manifest', str(bad))"""),
    ("""    def test_a_superseding_registry_entry_retires_the_old_revision(self):""",
     """    def test_release_record_needs_u_held_by_this_package_and_no_flag(self):
        # the reviewer's item 3 review, A: checked before the permanent, create-only record is written
        self.install()
        git(self.root, 'add', '-A')
        git(self.root, 'commit', '-q', '-m', 'package')
        args = ('release-record', '--root', str(self.root), '--package', 'TESTPKG', '--manifest', str(self.manifest))
        rel = self.root / IR.RECORDS_REL / 'RELEASE_TESTPKG_V1.json'
        lock = self.root / 'source_data' / '.results_master.lock'
        for content, why in ((None, 'U absent'), ('INSTALL OTHER 2026-11-11T00:00:00.000000Z', 'U names another package'),
                             ('update 2026-11-11', 'U holds an update\\'s content')):
            with self.subTest(why):
                if content is None:
                    lock.unlink()
                else:
                    lock.write_text(content)
                rc, out = self.run_tool(*args)
                self.assertEqual(rc, 1)
                self.assertIn('the install lock U is not held by this package', out)
                self.assertFalse(rel.exists())
        self.hold_u('TESTPKG')
        flag = self.root / 'src' / 'methods' / 'E_001' / 'IN_DEVELOPMENT.txt'
        flag.parent.mkdir(parents=True)
        flag.write_text('barrier E')
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 1)
        self.assertIn('src/methods/E_001/IN_DEVELOPMENT.txt still exists', out)
        self.assertFalse(rel.exists())
        flag.unlink()
        rc, out = self.run_tool(*args)
        self.assertEqual(rc, 0, out)
        self.assertTrue(rel.exists())

    def test_a_superseding_registry_entry_retires_the_old_revision(self):"""),
])
