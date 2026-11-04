#!/bin/sh
# MHUP-A slice 2: the dev tree = slice 1's dev tree + slice 2's whole-file replacements and new files.
# Usage: build_dev_slice2.sh BASE DEV TOOLS DATE
set -e
BASE="$1"; DEV="$2"; T="$3"; DATE="$4"
sh "$T/build_dev_slice1.sh" "$BASE" "$DEV" "$T" "$DATE" > /dev/null
cd "$T/slice2_edited" && find . -type f ! -path '*/__pycache__/*' | while read -r f; do
  rel="${f#./}"; mkdir -p "$DEV/$(dirname "$rel")"; cp "$f" "$DEV/$rel"
done
cd "$T/slice2_new" && find . -type f ! -path '*/__pycache__/*' | while read -r f; do
  rel="${f#./}"; mkdir -p "$DEV/$(dirname "$rel")"; cp "$f" "$DEV/$rel"
done
if [ -f "$T/apply_slice2.py" ]; then python3 -I "$T/apply_slice2.py" "$DEV"; fi
if [ -f "$T/edit_tests_slice2.py" ]; then python3 -I "$T/edit_tests_slice2.py" "$DEV"; fi
find "$DEV" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "slice 2 dev tree built at $DEV"
