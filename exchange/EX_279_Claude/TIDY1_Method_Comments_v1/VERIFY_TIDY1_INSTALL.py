#!/usr/bin/env python3
"""Read-only installation verifier for the light tidy-up package (headers and comments of the existing method files; RAT-40 note 3).

Claude, 31 October 2026 (from the wave 2 package verifier; adds deleted paths). Standard library only; does not import project code, run tests, change
files or touch Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0).
Phases:
  pre        clean tree; HEAD descends from the base commit; src/ and tests/ in HEAD are exactly the
             base commit's; the 0 new paths are absent; the 37 modified files and the 0 files
             to be deleted still have their base bytes; guarded files unchanged in Git.
  post       after copying the overlay (and the git rm step, if any): exactly the 0 new paths
             appear, exactly the 37 modified files change and exactly the 0 deleted files are gone
             (staged deletions), all with the expected bytes (CRLF tolerated: the comparison is on
             LF-normalised bytes).
  committed  after the commit: clean tree; HEAD has one parent; the last commit added exactly the
             new paths, modified exactly the modified files and deleted exactly the deleted files,
             all with the expected Git blobs.
On any STOP in the committed phase, the verifier prints the identities needed to decide what
to do (HEAD, its parent, the last commit's paths, the working-tree status). Do NOT push and do
NOT reset: send Claude the whole output.
Usage: python VERIFY_TIDY1_INSTALL.py --repo . --phase pre|post|committed
"""
import argparse, hashlib, os, subprocess, sys
from pathlib import Path

BASE = '7be6b3aa8115d6a44edd9ab59180c1cdcfcda674'
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
NEW = {  # path: Git-content SHA-256 (LF)

}
MODIFIED = {  # path: (base Git-content SHA-256, new Git-content SHA-256), LF
    'src/methods/E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py': ('ac21616499291d07d2421199e0b46067c33fcca7baf539528fec9ff802bf4bab', '81a9f7c5153d5ff6e3c76eb0b00da4c7525b6ea81085320d7bb47fa0dcbec46c'),
    'src/methods/E_002/__init__.py': ('d1650f4375a47c932da0d3e4c03e6ce84c8b8fc7e2d3b5362d6da753b2f2a133', 'cf487d8d98a915ba74afa560b31a5d56e3142c3991e31baf1585c2861d53cff9'),
    'src/methods/E_002/core_v1.py': ('9c30cab5a19d61b8bd9b0e8f50ea7a43913c1428a0971a02c702dc9f658658e4', 'cd3efcea83b2e67a5a926d274b9ba6de439705c711700e54faca7ecb992193d1'),
    'src/methods/E_002/variants.py': ('ffb0b88774a8f0b4ef8a37d175dd5368d517286e7b70f756e874f52d1522f236', 'e2fcf2c158c8ac62b54eb7526ddf32dc6caf5101a4fd48048abf304234d56b4f'),
    'src/methods/E_003/__init__.py': ('b6ca2d3f76e05ef842cb7071bcd648936a6500ba80019c3ed3235a308b980a7d', '09315284200275994be4dfeaf0464ea2580319197899ffa5647919b97a0c877f'),
    'src/methods/E_003/core_v1.py': ('14927308f772e2c215dd72ee1f66e03c4579f8c355680f0cc3a7ab4df150b8db', 'c73ce9603075f2eda3547cb13ae58878dc9a971d43f4403209c9e20dcf43d880'),
    'src/methods/E_003/variants.py': ('bdd60d39e404e162060c2707c6ead227cd2f61e0ec99893ba86a9942b5e8224b', '4b8bfe571b0f5a0ca0720606c75bfd5fa3c526903a361509a60482076ae40bb0'),
    'src/methods/E_004/__init__.py': ('964d1e906244d2148875a9305eee034c302e8d2e53ab5600aefe907376134883', '5e22e881d6a455fb9e3eeec56f4858f623c2c138281f42d9b790bbacca6db497'),
    'src/methods/E_004/core_v1.py': ('bb8ff8c73ac0ed88c9aad30ae7fcf3a9a17f7794802bf329d9ca7069b4489d95', '8ab52a5a2969afd389bbfd9d0a7b8a6949ddbf4e5bb22fb55088268fb0987f04'),
    'src/methods/E_004/variants.py': ('4c5494ca3ec938934ff7fa695b4d86218068ba18bb7c278e409155bbb6c0165b', '033d48a51e11882ae2bc8cb7e130b652a37a39dfe33281a3acc86f700a07992a'),
    'src/methods/E_006/__init__.py': ('81766cd46cc6c2d7d6821f37b4651281beb3d3b8f652437be94c6e40db74c199', '2547995d1047e8961a7421369617d08e6d698dc3006fdfe26dc6cab4b7f6d20d'),
    'src/methods/E_006/beta_bernoulli.py': ('2c94d463f4020e7eb4f29949d12cb0cc8d0456f54dd5e1a89504c8f2d7fd976c', 'b78fd987f51a468295eb484873a38e5d35f65fe74d1a6ef2bd3fc6e337f7cab9'),
    'src/methods/E_006/core_v1.py': ('1752ecc51046ffcc49ce1d8b95986872f7422c8a50feafc221c057f3ab800b4b', '84479a28f0a087f976f915ff38890768bb8c2ec42ac8c5be37654807dfe18524'),
    'src/methods/E_007/__init__.py': ('1da98a22935f560337c44054f6720365f405d26e3256526b207753db644ca0ce', 'bdf334e4fcb73f5418348a2e3121460f676396fd4ec2af588790cc557e55b3c1'),
    'src/methods/E_007/core_v1.py': ('200d7621ee38ed4c4c8c1d58350233acc125363cb457b307efe0fade45029306', '763b5471ac46be05c4c302968401954694d8d5095995cabd93f7a3e109df8bf1'),
    'src/methods/E_007/variants.py': ('96f0a31cc54a57f5c1fb2e50961a7b740fd97ce1e916cd64c8cb8541cd15eaf9', 'c4564dc74e274736c93a982579a8a99a52544fec3b6d06e37ae5b97de2fcd050'),
    'src/methods/E_008/__init__.py': ('e9575cdbbd2d0705325867834b8d0928dbac7460565b3726507b3e20a6640c04', 'f63fe36e544c522ee7deb99c24e619e5330a38ea04a3445e287c93e4240dd203'),
    'src/methods/E_008/core_v1.py': ('414eaf8455f705a6f358476beaf0fd4577ad5a357172a8be79952b0b4978aa45', '5fb271d74bfac34c5bfec65deaa7ca81edb5eaf5e53acaa2705c70bad6d0f0fb'),
    'src/methods/E_008/variants.py': ('c231433c1071787ebaea1ddbdbe1ccb8f768cb8938acac9a50404599a05f2dbb', 'd4ef20ea3e09ff3d43962d019ebfe77fa197d0e4f136e06778e754c13a0a3bbd'),
    'src/methods/E_009/__init__.py': ('19b5becca8080f89b8def212847576e0a03a5cabbf781fa4b9f0f7c1cfcf7559', '007fd8173bb5ce3b68b5c90a8becd5917516e7f3b496f888afe9c94297082b1f'),
    'src/methods/E_009/core_v1.py': ('0c2ed81d06edd79cde325bbcecd1f73d1297a5829b74d11a1ff08f4c73779b3b', '244b28361764cec8accf1da589c2a215ab9a0370bceb518f06a4573a60896436'),
    'src/methods/E_009/variants.py': ('739a8a2f631f0e1da9bb39397dd225dea86893df95f6d1bb088c384e39ca43ea', '9474dba999b2881ffc2cb243a2d041ac9ccdfef28ffd9a7e8b0805a54d4ea4cf'),
    'src/methods/E_010/__init__.py': ('e8a831c4b2b8a75fa1b24a5cca5d83f41838d5cfa56f97f6a0a9c9b48deea12d', 'b881e22b50f7101c70cba34a77eb484753b988deb9a6fba5736667f14d108912'),
    'src/methods/E_010/core_v1.py': ('1507ecca77aa7171d0b3bde97425e2b1f5cd8ac55f52356ef1909f16b947cfe8', 'f1864a401968d5b5acad8ac10ac84cd2666b31a3aa9f922411d7bc2aec0c10f3'),
    'src/methods/E_010/variants.py': ('883213f497e641e80b477eb076272b70e46c0ebc9a11220320bd8c4feadb1a5f', '5f7f82b204bb04f7117f79f71511862e626707c43bc205f409ba1bebe956c832'),
    'src/methods/E_017/__init__.py': ('818d3bf627580aa5d029e77003857c8e31d2964df375fa7dc4354f9d1d733f54', '19d0824aabccc0bc45f716a4e3b3487ab89302b7d6a973f54d76a354643b00cd'),
    'src/methods/E_017/core_v1.py': ('7352da802d85b02187be35f978a37b1317a1702d06b66116629672118ce0b2ce', '8137a76f2fe2a466d63a76ddb96c20269d840d6ff7d308cf9e83b8f8efcecafe'),
    'src/methods/E_017/variants.py': ('d7198ed6fc4ba1d1909c8d2bbb0187945573f2ab25fda6e1707c915b15b798b6', 'c9b5fb379195505809c9f641843876e141663e2e282c22a7ededd5d544862c91'),
    'src/methods/E_018/__init__.py': ('74a177f7a6b6d8b367bdc73abb804b83f7852ea267a0a8bc66eaa65f6aede314', '31e374f338ae94d8cafb8b931c4aefa7062faff4228d9ac0d13f82326db81513'),
    'src/methods/E_018/core_v1.py': ('9ff76f5c40006a4e6e73582d9346c56fd036a82e26366013e73617d5fe44edf7', 'd1bc9ca67407900bf84e400d1eb9b0702eca7392775bd73bf9c5e35228caedfc'),
    'src/methods/E_018/variants.py': ('46f9e36602ead8e932ce8b3193370ed86fc22f1cd10a1f9d5033e234839a891c', 'd772ba0f60ec6d68403aa92f29377931b4a313f17d6f7809f2a1873c5f06d493'),
    'src/methods/E_019/__init__.py': ('580fd2c6263d849acc523617b5ef22516dbf480520c50cf51f932559ad177cfc', 'f651c2195ac9e67472247130d979202c669a5f24dac6562c6cdd70a93a4dff68'),
    'src/methods/E_019/core_v1.py': ('7d0a85ff24452c810e4e66fe61b49ab3e8b966daa880c0f3ae79b4297cceaf11', 'f5101702cc10290b115ad0c2bf5314eb664701881160f2af5c085b7e3f0258c3'),
    'src/methods/E_019/variants.py': ('a25cece3909d40f9c33aa2eb2490cc64a82fefdf424f600671aa12daf0be7e51', '9905d512a8fffbeaabd775f395b0f1a0b53f5f67703b2366e843d4641da9e438'),
    'src/methods/_shared/occurrence_counts_v1.py': ('76e39bf0aeb3273d0f5a9a41391d0ceac1cfd6a7b06955cbb80518e05f5cbde9', '8ce0d4c7fc65898a127bea7479b693d1cccc80b315f85ffb0430490e7b93517b'),
    'src/methods/_shared/polynomial_fits_v1.py': ('1d1c8d1078638607c0c0f584184834a95285f6d3e00b544a2a8a103e5d831615', 'bbd520afc347fa416ca96ff6c37f1b9cd1690e1c05181dff90ad8758ff60419d'),
    'src/methods/_shared/recurrence_gaps_v1.py': ('37b1be1d33bd7da5291fe36cf40272b1f12673f36a9fda8e20d7d6a26fdd1f25', 'e42741e0c3fe3b2510102aa912d2653ee0675bd1b66816f443e8396034aad888'),
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
    'src/methods/E_001/__init__.py': 'cd73a76370e0aa1934c1de0ec9b8a831bbea9556b9fcfddac103e6c5c28c8460',
    'src/methods/E_001/e1_common_reader_bridge.py': '2bfa693485cb2f417f4a0f24bd57a9b090c0f154bed8fa53299f4ed0cd9054db',
    'src/methods/E_001/e1_historical_appearance_frequency.py': '2c727d3b20584cd9a30c89863b6b51c72a1e0c373b48751e3da27d55f514f250',
    'src/methods/E_001/e1_standalone_contract.py': 'd9ef642c2949b1b2a10232d614ba1306365abaefe65338b5c0aa9e3d9f285e50',
    'src/methods/E_001/e1_training_view.py': 'e75e13729ffcdb5f14c4d7f762d8b31e590adbb1498142f9731eaf452394cad8',
    'src/methods/E_001/multigame_e1.py': 'd766416f3144ebd80dbcd11b538dcbdf97c93e83f8c4ad907baef24c4a10762b',
    'src/Powerball_Experiment_Coordinator.py': '6d202f5efd164c8e4a0eba97d435a0ec55787da87fcb2930af51309f573adcff',
    'src/results_master_v0_2.py': 'b71f4ffa14ea9f8b6c3e404c0ba46f6abe313ead3178bba553ed9b4ad5e2a43f',
    '.gitattributes': '5f824caa7fa974d37d6ad08766bbb4c59f73813be3d99bbc8be19d48d5fd708a',
    '.gitignore': '1548c367d7ebd60077d05b9cfbfb44e87f0524c265decae722e796968db61f72',
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
