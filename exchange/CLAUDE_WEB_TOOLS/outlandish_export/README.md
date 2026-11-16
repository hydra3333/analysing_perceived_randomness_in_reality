# OUTLANDISH_01 export: Oz Lotto, pre-holdout only (Claude web chat, 16 November 2026)

`make_ozlotto_preholdout.py` writes `GAIS/OUTLANDISH_01/OZLOTTO_preholdout_only.csv` for the side project, owner-run only.
It reads only the committed version-1 Oz Lotto master (pinned by SHA-256 `4a6cecc2...`), never the working-tree master
(which holds the holdout since Approval 2), and stops on any draw at or after 1694 before writing anything. It writes one
new file in `GAIS/` and nothing else; it changes nothing the Mode H freeze protects (no file under `src/`, no package).
No AI chat runs it or sees its output values; its certificate prints counts and hashes only.

Development test (invented master in a scratch Git repository; Linux Python 3.15): a normal run (220 rows, 1474-1693, LF,
no BOM); a refusal when the output exists; the same output when the working tree holds an extra draw 1694 (proving it
reads only the committed bytes); a refusal when the committed master's hash differs. Not Windows evidence.

Note for the side project: the numbers are in the order the master stores them, which is the order the official results
page lists them; whether that is the machine's drawn order is not something this project has established.
