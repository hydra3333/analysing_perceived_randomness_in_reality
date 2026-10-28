"""Build the NAMES-1 code installation package (Claude, 28 Oct 2026).

Usage: python3 -I build_names1_install.py BASE_TREE RENAMED_TREE REGISTER_V08 OUTDIR [EXTRA_REVIEW_FILE ...]
BASE_TREE: an export of the repository after DOC-2 (src/tests unchanged since 38fc60e).
RENAMED_TREE: the same export after apply_trial.py (the NAMES-1 map). REGISTER_V08: the register
candidate (for review) or its finalised bytes (for install). EXTRA files go under review/.
Writes: repo_overlay/, RENAME_FILES.cmd, STAGE_EXACT_FILES.cmd, VERIFY_NAMES1_INSTALL.py,
RUN_NAMES1_SUITE.py, CHECK_NAMES1_IMPORTS.py, INSTALL_INSTRUCTIONS.md, and a Linux test helper
rename_files_for_linux_test.sh (not for the owner).
"""
import hashlib, json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'tools'))
import rename_map as R

base, renamed, reg, outdir = (Path(x) for x in sys.argv[1:5])
extra = [Path(x) for x in sys.argv[5:]]
BASE_COMMIT = '908db9ea9d4a37b17833f5d43919804c78ef7e14'  # the DOC-2 commit
W = Path('/home/claude/work')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_blob(path):
    # .bat files are checked out (and archived) with CRLF by .gitattributes; Git stores LF blobs.
    import os, subprocess
    return subprocess.run(['git', '-C', os.environ['NAMES1_BASE_GIT'], 'show', f'HEAD:{path}'],
                          check=True, capture_output=True).stdout


renames = R.files()
inv = {v: k for k, v in renames.items()}
in_place = ['src/Powerball_Experiment_Coordinator.py', 'src/methods/E_001_Historical_Appearance_Frequency.py',
            'src/methods/POC_MultiGame_Synthetic_Worker.py']
edited = {}
for new in list(renames.values()) + in_place:
    old = inv.get(new, new)
    ob, nb = (base / old).read_bytes(), (renamed / new).read_bytes()
    if ob != nb:
        edited[new] = nb
assert len(edited) == 27 and all(p in edited for p in in_place), len(edited)
pure = [n for n in renames.values() if n not in edited]
assert len(pure) == 3, pure
base_sha = {p: sha((base / p).read_bytes()) for p in list(renames) + in_place}

ev = HERE / 'evidence'
new_files = {
    'doc/Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md': W / 'names1/v02/Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md',
    'doc/RATIFICATION_REGISTER_v0_8.md': reg,
    'review/NAMES1_Spec_Review_v0_1.zip': W / 'names1/NAMES1_Spec_Review_v0_1.zip',
    'review/Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md': W / 'names1/reviews/Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md',
    'review/NAMES1_Spec_Recheck_v0_2.zip': W / 'names1/NAMES1_Spec_Recheck_v0_2.zip',
    'review/Independent_ChatGPT_Focused_Recheck_NAMES1_Spec_v0_2.md': W / 'names1/reviews/Independent_ChatGPT_Focused_Recheck_NAMES1_Spec_v0_2.md',
    'review/Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md': W / 'e1align/Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md',
    'doc/Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md': HERE / 'history/Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md',
    'review/Independent_ChatGPT_E1_ALIGN_Early_Design_Comments_28Oct2026.md': HERE / 'history/Independent_ChatGPT_E1_ALIGN_Early_Design_Comments_28Oct2026.md',
    'review/Independent_ChatGPT_R3_Review_E1_ALIGN_v0_1.md': HERE / 'history/Independent_ChatGPT_R3_Review_E1_ALIGN_v0_1.md',
    'review/Independent_ChatGPT_E1_ALIGN_v0_2_Focused_Recheck_v0_1.md': HERE / 'history/Independent_ChatGPT_E1_ALIGN_v0_2_Focused_Recheck_v0_1.md',
    'review/Independent_ChatGPT_EX_009_E1_ALIGN_v0_2r1_and_NAMES1_Order_Recheck.md': HERE / 'history/Independent_ChatGPT_EX_009_E1_ALIGN_v0_2r1_and_NAMES1_Order_Recheck.md',
    'review/Independent_ChatGPT_NAMES1_Code_Review_v0_1.md': HERE / 'history/Independent_ChatGPT_NAMES1_Code_Review_v0_1.md',
    'review/Independent_ChatGPT_Register_v0_8_Review_v0_1.md': HERE / 'history/Independent_ChatGPT_Register_v0_8_Review_v0_1.md',
    'review/NAMES1_Code_Install_v1/names1_allowlist.tsv': ev / 'names1_allowlist.tsv',
    'review/NAMES1_Code_Install_v1/t02_check_output.txt': ev / 't02_check_output.txt',
    'review/NAMES1_Code_Install_v1/ast_check_output.txt': ev / 'ast_check_output.txt',
    'review/NAMES1_Code_Install_v1/negative_checks_output.txt': ev / 'negative_checks_output.txt',
    'review/NAMES1_Code_Install_v1/suite_per_module_linux.txt': ev / 'suite_per_module_linux.txt',
}
for e in extra:
    new_files['review/' + e.name] = e
# History files the owner already committed (2c76664, byte-identical): guarded, not added.
already = {p: src for p, src in new_files.items() if (base / p).exists()}
for p, src in already.items():
    assert (base / p).read_bytes() == src.read_bytes(), f'already-committed file differs: {p}'
    del new_files[p]
expected = dict(edited)
for p, src in new_files.items():
    expected[p] = src.read_bytes()
pinned = {
    'doc/Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md': '07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a',
    'review/NAMES1_Spec_Review_v0_1.zip': '6aab40a1407c4b438ce05b7132ee2d3e183a6feb711d6f5877d9becc3246325f',
    'review/NAMES1_Spec_Recheck_v0_2.zip': 'fddf24f147406038653673e49350a7737b97c518849e46fc8c7b178d06b442a6',
    'review/Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md': '30d24ed02ff4ba3b0c84c760f306c8bfd02ddd2717db61013e60f855e3ace85a',
    'review/Independent_ChatGPT_Focused_Recheck_NAMES1_Spec_v0_2.md': '020fe9f73ba15f5260812d06701713d7b439880afb4197ace3488c4d63849f45',
    'review/Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md': '244aac86c72ff696e1d658023de8ab14035f2bb732585467bd140830e461cb59',
    'doc/Predictive_Randomness_E1_ALIGN_Specification_v0_2r1.md': 'd9ffd900c74d8a0cc5002bb78c83121f818514cd88ca9150bada8d6d1fa6653a',
    'review/Independent_ChatGPT_E1_ALIGN_Early_Design_Comments_28Oct2026.md': '0cf83504ecd35440cc35723d74dcafab5c58b4dbd33c7feb3daaca3b475021af',
    'review/Independent_ChatGPT_R3_Review_E1_ALIGN_v0_1.md': 'ba64d1ef5a05718ac87f80802a74f08bde88b224c75a6cf58e6e9b7fb946df13',
    'review/Independent_ChatGPT_E1_ALIGN_v0_2_Focused_Recheck_v0_1.md': '7a887a780875da5b0f3f315b84d695c363017f8078aa6f6530939a9e5e9683c9',
    'review/Independent_ChatGPT_EX_009_E1_ALIGN_v0_2r1_and_NAMES1_Order_Recheck.md': 'fbe0584ab69d7c59403bfc1f2e65aa3d868573d4fa17c38e6770d0ede7810248',
    'review/Independent_ChatGPT_NAMES1_Code_Review_v0_1.md': '767fb75084f23180f8573a3bb0d759a8461fa71f3bf01e185a39e1bcde5646d7',
    'review/Independent_ChatGPT_Register_v0_8_Review_v0_1.md': '536bbd6807fa921e2f9426a6c66172754ec0c1e9370e9258b708c649ac7caab4',
}
for p, h in pinned.items():
    assert sha(expected[p] if p in expected else (base / p).read_bytes()) == h, p

man_path = 'review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt'
lines = [f'{sha(b)}  {p}' for p, b in sorted(expected.items())]
lines += [f'{base_sha[inv[n]]}  {n}  (pure rename of {inv[n]})' for n in sorted(pure)]
lines += [f'-  {o}  (removed by rename to {n})' for o, n in sorted(renames.items())]
manifest = ('# NAMES-1 code installation manifest (Git-content SHA-256, LF)\n' + '\n'.join(lines) + '\n').encode()
expected[man_path] = manifest
new_list = sorted(set(new_files) | {man_path})

out = outdir
if out.exists():
    shutil.rmtree(out)
ov = out / 'repo_overlay'
for p, b in expected.items():
    (ov / p).parent.mkdir(parents=True, exist_ok=True)
    (ov / p).write_bytes(b)
data = {
    'renames': renames, 'base_sha': base_sha,
    'new_sha': {p: sha(b) for p, b in sorted(expected.items())},
    'in_place': in_place, 'new_files': new_list, 'old_names': sorted(R.bare()),
    'guarded': {
        'doc/HANDOVER/Claude_Primary_Handover_H1_v1r2.md': '55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0',
        'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md': 'a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1',
        'doc/RATIFICATION_REGISTER_v0_7.md': 'f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015',
        'doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md': '0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954',
        **{b: sha(git_blob(b)) for b in sorted(p.name for p in base.glob('*.bat'))},
        'tests/fixtures/coordinator_v0_6_baseline/Powerball_Experiment_Coordinator_v0_6.py.txt':
            sha((base / 'tests/fixtures/coordinator_v0_6_baseline/Powerball_Experiment_Coordinator_v0_6.py.txt').read_bytes()),
        'tests/p3_e1_synthetic_v0_3.json': sha((base / 'tests/p3_e1_synthetic_v0_3.json').read_bytes()),
        **{p: sha((base / p).read_bytes()) for p in sorted(already)},
    },
}
assert len(data['guarded']) == 12 + len(already), len(data['guarded'])
print('already committed (now guarded):', len(already), sorted(already))
v = (HERE / 'verify_template.py').read_text().replace('@@BASE@@', BASE_COMMIT).replace('@@DATA@@', json.dumps(data, indent=1, sort_keys=True))
(out / 'VERIFY_NAMES1_INSTALL.py').write_text(v, newline='\n')
mods = {}
for old, new in {**R.MODULES, **R.TESTS}.items():
    leaf = new.split('.')[-1]
    rel = [n for n in renames.values() if Path(n).stem == leaf][0]
    mods[old] = [new, rel]
c = (HERE / 'CHECK_NAMES1_IMPORTS.py').read_text().replace('@@MODULES@@', json.dumps(mods, indent=1, sort_keys=True))
(out / 'CHECK_NAMES1_IMPORTS.py').write_text(c, newline='\n')
shutil.copy(HERE / 'RUN_NAMES1_SUITE.py', out / 'RUN_NAMES1_SUITE.py')

win = lambda p: p.replace('/', '\\')
mv = ['@echo off', 'setlocal',
      'rem NAMES-1: the 27 explicit renames (git mv). Run from the repository root after PRE PASS.',
      'rem Stops at the first failure. No commit, push or deletion of content.']
for o, n in sorted(renames.items()):
    mv.append(f'git mv -- "{win(o)}" "{win(n)}" || goto :fail')
mv += ['echo RENAMES DONE: 27 files renamed in the index.', 'endlocal', 'exit /b 0', ':fail',
       'echo RENAME FAILED: stop and send Claude this output.', 'endlocal', 'exit /b 1']
(out / 'RENAME_FILES.cmd').write_bytes(('\r\n'.join(mv) + '\r\n').encode('ascii'))
(out / 'rename_files_for_linux_test.sh').write_text(
    'set -e\n' + ''.join(f'git mv -- "{o}" "{n}"\n' for o, n in sorted(renames.items())), newline='\n')
stage_paths = sorted(edited) + new_list
st = ['@echo off', 'setlocal',
      f'rem OPTIONAL owner-run staging of the {len(stage_paths)} NAMES-1 content paths (the renames are already staged).',
      'rem No commit, push or deletion.', 'git add -- ^']
st.append(' ^\r\n'.join(f'  "{win(p)}"' for p in stage_paths))
st += ['if errorlevel 1 (echo STAGING FAILED & exit /b 1)', 'git status --short', 'endlocal']
(out / 'STAGE_EXACT_FILES.cmd').write_bytes(('\r\n'.join(st) + '\r\n').encode('ascii'))
(out / 'stage_for_linux_test.sh').write_text('set -e\ngit add -- ' + ' '.join(f'"{p}"' for p in stage_paths) + '\n', newline='\n')

n_new = len(new_list)
instr = f"""# NAMES-1 - code installation (only after the reviewer's code RECHECK PASS and the owner's go-ahead)

DOC-2 must already be installed. Windows CMD, repository root. `git status --short` must print nothing first. Delete any earlier extracted `E:\\TEMP\\NAMES1_*` folders, then save this ZIP to `E:\\TEMP` and extract it there (`tar -xf "E:\\TEMP\\NAMES1_Code_Install_v1.zip" -C E:\\TEMP`).

## 1. Check, rename, copy, check

```bat
python "E:\\TEMP\\NAMES1_Code_Install_v1\\VERIFY_NAMES1_INSTALL.py" --repo . --phase pre
call "E:\\TEMP\\NAMES1_Code_Install_v1\\RENAME_FILES.cmd"
xcopy "E:\\TEMP\\NAMES1_Code_Install_v1\\repo_overlay\\*" . /E /Y
python "E:\\TEMP\\NAMES1_Code_Install_v1\\VERIFY_NAMES1_INSTALL.py" --repo . --phase post
```

Expected: `PRE PASS`; `RENAMES DONE`; `{len(expected)} File(s) copied` ({len(edited)} replace renamed or existing files, as intended; {n_new} are new); `POST PASS`.

## 2. Tests and import checks (offline; nothing is changed)

```bat
.venv\\Scripts\\python.exe "E:\\TEMP\\NAMES1_Code_Install_v1\\RUN_NAMES1_SUITE.py" --repo .
.venv\\Scripts\\python.exe "E:\\TEMP\\NAMES1_Code_Install_v1\\CHECK_NAMES1_IMPORTS.py" --repo .
```

Expected: `SUITE PASS` (79 tests; the only allowed skips are the two symlink tests, if Windows cannot create symlinks), then `RESULT PASS`. Send Claude both outputs whatever they say. If either says `STOP`, do not commit: to undo, run `git reset --hard` and then `git clean -fd -- doc review`, which puts the repository back exactly as it was.

## 3. Stage, commit, check, and only then push

```bat
call "E:\\TEMP\\NAMES1_Code_Install_v1\\STAGE_EXACT_FILES.cmd"
git diff --cached --name-status
git commit -m "NAMES-1: one-off rename to stable file names; NAMES-1 v0.2 (ratified) and register v0.8"
python "E:\\TEMP\\NAMES1_Code_Install_v1\\VERIFY_NAMES1_INSTALL.py" --repo . --phase committed
```

Expected: the staged list shows renames (`R`) and modifications (`M`), and {n_new} lines starting with `A`; then `COMMITTED PASS`. **Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID. Claude then verifies it from GitHub and runs the immediate recovery check (N1-T10) in a disposable clone. If the committed check prints `STOP`, do **not** push: send Claude the output (the commit is still only on your PC; `git reset --hard HEAD~1` removes it). If anything else prints `STOP`, stop and send Claude the output.
"""
(out / 'INSTALL_INSTRUCTIONS.md').write_text(instr, newline='\r\n')
print('edited', len(edited), 'pure renames', len(pure), 'new files', n_new, 'overlay files', len(expected))
print('register v0.8 in package', sha(expected['doc/RATIFICATION_REGISTER_v0_8.md']))
print('manifest', sha(manifest))
