#!/bin/bash
# Rehearsal of the step 2 install in disposable clones: an LF checkout and a CRLF checkout, then cases that must STOP.
# Usage: rehearse_install.sh <repository clone> <extracted package folder> <work folder> <python>
R=$1; P=$2; W=$3; PY=$4
V="$PY -I $P/VERIFY_STEP2_INSTALL.py"; G='grep -E PASS|STOP|FAIL'
ADD='git add .gitignore deploy src tests Run_Research.bat Withdraw_Variant.bat ENVIRONMENT.example.ini'
rm -rf "$W"; mkdir -p "$W"; cd "$W"
for kind in lf crlf; do
  if [ $kind = crlf ]; then git clone -q -c core.autocrlf=true "$R" $kind; else git clone -q "$R" $kind; fi
  git -C $kind config user.email rehearsal@example.invalid; git -C $kind config user.name rehearsal
  echo "== $kind checkout (core.autocrlf=$(git -C $kind config core.autocrlf || echo unset))"
  $V --repo $kind --phase pre 2>&1 | $G
  cp -r "$P/repo_overlay/." $kind/
  $V --repo $kind --phase post 2>&1 | $G
  (cd $kind && $ADD 2>/dev/null)
  echo "git status --short, by first letter: $(git -C $kind status --short | cut -c1 | sort | uniq -c | tr '\n' ' ')"
  git -C $kind commit -q -m rehearsal
  $V --repo $kind --phase committed 2>&1 | $G | sed -E 's/\([0-9a-f]{7}\)/(commit)/'
  echo "the launchers in Git and on disk: $(git -C $kind ls-files --eol Run_Research.bat Withdraw_Variant.bat | awk '{print $1, $2}' | sort -u | tr '\n' ' ')"
  echo "after the commit, git status --short prints $(git -C $kind status --short | wc -l) lines"
done
echo "== cases that must STOP"
git clone -q "$R" n1; mkdir -p n1/src/research; echo x > n1/src/research/stray.py
echo "a stray file before the install:        $($V --repo n1 --phase pre 2>&1 | $G | cut -c1-80)"
git clone -q "$R" n2; cp -r "$P/repo_overlay/." n2/; echo "# x" >> n2/src/research/scoring.py
echo "wrong bytes in a copied file:           $($V --repo n2 --phase post 2>&1 | $G | cut -c1-80)"
git clone -q "$R" n3; cp -r "$P/repo_overlay/." n3/; rm n3/src/research/withdraw.py
echo "one file not copied:                    $($V --repo n3 --phase post 2>&1 | $G | cut -c1-80)"
git clone -q "$R" n4; echo >> n4/source_data/OZLOTTO_results_master.csv
echo "a results master changed:               $($V --repo n4 --phase pre 2>&1 | $G | cut -c1-80)"
git clone -q "$R" n5; cp -r "$P/repo_overlay/." n5/; echo "# x" >> n5/src/methods/_common/contract_records.py
echo "an old shared file changed:             $($V --repo n5 --phase post 2>&1 | $G | cut -c1-80)"
git clone -q "$R" n6; cp -r "$P/repo_overlay/." n6/; git -C n6 checkout -q -- .gitignore
echo "one edited file not replaced:           $($V --repo n6 --phase post 2>&1 | $G | cut -c1-80)"
git clone -q "$R" n7; cp -r "$P/repo_overlay/." n7/; echo "x" > n7/src/methods/E_002/RECUR_MEAN_ALL_V1/VARIANT_STATUS.ini.writing
echo "a stray file in a variant folder:       $($V --repo n7 --phase post 2>&1 | $G | cut -c1-80)"
