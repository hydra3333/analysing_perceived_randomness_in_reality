# P1/P2 Orphan Interlock v0.6 — safety review handback

**Date:** 23 October 2026  
**Status:** REVIEW CANDIDATE ONLY — NOT AUTHORISED FOR WINDOWS INSTALLATION OR DESTRUCTIVE TESTING  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Current Windows coordinator source understood to be v0.3:** SHA-256 `a2402175eaf22bf9d0293b49a6d1c91b48fe20d26866cf5d096dcfae6a95a58b`. Do not assume Git HEAD equals that source without verification.  
**Supplied repository snapshot `(4).zip`:** coordinator v0.2 SHA-256 `26c471e183d073db6e258a51c5b363f90d3024bc497ebebeba804a25ab187cf4`. The package supplies exact diffs from both baselines and from the v0.5 candidate.

## Purpose and B2 correction

Claude rejected v0.5 because a wrapper could exit before its live Python experiment was captured. The scheduler then recorded ordinary failure and continued, despite matching status.json naming a live/uncertain PID.

v0.6 checks **both** retained captured descendants and run-ID-matched status PID evidence on every observed wrapper exit, including nonzero exit and zero captured children. Matching status PID with `same_process(pid, ctime) is True or None` causes `ORPHAN_SUSPECTED`, a flushed safety banner, durable `UNRESOLVED_ORPHAN.json` marker and no more new workers in this coordinator. For missing/invalid creation time, liveness remains unknown and the interlock blocks conservatively. A confirmed-gone or reused PID is not an orphan indicator by itself. The post-loop validation uses the same typed check and no longer relies on parsing an error string. Remaining active workers are supervised as before; they are not silently killed.

**Status-file PIDs only justify a safety BLOCK, NEVER any termination target.** The ratified strict no-status/no-kill rule remains unchanged. `ENABLE_PROCESS_TERMINATION = False` is unchanged with no CLI bypass. Existing `terminate_owned_tree`, `_member_alive`, `same_process`, `save_new`, root registration and termination plan functions are identical to v0.3; their AST was checked. No new process-kill calls.

## Human-facing safety messages

The immediate stderr output includes `[COORDINATOR] ORPHAN_SUSPECTED` with worker, matching status PID, recorded creation time and observed liveness or uncertainty; the `SAFETY STOP` banner includes group/run/root identifiers, exact marker path, original reason, and numbered recovery steps. Attempts to start another run repeat the original reason and worker/status evidence from the persisted marker. All these lines are flushed immediately.

**Operator procedure (owner-approved):** Do not terminate listed PIDs by hand. Investigate both PID and process creation time; if any identity is live or uncertain, leave the interlock and escalate. Only when ALL listed identities have exited should the operator archive the original marker bytes, SHA-256 and logs, then manually remove the active marker. No CLI acknowledgement.

**Residual limitation:** If the wrapper exits before any descendant is captured *and* no usable matching status file exists, the coordinator has no evidence of an orphan. It must not infer ownership or kill. This limitation remains documented rather than misrepresented as complete process containment.

## Decision ledger

- **DECIDED within ratified design:** status PID evidence blocks on matching live/unknown identity; never grants kill authority. Human warnings are explicit and immediately flushed.
- **ALREADY OWNER-RATIFIED:** strict no-status/no-kill; manual marker clearance with archived evidence; common `.bat` execution interface; default kill switch False.
- **RECOMMENDED, AWAITING CLAUDE REVIEW:** v0.6 fixes B2; accept for Windows **non-destructive** installation/testing only after independent source review.
- **OPEN:** actual Windows orphan/marker acceptance tests, Ctrl+C, timeout, code page and direct-coordinator rejection checks; separate explicit owner approval required before any switch-on destructive tests.

## Exact files in the installation ZIP

- `src/Powerball_Experiment_Coordinator.py` — proposed **replacement** of installed v0.3; verify installed hash `a2402175eaf22bf9d0293b49a6d1c91b48fe20d26866cf5d096dcfae6a95a58b` first.
- `tests/p1p2_orphan_interlock_v0_4.py`, `tests/p1p2_orphan_interlock_v0_5.py`, `tests/p1p2_orphan_interlock_v0_6.py` — **new** fake-only tests. No batch runners or production data changes.

The original `tests/p1p2_automated_decoy_ownership.py` remains pinned to v0.3 and must **NOT** be executed against v0.6 until its coordinator hash guard is separately updated and reviewed. Do not run timeout/Ctrl+C/destructive tests during this review.

## Local verification

All seven P0/P1-P2 static/synthetic suites passed on the tool host (Python 3.13 with `psutil` installed); this does **not** demonstrate actual Windows process supervision. `tests/p1p2_orphan_interlock_v0_6.py` uses fake process liveness and a temporary marker directory; no real PID lookup or termination. Previous Windows PASS evidence belongs to v0.3, not v0.6.

Exact new source SHA-256: `2e23d55049afa8cf336a14e60d7ee52f3ea5043fda442da4d6837f81f79c762b`.

## Out-of-scope

No changes to ratified architecture, scientific E-methods, training/holdout data, dependency package policy, ownership-based termination, or permission to enable termination. No Git commit is claimed.
