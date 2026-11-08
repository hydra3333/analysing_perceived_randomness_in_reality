#!/bin/sh
# MHUP-A integrated package: the development tree = the reviewed slice 2 tree (slice 1 included), built on the current
# main, with E_1 revision 3's effective_date = DATE (C01-EFF: the date the package is prepared and frozen for review).
# The one test that pins that date (tests/test_e1r3_revision3.py, written with the candidates' 2026-11-04) gets DATE by one
# counted edit, so the test keeps checking the exact date rather than any date.
# Usage: build_dev_integrated.sh BASE DEV TOOLS DATE      (TOOLS = exchange/CLAUDE_WEB_TOOLS/mhupa)
set -e
BASE="$1"; DEV="$2"; T="$3"; DATE="$4"
echo "$DATE" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' || { echo "DATE must be YYYY-MM-DD"; exit 2; }
sh "$T/build_dev_slice2.sh" "$BASE" "$DEV" "$T" "$DATE"
python3 -I - "$DEV/tests/test_e1r3_revision3.py" "$DATE" <<'EOF'
import sys
p, date = sys.argv[1], sys.argv[2]
s = open(p, encoding='utf-8').read()
old = "self.assertEqual(chain[2]['effective_date'], '2026-11-04')"
assert s.count(old) == 1, 'the pinned-date line is not found exactly once'
s = s.replace(old, "self.assertEqual(chain[2]['effective_date'], '%s')" % date)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('pinned E_1 r3 effective_date in the test set to', date)
EOF
echo "integrated dev tree built at $DEV (E_1 r3 effective_date $DATE)"
