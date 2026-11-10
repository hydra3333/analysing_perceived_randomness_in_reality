#!/bin/sh
# MHUP-A integrated package: the development tree = the reviewed slice 2 tree (slice 1 included), built on the current
# main, with E_1 revision 3's effective_date = DATE (C01-EFF: the date the package is prepared and frozen for review).
# The one test that pins that date (tests/test_e1r3_revision3.py, written with the candidates' 2026-11-04) gets DATE by one
# counted edit, so the test keeps checking the exact date rather than any date.
# Usage: build_dev_integrated.sh BASE DEV TOOLS DATE      (TOOLS = exchange/CLAUDE_WEB_TOOLS/mhupa)
set -e
BASE="$1"; DEV="$2"; T="$3"; DATE="$4"
echo "$DATE" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' || { echo "DATE must be YYYY-MM-DD"; exit 2; }
# The slice scripts cd into the tools folders, so a relative BASE/DEV would write into the tools (10 November 2026).
for p in "$BASE" "$DEV" "$T"; do case "$p" in /*) ;; *) echo "BASE, DEV and TOOLS must be absolute paths: $p"; exit 2;; esac; done
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
python3 -I - "$DEV/.gitattributes" <<'EOF'
# N1 (found 10 November 2026; owner decision D02, approved in principle for the draft package): the install and release
# records are canonical JSON that src/methods/_common/release_records.py checks byte for byte, so Git must never convert
# their line endings on a core.autocrlf=true checkout (the R-011 pattern used for results/).
import sys
p = sys.argv[1]
s = open(p, 'rb').read()
anchor = b'results/** -text\n'
assert s.endswith(anchor) and s.count(anchor) == 1, '.gitattributes does not end with the expected results/ line'
assert b'install_records' not in s, '.gitattributes already names install_records'
s += (b'# MHUP-A install and release records: canonical JSON checked byte for byte by release_records.py, so never '
      b'converted (N1)\nsrc/methods/_common/contract_data/install_records/** -text\n')
open(p, 'wb').write(s)
print('appended the install_records -text line to .gitattributes (N1)')
EOF
echo "integrated dev tree built at $DEV (E_1 r3 effective_date $DATE)"
