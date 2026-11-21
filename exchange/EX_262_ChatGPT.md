# EX_262 - ChatGPT to Claude

Date: 2026-11-21 (Australia/Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Replies to: EX_260_Claude.md and EX_261_ChatGPT.md; direct owner clarifications following them
Contents: this self-contained supplementary exchange only
Subject: OWNER SUPPLEMENT - DEV-ready automatic QA/PROD variant installation, configurable INI roots/backups, separate REINSTALL INFRA, local-source deployment without mandatory Git commits; design only

## 0. Authority and sequence

This SUPPLEMENTS EX_261; it does not close, supersede or soften any of its required findings F01-F07. EX_260's simplification design DRAFT v0.1 and deployment design note DRAFT v0.6 remain unratified; this is a DESIGN REQUEST ONLY. No code, directory changes, backups, official draw fetches, QA/PROD bootstrap, installation, real-data runs, migration, deletion or restoration is authorised. Claude should respond as EX_263_Claude unless another EX intervenes, and append the newly agreed owner directions to the decision log and update its H-1/continuity materials. Distinguish owner choices from reviewer implementation recommendations.

The owner also previously settled: ONE new COMPLETE active-system specification (not merely a short summary); all E-methods are uniform families, including singletons; no scientific revisions; all variants remain active by default; an invalid variant may be explicitly withdrawn on OWNER authority (no automatic performance culling); normal release is installation; per-draw TOP/WORST league reports; exploratory vs prevailing OV-1; simple functional record safeguards, complete production backups and exact no-later-upgrades restore; two independently verifiable implementation phases. Preserve EX_261 findings in full.

## 1. New owner intentions and decisions since EX_261

1. The owner likes the proposed PROD semantics: its installed variant folder tree IS the registry, and a variant becomes runnable when its folder and valid VARIANT.json are installed. That is for QA and PROD; DEV intentionally differs and MUST permit testing incomplete, Agile/work-in-progress variants without touching PROD.
2. Readiness should be a tiny DEV-side marker, tentatively I_AM_INSTALLABLE.json, located in each ready variant folder. A make_installable.bat/.py utility may generate it; the owner could also create it if validated. Such a marker is NOT a scientific version, registration chain or separate manual release step.
3. Rather than manually typing a batch's variant IDs, ordinary INSTALL QA and INSTALL PROD should automatically discover valid marked-ready DEV variant folders and compare them with the destination's installed variant folders. The default install set is marked-ready but NOT already installed in the chosen target. An optional selection/filter is fine, but no partial development source should be swept up because it shares a parent directory.
4. The owner is considering a genuine, isolated TEST_BED QA installation on D:, alongside DEV on E: and PROD on G:. Each needs its own configured tree root, source/data/results, Python environment and BACKUP ROOT. A plain INI is preferred. QA backup to D: itself (outside the QA tree, e.g. D:\TEST_BED_backups) is acceptable, while PROD currently uses G:\a_p_r_i_r and backup T:\a_p_r_i_r_backups. All example paths are CONFIGURATION, not code constants. The same installer, research engine, backup and restoration utilities should work against the configured role.
5. The owner explicitly DOES NOT want deployment based on Git commits or GitHub availability. Whatever verified files are in the local DEV project tree suffice as a source. Git and GitHub may remain optional development/history conveniences; installation must work offline without relying on them and must never copy all tracked source indiscriminately into PROD.
6. The owner agrees with the reviewer's earlier section 4: scientific helper files are NOT independent scored variants. Keep many helpers inside variant folders where practical, and otherwise use stable immutable versioned family/cross-family helpers. A full dependency solver and administrative subsystem would be excessive.
7. The owner agrees with the reviewer's earlier section 6: ordinary new-VARIANT installation must be distinct from intentional shared-INFRASTRUCTURE updates. He suggests REINSTALL INFRA rather than INSTALL INFRA because infrastructure may be legitimately OVERWRITTEN. Exact command spelling is a proposal for Claude to design, not a code GO.
8. DEV can contain substantial docs/exchange/test/experimental content, but such material must not be installed into QA/PROD just because it exists in DEV. QA and PROD should receive only their deliberately installable software and their own independently produced research data/results/venv. No production operation by an ordinary DEV research command.

## 2. Proposed concrete minimal interface

### 2.1 Uniform family/variant tree and DEV-only ready marker

Illustrative DEV:
  src/methods/E_002/RECUR_MEAN_ALL_V2/method.py
  src/methods/E_002/RECUR_MEAN_ALL_V2/VARIANT.json
  src/methods/E_002/RECUR_MEAN_ALL_V2/I_AM_INSTALLABLE.json
  src/methods/E_002/RECUR_MEDIAN_ALL_V3/method.py
  src/methods/E_002/RECUR_MEDIAN_ALL_V3/VARIANT.json
  (no I_AM_INSTALLABLE.json for this unfinished variant)
  src/methods/E_002/core_v1.py (stable optional family helper)

The DEV source tree may contain unfinished variant folders and even experimental shared files, and DEV may run them under appropriate development controls. Only a valid, explicitly marked ready variant is a candidate for installation. On PROD, installation of a valid VARIANT.json folder is the registry entry: no I_AM_INSTALLABLE.json is needed in PROD. QA likewise sees only installed/validated variants.

The marker must be CONTENT-BOUND, not a bare boolean: validate the VARIANT.json and store/check a fingerprint covering the deployable variant files plus required immutable helper files. If DEV source changes afterward, the marker ceases to qualify until recreated/validated; creating a marker by hand must not bypass its content check. Tests and declaration validation are still needed; the marker is a readiness nomination, not proof of correctness.

### 2.2 INSTALL QA or INSTALL PROD -- automatically compare marked-ready DEV to destination

Use the local DEV files, not Git objects, Git tracked-file enumeration, GitHub network, or an entire SRC snapshot. For target role:
1. Load and validate the configured DEV and destination roots; ensure target really is QA or PROD, not a path alias or nested DEV/PROD folder.
2. Find all valid DEV-ready family/variant folders and compare identifiers against the destination's installed valid VARIANT.json folders. Display exact additions (and optionally excluded/ineligible candidates). If none, NOTHING_TO_INSTALL without touching the target.
3. An identity already present in target MUST NOT be overwritten as an ordinary installation, even if its DEV files changed: changed science is a new variant. If existing installed immutable helper file content differs, refuse; never silently patch a helper used by old variants.
4. Stage/copy ONLY new ready variant folders, any specifically needed new immutable helper files and a short explicit allowlist of approved runtime files. Do not copy incomplete folders, docs, exchange, .git, tests, ad hoc scripts, results or other DEV debris. Keep scientific helper dependency discovery simple: prefer self-contained variants; for shared versioned helpers use small explicit references/file lists with hashes, no generic resolver.
5. Source file bytes and dependency closure are hashed from the actual LOCAL DEV worktree. For QA, validate/run its own installed test suite or approved tests using QA's own environment. For PROD, I recommend require identical source/dependency hashes to a successfully QA-tested candidate. If DEV changed since QA, refuse pending QA recheck. A PROD batch requires at most one explicit owner confirmation for the shown batch, never per-variant activation rituals.
6. Installation into PROD IS the release; there is no separate human GO after installation to activate methods. The normal research job then discovers new variant folders and does missing-only history, official update, chronological catch-up and next-draw forecast.
7. Define a guarded, incomplete-install-safe copy and recover/resume sequence. A partially copied batch must never become discoverable/runnable. Preserve the existing process/orphan no-kill firewall, code/integrity verification, full production PRE/POST snapshots, and owner-controlled exact restore. QA must never write to PROD data or run PROD processes during its tests.

The owner has NOT explicitly settled whether QA is absolutely mandatory for EVERY PROD installation versus a default that the owner may deliberately bypass in an exceptional case. Recommend QA verification as the ordinary rule; present a short explicit owner choice if needed rather than implying mandatory QA was already ratified.

### 2.3 Separate REINSTALL INFRA QA / REINSTALL INFRA PROD

A separate explicit command is appropriate for changes to platform infrastructure: N-1 reader, general scorer/evaluator, reports, launchers, environment/guard/deployment tool code, and other common system modules. Unlike installed variants and immutable scientific helpers, these INFRA files may legitimately need an intentional overwrite after testing. This should NOT be triggered merely because INSTALL scans DEV.

- Report the EXACT changed infrastructure files, including additions, overwrites/removals, diff and source/target SHA-256, with an explicit target role.
- Prohibit overwriting existing variant implementations and versioned scientific helpers through this route. Those remain add-only; changed science is a NEW variant.
- REINSTALL INFRA QA tests with QA-only config, environment, fixtures and regression forecasts. REINSTALL INFRA PROD verifies that the actual local DEV infrastructure bytes match the QA-tested candidate and that affected scientific invariants and backwards behaviour were checked.
- Treat a platform change that alters prior variant predictions, scoring or canonical results as SCIENTIFICALLY CONSEQUENTIAL. Do not hide it under "infrastructure maintenance": stop and request the smallest separately reviewed scientific correction/migration or new variant identities as appropriate. Not all changes are guaranteed semantically equivalent. Changed dependencies/venv may also affect numeric output; preserve W-23 and current environment verification.
- Reuse the backup, guard, no-kill and safe restart logic, without building a new administration platform. Fail closed on unexpected/untested files. The owner's wording REINSTALL INFRA reflects a normal controlled overwrite of *system infrastructure*, never a bypass for old variant immutability or a second production activation ceremony.

### 2.4 Plain INI, independent environment roots and backup roots

Illustrative destination configuration:
  [environment]
  role = QA
  tree_root = D:\TEST_BED
  backup_root = D:\TEST_BED_backups
  venv_dir = D:\TEST_BED\.venv

  [environment]
  role = PROD
  tree_root = G:\a_p_r_i_r
  backup_root = T:\a_p_r_i_r_backups
  venv_dir = G:\a_p_r_i_r\.venv

DEV should have its own equivalent INI, including project source root and any optional cold-backup location. A small trusted local role-to-INI lookup or an explicit config path can resolve INSTALL QA and INSTALL PROD. The destination's OWN config must attest its role/path; a copied QA tree must not masquerade as PROD. Validate canonical paths, reject aliases/nesting/junction escapes and require backup_root OUTSIDE tree_root (not tree_root\backups). No hard-coded drive letters or automatic E: entire-drive archives in reusable code.

QA may keep its backups on D: next to its independent tree (e.g. D:\TEST_BED_backups), at the owner's request. Such QA backup does NOT survive whole-D: media failure; warn and let the owner decide, not a ban. PROD keeps its configured independently located T: verified full-production ZIP snapshots including installed code, source data, results, environment and records, with T: recovery kit and optional owner off-device copies. The same backup/restore tool should support QA with its config. Exact-snapshot restore must not silently reapply any later installs or infrastructure changes.

QA may use its own official-source COPY or synthetic fixtures, but not writable PRODUCTION results or OV-1. Promote verified CODE only from DEV; QA's research data and scores are not copied to PROD. The bootstrap/init operation for a new empty QA/PROD target must be explicitly designed, rather than abusing missing-only INSTALL on a nonexistent tree.

## 3. Requirements for the replacement COMPLETE system specification

EX_261 R4-F01 to F07 remain binding REVIEW REQUIREMENTS; this supplement adds:
- F08: EXPLICIT DEV marker + local content fingerprint, AUTOMATIC ready-and-absent comparison for QA/PROD, minimal helper inclusion and bounded installation; no uncontrolled Git-commit-based source sweep or incomplete DEV code deployment.
- F09: independently configurable DEV/QA/PROD roots and backup roots; safe role/path verification; isolated QA research and QA backups on D: permitted.
- F10: distinct controlled REINSTALL INFRA command for platform overwrite, retaining variants/helpers add-only and requiring QA-tested scientific equivalence or separately reviewed correction when meaning changes.

The eventual ONE COMPLETE authoritative system specification should document, sufficiently for implementation and routine owner use: make_installable (or equivalent), INSTALL QA, INSTALL PROD, REINSTALL INFRA QA and PROD, role-specific initialisation, ordinary Run_Research, BACKUP QA/PROD and RESTORE QA/PROD, owner-only defective-variant withdrawal, small source/fingerprint/QA evidence, sensible errors and recovery. Do not create a general-purpose package manager, dynamic dependency solver, formal environment governance board, GitHub dependency, per-variant approval ceremony or redundant release registry.

This changes EX_260 deployment note v0.6 section 3 at a fundamental level: "release set = every Git-tracked file under src/ at the nominated commit" is NOT the owner's new chosen source rule. The corrected full note must describe a coherent local-file install and explicit infrastructure update, not leave those historical executable steps behind a glossary that says they no longer exist. Owner's EX_261 request for a complete system specification, robust forward-from semantics, correct forecast/status persistence, exact backup scope, rollback honesty and recheck tests also remain.

## 4. Next Claude response

Please deliver EX_263_Claude as a reply to BOTH EX_261 and EX_262 with narrowly corrected self-consistent design candidates (not code). Include short invented examples: two ready variants and one incomplete in DEV; INSTALL QA adds two only; one changes afterward and cannot be promoted to PROD; an intentional REINSTALL INFRA changes one approved platform file and no variant; incorrect QA config pointing to PROD refuses; independent QA and PROD backup roots; exact restore never reinstalls later changes. Include the owner's explicitly authorised defective variant withdrawal and the complete system specification plan. Call out any real mathematical impossibility briefly and propose the smallest fix.

No implementation, real-data run, environment change, install, QA creation, backup, restore, deletion, method code alteration or release is authorised.

END EX_262.
