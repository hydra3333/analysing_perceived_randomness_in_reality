#!/bin/bash
# E1-ALIGN code install end-to-end test in disposable clones (Claude, Linux). Usage: e2e_e1align.sh REPO PKGDIR WORKDIR [PYTHON]
set -u
REPO=$1; PKG=$2; W=$3; PY=${4:-python3}
rm -rf "$W"; mkdir -p "$W"; cd "$W"
V() { python3 -I "$PKG/VERIFY_E1ALIGN_INSTALL.py" --repo . --phase "$1" 2>&1 | grep -E 'PASS|STOP' | head -1; }
MOVES() { grep '^git mv' "$PKG/RENAME_FILES.cmd" | tr -d '\r' | sed 's/\\/\//g' | while read -r _ _ _ o n; do mkdir -p src/methods/E_001; eval git mv -- $o $n || echo MOVE-FAILED; done; }
STAGE() { git add -- $(grep '^  "' "$PKG/STAGE_EXACT_FILES.cmd" | tr -d '\r' | sed 's/^  "//; s/".*//; s|\\|/|g') 2>&1 | grep -v -i '^warning' ; }
fresh() { rm -rf r; if [ "$1" = crlf ]; then git clone -q -c core.autocrlf=true "$REPO" r; else git clone -q "$REPO" r; fi; cd r; git config user.email t@t; git config user.name t; }
echo "base: $(git -C "$REPO" rev-parse HEAD)  python: $($PY --version)"
for MODE in lf crlf; do
  echo "== $MODE: happy path"; fresh $MODE
  V pre; MOVES; echo "moves staged: $(git diff --cached --name-status --no-renames | wc -l) index lines"
  cp -r "$PKG/repo_overlay/." .
  [ $MODE = crlf ] && (cd "$PKG/repo_overlay" && find . -type f) | while read -r f; do perl -pi -e 's/\n/\r\n/' "$f"; done
  V post
  $PY -I "$PKG/RUN_E1ALIGN_SUITE.py" --repo . | tail -2
  $PY -I "$PKG/CHECK_E1ALIGN_IMPORTS.py" --repo . | grep -E '^RESULT|^FAIL'
  echo "untracked or changed after suite/check: $(git status --porcelain --untracked-files=all | grep -v '^R \|^ M\|^RM\|^M \|^A \|^??' | wc -l) unexpected; pycache in tree: $(find src tests -name __pycache__ | wc -l)"
  STAGE; echo "staged: $(git diff --cached --name-status | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git commit -q -m E1ALIGN; V committed
  if [ $MODE = lf ]; then
    echo "-- E1A-T13 recovery: git revert in this disposable clone"
    git revert --no-edit HEAD >/dev/null && [ -z "$(git diff --name-only "$(git -C "$REPO" rev-parse HEAD)" HEAD -- src tests doc review)" ] && echo "revert tree identical to base: yes" || echo "revert tree identical to base: NO"
    PYTHONPATH=src:src/methods:tests $PY -B -m unittest tests.test_multigame_reader_contracts tests.test_multigame_static_and_timing tests.test_multigame_launch_and_manifest tests.test_multigame_exit_receipt tests.test_multigame_science_allowlist tests.test_multigame_console_and_synthetic_scorer tests.test_t05_hardening tests.test_e1_standalone tests.test_multigame_windows_lifecycle_review 2>&1 | tail -3 | tr '\n' ' '; echo
  fi
  cd ..
done
echo "== negatives"
fresh lf; echo x > stray.txt; echo "-- pre, untracked file:"; V pre; rm stray.txt
MOVES; cp -r "$PKG/repo_overlay/." .
sed -i 's/^import json$/import json  # x/' src/methods/E_001/e1_historical_appearance_frequency.py; echo "-- post, unlisted edit on a kept line:"; V post
git checkout -q -- src/methods/E_001/e1_historical_appearance_frequency.py 2>/dev/null; cp "$PKG/repo_overlay/src/methods/E_001/e1_historical_appearance_frequency.py" src/methods/E_001/
echo 'X = 1' > src/methods/E_001/extra.py; echo "-- post, extra file in E_001:"; V post; rm src/methods/E_001/extra.py
echo '# x' >> src/methods/E_001/e1_standalone_contract.py; echo "-- post, moved-unchanged file edited:"; V post; git checkout -q -- src/methods/E_001/e1_standalone_contract.py
echo '# x' >> src/Powerball_Experiment_Coordinator.py; echo "-- post, coordinator touched:"; V post; git checkout -q -- src/Powerball_Experiment_Coordinator.py
V post
STAGE; git commit -q -m E1ALIGN
echo y > extra.txt; git add extra.txt; git commit -q --amend -m E1ALIGNx; echo "-- committed, extra file in the commit:"; V committed
python3 -I "$PKG/VERIFY_E1ALIGN_INSTALL.py" --repo . --phase committed 2>&1 | grep -E '^\[|Do NOT push' | tr '\n' ' '; echo
cd ..; rm -rf r
fresh lf; MOVES; git mv -- src/methods/E_001/multigame_e1.py src/methods/_common/multigame_e1.py; cp -r "$PKG/repo_overlay/." .; echo "-- post, one move missing:"; V post; cd ..; rm -rf r
cp -r "$PKG" dmg; printf ' ' >> dmg/repo_overlay/review/E1ALIGN_Code_Install_v1/e1align_allowlist.json; fresh lf; echo "-- damaged allowlist in package:"; python3 -I ../dmg/VERIFY_E1ALIGN_INSTALL.py --repo . --phase pre 2>&1 | grep STOP | head -1; cd ..; rm -rf r dmg
echo end
