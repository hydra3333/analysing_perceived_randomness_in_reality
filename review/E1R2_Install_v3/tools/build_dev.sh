#!/bin/bash
# Rebuild the E1R2 dev tree from the base tree: CODE-3 library, E_1 r2 changes, reference fixture, new tests, test edits.
set -e
S=/tmp/claude-0/-home-claude/5e241a26-14db-516d-9aeb-bda4dbe85524/scratchpad; H=/home/claude/work/e1r2code
rm -rf $S/e1r2_dev; cp -a $S/e1r2_base $S/e1r2_dev
cp -r $H/src_new/package_tools $S/e1r2_dev/src/
python3 -I $H/tools/make_e1r2.py $S/e1r2_dev 2026-10-31
python3 -I $H/tools/make_e1_r1_reference.py $S/e1r2_base $S/e1r2_dev/tests/fixtures/e1_r1_reference_v1.json
if [ -d $H/tests_new ]; then cp $H/tests_new/*.py $S/e1r2_dev/tests/; fi
if [ -f $H/tools/edit_tests_e1r2.py ]; then python3 -I $H/tools/edit_tests_e1r2.py $S/e1r2_dev; fi
find $S/e1r2_dev -name __pycache__ -prune -exec rm -rf {} +
echo dev tree rebuilt
