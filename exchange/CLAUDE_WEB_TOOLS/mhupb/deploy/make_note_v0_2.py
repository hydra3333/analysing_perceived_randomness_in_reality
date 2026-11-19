"""Build the deployment design note DRAFT v0.2 from DRAFT v0.1 by counted replacements (answer to EX_248).
Usage: python3 -I make_note_v0_2.py V0_1_PATH OUT_PATH CLOCK_TEXT
Each old text must occur exactly once; whole sections are replaced between two headings. Reads and writes only the two
paths given."""
import hashlib, sys
src, out, clock = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '31119cfc2fe79621382045e863846d81eb1c6ea4a29077b12a82919bd3fd3923', 'not the v0.1 bytes sent as EX_247'
s = raw.decode('ascii')


def one(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)


def part(start, end, new):
    global s
    assert s.count(start) == 1 and s.count(end) == 1, (start[:50], end[:50])
    a, b = s.index(start), s.index(end)
    assert a < b
    s = s[:a] + new + s[b:]


def line(start):
    assert s.count(start) == 1, start[:60]
    i = s.index(start)
    return s[i:s.index('\n', i) + 1]


# ---------------------------------------------------------------- header
one('# MHUP-B deployment design note - DRAFT v0.1\n', '# MHUP-B deployment design note - DRAFT v0.2\n')
one(line('**Status:** DRAFT for the reviewer'),
    '**Status:** DRAFT v0.2 for the reviewer\'s R-3 RECHECK. Not ratified. It authorises nothing. It answers EX_248 (RECHECK;\n'
    'findings B01 to B06) and carries the nine choices the owner confirmed on 20 November 2026 (decision log entry 110).\n'
    'Section 18 says where each finding landed. v0.1 (sent as EX_247) is kept beside it; `NOTE_v0_1_TO_v0_2.diff` is exact.\n')
one(line('**Written:**'),
    f'**Written:** {clock} Australia/Adelaide, by the Claude web chat (primary designer and coder), on the project owner\'s\n'
    'go of 19 November 2026, 23:50 (decision log entry 107) and his go for this revision (entry 110). Fable (High).\n')
one('of 19 November 2026, 23:50 (decision log entry 107: the design note only; Fable (High)).\n', '')
one('and the formal OV-1 claim). **Base:** `main` at `dd5788d`;', 'and the formal OV-1 claim). **Base:** `main` at `9350196`;')
one('decision log 100 (how a restore is done), 103 (Python 3.15 only), 104 (no monthly restore test), 105 (no replay comparison), 107 (this go);',
    'decision log 100 (how a restore is done), 103 (Python 3.15 only), 104 (no monthly restore test), 105 (no replay comparison), 107 (the go), 110 (the nine confirmed choices; EX_248 section 1, the owner\'s scientific clarification);')
one('| Evidence state | DESIGNED. Nothing implemented or tested, except one small probe on invented files (section 14) |',
    '| Evidence state | DESIGNED. Nothing implemented or tested, except a probe and a trace on invented files (section 14) |')

# ---------------------------------------------------------------- section 0
part('5. **A snapshot is one ordinary `.zip`**', '## 1. What I read and verified first', '''5. **A snapshot is one ordinary `.zip`** of the whole production folder except its Python environment, written by
   Python's own `zipfile`, checked twice before it counts (the archive read back; the files read again), named with
   the date and time, in `T:\\a_p_r_i_r_backups`. Every production job ends with one. A "snapshot due" file, written
   before a job's first write, makes the next job take a missed one first. If it cannot be made (T: missing), every
   job goes on with a loud warning that stays until one is made: your decision, with its risk stated in section 7.
6. **Restore** works even when production is damaged: it needs only a verified snapshot, a clean process check and
   your go. It renames the old tree aside (kept), unpacks the snapshot into a fresh tree at `G:\\a_p_r_i_r`, rebuilds
   the Python environment from that release's own locked wheels and writes a restore record. After that you work
   normally: the updater, then the weekly session, replay the missing draws one at a time from the draws before each.
   That is the same chronological process and valid research (EX_244; EX_248 section 1). Nothing is compared with the
   old tree, no timestamp proof is asked for, nothing stops.
7. **The formal OV-1 claim is kept apart, with no human choice.** A trace of the passed code (section 9) shows the one
   thing a restore changes: a draw that was counted before the restore can come back as "missed". The fix is one
   objective check in the recorder, fed by a small restore notice: such a draw makes the *registered formal claim*
   read "not established from draw T". Forecasting, scoring, league tables and the descriptive OV-1 view never wait
   for it and are never changed by it.
8. **A marker file** at the production root, checked with its path at every real-data launch, so nothing real starts
   in the E: clone or in a copied or set-aside folder. The proof-of-concept suite still runs where it does today.
9. **A stale orphan marker never blocks a restore for ever and is never copied back as a live block:** restart the PC
   (recommended and checked), a fresh clean process check, and your typed acknowledgement (section 8).

The nine choices you confirmed are recorded in section 15, with five smaller ones still yours.

''')

# ---------------------------------------------------------------- section 1: the trace's facts
one('- **Not verified (carried to the code stage or T017):**',
    '''  9. **The trace of section 9** (the passed slice 3 tree run on the invented weekly project; section 14): after a
     restore the recorder re-derives a lost FACTOR line with all 17 fields equal; it records a formerly counted draw as
     MISSED when its pre-cut-off freeze line is not in the snapshot and its cut-off has passed; its own `verify` then
     passes; and in a tree whose snapshot predates the registration a second `register` is accepted.
  10. The owner's existing orphan-clearance utility (`transitory_data/P1P2_Clear_Archived_Real_Orphan_v0_1.py`) is
     written for one incident: it is pinned to that marker's SHA-256 and that incident's process identities. A new
     marker needs a new reviewed procedure. Section 8 does not change that route; it adds one other.
- **Not verified (carried to the code stage or T017):**''')

# ---------------------------------------------------------------- section 2: layout
one('    G:\\<production>\\                 (the owner names it; a short path, section 15 item 8)',
    '    G:\\a_p_r_i_r\\                    (the owner\'s choice; backups in T:\\a_p_r_i_r_backups\\)')
one('''      PRODUCTION_SETTINGS.json       the owner's settings: the backup folder (T:...), the wheel folder (section 6).''',
    '''      PRODUCTION_SETTINGS.json       the owner's settings: the backup folder, the wheel folder (section 6).''')
one('''                                     SNAPSHOT_LOG.jsonl, INIT_RECORD.json, RESTORE_<date>_<time>.json,''',
    '''                                     LOCK_<digest>.txt (the Python lock of each release deployed; section 6),
                                     SNAPSHOT_LOG.jsonl, INIT_RECORD.json, RESTORE_<date>_<time>.json (and, beside
                                     it, the bytes of any orphan marker a restore set aside as evidence),''')

# ---------------------------------------------------------------- section 4.1 (B01)
one('both; the longest path. Every other mode starts with the same checks and stops on a refusal.',
    '''both; the longest path. `init`, `update` and `export` start with the checks that concern them and stop on a
refusal. **`restore` does not:** it has its own short list (section 8), because it must work when production is the
thing that is broken.''')

# ---------------------------------------------------------------- section 4.4 (B04)
part('- **After a restore** production\'s records legitimately differ', '- The tool never stages, commits or pushes.',
     '''- **Every export is planned before it writes.** The tool first classifies every file on both sides (new, identical,
  grown, changed, and in the clone only), and requires the clone's `source_data/`, `results/` and
  `production_records/` to have no uncommitted change. If anything is refused it prints the whole list and writes
  nothing.
- **After a restore** production's records legitimately differ from the clone's, and the clone holds later records
  that no longer belong to production's state. An ordinary `export` then refuses (changed records). The owner runs
  `export --after-restore`, allowed only when production holds a restore record the clone does not. It makes the
  clone's active folders **exactly** production's tracked records, and nothing is deleted:
  1. every clone file that is changed, or is in the clone only, is first **moved** to
     `superseded_by_restore/<the restore's date and time>/<its same path>` in the clone (bytes checked);
  2. then production's files are copied in.
  So after it, `source_data/` and `results/` in the clone are one coherent state (production's), and everything that
  was there before the restore is in one dated folder, visibly not current, and in Git's history. An interrupted run
  is finished by typing the command again (a file already moved with the same bytes is skipped). **Active** therefore
  has one meaning: what is under `source_data/` and `results/`; a reader of GitHub is never shown a mixture.
- **A worked example (invented names).** Before the restore the clone holds the forecast ledger with freeze lines
  for draws 1 to 5, session files S4 and S5, and OV-1's ledger through draw 5. Production is restored to a snapshot
  taken after draw 3 and replays draws 4 and 5 (new session R4). Ordinary `export`: REFUSED, listing the forecast
  ledger and OV-1's ledger as changed and S4, S5 as in the clone only; nothing written. `export --after-restore`:
  the four old files go to `superseded_by_restore/20261203_101500/results/...`; the clone then holds production's
  ledgers and R4 only. The commit shows four moves and the new files.
''')

# ---------------------------------------------------------------- section 6 (B05: historical lock and wheels)
part('- **The wheel folder** holds the wheel files.', '- **Making the lock and the wheel folder**',
    '''- **Each release has its own lock.** `update` and `init` copy the release's lock file into
  `production_records/LOCK_<digest>.txt`, so **every snapshot carries the exact lock of the release it holds**.
- **The wheel folder** (recommended: `T:\\a_p_r_i_r_backups\\wheels`, a setting) holds the wheel files of every lock
  ever deployed. Nothing prunes it. It is not evidence (every wheel is hash-checked against the lock when installed),
  so it lives outside Git and outside the snapshots.
- **A restore rebuilds the environment from the snapshot's own lock,** not from whatever lock is newest on E:. If a
  wheel that lock names is missing or has another hash, the tool lists exactly which, writes no marker (so nothing
  runs in the fresh tree) and reports RESTORE NOT COMPLETE: ENVIRONMENT NOT BUILT. The owner puts the wheels back (the
  same pinned versions fetched again, on a dependency go; they are hash-checked) and types the command again. An old
  lock also needs the Python version it was made for; the tool says so if the base Python no longer matches.
''')

# ---------------------------------------------------------------- section 7 (B05)
a = s.index('- **How:** Python\'s `zipfile`, Deflate at level 9')
b = s.index('- **Name:** `PRODUCTION_<YYYYMMDD>')
s = s[:a] + '''- **How:** Python's `zipfile`, Deflate at level 9, into `<backup folder>\\<name>.zip.partial`. While each file is read
  its SHA-256 goes into a list stored as the last member (`SNAPSHOT_MANIFEST.json`), with the time the copying began.
- **Verified means two checks, both required.** (1) *The archive:* it is read back and every member's bytes are hashed
  and compared with the list. (2) *The source:* after the archive is complete, every file in production is read and
  hashed **again** and must equal the list, and the set of files must be the same. Production's records are created,
  grow, or are replaced by newer ones; none returns to earlier bytes. So files equal at both readings were the same
  in between: the snapshot is one state, the state at the moment between the two readings. A file that changed, appeared or vanished fails the snapshot. Only
  then is the file renamed to `<name>.zip` (never over an existing name), a line appended to `SNAPSHOT_LOG.jsonl`, and
  `SNAPSHOT_DUE` removed. A `.partial` file is never a snapshot. A lock file stops two snapshots running at once.
''' + s[b:]
part('- **Which jobs end with one:**', '- **Nothing prunes the backup folder.**',
     '''- **Which commands do it by themselves** (flag before the first write, snapshot at the end):

  | Command | Flag and snapshot |
  |---|---|
  | `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` | automatic, in their sequencers |
  | `Run_Results_Updater.bat update` | automatic, in the launcher: flag, the updater, then the snapshot. The updater's own file is not touched. So the first backup after a results update exists even if no weekly session follows |
  | the deploy tool's `init` and `update` | automatic |
  | `Run_Production_Snapshot.bat` | the snapshot, by hand, at any time |
  | single owner commands through the general launchers (`declare-developed`; OV-1's `register` and `stop`; a league `admit` or `repair` typed by hand; a witness line; an old-style walk-forward or report run typed by hand) | **not automatic.** Their run sheets end with `Run_Production_Snapshot.bat`. Until then their change is in no snapshot. This is an exception for the owner's explicit acceptance (section 15, item A) |
  | `restore`; `export`; `check`; any read-only command | none (nothing in production changes, or the tree is the snapshot just read) |

- **`SNAPSHOT_DUE`:** written just before a job's first write (the weekly session: before `open-session`), removed
  only by a verified snapshot. It means "production may have changed since the last verified snapshot". A job that
  finds it tries that snapshot before anything else, whatever kind of job left it and however long ago. A job that was
  refused before it started writes nothing and leaves no flag.
- **If a snapshot cannot be made** (T: unplugged, disk full, a check fails), at the start or at the end of a job:
  **every job goes on** (the owner's decision, entry 110, item 3). The flag stays. Nothing claims a snapshot was made.
  A warning in capitals is printed at the start and again as the last lines of the job, by every job, until a
  verified snapshot exists; the job's exit status says so (a new status "complete, snapshot not made" when everything
  else was complete; otherwise the job's own status, with the warning). The live path comes first.
  **The risk the owner accepts, stated plainly:** while the flag stands, the newest rollback point is the last
  verified snapshot; a restore then replays everything since. That costs time, never research validity. It can cost a
  game's formal OV-1 claim if a counted draw's records exist only in the unsnapshotted stretch (section 9). The
  exposure is largest before `update`, which changes the code with no fresh snapshot of the old state; `update` prints
  that sentence and the date of the last verified snapshot before it goes on.
''')

# ---------------------------------------------------------------- sections 8, 9, 10: rewritten whole
part('## 8. Restore (D10; decision log entry 100; EX_244)', '## 11. Edits to code that is installed or has passed review',
     open(__file__.replace('make_note_v0_2.py', 'note_v0_2_sections_8_9_10.md'), encoding='ascii').read())

# ---------------------------------------------------------------- section 11
one('''| `Run_Experiment.bat`, `Run_Evaluation.bat`, `Run_Method_Rankings.bat`, `Run_Results_Updater.bat`, `Run_Coordinator.bat` (installed); `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` (slice 3) | the marker test |''',
    '''| `Run_Experiment.bat`, `Run_Evaluation.bat`, `Run_Method_Rankings.bat`, `Run_Results_Updater.bat` (installed); `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` (slice 3) | the production guard, inside the Python pre-check each already makes (section 10). `Run_Experiment.bat`: not for the one proof-of-concept probe. `Run_Results_Updater.bat`: also the flag and the snapshot around `update` (section 7). `Run_Coordinator.bat` is not edited |''')
one('''| `src/package_tools/process_check.py` (installed) | the root test no longer requires `.git` |''',
    '''| `src/package_tools/process_check.py` (installed) | the root test no longer requires `.git`; for `restore` only, the listing rule is applied to the production path even when the folder is missing or damaged (the rule itself is unchanged) |
| `src/evaluation/ov1.py` (slice 2; the recorder, not the kernel) | reads the restore notices in its own weekly folder; one new stop cause where it would otherwise write MISSED; `register` refuses after a lost registration (section 9) |
| `src/evaluation/consolidated_report.py` (slice 3) | the formal view's wording when a registration was lost (section 9) |''')
one('''| New | `deploy/Deploy_Production.py` and its launcher; `deploy/RELEASE.json`; the lock file; `src/package_tools/production_snapshot.py`; `Run_Production_Snapshot.bat` |''',
    '''| New | `deploy/Deploy_Production.py` and its launcher; `deploy/RELEASE.json`; the lock file; `src/package_tools/production_snapshot.py`; `src/package_tools/production_guard.py` (the pre-check); `Run_Production_Snapshot.bat` |''')
one('Not edited: the OV-1 kernel and recorder, the forecasting and scoring halves, the league table, the report.',
    'Not edited: the OV-1 kernel (`ov1_numeric.py`), the forecasting and scoring halves, the league table, the updater.')

# ---------------------------------------------------------------- section 12
one('''- **Restore:** onto an invented production tree; the set-aside tree is byte-identical to the tree before; a launcher
  refuses in it; a process listed, or an orphan marker, refuses as decided; the formal OV-1 listing for each of F-A,
  F-B and F-C on invented ledgers; after a restore the weekly sequence on invented data runs to a clean end.''',
    '''- **Restore:** onto an invented production tree; the set-aside tree is byte-identical to the tree before, apart from
  its renamed marker; with the old tree absent, half missing, without a `.venv`, with an unreadable OV-1 ledger: the
  restore completes; a process listed refuses and no acknowledgement overrides it; extraction stopped half-way, then
  the command again; a wheel missing: no marker, RESTORE NOT COMPLETE, then complete after the wheel is put back.
- **The orphan marker at a restore:** in the old tree and in the snapshot; restart shown, clean check and the typed
  sentence: the restore proceeds, the fresh tree has no active marker, the evidence bytes are kept; no restart shown:
  refused; a wrong or missing sentence: refused; a marker written after the last restart: refused.
- **Formal OV-1 after a restore** (the five cases of section 9, on the invented weekly project): (a) and (b)
  unchanged ledgers and equal factors; (c) the new stop at the earliest unverifiable draw, never a MISSED line, with
  forecasting, scoring, the league table and the retrospective view identical to a run without the check; a draw
  whose cut-off is before the snapshot or after the restore still becomes MISSED as today; (d) the report's wording
  and `register` refusing; (e) the same as (c) with the old tree deleted. One planted defect per rule.
- **Labels after a restore** (EX_248 section 3): an original release record brought back by `update`; a replayed
  forecast for a draw after that release date is CATCH-UP, never PROSPECTIVE; revisions are not pooled.
- **The production guard:** the clone (no marker), a renamed-aside tree and a hand-copied marked folder each refuse
  every real-data launcher; the proof-of-concept probe still starts in the clone.''')
one('''- **`export`:** new, grown and identical files; a changed create-only record refuses and writes nothing; the two
  exempt kinds; `--after-restore` refused without a new restore record; production's bytes never change.''',
    '''- **`export`:** new, grown and identical files; a changed create-only record refuses and writes nothing at all (the
  plan is complete before the first write); the two exempt kinds; an uncommitted change in the clone refuses;
  `--after-restore` refused without a new restore record; the worked example of section 4.4 end to end: afterwards
  the clone's active folders equal production's tracked records file for file, every earlier file is under the dated
  folder with its bytes, and an interruption at each step followed by the command again gives the same result;
  production's bytes never change.''')
one('''  the archive, a file changed during the snapshot, a full or missing backup folder each leave no snapshot and leave
  the flag; an existing name is never overwritten; the overdue snapshot is taken first.''',
    '''  the archive, a file changed, added or removed during the snapshot (a same-size rewrite included), a full or
  missing backup folder each leave no snapshot and leave the flag; an existing name is never overwritten; the overdue
  snapshot is tried first; when it cannot be made the job still runs, warns at its start and end, and exits with the
  stated status; the updater's launcher takes one after `update` and none after a read-only command.''')

# ---------------------------------------------------------------- section 13
one('`update` with a fault planted and the command typed again; an overdue snapshot taken first; one `restore`, then a\ncatch-up over the lost draws;',
    '`update` with a fault planted and the command typed again; an overdue snapshot taken first, and a job that goes\non with the warning when the backup folder is missing; one `restore`, with a stale orphan marker and a restart of the\nPC by the owner, then a catch-up over the lost draws and the formal view\'s "not established" line;')

# ---------------------------------------------------------------- section 14
one('## 14. The probe (invented files; cloud, Linux; an indication only)\n', '## 14. The probe and the trace (invented files; cloud, Linux)\n')
one('File Explorer.\n\n## 15.', '''File Explorer.

**The trace** (`restore_ov1_trace.py`, output in `restore_ov1_trace_output.txt`): the passed slice 3 tree, built from
the repository copy (tree digest `ef2b67e0...1f50e9d13`), on the invented weekly project of the slice's own tests,
Python 3.15.0b4. A "restore" there is: the invented project folder renamed aside and an earlier copy put in its
place, with the clock left at the real later time. Section 9 quotes its five cases. It is a trace of existing code on
invented data: not a test, not a result, and it changes no file of the slices.

## 15.''')

# ---------------------------------------------------------------- section 15: rewritten whole
part('## 15. Choices for the owner (each: the question, the options, my recommendation and why)',
     '## 16. Documents to amend with the integrated package',
     open(__file__.replace('make_note_v0_2.py', 'note_v0_2_section_15.md'), encoding='ascii').read())

# ---------------------------------------------------------------- section 16
one('''- **Architecture** (the launch interfaces: the marker test, the new launcher);''',
    '''- **Supplement v0.8 section 6.8** (and code plan v0.3 L5): the restore notice; one more stop cause; `register` after a
  lost registration (section 9). **The orphan-marker rule** (Architecture 5C, a protected block, amended by
  ratification and not edited; H-1 5.4): the one added exception of section 8.
- **Architecture** (the launch interfaces: the production guard in the pre-check, the new launcher);''')

# ---------------------------------------------------------------- section 17
one('- The multi-zip fallback, unless File Explorer needs it.',
    '''- The multi-zip fallback, unless File Explorer needs it.
- **A restore by hand in File Explorer** is possible because a snapshot is an ordinary zip, but it writes no restore
  record and no restore notice, so the formal check of section 9 would not see it. It is therefore not a supported
  procedure: if the tool cannot be used, the steps are written and reviewed for that case.
- **Section 9's check is conservative in one way:** a draw that was genuinely missed, whose cut-off lies between the
  snapshot and the restore, also reads "not established", because the restored tree cannot tell the two apart.''')
one('''- Rule F-B (iii) depends on a human reading of "has the cut-off passed" from the printed list. The cut-off is a fixed
  instant (01:30 UTC on the draw date); the run sheet will give it for the draw in question.
''', '')
one('- Size: about a small slice (one tool, one module, counted edits to twelve files, their tests).',
    '- Size: about a small slice (one tool, two small modules, counted edits to thirteen files, their tests).')

# ---------------------------------------------------------------- section 18
one('*End of the draft.*\n', open(__file__.replace('make_note_v0_2.py', 'note_v0_2_section_18.md'), encoding='ascii').read() + '\n*End of the draft.*\n')

# ---------------------------------------------------------------- wording brought into line with section 10
one('marker guard keeps real-data jobs from running there;', 'production guard (section 10) keeps real-data jobs from running there;')
one('| 9. The marker guard; every mode re-runnable | Sections 10 and 4 |', '| 9. The production guard; every mode re-runnable | Sections 10 and 4 |')
one('Smaller: with the marker guard every launcher refuses outside production,', 'Smaller: with the production guard every real-data launcher refuses outside production,')
one("6.1 (the launchers' marker test; the snapshot at a session's end)", "6.1 (the launchers' production guard; the snapshot at a session's end)")

s.encode('ascii')
assert '\r' not in s and 'F-A' not in s and 'F-B' not in s and 'F-C' not in s
open(out, 'w', encoding='ascii', newline='\n').write(s)
print(len(s.splitlines()), 'lines', hashlib.sha256(s.encode()).hexdigest())
