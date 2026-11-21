"""Build the deployment design DRAFT v0.8 from DRAFT v0.7 by counted replacements (the owner's decision of
21 November 2026, 13:18, and his question on the settings files). Usage: python3 -I make_deploy_v0_8.py IN OUT CLOCK"""
import hashlib, re, sys
src, out, clock = sys.argv[1:4]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '073e27f4c310efb617f76068c2e7aa780b3529b44a32426ff7be1c6be9654bfe'
s = raw.decode('ascii')
def one(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
def part(a, b, new):
    global s
    assert s.count(a) == 1 and s.count(b) == 1, (s.count(a), a[:50], s.count(b), b[:50])
    i, j = s.index(a), s.index(b); assert i < j; s = s[:i] + new + s[j:]

one('# Deployment design - DRAFT v0.7 (', '# Deployment design - DRAFT v0.8 (')
one('**Status:** DRAFT v0.7 for independent review.', '**Status:** DRAFT v0.8 for independent review (v0.7 with the owner\'s decision of 21 November 2026, 13:18: sections 0, 1,\n2 to 8, 11, 12, 14 to 16; `DEPLOY_v0_7_TO_v0_8.diff` is exact).')
one('specification DRAFT v0.1 and says how', 'specification DRAFT v0.2 and says how')
s, n = re.subn(r'\*\*Written:\*\* .*? Australia/Adelaide', f'**Written:** {clock} Australia/Adelaide', s, count=1); assert n == 1
one('his decision of 21 November 2026 on QA (decision log entry 124).', 'his decisions of 21 November 2026 on installing (decision log entries 124 and 126).')
one('3. **QA proves, PROD copies the proof.** A QA operation ends by testing QA as a whole and writing a pass that lists\n   every installed file with its hash. A PROD operation compares itself with that pass, file by file, before it\n   touches anything, and no option skips the comparison.',
    '3. **The marker is the whole of readiness.** A variant, or the infrastructure, is installable when its marker in DEV\n   matches its files. QA is an optional test bed with the same commands; nothing links it to PROD. Each install\n   checks itself in the tree it installs into.')
one('## 2. What a QA or PROD tree holds', '''**How the settings files come to exist, and why nothing overwrites them** (the owner's question of 21 November 2026).
- **DEV's file is made once, by the owner:** he copies the tracked `ENVIRONMENT.example.ini` to `ENVIRONMENT.ini` and types
  his paths. Git ignores the real file, so no checkout or pull can replace it. `Check_Tree.bat` prints how the tools
  read it and what each check finds, and changes nothing.
- **A QA or PROD tree's file is written exactly once, by `Init_Tree.bat`,** from DEV's entry for that role. It is opened
  create-only: if a file of that name already exists the write fails and the tool refuses.
- **After that no program writes it.** It is not on the infrastructure manifest, so `Reinstall_Infra.bat` cannot touch
  it; it is not part of any variant; every launcher and tool opens it for reading only. A test searches the code for
  any other write and plants an attempt. The one exception is a restore, which writes the backup's own copy into a
  fresh, empty tree (section 12).
- **To change a setting later** (a new backup drive, say) the owner edits the tree's own file by hand, and DEV's entry
  to match. The checks below run at the next command; if the two disagree it refuses and prints both values.
- Every backup holds its tree's file, so a restore brings the settings back with everything else.

## 2. What a QA or PROD tree holds''')
one('            QA_PASS_<number>.json  QA only (section 3)\n', '')

part('## 3. The candidate, the QA pass and the five checks', '## 9. The guard and the process rules', '''## 3. What can be installed, and what an install checks (the owner's decision of 21 November 2026, 13:18)

**3.1 What can be installed, and only this.**
- *Variants:* the folders of ready variants (specification section 4), without their markers, and the helper files
  their declarations name.
- *Infrastructure:* the files listed in DEV's `deploy\\INFRA_MANIFEST.txt`, one path a line, when
  `deploy\\INFRA_IS_INSTALLABLE.json` matches them. `Make_Installable.bat INFRA` writes that marker: every manifest file
  and every file of the install tool, with SHA-256.
- Nothing else in DEV is ever read for copying. A file under `src\\` in a target that is neither is a refusal.

**3.2 The markers are the whole of readiness (owner).** DRAFT v0.7 had a QA pass record and five comparisons of PROD
with QA before every PROD installation. The owner has withdrawn that: PROD is installed on the DEV markers alone.
There is no pass record, and no tool reads one tree in order to decide about another. QA and PROD are each installed
from DEV, in any order, or QA not at all.

**3.3 What every install checks in its own target,** and stops on:
1. the markers match DEV's files now (so a file edited after marking is named and refused);
2. add-only: no installed variant or helper would change; no unexpected file under `src\\`;
3. after copying, every installed file equals the plan;
4. the whole suite, with the target's Python, on a temporary copy;
5. the regression of what was already installed: a fixed sample after variants, everything after infrastructure.

## 4. Creating a tree: `Init_Tree.bat QA|PROD`

| Step | What happens |
|---|---|
| 1 | Settings checked (section 1). The target root does not exist, or is empty, or holds this same unfinished creation |
| 2 | The plan: the infrastructure manifest's files (its marker must match) and every ready variant with its helpers, all hashed. It is shown; for PROD the owner types the confirmation |
| 3 | The process check (section 9). The folder is created; `ENVIRONMENT.ini` (create-only) and the barrier `records\\INSTALL_IN_PROGRESS.json`, holding the plan, are written |
| 4 | Every planned file is copied from DEV: to a temporary name, hashed, renamed into place |
| 5 | The accepted results are copied (QA: from PROD, or from DEV while no PROD exists; PROD: from DEV), each file hashed on both sides; the list is kept as `INIT_RECORD.json`. No result, score, report or record is copied |
| 6 | **It stops and asks the owner to build `.venv`** with `create_venv.bat` and `install_upgrade_dependencies_into_venv.bat` in the new tree. The same command typed again goes on |
| 7 | The whole tree's software is checked against the plan. The suite is run with the new tree's Python on a temporary copy (the planned software and DEV's tests), which is then removed. On success `ENVIRONMENT_VERIFIED.json` is written |
| 8 | `INSTALLED_FILES.json`; the log line; the recovery kit, written and checked (PROD: a failure here stops); the barrier removed, last |
| 9 | The `INIT` backup. The owner then runs the research job |

## 5. Adding variants: `Install.bat PROD` (or `QA`)

| Step | What happens |
|---|---|
| 1 | Settings and role checked. The plan: ready variants the target lacks (narrowed by `--only`), their folders, and helper files the target lacks. A helper the target holds with other bytes refuses. Shown: to add; left out, each with its reason (not marked; marker does not match its files; already installed; already installed with different bytes). Nothing to add: end, target untouched |
| 2 | **PROD: one typed confirmation** of the batch shown |
| 3 | The process check; no job lock, updater lock, orphan marker or other unfinished install |
| 4 | The recovery kit for the new software state (PROD: a failure stops; QA: a failure warns) |
| 5 | The `PRE_INSTALL` backup, always attempted; if it cannot be made: NO ROLLBACK POINT WAS CREATED, and it goes on |
| 6 | The barrier, holding the plan; the updater's own lock is taken; `SNAPSHOT_DUE` |
| 7 | Each new file: temporary name, hash, rename. No existing file is opened for writing |
| 8 | The whole tree's software against the old list plus the plan; nothing unexpected under `src\\` |
| 9 | The suite with the target's Python on a temporary copy; the sample regression |
| 10 | `INSTALLED_FILES.json`; the log line; the updater's lock released; the barrier removed, last |
| 11 | The `POST_INSTALL` backup. Installation is release: the owner's next `Run_Research.bat` fills the new variants' history |

## 6. Updating infrastructure: `Reinstall_Infra.bat PROD` (or `QA`)

The same eleven steps with these differences.
- **Step 1:** the infrastructure marker must match. The plan is the difference between DEV's manifest files and the
  target's infrastructure: files to add, to overwrite and to remove, each with both hashes; the text differences are
  shown. No path under a family folder or `_shared\\` can be in it. No difference: end.
- **Step 7:** overwritten files are replaced by rename; removals come after all copies.
- **Step 9:** the **full** regression: every forecast and every score of every installed variant is recomputed from the
  permitted views and must equal the canonical files in content. One difference stops the install with the barrier
  in place: it is reported as a scientific change, and the way back is the `PRE_INFRA` backup.
- Backups are named `PRE_INFRA` and `POST_INFRA`.

## 7. Verifying a tree: `Verify_Tree.bat` (run in the tree, after its environment is rebuilt)

Process check; a backup; the suite with the tree's Python on a temporary copy of the installed software and DEV's
tests; the sample regression, whose differences after an environment change are **reported** for the W-23 review and
do not by themselves refuse; `ENVIRONMENT_VERIFIED.json`; a backup. A failed suite writes no marker and removes an
older one. The owner's install script removes the marker before it changes anything.

## 8. When an operation stops half-way

| State found | Meaning | What the same command does | The other way out |
|---|---|---|---|
| The barrier exists and its plan equals the plan now | this operation was interrupted, or a check failed and the cause is now corrected | continues: files already in place with the right hash are skipped; the checks run again | restore the backup taken at step 5 |
| The barrier exists with another plan | a different operation is unfinished, or DEV changed meanwhile | refuses and shows both plans | finish that one, or restore |
| `INSTALLED_FILES.json` and the tree differ, no barrier | something changed a file outside the tools | every launcher and tool refuses, naming the file | restore |

While the barrier exists every launcher in that tree refuses. A file not on `INSTALLED_FILES.json` is never run: a
variant folder that is present but not listed is an unexpected file, which refuses the job.

''')
one('It is built from the tool files that passed in QA (check 5).', 'It is built from DEV\'s install tool files, as the infrastructure marker lists them.')
one('Anything further is a new decision, through QA.', 'Anything further is a new decision by the owner.')
part('## 14. Worked examples (invented names; EX_262 section 4)', '## 15. Tests and the rehearsal', '''## 14. Worked examples (invented names; EX_262 section 4, adjusted to the owner's decision)

1. **Two ready, one unfinished.** DEV holds `E_002\\RECUR_MEAN_ALL_V2` and `E_017\\HAZARD_BINS_C100_V2`, both marked, and
   `E_002\\RECUR_MEDIAN_ALL_V3` with no marker. `Install.bat QA` (the owner chooses to look first) shows "to add: 2
   variants, 1 helper (`_shared\\recurrence_gaps_v2.py`); left out: `RECUR_MEDIAN_ALL_V3` (not marked)". It installs and
   checks. The owner runs QA's research job and reads its league reports.
2. **One changes afterwards.** The owner edits `HAZARD_BINS_C100_V2\\method.py` in DEV. `Install.bat PROD` shows "to add:
   `RECUR_MEAN_ALL_V2`; left out: `HAZARD_BINS_C100_V2` (marker does not match its files)". When he has finished and
   marked it again, the next `Install.bat PROD` adds it. QA still holds the earlier bytes under that name:
   `Check_Tree.bat QA` says so, and `Install.bat QA` leaves it alone ("already installed with different bytes"). QA is
   a test bed: it can be restored to an earlier backup or created again; PROD is not affected either way.
3. **Infrastructure.** `src\\evaluation\\reports.py` is improved and `Make_Installable.bat INFRA` run.
   `Reinstall_Infra.bat PROD` shows one file to overwrite and no variant; one confirmation; `PRE_INFRA`; the file
   replaced; the suite; the full regression finds no difference; `POST_INFRA`. Had the change altered one old
   forecast, the install would have stopped there with no job able to run, and `PRE_INFRA` would be restored. Trying
   it in QA first would have shown the same without touching PROD.
4. **A wrong setting.** DEV's `[QA]` entry is mistyped as `G:\\a_p_r_i_r`. `Install.bat QA` refuses at once: QA's and
   PROD's roots are the same folder. Had only the folder been reused, its own file says `role = PROD`: refused.
5. **Separate backups.** QA's job ends with `D:\\TEST_BED_backups\\QA_20270105_101500_RESEARCH.zip` (with the same-volume
   warning); PROD's with `T:\\a_p_r_i_r_backups\\PROD_20270105_193000_RESEARCH.zip`.
6. **A restore installs nothing.** PROD is restored to a backup made before `RECUR_MEAN_ALL_V2` was installed. The tree
   holds forty variants; the job catches up with forty. `Check_Tree.bat PROD` lists the variant as "ready in DEV, not
   installed", as information. If the owner later runs `Install.bat PROD`, it is a new installation: new files, and
   a new `FORWARD_FROM`.

''')
one('the four states of section 8; each of the five checks\nwith one planted difference, and no command line that avoids them;',
    'the three states of section 8; the two kinds of marker (matching; one file\nedited afterwards; made by hand with a wrong hash); a settings file never written after its creation;')
one('roots set in a scratch settings file; `Init_Tree` for a scratch QA and a scratch PROD; an `Install` through both; a',
    'roots set in a scratch settings file; `Init_Tree` for a scratch QA and a scratch PROD; an `Install` into each; a')
one('every OV-1 restore rule;', 'the QA pass record and the five checks of DRAFT v0.7 (the owner\'s decision of 13:18); every OV-1 restore rule;')
one('that list is part of the pass\'s `test_material`.', 'that list sits beside the infrastructure manifest.')
one('End of the deployment design, DRAFT v0.7.', 'End of the deployment design, DRAFT v0.8.')
s.encode('ascii')
for w in ('QA pass', 'pass', 'five checks', 'check 5', 'QA-tested'):
    print(repr(w), [l[:80] for l in s.split('\n') if w in l])
open(out, 'w', encoding='ascii', newline='\n').write(s); print(len(s.splitlines()), hashlib.sha256(s.encode()).hexdigest())
