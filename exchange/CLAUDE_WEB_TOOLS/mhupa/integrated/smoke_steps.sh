#!/bin/sh
# Smoke test of the DRAFT package scaffold, Appendix J steps 0-16 (suite step 10 omitted: it needs the real masters,
# which this synthetic root does not have; the suite runs separately on full clones). Synthetic root: a scratch clone
# of the frozen mirror with source_data/, results/ and transitory_data/ removed by a local commit (never pushed).
# Usage: smoke_steps.sh MIRROR PKGDIR WORK PYTHON [crlf]
set -u
MIRROR="$1"; PKGSRC="$2"; W="$3"; PY="$4"; MODE="${5:-lf}"
rm -rf "$W"; mkdir -p "$W"; cp -r "$PKGSRC" "$W/stage"; PKG="$W/stage"
if [ "$MODE" = crlf ]; then git -c core.autocrlf=true clone -q "$MIRROR" "$W/repo"; git -C "$W/repo" config core.autocrlf true
else git clone -q "$MIRROR" "$W/repo"; fi
R="$W/repo"; G="git -C $R -c user.name=smoke -c user.email=smoke@invalid"
$G rm -r -q --cached source_data results transitory_data >/dev/null && rm -rf "$R/source_data" "$R/results" "$R/transitory_data"
mkdir -p "$R/source_data" "$R/results"   # empty placeholders: process_check needs the folders to exist
$G commit -q -m "SYNTHETIC ROOT for the smoke test: data folders removed (local only)"
NOPYC="$R/transitory_data/no_pycache_ever"; PC="$PKG/repo_overlay/src/package_tools/process_check.py"
IR="$PKG/repo_overlay/src/package_tools/install_records.py"; MAN="$PKG/PACKAGE_MANIFEST_MHUP_A.json"
step() { n="$1"; shift; echo "--- step $n: $*" | cut -c1-200; "$@"; rc=$?; echo "    (exit $rc)"; [ $rc -eq 0 ] || { echo "SMOKE STOP at step $n"; exit 1; }; }
step 0 sh -c "test -z \"\$(git -C $R status --short)\" && echo clean"
step 1 "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase pre
step 2 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$PC" check-no-runs --root "$R" --install "$MAN"
step 3 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$PC" take-install-lock --root "$R" --package MHUP_A
step 4E "$PY" -I -B "$PKG/MHUPA_COPY.py" barrier --create E --repo "$R"
step 4P "$PY" -I -B "$PKG/MHUPA_COPY.py" barrier --create P --repo "$R"
step 5 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$PC" check-no-runs --root "$R" --install "$MAN"
step 6 "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part gate --repo "$R"
step 7 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$PC" check-no-runs --root "$R" --install "$MAN"
step 8 "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part rest --repo "$R"
step 9 "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase post
echo "--- step 10: the suite is OMITTED in the smoke test (synthetic root has no masters)"
step 11 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$PC" check-no-runs --root "$R" --install "$MAN"
step 12a "$PY" -I -B -X "pycache_prefix=$NOPYC" "$IR" install-record --root "$R" --package MHUP_A --manifest "$MAN"
step 12b $G add --pathspec-from-file="$PKG/STAGE_PACKAGE_COMMIT.txt"
echo "    staged lines: $($G status --short --no-renames | wc -l); not A/M/D: $($G status --short --no-renames | grep -cv '^[AMD] ')"
step 12c $G commit -q -m "MHUP-A smoke package commit"
step 13 "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase committed
step 14 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$PC" check-no-runs --root "$R" --install "$MAN"
step 15E "$PY" -I -B "$PKG/MHUPA_COPY.py" barrier --remove E --repo "$R"
step 15P "$PY" -I -B "$PKG/MHUPA_COPY.py" barrier --remove P --repo "$R"
step 16 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$IR" release-record --root "$R" --package MHUP_A --manifest "$MAN"
step 17a $G add --pathspec-from-file="$PKG/STAGE_RELEASE_COMMIT.txt"
echo "    staged: $($G status --short)"
step 17b $G commit -q -m "MHUP-A smoke release commit"
echo "--- step 17c: released phase (expected to STOP: item 3 not built)"; "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase released 2>&1 | head -2
step 18 "$PY" -I -B -X "pycache_prefix=$NOPYC" "$PC" release-install-lock --root "$R" --package MHUP_A
echo "no_pycache_ever exists: $(test -e $NOPYC && echo YES || echo no); __pycache__ in stage: $(find $PKG -name __pycache__ | wc -l); in repo src: $(find $R/src -name __pycache__ | wc -l)"
echo "final status lines: $($G status --short | wc -l); log:"; git -C $R log --oneline -3
echo "SMOKE PASS ($MODE)"
