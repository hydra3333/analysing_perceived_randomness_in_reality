#!/bin/bash
# Build step 2, workspace helper: copy the overlay into a disposable dev tree and run the named test modules there.
# Usage: sync_and_test.sh <dev tree> <python> [test module ...]     (no module: only the copy)
OVERLAY="$(cd "$(dirname "$0")" && pwd)/overlay"; DEV=$1; PY=$2; shift 2
cp -r "$OVERLAY/." "$DEV/" || exit 1
"$PY" -B "$(dirname "$OVERLAY")/apply_edits.py" "$DEV" | grep -v "already applied" ; true
cd "$DEV" || exit 1
for m in "$@"; do
  PYTHONPATH=src:src/methods:tests "$PY" -B -m unittest "$m" 2>&1 | tail -n 12
done
