"""Build DOC-9, the document-only install of register v0.22 and three review copies (Claude, 31 October 2026).

Usage: python3 -I build_doc9.py REGISTER_v0_22 OUTDIR BASE_COMMIT
Adds only new files: doc/RATIFICATION_REGISTER_v0_22.md, three LF review copies under review/, and the builder, the
register diff and the manifest under review/DOC9_Register22_v1/. Nothing is replaced or deleted. The verifier is the
REL-1/WF-1A template (A lines only).
"""
import hashlib, shutil, subprocess, sys
from pathlib import Path

reg, outdir, BASE = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
HERE = Path(__file__).resolve().parent
REPO = '/home/claude/analysing_perceived_randomness_in_reality'
PKG, TITLE = 'DOC9_Register22_v1', 'DOC-9 package (register v0.22 and three review copies; document-only)'
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {'doc/RATIFICATION_REGISTER_v0_22.md': reg.read_bytes()}
for f in sorted((HERE / 'docs' / 'review').glob('*.md')):
    files[f'review/{f.name}'] = f.read_bytes()
files[f'review/{PKG}/make_register_v22.py'] = (HERE / 'make_register_v22.py').read_bytes()
files[f'review/{PKG}/register_v0_21_to_v0_22.diff'] = (HERE / 'register_v0_21_to_v0_22.diff').read_bytes()
for p, raw in files.items():
    assert b'\r' not in raw, p
    assert raw.isascii() or p.startswith('doc/RATIFICATION_REGISTER_') or p.endswith('.diff'), p
    r = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', f'{BASE}:{p}'], capture_output=True)
    assert r.returncode != 0, f'already in the base: {p}'
mp = f'review/{PKG}/INSTALL_MANIFEST_SHA256.txt'
man = (f'# {PKG} installation manifest (Git-content SHA-256, LF); "A" new path\n' +
       ''.join(f'A {sha(raw)}  {p}\n' for p, raw in sorted(files.items())))
files[mp] = man.encode('ascii')
GUARDED_PATHS = ['doc/RATIFICATION_REGISTER_v0_21.md', 'doc/Predictive_Randomness_CODE3_and_E1_Revision2_Design_v0_1r2.md',
                 'doc/Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md',
                 'doc/Deferred_Performance_Engineering_Proposal_v0_1.md',
                 'src/methods/_common/contract_runner.py', 'src/methods/_common/walk_forward.py',
                 'src/methods/E_001/multigame_e1.py', 'results/audit/SEARCH_LOG.csv']
guarded = {p: sha(subprocess.run(['git', '-C', REPO, 'show', f'{BASE}:{p}'], capture_output=True, check=True).stdout)
           for p in GUARDED_PATHS}
if outdir.exists():
    shutil.rmtree(outdir)
for p, raw in files.items():
    (outdir / 'repo_overlay' / p).parent.mkdir(parents=True, exist_ok=True)
    (outdir / 'repo_overlay' / p).write_bytes(raw)
VERIFIER = 'VERIFY_DOC9_INSTALL.py'
v = (Path('/home/claude/work/wf1code/verifier_template.py').read_text()
     .replace('@@NEW@@', '\n'.join(f"    '{p}': '{sha(raw)}'," for p, raw in sorted(files.items())))
     .replace('@@MODIFIED@@', '').replace('@@DELETED@@', '')
     .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in guarded.items()))
     .replace('@@BASE@@', BASE).replace('@@N@@', str(len(files))).replace('@@M@@', '0').replace('@@D@@', '0')
     .replace('@@TITLE@@', TITLE).replace('@@VERIFIER@@', VERIFIER))
assert '@@' not in v
(outdir / VERIFIER).write_bytes(v.encode('ascii'))
P = rf'E:\TEMP\{PKG}'
instr = f"""# {PKG} - {TITLE} (only after the owner's ratification)

Windows CMD, repository root. **Save the ZIP to `E:\\TEMP`, not into the repository**, and extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(files)} new files and changes nothing else: register v0.22, three review copies, and its builder, diff and manifest. No code changes, so no tests are needed.

## 1. Update, check, copy, check

```bat
git status --short
git pull --ff-only
python "{P}\\{VERIFIER}" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\{VERIFIER}" --repo . --phase post
```

Expected: `git status --short` prints nothing (if it prints anything, stop and send Claude the output); the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{len(files)} File(s) copied`; `POST PASS`. If anything prints `STOP`, do not commit: send Claude the output.

## 2. Stage, commit, check, and only then push

```bat
git add doc review
git status --short
git commit -m "DOC-9: register v0.22 (owner-ratified 31 October 2026) and three review copies (document-only install)"
python "{P}\\{VERIFIER}" --repo . --phase committed
```

Expected: `git status --short` lists {len(files)} lines starting with `A`, and nothing else; then `COMMITTED PASS`.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:** `git push`, then `git rev-parse HEAD`, and send Claude the commit ID.
"""
(outdir / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(PKG, len(files), 'new files; base', BASE)
