# OUTLANDISH_01 — Stage A (Powerball)

**Standalone experiment, not a released prediction method.** It does not import or execute any GAIS fetching script or project runner, does not use a network connection, and does not write to the official data files. Do not commit the experimental data files or results into the project unless separately agreed.

## Current representation (fixed for Stage A)

- A `.bin` constant contains **one numeric decimal digit per unsigned byte**, values `0..9`. Thus `3.1415…` becomes bytes `[3,1,4,1,5,…]`, not ASCII bytes.
- A lottery ball is **two decimal digits**, encoded as two of those bytes: ball `3` → `[0,3]`; ball `12` → `[1,2]`.
- The scanner examines **every starting byte offset**, even/odd alike, never only aligned pairs.
- **P1:** drawn-order seven main balls plus Powerball = 16 digit bytes.
- **P2:** drawn-order seven main balls alone = 14 digit bytes.
- **P3:** any six distinct winning main balls in **any order**, followed by the Powerball = 14 digit bytes. All `7 × 6! = 5,040` orders per draw are recognised using **seven sorted six-ball keys per draw**, instead of materialising millions of permutations.
- The module `digit_bytes_for_ball` centralises the alternative representation (e.g., future `3` → `[3]`); **only the fixed-two-digit scanner is implemented and benchmarked** here. Switching to variable-length numbers requires a separately tested scanning backend, not merely changing the label.

## Exact Windows location for development draws

The project's master filename, as specified by its common draw reader, is:

`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\source_data\POWERBALL_results_master.csv`

Expected columns: `Draw_Number,Date,Drawn_1,...,Drawn_7,Powerball`, with `Drawn_1` through `Drawn_7` in operator-drawn order. The source may have rows outside the experiment's authorised development range.

**Do not manually copy the entire master into the experimental directory.** Instead, use the `prepare` command below. It creates a local **pre-holdout-only** copy, and stops as soon as it sees Powerball draw `1577` or later, without reading the winning-number fields of that draw. It reads only the leading draw number to determine the cutoff. The search itself refuses a CSV containing a draw numbered `1577` or later.

This is a deliberately owner-run, local operation. No project AI session should be sent the actual master or restricted results. To review performance, share only the console log, `.json` summary, and optionally experimental matches from the safe, pre-holdout copy.

## Install files and run (Command Prompt)

Put `outlandish_powerball_stage_a.py` in:

`E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\src\GAIS\OUTLANDISH_01\`

Leave the existing million-byte `digits_pi_10_to_6.bin` and `digits_golden_ratio_10_to_6.bin` there. This scanner does not depend on the old `powerball_search.py` or require `pyahocorasick`. It **does require NumPy**; use the existing project Python environment that already has NumPy if convenient.

```bat
cd /d "E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\src\GAIS\OUTLANDISH_01"
python -c "import numpy; print('NumPy', numpy.__version__)"
python outlandish_powerball_stage_a.py sizes
python outlandish_powerball_stage_a.py self-test
python outlandish_powerball_stage_a.py prepare --source "..\..\..\source_data\POWERBALL_results_master.csv"
python outlandish_powerball_stage_a.py scan
```

The `prepare` command writes `POWERBALL_preholdout_only.csv` in this experimental folder, and **refuses to overwrite it** if it already exists. It checks all extracted rows are consecutive and valid. Keep the copy local, outside the official master and method outputs.

The `scan` command reads that copy, builds all three category indexes, then searches **both** million-digit `.bin` files. It prints a progress line after every 100,000 bytes for the one-million-digit inputs. Output goes under a new, timestamped folder within `OUTLANDISH_01_results\` for each run:

- `<constant>_matches.csv` — every match, with draw number, P1/P2/P3 category, **zero-based start byte offset** and end offset.
- `<constant>_transitions.csv` — W → W+1 pairs where both draws had matches; includes P1-to-next-category nearest signed digit-offset distances.
- `<constant>_summary.json` and `run_summary.json` — draw range, counts, scanned-byte SHA-256, preparation/scan/analysis timing, scan-only throughput and linear 10^9 / 10^12 projections.

It is completely normal for a million-digit scan to find **zero matches**. The `self-test` deliberately plants synthetic matches to prove the matching logic without depending on chance.

For a **larger** binary input, increase chunk size to lower per-chunk overhead, and keep periodic progress time-gated:

```bat
python outlandish_powerball_stage_a.py scan --digits digits_pi_10_to_9.bin --chunk-bytes 4000000 --progress-seconds 5
```

No `mmap`, multi-threading or multiprocessing is required. The scanner uses **bounded-memory positional reads**, processing a chunk plus a **15-digit look-ahead**, so patterns spanning chunks are not missed. For 10^9–10^12, the file remains on disk; it is never wholly read into RAM.

## File size and practical limits

| Decimal digit count | Each numeric-byte `.bin` | Two constants | Notes |
|---:|---:|---:|---|
| 10^6 | 1,000,000 bytes (~0.954 MiB) | 2 MB | Current test |
| 10^9 | 1,000,000,000 bytes (~0.931 GiB) | 2 GB | Feasible storage on reported drive |
| 10^12 | 1,000,000,000,000 bytes (~931.323 GiB) | 2 TB | **One alone exceeds the reported 912.75 GB free** on E:; a larger drive or streaming generation/search would be needed |

The printed runtime projections are **scan-only**, based on observed throughput at the current scale. They are not measured 1 GB/1 TB times. Long-run I/O, caching, disk speed and overhead can change the result. They also exclude digit calculation/generation, input conversion, and building/updating the official results master.

A trillion digits is an enormous computation and storage undertaking even if *searching* that file proves quick; do not generate it before a measured longer trial and a storage plan.

## Optional future constant generation/conversion

The supplied `convert_constant_ascii_to_bin.py` accepts a **plain ASCII text digit stream** (digits, optional whitespace, and at most one decimal point after the initial digit) and writes numeric-byte `.bin` **in constant memory**. It rejects text metadata and checks the declared exact digit count and expected leading digit. It **does not compute the mathematical constant** and deliberately cannot interpret arbitrary y-cruncher formatted output.

For an already verified text file with exactly 1,000,000,000 digits, including the leading integer digit, the eventual conversion would be:

```bat
python convert_constant_ascii_to_bin.py --input "E:\TEMP\pi_digits_plain.txt" --output digits_pi_10_to_9.bin --digits 1000000000 --constant pi
```

**Do not run that example yet** without first verifying the input is clean text and that the output disk has space. The existing `generate_and_convert_10_to_6.py` is suitable only for the current small experiment and is not a scalable 1e9/1e12 generator. Generating truly large π/φ digit streams with y-cruncher is a separate, measured step, with its own output format and storage requirements. The y-cruncher documentation supports both `pi` and `phi`/`goldenratio`; exact CLI options should be checked against your installed version before using them.

## Science / accuracy notes

For 433 illustrative draws (not a claim about the latest real draw count), the **uniform-decimal-digit reference** gives approximate P1 match expectations per constant of 4.33×10^-8 for 10^6 digits, 4.33×10^-5 for 10^9, and 0.0433 for 10^12. P3 expectations are respectively ~0.0218, ~21.8, and ~21,823. Those are reference calculations, not a claim π or φ is random. Consequently, W P1 versus W+1 relationships will likely have no observations even at very large scales. It is exploratory; no conclusions about forecasting follow from matches alone.

**Oz Lotto** is deliberately a separate future script. It must handle its distinct seven main and three supplementary balls, keeping the two games entirely separate. First obtain the actual Powerball results and performance evidence, then design/test Oz Lotto against its own pre-holdout data.
