# modeh_reading - the tools behind Claude's reading of the two Mode H reports (EX_201)

Four small Python programs (standard library only). They read **only** a Mode H rankings report `.txt` file: a value-free
text file. They open no master, grab, backup, ledger, forecast or score file, contact nothing, and write nothing.

They are published so that every figure in `exchange/EX_201_Claude.md` and `exchange/EX_202_Claude.md` can be reproduced
from the two report files. They are reading aids for the Claude web chat: not project code, not installed, not part of any
package, and never run by the local runner.

| File | What it does | Usage |
|---|---|---|
| `parse_report.py` | Splits a report into its Part A and Part B tables. Used by the other three. | `python -I parse_report.py REPORT.txt` |
| `analyse.py` | For each Part B table: the smallest local P, and the ten smallest in the whole report. | `python -I analyse.py REPORT.txt` |
| `detail.py` | Recomputes every MR7 exact probability from each track's own total (exact fractions) and compares it with the report; TOP and WORST totals; mean ranks; prize-division counts. | `python -I detail.py REPORT.txt OZLOTTO` or `... POWERBALL` |
| `aggregate.py` | Post hoc, exploratory arithmetic: the overlap allowance, what the family test could detect, the cross-game comparison. | `python -I aggregate.py OZLOTTO_REPORT.txt POWERBALL_REPORT.txt` |

The reports they were run on (16 November 2026), by SHA-256:

- Oz Lotto: `68112928b332666c8e2da6504b06e93a81295cf21682cd076d0a85e754ebd0e6` (585,497 bytes)
- Powerball: `1bad6295f5af67845412983c3c37ae48156530dad3b12ce24ad3234cf4177ffc` (750,084 bytes)

The reports themselves are not in this folder: committing them is the project owner's separate decision (D5).

`aggregate.py` is exploratory. Its overlap figure is estimated from the same totals it then assesses, so its sigma values
are rough guides, not calibrated probabilities (EX_201 section 3.3; EX_202 question Q2).
