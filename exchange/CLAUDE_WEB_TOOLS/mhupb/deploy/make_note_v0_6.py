"""Build the deployment design note DRAFT v0.6 from DRAFT v0.5 by counted replacements (EX_258; EX_259 sections 7, 8 G).
Usage: python3 -I make_note_v0_6.py V0_5_PATH OUT_PATH CLOCK_TEXT BASE_COMMIT"""
import hashlib, os, sys
src, out, clock, base = sys.argv[1:5]
HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == 'e8b784c26b1496ac861f8720ae4d0c115bf0e5203cc4adab7e31db40881e2a00', 'not the v0.5 bytes sent as EX_256'
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
    global s
    lines = s.split('\n'); hit = [i for i, l in enumerate(lines) if l.startswith(first)]
    assert len(hit) == 1, (len(hit), first[:60])
    lines[hit[0]] = new; s = '\n'.join(lines)

one('# MHUP-B deployment design note - DRAFT v0.5\n', '# Deployment design note - DRAFT v0.6\n')
part('**Status:** DRAFT v0.5', '**Reviewer:** the ChatGPT reviewer chat.',
     '**Status:** DRAFT v0.6 for the reviewer\'s recheck. Not ratified. It authorises nothing. It removes the error of v0.5\n'
     'that the owner rejected (later releases put back after a restore: EX_258, EX_259 section 7) and points this note at\n'
     'the simplified research system (EX_259). Section 0A says exactly what changed and how to read the rest. The backup\n'
     'scope, the recovery kit, the exact restore, the guard and the environment rules are as the reviewer checked them in\n'
     f'v0.5. v0.1 to v0.5 are kept beside it; `NOTE_v0_5_TO_v0_6.diff` is exact.\n**Written:** {clock} Australia/Adelaide, by the Claude web chat (primary designer and coder), under the project\n'
     'owner\'s go of 21 November 2026 for design work only (decision log entry 122). Fable (High).\n')
one('**Base:** `main` at `96083aa`;', f'**Base:** `main` at `{base}`;')

# section 0
one('the test suite before release, the same install and release records with\n   the same meaning.',
    'the test suite before release, and one deployment-log line per release (installation is release; section 0A).')
one('Then you work normally: the updater, then the weekly session, replay the missing draws one at a time from\n   the draws before each.',
    'Then you work normally: the research job fetches the results and replays the missing draws one at a time from\n   the draws before each, with the snapshot\'s own variants. **No later release is put back automatically.**')
part('8. **OV-1 needs nothing special after a restore.**', '9. **A marker file** at the production root',
     '8. **OV-1 needs nothing special after a restore.** The snapshot\'s ledger comes back and the catch-up continues it.\n'
     '   The score may differ from the one that was lost; that is a truthful result and nothing is marked down for it\n'
     '   (section 9).\n')
one('## 1. What I read and verified first', frag('note_v0_6_section_0A.md') + '## 1. What I read and verified first')

# 4.1, 4.2, 4.3
one('; any release the clone holds that production lacks, with its first-draw numbers and the order of section 9', '')
one('Copy `source_data/`, `results/` and `transitory_data/` whole, the git-ignored run folders\n   included, each file hashed on both sides;',
    'Copy `source_data/` only (the accepted results files, their version ledgers and verification records: the clean\n   baseline of the simplification design, section 9), each file hashed on both sides; nothing of the old `results/` or\n   `transitory_data/` is copied;')
one('the install record, the release record (MHUP-B\'s has an empty entry list:\n   no roster change; it carries each game\'s first draw, the last draw on file plus one, which is the start of the OV-1\n   score: the OV-1 amendment 2.3).',
    'the deployment-log line.')
one('the new release descends from the deployed one', 'no file under `src/methods/E_*/` or `src/methods/_shared/` that the deployed hash list holds is changed or missing in the new one (the add-only rule of the simplification design, 3.2); the new release descends from the deployed one')
one(' for a roster change it also requires the weekly records caught up to the last draw on file, and it writes each game\'s first draw, the last draw on file plus one or a later number given on the command (the OV-1 amendment 2.3);', '')
part('**One rule about the two records.**', '### 4.4 `export`',
     '**After a restore, `update` puts nothing back.** It installs a release only when the owner asks for that release as a\n'
     'new decision. A release that had been installed after the snapshot, and is installed again later, is a new\n'
     'installation with a new deployment-log line; its variants start new lists (section 9). The records of the lost\n'
     'period that the clone holds are set aside by `export --after-restore`, as section 4.4 already says.\n\n')

# section 7
row('  | `Run_Weekly_Session.bat`, `Run_Development_Batch.bat` |', '  | `Run_Research.bat` (the one job; it runs the results updater inside it) | automatic: the flag before its first write, the snapshot at its end |')
row('  | single owner commands through the general launchers', '  | single owner commands that write | none remain in the simplified system (section 0A) |')

# section 8
part('Ordinary work, each step on its usual go:', '**No monthly restore test**',
     'Ordinary work, on the owner\'s usual go: the research job. It fetches the results with the one reviewed updater and\n'
     'catches up one target at a time, each from the draws before it, with exactly the variants the snapshot holds;\n'
     'it saves a league report and an OV-1 line after each, and forecasts the next draw. This is the same chronological\n'
     'process as before and valid research (EX_244; EX_248 section 1; EX_258).\n\n'
     '**Nothing else happens by itself.** No later release is installed; no variant is added, retired or replaced; the\n'
     'environment is not rebuilt or upgraded; nothing is read from the set-aside tree or the clone. The owner looks at why\n'
     'the restore was needed, and decides separately, afterwards, whether to install anything. A new method, its\n'
     'computation or a failed installation may have been the cause; it is not brought back automatically.\n\n'
     'Forecasts that were made after the snapshot are in the set-aside tree only; the replayed ones for the same draws\n'
     'record truthfully that the result was on file when they were computed. Nothing is merged back, compared (entry\n'
     '105) or recovered.\n\n')

# section 9
part('## 9. OV-1 after a restore: no special rule, and a plain statement of what a replay gives', '## 10. The production guard (D5; EX_248 B06)', frag('note_v0_6_section_9.md'))

# section 10, 11
one('`Run_Results_Updater.bat`, `Run_Weekly_Session.bat`, `Run_Development_Batch.bat`, `Run_Production_Snapshot.bat`.',
    '`Run_Results_Updater.bat`, `Run_Research.bat`, `Run_Production_Snapshot.bat` (and, until phase 2 replaces them, the\n  old system\'s launchers in the E: clone, which production never receives).')
row('| `src/sequencer_children.py` (slice 3) |', '| `src/research_job.py`, `Run_Research.bat` (new in phase 2 of the simplification design) | the guard, the overdue snapshot, `SNAPSHOT_DUE` before the first write, the end-of-job snapshot and the full environment digest check are built into the one job; no sequencer |')
row('| `Weekly_Session_Orchestrator.py`, `Development_Batch_Orchestrator.py` (slice 3) |', '| `Weekly_Session_Orchestrator.py`, `Development_Batch_Orchestrator.py`, `sequencer_children.py` (slice 3) | not installed (section 0A) |')

# section 12
part('- **Labels after a restore** (EX_248 section 3):', '- **The production guard:**',
     '- **After a restore** (EX_258; EX_259 section 7): the job continues with exactly the snapshot\'s variants; `check` and\n'
     '  `update` propose and install nothing by themselves; a release installed after the snapshot is absent and stays\n'
     '  absent; installed again later, its variants start new lists; no line is marked for the restore.\n'
     '- **The add-only rule** in `update`: a changed, a removed and an added file under the two folders.\n')

one('- **OV-1 after a restore:** nothing in this layer. The OV-1 amendment\'s own tests show a replay giving the same lines\n  when the cohort is reproduced, and qualified lines when it is not.',
    '- **OV-1 after a restore:** nothing in this layer. The simplification design\'s own tests show the job continuing the\n  snapshot\'s ledger with the snapshot\'s variants.')
one('(v0.3\'s two edits are withdrawn; the OV-1 amendment lists its own changes)', '(v0.3\'s two edits are withdrawn; the simplification design lists its own changes)')
one('under the OV-1 amendment it is kept only as the record of what the\nold rule did.', 'it is kept only as the record of what the\nold rule did.')

# section 15
row('| C | OV-1 after a restore:', '| C | A restore is exactly the snapshot; nothing is put back automatically; OV-1 has no restore rule and no restore penalty (entries 121, 122) | 0A, 8, 9 |')

# section 17
one('- The run sheets for the first deployment and `declare-developed`.', '- The run sheet for the first deployment.')
part('- **Labels after a restore:** `update` brings back', '- **W-23 and "changing the environment at will".**',
     '- **This note still speaks of the old system in places** (section 0A\'s table). I judged an exact, small diff more\n'
     '  useful to the reviewer now than a rewrite; the rewrite belongs with the phase 2 package.\n')

# section 18
one('## 18. Where each finding of EX_248, EX_250, EX_252 and EX_255 landed', '## 18. Where each finding of EX_248, EX_250, EX_252, EX_255, EX_258 and EX_259 landed')
row('| Section 3, labels |', '| Section 3, labels | A replayed forecast after a restore | It records that the result was on file when it was computed; no class, no date (section 0A) | 8 |')
row('| EX_255 E01, as it touches this note |', '| EX_255 E01, as it touched this note | A release put back after a restore | **Withdrawn** with the practice itself (EX_258): nothing is put back | 0A, 4.3 |')
one('| EX_255 section 6, test oracle |', '| EX_258 section 2; EX_259 section 7 | v0.5 put later releases back before the catch-up: "a restore being mangled" | Removed everywhere: the restore is exactly the snapshot; the catch-up uses its variants; any later install is a separate owner decision; no qualification for a restore | 0, 0A, 4.1, 4.3, 8, 9, 12 |\n'
    '| EX_259 sections 2 to 6, as they touch this note | Revisions, release records, weekly sessions and the old results are not part of the new system | `init` copies `source_data/` only; one deployment-log line per release; the add-only rule in `update`; the one job in the snapshot table | 0A, 4.2, 4.3, 7, 11 |\n'
    '| EX_255 section 6, test oracle |')

s.encode('ascii'); assert '\r' not in s
for stale in ('puts back any later release', 'put back each later release', 'keeps the most lines supported', 'first-draw numbers', 'OV-1 amendment 2.3'):
    print(repr(stale), s.count(stale))
open(out, 'w', encoding='ascii', newline='\n').write(s)
print(len(s.splitlines()), 'lines', hashlib.sha256(s.encode()).hexdigest())
