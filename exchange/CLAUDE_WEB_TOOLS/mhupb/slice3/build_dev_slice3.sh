#!/bin/sh
# MHUP-B slice 3: make the dev tree from the base tree: slice 1, then slice 2, then slice 3 on top of them.
# Usage: build_dev_slice3.sh BASE DEV SLICE1_TOOLS SLICE2_TOOLS SLICE3_TOOLS     (absolute or relative paths)
set -e
BASE="$(cd "$1" && pwd)"; mkdir -p "$2"; DEV="$(cd "$2" && pwd)"
T1="$(cd "$3" && pwd)"; T2="$(cd "$4" && pwd)"; T3="$(cd "$5" && pwd)"
sh "$T2/build_dev_slice2.sh" "$BASE" "$DEV" "$T1" "$T2" >/dev/null
python3 -I "$T3/apply_slice3.py" "$DEV"
python3 -I "$T3/edit_tests_slice3.py" "$DEV"
(cd "$T3/slice3_new" && find . -type f ! -name '*.pyc' | while read f; do mkdir -p "$DEV/$(dirname "$f")"; cp "$f" "$DEV/$f"; done)
find "$DEV" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "dev tree built at $DEV"
