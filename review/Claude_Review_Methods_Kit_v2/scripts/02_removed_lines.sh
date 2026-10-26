#!/bin/sh
# List every line of a ratified base that is missing from a candidate edition.
# The count and content must match exactly what the evidence note declares.
# Usage: sh 02_removed_lines.sh base.md candidate.md
diff "$1" "$2" | grep '^<' | cut -c1-230
echo "removed-or-changed base lines: $(diff "$1" "$2" | grep -c '^<')"
