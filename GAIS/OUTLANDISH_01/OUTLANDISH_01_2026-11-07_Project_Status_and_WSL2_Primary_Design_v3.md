# OUTLANDISH_01 — current project handover: WSL2 primary design and verified feasibility

**Document:** `OUTLANDISH_01_2026-11-07_Project_Status_and_WSL2_Primary_Design_v3.md`  
**Date:** 7 November 2026 (Australia/Adelaide); updated after the WSL2 experiments and architecture decisions on this date  
**Version:** v3 (supersedes v2 as the *conversation handover*, not as source-code authority)  
**Status:** **WSL2 is the adopted primary direction**, with non-root Linux y-cruncher calculations demonstrated through 100 million golden-ratio digits. **The Linux-to-Windows import integration is not yet implemented or tested. No 10-billion-digit calculation has been completed.**  
**Audience:** Owner and next ChatGPT development/review conversation working specifically on `GAIS/OUTLANDISH_01/OUTLANDISH_WSL`.

> **Priority reading:** Read Part I (current decisions and evidence) before the retained historical baseline and Windows Sandbox appendices in Part II. The installed E: Python source, current TOML, current README, and actual G: registry/files are authoritative for code and state. This document records owner-supplied console evidence and review conclusions, not a live filesystem audit. Nothing herein authorises a 10^10 calculation, promotion, deletion, changes to system privileges, or changes to the main predictive-randomness project.

---

# Part I — current state, decided primary architecture and next implementation

## Executive checkpoint

**What is already established:**

- OUTLANDISH_01 is a **separate, intentionally speculative digit-search study** located at `GAIS/OUTLANDISH_01/` in the `hydra3333/analysing_perceived_randomness_in_reality` repository. Keep it separate from the governed E_1..E_62 randomness-method programme and its holdout.
- The existing native-Windows OUTLANDISH v0.2r4 code and owner-reported active registry on E:/G: already manage six independently verified **10^9-decimal-digit numeric-byte streams**: `pi`, `phi`, `e`, `log2`, `gamma`, and `lemniscate` (half-perimeter convention). The six G: production binaries are not test inputs for destructive operations.
- Windows Sandbox was tried, comprehensively diagnosed and **abandoned**. Python and tests eventually worked, but the Windows guest y-cruncher launcher failed `0xC000007B`. Historical evidence is retained below; do not restart that work by default.
- **Debian 13 (trixie) under WSL2 is now installed, running and stored on T:**. The Linux *static* y-cruncher v0.8.7 Build 9547 launches and has generated/verified golden-ratio decimal outputs in RAM and disk-swap mode, **without `sudo`**.
- Windows can read WSL output via `\\wsl.localhost\Debian\home\u\...`; a real directory listing of the 100-million-digit output succeeded.
- Owner agreed the **primary new design**: version-controlled WSL-specific code/configuration/documentation on E: in `OUTLANDISH_WSL/`; Debian-native execution and large scratch on T:; existing, unmodified Windows verification/registry on G: only when explicitly authorised. **Do not build a parallel complete Linux OUTLANDISH registry or install Debian Python by default.**
- **The next work item is a thin, isolated WSL generation-to-Windows staging/conversion/verification adapter**, with a non-promoting rehearsal against the already-generated 100-million-digit φ output. No new large calculations are needed to design/test that integration.

## 1. Exact directory layout and status

| Location | Purpose | Status / rule |
|---|---|---|
| `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\GAIS\OUTLANDISH_01\` | Established Windows Python modules, production TOML, tests, README, small project docs | **Existing authoritative implementation.** Do not casually modify. |
| `E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality\GAIS\OUTLANDISH_01\OUTLANDISH_WSL\` | **Single authoritative source folder for new WSL-specific scripts (`.sh`, optional `.py`), test source, configuration templates and documentation** | Created by owner. New files here are proposed; there is **no completed integration code yet**. Git-managed, small files only. |
| `/mnt/e/SOFTWARE-Win11/powerball/analysing_perceived_randomness_in_reality/GAIS/OUTLANDISH_01/OUTLANDISH_WSL` | Same E: folder as seen by Debian | WSL can run scripts directly, e.g. `bash ./script.sh`. No permanent duplicate editable script tree inside Debian. Avoid heavy data I/O here. |
| `T:\OUTLANDISH_WSL\` | Experimental downloads and WSL2 distro storage | Created by owner. T: is **not** the G: production artifact root. |
| `T:\OUTLANDISH_WSL\Debian\ext4.vhdx` | Debian-native ext4 filesystem inside WSL2 | **Verified** at this T: path. On 7 Nov its host file was 348,127,232 bytes; dynamically grows. |
| `/home/u/outlandish-test/` | Current Linux test workspace and extracted static y-cruncher | Working. Successful 100k RAM, 1m/10m/100m swap outputs retained in individual folders. |
| `/home/u/outlandish-work/` | **Proposed** controlled future native Linux workspace | Not yet created as the integrated production workspace. Would separate scratch/swap, completed outputs and logs. Inside T:-backed ext4, not `/mnt/t`. |
| `G:\OUTLANDISH_01\large_artifacts\` | Established Windows artifact root (digits, scratch, staging, results, logs) | Existing six production active constants. Never use for destructive rehearsals. |

The owner also created `T:\OUTLANDISH_WSL` and the E: `OUTLANDISH_WSL` folder before installing Debian; the two folders have distinct jobs. WSL **code is edited and versioned on E:**; the executing Bash process can read it directly via `/mnt/e`; Linux y-cruncher binary and large working files live **inside ext4 on T:**. This is an explicit owner design choice and supersedes earlier suggestions of maintaining duplicate scripts within Debian.

**Windows view of the existing successful Linux sample**, tested by the owner:

```bat
 dir "\\wsl.localhost\Debian\home\u\outlandish-test\phi_100m_swap"
```

Observed `Golden Ratio - Dec - Newton.txt` size: **100,000,001 bytes** (decimal point included), and verification report `Golden Ratio - 20261107-172852.txt` 11,695 bytes. The file contains **100,000,000 digits including the integer digit** and one decimal point; the planned canonical binary is exactly **100,000,000 bytes**, one numeric value 0–9 per byte.

### Why not store everything in one drive?

E: is versioned source; T: is dispensable computational/testing storage; G: holds irreplaceable/reproducible but costly-to-regenerate production outputs. No generated multi-gigabyte files, Python caches, WSL virtual disks, checkout-local registry copies, or sensitive historical CSVs should be added to Git. Linux heavy scratch/FFT/swap must use ext4 for best compatibility and I/O rather than `/mnt/e`, `/mnt/t` or `/mnt/g`. A Windows-only test may use a separately configured T: scratch workspace; it must not accidentally load the production registry merely because the script imports a module from E:.

## 2. Actual Debian and WSL2 evidence, 7 November 2026

**Installation facts reported by owner:**

```text
wsl --status          Default Version: 2
wsl --version         WSL 2.5.7.0; kernel 6.6.87.1-1
wsl --list --verbose  Debian  Running  VERSION 2
Linux home:           /home/u
uname -m:             x86_64
Linux filesystem:     /dev/sdd ext4, 1007G virtual capacity
Host backing VHDX:    T:\OUTLANDISH_WSL\Debian\ext4.vhdx
```

Debian is `trixie`. Minimal Debian did not initially have the `xz` executable; `sudo apt update` and `sudo apt install -y xz-utils` completed. No Debian Python, pip, NumPy, compilers, or whole OUTLANDISH runtime has been installed for this work. The Linux static y-cruncher archive `y-cruncher v0.8.7.9547-static.tar.xz` was downloaded to T:, inspected and unpacked under `/home/u/outlandish-test/y-cruncher v0.8.7.9547-static`. The Linux executable started correctly and selected `Linux/19-ZN2 ~ Kagari` for the Ryzen 9 3900X. The `Insufficient permissions to set thread priority; retry as root` warning is **nonfatal**, and there is no reason to run these tasks as root just to remove it.

Owner's verified calculation results:

| Case | y-cruncher mode / parallel settings | Exit | Wall time | Logical RAM estimate | Logical disk estimate (excluding text unless noted) | Spot check |
|---|---|---:|---:|---:|---:|---|
| φ **100,000 digits**, `-dec:99999` | RAM; `-TD:1 -PF:none` | 0 | **0.086s** | 12.0 MiB | No swap; 97.7 KiB output | Good through 75,000 |
| φ **1,000,000 digits**, `-dec:999999` | Swap; `-TD:1 -PF:none -M:256m`, dedicated RAID0 dir | 0 | **1.727s** | 83.8 MiB | 73.6 MiB + 977 KiB output | Good through 750,000 |
| φ **10,000,000 digits**, `-dec:9999999` | Same swap settings | 0 | **6.982s** | 122 MiB | 101 MiB + 9.54 MiB output | Good through 7,500,000 |
| φ **100,000,000 digits**, `-dec:99999999` | Same swap settings | 0 | **50.108s** | 256 MiB | 373 MiB + 95.4 MiB output | Good through 75,000,000 |

All four reported `Verify Output: Enabled`, finished with **exit code 0**, and produced the requested decimal text plus verification reports. The 100-million-digit run used `Working Memory 179 MiB`, `Twiddle Tables 13.9 MiB`, `I/O Buffers 64.0 MiB`. Its swap directory showed only **8 KiB** after successful cleanup. This supports completed disk-swap mode, but the post-run directory size **does not measure peak physical I/O**. At 100 million digits y-cruncher estimated 373 MiB temporary disk, exceeding the 256 MiB total configured memory; this is a more meaningful far-memory rehearsal than tiny runs, without proving performance or endurance at 10^10.

**Observed successful small-run Linux command pattern** (examples are **historical evidence**, not an instruction to rerun now):

```bash
# Executed in a dedicated /home/u/outlandish-test/phi_100m_swap folder.
"../y-cruncher v0.8.7.9547-static/y-cruncher" custom goldenratio \
  -dec:99999999 -hex:0 -od:1 -compress:0 -verify:1 \
  -mode:swap -TD:1 -PF:none -M:256m -swap:raid0 "$PWD/swap"
```

Later resource inspection:

```text
free -h:    Mem total 15 GiB; used 597 MiB; available ~14 GiB
            OS Swap 4.0 GiB, 0 used
 df -h /:   /dev/sdd ext4 1007G, used 722 MiB, available 955 GiB (at that checkpoint)
 du -sh:    /home/u/outlandish-test initially 274 MiB, later 294 MiB including an interrupted run
T: host free: approximately 2.90 TB, as previously reported
```

**Do not conflate the Linux OS's 4 GiB swap with y-cruncher's own disk-swap files.** The 1007G ext4 value is guest filesystem *capacity*, while the T: VHDX is a dynamically growing Windows host file; guest and host free space must both be checked for large jobs. VHDX capacity can be enlarged as a separate, explicitly reviewed operation if actually needed; do not change WSL memory or VHDX defaults pre-emptively.

### Accidental 10^10 run and containment

During a **resource-estimation-only interactive session**, the y-cruncher menu's `0` meant *Done* in a submenu but **Start Computation** on the main menu. An input/paste error accidentally started a **10-billion-digit φ** run on 7 November around 17:44 Adelaide time with **single enabled logical core**, `Task Decomposition: 1`, but only **79.7 MiB** total memory and the **default** swap directory. The owner immediately pressed `Ctrl+C`; shell prompt returned. Subsequent `pgrep -af y-cruncher` returned **no process**, and `df -h /` showed only about 21 MiB extra space used. A `du` inventory identified `.../y-cruncher v0.8.7.9547-static/ycs-0-0` occupying **21 MiB** (likely interrupted job scratch/checkpoint). Removal of this directory **was proposed after inspection, but actual deletion was not confirmed**. No result was completed, no G: production registry action occurred, and no evidence indicates damage to production binaries.

**Policy resulting from this incident:** Do not conduct further high-digit resource estimates through an error-prone interactive menu. Future WSL runner must have an explicit **preview-only default and opt-in execution gate**, printed effective digits/constant/mode/TD/framework/memory/swap/output/verification paths and space checks before any launch. When previewing a command manually, **never paste an executable `10^10` launch command into the shell**. A `--run`-type explicit execution gate is preferred. This is a proposed new control, not yet coded.

## 3. Measured/proposed 10-billion-digit golden-ratio settings

The experiment's counting convention is **total digit bytes INCLUDING the integer digit**. For φ:

- 10,000,000,000 numeric-byte output digits require y-cruncher **9,999,999,999 decimal places**, therefore `-dec:9999999999`.
- Use **Golden Ratio**, Newton's method, decimal plain-text output, no compression (`-compress:0`), decimal output (`-od:1`), hexadecimal output disabled (`-hex:0`). Preserve the correct known 32-digit prefix and entire prior 10^9 prefix during final Windows validation.
- Enable **y-cruncher's own output/base-conversion verification**, `-verify:1`, on Linux for large generations (unlike the old Windows pipeline's default `ycruncher_verify_output=false`). This supplies an additional check but not an absolute proof of mathematical correctness of all digits.
- **Swap Mode** (`-mode:swap`) with an **explicit, dedicated, pre-created ext4 swap folder** inside the T:-backed VHDX. Do not use the default path and do not use a Windows-mounted path for heavy far memory.
- Start with conservative **task decomposition 1**, **no multithreading framework** (`-TD:1 -PF:none` in the successfully tested small-run CLI); owner observed past hard host power-offs at higher native-Windows y-cruncher concurrency. These settings avoid the observed 24-logical-core defaults, though do not guarantee there are literally no helper threads. Do not raise concurrency automatically; any change requires the owner's decision and a separate measured safety/performance test.
- Proposed **total memory cap around 4 GB** (~3.73 GiB if decimal GB), rather than the interactive default **14.1 GiB** within WSL2's ~15.6 GiB limit. Treat 4 GB as a starting design value, **NOT a measured, validated final allocation**. There is substantial host/guest headroom in WSL2 at this cap. The exact command-line `-M:` value, effective cap and resource estimates must be validated in a **non-executing preview** before any substantial run. An earlier attempted interactive `4GB` input **did not successfully establish a 4-GB cap**; the accidental launch showed 79.7 MiB.
- Keep **checkpointing** and handling of partial results under review: do not assume that the theoretical `Largest: ~21.3 GiB` checkpoint size is additional required free space in every configuration, nor that a killed run can safely resume without y-cruncher's documented procedure and owner decision.

**Actual interactive y-cruncher estimates for 9,999,999,999 decimal places:**

| Configuration observed | Logical RAM | Logical temporary disk | Text output estimate | Largest checkpoint shown |
|---|---:|---:|---:|---:|
| RAM-only, all 24 logical processors (not safe/feasible here) | **41.0 GiB** | 0 | **17.0 GiB** | n/a |
| Swap, original all-core settings | **14.1 GiB** | **37.0 GiB** | **17.0 GiB** | **21.4 GiB** |
| Swap, after restricting to core 0 and TD=1 (before attempting memory cap) | **14.1 GiB** | **37.0 GiB** | **17.0 GiB** | **21.3 GiB** |
| Accidental launch after incorrect memory-menu input | **79.7 MiB displayed** | **37.0 GiB** | **17.0 GiB** | 21.3 GiB shown immediately before |

The values are **y-cruncher's upper-bound estimates** for the shown configurations, not measured peak disk traffic, not reliable duration forecasts, and **not a measured 4-GB configuration**. The tool itself states that runtime libraries, bookkeeping, OS RAM overhead, RAID overhead and certain other costs are excluded. Small real runs produced output text with precisely `N+1` bytes for `N` digits (decimal point), but the 17.0 GiB interactive 10^10 output estimate should be reserved conservatively until actual large-run behavior is measured. An exact canonical numeric-byte binary of 10^10 digits would be **10,000,000,000 bytes (~9.31 GiB)**; during Windows staging/conversion/registration multiple independent large files may coexist. Check **both T: and G:** available space and temporary buffer peaks rather than calculating space only from one output.

**No validated 10^10 wall-time or swap traffic estimate exists.** Do not extrapolate linearly from the 50-second 10^8 test or native-Windows 10^9 times. Larger computations may be dominated by far-memory I/O and FFT/multiplication, and the WSL2 VHDX is backed by a physical HDD. The only next permitted use of these estimates is planning/preview, not launching a ten-billion-digit computation.

## 4. Adopted architecture: Linux generation, Windows conversion/verification/registration

### 4.1 Separation of responsibilities

1. **New WSL-specific orchestration lives on E:** within `GAIS/OUTLANDISH_01/OUTLANDISH_WSL/` and can be run by Debian directly over `/mnt/e`. Prefer a small Bash adapter for Linux y-cruncher, and a small Windows-side adapter/test launcher when justified. `.py` scripts are acceptable on **Windows** using its existing Python; **Debian Python is not required** for the initial approach. Filenames such as `wsl_generate.sh`, `wsl_import.py`, `wsl_config.toml`, `test_wsl_integration.py` are design examples, **not files known to exist**. Do not fork/rewrite all five original Python modules.
2. **WSL-native computation and verification:** run static Linux y-cruncher from ext4; write temporary far-memory and decimal text to a unique, dedicated ext4 attempt directory. Require explicit `--run`/operator approval after a safe preview; do not let bare calls launch a 10^10 job. Capture y-cruncher version, exact options, report, exit code and digests; retain diagnostic reports and generate a manifest/receipt as a proposed design feature. Never claim this is implemented yet.
3. **Linux-to-Windows transfer:** Windows can read completed Linux files via `\\wsl.localhost\Debian\...`; for the initial workflow, **copy** (do not move/delete) the completed text into a controlled Windows staging directory. Hash the Linux source and Windows destination independently to detect transfer errors, verify expected byte count and constant provenance, and retain Linux source until successful independent Windows checks and explicit cleanup authorisation.
4. **Windows conversion on an isolated configuration:** use the existing `outlandish_big_constants.py convert` and `verify` routines, which enforce numeric-byte format, number of digits, known prefix and optionally a trusted reference. **The first 100-million-digit rehearsal is deliberately non-promoting**, because all active production constants are already 10^9 digits and registration requires strictly longer candidates. Use an isolated T: Windows artifact root/registry for rehearsal, not the live E: production TOML and G: files.
5. **Production validation (separate later permission):** once a future 10^10 candidate is complete, cross-check against the complete currently active 10^9 verified binary, independently reread/have SHA-256 evidence, then use existing `outlandish_artifacts.py register` **preview first** and only later `--apply --confirm-idle` after the owner's express approval. Keep the original 10^9 predecessor safe by deciding retention/backup policy *before* any promotion. Never activate this path for a 100m rehearsal.
6. **Results and scientific scanner** remain in the established Windows pipeline on G:, after successful registration and ordinary experimental governance. No reason to put lottery history or scanning/registries into Debian merely to generate the numerical digits.

### 4.2 Critical existing-code contract discovered in source review

The owner supplied `OUTLANDISH_01.zip` on 7 November; its inspected implementation contains `outlandish_big_constants.py`, `outlandish_artifacts.py`, `outlandish_config.py`, test suite, launchers, `outlandish.local.toml`, README and historical documents. Not all ZIP members are suitable to commit or distribute; it includes registry snapshot/state and the isolated preholdout CSV. **Use this ZIP as a source-review snapshot, not as authority to overwrite current E: files.**

- `outlandish_big_constants.py` already has `convert`, `verify`, and `pipeline` commands. `convert` accepts `--constant`, `--digits`, one or more `--input` files, `--output` and optional `--reference`; `verify` accepts `--input-file` and optional `--reference`. Both are useful separately without launching y-cruncher, and do **not** themselves register a candidate.
- `outlandish_artifacts.py register` already exists with mandatory `--constant`, `--source`, `--digits`, `--expected-sha256`, and optional `--apply`, `--confirm-idle`, `--delete-source`. It verifies the source/destination content, copies/publishes without overwriting, verifies the **entire prior active prefix** when replacing an existing active file, and atomically publishes state. `--expected-sha256` must be an independently recorded, trusted digest from an earlier verified step. **Registration preview does not promote.**
- **Important:** `outlandish_config.py` uses `WORKSPACE = Path(__file__).resolve().parent` and **`CONFIG_FILE = WORKSPACE / 'outlandish.local.toml'`**. Therefore simply adding `wsl_config.toml` under `OUTLANDISH_WSL/` **does not redirect** calls to the existing production modules. A safe isolated test requires a deliberate isolation mechanism (e.g. separate temporary T: Windows test workspace with copied small, unchanged modules and an isolated TOML; or a separately reviewed minimal config-path injection). Choose one, prove it with tests, and keep only **one authoritative editable source on E:**. A temporary test copy on T: is not a second maintained codebase.
- `convert`/`verify` require large explicit paths beneath the **configured artifact area**. Running them from the E: original source without isolation would resolve the live `G:\OUTLANDISH_01` root, not automatically the T: rehearsal root. Do **not** bypass link/junction, path containment or large-file audit restrictions to make the UNC path appear inside the root.
- The current production `[settings.retention] delete_superseded = true`. On successful real promotion, the verified former active 10^9 file may be automatically deleted **after** atomic state publication (with pending-retirement/recovery safety provisions). If preservation of the original 10^9 file is desired, establish a verified independent backup/retention arrangement and review settings before authorising production promotion; do not hand-edit generated registry state.
- An imported 100m binary is **shorter** than the existing 1e9 active φ file, so `register --apply` must not be called against the production registry. The test goal is conversion + independent binary verification + source/destination integrity; optional simulated registration belongs **only** in an isolated test registry with synthetic/prepared smaller predecessor.
- Preserve production scanner's 433 preholdout-only Powerball draws, drawn-order FIXED2 encoding and holdout firewall. Linux generation need not read any draw data.

### 4.3 Initial 100-million-digit rehearsal — **design, not yet executed**

- Create a tiny, reviewable adapter under E:`OUTLANDISH_WSL/`, with **no default destructive actions**. Use `/mnt/e/...` as the script path in Debian, but ext4 `~/outlandish-test/phi_100m_swap/Golden Ratio - Dec - Newton.txt` as the tested input source.
- Set up an isolated Windows T: test artifact root and matching **independent** user-configurable and generated TOML state; ensure no production G: outputs or original E: production TOML are written. Run existing code from a temporary isolated small-module copy if that is the chosen isolation method.
- Transfer the existing 100m decimal text with a recorded source SHA-256 and a new Windows destination SHA-256. The UNC source is accessible, as proven by owner `dir` output. Do not assume remote reads over UNC have the same durability/performance as ext4 local reads.
- Run existing text-to-numeric-byte conversion, then separately reread/verify the resulting **100,000,000-byte** `.bin`. Check known prefix, digit count, invalid bytes, digest and optional trusted short reference. Preserve originals; record elapsed time and throughput.
- Exercise read-only/preview safeguards and negative tests (wrong digit count, unexpected text headers, corrupted prefix, transfer mismatch, symlink/junction/refusal, no `--run` means no launch). No transfer-then-automatic-register behavior.
- Review results and inspect output paths before deciding whether a production 10^10 attempt is worth authorising. Only after a successful rehearsal should alternatives such as **Linux-side conversion** be benchmarked; that would be an explicit additional design, not an assumption that Linux `python3` or NumPy exists.

### 4.4 Resource / security / operational guardrails

- A proper dedicated swap folder must be selected using an explicit absolute ext4 path, not y-cruncher's `** Default Path **`; a unique per-attempt ID prevents collisions and makes failed job cleanup reviewable.
- Check process identity/existence and current sizes after any crash or Ctrl+C **before** deleting partial scratch. Prefer inspection of exact owned paths, never sweeping `rm -rf` over uncertain directories.
- All Windows tests remain non-destructive, use isolated T: state and have no production registry writes. Do not treat a local `outlandish.local.toml.bak` as backup of the 10^9/10^10 digit binaries.
- Distinguish **OS root privilege** from y-cruncher's harmless Linux thread-priority warning; calculations have passed without `sudo`. Do not add Windows `SeManageVolumePrivilege` while WSL2 is the preferred working route.
- Separate source review, preview, small rehearsal, owner approval of a 10^10 resource budget, actual run, post-run verification, **distinct promotion approval**, and scanning. Do not merge these into a single opaque or auto-destructive action.
- Large-file staging on T: and G: can use significant **simultaneous** capacity; plan for Linux decimal text, Linux swap, copied Windows text, temporary canonical binary, final imported binary and any deliberately retained 10^9 backup. WSL2's VHDX auto-expansion and future compaction behavior require host free-space checks; spare VHDX virtual capacity alone is not enough.
- If Linux generation proves impractical in real 10^10 conditions, **only then** revisit the owner's conditional, security-sensitive native-Windows `SeManageVolumePrivilege` fallback. Windows Sandbox and unrelated VM solutions are not the primary route.

## 5. Proposed minimal next implementation package (not yet written)

Use the established E: `OUTLANDISH_WSL/` directory for a small, self-contained **design document and scripts**. At minimum the proposed package should include:

| Proposed item (working title) | Purpose | Must NOT do by default |
|---|---|---|
| `README.md` | Describe environment, E/T/G boundary, prerequisites, safe preview/test/run usage, cleanup protocol and limitations | Present proposals as implemented behaviors |
| `wsl_generate.sh` | Linux-only wrapper around current static y-cruncher: show command, filesystems and resource requests; explicit execution opt-in; unique ext4 attempt folders; capture receipts | Start a large calculation through a normal preview or use default swap dir |
| `wsl_transfer_and_verify.py` **or** a Windows `.cmd` + Python pair | Copy completed Linux text from UNC to isolated T: Windows scratch; perform digest checks and call existing `convert`/`verify` | Load/publish production registry during initial rehearsal; overwrite files |
| `wsl_settings.toml` (template) | Non-secret paths and conservative defaults for WSL2; **not** a replacement for machine-maintained `outlandish.local.toml` | Contain production `[state.active]` or auto-promote switches |
| `test_wsl_integration.py` / smoke test script | Exercise exact T: isolation, refusal and no-promotion semantics using manageable small inputs | Use actual 10^9 G: binaries as writable test fixtures |

The exact names/languages can be simplified after inspecting the existing modules. **Do not add a full Linux Python install, duplicate registry, general-purpose orchestration framework, or administrative approval machinery without a concrete need.** If the toolchain remains Linux y-cruncher + Windows Python, the Windows side can reuse the already-installed Windows NumPy but need not install it in Debian.

**Decisions not yet made:** final isolated-Windows module/config loading mechanism; exact data transfer placement and evidence format; supported failure/retry semantics; final 4-GB memory CLI spelling and non-executing validation; duration limits/checkpoint policy; whether Windows conversion is efficient enough at 10^10 or Linux-side conversion is warranted; retaining/verifying previous 10^9 originals on later promotion; any 10^10 production launch. These must not be silently marked complete.

## 6. Immediate next safe actions

1. **Prepare/review the thin WSL integration design and test source** in `E:\...\OUTLANDISH_01\OUTLANDISH_WSL\`, using the supplied current Windows code snapshot as reference. Limit the first implementation to the 100m test input and a T: isolated Windows artifact root. Do not touch the six G: active binaries.
2. Add a **default dry-run / preview** for WSL launch and Windows transfer, with explicit large-run opt-in, strict non-overwrite, unique filenames, and refusal of unintended production registry access.
3. Complete a **single 100-million-digit φ** cross-OS conversion and verification rehearsal, using the already verified Linux decimal text. Check hashes, known prefix, exact binary byte length and full readback; no registry promotion.
4. Benchmark copying/converting that file enough to make an informed architecture choice; decide if the initial Windows-only conversion route is sufficiently economical for 10^10.
5. Before any large calculation, inspect live WSL/T:/G: space, actual y-cruncher 4-GB cap settings in an **execution-disabled preview**, filesystem safety, progress logging, verified predecessor preservation and owner-authorised running parameters. Defer speculative throughput extrapolation.

**New-conversation opening request:**

> Continue the standalone OUTLANDISH_01 study from `OUTLANDISH_01_2026-11-07_Project_Status_and_WSL2_Primary_Design_v3.md`. The primary design is now Debian/WSL2 Linux static y-cruncher generating decimal text in T:-backed ext4, with **all new WSL-specific code and config templates in E:/GAIS/OUTLANDISH_01/OUTLANDISH_WSL** and existing Windows conversion, validation and eventual G: registration reused. WSL2 has passed 100k RAM and 1m/10m/100m verified swap runs. No Debian Python is installed or needed for the initial thin adapter. Source-review ZIP dated 7 Nov includes current v0.2r4 modules and a TOML with six registered 10^9 files. First design a non-destructive T:-isolated Windows conversion/verification rehearsal using the existing 100m φ Linux output. Be alert: existing `outlandish_config.CONFIG_FILE` is fixed relative to its module; a WSL TOML elsewhere will not redirect it automatically. Do not launch 10^10 work, use a WSL interactive menu for estimates, modify the production G: registry, or touch holdout data.

---

# Part II — retained earlier baseline and Windows Sandbox evidence (historical)

The sections below are preserved substantially from the 7-November v2 handover to avoid losing technical details, safety rationale or evidence. **They describe the state *before* WSL2 installation and should not be read as current instructions where they say WSL is merely planned or name v2 as the latest handover.** Part I is the current authority for next actions and architecture; current source/TOML remain authoritative for implementation.

## 1. Project identity, scope and division of work

- GitHub repository: `https://github.com/hydra3333/analysing_perceived_randomness_in_reality`.
- OUTLANDISH source directory **now**: `GAIS/OUTLANDISH_01/` at repository root, not the former `src/GAIS/OUTLANDISH_01/`.
- Primary host: Windows 11; Ryzen 9 3900X (12 physical / 24 logical processors), 32 GiB RAM. Repository and main project virtual environment live on E:; large digit data and OUTLANDISH run artifacts live on G:; T: is a separate WD Black HDD with substantial space, reserved for possible WSL/Sandbox trials.
- OUTLANDISH_01 is an **independent, speculative mathematical-constant digit-stream thought experiment**. It is not the governed E_1..E_62 main predictive-randomness method suite, and it does **not** demonstrate lottery predictability. It nonetheless preserves the independent pre-holdout dataset and does not inspect held-out outcomes in development.
- The owner has authorised direct development/testing of this standalone OUTLANDISH workstream; do **not** infer authority to change the main research project's methods, orchestration, scientific gates, or held-out data.
- The owner strongly prefers pragmatic, reviewable implementations, precise claims, no fabricated runtimes or verification, and command-line procedures appropriate to Windows CMD. Code/diagnostic changes should be isolated and should not unnecessarily proliferate administrative machinery.

## 2. Established pre-Sandbox implementation: what is already in place

### 2.1 Main files and roles

Located under `GAIS/OUTLANDISH_01/` unless stated otherwise:

| File | Role |
|---|---|
| `outlandish_big_constants.py` | Native-Windows y-cruncher launcher, digit conversion, verification and registered `pipeline`; supports previews and explicit `--run`. |
| `outlandish_artifacts.py` | Shared artifact paths, pre/postflight safeguards, active-digit registry, verification, promotion, locking, retirement and recovery. Installed version reported as **v0.2r4**. |
| `outlandish_config.py` | TOML parsing / configuration helpers. |
| `outlandish_powerball_stage_a.py` | Fixed-width, NumPy-vectorised digit scanning and reports for the Powerball historical pre-holdout dataset. |
| `test_outlandish_v02.py` | Standalone regression tests and synthetic safety cases. |
| `outlandish.local.toml` | **Intentionally Git-tracked** local configuration **and machine-maintained active-digit registry**. User section may be edited deliberately; generated state must not be hand-edited. |
| `POWERBALL_preholdout_only.csv` | Pre-holdout-only development data; not a live-results fetcher. |
| `OUTLANDISH_01_v0_2_README.md`, `README.md` | Operational reference; inspect the installed version before relying on old handover excerpts. |
| `generate_1e10.cmd`, `scan_1e9.cmd`, `scan_1e10.cmd` | Convenience launchers; check their current contents and preview semantics before running. |
| `y-cruncher v0.8.7.9547b/` | Local Windows y-cruncher installation, **ignored by Git**. Contains binaries/libraries. |
| `ycruncher_digits/` | Legacy local folder; ignored, not the active large-artifact root. |

The historical standalone handover spec, old v0.1/v0.2 installers and earlier 10^10 README versions are **not** superior to the installed v0.2r4 code, TOML and README. Some older text predates G: relocation, automatic retirement, and the new GAIS root path.

### 2.2 Six constant streams and encoding

| CLI ID | Constant | First digits (decimal point shown for explanation only) |
|---|---|---|
| `pi` | π | `3.1415926535...` |
| `phi` | Golden ratio | `1.6180339887...` |
| `e` | e | `2.7182818284...` |
| `log2` | ln 2 | `0.6931471805...` |
| `gamma` | Euler–Mascheroni γ | `0.5772156649...` |
| `lemniscate` | **Half-perimeter** lemniscate constant | `2.6220575542...` |

Each output file contains **one numeric byte 0–9 per decimal digit** (NOT ASCII `'0'`–`'9'`), beginning with the integer digit and containing **no decimal point**. Thus a `10^9` file has exactly 1,000,000,000 bytes; a `10^10` file will have 10,000,000,000 bytes.

**Lemniscate convention matters:** the y-cruncher built-in source returns approximately `5.244115...` (full perimeter). The OUTLANDISH Python converter applies an exact streaming division by 2 to obtain the chosen `2.622057...` stream before verification and registration. Do not silently change this convention.

### 2.3 Existing large-file state, G:

The owner reported that **all six** constants had successfully completed native-Windows RAM-only pipelines to **10^9 digits each** by the end of 2026-11-06. The six 1,000,000,000-byte binaries were verified and registered active; no pending retirements remained at that checkpoint. This is **owner-reported and previously checked in conversation**, not freshly revalidated by this handover.

Established live artifact parent:

```text
G:\OUTLANDISH_01\large_artifacts\
    digits\       six registered, verified 10^9 numeric-byte binaries
    scratch\      calculation attempts, retained small reports
    staging\      in-progress candidates
    results\      scanner reports
    logs\         receipts and diagnostics
```

Important controls:

- Read the current `outlandish.local.toml` and run `python outlandish_artifacts.py status` / `audit` before new operations. Its `[state.active]` and `[state.pending_retirement]` are **program-generated; do not manually edit**. A `.toml.bak` is only the previous registry snapshot, **not** a backup of the big binaries.
- Live owner policy: `[settings.retention] delete_superseded = true`. In **v0.2r4**, after successful replacement validation and an atomic state publication, precisely the verified predecessor may be auto-retired. This is **not** an authorisation to manually delete files or bypass lock/identity checks. Third-party readers must be idle.
- Registered active files must be strictly extended; a second same-length `pipeline` is not an appropriate test. Full previous-prefix comparison is required for promotion. On handled failures, owned large scratch/intermediates are cleaned but small error evidence remains; crashes may leave recovery material.
- The output location and generated-large-file audits are important. The old project had an accidental history of large generated files under Git-tracked paths; that has been corrected. Large files should not be reintroduced into Git.
- The root `.gitignore` covers OUTLANDISH large artifacts and local y-cruncher, including `/GAIS/**/*.bin`, `/GAIS/OUTLANDISH_01/y-cruncher v0.8.7.9547b/`, and `/GAIS/OUTLANDISH_01/ycruncher_digits/`. Confirm the latest ignored-root entry in the current repository if relevant.

### 2.4 Known native-Windows execution characteristics

- Installed y-cruncher version: `v0.8.7.9547b`.
- Owner observed actual **hard instantaneous power-offs** under some higher-concurrency y-cruncher settings. `-TD:4` was used for the established stable runs and is the cautious default for follow-up tests. **`-TD:4` sets y-cruncher's task decomposition, not a strict four-OS-thread/core cap**; observed CPU usage can exceed four cores. Do not raise it automatically or suggest stress tests to find a failure threshold.
- With `[settings.generator] mode = 'auto'`, the installed implementation selects RAM mode for inputs **below** 5 billion digits and disk-swap mode at/above that boundary. `[settings.generator] memory_gib` concerns requested working memory in swap mode, **not** a RAM cap for normal RAM-only calculations.
- The live `[settings.generator]` values must be read from current TOML; historical README examples vary (`threads = 4` and `threads = 12` both appear in different explanatory contexts). Do not infer current live settings from a README example.
- `ycruncher_verify_output = false` was selected in the newer pipeline for speed. Python format, reference-prefix and full SHA-256 checks remain, but **do not independently re-prove newly computed mathematical digits**. Preserve this limitation in scientific claims.
- Owner-supplied order-of-magnitude 10^9 generator observations: `phi` ~15 s y-cruncher; `e` ~44 s; `pi` ~71 s; `log2` ~180 s; `gamma` ~2,447 s (~41 min); lemniscate on the scale of minutes. These are individual observed runs, **not** credible extrapolations to 10^10/10^11 disk-backed computation.

### 2.5 Tests and evidence

Earlier native-Windows owner test run of `test_outlandish_v02.py`: **25 tests total**, 24 PASS and one allowed symlink skip. Separate generator/scanner self-tests existed. The full set of real 10^9 promotions was reported complete and the project committed/pushed; no 10^10 real run has been demonstrated.

`status` reflects registry metadata; `audit` checks path/placement/symlink/large-file safety. Neither substitutes for a **new** full-byte verification of every binary. Full-source digest verification happens in the relevant pipeline/whole-active-file scan paths.

## 3. Established Stage-A Powerball exploration

- Historical Powerball **pre-holdout only**: **433 draws, draw numbers 1144–1576**, cutoff exclusive `1577`. No later draws in development scans.
- Each selected ball is exactly two decimal digits (`03`, `12`, etc.). Search scans **every possible digit-byte offset**, including odd alignment and chunk boundaries.
- Pattern definitions:
  - **P1:** all seven main numbers in operator-drawn order, plus Powerball.
  - **P2:** all seven main numbers in operator-drawn order.
  - **P3:** any six distinct main numbers in any order, plus Powerball.
- A measured **π 10^9** run with `chunk_bytes = 4,000,000` took **27.278917 s** of scan time, yielding **P1=0, P2=0, P3=29**. This result is descriptive only, not evidence of causal structure or predictive power. A one-trillion-byte scan estimate based on it is merely a rough scan-only extrapolation, not a generation forecast.
- Scans use the OUTLANDISH-only historical CSV and do not pool games or consult future/holdout outcomes. The various other-constant scan statuses and report results should be read from the actual reports rather than assumed complete from the existence of six digit binaries.

## 4. Pre-Sandbox open problem: moving from 10^9 to 10^10 (possibly 10^11)

### 4.1 Windows y-cruncher disk-swap privilege obstacle

A 10^10 computation generally exceeds the comfortable 32 GiB RAM-only budget, making y-cruncher's **disk-backed swap mode** necessary. On native Windows, y-cruncher requested **`SeManageVolumePrivilege`** (“Perform volume maintenance tasks”) to use `SetFileValidData()` when preparing large swap files. A conventional non-elevated user did not have the needed privilege. The exact y-cruncher command / performance and safe swap-mode operation remain **untested for a substantive real 10^10 calculation**.

This privilege is security-sensitive and is **not restricted merely to T: or G:**. Do not casually grant it to the everyday user or change system policy. The owner considered a temporary grant/relogin/revoke sequence, but deferred it, preferring a potentially safer Linux route. No authorisation to alter this privilege has been given in this handover.

### 4.2 Research on replacement external-memory numerical engines

The owner sought a **mature, reusable** alternative capable of 10^10–10^11 digits, not a new numerical-HPC software project. Research included FLINT/Arb, python-flint, GMP, apfloat, TachusPI, binary splitting, external-memory FFT, and specialized constant algorithms. An external AI's initial report contained substantial errors and overconfident predictions; a requested correction concluded **NO-GO for a new independent engine**, **GO for further y-cruncher evaluation**. The corrected conclusion is a research judgment, **not** proof that no alternative can work. A function that streams a slice of output still may require enormous RAM to compute the preceding digits.

### 4.3 Historical pre-WSL planning notes — superseded by current results

Before diverting to Windows Sandbox, the preferred next *exploratory* route was the **Linux edition of y-cruncher under Debian/WSL2**, potentially avoiding Windows's `SetFileValidData()` requirement.

Known WSL host observations at that time:

```text
WSL version 2.5.7.0; kernel 6.6.87.1-1
Default WSL version: 2
No Linux distributions installed
```

The owner selected **Debian** rather than Ubuntu. Intended *host* area: `T:\OUTLANDISH_WSL\Debian\` holding the guest ext4 VHDX and Linux-side y-cruncher/swap scratch, without repartitioning or formatting T:. The six active result binaries remain on **G:**. Host T: was reported to have approximately **2.62 TB free** at the time; verify current free space before allocating anything.

Important planned controls:

- Complete the owner's **comprehensive backups and recovery-media checks** before Linux installation, privilege edits, disk-layout work, or heavy stress tests. The exact **current** backup completion status should be confirmed with owner; do not infer it from this handover.
- Before WSL installation set/inspect `.wslconfig` memory and WSL **VM swap-file location**, which otherwise may use C:. Beware of WSL virtual-disk max size and dynamic VHDX growth; verify current Microsoft guidance rather than assuming 2.62 TB is automatically addressable.
- Test Linux y-cruncher CLI and external-memory scratch on the ext4 filesystem. `/mnt/t` Windows/WSL cross-filesystem I/O is not equivalent to native ext4 random I/O and may be much slower. Preserve established converter, verification and registry contracts; a **new** Linux-runner integration is not installed.
- Start with a small Linux execution smoke test, then a calculation proven to exercise swap (small 10^5/10^6 calculations may not), then evaluate storage, speed and safety. No guessed runtimes for 10^10 or 10^11.
- `wsl --unregister Debian` would **delete** the Debian guest/data. Do not use casual cleanup commands against a live guest or running computation.

### 4.4 Remaining work (historical pre-Sandbox list; updated current plan in §7)

1. Protect the existing production source/TOML and six verified G: binaries; confirm backup/recovery readiness.
2. Establish a controlled, genuinely disk-backed y-cruncher execution mode (Debian/WSL2 was preferred; native Windows temporary privilege only with explicit owner decision; Windows Sandbox has now been abandoned as an unsuccessful test environment).
3. Verify scratch/data placement, required temporary capacity, runtime characteristics, bounded concurrency, log evidence, and uninterrupted/restorable behaviour before long calculations.
4. Assess feasibility and resource budgeting **per constant**, particularly much slower `gamma`; don't jump directly to six 10^10 calculations or extrapolate RAM-mode timings.
5. Integrate, if necessary, a reviewed Linux / external-swap generation adapter feeding **the same numeric-byte, verified, registered files** on G:, with safe restart/cleanup semantics. Do not bypass the existing content and predecessor-prefix integrity checks.
6. Only then generate larger numbers and use the pre-holdout scanner; interpret matches with chance baselines and guard against exploratory overfitting.

## 5. Safe baseline commands on the original Windows project

These commands are for the original **native project** with its actual project-root `.venv` activated, executed from `GAIS\OUTLANDISH_01`. They are **not** an instruction to run now without reviewing state. Commands without `--run` do not start the real generator.

```bat
python outlandish_artifacts.py validate
python outlandish_artifacts.py paths
python outlandish_artifacts.py status
python outlandish_artifacts.py audit
python outlandish_big_constants.py self-test
python outlandish_powerball_stage_a.py self-test
python test_outlandish_v02.py
python outlandish_big_constants.py pipeline --constant pi --digits 10000000000
```

Do not issue the final command with `--run` until swap privilege/WSL adapter, storage, disk budget, safety and owner approval have been addressed. In particular, never run an unverified same-length `10^9` promotion against an already active 10^9 binary.

## 6. Repository and evidence boundary

The Git repository underwent a **completed** GAIS relocation and targeted history rewrite on 2026-11-06. Its authoritative record is under `exchange/HISTORY_CLEANUP_2026_11_06/` (including `CLOSEOUT.md` and `commit-map.txt`). Old references to `src/GAIS` and old pre-rewrite Git SHAs in earlier records are historical, **not** necessarily current locations or commit identities. Handover material from before v0.2r4 must not be read as the latest code state. The owner reported a committed, pushed clean state for OUTLANDISH after the six 10^9 files were established, but the new chat should inspect actual status rather than assuming today's working tree is unchanged.

---



---

## Historical Appendix A — Completed Windows Sandbox experiment: configuration and scope

**Purpose:** Test the Windows y-cruncher/OUTLANDISH pipeline on `10^5 = 100,000` golden-ratio digits in an isolated disposable Windows Sandbox, with copied source on T: and scratch/results under a separate T: data tree. Goal was to avoid native Windows's disk-swap privilege at larger sizes. **Outcome: the real test never computed digits; Windows y-cruncher failed at process load time.** This appendix is forensic/historical. Its T: files were being deleted at owner's decision and should not be presumed available.

## A.1 Snapshot of host-to-guest setup (historical, not to recreate by default)

```text
HOST (T:)
T:\OUTLANDISH_01_SANDBOX\                 copied stand-alone source, local y-cruncher, PYTHON/, SANDBOX/
  PYTHON\python-3.15.2-amd64.exe         installer
  PYTHON\000-Pip-Install-Dependencies.bat   owner's full dependency BAT (v5 later edited for compiler)
  SANDBOX\OUTLANDISH_01_sandbox.wsb
  SANDBOX\OUTLANDISH_01_Setup.bat
  SANDBOX\OUTLANDISH_01_Install_Persistent_Python_MANUAL.bat
  SANDBOX\OUTLANDISH_01_Python_Env.bat
T:\OUTLANDISH_01_SANDBOX_DATA\            writable test-data tree
  python_candidate\Python315\          installed Python and pip; persisted between guest restarts
  outlandish_run\large_artifacts\     separate scientific data root

GUEST
C:\HOST_OUTLANDISH_SOURCE\          read-only mapping of first T: tree
C:\HOST_OUTLANDISH_DATA\            writable mapping of second T: tree
C:\HOST_SOFTWARE\                  read-only host software/Notepad++ mapping
C:\OUTLANDISH_WORK\                disposable cloned source, y-cruncher, test TOML
```

The .wsb mapped folders correctly. GUI and user preferences were re-applied by startup, while the guest C: filesystem, Windows registry and installed system toolchains were discarded on closing Sandbox. The host-mapped T: data retained any changes made there, including pip updates and installed binaries. **Never confuse this with isolation from the host writable folder.**

The owner originally had nine Explorer registry preferences, a Notepad++ context-menu integration and desktop shortcuts; early assistant setup packages inadvertently removed them, then restored them. Explorer **compact view** (`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\UseCompactMode = 1`) was explicitly added. Three shortcuts were verified:

```text
HOST_software.lnk
HOST_OUTLANDISH_01.lnk
HOST_OUTLANDISH_DATA.lnk
```

The first `.bat` used VBScript through `cscript` and failed because the guest lacked a `.vbs` script engine; PowerShell with `WScript.Shell` COM `CreateShortcut` succeeded. A subsequent automatic setup with **no pauses**, logging and no Python install passed all five startup stages. Manual scripts were separate and allowed diagnostic pauses. **No files or settings in the T: Sandbox test should be installed into E: production.**

## A.2 Python on ephemeral C: — extremely slow and ultimately invalid

A Windows Sandbox guest ran Python installer `python-3.15.2-amd64.exe` (owner-selected **per-user** standard location, PATH on, without documentation, Tcl/Tk/IDLE, Python test suite or standard-library precompilation). The installer took an unusually long time. The initially successful test reported:

```text
C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python315\python.exe
size: 105,696 bytes
Python 3.15.2
pip 26.2.2
```

Existing CMD didn't pick up new PATH until the owner explicitly added Python315 and `Scripts` directories. The original full pip BAT later produced Windows's blue **"This app cannot run on your PC"** popup, pip launcher failure and `Access is denied`. At 10:36 local, `dir` reported **`python.exe` = 0 bytes**. `certutil -hashfile` failed with `0x800703EE` / Win32 1006 `ERROR_FILE_INVALID` (*"volume ... externally altered ... opened file ... no longer valid"*). This proves an invalid executable, **not its cause**. The exact process that truncated or invalidated the file was never identified. Do **not** infer host T:/G: corruption from it.

System event query for IDs 55/98/153/7 returned `Microsoft-Windows-Kernel-Processor-Power` Event 55 (**informational CPU power-management capability**), not NTFS disk corruption. Defender Operational queries for events 1116/1117 returned no output; no Code Integrity enforcement event was established. An empty or broad event query cannot prove the absence of relevant security or volume events.

## A.3 Persistent Python on T: — demonstrated feasible

A later candidate used Windows Python installer's documented `TargetDir` to install once under:

```text
C:\HOST_OUTLANDISH_DATA\python_candidate\Python315
(Host: T:\OUTLANDISH_01_SANDBOX_DATA\python_candidate\Python315)
```

Python installation returned **exit code 0** with the owner's requested exclusions. Direct startup and `-m pip` worked; its `sys.prefix` and `pip` `Lib\site-packages` both resolved within the T: mapped tree. A baseline SHA-256 was saved. A fresh Sandbox restart **independently passed** the provided `VERIFY` phase. Another restart after substantial dependency updates also passed:

```text
Python 3.15.2
pip 26.3
sys.prefix = C:\HOST_OUTLANDISH_DATA\python_candidate\Python315
site-packages = C:\HOST_OUTLANDISH_DATA\python_candidate\Python315\Lib\site-packages
```

`numpy` imported successfully at version **2.5.4**, and owner reports also confirmed Scipy/pandas imports in dependency checks. This is a *real positive result*: a Python installation and packages **can** remain usable across Windows Sandbox restarts when the guest mapping path is stable. The path used for temporary downloads/builds was under `%TEMP%` (disposable C:), which does **not** mean pip's final installation went there. This positive result **did not fix the y-cruncher launch failure** and is not a recommendation to retain Sandbox.

## A.4 Full owner dependency BAT: not required for OUTLANDISH smoke; compiler failure

The owner's original `PYTHON\000-Pip-Install-Dependencies.bat` requested many upgrades, `--upgrade-strategy eager`, `pip-review --auto`, and packages not used by OUTLANDISH. It also contained a bad `python -m python -m pipdeptree` command, which a later draft proposed correcting. The owner expressly wanted the original package list preserved; early assistant NumPy-only substitutions were rejected. One replacement v5 included compiler installation/prerequisites and fail-fast pip error tracking, but this was a Sandbox-only candidate, **not** part of the main project requirements.

A supplied pip log of 1,605 lines showed **six build failures for five distinct packages**:

| Package | Attempts failed | Interpretation |
|---|---:|---|
| PyYAML | 2 | Compiled extension build attempted; missing MSVC toolchain |
| inflate64 | 1 | Compiled archive dependency; missing compiler |
| pybcj | 1 | Compiled archive dependency; missing compiler |
| pyppmd | 1 | Compiled archive dependency; missing compiler |
| pyahocorasick | 1 | Compiled pattern-matching extension; missing compiler |

Representative error:

```text
error: Microsoft Visual C++ 14.0 or greater is required.
Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**This is not a VC++ Redistributable runtime failure.** These packages fell back to compiling from source on Python 3.15 because suitable wheels were unavailable/unsuitable at the time. Many other packages, including NumPy 2.5.4, SciPy and pandas, were usable. OUTLANDISH's scanner uses NumPy; generation is primarily standard-library Python plus external y-cruncher. The five failed packages were **not a demonstrated prerequisite** of the `10^5` OUTLANDISH test.

Attempted Build Tools installer (`vs_BuildTools.exe`) ran the Visual Studio Installer on Sandbox disposable C: and made very slow progress, **stalled at 35% / package 149 of 268**, and was abandoned by closing the entire Sandbox. That is an **abandoned incomplete install**, not proof that Microsoft's toolchain would never install. No completed compiler toolchain survived the guest restart. The owner decided not to spend further effort on full dependency/toolchain installation.

## A.5 OUTLANDISH smoke tests: 25 tests individually accounted for

After the successful persistent Python setup and source copy, the complete Python suite ran:

```text
Ran 25 tests in 51.830s
24 passed ('ok'), 1 ERROR: test_all_launchers_use_manifest_not_hardcoded_drive
FileNotFoundError: C:\OUTLANDISH_WORK\scan_1e9.cmd
```

The failure was **packaging**, not computation: the startup copy routine omitted the three launcher `.cmd` files. The owner copied `scan_1e9.cmd`, `scan_1e10.cmd`, `generate_1e10.cmd` from read-only source to C: worktree and reran the one failing test:

```text
Ran 1 test in 0.013s
OK
```

Therefore **each of the 25 tests passed in aggregate**, but a full 25-test run was **not repeated after copying**. Do not misreport a single clean 25/25 suite execution. The full suite was slow (~52 s) in the mapped persistent Python environment; this does not directly measure numeric calculation performance.

## A.6 Artifact audit and correct test data root

The original clean test TOML had:

```toml
[settings.storage]
main_root = 'C:\HOST_OUTLANDISH_DATA'
```

OUTLANDISH's audit correctly identified **eight unsafe misplaced entries** within `python_candidate`, including large NumPy/SciPy DLLs (`~20 MB`) and `chardet` `.bin` model files. The audit was working as specified; the configuration wrongly placed **all persistent Python files beneath a scientific-artifact-scanned root**. Nothing was deleted and audit rules were not bypassed.

The owner fixed only the test TOML and created a separate root:

```toml
[settings.storage]
main_root = 'C:\HOST_OUTLANDISH_DATA\outlandish_run'
```

```text
T:\OUTLANDISH_01_SANDBOX_DATA\
   python_candidate\Python315\        (outside the audit root)
   outlandish_run\large_artifacts\    (scientific-only subtree)
```

Then:

```text
ARTIFACT AUDIT PASS (standalone audit): no misplaced generated/large files
CONFIG C:\OUTLANDISH_WORK\outlandish.local.toml root=C:\HOST_OUTLANDISH_DATA\outlandish_run
pi/phi/e/log2/gamma/lemniscate: active=NONE pending_retire=NONE
```

The generator's `phi --digits 100000` **dry run passed**, reporting the exact CLI and `-TD:4`:

```text
[phi] TARGET: 100,000 digits INCLUDING integer digit.
[phi] MODE=RAM THREADS_REQUESTED=4 (TD task decomposition, not strict OS thread count)
[phi] COMMAND: "C:\OUTLANDISH_WORK\y-cruncher v0.8.7.9547b\y-cruncher.exe" custom goldenratio -dec:99999 -hex:0 -od:1 -compress:0 -verify:0 -mode:ram -TD:4 -PF:taskqueue
[phi] DRY RUN: nothing launched or modified.
ARTIFACT AUDIT PASS (post-run): no misplaced generated/large files
```

The `-dec:99999` argument yields exactly **100,000 digits including the integer digit**. This was a correct preview and does **not** mean the actual digit output existed.

## A.7 Actual y-cruncher invocation: launch failure, no generated digits

The owner then ran:

```bat
python outlandish_big_constants.py pipeline --constant phi --digits 100000 --run
```

It completed only the safe Python preflight and y-cruncher launch step. y-cruncher immediately failed:

```text
[phi] y-cruncher exit code=3221225595; wall=0.1s
[phi] FAILURE CLEANUP: removed 0 failed-run data file(s); kept small reports
ARTIFACT AUDIT PASS (post-run / error-path): no misplaced generated/large files
ERROR: y-cruncher exit 3221225595
```

**Interpretation:** `3221225595` (unsigned) and `-1073741701` (signed) are both `0xC000007B`, Windows `STATUS_INVALID_IMAGE_FORMAT`. Likely failure to load an executable image or dependency/DLL. That code is not a mathematical failure, Python artifact-registry failure or disk-swap privilege failure. Its **specific cause was not determined**.

Direct execution of `C:\OUTLANDISH_WORK\y-cruncher v0.8.7.9547b\y-cruncher.exe` likewise printed nothing and returned `-1073741701`. Given the very recent y-cruncher Windows launcher and suspected runtime dependency, the owner attempted the official Microsoft VC++ **x64 Redistributable** (`vc_redist.x64.exe`) from the source SANDBOX mapped folder. Its installation appeared very slow; it was launched with `start` (asynchronous), and **successful installation was never conclusively verified**. Running y-cruncher afterwards still produced `0xC000007B`. Do **not** claim the correct Redistributable was definitely installed and failed to fix it; equally do not claim that `STATUS_INVALID_IMAGE_FORMAT` proves a missing runtime is the sole cause.

This is the decisive failure of the Sandbox experiment. The zero-byte ephemeral C: Python issue was separate; the **persistent Python actually worked well enough for all Python tests and checks**. Running the same Windows y-cruncher natively outside Sandbox had previously succeeded at 10^9 digits, so the obstacle is specific to this test guest/toolchain combination, but exact cause remains unproven.

## A.8 Operational disposition

- Owner judged Windows Sandbox not worth further effort and is deleting `T:\OUTLANDISH_01_SANDBOX\` and `T:\OUTLANDISH_01_SANDBOX_DATA\`, plus redundant Sandbox source-copy material on E: (exact deletion completion **not verified**).
- Any `.wsb`, copied production registry, persistent Python candidate, compiler bootstrappers and interim result logs within those trees are **temporary failed-test material**, not needed for ongoing OUTLANDISH operation. Do **not** delete G: active artifacts or E: working source.
- The guest test TOML had **no active registered constants**; the production registry on E: and verified six G: 10^9 files were not involved in a real Sandbox pipeline run.
- Retain narrative evidence in this handover. No future chat should propose spending more time on Sandbox as the default next step.

---

## Historical Appendix B — Explanation of Windows Sandbox errors and limits of findings

| Symptom / output | What is established | What is *not* established |
|---|---|---|
| Silent/slow classic Python MSI installation | The owner observed extreme delays; Python eventually launched once on ephemeral C: | Exact responsible security policy; whether installing to T: resolves guest filesystem cause |
| `python.exe` = 0 bytes and `certutil 0x800703EE` | Guest C: executable was unusable after pip attempts | Root cause; host disk damage or driver fault |
| `cscript` no `.vbs` engine | Original shortcut creation couldn't execute | Whether all scripting methods fail (PowerShell COM succeeded) |
| Missing C++ 14+ while building PyYAML etc | Wheels fell back to source builds requiring MSVC compiler | Need for Visual C++ **runtime** or all packages to run OUTLANDISH |
| Visual Studio installer 35% / 149 of 268 | An expensive guest-C: compiler install stalled and was abandoned | That compiler *could never* complete on a normal machine |
| Eight artifact audit violations under `python_candidate` | Scientific scan root was overly broad | Corruption/misplacement of genuine scientific output |
| `0xC000007B` from y-cruncher | Windows guest couldn't load y-cruncher image/dependency | Which DLL failed, a y-cruncher algorithm bug, a `10^10` swap problem, or proof runtime redist succeeded |
| Power-management provider Event 55 logs | CPU capabilities enumerated at guest startup | NTFS file corruption or host disk errors |

**Relevant background research retained from previous conversation (7 Nov 2026):**

- Microsoft Windows Sandbox slow-MSI issues and trust verification: https://github.com/microsoft/Windows-Sandbox/issues/85 and https://github.com/microsoft/Windows-Sandbox/issues/68. These are relevant to extreme installation time, not proven causes of zero-byte `python.exe` or `0xC000007B`.
- Microsoft Q&A slow Python install in Sandbox: https://learn.microsoft.com/en-us/answers/questions/3898205/the-setup-process-performance-inside-windows-sandb
- Microsoft Sandbox configuration and mapping semantics: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file
- Windows error 1006 `ERROR_FILE_INVALID`: https://learn.microsoft.com/openspecs/windows_protocols/ms-erref/18d8fbe8-a967-4f1c-ae50-99ca8e491d2d
- Windows `STATUS_INVALID_IMAGE_FORMAT` code and y-cruncher Windows launcher notes were discussed in chat; recheck official release notes and dependency diagnostics if ever revisiting, but owner has closed Sandbox path.

---

## Historical Appendix C — Historical handover filenames and their proper authority

The E: folder listing on 7 November contained these three documents (before owner agreed to clearer filenames). The following **renames were recommended; actual renaming was not independently verified**:

| Original | Suggested new name | What it represents |
|---|---|---|
| `OUTLANDISH_01_Standalone_Handover_Spec_v0_1.md` | `OUTLANDISH_01_2026-11-05_Historical_Status_and_Draft_Spec_v0_1.md` | **5 Nov historical** early two-constant status, proposed Oz Lotto work, coding and experiment specification. Not latest implementation. |
| `OUTLANDISH_01_Standalone_Handover_Bundle_v0_1.zip` | `OUTLANDISH_01_2026-11-05_Historical_Source_and_Evidence_Bundle_v0_1.zip` | **5 Nov evidence bundle** accompanying the early handover; historical code/results snapshot, not current release. |
| `OUTLANDISH_01_Handover_2026-11-07_v1.md` | `OUTLANDISH_01_2026-11-07_Project_Status_and_Early_Sandbox_Diagnostics_v1.md` | **7 Nov early checkpoint**, pre-final Sandbox, before persistent T: Python verification and y-cruncher load failure. Superseded as conversation handover by this v2. |

**This document:** `OUTLANDISH_01_2026-11-07_Project_Status_and_Sandbox_Final_Closure_v2.md` is the **most current consolidated AI-to-AI conversation handover**. It is a guide, not a replacement for installed source code, actual live TOML, current repository README or original scientific evidence. Keep the historical files for provenance, but don't follow their obsolete paths and operational assumptions without checking current source.

---


---

## Provenance, limitations and document history

- Direct user-reported WSL/Windows console transcripts on **7 November 2026** establish the running Debian version, T:-backed VHDX, successful static Linux y-cruncher 100k/1m/10m/100m commands and timings, source-file visibility via `\\wsl.localhost`, estimated 10^10 menu resources, accidental-run interruption, and directory inventory. No assistant connected to the user's live Windows drives or performed these large numerical runs.
- The uploaded **`OUTLANDISH_01.zip`** reviewed in this session provides a source snapshot (SHA-256 `dbd30202bffb5c64ae85f70dcae552cb0760478391e11d5f5cd27ff3c0a43c57`), including `outlandish_big_constants.py`, `outlandish_artifacts.py`, `outlandish_config.py`, tests and the fixed-location TOML contract. This is not a proof of live filesystem contents after any subsequent owner changes.
- This v3 draws its historical narrative/Windows Sandbox diagnostic appendix from `OUTLANDISH_01_2026-11-07_Project_Status_and_Sandbox_Final_Closure_v2.md` (SHA-256 of text as read in this session `a57e05e2347400e341edd501a62fdaa781bcfc014d9fe12e3af40eadf5ea8f54`). The v2 and older 5-November historical bundle remain evidence, not current instructions. The owner stated that the agreed older-file renames and the v2 installation were completed.
- **Version chronology:** 5-November historical status + bundle (v0.1); 7-November early Sandbox handover (v1); 7-November final Sandbox closeout (v2); **7-November WSL2 feasibility and adopted primary architecture (this v3)**. v3 supersedes v2 **only as the current chat handover**.
- Precise y-cruncher 4-GB total-memory cap for 10^10, final disk usage and throughput, Linux/Windows transfer verification, final Windows convert+verify rehearsal, and production registration are **not yet demonstrated**. No claim is made about predictive power or success of the eventual 10^10 computations.

**End of OUTLANDISH_01 consolidated v3 handover — 7 November 2026.**
