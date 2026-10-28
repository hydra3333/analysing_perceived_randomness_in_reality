@echo off
setlocal
rem OPTIONAL owner-run staging of the 40 NAMES-1 content paths (the renames are already staged).
rem No commit, push or deletion.
git add -- ^
  "src\Powerball_Experiment_Coordinator.py" ^
  "src\coordinator_private\multigame_coordinator_exit_receipt.py" ^
  "src\coordinator_private\multigame_launch_spec.py" ^
  "src\coordinator_private\multigame_windows_lifecycle.py" ^
  "src\methods\E_001_Historical_Appearance_Frequency.py" ^
  "src\methods\POC_MultiGame_Synthetic_Worker.py" ^
  "src\methods\_common\e1_common_reader_bridge.py" ^
  "src\methods\_common\e1_training_view.py" ^
  "src\methods\_common\game_draws_reader.py" ^
  "src\methods\_common\multigame_ancestry_release.py" ^
  "src\methods\_common\multigame_console_protocol.py" ^
  "src\methods\_common\multigame_coordinated_manifest.py" ^
  "src\methods\_common\multigame_e1.py" ^
  "src\methods\_common\multigame_method_registry.py" ^
  "src\methods\_common\multigame_result_registry.py" ^
  "src\methods\_common\multigame_standalone_contract.py" ^
  "src\methods\_common\multigame_synthetic_scorer.py" ^
  "src\methods\_common\multigame_worker_launch_handshake.py" ^
  "tests\test_e1_standalone.py" ^
  "tests\test_multigame_console_and_synthetic_scorer.py" ^
  "tests\test_multigame_exit_receipt.py" ^
  "tests\test_multigame_launch_and_manifest.py" ^
  "tests\test_multigame_reader_contracts.py" ^
  "tests\test_multigame_science_allowlist.py" ^
  "tests\test_multigame_static_and_timing.py" ^
  "tests\test_multigame_windows_lifecycle_review.py" ^
  "tests\test_t05_hardening.py" ^
  "doc\Predictive_Randomness_NAMES1_Rename_Specification_v0_2.md" ^
  "doc\RATIFICATION_REGISTER_v0_8.md" ^
  "review\Independent_ChatGPT_Focused_Recheck_NAMES1_Spec_v0_2.md" ^
  "review\Independent_ChatGPT_R3_Design_Review_NAMES1_v0_1.md" ^
  "review\NAMES1_Code_Install_v1\INSTALL_MANIFEST_SHA256.txt" ^
  "review\NAMES1_Code_Install_v1\ast_check_output.txt" ^
  "review\NAMES1_Code_Install_v1\names1_allowlist.tsv" ^
  "review\NAMES1_Code_Install_v1\negative_checks_output.txt" ^
  "review\NAMES1_Code_Install_v1\suite_per_module_linux.txt" ^
  "review\NAMES1_Code_Install_v1\t02_check_output.txt" ^
  "review\NAMES1_Spec_Recheck_v0_2.zip" ^
  "review\NAMES1_Spec_Review_v0_1.zip" ^
  "review\Owner_Decisions_and_E1_ALIGN_Proposal_28Oct2026.md"
if errorlevel 1 (echo STAGING FAILED & exit /b 1)
git status --short
endlocal
