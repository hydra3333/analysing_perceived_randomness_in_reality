# OUTLANDISH_01 — mathematical-constant digit experiments

**Version:** v0.2r4 (automatic superseded-binary retirement)  
**Location in repository:** `GAIS/OUTLANDISH_01/`  
**Large-data root:** configured in `outlandish.local.toml` (currently `G:\OUTLANDISH_01`)  
**Platform:** Windows 11, project Python `.venv`, local y-cruncher

This is an independent *exploratory* experiment in decimal digit streams. It is
**not** the main predictive-randomness experiment or a demonstrated prediction
method. It uses a separate, pre-holdout-only Powerball CSV for scanning.

## Quick reference (CMD.exe)

Open CMD in `GAIS\OUTLANDISH_01` with the **project `.venv` active**. All
commands below run from that directory. `python` means the `.venv` interpreter.

```bat
rem Inspect configuration, active binaries, and artifact placement.
python outlandish_artifacts.py validate
python outlandish_artifacts.py paths
python outlandish_artifacts.py status
python outlandish_artifacts.py audit

rem Verify local program behaviour without a real calculation or lottery data.
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test
python test_outlandish_v02.py

rem PREVIEW generation (does not launch y-cruncher or write digit data).
python outlandish_big_constants.py pipeline --constant pi --digits 1000000000

rem REAL generation: y-cruncher -> numeric-byte binary -> verify -> promote.
python outlandish_big_constants.py pipeline --constant pi --digits 1000000000 --run

rem Scan the full *active* verified pi file. Requires the local pre-holdout CSV.
python outlandish_powerball_stage_a.py scan --constants pi

rem Scan only the first billion digits, when the active file is >= that length.
python outlandish_powerball_stage_a.py scan --constants pi --prefix-digits 1000000000

rem Preview a manual predecessor retirement. No deletion in preview.
python outlandish_artifacts.py retire --constant pi

rem After checking that no user/other program needs that superseded file:
python outlandish_artifacts.py retire --constant pi --apply --confirm-idle
```

**Important:** `status` lists TOML metadata. `audit` checks placement and link
safety, **not** complete file hashes. Real `pipeline` verification/registration
and a full-active-file scan perform full-file digest checks.

## Six supported constants

| CLI identifier | Mathematical quantity | Digit-stream convention |
| --- | --- | --- |
| `pi` | π | `3.14159...` |
| `phi` | Golden ratio | `1.61803...` |
| `e` | Euler's number | `2.71828...` |
| `log2` | Natural logarithm of 2 | `0.69314...` |
| `gamma` | Euler–Mascheroni constant | `0.57721...` |
| `lemniscate` | Lemniscate half-perimeter constant | `2.62205...` |

All binaries are **one byte per decimal digit**, values `0..9` (not ASCII
`'0'..'9'`), and include the initial integer digit. Thus one billion digits
occupy exactly `1,000,000,000` bytes. The stream contains no decimal point.

For `lemniscate`, this experiment uses the conventional half-perimeter
`2.622057...`; y-cruncher's built-in `lemniscate` calculation returns the
full perimeter `5.244115...`. The pipeline performs exact, streaming decimal
division by 2 **before** binary verification and registration; the verification
receipt identifies this transformation.

## `outlandish.local.toml` — user settings and generated state

This is the single local configuration and active-digit registry. The owner has
**chosen to track it in Git**; ignore the older template comment that says
"keep it out of Git". Be aware it contains machine-specific absolute paths.
The program preserves the user section's existing comments, while atomically
replacing the bounded generated-state section. Do not edit generated entries.

### `[settings.storage]` — locations

```toml
[settings.storage]
main_root = 'G:\OUTLANDISH_01'
artifact_dir = 'large_artifacts'
digits_dir = 'digits'
scratch_dir = 'scratch'
staging_dir = 'staging'
results_dir = 'results'
logs_dir = 'logs'
```

The resulting directory tree is:

```text
G:\OUTLANDISH_01\large_artifacts\
    digits\    verified active binaries; pending predecessors only if retained
    scratch\   per-attempt y-cruncher workspace and small run receipts
    staging\   unpromoted, in-progress binary files
    results\   scanner CSV and JSON outputs
    logs\      other small records
```

All generated large files must live beneath this configured artifact root;
there is no implicit fallback to E:. Missing subdirectories are created when
needed. Symlinks and Windows junctions are refused.

### `[settings.generator]` — calculation

```toml
[settings.generator]
threads = 12
mode = 'auto'
memory_gib = 16
ycruncher_verify_output = false
```

- **`threads`**: y-cruncher's `-TD:N` task-queue decomposition, **not** an
  absolute Windows OS-thread cap. The installed v0.2r3 configuration previously
  used `threads = 4`; use `12` if that is your preferred new default. This
  README example does **not** automatically modify your live TOML.
- **`mode`**: `auto` chooses RAM-only below 5 billion digits and disk-swap
  mode at or above that threshold. This does **not** guarantee swap works:
  y-cruncher's Windows disk-swap privilege issue remains unresolved. Explicit
  RAM-only real launches at >=5 billion digits are refused until memory safety
  is reviewed. Check the preview before starting expensive work.
- **`memory_gib`**: y-cruncher memory allocation parameter *in swap mode*;
  it is **not** an enforced RAM ceiling for RAM-only calculations.
- **`ycruncher_verify_output`**: defaults to `false`, producing `-verify:0`.
  `true` produces `-verify:1`. The Python converter still checks format,
  known reference prefix, complete predecessor prefix, and full SHA-256.
  These checks do **not** independently establish the mathematical correctness
  of *new* digits beyond the trusted prior prefix when y-cruncher's own
  verification is disabled.

Per-run overrides:

```bat
python outlandish_big_constants.py pipeline --constant gamma --digits 1000000000 --threads 12
python outlandish_big_constants.py pipeline --constant gamma --digits 1000000000 --threads 12 --run
python outlandish_big_constants.py pipeline --constant gamma --digits 1000000000 --ycruncher-verify-output --run
```

A command without `--run` is a preview; the number of threads alone does not
start a calculation.

### `[settings.scanner]` — scanning

```toml
[settings.scanner]
chunk_bytes = 4000000
progress_seconds = 5
```

The scanner uses one NumPy-vectorised scanning process and reports progress
at the configured interval. `chunk_bytes` controls chunk size, **not** thread
count. Per-run overrides: `--chunk-bytes N` and `--progress-seconds N`.

### `[settings.retention]` — automatic predecessor cleanup (v0.2r4)

```toml
[settings.retention]
delete_superseded = true
```

When `true`, a **successful new verified promotion** automatically deletes
only the precisely recorded predecessor binary. The sequence under the
shared OUTLANDISH cross-process lock is:

1. Verify the new complete file and SHA-256, verify the old complete file and
   its recorded SHA-256, and compare **all** old digits against the new prefix.
2. Atomically publish the new active registry record and a pending-retirement
   record for the old file.
3. Check that the just-published file identities/lengths are unchanged.
4. Unlink the old predecessor and atomically clear its pending record.

The new active file is never a deletion target. The lock coordinates
cooperating OUTLANDISH generators, scanners and registry commands; it **cannot
prove that arbitrary outside programs are idle**. Make sure third-party
readers are closed when retiring a large predecessor. No deletion occurs on a
failed validation or unsuccessful promotion.

When `false`, the predecessor remains and is recorded as pending. The same
manual retirement command is available after changing the setting to `true`.

**Important transitional detail:** enabling v0.2r4 does *not* automatically
remove predecessors already pending from runs completed with v0.2r3. Those
need the explicit `retire` operation shown below. The next successful
promotion for any constant with an unresolved pending predecessor is refused
until it is resolved, so no retirement record is silently overwritten.

### `[state.active]` and `[state.pending_retirement]`

**Program-generated; do not manually edit.** Each active constant has a
basename, digit count, SHA-256, and verification time. A pending entry
identifies the exact superseded file awaiting safe deletion or recovery. The
`.toml.bak` file is the previous registry snapshot, **not** a replacement for
backing up the G: binaries. Git tracks the TOML by the owner's choice; the
large `.bin` files are not Git artifacts.

## Generating digits

The recommended subcommand is **`pipeline`**: it runs y-cruncher, locates the
plain-text source, converts to numeric-byte binary, re-reads/verifies it,
compares the entire previous active prefix when present, publishes the new
binary, updates TOML, cleans intermediate digit text, and optionally retires
the old active binary as above. Small y-cruncher reports and verification
manifests are retained.

Start with 1,000,000 digits when a constant has no prior registered reference:

```bat
python outlandish_big_constants.py pipeline --constant pi --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant phi --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant e --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant log2 --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant gamma --digits 1000000 --run
python outlandish_big_constants.py pipeline --constant lemniscate --digits 1000000 --run
```

Then promote to a billion digits, **one constant/run at a time**:

```bat
python outlandish_big_constants.py pipeline --constant pi --digits 1000000000 --run
python outlandish_big_constants.py pipeline --constant phi --digits 1000000000 --run
python outlandish_big_constants.py pipeline --constant e --digits 1000000000 --run
python outlandish_big_constants.py pipeline --constant log2 --digits 1000000000 --run
python outlandish_big_constants.py pipeline --constant gamma --digits 1000000000 --run
python outlandish_big_constants.py pipeline --constant lemniscate --digits 1000000000 --run
```

**These are examples, not a script to run blindly:** each new candidate must
be *strictly longer* than the current active file. Do not re-run a completed
same-size generation; confirm status and choose a larger depth. Use the
no-`--run` preview to see the actual command and resource mode. A large
calculation requires an already registered, verified smaller prefix.

### Other calculator/format operations

```bat
rem Only launch y-cruncher; DOES NOT convert/promote into the active registry.
python outlandish_big_constants.py generate --constant pi --digits 1000000
python outlandish_big_constants.py generate --constant pi --digits 1000000 --run

rem Inspect a specific owned scratch output directory (replace the folder).
python outlandish_big_constants.py inspect --folder "G:\OUTLANDISH_01\large_artifacts\scratch\ACTUAL_ATTEMPT_FOLDER"

rem Convert EXISTING y-cruncher decimal text to a staged numeric-byte binary.
rem Explicit arguments required: replace all paths and specify a real reference
rem only when it actually exists. `convert` does not promote by itself.
python outlandish_big_constants.py convert --constant pi --digits 1000000 --input "G:\OUTLANDISH_01\large_artifacts\scratch\ACTUAL_ATTEMPT_FOLDER\ACTUAL_DIGIT_FILE.txt" --output "G:\OUTLANDISH_01\large_artifacts\staging\custom_pi.bin"

rem Independently read and check a staged binary, without registering it.
python outlandish_big_constants.py verify --constant pi --digits 1000000 --input-file "G:\OUTLANDISH_01\large_artifacts\staging\custom_pi.bin"
```

Conversion input/output must be beneath the configured artifact root. For
normal work, use `pipeline` instead of manual conversion, verification and
registration. `--keep-text` overrides ordinary **successful** temporary-text
cleanup and can consume substantial disk space. On a *handled failed run*,
owned large intermediates are removed but small failure reports are kept;
previous unrecognised scratch folders are not automatically deleted.

## Scanning / parsing the digit streams

The Powerball scanner reads `POWERBALL_preholdout_only.csv` from the
OUTLANDISH folder by default. It uses **only** the 433 pre-holdout draws
1144–1576; draw 1577 and later are excluded. Its three pattern categories:

- **P1** — seven main numbers in operator-drawn order, followed by Powerball.
- **P2** — seven main numbers in operator-drawn order.
- **P3** — any six distinct main numbers in any order, followed by Powerball.

Balls are encoded as two decimal digits each (`03`, `12`, etc.). This
experiment intentionally uses fixed-width encoding and searches at every
possible byte offset. Matches/transition evidence are written to separate
run directories beneath `large_artifacts\results\`.

```bat
rem Scan all six at their respective COMPLETE active digit lengths.
python outlandish_powerball_stage_a.py scan --constants pi phi e log2 gamma lemniscate

rem Compare six constants at the SAME first 1,000,000,000 digits, when each
rem has an active file with at least that many digits.
python outlandish_powerball_stage_a.py scan --constants pi phi e log2 gamma lemniscate --prefix-digits 1000000000

rem Single constant at a specified depth.
python outlandish_powerball_stage_a.py scan --constants pi --prefix-digits 1000000000

rem View binary storage/size guidance and run invented-data tests.
python outlandish_powerball_stage_a.py sizes
python outlandish_powerball_stage_a.py self-test
```

The existing convenience launchers `scan_1e9.cmd` and `scan_1e10.cmd`
request **π and φ together** at those depths and will refuse if either active
file is too short. The `generate_1e10.cmd` launcher is preview-only by
default; `generate_1e10.cmd RUN` attempts real generation, but the current
swap/memory preflight limitations still apply.

### Preparing the isolated draw CSV (only if absent)

```bat
python outlandish_powerball_stage_a.py prepare --source "E:\ACTUAL\PATH\TO\AUTHORIZED_HISTORICAL_MASTER.csv"
```

Supply the *actual*, explicitly authorised historical master path; the
script's default output is `GAIS\OUTLANDISH_01\POWERBALL_preholdout_only.csv`.
Do not run `prepare` merely to refresh an existing valid copy, and do not
point the scanner directly at a master containing held-out outcomes.

## Retiring predecessors, including v0.2r3 pending files

Automatic retirement applies **only to new successful promotions after this
patch is installed**. For predecessors already pending in your TOML, the
retirement operation is deliberately still explicit. With all OUTLANDISH
work idle, inspect each preview:

```bat
python outlandish_artifacts.py retire --constant pi
python outlandish_artifacts.py retire --constant phi
python outlandish_artifacts.py retire --constant e
python outlandish_artifacts.py retire --constant log2
```

Then execute **only for constants whose pending predecessors are shown**:

```bat
python outlandish_artifacts.py retire --constant pi --apply --confirm-idle
python outlandish_artifacts.py retire --constant phi --apply --confirm-idle
python outlandish_artifacts.py retire --constant e --apply --confirm-idle
python outlandish_artifacts.py retire --constant log2 --apply --confirm-idle
```

The explicit operation re-verifies both complete files and the entire
predecessor prefix before deleting the old one. It leaves new active files
alone. `--confirm-idle` means *you* have checked that outside programs will
not be using the predecessor; it does not probe every external process.

If a crash happened **after unlink but before the pending marker was
removed**, first preview and inspect:

```bat
python outlandish_artifacts.py recover-retirement --constant pi
```

Only if the reported predecessor is **already missing** and the verified new
active file is correct, clear the stale marker:

```bat
python outlandish_artifacts.py recover-retirement --constant pi --apply --confirm-idle
```

Do not manually edit the registry, delete a pending file by hand, overwrite
any active `.bin`, or run another same-constant upgrade with unresolved
retirement. If automatic deletion warns that the old file is still present,
use `retire`. If the old file is missing, use `recover-retirement`.

## Importing an existing externally verified numeric-byte binary

Use this only for previously verified binaries, not for y-cruncher text.
Registration requires an **independently recorded** SHA-256, not a hash you
just computed from an untrusted candidate. Example syntax (replace paths and
hash with genuine existing evidence):

```bat
python outlandish_artifacts.py register --constant pi --source "E:\ACTUAL\PATH\digits_pi_10_to_9.bin" --digits 1000000000 --expected-sha256 REPLACE_WITH_PREVIOUSLY_VERIFIED_64_HEX_SHA256

rem Add flags to the same command only after inspecting its preview:
rem --apply --confirm-idle
rem Optional --delete-source removes the import source AFTER verified promotion.
```

The input source must be in the OUTLANDISH workspace or configured artifact
root, not an arbitrary external path. Registration still uses the same
strictly-longer active/prefix conditions and new v0.2r4 automatic predecessor
retirement setting.

## Diagnostics, failure handling, and operational boundaries

```bat
python outlandish_artifacts.py validate
python outlandish_artifacts.py paths
python outlandish_artifacts.py status
python outlandish_artifacts.py inventory
python outlandish_artifacts.py audit
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test
python test_outlandish_v02.py
```

- Generator and scanner use a shared cooperative lock. A normal scanner holds
  it for its full scan, so normal automatic retirement cannot race that scan.
  Non-cooperating external programs remain the operator's responsibility.
- The generated active file is validated *before* the old file is deleted.
  Auto-retire failure does not roll back the already successful active
  promotion. It prints a warning and preserves the pending state for manual
  resolution; on an interruption after unlink, `recover-retirement` applies.
- Failed y-cruncher attempts clean **owned large temporary data** but preserve
  small diagnostics. A power loss or an old v0.2r2 attempt may leave large
  historical scratch data requiring deliberate inspection and cleanup.
- A scan's reported full-file digest verifies the entire active binary only
  when the entire active file was scanned. A shorter prefix scan does not
  re-verify the unscanned suffix.
- Neither matching lottery patterns nor a recorded SHA-256 establishes
  predictive performance. Digit-stream patterns must be interpreted against
  appropriate chance baselines, multiple comparisons and independent tests.
- This v0.2r4 source/test patch was synthetically tested in a separate
  workspace; Windows destructive-file and lock behaviour should be checked
  with a small verified promotion before relying on it at larger data depths.
