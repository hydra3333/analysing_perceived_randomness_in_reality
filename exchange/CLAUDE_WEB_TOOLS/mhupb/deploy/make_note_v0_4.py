"""Build the deployment design note DRAFT v0.4 from DRAFT v0.3 by counted replacements (EX_252's corrections; EX_253's
removal of the restore-specific OV-1 rules; decision log entry 116).
Usage: python3 -I make_note_v0_4.py V0_3_PATH OUT_PATH CLOCK_TEXT BASE_COMMIT
Each old text must occur exactly once; whole parts are replaced between two anchors; a table row by its first cell."""
import hashlib, os, sys
src, out, clock, base = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'b24bf024ae7c890e475792acba6fa7c05dc208e7d928805e8753083da2d84c38', 'not the v0.3 bytes sent as EX_251'
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
def row(first, new):
    """Replace the one whole line that starts with `first`."""
    global s
    lines = s.split('\n'); hit = [i for i, l in enumerate(lines) if l.startswith(first)]
    assert len(hit) == 1, (len(hit), first[:60])
    lines[hit[0]] = new; s = '\n'.join(lines)

# ---- header
one('# MHUP-B deployment design note - DRAFT v0.3\n', '# MHUP-B deployment design note - DRAFT v0.4\n')
part('**Status:** DRAFT v0.3', '**Reviewer:** the ChatGPT reviewer chat.',
     '**Status:** DRAFT v0.4 for the reviewer\'s recheck. Not ratified. It authorises nothing. It makes the bounded\n'
     'corrections of EX_252 (the narrow RECHECK of v0.3) and, following the owner\'s direction in EX_253, removes every\n'
     'restore-specific OV-1 rule: section 9 is now one short section that rests on the OV-1 simplification amendment sent\n'
     'with it. Section 18 says where each finding landed. v0.1 to v0.3 are kept beside it; `NOTE_v0_3_TO_v0_4.diff` is exact.\n'
     f'**Written:** {clock} Australia/Adelaide, by the Claude web chat (primary designer and coder), under the project\n'
     'owner\'s go of 19 November 2026 for the design note (decision log entry 107) and his decisions of entry 116. Fable (High).\n')
one('it touches gates, installs\nand the formal OV-1 claim). **Base:** `main` at `4a72269`;', f'it touches gates and\ninstalls). **Base:** `main` at `{base}`;')

# ---- section 0
part('8. **The formal OV-1 claim is kept apart, with no human choice.**', '9. **A marker file** at the production root',
     '8. **OV-1 needs nothing special after a restore.** Under the OV-1 simplification amendment sent with this note, a\n'
     '   draw replayed after a restore is counted like any caught-up draw, and the score is the same. The restore notices\n'
     '   and the extra stop of v0.3 are withdrawn (section 9).\n')
one('you\n   can unzip a snapshot by hand; the kit\'s instructions say what to run afterwards.',
    'you\n   can unzip a snapshot by hand into an empty folder at the same path; the kit\'s instructions say how, and what to\n   run afterwards so the files are checked.')

# ---- section 1
part('  8. The staged weekly sequencer already treats a stopped formal OV-1 stream', '  10. The owner\'s existing orphan-clearance utility',
     '  8. (v0.4) Facts 8 and 9 of v0.3 concerned the staged OV-1 recorder\'s stopped state and its behaviour after a\n'
     '     restore. This note no longer rests on them (section 9).\n'
     '  9. The weekly session computes the environment\'s full digest when it opens a session (`open_session` calls the\n'
     '     closure and environment inventory), and `environment_inventory()` exists in `src/methods/_common/closure.py`.\n')

# ---- section 4.3
one('| 9 | The environment: never built by the tool. If it is not the verified one, the environment inventory is run here and, after step 10 passes, `ENVIRONMENT_VERIFIED.json` is written (section 6) | new (D6; H1) |',
    '| 9 | The environment: never built by the tool. Its full inventory digest is computed. If it is not the verified one, any older `ENVIRONMENT_VERIFIED.json` is removed here, and a new one is written only after step 10 passes (section 6). A verification-only `update` on the release already deployed runs steps 1 to 5 and 9 to 14 and copies nothing | new (D6; H1; EX_252 section 3) |')

# ---- section 6
part('## 6. Production\'s Python environment (D6;', '## 7. Snapshots (D7 to D9;', frag('note_v0_4_section_6.md'))

# ---- section 7
one('     routine snapshots; every launcher-run program of production is still listed, because the launchers start them\n     inside the folder and name it. One new read-only command in the process tool. Any process listed, or one that\n     cannot be read: not quiet, no snapshot.',
    '     routine snapshots; every launcher-run program of production is still listed, because the launchers start them\n     inside the folder and name it (a production child whose executable is the shared base interpreter is listed\n     through its launcher ancestor; a test shows it). One new read-only command in the process tool. Any process\n     listed, or one that cannot be read: not quiet, no snapshot. **The original install and safety check of design\n     6.1 and the coordinator\'s orphan rule are not relaxed.**')
one('  3. *No file differs.* The second reading below.',
    '  3. *No file differs.* The second reading below.\n'
    '  **What this is and is not** (EX_252 section 1). It is a sound operating rule for the project\'s own controlled\n'
    '  writers. It is not a guarantee against an arbitrary program that is not Python, or against a change made and\n'
    '  undone between the two readings, and is not described as one.\n'
    '  **While `SNAPSHOT_IN_PROGRESS.lock` exists,** the commands of `process_check.py` and `install_records.py` that\n'
    '  write a lock or a record also refuse, as the guarded launchers do. The snapshot\'s own read-only quiet check stays\n'
    '  allowed, or a snapshot would block itself.\n'
    '  **A file named `SNAPSHOT_MANIFEST.json` at production\'s root** (left there only by an unzip by hand, section 8)\n'
    '  stops a snapshot being made, with the standing warning, until `--after-hand-unzip` has checked the tree and moved it.')
row('  | `Run_Production_Snapshot.bat` | **a snapshot by hand',
    '  | `Run_Production_Snapshot.bat` | **a snapshot can be asked for by hand at any time, by itself** (the owner\'s question of 20 November 2026). It is made, and called verified, only if the quiet checks above pass. With `--mark-due` it only sets the flag |')
one('(`declare-developed`; OV-1\'s `register` and `stop`; a league', '(`declare-developed`; a league')
one(' Between the command and that snapshot its change is in no snapshot; the one that matters most is `register`, which cannot be made again if lost (section 9) |',
    ' Between the command and that snapshot its change is in no snapshot |')
one('  verified snapshot; a restore then replays everything since. That costs time, never research validity. It can cost a\n  game\'s formal OV-1 claim if a counted draw\'s records exist only in the unsnapshotted stretch (section 9).',
    '  verified snapshot; a restore then replays everything since. That costs time, never research validity, and under\n  the OV-1 amendment it does not change the OV-1 score either (section 9).')

# ---- section 8
part('**What it does, in order:**', '### A stale orphan marker', frag('note_v0_4_section_8_steps.md'))
one('a forecast made after its draw is catch-up or development evidence, not prospective.',
    'a forecast made after its draw is catch-up or development evidence, not prospective. (Under the OV-1 amendment a\ncatch-up forecast is counted in the OV-1 score all the same; section 9.)')

# ---- section 9
part('## 9. The formal OV-1 claim after a restore (EX_248 B03)', '## 10. The production guard (D5; EX_248 B06)', frag('note_v0_4_section_9.md'))

# ---- section 10
one('- **Two more things the same pre-check refuses on:** `SNAPSHOT_IN_PROGRESS.lock` present (a snapshot is being taken;\n  section 7); `.venv\\ENVIRONMENT_VERIFIED.json` missing, or its list not the installed distributions (section 6).',
    '- **Two more things the same pre-check refuses on:** `SNAPSHOT_IN_PROGRESS.lock` present (a snapshot is being taken;\n  section 7); `.venv\\ENVIRONMENT_VERIFIED.json` missing, or its list not the installed distributions. That second\n  test is a cheap first gate only; the full environment digest is compared at each job boundary (section 6).')
one('They apply the same marker-and-path test to the folder they are given, so they too refuse\n  outside production (EX_250 section 4, B06); the tests\' invented folders carry an invented marker.',
    'They apply the same marker-and-path test to the folder they are given, so they too refuse\n  outside production (EX_250 section 4, B06); the tests\' invented folders carry an invented marker. Their writing\n  commands also refuse while a snapshot is in progress; their read-only commands do not (section 7; EX_252 section 1).')

# ---- section 11
row('| `src/evaluation/ov1.py` (slice 2; the recorder, not the kernel) |',
    '| `src/evaluation/ov1.py`, `src/evaluation/consolidated_report.py` | **none from this note** (v0.3\'s two edits are withdrawn; the OV-1 amendment lists its own changes) |')
row('| `src/evaluation/consolidated_report.py` (slice 3) |',
    '| `install_upgrade_dependencies_into_venv.bat` (the owner\'s script; installed) | one line, in its installing modes only: remove `.venv\\ENVIRONMENT_VERIFIED.json` before anything changes (the owner\'s yes, entry 116 item 5) |')
one('`SNAPSHOT_DUE` written before the first writing child. The sequence itself is untouched |',
    '`SNAPSHOT_DUE` written before the first writing child; the environment\'s full digest compared with the verified marker before anything is written (section 6). The sequence itself is untouched |')
one('one new read-only command, the quiet check of section 7 (design 6.1\'s rule without the shared-interpreter clause). `restore` does not use this tool |',
    'one new read-only command, the quiet check of section 7 (design 6.1\'s rule without the shared-interpreter clause); its writing commands refuse while a snapshot is in progress. `restore` does not use this tool |')
one('(no `.git`; the production marker);', '(no `.git`; the production marker; its writing commands refuse while a snapshot is in progress);')

# ---- section 12
part('- **Formal OV-1 after a restore** (the five cases of section 9', '- **Labels after a restore** (EX_248 section 3)',
     '- **OV-1 after a restore:** nothing in this layer. The OV-1 amendment\'s own tests show a replay giving the same lines.\n'
     '- **EX_252\'s named tests:** a writing command of each of the two unlaunched tools refuses during a snapshot, and the\n'
     '  read-only quiet check runs during it; a production child whose executable is the shared base interpreter is listed\n'
     '  through its launcher ancestor; the restore\'s exact-set check **passes** on a correct restore and refuses one\n'
     '  file missing, one extra and one changed; a same-version reinstall and a same-version changed file are refused at\n'
     '  the job boundary though the launch gate passes; a failed suite leaves no marker and removes an older one; a\n'
     '  verification-only `update`; `--after-hand-unzip` run late (its record says "reconciliation recorded at"); a\n'
     '  snapshot holding an orphan marker unzipped by hand: every launch refuses.\n')
one('with the old tree absent, half missing, without a `.venv`, with an unreadable OV-1 ledger: the restore',
    'with the old tree absent, half missing, without a `.venv`, with unreadable records: the restore')

# ---- section 13
one('then a catch-up over the lost draws and the formal view\'s "not established" line;', 'then a catch-up over the lost draws;')

# ---- section 14
one('Section 9 quotes its five cases.', 'v0.3\'s section 9 quoted its five cases; under the OV-1 amendment it is kept only as the record of what the\nold rule did.')

# ---- section 15
row('| C | Formal OV-1:', '| C | OV-1 after a restore: nothing special, under the OV-1 simplification amendment (entry 116; replaces the earlier C) | 9 |')
row('| - | A snapshot by hand at any time;',
    '| - | A snapshot can be asked for by hand at any time (verified only when the quiet checks pass); and, as the last resort, an unzip by hand | 7, 8 |\n'
    '| - | W-23 is kept for every dependency upgrade: the reviewer\'s look and the owner\'s go before real production use (entry 116 item 4) | 6 |\n'
    '| - | One line added to `install_upgrade_dependencies_into_venv.bat` (entry 116 item 5) | 6, 11 |')
part('**Two small things I added that you have not been asked about; say if either is unwelcome.**', '**Still needing your word, later:**',
     '**Two small things I added in v0.3.** (1) The file `.venv\\ENVIRONMENT_VERIFIED.json`: the reviewer judged it worth\n'
     'keeping (EX_252 section 3), with the full digest checked at each job. (2) `Restore_Production.bat\n'
     '--after-hand-unzip`: kept, now only to check a tree unzipped by hand and to let snapshots resume (section 8).\n\n')

# ---- section 16
one('- **Supplement v0.8 section 6.8** (and code plan v0.3 L5): the restore notice; one more stop cause; `register` after a\n  lost registration (section 9). **The orphan-marker rule**',
    '- **Supplement v0.8 section 6:** nothing from this note; the OV-1 simplification amendment is its own document.\n  **The orphan-marker rule**')

# ---- section 17
one('- The run sheets for the first deployment, `declare-developed` and the registrations.', '- The run sheets for the first deployment and `declare-developed`.')
part('- **Section 9\'s check is conservative in one way:**', '- **A point for the reviewer\'s judgement (labels):**', '')

# ---- section 18
one('## 18. Where each finding of EX_248 and EX_250 landed', '## 18. Where each finding of EX_248, EX_250 and EX_252 landed')
row('| B03 formal OV-1 |', '| B03 formal OV-1 | The staged recorder turns a formerly counted draw into MISSED after a restore, and accepts a second registration | **Superseded** (EX_253): the rule that caused it is replaced by the OV-1 amendment, under which a replayed draw is counted. v0.2\'s and v0.3\'s notices, stop cause and refusal are withdrawn | 9 |')
row('| B05 snapshots |', '| B05 snapshots | Which commands snapshot; a coherent single state; what a restore needs of the environment; the changed choice on an overdue snapshot | A table of commands, the updater\'s launcher included; every snapshot the full tree with `.venv`; quiet by three things; a recovery kit per release; `PRE_DEPLOY` and `POST_DEPLOY`; no "ready" before the environment is shown to start; all jobs go on with a standing warning when a snapshot cannot be made (v0.2\'s lock and wheels are withdrawn) | 4.7, 6, 7, 8 |')
one('| EX_250 section 4, B06 note | Direct commands that change real files | The two tools run without a launcher apply the same marker-and-path test | 10 |\n',
    '| EX_250 section 4, B06 note | Direct commands that change real files | The two tools run without a launcher apply the same marker-and-path test | 10 |\n'
    '| EX_252 section 1, quiet | The unlaunched tools could write during a snapshot; the claim could be read as tamper-proof | Their writing commands refuse during a snapshot, the read-only quiet check does not; the rule is stated as operational, not adversarial; the base-interpreter child is tested | 7, 10, 12 |\n'
    '| EX_252 R3-D01 | The restore\'s "nothing extra" check could not pass: the progress file, the record and the marker were not in the list | The payload is defined; it is verified before anything is added; the additions are named; the marker is last; one sentence states the whole allowed difference; a test shows the check passing | 8, 12 |\n'
    '| EX_252 section 3, the marker | Names and versions miss a same-version reinstall; a failed verification could leave a marker | The full inventory digest at every job boundary; the launch test called a first gate only; the owner\'s script removes the marker first; no marker survives a failed verification; a verification-only `update` | 4.3, 6, 10 |\n'
    '| EX_252 section 4, W-23 | H1 could be read as replacing the always-review rule | It does not: the five steps of section 6, each upgrade, with the evidence H-1 5.4 names; the owner confirmed (entry 116) | 6 |\n'
    '| EX_252 section 5, hand unzip | Ordinary work before reconciliation could change the formal stream; a live orphan marker | The OV-1 part falls away with the amendment; unzip into an empty folder at the same path; "reconciliation recorded at"; a live orphan marker blocks as always; no snapshot until reconciled | 7, 8 |\n'
    '| EX_252 section 6, wording | The B05 row; "a snapshot by hand at any time" | Both corrected | 7, 15, 18 |\n'
    '| EX_253 | The owner\'s direction: no restore-specific OV-1 rules | Section 9 replaced; the amendment sent with this note | 9 |\n')
one('Unchanged in substance since v0.2, and accepted in principle in EX_250: sections 4.4 (export), 9 (formal OV-1) and the\norphan-marker rule of section 8. B05\'s wheel-and-lock part is superseded by section 6.',
    'Unchanged in substance since v0.2, and accepted in principle in EX_250: section 4.4 (export) and the orphan-marker\nrule of section 8. Accepted in EX_252 and unchanged here: the architecture of sections 2 to 5, 4.7 and 7.')

s.encode('ascii'); assert '\r' not in s
for stale in ('RESTORE_NOTICE', 'NOT_ESTABLISHED', 'restore notice', 'the notices', 'registration', 'formal OV-1 claim', 'formal view'):
    hits = [l for l in s.split('\n') if stale in l]
    print(f'{stale!r}: {len(hits)}')
open(out, 'w', encoding='ascii', newline='\n').write(s)
print(len(s.splitlines()), 'lines', hashlib.sha256(s.encode()).hexdigest())
