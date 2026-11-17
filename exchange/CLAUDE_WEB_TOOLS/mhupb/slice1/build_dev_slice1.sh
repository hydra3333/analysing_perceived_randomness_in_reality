#!/bin/sh
# MHUP-B slice 1: make the dev tree from the base tree. Usage: build_dev_slice1.sh BASE DEV TOOLS
set -e
BASE="$(cd "$1" && pwd)"; mkdir -p "$2"; DEV="$(cd "$2" && pwd)"; T="$(cd "$3" && pwd)"
rm -rf "$DEV"; cp -a "$BASE" "$DEV"; rm -rf "$DEV/.git"
python3 -I "$T/apply_slice1.py" "$DEV"
python3 -I "$T/edit_tests_slice1.py" "$DEV"
(cd "$T/slice1_new" && find . -type f ! -name '*.pyc' | while read f; do mkdir -p "$DEV/$(dirname "$f")"; cp "$f" "$DEV/$f"; done)
find "$DEV" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "dev tree built at $DEV"
