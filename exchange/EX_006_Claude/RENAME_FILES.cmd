@echo off
setlocal
rem NAMES-1: the 27 explicit renames (git mv). Run from the repository root after PRE PASS.
rem Stops at the first failure. No commit, push or deletion of content.
git mv -- "src\coordinator_private\multigame_coordinator_exit_receipt_v2.py" "src\coordinator_private\multigame_coordinator_exit_receipt.py" || goto :fail
git mv -- "src\coordinator_private\multigame_launch_spec_v1.py" "src\coordinator_private\multigame_launch_spec.py" || goto :fail
git mv -- "src\coordinator_private\multigame_windows_lifecycle_v1.py" "src\coordinator_private\multigame_windows_lifecycle.py" || goto :fail
git mv -- "src\methods\_common\e1_common_reader_bridge_v1.py" "src\methods\_common\e1_common_reader_bridge.py" || goto :fail
git mv -- "src\methods\_common\e1_historical_appearance_frequency_v0_3.py" "src\methods\_common\e1_historical_appearance_frequency.py" || goto :fail
git mv -- "src\methods\_common\e1_standalone_contract_v0_1.py" "src\methods\_common\e1_standalone_contract.py" || goto :fail
git mv -- "src\methods\_common\e1_training_view_v0_1.py" "src\methods\_common\e1_training_view.py" || goto :fail
git mv -- "src\methods\_common\game_draws_reader_v1.py" "src\methods\_common\game_draws_reader.py" || goto :fail
git mv -- "src\methods\_common\game_profiles_v1.py" "src\methods\_common\game_profiles.py" || goto :fail
git mv -- "src\methods\_common\multigame_ancestry_release_v1.py" "src\methods\_common\multigame_ancestry_release.py" || goto :fail
git mv -- "src\methods\_common\multigame_console_protocol_v1.py" "src\methods\_common\multigame_console_protocol.py" || goto :fail
git mv -- "src\methods\_common\multigame_coordinated_manifest_v1.py" "src\methods\_common\multigame_coordinated_manifest.py" || goto :fail
git mv -- "src\methods\_common\multigame_e1_v1.py" "src\methods\_common\multigame_e1.py" || goto :fail
git mv -- "src\methods\_common\multigame_method_registry_v1.py" "src\methods\_common\multigame_method_registry.py" || goto :fail
git mv -- "src\methods\_common\multigame_result_registry_v1.py" "src\methods\_common\multigame_result_registry.py" || goto :fail
git mv -- "src\methods\_common\multigame_standalone_contract_v1.py" "src\methods\_common\multigame_standalone_contract.py" || goto :fail
git mv -- "src\methods\_common\multigame_synthetic_scorer_v1.py" "src\methods\_common\multigame_synthetic_scorer.py" || goto :fail
git mv -- "src\methods\_common\multigame_worker_launch_handshake_v1.py" "src\methods\_common\multigame_worker_launch_handshake.py" || goto :fail
git mv -- "tests\test_multigame_console_and_synthetic_scorer_v0_4.py" "tests\test_multigame_console_and_synthetic_scorer.py" || goto :fail
git mv -- "tests\test_multigame_exit_receipt_v0_8.py" "tests\test_multigame_exit_receipt.py" || goto :fail
git mv -- "tests\test_multigame_launch_and_manifest_v0_8.py" "tests\test_multigame_launch_and_manifest.py" || goto :fail
git mv -- "tests\test_multigame_science_allowlist_v0_8.py" "tests\test_multigame_science_allowlist.py" || goto :fail
git mv -- "tests\test_multigame_v011_reader_contracts.py" "tests\test_multigame_reader_contracts.py" || goto :fail
git mv -- "tests\test_multigame_v011_static_and_timing.py" "tests\test_multigame_static_and_timing.py" || goto :fail
git mv -- "tests\test_multigame_windows_lifecycle_review_v0_9.py" "tests\test_multigame_windows_lifecycle_review.py" || goto :fail
git mv -- "tests\test_p2_r1_t05_hardening_v1.py" "tests\test_t05_hardening.py" || goto :fail
git mv -- "tests\test_p3_e1_standalone_v0_1.py" "tests\test_e1_standalone.py" || goto :fail
echo RENAMES DONE: 27 files renamed in the index.
endlocal
exit /b 0
:fail
echo RENAME FAILED: stop and send Claude this output.
endlocal
exit /b 1
