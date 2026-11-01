"""Draft Architecture v0.9 from the installed Architecture v0.8 by counted in-place edits (Claude, 1 Nov 2026).

A status edition: a new section 0B records what is installed since v0.8 (the method contract and walk-forward
driver, the WF-1B scorer and report tool, PERF-1), where the records live, the switches, the worker limits as they
stand (WORKERS-1 decided for WF-1C, not pre-empted), the version-1-only readers, and the planned .gitattributes rule.
Pointer lines are added to 5A.4, 10.1, 12.5, 13.1 and 20A. Every other line, including the protected section 5C, is
byte-identical to v0.8. Every old string must occur exactly once; inserted text is ASCII.
Input: the Git blob of doc/Predictive_Randomness_Software_Architecture_Discussion_v0_8.md (32cf157d...52ec).
Usage: python3 -I make_arch_v09.py ARCH_v0_8 OUT_v0_9
"""
import hashlib, sys

src, out = sys.argv[1:3]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == '32cf157d9ce8850e790274e962236f2be3b50a8bdee7ec94a28ba00d7fd452ec'
t = raw.decode('utf-8')
assert '\r' not in t
P5C = t[t.index('## 5C.'):t.index('## 6. ')]

SECTION_0B = """
---

## 0B. Status at edition 0.9 (1 November 2026)

This section records what is installed and in force on 1 November 2026. Where section 0's status lines (written for v0.8) differ, this section and the ratification register (v0.23) prevail; those lines are kept as history. Edition 0.9 changes no design decision of v0.8: it records installed facts and adds pointer lines to 5A.4, 10.1, 12.5, 13.1 and 20A. The protected section 5C is byte-identical.

**Installed since v0.8** (each reviewed by the ChatGPT reviewer chat, accepted by the owner, rehearsed by Claude Code in a task clone, installed by the owner and verified by Claude from GitHub; details in the register):
- **The method-generic contract and its runner** (E2R-CODE-1 and E2R-CODE-2): `src/methods/_common/` (the contract records, registry, receipts and publication, the dispatch gate) and `src/methods/Method_Contract_Runner.py`, run through `Run_Experiment.bat`. This is the method-generic contract that 20A requires before E_2; its acceptance is recorded in the register (v0.11 to v0.14).
- **The methods:** E_1 (revision 2), E_2, E_3, E_4, E_6, E_7, E_8, E_9, E_10, E_17, E_18 and E_19, 40 variants, released in both games (REL-1; E_1 revision 2 with CODE-3's retirement tooling, revision 1 archived under `archive/methods/E_001/r1/`).
- **The walk-forward driver (WF-1A):** `src/methods/Method_Walk_Forward.py` and `src/methods/_common/walk_forward.py`, run as `Run_Experiment.bat Method_Walk_Forward.py plan|run|status`. It runs one (variant, target) pair at a time, in a fixed order, in one process, through the unchanged contract runner; it starts no subprocess and uses no coordinator; it stops at the first STOP-class result, and re-running the same command resumes. It has no worker option.
- **The scorer and ranking report tool (WF-1B, installed at `24d192f`):** `src/evaluation/`, launched by `Run_Method_Rankings.bat` (5A.4) as `--game G --batch ID --first S --last L`. It runs in the fixed order of the releases and WF-1 design v0.1r1 section 6.1 with the WF-1B supplement v0.1r1: refusals that read nothing; the grid and the frozen forecasts; the search-log row and the create-only scoring plan, both before any outcome is read; the outcome reader (`src/evaluation/outcome_reader.py`; only the requested grid targets, all below the holdout, are decoded); the score and rank ledgers; then the measures, the families and N1. It runs no method code.
  - **N1** (`src/evaluation/n1.py`, `n1_generator.py`): R = 10,000 fair-draw histories from SHAKE-256 streams keyed by the approved seed policy's root.
  - **Seed policies** (`src/evaluation/seed_policies.py` and `seed_policies/`): one `APPROVED` policy, `N1_ROOT_NIST_C2_20261031T1030Z_V1`; the replaced 6 November policy stays on file. With no approved policy the report runs without N1 and says so.
  - **Registries:** `src/evaluation/registry/MEASURE_REGISTRY_V1.json` and `FAMILY_REGISTRY_V1.json`.
- **PERF-1** (installed at `3fce327`, 1 November 2026): `src/evaluation/numerics.py`'s exact binomial sums by binary splitting and its Clopper-Pearson interval by a decimal-guided bisection confirmed with the exact tails (the same results as before, much faster), and count-only progress lines in the report tool.

**Where the records live:**

| Path | What | In Git? |
|---|---|---|
| `results/audit/SEARCH_LOG.csv` | the append-only search log (batch rows, ranking-report rows) | committed by the owner |
| `results/real/development/wf_batches/<GAME>/<batch>/` | each batch's `plan.json` and segment record; `attempts.jsonl` | the plan and segment record committed; `attempts.jsonl` git-ignored |
| `results/real/development/contract_runs/` | every walk-forward run's frozen records | git-ignored (local only) |
| `results/real/development/scores/<GAME>/<batch>/<attempt>/` | each report attempt's scoring plan and score and rank ledgers | git-ignored (local only) |
| `results/method_rankings/<GAME>/` | each report's `.txt`, `.csv` and `.json`, create-only, named with the window, time and attempt | committed by the owner |

Claude checks the owner's results commits by paths and sizes only; no AI session opens `source_data/`, `results/` or `transitory_data/`.

**Line endings (R-011, in the snapshot package):** `.gitattributes` already stores `source_data/**` byte for byte (`-text`). A matching rule for `results/**`, in the snapshot package, stops Git rewriting committed record files with Windows line endings on the owner's computer (the first Powerball report was refused because its two committed batch records had been rewritten with Windows line endings in the working copy; the owner restored the committed bytes, and the report then ran).

**Switches and allowlist:** `ENABLE_CONTRACT_REAL_DEVELOPMENT` is True (WF1-3, since WF-1A). `ENABLE_PROCESS_TERMINATION`, `ENABLE_SCIENTIFIC_COORDINATION` and `ENABLE_SYNTHETIC_WINDOWS_LIFECYCLE` stay False, and the coordinated science allowlist stays empty.

**Workers and threads, as they stand:**
- **The coordinator** keeps its limit of 1 to 6 workers, default 6 (10.1, 10.3, O-CPU-01, O-POL-03). It still runs only the proof-of-concept probes, not scientific methods.
- **WORKERS-1** (the owner's decision, 31 October 2026): the coordinator's limit is to become 1 up to the machine's logical processor count, default half, and the walk-forward driver is to get a `--workers` option. By the owner's decision WB-0 this belongs to a separate package, **WF-1C**, with its own design round carrying EX_101's and EX_105's obligations in full. Until WF-1C is reviewed and owner-ratified, sections 10.1 and 10.3 stand unchanged; their "No default 12-worker or 24-worker SMT stress runs" line and the ~2 GB-per-worker planning figure are to be revisited in WF-1C's design, not here.
- **Thread pins:** `Run_Experiment.bat`, `Run_Coordinator.bat` and `Run_Method_Rankings.bat` set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` and `NUMEXPR_NUM_THREADS` to 1 before Python starts (10.2). The effective backend and thread count are not yet recorded by walk-forward runs (a WF-1C matter, EX_105 C02).

**Known limitation (for the Mode H, results update and prospective design):** the method reader (`src/methods/_common/game_draws_reader.py`) and the outcome reader (`src/evaluation/outcome_reader.py`) accept a master only when its ledger is the single version-1 `INIT` line. Any results update, even one that adds no draw, appends a ledger line, after which every method run and report refuses. A reviewed reader for later master versions, with how a run pins a version, must be designed together with Mode H and the results update before the update is run.
"""

EDITS = [
    ('**Version:** 0.8 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026): Architecture v0.7 plus',
     "**Version:** 0.9 OWNER-RATIFIED 1 November 2026 (content reviewed in EX_117, EX_119 and EX_121): Architecture v0.8 plus a status section (0B) and five pointer lines; no design decision changes. Predecessor: 0.8 OWNER-RATIFIED 27 October 2026 (drafted 26 October 2026): Architecture v0.7 plus"),
    ('**Edition status: OWNER-RATIFIED 27 October 2026; Architecture v0.7 is historical.**',
     '**Edition status: OWNER-RATIFIED 1 November 2026; Architecture v0.8 is historical.** Edition 0.8: **OWNER-RATIFIED 27 October 2026; Architecture v0.7 is historical.**'),
    ('\n---\n\n## 0. Document purpose, authority and controls\n',
     '\n' + SECTION_0B + '\n---\n\n## 0. Document purpose, authority and controls\n'),
    ('- **Wrapper:** `Run_Method_Rankings.bat` follows the ratified wrapper rules',
     '- **Status (v0.9):** installed with WF-1B at `24d192f`; it pins the numerical-library threads to 1 like the other launchers (0B).\n- **Wrapper:** `Run_Method_Rankings.bat` follows the ratified wrapper rules'),
    ('\n### 10.2 Internal numerical libraries and environment\n',
     '\n**v0.9 note:** this section and 10.3 stay in force for the coordinator until WF-1C (the owner\'s WORKERS-1, deferred by WB-0) is reviewed and ratified; WF-1C\'s design revisits the 12/24-worker line and the ~2 GB figure. The walk-forward driver has no worker limit: it runs one pair at a time in one process (0B).\n\n### 10.2 Internal numerical libraries and environment\n'),
    ('- The wrapper is in 5A.4. The evaluator rules',
     '- **Status (v0.9):** the report tool and N1 are installed (WF-1B, `24d192f`); the evaluator is `src/evaluation/` (0B). IS runs are not built.\n- The wrapper is in 5A.4. The evaluator rules'),
    ('**`transitory_data/` is optional** and should not be created until genuinely needed.',
     '**Record locations as installed (v0.9):** see 0B; under `results/real/development/`, the walk-forward batch plans and segment records are committed, the run records, attempt logs and report scores are git-ignored, and the reports under `results/method_rankings/` and the search log `results/audit/SEARCH_LOG.csv` are committed.\n\n**`transitory_data/` is optional** and should not be created until genuinely needed.'),
    ('**Stage-1 contract fields (DECIDED; Method Ranking Measures Proposal v0.5):**',
     '**v0.9 note (version-1 readers):** both installed readers accept only the version-1 master (0B, known limitation); a reader for later versions is part of the Mode H and results-update design.\n\n**Stage-1 contract fields (DECIDED; Method Ranking Measures Proposal v0.5):**'),
]
for old, new in EDITS:
    n = t.count(old)
    assert n == 1, (n, old[:80])
    assert all(ord(c) < 128 for c in new), old[:60]
    t = t.replace(old, new)
assert t[t.index('## 5C.'):t.index('## 6. ')] == P5C, 'section 5C changed'
open(out, 'wb').write(t.encode('utf-8'))
print(out, hashlib.sha256(t.encode()).hexdigest(), len(t.splitlines()), 'lines')
