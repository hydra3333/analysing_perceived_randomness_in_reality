#!/bin/sh
# MHUP-B slice 2: make the dev tree from the base tree: slice 1 first, then slice 2 on top of it.
# Usage: build_dev_slice2.sh BASE DEV SLICE1_TOOLS SLICE2_TOOLS     (absolute or relative paths)
set -e
BASE="$(cd "$1" && pwd)"; mkdir -p "$2"; DEV="$(cd "$2" && pwd)"; T1="$(cd "$3" && pwd)"; T2="$(cd "$4" && pwd)"
sh "$T1/build_dev_slice1.sh" "$BASE" "$DEV" "$T1" >/dev/null
if [ -f "$T2/apply_slice2.py" ]; then python3 -I "$T2/apply_slice2.py" "$DEV"; fi
if [ -f "$T2/edit_tests_slice2.py" ]; then python3 -I "$T2/edit_tests_slice2.py" "$DEV"; fi
(cd "$T2/slice2_new" && find . -type f ! -name '*.pyc' | while read f; do mkdir -p "$DEV/$(dirname "$f")"; cp "$f" "$DEV/$f"; done)
find "$DEV" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "dev tree built at $DEV"
