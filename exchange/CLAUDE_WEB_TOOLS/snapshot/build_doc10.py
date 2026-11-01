"""Build DOC-10, the snapshot's document-only install (Claude, 1 November 2026).

Usage: python3 -I build_doc10.py OUTDIR BASE_COMMIT
Adds and replaces documents only (no file under src/ or tests/ changes): register v0.23, Architecture v0.9, H-1 v1r7
and H-2 v1r8 with their introductory blurbs, the holdout exposure record v0.3, the new-method template draft 4, the
repository README, the Claude Code rulebook v0.3, the .gitattributes rule for results/ (R-011), four LF review copies
(EX_109, EX_111, EX_113, EX_115), and under review/DOC10_Snapshot_v1/ the generators, their diffs, this builder and the
manifest. The verifier is the WF-1B/PERF-1 template (A and M lines).
"""
import hashlib, shutil, subprocess, sys
from pathlib import Path

outdir, BASE = Path(sys.argv[1]), sys.argv[2]
S = Path('/home/claude/work/snap')
REPO = '/home/claude/analysing_perceived_randomness_in_reality'
PKG, TITLE = 'DOC10_Snapshot_v1', 'DOC-10 snapshot package (register v0.23, Architecture v0.9, handovers and related documents; document-only)'
R = f'review/{PKG}'
sha = lambda b: hashlib.sha256(b).hexdigest()


def rd(p):
    b = Path(p).read_bytes()
    assert b'\r' not in b, p
    return b


def base_blob(p):
    return subprocess.run(['git', '-C', REPO, 'show', f'{BASE}:{p}'], capture_output=True, check=True).stdout


NEW = {
    'doc/RATIFICATION_REGISTER_v0_23.md': S / 'reg23/RATIFICATION_REGISTER_v0_23.md',
    'doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md': S / 'arch09/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7.md': S / 'h1/Claude_Primary_Handover_H1_v1r7.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md': S / 'h1/Claude_Primary_Handover_H1_v1r7_introductory_blurb.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md': S / 'h2/ChatGPT_Reviewer_Handover_H2_v1r8.md',
    'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8_introductory_blurb.md': S / 'h2/ChatGPT_Reviewer_Handover_H2_v1r8_introductory_blurb.md',
    'doc/HOLDOUT_EXPOSURE_RECORD_v0_3.md': S / 'misc/HOLDOUT_EXPOSURE_RECORD_v0_3.md',
    'doc/METHOD_TEMPLATE/CHANGES.md': S / 'misc/METHOD_TEMPLATE/CHANGES.md',
    f'{R}/make_register_v23.py': S / 'reg23/make_register_v23.py',
    f'{R}/register_v0_22_to_v0_23.diff': S / 'reg23/register_v0_22_to_v0_23.diff',
    f'{R}/make_arch_v09.py': S / 'arch09/make_arch_v09.py',
    f'{R}/arch_v0_8_to_v0_9.diff': S / 'arch09/arch_v0_8_to_v0_9.diff',
    f'{R}/make_h1_v1r7.py': S / 'h1/make_h1_v1r7.py',
    f'{R}/h1_section12.md': S / 'h1/section12.md',
    f'{R}/H1_v1r6_to_v1r7.diff': S / 'h1/H1_v1r6_to_v1r7.diff',
    f'{R}/make_h2_v1r8.py': S / 'h2/make_h2_v1r8.py',
    f'{R}/H2_v1r7_to_v1r8.diff': S / 'h2/H2_v1r7_to_v1r8.diff',
    f'{R}/make_blurbs_v1r7_v1r8.py': S / 'h1/make_blurbs_v1r7_v1r8.py',
    f'{R}/H1_blurb_v1r6_to_v1r7.diff': S / 'h1/H1_blurb_v1r6_to_v1r7.diff',
    f'{R}/H2_blurb_v1r7_to_v1r8.diff': S / 'h2/H2_blurb_v1r7_to_v1r8.diff',
    f'{R}/build_doc10.py': Path(__file__).resolve(),
}
REVIEW_COPIES = {
    'review/Independent_ChatGPT_WF1B_Code_R2_Review_EX109.md': 'exchange/EX_109_ChatGPT.md',
    'review/Independent_ChatGPT_WF1B_Code_Focused_RECHECK_EX111.md': 'exchange/EX_111_ChatGPT.md',
    'review/Independent_ChatGPT_WF1B_v3_Focused_Review_EX113.md': 'exchange/EX_113_ChatGPT.md',
    'review/Independent_ChatGPT_PERF1_Code_Review_EX115.md': 'exchange/EX_115_ChatGPT.md',
}
MOD = {
    'doc/METHOD_TEMPLATE/README.md': S / 'misc/METHOD_TEMPLATE/README.md',
    'doc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md': S / 'misc/METHOD_TEMPLATE/METHOD_SPECIFICATION_TEMPLATE.md',
    'README.md': S / 'misc/README.md',
    '.gitattributes': S / 'misc/gitattributes.proposed',
    'CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md': S / 'misc/CLAUDE_CODE_RULEBOOK_v0_3.md',
}
UTF8_OK = {'doc/RATIFICATION_REGISTER_v0_23.md', 'doc/Predictive_Randomness_Software_Architecture_Discussion_v0_9.md',
           'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r8.md'}
GUARDED_PATHS = [
    'src/evaluation/numerics.py', 'src/evaluation/report.py', 'src/evaluation/Method_Rankings_Report.py',
    'src/evaluation/n1.py', 'src/evaluation/n1_generator.py', 'src/evaluation/measures.py', 'src/evaluation/divisions.py',
    'src/evaluation/collect.py', 'src/evaluation/outcome_reader.py', 'src/evaluation/report_writer.py',
    'src/evaluation/seed_policies.py', 'src/evaluation/registry/MEASURE_REGISTRY_V1.json',
    'src/evaluation/registry/FAMILY_REGISTRY_V1.json',
    'src/evaluation/seed_policies/N1_ROOT_NIST_C2_20261031T1030Z_V1.json',
    'src/evaluation/seed_policies/N1_ROOT_NIST_C2_20261106T0000Z_V1.json',
    'src/methods/_common/walk_forward.py', 'src/methods/Method_Walk_Forward.py',
    'src/methods/_common/contract_runner.py', 'src/methods/_common/game_draws_reader.py',
    'src/methods/_common/game_profiles.py', 'src/Powerball_Experiment_Coordinator.py',
    'Run_Method_Rankings.bat', 'Run_Experiment.bat', 'Run_Coordinator.bat', 'Run_Results_Updater.bat',
    'doc/RATIFICATION_REGISTER_v0_22.md', 'doc/Predictive_Randomness_WF1B_Supplement_Design_v0_1r1.md',
    'doc/Predictive_Randomness_Releases_and_WF1_Design_v0_1r1.md',
    'doc/Predictive_Randomness_CODE3_and_E1_Revision2_Design_v0_1r2.md',
    'doc/Predictive_Randomness_Evaluation_and_Reporting_Specifications_R3_v0_5.md',
    'doc/HANDOVER/Claude_Primary_Handover_H1_v1r6.md', 'doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r7.md',
    'doc/HOLDOUT_EXPOSURE_RECORD_v0_2.md',
]

files = {p: rd(src) for p, src in NEW.items()}
for p, ex in REVIEW_COPIES.items():
    files[p] = (Path(REPO) / ex).read_bytes().replace(b'\r\n', b'\n')
replaced = {p: rd(src) for p, src in MOD.items()}
for p, raw in [*files.items(), *replaced.items()]:
    assert b'\r' not in raw, p
    assert raw.isascii() or p in UTF8_OK or p.endswith('.diff'), p
for p in files:
    r = subprocess.run(['git', '-C', REPO, 'cat-file', '-e', f'{BASE}:{p}'], capture_output=True)
    assert r.returncode != 0, f'already in the base: {p}'
for p, raw in replaced.items():
    assert base_blob(p) != raw, f'replacement unchanged: {p}'
assert not any(p.startswith(('src/', 'tests/')) for p in [*files, *replaced])
mp = f'{R}/INSTALL_MANIFEST_SHA256.txt'
man = (f'# {PKG} installation manifest (Git-content SHA-256, LF); "A" new path, "M" replaced file\n' +
       ''.join(f'A {sha(raw)}  {p}\n' for p, raw in sorted(files.items())) +
       ''.join(f'M {sha(raw)}  {p}  (base {sha(base_blob(p))})\n' for p, raw in sorted(replaced.items())))
files[mp] = man.encode('ascii')
NEWH = {p: sha(raw) for p, raw in files.items()}
MODH = {p: (sha(base_blob(p)), sha(raw)) for p, raw in replaced.items()}
guarded = {p: sha(base_blob(p)) for p in GUARDED_PATHS}
if outdir.exists():
    shutil.rmtree(outdir)
for p, raw in [*files.items(), *replaced.items()]:
    (outdir / 'repo_overlay' / p).parent.mkdir(parents=True, exist_ok=True)
    (outdir / 'repo_overlay' / p).write_bytes(raw)
VERIFIER = 'VERIFY_DOC10_INSTALL.py'
v = (Path('/home/claude/work/wf1code/verifier_template.py').read_text()
     .replace('@@NEW@@', '\n'.join(f"    '{p}': '{x}'," for p, x in sorted(NEWH.items())))
     .replace('@@MODIFIED@@', '\n'.join(f"    '{p}': ('{o}', '{n}')," for p, (o, n) in sorted(MODH.items())))
     .replace('@@DELETED@@', '')
     .replace('@@GUARDED@@', '\n'.join(f"    '{p}': '{x}'," for p, x in guarded.items()))
     .replace('@@BASE@@', BASE).replace('@@N@@', str(len(NEWH))).replace('@@M@@', str(len(MODH))).replace('@@D@@', '0')
     .replace('@@TITLE@@', TITLE).replace('@@VERIFIER@@', VERIFIER))
assert '@@' not in v
(outdir / VERIFIER).write_bytes(v.encode('ascii'))
TOTAL = len(NEWH) + len(MODH)
P = rf'E:\TEMP\{PKG}'
GIT_ADD = 'git add .gitattributes README.md CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md doc review'
instr = f"""# {PKG} - {TITLE} (only after the owner's ratification)

Windows CMD, repository root, with the project venv. **Save the ZIP to `E:\\TEMP`, not into the repository.** Delete any earlier extracted `E:\\TEMP\\{PKG}` folder, then extract it there (`tar -xf "E:\\TEMP\\{PKG}_candidate.zip" -C E:\\TEMP`). This package adds {len(NEWH)} new files and replaces {len(MODH)} (`.gitattributes`, `README.md`, `CLAUDE_CODE_WORKING_FOLDER_TREE/CLAUDE.md` and two template files). No file under `src/` or `tests/` changes, so the test suite is not needed: Claude ran it once on Linux with these documents in place (471 tests PASS).

## 0. First, check the line endings of the committed record files

The new `.gitattributes` rule (`results/** -text`) stops Git converting record files. Once it is in place, any record file whose working copy Git had already converted can show as modified whenever Git next rechecks it (at the POST check, or at some later `git status`). So check first:

```bat
git status --short
git ls-files --eol results
```

Expected: `git status --short` prints nothing, and every line of the second command shows `w/lf` (one empty log file may show `w/none`). **If any line shows `w/crlf`, stop here and send Claude the output:** Claude will give you the exact commands to put those files' committed bytes back, as for the Powerball batch records on 1 November 2026.

## 1. Update, check, copy, check

```bat
git pull --ff-only
python "{P}\\{VERIFIER}" --repo . --phase pre
xcopy "{P}\\repo_overlay\\*" . /E /Y
python "{P}\\{VERIFIER}" --repo . --phase post
git ls-files --eol results
```

Expected: the pull says `Fast-forward` or `Already up to date`; `PRE PASS`; `{TOTAL} File(s) copied`; `POST PASS`; and every results line still `w/lf` (or `w/none`). If anything prints `STOP`, do not commit: send Claude the output.

## 2. Stage, commit, check, and only then push

```bat
{GIT_ADD}
git status --short
git commit -m "DOC-10: the snapshot - register v0.23, Architecture v0.9, H-1 v1r7 and H-2 v1r8 with blurbs, holdout exposure record v0.3, template draft 4, README, Claude Code rulebook v0.3, .gitattributes results rule (document-only install)"
python "{P}\\{VERIFIER}" --repo . --phase committed
git status --short
```

Expected: the first `git status --short` lists {len(NEWH)} lines starting with `A` and {len(MODH)} starting with `M`, and nothing else; then `COMMITTED PASS`; then the last `git status --short` prints nothing (the new `.gitattributes` rule changes no stored file). Git's "LF will be replaced by CRLF" warnings while staging are normal.

**If the committed check prints `STOP`: do not push, and do not reset or undo anything.** Send Claude the whole output.

**Push only after `COMMITTED PASS`:**

```bat
git push
git rev-parse HEAD
```

Send Claude the commit ID; Claude verifies it from GitHub.

## 3. Your own edit: one line in `.claude\\settings.json`

The rulebook v0.3 now names the ranking report tool in rule 7. To make Claude Code's settings refuse it too, add this one entry to the `"deny"` list in `.claude\\settings.json` (it is your file; Claude does not edit it), for example after the line `"Bash(*.bat*)",`:

```
      "Bash(*Method_Rankings_Report*--game*)",
```

This exact pattern refuses any command that runs the report tool (it needs `--game`) and refuses none of the existing task commands T001 to T015 (checked). Then commit it on its own:

```bat
git add .claude/settings.json
git commit -m "settings: deny running the ranking report tool from Claude Code (rulebook v0.3 rule 7)"
git push
```
"""
(outdir / 'INSTALL_INSTRUCTIONS.md').write_bytes(instr.replace('\n', '\r\n').encode('ascii'))
print(PKG, len(NEWH), 'A', len(MODH), 'M; base', BASE)
