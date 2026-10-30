"""Draft 2 of the template's contract skeleton (method_folder/contract.py.txt), by counted edits from draft 1
(Claude, 30 Oct 2026; wave 1 code package). Usage: python3 -I make_template_draft2_code.py TEMPLATE_DIR OUT_DIR
Adds the minimum-history case and separate probability checks (README draft 2, step 4)."""
import hashlib, sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
name = 'method_folder/contract.py.txt'
raw = (src / name).read_bytes()
assert hashlib.sha256(raw).hexdigest() == sys.argv[3] if len(sys.argv) > 3 else True
t = raw.decode('utf-8')
EDITS = [
    ("TEMPLATE (copy to src/methods/E_<nnn>/contract.py and drop the .txt). Taken from E_6's contract.py.",
     "TEMPLATE, draft 2 (copy to src/methods/E_<nnn>/contract.py and drop the .txt). Taken from E_6's contract.py,\n"
     "with wave 1's minimum-history case and separate probability checks."),
    ("PROVENANCE = 'E_<n> r1: FILL IN one line on how the probabilities were computed'\n",
     "PROVENANCE = 'E_<n> r1: FILL IN one line on how the probabilities were computed'\n"
     "MINIMUM_HISTORY = 1                      # FILL IN: the declaration's minimum_history_draws; a dict\n"
     "                                         # {variant_id: draws} if the variants differ\n"),
    ("def _exact(task, view, algorithm):\n    setting = _setting(task)\n    return {",
     "def _minimum(task) -> int:\n"
     "    return MINIMUM_HISTORY[task.variant_id] if isinstance(MINIMUM_HISTORY, dict) else MINIMUM_HISTORY\n\n\n"
     "def _exact(task, view, algorithm):\n"
     "    \"\"\"{barrel_id: {label: exact score}}, or None when the history is shorter than the declared minimum.\"\"\"\n"
     "    setting = _setting(task)\n"
     "    if len(view.simple_rows()) < _minimum(task):\n"
     "        return None                       # LEAVE ALONE: the contract then records INSUFFICIENT_HISTORY\n"
     "    return {"),
    ("def compute(task, view) -> MethodOutput:\n    out = {}\n    for bid, exact in _exact(task, view, scores).items():",
     "def compute(task, view) -> MethodOutput:\n"
     "    exact_all = _exact(task, view, scores)\n"
     "    if exact_all is None:\n"
     "        return MethodOutput(barrels={})   # LEAVE ALONE: too little history\n"
     "    out = {}\n"
     "    for bid, exact in exact_all.items():"),
    ("    exact = _exact(task, view, scores_by_second_algorithm)\n    if set(forecast['barrels']) != set(exact):",
     "    exact = _exact(task, view, scores_by_second_algorithm)\n"
     "    if exact is None:\n"
     "        if forecast['record_status'] != 'INSUFFICIENT_HISTORY':\n"
     "            raise ValueError(f'{METHOD_ID} check: too few draws, but the record is not INSUFFICIENT_HISTORY')\n"
     "        return\n"
     "    if set(forecast['barrels']) != set(exact):"),
    ("        if rec['scores'] != want or (PROBABILITIES and rec['probability'].get('vector') != want):\n"
     "            raise ValueError(f'{METHOD_ID} check: the record differs from the recomputation in barrel {bid}')\n",
     "        if rec['scores'] != want:\n"
     "            raise ValueError(f'{METHOD_ID} check: the record differs from the recomputation in barrel {bid}')\n"
     "        if PROBABILITIES and rec['probability'].get('vector') != want:     # test this check on its own\n"
     "            raise ValueError(f'{METHOD_ID} check: the probability vector differs in barrel {bid}')\n"
     "        if not PROBABILITIES and rec['probability'] != {'kind': 'NONE'}:\n"
     "            raise ValueError(f'{METHOD_ID} check: a score-only method published a probability in barrel {bid}')\n"),
]
for o, n in EDITS:
    assert t.count(o) == 1, o[:60]
    assert all(ord(c) < 128 for c in n)
    t = t.replace(o, n)
(out / 'method_folder').mkdir(parents=True, exist_ok=True)
(out / name).write_bytes(t.encode('utf-8'))
print(name, hashlib.sha256(t.encode()).hexdigest(), len(EDITS), 'edits')
