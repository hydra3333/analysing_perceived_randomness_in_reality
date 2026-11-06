# OUTLANDISH_01 — billion-digit π and φ pipeline, v1r1

**Standalone exploratory experiment.** Not a production method, and no operation in this package accesses lottery results, the project's live datasets, or a lottery website. The existing `outlandish_powerball_stage_a.py` scanner is unchanged and is already parameterised for arbitrary numeric-byte `.bin` files.

## What stays the same

- Both π and φ contain **one unsigned numeric byte per decimal digit** (`0` through `9`), including the integer digit: π starts `[3,1,4,1,5,...]`; φ starts `[1,6,1,8,0,...]`.
- Each lottery ball uses current **FIXED2** representation (`03` = two numeric digit bytes `[0,3]`).
- P1, P2, and P3 and all 433 pre-holdout Powerball draws remain identical. Your existing `POWERBALL_preholdout_only.csv` is reused; **do not rerun `prepare`**.
- The search is single-threaded; every digit offset is considered and 15-digit chunk lookahead preserves cross-boundary matches. The file is never loaded entirely into RAM.
- The π and φ generators are performed **sequentially**, with y-cruncher's own documented single-thread options `-TD:1 -PF:none`; no parallelism. The `--run` launcher uses each output folder as its process working directory.

## Install this add-on

Copy **only** `outlandish_big_constants.py` into:

`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\src\GAIS\OUTLANDISH_01`

Do not overwrite `outlandish_powerball_stage_a.py` or the existing 1,000,000-byte files. Use your existing `.venv` and the same Command Prompt folder.

Run:

```bat
python outlandish_big_constants.py self-test
```

## v1r1 Windows output-location correction

The owner's first real Windows pi smoke test succeeded at 1,000,000 digits in
0.222 seconds of y-cruncher wall time but y-cruncher put its output in the
`OUTLANDISH_01` current directory, **not** the output directory passed with
`-o`. The files observed were `Pi - Dec - Chudnovsky.txt` (1,000,001 bytes)
and `Pi - 20261105-225352.txt` (validation/status file). v1r1 avoids the
uncertain `-o` handling: the subprocess uses `cwd` equal to the dedicated
output directory and omits `-o`. A success with no output files now refuses.
This needs a fresh Windows smoke for phi; only then run the billion-digit jobs.

**Use the already generated pi text as-is to validate the decimal count and
conversion** (do not regenerate it or use the validation/status file):

```bat
python -c "from pathlib import Path; p=Path('Pi - Dec - Chudnovsky.txt'); print('PI TEXT SIZE:',p.stat().st_size,'PREFIX:',repr(p.open('rb').read(40)))"
python outlandish_big_constants.py convert --constant pi --digits 1000000 --input "Pi - Dec - Chudnovsky.txt" --output digits_pi_ycruncher_smoke.bin --reference digits_pi_10_to_6.bin
python outlandish_big_constants.py verify --constant pi --digits 1000000 --input-file digits_pi_ycruncher_smoke.bin --reference digits_pi_10_to_6.bin
```

The prefix should start `b'3.14159265...'`. If the conversion PASSes, the
entire new million-digit sequence equals your existing million-digit pi file.
Do not remove the existing original pi source or original million-digit binary.

## Step 1 — local y-cruncher smoke test at 10^6 (IMPORTANT)

We know y-cruncher v0.8.7.9547b is installed at `y-cruncher v0.8.7.9547b\y-cruncher.exe`, but cannot verify its exact text-file naming and formatting without running it on your Windows PC. **Do not spend time computing 10^9 yet.** First use these commands to test the text format and number of digits generated.

Preview the commands (does not run y-cruncher):

```bat
python outlandish_big_constants.py generate --constant both --digits 1000000
```

Your π smoke run was already successful and its original output can be
validated with the commands above. **Do not repeat π unless needed.** The old
empty `ycruncher_digits\pi_1000000_digits` folder remains and the tool
will intentionally refuse to reuse it. For phi the destination has not been
used, so generate phi next:

```bat
python outlandish_big_constants.py generate --constant phi --digits 1000000 --run
python outlandish_big_constants.py inspect --folder ycruncher_digits\phi_1000000_digits
```

For reference, the π commands below only apply if using a *fresh* output
location; the script refuses an existing output directory to prevent overwrite:


```bat
python outlandish_big_constants.py generate --constant pi --digits 1000000 --run
python outlandish_big_constants.py inspect --folder ycruncher_digits\pi_1000000_digits
```

The φ commands are shown above; do not run them twice.

y-cruncher's command requests `999999` **decimal places** to target `1,000,000` digits **including** the integer digit. This count convention is provisionally based on the command manual and **must be confirmed by the smoke test**. If the generator produces a different count or formatting, **STOP and show the `inspect` output; do not edit the files or guess which lines contain digits**.

Select the actual large **plain-text digit file** reported by `inspect` (not the validation file). If it has only ASCII digits, optional line breaks/spaces, and an optional decimal point after the first digit, convert it. The following uses `YOUR_PI_DIGITS.txt` and `YOUR_PHI_DIGITS.txt` as placeholders—replace these with the real paths from `inspect`:

```bat
python outlandish_big_constants.py convert --constant pi --digits 1000000 --input "YOUR_PI_DIGITS.txt" --output digits_pi_smoke.bin --reference digits_pi_10_to_6.bin
python outlandish_big_constants.py convert --constant phi --digits 1000000 --input "YOUR_PHI_DIGITS.txt" --output digits_golden_ratio_smoke.bin --reference digits_golden_ratio_10_to_6.bin
```

If y-cruncher splits the digits across more than one **digit-only text** file, list the files in correct order after `--input`, e.g. `--input "part1.txt" "part2.txt"` (never include metadata or validation files). The converter is strict, writes a temporary binary first, validates the total count and first million digits, and publishes only on success.

**Do not continue to Step 2 until both smoke conversions PASS.** This verifies alignment of y-cruncher's output with your existing million-digit .bin files.

## Step 2 — generate the 10^9 source text files

Only after Step 1 succeeds:

```bat
python outlandish_big_constants.py generate --constant both --digits 1000000000
```

Review the displayed commands and space. Then generate one constant at a time:

```bat
python outlandish_big_constants.py generate --constant pi --digits 1000000000 --run
python outlandish_big_constants.py inspect --folder ycruncher_digits\pi_1000000000_digits
```

Repeat for the golden ratio:

```bat
python outlandish_big_constants.py generate --constant phi --digits 1000000000 --run
python outlandish_big_constants.py inspect --folder ycruncher_digits\phi_1000000000_digits
```

**Note:** Generating a billion digits is a substantial computation and y-cruncher may need additional memory or scratch/disk space. `-verify:1` checks y-cruncher's output. This software does not estimate or guarantee generation duration. If y-cruncher reports that RAM is insufficient or that it has changed output format, STOP and consult its interactive settings; do not automatically rerun with new unverified flags.

## Step 3 — convert into exact 1,000,000,000-byte files

Replace the `YOUR_...` placeholders with the **actual digit-only** text files from `inspect`. Examples:

```bat
python outlandish_big_constants.py convert --constant pi --digits 1000000000 --input "YOUR_PI_BILLION_DIGITS.txt" --output digits_pi_10_to_9.bin --reference digits_pi_10_to_6.bin
python outlandish_big_constants.py convert --constant phi --digits 1000000000 --input "YOUR_PHI_BILLION_DIGITS.txt" --output digits_golden_ratio_10_to_9.bin --reference digits_golden_ratio_10_to_6.bin
```

The two output files must each be **exactly 1,000,000,000 bytes**. The conversion uses bounded memory (4 MiB input chunks); it never loads a billion digits at once. It checks both the known 32-digit constant prefix and the **full first million digits** against your existing binary files. It rejects extra/missing digits and unrecognised source formatting, without replacing existing outputs.

## Step 4 — independently re-read and validate the resulting binaries

```bat
python outlandish_big_constants.py verify --constant pi --digits 1000000000 --input-file digits_pi_10_to_9.bin --reference digits_pi_10_to_6.bin
python outlandish_big_constants.py verify --constant phi --digits 1000000000 --input-file digits_golden_ratio_10_to_9.bin --reference digits_golden_ratio_10_to_6.bin
```

For each, expect `VERIFY PASS`, the exact size, reference-prefix match, numeric byte values 0..9 everywhere, and a SHA-256 checksum. Preserve these checksums with the search results.

## Step 5 — Powerball search, *no scanner changes needed*

The existing searcher already accepts **multiple input filenames** using `--digits`. This command searches the entire billion-byte input of each constant against the same 433 pre-holdout draws and the same FIXED2 P1/P2/P3 definitions:

```bat
python outlandish_powerball_stage_a.py scan --draws POWERBALL_preholdout_only.csv --digits digits_pi_10_to_9.bin digits_golden_ratio_10_to_9.bin --chunk-bytes 4000000 --progress-seconds 5
```

The scanner creates a new timestamped folder under `OUTLANDISH_01_results` with `*_matches.csv`, `*_transitions.csv`, `*_summary.json` and `run_summary.json`. It prints time-gated progress. **The scan is single-threaded**, chunked, and accepts files much larger than available RAM.

Use a shorter optional smoke on the billion-byte file before the full scan (only 10 million bytes read; does not change the file):

```bat
python outlandish_powerball_stage_a.py scan --draws POWERBALL_preholdout_only.csv --digits digits_pi_10_to_9.bin --chunk-bytes 4000000 --progress-seconds 5 --max-bytes 10000000
```

### Size / timing caveats

One binary file = 1,000,000,000 bytes = 1 GB decimal = 0.931 GiB. Two files = 2 GB. Source text is another ~2 GB in total; allow extra scratch space for y-cruncher and conversion. On E: you previously reported ~912 GB free, enough for this stage in principle.

Earlier 10^6 measured scan-only times were ~0.023 s (π) and ~0.027 s (φ); naïve linear projections were ~23 s and ~27 s at 10^9, respectively. These are **not** measured 1 GB timings and exclude generation/conversion, disk latency, output writing, and differences in match frequency. We will replace them with actual Windows 10^9 measurements.

### Current limitations

- Binary prefix equality plus y-cruncher's own verification is **strong consistency evidence**, but is not an independent check of all billion digits against a separately computed constant.
- This build does not parse arbitrary y-cruncher text headers, validation files, or proprietary compressed `.ycd` output. `-compress:0` requests uncompressed text. The smoke test confirms the exact format before the billion-digit run.
- This addition does not implement Oz Lotto yet. That remains the next separate development stage after Powerball.
- Do not commit experimental binaries, actual draw copies, or result files into the main repository.
