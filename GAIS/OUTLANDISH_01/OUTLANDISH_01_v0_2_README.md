# OUTLANDISH_01 v0.2 — External storage, TOML registry, and conservative retention

**Status:** Implementation candidate for independent review and Windows verification. **Do not regard it as owner-ratified or as installed.** No data copied, deleted, generated, or scanned on the owner's PC by preparing this package.

## Configuration

`outlandish.local.toml` is a **single** commented file beside the active Python scripts, excluded from Git. A tracked template may be kept separately later. `tomllib` (Python 3.11+) reads the user-settings section; Python rewrites *only the marked generated-state section* using a deterministic renderer, preserving user comments/whitespace above the marker. Changes are written by same-directory temporary file + `os.replace`, with a `.toml.bak` containing the previous file. A separate `.lock` serializes cooperating readers and state-writers; the lock and backup are ignored in Git.

**PART 1 — USER CONFIGURABLE:** `main_root = 'G:\OUTLANDISH_01'`; `artifact_dir`, `digits_dir`, `scratch_dir`, `staging_dir`, `results_dir`, and `logs_dir` are explicitly named, separately commented single directory components. Every directory is underneath its commented parent. Configure generator threads/mode/memory and scanner chunk/progress and retention policy here.

**PART 2 — PROGRAM GENERATED — DO NOT EDIT:** `[state.active]` is **empty on first installation**; after registration it has `[state.active.pi]`, `[state.active.phi]`, etc. Each stores a basename only, digit count, independent SHA-256, and UTC verification timestamp. `[state.pending_retirement]` records old verified files until explicitly retired. These records are *not populated based on filename or the old handover*. No symlinks or Windows junctions are permitted.

Derived on the owner's machine:

```text
G:\OUTLANDISH_01\
  large_artifacts\
    digits\     # verified active + explicitly pending-retirement .bin files
    scratch\    # y-cruncher working folders and temporary source TXT
    staging\    # candidate .bin / import copy before create-only publication
    results\    # scanner reports
    logs\       # small optional receipts
```

No implicit E: or fallback location for G: file output. Config `paths` and `audit` are read-only; production subfolders are created on actual use.

## Importing old one-billion-digit files

After installation and an initial audit, import the actual **verified** historical binaries one at a time. `register` requires you to give an *independently recorded* expected SHA-256, not merely one computed from the current input, to avoid accepting arbitrary bytes with a matching 32-digit prefix as authoritative.

The earlier handover recorded these values for the then-verified N=1,000,000,000 numeric-byte data:

- `pi`: `2e633867ad0ed7d866bcc0b3defc29b7704d0808cf62bba1dee1935fc357316e`
- `phi`: `6be7059e971a6c710074682bfac76d415d1eff32c310bdb32c3c91283238d6d8`

**These are historical receipts, not a claim that the two files are currently present or unchanged.** The latest supplied `dir /s /b` listing does not show those two `.bin` files; locate the actual binaries on the owner's machine before attempting import. Do not invent filenames or regenerate automatically.

Example **preview** (replace path with one verified as actually existing):

```bat
python outlandish_artifacts.py register --constant pi --source "E:\ACTUAL\PATH\digits_pi_10_to_9.bin" --digits 1000000000 --expected-sha256 2e633867ad0ed7d866bcc0b3defc29b7704d0808cf62bba1dee1935fc357316e
```

The source must reside under the OUTLANDISH workspace or the configured artifact root; arbitrary external or primary-project paths are refused. After checking the preview and verifying all writers are idle, add `--apply --confirm-idle`. If it is safe and specifically intended to remove the verified original E: binary **after** promotion, also add `--delete-source`. If the source is absent, **do not** attempt registration. The prior root `ycruncher_digits` directory is not automatically deleted.

Registration copies E: to G: staging, verifies numeric byte range, 32-digit mathematical prefix and full SHA against the supplied receipt, safely publishes a create-only `.bin`, then updates TOML atomically. If interrupted after publication, repeating the same command is permitted only if the existing destination independently hashes identically to the supplied receipt. If the TOML is updated but deleting a legacy source fails, the source is preserved and will be reported as misplaced by `audit`.

## Generate and scan

All six mathematical constants remain available through `outlandish_big_constants.py` with the existing y-cruncher CLI, including `pi`, `phi`, `e`, `log2`, `gamma`, and `lemniscate`. Generator output and swap scratch are under configured `scratch_dir`. Conversion writes into `staging_dir`, verifies against the entire previous active file if present, then publishes to `digits_dir`, promotes the new active record and keeps the superseded file *until separate retirement*. It does not bypass the conservative `>=5e9` RAM-only safety guard, nor the Windows y-cruncher swap-mode administrator issue.

```bat
python outlandish_big_constants.py pipeline --constant e --digits 1000000
rem Above is dry-run by default. Add --run only when intended.

python outlandish_powerball_stage_a.py scan --constants pi phi --prefix-digits 1000000000
rem Requires registered active pi and phi with >=1e9 digits each.
```

`scan_1e9.cmd` and `scan_1e10.cmd` use those active records, not historical hard-coded filenames. The scanner stays single-threaded, FIXED2, and still reads only the isolated local `POWERBALL_preholdout_only.csv` for real scans. It never reads the master by default; `prepare` remains an explicit owner-only command. `--prefix-digits` or the older `--max-bytes` limits scan I/O to the requested prefix; scanning the entire active file also checks the recorded SHA-256 against the streamed scan hash. Shorter scans report the registered full-file SHA, but cannot reverify the unscanned suffix during that scan.

## Safe predecessor retirement

After verified replacement, `[state.pending_retirement.pi]` records the former `.bin`. **Nothing is automatically deleted in generation.** Once no program is reading/writing old data, use:

```bat
python outlandish_artifacts.py retire --constant pi
rem Only when you have inspected the plan and confirmed all writers are idle:
python outlandish_artifacts.py retire --constant pi --apply --confirm-idle
```

Retirement rehashes both the new active and old predecessor and checks the entire old prefix before unlinking the old. In the rare case of power loss between unlink and TOML update, `recover-retirement --constant pi` previews recovery, and `--apply --confirm-idle` clears a missing-old marker *only after re-verifying the new active*. Crashes or manually altered configurations require operator inspection; do not automatically guess or repair state. The setting `delete_superseded=true` permits **explicitly approved** retirement, not unattended deletion.

## Audits and recovery

```bat
python outlandish_artifacts.py validate
python outlandish_artifacts.py paths
python outlandish_artifacts.py status
python outlandish_artifacts.py inventory
python outlandish_artifacts.py audit
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test
python test_outlandish_v02.py
python outlandish_artifacts.py audit
```

`audit` reads metadata, detects large/generated files outside the configured G: artifact area and disallows symlinks/junctions, including inside artifacts; the local y-cruncher installation is an explicit exception. It does not open lottery outcome data. Unregistered complete files under `digits/` or incomplete staging files can remain after a crash; these are **not** silently promoted/deleted. Review manually. Normal generator/scanner runs perform pre/post audit. Registry writes use process locks; any non-cooperating external process is a manual safety concern.

Use `generate_1e10.cmd` without parameters for a dry-run. **Only** `generate_1e10.cmd RUN` launches real calculations; the known Windows swap-mode privilege blocker remains.

### Limitations requiring independent review and Windows validation

1. Tested in a Linux synthetic environment, not against the owner's actual G: NTFS filesystem. Windows NTFS hardlink create-only publication, antivirus interaction, free-space estimates and abrupt-kill recovery require Windows evidence.
2. The whole-file validity check uses known 32-digit prefixes and full recorded SHA receipts; for newly generated digits, y-cruncher's own verification and previous-prefix comparison remain the mathematical validation mechanisms. Hashes alone do not independently prove mathematical correctness.
3. The final folder inventory is based on the owner-supplied `dir` list, not a live source checkout. Installer archives specific active names rather than recursively deleting anything unknown.
4. Existing v0.1/1r1 `ARCHIVE` files, y-cruncher installation, pre-holdout CSV and historical scan results are preserved. The retired `test_artifact_safeguards.py` is archived and replaced with `test_outlandish_v02.py`.
5. No real 10^9/10^10/10^11 generation, data migration, lottery scan or destructive Windows validation was performed while building the candidate.
