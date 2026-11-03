"""Build DOC-11, the Claude handover package (document-only install; Claude, 3 November 2026).

Usage: python3 -I build_doc11.py WORKDIR OUTDIR BASE_COMMIT STATUS(CANDIDATE|RATIFIED) [DATE text for @@DATE@@, RATIFIED only]
WORKDIR holds this chat's DOC-11 sources: make_register_v24.py, reg24_section.md, make_h1_v1r8.py and the H-1 v1r8
blurb. Adds only new files, all under doc/ and review/ (no file is replaced; nothing under src/ or tests/): register
v0.24; H-1 v1r8 and its introductory blurb; the ratified MHUP-1 design v0.1r5 (byte-identical to EX_132's member);
the direction document v0.2r1 (the exchange copy, CRLF to LF); six LF review copies; and under
review/DOC11_Claude_Handover_v1/ the builders, their diffs, this builder and the manifest. Under the owner's staged
handover (HO-2) there is no H-2 edition in this package. The verifier is the WF-1B/PERF-1 template (A lines only).
"""
import hashlib, shutil, subprocess, sys
from pathlib import Path

W, outdir, BASE, STATUS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
DATE = sys.argv[5] if len(sys.argv) > 5 else None
REPO = '/home/claude/analysing_perceived_randomness_in_reality'
TPL = Path(REPO) / 'exchange/CLAUDE_WEB_TOOLS/wf1/verifier_template.py'
PKG = 'DOC11_Claude_Handover_v1'
TITLE = 'DOC-11 Claude handover package (register v0.24, H-1 v1r8 and blurb, the MHUP-1 design v0.1r5, the direction document; document-only)'
R = f'review/{PKG}'
sha = lambda b: hashlib.sha256(b).hexdigest()


def git_blob(rev, p):
    return subprocess.run(['git', '-C', REPO, 'show', f'{rev}:{p}'], capture_output=True, check=True).stdout


def run(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    assert r.returncode == 0, (a, r.stdout, r.stderr)
    return r.stdout


B = outdir.parent / (outdir.name + '_build')
if B.exists():
    shutil.rmtree(B)
B.mkdir(parents=True)
(B / 'reg23.md').write_bytes(git_blob(BASE, 'doc/RATIFICATION_REGISTER_v0_23.md'))
(B / 'h1v1r7.md').write_bytes(git_blob(BASE, 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md'))
run(sys.executable, '-I', str(W / 'make_h1_v1r8.py'), str(B / 'h1v1r7.md'), str(B / 'H1_v1r8.md'), STATUS)
if DATE:
    (B / 'H1_v1r8.md').write_bytes((B / 'H1_v1r8.md').read_bytes().replace(b'@@DATE@@', DATE.encode('ascii')))
h1sha = sha((B / 'H1_v1r8.md').read_bytes())
blsha = sha((W / 'Claude_Primary_Handover_H1_v1r8_introductory_blurb.md').read_bytes())
run(sys.executable, '-I', str(W / 'make_register_v24.py'), str(B / 'reg23.md'), str(W / 'reg24_section.md'),
    str(B / 'RATIFICATION_REGISTER_v0_24.md'), STATUS, *([] if STATUS == 'CANDIDATE' else [h1sha, blsha]))
for name in ('RATIFICATION_REGISTER_v0_24.md', 'H1_v1r8.md'):
    if DATE:
        p = B / name
        p.write_bytes(p.read_bytes().replace(b'@@DATE@@', DATE.encode('ascii')))
    assert b'@@' not in (B / name).read_bytes(), name


def udiff(a, b, la, lb):
    r = subprocess.run(['diff', '-u', '--label', la, '--label', lb, str(a), str(b)], capture_output=True)
    assert r.returncode == 1, r.stderr
    return r.stdout


blurb = (W / 'Claude_Primary_Handover_H1_v1r8_introductory_blurb.md').read_bytes()
design = git_blob(BASE, 'exchange/EX_132_Claude/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md')
assert sha(design) == 'e5fb491ca601fa71793d143871d99c40929d20cdd8398fe92e0c6858c44a5455'
direction = git_blob(BASE, 'exchange/Direction_for_operational_procedures_v0_2r1.md').replace(b'\r\n', b'\n')
assert sha(direction) == '0aa5967febb817707953b4634937a9a76e2a56e364360cfd1004d10d85c56855'
files = {
    'doc/RATIFICATION_REGISTER_v0_24.md': (B / 'RATIFICATION_REGISTER_v0_24.md').read_bytes(),
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md': (B / 'H1_v1r8.md').read_bytes(),
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r8_introductory_blurb.md': blurb,
    'doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r5.md': design,
    'doc/Direction_for_operational_procedures_v0_2r1.md': direction,
    f'{R}/make_register_v24.py': (W / 'make_register_v24.py').read_bytes(),
    f'{R}/reg24_section.md': (W / 'reg24_section.md').read_bytes(),
    f'{R}/register_v0_23_to_v0_24.diff': udiff(B / 'reg23.md', B / 'RATIFICATION_REGISTER_v0_24.md',
                                               'doc/RATIFICATION_REGISTER_v0_23.md', 'doc/RATIFICATION_REGISTER_v0_24.md'),
    f'{R}/make_h1_v1r8.py': (W / 'make_h1_v1r8.py').read_bytes(),
    f'{R}/H1_v1r7_to_v1r8.diff': udiff(B / 'h1v1r7.md', B / 'H1_v1r8.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md',
                                       'doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md'),
    f'{R}/build_doc11.py': Path(__file__).resolve().read_bytes(),
    f'{R}/H1_blurb_v1r7_to_v1r8.diff': None,
    f'{R}/e2e_doc11.sh': (W / 'e2e_doc11.sh').read_bytes(),
}
(B / 'blurb_v1r7.md').write_bytes(git_blob(BASE, 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md'))
files[f'{R}/H1_blurb_v1r7_to_v1r8.diff'] = udiff(B / 'blurb_v1r7.md', W / 'Claude_Primary_Handover_H1_v1r8_introductory_blurb.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r8_introductory_blurb.md')
REVIEW_COPIES = {
    'review/Independent_ChatGPT_MHUP1_Design_R3_Review_EX125.md': 'exchange/EX_125_ChatGPT.md',
    'review/Independent_ChatGPT_MHUP1_Design_Focused_RECHECK_EX127.md': 'exchange/EX_127_ChatGPT.md',
    'review/Independent_ChatGPT_MHUP1_Design_Narrow_RECHECK_EX129.md': 'exchange/EX_129_ChatGPT.md',
    'review/Independent_ChatGPT_MHUP1_Design_Conditional_PASS_EX131.md': 'exchange/EX_131_ChatGPT.md',
    'review/Independent_ChatGPT_Direction_v0_1_Content_Check_RECHECK.md': 'exchange/Direction_v0_1_review_ChatGPT_2026_11_02_RECHECK.md',
    'review/Independent_ChatGPT_Direction_v0_2_Focused_PASS.md': 'exchange/Direction_v0_2_review_ChatGPT_2026_11_02_PASS.md',
}
EXPECT_REVIEW = {
    'review/Independent_ChatGPT_MHUP1_Design_R3_Review_EX125.md': '546397c546a8a3dc8e0ba6d60c58c51619b7ada48741d145d8e46ce54e66c081',
    'review/Independent_ChatGPT_MHUP1_Design_Focused_RECHECK_EX127.md': '4620321d51b29be913f0bc6db466432416200dab1a3753c3720bf423888ccfe2',
    'review/Independent_ChatGPT_MHUP1_Design_Narrow_RECHECK_EX129.md': 'cb8c8239a6cf0df3bc497a783621ad0c3888ea6b14426729de3b41e88cd7756b',
    'review/Independent_ChatGPT_MHUP1_Design_Conditional_PASS_EX131.md': '01840b8dcafc7fad4382028dd87509f3b2414990583b51b8f7806eb4488b9efa',
    'review/Independent_ChatGPT_Direction_v0_1_Content_Check_RECHECK.md': '45091f629cf6936e2222717466a0c45eaff420269ce15d5df8552dc7653c1580',
    'review/Independent_ChatGPT_Direction_v0_2_Focused_PASS.md': 'a8c61caedb3a7704f243bc96c52e6102f743b15bd244f5c8eb853633ee3c70fd',
}
for p, ex in REVIEW_COPIES.items():
    files[p] = git_blob(BASE, ex).replace(b'\r\n', b'\n')
    assert sha(files[p]) == EXPECT_REVIEW[p], p
UTF8_OK = {'doc/RATIFICATION_REGISTER_v0_24.md', *REVIEW_COPIES}  # the reviewer's texts are kept as written
for p, raw in files.items():
    assert b'\r' not in raw, p
    assert raw.isascii() or p in UTF8_OK or p.endswith('.diff'), p
    r = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', f'{BASE}:{p}'], capture_output=True)
    assert r.returncode != 0, f'already in the base: {p}'
    assert p.startswith(('doc/', 'review/')), p
GUARDED_PATHS = [
    'doc/RATIFICATION_REGISTER_v0_23.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md', 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8_introductory_blurb.md',
    'doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md',
    'doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md',
    'doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md',
    'doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md', 'doc/Direction_for_operational_procedures_v0_2_to_v0_2r1.diff',
    'doc/owner_stocktake_v1_0.txt', 'README.md', '.gitattributes', '.claude/settings.json',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md', 'Run_Experiment.bat', 'Run_Results_Updater.bat', 'Run_Coordinator.bat',
    'Run_Method_Rankings.bat', 'src/results_master_v0_1.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/contract_dispatch.py', 'src/methods/_common/contract_runner.py',
    'src/evaluation/outcome_reader.py', 'src/Powerball_Experiment_Coordinator.py',
]
mp = f'{R}/INSTALL_MANIFEST_SHA256.txt'
files[mp] = (f'# {PKG} installation manifest (Git-content SHA-256, LF); "A" new path\n' +
             ''.join(f'A {sha(raw)}  {p}\n' for p, raw in sorted(files.items()))).encode('ascii')
NEWH = {p: sha(raw) for p, raw in files.items()}
guarded = {p: sha(git_blob(BASE, p)) for p in GUARDED_PATHS}
if outdir.exists():
    shutil.rmtree(outdir)
for p, raw in files.items():
    (outdir / 'repo_overlay' / p).parent.mkdir(parents=True, exist_ok=True)
    (outdir / 'repo_overlay' / p).write_bytes(raw)
VERIFIER = 'VERIFY_DOC11_INSTALL.py'
v = (TPL.read_text()
     .replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEWH.items())))
     .replace('@@MODIFIED@@', '').replace('@@DELETED@@', '')
     .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in guarded.items()))
     .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEWH))).replace('@@M@@', '0').replace('@@D@@', '0')
     .replace('@@TITLE@@', TITLE).replace('@@VERIFIER@@', VERIFIER))
assert '@@' not in v
(outdir / VERIFIER).write_bytes(v.encode('ascii'))
P = rf'E:\TEMP\{PKG}'
instr = f"""# {PKG} - {TITLE}

**Install only after the ChatGPT reviewer's Step 1.1 review of this package is resolved and you have ratified it (HO-2).**
Windows CMD, repository root. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\{PKG}` folder, then extract it there (`tar -xf "E:\\TEMP\\{PKG}.zip" -C E:\\TEMP`). This package adds {len(NEWH)} new files, all under `doc/` and `review/`, and replaces and deletes nothing. No file under `src/` or `tests/` changes, so the test suite is not needed.

## 1. Update, check, copy, check

```bat
git status --short
git pull --ff-only
python "{P}\\{VERIFIER}" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\{VERIFIER}" --repo . --phase post
```

Expected: the first `git status --short` prints nothing; the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{len(NEWH)} File(s) copied`; `POST PASS`. If anything prints `STOP`, do not commit: send Claude the whole output.

## 2. Stage, commit, check, and only then push

```bat
git add doc review
git status --short
git commit -m "DOC-11: the Claude handover package - register v0.24, H-1 v1r8 and blurb, the ratified MHUP-1 design v0.1r5, the direction document v0.2r1, six review copies (document-only install)"
python "{P}\\{VERIFIER}" --repo . --phase committed
git status --short
```

Expected: the first `git status --short` lists {len(NEWH)} lines starting with `A` and nothing else; then `COMMITTED PASS`; then the last `git status --short` prints nothing. Git's "LF will be replaced by CRLF" warnings while staging are normal.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub. Then start the replacement Claude chat with the text of `doc\\HANDOVER\\Claude_Primary_Handover_H1_v1r8_introductory_blurb.md` (everything below its line), as HO-2 step 2 says.
"""
(outdir / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(PKG, len(NEWH), 'A; base', BASE)
for p in ('doc/RATIFICATION_REGISTER_v0_24.md', 'doc/HANDOVER/Claude_Primary_Handover_H1_v1r8.md',
          'doc/HANDOVER/Claude_Primary_Handover_H1_v1r8_introductory_blurb.md'):
    print(NEWH[p], p)
