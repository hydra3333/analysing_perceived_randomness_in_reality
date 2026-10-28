#!/usr/bin/env python3
"""Read-only installation verifier for NAMES-1 (one-off rename to stable file names; register v0.8).

Claude, 28 October 2026. Standard library only; does not import project code, run tests, change
files or touch Git state (every Git call uses --no-optional-locks and GIT_OPTIONAL_LOCKS=0). It never
reads source_data/, results/ or transitory_data/.
Phases:
  pre        clean tree; HEAD descends from the base commit and has register v0.7 (DOC-2 installed);
             every file NAMES-1 touches is at its base bytes in Git; every new path is absent;
             guarded files unchanged.
  post       after RENAME_FILES.cmd and copying the overlay: the index holds exactly the 27 renames;
             the working tree differs from the index in exactly the edited files; exactly the new
             files are untracked; every file has its expected bytes (CRLF tolerated for text);
             no old path remains; no live file names an old module (N1-T01).
  committed  after the commit: clean tree; the last commit deleted the 27 old paths, added the 27
             new ones and the new files, and modified exactly the 3 edited-in-place files, all with
             the expected Git blobs; each pure rename's blob equals its predecessor's.
Usage: python VERIFY_NAMES1_INSTALL.py --repo . --phase pre|post|committed
"""
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path

BASE = 'de2bd530bb548dc74b78daaf94a7d061b1ec2567'
REG_V07 = ('doc/RATIFICATION_REGISTER_v0_7.md', 'f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015')
DATA = json.loads(r'''{
 "base_sha": {
  "src/Powerball_Experiment_Coordinator.py": "bc8380b5f20a704c0f47d5f76eeb86156237142b5639e5b9770b8314db3bb822",
  "src/coordinator_private/multigame_coordinator_exit_receipt_v2.py": "d313ff16f29c8182de72428becc849eb7045d00d8afe1d3b098c24cddebe5f7a",
  "src/coordinator_private/multigame_launch_spec_v1.py": "f9bac5cf3689ce2dc6879155a1e26dcb028421cc2196cbc1ce18afaa0b8e8162",
  "src/coordinator_private/multigame_windows_lifecycle_v1.py": "e9e2c4379905670b44f06ce9774cf831e982446e4634caabc7562c2a9164708d",
  "src/methods/E_001_Historical_Appearance_Frequency.py": "9ce866e44c7e8e13a3c245a7fa800d1c2a8d6c6b7ca311e4c9f8ec0fbe309a45",
  "src/methods/POC_MultiGame_Synthetic_Worker.py": "c39a49dea6d3dba3b0e005abdfd05fb22ec3e38222f2db38e4cdd7303bd13489",
  "src/methods/_common/e1_common_reader_bridge_v1.py": "66605ac0d72dd34ab4d223d5ae4a0fa78ddef65edf973e63d19bd613977977e2",
  "src/methods/_common/e1_historical_appearance_frequency_v0_3.py": "794320b0f330acf132f5c1ad78c732fe47fb1e561225df6974313adc68ccb0ef",
  "src/methods/_common/e1_standalone_contract_v0_1.py": "d9ef642c2949b1b2a10232d614ba1306365abaefe65338b5c0aa9e3d9f285e50",
  "src/methods/_common/e1_training_view_v0_1.py": "f51b2a76a029f7d690cf07abdb1ea703830fc1462f69c53849d4e614938f5838",
  "src/methods/_common/game_draws_reader_v1.py": "e06e0cca7edc298aadf5298ae860d6093467f6460fcbf9839928b1e4fdb342b5",
  "src/methods/_common/game_profiles_v1.py": "d49e83b5f91f5a0b299c6e08ae48c598d03b969a5dec70e05932daa3e4827a9b",
  "src/methods/_common/multigame_ancestry_release_v1.py": "ca8e47f99157b09d10bf55abd89fa2c1cab94a65e3f536a4d044f01218ac248e",
  "src/methods/_common/multigame_console_protocol_v1.py": "fffcfe22b9d2ee123617e24b467f14907cdc832de7fce7dfa7d1be720b7ec69d",
  "src/methods/_common/multigame_coordinated_manifest_v1.py": "7218000b3e4b0759cdc2b87171ea7a9046638a6bc615c825e50b854607694860",
  "src/methods/_common/multigame_e1_v1.py": "a4d22baa267dde5fbe32dca28f2caab0301bc3e1f7df74e4b7c53cf9ce6d7268",
  "src/methods/_common/multigame_method_registry_v1.py": "cf979fa592995aa37ad9ad38c314c4648085d14b71adccecfd0eae7c18d640df",
  "src/methods/_common/multigame_result_registry_v1.py": "8fa601082c5472d2d8837f62763b9b12597d63929e7dfdf20ceba87eefa58406",
  "src/methods/_common/multigame_standalone_contract_v1.py": "a83fde8becd364c3dc4960722585a828c5d76aaeaa99a1efc3f28a1cbc12bb04",
  "src/methods/_common/multigame_synthetic_scorer_v1.py": "4ca49b782f11ad19a1d3def1d90e066bedbc62c1b56f70e9afc6077cbde2936c",
  "src/methods/_common/multigame_worker_launch_handshake_v1.py": "603903be4ec860e7e9cecfbcc643b361f310ce2e448a72faa979d17d1e447763",
  "tests/test_multigame_console_and_synthetic_scorer_v0_4.py": "1e6b7d17b42bca6f6b0075f4a68d55339440ab760cfd2d7cf1f1230af3bb9f55",
  "tests/test_multigame_exit_receipt_v0_8.py": "e04f9336b755566549bfb84f2caba1d4531b1b2b3383ede53678b38c19e9becf",
  "tests/test_multigame_launch_and_manifest_v0_8.py": "339d4cd2a9e46ad796374e94aebb441c2036e09d2abec09bb7ef3e4f890b013a",
  "tests/test_multigame_science_allowlist_v0_8.py": "b0570b2c3faae962960c281b6e6882331b06fc4ec1e2aab5c1b7aed268ddfaca",
  "tests/test_multigame_v011_reader_contracts.py": "a0460c49ac5d193871dd35f02ba532271e9c943185b8a9b759f0ee5b4a0da2dc",
  "tests/test_multigame_v011_static_and_timing.py": "8e606e965f748cb7b48f3ba8f76b29dfecf71552f59c4b3292cc76f42ab43696",
  "tests/test_multigame_windows_lifecycle_review_v0_9.py": "29e4b0f8e013d6d579c566355a79e6dd8d057c6c2dbac1c524a07661df86f288",
  "tests/test_p2_r1_t05_hardening_v1.py": "c3341ce2fa7409335f6232c0f65b2d9b5a1b2d03fde6ee863e4fe4e30c8b9e58",
  "tests/test_p3_e1_standalone_v0_1.py": "8e64030808aadaf27d1f07b16bbaa0ada26ce76640ab54645c200539ee8245b1"
 },
 "guarded": {
  "Run_Coordinator.bat": "6ccb23302c897747432d84d1a1f4ed6fd7b2cf99faa8298ec4f3b5d82841bc70",
  "Run_Experiment.bat": "dfd324d645cbbe5d528883f7a0309d5f5f3cbea47c4a49ddffaf6b0bdc7f0c5d",
  "Run_Results_Updater.bat": "c01ac19ed4a04ad133f28f4873dfe8c161bac811237b2176e70717f63bb80230",
  "activate_venv.bat": "906a3370d4cbf0f66355d7b5b5219b90b6d3b4fdd38af9228e1765aa9cd12587",
  "deactivate_venv.bat": "697115ed8ac7e09109e797066369007e2e876c71529231df1c405a6637e5da96",
  "doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r3.md": "a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1",
  "doc/HANDOVER/Claude_Primary_Handover_H1_v1r2.md": "55543ba522a4085fc4f2476d421a4940171bcd4c183a1fab5a691d291605eac0",
  "doc/Predictive_Randomness_E2_Readiness_Method_Contract_Specification_v0_3r3.md": "0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954",
  "doc/RATIFICATION_REGISTER_v0_7.md": "f9be980c2482c22cb2da6f7af34020f8cfd8e32302694c975c955ec407fcc015",
  "install_upgrade_dependencies_into_venv.bat": "b7d659b87fe0e7be226cce3583a3b6d59bf35de11bbc0285f5b54299996f9a54",
  "tests/fixtures/coordinator_v0_6_baseline/Powerball_Experiment_Coordinator_v0_6.py.txt": "2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b",
  "tests/p3_e1_synthetic_v0_3.json": "ea8956c490c71550505ec38d1b5f705ae47ea444459c63a987cea3fa919f60dd"
 },
 "in_place": [
  "src/Powerball_Experiment_Coordinator.py",
  "src/methods/E_001_Historical_Appearance_Frequency.py",
  "src/methods/POC_MultiGame_Synthetic_Worker.py"
 ],
 "new_files": [
  "doc/Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md",
  "doc/RATIFICATION_REGISTER_v0_8.md",
  "review/Independent_ChatGPT_Focused_Recheck_NAMES1_Spec_v0_2.md",
  "review/Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md",
  "review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt",
  "review/NAMES1_Code_Install_v1/ast_check_output.txt",
  "review/NAMES1_Code_Install_v1/names1_allowlist.tsv",
  "review/NAMES1_Code_Install_v1/negative_checks_output.txt",
  "review/NAMES1_Code_Install_v1/suite_per_module_linux.txt",
  "review/NAMES1_Code_Install_v1/t02_check_output.txt",
  "review/NAMES1_Spec_Recheck_v0_2.zip",
  "review/NAMES1_Spec_Review_v0_1.zip",
  "review/Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md"
 ],
 "new_sha": {
  "doc/Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md": "07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a",
  "doc/RATIFICATION_REGISTER_v0_8.md": "094ce38ea1052395ff21f57e7091c670303b46f65f51726b5ffd37ee979f1a9c",
  "review/Independent_ChatGPT_Focused_Recheck_NAMES1_Spec_v0_2.md": "020fe9f73ba15f5260812d06701713d7b439880afb4197ace3488c4d63849f45",
  "review/Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md": "30d24ed02ff4ba3b0c84c760f306c8bfd02ddd2717db61013e60f855e3ace85a",
  "review/NAMES1_Code_Install_v1/INSTALL_MANIFEST_SHA256.txt": "0b4e34b869b0f9fa9984767bb15ad7a1add84ada4e8f842501c8cf9127edadb5",
  "review/NAMES1_Code_Install_v1/ast_check_output.txt": "e85415cdf57ebb563bab1cb7528ac38cc922dbe1bbe29a213782d762d64a98db",
  "review/NAMES1_Code_Install_v1/names1_allowlist.tsv": "2074f152b52f0adadd581546ef704341962cffe0c2d00a4d59d8301e1a3c315f",
  "review/NAMES1_Code_Install_v1/negative_checks_output.txt": "362f43584f6b2dcf908278c4d80a2da3237107a627a41cc81ac5d70c721ee1c6",
  "review/NAMES1_Code_Install_v1/suite_per_module_linux.txt": "f7c72673a8d157aa7d01f4b0eb4a1c24fb5234ade870a460fd2bab3ff843e844",
  "review/NAMES1_Code_Install_v1/t02_check_output.txt": "6cd932778c7e21aeace7103d0acb222d8d2957ae7d30d90b6140d9a702aa9067",
  "review/NAMES1_Spec_Recheck_v0_2.zip": "fddf24f147406038653673e49350a7737b97c518849e46fc8c7b178d06b442a6",
  "review/NAMES1_Spec_Review_v0_1.zip": "6aab40a1407c4b438ce05b7132ee2d3e183a6feb711d6f5877d9becc3246325f",
  "review/Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md": "244aac86c72ff696e1d658023de8ab14035f2bb732585467bd140830e461cb59",
  "src/Powerball_Experiment_Coordinator.py": "6d202f5efd164c8e4a0eba97d435a0ec55787da87fcb2930af51309f573adcff",
  "src/coordinator_private/multigame_coordinator_exit_receipt.py": "ba6998be867b0a286aa4097b22cfa66050af94af41558b3a91c9a65b84e110af",
  "src/coordinator_private/multigame_launch_spec.py": "2f4717f4e6be2d2084a01205c24a9ab048b55239da334b4b79181616ce675507",
  "src/coordinator_private/multigame_windows_lifecycle.py": "885fe1e67a5b91ddf5d4cf79f15e3a8ad27c62b087ffbd075ee160c811cab03b",
  "src/methods/E_001_Historical_Appearance_Frequency.py": "0874ec012ecf2be3b7c40d8adf3bf22736202fbd209e04878de846c035b0259e",
  "src/methods/POC_MultiGame_Synthetic_Worker.py": "3078e9c25c5d3665a785883e72ea17dcce14c77e8d031efbc670d844150f0c17",
  "src/methods/_common/e1_common_reader_bridge.py": "0504c0c297fd494c4f42f18e3eadf77ec99f7c2bc4b3db714c0f3a606dbe5e0c",
  "src/methods/_common/e1_training_view.py": "e9708acfb6918885de7e8b545bece7cb87f6883ecc65253b8db11028da943565",
  "src/methods/_common/game_draws_reader.py": "9ed28e3db821272cbeb47725a587eaefb3d38a13f20403a549b82cd0cdd973e3",
  "src/methods/_common/multigame_ancestry_release.py": "d9ee41180f32362de5f7f2ecc5aa8da3f88674a65fc77b26f645c5b1c9bd7dd0",
  "src/methods/_common/multigame_console_protocol.py": "4a63d70474082e9c71685e99871aa50ee106904bcbea6edd253a0624f4b08406",
  "src/methods/_common/multigame_coordinated_manifest.py": "70dd2954ffd7dfe38204c6dbe70a0ee275f8a4cb86d2c48d77da6422f6cb4cee",
  "src/methods/_common/multigame_e1.py": "4762c65e5a5715942d0ee4cde7e352be9ee226a17ebc5b1a44c6c92f6d39c536",
  "src/methods/_common/multigame_method_registry.py": "78693c06d109f584b3ce987baaf633028fb8d6eb036f4068006173754b46aacd",
  "src/methods/_common/multigame_result_registry.py": "768e719f17e61a1b246668fcd9050a6e218be43ad89b73bcc1d9d779100eb34b",
  "src/methods/_common/multigame_standalone_contract.py": "d27fc6b15948e0701ff4c9e7020274e29d2c9423a903f5dc1c8e75139ce20b95",
  "src/methods/_common/multigame_synthetic_scorer.py": "ff33caea1d2f0ac4ca28e355f1ee983db8d4c80e029229038b66140247595992",
  "src/methods/_common/multigame_worker_launch_handshake.py": "8397c5140c2f9f8e3437df88b8a3e845703db54933d30fe3658f8e0e2e3e8e63",
  "tests/test_e1_standalone.py": "e1eb575744da41a0ace48e78f24203ee2ba0712bfd6f338bb3601635c49f43f1",
  "tests/test_multigame_console_and_synthetic_scorer.py": "e6327ed6d3b779f5cd6503229062ea31a56a826f8b2531236cc103a1a3b512f8",
  "tests/test_multigame_exit_receipt.py": "e6422db86185578189b9085a971adf6c541f436e6134f0bba68244a684eb14fa",
  "tests/test_multigame_launch_and_manifest.py": "239c5b81a02eb357d1dd98866ab9eff04755d94102e15639ad011a2c489abda4",
  "tests/test_multigame_reader_contracts.py": "b4252eaead12131b98d4fd7fc855584adc14d6a0e387f21fe9c094ce367212bf",
  "tests/test_multigame_science_allowlist.py": "f70f701b2601ff4c542cc2364763e3b32bbbc013f189161c9f24e0615783fdc8",
  "tests/test_multigame_static_and_timing.py": "bc1f31b87085acfd0206ab7a28cecdc7d017c33227e98a109cb1b8c6e7cf3e79",
  "tests/test_multigame_windows_lifecycle_review.py": "82f232daed90a9f9638cb6b7dcd62b6b0cc5286198ce94aaa8ded559bd3033ce",
  "tests/test_t05_hardening.py": "b435f57cdaf40092baa72fece56cc528e4263b8cf9be2286f3ec97cc50e2b8ad"
 },
 "old_names": [
  "e1_common_reader_bridge_v1",
  "e1_historical_appearance_frequency_v0_3",
  "e1_standalone_contract_v0_1",
  "e1_training_view_v0_1",
  "game_draws_reader_v1",
  "game_profiles_v1",
  "multigame_ancestry_release_v1",
  "multigame_console_protocol_v1",
  "multigame_coordinated_manifest_v1",
  "multigame_coordinator_exit_receipt_v2",
  "multigame_e1_v1",
  "multigame_launch_spec_v1",
  "multigame_method_registry_v1",
  "multigame_result_registry_v1",
  "multigame_standalone_contract_v1",
  "multigame_synthetic_scorer_v1",
  "multigame_windows_lifecycle_v1",
  "multigame_worker_launch_handshake_v1",
  "test_multigame_console_and_synthetic_scorer_v0_4",
  "test_multigame_exit_receipt_v0_8",
  "test_multigame_launch_and_manifest_v0_8",
  "test_multigame_science_allowlist_v0_8",
  "test_multigame_v011_reader_contracts",
  "test_multigame_v011_static_and_timing",
  "test_multigame_windows_lifecycle_review_v0_9",
  "test_p2_r1_t05_hardening_v1",
  "test_p3_e1_standalone_v0_1"
 ],
 "renames": {
  "src/coordinator_private/multigame_coordinator_exit_receipt_v2.py": "src/coordinator_private/multigame_coordinator_exit_receipt.py",
  "src/coordinator_private/multigame_launch_spec_v1.py": "src/coordinator_private/multigame_launch_spec.py",
  "src/coordinator_private/multigame_windows_lifecycle_v1.py": "src/coordinator_private/multigame_windows_lifecycle.py",
  "src/methods/_common/e1_common_reader_bridge_v1.py": "src/methods/_common/e1_common_reader_bridge.py",
  "src/methods/_common/e1_historical_appearance_frequency_v0_3.py": "src/methods/_common/e1_historical_appearance_frequency.py",
  "src/methods/_common/e1_standalone_contract_v0_1.py": "src/methods/_common/e1_standalone_contract.py",
  "src/methods/_common/e1_training_view_v0_1.py": "src/methods/_common/e1_training_view.py",
  "src/methods/_common/game_draws_reader_v1.py": "src/methods/_common/game_draws_reader.py",
  "src/methods/_common/game_profiles_v1.py": "src/methods/_common/game_profiles.py",
  "src/methods/_common/multigame_ancestry_release_v1.py": "src/methods/_common/multigame_ancestry_release.py",
  "src/methods/_common/multigame_console_protocol_v1.py": "src/methods/_common/multigame_console_protocol.py",
  "src/methods/_common/multigame_coordinated_manifest_v1.py": "src/methods/_common/multigame_coordinated_manifest.py",
  "src/methods/_common/multigame_e1_v1.py": "src/methods/_common/multigame_e1.py",
  "src/methods/_common/multigame_method_registry_v1.py": "src/methods/_common/multigame_method_registry.py",
  "src/methods/_common/multigame_result_registry_v1.py": "src/methods/_common/multigame_result_registry.py",
  "src/methods/_common/multigame_standalone_contract_v1.py": "src/methods/_common/multigame_standalone_contract.py",
  "src/methods/_common/multigame_synthetic_scorer_v1.py": "src/methods/_common/multigame_synthetic_scorer.py",
  "src/methods/_common/multigame_worker_launch_handshake_v1.py": "src/methods/_common/multigame_worker_launch_handshake.py",
  "tests/test_multigame_console_and_synthetic_scorer_v0_4.py": "tests/test_multigame_console_and_synthetic_scorer.py",
  "tests/test_multigame_exit_receipt_v0_8.py": "tests/test_multigame_exit_receipt.py",
  "tests/test_multigame_launch_and_manifest_v0_8.py": "tests/test_multigame_launch_and_manifest.py",
  "tests/test_multigame_science_allowlist_v0_8.py": "tests/test_multigame_science_allowlist.py",
  "tests/test_multigame_v011_reader_contracts.py": "tests/test_multigame_reader_contracts.py",
  "tests/test_multigame_v011_static_and_timing.py": "tests/test_multigame_static_and_timing.py",
  "tests/test_multigame_windows_lifecycle_review_v0_9.py": "tests/test_multigame_windows_lifecycle_review.py",
  "tests/test_p2_r1_t05_hardening_v1.py": "tests/test_t05_hardening.py",
  "tests/test_p3_e1_standalone_v0_1.py": "tests/test_e1_standalone.py"
 }
}''')
RENAMES = DATA['renames']            # old path -> new path (27)
BASE_SHA = DATA['base_sha']          # every touched base path -> its Git blob SHA-256
NEW_SHA = DATA['new_sha']            # every path with new bytes (edited files and new files) -> SHA-256
IN_PLACE = DATA['in_place']          # edited without a rename (3)
NEW_FILES = DATA['new_files']        # added files (docs, history, evidence)
OLD_NAMES = DATA['old_names']        # old module base names, for the N1-T01 scan
GUARDED = DATA['guarded']            # must stay byte-identical in Git
GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
HERE = Path(__file__).resolve().parent
SKIP_SCAN = ('review', 'doc', 'transitory_data', 'exchange', 'source_data', 'results', '.git', '.venv')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(p, b):
    return b if p.endswith('.zip') else b.replace(b'\r\n', b'\n')


def git(repo, *args):
    r = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=GIT_ENV)
    if r.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)} failed: {r.stderr.decode(errors="replace")[:300]}')
    return r.stdout


def need(cond, msg):
    if not cond:
        raise RuntimeError('FAIL: ' + msg)


def name_status(out):
    got = {}
    for ln in out.decode(errors='replace').splitlines():
        if ln:
            code, path = ln.split('\t', 1)
            got[path.strip('"')] = code
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--phase', required=True, choices=['pre', 'post', 'committed'])
    a = ap.parse_args()
    repo = a.repo.resolve()
    need((repo / '.git').exists(), f'not a Git checkout: {repo}')
    for p, h in NEW_SHA.items():  # the package itself must be intact
        need(sha(norm(p, (HERE / 'repo_overlay' / p).read_bytes())) == h, f'package file damaged: {p}')
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    anc = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), 'merge-base', '--is-ancestor', BASE, 'HEAD'],
                         env=GIT_ENV)
    need(anc.returncode == 0, f'HEAD {head} does not descend from base {BASE}; STOP')
    print('HEAD:', head, '(descends from base', BASE[:7] + ')')
    reg = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), 'show', f'HEAD:{REG_V07[0]}'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=GIT_ENV)
    need(reg.returncode == 0 and sha(reg.stdout) == REG_V07[1], 'register v0.7 not installed: install DOC-2 first; STOP')
    for p, h in GUARDED.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'guarded file changed in Git: {p}')
    print(f'{len(GUARDED)} guarded files unchanged in Git HEAD')
    status = git(repo, 'status', '--porcelain=v1', '--untracked-files=all').decode(errors='replace')

    if a.phase == 'pre':
        need(not status.strip(), 'working tree or index not clean:\n' + status[:600])
        for p, h in BASE_SHA.items():
            need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'file to be renamed or edited is not at its base bytes: {p}')
        for p in list(RENAMES.values()) + list(NEW_FILES):
            need(not (repo / p).exists(), f'new path already exists: {p}; STOP')
        print(f'PRE PASS: clean tree; DOC-2 installed; {len(BASE_SHA)} files at their base bytes; '
              f'{len(RENAMES) + len(NEW_FILES)} new paths absent. Nothing was changed.')
        return

    if a.phase == 'post':
        idx = name_status(git(repo, 'diff', '--cached', '--no-renames', '--name-status'))
        want_idx = dict({o: 'D' for o in RENAMES}, **{n: 'A' for n in RENAMES.values()})
        need(idx == want_idx, 'index is not exactly the 27 renames: ' + ', '.join(map(str, sorted(set(idx.items()) ^ set(want_idx.items()))))[:900])
        wt = name_status(git(repo, 'diff', '--no-renames', '--name-status'))
        edited = sorted(p for p in NEW_SHA if p not in NEW_FILES)
        want_wt = {p: 'M' for p in edited}
        need(wt == want_wt, 'working tree changes are not exactly the edited files: ' + ', '.join(map(str, sorted(set(wt.items()) ^ set(want_wt.items()))))[:900])
        untracked = {ln[3:].strip().strip('"') for ln in status.splitlines() if ln.startswith('??')}
        need(untracked == set(NEW_FILES), 'untracked files are not exactly the new files: ' + ', '.join(sorted(untracked ^ set(NEW_FILES)))[:900])
        for p, h in NEW_SHA.items():
            f = repo / p
            need(f.is_file() and not f.is_symlink(), f'missing or symlink: {p}')
            need(sha(norm(p, f.read_bytes())) == h, f'wrong bytes: {p}')
        for o, n in RENAMES.items():
            need(not (repo / o).exists(), f'old path still present: {o}')
            if n not in NEW_SHA:  # pure rename: bytes unchanged
                need(sha(norm(n, (repo / n).read_bytes())) == BASE_SHA[o], f'pure rename changed bytes: {n}')
        pat = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, OLD_NAMES), key=len, reverse=True)) + r')\b')
        hits, stray = [], []
        live = []
        for root, dirs, names in os.walk(repo):
            r = Path(root)
            dirs[:] = sorted(d for d in dirs if d != '__pycache__' and not (r == repo and d in SKIP_SCAN))
            live.extend(r / n for n in sorted(names))
        for f in live:
            rel = f.relative_to(repo)
            if f.is_symlink() or not f.is_file():
                continue
            if rel.parts[0] in ('src', 'tests') and f.suffix in ('.py', '.pyc') and f.stem.split('.')[0] in OLD_NAMES:
                stray.append(rel.as_posix())
            try:
                txt = f.read_text(encoding='utf-8')
            except (UnicodeDecodeError, OSError):
                continue
            if pat.search(txt):
                hits.append(rel.as_posix())
        need(not stray, 'old-name .py/.pyc outside __pycache__: ' + ', '.join(stray))
        need(not hits, 'live files still name an old module: ' + ', '.join(hits))
        print(f'POST PASS: index has exactly the {len(RENAMES)} renames; exactly {len(edited)} edited and '
              f'{len(NEW_FILES)} new files, all with the expected bytes; no old path or old name in live files.')
        return

    need(not status.strip(), 'working tree or index not clean after commit:\n' + status[:600])
    got = name_status(git(repo, 'diff', '--no-renames', '--name-status', 'HEAD~1', 'HEAD'))
    want = dict({o: 'D' for o in RENAMES}, **{n: 'A' for n in RENAMES.values()},
                **{p: 'A' for p in NEW_FILES}, **{p: 'M' for p in IN_PLACE})
    need(got == want, 'the last commit did not change exactly the expected paths: ' + ', '.join(map(str, sorted(set(got.items()) ^ set(want.items()))))[:900])
    for p, h in NEW_SHA.items():
        need(sha(git(repo, 'show', f'HEAD:{p}')) == h, f'wrong Git blob in HEAD: {p}')
    for o, n in RENAMES.items():
        if n not in NEW_SHA:
            need(git(repo, 'show', f'HEAD:{n}') == git(repo, 'show', f'HEAD~1:{o}'), f'pure rename changed bytes: {n}')
    print(f'COMMITTED PASS: the last commit made the {len(RENAMES)} renames, edited {len(NEW_SHA) - len(NEW_FILES)} files '
          f'and added {len(NEW_FILES)}; all Git blobs match.')


if __name__ == '__main__':
    try:
        main()
        print('Read-only: no project code imported, nothing run, nothing changed.')
    except Exception as exc:
        print('VERIFICATION STOP:', exc, file=sys.stderr)
        sys.exit(2)
