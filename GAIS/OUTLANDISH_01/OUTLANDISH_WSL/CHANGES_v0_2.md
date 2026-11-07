# WSL packed-nibble redesign — change record v0.2 (2026-11-07)

* **Replaces** the development `OUTLANDISH_WSL_Integration_v0_1` source candidate. Does not install into or edit user's E:/T:/G: workspaces.
* Adds `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1` format, 2 ASCII decimal digits per byte, high nibble first; final low nibble zero padding for odd digit count.
* Rewrites Linux converter to perform native-C `bytes.fromhex` packing in bounded chunks, including exact decimal halving of y-cruncher full-perimeter lemniscate (a pure-Python slower operation). Source text is removed after create-only output publication, bounded sample readback and a durable receipt; on conversion failure source retained.
* Rewrites Windows verifier as **read-only sampled** inspection of packed receipt blocks and optional sampled numeric-byte legacy-reference prefix. No full reread in converter or verifier.
* Adds a separate NumPy Powerball P1/P2/P3 packed scanner, comparing all decimal-digit offsets and validating a complete file's streamed SHA-256 during its ordinary scan. Does not read master draw history or post-cutoff outcomes.
* Retains conservative standalone Linux y-cruncher generation (`-verify:1`, TD1, proposed 4g swap cap), preview-only by default; execution requires explicit `--run`, large count acknowledgement where applicable.
* Adds Windows BAT wrappers that locate the EXISTING repo-root `.venv` and call the EXISTING repo-root `activate_venv.bat`; the supplied project-root venv/dependency BATs are not edited.
* No second mutable production TOML; per-file staging receipts only. **Neither existing numeric-byte scanner nor active registry is compatible with packed binaries.** Future production registration and replacement/retirement policy remain separate; six G: active binaries are untouched.
* Tests: 12 synthetic cases passed on the builder's Python 3.13/NumPy 2.3.5 Linux container. `bash -n` on generator passed; user-specific WSL/DrvFS hard links, Win11 CMD wrappers and existing project NumPy venv **NOT YET TESTED**. First rehearsal must be on T: with `--keep-text`.
