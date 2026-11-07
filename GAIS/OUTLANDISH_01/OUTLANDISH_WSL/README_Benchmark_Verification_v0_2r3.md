# OUTLANDISH_WSL benchmark-only verification opt-out (candidate v0.2r3)

Contains replacement `wsl_generate.sh`, based on installed v0.2r2.

- Default remains `-verify:1` (no change to verified generation).
- Explicit `--benchmark-no-verify` requests `-verify:0` for throwaway performance experiments only.
- Preview remains default; `--run` required to compute. Large runs still require matching `--ack-large-run N`.
- Prints `RUN_CLASS=BENCHMARK_UNVERIFIED` and `VERIFY_OUTPUT=OFF` to preview, prints warnings, and writes run class to `run.log`.
- Never convert, register or promote output from an unverified benchmark. `wsl_convert.py` validation guard remains untouched.
- Retains disk-swap, CPU, memory and working-root rules as in v0.2r2. Use `taskset -c 0,2,4,6` separately for CPU affinity.

Owner installation is NOT automatic. Back up `OUTLANDISH_WSL/wsl_generate.sh` on E:, then copy this replacement there. Review `bash wsl_generate.sh --help` and PREVIEW both modes; do not run a large computation before preview review.

Example PREVIEW only (no execution):
```bash
taskset -c 0,2,4,6 bash wsl_generate.sh --constant phi --digits 3000000000 --mode swap --memory 12g --td 4 --benchmark-no-verify
```

The tested synthetic candidate does not replace the need for the user's actual system preview or resource review.
