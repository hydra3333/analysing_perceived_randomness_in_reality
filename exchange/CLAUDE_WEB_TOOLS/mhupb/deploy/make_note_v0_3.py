"""Build the deployment design note DRAFT v0.3 from DRAFT v0.2 by counted replacements (answer to EX_250).
Usage: python3 -I make_note_v0_3.py V0_2_PATH OUT_PATH CLOCK_TEXT BASE_COMMIT
Each old text must occur exactly once; whole sections are replaced between two headings."""
import hashlib, os, sys
src, out, clock, base = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'a60ebdf379af4ebf18d7e5cd179c763eb3e941665f41609312f83032830b4ebd', 'not the v0.2 bytes sent as EX_249'
s = raw.decode('ascii')
def frag(name): return open(os.path.join(HERE, name), encoding='ascii').read()
def one(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)
def part(start, end, new):
    global s
    assert s.count(start) == 1 and s.count(end) == 1, (s.count(start), start[:50], s.count(end), end[:50])
    a, b = s.index(start), s.index(end); assert a < b
    s = s[:a] + new + s[b:]

# ---- header
one('# MHUP-B deployment design note - DRAFT v0.2\n', '# MHUP-B deployment design note - DRAFT v0.3\n')
part('**Status:** DRAFT v0.2', '**Reviewer:** the ChatGPT reviewer chat.',
     '**Status:** DRAFT v0.3 for the reviewer\'s focused R-3 recheck. Not ratified. It authorises nothing. It answers EX_250\n'
     '(a narrow RECHECK: R3-C01, R3-C02) and carries the owner\'s decisions of 20 November 2026 on full backups, the\n'
     'recovery kit and the environment (decision log entries 112 and 113). Section 18 says where each finding landed.\n'
     'v0.1 (EX_247) and v0.2 (EX_249) are kept beside it; `NOTE_v0_2_TO_v0_3.diff` is exact.\n'
     f'**Written:** {clock} Australia/Adelaide, by the Claude web chat (primary designer and coder), under the project\n'
     'owner\'s go of 19 November 2026 for the design note (decision log entry 107; entries 110 and 113). Fable (High).\n')
one('**Base:** `main` at `9350196`;', f'**Base:** `main` at `{base}`;')
one('110 (the nine confirmed choices; EX_248 section 1, the owner\'s scientific clarification);',
    '110 (the nine confirmed choices; EX_248 section 1, the owner\'s scientific clarification), 112 and 113 (EX_250: full snapshots with `.venv`, a plain restore, before-and-after deployment snapshots, the recovery kit, A to G, H1, no Python at a restore);')

# ---- section 0
one('2. **One tool, kept in the development clone, never copied to production.**',
    '2. **One tool, kept in the development clone and in each recovery kit, never copied into production.**')
part('5. **A snapshot is one ordinary `.zip`**', '## 1. What I read and verified first', frag('note_v0_3_section_0_tail.md'))

# ---- section 2
part('## 2. The production folder', '## 3. The release, and how production is proved equal to it', frag('note_v0_3_section_2.md'))

# ---- section 3
one('`Run_*.bat` (today 487 and 5).',
    '`Run_*.bat`, and the owner\'s four environment scripts (`create_venv.bat`,\n  `install_upgrade_dependencies_into_venv.bat`, `activate_venv.bat`, `deactivate_venv.bat`), as they are (today 487, 5\n  and 4).')
one('the expected digest of the release hash list; the name and\n  digest of the Python lock file (section 6).', 'the expected digest of the release hash list.')

# ---- section 4
one('It\nstarts three kinds of child process: `git` (on the E: side only), `pip` (section 6) and the project\'s own reviewed\ntools. It is reviewed code, installed into `main` by the package, and is not part of the release set.',
    'It\nstarts two kinds of child process: `git` (on the E: side only, and never in `restore`) and the project\'s own reviewed\ntools. It is reviewed code, installed into `main` by the package, and is not part of the release set; a copy travels\nin every recovery kit (section 4.7).')
one('**The process check** is always the reviewed `process_check.py`, verified by hash before it is run: with production\'s\nPython when production\'s environment exists and is verified, otherwise with the development environment\'s.',
    '**The process check** of `init` and `update` is the reviewed `process_check.py`, verified by hash before it is run, with\nproduction\'s Python (for `init`, before production\'s environment exists, the development environment\'s). `restore`\nuses its own stricter check, which needs neither (section 8).')
one('the environment against the lock;', 'the environment against `ENVIRONMENT_VERIFIED.json`;')
one('2. Create the folder. Copy', '2. Write and verify the recovery kit on T: (section 4.7); stop if it cannot be written. Create the folder. Copy')
one('(MHUP-B\'s has an empty entry list:\n   no roster change).', '(MHUP-B\'s has an empty entry list:\n   no roster change). At the environment step `init` stops and asks the owner to build `.venv` with his two scripts;\n   the same command typed again goes on (section 6).')
one('5. Take the first snapshot.', '5. Take the first snapshot (`INIT_<release>`). There is no earlier G: tree, so there is none before.')
one('| 1 | `check`: production equals its recorded release (no drift);',
    '| 1 | The recovery kit for this release is written and verified on T:, or the update stops there (section 4.7). `check`: production equals its recorded release (no drift);')
one('| 3 | If `SNAPSHOT_DUE` exists: the overdue snapshot first (section 7) | new (D8) |',
    '| 3 | The `PRE_DEPLOY` snapshot of the whole tree, always attempted, while the old release is whole and quiet (section 7). If it cannot be made the update goes on with the warning NO ROLLBACK POINT WAS CREATED FOR THIS UPDATE | new (D8; EX_250 R3-C02) |')
one('| 9 | The environment: built or rebuilt only if the lock changed, then verified (section 6) | new (D6) |',
    '| 9 | The environment: never built by the tool. If it is not the verified one, the environment inventory is run here and, after step 10 passes, `ENVIRONMENT_VERIFIED.json` is written (section 6) | new (D6; H1) |')
one('| 14 | The end-of-job snapshot, verified; `SNAPSHOT_DUE` removed.', '| 14 | The `POST_DEPLOY` snapshot of the whole tree, verified; `SNAPSHOT_DUE` removed.')
one('be completed is abandoned by restoring the last verified snapshot (D10),', 'be completed is abandoned by restoring the `PRE_DEPLOY` snapshot, or the last verified one (D10),')
one('While `update`, `restore`, `init` or a session resume runs its process check:', 'While `update`, `init` or a session resume runs its process check:')
one('## 5. Appendix J\'s safety properties: kept, or consciously replaced', frag('note_v0_3_section_4_7.md') + '## 5. Appendix J\'s safety properties: kept, or consciously replaced')
one('| 7. A reproducible environment | New, section 6 |',
    '| 7. A verified environment | Section 6: built the owner\'s way; verified by the suite with production\'s own Python before any launcher runs; the exact environment is inside every snapshot. v0.2\'s pinned lock is withdrawn (H1) |')

# ---- sections 6, 7, 8
part('## 6. Production\'s Python environment (D6)', '## 7. Snapshots (D7 to D9)', frag('note_v0_3_section_6.md'))
part('## 7. Snapshots (D7 to D9)', '## 8. Restore (D10;', frag('note_v0_3_section_7.md'))
part('## 8. Restore (D10;', '### A stale orphan marker', frag('note_v0_3_section_8_head.md'))
one('not that nothing new was started since.', 'not that nothing new was started since. Here (c) is the restore\'s own check: no Python program at all. The start\n  time is read from Windows with the standard library.')

# ---- section 10
one('- **Which launchers:**',
    '- **Two more things the same pre-check refuses on:** `SNAPSHOT_IN_PROGRESS.lock` present (a snapshot is being taken;\n  section 7); `.venv\\ENVIRONMENT_VERIFIED.json` missing, or its list not the installed distributions (section 6).\n'
    '- **The two tools that run without a launcher** (`process_check.py`, `install_records.py`) change real files (locks,\n  the two records). They apply the same marker-and-path test to the folder they are given, so they too refuse\n  outside production (EX_250 section 4, B06); the tests\' invented folders carry an invented marker.\n'
    '- **Which launchers:**')

# ---- section 11
one('| `src/package_tools/process_check.py` (installed) | the root test no longer requires `.git`; for `restore` only, the listing rule is applied to the production path even when the folder is missing or damaged (the rule itself is unchanged) |',
    '| `src/package_tools/process_check.py` (installed) | the root test no longer requires `.git` and requires the production marker (section 10); one new read-only command, the quiet check of section 7 (design 6.1\'s rule without the shared-interpreter clause). `restore` does not use this tool |')
one('| `src/package_tools/install_records.py` (installed) | the root test likewise;', '| `src/package_tools/install_records.py` (installed) | the root test likewise (no `.git`; the production marker);')
one('`deploy/RELEASE.json`; the lock file;', '`deploy/RELEASE.json`; the kit\'s `Restore_Production.bat` and `HOW_TO_RESTORE.txt`;')

# ---- section 12
one('- **Restore:** onto an invented production tree; the set-aside tree is byte-identical to the tree before, apart from\n  its renamed marker; with the old tree absent, half missing, without a `.venv`, with an unreadable OV-1 ledger: the\n  restore completes; a process listed refuses and no acknowledgement overrides it; extraction stopped half-way, then\n  the command again; a wheel missing: no marker, RESTORE NOT COMPLETE, then complete after the wheel is put back.',
    '- **The kit:** built from a commit\'s bytes whatever the working files hold; a changed, missing or extra file in an\n  unpacked kit, and a zip that is not its `.sha256`, each refuse; `update` and `init` stop before touching production\n  when the kit cannot be written.\n'
    '- **Restore:** run from an unpacked kit by a bare Python with no third-party package, with no E: clone present, onto\n  an invented production tree with an environment in it; the set-aside tree is byte-identical to the tree before,\n  apart from its renamed marker; the fresh tree equals the snapshot file for file, environment included, with nothing\n  extra; with the old tree absent, half missing, without a `.venv`, with an unreadable OV-1 ledger: the restore\n  completes; any Python process in a stand-in process table refuses, an unreadable table refuses, and no\n  acknowledgement overrides either; a process appearing between the two checks stops it after the rename with\n  nothing unpacked; extraction stopped half-way, then the command again; the health check READY, and NOT READY when\n  the environment cannot start (never "ready"); `--after-hand-unzip` on a tree unzipped by hand.\n'
    '- **The environment:** a rebuilt `.venv` and an upgrade in place each make every real-data launcher refuse until\n  `update` has verified it; a failing suite writes no `ENVIRONMENT_VERIFIED.json`.')
one('  the archive, a file changed, added or removed during the snapshot (a same-size rewrite included), a full or',
    '  the archive, a file changed, added or removed during the snapshot (a same-size rewrite included), a project\n  process listed before or after (not quiet), a launch attempted during the snapshot (refused), a link to another\n  place in the tree, a full or')
one('- **`update`:** every refusal', '- **`update`:** a `PRE_DEPLOY` and a `POST_DEPLOY` snapshot, each full and each naming the release and its kit; the\n  PRE one failing: the update goes on and prints that no rollback point was created; every refusal')

# ---- section 13
one('one snapshot\nopened in **File Explorer by the owner**', 'one snapshot\nof a tree of the real size, environment included, opened in **File Explorer by the owner**')
one('then a catch-up over the lost draws and the formal view\'s "not established" line;',
    'run from an unpacked recovery kit with the task clone out of reach, the restored environment running at the same\npath with nothing installed, then a catch-up over the lost draws and the formal view\'s "not established" line; an\nenvironment rebuilt with the owner\'s two scripts, refused by a launcher until `update` verifies it; the restore\'s\nprocess table and start time read on Windows;')

one('clone into a scratch production folder (with the offline environment build);', 'clone into a scratch production folder (its environment built by the owner with his two scripts: the runner never\nruns `pip`);')
# ---- section 15
part('## 15. The owner\'s choices', '## 16. Documents to amend with the integrated package', frag('note_v0_3_section_15.md'))

# ---- section 16
one('- **Supplement v0.8 section 6.8**', '- **Design 6.1** (the process rule): the quiet check of section 7 and the restore\'s own rule of section 8, each named\n  beside the existing rule, which is not changed.\n- **Supplement v0.8 section 6.8**')
one('- **Direction document v0.3r1 section 9:** the backup paragraph replaced by D7 to D10 and the restore method;',
    '- **Direction document v0.3r1 section 9:** the backup paragraph replaced by D7 to D10, full snapshots, the recovery kit\n  and the restore method;')

# ---- section 17
one('- The dependency procedure (lock and wheel folder): its own reviewed step.', '- The run sheet for an environment change (section 6): written and reviewed with the package.')
part('- **A restore by hand in File Explorer** is possible', '- **Section 9\'s check is conservative in one way:**',
     '- **Not shown anywhere yet (T017):** reading Windows\' process table and start time with the standard library; an\n  environment restored from a zip running at the same path; File Explorer on an archive of the real size; the time a\n  full snapshot takes with the environment inside.\n'
     '- **The quiet check narrows an always-review rule** for snapshots only (it drops the shared-interpreter clause). I\n  believe every launcher-run program is still listed; the reviewer should judge that, and the alternative is to keep\n  the full rule and accept that an unrelated Python job on the PC stops routine snapshots.\n')

# ---- section 18
one('## 18. Where each finding of EX_248 landed', '## 18. Where each finding of EX_248 and EX_250 landed')
one('| Section 3, labels | A replayed forecast for a draw after an original release date | CATCH-UP, never PROSPECTIVE; revisions never pooled; a fixture | 4.3, 12 |\n',
    '| Section 3, labels | A replayed forecast for a draw after an original release date | CATCH-UP, never PROSPECTIVE; revisions never pooled; a fixture | 4.3, 12 |\n' + frag('note_v0_3_section_18_add.md'))
one('Not changed from v0.1: sections 3 (the release and its proof), 4.2, 4.3 and 5 (init, update, Appendix J\'s properties),\nwhich EX_248 supported.',
    'Unchanged in substance since v0.2, and accepted in principle in EX_250: sections 4.4 (export), 9 (formal OV-1) and the\norphan-marker rule of section 8. B05\'s wheel-and-lock part is superseded by section 6.')

s.encode('ascii'); assert '\r' not in s
for stale in ('wheel folder (section 6)', 'LOCK_<digest>', 'RESTORE NOT COMPLETE', 'from the clone\'s hash-verified'):
    assert stale not in s, stale
open(out, 'w', encoding='ascii', newline='\n').write(s)
print(len(s.splitlines()), 'lines', hashlib.sha256(s.encode()).hexdigest())
