# MHUP-B slice 2 - working notes (Claude; cloud workspace; nothing installed)

Slice 2 = L5 (OV-1) + L6 (development runs), built ON TOP of slice 1's tree. Governing: code plan v0.3 (L5, L6,
sections 6, 7, 9), supplement v0.8 (6.5, 6.8, 7), the working principle of 18 November 2026 (decision log entry 81).

Workspace: /home/claude/work/slice2/{tools, dev}. Build: `sh tools/build_dev_slice2.sh BASE DEV SLICE1_TOOLS SLICE2_TOOLS`
(slice 1 first, then `apply_slice2.py`, `edit_tests_slice2.py` if present, then the files of `slice2_new/` by final path).
Suite: slice 1's `run_suite.py`. Second Python: /home/claude/work/venv315 (see CONTINUITY_NOW, "Resuming").

## Progress log (times Australia/Adelaide, read from the clock)
- 00:46 18 Nov: started on the owner's go (00:35). Kernel `src/evaluation/ov1_numeric.py` and `tests/test_mhupb_ov1_numeric.py` (18 tests) pass on 3.13.18 and 3.15.0b4. Found and fixed a hole in the plan-stage probe's `exp_enc`: when ceil(a / 2^j) was S + 1 it used exp(1)'s upper end; the kernel reduces until the CEILING is within range. The plan's |Z| bound is valid but not attained (two-level weights give Z^2 = N - 1). NEXT: ov1.py (registration, ledger, record/stop/status/verify), Method_OV1.py, tests; then L6.
- 00:52 18 Nov: `src/evaluation/ov1.py` and `Method_OV1.py` written; a whole register / freeze / record / score / record flow works on the synthetic weekly project (eligibility sealed before the cut-off, factor from the score lines, verify rebuilds 3 lines). NEXT: tests/test_mhupb_ov1.py (list in the module docstring to come), measure registry entry, then L6.
