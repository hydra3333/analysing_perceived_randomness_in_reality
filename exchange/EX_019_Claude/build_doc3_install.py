"""Build the DOC-3 installation package (Claude, 28 Oct 2026).

Finalises register v0.9 mechanically (owner ratification status and date only; DOC3-RD-08), then
assembles the overlay, manifest, read-only verifier, staging script and instructions.
Usage:
  python3 -I build_doc3_install.py REG_V09_CANDIDATE H1_V1R3 EX_016 EX_018 OUTDIR "28 October 2026"
EX_016 and EX_018 are the reviewer's DOC-3 review and recheck as recorded in exchange/ (CRLF);
they are stored under review/ as LF copies with descriptive names.
"""
import difflib, hashlib, shutil, sys
from pathlib import Path

reg_c, h1, ex16, ex18, outdir, D = sys.argv[1:7]
d = D.split()
short = f'{d[0]} {d[1][:3]} {d[2]}'
BASE = 'd8bb8d84338016c8b6803ff3857363282a9e8307'
GUARDED = {
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r2.md': '55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md': 'a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1',
    'doc/RATIFICATION_REGISTER_v0_8.md': '3f217c6875d443a0cc1bba2f6c329b1fda455fb4a97bf7fe06090394736fffcf',
    'exchange/README.md': 'a20589e5c5bdeed043e78815f86b1a71679426f17528aedfb14aef7d72ed10ef',
    'review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt': '9d8664f38c33ee374ace06d29d98a4d84477af9199359e22bfcef84e1897f6a7',
    'src/Powerball_Experiment_Coordinator.py': '6d202f5efd164c8e4a0eba97d435a0ec55787da87fcb2930af51309f573adcff',
    'src/methods/_common/game_draws_reader.py': '9ed28e3db821272cbeb47725a587eaefb3d38a13f20403a549b82cd0cdd973e3',
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rd(p, want):
    b = open(p, 'rb').read()
    assert sha(b) == want, (p, sha(b))
    return b


r = rd(reg_c, 'dfec0fe437d3f5f22d62ada56fdf1c7949aa9990f01e5b62498815fe3e5ac2bc')
h = rd(h1, 'ddf4de23b726b2abf55ffcab613f926b62775469076476f939288a278e6422fc')
e16 = rd(ex16, '3b0871cbb5589f5be4bd158654f2ca603c7e9a1190ac3946cd4f21f7f45a382a')
e18 = rd(ex18, '6b2e13440a2ce1b8901bf6f5ba73b8cfe7362a39dd82e58521b125d458d6d543')
t = r.decode('utf-8')
assert '\r' not in t
for old, new in [
    ('**Register version:** v0.9 RATIFICATION CANDIDATE (drafted 28 October 2026), recording',
     f'**Register version:** v0.9 OWNER-RATIFIED {D}, recording'),
    ('H-1 v1r3 and register v0.9 are candidates pending owner ratification and DOC-3 installation, and are identified by content hash;',
     f'H-1 v1r3 and register v0.9 were OWNER-RATIFIED {D} and are installed together in the DOC-3 commit, identified by content hash;'),
    ('is a candidate pending owner ratification, to be installed with this register; its ratification is recorded as OWNER-RATIFIED [H1-DATE] when given, and its installation is verified after the install.',
     f'was OWNER-RATIFIED {D} and is installed with this register; its installation is verified after the install.'),
    ('| OWNER-RATIFIED [H1-DATE]; `ddf4de23', f'| OWNER-RATIFIED {short}; `ddf4de23'),
]:
    assert t.count(old) == 1, old[:60]
    assert all(ord(c) < 128 for c in new)
    t = t.replace(old, new)
assert '[H1-DATE]' not in t and 'RATIFICATION CANDIDATE (drafted 28 October 2026)' not in t
reg_final = t.encode('utf-8')
diff = ''.join(difflib.unified_diff(r.decode().splitlines(True), t.splitlines(True),
                                    'RATIFICATION_REGISTER_v0_9_candidate.md', 'RATIFICATION_REGISTER_v0_9.md', n=0))

out = Path(outdir)
if out.exists():
    shutil.rmtree(out)
ov = out / 'repo_overlay'
lf = lambda b: b.replace(b'\r\n', b'\n')
files = {
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r3.md': h,
    'doc/RATIFICATION_REGISTER_v0_9.md': reg_final,
    'review/DOC3_Register_v0_9_candidate_to_final.diff': diff.encode('utf-8'),
    'review/Independent_ChatGPT_EX_016_DOC3_H1_v1r3_Register_v0_9_Review.md': lf(e16),
    'review/Independent_ChatGPT_EX_018_DOC3_Register_v0_9_r1_Recheck.md': lf(e18),
}
for p, b in files.items():
    assert b'\r' not in b, p
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(b)
man = '# DOC-3 installation manifest (Git-content SHA-256, LF)\n' + ''.join(f'{sha(b)}  {p}\n' for p, b in sorted(files.items()))
mp = 'review/DOC3_Install_v1/INSTALL_MANIFEST_SHA256.txt'
(ov / mp).parent.mkdir(parents=True, exist_ok=True)
(ov / mp).write_bytes(man.encode('ascii'))
files[mp] = man.encode('ascii')
NEW = {p: sha(b) for p, b in files.items()}

v = open(Path(__file__).with_name('verifier_template.py')).read()
v = (v.replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEW.items())))
      .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in GUARDED.items()))
      .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEW))))
assert '@@' not in v
(out / 'VERIFY_DOC3_INSTALL.py').write_bytes(v.encode('ascii'))
cmd = ('@echo off\r\nsetlocal\r\nrem OPTIONAL owner-run staging of exactly the %d DOC-3 paths. No commit, push or deletion.\r\ngit add -- ^\r\n' % len(NEW)
       + ' ^\r\n'.join('  "%s"' % p.replace('/', '\\') for p in sorted(NEW)) + '\r\n'
       + 'if errorlevel 1 (echo STAGING FAILED & exit /b 1)\r\ngit status --short\r\nendlocal\r\n')
(out / 'STAGE_EXACT_FILES.cmd').write_bytes(cmd.encode('ascii'))
P = r'E:\TEMP\DOC3_Install_v1'
instr = f"""# DOC-3 - installation of H-1 v1r3 and register v0.9 (both owner-ratified {D})

Windows CMD, repository root. Delete any earlier extracted `E:\\TEMP\\DOC3_*` folders, then save this ZIP to `E:\\TEMP` and extract it there (`tar -xf "E:\\TEMP\\DOC3_Install_v1.zip" -C E:\\TEMP`).

**Step 1 - bring your copy up to date and check it** (`git status --short` must print nothing; the pull must say `Fast-forward` or `Already up to date`):

```bat
git status --short
git pull --ff-only
python "{P}\\VERIFY_DOC3_INSTALL.py" --repo . --phase pre
```

Expected: `PRE PASS`. If the pull or PRE fails, stop and send Claude the output. Nothing has changed yet.

**Step 2 - copy, check, stage:**

```bat
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\VERIFY_DOC3_INSTALL.py" --repo . --phase post
call "{P}\\STAGE_EXACT_FILES.cmd"
git diff --cached --name-status
```

Expected: `{len(NEW)} File(s) copied` (all new; nothing is replaced or deleted); `POST PASS`; {len(NEW)} lines starting with `A`. If POST prints `STOP`, stop and send Claude the output (nothing is committed; the copied files are only new files).

**Step 3 - commit and check the commit (do not push yet):**

```bat
git commit -m "DOC-3: H-1 v1r3 and register v0.9 (owner-ratified {D})"
python "{P}\\VERIFY_DOC3_INSTALL.py" --repo . --phase committed
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
print('register v0.9 final', sha(reg_final))
for p, x in sorted(NEW.items()):
    print(x, p)
