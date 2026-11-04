#!/bin/sh
# MHUP-A slice 1: make the dev tree from the base tree. Usage: build_dev_slice1.sh BASE DEV TOOLS DATE
set -e
BASE="$1"; DEV="$2"; T="$3"; DATE="$4"
rm -rf "$DEV"; cp -a "$BASE" "$DEV"
python3 -I "$T/make_e1r3.py" "$DEV" "$DATE"
python3 -I "$T/apply_slice1.py" "$DEV"
cp "$T/slice1_new/src/methods/_common/master_versions.py" "$DEV/src/methods/_common/"
cp "$T/slice1_new/src/methods/_common/owner_records.py" "$DEV/src/methods/_common/"
for f in src/methods/_common/game_draws_reader.py src/methods/_common/contract_dispatch.py src/methods/_common/contract_runner.py \
         src/methods/_common/walk_forward.py src/evaluation/outcome_reader.py src/evaluation/report.py src/methods/Method_Contract_Runner.py; do
  cp "$T/slice1_edited/$f" "$DEV/$f"
done
find "$DEV" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "dev tree built at $DEV"
python3 -I "$T/edit_tests_slice1.py" "$DEV"
cp "$T/slice1_new/tests/ledger_fixture.py" "$T/slice1_new/tests/mhupa_fixtures.py" "$T/slice1_new/tests/test_mhupa_master_versions.py" "$T/slice1_new/tests/test_mhupa_gates.py" "$T/slice1_new/tests/test_e1r3_revision3.py" "$DEV/tests/"
cp "$T/slice1_new/tests/fixtures/e1_r2_reference_v1.json" "$DEV/tests/fixtures/"
