#!/usr/bin/env python3
"""Read-only installation verifier for the build step 2 package, corrected after EX_283 (the research engine, in DEV; specification v0.6 sections 3 to 11).

Claude, 31 October 2026 (from the wave 2 package verifier; adds deleted paths). Standard library only; does not import project code, run tests, change
files or touch Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0).
Phases:
  pre        clean tree; HEAD descends from the base commit; src/ and tests/ in HEAD are exactly the
             base commit's; the 33 new paths are absent; the 2 modified files and the 0 files
             to be deleted still have their base bytes; guarded files unchanged in Git.
  post       after copying the overlay (and the git rm step, if any): exactly the 33 new paths
             appear, exactly the 2 modified files change and exactly the 0 deleted files are gone
             (staged deletions), all with the expected bytes (CRLF tolerated: the comparison is on
             LF-normalised bytes).
  committed  after the commit: clean tree; HEAD has one parent; the last commit added exactly the
             new paths, modified exactly the modified files and deleted exactly the deleted files,
             all with the expected Git blobs.
On any STOP in the committed phase, the verifier prints the identities needed to decide what
to do (HEAD, its parent, the last commit's paths, the working-tree status). Do NOT push and do
NOT reset: send Claude the whole output.
Usage: python VERIFY_STEP2_INSTALL.py --repo . --phase pre|post|committed
"""
import argparse, hashlib, os, subprocess, sys
from pathlib import Path

BASE = '465758de3909b2f537b03c313658918a9a440348'
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
NEW = {  # path: Git-content SHA-256 (LF)
    'ENVIRONMENT.example.ini': '565b7f9fdef8d236600569df5c47088bac81935e2aeef78ebfd5c8798c47fdd7',
    'Run_Research.bat': 'e4786da8f15c3cbc9e52e94e648753b6f81ebb0d04e149b3330a1e6c1d4dbdf3',
    'Withdraw_Variant.bat': '7cd9afe9a0a978a301de8d8ad9db252707ff3ca635493ab579a07a882281f0ab',
    'deploy/INFRA_MANIFEST.ini': 'eccdea0040a4fc96792d5192f495f5e8901ab51dc29bd911e0888ae0e3baaace',
    'src/research/__init__.py': 'fe93facf6d0371164ab374020ebd688aac2131ea020e65dfac2e76c6ceaddf87',
    'src/research/code_identity.py': '925adbb4f0b5c822d543ac77d0f8b9cf467c8037a7e1dfeee998fa75b85daea8',
    'src/research/derived_check.py': '129d83d2ac4a4d5e8e1ae6515205373d8cdb2766725644be1e967e20d4c02c41',
    'src/research/forecast_engine.py': '38183ae5083d5b4ebe442db3fc7dca2785fb2d8081ffd99bb934700781937978',
    'src/research/game_state.py': 'b1f9cbf5f783fc05257a9945016512c73a9a5137f46bbf10d7fdadce35a3ba8b',
    'src/research/job_lock.py': '2a807b2e6bc582e5f60adbb96e7a0534bf1417033cfe195d62a8269bbf0b709a',
    'src/research/method_api.py': '6171890f10340b0bfa55d9c255ff245559e7671afd38881a632eee073087e817',
    'src/research/ov1_ledger.py': '51b2d3147f35863769d16dec690563692172ea62cefec85bb606c7b4404f8e50',
    'src/research/ov1_numeric.py': '2858075e37d2fed447388c770aafe2de9c6d296cd84808078f4cff8cba8d8234',
    'src/research/reader.py': '6122668783bfddfec46aba8a0eef29c11369131199b3dcbcd568d3b51bf92544',
    'src/research/readout.py': 'c9ccbee727aedb36189a33c8dda5366385ffedb985d26b246997c6aaedd88882',
    'src/research/reports.py': '1abf67454ffbbaefe130b9b137ca3d8e47006159d46e16f52e2e235c7c9b222e',
    'src/research/research_job.py': '6d0372642481a17ac4a26db4f78d455aa9bc864bd0880937030b00f28bb150a3',
    'src/research/results_step.py': 'df578d800dc79c63c902b1e0ccae9cad1e5be31c00c9dbd5c2ae791bbce3a6fe',
    'src/research/scoring.py': '0015bd358b6871ef3c1ee49809712d3d196e81bd93b5ebf70104d25831db1ce4',
    'src/research/settings.py': 'd12bb503bdb9333b1f00a54c89615274abb25465d0f7f95881a2e0baa00aa624',
    'src/research/status_file.py': '8cf0a4623b1792df08217102070c16dbc0013ee32b043001c215eaabf8f79f6d',
    'src/research/variant_folders.py': '9d2c5c1c8f2c38d0fcfcf347807e4b16e9343b2815073dd090b5ee3fe12529c9',
    'src/research/variant_lists.py': '6bbc7b6bb54cd34d037c7107374f61deb629e040ffc578cc2680b384c07e69e3',
    'src/research/withdraw.py': '87250e1790e7041dd236d940007e4dd425797ff2771ae23a19a870be06192b44',
    'src/research_command.py': '67e2edd38a27933768c3a034cc8612c27f8da64730f4d9f2915b10fbcea627a5',
    'tests/research_fixtures.py': '7ceffe94511d9116221c077afbc12cac105beafd91f01294856cc0ddc048f839',
    'tests/test_research_forecasts.py': 'a27716730be470f948a64d4597ed9abbe32e3789ad33d9ce2c2371561a6bd50a',
    'tests/test_research_identity.py': '0886ebf6bd2adf267156a35e392cb23227d1c8cac643b0ce75efb287f041608b',
    'tests/test_research_job.py': '440470a45d899fa72ba13c6d7d44364d547fb11742e7aa3a99c9a23f02af87fa',
    'tests/test_research_manifest.py': '12a9d37ae1f9b7b2120a3c157f42ce6a70b7cf2d0833ac3e5ce00e94c6947905',
    'tests/test_research_ov1_and_checks.py': 'b0bffa95468b0b6e0f254e7d5167ba26780890ab2710f05199cffff425249f20',
    'tests/test_research_ov1_numeric.py': 'ed5d2c1fb95dd4c698e50f831c372c602afe35f18df49da29088840051fd2bf5',
    'tests/test_research_records.py': '33a558a5795b83e2a2e08c6115e4e9cf30b18dfab6ec19d5f294723a123bae1b',
}
MODIFIED = {  # path: (base Git-content SHA-256, new Git-content SHA-256), LF
    '.gitignore': ('1548c367d7ebd60077d05b9cfbfb44e87f0524c265decae722e796968db61f72', '49d86c801ff907f73bb3d61249c842f1c230072afaeff1e7689ac2ace24c7da0'),
    'tests/test_mhupa_master_versions.py': ('c26549cd59c6bf795afd98a3f481d237d2eaf0912f6c2970be446df11ad548c3', '7198a7ad6658c8626e7722dafbdb4748f988116ab0c4df819af79da7d165f273'),
}
DELETED = {  # path: base Git-content SHA-256 (LF)

}
GUARDED = {  # must stay byte-identical in Git (hashes of the Git blobs at the base commit)
    'source_data/POWERBALL_results_master.csv': 'e4f2feb8b18fc2dbe389583a189fa26127a648f4da940dd76219ee282170f3e0',
    'source_data/POWERBALL_results_master_ledger.csv': '23f3f8a78b8cdaaf8f10d56c1684581e54be563f263d835d90cee966a0e446dd',
    'source_data/POWERBALL_results_master_init_verification.json': 'bc3cf72c42fd832193f8e043df63242091259abd6dbcd067152d902c2b132547',
    'source_data/HOLDOUT_OPENED_POWERBALL.json': 'e6cd70a61cefc9aeb7913b90799e1c52489803eff280bb5c3723ea5c8b2ccd57',
    'source_data/OZLOTTO_results_master.csv': '63e3349333f8aa0485b7b067abe70249e39de81c6d02cda1a5710cf1041a4e9e',
    'source_data/OZLOTTO_results_master_ledger.csv': '78ab9fdef29f8faafb10bb3d1fd2197747195b95b46640e73ff031797761a3c6',
    'source_data/OZLOTTO_results_master_init_verification.json': '3a8decb43dbf52a5d1e2d3d621162541e327f90bcf08e066da4faa3ed41836a8',
    'source_data/HOLDOUT_OPENED_OZLOTTO.json': '0418aebba259f5b94c06f938de0501c4ad97fabb9b0d0c083e7d5956904eb3db',
    'src/methods/_common/__init__.py': 'e834c2d46453f40aeadc61eaa8666d05b366f782fbdfc12430d62aaf61d8750d',
    'src/methods/_common/canonical_encoding.py': '2096d8adb40737373169aea6c5d94147daa2b16ae6c961bbfcc6063e333efcac',
    'src/methods/_common/contract_vocab.py': 'f0e04f4720ba98ada37991d15796020dc13f56ed5cd83c877680c6e448df91a3',
    'src/methods/_common/game_draws_reader.py': '1de081f9c0832b3c21646383d4563572791e52ecffc987a470b818920b8e045c',
    'src/methods/_common/game_profiles.py': 'd49e83b5f91f5a0b299c6e08ae48c598d03b969a5dec70e05932daa3e4827a9b',
    'src/methods/_common/contract_forecast.py': '9c1498207a3b401406f27b18948b62ea0109285eb0afd4ed103fc54a5df1d16d',
    'src/methods/_common/contract_records.py': '40f058208cd3dd7062ebee7fb058a2acdbe66326a6925fff3344f1c2a5e0bce9',
    'src/methods/_common/contract_task.py': 'e68094199281c0722f3963514edb4f32c669d5342aa4d50ae88b51dceb0b36eb',
    'src/methods/_common/contract_runner.py': 'f86c81306a35bef4ea3bb3fdd357ff939d16b245f6f34ca63a2bacb49476a113',
    'src/methods/_common/contract_dispatch.py': '3c7bb22c7de8a76dae47f199393f87d93b34adc230bcf9f1a27311b3b819de4f',
    'src/methods/_common/contract_registry.py': '00082aad1754edbf2380c2caa144b0c79a12e2b6f26eb806d85903f177f11064',
    'src/methods/_common/walk_forward.py': 'a3f9cfa3800aa99a0c9fcf2609cee2360c6b87c375ce8411bad47d2820fd9329',
    'src/methods/_common/master_versions.py': '57ba431edc56b350deadb60919310615c1598e1f241644890ab823b864f3e7ab',
    'src/methods/_common/closure.py': 'e8d5114a486927292e227f599dd57de8149ff69de708dd68124759ea0f7951fc',
    'src/methods/_common/method_table.py': 'ca63c367b5e9ebfdd78eb8477410aafe9f7afa0ea66a8f5f423b9eb4ba79c0eb',
    'src/evaluation/__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'src/evaluation/divisions.py': 'bd6201c310e3b9eea085062d5b84627f9d8b30fc593c06a0d82e2743a288deb2',
    'src/Powerball_Experiment_Coordinator.py': '6d202f5efd164c8e4a0eba97d435a0ec55787da87fcb2930af51309f573adcff',
    'src/results_master_v0_2.py': 'b71f4ffa14ea9f8b6c3e404c0ba46f6abe313ead3178bba553ed9b4ad5e2a43f',
    '.gitattributes': '5f824caa7fa974d37d6ad08766bbb4c59f73813be3d99bbc8be19d48d5fd708a',
}
HERE = Path(__file__).resolve().parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(b):
    return b.replace(b'\r\n', b'\n')


def run(repo, *args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=GIT_ENV)


def git(repo, *args):
    r = run(repo, *args)
    if r.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)} failed: {r.stderr.decode(errors="replace")[:300]}')
    return r.stdout


def need(cond, msg):
    if not cond:
        raise RuntimeError('FAIL: ' + msg)


def identities(repo):
    """Read-only facts for deciding after a committed-phase STOP."""
    print('--- identities for Claude (read-only) ---', file=sys.stderr)
    for label, args in [('HEAD and parents', ['log', '-1', '--format=%H %P %s', 'HEAD']),
                        ('last 3 commits', ['log', '--oneline', '-3']),
                        ('last commit paths', ['diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD']),
                        ('upstream', ['rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}']),
                        ('commits not yet pushed', ['log', '--oneline', '@{u}..HEAD']),
                        ('working tree and index', ['status', '--porcelain=v1', '--untracked-files=all'])]:
        r = run(repo, *args)
        out = (r.stdout if r.returncode == 0 else r.stderr).decode(errors='replace').rstrip()
        print(f'[{label}]\n{out[:1500] or "(none)"}', file=sys.stderr)
    print('--- Do NOT push. Do NOT reset. Send Claude this whole output. ---', file=sys.stderr)


def main(a):
    repo = a.repo.resolve()
    need((repo / '.git').exists(), f'not a Git checkout: {repo}')
    for p, h in [*NEW.items(), *((p, n) for p, (_o, n) in MODIFIED.items())]:  # the package must be intact
        need(sha(norm((HERE / 'repo_overlay' / p).read_bytes())) == h, f'package file damaged: {p}')
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    anc = run(repo, 'merge-base', '--is-ancestor', BASE, 'HEAD')
    need(anc.returncode == 0, f'HEAD {head} does not descend from base {BASE}; STOP')
    print('HEAD:', head, '(descends from base', BASE[:7] + ')')
    for p, h in GUARDED.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'guarded file changed in Git: {p}')
    print(f'{len(GUARDED)} guarded files unchanged in Git HEAD')
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode(errors='replace')

    if a.phase == 'pre':
        need(not status.strip(), 'working tree or index not clean:\n' + status[:600])
        diff = git(repo, 'diff', '--name-only', BASE, 'HEAD', '--', 'src', 'tests').decode().split()
        need(not diff, 'src/ or tests/ changed since the base commit: ' + ', '.join(diff[:20]))
        for p in NEW:
            need(not (repo / p).exists(), f'new path already exists: {p}; STOP')
        for p, (old, _new) in MODIFIED.items():
            need(sha(git(repo, 'show', f'HEAD:{p}')) == old, f'file to be replaced is not its base version in Git: {p}')
            need(sha(norm((repo / p).read_bytes())) == old, f'file to be replaced differs on disk: {p}')
        for p, old in DELETED.items():
            need(sha(git(repo, 'show', f'HEAD:{p}')) == old, f'file to be deleted is not its base version in Git: {p}')
            need(sha(norm((repo / p).read_bytes())) == old, f'file to be deleted differs on disk: {p}')
        print(f'PRE PASS: clean tree; {len(NEW)} new paths absent; {len(MODIFIED)} files to replace and {len(DELETED)} to delete '
              'at their base version. Nothing was changed.')
        return

    if a.phase == 'post':
        lines = status.splitlines()
        new = {ln[3:].strip().strip('"').replace('\\', '/') for ln in lines if ln.startswith('?? ')}
        mod = {ln[3:].strip().strip('"').replace('\\', '/') for ln in lines if ln.startswith(' M ')}
        dele = {ln[3:].strip().strip('"').replace('\\', '/') for ln in lines if ln.startswith('D  ')}
        need(len(new) + len(mod) + len(dele) == len(lines),
             'changes other than new files, modified files and staged deletions:\n' + status[:600])
        need(dele == set(DELETED), 'unexpected staged deletions: ' + ', '.join(sorted(dele ^ set(DELETED))))
        for p in DELETED:
            need(not (repo / p).exists(), f'deleted path still on disk: {p}')
        need(new == set(NEW), 'unexpected new paths: ' + ', '.join(sorted(new ^ set(NEW))))
        need(mod == set(MODIFIED), 'unexpected modified paths: ' + ', '.join(sorted(mod ^ set(MODIFIED))))
        for p, h in [*NEW.items(), *((p, n) for p, (_o, n) in MODIFIED.items())]:
            f = repo / p
            need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
            need(sha(norm(f.read_bytes())) == h, f'wrong bytes: {p}')
        print(f'POST PASS: exactly the {len(NEW)} expected new paths, {len(MODIFIED)} modified files and '
              f'{len(DELETED)} staged deletions, all with the expected bytes.')
        return

    need(not status.strip(), 'working tree or index not clean after commit:\n' + status[:600])
    parents = git(repo, 'log', '-1', '--format=%P', 'HEAD').decode().split()
    need(len(parents) == 1, f'HEAD has {len(parents)} parents, expected 1')
    diff = git(repo, 'diff', '--name-only', BASE, 'HEAD~1', '--', 'src', 'tests').decode().split()
    need(not diff, "the commit's parent has src/ or tests/ changes since the base: " + ', '.join(diff[:20]))
    for p, h in [*NEW.items(), *((p, n) for p, (_o, n) in MODIFIED.items())]:
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'wrong Git blob in HEAD: {p}')
    for p, (old, _n) in MODIFIED.items():
        need(sha(git(repo, 'show', f'HEAD~1:{p}')) == old, f'parent does not hold the base version: {p}')
    for p, old in DELETED.items():
        need(sha(git(repo, 'show', f'HEAD~1:{p}')) == old, f'parent does not hold the deleted file: {p}')
        need(run(repo, 'cat-file', '-e', f'HEAD:{p}').returncode != 0, f'deleted file still in HEAD: {p}')
    names = git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD').decode().splitlines()
    got = {ln.split('\t', 1)[1]: ln.split('\t', 1)[0] for ln in names if ln}
    want = {**{p: 'A' for p in NEW}, **{p: 'M' for p in MODIFIED}, **{p: 'D' for p in DELETED}}
    need(got == want, 'the last commit did not change exactly the expected paths; differences (path, status): ' +
         repr(sorted(set(got.items()) ^ set(want.items()))))
    print(f'COMMITTED PASS: the last commit ({head[:7]}) added exactly {len(NEW)} files, modified '
          f'{len(MODIFIED)} and deleted {len(DELETED)}; all Git blobs match.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--phase', required=True, choices=['pre', 'post', 'committed'])
    args = ap.parse_args()
    try:
        main(args)
        print('Read-only: no project code imported, nothing run, nothing changed.')
    except Exception as exc:
        print('VERIFICATION STOP:', exc, file=sys.stderr)
        if args.phase == 'committed':
            try:
                identities(args.repo.resolve())
            except Exception as exc2:
                print('(could not list identities:', exc2, ')', file=sys.stderr)
        sys.exit(2)
