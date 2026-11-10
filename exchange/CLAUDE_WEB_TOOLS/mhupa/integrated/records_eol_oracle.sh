#!/bin/sh
# N1 oracle (owner decision D02): the three canonical install/release records under
# src/methods/_common/contract_data/install_records/ keep their LF bytes through Git on a core.autocrlf=true checkout,
# and fail without the attribute. Claude web chat, 10 November 2026. Working tool; touches only WORK (a local bare
# "origin" made from the frozen mirror; nothing is pushed anywhere else). Synthetic root: data folders removed by a local
# commit, empty source_data/ and results/ placeholders. No data is read.
# Usage: records_eol_oracle.sh MIRROR PKGDIR WORK PYTHON
set -u
MIRROR="$1"; PKG="$2"; W="$3"; PY="$4"
rm -rf "$W"; mkdir -p "$W"
REC=src/methods/_common/contract_data/install_records
IR="$PKG/repo_overlay/src/package_tools/install_records.py"
COPY="$PKG/MHUPA_COPY.py"; MAN="$PKG/PACKAGE_MANIFEST_MHUP_A.json"
fail=0
G() { git -c user.name=oracle -c user.email=oracle@invalid "$@"; }
must() { "$@" || { echo "ORACLE STOP: command failed: $*"; exit 1; }; }

records_check() {   # $1 = repo, $2 = label, $3 = expect PASS|STOP
  r="$1"; echo "=== $2"
  ( cd "$r" && git check-attr text -- $REC/*.json | sed 's/^/  attr: /'
    git ls-files --eol -- $REC | sed 's/^/  eol:  /' )
  for f in "$r"/$REC/*.json; do
    rel=${f#$r/}; w=$(sha256sum < "$f" | cut -c1-64); b=$(git -C "$r" show "HEAD:$rel" | sha256sum | cut -c1-64)
    cr=$(tr -cd '\r' < "$f" | wc -c)
    if [ "$w" = "$b" ]; then echo "  bytes: $(basename $f) worktree = blob ($w) CR=$cr"; else echo "  bytes: $(basename $f) worktree $w != blob $b CR=$cr"; fi
  done
  out=$("$PY" -I -B "$IR" validate --root "$r" 2>&1); echo "  validate: $out"
  case "$3:$out" in
    PASS:"RECORDS PASS"*) echo "  -> as expected (PASS)";;
    STOP:*STOP*) echo "  -> as expected (STOP)";;
    *) echo "  -> UNEXPECTED (wanted $3)"; fail=1;;
  esac
}

# 1. origin and the installing clone A (autocrlf=true, as on the owner's PC)
must git clone -q --bare "$MIRROR" "$W/origin.git"
must git -c core.autocrlf=true clone -q "$W/origin.git" "$W/A"; git -C "$W/A" config core.autocrlf true
A="$W/A"
must G -C "$A" rm -r -q --cached source_data results transitory_data
rm -rf "$A/source_data" "$A/results" "$A/transitory_data"; mkdir -p "$A/source_data" "$A/results"
must G -C "$A" commit -q -m "SYNTHETIC ROOT (local only)"
unset_before=$(cd "$A" && git ls-files | git check-attr --stdin text | grep -c ': text: unset$')
# the package steps that create and commit the records (barriers and copies as Appendix J; the suite and the process
# checks are not this oracle's subject)
must "$PY" -I -B "$COPY" barrier --create E --repo "$A" >/dev/null
must "$PY" -I -B "$COPY" barrier --create P --repo "$A" >/dev/null
must "$PY" -I -B "$COPY" copy --part gate --repo "$A" >/dev/null
must "$PY" -I -B "$COPY" copy --part rest --repo "$A" >/dev/null
must "$PY" -I -B "$IR" install-record --root "$A" --package MHUP_A --manifest "$MAN" >/dev/null
must G -C "$A" add --pathspec-from-file="$PKG/STAGE_PACKAGE_COMMIT.txt" 2>/dev/null
must G -C "$A" commit -q -m "package commit"
must "$PY" -I -B "$COPY" barrier --remove E --repo "$A" >/dev/null
must "$PY" -I -B "$COPY" barrier --remove P --repo "$A" >/dev/null
must "$PY" -I -B "$IR" release-record --root "$A" --package MHUP_A --manifest "$MAN" >/dev/null
must G -C "$A" add --pathspec-from-file="$PKG/STAGE_RELEASE_COMMIT.txt" 2>/dev/null
must G -C "$A" commit -q -m "release commit"
unset_after=$(cd "$A" && git ls-files | git check-attr --stdin text | grep -c ': text: unset$')
records_check "$A" "A: written by the tools, then git add and commit (autocrlf=true)" PASS
must git -C "$A" push -q origin HEAD:refs/heads/main 2>/dev/null

# 2. a fresh clone B (every file written by Git)
must git -c core.autocrlf=true clone -q "$W/origin.git" "$W/B"; git -C "$W/B" config core.autocrlf true
mkdir -p "$W/B/source_data" "$W/B/results"; rm -rf "$W/B/source_data"/* 2>/dev/null
records_check "$W/B" "B: fresh clone (autocrlf=true)" PASS

# 3. forced rewrite in B: delete and check out again, then a full renormalising checkout
rm "$W/B"/$REC/*.json; must git -C "$W/B" checkout -- $REC
records_check "$W/B" "B: records deleted and checked out again" PASS
must git -C "$W/B" rm -r -q --cached .; must git -C "$W/B" reset -q --hard
records_check "$W/B" "B: whole index dropped and reset --hard" PASS

# 4. a later update: A commits an unrelated change; B pulls it fast-forward
printf 'later\n' > "$A/README_LATER.txt"; must G -C "$A" add README_LATER.txt; must G -C "$A" commit -q -m later
must git -C "$A" push -q origin HEAD:refs/heads/main 2>/dev/null
must git -C "$W/B" pull -q --ff-only origin main
records_check "$W/B" "B: after a later fast-forward pull" PASS

# 5. negative: the attribute overridden to text (as if the N1 line were absent)
must git -c core.autocrlf=true clone -q "$W/origin.git" "$W/C"; git -C "$W/C" config core.autocrlf true
printf '%s/** text\n' "$REC" > "$W/C/.git/info/attributes"
rm "$W/C"/$REC/*.json; must git -C "$W/C" checkout -- $REC
records_check "$W/C" "C: NEGATIVE, attribute overridden to text, records rewritten" STOP

# 6. scope: the set of unconverted (-text) files grows by exactly the three records
echo "=== scope: tracked files with text unset: before the package $unset_before, after $unset_after (expected +3)"
[ $((unset_after - unset_before)) -eq 3 ] || { echo "  -> UNEXPECTED"; fail=1; }
(cd "$A" && git ls-files | git check-attr --stdin text | grep ': text: unset$' | grep -v '^source_data/\|^results/' | sed 's/^/  unset outside source_data, results: /')

[ $fail -eq 0 ] && echo "N1 ORACLE PASS" || { echo "N1 ORACLE STOP"; exit 1; }
