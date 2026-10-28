"""Build the E1-ALIGN code installation package (Claude, 28 Oct 2026).

Usage: python3 -I build_e1align_install.py BASE_TREE TRIAL_TREE ALLOWLIST REGISTER EVIDENCE_DIR OUTDIR
BASE_TREE: a checkout of BASE (below); TRIAL_TREE: the same after apply_e1align.py plus tests/test_e1_align.py;
ALLOWLIST: the reviewed frozen allowlist (aaf7f46e...); REGISTER: register v0.10 (doc/RATIFICATION_REGISTER_v0_10.md);
EVIDENCE_DIR: Linux evidence files copied under review/E1ALIGN_Code_Install_v1/.
The overlay holds the 10 edited files (at their new paths), the 3 added files and the documents. The 5 moves
are made by RENAME_FILES.cmd (git mv); the one file moved unchanged arrives that way.
"""
import hashlib, json, shutil, sys
from pathlib import Path

base, trial, allow_p, reg_p, ev, outdir = map(Path, sys.argv[1:7])
BASE = 'b64c2a691735137b01cf82c428cb3cb8da9a7f1f'
ALLOW_SHA = 'aaf7f46e529ff42036cf7f943c4efc6232edbd2c3ff463e9e1be02f10a975164'
PKG = 'E1ALIGN_Code_Install_v1'
GUARDED_PATHS = [
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r3.md', 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md',
    'doc/RATIFICATION_REGISTER_v0_9.md', 'doc/Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md',
    'src/Powerball_Experiment_Coordinator.py', 'src/coordinator_private/multigame_coordinator_exit_receipt.py',
    'src/coordinator_private/multigame_launch_spec.py', 'src/coordinator_private/multigame_windows_lifecycle.py',
]
EVIDENCE = ['e1align_checks_output_linux.txt', 'suite_e1align_linux_py313.txt', 'suite_e1align_linux_py315b4.txt',
            'check_imports_linux_py313.txt', 'e1align_trial_diff.diff']


def sha(b):
    return hashlib.sha256(b).hexdigest()


ab = allow_p.read_bytes()
assert sha(ab) == ALLOW_SHA, 'not the reviewed allowlist'
allow = json.loads(ab)
moves, edited = allow['moves'], allow['edited']
assert len(moves) == 5 and len(edited) == 10 and len(allow['added']) == 3 and len(allow['moved_unchanged']) == 1

files = {}
for e in edited:
    files[e['new_path']] = (trial / e['new_path']).read_bytes()
for p, h in allow['added'].items():
    b = (trial / p).read_bytes()
    assert sha(b) == h, p
    files[p] = b
docs = {'doc/RATIFICATION_REGISTER_v0_10.md': reg_p.read_bytes(), f'review/{PKG}/e1align_allowlist.json': ab}
for n in EVIDENCE:
    docs[f'review/{PKG}/{n}'] = (ev / n).read_bytes()
for p, b in {**files, **docs}.items():
    assert b'\r' not in b, p
files.update(docs)

out = outdir
if out.exists():
    shutil.rmtree(out)
ov = out / 'repo_overlay'
for p, b in files.items():
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(b)
mp = f'review/{PKG}/INSTALL_MANIFEST_SHA256.txt'
man = ('# E1-ALIGN code installation manifest (Git-content SHA-256, LF). Moves (git mv):\n'
       + ''.join(f'#   {o} -> {n}\n' for o, n in moves.items())
       + ''.join(f'{sha(b)}  {p}\n' for p, b in sorted(files.items())))
(ov / mp).write_bytes(man.encode('ascii'))
files[mp] = man.encode('ascii')
docs[mp] = files[mp]
NEW = {p: sha(b) for p, b in files.items()}
guarded = {p: sha((base / p).read_bytes()) for p in GUARDED_PATHS}
for p in GUARDED_PATHS:
    assert (trial / p).read_bytes() == (base / p).read_bytes(), p

data = {'new_sha': dict(sorted(NEW.items())), 'docs': sorted(docs), 'guarded': guarded}
v = open(Path(__file__).with_name('verify_template.py')).read()
v = (v.replace('@@BASE@@', BASE).replace('@@ALLOW_SHA@@', ALLOW_SHA)
      .replace('@@DATA@@', json.dumps(data, indent=1)))
assert '@@' not in v
(out / 'VERIFY_E1ALIGN_INSTALL.py').write_bytes(v.encode('ascii'))
for n in ('RUN_E1ALIGN_SUITE.py', 'CHECK_E1ALIGN_IMPORTS.py'):
    shutil.copy(Path(__file__).with_name(n), out / n)

w = lambda p: p.replace('/', '\\')
ren = ('@echo off\r\nsetlocal\r\nrem E1-ALIGN: the 5 explicit moves (git mv) into the new method folder. Run from the repository\r\n'
       'rem root after PRE PASS. Stops at the first failure. No commit, push or deletion of content.\r\n'
       'if not exist "src\\methods\\E_001" mkdir "src\\methods\\E_001" || goto :fail\r\n'
       + ''.join(f'git mv -- "{w(o)}" "{w(n)}" || goto :fail\r\n' for o, n in moves.items())
       + 'echo MOVES DONE\r\nendlocal\r\nexit /b 0\r\n:fail\r\necho MOVE FAILED: stop and send Claude this output.\r\nendlocal\r\nexit /b 1\r\n')
(out / 'RENAME_FILES.cmd').write_bytes(ren.encode('ascii'))
stage = sorted(NEW)  # the 5 moves are already staged by RENAME_FILES.cmd (git mv)
cmd = ('@echo off\r\nsetlocal\r\nrem Owner-run staging of exactly the %d E1-ALIGN files with new bytes (the 5 moves are already\r\nrem staged by RENAME_FILES.cmd). No commit, push or deletion.\r\ngit add -- ^\r\n' % len(stage)
       + ' ^\r\n'.join('  "%s"' % w(p) for p in stage) + '\r\n'
       + 'if errorlevel 1 (echo STAGING FAILED & exit /b 1)\r\ngit status --short\r\nendlocal\r\n')
(out / 'STAGE_EXACT_FILES.cmd').write_bytes(cmd.encode('ascii'))

n_new = len(set(allow['added']) | set(docs))
P = rf'E:\TEMP\{PKG}'
instr = f"""# E1-ALIGN - code installation (only after the reviewer's RECHECK PASS and the owner's go-ahead)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\E1ALIGN_*` folders, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`).

## 1. Update, check, move, copy, check

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_E1ALIGN_INSTALL.py" --repo . --phase pre
call "{P}\\RENAME_FILES.cmd"
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_E1ALIGN_INSTALL.py" --repo . --phase post
```

Expected: `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `MOVES DONE`; `{len(files)} File(s) copied` (10 replace moved or existing files, as intended; {n_new} are new); `POST PASS`.

## 2. Tests and import checks (offline; nothing is changed)

```bat
.venv\\Scripts\\python.exe "{P}\\RUN_E1ALIGN_SUITE.py" --repo .
.venv\\Scripts\\python.exe "{P}\\CHECK_E1ALIGN_IMPORTS.py" --repo .
```

Expected: `SUITE PASS` (84 tests; the only allowed skips are the two symlink tests, if Windows cannot create symlinks), then `RESULT PASS`. **Send Claude both outputs whatever they say.**

If anything in steps 1 or 2 prints `STOP` or `FAILED`, do not commit. Send Claude the output. Nothing is committed at that point; Claude will then give you the commands that put the repository back as it was.

## 3. Stage, commit, check, and only then push

```bat
call "{P}\\STAGE_EXACT_FILES.cmd"
git diff --cached --name-status
git commit -m "E1-ALIGN: E_1 modules into src/methods/E_001, shared canonical encoding, symbol-aware firewall; register v0.10"
python "{P}\\VERIFY_E1ALIGN_INSTALL.py" --repo . --phase committed
```

Expected: the staged list shows 5 renames (`R`), 6 modifications (`M`) and {n_new} lines starting with `A`; then `COMMITTED PASS`.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** The verifier prints the commit identities; send Claude the whole output, and Claude gives you the exact recovery commands after confirming them.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID. Claude then verifies it from GitHub and runs the immediate recovery check (E1A-T13) in a disposable clone. Claude pushes nothing to the repository while you install.
"""
(out / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(f'{len(files)} overlay files ({len(edited)} edited, {len(allow["added"])} added code, {len(docs)} docs); {len(stage)} staged paths')
for p, x in sorted(NEW.items()):
    print(x, p)
