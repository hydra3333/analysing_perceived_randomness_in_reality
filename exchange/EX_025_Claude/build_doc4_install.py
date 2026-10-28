"""Build the DOC-4 installation package: H-2 v1r4 (owner-ratified 28 Oct 2026) and its review history.

Claude, 28 Oct 2026. No document is edited: every overlay file is an exact recorded input, an LF copy
of a recorded CRLF EX message, or Claude's owner-decisions record. Usage:
  python3 -I build_doc4_install.py INDIR OUTDIR
INDIR holds the files named in SOURCES (from exchange/EX_022..EX_024 and Claude's record).
"""
import hashlib, shutil, sys
from pathlib import Path

ind, outdir = Path(sys.argv[1]), Path(sys.argv[2])
BASE = '63c19e7515e02acc10af1a9c7a290acc73371b7e'
GUARDED = {
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md': 'a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r3.md': 'ddf4de23b726b2abf55ffcab613f926b62775469076476f939288a278e6422fc',
    'doc/RATIFICATION_REGISTER_v0_9.md': 'e84a7a208d99775bbbbf15af8a177d956c5a8e4819cf5b35537f6b70f5dfc6c8',
    'exchange/README.md': 'b08d9e2b62daf1f435c5c02b8908e447c1bc790b28d1d92c2866f110846b2256',
    'review/DOC3_Install_v1/INSTALL_MANIFEST_SHA256.txt': '60e16fcb4c55843b76dc0ab42bbc4424d0e3094661a27a34f48b8f54f23d9009',
    'src/Powerball_Experiment_Coordinator.py': '6d202f5efd164c8e4a0eba97d435a0ec55787da87fcb2930af51309f573adcff',
    'src/methods/_common/game_draws_reader.py': '9ed28e3db821272cbeb47725a587eaefb3d38a13f20403a549b82cd0cdd973e3',
}
# repo path: (input file, SHA-256 of the input as recorded, convert CRLF->LF?)
SOURCES = {
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md':
        ('ChatGPT_Reviewer_Handover_H2_v1r4.md', '73b90ea348aea5fc337097a14ec4a8669258bc6cba55ce5a2485de26575f3f3a', False),
    'review/ChatGPT_Reviewer_Handover_H2_v1r4_initial_draft.md':
        ('ChatGPT_Reviewer_Handover_H2_v1r4_DRAFT.md', 'f27b7612f74ae89a242cb5618d4c3808e41e4c7196e1d71945d119e3eaac3d91', False),
    'review/ChatGPT_Reviewer_Handover_H2_v1r3_to_v1r4.diff':
        ('ChatGPT_Reviewer_Handover_H2_v1r3_to_v1r4_FINAL.diff', '7ab39c21667bc8067f4d1202ebdab5b9e0480bd26d3d0d98ca74183298de095c', False),
    'review/ChatGPT_Reviewer_Handover_H2_v1r4_fact_corrections.diff':
        ('h2v1r4_H2F_fixes.diff', '8033d0ec84a1505bde045bc24229001a7a303183a8c1e8593c8cdbe2d4a71675', True),
    'review/Claude_Fact_Check_H2_v1r4_v1.md':
        ('EX_023_Claude.md', '9b9a027cd18a2b942e1769a9f2e4614c0be1a38c3500a9b0ca7ebb84f7339e6d', True),
    'review/Independent_ChatGPT_EX_024_H2_v1r4_Final_Candidate.md':
        ('EX_024_ChatGPT.md', 'b1a12829fec51bfbbc8d77bcb588905a4aadf45a3667772155a8d8480d01a481', True),
    'review/Owner_Decisions_H2_v1r4_and_Exchange_v0_4_28Oct2026.md':
        ('Owner_Decisions_H2_v1r4_and_Exchange_v0_4_28Oct2026.md', None, False),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


files = {}
for p, (name, want, to_lf) in SOURCES.items():
    b = (ind / name).read_bytes()
    if want:
        assert sha(b) == want, (name, sha(b))
    if to_lf:
        b = b.replace(b'\r\n', b'\n')
    assert b'\r' not in b, p
    files[p] = b
# the installed handover must equal v1r3 + the final diff (checked separately) and keep the rights region
h2 = files['doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md']
assert h2.index(b'\n## 4') - h2.index(b'\n## 2') == 7676

out = outdir
if out.exists():
    shutil.rmtree(out)
ov = out / 'repo_overlay'
for p, b in files.items():
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(b)
man = '# DOC-4 installation manifest (Git-content SHA-256, LF)\n' + ''.join(f'{sha(b)}  {p}\n' for p, b in sorted(files.items()))
mp = 'review/DOC4_Install_v1/INSTALL_MANIFEST_SHA256.txt'
(ov / mp).parent.mkdir(parents=True, exist_ok=True)
(ov / mp).write_bytes(man.encode('ascii'))
files[mp] = man.encode('ascii')
NEW = {p: sha(b) for p, b in files.items()}

v = open(Path(__file__).with_name('verifier_template.py')).read()
v = (v.replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEW.items())))
      .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in GUARDED.items()))
      .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEW))))
assert '@@' not in v
(out / 'VERIFY_DOC4_INSTALL.py').write_bytes(v.encode('ascii'))
cmd = ('@echo off\r\nsetlocal\r\nrem OPTIONAL owner-run staging of exactly the %d DOC-4 paths. No commit, push or deletion.\r\ngit add -- ^\r\n' % len(NEW)
       + ' ^\r\n'.join('  "%s"' % p.replace('/', '\\') for p in sorted(NEW)) + '\r\n'
       + 'if errorlevel 1 (echo STAGING FAILED & exit /b 1)\r\ngit status --short\r\nendlocal\r\n')
(out / 'STAGE_EXACT_FILES.cmd').write_bytes(cmd.encode('ascii'))
P = r'E:\TEMP\DOC4_Install_v1'
D = '28 October 2026'
instr = f"""# DOC-4 - installation of H-2 v1r4 (owner-ratified {D}) and its review history

Windows CMD, repository root. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\DOC4_*` folders, then extract it there (`tar -xf "E:\\TEMP\\DOC4_Install_v1.zip" -C E:\\TEMP`).

**Step 1 - bring your copy up to date and check it** (`git status --short` must print nothing; the pull must say `Fast-forward` or `Already up to date`):

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_DOC4_INSTALL.py" --repo . --phase pre
```

Expected: `PRE PASS`. If the pull or PRE fails, stop and send Claude the output. Nothing has changed yet.

**Step 2 - copy, check, stage:**

```bat
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_DOC4_INSTALL.py" --repo . --phase post
call "{P}\\STAGE_EXACT_FILES.cmd"
git diff --cached --name-status
```

Expected: `{len(NEW)} File(s) copied` (all new; nothing is replaced or deleted); `POST PASS`; {len(NEW)} lines starting with `A`. If POST prints `STOP`, stop and send Claude the output (nothing is committed; the copied files are only new files).

**Step 3 - commit and check the commit (do not push yet):**

```bat
git commit -m "DOC-4: H-2 v1r4 (owner-ratified {D}) and review history"
python "{P}\\VERIFY_DOC4_INSTALL.py" --repo . --phase committed
```

Expected: `COMMITTED PASS`.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** The verifier then prints the commit identities (HEAD, its parent, the commit's paths, anything not yet pushed, the working-tree status). Send Claude the whole output. Claude confirms from those identities exactly what the latest commit is, and only then gives you the exact recovery commands. Nothing has left your PC at that point.

**Step 4 - push, only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub. No test run is needed: no code changes. Claude pushes nothing to the repository while you install.
"""
(out / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
for p, x in sorted(NEW.items()):
    print(x, p)
